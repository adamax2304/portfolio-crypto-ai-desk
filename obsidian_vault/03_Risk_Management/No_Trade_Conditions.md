# No-Trade Conditions

If any of these are true, the desk rejects (or should reject) the idea. Many are enforced; a few require manual discipline.

## Enforced (in code)

1. **No invalidation level.** → score cap 50 + `tier=rejected`.
2. **Stale data (> 3h since the latest cached candle).** → score cap 50 + `tier=rejected`.
3. **Extreme adverse funding** (`> +0.001` for long, `< -0.001` for short). → cap 78.
4. **Rumor-only catalyst.** → cap 55.
5. **MEXC-only listing.** → cap 70 (65 if weak structure).
6. **Not listed on anchor exchange (Binance).** → cap 75.
7. **Low liquidity** (RiskAgent warning includes "low_liquidity"). → cap 60.
8. **Setup extension > 2.5 ATR from EMA20.** → `TechnicalSetupAgent` converts direction to `watchlist_only`.
9. **ATR unavailable.** → `direction = no_trade`.
10. **`high-volatility danger` regime + RiskAgent +25 penalty.** → typically pushes `risk_level = high`.

## Discipline (manual)

11. **No setup at all** — symbol not in latest ranked candidates; do not invent one.
12. **Coverage audit screams "missing major data".** Check `CoverageAuditAgent` output; if regime data is degraded, hold.
13. **Open conflicting position** — if you already hold the opposite side in a correlated symbol, do not stack.
14. **Time of day / event proximity** — within 30 min of CPI / FOMC / major listing announcement: hold.
15. **Telegram euphoria stage** — `CrowdAttentionAgent.stage == "euphoria"` and you don't already have a position: skip.
16. **Exchange flagged** — if the symbol's anchor exchange is degraded, hold.
17. **No clear thesis sentence** — if you can't write the trade thesis in one sentence, the trade isn't there.

## How to read the report's "rejected" block

Each rejected idea has:

- `primary_reason` — the dominant cap or warning.
- `reasons[]` — supporting reasons, up to 6.
- `risk_flags` — exchange/structure flags (e.g. `mexc_only`, `not_on_anchor`).
- `exchanges` — which venues list it.

This is high-signal: read the rejection block before the active-ideas block when calibrating your eye for the day.

## Related

- [[Score_Caps]]
- [[Risk_Management_Overview]]
- [[Pre_Trade_Checklist_For_LLM]]

## Implemented status

- **Implemented** (rules 1–10) / **Partially implemented** (rules 11–17 are operator discipline).
