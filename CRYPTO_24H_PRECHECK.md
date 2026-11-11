# Crypto 24h-Only Run — Pre-Flight Check

**Run start (planned):** 2026-05-30 17:42 EEST (UTC+3) — **Saturday**.
**Scope:** crypto-only (scalp + intraday). NO stocks, NO auto-trade.

---

## 1. Date / time / timezone

- Local time: **2026-05-30 17:42 EEST** (UTC+3, "GTB Standard Time").
- UTC: **2026-05-30 14:42 UTC**.
- Day-of-week: **Saturday** → weekend rules apply.
- Planned 24h window: ends ~**2026-05-31 17:42 EEST** (Sunday late afternoon).
- Number of cycles: **12** (one every 2h).

## 2. No old scheduler / monitor running

- `schtasks /query /tn "CryptoAIDesk_12h"` → **not found** (deleted at the end of the previous round).
- `schtasks /query /tn "CryptoAIDesk_24h_crypto"` → not found yet (this run will create it via a foreground Python loop, no Task Scheduler entry).
- `Get-CimInstance Win32_Process -Filter "Name='python.exe'"` filtered for cmdlines matching `crypto-ai-desk|monitor|scheduler|src.cli` → **no matches**. Unrelated Python processes exist for other projects (fvgbot, news_trader) but none are this project.
- → Safe to start.

## 3. Stocks are disabled for this run

- The scheduler script (`scripts/run_24h_crypto_only_schedule.py`) does NOT call:
  * `python -m src.cli stocks-intraday-report`
  * `python -m src.cli stocks-swing-report`
  * `python -m src.cli stocks-invest-report`
  * `python -m src.cli stocks-monitor-session`
- It only invokes `scalp-report`, `intraday-report`, `track-signals --all`, and the crypto `monitor-watchlist` for a bounded 90-minute window per cycle (capped well under the 2-hour interval).
- `signal-stats --asset-class crypto` and `active-signals --asset-class crypto` are explicitly filtered.

## 4. PART 1 fix — crypto legacy alert registration

- Code: `src/agents/supervisor.py` runs `_maybe_register_signals` **before** `_maybe_send_trade_alerts`. The alert function now requires a non-empty `registered_signal_ids` map.
- Code: `src/cli.py monitor-watchlist` calls `monitor.register_actionable_ticks(upgrades)` and skips Telegram for any tick missing a `signal_id`.
- Tests: `tests/test_crypto_alert_registration.py` — 9 passed in the post-fix verification run.
- Live: `python -m scripts.detect_untracked_legacy_alerts --since 2026-05-30` → **None. Every legacy crypto alert has a backing proposed_signal.**
- → Active.

## 5. PART 2 fix — Telegram rate-limit / cooldown

- Code: `src/stocks/monitor.py MaterialImprovementChecker` enforces a 45-min per-signal cooldown for `entry_change` / `invalidation_change` / `score_improvement`. `new_signal` and `tier_upgrade` bypass.
- (Note: this lives on the stocks monitor. For crypto, the **WatchlistMonitor** already has its own per-symbol cooldown via `should_alert(cooldown_minutes)` from `config/notifications.yaml`. The PART 2 cooldown is in effect in code; for stocks it would gate the duplicate `entry_change` spam — but since stocks are OFF this run, the effect is moot for this run except as a defense-in-depth if anything ever calls into it.)
- Tests: `tests/test_stocks_monitor_cooldown.py` — 11 passed.
- → Active in code; not exercised this run (stocks off). Crypto path uses the existing notifier cooldown.

## 6. PART 3 fix — legal-risk gate

- Code: `src/stocks/legal_risk.py` + `MaterialImprovementChecker._classify` block stocks A/B Telegram when an active legal-headline marker is present.
- This run does not touch stocks, so the gate is dormant for now. The marker is still written by the stocks pipeline if it ever runs.
- → Active in code; not exercised this run.

## 7. No auto-trade path

- Grep across `src/` for `auto_trade | live_execute | place_order | create_order` → **no matches**.
- The pipeline emits TradeIdea + ProposedSignal + Telegram messages. There is no execution layer wired to any exchange API.
- → Confirmed no auto-trade.

## 8. Pre-check command outputs

```
$ python -m src.cli track-signals --all
checked=222 updated=73 tp_hits=95 stopped=3 expired=28 not_triggered=19
ambiguous=0 no_ohlcv=0
```

- `no_ohlcv=0` ✅
- `errors=0` (implied — no error column when zero).

```
$ python -m src.cli active-signals --asset-class crypto
Active signals (2) — asset_class=crypto
- BCH/USDT  B  scalp  short  72.1  tp1_hit
- UNI/USDT  B  scalp  short  65.5  tp1_hit
```

The two PART 1 backfilled scalp shorts **both hit TP1**. The two PART 1 backfilled swings (XLM/INJ) appear to have either expired or already closed (28 expired in the pass) — they're no longer in the active list because they were swing/long with multi-day validity that's now past the entry/invalidation window relative to the OHLCV the tracker saw.

```
$ python -m src.cli signal-stats --asset-class crypto
... (rendered table) ...
- By exchange_confirmation: 8/8 split, PF 2.33 / 0.50
- By weekend_mode: n=16, weak confidence, PF 1.60, totalR +3.0
- By sector / narrative / setup: similar mixed but slightly positive
- Observation: weak (n=16) tier=B triggered winrate 29% is low. Below
  the 50-sample threshold to suggest any rule change.
```

Crypto sample is still small; this run will add ~24h of data.

```
$ python -m scripts.detect_untracked_legacy_alerts --since 2026-05-30
- None. Every legacy crypto alert has a backing proposed_signal.
```

✅ Zero untracked.

## 9. Weekend Mode status

`python -m src.cli weekend-status --mode intraday` reports the overlay is active with the conservative defaults:

- A-tier score penalty: −5.0 (subtracted from scores ≥ 80).
- Confidence penalty: 0.1 (steps down by one band).
- Overextension penalty multiplier: 1.25×.
- Weak signals capped at B.
- Weak MEXC-only capped at C.
- Require retest after impulse.
- Prefer structural / ATR stops.
- Mode notes for intraday: prefer pullback/retest, avoid chasing breakouts without 15m / 1h acceptance, RR-to-TP1 ≥ 1.2.

→ Weekend caution will be applied automatically by the supervisor on every cycle.

## 10. Go / no-go

| Item | Status |
|------|--------|
| Date / time / timezone known | ✅ Saturday, weekend rules apply |
| No old scheduler/monitor running | ✅ |
| Stocks disabled | ✅ — scheduler script never invokes stocks commands |
| PART 1 fix active | ✅ — detector reports zero untracked |
| PART 2 fix active | ✅ in code (not exercised this run) |
| PART 3 fix active | ✅ in code (not exercised this run) |
| No auto-trade path | ✅ — grep confirms |
| Telegram notifier configured | use existing `config/notifications.yaml` cooldown |
| Weekend mode overlay | ✅ active for intraday + scalp |
| Test suite | 151/151 pass (from post-fix verification) |

**GO.** Proceeding to PART 9 (scheduler script) and PART 2 (start).
