# Earnings Risk

[src/stocks/agents/earnings_risk_agent.py](../../src/stocks/agents/earnings_risk_agent.py) reads the merged earnings calendar (manual CSV + yfinance) and tags each symbol with severity.

## Severity levels

- **active** — earnings today (days_ahead ≤ 0)
- **next_session** — earnings tomorrow (days_ahead = 1)
- **this_week** — 2 ≤ days_ahead ≤ 5
- **safe** — ≥6 trading-ish days out
- **unknown** — no calendar entry available

## Mode-specific rules (config/stocks/risk.yaml → earnings)

### intraday
- Do NOT block trading around earnings — but flag every active/next_session symbol as **high_risk_warning**.
- Require explicit acknowledgement in the thesis ("I am intentionally trading the earnings reaction").

### swing
- **Block** new entries if `days_ahead ≤ 2`.
- Downgrade `this_week` setups unless the user invokes an explicit "earnings swing" strategy.

### invest
- Block only on the actual event day. Invest mode tolerates a single earnings event (long-term thesis dominates).

## Hard-block flow

When earnings hit the blocking threshold for the active mode, `EarningsRiskAgent` writes `blocks_swing` (or analogous). `StockRiskAgent` propagates that to its `blocks` list, which forces `StockScoringAgent` to tag the trade as **rejected** regardless of score.

## Manual override

If yfinance doesn't have a date you trust, add a row to `data/manual/stocks/earnings_calendar.csv`:

```
2026-05-28,NVDA,AMC,0.59,28500000000,Q1 FY27
```

Manual entries win on `(date, symbol)` collisions with yfinance.

## Why this matters

Holding a swing through earnings turns the thesis into a coin flip — the post-earnings gap routinely exceeds 2 ATR, blowing through any technical stop. The system is intentionally pessimistic about this and would rather miss the move than blindly hold the lottery ticket.
