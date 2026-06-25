# Local Recover

Command:

```powershell
python -m certamerge recover .
```

Recover scans local repository metadata and emits:

- repo proof snapshot;
- detected project type;
- available evidence signals;
- missing proof;
- risk surfaces;
- repair missions;
- draft CAR data.

Recover detects:

- package manager files;
- test scripts;
- CI config;
- GitHub Actions workflows;
- dependency lockfiles;
- SARIF references;
- auth/payment/config/deployment path patterns;
- README, CONTRIBUTING, and SECURITY presence;
- generated-code style path hints without overclaiming.

Recover does not claim that a repo is secure. It reports missing proof and repair missions.

Recover treats proof quality as stateful evidence. Failed, stale, malformed, negative, insufficient, and conflicting evidence must remain visible because they lead to different user actions and different CAR records.
