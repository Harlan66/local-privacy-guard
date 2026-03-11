from __future__ import annotations

import ast
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCAN_DIRS = [ROOT / "core", ROOT / "scripts"]
FORBIDDEN_IMPORTS = {
    "requests",
    "httpx",
    "socket",
    "websocket",
    "pty",
    "pickle",
    "marshal",
    "shelve",
    "ctypes",
}
FORBIDDEN_FROM_IMPORTS = {"urllib.request"}
FORBIDDEN_CALLS = {
    "subprocess.run",
    "subprocess.Popen",
    "subprocess.call",
    "os.system",
    "os.popen",
    "eval",
    "exec",
    "__import__",
    "importlib.import_module",
}


def dotted_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = dotted_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return None


class NoNetworkImportTests(unittest.TestCase):
    def test_no_forbidden_imports_or_calls(self) -> None:
        for scan_dir in SCAN_DIRS:
            for path in scan_dir.rglob("*.py"):
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            self.assertNotIn(alias.name, FORBIDDEN_IMPORTS, f"forbidden import in {path}: {alias.name}")
                    elif isinstance(node, ast.ImportFrom):
                        module = node.module or ""
                        self.assertNotIn(module, FORBIDDEN_FROM_IMPORTS, f"forbidden import-from in {path}: {module}")
                    elif isinstance(node, ast.Call):
                        name = dotted_name(node.func)
                        if name in FORBIDDEN_CALLS:
                            self.fail(f"forbidden call in {path}: {name}")


if __name__ == "__main__":
    unittest.main()
