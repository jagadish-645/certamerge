# GitHub Action Live Validation Checklist

## Purpose

This checklist turns the statically validated CertaMerge GitHub Action into live evidence before public launch.

Run this only in a clean test repository or controlled test branch. Do not use a customer repository for first validation.

## Setup

1. Create a clean test GitHub repository.
2. Add a minimal `.certamerge.yml` policy.
3. Add a small sample app with one safe PR path and one protected path.
4. Add a workflow that uses the public CertaMerge action:

```yaml
name: CertaMerge Proof Gate

on:
  pull_request:

permissions:
  contents: read

jobs:
  certamerge:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: OWNER/certamerge/community/github-action@main
        with:
          policy: .certamerge.yml
          repo: .
          output: certamerge-car.json
          artifact-name: certamerge-car
          fail-on-block: "false"
```

Replace `OWNER` with the actual GitHub owner after remotes are configured.

## Allow PR

1. Open a PR that changes a low-risk path.
2. Confirm the workflow runs.
3. Confirm the action installs CertaMerge from the action path.
4. Confirm the verdict output is set.
5. Confirm a `certamerge-car` artifact exists.
6. Download the CAR artifact and verify it locally:

```powershell
python -m certamerge verify-car certamerge-car.json
python -m certamerge explain-car certamerge-car.json
```

## Needs-Evidence PR

1. Open a PR that changes a protected path without required evidence.
2. Confirm the action emits a blocking or would-block verdict.
3. Confirm `fail-on-block: "false"` keeps the workflow from failing.
4. Confirm the summary shows:
   - verdict;
   - policy reason;
   - missing proof;
   - accountable next action;
   - CAR artifact path.

## Configured Block Mode

1. Change the workflow to `fail-on-block: "true"`.
2. Re-run the needs-evidence PR workflow.
3. Confirm the job fails only because CertaMerge emitted a blocking verdict.
4. Confirm the CAR artifact still uploads.

## Built-In Repository Validation Workflow

The public CertaMerge repository also contains:

```text
.github/workflows/certamerge-action-validation.yml
```

This workflow should pass on `main` before public release. It validates allow, observe would-block, and configured-block behavior using unique CAR artifact names.

Current validated run:

```text
https://github.com/jagadish-645/certamerge/actions/runs/28169666397
```

## Artifact And Log Review

Confirm:

- CAR artifact exists and contains no raw source code;
- action logs contain no secrets, tokens, or raw diffs;
- workflow summary is clear enough for a developer to act on;
- the generated CAR verifies locally;
- the generated CAR explains locally.

## Evidence To Save

Before public launch, save:

- workflow run URL;
- allow PR URL;
- needs-evidence PR URL;
- configured block-mode PR URL or run URL;
- screenshots or logs showing artifact upload;
- downloaded CAR verification output;
- downloaded CAR explanation output;
- notes for any failure and fix.

## Exit Criteria

Live validation passes only when allow, needs-evidence, and configured-block paths all behave as documented.

If any path fails, public launch remains blocked until the action or docs are corrected and the checklist is rerun.
