from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SATISFYING_EVIDENCE_STATES = {"present", "negative"}

REQUIRED_EVIDENCE_ALIASES = {
    "tests": "test_result",
    "test_result": "test_result",
    "ci": "ci_status",
    "ci_status": "ci_status",
    "lint": "lint_result",
    "lint_result": "lint_result",
    "sarif": "sarif_scan",
    "sarif_scan": "sarif_scan",
    "security_scan": "sarif_scan",
    "gitleaks": "secret_scan",
    "secret_scan": "secret_scan",
    "dependency": "dependency_reference",
    "dependency_reference": "dependency_reference",
    "sbom": "dependency_reference",
    "owner_approval": "owner_approval",
    "approval": "owner_approval",
    "github_actions_artifact": "github_actions_artifact",
    "car_verification": "car_verification",
    "no_source_egress": "no_source_egress",
    "risk_surface_classification": "risk_surface_classification",
    "workflow_validation": "workflow_validation",
    "action_contract_validation": "action_contract_validation",
    "schema_validation": "schema_validation",
    "compliance_safe_language": "compliance_safe_language",
    "no_secret_leakage": "no_secret_leakage",
    "links_valid": "links_valid",
    "license_file": "license_file",
    "codeowners": "codeowners",
    "pr_template": "pr_template",
    "issue_template": "issue_template",
    "action_metadata": "action_metadata",
    "terraform_files": "terraform_files",
    "terraform_validation": "terraform_validation",
    "terraform_plan": "terraform_plan",
    "docs_site": "docs_site",
    "docs_build": "docs_build",
}


def _read_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return None, str(exc)
    if not isinstance(data, dict):
        return None, "JSON evidence must be an object."
    return data, None


def _read_xml(path: Path) -> tuple[ET.Element | None, str | None]:
    try:
        return ET.parse(path).getroot(), None
    except (ET.ParseError, OSError, UnicodeDecodeError) as exc:
        return None, str(exc)


def _parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _package_json(repo: Path) -> dict[str, Any] | None:
    package = repo / "package.json"
    if not package.exists():
        return None
    data, _ = _read_json(package)
    return data


def package_json_has_script(repo: Path, script: str) -> bool:
    data = _package_json(repo)
    if not data:
        return False
    scripts = data.get("scripts")
    if not isinstance(scripts, dict):
        return False
    value = scripts.get(script)
    if not isinstance(value, str):
        return False
    normalized = value.strip().lower()
    if not normalized or "no test" in normalized:
        return False
    return True


def package_json_script_state(repo: Path, script: str) -> str:
    data = _package_json(repo)
    if not data:
        return "missing"
    scripts = data.get("scripts")
    if not isinstance(scripts, dict) or script not in scripts:
        return "missing"
    value = scripts.get(script)
    if not isinstance(value, str) or not value.strip():
        return "missing"
    normalized = value.lower()
    if "no test" in normalized:
        return "missing"
    if "exit 1" in normalized or "false" == normalized.strip():
        return "failed"
    return "present"


def _metadata_evidence_refs(names: list[str], *needles: str) -> list[str]:
    refs = []
    for name in names:
        normalized = name.lower().replace("_", "-")
        if name.startswith(".certamerge/evidence/") and any(needle in normalized for needle in needles):
            refs.append(name)
    return refs


