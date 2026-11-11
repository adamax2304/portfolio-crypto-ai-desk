# Pending-Signal Revalidation — Spec (PART 5)

**Date:** 2026-06-09 · **Scope:** A new pass that decides whether `waiting_for_entry` signals are still actionable, **without mutating their levels**. Read-mostly: it can only change `status` and append a `notes` annotation.

## 1. Problem

Today the tracker only asks: *did the OHLCV touch entry / stop / TP?* It never asks: *is the thesis still valid given the new tape?* Pending signals accumulate in dashboards until they either get filled, get invalidated (price hits the stop without entry), or expire on the static `expires_at` clock.

User-visible symptoms:
- Stale pending signals clutter the open-trades list.
- A signal whose thesis was "BTC reclaims X then push toward Y" can still be pending after BTC failed to reclaim and rolled over — the entry might still be technically valid as a price level, but the **structure has changed**.
- A scalp signal whose 2h validity window is partially gone is still "waiting" even though only 20 minutes remain.

## 2. Goals
- Detect 6 categories of stale-ness on pending signals.
- Mark them with a new status (or append annotation), **without rewriting** entry / stop / TP / expires_at.
- Surface them in dashboards so the user can manually act.

## 3. Statuses introduced (additive)

These are new strings; existing rows are unaffected.

| New status | Trigger | Treated as |
|---|---|---|
| `stale_before_entry` | signal is past `freshness_horizon_hours` for its mode (see PART 6) but `expires_at` not yet reached and entry hasn't triggered | C-tier in dashboards; no Telegram alert |
| `entry_moved_away` | price moved ≥ 2R *away* from entry zone in the favorable direction without filling (long signal where price ran up without pulling back; short signal where price dumped without bouncing) | C-tier; surface in dashboard as "missed-entry" |
| `invalidated_before_entry` | already covered by the tracker's pre-entry invalidation logic; rename the existing `missed_no_entry` to this for clarity (optional, deferred) | unchanged in stats |
| `regime_changed` | BTC trend flipped (crypto) OR stocks session transitioned (e.g., signal created in pre-market and US RTH opened with a gap > 1% against direction) | C-tier; manual review |
| `needs_reprice` | structural break visible on chart but entry/stop levels could still be revised — flagged only, never auto-revised | C-tier; manual review |
| `manual_review_required` | catch-all when none of the above match but the heuristic confidence is low | C-tier; manual review |

`waiting_for_entry` remains the default for fresh pending signals. The revalidator only **promotes** to one of the above when a clear condition is met.

## 4. Detection rules (read-only checks)

### Rule R1 — `stale_before_entry`
- Trigger: `now() - created_at >= mode_freshness_horizon_hours(mode)`
- Mode freshness horizons (PART 6):
  - scalp: 1.0 h
  - intraday: 4.0 h
  - swing: 24 h
  - invest: 72 h
- Action: mark `status=stale_before_entry`, append note. Do NOT change expires_at.

### Rule R2 — `entry_moved_away`
- Trigger: latest closed candle's `close` is ≥ 2 × (entry_high − invalidation) for LONG above entry_high; symmetric for SHORT.
- Means: the favorable move happened without filling.
- Action: mark `status=entry_moved_away`, note `price_moved_away_at=<ts>`.

### Rule R3 — `regime_changed`
- Crypto: pull current regime label from the latest `data/processed/market_summary/last_update.json`; if `regime.label` is now `range/chop` or `bearish trend` AND the signal is a LONG, OR `bullish trend` AND signal is SHORT → mark `status=regime_changed`.
- Stocks: if `signal.created_at` was in pre-market UTC hours (13:00–13:30 UTC for US) AND first RTH candle gapped > 1% against direction → mark.

### Rule R4 — `needs_reprice`
- Trigger: signal age > 1.5× the mode's typical "first-fill" time (scalp: 30 min, intraday: 2h, swing: 8h) AND price is **within 0.5R** of entry but hasn't filled, OR price chopped through entry zone repeatedly without sustained fill.
- This is heuristic; default OFF in v1 (deferred — flag in notes only).

### Rule R5 — pre-entry invalidation
- Already covered by the existing tracker. Cosmetic: rename `STATUS_MISSED_NO_ENTRY` → `STATUS_INVALIDATED_BEFORE_ENTRY` (already defined in `src/signals/models.py`, just not used). Wire it in tracker `_classify` only when the cause is invalidation hit, not generic expiry. (Optional, can be deferred.)

### Rule R6 — catalyst staleness
- Trigger: signal carries `news_supported=1`, but the source catalyst event ID is no longer in `data/catalysts/<today>/catalyst_events.jsonl` (catalyst rolled over).
- Action: mark `status=manual_review_required`, note `catalyst_aged_out`.
- (Deferred — requires catalyst-id tracking on signals; v2.)

## 5. Hard constraints (what the revalidator MUST NOT do)
- **Must not change** entry_low / entry_high / entry_trigger / stop_loss / invalidation / tp1 / tp2 / tp3.
- **Must not change** expires_at, validity_window_hours.
- **Must not delete** any rows.
- **Must not send Telegram.**
- **Must not register a "revised" signal** in the same scope as the original. If we ever support reprice, it requires:
  - A new `signal_revisions` table (additive), or
  - A new `signal_id` for the revised setup, with a back-reference column `parent_signal_id`.
  - Until that schema lands, reprice is OFF and the revalidator only marks `needs_reprice` for human action.

## 6. CLI surface (additive)

New flag on the existing `track-signals` command:
```
python -m src.cli track-signals --revalidate-pending
```
- Without the flag → existing tracker behavior (candle walk).
- With the flag → also runs revalidation pass after the candle walk.

For dashboards: the existing `active-signals` CLI will continue to render all open signals; new statuses appear as additional rows with their cap reason in the notes column. No change to existing output for `waiting_for_entry` rows.

## 7. Ordering with the candle walker
1. Candle walker runs first (existing behavior).
2. If candle walker promotes a signal to `triggered` / `stopped` / `tp*_hit` / `expired` — revalidator skips it (the outcome is now decided).
3. Only signals still in `waiting_for_entry` after the candle walker are eligible for revalidation.
4. Revalidator picks the FIRST matching rule (priority: invalidation > entry_moved_away > regime_changed > stale > needs_reprice > manual_review_required). It does not stack statuses.

## 8. Observability
- Each revalidation tick writes one row to `signal_outcomes` with the new `status`, `entry_triggered=0`, and a `notes` field describing the trigger (e.g., `revalidator: stale_before_entry; age=5.2h, freshness_horizon=4.0h`).
- A summary line is added to the CLI output: `revalidated: stale=N, moved_away=N, regime_changed=N`.

## 9. Backout
If a revalidator decision turns out wrong (e.g., user disagrees with the staleness call), the signal can be re-promoted manually:
```
UPDATE proposed_signals SET status='waiting_for_entry' WHERE signal_id=?
```
(This is a manual SQL step; we do not build a UI for it in v1.) The next candle walker tick will re-evaluate from the latest OHLCV.

## 10. Acceptance criteria
1. No level mutation in `proposed_signals` rows: enforced by code path that never calls `upsert_proposed_signal` from the revalidator.
2. New statuses are visible in `active-signals` output.
3. Tests cover R1 (stale by age), R2 (moved-away), R5 (pre-entry invalidation cosmetic), and the "do not mutate levels" invariant.
4. Existing tracker tests still pass.
