# Writing Skill Factory

The writing skill factory turns repeated writing situations into reusable
`SKILL.md` files.

The core idea:

```text
voice-profile.md
  + user-provided recurring writing rules
  + synthetic examples
  -> reusable writing skill
```

This keeps `write-as-me-ko` open-ended. It should not hard-code only Threads,
LinkedIn, Facebook, Instagram, professor messages, or blog posts. Those are
starter examples. The user can ask for any recurring writing situation.

## Workflow

1. Run the normal init workflow to build or review `voice-profile.md`.
2. Ask Codex or Claude Code to create a skill:

```text
쓰레드 글쓰기 스킬 만들어줘.
한 시리즈당 500자 이하, 보통 5개, 첫 글은 문제의식 중심,
너무 홍보문처럼 쓰지 말고 내 블로그 말투를 참고해.
```

3. The agent converts the request into:

- purpose
- audience
- hard constraints
- tone constraints
- synthetic examples
- checklist

4. The agent runs `scripts.create_writing_skill`.
5. The agent reviews the generated skill and verifies the repo.

## Presets

Presets are starter templates, not limits:

- `thread-post`
- `facebook-post`
- `linkedin-post`
- `instagram-story`
- `professor-message`
- `blog-retrospective`

List them with:

```powershell
python -m scripts.create_writing_skill --list-presets
```

Generate one with:

```powershell
python -m scripts.create_writing_skill --preset thread-post --output-root dist\writing-skills --force
```

Create a custom one with:

```powershell
python -m scripts.create_writing_skill `
  --name launch-thread `
  --purpose "Write Korean launch thread posts." `
  --audience "Korean builders and followers." `
  --constraint "Default to 5 posts." `
  --constraint "Keep every post under 500 Korean characters." `
  --tone "Start from the user's concrete problem." `
  --checklist "No generic marketing copy."
```

## Claude Code Notes

Claude Code supports skills as `SKILL.md` files. The official docs describe
skills as reusable instruction files that Claude can load when relevant or when
the user invokes a slash command. They also describe plugin skills under
`<plugin>/skills/<skill-name>/SKILL.md`, which matches this repo's plugin
layout. See:

- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code hooks](https://code.claude.com/docs/en/hooks)
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)

Claude Code custom commands now overlap with skills for slash-command style
workflows. For this project, prefer generated skills over separate command files
because skills can carry references, examples, and validation scripts.

## Safety Boundaries

- Do not claim official platform algorithm optimization.
- Do not copy real third-party posts into examples.
- Do not call external LLM APIs from Python for analysis. Codex or Claude Code
  performs LLM interpretation in the session.
- Keep private user writing out of git-tracked generated examples.
