# Concentration Cap — Counterfactual Replay (PART 6)

**Date:** 2026-06-16 · `scripts/counterfactual_stock_concentration.py` (read-only).
Replays entered+closed stocks-intraday A/B trades day-by-day through the overlay.
**Raw/unsized paper R (mostly ±1R).** Both benefits AND costs shown — no cherry-picking.

| Window | n | base raw R | base sized R | proxy-only (A) | full cap (A+B) | →half / →shadow | cluster R base→cap | worst day base→cap |
|--------|---|-----------:|-------------:|---------------:|---------------:|-----------------|--------------------|--------------------|
| 24h | 20 | +1.0 | +0.0 | −1.0 | −1.0 | 4 / 7 | +0 → +0 | −1.0 → −1.5 |
| 7d  | 52 | +1.0 | +0.0 | +0.0 | **+1.5** | 11 / 12 | −7.0 → −4.5 | −3.0 → −2.5 |
| 14d | 110 | +4.0 | +5.5 | **+10.5** | +7.0 | 21 / 36 | −13.0 → −7.0 | −4.5 → −2.5 |
| all | 465 | +136 | +133 | **+21.5** | **+15.0** | 31 / 361 | −13.0 → −7.0 | −21.5 → −2.5 |

## Honest reading (benefits AND costs)
**Benefit (recent regime):** 7d/14d the cap is net-positive vs baseline sized R
(+1.5 / +1.5), softens the worst day (−4.5→−2.5), and cuts all-loss-cluster bleed
(−13→−7). It would have reduced today's −4R semis/tech wipeout. For the **manual** operator
it collapses 18 correlated alerts to the best 1–2 — which is all a human would take anyway.

**Cost / caveat (full history):** over **all** data the cap is **strongly negative**
(sized +133 → +15; proxy-only +21.5). Two reasons, stated plainly:
1. **Duplicate-signal inflation** — the baseline counts the same Nasdaq move captured by
   QQQ+XLK+AAPL+MSFT as ~4–5× R; the cap removes the duplicates, so it "loses" phantom
   double-counted R it could never have realized as one portfolio.
2. **Regime** — historically the correlated tech-long book was *net-profitable on trend
   days*; an equal-weight-everything backtest that takes all 137 same-day tech longs makes
   the cap look like it forfeits real upside. No live operator sizes that way.

**14d shows proxy-only (Rule A, +10.5) beats full A+B (+7.0)** — Rule B (sector cap) gives
back some upside even recently. Rule A (collapsing genuine ETF/duplicate redundancy) is the
more robust component.

## Conclusion
The cap is **not** an unambiguous auto-P&L win on the full record, and we do **not** claim
one. It is a **risk-shape / manual-de-noise** tool: it reliably cuts correlated wipeout
days and redundant alert spam, at the cost of capping correlated upside on trend days.
That profile → **enable shadow-first** (labels + alert de-noising) and validate forward
rather than hard-committing the sized-R cap on the strength of a duplicate-confounded
backtest. **PART 6 status: DONE.**
