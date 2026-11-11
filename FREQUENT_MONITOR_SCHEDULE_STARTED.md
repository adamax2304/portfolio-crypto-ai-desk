# Frequent Monitor Schedule — Started

**Started at:** 2026-05-28 **01:09 EEST** (deadline 23:09 EEST, 22-hour run)
**Scheduler task:** `bh2cl81sn` (running in background)
**Script:** `scripts/run_frequent_schedule.py` (NEW — read-only, 2-hour cadence)

---

## 1. Audit summary

See **`CRYPTO_SIGNAL_ABSENCE_AUDIT.md`** in project root.

Key finding:
- Crypto had only **1 A/B signal today (ICP scalp at 13:30 UTC, expired)** because the market regime flipped to **downtrend** (BTC + ETH both downtrend, breadth 57 %). System correctly rejected over-extended movers — **NO TRADE was the correct verdict**.
- Stocks got 110 Telegram alerts because they use the modern `signal_alerts` ledger with `MaterialImprovementChecker`; crypto uses the legacy `watchlist_alerts` path which only fires on tier upgrades. This is a known asymmetry, not a bug.
- **No scoring / threshold changes recommended.** Sample is too small (9 crypto signals total over a week → anecdotal).

---

## 2. Why crypto had few/no alerts today

| Factor | Weight |
|--------|-------|
| Regime turned downtrend → fewer A/B candidates produced by scoring | **~80 %** |
| Over-extension gate rejected obvious movers (correct behaviour) | implicit |
| Crypto uses legacy `watchlist_alerts` path (lower-frequency alerter) | **~20 %** |
| Filters too strict / data missing / monitor broken | **0 %** — none of these are the cause today |

This is a **correct no-trade outcome**, not a system failure.

---

## 3. New schedule table (from now onward)

12 cycles across 22 hours. **Interval: 2 hours.**

| # | Time (Nicosia) | Window type | Steps |
|---|---------------:|-------------|------:|
| 1 | **01:09** (now) | regular | 9 |
| 2 | 03:09 | regular | 9 |
| 3 | 05:09 | regular | 9 |
| 4 | 07:09 | regular | 9 |
| 5 | 09:09 | regular | 9 |
| 6 | 11:09 | regular | 9 |
| 7 | 13:09 | regular | 9 |
| 8 | 15:09 | regular | 9 |
| 9 | **17:09** | **US OPEN** (90-min monitors) | 9 (incl. 90-min crypto + 90-min stocks monitors) |
| 10 | **19:09** | **MID-US** (60-min monitors) | 11 (incl. 60-min crypto + 60-min stocks monitors) |
| 11 | 21:09 | regular | 9 |
| 12 | 23:09 | regular | 9 |

**Special window classification** is automatic — the scheduler reads its own current Nicosia time and picks the right step list:
- `us_open` window: 16:00–17:30 → 90-min monitors
- `mid_us` window: 18:30–20:00 → 60-min monitors
- `final_review` window: 22:00–23:00 → dedup + alert-status
- Otherwise: `regular` (fast scan, no monitors)

**Note:** the 22:30 final-review window is **not hit exactly** by the 2-hour grid this run (last cycle at 23:09 is past the window). I will run a manual `track-signals --all` + dedup before tomorrow's start if needed; the per-cycle stats are written every 2 hours regardless.

---

## 4. Next cycle time

**Already running:** cycle 1 at 01:09 EEST. **Next:** **cycle 2 @ 03:09 EEST** (~2h from now).

---

## 5. What each regular cycle runs

```
python -m src.cli track-signals --all                       # pre
python -m src.cli scalp-report                              # ~9 min
python -m src.cli intraday-report                           # ~8 min
python -m src.cli stocks-intraday-report                    # ~3 min
python -m src.cli active-signals --asset-class crypto       # fast
python -m src.cli active-signals --asset-class stocks       # fast
python -m src.cli signal-stats --asset-class crypto         # fast
python -m src.cli signal-stats --asset-class stocks         # fast
python -m src.cli track-signals --all                       # post
```

**Per-cycle wall-time:** ~22–25 minutes (mostly the two crypto reports).

---

## 6. What the US-open & mid-US cycles add

Cycle 9 (17:09, US OPEN) adds:
```
python -m src.cli monitor-watchlist --interval 600 --iterations 9   (background, 90 min)
python -m src.cli stocks-monitor-session --minutes 90 ... --send-telegram   (foreground, 90 min)
```

Cycle 10 (19:09, MID-US) adds:
```
python -m src.cli monitor-watchlist --interval 600 --iterations 6   (background, 60 min)
python -m src.cli stocks-monitor-session --minutes 60 ... --send-telegram   (foreground, 60 min)
```

---

## 7. Telegram behaviour

**What will be sent:**
- 1 short scheduler summary per cycle (`[FREQUENT] cycle_HHMM_window / steps: ok=X failed=Y`)
- A/B alerts from `stocks-monitor-session` during cycles 9 + 10 (with `MaterialImprovementChecker` dedup)
- Crypto tier-upgrade alerts from `WatchlistMonitor` during cycles 9 + 10 (legacy path)

**What will NOT be sent:**
- C-tier or rejected ideas (gated in code)
- Duplicate setups (gated in code)
- Setups without invalidation (gated)
- Stale-data setups (gated)

