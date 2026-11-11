# PRE — Safe Guardrails & Catalyst-Fix Baseline (PART 0)

**Date:** 2026-06-17 · **Mode:** read-only snapshot before any change in this stage.
**Scope reminder:** diagnostics + alert-only/shadow-only labels + one catalyst *label* bug fix. No live, no scalp enable, no TP/SL/scoring/threshold/cap-value change, no force-close, no historical mutation, no production block. Control Plane untouched.

## Data sources (read-only)
| Source | Value |
|---|---|
| Primary DB | `db/crypto_ai_desk.sqlite` — **1,526 MB**, opened `mode=ro` (live, actively written) |
| Scalp history DB | `db/scalp_history.sqlite` — 234 MB (not modified) |
| Audit dataset | `reports/LAST_3_7D_TRADE_AND_SHADOW_AUDIT_DATASET.csv` — **558 rows** (last 7d), rebuilt via `reports/audit_3_7d.py 7` |
| OHLCV | `data/raw/ohlcv/{binance,bybit,mexc}/{1m..1d}/SYM_USDT.csv` |
| Catalyst artifacts | `data/catalysts/2026-06-13 … 2026-06-17/` |

## Table counts (baseline)
| Table | Rows |
|---|---|
| `proposed_signals` | 2,017 |
| `signal_outcomes` | 152,994 |
| `signal_alerts` | 1,220 |
| `news_items` | 15,854 |
| `signal_catalyst_labels` | 1,016 |

## news_items integrity snapshot (feeds PART 1)
| Metric | Value |
|---|---|
| Total rows | 15,854 |
| Symbol-tagged (`detected_symbols_json` nonempty) | 3,052 |
| High-importance (≥1.0) **and** symbol-tagged | 2,738 |
| High-importance symbol-tagged, last 24h | 250 |
| Symbol column present | `detected_symbols_json` only (**no legacy `detected_symbols` column**) |

## Last-7d trade universe (558 rows, from dataset)
- Triggered (entry filled): used as the basis for all PART 2–6 counterfactuals.
- Asset classes: crypto + stocks; modes scalp/intraday/swing/invest.
- Fields available per row: signal_id, symbol, asset_class, mode, tier, direction, created_at, entry_triggered_at, stop, tp1/2/3, status, final_outcome, exit_at, result_R, mfe_r, mae_r, time_to_stop_h, held_hours, overnight_carried, freshness_label, shadow_reason, concentration_status, market_regime.

## Known-state carried from prior audit (still valid, not re-derived here)
- Recent crypto losses ≈ exit-management (tight stops + no profit protection), not bad entries.
- No engine-level circuit breaker exists.
- `concentration_status` set **0× live** → sector cap suspected inert on the live path.
- Regime label lagged the 06-16/06-17 intraday turn.

## Guardrail acknowledgement
This baseline establishes the read-only starting point. Everything produced in PARTS 2–9 is a report / CSV / test / add-only field / alert-or-shadow label, plus the single PART 1 catalyst **label** fix (already landed; see PART 1 reports). No production behavior was changed by this stage.
