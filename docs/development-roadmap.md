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

## Stage 5: Writing Skill Factory

Status: implemented.

Scope:

- Add `scripts/create_writing_skill.py`.
- Add `templates/writing-skill/SKILL.md`.
- Add `plugins/write-as-me-ko/skills/create-skill/SKILL.md`.
- Add `plugins/write-as-me-ko/commands/create-skill.md`.
- Include synthetic starter examples for thread, Facebook, LinkedIn, Instagram
  story, professor message, and blog retrospective writing.
- Keep the system open-ended so users can create skills for any recurring
  writing situation.

Acceptance:

- Presets generate valid `SKILL.md` files.
- Custom skills can be generated without overwriting existing files unless
  `--force` is passed.
- Generated examples do not copy third-party posts or claim official platform
  algorithm optimization.
- `npm run docs:check` covers the factory script.

## Stage 6: Profile Pack v2 CLI

Status: implemented.

Scope:

- Add `write_as_me/profile_pack.py`.
- Add `write_as_me/cli.py`.
- Add `pyproject.toml` with a `write-as-me` console script.
- Generate `profile.json`, `sample-manifest.json`, `voice-profile.md`,
  `route-map.md`, `privacy-report.md`, and `coverage-report.md`.
- Add `doctor`, `eval`, and `export agents` commands.
- Add synthetic demo samples under `examples/profile-pack-samples/`.

Acceptance:

- Unit tests cover profile pack generation, raw-sample exclusion, CLI workflow,
  and packaging metadata.
- `npm run docs:check` runs the profile pack demo build, doctor, eval, and
  export workflow.
- The exported portable `AGENTS.md` includes profile metadata and reports but
  not raw sample text.

## Stage 7: Korean Style Signals

Status: implemented.

Scope:

- Add `write_as_me/style_signals.py`.
- Extract deterministic Korean style signals: sentence length, endings,
  connectors, first-person markers, stance markers, bullet structure,
  English-character ratio, and character n-grams.
- Embed aggregate `style_features` and route-level `route_style_features` in
  `profile.json`.
- Surface style signal coverage in `coverage-report.md`.
- Add a research grounding document explaining the deterministic-first design.

Acceptance:

- Tests cover the style signal analyzer.
- Tests prove profile packs include style features without raw sample text.
- `npm run docs:check` covers the updated profile pack behavior.

## Deferred Work

- Web UI.
- Hosted profile storage.
- Detector-style scoring claims.
- Multi-language expansion.
- Automatic voice cloning or personality simulation.
- PII pattern scanner for phone numbers, email addresses, student ids, and
  token-like strings.
