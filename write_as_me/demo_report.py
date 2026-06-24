from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_demo_report(profile_pack: Path) -> str:
    profile_pack = Path(profile_pack)
    profile = _read_json(profile_pack / "profile.json")
    summary = profile.get("summary", {})
    routes = profile.get("routes", {})
    privacy = profile.get("privacy", {})
    style = profile.get("style_features", {})
    covered_routes = ", ".join(routes.keys()) if routes else "none"
    signal_groups = ", ".join(style.get("signal_groups", [])) or "none"
    privacy_kinds = ", ".join(privacy.get("kind_counts", {}).keys()) or "none"

    return "\n".join(
        [
            "# Write As Me KO Demo Report",
            "",
            "This report is generated from Profile Pack v2 metadata. It does not include raw sample text.",
            "",
            "## Profile Pack Summary",
            "",
            f"- Confidence: {summary.get('confidence', 'unknown')}",
            f"- Source samples reviewed: {summary.get('sample_count', 0)}",
            f"- Covered routes: {covered_routes}",
            f"- Raw samples included: {'yes' if profile.get('raw_samples_included') else 'no'}",
            "",
            "## Style Signals",
            "",
            f"- Signal groups: {signal_groups}",
            f"- Average sentence length: {style.get('avg_sentence_chars', 0.0)} characters",
            f"- Endings tracked: {', '.join(style.get('ending_counts', {}).keys()) or 'none'}",
            f"- Connectors tracked: {', '.join(style.get('connector_counts', {}).keys()) or 'none'}",
            f"- First-person markers: {style.get('first_person_count', 0)}",
            "",
            "## Privacy",
            "",
            f"- Privacy risk: {privacy.get('risk', 'none')}",
            f"- Privacy finding count: {privacy.get('finding_count', 0)}",
            f"- Finding kinds: {privacy_kinds}",
            "- Export stores findings by kind/count/redacted form, not raw sample values.",
            "",
            "## What changes with the profile pack",
            "",
            "| Scenario | Generic agent | Profile-aware agent |",
            "| --- | --- | --- |",
            "| Blog/reflection | Polishes into a broad summary. | Keeps route-specific judgment flow and measured first-person stance. |",
            "| Project document | May over-explain the tool. | Separates implementation, verification, limits, and next action. |",
            "| Message | May add excess context. | Keeps request, schedule, and thanks compact. |",
            "| Privacy | Usually depends on manual caution. | Runs local privacy checks and exports no raw samples. |",
            "",
            "## Judge-facing claim",
            "",
            "`write-as-me-ko` is a local-first Korean author-context compiler. It extracts reproducible style and privacy signals, then exports portable agent context and reusable writing skills.",
            "",
        ]
    )


def write_demo_report(profile_pack: Path, output: Path) -> Path:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_demo_report(Path(profile_pack)), encoding="utf-8")
    return output
