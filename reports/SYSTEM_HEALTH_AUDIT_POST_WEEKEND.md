# System Health Audit — Post-Weekend (READ-ONLY)

**As of:** 2026-06-07 ~13:15 EEST (Sun) · window: weekend (06-05 → 06-07). No
strategy/scoring changes. Only audit-script bugs fixed (see PART 10).

## 1. Default market scheduler
- **Running** — python PID **13864** (parent autostart cmd), born 06-07 11:08;
  Windows task `CryptoAIDesk_Scheduler` State=**Running**.
- **Cadence:** 2 h interval, `--hours 24` per boot, `--monitor-minutes 90`,
  `--send-telegram`. Autostart `.bat` relaunches on exit (infinite loop).
- **Restarts over weekend (all self-healed by the loop):**
  - 06-06 09:47 — boot-time **DLL init race** `exit=-1073741502` (0xC0000142),
    retried ~12× in <1 s, booted clean at 09:48:47. Known logon-race; the loop
    is designed to absorb it.
  - 06-06 09:48 relogin + 06-07 11:08 — fresh 24 h boots (cycle counter resets
    to 1 each boot; expected).
- **Cycle results (weekend):** `CYCLE END ok=9–11 failed=0–2`. Clean overnight
  (cycles 06-07 00:38 & 04:01 = **failed=0**); daytime cycles **failed=2**.
- **⚠ Recurring step TIMEOUT (P1 infra):** `crypto scalp report` and
  `crypto intraday report` hit the **2700 s (45 min)** wall on most *daytime*
  cycles (e.g. 06-07 06:47 scalp, 07:32 intraday). Overnight cycles finish well
  under it. → intermittent, **load/network-correlated**, not a simple low-limit
  bug (timeout was already bumped 1500→1800→2700). Non-fatal (cycle continues;
  failed steps just skip that report). Documented as **TODO-crypto-report-timeout**
  with a safe diagnostic proposal — NOT changed blind (see PART 10).
- **No SQLite locks**, no stale/hung cycles, no DLL errors mid-run. Tracebacks:
  only the boot DLL race above.

## 2. Telegram collector
- **Running** — PID **11136** (since 06-06 09:48); task
  `CryptoAIDesk_TelegramCollector` State=Running.
- Connected as `@sbegemotho`, listening on **18 channels**.
- **Ingest:** news_items **614 / 24h, 1345 / 48h, 2304 / 72h** (total 5821).
  Telegram bridge active (sources `t.me/lookonchain` 122, `t.me/WalterBloomberg`
  59 in 48h). No collector errors. Bridge OK.

## 3. Crypto monitor
- **Running** — per-cycle child PID **3584** (lock
  `2026-06-07_default_schedule/crypto_monitor.pid`), plus `CryptoWatchlistMonitor`
  Windows task Running (next 13:23). Cooldown/dedup intact.
- **Untracked legacy alerts: 0** — every crypto `signal_alert` has a backing
  `proposed_signal`. Bad asset_class rows: **0**.

## 4. Stocks monitor
- **Correctly INACTIVE this weekend.** The scheduler runs `crypto-only` on
  weekends → no stocks monitor child spawned (no `stocks_monitor.pid` today).
  `--market-hours-only` would no-op it anyway (US cash closed Sat/Sun).
- **No inappropriate weekend stock alerts** — 0 stock `signal_alerts` over the
  weekend window after the Friday close.
- **Swing pause active** (verified live, see `POST_WEEKEND_FIX_VERIFICATION.md`):
  post-fix swing → C; 0 new swing A/B.
- **Telegram 400 fix active**: 0 `failed:HTTPError` after the fix.

## 5. Scheduled tasks
| Task | State | Note |
|---|---|---|
| CryptoAIDesk_Scheduler | **Running** | PID 13864, healthy |
| CryptoAIDesk_TelegramCollector | **Running** | PID 11136 |
| CryptoWatchlistMonitor | **Running** | next 06-07 13:23 |
| CryptoAIDesk_Frequent | Ready (idle) | legacy, not used |
| opus-enriched-review-4h (+ -preus/-postclose) | **enabled** | all firing; lastRun 4h=06-07 08:39 UTC; reviews produced every slot |
| opus-decision-us-open / -evening | disabled | superseded (expected) |
| enriched-review-cycle-6 | disabled | one-time legacy |

## Health verdict
```
SYSTEM_HEALTHY (one non-fatal infra TODO: crypto-report timeout)
```
All core components up and producing fresh data (scheduler, collector, crypto
monitor, tracker, Opus). Untracked alerts 0, data contamination 0. The single
blemish is the intermittent daytime crypto scalp/intraday report timeout — a
performance/network issue that degrades signal *freshness* on some cycles but
corrupts nothing and self-recovers. Stocks correctly idle (weekend).