def detect_signals(repo: Path, files: list[Path]) -> dict[str, Any]:
    names = [p.as_posix() for p in files]
    lower_names = {name.lower(): name for name in names}
    package = _package_json(repo) or {}
    scripts = package.get("scripts") if isinstance(package.get("scripts"), dict) else {}
    lint_refs = ["package.json:scripts.lint"] if isinstance(scripts, dict) and package_json_has_script(repo, "lint") else []
    lint_refs.extend(name for name in names if name.startswith(".eslint") or name in {"ruff.toml", "flake8"})
    test_source_refs = [
        name
        for name in names
        if name.startswith("tests/")
        or name.startswith("__tests__/")
        or "/tests/" in name
        or "/__tests__/" in name
        or name.endswith(".test.js")
        or name.endswith(".test.ts")
        or name.endswith("_test.py")
        or name.endswith("_test.go")
    ]
    docs_refs = [name for name in names if name.startswith("docs/") or name in {"README.md", "mkdocs.yml", "docusaurus.config.js"}]
    codeowners_refs = [
        name
        for name in names
        if name in {"CODEOWNERS", ".github/CODEOWNERS", "docs/CODEOWNERS"}
    ]
    pr_template_refs = [
        name
        for name in names
        if name in {"PULL_REQUEST_TEMPLATE.md", ".github/PULL_REQUEST_TEMPLATE.md"} or name.startswith(".github/PULL_REQUEST_TEMPLATE/")
    ]
    issue_template_refs = [name for name in names if name.startswith(".github/ISSUE_TEMPLATE/")]
    terraform_refs = [name for name in names if name.endswith(".tf") or name.endswith(".tfvars")]
    docs_build_refs = []
    if "mkdocs.yml" in names or "docusaurus.config.js" in names:
        docs_build_refs.append("docs-site-config")
    if isinstance(scripts, dict):
        for script_name in ("docs", "build:docs", "docs:build"):
            if package_json_has_script(repo, script_name):
                docs_build_refs.append(f"package.json:scripts.{script_name}")
    return {
        "package_manager_files": [name for name in names if name in {"package.json", "pyproject.toml", "requirements.txt", "go.mod"}],
        "test_scripts": ["package.json:scripts.test"] if package_json_has_script(repo, "test") else [],
        "test_script_state": package_json_script_state(repo, "test"),
        "test_source_refs": sorted(set(test_source_refs)),
        "ci_configs": [name for name in names if name.startswith(".github/workflows/") or name == ".gitlab-ci.yml"],
        "lockfiles": [name for name in names if name in {"package-lock.json", "pnpm-lock.yaml", "yarn.lock", "poetry.lock", "go.sum"}],
        "lint_refs": sorted(set(lint_refs)),
        "test_result_refs": [
            name
            for name in names
            if name.startswith(".certamerge/evidence/") and ("test-result" in name.lower() or "test_result" in name.lower())
        ],
        "junit_refs": [
            name
            for name in names
            if name.endswith(".xml") and ("junit" in name.lower() or "surefire-reports" in name.lower() or "test-results" in name.lower())
        ],
        "sarif_files": [name for name in names if name.endswith(".sarif") or name.endswith(".sarif.json")],
        "sbom_refs": [
            name
            for name in names
            if (name.endswith(".json") or name.endswith(".xml"))
            and ("sbom" in name.lower() or "cyclonedx" in name.lower() or name.lower().endswith("bom.json") or name.lower().endswith("bom.xml"))
        ],
        "dependency_review_refs": [
            name
            for name in names
            if name.startswith(".certamerge/evidence/")
            and "dependency" in name.lower()
            and (name.endswith(".json") or name.endswith(".xml"))
        ],
        "owner_approval_refs": [name for name in names if name.startswith(".certamerge/evidence/") and "approval" in name.lower()],
        "car_verification_refs": _metadata_evidence_refs(names, "car-verification"),
        "no_source_egress_refs": _metadata_evidence_refs(names, "no-source-egress"),
        "risk_surface_classification_refs": _metadata_evidence_refs(names, "risk-surface"),
        "workflow_validation_refs": _metadata_evidence_refs(names, "workflow-validation"),
        "action_contract_validation_refs": _metadata_evidence_refs(names, "action-contract"),
        "schema_validation_refs": _metadata_evidence_refs(names, "schema-validation"),
        "compliance_safe_language_refs": _metadata_evidence_refs(names, "compliance-safe-language"),
        "no_secret_leakage_refs": _metadata_evidence_refs(names, "no-secret-leakage"),
        "links_valid_refs": _metadata_evidence_refs(names, "links-valid"),
        "license_refs": [lower_names[key] for key in lower_names if key in {"license", "license.md", "license.txt", "copying"}],
        "codeowners_refs": codeowners_refs,
        "pr_template_refs": pr_template_refs,
        "issue_template_refs": issue_template_refs,
        "action_metadata_refs": [name for name in names if name in {"action.yml", "action.yaml"}],
        "terraform_refs": terraform_refs,
        "terraform_validation_refs": _metadata_evidence_refs(names, "terraform-validation", "tf-validate"),
        "terraform_plan_refs": sorted(
            set(
                _metadata_evidence_refs(names, "terraform-plan", "tf-plan")
                + [
                    name
                    for name in names
                    if name.endswith(".json") and ("terraform-plan" in name.lower() or "tfplan" in name.lower() or name.lower().endswith("plan.json"))
                ]
            )
        ),
        "secret_scan_refs": [
            name
            for name in names
            if name.endswith(".json") and ("gitleaks" in name.lower() or "secret-scan" in name.lower() or "secrets-scan" in name.lower())
        ],
        "docs_refs": sorted(set(docs_refs)),
        "docs_build_refs": sorted(set(docs_build_refs + _metadata_evidence_refs(names, "docs-build"))),
        "readme": ["README.md"] if "README.md" in names else [],
        "contributing": ["CONTRIBUTING.md"] if "CONTRIBUTING.md" in names else [],
        "security": ["SECURITY.md"] if "SECURITY.md" in names else [],
    }


