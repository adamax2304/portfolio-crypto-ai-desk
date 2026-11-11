# Crypto Alert Registration Audit (PART 1)

**Status:** read-only audit written WHILE the 12h scheduler is running. **No code changed. Scheduler NOT interrupted.** Implementation (PART 2–5) is deferred until the scheduler finishes (~01:11 EEST).

---

## Alert paths inventory

| # | Path | Sends Telegram? | Creates `proposed_signals`? | Alert table |
|---|------|-----------------|------------------------------|-------------|
| 1 | **Crypto report → `Supervisor._maybe_send_trade_alerts`** (scalp / intraday / swing / daily) | ✅ A/B, long/short | ⚠️ Separately via `_maybe_register_signals`, **called AFTER the alert** (supervisor.py L481 alert, L482 register) | `watchlist_alerts` (legacy) |
| 2 | **`monitor-watchlist` → WatchlistMonitor** | ✅ on tier flip to B/A | ❌ **does NOT call `register_ideas`** (grep finds no `register_ideas` import in `watchlist_monitor.py`) | `watchlist_alerts` (legacy) |
| 3 | **Stocks `stocks-monitor-session`** | ✅ A/B via `MaterialImprovementChecker` | ✅ pipeline registers first, then alerts | `signal_alerts` (modern) |
| 4 | **Stocks pipeline `run_report`** | (no direct TG) | ✅ `register_ideas(... asset_class="stocks")` | n/a |

**Conclusion:** crypto has two legacy alert emitters (report-level and watchlist-monitor) both writing to `watchlist_alerts`. Stocks uses the modern `signal_alerts` ledger that is registration-first. The asymmetry is structural.

---

## Why alerted ≠ registered (root-cause analysis)

Two independent contributing causes:

### Cause A — ordering + filter mismatch in the report path
- `Supervisor` (src/agents/supervisor.py) calls **`_maybe_send_trade_alerts` at L481 BEFORE `_maybe_register_signals` at L482.** Alert goes out first; registration is a separate later step that can skip the same idea.
- The **alert filter** is loose: `_maybe_send_trade_alerts` sends any idea with `tier in {A,B}` and `direction in {long,short}` (supervisor L678).
- The **registration filter** is stricter: `register_ideas` → `_qualifies_for_tracking` (src/signals/registry.py L150). A `C`-tier needs entry+invalidation; an `A/B` long/short qualifies on tier alone — **but** `build_signal_from_idea` can still produce a row with NULL entry/invalidation if the idea's `raw.setup` is empty.
- Net: an A/B idea whose `raw.setup` lacks entry/invalidation can be **alerted** but its registry row (if created) is incomplete — and if it flows through the watchlist-monitor path instead, **no row is created at all.**

### Cause B — watchlist-monitor has no registration call
- `WatchlistMonitor` records to `watchlist_alerts` directly and never calls `register_ideas`. Any alert it emits (a symbol flipping to B/A between ticks) is **untracked by design.**

### Evidence (today, 2026-05-29)
Detector `scripts/detect_untracked_legacy_alerts.py` found **4** crypto `watchlist_alerts` with no matching `proposed_signal`:

| symbol | tier | mode | direction | sent (UTC) |
|--------|------|------|-----------|------------|
| UNI/USDT | B | scalp | short | 08:36 |
| BCH/USDT | B | scalp | short | 08:45 |
| XLM/USDT | B | swing | long | 10:56 |
| INJ/USDT | B | swing | long | 11:36 |

Affected modes: **scalp + swing** (intraday not seen today but the same path applies).

---

## Legacy alert payload — fields available vs missing for tracking

`watchlist_alerts` row columns: `sent_at, symbol, previous_tier, new_tier, score, direction, mode, asset_class, payload_json`.

| Needed for tracking | In legacy alert? |
|---------------------|------------------|
| symbol | ✅ |
| asset_class | ✅ |
| mode | ✅ |
| direction | ✅ |
| tier (new_tier) | ✅ |
| score | ✅ |
| **entry_low / entry_high** | ❌ usually absent (payload_json may carry thesis only) |
| **invalidation / stop** | ❌ absent |
| **TP1/TP2/TP3** | ❌ absent |
| created_at | ⚠️ only `sent_at` |
| source_report_path | ❌ |
| signal_id | ❌ (no link) |

**Critical limitation:** the legacy alert row alone does **not** contain entry/invalidation/TP. To backfill a *trackable* signal we must recover those from the **source report** that produced the alert (matched by symbol + mode + timestamp). Where the source report no longer has the idea (e.g. watchlist-monitor flips), entry/stop **cannot be reconstructed** and the signal is **not backfillable** without fabricating values (which the spec forbids).

---

## Planned fix (PART 2–5) — to implement AFTER scheduler finishes

1. **Registration-before-alert, unified rule** (`Supervisor` + `WatchlistMonitor`): before any A/B Telegram send, call `register_ideas` (or a new `ensure_signal_for_alert`) and obtain a `signal_id`. Only send the alert if a signal exists (or mark it untrackable with `data_confidence='low'` + explicit missing-fields note — never silently send untrackable A/B).
2. **Link alert → signal_id** in the alert payload.
3. **Backfill** today's 4 untracked alerts from their source reports where entry/invalidation exist; mark `source='legacy_backfill'`; skip (with audit note) any that cannot be reconstructed.
4. **Tests** (9 cases from the spec).
5. **Report** `CRYPTO_LEGACY_ALERT_TRACKING_FIX_REPORT.md`.

**Not touched:** scoring, thresholds, agents' analytical logic, strategy. Only registration/alert/tracking consistency.

---

## Safety

- Scheduler running, NOT interrupted, NOT modified.
- This document is read-only analysis.
- No code/scoring/threshold/trading changes made.
- Backfill + code fix will run only after the 12h schedule completes.
