# Self-Dogfooding

CertaMerge uses CertaMerge on its own public alpha repository.

The self-dogfood policy lives at:

```text
.certamerge.yml
```

It keeps the public repository aligned to the product grammar:

```text
Verdict.
Policy reason.
Missing proof.
Accountable next action.
Change Authorization Record.
```

## Local Self-Check

Run from the repository root:

```powershell
python -m certamerge gate --repo . --policy .certamerge.yml --output .tmp/certamerge-pr.car.json
python -m certamerge verify-car .tmp/certamerge-pr.car.json
```

The policy is observe-mode by default. It can show `OBSERVE_ONLY_WOULD_BLOCK` without breaking a contributor workflow.

## What The Policy Protects

- CLI and verifier behavior.
- CAR schema and verifier integrity.
- GitHub Action and workflow changes.
- Specs, samples, public docs, packaging, and license files.

## What It Requires

Depending on the changed path, the policy may require tests, CI status, owner approval evidence, GitHub Actions artifact evidence, security-doc presence, or dependency review evidence.

The current self-policy also recognizes metadata proof for CAR verification, no-source-egress posture, risk surface classification, workflow validation, action contract validation, schema validation, compliance-safe language, no-secret-leakage review, and link validation.

## Current Alpha Limitations

Community alpha CARs have schema and SHA-256 content-hash verification. They are not cryptographically signed yet and must not be represented as non-repudiable approvals.
