from __future__ import annotations

import io
import json
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Tuple

from .policy import DEFAULT_MAX_SIZE, FORBIDDEN_OUTPUT_PREFIXES, SUPPORTED_EXTENSIONS


class GuardError(RuntimeError):
    pass


def _resolved(path: Path) -> Path:
    return path.expanduser().resolve(strict=False)


def _ensure_not_symlink(path: Path) -> None:
    if path.is_symlink():
        raise GuardError(f"symlink paths are not allowed: {path}")


def read_text_input(*, input_path: Optional[str], use_stdin: bool, max_size: int = DEFAULT_MAX_SIZE) -> Tuple[str, str]:
    if use_stdin and input_path:
        raise GuardError("use either --stdin or --input, not both")
    if not use_stdin and not input_path:
        raise GuardError("one of --stdin or --input is required")

    if use_stdin:
        raw = os.read(0, max_size + 1)
        if len(raw) > max_size:
            raise GuardError("stdin input exceeds max size")
        try:
            return raw.decode("utf-8-sig"), "text"
        except UnicodeDecodeError as exc:
            raise GuardError("stdin must be UTF-8 or UTF-8 BOM") from exc

    path = Path(str(input_path)).expanduser()
    _ensure_not_symlink(path)
    if not path.exists() or not path.is_file():
        raise GuardError(f"input file does not exist: {path}")
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise GuardError(f"unsupported input type: {path.suffix}")
    if path.stat().st_size > max_size:
        raise GuardError("input file exceeds max size")
    data = path.read_bytes()
    if b"\x00" in data:
        raise GuardError("binary/null-byte inputs are not supported")
    try:
        return data.decode("utf-8-sig"), path.suffix.lower().lstrip(".")
    except UnicodeDecodeError as exc:
        raise GuardError("input files must be UTF-8 or UTF-8 BOM") from exc


def validate_output_path(output_path: str) -> Path:
    path = Path(output_path).expanduser()
    if path.exists():
        _ensure_not_symlink(path)
    resolved = _resolved(path)
    for prefix in FORBIDDEN_OUTPUT_PREFIXES:
        prefix_resolved = _resolved(prefix)
        if resolved == prefix_resolved or prefix_resolved in resolved.parents:
            raise GuardError(f"refusing to write under protected path: {resolved}")
    return resolved


@contextmanager
def tightened_umask(mask: int = 0o177):
    old = os.umask(mask)
    try:
        yield
    finally:
        os.umask(old)


def write_output(path: Path, content: str, *, force: bool = False) -> None:
    if path.exists() and path.is_dir():
        raise GuardError("output path is a directory")
    parent = path.parent
    parent.mkdir(parents=True, exist_ok=True)
    if parent.is_symlink():
        raise GuardError("output parent cannot be a symlink")

    if path.exists() and not force:
        try:
            if path.stat().st_size > 0:
                raise GuardError("refusing to overwrite existing non-empty file without --force")
        except FileNotFoundError:
            pass

    flags = os.O_WRONLY | os.O_CREAT
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    if path.exists() and force:
        flags |= os.O_TRUNC
    else:
        flags |= os.O_EXCL

    with tightened_umask():
        fd = os.open(str(path), flags, 0o600)
        with io.open(fd, mode="w", encoding="utf-8", closefd=True) as handle:
            handle.write(content)


def json_dumps(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
