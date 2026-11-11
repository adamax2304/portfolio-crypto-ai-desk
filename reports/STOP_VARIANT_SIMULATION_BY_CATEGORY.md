# Stop Variant Simulation By Category (PART 5)

**Date:** 2026-06-11 · Read-only. No production change.

For each cohort, we simulate widening / tightening the stop by 10-20%, ATR-based stops, wick-aware stops, BE-after-MFE-threshold. We answer: are stops chronically too tight, too wide, or appropriate?

---

## 1. Crypto scalp (n triggered = 25; 5m fallback)

| Variant | n | WR | sum R | Notes |
|---|---:|---:|---:|---|
| **A. current** | 25 | 25% | −9.0 | baseline |
| B. wider stop +20% | 25 | 32% est. | −8.0 est. | saves 1R; same overall picture |
| C. tighter stop −20% | 25 | 8% est. | −11.0 est. | clearly worse |
| D. ATR-based stop | 25 | n/a | n/a | not feasible without 1m for proper ATR window |
| E. BE after +0.6R MFE | 25 | 33% | −4.0 | reduces drag but kills small winners |
| F. invalidation-close vs wick-touch | 25 | 25% | −9.0 | data shows wick stops triggering — minor effect |

**Diagnosis:** stops are NOT chronically wrong. The cohort loses because thesis fails, not because stops are tight. Most losses are clean stop-outs after price moves immediately against entry.

---

## 2. Crypto intraday (n triggered = 38)

| Variant | n | WR | sum R |
|---|---:|---:|---:|
| **A. current** | 38 | 19% | −10.0 |
| B. wider stop +20% | 38 | 24% est. | −8.0 est. |
| C. tighter stop −20% | 38 | 13% est. | −12.0 est. |
| D. ATR-based | 38 | 22% est. | −9.0 est. |
| E. BE after +1R MFE | 38 | 19% | −9.0 est. |
| F. wick-aware (require close past invalidation) | 38 | 24% est. | −7.5 est. |

The "wick-aware" variant adds 2.5R of theoretical lift by ignoring wick-stops. But the data shows only ~3 wick-stop cases in the cohort — small impact, high implementation risk.

**Diagnosis:** stops are not the lever. The losses are mostly *clean* stops where price went against the breakdown-retest thesis from entry. This is an entry-filter problem.

---

## 3. Crypto swing (n triggered = 35)

| Variant | n | WR | sum R |
|---|---:|---:|---:|
| **A. current** | 35 | 48% | +19.0 |
| B. wider stop +15% | 35 | 51% est. | +18.0 est. | wider stop lowers max-R-per-win |
| C. tighter stop −15% | 35 | 45% est. | +18.0 est. | tighter stop = more stop-outs but smaller |
| D. ATR-based | 35 | 50% est. | +20.0 est. | marginal lift |
| E. BE after +1.5R MFE | 35 | 48% | +18.5 est. | slight lift on tail winners |

All variants are within 1-2R of baseline. **No change justified.**

---

## 4. Crypto shorts (n triggered = 25)

| Variant | n | WR | sum R |
|---|---:|---:|---:|
| **A. current** | 25 | 40% | +5.0 |
| B. wider stop +20% | 25 | 45% est. | +6.0 est. |
| C. tighter stop −20% | 25 | 30% est. | +2.0 est. |
| D. wick-aware close-past invalidation | 25 | 50% est. | +7.0 est. |

The wick-aware variant could lift +2R. But the change-policy risk is significant: requiring "close past invalidation" delays stop-out and risks larger losses in true breakouts.

**Decision:** no stop change. The cohort is already net positive.

---

## 5. Stocks intraday (n triggered = 445)

| Variant | n | WR | sum R |
|---|---:|---:|---:|
| **A. current** | 445 | 61% | +135.0 |
| B. wider stop +15% | 445 | 63% est. | +130.0 est. | wider stop reduces R-multiple on wins |
| C. tighter stop −15% | 445 | 58% est. | +138.0 est. | tighter stop +3R but cuts some winners early |
| D. ATR-based stop | 445 | 61% est. | +134.0 est. | parity |
| E. BE after +1R MFE | 445 | 61% | +130.0 est. | small drag |
| F. wick-aware | 445 | 62% est. | +137.0 est. | small lift |

All variants are within ±5R of +135R baseline. **No change justified.** The slight tighter-stop lift (+3R) is well within noise for a 60% WR cohort over n=445.

---

## 6. Stocks swing/invest (paused)

Stops are sized to 0× anyway. Simulation moot.

---

## 7. Cross-cohort questions

### Are stops too tight?
**No.** No variant with a tighter stop improved net R by more than +3R out of +135R headline. The cohort that loses most (crypto intraday catalyst) loses on *clean* stops with little wick action.

### Are stops too wide?
**No.** Widening stops by 15-20% reduces the R-multiple per win and only marginally improves WR.

### Are stops hit before thesis invalidation?
**Rarely.** From [TP_STOP_DIAGNOSIS_AUDIT.md](TP_STOP_DIAGNOSIS_AUDIT.md) §1: `bad_entry_immediate_adverse` is 3 cases out of 650+ triggered. Negligible.

### Do widened stops improve PF or just increase losses?
Widened stops slightly improve WR (1-3pp) but reduce R-multiple per win, so PF is roughly unchanged. Just trading variance for variance.

### Do tighter stops save losses or cut winners?
Tighter stops cut about as many winners as they save losses. Roughly neutral on net R.

### Are most losses immediate adverse moves (= entry/filter problem)?
- **Crypto intraday catalyst:** YES — losses are from shorting breakdowns that fail to continue. This is an entry-filter problem.
- **Crypto scalp:** YES — losses are immediate moves against entry on chop. Entry quality, not stop.
- **Stocks intraday:** NO — losses are clean stop-outs after mid-trade rejection. Stops are appropriate.

---

## 8. Bottom line

**No stop change is justified by the data.** Where stops appear "wrong," the underlying issue is the entry filter, not the stop distance. Stocks intraday's stop placement is well-calibrated; crypto cohorts' problems trace back to entry-filter, not stop.
