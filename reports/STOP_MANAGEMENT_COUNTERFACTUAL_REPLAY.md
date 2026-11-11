# Stop-Management Counterfactual Replay (PART 6)

**Date:** 2026-06-23. Reconstructed from recorded path. **No production change.** **Reliability: RELATIVE RANKING ONLY** (not reliable absolute R) — same caveats as the prior shadow-exit replay: same-candle stop-first conservative + 5m/15m granularity, AND the production baseline is optimistic best-TP-touched, so BE/partial measured against it are biased toward "looks worse."

## Why these are conceptual vs the current paper trade
The production model has **no remaining position** — it books one R (best TP touched). It is NOT "full-close at TP1." So BE/partial/trailing are **alternative exit models**, compared on the path, not deltas to a partial book. (PART 6 STOP VARIANT 1 caveat applies: marked conceptual.)

## Variants — ACTIONABLE (582), net R (relative)
| | net R | vs current best-TP (+5.0) | vs hold→TP3 (−136.8) |
|---|---|---|---|
| BASELINE current (best-TP) | +5.0 | — | +142 |
| hold→TP3 (no stop mgmt) | −136.8 | −142 | — |
| STOP-1 BE after TP1 | −109.8 | −115 | **+27** |
| STOP-2 lock +0.2R after TP1 | ≈ −104 | −109 | +33 |
| STOP-3 BE after +0.6R MFE | ≈ −118 | −123 | +19 |
| STOP-4 partial@TP1 + runner+BE | −107.9 | −113 | **+29** |
| STOP-5 TP2 profit-lock (stop→+1R after TP2) | ≈ −112 | −117 | +25 |

## Reading this honestly
- **Against the current (optimistic best-TP) accounting, every stop-management variant is WORSE** (−109 to −123R) — because best-TP already banks the upside and BE only caps it. This is the same "pessimistic vs real book" caveat the prior shadow replay flagged.
- **Against a realistic hold-to-TP3 baseline, BE/partial HELP** (+19 to +33R): they convert give-backs (TP1→stop, 3% of trades) and reduce holding losses. So IF real execution is "hold for the far target," partial@TP1+BE (−108) and BE-after-TP1 (−110) are the best of the realistic family, beating naive hold→TP3 (−137).
- The two framings disagree because the **true operator behavior is unknown** (manual exits). The replay cannot tell you the absolute R; it tells you: *if you tend to hold for TP3, add a partial/BE; if you already exit near the best TP, BE costs you.*

## Give-back & false-safety
- Give-back set (TP1→later stop) = **42 trades / 3.0%** — small. BE-after-TP1 rescues these to ~0R under the hold model.
- False-safety (BE'd out then would have hit TP3): bounded by the 45 TP3 trades; a handful of crypto-swing TP3 runners would be cut to BE under aggressive BE-after-TP1. Net of give-backs saved, partial@TP1 (keep a runner) dominates pure BE because it preserves TP3 upside on the runner.

## Verdict
`STOP_MANAGEMENT_REPLAY_COMPLETE` — results are **relative-only**; BE/partial help only under a hold-to-far-target assumption, hurt under the current optimistic accounting; give-back is small (3%).
