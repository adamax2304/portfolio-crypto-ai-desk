# Crypto Scalp — Missed-Move Shadow Study (PART 2)

**Date:** 2026-06-15 · Read-only, research only. **No policy implemented.**

## Method

For every scalp signal that was skipped / never_filled / stale_before_entry / expired-flat (n=113 all-time), walk available candles forward from `created_at` and measure max favorable excursion in the intended direction vs whether the stop was hit first. Candle source: 1m where the window is covered, else 5m/15m fallback.

**Coverage:** 108 of 113 analyzable (5 had no forward candles). 1m archive is ~3.7h rolling, so longer-dated signals fall back to coarser TF — treat absolute figures as **LOW-CONFIDENCE**; the *distribution* is the signal.

## Missed-move distribution (108 analyzable skipped signals)

| Outcome after skip | n | % |
|---|---:|---:|
| reached **+0.3R** in intended direction | 48 | 44% |
| reached **+0.5R** | 45 | 42% |
| reached **+0.7R** | 43 | 40% |
| reached **+1.0R** | 40 | 37% |
| **hit stop first** (went adverse, < +0.3R favorable) | **55** | **51%** |
| fakeout (+0.5R then reversed to stop) | 3 | 3% |

## Shadow policy comparison (qualitative — excursion ≠ realized capture)

| Policy | Hypothetical effect | Verdict |
|---|---|---|
| **A. Current (skip)** | baseline — avoids the 55 stop-first losers, forgoes the ~40 favorable | the ~50/50 split means skipping is roughly break-even-protective |
| **B. Enter on +0.3R move** | catches 48 favorable starts, but a chunk of the 55 stop-firsts also tick +0.3R briefly then reverse → net near-zero | NOT compelling |
| **C. Enter on +0.5R move** | catches 45, fewer false starts, but you enter later (worse RR) | marginal |
| **D. Failed-reclaim confirmation** | would filter the 55 stop-firsts best, but needs reclaim logic + more data | most promising, research-only |
| **E. BTC/ETH-aligned only** | not separable on current data (no per-signal BTC-trend snapshot stored) | needs data |
| **F. Volume-expansion confirm** | not separable (no per-signal rel-volume-at-decision stored) | needs data |

## Key reads

- **Skips are ~50% protective**: 55 of 108 skipped signals would have hit stop first. Entering them blindly creates real losses.
- **Missed winners exist (~40%) but capture is unreliable**: reaching +1R as max-excursion ≠ exiting at +1R — the scalp horizon expires flat (see PART 1: avg MFE +0.56R but 49/61 triggered expire flat). So even captured entries tend to give the move back.
- **No policy clears the bar** to justify changing production entry on a ~50/50, 1m-thin sample.

## Conclusion

The missed moves are real but not cleanly capturable with current TP/horizon, and roughly half the skips were protective. **No entry policy change is justified.** Failed-reclaim confirmation (policy D) is the only candidate worth a future study, and only after a proper 1m archive exists.
