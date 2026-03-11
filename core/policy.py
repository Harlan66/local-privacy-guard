from __future__ import annotations

from pathlib import Path

TOOL_NAME = "local-privacy-guard"
MODE = "local-only"
DEFAULT_MAX_SIZE = 1024 * 1024  # 1 MiB
SUPPORTED_EXTENSIONS = {".txt", ".md", ".json", ".csv", ".tsv"}
UTF8_BOMS = ("utf-8", "utf-8-sig")

FORBIDDEN_OUTPUT_PREFIXES = [
    Path.home() / ".ssh",
    Path.home() / ".gnupg",
    Path.home() / ".aws",
    Path.home() / ".config" / "gh",
]

PLACEHOLDER_PREFIXES = {
    "email": "EMAIL",
    "phone": "PHONE",
    "ipv4": "IPV4",
    "url_secret": "SECRET",
    "api_key": "APIKEY",
    "bank_or_id": "ID",
}

FORBIDDEN_IMPORT_TOKENS = [
    "requests",
    "httpx",
    "urllib.request",
    "socket",
    "websocket",
    "subprocess",
    "pty",
    "os.system",
    "os.popen",
    "eval(",
    "exec(",
    "pickle",
    "marshal",
    "shelve",
    "ctypes",
]
