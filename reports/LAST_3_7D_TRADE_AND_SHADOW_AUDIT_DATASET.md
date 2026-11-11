# Last 3–7d Trade & Shadow Audit — Dataset (PART 1)

**Date:** 2026-06-17 · **Window:** last 7 days (2026-06-10 → 06-17 UTC) · **Read-only** (DB opened `mode=ro`; no strategy/scoring/TP/SL changes).
**Builder:** `reports/audit_3_7d.py` → `LAST_3_7D_TRADE_AND_SHADOW_AUDIT_DATASET.csv` (one row per signal, all PART-1 fields) + `_audit_3_7d_agg.json`.
Sources: `db/crypto_ai_desk.sqlite` (`proposed_signals`, `signal_outcomes`, `signal_alerts`), OHLCV cache `data/raw/ohlcv/`, `config/signal_tracking.yaml`.

## What's in the CSV
`signal_id, symbol, asset_class, mode, tier, direction, score, created_at, entry_planned,
entry_triggered_at, entry_actual, stop, tp1/2/3, status, final_outcome, exit_at, result_R,
mfe_r, mae_r, time_to_stop_h, time_to_tp_h, held_hours, overnight_carried, freshness_label,
detection_lag_h, alert_sent_at, telegram_status, shadow_reason, concentration_status,
concentration_reason, size_weight, playbook, news_supported, oi_context, funding_context,
market_regime, narrative, validity_hours`

MFE/MAE/hit-times/final_R are taken from the tracker's stored `signal_outcomes` (already reconciled against OHLCV), so most of the audit needs no re-replay.

## Totals (559 signals in window)

| asset/mode | signals | triggered | closed | W | L | exp@0R | WR(excl exp) | sumR | avgR | PF |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| stocks/intraday | 173 | 113 | 113 | 20 | 45 | 48 | 30.8% | **−12.0** | −0.106 | 0.73 |
| crypto/scalp *(shadow)* | 113 | 45 | 45 | 2 | 9 | 34 | 18.2% | **−7.0** | −0.156 | 0.22 |
| crypto/intraday | 89 | 52 | 52 | 18 | 33 | 1 | 35.3% | 0.0 | 0.0 | 1.00 |
| stocks/swing | 70 | 51 | 51 | 7 | 8 | 36 | 46.7% | +2.0 | +0.039 | 1.25 |
| stocks/invest | 59 | 36 | 36 | 0 | 0 | 36 | — | 0.0 | 0.0 | — |
| crypto/swing | 55 | 47 | 47 | 17 | 30 | 0 | 36.2% | 0.0 | 0.0 | 1.00 |

**Status mix:** stale_before_entry 141 · stopped 123 · triggered(open) 88 · expired 67 · waiting 38 · tp1 33 · entry_moved_away 31 · tp2 18 · tp3 13 · missed_no_entry 5 · ambiguous 2.
**Triggered final outcome:** expired 155 · loss 123 · win 64 · ambiguous 2.

## Headline reads (detail in the per-part reports)
- **Net P&L is roughly flat-to-slightly-negative**, dragged by **stocks/intraday (−12R)** and **crypto/scalp (−7R, shadow-only — correctly not actionable)**. crypto/intraday + crypto/swing are ≈breakeven (PF 1.0); stocks/swing slightly positive.
- **155 triggered trades "expired at 0R"** (entered, never resolved to ±1R inside the validity window) — concentrated in stocks (48 intraday + 36 swing + 36 invest) and crypto scalp (34).
- **91 intraday trades carried overnight** (84 stocks, 7 crypto).
- Companion CSVs: `STOP_WICK_REENTRY_STUDY.csv`, `STOP_WICK_MANIPULATION_COUNTERFACTUAL.csv`, `SHADOW_MODE_COUNTERFACTUAL.csv`, `STOCK_SECTOR_CAP_COUNTERFACTUAL.csv`.
