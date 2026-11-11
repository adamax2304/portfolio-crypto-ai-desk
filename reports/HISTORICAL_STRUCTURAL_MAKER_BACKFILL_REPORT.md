# HISTORICAL STRUCTURAL + MAKER-FIRST BACKFILL (PART 8)

**Scope:** PAPER ONLY. Derived ledgers; `signal_outcomes.final_r` untouched.
Date: 2026-06-24. Universe: 587 deduped actionable paper trades.

## A vs B — final equity by fee profile ($5000 start, 0.5% risk, max-2x sizing both)

| fee profile | A mech+taker $ | A ret% | B struct+maker $ | B ret% | A fees | B fees | B skip | B maker fills |
|---|---|---|---|---|---|---|---|---|
| zero (no-cost) | 7429.59 | +48.59% | 7429.59 | +48.59% | 0 | 0 | 0 | 177 |
| **bybit_non_vip_usdt_perp** | 5185.91 | **+3.72%** | **5409.39** | **+8.19%** | 1763 | 1585 | 0 | 177 |
| mexc_default_futures | 5855.93 | +17.12% | 5998.80 | +19.98% | 1240 | 1125 | 0 | 177 |
| conservative_taker | 4754.69 | −4.91% | 4963.36 | −0.73% | 2098 | 1892 | 2 | 177 |

(custom_account_override is configurable per-account; not run here.)

## Read
- **Maker-first is the decisive lever** on the fee-fragile profiles: Bybit +4.47pp,
  MEXC +2.86pp, conservative +4.18pp. The no-cost ceiling (+48.59%) is unchanged —
  confirming the edge exists pre-fee and the work is fee-survival.
- **Conservative profile is still net-negative** (−0.73%) even with maker-first —
  i.e. on a punitive taker-heavy account the strategy does not clear costs. Bybit
  non-VIP with maker-first is the realistic viable path.
- Fee drag skips: **2** (conservative only). The 2x-sized notionals rarely exceed
  0.35R fee cost on Bybit/MEXC.

## Coverage / honesty
- **Structural TP labels in the backfill are `STRUCTURAL_FALLBACK_ATR`** because the
  historical replay has no per-trade OHLCV slice; the structural swing/range/VP engine
  is active on the **forward** path (live candles). The backfill therefore measures
  the **maker-first + fee-aware + 2x** economics on the Model-F R base — the
  economically decisive levers — not a re-walk against different structural TP levels.
- maker_missed = 0 under the conservative fill model (assumes the limit was touched
  again); the forward path will record real misses.

## Comparison artefacts
`data/research/structural_maker_comparison_2026-06-24.csv`,
`data/research/paper_portfolio_equity_curve_2026-06-24.csv`,
`data/research/paper_portfolio_ledger_2026-06-24.csv`.
Ledger: 5 profiles × 587 rows (incl. `bybit_structural_maker_first`).

## Verdict
**HISTORICAL_STRUCTURAL_MAKER_BACKFILL_COMPLETE**
