from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.export_agent_context import build_agent_context


class ExportAgentContextTests(unittest.TestCase):
    def test_build_agent_context_combines_core_references(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            refs = root / "codex" / "skills" / "write-as-me-ko" / "references"
            refs.mkdir(parents=True)
            (refs / "voice-profile.md").write_text("# Voice Profile\n\n- Confidence: medium\n", encoding="utf-8")
            (refs / "judgment-rules.md").write_text("# Judgment Rules\n\n- 근거를 우선한다.\n", encoding="utf-8")
            (refs / "format-routes.md").write_text("# Format Routes\n\n## Blog\n", encoding="utf-8")
            (refs / "anti-ai-tells-ko.md").write_text("# Korean AI-Tell Checklist\n\n- 결론적으로\n", encoding="utf-8")

            context = build_agent_context(root)

        self.assertIn("# AGENTS.write-as-me-ko", context)
        self.assertIn("Do not invent personal experiences", context)
        self.assertIn("Confidence: medium", context)
        self.assertIn("근거를 우선한다", context)
        self.assertIn("## Blog", context)
        self.assertIn("결론적으로", context)


if __name__ == "__main__":
    unittest.main()

