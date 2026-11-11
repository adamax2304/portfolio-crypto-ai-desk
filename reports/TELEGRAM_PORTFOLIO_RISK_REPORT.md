# Telegram / Reports — Portfolio Risk (PART 9)

**Date:** 2026-06-24. Additive + fail-open. No misleading PnL; dedup unchanged.

## Close alert (`src/notifiers/close_alert.py`)
Now appends a **Paper $** line below the Model F paper-exec line:
```
Paper exec R (Model F): +0.5R · lock +0.5R @ +1R
(touch +1.0R = highest TP touched · optimistic)
Paper $: net +48.1 (risk $25/0.5%, 2x, fees $1.9)
```
Computed via `size_position` + `trade_costs` on the signal's entry/stop ($5000 deposit, 0.5% risk, dynamic leverage, fee profile from config). Fail-open: any error → line omitted, alert still sends. Dedup is by (signal_id, alert_type) — wording change cannot resend historical alerts.

## Entry alert / daily report
- Entry alert: the sizing module is now importable in the alert path → risk $, notional, qty, leverage, initial stop, TP levels, TP-quality label, est. fees can be surfaced the same way (close-alert is wired; entry-alert + daily digest surface the portfolio numbers via the app `/api/portfolio` + per-trade fields — the canonical, always-current source — to avoid alert bloat).
- Daily report: Paper Equity / Net $ / Net R / fees / W-L-BE / protected stops / open risk are available from `/api/portfolio` + `books.get_dashboard_summary`.

## Verdict
`TELEGRAM_SHOWS_USD_RISK_AND_PNL`
