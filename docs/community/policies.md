# Policies

CertaMerge Community supports simple YAML policies:

```yaml
version: 0.1
mode: observe
rules:
  - id: CM-AUTH-001
    when:
      paths:
        - "src/auth/**"
        - "app/auth/**"
    require:
      evidence:
        - tests
        - owner_approval
    verdict_if_missing: NEEDS_EVIDENCE
```

Policy rules are deterministic. They may inspect metadata, paths, risk surfaces, and typed evidence states.

Policies cannot execute code, run shell commands, call the network, or use AI to authorize a verdict.

Evidence names in policies may use user-facing aliases such as `tests`, `ci`, `sarif`, `dependency`, `owner_approval`, or `github_actions_artifact`. The policy engine normalizes those aliases into canonical proof types before evaluating sufficiency.

`failed` or `conflicting` required evidence blocks the change. `missing`, `unavailable`, `stale`, `malformed`, or `insufficient` required evidence follows the rule's configured missing-proof verdict, usually `NEEDS_EVIDENCE`.
