# Expired Positive-MFE Opportunity Audit (PART 2)

**Date:** 2026-06-14 11:11 UTC
**Scope:** A/B triggered signals where `final_outcome='expired'` and MFE > +0.05R.

## Headline

- Triggered A/B trades total: **650**
- Expired with positive MFE > +0.05R: **261** (40.2%)
- Of those, MFE later reversed to deeply adverse (MAE < −0.8R): **29**

## MFE bucket distribution

| MFE bucket | n |
|---|---:|
| 0-0.3R | 72 |
| 0.3-0.5R | 63 |
| 0.5-0.7R | 35 |
| 0.7-1R | 77 |
| >=1R | 14 |

## Hypothetical partial-TP uplift

| Policy | Naive uplift | Caveat |
|---|---:|---|
| 50% close @ +0.3R | **+28.3R** | catches more trades but each contributes only +0.15R |
| 50% close @ +0.5R | **+31.5R** | catches fewer trades but each contributes +0.25R |

## Winner-cut risk

- Full winners (final_r > +0.8R): **169**
- Of those, MFE ≥ +0.5R BEFORE final TP: **169** would have had 50% closed at +0.5R
- Estimated winner cut cost (50% × (final_r − 0.5R)): **101.2R**

## Net of partial-TP @ +0.5R

- Naive uplift: **+31.5R**
- Naive cost: **−101.2R**
- **Net: -69.8R** across all A/B triggered trades over 20 days

## Interpretation

- Partial-TP @ +0.5R would have **lost** 69.8R net by cutting winners short.

**No TP change is implemented.** This is research only.