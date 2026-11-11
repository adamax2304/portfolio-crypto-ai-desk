# Binance Role

## Role

**Anchor exchange.** The structural and liquidity reference. Every OHLCV-driven decision in the desk uses Binance candles as the source of truth.

## Concretely

- `anchor_exchange = binance` in `config/universe.yaml`.
- `BinanceOHLCVCollector` fetches all configured timeframes for the active symbol set.
- `BinanceDerivativesCollector` fetches USD-M futures funding, OI, OI history, long/short ratio.
- `BinanceUniverseCollector` (single-exchange fallback) discovers the active USDT universe.
- `MultiExchangeUniverseCollector` aggregates Binance + Bybit + MEXC, prioritizing Binance for confirmation.

## Why anchor

- Highest liquidity by far.
- Most reliable candles (least manipulation risk).
- Provides USD-M futures funding and OI in real time.
- `EMA20/50/200` on Binance is the canonical structure.

## What downstream agents trust on Binance

- `MarketRegimeAgent` reads BTC/ETH 4h from Binance.
- `MomentumScannerAgent` ranks on Binance candles where listed.
- `TechnicalSetupAgent` builds invalidation from Binance support/resistance.
- `DerivativesAgent` uses Binance USD-M funding for the cap thresholds (`±0.001`, `±0.0005`).

## Risks specific to Binance

- API rate limits (handled via ccxt rate-limit toggle).
- Withdrawal halts on small caps.
- US restrictions for some users.
- Occasional regional cookie / Cloudflare issues on RSS-side (announcements feed handled separately).

## What happens if Binance fails

- `Supervisor.update_data` records failures in `summary.failed`.
- Downstream agents skip the symbol with missing data; `CoverageAuditAgent` calls it out.
- For BTC/ETH specifically, regime confidence drops; warnings added.

## Related

- [[Exchange_Overview]]
- [[Cross_Exchange_Confirmation]]
- [[Exchange_Failure_Handling]]
- [[Derivatives_Agent]]

## Implemented status

- **Implemented**.
