# CertaMerge Evolutionary Product Hardening Report

## 1. Executive Verdict

CertaMerge open source now passes the first wrapper-kill test.

It is not production enterprise governance. It is not a compliance certification product. It is not a scanner, GitHub rules wrapper, dashboard, or AI reviewer.

It is now a credible open-source ProofOps wedge:

```text
Recover proof gaps.
Suggest starter policy.
Gate the evaluated context.
Record a change-bound CAR.
Verify the CAR locally.
```

## 2. Did Open Source Prove It Is More Than A Wrapper/Template?

Yes, for alpha scope.

CertaMerge now produced repo-specific proof gaps, starter policies, repair missions, and verifier-checked CARs across six different local repo archetypes.

The strongest evidence is that Terraform/IaC, docs-heavy, GitHub Action, Python library, Node/TypeScript app, and monorepo fixtures produced different proof expectations instead of a generic checklist.

## 3. Wrapper-Kill Test Result

Result:

```text
CERTAMERGE IS MORE THAN A TEMPLATE
```

Source:

```text
docs/research/WRAPPER_KILL_VALIDATION_RESULTS.md
```

## 4. Repo Archetypes Tested

Tested local fixtures:

- `samples/repos/archetypes/python-library/`
- `samples/repos/archetypes/node-typescript-app/`
- `samples/repos/archetypes/github-action-repo/`
- `samples/repos/archetypes/terraform-iac-repo/`
- `samples/repos/archetypes/monorepo-app/`
- `samples/repos/archetypes/docs-heavy-repo/`

All six completed:

- Recover;
- Recover with suggested policy;
- `suggest-policy`;
- Gate;
- `verify-car`;
- `explain-car`.

## 5. Open-Source Improvements Made

Implemented:

- repo-adaptive Recover profile;
- six realistic archetype fixtures;
- deterministic starter policy suggestion;
- expanded risk-surface detection;
- expanded evidence-source detection;
- explicit evidence states including unavailable and insufficient;
- change-bound CAR metadata;
- policy source hash binding;
- evidence artifact hash binding;
- verifier checks for policy/evidence mutation;
- GitHub Actions context recording;
- workflow-native GitHub Action summary;
- public sample CAR path sanitization;
- professional hardening scans and docs.

## 6. CertaMerge Self-Dogfood Result

Recover on the CertaMerge open-source root:

```text
Verdict: NEEDS_EVIDENCE
Repo profile: python-library
Missing proof: sarif_scan
```

Gate on the CertaMerge open-source root:

```text
Verdict: OBSERVE_ONLY_WOULD_ALLOW
Policy reason: All matched policy requirements are satisfied.
CAR verification: valid
```

CAR:

```text
.tmp/open-source-evolution.car.json
```

## 7. GitHub Action Result

The composite action now writes a structured proof summary from the generated CAR.

Summary includes:

- verdict;
- policy reason;
- matched rules;
- evidence states;
- missing proof;
- accountable next action;
- CAR artifact;
- verification command.

Live GitHub Actions validation has run on draft PR #4. The public `test` and `certamerge-proof` checks passed.

## 8. Change-Bound CAR Improvements

CARs now include:

- repo path;
- repo name;
- branch when available;
- current commit SHA when available;
- GitHub PR/run metadata when available;
- policy source path and file hash;
- evidence artifact hashes when files are resolvable;
- CertaMerge evaluator version;
- generated timestamp;
- replay change binding.

Verifier now detects:

- CAR content tampering;
- policy file mutation after CAR generation;
- evidence artifact mutation after CAR generation.

## 9. Evidence Ingestion Improvements

Evidence ingestion now supports:

- metadata evidence files under `.certamerge/evidence/`;
- native repo/workflow signals;
- SARIF files;
- dependency lockfiles;
- SBOM references;
- SECURITY/CODEOWNERS/LICENSE/templates;
- GitHub Action metadata;
- Terraform file/validation/plan references;
- docs build and link/safe-language references.

Supported evidence states:

```text
present
missing
unavailable
stale
malformed
failed
negative
insufficient
conflicting
```

## 10. Starter Policy Suggestion Result

Implemented commands:

```powershell
python -m certamerge suggest-policy <repo>
python -m certamerge suggest-policy <repo> --output .tmp/starter.certamerge.yml
python -m certamerge recover <repo> --suggest-policy
```

Result:

```text
6 of 6 archetypes received repo-specific starter policies.
```

## 11. Comparison Against Existing Tools

Source:

```text
docs/research/CERTAMERGE_VS_EXISTING_TOOLS_AFTER_EVOLUTION.md
```

Final differentiation:

```text
CertaMerge converts scattered evidence from CI, scanners, repo metadata, policy, approval, and workflow context into a deterministic missing-proof decision and verifier-checked CAR for the evaluated change.
```

## 12. Security/Privacy/Compliance Hardening

