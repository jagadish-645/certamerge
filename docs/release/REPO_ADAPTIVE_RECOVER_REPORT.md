# Repo-Adaptive Recover Report

## Summary

Recover has been upgraded from basic repo proof detection to deterministic repo profiling with adaptive proof gaps.

It now returns a `profile` object and a `suggested_policy` object in the Recover snapshot.

## Implementation Changes

- Expanded repo type detection in `risk.py` for:
  - `python-library`
  - `node-typescript-app`
  - `github-action-repo`
  - `terraform-iac-repo`
  - `monorepo-app`
  - `docs-heavy-repo`
- Expanded metadata signal detection in `evidence.py` for:
  - license files
  - CODEOWNERS
  - PR and issue templates
  - GitHub Action metadata
  - Terraform files
  - Terraform validation/plan evidence
  - docs site and docs build evidence
- Added adaptive proof gaps in `recover.py`.
- Reduced generic proof noise for docs-heavy and Terraform/IaC repositories.
- Added CLI output for repo profile and ecosystems.

## Example Results

| Fixture | Detected Type | Useful Missing Proof |
|---|---|---|
| `python-library` | `python-library` | dependency proof, security doc, scanner evidence |
| `node-typescript-app` | `node-typescript-app` | owner approval and scanner evidence for auth surface |
| `github-action-repo` | `github-action-repo` | workflow validation, action contract validation, CAR verification |
| `terraform-iac-repo` | `terraform-iac-repo` | Terraform validation, plan evidence, owner approval |
| `monorepo-app` | `monorepo-app` | owner approval, security doc, license, scanner evidence |
| `docs-heavy-repo` | `docs-heavy-repo` | link validation and compliance-safe-language review |

## Tests Added

The focused contract suite now validates:

- repo type detection for all six archetypes;
- risk surface detection for IaC, docs, and GitHub Action surfaces;
- Recover profile output;
- Recover missing-proof output;
- suggested policy rule IDs;
- docs-heavy Recover avoids generic test/owner noise.

Focused result:

```text
115 passed
```

## Current Limits

- Recover is still metadata/path based. It does not run tests or scanners.
- Test source presence and passing test result evidence are still distinct.
- SARIF scanner evidence is recognized but not produced.
- Suggested policies are starter policies and must be reviewed before enforcement.

## Verdict

Recover is meaningfully more repo-adaptive than the previous self-dogfood-only version. It still needs full wrapper-kill validation across all archetypes before claiming the product is more than a template.
