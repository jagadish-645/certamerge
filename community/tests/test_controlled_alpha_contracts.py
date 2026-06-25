from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from certamerge.car import base_car
from certamerge.evidence import normalize_required_evidence, package_json_script_state
from certamerge.gate import gate_repo
from certamerge.policy import PolicyError, load_policy, match_paths
from certamerge.recover import recover_repo
from certamerge.risk import detect_project_type, detect_risk_surfaces, iter_repo_files
from certamerge.verifier import validate_car, verify_car

ROOT = Path(__file__).resolve().parents[2]
SAMPLES = ROOT / "samples"


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def valid_policy() -> dict[str, str]:
    return {
        "policy_id": "test",
        "policy_version": "0.1",
        "mode": "proof_only",
        "policy_hash": "sha256:test",
    }


def minimal_evidence(state: str = "present") -> list[dict[str, str]]:
    return [{"evidence_id": "ev_tests", "type": "test_result", "state": state, "source": "local"}]


def make_car(verdict: str = "ALLOW", missing: list[dict[str, str]] | None = None, repairs: list[dict[str, str]] | None = None, record_state: str | None = None) -> dict[str, object]:
    return base_car(
        repo=SAMPLES / "repos" / "basic-node-app",
        verdict_state=verdict,
        policy_reason="test policy reason",
        enforcement_effect="proof_only",
        risk_surfaces=["dependency"],
        evidence=minimal_evidence(),
        missing_proof=missing or [],
        repair_missions=repairs or [],
        verdict_trace=[{"rule_id": "TEST", "result": "satisfied", "evidence_refs": ["ev_tests"]}],
        policy=valid_policy(),
        owner="repo-owner",
        next_action="Proceed with record.",
        record_state=record_state,
    )


@pytest.mark.parametrize(
    ("alias", "expected"),
    [
        ("tests", "test_result"),
        ("test_result", "test_result"),
        ("ci", "ci_status"),
        ("ci_status", "ci_status"),
        ("lint", "lint_result"),
        ("sarif", "sarif_scan"),
        ("security_scan", "sarif_scan"),
        ("dependency", "dependency_reference"),
        ("sbom", "dependency_reference"),
        ("owner_approval", "owner_approval"),
        ("approval", "owner_approval"),
        ("custom_evidence", "custom_evidence"),
    ],
)
def test_required_evidence_aliases_are_stable(alias: str, expected: str) -> None:
    assert normalize_required_evidence(alias) == expected


@pytest.mark.parametrize(
    ("files", "expected"),
    [
        ([Path("package.json")], "node"),
        ([Path("pyproject.toml")], "python"),
        ([Path("requirements.txt")], "python"),
        ([Path("go.mod")], "go"),
        ([Path("README.md")], "unknown"),
    ],
)
def test_project_type_detection(files: list[Path], expected: str) -> None:
    assert detect_project_type(files) == expected


@pytest.mark.parametrize(
    ("file_name", "expected_surface"),
    [
        ("src/auth/session.js", "auth"),
        ("src/payments/refund.js", "payments"),
        ("config/settings.yml", "config"),
        (".github/workflows/ci.yml", "deployment"),
        ("package-lock.json", "dependency"),
        ("db/migrations/001_init.sql", "database"),
        ("app/generated/client.ts", "generated_code"),
        ("src/login/oauth.ts", "auth"),
        ("billing/stripe-webhook.ts", "payments"),
    ],
)
def test_risk_surface_detection(file_name: str, expected_surface: str) -> None:
    assert expected_surface in detect_risk_surfaces([Path(file_name)])


@pytest.mark.parametrize(
    ("script_value", "expected_state"),
    [
        ("node tests/app.test.js", "present"),
        ("pytest", "present"),
        ("exit 1", "failed"),
        ("false", "failed"),
        ("echo \"no test specified\"", "missing"),
    ],
)
def test_package_test_script_states(tmp_path: Path, script_value: str, expected_state: str) -> None:
    write_json(tmp_path / "package.json", {"scripts": {"test": script_value}})
    assert package_json_script_state(tmp_path, "test") == expected_state


