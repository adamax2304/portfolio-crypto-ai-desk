# Crypto Scalp — Keep / Pause / Rework Decision (PART 5)

**Date:** 2026-06-15

## Verdict

```
SILENCE_SCALP_SETUP_ALERTS_KEEP_PAPER_ENTRY
```

## Answers

1. **Is crypto scalp currently useful?** Marginally, as research. Entry edge is real (avg MFE +0.56R) but it does not convert (49/61 triggered expire flat; net −8R all-time). Not useful as an actionable live channel.
2. **Net harmful or just noisy?** **Mostly noisy, mildly negative.** Sized at 0.5× it contributes ~−4R sized all-time — small. The real harm was Telegram noise (152 setup alerts → 7 wins).
3. **Are skips mostly protective?** **Roughly half-protective.** 55 of 108 analyzable skips would have hit stop first; ~40 reached favorable moves that the horizon couldn't capture. Net: skipping is approximately break-even-protective, not a costly mistake.
4. **Are missed moves common enough to justify a new entry policy?** **No.** Missed moves exist (~40% reach +0.5-1R excursion) but capture is unreliable (TP/horizon mismatch), and the sample is 1m-thin. No policy beats current cleanly.
5. **Should scalp remain paper-only?** **Yes.** Keep at 0.5× sized weight, paper-only, no live promotion.
6. **Should scalp setup Telegram alerts be silenced/digested?** **Yes — implemented.** Setup alerts → Obsidian/journal/digest; paper-entry + close alerts stay on Telegram.
7. **Is TP1@+0.5R still worth studying?** **Yes** — strongly motivated (avg MFE +0.56R, 27 trades touched +0.5R before expiring flat). But research-only until a real 1m archive exists.
8. **Is there enough 1m data to decide?** **No.** 1m archive is rolling ~3.7h. Cannot validate an exit change → NEED_MORE_1M_DATA for any TP/SL decision.
9. **Safest next action?** Ship the notification-only silence (done), keep paper-only at 0.5×, and start an append-only 1m archive so TP1@+0.5R can be tested properly in ≥ 14 days.

## What was NOT done (by design)

No change to scoring, thresholds, TP/SL, entry logic, routing, sizing weights. Scalp is not promoted, filters not loosened, no historical outcome rewritten. The only change is silencing the crypto-scalp **setup** Telegram message.
