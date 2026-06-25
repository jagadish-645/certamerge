# SBOM And Provenance Plan

## Purpose

CertaMerge should not ask customers to trust proof records while shipping unverifiable release artifacts. Public release needs a supply-chain evidence plan.

## Dependency And License Audit

Initial command options:

```powershell
python -m pip install pip-audit pip-licenses cyclonedx-bom
python -m pip_audit
python -m piplicenses --format=markdown --with-license-file
python -m cyclonedx_py environment --output-file sbom.cdx.json
```

These commands are plan candidates. They are not yet wired into CI.

## SBOM Plan

Release artifacts should include:

- CycloneDX JSON SBOM for Python dependencies;
- package version;
- source commit hash;
- generated timestamp;
- tool name and version;
- dependency names, versions, licenses, and hashes when available.

## Provenance Plan

Release provenance should record:

- repository URL;
- commit SHA;
- workflow run ID;
- Python version;
- build command;
- test command;
- package artifact names;
- SBOM artifact name;
- checksum manifest.

## Vulnerability Review Plan

Before public release:

1. Run dependency vulnerability audit.
2. Review license inventory.
3. Flag copyleft or source-available license risks.
4. Publish security contact.
5. Create advisory workflow.
6. Add recurring dependency update policy.

## Current Status

Not implemented as a release workflow yet.

This is acceptable for local public-release-candidate hardening, but public publication should not claim SBOM-backed or provenance-signed release artifacts until the workflow exists and has been run.

## Release Blocker Status

SBOM/provenance is a public release hardening blocker for a polished release, not a blocker for local alpha testing.
