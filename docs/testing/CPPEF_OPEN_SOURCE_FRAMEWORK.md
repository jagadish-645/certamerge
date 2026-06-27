# CPPEF Open-Source Framework

CPPEF evaluates whether CertaMerge open source is a deterministic proof-decision layer for software change that is useful to human engineers, AI coding agents, repo maintainers, reviewers, platform engineers, and security-conscious developers.

This framework is intentionally harsh. Passing unit tests is not enough. The open-source product must be installable, runnable, understandable, generalizable, agent-usable, human-usable, safe in claims, and clean in public/private boundaries.

## Score Scale

| Score | Meaning |
|---|---|
| 0 | Broken / unusable |
| 1 | Toy demo |
| 2 | Useful alpha |
| 3 | Release-ready |
| 4 | Production-shaped |
| 5 | Enterprise-grade / acquisition-grade evidence |

Do not score 5 without real external adoption or strong proof. Do not score 4 if workflows are still buggy or narrow.

## Categories

### 1. Installation And Packaging

Checks:

- fresh clone install path is documented;
- editable install;
- wheel build;
- sdist build;
- twine check;
- checksums;
- package metadata;
- license metadata;
- CLI entrypoint;
- import sanity;
- Python 3.11;
- Python 3.12 where available.

### 2. CLI UX

Checks:

- help output;
- bad command handling;
- missing repo path;
- missing policy path;
- malformed policy;
- missing evidence;
- malformed evidence;
- invalid CAR;
- `explain-car` clarity;
- machine-readable output where available;
- human-readable output quality.

### 3. Recover Usefulness

Checks:

- repo type detection;
- ecosystem detection;
- CI detection;
- test source versus test result distinction;
- lockfile detection;
- security policy detection;
- scanner artifact detection;
- SBOM detection;
- Terraform/IaC detection;
- GitHub Action repo detection;
- docs-heavy detection;
- risk surfaces;
- missing proof output;
- repair missions.

### 4. Suggest-Policy Usefulness

Checks:

- repo-specific policy output;
- Python library policy;
- Node/TypeScript policy;
- GitHub Action policy;
- Terraform/IaC policy;
- monorepo policy;
- docs-heavy policy;
- mixed repo policy;
- policy validity;
- not overly generic;
- not impossibly strict.

### 5. Gate Usefulness

Checks:

- repo snapshot gate;
- explicit changed-files gate;
- base/head diff gate where git context exists;
- GitHub PR context where event fixtures exist;
- docs-only change;
- auth/source change;
- workflow change;
- dependency change;
- Terraform change;
- test-only change;
- mixed high-risk change;
- unknown context fallback.

### 6. Evidence Adapters

Checks:

- JUnit XML pass/fail/malformed;
- SARIF negative/failed/malformed;
- CycloneDX/SBOM present/malformed;
- Terraform plan present/malformed;
- Gitleaks/secret scan negative/failed/malformed;
- dependency lockfiles;
- `SECURITY.md`;
- `CODEOWNERS`;
- `LICENSE`;
- GitHub Action metadata;
- owner approval evidence;
- test result evidence;
- stale evidence if supported;
- conflicting evidence if supported.

### 7. CAR Integrity

Checks:

- CAR schema;
- CAR content hash;
- policy hash;
- evidence hashes;
- changed-files context;
- base/head context;
- PR metadata;
- mutation detection;
- missing context honesty;
- `verify-car` clean failure;
- `explain-car` clarity;
- unsigned/signature status warning or limitation.

### 8. GitHub Action

Checks:

- action metadata;
- inputs;
- outputs;
- artifact upload;
- CAR artifact;
- summary quality;
- fail-on-block;
- observe mode;
- PR context;
- minimal permissions;
- self-gate proof;
- CI integration.

### 9. General Repo Usefulness

Required archetypes:

- `python-library`;
- `node-typescript-app`;
- `github-action-repo`;
- `terraform-iac-repo`;
- `monorepo-app`;
- `docs-heavy-repo`.

Additional archetypes should be added when feasible:

- Go service;
- Java service;
- dockerized service;
- security-tooling repo.

### 10. Security, Privacy, And Safe Language

Checks:

- no source-code egress;
- no telemetry;
- no LLM final authorization;
- no local path leakage in public docs;
- no secret-looking leakage;
- no unsafe compliance claims;
- no production-enterprise claims;
- no private enterprise leakage;
- `SECURITY.md` quality;
- alpha limitations quality.

### 11. Agent Usability

Simulate:

- AI agent creates code change;
- AI agent runs Recover;
- AI agent runs Suggest Policy;
- AI agent runs Gate;
- AI agent sees missing proof;
- AI agent adds evidence or test artifact;
- AI agent reruns Gate;
- AI agent produces CAR;
- AI agent verifies CAR;
- AI agent includes proof summary in PR.

### 12. Human Engineer Usability

Test whether a normal engineer can understand:

- what CertaMerge is;
- how to install;
- how to run;
- what a verdict means;
- what missing proof means;
- what action to take;
- how to verify a CAR;
- what CertaMerge does not claim.

## Final Open-Source Verdicts

CPPEF must end open-source evaluation with exactly one of:

```text
CERTAMERGE OPEN SOURCE V0.1.0-ALPHA FINAL READY
```

```text
CERTAMERGE OPEN SOURCE NOT FINAL READY - missing: ...
```

```text
CERTAMERGE OPEN SOURCE NEEDS PRODUCT PIVOT - reason: ...
```
