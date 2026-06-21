---
description: Analyze local Korean writing samples and initialize a writing AGENTS.md workflow.
argument-hint: "[sample path or writing goal]"
---

Use the Write As Me KO Init workflow.

If `$ARGUMENTS` names a sample path, inspect that path. Otherwise inspect the repo `samples/`
folder and ask only when no reasonable sample location is available.

Run the local baseline first:

```powershell
python -m scripts.init_writing_workspace --samples samples --repo-root .
```

Then read `_workspace/writing-init/llm-review.md`, inspect representative samples as needed,
strengthen `codex/skills/write-as-me-ko/references/voice-profile.md`, re-export the writing
AGENTS file, and run:

```powershell
npm run docs:check
```
