---
name: write-as-me-ko
description: Korean-first writing profile skill. Use when the user asks to draft, rewrite, or polish Korean reports, essays, blog posts, portfolio copy, messages, README copy, PR text, or submission notes in their own style. Reads local voice, judgment, format, and Korean AI-tell references before writing. Not for translation, factual research, or inventing personal experiences.
---

# Write As Me KO

Draft or rewrite Korean text using the user's local writing profile. This skill is not a generic humanizer. It applies the user's visible writing habits, judgment rules, and genre-specific format preferences before producing the first draft.

## Load Order

Read only the references needed for the request:

1. `references/voice-profile.md` for the user's current voice profile.
2. `references/judgment-rules.md` for stance, reasoning, and claim boundaries.
3. `references/format-routes.md` for the target output type.
4. `references/anti-ai-tells-ko.md` for the final Korean AI-tell pass.

If `voice-profile.md` is still a placeholder or too thin, ask for 3-10 representative samples or proceed with a conservative Korean style pass instead of pretending to know the user's voice.

## Workflow

1. Identify the target output type: report, essay, blog/reflection, message, project document, or other.
2. Load the matching format route and the general voice/judgment rules.
3. Preserve all facts, names, dates, numbers, links, and quoted text from the user's input.
4. Draft in Korean unless the user explicitly asks otherwise.
5. Apply the genre route:
   - Reports and essays: prioritize clarity, evidence, structure, and restrained formal Korean.
   - Blog or reflection: allow more personal rhythm and judgment shifts.
   - Messages: match recipient distance and formality.
   - Project docs: keep concise, concrete, and implementation-grounded.
6. Run a final anti-AI-tell check against `anti-ai-tells-ko.md`.
7. Return the output plus a short note with the route used and any assumptions.

## Guardrails

- Do not invent personal experiences, emotions, achievements, relationships, grades, usage numbers, or praise.
- Do not make the user sound more certain than their source material supports.
- Do not flatten every output into blog voice. Formal deliverables should remain formal.
- Do not overuse bullets, mechanical transitions, summary endings, or English terms when natural Korean is available.
- If the source is already written in the user's voice, preserve it and make only necessary edits.

## Missing Context Behavior

When local references are empty:

- For drafting: produce a neutral, natural Korean draft and label it as "profile-light".
- For voice matching: ask for samples before claiming voice match.
- For sensitive submissions: keep claims conservative and explicitly mark assumptions.
