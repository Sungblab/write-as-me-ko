# Profile Pack v2

Profile Pack v2 turns local Korean writing samples into a portable context pack
for AI writing agents.

It is not a detector-bypass layer and it does not export raw sample text. The
pack stores route counts, confidence, hashes, coverage, privacy notes, and a
portable `AGENTS.md` export that future agents can read before drafting.

## Commands

Build a profile pack:

```powershell
python -m write_as_me.cli profile build --samples examples\profile-pack-samples --output _workspace\profile-pack-demo --json
```

Validate it:

```powershell
python -m write_as_me.cli doctor --profile-pack _workspace\profile-pack-demo --json
```

Evaluate whether it is strong enough for reuse:

```powershell
python -m write_as_me.cli eval --profile-pack _workspace\profile-pack-demo --json
```

Export portable agent context:

```powershell
python -m write_as_me.cli export agents --profile-pack _workspace\profile-pack-demo --output _workspace\profile-pack-demo\AGENTS.md --json
```

## Artifacts

- `profile.json`: machine-readable summary, confidence, route counts, and privacy metadata.
- `sample-manifest.json`: relative paths, routes, hashes, and character counts only.
- `voice-profile.md`: conservative profile summary without raw sample text.
- `route-map.md`: route coverage for writing situations.
- `privacy-report.md`: local-only and raw-sample export boundary.
- `coverage-report.md`: missing route and confidence summary.

## Completion Gate

`npm run docs:check` runs the unit tests, the existing synthetic writing eval,
and the Profile Pack v2 demo build/doctor/eval/export workflow.
