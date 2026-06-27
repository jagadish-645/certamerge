# Pull Request

## What Changed

-

## Why It Matters

-

## Product Boundary

- [ ] Strengthens evidence collection, risk classification, deterministic policy decision, or CAR/proof verification.
- [ ] Does not add chatbot, dashboard-first, scanner-replacement, or compliance-certification behavior.
- [ ] Does not make an LLM authoritative for final verdicts.
- [ ] Does not introduce source-code egress by default.

## Verification

- [ ] `python -m pip install -e .`
- [ ] `python -m certamerge recover samples/repos/no-ci-vibe-repo`
- [ ] `python -m certamerge gate --repo samples/repos/payment-change-with-tests --policy samples/policies/payment.certamerge.yml --output .tmp/payment.car.json`
- [ ] `python -m certamerge verify-car .tmp/payment.car.json`
- [ ] `python -m pytest`

## CertaMerge Proof

Verdict:

Policy reason:

Missing proof:

Accountable next action:

CAR:

Verification:

Limitations:

Recommended local self-check:

```powershell
python -m certamerge gate --repo . --policy .certamerge.yml --output .tmp/certamerge-pr.car.json
python -m certamerge verify-car .tmp/certamerge-pr.car.json
```

## Data Safety

- [ ] No secrets, tokens, raw proprietary source code, raw restricted diffs, or customer production data are included.
