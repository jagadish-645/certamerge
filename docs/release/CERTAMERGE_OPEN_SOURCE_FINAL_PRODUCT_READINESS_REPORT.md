# CertaMerge Open-Source Final Product Readiness Report

Generated: 2026-06-27

Branch: `finalization/open-source-product-hardening`

Current branch head at report generation: `d4418eb`

## Product Status

CertaMerge open source is a community alpha deterministic proof-decision layer for software changes.

It currently provides:

- local Recover;
- proof-only Gate;
- CAR creation;
- CAR hash-integrity verification;
- CAR explanation;
- repo-adaptive proof detection;
- starter policy suggestion;
- evidence states and repair missions;
- GitHub Action wrapper;
- agent-readable JSON output for Recover, Gate, and explain-car;
- community docs, quickstart, demo outputs, and agent workflow sample.

## Tests And Gates

Fresh final gate passed on 2026-06-27:

- editable install passed;
- CLI help passed;
- Recover on repo root passed;
- Recover with suggested policy passed;
- suggest-policy output passed;
- Gate on repo root produced a CAR;
- CAR verification returned `valid: true`;
- explain-car rendered the CAR;
- `python -m pytest -q` returned `267 passed`;
- `python -m pytest --collect-only -q` collected `267` tests;
- `python -m compileall community scripts` passed;
- package build produced wheel and source archive;
- `twine check dist\*` passed;
- checksum generation passed.

## CPPEF Score

CPPEF open-source score: `4.0`

Category scores:

- installation: `4.0`
- CLI UX: `4.0`
- Recover: `4.0`
- suggest-policy: `4.0`
- Gate: `4.0`
- evidence adapters: `4.0`
- CAR integrity: `4.0`
- GitHub Action: `4.0`
- agent usability: `4.0`
- human usability: `4.0`
- security/privacy/safe language: `4.0`

## Agent Usability

Agent usability improved in this pass:

- `recover --json`
- `gate --json`
- `explain-car --json`
- machine-readable JSON test coverage;
- agent workflow documentation;
- sample agent run fixture.

This lets a coding agent parse verdict, policy reason, missing proof, accountable next action, repair missions, and CAR status without guessing from prose.

## Human Usability

Human onboarding is usable for alpha:

- README gives the first 30-second explanation.
- Quickstart gives install/run/verify path.
- Demo docs show expected outputs.
- Alpha limitations are explicit.
- No-source-egress and no-telemetry defaults are documented.

## General Repo Validation

Coverage includes:

- Python library profile;
- Node/TypeScript profile;
- GitHub Action repo profile;
- Terraform/IaC profile;
- monorepo profile;
- docs-heavy profile;
- auth, payment, workflow, dependency, database, IaC, generated-code, and docs risk surfaces.

## CAR Verification

Final self-gate CAR:

- verdict: `OBSERVE_ONLY_WOULD_ALLOW`;
- verification result: `valid: true`;
- policy hash present;
- CAR explanation rendered verdict, policy reason, missing proof, next action, state, commit, and policy hash.

## GitHub Action Status

The GitHub Action wrapper remains part of the public alpha surface. Local tests validate action metadata and release-candidate workflow expectations. Remote CI should still be used before cutting a public tag.

## Known Limitations

- Community CARs are not cryptographically signed yet.
- Community alpha is not an enterprise service.
- No RBAC/SSO, durable enterprise storage, admin UI, hosted SaaS, or deployment gate.
- Python 3.12 validation was not run in this local final gate.
- No external user adoption evidence yet.
- No production security certification is claimed.

## Release Readiness Verdict

```text
CERTAMERGE OPEN SOURCE V0.1.0-ALPHA FINAL READY
```
