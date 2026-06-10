# Product Goal

`write-as-me-ko` is a Korean-first, local-first author context pack generator.

The project helps a user turn their own Korean writing samples, judgment rules,
and format preferences into reusable context for AI agents. The goal is not to
make AI text bypass detectors or perfectly clone a person. The goal is to stop
repeating the same style instructions and let agents write closer to the user's
actual Korean habits from the first draft.

## Final Development Goal

A complete version of `write-as-me-ko` should let the user:

1. Put representative Korean samples under `samples/`.
2. Build a reviewable author profile from those local samples.
3. Edit the generated references before using them for sensitive writing.
4. Install the Codex skill or export a portable agent context file.
5. Use that context for Korean reports, essays, blog posts, messages, and
   project documents.
6. Keep private source samples out of git-tracked paths by default.

## Positioning

This project is inspired by `epoko77-ai/im-not-ai`, especially its Korean AI-tell
taxonomy and its fast-versus-strict workflow split. It is not a fork, a detector
bypass product, or a generic humanizer.

`im-not-ai` starts after a draft exists and asks, "How do we remove Korean AI
tells while preserving meaning?"

`write-as-me-ko` starts before the draft and asks, "What local author context
should an agent use so the first draft is already closer to the user's style,
judgment, and target format?"

## Product Principles

- Local-first: profile generation and export work from local files.
- Sensitive by default: samples may contain private writing and should not be
  committed accidentally.
- Korean-first: reports, essays, blog posts, messages, and project docs are the
  main target outputs.
- Reviewable context: generated profiles are drafts for the user to inspect,
  not hidden model state.
- Format before surface voice: reports should remain reports, messages should
  remain messages, and blog voice should not flatten every output.

## Non-Goals

- No AI-detector bypass guarantee.
- No fake personal experience generation.
- No plagiarism or author impersonation.
- No claim that one profile fits every genre.
- No uploading private samples to a hosted service as a required workflow.
