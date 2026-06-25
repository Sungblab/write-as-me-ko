from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .demo_report import write_demo_report
from .profile_pack import build_profile_pack
from .style_distance import (
    build_rewrite_brief,
    build_style_distance_report,
    compare_variants,
    evaluate_draft,
)


REQUIRED_PACK_FILES = (
    "profile.json",
    "sample-manifest.json",
    "voice-profile.md",
    "route-map.md",
    "privacy-report.md",
    "coverage-report.md",
)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _missing_files(profile_pack: Path) -> list[str]:
    return [name for name in REQUIRED_PACK_FILES if not (profile_pack / name).exists()]


def _doctor_payload(profile_pack: Path) -> dict[str, Any]:
    missing = _missing_files(profile_pack)
    if missing:
        return {
            "status": "fail",
            "profile_pack": str(profile_pack),
            "missing": missing,
            "checks": [],
        }

    profile = _read_json(profile_pack / "profile.json")
    manifest = _read_json(profile_pack / "sample-manifest.json")
    checks = [
        {
            "id": "schema-version",
            "status": "pass" if profile.get("schema_version") == 2 else "fail",
        },
        {
            "id": "raw-samples-profile",
            "status": "pass" if profile.get("raw_samples_included") is False else "fail",
        },
        {
            "id": "raw-samples-manifest",
            "status": "pass" if manifest.get("raw_samples_included") is False else "fail",
        },
        {
            "id": "sample-count",
            "status": "pass" if profile.get("summary", {}).get("sample_count", 0) > 0 else "warn",
        },
    ]
    status = "pass" if all(check["status"] == "pass" for check in checks[:3]) else "fail"
    if status == "pass" and any(check["status"] == "warn" for check in checks):
        status = "warn"
    return {
        "status": status,
        "profile_pack": str(profile_pack),
        "checks": checks,
    }


def _eval_payload(profile_pack: Path) -> dict[str, Any]:
    doctor = _doctor_payload(profile_pack)
    if doctor["status"] == "fail":
        return {
            "status": "fail",
            "profile_pack": str(profile_pack),
            "doctor": doctor,
            "score": 0,
        }

    profile = _read_json(profile_pack / "profile.json")
    summary = profile.get("summary", {})
    confidence = summary.get("confidence", "none")
    route_count = len(profile.get("routes", {}))
    privacy = profile.get("privacy", {})
    style_features = profile.get("style_features", {})
    checks = [
        {
            "id": "confidence",
            "status": "pass" if confidence in {"medium", "high"} else "warn",
            "value": confidence,
        },
        {
            "id": "route-coverage",
            "status": "pass" if route_count >= 2 else "warn",
            "value": route_count,
        },
        {
            "id": "raw-samples",
            "status": "pass" if profile.get("raw_samples_included") is False else "fail",
        },
        {
            "id": "style-signals",
            "status": "pass" if len(style_features.get("signal_groups", [])) >= 3 else "warn",
            "value": style_features.get("signal_groups", []),
        },
        {
            "id": "privacy-scan",
            "status": "pass" if privacy.get("finding_count", 0) == 0 else "warn",
            "value": {
                "risk": privacy.get("risk", "none"),
                "finding_count": privacy.get("finding_count", 0),
            },
        },
    ]
    if any(check["status"] == "fail" for check in checks):
        status = "fail"
    elif any(check["status"] == "warn" for check in checks):
        status = "warn"
    else:
        status = "pass"
    score = sum(1 for check in checks if check["status"] == "pass")
    return {
        "status": status,
        "profile_pack": str(profile_pack),
        "score": score,
        "checks": checks,
    }


