from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def default_paths() -> list[Path]:
    dist = Path("dist")
    if dist.is_dir():
        return sorted(path for path in dist.iterdir() if path.is_file())
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate SHA-256 checksums for CertaMerge release artifacts.")
    parser.add_argument("paths", nargs="*", type=Path, help="Files to checksum. Defaults to files under dist/.")
    args = parser.parse_args()
    paths = args.paths or default_paths()
    if not paths:
        parser.error("no files supplied and dist/ contains no files")
    for path in paths:
        if not path.is_file():
            parser.error(f"not a file: {path}")
        print(f"{sha256_file(path)}  {path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
