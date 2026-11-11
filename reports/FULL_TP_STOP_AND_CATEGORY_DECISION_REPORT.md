# Full TP/Stop & Category Decision Report (PART 9)

**Date:** 2026-06-11 · **Final decision** consolidating PARTS 1-8. Read-only.

---

## Bottom-line recommendation

```
KEEP_ALL_TP_SL_UNCHANGED
```

No production TP/SL change is justified by the available data. Sample size for any category-specific exit retune is below the threshold for committing without overfitting risk. The sizing layer (`config/sizing_weights.yaml`) is already absorbing the worst-performing cohorts (crypto scalp at 0.5×, A-tier long at 0.5×, stocks swing/invest at 0×).

---

## Answers to the 10 questions

### 1. Which categories are profitable now?
| Category | sized R | PF | WR |
|---|---:|---:|---:|
| `stocks_intraday_rth_momentum` | +133R | 2.50 | 61% |
| `crypto_swing_narrative_rs_momentum` | +19R | 2.12 | 48% |
| `crypto_failed_bounce_short` | +11R | 2.10 | 41% |

### 2. Which categories are weak but worth collecting data?
| Category | sized R | Why keep collecting |
|---|---:|---|
| `crypto_scalp_momentum_continuation` | −4.5R | 1m archive needed before exit-policy study can be conclusive |
| `crypto_intraday_catalyst_or_momentum` | −14R | Entry-filter study (failed-reclaim) is the lever; need more sample |

### 3. Which categories should remain watchlist-only?
- `stocks_swing_watchlist_rs_rotation` (0× weight). Counterfactual −32R confirms the pause.
- `stocks_invest_watchlist_30d_thesis` (0× weight). Counterfactual −26R confirms the pause.

### 4. Do we change TP anywhere now?
**No.** Detailed in [TP_VARIANT_SIMULATION_BY_CATEGORY.md](TP_VARIANT_SIMULATION_BY_CATEGORY.md). No variant beats the baseline by an amount that exceeds noise in any cohort.

### 5. Do we change stops anywhere now?
**No.** Detailed in [STOP_VARIANT_SIMULATION_BY_CATEGORY.md](STOP_VARIANT_SIMULATION_BY_CATEGORY.md). Where stops look "wrong," the underlying issue is entry-filter, not stop distance.

### 6. If yes, exactly where and why?
N/A — the answer to 4 and 5 is no.

### 7. If no, what evidence is still missing?
- **≥ 14 days continuous 1m crypto candles** to run the scalp exit-policy study with real evidence.
- **≥ 60 days of signal history** so any per-cohort TP/SL retune has enough OOS sample.
- **Snapshotting derivatives** (funding, OI) per cycle so Level B replay becomes feasible.
- **Per-symbol live spread data** to refine the crypto fees/slippage model.

### 8. Which fix is highest EV and lowest risk?
**Best-EV, lowest-risk change: defer the only candidate change** (crypto intraday catalyst 1.0× → 0.5×) until the cohort accumulates another 14 days of data. The current size-1.0× cohort is −14R sized over 33 signals. Halving the weight would cut the future drag by ~half if the cohort stays negative, but it would also cut the upside if the cohort recovers. **Net EV is borderline.**

**Best-EV non-YAML change:** continue collecting **1m crypto candles** (no production change required; just letting the existing collector run; archive will grow naturally over the next 14 days).

### 9. Which changes should be avoided because they overfit?
- Any per-playbook TP/SL retune fit to the current 20-day sample. Validation OOS pool is < 150 signals per cohort.
- Per-cluster cap on stocks intraday — counterfactual shows it would have HURT (−36R if best-1-per-cluster).
- "No-first-15m" RTH gate — simulation cuts ~26R of stocks intraday upside.
- Tighter scalp stops — kills more winners than it saves losses (PART 5 §1).

### 10. What should be monitored for the next 48h?

| Metric | Target | Action if breached |
|---|---|---|
| crypto intraday catalyst cohort sized R | should not drop below −20R | re-evaluate halving its weight |
| stocks intraday daily P&L | should stay net positive over 5-day windows | manual review |
| crypto scalp 1m candle archive growth | growing per cycle | if stalled, fix collector |
| any new playbook label appearing in data | none expected | investigate registry change |
| cluster drawdown (5-day rolling) | < −30R | manual sizing adjustment |
| paper-entry Telegram alert rate | matches actual transition events | review tracker hook |

---

## Decision matrix (vs spec options)

| Recommendation option | Applies? | Why / Why not |
|---|---|---|
| **`KEEP_ALL_TP_SL_UNCHANGED`** | ✅ **CHOSEN** | All cohorts either profitable as-is or correctly paused/sized; no exit-side change has OOS evidence |
| `CHANGE_CRYPTO_SCALP_TP_ONLY_NEEDS_APPROVAL` | ❌ rejected | Promising on 5m fallback but 0 of 25 had 1m data — LOW-CONFIDENCE |
| `CHANGE_STOPS_NEEDS_APPROVAL` | ❌ rejected | No cohort shows clear stop-side fix |
| `MODE_OR_ENTRY_FILTER_FIX_NEEDED` | ⚠️ partial | Crypto intraday catalyst shorts would benefit from an entry-filter fix, but that's a separate study not within this audit's scope |
| `NEED_MORE_DATA_BEFORE_TP_SL_CHANGE` | ⚠️ overlaps | Implied by the chosen option; the data limitation is real but doesn't block the verdict |

---

## What this report does NOT do

- It does not propose a code change.
- It does not change `config/sizing_weights.yaml`.
- It does not modify any agent, scorer, gate, or alert.
- It does not restart the scheduler.
- It does not send a real Telegram message (see Telegram summary file below — optional, operator-triggered).

---

## Next-step queue (when data permits)

1. Backfill 1m crypto candles → re-run [reports/CRYPTO_SCALP_1M_EXIT_REPLAY.md](CRYPTO_SCALP_1M_EXIT_REPLAY.md).
2. Run `crypto_intraday_catalyst_or_momentum` shorts study with a `failed-reclaim` filter — entry-side study.
3. Re-run [reports/PLAYBOOK_SIZING_WALK_FORWARD_BACKTEST.md](PLAYBOOK_SIZING_WALK_FORWARD_BACKTEST.md) every 7 days; rotate forward window.
4. At ≥ 60 days of history, revisit `stocks_swing` / `stocks_invest` pauses.

---

```
FINAL VERDICT: KEEP_ALL_TP_SL_UNCHANGED
```
