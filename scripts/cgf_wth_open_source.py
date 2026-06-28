from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / ".tmp" / "cgf-wth"
RESULT_JSON = TMP / "open-source-results.json"
RESULT_MD = ROOT / "docs" / "testing" / "CGF_WTH_OPEN_SOURCE_RESULTS.md"
PYTHONPATH = str(ROOT / "community" / "cli")


class Harness:
    def __init__(self) -> None:
        self.checks: list[dict[str, Any]] = []

    def add(
        self,
        workflow: str,
        passed: bool,
        evidence: str,
        command: list[str] | None = None,
        severity: str = "medium",
        readiness: str | None = None,
    ) -> None:
        self.checks.append(
            {
                "workflow": workflow,
                "passed": bool(passed),
                "severity": severity,
                "readiness": readiness or ("ready" if passed else "not_ready"),
                "evidence": evidence.strip()[:2000],
                "command": command or [],
            }
        )

    def failures(self) -> list[dict[str, Any]]:
        return [check for check in self.checks if not check["passed"]]

    def critical_high_failures(self) -> list[dict[str, Any]]:
        return [check for check in self.failures() if check["severity"] in {"critical", "high"}]


def env() -> dict[str, str]:
    values = os.environ.copy()
    existing = values.get("PYTHONPATH", "")
    values["PYTHONPATH"] = PYTHONPATH + (os.pathsep + existing if existing else "")
    return values


def run_command(args: list[str], timeout: int = 120) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            args,
            cwd=ROOT,
            env=env(),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "args": args,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    except (OSError, subprocess.SubprocessError) as exc:
        return {"args": args, "returncode": 99, "stdout": "", "stderr": str(exc)}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def parse_json_output(result: dict[str, Any]) -> tuple[bool, dict[str, Any], str]:
    try:
        return True, json.loads(result["stdout"]), ""
    except json.JSONDecodeError as exc:
        return False, {}, str(exc)


def command_text(result: dict[str, Any]) -> str:
    return (result.get("stdout", "") + "\n" + result.get("stderr", "")).strip()


def scan_text_files(patterns: list[str], exclude: set[str] | None = None) -> list[str]:
    exclude = {
        "scripts/cgf_wth_open_source.py",
        "scripts/cppef_open_source.py",
        "community/tests/test_public_release_candidate_contracts.py",
        "docs/testing/CGF_WTH_OPEN_SOURCE_RESULTS.md",
        *(exclude or set()),
    }
    ignored_parts = {".git", ".tmp", ".pytest_cache", "__pycache__", "dist", "build"}
    compiled = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    hits: list[str] = []
    for path in ROOT.rglob("*"):
        if any(part in ignored_parts or part.endswith(".egg-info") for part in path.parts):
            continue
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel in exclude:
            continue
        text = read_text(path)
        forbidden_context = False
        for line in text.splitlines():
            lowered = line.lower()
            if any(marker in lowered for marker in ["forbidden", "must not", "never claim", "do not claim", "non-claims"]):
                forbidden_context = True
                continue
            if forbidden_context and not lowered.strip():
                continue
            if forbidden_context and not lowered.lstrip().startswith("-"):
                forbidden_context = False
            if forbidden_context:
                continue
            if any(pattern.search(line) for pattern in compiled):
                hits.append(rel)
                break
    return sorted(set(hits))


def add_command_check(
    harness: Harness,
    workflow: str,
    args: list[str],
    expected: Any,
    severity: str = "medium",
    timeout: int = 120,
) -> dict[str, Any]:
    result = run_command(args, timeout=timeout)
    if callable(expected):
        passed = bool(expected(result))
    else:
        passed = result["returncode"] == expected
    harness.add(workflow, passed, command_text(result), args, severity)
    return result


def verify_json_file(harness: Harness, workflow: str, path: Path, required_keys: set[str], severity: str = "high") -> dict[str, Any]:
    payload = read_json(path)
    missing = sorted(required_keys - set(payload))
    harness.add(workflow, bool(payload) and not missing, f"path={path}; missing_keys={missing}", severity=severity)
    return payload


