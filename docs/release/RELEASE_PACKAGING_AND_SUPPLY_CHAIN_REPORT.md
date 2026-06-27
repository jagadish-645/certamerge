# Release Packaging And Supply Chain Report

Date: 2026-06-27

## Summary

CertaMerge Community Alpha can build Python wheel and sdist artifacts locally. Artifact metadata passes `twine check`. Release signing, SBOM automation, and provenance are still explicitly deferred alpha-hardening work.

## Packaging Metadata

`pyproject.toml` declares:

- project name: `certamerge`;
- version: `0.1.0`;
- Python requirement: `>=3.11`;
- license: MIT;
- README long description;
- console script: `certamerge = "certamerge.cli:app"`;
- runtime dependencies: Typer, PyYAML, jsonschema, pydantic.

## Commands Run

```powershell
python -m build
python -m twine check dist\*
python scripts\generate_checksums.py
```

Results:

- wheel build: passed;
- sdist build: passed;
- `twine check`: passed for wheel and sdist;
- checksum generation: passed.

Built artifacts:

```text
dist/certamerge-0.1.0-py3-none-any.whl
dist/certamerge-0.1.0.tar.gz
```

Artifact checksums:

```text
6df0f95112872d2ca0895b3672f3ac3000bc806c60602b5a65808cb0eb81a7fc  dist/certamerge-0.1.0-py3-none-any.whl
d97452d3028536c73e8186d8b60a6a8764a5f5211199ba91ccfa693a7f0725e7  dist/certamerge-0.1.0.tar.gz
```

## Dependency Health Note

`python -m pip check` in the current global Python environment reported an unrelated pre-existing conflict:

```text
opencv-python 4.12.0.88 requires numpy<2.3.0,>=2, but numpy 2.3.4 is installed.
```

CertaMerge does not depend on `opencv-python` or `numpy`. CI now runs `pip check` in a clean GitHub Actions environment. A final local release gate should also run in an isolated virtual environment.

## Supply Chain Status

| Control | Status |
|---|---|
| Wheel build | Passed locally |
| Sdist build | Passed locally |
| README metadata check | Passed through `twine check` |
| Checksum generation script | Added |
| SECURITY.md | Present |
| CONTRIBUTING.md | Present |
| Release signing | Deferred |
| SBOM generation | Planned |
| Provenance/in-toto/SLSA attestation | Planned |

## Verdict

```text
COMMUNITY ALPHA PACKAGING IS RELEASE-SHAPED — SIGNING, SBOM, AND PROVENANCE REMAIN FAST-FOLLOW HARDENING
```
