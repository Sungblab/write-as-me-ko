# AGENTS.md

This repository builds a Korean-first local author context skill.

## Product Direction

- Keep the project local-first.
- Treat user samples as sensitive by default.
- Focus on Korean writing output: reports, essays, blog posts, messages, and project documents.
- Position the project as inspired by `epoko77-ai/im-not-ai`, but not as a fork or detector-bypass tool.
- The core promise is reusable author context, not perfect voice cloning.

## Writing Rules

- Write public docs in clear Korean or concise English depending on the existing file.
- Do not make unsupported claims about AI detector bypass, privacy, accuracy, or model compatibility.
- Keep README copy product-like, not a progress report.
- Separate implemented behavior from planned behavior.

## Engineering Rules

- Keep the skill `SKILL.md` lean.
- Put detailed Korean writing rules under `references/`.
- Do not store private user writing in git-tracked paths.
- Avoid symlink-dependent packaging until Windows behavior is explicitly handled.

## Finish Gate

- Use a branch and PR for any feature, evaluator, skill packaging, privacy-sensitive, or multi-file change.
- Before claiming completion, run `npm run docs:check` and record the exact result.
- Required review evidence is local Devflow review or another available independent reviewer. Do not depend on discontinued or consumer-only review services as a required gate.
- Direct commits to the default branch are only acceptable for tiny reversible typo, formatting, or note-only changes.
