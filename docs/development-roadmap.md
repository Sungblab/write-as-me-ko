# Development Roadmap

This roadmap keeps `write-as-me-ko` focused on a small local workflow before any
hosted or UI expansion.

## Stage 1: Usable Local MVP

Status: implemented.

Scope:

- Codex skill under `codex/skills/write-as-me-ko/`.
- Local profile builder in `scripts/build_voice_profile.py`.
- Portable context exporter in `scripts/export_agent_context.py`.
- Windows-friendly Codex installer script.
- Unit tests and smoke script.

Acceptance:

- `python -m unittest discover -s tests -v` passes.
- `.\scripts\smoke_profile.ps1` creates local `_workspace` smoke outputs.
- README explains the workflow without promising detector bypass or perfect
  voice cloning.

## Stage 2: Reviewable Author Profile

Status: implemented.

Scope:

- Improve route-specific profile signals for blog, report, message, and project
  samples.
- Surface privacy notes when private sample paths are used.
- Keep generated output conservative when sample confidence is low.
- Preserve simple standard-library implementation.

Acceptance:

- Generated `voice-profile.md` includes route-specific signals.
- Private sample paths are called out as local-only material.
- Existing profile builder tests cover route guidance and privacy notes.

## Stage 3: Writing AGENTS.md Workflow

Status: implemented.

Scope:

- Keep Codex as the first-class install target.
- Export a writing `AGENTS.md` file for other agents.
- Include only distilled rules and profile references, never raw samples.
- Add a manifest-like summary of confidence, source routes, and generated files.
- Add an init helper that produces a Python baseline profile plus an LLM review
  brief for Codex or Claude Code.

Acceptance:

- Export command works from a clean checkout.
- Output is useful outside Codex without symlink-dependent references.
- Tests prove missing reference files degrade with explicit "Missing" sections.
- Init command writes profile, writing AGENTS output, and an LLM review brief.

## Stage 3.5: Plugin Init Surface

Status: implemented.

Scope:

- Add a local Codex plugin under `plugins/write-as-me-ko/`.
- Provide an `init` command and skill that describe the agent-led setup flow.
- Keep the workflow split into Python baseline analysis and LLM interpretation.

Acceptance:

- Plugin manifests exist under `plugins/write-as-me-ko/.codex-plugin/` and
  `plugins/write-as-me-ko/.claude-plugin/`.
- The local marketplace entry points to `./plugins/write-as-me-ko`.
- The init skill tells the agent to run `scripts.init_writing_workspace`, review
  samples conservatively, re-export `dist/writing/AGENTS.md`, and verify.

## Stage 4: Evaluation Loop

Status: implemented.

Scope:

- Add before/after examples under `eval/`.
- Define checks for fact preservation, genre preservation, Korean naturalness,
  and profile usage.
- Keep evaluation local and text-based.

Acceptance:

- `python -m scripts.run_eval` writes `_workspace/eval/evaluation-report.md`.
- Evaluation uses committed synthetic before/after cases and does not require
  private sample text to be committed.
- Failures point to concrete profile or rule gaps under
  `codex/skills/write-as-me-ko/references/`.

## Deferred Work

- Web UI.
- Hosted profile storage.
- Detector-style scoring claims.
- Multi-language expansion.
- Automatic voice cloning or personality simulation.
