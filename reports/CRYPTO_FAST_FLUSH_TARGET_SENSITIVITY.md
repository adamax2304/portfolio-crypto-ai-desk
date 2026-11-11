# Crypto Fast Flush - Profit Target Sensitivity

- generated: `2026-09-29T16:24:56.092552+00:00`
- medium-deep candidate trades: `25`
- reconstructed trades: `25`
- baseline replay max absolute delta: `0.0`

Entry, structural stop, 70/30 exits, breakeven-after-TP1, 45-minute timeout, fees, slippage, and stop-first intrabar handling are unchanged. Only TP prices differ.

A reclaim level below a confirmed long entry is not treated as a target. Strict structural variants are reported with their availability so missing geometry cannot be hidden.

| Variant | Coverage | Median TP R | Train | Validation | Latest test | All |
|---|---:|---:|---:|---:|---:|---:|
| `BASELINE_R_080_135` | 25/25 | 0.8/1.35 | n=11, +4.550R, PF=4.764, win=81.8%, DD=$11.61 | n=9, +2.131R, PF=1.895, win=77.8%, DD=$14.97 | n=5, +3.334R, PF=None, win=100.0%, DD=$0.00 | n=25, +10.015R, PF=3.791, win=84.0%, DD=$14.98 |
| `TIGHT_R_065_115` | 25/25 | 0.65/1.15 | n=11, +3.755R, PF=4.234, win=90.9%, DD=$11.61 | n=9, +2.836R, PF=3.322, win=88.9%, DD=$12.21 | n=5, +2.807R, PF=None, win=100.0%, DD=$0.00 | n=25, +9.398R, PF=4.944, win=92.0%, DD=$12.21 |
| `EXTENDED_R_100_175` | 25/25 | 1.0/1.75 | n=11, +6.096R, PF=6.043, win=81.8%, DD=$11.61 | n=9, +2.262R, PF=1.951, win=77.8%, DD=$12.38 | n=5, +4.393R, PF=None, win=100.0%, DD=$0.00 | n=25, +12.751R, PF=4.553, win=84.0%, DD=$12.38 |
| `PREVIOUS_CLOSE_RECOVERY` | 25/25 | 0.535/1.071 | n=11, +3.362R, PF=None, win=100.0%, DD=$0.00 | n=9, +2.647R, PF=3.167, win=88.9%, DD=$12.21 | n=5, +2.266R, PF=None, win=100.0%, DD=$0.00 | n=25, +8.275R, PF=7.775, win=96.0%, DD=$12.21 |
| `VWAP1H_THEN_PREVIOUS_CLOSE` | 24/25 | 0.727/1.093 | n=11, +4.118R, PF=4.546, win=90.9%, DD=$11.61 | n=9, +2.983R, PF=2.253, win=77.8%, DD=$12.21 | n=4, +2.283R, PF=None, win=100.0%, DD=$0.00 | n=24, +9.384R, PF=3.65, win=87.5%, DD=$12.21 |
| `VWAP4H_THEN_PREVIOUS_CLOSE` | 22/25 | 0.969/2.008 | n=10, +5.994R, PF=None, win=100.0%, DD=$0.00 | n=8, +3.992R, PF=4.269, win=87.5%, DD=$12.21 | n=4, +3.056R, PF=None, win=100.0%, DD=$0.00 | n=22, +13.042R, PF=11.678, win=95.5%, DD=$12.21 |
| `HYBRID_VWAP1H_CLAMPED` | 25/25 | 0.8/1.1 | n=11, +4.839R, PF=5.168, win=90.9%, DD=$11.61 | n=9, +2.831R, PF=2.19, win=77.8%, DD=$12.67 | n=5, +3.234R, PF=None, win=100.0%, DD=$0.00 | n=25, +10.904R, PF=4.08, win=88.0%, DD=$12.67 |
| `HYBRID_VWAP4H_CLAMPED` | 25/25 | 1.0/1.1 | n=11, +4.619R, PF=4.821, win=81.8%, DD=$11.61 | n=9, +2.821R, PF=2.186, win=77.8%, DD=$12.67 | n=5, +3.835R, PF=None, win=100.0%, DD=$0.00 | n=25, +11.275R, PF=4.142, win=84.0%, DD=$12.67 |

## Interpretation

A full-coverage alternative improved both the latest test and the complete sample: `EXTENDED_R_100_175`, `HYBRID_VWAP4H_CLAMPED`. It should still be verified in a separate Paper lane.

No production or Paper profile was changed by this research run.
