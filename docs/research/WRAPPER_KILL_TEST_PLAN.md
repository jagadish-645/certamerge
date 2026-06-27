# Wrapper-Kill Test Plan

## Purpose

This plan defines the test that decides whether CertaMerge is becoming a real repo-adaptive proof-decision layer or remains too close to a GitHub rules/template wrapper.

The test is intentionally skeptical:

```text
Is CertaMerge useful outside a handcrafted CertaMerge-ready repo?
```

## Product Claim Under Test

CertaMerge should normalize scattered repository, workflow, evidence, risk, and policy signals into:

```text
Verdict.
Policy reason.
Missing proof.
Accountable next action.
Change Authorization Record.
```

The product fails this test if it needs a perfect `.certamerge.yml` and hand-written evidence files before it can say anything useful.

## Non-Goals

This test does not evaluate:

- hosted SaaS behavior;
- enterprise ProofGraph behavior;
- dashboard UX;
- LLM-generated review;
- vulnerability detection quality;
- compliance certification;
- production branch-protection enforcement.

The open-source wedge is allowed to be alpha. It is not allowed to be fake-useful.

## Repo Archetypes

The validation uses six local fixture repositories:

| # | Archetype | Fixture Path | Why It Matters |
|---|---|---|---|
| 1 | Small Python library | `samples/repos/archetypes/python-library/` | Common OSS/library shape with package metadata, tests, CI, and missing dependency/security proof possibilities. |
| 2 | Node/TypeScript app | `samples/repos/archetypes/node-typescript-app/` | Common app shape with lockfiles, scripts, tests, and frontend/backend risk surfaces. |
| 3 | GitHub Action repository | `samples/repos/archetypes/github-action-repo/` | Tests whether CertaMerge understands action metadata and workflow risk instead of generic code-only policy. |
| 4 | Terraform/IaC repository | `samples/repos/archetypes/terraform-iac-repo/` | Tests infrastructure proof needs: validation, plan evidence, owner approval, and environment blast radius. |
| 5 | Monorepo-style app | `samples/repos/archetypes/monorepo-app/` | Tests multi-package/app detection and policy scoping by path. |
| 6 | Docs-heavy open-source repository | `samples/repos/archetypes/docs-heavy-repo/` | Tests docs-specific proof needs: link validation, docs build, spelling/lint proof, safe claims. |

## Required Commands Per Archetype

For each fixture, run:

```powershell
python -m certamerge recover samples/repos/archetypes/<repo>
python -m certamerge recover samples/repos/archetypes/<repo> --suggest-policy
python -m certamerge gate --repo samples/repos/archetypes/<repo> --policy <generated-or-sample-policy> --output .tmp/<repo>.car.json
python -m certamerge verify-car .tmp/<repo>.car.json
python -m certamerge explain-car .tmp/<repo>.car.json
```

If `suggest-policy` is implemented as a standalone command instead of a `recover` flag, substitute:

```powershell
python -m certamerge suggest-policy samples/repos/archetypes/<repo>
```

## Minimum Pass Criteria

CertaMerge passes the wrapper-kill test only if all minimum criteria are met:

1. Zero-config Recover produces useful proof gaps on at least 4 of 6 repo archetypes.
2. Starter policy suggestion produces reasonable repo-specific policy on at least 4 of 6 archetypes.
3. Change simulation or Gate produces sane missing-proof output on at least 4 of 6 archetypes.
4. At least 3 outputs are more useful than `run tests`.
5. CertaMerge clearly adds something beyond GitHub branch rules, required checks, PR templates, and scanner output.
6. CARs remain verifier-checkable after archetype Gate runs.
7. Outputs avoid raw source code, secrets, local machine paths, and false compliance/security claims.

## Failure Criteria

CertaMerge fails the wrapper-kill test if any of these are true:

1. It only works after handcrafted policy/evidence.
2. Outputs are generic checklists.
3. It duplicates GitHub rules or PR templates without adding proof normalization.
4. It cannot infer repo type or risk surfaces.
5. CAR is only a log file with no useful verification value.
6. Missing-proof output is obvious, noisy, or unactionable.
7. An LLM or non-deterministic process influences final verdicts.
8. Any command emits raw source code, raw diffs, secrets, local private paths, or unsupported compliance/security claims.

## Scoring Rubric

Each archetype receives up to 20 points:

| Dimension | Points | Evidence |
|---|---:|---|
| Repo profile detection | 4 | Correct repo type, ecosystem, CI/tests/lockfile/security/license indicators. |
| Proof gap quality | 4 | Gaps are specific, relevant, and not merely `run tests`. |
| Starter policy quality | 4 | Suggested policy is repo-specific and maps to real risk surfaces. |
| Gate/CAR usefulness | 4 | Gate produces meaningful verdict/missing proof and valid CAR. |
| Non-slop differentiation | 4 | Output adds value beyond GitHub rules/templates/scanner findings. |

Overall score:

- `>= 80/120`: pass if all minimum criteria also pass.
- `60-79/120`: partial wedge; fix required before enterprise work.
- `< 60/120`: product remains too template-like.

## Evidence To Record

For every archetype, record:

- repo type detected;
- ecosystem detected;
- CI presence;
- test presence;
- lockfile/SBOM/dependency proof;
- security policy presence;
- license presence;
- GitHub Action presence;
- IaC indicators;
- docs-heavy indicators;
- risk surfaces;
- missing proof;
- suggested policy rules;
- Gate verdict;
- CAR validity;
- repair missions;
- noise level;
- what was more useful than GitHub rules/templates;
- what was weak or redundant.

## Wrapper-Kill Final Verdicts

The validation report must end with exactly one of:

```text
CERTAMERGE IS MORE THAN A TEMPLATE
```

or

```text
CERTAMERGE IS STILL TOO TEMPLATE-LIKE — FIX REQUIRED
```

or

```text
CERTAMERGE OPEN-SOURCE WEDGE SHOULD PIVOT
```

## Anti-Slop Gate

Before counting a result as useful, ask:

1. Does it strengthen evidence collection, risk classification, deterministic policy, or proof verification?
2. Does it produce a concrete next action?
3. Does it distinguish missing, failed, malformed, stale, conflicting, unavailable, and insufficient evidence where possible?
4. Would a senior maintainer learn anything beyond what GitHub branch protection already says?
5. Can the decision be verified later?
6. Does it avoid chatbot, dashboard, scanner-wrapper, and AI-reviewer behavior?

If any answer is no, the archetype result cannot receive full points.

## Current Expected Risk

The initial hypothesis is that PR #3 made CertaMerge self-dogfooded but still too handcrafted. This branch must either fix that or honestly say the current open-source wedge is not strong enough yet.
