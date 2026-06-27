# Suggest Policy

`suggest-policy` prints a deterministic starter `.certamerge.yml` for a repository.

The generated policy is a starting point for review. It is not an enterprise policy pack and must not be treated as a production authorization policy without review.

## Command

```powershell
python -m certamerge suggest-policy <repo>
```

Write the policy to a file:

```powershell
python -m certamerge suggest-policy <repo> --output .tmp/starter.certamerge.yml
```

Recover can also print the same starter policy:

```powershell
python -m certamerge recover <repo> --suggest-policy
```

## Current Repo-Specific Behavior

| Repo Profile | Starter Policy Focus |
|---|---|
| `python-library` | tests, CI, dependency evidence, security doc, license proof |
| `node-typescript-app` | tests, CI, dependency evidence, sensitive-path owner approval, scanner evidence |
| `github-action-repo` | workflow validation, action contract validation, tests, CAR verification |
| `terraform-iac-repo` | Terraform validation, plan evidence, owner approval |
| `monorepo-app` | app/package-scoped tests and CI, dependency evidence, ownership proof |
| `docs-heavy-repo` | docs build, link validation, compliance-safe-language review |

## Example

```powershell
python -m certamerge suggest-policy samples/repos/archetypes/terraform-iac-repo --output .tmp/terraform.certamerge.yml
python -m certamerge gate --repo samples/repos/archetypes/terraform-iac-repo --policy .tmp/terraform.certamerge.yml --output .tmp/terraform.car.json
python -m certamerge verify-car .tmp/terraform.car.json
```

Expected Gate shape:

```text
Verdict: OBSERVE_ONLY_WOULD_BLOCK
Missing proof: terraform_validation, terraform_plan, owner_approval
```

## Safety Rules

- The generated policy must be reviewed before enforcement.
- The policy is observe-mode by default.
- Missing proof should produce `NEEDS_EVIDENCE`, `ESCALATE`, or observe-mode would-block, not silent allow.
- No LLM decides the policy or verdict.
