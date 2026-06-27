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
TMP = ROOT / ".tmp" / "cppef"
RESULT_JSON = TMP / "open-source-results.json"
RESULT_MD = ROOT / "docs" / "testing" / "CPPEF_OPEN_SOURCE_RESULTS.md"
PYTHONPATH = str(ROOT / "community" / "cli")

sys.path.insert(0, PYTHONPATH)

from certamerge.gate import gate_repo
from certamerge.recover import recover_repo
from certamerge.verifier import verify_car


class Evidence:
    def __init__(self) -> None:
        self.categories: dict[str, list[dict[str, Any]]] = {}

    def add(self, category: str, name: str, passed: bool, detail: str = "", critical: bool = False) -> None:
        self.categories.setdefault(category, []).append(
            {
                "name": name,
                "passed": bool(passed),
                "detail": detail,
                "critical": critical,
            }
        )

    def score(self, category: str) -> float:
        checks = self.categories.get(category, [])
        if not checks:
            return 0.0
        passed = sum(1 for item in checks if item["passed"])
        ratio = passed / len(checks)
        score = round(ratio * 4, 1)
        if any(item["critical"] and not item["passed"] for item in checks):
            score = min(score, 2.0)
        return score

    def failures(self) -> list[dict[str, Any]]:
        failures: list[dict[str, Any]] = []
        for category, checks in self.categories.items():
            for item in checks:
                if not item["passed"]:
                    failures.append({"category": category, **item})
        return failures


def _env() -> dict[str, str]:
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = PYTHONPATH + (os.pathsep + existing if existing else "")
    return env


def run_command(args: list[str], timeout: int = 30) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            args,
            cwd=ROOT,
            env=_env(),
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


