# AI-Tell Smoke Test

This note records a small Copykiller/GPT Killer smoke test run on 2026-06-25.
It is evidence for product direction, not a detector-bypass claim.

## Boundary

- External tool: `https://kookmin.copykiller.com/`
- Document type: blog
- Enabled checks: plagiarism check and AI-generation check
- Raw user sample text is not stored in this git-tracked note.
- The local working copy used temporary files under `_workspace/copykiller-test/`.
- The external score is treated as coarse, non-authoritative evidence.

## Test Inputs

| Variant | Source | Purpose |
|---|---|---|
| A Human excerpt | Held-out excerpt from a real public user blog post | Baseline for actual user prose |
| B Generic LLM-style draft | One-pass polished summary draft | Baseline for generic AI prose |
| C Seeded draft | One-pass draft lightly guided by the user blog tone | Baseline for shallow "write like me" prompting |

The held-out human excerpt came from a public blog file outside this repository:
`sungblab-nextjs/content/blog/나의 프로그래밍 일대기.mdx`.

## Results

| Variant | Plagiarism rate | AI writing rate | Result |
|---|---:|---:|---|
| A Human excerpt | 0% | 0% | Actual user prose was not flagged in this smoke test. |
| B Generic LLM-style draft | 0% | 100% | Generic polished AI draft was fully flagged. |
| C Seeded draft | 0% | 100% | A shallow profile-guided draft was still fully flagged. |

## Interpretation

The result supports the core `write-as-me-ko` direction: real user prose can
look measurably different from generic generated prose. It also raises the bar:
a one-pass "write like me" prompt is not enough.

The next useful feature should be a local AI-tell and style-distance loop:

1. Keep held-out human samples that are not used to build the profile.
2. Generate a generic baseline and a profile-guided draft for the same route.
3. Compare deterministic style signals before any external upload.
4. Ask the agent to revise specific risk points such as overly uniform sentence
   rhythm, generic transitions, flattened personal judgment, or missing lived
   uncertainty.
5. Optionally record external detector results as smoke-test evidence.

## Product Constraint

Do not describe this as AI detector bypass. The product promise remains reusable
author context and Korean writing quality control. External detector results can
help evaluate whether generated drafts still look mechanically AI-written, but
they do not prove authorship or guarantee non-detection.

## Implemented Local Workflow

Stage 9 implements local checks before any optional external smoke test.

Evaluate one draft against a profile pack:

```powershell
python -m write_as_me.cli style-distance `
  --profile-pack dist\profile-pack `
  --route blog `
  --draft draft.md `
  --output dist\style-distance-report.md `
  --json
```

Compare a held-out human baseline, a generic LLM draft, and a profile-guided
draft:

```powershell
python -m write_as_me.cli style-distance `
  --profile-pack dist\profile-pack `
  --route blog `
  --human heldout-human.md `
  --generic generic-llm.md `
  --profile-guided profile-guided.md `
  --output dist\style-distance-report.md `
  --json
```

Generate an agent rewrite brief for an existing draft:

```powershell
python -m write_as_me.cli rewrite brief `
  --profile-pack dist\profile-pack `
  --input draft.md `
  --route blog `
  --mode balanced `
  --output dist\rewrite-brief.md `
  --json
```

The rewrite brief is for Codex, Claude Code, or another writing agent. It
contains profile metadata, style-distance evidence, AI-tell risks, and rewrite
instructions, but it does not include raw profile samples.

Stage 10 adds the local loop that should run before any optional external smoke
test:

```powershell
python -m write_as_me.cli heldout prepare `
  --samples samples `
  --output dist\heldout-eval `
  --route blog `
  --json

python -m write_as_me.cli heldout compare `
  --workspace dist\heldout-eval `
  --generic generic.md `
  --profile-guided profile-guided.md `
  --output dist\heldout-eval\heldout-report.md `
  --json

python -m write_as_me.cli rewrite loop `
  --profile-pack dist\profile-pack `
  --input draft.md `
  --route blog `
  --output-dir dist\rewrite-loop `
  --json

python -m write_as_me.cli rewrite check `
  --profile-pack dist\profile-pack `
  --original draft.md `
  --rewritten rewritten.md `
  --route blog `
  --output dist\rewrite-loop\rewrite-check.md `
  --json
```

These commands produce local evidence about profile distance and rewrite
movement. They should not be described as Copykiller automation or detector
bypass.
