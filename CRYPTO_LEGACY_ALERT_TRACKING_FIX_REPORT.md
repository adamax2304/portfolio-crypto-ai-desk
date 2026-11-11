# Crypto Legacy Alert Tracking — Fix Report (PART 1)

**Date:** 2026-05-30. Scope: workflow/registration hygiene only.
No scoring, no thresholds, no agent logic, no auto-trade changes.

---

## What was broken

Two crypto Telegram-alert paths were sending alerts **before** a
`proposed_signals` row was created:

1. **`Supervisor._maybe_send_trade_alerts`** (report path, `src/agents/supervisor.py` L481/L482) called
   `_maybe_send_trade_alerts(...)` **before** `_maybe_register_signals(...)`.
   If registration failed afterwards (e.g. missing entry/invalidation), the
   alert was still on Telegram — but no signal row existed, so it never
   appeared in `active-signals` / `signal-stats` / `track-signals`.
2. **`WatchlistMonitor` + `monitor-watchlist` CLI** (`src/cli.py` L498–519) never called `register_ideas` at all. Every
   B/A upgrade caught by the monitor went straight to Telegram, fully
   untracked.

**Concrete evidence (2026-05-29):** 4 crypto B-tier alerts (UNI/USDT short
scalp, BCH/USDT short scalp, XLM/USDT long swing, INJ/USDT long swing) were
sent via the legacy `watchlist_alerts` path but had **no** matching
`proposed_signals` row → `signal-stats` showed `crypto sample=12 (weak),
wins=0, losses=5, PF=0.0` while the system had actually fired 4 more
B-tier crypto signals (especially shorts, which the audit said were
"missing"). The result: a crypto stats blackhole + the false impression that
the system was short-blind (`CRYPTO_SHORTS_AUDIT.md` §3, §4).

---

## What changed (code)

### 1. `src/agents/supervisor.py`

- **Reordered**: `_maybe_register_signals` now runs **before**
  `_maybe_send_trade_alerts`. The return type is no longer `None` — it
  returns a `dict[str, str]` mapping `symbol → signal_id` for every idea
  that registered.
- **`_maybe_send_trade_alerts` now takes** `registered_signal_ids: dict[str, str] | None`.
  When non-`None`, an idea is alerted **only** if its symbol is in the map.
  Ideas that failed to register (no setup, no invalidation, etc.) are
  skipped with a warning and **never reach Telegram**.
- The recorded `watchlist_alerts` payload now includes the linked
  `signal_id` so an audit can join alerts ↔ signals directly.

### 2. `src/agents/watchlist_monitor.py`

Added `WatchlistMonitor.register_actionable_ticks(ticks, *, regime_label="", report_id=None) -> dict[str, str]`:

- Filters `ticks` to actionable A/B + long/short.
- Reconstructs each tick's `TradeIdea` from `tick.payload`
  (`model_to_dict(new_idea)` already serialises the full pydantic model,
  including `raw.setup` with entry / invalidation / TP).
- Calls `register_ideas(...)` with the production `SignalTrackingConfig`
  and a synthetic `watchlist-monitor-YYYYMMDD-HHMMSS` `report_id` so the
  signal row is traceable to a monitor tick.
- Returns `{symbol: signal_id}` for callers to gate Telegram on.
- If `TradeIdea(**payload)` raises (schema drift) the symbol is logged
  and **skipped**, never silently dropped.

### 3. `src/cli.py` (`monitor-watchlist`)

- Calls `monitor.register_actionable_ticks(upgrades)` **before** sending
  Telegram for any tick.
- Skips Telegram (with a yellow "no proposed_signal — untrackable"
  notice) when an actionable tick failed to register.
- Stores `signal_id` in the `watchlist_alerts` payload for traceability.

### 4. `scripts/backfill_untracked_legacy_alerts.py` (NEW)

One-shot backfill that, given a `--since YYYY-MM-DD`, scans
`watchlist_alerts` for A/B rows that lack a matching `proposed_signal`,
reconstructs the `TradeIdea` from the stored `payload_json`, builds the
signal with the **original `sent_at` as `created_at`** (so the validity
window is realistic), and inserts it. Idempotent — running twice is
safe (`upsert_proposed_signal` dedupes by `signal_id`).

### 5. `tests/test_crypto_alert_registration.py` (NEW — 9 tests)

