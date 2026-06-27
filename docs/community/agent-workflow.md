# Agent Workflow

CertaMerge can be used by AI coding agents without making an AI responsible for the final authorization verdict. The agent may inspect CertaMerge output, repair missing proof, and rerun the gate. The verdict remains deterministic policy output.

## Workflow

1. The agent creates or modifies a change in a local branch.
2. The agent runs Recover:

```powershell
python -m certamerge recover . --json
```

3. The agent reads:

- `verdict`;
- `policy_reason`;
- `missing_proof`;
- `repair_missions`;
- `accountable_next_action`;
- CAR context.

4. The agent generates or attaches the missing proof that is safe for the repository:

- tests or test result evidence;
- CI evidence;
- owner approval evidence;
- scanner evidence;
- docs build evidence;
- Terraform validation or plan evidence.

5. The agent suggests a starter policy when one is missing:

```powershell
python -m certamerge suggest-policy . --output .certamerge.yml
```

6. The agent gates the change:

```powershell
python -m certamerge gate --repo . --policy .certamerge.yml --output .tmp/certamerge.car.json --json
```

7. The agent verifies the CAR:

```powershell
python -m certamerge verify-car .tmp/certamerge.car.json
```

8. The agent explains the CAR in the PR summary:

```powershell
python -m certamerge explain-car .tmp/certamerge.car.json --json
```

9. The agent includes only the proof summary in the PR, not raw source code, raw diffs, secrets, private keys, or scanner payloads.

## Agent Output Contract

An agent-generated proof summary must include:

- verdict;
- policy reason;
- missing proof;
- accountable next action;
- CAR path or artifact reference;
- CAR verification result;
- limitations, including unsigned CAR status if signing is not enabled.

## Required Agent Discipline

- Do not rewrite policy to make a failing change pass.
- Do not invent proof.
- Do not claim that CertaMerge says code is secure.
- Do not treat `OBSERVE_ONLY_WOULD_ALLOW` as production authorization.
- Do not send source code to external services as part of the proof loop.
- Do not use an LLM as the final authorization decision maker.

## Example Agent PR Summary

```text
CertaMerge verdict: OBSERVE_ONLY_WOULD_BLOCK
Policy reason: Auth-path changes require test result and owner approval evidence.
Missing proof: test_result, owner_approval
Accountable next action: policy-owner - add passing test evidence and owner approval, then rerun CertaMerge Gate.
CAR: .tmp/certamerge.car.json
Verification: valid true
Limitations: observe mode only; this is not a production enforcement claim.
```
