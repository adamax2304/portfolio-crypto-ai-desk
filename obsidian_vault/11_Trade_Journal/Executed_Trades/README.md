# Executed_Trades

Trades you actually entered. The desk does not place trades, so this is your private execution log.

## How files land here

- Manual: move a Potential_Trades file here and re-apply [[Executed_Trade_Template]] (add Entry / Management / Exit / Review sections).
- Cross-link to the original report path: `data/reports/{kind}/YYYY-MM-DD_*.md`.

## Filename

```
YYYY-MM-DD_SYMBOL_MODE_DIRECTION_SCORE.md
```

## Per-trade workflow

1. Fill **Entry** immediately after fill.
2. Fill **Management** as the trade evolves (every 4h for swing, every 1h for intraday, every 15m for scalp).
3. Fill **Exit** at close.
4. Fill **Review** within 24h.

## Related

- [[Executed_Trade_Template]]
- [[Review_Template]]
- [[Daily_Review_Template]]

## Implemented status

- Folder ready; manual workflow.
