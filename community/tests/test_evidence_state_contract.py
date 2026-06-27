from __future__ import annotations

import json
from pathlib import Path

from certamerge.car import write_json
from certamerge.evidence import detect_signals, evidence_from_signals
from certamerge.gate import gate_repo
from certamerge.risk import iter_repo_files
from certamerge.verifier import verify_car

ROOT = Path(__file__).resolve().parents[2]
SAMPLES = ROOT / "samples"


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def write_data(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def copy_fixture(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def make_repo(tmp_path: Path, package_test: str = "node tests/app.test.js") -> Path:
    repo = tmp_path / "repo"
    write_text(repo / "src" / "auth" / "session.js", "export function session() { return true; }\n")
    write_data(
        repo / "package.json",
        {
            "name": "evidence-state-fixture",
            "version": "1.0.0",
            "scripts": {"test": package_test},
        },
    )
    write_text(repo / ".github" / "workflows" / "ci.yml", "name: ci\n")
    return repo


def write_policy(path: Path, required: str) -> None:
    write_text(
        path,
        "\n".join(
            [
                "version: 0.1",
                "mode: proof_only",
                "rules:",
                "  - id: CM-STATE-001",
                "    when:",
                "      paths:",
                '        - "src/auth/**"',
                "    require:",
                "      evidence:",
                f"        - {required}",
                "    verdict_if_missing: NEEDS_EVIDENCE",
                "    severity: high",
                '    reason: "Protected auth paths require explicit proof."',
                "",
            ]
        ),
    )


def evidence_state(repo: Path, evidence_type: str) -> str:
    files = iter_repo_files(repo)
    signals = detect_signals(repo, files)
    evidence = evidence_from_signals(repo, signals)
    return next(item for item in evidence if item["type"] == evidence_type)["state"]


def test_sample_evidence_fixtures_map_to_expected_states(tmp_path: Path) -> None:
    cases = [
        ("negative-sarif", "sarif-negative.example.sarif", "reports/scan.sarif", "sarif_scan", "negative"),
        ("failed-sarif", "sarif-failed.example.sarif", "reports/scan.sarif", "sarif_scan", "failed"),
        ("malformed-sarif", "sarif-malformed.example.sarif", "reports/scan.sarif", "sarif_scan", "malformed"),
        ("stale-approval", "owner-approval-stale.example.json", ".certamerge/evidence/owner-approval.json", "owner_approval", "stale"),
        ("denied-approval", "owner-approval-denied.example.json", ".certamerge/evidence/owner-approval.json", "owner_approval", "failed"),
        ("failed-tests", "test-result-failed.example.json", ".certamerge/evidence/test-result.json", "test_result", "failed"),
    ]

    for dirname, fixture_name, target_name, evidence_type, expected_state in cases:
        repo = make_repo(tmp_path / dirname)
        copy_fixture(SAMPLES / "evidence" / fixture_name, repo / target_name)

        assert evidence_state(repo, evidence_type) == expected_state


def test_failed_test_evidence_blocks_instead_of_looking_missing(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, package_test="exit 1")
    policy = tmp_path / "policy.yml"
    write_policy(policy, "tests")

    result = gate_repo(repo, policy)

    assert result["verdict"] == "BLOCK"
    assert result["missing_proof"][0]["state"] == "failed"
    assert result["missing_proof"][0]["normalized_type"] == "test_result"


def test_malformed_sarif_is_needs_evidence_not_scanner_dump(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    write_text(repo / "reports" / "scan.sarif", "{not-json")
    policy = tmp_path / "policy.yml"
    write_policy(policy, "sarif_scan")

    result = gate_repo(repo, policy)

    assert result["verdict"] == "NEEDS_EVIDENCE"
    assert result["missing_proof"][0]["state"] == "malformed"
    assert result["missing_proof"][0]["normalized_type"] == "sarif_scan"


def test_negative_sarif_satisfies_security_scan_requirement(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    write_data(repo / "reports" / "scan.sarif", {"version": "2.1.0", "runs": [{"results": []}]})
    policy = tmp_path / "policy.yml"
    write_policy(policy, "sarif_scan")

    result = gate_repo(repo, policy)

    assert result["verdict"] == "ALLOW"
    sarif = next(item for item in result["car"]["evidence"] if item["type"] == "sarif_scan")
    assert sarif["state"] == "negative"


def test_stale_owner_approval_stays_needs_evidence(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    write_data(
        repo / ".certamerge" / "evidence" / "owner-approval.json",
        {
            "approval_id": "approval-1",
            "owner": "auth-owner",
            "decision": "approved",
            "expires_at": "2000-01-01T00:00:00Z",
        },
    )
    policy = tmp_path / "policy.yml"
    write_policy(policy, "owner_approval")

    result = gate_repo(repo, policy)

    assert result["verdict"] == "NEEDS_EVIDENCE"
    assert result["missing_proof"][0]["state"] == "stale"


def test_unavailable_test_evidence_stays_needs_evidence(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    write_data(repo / ".certamerge" / "evidence" / "test-result.json", {"status": "unavailable"})
    policy = tmp_path / "policy.yml"
    write_policy(policy, "tests")

    result = gate_repo(repo, policy)

    assert result["verdict"] == "NEEDS_EVIDENCE"
    assert result["missing_proof"][0]["state"] == "unavailable"


def test_insufficient_test_evidence_stays_needs_evidence(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    write_data(repo / ".certamerge" / "evidence" / "test-result.json", {"summary": "test evidence exists but no status is present"})
    policy = tmp_path / "policy.yml"
    write_policy(policy, "tests")

    result = gate_repo(repo, policy)

    assert result["verdict"] == "NEEDS_EVIDENCE"
    assert result["missing_proof"][0]["state"] == "insufficient"


def test_unavailable_owner_approval_stays_needs_evidence(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    write_data(repo / ".certamerge" / "evidence" / "owner-approval.json", {"owner": "auth-owner", "decision": "unavailable"})
    policy = tmp_path / "policy.yml"
    write_policy(policy, "owner_approval")

    result = gate_repo(repo, policy)

    assert result["verdict"] == "NEEDS_EVIDENCE"
    assert result["missing_proof"][0]["state"] == "unavailable"


def test_conflicting_owner_approval_blocks_and_records_conflict(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    write_data(repo / ".certamerge" / "evidence" / "owner-approval-a.json", {"owner": "auth-owner", "decision": "approved"})
    write_data(repo / ".certamerge" / "evidence" / "owner-approval-b.json", {"owner": "auth-owner", "decision": "denied"})
    policy = tmp_path / "policy.yml"
    write_policy(policy, "owner_approval")

    result = gate_repo(repo, policy)

    assert result["verdict"] == "BLOCK"
    assert result["missing_proof"][0]["state"] == "conflicting"


def test_car_verifier_detects_tampered_content_hash(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    policy = tmp_path / "policy.yml"
    car_path = tmp_path / "car.json"
    write_policy(policy, "tests")
    result = gate_repo(repo, policy)
    car = result["car"]
    car["verdict"]["policy_reason"] = "tampered after signing"
    write_json(car_path, car)

    verification = verify_car(car_path)

    assert not verification["valid"]
    assert "CAR integrity content_hash does not match canonical CAR content." in verification["errors"]
