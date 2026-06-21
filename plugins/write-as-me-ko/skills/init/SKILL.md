---
name: init
description: Initialize a Korean writing AGENTS.md by analyzing local blog, portfolio, report, message, or project samples with Python plus LLM interpretation.
---

# Write As Me KO Init

Use this skill when the user wants Codex or Claude Code to analyze their Korean
writing samples and build the writing setup for future drafting. The user should
not need to manually run each script.

## Product Shape

This is an agent-led local workflow:

1. The maintainer provides a repo, folder, or local writing samples.
2. The agent runs deterministic Python analysis for counts, routes, sentence
   length, repeated phrases, privacy notes, and baseline route signals.
3. The agent reads representative samples and interprets writing habits with
   the LLM.
4. The agent updates `voice-profile.md` conservatively.
5. The agent exports a writing `AGENTS.md` for reuse.
6. The agent verifies the setup.

This is not model fine-tuning and not an AI-detector bypass workflow.

## Steps

1. Read `README.md`, `docs/product-goal.md`, and `docs/architecture.md`.
2. Locate samples:
   - Prefer an explicit path from the user.
   - Otherwise use `samples/`.
   - Treat `samples/private/` and `*.local.md` as sensitive local inputs.
3. Run:

```powershell
python -m scripts.init_writing_workspace --samples samples --repo-root .
```

4. Read `_workspace/writing-init/llm-review.md`.
5. Inspect 3-10 representative samples when available. Do not copy private raw
   sample text into git-tracked docs or exported AGENTS files.
6. Edit `codex/skills/write-as-me-ko/references/voice-profile.md`:
   - Keep the Python quantitative signals.
   - Add LLM-observed writing habits only when supported by samples.
   - Mark thin or missing routes explicitly.
   - Preserve uncertainty instead of pretending to know the user's voice.
7. Re-export:

```powershell
python -m scripts.export_agent_context --output dist/writing/AGENTS.md
```

8. Verify:

```powershell
npm run docs:check
```

## Output

Report:

- sample source used
- files generated or updated
- what Python measured
- what the LLM interpreted
- confidence and missing sample routes
- verification result

## Guardrails

- Do not commit private user writing.
- Do not claim perfect voice cloning.
- Do not claim AI detector bypass.
- Do not invent personal experiences, achievements, relationships, or metrics.
- If samples are too thin, produce a conservative writing profile and say so.
