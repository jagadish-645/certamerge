# CAR Integrity Release Decision

## Decision

Use Option B for community alpha:

```text
Implement integrity hashes now and formally defer cryptographic signing.
```

## Reason

Community alpha already has meaningful CAR integrity through canonical SHA-256 content hashes and verifier checks. Adding signing without a complete key lifecycle would create a false trust claim.

The safe release decision is to document the current integrity model clearly and make cryptographic signing a production requirement.

## Current Integrity Model

Implemented:

- canonical JSON content hashing;
- SHA-256 content hash stored in CAR integrity metadata;
- verifier check for content-hash mismatch;
- schema validation;
- verdict consistency validation;
- evidence-state validation;
- missing-proof-state validation;
- sample CAR verification;
- tamper-detection tests.

## Threats Not Solved Yet

Current community alpha does not solve:

- signer identity;
- non-repudiation;
- key rotation;
- revocation;
- trusted timestamping;
- compromised-key response;
- proof that a specific CertaMerge instance generated a CAR.

## Public Wording

Allowed:

```text
Community alpha CARs are integrity-bound with a verifier-checked SHA-256 content hash.
```

Forbidden:

```text
Community alpha CARs are cryptographically signed.
```

## Production Requirement

Before production release, implement signed CARs with:

- asymmetric signing;
- offline verification;
- public key manifest;
- revocation model;
- key rotation;
- signing failure behavior;
- signature mismatch tests;
- compromised-key response plan.

## Verdict

CAR integrity is honest and useful for community alpha.

Cryptographic signing remains a launch blocker for production-grade enterprise authorization.
