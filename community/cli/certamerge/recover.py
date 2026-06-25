from __future__ import annotations

from pathlib import Path
from typing import Any

from .car import base_car
from .evidence import detect_signals, evidence_from_signals, missing_proof_from_evidence
from .repair import repair_missions_for_missing
from .risk import detect_project_type, detect_risk_surfaces, iter_repo_files


def recover_repo(repo: Path) -> dict[str, Any]:
    repo = repo.resolve()
    files = iter_repo_files(repo)
    project_type = detect_project_type(files)
    signals = detect_signals(repo, files)
    risk_surfaces = detect_risk_surfaces(files)
    evidence = evidence_from_signals(repo, signals)
    missing = missing_proof_from_evidence(evidence, risk_surfaces)
    missions = repair_missions_for_missing(missing, risk_surfaces)
    verdict = "NEEDS_EVIDENCE" if missing else "ALLOW"
    policy = {
        "policy_id": "recover-default",
        "policy_version": "0.1",
        "mode": "observe",
        "policy_hash": "sha256:recover-default",
    }
    car = base_car(
        repo=repo,
        verdict_state=verdict,
        policy_reason="Recover checks for basic proof signals without claiming security correctness.",
        enforcement_effect="observe_only",
        risk_surfaces=risk_surfaces,
        evidence=evidence,
        missing_proof=missing,
        repair_missions=missions,
        verdict_trace=[
            {
                "rule_id": "RECOVER-BASIC-001",
                "result": "missing_evidence" if missing else "satisfied",
                "evidence_refs": [item["evidence_id"] for item in evidence],
            }
        ],
        policy=policy,
        owner="repo-owner",
        next_action="Review missing proof and complete repair missions before relying on this repo for production.",
        record_state="pending" if missing else "final",
    )
    return {
        "snapshot_version": "0.1",
        "repo": str(repo),
        "project_type": project_type,
        "signals": signals,
        "risk_surfaces": risk_surfaces,
        "evidence": evidence,
        "missing_proof": missing,
        "repair_missions": missions,
        "verdict": verdict,
        "car": car,
    }
