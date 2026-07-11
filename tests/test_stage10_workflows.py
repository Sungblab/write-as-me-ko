from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path


class Stage10WorkflowTests(unittest.TestCase):
    def test_heldout_prepare_and_compare_excludes_heldout_from_profile(self) -> None:
        from write_as_me.heldout import compare_heldout_workspace, prepare_heldout_workspace

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            samples = root / "samples"
            workspace = root / "heldout"
            generic = root / "generic.md"
            guided = root / "guided.md"
            report = root / "heldout-report.md"
            (samples / "blog").mkdir(parents=True)
            (samples / "blog" / "a.md").write_text(
                "나는 먼저 직접 해봤다. 그런데 결과가 애매했다. 그래서 확인한 사실과 추정을 나눠 적었다.",
                encoding="utf-8",
            )
            (samples / "blog" / "b.md").write_text(
                "나는 처음엔 쉽게 봤다. 그런데 직접 돌려보니 달랐다. 그래서 다음에 확인할 걸 남겼다.",
                encoding="utf-8",
            )
            generic.write_text(
                "결론적으로 이 경험은 매우 중요한 성장 과정입니다. 이를 통해 더 나은 결과를 만들었습니다.",
                encoding="utf-8",
            )
            guided.write_text(
                "나는 처음엔 쉽게 봤다. 그런데 직접 해보니 판단이 바뀌었다. 그래서 다음 확인할 걸 남겼다.",
                encoding="utf-8",
            )

            prepared = prepare_heldout_workspace(samples, workspace, route="blog", holdout_count=1)
            manifest = json.loads((workspace / "heldout-manifest.json").read_text(encoding="utf-8"))
            profile_manifest = json.loads((workspace / "profile-pack" / "sample-manifest.json").read_text(encoding="utf-8"))
            compared = compare_heldout_workspace(workspace, generic, guided, output_path=report)
            report_text = report.read_text(encoding="utf-8")

        self.assertEqual(prepared["status"], "prepared")
        self.assertEqual(manifest["training_count"], 1)
        self.assertEqual(manifest["heldout_count"], 1)
        self.assertFalse(manifest["raw_samples_included"])
        self.assertEqual(profile_manifest["samples"][0]["path"], "blog/a.md")
        self.assertEqual(compared["status"], "ok")
        self.assertIn("Held-Out Style Evaluation", report_text)
        self.assertIn("AI-detector bypass", report_text)
        self.assertNotIn("직접 돌려보니", json.dumps(manifest, ensure_ascii=False))

    def test_rewrite_loop_and_check_report_improvement(self) -> None:
        from write_as_me.profile_pack import build_profile_pack
        from write_as_me.rewrite_loop import check_rewrite, prepare_rewrite_loop

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            samples = root / "samples"
            pack = root / "pack"
            draft = root / "draft.md"
            rewritten = root / "rewritten.md"
            loop_dir = root / "rewrite-loop"
            check_report = root / "rewrite-check.md"
            (samples / "blog").mkdir(parents=True)
            (samples / "blog" / "post.md").write_text(
                "나는 먼저 직접 해봤다. 그런데 생각보다 달랐다. 그래서 아직 모르는 부분을 따로 적었다.",
                encoding="utf-8",
            )
            build_profile_pack(samples, pack)
            draft.write_text(
                "결론적으로 이 경험은 매우 중요한 성장 과정입니다. 이를 통해 더 나은 결과를 만들었습니다.",
                encoding="utf-8",
            )
            rewritten.write_text(
                "나는 처음엔 쉽게 봤다. 그런데 직접 해보니 판단이 바뀌었다. 그래서 다음 확인할 걸 남겼다.",
                encoding="utf-8",
            )

            prepared = prepare_rewrite_loop(pack, draft, loop_dir, route="blog", mode="balanced")
            checked = check_rewrite(pack, draft, rewritten, check_report, route="blog")
            manifest = json.loads((loop_dir / "rewrite-loop.json").read_text(encoding="utf-8"))
            check_text = check_report.read_text(encoding="utf-8")
            brief_exists = (loop_dir / "rewrite-brief.md").exists()
            before_report_exists = (loop_dir / "style-distance-before.md").exists()

        self.assertEqual(prepared["status"], "prepared")
        self.assertFalse(manifest["raw_profile_samples_included"])
        self.assertTrue(brief_exists)
        self.assertTrue(before_report_exists)
        self.assertTrue(checked["distance_improved"])
        self.assertTrue(checked["risk_count_not_increased"])
        self.assertIn("Rewrite Check Report", check_text)


if __name__ == "__main__":
    unittest.main()
