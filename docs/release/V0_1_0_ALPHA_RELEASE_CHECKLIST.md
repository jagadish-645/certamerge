# CertaMerge v0.1.0 Alpha Release Checklist

Date: 2026-06-27

## Release Scope

Community alpha release scope:

- local CLI;
- Recover;
- suggest-policy;
- proof-only Gate;
- PR-diff-aware Gate v1;
- evidence adapters v1;
- hash-bound CAR generation;
- local CAR verification and explanation;
- composite GitHub Action wrapper;
- sample repos, policies, CARs, and public docs.

Out of scope:

- enterprise production deployment;
- hosted SaaS;
- SSO/RBAC;
- cryptographic CAR signing;
- release signing;
- SBOM/provenance automation;
- compliance certification claims.

## Required Before Merging PR #4

- [x] Editable install passes.
- [x] CLI help passes.
- [x] Recover runs on repo.
- [x] Suggested policy generation works.
- [x] Gate runs on repo.
- [x] CAR verifies.
- [x] Tests pass locally.
- [x] Package build passes locally.
- [x] GitHub checks pass on current PR #4 revision before this hardening pass.
- [x] PR-diff-aware Gate v1 implemented.
- [x] Evidence adapters v1 implemented.
- [x] CAR signing decision documented honestly.
- [x] Checksum script added.
- [x] `twine check` passes locally.
- [ ] Full final local gate rerun after all edits.
- [ ] GitHub checks pass after pushing this hardening pass.
- [ ] PR #4 marked ready for review.
- [ ] PR #4 merged.
- [ ] Superseded PR #2/#3 closed with explanation.

## Release Verification Commands

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
python -m compileall community
python -m build
python -m twine check dist\*
python scripts\generate_checksums.py
```

## Go/No-Go Rule

Do not call the community alpha release-ready unless:

- local gate passes after final edits;
- GitHub `test` passes;
- GitHub `certamerge-proof` passes;
- public docs scan finds no private leakage or unsafe claims;
- generated CAR verifies;
- PR state is resolved.

## Current Checklist Verdict

```text
V0.1.0 ALPHA RELEASE CHECKLIST CREATED — FINAL GATE STILL REQUIRED
```

