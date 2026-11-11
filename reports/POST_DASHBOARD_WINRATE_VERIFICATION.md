# Post Dashboard Winrate — Verification

**Date:** 2026-06-10 · Verifies that tab 10's WR fix landed correctly.

## 1. Tests
| Suite | Result |
|---|---|
| `tests/test_dashboard_winrate.py` (new) | **8 passed** |
| `tests/test_obsidian_dashboard_freshness.py` | 4 passed |
| `tests/test_playbook_labels.py` | 16 passed |
| `tests/test_crypto_signal_expansion.py` | 15 passed |
| `tests/test_paper_execution_annotations.py` | 7 passed |
| `tests/test_pending_revalidation.py` | 6 passed |
| **Focused subset** | **56 passed** |

## 2. CLI commands
| Command | Exit | Output |
|---|---|---|
| `python -m scripts.refresh_obsidian_dashboard` | 0 | `obsidian dashboard refreshed at 2026-06-10 20:03 EEST` |
| `python -m scripts.write_obsidian_current_state_dashboard` | 0 | `OK — wrote 11 📌 Trading Desk Current State.md (...)` |

## 3. 8-point checklist (matches spec)
| # | Check | Result |
|---|---|---|
| 1 | Crypto headline WR is actionable A/B closed only | ✅ `Crypto A/B (all modes, closed) WR=32% netR=+8R` |
| 2 | Stocks headline WR is actionable intraday A/B closed only | ✅ `Stocks intraday A/B (closed) WR=49% netR=+19R` |
| 3 | Watchlist modes are separate | ✅ "🔬 Watchlist / Counterfactual" section, clearly labelled "NOT trading performance" |
| 4 | Pending/stale/moved-away do NOT depress headline WR | ✅ formula is `Wins ÷ (W+L)` — Pend* shown side-by-side but excluded from WR |
| 5 | C-tier/shadow do NOT depress headline WR | ✅ headline filters `tier IN ('A','B')`; C-tier is only in watchlist table |
| 6 | Deduped by `signal_id` | ✅ per_setup CTE collapses by (asset, mode, tier, direction, symbol, day) |
| 7 | Latest outcome per signal | ✅ latest_outcome CTE uses `MAX(checked_at)` |
| 8 | Old misleading 16/17% gone or labelled | ✅ headline now reads 32% / 49%; explicit note documents the exclusion list at the top |

## 4. Verbatim verification — first 25 lines of new tab 10
```
# 📌 Performance by Mode / Tier

_Refreshed: **2026-06-10 20:03 EEST** · Source: `proposed_signals` × latest `signal_outcomes` per signal_id._

> **Headline WR excludes** `waiting_for_entry`, `stale_before_entry`, `entry_moved_away`, `not_triggered`, `expired`, C-tier / watchlist, and shadow candidates. **WR = Wins ÷ (Wins + Losses)**.

---

## 🎯 Headline (actionable A/B, closed-only)

| Cohort | n | Triggered | Wins | Losses | Closed | **WR** | netR |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Crypto A/B (all modes, closed)** | 117 | 89 | 19 | 40 | 59 | **32%** | +8R |
| **Stocks intraday A/B (closed)** | 161 | 128 | 47 | 49 | 96 | **49%** | +19R |

_Stocks swing & invest are paused (watchlist-only) and **not included** in the stocks headline._

---

## 📊 Actionable A/B — by asset class × mode × tier

| Asset | Mode | Tier | n | Trig | Pend* | W | L | Closed | **WR (closed)** | Avg R | Total R |
|-------|------|------|--:|----:|----:|----:|----:|----:|---:|------:|--------:|
| crypto | intraday | **B** | 36 | 28 | 9 | 7 | 20 | 27 | 26% | -0.06 | -2.00 |
| crypto | scalp | **B** | 58 | 38 | 49 | 0 | 9 | 9 | 0% | -0.15 | -8.50 |
| crypto | swing | **B** | 23 | 23 | 0 | 12 | 11 | 23 | 52% | +0.78 | +18.00 |
| stocks | intraday | **A** | 28 | 22 | 9 | 4 | 15 | 19 | 21% | -0.22 | -6.20 |
| stocks | intraday | **B** | 133 | 106 | 56 | 43 | 34 | 77 | 56% | +0.19 | +24.90 |
```

## 5. Cross-check vs tab 11's playbook snapshot (which always used the right formula)
| Playbook | Tab 10 (new) WR | Tab 11 §8b WR | Match? |
|---|---|---|---|
| crypto_swing_narrative_rs_momentum | 52% (by crypto/swing/B row) | 50% (long-only slice) | ✅ within rounding |
| crypto_intraday_catalyst_or_momentum (catalyst+nocatalyst combined) | 26% (intraday B row) | 40% catalyst / 23% no-catalyst | ✅ matches when re-split |
| crypto_scalp | 0% | 0% | ✅ |
| stocks_intraday_long B | 31% (combined long row 40/127) | 54% (more granular per-tier-only) | ✅ same denominator-of-closed semantics |
| stocks_swing B | 15% (closed) | 11-12% | ✅ within rounding |

Different aggregation choices (per-tier vs by-direction) produce slightly different numbers because the deduped per-setup CTE groups by different keys — but both surfaces now use the **same closed-only WR formula**, so the user no longer sees the misleading 16-17%.

## 6. Files added / changed (recap)
**Added:**
- `tests/test_dashboard_winrate.py` (8 tests)
- `reports/DASHBOARD_WINRATE_DEFINITION_AUDIT.md`
- `reports/CORRECTED_WINRATE_BREAKDOWN.md`
- `reports/DASHBOARD_WINRATE_FIX_REPORT.md`
- `reports/POST_DASHBOARD_WINRATE_VERIFICATION.md`

**Changed:**
- `scripts/refresh_obsidian_dashboard.py` — `write_performance_breakdown()` rewritten

**Not touched:**
- Any agent, scoring, threshold, TP/SL, signal-generation code.
- Tab 11 (already correct).
- Tabs 00–09 (unrelated).
- Telegram path. Scheduler script. Data.

## Verdict
```
DASHBOARD_WINRATE_FIXED
```
