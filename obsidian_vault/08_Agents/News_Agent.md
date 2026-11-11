# NewsAgent

## File

[src/agents/news_agent.py](../../src/agents/news_agent.py).

## Role

Buckets the latest RSS news rows into top_news + by_symbol + by_narrative.

## Inputs

- `rows: list[dict]` — SQLite `news_items` rows (raw_json fallback to per-column fields).

## Outputs

```python
{
  "top_news":     [first 15 items by importance],
  "by_symbol":    {ticker: [items[:8]]},
  "by_narrative": {narrative_name: [items[:8]]},
  "warnings":     [...]
}
```

Each item is a `NewsItem` Pydantic model:

- `title`, `source`, `url`, `published_at`.
- `detected_symbols`, `detected_narratives`.
- `importance` (float, default 1).

## How it makes decisions

- No agent-side scoring beyond sorting by importance and clipping bucket sizes.
- Importance is set by the collector (`RSSNewsCollector`) — primary sources can be configured to have higher importance.

## Used by agents

- `CatalystAgent` reads `by_symbol` to attach news mentions to each ticker.
- `NarrativeAgent` reads both `by_symbol` and `by_narrative` for the narrative heatmap.
- `MacroGeopoliticsAgent` reads `top_news` for keyword scans.
- Report builder renders the top news block.

## Common mistakes

- Assuming all RSS items have valid `detected_symbols` — many headlines are ambiguous; conservative detection means lots of items have empty arrays.
- Treating `importance` as gospel — it's a coarse number.

## Future improvements

- Per-source reliability weight.
- ML-based ticker detection (current is keyword regex).
- Per-narrative sentiment classification.

## Related

- [[News_System_Overview]]
- [[Primary_vs_Secondary_Sources]]
- [[Catalyst_Agent]]
- [[Narrative_Agent]]

## Implemented status

- **Implemented**.
