# Pre-Check — Option B Latency Verification (PART 1)

**Date:** 2026-06-16 ~11:16 UTC · Production DB: `db/crypto_ai_desk.sqlite` (read-only)

## State checks — all pass

| Check | Result |
|-------|--------|
| SQLite WAL enabled | ✅ `journal_mode=wal` |
| busy_timeout active | ✅ `30000` ms |
| Pending lock dir / no stale lock | ✅ `.locks/` exists, **empty** (no held/stale lock) |
| monitor-watchlist `--track-pending` default | ✅ on by default |
| Full-pass marker works | ✅ marker active → pending pass yields → marker cleared after |
| Crypto scalp sizing | ✅ `0.0×` |
| Crypto scalp shadow predicate | ✅ `True` |
| Crypto scalp setup Telegram | ✅ suppressed (intraday not suppressed) |
| Tracker gates | ✅ paper-entry fires open/not-closed; close fires terminal-from-triggered only |
| Non-scalp paper-entry/close | ✅ allowed (gates + routing intact) |
| Auto-trade path | ✅ none (grep `create_order/place_order/ccxt..Order` → empty) |

## ⚠️ Critical operational finding — Option B is NOT live yet

| Signal | Value |
|--------|-------|
| Option B code mtime (impl boundary) | **2026-06-16 10:25 UTC** |
| Now | 2026-06-16 11:16 UTC |
| Last `signal_alerts.sent_at` | 2026-06-16 **10:07** UTC (pre-impl) |
| Last `signal_outcomes.checked_at` | 2026-06-16 **10:07** UTC (pre-impl) |
| Alerts / outcomes / entries **after** impl | **0 / 0 / 0** |
| Today's monitor pidfiles mtime | **10:07 UTC** (pre-impl) |
| Freshest OHLCV cache | 11:14 UTC (fresh) |

**Diagnosis:** a monitor process **is running** (OHLCV cache is being refreshed every few
minutes), but it was **started at ~10:07 UTC — before the 10:25 implementation** — so it is
executing **pre-Option-B code**. A running Python process does not hot-reload edited
modules, so it refreshes candles (its `re_evaluate`) but never calls the new
`track_pending_entries`. The 2-hourly `track-signals` (which does write outcomes/alerts)
last ran at 10:07, also pre-impl.

**Consequence for PART 2:** there is **no post-Option-B live data** to measure yet. The
latency audit can only show the pre-Option-B baseline until a **fresh monitor process**
(next 2h scheduler cycle, or a manual monitor restart) loads the new code and runs the
5-min pending pass against newly-triggered entries.

**Action required to activate Option B:** the monitor must restart. The scheduler starts a
fresh monitor each 2h cycle, so it will activate automatically on the next cycle; a manual
`monitor-watchlist --interval 300` restart would activate it immediately. (Not done here —
verification task; flagged for the operator.)

**PART 1 status: DONE — all guards pass; Option B implemented correctly but not yet
exercised by a live process.**
