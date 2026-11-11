# Bybit Role

## Role

**Derivatives confirmation.** Bybit is treated as the secondary positioning data source after Binance.

## Concretely

- `BybitOHLCVCollector` fetches spot + linear OHLCV for the symbols Bybit lists.
- `BybitDerivativesCollector` fetches OI history + funding history (dedicated collector for richer time-series).
- `MultiExchangeDerivativesCollector` includes Bybit in the snapshot fetch alongside OKX.
- `MultiExchangeDerivativesAgent` (consumed by reports) reads the multi-venue summary plus `bybit_history` for OI delta and funding delta.

## Why this matters

- Bybit perp positioning often diverges slightly from Binance. Cross-venue agreement is a real confirmation signal.
- For symbols not on Binance but on Bybit (rare), Bybit becomes the structural reference for that symbol.
- Bybit's symbol naming convention differs for high-supply tokens (1000PEPE, 1000SHIB, etc.). `config/exchanges.yaml.symbol_aliases.bybit` maps canonical → Bybit names.

## Caps and flags

- `derivatives_listed` is True when Bybit (or any non-anchor non-high-risk venue) lists the symbol.
- An idea with `anchor_listed=True` + `derivatives_listed=True` and consistent price across venues gets the highest fusion confirmation score.

## Risks specific to Bybit

- Smaller spot books than Binance.
- Some perp pairs use 1000-x multiplier (price units are 1000× the base).
- Occasional API hiccups; collector logs failures into `failures` dict.

## What happens if Bybit fails

- `Supervisor.update_data` swallows secondary failures into `secondary_summaries["bybit"]`.
- `DerivativesAgent` falls back to Binance-only.
- `derivatives_listed` becomes False, which can cap an otherwise strong idea at 75 if it's also not on Binance.

## Related

- [[Exchange_Overview]]
- [[Bybit_Derivatives_Confirmation]]
- [[Multi_Exchange_Derivatives_Agent]]

## Implemented status

- **Implemented**.
