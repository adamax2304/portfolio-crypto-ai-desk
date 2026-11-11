# Volume Anomaly

## Source

`src/indicators/volume_anomaly.py`. Computes per-bar volume ratio vs SMA20. Returns 1.0 = average, > 1.5 = expansion, > 3.0 = strong anomaly.

## Where it is used

- **Universe Stage 2** ranking — `volume_anomaly` per candidate.
- **Candidate ranking score** — opportunity score adds points for elevated volume.
- **`RiskAgent`** — warns when `volume_ratio < 0.5` (weak breakout confirmation).
- **`NarrativeAgent`** — `volume_score = avg(volume_ratio / 2, capped 1.5) * 100` per narrative.
- **`CrowdAttentionAgent`** — feeds the evidence block.

## Thresholds (rule of thumb)

| volume_ratio | Interpretation |
|---|---|
| < 0.5 | drying up; breakout risk |
| 0.5–1.0 | quiet |
| 1.0–1.5 | normal |
| 1.5–3.0 | confirmation candidate |
| > 3.0 | strong anomaly; verify it's not a single fat bar |

## Reading

- Volume confirmation should appear on the **breakout candle itself** and the **first retest**. Volume after the move has happened is exit signal, not entry.
- On lower timeframes (1m / 5m), single fat candles can produce misleading ratios. Demand 2+ consecutive bars.

## Common mistakes

- Trusting the anomaly tag without checking absolute quote volume — a 3x spike on $20k is meaningless.
- Reading a high anomaly as bullish even on red bars — volume confirms direction, not bias.

## Related

- [[Indicators_Overview]]
- [[Liquidity_Risk]]
- [[Breakout_Reclaim_Structure]]
- [[Relative_Strength]]

## Implemented status

- **Implemented**.
