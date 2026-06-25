# No Source Egress

CertaMerge Community runs locally by default.

It may read local metadata and selected configuration files needed for proof detection, but it must not transmit source code to a vendor service by default.

CARs and Repo Proof Snapshots may contain:

- file paths;
- package manager names;
- CI config presence;
- evidence states;
- artifact references;
- hashes;
- policy IDs;
- verdict traces.

CARs and snapshots must not contain:

- raw source code;
- raw diffs;
- secrets;
- tokens;
- private keys;
- credentials;
- unredacted scanner payloads.