@pytest.mark.parametrize(
    "policy_value",
    [
        ["not", "mapping"],
        {"mode": "proof_only", "rules": []},
        {"version": 0.1, "mode": "unsafe", "rules": [{"id": "x"}]},
        {"version": 0.1, "mode": "proof_only", "rules": []},
        {"version": 0.1, "mode": "proof_only", "rules": ["not mapping"]},
        {"version": 0.1, "mode": "proof_only", "rules": [{"id": "x", "when": {}, "require": {}}]},
        {"version": 0.1, "mode": "proof_only", "rules": [{"id": "x", "when": {}, "require": {}, "verdict_if_missing": "MAYBE"}]},
    ],
)
def test_policy_rejects_invalid_documents(tmp_path: Path, policy_value: object) -> None:
    path = tmp_path / "bad-policy.yml"
    path.write_text(yaml.safe_dump(policy_value), encoding="utf-8")
    with pytest.raises(PolicyError):
        load_policy(path)


@pytest.mark.parametrize(
    ("patterns", "files", "expected"),
    [
        (["src/auth/**"], [Path("src/auth/session.js"), Path("README.md")], ["src/auth/session.js"]),
        (["*.md"], [Path("README.md"), Path("src/app.js")], ["README.md"]),
        (["db/**", "migrations/**"], [Path("migrations/001.sql"), Path("src/app.js")], ["migrations/001.sql"]),
        (["package*.json"], [Path("package.json"), Path("package-lock.json")], ["package-lock.json", "package.json"]),
        (["no-match/**"], [Path("src/app.js")], []),
    ],
)
def test_match_paths_is_deterministic(patterns: list[str], files: list[Path], expected: list[str]) -> None:
    assert match_paths(patterns, files) == expected


@pytest.mark.parametrize(
    ("mutator", "expected_error"),
    [
        (lambda car: car["missing_proof"].append({"proof_id": "mp", "type": "tests", "state": "missing", "reason": "missing"}), "ALLOW verdict cannot include missing_proof."),
        (lambda car: car["verdict"].update({"state": "NEEDS_EVIDENCE"}), "NEEDS_EVIDENCE verdict requires missing_proof."),
        (lambda car: car["verdict"].update({"state": "REPAIR_REQUIRED"}), "REPAIR_REQUIRED verdict requires repair_missions."),
        (lambda car: car["verdict"].update({"state": "OVERRIDE_RECORDED"}), "OVERRIDE_RECORDED requires record_state override_recorded."),
        (lambda car: (car.update({"record_state": "final"}), car["verdict"].update({"state": "NEEDS_EVIDENCE"})), "NEEDS_EVIDENCE cannot use final CAR state in v0."),
        (lambda car: car["evidence"][0].update({"state": "weird"}), "Evidence ev_tests has invalid state weird."),
        (lambda car: car["missing_proof"].append({"proof_id": "mp", "type": "tests", "state": "weird", "reason": "bad"}), "Missing proof mp has invalid state weird."),
        (lambda car: car["verdict"].update({"policy_reason": "tampered"}), "CAR integrity content_hash does not match canonical CAR content."),
    ],
)
def test_car_verifier_rejects_invalid_state_contracts(mutator: object, expected_error: str) -> None:
    car = make_car()
    mutator(car)
    assert expected_error in validate_car(car)


@pytest.mark.parametrize(
    ("sample_name", "expected_valid"),
    [
        ("allow.example.json", True),
        ("block.example.json", True),
        ("needs-evidence.example.json", True),
        ("override-recorded.example.json", True),
        ("repair-required.example.json", True),
    ],
)
def test_sample_cars_verify(sample_name: str, expected_valid: bool) -> None:
    assert verify_car(SAMPLES / "cars" / sample_name)["valid"] is expected_valid


