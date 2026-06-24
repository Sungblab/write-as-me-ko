from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any


PATTERNS: tuple[tuple[str, str, str], ...] = (
    ("email", r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![A-Za-z0-9._%+-])", "medium"),
    ("phone", r"(?<!\d)01[016789][-\s.]?\d{3,4}[-\s.]?\d{4}(?!\d)", "high"),
    ("resident_id", r"(?<!\d)\d{6}[-\s]?[1-4]\d{6}(?!\d)", "high"),
    ("student_id", r"(?<!\d)20\d{6,8}(?!\d)", "medium"),
    ("token_like", r"\b(?:sk|ghp|github_pat|xoxb|xoxp)-[A-Za-z0-9_\-]{20,}\b", "high"),
    ("url", r"https?://[^\s)>\]]+", "low"),
)

RISK_ORDER = {"none": 0, "low": 1, "medium": 2, "high": 3}


def _mask(value: str) -> str:
    if len(value) <= 6:
        return "[redacted]"
    return f"{value[:2]}...[redacted]...{value[-2:]}"


def _merge_risk(risks: list[str]) -> str:
    if not risks:
        return "none"
    return max(risks, key=lambda risk: RISK_ORDER[risk])


def scan_text(text: str, source_path: str = "") -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    for kind, pattern, risk in PATTERNS:
        for match in re.finditer(pattern, text):
            findings.append(
                {
                    "kind": kind,
                    "risk": risk,
                    "source_path": source_path,
                    "span": [match.start(), match.end()],
                    "redacted": _mask(match.group(0)),
                }
            )

    kind_counts = Counter(finding["kind"] for finding in findings)
    return {
        "risk": _merge_risk([finding["risk"] for finding in findings]),
        "finding_count": len(findings),
        "kind_counts": dict(kind_counts),
        "findings": findings,
    }


def scan_samples(samples: list[Any]) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    for sample in samples:
        source_path = getattr(sample, "relative_path", str(getattr(sample, "path", "")))
        report = scan_text(getattr(sample, "text", ""), source_path=source_path)
        findings.extend(report["findings"])

    kind_counts = Counter(finding["kind"] for finding in findings)
    path_counts = Counter(finding["source_path"] for finding in findings)
    private_path_count = sum(
        1
        for path in path_counts
        if "private" in Path(path).parts or path.endswith(".local.md")
    )
    return {
        "risk": _merge_risk([finding["risk"] for finding in findings]),
        "finding_count": len(findings),
        "kind_counts": dict(kind_counts),
        "path_counts": dict(path_counts),
        "private_path_count": private_path_count,
        "findings": findings,
    }
