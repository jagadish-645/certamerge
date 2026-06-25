from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .car import stable_hash
from .schema import CAR_SCHEMA, EVIDENCE_STATES


def load_car(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"CAR JSON could not be parsed: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("CAR must be a JSON object.")
    return data


def validate_car(car: dict[str, Any]) -> list[str]:
    errors = [error.message for error in Draft202012Validator(CAR_SCHEMA).iter_errors(car)]
    verdict = car.get("verdict", {}).get("state")
    record_state = car.get("record_state")
    missing = car.get("missing_proof", [])
    repair = car.get("repair_missions", [])
    evidence = car.get("evidence", [])
    if verdict == "ALLOW" and missing:
        errors.append("ALLOW verdict cannot include missing_proof.")
    if verdict == "NEEDS_EVIDENCE" and not missing:
        errors.append("NEEDS_EVIDENCE verdict requires missing_proof.")
    if verdict == "REPAIR_REQUIRED" and not repair:
        errors.append("REPAIR_REQUIRED verdict requires repair_missions.")
    if verdict == "OVERRIDE_RECORDED" and record_state != "override_recorded":
        errors.append("OVERRIDE_RECORDED requires record_state override_recorded.")
    if record_state == "final" and verdict in {"NEEDS_EVIDENCE", "SOFT_BLOCK"}:
        errors.append(f"{verdict} cannot use final CAR state in v0.")
    for item in evidence:
        state = item.get("state")
        if state not in EVIDENCE_STATES:
            errors.append(f"Evidence {item.get('evidence_id', '<unknown>')} has invalid state {state}.")
    for item in missing:
        state = item.get("state")
        if state not in EVIDENCE_STATES:
            errors.append(f"Missing proof {item.get('proof_id', '<unknown>')} has invalid state {state}.")
    integrity = car.get("integrity", {})
    content_hash = integrity.get("content_hash")
    if isinstance(content_hash, str) and content_hash.startswith("sha256:") and content_hash != "sha256:pending":
        computed = stable_hash({key: value for key, value in car.items() if key != "integrity"})
        if content_hash != computed:
            errors.append("CAR integrity content_hash does not match canonical CAR content.")
    return sorted(set(errors))


def verify_car(path: Path) -> dict[str, Any]:
    try:
        car = load_car(path)
        errors = validate_car(car)
    except ValueError as exc:
        return {"valid": False, "errors": [str(exc)], "warnings": [], "car_id": "", "verdict": ""}
    return {
        "valid": not errors,
        "errors": errors,
        "warnings": [],
        "car_id": car.get("car_id", ""),
        "verdict": car.get("verdict", {}).get("state", ""),
    }


def explain_car(path: Path) -> str:
    car = load_car(path)
    verdict = car.get("verdict", {})
    missing = car.get("missing_proof", [])
    next_action = car.get("accountable_next_action", {})
    lines = [
        f"CAR: {car.get('car_id', '<missing>')}",
        f"Verdict: {verdict.get('state', '<missing>')}",
        f"Policy reason: {verdict.get('policy_reason', '<missing>')}",
        "Missing proof: " + (", ".join(item.get("type", "unknown") for item in missing) if missing else "No missing proof required by current policy."),
        f"Accountable next action: {next_action.get('owner', '<missing>')} - {next_action.get('action', '<missing>')}",
        f"CAR state: {car.get('record_state', '<missing>')}",
    ]
    return "\n".join(lines)
