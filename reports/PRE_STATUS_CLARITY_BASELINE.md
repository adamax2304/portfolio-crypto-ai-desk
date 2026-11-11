# Pre-Status-Clarity Baseline Audit (PART 0)

**Date:** 2026-06-19 · **Type:** read-only baseline for the status-display-clarity fix. **No trade logic touched.**

## 1. Status fields that exist in the DB
- `proposed_signals.status` (TEXT) — lifecycle status.
- `signal_outcomes.status` (TEXT) — per-check status snapshots.
- `signal_outcomes.entry_triggered` (0/1) — **the key flag**: was the entry zone/trigger touched.
- `signal_outcomes.final_outcome` (win/loss/expired/not_triggered/ambiguous/None).
- `signal_outcomes.final_r`, `max_favorable_excursion_r` (MFE), `max_adverse_excursion_r` (MAE).
- `signal_alerts` rows (paper-entry / close alerts) — presence ⇒ an alert was sent.

## 2. Status values that exist (proposed_signals.status)
`generated · waiting_for_entry · triggered · tp1_hit · tp2_hit · tp3_hit · stopped · invalidated_before_entry · expired · missed_no_entry · stale_before_entry · entry_moved_away · cancelled_by_regime_change · cancelled_by_news · ambiguous · reviewed`
Constants in `src/signals/models.py:18-31`; `stale_before_entry`/`entry_moved_away` come from `src/signals/revalidator.py`.

## 3. Where `expired` is generated
- `src/signals/tracker.py` `_classify`: `expired` when **entry WAS triggered** but no TP/stop before `expires_at`; `missed_no_entry` when entry never touched.
- `src/signals/revalidator.py`: `stale_before_entry` (Rule R1 — age ≥ mode freshness horizon, no fill, no >2R move) and `entry_moved_away` (Rule R2 — favorable excursion ≥ 2R but never filled).
- **Empirical (DB):** `expired` → `entry_triggered=1` for **483/483**; `missed/stale/moved_away` → mostly `entry_triggered=0`. So "expired" is overwhelmingly an *entered-but-unresolved* state, while the no-entry states are distinct.

## 4. Where `+0R` / R is displayed
- `src/notifiers/close_alert.py:211` — `f"Result: {raw_r_f:+.1f}R raw / {sized_r:+.1f}R sized"`.
- `src/signals/obsidian_export.py:102` — `f"- Final R: {_fmt(latest.get('final_r'))}"`.
- `src/signals/analytics.py` — R bucketing.
- Control Plane `frontend/src/screens.tsx` — `fmtR()` for Today PnL / Open risk / final_r.
- **Gap:** none of these explain *why* R is 0 — an `expired`-after-entry (no TP/SL) shows the same "0R" as a true flat close.

## 5. Where "no active …" is generated
- `src/cli.py:969` — `console.print("[dim]no active signals[/dim]")` (active-signals CLI when zero rows).
- Control Plane `frontend/src/screens.tsx:137-142` empty states: `"No open trades"`, `"No pending entries"`, etc.

## 6. Where the Telegram app summary comes from
- The per-cycle Telegram summary (`scripts/run_default_market_schedule.py:860-876`) reports **step ok/failed only** — no trade-status counts.
- The Control Plane Mini App reads via `backend/app/desk_adapter.py` (`list_signals` → normalized dict → `actionability.classify`) and the frontend buckets by `actionability.status`.

## 7. Where the Control Plane "active trades" count comes from
- `frontend/src/screens.tsx:23-24`: `open = entry_triggered_at && !final_outcome && actionability.status!=="closed"`; `pending = actionability.status==="actionable" && !entry_triggered_at`.
- Backend `desk_adapter.py:159-175` `trades(bucket)` buckets open/pending/closed/shadow using raw status + actionability. **Already logic-based (good).**

## 8. Examples of confusing current output
- A row shows `expired` with `final_r` blank/0 — operator can't tell it was **entered then unresolved** vs **never entered**.
- "no active signals" prints even when many `waiting_for_entry` / C-tier review signals exist.
- "+0R" on an expired-after-entry reads like a flat trade.
- One raw `Expired: N` count mixes entered-unresolved + no-entry/stale/moved-away + old-tail.

## 9. What WILL be changed (display/semantics only)
- New canonical module `src/status/display_status.py` (`derive_display_status`, `format_r_with_lifecycle`, `summarize_display_states`, `format_paper_monitor_status`).
- A read-only backfill/report script `scripts/backfill_display_status.py` (no destructive migration).
- New Telegram monitor-status formatter (additive) + report counts split by display group.
- Control Plane: **optional** display_* fields passed through in `desk_adapter.py` + optional TS fields; no behavior change.
- Docs + tests + reports.

## 10. What will NOT be changed
`status` values, `entry_triggered`, `final_r`, `final_outcome`, alerts, scoring, TP/SL, entry logic, routing/actionability, validity windows, filters, live/scalp/BE-partial-trailing, historical outcomes. Display layer only.
