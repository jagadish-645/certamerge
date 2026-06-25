# GitHub Action Validation

## Current Status

The CertaMerge GitHub Action is statically validated for public-alpha release-candidate review.

Live validation in a clean GitHub repository has not been performed in this local run.

## Action File

```text
community/github-action/action.yml
```

## Action Contract

The action must:

- install CertaMerge from the action checkout path, not from the caller repository;
- evaluate the caller repository path passed through `repo`;
- use the policy path passed through `policy`;
- write a CAR to the path passed through `output`;
- emit a `verdict` output from the generated CAR;
- upload the CAR artifact;
- append a workflow summary;
- default to non-blocking behavior with `fail-on-block: "false"`;
- fail only when `fail-on-block: "true"` and the verdict is blocking;
- avoid vendor callbacks and LLM-based authorization.

## Inputs

| Input | Default | Meaning |
|---|---|---|
| `policy` | `.certamerge.yml` | Policy file inside the caller repository. |
| `repo` | `.` | Repository path to evaluate. |
| `output` | `certamerge-car.json` | CAR output path. |
| `fail-on-block` | `"false"` | Whether blocking verdicts should fail the job. |

## Outputs

| Output | Meaning |
|---|---|
| `car-path` | Path to the generated CAR. |
| `verdict` | Verdict state read from the generated CAR. |
| `summary-path` | Local summary text path. |

## Static Validation Performed

The local test suite and CI workflow validate:

- composite action metadata parses as YAML;
- required inputs exist;
- required outputs exist;
- action install command uses `$GITHUB_ACTION_PATH/../..`;
- artifact upload step uses `actions/upload-artifact@v4`;
- summary step writes to `GITHUB_STEP_SUMMARY`;
- blocking state list includes `OBSERVE_ONLY_WOULD_BLOCK`;
- default behavior is non-blocking.

## Example Caller Workflow

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
          fail-on-block: "false"
```

Replace `OWNER` with the actual GitHub owner after the public repository is prepared.

## Live Validation Requirement

Before public launch, run the live checklist in:

```text
docs/release/GITHUB_ACTION_LIVE_VALIDATION_CHECKLIST.md
```

Public release should not claim the GitHub Action is production-proven until that checklist has evidence from a real GitHub Actions run.
