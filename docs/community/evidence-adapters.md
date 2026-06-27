# Evidence Adapters

CertaMerge Community Alpha normalizes a small set of common evidence artifact formats into evidence states. It does not replace scanners or test runners. It reads metadata artifacts that already exist and converts them into policy-usable proof signals.

## Evidence States

Adapters may produce:

```text
present
missing
unavailable
stale
malformed
failed
negative
insufficient
conflicting
```

`present` and `negative` satisfy policy requirements. Other states require repair, review, or additional proof.

## Supported V1 Inputs

| Evidence | Artifact shape | Output |
|---|---|---|
| Test command | `package.json` test script | `test_result: present`, `missing`, or `failed` |
| Test result JSON | `.certamerge/evidence/*test-result*.json` | `test_result` state from explicit status |
| JUnit XML | files named like `junit.xml`, `test-results.xml`, or under `surefire-reports` | `test_result: present`, `failed`, `malformed`, or `insufficient` |
| SARIF | `*.sarif` or `*.sarif.json` | `sarif_scan: negative`, `failed`, or `malformed` |
| CycloneDX/SBOM | `*sbom*.json`, `*cyclonedx*.json`, `bom.json`, or XML equivalents | `dependency_reference: present`, `malformed`, or `insufficient` |
| Lockfiles | `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `poetry.lock`, `go.sum` | `dependency_reference: present` |
| Terraform plan JSON | `terraform-plan*.json`, `*tfplan*.json`, or `plan.json` | `terraform_plan: present`, `malformed`, or `insufficient` |
| Gitleaks/secret scan JSON | `*gitleaks*.json`, `*secret-scan*.json`, or `*secrets-scan*.json` | `secret_scan: negative`, `failed`, `malformed`, or `insufficient` |
| Owner approval JSON | `.certamerge/evidence/*approval*.json` | `owner_approval: present`, `failed`, `stale`, `unavailable`, `insufficient`, `conflicting`, or `malformed` |

## What CertaMerge Does Not Do

CertaMerge does not:

- run CodeQL, Semgrep, Trivy, Gitleaks, Terraform, pytest, npm, or any scanner by itself;
- inspect raw source code for vulnerabilities;
- claim a finding-free scan proves a change is safe;
- upload artifacts to a vendor service;
- store raw scanner payloads in the CAR beyond metadata references and hashes.

## Adapter Rules

Every adapter must:

- parse defensively;
- classify malformed input as `malformed`;
- avoid crashing on missing fields;
- produce metadata summaries only;
- preserve artifact references and SHA-256 hashes when included in a CAR;
- avoid raw source-code and secret egress;
- avoid unsafe compliance/security claims.

## Repair Meaning

Examples:

- `test_result: failed` means tests ran and failed.
- `test_result: malformed` means the evidence file could not be parsed.
- `sarif_scan: negative` means SARIF was valid and contained zero results.
- `sarif_scan: failed` means SARIF contained findings; it does not mean CertaMerge found vulnerabilities.
- `secret_scan: failed` means the secret-scan artifact reported findings; CertaMerge did not independently find secrets.

