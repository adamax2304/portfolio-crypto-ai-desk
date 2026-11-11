# MSTR 184min LATE / MISSED ENTRY — ROOT CAUSE + FIX (PART 9)

**Scope:** PAPER / read-model + UI. Date: 2026-06-24.

## Investigation (live DB, `sig_f2fc71137a472dfc` MSTR short)
| field | value |
|---|---|
| signal created | 2026-06-24 14:09:51 |
| entry triggered | 2026-06-24 14:15:00 (**+6 min** — NOT late) |
| entry price used | 98.67 |
| outcome | **expired +0R**, MFE only **0.36R** (chopped flat) |
| "very late 184m" | = `now − entry_triggered_at` ≈ 184 min at view time |

## Answers to the operator's questions
- **Actual execution latency?** No — entry triggered 6 min after the signal.
- **Stale signal / scheduler / data delay?** No — timestamps are tight; the tracker
  evaluated on schedule.
- **Frontend calculation?** **Yes — this is the bug.** `actionability.classify()` returned
  `status:"closed"` for the terminal/expired trade **but still attached the freshness
  dict** with "very late 184m — DO NOT CHASE". That chase-guard is for OPEN trades; the
  UI rendered it on an already-closed trade.
- **No-chase guard / maker-first miss?** No — entry filled; not a maker miss.
- **Did MSTR move favorably / was it a missed profitable trade?** No — MFE 0.36R, never
  approached TP1; it expired flat. Not missed, not profitable.

## Fix
`backend/app/actionability.py` — for terminal statuses, return a neutral
`freshness:{label:"closed (<status>)", ok:true}` instead of leaking the chase-guard. The
UI now shows MSTR as **"Expired flat (+0R, MFE 0.36R) · entry filled"** with the full
lifecycle, not "very late — DO NOT CHASE".

## Missed-opportunity journal (genuine misses)
`backend/app/lifecycle.py → missed_opportunities()` + `GET /api/missed-opportunities`:
lists signals whose **entry never triggered** (late/missed) with `late_minutes`,
`would_have_entered_price`, `max_favorable_move_r`, `would_have_been_profitable`, reason.
Entry-then-expired trades like MSTR are correctly **excluded** (they filled; they live in
Closed).

## Latency posture
No real latency was found for MSTR, so no scheduler-interval change was required. The
journal + freshness-only-on-open changes make any *true* future latency/miss visible and
correctly labelled.

## Verdict
**MSTR_LATE_ENTRY_CAUSE_IDENTIFIED_AND_FIXED** (cause = chase-guard label leaked onto a
closed trade; entry was on time; not a missed profitable trade).
