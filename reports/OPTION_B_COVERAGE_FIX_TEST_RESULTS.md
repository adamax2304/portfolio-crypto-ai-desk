# Option B Coverage Fix — Test Results (PART 6)

**Date:** 2026-06-16

## New suite — `tests/test_option_b_pending_symbol_refresh.py` (12 passed)
1. pending selector includes discovery alt with A/B waiting_for_entry ✅
2. excludes C-tier ✅
3. excludes terminal statuses (expired/stopped/tp3_hit) ✅
4. distinct symbols + metadata ✅
5. scalp included but deprioritized + `include_scalp=False` drops it ✅
6. store error fails safe (no crash) ✅
7. crypto intraday thresholds unchanged (2/5/15) ✅
8. crypto scalp thresholds tight ✅
9. stocks intraday 16/20/24m **not** very_late (+ "candle floor" note); 50m is very_late ✅
10. unknown mode → tight default ✅
11. **structural:** refresh block precedes `track_pending_entries` in `cli.py` ✅
12. **structural:** latency audit joins by `signal_id`, not symbol+mode ✅

## Regression (all green)
| Suite | Result |
|-------|--------|
| test_option_b_pending_symbol_refresh | 12 passed |
| test_pending_tracker_option_b | passed |
| test_alert_dispatch_gates | passed |
| test_paper_entry_alerts | passed |
| test_scalp_downgrade | passed |
| test_telegram_standardization | passed |
| test_stock_concentration_caps | passed |
| test_sizing | passed |
| **Combined run** | **118 passed, 0 failed** |

(Test #5 "refresh runs before tracker" and #10 "audit join" are structural source-order /
content asserts, since the full CLI tick requires live network — the end-to-end ordering is
also confirmed live in PART 7.)

**PART 6 status: DONE — coverage-fix suite + regression green.**
