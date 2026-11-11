# Default Market Schedule — Implementation Report

**Date:** 2026-06-01. Permanent operating loop for the desk.
**Scope:** workflow / scheduling hygiene only.
**Does NOT** auto-trade, change scoring / thresholds / agents / strategy,
or auto-invoke Opus / Claude / any LLM API.

---

## What was implemented

### Files

| Path | Purpose |
|------|---------|
| `scripts/run_default_market_schedule.py` | The scheduler — every-2h loop, weekday/weekend logic, daily-once gate, DLL retry, Telegram retry. |
| `scripts/run_default_market_schedule.bat` | Windows launcher (PowerShell-friendly). |
| `tests/test_default_market_schedule.py` | 17 regression tests — calendar gates, step composition, no-LLM contract, Windows DLL constant. |
| `DEFAULT_SCHEDULE_PRECHECK.md` | Pre-flight check / go-no-go. |
| `DEFAULT_SCHEDULE_WINDOWS_TASK_INSTRUCTIONS.md` | Manual + Task Scheduler instructions. |
| `DEFAULT_MARKET_SCHEDULE_IMPLEMENTATION_REPORT.md` | This file. |

### Daily run folder

```
data/scheduled_runs/YYYY-MM-DD_default_schedule/
    scheduler.log
    cycle_NN_HH-MM_summary.md
    crypto_monitor_*.log
    daily_<UTC-date>.done            # marker; gates swing/invest to once-per-day
    final_daily_default_schedule_review.md
```

Final review also written to `FINAL_DAILY_DEFAULT_SCHEDULE_REVIEW.md` at the project root.

---

## Schedule rules

### Cadence

- **Default**: 24 hours total, 2-hour interval → 12 cycles per run.
- **`--run-once`**: exactly one cycle, then exit. Useful for ad-hoc spot
  checks and for the dry-run tests.
- **`--minutes` / `--interval-minutes`**: smoke-test overrides.

### Weekday vs weekend

| Day | Crypto scalp | Crypto intraday | Crypto swing/invest | Stocks intraday | Stocks swing/invest |
|-----|:------------:|:---------------:|:-------------------:|:---------------:|:-------------------:|
| Mon-Fri | every 2h | every 2h | daily (once) | every 2h | daily (once) |
| Sat-Sun | every 2h | every 2h | daily (once) | **off** | **off** |

`is_weekend()` and `stocks_enabled()` are tested with explicit Sat/Sun and
Mon/Fri datetimes. `--crypto-only` / `--no-stocks` overrides weekday-on-stocks
when the user wants a deliberately crypto-only window.

### Long-horizon (swing / invest) daily-once gate

- Each UTC day has a marker file `daily_<YYYY-MM-DD>.done` inside the run folder.
- The first cycle of the UTC day includes swing/invest steps; subsequent
  cycles skip them and log `long_horizon=no (done earlier)`.
- The marker is written **only after** at least one swing/invest step
  exited ok — a failed first run does not block a retry on cycle 2.

### Stocks scalp

Not present in this CLI. The plan reserves a `note` step
("stocks scalp unavailable in this CLI") so the per-cycle summary records
the gap honestly. Does not fail the cycle.

---

## Commands invoked per cycle

Always:

1. `python -m src.cli track-signals --all`        (pre)
2. `python -m src.cli scalp-report`               (crypto)
3. `python -m src.cli intraday-report`            (crypto)

Weekday-only adds:

4. `(note) stocks scalp report — unavailable`
5. `python -m src.cli stocks-intraday-report`

First cycle of UTC day adds (long-horizon):

6. `python -m src.cli swing-report`               (crypto)
7. `python -m src.cli stocks-swing-report`        (weekday only)
8. `python -m src.cli stocks-invest-report`       (weekday only)

Always (background monitor, end-of-cycle cleanup):

9. `python -m src.cli monitor-watchlist --interval 300 --duration-hours 1.5`
   (background, PID-locked, killed at end-of-cycle)

Tail:

