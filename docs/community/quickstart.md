# Community Quickstart

This quickstart proves the community spine locally: Recover finds proof gaps, Gate evaluates a policy, the verifier checks the generated CAR, and explain renders the decision in human language.

## Requirements

- Python 3.11 or newer.
- A shell running from the CertaMerge repository root.
- No cloud account, hosted service, token, or LLM API is required.

## Install

```powershell
python -m pip install -e .
```

Confirm the module route:

```powershell
python -m certamerge --help
```

Expected commands:

```text
verify-car
explain-car
recover
gate
```

If the console script is on your PATH, this should also work:

```powershell
certamerge --help
```

## Run Local Recover

```powershell
python -m certamerge recover samples/repos/no-ci-vibe-repo
```

Expected shape:

```text
Verdict: NEEDS_EVIDENCE
Policy reason: Recover checks basic proof signals without claiming security correctness.
Missing proof: test_result, ci_status, owner_approval
Accountable next action: repo-owner - Review generated repair missions and rerun CertaMerge after evidence is present.
```

Recover is for repo-level proof gaps. It is useful before you write a policy because it shows whether a repo has the minimum evidence signals a reviewer would ask for.

## Run Proof-Only Gate

```powershell
python -m certamerge gate --repo samples/repos/payment-change-with-tests --policy samples/policies/payment.certamerge.yml --output .tmp/payment.car.json
```

Expected shape:

```text
Verdict: ALLOW
Policy reason: All matched policy requirements are satisfied.
Missing proof: No missing proof required by current policy.
Accountable next action: repo-owner - Proceed with record.
CAR: .tmp/payment.car.json
```

Gate evaluates a repo snapshot against a CertaMerge policy and writes a Change Authorization Record when `--output` is provided.

## Verify The CAR

```powershell
python -m certamerge verify-car .tmp/payment.car.json
```

Expected shape:

```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "car_id": "car_payment-change-with-tests_...",
  "verdict": "ALLOW"
}
```

The verifier checks schema rules, verdict consistency, evidence-state consistency, and the CAR content hash.

## Explain The CAR

```powershell
python -m certamerge explain-car .tmp/payment.car.json
```

Expected shape:

```text
CAR: car_payment-change-with-tests_...
Verdict: ALLOW
Policy reason: All matched policy requirements are satisfied.
Missing proof: No missing proof required by current policy.
Accountable next action: repo-owner - Proceed with record.
CAR state: final
```

## Try A Would-Block Sample

```powershell
python -m certamerge gate --repo samples/repos/auth-change-missing-tests --policy samples/policies/auth.certamerge.yml --output .tmp/auth.car.json
python -m certamerge explain-car .tmp/auth.car.json
```

Expected verdict:

```text
OBSERVE_ONLY_WOULD_BLOCK
```

This sample demonstrates the safe rollout posture: CertaMerge can show what would block without breaking a team during initial adoption.

## Run CertaMerge On CertaMerge

This repository includes a self-dogfood observe-mode policy:

```powershell
python -m certamerge gate --repo . --policy .certamerge.yml --output .tmp/certamerge-pr.car.json
python -m certamerge verify-car .tmp/certamerge-pr.car.json
```

The output should still follow the same grammar: verdict, policy reason, missing proof, accountable next action, and CAR.

## Data Boundary

CertaMerge Community runs locally. It reads repository metadata, selected configuration files, and evidence references. It does not send source code, raw diffs, tokens, or CARs to a vendor service by default.

## Next Files To Read

- [Alpha limitations](alpha-limitations.md)
- [CAR integrity](car-integrity.md)
- [No source egress](no-source-egress.md)
- [GitHub Action](github-action.md)
- [Self-dogfooding](self-dogfooding.md)
- [Policies](policies.md)
