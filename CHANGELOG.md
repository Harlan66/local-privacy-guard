# Changelog

All notable changes to `local-privacy-guard` will be documented in this file.

## 0.1.3 - 2026-03-11

- fixed empty-file overwrite behavior to match documented guard semantics
- gave `--stdout` a concrete role: mirror redacted text to stdout when `--output` is used
- aligned documentation references around `docs/index.html` as the primary landing page
- added regression tests for overwrite guards and stdout mirroring

## 0.1.2 - 2026-03-11

- rewrote project positioning to focus explicitly on OpenClaw users
- replaced mixed bilingual copy with language-separated README sections
- added click-to-switch bilingual GitHub Pages landing page (`docs/index.html`)

## 0.1.1 - 2026-03-11

- added generated project logo via Nano Banana Pro
- added bilingual README (English + 中文)
- updated GitHub Pages landing page to bilingual layout
- added logo assets for repository and docs site

## 0.1.0 - 2026-03-11

Initial build:
- created `local-privacy-guard` skill and repository structure
- added pure-local Python CLI with zero third-party runtime dependencies
- added path guards, UTF-8-only policy, symlink rejection, and overwrite controls
- added default-safe JSON output without raw sensitive matches
- added repo docs: README, SECURITY, GitHub Pages landing page
- added unit tests for security guardrails and core functionality

#huanyuan
