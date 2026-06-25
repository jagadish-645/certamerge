# Examples

Sample repos:

- `samples/repos/basic-node-app`
- `samples/repos/auth-change-missing-tests`
- `samples/repos/payment-change-with-tests`
- `samples/repos/no-ci-vibe-repo`

Sample policies:

- `samples/policies/basic.certamerge.yml`
- `samples/policies/auth.certamerge.yml`
- `samples/policies/payment.certamerge.yml`

Sample CARs:

- `samples/cars/allow.example.json`
- `samples/cars/needs-evidence.example.json`
- `samples/cars/block.example.json`
- `samples/cars/repair-required.example.json`
- `samples/cars/override-recorded.example.json`

Run:

```powershell
python -m certamerge gate --repo samples/repos/payment-change-with-tests --policy samples/policies/payment.certamerge.yml --output samples/cars/local-demo.json
```

Sample evidence fixtures:

- `samples/evidence/sarif-negative.example.sarif`
- `samples/evidence/sarif-failed.example.sarif`
- `samples/evidence/sarif-malformed.example.sarif`
- `samples/evidence/owner-approval-stale.example.json`
- `samples/evidence/owner-approval-denied.example.json`
- `samples/evidence/test-result-failed.example.json`

Sample PR metadata fixtures:

- `samples/prs/auth-missing-proof.pr.json`
- `samples/prs/payment-allow.pr.json`
