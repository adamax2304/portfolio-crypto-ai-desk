# Backtesting and Review

How to validate desk behavior against actual outcomes.

## What the desk has

- **`ReviewAgent`** (`python -m src.cli review`) — loads saved ideas from SQLite, checks subsequent candles, computes MFE / MAE / entry-trigger / TP hits / invalidation hits.
- SQLite tables `trade_ideas`, `idea_checks`, `news_items`, `events`, `agent_runs`, `watchlist_alerts`.
- `data/processed/agent_outputs/` — JSON snapshot of every agent per run.

## What the desk does NOT have

- Full historical backtest engine (replay over months).
- Slippage / fee modeling.
- Trade lifecycle (partial fills, scaling out).

## Operator-grade backtest workflow

1. Generate reports across a date range manually:
   ```
   git log --oneline data/reports/   # see what was already saved
   ```
2. Use `python -m src.cli review` to refresh `idea_checks` against the latest candle cache.
3. For each saved idea, the review computes:
   - Did price enter the entry zone?
   - Did TP1 / TP2 / TP3 hit?
   - Did invalidation hit?
   - MFE / MAE relative to entry midpoint.
4. Per-mode and per-tier roll-ups should be done manually or by writing a small script.

## What to look for

- **Hit rate per tier**: A-tier should hit TP1 ≥ 60% historically; B-tier ≥ 50%.
- **R multiple distribution**: median expected R per tier.
- **Per-cap success**: did MEXC-only B-tier outperform anchor B-tier? (Probably not.) Did rumor-capped ideas ever surprise upward? (Rare.)
- **Per-mode success**: scalp should hit TP1 fast; swing should hit TP2.

## Recommended improvements

- A `python -m src.cli backtest --start YYYY-MM-DD --end YYYY-MM-DD --mode intraday` that regenerates reports from cached candles.
- A `python -m src.cli backtest-report` that joins SQLite with subsequent candles and computes statistics.
- Persistent storage of historical regime + breadth for cross-time analysis.

## Per-trade review checklist

See [[Post_Trade_Review_Checklist_For_LLM]] and [[Review_Template]].

## Related

- [[Review_Agent]]
- [[Review_Template]]
- [[Daily_Review_Template]]
- [[Weekly_Review_Template]]

## Implemented status

- **Implemented** (ReviewAgent). Full backtest engine **Recommended**.
