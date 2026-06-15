from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.run_eval import (
    build_evaluation_report,
    evaluate_cases,
    parse_before_after_cases,
)


BEFORE_AFTER = """# Before / After Log

### Case: Report intro

Route: report
Prompt: Write a Korean report introduction about local-first writing context.

Expected Facts:
- local-first
- Korean users

Required Profile Signals:
- 근거
- 한계

### Generic Draft

이 솔루션은 혁신적인 가능성을 제시한다. 결론적으로 중요한 역할을 한다.

### write-as-me-ko Draft

로컬-first 글쓰기 컨텍스트는 한국어 사용자가 매번 문체 설명을 반복하지 않아도
보고서의 근거와 한계를 먼저 정리하게 돕는다. 이 방식은 샘플을 로컬에 두는 것을
전제로 하므로, 작성자는 민감한 원문을 외부에 올리지 않고도 초안을 점검할 수 있다.

### Notes

- What improved: 근거와 한계를 분리했다.
- What still sounds wrong: 없음.
- Profile update needed: 없음.
"""


class RunEvalTests(unittest.TestCase):
    def test_parse_before_after_cases_reads_route_facts_and_drafts(self) -> None:
        cases = parse_before_after_cases(BEFORE_AFTER)

        self.assertEqual(len(cases), 1)
        self.assertEqual(cases[0].title, "Report intro")
        self.assertEqual(cases[0].route, "report")
        self.assertIn("local-first", cases[0].expected_facts)
        self.assertIn("Korean users", cases[0].expected_facts)
        self.assertIn("근거", cases[0].required_profile_signals)
        self.assertIn("혁신적인 가능성", cases[0].generic_draft)
        self.assertIn("로컬-first 글쓰기 컨텍스트", cases[0].target_draft)

    def test_evaluate_cases_marks_passing_case_and_reports_generic_baseline_issues(self) -> None:
        cases = parse_before_after_cases(BEFORE_AFTER)

        results = evaluate_cases(cases)

        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].passed)
        self.assertEqual(results[0].checks["fact_preservation"].status, "pass")
        self.assertEqual(results[0].checks["genre_preservation"].status, "pass")
        self.assertEqual(results[0].checks["korean_naturalness"].status, "pass")
        self.assertEqual(results[0].checks["profile_usage"].status, "pass")
        self.assertIn("결론적으로", results[0].generic_issues)

    def test_build_evaluation_report_points_failures_to_concrete_reference_gaps(self) -> None:
        broken = BEFORE_AFTER.replace("로컬-first 글쓰기 컨텍스트", "이 도구").replace(
            "샘플을 로컬에 두는 것을", "샘플을 관리하는 것을"
        )
        cases = parse_before_after_cases(broken)
        results = evaluate_cases(cases)

        report = build_evaluation_report(results)

        self.assertIn("Status: fail", report)
        self.assertIn("Missing expected facts", report)
        self.assertIn("codex/skills/write-as-me-ko/references/judgment-rules.md", report)
        self.assertIn("codex/skills/write-as-me-ko/references/voice-profile.md", report)

    def test_main_command_writes_local_artifact_without_private_samples(self) -> None:
        from scripts.run_eval import main

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "eval").mkdir()
            (root / "eval" / "before-after.md").write_text(BEFORE_AFTER, encoding="utf-8")

            exit_code = main(
                [
                    "--repo-root",
                    str(root),
                    "--output",
                    str(root / "_workspace" / "eval" / "evaluation-report.md"),
                ]
            )

            artifact = root / "_workspace" / "eval" / "evaluation-report.md"
            self.assertEqual(exit_code, 0)
            self.assertTrue(artifact.exists())
            self.assertIn("Stage 4 Evaluation Report", artifact.read_text(encoding="utf-8"))
            self.assertFalse((root / "samples" / "private").exists())


if __name__ == "__main__":
    unittest.main()
