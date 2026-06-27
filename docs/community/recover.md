# Recover

`recover` inspects a repository without requiring a `.certamerge.yml` first.

It is a repo-readiness proof discovery command, not a scanner and not an AI reviewer.

## Command

```powershell
python -m certamerge recover <repo>
```

Optional snapshot output:

```powershell
python -m certamerge recover <repo> --output .tmp/recover.snapshot.json
```

Optional starter policy preview:

```powershell
python -m certamerge recover <repo> --suggest-policy
```

## What Recover Infers

Recover deterministically inspects file paths, manifests, workflow files, and metadata evidence references to infer:

- repo profile type;
- package ecosystems;
- CI presence;
- test command or test file presence;
- lockfile, SBOM, or dependency evidence;
- security policy presence;
- license presence;
- GitHub Action metadata;
- Terraform/IaC files;
- docs-heavy repo indicators;
- risk surfaces;
- missing proof;
- repair missions;
- starter policy recommendation.

## Example Output

```text
Verdict: NEEDS_EVIDENCE
Policy reason: Recover checks repo-adaptive proof signals without claiming security correctness.
Repo profile: terraform-iac-repo
Ecosystems: docs, terraform
Missing proof: terraform_validation, terraform_plan, owner_approval, security_doc
Accountable next action: repo-owner - Review generated repair missions and rerun CertaMerge after evidence is present.
```

## What Recover Does Not Do

- It does not certify security or compliance.
- It does not run scanners.
- It does not inspect raw source code for vulnerabilities.
- It does not use an LLM for final classification.
- It does not transmit repository contents to a vendor service.

## Interpretation

Recover should answer:

```text
What proof is present?
What proof is missing?
Why does this repo shape need that proof?
What should happen next?
Can a future decision be recorded as a CAR?
```

If Recover returns only a generic checklist, treat that as a product bug.