def _fact(evidence_type: str, state: str, summary: str, refs: list[str] | None = None, details: dict[str, Any] | None = None) -> dict[str, Any]:
    refs = refs or []
    return {
        "evidence_id": f"ev_{evidence_type}",
        "type": evidence_type,
        "state": state,
        "source": "local",
        "summary": summary,
        "artifact_ref": refs[0] if refs else "",
        "artifact_refs": refs,
        "sensitive": "metadata",
        "details": details or {},
    }


def _sarif_fact(repo: Path, refs: list[str]) -> dict[str, Any]:
    if not refs:
        return _fact("sarif_scan", "missing", "SARIF/code scanning evidence is missing.")
    total_results = 0
    for ref in refs:
        data, error = _read_json(repo / ref)
        if error or data is None:
            return _fact("sarif_scan", "malformed", f"SARIF evidence could not be parsed: {error}", refs)
        runs = data.get("runs")
        if not isinstance(runs, list):
            return _fact("sarif_scan", "malformed", "SARIF evidence is missing a runs array.", refs)
        for run in runs:
            if isinstance(run, dict):
                results = run.get("results", [])
                if isinstance(results, list):
                    total_results += len(results)
    if total_results == 0:
        return _fact("sarif_scan", "negative", "SARIF evidence is present and contains no findings.", refs, {"finding_count": 0})
    return _fact("sarif_scan", "failed", f"SARIF evidence contains {total_results} finding(s).", refs, {"finding_count": total_results})


def _junit_state(repo: Path, ref: str) -> tuple[str, dict[str, int], str]:
    root, error = _read_xml(repo / ref)
    if error or root is None:
        return "malformed", {}, f"JUnit evidence could not be parsed: {error}"
    suites = [root] if root.tag.endswith("testsuite") else [item for item in root.iter() if item.tag.endswith("testsuite")]
    tests = 0
    failures = 0
    errors = 0
    for suite in suites:
        try:
            tests += int(suite.attrib.get("tests", "0"))
            failures += int(suite.attrib.get("failures", "0"))
            errors += int(suite.attrib.get("errors", "0"))
        except ValueError:
            return "malformed", {}, "JUnit evidence contains non-integer test counters."
    if tests == 0:
        tests = len([item for item in root.iter() if item.tag.endswith("testcase")])
        failures = len([item for item in root.iter() if item.tag.endswith("failure")])
        errors = len([item for item in root.iter() if item.tag.endswith("error")])
    details = {"tests": tests, "failures": failures, "errors": errors}
    if failures or errors:
        return "failed", details, "JUnit evidence reports failing tests."
    if tests:
        return "present", details, "JUnit evidence is present and passing."
    return "insufficient", details, "JUnit evidence exists but contains no test cases."


