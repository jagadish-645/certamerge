# CertaMerge Public Alpha Sample Outputs

## Recover Output

```text
Verdict: NEEDS_EVIDENCE
Policy reason: Recover checks basic proof signals without claiming security correctness.
Missing proof: test_result, ci_status, owner_approval
Accountable next action: repo-owner - Review generated repair missions and rerun CertaMerge after evidence is present.
```

## Allow Gate Output

```text
Verdict: ALLOW
Policy reason: All matched policy requirements are satisfied.
Missing proof: No missing proof required by current policy.
Accountable next action: repo-owner - Proceed with record.
CAR: .tmp/payment.car.json
```

## Observe Would-Block Output

```text
Verdict: OBSERVE_ONLY_WOULD_BLOCK
Policy reason: Observe mode records what would block without denying the change.
Missing proof: test_result, owner_approval
Accountable next action: repo-owner - Attach required proof and rerun CertaMerge.
```

## Verification Output

```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "verdict": "ALLOW"
}
```

## Output Contract

Every user-facing output should preserve this order:

```text
Verdict.
Policy reason.
Missing proof.
Accountable next action.
Change Authorization Record.
```
