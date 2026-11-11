# Glossary

Internal terms used throughout the desk + vault. When in doubt, this is the canonical definition.

## Tiers and ideas

- **Idea** — a structured record with symbol, direction, score, tier, entry, invalidation, targets. Produced by `TradeIdeaAgent`.
- **A-tier** — score ≥ 80 **and** no active score caps. Long or short only. The desk does not produce A-tier for `watchlist_only` direction.
- **B-tier** — score ≥ 65. Long or short with valid invalidation. Most actionable ideas live here.
- **C-tier** — score ≥ 50. Direction "watchlist only". The setup is interesting but not ready.
- **Rejected** — explicit non-trade with reason(s). Logged separately so silence has a justification.
- **Tier upgrade** — diff vs prior tier in `WatchlistMonitor`. Order: `rejected (0) < C (1) < B (2) < A (3)`.

## Modes

- **Scalp** — 1m/5m/15m timeframes, 30m–2h horizon.
- **Intraday** — 15m/1h/4h timeframes, 4–24h horizon.
- **Swing** — 1h/4h/1d timeframes, several days.
- **Discovery** — flag (`--discovery`) widening the scan to 250 candidates with lower volume floor.
- **Long-term** — **not implemented**; see [[Long_Term_Mode]].

## Exchanges (per `config/exchanges.yaml`)

- **Anchor** — primary structure reference; currently `binance`.
- **Derivatives** — `bybit`; funding/OI/perp confirmation.
- **Discovery / high-risk** — `mexc`; early new-listing surface, capped at B-tier on its own.

## Regime labels

- `bullish trend` / `bearish trend` / `range/chop` / `transition` / `high-volatility danger` / `low-volatility compression`. See [[Market_Regime_Overview]].

## Indicators / metrics

- **EMA20/50/200** — exponential moving averages from [src/indicators/technicals.py](../../src/indicators/technicals.py).
- **ATR14** — average true range over 14 bars.
- **RSI14** — relative strength index over 14 bars.
- **Volume SMA20** — 20-bar simple moving average of volume.
- **Volume ratio** — recent volume / SMA20.
- **Relative strength vs BTC** — symbol return − BTC return over the same window.
- **Distance from EMA20 in ATR** — `(close - ema20) / atr14`. Used as "extension" gate.

## Derivatives

- **Funding rate** — Binance USD-M perp lastFundingRate. Cap thresholds: |funding| > 0.001 = "extreme", > 0.0005 = "elevated".
- **OI change** — relative change in open interest over the available history window.
- **Long/short ratio** — Binance global long/short positions ratio.
- **Crowding risk** — derived label (`normal / elevated long crowding / extreme long crowding / short squeeze potential / unknown`).

## News / Telegram

- **`news_trader`** — sister project that runs Telethon, scrapes 50+ Telegram channels, classifies signals. Lives at `C:\Users\adama\Documents\zeph ai projects\news_trader\`. **Read-only from this desk.**
- **`news_trader_bridge`** — this project's read-only consumer of `news_trader/news_trader/state/telemetry.jsonl`. See [[Telegram_Integration]].
- **Tier strong / medium** — news_trader's own classification; "strong" raises verification to `confirmed`.
- **Verification status** — `none / news_mention / manual_event / single_source / rumor / confirmed`.
- **Attention score** — derived in `CrowdAttentionAgent`; combines social mentions + manual notes + Telegram mention count + strong-tier count.

## Crowd stages (`CrowdAttentionAgent`)

`silent / early_attention / growing_hype / euphoria / exhaustion / fear_capitulation / rumor_driven / unknown`.

## Files

- **`context_for_llm.md`** — `data/processed/context_for_llm.md`; compact LLM-readable snapshot.
- **`exchange_symbol_map.json`** — `data/processed/exchange_symbol_map.json`; canonical symbol → list of venues.
- **`universe_ranked_candidates*.json`** — Stage-2 ranked candidates, optionally per mode.
- **`telemetry.jsonl`** — news_trader event stream (read-only via bridge).

## Related

- [[System_Principles]]
- [[Score_Caps]]
- [[Trading_Modes_Overview]]

## Implemented status

- **Implemented** — all defined terms map to entities in the current code.
