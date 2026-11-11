# Old Paper vs New Logic Shadow — Underperformance Diagnostic (2026-07-12T17:21:41.271230+00:00)

> Audit item #3. No trading-logic, TP/SL, entry, routing, scoring, or Model F changes. Live/auto-live/manual-live remain locked; signal_outcomes/final_r untouched. Compares the two PAPER SHADOW branches in `paper_shadow_execution_outcomes` (old_paper vs new_logic_shadow) — NOT the production paper book (`paper_execution_outcomes` / Model F), which is untouched here. This module itself writes nothing to the database; the CLI command that generates this report additionally re-runs entry_mode_calibration.refresh() first by default (writes ONLY the entry_mode_calibration_* read-model tables, never a trading table) — run with `--no-refresh-source` for a strictly read-only pass.

## Expiry-aware entry-fill fix — before/after
_paper_shadow_engine now blocks any entry fill past the signal's own validity window (expires_at, else created_at+validity_window_hours, else the mode default: scalp=2h/intraday=24h/swing=168h/invest=720h) instead of silently accepting a late fill. Old late-fill rows are NOT clean evidence — they never should have been 'filled'._
- **before** the expiry-aware rebuild: 847 filled rows checked, **157** filled AFTER their own validity window (by mode: {'swing': 48, 'scalp': 46, 'intraday': 63})
- **after** the rebuild: **441** rows now correctly classified `entry_late_status=after_expiry_blocked` (never 'filled') (by mode: {'intraday': 189, 'scalp': 187, 'swing': 65})
- all PnL/exit-cause/fee numbers below already reflect the post-fix data (blocked rows are `entry_fill_status='missed'`, so `_is_filled()` excludes them from executed_common automatically — no separate re-filtering needed in this report).

## Evidence quality
- forward_since_activation pairs: **501** (executed_common=79, Σdelta_usd=-203)
- historical_backfill pairs: **345** (executed_common=5, Σdelta_usd=-60) — hypothesis/context only. Not parameter-overfit the way Model F's thresholds were (old_paper/new_logic_shadow are fixed, pre-specified logic, not backfill-tuned), but still not accumulated live experience — see the forward-only cross-check section before treating any pattern as proven.
- Tables below combine both windows for statistical power unless labeled forward-only.

## Headline (all windows)
- old_paper: net $257 / 10.27R over 84 common executed trades (WR 42%, PF 1.21)
- new_logic_shadow: net $-6 / -0.26R (WR 56%, PF 0.99)
- **delta (new − old): $-263** (new better 20 / old better 44 / flat 20)
- with-skips-or-avoided delta (unfilled counted as $0): $2456 over 846 pairs — avoided_bad n=182 ($-4360), missed_good n=36 ($1641)

**Entry-latency note:** the multi-day/multi-week entry-fill gaps previously seen here were the after-expiry contamination fixed above (see 'Expiry-aware entry-fill fix') — those rows are now excluded from executed_common instead of skewing these numbers. The avg entry-latency columns below reflect only genuinely-valid, in-window fills.

## Ranked by asset_class × mode — where old_paper loses most (worst first, all windows)
| asset/mode | n | old $ | new $ | delta $ | old/new R | old/new WR | old/new PF | old/new avg fee $ | old/new avg entry-latency min | avg data-gap min |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| crypto/swing | 44 | 26 | -137 | -163 | 1.02 / -5.49 | 34% / 50% | 1.04 / 0.76 | 1.62 / 2.28 | 47.2 / 32.2 | - |
| crypto/scalp | 19 | 194 | 101 | -93 | 7.75 / 4.05 | 63% / 68% | 2.04 / 1.63 | 1.32 / 1.60 | 80.7 / 77.8 | - |
| crypto/intraday | 21 | 37 | 30 | -8 | 1.49 / 1.19 | 38% / 57% | 1.11 / 1.11 | 2.16 / 2.57 | 161.6 / 128.7 | - |

## By entry_mode
| entry_mode | n | old $ | new $ | delta $ | old/new R | old/new WR | old/new PF | old/new avg fee $ | old/new avg entry-latency min | avg data-gap min |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| BREAKOUT_CONTINUATION | 44 | -105 | -297 | -193 | -4.19 / -11.89 | 32% / 50% | 0.86 / 0.52 | 2.10 / 2.74 | 54.6 / 20.3 | - |
| PULLBACK_LIMIT | 19 | 542 | 423 | -119 | 21.69 / 16.93 | 84% / 90% | 9.75 / 8.81 | 1.06 / 1.25 | 215.5 / 215.5 | - |
| MOMENTUM_TAKER_NOW | 4 | 46 | 21 | -25 | 1.85 / 0.84 | 50% / 50% | 1.90 / 1.59 | 0.78 / 1.39 | 112.5 / 18.8 | - |
| STRUCTURAL_RETEST | 2 | 47 | 62 | 15 | 1.87 / 2.47 | 50% / 100% | 6.31 / inf | 1.86 / 6.68 | 8.2 / 248.2 | - |
| LIMIT_THEN_TAKER_TIMEOUT | 15 | -274 | -215 | 58 | -10.95 / -8.61 | 13% / 27% | 0.21 / 0.27 | 1.48 / 1.45 | 2.6 / 2.6 | - |

