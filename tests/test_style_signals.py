from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path


class StyleSignalsTests(unittest.TestCase):
    def test_analyze_style_signals_extracts_korean_writing_markers(self) -> None:
        try:
            from write_as_me.style_signals import analyze_style_signals
        except ModuleNotFoundError as exc:
            self.fail(f"style signal analyzer is missing: {exc}")

        text = "\n".join(
            [
                "나는 먼저 실제 문제를 본다. 그런데 구현해보니 판단이 바뀌었다.",
                "그래서 확인한 사실과 아직 모르는 부분을 분리한다.",
                "- 검증 명령을 남긴다.",
                "- 다음 행동을 짧게 적는다.",
            ]
        )

        signals = analyze_style_signals(text)

        self.assertEqual(signals["sentence_count"], 5)
        self.assertGreater(signals["avg_sentence_chars"], 10)
        self.assertIn("다", signals["ending_counts"])
        self.assertGreaterEqual(signals["connector_counts"]["그런데"], 1)
        self.assertGreaterEqual(signals["connector_counts"]["그래서"], 1)
        self.assertGreaterEqual(signals["first_person_count"], 1)
        self.assertEqual(signals["bullet_line_count"], 2)
        self.assertIn("sentence-length", signals["signal_groups"])
        self.assertIn("connectors", signals["signal_groups"])

    def test_profile_pack_embeds_style_features_without_raw_text(self) -> None:
        from write_as_me.profile_pack import build_profile_pack

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            samples = root / "samples"
            output = root / "profile-pack"
            (samples / "blog").mkdir(parents=True)
            (samples / "blog" / "post.md").write_text(
                "나는 처음에는 쉽게 봤다. 그런데 실제로 구현해보니 판단이 바뀌었다. "
                "그래서 확인한 사실과 아직 모르는 부분을 분리한다.",
                encoding="utf-8",
            )

            build_profile_pack(samples, output)

            profile = json.loads((output / "profile.json").read_text(encoding="utf-8"))
            coverage = (output / "coverage-report.md").read_text(encoding="utf-8")

        self.assertIn("style_features", profile)
        self.assertIn("ending_counts", profile["style_features"])
        self.assertIn("connector_counts", profile["style_features"])
        self.assertIn("first_person_count", profile["style_features"])
        self.assertIn("Style Signals", coverage)
        self.assertNotIn("처음에는 쉽게 봤다", json.dumps(profile, ensure_ascii=False))


if __name__ == "__main__":
    unittest.main()
