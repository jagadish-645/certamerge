# Compliance Safe Language Scan

## Scope

This scan covers public-facing self-dogfood docs, templates, and release reports added by the branch.

## Required Language

Public CertaMerge language should use:

- policy requires
- missing proof
- evidence present
- evidence unavailable
- verification
- owner approval required
- override recorded
- Change Authorization Record
- may support audit or change-control review

## Forbidden Claim Pattern

Public CertaMerge language must not claim that the community alpha:

- makes code secure;
- guarantees production safety;
- certifies compliance;
- replaces scanners;
- replaces human review;
- provides non-repudiable approval;
- cryptographically signs CARs;
- authorizes production through an LLM.

## Branch Language Finding

The branch describes CertaMerge as a local proof and change-authorization record tool. It uses limitations language for community alpha CARs, signing, enterprise features, and live GitHub Action validation.

## Review Commands

Recommended scan:

```powershell
rg -n --hidden -g '!.git/**' -g '!*.egg-info/**' -g '!__pycache__/**' -g '!.pytest_cache/**' '(guarantees production safety|certifies compliance|makes code secure|replaces scanners|non-repudiable|cryptographically signs CARs)' README.md SECURITY.md docs .github
```

Allowed hits are only acceptable when they appear inside explicit non-claims or limitations sections.

## Verdict

The branch is compliance-language safe for public alpha review if the scan returns only explicit non-claim contexts.
