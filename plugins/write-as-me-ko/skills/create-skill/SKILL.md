---
name: create-skill
description: Create a reusable writing SKILL.md for any recurring writing situation such as Threads posts, Facebook posts, LinkedIn posts, Instagram stories, professor messages, blog retrospectives, launch posts, or any user-defined format. Use when the user says they keep repeating writing rules or wants a new tone/channel/workflow skill.
---

# Write As Me KO Create Skill

Create a writing skill from the user's repeated writing situation. Do not limit
the user to preset channels. Presets are starters, not product boundaries.

## Source References

- Claude Code supports skills as `SKILL.md` files and plugin skills under
  `<plugin>/skills/<skill-name>/SKILL.md`.
- Claude Code custom commands are now equivalent to skills for slash-command
  workflows, so generated skills should be usable as reusable commands.
- Codex skills also use `SKILL.md` with concise frontmatter and body guidance.

## Workflow

1. Read the user's requested writing situation and constraints.
2. Read `codex/skills/write-as-me-ko/references/voice-profile.md` when present.
3. If the request matches a preset, use it only as a starting point:
   - `thread-post`
   - `facebook-post`
   - `linkedin-post`
   - `instagram-story`
   - `professor-message`
   - `blog-retrospective`
4. If the user provides a custom situation, create a custom skill name.
5. Build the skill from:
   - purpose
   - audience
   - hard constraints
   - tone constraints
   - examples
   - checklist
6. Use `scripts/create_writing_skill.py` to generate the `SKILL.md`.
7. Review the generated skill:
   - no unsupported algorithm or growth claims
   - no copied third-party writing
   - constraints are concrete enough to reuse
   - examples are synthetic
8. Run `npm run docs:check`.

## Commands

List presets:

```powershell
python -m scripts.create_writing_skill --list-presets
```

Generate from a preset:

```powershell
python -m scripts.create_writing_skill --preset thread-post --output-root dist\writing-skills --force
```

Generate a custom skill:

```powershell
python -m scripts.create_writing_skill --name my-writing-situation --purpose "..." --audience "..." --constraint "..." --tone "..." --checklist "..." --output-root dist\writing-skills
```

To make a generated skill part of this plugin, write it under
`plugins/write-as-me-ko/skills/`. To keep it local to one project or user, write
it under the target `.claude/skills/`, `.codex/skills/`, or a private workspace
path according to the user's environment.

## Guardrails

- Do not claim official algorithm optimization for any platform.
- Do not copy real third-party posts into examples.
- Do not call external LLM APIs from Python. Codex or Claude Code performs the
  LLM interpretation in the session.
- Preserve the user's newest explicit constraints over preset defaults.
