---
description: Create a reusable writing skill for any recurring writing situation.
argument-hint: "[writing situation and constraints]"
---

Use the Write As Me KO Create Skill workflow.

Start from `$ARGUMENTS`. Do not restrict the user to predefined channels. If the user
mentions a known preset, use it as a starter; otherwise create a custom skill from the
user's situation, audience, constraints, tone, examples, and checklist.

Useful commands:

```powershell
python -m scripts.create_writing_skill --list-presets
python -m scripts.create_writing_skill --preset thread-post --output-root dist\writing-skills --force
```

For a custom skill, collect or infer:

- skill name
- purpose
- audience
- hard constraints
- tone constraints
- examples
- checklist

Then generate a skill with `scripts.create_writing_skill`, review the generated
`SKILL.md`, and run `npm run docs:check`.
