# CertaMerge Change Authorization Record Spec v0.1

## Purpose

The Change Authorization Record, or CAR, is the durable proof record for a repository, pull request, release, deployment, or agent action decision.

A CAR is not a log line, dashboard row, AI summary, scanner report, or compliance certificate. It records the deterministic authorization context:

```text
Verdict.
Policy reason.
Missing proof.
Accountable next action.
Change Authorization Record.
```

## Objects

| Object | Meaning |
|---|---|
| CAR | Durable record that binds change identity, policy, evidence, verdict, trace, and replay metadata. |
| Change identity | Stable identity for the evaluated repo/change/action. |
| Repository identity | Metadata-only repository reference. Raw source is excluded. |
| Actor identity | Human, bot, service, or agent identity involved in authoring, approving, overriding, or running the change. |
| Evidence reference | Typed reference to evidence facts or artifacts used by policy. |
| Missing proof | Required proof not present, stale, unavailable, malformed, insufficient, failed, negative, or conflicting. |
| Verdict trace | Deterministic explanation of evaluated rules and evidence states. |
| Repair mission | Proof-producing action required to satisfy missing proof. |
| Integrity metadata | Hashes, canonicalization metadata, verifier version, optional signature, and replay references. |

## Required Fields

| Field | Required | Type | Rule |
|---|---:|---|---|
| `car_version` | yes | string | Current value: `0.1`. |
| `car_id` | yes | string | Stable unique ID. |
| `created_at` | yes | RFC 3339 string | CAR creation timestamp. |
| `record_state` | yes | enum | One of the CAR states below. |
| `change` | yes | object | Change identity and source. |
| `repository` | yes | object | Metadata-only repo identity. |
| `actors` | yes | array | Author/source/approver/runner identities. |
| `risk_surfaces` | yes | array | Deterministic risk surfaces or `unknown`. |
| `policy` | yes | object | Policy ID, version, mode, and hash/reference when available. |
| `evidence` | yes | array | Evidence references or normalized evidence facts. |
| `missing_proof` | yes | array | Required proof gaps. Empty only for `ALLOW` or valid `OVERRIDE_RECORDED`. |
| `verdict` | yes | object | Verdict state and reason. |
| `verdict_trace` | yes | array | Rule/evidence trace entries. |
| `repair_missions` | yes | array | Finite proof-producing missions. Empty when no repair is required. |
| `accountable_next_action` | yes | object | Owner and action. |
| `replay` | yes | object | Versions and references needed to replay decision. |
| `integrity` | yes | object | Canonicalization and hash metadata. |

## Change Object

Required fields:

- `change_id`
- `change_type`: `repo_snapshot`, `pull_request`, `release`, `deployment`, or `agent_action`
- `source_system`: `local`, `github`, `gitlab`, `ci`, `release_system`, `deployment_system`, or `agent_runtime`
- `source_ref`
- `base_ref`
- `head_ref`
- `created_at`

Raw source code and raw diff content are forbidden in this object.

## Repository Object

Required fields:

- `repo_id`
- `repo_name`
- `provider`
- `default_branch`
- `metadata_only`: must be `true`

Allowed metadata includes file paths, counts, package manager names, CI config presence, evidence artifact references, and policy references. File contents are forbidden by default.

## CAR States

| State | Meaning |
|---|---|
| `draft` | CAR is generated before complete decision evidence is finalized. |
| `pending` | CAR records a block, escalation, evidence gap, repair requirement, or unresolved context. |
| `final` | CAR records an allow, block, hard block, final repair-required state, or final observe result. |
| `override_recorded` | CAR records an authorized exception while preserving original verdict. |
| `verification_failed` | CAR exists but verifier found schema, integrity, or consistency failure. |
| `superseded` | A newer CAR replaces this one for the same change after new evidence or policy. |
| `expired` | CAR record is past retention or evidence validity window but remains historically interpretable if retained. |

## Valid Transitions

| From | To | Allowed when |
|---|---|---|
| `draft` | `pending` | Missing proof, escalation, repair, unknown, or block is emitted. |
| `draft` | `final` | Evaluation has complete proof and final verdict. |
| `pending` | `final` | Required proof arrives and re-evaluation finalizes, or block remains final. |
| `pending` | `override_recorded` | Authorized override is recorded with scope, owner, reason, and expiry. |
| `final` | `superseded` | Change, policy, evidence, or replay context changes. |
| `override_recorded` | `superseded` | New evaluation replaces the override record. |
| any active state | `verification_failed` | Verifier detects invalid schema, integrity, or consistency. |
| `final` | `expired` | Retention policy expires record while preserving export/replay rules if retained. |

## Invalid Transitions

- `verification_failed` to `final` without creating a corrected superseding CAR.
- `override_recorded` to `ALLOW` without preserving original verdict and override trace.
- `pending` to `final` with missing proof silently removed.
- `draft` to `expired`.
- Any transition caused by AI advisory text.

## Verdict Consistency Rules

