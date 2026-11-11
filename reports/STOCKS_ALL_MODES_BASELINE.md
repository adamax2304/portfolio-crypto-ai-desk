# Stocks All-Modes Baseline

> Read-only evidence registry. No strategy was changed or promoted by this report.

| Family | Evidence | Closed | Net USD | PF | Verdict |
|---|---|---:|---:|---:|---|
| `stocks_intraday_breakout_continuation` | forward_post_activation | 6 | 68.39 | 3.61 | **UNDERPOWERED_CONTINUE_FORWARD** |
| `stocks_intraday_pullback_limit` | forward_post_activation | 15 | 35.15 | 1.24 | **UNDERPOWERED_CONTINUE_FORWARD** |
| `stocks_intraday_raw_variants` | forward_shadow_clean | 499 | -547.89 | 0.85 | **REJECT_STOP_TUNING** |
| `stocks_catalyst_rs` | forward_post_activation | 20 | -113.28 | 0.61 | **UNDERPOWERED_WEAK_BASELINE** |
| `stocks_earnings_gap` | earnings_only_v2 | 0 | 0 | n/a | **NO_VALID_SAMPLE** |
| `stocks_position_swing_v2` | forward_shadow_clean | 1 | -4.38 | 0.00 | **NO_VALID_SAMPLE** |
| `stocks_preus_mexc_news` | forward_paper | 22 | 518.21 | 2.37 | **PROMISING_UNDERPOWERED** |
| `stocks_residual_momentum` | historical_validation_partially_informed | 18 | 204.36 | 2.87 | **PROMISING_BUT_CONCENTRATED** |
| `stocks_pead_long` | untouched_2024_validation | n/a | -66.12 | 0.60 | **REJECT_VALIDATION_FAILURE** |
| `stocks_pead_short` | development_reconstruction | n/a | -9.38 | 0.92 | **REJECT_NO_GRID_EDGE** |
| `stocks_technical_fvg_reclaim` | development_reconstruction | 31 | -238.59 | n/a | **REJECT_NO_GROSS_EDGE** |
| `stocks_position_swing_v2_historical` | historical_screening_event_risk_partial | 9 | 1.12 | 1.03 | **UNDERPOWERED_NO_EDGE_YET** |

## Data readiness

- Yahoo symbols: 15m `54`, 1h `54`, 1d `54`.
- SPY coverage: 15m `58.3d`, 1h `548.2d`, 1d `548.0d`.
- MEXC stock-contract 15m symbols: `45`.
- Symbols with reconstructed earnings history: `68`.
- Intraday event studies are constrained by the short 15m/news overlap; 18-month claims use 1h/1d only.

## Decisions

- `stocks_intraday_breakout_continuation`: **UNDERPOWERED_CONTINUE_FORWARD**. Current production rule, not the rejected raw profile.
- `stocks_intraday_pullback_limit`: **UNDERPOWERED_CONTINUE_FORWARD**. Current production rule, not the rejected raw profile.
- `stocks_intraday_raw_variants`: **REJECT_STOP_TUNING**. Large clean sample is negative after costs; quality profiles have no closed sample.
- `stocks_catalyst_rs`: **UNDERPOWERED_WEAK_BASELINE**. Event logic is distinct, but current forward net result is negative and below 30 closes.
- `stocks_earnings_gap`: **NO_VALID_SAMPLE**. The mixed-event v1 history is invalid for v2; v2 has no clean closed trades yet.
- `stocks_position_swing_v2`: **NO_VALID_SAMPLE**. A multi-session historical adapter is required before parameter screening.
- `stocks_preus_mexc_news`: **PROMISING_UNDERPOWERED**. Strong early result, but only a few sessions and a long-heavy sample.
- `stocks_residual_momentum`: **PROMISING_BUT_CONCENTRATED**. Positive development and validation, but trade count and concentration fail selection gates.
- `stocks_pead_long`: **REJECT_VALIDATION_FAILURE**. The frozen development winner failed the next calendar year.
- `stocks_pead_short`: **REJECT_NO_GRID_EDGE**. Every preregistered short profile was negative.
- `stocks_technical_fvg_reclaim`: **REJECT_NO_GROSS_EDGE**. The best profile lost before costs; the sealed holdout was correctly left unopened.
- `stocks_position_swing_v2_historical`: **UNDERPOWERED_NO_EDGE_YET**. Exact screening is near flat; pullback is weak and breakout has only one close.

### Pre-US robustness check

- Positive sessions: `6/7`.
- Best session share of net PnL: `0.55`.
- Net PnL after removing the best session: `$231.40`.
- Top-five symbol share of positive profit: `0.75`.
- The result survives removal of its best day, but the sample is still only seven sessions and all long.

Score-threshold sensitivity is in-sample diagnostic only:

| Minimum score | Closed | Net USD | PF |
|---:|---:|---:|---:|
| 65 | 22 | 518.21 | 2.37 |
| 70 | 20 | 590.89 | 2.93 |
| 75 | 17 | 483.45 | 2.67 |
| 80 | 14 | 366.12 | 2.63 |
| 85 | 11 | 335.54 | 3.06 |
| 90 | 10 | 340.43 | 3.16 |

### Residual-momentum period check

| Period | Closed | Net USD | PF | Win rate |
|---|---:|---:|---:|---:|
| Development 2020-2023 | 70 | 309.25 | 1.53 | 0.51 |
| Validation 2024 | 18 | 204.36 | 2.87 | 0.67 |
| Known audit 2025-2026 | 17 | 154.56 | 2.36 | 0.65 |

The sign is positive in all three periods, but validation/audit are small and not fully sealed.

## News and Enriched Review

- Canonical stock news rows: `67985` from `2026-07-19T10:30:00-04:00` to `2026-08-18T22:58:28+00:00`.
- Causal pre-US reviews: `217/217`.
- Current stock Paper exits with a non-empty catalyst label: `7/264`.

News is causally timestamped and materially participates in event strategies. The current technical-Paper exit sample has inadequate catalyst-label coverage, so a reliable news-vs-no-news PnL claim cannot yet be made. Enriched review is mostly neutral/caution and has too few closed outcomes for an incremental-PnL claim.

### Closed Pre-US PnL by review verdict

| Verdict | Closed | Net USD |
|---|---:|---:|
| NEUTRAL | 13 | 444.37 |
| CAUTION | 6 | 6.58 |
| INSUFFICIENT_DATA | 3 | 67.27 |

### Raw technical controls by causal news state

| News state at decision | Closed | Net USD | PF | Win rate |
|---|---:|---:|---:|---:|
| NO_FRESH_NEWS | 471 | -273.20 | 0.92 | 0.54 |
| POSITIVE_CONFIRMED | 3 | 12.40 | n/a | 1.00 |
| UNKNOWN_OR_STALE | 25 | -287.09 | 0.13 | 0.32 |

## Strict next stage

1. Stop PEAD, technical FVG reclaim and raw intraday variant tuning.
2. Continue exact production breakout/pullback forward collection; do not pool raw controls.
3. Expand residual-momentum universe/history and test concentration controls.
4. Keep Position V2 parameters frozen: its new exact historical screen is near flat and underpowered.
5. Keep pre-US MEXC unchanged while accumulating more sessions; validate event and direction slices.
6. Keep Catalyst RS and Earnings Gap in evidence collection; their current historical event window is too short.
7. Continue forward materialization of point-in-time news-state labels; the first causal ablation is underpowered.