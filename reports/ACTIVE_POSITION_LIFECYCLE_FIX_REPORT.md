# ACTIVE POSITION LIFECYCLE — FIX/VERIFY REPORT (PART 6)

**Date:** 2026-06-24. PAPER / read-model + UI.

## Audit
- **Does the system close at first TP?** No. The desk marks `signal_outcomes.final_outcome`
  only at a *terminal* event (TP3 / stop / expired). A TP1-only trade has
  `final_outcome=NULL` → it is non-terminal → it stays in the **open/pending** bucket.
- **Touch vs lifecycle?** The lifecycle read-model (`backend/app/lifecycle.py`) derives a
  partial-exit status, not the touch outcome.
- **Active tab separation?** Open/pending vs closed is driven by the terminal status; the
  lifecycle adds the partial sub-state.

## Behaviour (implemented)
Lifecycle status mapping (`_assemble`/event loop):
`waiting_entry → entry_filled_active → tp1_filled_active ("TP1 filled · waiting TP2/TP3")
→ tp2_filled_active ("TP2 filled · runner to TP3") → closed_win / stopped / expired /
closed_partial_stop / closed_partial_expired`. `position_active` event carries
`remaining_qty`, realized R/$, current stop.

Frontend `TradeCard` (Active tab) shows the partial badge from `tp1_hit`/`tp2_hit`/
`tp3_hit`:
`Entry filled · waiting TP1` / `TP1 filled · waiting TP2/TP3` / `TP2 filled · runner to
TP3`, and the **Next TP** cell points to the next unfilled target — so a TP1-partial
trade **stays in Active** with realized + remaining shown.

## Verification
No trade was mid-flight at exactly TP1 at audit time, so a live demo row wasn't available;
the status mapping + badge are code-verified and covered by lifecycle tests. When a trade
takes TP1 it remains in the open bucket (non-terminal) and renders the partial badge.

## Verdict
**ACTIVE_POSITIONS_REMAIN_AFTER_PARTIAL_TP**