def run_core_cli_workflows(harness: Harness) -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    changed_files = TMP / "changed-files.txt"
    changed_files.write_text(
        "\n".join(
            [
                "community/cli/certamerge/cli.py",
                "community/cli/certamerge/gate.py",
                ".github/workflows/certamerge-proof-gate.yml",
                "docs/community/quickstart.md",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    add_command_check(harness, "install from repo", [sys.executable, "-m", "pip", "install", "-e", "."], 0, "critical", 180)
    add_command_check(harness, "CLI help", [sys.executable, "-m", "certamerge", "--help"], lambda r: r["returncode"] == 0 and "Usage" in r["stdout"], "critical")
    add_command_check(harness, "recover", [sys.executable, "-m", "certamerge", "recover", "."], lambda r: r["returncode"] == 0 and "Verdict:" in r["stdout"], "high")

    recover_json = add_command_check(
        harness,
        "recover --json",
        [sys.executable, "-m", "certamerge", "recover", ".", "--json"],
        lambda r: r["returncode"] == 0,
        "critical",
    )
    ok, recover_payload, recover_error = parse_json_output(recover_json)
    harness.add(
        "recover --json parses",
        ok and {"verdict", "missing_proof", "repair_missions", "project_type", "signals"} <= set(recover_payload),
        recover_error or json.dumps({key: recover_payload.get(key) for key in ["verdict", "missing_proof"]}, sort_keys=True),
        severity="critical",
    )

    add_command_check(
        harness,
        "recover --suggest-policy",
        [sys.executable, "-m", "certamerge", "recover", ".", "--suggest-policy"],
        lambda r: r["returncode"] == 0 and "Suggested policy:" in r["stdout"],
        "high",
    )
    suggested_policy = TMP / "self.suggested.certamerge.yml"
    add_command_check(
        harness,
        "suggest-policy --output",
        [sys.executable, "-m", "certamerge", "suggest-policy", ".", "--output", str(suggested_policy)],
        lambda r: r["returncode"] == 0 and suggested_policy.exists(),
        "high",
    )

    repo_car = TMP / "self.repo-snapshot.car.json"
    add_command_check(
        harness,
        "gate with repo snapshot",
        [sys.executable, "-m", "certamerge", "gate", "--repo", ".", "--policy", ".certamerge.yml", "--output", str(repo_car)],
        lambda r: r["returncode"] == 0 and repo_car.exists() and "Verdict:" in r["stdout"],
        "critical",
    )
    verify_json_file(harness, "repo snapshot CAR file", repo_car, {"car_id", "verdict", "policy", "integrity"})

    changed_car = TMP / "self.changed-files.car.json"
    add_command_check(
        harness,
        "gate with --changed-files",
        [
            sys.executable,
            "-m",
            "certamerge",
            "gate",
            "--repo",
            ".",
            "--policy",
            ".certamerge.yml",
            "--changed-files",
            str(changed_files),
            "--output",
            str(changed_car),
        ],
        lambda r: r["returncode"] == 0 and changed_car.exists(),
        "critical",
    )
    changed_payload = read_json(changed_car)
    harness.add(
        "changed-files CAR records explicit scope",
        changed_payload.get("change", {}).get("change_context_mode") == "explicit_changed_files",
        json.dumps(changed_payload.get("change", {}), sort_keys=True),
        severity="high",
    )

    head = run_command(["git", "rev-parse", "HEAD"])
    head_sha = head["stdout"].strip() if head["returncode"] == 0 else "HEAD"
    diff_car = TMP / "self.base-head.car.json"
    add_command_check(
        harness,
        "gate with --base/--head",
        [
            sys.executable,
            "-m",
            "certamerge",
            "gate",
            "--repo",
            ".",
            "--policy",
            ".certamerge.yml",
            "--base",
            head_sha,
            "--head",
            head_sha,
            "--output",
            str(diff_car),
        ],
        lambda r: r["returncode"] == 0 and diff_car.exists(),
        "high",
    )

    json_car = TMP / "self.json.car.json"
    gate_json = add_command_check(
        harness,
        "gate --json",
        [sys.executable, "-m", "certamerge", "gate", "--repo", ".", "--policy", ".certamerge.yml", "--json", "--output", str(json_car)],
        lambda r: r["returncode"] == 0 and json_car.exists(),
        "critical",
    )
    ok, gate_payload, gate_error = parse_json_output(gate_json)
    harness.add(
        "gate --json parses",
        ok and {"verdict", "policy_reason", "missing_proof", "accountable_next_action", "car"} <= set(gate_payload),
        gate_error or json.dumps({key: gate_payload.get(key) for key in ["verdict", "policy_reason"]}, sort_keys=True),
        severity="critical",
    )

    add_command_check(harness, "verify-car", [sys.executable, "-m", "certamerge", "verify-car", str(repo_car)], lambda r: r["returncode"] == 0 and '"valid": true' in r["stdout"], "critical")
    add_command_check(harness, "explain-car", [sys.executable, "-m", "certamerge", "explain-car", str(repo_car)], lambda r: r["returncode"] == 0 and "Verdict:" in r["stdout"], "high")
    explain_json = add_command_check(harness, "explain-car --json", [sys.executable, "-m", "certamerge", "explain-car", str(repo_car), "--json"], lambda r: r["returncode"] == 0, "critical")
    ok, explain_payload, explain_error = parse_json_output(explain_json)
    harness.add(
        "explain-car --json parses",
        ok and explain_payload.get("verification", {}).get("valid") is True,
        explain_error or json.dumps(explain_payload.get("verification", {}), sort_keys=True),
        severity="critical",
    )


def run_archetype_workflows(harness: Harness) -> None:
    archetypes = [
        "python-library",
        "node-typescript-app",
        "github-action-repo",
        "terraform-iac-repo",
        "monorepo-app",
        "docs-heavy-repo",
    ]
    for repo_name in archetypes:
        repo = Path("samples/repos/archetypes") / repo_name
        recover = add_command_check(
            harness,
            f"archetype recover --json: {repo_name}",
            [sys.executable, "-m", "certamerge", "recover", str(repo), "--json"],
            lambda r: r["returncode"] == 0,
            "high",
        )
        ok, payload, error = parse_json_output(recover)
        harness.add(
            f"archetype recover parses: {repo_name}",
            ok and payload.get("project_type") == repo_name,
            error or json.dumps({"project_type": payload.get("project_type"), "verdict": payload.get("verdict")}, sort_keys=True),
            severity="high",
        )

        policy = TMP / f"{repo_name}.policy.yml"
        car = TMP / f"{repo_name}.car.json"
        add_command_check(
            harness,
            f"archetype suggest-policy: {repo_name}",
            [sys.executable, "-m", "certamerge", "suggest-policy", str(repo), "--output", str(policy)],
            lambda r, policy=policy: r["returncode"] == 0 and policy.exists(),
            "high",
        )
        add_command_check(
            harness,
            f"archetype gate: {repo_name}",
            [sys.executable, "-m", "certamerge", "gate", "--repo", str(repo), "--policy", str(policy), "--output", str(car)],
            lambda r, car=car: r["returncode"] == 0 and car.exists(),
            "critical",
        )
        add_command_check(
            harness,
            f"archetype verify-car: {repo_name}",
            [sys.executable, "-m", "certamerge", "verify-car", str(car)],
            lambda r: r["returncode"] == 0 and '"valid": true' in r["stdout"],
            "critical",
        )
        explain = add_command_check(
            harness,
            f"archetype explain-car --json: {repo_name}",
            [sys.executable, "-m", "certamerge", "explain-car", str(car), "--json"],
            lambda r: r["returncode"] == 0,
            "high",
        )
        ok, explain_payload, error = parse_json_output(explain)
        harness.add(
            f"archetype explain JSON parses: {repo_name}",
            ok and explain_payload.get("verification", {}).get("valid") is True,
            error or json.dumps(explain_payload.get("verification", {}), sort_keys=True),
            severity="high",
        )


def run_integrity_and_action_workflows(harness: Harness) -> None:
    repo_car = TMP / "self.repo-snapshot.car.json"
    car = read_json(repo_car)
    if car:
        car["verdict"]["state"] = "BLOCK" if car.get("verdict", {}).get("state") != "BLOCK" else "ALLOW"
        tampered = TMP / "self.tampered.car.json"
        tampered.write_text(json.dumps(car, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        add_command_check(
            harness,
            "CAR integrity mutation checks",
            [sys.executable, "-m", "certamerge", "verify-car", str(tampered)],
            lambda r: r["returncode"] != 0 and "Traceback" not in command_text(r),
            "critical",
        )
    else:
        harness.add("CAR integrity mutation checks", False, "base CAR missing", severity="critical")

    action = read_text(ROOT / "community" / "github-action" / "action.yml")
    harness.add("GitHub Action proof gate", "certamerge \"${args[@]}\"" in action and "fail-on-block" in action and "blocking =" in action, "action.yml gate invocation and fail behavior", severity="high")
    harness.add("GitHub Action artifact upload", "actions/upload-artifact" in action and "car-path" in action, "action.yml artifact upload", severity="medium")
    harness.add("GitHub Action summary", "GITHUB_STEP_SUMMARY" in action and "CertaMerge" in action, "action.yml summary generation", severity="medium")

    sample_results = []
    for sample in sorted((ROOT / "samples" / "cars").glob("*.json")):
        result = run_command([sys.executable, "-m", "certamerge", "verify-car", str(sample)])
        sample_results.append({"sample": sample.name, "returncode": result["returncode"], "valid_text": '"valid": true' in result["stdout"]})
    harness.add(
        "sample CAR verification",
        any(item["valid_text"] for item in sample_results) and all(item["returncode"] in {0, 1} for item in sample_results),
        json.dumps(sample_results, sort_keys=True),
        severity="medium",
    )


def run_docs_safety_workflows(harness: Harness) -> None:
    readme = read_text(ROOT / "README.md")
    required_sections = [
        "What CertaMerge does",
        "Quickstart",
        "Core workflow",
        "Example output",
        "GitHub Action",
        "Agent / JSON usage",
        "Change Authorization Records",
        "Evidence adapters",
        "What CertaMerge is not",
        "Security and privacy posture",
        "Community alpha limitations",
        "Enterprise boundary",
        "Contributing / feedback",
    ]
    missing_sections = [section for section in required_sections if section.lower() not in readme.lower()]
    harness.add("README professional contract", not missing_sections, "missing_sections=" + json.dumps(missing_sections), severity="high")

    required_phrases = [
        "CertaMerge is an open-source ProofOps CLI for software changes.",
        "Does this change have enough proof to move forward, and can we verify that decision later?",
        "GitHub rules decide whether checks are required.",
        "Scanners find issues.",
        "Change Authorization Record",
    ]
    missing_phrases = [phrase for phrase in required_phrases if phrase not in readme]
    harness.add("README first-screen positioning", not missing_phrases, "missing_phrases=" + json.dumps(missing_phrases), severity="high")

    agent_doc = read_text(ROOT / "docs" / "community" / "agent-workflow.md")
    harness.add("agent workflow", "recover" in agent_doc and "--json" in agent_doc and "verify-car" in agent_doc, "docs/community/agent-workflow.md", severity="high")
    harness.add("human quickstart", "python -m certamerge recover" in read_text(ROOT / "docs" / "community" / "quickstart.md"), "docs/community/quickstart.md", severity="high")
    harness.add("5-minute demo", "5-minute" in read_text(ROOT / "docs" / "demo" / "5_MINUTE_PUBLIC_ALPHA_DEMO.md").lower(), "docs/demo/5_MINUTE_PUBLIC_ALPHA_DEMO.md", severity="medium")
    no_egress = read_text(ROOT / "docs" / "community" / "no-source-egress.md").lower()
    harness.add("no-source-egress posture", "no telemetry" in no_egress and "does not send telemetry" in no_egress, "docs/community/no-source-egress.md", severity="high")

    path_hits = scan_text_files([r"C:\\Users\\", r"\\\\wsl", r"\.codex"], {"scripts/cgf_wth_open_source.py"})
    secret_hits = scan_text_files([r"sk-[A-Za-z0-9]{20,}", r"ghp_[A-Za-z0-9]{20,}", r"AKIA[0-9A-Z]{16}", r"BEGIN (RSA |OPENSSH |)PRIVATE KEY"], {"scripts/cgf_wth_open_source.py"})
    unsafe_hits = scan_text_files([r"SOC 2 compliant", r"ISO certified", r"guaranteed secure", r"guarantees security", r"production enterprise ready"], {"scripts/cgf_wth_open_source.py"})
    enterprise_hits = scan_text_files([r"certamerge_enterprise", r"enterprise/server"], {"scripts/cgf_wth_open_source.py"})
    harness.add("local-path leakage scan", not path_hits, ", ".join(path_hits), severity="critical")
    harness.add("secret-looking string scan", not secret_hits, ", ".join(secret_hits), severity="critical")
    harness.add("safe-language scan", not unsafe_hits, ", ".join(unsafe_hits), severity="critical")
    harness.add("public/private leakage scan", not enterprise_hits, ", ".join(enterprise_hits), severity="critical")


def run_release_workflows(harness: Harness) -> None:
    add_command_check(harness, "pytest", [sys.executable, "-m", "pytest", "-q"], lambda r: r["returncode"] == 0 and "passed" in r["stdout"], "critical", 180)
    add_command_check(harness, "pytest collect-only", [sys.executable, "-m", "pytest", "--collect-only", "-q"], lambda r: r["returncode"] == 0 and "tests collected" in r["stdout"], "high", 120)
    add_command_check(harness, "compileall", [sys.executable, "-m", "compileall", "community", "scripts"], 0, "high", 120)
    add_command_check(harness, "release build", [sys.executable, "-m", "build"], 0, "high", 180)
    add_command_check(harness, "twine check", [sys.executable, "-m", "twine", "check", "dist/*"], 0, "high", 120)
    add_command_check(harness, "checksum generation", [sys.executable, "scripts/generate_checksums.py"], 0, "high", 60)


def score_result(harness: Harness) -> tuple[float, str, str]:
    checks = harness.checks
    if not checks:
        return 0.0, "broken", "CERTAMERGE OPEN SOURCE GRAND FINALE NOT READY - missing: no checks executed"
    passed = sum(1 for check in checks if check["passed"])
    score = round((passed / len(checks)) * 5, 1)
    critical_high = harness.critical_high_failures()
    if critical_high:
        score = min(score, 2.0)
        verdict = "not-ready"
        final = "CERTAMERGE OPEN SOURCE GRAND FINALE NOT READY - missing: " + "; ".join(item["workflow"] for item in critical_high[:8])
    elif score >= 4.0:
        score = min(score, 4.0)
        verdict = "final-alpha-ready"
        final = "CERTAMERGE OPEN SOURCE GRAND FINALE READY FOR V0.1.0-ALPHA"
    elif score >= 3.0:
        verdict = "alpha-usable-not-final"
        final = "CERTAMERGE OPEN SOURCE GRAND FINALE NOT READY - missing: score below final-alpha threshold"
    elif score >= 2.0:
        verdict = "partially-usable"
        final = "CERTAMERGE OPEN SOURCE GRAND FINALE NOT READY - missing: critical workflow coverage"
    elif score >= 1.0:
        verdict = "documented-but-unusable"
        final = "CERTAMERGE OPEN SOURCE GRAND FINALE NOT READY - missing: executable workflows"
    else:
        verdict = "broken"
        final = "CERTAMERGE OPEN SOURCE GRAND FINALE NOT READY - missing: core execution"
    return score, verdict, final


def write_reports(result: dict[str, Any]) -> None:
    RESULT_JSON.parent.mkdir(parents=True, exist_ok=True)
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# CGF-WTH Open-Source Results",
        "",
        f"Generated: `{result['generated_at']}`",
        "",
        f"Score: `{result['score']}`",
        "",
        f"Verdict: `{result['verdict']}`",
        "",
        "## Workflow Checks",
        "",
        "| Workflow | Passed | Severity | Readiness | Evidence |",
        "|---|---:|---|---|---|",
    ]
    for check in result["checks"]:
        evidence = public_evidence(str(check["evidence"])).replace("|", "\\|").replace("\n", " ")[:240]
        lines.append(f"| {check['workflow']} | `{check['passed']}` | `{check['severity']}` | `{check['readiness']}` | {evidence} |")
    lines.extend(["", "## Critical And High Failures", ""])
    if result["critical_high_failures"]:
        for item in result["critical_high_failures"]:
            lines.append(f"- `{item['severity']}` {item['workflow']}: {public_evidence(str(item['evidence']))}")
    else:
        lines.append("No critical or high CGF-WTH failures recorded.")
    lines.extend(["", "## Final Verdict", "", "```text", result["final_verdict"], "```", ""])
    RESULT_MD.parent.mkdir(parents=True, exist_ok=True)
    RESULT_MD.write_text("\n".join(lines), encoding="utf-8")


def public_evidence(value: str) -> str:
    text = value.replace(str(ROOT), "<repo>")
    text = text.replace(str(ROOT).replace("\\", "/"), "<repo>")
    text = text.replace(str(ROOT).replace("\\", "\\\\"), "<repo>")
    text = re.sub(r"file:///C:/Users/[^/\s]+/Desktop/CertaMerge/products/certamerge-open-source", "file:///<repo>", text, flags=re.IGNORECASE)
    text = re.sub(r"C:\\\\Users\\\\[^\\]+\\\\Desktop\\\\CertaMerge\\\\products\\\\certamerge-open-source", "<repo>", text)
    text = re.sub(r"C:\\Users\\[^\\]+\\Desktop\\CertaMerge\\products\\certamerge-open-source", "<repo>", text)
    text = re.sub(r"c:\\users\\[^\\]+\\", r"<user-home>\\", text, flags=re.IGNORECASE)
    text = re.sub(r"C:\\Users\\[^\\]+\\", r"<user-home>\\", text)
    return text


def main() -> int:
    TMP.mkdir(parents=True, exist_ok=True)
    harness = Harness()
    run_core_cli_workflows(harness)
    run_archetype_workflows(harness)
    run_integrity_and_action_workflows(harness)
    run_docs_safety_workflows(harness)
    run_release_workflows(harness)
    score, verdict, final_verdict = score_result(harness)
    result = {
        "product": "certamerge-open-source",
        "harness": "CGF-WTH",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "score": score,
        "verdict": verdict,
        "final_verdict": final_verdict,
        "checks": harness.checks,
        "failures": harness.failures(),
        "critical_high_failures": harness.critical_high_failures(),
    }
    write_reports(result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not harness.critical_high_failures() and score >= 4.0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
