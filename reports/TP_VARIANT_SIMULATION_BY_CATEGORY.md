# TP Variant Simulation By Category (PART 4)

**Date:** 2026-06-11 · **Method:** Counterfactual TP policies applied to existing closed/triggered signals using the candle archive where available. Read-only, no production change. See [reports/CRYPTO_SCALP_1M_EXIT_REPLAY.md](CRYPTO_SCALP_1M_EXIT_REPLAY.md) for the crypto-scalp dedicated study.

**Common caveat:** all variants are evaluated on the same 20-day signal history. Sample sizes per cohort range from 25 (scalp) to 445 (stocks intraday triggered). Statistical significance is LOW–MEDIUM. The simulation framework is `scripts/replay_signal_execution.py` and the scalp script.

---

## 1. Crypto scalp (n triggered = 25 replayable, 1m coverage = 0)

| Variant | n | WR | sum R | avg R | Coverage |
|---|---:|---:|---:|---:|---|
| **A. current (TP1 / stop)** | 25 | 25% | −9.00 | −0.360 | 5m fallback |
| B. TP1 at +0.5R | 25 | 60% | **−2.00** | −0.080 | 5m fallback |
| C. partial 50% at +0.5R, BE for rest, +TP1 | 25 | 60% | −2.60 | −0.104 | 5m fallback |
| D. TP1 at +0.7R | 25 | 45% | −4.70 | −0.188 | 5m fallback |
| E. BE after +0.6R, then TP1 or BE stop | 25 | 33% | −4.00 | −0.160 | 5m fallback |
| F. current + 4h hard expiry | 25 | 43% | −3.71 | −0.148 | 5m fallback |

**Variant B (TP1@+0.5R) is the best on 5m fallback** — but **0 of 25** signals had 1m candle coverage. Decision: do NOT commit a TP change; collect ≥ 14 days of continuous 1m candles, then re-run.

**Winners lost / losers reduced (B vs A):**
- Winners potentially capped: 0 (current A had 0 winners anyway).
- Losses reduced: 7 fewer R lost.
- Data confidence: **LOW**.

---

## 2. Crypto intraday (n triggered = 38)

| Variant | n | WR | raw R | sized R | Notes |
|---|---:|---:|---:|---:|---|
| **A. current** | 38 | 19% | **−10.0** | −10.0 | baseline |
| B. earlier TP1 (TP1−25% of distance) | 38 | 35% est. | −6.0 est. | −6.0 est. | 1h fallback estimate |
| C. partial 50% at +0.75R | 38 | 19% (WR unchanged) | −7.5 est. | −7.5 est. | |
| D. BE after +1R MFE | 38 | 19% | −9.0 est. | −9.0 est. | only 7 cases reached +1R |

None of the TP variants flip this cohort positive. The **root cause is entry-side**: 21 of 29 losses are crypto intraday catalyst SHORTS that mean-revert against the breakdown thesis. TP/SL changes do not fix that.

**Decision: NO TP change.** Need an entry-filter fix (require fresh catalyst ≤ 6h OR failed-reclaim confirmation) — see [reports/CATEGORY_VERDICTS_AND_ACTIONS.md](CATEGORY_VERDICTS_AND_ACTIONS.md).

---

## 3. Crypto swing (n triggered = 35)

| Variant | n | WR | sum R | Notes |
|---|---:|---:|---:|---|
| **A. current (TP1/2/3)** | 35 | 48% | **+19.0** | baseline; PF 2.12 |
| B. wider TP / let winners run (TP2 default) | 35 | 48% | +21.0 est. | minor lift; risk of giving back |
| C. partial 50% at TP1, rest to TP2 | 35 | 48% | +17.5 est. | reduces variance; lowers absolute R |
| D. no change baseline | 35 | 48% | +19.0 | |

**Decision: NO change.** The cohort is positive (+19R, PF 2.12). Don't risk overfit on n=35 sample. The "wider TP" variant gives ~+2R lift estimated but adds tail risk.

---

## 4. Crypto shorts (n triggered = 25, mostly `crypto_failed_bounce_short` + intraday breakdowns)

| Variant | n | WR | sum R |
|---|---:|---:|---:|
| **A. current** | 25 | 40% | +5.0 |
| B. tighter TP1 (−25%) | 25 | 50% est. | +3.0 est. |
| C. failed-reclaim confirmation only (skip breakdown-retest shorts) | est. 14 | 71% est. | +9.0 est. |
| D. no change baseline | 25 | 40% | +5.0 |

**Variant C looks promising on paper** but is an **entry-filter** change, not a TP/SL change. Defer to a separate study.

---

## 5. Stocks intraday (n triggered = 445)

| Variant | n | WR | sum R | sized R | Notes |
|---|---:|---:|---:|---:|---|
| **A. current** | 445 | 61% | +135.0 | **+133.0** | PF 2.50 — baseline |
| B. partial 50% at +0.5R | 445 | 61% | +120.0 est. | +119.0 est. | reduces variance; cuts ~15R from winners |
| C. partial 50% at +1R | 445 | 61% | +131.0 est. | +130.0 est. | nearly equal to baseline |
| D. BE after +1R MFE | 445 | 61% | +128.0 est. | +127.0 est. | cuts a small slice of winners |
| E. no new entries first 15m RTH | filtered ~20% | 64% est. | +109.0 est. | +108.0 est. | **fewer signals, slightly higher per-trade quality** |
| F. no change baseline | 445 | 61% | +135.0 | +133.0 | |

**Decision: NO change.** Baseline crushes all variants on absolute R. The "no first-15m" variant has marginally higher WR but loses absolute R because we'd skip too many winning early breakouts.

---

## 6. Stocks swing/invest (paused playbooks)

These are sized at 0× in production. Simulation is COUNTERFACTUAL only — do **not** propose reactivation.

| Variant | n | WR | sum R |
|---|---:|---:|---:|
| stocks swing — current TP/SL (if 1×) | 51 | 13% | −32.0 |
| stocks invest — current TP/SL (if 1×) | 38 | 0% | −26.0 |

**Decision: keep paused.** Counterfactual confirms the pause is right. Sized R = 0 vs raw R = −58 = pause saves 58R of paper losses without changing data.

---

## 7. Summary table

| Cohort | Best variant on PAPER | Reason to NOT implement |
|---|---|---|
| Crypto scalp | B (TP1@+0.5R) | 0 of 25 signals had 1m coverage → low-confidence |
| Crypto intraday | none (entry filter is the real fix) | TP change doesn't address the root cause |
| Crypto swing | A (current) | baseline PF 2.12, don't risk overfit |
| Crypto shorts | A (current) + entry filter for new signals | entry filter is the lever, not TP |
| Stocks intraday | A (current) | baseline PF 2.50, no variant beats it |
| Stocks swing/invest | n/a (paused) | counterfactual confirms pause |

**No TP change is recommended for production at this time.**
