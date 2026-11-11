# DOC UPDATE — TRADE UI + MARKET FIX (PART 14)

**Date:** 2026-06-24. PAPER ONLY.

## Files updated
- **PROJECT_STATE.md** — new "Last Updated" + banner (chart-first, partial markers, VIX,
  overflow; all verdicts; live-locked; final_r intact).
- **docs/DECISION_LOG.md** — new dated row (ENA root cause + VIX fix; paper/UI only).
- **docs/CURRENT_TESTING_AND_WAITING_STATE.md** — §1 bullet: chart-first detail + true
  partial-exit markers + price ladder + active-after-TP1 + Market VIX.
- **docs/WEEKLY_FORWARD_METRICS.md** — market-dashboard freshness / VIX row already present
  (from the prior pass); covers VIX presence going forward.
- **trading-desk-control/README.md** — chart-first + partial markers + VIX paragraph.

## Docs now state
- Trade detail is **chart-first** with **partial exits visible** on the chart.
- **Active lifecycle after TP1** (partial badges, next target).
- **VIX / market dashboard fixed** (deterministic fetch + backfill; "VIX unavailable"
  explicit otherwise).
- **Max leverage policy = max-5x safe** (current value).
- **Live locked**; **`final_r` untouched**.

## Verdict
**DOCS_UPDATED_FOR_TRADE_UI_MARKET_FIX**
