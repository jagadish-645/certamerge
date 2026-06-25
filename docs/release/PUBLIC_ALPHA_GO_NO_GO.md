# Public Alpha Go/No-Go

## Executive Verdict

```text
GO
```

CertaMerge is public-alpha ready with explicit limitations. The public repository contains the community-safe surface, CI passes, and GitHub Action validation covers sample allow, observe, and configured-block paths.

## Gate Checklist

| Gate | Status | Evidence |
|---|---|---|
| Repo is isolated | Pass | Public repository tracks only community-safe files. |
| Repo is clean | Pass | Public branch has no generated cache, local path, or internal strategy artifact tracked. |
| Public boundary is applied | Pass | Community package excludes enterprise runtime and internal agent-system material. |
| GitHub target repo exists | Pass | `jagadish-645/certamerge` is the public community repository. |
| Install works | Pass | Clean editable install was verified. |
| CLI works | Pass | `python -m certamerge --help`, Recover, Gate, verify, explain verified. |
| Sample flows work | Pass | Recover no-CI sample and Gate payment sample verified. |
| Tests pass | Pass | Mixed root tests pass; public staging and enterprise staging tests pass independently. |
| GitHub Action static validation | Pass | Tests and CI validate metadata/action contract. |
| GitHub Action live validation | Pass | Built-in live workflow validates allow, observe, and configured-block sample paths. |
| README is strong | Pass | README answers the 15 first-30-second questions. |
| No-source-egress posture documented | Pass | README, SECURITY, no-source-egress docs, and tests cover it. |
| Compliance-safe language used | Pass | Docs use support/evidence language and list forbidden claims. |
| CAR integrity status is honest | Pass | Hash integrity documented; signing deferred. |
| Known limitations are public | Pass | `docs/community/alpha-limitations.md`. |
| Release artifact integrity | Partial | Source-controlled alpha checksums exist; signed release/SBOM automation remains release-hardening work. |

## Public Alpha Conditions Satisfied

- public/community repo tree is separated from enterprise-only material;
- initial public commits exist;
- public remote is configured;
- public package metadata is community-only;
- public-only test run passes from the staged public repo;
- GitHub Action live validation is completed;
- release checksum notes exist;
- README and limitations remain honest.

## Remaining Non-Blocking Alpha Limitations

1. Release artifacts are not built with signed archives or SBOM automation.
2. Public checksums cover selected source-controlled alpha files, not distribution archives.
3. CAR cryptographic signing remains deferred.
4. Enterprise deployment, org policy, ProofGraph, and audit export are outside community alpha.

## Maintainer Actions Before Stable Release

1. Add release SBOM/checksum workflow for packaged artifacts.
2. Decide public release signing method.
3. Implement production-grade CAR cryptographic signing before production authorization claims.
4. Collect public alpha issue feedback and demo results.

## Final Gate

```text
CERTAMERGE PUBLIC ALPHA GO
```
