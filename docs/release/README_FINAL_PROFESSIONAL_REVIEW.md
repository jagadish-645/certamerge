# README Final Professional Review

## File Reviewed

`README.md`

## Review Criteria

The README must tell a serious developer within 60 seconds:

- what CertaMerge is;
- why it exists;
- how it differs from GitHub rules and scanners;
- how to install;
- how to run Recover;
- how to run Gate;
- how to verify a CAR;
- how to use the GitHub Action;
- how agents use JSON output;
- what CertaMerge does not claim;
- what alpha means;
- where enterprise begins.

## Required First-Screen Positioning

Present:

```text
CertaMerge is an open-source ProofOps CLI for software changes.
```

Present:

```text
Does this change have enough proof to move forward, and can we verify that decision later?
```

## Required Distinction

Present:

```text
GitHub rules decide whether checks are required.
Scanners find issues.
CertaMerge records whether the proof required for a change is present, missing, stale, failed, malformed, conflicting, or insufficient - then writes a Change Authorization Record.
```

## Required Sections

| Section | Status |
|---|---|
| What CertaMerge does | Present |
| Quickstart | Present |
| Core workflow | Present |
| Example output | Present |
| GitHub Action | Present |
| Agent / JSON usage | Present |
| Change Authorization Records | Present |
| Evidence adapters | Present |
| What CertaMerge is not | Present |
| Security and privacy posture | Present |
| Community alpha limitations | Present |
| Enterprise boundary | Present |
| Contributing / feedback | Present |

## Safety Review

Passed:

- no compliance certification claim;
- no production enterprise readiness claim;
- no guaranteed-security claim;
- no source-code egress by default;
- no telemetry by default;
- no LLM final authorization claim;
- no non-repudiation claim before signing/key management is real.

## Harness Evidence

`scripts/cgf_wth_open_source.py` reports:

- README professional contract: passed;
- README first-screen positioning: passed;
- safe-language scan: passed.

## Verdict

The README is professional, developer-native, clear, and alpha-honest.

```text
README FINAL PROFESSIONAL REVIEW PASSED
```
