# Backtest — Execution Cost Model (PART 8)

**Date:** 2026-06-11 · **Used by:** `scripts/replay_signal_execution.py` (`--include-fees`, `--include-slippage`).

This document is the source of truth for the assumptions used to convert raw R into a fees/slippage-adjusted R. All values are explicit and conservative. No paid APIs, no new external dependencies.

---

## 1. Crypto

### 1.1 Trading fees
| Component | Default | Source |
|---|---|---|
| Taker fee | **5 bps per side** (0.05%) | Binance retail spot fallback (BNB-paid discounted rate higher; we use the no-BNB conservative number) |
| Maker fee | **2 bps per side** (0.02%) | Same source. Not currently used by the replay (treats fills as taker by default). |
| Round-trip taker | **10 bps** | 2 × 5 bps |

### 1.2 Slippage
| Component | Default | Notes |
|---|---|---|
| Slippage on entry | **5 bps** | absorbs spread + price drift between decision and fill |
| Slippage on exit | implicit in 5 bps already (round-trip total) | |
| Thin/MEXC penalty | **+10 bps** | applied when `primary_exchange == 'mexc'` OR `data_confidence == 'low'` |

### 1.3 Spread proxy when orderbook not stored
- Use **last 5 candles' (high-low)/close** average as a proxy for typical intracandle range; if this exceeds **30 bps**, mark the symbol `thin_alt` and add +10 bps penalty.
- The replay does not currently load this proxy (kept simple); the **thin_alt penalty is triggered only via `primary_exchange == 'mexc'` or `data_confidence == 'low'`** until a per-symbol spread metric is added.

### 1.4 Funding cost (short positions)
- If a short is held over a funding timestamp (every 8h on Binance/Bybit), deduct `funding_rate × position_size` from R.
- **Current limitation:** historical funding archive is `latest-cache only` — no time series. We therefore do NOT add a funding cost in the replay and **explicitly flag this as an approximation**. Funding can be -3 bps to +30 bps per 8h on alt-coins; a short held 24h could easily eat 0.05–0.20 R worth of cost.
- Marking: `notes` field will say `funding_cost_unknown` if a short is held > 8h after entry.

### 1.5 Symbol-bucket modifier
- `quote_volume` bucket (24h):
  - > $500M → no extra penalty
  - $50M – $500M → +2 bps
  - $5M – $50M → +5 bps
  - < $5M → +15 bps and flag `thin_alt_high_risk` for live-trading prohibition
- The replay does not currently compute this — symbols are pre-filtered to liquid pairs upstream. For LIVE, this gate MUST be re-checked at runtime.

---

## 2. Stocks

### 2.1 Commissions
- $0 commission per side (Robinhood / IBKR Lite / Fidelity default). Round-trip = $0.

### 2.2 Slippage
| Component | Default | Notes |
|---|---|---|
| On 15m fills (RTH) | **±$0.02 per share** (~2 bps on $100 stock) | conservative for liquid names; tight names like AAPL/NVDA see ≤ $0.01 |
| On gap fills (open after a halt or overnight gap > 1%) | mark **lower-confidence** | replay uses gap candle's open price as fill, but the fill is unrealistic for retail without paying spread; flag in `notes` |

### 2.3 Market hours
- Replay only fills inside RTH (09:30–16:00 ET).
- Premarket / after-hours fills are **NOT supported** in this pass and are explicitly out of scope.
- If a signal's `created_at` is in premarket and the entry zone is touched before 09:30, the entry is deferred to the 09:30 open (using the open price), with a `gap_slip` flag.

### 2.4 Earnings gap risk
- Stocks holding overnight through an earnings release: replay marks **lower-confidence** and does not assume the entry / TP / stop are honored.

---

## 3. How the replay applies the model

```python
if asset_class == "crypto":
    bps_round_trip = 10  # taker
    if include_slippage:
        bps_round_trip += 5  # entry slippage
    if primary_exchange == "mexc" or data_confidence == "low":
        bps_round_trip += 10  # thin penalty
    cost_per_unit_price = entry_price * bps_round_trip / 10000.0
    fees_r = -cost_per_unit_price / risk_per_unit

elif asset_class == "stocks":
    slip_usd = 0.02 if include_slippage else 0
    fees_r = -slip_usd / risk_per_unit
```

`fees_r` is added to `replay_raw_r` before sizing.

---

## 4. What this model deliberately under-counts (live-trading buffer)

| Item | Direction | Why it's intentionally not modeled |
|---|---|---|
| Short funding on multi-day shorts | OUT of replay | no historical funding archive; live exec must re-cost |
| Borrow fees for stocks shorts | OUT | retail short borrow varies wildly; cannot snapshot |
| Realized slippage on stop-runs in fast markets | UNDER | the 5 bps assumption holds only in normal vol |
| Live latency / cancel-replace | OUT | replay is a snapshot, not a simulator of order flow |
| Tax drag | OUT | strategy-level decision, not a backtest concern |

**Net effect:** the replay's `fees_slippage_r_adjustment` is a **floor on cost, not a worst case**. The live readiness verdict in [LIVE_READINESS_FROM_BACKTEST.md](LIVE_READINESS_FROM_BACKTEST.md) explicitly buffers for this.

---

## 5. Sensitivity table (back-of-envelope)

| Doubling cost assumption | Effect on portfolio sized R |
|---|---|
| 10 bps crypto round-trip → 20 bps | crypto cohort loses ~0.05 R per trade × n_crypto_trades. With 130 crypto signals: ~−6.5 R. |
| Stocks slippage $0.02 → $0.05 | stocks cohort loses ~0.03 R per trade × 1340: ~−40 R. **Materially erodes the cohort.** |
| MEXC penalty +10 → +25 bps | adds ~−0.05R per MEXC trade. Effect bounded by MEXC trade share. |

The stocks slippage assumption is the **biggest sensitivity** in this model. The live readiness verdict treats stocks as MORE fragile than crypto for this reason.
