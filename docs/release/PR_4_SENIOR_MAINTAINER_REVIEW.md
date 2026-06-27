# PR #4 Senior Maintainer Review

Date: 2026-06-27

PR: https://github.com/jagadish-645/certamerge/pull/4

Branch: `evolution/repo-adaptive-proof-engine`

Local checkout: public product checkout

## Review Verdict

```text
PR #4 IS TECHNICALLY HEALTHY BUT NOT MERGE-READY UNTIL THE NEW PRODUCTION-SHAPED HARDENING PASS IS COMPLETE
```

PR #4 is the correct public integration target. It includes PR #3's self-dogfood work and adds meaningful repo-adaptive proof capability. It passes local tests, local build, local self-gate, and GitHub checks.

It should remain draft until the Phase 3 hardening requirements are finished, because the current objective requires more than "green tests":

- true PR-diff-aware proof v1;
- broader evidence adapter v1;
- CAR signing decision;
- release packaging and supply-chain hygiene;
- CI matrix/self-gate tightening;
- public docs/leakage/safe-language scan.

## GitHub Check Evidence

Current PR #4 status:

| Check | Status |
|---|---|
| `CertaMerge CI / test` | success |
| `CertaMerge Proof Gate / certamerge-proof` | success |

Mergeability:

```text
MERGEABLE / CLEAN
```

Draft state:

```text
Open draft
```

## Local Command Evidence

Commands run:

```powershell
python -m pip install -e .
python -m certamerge --help
python -m certamerge recover .
python -m certamerge recover . --suggest-policy
python -m certamerge suggest-policy . --output .tmp/self.suggested.certamerge.yml
python -m certamerge gate --repo . --policy .certamerge.yml --output .tmp/open-source-review.car.json
python -m certamerge verify-car .tmp/open-source-review.car.json
python -m certamerge explain-car .tmp/open-source-review.car.json
python -m pytest -q
python -m pytest --collect-only -q
python -m compileall community
python -m build
```

Results:

| Command | Result |
|---|---|
| Editable install | Passed |
| CLI help | Passed; commands are `recover`, `suggest-policy`, `gate`, `verify-car`, `explain-car` |
| `recover .` | Passed; verdict `NEEDS_EVIDENCE`, repo profile `python-library`, missing proof `sarif_scan` |
| `recover . --suggest-policy` | Passed; generated repo-adaptive suggested policy |
| `suggest-policy . --output .tmp/self.suggested.certamerge.yml` | Passed |
| `gate --repo . --policy .certamerge.yml` | Passed; verdict `OBSERVE_ONLY_WOULD_ALLOW` |
| `verify-car .tmp/open-source-review.car.json` | Passed; `valid: true` |
| `explain-car .tmp/open-source-review.car.json` | Passed; showed CAR id, verdict, policy hash, commit |
| `pytest -q` | Passed; `246 passed` |
| `pytest --collect-only -q` | Passed; `246 tests collected` |
| `compileall community` | Passed |
| `python -m build` | Passed; built wheel and sdist |

Generated build artifacts:

```text
dist/certamerge-0.1.0-py3-none-any.whl
dist/certamerge-0.1.0.tar.gz
```

These are ignored by Git, as expected.

## Architecture Clarity

What works:

- Public repo now has a clearer community-alpha boundary.
- CLI surface is intentionally small.
- Core grammar is visible: verdict, policy reason, missing proof, accountable next action, CAR.
- The PR avoids chatbot/dashboard/scanner-wrapper behavior.
- The project remains local-first with no telemetry or source-code egress by default.

Concern:

- The architecture has not yet fully crossed from repo-snapshot proof into true PR-diff proof. CARs bind current Git/GitHub context, but Gate still evaluates the repo snapshot rather than explicitly scoped changed files.

Required before merge:

- Implement or explicitly document a practical PR-diff-aware v1.

## Code Quality

What works:

- Code remains compact and understandable.
- CLI is Typer-based with clear command boundaries.
- Policy evaluation, evidence detection, CAR construction, and verification remain separated.
- CAR verification rejects invalid state contracts and tampered hashes.
- Evidence states are tested.

Concern:

- `gate` currently accepts only `--repo`, `--policy`, and `--output`.
- No CLI inputs yet for explicit changed files, base/head diff, or GitHub event changed-file extraction.
- Evidence adapter logic is pragmatic but still limited.

Required before merge:

- Add explicit PR/change context options or document exact scope if deferred.
- Expand parser coverage where feasible without turning CertaMerge into a scanner.

## CLI UX

What works:

- CLI help is short and readable.
- Recover and Gate outputs are concise.
- Output uses the desired grammar.
- Failure exits are covered for malformed CAR and invalid policy.

Concern:

- `gate` does not yet expose PR-diff flags such as `--changed-files`, `--base`, or `--head`.

Required before merge:

- Add changed-file inputs if practical in this pass.

## Error Handling

What works:

- Invalid policy raises a CLI error.
- Missing/malformed CAR returns nonzero.
- Verifier emits structured `valid`, `errors`, `warnings`, `car_id`, and `verdict`.
- Evidence parser classifies malformed SARIF as `malformed` instead of crashing.

Concern:

- The new parser surface required by this objective needs more malformed-input coverage for JUnit, CycloneDX/SBOM, Terraform plan, and Gitleaks-style JSON if implemented.

## Test Quality

What works:

