# Stocks Scalp Feasibility Audit (PART 8)

**Date:** 2026-06-16

## Why there is no stocks scalp mode today

The stocks pipeline was built MVP-style on **yfinance**, whose finest cached timeframe is
**15m** (`data/raw/stocks/{15m,1h,1d,1wk}`). There is **no 1m or 5m stock history** — the
tracker code says so explicitly: *"Stocks have no 5m / 4h history under MVP yfinance."*
`STOCKS_TIMEFRAME_PREFERENCE["scalp"]` exists as a placeholder but resolves to 15m, and no
stocks-scalp generation pipeline exists. So a stocks scalp mode has simply never had the
sub-15m data or geometry to run.

## Current stocks intraday config (the baseline a scalp mode would compress)

| Aspect | Current value |
|--------|---------------|
| Timeframe | **15m** (→ 1h → 1d fallback) |
| Generation | report cycle (2h); tracked at 2h `track-signals`; monitored every 10 min RTH |
| Geometry | same ATR-zone model as crypto (entry zone, stop ≈ 1R, TP1/2/3) |
| RTH gates | stocks monitor runs only during US regular session |
| Earnings | intraday: trade reaction but flag; swing: block ≤2d; invest: block event-day |
| Legal/news | verified-source-for-A-tier, reject rumor-only, discount priced-in (0.5×) |
| Liquidity | min $25M 30d ADV, min price $5, reject rel-vol < 0.5 |
| Confirmation | index-contradicts → cap B; sector-contradicts → cap C; both → reject |
| Structure | require invalidation for A/B, RR-to-TP1 ≥ 1.5, reject if > 2 ATR from entry |
| Gaps | retest required > 5% gap; reject chase > 10% gap |
| Current expired rate | **highest in system** — 87% of all expiries; ~49% no-fill / ~51% flat (PART 6) |
| Current latency | `very_late` (~135 min median, structural — PART 2) |
| Spread / commission / slippage | **not modeled** — paper R is computed from price levels with **zero fees** |

## Is a stocks scalp mode theoretically viable?

**Low feasibility / not justified to build now.** Reasons:

1. **Crypto scalp precedent.** A 12-month, 139k-trade backtest of crypto scalp on the
   *cheapest, most liquid, 24/7* venue was **net-negative after fees** (WR 43% / PF 0.63 /
   avg −0.466R; root cause = cost vs tight ATR distance). Stocks have a **worse** cost
   structure, so the prior is strongly negative.
2. **Higher costs on stocks:** commissions (even if $0 at retail, payment-for-order-flow
   spread), wider relative bid/ask on non-mega-caps, and **slippage on tight scalp stops** —
   exactly the lever that sank crypto scalp.
3. **RTH-only opportunity loss:** ~6.5h/day vs crypto 24/7 → far fewer setups; overnight
   **gap risk** can blow through tight stops; **halts** on news names.
4. **PDT rule:** a pattern-day-trader account under $25k is capped at 3 day-trades / 5
   business days — scalping is structurally incompatible with small accounts.
5. **Liquidity / shorts:** shorting requires locate/borrow; many high-beta names are hard
   to borrow — asymmetric vs crypto perps.
6. **Missing inputs:** no options/OI flow currently ingested for stocks; a scalp edge would
   lean heavily on microstructure the system doesn't have.
7. **Data blocker (see PART 9):** no 1m/5m stock history, and free sources can't provide a
   *robust* 6–12-month sub-15m dataset.

## Conclusion

A stocks scalp mode should **not** be built now. If pursued, it must first clear the
**same bar crypto scalp failed**: net-positive (PF > 1) after realistic spread + commission +
slippage, in TRAIN + VALIDATION + OOS, on ≥ 6 months of 1m/5m RTH data. That data is not
currently available for free at the required length (PART 9). Stocks scalp stays
**research-only** until a backtest proves an edge.

**PART 8 status: DONE — feasibility LOW; do not build; backtest-gated like crypto scalp.**
