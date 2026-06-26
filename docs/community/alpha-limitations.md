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
| GitHub Action | Composite action metadata, static contract tests, and sample live-validation paths exist. | It is suitable for proof-only experiments, not production branch-protection enforcement. |
| Self-dogfooding | The public repo has an observe-mode `.certamerge.yml` and PR workflow. | It proves CertaMerge can govern its own alpha changes, but it is not yet a production branch-protection guarantee. |
| Evidence adapters | Basic local adapters and SARIF/test/approval state handling exist. | Deep scanner-specific parsing remains limited. |
| Policy engine | YAML policy parsing and deterministic evaluation exist. | Policy language is intentionally small and may change before stable release. |
| Recovery | Local Recover detects proof gaps from repo metadata and evidence files. | It is not a complete production readiness assessment. |
| No source egress | Community commands do not call vendor services or telemetry by default. | Users must still avoid placing secrets in sample policies, evidence files, or CAR artifacts. |
| Packaging | Editable install works from repo root. | Signed wheels, release checksums, and SBOM-backed release artifacts are not published yet. |
| Organization-wide runtime | Advanced enterprise deployment and governance surfaces are outside this community repository. | Do not treat community alpha as an enterprise control plane. |

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

Advanced enterprise deployment, organization-wide policy administration, proprietary policy/risk packs, pilot packets, and internal agent-system artifacts are outside this repository until an explicit open-core publication decision is made.

## When This Becomes Public-Release Ready

Community alpha becomes public-release ready when:

- the repo is isolated and committed cleanly;
- the public repository contains only community-safe assets;
- install and sample flows pass in a clean environment;
- tests exceed the release-candidate target with meaningful coverage;
- GitHub Action static validation passes and live validation is either completed or founder-run instructions are exact;
- CAR integrity wording is public and honest;
- SBOM, provenance, checksums, and vulnerability disclosure plans exist;
- known limitations are public.
