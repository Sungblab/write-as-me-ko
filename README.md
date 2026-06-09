# write-as-me-ko

Korean-first local author context pack for AI agents.

This project is inspired by [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai), especially its Korean AI-writing tell detection and rewriting approach. `im-not-ai` focuses on reducing AI tells after a draft already exists. `write-as-me-ko` starts one step earlier: it helps Korean users turn their own writing samples, judgment rules, and output formats into reusable local context so agents can draft closer to their actual voice from the beginning.

The goal is not to pretend AI text is human. The goal is to stop repeating the same tone instructions every session and make reports, essays, blog posts, messages, and project documents follow the user's real Korean writing habits more consistently.

## MVP

The first version is a Codex skill:

```text
codex/skills/write-as-me-ko/
  SKILL.md
  references/
    anti-ai-tells-ko.md
    format-routes.md
    judgment-rules.md
    voice-profile.md
```

Use it to:

- draft Korean reports, essays, blog posts, and messages in a user-specific style
- rewrite generic AI drafts using a local voice profile
- keep formal Korean formal, casual Korean casual, and technical writing precise
- avoid common Korean AI tells such as translationese, mechanical transitions, inflated claims, and over-structured endings

## Repository Layout

```text
samples/
  blog/       # user's blog or reflective writing samples
  report/     # reports, essays, assignment-style writing
  message/    # emails, team messages, professor-facing notes
eval/
  test-prompts.md
  before-after.md
codex/skills/write-as-me-ko/
```

Add real samples under `samples/`, then update `codex/skills/write-as-me-ko/references/voice-profile.md` with patterns that are actually visible in those samples.

## Non-goals

- No fake personal experience generation
- No plagiarism or author impersonation
- No AI-detector bypass guarantee
- No promise that one profile fits every genre

