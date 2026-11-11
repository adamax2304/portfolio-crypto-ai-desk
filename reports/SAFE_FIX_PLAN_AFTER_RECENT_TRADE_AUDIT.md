# Safe Fix Plan after Recent Trade Audit (PART 10)

**Date:** 2026-06-17 · **No code changed yet.** Each item: problem → evidence → proposed fix → risk → test → counterfactual → rollback. Order = lowest risk / highest leverage first. Nothing here unlocks live, re-enables scalp, or edits scoring/TP/SL.

---
### FIX 1 — Circuit breaker (alert-first)  ·  Priority: HIGH
- **Problem:** engine has no daily-loss / consecutive-stop halt.
- **Evidence:** 27 crypto stops on 06-15, 16 on 06-17, with new longs firing throughout (PART 8).
- **Fix:** in the monitor tick, compute rolling realized R per asset/day; emit a **"would-pause"** alert + `circuit_breaker` flag in `signal_alerts` when ≤ −2R/−3R or ≥3 consecutive stops. **No hard block yet.**
- **Risk:** very low (observe-only). **Rollback:** delete the flag write.
- **Test:** unit test the counter on a fixture day; replay 06-15/06-17 → expect the flag to fire mid-day. Add to `track-signals`/monitor tests.
- **Counterfactual needed:** sweep thresholds (−2R/−3R, N=2/3/4) over ≥30d history before any *hard* block (Phase 2).

### FIX 2 — Verify sector-cap wiring  ·  Priority: HIGH (verification only)
- **Problem:** `concentration_status` set 0× live; cap may be inert on the per-signal monitor path.
- **Evidence:** 18/92 cluster-day groups would bind under cap-2, but 0 live (PART 6).
- **Fix:** read `paper_entry.py` cap-invocation path; confirm whether it receives batch context. If it's a silent no-op, document; only then decide soft/rank-based. **No behavior change in this step.**
- **Risk:** none (read). **Rollback:** n/a.

### FIX 3 — Crypto profit-protection (validate, then maybe enable)  ·  Priority: MED
- **Problem:** trades reach +1R then give back to −1R; no move-to-BE / partial.
- **Evidence:** 19% of crypto losers reached TP1, 69% reached +0.5R; counterfactual −72→−58/−51R on losers (PART 4).
- **Fix (Phase 1 = measure):** extend the counterfactual to **re-price all 64 winners** under (a) move-to-BE after +1R, (b) 0.4/0.4/0.2 partial (`partial_exit_model` already in config, disabled). Report net R/PF.
- **Risk of measuring:** none. **Risk of enabling:** clips some runners → must see net-positive incl. winners first.
- **Test:** new counterfactual script + fixture; compare net R vs current.
- **Rollback:** config flag (`partial_exit_model.enabled`) stays false until proven.

### FIX 4 — Intraday risk-off throttle  ·  Priority: MED
- **Problem:** regime label lags intraday turns; longs fire into red BTC (06-16/17).
- **Evidence:** all 06-17 losers = "bullish trend" longs while BTC −2.36% intraday (PART 7).
- **Fix (Phase 1 = shadow):** compute an **intraday risk-off flag** (BTC 1h<MA / day<−X%); **shadow/half-size** new intraday longs when set. Ship as a label first; measure how many recent losers it would have caught vs winners it would have skipped.
- **Risk:** low as shadow-only. **Test:** replay 06-15 (should NOT trip — BTC up) vs 06-16/17 (should trip). **Rollback:** remove flag.

### FIX 5 — Intraday lifecycle hygiene  ·  Priority: MED
- **Problem:** filled intraday trades have no max-age / EOD close / next-session revalidation; 91 carried overnight, 155 expired@0R.
- **Evidence:** PART 3.
- **Fix:** (a) ensure `--revalidate-pending` actually runs on the monitor; (b) add **max-trade-age** for filled intraday (e.g. 12–16h) → review/flatten; (c) **RTH-aware expiry** for stocks intraday; (d) explicit **relabel intraday→carryover/swing with reduced risk** instead of silent overnight holds.
- **Risk:** low–med (carry is net +17R, so don't blanket-flatten — relabel+revalidate). **Test:** fixture trades crossing day/RTH boundaries; assert expiry/relabel. **Rollback:** config-gate each rule.

### FIX 6 — No-new-longs-after-N-stops  ·  Priority: MED (folds into FIX 1)
- Same mechanism as the circuit breaker, scoped to longs/regime; alert-first.

---
## Do-not-touch (reaffirmed)
Live, auto-live, exchange execution, crypto scalp actionable, stocks scalp production, C-tier promotion, sector-cap value, and all scoring/TP/SL/thresholds — **unchanged until the above counterfactuals/tests pass and you explicitly approve.**

## Sequencing
1. FIX 1 + FIX 2 (alert/verify — zero behavior risk) →
2. FIX 3 + FIX 4 measurement (winners-inclusive counterfactual + shadow flags) →
3. Review numbers with you → only then consider enabling any soft action (still paper) →
4. Re-audit a fresh 7d before discussing manual micro-live.
