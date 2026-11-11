# OPUS ROUTINE → MARKET TAB INTEGRATION — REPORT (PART 11)

**Scope:** PAPER/display. Date: 2026-06-24. **Enriched-review body/logic UNCHANGED** —
only a trailing final-output block is consumed.

## What was added
- **Protocol §17** appended to `prompts/llm_review/enriched_market_review_protocol.md`:
  instructs the ~4h enriched review to append, at the **very end**, a single
  `{"market_dashboard_update": {...}}` JSON block (modes, fear&greed, risk-now, today &
  long-term news, regimes, extras). Explicitly: "do not let this block alter anything
  above it"; unknown numbers → `null` (never invent F&G/VIX).
- **Parser** `src/market/market_dashboard.py`:
  - `extract_market_block(text)` — brace-balanced extraction tolerant of markdown/prose.
  - `parse_and_store(text)` — normalize + persist a snapshot.
  - `deterministic_fallback()` — minimal snapshot (latest crypto regime) when no block.
- **CLI** `scripts/market_dashboard_from_review.py` — runs at the end of the routine:
  finds the latest enriched-review markdown, extracts + stores; on missing/invalid JSON →
  fail-open to the deterministic fallback (Market tab never goes empty).

## Fail-open + staleness
If the JSON is missing/invalid, the previous snapshot is kept (or a deterministic
fallback is written). The app shows a stale-warning when the snapshot is >4h and "stale"
when >6h.

## Verified
Parser extracts a sample block (mode `chop`, F&G 52, 1 today-news); fallback stores a
snapshot; CLI smoke OK. Tests: `tests/test_market_dashboard.py` (4 passed — extract,
missing→None, persist, fallback).

## Verdict
**OPUS_ROUTINE_UPDATES_MARKET_TAB_WITHOUT_CHANGING_REVIEW**