10. `python -m src.cli active-signals --asset-class crypto --limit 20`
11. `python -m src.cli signal-stats --asset-class crypto`
12. (weekday) `python -m src.cli active-signals --asset-class stocks --limit 20`
13. (weekday) `python -m src.cli signal-stats --asset-class stocks`
14. `python -m scripts.detect_untracked_legacy_alerts --since <today>`
15. `python -m src.cli track-signals --all`       (post)
16. `python -m src.cli review-day --no-print --write-obsidian`

Weekday cycle = 13 steps; weekend cycle = 11 steps; weekday first-of-day with long-horizon = 16 steps.

---

## Error handling

### Windows DLL init failure (the cycle-10 case from the 24h crypto-only run)

- Exit code **3221225794** (`0xC0000142` / `STATUS_DLL_INIT_FAILED`) is
  classified as transient infrastructure.
- The scheduler **retries the failing command** with a 60-second backoff,
  up to **2 retries** (3 attempts total). Each retry is logged.
- If all attempts fail, the step is **skipped**, the cycle continues
  with the remaining steps, and the Telegram cycle summary lists the
  failure.
- `tests/test_default_market_schedule.py::test_windows_dll_init_failed_constant_is_correct`
  pins the exit-code constant.

### Telegram ReadTimeout

- The Telegram cycle-summary send tries up to **2 times** (one retry).
- ReadTimeout / Timeout names trigger the retry; other exceptions are
  logged and the cycle continues (no spam).

### Subprocess timeouts / generic exceptions

- Each step is wrapped — failure in one step never kills the loop.
- A 900s timeout per step protects against runaway processes.

### Duplicate monitors

- The crypto monitor PID is written to
  `data/scheduled_runs/<date>_default_schedule/crypto_monitor.pid`.
- Start of each cycle checks the lock — stale PID killed, fresh PID
  started, end-of-cycle kills the child cleanly.

### PC sleep

- Documented in `DEFAULT_SCHEDULE_WINDOWS_TASK_INSTRUCTIONS.md`.
- Not auto-handled — disable sleep or use `--wake-to-run` cautiously.

---

## Tests

```
$ python -m pytest -q
....................................................................... (177 passed in 3:43)
```

| Suite | Result |
|-------|--------|
| `tests/test_default_market_schedule.py` (NEW) | **17 / 17 pass** |
| Full suite (incl. PART 1-5 regressions, ingest, daily review, cooldown, legal-risk, stocks-monitor) | **177 / 177 pass** |

Key tests in the new file:

- `test_saturday_is_weekend`, `test_sunday_is_weekend`,
  `test_monday_is_weekday`, `test_friday_is_weekday` — calendar gate.
- `test_stocks_off_on_weekend`, `test_stocks_on_on_weekday` — pipeline gate.
- `test_force_crypto_only_overrides_weekday` — flag respected.
- `test_weekend_cycle_excludes_all_stocks_commands` — Sat plan has zero
  "stocks" tokens.
- `test_weekday_cycle_includes_stocks_intraday` — Mon plan includes
  stocks intraday + the "unavailable" note for scalp.
- `test_crypto_only_flag_strips_stocks_on_weekday` — Mon plan with
  `crypto_only=True` has zero "stocks" tokens.
- `test_long_horizon_first_cycle_only` — first cycle includes swing +
  stocks-swing + stocks-invest; subsequent cycles do not.
- `test_long_horizon_weekend_excludes_stocks_swing_invest` — Sat
  long-horizon has crypto swing but no stocks swing/invest.
- `test_cycle_always_includes_track_signals_and_detector` — track-pre,
  detector, track-post, review-day always present.
- `test_skip_reports_drops_heavy_steps_but_keeps_tail` — `--skip-reports`
  removes scalp/intraday but tail still runs.
- `test_no_llm_tokens_in_any_cycle_plan` — no `opus / anthropic /
  claude api / enriched-review` tokens in any cycle plan, ever.
- `test_windows_dll_init_failed_constant_is_correct` — constant pinned.

---

## Dry-run validation

