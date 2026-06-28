# CGF-WTH Open-Source Results

Generated: `2026-06-28T05:34:45Z`

Score: `4.0`

Verdict: `final-alpha-ready`

## Workflow Checks

| Workflow | Passed | Severity | Readiness | Evidence |
|---|---:|---|---|---|
| install from repo | `True` | `critical` | `ready` | Obtaining file:///<repo>   Installing build dependencies: started   Installing build dependencies: finished with status 'done'   Checking if build backend supports build_editable: started   Checking if build backend supports build_editable: |
| CLI help | `True` | `critical` | `ready` | Usage: python -m certamerge [OPTIONS] COMMAND [ARGS]...                                                                                                        +- Options -------------------------------------------------------------------+ \ |
| recover | `True` | `high` | `ready` | Verdict: NEEDS_EVIDENCE Policy reason: Recover checks repo-adaptive proof signals without claiming security correctness. Repo profile: python-library Ecosystems: docs, python Missing proof: sarif_scan Accountable next action: repo-owner - R |
| recover --json | `True` | `critical` | `ready` | {   "snapshot_version": "0.1",   "repo": "<repo>",   "project_type": "python-library",   "signals": {     "package_manager_files": [       "pyproject.toml"     ],     "test_scripts": [],     "test_script_state": "missing",     "test_source_ |
| recover --json parses | `True` | `critical` | `ready` | {"missing_proof": [{"evidence_id": "ev_sarif_scan", "normalized_type": "sarif_scan", "proof_id": "mp_recover_sarif_scan", "reason": "Code repositories should attach scanner evidence when moving toward protected change authorization.", "stat |
| recover --suggest-policy | `True` | `high` | `ready` | Verdict: NEEDS_EVIDENCE Policy reason: Recover checks repo-adaptive proof signals without claiming security correctness. Repo profile: python-library Ecosystems: docs, python Missing proof: sarif_scan Accountable next action: repo-owner - R |
| suggest-policy --output | `True` | `high` | `ready` | Suggested policy: <repo>\.tmp\cgf-wth\self.suggested.certamerge.yml |
| gate with repo snapshot | `True` | `critical` | `ready` | Verdict: OBSERVE_ONLY_WOULD_ALLOW Policy reason: All matched policy requirements are satisfied. Missing proof: No missing proof required by current policy. Accountable next action: repo-owner - Proceed with record. CAR: <repo>\.tmp\cgf-wth\ |
| repo snapshot CAR file | `True` | `high` | `ready` | path=<repo>\.tmp\cgf-wth\self.repo-snapshot.car.json; missing_keys=[] |
| gate with --changed-files | `True` | `critical` | `ready` | Verdict: OBSERVE_ONLY_WOULD_ALLOW Policy reason: All matched policy requirements are satisfied. Missing proof: No missing proof required by current policy. Accountable next action: repo-owner - Proceed with record. CAR: <repo>\.tmp\cgf-wth\ |
| changed-files CAR records explicit scope | `True` | `high` | `ready` | {"base_ref": "unavailable", "base_sha": "unavailable", "branch": "grand-finale/open-source-workflow-hardening", "change_context_mode": "explicit_changed_files", "change_id": "local_repo_snapshot", "change_type": "repo_snapshot", "changed_fi |
| gate with --base/--head | `True` | `high` | `ready` | Verdict: OBSERVE_ONLY_WOULD_ALLOW Policy reason: All matched policy requirements are satisfied. Missing proof: No missing proof required by current policy. Accountable next action: repo-owner - Proceed with record. CAR: <repo>\.tmp\cgf-wth\ |
| gate --json | `True` | `critical` | `ready` | {   "verdict": "OBSERVE_ONLY_WOULD_ALLOW",   "policy_reason": "All matched policy requirements are satisfied.",   "missing_proof": [],   "accountable_next_action": {     "owner": "repo-owner",     "action": "Proceed with record."   },   "ca |
| gate --json parses | `True` | `critical` | `ready` | {"policy_reason": "All matched policy requirements are satisfied.", "verdict": "OBSERVE_ONLY_WOULD_ALLOW"} |
| verify-car | `True` | `critical` | `ready` | {   "valid": true,   "errors": [],   "warnings": [],   "car_id": "car_certamerge-open-source_16daf42acb",   "verdict": "OBSERVE_ONLY_WOULD_ALLOW" } |
| explain-car | `True` | `high` | `ready` | CAR: car_certamerge-open-source_16daf42acb Verdict: OBSERVE_ONLY_WOULD_ALLOW Policy reason: All matched policy requirements are satisfied. Missing proof: No missing proof required by current policy. Accountable next action: repo-owner - Pro |
| explain-car --json | `True` | `critical` | `ready` | {   "car_id": "car_certamerge-open-source_16daf42acb",   "verdict": "OBSERVE_ONLY_WOULD_ALLOW",   "policy_reason": "All matched policy requirements are satisfied.",   "missing_proof": [],   "accountable_next_action": {     "owner": "repo-ow |
| explain-car --json parses | `True` | `critical` | `ready` | {"car_id": "car_certamerge-open-source_16daf42acb", "errors": [], "valid": true, "verdict": "OBSERVE_ONLY_WOULD_ALLOW", "warnings": []} |
| archetype recover --json: python-library | `True` | `high` | `ready` | {   "snapshot_version": "0.1",   "repo": "<repo>\\samples\\repos\\archetypes\\python-library",   "project_type": "python-library",   "signals": {     "package_manager_files": [       "pyproject.toml"     ],     "test_scripts": [],     "test |
| archetype recover parses: python-library | `True` | `high` | `ready` | {"project_type": "python-library", "verdict": "NEEDS_EVIDENCE"} |
| archetype suggest-policy: python-library | `True` | `high` | `ready` | Suggested policy: <repo>\.tmp\cgf-wth\python-library.policy.yml |
| archetype gate: python-library | `True` | `critical` | `ready` | Verdict: OBSERVE_ONLY_WOULD_BLOCK Policy reason: Public Python library metadata requires security and license proof.; Python library code changes require test, CI, and dependency evidence. Missing proof: tests, dependency_reference, securit |
| archetype verify-car: python-library | `True` | `critical` | `ready` | {   "valid": true,   "errors": [],   "warnings": [],   "car_id": "car_python-library_364f14987e",   "verdict": "OBSERVE_ONLY_WOULD_BLOCK" } |
| archetype explain-car --json: python-library | `True` | `high` | `ready` | {   "car_id": "car_python-library_364f14987e",   "verdict": "OBSERVE_ONLY_WOULD_BLOCK",   "policy_reason": "Public Python library metadata requires security and license proof.; Python library code changes require test, CI, and dependency ev |
| archetype explain JSON parses: python-library | `True` | `high` | `ready` | {"car_id": "car_python-library_364f14987e", "errors": [], "valid": true, "verdict": "OBSERVE_ONLY_WOULD_BLOCK", "warnings": []} |
| archetype recover --json: node-typescript-app | `True` | `high` | `ready` | {   "snapshot_version": "0.1",   "repo": "<repo>\\samples\\repos\\archetypes\\node-typescript-app",   "project_type": "node-typescript-app",   "signals": {     "package_manager_files": [       "package.json"     ],     "test_scripts": [     |
| archetype recover parses: node-typescript-app | `True` | `high` | `ready` | {"project_type": "node-typescript-app", "verdict": "NEEDS_EVIDENCE"} |
| archetype suggest-policy: node-typescript-app | `True` | `high` | `ready` | Suggested policy: <repo>\.tmp\cgf-wth\node-typescript-app.policy.yml |
| archetype gate: node-typescript-app | `True` | `critical` | `ready` | Verdict: OBSERVE_ONLY_WOULD_BLOCK Policy reason: Sensitive app surfaces require owner approval and scanner evidence. Missing proof: owner_approval, sarif_scan Accountable next action: policy-owner - Supply missing proof or complete repair m |
| archetype verify-car: node-typescript-app | `True` | `critical` | `ready` | {   "valid": true,   "errors": [],   "warnings": [],   "car_id": "car_node-typescript-app_efc8a703df",   "verdict": "OBSERVE_ONLY_WOULD_BLOCK" } |
| archetype explain-car --json: node-typescript-app | `True` | `high` | `ready` | {   "car_id": "car_node-typescript-app_efc8a703df",   "verdict": "OBSERVE_ONLY_WOULD_BLOCK",   "policy_reason": "Sensitive app surfaces require owner approval and scanner evidence.",   "missing_proof": [     {       "proof_id": "mp_NODE-APP |
| archetype explain JSON parses: node-typescript-app | `True` | `high` | `ready` | {"car_id": "car_node-typescript-app_efc8a703df", "errors": [], "valid": true, "verdict": "OBSERVE_ONLY_WOULD_BLOCK", "warnings": []} |
| archetype recover --json: github-action-repo | `True` | `high` | `ready` | {   "snapshot_version": "0.1",   "repo": "<repo>\\samples\\repos\\archetypes\\github-action-repo",   "project_type": "github-action-repo",   "signals": {     "package_manager_files": [],     "test_scripts": [],     "test_script_state": "mis |
| archetype recover parses: github-action-repo | `True` | `high` | `ready` | {"project_type": "github-action-repo", "verdict": "NEEDS_EVIDENCE"} |
| archetype suggest-policy: github-action-repo | `True` | `high` | `ready` | Suggested policy: <repo>\.tmp\cgf-wth\github-action-repo.policy.yml |
| archetype gate: github-action-repo | `True` | `critical` | `ready` | Verdict: OBSERVE_ONLY_WOULD_BLOCK Policy reason: GitHub Action changes require tests, workflow validation, action contract validation, and CAR verification. Missing proof: tests, workflow_validation, action_contract_validation, car_verifica |
| archetype verify-car: github-action-repo | `True` | `critical` | `ready` | {   "valid": true,   "errors": [],   "warnings": [],   "car_id": "car_github-action-repo_96f19e9ff5",   "verdict": "OBSERVE_ONLY_WOULD_BLOCK" } |
| archetype explain-car --json: github-action-repo | `True` | `high` | `ready` | {   "car_id": "car_github-action-repo_96f19e9ff5",   "verdict": "OBSERVE_ONLY_WOULD_BLOCK",   "policy_reason": "GitHub Action changes require tests, workflow validation, action contract validation, and CAR verification.",   "missing_proof": |
| archetype explain JSON parses: github-action-repo | `True` | `high` | `ready` | {"car_id": "car_github-action-repo_96f19e9ff5", "errors": [], "valid": true, "verdict": "OBSERVE_ONLY_WOULD_BLOCK", "warnings": []} |
| archetype recover --json: terraform-iac-repo | `True` | `high` | `ready` | {   "snapshot_version": "0.1",   "repo": "<repo>\\samples\\repos\\archetypes\\terraform-iac-repo",   "project_type": "terraform-iac-repo",   "signals": {     "package_manager_files": [],     "test_scripts": [],     "test_script_state": "mis |
| archetype recover parses: terraform-iac-repo | `True` | `high` | `ready` | {"project_type": "terraform-iac-repo", "verdict": "NEEDS_EVIDENCE"} |
| archetype suggest-policy: terraform-iac-repo | `True` | `high` | `ready` | Suggested policy: <repo>\.tmp\cgf-wth\terraform-iac-repo.policy.yml |
| archetype gate: terraform-iac-repo | `True` | `critical` | `ready` | Verdict: OBSERVE_ONLY_WOULD_BLOCK Policy reason: Terraform/IaC changes require validation, plan evidence, and owner approval. Missing proof: terraform_validation, terraform_plan, owner_approval Accountable next action: policy-owner - Supply |
| archetype verify-car: terraform-iac-repo | `True` | `critical` | `ready` | {   "valid": true,   "errors": [],   "warnings": [],   "car_id": "car_terraform-iac-repo_f5e8f738ce",   "verdict": "OBSERVE_ONLY_WOULD_BLOCK" } |
| archetype explain-car --json: terraform-iac-repo | `True` | `high` | `ready` | {   "car_id": "car_terraform-iac-repo_f5e8f738ce",   "verdict": "OBSERVE_ONLY_WOULD_BLOCK",   "policy_reason": "Terraform/IaC changes require validation, plan evidence, and owner approval.",   "missing_proof": [     {       "proof_id": "mp_ |
| archetype explain JSON parses: terraform-iac-repo | `True` | `high` | `ready` | {"car_id": "car_terraform-iac-repo_f5e8f738ce", "errors": [], "valid": true, "verdict": "OBSERVE_ONLY_WOULD_BLOCK", "warnings": []} |
| archetype recover --json: monorepo-app | `True` | `high` | `ready` | {   "snapshot_version": "0.1",   "repo": "<repo>\\samples\\repos\\archetypes\\monorepo-app",   "project_type": "monorepo-app",   "signals": {     "package_manager_files": [       "package.json"     ],     "test_scripts": [       "package.js |
| archetype recover parses: monorepo-app | `True` | `high` | `ready` | {"project_type": "monorepo-app", "verdict": "NEEDS_EVIDENCE"} |
| archetype suggest-policy: monorepo-app | `True` | `high` | `ready` | Suggested policy: <repo>\.tmp\cgf-wth\monorepo-app.policy.yml |
| archetype gate: monorepo-app | `True` | `critical` | `ready` | Verdict: OBSERVE_ONLY_WOULD_BLOCK Policy reason: Monorepo scoped changes require ownership evidence. Missing proof: owner_approval Accountable next action: policy-owner - Supply missing proof or complete repair missions, then rerun CertaMer |
| archetype verify-car: monorepo-app | `True` | `critical` | `ready` | {   "valid": true,   "errors": [],   "warnings": [],   "car_id": "car_monorepo-app_03b562fcab",   "verdict": "OBSERVE_ONLY_WOULD_BLOCK" } |
| archetype explain-car --json: monorepo-app | `True` | `high` | `ready` | {   "car_id": "car_monorepo-app_03b562fcab",   "verdict": "OBSERVE_ONLY_WOULD_BLOCK",   "policy_reason": "Monorepo scoped changes require ownership evidence.",   "missing_proof": [     {       "proof_id": "mp_MONOREPO-OWNERS-002_owner_appro |
| archetype explain JSON parses: monorepo-app | `True` | `high` | `ready` | {"car_id": "car_monorepo-app_03b562fcab", "errors": [], "valid": true, "verdict": "OBSERVE_ONLY_WOULD_BLOCK", "warnings": []} |
| archetype recover --json: docs-heavy-repo | `True` | `high` | `ready` | {   "snapshot_version": "0.1",   "repo": "<repo>\\samples\\repos\\archetypes\\docs-heavy-repo",   "project_type": "docs-heavy-repo",   "signals": {     "package_manager_files": [],     "test_scripts": [],     "test_script_state": "missing", |
| archetype recover parses: docs-heavy-repo | `True` | `high` | `ready` | {"project_type": "docs-heavy-repo", "verdict": "NEEDS_EVIDENCE"} |
| archetype suggest-policy: docs-heavy-repo | `True` | `high` | `ready` | Suggested policy: <repo>\.tmp\cgf-wth\docs-heavy-repo.policy.yml |
| archetype gate: docs-heavy-repo | `True` | `critical` | `ready` | Verdict: OBSERVE_ONLY_WOULD_BLOCK Policy reason: Docs-heavy repositories require docs build, link validation, and safe public-claims review. Missing proof: links_valid, compliance_safe_language Accountable next action: policy-owner - Supply |
| archetype verify-car: docs-heavy-repo | `True` | `critical` | `ready` | {   "valid": true,   "errors": [],   "warnings": [],   "car_id": "car_docs-heavy-repo_522d4480e8",   "verdict": "OBSERVE_ONLY_WOULD_BLOCK" } |
| archetype explain-car --json: docs-heavy-repo | `True` | `high` | `ready` | {   "car_id": "car_docs-heavy-repo_522d4480e8",   "verdict": "OBSERVE_ONLY_WOULD_BLOCK",   "policy_reason": "Docs-heavy repositories require docs build, link validation, and safe public-claims review.",   "missing_proof": [     {       "pro |
| archetype explain JSON parses: docs-heavy-repo | `True` | `high` | `ready` | {"car_id": "car_docs-heavy-repo_522d4480e8", "errors": [], "valid": true, "verdict": "OBSERVE_ONLY_WOULD_BLOCK", "warnings": []} |
| CAR integrity mutation checks | `True` | `critical` | `ready` | {   "valid": false,   "errors": [     "CAR integrity content_hash does not match canonical CAR content."   ],   "warnings": [],   "car_id": "car_certamerge-open-source_16daf42acb",   "verdict": "BLOCK" } |
| GitHub Action proof gate | `True` | `high` | `ready` | action.yml gate invocation and fail behavior |
| GitHub Action artifact upload | `True` | `medium` | `ready` | action.yml artifact upload |
| GitHub Action summary | `True` | `medium` | `ready` | action.yml summary generation |
| sample CAR verification | `True` | `medium` | `ready` | [{"returncode": 0, "sample": "allow.example.json", "valid_text": true}, {"returncode": 0, "sample": "block.example.json", "valid_text": true}, {"returncode": 0, "sample": "needs-evidence.example.json", "valid_text": true}, {"returncode": 0, |
| README professional contract | `True` | `high` | `ready` | missing_sections=[] |
| README first-screen positioning | `True` | `high` | `ready` | missing_phrases=[] |
| agent workflow | `True` | `high` | `ready` | docs/community/agent-workflow.md |
| human quickstart | `True` | `high` | `ready` | docs/community/quickstart.md |
| 5-minute demo | `True` | `medium` | `ready` | docs/demo/5_MINUTE_PUBLIC_ALPHA_DEMO.md |
| no-source-egress posture | `True` | `high` | `ready` | docs/community/no-source-egress.md |
| local-path leakage scan | `True` | `critical` | `ready` |  |
| secret-looking string scan | `True` | `critical` | `ready` |  |
| safe-language scan | `True` | `critical` | `ready` |  |
| public/private leakage scan | `True` | `critical` | `ready` |  |
| pytest | `True` | `critical` | `ready` | ........................................................................ [ 26%] ........................................................................ [ 53%] ........................................................................ [ 80%]  |
| pytest collect-only | `True` | `high` | `ready` | community/tests/test_community_core.py::test_recover_detects_missing_proof_in_no_ci_repo community/tests/test_community_core.py::test_gate_blocks_auth_change_in_observe_language community/tests/test_community_core.py::test_gate_allows_payme |
| compileall | `True` | `high` | `ready` | Listing 'community'... Listing 'community\\cli'... Listing 'community\\cli\\certamerge'... Listing 'community\\cli\\certamerge.egg-info'... Listing 'community\\github-action'... Listing 'community\\policies'... Listing 'community\\tests'... |
| release build | `True` | `high` | `ready` | running egg_info writing community/cli\certamerge.egg-info\PKG-INFO writing dependency_links to community/cli\certamerge.egg-info\dependency_links.txt writing entry points to community/cli\certamerge.egg-info\entry_points.txt writing requir |
| twine check | `True` | `high` | `ready` | Checking dist\certamerge-0.1.0-py3-none-any.whl: PASSED Checking dist\certamerge-0.1.0.tar.gz: PASSED |
| checksum generation | `True` | `high` | `ready` | eb799e3bf0f804da58c1188a7dfbdf583317eba4d523d7bb584d356d4b40b92a  dist/certamerge-0.1.0-py3-none-any.whl 0000cfd49e58e171c467ba9849f6061e2fb1cc034b6598d63e4c366c3fb2bc2d  dist/certamerge-0.1.0.tar.gz |

## Critical And High Failures

No critical or high CGF-WTH failures recorded.

## Final Verdict

```text
CERTAMERGE OPEN SOURCE GRAND FINALE READY FOR V0.1.0-ALPHA
```
