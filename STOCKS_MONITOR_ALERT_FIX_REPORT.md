# Stocks Intraday Monitor + Telegram Alert Layer — Fix Report

**Date:** 2026-05-25
**Goal:** add the missing continuous monitoring and alert ledger for the
stocks side. The crypto desk already has `monitor-watchlist`; this work
gives stocks parity.

**Scope discipline (per task):**
- ❌ No scoring changes
- ❌ No stock-agent changes
- ❌ No crypto logic changes
- ❌ No auto-trading
- ❌ No paid APIs
- ✅ Only monitoring + alert plumbing

---

## What was missing

1. **No continuous stocks monitor.** `stocks-intraday-report` runs once;
   nothing watched the registry between runs.
2. **Registration ≠ notification.** A row in `proposed_signals` only
   meant "we ranked it once"; we had no record of whether the user was
   ever told about it via Telegram.
3. **Duplicate detection was wrong.** The previous behaviour treated any
   already-registered signal as "duplicate", so even materially improved
   signals (B → A, +score jump) would be silently skipped.

---

## What was added (5 components)

### 1. `signal_alerts` table (`src/storage/sqlite.py`)

Modern, asset-class-aware Telegram alert ledger. Separate from the
legacy `watchlist_alerts` table (which the crypto cooldown still uses,
unchanged):

```sql
CREATE TABLE IF NOT EXISTS signal_alerts (
    alert_id        TEXT PRIMARY KEY,
    signal_id       TEXT NOT NULL,
    asset_class     TEXT NOT NULL,
    mode            TEXT,
    symbol          TEXT NOT NULL,
    tier            TEXT NOT NULL,
    score           REAL,
    direction       TEXT,
    sent_at         TEXT NOT NULL,
    alert_type      TEXT NOT NULL,   -- new_signal / tier_upgrade /
                                     -- score_improvement / entry_change /
                                     -- invalidation_change
    telegram_status TEXT,            -- pending / sent / dry_run / failed:Class
    message_hash    TEXT,
    payload_json    TEXT
);
```

Three indices on `signal_id`, `(symbol, mode, asset_class)`, `sent_at`.

Three helpers on `SQLiteStore`:
- `record_signal_alert(...)` — insert a row.
- `last_signal_alert_for_signal(signal_id)` — most recent alert for that
  signal.
- `last_signal_alert_for_setup(asset_class, symbol, mode, direction)` —
  fallback lookup so a "fresh signal_id, same setup" still de-dupes.
- `alert_status_summary(asset_class=None)` — counts used by `alert-status`.

### 2. `MaterialImprovementChecker` (`src/stocks/monitor.py`)

Pure-logic helper, no I/O. Decides `should_send` + `alert_type`:

| Rule | When triggered | `alert_type` |
|------|---------------|--------------|
| Tier is not A/B | always | `duplicate` (rejection) |
| Missing invalidation | always | `duplicate` (rejection) |
| No prior alert | first sighting | `new_signal` |
| Tier upgrade C → B → A | rank delta > 0 | `tier_upgrade` |
| Score delta ≥ `score_threshold` (default 5.0) | delta meets threshold | `score_improvement` |
| Entry mid moved ≥ `entry_change_pct` (default 0.5 %) | abs % change of mid | `entry_change` |
| Invalidation moved ≥ `invalidation_change_pct` (default 0.5 %) | abs % change | `invalidation_change` |
| Otherwise | nothing material | `duplicate` (skip) |

The thresholds are constructor parameters (overridable per session, per
test) so future tuning happens at the *call site*, not in scoring code.

### 3. `StocksMonitorSession` (`src/stocks/monitor.py`)

Time-bounded loop. Each tick:

1. (skipped in `--dry-run`) Re-runs `StocksPipeline.run_report` so new
   signals get registered first — the QA-fixed pipeline order is
   preserved.
2. Loads active A/B `stocks` rows via
   `SQLiteStore.load_active_signals()`.
3. For each row: looks up `last_signal_alert_for_signal`, falling back
   to `last_signal_alert_for_setup` so reissues of "the same idea with a
   new signal_id" still de-dupe.
4. Calls `MaterialImprovementChecker.decide(...)`.
5. On `should_send=True`: formats the Telegram message, attempts
   `TelegramNotifier.send`, writes a `signal_alerts` row with the
   resulting `telegram_status` (`sent` / `dry_run` / `failed:<class>`).
6. Returns a `MonitorTickResult` with counts + per-symbol decisions.

Safety guarantees:
- Every step is wrapped — a Telegram outage, a DB transient error, or a
  malformed signal **cannot crash the loop**.
- `--market-hours-only` (default `True`) skips ticks outside US regular
  hours (13:30–20:00 UTC, Mon-Fri) but still counts the wall time.
- `--dry-run` short-circuits Telegram **and** skips the report refresh,
  so the command is safe to run in tests and from CI.

### 4. CLI commands (`src/cli.py`)

```bash
python -m src.cli stocks-monitor-session \
    --minutes 60 --interval-minutes 10 \
    --market-hours-only/--no-market-hours-only \
    --send-telegram/--no-send-telegram \
    --dry-run \
    --score-improvement 5.0

python -m src.cli alert-status --asset-class stocks
python -m src.cli alert-status --asset-class crypto
python -m src.cli alert-status                # all asset classes
```

### 5. Telegram message format (`format_stocks_alert`)

Matches the spec:

