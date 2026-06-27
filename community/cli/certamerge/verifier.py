from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .car import file_hash, stable_hash
from .schema import CAR_SCHEMA, EVIDENCE_STATES


def load_car(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"CAR file could not be read: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"CAR JSON could not be parsed: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("CAR must be a JSON object.")
    return data


def _valid_sha256(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("sha256:") and len(value) == 71


def _resolve_path(path_text: str, repo_path: str | None) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    if repo_path:
        return Path(repo_path) / path
    return path


def _policy_source_errors(car: dict[str, Any]) -> list[str]:
    errors = []
    policy = car.get("policy", {})
    source = policy.get("policy_source")
    if not isinstance(source, dict):
        return errors
    recorded_hash = source.get("file_hash")
    if not _valid_sha256(recorded_hash):
        errors.append("Policy file hash is missing or invalid for policy_source.")
        return errors
    path_text = source.get("resolved_path") or source.get("path")
    if not isinstance(path_text, str) or not path_text:
        errors.append("Policy source path is missing.")
        return errors
    actual_hash = file_hash(Path(path_text))
    if actual_hash is None:
        errors.append(f"Policy source file is unavailable for verification: {path_text}.")
    elif actual_hash != recorded_hash:
        errors.append("Policy file hash does not match policy_source.file_hash.")
    return errors


def _evidence_artifact_errors(car: dict[str, Any]) -> list[str]:
    errors = []
    repository = car.get("repository", {})
    repo_path = repository.get("repo_path") if isinstance(repository, dict) else None
    for item in car.get("evidence", []):
        if not isinstance(item, dict):
            continue
        artifact_hashes = item.get("artifact_hashes", [])
        if not isinstance(artifact_hashes, list):
            continue
        for artifact in artifact_hashes:
            if not isinstance(artifact, dict):
                continue
            path_text = artifact.get("path")
            recorded_hash = artifact.get("content_hash")
            if not isinstance(path_text, str) or not path_text:
                errors.append(f"Evidence {item.get('evidence_id', '<unknown>')} has an artifact hash without a path.")
                continue
            if not _valid_sha256(recorded_hash):
                errors.append(f"Evidence artifact hash for {path_text} is missing or invalid.")
                continue
            actual_hash = file_hash(_resolve_path(path_text, repo_path if isinstance(repo_path, str) else None))
            if actual_hash is None:
                errors.append(f"Evidence artifact is unavailable for verification: {path_text}.")
            elif actual_hash != recorded_hash:
                errors.append(f"Evidence artifact hash mismatch for {path_text}.")
    return errors


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
    errors.extend(_policy_source_errors(car))
    errors.extend(_evidence_artifact_errors(car))
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
        f"Commit: {car.get('change', {}).get('current_commit_sha', '<missing>')}",
        f"Policy hash: {car.get('policy', {}).get('policy_hash', '<missing>')}",
    ]
    return "\n".join(lines)
