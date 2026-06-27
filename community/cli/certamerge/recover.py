from __future__ import annotations

from pathlib import Path
from typing import Any

from .car import base_car
from .evidence import detect_signals, evidence_from_signals, evidence_for_required, missing_proof_from_evidence
from .repair import repair_missions_for_missing
from .risk import detect_project_type, detect_risk_surfaces, iter_repo_files, profile_signal_files


def _state(required: str, snapshot: dict[str, Any]) -> str:
    item = evidence_for_required(required, snapshot)
    return str(item.get("state")) if item else "missing"


def _gap(required: str, reason: str, snapshot: dict[str, Any]) -> dict[str, Any]:
    item = evidence_for_required(required, snapshot)
    return {
        "proof_id": f"mp_recover_{required}",
        "type": required,
        "normalized_type": required,
        "state": item.get("state") if item else "missing",
        "reason": reason,
        "evidence_id": item.get("evidence_id") if item else "",
    }


def repo_profile_from_signals(project_type: str, signals: dict[str, Any], risk_surfaces: list[str]) -> dict[str, Any]:
    ecosystems: list[str] = []
    package_files = set(signals.get("package_manager_files", []))
    if "pyproject.toml" in package_files or "requirements.txt" in package_files:
        ecosystems.append("python")
    if "package.json" in package_files:
        ecosystems.append("node")
    if "go.mod" in package_files:
        ecosystems.append("go")
    if signals.get("terraform_refs"):
        ecosystems.append("terraform")
    if signals.get("action_metadata_refs"):
        ecosystems.append("github-actions")
    if signals.get("docs_refs"):
        ecosystems.append("docs")

    indicators = {
        "ci": "present" if signals.get("ci_configs") else "missing",
        "tests": "present" if signals.get("test_scripts") or signals.get("test_source_refs") else "missing",
        "lockfile": "present" if signals.get("lockfiles") else "missing",
        "security_policy": "present" if signals.get("security") else "missing",
        "license": "present" if signals.get("license_refs") else "missing",
        "codeowners": "present" if signals.get("codeowners_refs") else "missing",
        "pull_request_template": "present" if signals.get("pr_template_refs") else "missing",
        "issue_templates": "present" if signals.get("issue_template_refs") else "missing",
        "github_action": "present" if signals.get("action_metadata_refs") else "missing",
        "scanner_evidence": "present" if signals.get("sarif_files") else "missing",
        "iac": "present" if signals.get("terraform_refs") else "missing",
        "docs": "present" if signals.get("docs_refs") else "missing",
        "docs_build": "present" if signals.get("docs_build_refs") else "missing",
    }
    return {
        "type": project_type,
        "ecosystems": sorted(set(ecosystems)) or ["unknown"],
        "indicators": indicators,
        "risk_surfaces": risk_surfaces,
    }


def adaptive_missing_proof(snapshot: dict[str, Any], profile: dict[str, Any]) -> list[dict[str, Any]]:
    project_type = profile["type"]
    ecosystems = set(profile["ecosystems"])
    risk_surfaces = set(profile["risk_surfaces"])
    required: list[tuple[str, str]] = []

    if "python" in ecosystems or "node" in ecosystems or project_type in {"python-library", "node-typescript-app", "monorepo-app"}:
        required.extend(
            [
                ("test_result", "Code/application repositories should expose test command or test result proof."),
                ("ci_status", "Code/application repositories should expose CI workflow proof."),
                ("dependency_reference", "Package-managed repositories should expose lockfile, SBOM, or dependency review evidence."),
                ("security_doc", "Public code repositories should document security reporting and supported security expectations."),
                ("license_file", "Public code repositories should include an explicit license file."),
                ("sarif_scan", "Code repositories should attach scanner evidence when moving toward protected change authorization."),
            ]
        )

    if project_type == "github-action-repo":
        required.extend(
            [
                ("action_metadata", "GitHub Action repositories must expose action metadata."),
                ("workflow_validation", "GitHub Action repositories should prove workflow validation."),
                ("action_contract_validation", "GitHub Action repositories should validate action inputs and outputs."),
                ("car_verification", "Action changes should prove generated CARs can be verified."),
            ]
        )

    if project_type == "terraform-iac-repo" or "iac" in risk_surfaces:
        required.extend(
            [
                ("terraform_validation", "Terraform/IaC repositories should attach terraform validation proof."),
                ("terraform_plan", "Terraform/IaC repositories should attach plan evidence before approval."),
                ("owner_approval", "Infrastructure changes require accountable owner approval evidence."),
                ("security_doc", "Infrastructure repositories should document security reporting and handling boundaries."),
            ]
        )

    if project_type == "docs-heavy-repo" or (project_type == "unknown" and "docs" in ecosystems):
        required.extend(
            [
                ("docs_build", "Docs-heavy repositories should prove docs build or static-site validation."),
                ("links_valid", "Docs-heavy repositories should attach link validation evidence."),
                ("compliance_safe_language", "Public docs should prove unsafe security/compliance claims were reviewed."),
            ]
        )

    if "auth" in risk_surfaces or "payments" in risk_surfaces or "database" in risk_surfaces:
        required.append(("owner_approval", "Sensitive code paths require accountable owner approval evidence."))

    gaps = []
    seen: set[str] = set()
    for evidence_type, reason in required:
        if evidence_type in seen:
            continue
        seen.add(evidence_type)
        if _state(evidence_type, snapshot) not in {"present", "negative"}:
            gaps.append(_gap(evidence_type, reason, snapshot))
    return gaps


