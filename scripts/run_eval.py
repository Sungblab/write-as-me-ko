from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


DEFAULT_INPUT = Path("eval/before-after.md")
DEFAULT_OUTPUT = Path("_workspace/eval/evaluation-report.md")
REFERENCE_ROOT = Path("codex/skills/write-as-me-ko/references")
KOREAN_RE = re.compile(r"[가-힣]")

AI_TELL_PHRASES = (
    "결론적으로",
    "시사하는 바가 크다",
    "주목할 만하다",
    "중요한 역할",
    "다양한 가능성",
    "혁신적인",
    "효율적인",
    "의미 있는",
)

FACT_ALIASES = {
    "korean users": ("Korean users", "한국어 사용자", "한국어 사용자가", "한국어 사용자는"),
    "local-first": ("local-first", "로컬-first", "로컬 first", "로컬에 두"),
}


def _reference(name: str) -> str:
    return (REFERENCE_ROOT / name).as_posix()


@dataclass(frozen=True)
class EvalCase:
    title: str
    route: str
    prompt: str
    expected_facts: tuple[str, ...]
    required_profile_signals: tuple[str, ...]
    generic_draft: str
    target_draft: str
    notes: str


@dataclass(frozen=True)
class CheckResult:
    status: str
    message: str
    reference: str


@dataclass(frozen=True)
class CaseResult:
    case: EvalCase
    checks: dict[str, CheckResult]
    generic_issues: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return all(check.status == "pass" for check in self.checks.values())


def _collect_list(lines: list[str], start: int) -> tuple[tuple[str, ...], int]:
    values: list[str] = []
    index = start
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if stripped.startswith("- "):
            values.append(stripped[2:].strip())
            index += 1
            continue
        if not stripped:
            index += 1
            if values:
                break
            continue
        break
    return tuple(values), index


def _collect_section(lines: list[str], start: int) -> tuple[str, int]:
    body: list[str] = []
    index = start
    while index < len(lines):
        if lines[index].startswith("### "):
            break
        body.append(lines[index])
        index += 1
    return "\n".join(body).strip(), index


def _parse_case(title: str, body: str) -> EvalCase:
    lines = body.splitlines()
    route = ""
    prompt = ""
    expected_facts: tuple[str, ...] = ()
    required_profile_signals: tuple[str, ...] = ()
    generic_draft = ""
    target_draft = ""
    notes = ""
    index = 0

    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.startswith("Route:"):
            route = stripped.removeprefix("Route:").strip().lower()
            index += 1
        elif stripped.startswith("Prompt:"):
            prompt = stripped.removeprefix("Prompt:").strip()
            index += 1
        elif stripped == "Expected Facts:":
            expected_facts, index = _collect_list(lines, index + 1)
        elif stripped == "Required Profile Signals:":
            required_profile_signals, index = _collect_list(lines, index + 1)
        elif stripped == "### Generic Draft":
            generic_draft, index = _collect_section(lines, index + 1)
        elif stripped == "### write-as-me-ko Draft":
            target_draft, index = _collect_section(lines, index + 1)
        elif stripped == "### Notes":
            notes, index = _collect_section(lines, index + 1)
        else:
            index += 1

    return EvalCase(
        title=title,
        route=route,
        prompt=prompt,
        expected_facts=expected_facts,
        required_profile_signals=required_profile_signals,
        generic_draft=generic_draft,
        target_draft=target_draft,
        notes=notes,
    )


def parse_before_after_cases(markdown: str) -> list[EvalCase]:
    matches = list(re.finditer(r"^### Case(?::\s*(.+))?$", markdown, flags=re.MULTILINE))
    cases: list[EvalCase] = []
    for position, match in enumerate(matches):
        title = (match.group(1) or f"Case {position + 1}").strip()
        start = match.end()
        end = matches[position + 1].start() if position + 1 < len(matches) else len(markdown)
        cases.append(_parse_case(title, markdown[start:end]))
    return cases


def _contains_fact(text: str, fact: str) -> bool:
    normalized = fact.strip()
    aliases = FACT_ALIASES.get(normalized.lower(), (normalized,))
    return any(alias in text for alias in aliases)


def _generic_issues(text: str) -> tuple[str, ...]:
    return tuple(phrase for phrase in AI_TELL_PHRASES if phrase in text)


