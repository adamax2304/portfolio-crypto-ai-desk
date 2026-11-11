# Intraday Commands

## Generate intraday report

```powershell
python -m src.cli intraday-report                    # refresh 15m/1h + render
python -m src.cli intraday-report --no-update        # render from cache
python -m src.cli intraday-report --auto-universe    # Stage 1+2 funnel
python -m src.cli intraday-report --auto-universe --discovery
```

`intraday-report --auto-universe` is an alias for `auto_universe_report(mode="intraday", kind="intraday")`.

## Behavior

- 15m / 1h / 4h timeframes for active symbols.
- `daily-report --mode intraday` is equivalent in mode but writes under `data/reports/daily/`.

## Output

```
data/reports/intraday/YYYY-MM-DD_HH-MM_intraday_report.md
```

## Default for most workflows

This is the desk's primary mode. When in doubt, run intraday.

## Related

- [[Intraday_Mode]]
- [[Daily_Commands]]
- [[Mode_Specific_Scoring]]

## Implemented status

- **Implemented**.