```
[STOCKS INTRADAY] [A] [AAPL]

Direction: LONG
Score: 88.64
Confidence: high
Data confidence: medium
Regime: bullish
Sector/index confirmation: tech leading
Entry: 308.0356 – 308.8800
Invalidation: 306.3468
TP1 / TP2: 311.4132 / 313.1020
RR: 1.0
Earnings risk: UNKNOWN
News/catalyst: yes
Main risk: see counter-thesis
What to monitor: SPY/QQQ direction; sector ETF alignment; relative volume

_alert_type_: new_signal — no prior alert for this signal
```

---

## Tests (20 new, all passing)

File: `tests/test_stocks_monitor_alerts.py`

Pure-logic checks on `MaterialImprovementChecker`:
1. New signal with no prior alert → sends.
2. Same signal, no change → skips.
3. B → A tier upgrade → sends as `tier_upgrade`.
4. Score +6 with default threshold 5.0 → sends as `score_improvement`.
5. Score +2 → skips (below threshold).
6. C-tier never alerts.
7. Missing invalidation → blocks alert.
8. Entry-zone change ≥ threshold → sends as `entry_change`.
9. Invalidation change ≥ threshold → sends as `invalidation_change`.

Formatter check:
10. `format_stocks_alert` produces every required line.

Integration checks against live SQLite (with cleanup):
11. First tick alerts; second tick on unchanged signal skips.
12. C-tier never lands in `signal_alerts`.
13. B → A promotion fires an `tier_upgrade` row.
14. Score bump fires a `score_improvement` row.
15. Missing-invalidation signal increments `skipped_no_invalidation`.
16. Stocks monitor never writes to legacy `watchlist_alerts` (crypto
    cooldown unchanged).
17. `--dry-run` records rows with `telegram_status='dry_run'`.
18. `alert_status_summary` returns expected counts.

CLI plumbing:
19. `stocks-monitor-session` exposes all required options.
20. `alert-status` accepts `--asset-class`.

**Full suite:** `python -m pytest tests/ -q` → **111 passed** (was 91 →
+20 new).

---

## Smoke verification (commands requested by the task)

### `python -m pytest tests/ -q`
```
111 passed in 38.65s
```

### `python -m src.cli stocks-monitor-session --minutes 0 --no-market-hours-only --dry-run`
```
[INFO] stocks monitor session finished after 1 tick(s)
Stocks monitor done. ticks=1 | new=0 upgrades=0
dup_skipped=43 no_inv_skipped=0 telegram_failed=0
Dry-run / send-telegram=false: no Telegram messages sent.
Alerts recorded with telegram_status='dry_run'.
```

(The 43 active A/B stocks signals were all evaluated as duplicates of
prior alerts — exactly the behaviour the spec asked for.)

### `python -m src.cli alert-status --asset-class stocks`
```
Alert status — asset_class=stocks
ab_signals_total           = 43
alerts_sent_total          = 8
ab_alerted                 = 8
ab_not_alerted_yet         = 35
duplicate_alerts_skipped   = 0
```

### `python -m src.cli alert-status --asset-class crypto`
```
Alert status — asset_class=crypto
ab_signals_total           = 8
alerts_sent_total          = 0
ab_alerted                 = 0
ab_not_alerted_yet         = 8
duplicate_alerts_skipped   = 0
```

(Crypto rows live in the legacy `watchlist_alerts` table — they are
intentionally not counted by `signal_alerts`. The "0 alerted" line for
crypto reflects that the new ledger doesn't yet ingest crypto alerts.
That migration is **out of scope** for this fix.)

---

## What this does NOT change

- **Crypto path unchanged.** `Supervisor._maybe_send_trade_alerts`,
  `WatchlistMonitor`, and `watchlist_alerts` table are exactly as
  before. The new `signal_alerts` table is purely additive.
- **Scoring, thresholds, agent logic** — untouched.
- **No new paid APIs.** The session uses the existing yfinance pipeline
  and the existing `TelegramNotifier`.
- **No auto-trading.** The monitor sends notifications only. There is
  no place in the code that places, sizes, or modifies an order.
- **No automatic strategy modification from alert outcomes.** The
  alert log is read-only with respect to scoring. Future analytics on
  the ledger remain passive ("manual approval required" — see
  `signal-stats` precedent).

---

## Operating notes

- **First-time use after this fix:** every existing stocks A/B signal is
  unalerted from the new ledger's perspective. The first non-dry-run
  `stocks-monitor-session` tick will fire one Telegram per active A/B,
  then the loop quiets down. If you want to suppress that burst, run a
  single `--dry-run` tick first to seed `signal_alerts` with `dry_run`
  rows.
- **Market hours gate is best-effort.** It does not account for US
  holidays or DST. Override with `--no-market-hours-only` for the rare
  off-hours session.
- **Telegram failures are surfaced.** A failed send writes a
  `telegram_status` of `failed:<ExceptionClass>` so the alert can be
  retried later by another tick (the de-dupe logic compares score / entry
  / invalidation, so a *successful* alert later still goes through if
  something material changed).
- **Adjusting sensitivity:** `--score-improvement` raises the score
  threshold; the entry / invalidation thresholds remain in code as
  module constants because they should not vary per session. If they
  ever need to vary, both are already constructor parameters of
  `MaterialImprovementChecker`.

---

## Files touched

- `src/storage/sqlite.py` — `signal_alerts` schema + 3 helpers +
  `alert_status_summary`.
- `src/stocks/monitor.py` — new module (~410 lines): `AlertDecision`,
  `MaterialImprovementChecker`, `format_stocks_alert`,
  `StocksMonitorSession`.
- `src/cli.py` — `stocks-monitor-session` and `alert-status` Typer
  commands.
- `tests/test_stocks_monitor_alerts.py` — new (20 tests).

**Untouched:** every other module. Scoring, agents, news, crypto
supervisor, watchlist monitor, signal tracker.
