# Stock Technical Setups

[src/stocks/agents/technical_agent.py](../../src/stocks/agents/technical_agent.py) computes a setup per symbol per mode using EMA stack, ATR, prev-day H/L, and (intraday only) a rolling session VWAP.

## Timeframe pairs per mode

| Mode | Execution TF | Context TF |
|---|---|---|
| intraday | 15m | 1h |
| swing | 1h | 1d |
| invest | 1d | 1wk |

The agent always reads daily bars for prev-day H/L regardless of mode.

## Trend classification (context TF)

- **uptrend** — last_close > EMA20 > EMA20[t-5] **AND** last_close > EMA50
- **downtrend** — last_close < EMA20 < EMA20[t-5] **AND** last_close < EMA50
- **range** — otherwise

## Direction derivation

- uptrend → **long**
- downtrend → **short**
- range → **no_trade**

## Entry / invalidation / target conventions

For longs (mirror for shorts):

- `entry_high` = last close
- `entry_low` = last close − 0.5 ATR
- `invalidation` = entry_low − 1 ATR
- `tp1` = entry_high + 1.5 ATR
- `tp2` = entry_high + 2.5 ATR
- `tp3` = entry_high + 4.0 ATR
- `rr_to_tp1` = (tp1 − entry_high) / (entry_high − invalidation)

## Quality score components (0–100)

- +30 if trend is directional (up or down)
- +15 if last close is consistent with EMA50 stack
- +20 if rr_to_tp1 ≥ 1.5
- +15 if ATR/price > 0.5% (enough volatility to matter)
- +10 if VWAP confirms direction (intraday only)
- +10 if price has cleared the prev-day high/low in the trade direction

Capped at 100. This value feeds `technical_setup` in the scoring agent.

## Prev-day H/L significance

Breaking the prior day's high (longs) or low (shorts) is the single most important signal on a stock chart for intraday trades — institutional algos and stop placements cluster there. The quality_score bonus reflects that.

## VWAP caveat

The intraday VWAP is a rolling 26-bar window (~one US session for 15m bars), not a true session-anchored VWAP. Good enough for confirmation; not good enough to execute mean-reversion fades against. Treat it as directional context, not a precise level.

## When no setup is produced

If the context frame doesn't exist or has < 30 rows, the agent skips the symbol entirely. Make sure `stocks-update-data` has run for the mode you want before the report.
