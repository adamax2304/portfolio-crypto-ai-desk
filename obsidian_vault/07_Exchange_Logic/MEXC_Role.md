# MEXC Role

## Role

**Discovery / high-risk.** MEXC surfaces early listings and small-cap movers that Binance and Bybit haven't picked up yet. The desk treats MEXC data with explicit skepticism.

## Concretely

- `MEXCOHLCVCollector` fetches spot OHLCV.
- `MultiExchangeUniverseCollector` includes MEXC in Stage 1 discovery with the lowest volume floor (1.5M vs 10M / 5M).
- MEXC has no dedicated derivatives collector in this desk — its perp data is not integrated.
- `config/exchanges.yaml.mexc.high_risk: true`.
- `config/universe.yaml.high_risk_exchanges: [mexc]`.

## Score caps tied to MEXC

- **MEXC-only listing**: score cap 70.
- **MEXC-only listing with weak structure** (technical_setup contribution < 14): score cap 65.

These are enforced in `ScoringAgent`. The fusion agent flags `mexc_only` so the cap fires.

## When MEXC adds value

- Catching listings ~hours before Binance / Coinbase pick them up.
- Surfacing low-cap rotation that mainstream venues miss.
- Early discovery of memes and ecosystem launches.

## When MEXC is dangerous

- Single-venue manipulation (illiquid books can be moved by small actors).
- "MEXC-only pump" — the classic setup for a 30-50% rug.
- Stale data / wide spreads (sometimes the price on MEXC drifts from real markets by minutes).

## Operator rules

- **Never size a MEXC-only trade like an anchor-listed trade.** Half size at most.
- **Verify withdraw works** before holding a MEXC position for hours.
- **Don't chase MEXC pumps.** The cap (70) plus extension gate usually kicks them to watchlist.

## What happens if MEXC fails

- Discovery surface shrinks. Stage 1 universe loses MEXC-only symbols.
- `multi_exchange_universe_collector` records failures; downstream coverage audit notes it.

## Related

- [[Exchange_Overview]]
- [[MEXC_Only_Risk]]
- [[Score_Caps]]
- [[Liquidity_Risk]]

## Implemented status

- **Implemented**.
