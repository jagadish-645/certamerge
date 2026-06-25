from __future__ import annotations

from typing import Any

MISSION_OBJECTIVES = {
    "tests": "Produce test evidence for the current change context.",
    "test_result": "Produce test evidence for the current change context.",
    "ci_status": "Produce CI status evidence bound to the current change.",
    "owner_approval": "Obtain accountable owner approval for the protected risk surface.",
    "sarif_scan": "Produce code-scanning evidence with redacted finding references.",
    "dependency_reference": "Attach dependency lockfile, SBOM, or dependency scan reference evidence.",
    "lint": "Produce lint evidence for the current change context.",
    "lint_result": "Produce lint evidence for the current change context.",
    "rollback_plan": "Attach rollback plan evidence for deployment-risk movement.",
}


def repair_missions_for_missing(missing: list[dict[str, Any]], risk_surfaces: list[str]) -> list[dict[str, Any]]:
    missions: list[dict[str, Any]] = []
    for item in missing:
        proof_type = item["type"]
        normalized = proof_type.replace("_", "-")
        mission_id = f"R-{normalized.upper()}-001"
        objective = MISSION_OBJECTIVES.get(proof_type, f"Produce {proof_type} evidence for the current change context.")
        missions.append(
            {
                "mission_id": mission_id,
                "objective": objective,
                "why": item["reason"],
                "risk_surface": ",".join(risk_surfaces),
                "source_verdict": "NEEDS_EVIDENCE" if item.get("state") != "failed" else "BLOCK",
                "proof_gap_id": item["proof_id"],
                "required_proof": [proof_type],
                "human_action": f"Attach or generate {proof_type} evidence, then rerun CertaMerge.",
                "agent_prompt": f"Collect {proof_type} evidence and return only evidence references. Do not authorize the change.",
                "acceptance_criteria": f"{proof_type} evidence is present or negative, fresh, and bound to the current change.",
                "rerun_instruction": "certamerge gate --repo . --policy .certamerge.yml",
                "expected_car_change": "pending to final if all required proof passes",
            }
        )
    return missions
