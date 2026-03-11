from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from core.io_guard import GuardError, read_text_input, validate_output_path


class SafeFileTypeTests(unittest.TestCase):
    def test_rejects_non_utf8_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.txt"
            path.write_bytes("é".encode("latin-1"))
            with self.assertRaises(GuardError):
                read_text_input(input_path=str(path), use_stdin=False)

    def test_rejects_unsupported_extension(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.pdf"
            path.write_text("fake", encoding="utf-8")
            with self.assertRaises(GuardError):
                read_text_input(input_path=str(path), use_stdin=False)

    def test_rejects_input_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            real = Path(tmp) / "real.txt"
            real.write_text("hello", encoding="utf-8")
            link = Path(tmp) / "link.txt"
            os.symlink(real, link)
            with self.assertRaises(GuardError):
                read_text_input(input_path=str(link), use_stdin=False)

    def test_rejects_protected_output_prefix(self) -> None:
        protected = str(Path.home() / ".ssh" / "authorized_keys")
        with self.assertRaises(GuardError):
            validate_output_path(protected)


if __name__ == "__main__":
    unittest.main()
