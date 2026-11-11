# Category Verdicts & Actions (PART 8)

**Date:** 2026-06-11 · Per-category verdicts based on PARTS 1-7 audits. Read-only — no production change.

---

## Crypto scalp (`crypto_scalp_momentum_continuation`)

| Question | Verdict |
|---|---|
| Keep active low-confidence? | ✅ YES — current 0.5× sizing already mitigates the −9R raw drag to −4.5R sized |
| Change TP? | ❌ NO — exit study showed B (TP1@+0.5R) promising but 0 of 25 had 1m candles (LOW-CONFIDENCE) |
| Paper-only? | ✅ YES — already paper-only; current state is correct |
| Need more 1m data? | ✅ YES — backfill ≥ 14d continuous 1m candles before any exit change |

**Action:** **KEEP UNCHANGED.** Add to monitoring: 1m archive growth. Re-run scalp exit study when 1m sample ≥ 30 signals.

---

## Crypto intraday (`crypto_intraday_catalyst_or_momentum`)

| Question | Verdict |
|---|---|
| Keep? | ⚠️ CONDITIONAL — current cohort is −14R sized (worst non-paused) |
| Require catalyst? | ⏳ STUDY NEEDED — propose "fresh catalyst ≤ 6h OR failed-reclaim confirmation" as entry filter (not TP/SL) |
| Change TP/stop? | ❌ NO — TP variants don't flip cohort positive |
| Adjust short confirmation? | ⏳ STUDY NEEDED — `failed-reclaim` filter looks promising in §4 of TP_VARIANT_SIMULATION_BY_CATEGORY.md |

**Action:** **KEEP TP/SL UNCHANGED.** Open separate study: shorts need either a fresh-catalyst gate OR a failed-reclaim confirmation. Until that's tested OOS, the existing sized R weight (1.0×) absorbs the loss. Could consider lowering to 0.5× as defensive measure.

---

## Crypto swing (`crypto_swing_narrative_rs_momentum`)

| Question | Verdict |
|---|---|
| Keep primary? | ✅ YES — PF 2.12, +19R sized, 48% WR |
| Change TP/stop? | ❌ NO — no variant beats baseline by more than noise |
| Increase size or keep 1×? | ✅ KEEP 1× — sample (n=35) too small to upsize confidently |

**Action:** **NO CHANGE.** Continue monitoring weekly.

---

## Crypto shorts (subset of `crypto_failed_bounce_short` + intraday breakdown shorts)

| Question | Verdict |
|---|---|
| Keep? | ✅ YES — `crypto_failed_bounce_short` cohort PF 2.10, +11R sized |
| Require fresh catalyst / failed-reclaim? | ⏳ DEFER — current playbook gate already incorporates this; the broken cohort is `crypto_intraday_catalyst_or_momentum` shorts, not `failed_bounce_short` |
| Stop/TP changes? | ❌ NO — wick-aware stop adds +2R but cohort is already positive |

**Action:** **KEEP UNCHANGED.** Failed-bounce-short playbook is healthy; don't add complexity.

---

## Stocks intraday (`stocks_intraday_rth_momentum`)

| Question | Verdict |
|---|---|
| Keep? | ✅ YES — champion cohort: 61% WR, PF 2.50, +133R sized |
| A-tier long half-size enough? | ✅ YES — fine-override at 0.5× is correctly absorbing A-tier overpromotion |
| B-tier stronger? | ✅ YES — confirmed: B-tier carries most of the +135R raw |
| Need RTH-open caution? | ❌ NO — "no first-15m" simulation reduces R by ~26 vs baseline; current handling is fine |

**Action:** **NO CHANGE.** Best-performing cohort; don't risk it.

---

## Stocks swing (`stocks_swing_watchlist_rs_rotation`)

| Question | Verdict |
|---|---|
| Keep watchlist-only? | ✅ YES — counterfactual −32R confirms the pause is right |

**Action:** **KEEP PAUSED (0× sized weight).** Re-evaluate after 60 days of fresh data.

---

## Stocks invest (`stocks_invest_watchlist_30d_thesis`)

| Question | Verdict |
|---|---|
| Keep watchlist-only? | ✅ YES — counterfactual 0% WR / −26R confirms pause is right |

**Action:** **KEEP PAUSED (0× sized weight).** Re-evaluate after 60 days.

---

## Summary table

| Category | TP change? | Stop change? | Size change? | Other action |
|---|---|---|---|---|
| crypto scalp | NO (need 1m) | NO | NO | Backfill 1m archive |
| crypto intraday catalyst | NO | NO | Consider 0.5× | Study entry filter |
| crypto swing | NO | NO | NO | Monitor |
| crypto failed-bounce short | NO | NO | NO | Monitor |
| stocks intraday | NO | NO | NO | Monitor (champion) |
| stocks swing | n/a | n/a | KEEP 0× | Re-eval in 60d |
| stocks invest | n/a | n/a | KEEP 0× | Re-eval in 60d |

**Net:** zero TP/SL/routing changes. One possible defensive size cut (crypto intraday catalyst 1.0× → 0.5×) is the only YAML change that could be defended on data, but even that is borderline and would benefit from waiting another 14 days.
