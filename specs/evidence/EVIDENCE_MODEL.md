# CertaMerge Evidence Model v0.1

## Purpose

Evidence is the typed, traceable input used to decide whether a change has enough proof to move forward under policy.

Evidence is not raw scanner output, raw source code, raw diffs, or AI opinion. Adapters may read external artifacts and normalize them into evidence facts or references.

## Objects

| Object | Meaning |
|---|---|
| Evidence source | Tool, workflow, person, system, or file that emits evidence. |
| Evidence artifact | External artifact or local file reference, such as SARIF, JUnit, SBOM, CI status, or approval record. |
| Evidence fact | Normalized, policy-addressable fact extracted from an artifact or source. |
| Evidence reference | Pointer to evidence without embedding sensitive raw content. |
| Evidence binding | Link from evidence to a specific change, policy rule, risk surface, and decision time. |
| Evidence integrity record | Hash, signature, timestamp, or source validation metadata. |

## Evidence Categories

| Category | Examples | Community v0 |
|---|---|---:|
| `ci_status` | CI passed/failed/unavailable. | yes |
| `test_result` | JUnit, test command status, test artifact reference. | yes |
| `lint_result` | lint artifact or command status. | yes |
| `sarif_scan` | CodeQL, Semgrep, other SARIF reference. | yes |
| `dependency_reference` | lockfile present, SBOM reference, dependency scan reference. | yes |
| `owner_approval` | CODEOWNERS or human approval reference. | yes, reference only |
| `github_actions_artifact` | workflow run/artifact URL or local artifact reference. | yes |
| `terraform_plan` | IaC plan reference and summary facts. | enterprise pack later |
| `deployment_readiness` | rollback plan, artifact provenance, environment owner. | enterprise later |
| `agent_action_context` | agent identity, scope, requested operation. | enterprise later |

## Required Fields

| Field | Required | Rule |
|---|---:|---|
| `evidence_id` | yes | Stable within CAR or snapshot. |
| `type` | yes | One evidence category. |
| `state` | yes | One evidence state. |
| `source` | yes | Tool, file, workflow, or human source. |
| `collected_at` | yes when known | Decision-time timestamp. |
| `subject_ref` | yes | Change/repo/policy/rule binding. |
| `summary` | yes | Short safe summary. |
| `artifact_ref` | optional | File path, URL, artifact ID, or hash reference. |
| `integrity` | optional | Hash/signature/source validation metadata. |
| `freshness` | optional | TTL and freshness state. |
| `sensitive` | yes | `none`, `metadata`, `restricted`, or `secret_risk`. |

## Evidence States

| State | Meaning | Verdict effect |
|---|---|---|
| `present` | Evidence exists and can be evaluated. | May satisfy proof. |
| `missing` | Required evidence does not exist or was not found. | Usually `NEEDS_EVIDENCE`. |
| `unavailable` | Source cannot be reached or artifact cannot be accessed. | `NEEDS_EVIDENCE` or `UNKNOWN_INSUFFICIENT_CONTEXT`. |
| `stale` | Evidence exists but is outside freshness window or not bound to current change. | `NEEDS_EVIDENCE`. |
| `malformed` | Evidence exists but cannot be parsed safely. | `NEEDS_EVIDENCE` or `BLOCK` for safety-critical surfaces. |
| `failed` | Evidence source ran and reported failure. | Usually `BLOCK` or `REPAIR_REQUIRED`. |
| `negative` | Evidence proves a required condition is absent or violated. | Usually `BLOCK`. |
| `insufficient` | Evidence exists but does not meet policy threshold or binding. | `NEEDS_EVIDENCE` or `REPAIR_REQUIRED`. |
| `conflicting` | Evidence facts disagree or precedence must be resolved. | `BLOCK` or `UNKNOWN_INSUFFICIENT_CONTEXT`. |

## Valid Transitions

| From | To | Allowed when |
|---|---|---|
| `missing` | `present` | Evidence is attached, generated, or found. |
| `unavailable` | `present` | Source recovers and artifact is fetched. |
| `present` | `stale` | Freshness window expires or change mutates. |
| `present` | `failed` | Source reports failed check. |
| `present` | `negative` | Evidence proves policy condition is violated. |
| `present` | `insufficient` | Evidence lacks required binding, coverage, or trust. |
| any non-terminal state | `malformed` | Parser rejects artifact safely. |
| any evaluable state | `conflicting` | Contradictory evidence is discovered. |

## Invalid Transitions

- AI advisory text cannot move evidence to `present`.
- `failed` cannot become `present` without new evidence collection.
- `stale` cannot satisfy policy without decision-time replay rules proving it was fresh at the original decision time.
- `malformed` cannot be treated as `missing` without preserving parse failure.
- `conflicting` cannot silently select the most convenient fact.

## Failure States

| Failure | Required behavior |
|---|---|
| Parser crash risk | Reject artifact safely and emit `malformed`. |
| Oversized artifact | Refuse or truncate only after retaining safe metadata and state. |
| Secret detected in artifact summary | Suppress unsafe output and emit redacted evidence state. |
| Artifact hash mismatch | Emit `conflicting` or `failed` depending policy. |
| Source outage | Emit `unavailable`, not `failed`. |
| Missing artifact path | Emit `missing`, not `failed`. |

## Example Evidence Fact

```json
{
  "evidence_id": "ev_tests_001",
  "type": "test_result",
  "state": "present",
  "source": "local",
  "collected_at": "2026-06-25T00:00:00Z",
  "subject_ref": {
    "change_id": "local_repo_snapshot",
    "policy_rule_id": "CM-AUTH-001"
  },
  "summary": "Test script configured in package metadata.",
  "artifact_ref": "package.json:test",
  "integrity": {
    "hash_algorithm": "sha256",
    "content_hash": "sha256:metadata-only-example"
  },
  "freshness": {
    "state": "fresh",
    "ttl_seconds": 86400
  },
  "sensitive": "metadata"
}
```

## Security And Privacy Constraints

- Evidence facts may include file paths, artifact names, status, counts, and hashes.
- Evidence facts must not include raw source code, raw diffs, secrets, private keys, tokens, credentials, or full scanner payloads by default.
- Evidence adapters must treat every artifact as untrusted input.
- Redaction failure suppresses output rather than emitting unsafe data.
- Evidence refs should be enough for customer-controlled replay without vendor egress.

## Community vs Enterprise Placement

| Capability | Community | Enterprise |
|---|---:|---:|
| Evidence state model | yes | yes |
| Basic adapters | yes | yes |
| Advanced scanner/IaC/deployment packs | examples only | yes |
| Evidence retention | local artifacts | governed store |
| Legal hold/deletion | no | yes |
| Cross-repo evidence memory | no | yes |

## Versioning Strategy

- Evidence model version starts at `0.1`.
- New evidence types require adapter fixtures and policy tests.
- New states require verdict-state consistency tests.
- Evidence facts used in CARs must carry enough version context for historical replay.
