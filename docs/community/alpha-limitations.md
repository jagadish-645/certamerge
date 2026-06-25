# Community Alpha Limitations

Community alpha is a useful local proof spine.

CertaMerge Community is not a production authorization platform yet.

## Release Status

Community alpha is intended for:

- local repo proof-gap checks;
- sample policy evaluation;
- proof-only PR or CI experiments;
- CAR verification and explanation;
- founder-led demos and early open-source feedback.

Community alpha is not intended for:

- unattended production merge blocking;
- regulated audit reliance without independent review;
- security certification claims;
- enterprise-wide deployment;
- signed release distribution;
- customer production support commitments.

## Current Technical Limits

| Area | Current state | Public-alpha consequence |
|---|---|---|
| CAR integrity | SHA-256 content hash over canonical CAR content is implemented and verified. | Local tampering can be detected, but CARs are not cryptographically signed. |
| Signing keys | Signing-key lifecycle is specified, not implemented. | Do not claim non-repudiation or signer identity proof. |
| GitHub Action | Composite action metadata and static contract tests exist. | Live validation in a clean GitHub repo is still required before public launch. |
| Evidence adapters | Basic local adapters and SARIF/test/approval state handling exist. | Deep scanner-specific parsing remains limited. |
| Policy engine | YAML policy parsing and deterministic evaluation exist. | Policy language is intentionally small and may change before stable release. |
| Recovery | Local Recover detects proof gaps from repo metadata and evidence files. | It is not a complete production readiness assessment. |
| No source egress | Community commands do not call vendor services or telemetry by default. | Users must still avoid placing secrets in sample policies, evidence files, or CAR artifacts. |
| Packaging | Editable install works from repo root. | Signed wheels, release checksums, and SBOM-backed release artifacts are not published yet. |
| Enterprise runtime | Enterprise alpha exists in this workspace. | It is design-partner material, not part of the public community repo by default. |

## Safe Claims

CertaMerge may say:

- It provides machine-checkable change authorization evidence.
- It can show missing proof and accountable next action.
- It can generate and verify local CARs.
- It may support review, audit, and change-control workflows.

CertaMerge must not say:

- It makes code secure.
- It does not certify compliance.
- It replaces scanners.
- It guarantees production safety.
- It cryptographically signs CARs in community alpha.

## Public Repository Boundary

The public `certamerge` repository should contain community-safe assets only:

- community CLI;
- CAR/evidence/policy/verdict/repair specs;
- sample repos, policies, evidence, and CARs;
- community docs;
- GitHub Action wrapper;
- public release docs;
- tests that validate the community product.

Enterprise alpha code, enterprise docs, paid-tier strategy, pilot packets, proprietary policy/risk packs, and internal agent-system artifacts should remain private until an explicit open-core publication decision is made.

## When This Becomes Public-Release Ready

Community alpha becomes public-release ready when:

- the repo is isolated and committed cleanly;
- Public/private split is applied;
- install and sample flows pass in a clean environment;
- tests exceed the release-candidate target with meaningful coverage;
- GitHub Action static validation passes and live validation is either completed or founder-run instructions are exact;
- CAR integrity wording is public and honest;
- SBOM, provenance, checksums, and vulnerability disclosure plans exist;
- known limitations are public.
