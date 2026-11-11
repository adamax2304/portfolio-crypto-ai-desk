# Last 3–7d Final Trading Decision Report (PART 9)

**Date:** 2026-06-17 · read-only audit. **No production change made.** No live, no auto-live, no scalp re-enable, no TP/SL/scoring/threshold change, no sector-cap change.

## One-paragraph picture
Over 7d the book is **roughly flat**, dragged by **stocks/intraday (−12R, 31% WR)** and **crypto/scalp (−7R — shadow-only, correctly not actionable)**; crypto intraday/swing are **breakeven (PF≈1.0)**. The recent crypto "−1R series" is **mostly exit-management**, not bad signals: **78% of crypto losers were stopped by a shallow (<1.5R) dip and 19% had already reached +1R** before reversing — there is **no profit-protection** (partial-TP off, no move-to-BE). On top of that, two structural gaps amplified it: **no circuit breaker** (27 crypto stops on 06-15 with nothing to halt new entries) and a **regime label that lagged the 06-16/06-17 BTC roll-over** (longs into a falling tape). Shadow modes are all **net-negative if taken → correctly kept shadow**. The **sector cap fired 0× and is not choking stocks**.

## Decisions by category

### 1. Must fix now (obvious gap / high leverage, alert-first)
- **Circuit breaker** (daily-R / consecutive-stop) — engine has none; 27-stop day proves the gap. Implement **alert-first**, then soft block. *(PART 8)*
- **Verify sector-cap wiring** — it set `concentration_status` 0× live; likely inert on the monitor path. Confirm it isn't a silent no-op. *(PART 6 — verification, not a behavior change.)*

### 2. Should change after more data (validate counterfactual first)
- **Crypto profit-protection**: move-to-BE after +1R and/or partial at TP1 (cuts loser column ~14–21R gross, but re-price the 64 winners first). *(PART 4)*
- **Intraday risk-off throttle**: reduce/shadow new intraday longs when BTC intraday is red even if daily label is "bullish." *(PART 7)*
- **Intraday max-trade-age + RTH-aware expiry + relabel-to-carryover (reduced risk) + next-session revalidation.** *(PART 3)*
- **No-new-longs after N stops/day.** *(PART 7/8)*

### 3. Keep as is
- **Shadow modes** (crypto scalp −7R, late_shadow −2R, C-tier −8R) — all net-negative if taken; keep suppressed. *(PART 5)*
- **Regime gate for bearish-trend intraday longs** — sound; just add the intraday-risk-off layer. *(PART 7)*
- **Crypto intraday/swing core strategy** — PF≈1.0, edge intact; fix exits/throttle, don't touch scoring/TP/SL.

### 4. Research only
- Wider/candle-close stop for crypto; re-entry-on-reclaim; enabling shorts in clear intraday downtrends; rank-based/soft sector cap (only if/when it ever binds). *(PART 4/6/7)*

### 5. Do not change
- **Live / auto-live** (stay locked); **crypto scalp actionable** (stays shadow); **stocks scalp production** (stays research); **TP/SL/scoring/thresholds** (no edit pre-validation); **sector cap value** (non-binding — leave until verified).

## Verdicts (multiple, by area)
- **Crypto:** `RECENT_LOSSES_NORMAL_KEEP_RULES` **+** `RECENT_LOSSES_REQUIRE_REGIME_THROTTLE` (partial, 06-16/17) **+** stop/exit is the real leak → validate profit-protection (not a "stop-wick rework" yet).
- **Intraday lifecycle:** `RECENT_LOSSES_REQUIRE_INTRADAY_EXPIRY_FIX` (risk-hygiene, mostly stocks).
- **Structural:** add a **circuit breaker** (highest leverage).
- **Sector cap:** **NOT** `SECTOR_CAP_TOO_STRICT` — it's non-binding; `SECTOR_CAP_NON_BINDING_VERIFY_WIRING`.
- **Shadow:** `SHADOW_MODES_WORKING_KEEP`.
- **Overall live-readiness:** `SYSTEM_NOT_READY_FOR_LIVE` for autonomous; **ready for cautious manual micro-live on crypto intraday/swing A/B only** *after* the circuit breaker + intraday-risk-off throttle land, with tiny size and the operator applying BE-after-TP1 manually.

See `SAFE_FIX_PLAN_AFTER_RECENT_TRADE_AUDIT.md` for the staged, test-gated plan.
