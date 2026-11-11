# Mode Selection Logic

How the desk decides which mode to run.

## Explicit selection

- `python -m src.cli scalp-report` → mode=scalp.
- `python -m src.cli intraday-report` → mode=intraday.
- `python -m src.cli swing-report` → mode=swing.
- `python -m src.cli daily-report --mode intraday` (or `scalp` / `swing`) — explicit override.

Inside `auto_universe_report(mode, kind, discovery)`:

1. `MultiExchangeUniverseCollector.rank_candidates(mode=...)` ranks with mode-specific filters from `universe.yaml`.
2. Top symbols are fetched on the mode-specific timeframes (`_mode_timeframes`).
3. The report is rendered with the matching kind.

## Auto / natural-language

`Supervisor.ask(query, refresh=None)` runs `_infer_action(normalized_query)`:

| Keywords (any) | Action |
|---|---|
| review, worked, failed, ревью, обзор идей | `review` |
| intraday, morning, still valid, утро, интрадей, актуаль | `intraday-report` |
| update, refresh, обнов, fresh data | `update-data` |
| scanner, scan, скан | `scan` |
| else | `daily-report` |

There is no auto-routing to `scalp` or `swing` from natural language — the desk demands an explicit CLI command.

## Watchlist monitor mode

`WatchlistMonitor.baseline_tiers()` reads the latest `*_trade_idea_agent.json` and adopts its `mode`. So if the last report was `swing`, the monitor will re-evaluate at swing timeframes. To force a switch, run a fresh report in the new mode.

## How to choose manually

- **Trading the next 30m–2h on a specific symbol** → scalp.
- **Trading the next 4–24h on rotating candidates** → intraday (default).
- **Trading the next 2–7 days with narrative / catalyst basis** → swing.
- **Wanting to widen discovery (50% lower volume floor, 250 symbols)** → add `--discovery`.

## Mode mismatch warnings

If you re-evaluate a swing setup in scalp mode, you get:

- Wider invalidation (built off 1h ATR, not 4h ATR).
- Tighter min_atr_percent filter (0.12 vs 0.80) — swing candidates often pass scalp filter, but their 1h structure is irrelevant.
- Mode multipliers will mute narrative and catalyst by design.

Prefer re-running the same mode that produced the original idea.

## Related

- [[Trading_Modes_Overview]]
- [[Mode_Specific_Timeframes]]
- [[Mode_Specific_Risk]]

## Implemented status

- **Implemented**.
