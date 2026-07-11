from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from .style_signals import analyze_style_signals, split_sentences


GENERIC_AI_TELLS = (
    "결론적으로",
    "요약하면",
    "종합해보면",
    "중요한 것은",
    "이를 통해",
    "첫째",
    "둘째",
    "마지막으로",
    "전반적으로",
)

MODE_GUIDANCE = {
    "minimal": "Preserve the current structure and only revise sentences that create clear style-distance or AI-tell risk.",
    "balanced": "Revise wording, rhythm, and paragraph flow while preserving facts and the target route.",
    "strong": "Restructure the draft when needed, but do not invent personal experiences, facts, emotions, or claims.",
}


def read_profile(profile_pack: Path) -> dict[str, Any]:
    return json.loads((Path(profile_pack) / "profile.json").read_text(encoding="utf-8"))


def _distribution_distance(left: dict[str, int], right: dict[str, int]) -> float:
    keys = set(left) | set(right)
    left_total = sum(left.values())
    right_total = sum(right.values())
    if not keys or (left_total == 0 and right_total == 0):
        return 0.0
    distance = 0.0
    for key in keys:
        left_value = left.get(key, 0) / left_total if left_total else 0.0
        right_value = right.get(key, 0) / right_total if right_total else 0.0
        distance += abs(left_value - right_value)
    return min(distance / 2, 1.0)


def _numeric_distance(left: float, right: float, scale: float) -> float:
    if left == 0 and right == 0:
        return 0.0
    return min(abs(left - right) / scale, 1.0)


def _ratio_distance(left: float, right: float) -> float:
    return min(abs(left - right), 1.0)


def _sentence_length_stdev(text: str) -> float:
    lengths = [len(sentence) for sentence in split_sentences(text)]
    if len(lengths) < 2:
        return 0.0
    avg = sum(lengths) / len(lengths)
    variance = sum((length - avg) ** 2 for length in lengths) / len(lengths)
    return math.sqrt(variance)


def style_distance(profile_features: dict[str, Any], draft_features: dict[str, Any]) -> dict[str, Any]:
    component_weights = {
        "sentence_length": 0.18,
        "endings": 0.18,
        "connectors": 0.14,
        "first_person": 0.12,
        "stance": 0.14,
        "structure": 0.08,
        "english_ratio": 0.06,
        "character_ngrams": 0.10,
    }
    component_scores = {
        "sentence_length": _numeric_distance(
            float(profile_features.get("avg_sentence_chars", 0.0)),
            float(draft_features.get("avg_sentence_chars", 0.0)),
            45.0,
        ),
        "endings": _distribution_distance(
            profile_features.get("ending_counts", {}),
            draft_features.get("ending_counts", {}),
        ),
        "connectors": _distribution_distance(
            profile_features.get("connector_counts", {}),
            draft_features.get("connector_counts", {}),
        ),
        "first_person": _numeric_distance(
            float(profile_features.get("first_person_count", 0)),
            float(draft_features.get("first_person_count", 0)),
            max(float(profile_features.get("sentence_count", 1)), 1.0),
        ),
        "stance": _distribution_distance(
            {
                **{f"hedge:{key}": value for key, value in profile_features.get("hedge_counts", {}).items()},
                **{f"assertive:{key}": value for key, value in profile_features.get("assertive_counts", {}).items()},
            },
            {
                **{f"hedge:{key}": value for key, value in draft_features.get("hedge_counts", {}).items()},
                **{f"assertive:{key}": value for key, value in draft_features.get("assertive_counts", {}).items()},
            },
        ),
        "structure": _numeric_distance(
            float(profile_features.get("bullet_line_count", 0)),
            float(draft_features.get("bullet_line_count", 0)),
            6.0,
        ),
        "english_ratio": _ratio_distance(
            float(profile_features.get("english_char_ratio", 0.0)),
            float(draft_features.get("english_char_ratio", 0.0)),
        ),
        "character_ngrams": _distribution_distance(
            profile_features.get("char_bigram_counts", {}),
            draft_features.get("char_bigram_counts", {}),
        ),
    }
    distance = sum(component_scores[key] * component_weights[key] for key in component_weights)
    return {
        "distance": round(distance, 3),
        "similarity": round(1 - distance, 3),
        "components": {key: round(value, 3) for key, value in component_scores.items()},
    }


def _route_features(profile: dict[str, Any], route: str | None) -> dict[str, Any]:
    if route:
        route_features = profile.get("route_style_features", {}).get(route)
        if route_features:
            return route_features
    return profile.get("style_features", {})


def ai_tell_risks(profile_features: dict[str, Any], draft_text: str, draft_features: dict[str, Any]) -> list[dict[str, str]]:
    risks: list[dict[str, str]] = []
    sentence_count = draft_features.get("sentence_count", 0)
    avg_sentence_chars = float(draft_features.get("avg_sentence_chars", 0.0))
    sentence_stdev = _sentence_length_stdev(draft_text)
    generic_hits = {phrase: draft_text.count(phrase) for phrase in GENERIC_AI_TELLS if draft_text.count(phrase)}

    if sentence_count >= 4 and sentence_stdev < 8:
        risks.append(
            {
                "id": "uniform-sentence-rhythm",
                "severity": "medium",
                "message": "Sentences have a very even rhythm; vary sentence length and paragraph movement.",
            }
        )
    if avg_sentence_chars > float(profile_features.get("avg_sentence_chars", 0.0)) + 25:
        risks.append(
            {
                "id": "long-polished-sentences",
                "severity": "medium",
                "message": "Draft sentences are much longer than the profile baseline.",
            }
        )
    if generic_hits:
        risks.append(
            {
                "id": "generic-ai-transitions",
                "severity": "high" if sum(generic_hits.values()) >= 3 else "medium",
                "message": "Generic AI transition phrases remain: " + ", ".join(generic_hits.keys()),
            }
        )
    if profile_features.get("first_person_count", 0) > 0 and draft_features.get("first_person_count", 0) == 0:
        risks.append(
            {
                "id": "missing-first-person-stance",
                "severity": "medium",
                "message": "Profile uses first-person stance, but the draft has no first-person markers.",
            }
        )
    if profile_features.get("hedge_counts") and not draft_features.get("hedge_counts"):
        risks.append(
            {
                "id": "missing-uncertainty",
                "severity": "medium",
                "message": "Profile contains uncertainty/limit markers, but the draft sounds too settled.",
            }
        )
    return risks


