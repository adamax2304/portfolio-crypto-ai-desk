# Post-P1-Fix Verification Report

**Date:** 2026-06-05 · Covers the two P1 stock fixes from the 48h audit:
**(1) stocks swing pause**, **(2) stocks Telegram 400 delivery fix.**

## 1. Changes landed (code)
| File | Change |
|---|---|
| `src/stocks/agents/trade_idea_agent.py` | **Gate C** — `mode=="swing"` demotes stocks A/B → C with cap_reason `stocks_swing_paused_after_48h_audit` + watchlist avoid note. Mirrors existing legal/post-earnings/market-closed gate pattern (demote, never reject). |
| `src/stocks/reports/stocks_report_builder.py` | Swing **watchlist-only banner** ("…temporarily watchlist-only due to 48h audit: −12R, 0W/12L…"). |
| `src/stocks/monitor.py` | `format_stocks_alert()` footer `_alert_type_:` → `alert_type:` (no Markdown markers); send site now `notifier.send(text, parse_mode="")` (plain text). |

No change to: scoring, A/B thresholds, stop/TP geometry, crypto logic, monitor
selection/cooldown/dedup, or any stored data.

## 2. Test results
| Suite | Result |
|---|---|
| `tests/test_stocks_swing_pause.py` (9 swing + 2 report) | ✅ 11 passed |
| `tests/test_stocks_swing_pause.py` + `test_stocks_telegram_safe.py` + `test_stocks_market_closed_stale.py` | ✅ 26 passed |
| `…` + `test_stocks_monitor_alerts.py` + `test_stocks_monitor_cooldown.py` | ✅ 57 passed |

(The monitor integration tests run real per-signal data fetches, hence the long
wall-clock; all green.)

### Part 1 — swing pause, verified
- swing A/B → C with `stocks_swing_paused_after_48h_audit` cap_reason ✅
- cap_reason + demote reason recorded; signal **not deleted** (stays C) ✅
- **intraday / invest / crypto-swing unaffected** ✅
- capped swing produces **no A/B Telegram** (C-tier is non-actionable by the
  monitor; selection logic unchanged) ✅
- report renders the watchlist-only note for swing, and **not** for intraday ✅

### Part 2 — Telegram 400, verified
- formatter emits no Markdown italic markers; `alert_type:` plain ✅
- hostile ticker/reason (`[]`, `()`, `_`, `+/-`, `$`) doesn't crash formatter ✅
- monitor sends with `parse_mode=""` (plain text) on every send ✅
- a 400 on every send does **not** crash the monitor; counted as
  `telegram_failed`, alert row still recorded `failed:…` ✅
- **dedup/cooldown unchanged** (duplicate tick → no re-send; cooldown suite
  green) ✅

## 3. Expected production impact
- **Removes the −12R / 0W-12L stocks-swing loss bucket** from the actionable
  (Telegram-pushed) book; swing remains visible as research/watchlist.
- **Stocks Telegram delivery** moves from ~19% 400-failure to plain-text
  transport that carries brackets/tickers/symbols verbatim → expected
  near-elimination of HTTP-400 delivery failures. (ReadTimeouts are network,
  not addressed by this fix and not a code defect.)
- Crypto book (shorts +6R, intraday, catalyst-backed) untouched.

## 4. Go-live note
The long-lived scheduler / stocks-monitor process caches old code until
restarted. These fixes take effect for new cycles **after the next scheduler
restart**. Recommend restarting the default scheduler + stocks monitor to load
the build (pending user approval, per standing process).

## 5. Not in scope (remaining audit TODOs)
- `TODO-stocks-atier-promotion` (A-tier PF 0.14) — needs a scoped scoring study;
  not touched here (would alter scoring).
- `TODO-crypto-scalp-review`, `TODO-crypto-weight-catalyst` — need more data.
- `TODO-stocks-chart-ohlcv-path` (cosmetic).

## Final verdict
```
READY_AFTER_P1_STOCK_FIXES
```
Both P1 stock fixes are implemented, scoped strictly, and verified by tests
(57 passing across the swing-pause, Telegram-safe, market-closed, monitor-alert
and cooldown suites) with no change to scoring, thresholds, stop/TP geometry,
crypto logic, or monitor selection/cooldown/dedup. Apply on the next scheduler
restart.
```