def _agents_context(profile_pack: Path) -> str:
    profile = _read_json(profile_pack / "profile.json")
    summary = profile["summary"]
    route_map = (profile_pack / "route-map.md").read_text(encoding="utf-8").strip()
    coverage = (profile_pack / "coverage-report.md").read_text(encoding="utf-8").strip()
    privacy = (profile_pack / "privacy-report.md").read_text(encoding="utf-8").strip()
    routes = ", ".join(profile.get("routes", {}).keys()) or "none"
    return "\n".join(
        [
            "# Writing AGENTS.md",
            "",
            "Use this generated file as a portable Korean author-context guide for AI agents.",
            "",
            "## Core Rules",
            "",
            "- Write in Korean unless the user explicitly asks otherwise.",
            "- Preserve facts, names, dates, numbers, links, and quoted text.",
            "- Do not invent personal experiences, emotions, achievements, metrics, praise, or relationships.",
            "- Match the target route before matching surface voice.",
            "- Treat this as context, not as permission to copy raw samples.",
            "",
            "## Profile Pack Manifest",
            "",
            f"- Confidence: {summary['confidence']}",
            f"- Source samples reviewed: {summary['sample_count']}",
            f"- Source routes: {routes}",
            "- Raw samples included: no",
            "",
            "---",
            "",
            route_map,
            "",
            "---",
            "",
            coverage,
            "",
            "---",
            "",
            privacy,
            "",
        ]
    )


def _handle_profile(args: argparse.Namespace) -> int:
    result = build_profile_pack(Path(args.samples), Path(args.output))
    payload = {
        "status": "built",
        "profile_pack": str(result.output_dir),
        "profile_path": str(result.profile_path),
        "manifest_path": str(result.manifest_path),
    }
    if args.json:
        _print_json(payload)
    else:
        print(f"wrote {result.output_dir}")
    return 0


def _handle_doctor(args: argparse.Namespace) -> int:
    payload = _doctor_payload(Path(args.profile_pack))
    if args.json:
        _print_json(payload)
    else:
        print(f"{payload['status']}: {payload['profile_pack']}")
    return 0 if payload["status"] in {"pass", "warn"} else 1


def _handle_eval(args: argparse.Namespace) -> int:
    payload = _eval_payload(Path(args.profile_pack))
    if args.json:
        _print_json(payload)
    else:
        print(f"{payload['status']}: score={payload['score']}")
    return 0 if payload["status"] in {"pass", "warn"} else 1


def _handle_export(args: argparse.Namespace) -> int:
    profile_pack = Path(args.profile_pack)
    doctor = _doctor_payload(profile_pack)
    if doctor["status"] == "fail":
        if args.json:
            _print_json(doctor)
        else:
            print(f"fail: {profile_pack}")
        return 1
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(_agents_context(profile_pack), encoding="utf-8")
    payload = {
        "status": "exported",
        "profile_pack": str(profile_pack),
        "output": str(output),
    }
    if args.json:
        _print_json(payload)
    else:
        print(f"wrote {output}")
    return 0


def _handle_demo_report(args: argparse.Namespace) -> int:
    output = write_demo_report(Path(args.profile_pack), Path(args.output))
    payload = {
        "status": "written",
        "profile_pack": str(args.profile_pack),
        "output": str(output),
    }
    if args.json:
        _print_json(payload)
    else:
        print(f"wrote {output}")
    return 0


def _handle_style_distance(args: argparse.Namespace) -> int:
    profile_pack = Path(args.profile_pack)
    if args.human and args.generic and args.profile_guided:
        payload = compare_variants(
            profile_pack,
            Path(args.human).read_text(encoding="utf-8"),
            Path(args.generic).read_text(encoding="utf-8"),
            Path(args.profile_guided).read_text(encoding="utf-8"),
            route=args.route,
        )
    elif args.draft:
        payload = evaluate_draft(
            profile_pack,
            Path(args.draft).read_text(encoding="utf-8"),
            route=args.route,
        )
    else:
        payload = {
            "status": "fail",
            "message": "Provide --draft or all of --human, --generic, and --profile-guided.",
        }
        if args.json:
            _print_json(payload)
        else:
            print(payload["message"])
        return 1

    payload["status"] = "ok"
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(build_style_distance_report(payload), encoding="utf-8")
        payload["output"] = str(output)
    if args.json:
        _print_json(payload)
    else:
        print(f"style-distance: {payload['status']}")
    return 0


