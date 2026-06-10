# Architecture

`write-as-me-ko` is a local file workflow built around a Codex skill and a small
set of standard-library Python scripts.

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
codex/skills/write-as-me-ko/references/voice-profile.md
      |
      +--> Codex skill reads references during writing
      |
      v
scripts/export_agent_context.py
      |
      v
dist/AGENTS.write-as-me-ko.md
```

Raw samples are inputs only. They should not be copied into generated portable
context files.

## Main Components

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

### `scripts/export_agent_context.py`

The exporter combines the core references into a portable agent context file.
It should include distilled profile and rule content, not source samples.

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
python -m scripts.export_agent_context --output _workspace\AGENTS.write-as-me-ko.smoke.md
```
