# CAR Signing And Integrity

## Purpose

This document defines the v0 integrity model for CertaMerge Change Authorization Records.

It does not fake cryptographic signing. It clearly separates what exists now from what must be implemented before production release.

## Implemented Now

Community CARs include an `integrity` object:

```json
{
  "canonicalization": "certamerge-json-canonical-v0",
  "content_hash": "sha256:<hash>",
  "hash_algorithm": "sha256",
  "verifier_version": "certamerge-community-<version>"
}
```

The content hash is computed over the canonical JSON representation of the CAR excluding the `integrity` object itself.

The verifier currently checks:

- CAR schema validity;
- verdict and missing-proof consistency;
- evidence state validity;
- missing-proof state validity;
- `ALLOW` cannot include missing proof;
- `NEEDS_EVIDENCE` requires missing proof;
- `REPAIR_REQUIRED` requires repair missions;
- `OVERRIDE_RECORDED` requires `record_state: override_recorded`;
- `content_hash` mismatch after CAR tampering.

## Implemented Test Evidence

The test suite includes:

- CAR tamper detection through changed content hash;
- invalid verdict-state combinations;
- invalid evidence states;
- invalid missing-proof states;
- valid sample CAR verification.

## Designed But Not Implemented

Full cryptographic signing is not implemented in this controlled alpha.

The production signing design should use:

- asymmetric signatures, preferably Ed25519;
- deterministic canonical JSON;
- key separation for CAR signing, release signing, and future attestation signing;
- public key manifest;
- key rotation with overlap;
- revocation list;
- offline verification with no network dependency;
- test vectors for valid, tampered, expired, and revoked-key CARs.

## Future Production Requirement

Before production launch, CertaMerge must implement:

- signed CARs;
- key manifest schema;
- revocation-list schema;
- signing-key generation and storage procedure;
- offline signature verification command;
- signing failure behavior;
- signature mismatch tests;
- key rotation tests;
- compromised-key response plan.

## Non-Claims

The current v0 content hash is tamper-evident for local files. It is not non-repudiation, identity proof, or cryptographic authorization by an external signer.

Controlled alpha may say:

```text
CARs are integrity-bound with a verifier-checked SHA-256 content hash.
```

Controlled alpha must not say:

```text
CARs are cryptographically signed.
```
