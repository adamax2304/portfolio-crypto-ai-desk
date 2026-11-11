# Swing Commands

## Generate swing report

```powershell
python -m src.cli swing-report --auto-universe
python -m src.cli swing-report --auto-universe --discovery
python -m src.cli swing-report --no-auto-universe    # cache-only (rare)
```

## Behavior

- Stage 1 + Stage 2 with swing filters (volume 150k, ATR 0.80%, top 3 ideas).
- Loads 1h / 4h / 1d for top N.
- `Supervisor.auto_universe_report(mode="swing", kind="swing")`.
- Scoring multipliers: narrative × 1.30, catalyst × 1.20, regime × 1.15, momentum × 0.90.

## Output

```
data/reports/swing/YYYY-MM-DD_HH-MM_swing_report.md
```

## When to use

- Multi-day positioning.
- Narrative-driven setups (sector heating, catalyst pipeline).
- Higher-timeframe structure dominant.

## When NOT to use

- Within 2 days of a known unlock for the symbol.
- `high-volatility danger` regime.
- Narrative cooling rapidly.

## Related

- [[Swing_Mode]]
- [[Narrative_Heatmap]]
- [[Token_Unlocks]]

## Implemented status

- **Implemented**.
