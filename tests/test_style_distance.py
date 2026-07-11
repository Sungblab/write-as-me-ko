from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path


class StyleDistanceTests(unittest.TestCase):
    def test_evaluate_draft_reports_distance_and_ai_tell_risks(self) -> None:
        from write_as_me.profile_pack import build_profile_pack
        from write_as_me.style_distance import evaluate_draft

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            samples = root / "samples"
            pack = root / "pack"
            (samples / "blog").mkdir(parents=True)
            (samples / "blog" / "post.md").write_text(
                "나는 처음엔 쉽게 봤다. 그런데 실제로 해보니 판단이 바뀌었다. "
                "그래서 아직 모르는 부분과 확인한 사실을 나눠 적는다.",
                encoding="utf-8",
            )
            build_profile_pack(samples, pack)

            result = evaluate_draft(
                pack,
                "결론적으로 이 경험은 매우 중요한 성장 과정이었다. "
                "이를 통해 저는 더 나은 개발자가 될 수 있었다. "
                "요약하면 모든 과정은 의미 있는 배움이었다.",
                route="blog",
            )

        self.assertIn("style_distance", result)
        self.assertGreaterEqual(result["style_distance"]["distance"], 0)
        self.assertLessEqual(result["style_distance"]["distance"], 1)
        self.assertTrue(any(risk["id"] == "generic-ai-transitions" for risk in result["ai_tell_risks"]))

    def test_compare_variants_marks_profile_guided_when_closer_than_generic(self) -> None:
        from write_as_me.profile_pack import build_profile_pack
        from write_as_me.style_distance import compare_variants

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            samples = root / "samples"
            pack = root / "pack"
            (samples / "blog").mkdir(parents=True)
            human = "나는 먼저 직접 해봤다. 그런데 생각보다 달랐다. 그래서 아직 모르는 부분을 따로 적었다."
            generic = "결론적으로 이 프로젝트는 큰 의미가 있습니다. 이를 통해 많은 성장을 할 수 있었습니다."
            guided = "나는 처음엔 쉽게 봤다. 그런데 직접 구현해보니 판단이 바뀌었다. 그래서 다음에 확인할 걸 남겼다."
            (samples / "blog" / "post.md").write_text(human, encoding="utf-8")
            build_profile_pack(samples, pack)

            result = compare_variants(pack, human, generic, guided, route="blog")

        self.assertIn("variants", result)
        self.assertTrue(result["profile_guided_closer_than_generic"])
        self.assertGreater(result["distance_delta"], 0)

    def test_rewrite_brief_uses_profile_metadata_without_raw_samples(self) -> None:
        from write_as_me.profile_pack import build_profile_pack
        from write_as_me.style_distance import build_rewrite_brief

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            samples = root / "samples"
            pack = root / "pack"
            draft = root / "draft.md"
            (samples / "blog").mkdir(parents=True)
            (samples / "blog" / "post.md").write_text(
                "이 원문 샘플 문장은 brief에 들어가면 안 된다. 나는 한계를 따로 적는다.",
                encoding="utf-8",
            )
            draft.write_text("결론적으로 이 글은 좋은 경험을 설명합니다.", encoding="utf-8")
            build_profile_pack(samples, pack)

            brief = build_rewrite_brief(pack, draft, route="blog", mode="minimal")

        self.assertIn("# Rewrite Brief", brief)
        self.assertIn("Rewrite mode: minimal", brief)
        self.assertIn("AI-Tell Risks", brief)
        self.assertNotIn("원문 샘플 문장", brief)


if __name__ == "__main__":
    unittest.main()
