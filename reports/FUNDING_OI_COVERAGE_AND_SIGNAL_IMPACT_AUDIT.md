# Funding & Open-Interest Coverage + Signal Impact (PART 5)

**Date:** 2026-06-15 · Read-only.

## 1. Coverage on A/B crypto signals

| Window | n | funding present | OI present | derivatives_supported |
|---|---:|---:|---:|---:|
| 48h | 105 | 105 (100%) | 105 (100%) | 105 (100%) |
| 7d | 172 | 172 (100%) | 172 (100%) | 172 (100%) |
| 14d | 241 | 241 (100%) | 241 (100%) | 241 (100%) |
| all | 261 | 261 (100%) | 261 (100%) | 261 (100%) |

**Every crypto A/B signal carries funding + OI context.** Coverage is not the problem.

## 2. Point-in-time vs latest-cache

**Latest-cache only.** Stored as a string blob on each signal at creation:
```
funding=-1.132e-05, crowding=normal
price up + OI up: fresh positioning confirms trend, monitor crowding
```
There is **no `funding_snapshots` / `oi_snapshots` archive table** (verified: DB has no such table). So:
- Each signal has a snapshot of funding/OI *at creation time* ✅
- There is **no historical time series** to replay funding/OI at arbitrary past timestamps ❌ (blocks Level-B/C backtest and funding-cost modelling — consistent with the earlier archive-readiness audit).

## 3. Does missing derivatives block/downgrade?

Coverage is 100%, so the "missing" path is rarely exercised for crypto. When derivatives are unavailable, the scorer falls back to a 0.3 baseline for the derivatives component (no hard block). Extreme funding IS detected (crowding/squeeze flags) and feeds an alignment penalty.

## 4. Performance impact

Because coverage is 100%, a with-vs-without derivatives split is **not possible** for crypto A/B (no "without" group exists). What we CAN measure is the **catalyst/news** split (the more informative axis):

| news_supported | n | W | L | raw R |
|---|---:|---:|---:|---:|
| 1 | 34 | 12 | 11 | **+15.0** |
| 0 | 126 | 25 | 59 | **−3.0** |

And by direction (derivatives matter most for shorts via squeeze guard): the `crypto_failed_bounce_short` cohort (PF 2.10 historically) relies on funding/OI squeeze interpretation and is net-positive — evidence the derivatives signal is being used productively on shorts.

## 5. Long/short ratio

Collected by `binance_derivatives_collector` (globalLongShortAccountRatio) and interpreted in `derivatives_agent` (crowding warnings). Reaches scoring as an alignment penalty. Not separately stored as a time series.

## Conclusion

- Funding ✅ checked (100% coverage). OI ✅ checked (100%). Long/short ✅ collected.
- **Latest-cache, not point-in-time** — adequate for live scoring, insufficient for historical replay.
- No archive table → recommend (safe, additive) a `funding_snapshots`/`oi_snapshots` table written per cycle. See [CATALYST_PIPELINE_SAFE_FIX_PLAN.md](CATALYST_PIPELINE_SAFE_FIX_PLAN.md).
