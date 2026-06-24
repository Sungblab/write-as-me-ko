from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


class DemoReportTests(unittest.TestCase):
    def test_demo_report_cli_writes_judge_readable_report(self) -> None:
        from write_as_me.cli import main
        from write_as_me.profile_pack import build_profile_pack

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            samples = root / "samples"
            pack = root / "profile-pack"
            report = root / "demo-report.md"
            (samples / "blog").mkdir(parents=True)
            (samples / "project").mkdir()
            (samples / "blog" / "post.md").write_text(
                "나는 실제 문제를 먼저 보고, 확인한 사실과 모르는 부분을 나눠 쓴다. "
                "그래서 과장된 결론보다 다음 행동을 남긴다.",
                encoding="utf-8",
            )
            (samples / "project" / "summary.md").write_text(
                "구현 결과와 검증 명령을 먼저 정리한다. 남은 한계는 별도로 적는다.",
                encoding="utf-8",
            )
            build_profile_pack(samples, pack)

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["demo", "report", "--profile-pack", str(pack), "--output", str(report), "--json"])
            payload = json.loads(stdout.getvalue())
            markdown = report.read_text(encoding="utf-8")

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["status"], "written")
        self.assertIn("# Write As Me KO Demo Report", markdown)
        self.assertIn("What changes with the profile pack", markdown)
        self.assertIn("Generic agent", markdown)
        self.assertIn("Profile-aware agent", markdown)
        self.assertIn("Style Signals", markdown)
        self.assertIn("Privacy", markdown)
        self.assertNotIn("실제 문제를 먼저 보고", markdown)


if __name__ == "__main__":
    unittest.main()
