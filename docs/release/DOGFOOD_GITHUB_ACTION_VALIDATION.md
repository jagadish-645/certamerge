# Dogfood GitHub Action Validation

## Scope

This report validates the self-dogfood GitHub Action workflow contract for the public alpha repository.

## Workflow Under Review

```text
.github/workflows/certamerge-proof-gate.yml
```

## Required Behavior

The workflow must:

- run on pull requests;
- run manually through `workflow_dispatch`;
- install the community package from the repository checkout;
- invoke the local composite action at `./community/github-action`;
- evaluate `repo: .` against `.certamerge.yml`;
- write `.tmp/certamerge-pr.car.json`;
- verify the CAR with `python -m certamerge verify-car .tmp/certamerge-pr.car.json`;
- upload artifact `certamerge-pr-car`;
- write a concise CertaMerge summary to the GitHub step summary;
- default pull-request behavior to observe mode rather than hard blocking contributors.

## Local Contract Evidence

The test suite verifies the static action and workflow contract:

- action inputs: `policy`, `repo`, `output`, `fail-on-block`, `artifact-name`
- action outputs: `car-path`, `verdict`, `summary-path`
- workflow path: `.github/workflows/certamerge-proof-gate.yml`
- local action call: `uses: ./community/github-action`
- policy path: `.certamerge.yml`
- repo path: `.`
- output CAR path: `.tmp/certamerge-pr.car.json`
- CAR verification command
- artifact name: `certamerge-pr-car`

## Live Validation Status

Live GitHub Action evidence is created only after this branch is opened as a pull request. Until then, the workflow is locally contract-validated but not yet live-run validated on GitHub infrastructure.

## Failure Handling

If the workflow cannot generate a CAR, the action should expose the failed step in logs and the missing artifact should be treated as missing proof. If the CAR is generated but fails verification, the PR must not be moved out of draft.

## Non-Claims

The workflow does not certify the repository as secure. It records whether the self-dogfood policy found the required proof for this PR.
