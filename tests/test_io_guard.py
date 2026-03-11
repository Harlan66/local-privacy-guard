from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from core.io_guard import GuardError, write_output


class IoGuardTests(unittest.TestCase):
    def test_allows_overwrite_of_existing_empty_file_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dst = Path(tmp) / "out.txt"
            dst.write_text("", encoding="utf-8")
            write_output(dst, "hello\n", force=False)
            self.assertEqual(dst.read_text(encoding="utf-8"), "hello\n")

    def test_rejects_overwrite_of_existing_non_empty_file_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dst = Path(tmp) / "out.txt"
            dst.write_text("existing\n", encoding="utf-8")
            with self.assertRaises(GuardError):
                write_output(dst, "hello\n", force=False)


if __name__ == "__main__":
    unittest.main()
