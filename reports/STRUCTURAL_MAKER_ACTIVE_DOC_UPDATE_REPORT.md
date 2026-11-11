# DOC UPDATE — STRUCTURAL + MAKER-FIRST ACTIVE (PART 11)

**Date:** 2026-06-24. PAPER ONLY.

## Files updated
- **`PROJECT_STATE.md`** — new "Last Updated" + banner with all 9 verdicts, A/B
  numbers, module list, forward-only structural-TP caveat, live-locked + final_r-intact.
- **`docs/DECISION_LOG.md`** — new dated row (active, paper-only) with reason +
  numbers + report link.
- **`docs/CURRENT_TESTING_AND_WAITING_STATE.md`** — §1 status bullet (paper uses
  structural TP + maker-first under max-2x; production TP unchanged; B book name) and 4
  new rows in §2 active features (max-2x sizing, structural TP, fee-aware, maker-first).
- **`docs/WEEKLY_FORWARD_METRICS.md`** — new watch rows: B vs A paper equity vs the
  replay baselines, fees-as-%-of-gross, maker fill rate, missed maker entries, fee-drag
  skips, structural TP usage.
- **`docs/SHADOW_MODE_REGISTRY.md`** — 4 new LIVE-ADVISORY (paper) rows for the new
  policies + promote-when conditions.
- **`trading-desk-control/README.md`** — new paragraph: structural TP + maker-first +
  max-2x, `/api/portfolio/compare`, A/B numbers, B book name, forward-only caveat.

## Docs say (explicitly)
- Paper now uses **structural TP**; **production TP generation is UNCHANGED** (mechanical
  ATR ladder).
- **Maker-first active in paper**; stops always taker.
- **Max leverage 2x active** (leverage ≠ risk).
- **Fee-aware active** (skip extreme/tight fee drag).
- **Live locked**; `final_r` never rewritten.
- **What to watch:** forward B equity vs the +8.19% Bybit replay; fees as % of gross
  (~74%); maker fill rate vs the conservative model; structural-TP forward re-walk.

## Verdict
**DOCS_UPDATED_FOR_STRUCTURAL_MAKER_ACTIVE**
