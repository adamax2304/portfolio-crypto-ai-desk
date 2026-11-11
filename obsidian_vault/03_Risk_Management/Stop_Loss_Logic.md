# Stop Loss Logic

From `TechnicalSetupAgent` in [src/agents/technical_setup_agent.py](../../src/agents/technical_setup_agent.py).

## Default stop construction

Given the last bar's close `c` and ATR14 `a`:

### Long setup

```
entry_low  = c - 0.65 * a
entry_high = c - 0.20 * a
atr_stop   = c - 1.2 * a
support_stop = (support - 0.15 * a) if support is not None else None

invalidation = support_stop  if support_stop is not None and support_stop > c - 1.8 * a
                            else atr_stop
```

So invalidation prefers **recent local support − 0.15 ATR** as long as it is not further than 1.8 ATR below current price. Otherwise it falls back to a clean 1.2 ATR stop.

### Short setup

Symmetric:

```
entry_low  = c + 0.20 * a
entry_high = c + 0.65 * a
atr_stop   = c + 1.2 * a
resistance_stop = (resistance + 0.15 * a) if resistance is not None else None

invalidation = resistance_stop if resistance_stop is not None and resistance_stop < c + 1.8 * a
                              else atr_stop
```

### Watchlist / no-trade

`invalidation = None`. That triggers the score cap to 50, tier=rejected.

## Targets (for reference)

```
TP1 = c ± 1.0 * a
TP2 = c ± 2.0 * a
TP3 = c ± 3.0 * a
```

Sign matches direction. R/R to TP1 is reported as `rr_to_tp1`.

## When ATR is unavailable

`TechnicalSetupAgent` emits a `no_trade` setup with `["ATR unavailable; cannot build clean invalidation."]` and the symbol auto-rejects downstream.

## How to use the stop

- The desk's stop is **bar-close based**, not wick-based. Wait for the `setup.timeframe` close past the level before exiting.
- For scalps, you may use 5m close instead of 1h close to respect the level — at your discretion; not coded.
- The stop assumes your entry was inside `[entry_low, entry_high]`. If you entered higher (chased), recompute risk from your actual entry.

## Trailing logic (not coded)

The desk does not auto-trail. Once TP1 is hit, you can manually move stop to entry (B/E) — operator decision.

## Common mistakes

- Using the wide ATR stop when local support is much closer — that bleeds R/R.
- Ignoring `setup.warnings` — they often signal "stop will likely be tested".
- Stop too tight on swing — 1.2 ATR on 1h is often too tight for a 3-day hold; use a 4h ATR mentally.

## Related

- [[Invalidation]]
- [[Risk_Reward]]
- [[ATR]]
- [[Technical_Setup_Agent]]

## Implemented status

- **Implemented** as described.
