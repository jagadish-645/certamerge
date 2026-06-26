# PR 2 Review And Next Action Report

## Review Scope

PR #2, `docs: professionalize public README`, was reviewed as a separate draft branch before this self-dogfood branch was prepared. It changes only `README.md` and is not a dependency of this branch.

## Current PR State

- Number: `#2`
- Title: `docs: professionalize public README`
- Head branch: `docs/professional-readme`
- Base branch: `main`
- State: open draft
- Mergeability: mergeable at the Git object level
- Reviews: none recorded
- Comments: none recorded
- Changed files: `README.md`
- Latest check result: `test` failed in run `28226483907`

## CI Finding

The failing CI is meaningful product evidence. The branch rewrites the public README in a way that removes executable public-alpha wording contracts asserted by `community/tests/test_public_release_candidate_contracts.py`.

The failed run collected `172` tests and reported `16 failed, 156 passed`. The failing tests show that the README no longer answers the first-30-second user questions and no longer preserves the exact public repository boundary sentence required by the release candidate contract.

## Removed Public Contract Areas

The failing test log shows missing README phrases for:

- `What is CertaMerge?`
- `Why does it exist?`
- `What problem does it solve?`
- `What is a CAR?`
- `Different from AI code review?`
- `Different from scanners?`
- `Install?`
- `Local Recover?`
- `Proof-only Gate?`
- `Verify a CAR?`
- `Output shape?`
- `Community/open source?`
- `Enterprise?`
- `Non-claims?`
- `Alpha limits?`

The boundary check also showed that the combined public docs no longer contained `This repository is the community alpha surface`.

## Decision

Do not merge PR #2 into this self-dogfood branch. Keep it draft until the professionalized README preserves the executable public contract language.

## Next Action

The PR #2 owner should revise the README so it keeps the tested public-alpha questions, the community boundary, the non-claims language, and the copy-paste command block. After that, rerun CI and then run CertaMerge Gate on the revised branch.

## CertaMerge Lesson

PR #2 proves why CertaMerge should govern documentation changes too. A polished rewrite can still remove product-critical proof language. The correct response is not to block style improvements; it is to require evidence that the public contract remains intact.
