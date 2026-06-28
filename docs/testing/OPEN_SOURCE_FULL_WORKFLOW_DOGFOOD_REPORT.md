# Open-Source Full Workflow Dogfood Report

Generated for branch `grand-finale/open-source-workflow-hardening`.

## Scope

This dogfood pass ran CertaMerge open source against the CertaMerge open-source repository itself plus six synthetic archetype repositories. The purpose was to prove that documented alpha workflows execute as real CLI, CAR, GitHub Action, packaging, and safety checks.

## Workflows Actually Run

The CGF-WTH open-source harness executed 81 checks covering:

- install from repo;
- CLI help;
- `recover`;
- `recover --json`;
- `recover --suggest-policy`;
- `suggest-policy --output`;
- Gate with repo snapshot;
- Gate with `--changed-files`;
- Gate with `--base/--head`;
- Gate with `--json`;
- `verify-car`;
- `explain-car`;
- `explain-car --json`;
- six archetype recover/suggest-policy/gate/verify/explain flows;
- CAR integrity mutation detection;
- GitHub Action proof gate, artifact upload, and summary contract;
- sample CAR verification;
- README contract;
- agent workflow doc;
- human quickstart doc;
- 5-minute demo doc;
- no-source-egress posture;
- local-path, secret-looking string, safe-language, and public/private leakage scans;
- pytest, collect-only, compileall, package build, twine check, and checksum generation.

## Results

| Area | Result |
|---|---|
| CGF-WTH score | `4.0` |
| CGF-WTH verdict | `final-alpha-ready` |
| Critical/high failures | `0` |
| Total failures | `0` |
| Test suite | `267 passed` |
| Package build | Passed |
| Twine check | Passed |
| CAR verification | Passed |
| Tampered CAR detection | Passed |
| Public/private leakage scan | Passed |

## Failed Because Of Bugs

Earlier loop failures were real enough to fix before accepting the result:

- the first harness pass expected old JSON keys instead of the current `accountable_next_action` contract;
- the GitHub Action contract check was too brittle for the actual shell invocation style;
- the README did not yet satisfy the final first-screen positioning contract;
- the no-source-egress doc did not state the no-telemetry default clearly enough;
- the public result report sanitizer missed `file:///C:/Users/...` install evidence.

All critical/high open-source failures are now resolved.

## Failed Because Of Environment

No current open-source workflow is blocked by environment.

## Docs That Overstated Readiness

The README presentation was upgraded so alpha readiness is confident but not overclaimed. It now distinguishes CertaMerge from GitHub rules and scanners, states alpha limits, and keeps enterprise boundaries explicit.

## What Was Fixed

- Rewrote `README.md` into the final professional alpha positioning.
- Added no-telemetry default language to `docs/community/no-source-egress.md`.
- Added `scripts/cgf_wth_open_source.py`.
- Added `docs/testing/CGF_WTH_OPEN_SOURCE.md`.
- Added `docs/testing/OPEN_SOURCE_WORKFLOW_INVENTORY.md`.
- Regenerated `docs/testing/CGF_WTH_OPEN_SOURCE_RESULTS.md` with sanitized public evidence.

## Remaining Accepted Limitations

- Open source is alpha-ready, not production certified.
- CARs are tamper-evident via content hash, but not yet signed for non-repudiation.
- The GitHub Action is validated by repository fixtures and contract checks, not by a live external marketplace release in this pass.
- No compliance certification is claimed.

## Final Verdict

```text
CERTAMERGE OPEN SOURCE GRAND FINALE READY FOR V0.1.0-ALPHA
```
