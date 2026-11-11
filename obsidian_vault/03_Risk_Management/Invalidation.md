# Invalidation

Invalidation is the structural level whose breach means the trade thesis is dead. The desk treats it as **mandatory**.

## Hard rule

- `setup.invalidation is None` → score capped at 50 **and** −15 risk penalty **and** tier = rejected.
- A "trade" without an invalidation is not a trade in this system. It is a watch note.

## How invalidation is built

See [[Stop_Loss_Logic]]. Two pieces:

- Recent local support (long) or resistance (short) from `recent_range(frame, 20)`.
- ATR-based fallback at 1.2 ATR.

The desk picks whichever is **closer** but still beyond a small cushion (0.15 ATR).

## How invalidation is described in the report

`TradeIdeaAgent` renders:

```
{timeframe} close beyond {invalidation_value}
```

For a long in intraday, that's a 1h close below the invalidation. For a scalp, 5m or 15m close (depending on your execution discipline).

## What "invalidation" is NOT

- It is not a market-order stop you must place at exchange. The desk does not place orders.
- It is not the absolute worst-case price — wicks can pierce it; the rule is **close past it**.
- It is not a profit-trail.

## Re-evaluation after partial fill

After TP1, you may move stop to entry. This is operator discretion. The desk does not change `invalidation`.

## When invalidation is too close

If `setup.rr_to_tp1 < 1`, the desk flags `Risk/reward to TP1 is below 1R`, adds −10 penalty, and warns. This is the desk telling you the invalidation is too tight for the implied target.

## When invalidation is too far

If the move is extended (`distance_from_ema20_atr > 2.5`), the setup converts to watchlist_only and clears entry/invalidation/TPs. You should wait for a pullback before re-evaluating.

## Telegram alert handling

`WatchlistMonitor.format_alert` now includes:

```
SL: {sl_value}
```

If the trade idea exposes `setup.sl`, that wins; otherwise it falls back to `invalidation`. This was added to make sure Telegram alerts never omit the stop.

## Related

- [[Stop_Loss_Logic]]
- [[No_Trade_Conditions]]
- [[Score_Caps]]
- [[Technical_Setup_Agent]]

## Implemented status

- **Implemented**.
