# Packaging And Install Report

## Package Name

```text
certamerge
```

## Current Version

```text
0.1.0
```

## Entry Points

Current workspace entry points:

```text
certamerge = certamerge.cli:app
certamerge-enterprise = certamerge_enterprise.cli:app
```

The public repository must remove or split the enterprise entry point before public publication.

## Install Command Tested

Clean editable install was tested in a local virtual environment:

```powershell
python -m pip install -e .
```

## CLI Commands Tested

```powershell
python -m certamerge --help
certamerge --help
python -m certamerge recover samples/repos/no-ci-vibe-repo
python -m certamerge gate --repo samples/repos/payment-change-with-tests --policy samples/policies/payment.certamerge.yml --output .tmp/payment.car.json
python -m certamerge verify-car .tmp/payment.car.json
python -m certamerge explain-car .tmp/payment.car.json
```

## Observed Results

- Module route works.
- Console script route worked inside the clean virtual environment.
- Recover returned `NEEDS_EVIDENCE` for the no-CI sample.
- Gate returned `ALLOW` for the payment sample.
- Generated CAR verified successfully.
- Generated CAR explained successfully.

## Metadata Hardened

`pyproject.toml` now includes:

- readme reference;
- license reference;
- maintainer author entry;
- keywords;
- alpha classifiers;
- console entry points.

## Limitations

- Current workspace packaging includes enterprise alpha packages and entry point.
- Public `certamerge` packaging must be community-only before push.
- Release wheels and source distributions have not been built or signed.
- Release checksums and SBOM are not published.
- The current verified path is editable install from repository root.

## Verdict

Local packaging is functional for release-candidate testing.

Public package publication is blocked until the community/private package split is applied.