def _test_result_fact(repo: Path, script_state: str, script_refs: list[str], result_refs: list[str], junit_refs: list[str]) -> dict[str, Any]:
    refs = script_refs + result_refs + junit_refs
    if not result_refs and not junit_refs:
        summary = "Test command configured." if script_refs else "Test result evidence is missing."
        return _fact("test_result", script_state, summary, refs)
    passed = 0
    failed = 0
    stale = 0
    unavailable = 0
    insufficient = 0
    junit_details: list[dict[str, int]] = []
    now = _now()
    for ref in result_refs:
        data, error = _read_json(repo / ref)
        if error or data is None:
            return _fact("test_result", "malformed", f"Test result evidence could not be parsed: {error}", refs)
        expires_at = _parse_time(data.get("expires_at"))
        if expires_at and expires_at < now:
            stale += 1
            continue
        status = str(data.get("status") or data.get("state") or data.get("conclusion") or data.get("result") or "").lower()
        if status in {"passed", "pass", "success", "succeeded", "green"}:
            passed += 1
        elif status in {"failed", "fail", "failure", "error", "red"}:
            failed += 1
        elif status in {"unavailable", "not_available", "unreachable", "skipped_unavailable"}:
            unavailable += 1
        else:
            insufficient += 1
    for ref in junit_refs:
        state, details, summary = _junit_state(repo, ref)
        if state == "malformed":
            return _fact("test_result", "malformed", summary, refs)
        if state == "failed":
            failed += 1
        elif state == "present":
            passed += 1
        elif state == "insufficient":
            insufficient += 1
        if details:
            junit_details.append(details)
    if failed:
        return _fact("test_result", "failed", "Test result evidence reports failing tests.", refs, {"junit": junit_details})
    if passed:
        return _fact("test_result", "present", "Test result evidence is present and passing.", refs, {"junit": junit_details})
    if stale:
        return _fact("test_result", "stale", "Test result evidence is expired.", refs)
    if unavailable:
        return _fact("test_result", "unavailable", "Test result evidence is explicitly unavailable.", refs)
    if insufficient:
        return _fact("test_result", "insufficient", "Test result evidence exists but lacks a passing or failing status.", refs)
    return _fact("test_result", script_state, "Test result evidence is missing.", refs)


