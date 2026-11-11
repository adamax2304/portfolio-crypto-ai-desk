# Crypto Quality Overlay — cqo_v1 (2026-11-11T21:06:51.559198+00:00)

> PAPER / READ-MODEL. Soft sizing/routing breaker for crypto paper candidates. Live LOCKED; signal generation / tier / final_r untouched. Only ever downgrades (never upgrades).

## Decision mix (recent crypto signals)
- HALF_SIZE: 1319
- SHADOW_ONLY: 997
- FULL_SIZE: 422
- BLOCK: 183

## Crypto intraday cohort guard (forward-only)
- routing mode: **warn**; policy: `cohort_guard_v2`
- second routing key enabled: **False**
- activation verdict: **NOT_ELIGIBLE**
- narrow target resolved: **198 / 30**
- only append-once point-in-time post-v2 decisions count; current snapshots and backfill do not

| entry mode | catalyst | resolved | WR | PF | net R | avg R |
|---|---|---:|---:|---:|---:|---:|
| BREAKOUT_CONTINUATION | no_fresh | 199 | 39.7 | 1.9466 | +75.73 | 0.3805 |
| LEVEL_HOLD_1BAR | no_fresh | 37 | 40.5 | 2.0124 | +12.15 | 0.3283 |
| LEVEL_HOLD_V2 | no_fresh | 10 | 40.0 | 2.0726 | +5.36 | 0.5363 |
| LIMIT_THEN_TAKER_TIMEOUT | no_fresh | 37 | 37.8 | 1.8909 | +12.47 | 0.3371 |
| MOMENTUM_TAKER_NOW | no_fresh | 16 | 31.2 | 2.1487 | +6.89 | 0.4308 |
| NO_CHASE_SKIP | no_fresh | 4 | 100.0 | inf | +5.29 | 1.3214 |
| PULLBACK_LIMIT | no_fresh | 160 | 39.4 | 1.492 | +31.49 | 0.1968 |

## Counterfactual (baseline full-size vs overlay) — avoided loss vs missed profit
_net Δ USD conflates two different things: HALF_SIZE mechanically halving a winning cohort's dollar total looks the same as a genuinely bad call. avoided-loss $ / missed-profit $ split those apart so a guard that's net-negative because it protects against real losses isn't judged the same as one that's just cutting winners._
| window | net Δ USD | avoided-loss $ | missed-profit $ | PF base→overlay | orig-stop red. | missed tp3 runners | missed winners | trade Δ |
|---|---|---|---|---|---|---|---|---|
| 48h | +0 | +0 | +0 | None→None | 0/0 | 0/0 | 0 | 0 |
| 7d | +11 | +11 | +0 | 0.0→0.0 | 0/1 | 0/0 | 0 | 0 |
| 14d | +16 | +27 | +11 | 0.223→0.151 | 0/3 | 0/0 | 0 | 0 |
| all | +226 | +2326 | +2099 | 1.532→1.752 | 1/358 | 0/128 | 0 | -1 |

**⚠ SHADOW_ONLY blind spot:** 1573 of 2628 all-time evaluated trades have NO visible baseline (mostly SHADOW_ONLY routing, which writes no paper_portfolio_ledger row) and are excluded from every number above. avoided-loss $ is therefore a floor, not the true total prevented loss -- SHADOW_ONLY's real counterfactual impact is currently unmeasured, not zero.

_Evidence-class split (Model F): only forward_postfreeze is proof the underlying trades are profitable — backfill_pretrained is the same in-sample data that chose Model F's own thresholds and must never be read as "profitable"; unclassified predates the evidence_class column._
| window | forward_postfreeze n/resolved/netR | backfill_pretrained n/resolved/netR | unclassified n |
|---|---|---|---|
| 48h | 1/1/+0.00 | 0/0/- | 0 |
| 7d | 3/3/-1.00 | 0/0/- | 0 |
| 14d | 16/16/-1.52 | 0/0/- | 0 |
| all | 612/612/+92.55 | 443/443/+202.11 | 0 |

## Active session cooldowns: 0
- _none_

## Active symbol cooldowns: 0
- _none_