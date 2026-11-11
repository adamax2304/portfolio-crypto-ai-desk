# Post-Scheduler-Stop Snapshot

**Stopped at:** 2026-05-29 20:37 EEST. Switching monitoring → fix mode.

---

## Scheduler status (before/after stop)

- **Before:** 12h scheduler (`run_12h_monitor_schedule`) running as Task Scheduler task `CryptoAIDesk_12h`. Was mid **cycle 3** (US-window): started 60-min stocks monitor at 20:10, crypto monitor (pid 15036) at 20:10.
- **Action taken (safe stop):**
  1. `schtasks /delete /tn "CryptoAIDesk_12h" /f` → task removed (no future re-trigger).
  2. `taskkill /F /PID 23300` → scheduler **loop** terminated (prevents cycle 4+).
  3. **In-flight monitors LEFT to finish** (per instruction "let current command finish if mid-write"):
     - pid 4668 = stocks-monitor-session (60 min, ends ~21:10)
     - pid 15036 = crypto monitor-watchlist (ends ~21:10)
  - These self-terminate; no blind kill of writing processes. SQLite is transactional → no corruption risk.
- **After:** no scheduler loop, no task. Two monitors finishing their current cycle, then idle.

## Completed cycles today (12h run)

- **Cycle 1** (13:10–14:04): regular + swing/invest (once). ok=12, telegram=sent.
- **Cycle 2** (16:04–17:43): US-window, 60-min stocks monitor, A-tier emerged (AAPL/SMCI A, LLY→A). ok=11, telegram=sent. **78 alerts** (entry_change spam).
- **Cycle 3** (19:5x–~21:10): US-window, in-flight at stop time; monitors finishing.

## Data snapshot (at stop)

```
track-signals --all: checked=215 updated=55 tp_hits=91 stopped=22 expired=0 no_ohlcv=0 errors=0
crypto: sample=12 (weak) | triggered=10 | wins=0 losses=5 | PF=0.0 avgR=-0.5 totalR=-5.0
stocks: sample=711 (inflated) | triggered=471 | wins=101 losses=99 amb=1 | PF=1.53 avgR=0.11 totalR=+53.0
```
Note: stocks PF fell 2.37 → 1.53 as cycle-3 stops registered (the early 100%-winrate artifact is washing out → more honest now). Still raw/inflated; trust dedup.

## Untracked legacy crypto alerts (unchanged — fix target)

| symbol | tier | mode | dir | score | sent (UTC) |
|--------|------|------|-----|------:|------------|
| UNI/USDT | B | scalp | short | 65.5 | 08:36 |
| BCH/USDT | B | scalp | short | 72.1 | 08:45 |
| XLM/USDT | B | swing | long | 65.4 | 10:56 |
| INJ/USDT | B | swing | long | 66.1 | 11:36 |

**4 untracked** → crypto PF/winrate incomplete. Fix target = PART 1.

## Files generated today

- Reports: 5 scalp, 5 intraday, ~14 stocks intraday + swing/invest (cycle 1).
- `data/scheduled_runs/2026-05-29_12h_monitor/`: scheduler.log, cycle_1_summary.md, cycle_2_summary.md (cycle_3 summary may be absent — loop killed before it wrote).
- Review files: OPUS_MANUAL_REVIEW_LATEST_ANALYSIS.md, OPUS_ENRICHED_MARKET_REVIEW_LATEST.md, OPUS_ENRICHED_REVIEW_CYCLE2.md.
- Audits: CRYPTO_ALERT_REGISTRATION_AUDIT.md, CRYPTO_SHORTS_AUDIT.md, AUDIT_NOTE_UNTRACKED_LEGACY_CRYPTO_ALERTS.md, LLM_INTEGRATION_AUDIT.md.

## Known issues (fix queue)

1. **Crypto legacy alerts → no proposed_signal** (PART 1) — 4 today; crypto stats incomplete.
2. **Telegram spam** — 78 alerts/cycle, mostly entry_change re-fires (PART 2).
3. **Stocks A-tier blind to legal/headline risk** — SMCI A-tier with active federal indictment (PART 3).
4. **News source discipline** — enriched review needs mandatory citations (PART 4).
5. **Obsidian dormant** — no live daily logging (PART 5).

## No data deleted. All reports/DB/logs preserved.
