# Mode-Specific Timeframes

From `config/universe.yaml.modes` (authoritative).

## Table

| Mode | Timeframes loaded | Primary TF (ranking) | Setup TF (`TechnicalSetupAgent`) | Execution TF (label) | Regime TF (`settings.yaml`) |
|---|---|---|---|---|---|
| scalp | 1m, 5m, 15m, **1h** auto-added by `WatchlistMonitor` | 5m | `setup_timeframe` in `settings.yaml` = `1h` | 5m | 4h |
| intraday | 15m, 1h, 4h | 1h | 1h | 15m | 4h |
| swing | 1h, 4h, 1d | 4h | 1h (currently) | 4h | 4h |

## Why setup TF defaults to 1h

`TechnicalSetupAgent` reads `config/settings.yaml.execution.setup_timeframe = "1h"` for **all** modes. This means:

- Scalp setups still build their invalidation off **1h** ATR, even though execution is on 5m.
- Swing setups build off **1h** ATR even though the thesis is on 4h/1d.

This is a known simplification. To get truly TF-specific invalidation, you can:

- Change `setup_timeframe` to `5m` for scalp runs (do not commit — runtime override).
- Or extend `TechnicalSetupAgent` to accept a per-mode setup TF (recommended; not implemented).

## Why scalp force-adds 1h

`WatchlistMonitor._mode_timeframes` and `Supervisor._mode_timeframes`:

```python
if mode == "scalp" and "1h" not in timeframes:
    timeframes.append("1h")
```

This is so `MarketRegimeAgent` (which uses regime_timeframe `4h` by default, with `1h` fallback) still has some data even when only 1m/5m/15m would otherwise be loaded.

## OHLCV limits

From `config/settings.yaml.data.ohlcv_limit`:

| TF | Bars cached |
|---|---|
| 15m | 220 |
| 1h | 220 |
| 4h | 220 |
| 1d | 180 |

Other timeframes (1m, 5m) use the collector default. Long enough for EMA200 + ATR14.

## Related

- [[Mode_Selection_Logic]]
- [[Indicators_Overview]]
- [[Technical_Setup_Agent]]

## Implemented status

- **Implemented**, with the simplification of single setup_timeframe noted.
