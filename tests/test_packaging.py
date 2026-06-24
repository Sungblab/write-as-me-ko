from __future__ import annotations

import tomllib
import unittest
from pathlib import Path


class PackagingTests(unittest.TestCase):
    def test_pyproject_exposes_write_as_me_console_script(self) -> None:
        pyproject = Path("pyproject.toml")
        self.assertTrue(pyproject.exists(), "pyproject.toml is required for CLI packaging")

        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))

        self.assertEqual(data["project"]["name"], "write-as-me-ko")
        self.assertEqual(data["project"]["scripts"]["write-as-me"], "write_as_me.cli:main")


if __name__ == "__main__":
    unittest.main()
