# Offline specification checks

Run from the repository root with Python 3.12 or later:

```sh
python -m unittest discover -s tests -v
```

No packages, credentials, network access, model calls or mailbox access are needed.
This remains a **no-code protocol**: `spec_model.py` is a **test-only oracle**, not
a runtime protocol engine or a connector to deploy.

The checks parse all ten draft examples from `examples/`, with explicitly
assumed service metadata (the Markdown examples contain no real envelope).
Adversarial fixtures cover draft provenance, recipients, reply/forward/quoted
carriers, missing metadata, block/key syntax, values and supported versions.
Timeline vectors exercise §7 renewal, expiry, hand-off, competing claims,
close/reopen and ambiguity. Recording/work vectors cover §6.1 exceptions,
frequency limits, read-only mode, joining/leaving and claim confirmation.

The model only handles simple fixture text/HTML and supplied metadata. It cannot
prove that a real connector exposes trustworthy metadata or enforces operations,
that a log's evidence is true, that an AI follows the instructions, that mailbox
search is complete, or that concurrent work executes once. Its HTML handling is
not a general MIME or prompt-injection sanitizer. Keep the examples, vectors and
written specification aligned when reviewing changes; these tests do not replace
real mailbox validation or the unreleased STOP in `SETUP.md`.
