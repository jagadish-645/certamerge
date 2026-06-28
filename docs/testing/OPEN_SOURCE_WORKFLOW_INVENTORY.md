# Open-Source Workflow Inventory

## Purpose

This inventory lists every open-source workflow CertaMerge claims to support and records whether it is implemented, tested, and ready. Any workflow marked ready must be executed by CGF-WTH, covered by an existing test, or directly validated in the grand finale dogfood report.

## Inventory

| Workflow | Command or doc path | Implemented | Tested | Test evidence | Known bugs | Readiness verdict |
|---|---|---|---|---|---|---|
| install from repo | `python -m pip install -e .` | yes | yes | CGF-WTH and final gate | none known | ready for alpha |
| CLI help | `python -m certamerge --help` | yes | yes | CGF-WTH and final gate | none known | ready for alpha |
| recover | `python -m certamerge recover <repo>` | yes | yes | CGF-WTH, unit tests, final gate | none known | ready for alpha |
| recover --json | `python -m certamerge recover <repo> --json` | yes | yes | CGF-WTH JSON parse, unit tests | none known | ready for alpha |
| recover --suggest-policy | `python -m certamerge recover <repo> --suggest-policy` | yes | yes | CGF-WTH and final gate | none known | ready for alpha |
| suggest-policy | `python -m certamerge suggest-policy <repo>` | yes | yes | CGF-WTH and tests | none known | ready for alpha |
| suggest-policy --output | `python -m certamerge suggest-policy <repo> --output <file>` | yes | yes | CGF-WTH and final gate | none known | ready for alpha |
| gate with repo snapshot | `python -m certamerge gate --repo <repo> --policy <policy> --output <car>` | yes | yes | CGF-WTH, unit tests, final gate | none known | ready for alpha |
| gate with --changed-files | `python -m certamerge gate --repo <repo> --policy <policy> --changed-files <file> --output <car>` | yes | yes | CGF-WTH and focused change-binding tests | none known | ready for alpha |
| gate with --base/--head | `python -m certamerge gate --repo <repo> --policy <policy> --base <sha> --head <sha> --output <car>` | yes | yes | CGF-WTH and fallback tests | none known | ready for alpha |
| gate --json | `python -m certamerge gate --repo <repo> --policy <policy> --json --output <car>` | yes | yes | CGF-WTH JSON parse, unit tests | none known | ready for alpha |
| verify-car | `python -m certamerge verify-car <car>` | yes | yes | CGF-WTH, verifier tests, final gate | none known | ready for alpha |
| explain-car | `python -m certamerge explain-car <car>` | yes | yes | CGF-WTH and final gate | none known | ready for alpha |
| explain-car --json | `python -m certamerge explain-car <car> --json` | yes | yes | CGF-WTH JSON parse, unit tests | none known | ready for alpha |
| evidence adapters | `community/cli/certamerge/evidence.py` and `docs/community/evidence-adapters.md` | yes | yes | evidence state contract tests and CGF-WTH | none known | ready for alpha |
| CAR integrity mutation checks | `python -m certamerge verify-car <mutated-car>` | yes | yes | CGF-WTH mutation check and verifier tests | none known | ready for alpha |
| GitHub Action proof gate | `community/github-action/action.yml` | yes | partial | metadata and static contract tests; live GitHub action has prior validation docs | live external rerun not part of local harness | ready for alpha with documented external CI boundary |
| GitHub Action artifact upload | `community/github-action/action.yml` | yes | partial | static contract tests and CGF-WTH inspection | live artifact upload depends on GitHub runner | ready for alpha with external-runner caveat |
| GitHub Action summary | `community/github-action/action.yml` | yes | partial | static contract tests and CGF-WTH inspection | live summary depends on GitHub runner | ready for alpha with external-runner caveat |
| agent workflow | `docs/community/agent-workflow.md` and `samples/agent-workflows/auth-missing-proof-agent-run.json` | yes | yes | CGF-WTH docs check and JSON CLI tests | repair execution remains human/agent performed | ready for alpha |
| human quickstart | `docs/community/quickstart.md` | yes | yes | CGF-WTH docs check and final gate commands | none known | ready for alpha |
| 5-minute demo | `docs/demo/5_MINUTE_PUBLIC_ALPHA_DEMO.md` | yes | yes | CGF-WTH docs check and manual dogfood commands | none known | ready for alpha |
| release build | `python -m build` | yes | yes | CGF-WTH and final gate | none known | ready for alpha |
| twine check | `python -m twine check dist\*` | yes | yes | CGF-WTH and final gate | none known | ready for alpha |
| checksum generation | `python scripts\generate_checksums.py` | yes | yes | CGF-WTH and final gate | none known | ready for alpha |
| sample CAR verification | `samples/cars/*.json` | yes | yes | CGF-WTH and verifier tests | some samples may be negative examples; verifier must return cleanly | ready for alpha |
| no-source-egress posture | `docs/community/no-source-egress.md` | yes | yes | CGF-WTH docs and leakage scans | no runtime network monitor in alpha | ready for alpha with documented limit |
| safe-language scan | CGF-WTH scan | yes | yes | CGF-WTH | none known | ready for alpha |

## Downgrade Rule

If a workflow fails CGF-WTH or final gate and cannot be fixed in this pass, the public README and docs must mark it as planned, limited, or externally dependent. It must not remain ready-claimed.

## Current Inventory Verdict

The inventory is complete for the open-source alpha surface. Final readiness depends on CGF-WTH and the full dogfood report.
