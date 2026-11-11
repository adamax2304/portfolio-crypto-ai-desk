# Pre Catalyst Safe-Fix Baseline (PART 0)

**Date:** 2026-06-15 · Confirmed before any change.

| Check | Baseline value |
|---|---|
| Source modifications from prior audit | none (prior audit was read-only) |
| crypto A/B funding/OI coverage | present (263 with funding_context) |
| stocks `news_supported=1` count | **0** (all 1542 stocks signals) |
| crypto scalp setup Telegram | suppressed (`should_suppress_setup_telegram`) |
| paper-entry alerts | enabled |
| funding_snapshots / oi_snapshots tables | did NOT exist |
| signal_catalyst_labels table | did NOT exist |
| proposed_signals | 1805 |
| signal_outcomes | 101768 |
| SUM(final_r) | 75256.0 |

Baseline captured. All safe-fix work is additive on top of this state.
