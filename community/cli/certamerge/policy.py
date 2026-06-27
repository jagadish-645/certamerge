from __future__ import annotations

import hashlib
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

import yaml

from .evidence import SATISFYING_EVIDENCE_STATES, evidence_for_required, normalize_required_evidence
from .recover import recover_repo
from .repair import repair_missions_for_missing
from .risk import detect_risk_surfaces, iter_repo_files


class PolicyError(ValueError):
    pass


def load_policy(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise PolicyError(f"Policy YAML could not be parsed safely: {exc}") from exc
    if not isinstance(data, dict):
        raise PolicyError("Policy must be a YAML mapping.")
    if data.get("version") is None:
        raise PolicyError("Policy requires version.")
    if data.get("mode") not in {"observe", "proof_only", "soft_block", "hard_block"}:
        raise PolicyError("Policy mode must be observe, proof_only, soft_block, or hard_block.")
    rules = data.get("rules")
    if not isinstance(rules, list) or not rules:
        raise PolicyError("Policy requires a non-empty rules list.")
    for rule in rules:
        if not isinstance(rule, dict):
            raise PolicyError("Every rule must be a mapping.")
        for field in ("id", "when", "require", "verdict_if_missing"):
            if field not in rule:
                raise PolicyError(f"Rule is missing required field: {field}.")
        if rule["verdict_if_missing"] not in {"NEEDS_EVIDENCE", "BLOCK", "ESCALATE", "REPAIR_REQUIRED", "UNKNOWN_INSUFFICIENT_CONTEXT"}:
            raise PolicyError(f"Rule {rule['id']} has unsupported verdict_if_missing.")
    return data


def policy_hash(policy: dict[str, Any]) -> str:
    encoded = yaml.safe_dump(policy, sort_keys=True).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def match_paths(patterns: list[str], files: list[Path]) -> list[str]:
    matches: list[str] = []
    for file_path in files:
        value = file_path.as_posix()
        if any(fnmatch(value, pattern) for pattern in patterns):
            matches.append(value)
    return sorted(set(matches))


def proof_gap_for_required(required: str, rule: dict[str, Any], snapshot: dict[str, Any]) -> dict[str, Any] | None:
    item = evidence_for_required(required, snapshot)
    evidence_type = normalize_required_evidence(required)
    if item and item.get("state") in SATISFYING_EVIDENCE_STATES:
        return None
    state = item.get("state") if item else "missing"
    return {
        "proof_id": f"mp_{rule['id']}_{required}",
        "type": required,
        "normalized_type": evidence_type,
        "state": state,
        "reason": rule.get("reason") or f"Policy {rule['id']} requires {required}.",
        "evidence_id": item.get("evidence_id") if item else "",
    }


def evaluate_policy(repo: Path, policy_path: Path, scoped_files: list[str] | None = None) -> dict[str, Any]:
    repo = repo.resolve()
    policy = load_policy(policy_path)
    snapshot = recover_repo(repo)
    files = [Path(value) for value in scoped_files] if scoped_files else iter_repo_files(repo)
    if scoped_files is not None:
        snapshot = {**snapshot, "risk_surfaces": detect_risk_surfaces(files)}
    missing = []
    trace = []
    matched_rules = []
    risk_surfaces = set(snapshot["risk_surfaces"])
    for rule in policy["rules"]:
        when = rule.get("when", {})
        patterns = when.get("paths", [])
        rule_surfaces = set(when.get("risk_surfaces", []))
        path_matches = match_paths(patterns, files) if patterns else []
        surface_matches = bool(rule_surfaces & risk_surfaces) if rule_surfaces else False
        matched = bool(path_matches) or surface_matches or (not patterns and not rule_surfaces)
        if not matched:
            trace.append({"rule_id": rule["id"], "result": "not_applicable", "evidence_refs": []})
            continue
        matched_rules.append(rule)
        required_evidence = rule.get("require", {}).get("evidence", [])
        rule_missing = []
        for required in required_evidence:
            gap = proof_gap_for_required(required, rule, snapshot)
            if gap:
                rule_missing.append(gap)
        missing.extend(rule_missing)
        trace.append(
            {
                "rule_id": rule["id"],
                "result": "missing_evidence" if rule_missing else "satisfied",
                "matched_paths": path_matches,
                "evidence_refs": [item["evidence_id"] for item in snapshot["evidence"]],
            }
        )
    if not matched_rules:
        verdict = "ALLOW"
        reason = "No policy rules matched this change scope."
    elif missing:
        if any(item["state"] in {"failed", "conflicting"} for item in missing):
            verdict = "BLOCK"
        else:
            severity_order = {"NEEDS_EVIDENCE": 1, "REPAIR_REQUIRED": 2, "ESCALATE": 3, "BLOCK": 4, "UNKNOWN_INSUFFICIENT_CONTEXT": 5}
            verdict = max((rule["verdict_if_missing"] for rule in matched_rules), key=lambda state: severity_order.get(state, 0))
        reason = "; ".join(sorted({item["reason"] for item in missing}))
    else:
        verdict = "ALLOW"
        reason = "All matched policy requirements are satisfied."
    repair_missions = repair_missions_for_missing(missing, snapshot["risk_surfaces"])
    return {
        "policy": policy,
        "policy_hash": policy_hash(policy),
        "snapshot": snapshot,
        "matched_rules": matched_rules,
        "missing_proof": missing,
        "verdict": verdict,
        "policy_reason": reason,
        "verdict_trace": trace,
        "repair_missions": repair_missions,
    }
