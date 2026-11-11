# Risk / Reward

## Definitions used in code

- `entry_mid = (entry_low + entry_high) / 2`
- `risk = abs(entry_mid - invalidation)`
- `reward = abs(TP1 - entry_mid)`
- `rr_to_tp1 = reward / risk`

`TP1 = close ± 1 ATR`, `TP2 = ±2 ATR`, `TP3 = ±3 ATR`.

## Thresholds enforced

| Condition | Effect |
|---|---|
| `rr_to_tp1 < 1` | −10 risk penalty in `ScoringAgent`, +14 in `RiskAgent`, setup quality −12, warning added |
| `rr_to_tp1` undefined (no invalidation) | rejected via no-invalidation cap |
| ideal | `rr_to_tp1 ≥ 1`, `rr_to_tp2 ≥ 2` (defaults in `scoring.yaml.execution`) |

## How `setup_quality` uses R/R

```
setup_quality += min(rr_to_tp1, 2.5) * 8
```

A 2R setup adds +16 to setup quality; capped at +20.

## When the desk doesn't show R/R

- Watchlist-only ideas have no R/R.
- ATR-less setups (rare) have no R/R.

## Sanity tests

- If `rr_to_tp1 > 5` on a scalp, double-check: invalidation is probably too tight (likely wick-prone).
- If `rr_to_tp1 < 1` on a swing, the targets are too close given a 1.2 ATR stop — either the trend is exhausted or the volatility is wrong for the mode.

## Practical rules

| Mode | Minimum R/R to TP1 | Ideal R/R to TP1 | Ideal R/R to TP2 |
|---|---|---|---|
| scalp | 1.0 | 1.5 | 2.0 |
| intraday | 1.0 | 1.5 | 2.0–2.5 |
| swing | 1.2 | 2.0 | 3.0+ |

The desk uses the same 1.0 minimum across modes. Apply the swing 1.2 manually if you are tightening discipline.

## Related

- [[Invalidation]]
- [[Stop_Loss_Logic]]
- [[ATR]]
- [[Scoring_Overview]]

## Implemented status

- **Implemented**.
