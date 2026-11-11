# Stocks Position Swing V2

> SHADOW ONLY. Separate tables and strategy identity. No proposed_signals, signal_outcomes, final_r, Paper ledger, Telegram, or live routing.

- strategy_id: `stocks_position_swing_v2`
- shadow_lane: `shadow_stocks_position_swing_v2`
- profile: `stocks_position_swing_v2@2026-08-05_swing_entry_window_v2`
- execution profile: `us_equity_commission_free_7bps_swing_entry_window_v2`
- scheduler_enabled: `True`

## Implemented rules

- Long-only v2.
- Setups: confirmed BREAKOUT_RETEST and TREND_PULLBACK_RECLAIM.
- Entry begins on the next US cash session, expires after 5 sessions, and rejects gaps beyond the configured ATR chase limit.
- Risk-on allows both setups; neutral allows half-size pullback/reclaim only; risk-off blocks new longs.
- Earnings, legal/dilution/delisting/FDA risk, stale/missing data, sector trend, SPY/sector relative strength, weekly trend, and gap risk are deterministic gates.
- Stop and target fills are gap-aware; same-bar ambiguity is stop-first.
- Net USD PnL is authoritative; fees and slippage remain separate.

## Readiness

- verdict: **INSUFFICIENT_FORWARD_EVIDENCE**
- candidates: 9; clean closed: 1; pending: 5; no-entry: 3
- forward days: 56; net USD: $-4.38; PF: 0.000; winrate: 0.000
- max drawdown: $4.38 (0.09% of model equity); drawdown gate: True
- clean closed by setup: `{"TREND_PULLBACK_RECLAIM": 1}`

## Latest rejection reasons

| Reason | Count |
|---|---:|
| SECTOR_RS_NOT_POSITIVE | 52 |
| NOT_ABOVE_50D | 40 |
| RS_SPY_NOT_POSITIVE | 40 |
| RS_SECTOR_NOT_POSITIVE | 36 |
| SECTOR_NOT_ABOVE_50D | 33 |
| NOT_ABOVE_WEEKLY_30W | 32 |
| NOT_ABOVE_200D | 31 |
| TOO_FAR_FROM_HIGH | 30 |
| BLOCKING_EVENT:legal_risk | 4 |
| EARNINGS_WITHIN_HOLD_WINDOW | 4 |
| NO_CONFIRMED_V2_SETUP | 4 |

## Candidates

| ID | Symbol | Setup | Regime | Score | Entry | Stop | TP1 | TP2 | Risk $ | Size | Status |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| spv2_MSFT_2026-09-24_trend_pullback_reclaim | MSFT | TREND_PULLBACK_RECLAIM | risk_on | 93 | 499.29 | 488.74 | 520.40 | 530.95 | 12.50 | 1.00 | shadow_open |
| spv2_XOM_2026-09-22_trend_pullback_reclaim | XOM | TREND_PULLBACK_RECLAIM | risk_on | 81 | 160.16 | 155.67 | 169.13 | 173.62 | 12.50 | 1.00 | shadow_open |
| spv2_MRK_2026-09-17_trend_pullback_reclaim | MRK | TREND_PULLBACK_RECLAIM | risk_on | 87 | 147.80 | 142.75 | 157.89 | 162.93 | 12.50 | 1.00 | shadow_open |
| spv2_JNJ_2026-09-17_trend_pullback_reclaim | JNJ | TREND_PULLBACK_RECLAIM | risk_on | 79 | 271.13 | 264.99 | 283.42 | 289.56 | 12.50 | 1.00 | shadow_open |
| spv2_ABBV_2026-09-15_trend_pullback_reclaim | ABBV | TREND_PULLBACK_RECLAIM | neutral | 86 | 265.10 | 256.33 | 282.64 | 291.41 | 6.25 | 0.50 | shadow_open |
| spv2_MRK_2026-09-08_trend_pullback_reclaim | MRK | TREND_PULLBACK_RECLAIM | risk_on | 87 | 149.84 | 144.89 | 159.74 | 164.69 | 12.50 | 1.00 | shadow_no_entry |
| spv2_TMO_2026-09-03_trend_pullback_reclaim | TMO | TREND_PULLBACK_RECLAIM | risk_on | 88 | 623.76 | 596.43 | 678.44 | 705.78 | 12.50 | 1.00 | shadow_no_entry |
| spv2_BAC_2026-09-03_trend_pullback_reclaim | BAC | TREND_PULLBACK_RECLAIM | risk_on | 81 | 63.33 | 61.66 | 66.65 | 68.32 | 12.50 | 1.00 | shadow_no_entry |
| spv2_MS_2026-08-04_trend_pullback_reclaim | MS | TREND_PULLBACK_RECLAIM | risk_on | 74 | 219.13 | 206.17 | 245.04 | 257.99 | 12.50 | 1.00 | shadow_closed |

## Outcomes

| Candidate | Symbol | Setup | Status | Net $ | Fees $ | Slip $ | MFE R | MAE R | Gap R | Clean |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| spv2_ABBV_2026-09-15_trend_pullback_reclaim | ABBV | TREND_PULLBACK_RECLAIM | pending | - | - | - | 0.49 | -0.44 | 0.00 | True |
| spv2_JNJ_2026-09-17_trend_pullback_reclaim | JNJ | TREND_PULLBACK_RECLAIM | pending | - | - | - | 0.52 | -0.99 | 0.10 | True |
| spv2_MRK_2026-09-17_trend_pullback_reclaim | MRK | TREND_PULLBACK_RECLAIM | pending | - | - | - | 1.14 | -0.44 | 0.00 | True |
| spv2_XOM_2026-09-22_trend_pullback_reclaim | XOM | TREND_PULLBACK_RECLAIM | pending | - | - | - | 1.06 | -0.20 | 0.00 | True |
| spv2_MSFT_2026-09-24_trend_pullback_reclaim | MSFT | TREND_PULLBACK_RECLAIM | pending | - | - | - | 1.91 | -0.19 | 0.00 | True |
| spv2_MRK_2026-09-08_trend_pullback_reclaim | MRK | TREND_PULLBACK_RECLAIM | no_entry | - | - | - | - | - | - | True |
| spv2_BAC_2026-09-03_trend_pullback_reclaim | BAC | TREND_PULLBACK_RECLAIM | no_entry | - | - | - | - | - | - | True |
| spv2_TMO_2026-09-03_trend_pullback_reclaim | TMO | TREND_PULLBACK_RECLAIM | no_entry | - | - | - | - | - | - | True |
| spv2_MS_2026-08-04_trend_pullback_reclaim | MS | TREND_PULLBACK_RECLAIM | closed | -4.38 | 0.00 | 0.23 | 0.08 | -0.43 | 0.00 | True |

## Evidence gate

- Minimum 28 forward days.
- Minimum 30 clean closed trades and 10 per setup.
- Positive net USD PnL and PF >= 1.25.
- Maximum drawdown no greater than 8% of model equity.
- No automatic promotion. A passing gate remains REVIEW_ONLY until manual review.

## Advisory reviews

| Candidate | Cycle | Verdict | Confidence |
|---|---|---|---:|
| - | - | no reviews yet | - |
