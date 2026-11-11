# Latency / Expired / Stock-Scalp Audit — Final Decision (PART 13)

**Date:** 2026-06-16

## Final answer

```
LATENCY_EXPIRED_STOCK_SCALP_AUDIT_COMPLETE
```

Audit complete; safe fixes shipped; one cadence change specified and deferred for approval.

## Component verdicts

| Area | Verdict | Basis |
|------|---------|-------|
| Double-alert fix (PART 1) | **VERIFIED FIXED** | exhaustive gate test; 0 post-fix same-tick pairs |
| Entry latency (PART 2) | **VERY HIGH (~135 min median)** | 0% fresh; detection only at 2h `track-signals` |
| Telegram delivery (PART 3) | **FAST / RELIABLE** | sub-second, 0.7% timeout-drop, no formatting errors |
| Latency reduction (PART 4) | Label now; **Option B deferred** | second-writer DB-lock risk needs WAL+lock |
| Freshness label (PART 5/11) | **IMPLEMENTED** | fresh/late/very-late + DO-NOT-CHASE + late shadow |
| Expired signals (PART 6/7) | **EXPIRED_RATE_HIGH_BUT_PROTECTIVE** | no-fill + flat-drift; 0% masked losses |
| Manual readiness (PART 10) | **SWING_ONLY_MANUAL_TEST** | fast modes too delayed until cadence fix |
| Stocks scalp (PART 8/9) | **STOCKS_SCALP_BACKTEST_REQUIRED** | feasibility LOW; no 1m/5m data; crypto-scalp precedent |

## What this means in practice

1. **The simultaneous open+close bug is gone** and provably cannot recur.
2. **Telegram is not the latency problem — the 2h detection cadence is.** Until a faster
   pending-only tracker lands, paper-entry alerts arrive ~2h late and are now honestly
   labelled "very late — NOT actionable" and not pushed (late-shadow), instead of pinging
   the operator with un-actionable entries.
3. **Expiries are healthy, not broken** — mostly stocks-intraday no-fills (no risk) and
   flat-drift (never hit stop). One targeted follow-up: a stocks-intraday entry-validity
   *study* (research only).
4. **Manual live = swing only, tiny size, price-checked.** Intraday/scalp blocked.
5. **No stocks scalp** without a 6-month 1m/5m backtest clearing the bar crypto scalp
   failed — and that data isn't freely available yet.

## Recommended next step → ✅ NOW IMPLEMENTED (2026-06-16)

PART 4 **Option B** has since been implemented and tested — entry detection on the existing
5-min monitor tick (WAL + busy_timeout + full-pass marker + exclusive lock, A/B non-paused
pending only). Expected typical entry-age drops from ~135 min to ~5–10 min. See
[LATENCY_OPTION_B_PENDING_TRACKER_IMPLEMENTATION.md](LATENCY_OPTION_B_PENDING_TRACKER_IMPLEMENTATION.md).
**Next:** after a few live monitor cycles, re-run the PART 2 latency audit to confirm the
measured drop, then re-evaluate intraday manual readiness (PART 10).

## Constraints honored

No auto-trade, no TP/SL/scoring/threshold change, no scalp reactivation, no setup-Telegram
re-enable, no C-tier promotion, no stocks swing/invest unpause, no history rewrite, no data
deletion, no new dependency, late alerts not made to look fresh.

---

**FINAL ANSWER: `LATENCY_EXPIRED_STOCK_SCALP_AUDIT_COMPLETE`**
(component verdicts: manual = `SWING_ONLY_MANUAL_TEST`; stocks scalp =
`STOCKS_SCALP_BACKTEST_REQUIRED`; expired = `EXPIRED_RATE_HIGH_BUT_PROTECTIVE`.)
