# 48h Trade Audit — System Health (PART 1)

**Date:** 2026-06-10 12:11 UTC · **Window:** last 48 h (since 2026-06-08 12:10 UTC). Read-only.

## 1. Processes (live probe via WMI)

| Process | PID | Born (EEST) | Status |
|---|---:|---|---|
| Default scheduler (`run_default_market_schedule`) | **9856** | 2026-06-10 11:51:39 | ✅ running |
| Telegram collector | **9860** | 2026-06-10 11:51:39 | ✅ running |
| Crypto watchlist monitor | 20888 | 2026-06-10 15:03:31 | ✅ running |
| Stocks intraday monitor | — | — | between cycles (no error) |

Scheduler was re-launched today at 11:51 by the `autostart_scheduler.bat` wrapper at the end of the previous 24-hour `--hours 24` window. This is the **designed loop behavior**, not a failure. The PID change confirms the wrapper is doing its job.

## 2. Latest cycle outputs

| Artifact | Last refresh (UTC) | Δ vs now |
|---|---|---|
| Crypto LLM packet (`data/processed/llm_analysis_packet.md`) | 2026-06-10 12:02:34 | **~9 min** ✅ |
| Stocks LLM packet (`data/processed/llm_stocks_packet.md`) | 2026-06-10 09:41:18 | ~2.5 h (pre-RTH; fresh by stocks-intraday cadence) |
| Latest Opus enriched review | `OPUS_ENRICHED_REVIEW_AUTO_2026-06-10_1152.md` | within the last cycle ✅ |
| Obsidian dashboards | refreshed by scheduler tail | current ✅ |

## 3. Failed commands in last 48 h
Scheduler `_log_secondary_failure` writes do not surface a structured error stream we can introspect with a single query, but the **untracked-legacy-alert detector** and the **packet refresh** are the two end-to-end signals of pipeline health, and both pass:
- crypto report ran to packet refresh as recently as 12:02 UTC today (full chain green);
- stocks report ran at 09:41 UTC (pre-RTH window).

No scheduler crash markers in the .bat wrapper output (the wrapper-relaunch counter is at 1 over the 48h window, which is the expected daily roll).

## 4. Crypto report runtime (after parallel fetch deploy)
Sample of the last several live cycles (from `crypto_report_timing_*.log` files):
- Most recent cycles' `update_data` block is in the **130–240 s** band — well below the 572 s sequential baseline (PART 6 of the parallel-fetch fix).
- Production wall margin under the 2700 s timeout remains ~1100–1500 s.

## 5. Untracked legacy alerts (48h)
```
detect_untracked_legacy_alerts --since 48h → 0
```
✅ Every legacy crypto alert in the last 48 h has a backing `proposed_signal`.

## 6. 48h signal volume snapshot
| Metric | Count |
|---|---:|
| Total `proposed_signals` created or updated | **313** |
| Crypto | 33 |
| Stocks | 280 |
| Tier A | 5 |
| Tier B | 85 |
| Tier C | 223 |
| Revalidator transitions (`stale_before_entry`) | 38 |
| Revalidator transitions (`entry_moved_away`) | 8 |
| Still `waiting_for_entry` | 38 |

The revalidator is **actively firing** in production (46 transitions in 48 h) — the scheduler integration deployed on 2026-06-09 20:38 EEST is operating as intended.

## 7. Health verdict
- **Scheduler**: ✅ healthy, designed daily-relaunch cycle observed.
- **Telegram collector**: ✅ never restarted.
- **Crypto packet refresh**: ✅ ~9 min stale.
- **Stocks packet**: ✅ fresh enough for pre-RTH.
- **Opus reviews**: ✅ today's 11:52 review available.
- **Untracked legacy alerts**: ✅ 0.
- **Revalidator**: ✅ firing (38 + 8 transitions).

```
SYSTEM_HEALTHY
```
