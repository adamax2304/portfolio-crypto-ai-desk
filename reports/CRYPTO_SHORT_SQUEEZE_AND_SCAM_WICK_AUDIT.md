# Crypto Short Squeeze / Scam-Wick Audit (READ-ONLY)

**Date:** 2026-06-04 · **Window:** last 48h · **Mode:** read-only diagnosis.
No scoring/threshold/strategy/data changes; no auto-trade.

## 1. Executive summary
- **The failed shorts were mostly BAD-TIMED, not bad-stopped.** Stops were
  fine (every stop sat **2.4–4.5×** the 90th-pctile upper wick, 1.25–2.54 ATR
  away); widening them would not have saved 3 of the 4 losers.
- **Dominant failure mode = late short into a bounce on a thin coin.** 3 of 4
  losers (BCH, DEXE, GPS) were shorted while price was **bouncing** (1h
  +2.2% / +6.4% / +6.4%) after an extended down-move, on **sub-$15M** 24h
  volume. DEXE was shorted straight into a **2.1× volume squeeze candle**.
- **Only SAHARA was "right but stopped"** — it reached 0.84R toward target,
  got squeezed out, then **did hit TP1 afterward**. It is also a thin coin
  ($5.4M).
- **The liquid name (ETH, $1.2B) did not lose** — it expired flat.
- **Recommendation:** add a **late-short / squeeze guard** (bounce guard +
  thin-liquidity/high-wick cap + retest requirement for hard drops) as a
  **cap-to-C**, NOT a hard reject, and validate on more data. Do **not** add
  wick-aware stop-widening (stops weren't the problem). Sample is small
  (5 triggered, **0 winning shorts**) → implement conservatively + validate.

## 2. All recent shorts
See `SHORT_SQUEEZE_RISK_TABLE.md` for the full metric table. Summary:

| symbol | mode | tier | score | outcome | R | MFE | MAE | Telegram | signal row | comment |
|---|---|---|---|---|---|---|---|---|---|---|
| SAHARA | scalp | B | 67.8 | loss | −1 | 0.84 | −1.32 | yes | yes | near-miss → real squeeze; hit TP1 after stop |
| OPG | intraday | B | 65.5 | loss | −1 | 0.03 | −0.94 | yes | yes | late breakdown chase (1h −4%) |
| BCH | intraday | B | 65.2 | loss | −1 | 0.09 | −1.19 | yes | yes | shorted into +2.2% 1h bounce |
| GPS | scalp | B | 65.7 | expired | 0 | 0.18 | −0.36 | yes | yes | bounce (+6.4% 1h) after −20% crash |
| DEXE | scalp | B | 65.9 | loss | −1 | 0.07 | −1.05 | yes | yes | squeeze: +6.4% 1h, 2.1× vol, max wick 2.0 ATR |
| ETH | scalp | B | 65.6 | expired | 0 | 0.71 | −0.37 | yes | yes | liquid; near-miss, no loss |
| NEAR | scalp | B | 66.1 | waiting | — | — | — | (pending) | yes | not triggered |

All shorts have a backing `proposed_signal` and were Telegram-alerted (B-tier).
Mechanically the short pipeline is working.

## 3. Case studies
- **SAHARA** — `near_miss_then_squeeze`. 24h −7.5%, 1.8 ATR below EMA20. Short
  worked to +0.84R, then a real candle **closed** above the stop (squeeze, not
  a wick), then price fell and **hit TP1**. Right thesis, stopped first; thin
  ($5.4M). Wider stop *might* have caught the move, but the coin's thinness is
  the deeper risk.
- **OPG** — `late breakdown chase`. 1h **−4.0%**, 4h −6.7%; shorted a fresh
  breakdown already extended down; bounced; **wick-only stop**; never reached
  TP1 after. Late.
- **BCH** — `short into bounce`. 1h **+2.2%** and **above** EMA20 at entry;
  liquid but breakdown on contracting volume (0.64×); bounced, no TP1. Wrong
  side.
- **GPS** — `bounce after crash`. 24h **−20.4%** then +6.4% 1h; shorted the
  dead-cat bounce; expired flat (0R).
- **DEXE** — `active squeeze`. 24h −12.8%, then **+6.4% 1h, 2.1× volume,
  max upper wick 2.0× ATR**, price **above** EMA20 (+1.25 ATR); shorted into the
  squeeze; wick-only stop; no TP1 after. Textbook scam-wick/squeeze.
- **ETH** — liquid, near-miss, expired flat — the control case showing deep
  liquidity ≠ squeeze loss.

## 4. Price-path after entry (PART 2 classification)
| symbol | immediate wrong-side | near-miss→squeeze | wick-stop→correct dir | late/exhaustion | valid stop | low-liquidity |
|---|---|---|---|---|---|---|
| SAHARA | | ✅ | ✅ (hit TP1 after) | | | ✅ |
| OPG | ✅ | | (wick stop, no TP after) | ✅ | | ✅ |
| BCH | ✅ | | | ✅ (bounce) | ✅ (genuine) | |
| GPS | | | | ✅ | (expired) | ✅ |
| DEXE | ✅ | | (wick stop, no TP after) | ✅ | | ✅ |

## 5. Squeeze / wick / liquidity diagnostics
- **Liquidity:** 4/4 losers ≤ $15M 24h quote vol (SAHARA $5M, OPG $6M, DEXE $9M,
  GPS $15M). Only the liquid ETH avoided a loss.
- **Bounce at entry:** BCH/DEXE/GPS had **positive 1h returns** at entry; DEXE/
  BCH were above EMA20.
- **Wick volatility:** DEXE max upper wick **2.0× ATR**, OPG 1.67× — thin-coin
  squeeze wicks. SAHARA/GPS 1.1×.
- **Volume:** DEXE 2.1× spike (squeeze in progress) is the standout; others had
  contracting volume (0.64–0.86×) = weak breakdowns prone to mean reversion.
- **Stops:** none were inside normal wick noise (stop/p90wick 2.4–4.5).
- **Derivatives/funding/OI:** mostly unavailable for these thin alts (the same
  "derivatives data unavailable" flag seen in the source reports) → no crowding
  read; this itself is a thin-coin warning sign.

## 6. Winners vs losers (PART 4)
**There were 0 winning shorts in the window** → no clean statistical winner/
loser split is possible (documented limitation). The available contrast:
- **Lost (thin + bounce):** avg 24h vol ≈ $26M (skewed by BCH; median ≈ $7.7M),
  3/4 bouncing at entry, 2/4 above EMA20, avg max-wick/ATR ≈ 1.35.
- **Did not lose (ETH, liquid):** $1.2B vol, falling at entry (1h −0.9%),
  1.98 ATR below mean, max-wick/ATR 0.63.
→ **What separates good from bad shorts (hypotheses, small n):** (1) liquidity —
thin coins squeeze; (2) timing — don't short an active bounce; (3) wick
volatility — high upper-wick coins stop you on noise spikes. **Not** stop width.

## 7. Were stops too tight or shorts bad/late?
**Shorts were bad/late, stops were adequate.** Evidence: stop/p90wick 2.4–4.5×;
SAHARA stopped on a candle **close** (real squeeze); OPG/BCH/DEXE never returned
to TP1 after stopping, so a wider stop would have lost more, not less.

## 8. Did price later move in intended direction after stop?
Only **SAHARA** (hit TP1 after stop). OPG/BCH/DEXE did **not** — they bounced
and stayed up. So "stopped then went my way" applies to **1 of 5**, not the
group.

## 9. Candidate protections (PART 5 — design only)
- **A. Squeeze-risk cap** — cap short to C / no A/B alert if: coin already
  −X% over 24h (e.g. < −12%) **and** bouncing (1h return > +1.5%), or volume
  spike (>1.8×) against the short, or funding/OI shows crowded short.
- **B. Late-short / exhaustion filter** — if > ~2 ATR below EMA20, don't short
  the breakdown; require failed-bounce / lower-high / close-below-support-after-
  retest, else watchlist.
- **C. Wick-aware stop check** — only relevant if stop < ~p90 upper wick;
  **not triggered by any case here** → low priority.
- **D. Liquidity / scam-wick cap** — cap to C / no A/B if 24h quote vol < ~$15M
  **or** max upper-wick > ~1.5× ATR **or** volume_ratio very low + no derivatives.
- **E. Retest requirement for hard drops** — after a large drop, only short a
  failed retest, not the first breakdown / not a bounce.

## 10. Read-only simulation (PART 6)
Population: 5 triggered shorts with outcomes (SAHARA, OPG, BCH, DEXE = −1R;
GPS, ETH = 0R). **0 winners exist**, so no winner can be removed by any filter.

| Filter | Blocks/caps | Losers removed | Winners removed | Net R | Catches SAHARA/BCH/OPG/DEXE? |
|---|---|---|---|---|---|
| **A/E Bounce guard** (1h > +1.5%) | BCH, DEXE, GPS | BCH, DEXE (−2R→**+2R**) | 0 | **+2** | BCH+DEXE only |
| **B Exhaustion** (>1.8 ATR below EMA20 / 24h<−10% → retest) | GPS, DEXE, SAHARA, ETH, NEAR | DEXE, SAHARA (+2R) | 0 | caps SAHARA (the "right" one) |
| **C Wick-aware stop** | none | 0 | 0 | 0 | none (stops already wide) |
| **D Thin/high-wick cap** (<$15M or wick>1.5 ATR) | SAHARA, OPG, DEXE, GPS | SAHARA, OPG, DEXE (−3R→**+3R**) | 0 | all but BCH |
| **A+D combined** | all losers | all 4 (−4R→**+4R**) | 0 | **all 4** |

Caveat: every removal looks "free" only because there were **no winning shorts**
to harm. The true cost (blocking future good shorts) is **unmeasured** at n=5.

## 11. Recommendation
**Implement a combined late-short / squeeze guard — as a CAP-to-C (watchlist,
no A/B Telegram), not a hard reject — then validate before trusting it.**

Priority order (TODOs — not implemented in this read-only pass):
- **P1 `TODO-short-bounce-guard`** (filter A/E): do not issue an actionable A/B
  short when 1h momentum is strongly positive (price bouncing). Lowest
  collateral, removes BCH+DEXE, leaves SAHARA. **Best first step.**
- **P1 `TODO-short-thin-liquidity-cap`** (filter D): cap shorts on sub-~$15M /
  high-upper-wick / derivatives-less coins to C. Removes the most losses; pairs
  with the bounce guard.
- **P2 `TODO-short-retest-requirement`** (filter B/E): after a large drop,
  require a failed retest / lower-high instead of chasing the breakdown.
- **Do NOT implement** wick-aware stop-widening (C) — stops were adequate.
- **Do NOT change** stop/TP geometry, scoring weights, or A/B thresholds.
- **Validate**: re-audit after ≥20–30 more shorts (incl. some winners) to
  confirm the guards don't suppress good shorts before making them permanent.

## Final answer
```
SHORT_SQUEEZE_AUDIT_COMPLETE
```
Verdict: failed shorts were **late/thin/squeezed**, not mis-stopped. Recommend a
**bounce + thin-liquidity guard (cap-to-C)** with validation; **no wick-aware
stop change**; sample small → implement conservatively, do not change live logic
in this read-only task.