def suggested_policy_for_profile(profile: dict[str, Any]) -> dict[str, Any]:
    project_type = profile["type"]
    rules: list[dict[str, Any]] = []

    def add_rule(rule_id: str, paths: list[str], evidence: list[str], reason: str, verdict: str = "NEEDS_EVIDENCE", severity: str = "medium") -> None:
        rules.append(
            {
                "id": rule_id,
                "when": {"paths": paths},
                "require": {"evidence": evidence},
                "verdict_if_missing": verdict,
                "severity": severity,
                "reason": reason,
            }
        )

    if project_type == "python-library":
        add_rule("PY-LIB-CODE-001", ["src/**", "tests/**", "pyproject.toml"], ["tests", "ci_status", "dependency_reference"], "Python library code changes require test, CI, and dependency evidence.")
        add_rule("PY-LIB-PUBLIC-002", ["README.md", "SECURITY.md", "LICENSE"], ["security_doc", "license_file"], "Public Python library metadata requires security and license proof.")
    elif project_type == "node-typescript-app":
        add_rule("NODE-APP-CODE-001", ["src/**", "tests/**", "__tests__/**", "package.json"], ["tests", "ci_status", "dependency_reference"], "Node/TypeScript app changes require tests, CI, and dependency evidence.")
        add_rule("NODE-APP-RISK-002", ["src/auth/**", "src/payments/**", "src/database/**"], ["owner_approval", "sarif_scan"], "Sensitive app surfaces require owner approval and scanner evidence.", "ESCALATE", "high")
    elif project_type == "github-action-repo":
        add_rule("ACTION-CONTRACT-001", ["action.yml", "action.yaml", "src/**", "scripts/**"], ["tests", "ci_status", "workflow_validation", "action_contract_validation", "car_verification"], "GitHub Action changes require tests, workflow validation, action contract validation, and CAR verification.", "NEEDS_EVIDENCE", "high")
    elif project_type == "terraform-iac-repo":
        add_rule("IAC-TERRAFORM-001", ["*.tf", "**/*.tf", "*.tfvars", "**/*.tfvars"], ["terraform_validation", "terraform_plan", "owner_approval"], "Terraform/IaC changes require validation, plan evidence, and owner approval.", "ESCALATE", "high")
    elif project_type == "monorepo-app":
        add_rule("MONOREPO-APPS-001", ["apps/**", "packages/**"], ["tests", "ci_status", "dependency_reference"], "Monorepo application/package changes require tests, CI, and dependency evidence.")
        add_rule("MONOREPO-OWNERS-002", ["apps/**", "packages/**", "CODEOWNERS"], ["codeowners", "owner_approval"], "Monorepo scoped changes require ownership evidence.", "NEEDS_EVIDENCE", "high")
    elif project_type == "docs-heavy-repo":
        add_rule("DOCS-PUBLIC-001", ["README.md", "docs/**", "mkdocs.yml"], ["docs_build", "links_valid", "compliance_safe_language"], "Docs-heavy repositories require docs build, link validation, and safe public-claims review.")
    else:
        add_rule("GENERIC-REPO-001", ["**"], ["tests", "ci_status", "security_doc"], "Generic repositories require basic test, CI, and security documentation proof.")

    return {"version": 0.1, "mode": "observe", "rules": rules}


def recover_repo(repo: Path) -> dict[str, Any]:
    repo = repo.resolve()
    files = iter_repo_files(repo)
    profile_files = profile_signal_files(files)
    project_type = detect_project_type(profile_files)
    signals = detect_signals(repo, profile_files)
    risk_surfaces = detect_risk_surfaces(profile_files)
    evidence = evidence_from_signals(repo, signals)
    evidence_snapshot = {"evidence": evidence}
    profile = repo_profile_from_signals(project_type, signals, risk_surfaces)
    missing = missing_proof_from_evidence(evidence, risk_surfaces)
    if project_type == "docs-heavy-repo":
        missing = [item for item in missing if item["type"] not in {"test_result", "owner_approval"}]
    if project_type == "terraform-iac-repo":
        missing = [item for item in missing if item["type"] != "test_result"]
    for gap in adaptive_missing_proof(evidence_snapshot, profile):
        if not any(item["type"] == gap["type"] for item in missing):
            missing.append(gap)
    missions = repair_missions_for_missing(missing, risk_surfaces)
    verdict = "NEEDS_EVIDENCE" if missing else "ALLOW"
    policy = {
        "policy_id": "recover-default",
        "policy_version": "0.1",
        "mode": "observe",
        "policy_hash": "sha256:recover-default",
    }
    car = base_car(
        repo=repo,
        verdict_state=verdict,
        policy_reason="Recover checks repo-adaptive proof signals without claiming security correctness.",
        enforcement_effect="observe_only",
        risk_surfaces=risk_surfaces,
        evidence=evidence,
        missing_proof=missing,
        repair_missions=missions,
        verdict_trace=[
            {
                "rule_id": "RECOVER-BASIC-001",
                "result": "missing_evidence" if missing else "satisfied",
                "evidence_refs": [item["evidence_id"] for item in evidence],
            }
        ],
        policy=policy,
        owner="repo-owner",
        next_action="Review missing proof and complete repair missions before relying on this repo for production.",
        record_state="pending" if missing else "final",
    )
    return {
        "snapshot_version": "0.1",
        "repo": str(repo),
        "project_type": project_type,
        "signals": signals,
        "profile": profile,
        "risk_surfaces": risk_surfaces,
        "evidence": evidence,
        "missing_proof": missing,
        "repair_missions": missions,
        "suggested_policy": suggested_policy_for_profile(profile),
        "verdict": verdict,
        "car": car,
    }
