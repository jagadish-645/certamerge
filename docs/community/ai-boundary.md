# AI Boundary

AI may assist CertaMerge-adjacent workflows by drafting:

- explanations;
- repair prompts;
- policy suggestions;
- summaries.

AI must not:

- decide `ALLOW`;
- decide `BLOCK`;
- decide `HARD_BLOCK`;
- approve overrides;
- satisfy missing proof through prose;
- classify protected risk in the authorization path;
- approve its own generated change.

CertaMerge final verdicts are deterministic and must be replayable from policy, evidence, risk surface, mode, and evaluator version.
