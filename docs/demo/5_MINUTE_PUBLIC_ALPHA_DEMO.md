# 5-Minute Public Alpha Demo

## Goal

Show the core CertaMerge community loop:

```text
Recover proof gaps.
Gate a change.
Record a CAR.
Verify the CAR offline.
```

## Setup

```powershell
python -m pip install -e .
```

## 1. Inspect The CLI

```powershell
python -m certamerge --help
```

## 2. Recover Proof Gaps In A Sample Repo

```powershell
python -m certamerge recover samples/repos/no-ci-vibe-repo
```

Expected shape:

```text
Verdict: NEEDS_EVIDENCE
Policy reason: Recover checks basic proof signals without claiming security correctness.
Missing proof: test_result, ci_status, owner_approval
Accountable next action: repo-owner - Review generated repair missions and rerun CertaMerge after evidence is present.
```

## 3. Gate A Payment Sample With Evidence Present

```powershell
python -m certamerge gate --repo samples/repos/payment-change-with-tests --policy samples/policies/payment.certamerge.yml --output .tmp/payment.car.json
```

Expected shape:

```text
Verdict: ALLOW
Policy reason: All matched policy requirements are satisfied.
Missing proof: No missing proof required by current policy.
Accountable next action: repo-owner - Proceed with record.
CAR: .tmp/payment.car.json
```

## 4. Verify The CAR Offline

```powershell
python -m certamerge verify-car .tmp/payment.car.json
```

Expected shape:

```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "verdict": "ALLOW"
}
```

## 5. Explain The CAR

```powershell
python -m certamerge explain-car .tmp/payment.car.json
```

Expected shape:

```text
Verdict: ALLOW
Policy reason: All matched policy requirements are satisfied.
Missing proof: No missing proof required by current policy.
Accountable next action: repo-owner - Proceed with record.
```

## Demo Boundary

This demo proves the community alpha workflow. It does not prove production deployment readiness, cryptographic CAR signing, security certification, or compliance certification.
