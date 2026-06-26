# CertaMerge

**Proof-carrying change authorization for AI-era software delivery.**

CertaMerge is a local, deterministic ProofOps CLI for asking one release-critical question:

```text
Does this repo or change have enough evidence to move forward, and can we prove why later?
```

It is **not** an AI code reviewer, scanner, chatbot, compliance-certification tool, or dashboard. CertaMerge evaluates declared policy against available evidence, explains missing proof, and records the result in a **Change Authorization Record (CAR)**.

> AI agents and fast-moving teams create more software change. CertaMerge creates a proof record for whether that change has enough evidence to proceed.

---

## What CertaMerge does

CertaMerge Community Alpha provides a local proof spine for repos, pull requests, and CI experiments:

- detects proof gaps with `recover`;
- evaluates repo/change evidence against YAML policy with `gate`;
- keeps evidence states distinct: `present`, `missing`, `unavailable`, `stale`, `malformed`, `failed`, `negative`, `insufficient`, and `conflicting`;
- emits a verdict, policy reason, missing proof, accountable next action, and CAR;
- generates finite repair missions for missing proof;
- verifies and explains CARs offline;
- provides a composite GitHub Action wrapper for proof-only CI/PR experiments;
- runs locally with no telemetry, vendor callback, or source-code egress by default.

The core product grammar is intentionally small:

```text
Verdict.
Policy reason.
Missing proof.
Accountable next action.
Change Authorization Record.
```

---

## What CertaMerge is not

CertaMerge Community Alpha does **not**:

- decide whether code is secure;
- certify SOC 2, ISO 27001, SLSA, NIST SSDF, or any other framework;
- replace CodeQL, Semgrep, Trivy, Gitleaks, Snyk, human review, or AppSec review;
- cryptographically sign CARs yet;
- provide production-grade branch protection enforcement;
- include SSO, RBAC, admin UI, hosted SaaS, or enterprise deployment automation;
- send source code, raw diffs, secrets, tokens, private keys, or credentials to a vendor service by default.

Use this alpha to inspect proof gaps, test policy ideas, generate CARs, and give feedback. Do not use it as an unattended production authorization system.

---

## Quickstart

From the repository root:

```powershell
python -m pip install -e .
python -m certamerge --help
python -m certamerge recover samples/repos/no-ci-vibe-repo
python -m certamerge gate --repo samples/repos/payment-change-with-tests --policy samples/policies/payment.certamerge.yml --output .tmp/payment.car.json
python -m certamerge verify-car .tmp/payment.car.json
python -m certamerge explain-car .tmp/payment.car.json
```

Expected `recover` shape:

```text
Verdict: NEEDS_EVIDENCE
Policy reason: Recover checks basic proof signals without claiming security correctness.
Missing proof: test_result, ci_status, owner_approval
Accountable next action: repo-owner - Review generated repair missions and rerun CertaMerge after evidence is present.
```

Expected `gate` shape on the payment sample:

```text
Verdict: ALLOW
Policy reason: All matched policy requirements are satisfied.
Missing proof: No missing proof required by current policy.
Accountable next action: repo-owner - Proceed with record.
CAR: .tmp/payment.car.json
```

Expected CAR verification shape:

```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "car_id": "car_payment-change-with-tests_...",
  "verdict": "ALLOW"
}
```

---

## Example policy

A minimal `.certamerge.yml` can require proof for sensitive paths:

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

In observe mode, CertaMerge can show what would be allowed, blocked, or missing evidence without becoming a hard merge gate.

---

## Change Authorization Records

A **CAR** is a machine-checkable JSON record that captures:

- change identity;
- repo/change metadata;
- matched policy rules;
- evidence states and references;
- risk surfaces;
- verdict trace;
- missing proof;
- repair missions;
- content-hash integrity metadata.

Community alpha supports SHA-256 content-hash integrity and verifier-side tamper detection. It does **not** yet provide cryptographic signing, signer identity, key rotation, revocation, or non-repudiation.

See:

- [CAR integrity](docs/community/car-integrity.md)
- [Alpha limitations](docs/community/alpha-limitations.md)

---

## GitHub Action

The community GitHub Action runs CertaMerge Gate in CI, writes a workflow summary, and uploads the generated CAR artifact.

```yaml
name: CertaMerge Proof Gate

on:
  pull_request:

permissions:
  contents: read

jobs:
  certamerge:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: jagadish-645/certamerge/community/github-action@main
        with:
          policy: .certamerge.yml
          repo: .
          output: certamerge-car.json
          artifact-name: certamerge-car
          fail-on-block: "false"
```

Default behavior is non-blocking. Set `fail-on-block: "true"` only after validating the policy and evidence behavior on your repo.

See [GitHub Action validation](docs/community/github-action-validation.md).

---

## Security and privacy posture

Community alpha is designed for local-first evaluation:

- no telemetry by default;
- no vendor callback by default;
- no LLM in the final authorization path;
- no source-code egress by default;
- deterministic policy evaluation for final verdicts;
- CARs should contain metadata, evidence states, hashes/references, policy trace, and verdict trace — not raw source code or secrets.

Do not include secrets, production credentials, private keys, proprietary raw source, raw diffs, or unredacted scanner payloads in issues, logs, sample CARs, policies, evidence files, or screenshots.

See:

- [Security policy](SECURITY.md)
- [No source egress](docs/community/no-source-egress.md)
- [Compliance-safe language](docs/community/compliance-safe-language.md)

---

## Compliance-safe use

CertaMerge may support review, audit, and change-control workflows by producing machine-checkable evidence records.

CertaMerge must **not** be represented as:

- making code secure;
- guaranteeing production safety;
- certifying compliance;
- replacing scanners or AppSec review;
- proving a change is safe;
- providing cryptographically signed authorization records in community alpha.

A safer way to describe the project:

```text
CertaMerge helps teams identify missing proof before software changes move forward and records the decision in a Change Authorization Record.
```

---

## Repository boundary

This public repository contains the community alpha surface:

- local CLI;
- CAR verifier;
- Recover;
- proof-only Gate;
- basic policy examples;
- sample repos, policies, evidence, and CARs;
- specs;
- tests;
- composite GitHub Action wrapper;
- community documentation.

Advanced organization-wide capabilities — policy administration, segregation of duties, observe replay, ProofGraph memory, audit export, proprietary proof packs, self-hosted governance, support, and enterprise deployment hardening — are outside this public package until explicitly released under a clear open-core boundary.

---

## Documentation

- [Community quickstart](docs/community/quickstart.md)
- [Alpha limitations](docs/community/alpha-limitations.md)
- [CAR integrity](docs/community/car-integrity.md)
- [No source egress](docs/community/no-source-egress.md)
- [GitHub Action validation](docs/community/github-action-validation.md)
- [5-minute demo](docs/demo/5_MINUTE_PUBLIC_ALPHA_DEMO.md)
- [Security policy](SECURITY.md)

---

## Contributing

This project is in community alpha. High-signal feedback is more valuable than feature requests.

Useful contributions include:

- proof-gap examples from real repos;
- evidence adapter requests;
- policy examples;
- parser edge cases;
- CAR verification failures;
- documentation corrections;
- GitHub Action feedback.

Before opening an issue, remove secrets, raw proprietary source, private diffs, credentials, and unredacted scanner payloads.

---

## License

CertaMerge Community is released under the repository license. See [LICENSE](LICENSE).
