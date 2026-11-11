# Post-Status-Clarity Fix Report (PART 10)

**Date:** 2026-06-19 · **Type:** UX / Telegram / status-semantics fix. **Display only — no trade logic / scoring / TP-SL / routing / outcomes changed.**

## 1. What was confusing before?
- One word `expired` covered two opposite things: a trade that was **entered** but didn't resolve, and a signal that **never got an entry**.
- `+0R` was shown bare — couldn't tell unresolved-expiry from a true flat close from N/A.
- "no active trades" printed even when waiting / review / entered-unresolved signals existed.
- Review-only / C-tier signals were ambiguous vs actionable.

## 2. What display taxonomy now exists?
Canonical `src/status/display_status.py` (+ Control-Plane mirror `backend/app/display_status.py`) with 9 groups:
`OPEN_ACTIVE · WAITING_FOR_ENTRY · REVIEW_ONLY_SHADOW · ENTERED_UNRESOLVED_EXPIRED · NO_ENTRY_EXPIRED · CLOSED_WIN · CLOSED_LOSS · CLOSED_FLAT · UNKNOWN_INCONSISTENT`.
`derive_display_status(row)` returns display_status/group/reason, operator_label, entry_touched, paper_entered, paper_alert_sent, is_actionable, is_shadow_or_review, is_active_for_operator, r_display_policy, and the should_show_in_* flags.

## 3. How the Telegram monitor now counts
`scripts/paper_monitor_status.py` → `format_paper_monitor_status`:
```
📊 Paper Monitor Status
Open actionable: N · Waiting for entry: N · Entered unresolved: N
Review/Shadow: N · No-entry/stale/moved-away: N · Closed: W/L/Flat
```
If open actionable = 0 but others exist → "No open actionable trades, but there are X waiting and Y review/shadow setups (and Z entered-unresolved)." Top-5 items per bucket with entry-touched / alerted / reason / lifecycle-R.

## 4. How `expired` is split
By `entry_triggered`: **`ENTERED_UNRESOLVED_EXPIRED`** (entry filled, no TP/SL before the window — *not a miss*) vs **`NO_ENTRY_EXPIRED`** (never touched / stale / moved-away). Telegram shows an explicit "Expired split" block; reports expose `expired_after_entry_count` and `no_entry_expired_count`. Full-history: **467 entered-unresolved vs 545 no-entry** (previously one ~1012 "expired" blob).

## 5. How `+0R` is displayed now
`format_r_with_lifecycle(row)` by `r_display_policy`:
- terminal win/loss → `+x.xR` / `-x.xR`
- true flat → `CLOSED FLAT 0R`
- entered-unresolved expiry → `0R display / no TP-SL before expiry (unresolved, not a flat trade)`
- no-entry → `N/A — no entry` · waiting → `N/A — waiting for entry` · shadow → `N/A — review/shadow` · open → `unrealized (open)`

## 6. Were DB / trade outcomes changed?
**No.** Backfill is report-only; it ran read-only over **2077 rows** and wrote **0 rows** (no display columns present). `status`/`entry_triggered`/`final_r`/`final_outcome`/alerts untouched. A test asserts `derive_display_status` never mutates its input.

## 7. Were scoring / TP-SL / routing changed?
**No.** No scoring/tracker/paper_entry/routing/validity/filter file modified. `decide_paper_entry` and Control-Plane `actionability.classify` are unchanged — the display layer only reads their verdict. See `reports/STATUS_CLARITY_SAFETY_VERIFICATION.md`.

## 8. Did tests pass?
- crypto-ai-desk focused: **86 passed** (incl. 15 new `test_display_status`, paper-entry, scheduler plan, telegram, docs).
- Control Plane: **38 passed** (incl. 5 new `test_display_status`); frontend `tsc -b` **exit 0**.
- Docs validator OK.

## 9. Any inconsistent rows found?
Yes — **87** map to `UNKNOWN_INCONSISTENT` (a no-entry status carrying `entry_triggered=1`, or `ambiguous`). Listed in `reports/DISPLAY_STATUS_BACKFILL_REPORT.md` for review; **left untouched** (display surfaces them, never rewrites).

## 10. What should the operator expect in Telegram now?
Six honest buckets instead of one word: open-actionable, waiting, entered-unresolved, review/shadow, no-entry/stale/moved-away, closed (W/L/flat) — plus an explicit expired split and an inconsistent-rows flag. "No active trades" now strictly means **no OPEN actionable paper trade**; waiting/review/entered-unresolved are always shown separately. `+0R` always carries a lifecycle reason.

## 11. What remains for Friday review?
- Separate entered-unresolved vs no-entry expired in the weekly review (checklist item added to `docs/WEEKLY_FORWARD_METRICS.md`).
- Optional follow-up (not done, to avoid touching the live dedup/hash path): adopt `format_r_with_lifecycle` inside `src/notifiers/close_alert.py` so each close alert's R line is lifecycle-aware too. The monitor-status summary already gives the operator the honest view.
- Optional: wire `scripts/paper_monitor_status.py --send-telegram` as a scheduler step once the cadence is chosen.
- Investigate the 87 inconsistent rows' provenance (likely revalidator/tracker re-walk timing) — display-only for now.

## Verdicts
`STATUS_DISPLAY_SEMANTICS_FIXED` · `EXPIRED_SPLIT_READY` · `R_DISPLAY_LIFECYCLE_AWARE` · `TELEGRAM_MONITOR_CLARITY_READY` · `CONTROL_PLANE_DISPLAY_SAFE` · `NO_TRADE_LOGIC_CHANGE`
