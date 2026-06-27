# CAR Signing Design

Status: deferred from community `v0.1.0-alpha`

This document defines the minimum credible design for future cryptographic CAR signing. It is not implemented in the community alpha.

## Current State

Community alpha CARs are hash-bound and verifier-checked:

- canonical CAR content hash;
- policy hash when a policy file is available;
- evidence hashes when evidence files are referenced;
- offline `verify-car` tamper detection.

Community alpha CARs are not cryptographically signed and do not provide signer identity, revocation, key rotation, timestamp authority, or non-repudiation.

## Design Goals

Future signing must provide:

- signer identity without exposing private keys;
- deterministic canonical payload signing;
- offline verification;
- key rotation and revocation;
- clear unsigned/signed status in `verify-car`;
- dev-local signing for community experimentation;
- enterprise KMS/HSM compatibility later;
- no source-code egress;
- no vendor callback requirement.

## Non-Goals

This design must not:

- claim certification;
- claim non-repudiation until key custody is real;
- require a hosted CertaMerge service;
- send CARs, source code, diffs, secrets, or scanner payloads to a vendor service;
- let an LLM authorize a verdict;
- hide unsigned CARs behind optimistic language.

## Proposed Signed CAR Fields

```json
{
  "signature": {
    "state": "signed",
    "algorithm": "Ed25519",
    "key_id": "dev-local-key-001",
    "public_key_fingerprint": "sha256:<fingerprint>",
    "signed_payload_hash": "sha256:<canonical-car-without-signature>",
    "signature": "base64:<signature-bytes>",
    "signed_at": "2026-06-27T00:00:00Z",
    "verifier_version": "certamerge-community-0.1.x",
    "key_manifest_ref": "optional path or URI",
    "revocation_ref": "optional path or URI"
  }
}
```

Unsigned CARs must remain explicit:

```json
{
  "signature": {
    "state": "unsigned",
    "reason": "community alpha signing not configured"
  }
}
```

## Canonicalization Rule

Signing must use the same deterministic canonicalization path as content-hash verification.

Rules:

- remove the `signature` object before computing `signed_payload_hash`;
- canonicalize JSON with stable key order and stable separators;
- hash the canonical bytes with SHA-256;
- sign the SHA-256 digest or canonical payload according to the selected algorithm specification;
- verify by recomputing the canonical payload hash before checking the signature.

## CLI Contract

Future command shape:

```powershell
python -m certamerge keygen --output .certamerge/keys/dev
python -m certamerge sign-car .tmp/change.car.json --key .certamerge/keys/dev/private.key --output .tmp/change.signed.car.json
python -m certamerge verify-car .tmp/change.signed.car.json --public-key .certamerge/keys/dev/public.key
```

`verify-car` must report:

- CAR integrity result;
- signature state;
- signer key id;
- public-key fingerprint;
- signature verification result;
- revocation check status if a revocation source is supplied;
- clear warning when a CAR is unsigned.

## Key Modes

Community dev-local mode:

- locally generated keypair;
- file permissions documented;
- public key checked into a demo keyring only for samples;
- no claim of enterprise custody.

Enterprise mode later:

- KMS/HSM-backed signing;
- key rotation;
- revocation list;
- key manifest signing;
- separation between release signing and CAR signing keys;
- support for air-gapped verification bundles.

## Verification Failure States

`verify-car` must fail or warn precisely:

| State | Behavior |
|---|---|
| unsigned CAR | Valid integrity may pass, signature status warns `unsigned` |
| missing public key | Verification fails with key-not-found |
| signature mismatch | Verification fails |
| payload hash mismatch | Verification fails |
| revoked key | Verification fails |
| expired key | Verification fails or warns based on strict mode |
| unsupported algorithm | Verification fails |
| malformed signature | Verification fails |

## Acceptance Criteria For Implementation

- Existing unsigned CARs remain verifiable with explicit unsigned warning.
- Signed CARs verify offline without network access.
- Tampering with any signed field fails verification.
- Tampering with the signature object fails verification.
- Key rotation and revocation metadata are represented before enterprise claims are made.
- Tests cover unsigned, signed, tampered, missing-key, revoked-key, expired-key, malformed-signature, and unsupported-algorithm cases.

## Safe Language

Allowed after implementation:

```text
This CAR signature verified against the configured public key.
```

Allowed before implementation:

```text
Community alpha CARs are hash-bound but unsigned.
```

Forbidden:

```text
CertaMerge CARs are non-repudiable.
CertaMerge guarantees the signer identity.
CertaMerge is audit-certified because CAR signing exists.
```
