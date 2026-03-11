---
name: local-privacy-guard
description: Pure-local privacy redaction for text and simple text files. Use this whenever the user wants to redact sensitive information before sending it to an external model, sharing logs, posting debug output, or exporting notes, especially when they want a zero-network, default-safe workflow. Prefer this skill over generic text processing whenever privacy protection is the main goal.
---

# Local Privacy Guard

A pure-local, zero-network, default-irreversible privacy redaction skill.

## When to use

Use this skill when the user wants to:
- redact private text before sending it to an external model
- sanitize logs, transcripts, notes, or incident reports
- process `.txt`, `.md`, `.json`, `.csv`, or `.tsv` locally
- avoid cloud APIs, telemetry, or dependency-heavy privacy tooling

Do **not** use this skill for:
- PDF/DOCX/image/audio/video inputs
- deanonymization / restore flows
- high-recall semantic entity detection
- cloud-backed privacy tooling

## Safety invariants

These rules are non-negotiable for v1:
- Never make network requests in the main flow
- Never include raw sensitive matches in default JSON output
- Never include surrounding-context previews in default output
- Never write files unless the user explicitly asked for output
- Never create persistent side effects by default
- Never bypass path guards with `--force`
- Never require third-party dependencies at runtime for v1

## Supported inputs

- `stdin` (preferred for direct sensitive text)
- UTF-8 / UTF-8 BOM encoded:
  - `.txt`
  - `.md`
  - `.json`
  - `.csv`
  - `.tsv`

## Detection scope

Default v1 focuses on high-confidence, low-ambiguity matches:
- email addresses
- phone numbers (conservative)
- IPv4 addresses
- URL query secrets (`token`, `key`, `secret`, `password`, `auth`)
- common API-key patterns
- conservative strong-format card / id-like strings

Not enabled by default in v1:
- generic high-entropy token detection
- names / organizations / semantic entities

## CLI usage

Preferred:

```bash
cat secret.txt | python3 scripts/redact.py --stdin --json
python3 scripts/redact.py --input ./note.md --output ./note.redacted.md
python3 scripts/redact.py --input ./data.csv --json
```

Avoid passing sensitive plaintext directly as a shell argument when possible.

## Output rules

- `--json` and `--stdout` are mutually exclusive
- Without `--output`, redacted text goes to stdout by default
- With `--output` and no `--json`, redacted text is written to file
- With `--output` and `--stdout`, redacted text is both written to file **and mirrored to stdout**
- With `--output` and `--json`, write JSON to file

Default JSON output must not contain raw matches.

## Repository layout

- `scripts/redact.py` — CLI entrypoint
- `core/policy.py` — security constants and policy
- `core/io_guard.py` — path, encoding, and output guards
- `core/patterns.py` — regex patterns
- `core/detector.py` — matching and replacement planning
- `core/renderer.py` — output rendering
- `tests/` — unit and guardrail tests
- `docs/` — GitHub Pages material

## References

- `README.md` — project overview
- `SECURITY.md` — security model and disclosure notes
- `docs/index.html` — primary GitHub Pages landing page
- `docs/index.md` — lightweight markdown mirror / pointer

#huanyuan
