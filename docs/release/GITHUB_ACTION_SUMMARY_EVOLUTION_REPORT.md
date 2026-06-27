# GitHub Action Summary Evolution Report

## Summary

The CertaMerge composite GitHub Action now writes a structured proof summary from the generated CAR instead of copying raw CLI output into `GITHUB_STEP_SUMMARY`.

The summary is designed for PR reviewers. The CAR artifact remains the source of truth.

## Implementation Changes

- Gate output is still shown in logs through `certamerge-cli-output.txt`.
- The action now reads the generated CAR and writes `certamerge-summary.txt`.
- The workflow summary now includes:
  - verdict;
  - policy reason;
  - matched rules;
  - evidence states;
  - missing proof;
  - accountable next action;
  - CAR artifact name;
  - verification command.
- The action still uploads the configured CAR artifact with `actions/upload-artifact@v4`.
- The action still defaults to non-blocking behavior.
- The action still supports `fail-on-block: "true"` for intentional enforcement.

## Reviewer-Facing Contract

The summary must follow this shape:

```markdown
## CertaMerge Proof Gate

Verdict: `<state>`

Policy reason:
<reason>

Matched rules:
- `<rule-id>` - <result>

Evidence:
- `<evidence-type>`: `<state>`

Missing proof:
- `<proof-type>`: `<state>` - <reason>

Accountable next action:
<owner> - <action>

CAR artifact:
`<artifact-name>`

Verification:
`python -m certamerge verify-car <car-path>`
```

## Static Validation

Tests now check that the composite action contains:

- `GITHUB_STEP_SUMMARY`;
- `actions/upload-artifact@v4`;
- `OBSERVE_ONLY_WOULD_BLOCK`;
- `## CertaMerge Proof Gate`;
- `Matched rules:`;
- `Evidence:`;
- `Missing proof:`;
- `Accountable next action:`;
- `python -m certamerge verify-car`.

## Anti-Slop Assessment

This is workflow-native. It does not introduce a dashboard, chatbot, scanner replacement, or LLM-generated review.

The summary compresses the CAR into the required interaction grammar:

```text
Verdict.
Policy reason.
Missing proof.
Accountable next action.
Change Authorization Record.
```

## Current Limits

- The summary is static Markdown generated inside the composite action.
- It intentionally truncates long text fields to avoid noisy PR summaries.
- It does not render full evidence payloads or source code.
- It does not replace offline CAR verification.

## Verdict

The GitHub Action summary is useful enough for wrapper-kill and self-dogfood validation. Live GitHub Actions validation still needs to run after this branch is pushed.

