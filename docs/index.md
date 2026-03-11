# local-privacy-guard

Pure-local privacy redaction for text and simple text files.

## What it does

`local-privacy-guard` replaces high-confidence sensitive values locally before you share logs, notes, or prompts with external systems.

## Security model

- zero network I/O in the main path
- default-irreversible output
- no raw sensitive matches in default JSON
- no context preview by default
- no persistence without explicit output
- no third-party runtime dependencies in v1

## Supported inputs

- stdin
- UTF-8 / UTF-8 BOM `.txt`, `.md`, `.json`, `.csv`, `.tsv`

## Current scope

- email
- conservative phone patterns
- IPv4
- URL query secrets
- common API key patterns
- conservative strong-format IDs / card-like strings

## Status

v0.1.0 — initial release candidate skeleton.

## Repository

See the repository README for usage, tests, and security notes.

#huanyuan
