# Risk-Guard Visibility Fields — Plan (PART 7)

**Date:** 2026-06-17 · **Status:** plan (add-only fields). **No routing/channel change, no new blocking.**

All fields below are **additive** to the existing alert payload / report / Control-Plane view. They make the diagnostics from PARTS 2–6 *visible* without changing which alerts fire or where they route. Each is a label the operator (and Opus) reads; none gates a trade.

## Fields to add (payload + report + Control Plane)
| Field | Source (PART) | Values | Where shown |
|---|---|---|---|
| `circuit_breaker_state` | PART 2 | `ok` / `would_pause_2R` / `would_pause_3R` / `would_pause_3stops` | Telegram header line + dashboard risk panel |
| `day_realized_r` | PART 2 | float (rolling per asset/day) | dashboard risk panel |
| `day_stops` / `consec_stops` | PART 2 | int | dashboard risk panel |
| `would_bind_sector_cap` | PART 3 | `actionable` / `half_size` / `shadow_proxy_duplicate` / `shadow_sector_cap` | stocks-intraday alert info line |
| `would_bind_rank` | PART 3 | int | dashboard (stocks) |
| `profit_protection_hint` | PART 4 | `none` / `reached_+0.5R` / `reached_+1R` (informational, from live MFE) | crypto alert info line |
| `lifecycle_label` | PART 5 | `fresh` / `aging_intraday` / `carryover_needs_review` / `overnight_relabel_candidate` | alert + dashboard |
| `held_hours` | PART 5 | float | alert (already partly available) |
| `btc_intraday_risk_off` | PART 6 | bool | crypto-long alert context line |
| `regime_context` | PART 6 | `btc_up` / `btc_flat` / `btc_risk_off` | alert context line |

## Implementation notes (add-only, safe)
- Payload: extend the existing `payload` dict in `src/notifiers/paper_entry.py` (same place `concentration_*` fields are already attached, ~line 496). New keys default to safe/neutral values; absent fields must not break the Mini App (Control Plane reads defensively).
- Report: add a **"Risk Guards (diagnostic)"** subsection to the stocks/crypto report builders + LLM packet. Read-only render.
- Control Plane: add a read-only **Risk Guards** card. **No** change to the engine-online/offline status, paper/live lock, or routing — v1 stays read-only+paper, live stays locked.
- Telegram: append at most one compact info line per alert (e.g. `🛡 cb:ok · regime:btc_risk_off · life:aging_intraday`). No new channels, no rate-limit change. SL level must still always appear on B/A-tier alerts (existing requirement — these fields are appended, not replacing the SL line).

## What this plan does NOT do
- No new blocking, throttling, force-close, or sizing change.
- No routing/channel/rate-limit change; no engine status change.
- No scoring/TP/SL/threshold/cap-value change.
- Purely visibility — every field is an observation the operator can act on manually.

## Sequencing
Ship `circuit_breaker_state` + `regime_context` first (highest operator value, zero risk), then the rest. Each field is independently revertible by removing its write + render.
