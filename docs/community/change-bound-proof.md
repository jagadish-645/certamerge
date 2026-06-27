# Change-Bound Proof

CertaMerge Community alpha now binds generated CARs to the change context, policy file, and evidence artifact references that were available when the CAR was created.

This is not cryptographic signing. It is local, verifier-checked integrity binding for the proof record.

## What Gets Recorded

When `gate` writes a CAR, the record includes:

- repository path and repository name;
- branch when Git or GitHub Actions context is available;
- current commit SHA when Git or GitHub Actions context is available;
- base/head SHA when GitHub Actions provides them;
- PR number when running in a pull request workflow;
- GitHub run ID and run URL when running in GitHub Actions;
- policy file path and SHA-256 file hash;
- evidence artifact paths and SHA-256 file hashes when the referenced files are resolvable;
- CertaMerge evaluator version;
- generated timestamp;
- CAR content hash.

Unavailable values are recorded as `unavailable`. CertaMerge does not invent commit SHAs, PR numbers, run IDs, or base refs.

## Verification Behavior

`python -m certamerge verify-car <car>` checks:

- CAR schema validity;
- verdict and missing-proof consistency;
- evidence state validity;
- CAR content hash integrity;
- policy file hash integrity when a policy file was used;
- evidence artifact hash integrity when evidence artifact hashes are present.

If the policy file or a bound evidence artifact changes after CAR generation, verification fails.

## What This Prevents

Change-bound proof helps catch:

- a CAR generated with one policy and reviewed after the policy changed;
- evidence files that changed after the CAR was produced;
- manual CAR edits;
- CARs that lack available local/GitHub context;
- proof records that cannot explain what repo/change context they describe.

## What It Does Not Claim

CertaMerge Community alpha still does not claim:

- cryptographic CAR signing;
- trusted timestamping;
- signer identity;
- non-repudiation;
- authoritative compliance certification;
- deep source-code analysis.

## Local Example

```powershell
python -m certamerge gate --repo . --policy .certamerge.yml --output .tmp/change-bound.car.json
python -m certamerge verify-car .tmp/change-bound.car.json
python -m certamerge explain-car .tmp/change-bound.car.json
```

Expected verification shape:

```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "car_id": "car_certamerge_...",
  "verdict": "OBSERVE_ONLY_WOULD_ALLOW"
}
```

## Privacy Boundary

The CAR stores metadata and hashes. It does not store raw source code, raw diffs, tokens, or secret values by design.

Evidence artifact hashes are used to detect mutation of referenced files. They are not a substitute for signed provenance.

