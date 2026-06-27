# PR-Diff-Aware Proof

CertaMerge Community Gate can scope policy matching to a concrete change when changed-file information is available. This makes a Gate run more precise than a whole-repo snapshot while preserving an honest fallback when PR metadata is unavailable.

## What It Does

Gate now records a `change_context_mode` in every generated CAR:

| Mode | Meaning |
|---|---|
| `explicit_changed_files` | A newline-delimited changed-files list was supplied with `--changed-files`. |
| `git_diff` | Gate derived changed files from `git diff --name-only base...head`. |
| `github_pr` | Gate derived PR base/head context from GitHub Actions or event metadata and resolved files through Git. |
| `repo_snapshot` | Gate could not safely derive changed files and evaluated the repository snapshot instead. |

The CAR also records:

- `changed_files`
- `changed_file_count`
- `base_sha`
- `head_sha`
- `pr_number` when available
- `github_run_id` when available
- `unavailable_context` warnings when diff context could not be resolved

## CLI Usage

Explicit changed-files list:

```powershell
python -m certamerge gate --repo . --policy .certamerge.yml --changed-files .tmp/changed-files.txt --output .tmp/pr.car.json
python -m certamerge verify-car .tmp/pr.car.json
```

Git diff range:

```powershell
python -m certamerge gate --repo . --policy .certamerge.yml --base <base-sha> --head <head-sha> --output .tmp/pr.car.json
python -m certamerge verify-car .tmp/pr.car.json
```

Fallback behavior:

```text
If the changed-file list or git diff range cannot be resolved, CertaMerge records repo_snapshot mode and does not claim PR-diff precision.
```

## GitHub Action Usage

The composite action accepts:

```yaml
with:
  policy: .certamerge.yml
  repo: .
  output: .tmp/certamerge-pr.car.json
  base: ${{ github.event.pull_request.base.sha }}
  head: ${{ github.event.pull_request.head.sha }}
```

If checkout history does not contain the base/head range, Gate falls back to `repo_snapshot` and records that changed files were unavailable.

## Security And Privacy Boundary

CertaMerge records file paths as metadata. It does not store raw diffs or raw source code in the CAR by default.

Do not put raw source snippets, secrets, tokens, credentials, private keys, or proprietary raw diffs into changed-files input files.

## Acceptance Criteria

A PR-diff-aware CAR is acceptable when:

- `change_context_mode` is explicit and accurate;
- `changed_files` is populated only when changed files were actually known;
- risk surfaces are computed from changed files when available;
- policy rule path matching uses changed files when available;
- fallback mode is recorded honestly as `repo_snapshot`;
- `verify-car` succeeds for the generated CAR.

## Known Limitations

- Community alpha does not call the GitHub API to fetch changed files.
- `github_pr` mode depends on local checkout history containing the base/head range.
- `repo_snapshot` fallback is intentionally less precise and should not be described as PR-diff proof.

