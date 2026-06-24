# Profile Pack v2

Profile Pack v2 turns local Korean writing samples into a portable context pack
for AI writing agents.

It is not a detector-bypass layer and it does not export raw sample text. The
pack stores route counts, confidence, hashes, coverage, privacy notes, and a
portable `AGENTS.md` export that future agents can read before drafting.
It also stores deterministic Korean style signals, such as sentence length,
sentence endings, connectors, first-person markers, stance markers, structure,
and character n-grams.
Privacy scanning detects sensitive patterns such as emails, phone numbers,
resident-id-like strings, student-id-like strings, token-like strings, and URLs
without copying raw values into generated reports.

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

Write a judge-readable demo report:

```powershell
python -m write_as_me.cli demo report --profile-pack _workspace\profile-pack-demo --output _workspace\profile-pack-demo\demo-report.md --json
```

## Artifacts

- `profile.json`: machine-readable summary, confidence, route counts, and privacy metadata.
- `sample-manifest.json`: relative paths, routes, hashes, and character counts only.
- `voice-profile.md`: conservative profile summary without raw sample text.
- `route-map.md`: route coverage for writing situations.
- `privacy-report.md`: local-only and raw-sample export boundary.
- `coverage-report.md`: missing route and confidence summary.
- `demo-report.md`: judge-readable summary of profile, style, privacy, and expected agent behavior.

`profile.json` also includes:

- `style_features`: aggregate deterministic writing signals across the sample set.
- `route_style_features`: the same signals split by route.
- `privacy`: risk, finding count, finding kinds, and path counts only.

These fields are deliberately count-based and summary-based. They are meant to
support review and downstream skills without copying the user's original text.

## Completion Gate

`npm run docs:check` runs the unit tests, the existing synthetic writing eval,
and the Profile Pack v2 demo build/doctor/eval/export/demo-report workflow.

## Research Grounding

See [Research Basis](research-basis.md) for the stylometry and text-style
transfer rationale behind the deterministic-first design.
