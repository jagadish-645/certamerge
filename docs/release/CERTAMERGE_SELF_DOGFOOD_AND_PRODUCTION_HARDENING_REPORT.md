# CertaMerge Self-Dogfood And Production Hardening Report

## 1. Executive Verdict

CertaMerge now uses CertaMerge on its own public alpha repository through a repo-local observe-mode policy, metadata evidence files, a pull-request proof workflow, verifier-checked CAR generation, and release documentation.

This is a real dogfood step. It does not make the community alpha production-authoritative, but it proves the public repository can speak the same product grammar it asks users to trust:

```text
Verdict.
Policy reason.
Missing proof.
Accountable next action.
Change Authorization Record.
```

## 2. Branch And Pull Request

- Branch: `dogfood/self-proofing-hardening`
- Draft PR: https://github.com/jagadish-645/certamerge/pull/3
- PR title: `dogfood: use CertaMerge to govern its own public alpha repo`
- Base branch: `main`
- Review stance: draft until live GitHub Action evidence is inspected

## 3. Scope

This branch hardens the public open-source repository only. It changes community alpha policy, evidence detection, GitHub workflow proof, issue/PR templates, CLI verifier error handling, public docs, and release reports.

It does not add enterprise runtime services, hosted services, SaaS, dashboards, admin UI, deployment gates, ProofGraph services, or closed-source features.

## 4. PR 2 Inspection

PR #2, `docs: professionalize public README`, remains separate and draft. It changes only `README.md` and its latest CI run failed `16` release-candidate contract tests because the rewrite removed tested public README phrases and repository-boundary wording.

The dogfood branch records that finding in `docs/release/PR_2_REVIEW_AND_NEXT_ACTION_REPORT.md` and does not depend on PR #2.

## 5. Self-Dogfood Policy

The branch replaces the narrow root policy with `.certamerge.yml` that governs:

- CLI and verifier code;
- CAR, verifier, and schema files;
- GitHub Action and workflow files;
- community tests;
- specs;
- samples;
- public docs;
- packaging and license files.

The policy is observe mode by default. It can show `OBSERVE_ONLY_WOULD_BLOCK` without breaking contributor flow.

## 6. Evidence Model Hardening

The evidence detector now recognizes metadata proof files for:

- dependency review evidence;
- CAR verification;
- no-source-egress posture;
- risk surface classification;
- workflow validation;
- action contract validation;
- schema validation;
- compliance-safe language;
- no-secret-leakage review;
- link validation.

These evidence types are pinned by tests so future edits cannot silently weaken the policy vocabulary.

## 7. Metadata Evidence Files

The branch adds `.certamerge/evidence/` files for the self-dogfood run. They are intentionally metadata-only. They do not carry source code, raw diffs, customer data, private keys, tokens, or production secrets.

The files exist to let CertaMerge decide whether required proof is present, not to replace tests or external attestations.

## 8. GitHub Proof Gate

The new workflow `.github/workflows/certamerge-proof-gate.yml` runs CertaMerge on pull requests. It uses the repository-local composite action, evaluates `.certamerge.yml`, writes `.tmp/certamerge-pr.car.json`, verifies the CAR, and uploads `certamerge-pr-car`.

Local static tests validate the workflow contract. Live GitHub proof is created by PR #3 after the workflow runs on GitHub infrastructure.

## 9. CLI And Verifier Hardening

The verifier path now handles missing CAR files with a clear user-facing error instead of an exception-shaped failure. Tests assert that `verify-car` and `explain-car` return nonzero and explain that the CAR file could not be read.

This matters because proof workflows must fail as useful next actions, not noisy traces.

## 10. Security And Privacy Hardening

The branch keeps the community alpha local and metadata-oriented. CertaMerge community commands do not require a hosted service, LLM API, telemetry, or source-code egress by default.

The branch also adds user-facing safety language to templates and docs, including instructions not to paste secrets, private keys, raw proprietary source, raw restricted diffs, customer production data, or credentials into public issues.

## 11. Compliance-Safe Language

The branch keeps claims bounded. It says CertaMerge may support review, audit, and change-control evidence. It does not claim that community alpha makes code secure, guarantees production safety, certifies compliance, replaces scanners, replaces AppSec review, or cryptographically signs CARs.

The language scan report is stored at `docs/release/COMPLIANCE_SAFE_LANGUAGE_SCAN.md`.

## 12. Documentation And Templates

The branch adds or strengthens:

- PR template proof fields;
- issue templates for bugs, alpha feedback, proof gaps, and evidence adapter requests;
- community feedback docs;
- self-dogfooding docs;
- GitHub Action docs;
- quickstart notes for running CertaMerge on CertaMerge;
- release reports for proof runs, security/privacy, compliance language, PR #2 review, and fix log.

## 13. Value Comparison

The value comparison report explains that CertaMerge is not a replacement for GitHub branch protection, GitHub Actions artifacts, code scanning, Semgrep, Snyk, SLSA, or in-toto.

CertaMerge earns its place only at the proof-decision layer: policy reason, missing proof, accountable next action, and a verifier-checked CAR.

Report: `docs/research/CERTAMERGE_SELF_DOGFOOD_VALUE_COMPARISON.md`

## 14. Verification Evidence

Local verification performed for this branch:

```text
python -m pip install -e .
python -m certamerge --help
python -m certamerge recover .
python -m certamerge gate --repo . --policy .certamerge.yml --output .tmp\dogfood-pr.car.json
python -m certamerge verify-car .tmp\dogfood-pr.car.json
python -m certamerge explain-car .tmp\dogfood-pr.car.json
python -m pytest -q
python -m pytest --collect-only -q
python -m compileall community
python -m build
```

Observed local results:

- CertaMerge Gate: `OBSERVE_ONLY_WOULD_ALLOW`
- CAR verification: valid
- Full tests: `215 passed`
- Test collection: `215 tests collected`
- Compileall: passed
- Build: wheel and source distribution built successfully
- Enterprise checkout smoke: `7 passed`
- Residue scan: no local-path, tooling-residue, scaffold-marker, or token-looking strings in public tracked content

`python -m pip check` reports an unrelated machine-level `opencv-python` and `numpy` version conflict. CertaMerge does not depend on either package.

## 15. Remaining Limitations And Final Verdict

Remaining limitations:

- Community alpha CARs are content-hash checked but not cryptographically signed.
- The GitHub proof workflow is observe mode by default.
- PR #3 must stay draft until live GitHub Action evidence is reviewed.
- Enterprise ProofGraph, org-wide policy, deployment gates, separation of duties, and audit exports remain outside the public repository.
- The public alpha is not a compliance certification product.

```text
CERTAMERGE SELF-DOGFOODING READY FOR REVIEW
```
