from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .profile_pack import PackSample, build_profile_pack_from_samples, collect_pack_samples
from .style_distance import build_style_distance_report, compare_variants


def _sample_entry(sample: PackSample, role: str) -> dict[str, Any]:
    return {
        "path": sample.relative_path,
        "route": sample.route,
        "sha256": sample.sha256,
        "chars": len(sample.text),
        "role": role,
    }


def _select_heldout(samples: list[PackSample], route: str | None, holdout_count: int) -> list[PackSample]:
    candidates = [sample for sample in samples if route is None or sample.route == route]
    if not candidates:
        return []
    return candidates[-max(holdout_count, 1) :]


def prepare_heldout_workspace(
    samples_root: Path,
    output_dir: Path,
    route: str | None = None,
    holdout_count: int = 1,
) -> dict[str, Any]:
    samples_root = Path(samples_root)
    output_dir = Path(output_dir)
    profile_pack = output_dir / "profile-pack"
    output_dir.mkdir(parents=True, exist_ok=True)

    samples = collect_pack_samples(samples_root)
    heldout = _select_heldout(samples, route, holdout_count)
    heldout_paths = {sample.relative_path for sample in heldout}
    training = [sample for sample in samples if sample.relative_path not in heldout_paths]
    build_profile_pack_from_samples(training, profile_pack)

    manifest = {
        "schema_version": 1,
        "raw_samples_included": False,
        "samples_root": str(samples_root),
        "profile_pack": str(profile_pack),
        "route": route or "any",
        "sample_count": len(samples),
        "training_count": len(training),
        "heldout_count": len(heldout),
        "training_samples": [_sample_entry(sample, "training") for sample in training],
        "heldout_samples": [_sample_entry(sample, "heldout") for sample in heldout],
        "notes": [
            "Held-out sample text is not copied into this manifest.",
            "Build profile-guided and generic drafts outside this file, then run heldout compare.",
        ],
    }
    manifest_path = output_dir / "heldout-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "status": "prepared" if heldout and training else "warn",
        "workspace": str(output_dir),
        "manifest": str(manifest_path),
        "profile_pack": str(profile_pack),
        "training_count": len(training),
        "heldout_count": len(heldout),
        "warnings": _workspace_warnings(samples, training, heldout),
    }


def _workspace_warnings(
    samples: list[PackSample],
    training: list[PackSample],
    heldout: list[PackSample],
) -> list[str]:
    warnings: list[str] = []
    if not samples:
        warnings.append("No Korean samples were found.")
    if not heldout:
        warnings.append("No held-out sample could be selected.")
    if not training:
        warnings.append("No training samples remain after the held-out split.")
    if len(training) < 2:
        warnings.append("Training profile confidence may be low with fewer than two samples.")
    return warnings


def _read_manifest(workspace: Path) -> dict[str, Any]:
    return json.loads((Path(workspace) / "heldout-manifest.json").read_text(encoding="utf-8"))


def compare_heldout_workspace(
    workspace: Path,
    generic_path: Path,
    profile_guided_path: Path,
    output_path: Path | None = None,
    route: str | None = None,
) -> dict[str, Any]:
    workspace = Path(workspace)
    manifest = _read_manifest(workspace)
    heldout_samples = manifest.get("heldout_samples", [])
    if not heldout_samples:
        return {
            "status": "fail",
            "message": "No held-out sample is recorded in heldout-manifest.json.",
            "workspace": str(workspace),
        }

    samples_root = Path(manifest["samples_root"])
    human_path = samples_root / heldout_samples[0]["path"]
    profile_pack = Path(manifest["profile_pack"])
    result = compare_variants(
        profile_pack,
        human_path.read_text(encoding="utf-8"),
        Path(generic_path).read_text(encoding="utf-8"),
        Path(profile_guided_path).read_text(encoding="utf-8"),
        route=route or heldout_samples[0].get("route"),
    )
    result["status"] = "ok"
    result["heldout"] = {
        "path": heldout_samples[0]["path"],
        "route": heldout_samples[0].get("route", "other"),
        "sha256": heldout_samples[0]["sha256"],
        "raw_text_included": False,
    }
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(build_heldout_report(result), encoding="utf-8")
        result["output"] = str(output_path)
    return result


def build_heldout_report(result: dict[str, Any]) -> str:
    lines = [
        "# Held-Out Style Evaluation",
        "",
        f"- Route: {result['route']}",
        f"- Held-out path: `{result['heldout']['path']}`",
        f"- Held-out raw text included: {str(result['heldout']['raw_text_included']).lower()}",
        f"- Profile-guided closer than generic: {str(result['profile_guided_closer_than_generic']).lower()}",
        f"- Distance delta: {result['distance_delta']}",
        "",
        "## Style-Distance Summary",
        "",
        build_style_distance_report(result).strip(),
        "",
        "## Boundary",
        "",
        "- This is local style evidence, not an AI-detector bypass claim.",
        "- External detector scores, if any, should be recorded separately as optional smoke-test notes.",
        "",
    ]
    return "\n".join(lines)
