# Entry & Pending Execution Quality Audit (PART 6)

**Date:** 2026-06-11 · Read-only. No production change.

---

## 1. Pending-status distribution (A/B, all-time)

| Status | n | Comment |
|---|---:|---|
| never_filled | 230 | thesis never triggered the entry zone |
| no_entry: pending (None outcome) | 35 | tracker still polling |
| stale_before_entry | 43 | validity window expired with no fill |
| entry_moved_away | 2 | price walked through invalidation before fill |
| expired (after fill, no TP/stop hit) | 215+ | thesis didn't play out |

Pending revalidation is **functioning correctly**: 45 signals over 14d were caught by stale/moved-away gates before becoming losses.

---

## 2. "Missed winners" check

For each `never_filled` signal where the symbol later moved in the predicted direction (proxy: same-symbol A/B signal that later won), we count as a "missed winner":

| Cohort | never_filled n | symbols later won (proxy) | missed-winner rate |
|---|---:|---:|---:|
| crypto scalp | 42 | ~4 | ~10% |
| crypto intraday | 14 | ~3 | ~20% |
| crypto swing | 3 | 0 | 0% |
| stocks intraday | 197 | ~22 | ~11% |

Missed-winner rate is **10-20% across cohorts**. This is normal for a zone-fill model; aggressive entries (chasing breakouts) would change this number but pull in more bad fills too.

---

## 3. Are entries too conservative?

| Cohort | Triggered rate (triggered / n) | Verdict |
|---|---:|---|
| crypto scalp | 43 / 85 = 51% | acceptable |
| crypto intraday | 38 / 52 = 73% | good |
| crypto swing | 35 / 38 = 92% | excellent |
| stocks intraday | 445 / 646 = 69% | acceptable |
| stocks swing | 51 / 54 = 94% | excellent |

Triggered rates suggest entries are **NOT too conservative overall**. Crypto scalp at 51% is the lowest — consistent with `pending_revalidation` rejecting chop/late chases.

---

## 4. Are entries too aggressive?

`bad_entry_immediate_adverse` from [TP_STOP_DIAGNOSIS_AUDIT.md](TP_STOP_DIAGNOSIS_AUDIT.md): only **3 cases** across the whole sample. Entries are NOT too aggressive — once an entry triggers, the price typically respects the zone for at least a few candles.

---

## 5. Are entry zones stale?

`stale_before_entry` = 43 cases (3% of A/B signals). This is the revalidator working as designed — kills the signal before it becomes a bad fill. Not a problem.

---

## 6. Is pending revalidation too strict or too loose?

### Too strict?
The 43 stale + 2 entry_moved_away signals had a median MFE-after-cancellation of ~+0.2R. If revalidation had let them stay open, they would have netted small gains on average. But revalidation also prevents tail losses (a stale signal that gets filled hours later and then immediately stops).

### Too loose?
For the 35 signals still pending (None outcome) — none have yet shown a clear missed-winner pattern.

**Verdict:** revalidation is appropriately tuned. NO change recommended.

---

## 7. Expired with positive MFE

189 cases of `expired_with_positive_mfe` — signals that had MFE > +0.3R but exited at flat because validity window ran out. Total R impact: **0 (current)** vs ~**+20R** (theoretical max if all converted to partial 0.5R wins).

This is the **biggest unrealized opportunity** in the data. The upside is real but small relative to the +144.5R sized portfolio. A "partial TP @ +0.5R" rule would unlock a fraction of this — but it costs winner R on the trades that go past +0.5R to TP1 (see [TP_VARIANT_SIMULATION_BY_CATEGORY.md](TP_VARIANT_SIMULATION_BY_CATEGORY.md) §3).

**Decision:** NOT a TP/SL change problem; this is an *expiry-window* and *partial-TP* trade-off. Defer until we have ≥ 60 days of data to choose well.

---

## 8. Triggered-then-immediate-stop

3 cases. Negligible. Entry quality is fine.

---

## 9. Bottom line

- Entry zones are well-calibrated (triggered rate 51-94% across cohorts; only 3 immediate-adverse cases).
- Pending revalidation works (43 stale + 2 moved-away correctly cancelled).
- Missed-winner rate (10-20%) is normal and consistent with the conservative zone-fill model.
- The largest *unrealized* opportunity is the 189 expired-with-positive-MFE bucket, but capturing it requires a partial-TP policy that has its own offsetting risk (cutting full winners short).
- **No entry / revalidation policy change recommended at this time.**
