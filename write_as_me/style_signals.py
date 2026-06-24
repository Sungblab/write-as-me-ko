from __future__ import annotations

import re
from collections import Counter
from typing import Any


SENTENCE_RE = re.compile(r"[^.!?。！？\n]+[.!?。！？]?")
TOKEN_RE = re.compile(r"[가-힣A-Za-z0-9+#./_-]+")
KOREAN_CHAR_RE = re.compile(r"[가-힣]")
ENDING_RE = re.compile(r"([가-힣]{1,4})(?:[.!?。！？]|$)")

CONNECTORS = (
    "그리고",
    "그런데",
    "하지만",
    "그래서",
    "따라서",
    "다만",
    "또한",
    "막상",
    "실제로",
    "결국",
)
FIRST_PERSON = ("나는", "내가", "저는", "제가", "나의", "내")
HEDGE_WORDS = ("아직", "아마", "대략", "정도", "가능성", "한계", "모른다", "확실하지")
ASSERTIVE_WORDS = ("반드시", "무조건", "확실히", "분명히", "당연히")


def split_sentences(text: str) -> list[str]:
    return [match.group(0).strip() for match in SENTENCE_RE.finditer(text) if match.group(0).strip()]


def _tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(text)


def _ending(sentence: str) -> str | None:
    stripped = sentence.strip()
    if not stripped:
        return None
    stripped = stripped.rstrip(".!?。！？")
    if not stripped:
        return None
    last = stripped[-1]
    if KOREAN_CHAR_RE.match(last):
        return last
    return None


def _count_contains(text: str, candidates: tuple[str, ...]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for candidate in candidates:
        count = text.count(candidate)
        if count:
            counts[candidate] = count
    return dict(counts)


def _char_ngrams(text: str, n: int = 2, limit: int = 12) -> dict[str, int]:
    compact = "".join(ch for ch in text if KOREAN_CHAR_RE.match(ch))
    counts: Counter[str] = Counter(compact[i : i + n] for i in range(max(len(compact) - n + 1, 0)))
    return dict(counts.most_common(limit))


def _signal_groups(signals: dict[str, Any]) -> list[str]:
    groups: list[str] = []
    if signals["sentence_count"]:
        groups.append("sentence-length")
    if signals["connector_counts"]:
        groups.append("connectors")
    if signals["ending_counts"]:
        groups.append("endings")
    if signals["first_person_count"]:
        groups.append("first-person")
    if signals["bullet_line_count"]:
        groups.append("structure")
    if signals["hedge_counts"] or signals["assertive_counts"]:
        groups.append("stance")
    if signals["char_bigram_counts"]:
        groups.append("character-ngrams")
    return groups


def analyze_style_signals(text: str) -> dict[str, Any]:
    sentences = split_sentences(text)
    sentence_lengths = [len(sentence) for sentence in sentences]
    tokens = _tokens(text)
    endings = Counter(ending for ending in (_ending(sentence) for sentence in sentences) if ending)
    bullet_line_count = sum(
        1 for line in text.splitlines() if line.strip().startswith(("-", "*", "1.", "2.", "3."))
    )
    korean_chars = sum(1 for ch in text if KOREAN_CHAR_RE.match(ch))
    english_chars = sum(1 for ch in text if ("A" <= ch <= "Z") or ("a" <= ch <= "z"))
    signals: dict[str, Any] = {
        "sentence_count": len(sentences),
        "avg_sentence_chars": round(sum(sentence_lengths) / len(sentence_lengths), 1)
        if sentence_lengths
        else 0.0,
        "max_sentence_chars": max(sentence_lengths) if sentence_lengths else 0,
        "token_count": len(tokens),
        "korean_char_count": korean_chars,
        "english_char_count": english_chars,
        "english_char_ratio": round(english_chars / (korean_chars + english_chars), 3)
        if korean_chars + english_chars
        else 0.0,
        "bullet_line_count": bullet_line_count,
        "ending_counts": dict(endings.most_common(8)),
        "connector_counts": _count_contains(text, CONNECTORS),
        "first_person_count": sum(text.count(word) for word in FIRST_PERSON),
        "hedge_counts": _count_contains(text, HEDGE_WORDS),
        "assertive_counts": _count_contains(text, ASSERTIVE_WORDS),
        "char_bigram_counts": _char_ngrams(text, n=2),
    }
    signals["signal_groups"] = _signal_groups(signals)
    return signals
