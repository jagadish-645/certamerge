# Release Artifact Integrity Plan

## Purpose

CertaMerge release artifacts should be independently verifiable by users before they install or run a proof-authorizing tool.

## Artifact Types

Expected public artifacts:

- source archive;
- Python source distribution;
- Python wheel;
- SBOM;
- checksum manifest;
- release notes;
- GitHub Action tag;
- CAR sample bundle.

Expected enterprise artifacts later:

- private enterprise package;
- deployment bundle;
- audit export bundle;
- support bundle schema;
- enterprise trust packet.

## Checksum Plan

Each public release should publish a checksum manifest:

```text
SHA256SUMS
```

The manifest should include every release artifact and be stored with the release.

## Signing Plan

Public release should define one release-signing path before broad publication:

- signed Git tags;
- signed checksum manifest;
- future package signing when packaging channel supports it.

Do not claim signed releases until signing is implemented and verification instructions are published.

## Verification Instructions To Publish

Future release docs should include:

```powershell
Get-FileHash .\certamerge-<version>.whl -Algorithm SHA256
```

and equivalent Unix instructions.

## Current Status

Not implemented yet:

- signed release artifact;
- checksum manifest;
- release SBOM;
- provenance artifact;
- public verification command in a release page.

## Required Before Public Launch

1. Build release artifacts in CI.
2. Generate checksum manifest.
3. Generate SBOM.
4. Decide signing method.
5. Publish verification instructions.
6. Verify a clean install from release artifacts, not only editable install.

## Verdict

Release artifact integrity is planned but not complete.

Public alpha should remain blocked until at least checksums, SBOM, and release verification instructions exist.
