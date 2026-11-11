# Crypto Scalp — Viability Audit (PART 2)

**Date:** 2026-06-09 · **Scope:** Read-only diagnostic. No code/TP/SL/scoring/routing touched.
**Sample:** 55 deduped scalp A/B signals over 14d (2026-05-26 → 2026-06-09). All B-tier (no A-tier scalp fired in 14d).

## 1. Headline
| n | triggered | closed | W | L | expired | WR% | PF | netR |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 55 | 35 | 8 | 1 | 7 | 27 | 12.5 | 0.14 | −6 |

20 of 55 (36%) never triggered. Of 35 that triggered, only 8 reached a terminal verdict; the other 27 ran the 2h validity window flat (after touching positive MFE).

## 2. The defining pattern: positive MFE, expired flat

| Bucket | n | share |
|---|---:|---:|
| triggered & expired flat | 27 | 49% of all scalp |
| triggered & stopped (loss) | 7 | 13% |
| triggered & hit TP1 (win) | 1 | 2% |
| not triggered | 20 | 36% |

**Of the 27 "expired with MFE":**
- avg MFE = **+0.54R**
- 27/27 (**100%**) had POSITIVE MFE during the 2h window
- 12/27 (44%) had MFE ≥ +0.5R
- 6/27 (22%) had MFE ≥ +0.7R
- avg MAE = −0.39R (rarely came close to stop)

Signals routinely run +0.5–1.2R favorable, then revert toward entry, then time out. Examples (all expired flat):
- SUI/USDT short — MFE +1.07R
- NEAR/USDT short — MFE +1.19R
- OPN/USDT long — MFE +1.15R
- ALGO/USDT long — MFE +0.95R
- OPG/USDT short — MFE +0.90R
- ETH/USDT short — MFE +0.71R

The one win (C/USDT long) hit TP1 at +1.00R after 35 minutes; its MFE was +1.74R, so even that win left chips on the table.

## 3. Stop / TP geometry vs scalp horizon

Computed from 55 entries:
| Metric | Value |
|---|---|
| avg stop distance (% of entry) | **3.20%** |
| avg TP1 distance (% of entry) | **5.89%** |
| avg TP2 distance (% of entry) | **10.03%** |
| avg implicit RR (TP1/risk) | **1.86** |
| avg implicit RR (TP2/risk) | **3.16** |
| avg `expected_rr_tp1` field | 1.21 |
| avg `expected_rr_tp2` field | 2.22 |
| validity window | **2.0 h (all 55 signals)** |

The implicit TP1 RR (1.86) is reasonable for a structural scalp, but the **TP is 5.89% away while the typical favorable run captured is +0.54R ≈ 1.7% of entry**. The scalp horizon is the bottleneck, not the entry edge.

## 4. Timing
| Metric | n | median | avg | max |
|---|---:|---:|---:|---:|
| time-to-entry (from creation) | 35 | 8 min | 26 min | 102 min |
| time-to-stop (from entry) | 7 | 70 min | 64 min | 100 min |
| time-to-tp1 (from entry) | 1 | 35 min | 35 min | 35 min |

Entries trigger fast (median 8 min) — entry logic is not the failure point. Stops fire late in the 2h window, suggesting reversals are slow grinds rather than sudden invalidations.

## 5. Conditional cuts

### By news_supported
| news | n | closed | WR% | PF | netR |
|---|---:|---:|---:|---:|---:|
| news=1 | 13 | 2 | 0.0 | 0.00 | −2 |
| news=0 | 42 | 6 | 16.7 | 0.20 | −4 |

**News does NOT rescue scalp.** Catalyst-backed scalps are slightly worse than no-news scalps (small sample, but no edge visible). This is opposite to intraday/swing where news raises PF.

### By regime
| regime | n | closed | netR |
|---|---:|---:|---:|
| (empty) | 39 | 3 | −1 |
| bearish trend | 8 | 1 | −1 |
| range/chop | 5 | 2 | −2 |
| high-vol danger | 2 | 2 | −2 |
| transition | 1 | 0 | 0 |

No regime produces positive scalp. `range/chop` and `high-volatility danger` are uniformly losing; `bearish trend` neutral on tiny sample.

### By direction
| dir | n | closed | WR% | netR |
|---|---:|---:|---:|---:|
| long | 27 | 4 | 25.0 | −2 |
| short | 28 | 4 | 0.0 | −4 |

