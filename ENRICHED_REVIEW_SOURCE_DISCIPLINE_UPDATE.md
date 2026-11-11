# Enriched Review — Source Discipline Update (PART 4)

**Date:** 2026-05-29. Markdown-only change. No code/scoring/strategy touched.

## What changed

Added **Section 14 — Source citation discipline (MANDATORY)** to
`prompts/llm_review/enriched_market_review_protocol.md`.

## New mandatory rules

Every external claim in an enriched review must carry:
- source name; headline/title; date/timestamp; URL (if available); freshness;
  relevance; confirms/weakens/contradicts; whether price already reacted.

Hard prohibitions:
- **No uncited external statistics** (revenue/EPS/PT/%-moves must be sourced).
- **No uncited legal claims** — indictment/SEC/DOJ/auditor/fraud/class-action
  statements REQUIRE a named source + date (+ URL ideally). Uncitable → cannot
  be stated as fact.
- **No invented TradingView/chart observations** — if charts unavailable, say so.
- **Missing source → "source unavailable"**, never assumption.
- **test_source / fixture data is not a valid external source.**
- Every review ends with a **Sources:** section (markdown hyperlinks).
- If web access is fully unavailable: declare it up front and do NOT upgrade
  confidence on imagined context.

## Why

The cycle-2 SMCI finding (active federal indictment) showed external research
materially changes verdicts. To trust that layer, every external claim must be
auditable. The prior two enriched reviews already included a Sources section;
this update makes it a **hard requirement** of the protocol going forward.

## Compliance check (existing reviews)

- `OPUS_ENRICHED_MARKET_REVIEW_LATEST.md` — ✅ has Sources section.
- `OPUS_ENRICHED_REVIEW_CYCLE2.md` — ✅ has Sources section (SMCI/PLTR/NVDA cited).
- `OPUS_MANUAL_REVIEW_LATEST_ANALYSIS.md` — internal-only review (no external
  claims), so no citations required; conforms.

No code changes. No auto-trade. Advisory layer only.
