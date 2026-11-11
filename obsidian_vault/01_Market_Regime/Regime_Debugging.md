# Regime Debugging

## When the regime call "looks wrong"

1. Open `data/processed/agent_outputs/<latest>_market_regime_agent.json`. Look at:
   - `label`, `confidence`.
   - `btc_trend`, `eth_trend` — these should match what you see on a 4h chart.
   - `alt_breadth.symbols_counted` — if < 8, regime confidence is low.
   - `alt_breadth.above_ema20_pct` — this is the gate.
2. If symbols_counted is low → universe filtered too aggressively. Re-run:
   ```
   python -m src.cli update-universe
   python -m src.cli update-data
   python -m src.cli daily-report
   ```
3. If BTC/ETH trend tag disagrees with chart → the regime TF (default `4h`) may differ from your chart TF. Check `config/settings.yaml.execution.regime_timeframe`.

## When breadth misclassifies

Breadth uses the **whole loaded `market_data` set**, not just the watchlist. If `update-data` ran with `--symbols`, breadth is computed on that subset and may be noisy. Re-run without `--symbols`.

## When ATR percentile is missing

`atr_percentile(btc_frame)` returns `None` if frame too short. `high_vol` becomes `False` → danger regime can't trigger. Make sure BTC has ≥ ~120 bars on the regime TF.

## When the desk says `transition` and you expect `bullish trend`

Check both gates:

- BTC trend ∈ {uptrend, transition_up}?
- ETH trend ∈ {uptrend, transition_up}?
- `above_ema20_pct ≥ 55`?

A single failure pushes the label to `transition`. ETH lagging is the most common cause.

## When regime flips on every tick

Look at `confidence` and breadth size. A < 50 confidence regime is volatile by design. Solutions:

- Widen the universe.
- Increase `data.ohlcv_limit.4h` in `settings.yaml` so trend has more bars.

## Related

- [[How_Regime_Is_Detected]]
- [[Market_Regime_Overview]]
- [[ATR]]

## Implemented status

- **Implemented** — these are the actual debug surfaces (`agent_outputs/` JSON files exist).
