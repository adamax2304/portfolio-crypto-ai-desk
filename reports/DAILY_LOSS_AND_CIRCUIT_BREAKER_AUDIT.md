# Daily-Loss / Circuit-Breaker Audit (PART 8)

**Date:** 2026-06-17 · read-only.

## Current state
**No circuit breaker exists in the trading engine.** Code search found no daily loss cap, no max-stops-per-day, no no-new-trades-after-N, no per-mode/per-direction daily cap. Exposure is limited only by per-trade sizing weights (1.0×/0.5×/0×) and the regime/tier caps. The **Control Plane** (`trading-desk-control`) has a `daily_loss_limit` *setting*, but it governs the paper control plane, **not** the crypto-ai-desk engine — the engine ignores it.

## What the data shows (crypto stops per UTC day)
| day | crypto stops |
|---|--:|
| 06-11 | 3 |
| 06-12 | 7 |
| 06-13 | 2 |
| 06-14 | 7 |
| **06-15** | **27** |
| 06-16 | 10 |
| **06-17** | **16** |

On **06-15 the desk took 27 crypto stops in one day** and **kept opening new longs throughout** — there was nothing to halt the bleed. Same pattern building 06-17 (16). Stocks intraday had similar clustered loss days (06-11 −6R/20 losses, 06-15 −4R/15 losses).

This is the single clearest *structural* gap: the system has **no "stop digging" mechanism**. On a chop/whipsaw day it will keep firing the same losing pattern dozens of times.

## Proposed circuit breakers (cautious — not implemented; mostly belong in the engine/monitor, but can ALSO be enforced read-only as alerts first)
| rule | trigger | action | risk |
|---|---|---|---|
| **daily R stop** | cumulative realized ≤ −2R to −3R (per asset class) for the UTC/RTH day | **no new entries** that asset/day | low — only blocks *new* risk |
| **consecutive-stop halt** | N (e.g. 3) stopped longs same regime/day | pause new **longs** until next session | low |
| **size step-down** | after 1st stop of the day | new entries at 0.5× | very low |
| **fresh-catalyst gate after streak** | after a losing streak | require a *new* catalyst, not momentum-only | low |
| **per-mode daily cap** | mode hits daily R floor | pause that mode until next session | low |

Start as **monitor-side alerts / shadow flags** ("would-pause") to validate the thresholds against history before any hard block — fully consistent with the "observe first" tracking philosophy.

## Caveat
A breaker capping the day at −2R on 06-15 would have stopped ~25 of the 27 stops — but it would also forgo any late-day winners. Backtest the threshold on the 7d (and longer) history before enforcing; pick the level that cuts tail days without gutting normal variance.

## Verdict
**Highest-leverage structural gap.** Recommend implementing a **daily-loss / consecutive-stop circuit breaker** (alert-first, then soft block) — this is the one change most directly tied to the "series of −1R" days. Validate thresholds on history; do not hard-enforce blind.
