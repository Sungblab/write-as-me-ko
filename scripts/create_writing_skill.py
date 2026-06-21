from __future__ import annotations

import argparse
import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path


DEFAULT_OUTPUT_ROOT = Path("dist/writing-skills")
TEMPLATE_PATH = Path("templates/writing-skill/SKILL.md")


@dataclass(frozen=True)
class WritingSkillSpec:
    name: str
    description: str
    purpose: str
    audience: str
    constraints: tuple[str, ...] = field(default_factory=tuple)
    tone: tuple[str, ...] = field(default_factory=tuple)
    checklist: tuple[str, ...] = field(default_factory=tuple)
    examples: tuple[str, ...] = field(default_factory=tuple)


PRESETS: dict[str, WritingSkillSpec] = {
    "thread-post": WritingSkillSpec(
        name="thread-post",
        description="Draft Korean social thread posts. Use when the user asks for Threads/X-style serial posts, launch threads, or follow-up posts with per-post length limits.",
        purpose="Turn one idea into a short Korean thread that reads like the user's own launch or reflection post.",
        audience="Korean readers who follow the user's projects, blog, or AI/dev experiments.",
        constraints=(
            "Write in Korean unless the user asks otherwise.",
            "Default to about 5 posts.",
            "Keep each post under 500 Korean characters.",
            "Let the first post be the longest if it carries the problem setup.",
            "Use line breaks for mobile reading rhythm.",
            "Do not make the thread sound like generic marketing copy.",
        ),
        tone=(
            "Start from a concrete discomfort, question, or realization.",
            "Prefer plain first-person reasoning over hype.",
            "Use the user's blog/profile voice when a voice profile is available.",
        ),
        checklist=(
            "Every post is under 500 Korean characters.",
            "The first post explains why this exists.",
            "The middle posts explain what changed or how it works.",
            "The last post can include a link, caveat, or next step.",
        ),
        examples=(
            "Input: 새 글쓰기 도구 출시\nOutput: 문제의식 -> AGENTS.md 비유 -> 만든 것 -> 사용 흐름 -> 링크",
        ),
    ),
    "facebook-post": WritingSkillSpec(
        name="facebook-post",
        description="Draft Korean Facebook-style posts. Use when the user wants a personal, slightly longer public post for friends, communities, or project updates.",
        purpose="Write a standalone Korean post that mixes context, personal reasoning, and a clear update without becoming a press release.",
        audience="Friends, builders, classmates, and community readers.",
        constraints=(
            "Prefer paragraphs over numbered lists.",
            "Open with a concrete situation or reflection.",
            "Keep links near the end unless the user asks for a link-first post.",
            "Avoid exaggerated claims about popularity, algorithms, or guaranteed outcomes.",
        ),
        tone=(
            "Use natural Korean with first-person reflection.",
            "Allow a little context before the point.",
            "Keep the ending grounded and specific.",
        ),
        checklist=(
            "The post has one clear reason for existing.",
            "The update is understandable without prior context.",
            "No copied third-party phrasing appears.",
        ),
    ),
    "linkedin-post": WritingSkillSpec(
        name="linkedin-post",
        description="Draft Korean or English LinkedIn-style professional posts. Use for project updates, lessons learned, launches, and career-facing reflections.",
        purpose="Turn a project or lesson into a professional post that is concrete, not performative.",
        audience="Professional peers, recruiters, founders, engineers, and collaborators.",
        constraints=(
            "Lead with the concrete project, result, or lesson.",
            "Avoid algorithm optimization claims.",
            "Use bullets only when they improve scanability.",
            "End with a specific takeaway, question, or link.",
        ),
        tone=(
            "Professional but not corporate.",
            "Evidence-backed and modest.",
            "Prefer what changed, what was learned, and what is next.",
        ),
        checklist=(
            "The post does not overstate impact.",
            "Any metric or claim is provided by the user.",
            "The CTA is natural and not engagement bait.",
        ),
    ),
    "instagram-story": WritingSkillSpec(
        name="instagram-story",
        description="Draft short Korean Instagram Story text. Use for casual story captions, launch snippets, progress notes, or screenshot overlays.",
        purpose="Create compact Korean story copy that fits visual or screenshot-based posts.",
        audience="Casual followers who may only glance at the story.",
        constraints=(
            "Keep each story frame short.",
            "Use 1-2 lines per frame by default.",
            "Prefer concrete captions over long explanations.",
            "Do not overuse emoji unless the user asks.",
        ),
        tone=(
            "Casual and direct.",
            "Slightly personal, not polished like an ad.",
            "Let screenshots or visuals carry details when present.",
        ),
        checklist=(
            "Each frame can be read quickly.",
            "No dense paragraphs.",
            "The sequence has a beginning, update, and small close.",
        ),
    ),
    "professor-message": WritingSkillSpec(
        name="professor-message",
        description="Draft Korean professor-facing messages. Use for emails, LMS notes, schedule requests, clarifications, and polite academic communication.",
        purpose="Write concise, respectful Korean messages to professors without overexplaining.",
        audience="Professors, instructors, TAs, and school staff.",
        constraints=(
            "Use polite Korean.",
            "State the reason and request clearly.",
            "Avoid excessive apologies or emotional framing.",
            "Include dates, course names, or attachments only when provided by the user.",
        ),
        tone=(
            "Respectful and concise.",
            "Practical rather than dramatic.",
            "Close with thanks and the requested next action when needed.",
        ),
        checklist=(
            "The request is visible in the first half.",
            "No unsupported excuse is invented.",
            "The message preserves all dates and names exactly.",
        ),
    ),
    "blog-retrospective": WritingSkillSpec(
        name="blog-retrospective",
        description="Draft Korean blog retrospective posts. Use when the user wants a personal blog post about a project, learning process, failure, or changed judgment.",
        purpose="Write a Korean blog post that starts from experience, follows the user's reasoning, and ends with a grounded lesson.",
        audience="Readers of the user's portfolio/blog and people interested in the project process.",
        constraints=(
            "Start from a real event, discomfort, or question.",
            "Do not flatten the post into a generic tech tutorial.",
            "Keep personal experience only where the user provided it.",
            "Use headings only when the post needs structure.",
        ),
        tone=(
            "Reflective, concrete, and Korean-first.",
            "Show how the user's judgment changed.",
            "Prefer specific process details over grand conclusions.",
        ),
        checklist=(
            "The post has a clear before/after in thinking.",
            "Technical details serve the story.",
            "The ending does not become an empty motivational slogan.",
        ),
    ),
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    if not slug:
        digest = hashlib.sha1(value.strip().encode("utf-8")).hexdigest()[:8]
        return f"writing-skill-{digest}"
    if len(slug) > 64:
        slug = slug[:64].rstrip("-")
    return slug


def bullet_lines(items: tuple[str, ...]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- Follow the user's request and the writing profile."


def examples_block(examples: tuple[str, ...]) -> str:
    if not examples:
        return "No fixed examples yet. Add synthetic examples after the first successful use."
    return "\n\n".join(f"```text\n{example}\n```" for example in examples)


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_skill(spec: WritingSkillSpec, template: str) -> str:
    skill_name = slugify(spec.name)
    return template.replace("{{skill_name_yaml}}", yaml_quote(skill_name)).replace(
        "{{description_yaml}}", yaml_quote(spec.description.strip())
    ).replace(
        "{{skill_title}}", spec.name.strip() or skill_name
    ).replace("{{purpose}}", spec.purpose.strip()).replace(
        "{{audience}}", spec.audience.strip()
    ).replace(
        "{{constraints}}", bullet_lines(spec.constraints)
    ).replace(
        "{{tone}}", bullet_lines(spec.tone)
    ).replace(
        "{{checklist}}", bullet_lines(spec.checklist)
    ).replace(
        "{{examples}}", examples_block(spec.examples)
    )


def create_skill(spec: WritingSkillSpec, output_root: Path, template_path: Path = TEMPLATE_PATH, force: bool = False) -> Path:
    template = template_path.read_text(encoding="utf-8")
    skill_name = slugify(spec.name)
    skill_dir = output_root / skill_name
    skill_path = skill_dir / "SKILL.md"
    if skill_path.exists() and not force:
        raise FileExistsError(f"{skill_path} already exists. Use --force to overwrite.")
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_path.write_text(render_skill(spec, template), encoding="utf-8")
    return skill_path


def spec_from_args(args: argparse.Namespace) -> WritingSkillSpec:
    if args.preset:
        preset = PRESETS[args.preset]
        return WritingSkillSpec(
            name=args.name or preset.name,
            description=args.description or preset.description,
            purpose=args.purpose or preset.purpose,
            audience=args.audience or preset.audience,
            constraints=tuple(args.constraint) or preset.constraints,
            tone=tuple(args.tone) or preset.tone,
            checklist=tuple(args.checklist) or preset.checklist,
            examples=tuple(args.example) or preset.examples,
        )
    if not args.name:
        raise ValueError("--name is required when --preset is not used.")
    return WritingSkillSpec(
        name=args.name,
        description=args.description or f"Draft Korean writing for {args.name}. Use when the user asks for this recurring writing situation.",
        purpose=args.purpose or "Create reusable writing guidance for a recurring user-defined situation.",
        audience=args.audience or "Audience specified by the user for this writing situation.",
        constraints=tuple(args.constraint),
        tone=tuple(args.tone),
        checklist=tuple(args.checklist),
        examples=tuple(args.example),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a reusable writing skill from user-provided constraints.")
    parser.add_argument("--preset", choices=sorted(PRESETS), help="Optional starter preset")
    parser.add_argument("--name", help="Skill name; normalized to hyphen-case")
    parser.add_argument("--description", help="Skill frontmatter description")
    parser.add_argument("--purpose", help="What the skill should accomplish")
    parser.add_argument("--audience", help="Who the writing is for")
    parser.add_argument("--constraint", action="append", default=[], help="Constraint line; can repeat")
    parser.add_argument("--tone", action="append", default=[], help="Tone line; can repeat")
    parser.add_argument("--checklist", action="append", default=[], help="Checklist line; can repeat")
    parser.add_argument("--example", action="append", default=[], help="Synthetic example; can repeat")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT), help="Directory where skill folders are written")
    parser.add_argument("--template", default=str(TEMPLATE_PATH), help="Skill template path")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing generated skill")
    parser.add_argument("--list-presets", action="store_true", help="Print available presets and exit")
    args = parser.parse_args(argv)

    if args.list_presets:
        for name in sorted(PRESETS):
            print(name)
        return 0

    path = create_skill(
        spec_from_args(args),
        output_root=Path(args.output_root),
        template_path=Path(args.template),
        force=args.force,
    )
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
