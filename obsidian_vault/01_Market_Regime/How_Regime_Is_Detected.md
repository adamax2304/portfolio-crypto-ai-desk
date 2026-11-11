# How Regime Is Detected

Exact logic from [src/agents/market_regime_agent.py](../../src/agents/market_regime_agent.py).

## Step 1 — Per-symbol trend on the regime timeframe

Regime timeframe: `config/settings.yaml.execution.regime_timeframe` (default `4h`, fallback `1h`).

For BTC/USDT and ETH/USDT, compute `trend_label` from `enrich_ohlcv(frame)`:

| Condition | Label |
|---|---|
| close > EMA20 > EMA50 | uptrend |
| close < EMA20 < EMA50 | downtrend |
| close > EMA50 and EMA20 < EMA50 | transition_up |
| close < EMA50 and EMA20 > EMA50 | transition_down |
| otherwise | range |

If frame length < 60 bars → `unknown`. Missing BTC or ETH frame raises a warning and keeps the label fallback.

## Step 2 — Breadth

Iterate the **entire loaded universe** (each symbol with ≥ 60 bars on regime TF):

- `above_ema20_pct` — % of symbols with close > EMA20.
- `above_ema50_pct` — % above EMA50.
- `positive_24h_pct` — % with 24h return > 0 on regime TF (6 bars × 4h).
- `outperforming_btc_pct` — % outperforming BTC 24h return.

`breadth_score = above_ema20_pct`.

## Step 3 — Volatility flag

`btc_atr_pct = atr_percentile(btc_frame)` — percentile of BTC ATR vs trailing window.

`high_vol = btc_atr_pct ≥ 80`.

## Step 4 — Decision tree (in this exact order)

```
if high_vol AND |btc_24h_return| > 4%:
    label = "high-volatility danger"
    risk_mode = "danger"
elif btc_trend in {uptrend, transition_up}
     AND eth_trend in {uptrend, transition_up}
     AND breadth_score >= 55:
    label = "bullish trend"
    risk_mode = "risk-on"
elif btc_trend in {downtrend, transition_down}
     AND breadth_score <= 40:
    label = "bearish trend"
    risk_mode = "risk-off"
elif 40 <= breadth_score <= 60:
    label = "range/chop"
    risk_mode = "neutral"
else:
    label = "transition"
    risk_mode = "mixed"
```

Notes:

- `bullish trend` requires **both** BTC and ETH to confirm and breadth ≥ 55. One-of is not enough.
- `bearish trend` only requires BTC + breadth ≤ 40 (ETH is not gated here).
- `range/chop` is breadth-bounded; it does not check trend.
- `transition` is the catch-all when nothing above matches.
- `low-volatility compression` is **not** emitted today.

## Step 5 — Confidence

Starts at 45 and adds:

- +20 if BTC trend known.
- +10 if ETH trend known.
- +15 if at least 8 symbols counted in breadth.
- +10 if BTC ATR percentile is known.

Clamped to 0–100.

## Step 6 — Key levels

For BTC/USDT and ETH/USDT, compute `recent_range(frame, lookback=20)` → local resistance + local support.

## What the report shows

```
Market regime is {label} ({risk_mode}); style: {recommended_style}.
BTC trend: {btc_trend}, ETH trend: {eth_trend}; breadth above EMA20: {x.x}%.
```

## How to debug a wrong-looking regime

- Run `python -m src.cli candidate-debug --symbol BTC/USDT --mode intraday` and look at the BTC trend tag.
- Check `data/processed/agent_outputs/<latest>_market_regime_agent.json` — raw label + breadth.
- If breadth is calculated on too few symbols (universe filtered hard), re-run `update-data` without `--symbols` to widen.

## Related

- [[Market_Regime_Overview]]
- [[Bullish_Regime]] · [[Bearish_Regime]] · [[Neutral_Chop_Regime]] · [[Transition_Regime]] · [[High_Volatility_Regime]] · [[Low_Volatility_Compression]]
- [[Regime_Debugging]]

## Implemented status

- **Implemented** (exact code path described).
