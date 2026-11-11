# Full System Health Audit — 48H (READ-ONLY)

**As of:** 2026-06-05 20:30 EEST · window: last 48h. No changes made.

## 1. Default scheduler
- **Running** — python PID **37572**; task State Running.
- 24h auto-restart loop healthy: boots 06-04 15:21, 06-04 16:00, 06-05 16:01
  (the .bat relaunches after each 24h `--hours 24` run; expected, not a crash).
- ~13 cycles in 48h, mostly `ok=16/19 failed=0`, `telegram=sent`.
- Avg durations: crypto scalp ~1360–1760s, intraday ~1340–1410s, stocks
  intraday ~750–850s. Comfortably under the 2 h interval.
- **1 transient cycle failure** (cycle 2, 06-05 20:04): crypto scalp + intraday
  both `exit=1` — root cause = **network connection error** (urllib3
  `create_connection` traceback), NOT a code bug (the identical build ran
  `exit=0` the prior cycle at 16:31). Self-recovers next cycle.
- No SQLite locks, no DLL (0xC0000142) errors, no stale cycles. One old TIMEOUT
  (06-02) and one recurring crypto-swing `exit=1` (06-03), both pre-window.

## 2. Telegram collector
- **Running** — PID 26656 (since 06-03). Bridge feeding catalyst/news.
- **⚠ Delivery bug:** stocks-monitor Telegram sends failing — over 48h
  `signal_alerts`: **76 sent, 15 `failed:HTTPError` (400), 3 `failed:ReadTimeout`,
  7 dry_run**. ~19% of stock alerts not delivered (400 Bad Request — likely a
  Markdown-parse issue in the alert text, same class as a `parse_mode` 400).
  → **TODO-stocks-telegram-400** (P1, operational).

## 3. Crypto monitor
- **Running** — PID 37880. Alerts generated, cooldown/dedup intact.
- **Untracked legacy alerts: 0** (detector clean). Every A/B alert has a backing
  `proposed_signal`.

## 4. Stocks monitor
- **Running** — PID 36276. Gates verified active in production:
  - market-closed intraday gate ✅ (overnight A/B demoted to C).
  - post-earnings stale gate ✅ (AVGO-class).
  - legal gate ✅ (SMCI = C + flag).
  - ETF earnings N/A ✅.
- Noise: yfinance `404 No fundamentals` for ETFs (DIA/SMH/XLK/XLF/XLE/XLY/XLV) —
  cosmetic logging, not fatal (ETF gate already handles them).

## 5. Catalyst / narrative
- ~1,400 catalyst events/day, importance non-zero (avg ~0.44), top narratives
  ranked sensibly; **symbol mapping ~24%** (persistent weak spot, context-only).
- Reaches reports + LLM packets + Opus reviews. No cross-asset contamination
  (`proposed_signals` bad asset_class = 0).

## 6. Opus auto-review
- **New market-aware schedule live & correct:** review titles carry slot type —
  e.g. "US open reaction review" (18:30), "pre-US-open decision review" (16:20).
- Uses WebSearch/WebFetch (8–9 cited URLs/review), compares prior review,
  no permission-heavy actions, no auto-trade / code edits.
- **Adds value:** independently flags the AVGO stale setup, the stocks
  swing/A-tier weakness — matching this audit.

## 7. Obsidian / dashboards
- Dashboard + daily review refreshed each cycle (last 06-05 20:19). Not stale.

## Health verdict
```
SYSTEM_PARTIAL
```
Core infra is **healthy and stable** (scheduler, monitors, collector, gates,
reporting, Opus all working; 0 untracked alerts; 0 data contamination). Two
non-fatal issues hold it back from fully-healthy: **(1) stocks-monitor Telegram
400 delivery failures (~19%)** and **(2) a transient network-caused cycle
failure**. Neither corrupts data or trades.
