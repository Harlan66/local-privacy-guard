from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "redact.py"


class CliContractTests(unittest.TestCase):
    def test_json_default_contains_no_raw_match(self) -> None:
        proc = subprocess.run(
            ["python3", str(SCRIPT), "--stdin", "--json"],
            input="email alice@example.com\n",
            text=True,
            capture_output=True,
            check=True,
            cwd=str(ROOT),
        )
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["success"], True)
        self.assertNotIn("match", payload["detections"][0])

    def test_output_writes_text_when_not_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "input.md"
            dst = Path(tmp) / "output.md"
            src.write_text("email alice@example.com", encoding="utf-8")
            subprocess.run(
                ["python3", str(SCRIPT), "--input", str(src), "--output", str(dst)],
                text=True,
                capture_output=True,
                check=True,
                cwd=str(ROOT),
            )
            content = dst.read_text(encoding="utf-8")
            self.assertIn("[[EMAIL:", content)
            self.assertNotIn("alice@example.com", content)

    def test_stdout_can_mirror_text_when_output_is_used(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "input.md"
            dst = Path(tmp) / "output.md"
            src.write_text("email alice@example.com", encoding="utf-8")
            proc = subprocess.run(
                ["python3", str(SCRIPT), "--input", str(src), "--output", str(dst), "--stdout"],
                text=True,
                capture_output=True,
                check=True,
                cwd=str(ROOT),
            )
            self.assertIn("[[EMAIL:", proc.stdout)
            self.assertTrue(dst.exists())


if __name__ == "__main__":
    unittest.main()
