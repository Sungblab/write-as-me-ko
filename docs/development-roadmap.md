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

Status: current active development stage.

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

## Stage 3: Portable Agent Context Pack

Scope:

- Keep Codex as the first-class install target.
- Export a single `AGENTS.write-as-me-ko.md` file for other agents.
- Include only distilled rules and profile references, never raw samples.
- Add a manifest-like summary of confidence, source routes, and generated files.

Acceptance:

- Export command works from a clean checkout.
- Output is useful outside Codex without symlink-dependent references.
- Tests prove missing reference files degrade with explicit "Missing" sections.

## Stage 4: Evaluation Loop

Scope:

- Add before/after examples under `eval/`.
- Define checks for fact preservation, genre preservation, Korean naturalness,
  and profile usage.
- Keep evaluation local and text-based.

Acceptance:

- A maintainer can run one command and inspect generated evaluation artifacts.
- Evaluation does not require private sample text to be committed.
- Failures point to concrete profile or rule gaps.

## Deferred Work

- Web UI.
- Hosted profile storage.
- Detector-style scoring claims.
- Multi-language expansion.
- Automatic voice cloning or personality simulation.
