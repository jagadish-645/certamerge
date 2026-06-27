# CAR Signing V0 Decision Report

Date: 2026-06-27

## Decision

```text
DEFER CRYPTOGRAPHIC CAR SIGNING FROM COMMUNITY V0.1.0 ALPHA
```

## Current State

CertaMerge Community Alpha supports hash-bound CAR integrity:

- CAR content hash;
- policy file hash;
- evidence artifact hashes;
- verifier-side tamper detection.

`python -m certamerge verify-car` confirms whether the CAR content, policy file, and referenced evidence hashes still match.

## Why Signing Is Not Implemented In This Pass

Adding Ed25519 signing without key management would create misleading trust language. A real signing model needs:

- local key storage rules;
- key rotation;
- public-key distribution;
- compromised-key response;
- timestamping;
- release manifest alignment;
- offline verification UX;
- future enterprise KMS/HSM compatibility.

## Production Direction

Future commands should be designed around:

```text
certamerge keygen
certamerge sign-car
certamerge verify-car --public-key
```

The implementation must make unsigned CARs visibly different from signed CARs and must not describe unsigned CARs as non-repudiable.

## Current Safe Claim

```text
Community alpha CARs are SHA-256 hash-bound and verifier-checked.
```

## Forbidden Claims

```text
Community alpha CARs are cryptographically signed.
Community alpha CARs are non-repudiable.
Community alpha CARs prove signer identity.
```

## Verdict

```text
CAR SIGNING DEFERRED HONESTLY — HASH-BOUND CAR INTEGRITY REMAINS ACTIVE
```
