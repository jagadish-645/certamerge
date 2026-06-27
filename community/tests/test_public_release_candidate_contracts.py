from __future__ import annotations

from pathlib import Path

import pytest
import tomllib
import yaml
from typer.testing import CliRunner

from certamerge.cli import app

ROOT = Path(__file__).resolve().parents[2]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "required_phrase",
    [
        "What is CertaMerge?",
        "Why does it exist?",
        "What problem does it solve?",
        "What is a CAR?",
        "Different from AI code review?",
        "Different from scanners?",
        "Install?",
        "Local Recover?",
        "Proof-only Gate?",
        "Verify a CAR?",
        "Output shape?",
        "Community/open source?",
        "Enterprise?",
        "Non-claims?",
        "Alpha limits?",
    ],
)
def test_readme_answers_first_30_second_questions(required_phrase: str) -> None:
    assert required_phrase in text("README.md")


@pytest.mark.parametrize(
    "required_command",
    [
        "python -m pip install -e .",
        "python -m certamerge --help",
        "python -m certamerge recover samples/repos/no-ci-vibe-repo",
        "python -m certamerge gate --repo samples/repos/payment-change-with-tests --policy samples/policies/payment.certamerge.yml --output .tmp/payment.car.json",
        "python -m certamerge verify-car .tmp/payment.car.json",
        "python -m certamerge explain-car .tmp/payment.car.json",
    ],
)
def test_readme_and_quickstart_publish_copy_paste_commands(required_command: str) -> None:
    combined = text("README.md") + text("docs/community/quickstart.md")
    assert required_command in combined


@pytest.mark.parametrize(
    "required_phrase",
    [
        "Community alpha is a useful local proof spine",
        "not cryptographically signed",
        "sample live-validation paths exist",
        "community-safe assets",
        "It does not certify compliance",
        "Advanced enterprise deployment",
        "GitHub Action static validation",
        "known limitations are public",
    ],
)
def test_alpha_limitations_are_explicit(required_phrase: str) -> None:
    assert required_phrase in text("docs/community/alpha-limitations.md")


@pytest.mark.parametrize(
    "required_phrase",
    [
        "verifier-checked SHA-256 content hash",
        "does not implement cryptographic CAR signing",
        "signer identity",
        "non-repudiation",
        "public key manifest",
        "Community alpha CARs are integrity-bound",
    ],
)
def test_car_integrity_doc_separates_hashes_from_signing(required_phrase: str) -> None:
    assert required_phrase in text("docs/community/car-integrity.md")


def test_github_action_installs_certamerge_from_action_checkout_path() -> None:
    action_text = text("community/github-action/action.yml")
    assert 'python -m pip install "$GITHUB_ACTION_PATH/../.."' in action_text
    assert "python -m pip install ." not in action_text


def test_github_action_summary_survives_gate_step_failure() -> None:
    action_text = text("community/github-action/action.yml")
    assert "if [ -f certamerge-summary.txt ]" in action_text
    assert "Check the prior action step logs" in action_text


@pytest.mark.parametrize("input_name", ["policy", "repo", "output", "fail-on-block", "artifact-name"])
def test_github_action_metadata_inputs_are_release_candidate_ready(input_name: str) -> None:
    action = yaml.safe_load(text("community/github-action/action.yml"))
    assert input_name in action["inputs"]


@pytest.mark.parametrize("output_name", ["car-path", "verdict", "summary-path"])
def test_github_action_metadata_outputs_are_release_candidate_ready(output_name: str) -> None:
    action = yaml.safe_load(text("community/github-action/action.yml"))
    assert output_name in action["outputs"]


