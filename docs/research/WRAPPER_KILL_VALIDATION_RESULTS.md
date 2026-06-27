# Wrapper-Kill Validation Results

## Purpose

This report records the first full wrapper-kill validation run for the repo-adaptive CertaMerge open-source evolution branch.

The question under test:

```text
Is CertaMerge useful outside a handcrafted CertaMerge-ready repo?
```

## Commands Run

For each archetype:

```powershell
python -m certamerge recover samples/repos/archetypes/<repo>
python -m certamerge recover samples/repos/archetypes/<repo> --suggest-policy
python -m certamerge suggest-policy samples/repos/archetypes/<repo> --output .tmp/<repo>.suggested.certamerge.yml
python -m certamerge gate --repo samples/repos/archetypes/<repo> --policy .tmp/<repo>.suggested.certamerge.yml --output .tmp/<repo>.car.json
python -m certamerge verify-car .tmp/<repo>.car.json
python -m certamerge explain-car .tmp/<repo>.car.json
```

All six generated CARs verified successfully.

## Results Matrix

| Archetype | Detected Repo Type | Recover Useful? | Suggested Policy Quality | Gate Verdict | Missing Proof | Repair Missions | CAR Valid? |
|---|---|---:|---|---|---|---|---:|
| Small Python library | `python-library` | yes | good | `OBSERVE_ONLY_WOULD_BLOCK` | tests, dependency reference, security doc | tests, dependency reference, security doc | yes |
| Node/TypeScript app | `node-typescript-app` | yes | good | `OBSERVE_ONLY_WOULD_BLOCK` | owner approval, SARIF scan | owner approval, SARIF scan | yes |
| GitHub Action repo | `github-action-repo` | yes | good | `OBSERVE_ONLY_WOULD_BLOCK` | tests, workflow validation, action contract validation, CAR verification | tests, workflow validation, action contract validation, CAR verification | yes |
| Terraform/IaC repo | `terraform-iac-repo` | yes | good | `OBSERVE_ONLY_WOULD_BLOCK` | Terraform validation, Terraform plan, owner approval | Terraform validation, Terraform plan, owner approval | yes |
| Monorepo app | `monorepo-app` | yes | good | `OBSERVE_ONLY_WOULD_BLOCK` | owner approval | owner approval | yes |
| Docs-heavy repo | `docs-heavy-repo` | yes | good | `OBSERVE_ONLY_WOULD_BLOCK` | link validation, compliance-safe language | link validation, compliance-safe language | yes |

## Minimum Pass Criteria

| Criterion | Required | Result | Pass? |
|---|---:|---:|---:|
| Zero-config Recover produces useful proof gaps | at least 4 of 6 | 6 of 6 | yes |
| Starter policy suggestion is repo-specific and reasonable | at least 4 of 6 | 6 of 6 | yes |
| Gate produces sane missing-proof output | at least 4 of 6 | 6 of 6 | yes |
| Outputs more useful than `run tests` | at least 3 outputs | 6 outputs | yes |
| Adds beyond GitHub rules/templates/scanners | concrete differentiation required | present | yes |

## What Was More Useful Than GitHub Rules Or PR Templates

- Python library: CertaMerge distinguishes test source from passing test evidence, and asks for dependency and security proof.
- Node/TypeScript app: CertaMerge recognizes auth surface risk and asks for owner approval and scanner evidence.
- GitHub Action repo: CertaMerge asks for action contract validation and CAR verification, not just CI pass/fail.
- Terraform/IaC repo: CertaMerge asks for Terraform validation, plan evidence, and owner approval.
- Monorepo app: CertaMerge recognizes ownership evidence as proof, not only review count.
- Docs-heavy repo: CertaMerge asks for link validation and compliance-safe-language proof instead of generic tests.

## What Was Weak Or Redundant

- Some ecosystems still include `docs` because README/docs files are common. This is acceptable but should be refined so ecosystem labels distinguish primary vs supporting surfaces.
- Python fixture has test source but no passing test result evidence, so Recover asks for tests. This is intentionally conservative, but the CLI should explain the difference more clearly.
- GitHub Action repo asks for `tests` because no explicit test result evidence is attached, even though tests exist. Same conservative distinction.
- The suggested policies are useful starters but not production policy packs.
- Gate still evaluates repo snapshots, not true PR diffs.
- CARs are hash-bound and change-bound, but not cryptographically signed.

## Noise Level

Noise level is acceptable for alpha validation.

Best examples:

- docs-heavy repo avoids generic `test_result` and `owner_approval` noise;
- Terraform repo avoids generic test noise and focuses on plan/validation/owner proof;
- Node auth repo focuses on owner/scanner proof after existing test/CI/dependency evidence is present.

Remaining noise:

- `docs` as a secondary ecosystem appears in code repos because README files are detected.
- `tests` means passing test result evidence, not merely test files; this needs clearer user-facing wording.

## Differentiation Verdict

CertaMerge is no longer only a wrapper around GitHub rules or repo templates in this branch.

The differentiating behavior is concrete:

```text
CertaMerge converts repo shape, workflow metadata, policy requirements, evidence states, missing proof, repair missions, and CAR verification into a deterministic proof decision for the evaluated change context.
```

This is still not production enterprise proof governance. It is, however, a real open-source wedge.

## Final Result

CERTAMERGE IS MORE THAN A TEMPLATE

