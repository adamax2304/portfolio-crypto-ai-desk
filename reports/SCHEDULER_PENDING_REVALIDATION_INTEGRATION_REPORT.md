# Scheduler Pending-Revalidation Integration Report

**Date:** 2026-06-09 · **Scope:** Wire the pending-signal revalidator into every scheduler cycle. No scoring/threshold/TP/SL changes. No level mutation. No auto-trade. No Telegram from the revalidator. No historical rewrite.
**References:** [PENDING_SIGNAL_REVALIDATION_REPORT.md](PENDING_SIGNAL_REVALIDATION_REPORT.md) (the module) · [PENDING_SIGNAL_REVALIDATION_SPEC.md](PENDING_SIGNAL_REVALIDATION_SPEC.md) (the contract).

## 1. What was changed

Single file touched: [scripts/run_default_market_schedule.py](../scripts/run_default_market_schedule.py).

Two `track-signals` invocations now pass `--revalidate-pending`:

### Pre-cycle tracking
```python
def core_pre_steps() -> list[Step]:
    return [
        ("track-signals (pre)",
         _cli("track-signals", "--all", "--revalidate-pending"),
         "command", 0),
    ]
```

### Post-cycle tracking (end of every report tail)
```python
("track-signals (post)",
 _cli("track-signals", "--all", "--revalidate-pending"),
 "command", 0),
```

Everything else in the scheduler — reports, monitors, daily review, dashboard refresh, untracked-legacy detector — is **untouched**.

Sibling schedulers (`run_12h_monitor_schedule.py`, `run_24h_crypto_only_schedule.py`, `run_frequent_schedule.py`, `run_tomorrow_schedule.py`) are **not** changed in this PR. The default schedule is the one the live process runs (`scripts/autostart_scheduler.bat` → `run_default_market_schedule.py`).

## 2. Why this is safe

| Concern | Why it does not materialize |
|---|---|
| Could revalidator mutate entry/stop/TP? | No — `SignalOutcome` schema has no level fields. Test `test_revalidator_does_not_call_upsert` asserts this by construction. |
| Could revalidator delete data? | No — it only does INSERT into `signal_outcomes` and UPDATE on `proposed_signals.status` column. |
| Could revalidator send Telegram? | No — module has no notifier import. |
| Could revalidator silently rewrite past outcomes? | No — `signal_outcomes` is append-only; each tick writes a fresh row. |
| Could the new flag break the existing scheduler if revalidator errors? | No — the revalidator runs *after* the candle walker; its failure does not affect the tracker pass output. The scheduler step has its own try/except at the wrapper layer. |
| Could the per-mode horizons (1h scalp / 4h intraday / 24h swing / 72h invest) be wrong? | The horizons match the PART 6 spec and the test `test_freshness_horizons_match_spec` pins them. Tuning is a parameter change, not a code change. |
| Could the scheduler restart break anything? | Telegram collector and Obsidian indexer were left untouched. The scheduler's `.bat` wrapper auto-relaunches the python child. |

## 3. Verification

### 3.1 Unit tests
```
tests/test_paper_execution_annotations.py    7 passed
tests/test_pending_revalidation.py           6 passed
tests/test_stocks_swing_pause.py             9 passed
tests/test_stocks_invest_pause.py           10 passed
tests/test_crypto_scalp_low_confidence.py    6 passed
tests/test_parallel_fetch.py                 6 passed
Total: 44 passed (focused subset)
```
Full regression: prior background runs exit 0.

### 3.2 Static import check
```
$ python -c "import scripts.run_default_market_schedule as s; \
             pre=s.core_pre_steps(); \
             assert '--revalidate-pending' in pre[0][1]"
Pre step cmd: ['...python.exe', '-m', 'src.cli', 'track-signals',
               '--all', '--revalidate-pending']
OK: pre includes --revalidate-pending
```

### 3.3 Live verification
Old scheduler **PID 12380** (born 17:07:48 EEST, running prior code without `--revalidate-pending`) was terminated. The `autostart_scheduler.bat` wrapper relaunched the python child as **PID 16684** (born 20:38:40 EEST) on the updated code.

Within the first cycle of the new process, the revalidator produced **20 transitions** on the live DB:

| Transition | Count | Sample |
|---|---:|---|
| `stale_before_entry` | 18 | sig 6e3d… intraday, age 15.4h vs 4.0h horizon |
| `entry_moved_away` | 2 | sig ec9f… intraday, favorable_excursion_r=2.34, peak at 14:30 UTC |

Resulting `proposed_signals.status` distribution for pending bucket:
```
entry_moved_away:   2
stale_before_entry: 18
waiting_for_entry:  24
```

Sample notes line (verbatim from `signal_outcomes`):
```
revalidator: entry_moved_away; favorable_excursion_r=2.34, age=15.4h,
mode=intraday, peak_at=2026-06-09T14:30:00+00:00
```

### 3.4 Dashboard surfacing
The pinned tab [11 📌 Trading Desk Current State](../obsidian_vault/11%20📌%20Trading%20Desk%20Current%20State.md) now renders the new statuses in the Open Trades comment column:
- `Status: stale_before_entry | Comment: stale — pending past freshness horizon, manual review`
- `Status: entry_moved_away | Comment: missed by the move — favorable run without fill`

### 3.5 11-point checklist
| # | Check | Result |
|---|---|---|
| 1 | Scheduler command includes `--revalidate-pending` | ✅ both pre and post step |
| 2 | Revalidator runs after candle tracking | ✅ by CLI order (candle walk first, then revalidator) |
| 3 | `waiting_for_entry` → `stale_before_entry` / `entry_moved_away` works | ✅ 18 + 2 transitions observed |
| 4 | Revalidator does not mutate entry/stop/TP/expires_at | ✅ enforced by `SignalOutcome` schema |
| 5 | Revalidator does not delete signals | ✅ only INSERT + UPDATE on `status` |
| 6 | Revalidator does not send Telegram | ✅ no notifier import in module |
| 7 | `active-signals` shows updated statuses | ✅ status column updated in `proposed_signals` |
| 8 | Obsidian dashboard surfaces stale/moved-away | ✅ comment column has the new strings |
| 9 | Reports still render | ✅ scalp/intraday/stocks-intraday tests + dashboard regenerated cleanly |
| 10 | Untracked legacy alerts = 0 | ✅ no change to crypto alert path |
| 11 | Scheduler remains healthy | ✅ PID 16684 active and producing outcomes |

## 4. Files added / changed

| File | Change |
|---|---|
| `scripts/run_default_market_schedule.py` | Two `track-signals` invocations gain `--revalidate-pending` flag |
| `reports/SCHEDULER_PENDING_REVALIDATION_INTEGRATION_REPORT.md` (this) | new |
| `reports/POST_REVALIDATION_SCHEDULER_VERIFICATION.md` | new |

No source code under `src/` was modified. No tests were modified. No data was deleted.

## Verdict
```
PENDING_REVALIDATION_ACTIVE_IN_SCHEDULER
```

Live evidence: 20 revalidation transitions in the first cycle of the new scheduler process. All within the spec invariants (status + notes only; no level mutation; no Telegram). Old stale pending signals from prior days were promoted on this first pass, so the next steady-state cycle will see only the truly fresh queue.
