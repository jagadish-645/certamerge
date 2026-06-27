# CertaMerge GitHub Action v0

The community GitHub Action runs the local CertaMerge CLI in a workflow, generates a CAR artifact, and defaults to non-disruptive proof behavior.

Example:

```yaml
name: CertaMerge Proof Gate
on:
  pull_request:
jobs:
  certamerge:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./community/github-action
        with:
          policy: .certamerge.yml
          repo: .
          output: certamerge-car.json
          fail-on-block: "false"
```

`fail-on-block` defaults to `false` so teams can observe proof gaps before enforcing blocks.

The action does not send source code to a vendor service. It runs inside the workflow environment and emits metadata, evidence states, missing proof, repair missions, a workflow-native proof summary, and a CAR artifact.

## PR Summary Shape

The action writes a structured summary to `GITHUB_STEP_SUMMARY` using the generated CAR:

```text
## CertaMerge Proof Gate

Verdict: `<verdict>`

Policy reason:
<reason>

Matched rules:
- `<rule-id>` - <result>

Evidence:
- `<evidence-type>`: `<state>`

Missing proof:
- None.

Accountable next action:
repo-owner - Proceed with record.

CAR artifact:
`certamerge-car`

Verification:
`python -m certamerge verify-car certamerge-car.json`
```

This summary is for reviewer workflow. The CAR artifact remains the source of truth.

## Self-Dogfood Workflow

This repository includes a workflow that runs the local composite action against CertaMerge itself:

```text
.github/workflows/certamerge-proof-gate.yml
```

The workflow uploads a `certamerge-pr-car` artifact and verifies the generated CAR with:

```powershell
python -m certamerge verify-car .tmp/certamerge-pr.car.json
```

The workflow remains non-blocking by default so pull requests can observe proof gaps before branch protection depends on CertaMerge.
