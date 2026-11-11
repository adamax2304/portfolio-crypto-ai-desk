# Position / Leverage Advisor — Implementation (PART 7)

**Date:** 2026-06-17 · **Verdict:** **POSITION_LEVERAGE_ADVISOR_LABEL_ONLY_READY**
**Label only. NOT execution, NOT auto-sizing, NOT auto-leverage. Never calls an exchange, never changes `size_weight`.**

## What was built
- **`src/risk/position_advisor.py`** — `position_leverage_advice(entry, stop, equity, risk_pcts=(0.25,0.5,1.0), max_leverage=10, liq_buffer_min_pct=30, atr, …)`:
  - `risk_usd = equity * risk_pct`; `stop_distance_pct = |entry−stop|/entry*100`; `suggested_notional = risk_usd / (stop_distance_pct/100)`.
  - `max_safe_leverage = min(max_leverage, floor(100 / (stop_distance_pct * (1 + buffer))))` (isolated-margin liquidation approximation; optional ATR haircut).
  - flags `unsafe` if the liquidation buffer can't be met at any leverage ≤ max, or `warning` if reaching the notional needs leverage above the safe estimate.
  - `unknown` on missing/invalid inputs (never fakes).
- Wired into the risk-guard payload (label fields) + a compact Telegram line via `advisor_line(...)`.

## Outputs (all diagnostic)
`position_advisor_status` (ok/warning/unsafe/unknown), `stop_distance_pct`, `suggested_notional`, `suggested_margin_at_{1,2,3,5}x`, `max_safe_leverage_estimate`, `leverage_warning`, `capital_efficiency_note`, `by_risk_pct` (0.25/0.5/1.0%), `diagnostic_only=true`.

## Telegram / Control Plane
Compact line: *"ℹ Position advisor: stop 2.00%, risk 0.5% → notional ~$2,500, max safe 10x — diagnostic only"* (+ a warning suffix when unsafe). Surfaced read-only; never gates anything.

## Rules honored
- Does not change `size_weight`, place an order, modify exchange leverage, or call any exchange API.
- Does not hide an unsafe leverage — it is surfaced explicitly.
- Missing inputs → `unknown`.

## Defaults (assumptions, overridable)
assumed equity $10,000; risk 0.25/0.5/1.0%; max leverage 10x; min liquidation buffer 30% beyond the stop. These are **display assumptions** for the advisory, not account settings.
