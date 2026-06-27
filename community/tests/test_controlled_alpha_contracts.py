from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from certamerge.car import base_car
from certamerge.evidence import detect_signals, evidence_from_signals, normalize_required_evidence, package_json_script_state
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


def write_minimal_policy(path: Path, evidence: list[str] | None = None) -> None:
    write_text(
        path,
        yaml.safe_dump(
            {
                "version": 0.1,
                "mode": "observe",
                "rules": [
                    {
                        "id": "CHANGE-001",
                        "when": {},
                        "require": {"evidence": evidence or ["tests"]},
                        "verdict_if_missing": "NEEDS_EVIDENCE",
                        "reason": "Changes require bound proof evidence.",
                    }
                ],
            },
            sort_keys=False,
        ),
    )


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
        ("car_verification", "car_verification"),
        ("no_source_egress", "no_source_egress"),
        ("risk_surface_classification", "risk_surface_classification"),
        ("workflow_validation", "workflow_validation"),
        ("action_contract_validation", "action_contract_validation"),
        ("schema_validation", "schema_validation"),
        ("compliance_safe_language", "compliance_safe_language"),
        ("no_secret_leakage", "no_secret_leakage"),
        ("links_valid", "links_valid"),
        ("custom_evidence", "custom_evidence"),
    ],
)
def test_required_evidence_aliases_are_stable(alias: str, expected: str) -> None:
    assert normalize_required_evidence(alias) == expected


@pytest.mark.parametrize(
    ("files", "expected"),
    [
        ([Path("package.json")], "node"),
        ([Path("pyproject.toml")], "python-library"),
        ([Path("requirements.txt")], "python-library"),
        ([Path("go.mod")], "go"),
        ([Path("action.yml")], "github-action-repo"),
        ([Path("main.tf")], "terraform-iac-repo"),
        ([Path("apps/web/src/index.ts"), Path("packages/core/src/index.ts"), Path("package.json")], "monorepo-app"),
        ([Path("mkdocs.yml"), Path("docs/index.md")], "docs-heavy-repo"),
        ([Path("package.json"), Path("tsconfig.json"), Path("src/index.ts")], "node-typescript-app"),
        ([Path("README.md")], "unknown"),
    ],
)
def test_project_type_detection(files: list[Path], expected: str) -> None:
    assert detect_project_type(files) == expected


def test_project_type_ignores_nested_sample_fixtures_for_root_profile() -> None:
    files = [
        Path("pyproject.toml"),
        Path("community/cli/certamerge/cli.py"),
        Path("samples/repos/archetypes/terraform-iac-repo/main.tf"),
        Path("samples/repos/archetypes/github-action-repo/action.yml"),
    ]
    assert detect_project_type(files) == "python-library"


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
        ("main.tf", "iac"),
        ("action.yml", "github_action"),
        ("docs/index.md", "docs"),
    ],
)
def test_risk_surface_detection(file_name: str, expected_surface: str) -> None:
    assert expected_surface in detect_risk_surfaces([Path(file_name)])


def test_risk_surface_detection_ignores_nested_sample_fixtures_for_root_profile() -> None:
    files = [
        Path("pyproject.toml"),
        Path("community/cli/certamerge/cli.py"),
        Path("samples/repos/archetypes/terraform-iac-repo/main.tf"),
        Path("samples/repos/archetypes/node-typescript-app/src/auth/session.ts"),
    ]
    surfaces = detect_risk_surfaces(files)
    assert "dependency" in surfaces
    assert "iac" not in surfaces
    assert "auth" not in surfaces


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
            ("payment-change-with-tests", "NEEDS_EVIDENCE", "payments"),
            ("no-ci-vibe-repo", "NEEDS_EVIDENCE", "generated_code"),
        ],
    )
def test_recover_samples_have_expected_contract(repo_name: str, expected_verdict: str, expected_surface: str) -> None:
    snapshot = recover_repo(SAMPLES / "repos" / repo_name)
    assert snapshot["verdict"] == expected_verdict
    assert expected_surface in snapshot["risk_surfaces"]
    assert snapshot["car"]["accountable_next_action"]["owner"] == "repo-owner"


