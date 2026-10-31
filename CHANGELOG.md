# Changelog

All notable changes to this project are recorded here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions: [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-11-01

### Added

- First release of the protocol (`postbox-version: 1`).
- Logs are drafts with no recipients in the owner's mailbox. They are never sent.
- README.md (Japanese, with a short English summary), SETUP.md (for agents, English with Japanese notes), and SPEC.md.
- Eight core rules, including a list of the only mailbox actions agents may take; the valid-log check; case-ids; claim and hand-off with a 48-hour limit; the rule card; the `postbox-setup` join log; log, read-only and inactive modes; and the optional `postbox` label.
- Five example logs in `examples/`.

[1.0.0]: https://github.com/aigamoid/ai-postbox-protocol/releases/tag/v1.0.0
