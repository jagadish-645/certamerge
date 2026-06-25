# CertaMerge v0.1.0 Alpha Verification

Run these commands from the repository root after cloning the public repository.

```powershell
python -m pip install -e .
python -m certamerge --help
python -m certamerge recover samples/repos/no-ci-vibe-repo
python -m certamerge gate --repo samples/repos/payment-change-with-tests --policy samples/policies/payment.certamerge.yml --output .tmp/payment.car.json
python -m certamerge verify-car .tmp/payment.car.json
python -m certamerge explain-car .tmp/payment.car.json
python -m pytest
python -m compileall community
python -m certamerge verify-car samples/cars/allow.example.json
```

Expected verification result:

```text
All community CLI smoke flows pass.
All tests pass.
Community Python modules compile.
Sample CAR verification returns valid: true.
```

These checks validate local CLI behavior, sample policy evaluation, CAR creation, CAR verification, test coverage, and importability. They do not validate production deployment hardening, signed releases, SBOM generation, or cryptographic CAR signing.
