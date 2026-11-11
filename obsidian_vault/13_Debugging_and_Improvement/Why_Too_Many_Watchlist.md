# Why Too Many Watchlist

When most ideas are C-tier (watchlist) instead of B/A, the desk is correctly cautious — but it's worth understanding why.

## Common causes

1. **Regime is `transition` or `range/chop`**: momentum is muted, alignment is 0.58 for both sides — setups don't get to 65.
2. **Many candidates extended > 2 ATR from EMA20**: auto-converted to watchlist.
3. **Missing derivatives data**: derivative quality drops to baseline; component is mid; +2 penalty too.
4. **Catalyst missing**: catalyst quality drops; +2 penalty.
5. **Narrative status `crowded/watch carefully`**: narrative contribution dropped, warnings added.
6. **Most setups on MEXC**: capped at 70, often pinned to mid-C.

## Diagnostic

```
python -m src.cli scan-universe --mode intraday
python -m src.cli candidate-debug --symbol SOL/USDT --mode intraday
```

Look at `setup_quality` and `cap_reasons` per candidate.

## What to do

- **If regime is the cause** — wait for regime resolution.
- **If extension is the cause** — wait for pullback. Watchlist monitor will fire on upgrade.
- **If data is the cause** — re-run `update-data`; check `coverage_audit`.
- **If MEXC-cap is the cause** — limit your attention to anchor-listed candidates only.

## Don't

- Don't upgrade C → B manually because "the chart looks good".
- Don't lower the C-tier threshold in `scoring.yaml` to manufacture more ideas.

## Related

- [[C_Tier_Watchlist_Setups]]
- [[Candidate_Debug_Guide]]
- [[How_to_Adjust_Filters]]

## Implemented status

- **Diagnostic guide**.
