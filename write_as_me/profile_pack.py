from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .privacy_scanner import scan_samples
from .style_signals import analyze_style_signals


SUPPORTED_EXTENSIONS = {".md", ".txt"}
ROUTE_ORDER = ("blog", "report", "message", "project", "other")
ROOT_GUIDANCE_FILES = {"readme.md", "template.md", ".gitkeep"}
KOREAN_RE = re.compile(r"[가-힣]")
SENTENCE_RE = re.compile(r"[^.!?。！？\n]+[.!?。！？]?")


@dataclass(frozen=True)
class PackSample:
    path: Path
    relative_path: str
    route: str
    text: str
    sha256: str


@dataclass(frozen=True)
class ProfilePackResult:
    output_dir: Path
    profile_path: Path
    manifest_path: Path
    voice_profile_path: Path
    route_map_path: Path
    privacy_report_path: Path
    coverage_report_path: Path


def infer_route(path: Path, samples_root: Path) -> str:
    try:
        rel = path.relative_to(samples_root)
    except ValueError:
        return "other"
    if len(rel.parts) < 2:
        return "other"
    route = rel.parts[0].lower()
    return route if route in ROUTE_ORDER else "other"


def _relative_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _is_guidance_file(path: Path, root: Path) -> bool:
    try:
        rel = path.relative_to(root)
    except ValueError:
        return False
    return len(rel.parts) == 1 and path.name.lower() in ROOT_GUIDANCE_FILES


