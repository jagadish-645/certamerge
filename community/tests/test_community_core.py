from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from certamerge.car import base_car, write_json
from certamerge.cli import app
from certamerge.gate import gate_repo
from certamerge.recover import recover_repo
from certamerge.verifier import validate_car, verify_car

ROOT = Path(__file__).resolve().parents[2]
SAMPLES = ROOT / "samples"


def test_recover_detects_missing_proof_in_no_ci_repo() -> None:
    snapshot = recover_repo(SAMPLES / "repos" / "no-ci-vibe-repo")
    assert snapshot["verdict"] == "NEEDS_EVIDENCE"
    assert "auth" in snapshot["risk_surfaces"]
    assert "generated_code" in snapshot["risk_surfaces"]
    missing_types = {item["type"] for item in snapshot["missing_proof"]}
    assert {"test_result", "ci_status", "owner_approval"} <= missing_types
    assert snapshot["repair_missions"]


def test_gate_blocks_auth_change_in_observe_language() -> None:
    result = gate_repo(
        SAMPLES / "repos" / "auth-change-missing-tests",
        SAMPLES / "policies" / "auth.certamerge.yml",
    )
    assert result["verdict"] == "OBSERVE_ONLY_WOULD_BLOCK"
    missing_types = {item["type"] for item in result["missing_proof"]}
    assert {"tests", "owner_approval"} <= missing_types
    assert result["accountable_next_action"]["owner"] == "policy-owner"


def test_gate_allows_payment_repo_with_required_proof(tmp_path: Path) -> None:
    output = tmp_path / "payment-car.json"
    result = gate_repo(
        SAMPLES / "repos" / "payment-change-with-tests",
        SAMPLES / "policies" / "payment.certamerge.yml",
        output=output,
    )
    assert result["verdict"] == "ALLOW"
    assert result["missing_proof"] == []
    verification = verify_car(output)
    assert verification["valid"], verification["errors"]


def test_car_verifier_rejects_allow_with_missing_proof() -> None:
    car = base_car(
        repo=SAMPLES / "repos" / "basic-node-app",
        verdict_state="ALLOW",
        policy_reason="Invalid fixture intentionally includes missing proof.",
        enforcement_effect="proof_only",
        risk_surfaces=["dependency"],
        evidence=[
            {
                "evidence_id": "ev_tests",
                "type": "test_result",
                "state": "missing",
                "source": "local",
            }
        ],
        missing_proof=[
            {
                "proof_id": "mp_tests",
                "type": "tests",
                "state": "missing",
                "reason": "Tests are missing.",
            }
        ],
        repair_missions=[],
        verdict_trace=[{"rule_id": "INVALID", "result": "missing_evidence", "evidence_refs": ["ev_tests"]}],
        policy={
            "policy_id": "invalid",
            "policy_version": "0.1",
            "mode": "proof_only",
            "policy_hash": "sha256:invalid",
        },
        owner="repo-owner",
        next_action="Fix the invalid fixture.",
        record_state="final",
    )
    errors = validate_car(car)
    assert "ALLOW verdict cannot include missing_proof." in errors


def test_cli_recover_and_gate_commands(tmp_path: Path) -> None:
    runner = CliRunner()
    recover_result = runner.invoke(app, ["recover", str(SAMPLES / "repos" / "no-ci-vibe-repo")])
    assert recover_result.exit_code == 0, recover_result.output
    assert "Verdict: NEEDS_EVIDENCE" in recover_result.output

    output = tmp_path / "car.json"
    gate_result = runner.invoke(
        app,
        [
            "gate",
            "--repo",
            str(SAMPLES / "repos" / "payment-change-with-tests"),
            "--policy",
            str(SAMPLES / "policies" / "payment.certamerge.yml"),
            "--output",
            str(output),
        ],
    )
    assert gate_result.exit_code == 0, gate_result.output
    assert "Verdict: ALLOW" in gate_result.output
    assert output.exists()


def test_cli_verify_and_explain_car(tmp_path: Path) -> None:
    car_path = tmp_path / "allow-car.json"
    result = gate_repo(
        SAMPLES / "repos" / "payment-change-with-tests",
        SAMPLES / "policies" / "payment.certamerge.yml",
        output=car_path,
    )
    assert result["verdict"] == "ALLOW"
    runner = CliRunner()
    verify_result = runner.invoke(app, ["verify-car", str(car_path)])
    assert verify_result.exit_code == 0, verify_result.output
    assert '"valid": true' in verify_result.output
    explain_result = runner.invoke(app, ["explain-car", str(car_path)])
    assert explain_result.exit_code == 0, explain_result.output
    assert "Verdict: ALLOW" in explain_result.output


def test_cli_agent_json_outputs_are_machine_readable(tmp_path: Path) -> None:
    runner = CliRunner()

    recover_result = runner.invoke(app, ["recover", str(SAMPLES / "repos" / "no-ci-vibe-repo"), "--json"])
    assert recover_result.exit_code == 0, recover_result.output
    recover_payload = json.loads(recover_result.output)
    assert recover_payload["verdict"] == "NEEDS_EVIDENCE"
    assert recover_payload["missing_proof"]
    assert recover_payload["repair_missions"]

    car_path = tmp_path / "payment-car.json"
    gate_result = runner.invoke(
        app,
        [
            "gate",
            "--repo",
            str(SAMPLES / "repos" / "payment-change-with-tests"),
            "--policy",
            str(SAMPLES / "policies" / "payment.certamerge.yml"),
            "--output",
            str(car_path),
            "--json",
        ],
    )
    assert gate_result.exit_code == 0, gate_result.output
    gate_payload = json.loads(gate_result.output)
    assert gate_payload["verdict"] == "ALLOW"
    assert gate_payload["car"]["car_id"]
    assert car_path.exists()

    explain_result = runner.invoke(app, ["explain-car", str(car_path), "--json"])
    assert explain_result.exit_code == 0, explain_result.output
    explain_payload = json.loads(explain_result.output)
    assert explain_payload["verdict"] == "ALLOW"
    assert explain_payload["verification"]["valid"] is True


def test_written_sample_like_car_validates(tmp_path: Path) -> None:
    car_path = tmp_path / "recover-car.json"
    snapshot = recover_repo(SAMPLES / "repos" / "auth-change-missing-tests")
    write_json(car_path, snapshot["car"])
    verification = verify_car(car_path)
    assert verification["valid"], verification["errors"]
