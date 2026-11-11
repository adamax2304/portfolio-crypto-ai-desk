# Supervisor

## Role

Orchestrator. There's no "Supervisor agent" file; the orchestration lives in [src/agents/supervisor.py](../../src/agents/supervisor.py) at the top level.

## Responsibilities

- Owns `ProjectConfig`, `FileStore`, `SQLiteStore`.
- Resolves the active universe.
- Runs the full daily/intraday/scalp/swing pipeline.
- Wires in `news_trader_bridge` snapshot.
- Saves outputs: markdown reports, `context_for_llm.md`, agent outputs, SQLite trade_ideas, rejected_ideas, latest_candidates, news_trader_bridge_latest.
- Calls `_maybe_send_trade_alerts` to push A/B-tier ideas to Telegram.
- Provides CLI-facing methods: `update_data`, `update_universe`, `rank_universe_candidates`, `daily_report`, `intraday_report`, `scalp_report`, `swing_report`, `review`, `ask`, `scan`, `idea`, `status`, `doctor`, `latest_report`, `exchange_status`, `candidate_debug`.

## Inputs / Outputs

- **Inputs**: ProjectConfig, CLI args.
- **Outputs**: Path to report, dict status payloads, side-effect writes to `data/`, `db/`.

## Failure modes

- "No market data available" — anchor (Binance) cache empty + fetch failed.
- Telegram alert failure on per-symbol basis — logged via `_log_secondary_failure`, doesn't crash the report.
- news_trader_bridge unavailable — logged warning, continue without it.

## Used by agents

This is the agent-runner; agents do not call back into it.

## Common mistakes (LLM editing)

- Adding a new agent without registering it in `daily_report`'s ordered call list.
- Removing the `news_trader_bridge` block and breaking Telegram-derived crowd attention.
- Bypassing `_maybe_send_trade_alerts` by sending Telegram from individual agents (don't; centralize).

## Future improvements

- Split orchestration into per-mode pipelines so scalp / swing don't drag the full chain.
- Make agent ordering data-driven (yaml-defined pipeline) so additions don't require code edits.

## Related

- [[Agents_Overview]]
- [[Trade_Idea_Agent]]
- [[Watchlist_Monitor_Agent]]

## Implemented status

- **Implemented**.
