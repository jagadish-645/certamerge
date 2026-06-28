# Public Repository Boundary

CertaMerge's public repository is the community alpha product surface.

It should help a developer, maintainer, coding agent, or reviewer install the CLI, run Recover, run proof-only Gate, verify a CAR, understand the specs, try sample repos, and use the GitHub Action wrapper.

## Belongs Here

- Community CLI source and tests.
- CAR, evidence, policy, verdict, and repair mission specs.
- Sample repos, sample policies, sample evidence, and sample CARs.
- Community docs for Recover, Gate, CAR verification, evidence adapters, no-source-egress behavior, and agent JSON workflows.
- Public release notes, checksums, verification steps, and honest alpha limitations.
- GitHub Action wrapper and workflow examples that a public repo maintainer can copy.

## Does Not Belong Here

- Enterprise runtime code or enterprise-only command surfaces.
- Organization-wide policy governance, segregation-of-duties runtime, ProofGraph memory, audit export, support bundle generation, or design-partner pilot packets.
- Local workspace notes, agent-system playbooks, private architecture plans, builder loop logs, cleanup reports, internal readiness reports, or research artifacts.
- Founder strategy, acquisition strategy, pricing strategy, or private validation notes.
- Raw customer source code, raw diffs, secrets, private keys, proprietary scanner payloads, or production customer data.

## Where Excluded Material Belongs

| Material | Home |
|---|---|
| Open-source product code, public specs, samples, community docs | Public `certamerge` repo |
| Enterprise pilot runtime, paid-tier workflows, private buyer-facing controls | Private enterprise repo |
| Agent instructions, governance gates, build history, audit notes, local validation reports | Private local/root workspace |
| Temporary command output, CARs from local proof runs, build caches | Ignored `.tmp/`, `dist/`, or local workspace folders |

The public repo should read like a product someone can clone and use, not like a dumped builder workspace.
