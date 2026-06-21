---
name: "thread-post"
description: "Draft Korean social thread posts. Use when the user asks for Threads/X-style serial posts, launch threads, or follow-up posts with per-post length limits."
---

# thread-post

## Purpose

Turn one idea into a short Korean thread that reads like the user's own launch or reflection post.

## Audience

Korean readers who follow the user's projects, blog, or AI/dev experiments.

## Inputs To Read

1. Read the user's immediate request and source text.
2. If available, read `codex/skills/write-as-me-ko/references/voice-profile.md`.
3. If available, read the generated writing `AGENTS.md`.
4. Preserve all facts, names, dates, numbers, links, and quoted text from the user.

## Constraints

- Write in Korean unless the user asks otherwise.
- Default to about 5 posts.
- Keep each post under 500 Korean characters.
- Let the first post be the longest if it carries the problem setup.
- Use line breaks for mobile reading rhythm.
- Do not make the thread sound like generic marketing copy.

## Tone

- Start from a concrete discomfort, question, or realization.
- Prefer plain first-person reasoning over hype.
- Use the user's blog/profile voice when a voice profile is available.

## Examples

```text
Input: 새 글쓰기 도구 출시
Output: 문제의식 -> AGENTS.md 비유 -> 만든 것 -> 사용 흐름 -> 링크
```

## Checklist

- Every post is under 500 Korean characters.
- The first post explains why this exists.
- The middle posts explain what changed or how it works.
- The last post can include a link, caveat, or next step.
- Do not invent personal experience, metrics, praise, relationships, or outcomes.
- Do not copy third-party wording into the output.
- If the request conflicts with this skill, follow the user's newest explicit constraint and mention the assumption briefly.
