# Scalp Commands

## Generate scalp report

```powershell
python -m src.cli scalp-report --auto-universe
python -m src.cli scalp-report --auto-universe --discovery
python -m src.cli scalp-report --no-auto-universe    # use cached intraday cache only
```

## Behavior

- Stage 1 + Stage 2 with scalp filters (volume 20k, ATR 0.12%, top 3 ideas).
- Loads 1m / 5m / 15m timeframes for top N.
- `Supervisor.auto_universe_report(mode="scalp", kind="scalp")`.

## Output

```
data/reports/scalp/YYYY-MM-DD_HH-MM_scalp_report.md
```

## Monitor

After a scalp report, `python -m src.cli monitor-watchlist` will adopt scalp mode automatically (because the latest trade-idea-agent payload says so).

## When to use

- Active session (US / EU / Asia open).
- Volatility regime not in `high-volatility danger`.
- You want 30m–2h horizon.

## When NOT to use

- Weekend off-hours.
- 30 min before / after a known macro event.
- `high-volatility danger` regime — whipsaws kill scalpers.

## Related

- [[Scalp_Mode]]
- [[Daily_Commands]]
- [[Mode_Specific_Risk]]

## Implemented status

- **Implemented**.
