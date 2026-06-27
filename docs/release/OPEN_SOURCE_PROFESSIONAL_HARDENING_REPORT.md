# Open-Source Professional Hardening Report

## Summary

This pass checked the community repository as a public alpha product surface after the repo-adaptive evolution work.

The goal was not to bloat documentation. The goal was to remove public-repo residue, keep claims safe, and verify the repository has the basic maintainer surfaces expected by a serious open-source reviewer.

## Required Surfaces Checked

All required surfaces are present:

- `README.md`
- `SECURITY.md`
- `CONTRIBUTING.md`
- `LICENSE`
- `pyproject.toml`
- `.github/ISSUE_TEMPLATE/*`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `docs/community/*`
- `docs/demo/*`
- `docs/release/*`
- `samples/*`
- `community/tests/*`

## Cleanup Performed

Sample CAR fixtures contained absolute local Windows paths in `change.source_ref`.

Updated:

- `samples/cars/allow.example.json`
- `samples/cars/block.example.json`
- `samples/cars/needs-evidence.example.json`
- `samples/cars/override-recorded.example.json`
- `samples/cars/repair-required.example.json`

The sample CAR paths now use repository-relative public fixture paths, and each CAR content hash was recalculated.

Also updated one release report wording from a tool-specific residue phrase to `tooling-residue`.

## Scans Run

Local path / private tooling residue scan:

```powershell
Run a repository-wide search for local Windows user paths, private workspace names, private tool folders, and tool-specific residue across public docs, product code, samples, and GitHub metadata.
```

Result:

```text
no matches
```

Token-looking / secret-looking scan:

```powershell
Ran a repository-wide search for common token, private-key, and credential assignment shapes across public docs, source, samples, workflows, and package metadata.
```

Result:

```text
no real secrets found
```

Remaining matches are test strings that intentionally verify raw source/secret-like words are not emitted into Recover or Gate output.

Unsafe claim scan:

```powershell
rg -n "guarantees production safety|certifies compliance|makes code secure|cryptographically signs CARs" README.md SECURITY.md docs .github -S
```

Result:

```text
matches exist only in non-claim / forbidden-claim contexts
```

Examples:

- `SECURITY.md` lists claims the project must not make.
- `docs/community/alpha-limitations.md` lists alpha non-claims.
- release reports document safe-claim boundaries.

## Verification

Sample CAR and public template verification:

```powershell
python -m pytest community/tests/test_controlled_alpha_contracts.py::test_sample_cars_verify community/tests/test_public_release_candidate_contracts.py::test_public_templates_do_not_contain_local_paths_or_token_shapes -q
```

Result:

```text
10 passed
```

Full suite after the current evolution work:

```text
238 passed
```

## Remaining Open-Source Hardening Work

- Run link checking before public release.
- Run live GitHub Actions validation after this branch is pushed.
- Add signed release/SBOM automation before any production claim.
- Keep public docs clear that community alpha CARs are hash-bound but not cryptographically signed.
- Continue rejecting dashboard/chatbot/scanner-wrapper framing.

## Verdict

The public repository surface is clean enough for the current evolution PR, with no known local path leakage or secret leakage in public product files.
