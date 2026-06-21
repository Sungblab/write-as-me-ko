# Product Goal

`write-as-me-ko` is a Korean-first, local-first writing AGENTS.md workflow.

The project helps a user work with Codex or Claude Code to analyze their Korean
blog, portfolio, report, message, and project samples, then turn those findings
into a reusable writing profile, Codex skill, and writing `AGENTS.md`. It also
helps the user turn repeated writing situations into reusable writing skills.
The goal is not to make AI text bypass detectors or perfectly clone a person.
The goal is to stop repeating the same style and format instructions and make
future drafting start from a reviewed local writing setup.

## Final Development Goal

A complete version of `write-as-me-ko` should let the user:

1. Open the repo in Codex or Claude Code and request an init workflow.
2. Provide representative Korean samples under `samples/` or an explicit local
   sample path.
3. Let the agent run Python baseline analysis for reproducible signals.
4. Let the LLM interpret representative samples and strengthen the profile.
5. Review generated references before using them for sensitive writing.
6. Install the Codex skill or export a writing `AGENTS.md`.
7. Create reusable writing skills for recurring situations such as threads,
   social posts, professor messages, blog retrospectives, or any user-defined
   format.
8. Use that writing setup for Korean reports, essays, blog posts, messages, and
   project documents.
9. Keep private source samples out of git-tracked paths by default.

## Positioning

This project is inspired by `epoko77-ai/im-not-ai`, especially its Korean AI-tell
taxonomy and its fast-versus-strict workflow split. It is not a fork, a detector
bypass product, or a generic humanizer.

`im-not-ai` starts after a draft exists and asks, "How do we remove Korean AI
tells while preserving meaning?"

`write-as-me-ko` starts before the draft and asks, "What local writing setup
should Codex or Claude Code build so future drafts stay closer to the user's
style, judgment, and target format?"

## Product Principles

- Local-first: profile generation and export work from local files.
- Sensitive by default: samples may contain private writing and should not be
  committed accidentally.
- Korean-first: reports, essays, blog posts, messages, and project docs are the
  main target outputs.
- Agent-led setup: the user can ask Codex or Claude Code to run the init
  workflow instead of manually executing every script.
- Reviewable profile: generated profiles are drafts for the user to inspect,
  not hidden model state.
- Python plus LLM: deterministic scripts provide baseline evidence, and the LLM
  interprets supported writing habits.
- Skill factory: repeated writing rules should become reusable skills instead
  of being pasted into every chat.
- Format before surface voice: reports should remain reports, messages should
  remain messages, and blog voice should not flatten every output.

## Non-Goals

- No AI-detector bypass guarantee.
- No fake personal experience generation.
- No plagiarism or author impersonation.
- No claim that one profile fits every genre.
- No uploading private samples to a hosted service as a required workflow.
