from __future__ import annotations

import secrets
from dataclasses import dataclass
from typing import Dict, Iterable, List

from .patterns import PATTERNS, URL_SECRET_PARAM_RE
from .policy import PLACEHOLDER_PREFIXES


@dataclass(frozen=True)
class Detection:
    type: str
    start: int
    end: int
    placeholder: str
    fingerprint: str
    confidence: str = "high"
    raw_match: str = ""


def _fingerprint_for(raw_value: str, cache: Dict[str, str]) -> str:
    if raw_value not in cache:
        cache[raw_value] = secrets.token_hex(6)
    return cache[raw_value]


def _placeholder(kind: str, fingerprint: str) -> str:
    prefix = PLACEHOLDER_PREFIXES.get(kind, kind.upper())
    return f"[[{prefix}:{fingerprint}]]"


def _collect_matches(text: str, enabled_types: set[str] | None = None) -> List[tuple[str, int, int, str]]:
    matches: List[tuple[str, int, int, str]] = []
    allowed = enabled_types or {kind for kind, _ in PATTERNS} | {"url_secret"}

    for kind, pattern in PATTERNS:
        if kind not in allowed:
            continue
        for match in pattern.finditer(text):
            value = match.group(0)
            matches.append((kind, match.start(), match.end(), value))

    if "url_secret" in allowed:
        for match in URL_SECRET_PARAM_RE.finditer(text):
            value = match.group(2)
            matches.append(("url_secret", match.start(2), match.end(2), value))

    matches.sort(key=lambda item: (item[1], -(item[2] - item[1]), item[0]))
    return matches


def _resolve_overlaps(matches: Iterable[tuple[str, int, int, str]]) -> List[tuple[str, int, int, str]]:
    selected: List[tuple[str, int, int, str]] = []
    occupied: List[tuple[int, int]] = []

    for item in matches:
        _, start, end, _ = item
        if any(not (end <= s or start >= e) for s, e in occupied):
            continue
        selected.append(item)
        occupied.append((start, end))

    return selected


def detect(text: str, enabled_types: set[str] | None = None, debug: bool = False) -> List[Detection]:
    cache: Dict[str, str] = {}
    detections: List[Detection] = []

    for kind, start, end, raw_value in _resolve_overlaps(_collect_matches(text, enabled_types=enabled_types)):
        fingerprint = _fingerprint_for(raw_value, cache)
        detections.append(
            Detection(
                type=kind,
                start=start,
                end=end,
                placeholder=_placeholder(kind, fingerprint),
                fingerprint=fingerprint,
                raw_match=raw_value if debug else "",
            )
        )

    return detections
