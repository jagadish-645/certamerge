# Evolutionary Improvement Loop Log

## Loop 1

### Failures Found

- Self-dogfood `recover .` initially classified the CertaMerge root repository as `terraform-iac-repo` because bundled sample fixtures under `samples/repos/archetypes/` included Terraform files.
- Sample CAR fixtures contained absolute local Windows paths in `change.source_ref`.
- GitHub Action summary copied raw CLI output instead of producing a reviewer-native proof summary.
- Evidence parser distinguished malformed/stale/failed/negative/conflicting states, but explicit unavailable evidence could collapse into insufficient evidence.

### Fixes Made

- Added repo profile filtering so bundled samples and demo docs do not dominate root repository project-type or risk-surface inference.
- Sanitized sample CAR fixture paths and recalculated CAR content hashes.
- Added change-bound CAR metadata:
  - Git/GitHub context when available;
  - policy source hash;
  - evidence artifact hashes;
  - replay change binding.
- Added verifier checks for policy file hash and evidence artifact hash integrity.
- Added explicit unavailable evidence handling for test and owner approval evidence.
- Reworked the composite GitHub Action summary to render from the CAR:
  - verdict;
  - policy reason;
  - matched rules;
  - evidence states;
  - missing proof;
  - accountable next action;
  - CAR artifact;
  - verification command.
- Added docs and reports for change-bound proof, evidence ingestion, action summary, professional hardening, and wrapper-kill validation.

### Tests Run

Focused tests:

```text
python -m pytest community/tests/test_controlled_alpha_contracts.py -q
127 passed
```

Evidence-state tests:

```text
python -m pytest community/tests/test_evidence_state_contract.py community/tests/test_controlled_alpha_contracts.py -q
129 passed
```

Public/action contract tests:

```text
python -m pytest community/tests/test_public_release_candidate_contracts.py community/tests/test_controlled_alpha_contracts.py -q
227 passed
```

Full suite during this loop:

```text
python -m pytest -q
238 passed
```

### CertaMerge Self-Verdict

Recover:

```text
Verdict: NEEDS_EVIDENCE
Repo profile: python-library
Missing proof: sarif_scan
```

Gate:

```text
Verdict: OBSERVE_ONLY_WOULD_ALLOW
Policy reason: All matched policy requirements are satisfied.
CAR verification: valid
```

### Archetype Validation Score

Wrapper-kill validation:

```text
6 of 6 archetypes produced useful Recover output.
6 of 6 archetypes produced repo-specific starter policies.
6 of 6 archetypes produced sane Gate missing-proof output.
6 of 6 generated CARs verified.
```

Result:

```text
CERTAMERGE IS MORE THAN A TEMPLATE
```

### Remaining Weaknesses

- CertaMerge still evaluates repo snapshots, not true PR diffs.
- Community CARs are hash-bound and change-bound but not cryptographically signed.
- JUnit XML, Terraform plan JSON, SBOM parsing, and scanner adapter depth remain limited.
- Live GitHub Actions validation still needs to run after the branch is pushed.
- Recover should better explain test-source presence versus passing test-result evidence.

### Decision

Stop the improvement loop early and move to PR readiness because:

- wrapper-kill validation passes;
- focused tests pass;
- full tests pass;
- self-dogfood Gate passes;
- GitHub Action summary is materially more useful;
- no critical public residue remains after hardening.

