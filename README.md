# CertaMerge

CertaMerge is a local ProofOps tool for software changes. It answers one practical release question:

```text
Does this repo or change have enough evidence to move forward, and can we prove why later?
```

It is not an AI code reviewer, scanner, chatbot, or compliance certification tool. CertaMerge evaluates evidence and policy, then records the decision in a Change Authorization Record.

## The First 30 Seconds

| Question | Answer |
|---|---|
| What is CertaMerge? | A proof-carrying authorization layer for repos, PRs, and future deploys. Community alpha runs as a local CLI and GitHub Action wrapper. |
| Why does it exist? | AI-built and fast-moving code needs a durable proof trail before teams trust it in production. |
| What problem does it solve? | It reduces manual evidence chasing by showing verdict, policy reason, missing proof, owner action, and CAR. |
| What is a CAR? | A Change Authorization Record: a JSON proof record containing change identity, evidence states, policy trace, verdict, repair missions, and integrity metadata. |
| Different from AI code review? | CertaMerge does not ask an LLM if code is safe. Final verdicts are deterministic and policy-based. |
| Different from scanners? | Scanners produce findings. CertaMerge consumes evidence from tools/workflows and decides whether proof is sufficient. |
| Install? | `python -m pip install -e .` from this repository. |
| Local Recover? | `python -m certamerge recover samples/repos/no-ci-vibe-repo` |
| Proof-only Gate? | `python -m certamerge gate --repo samples/repos/payment-change-with-tests --policy samples/policies/payment.certamerge.yml --output .tmp/payment.car.json` |
| Verify a CAR? | `python -m certamerge verify-car .tmp/payment.car.json` |
| Output shape? | Verdict, policy reason, missing proof, accountable next action, CAR. |
| Community/open source? | CLI, CAR spec/verifier, Recover, proof-only Gate, basic policies, evidence states, repair missions, GitHub Action wrapper, samples, docs. |
| Enterprise? | Not included in this public community alpha. Advanced org policy, SoD, observe replay, ProofGraph memory, audit export, and self-hosted governance are outside the community package. |
| Non-claims? | CertaMerge does not make code secure, certify compliance, replace scanners, or guarantee production safety. |
| Alpha limits? | Local/community alpha only; CAR hash integrity exists, cryptographic signing and production deployment hardening are not implemented yet. |

## 5-Minute Quickstart

From the repository root:

```powershell
python -m pip install -e .
python -m certamerge --help
python -m certamerge recover samples/repos/no-ci-vibe-repo
python -m certamerge gate --repo samples/repos/payment-change-with-tests --policy samples/policies/payment.certamerge.yml --output .tmp/payment.car.json
python -m certamerge verify-car .tmp/payment.car.json
python -m certamerge explain-car .tmp/payment.car.json
```

Expected Recover shape:

```text
Verdict: NEEDS_EVIDENCE
Policy reason: Recover checks repo-adaptive proof signals without claiming security correctness.
Missing proof: test_result, ci_status, owner_approval
Accountable next action: repo-owner - Review generated repair missions and rerun CertaMerge after evidence is present.
```

Expected Gate shape on the payment sample:

```text
Verdict: ALLOW
Policy reason: All matched policy requirements are satisfied.
Missing proof: No missing proof required by current policy.
Accountable next action: repo-owner - Proceed with record.
CAR: .tmp/payment.car.json
```

Expected verification shape:

```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "car_id": "car_payment-change-with-tests_...",
  "verdict": "ALLOW"
}
```

## Product Grammar

Every useful CertaMerge surface must compress complexity into:

```text
Verdict.
Policy reason.
Missing proof.
Accountable next action.
Change Authorization Record.
```

That grammar is the product. Anything that cannot serve it is out of scope for the community release.

## What Community Alpha Does

- Finds missing proof in local repos with `recover`.
- Evaluates a repo against YAML policy with `gate`.
- Keeps evidence states distinct: `present`, `missing`, `unavailable`, `stale`, `malformed`, `failed`, `negative`, `insufficient`, and `conflicting`.
- Generates finite repair missions for missing proof.
- Emits CARs with schema checks and SHA-256 content-hash integrity.
- Verifies and explains CARs offline.
- Provides a composite GitHub Action wrapper that defaults to non-blocking proof behavior.
- Runs without telemetry, vendor callbacks, or source-code egress by default.

## What Community Alpha Does Not Do

- It does not cryptographically sign CARs yet.
- It does not replace CodeQL, Semgrep, Trivy, Gitleaks, Snyk, or human AppSec review.
- It does not certify SOC 2, ISO 27001, SLSA, NIST SSDF, or any other standard.
- It does not ship production enterprise deployment automation yet.
- It does not include SSO, RBAC, admin UI, hosted SaaS, or dashboard-first workflows.
- It does not publish raw source code, raw diffs, secrets, or tokens in CAR output by default.

## Repository Boundary

This repository is the community alpha surface. It contains the local CLI, CAR verifier, proof-only Gate, Recover, basic policy examples, sample repositories, specs, tests, and a composite GitHub Action wrapper.

Advanced organization-wide capabilities are intentionally outside this package until they can be evaluated, documented, and released with a clear open-core boundary.

See:

- [Community quickstart](docs/community/quickstart.md)
- [Alpha limitations](docs/community/alpha-limitations.md)
- [CAR integrity](docs/community/car-integrity.md)
- [CAR signing status](docs/community/car-signing.md)
- [PR-diff-aware proof](docs/community/pr-diff-aware-proof.md)
- [Evidence adapters](docs/community/evidence-adapters.md)
- [No source egress](docs/community/no-source-egress.md)
- [Self-dogfooding](docs/community/self-dogfooding.md)
- [5-minute demo](docs/demo/5_MINUTE_PUBLIC_ALPHA_DEMO.md)
- [GitHub Action validation](docs/community/github-action-validation.md)

## Example Policy

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
    reason: "Auth changes require test and owner approval proof."
```

In observe mode, CertaMerge records what would be allowed or blocked without becoming a hard merge gate.

## Safe Language

CertaMerge may say it provides machine-checkable evidence that can support review, audit, and change-control workflows.

CertaMerge must not say it makes code secure, guarantees compliance, replaces scanners, or proves a change is safe.