@pytest.mark.parametrize("forbidden_text", ["export function", "generatedSession", "refund(amount)", "apiKey =", "password" + " ="])
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
    rules = {rule["id"]: rule for rule in policy["rules"]}
    assert set(rules) == {
        "CM-SELF-CLI-001",
        "CM-SELF-CAR-002",
        "CM-SELF-ACTION-003",
        "CM-SELF-TESTS-004",
        "CM-SELF-SPECS-005",
        "CM-SELF-SAMPLES-006",
        "CM-SELF-DOCS-007",
        "CM-SELF-PACKAGING-008",
    }
    assert "community/cli/**" in rules["CM-SELF-CLI-001"]["when"]["paths"]
    assert ".github/workflows/**" in rules["CM-SELF-ACTION-003"]["when"]["paths"]
    assert "community/tests/**" in rules["CM-SELF-TESTS-004"]["when"]["paths"]
    assert "docs/research/**" in rules["CM-SELF-DOCS-007"]["when"]["paths"]
    assert "enterprise/**" not in json.dumps(policy)
    assert "car_verification" in rules["CM-SELF-CLI-001"]["require"]["evidence"]
    assert "schema_validation" in rules["CM-SELF-CAR-002"]["require"]["evidence"]
    assert "github_actions_artifact" in rules["CM-SELF-ACTION-003"]["require"]["evidence"]
    assert "action_contract_validation" in rules["CM-SELF-ACTION-003"]["require"]["evidence"]
    assert "no_secret_leakage" in rules["CM-SELF-DOCS-007"]["require"]["evidence"]
    assert "dependency_reference" in rules["CM-SELF-PACKAGING-008"]["require"]["evidence"]


def test_dependency_review_evidence_satisfies_dependency_reference(tmp_path: Path) -> None:
    write_json(
        tmp_path / ".certamerge" / "evidence" / "self-dogfood-dependency-review.json",
        {
            "status": "reviewed",
            "summary": "Dependency review evidence present.",
        },
    )
    files = iter_repo_files(tmp_path)
    signals = detect_signals(tmp_path, files)
    evidence = evidence_from_signals(tmp_path, signals)
    dependency = next(item for item in evidence if item["type"] == "dependency_reference")
    assert dependency["state"] == "present"
    assert dependency["artifact_refs"] == [".certamerge/evidence/self-dogfood-dependency-review.json"]


@pytest.mark.parametrize(
    ("file_name", "evidence_type"),
    [
        ("self-dogfood-car-verification.json", "car_verification"),
        ("self-dogfood-no-source-egress.json", "no_source_egress"),
        ("self-dogfood-risk-surface-classification.json", "risk_surface_classification"),
        ("self-dogfood-workflow-validation.json", "workflow_validation"),
        ("self-dogfood-action-contract-validation.json", "action_contract_validation"),
        ("self-dogfood-schema-validation.json", "schema_validation"),
        ("self-dogfood-compliance-safe-language.json", "compliance_safe_language"),
        ("self-dogfood-no-secret-leakage.json", "no_secret_leakage"),
        ("self-dogfood-links-valid.json", "links_valid"),
    ],
)
def test_metadata_evidence_files_satisfy_self_dogfood_proof_types(tmp_path: Path, file_name: str, evidence_type: str) -> None:
    write_json(
        tmp_path / ".certamerge" / "evidence" / file_name,
        {
            "status": "passed",
            "summary": f"{evidence_type} evidence present.",
        },
    )
    signals = detect_signals(tmp_path, iter_repo_files(tmp_path))
    evidence = evidence_from_signals(tmp_path, signals)
    item = next(entry for entry in evidence if entry["type"] == evidence_type)
    assert item["state"] == "present"
    assert item["artifact_refs"] == [f".certamerge/evidence/{file_name}"]


def test_conflicting_owner_approval_golden_fixtures_exist() -> None:
    approved = SAMPLES / "evidence" / "owner-approval-conflicting-approved.example.json"
    denied = SAMPLES / "evidence" / "owner-approval-conflicting-denied.example.json"
    assert json.loads(approved.read_text(encoding="utf-8"))["decision"] == "approved"
    assert json.loads(denied.read_text(encoding="utf-8"))["decision"] == "denied"


