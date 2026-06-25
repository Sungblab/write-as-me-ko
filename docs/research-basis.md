# Research Basis

`write-as-me-ko` uses deterministic Korean writing signals first, then leaves
LLM interpretation as an optional review layer. This is intentional.

The project is not trying to identify a person, bypass detectors, or clone a
voice. It borrows conservative ideas from stylometry and text style transfer:
measure reproducible writing signals, keep source content private, preserve
facts, and expose the confidence limits of the generated profile.

## Why Deterministic Signals Come First

Stylometry and authorship-attribution research has long used measurable text
features such as function words, character n-grams, lexical patterns,
structural layout, and syntactic patterns. These features are useful because
they can be extracted repeatedly without asking a model to guess.

For this project, that means the baseline profile should come from local,
auditable signals:

- sentence and paragraph length
- Korean sentence endings
- connectors such as `그런데`, `그래서`, `다만`
- first-person markers
- stance markers such as hedging or assertive words
- bullet and heading structure
- character n-gram summaries
- route-specific differences between blog, report, message, and project docs

The deterministic layer should never export raw sample text. It should export
counts, hashes, confidence, and reviewable summaries.

## Why LLM Review Still Helps

Statistics can show that a user often writes short sentences, uses `다` endings,
or separates limits from results. It cannot reliably decide by itself how those
signals should become a useful LinkedIn post skill, professor-message skill, or
contest-submission skill.

The intended split is:

- Python: extract reproducible signals and privacy-safe profile artifacts.
- LLM: interpret those signals into route-specific writing guidance and reusable
  `SKILL.md` files.
- User: review the generated profile before using it for sensitive writing.

This keeps the project local-first and inspectable while still using AI where it
is useful: summarizing patterns, drafting route guidance, and creating reusable
agent skills.

## Evaluation Principle

Text style transfer evaluation is multi-dimensional. A good result should not
only sound more like a target style. It should also preserve content and remain
fluent.

For `write-as-me-ko`, the practical evaluation dimensions are:

- content preservation: facts, names, dates, numbers, quotes, and links remain intact
- route fit: a report remains a report, a message remains a message
- style adherence: generated output follows the profile within confidence limits
- style distance: generated output should move closer to held-out user prose
  than a generic LLM baseline does
- natural Korean: avoid mechanical transitions and translationese
- privacy: raw samples and obvious private identifiers do not leak into exports

External detector scores can be useful as smoke-test observations, but they
should not become a product guarantee. Detector results are sensitive to domain,
length, model, and revision behavior, and should be recorded separately from
local deterministic evaluation.

The Stage 9 local workflow turns this into two checks:

- `style-distance`: compare a draft against profile-pack style signals, or
  compare human/generic/profile-guided variants for the same route.
- `rewrite brief`: produce an agent-readable revision brief with distance,
  risk points, rewrite mode, and strict fact-preservation constraints.

The Stage 10 local workflow makes the check closer to real use:

- `heldout prepare`: exclude selected local samples from the training profile
  and keep only metadata in the held-out manifest.
- `heldout compare`: compare the excluded human sample with generic and
  profile-guided drafts for the same route.
- `rewrite loop` and `rewrite check`: produce a before report and brief, then
  verify whether a revised draft moved closer to the profile without treating
  that as an external detector result.

## Sources

- Mike Kestemont, "Function Words in Authorship Attribution. From Black Magic to Theory?" ACL Anthology, 2014: https://aclanthology.org/W14-0908/
- Ahmed Abbasi and Hsinchun Chen, "Writeprints: A Stylometric Approach to Identity-Level Identification and Similarity Detection in Cyberspace", ACM TOIS, 2008: https://dl.acm.org/doi/10.1145/1344411.1344413
- G. Rios-Toledo et al., "Detection of changes in literary writing style using N-grams as style markers and supervised machine learning", PLOS ONE, 2022: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0267590
- Razieh Ostadimoqadam et al., "Text Style Transfer Evaluation Using Large Language Models", LREC-COLING, 2024: https://aclanthology.org/2024.lrec-main.1373/
- "TSTBench: A Comprehensive Benchmark for Text Style Transfer", PMC, 2025: https://pmc.ncbi.nlm.nih.gov/articles/PMC12191983/
