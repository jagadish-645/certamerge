# Current Production Readiness Standards Review

Date: 2026-06-27

Scope: CertaMerge open-source community alpha.

## Purpose

This review translates current public software supply-chain and open-source release guidance into practical CertaMerge alpha decisions. It is not a standards-mapping marketing document. It decides what belongs now, what belongs next, and what must not be claimed.

## Source Anchors

Primary sources reviewed:

- GitHub rulesets and branch protection: <https://docs.github.com/en/rest/repos/rules>, <https://docs.github.com/rest/branches/branch-protection>
- GitHub Actions secure use and workflow artifacts: <https://docs.github.com/en/actions/reference/security/secure-use>, <https://docs.github.com/en/actions/tutorials/store-and-share-data>
- GitHub artifact attestations and offline verification: <https://docs.github.com/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds>, <https://docs.github.com/actions/security-for-github-actions/using-artifact-attestations/verifying-attestations-offline>
- GitHub repository security advisories: <https://docs.github.com/code-security/security-advisories/repository-security-advisories/about-repository-security-advisories>
- SLSA v1.0 provenance and verification: <https://slsa.dev/spec/v1.0/provenance>, <https://slsa.dev/spec/v1.0/verifying-artifacts>
- Sigstore/Cosign signing and verification: <https://docs.sigstore.dev/quickstart/quickstart-cosign/>, <https://docs.sigstore.dev/cosign/verifying/verify/>
- Python packaging and Twine checks: <https://packaging.python.org/tutorials/packaging-projects/>, <https://packaging.python.org/guides/distributing-packages-using-setuptools/>
- CycloneDX and SPDX SBOM standards: <https://cyclonedx.org/specification/overview/>, <https://spdx.dev/use/specifications/>
- OpenSSF Scorecard: <https://scorecard.dev/>
- NIST SSDF SP 800-218: <https://csrc.nist.gov/pubs/sp/800/218/final>

## Current State Summary

CertaMerge open source currently has:

- branch-local GitHub CI;
- Python 3.11 and 3.12 test matrix;
- package build;
- Twine check;
- checksum generation;
- GitHub Action validation;
- CertaMerge self-gate proof;
- sample CAR verification;
- security policy;
- public docs with safe compliance language.

The current public `main` branch remote checks are green after commit `512ee5a`.

## Now: Required For Community Alpha

These are already appropriate for the current alpha and should remain required:

| Area | CertaMerge Requirement |
|---|---|
| Required checks | Keep CI and CertaMerge proof gate green before release work |
| Python packaging | Build wheel/sdist and run `twine check dist\*` before publishing |
| Artifact retention | Upload CAR/proof artifacts in CI when feasible, with defined retention |
| Security policy | Keep `SECURITY.md` clear about disclosure and non-claims |
| Safe GitHub Actions | Avoid untrusted code checkout assumptions and keep token permissions minimal |
| CAR verification | Require local `verify-car` for generated proof records |
| Checksums | Generate SHA-256 checksums for release artifacts |
| Public claim discipline | Say release-ready/community alpha, not enterprise production-ready |

## Next: Release-Hardening Work

These are not blockers for community alpha, but they are the next hardening layer:

| Area | Next Action |
|---|---|
| Repository rulesets | Configure GitHub rulesets or branch protection for required CI and proof checks |
| Artifact attestations | Add GitHub artifact attestations for built distributions |
| SLSA provenance | Emit provenance for release artifacts and document verification |
| Sigstore/Cosign | Sign release archives or attestations once release identity/key strategy is chosen |
| SBOM | Generate CycloneDX or SPDX SBOM for the package and release bundle |
| Security advisories | Enable and document repository security advisory workflow |
| OpenSSF Scorecard | Add Scorecard evaluation and record exceptions |
| Dependency automation | Add dependency update policy and vulnerability triage workflow |
| Changelog/versioning | Formalize release notes, breaking-change policy, and schema compatibility notes |

## Not Now

These should not be forced into the public alpha yet:

- enterprise RBAC/SSO;
- deployment manifests;
- hosted SaaS telemetry;
- production KMS/HSM;
- enterprise retention/query service;
- compliance mappings as marketing claims;
- SLSA compliance claims before provenance and verification are actually implemented.

## CertaMerge-Specific Decision

CertaMerge should treat public release readiness as:

```text
tests + build + package metadata + CAR verification + GitHub proof gate + safe docs + no leakage
```

It should treat supply-chain maturity as a staged path:

```text
checksums -> SBOM -> attestations -> signatures -> provenance verification -> release policy gate
```

The public alpha has reached the first stage. It has not reached the later stages.

## Anti-Slop Gate

This standards review rejects:

- a generic badge-collection roadmap;
- claiming SLSA, SOC 2, or secure-by-default status;
- turning CertaMerge into a scanner;
- making artifact signing look complete before key/signature verification is real;
- shipping release artifacts without a verifier story.

## Final Decision

```text
CURRENT PRODUCTION READINESS STANDARDS REVIEW COMPLETE — COMMUNITY ALPHA RELEASE READY WITH SUPPLY-CHAIN HARDENING NEXT
```
