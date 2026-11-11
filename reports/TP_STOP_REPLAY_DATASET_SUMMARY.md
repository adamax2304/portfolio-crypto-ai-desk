# TP/Stop Replay Dataset — Summary (PART 2)

**Date:** 2026-06-23. Read-only. CSV: `data/research/tp_stop_replay_dataset_2026-06-23.csv` (builder: `scripts/tp_stop_replay.py`).

## Scope & dedup
- Source: `signal_outcomes` latest-row-per-signal (`ROW_NUMBER() … ORDER BY checked_at DESC, id DESC`), joined to `proposed_signals`, **entry_triggered=1**, window **last 60 days** (since 2026-04-24).
- Deduped to **economic trades** by `(symbol, direction, mode, tier, rounded-entry, entry-day)`, keeping the most-resolved row. Original signal_ids collapse into one trade.
- **N = 1404** deduped entered economic trades.
- **Path coverage = 100%** (1404/1404 have a resolvable outcome + computable R-ladder) — the 60-day OHLCV backfill (5m/15m crypto, 15m stocks) covers the whole window. (Secondary 30d / since-restart are subsets of this.)

## Book split (per the canonical actionability gates)
| Book | n | note |
|---|---|---|
| **Operator/Paper (actionable)** = A/B tier, not crypto-scalp, not stocks swing/invest | **582** | the cohort a policy change would affect |
| Shadow (C-tier, crypto scalp, stocks swing/invest, guard-blocked) | 822 | excluded from the decision; reported separately |

Fields per trade (CSV columns): economic key, signal_id, symbol, asset_class, mode, tier, direction, playbook, regime, catalyst(yes/no), created_at, entry_at, stop_at, final_outcome, final_r, r_tp1/r_tp2/r_tp3 (R-ladder from prices), reached_tp1/2/3, hit_stop, expired, ambiguous, mfe_r, mae_r, and 7 reconstructed exit-model R columns (`m_prod_best`, `m_cap_tp2`, `m_hold_tp1/2/3`, `m_be_after_tp1`, `m_partial_be`).

## Reconstruction method (no re-walk needed)
The production tracker already recorded the **order** of level touches (`tp1_hit_at`, `tp2_hit_at`, `tp3_hit_at`, `stop_hit_at`). Counterfactual exit models are reconstructed from those timestamps + the per-trade R-ladder (R of each TP relative to entry, risk = |entry−stop|). Same-candle stop+TP is conservative (stop-first), inherited from production.

## Coverage caveats (reliability)
- Production accounting is **best-TP-touched (optimistic)** — see `STOP_AFTER_TP_ACTUAL_BEHAVIOR_AUDIT.md`. So `final_r` over-credits; realistic hold/BE models are computed separately and are **relative rankings, not reliable absolute R** (5m/15m granularity + same-candle ambiguity).
- `market_regime` present on ~63% of rows (rest = "unknown"); catalyst flag is the refreshed `news_supported/telegram_supported`.

## Verdict
`TP_REPLAY_DATASET_READY`
