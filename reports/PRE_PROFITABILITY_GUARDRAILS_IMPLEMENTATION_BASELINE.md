# PRE — Profitability Guardrails Implementation Baseline (PART 0)

**Date:** 2026-06-17 · **Stage:** alert-only / shadow-only / diagnostic / add-only guardrails + catalyst-integrity monitoring. **No production strategy change.**

## Current state (verified read-only)

### Code / fix status
- **Catalyst ASTER fix is present** (prior stage): `src/catalysts/collector.py` (`news_catalyst_symbols()`, `CATALYST_MIN_IMPORTANCE=1.0`) + `src/catalysts/baskets.py` (`build_momentum_breakout_basket(catalyst_symbols=...)`). Label-only; ASTER-like → catalyst-backed watch-pullback, never actionable.
- **Full test suite green at baseline:** `python -m pytest tests/ -q` → **687 passed** (run 2026-06-17).

### DB / schema (db/crypto_ai_desk.sqlite, 1,526 MB, read mode=ro for analysis)
- `proposed_signals`: 2,017 rows. Cols incl. signal_id, symbol, asset_class, mode, tier, direction, status, market_regime, created_at, stop_loss, tp1/2/3, expires_at, news_supported.
- `signal_outcomes`: 152,994 rows. Cols incl. final_r, final_outcome (win/loss/partial_win/expired/not_triggered/ambiguous), stop_hit, stop_hit_at, tp{1,2,3}_hit_at, entry_triggered_at, mfe_r/mae_r, checked_at.
- `signal_alerts`: 1,220 rows. Cols incl. alert_type, payload_json, sent_at, telegram_status, message_hash. Dedupe by `signal_id` + `alert_type='paper_entry'`.
- `news_items`: 15,854 rows; `detected_symbols_json` is the live symbol column (no legacy column).

### Config (verbatim, unchanged this stage)
- `config/signal_tracking.yaml`: validity scalp=2h, intraday=24h, swing=168h, invest=720h; `r_model` stop=-1/tp1=1/tp2=2/tp3=3; `outcome_model.ambiguous_same_candle=conservative`; **`partial_exit_model.enabled: false`** (0.4/0.4/0.2). No move-to-BE / trailing configured anywhere.
- **Sector cap** is hardcoded in `src/signals/portfolio_caps.py:27` (`_RANK_WEIGHT={1:1.0, 2:0.5}`, 3rd+→0). Not in YAML. Applies to stocks intraday A/B only. **Value not touched.**

### Live paths
- Paper-entry alert: `src/notifiers/paper_entry.py` `send_paper_entry_alert()` builds `payload` (23 keys incl. concentration_*), persists via `store.record_signal_alert(... payload=...)`, sends via `TelegramNotifier.send()`. Concentration uses **per-signal** `concentration_for_live_signal` (only concurrently-open peers → effectively inert; confirmed prior stage).
- Tracking cycle: `src/signals/tracker.py` `track_active_signals()` / `track_pending_entries()`; stocks `src/stocks/monitor.py StocksMonitorSession.run_once()`.

### OHLCV coverage (for PART 4)
- 1m bars exist but cover **only ~4h of today** (2026-06-17 ~11:54–16:05 UTC). **Not sufficient** for a 7–30d 1m path replay.
- 5m/15m/1h/4h/1d present across binance/bybit/mexc (≈150 symbols each). PART 4 will use **5m (fallback 15m)** with an explicit coverage %.

### Control Plane (trading-desk-control) — consumer
- Reads crypto-ai-desk DB **read-only** (`?mode=ro`) via `backend/app/desk_adapter.py`; parses `payload_json` permissively (`.get()`), TS `Signal` fields all optional. **Adding new payload keys is SAFE** (non-breaking). Live/auto-live lock in `backend/app/config.py` (`enable_live_commands=False`, `auto_live_locked=True`) and command queue in `commands.py` — **will not be touched**.

## What this stage will change (add-only)
- **New modules:** `src/risk/circuit_breaker.py`, `src/risk/risk_off.py`, `src/risk/risk_guards.py`, `src/signals/lifecycle.py`, `src/signals/sector_cap_shadow.py`, `src/catalysts/integrity.py`.
- **2 new read-only store methods** in `src/storage/sqlite.py`: `load_recent_terminal_outcomes(since_iso)`, `last_alert_by_type(alert_type)` (pure SELECT, no schema change).
- **Add-only payload wiring** in `src/notifiers/paper_entry.py` (fail-open) + one compact, deduped Telegram warning line.
- **New scripts:** `scripts/replay_profit_protection_path_aware.py` + diagnostic CLIs for the monitoring reports.
- **Control Plane (optional, safe):** extend `desk_adapter.py` pass-through dict + `frontend/src/types.ts` optional fields — read-only surfacing only.
- **New tests** per part; full suite at PART 8.

## What must NOT change (reaffirmed)
Live, auto-live, exchange execution, crypto scalp actionable, stocks scalp production, scoring, TP/SL, thresholds, sector-cap value, force-close, hard production block (without separate approval), historical outcomes, Control Plane safety/commands/locks.

## Commands used (baseline)
`python -m pytest tests/ -q`; read-only SQLite (`mode=ro`) introspection; OHLCV CSV header/range sampling. No writes to the trading DB in this baseline step.
