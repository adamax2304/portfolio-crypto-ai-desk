# Intraday Risk-Off / Long-Bias Throttle — Diagnostic (PART 6)

**Date:** 2026-06-17 · **Mode:** shadow/label only. **No throttle, no half-size, no block enabled.**
**CSV:** `INTRADAY_RISK_OFF_THROTTLE_DIAGNOSTIC.csv` (per crypto long, with BTC day % + would_throttle flag).
**Verdict:** **SHADOW_LABEL_ONLY** — the throttle would NOT have saved meaningful R; keep as an informational regime label, do not act on it yet.

## Diagnostic rule
`btc_intraday_risk_off` = BTC daily change ≤ **−0.75%** (Binance 1d). For each triggered crypto **long**, flag `would_throttle_long` when its entry day is risk-off.

## Replay validation (the important check)
| Day | BTC day % | Risk-off? | Expectation | Result |
|---|---|---|---|---|
| 2026-06-15 | **+0.89%** | NO | should NOT trip (BTC up) | ✅ not tripped |
| 2026-06-16 | **−0.99%** | YES | should trip (BTC down) | ✅ tripped |
| 2026-06-17 | **−0.96%** | YES | should trip (BTC down) | ✅ tripped |

The flag correctly distinguishes the up day (06-15) from the two down days (06-16/17) — confirming the regime-lag thesis: longs kept firing into red BTC on 06-16/17.

## Counterfactual on throttled longs
| Metric | Value |
|---|---|
| Crypto longs on risk-off days | losers caught **26**, winners missed **16** |
| **Net realized R on those longs (as-traded)** | **−1.0R** |

## Honest read — why "label only", not "throttle"
- The longs that fired on risk-off days netted only **−1.0R combined**. Throttling/half-sizing them would have saved ~1R *at most*, while **also skipping 16 winners**. The 26 losers were nearly fully offset by the 16 winners.
- So on a pure-R basis the long-bias-into-red-BTC problem is **real as a pattern but small as a cost** in this window. A throttle here is not justified by the numbers — it would mostly trade variance for variance.
- The value of the flag is **visibility/context** (Opus + Telegram can see "longs firing into risk-off"), not automated sizing.

## Recommendation
- Ship `btc_intraday_risk_off` as a **shadow regime label** on crypto-long alerts + dashboard + Opus packet (PART 7). No sizing/blocking.
- Re-measure over ≥30d and across a genuinely trending-down stretch (e.g. the −14% 02-05 type day) before considering any half-size action. In a sharper downtrend the asymmetry may grow; 06-16/17 were only ~−1% days.
- **Do NOT** throttle, half-size, or block longs in this stage.
