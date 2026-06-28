# CertaMerge

CertaMerge is an open-source ProofOps CLI for software changes.

It answers one release question:

```text
Does this change have enough proof to move forward, and can we verify that decision later?
```

GitHub rules decide whether checks are required.
Scanners find issues.
CertaMerge records whether the proof required for a change is present, missing, unavailable, stale, failed, malformed, conflicting, or insufficient - then writes a Change Authorization Record.

It is not an AI code reviewer, scanner, chatbot, dashboard, or compliance certification tool. It evaluates evidence and policy, then records a deterministic proof decision.

## The First 30 Seconds

| Question | Answer |
|---|---|
| What is CertaMerge? | A local ProofOps CLI and proof-carrying authorization layer for software changes. Community alpha runs as a CLI and GitHub Action wrapper. |
| Why does it exist? | Fast-moving human and AI-authored code needs a durable proof trail before teams trust it near production. |
| What problem does it solve? | It reduces manual evidence chasing by showing verdict, policy reason, missing proof, accountable next action, and CAR. |
| What is a CAR? | A Change Authorization Record: a JSON proof record containing change identity, evidence states, policy trace, verdict, repair missions, and integrity metadata. |
| Different from AI code review? | CertaMerge does not ask an LLM if code is safe. Final verdicts are deterministic and policy-based. |
| Different from scanners? | Scanners produce findings. CertaMerge consumes proof signals and decides whether required evidence is sufficient. |
| Install? | `python -m pip install -e .` from this repository. |
| Local Recover? | `python -m certamerge recover samples/repos/no-ci-vibe-repo` |
| Proof-only Gate? | `python -m certamerge gate --repo samples/repos/payment-change-with-tests --policy samples/policies/payment.certamerge.yml --output .tmp/payment.car.json` |
| Verify a CAR? | `python -m certamerge verify-car .tmp/payment.car.json` |
| Output shape? | Verdict, policy reason, missing proof, accountable next action, CAR. |
| Community/open source? | CLI, CAR spec/verifier, Recover, proof-only Gate, basic policies, evidence states, repair missions, GitHub Action wrapper, samples, docs. |
| Enterprise? | Not included in this public community alpha. Multi-repo ProofOps governance, SoD, observe replay, ProofGraph memory, audit export, and self-hosted enterprise controls live outside this repo. |
| Non-claims? | CertaMerge does not make code secure, certify compliance, replace scanners, or prove a change is safe. |
| Alpha limits? | Local/community alpha only; CAR hash integrity exists, cryptographic signing and production deployment hardening are not implemented yet. |

## What CertaMerge does

CertaMerge turns repo and change evidence into a proof decision:

- detects missing proof with `recover`;
- suggests a starter policy from the repo shape;
- evaluates a repo or scoped change with `gate`;
- records verdict, policy reason, missing proof, accountable next action, and CAR;
- verifies and explains CARs offline;
- gives coding agents machine-readable JSON so they can repair missing proof and rerun the gate;
- runs locally by default without telemetry or source-code egress.

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

## Core workflow

1. Run Recover on a repo to see missing proof.
2. Generate or choose a policy.
3. Run Gate on the repo, changed files, or local Git diff.
4. Store the CAR artifact.
5. Verify the CAR before trusting or sharing it.
6. Repair missing proof and rerun.

The product grammar is always:

```text
Verdict.
Policy reason.
Missing proof.
Accountable next action.
Change Authorization Record.
```

## Example output

Recover on a repo with auth-like code and no CI proof:

```text
Verdict: NEEDS_EVIDENCE
Policy reason: Recover checks repo-adaptive proof signals without claiming security correctness.
Missing proof: test_result, ci_status, owner_approval
Accountable next action: repo-owner - Review generated repair missions and rerun CertaMerge after evidence is present.
```

Gate on the payment sample:

```text
Verdict: ALLOW
Policy reason: All matched policy requirements are satisfied.
Missing proof: No missing proof required by current policy.
Accountable next action: repo-owner - Proceed with record.
CAR: .tmp/payment.car.json
```

CAR verification:

```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "car_id": "car_payment-change-with-tests_...",
  "verdict": "ALLOW"
}
```

## GitHub Action

The community package includes a composite action at:

```text
community/github-action/action.yml
```

Minimal workflow:

```yaml
name: CertaMerge Proof Gate
on:
  pull_request:
jobs:
  certamerge:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./community/github-action
        with:
          policy: .certamerge.yml
          repo: .
          output: .tmp/certamerge-pr.car.json
          artifact-name: certamerge-pr-car
```