def _check_fact_preservation(case: EvalCase) -> CheckResult:
    missing = [fact for fact in case.expected_facts if not _contains_fact(case.target_draft, fact)]
    if not missing:
        return CheckResult(
            "pass",
            "All expected facts are present in the write-as-me-ko draft.",
            _reference("judgment-rules.md"),
        )
    return CheckResult(
        "fail",
        "Missing expected facts: " + ", ".join(missing),
        f"{_reference('judgment-rules.md')}; {_reference('voice-profile.md')}",
    )


def _check_genre_preservation(case: EvalCase) -> CheckResult:
    route = case.route
    draft = case.target_draft
    passed = False
    if route == "report":
        passed = "다." in draft and "근거" in draft
    elif route == "blog":
        passed = any(token in draft for token in ("나는", "내가", "생각", "봤다", "느꼈"))
    elif route == "message":
        passed = any(token in draft for token in ("교수님", "부탁", "확인", "검토")) and any(
            token in draft for token in ("드립니다", "감사", "부탁드립니다")
        )
    elif route == "project":
        passed = any(token in draft for token in ("README", "프로젝트", "검증", "사용"))
    else:
        passed = bool(KOREAN_RE.search(draft))

    if passed:
        return CheckResult(
            "pass",
            f"Draft matches the expected `{route}` route.",
            _reference("format-routes.md"),
        )
    return CheckResult(
        "fail",
        f"Draft does not preserve the expected `{route}` route.",
        _reference("format-routes.md"),
    )


def _check_korean_naturalness(case: EvalCase) -> CheckResult:
    issues = _generic_issues(case.target_draft)
    if not KOREAN_RE.search(case.target_draft):
        return CheckResult(
            "fail",
            "Draft does not contain enough Korean text for this Korean-first evaluation.",
            _reference("anti-ai-tells-ko.md"),
        )
    if issues:
        return CheckResult(
            "fail",
            "AI-tell phrases remain: " + ", ".join(issues),
            _reference("anti-ai-tells-ko.md"),
        )
    return CheckResult(
        "pass",
        "No configured Korean AI-tell phrases remain in the write-as-me-ko draft.",
        _reference("anti-ai-tells-ko.md"),
    )


def _check_profile_usage(case: EvalCase) -> CheckResult:
    missing = [signal for signal in case.required_profile_signals if signal not in case.target_draft]
    if not missing:
        return CheckResult(
            "pass",
            "Required profile signals appear in the write-as-me-ko draft.",
            _reference("voice-profile.md"),
        )
    return CheckResult(
        "fail",
        "Missing required profile signals: " + ", ".join(missing),
        _reference("voice-profile.md"),
    )


def evaluate_cases(cases: list[EvalCase]) -> list[CaseResult]:
    results: list[CaseResult] = []
    for case in cases:
        checks = {
            "fact_preservation": _check_fact_preservation(case),
            "genre_preservation": _check_genre_preservation(case),
            "korean_naturalness": _check_korean_naturalness(case),
            "profile_usage": _check_profile_usage(case),
        }
        results.append(CaseResult(case=case, checks=checks, generic_issues=_generic_issues(case.generic_draft)))
    return results


def build_evaluation_report(results: list[CaseResult]) -> str:
    passed_count = sum(1 for result in results if result.passed)
    status = "pass" if results and passed_count == len(results) else "fail"
    lines = [
        "# Stage 4 Evaluation Report",
        "",
        f"Status: {status}",
        f"Cases: {len(results)}",
        f"Passing: {passed_count}",
        "",
        "This report is generated from committed synthetic before/after cases. It does not read private samples.",
        "",
    ]

    for result in results:
        lines.extend(
            [
                f"## {result.case.title}",
                "",
                f"- Route: `{result.case.route}`",
                f"- Result: {'pass' if result.passed else 'fail'}",
                f"- Generic baseline issues: {', '.join(result.generic_issues) if result.generic_issues else 'none'}",
                "",
                "### Checks",
                "",
            ]
        )
        for name, check in result.checks.items():
            lines.append(f"- {name}: {check.status} - {check.message}")
        failing = [check for check in result.checks.values() if check.status == "fail"]
        if failing:
            lines.extend(["", "### Suggested Reference Gaps", ""])
            for check in failing:
                lines.append(f"- {check.message} -> review `{check.reference}`")
        lines.append("")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run local Stage 4 text evaluation.")
    parser.add_argument("--repo-root", default=".", help="Repository root")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Before/after Markdown input")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Evaluation report output")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root)
    input_path = repo_root / args.input
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = repo_root / output_path

    markdown = input_path.read_text(encoding="utf-8")
    results = evaluate_cases(parse_before_after_cases(markdown))
    report = build_evaluation_report(results)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"wrote {output_path}")
    return 0 if results and all(result.passed for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
