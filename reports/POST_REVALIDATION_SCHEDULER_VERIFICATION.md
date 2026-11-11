# Post-Revalidation Scheduler Verification

**Date:** 2026-06-09 · **Scope:** Independent verification that `--revalidate-pending` is active in the default scheduler, the revalidator is behaving inside its spec invariants, and no other surface regressed.

## 1. Scheduler process state

| | Before | After |
|---|---|---|
| Default scheduler PID | 12380 (born 2026-06-09 17:07:48 EEST, **without** --revalidate-pending) | **16684 (born 2026-06-09 20:38:40 EEST, with --revalidate-pending)** ✅ |
| Wrapper (`autostart_scheduler.bat`) | running | still running, auto-relaunched the child |
| Telegram collector PID | 9240 (born 2026-06-09 15:51:39 EEST) | **9240 — unchanged** ✅ |
| Obsidian indexer / other | unchanged | unchanged |

## 2. CLI command verification

The scheduler script now emits the following command for both pre and post tracking steps:
```
python -m src.cli track-signals --all --revalidate-pending
```
Confirmed via import:
```
Pre step cmd: ['...python.exe', '-m', 'src.cli', 'track-signals',
               '--all', '--revalidate-pending']
```

## 3. First-cycle live results

The new scheduler's first tracking pass produced revalidator transitions immediately. Output from `signal_outcomes.notes` (filter `revalidator:` since 17:30 UTC):

| Status | Count | Mode mix |
|---|---:|---|
| `stale_before_entry` | 18 | 12 intraday, 2 swing, 4 invest |
| `entry_moved_away` | 2 | 2 intraday (favorable_excursion_r = 2.33–2.34) |
| **Total transitions** | **20** | first pass, expected one-time backlog |

Verbatim sample row:
```
sig_491a6b0343bd3a51 -> entry_moved_away |
  revalidator: entry_moved_away; favorable_excursion_r=2.33, age=6.6h,
  mode=intraday, peak_at=2026-06-09T16:45:00+00:00
```

The intraday-bucket staleness (15.4h vs 4.0h horizon) is the expected one-time clean-up of yesterday's pending signals that survived the older code's static-expiry policy. Steady-state passes should see far fewer transitions per cycle (only signals freshly aging through their per-mode horizon).

## 4. Invariant checks (post-deploy)

| Invariant | Verification |
|---|---|
| Revalidator did not modify entry/stop/TP/expires_at | Query `SELECT signal_id, entry_low, entry_high, stop_loss, invalidation, tp1, tp2, tp3 FROM proposed_signals WHERE status IN ('stale_before_entry','entry_moved_away')` — same values as before the revalidator ran (checked against `created_at` historical baseline). ✅ |
| Revalidator did not delete rows | Row count for `proposed_signals` unchanged before/after; only status column updated. ✅ |
| Revalidator did not send Telegram | No Telegram alerts fired in the time window matching the transition timestamps. Module has no notifier import. ✅ |
| Headline R-model unchanged | `signal_outcomes.final_r` for transitioned rows is `NULL` (entry never triggered) — same as the prior `waiting_for_entry` / `missed_no_entry` semantics. ✅ |
| Active-signals (still pending) bucket | `waiting_for_entry`: 24 rows — these are the genuinely fresh pending signals (within their per-mode horizons). ✅ |
| Untracked legacy alerts | Unchanged — no crypto alert path touched. ✅ |

## 5. Other system surfaces

| Surface | State |
|---|---|
| Crypto reports (scalp / intraday / swing) | unchanged code path; latest run cleanly produced report file + LLM packet refresh |
| Stocks reports (intraday / swing / invest) | unchanged code path; banners (swing/invest watchlist-only) still render |
| Telegram alert path | untouched; only the supervisor `_format_idea_alert` + watchlist monitor `format_alert` are involved, neither was edited in this PR |
| LLM analysis packets | unchanged code path |
| Obsidian pinned dashboards (00-11) | refresh script `refresh_obsidian_dashboard.py` unchanged; `write_current_state` already surfaces the new statuses via [comment mapping](../scripts/write_obsidian_current_state_dashboard.py) |
| `signal-stats` CLI | unchanged code path; new statuses count as "pending" (zero-R) in the headline metric |

## 6. Sample of the new dashboard render

`11 📌 Trading Desk Current State.md` Open Trades section now shows:
```
- META · SHORT · intraday · tier B · score 68 · [TradingView](...)
  - Created: 2026-06-09 14:29 UTC | Expires: 2026-06-10 14:33 UTC
  - Paper entry: not triggered yet.
  - Entry zone: 594.47 – 598.40 | SL: 606.26 | TP1 582.68 / TP2 574.82 / TP3 563.03
  - Status: stale_before_entry | Current R: open | MFE: — | MAE: —
  - Comment: stale — pending past freshness horizon, manual review
```

## 7. Backout

If a transition turns out wrong, the signal can be manually returned to the active pool:
```sql
UPDATE proposed_signals SET status='waiting_for_entry' WHERE signal_id=?;
```
The next scheduler cycle will re-evaluate it under the same rules. No data loss.

If the flag itself needs to be disabled, the rollback is the inverse single-line edit on `core_pre_steps` and the post step in `run_default_market_schedule.py`. No schema or other code to undo.

## Verdict
```
PENDING_REVALIDATION_ACTIVE_IN_SCHEDULER
```

- New default scheduler **PID 16684** is producing revalidation transitions live (20 in the first cycle, with mode-correct horizons and favorable-excursion math).
- All hard invariants (no level mutation, no deletes, no Telegram, no R rewrite) hold by construction and by spot-check.
- Telegram collector (PID 9240) is unchanged.
- Sibling tabs and reports continue to render with the new statuses surfacing where appropriate.
- 11-point checklist in `SCHEDULER_PENDING_REVALIDATION_INTEGRATION_REPORT.md` passes.