| Verdict | Required CAR state | Required proof behavior |
|---|---|---|
| `ALLOW` | `final` | `missing_proof` must be empty. Evidence must satisfy policy. |
| `BLOCK` | `pending` or `final` | Missing, failed, negative, or conflicting proof must explain block. |
| `NEEDS_EVIDENCE` | `pending` | Missing proof must name unavailable/stale/malformed/absent evidence. |
| `ESCALATE` | `pending` | Accountable owner must be present. |
| `REPAIR_REQUIRED` | `pending` or `final` | At least one repair mission must exist. |
| `OBSERVE_ONLY_WOULD_ALLOW` | `final` | Enforcement mode must be observe. |
| `OBSERVE_ONLY_WOULD_BLOCK` | `final` | Enforcement mode must be observe. |
| `SOFT_BLOCK` | `pending` | Override path must be defined. |
| `HARD_BLOCK` | `pending` or `final` | Normal override path must be absent. |
| `OVERRIDE_RECORDED` | `override_recorded` | Original verdict, owner, scope, reason, and expiry must be recorded. |
| `UNKNOWN_INSUFFICIENT_CONTEXT` | `pending` | Required context must be listed. |

## Integrity And Replay

`integrity` fields:

- `canonicalization`: required string.
- `content_hash`: required string when available.
- `hash_algorithm`: required string when `content_hash` is present.
- `signature`: optional object.
- `verifier_version`: required string.

`replay` fields:

- `policy_version`
- `policy_hash`
- `evaluator_version`
- `evidence_snapshot_time`
- `evidence_refs`
- `risk_pack_versions`
- `repair_pack_versions`

Historical replay must use decision-time policy and evidence states, not current policy.

## Example CAR

```json
{
  "car_version": "0.1",
  "car_id": "car_local_20260625_0001",
  "created_at": "2026-06-25T00:00:00Z",
  "record_state": "pending",
  "change": {
    "change_id": "local_repo_snapshot",
    "change_type": "repo_snapshot",
    "source_system": "local",
    "source_ref": ".",
    "base_ref": "unknown",
    "head_ref": "working_tree",
    "created_at": "2026-06-25T00:00:00Z"
  },
  "repository": {
    "repo_id": "local:certamerge-sample",
    "repo_name": "certamerge-sample",
    "provider": "local",
    "default_branch": "main",
    "metadata_only": true
  },
  "actors": [
    {
      "actor_id": "local-user",
      "actor_type": "human",
      "source": "local"
    }
  ],
  "risk_surfaces": ["auth"],
  "policy": {
    "policy_id": "local-policy",
    "policy_version": "0.1",
    "mode": "observe",
    "policy_hash": "sha256:policy-example"
  },
  "evidence": [
    {
      "evidence_id": "ev_tests_absent",
      "type": "test_result",
      "state": "missing",
      "source": "local"
    }
  ],
  "missing_proof": [
    {
      "proof_id": "mp_auth_tests",
      "type": "tests",
      "state": "missing",
      "reason": "Policy CM-AUTH-001 requires test evidence for auth paths."
    }
  ],
  "verdict": {
    "state": "NEEDS_EVIDENCE",
    "policy_reason": "CM-AUTH-001 requires tests for auth paths.",
    "enforcement_effect": "observe_only"
  },
  "verdict_trace": [
    {
      "rule_id": "CM-AUTH-001",
      "result": "missing_evidence",
      "evidence_refs": ["ev_tests_absent"]
    }
  ],
  "repair_missions": [
    {
      "mission_id": "R-AUTH-001",
      "objective": "Produce auth test evidence for changed auth paths.",
      "acceptance": "Test evidence artifact exists and policy CM-AUTH-001 passes."
    }
  ],
  "accountable_next_action": {
    "owner": "repo-owner",
    "action": "Attach or generate required auth test evidence, then rerun CertaMerge Gate."
  },
  "replay": {
    "policy_version": "0.1",
    "policy_hash": "sha256:policy-example",
    "evaluator_version": "certamerge-community-0.1",
    "evidence_snapshot_time": "2026-06-25T00:00:00Z",
    "evidence_refs": ["ev_tests_absent"],
    "risk_pack_versions": ["community-basic-0.1"],
    "repair_pack_versions": ["community-basic-0.1"]
  },
  "integrity": {
    "canonicalization": "certamerge-json-canonical-v0",
    "content_hash": "sha256:not-yet-signed-example",
    "hash_algorithm": "sha256",
    "verifier_version": "certamerge-community-0.1"
  }
}
```

## Security And Privacy Constraints

- Raw source code is forbidden in CARs by default.
- Raw diffs are forbidden in CARs by default.
- Secrets, tokens, credentials, private keys, and unredacted scanner payloads are forbidden.
- CARs may contain metadata, evidence states, artifact hashes, file paths, counts, policy IDs, and owner references.
- CAR verification must work without trusting an enterprise control plane.

## Community vs Enterprise Placement

| Capability | Community | Enterprise |
|---|---:|---:|
| CAR spec | yes | yes |
| CAR verifier | yes | yes |
| local CAR generation | yes | yes |
| CAR storage/query/retention | local files | managed self-hosted store |
| CAR audit export bundles | basic examples | enterprise export workflows |
| override governance | record format | governed workflow and retention |
| historical replay | local verifier scope | org-wide replay and ProofGraph |

## Versioning Strategy

- `car_version` changes only for record format changes.
- Verifiers must reject unknown major versions and warn on newer minor versions.
- Historical CARs must remain verifiable by pinned or compatibility verifier versions.
- Schema changes require golden CAR fixtures for every supported verdict state.
