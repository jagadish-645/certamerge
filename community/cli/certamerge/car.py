from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import __version__
from .schema import CAR_VERSION


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stable_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def repo_identity(repo: Path) -> dict[str, Any]:
    resolved = repo.resolve()
    return {
        "repo_id": f"local:{resolved.name}",
        "repo_name": resolved.name,
        "provider": "local",
        "default_branch": "unknown",
        "metadata_only": True,
    }


def base_car(
    repo: Path,
    verdict_state: str,
    policy_reason: str,
    enforcement_effect: str,
    risk_surfaces: list[str],
    evidence: list[dict[str, Any]],
    missing_proof: list[dict[str, Any]],
    repair_missions: list[dict[str, Any]],
    verdict_trace: list[dict[str, Any]],
    policy: dict[str, Any],
    owner: str,
    next_action: str,
    record_state: str | None = None,
) -> dict[str, Any]:
    created_at = utc_now()
    evidence_refs = [item["evidence_id"] for item in evidence if "evidence_id" in item]
    if record_state is None:
        record_state = "final" if verdict_state in {"ALLOW", "OBSERVE_ONLY_WOULD_ALLOW", "OBSERVE_ONLY_WOULD_BLOCK"} else "pending"
    car = {
        "car_version": CAR_VERSION,
        "car_id": f"car_{repo.resolve().name}_{hashlib.sha1(created_at.encode('utf-8')).hexdigest()[:10]}",
        "created_at": created_at,
        "record_state": record_state,
        "change": {
            "change_id": "local_repo_snapshot",
            "change_type": "repo_snapshot",
            "source_system": "local",
            "source_ref": str(repo),
            "base_ref": "unknown",
            "head_ref": "working_tree",
            "created_at": created_at,
        },
        "repository": repo_identity(repo),
        "actors": [{"actor_id": "local-user", "actor_type": "human", "source": "local"}],
        "risk_surfaces": risk_surfaces,
        "policy": policy,
        "evidence": evidence,
        "missing_proof": missing_proof,
        "verdict": {
            "state": verdict_state,
            "policy_reason": policy_reason,
            "enforcement_effect": enforcement_effect,
        },
        "verdict_trace": verdict_trace,
        "repair_missions": repair_missions,
        "accountable_next_action": {"owner": owner, "action": next_action},
        "replay": {
            "policy_version": policy["policy_version"],
            "policy_hash": policy["policy_hash"],
            "evaluator_version": f"certamerge-community-{__version__}",
            "evidence_snapshot_time": created_at,
            "evidence_refs": evidence_refs,
            "risk_pack_versions": ["community-basic-0.1"],
            "repair_pack_versions": ["community-basic-0.1"],
        },
        "integrity": {
            "canonicalization": "certamerge-json-canonical-v0",
            "content_hash": "sha256:pending",
            "hash_algorithm": "sha256",
            "verifier_version": f"certamerge-community-{__version__}",
        },
    }
    car["integrity"]["content_hash"] = stable_hash({k: v for k, v in car.items() if k != "integrity"})
    return car


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=False) + "\n", encoding="utf-8")
