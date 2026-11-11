# Bybit Derivatives Confirmation

## What it means

Bybit is the desk's secondary positioning source. When `confirmation.derivatives_listed = True` (i.e. Bybit lists the symbol's perp), the idea has cross-venue derivatives confirmation.

## How it shows up

- `ExchangeFusionAgent.confirmation_score` gets +20.
- `MultiExchangeDerivativesAgent` produces a per-symbol summary combining Binance USD-M + Bybit linear (+ OKX where available).
- `BybitDerivativesCollector` separately produces OI delta + funding history.

## Why this matters

- Binance funding alone can occasionally diverge from real positioning (anchor's perp may be different from the broader perp ecosystem).
- Bybit confirms: are perps everywhere agreeing on direction?
- Bybit funding history (multi-bar) is sometimes more informative than a single Binance snapshot.

## How to use it

- If `derivatives_listed = True` and price + funding direction agree across Binance and Bybit, your trade has stronger derivative confirmation.
- If the two venues disagree (e.g. Binance funding +0.0008 but Bybit funding 0), do not stack confidence on top of the funding read.

## Risks

- Bybit symbol naming uses 1000× multiplier for some tokens (PEPE → 1000PEPE). The desk's aliases handle this; if you query the agent output for "PEPE/USDT", it works correctly.
- Bybit perp can have its own listing decisions; sometimes a Binance perp exists but Bybit's doesn't, or vice versa.

## Related

- [[Bybit_Role]]
- [[Derivatives_Agent]]
- [[Multi_Exchange_Derivatives_Agent]]
- [[Cross_Exchange_Confirmation]]

## Implemented status

- **Implemented**.