def _handle_rewrite_brief(args: argparse.Namespace) -> int:
    brief = build_rewrite_brief(
        Path(args.profile_pack),
        Path(args.input),
        route=args.route,
        mode=args.mode,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(brief, encoding="utf-8")
    payload = {
        "status": "written",
        "profile_pack": str(args.profile_pack),
        "input": str(args.input),
        "output": str(output),
        "route": args.route,
        "mode": args.mode,
    }
    if args.json:
        _print_json(payload)
    else:
        print(f"wrote {output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Korean author-context profile packs.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    profile = subparsers.add_parser("profile", help="Profile pack commands")
    profile_subparsers = profile.add_subparsers(dest="profile_command", required=True)
    build = profile_subparsers.add_parser("build", help="Build a profile pack")
    build.add_argument("--samples", default="samples", help="Samples directory")
    build.add_argument("--output", default="dist/profile-pack", help="Profile pack output directory")
    build.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    build.set_defaults(func=_handle_profile)

    doctor = subparsers.add_parser("doctor", help="Validate a profile pack")
    doctor.add_argument("--profile-pack", default="dist/profile-pack", help="Profile pack directory")
    doctor.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    doctor.set_defaults(func=_handle_doctor)

    eval_parser = subparsers.add_parser("eval", help="Score a profile pack for safe reuse")
    eval_parser.add_argument("--profile-pack", default="dist/profile-pack", help="Profile pack directory")
    eval_parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    eval_parser.set_defaults(func=_handle_eval)

    export = subparsers.add_parser("export", help="Export profile pack context")
    export_subparsers = export.add_subparsers(dest="export_command", required=True)
    agents = export_subparsers.add_parser("agents", help="Export a portable AGENTS.md")
    agents.add_argument("--profile-pack", default="dist/profile-pack", help="Profile pack directory")
    agents.add_argument("--output", default="dist/writing/AGENTS.md", help="Output AGENTS.md path")
    agents.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    agents.set_defaults(func=_handle_export)

    demo = subparsers.add_parser("demo", help="Demo and contest report commands")
    demo_subparsers = demo.add_subparsers(dest="demo_command", required=True)
    report = demo_subparsers.add_parser("report", help="Write a judge-readable demo report")
    report.add_argument("--profile-pack", default="dist/profile-pack", help="Profile pack directory")
    report.add_argument("--output", default="dist/demo-report.md", help="Output report path")
    report.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    report.set_defaults(func=_handle_demo_report)

    style_distance = subparsers.add_parser("style-distance", help="Score draft style distance")
    style_distance.add_argument("--profile-pack", default="dist/profile-pack", help="Profile pack directory")
    style_distance.add_argument("--route", default=None, help="Route to compare against, such as blog or message")
    style_distance.add_argument("--draft", help="Single draft file to evaluate")
    style_distance.add_argument("--human", help="Held-out human baseline file")
    style_distance.add_argument("--generic", help="Generic LLM baseline file")
    style_distance.add_argument("--profile-guided", help="Profile-guided draft file")
    style_distance.add_argument("--output", help="Optional markdown report output path")
    style_distance.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    style_distance.set_defaults(func=_handle_style_distance)

    rewrite = subparsers.add_parser("rewrite", help="Rewrite workflow commands")
    rewrite_subparsers = rewrite.add_subparsers(dest="rewrite_command", required=True)
    brief = rewrite_subparsers.add_parser("brief", help="Write an agent rewrite brief")
    brief.add_argument("--profile-pack", default="dist/profile-pack", help="Profile pack directory")
    brief.add_argument("--input", required=True, help="Draft file to rewrite")
    brief.add_argument("--route", required=True, help="Target route, such as blog, report, message, or project")
    brief.add_argument(
        "--mode",
        choices=["minimal", "balanced", "strong"],
        default="balanced",
        help="Rewrite strength",
    )
    brief.add_argument("--output", required=True, help="Rewrite brief output path")
    brief.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    brief.set_defaults(func=_handle_rewrite_brief)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
