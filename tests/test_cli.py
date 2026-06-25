from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


class CliTests(unittest.TestCase):
    def test_profile_pack_cli_build_doctor_eval_and_export_agents_context(self) -> None:
        try:
            from write_as_me.cli import main
        except ModuleNotFoundError as exc:
            self.fail(f"CLI package is missing: {exc}")

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            samples = root / "samples"
            pack = root / "dist" / "profile-pack"
            export = root / "dist" / "writing" / "AGENTS.md"
            (samples / "blog").mkdir(parents=True)
            (samples / "message").mkdir()
            (samples / "blog" / "post.md").write_text(
                "나는 실제 문제를 먼저 보고, 구현한 뒤 검증 결과를 짧게 정리한다. "
                "과장된 표현보다 지금 확인한 사실과 다음 행동을 분리해서 쓰는 편이다.",
                encoding="utf-8",
            )
            (samples / "message" / "note.md").write_text(
                "교수님, 확인 부탁드립니다. 필요한 내용은 다시 정리하겠습니다. "
                "일정과 요청 사항을 짧게 적고 감사 표현을 마지막에 붙입니다.",
                encoding="utf-8",
            )

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                build_exit = main(["profile", "build", "--samples", str(samples), "--output", str(pack), "--json"])
            build_payload = json.loads(stdout.getvalue())

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                doctor_exit = main(["doctor", "--profile-pack", str(pack), "--json"])
            doctor_payload = json.loads(stdout.getvalue())

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                eval_exit = main(["eval", "--profile-pack", str(pack), "--json"])
            eval_payload = json.loads(stdout.getvalue())

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                export_exit = main(["export", "agents", "--profile-pack", str(pack), "--output", str(export)])
            exported = export.read_text(encoding="utf-8")

            self.assertEqual(build_exit, 0)
            self.assertEqual(build_payload["status"], "built")
            self.assertTrue((pack / "profile.json").exists())
            self.assertEqual(doctor_exit, 0)
            self.assertEqual(doctor_payload["status"], "pass")
            self.assertEqual(eval_exit, 0)
            self.assertEqual(eval_payload["status"], "pass")
            self.assertEqual(export_exit, 0)
            self.assertIn("# Writing AGENTS.md", exported)
            self.assertIn("Raw samples included: no", exported)
            self.assertIn("Confidence: medium", exported)
            self.assertNotIn("실제 문제를 먼저 보고", exported)

    def test_style_distance_and_rewrite_brief_cli(self) -> None:
        from write_as_me.cli import main
        from write_as_me.profile_pack import build_profile_pack

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            samples = root / "samples"
            pack = root / "profile-pack"
            draft = root / "draft.md"
            human = root / "human.md"
            generic = root / "generic.md"
            guided = root / "guided.md"
            report = root / "style-distance.md"
            brief = root / "rewrite-brief.md"
            (samples / "blog").mkdir(parents=True)
            human_text = "나는 먼저 직접 해봤다. 그런데 생각보다 달랐다. 그래서 아직 모르는 부분을 따로 적었다."
            generic_text = "결론적으로 이 경험은 매우 중요한 성장 과정입니다. 이를 통해 더 나은 결과를 만들었습니다."
            guided_text = "나는 처음엔 쉽게 봤다. 그런데 직접 해보니 판단이 바뀌었다. 그래서 다음 확인할 걸 남겼다."
            (samples / "blog" / "post.md").write_text(human_text, encoding="utf-8")
            draft.write_text(generic_text, encoding="utf-8")
            human.write_text(human_text, encoding="utf-8")
            generic.write_text(generic_text, encoding="utf-8")
            guided.write_text(guided_text, encoding="utf-8")
            build_profile_pack(samples, pack)

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                distance_exit = main(
                    [
                        "style-distance",
                        "--profile-pack",
                        str(pack),
                        "--route",
                        "blog",
                        "--human",
                        str(human),
                        "--generic",
                        str(generic),
                        "--profile-guided",
                        str(guided),
                        "--output",
                        str(report),
                        "--json",
                    ]
                )
            distance_payload = json.loads(stdout.getvalue())

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                brief_exit = main(
                    [
                        "rewrite",
                        "brief",
                        "--profile-pack",
                        str(pack),
                        "--input",
                        str(draft),
                        "--route",
                        "blog",
                        "--mode",
                        "balanced",
                        "--output",
                        str(brief),
                        "--json",
                    ]
                )
            brief_payload = json.loads(stdout.getvalue())
            report_text = report.read_text(encoding="utf-8")
            brief_text = brief.read_text(encoding="utf-8")

        self.assertEqual(distance_exit, 0)
        self.assertEqual(distance_payload["status"], "ok")
        self.assertTrue(distance_payload["profile_guided_closer_than_generic"])
        self.assertIn("# Style-Distance Report", report_text)
        self.assertEqual(brief_exit, 0)
        self.assertEqual(brief_payload["status"], "written")
        self.assertIn("Rewrite Instructions", brief_text)
        self.assertNotIn("먼저 직접 해봤다", brief_text)


if __name__ == "__main__":
    unittest.main()
