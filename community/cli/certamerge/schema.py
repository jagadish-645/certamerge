from __future__ import annotations

CAR_VERSION = "0.1"

VERDICT_STATES = {
    "ALLOW",
    "BLOCK",
    "NEEDS_EVIDENCE",
    "ESCALATE",
    "REPAIR_REQUIRED",
    "OBSERVE_ONLY_WOULD_ALLOW",
    "OBSERVE_ONLY_WOULD_BLOCK",
    "SOFT_BLOCK",
    "HARD_BLOCK",
    "OVERRIDE_RECORDED",
    "UNKNOWN_INSUFFICIENT_CONTEXT",
}

CAR_STATES = {
    "draft",
    "pending",
    "final",
    "override_recorded",
    "verification_failed",
    "superseded",
    "expired",
}

EVIDENCE_STATES = {
    "present",
    "missing",
    "unavailable",
    "stale",
    "malformed",
    "failed",
    "negative",
    "insufficient",
    "conflicting",
}

CAR_SCHEMA = {
    "type": "object",
    "required": [
        "car_version",
        "car_id",
        "created_at",
        "record_state",
        "change",
        "repository",
        "actors",
        "risk_surfaces",
        "policy",
        "evidence",
        "missing_proof",
        "verdict",
        "verdict_trace",
        "repair_missions",
        "accountable_next_action",
        "replay",
        "integrity",
    ],
    "additionalProperties": True,
    "properties": {
        "car_version": {"type": "string"},
        "car_id": {"type": "string", "minLength": 1},
        "created_at": {"type": "string", "minLength": 1},
        "record_state": {"type": "string", "enum": sorted(CAR_STATES)},
        "change": {
            "type": "object",
            "required": [
                "change_id",
                "change_type",
                "source_system",
                "source_ref",
                "base_ref",
                "head_ref",
                "created_at",
            ],
        },
        "repository": {
            "type": "object",
            "required": ["repo_id", "repo_name", "provider", "default_branch", "metadata_only"],
            "properties": {"metadata_only": {"const": True}},
        },
        "actors": {"type": "array", "minItems": 1},
        "risk_surfaces": {"type": "array"},
        "policy": {
            "type": "object",
            "required": ["policy_id", "policy_version", "mode", "policy_hash"],
        },
        "evidence": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["evidence_id", "type", "state", "source"],
                "properties": {"state": {"type": "string", "enum": sorted(EVIDENCE_STATES)}},
            },
        },
        "missing_proof": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["proof_id", "type", "state", "reason"],
                "properties": {"state": {"type": "string", "enum": sorted(EVIDENCE_STATES)}},
            },
        },
        "verdict": {
            "type": "object",
            "required": ["state", "policy_reason", "enforcement_effect"],
            "properties": {"state": {"type": "string", "enum": sorted(VERDICT_STATES)}},
        },
        "verdict_trace": {"type": "array"},
        "repair_missions": {"type": "array"},
        "accountable_next_action": {
            "type": "object",
            "required": ["owner", "action"],
        },
        "replay": {
            "type": "object",
            "required": [
                "policy_version",
                "policy_hash",
                "evaluator_version",
                "evidence_snapshot_time",
                "evidence_refs",
                "risk_pack_versions",
                "repair_pack_versions",
            ],
        },
        "integrity": {
            "type": "object",
            "required": ["canonicalization", "content_hash", "hash_algorithm", "verifier_version"],
        },
    },
}
