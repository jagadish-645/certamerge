from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from copy import deepcopy
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


def file_hash(path: Path) -> str | None:
    try:
        return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def _git(repo: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            check=False,
            text=True,
            timeout=3,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    return value or None


def _pr_number_from_ref(ref: str | None) -> str:
    if not ref:
        return "unavailable"
    match = re.match(r"refs/pull/(\d+)/", ref)
    return match.group(1) if match else "unavailable"


def change_context(repo: Path) -> dict[str, Any]:
    env = os.environ
    resolved = repo.resolve()
    github_actions = env.get("GITHUB_ACTIONS") == "true"
    github_repository = env.get("GITHUB_REPOSITORY", "")
    github_run_id = env.get("GITHUB_RUN_ID", "")
    github_server = env.get("GITHUB_SERVER_URL", "https://github.com")
    git_root = _git(resolved, "rev-parse", "--show-toplevel")
    branch = env.get("GITHUB_HEAD_REF") or _git(resolved, "rev-parse", "--abbrev-ref", "HEAD")
    current_sha = env.get("GITHUB_SHA") or _git(resolved, "rev-parse", "HEAD")
    base_sha = env.get("GITHUB_BASE_SHA") or "unavailable"
    head_sha = env.get("GITHUB_HEAD_SHA") or env.get("GITHUB_SHA") or current_sha or "unavailable"
    github_ref = env.get("GITHUB_REF", "")
    unavailable = []
    if not current_sha:
        unavailable.append("current_commit_sha")
    if not branch:
        unavailable.append("branch")
    if not git_root and not github_actions:
        unavailable.append("git_repository_context")
    source_system = "github_actions" if github_actions else "local"
    pr_number = env.get("CERTAMERGE_PR_NUMBER") or _pr_number_from_ref(github_ref)
    run_url = ""
    if github_repository and github_run_id:
        run_url = f"{github_server}/{github_repository}/actions/runs/{github_run_id}"
    return {
        "change_id": f"github:{github_repository}:pr:{pr_number}" if github_actions and pr_number != "unavailable" else "local_repo_snapshot",
        "change_type": "pull_request" if github_actions and pr_number != "unavailable" else "repo_snapshot",
        "source_system": source_system,
        "source_ref": str(repo),
        "repo_path": str(resolved),
        "branch": branch or "unavailable",
        "current_commit_sha": current_sha or "unavailable",
        "base_ref": env.get("GITHUB_BASE_REF") or base_sha,
        "head_ref": env.get("GITHUB_HEAD_REF") or head_sha,
        "base_sha": base_sha,
        "head_sha": head_sha,
        "pr_number": pr_number,
        "github_repository": github_repository or "unavailable",
        "github_ref": github_ref or "unavailable",
        "github_run_id": github_run_id or "unavailable",
        "github_run_url": run_url or "unavailable",
        "git_context_available": bool(git_root or current_sha),
        "working_tree_dirty": bool(_git(resolved, "status", "--porcelain")),
        "unavailable_context": sorted(set(unavailable)),
    }


def repo_identity(repo: Path, context: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = repo.resolve()
    context = context or {}
    github_repository = context.get("github_repository")
    provider = "github" if github_repository and github_repository != "unavailable" else "local"
    return {
        "repo_id": f"github:{github_repository}" if provider == "github" else f"local:{resolved.name}",
        "repo_name": github_repository or resolved.name,
        "repo_path": str(resolved),
        "provider": provider,
        "default_branch": "unknown",
        "metadata_only": True,
    }


def _artifact_hashes(repo: Path, evidence: list[dict[str, Any]]) -> list[dict[str, str]]:
    artifact_hashes = []
    seen: set[str] = set()
    for item in evidence:
        refs = item.get("artifact_refs")
        if not isinstance(refs, list):
            refs = []
        artifact_ref = item.get("artifact_ref")
        if isinstance(artifact_ref, str) and artifact_ref:
            refs = [artifact_ref, *refs]
        for ref in refs:
            if not isinstance(ref, str) or not ref or ref in seen:
                continue
            seen.add(ref)
            if ":" in ref and not re.match(r"^[A-Za-z]:[\\/]", ref):
                continue
            candidate = Path(ref)
            path = candidate if candidate.is_absolute() else repo / ref
            if not path.is_file():
                continue
            digest = file_hash(path)
            if digest:
                artifact_hashes.append({"path": ref, "hash_algorithm": "sha256", "content_hash": digest})
    return sorted(artifact_hashes, key=lambda item: item["path"])


def _bind_evidence_hashes(repo: Path, evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
    bound = deepcopy(evidence)
    hashes_by_path = {item["path"]: item for item in _artifact_hashes(repo, bound)}
    for item in bound:
        refs = item.get("artifact_refs")
        if not isinstance(refs, list):
            refs = []
        item_hashes = [hashes_by_path[ref] for ref in refs if isinstance(ref, str) and ref in hashes_by_path]
        artifact_ref = item.get("artifact_ref")
        if isinstance(artifact_ref, str) and artifact_ref in hashes_by_path and hashes_by_path[artifact_ref] not in item_hashes:
            item_hashes.insert(0, hashes_by_path[artifact_ref])
        if item_hashes:
            item["artifact_hashes"] = item_hashes
    return bound


def _policy_record(policy: dict[str, Any], policy_path: Path | None) -> dict[str, Any]:
    record = deepcopy(policy)
    if policy_path:
        resolved = policy_path.resolve()
        record["policy_source"] = {
            "path": str(policy_path),
            "resolved_path": str(resolved),
            "hash_algorithm": "sha256",
            "file_hash": file_hash(resolved) or "unavailable",
        }
    return record


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
    policy_path: Path | None = None,
    record_state: str | None = None,
) -> dict[str, Any]:
    created_at = utc_now()
    repo = repo.resolve()
    context = change_context(repo)
    bound_evidence = _bind_evidence_hashes(repo, evidence)
    evidence_refs = [item["evidence_id"] for item in bound_evidence if "evidence_id" in item]
    evidence_artifact_hashes = _artifact_hashes(repo, bound_evidence)
    policy_record = _policy_record(policy, policy_path)
    if record_state is None:
        record_state = "final" if verdict_state in {"ALLOW", "OBSERVE_ONLY_WOULD_ALLOW", "OBSERVE_ONLY_WOULD_BLOCK"} else "pending"
    car = {
        "car_version": CAR_VERSION,
        "car_id": f"car_{repo.name}_{hashlib.sha1(created_at.encode('utf-8')).hexdigest()[:10]}",
        "created_at": created_at,
        "record_state": record_state,
        "change": {
            **context,
            "created_at": created_at,
        },
        "repository": repo_identity(repo, context),
        "actors": [{"actor_id": "local-user", "actor_type": "human", "source": "local"}],
        "risk_surfaces": risk_surfaces,
        "policy": policy_record,
        "evidence": bound_evidence,
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
            "policy_file_hash": policy_record.get("policy_source", {}).get("file_hash", "unavailable"),
            "evaluator_version": f"certamerge-community-{__version__}",
            "evidence_snapshot_time": created_at,
            "evidence_refs": evidence_refs,
            "evidence_artifact_hashes": evidence_artifact_hashes,
            "change_binding": {
                "branch": context["branch"],
                "current_commit_sha": context["current_commit_sha"],
                "base_sha": context["base_sha"],
                "head_sha": context["head_sha"],
                "github_run_id": context["github_run_id"],
            },
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
