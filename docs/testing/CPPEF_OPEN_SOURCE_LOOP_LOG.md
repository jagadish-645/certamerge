# CPPEF Open-Source Loop Log

Generated: 2026-06-27

Scope: CertaMerge community/open-source product on branch `finalization/open-source-product-hardening`.

## Loop 0 - Baseline Inspection

Evidence inspected:

- Existing community CLI, Recover, Gate, CAR verifier, GitHub Action wrapper, samples, docs, and release reports.
- Existing public readiness reports and tests.
- Current branch head at report generation: `d4418eb`.

Baseline risks:

- Agent workflows needed a clearer machine-readable path.
- The CLI did not expose JSON output consistently for Recover, Gate, and explain-car.
- No CPPEF runner existed to score the community product against install, CLI, Recover, Gate, evidence, CAR, action, human, agent, and safe-language criteria.

Decision:

- Continue to Loop 1.

## Loop 1 - Agent-Usability And CPPEF Hardening

Fixes made:

- Added `--json` output to `recover`.
- Added `--json` output to `gate`.
- Added `--json` output to `explain-car`.
- Added `test_cli_agent_json_outputs_are_machine_readable`.
- Added `docs/community/agent-workflow.md`.
- Added `samples/agent-workflows/auth-missing-proof-agent-run.json`.
- Added `scripts/cppef_open_source.py`.
- Added `docs/testing/CPPEF_OPEN_SOURCE_FRAMEWORK.md`.
- Generated `docs/testing/CPPEF_OPEN_SOURCE_RESULTS.md`.
- Strengthened `docs/community/no-source-egress.md` with no telemetry and no vendor-egress default language.

Top weaknesses addressed:

| Weakness | Resolution |
|---|---|
| Agent-readable output was incomplete | JSON output added to core commands |
| Agent workflow needed a concrete sample | Agent workflow doc and sample run added |
| Product proof needed an executable scorecard | CPPEF runner and framework added |
| Safe-language/no-egress evidence needed to be explicit | No-source-egress doc strengthened |

Validation:

- CPPEF open-source score: `4.0`.
- CPPEF verdict: `release-ready alpha`.
- Targeted community tests passed during implementation.

Decision:

- Stop after Loop 1 because no critical or high blocker remained in the CPPEF result, full final gate passed, CAR verified, package built, and safe-language scan issues were either fixed or deliberate forbidden-claim examples in tests/docs.

## Final Gate Evidence

Fresh final gate passed on 2026-06-27:

```text
python -m pip install -e .
python -m certamerge --help
python -m certamerge recover .
python -m certamerge recover . --suggest-policy
python -m certamerge suggest-policy . --output .tmp/final.suggested.certamerge.yml
python -m certamerge gate --repo . --policy .certamerge.yml --output .tmp/final-open-source.car.json
python -m certamerge verify-car .tmp/final-open-source.car.json
python -m certamerge explain-car .tmp/final-open-source.car.json
python -m pytest -q
python -m pytest --collect-only -q
python -m compileall community scripts
python -m build
python -m twine check dist\*
python scripts\generate_checksums.py
```

Observed results:

- `267 passed`.
- `267 tests collected`.
- `compileall` passed.
- Wheel and sdist built.
- `twine check` passed for wheel and sdist.
- Final CAR verified with `valid: true`.
- Final self-gate verdict: `OBSERVE_ONLY_WOULD_ALLOW`.
- Distribution checksums generated:
  - Wheel: `bf8940aab201f6c8461dc392806384eae978830d3fce01ca03f3e547bdad88db`
  - Source archive: `ed84b852fef7eee1438033a978535e3bc5875f2e4ac186da6323a5cdc8ff08a1`

## Accepted Limitations

- Community alpha CARs are hash-integrity checked but not cryptographically signed.
- Community alpha is a local CLI and GitHub Action wrapper, not an enterprise self-hosted service.
- Community alpha does not claim code security, certification, or production-enterprise readiness.
- Python 3.12 was listed in CPPEF coverage as a target, but this local final gate used the available Python 3.11 runtime.

## Final Verdict

```text
CERTAMERGE OPEN SOURCE V0.1.0-ALPHA FINAL READY
```
