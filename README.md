# local-privacy-guard

Pure-local privacy redaction for text and simple text files.

`local-privacy-guard` is a minimal, auditable privacy-redaction skill and Python CLI designed for one job: **replace high-confidence sensitive values locally, with zero network access and safe defaults**.

## Why this exists

Most privacy tools optimize for coverage and convenience. This project optimizes for:

- **local-only execution**
- **default-irreversible redaction**
- **no raw sensitive values in default reports**
- **no persistent side effects by default**
- **no third-party runtime dependencies in v1**
- **small enough to audit by hand**

## Security posture

This project follows a strict “small, local, auditable” model.

### Security invariants

1. Mainline execution must not perform network I/O
2. Default mode must not emit raw sensitive values
3. Default mode must not emit surrounding-context previews
4. Default mode must not create persistent side effects
5. No file writes without explicit `--output`
6. All output paths must be `resolve()`-checked before use
7. `--force` only removes the non-empty overwrite guard; it never bypasses path or symlink protections
8. No deanonymize support in v1
9. No third-party runtime dependencies in v1
10. UTF-8 only input policy (UTF-8 BOM accepted)

## Supported inputs

- `stdin` (preferred)
- UTF-8 / UTF-8 BOM files:
  - `.txt`
  - `.md`
  - `.json`
  - `.csv`
  - `.tsv`

Unsupported in v1:
- PDF / DOCX / image / audio / video
- restore / deanonymize flows
- generic entropy scanning by default

## What it detects in v1

High-confidence defaults:
- email addresses
- conservative phone numbers
- IPv4 addresses
- secret-bearing URL query parameters
- common API key formats
- conservative strong-format card-like / ID-like strings

Not enabled by default:
- generic high-entropy token detection
- semantic names / entities

## Quick start

### Read from stdin

```bash
cat secret.txt | python3 scripts/redact.py --stdin --json
```

### Read from file and print redacted text

```bash
python3 scripts/redact.py --input ./note.md
```

### Write redacted text to file

```bash
python3 scripts/redact.py --input ./note.md --output ./note.redacted.md
```

### Write JSON to file

```bash
python3 scripts/redact.py --input ./note.md --json --output ./note.redacted.json
```

## Output example

```json
{
  "success": true,
  "tool": "local-privacy-guard",
  "mode": "local-only",
  "reversible": false,
  "input_type": "text",
  "detections": [
    {
      "type": "email",
      "placeholder": "[[EMAIL:7f3a91c24e6b]]",
      "fingerprint": "7f3a91c24e6b",
      "start": 5,
      "end": 22,
      "confidence": "high"
    }
  ],
  "redacted_text": "联系我：[[EMAIL:7f3a91c24e6b]]",
  "warnings": []
}
```

## CLI rules

- `--json` and `--stdout` are mutually exclusive
- no `--output` → write to stdout only
- `--output` without `--json` → write redacted text to file
- `--output` with `--json` → write JSON to file
- `--force` only allows overwrite of an existing ordinary file after all path checks pass

## Testing

```bash
python3 -m unittest discover -s tests -v
```

## Repository structure

```text
local-privacy-guard/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── SECURITY.md
├── LICENSE.txt
├── .gitignore
├── docs/
│   └── index.md
├── core/
│   ├── __init__.py
│   ├── policy.py
│   ├── io_guard.py
│   ├── patterns.py
│   ├── detector.py
│   └── renderer.py
├── scripts/
│   └── redact.py
└── tests/
    └── ...
```

## GitHub Pages

A simple project landing page lives in `docs/index.md`.

If publishing on GitHub Pages, serve from the `docs/` folder on the default branch.

## License

MIT.

#huanyuan
