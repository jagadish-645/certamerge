# Security

CertaMerge is an authorization and proof tool. It must be safer than the workflows it evaluates.

## Supported Versions

| Version | Status |
|---|---|
| `0.1.x` community alpha | Security feedback accepted. Not recommended for unattended production blocking. |

## Current Community Security Posture

- Local CLI execution.
- No telemetry.
- No vendor callback.
- No LLM in the final authorization path.
- No source-code egress by default.
- CARs store metadata, evidence states, hashes/references, policy trace, and verdict trace.
- CARs should not contain raw source code, raw diffs, secrets, tokens, private keys, or credentials.
- CAR integrity uses verifier-checked SHA-256 content hashes in community alpha.

## Current Security Limits

- CARs are not cryptographically signed yet.
- Public release artifacts are not signed yet.
- SBOM/provenance generation is planned for release hardening.
- GitHub Action validation has coverage for sample allow, observe, and configured-block paths.
- Production deployment hardening is not part of the community alpha.

## Reporting Security Issues

For now, open a GitHub issue that asks for a secure maintainer contact without including exploit details, sensitive logs, or proof-of-concept payloads. If GitHub Security Advisories are enabled for the repository, use that channel instead.

The project should publish a dedicated security contact, advisory publication process, expected triage response windows, and coordinated disclosure expectations before any production deployment claim.

Do not disclose suspected vulnerabilities publicly before the maintainer has a chance to investigate and prepare a fix.

## Sensitive Data Rules

Do not include any of the following in issues, sample CARs, policies, evidence files, logs, screenshots, or support material:

- secrets;
- tokens;
- private keys;
- customer production data;
- raw proprietary source code;
- raw diffs from restricted repositories;
- unredacted scanner payloads that contain private content.

## Safe Claims

CertaMerge may claim:

- It provides machine-checkable evidence for software change authorization.
- It may support review, audit, and change-control workflows.
- It can detect missing proof, failed proof, stale proof, malformed proof, and conflicting proof in supported evidence paths.

CertaMerge must not claim:

- It makes code secure.
- It guarantees production safety.
- It certifies compliance.
- It replaces scanners or security review.
- It cryptographically signs CARs in community alpha.

## Maintainer Security Checklist Before Public Release

- Publish security contact.
- Finalize vulnerability disclosure workflow.
- Add dependency/license audit command to release process.
- Generate SBOM for release artifacts.
- Publish checksums for release artifacts.
- Decide release signing method.
- Keep advanced enterprise-only code and docs out of the community repository unless explicitly approved for public release.