def iter_public_files() -> list[Path]:
    ignored_parts = {".git", ".tmp", ".pytest_cache", "__pycache__", "dist", "build"}
    ignored_suffixes = {".pyc", ".pyo", ".whl", ".gz", ".zip"}
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if any(part in ignored_parts or part.endswith(".egg-info") for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() not in ignored_suffixes:
            files.append(path)
    return files


def scan_public_text(patterns: list[str]) -> list[str]:
    compiled = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    hits: list[str] = []
    for path in iter_public_files():
        relative = path.relative_to(ROOT).as_posix()
        if relative in {"scripts/cppef_open_source.py", "community/tests/test_public_release_candidate_contracts.py"}:
            continue
        text = read_text(path)
        forbidden_context = False
        for line in text.splitlines():
            lowered = line.lower()
            if any(marker in lowered for marker in ["forbidden", "must not", "must never", "must not say", "never claim", "do not claim", "not in project_text"]):
                forbidden_context = True
                continue
            if forbidden_context and not lowered.strip():
                continue
            if forbidden_context and not lowered.lstrip().startswith("-"):
                forbidden_context = False
            if forbidden_context:
                continue
            if any(pattern.search(line) for pattern in compiled):
                hits.append(relative)
                break
    return sorted(set(hits))


def check_installation(evidence: Evidence) -> None:
    help_result = run_command([sys.executable, "-m", "certamerge", "--help"])
    evidence.add("installation", "CLI entrypoint help", help_result["returncode"] == 0 and "Usage" in help_result["stdout"], help_result["stderr"], True)

    import_result = run_command([sys.executable, "-c", "import certamerge; print(certamerge.__version__)"])
    evidence.add("installation", "import sanity", import_result["returncode"] == 0, import_result["stderr"], True)

    metadata = read_text(ROOT / "pyproject.toml")
    evidence.add("installation", "package metadata", "name = \"certamerge\"" in metadata and "requires-python = \">=3.11\"" in metadata)
    evidence.add("installation", "license metadata", (ROOT / "LICENSE").exists() and "license" in metadata.lower())

    build_check = run_command([sys.executable, "-m", "build"], timeout=90)
    evidence.add("installation", "wheel and sdist build", build_check["returncode"] == 0, build_check["stderr"])

    twine_check = run_command([sys.executable, "-m", "twine", "check", "dist/*"], timeout=60)
    evidence.add("installation", "twine check", twine_check["returncode"] == 0, twine_check["stderr"])

    checksum_check = run_command([sys.executable, "scripts/generate_checksums.py"], timeout=30)
    evidence.add("installation", "checksums generated", checksum_check["returncode"] == 0, checksum_check["stderr"])


def check_cli_ux(evidence: Evidence) -> None:
    bad_command = run_command([sys.executable, "-m", "certamerge", "not-a-command"])
    evidence.add("cli_ux", "bad command returns non-zero", bad_command["returncode"] != 0)

    recover_json = run_command([sys.executable, "-m", "certamerge", "recover", "samples/repos/no-ci-vibe-repo", "--json"])
    try:
        recover_payload = json.loads(recover_json["stdout"])
    except json.JSONDecodeError:
        recover_payload = {}
    evidence.add("cli_ux", "recover JSON output", recover_json["returncode"] == 0 and recover_payload.get("verdict") == "NEEDS_EVIDENCE", recover_json["stderr"], True)

    car_path = TMP / "cli-json-payment.car.json"
    gate_json = run_command(
        [
            sys.executable,
            "-m",
            "certamerge",
            "gate",
            "--repo",
            "samples/repos/payment-change-with-tests",
            "--policy",
            "samples/policies/payment.certamerge.yml",
            "--output",
            str(car_path),
            "--json",
        ]
    )
    try:
        gate_payload = json.loads(gate_json["stdout"])
    except json.JSONDecodeError:
        gate_payload = {}
    evidence.add("cli_ux", "gate JSON output", gate_json["returncode"] == 0 and gate_payload.get("verdict") == "ALLOW", gate_json["stderr"], True)

    explain_json = run_command([sys.executable, "-m", "certamerge", "explain-car", str(car_path), "--json"])
    try:
        explain_payload = json.loads(explain_json["stdout"])
    except json.JSONDecodeError:
        explain_payload = {}
    evidence.add("cli_ux", "explain-car JSON output", explain_json["returncode"] == 0 and explain_payload.get("verification", {}).get("valid") is True)

    invalid_car = TMP / "invalid.car.json"
    invalid_car.write_text("{not-json", encoding="utf-8")
    invalid_result = run_command([sys.executable, "-m", "certamerge", "verify-car", str(invalid_car)])
    evidence.add("cli_ux", "invalid CAR clean failure", invalid_result["returncode"] != 0 and "Traceback" not in invalid_result["stderr"] + invalid_result["stdout"])


def check_recover_and_policy(evidence: Evidence) -> None:
    expected_types = {
        "python-library": "samples/repos/archetypes/python-library",
        "node-typescript-app": "samples/repos/archetypes/node-typescript-app",
        "github-action-repo": "samples/repos/archetypes/github-action-repo",
        "terraform-iac-repo": "samples/repos/archetypes/terraform-iac-repo",
        "monorepo-app": "samples/repos/archetypes/monorepo-app",
        "docs-heavy-repo": "samples/repos/archetypes/docs-heavy-repo",
    }
    for expected, rel_path in expected_types.items():
        snapshot = recover_repo(ROOT / rel_path)
        evidence.add("recover", f"detects {expected}", snapshot["project_type"] == expected, snapshot["project_type"])
        evidence.add("suggest_policy", f"suggest-policy for {expected}", bool(snapshot["suggested_policy"].get("rules")), str(snapshot["suggested_policy"]))

    no_ci = recover_repo(ROOT / "samples/repos/no-ci-vibe-repo")
    missing_types = {item["type"] for item in no_ci["missing_proof"]}
    evidence.add("recover", "missing proof output", {"test_result", "ci_status", "owner_approval"} <= missing_types, str(sorted(missing_types)), True)
    evidence.add("recover", "repair missions output", bool(no_ci["repair_missions"]))
    evidence.add("recover", "risk surface output", "auth" in no_ci["risk_surfaces"] and "generated_code" in no_ci["risk_surfaces"])


def check_gate_and_car(evidence: Evidence) -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    payment_car = TMP / "payment.car.json"
    payment = gate_repo(ROOT / "samples/repos/payment-change-with-tests", ROOT / "samples/policies/payment.certamerge.yml", output=payment_car)
    evidence.add("gate", "payment repo ALLOW", payment["verdict"] == "ALLOW", payment["verdict"], True)
    verification = verify_car(payment_car)
    evidence.add("car_integrity", "payment CAR verifies", verification["valid"], str(verification), True)
    evidence.add("car_integrity", "CAR content hash present", payment["car"]["integrity"]["content_hash"].startswith("sha256:"))
    evidence.add("car_integrity", "policy hash present", payment["car"]["policy"]["policy_hash"].startswith("sha256:"))
    evidence.add("car_integrity", "changed-files context present", "change_context_mode" in payment["car"]["change"])

    auth = gate_repo(ROOT / "samples/repos/auth-change-missing-tests", ROOT / "samples/policies/auth.certamerge.yml")
    evidence.add("gate", "auth repo would block in observe mode", auth["verdict"] == "OBSERVE_ONLY_WOULD_BLOCK", auth["verdict"], True)
    evidence.add("gate", "missing proof shown", bool(auth["missing_proof"]))

    changed_files = TMP / "changed-files.txt"
    changed_files.write_text("src/auth/session.js\n", encoding="utf-8")
    scoped = gate_repo(
        ROOT / "samples/repos/auth-change-missing-tests",
        ROOT / "samples/policies/auth.certamerge.yml",
        changed_files_path=changed_files,
    )
    evidence.add("gate", "explicit changed-files gate", scoped["car"]["change"]["change_context_mode"] == "explicit_changed_files")

    mutated = json.loads(payment_car.read_text(encoding="utf-8"))
    mutated["verdict"]["state"] = "BLOCK"
    tampered = TMP / "tampered-payment.car.json"
    tampered.write_text(json.dumps(mutated, indent=2), encoding="utf-8")
    tamper_result = verify_car(tampered)
    evidence.add("car_integrity", "mutation detection", not tamper_result["valid"], str(tamper_result), True)


def check_evidence_and_action(evidence: Evidence) -> None:
    targeted = run_command([sys.executable, "-m", "pytest", "community/tests/test_evidence_state_contract.py", "-q"], timeout=60)
    evidence.add("evidence_adapters", "evidence state contract tests", targeted["returncode"] == 0, targeted["stdout"] + targeted["stderr"], True)

    action_text = read_text(ROOT / "community/github-action/action.yml")
    evidence.add("github_action", "action metadata exists", "runs:" in action_text and "inputs:" in action_text)
    evidence.add("github_action", "CAR artifact language", "car" in action_text.lower())
    evidence.add("github_action", "observe/fail behavior", "fail" in action_text.lower() or "observe" in action_text.lower())


def check_usability_and_safety(evidence: Evidence) -> None:
    docs = [
        "README.md",
        "docs/community/quickstart.md",
        "docs/demo/5_MINUTE_PUBLIC_ALPHA_DEMO.md",
        "docs/demo/SAMPLE_OUTPUTS.md",
        "docs/community/agent-workflow.md",
        "docs/community/alpha-limitations.md",
        "docs/community/no-source-egress.md",
    ]
    for doc in docs:
        text = read_text(ROOT / doc)
        evidence.add("human_usability", f"{doc} exists and names CertaMerge", bool(text) and "CertaMerge" in text)

    agent_doc = read_text(ROOT / "docs/community/agent-workflow.md")
    evidence.add("agent_usability", "agent workflow doc covers rerun and CAR", "rerun" in agent_doc.lower() and "CAR" in agent_doc)
    evidence.add("agent_usability", "agent workflow fixtures exist", (ROOT / "samples/agent-workflows").exists())

    path_hits = scan_public_text([r"C:\\Users\\", r"\\\\wsl", r"\.codex"])
    secret_hits = scan_public_text([r"sk-[A-Za-z0-9]{20,}", r"ghp_[A-Za-z0-9]{20,}", r"AKIA[0-9A-Z]{16}", r"BEGIN (RSA |OPENSSH |)PRIVATE KEY"])
    unsafe_claim_hits = scan_public_text([r"SOC 2 compliant", r"ISO certified", r"guaranteed secure", r"guarantees security", r"production enterprise ready"])
    enterprise_hits = scan_public_text([r"certamerge_enterprise", r"enterprise/server"])

    evidence.add("security_privacy_safe_language", "no local path leakage", not path_hits, ", ".join(path_hits), True)
    evidence.add("security_privacy_safe_language", "no secret-looking leakage", not secret_hits, ", ".join(secret_hits), True)
    evidence.add("security_privacy_safe_language", "no unsafe claims", not unsafe_claim_hits, ", ".join(unsafe_claim_hits), True)
    evidence.add("security_privacy_safe_language", "no private enterprise leakage", not enterprise_hits, ", ".join(enterprise_hits), True)
    evidence.add("security_privacy_safe_language", "no telemetry claim present", "telemetry" in read_text(ROOT / "docs/community/no-source-egress.md").lower())


def build_result(evidence: Evidence) -> dict[str, Any]:
    categories = {category: evidence.score(category) for category in sorted(evidence.categories)}
    score = round(sum(categories.values()) / len(categories), 1) if categories else 0.0
    failures = evidence.failures()
    blockers = [item for item in failures if item.get("critical")]
    if blockers:
        verdict = "not-final-ready"
        final_verdict = "CERTAMERGE OPEN SOURCE NOT FINAL READY - missing: " + "; ".join(item["name"] for item in blockers[:5])
    elif score >= 3.0:
        verdict = "release-ready alpha"
        final_verdict = "CERTAMERGE OPEN SOURCE V0.1.0-ALPHA FINAL READY"
    else:
        verdict = "not-final-ready"
        final_verdict = "CERTAMERGE OPEN SOURCE NOT FINAL READY - missing: CPPEF score below 3.0"
    return {
        "product": "certamerge-open-source",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "score": score,
        "verdict": verdict,
        "final_verdict": final_verdict,
        "categories": categories,
        "checks": evidence.categories,
        "failures": failures,
        "blockers": blockers,
        "next_actions": [item["name"] for item in failures[:10]],
    }


def write_markdown(result: dict[str, Any]) -> None:
    lines = [
        "# CPPEF Open-Source Results",
        "",
        f"Generated: `{result['generated_at']}`",
        "",
        f"Score: `{result['score']}`",
        "",
        f"Verdict: `{result['verdict']}`",
        "",
        "## Category Scores",
        "",
        "| Category | Score |",
        "|---|---|",
    ]
    for category, score in result["categories"].items():
        lines.append(f"| `{category}` | `{score}` |")
    lines.extend(["", "## Failures", ""])
    if result["failures"]:
        for item in result["failures"]:
            severity = "blocker" if item.get("critical") else "finding"
            lines.append(f"- `{severity}` `{item['category']}`: {item['name']} - {item.get('detail', '')}")
    else:
        lines.append("No CPPEF failures recorded.")
    lines.extend(["", "## Final Verdict", "", "```text", result["final_verdict"], "```", ""])
    RESULT_MD.parent.mkdir(parents=True, exist_ok=True)
    RESULT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    TMP.mkdir(parents=True, exist_ok=True)
    evidence = Evidence()
    check_installation(evidence)
    check_cli_ux(evidence)
    check_recover_and_policy(evidence)
    check_gate_and_car(evidence)
    check_evidence_and_action(evidence)
    check_usability_and_safety(evidence)
    result = build_result(evidence)
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not result["blockers"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