@pytest.mark.parametrize("input_name", ["policy", "repo", "output", "fail-on-block", "artifact-name", "changed-files", "base", "head"])
def test_github_action_declares_required_inputs(input_name: str) -> None:
    action = yaml.safe_load((ROOT / "community" / "github-action" / "action.yml").read_text(encoding="utf-8"))
    assert input_name in action["inputs"]


@pytest.mark.parametrize("output_name", ["car-path", "verdict", "summary-path"])
def test_github_action_declares_workflow_outputs(output_name: str) -> None:
    action = yaml.safe_load((ROOT / "community" / "github-action" / "action.yml").read_text(encoding="utf-8"))
    assert output_name in action["outputs"]


@pytest.mark.parametrize(
    "required_text",
    [
        "actions/upload-artifact@v4",
        "GITHUB_STEP_SUMMARY",
        "fail-on-block",
        "OBSERVE_ONLY_WOULD_BLOCK",
        "## CertaMerge Proof Gate",
        "Matched rules:",
        "Evidence:",
        "Missing proof:",
        "Accountable next action:",
        "python -m certamerge verify-car",
    ],
)
def test_github_action_contains_static_release_contract(required_text: str) -> None:
    action_text = (ROOT / "community" / "github-action" / "action.yml").read_text(encoding="utf-8")
    assert required_text in action_text


@pytest.mark.parametrize(
    ("repo_name", "expected_type", "expected_missing", "expected_rule"),
    [
        ("python-library", "python-library", {"dependency_reference", "security_doc", "sarif_scan"}, "PY-LIB-CODE-001"),
        ("node-typescript-app", "node-typescript-app", {"owner_approval", "sarif_scan"}, "NODE-APP-RISK-002"),
        ("github-action-repo", "github-action-repo", {"workflow_validation", "action_contract_validation", "car_verification"}, "ACTION-CONTRACT-001"),
        ("terraform-iac-repo", "terraform-iac-repo", {"terraform_validation", "terraform_plan", "owner_approval"}, "IAC-TERRAFORM-001"),
        ("monorepo-app", "monorepo-app", {"owner_approval", "security_doc", "license_file"}, "MONOREPO-APPS-001"),
        ("docs-heavy-repo", "docs-heavy-repo", {"links_valid", "compliance_safe_language"}, "DOCS-PUBLIC-001"),
    ],
)
def test_archetype_recover_is_repo_adaptive(repo_name: str, expected_type: str, expected_missing: set[str], expected_rule: str) -> None:
    snapshot = recover_repo(SAMPLES / "repos" / "archetypes" / repo_name)
    assert snapshot["profile"]["type"] == expected_type
    missing_types = {item["type"] for item in snapshot["missing_proof"]}
    assert expected_missing <= missing_types
    rule_ids = {rule["id"] for rule in snapshot["suggested_policy"]["rules"]}
    assert expected_rule in rule_ids


def test_docs_heavy_recover_avoids_generic_test_noise() -> None:
    snapshot = recover_repo(SAMPLES / "repos" / "archetypes" / "docs-heavy-repo")
    missing_types = {item["type"] for item in snapshot["missing_proof"]}
    assert "test_result" not in missing_types
    assert "owner_approval" not in missing_types


def test_suggested_archetype_policy_can_drive_gate_and_valid_car(tmp_path: Path) -> None:
    repo = SAMPLES / "repos" / "archetypes" / "terraform-iac-repo"
    snapshot = recover_repo(repo)
    policy_path = tmp_path / "terraform.suggested.certamerge.yml"
    policy_path.write_text(yaml.safe_dump(snapshot["suggested_policy"], sort_keys=False), encoding="utf-8")
    car_path = tmp_path / "terraform.car.json"
    result = gate_repo(repo, policy_path, output=car_path)
    assert result["verdict"] == "OBSERVE_ONLY_WOULD_BLOCK"
    assert {item["type"] for item in result["missing_proof"]} == {"terraform_validation", "terraform_plan", "owner_approval"}
    assert verify_car(car_path)["valid"] is True


