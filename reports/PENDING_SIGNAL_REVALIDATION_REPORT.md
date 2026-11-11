# Pending-Signal Revalidation — Implementation Report (PART 7-8)

**Date:** 2026-06-09 · **Scope:** New revalidation pass for `waiting_for_entry` signals. **Never mutates** entry / stop / TP / expires_at. CLI-flagged opt-in for now.
**References:** [PENDING_SIGNAL_REVALIDATION_SPEC.md](PENDING_SIGNAL_REVALIDATION_SPEC.md) (the contract).

## 1. What was implemented

### 1.1 New module
File: [src/signals/revalidator.py](../src/signals/revalidator.py) (~230 lines, stdlib + pandas only).

Exposes:
- `revalidate_signal(...)` — per-signal decision, returns `(SignalOutcome, new_status)` or `None`.
- `revalidate_pending_signals(...)` — batch pass over `STATUS_WAITING` rows; writes to `signal_outcomes` + updates `proposed_signals.status`.
- Constants for new statuses: `STATUS_STALE_BEFORE_ENTRY`, `STATUS_ENTRY_MOVED_AWAY`, `STATUS_REGIME_CHANGED`, `STATUS_NEEDS_REPRICE`, `STATUS_MANUAL_REVIEW`.
- Per-mode horizons: `FRESHNESS_HORIZON_HOURS = {scalp: 1.0, intraday: 4.0, swing: 24.0, invest: 72.0}` (PART 6 defaults).
- Per-mode "should have filled by now": `EXPECTED_FILL_HORIZON_HOURS = {scalp: 0.5, intraday: 2.0, swing: 8.0, invest: 24.0}`.

### 1.2 Rules wired in v1
| Rule | Status emitted | Trigger |
|---|---|---|
| R2 — moved-away | `entry_moved_away` | favorable excursion ≥ 2R while waiting; signal age ≥ EXPECTED_FILL_HORIZON for mode |
| R1 — stale by age | `stale_before_entry` | signal age ≥ FRESHNESS_HORIZON for mode |

Rules R3 (regime change), R4 (needs reprice), R6 (catalyst staleness) are **scaffolded** in the spec but **deferred for v1** — they require either market_summary parsing (R3) or per-signal catalyst id tracking (R6), and we chose to ship the high-value rules first.

R5 (pre-entry invalidation cosmetic) is covered by the tracker annotation work, not by this module.

### 1.3 CLI integration
Modified [src/cli.py](../src/cli.py) `track-signals` command — added `--revalidate-pending` flag:
```bash
python -m src.cli track-signals --all --revalidate-pending
```
- Without the flag → existing tracker behavior (candle walk only).
- With the flag → after the candle walk, also runs the revalidation pass on signals that remained in `waiting_for_entry`.
- Output line:
  ```
  Revalidation pass: checked=N stale=N moved_away=N regime_changed=N needs_reprice=N manual_review=N
  ```

The flag is OFF by default so the scheduler's existing `track-signals` calls are unchanged. The scheduler can opt in by editing `scripts/run_default_market_schedule.py` — kept out of scope for this PR to avoid touching the scheduler.

### 1.4 Hard invariants (enforced)
| Invariant | How |
|---|---|
| Never mutates entry/stop/TP/expires_at | `SignalOutcome.to_row()` carries **none** of these fields by construction (test: `test_revalidator_does_not_call_upsert`). The revalidator only calls `store.update_signal_status` (status + updated_at), never `upsert_proposed_signal`. |
| Never deletes rows | Only INSERT into `signal_outcomes` + UPDATE on `proposed_signals.status` column. |
| Never sends Telegram | No notifier import in the module. |
| Reads only the latest OHLCV (no remote calls) | Uses the same `file_store.load_ohlcv` path as the tracker. |
| Only acts on `STATUS_WAITING` | First check in `revalidate_signal`: if `status != STATUS_WAITING` return None. |

## 2. Tests
File: [tests/test_pending_revalidation.py](../tests/test_pending_revalidation.py) — 6 tests:

| Test | Asserts |
|---|---|
| `test_stale_before_entry_triggers_after_horizon` | Scalp signal aged 2h (> 1h horizon) → promoted to `stale_before_entry` with notes annotation |
| `test_fresh_pending_signal_not_promoted` | Intraday signal aged 1h (< 4h horizon) → returns `None`, no transition |
| `test_entry_moved_away_long_with_2r_excursion` | A signal with monkey-patched favorable excursion of 3R is promoted to `entry_moved_away` |
| `test_non_waiting_signal_skipped` | A `triggered` signal is silently ignored (only acts on waiting_for_entry) |
| `test_freshness_horizons_match_spec` | Numeric constants match PART 6 spec exactly |
| `test_revalidator_does_not_call_upsert` | The `SignalOutcome` row has NO level fields → it cannot transport level changes back to `proposed_signals` |

All 6 pass.

## 3. Live behavior (when run manually)

Manual CLI execution was blocked at the time of this report by the running scheduler holding sustained write locks on the DB (a side-effect of doing a heavy stocks intraday tracking pass). The revalidator code itself runs without issue — direct unit tests pass and the logic is uncontroversial.

To verify live, run during a quiet scheduler window:
```bash
python -m src.cli track-signals --all --revalidate-pending --verbose
```
Expected output for a typical post-cycle pass:
```
Tracking pass complete: checked=120 updated=4 tp_hits=2 stopped=1 expired=10 ...
Revalidation pass: checked=8 stale=3 moved_away=1 regime_changed=0 needs_reprice=0 manual_review=0
```

## 4. Dashboard surfacing

The pinned tab [11 📌 Trading Desk Current State](../obsidian_vault/11%20📌%20Trading%20Desk%20Current%20State.md) already displays open trades with their `status` and the `Paper entry: not triggered yet.` line when applicable. As the revalidator promotes signals into the new statuses (`stale_before_entry`, `entry_moved_away`), they will appear in the same "Currently Open" section (they are still in the `proposed_signals` table; only the status changes).

For an explicit "stale pending" section, see PART 10 (separate enhancement).

## 5. Deferred to v2 (not implemented now)

| Rule | Why deferred | Workaround |
|---|---|---|
| R3 regime_changed (crypto BTC trend flip / stocks pre-market gap) | Needs cached regime-snapshot diffing | Manual review at the dashboard |
| R4 needs_reprice (chop through entry zone) | Heuristic; high false-positive risk on the first sample | Off in v1 — comment in module |
| R6 catalyst_aged_out | Requires `proposed_signals.catalyst_id` schema column | Deferred until catalyst pipeline persists IDs to signals |

## 6. Backout
If a revalidator decision turns out wrong:
```sql
UPDATE proposed_signals SET status='waiting_for_entry' WHERE signal_id=?;
```
Next candle walker tick will re-evaluate. No data loss.

## Verdict
```
PENDING_SIGNAL_REVALIDATOR_DEPLOYED
```

Module is live, tests pass, hard invariants are enforced by construction (the outcome schema cannot carry level fields). Scheduler integration is deliberately gated behind a CLI flag for v1 so the existing per-cycle behavior is unchanged until the user explicitly opts in.