## By authoritative fee_profile
| fee_profile | n | old $ | new $ | delta $ | old/new R | old/new WR | old/new PF | old/new avg fee $ | old/new avg entry-latency min | avg data-gap min |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| bybit_non_vip_usdt_perp | 84 | 257 | -6 | -263 | 10.27 / -0.26 | 42% / 56% | 1.21 / 0.99 | 1.69 / 2.20 | 83.4 / 66.6 | - |

## By session bucket (UTC, entry_fill_time else signal created_at)
| session | n | old $ | new $ | delta $ | old/new R | old/new WR | old/new PF | old/new avg fee $ | old/new avg entry-latency min | avg data-gap min |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| us | 21 | 60 | -61 | -122 | 2.41 / -2.46 | 43% / 48% | 1.19 / 0.79 | 1.94 / 2.48 | 60.7 / 33.6 | - |
| europe | 11 | 168 | 80 | -88 | 6.73 / 3.20 | 64% / 82% | 2.87 / 2.44 | 1.79 / 2.44 | 240.0 / 200.0 | - |
| asia | 46 | 51 | -18 | -69 | 2.06 / -0.72 | 37% / 54% | 1.07 / 0.97 | 1.51 / 2.01 | 56.3 / 50.0 | - |
| off | 6 | -23 | -7 | 16 | -0.93 / -0.28 | 33% / 50% | 0.78 / 0.91 | 1.95 / 2.23 | 83.1 / 65.6 | - |

## Data-quality (DATA_GAP_LATE / clean status)
| data_coverage_status | n | old $ | new $ | delta $ | avg gap min |
|---|--:|--:|--:|--:|--:|
| unknown | 84 | 257 | -6 | -263 | - |

## Exit-cause matrix (common executed trades only, all windows)
_protective_stop = stop hit after moving to BE/lock favorably; original_stop = stop hit before any favorable move; expired_win/expired_flat by net_r sign at expiry._

| old exit | new exit | n | Σdelta $ |
|---|---|--:|--:|
| win | no_entry | 22 | -1363 |
| win | protective_stop | 9 | -285 |
| win | win | 10 | -166 |
| expired_win | no_entry | 8 | -163 |
| protective_stop | no_entry | 6 | -114 |
| expired_win | protective_stop | 6 | -95 |
| expired_win | expired_win | 7 | -40 |
| protective_stop | protective_stop | 1 | -15 |
| win | expired_win | 1 | -8 |
| expired_flat | expired_flat | 6 | 0 |
| expired_win | win | 1 | 2 |
| original_stop | original_stop | 37 | 6 |
| expired_flat | no_entry | 543 | 64 |
| original_stop | protective_stop | 12 | 338 |
| original_stop | no_entry | 177 | 4296 |

## Entry-fill-status matrix (filled / missed / skipped / invalid / no_entry)
| old status | new status | n | Σdelta $ |
|---|---|--:|--:|
| filled | filled | 84 | -263 |
| missed | missed | 6 | 0 |
| missed | skipped | 538 | 0 |
| filled | missed | 6 | 164 |
| filled | skipped | 212 | 2555 |

## Chase / late-entry attribution (NO_CHASE_SKIP)
_new_logic_shadow's entry_mode_classifier skips entries that are too extended with no continuation structure; old_paper's mechanical pullback-limit entry has no such gate and always fills. This isolates exactly that chase-avoidance from the broader avoided_bad bucket above._
- all windows: 4 chase-flagged pairs — old_paper losses avoided: n=1 ($-10); old_paper wins also missed: n=2 ($65)
- forward-only: 4 chase-flagged pairs — losses avoided n=1 ($-10); wins also missed n=2 ($65)

## Fee / cost attribution (executed_vs_executed, authoritative fee_profile only)
| slice | old avg fee+slip $ | new avg fee+slip $ | Σfee delta (old−new) $ | old ΣgrossR | old ΣnetR | new ΣgrossR | new ΣnetR |
|---|--:|--:|--:|--:|--:|--:|--:|
| crypto/swing | 1.62 | 2.28 | -29.41 | 3.87 | 1.02 | -1.47 | -5.49 |
| crypto/scalp | 1.32 | 1.60 | -5.16 | 8.76 | 7.75 | 5.26 | 4.05 |
| crypto/intraday | 2.16 | 2.57 | -8.69 | 3.30 | 1.49 | 3.35 | 1.19 |

