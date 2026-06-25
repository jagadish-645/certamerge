# Test Expansion Report

## Objective

Expand CertaMerge release-candidate testing beyond the controlled-alpha baseline only where the tests add real trust.

## Previous Baseline

```text
100 tests
```

The baseline already covered:

- community CLI Recover/Gate/verify/explain;
- evidence state handling;
- CAR verifier consistency;
- sample CAR validity;
- root policy loading;
- GitHub Action metadata basics;
- enterprise alpha runtime basics.

## Added Coverage

New release-candidate tests were added in:

```text
community/tests/test_public_release_candidate_contracts.py
```

The added tests cover:

- README first-30-second product explanation;
- 5-minute quickstart copy-paste commands;
- public alpha limitations;
- CAR integrity language;
- GitHub Action install path from `$GITHUB_ACTION_PATH`;
- GitHub Action summary behavior on failure;
- GitHub Action inputs and outputs;
- CI release smoke checks;
- release foundation report existence;
- public/private repository split guardrails;
- package metadata;
- packaging report warning about enterprise entry point split;
- malformed CAR JSON CLI behavior;
- invalid policy CLI behavior;
- security forbidden-claim language;
- SBOM/provenance and release artifact honesty.

## New Test Count

```text
175 tests collected
175 passed
```

## Commands Run

```powershell
python -m pytest --collect-only -q
python -m pytest -q
```

## Release Trust Added

The expansion adds meaningful public-release trust because it locks down the user-facing claims and release safety boundary, not just internal implementation behavior.

It specifically reduces risk of:

- public README overclaiming;
- community docs hiding limits;
- enterprise material leaking into the public repo;
- broken GitHub Action install behavior in caller repositories;
- silent invalid-policy CLI failures;
- vague CAR signing claims;
- release-trust plans being described as already implemented.

## Remaining Testing Gaps

Still not covered:

- live GitHub Action execution in GitHub;
- release artifact build from wheel/source distribution;
- SBOM generation in CI;
- signed release verification;
- public/private split staging test;
- public-only package install after enterprise files are removed;
- network egress guard beyond static/local behavior;
- large-repo performance test;
- fuzz/property test suites for all parsers.

## Verdict

The test target of 120+ meaningful tests has been exceeded.

Testing is stronger, but public release remains blocked by repository split, live action validation, artifact integrity, and initial commit/remote readiness.
