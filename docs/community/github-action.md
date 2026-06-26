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

The action does not send source code to a vendor service. It runs inside the workflow environment and emits metadata, evidence states, missing proof, repair missions, and a CAR artifact.

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
