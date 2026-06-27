# PR-Diff-Aware Proof Report

Date: 2026-06-27

## Summary

Implemented practical PR-diff-aware Gate v1 for the community alpha. Gate can now scope policy matching and risk classification to known changed files, while honestly falling back to repo snapshot mode when changed files cannot be resolved.

## Implemented

- Added `--changed-files` CLI input for newline-delimited changed-file lists.
- Added `--base` and `--head` CLI inputs for `git diff --name-only base...head`.
- Added GitHub Actions/event context detection for PR number, base SHA, head SHA, and run id.
- Added CAR fields:
  - `change_context_mode`;
  - `changed_files`;
  - `changed_file_count`;
  - `base_sha`;
  - `head_sha`;
  - `pr_number`;
  - `github_run_id`;
  - `unavailable_context` fallback warnings.
- Scoped policy path matching to changed files when available.
- Scoped risk-surface classification to changed files when available.
- Preserved honest `repo_snapshot` fallback when diff metadata is unavailable.
- Added GitHub Action inputs:
  - `changed-files`;
  - `base`;
  - `head`.

## Validation

Focused tests passed:

```text
7 passed
```

Covered:

- explicit changed files;
- git diff unavailable fallback;
- GitHub event fallback;
- docs-only change;
- workflow change;
- auth/source change;
- dependency file change;
- Terraform file change.

## Limitations

- Community alpha does not call the GitHub API to fetch PR file lists.
- `github_pr` mode depends on checkout history being deep enough to diff base/head.
- `repo_snapshot` is a fallback and must not be described as PR-diff proof.

## Verdict

```text
PR-DIFF-AWARE PROOF V1 IMPLEMENTED FOR COMMUNITY ALPHA
```

