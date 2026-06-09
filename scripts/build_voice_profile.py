from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


SUPPORTED_EXTENSIONS = {".md", ".txt"}
ROUTE_ORDER = ("blog", "report", "message", "project", "other")
IGNORED_SAMPLE_NAMES = {"readme.md", "template.md", ".gitkeep"}
KOREAN_RE = re.compile(r"[가-힣]")
SENTENCE_RE = re.compile(r"[^.!?。！？\n]+[.!?。！？]?")
TOKEN_RE = re.compile(r"[가-힣A-Za-z0-9+#./_-]+")

STOPWORDS = {
    "그리고",
    "그러나",
    "하지만",
    "그래서",
    "또한",
    "따라서",
    "이것은",
    "저것은",
    "것이다",
    "있다",
    "한다",
    "됩니다",
    "합니다",
}


@dataclass(frozen=True)
class Sample:
    path: Path
    route: str
    text: str


def infer_route(path: Path, samples_root: Path) -> str:
    try:
        rel = path.relative_to(samples_root)
    except ValueError:
        return "other"
    if len(rel.parts) < 2:
        return "other"
    route = rel.parts[0].lower()
    return route if route in ROUTE_ORDER else "other"


def collect_samples(samples_root: Path) -> list[Sample]:
    samples: list[Sample] = []
    if not samples_root.exists():
        return samples

    for path in sorted(samples_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        if path.name.lower() in IGNORED_SAMPLE_NAMES:
            continue
        text = path.read_text(encoding="utf-8").strip()
        if not text or not KOREAN_RE.search(text):
            continue
        samples.append(Sample(path=path, route=infer_route(path, samples_root), text=text))
    return samples


def split_sentences(text: str) -> list[str]:
    return [m.group(0).strip() for m in SENTENCE_RE.finditer(text) if m.group(0).strip()]


def extract_tokens(text: str) -> list[str]:
    tokens = [t.strip(".,!?;:()[]{}\"'`").lower() for t in TOKEN_RE.findall(text)]
    return [t for t in tokens if len(t) >= 2 and t not in STOPWORDS]


def confidence_for(sample_count: int, total_chars: int) -> str:
    if sample_count >= 7 and total_chars >= 6000:
        return "high"
    if sample_count >= 2 and total_chars >= 80:
        return "medium"
    if sample_count >= 1:
        return "low"
    return "none"


def summarize_route_counts(samples: list[Sample]) -> list[str]:
    counts = Counter(s.route for s in samples)
    lines: list[str] = []
    for route in ROUTE_ORDER:
        if counts.get(route):
            lines.append(f"- {route}: {counts[route]}")
    return lines or ["- none: 0"]


def top_phrases(samples: list[Sample], limit: int = 8) -> list[str]:
    counter: Counter[str] = Counter()
    for sample in samples:
        counter.update(extract_tokens(sample.text))
    return [phrase for phrase, _ in counter.most_common(limit)]


def detect_voice_notes(text: str) -> list[str]:
    notes: list[str] = []
    if any(word in text for word in ("과장", "근거", "실제", "구체", "검증")):
        notes.append("근거, 실제 문제, 검증 가능성을 중시하는 표현이 보입니다.")
    if any(word in text for word in ("교수님", "감사", "확인", "부탁")):
        notes.append("공식 메시지에서는 요청과 감사 표현을 짧게 붙이는 경향이 보입니다.")
    if any(word in text for word in ("나는", "내가", "생각", "느꼈")):
        notes.append("개인 글에서는 1인칭 판단 흐름을 사용할 수 있습니다.")
    if not notes:
        notes.append("아직 뚜렷한 판단 패턴이 부족합니다. 샘플을 더 추가하세요.")
    return notes


def build_profile_markdown(samples_root: Path) -> str:
    samples = collect_samples(samples_root)
    all_text = "\n\n".join(sample.text for sample in samples)
    total_chars = len(all_text)
    sentences = split_sentences(all_text)
    avg_sentence_length = round(
        sum(len(sentence) for sentence in sentences) / len(sentences), 1
    ) if sentences else 0.0
    confidence = confidence_for(len(samples), total_chars)
    phrases = top_phrases(samples)
    notes = detect_voice_notes(all_text)

    phrase_lines = [f"- {phrase}" for phrase in phrases] or ["- 샘플 부족"]
    note_lines = [f"- {note}" for note in notes]
    route_lines = summarize_route_counts(samples)

    return "\n".join(
        [
            "# Voice Profile",
            "",
            "Generated from local samples. Review and edit this file before relying on it for sensitive writing.",
            "",
            "## Current Status",
            "",
            f"- Confidence: {confidence}",
            f"- Source samples reviewed: {len(samples)}",
            f"- Total Korean text length: {total_chars} characters",
            "- Safe mode: preserve facts, avoid unsupported personal claims",
            "",
            "## Sample Routes",
            "",
            *route_lines,
            "",
            "## Quantitative Signals",
            "",
            f"- 평균 문장 길이: {avg_sentence_length}자",
            f"- 문장 수: {len(sentences)}",
            "",
            "## 자주 보이는 표현",
            "",
            *phrase_lines,
            "",
            "## 관찰된 문체/판단 패턴",
            "",
            *note_lines,
            "",
            "## Drafting Guidance",
            "",
            "- 보고서/과제는 격식체를 유지하고 근거와 한계를 분리합니다.",
            "- 블로그/회고는 판단이 바뀐 지점을 자연스럽게 드러냅니다.",
            "- 메시지는 배경을 길게 늘리지 말고 요청과 다음 행동을 분명히 씁니다.",
            "- 샘플에서 확인되지 않은 경험이나 감정은 만들지 않습니다.",
            "",
        ]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a Korean author voice profile.")
    parser.add_argument("--samples", default="samples", help="Samples directory")
    parser.add_argument(
        "--output",
        default="codex/skills/write-as-me-ko/references/voice-profile.md",
        help="Output Markdown path",
    )
    args = parser.parse_args(argv)

    markdown = build_profile_markdown(Path(args.samples))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
