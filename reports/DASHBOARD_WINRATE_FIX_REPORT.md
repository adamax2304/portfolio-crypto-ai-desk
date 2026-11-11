# Dashboard Winrate — Fix Report

**Date:** 2026-06-10 · Scope: reporting/labeling only. No scoring, threshold, TP/SL, signal-generation, or data changes. Tab 10 `Performance by Mode` rewritten to use the correct WR formula and to separate actionable A/B from watchlist/counterfactual rows.

## 1. Root cause (one line)
Tab 10 computed `WR = Wins ÷ n`, where `n` included pending / expired / not_triggered AND C-tier watchlist setups. The closed-only formula `WR = Wins ÷ (Wins + Losses)` was missing.

## 2. What was changed
File: `scripts/refresh_obsidian_dashboard.py` — `write_performance_breakdown()`.

| Change | Detail |
|---|---|
| New WR formula | `_wr_closed(wins, losses)` returns `wins / (wins + losses) * 100`. No closures → returns `—`, never `0%`. |
| **Headline section** | New "🎯 Headline (actionable A/B, closed-only)" block shows two rows: `Crypto A/B (all modes)` and `Stocks intraday A/B`. Stocks swing & invest are explicitly excluded from the stocks headline (they're paused). |
| **Pend\*** column added | Visible alongside W/L/Closed so the reader can see how many setups are pending vs closed. |
| Actionable vs Watchlist split | Two separate tables: **"Actionable A/B — by asset × mode × tier"** and **"Watchlist / Counterfactual"** (clearly labelled "NOT trading performance"). |
| Same split for By-direction | Actionable A/B by direction in one table; C-tier by direction in the watchlist section. |
| Explicit headline note | Top of file: `Headline WR excludes waiting_for_entry, stale_before_entry, entry_moved_away, not_triggered, expired, C-tier/watchlist, and shadow candidates. WR = Wins ÷ (Wins + Losses).` |
| Column documentation updated | "WR" definition rewritten to `Wins ÷ Closed × 100`; "Pend*" added; "Closed" added. |

## 3. Before / after (live data)

### Before (yesterday's render of tab 10)
```
| crypto | long | 67 | 13 | 27 | 19% |   ← misleading
| stocks | long | 467 | 78 | 197 | 17% |  ← misleading
| stocks | intraday | C | 226 | 37 | 16% |  ← THE user-reported 16%
```

### After (today's regenerated tab 10)
```
🎯 Headline (actionable A/B, closed-only)

| Crypto A/B (all modes, closed) | n=117 | trig=89 | W=19 L=40 closed=59 | WR=32% | netR=+8R |
| Stocks intraday A/B (closed)   | n=161 | trig=128 | W=47 L=49 closed=96 | WR=49% | netR=+19R |
```

Both numbers now match what tab 11's `## 8b. Playbook Performance Snapshot` shows (which always used the right formula).

## 4. Tests
File: `tests/test_dashboard_winrate.py` — 8 tests, all pass:

| # | Test | What it asserts |
|---|---|---|
| 1 | `test_pending_signals_excluded_from_closed_wr` | 3W/2L/10pending → 60% (not 21%) |
| 2 | `test_expired_zero_r_excluded_from_wr` | expired rows (final_r=0) excluded |
| 3 | `test_only_losses_returns_zero_percent` | 0W/9L → "0%" (real outcome) |
| 4 | `test_only_wins_returns_hundred_percent` | 5W/0L → "100%" |
| 5 | `test_no_closures_returns_dash` | 0W/0L → "—" (not a misleading 0) |
| 6 | `test_dedupe_cte_collapses_duplicate_signal_ids` | per_setup CTE deduplicates duplicate signal_ids per (asset, mode, tier, direction, symbol, day) |
| 7 | `test_watchlist_modes_excluded_from_headline_helper` | stocks intraday headline doesn't pull from stocks swing / invest |
| 8 | `test_old_misleading_formula_vs_new` | Documents the bug: 40W/30L/30pend gave 40% old, 57% correct |

## 5. What was NOT changed
- No trading strategy.
- No scoring.
- No thresholds.
- No TP/SL.
- No signal generation.
- No agents.
- No data was rewritten, deleted, or moved.
- No other dashboard tabs touched (tab 11's WR was already correct).

## 6. Verdict
```
DASHBOARD_WINRATE_FIXED
```

The user's 16-17% WR observation was caused by a misleading display formula on tab 10 — **not** by real trading performance issues. The corrected headline matches what tab 11 and prior playbook audits already documented: crypto A/B at 32% closed WR (driven by swing 52% and catalyst intraday 40%), stocks intraday A/B at 49% closed WR (with B-tier shorts at 69% PF 3.00).
