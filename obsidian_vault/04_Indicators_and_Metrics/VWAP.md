# VWAP

## Status

**Not implemented.** VWAP is not computed anywhere in `src/indicators/` or used in any agent.

## Why it would help

- Scalpers often use anchored VWAP from session open / a recent pivot as a mean-reversion anchor.
- Confluence: VWAP touch + EMA20 + recent support stacks evidence.

## Suggested implementation

In `src/indicators/technicals.py`:

```python
def vwap(frame: pd.DataFrame, session_start: pd.Timestamp | None = None) -> pd.Series:
    # session_start defaults to first bar; for anchored VWAP, pass a chosen pivot.
    typical = (frame["high"] + frame["low"] + frame["close"]) / 3
    pv = typical * frame["volume"]
    if session_start is None:
        return pv.cumsum() / frame["volume"].cumsum()
    mask = frame["timestamp"] >= session_start
    pv_session = pv.where(mask, 0).cumsum()
    vol_session = frame["volume"].where(mask, 0).cumsum()
    return pv_session / vol_session.replace(0, pd.NA)
```

Then expose `vwap` in `enrich_ohlcv` and use it in:

- `TechnicalSetupAgent` — bias entry zone toward VWAP for scalp.
- `MomentumScannerAgent` — add VWAP-distance metric.
- `ScoringAgent` — small bonus when entry is near VWAP and direction agrees.

## Related

- [[Indicators_Overview]]
- [[Improvement_Backlog]]

## Implemented status

- **Recommended / not implemented**.
