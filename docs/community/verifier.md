# CAR Verifier

Commands:

```powershell
python -m certamerge verify-car samples/cars/allow.example.json
python -m certamerge explain-car samples/cars/allow.example.json
```

`verify-car` emits machine-readable JSON:

```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "car_id": "car_sample_allow_001",
  "verdict": "ALLOW"
}
```

`explain-car` emits the workflow-native summary:

```text
CAR.
Verdict.
Policy reason.
Missing proof.
Accountable next action.
CAR state.
```

The verifier rejects inconsistent states such as `ALLOW` with missing proof.
