# CertaMerge Open-Core Boundary v0.1

## Purpose

This boundary keeps the community product genuinely useful while preserving real enterprise value. CertaMerge must earn developer trust in the open and earn enterprise money through governance, memory, scale, self-hosted operations, and support.

## Boundary Laws

1. Community must create real proof value without procurement.
2. Enterprise must not be community plus login.
3. CAR spec and verification must be inspectable.
4. Customer-owned CARs and evidence references must remain portable.
5. Enterprise value lives in governance, retention, ProofGraph, observe replay, audit export, deployment/agent gates, advanced packs, and support.
6. Open components must not leak proprietary enterprise risk ontology or commercial pack corpus by accident.

## Objects

| Object | Meaning |
|---|---|
| Capability | Product behavior, artifact, spec, pack, service, or operational control that must be placed. |
| Placement | Community/open, shared spec, enterprise/closed, commercial service, or undecided. |
| Community artifact | Open artifact that creates useful local proof value. |
| Enterprise artifact | Paid artifact that adds governance, memory, scale, control, or support. |
| Shared spec | Inspectable contract that must remain portable across editions. |
| Boundary decision | Versioned decision explaining why a capability belongs in a placement. |
| Upgrade path | How a community user moves to enterprise without losing CARs or evidence references. |

## Boundary Record Required Fields

Each boundary decision must record:

- `capability`
- `placement`
- `reason`
- `trust_effect`
- `adoption_effect`
- `monetization_effect`
- `defensibility_effect`
- `support_burden`
- `portability_rule`
- `version`

## Boundary States

| State | Meaning |
|---|---|
| `proposed` | Boundary is drafted but not accepted. |
| `community_open` | Capability is open/community. |
| `shared_spec` | Capability is an inspectable standard or record format. |
| `enterprise_control` | Capability belongs to enterprise governance/control plane. |
| `commercial_service` | Capability is delivered as service or productized implementation. |
| `rejected` | Capability does not belong in CertaMerge. |
| `superseded` | Boundary changed in a later version. |

## Valid Transitions

| From | To | Allowed when |
|---|---|---|
| `proposed` | `community_open` | Openness increases trust/adoption without giving away enterprise control. |
| `proposed` | `shared_spec` | Portability or verification requires inspectability. |
| `proposed` | `enterprise_control` | Capability creates governance, scale, retention, memory, or support value. |
| `proposed` | `commercial_service` | Capability is high-touch but can become reusable product IP. |
| any accepted state | `superseded` | Business model, security, adoption, or customer proof changes. |
| `proposed` | `rejected` | Capability violates product doctrine or anti-slop gate. |

## Invalid Transitions

- `community_open` to `enterprise_control` if it strands existing CARs or prevents open verification.
- `shared_spec` to closed-only without a new trust decision.
- `enterprise_control` to `community_open` if it gives away the full governance/control moat without a monetization path.
- Any state to accepted if it requires source-code egress by default.
- Any state to accepted if it makes dashboards, chatbots, or scanner replacement the primary product.

## Failure States

| Failure | Required behavior |
|---|---|
| Community becomes crippleware | Move enough CAR/verifier/Recover/Gate value into open scope. |
| Enterprise becomes thin wrapper | Add governance, memory, retention, SoD, ProofGraph, audit, deployment, or support value. |
| Verifier trust is closed | Move verifier contract into open/shared spec. |
| Enterprise pack bypasses deterministic core | Reject pack until deterministic, versioned, and replayable. |
| Support burden overwhelms community | Keep advanced workflow orchestration in enterprise or service lane. |

## Capability Placement

