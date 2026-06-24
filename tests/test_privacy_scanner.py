from __future__ import annotations

import json
import tempfile
import unittest
import io
from contextlib import redirect_stdout
from pathlib import Path


class PrivacyScannerTests(unittest.TestCase):
    def test_scan_text_finds_private_identifiers_without_storing_values(self) -> None:
        try:
            from write_as_me.privacy_scanner import scan_text
        except ModuleNotFoundError as exc:
            self.fail(f"privacy scanner is missing: {exc}")

        report = scan_text(
            "연락은 sungbin@example.com 또는 010-1234-5678로 주세요. "
            "학번은 202612345이고 API key는 sk-abcdefghijklmnopqrstuvwxyz1234567890 입니다.",
            source_path="message/private.local.md",
        )

        self.assertEqual(report["finding_count"], 4)
        self.assertEqual(report["risk"], "high")
        kinds = {finding["kind"] for finding in report["findings"]}
        self.assertEqual(kinds, {"email", "phone", "student_id", "token_like"})
        self.assertNotIn("sungbin@example.com", json.dumps(report, ensure_ascii=False))
        self.assertNotIn("010-1234-5678", json.dumps(report, ensure_ascii=False))
        self.assertTrue(all("redacted" in finding for finding in report["findings"]))

    def test_profile_pack_privacy_report_includes_findings_and_eval_warns(self) -> None:
        from write_as_me.cli import main
        from write_as_me.profile_pack import build_profile_pack

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            samples = root / "samples"
            output = root / "profile-pack"
            (samples / "message").mkdir(parents=True)
            (samples / "message" / "private.local.md").write_text(
                "교수님, 확인 부탁드립니다. 제 연락처는 010-1234-5678이고 "
                "메일은 sungbin@example.com입니다.",
                encoding="utf-8",
            )

            build_profile_pack(samples, output)

            profile = json.loads((output / "profile.json").read_text(encoding="utf-8"))
            privacy_report = (output / "privacy-report.md").read_text(encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                eval_exit = main(["eval", "--profile-pack", str(output), "--json"])
            eval_payload = json.loads(stdout.getvalue())

        self.assertEqual(profile["privacy"]["finding_count"], 2)
        self.assertEqual(profile["privacy"]["risk"], "high")
        self.assertIn("Privacy Findings", privacy_report)
        self.assertIn("email", privacy_report)
        self.assertIn("phone", privacy_report)
        self.assertNotIn("sungbin@example.com", privacy_report)
        self.assertEqual(eval_exit, 0)
        privacy_check = [check for check in eval_payload["checks"] if check["id"] == "privacy-scan"][0]
        self.assertEqual(privacy_check["status"], "warn")


if __name__ == "__main__":
    unittest.main()
