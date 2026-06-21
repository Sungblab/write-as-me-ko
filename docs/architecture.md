# Architecture

`write-as-me-ko` is an agent-led local file workflow built around a Codex plugin,
a Codex skill, and a small set of standard-library Python scripts.

## Data Flow

```text
samples/
  blog/
  report/
  message/
  project/
  private/
      |
      v
scripts/build_voice_profile.py
      |
      v
scripts/init_writing_workspace.py
      |
      +--> _workspace/writing-init/llm-review.md
      |
      v
codex/skills/write-as-me-ko/references/voice-profile.md
      |
      +--> Codex/Claude Code performs LLM interpretation and profile review
      |
      v
scripts/export_agent_context.py
      |
      v
dist/writing/AGENTS.md
```

Raw samples are inputs only. They should not be copied into generated portable
context files.

## Main Components

### `plugins/write-as-me-ko/`

The plugin is the agent-facing workflow surface. It provides:

- `commands/init.md` for the init command shape.
- `skills/init/SKILL.md` for the Python-plus-LLM setup workflow.
- `skills/write/SKILL.md` for drafting from the generated profile.

The plugin follows the same local plugin shape as `devflow-native`: Codex and
Claude plugin manifests plus command and skill folders.

### `codex/skills/write-as-me-ko/SKILL.md`

The skill is the runtime entrypoint. It stays lean and tells the agent which
references to read:

- `voice-profile.md`
- `judgment-rules.md`
- `format-routes.md`
- `anti-ai-tells-ko.md`

The skill decides the route first, then applies voice and judgment guidance.

### `references/voice-profile.md`

The profile is generated from local samples, then reviewed by the user. It
contains confidence, sample route counts, quantitative signals, common phrases,
route-specific signals, privacy notes, and drafting guidance.

### `references/judgment-rules.md`

This file captures claim boundaries and reasoning style. It prevents unsupported
claims, fake personal experience, inflated certainty, and public-facing hype.

### `references/format-routes.md`

This file maps writing requests to report, blog, message, project document, or
fallback behavior. The format route has priority over surface voice.

### `references/anti-ai-tells-ko.md`

This is the final Korean naturalness pass. It borrows the useful part of the
`im-not-ai` inspiration without making detector-bypass claims.

### `scripts/build_voice_profile.py`

The profile builder scans `.md` and `.txt` files under `samples/`, ignores repo
guidance files, extracts conservative signals, and writes Markdown. It uses only
the Python standard library so the project remains easy to run on Windows.

### `scripts/init_writing_workspace.py`

The init helper creates the baseline profile, exports the writing `AGENTS.md`,
and writes `_workspace/writing-init/llm-review.md`. The review brief tells Codex
or Claude Code what to inspect and how to strengthen the profile without copying
private raw samples into tracked outputs.

### `scripts/export_agent_context.py`

The exporter combines the core references into a writing `AGENTS.md`. It should
include distilled profile and rule content, not source samples.

### `scripts/install_codex.ps1`

The installer copies the skill into `%USERPROFILE%\.codex\skills\write-as-me-ko`.
It avoids symlink-dependent packaging because Windows behavior is a known risk.

## Privacy Boundary

- `samples/private/` is for local-only writing samples.
- `samples/private/` and `*.local.md` stay gitignored.
- Generated context should summarize patterns, not reproduce private raw text.
- Users should review generated `voice-profile.md` before using it for school,
  applications, public posts, or sensitive messages.

## Verification

The baseline verification commands are:

```powershell
python -m unittest discover -s tests -v
.\scripts\smoke_profile.ps1
python -m scripts.init_writing_workspace --samples samples --profile _workspace\voice-profile.init.md --agents _workspace\writing\AGENTS.md --repo-root .
python -m scripts.export_agent_context --output _workspace\writing\AGENTS.md
```
