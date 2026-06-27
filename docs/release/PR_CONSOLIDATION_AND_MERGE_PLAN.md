# PR Consolidation And Merge Plan

Date: 2026-06-27

Repository: `jagadish-645/certamerge`

Local checkout: public product checkout

## Purpose

This plan decides how to handle the currently open public PRs before the production-readiness pass continues. It prevents stale draft PR clutter, avoids merging failing work, and gives PR #4 a clear path to become the public release-ready alpha branch only after gates pass.

## Current Public PRs

| PR | Branch | State | Checks | Mergeability | Decision |
|---|---|---|---|---|---|
| #2 `docs: professionalize public README` | `docs/professional-readme` | Open draft | `test` failed | Mergeable, `UNSTABLE` | Do not merge. Salvage useful README language during PR #4 docs polish, then close as superseded. |
| #3 `dogfood: use CertaMerge to govern its own public alpha repo` | `dogfood/self-proofing-hardening` | Open draft | `test` success, `certamerge-proof` success | Mergeable, `CLEAN` | Close as superseded by PR #4 after confirming PR #4 passes final gates. |
| #4 `evolution: make CertaMerge repo-adaptive beyond self-dogfood` | `evolution/repo-adaptive-proof-engine` | Open draft | `test` success, `certamerge-proof` success | Mergeable, `CLEAN` | Treat as the main public evolution PR. Keep draft until deep review and hardening pass complete. |

## PR #2 Decision

Decision:

```text
close as superseded after PR #4 docs polish
```

Rationale:

- PR #2 changes only `README.md`.
- PR #2 currently has a failing `test` check.
- PR #2's README contains useful professional sections:
  - concise product tagline;
  - safe "what CertaMerge is not" language;
  - example policy;
  - CAR explanation;
  - GitHub Action example;
  - security/privacy posture;
  - contribution guidance.
- PR #4's current README is shorter and more aligned with the latest product grammar, but should absorb the strongest safe sections from PR #2 during the open-source docs polish phase.

Action:

1. Do not merge PR #2 as-is.
2. During Phase 3 docs polish, port useful README sections into PR #4 if they remain accurate.
3. After PR #4 passes final gates or is merged, close PR #2 with a professional superseded comment.

Suggested close comment:

```text
Closing as superseded by PR #4 / the repo-adaptive evolution PR. The useful README and public-positioning work is being consolidated into the release-ready public alpha branch, which also includes the self-dogfood proof gate and updated CertaMerge validation.
```

## PR #3 Decision

Decision:

```text
close as superseded by PR #4 after PR #4 passes gates
```

Rationale:

- PR #3 contains the self-dogfood baseline:
  - `.certamerge.yml`;
  - self-dogfood evidence files;
  - CertaMerge proof GitHub Action;
  - issue templates;
  - pull request template;
  - evidence/verifier hardening;
  - self-dogfood release reports.
- PR #4 includes PR #3's commits:
  - `d16f5f2 dogfood CertaMerge self-proofing gate`
  - `e3c8dc4 docs add self dogfood hardening report`
- PR #4 also adds repo-adaptive Recover, suggest-policy, change-bound CAR, expanded verifier behavior, archetype fixtures, and broader release reports.

Action:

1. Keep PR #3 open until PR #4 passes local and GitHub gates.
2. Confirm no unique PR #3 files are missing from PR #4.
3. Close PR #3 as superseded after PR #4 is ready or merged.

Suggested close comment:

```text
Closing as superseded by PR #4 / the repo-adaptive evolution PR, which includes the self-dogfood policy, CertaMerge proof gate, evidence files, templates, tests, docs, and release reports from this branch, plus the next repo-adaptive proof engine work.
```

## PR #4 Decision

Decision:

```text
main public evolution PR; keep draft until hardening and final gates pass
```

Current strengths:

- Mergeable and clean.
- `CertaMerge CI / test` passed.
- `CertaMerge Proof Gate / certamerge-proof` passed.
- Contains self-dogfood foundation from PR #3.
- Adds repo-adaptive Recover and starter policy suggestion.
- Adds change-bound CAR/verifier evolution.
- Adds community docs and archetype fixtures.

Current risks:

- Large change set touching code, docs, samples, workflows, and tests.
- Existing gate is green but not sufficient for the new production-readiness objective.
- Needs deeper maintainer review for:
  - true PR-diff awareness;
  - evidence adapter semantics;
  - CAR signing decision;
  - release packaging and supply-chain hygiene;
  - CI matrix and self-gate coverage;
  - public docs cleanliness and no leakage.

Required before merge:

```text
test check passes
certamerge-proof check passes
CertaMerge CAR artifact is inspectable or regenerable
README/docs render cleanly
no private leakage
no local-path leakage
no unsafe compliance claims
tests pass locally
build passes locally
CertaMerge self-gate CAR verifies locally
```

Merge recommendation at this phase:

```text
DO NOT MERGE YET — proceed to senior maintainer review and production-shaped hardening.
```

## Enterprise PR #1 Plan

Repository: private enterprise product repository

PR: #1 `evolution: strengthen enterprise ProofOps pilot spine`

Current state:

- Open draft.
- Mergeable and clean.
- No GitHub status checks configured.
- Local validation is therefore the authoritative gate until CI is added.

Decision:

```text
keep draft until enterprise local gates pass and production-path docs are hardened
```

Actions:

1. Fetch and merge/rebase against `origin/main` only if needed.
2. Run local enterprise validation:
   - editable install;
   - CLI help;
   - pytest;
   - compileall;
   - enterprise store verification;
   - pilot packet generation;
   - support bundle/audit export checks where available.
3. Create `docs/release/ENTERPRISE_PR_1_MERGEABILITY_REPAIR_REPORT.md`.
4. Do not claim enterprise production readiness.

## Consolidation Verdict

```text
PR CONSOLIDATION PLAN READY — PR #4 IS THE PUBLIC INTEGRATION TARGET; PR #2 AND PR #3 SHOULD BE CLOSED ONLY AFTER PR #4 ABSORBS USEFUL WORK AND PASSES FINAL GATES
```
