# CertaMerge Public Release Candidate Report

## 1. Executive Verdict

CertaMerge has advanced from controlled alpha toward public-release-candidate quality.

The community product is now more credible: public docs are stronger, package metadata is improved, the GitHub Action install path is corrected, release trust plans exist, CAR integrity language is honest, and the test suite expanded from 100 to 175 passing tests.

However, public release candidate is not fully ready because the current workspace is not yet split between the public `certamerge` repo and private `certamerge_enterprise` repo, no initial commit exists, live GitHub Action validation has not run, and release artifact integrity is planned but not implemented.

## 2. Repository Isolation Status

Pass with blockers.

Git now resolves CertaMerge to:

```text
C:/Users/Jagadish/Desktop/CertaMerge
```

The repo is independent from the parent Git root.

Remaining blockers:

- no initial commit;
- all files currently untracked;
- no remote configured;
- parent repo may still see `Desktop/CertaMerge/` as an untracked nested repo;
- public/private split not executed.

GitHub targets were verified:

```text
https://github.com/jagadish-645/certamerge              public
https://github.com/jagadish-645/certamerge_enterprise   private
```

No remote was configured because this mixed workspace is not public-safe yet.

Report:

```text
docs/release/REPOSITORY_ISOLATION_REPORT.md
```

## 3. Install And Package Status

Pass for local editable install.

Verified commands include:

```powershell
python -m pip install -e .
python -m certamerge --help
certamerge --help
python -m certamerge recover samples/repos/no-ci-vibe-repo
python -m certamerge gate --repo samples/repos/payment-change-with-tests --policy samples/policies/payment.certamerge.yml --output .tmp/payment.car.json
python -m certamerge verify-car .tmp/payment.car.json
python -m certamerge explain-car .tmp/payment.car.json
```

Package metadata was hardened with readme, license, author, keywords, and alpha classifiers.

Public package blocker:

```text
pyproject.toml currently includes the enterprise alpha package and certamerge-enterprise entry point.
```

The public repository must split or remove enterprise packaging before publication.

## 4. README And Docs Status

Pass.

Updated:

- `README.md`
- `docs/community/quickstart.md`
- `docs/community/alpha-limitations.md`
- `docs/community/car-integrity.md`
- `SECURITY.md`

README now answers:

1. What CertaMerge is.
2. Why it exists.
3. What problem it solves.
4. What a CAR is.
5. Difference from AI code review.
6. Difference from scanners.
7. Install command.
8. Recover command.
9. Gate command.
10. Verify command.
11. Output shape.
12. Community/open-source scope.
13. Enterprise scope.
14. Non-claims.
15. Alpha limitations.

## 5. GitHub Action Status

Pass for static validation.

Corrected:

```text
community/github-action/action.yml
```

The action now installs CertaMerge from:

```bash
$GITHUB_ACTION_PATH/../..
```

This matters because a composite action consumed from another repository must not install the caller repository by accident.

Added:

```text
docs/release/GITHUB_ACTION_LIVE_VALIDATION_CHECKLIST.md
```

Remaining blocker:

```text
No live GitHub Actions run has been performed in a clean test repository.
```

## 6. CAR Integrity And Signing Status

Pass for honest community alpha.

Decision:

```text
Use SHA-256 content-hash integrity now and formally defer cryptographic signing.
```

Implemented:

- canonical CAR hash;
- verifier content-hash check;
- CAR tamper detection test;
- public doc separating hash integrity from signatures.

Not implemented:

- CAR cryptographic signing;
- signing key lifecycle;
- revocation;
- signer identity;
- non-repudiation.

Report:

```text
docs/release/CAR_INTEGRITY_RELEASE_DECISION.md
```

## 7. SBOM, Provenance, And Release Artifact Status

Plan exists, implementation pending.

Created:

- `docs/release/SBOM_AND_PROVENANCE_PLAN.md`
- `docs/release/RELEASE_ARTIFACT_INTEGRITY_PLAN.md`

Remaining blockers:

- no generated SBOM artifact;
- no checksum manifest;
- no signed release;
- no release provenance artifact;
- no clean install from built wheel/source distribution.

## 8. Test Count And Results

Current verified result:

```text
175 passed
```

Commands:

```powershell
python -m pytest --collect-only -q
python -m pytest -q
```

The target of 120+ meaningful tests was exceeded.

## 9. Commands Verified

Verified in this release-candidate pass:

```powershell
python -m pytest -q
python -m pytest --collect-only -q
python -m certamerge --help
python -m certamerge_enterprise --help
python -m compileall community enterprise
```

Clean editable install and community sample flows were also verified in the clean virtual environment created for this release work.

## 10. Enterprise Design-Partner Readiness

Enterprise alpha remains preserved, not expanded.

Verified:

- enterprise CLI help works;
- enterprise tests pass as part of the 175-test suite;
- enterprise docs exist;
- service-package docs exist.

Enterprise is design-partner credible for founder-led pilots and observe-mode/service-led demos.

Enterprise is not production-sales ready.

Report:

```text
docs/release/ENTERPRISE_DESIGN_PARTNER_READINESS_REPORT.md
```

## 11. Public Alpha Go/No-Go

Current gate:

```text
NO-GO
```

Report:

```text
docs/release/PUBLIC_ALPHA_GO_NO_GO.md
```

## 12. Known Limitations

- Public/private repo split not executed.
- No initial commit.
- No remote configured.
- GitHub Action live validation not run.
- Release artifact integrity not implemented.
- CAR cryptographic signing not implemented.
- Public package metadata still needs enterprise split.
- Enterprise alpha is not production deployment ready.

## 13. Exact Next Founder Actions

1. Approve public/private repo split execution.
2. Approve initial commit creation.
3. Confirm GitHub owner and remote URLs for `certamerge` and `certamerge_enterprise`.
4. Decide whether the live GitHub Action checklist must pass before public push.
5. Decide minimum artifact integrity requirement for public alpha.

## 14. Exact Next Codex Goal

Create clean public and private staging trees from the current workspace, remove enterprise/private material from the public tree, run public-only install/tests, then commit and configure remotes only after explicit permission.

## Final Verdict

CERTAMERGE PUBLIC RELEASE CANDIDATE NOT READY — missing: public/private repo split execution, initial commit, remote configuration, live GitHub Action validation, public-only package split, release SBOM/checksum/signing implementation
