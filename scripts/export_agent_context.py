from __future__ import annotations

import argparse
import re
from pathlib import Path


REFERENCE_DIR = Path("codex/skills/write-as-me-ko/references")
REFERENCE_FILES = [
    "voice-profile.md",
    "judgment-rules.md",
    "format-routes.md",
    "anti-ai-tells-ko.md",
]


def read_reference(repo_root: Path, name: str) -> str:
    path = repo_root / REFERENCE_DIR / name
    if not path.exists():
        return f"# Missing: {name}\n\nThis reference file was not found.\n"
    return path.read_text(encoding="utf-8").strip()


def _extract_confidence(voice_profile: str) -> str:
    match = re.search(r"^- Confidence:\s*(.+)$", voice_profile, flags=re.MULTILINE)
    return match.group(1).strip() if match else "unknown"


def _extract_source_routes(voice_profile: str) -> list[str]:
    routes: list[str] = []
    for match in re.finditer(r"^- ([a-z]+):\s*([1-9][0-9]*)$", voice_profile, flags=re.MULTILINE):
        route = match.group(1)
        if route != "none":
            routes.append(route)
    return routes


def build_manifest(voice_profile: str) -> str:
    routes = _extract_source_routes(voice_profile)
    source_routes = ", ".join(routes) if routes else "none"
    included = ", ".join(REFERENCE_FILES)
    return "\n".join(
        [
            "## Context Manifest",
            "",
            f"- Confidence: {_extract_confidence(voice_profile)}",
            f"- Source routes: {source_routes}",
            f"- Included references: {included}",
            "- Generated file: writing/AGENTS.md",
            "- Raw samples included: no",
        ]
    )


def build_agent_context(repo_root: Path) -> str:
    references = {name: read_reference(repo_root, name) for name in REFERENCE_FILES}
    sections = [references[name] for name in REFERENCE_FILES]
    body = "\n\n---\n\n".join(sections)
    return "\n".join(
        [
            "# Writing AGENTS.md",
            "",
            "Use this file as a portable Korean writing guide for AI agents.",
            "",
            "## Core Rules",
            "",
            "- Write in Korean unless the user explicitly asks otherwise.",
            "- Preserve facts, names, dates, numbers, links, and quoted text.",
            "- Do not invent personal experiences, emotions, achievements, metrics, praise, or relationships.",
            "- Match the target format before matching surface voice.",
            "- If the profile is thin, say so and use conservative natural Korean.",
            "",
            build_manifest(references["voice-profile.md"]),
            "",
            "---",
            "",
            body,
            "",
        ]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export a portable AGENTS context file.")
    parser.add_argument("--repo-root", default=".", help="Repository root")
    parser.add_argument("--output", default="dist/writing/AGENTS.md", help="Output file")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_agent_context(repo_root), encoding="utf-8")
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