```
$ python -m scripts.run_default_market_schedule --dry-run
2026-06-01 00:06:16 [INFO] === DRY RUN ===
2026-06-01 00:06:16 [INFO] cycle 1  @ Mon 00:06 (weekday, stocks=on, steps=16)   ← +long-horizon
2026-06-01 00:06:16 [INFO] cycle 2  @ Mon 02:06 (weekday, stocks=on, steps=13)
2026-06-01 00:06:16 [INFO] cycle 3  @ Mon 04:06 (weekday, stocks=on, steps=13)
...
2026-06-01 00:06:16 [INFO] cycle 12 @ Mon 22:06 (weekday, stocks=on, steps=13)
2026-06-01 00:06:22 [INFO] validate track-signals              OK
2026-06-01 00:06:27 [INFO] validate scalp-report               OK
2026-06-01 00:06:32 [INFO] validate intraday-report            OK
2026-06-01 00:06:37 [INFO] validate swing-report               OK
2026-06-01 00:06:42 [INFO] validate active-signals             OK
2026-06-01 00:06:46 [INFO] validate signal-stats               OK
2026-06-01 00:06:50 [INFO] validate monitor-watchlist          OK
2026-06-01 00:06:54 [INFO] validate review-day                 OK
2026-06-01 00:06:57 [INFO] validate stocks-intraday-report     OK
2026-06-01 00:07:00 [INFO] validate stocks-swing-report        OK
2026-06-01 00:07:04 [INFO] validate stocks-invest-report       OK
2026-06-01 00:07:04 [INFO] --- LLM-auto-invoke check OK (no Opus/Claude tokens in plan) ---
2026-06-01 00:07:04 [INFO] === dry run complete ===
```

`--dry-run --crypto-only --run-once` also validated cleanly (no stocks
commands present, no LLM tokens).

---

## How to start

```powershell
cd C:\Users\adama\Documents\crypto-ai-desk
.\scripts\run_default_market_schedule.bat --hours 24 --interval-hours 2 --send-telegram
```

For Task-Scheduler integration: see `DEFAULT_SCHEDULE_WINDOWS_TASK_INSTRUCTIONS.md`.

## How to stop

- **Foreground**: `Ctrl+C` in the PowerShell window.
- **Background / Task Scheduler**: `schtasks /End /TN "CryptoAIDesk_Default_24h"`.

## Known limitations

- **No execution layer** anywhere in the project — this is by design and inherited from upstream. Auto-trade impossible.
- **No automatic Opus / enriched-review trigger** — also by design.
  Use the `enriched-review` skill manually when you want a deeper review.
- **PC sleep is fatal** — the loop sleeps in 30s chunks; Windows sleep
  pauses Python `time.sleep` but resumes immediately on wake. Long
  sleeps (>2h) mean missed cycles. Disable sleep for unattended runs.
- **No web access in the deterministic pipeline** — Reddit social
  attention has been returning 403 for 6+ cycles in the prior run.
  This is a degraded crowd-attention input but does not break the
  cycle; the news_items pipeline still loads RSS data.
- **No auto-restart on hard crash** — Windows Task Scheduler triggers
  once per day; mid-day crashes mean lost cycles until the next trigger.
  The cycle-10 DLL retry mitigates the most common observed Windows
  transient.

---

## Safety statement

- No auto-trade — no execution layer exists in `src/`.
- No scoring / threshold / agent / strategy code changed.
- No Opus / Claude / Anthropic auto-call — gated by code (no imports),
  by test (`test_no_llm_tokens_in_any_cycle_plan`), and by dry-run check
  (rejected if any forbidden token appears in the rendered plan).
- All existing Telegram safety gates inherited:
  - **PART 1** registration-before-alert (no untracked alerts).
  - **PART 2** 45-min cooldown on `entry_change` / `score_improvement` /
    `invalidation_change`; `new_signal` and `tier_upgrade` bypass.
  - **PART 3** legal-headline-risk block for stocks A/B.
- Read-only with respect to `proposed_signals` / `signal_outcomes`
  schema — the scheduler is a thin orchestration layer over existing
  CLI commands.
- The news_trader bridge remains READ-ONLY (no writes to that repo).
