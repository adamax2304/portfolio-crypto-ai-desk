# Shadow-Mode Performance Audit (PART 5)

**Date:** 2026-06-17 · read-only · CSV: `SHADOW_MODE_COUNTERFACTUAL.csv`.

"If we had taken every shadow signal with the same TP/SL logic" — using the tracker's real reconciled outcomes (shadow signals are still registered + tracked, so their hypothetical results are known, not simulated).

## Would-be performance by shadow reason (triggered + closed)
| shadow reason | taken | W | L | winrate | sumR | reached TP1 | verdict |
|---|--:|--:|--:|--:|--:|--:|---|
| **c_tier** (C-tier / watchlist) | 163 | 20 | 37 | 35% | **−8R** | 23 | KEEP shadow |
| **crypto_scalp_shadow** | 45 | 2 | 9 | 18% | **−7R** | 10 | KEEP shadow |
| **late_shadow** (very-late entry) | 12 | 3 | 5 | 38% | **−2R** | 5 | KEEP shadow |
| sector_cap / proxy_duplicate | 0 | — | — | — | 0 | 0 | did not fire (see SECTOR_CAP) |

(Remaining 0R buckets are expirations.)

## Answers to PART-5 questions
- **Which shadow reasons are useful / save money?** All three active ones are **net-negative if taken** → every one is *correctly* protecting the book:
  - **crypto scalp** −7R, 18% WR, PF 0.22 — re-confirms the 12-mo decision. **Do NOT re-enable.** It did miss ~10 trades that touched TP1, but as a group it loses heavily.
  - **late_shadow** −2R, 38% WR — confirms late entries are a **chase trap**, not free money. Keep suppressing.
  - **C-tier** −8R, 35% WR — C/watchlist genuinely underperform; keep shadow.
- **Any shadow signals that should become actionable?** **No.** Every shadow group is net-negative as a basket. The 23 C-tier and 10 scalp signals that *reached* TP1 are survivorship — the basket still loses. At most, C-tier could feed a **"review-only / candidate"** lane (not auto-actionable) for manual eyeballing — **not** a sizing change.
- **Any actionable signals that should have been shadow?** **Yes —** the 06-16/06-17 **crypto intraday longs taken while BTC was rolling over** (regime label lagging) should have been throttled/shadowed. That's a regime-throttle gap (see REGIME report), not a shadow-mode flaw.
- **scalp shadow** — keep off; missed-move check shows the misses don't pay (PF 0.22).
- **sector-cap shadow** — **fired 0 times in 7d** (see SECTOR_CAP report); neither saved nor choked anything this window.
- **proxy duplicates** — collapse logic is sound in principle but also didn't trigger live this window.

## Verdict
`SHADOW_MODES_WORKING_KEEP`. No shadow mode is too strict on this data; none should be escalated to actionable. Optional, low-priority: surface C-tier as a **review-only candidate list** (manual, non-sized) rather than fully hidden.
