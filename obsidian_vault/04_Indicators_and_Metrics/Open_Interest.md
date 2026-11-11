# Open Interest

See [[Open_Interest_Risk]] for the full risk treatment. This page is the data-source view.

## Sources

- **Binance USD-M**: `openInterest` (current value) + `openInterestHist` (5-min granularity over a recent window) — `BinanceDerivativesCollector`.
- **Bybit linear**: snapshot — `MultiExchangeDerivativesCollector`.
- **Bybit history**: dedicated `BybitDerivativesCollector` for OI delta + funding history.
- **OKX**: snapshot — `MultiExchangeDerivativesCollector`.

## Derived

`DerivativesAgent._oi_change(hist)` returns the % change between first and last bar in the history window. Combined with the 1h price change, produces the four-cell interpretation table (see [[Open_Interest_Risk]]).

## When OI is unreliable

- New listings — OI history may be empty for the first few hours.
- Symbol delisted from a venue — collector logs failure; `data_available = False`.
- Symbol whose ccxt name differs across venues (e.g. PEPE vs 1000PEPE) — handled via `config/exchanges.yaml.symbol_aliases`.

## Reading the report's derivatives block

```
Derivatives: <interpretation>; funding <funding_rate>; OI change <oi_change_pct>%; crowding <label>.
```

If the interpretation says "data partially unavailable", do not fabricate a read — the agent saw nothing.

## Practical rule

- Long entries want OI rising **with** price.
- Short entries want OI rising **with** price falling (fresh shorts), but watch for squeeze if the level reclaims.

## Related

- [[Open_Interest_Risk]]
- [[Funding_Rate]]
- [[Funding_Risk]]
- [[Derivatives_Agent]]
- [[Multi_Exchange_Derivatives_Agent]]

## Implemented status

- **Implemented**.