- 246 tests passed locally.
- Tests cover:
  - evidence aliases;
  - repo profile detection;
  - risk surface detection;
  - policy validation;
  - deterministic path matching;
  - CAR state contract validation;
  - sample CAR verification;
  - no raw source/secret output;
  - GitHub Action contract;
  - repo-adaptive archetypes;
  - policy/evidence hash binding;
  - GitHub Actions change context;
  - public release contract checks.

Concern:

- Missing explicit changed-file tests requested by the objective:
  - explicit changed files;
  - git diff unavailable fallback;
  - GitHub event fallback;
  - docs-only change;
  - workflow change;
  - auth/source change;
  - dependency file change;
  - Terraform file change.

Required before merge:

- Add those tests with implementation or documented deferral.

## Evidence Semantics

What works:

- Evidence states are stable and tested:
  - `present`;
  - `missing`;
  - `unavailable`;
  - `stale`;
  - `malformed`;
  - `failed`;
  - `negative`;
  - `insufficient`;
  - `conflicting`.
- SARIF can be treated as `negative` when valid and empty.
- Test result metadata can become `present`, `failed`, `stale`, `unavailable`, `insufficient`, or `malformed`.
- Owner approval can become `present`, `failed`, `stale`, `unavailable`, `insufficient`, `malformed`, or `conflicting`.

Concern:

- JUnit XML is not yet parsed.
- CycloneDX SBOM metadata is not yet parsed beyond generic SBOM reference presence.
- Terraform plan JSON is not yet summarized.
- Gitleaks/secret scan JSON is not yet summarized.

Required before merge:

- Implement pragmatic v1 evidence adapters or create an explicit scoped deferral with tests and docs.

## Policy Suggestion Quality

What works:

- `recover --suggest-policy` generated a repo-adaptive policy for the CertaMerge repo as a Python library.
- Archetype tests validate Python, Node/TypeScript, GitHub Action, Terraform, monorepo, and docs-heavy repos.
- Docs-heavy repos avoid generic test noise.

Concern:

- Suggested policies are starter policies only and must remain clearly non-authoritative.

Required before merge:

- Keep README/docs explicit that suggested policy is an onboarding aid, not a production authorization policy.

## Change-Bound CAR Correctness

What works:

- CAR includes repository identity.
- CAR binds policy file hash.
- CAR binds evidence artifact hashes when evidence files are referenced.
- CAR records current commit, branch, GitHub context, run id, and PR number where available.
- Verifier rejects tampered CAR content, policy file mismatch, and evidence artifact hash mismatch.

Concern:

- Current CAR context does not yet record:
  - `change_context_mode`;
  - changed-file list;
  - explicit base/head diff mode;
  - GitHub PR event file discovery mode.

Required before merge:

- Add these fields if practical in Phase 3. If unavailable, the CAR must honestly say it used `repo_snapshot`.

## GitHub Action Summary Quality

What works:

- GitHub Action wrapper exists.
- Action emits CertaMerge summary language.
- Action uploads CAR artifact.
- Action is tested for required inputs, outputs, and summary text.
- PR #4's GitHub `certamerge-proof` check passed.

Concern:

- Action should pass PR changed-file context into Gate once the CLI supports it.

## Docs Accuracy

What works:

- README is aligned with the product grammar and safe claims.
- Community docs describe alpha limitations, CAR integrity, GitHub Action behavior, Recover, suggest-policy, and change-bound proof.
- Public repo boundary is explicit.

Concern:

- PR #2 has useful README sections that should be salvaged into the final docs polish pass where still accurate.
- New Phase 3 docs are missing:
  - `docs/community/pr-diff-aware-proof.md`;
  - `docs/community/evidence-adapters.md`;
  - `docs/community/car-signing.md`;
  - release reports for PR diff, evidence adapters, CAR signing, supply chain, CI, docs cleanliness, and final production readiness.

## Public/Private Boundary

What works:

- Public README says enterprise capabilities are outside the community package.
- Tests scan public templates for local paths and token-shaped strings.
- No enterprise runtime entry point exists in public `pyproject.toml`.

Concern:

- A deeper repo-wide leakage scan still needs to be run after Phase 3 edits.

## Release Readiness

Current state:

```text
Not release-ready yet under the new objective.
```

Reason:

- Local tests/build pass.
- GitHub checks pass.
- Self-gate CAR verifies.
- But the new objective requires additional hardening artifacts and PR resolution before final release readiness can be claimed.

## What Passed

- Editable install.
- CLI smoke.
- Recover on the repo itself.
- Suggested policy generation.
- Self-gate CAR generation.
- CAR verification and explanation.
- 246 tests.
- Test collection.
- Compileall.
- Package build.
- GitHub checks.

## What Failed

No executed command failed during this review.

## What Was Fixed

This review did not modify product code. It created the maintainer review report and identified the required hardening work.

## Deferred Or Still Required

- PR-diff-aware Gate v1.
- Evidence adapters v1 for JUnit, SARIF, CycloneDX/SBOM, Terraform plan, and secret scan JSON where feasible.
- CAR signing v0 decision or implementation.
- Supply-chain/release packaging report.
- CI matrix and self-gate tightening.
- Public docs/leakage/safe-language scan.
- Final production-readiness report.
- PR #2/#3 closure after PR #4 absorbs useful work and passes final gates.

## Final Merge Recommendation

```text
HOLD PR #4 AS DRAFT — CONTINUE HARDENING, THEN MERGE ONLY AFTER FINAL OPEN-SOURCE GATE PASSES
```
