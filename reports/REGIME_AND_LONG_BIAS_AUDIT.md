# Regime & Long-Bias Audit (PART 7)

**Date:** 2026-06-17 · read-only.

## What exists
`src/agents/scoring_agent.py` already has a **regime gate for intraday**: a long vs "bearish trend" is capped at score 60 (C-tier, no Telegram) unless it's an RS-leader (70 cap → B). Shorts vs "bullish trend" likewise capped. Regime label is produced by `src/agents/market_regime_agent.py` (BTC trend + breadth + vol → bullish/bearish/range/high-vol/transition) and stored on `proposed_signals.market_regime`.

## What the data shows
**Crypto intraday triggered, regime × direction × outcome:**
| regime · dir · result | n |
|---|--:|
| bullish trend · long · LOSS | 15 |
| (empty) · long · LOSS | 14 |
| bullish trend · long · WIN | 13 |
| (empty) · long · WIN | 4 |
| range/chop · long · LOSS | 2 |
| short · LOSS (any) | 2 |
| bearish trend · short · WIN | 1 |

- The book is **long-only** (≈2 shorts total). It cannot profit from a down move — it only stops out.
- Every recent loser was a **long labeled "bullish trend" or "" (blank)** — so the bearish-trend gate **never engaged**.

**Regime label vs reality (BTC daily):** 06-11 +3.44%, 06-13 +1.38%, 06-14 +2.00%, **06-15 +0.89%**, **06-16 −0.99%**, **06-17 −0.96% (intraday −2.36%)**.

Two regimes, two stories:
1. **06-15 (BTC +0.89%, 27 crypto stops):** regime label "bullish" was **correct**. The losses there are **alt whipsaw + tight stops + over-trading** within a genuinely up BTC — *not* a regime-bias failure. (See losing-streak / stop-wick reports.)
2. **06-16 / 06-17 (BTC −1% to −2.4% intraday):** BTC rolled over, but the structural label stayed **"bullish trend"**, so longs kept firing into a falling tape and stopped. Here the **regime label lagged the intraday turn**, and the gate (which only blocks *bearish*-labeled longs) couldn't help because the label never flipped.

## Diagnosis
Not "the system aggressively longs risk-off." It's:
- **(a) regime granularity/latency** — the label is structural/daily and slow to register an intraday risk-off turn; and
- **(b) long-only exposure** — no ability to stand aside or go short when BTC turns intraday-red; and
- **(c) no intraday risk-off throttle** between "bullish" and "bearish" (a red-intraday-BTC state isn't handled).

## Recommendations (cautious — not implemented)
- **Intraday long throttle on intraday risk-off:** when BTC 1h/4h is below a short MA / down >X% on the day, **reduce size or shadow new intraday longs** even if the daily label is still "bullish." (Bridges the bullish↔bearish gap.)
- **"Longs only if BTC/sector confirms" for intraday** — require intraday trend confirmation, not just structural label.
- **Lower size for longs during a falling intraday tape.**
- **No-new-longs after N stops/day** (ties to the circuit-breaker gap, PART 8).
- Optionally allow **shorts** in clear intraday downtrends (currently near-absent) — research-only.
- Verify regime **freshness** (how stale `market_regime` can be at signal time).

## Verdict
`RECENT_LOSSES_REQUIRE_REGIME_THROTTLE` — **partial**: applies to the 06-16/06-17 cluster (regime-lag longs), not to 06-15 (correct-bullish whipsaw). Add an **intraday risk-off throttle + no-new-longs-after-N-stops**; keep the existing bearish-trend gate. Medium-high priority; validate forward, do not change scoring now.
