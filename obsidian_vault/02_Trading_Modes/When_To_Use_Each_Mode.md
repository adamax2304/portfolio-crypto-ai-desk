# When To Use Each Mode

A practical decision guide.

## Decision tree

```
1. Do you intend to be in the position for < 2 hours?
   → scalp
2. Do you intend to be in the position for 4–24 hours?
   → intraday
3. Do you intend to be in the position for 2–7 days?
   → swing
4. Anything longer?
   → not supported by this desk; see [[Long_Term_Mode]]
```

## When NOT to use each mode

- **Scalp**: weekend off-hours, news windows (CPI/FOMC), `high-volatility danger` regime, < $20k recent candle quote volume.
- **Intraday**: data is older than 3h (auto-rejected anyway), no clear 1h structure, BTC in vertical whipsaw.
- **Swing**: 48h before a known unlock for the symbol's project, narrative cooling rapidly, BTC regime flipped against the trade.

## How to overlay modes

You can hold:

- A swing position **and** scalp inside it for liquidity / re-entry — but treat the two as separate book entries.
- An intraday trade **and** a watchlist note on a longer-term swing — but never blend the invalidation levels.

You should not:

- Open a "scalp that becomes swing" — that is a stop-loss-extension lie. Pick one mode, honor it.
- Use scalp scoring as a swing pre-screen — the multipliers are wrong.

## Mode-by-context cheatsheet

| Market context | Best mode | Why |
|---|---|---|
| Bull trend day, BTC making higher lows | intraday | Highest hit rate; trend respects intraday structure |
| Fast news rotation, frequent 1–2% moves | scalp | Momentum and execution multipliers reward this |
| Sector narrative heating over 3+ days | swing | Narrative + catalyst weighting active |
| Chop / consolidation | intraday with cap | Execution × 1.20 lifts mean-reversion setups |
| Vertical move, ATR percentile breaking 80 | none (no trade) | High-vol-danger regime overrides |

## Related

- [[Trading_Modes_Overview]]
- [[Mode_Selection_Logic]]
- [[Pre_Trade_Checklist_For_LLM]]

## Implemented status

- **Implemented** (informational page; rules align with code behavior).
