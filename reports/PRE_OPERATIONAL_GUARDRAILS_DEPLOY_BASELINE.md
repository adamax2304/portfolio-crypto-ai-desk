# PRE — Operational Guardrails Deploy Baseline (PART 0)

**Date:** 2026-06-17 · **Stage:** wire already-built alert-only/shadow/diagnostic modules into the daily scheduler + add OHLCV archival + a label-only leverage advisor + a stocks-intraday diagnostic. **No trade-math change.**

## What already exists (verified)
| Item | State |
|---|---|
| `src/risk/circuit_breaker.py` | present (alert-only would-pause) |
| `src/risk/risk_guards.py` | present (assembler; called from `paper_entry.send_paper_entry_alert`) |
| `src/risk/risk_off.py`, `src/signals/lifecycle.py`, `src/signals/sector_cap_shadow.py`, `src/catalysts/integrity.py` | present |
| `scripts/catalyst_integrity_scan.py`, `scripts/replay_profit_protection_path_aware.py` | present |
| Control Plane adapter `backend/app/desk_adapter.py` | compiles; reads payload via `.get()` (read-only pass-through) |
| `config/signal_tracking.yaml` → `partial_exit_model.enabled` | **false** (unchanged) |
| Live / auto-live / crypto-scalp-actionable / stocks-scalp-production | **off / locked** (`enable_live_commands=False`, `auto_live_locked=True` in Control Plane) |
| Last full suite | 729 passed, 0 failed |
| Version control | crypto-ai-desk is **not** a git repo (file-based project) — changes tracked via reports + tests |

## Scheduler / monitor wiring (discovered)
- Daily loop: `scripts/run_default_market_schedule.py` — `build_cycle_steps()` composes a 2h cycle: track-signals → crypto scalp/intraday reports → **catalyst-scan** → stocks intraday report → monitors → support tail (active-signals, signal-stats, detector, track-signals post, review, dashboard).
- Catalyst builder: `catalyst-scan` CLI → `src/catalysts/collector.collect_catalysts` → writes `data/catalysts/<date>/{catalyst_events,narrative_baskets}.jsonl`.
- Per-signal alerts: `src/notifiers/paper_entry.send_paper_entry_alert` (already calls the risk-guard assembler) via the crypto monitor (`monitor-watchlist`) + stocks monitor (`stocks-monitor-session`).
- OHLCV: `FileStore.save_ohlcv` writes a rolling ~220-candle CSV under `data/raw/ohlcv/{ex}/{tf}/`; limits in `config/settings.yaml`.
- System Telegram: scheduler end-of-cycle summary via `send_telegram()`; per-signal via `TelegramNotifier.send`.

## What will be connected (this stage)
1. **catalyst integrity scan** step right after `catalyst-scan` (non-fatal).
2. **OHLCV archive** step (append-only 5m/15m) after the reports (non-fatal).
3. **open intraday lifecycle review** step in the support tail (non-fatal).
4. New read-only scripts: `archive_ohlcv_history.py`, `circuit_breaker_dry_run.py`, `sector_cap_forward_tracker.py`, `stocks_intraday_diagnostic.py`, `open_intraday_lifecycle_review.py`.
5. New module `src/risk/position_advisor.py` (label-only) wired into the risk-guard payload.
6. Control Plane: the read-only pass-through already added; a display plan (no frontend break).

## What will NOT change
Live, auto-live, exchange execution, scalp enablement, scoring, TP/SL, thresholds, sector-cap value, BE/partial/trailing in trade logic, stop/TP widths, hard breaker, hard throttle, hard cap, force-close, history, Control Plane safety/commands/locks.

## Risk of change
Low. All additions are non-fatal scheduler steps (a failure logs and continues), read-only scripts, add-only payload fields, and a pure label module. None touches the order/sizing/scoring path. The OHLCV archive writes to a **separate** `data/archive/ohlcv` tree and only reads the rolling cache.

## Rollback plan
- Remove the 3 appended scheduler steps (`catalyst_integrity_step`, `ohlcv_archive_step`, lifecycle-review tail entry).
- Delete the new scripts + `src/risk/position_advisor.py`; revert the advisor block in `risk_guards.py`.
- The `data/archive/ohlcv` tree can be deleted with zero impact on trading (the rolling cache is untouched).
- Control Plane: revert the additive `.get()` keys in `desk_adapter.py` + the optional TS fields.

## Commands used
`pytest tests/ -q`; scheduler `--run-once --dry-run`; the new scripts run read-only/dry-run; read-only SQLite (`mode=ro`).
