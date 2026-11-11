# App Realistic-PnL Display Plan (PART 8) — PROPOSAL (default-off)

**Date:** 2026-06-23. The app currently shows the touch-based `final_r` as "realized R" with **no caveat**. Per PART 4 that overstates the actionable book by ≈+100…+143R. The app must not silently present it as real PnL.

**Status: PROPOSAL, not implemented this turn.** The Control Plane has been operationally fragile (recently stabilized to LOCAL mode); a UI/endpoint change risks re-breaking a working app. The derived numbers already exist (CSV + `compute_models`), so this is safe to implement on approval. No DB historical outcome is ever overwritten.

## What to add (display / read-model only)
1. **Backend (isolated, read-only):** new module `backend/app/realistic_pnl.py` + one endpoint `GET /api/books/realistic_summary` that reads `signal_outcomes` (same dedup as `books.py`) and returns, per book/window: `recorded_touch_r`, `realistic_r` (default model = first-TP-close or +0.5R-lock, query-selectable), `giveback_count`, `overstatement_r`. Reuses `scripts/realistic_pnl_sim.compute_models`. Does **not** touch existing `/books` endpoints → cannot break current screens.
2. **Dashboard header:** show **two numbers** — `Recorded (touch) R` and `Realistic R` — with a tooltip: *"Recorded = highest TP touched (optimistic). Realistic = simulated single-position exit."* Default the headline to **Recorded R but explicitly labelled "touch-based"** (no silent PnL); add a **model selector** (touch / first-TP-close / TP1-BE / +0.5R-lock / partial).
3. **Closed-trade detail:** per trade show `TP1 touched then stop? yes/no`, `would BE have saved it? (Δ vs hold)`, `would partial have changed it?`, and the close reason under each model.
4. **Do not** overwrite DB historical outcomes; `realistic_r` is derived at read time.

## Effort / risk
- Backend: ~1 small module + 1 endpoint (low risk, additive).
- Frontend: header label + selector + detail rows (moderate; the risky part given app fragility).
- Rollback: feature-flag `SHOW_REALISTIC_R` default **off**; remove endpoint → no effect on existing screens.

## Recommendation
Implement the **backend derived endpoint first** (safe, additive, gives the honest numbers via API), then the **header label** ("touch-based") as the minimal honesty fix, and the full selector/detail only after the app proves stable. All gated behind a default-off flag, on operator approval.

## Verdict
`APP_REALISTIC_PNL_DISPLAY_PROPOSED` (ready to implement on approval; not built this turn to protect the just-stabilized app).
