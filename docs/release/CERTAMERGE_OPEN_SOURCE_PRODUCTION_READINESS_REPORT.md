# CertaMerge Open Source Production Readiness Report

Date: 2026-06-27

Repository: `jagadish-645/certamerge`

Primary PR: #4 `evolution: make CertaMerge repo-adaptive beyond self-dogfood`

## Executive Summary

CertaMerge Community Alpha is release-ready as an open-source alpha after the PR #4 hardening pass. PR #4 was merged into `main`, the superseded draft PRs were closed, GitHub checks passed, and the merged `main` branch produced a valid self-gate CAR.

This is not an enterprise production-readiness claim. The release-ready scope is the community alpha surface:

- local CLI;
- Recover;
- suggest-policy;
- proof-only Gate;
- PR-diff-aware Gate v1;
- evidence adapters v1;
- hash-bound CAR generation;
- local CAR verification and explanation;
- composite GitHub Action wrapper;
- community docs, examples, policies, fixtures, and release reports.

## What Was Added In This Pass

- PR consolidation plan.
- Senior maintainer review for PR #4.
- PR-diff-aware Gate v1.
- CAR change-scope fields.
- Explicit changed-files CLI support.
- Git diff base/head CLI support.
- GitHub Actions PR context support with honest fallback.
- Evidence adapters v1 for JUnit, SARIF, CycloneDX/SBOM, Terraform plan, and Gitleaks/secret-scan artifacts.
- CAR signing v0 decision report.
- Checksum-generation script.
- CI matrix for Python 3.11 and 3.12.
- CI `pip check`, package build, changed-files smoke, and action metadata validation.
- Public docs and leakage/safe-language scan report.

## Local Gate Evidence

Commands run successfully:

```powershell
python -m pip install -e .
python -m certamerge --help
python -m certamerge recover .
python -m certamerge recover . --suggest-policy
python -m certamerge suggest-policy . --output .tmp/self.suggested.certamerge.yml
python -m certamerge gate --repo . --policy .certamerge.yml --output .tmp/open-source-final.car.json
python -m certamerge verify-car .tmp/open-source-final.car.json
python -m certamerge explain-car .tmp/open-source-final.car.json
python -m pytest -q
python -m pytest --collect-only -q
python -m compileall community scripts
python -m build
python -m twine check dist\*
python scripts\generate_checksums.py
```

Results:

| Gate | Result |
|---|---|
| Editable install | Passed |
| CLI help | Passed |
| Recover on repo | Passed; repo profile `python-library`, missing proof `sarif_scan` |
| Suggested policy generation | Passed |
| Self Gate | Passed; verdict `OBSERVE_ONLY_WOULD_ALLOW` |
| CAR verification | Passed; `valid: true` |
| CAR explanation | Passed |
| Tests | Passed; `266 passed` |
| Test collection | Passed; `266 tests collected` |
| Compileall | Passed |
| Build | Passed |
| Twine check | Passed |
| Checksum generation | Passed |
| `pip check` | Passed in GitHub CI; local global Python environment has an unrelated `opencv-python` / `numpy` conflict outside CertaMerge dependencies |

Generated final self-gate CAR:

```text
.tmp/open-source-final.car.json
```

Verified verdict:

```text
OBSERVE_ONLY_WOULD_ALLOW
```

## Post-Merge Main-Branch Evidence

Merged `main` commit:

```text
ccd5c9b evolution: make CertaMerge repo-adaptive beyond self-dogfood
```

Post-merge smoke commands passed on `main`:

```powershell
python -m pip install -e .
python -m certamerge --help
python -m certamerge recover .
python -m certamerge recover . --suggest-policy
python -m certamerge suggest-policy . --output .tmp/self.postmerge.suggested.certamerge.yml
python -m certamerge gate --repo . --policy .certamerge.yml --output .tmp/open-source-main.car.json
python -m certamerge verify-car .tmp/open-source-main.car.json
python -m certamerge explain-car .tmp/open-source-main.car.json
python -m pytest -q
python -m pytest --collect-only -q
python -m compileall community scripts
python -m build
python -m twine check dist\*
```

Post-merge self-gate verdict:

```text
OBSERVE_ONLY_WOULD_ALLOW
```

Post-merge CAR verification:

```text
valid: true
```

## Remote GitHub Gate Evidence

PR #4 remote checks passed before merge:

| GitHub check | Result |
|---|---|
| `CertaMerge CI / test (3.11)` | success |
| `CertaMerge CI / test (3.12)` | success |
| `CertaMerge Proof Gate / certamerge-proof` | success |

PR #4 was then merged into `main`.

## PR-Diff-Aware Proof

Implemented:

- `--changed-files`;
- `--base`;
- `--head`;
- `change_context_mode`;
- `changed_files`;
- `changed_file_count`;
- PR number, base SHA, head SHA, run id fields;
- honest `repo_snapshot` fallback.

Covered by tests:

- explicit changed files;
- git diff unavailable fallback;
- GitHub event fallback;
- docs-only change;
- workflow change;
- auth/source change;
- dependency file change;
- Terraform file change.

## Evidence Adapter V1

Implemented and tested:

- JUnit XML pass/fail/malformed;
- SARIF negative/failed/malformed;
- CycloneDX/SBOM present/malformed;
- Terraform plan present/malformed;
- Gitleaks/secret-scan negative/failed/malformed;
- existing owner approval and test result state semantics.

CertaMerge still does not run scanners itself. It only normalizes existing artifacts.

## CAR Integrity And Signing

Current alpha supports:

- SHA-256 CAR content hash;
- policy file hash;
- evidence artifact hashes;
- offline local verification.

Not implemented:

- cryptographic CAR signing;
- signer identity;
- key rotation;
- revocation;
- non-repudiation.

Decision:

```text
Signing is intentionally deferred until key management and verification UX can be done honestly.
```

## Public Docs And Boundary

Docs now cover:

- quickstart;
- Recover;
- suggest-policy;
- GitHub Action;
- PR-diff-aware proof;
- evidence adapters;
- CAR integrity;
- CAR signing status;
- alpha limitations;
- no source egress;
- feedback and self-dogfooding.

Public boundary remains community alpha only. Enterprise-only runtime, multi-repo governance, advanced ProofGraph, SoD, audit export, and deployment hardening remain outside this public package.

## Cleanliness And Safe Language

Scans found:

- no active local Windows path leakage;
- no real token/private-key/cloud-key leak;
- no active production-enterprise readiness claim;
- no active compliance certification claim;
- no active claim that CertaMerge makes code secure or guarantees safety.

Remaining scan hits are:

- an intentional test assertion that the private enterprise package name is absent from public text;
- false-positive token heuristic hits on `risk-surface` terminology;
- forbidden-claim language in negative contexts.

## Release Limitations

Still not included:

- signed release artifacts;
- SBOM generation automation;
- provenance or in-toto attestations;
- production deployment manifests;
- enterprise RBAC/SSO;
- enterprise retention/query service;
- hosted service;
- compliance certification.

These are not blockers for community alpha release readiness, but they are blockers for any enterprise production-readiness claim.

## PR Resolution Outcome

Resolved PR state:

| PR | Outcome |
|---|---|
| #4 `evolution: make CertaMerge repo-adaptive beyond self-dogfood` | Merged |
| #3 `dogfood: use CertaMerge to govern its own public alpha repo` | Closed as superseded by PR #4 |
| #2 `docs: professionalize public README` | Closed as superseded by PR #4 |

## Final Open-Source Verdict

```text
CERTAMERGE OPEN SOURCE RELEASE READY
```
