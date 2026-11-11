# Leverage / Position Visibility Fix (PART 5)

**Date:** 2026-06-24.

## Why the operator couldn't see leverage
The ledger stored `leverage_used` / `margin_used_usdt` / `position_notional_usdt` / `risk_usdt`, but the frontend never surfaced them and the summary didn't aggregate them.

## Fix
- **Dashboard:** new Leverage card (**avg 1.95x, max 5x**, risk-capped count) + Open/Margin card. `/api/portfolio` returns `avg_leverage`, `max_leverage`, `risk_capped_trades`, `fee_profiles_available`, `fee_estimated_any`.
- **Trade detail:** "Paper sizing & exit" block — leverage, notional, margin, risk $, net $, exit price + the note "leverage != risk — stop distance × size defines risk."
- **Telegram:** close-alert Paper $ line carries `risk $ / leverage / fees`.
- Sizing chain visible in detail (equity -> risk -> stop-distance -> notional -> qty -> leverage -> margin).

## Verdict
`LEVERAGE_VISIBLE_IN_APP_AND_TELEGRAM`
