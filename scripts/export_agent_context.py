from __future__ import annotations

import argparse
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


def build_agent_context(repo_root: Path) -> str:
    sections = [read_reference(repo_root, name) for name in REFERENCE_FILES]
    body = "\n\n---\n\n".join(sections)
    return "\n".join(
        [
            "# AGENTS.write-as-me-ko",
            "",
            "Use this file as a portable Korean author context for AI agents.",
            "",
            "## Core Rules",
            "",
            "- Write in Korean unless the user explicitly asks otherwise.",
            "- Preserve facts, names, dates, numbers, links, and quoted text.",
            "- Do not invent personal experiences, emotions, achievements, metrics, praise, or relationships.",
            "- Match the target format before matching surface voice.",
            "- If the profile is thin, say so and use conservative natural Korean.",
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
    parser.add_argument("--output", default="dist/AGENTS.write-as-me-ko.md", help="Output file")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_agent_context(repo_root), encoding="utf-8")
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

