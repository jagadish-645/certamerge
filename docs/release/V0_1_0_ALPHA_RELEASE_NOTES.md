# CertaMerge v0.1.0 Alpha Release Notes

## Release Type

Community alpha for local ProofOps workflows.

## Included

- Local `certamerge` CLI.
- `recover` for repo proof-gap discovery.
- `gate` for proof-only policy evaluation.
- `verify-car` and `explain-car` for offline CAR review.
- CAR, evidence, policy, verdict, repair-mission, and open-core specs.
- Sample repos, policies, evidence files, PR fixtures, and CAR examples.
- Composite GitHub Action wrapper for proof-only experiments.
- Community docs, public demo docs, and alpha limitation docs.
- Automated tests and CI for the public community surface.

## Not Included

- Production merge blocking guarantees.
- Cryptographic CAR signing.
- Signed release archives.
- SBOM-backed release distribution.
- Hosted SaaS.
- Enterprise runtime, ProofGraph, SoD, audit export, or organization-wide policy administration.
- Compliance certification.
- Scanner replacement.

## Safe Claim

CertaMerge v0.1.0 alpha provides machine-checkable evidence for software change authorization experiments. It may support review, audit, and change-control workflows, but it does not certify compliance or guarantee production safety.

## Upgrade Notes

This is the first public alpha baseline. Policy, evidence, and CAR formats are versioned but may evolve before a stable release.
