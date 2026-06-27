# CAR Signing

CertaMerge Community Alpha currently produces hash-bound CARs, not cryptographically signed CARs.

## Current Community Alpha Behavior

Every generated CAR includes:

- deterministic JSON canonicalization label;
- SHA-256 `integrity.content_hash`;
- policy file hash when a policy file is provided;
- evidence artifact hashes when evidence files are referenced;
- verifier-side tamper detection through `python -m certamerge verify-car`.

This supports local integrity checks. It does not provide signer identity, key custody, key rotation, revocation, timestamp authority, or non-repudiation.

## Why Signing Is Deferred

Cryptographic signing is intentionally deferred from v0.1.0 alpha because doing it credibly requires more than adding a signature field:

- key generation and storage rules;
- public-key distribution;
- signing-key rotation;
- compromised-key response;
- timestamping policy;
- signed release manifest alignment;
- offline verification UX;
- enterprise KMS/HSM compatibility;
- clear language that avoids overclaiming non-repudiation.

Adding an Ed25519 dependency without this operational model would create a false sense of enterprise assurance.

## Production Signing Direction

A future signing design should support:

```text
certamerge keygen --out .certamerge/keys/dev
certamerge sign-car .tmp/change.car.json --key .certamerge/keys/dev/private.key --output .tmp/change.signed.car.json
certamerge verify-car .tmp/change.signed.car.json --public-key .certamerge/keys/dev/public.key
```

Minimum required fields for signed CARs:

- signature algorithm;
- signer key id;
- public-key fingerprint;
- canonical payload hash;
- signature bytes;
- signing timestamp;
- verifier version;
- optional certificate or key manifest reference;
- revocation/rotation metadata when available.

## Safe Language

Allowed:

```text
Community alpha CARs are verifier-checked and SHA-256 hash-bound.
```

Forbidden:

```text
Community alpha CARs are non-repudiable.
Community alpha CARs are cryptographically signed.
Community alpha CARs are approved by auditors.
```
