# Security And Privacy Hardening Report

## Scope

This report covers the public community alpha repository self-dogfood branch. It reviews whether the branch keeps CertaMerge local, metadata-oriented, and safe to inspect before a public alpha PR.

## Security Posture

CertaMerge community alpha commands run locally by default. The self-dogfood flow reads repository files, policy files, sample evidence, and metadata evidence. It does not require source code to leave the repository environment to produce Recover, Gate, or Verify outputs.

The branch strengthens the public repository by adding:

- observe-mode self-dogfood policy;
- metadata-only evidence files;
- CAR verification proof;
- no-source-egress proof;
- no-secret-leakage proof;
- issue templates that tell users not to paste secrets, tokens, private keys, customer data, or proprietary source code;
- PR template fields for verdict, policy reason, missing proof, accountable action, CAR, verification, and limitations;
- graceful CLI error handling for missing CAR files.

## Privacy Posture

The CAR and Recover/Gate outputs should describe evidence state and risk surfaces, not raw source code. Existing tests assert that sample Recover and Gate payloads do not emit raw source snippets for the sample repositories.

The self-dogfood evidence files are marked metadata-sensitive and do not carry customer payloads.

## Local Scan Commands

The branch should be reviewed with:

```powershell
python -m pytest -q
python -m compileall community
rg -n --hidden -g '!.git/**' -g '!.pytest_cache/**' -g '!__pycache__/**' -g '!*.egg-info/**' '<credential-or-local-path-pattern>' .
```

## Known Security Limits

- Community alpha CARs have schema and SHA-256 content-hash verification, not cryptographic signing.
- The self-dogfood workflow is observe mode by default.
- The repository does not yet ship enterprise policy administration, separation of duties, deployment gates, org-wide audit export, or ProofGraph services.
- Local environment dependency conflicts must be separated from CertaMerge package behavior.

## Release Stance

Security and privacy posture is acceptable for draft public-alpha review when the full local verification commands pass. It is not a production authorization claim.
