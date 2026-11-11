# Catalyst Visibility Dashboard Update (PART 8)

**Date:** 2026-06-15 · Additive sections only. Performance calculations unchanged.

## Dashboard §14 — Catalyst & Derivatives Visibility (new)

Added to `scripts/write_obsidian_current_state_dashboard.py`
(`section_catalyst_visibility`), rendered into
`obsidian_vault/11 📌 Trading Desk Current State.md` (now 56,426 chars):

| Sub-panel | Content |
|---|---|
| 14a. Catalyst-backed vs technical | crypto A/B closed split (news_supported 1 vs 0): n / wins / raw R |
| 14b. Funding/OI archive status | funding_snapshots + oi_snapshots row counts; "append-only, not read by scoring" |
| 14c. Stocks catalyst labelling | count of stocks signals now labelled news_supported=1 (forward-only) |
| 14d. Derived catalyst labels | freshness + derivatives distribution from `signal_catalyst_labels` |

## Other surfaces

- **Live shadow journal** + **signal review reports** consume the same
  `signal_catalyst_labels` derived table and `compute_labels` helper for the
  catalyst stamp.
- **Recent catalyst-backed vs technical-only trades** are visible via §14a and
  the per-signal labels.
- **Fast-move latency** summary lives in its own report
  ([FAST_MOVE_LATENCY_REPORT.md](FAST_MOVE_LATENCY_REPORT.md)).

## Safety

No existing performance number recomputed — §14 is purely additive grouped
views. Dashboard regenerates cleanly.
