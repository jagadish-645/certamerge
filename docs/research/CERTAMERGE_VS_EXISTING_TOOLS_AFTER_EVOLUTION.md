# CertaMerge Vs Existing Tools After Evolution

Date: 2026-06-27

## Source Baseline

This comparison uses current public documentation and product pages for the categories named in the evolution objective:

- GitHub rulesets and branch protection: [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets), [branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule), [required status checks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/troubleshooting-required-status-checks).
- GitHub Actions artifacts: [GitHub workflow artifacts](https://docs.github.com/en/actions/tutorials/store-and-share-data), [upload-artifact](https://github.com/actions/upload-artifact).
- GitHub code scanning and CodeQL: [GitHub code scanning](https://docs.github.com/code-security/code-scanning/automatically-scanning-your-code-for-vulnerabilities-and-errors/about-code-scanning), [CodeQL](https://docs.github.com/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql), [SARIF support](https://docs.github.com/en/code-security/concepts/code-scanning/sarif-files).
- Semgrep: [Semgrep Supply Chain setup](https://docs.semgrep.dev/semgrep-supply-chain/set-up-and-configure), [Semgrep CI integration](https://semgrep.dev/blog/2022/integrating-semgrep-with-ci), [Semgrep lockfile glossary](https://semgrep.dev/docs/semgrep-supply-chain/glossary).
- Snyk: [Snyk Open Source](https://docs.snyk.io/scan-fix-and-prevent/scan-with-snyk/snyk-open-source), [Snyk Container](https://docs.snyk.io/scan-fix-and-prevent/scan-with-snyk/snyk-container), [Snyk IaC](https://snyk.io/product/infrastructure-as-code-security/).
- Trivy: [Trivy](https://trivy.dev/), [Trivy GitHub](https://github.com/aquasecurity/trivy), [Trivy SBOM/container docs](https://trivy.dev/docs/latest/guide/target/container_image/).
- Gitleaks: [Gitleaks GitHub](https://github.com/gitleaks/gitleaks), [Gitleaks site](https://gitleaks.io/).
- SLSA, in-toto, Sigstore/Cosign, OPA, CycloneDX: [SLSA provenance](https://slsa.dev/spec/v1.0/provenance), [SLSA spec](https://slsa.dev/spec/v1.0/), [in-toto](https://in-toto.io/), [in-toto GitHub](https://github.com/in-toto/in-toto), [Cosign signing](https://docs.sigstore.dev/cosign/signing/signing_with_containers/), [Cosign verifying](https://docs.sigstore.dev/cosign/verifying/verify/), [OPA docs](https://openpolicyagent.org/docs), [CycloneDX](https://cyclonedx.org/), [CycloneDX overview](https://cyclonedx.org/specification/overview/).
- AI code reviewers: [GitHub Copilot code review](https://docs.github.com/copilot/using-github-copilot/code-review/using-copilot-code-review), [Copilot code review concept](https://docs.github.com/en/copilot/concepts/agents/code-review), [CodeRabbit PR review docs](https://docs.coderabbit.ai/overview/pull-request-review).

## 1. What Existing Tools Already Solve

GitHub rulesets, branch protection, and required status checks already solve repository-level merge constraints. They can require reviews, status checks, branch naming patterns, signed commits, deployment checks, and bypass controls.

GitHub Actions artifacts already solve workflow artifact upload and retrieval. They are useful transport for CARs, scanner outputs, test reports, SBOMs, and other proof inputs.

GitHub code scanning and CodeQL already solve vulnerability/error detection and alert display inside GitHub. GitHub also supports SARIF ingestion from third-party tools.

Semgrep, Snyk, Trivy, and Gitleaks already solve major scanning categories:

- static analysis;
- dependency and supply-chain scanning;
- container scanning;
- IaC scanning;
- secret scanning;
- SBOM generation or consumption in some modes.

SLSA, in-toto, Sigstore/Cosign, and CycloneDX already define important supply-chain standards and implementation patterns:

- provenance;
- supply-chain step metadata;
- signing and verification;
- SBOM structure;
- artifact transparency.

OPA already solves general policy decision-making over structured data. It is stronger than CertaMerge for broad domain-agnostic policy logic.

AI code reviewers already solve review assistance, PR summarization, line-level suggestions, and potential bug/performance/security feedback.

## 2. Where CertaMerge Is Redundant

CertaMerge should not build:

- branch protection;
- required status checks;
- PR review assignment;
- vulnerability scanning;
- secret scanning;
- SBOM generation;
- IaC vulnerability detection;
- SARIF alert display;
- general-purpose Rego/OPA replacement;
- artifact upload/download infrastructure;
- AI code review comments.

Those are better handled by GitHub, scanners, standards tooling, and AI review products.

If CertaMerge only says "tests must pass" or "scan must pass," it is redundant.

If CertaMerge only wraps GitHub required checks, it is redundant.

If CertaMerge only uploads a JSON file to GitHub Actions, it is redundant.

## 3. Where CertaMerge Adds Differentiated Value

CertaMerge adds value when it converts scattered proof into an authorization-grade decision record.

The differentiated unit is not a scan result or checklist. It is:

```text
Verdict.
Policy reason.
Missing proof.
Accountable next action.
Change Authorization Record.
```

After this evolution branch, concrete differentiation exists in these areas:

| Area | Existing Tools | CertaMerge Addition |
|---|---|---|
| GitHub rules/status checks | Can require checks and reviews. | Explains which proof is missing, stale, malformed, failed, conflicting, or insufficient. |
| PR templates | Can ask humans to fill checklists. | Derives proof gaps from repo shape and policy, then records a verifier-checked CAR. |
| Code scanning | Finds code/security issues. | Treats scanner output as one evidence state among test, owner, policy, workflow, docs, IaC, and CAR proof. |
| GitHub Actions artifacts | Stores files. | Uses artifacts as proof inputs/outputs and verifies CAR integrity. |
| SLSA/in-toto/Cosign | Supply-chain provenance/signing standards. | Can consume or eventually emit compatible proof context around merge authorization. |
| OPA/Rego | General policy engine. | Productizes a software-change proof grammar, evidence taxonomy, repair missions, and CAR workflow. |
| AI code reviewers | Suggest code review findings/fixes. | Does not review code; determines whether required proof exists and records the decision. |

The strongest current open-source wedge:

```text
CertaMerge converts repo shape, native workflow metadata, policy requirements, evidence states, repair missions, and verifier-checked CAR integrity into a deterministic missing-proof decision for the evaluated change context.
```

## 4. What CertaMerge Must Never Become

CertaMerge must not become:

- a GitHub rules UI;
- a branch protection clone;
- a PR checklist generator;
- a scanner aggregator dashboard;
- an AI reviewer;
- a vulnerability scanner;
- an SBOM generator;
- an OPA competitor;
- a compliance PDF generator;
- a dashboard-first DevSecOps product.

The product becomes slop if the primary user value is "look at this dashboard" instead of "this change has or lacks required proof, and here is the verifiable CAR."

## 5. What CertaMerge Should Integrate With

CertaMerge should integrate with:

- GitHub rules/status checks as the enforcement surface;
- GitHub Actions artifacts as proof transport;
- CodeQL/SARIF as scanner evidence;
- Semgrep/Snyk/Trivy/Gitleaks as scanner evidence;
- CycloneDX/SPDX SBOMs as dependency evidence;
- SLSA provenance as build provenance evidence;
- in-toto attestations as supply-chain step evidence;
- Sigstore/Cosign for future signing and verification;
- OPA/Rego only if CertaMerge needs an optional advanced policy backend later.

The integration rule:

```text
Consume their evidence. Do not copy their core product.
```

## 6. What CertaMerge Should Not Build Itself

CertaMerge should not build:

- a custom SAST engine;
- a custom SCA engine;
- a custom secret scanner;
- a custom Terraform vulnerability scanner;
- a custom SBOM format;
- a custom general attestation standard;
- a custom artifact hosting system;
- a custom AI review system;
- a custom universal policy language before the current DSL proves insufficient.

The product should invest in:

- evidence normalization;
- evidence state taxonomy;
- repo-adaptive policy suggestions;
- repair mission generation;
- change-bound CARs;
- offline verification;
- signed proof/attestation later;
- wrapper-kill validation fixtures;
- enterprise proof governance only after the open-source spine holds.

## 7. Final Differentiation Verdict

CertaMerge is not ready to claim production-grade security, compliance, or enterprise governance.

CertaMerge can now honestly claim a narrower open-source differentiation:

```text
CertaMerge converts scattered evidence from CI, scanners, repo metadata, policy, approval, and workflow context into a deterministic missing-proof decision and verifier-checked CAR for the evaluated change.
```

That is different from GitHub rules, PR templates, scanners, artifact upload, and AI code review.

The differentiation remains conditional:

- it must become more PR-diff-aware;
- it must eventually support signed CARs;
- it must keep integrating with scanners rather than imitating them;
- it must prove continued value on real repositories outside local fixtures.

Current verdict:

```text
DIFFERENTIATED OPEN-SOURCE WEDGE VALIDATED FOR ALPHA - NOT YET PRODUCTION ENTERPRISE CLAIMS
```

