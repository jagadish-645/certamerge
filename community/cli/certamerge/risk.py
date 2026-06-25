from __future__ import annotations

from fnmatch import fnmatch
from pathlib import Path

IGNORED_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache"}

RISK_PATTERNS = {
    "auth": ["*auth*", "*session*", "*login*", "*oauth*"],
    "payments": ["*payment*", "*billing*", "*refund*", "*stripe*"],
    "config": ["*.env*", "*config*", "*settings*"],
    "deployment": ["*deploy*", "Dockerfile", "docker-compose.*", ".github/workflows/*"],
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


def detect_project_type(files: list[Path]) -> str:
    names = {p.as_posix() for p in files}
    if "package.json" in names:
        return "node"
    if "pyproject.toml" in names or "requirements.txt" in names:
        return "python"
    if "go.mod" in names:
        return "go"
    return "unknown"


def detect_risk_surfaces(files: list[Path]) -> list[str]:
    surfaces: set[str] = set()
    for file_path in files:
        value = file_path.as_posix().lower()
        for surface, patterns in RISK_PATTERNS.items():
            if any(fnmatch(value, pattern.lower()) for pattern in patterns):
                surfaces.add(surface)
    return sorted(surfaces) or ["none"]
