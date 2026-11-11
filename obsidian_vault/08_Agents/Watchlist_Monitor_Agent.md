# WatchlistMonitor

## File

[src/agents/watchlist_monitor.py](../../src/agents/watchlist_monitor.py).

## Role

Re-evaluate C/rejected watchlist symbols on a tight cadence (default every 10 minutes) and emit Telegram alerts when a name flips to B/A.

## CLI

```
python -m src.cli monitor-watchlist --interval 600 --iterations 0 --duration-hours 0 --dry-run
```

- `interval` — seconds between ticks.
- `iterations` — stop after N ticks (0 = forever).
- `duration_hours` — stop after H hours (0 = no limit).
- `dry_run` — print alerts instead of sending.

## How it works

1. Read the latest `*_trade_idea_agent.json` to get baseline tiers and ideas + the mode.
2. Pick the C / rejected symbols as the candidate set.
3. Always include BTC + ETH so `MarketRegimeAgent` works.
4. Refresh OHLCV (anchor only) on the mode's timeframes.
5. Refresh Binance derivatives + multi-exchange derivatives.
6. Re-run a lightweight pipeline: regime → momentum → derivatives → news → catalyst → narrative → fusion → crowd-attention → setup → risk → critic → score → trade-idea.
7. Diff new tier vs baseline. `TIER_RANK = {rejected: 0, C: 1, B: 2, A: 3}`. An upgrade → actionable when `new_tier ∈ {A, B}` AND `direction ∈ {long, short}`.
8. For each actionable upgrade, `should_alert(tick, cooldown_minutes)` checks `last_alert_for(symbol)`. If outside cooldown OR new tier differs from last, alert.
9. Format the alert (plain text, includes `SL:`):
   ```
   {SYMBOL} tier {prev} -> {new} ({DIRECTION})
   score X | mode Y | confidence Z
   entry low - high
   SL: <sl_or_invalidation>
   TP1 ... / TP2 ...
   <thesis>
   caps: ...
   ```
10. `notifier.send(text, parse_mode="")` to avoid markdown issues on symbol names.
11. Persist alert into SQLite `watchlist_alerts`.

## Important constants

- `TIER_RANK = {"rejected": 0, "C": 1, "B": 2, "A": 3}`.
- `_mode_timeframes` forces `1h` into scalp mode for regime context.
- `format_alert.sl = setup.get("sl") or setup.get("invalidation")` — explicit fallback ensures alerts always have an SL line.

## Used by

- CLI directly.
- Long-running monitor process (or short-running tick orchestrated by `Bash run_in_background`).

## Common mistakes

- Running monitor when the last trade-idea-agent output is older than 1 hour — baselines are stale.
- Running monitor in `scalp` mode against a swing report (`mode` is taken from the latest payload).
- Sending too aggressively — keep cooldown at 30 min minimum.

## Future improvements

- Add B-tier downgrade alerts (e.g. B → C means thesis weakened; useful to exit).
- Per-mode cooldown.
- Per-symbol stale watch (drop symbols not refreshed in N hours).

## Related

- [[Telegram_Integration]]
- [[Invalidation]]
- [[Trade_Idea_Agent]]

## Implemented status

- **Implemented**, with `SL:` line in `format_alert`.
