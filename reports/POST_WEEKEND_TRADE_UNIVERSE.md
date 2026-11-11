# Post-Weekend Trade / Signal Universe (72h)

**As of:** 2026-06-07 (Sun) · deduped unique setups from `proposed_signals` +
latest `signal_outcomes`. Full per-signal columns (signal_id, asset_class,
symbol, mode, direction, tier, score, created_at, entry, stop, TP1/TP2/TP3,
status, outcome, R, MFE_R, MAE_R, telegram_sent, news_supported, cap_reasons,
capped, source_report) → **`POST_WEEKEND_TRADE_UNIVERSE.csv`** (194 rows).

## Counts
| Class / tier | n |
|---|---|
| **Crypto A/B** | 46 (all B-tier; 0 A; 0 C) |
| Crypto C watchlist | 0 |
| **Stocks A/B** | 53 |
| Stocks C watchlist | 95 |
| **Total** | 194 |

## By mode (A/B)
| asset / mode | n | triggered |
|---|---|---|
| crypto scalp | 28 | 18 |
| crypto intraday | 15 | 12 |
| crypto swing | 3 | 3 |
| stocks intraday | 30 | 22 |
| stocks swing (watchlist-only, pre-fix residual) | 14 | 14 |
| stocks invest | 9 | 3 (6 waiting) |

## Gate / cap-reason tally (72h, all tiers)
| count | cap_reason |
|---|---|
| 48 | market_closed_intraday_planning_only |
| 34 | tier demoted B→C |
| 9 | legal_headline_risk |
| 2 | tier demoted A→C |
| 2 | stocks_swing_paused_after_48h_audit (post-fix) |
| 1 | extreme negative funding against short |

Notes: crypto produced **only B-tier** A/B this window (no A-tier crypto — the
funnel stayed conservative in a risk-off tape). Stocks C-tier (95) is large
because the market-closed + B→C demotions route weekend/closed intraday setups
to watchlist. See CSV for full detail.
