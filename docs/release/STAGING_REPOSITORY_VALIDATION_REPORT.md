# Staging Repository Validation Report

## Purpose

This report records the clean public/private split validation performed before public-safe repository publication.

## Staging Paths

```text
C:/Users/Jagadish/Desktop/CertaMerge/.tmp/public-staging
C:/Users/Jagadish/Desktop/CertaMerge/.tmp/enterprise-staging
```

Both paths are under `.tmp/`, which is ignored by the mixed root workspace.

## Public Staging Scope

Public staging contains:

- community CLI;
- GitHub Action wrapper;
- community tests;
- community docs;
- public release docs;
- sample repos, evidence, policies, PR fixtures, and CARs;
- CAR, evidence, policy, verdict, repair, and open-core specs;
- public-only `pyproject.toml`;
- no enterprise source tree;
- no internal agent-system tree;
- no local skill library;
- no UX/architecture/research strategy folders.

## Enterprise Staging Scope

Enterprise staging contains:

- enterprise alpha runtime;
- enterprise tests;
- enterprise docs;
- service docs;
- enterprise sample fixtures;
- private `pyproject.toml` that depends on `certamerge==0.1.0`;
- no duplicated community source tree;
- no internal agent-system tree;
- no local skill library.

## Public Staging Validation

Validated:

```powershell
python -m pip install -e .tmp/public-staging
python -m certamerge --help
certamerge --help
python -m certamerge recover samples/repos/no-ci-vibe-repo
python -m certamerge gate --repo samples/repos/payment-change-with-tests --policy samples/policies/payment.certamerge.yml --output .tmp/payment.car.json
python -m certamerge verify-car .tmp/payment.car.json
python -m certamerge explain-car .tmp/payment.car.json
python -m pytest -q
python -m compileall community
```

Observed:

```text
public staging CLI passed
public staging tests passed
public staging compile passed
public staging marker scan passed
public staging forbidden-directory scan passed
```

## Enterprise Staging Validation

Validated after installing public staging first:

```powershell
python -m pip install -e .tmp/public-staging
python -m pip install -e .tmp/enterprise-staging
python -m certamerge_enterprise --help
certamerge-enterprise --help
python -m pytest -q
python -m compileall enterprise
```

Observed:

```text
enterprise staging CLI passed
enterprise staging tests passed
enterprise staging compile passed
enterprise staging marker scan passed
enterprise staging forbidden-directory scan passed
```

## Git State

Both staging repositories were initialized on `main`, committed locally, configured with remotes, and pushed:

```text
public staging remote:     https://github.com/jagadish-645/certamerge
enterprise staging remote: https://github.com/jagadish-645/certamerge_enterprise
```

Public staging current commit:

```text
1102c51
```

Enterprise staging current commit:

```text
8a97717
```

GitHub validation:

```text
CertaMerge CI: https://github.com/jagadish-645/certamerge/actions/runs/28169666399
CertaMerge Action Live Validation: https://github.com/jagadish-645/certamerge/actions/runs/28169666397
```

## Remaining Public Release Gaps

Even with staging validated, production release remains gated by:

- release SBOM generation;
- release checksum manifest;
- release signing decision and verification instructions;
- CAR cryptographic signing for production-grade authorization.

## Verdict

Public/private staging split is validated locally and pushed.

Public release candidate is ready for alpha use with documented release-artifact and signing limitations.
