# Latency & Expired — Safe Fix Implementation (PART 11)

**Date:** 2026-06-16

Only changes that are **clearly safe and additive** were implemented. Cadence changes
(second DB writer) were specified but **deferred for approval** (PART 4 Phase 2).

## Implemented

### 1. Entry freshness label + late-entry shadow routing (`src/notifiers/paper_entry.py`)
- `entry_freshness(entry_triggered_at, now)` → `(label, age_seconds, actionable)`.
- `LATE_ENTRY_SHADOW_MINUTES = 15` threshold constant (tunable).
- `send_paper_entry_alert`:
  - appends `Entry freshness: …` to every paper-entry message;
  - **very-late (>15m) / unknown** → prepend `[LATE ENTRY DETECTED — DO NOT CHASE]`,
    `telegram_status="late_shadow"`, **not pushed**, recorded for journal/research
    (`telegram_channel="shadow_only_late"`, `reason_skipped="late_entry"`);
  - **fresh/acceptable/late (≤15m)** → pushed normally with the label;
  - **crypto scalp** → unchanged (`shadow_only` predicate runs first).
- Detail: [TELEGRAM_ENTRY_FRESHNESS_LABEL_REPORT.md](TELEGRAM_ENTRY_FRESHNESS_LABEL_REPORT.md).

### 2. Read-only audit tooling
- `scripts/audit_latency_expired.py` → `ENTRY_DETECTION_LATENCY.csv`,
  `EXPIRED_SIGNAL_DETAILS.csv` + summary tables (PARTS 2, 6).
- `scripts/backtest_stocks_scalp_1m_5m.py` → research-only harness skeleton, data-gated
  (PART 9). Does not run a backtest, does not trade.

### 3. Tests (`tests/test_alert_dispatch_gates.py`)
- freshness classification; very-late → `late_shadow` (not pushed, DO-NOT-CHASE banner);
  fresh → sent with label; plus the existing same-tick exhaustive guard.
- Updated `test_scalp_downgrade` 5–8 and `test_paper_entry_alerts` 10 to use fresh
  timestamps (they now test the intended "fresh non-scalp entry sends" guarantee).

## Deferred (specified, NOT implemented — needs approval)

- **Faster pending-only tracker / monitor-tick entry detection** (PART 4 Option B/A). This
  adds a second concurrent writer to `signal_outcomes`; safe *only* with WAL + a pidfile
  lock + A/B-pending scoping, verified against the live scheduler. Not "clearly safe"
  without that work, so deferred.
- Stocks-intraday entry-validity study (PART 7) — research, not a change.
- Stocks scalp production mode — backtest-gated (PART 8/9).

## Not touched (constraints honored)

No TP/SL, no scoring, no thresholds, no scalp reactivation, no setup-Telegram re-enable,
no C-tier promotion, no stocks swing/invest unpause, no history rewrite, no data deletion,
no auto-trade, no new external dependency.

**PART 11 status: DONE — freshness label + audit tooling shipped; cadence change deferred.**
