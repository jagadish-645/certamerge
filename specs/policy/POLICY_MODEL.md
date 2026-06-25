# CertaMerge Policy Model v0.1

## Purpose

Policy defines deterministic proof requirements for changes. Policies convert customer intent into explicit evidence, owner, repair, escalation, override, and verdict behavior.

Policy is not AI judgment, generic compliance text, or a scanner configuration file.

## Objects

| Object | Meaning |
|---|---|
| Policy | Versioned rule set that defines proof requirements and verdict behavior. |
| Policy rule | Stable condition plus requirements, reason, and missing-proof behavior. |
| Condition | Deterministic predicate over paths, risk surfaces, project type, evidence, actor, or mode. |
| Requirement | Evidence, owner, approval, repair mission, or escalation required by rule. |
| Owner reference | Accountable person, team, group, or role named by policy. |
| Enforcement mode | Observe, proof-only, soft-block, or hard-block behavior for evaluation. |
| Policy pack | Reusable versioned rule collection for a risk surface or workflow. |
| Policy version | Immutable version/hash reference used for CAR replay. |

## Policy Object

Required top-level fields:

| Field | Required | Rule |
|---|---:|---|
| `version` | yes | Policy format version, starting at `0.1`. |
| `mode` | yes | `observe`, `proof_only`, `soft_block`, or `hard_block`. |
| `rules` | yes | Non-empty array of policy rules. |
| `owners` | optional | Owner references for accountability. |
| `defaults` | optional | Default missing-proof behavior and freshness windows. |

## Rule Object

Required rule fields:

| Field | Required | Rule |
|---|---:|---|
| `id` | yes | Stable policy rule ID. |
| `when` | yes | Deterministic condition. |
| `require` | yes | Evidence, owner, approval, or repair requirements. |
| `verdict_if_missing` | yes | Allowed state when proof is missing. |
| `severity` | optional | `low`, `medium`, `high`, or `critical`. |
| `reason` | optional | Human-readable policy reason. |

## Supported v0 Conditions

| Condition | Meaning |
|---|---|
| `paths` | Glob-like path patterns. |
| `risk_surfaces` | Deterministic risk labels such as `auth`, `payments`, `config`, `deployment`, `dependency`, `database`, `generated_code`, `agent_action`. |
| `project_types` | Detected project type such as `node`, `python`, `go`, `unknown`. |
| `evidence_states` | Condition based on existing evidence state. |

## Supported v0 Requirements

| Requirement | Meaning |
|---|---|
| `evidence` | Required evidence types such as `tests`, `ci_status`, `sarif_scan`, `dependency_reference`, `owner_approval`. |
| `owner` | Accountable owner reference. |
| `repair_mission` | Repair mission type to generate when proof is missing. |

## Allowed Verdicts From Policy

- `ALLOW`
- `BLOCK`
- `NEEDS_EVIDENCE`
- `ESCALATE`
- `REPAIR_REQUIRED`
- `UNKNOWN_INSUFFICIENT_CONTEXT`

Observe mode may render `OBSERVE_ONLY_WOULD_ALLOW` or `OBSERVE_ONLY_WOULD_BLOCK` externally while preserving the same deterministic evaluation trace.

## Composition

Community v0 supports one policy file per run.

Enterprise extends composition to:

1. organization baseline;
2. workspace overlay;
3. repository policy;
4. risk-surface pack;
5. exception or emergency constraints.

More specific policy may add requirements. It may not silently weaken org-level hard-block rules. Customer policy takes precedence over vendor starter packs inside customer scope, but cannot alter CAR verifier semantics.

## Valid Transitions

| Policy state | Next state | Allowed when |
|---|---|---|
| `draft` | `valid` | Schema and deterministic validation pass. |
| `valid` | `active` | User selects policy for evaluation. |
| `active` | `superseded` | New policy version replaces it. |
| `active` | `disabled` | Customer disables policy. |
| `valid` | `invalid` | Later validation discovers unsafe ambiguity. |

## Invalid Transitions

- `invalid` to `active` without a new validated version.
- `active` to changed-in-place. Active policies are immutable for replay.
- AI-generated policy text to `active` without deterministic validation.
- Vendor pack to active customer policy without customer activation.

## Failure States

| Failure | Required behavior |
|---|---|
| YAML parse failure | Reject policy and return `UNKNOWN_INSUFFICIENT_CONTEXT` or command error before evaluation. |
| Unknown condition | Reject policy as invalid. |
| Unknown evidence type | Reject policy unless explicitly allowed by extension contract. |
| Conflicting rules | Emit conflict diagnostics; safety-critical conflicts block. |
| Missing rule ID | Reject policy. |
| Non-deterministic expression | Reject policy. |

## Example Policy

```yaml
version: 0.1
mode: observe
rules:
  - id: CM-AUTH-001
    when:
      paths:
        - "src/auth/**"
        - "app/auth/**"
      risk_surfaces:
        - auth
    require:
      evidence:
        - tests
        - owner_approval
      owner: auth-owner
      repair_mission: add-auth-test-proof
    verdict_if_missing: NEEDS_EVIDENCE
    severity: high
    reason: "Auth changes require test evidence and owner approval."
```

## Security And Privacy Constraints

- Policy parsing must use safe YAML parsing.
- Policies cannot execute code, shell commands, network calls, file reads outside declared repo metadata, or dynamic imports.
- Policy output must not include raw source code.
- Policy errors must not leak secrets from file paths, environment variables, or artifact content.

## Community vs Enterprise Placement

| Capability | Community | Enterprise |
|---|---:|---:|
| Basic YAML policy | yes | yes |
| Single-file policy evaluation | yes | yes |
| Policy version in CAR | yes | yes |
| Policy inheritance | no | yes |
| Policy simulation | no | yes |
| Conflict workflow | basic diagnostics | governed workflow |
| Rollout by org/workspace/repo | no | yes |
| Policy audit history | local files | managed store |

## Versioning Strategy

- Policy format starts at `0.1`.
- Each active policy must have a stable version and hash/reference.
- Policy changes produce new versions, not in-place mutation.
- Golden fixtures must cover valid, invalid, missing evidence, conflicting, and observe-mode policies.
