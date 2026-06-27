# Change-Bound CAR Report

## Summary

CertaMerge Gate now produces CARs that are bound to the local or GitHub Actions change context, the policy file used for evaluation, and resolvable evidence artifact files.

This directly addresses the static-template risk. A useful proof record must describe the exact context it evaluated and must detect when the policy or evidence it relied on changes afterward.

## Implementation Changes

- Added change context collection in the CAR builder.
- Added local Git metadata when available:
  - branch;
  - current commit SHA;
  - dirty working tree flag;
  - unavailable-context list.
- Added GitHub Actions metadata when available:
  - repository;
  - PR number from `GITHUB_REF`;
  - run ID;
  - run URL;
  - base/head refs;
  - base/head SHAs.
- Added policy source binding:
  - policy path;
  - resolved policy path;
  - SHA-256 policy file hash.
- Added evidence artifact binding:
  - artifact path;
  - SHA-256 artifact file hash;
  - per-evidence `artifact_hashes`;
  - replay-level `evidence_artifact_hashes`.
- Extended `verify-car` to fail when:
  - the policy file hash no longer matches;
  - a bound evidence artifact hash no longer matches;
  - a referenced bound file is unavailable.
- Extended `explain-car` with commit and policy hash lines.

## Verification Tests Added

Focused contract tests now cover:

- policy file hash binding;
- policy file mutation after CAR generation;
- evidence file hash binding;
- evidence file mutation after CAR generation;
- missing local Git context recording;
- GitHub Actions context recording.

Focused result:

```text
119 passed
```

## Trust Boundary

This implementation reads local metadata and files only. It does not send source code, evidence, policy, CARs, or telemetry to a vendor service.

The implementation records hashes and metadata. It does not record raw source code or raw diffs.

## What Is Still Not Implemented

- Cryptographic CAR signing.
- Key management.
- Trusted timestamping.
- External attestation.
- Ledger chaining.
- Deep replay of a historical policy engine version.
- Git diff-aware base/head comparison outside available GitHub metadata.

## Anti-Slop Assessment

This is materially stronger than a static checklist because the CAR now answers:

- what policy file was used;
- whether that policy file changed after the CAR was generated;
- what evidence artifacts were referenced;
- whether those evidence artifacts changed after the CAR was generated;
- what commit/run context was available;
- what context was unavailable instead of guessed.

## Current Limitations

- If a CAR is moved to another machine, policy/evidence file hash rechecking requires those referenced files to be available at their recorded paths.
- Native repo signals such as `package.json:scripts.test` may be recorded as evidence references but are not always file-hashed when the reference is virtual.
- Community alpha verification remains local integrity verification, not signed attestation.

## Verdict

Change-bound CARs are now strong enough for the wrapper-kill validation loop. They do not yet satisfy production signed-proof requirements.