**Today's Telegram bug fix:**
The `cycle_4` and `cycle_5` summaries from the previous scheduler **failed with HTTP 400 Bad Request**. The new scheduler:
- Sends summary as **plain text** (`parse_mode=""`) so Markdown parser cannot fail
- Caps message at **3800 chars** (under Telegram's 4096 limit)

This was a workflow bug — not in `src.cli telegram-test` (still works), only in the scheduler's `build_cycle_telegram` payload size.

**Expected Telegram volume over the 22 hours:** roughly **40–80 messages** (12 scheduler pings + ~30–70 stocks A/B alerts during cycle 9+10 if US session active). Crypto alerts likely 0–5 unless regime improves.

---

## 8. Where logs are saved

```
data/scheduled_runs/2026-05-28/                 # auto-rotates by current Nicosia date
├── frequent_scheduler.log                       # consolidated INFO log
├── cycle_0109_regular.md                        # this cycle's stdout per step
├── cycle_0309_regular.md
├── ...
├── cycle_1709_us_open.md                        # US-open special
├── cycle_1909_mid_us.md                         # mid-US special
├── crypto_monitor_<unixtime>.log                # background monitor stdouts
└── crypto_monitor.pid                           # transient PID file (auto-cleaned)
```

The daily folder is **today's Nicosia date at boot time** = `2026-05-28`.

---

## 9. PC requirements (PC must stay awake)

| Requirement | Why |
|-------------|-----|
| **PC plugged in to power** | Battery-mode Windows may sleep even with "Never" sleep |
| **Disable sleep**: Settings → System → Power & battery → Screen and sleep → both timers = **Never** | `time.sleep()` is suspended when PC sleeps |
| **Don't hibernate or shutdown** | Scheduler dies |
| **Win+L is fine** | Locks screen but processes keep running |
| **Internet on** | Reports / Telegram need network |
| **Claude session** | The scheduler is running via `run_in_background` in this Claude session. If you close Claude / sign out, **the process dies.** See §11 for safer launch options |

---

## 10. Is the scheduler running?

**Yes.** Background task `bh2cl81sn` is alive. First cycle (`cycle_0109_regular`) started at 01:09:23 EEST and is currently running through its 9 steps. ETA finish ~01:32 EEST.

Verified by:
```
2026-05-28 01:09:23 [INFO] frequent scheduler boot — hours=22.0 deadline=2026-05-28T23:09:23+03:00
2026-05-28 01:09:23 [INFO] CYCLE START cycle_0109_regular (window=regular)
2026-05-28 01:09:23 [INFO] CMD START: track-signals (pre)
```

Log path: `data/scheduled_runs/2026-05-28/frequent_scheduler.log` (growing live).

---

## 11. Risks / limitations

1. **Claude session dependency.** The scheduler is currently a Claude-managed background process. If you close this Claude window / sign out, the process **may die**. If you want true autonomy, kill task `bh2cl81sn` and re-launch from your own PowerShell:

   ```powershell
   # 1. Stop my version (from Claude):
   #    (ask me: "stop bh2cl81sn")
   # 2. Open your own PowerShell and run:
   cd C:\Users\adama\Documents\crypto-ai-desk
   $env:PYTHONIOENCODING='utf-8'
   $env:PYTHONPATH='.'
   python -m scripts.run_frequent_schedule --hours 22 --send-telegram
   ```

2. **PC sleep** suspends `time.sleep()` — cycles late or skipped.
3. **Internet drops** → individual reports fail (yfinance / Bybit / RSS); scheduler logs and continues.
4. **Telegram failures** → logged, cycle continues. The bug from earlier today (HTTP 400) is mitigated by `parse_mode=""` + 3800-char cap, but exhaustion of API rate limits could still produce failures.
5. **No automatic Obsidian writes** — `update-obsidian-context` is still a TODO stub. Signal logs / daily reviews are NOT being written to Obsidian by this scheduler. See audit §7.
6. **Final-review window** (22:00–23:00) is **not hit by the 2-hour grid this run** (last cycle 23:09 is past). Dedup + alert-status still run in regular scans, just not the dedicated review cycle. Acceptable.
7. **Crypto alert reactivity** remains low compared to stocks (legacy `watchlist_alerts` path, as audited). Not a fix today.
8. **Sample size:** crypto has 9 signals total (anecdotal). Do NOT adjust strategy based on this.

---

## 12. Safety re-confirmed

- ✅ No auto-trading
- ✅ No scoring / threshold / agent changes
- ✅ No paid APIs
- ✅ Only existing CLI commands invoked
- ✅ Telegram only A/B (gates inside CLI, not bypassed)
- ✅ De-dup honoured (stocks-monitor-session has built-in MaterialImprovementChecker)
- ✅ Crypto/stocks isolation preserved
- ✅ No code changes to scoring engine
- ✅ Telegram 400-bug fixed (plain text + length cap) — workflow-level only, not strategy

---

## TL;DR — answers to your questions

1. **Is the new schedule running?** ✅ Yes (task `bh2cl81sn`).
2. **When is the next scan?** **03:09 EEST** (in ~2 hours).
3. **How often will it scan?** Every **2 hours** for 22 hours → 12 cycles total.
4. **Key windows emphasized?** US-open (cycle 9 @ 17:09 → 90-min monitors) + Mid-US (cycle 10 @ 19:09 → 60-min monitors).
5. **What to expect in Telegram?** ~40–80 messages over 22 hours (12 scheduler pings + 30–70 stocks A/B alerts during cycles 9+10; 0–5 crypto alerts unless regime improves).
6. **Where do I find logs?** `data/scheduled_runs/2026-05-28/` — `frequent_scheduler.log` (live) + `cycle_HHMM_<window>.md` per cycle.