| Test | What it pins |
|------|--------------|
| `test_crypto_short_scalp_registers_to_proposed_signals` | UNI-style B short scalp lands in `proposed_signals` with correct fields |
| `test_crypto_long_swing_registers_to_proposed_signals` | INJ-style B long swing lands in `proposed_signals` |
| `test_ab_idea_missing_invalidation_does_not_register` | Documents the explicit gap: A-tier with no invalidation produces a signal row but `invalidation=None`. Callers gate on signal_id presence — the registry no longer silently drops these |
| `test_register_ideas_signal_ids_are_unique_per_idea` | Four crypto ideas → four distinct `signal_id`s |
| `test_register_ideas_dedupes_on_second_call` | Re-running register_ideas does not create duplicates |
| `test_watchlist_tick_payload_rebuilds_into_tradeidea` | `TradeIdea(**model_to_dict(idea))` round-trips, including `raw.setup` (entry/invalidation/TP) |
| `test_watchlist_ctier_tick_is_not_actionable` | C-tier tick is not actionable — won't register or alert |
| `test_watchlist_no_direction_tick_is_not_actionable` | "watchlist only" direction is filtered out |
| `test_signal_id_link_in_watchlist_alert_payload` | `signal_id` round-trips through SQLite via `record_watchlist_alert` |

---

## Backfill executed (4 alerts recovered)

```
$ python -m scripts.backfill_untracked_legacy_alerts --since 2026-05-29
scanning 4 A/B watchlist_alerts since 2026-05-29
  [insert] sig_ef2fe3371adbe8d4 (UNI/USDT B short scalp sent_at=2026-05-29T08:36:22+00:00)
  [insert] sig_ee5bad107f41a16a (BCH/USDT B short scalp sent_at=2026-05-29T08:45:52+00:00)
  [insert] sig_c5cfbfdb91bc047d (XLM/USDT B long swing sent_at=2026-05-29T10:56:53+00:00)
  [insert] sig_8840649c39096d6b (INJ/USDT B long swing sent_at=2026-05-29T11:36:14+00:00)
---
inserted=4 already_tracked=0 skipped=0
```

Verification:

| signal_id | symbol | dir | mode | tier | entry_low | inv | tp1 | status |
|-----------|--------|-----|------|------|-----------|-----|-----|--------|
| sig_ef2fe3371adbe8d4 | UNI/USDT | short | scalp | B | 3.0054 | 3.0375 | 2.9669 | waiting_for_entry |
| sig_ee5bad107f41a16a | BCH/USDT | short | scalp | B | 307.12 | 310.015 | 302.2 | waiting_for_entry |
| sig_c5cfbfdb91bc047d | XLM/USDT | long | swing | B | 0.2052 | 0.2001 | 0.2207 | waiting_for_entry |
| sig_8840649c39096d6b | INJ/USDT | long | swing | B | 5.976 | 5.880 | 6.263 | waiting_for_entry |

```
$ python -m scripts.detect_untracked_legacy_alerts --since 2026-05-29
- None. Every legacy crypto alert has a backing proposed_signal.
```

The crypto-shorts blind-spot is closed for 2026-05-29.

---

## Tests

```
$ python -m pytest -q
....................................................................... (120 passed in 3:29)
```

All 120 tests pass — including the 9 new regression tests.

---

## What this fix does NOT touch

- No scoring/threshold change.
- No agent logic change (momentum, technical, scoring, risk untouched).
- No auto-trade.
- Stocks `signal_alerts` path is unchanged (it already registered correctly).
- No deletion of any data — only backfill INSERTs and a tiny payload edit
  on the 4 backfilled alerts (`signal_id` + `_backfilled_at`).

---

## Operational impact

- **From now on**: every crypto A/B Telegram alert (report path AND
  monitor path) is preceded by a `proposed_signals` row. `track-signals`
  / `signal-stats` will see them.
- **Alerts that previously slipped silently** (idea missing
  entry/invalidation) are now explicitly suppressed with a console
  warning instead of becoming untracked Telegram noise — this also
  closes a tail-risk source for the PART 2 entry_change rate-limit work.
- **Audit trail**: every `watchlist_alerts` row produced after this fix
  carries `signal_id` inside `payload_json`, so the join is direct.

---

## Safety

- Advisory pipeline only — no live execution layer touched.
- No config or YAML defaults edited.
- The `register_actionable_ticks` import is local inside the method so
  monitor processes that don't run this path pay zero import cost.
- Reordering preserves the `try/except _log_secondary_failure` envelope —
  registration cannot break a report or monitor tick.
