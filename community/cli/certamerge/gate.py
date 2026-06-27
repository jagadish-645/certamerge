from __future__ import annotations

from pathlib import Path
from typing import Any

from .car import base_car, write_json
from .policy import evaluate_policy


def gate_repo(repo: Path, policy_path: Path, output: Path | None = None) -> dict[str, Any]:
    result = evaluate_policy(repo, policy_path)
    policy = result["policy"]
    mode = policy["mode"]
    verdict = result["verdict"]
    rendered_verdict = verdict
    enforcement_effect = mode
    if mode == "observe":
        rendered_verdict = "OBSERVE_ONLY_WOULD_ALLOW" if verdict == "ALLOW" else "OBSERVE_ONLY_WOULD_BLOCK"
        enforcement_effect = "observe_only"
    owner = "repo-owner"
    if result["missing_proof"]:
        owner = "policy-owner"
    next_action = "Proceed with record." if rendered_verdict.endswith("ALLOW") or rendered_verdict == "ALLOW" else "Supply missing proof or complete repair missions, then rerun CertaMerge Gate."
    car = base_car(
        repo=repo,
        verdict_state=rendered_verdict,
        policy_reason=result["policy_reason"],
        enforcement_effect=enforcement_effect,
        risk_surfaces=result["snapshot"]["risk_surfaces"],
        evidence=result["snapshot"]["evidence"],
        missing_proof=result["missing_proof"],
        repair_missions=result["repair_missions"],
        verdict_trace=result["verdict_trace"],
        policy={
            "policy_id": policy_path.stem,
            "policy_version": str(policy["version"]),
            "mode": mode,
            "policy_hash": result["policy_hash"],
        },
        owner=owner,
        next_action=next_action,
        policy_path=policy_path,
    )
    if output:
        write_json(output, car)
    return {
        "verdict": rendered_verdict,
        "policy_reason": result["policy_reason"],
        "missing_proof": result["missing_proof"],
        "accountable_next_action": car["accountable_next_action"],
        "car_path": str(output) if output else "",
        "car": car,
    }
