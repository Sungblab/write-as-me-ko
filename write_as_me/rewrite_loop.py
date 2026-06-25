from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .style_distance import build_rewrite_brief, build_style_distance_report, evaluate_draft


def prepare_rewrite_loop(
    profile_pack: Path,
    draft_path: Path,
    output_dir: Path,
    route: str,
    mode: str = "balanced",
) -> dict[str, Any]:
    profile_pack = Path(profile_pack)
    draft_path = Path(draft_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    draft_text = draft_path.read_text(encoding="utf-8")
    before = evaluate_draft(profile_pack, draft_text, route)
    before["status"] = "ok"
    before_report = output_dir / "style-distance-before.md"
    brief_path = output_dir / "rewrite-brief.md"
    manifest_path = output_dir / "rewrite-loop.json"

    before_report.write_text(build_style_distance_report(before), encoding="utf-8")
    brief_path.write_text(build_rewrite_brief(profile_pack, draft_path, route=route, mode=mode), encoding="utf-8")
    manifest = {
        "schema_version": 1,
        "raw_profile_samples_included": False,
        "profile_pack": str(profile_pack),
        "draft_path": str(draft_path),
        "route": route,
        "mode": mode,
        "before_distance": before["style_distance"]["distance"],
        "before_ai_tell_risk_count": len(before["ai_tell_risks"]),
        "artifacts": {
            "before_report": str(before_report),
            "rewrite_brief": str(brief_path),
        },
        "next_step": "Use rewrite-brief.md with an agent, write the revised draft locally, then run rewrite check.",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "status": "prepared",
        "workspace": str(output_dir),
        "manifest": str(manifest_path),
        "before_report": str(before_report),
        "rewrite_brief": str(brief_path),
        "before_distance": before["style_distance"]["distance"],
        "before_ai_tell_risk_count": len(before["ai_tell_risks"]),
    }


def check_rewrite(
    profile_pack: Path,
    original_path: Path,
    rewritten_path: Path,
    output_path: Path,
    route: str,
) -> dict[str, Any]:
    original_text = Path(original_path).read_text(encoding="utf-8")
    rewritten_text = Path(rewritten_path).read_text(encoding="utf-8")
    before = evaluate_draft(Path(profile_pack), original_text, route)
    after = evaluate_draft(Path(profile_pack), rewritten_text, route)
    before_distance = before["style_distance"]["distance"]
    after_distance = after["style_distance"]["distance"]
    before_risks = len(before["ai_tell_risks"])
    after_risks = len(after["ai_tell_risks"])
    payload = {
        "status": "ok",
        "route": route,
        "original": str(original_path),
        "rewritten": str(rewritten_path),
        "before_distance": before_distance,
        "after_distance": after_distance,
        "distance_delta": round(before_distance - after_distance, 3),
        "before_ai_tell_risk_count": before_risks,
        "after_ai_tell_risk_count": after_risks,
        "distance_improved": after_distance < before_distance,
        "risk_count_not_increased": after_risks <= before_risks,
    }
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_rewrite_check_report(payload), encoding="utf-8")
    payload["output"] = str(output_path)
    return payload


def build_rewrite_check_report(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Rewrite Check Report",
            "",
            f"- Route: {payload['route']}",
            f"- Original: `{payload['original']}`",
            f"- Rewritten: `{payload['rewritten']}`",
            f"- Before distance: {payload['before_distance']}",
            f"- After distance: {payload['after_distance']}",
            f"- Distance delta: {payload['distance_delta']}",
            f"- Distance improved: {str(payload['distance_improved']).lower()}",
            f"- Before AI-tell risks: {payload['before_ai_tell_risk_count']}",
            f"- After AI-tell risks: {payload['after_ai_tell_risk_count']}",
            f"- Risk count not increased: {str(payload['risk_count_not_increased']).lower()}",
            "",
            "## Boundary",
            "",
            "- This report checks deterministic local style signals.",
            "- It does not guarantee AI detector results or perfect author imitation.",
            "",
        ]
    )
