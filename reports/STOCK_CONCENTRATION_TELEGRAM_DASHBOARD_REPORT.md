# Concentration — Telegram / Dashboard Behavior (PART 5)

**Date:** 2026-06-16

## Telegram (implemented + tested)
For stocks-intraday A/B paper entries:
- **1st exposure** → sends normally.
- **2nd exposure** → sends with prefix
  `Correlation cap: 2nd exposure in <bucket> <dir> bucket — 0.5x only` (half-size warning).
- **3rd+ / proxy-duplicate** → **not pushed**; routed shadow with
  `[SHADOW ONLY — SECTOR CAP]\nReason: <reason>` (telegram_status `shadow_sector_cap`).

Tests: `test_live_second_exposure_half_size_warning`,
`test_live_third_exposure_shadow_not_pushed`, `test_live_proxy_duplicate_shadow`,
`test_live_first_exposure_sends`, `test_live_crypto_unaffected`.

The `signal_alerts.payload_json` for every stocks paper entry now carries `risk_bucket`,
`proxy_group`, `concentration_status`, `concentration_rank`,
`concentration_effective_weight`, `concentration_reason` — so journal / digest / dashboard
can render them with no schema change.

## Dashboard / journal (spec'd — follow-up)
Planned "**Stocks Concentration Guard**" section (reads the payload fields + live
`concentration_for_live_signal`): current open exposures grouped by `risk_bucket` ×
direction, each row showing symbol, status, effective weight, reason. Per-row labels:
`risk_bucket`, `proxy_group`, concentration status, effective weight. Not yet inserted into
the 1.5k-line dashboard builder — deferred with the shadow-first rollout to keep the live
change surface minimal; data is already available via the payload + helper.

**PART 5 status: Telegram DONE; dashboard section spec'd (data available).**
