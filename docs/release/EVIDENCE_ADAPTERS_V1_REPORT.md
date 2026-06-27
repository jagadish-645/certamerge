# Evidence Adapters V1 Report

Date: 2026-06-27

## Summary

Implemented pragmatic evidence adapter v1 support for common test, scanner, SBOM, Terraform, and secret-scan artifacts. The implementation normalizes evidence states and remains metadata-only.

## Implemented Adapters

| Adapter | States covered |
|---|---|
| JUnit XML | `present`, `failed`, `malformed`, `insufficient` |
| SARIF | `negative`, `failed`, `malformed` |
| CycloneDX/SBOM JSON/XML | `present`, `malformed`, `insufficient` |
| Terraform plan JSON | `present`, `malformed`, `insufficient` |
| Gitleaks/secret scan JSON | `negative`, `failed`, `malformed`, `insufficient` |
| Existing test-result JSON | `present`, `failed`, `stale`, `unavailable`, `insufficient`, `malformed` |
| Existing owner approval JSON | `present`, `failed`, `stale`, `unavailable`, `insufficient`, `conflicting`, `malformed` |

## Validation

Focused evidence-state suite passed:

```text
20 passed
```

New tests cover:

- valid JUnit pass;
- JUnit failed;
- malformed JUnit;
- CycloneDX/SBOM present;
- malformed SBOM;
- Terraform plan present;
- malformed Terraform plan;
- Gitleaks negative;
- Gitleaks failed;
- malformed Gitleaks.

Existing tests cover:

- SARIF negative;
- SARIF failed;
- malformed SARIF;
- failed test evidence;
- stale owner approval;
- conflicting approval;
- malformed CAR hash behavior.

## Anti-Slop Boundary

The adapters do not run scanners or replace security tools. They only parse existing artifacts and turn them into evidence states that CertaMerge policy can evaluate.

## Verdict

```text
EVIDENCE ADAPTERS V1 IMPLEMENTED FOR COMMUNITY ALPHA
```

