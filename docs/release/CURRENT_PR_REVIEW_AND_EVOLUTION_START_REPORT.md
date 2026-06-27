# Current PR Review And Evolution Start Report

## Purpose

This report records the required Phase 0 inspection before starting the repo-adaptive CertaMerge evolution branch.

The question for this next branch is not whether CertaMerge can dogfood itself. PR #3 already proved that in a controlled way. The harder question is whether CertaMerge can become useful on repositories that were not handcrafted for CertaMerge.

## Local Repository State

Open-source checkout:

```text
Repository: jagadish-645/certamerge
Local path: products/certamerge-open-source
Starting branch: dogfood/self-proofing-hardening
Evolution branch: evolution/repo-adaptive-proof-engine
Remote: origin https://github.com/jagadish-645/certamerge
```

The local product worktree had no tracked uncommitted changes before the evolution branch was created. Ignored `.tmp/` proof artifacts from the prior dogfood run remained local only.

GitHub CLI note: the installed `gh` version does not support `gh pr view --files`, so PR details were collected with `gh pr view --json files,comments,latestReviews,statusCheckRollup`.

## Open PR Summary

Open pull requests inspected:

| PR | Title | Branch | Draft | Check State | Decision |
|---|---|---|---|---|---|
| `#2` | `docs: professionalize public README` | `docs/professional-readme` | yes | `test` failed | Do not build on it. Salvage copy later only if it preserves tested contracts. |
| `#3` | `dogfood: use CertaMerge to govern its own public alpha repo` | `dogfood/self-proofing-hardening` | yes | `test` passed, `certamerge-proof` passed | Build on it. |

## PR #2 Review

PR #2 changes only `README.md`. It is still open and draft.

Current evidence:

```text
test: failed
run: 28226483907
changed files: README.md
reviews: none
comments: none
mergeability: MERGEABLE at Git object level
```

The failure remains valid. The README rewrite removes release-candidate wording that the public contract tests intentionally require, including the first-30-second sections:

- `What is CertaMerge?`
- `Why does it exist?`
- `What problem does it solve?`
- `What is a CAR?`
- `Different from AI code review?`
- `Different from scanners?`
- `Install?`
- `Local Recover?`
- `Proof-only Gate?`
- `Verify a CAR?`
- `Output shape?`
- `Community/open source?`
- `Enterprise?`
- `Non-claims?`
- `Alpha limits?`

The rewrite also removes the exact tested public repository boundary sentence: `This repository is the community alpha surface`.

### Salvage Assessment

PR #2 has useful writing moves:

- cleaner opening tagline;
- clearer "what CertaMerge is not" section;
- better CAR explanation;
- more polished GitHub Action example;
- better compliance-safe framing.

But those improvements are not safe to merge until they preserve the executable README contract and public alpha boundary. PR #2 should be updated or superseded by a later README polish PR that keeps the contract tests green.

### PR #2 Decision

Do not merge PR #2 as-is. Do not base the repo-adaptive evolution branch on it.

## PR #3 Review

PR #3 is the self-dogfood foundation branch. It is still open and draft.

Current evidence:

```text
test: passed
certamerge-proof: passed
changed files: self-policy, metadata evidence, GitHub proof workflow, docs, tests, verifier hardening
reviews: none
comments: none
mergeability: MERGEABLE at Git object level
```

The live `certamerge-proof` workflow passed. The uploaded `certamerge-pr-car` artifact was downloaded locally and verified:

```text
CAR file: .tmp/certamerge-pr-car-artifact/certamerge-pr.car.json
Verification: valid
CAR id: car_certamerge_5c471e3b5c
Verdict: OBSERVE_ONLY_WOULD_ALLOW
```

### What PR #3 Proves

PR #3 proves that CertaMerge can govern its own public alpha repository with:

- repo-local observe-mode policy;
- metadata evidence;
- deterministic policy evaluation;
- a GitHub Action proof gate;
- CAR artifact upload;
- offline CAR verification;
- proof-oriented PR documentation.

### What PR #3 Does Not Prove

PR #3 does not prove the product is more than a wrapper/template yet.

The self-dogfood policy and evidence are intentionally curated for the CertaMerge repository. That is valuable for dogfooding, but it is not enough to prove usefulness on arbitrary repositories.

Known PR #3 weaknesses to carry into this evolution branch:

- `.certamerge.yml` is handcrafted.
- `.certamerge/evidence/` proof files are manually curated.
- `recover` still needs stronger zero-config repo profiling.
- starter policies are not generated for unknown repos yet.
- CARs need more change-bound context and evidence-file hash verification.
- GitHub Action summaries can become more reviewer-useful.

### PR #3 Decision

Build on PR #3. Do not wait for it to merge because the evolution branch needs the dogfood policy, proof workflow, metadata evidence vocabulary, and tests as its foundation.

## Evolution Branch Start

The evolution branch is created from PR #3 head:

```text
evolution/repo-adaptive-proof-engine
```

This branch must prove whether CertaMerge becomes useful outside a handcrafted CertaMerge-ready repository.

## Initial Wrapper-Kill Hypothesis

Current honest state:

```text
CertaMerge is no longer only a README/template idea because PR #3 produces a live verified CAR for itself.
```

But the harder verdict remains unproven:

```text
CertaMerge may still be too template-like if it cannot profile unfamiliar repos, suggest useful policies, and produce change-bound CARs without handcrafted evidence.
```

## Required Next Work

The next work must focus on:

1. wrapper-kill test definition;
2. realistic repo archetype fixtures;
3. zero-config Recover improvements;
4. repo-specific starter policy suggestion;
5. change-bound CAR context and evidence integrity;
6. evidence ingestion beyond static `.certamerge/evidence/` files;
7. useful GitHub Action summary;
8. wrapper-kill validation across six archetypes.

## Phase 0 Verdict

```text
BUILD_ON_PR_3
```
