# Evidence Ingestion Evolution Report

## Summary

CertaMerge evidence ingestion now combines two deterministic sources:

1. metadata evidence files under `.certamerge/evidence/`;
2. native repository and workflow signals.

The implementation still avoids deep source-code analysis. It reads metadata, repository structure, selected config files, scanner/test evidence files, and proof references.

## Supported Evidence Sources

Implemented deterministic evidence sources include:

- `.certamerge/evidence/*test-result*.json`;
- `.certamerge/evidence/*approval*.json`;
- SARIF files;
- GitHub Actions workflow files;
- package manager manifests;
- dependency lockfiles;
- SBOM JSON/XML references;
- dependency review evidence files;
- `SECURITY.md`;
- `CODEOWNERS`;
- `LICENSE`;
- pull request templates;
- issue templates;
- `action.yml` / `action.yaml`;
- Terraform files;
- Terraform validation evidence references;
- Terraform plan evidence references;
- docs site files and docs build references;
- CertaMerge CAR verification evidence references;
- no-source-egress evidence references;
- risk-surface-classification evidence references;
- workflow-validation evidence references;
- action-contract-validation evidence references;
- schema-validation evidence references;
- compliance-safe-language evidence references;
- no-secret-leakage evidence references;
- link-validation evidence references.

## Evidence States

CertaMerge recognizes the full community alpha evidence-state taxonomy:

| State | Meaning |
|---|---|
| `present` | Evidence exists and satisfies the requirement. |
| `missing` | Required evidence was not found. |
| `unavailable` | Evidence was explicitly reported unavailable. |
| `stale` | Evidence exists but is expired. |
| `malformed` | Evidence exists but could not be parsed safely. |
| `failed` | Evidence exists and reports failure or denial. |
| `negative` | Scanner evidence exists and reports no findings. |
| `insufficient` | Evidence exists but lacks enough fields to prove pass/fail. |
| `conflicting` | Multiple evidence references disagree in a blocking way. |

## Implemented Parser Behavior

Test result evidence:

- passing status -> `present`;
- failing status -> `failed`;
- expired `expires_at` -> `stale`;
- explicit unavailable status -> `unavailable`;
- parse failure -> `malformed`;
- missing pass/fail status -> `insufficient`.

Owner approval evidence:

- approved decision -> `present`;
- denied/rejected decision -> `failed`;
- expired `expires_at` -> `stale`;
- explicit unavailable decision -> `unavailable`;
- approved and denied references together -> `conflicting`;
- missing approval decision -> `insufficient`.

SARIF evidence:

- parse failure -> `malformed`;
- no results -> `negative`;
- one or more results -> `failed`.

Native repo signals:

- workflow files produce CI/GitHub Actions references;
- lockfiles/SBOM/dependency-review evidence produce dependency references;
- security/license/CODEOWNERS/templates produce governance references;
- Terraform/docs/action metadata produce profile-specific references.

## Gate Behavior

Policy evaluation now treats evidence states deterministically:

- `present` and `negative` satisfy requirements;
- `failed` and `conflicting` produce `BLOCK`;
- `missing`, `unavailable`, `stale`, `malformed`, and `insufficient` produce the policy's configured missing-proof verdict, commonly `NEEDS_EVIDENCE`.

This prevents failed or conflicting proof from looking merely absent.

## Tests Added Or Confirmed

Focused evidence tests now cover:

- present native signal;
- missing native signal;
- malformed SARIF;
- stale approval;
- failed test evidence;
- denied approval;
- negative SARIF;
- unavailable test evidence;
- unavailable approval evidence;
- insufficient test evidence;
- conflicting approval evidence;
- CAR verification after tampering.

Focused result:

```text
129 passed
```

Full current test result after this slice:

```text
235 passed
```

## Anti-Slop Assessment

This is not a scanner wrapper because CertaMerge does not claim to find vulnerabilities itself. It normalizes scanner, CI, policy, approval, repository, and proof metadata into decision-grade evidence states.

It is not a GitHub rules clone because GitHub branch rules usually reason about pass/fail checks, while CertaMerge distinguishes missing, unavailable, stale, malformed, failed, negative, insufficient, and conflicting proof.

## Current Limits

- JUnit XML parsing is not implemented yet.
- Terraform plan JSON summarization is not implemented yet.
- SBOM content parsing is not implemented yet.
- GitHub Actions artifacts are represented through workflow references and local metadata evidence, not downloaded artifacts.
- Evidence file trust is currently verifier-checked by SHA-256 hash binding, not by signed provenance.
- Scanner adapters beyond basic SARIF parsing remain future work.

## Verdict

Evidence ingestion is materially stronger than static file presence checks and is ready for the wrapper-kill validation loop.

