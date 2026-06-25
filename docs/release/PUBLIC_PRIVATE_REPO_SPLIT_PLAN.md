# Public And Private Repository Split Plan

## Purpose

The current workspace contains community product, enterprise alpha, architecture documents, services documents, and local agent-system material.

Because the target GitHub repositories are:

```text
certamerge              public
certamerge_enterprise   private
```

the current workspace must not be pushed wholesale to the public repository.

## Verified GitHub Targets

Verified through GitHub CLI:

| Repository | Visibility | URL |
|---|---|---|
| `jagadish-645/certamerge` | Public | `https://github.com/jagadish-645/certamerge` |
| `jagadish-645/certamerge_enterprise` | Private | `https://github.com/jagadish-645/certamerge_enterprise` |

Do not set the current mixed workspace's `origin` to the public repository until the public-only tree exists.

## Public Repository: `certamerge`

Allowed public assets:

- `README.md`
- `LICENSE`
- `CODE_OF_CONDUCT.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `.gitignore`
- `.gitattributes`
- `.certamerge.yml`
- `.github/workflows/ci.yml`
- `pyproject.toml` after enterprise package/script removal or public-only packaging split
- `community/cli/certamerge`
- `community/github-action`
- `community/policies`
- `community/tests`
- `docs/community`
- `docs/release` public-release files only
- `samples/cars`
- `samples/evidence`
- `samples/policies`
- `samples/prs`
- `samples/repos`
- `specs/car`
- `specs/evidence`
- `specs/policy`
- `specs/verdict`
- `specs/repair-mission`
- `specs/open-core`

## Private Repository: `certamerge_enterprise`

Private assets:

- `enterprise/server`
- `enterprise/tests`
- `docs/enterprise`
- `docs/services`
- enterprise architecture and paid-tier strategy documents;
- design-partner readiness reports;
- proprietary risk/policy/ProofGraph planning;
- future enterprise deployment, SoD, ProofGraph, audit-export, and support material.

## Internal-Only Or Founder-Only Assets

These should not be pushed to the public repository without an explicit publication decision:

- `agent-system`
- local `skills`
- exploratory UX or architecture drafts not intended for open-source users;
- acquisition or monetization strategy;
- premium pricing and packaging material.

## Required Split Action Before Public Push

1. Create a clean public staging branch or staging directory.
2. Copy only public assets into that staging surface.
3. Remove enterprise entry points from public package metadata.
4. Run public-only install and tests from the staging surface.
5. Confirm public docs contain no enterprise-private files and contain community-safe assets only.
6. Configure public remote only after the public tree is clean.
7. Push only after the staged tree has passed validation.

## Current Verdict

public/private split is designed and locally staged.

Local staging has been validated under:

```text
.tmp/public-staging
.tmp/enterprise-staging
```

Public launch remains blocked until the staged repositories are pushed, live GitHub Action validation passes, and release artifact integrity work is completed.
