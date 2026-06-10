from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.build_voice_profile import build_profile_markdown, collect_samples


class BuildVoiceProfileTests(unittest.TestCase):
    def test_collect_samples_reads_supported_markdown_and_text_files(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "blog").mkdir()
            (root / "report").mkdir()
            (root / "blog" / "post.md").write_text("나는 먼저 문제를 본다.", encoding="utf-8")
            (root / "report" / "paper.txt").write_text("이 보고서는 결과를 정리한다.", encoding="utf-8")
            (root / "report" / "skip.pdf").write_text("ignored", encoding="utf-8")

            samples = collect_samples(root)

        self.assertEqual([s.route for s in samples], ["blog", "report"])
        self.assertEqual(samples[0].path.name, "post.md")
        self.assertIn("문제를 본다", samples[0].text)

    def test_collect_samples_ignores_repository_guidance_files(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "README.md").write_text("샘플을 여기에 넣으세요.", encoding="utf-8")
            (root / "blog").mkdir()
            (root / "blog" / "post.md").write_text("나는 실제 글만 분석한다.", encoding="utf-8")

            samples = collect_samples(root)

        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].path.name, "post.md")

    def test_build_profile_markdown_summarizes_korean_voice_signals(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "blog").mkdir()
            (root / "message").mkdir()
            (root / "blog" / "post.md").write_text(
                "나는 먼저 실제 문제를 본다. 그래서 과장된 표현은 별로 좋아하지 않는다.",
                encoding="utf-8",
            )
            (root / "message" / "note.md").write_text(
                "교수님, 확인해주시면 감사하겠습니다. 필요한 내용은 다시 정리하겠습니다.",
                encoding="utf-8",
            )

            markdown = build_profile_markdown(root)

        self.assertIn("Confidence: medium", markdown)
        self.assertIn("Source samples reviewed: 2", markdown)
        self.assertIn("blog: 1", markdown)
        self.assertIn("message: 1", markdown)
        self.assertIn("평균 문장 길이", markdown)
        self.assertIn("자주 보이는 표현", markdown)
        self.assertIn("과장", markdown)

    def test_build_profile_markdown_includes_route_specific_guidance(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "blog").mkdir()
            (root / "report").mkdir()
            (root / "message").mkdir()
            (root / "blog" / "post.md").write_text(
                "나는 처음에는 쉽게 봤다. 그런데 실제로 해보니 생각이 바뀌었다.",
                encoding="utf-8",
            )
            (root / "report" / "paper.md").write_text(
                "이 보고서는 구현 결과와 한계를 나누어 설명한다. 근거를 먼저 확인했다.",
                encoding="utf-8",
            )
            (root / "message" / "note.md").write_text(
                "교수님, 확인 부탁드립니다. 필요한 내용은 오늘 다시 정리하겠습니다.",
                encoding="utf-8",
            )

            markdown = build_profile_markdown(root)

        self.assertIn("## Route-Specific Signals", markdown)
        self.assertIn("### blog", markdown)
        self.assertIn("1인칭 판단 흐름", markdown)
        self.assertIn("### report", markdown)
        self.assertIn("근거와 한계를 분리", markdown)
        self.assertIn("### message", markdown)
        self.assertIn("요청과 다음 행동", markdown)

    def test_build_profile_markdown_warns_when_private_samples_are_present(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "private").mkdir()
            (root / "private" / "journal.md").write_text(
                "나는 이 글을 로컬에서만 분석하고 싶다.",
                encoding="utf-8",
            )

            markdown = build_profile_markdown(root)

        self.assertIn("## Privacy Notes", markdown)
        self.assertIn("private", markdown)
        self.assertIn("git에 올리지 마세요", markdown)


if __name__ == "__main__":
    unittest.main()
