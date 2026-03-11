# Security Policy

## Scope

`local-privacy-guard` is a local-only privacy redaction tool. Its security model prioritizes narrow scope, auditable code, and safe defaults over maximum recall.

## Supported guarantees for v1

- no network I/O in mainline execution
- no third-party runtime dependency requirement
- default JSON output contains no raw matches
- no surrounding-context preview in default output
- no persistence by default
- no writes without explicit `--output`
- protected path checks before file writes
- no deanonymize support

## Non-goals

- perfect recall of all sensitive information
- semantic entity understanding
- PDF / DOCX / OCR support
- cloud fallback
- restore / deanonymize workflows

## Reporting issues

Until a dedicated process exists, open a private report to the repository owner before publishing details publicly.

## Threat notes

This project reduces exposure risk. It does not make a compromised host safe, and it does not guarantee that all business-sensitive context has been removed.

#huanyuan
