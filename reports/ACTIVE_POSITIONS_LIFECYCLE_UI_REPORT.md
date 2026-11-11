# ACTIVE POSITIONS LIFECYCLE UI — REPORT (PART 7)

**Scope:** trading-desk-control frontend + read-model. Date: 2026-06-24. PAPER.

## What was built
`frontend/src/components.tsx` — `TradeCard` (used by the Active "open"/"pending" tab) now
shows a **partial-lifecycle badge** derived from the trade's `tp1_hit`/`tp2_hit`/`tp3_hit`
(already normalized by `desk_adapter`):
- `Entry filled · waiting TP1`
- `TP1 filled · waiting TP2/TP3`
- `TP2 filled · runner to TP3`
- `TP3 filled · closing`

The "Next TP" cell now points to the next unfilled target (TP1→TP2→TP3) instead of
always TP1, so a position that took TP1 shows TP2 as the next target and **stays in the
Active tab** (it is not removed while remaining qty exists).

## Full lifecycle on tap
Opening any active trade shows the full `LifecyclePanel` (PART 6): realized vs unrealized,
remaining qty, current stop, next target, blended R, execution timeline, price-scaled
chart — so an active "TP1 filled" position reads like a real exchange position.

## Verified
Frontend build clean (92 modules). Backend lifecycle returns `tp1_filled_active` /
`tp2_filled_active` statuses with a `position_active` event for trades with remaining qty.

## Verdict
**ACTIVE_POSITIONS_SHOW_PARTIALS_AND_NEXT_TARGETS**
