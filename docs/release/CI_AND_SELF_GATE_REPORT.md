# CI And Self-Gate Report

Date: 2026-06-27

## Summary

The public CI and self-gate workflows were tightened for community alpha release readiness.

## CI Updates

`.github/workflows/ci.yml` now includes:

- Python 3.11 and 3.12 matrix;
- editable install;
- pytest installation;
- `python -m pip check`;
- CLI smoke commands;
- changed-files Gate smoke;
- pytest;
- compileall;
- sample CAR verification;
- package build;
- GitHub Action metadata validation.

## Self-Gate Updates

`.github/workflows/certamerge-proof-gate.yml` now passes:

- PR base SHA;
- PR head SHA;
- non-blocking self-gate behavior by default.

The composite action uses the base/head range when available and records `repo_snapshot` fallback when not.

## Current GitHub PR #4 Checks Before This Hardening Pass

| Check | Result |
|---|---|
| `CertaMerge CI / test` | success |
| `CertaMerge Proof Gate / certamerge-proof` | success |

## Required After Push

After this hardening pass is committed and pushed, both checks must be re-run and pass again before PR #4 can be merged.

## Verdict

```text
CI AND SELF-GATE HARDENED — REMOTE CHECKS MUST PASS AFTER PUSH
```