The action runs Gate, writes a workflow summary, and uploads the CAR artifact. It defaults to non-blocking proof behavior unless `fail-on-block` is enabled.

## Agent / JSON usage

Coding agents should use JSON output instead of scraping text:

```powershell
python -m certamerge recover . --json
python -m certamerge gate --repo . --policy .certamerge.yml --json --output .tmp/self.car.json
python -m certamerge explain-car .tmp/self.car.json --json
```

Agent loop:

1. Read `verdict`, `policy_reason`, `missing_proof`, `repair_missions`, and `accountable_next_action`.
2. Repair only the missing proof that CertaMerge names.
3. Rerun `recover` or `gate`.
4. Verify the CAR before reporting completion.

See [agent workflow](docs/community/agent-workflow.md).

## Change Authorization Records

A Change Authorization Record is the durable output of Gate. It includes:

- change identity and Git context;
- repository metadata;
- evidence states;
- risk surfaces;
- policy trace;
- verdict;
- missing proof;
- repair missions;
- accountable next action;
- integrity metadata.

Community alpha CARs are integrity-bound with verifier-checked SHA-256 content hashes. They are not cryptographically signed yet. Do not claim signer identity or non-repudiation for community alpha CARs.

## Evidence adapters

Community alpha detects proof signals from local metadata and evidence artifacts, including:

- test scripts and test result evidence;
- CI configuration presence;
- SARIF scanner evidence;
- SBOM and dependency references;
- Terraform plan evidence;
- secret scan evidence;
- owner approval evidence;
- CAR verification evidence.

Evidence states stay distinct: `present`, `missing`, `unavailable`, `stale`, `malformed`, `failed`, `negative`, `insufficient`, and `conflicting`.

## What CertaMerge is not

CertaMerge is not:

- an AI code reviewer;
- a chatbot;
- a scanner replacement;
- a GitHub ruleset clone;
- a branch protection wrapper;
- a compliance certificate generator;
- a dashboard-first product;
- a SaaS account requirement.

## Security and privacy posture

Community alpha is local-first:

- no telemetry is sent by default;
- source code, raw diffs, secrets, scanner payloads, CARs, and Repo Proof Snapshots are not sent to a vendor service by default;
- CARs use metadata, hashes, paths, evidence states, policy IDs, and verdict traces;
- final authorization does not depend on an LLM;
- public docs avoid certification or production-readiness claims that the product does not implement.

See [no source egress](docs/community/no-source-egress.md), [AI boundary](docs/community/ai-boundary.md), and [security policy](SECURITY.md).

## Community alpha limitations

Community alpha is useful for local proof discovery and proof-only Gate workflows, but it is not a production enterprise deployment.

Known limits:

- CARs are not cryptographically signed yet;
- release archives are not signed yet;
- no hosted service is included;
- no SSO, RBAC, admin console, durable enterprise store, backup/restore, or production observability is included;
- GitHub Action behavior that depends on GitHub runners must be validated in GitHub Actions;
- compliance frameworks may be supported by evidence, but CertaMerge does not certify compliance.

## Enterprise boundary

This repository is the community alpha surface. It contains the local CLI, CAR verifier, proof-only Gate, Recover, basic policy examples, sample repositories, specs, tests, and a composite GitHub Action wrapper.

The public repository contains only community-safe assets and intentionally excludes advanced enterprise-only code and docs out of the community repository, including:

- enterprise runtime services;
- organization-wide policy governance;
- segregation of duties;
- observe-mode replay;
- ProofGraph memory;
- audit export;
- support bundle generation;
- internal strategy and agent-system material.

Advanced enterprise deployment and governance belong in the private enterprise product until they can be released with a clear open-core boundary. See the [public repository boundary](docs/community/repository-boundary.md).

## Contributing / feedback

Useful feedback is concrete:

- a repo shape Recover missed;
- an evidence type CertaMerge should detect;
- a CAR verification failure;
- a confusing proof gap;
- a GitHub Action issue;
- a README or quickstart command that does not run.

Start with:

- [Community quickstart](docs/community/quickstart.md)
- [5-minute demo](docs/demo/5_MINUTE_PUBLIC_ALPHA_DEMO.md)
- [Recover](docs/community/recover.md)
- [Suggest policy](docs/community/suggest-policy.md)
- [Evidence adapters](docs/community/evidence-adapters.md)
- [CAR integrity](docs/community/car-integrity.md)
- [CAR signing status](docs/community/car-signing.md)
- [GitHub Action](docs/community/github-action.md)
- [Feedback](docs/community/feedback.md)
