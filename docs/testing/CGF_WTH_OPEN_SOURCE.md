# CertaMerge Grand Finale Workflow Test Harness: Open Source

Short name: `CGF-WTH`

## Purpose

CGF-WTH verifies that open-source CertaMerge's ready-claimed workflows are executable, human-usable, agent-usable, and honest about alpha limits. It is stricter than CPPEF: CPPEF scores usefulness, while CGF-WTH proves workflow execution.

## Scoring

| Score | Meaning |
|---:|---|
| 0 | broken |
| 1 | documented but unusable |
| 2 | partially usable |
| 3 | alpha usable |
| 4 | final alpha / pilot ready |
| 5 | production-grade |

The open-source alpha must not score `5` because cryptographic CAR signing, production deployment hardening, and external user proof are not implemented.

## Command

```powershell
python scripts\cgf_wth_open_source.py
```

## Output

```text
.tmp/cgf-wth/open-source-results.json
docs/testing/CGF_WTH_OPEN_SOURCE_RESULTS.md
```

## Workflow Coverage

The harness executes or inspects:

- install from repository;
- CLI help;
- `recover`;
- `recover --json`;
- `recover --suggest-policy`;
- `suggest-policy --output`;
- `gate` with a repo snapshot;
- `gate` with `--changed-files`;
- `gate` with `--base` and `--head`;
- `gate --json`;
- `verify-car`;
- `explain-car`;
- `explain-car --json`;
- archetype Recover, policy suggestion, Gate, CAR verification, and JSON explanation;
- CAR mutation detection;
- sample CAR verification;
- GitHub Action proof gate, artifact upload, and summary contract;
- agent workflow documentation;
- human quickstart documentation;
- 5-minute demo documentation;
- no-source-egress posture;
- README professional contract;
- local path, secret-looking string, unsafe claim, and public/private leakage scans;
- full pytest suite;
- test collection;
- `compileall`;
- package build;
- `twine check`;
- checksum generation.

## Failure Rules

Critical or high failures block the grand finale verdict. A workflow may only remain documented as ready if it is executed by CGF-WTH, covered by a focused test, or explicitly downgraded in docs to planned or not implemented.

## Final Verdict Contract

The result must end with exactly one of:

```text
CERTAMERGE OPEN SOURCE GRAND FINALE READY FOR V0.1.0-ALPHA
```

or:

```text
CERTAMERGE OPEN SOURCE GRAND FINALE NOT READY - missing: ...
```
