# Architecture

`write-as-me-ko` is an agent-led local file workflow built around a Codex plugin,
a Codex skill, a Profile Pack v2 CLI, and a small set of standard-library Python
modules.

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

Profile Pack v2 adds a machine-readable path:

```text
samples/ or examples/profile-pack-samples/
      |
      v
write_as_me/profile_pack.py
      |
      +--> profile.json
      +--> sample-manifest.json
      +--> voice-profile.md
      +--> route-map.md
      +--> privacy-report.md
      +--> coverage-report.md
      +--> style_features / route_style_features
      |
      v
write_as_me/cli.py
      |
      +--> doctor / eval
      +--> portable AGENTS.md export
      +--> judge-readable demo report
      +--> style-distance report
      +--> rewrite brief
      +--> held-out evaluation workspace
      +--> rewrite loop/check reports
```

Raw samples are inputs only. They should not be copied into generated portable
context files.

## Main Components

### `plugins/write-as-me-ko/`

The plugin is the agent-facing workflow surface. It provides:

- `commands/init.md` for the init command shape.
- `commands/create-skill.md` for the writing skill factory command shape.
- `skills/init/SKILL.md` for the Python-plus-LLM setup workflow.
- `skills/create-skill/SKILL.md` for recurring writing situation skills.
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

### `write_as_me/profile_pack.py`

The Profile Pack v2 builder writes a portable, machine-readable pack for future
agent workflows. It includes hashes, route counts, confidence, coverage, and
privacy metadata, but does not export raw sample text. It also embeds
deterministic Korean style signals so future agent skills can use measurable
evidence rather than only LLM impressions.

### `write_as_me/style_signals.py`

The style signal analyzer extracts local, deterministic markers: sentence
length, Korean endings, connectors, first-person markers, stance markers, bullet
structure, English-character ratio, and character n-grams. These are aggregate
features only; raw sample text is not written to the profile pack.

### `write_as_me/privacy_scanner.py`

The privacy scanner detects common sensitive patterns in local samples: email
addresses, Korean mobile phone numbers, resident-id-like strings,
student-id-like strings, token-like strings, and URLs. Reports store only
finding kind, risk, source path, span, and a redacted representation.

### `write_as_me/demo_report.py`

The demo report builder writes a judge-readable Markdown report from profile
pack metadata. It summarizes style evidence, privacy risk, route coverage, and
how a profile-aware agent should differ from a generic agent without including
raw sample text.

### `write_as_me/style_distance.py`

The Stage 9 evaluator compares drafts against profile-pack style signals. It can
score one draft or compare held-out human, generic LLM, and profile-guided
variants for the same route. It also detects configured Korean AI-tell risks and
builds rewrite briefs for Codex or Claude Code. It reads raw draft inputs at
runtime, but reports only distances, risk labels, and instructions.

### `write_as_me/heldout.py`

The Stage 10 held-out workflow builds a local profile pack from training samples
only, records the excluded held-out sample as path/hash metadata, and compares
that held-out human baseline with generic and profile-guided drafts. It reads
the held-out text locally at compare time, but does not copy raw sample text into
the manifest or report.

### `write_as_me/rewrite_loop.py`

The rewrite loop prepares a before report, rewrite brief, and manifest for an
existing draft. After an agent writes a revised draft, the check step compares
before/after style-distance and AI-tell risk counts. The report is local style
evidence, not an AI detector result.

### `write_as_me/cli.py`

The CLI exposes `profile build`, `doctor`, `eval`, `export agents`,
`demo report`, `style-distance`, `heldout prepare`, `heldout compare`,
`rewrite brief`, `rewrite loop`, and `rewrite check`.
`doctor` validates the profile pack shape and raw-sample boundary. `eval` checks
whether the pack is strong enough for reuse. `export agents` writes a portable
`AGENTS.md` from the pack reports. `demo report` writes a contest-friendly
summary report. `style-distance` writes local distance/risk evidence, and
`rewrite brief` prepares an agent-readable revision brief for an existing draft.
The Stage 10 commands prepare held-out evaluation workspaces and verify whether
a rewrite moved closer to the profile.

### `scripts/init_writing_workspace.py`

The init helper creates the baseline profile, exports the writing `AGENTS.md`,
and writes `_workspace/writing-init/llm-review.md`. The review brief tells Codex
or Claude Code what to inspect and how to strengthen the profile without copying
private raw samples into tracked outputs.

### `scripts/create_writing_skill.py`

The skill factory script creates reusable `SKILL.md` files from a preset or a
custom writing situation. It handles deterministic name normalization,
templating, overwrite protection, and synthetic examples. The LLM still owns the
interpretation of user intent and sample-specific writing rules.

### `templates/writing-skill/SKILL.md`

The template is the common skeleton for generated writing skills. It keeps the
generated skills compatible with Codex and Claude Code's `SKILL.md` style.

### `examples/writing-skills/`

Examples show starter skills for thread posts, Facebook posts, LinkedIn posts,
Instagram stories, professor messages, and blog retrospectives. They are
synthetic examples, not copied third-party posts.

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
python -m write_as_me.cli profile build --samples examples\profile-pack-samples --output _workspace\profile-pack-demo --json
python -m write_as_me.cli doctor --profile-pack _workspace\profile-pack-demo --json
python -m write_as_me.cli eval --profile-pack _workspace\profile-pack-demo --json
python -m write_as_me.cli demo report --profile-pack _workspace\profile-pack-demo --output _workspace\profile-pack-demo\demo-report.md --json
python -m write_as_me.cli style-distance --profile-pack _workspace\profile-pack-demo --route blog --draft examples\profile-pack-samples\blog\post.md --output _workspace\profile-pack-demo\style-distance-report.md --json
python -m write_as_me.cli rewrite brief --profile-pack _workspace\profile-pack-demo --input examples\profile-pack-samples\blog\post.md --route blog --mode balanced --output _workspace\profile-pack-demo\rewrite-brief.md --json
python -m write_as_me.cli heldout prepare --samples examples\profile-pack-samples --output _workspace\stage10-heldout --route blog --json
python -m write_as_me.cli heldout compare --workspace _workspace\stage10-heldout --generic examples\stage10\generic.md --profile-guided examples\stage10\profile-guided.md --output _workspace\stage10-heldout\heldout-report.md --json
python -m write_as_me.cli rewrite loop --profile-pack _workspace\profile-pack-demo --input examples\stage10\rewrite-original.md --route blog --output-dir _workspace\stage10-rewrite --json
python -m write_as_me.cli rewrite check --profile-pack _workspace\profile-pack-demo --original examples\stage10\rewrite-original.md --rewritten examples\stage10\rewrite-revised.md --route blog --output _workspace\stage10-rewrite\rewrite-check.md --json
.\scripts\smoke_profile.ps1
python -m scripts.init_writing_workspace --samples samples --profile _workspace\voice-profile.init.md --agents _workspace\writing\AGENTS.md --repo-root .
python -m scripts.export_agent_context --output _workspace\writing\AGENTS.md
```
