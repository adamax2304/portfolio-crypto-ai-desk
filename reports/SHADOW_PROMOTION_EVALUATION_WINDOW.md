# Shadow Promotion — Evaluation Window (PART 0)

**Date:** 2026-06-19 ~18:08 UTC.

## Window
- **evaluation_start_utc:** `2026-06-18 15:39` — the first **stable persistent-monitor** restart (`CryptoAIDeskMonitor` task; root-caused the prior reaping). Forward data is only trustworthy from here.
- **evaluation_end_utc:** `2026-06-19 18:08`.
- **monitor_uptime (current PID):** ~331 min (the 06-19 15:37 UTC new-display-code restart; continuous with the 06-18 fix — track-signals re-walks history, so the restart caused no classification gap).
- **cycle_count (window):** continuous 2h cycles since 06-18 15:39; the latest two on new code = `CYCLE 1 END ok=25/0`, `CYCLE 2 END ok=21/0`.
- **valid_cycles:** all cycles since 06-18 15:39 (heartbeat `problems: []`, ok=N/0 each).
- **invalid/stale cycles:** the pre-fix gap **12:29 → 15:39 UTC on 06-18** is excluded (no cycles ran). Everything before 06-18 15:39 is pre-stable and excluded from forward promotion.
- **Telegram / paper-monitor:** alive (status sends succeed; close-alert lifecycle wording live).
- **fresh reports/caches:** scalp/intraday/stocks reports refreshing each cycle; intel `deriv_cache`/`phase_cache` last 16:36 UTC; catalyst integrity `ok`.

## Decisive sizing fact
The window is **~26.5 hours**. The number of **closed actionable paper decisions** (tier A/B, non-scalp crypto, non-swing/invest stocks) in it = **5** (see `SHADOW_PROMOTION_DATASET_SUMMARY.md`): 1 win / 4 losses, net −3R. Five decisions is far below the promotion gates (≥30 for PROMOTE_NOW, ≥15 for PROMOTE_PAPER_ONLY).

## Verdict
**EVALUATION_WINDOW_TOO_SHORT** for promoting any *trade-affecting* shadow feature. The window is valid and clean for **system-health** and **display/advisory** evaluation, but it cannot support statistical promotion of any guard/exit/intelligence feature that changes decisions. (Display/UX/advisory features are judged mechanically, not by sample size — see PART 5.)
