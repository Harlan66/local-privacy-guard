from __future__ import annotations

from typing import Iterable, List

from .detector import Detection
from .policy import MODE, TOOL_NAME


def redact_text(text: str, detections: Iterable[Detection]) -> str:
    ordered = sorted(detections, key=lambda item: item.start, reverse=True)
    redacted = text
    for item in ordered:
        redacted = redacted[: item.start] + item.placeholder + redacted[item.end :]
    return redacted


def render_json(text: str, detections: List[Detection], input_type: str, debug: bool = False) -> dict:
    payload = {
        "success": True,
        "tool": TOOL_NAME,
        "mode": MODE,
        "reversible": False,
        "input_type": input_type,
        "detections": [
            {
                "type": item.type,
                "placeholder": item.placeholder,
                "fingerprint": item.fingerprint,
                "start": item.start,
                "end": item.end,
                "confidence": item.confidence,
                **({"match": item.raw_match} if debug and item.raw_match else {}),
            }
            for item in detections
        ],
        "redacted_text": redact_text(text, detections),
        "warnings": [],
    }
    return payload
