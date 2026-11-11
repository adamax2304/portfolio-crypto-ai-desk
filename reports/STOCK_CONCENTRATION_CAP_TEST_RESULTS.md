# Concentration Cap — Test Results (PART 7)

**Date:** 2026-06-16

## New suite — `tests/test_stock_concentration_caps.py` (20 passed)
Covers the spec's 18 cases:
1–2 proxy collapse (QQQ/XLK, SPY/DIA/IWM) keep best, shadow rest ✅
3–5 sector cap 1.0×/0.5×/0× ✅ · 6 existing position counts ✅ · 7 opposite dir not capped ✅
8 different bucket not capped ✅ · 9 C-tier not promoted ✅ · 10 stocks swing/invest stay 0× ✅
11 crypto unaffected ✅ · 12 crypto scalp stays shadow 0× ✅ · 13–14 no score/TP/SL change, raw R
preserved ✅ · 15–16 half-size warning text / shadow-cap not pushed ✅ · 17 unknown symbol safe ✅
18 input not mutated ✅ · plus 5 **live paper-entry** integration tests (1st sends, 2nd
half-size warning, 3rd shadow not pushed, proxy-duplicate shadow, crypto unaffected).

## Regression (all green)
| Suite | Result |
|-------|--------|
| test_stock_concentration_caps | 20 passed |
| test_sizing | 19 passed |
| test_scalp_downgrade | 10 passed |
| test_paper_entry_alerts | 14 passed |
| test_telegram_standardization | 24 passed |
| test_alert_dispatch_gates + test_pending_tracker_option_b (+ risk_cluster) | green |
| **Combined touched-area run** | **119 passed, 0 failed** |

Full suite not run end-to-end here (contains the known pre-existing slow/stale
stocks-Telegram *format* tests, unrelated to this change). Every code path touched by the
concentration overlay is covered above.

**PART 7 status: DONE — all concentration + regression tests pass.**
