from __future__ import annotations

from fnmatch import fnmatch
from pathlib import Path

IGNORED_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache"}
PROFILE_FIXTURE_PREFIXES = ("samples/", "docs/demo/")

RISK_PATTERNS = {
    "auth": ["*auth*", "*session*", "*login*", "*oauth*"],
    "payments": ["*payment*", "*billing*", "*refund*", "*stripe*"],
    "config": ["*.env*", "*config*", "*settings*"],
    "deployment": ["*deploy*", "Dockerfile", "docker-compose.*", ".github/workflows/*"],
    "iac": ["*.tf", "*.tfvars", "terraform.*"],
    "docs": ["docs/*", "mkdocs.yml", "docusaurus.config.*", "README.md"],
    "github_action": ["action.yml", "action.yaml", "composite.yml"],
    "dependency": [
        "package.json",
        "package-lock.json",
        "pnpm-lock.yaml",
        "yarn.lock",
        "requirements*.txt",
        "pyproject.toml",
        "poetry.lock",
        "go.mod",
        "go.sum",
    ],
    "database": ["*migration*", "*schema*", "*prisma*", "*db*"],
    "generated_code": ["*lovable*", "*bolt*", "*v0*", "*generated*"],
}


def iter_repo_files(repo: Path) -> list[Path]:
    files: list[Path] = []
    for path in repo.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path.is_file():
            files.append(path.relative_to(repo))
    return sorted(files, key=lambda p: p.as_posix())


def profile_signal_files(files: list[Path]) -> list[Path]:
    filtered = [file_path for file_path in files if not file_path.as_posix().startswith(PROFILE_FIXTURE_PREFIXES)]
    return filtered or files


def detect_project_type(files: list[Path]) -> str:
    files = profile_signal_files(files)
    names = {p.as_posix() for p in files}
    if "action.yml" in names or "action.yaml" in names:
        return "github-action-repo"
    if any(name.endswith(".tf") for name in names):
        return "terraform-iac-repo"
    if any(name.startswith("apps/") for name in names) and any(name.startswith("packages/") for name in names):
        return "monorepo-app"
    if "mkdocs.yml" in names or "docusaurus.config.js" in names or ("docs/index.md" in names and not any(name.startswith("src/") for name in names)):
        return "docs-heavy-repo"
    if "package.json" in names and ("tsconfig.json" in names or any(name.endswith(".ts") or name.endswith(".tsx") for name in names)):
        return "node-typescript-app"
    if "package.json" in names:
        return "node"
    if "pyproject.toml" in names or "requirements.txt" in names:
        return "python-library"
    if "go.mod" in names:
        return "go"
    return "unknown"


def detect_risk_surfaces(files: list[Path]) -> list[str]:
    files = profile_signal_files(files)
    surfaces: set[str] = set()
    for file_path in files:
        value = file_path.as_posix().lower()
        for surface, patterns in RISK_PATTERNS.items():
            if any(fnmatch(value, pattern.lower()) for pattern in patterns):
                surfaces.add(surface)
    return sorted(surfaces) or ["none"]
