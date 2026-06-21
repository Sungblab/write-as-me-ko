from __future__ import annotations

import argparse
from pathlib import Path

from scripts.build_voice_profile import build_profile_markdown
from scripts.export_agent_context import build_agent_context


DEFAULT_PROFILE = Path("codex/skills/write-as-me-ko/references/voice-profile.md")
DEFAULT_AGENTS = Path("dist/writing/AGENTS.md")
DEFAULT_BRIEF = Path("_workspace/writing-init/llm-review.md")


def build_llm_review_brief(samples: Path, profile: Path, agents_file: Path) -> str:
    return "\n".join(
        [
            "# LLM Review Brief",
            "",
            "Use this after the Python baseline profile is generated.",
            "",
            "## Goal",
            "",
            "Turn local Korean blog, portfolio, message, report, and project samples into a reviewable writing profile.",
            "",
            "## Inputs",
            "",
            f"- Samples directory: `{samples}`",
            f"- Python profile draft: `{profile}`",
            f"- Writing AGENTS output: `{agents_file}`",
            "",
            "## Agent Tasks",
            "",
            "1. Read the generated `voice-profile.md` before reading raw samples.",
            "2. Inspect representative local samples only when needed for interpretation.",
            "3. Do not copy private raw sample text into git-tracked files or exported AGENTS files.",
            "4. Strengthen `voice-profile.md` with observed writing habits, uncertainty, and route-specific guidance.",
            "5. Keep claims conservative when samples are thin or route coverage is missing.",
            "6. Re-export the writing AGENTS file after profile edits.",
            "7. Run `npm run docs:check` and report the exact result.",
            "",
            "## Review Questions",
            "",
            "- Which route has enough evidence: blog, report, message, project, or other?",
            "- What should the agent preserve when drafting new Korean text?",
            "- Which AI-like patterns should be avoided for this user's writing?",
            "- Which parts are assumptions because the sample set is still thin?",
            "",
        ]
    )


def init_writing_workspace(
    samples: Path,
    profile: Path,
    agents_file: Path,
    brief: Path,
    repo_root: Path = Path("."),
) -> list[Path]:
    profile.parent.mkdir(parents=True, exist_ok=True)
    profile.write_text(build_profile_markdown(samples), encoding="utf-8")

    agents_file.parent.mkdir(parents=True, exist_ok=True)
    agents_file.write_text(build_agent_context(repo_root), encoding="utf-8")

    brief.parent.mkdir(parents=True, exist_ok=True)
    brief.write_text(build_llm_review_brief(samples, profile, agents_file), encoding="utf-8")

    return [profile, agents_file, brief]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Initialize a Korean writing AGENTS workspace.")
    parser.add_argument("--samples", default="samples", help="Samples directory")
    parser.add_argument("--profile", default=str(DEFAULT_PROFILE), help="Voice profile output")
    parser.add_argument("--agents", default=str(DEFAULT_AGENTS), help="Writing AGENTS output")
    parser.add_argument("--brief", default=str(DEFAULT_BRIEF), help="LLM review brief output")
    parser.add_argument("--repo-root", default=".", help="Repository root for references")
    args = parser.parse_args(argv)

    written = init_writing_workspace(
        samples=Path(args.samples),
        profile=Path(args.profile),
        agents_file=Path(args.agents),
        brief=Path(args.brief),
        repo_root=Path(args.repo_root),
    )
    for path in written:
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
