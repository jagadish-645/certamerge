# CertaMerge Community Alpha Readiness Report

## Verdict

Community local alpha is ready for the next build phase: enterprise implementation may begin after this report while the open-source spine remains the trust foundation.

Public launch is not allowed yet. GitHub Action live-run validation, release packaging, signed distribution, and broader security hardening still need later release gates.

## What Works

| Capability | Status | Evidence |
|---|---|---|
| Tech-stack ADR | Works | `docs/adr/ADR-0001-tech-stack.md` |
| Phase 0 specs | Works | `specs/car`, `specs/evidence`, `specs/policy`, `specs/verdict`, `specs/repair-mission`, `specs/open-core` |
| Python package | Works | `python -m pip install -e .` succeeded |
| CLI module route | Works | `python -m certamerge --help` lists `verify-car`, `explain-car`, `recover`, `gate` |
| CAR verifier | Works | All five sample CARs validate |
| CAR explanation | Works | `python -m certamerge explain-car samples/cars/allow.example.json` |
| Local Recover | Works | `python -m certamerge recover samples/repos/no-ci-vibe-repo` emits `NEEDS_EVIDENCE` with missing proof and next action |
| Proof-only Gate | Works | `python -m certamerge gate --repo samples/repos/payment-change-with-tests --policy samples/policies/payment.certamerge.yml --output samples/cars/local-demo.json` emits `ALLOW` and valid CAR |
| Basic policy engine | Works | YAML policies parse safely and evaluate path/evidence rules deterministically |
| Basic evidence adapters | Works | CI config, test script, SARIF reference, dependency reference, owner approval reference, GitHub Actions reference, lint reference states are normalized |
| Evidence state semantics | Works | `present`, `missing`, `unavailable`, `stale`, `malformed`, `failed`, `negative`, `insufficient`, and `conflicting` stay distinct |
| Repair missions | Works | Missing proof creates finite repair missions with acceptance criteria and re-run instruction |
| GitHub Action wrapper | Created | `community/github-action/action.yml` |
| Community docs | Created | `docs/community/*` and `README.md` |
| Trust docs | Created | `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, no-source-egress, AI boundary, compliance-safe language |
| Sample repos | Created | Four sample repos under `samples/repos` |
| Sample CARs | Created | Five sample CARs under `samples/cars` |

## What Does Not Work Yet

| Gap | Reason | Required next step |
|---|---|---|
| Live GitHub Action execution | No GitHub runner was invoked in this local build run. | Add action contract/static tests now or live-run validation in release hardening. |
| `certamerge` command on this PowerShell PATH | Editable install succeeded, but this shell does not resolve Python Scripts entry point from PATH. | Use `python -m certamerge` locally or add PATH/install docs before public release. |
| Signed CARs | v0 includes content hashes and integrity metadata, not signing keys. | Add artifact signing in later proof hardening. |
| Full JUnit/SBOM parsing | v0 detects references and states, with SARIF state handling for negative, failed, and malformed fixtures. | Add deeper parser coverage and fuzz tests. |
| Public release packaging | Local editable install only. | Add release packaging, checksums, SBOM, and signed artifacts later. |

## Commands Tested

```powershell
python -m pytest
python -m pip install -e .
python -m certamerge --help
python -m certamerge recover samples/repos/no-ci-vibe-repo
python -m certamerge gate --repo samples/repos/payment-change-with-tests --policy samples/policies/payment.certamerge.yml --output samples/cars/local-demo.json
python -m certamerge verify-car samples/cars/local-demo.json
python -m certamerge verify-car samples/cars/allow.example.json
python -m certamerge verify-car samples/cars/block.example.json
python -m certamerge verify-car samples/cars/needs-evidence.example.json
python -m certamerge verify-car samples/cars/override-recorded.example.json
python -m certamerge verify-car samples/cars/repair-required.example.json
```

## Test Results

```text
100 passed
```

Test coverage includes:

- Recover missing proof detection.
- Gate observe-mode would-block behavior.
- Gate allow behavior with payment proof.
- CAR verifier rejection of invalid `ALLOW` plus missing proof.
- Evidence-state handling for failed, stale, malformed, negative, insufficient, and conflicting proof.
- Sample evidence fixture contract for SARIF, owner approval, and explicit test-result evidence.
- Controlled-alpha contract coverage for evidence aliases, policy validation, risk detection, root policy, no-source-egress assumptions, GitHub Action metadata, and sample CARs.
- CAR integrity hash tamper rejection.
- CLI Recover and Gate commands.
- CLI verify and explain commands.
- Generated CAR validation.
- Enterprise alpha tests also pass in the same repository run, proving the paid-tier foundation still consumes the community spine cleanly.

## Examples Generated

Sample CARs:

- `samples/cars/allow.example.json`
- `samples/cars/needs-evidence.example.json`
- `samples/cars/block.example.json`
- `samples/cars/repair-required.example.json`
- `samples/cars/override-recorded.example.json`

Sample repos:

- `samples/repos/basic-node-app`
- `samples/repos/auth-change-missing-tests`
- `samples/repos/payment-change-with-tests`
- `samples/repos/no-ci-vibe-repo`

Sample policies:

- `samples/policies/basic.certamerge.yml`
- `samples/policies/auth.certamerge.yml`
- `samples/policies/payment.certamerge.yml`

Sample evidence and PR fixtures:

- `samples/evidence/sarif-negative.example.sarif`
- `samples/evidence/sarif-failed.example.sarif`
- `samples/evidence/sarif-malformed.example.sarif`
- `samples/evidence/owner-approval-stale.example.json`
- `samples/evidence/owner-approval-denied.example.json`
- `samples/evidence/test-result-failed.example.json`
- `samples/prs/auth-missing-proof.pr.json`
- `samples/prs/payment-allow.pr.json`

## No-Source-Egress Status

Community v0 runs locally. The implemented commands do not send source code, raw diffs, secrets, or evidence to a vendor service.

CARs contain metadata, evidence states, policy references, risk surfaces, repair missions, verdict traces, and integrity metadata.

Current limitations:

- The scanner does inspect local filenames and selected metadata files such as `package.json`.
- The sample repos contain sanitized source examples, but CertaMerge output does not emit raw source content.
- No telemetry exists in community v0.

## Compliance-Safe Claims

Allowed:

- CertaMerge provides machine-checkable change authorization evidence.
- CertaMerge may support review, audit, and change-control workflows.
- CertaMerge records missing proof and accountable next action.

Forbidden:

- CertaMerge makes code secure.
- CertaMerge certifies compliance.
- CertaMerge guarantees audit success.
- CertaMerge replaces scanners or AppSec review.

## Is Community Version Genuinely Useful?

Yes, for controlled local alpha.

A free/community user can:

1. install locally;
2. scan a repo for missing proof;
3. evaluate a repo against a simple policy;
4. generate a CAR;
5. verify and explain a CAR;
6. see finite repair missions instead of vague risk text.

This is not a full public release, but it is a real first proof spine rather than a toy demo.

## Anti-Slop Verdict

Pass.

- No dashboard-first value.
- No chatbot.
- No LLM final verdict.
- No scanner replacement.
- CAR is a durable JSON proof record.
- Missing proof and failed proof are distinct states.
- Repair missions exist.
- Verifier exists.
- Tests exist and pass.

## Handoff

Proceed to Phase 2 enterprise build with this community spine as the foundation.
