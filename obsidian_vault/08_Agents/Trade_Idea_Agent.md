# TradeIdeaAgent

## File

[src/agents/trade_idea_agent.py](../../src/agents/trade_idea_agent.py).

## Role

Assembles the final `TradeIdea` and `RejectedIdea` records from setups + scores + supporting evidence.

## Inputs

- `setups`, `candidates`, `scores`.
- `regime`, `derivatives`, `catalysts`, `risks`, `critiques`, `narratives`.
- `exchange_confirmations`.
- `mode: str`.

## Outputs

- `list[TradeIdea]` — capped at `max_trade_ideas + max_watchlist` items (default 5 + 10 = 15).
- `last_rejected: list[RejectedIdea]` — exposed as a property.

## TradeIdea fields

- `symbol`, `direction` ∈ {long, short, watchlist only, no trade}.
- `score`, `confidence`, `risk_level`, `tier`, `mode`, `timeframe`.
- `exchange_focus`, `exchanges_confirmed`, `data_confidence`.
- `thesis`, `evidence[]`, `counterarguments[]`.
- `entry_plan`, `invalidation`, `targets[]`.
- `what_to_monitor[]`, `avoid_conditions[]`.
- `data_sources_used[]`, `cap_reasons[]`.
- `status` ∈ {open, watchlist, no_trade}.
- `raw` — dict of all underlying agent payloads.

## How direction is assigned

- A/B + setup.direction in {long, short} → direction = long/short, status = open.
- C → direction = "watchlist only", status = watchlist.
- else → direction = "no trade", status = no_trade. Also creates `RejectedIdea`.

## risk_level overrides

- `score.risk_penalty >= 20` or `regime == high-volatility danger` → high.
- No `risk` + risk_penalty ≤ 8 + final_score ≥ 75 → medium-low.

## How mode timeframe label is built

```
scalp:   "{setup_tf} thesis / 5m execution (scalp 30m-2h)"
swing:   "{setup_tf} thesis / 4h execution (swing several days)"
default: "{setup_tf} thesis / 15m execution (intraday 4-24h)"
```

## Telegram alert payload

`Supervisor._format_idea_alert(idea, mode, report_id)` formats the alert with markdown (entry, invalidation, TP1/TP2/TP3, caps, thesis, report id). `WatchlistMonitor.format_alert` uses plain text with `SL:` line.

## Used by agents

- `Supervisor.daily_report` → SQLite save + chart generation + Telegram alerts + report rendering.
- `WatchlistMonitor.re_evaluate` → tier diff vs baseline.

## Common mistakes

- Re-running an LLM analysis without checking that `raw` is consistent (the raw dict is the ground truth).
- Treating `data_confidence = high` as "trade is good" — score and tier are separate axes.

## Future improvements

- Track per-trade outcome and back-feed into a learning loop.
- Surface `recommended_risk_pct` derived from data_confidence + risk_level.

## Related

- [[Scoring_Agent]]
- [[Risk_Agent]]
- [[Watchlist_Monitor_Agent]]
- [[Exchange_Fusion_Agent]]

## Implemented status

- **Implemented**.
