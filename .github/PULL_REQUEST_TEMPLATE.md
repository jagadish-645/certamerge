# Pull Request

## What Changed

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

## Data Safety

- [ ] No secrets, tokens, raw proprietary source code, raw restricted diffs, or customer production data are included.
