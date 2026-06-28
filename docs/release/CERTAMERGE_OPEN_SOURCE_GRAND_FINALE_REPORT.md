# CertaMerge Open-Source Grand Finale Report

## Branch And Commit

Branch:

```text
grand-finale/open-source-workflow-hardening
```

Current committed evidence branch before PR-link metadata update:

```text
b026f6d
```

PR link:

```text
https://github.com/jagadish-645/certamerge/pull/6
```

## Workflow Inventory Result

`docs/testing/OPEN_SOURCE_WORKFLOW_INVENTORY.md` exists and covers the required open-source workflows:

- install from repo;
- CLI help;
- Recover;
- Recover JSON;
- Recover suggested policy;
- suggest-policy output;
- Gate with repo snapshot;
- Gate with changed files;
- Gate JSON;
- verify-car;
- explain-car;
- sample archetypes;
- evidence adapters;
- CAR mutation checks;
- GitHub Action proof gate, artifact upload, and summary;
- agent workflow;
- human quickstart;
- 5-minute demo;
- release build;
- twine check;
- checksum generation;
- sample CAR verification;
- no-source-egress posture;
- safe-language scan.

## All Workflows Tested

Yes. The final CGF-WTH open-source harness executed 81 checks and recorded `0` failures.

Evidence:

```text
docs/testing/CGF_WTH_OPEN_SOURCE_RESULTS.md
```

## Bugs Found

- JSON contract drift in the initial harness assertions.
- GitHub Action invocation contract check drift.
- README first-screen positioning gaps.
- Missing explicit no-telemetry language in no-source-egress docs.
- Generated public result Markdown leaked a local file URL.

## Bugs Fixed

- Updated `scripts/cgf_wth_open_source.py` contracts.
- Rewrote `README.md`.
- Updated `docs/community/no-source-egress.md`.
- Regenerated sanitized `docs/testing/CGF_WTH_OPEN_SOURCE_RESULTS.md`.

## Remaining Limitations

- v0.1.0-alpha, not production certified.
- CARs are hash-verifiable, not yet signed for non-repudiation.
- No compliance certification is claimed.
- GitHub Action has repository-level contract validation in this pass, not external marketplace release validation.

## README Final Review

Passed.

Evidence:

```text
docs/release/README_FINAL_PROFESSIONAL_REVIEW.md
```

## CGF-WTH Score

```text
4.0
```

The score is intentionally capped below `5.0` because there is no external production proof.

## Test Results

```text
267 passed
compileall passed
python -m build passed
twine check passed
checksum generation passed
```

## CAR Verdict

Open-source self-gate verdict:

```text
OBSERVE_ONLY_WOULD_ALLOW
```

Tampered CAR verification:

```text
valid: false
error: CAR integrity content_hash does not match canonical CAR content.
```

## Release Readiness Verdict

```text
CERTAMERGE OPEN SOURCE GRAND FINALE READY FOR V0.1.0-ALPHA
```
