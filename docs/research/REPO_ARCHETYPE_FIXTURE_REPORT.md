# Repo Archetype Fixture Report

## Purpose

This report documents the six local fixture repositories created for the wrapper-kill validation.

They are not production repositories. They are minimal but realistic enough to test whether CertaMerge can infer repo shape, proof gaps, and starter policies without a handcrafted `.certamerge.yml`.

## Fixture Inventory

| Archetype | Path | Key Signals |
|---|---|---|
| Small Python library | `samples/repos/archetypes/python-library/` | `pyproject.toml`, `src/`, `tests/`, CI workflow, `LICENSE`, missing `SECURITY.md`, missing lockfile/SBOM/scanner evidence. |
| Node/TypeScript app | `samples/repos/archetypes/node-typescript-app/` | `package.json`, `package-lock.json`, `tsconfig.json`, `src/auth/`, `__tests__/`, CI workflow, `SECURITY.md`, `LICENSE`. |
| GitHub Action repository | `samples/repos/archetypes/github-action-repo/` | `action.yml`, `scripts/`, `tests/`, CI workflow, local action invocation, `LICENSE`. |
| Terraform/IaC repository | `samples/repos/archetypes/terraform-iac-repo/` | `main.tf`, `variables.tf`, `versions.tf`, Terraform CI workflow, missing plan/validation evidence files. |
| Monorepo-style app | `samples/repos/archetypes/monorepo-app/` | `apps/`, `packages/`, workspace `package.json`, `pnpm-lock.yaml`, `CODEOWNERS`, CI workflow, auth and database surfaces. |
| Docs-heavy open-source repo | `samples/repos/archetypes/docs-heavy-repo/` | `mkdocs.yml`, `docs/`, README, docs CI workflow, safe-language documentation surface. |

## Realism Rules Applied

- Fixtures include actual manifests and source/test/docs files, not empty directories.
- Fixtures expose realistic proof gaps instead of being perfect.
- Fixtures use synthetic names and do not include secrets, private paths, customer data, or proprietary source.
- Fixtures exercise different proof needs: package proof, action contract proof, IaC plan proof, owner proof, docs build/link proof, and compliance-safe language proof.

## Initial Recover Observations

Observed zero-config Recover profile detection:

| Fixture | Detected Type | Notable Missing Proof |
|---|---|---|
| `python-library` | `python-library` | `test_result`, `dependency_reference`, `security_doc`, `sarif_scan` |
| `node-typescript-app` | `node-typescript-app` | `owner_approval`, `sarif_scan` |
| `github-action-repo` | `github-action-repo` | `test_result`, `workflow_validation`, `action_contract_validation`, `car_verification` |
| `terraform-iac-repo` | `terraform-iac-repo` | `terraform_validation`, `terraform_plan`, `owner_approval`, `security_doc` |
| `monorepo-app` | `monorepo-app` | `owner_approval`, `security_doc`, `license_file`, `sarif_scan` |
| `docs-heavy-repo` | `docs-heavy-repo` | `links_valid`, `compliance_safe_language` |

## Current Limitations

- Fixtures are synthetic and local; they do not replace testing on real public repository structures.
- CertaMerge currently infers from filenames, manifests, and metadata only. It does not parse source code and must not become an AI code reviewer.
- Test-result proof remains conservative: presence of tests is different from proof that tests passed.
- Scanner evidence is detected through SARIF-like artifacts, not by running scanners.

## Verdict

The fixture set is adequate for the first wrapper-kill loop because it exercises six distinct repository shapes and multiple non-generic proof requirements.
