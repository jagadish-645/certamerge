# CertaMerge v0.1.0 Alpha Checksums

This alpha does not publish signed distribution archives yet. The checksums below cover selected source-controlled public alpha files and locally built distribution artifacts so maintainers can detect accidental drift in important examples and packaging metadata.

```text
656862867cbdfa6d93794027dddc7bd399c2d5a828539b2d029dbe5c49f65c0d  pyproject.toml
bd2c9553872e01aced271c4ec8c83de1615f44fdefada2a216b29da1c7c35ef4  community/github-action/action.yml
a2c052d6ac767adeb0ea7faef0299eea9e40a969e840746463a247bf8da8c439  samples/cars/allow.example.json
4442cc4e537ac3ea5f5f79e0077243f34147e066c36f98ea987bc1b24ab96125  samples/cars/block.example.json
dcdbf475ce82c55d1d998e93aa5a4b34e515b56c6e8f8a4434e1299f571558ab  samples/cars/needs-evidence.example.json
6df0f95112872d2ca0895b3672f3ac3000bc806c60602b5a65808cb0eb81a7fc  dist/certamerge-0.1.0-py3-none-any.whl
d97452d3028536c73e8186d8b60a6a8764a5f5211199ba91ccfa693a7f0725e7  dist/certamerge-0.1.0.tar.gz
```

Checksums were generated with:

```powershell
python scripts\generate_checksums.py
```

Before a stable release, CertaMerge should publish signed provenance and SBOM output in addition to checksums.
