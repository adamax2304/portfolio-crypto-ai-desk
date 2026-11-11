# Long-Term Commands

## Status

**No CLI commands exist for long-term mode.** See [[Long_Term_Mode]].

If you run `--mode long_term` or similar, `TradeIdeaAgent._mode_normalised` will silently fall back to `intraday`. The desk does not error — it just doesn't operate at the long-term horizon.

## Closest substitute

```powershell
python -m src.cli swing-report --auto-universe
```

Then mentally extend the horizon. The narrative + catalyst analysis is roughly applicable; the entry / invalidation / TPs are not, because they're built off short-window ATR.

## Recommended CLI (future)

```powershell
python -m src.cli long-term-report --auto-universe     # not implemented
python -m src.cli long-term-thesis-check               # not implemented
```

See [[Improvement_Backlog]].

## Operator workflow today

- Use [[Long_Term_Trade_Template]] as a personal thesis tracker.
- Use the desk's swing report for entry timing.
- Track macro / on-chain data externally.

## Related

- [[Long_Term_Mode]]
- [[Long_Term_Risk]]
- [[Long_Term_Trade_Template]]

## Implemented status

- **Recommended / not implemented**.
