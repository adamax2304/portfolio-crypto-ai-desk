# Why Too Many Longs

The desk leans long because `_market_alignment("long", "bullish trend") = 0.90`. If you see many long ideas, check the regime.

## Quick check

```bash
cat data/processed/agent_outputs/*_market_regime_agent.json
```

- `bullish trend` + ≥ 55 breadth → expect many longs.
- `range/chop` → both sides 0.58; longs no more favored than shorts.

## When "too many longs" is wrong

- Regime says `bearish trend` but desk produces longs anyway.
  - Likely: very strong counter-trend setups + setup_quality high.
  - Check: do the longs have `Regime conflict` warning?
- Regime says `transition` and desk produces longs.
  - Acceptable; transition is direction-neutral but momentum biased.

## Pattern recognition

- "Too many longs" usually means the desk is correctly identifying a healthy bull tape.
- If you don't trust it, check `confidence` on regime (< 60 = unstable).
- If breadth dropped below 55 since the last report, regime may have aged out.

## What to do

- Re-run `update-data && intraday-report` to refresh regime.
- If still all longs and regime says bull → that's correct; size accordingly but respect per-trade risk.

## Don't

- Don't manually force shorts in a bull tape to "balance" — that's just lower expectancy.

## Related

- [[Market_Regime_Overview]]
- [[Long_Short_Neutral_Bias]]
- [[Why_Too_Few_Shorts]]

## Implemented status

- **Diagnostic guide**.