def _cyclonedx_json_details(data: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    components = data.get("components", [])
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    valid = data.get("bomFormat") == "CycloneDX" or isinstance(components, list)
    return valid, {
        "format": str(data.get("bomFormat") or "json"),
        "component_count": len(components) if isinstance(components, list) else 0,
        "metadata_component": bool(metadata.get("component")),
    }


def _cyclonedx_xml_details(repo: Path, ref: str) -> tuple[str, dict[str, Any], str]:
    root, error = _read_xml(repo / ref)
    if error or root is None:
        return "malformed", {}, f"SBOM evidence could not be parsed: {error}"
    tag = root.tag.split("}")[-1]
    if tag != "bom":
        return "insufficient", {}, "SBOM XML evidence is not a CycloneDX bom document."
    components = [item for item in root.iter() if item.tag.split("}")[-1] == "component"]
    return "present", {"format": "CycloneDX XML", "component_count": len(components)}, "CycloneDX SBOM evidence is present."


def _dependency_reference_fact(repo: Path, lock_refs: list[str], sbom_refs: list[str], dependency_review_refs: list[str]) -> dict[str, Any]:
    refs = lock_refs + sbom_refs + dependency_review_refs
    sbom_details: list[dict[str, Any]] = []
    for ref in sbom_refs:
        if ref.endswith(".json"):
            data, error = _read_json(repo / ref)
            if error or data is None:
                return _fact("dependency_reference", "malformed", f"SBOM evidence could not be parsed: {error}", refs)
            valid, details = _cyclonedx_json_details(data)
            if not valid:
                return _fact("dependency_reference", "insufficient", "SBOM JSON evidence lacks CycloneDX metadata.", refs)
            sbom_details.append(details)
        elif ref.endswith(".xml"):
            state, details, summary = _cyclonedx_xml_details(repo, ref)
            if state != "present":
                return _fact("dependency_reference", state, summary, refs)
            sbom_details.append(details)
    if lock_refs or sbom_refs or dependency_review_refs:
        return _fact(
            "dependency_reference",
            "present",
            "Dependency lockfile, SBOM, or dependency review evidence reference present.",
            refs,
            {"sbom": sbom_details},
        )
    return _fact("dependency_reference", "missing", "Dependency/SBOM reference evidence is missing.", refs)


def _terraform_plan_fact(repo: Path, refs: list[str]) -> dict[str, Any]:
    if not refs:
        return _fact("terraform_plan", "missing", "Terraform plan evidence is missing.")
    for ref in refs:
        data, error = _read_json(repo / ref)
        if error or data is None:
            return _fact("terraform_plan", "malformed", f"Terraform plan evidence could not be parsed: {error}", refs)
        resource_changes = data.get("resource_changes")
        if not isinstance(resource_changes, list):
            return _fact("terraform_plan", "insufficient", "Terraform plan evidence lacks resource_changes.", refs)
        actions: dict[str, int] = {}
        for change in resource_changes:
            if not isinstance(change, dict):
                continue
            plan_change = change.get("change") if isinstance(change.get("change"), dict) else {}
            for action in plan_change.get("actions", []) if isinstance(plan_change.get("actions"), list) else []:
                actions[str(action)] = actions.get(str(action), 0) + 1
        return _fact("terraform_plan", "present", "Terraform plan evidence is present.", refs, {"resource_change_count": len(resource_changes), "actions": actions})
    return _fact("terraform_plan", "missing", "Terraform plan evidence is missing.")


def _secret_scan_fact(repo: Path, refs: list[str]) -> dict[str, Any]:
    if not refs:
        return _fact("secret_scan", "missing", "Secret scan evidence is missing.")
    total_findings = 0
    for ref in refs:
        try:
            data = json.loads((repo / ref).read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError, UnicodeDecodeError) as exc:
            return _fact("secret_scan", "malformed", f"Secret scan evidence could not be parsed: {exc}", refs)
        findings = []
        if isinstance(data, dict):
            findings = data.get("findings", data.get("results", data.get("leaks", [])))
        if isinstance(data, list):
            findings = data
        if not isinstance(findings, list):
            return _fact("secret_scan", "insufficient", "Secret scan evidence lacks a findings/results/leaks array.", refs)
        total_findings += len(findings)
    if total_findings:
        return _fact("secret_scan", "failed", f"Secret scan evidence contains {total_findings} finding(s).", refs, {"finding_count": total_findings})
    return _fact("secret_scan", "negative", "Secret scan evidence is present and contains no findings.", refs, {"finding_count": 0})


def _owner_approval_fact(repo: Path, refs: list[str]) -> dict[str, Any]:
    if not refs:
        return _fact("owner_approval", "missing", "Owner approval evidence is missing.")
    approved = 0
    denied = 0
    stale = 0
    unavailable = 0
    insufficient = 0
    now = _now()
    approvers: list[str] = []
    for ref in refs:
        data, error = _read_json(repo / ref)
        if error or data is None:
            return _fact("owner_approval", "malformed", f"Owner approval evidence could not be parsed: {error}", refs)
        decision = str(data.get("decision", "")).lower()
        expires_at = _parse_time(data.get("expires_at"))
        if expires_at and expires_at < now:
            stale += 1
            continue
        if decision in {"approved", "approve", "accepted"}:
            approved += 1
            owner = data.get("owner") or data.get("approver")
            if isinstance(owner, str) and owner:
                approvers.append(owner)
        elif decision in {"denied", "rejected", "blocked"}:
            denied += 1
        elif decision in {"unavailable", "not_available", "unreachable"}:
            unavailable += 1
        else:
            insufficient += 1
    if approved and denied:
        return _fact("owner_approval", "conflicting", "Owner approval evidence has conflicting approved and denied decisions.", refs, {"approvers": approvers})
    if denied:
        return _fact("owner_approval", "failed", "Owner approval evidence explicitly denies approval.", refs)
    if approved:
        return _fact("owner_approval", "present", "Owner approval reference present and approved.", refs, {"approvers": approvers})
    if stale:
        return _fact("owner_approval", "stale", "Owner approval evidence is expired.", refs)
    if unavailable:
        return _fact("owner_approval", "unavailable", "Owner approval evidence is explicitly unavailable.", refs)
    if insufficient:
        return _fact("owner_approval", "insufficient", "Owner approval evidence exists but lacks an approved decision.", refs)
    return _fact("owner_approval", "missing", "Owner approval evidence is missing.")


def evidence_from_signals(repo: Path, signals: dict[str, Any]) -> list[dict[str, Any]]:
    ci_refs = list(signals.get("ci_configs", []))
    test_refs = list(signals.get("test_scripts", []))
    test_result_refs = list(signals.get("test_result_refs", []))
    junit_refs = list(signals.get("junit_refs", []))
    lint_refs = list(signals.get("lint_refs", []))
    lock_refs = list(signals.get("lockfiles", []))
    sbom_refs = list(signals.get("sbom_refs", []))
    dependency_review_refs = list(signals.get("dependency_review_refs", []))
    evidence = [
        _fact("ci_status", "present" if ci_refs else "missing", "CI configuration present." if ci_refs else "CI status evidence is missing.", ci_refs),
        _test_result_fact(repo, signals.get("test_script_state", "missing"), test_refs, test_result_refs, junit_refs),
        _fact("lint_result", "present" if lint_refs else "missing", "Lint evidence reference present." if lint_refs else "Lint evidence is missing.", lint_refs),
        _sarif_fact(repo, list(signals.get("sarif_files", []))),
        _dependency_reference_fact(repo, lock_refs, sbom_refs, dependency_review_refs),
        _owner_approval_fact(repo, list(signals.get("owner_approval_refs", []))),
        _fact("github_actions_artifact", "present" if ci_refs else "missing", "GitHub Actions workflow reference present." if ci_refs else "GitHub Actions artifact/reference evidence is missing.", ci_refs),
        _fact("security_doc", "present" if signals.get("security") else "missing", "Security policy document present." if signals.get("security") else "Security policy document is missing.", list(signals.get("security", []))),
        _fact(
            "license_file",
            "present" if signals.get("license_refs") else "missing",
            "License file present." if signals.get("license_refs") else "License file is missing.",
            list(signals.get("license_refs", [])),
        ),
        _fact(
            "codeowners",
            "present" if signals.get("codeowners_refs") else "missing",
            "CODEOWNERS reference present." if signals.get("codeowners_refs") else "CODEOWNERS reference is missing.",
            list(signals.get("codeowners_refs", [])),
        ),
        _fact(
            "pr_template",
            "present" if signals.get("pr_template_refs") else "missing",
            "Pull request template present." if signals.get("pr_template_refs") else "Pull request template is missing.",
            list(signals.get("pr_template_refs", [])),
        ),
        _fact(
            "issue_template",
            "present" if signals.get("issue_template_refs") else "missing",
            "Issue template reference present." if signals.get("issue_template_refs") else "Issue template reference is missing.",
            list(signals.get("issue_template_refs", [])),
        ),
        _fact(
            "action_metadata",
            "present" if signals.get("action_metadata_refs") else "missing",
            "GitHub Action metadata present." if signals.get("action_metadata_refs") else "GitHub Action metadata is missing.",
            list(signals.get("action_metadata_refs", [])),
        ),
        _fact(
            "terraform_files",
            "present" if signals.get("terraform_refs") else "missing",
            "Terraform files present." if signals.get("terraform_refs") else "Terraform files are missing.",
            list(signals.get("terraform_refs", [])),
        ),
        _fact(
            "terraform_validation",
            "present" if signals.get("terraform_validation_refs") else "missing",
            "Terraform validation evidence is present." if signals.get("terraform_validation_refs") else "Terraform validation evidence is missing.",
            list(signals.get("terraform_validation_refs", [])),
        ),
        _terraform_plan_fact(repo, list(signals.get("terraform_plan_refs", []))),
        _secret_scan_fact(repo, list(signals.get("secret_scan_refs", []))),
        _fact(
            "docs_site",
            "present" if signals.get("docs_refs") else "missing",
            "Documentation surface present." if signals.get("docs_refs") else "Documentation surface is missing.",
            list(signals.get("docs_refs", [])),
        ),
        _fact(
            "docs_build",
            "present" if signals.get("docs_build_refs") else "missing",
            "Documentation build evidence or config present." if signals.get("docs_build_refs") else "Documentation build evidence is missing.",
            list(signals.get("docs_build_refs", [])),
        ),
        _fact(
            "car_verification",
            "present" if signals.get("car_verification_refs") else "missing",
            "CAR verification evidence is present." if signals.get("car_verification_refs") else "CAR verification evidence is missing.",
            list(signals.get("car_verification_refs", [])),
        ),
        _fact(
            "no_source_egress",
            "present" if signals.get("no_source_egress_refs") else "missing",
            "No-source-egress evidence is present." if signals.get("no_source_egress_refs") else "No-source-egress evidence is missing.",
            list(signals.get("no_source_egress_refs", [])),
        ),
        _fact(
            "risk_surface_classification",
            "present" if signals.get("risk_surface_classification_refs") else "missing",
            "Risk surface classification evidence is present." if signals.get("risk_surface_classification_refs") else "Risk surface classification evidence is missing.",
            list(signals.get("risk_surface_classification_refs", [])),
        ),
        _fact(
            "workflow_validation",
            "present" if signals.get("workflow_validation_refs") else "missing",
            "Workflow validation evidence is present." if signals.get("workflow_validation_refs") else "Workflow validation evidence is missing.",
            list(signals.get("workflow_validation_refs", [])),
        ),
        _fact(
            "action_contract_validation",
            "present" if signals.get("action_contract_validation_refs") else "missing",
            "Action contract validation evidence is present." if signals.get("action_contract_validation_refs") else "Action contract validation evidence is missing.",
            list(signals.get("action_contract_validation_refs", [])),
        ),
        _fact(
            "schema_validation",
            "present" if signals.get("schema_validation_refs") else "missing",
            "Schema validation evidence is present." if signals.get("schema_validation_refs") else "Schema validation evidence is missing.",
            list(signals.get("schema_validation_refs", [])),
        ),
        _fact(
            "compliance_safe_language",
            "present" if signals.get("compliance_safe_language_refs") else "missing",
            "Compliance-safe-language evidence is present." if signals.get("compliance_safe_language_refs") else "Compliance-safe-language evidence is missing.",
            list(signals.get("compliance_safe_language_refs", [])),
        ),
        _fact(
            "no_secret_leakage",
            "present" if signals.get("no_secret_leakage_refs") else "missing",
            "No-secret-leakage evidence is present." if signals.get("no_secret_leakage_refs") else "No-secret-leakage evidence is missing.",
            list(signals.get("no_secret_leakage_refs", [])),
        ),
        _fact(
            "links_valid",
            "present" if signals.get("links_valid_refs") else "missing",
            "Link validation evidence is present." if signals.get("links_valid_refs") else "Link validation evidence is missing.",
            list(signals.get("links_valid_refs", [])),
        ),
    ]
    return evidence


def normalize_required_evidence(required: str) -> str:
    return REQUIRED_EVIDENCE_ALIASES.get(required, required)


def evidence_for_required(required: str, snapshot: dict[str, Any]) -> dict[str, Any] | None:
    evidence_type = normalize_required_evidence(required)
    return next((item for item in snapshot["evidence"] if item["type"] == evidence_type), None)


def evidence_satisfied(required: str, snapshot: dict[str, Any]) -> bool:
    item = evidence_for_required(required, snapshot)
    return bool(item and item.get("state") in SATISFYING_EVIDENCE_STATES)


def missing_proof_from_evidence(evidence: list[dict[str, Any]], risk_surfaces: list[str]) -> list[dict[str, Any]]:
    missing: list[dict[str, Any]] = []
    required = ["test_result", "ci_status"]
    if any(surface in {"auth", "payments", "database"} for surface in risk_surfaces):
        required.append("owner_approval")
    for evidence_type in required:
        item = next((ev for ev in evidence if ev["type"] == evidence_type), None)
        if item and item["state"] not in SATISFYING_EVIDENCE_STATES:
            missing.append(
                {
                    "proof_id": f"mp_{evidence_type}",
                    "type": evidence_type,
                    "state": item["state"],
                    "reason": f"{evidence_type} proof is required for current repository/risk context.",
                    "evidence_id": item["evidence_id"],
                }
            )
    return missing
