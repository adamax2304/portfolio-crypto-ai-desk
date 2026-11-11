# Preflight Baseline — Latency / Expired / Stock-Scalp Audit (PART 0)

**Date:** 2026-06-16 · Production DB: `db/crypto_ai_desk.sqlite` (read-only)

## Production state — verified

| Invariant | State | Evidence |
|-----------|-------|----------|
| Crypto scalp sizing weight | **0.0×** | `size_decision(crypto/scalp).weight == 0.0` |
| Crypto scalp shadow predicate | **True** | `is_shadow_only_scalp(crypto/scalp) == True` |
| Crypto scalp setup Telegram | **suppressed** | `should_suppress_setup_telegram("crypto","scalp") == True` |
| Crypto intraday setup Telegram | **not suppressed** (correct) | `should_suppress_setup_telegram("crypto","intraday") == False` |
| Tracker paper-entry gate | **present** | `should_alert_paper_entry(True, triggered)=True`; `(True, expired)=False` |
| Tracker close gate | **present** | `should_alert_close(expired, triggered)=True`; `(expired, waiting)=False` |
| Auto-trade path | **none** | grep `create_order/place_order/.buy(/.sell(/ccxt..Order` in `src/` → empty |

Live routing confirmation (last 24h, from PART-prior audit): scalp paper-entry/close
routed `shadow_only` (not pushed); non-scalp paper-entry/close routed `sent`.

## Scheduler cadence (`scripts/run_default_market_schedule.py`)

| Job | Cadence | Notes |
|-----|---------|-------|
| **Full report cycle** | every **2h** (`--interval-hours` default 2) | scalp + intraday reports + support cmds |
| **track-signals (pre)** | once per cycle, at start | `track-signals --all --revalidate-pending` |
| **track-signals (post)** | once per cycle, at end | same |
| **crypto monitor** | every **300s (5 min)**, 90-min window/cycle | `monitor-watchlist --interval 300` |
| **stocks monitor** | every **10 min** during US RTH, bounded window | `stocks-monitor-session --interval-minutes 10` |
| **swing/invest windows** | 2×/day | cycle inside [03:00,05:00) and [15:00,17:00) EEST |
| **Telegram sender** | **inline / synchronous** | no separate sender service — `TelegramNotifier.send()` is called inside the producing command |

## ⚠️ Critical latency finding (drives PART 2/4)

**Paper-entry (and close) alerts are emitted ONLY by `track-signals`** — confirmed:
`track_active_signals(..., paper_entry_notifier=...)` is called from exactly one place
(`src/cli.py:1277`, `track-signals` command, `--paper-entry-alerts` defaults **True**).
`monitor-watchlist` / `WatchlistMonitor` do **not** call `track_active_signals` and do
**not** emit paper-entry alerts (grep confirms).

**Consequence:** entry-touch is only *detected* at the two `track-signals` runs per 2h
cycle. The 5-min crypto monitor re-checks the *watchlist* (setup-type alerts) but never
detects a paper-entry. So the structural entry-detection cadence is **~2h**, not 5 min —
this is the root cause of the large entry-detection latency measured in PART 2, and the
reason a lightweight pending-only tracker (PART 4 Option A) is the highest-leverage safe
fix.

## Constraints acknowledged for this audit

Read-only first; no auto-trade; no scalp reactivation; no setup-Telegram re-enable; no
TP/SL/scoring/threshold change; no C-tier promotion; no stocks swing/invest unpause; no
history rewrite; no data deletion; no making late alerts look fresh. Allowed: derived
latency tables, Telegram freshness labels, late-entry shadow routing, pending-only
tracker cadence tuning if safe, tests, dashboard labels, stock-scalp research/backtest.

**PART 0 status: DONE.**