Hardening performed:

- no local path leakage in public product files after sample CAR cleanup;
- no secret-looking values found in public docs/templates/product files;
- unsafe security/compliance claims remain in non-claim or forbidden-claim contexts only;
- no source-code egress added;
- no LLM authority added;
- no dashboard/chatbot/scanner-wrapper feature added.

Remaining:

- no cryptographic CAR signing yet;
- no signed release/SBOM automation yet;
- no production compliance claims.

## 13. Test Counts And Commands

Commands run:

```powershell
python -m pip install -e .
python -m certamerge --help
python -m certamerge recover .
python -m certamerge gate --repo . --policy .certamerge.yml --output .tmp/open-source-evolution.car.json
python -m certamerge verify-car .tmp/open-source-evolution.car.json
python -m certamerge explain-car .tmp/open-source-evolution.car.json
python -m pytest -q
python -m pytest --collect-only -q
python -m compileall community
python -m build
```

Results:

```text
pytest: 246 passed
collect-only: 246 tests collected
compileall: passed
build: built certamerge-0.1.0.tar.gz and certamerge-0.1.0-py3-none-any.whl
```

Generated build/cache outputs were cleaned after verification.

## 14. Open-Source PR Link

Draft PR:

```text
https://github.com/jagadish-645/certamerge/pull/4
```

Current branch:

```text
evolution/repo-adaptive-proof-engine
```

Target PR title:

```text
evolution: make CertaMerge repo-adaptive beyond self-dogfood
```

## 15. Enterprise Gap Analysis

Enterprise work is intentionally not included in this public open-source branch.

Current cross-product state:

```text
Open-source wrapper-kill validation survived, and enterprise pilot-spine work has moved to the separate private enterprise repo.
```

The public repo should not carry private enterprise runtime details. This public report only records the open-source wedge and the handoff boundary.

## 16. Enterprise Improvements Made, If Any

None in this open-source evolution branch.

This branch intentionally avoids private enterprise product changes. Enterprise pilot-spine improvements are documented in the private enterprise repo.

## 17. Enterprise Pilot Readiness Verdict

Not evaluated inside this public branch.

Current cross-product enterprise status from the private enterprise run:

```text
CERTAMERGE ENTERPRISE STILL ALPHA — PILOT PREP ONLY
```

## 18. Remaining Limitations

- Gate still evaluates repo snapshots, not true PR diffs.
- Community CARs are hash-bound and change-bound, but not cryptographically signed.
- JUnit XML parsing is not implemented.
- Terraform plan JSON summarization is not implemented.
- SBOM content parsing is not implemented.
- Scanner adapter depth is limited.
- Live GitHub Actions validation must run after push.
- Real external repository validation remains future work.

## 19. What Must Be Built Next

Next open-source work:

- PR-diff-aware change context;
- clearer test-source versus test-result language;
- SARIF/JUnit/SBOM/Terraform parser depth;
- signed CAR design and implementation;
- live GitHub Actions validation after PR push;
- more real-world repo validation with no external spam.

Next enterprise work:

- run the private enterprise pilot spine against real 10-50 PR/CAR history;
- validate policy inheritance and owner mapping with design-partner data;
- harden signed CAR/replay/key-management model;
- define production RBAC/SSO and customer-controlled retention;
- write procurement/security packet after real pilot evidence exists;
- avoid production enterprise claims until security, deployment, and support gates pass.

## 20. What Must Not Be Built Yet

Do not build yet:

- dashboard-first admin UI;
- chatbot interface;
- AI authorization;
- custom vulnerability scanner;
- hosted SaaS dependency;
- Kubernetes-heavy enterprise deployment;
- compliance certification claims;
- enterprise feature sprawl before pilot workflow proves value.

## 21. Honest Acquisition-Grade Potential Assessment

CertaMerge is more credible after this branch because it now has a concrete wedge:

```text
repo-adaptive proof gap discovery + starter policy + change-bound CAR + local verification
```

That can become valuable if it keeps strengthening proof integrity, replayability, enterprise evidence governance, and self-hosted trust.

It is not yet acquisition-grade. Acquisition-grade potential depends on:

- real adoption;
- repeatable proof value on real repos;
- signed/replayable CARs;
- enterprise multi-repo governance;
- defensible policy/evidence packs;
- credible security posture;
- clean open-core boundary.

## 22. Kill/Pivot Criteria That Remain

Kill or pivot if:

- real repos produce generic proof gaps;
- users cannot understand or act on missing proof;
- CertaMerge becomes a wrapper around required checks;
- CAR verification does not matter to users;
- scanner vendors or GitHub trivially absorb the useful behavior;
- enterprise buyers only want dashboards or reports;
- signed/replayable proof cannot be made trustworthy.

CERTAMERGE OPEN-SOURCE EVOLUTION READY — PRODUCT IS MORE THAN A TEMPLATE
