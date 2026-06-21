---
name: write
description: Draft or rewrite Korean reports, blog posts, portfolio copy, messages, and project documents using the generated writing profile.
---

# Write As Me KO Write

Use this skill after the init workflow has produced or reviewed
`codex/skills/write-as-me-ko/references/voice-profile.md`.

## Load Order

1. `codex/skills/write-as-me-ko/references/voice-profile.md`
2. `codex/skills/write-as-me-ko/references/judgment-rules.md`
3. `codex/skills/write-as-me-ko/references/format-routes.md`
4. `codex/skills/write-as-me-ko/references/anti-ai-tells-ko.md`

## Workflow

1. Identify the requested output route: blog, report, message, project document,
   portfolio copy, or other.
2. Preserve all facts, names, dates, numbers, links, and quoted text from the
   user's source.
3. Apply the route before surface voice.
4. Use the profile only as far as the sample confidence supports.
5. Run a final Korean AI-tell pass.
6. Return the drafted text and a short note naming the route and assumptions.

## Guardrails

- Do not invent experiences or achievements.
- Do not flatten every output into blog tone.
- Do not over-polish into generic marketing copy.
- If the profile is empty or thin, say that the result is profile-light.
