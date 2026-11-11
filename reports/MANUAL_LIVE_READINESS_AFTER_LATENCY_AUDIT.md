# Manual Live Readiness — After Latency Audit (PART 10)

**Date:** 2026-06-16

## Verdict

```
SWING_ONLY_MANUAL_TEST
```

Swing is the only category where the current ~135-min entry-detection latency does not
break the trade. Intraday and scalp are **not** manually mirrorable until the Phase-2
cadence fix lands. Scalp is forbidden regardless.

## Answers

1. **Are paper-entry alerts fresh enough for manual entry?** **No, for fast modes.**
   Median entry-age is **~135 min** and **0%** of alerts were fresh/acceptable/late (≤15m)
   in any window (PART 2). After PART 5, these now self-label "very late — NOT actionable"
   and route `late_shadow` rather than pretending to be fresh.

2. **Which modes are safe enough to manually mirror?** **Swing only** — its entry zone is
   valid for *days*, so a 2h-late "entered" alert still lets the operator enter near the
   planned zone (with a price check). Even then: confirm price is within tolerance before
   entering.

3. **Which modes are too delayed?** **Crypto/stocks intraday** (135-min lag ≫ intraday
   horizon) and **scalp** (2h validity, and forbidden + net-negative).

4. **Should intraday be blocked from manual micro-live until latency improves?** **Yes.**
   Under the strict rule "no manual entry if entry_age > 5 min for intraday," *every*
   current intraday alert is blocked. Keep it blocked until Phase-2 brings entry-age < 5m.

5. **Is swing still the only viable manual category?** **Yes**, currently.

6. **Should Telegram include a "manual actionable / not actionable" line?** **Yes — done
   in PART 5.** Every paper-entry now carries `Entry freshness: fresh/acceptable/late/very
   late …`, and very-late entries get `[LATE ENTRY DETECTED — DO NOT CHASE]` + are not
   pushed.

## Strict manual-entry rules (operator contract)

- ❌ **No manual entry if entry_age > 5 min for intraday.** (Currently blocks all intraday.)
- ❌ **No manual entry if current price is worse than planned entry by > 0.25R.**
- ❌ **No manual entry if distance to stop is too compressed** (price already > halfway to
  stop from entry).
- ❌ **No manual entry if catalyst missing for a crypto intraday long.**
- ❌ **No scalp manual entry, ever.**
- ✅ **Swing B-tier:** allowed as a *tiny-size manual test*, only after confirming live
  price is within the entry zone and ≤ 0.25R from the planned entry.

## Path to broader manual-live

Implement PART 4 **Option B** (entry detection on the 5-min monitor) → entry-age drops to
~5 min → intraday becomes conditionally mirrorable under the rules above. Then re-run this
audit. Until then: **swing-only, tiny size, price-checked.**

**PART 10 status: DONE — verdict `SWING_ONLY_MANUAL_TEST`.**