## Top 10 worst signal_ids (old_paper loses most vs new_logic_shadow)
| signal_id | asset/mode | entry_mode | window | delta $ | delta R | old close | new close |
|---|---|---|---|--:|--:|---|---|
| sig_23b972d7fbe54246 | crypto/swing | BREAKOUT_CONTINUATION | forward_since_activation | -64 | -2.57 | closed_win | stop |
| sig_78d17d3bc9071af9 | crypto/scalp | PULLBACK_LIMIT | forward_since_activation | -46 | -1.83 | closed_win | stop |
| sig_ce787d0def004a28 | crypto/swing | PULLBACK_LIMIT | historical_backfill | -46 | -1.82 | closed_win | stop |
| sig_a938871d7ad64082 | crypto/swing | BREAKOUT_CONTINUATION | historical_backfill | -40 | -1.61 | closed_win | stop |
| sig_a28b867ca5ba84a1 | crypto/swing | LIMIT_THEN_TAKER_TIMEOUT | historical_backfill | -40 | -1.60 | closed_win | stop |
| sig_6c6c6598dd4c9fbe | crypto/intraday | MOMENTUM_TAKER_NOW | forward_since_activation | -38 | -1.54 | expired_exit | stop |
| sig_99493b9211f0f4f3 | crypto/scalp | BREAKOUT_CONTINUATION | forward_since_activation | -38 | -1.52 | closed_win | closed_win |
| sig_6dcf39daee5bf433 | crypto/swing | BREAKOUT_CONTINUATION | historical_backfill | -38 | -1.50 | closed_win | stop |
| sig_261bc475fb76be71 | crypto/scalp | LIMIT_THEN_TAKER_TIMEOUT | forward_since_activation | -36 | -1.45 | closed_win | closed_win |
| sig_38bd1d72c28b48b8 | crypto/intraday | PULLBACK_LIMIT | forward_since_activation | -32 | -1.28 | closed_win | closed_win |

## Top 10 best signal_ids (old_paper beats new_logic_shadow)
| signal_id | asset/mode | entry_mode | window | delta $ | delta R | old close | new close |
|---|---|---|---|--:|--:|---|---|
| sig_f5829c4313e35c37 | crypto/intraday | PULLBACK_LIMIT | historical_backfill | 87 | 3.47 | stopped_full | stop |
| sig_a38c868327ddecd5 | crypto/intraday | BREAKOUT_CONTINUATION | historical_backfill | 74 | 2.95 | stopped_full | closed_win |
| sig_962ab484b8e89fc8 | crypto/scalp | LIMIT_THEN_TAKER_TIMEOUT | forward_since_activation | 58 | 2.31 | stopped_full | stop |
| sig_6c1288b8c2e6cdf4 | crypto/swing | PULLBACK_LIMIT | historical_backfill | 55 | 2.19 | closed_win | stop |
| sig_5ab487090badb13c | crypto/swing | PULLBACK_LIMIT | historical_backfill | 43 | 1.71 | stopped_full | stop |
| sig_14191573ca883e84 | crypto/swing | LIMIT_THEN_TAKER_TIMEOUT | historical_backfill | 39 | 1.56 | closed_win | closed_win |
| sig_facfccb70d53f45e | crypto/intraday | LIMIT_THEN_TAKER_TIMEOUT | forward_since_activation | 37 | 1.47 | stopped_full | stop |
| sig_a0f209551a0173f7 | crypto/intraday | BREAKOUT_CONTINUATION | forward_since_activation | 34 | 1.35 | stopped_full | stop |
| sig_0ce565596ac4a12c | crypto/swing | BREAKOUT_CONTINUATION | forward_since_activation | 34 | 1.34 | stopped_full | stop |
| sig_af30c07a9200d268 | crypto/intraday | BREAKOUT_CONTINUATION | historical_backfill | 33 | 1.34 | stopped_full | stop |

## Forward-only cross-check
_The same headline numbers, restricted to forward_since_activation pairs only — confirms whether the all-windows pattern above holds up in the (currently thin) live sample._
- n=79 common executed, old $146 vs new $-58, delta $-203

## Conclusion / recommendations
_Read the numbers above before trusting this section — it is a plain-language summary, not a substitute for the tables. No production-logic changes were made or are proposed here to apply automatically; any action requires a separate, explicit change with its own review._