@pytest.mark.parametrize(
    "required_ci_fragment",
    [
        "python -m pip install pytest",
        "python -m certamerge recover samples/repos/no-ci-vibe-repo",
        "python -m certamerge gate --repo samples/repos/payment-change-with-tests --policy samples/policies/payment.certamerge.yml --output .tmp/payment.car.json",
        "python -m certamerge verify-car .tmp/payment.car.json",
        "$GITHUB_ACTION_PATH/../..",
        "Validate GitHub Action metadata",
        "CertaMerge Action Live Validation",
    ],
)
def test_ci_contains_release_candidate_smoke_checks(required_ci_fragment: str) -> None:
    workflow_text = text(".github/workflows/ci.yml") + text(".github/workflows/certamerge-action-validation.yml")
    assert required_ci_fragment in workflow_text


def test_self_dogfood_workflow_runs_certamerge_on_this_repo() -> None:
    workflow = yaml.safe_load(text(".github/workflows/certamerge-proof-gate.yml"))
    assert "pull_request" in workflow[True]
    job_text = text(".github/workflows/certamerge-proof-gate.yml")
    assert "uses: ./community/github-action" in job_text
    assert "policy: .certamerge.yml" in job_text
    assert "repo: ." in job_text
    assert ".tmp/certamerge-pr.car.json" in job_text
    assert "python -m certamerge verify-car .tmp/certamerge-pr.car.json" in job_text
    assert "certamerge-pr-car" in job_text


@pytest.mark.parametrize(
    "required_path",
    [
        ".github/ISSUE_TEMPLATE/bug_report.md",
        ".github/ISSUE_TEMPLATE/alpha_feedback.md",
        ".github/ISSUE_TEMPLATE/proof_gap_example.md",
        ".github/ISSUE_TEMPLATE/evidence_adapter_request.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
        "docs/community/feedback.md",
        "docs/community/self-dogfooding.md",
    ],
)
def test_self_dogfood_feedback_and_template_surfaces_exist(required_path: str) -> None:
    assert (ROOT / required_path).is_file()


@pytest.mark.parametrize(
    "forbidden_fragment",
    [
        "C:\\Users\\",
        "sk-",
        "gh" + "p_",
        "github" + "_pat_",
        "BEGIN " + "PRIVATE KEY",
    ],
)
def test_public_templates_do_not_contain_local_paths_or_token_shapes(forbidden_fragment: str) -> None:
    template_paths = [
        ".github/ISSUE_TEMPLATE/bug_report.md",
        ".github/ISSUE_TEMPLATE/alpha_feedback.md",
        ".github/ISSUE_TEMPLATE/proof_gap_example.md",
        ".github/ISSUE_TEMPLATE/evidence_adapter_request.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
        "docs/community/feedback.md",
        "docs/community/self-dogfooding.md",
    ]
    combined = "\n".join(text(path) for path in template_paths)
    assert forbidden_fragment not in combined


@pytest.mark.parametrize(
    "required_phrase",
    [
        "Why It Matters",
        "CertaMerge Proof",
        "Verdict:",
        "Policy reason:",
        "Missing proof:",
        "Accountable next action:",
        "CAR:",
        "Verification:",
        "Limitations:",
    ],
)
def test_pull_request_template_requires_certamerge_proof_language(required_phrase: str) -> None:
    assert required_phrase in text(".github/PULL_REQUEST_TEMPLATE.md")


@pytest.mark.parametrize("command_name", ["verify-car", "explain-car"])
def test_car_reader_commands_return_nonzero_for_missing_file(command_name: str, tmp_path: Path) -> None:
    missing = tmp_path / "missing.car.json"
    result = CliRunner().invoke(app, [command_name, str(missing)])
    assert result.exit_code == 1
    assert "CAR file could not be read" in result.output


@pytest.mark.parametrize(
    "required_path",
    [
        "docs/release/V0_1_0_ALPHA_RELEASE_NOTES.md",
        "docs/release/V0_1_0_ALPHA_VERIFICATION.md",
        "docs/release/V0_1_0_ALPHA_CHECKSUMS.md",
        "docs/release/PUBLIC_ALPHA_GO_NO_GO.md",
        "docs/release/CERTAMERGE_PUBLIC_RELEASE_CANDIDATE_REPORT.md",
        "docs/demo/5_MINUTE_PUBLIC_ALPHA_DEMO.md",
        "docs/demo/SAMPLE_OUTPUTS.md",
    ],
)
def test_release_candidate_foundation_reports_exist(required_path: str) -> None:
    assert (ROOT / required_path).is_file()