def evaluate_draft(profile_pack: Path, draft_text: str, route: str | None = None) -> dict[str, Any]:
    profile = read_profile(profile_pack)
    profile_features = _route_features(profile, route)
    draft_features = analyze_style_signals(draft_text)
    distance = style_distance(profile_features, draft_features)
    risks = ai_tell_risks(profile_features, draft_text, draft_features)
    return {
        "route": route or "profile",
        "profile_confidence": profile.get("summary", {}).get("confidence", "unknown"),
        "style_distance": distance,
        "draft_features": {
            "sentence_count": draft_features.get("sentence_count", 0),
            "avg_sentence_chars": draft_features.get("avg_sentence_chars", 0.0),
            "signal_groups": draft_features.get("signal_groups", []),
        },
        "ai_tell_risks": risks,
    }


def compare_variants(
    profile_pack: Path,
    human_text: str,
    generic_text: str,
    profile_guided_text: str,
    route: str | None = None,
) -> dict[str, Any]:
    variants = {
        "human": evaluate_draft(profile_pack, human_text, route),
        "generic_llm": evaluate_draft(profile_pack, generic_text, route),
        "profile_guided": evaluate_draft(profile_pack, profile_guided_text, route),
    }
    generic_distance = variants["generic_llm"]["style_distance"]["distance"]
    guided_distance = variants["profile_guided"]["style_distance"]["distance"]
    return {
        "route": route or "profile",
        "variants": variants,
        "profile_guided_closer_than_generic": guided_distance < generic_distance,
        "distance_delta": round(generic_distance - guided_distance, 3),
    }


def build_style_distance_report(result: dict[str, Any]) -> str:
    if "variants" in result:
        lines = [
            "# Style-Distance Report",
            "",
            f"- Route: {result['route']}",
            f"- Profile-guided closer than generic: {str(result['profile_guided_closer_than_generic']).lower()}",
            f"- Distance delta: {result['distance_delta']}",
            "",
            "| Variant | Distance | Similarity | AI-tell risks |",
            "| --- | ---: | ---: | ---: |",
        ]
        for name, payload in result["variants"].items():
            style = payload["style_distance"]
            lines.append(
                f"| {name} | {style['distance']} | {style['similarity']} | {len(payload['ai_tell_risks'])} |"
            )
        lines.extend(["", "## Notes", "", "- Lower distance means closer to the profile's deterministic style signals.", ""])
        return "\n".join(lines)

    style = result["style_distance"]
    lines = [
        "# Style-Distance Report",
        "",
        f"- Route: {result['route']}",
        f"- Distance: {style['distance']}",
        f"- Similarity: {style['similarity']}",
        f"- AI-tell risks: {len(result['ai_tell_risks'])}",
        "",
        "## Component Distances",
        "",
    ]
    lines.extend(f"- {key}: {value}" for key, value in style["components"].items())
    lines.extend(["", "## AI-Tell Risks", ""])
    if result["ai_tell_risks"]:
        lines.extend(f"- {risk['id']} ({risk['severity']}): {risk['message']}" for risk in result["ai_tell_risks"])
    else:
        lines.append("- No configured AI-tell risks found.")
    lines.append("")
    return "\n".join(lines)


def build_rewrite_brief(
    profile_pack: Path,
    draft_path: Path,
    route: str,
    mode: str = "balanced",
) -> str:
    if mode not in MODE_GUIDANCE:
        raise ValueError(f"unknown rewrite mode: {mode}")
    draft_path = Path(draft_path)
    draft_text = draft_path.read_text(encoding="utf-8")
    evaluation = evaluate_draft(profile_pack, draft_text, route)
    style = evaluation["style_distance"]
    risk_lines = [
        f"- {risk['id']} ({risk['severity']}): {risk['message']}" for risk in evaluation["ai_tell_risks"]
    ] or ["- No configured AI-tell risks found. Preserve the draft unless the user asks for a stronger rewrite."]
    return "\n".join(
        [
            "# Rewrite Brief",
            "",
            "Use this brief with Codex, Claude Code, or another writing agent. It does not include raw profile samples.",
            "",
            "## Input",
            "",
            f"- Draft path: `{draft_path.as_posix()}`",
            f"- Route: {route}",
            f"- Rewrite mode: {mode}",
            f"- Mode guidance: {MODE_GUIDANCE[mode]}",
            "",
            "## Current Style Distance",
            "",
            f"- Distance: {style['distance']}",
            f"- Similarity: {style['similarity']}",
            f"- Profile confidence: {evaluation['profile_confidence']}",
            "",
            "## AI-Tell Risks",
            "",
            *risk_lines,
            "",
            "## Rewrite Instructions",
            "",
            "- Preserve facts, names, dates, numbers, links, quotes, and source meaning.",
            "- Match the route before surface voice.",
            "- Move the draft closer to the profile signals without copying private samples.",
            "- Keep uncertainty and personal judgment when the source supports it.",
            "- Do not invent personal experiences, achievements, emotions, relationships, or metrics.",
            "- Do not claim or optimize for AI detector bypass.",
            "",
        ]
    )
