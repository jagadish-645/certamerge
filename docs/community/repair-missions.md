# Repair Missions

Repair missions turn missing proof into finite action.

Example:

```text
Mission: R-TESTS-001
Objective: Produce tests evidence for the current change context.
Acceptance: tests evidence is present, fresh, and bound to the current change.
Re-run: python -m certamerge gate --repo . --policy .certamerge.yml
```

A repair mission is accepted only after CertaMerge re-evaluates the evidence. AI-generated text or a claim that work was done does not satisfy proof.
