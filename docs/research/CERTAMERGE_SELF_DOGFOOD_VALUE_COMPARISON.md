# CertaMerge Self-Dogfood Value Comparison

## Executive Verdict

CertaMerge is valuable only if it adds a workflow-native proof decision that existing tools do not already provide by themselves.

The self-dogfood branch passes that bar for public alpha review because it combines deterministic policy, typed evidence, missing-proof distinction, accountable next action, and a verifier-checked Change Authorization Record.

## What Existing Tools Already Solve

GitHub branch protection and required status checks can require reviews and passing checks before protected-branch merge. GitHub documents protected branches and required checks as mechanisms for enforcing repository workflow rules:

- GitHub protected branches: https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- GitHub status checks: https://docs.github.com/articles/about-status-checks

GitHub Actions artifacts can persist workflow outputs after a job completes, which is useful for storing a CAR artifact:

- GitHub workflow artifacts: https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts
- GitHub upload-artifact action: https://github.com/actions/upload-artifact

GitHub code scanning surfaces code issues and pull-request alerts:

- GitHub code scanning pull request triage: https://docs.github.com/en/code-security/how-tos/manage-security-alerts/manage-code-scanning-alerts/triage-alerts-in-pull-requests

Semgrep and Snyk already provide local and CI security/dependency scanning paths:

- Semgrep CLI reference: https://docs.semgrep.dev/cli-reference
- Semgrep local scans: https://docs.semgrep.dev/getting-started/cli
- Snyk CLI test: https://docs.snyk.io/developer-tools/snyk-cli/snyk-cli/commands/test

SLSA and in-toto already define serious supply-chain provenance and attestation concepts:

- SLSA: https://slsa.dev/
- SLSA build requirements: https://slsa.dev/spec/v1.2/build-requirements
- in-toto attestation framework: https://github.com/in-toto/attestation
- in-toto run metadata: https://in-toto.readthedocs.io/en/latest/command-line-tools/in-toto-run.html

GitHub templates already standardize contributor input:

- GitHub PR templates: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository
- GitHub issue and PR templates: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates

## What CertaMerge Does Not Yet Add

CertaMerge community alpha does not yet add cryptographic CAR signing, enterprise separation of duties, org-wide ProofGraph memory, deployment gates, source-control administration, scanner engines, or formal compliance certification.

It also does not replace SLSA or in-toto. Those are deeper provenance and attestation ecosystems. CertaMerge should eventually consume or reference such attestations, not pretend to be the entire supply-chain integrity stack.

## Where CertaMerge Is Redundant

CertaMerge would be redundant if it only:

- re-ran tests;
- uploaded an artifact;
- repeated scanner findings;
- produced a generic AI summary;
- acted as a dashboard over GitHub checks;
- used an LLM to say whether code is safe.

Those shapes are not enough to justify the product.

## Where CertaMerge Is Meaningfully Differentiated

CertaMerge earns a role when it records the decision layer around a change:

- Verdict: `ALLOW`, `NEEDS_EVIDENCE`, `BLOCK`, observe-mode would-allow/would-block, or other explicit UX states.
- Policy reason: a deterministic explanation of which policy requirement applied.
- Missing proof: the exact proof that is absent, stale, malformed, failed, conflicting, or insufficient.
- Accountable next action: who must provide what evidence next.
- Change Authorization Record: a durable JSON record that can be verified and replayed by the community verifier.

The self-dogfood branch demonstrates this by running CertaMerge Gate against its own repository and producing a verifier-checked CAR.

## What Must Improve Before Public Alpha

Before public alpha promotion, the project should keep:

- the full test suite green;
- the self-dogfood workflow live-run validated on a GitHub pull request;
- the README public contract tests green;
- the self-dogfood reports linked from the PR;
- the CAR artifact uploaded by GitHub Actions;
- safe limitations language in public docs.

The public alpha can be useful without enterprise features if it is honest about those limits.

## What Must Improve Before Enterprise Claims

Before enterprise claims, CertaMerge needs:

- cryptographic CAR signing or a clear integration path to signed attestations;
- durable org-wide policy administration;
- role and owner mapping;
- separation-of-duties controls;
- deployment and agent-action gate support;
- retention and export controls;
- ProofGraph decision memory;
- self-hosted enterprise runtime;
- formal threat model and audit export evidence.

Those are not part of this public alpha self-dogfood branch.

## Self-Dogfood Value Test

The branch asks a useful question:

```text
Can the CertaMerge public repository produce proof that it follows its own proof policy?
```

Current local answer:

```text
Verdict: OBSERVE_ONLY_WOULD_ALLOW
Policy reason: All matched policy requirements are satisfied.
CAR verification: valid
Tests: 215 passed
```

## Final Value Verdict

CertaMerge should not compete as another scanner, chatbot, dashboard, or status-check wrapper.

It should own the proof-decision layer: policy reason, missing proof, accountable action, and a verifier-checked CAR. The self-dogfood branch is a credible public-alpha proof of that direction.
