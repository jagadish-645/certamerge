# CertaMerge Verdict State Machine v0.1

## Purpose

Verdict states are the only allowed user-facing decision states. They must preserve the UX grammar:

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
| Verdict | User-facing decision state emitted by deterministic evaluation. |
| Policy reason | Rule, proof requirement, or context that produced the verdict. |
| Missing proof | Evidence, approval, plan, test, scan, or context required before movement. |
| Accountable next action | Owner and action required now. |
| Enforcement mode | Whether verdict is observe, proof-only, soft-block, hard-block, deploy-gate, or agent-gate. |
| CAR status | CAR state associated with the verdict. |
| Verdict trace | Deterministic record of rules, evidence, and reasoning inputs. |

## Allowed Verdict States

| State | Meaning | CAR status |
|---|---|---|
| `ALLOW` | Current policy proof is satisfied. | final |
| `BLOCK` | Policy failed or negative/failed/conflicting proof prevents movement. | pending or final |
| `NEEDS_EVIDENCE` | Required evidence is absent, unavailable, stale, malformed, or insufficient. | pending |
| `ESCALATE` | Human owner or authority must review. | pending |
| `REPAIR_REQUIRED` | Finite proof-producing repair is required. | pending or final |
| `OBSERVE_ONLY_WOULD_ALLOW` | Observe mode says enforcement would allow. | final observation |
| `OBSERVE_ONLY_WOULD_BLOCK` | Observe mode says enforcement would block. | final observation |
| `SOFT_BLOCK` | Blocked by default with authorized override path. | pending |
| `HARD_BLOCK` | Normal override is unavailable under current policy. | pending or final |
| `OVERRIDE_RECORDED` | Authorized exception recorded while preserving original verdict. | override_recorded |
| `UNKNOWN_INSUFFICIENT_CONTEXT` | The product lacks safe context to evaluate. | pending |

## Required Verdict Fields

- `state`
- `policy_reason`
- `missing_proof`
- `accountable_next_action`
- `car_status`
- `enforcement_mode`
- `decision_time`
- `trace_ref`

## Valid State Transitions

| From | To | Allowed when |
|---|---|---|
| `UNKNOWN_INSUFFICIENT_CONTEXT` | `NEEDS_EVIDENCE` | Required context is identified as evidence gap. |
| `NEEDS_EVIDENCE` | `REPAIR_REQUIRED` | Missing proof requires concrete repair work. |
| `NEEDS_EVIDENCE` | `ALLOW` | Required evidence is supplied and policy passes. |
| `REPAIR_REQUIRED` | `ALLOW` | Repair evidence is accepted by re-evaluation. |
| `REPAIR_REQUIRED` | `BLOCK` | Repair evidence fails or negative proof appears. |
| `ESCALATE` | `ALLOW` | Required approval is valid and all proof passes. |
| `ESCALATE` | `BLOCK` | Owner rejects or required proof fails. |
| `BLOCK` | `ALLOW` | New proof or policy version changes deterministic evaluation. |
| `SOFT_BLOCK` | `OVERRIDE_RECORDED` | Authorized override is valid. |
| `SOFT_BLOCK` | `ALLOW` | Missing proof is supplied instead of override. |
| `HARD_BLOCK` | `ALLOW` | Repair or emergency process creates valid proof and new CAR. |
| observe would-state | enforcement state | Customer activates enforcement and re-evaluates under same policy. |

## Invalid Transitions

- `HARD_BLOCK` to `OVERRIDE_RECORDED` through normal override.
- `BLOCK` to `ALLOW` without new evidence, policy, or corrected classification.
- `NEEDS_EVIDENCE` to `ALLOW` through explanation text only.
- `REPAIR_REQUIRED` to `ALLOW` without re-run.
- `UNKNOWN_INSUFFICIENT_CONTEXT` to `ALLOW`.
- Any verdict change caused by LLM output.
- Any verdict change that drops CAR trace.

## Evidence-To-Verdict Mapping

| Evidence state | Typical verdict |
|---|---|
| all required evidence `present` and policy satisfied | `ALLOW` |
| required evidence `missing` | `NEEDS_EVIDENCE` |
| evidence source `unavailable` | `NEEDS_EVIDENCE` or `UNKNOWN_INSUFFICIENT_CONTEXT` |
| evidence `stale` | `NEEDS_EVIDENCE` |
| evidence `malformed` | `NEEDS_EVIDENCE` or `BLOCK` for critical surfaces |
| evidence `failed` | `BLOCK` or `REPAIR_REQUIRED` |
| evidence `negative` | `BLOCK` |
| evidence `insufficient` | `NEEDS_EVIDENCE` or `REPAIR_REQUIRED` |
| evidence `conflicting` | `BLOCK` or `UNKNOWN_INSUFFICIENT_CONTEXT` |

## Failure States

| Failure | Verdict |
|---|---|
| Policy cannot be parsed safely | `UNKNOWN_INSUFFICIENT_CONTEXT` or command error. |
| Required owner cannot be resolved | `ESCALATE` or `NEEDS_EVIDENCE`. |
| Evidence adapter fails safely | `NEEDS_EVIDENCE`. |
| Integrity check fails | `BLOCK` or CAR `verification_failed`. |
| Unsupported repo type | `UNKNOWN_INSUFFICIENT_CONTEXT` with required context. |

## Example Output Contract

```text
Verdict: NEEDS_EVIDENCE
Policy reason: CM-AUTH-001 requires tests for auth paths.
Missing proof: tests, owner_approval
Accountable next action: repo-owner must attach proof or run the repair mission, then rerun CertaMerge Gate.
CAR: pending
```

## Security And Privacy Constraints

- Verdict messages must not reveal raw source code or secrets.
- Verdicts must name policy reason and proof state, not blame developers.
- Verdicts must not say "AI says safe", "guaranteed secure", or "compliant".
- Verdicts must be reproducible from policy, evidence, risk surface, mode, and evaluator version.

## Community vs Enterprise Placement

| Capability | Community | Enterprise |
|---|---:|---:|
| Core verdict states | yes | yes |
| CLI verdict output | yes | yes |
| PR/check verdict output | GitHub Action v0 | governed integrations |
| Observe/soft/hard enforcement | observe/proof-only basics | full rollout controls |
| Override governance | record format | governed workflow |

## Versioning Strategy

- Verdict state set starts at `0.1`.
- New states require UX contract update, CAR schema update, verifier update, and golden tests.
- Renaming states is a breaking change.
