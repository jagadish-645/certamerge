# CertaMerge Repair Mission Model v0.1

## Purpose

A Repair Mission is a finite proof-producing action generated from a missing proof gap. It is not an AI coding task, generic quality note, or open-ended remediation ticket.

Repair exists to help a user move from missing proof to verifiable proof.

## Objects

| Object | Meaning |
|---|---|
| Repair mission | Actionable proof-producing mission. |
| Source verdict | Verdict that created the mission. |
| Proof gap | Missing or failed proof that mission addresses. |
| Acceptance criteria | Objective evidence required to satisfy mission. |
| Suggested agent prompt | Optional non-authoritative prompt for an AI coding assistant. |
| Re-run instruction | Exact CertaMerge command or workflow to re-evaluate. |

## Required Fields

| Field | Required | Rule |
|---|---:|---|
| `mission_id` | yes | Stable mission ID. |
| `objective` | yes | One concrete proof outcome. |
| `why` | yes | Policy/risk reason mission exists. |
| `risk_surface` | yes | Risk surface or `unknown`. |
| `source_verdict` | yes | Verdict that created mission. |
| `proof_gap_id` | yes | Missing proof reference. |
| `required_proof` | yes | Evidence type or approval required. |
| `human_action` | yes | Exact human or owner action. |
| `agent_prompt` | optional | Advisory prompt, never proof by itself. |
| `acceptance_criteria` | yes | Evidence required to pass. |
| `rerun_instruction` | yes | Command/workflow to rerun. |
| `expected_car_change` | yes | Expected CAR state after success. |

## Mission States

| State | Meaning |
|---|---|
| `created` | Mission generated from verdict/proof gap. |
| `assigned` | Accountable owner is named. |
| `in_progress` | Work is underway outside CertaMerge. |
| `evidence_submitted` | New evidence reference exists. |
| `accepted` | Re-run accepted evidence and policy passes or moves forward. |
| `rejected` | Submitted evidence fails, is malformed, stale, insufficient, or conflicting. |
| `superseded` | New policy/change/CAR replaces mission. |
| `expired` | Mission no longer valid for current change or policy. |

## Valid Transitions

| From | To | Allowed when |
|---|---|---|
| `created` | `assigned` | Owner or role is resolved. |
| `assigned` | `in_progress` | Owner accepts work or workflow starts. |
| `in_progress` | `evidence_submitted` | Evidence reference is attached. |
| `evidence_submitted` | `accepted` | CertaMerge re-run validates evidence. |
| `evidence_submitted` | `rejected` | Evidence is failed, stale, malformed, insufficient, or conflicting. |
| any active state | `superseded` | New CAR/policy/change replaces the mission. |
| any active state | `expired` | Change or policy context is no longer current. |

## Invalid Transitions

- `created` to `accepted` without evidence and re-run.
- `in_progress` to `accepted` because an AI said it fixed the issue.
- `rejected` to `accepted` without new evidence.
- `expired` to `accepted`.
- Mission completion without CAR update or snapshot update.

## Failure States

| Failure | Required behavior |
|---|---|
| Owner unknown | Mission remains `created` and verdict may be `ESCALATE` or `UNKNOWN_INSUFFICIENT_CONTEXT`. |
| Evidence attached but stale | Mission becomes `rejected`; verdict remains `NEEDS_EVIDENCE` or `REPAIR_REQUIRED`. |
| Evidence attached but failed | Mission becomes `rejected`; verdict may become `BLOCK`. |
| Evidence malformed | Mission becomes `rejected`; parser error is recorded safely. |
| AI-generated patch with no proof | Mission remains open. |

## Example Mission

```json
{
  "mission_id": "R-AUTH-001",
  "objective": "Produce auth integration test evidence for changed auth paths.",
  "why": "Policy CM-AUTH-001 requires tests for auth risk surfaces.",
  "risk_surface": "auth",
  "source_verdict": "NEEDS_EVIDENCE",
  "proof_gap_id": "mp_auth_tests",
  "required_proof": ["tests"],
  "human_action": "Run or add auth integration tests and attach the resulting test evidence reference.",
  "agent_prompt": "Create or update auth integration tests, run them locally, and provide only the evidence reference. Do not claim authorization.",
  "acceptance_criteria": "A test evidence artifact exists, is fresh for the current change, and policy CM-AUTH-001 passes.",
  "rerun_instruction": "certamerge gate --repo . --policy .certamerge.yml",
  "expected_car_change": "pending to final if all required proof passes"
}
```

## Security And Privacy Constraints

- Repair missions must not include raw source code.
- Suggested prompts are advisory and cannot satisfy proof.
- Repair missions must not tell an AI agent to approve its own change.
- Missions must include acceptance criteria that CertaMerge can verify or reference.

## Community vs Enterprise Placement

| Capability | Community | Enterprise |
|---|---:|---:|
| Basic repair mission generation | yes | yes |
| Advisory agent prompt | yes | yes |
| Assignment workflow | owner text | governed workflow |
| Mission store | local CAR/snapshot | enterprise retention |
| Advanced mission packs | examples | paid packs |
| Repair orchestration | no | yes |

## Versioning Strategy

- Mission model starts at `0.1`.
- Mission pack versions must be recorded in CAR replay metadata.
- New mission types require examples and tests proving they produce verifiable proof.
