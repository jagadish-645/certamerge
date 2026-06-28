# Open-Source Grand Finale Loop Log

## Loop 1

Action:
- Ran the first CGF-WTH open-source harness.

Findings:
- Recover and Gate JSON assertions used stale harness expectations.
- GitHub Action check did not match the actual invocation contract.
- README contract was incomplete for final first-screen positioning.
- No-source-egress doc did not explicitly state the no-telemetry default.
- Public evidence report contained local path evidence from pip output.

Classification:
- Critical/high: JSON contract checks, README contract, no-source-egress posture, local-path leakage.
- Medium: GitHub Action artifact/summary wording.

Fixes:
- Updated harness expectations to match current `recover`, `gate`, and `explain-car` JSON.
- Updated action contract check.
- Rewrote README.
- Updated no-source-egress doc.
- Improved report evidence sanitization.

Result:
- Rerun passed with score `4.0`.

## Loop 2

Action:
- Reran open-source harness through the root cross-product gate.

Findings:
- Result Markdown still contained `file:///C:/Users/...` install evidence.

Classification:
- Critical: public local-path leakage in generated report.

Fixes:
- Patched `public_evidence()` to sanitize file URLs and slash-normalized repo paths.

Result:
- Rerun passed with score `4.0`, `0` failures, and `0` critical/high failures.

## Stop Condition

Satisfied:

- no known critical bugs;
- no known high bugs;
- documented ready workflows pass;
- tests pass;
- build passes;
- CAR verifies;
- tampered CAR fails verification;
- public/private scan passes;
- CGF-WTH meets final-alpha threshold.

Final accepted score is capped at `4.0` because no external production proof exists.
