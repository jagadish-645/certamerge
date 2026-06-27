# No Source Egress

CertaMerge Community runs locally by default.

It may read local metadata and selected configuration files needed for proof detection, but it must not transmit source code to a vendor service by default.

CertaMerge Community does not send telemetry, analytics, source code, diffs, secrets, scanner payloads, CARs, or Repo Proof Snapshots to a vendor service by default. Any future telemetry must be explicit opt-in, metadata-only, and outside the authorization path.

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
