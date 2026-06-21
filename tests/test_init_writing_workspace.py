from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from scripts.init_writing_workspace import (
    build_llm_review_brief,
    init_writing_workspace,
)


class InitWritingWorkspaceTests(unittest.TestCase):
    def test_build_llm_review_brief_keeps_private_sample_boundary(self) -> None:
        brief = build_llm_review_brief(
            samples=Path("samples"),
            profile=Path("codex/skills/write-as-me-ko/references/voice-profile.md"),
            agents_file=Path("dist/writing/AGENTS.md"),
        )

        self.assertIn("Python baseline profile", brief)
        self.assertIn("Do not copy private raw sample text", brief)
        self.assertIn("Re-export the writing AGENTS file", brief)

    def test_init_writing_workspace_writes_profile_agents_and_review_brief(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            samples = root / "samples"
            (samples / "blog").mkdir(parents=True)
            (samples / "blog" / "post.md").write_text(
                "나는 먼저 문제를 보고, 실제로 해본 뒤 판단을 바꾼다.",
                encoding="utf-8",
            )
            (samples / "blog" / "second.md").write_text(
                "처음에는 쉽게 생각했지만 막상 해보니 기준을 다시 세워야 했다. 그래서 결과보다 과정과 한계를 먼저 적었다.",
                encoding="utf-8",
            )
            refs = root / "codex" / "skills" / "write-as-me-ko" / "references"
            refs.mkdir(parents=True)
            (refs / "judgment-rules.md").write_text("# Judgment Rules", encoding="utf-8")
            (refs / "format-routes.md").write_text("# Format Routes", encoding="utf-8")
            (refs / "anti-ai-tells-ko.md").write_text("# Korean AI-Tell Checklist", encoding="utf-8")

            profile = refs / "voice-profile.md"
            agents = root / "dist" / "writing" / "AGENTS.md"
            brief = root / "_workspace" / "writing-init" / "llm-review.md"

            written = init_writing_workspace(samples, profile, agents, brief, repo_root=root)

            self.assertEqual(written, [profile, agents, brief])
            self.assertIn("Confidence: medium", profile.read_text(encoding="utf-8"))
            self.assertIn("# Writing AGENTS.md", agents.read_text(encoding="utf-8"))
            self.assertIn("Agent Tasks", brief.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
