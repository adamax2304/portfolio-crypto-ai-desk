# MEXC-Only Risk

## Definition

A symbol listed **only** on MEXC (no anchor, no derivatives). Triggered in `ExchangeFusionAgent.high_risk_only`.

## Effects in code

- Score capped at **70** in `ScoringAgent`.
- If `technical_setup` component < 14, cap drops to **65**.
- Confirmation score capped at 55 in `ExchangeFusionAgent`.
- Risk flag `mexc_only` added.
- Interpretation: "MEXC-only; treat as speculative discovery, demand confirmation from anchor or Bybit."

## Why the cap

- MEXC liquidity is thinnest of the three.
- Single-venue pumps are common.
- No derivatives data → no positioning confirmation.
- Withdrawal pauses are more frequent.

## Operator rules

- **No A-tier ever on MEXC-only.** The desk enforces this.
- Halve your typical position size at minimum.
- Verify withdrawal works for the asset before holding.
- Set wider mental stops to account for slippage; the desk's ATR-based stop assumes normal liquidity.
- Treat the trade as a scalp by default; multi-hour holds amplify single-venue risk.

## What lifts a MEXC-only flag

- Symbol gets listed on Binance / Bybit. Re-run `update-universe` to refresh `exchange_symbol_map.json`.

## Recommended improvements

- Add a MEXC-derivative collector if MEXC futures support the symbol.
- Auto-flag symbols whose MEXC book depth is below a threshold.

## Related

- [[MEXC_Role]]
- [[Score_Caps]]
- [[Liquidity_Risk]]
- [[Cross_Exchange_Confirmation]]

## Implemented status

- **Implemented**.
