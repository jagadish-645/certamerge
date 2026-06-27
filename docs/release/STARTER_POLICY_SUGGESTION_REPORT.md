# Starter Policy Suggestion Report

## Summary

CertaMerge now exposes deterministic starter policy suggestion for repo profiles.

Commands:

```powershell
python -m certamerge suggest-policy <repo>
python -m certamerge suggest-policy <repo> --output .tmp/starter.certamerge.yml
python -m certamerge recover <repo> --suggest-policy
```

## Design Boundary

Starter policy suggestion is not AI policy authoring.

It uses deterministic repo profiling and known proof patterns. The output is observe-mode by default and must be reviewed before enforcement.

## Profile-Specific Policies

| Profile | Example Rule |
|---|---|
| `python-library` | `PY-LIB-CODE-001` requires tests, CI status, dependency evidence. |
| `node-typescript-app` | `NODE-APP-RISK-002` requires owner approval and scanner evidence for auth/payment/database paths. |
| `github-action-repo` | `ACTION-CONTRACT-001` requires workflow validation, action contract validation, tests, and CAR verification. |
| `terraform-iac-repo` | `IAC-TERRAFORM-001` requires Terraform validation, plan evidence, and owner approval. |
| `monorepo-app` | `MONOREPO-OWNERS-002` requires CODEOWNERS and owner approval for scoped app/package changes. |
| `docs-heavy-repo` | `DOCS-PUBLIC-001` requires docs build, link validation, and compliance-safe-language review. |

## Validation Example

Generated policy for the Terraform fixture:

```powershell
python -m certamerge suggest-policy samples/repos/archetypes/terraform-iac-repo --output .tmp\terraform-iac-repo.suggested.certamerge.yml
python -m certamerge gate --repo samples/repos/archetypes/terraform-iac-repo --policy .tmp\terraform-iac-repo.suggested.certamerge.yml --output .tmp\terraform-iac-repo.car.json
python -m certamerge verify-car .tmp\terraform-iac-repo.car.json
```

Observed result:

```text
Verdict: OBSERVE_ONLY_WOULD_BLOCK
Missing proof: terraform_validation, terraform_plan, owner_approval
CAR verification: valid
```

## Anti-Slop Assessment

This is not a GitHub branch rule clone because it maps repo shape to proof needs that GitHub rules do not natively model:

- Terraform plan proof;
- action contract validation;
- compliance-safe-language review for docs;
- CAR verification proof;
- ownership proof as evidence, not only review count.

## Current Limits

- Generated policies are starter policies, not production policy packs.
- Suggestions do not infer organization-specific owners.
- Suggestions do not yet include customer policy inheritance or enterprise rollout modes.
- More archetype validation is required before claiming broad usefulness.

## Verdict

Starter policy suggestion is useful enough for the wrapper-kill validation loop, but it is not yet an enterprise policy authoring system.