Long scalps marginally less bad (1W/3L vs 0W/4L); not a real edge.

### By BTC/ETH alignment, liquidity, volume ratio, squeeze flags, score bucket
- All 55 scalps in 14d are B-tier (single tier). No score-bucket discrimination possible.
- Liquidity buckets: 4 "liquid_major" (BTC/ETH/SOL/BNB/XRP), 51 "other_liquid" (binance non-major), 0 thin alts. Liquid_major closures = 0; cannot separate.
- BTC/ETH alignment, volume ratio, squeeze flags are not persisted on `proposed_signals` — would require re-deriving from raw report files. Out of scope.

### By entry triggered vs not
| | n | netR |
|---|---:|---:|
| triggered | 35 | −6 |
| not triggered | 20 | 0 |

20 of 55 (36%) never even triggered → entry zones may be slightly tight, or the move continues without the pullback. Not a losing failure mode (0R contribution) but it caps actionable volume.

## 6. Answers to the 9 questions

1. **Is scalp bad across all conditions?** Across the conditions we *can* slice (news, regime, direction, liquidity), yes — every slice is negative or zero. No condition currently lifts scalp into positive PF.
2. **Or only bad without catalyst?** No — catalyst-backed is *worse* than no-catalyst in the 14d sample (0/2 vs 1/5).
3. **Or only bad in chop/danger?** Chop and danger are both negative, but `bearish trend` is also negative (1 closure −1R). No regime produces positive scalp.
4. **Or only bad on thin coins?** Cannot test — there are no thin-alt scalps in the sample (none on MEXC-only). All scalps are binance-listed.
5. **Are many scalp trades expiring with positive MFE?** **Yes — 27/27 expired had positive MFE; avg +0.54R; 12 reached ≥+0.5R; 6 reached ≥+0.7R.** This is the defining pattern.
6. **Are entries too conservative?** Marginally — 20/55 (36%) don't trigger. Median time-to-entry is 8 min, so entry zones are reachable; but the 36% miss rate suggests the trigger zone is a slight conservatism tax.
7. **Are TPs too far for scalp?** **Yes — TP1 sits ~5.9% away (≈1.86R), while the realised favorable run inside the 2h window averages ≈1.7% (≈0.54R MFE).** TP1 is roughly **3.5× further than the average favorable run actually achieved**. The single win confirms this: it captured 1.00R with 1.74R MFE.
8. **Would trailing/partial help?** Mathematically, on the existing 35 triggered:
   - If a +0.5R partial-take had fired on every triggered scalp, the 12 expired-with-MFE-≥0.5R would have produced ≈+6R partial; combined with current −6R, the mode would be ≈break-even.
   - A trailing stop after MFE ≥ +0.7R would have locked ≈+0.35R on the 6 expired-with-MFE-≥0.7R (≈+2R), still leaving the mode net-negative but materially better.
   - These are *strategy/TP changes* and **are out of scope for this audit** — flagged for separate consideration.
9. **Should scalp remain fully active, become catalyst-only, or just continue collecting data?**
   - Catalyst-only is **not justified** — catalyst scalp is worse than no-catalyst in this window.
   - Pause-actionable is **not yet justified** — the closed sample is 8. That's below the 20-closure noise floor typically needed for a confident "broken" verdict on a single-tier slice.
   - The best read is: **the entry edge appears genuine (100% positive MFE on expired); the exit machinery (TP1 distance vs 2h horizon) does not capture it.** This is a strategy/horizon question, not a routing question.
   - **Recommendation (kept for PART 6):** continue collecting data; treat scalp output as low-confidence in any user-facing summary; do not pause yet.

## 7. Confidence
- 8 closures is a thin base for any of the conditional cuts.
- The MFE pattern (100% positive, 44% ≥+0.5R) is consistent enough across 27 expired signals to be treated as a real characteristic, not noise.
- No A-tier scalp signals in 14d → A-tier behavior is unknown.

## Verdict for PART 2
Crypto scalp is **conditionally weak, not structurally broken**. The dominant failure mode is "entry triggers fast, captures +0.5–1.2R favorable, reverts inside the 2h window, expires flat." The TP1 distance relative to the 2h validity window is the geometric mismatch. **Continue collecting data; do not pause; do not gate by catalyst yet — catalyst-only would not have improved the 14d sample.**
