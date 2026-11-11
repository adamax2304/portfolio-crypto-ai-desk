# How to Debug Mode Selection

If the desk seems to be running the "wrong" mode.

## Where mode is set

- Explicit CLI: `scalp-report`, `intraday-report`, `swing-report`, `daily-report --mode X`.
- `Supervisor.ask` infers from natural language keywords ([[Mode_Selection_Logic]]).
- `WatchlistMonitor` reads `mode` from the latest `*_trade_idea_agent.json`.

## Diagnostic

1. **Open latest trade-idea-agent JSON**:
   ```
   ls -lt data/processed/agent_outputs/*_trade_idea_agent.json | head -1
   ```
   Read the `mode` field. That's the mode of the latest report.
2. **Compare to what you expected.** If wrong, the latest CLI invocation set the mode.
3. **For watchlist monitor**: it inherits this mode. If you want to switch monitor to a different mode, first run a fresh report in the desired mode.

## Common confusion

- "Why is monitor in intraday mode?" — because the latest report was intraday. Run `scalp-report` if you want monitor in scalp.
- "Why does the report say scalp but timeframes are 15m/1h?" — `WatchlistMonitor` force-adds `1h` to scalp for regime context. The setup TF is still `1h` because `settings.yaml.execution.setup_timeframe = "1h"`.

## Mode mismatch warnings

If you score a swing idea with intraday weights, narrative contribution drops 30%. Always match mode to original report.

## TradeIdeaAgent normalization

Anything not in `{scalp, intraday, swing}` falls back to `intraday`. So a typo in `--mode long_term` silently becomes intraday.

## Related

- [[Mode_Selection_Logic]]
- [[Trading_Modes_Overview]]
- [[Watchlist_Monitor_Agent]]

## Implemented status

- **Diagnostic guide**.
