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
        "Live validation in a clean GitHub repo is still required",
        "Public/private split is applied",
        "It does not certify compliance",
        "Enterprise alpha code",
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


@pytest.mark.parametrize("input_name", ["policy", "repo", "output", "fail-on-block"])
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
    ],
)
def test_ci_contains_release_candidate_smoke_checks(required_ci_fragment: str) -> None:
    assert required_ci_fragment in text(".github/workflows/ci.yml")


@pytest.mark.parametrize(
    "required_path",
    [
        "docs/release/PUBLIC_PRIVATE_REPO_SPLIT_PLAN.md",
        "docs/release/REPOSITORY_ISOLATION_REPORT.md",
        "docs/release/PACKAGING_AND_INSTALL_REPORT.md",
        "docs/release/GITHUB_ACTION_LIVE_VALIDATION_CHECKLIST.md",
        "docs/release/CAR_INTEGRITY_RELEASE_DECISION.md",
        "docs/release/SBOM_AND_PROVENANCE_PLAN.md",
        "docs/release/RELEASE_ARTIFACT_INTEGRITY_PLAN.md",
    ],
)
def test_release_candidate_foundation_reports_exist(required_path: str) -> None:
    assert (ROOT / required_path).is_file()


@pytest.mark.parametrize(
    "required_phrase",
    [
        "certamerge              public",
        "certamerge_enterprise   private",
        "must not be pushed wholesale",
        "community-safe assets only",
        "Private assets",
        "public/private split is designed and locally staged",
    ],
)
def test_public_private_split_plan_prevents_enterprise_leakage(required_phrase: str) -> None:
    assert required_phrase in text("docs/release/PUBLIC_PRIVATE_REPO_SPLIT_PLAN.md")


def test_pyproject_has_public_alpha_metadata() -> None:
    data = tomllib.loads(text("pyproject.toml"))
    project = data["project"]
    assert project["name"] == "certamerge"
    assert project["version"] == "0.1.0"
    assert project["readme"] == "README.md"
    assert project["license"]["file"] == "LICENSE"
    assert "Development Status :: 3 - Alpha" in project["classifiers"]


def test_packaging_report_flags_enterprise_entrypoint_split_before_publication() -> None:
    report = text("docs/release/PACKAGING_AND_INSTALL_REPORT.md")
    assert "certamerge-enterprise = certamerge_enterprise.cli:app" in report
    assert "public repository must remove or split the enterprise entry point" in report


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
        "SBOM And Provenance Plan",
        "Release Artifact Integrity Plan",
        "Do not claim signed releases",
        "Not implemented yet",
        "Release artifact integrity is planned but not complete",
    ],
)
def test_release_trust_docs_are_honest_about_unfinished_artifact_integrity(required_phrase: str) -> None:
    combined = text("docs/release/SBOM_AND_PROVENANCE_PLAN.md") + text("docs/release/RELEASE_ARTIFACT_INTEGRITY_PLAN.md")
    assert required_phrase in combined
