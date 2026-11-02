# Changelog

All notable changes to this project are recorded here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions: [Semantic Versioning](https://semver.org/).

## [1.0.0] - Unreleased

Work in progress. Not tested with real mailboxes yet.

### Added

- First version of the protocol (`postbox-version: 1`).
- Logs are drafts with no recipients in the owner's mailbox. They are never sent.
- README.md (Japanese, with a short English summary), SETUP.md (for agents, English with Japanese notes), and SPEC.md.
- Eight core rules, including a list of the only mailbox actions agents may take; the valid-log check; case-ids; claim and hand-off with a 48-hour limit; the rule card; the `postbox-setup` join log; log, read-only and inactive modes; and the optional `postbox` label.
- Six example documents in `examples/`, including reopening and correcting a closed case.
- Offline conformance cases and test-only models; these do not certify real agents or mail connectors.

### Fixed

- Separate case-work eligibility from permission to record facts, reopenings, corrections, digests and setup records.
- Define active claim renewal, exact 48-hour expiry, hand-off/closure release and non-revival of expired claims consistently across the specification and rule cards.
- Validate draft metadata, all recipient lists, standalone/unquoted origin, supported version and field values before using a log for state.
- Require independently enforced mail-operation boundaries; distinguish Gmail OAuth scopes from connector restrictions and fall back to verified read-only/inactive modes.
- Remove Gmail custom-label setup/search assumptions and use draft discovery instead.
- Describe concurrency as best effort, require claim confirmation/recheck and explain when an independent single-execution mechanism is necessary.
- Update Japanese/English explanations and all four diagrams while retaining the unreleased setup prohibition.

[1.0.0]: https://github.com/aigamoid/ai-postbox-protocol/releases/tag/v1.0.0
