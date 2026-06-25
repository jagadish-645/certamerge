# CAR Integrity

CertaMerge Community alpha uses verifier-checked content hashes for Change Authorization Records.

It does not implement cryptographic CAR signing yet.

## Implemented Now

Every generated CAR includes an `integrity` object with:

- canonicalization method;
- SHA-256 hash algorithm;
- content hash;
- verifier version.

The content hash is computed from the canonical JSON representation of the CAR with the `integrity` object excluded. This lets the verifier detect local tampering after the CAR was written.

## Verifier Checks

`python -m certamerge verify-car path/to/car.json` checks:

- CAR JSON parseability;
- CAR schema validity;
- verdict and missing-proof consistency;
- evidence-state validity;
- missing-proof-state validity;
- `ALLOW` cannot carry missing proof;
- `NEEDS_EVIDENCE` must carry missing proof;
- `REPAIR_REQUIRED` must carry repair missions;
- `OVERRIDE_RECORDED` must use the override record state;
- content-hash mismatch after CAR tampering.

## What This Protects

The current integrity model helps detect:

- accidental CAR corruption;
- manual edits to verdict text;
- manual edits to evidence states;
- manual edits to missing proof;
- manual edits to repair missions or policy trace.

## What This Does Not Protect Yet

The current model does not provide:

- signer identity;
- non-repudiation;
- key rotation;
- revocation;
- trusted timestamping;
- external attestation;
- cryptographic proof that a specific CertaMerge instance produced the CAR.

## Production Requirement

Before production release, CertaMerge must implement practical signed CARs with:

- asymmetric signatures;
- deterministic canonical JSON;
- offline verification;
- public key manifest;
- key rotation and revocation;
- compromised-key response;
- signing failure behavior;
- signature test vectors.

## Safe Public Wording

Use:

```text
Community alpha CARs are integrity-bound with a verifier-checked SHA-256 content hash.
```

Do not use:

```text
Community alpha CARs are cryptographically signed.
```
