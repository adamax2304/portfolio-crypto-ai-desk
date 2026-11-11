# TechnicalSetupAgent

## File

[src/agents/technical_setup_agent.py](../../src/agents/technical_setup_agent.py).

## Role

Per-symbol entry plan: entry zone, invalidation, targets, setup_quality.

## Inputs

- `candidates: list[MomentumCandidate]`.
- `market_data: dict[symbol, dict[tf, DataFrame]]`.
- `regime: MarketRegime`.
- `limit: int`.

## Outputs

`list[TechnicalSetup]`:

- `symbol`, `direction` ∈ {long, short, watchlist_only, no_trade}.
- `timeframe`, `current_price`.
- `entry_low`, `entry_high`, `invalidation`, `tp1`, `tp2`, `tp3`.
- `atr`, `rr_to_tp1`.
- `setup_quality` (0–100).
- `trend`, `support`, `resistance`.
- `warnings[]`.

## How it builds entries (verbatim)

See [[Stop_Loss_Logic]] for the long/short construction.

- Distance-from-EMA20 > 2 → warning + setup_quality −14.
- Distance > 2.5 → direction forced to `watchlist_only`.
- RR to TP1 < 1 → −12 setup quality + warning.
- ATR missing → direction = `no_trade`.
- Direction conflict with regime (long-in-bearish, short-in-bullish) → warning string included.

## Used by agents

- `RiskAgent`, `CriticAgent`, `ScoringAgent`, `TradeIdeaAgent` all consume `TechnicalSetup` directly.

## Common mistakes

- Trusting `current_price` as a fill price — it's the last bar's close at runtime.
- Treating `entry_low / entry_high` as a hard band — the desk expects pullback acceptance, not market-buy in the middle.

## Future improvements

- Per-mode setup timeframe (right now uses `settings.yaml.execution.setup_timeframe = "1h"` for all modes).
- Swing-aware structure (multi-bar pivots instead of 20-bar window).
- VWAP-aware entries.

## Related

- [[Stop_Loss_Logic]]
- [[Invalidation]]
- [[Risk_Reward]]
- [[Overextension_Risk]]

## Implemented status

- **Implemented**.