def collect_pack_samples(samples_root: Path) -> list[PackSample]:
    samples: list[PackSample] = []
    if not samples_root.exists():
        return samples

    for path in sorted(samples_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        if _is_guidance_file(path, samples_root):
            continue
        text = path.read_text(encoding="utf-8").strip()
        if not text or not KOREAN_RE.search(text):
            continue
        samples.append(
            PackSample(
                path=path,
                relative_path=_relative_path(path, samples_root),
                route=infer_route(path, samples_root),
                text=text,
                sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
            )
        )
    return samples


def _split_sentences(text: str) -> list[str]:
    return [m.group(0).strip() for m in SENTENCE_RE.finditer(text) if m.group(0).strip()]


def _confidence(sample_count: int, total_chars: int, route_count: int) -> str:
    if sample_count >= 7 and total_chars >= 6000 and route_count >= 3:
        return "high"
    if sample_count >= 2 and total_chars >= 80:
        return "medium"
    if sample_count >= 1:
        return "low"
    return "none"


def _route_counts(samples: list[PackSample]) -> dict[str, int]:
    counts = Counter(sample.route for sample in samples)
    return {route: counts.get(route, 0) for route in ROUTE_ORDER if counts.get(route, 0)}


def _private_sample_paths(samples: list[PackSample]) -> list[str]:
    private: list[str] = []
    for sample in samples:
        parts = [part.lower() for part in Path(sample.relative_path).parts]
        if "private" in parts or sample.path.name.endswith(".local.md"):
            private.append(sample.relative_path)
    return private


def _profile_json(samples: list[PackSample]) -> dict[str, Any]:
    all_text = "\n\n".join(sample.text for sample in samples)
    sentences = _split_sentences(all_text)
    routes = _route_counts(samples)
    total_chars = len(all_text)
    style_features = analyze_style_signals(all_text)
    privacy_scan = scan_samples(samples)
    return {
        "schema_version": 2,
        "product": "write-as-me-ko",
        "purpose": "Korean author-context profile pack for AI writing agents",
        "raw_samples_included": False,
        "summary": {
            "sample_count": len(samples),
            "total_chars": total_chars,
            "sentence_count": len(sentences),
            "avg_sentence_chars": round(
                sum(len(sentence) for sentence in sentences) / len(sentences), 1
            )
            if sentences
            else 0.0,
            "confidence": _confidence(len(samples), total_chars, len(routes)),
        },
        "routes": routes,
        "style_features": style_features,
        "route_style_features": {
            route: analyze_style_signals("\n\n".join(sample.text for sample in samples if sample.route == route))
            for route in routes
        },
        "privacy": {
            "private_sample_count": len(_private_sample_paths(samples)),
            "raw_sample_text_exported": False,
            "risk": privacy_scan["risk"],
            "finding_count": privacy_scan["finding_count"],
            "kind_counts": privacy_scan["kind_counts"],
            "path_counts": privacy_scan["path_counts"],
        },
    }


def _sample_manifest(samples: list[PackSample]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "raw_samples_included": False,
        "samples": [
            {
                "path": sample.relative_path,
                "route": sample.route,
                "sha256": sample.sha256,
                "chars": len(sample.text),
            }
            for sample in samples
        ],
    }


def _voice_profile_markdown(profile: dict[str, Any]) -> str:
    summary = profile["summary"]
    routes = profile["routes"]
    route_lines = [f"- {route}: {count}" for route, count in routes.items()] or ["- none: 0"]
    return "\n".join(
        [
            "# Voice Profile",
            "",
            "Generated from local samples. Raw sample text is not included in this profile pack.",
            "",
            "## Current Status",
            "",
            f"- Confidence: {summary['confidence']}",
            f"- Source samples reviewed: {summary['sample_count']}",
            f"- Total Korean text length: {summary['total_chars']} characters",
            "- Safe mode: preserve facts, avoid unsupported personal claims",
            "",
            "## Sample Routes",
            "",
            *route_lines,
            "",
            "## Quantitative Signals",
            "",
            f"- 평균 문장 길이: {summary['avg_sentence_chars']}자",
            f"- 문장 수: {summary['sentence_count']}",
            "",
        ]
    )


def _route_map_markdown(samples: list[PackSample]) -> str:
    counts = _route_counts(samples)
    lines = ["# Route Map", "", "Use route coverage to decide which writing skill preset is safe to use.", ""]
    if not counts:
        lines.extend(["## Missing", "", "- No Korean sample routes were found.", ""])
        return "\n".join(lines)

    for route in ROUTE_ORDER:
        count = counts.get(route)
        if not count:
            continue
        lines.extend([f"## {route}", "", f"- Samples: {count}", ""])
    return "\n".join(lines)


def _privacy_report_markdown(samples: list[PackSample], profile: dict[str, Any]) -> str:
    private_paths = _private_sample_paths(samples)
    privacy = profile.get("privacy", {})
    lines = [
        "# Privacy Report",
        "",
        "- Raw sample text included: no",
        "- Hashes and character counts are included for reproducible local checks.",
        f"- Privacy risk: {privacy.get('risk', 'none')}",
        f"- Privacy findings: {privacy.get('finding_count', 0)}",
        "",
        "## Private Samples",
        "",
    ]
    if private_paths:
        lines.append("- Private-looking sample paths were analyzed locally:")
        lines.extend(f"  - `{path}`" for path in private_paths)
    else:
        lines.append("- No `private/` or `*.local.md` samples were detected.")
    lines.extend(["", "## Privacy Findings", ""])
    kind_counts = privacy.get("kind_counts", {})
    if kind_counts:
        lines.extend(f"- {kind}: {count}" for kind, count in sorted(kind_counts.items()))
        lines.append("- Values are redacted and are not copied into this report.")
    else:
        lines.append("- No email, phone, student id, resident id, token-like, or URL patterns detected.")
    lines.extend(["", "## Rule", "", "- Do not commit raw personal samples or generated exports containing raw sample text.", ""])
    return "\n".join(lines)


def _coverage_report_markdown(profile: dict[str, Any]) -> str:
    routes = profile["routes"]
    confidence = profile["summary"]["confidence"]
    style_features = profile.get("style_features", {})
    covered = ", ".join(routes.keys()) if routes else "none"
    missing = [route for route in ("blog", "report", "message", "project") if route not in routes]
    lines = [
        "# Coverage Report",
        "",
        "## Coverage Status",
        "",
        f"- Confidence: {confidence}",
        f"- Covered routes: {covered}",
        f"- Missing recommended routes: {', '.join(missing) if missing else 'none'}",
        "",
        "## Style Signals",
        "",
        f"- Signal groups: {', '.join(style_features.get('signal_groups', [])) or 'none'}",
        f"- Sentence count: {style_features.get('sentence_count', 0)}",
        f"- Average sentence length: {style_features.get('avg_sentence_chars', 0.0)} characters",
        f"- First-person markers: {style_features.get('first_person_count', 0)}",
        f"- Bullet lines: {style_features.get('bullet_line_count', 0)}",
        "",
    ]
    return "\n".join(lines)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_profile_pack_from_samples(samples: list[PackSample], output_dir: Path) -> ProfilePackResult:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    profile = _profile_json(samples)
    manifest = _sample_manifest(samples)

    profile_path = output_dir / "profile.json"
    manifest_path = output_dir / "sample-manifest.json"
    voice_profile_path = output_dir / "voice-profile.md"
    route_map_path = output_dir / "route-map.md"
    privacy_report_path = output_dir / "privacy-report.md"
    coverage_report_path = output_dir / "coverage-report.md"

    _write_json(profile_path, profile)
    _write_json(manifest_path, manifest)
    voice_profile_path.write_text(_voice_profile_markdown(profile), encoding="utf-8")
    route_map_path.write_text(_route_map_markdown(samples), encoding="utf-8")
    privacy_report_path.write_text(_privacy_report_markdown(samples, profile), encoding="utf-8")
    coverage_report_path.write_text(_coverage_report_markdown(profile), encoding="utf-8")

    return ProfilePackResult(
        output_dir=output_dir,
        profile_path=profile_path,
        manifest_path=manifest_path,
        voice_profile_path=voice_profile_path,
        route_map_path=route_map_path,
        privacy_report_path=privacy_report_path,
        coverage_report_path=coverage_report_path,
    )


def build_profile_pack(samples_root: Path, output_dir: Path) -> ProfilePackResult:
    samples_root = Path(samples_root)
    return build_profile_pack_from_samples(collect_pack_samples(samples_root), output_dir)