| Capability | Community/open | Enterprise/closed or commercial | Reason |
|---|---:|---:|---|
| CAR spec | yes | yes | Trust requires inspectable records. |
| CAR verifier | yes | yes | Verification must not depend on enterprise control plane. |
| CLI | yes | yes | First value and workflow-native use. |
| Basic local evaluator | yes | yes | Developers need proof gaps quickly. |
| Local Recover | yes | advanced packs | Free emotional value and service-led wedge. |
| Proof-only Gate | yes | governed enforcement | PR value without rollout politics. |
| Basic policy format | yes | policy governance | Customers must understand proof rules. |
| Basic GitHub Action | yes | enterprise integrations | Workflow-native adoption. |
| Basic evidence adapters | yes | advanced adapters | Community can verify common proof. |
| Basic repair missions | yes | orchestration and advanced packs | Missing proof must become action. |
| Repo Proof Snapshot | yes | multi-repo retention | Free trust artifact. |
| Org-wide policy | no | yes | Governance and scale are paid value. |
| Policy inheritance | no | yes | Enterprise control. |
| Separation of duties | record shape | yes | Premium accountability. |
| ProofGraph | no | yes | Enterprise decision memory. |
| Observe-mode replay | small fixture examples | yes | Pilot and buyer value. |
| CAR retention/query | local files | yes | Enterprise audit and search. |
| Audit export bundles | basic example | yes | Buyer/CISO value and support burden. |
| Deployment gates | no | yes | Higher-value control point. |
| Agent-action gates | no | yes | Future autonomy control. |
| Advanced risk packs | no | yes | Proprietary risk ontology. |
| Advanced proof packs | no | yes | Commercial proof intelligence. |
| Advanced repair packs | no | yes | Service-to-product corpus. |
| Support/SLA | no | yes | Enterprise trust. |

## Required Community Artifacts

- `README.md`
- `LICENSE`
- `SECURITY.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- CAR spec and examples.
- Verifier.
- Recover command.
- Gate command.
- Basic policy examples.
- Basic evidence adapters.
- Repair missions.
- GitHub Action wrapper.
- Community docs.
- Community tests and sample repos.

## Required Enterprise Artifacts

- Self-hosted runtime.
- Org/workspace/repo governance.
- Policy store and versioning.
- CAR store, query, export, and retention.
- Evidence metadata store.
- ProofGraph decision memory.
- Observe-mode replay.
- SoD.
- Audit export bundle.
- Enterprise packs.
- Admin operational surface.
- Trust packet.
- Services docs.
- Enterprise tests and fixtures.

## Security And Privacy Constraints

- Community and enterprise must both default to no source-code egress.
- CARs and verifier must be usable without vendor network calls.
- Enterprise must not lock customers out of their own CARs or evidence references.
- Open examples must be sanitized and must not embed secrets or customer data.
- Closed enterprise packs must not undermine open verifier trust.

## Versioning Strategy

- Open specs use explicit versions and compatibility notes.
- Enterprise may add fields only if open verifier can safely ignore or report them.
- Breaking CAR/verifier changes require migration guidance and compatibility fixtures.
- Community-to-enterprise upgrade must preserve existing CARs.

## Acceptance Criteria

The boundary is valid if:

- community has useful first value in under five minutes;
- enterprise adds real governance and memory;
- CAR verification is open and portable;
- no-source-egress remains default in both;
- monetization does not depend on hiding proof truth from users.

## Rejection Criteria

Reject the boundary if:

- community is crippleware;
- enterprise is community plus auth;
- CAR verification requires enterprise;
- ProofGraph becomes vanity analytics or surveillance;
- advanced packs bypass deterministic verdict authority;
- users cannot export or verify their records.

## Example Boundary Record

```json
{
  "capability": "CAR verifier",
  "placement": "community_open",
  "reason": "Verification must not require trust in the enterprise control plane.",
  "trust_effect": "high",
  "adoption_effect": "high",
  "monetization_effect": "indirect enterprise upsell",
  "defensibility_effect": "proof standard ownership",
  "support_burden": "moderate",
  "portability_rule": "CARs generated by community or enterprise must be verifiable offline when required fields are present.",
  "version": "0.1"
}
```