@pytest.mark.parametrize(
    ("repo_name", "expected_verdict", "expected_surface"),
    [
        ("basic-node-app", "NEEDS_EVIDENCE", "dependency"),
        ("auth-change-missing-tests", "NEEDS_EVIDENCE", "auth"),
        ("payment-change-with-tests", "ALLOW", "payments"),
        ("no-ci-vibe-repo", "NEEDS_EVIDENCE", "generated_code"),
    ],
)
def test_recover_samples_have_expected_contract(repo_name: str, expected_verdict: str, expected_surface: str) -> None:
    snapshot = recover_repo(SAMPLES / "repos" / repo_name)
    assert snapshot["verdict"] == expected_verdict
    assert expected_surface in snapshot["risk_surfaces"]
    assert snapshot["car"]["accountable_next_action"]["owner"] == "repo-owner"


@pytest.mark.parametrize("forbidden_text", ["export function", "generatedSession", "refund(amount)", "secret", "token"])
def test_recover_and_gate_outputs_do_not_emit_raw_source_or_secret_words(forbidden_text: str) -> None:
    recover_payload = json.dumps(recover_repo(SAMPLES / "repos" / "no-ci-vibe-repo"), sort_keys=True)
    gate_payload = json.dumps(
        gate_repo(SAMPLES / "repos" / "payment-change-with-tests", SAMPLES / "policies" / "payment.certamerge.yml")["car"],
        sort_keys=True,
    )
    assert forbidden_text not in recover_payload
    assert forbidden_text not in gate_payload


def test_iter_repo_files_ignores_dependency_and_cache_dirs(tmp_path: Path) -> None:
    write_text(tmp_path / "node_modules" / "leftpad" / "index.js", "module.exports = 1\n")
    write_text(tmp_path / ".git" / "HEAD", "ref: refs/heads/main\n")
    write_text(tmp_path / "src" / "app.js", "console.log('ok')\n")
    assert iter_repo_files(tmp_path) == [Path("src/app.js")]


def test_root_example_policy_loads_safely() -> None:
    policy = load_policy(ROOT / ".certamerge.yml")
    assert policy["mode"] == "observe"
    assert {rule["id"] for rule in policy["rules"]} == {"CM-ROOT-001", "CM-ROOT-002"}


def test_conflicting_owner_approval_golden_fixtures_exist() -> None:
    approved = SAMPLES / "evidence" / "owner-approval-conflicting-approved.example.json"
    denied = SAMPLES / "evidence" / "owner-approval-conflicting-denied.example.json"
    assert json.loads(approved.read_text(encoding="utf-8"))["decision"] == "approved"
    assert json.loads(denied.read_text(encoding="utf-8"))["decision"] == "denied"


@pytest.mark.parametrize("input_name", ["policy", "repo", "output", "fail-on-block", "artifact-name"])
def test_github_action_declares_required_inputs(input_name: str) -> None:
    action = yaml.safe_load((ROOT / "community" / "github-action" / "action.yml").read_text(encoding="utf-8"))
    assert input_name in action["inputs"]


@pytest.mark.parametrize("output_name", ["car-path", "verdict", "summary-path"])
def test_github_action_declares_workflow_outputs(output_name: str) -> None:
    action = yaml.safe_load((ROOT / "community" / "github-action" / "action.yml").read_text(encoding="utf-8"))
    assert output_name in action["outputs"]


@pytest.mark.parametrize("required_text", ["actions/upload-artifact@v4", "GITHUB_STEP_SUMMARY", "fail-on-block", "OBSERVE_ONLY_WOULD_BLOCK"])
def test_github_action_contains_static_release_contract(required_text: str) -> None:
    action_text = (ROOT / "community" / "github-action" / "action.yml").read_text(encoding="utf-8")
    assert required_text in action_text
