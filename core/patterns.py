from __future__ import annotations

import re

# Keep patterns simple to reduce catastrophic-backtracking risk.
PATTERNS = [
    ("email", re.compile(r"\b[A-Za-z0-9._%+-]{1,64}@[A-Za-z0-9.-]{1,253}\.[A-Za-z]{2,24}\b")),
    ("phone", re.compile(r"(?<!\w)(?:\+?\d[\d\s().-]{6,18}\d)(?!\w)")),
    ("ipv4", re.compile(r"\b(?:25[0-5]|2[0-4]\d|1?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}\b")),
    ("api_key", re.compile(r"\b(?:sk-[A-Za-z0-9]{16,}|gh[opusr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{10,})\b")),
    ("bank_or_id", re.compile(r"\b(?:\d[ -]?){13,19}\b")),
]

URL_SECRET_PARAM_RE = re.compile(
    r"([?&](?:token|key|secret|password|auth)=)([^&#\s]+)",
    re.IGNORECASE,
)