def test_gate_car_binds_policy_file_hash(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    write_json(repo / ".certamerge" / "evidence" / "test-result.json", {"status": "passed"})
    policy_path = tmp_path / "policy.certamerge.yml"
    write_minimal_policy(policy_path)
    car_path = tmp_path / "policy-bound.car.json"

    result = gate_repo(repo, policy_path, output=car_path)

    assert result["verdict"] == "OBSERVE_ONLY_WOULD_ALLOW"
    assert verify_car(car_path)["valid"] is True
    car = json.loads(car_path.read_text(encoding="utf-8"))
    assert car["policy"]["policy_source"]["file_hash"].startswith("sha256:")
    write_minimal_policy(policy_path, ["ci_status"])
    verification = verify_car(car_path)
    assert verification["valid"] is False
    assert "Policy file hash does not match policy_source.file_hash." in verification["errors"]


def test_gate_car_binds_evidence_file_hashes(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    evidence_path = repo / ".certamerge" / "evidence" / "test-result.json"
    write_json(evidence_path, {"status": "passed"})
    policy_path = tmp_path / "policy.certamerge.yml"
    write_minimal_policy(policy_path)
    car_path = tmp_path / "evidence-bound.car.json"

    result = gate_repo(repo, policy_path, output=car_path)

    assert result["verdict"] == "OBSERVE_ONLY_WOULD_ALLOW"
    car = json.loads(car_path.read_text(encoding="utf-8"))
    test_evidence = next(item for item in car["evidence"] if item["type"] == "test_result")
    assert test_evidence["artifact_hashes"][0]["path"] == ".certamerge/evidence/test-result.json"
    assert verify_car(car_path)["valid"] is True
    write_json(evidence_path, {"status": "failed"})
    verification = verify_car(car_path)
    assert verification["valid"] is False
    assert "Evidence artifact hash mismatch for .certamerge/evidence/test-result.json." in verification["errors"]


def test_change_bound_car_records_missing_local_git_context(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ("GITHUB_ACTIONS", "GITHUB_REPOSITORY", "GITHUB_RUN_ID", "GITHUB_SHA", "GITHUB_REF", "GITHUB_HEAD_REF", "GITHUB_BASE_REF", "GITHUB_BASE_SHA", "GITHUB_HEAD_SHA"):
        monkeypatch.delenv(key, raising=False)
    repo = tmp_path / "repo"
    write_json(repo / ".certamerge" / "evidence" / "test-result.json", {"status": "passed"})
    policy_path = tmp_path / "policy.certamerge.yml"
    write_minimal_policy(policy_path)
    car_path = tmp_path / "missing-git-context.car.json"

    result = gate_repo(repo, policy_path, output=car_path)

    assert result["verdict"] == "OBSERVE_ONLY_WOULD_ALLOW"
    assert verify_car(car_path)["valid"] is True
    car = json.loads(car_path.read_text(encoding="utf-8"))
    assert car["repository"]["repo_path"] == str(repo.resolve())
    assert car["change"]["current_commit_sha"] == "unavailable"
    assert "current_commit_sha" in car["change"]["unavailable_context"]
    assert car["replay"]["change_binding"]["current_commit_sha"] == "unavailable"


def test_change_bound_car_records_github_actions_context(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GITHUB_EVENT_PATH", raising=False)
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setenv("GITHUB_REPOSITORY", "acme/widget")
    monkeypatch.setenv("GITHUB_RUN_ID", "123456")
    monkeypatch.setenv("GITHUB_SHA", "a" * 40)
    monkeypatch.setenv("GITHUB_REF", "refs/pull/17/merge")
    monkeypatch.setenv("GITHUB_HEAD_REF", "feature/proof")
    monkeypatch.setenv("GITHUB_BASE_REF", "main")
    monkeypatch.setenv("GITHUB_BASE_SHA", "b" * 40)
    monkeypatch.setenv("GITHUB_HEAD_SHA", "c" * 40)
    repo = tmp_path / "repo"
    write_json(repo / ".certamerge" / "evidence" / "test-result.json", {"status": "passed"})
    policy_path = tmp_path / "policy.certamerge.yml"
    write_minimal_policy(policy_path)
    car_path = tmp_path / "github-context.car.json"

    gate_repo(repo, policy_path, output=car_path)

    assert verify_car(car_path)["valid"] is True
    car = json.loads(car_path.read_text(encoding="utf-8"))
    assert car["repository"]["provider"] == "github"
    assert car["repository"]["repo_id"] == "github:acme/widget"
    assert car["change"]["change_type"] == "pull_request"
    assert car["change"]["pr_number"] == "17"
    assert car["change"]["github_run_id"] == "123456"
    assert car["change"]["github_run_url"] == "https://github.com/acme/widget/actions/runs/123456"
    assert car["replay"]["change_binding"]["head_sha"] == "c" * 40


@pytest.mark.parametrize(
    ("changed_file", "expected_surface"),
    [
        ("docs/index.md", "docs"),
        (".github/workflows/ci.yml", "deployment"),
        ("src/auth/session.py", "auth"),
        ("package-lock.json", "dependency"),
        ("main.tf", "iac"),
    ],
)
def test_explicit_changed_files_drive_change_scope_and_risk_surfaces(tmp_path: Path, changed_file: str, expected_surface: str) -> None:
    repo = tmp_path / "repo"
    write_text(repo / changed_file, "metadata only fixture\n")
    write_json(repo / ".certamerge" / "evidence" / "test-result.json", {"status": "passed"})
    write_minimal_policy(tmp_path / "policy.yml")
    changed_files = tmp_path / "changed-files.txt"
    write_text(changed_files, changed_file + "\n")
    car_path = tmp_path / "scoped.car.json"

    result = gate_repo(repo, tmp_path / "policy.yml", output=car_path, changed_files_path=changed_files)

    assert result["verdict"] == "OBSERVE_ONLY_WOULD_ALLOW"
    assert verify_car(car_path)["valid"] is True
    car = json.loads(car_path.read_text(encoding="utf-8"))
    assert car["change"]["change_context_mode"] == "explicit_changed_files"
    assert car["change"]["changed_files"] == [changed_file]
    assert car["change"]["changed_file_count"] == 1
    assert expected_surface in car["risk_surfaces"]


def test_git_diff_unavailable_falls_back_to_repo_snapshot_without_fake_changed_files(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    write_text(repo / "src" / "app.py", "print('ok')\n")
    write_json(repo / ".certamerge" / "evidence" / "test-result.json", {"status": "passed"})
    write_minimal_policy(tmp_path / "policy.yml")
    car_path = tmp_path / "fallback.car.json"

    result = gate_repo(repo, tmp_path / "policy.yml", output=car_path, base="missing-base", head="missing-head")

    assert result["verdict"] == "OBSERVE_ONLY_WOULD_ALLOW"
    assert verify_car(car_path)["valid"] is True
    car = json.loads(car_path.read_text(encoding="utf-8"))
    assert car["change"]["change_context_mode"] == "repo_snapshot"
    assert car["change"]["changed_files"] == []
    assert "changed_files_git_diff" in car["change"]["unavailable_context"]


def test_github_event_context_falls_back_honestly_when_changed_files_are_unavailable(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    event_path = tmp_path / "github-event.json"
    write_json(
        event_path,
        {
            "number": 42,
            "pull_request": {
                "number": 42,
                "base": {"sha": "b" * 40},
                "head": {"sha": "c" * 40},
            },
        },
    )
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event_path))
    monkeypatch.setenv("GITHUB_REPOSITORY", "acme/widget")
    monkeypatch.setenv("GITHUB_RUN_ID", "987654")
    monkeypatch.setenv("GITHUB_REF", "refs/pull/42/merge")
    monkeypatch.setenv("GITHUB_SHA", "c" * 40)
    repo = tmp_path / "repo"
    write_text(repo / "src" / "auth" / "session.py", "print('ok')\n")
    write_json(repo / ".certamerge" / "evidence" / "test-result.json", {"status": "passed"})
    write_minimal_policy(tmp_path / "policy.yml")
    car_path = tmp_path / "github-fallback.car.json"

    gate_repo(repo, tmp_path / "policy.yml", output=car_path)

    assert verify_car(car_path)["valid"] is True
    car = json.loads(car_path.read_text(encoding="utf-8"))
    assert car["change"]["change_context_mode"] == "repo_snapshot"
    assert car["change"]["pr_number"] == "42"
    assert car["change"]["base_sha"] == "b" * 40
    assert car["change"]["head_sha"] == "c" * 40
    assert car["change"]["github_run_id"] == "987654"
    assert car["change"]["changed_files"] == []
    assert "changed_files_git_diff" in car["change"]["unavailable_context"]
