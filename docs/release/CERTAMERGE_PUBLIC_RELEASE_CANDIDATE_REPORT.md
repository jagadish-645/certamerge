# CertaMerge Public Release Candidate Report

## Executive Verdict

CertaMerge community alpha is a credible public release candidate for local proof-gap discovery, proof-only policy evaluation, CAR generation, offline CAR verification, and GitHub Action experimentation.

It remains an alpha. It must not be described as a production authorization platform, compliance certification tool, scanner replacement, or security guarantee.

## Public Product Boundary

The public repository contains:

- community CLI;
- local Recover;
- proof-only Gate;
- CAR verifier and explainer;
- CAR, evidence, policy, verdict, and repair-mission specifications;
- basic policy examples;
- sample repositories, PR fixtures, evidence fixtures, and CAR examples;
- composite GitHub Action wrapper;
- community docs, demo docs, release notes, and tests.

The public repository intentionally excludes:

- enterprise runtime services;
- organization-wide ProofGraph memory;
- separation-of-duties enforcement;
- enterprise audit export;
- hosted control planes;
- production deployment manifests;
- proprietary policy/risk packs;
- internal strategy and agent-system material.

## Verified Community Flows

The release candidate verifies these user-facing loops:

1. `python -m certamerge --help`
2. `python -m certamerge recover samples/repos/no-ci-vibe-repo`
3. `python -m certamerge gate --repo samples/repos/payment-change-with-tests --policy samples/policies/payment.certamerge.yml --output .tmp/payment.car.json`
4. `python -m certamerge verify-car .tmp/payment.car.json`
5. `python -m certamerge explain-car .tmp/payment.car.json`
6. `python -m pytest`
7. `python -m compileall community`

## Trust Position

CertaMerge community alpha uses deterministic policy evaluation for final verdicts. It does not use an LLM for authorization.

CARs are integrity-bound with verifier-checked SHA-256 content hashes. They are not cryptographically signed in community alpha.

The community package defaults to no telemetry, no vendor callbacks, and no source-code egress. Users are still responsible for keeping sensitive data out of manually supplied evidence and issue reports.

## Release Candidate Limitations

- Production branch-protection enforcement is not recommended yet.
- Cryptographic CAR signing is not implemented yet.
- Signed release archives and SBOM-backed distribution are not automated yet.
- Advanced enterprise deployment, ProofGraph, audit export, and organization-wide policy administration are outside this package.
- Compliance language must remain evidence-support language, never certification language.

## Final Public Candidate Verdict

```text
CERTAMERGE PUBLIC RELEASE CANDIDATE READY WITH ALPHA LIMITATIONS
```
