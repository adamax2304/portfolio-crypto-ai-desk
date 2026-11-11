# 48h Trade Universe Snapshot (PART 2)

**Window:** 2026-06-08 12:10 UTC → 2026-06-10 12:10 UTC. Read-only deduped extract.
**Full per-signal data:** [`TRADE_UNIVERSE_48H_AFTER_RECENT_FIXES.csv`](TRADE_UNIVERSE_48H_AFTER_RECENT_FIXES.csv) (313 rows × 40 columns).

## 1. Top-level rollup

| Bucket | n |
|---|---:|
| **Total signals** | **313** |
| Asset: crypto | 33 |
| Asset: stocks | 280 |
| Tier A | 5 |
| Tier B | 85 |
| Tier C | 223 |
| Mode: scalp | 13 |
| Mode: intraday | 140 |
| Mode: swing | 82 |
| Mode: invest | 78 |

## 2. By status (live)

| Status | n |
|---|---:|
| triggered | 69 |
| stopped | 85 |
| tp1_hit | 18 |
| tp2_hit | 8 |
| tp3_hit | 6 |
| expired | 11 |
| missed_no_entry | 32 |
| waiting_for_entry | 38 |
| **stale_before_entry** (revalidator) | **38** |
| **entry_moved_away** (revalidator) | **8** |

## 3. By final outcome (signal_outcomes)

| Outcome | n |
|---|---:|
| win | 32 |
| loss | 85 |
| expired | 80 |
| not_triggered | 34 |
| pending | 82 |

## 4. By playbook (label_for routing)

| Playbook | n |
|---|---:|
| `stocks_intraday_rth_momentum` | 102 |
| `stocks_invest_watchlist_30d_thesis` | 78 |
| `crypto_swing_narrative_rs_momentum` | 14 |
| `crypto_scalp_momentum_continuation` | 13 |
| `crypto_intraday_catalyst_or_momentum` | 5 |
| `crypto_failed_bounce_short` | 4 |
| (stocks_swing → all C-tier under pause) | included in the 280-stocks bucket |

## 5. CSV columns (all 40)
`signal_id, asset_class, symbol, playbook, mode, tier, direction, score, created_at, expires_at, status, entry_low, entry_high, entry_trigger, stop_loss, invalidation, tp1, tp2, tp3, entry_triggered, entry_triggered_at, entry_price_used, stop_hit, stop_hit_at, tp1_hit, tp1_hit_at, tp2_hit, tp2_hit_at, final_outcome, final_r, mfe_r, mae_r, news_supported, ann_intrabar_entry_stop, ann_intrabar_entry_tp, ann_pre_entry_invalidation, ann_gap_slip_stop, ann_gap_slip_tp, revalidator_note, outcome_notes, cap_reasons_str, source_report_path, tv_link`

## 6. Splits
- **Crypto A/B**: B=33 (no A in window). Spread across scalp / intraday / swing.
- **Crypto C/watchlist**: stocks_swing/invest C-tier sit under their pause gates; crypto C-tier are watchlist-only outputs from the existing pipeline.
- **Stocks A/B**: A=5, B=44 (intraday). All swing/invest A/B prevented by gates (post-pause: 0 stocks-swing A/B leaks; some stocks-intraday A-tier from the earlier window remain).
- **Stocks C/watchlist swing/invest**: separately tracked — 78 invest + ~9 swing C-tier (per playbook breakdown).

## 7. Use this CSV
The CSV is the input for PART 3 (playbook performance), PART 4 (TBT), PART 5 (pending), PART 6 (execution accuracy). Each downstream report filters or aggregates this single source of truth.
