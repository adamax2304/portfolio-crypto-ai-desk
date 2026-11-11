# Dashboard Winrate Definition Audit (PART 1)

**Date:** 2026-06-10 · Read-only audit. No code changed in this step.

## 1. Surfaces that compute WR

| Surface | File | WR formula |
|---|---|---|
| **Tab 10 `Performance by Mode`** (the source of user-observed 16/17%) | `scripts/refresh_obsidian_dashboard.py` → `write_performance_breakdown()` | `_wr(wins, n) = wins / n * 100` where **n = ALL setups** (incl. pending, expired, not_triggered, C-tier) |
| Tab 11 `Trading Desk Current State` → `## 8b. Playbook Performance Snapshot` | `scripts/write_obsidian_current_state_dashboard.py` → `section_playbook_performance()` | `wr = wins / closed * 100` where **closed = wins + losses** ✅ |
| Tab 11 `Trading Desk Current State` → `## 9. Performance Snapshot` | same file → `section_performance()` + `slice_stats()` | `WR = wins / closed * 100` ✅ |
| CLI `signal-stats` | `src/signals/analytics.py` | mixed; per-cohort `triggered winrate` is `wins / triggered` |

## 2. Where the misleading 16/17% comes from

The user observed:
- "crypto winrate around 16%"
- "stocks winrate around 17%"

These numbers reproduce **exactly** in tab 10 today:
```
| crypto | long  | n=67  | wins=13 | WR=19% |  ← (13/67=19%, close to 16%)
| stocks | long  | n=467 | wins=78 | WR=17% |  ← THE 17%
| stocks | intraday | C | n=226 | wins=37 | WR=16% |  ← THE 16%
```

The denominator (`n`) in tab 10 is the **deduped-setup count**, which includes:
- C-tier watchlist/shadow signals (the stocks_swing + stocks_invest paused cohort, plus C-tier crypto)
- Pending `waiting_for_entry`, `stale_before_entry`, `entry_moved_away`
- `not_triggered` (entry never reached)
- `expired` (validity window passed without TP or stop)

None of these are clean wins or losses; they should NOT depress the WR. The correct formula is **Wins ÷ (Wins + Losses)** — closed trades only.

## 3. Answers to the 10 audit questions (about tab 10)

| # | Question | Answer |
|---|---|---|
| 1 | Which statuses are in the **numerator**? | Setups where the **average** `final_r > 0` across duplicate signal_ids (= "wins") |
| 2 | Which statuses are in the **denominator**? | **n** = every deduped (asset, mode, tier, direction, symbol, day) row — INCLUDING pending/expired/not_triggered/C-tier |
| 3 | Are pending/waiting/stale/entry_moved_away included? | **YES — in the denominator only** (depresses WR) |
| 4 | Are expired/not_triggered included? | **YES — in the denominator** |
| 5 | Are C-tier/watchlist/shadow included? | **YES** — every tier appears as its own row, but in the `By direction` aggregate they all blend together |
| 6 | Are stocks swing/invest watchlist-only included? | **YES — they appear as their own rows AND blend into the By-direction totals** (this is the main inflator of n=467 for stocks long) |
| 7 | Is the calculation deduped by signal_id? | **Yes** — the CTE collapses duplicate signal_ids per `(asset, mode, tier, direction, symbol, day)` tuple |
| 8 | Does it use latest outcome per signal? | **Yes** — `MAX(checked_at)` per signal_id |
| 9 | Does it mix A/B and C-tier? | **Yes in the By-direction table**; the By-mode-tier table separates them but C-tier rows are visible and confusing |
| 10 | Does it mix all modes? | **Yes in the By-direction table** (long+short totals span scalp/intraday/swing/invest) |

## 4. Tab 11 (Playbook Performance Snapshot) is already CORRECT

Lines 879-886 in `write_obsidian_current_state_dashboard.py`:
```python
wins = [r for r in sub if r["final_outcome"] == "win"]
losses = [r for r in sub if r["final_outcome"] == "loss"]
closed = wins + losses
wr = (len(wins) / len(closed) * 100) if closed else 0.0
```
This uses Wins/Closed — the right formula. Tab 11 shows the right WR per playbook (e.g., `crypto_swing 50%`, `stocks_intraday_long 54%`).

## 5. Verdict
- **Tab 10 is misleading.** It computes `Wins ÷ n` instead of `Wins ÷ (Wins + Losses)`.
- The denominator includes pending/expired/not_triggered AND mixes A/B with C-tier watchlist counterfactuals.
- Tab 11 already does the right calculation and shows realistic playbook WRs.

```
WINRATE_DEFINITION_BUG_FOUND_IN_TAB_10
```