@pytest.mark.parametrize(
    "required_phrase",
    [
        "This repository is the community alpha surface",
        "advanced enterprise-only code and docs out of the community repository",
        "public repository contains only community-safe assets",
        "intentionally excludes",
        "enterprise runtime services",
        "internal strategy and agent-system material",
    ],
)
def test_public_repository_boundary_prevents_enterprise_leakage(required_phrase: str) -> None:
    combined = (
        text("README.md")
        + text("SECURITY.md")
        + text("docs/community/alpha-limitations.md")
        + text("docs/release/CERTAMERGE_PUBLIC_RELEASE_CANDIDATE_REPORT.md")
    )
    assert required_phrase in combined


def test_pyproject_has_public_alpha_metadata() -> None:
    data = tomllib.loads(text("pyproject.toml"))
    project = data["project"]
    assert project["name"] == "certamerge"
    assert project["version"] == "0.1.0"
    assert project["readme"] == "README.md"
    assert project["license"] == "MIT"
    assert project["license-files"] == ["LICENSE"]
    assert "Development Status :: 3 - Alpha" in project["classifiers"]
    assert "License :: OSI Approved :: MIT License" not in project["classifiers"]


def test_public_pyproject_has_no_enterprise_entrypoint() -> None:
    project_text = text("pyproject.toml")
    assert "certamerge-enterprise" not in project_text
    assert "certamerge_enterprise" not in project_text


def test_verify_car_returns_nonzero_for_malformed_json(tmp_path: Path) -> None:
    bad_car = tmp_path / "bad.car.json"
    bad_car.write_text("{not-json", encoding="utf-8")
    result = CliRunner().invoke(app, ["verify-car", str(bad_car)])
    assert result.exit_code == 1
    assert "CAR JSON could not be parsed" in result.output


def test_gate_returns_nonzero_for_invalid_policy(tmp_path: Path) -> None:
    policy = tmp_path / "invalid.yml"
    policy.write_text("mode: proof_only\nrules: []\n", encoding="utf-8")
    result = CliRunner().invoke(
        app,
        [
            "gate",
            "--repo",
            str(ROOT / "samples" / "repos" / "payment-change-with-tests"),
            "--policy",
            str(policy),
        ],
    )
    assert result.exit_code != 0
    assert "Policy requires version." in result.output


@pytest.mark.parametrize(
    "forbidden_claim",
    [
        "makes code secure",
        "certifies compliance",
        "guarantees production safety",
        "cryptographically signs CARs in community alpha",
    ],
)
def test_security_doc_lists_forbidden_claims_as_non_claims(forbidden_claim: str) -> None:
    security = text("SECURITY.md")
    assert forbidden_claim in security
    assert "must not claim" in security


@pytest.mark.parametrize(
    "required_phrase",
    [
        "v0.1.0 Alpha Checksums",
        "does not publish signed distribution archives yet",
        "signed release/SBOM automation remains release-hardening work",
        "Cryptographic CAR signing is not implemented yet",
        "These checks validate local CLI behavior",
    ],
)
def test_release_trust_docs_are_honest_about_unfinished_artifact_integrity(required_phrase: str) -> None:
    combined = (
        text("docs/release/V0_1_0_ALPHA_CHECKSUMS.md")
        + text("docs/release/V0_1_0_ALPHA_VERIFICATION.md")
        + text("docs/release/PUBLIC_ALPHA_GO_NO_GO.md")
        + text("docs/release/CERTAMERGE_PUBLIC_RELEASE_CANDIDATE_REPORT.md")
    )
    assert required_phrase in combined
