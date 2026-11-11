# Daily Commands

The core CLI surface you'll use most days. All commands run from the project root `C:\Users\adama\Documents\crypto-ai-desk\` with the venv active.

## Refresh data

```powershell
python -m src.cli update-data
```

Fetches OHLCV (Binance + Bybit + MEXC), derivatives (Binance futures + Bybit/OKX snapshots + Bybit history), RSS news, social, loads manual events.

## Generate report

```powershell
# default daily (intraday-style)
python -m src.cli daily-report

# auto-universe (Stage 1 + Stage 2 funnel before deep analysis)
python -m src.cli daily-report --auto-universe --mode intraday

# explicit modes
python -m src.cli intraday-report --auto-universe
python -m src.cli scalp-report --auto-universe
python -m src.cli swing-report --auto-universe

# discovery (wider scan, lower volume floor)
python -m src.cli intraday-report --auto-universe --discovery
```

Output paths:

```
data/reports/daily/YYYY-MM-DD_daily_report.md
data/reports/intraday/YYYY-MM-DD_HH-MM_intraday_report.md
data/reports/scalp/YYYY-MM-DD_HH-MM_scalp_report.md
data/reports/swing/YYYY-MM-DD_HH-MM_swing_report.md
data/processed/context_for_llm.md
```

## Check latest report

```powershell
python -m src.cli latest --kind intraday --show
python -m src.cli latest --kind scalp
python -m src.cli latest --kind reviews
```

## Status / Doctor

```powershell
python -m src.cli status
python -m src.cli doctor
python -m src.cli exchange-status
```

## Watchlist monitor

```powershell
# run forever, 10-min cadence
python -m src.cli monitor-watchlist --interval 600

# single tick (good for cron / scheduled runs)
python -m src.cli monitor-watchlist --interval 600 --iterations 1

# dry run (don't send Telegram)
python -m src.cli monitor-watchlist --interval 600 --iterations 1 --dry-run
```

## Paper read-model refreshes (PAPER-ONLY, add-only)

These enrich entry-triggered signals into additive tables consumed by the Control-Plane
lifecycle / Mini App. They **never** touch `proposed_signals.tp*/entry*/direction` or
`signal_outcomes.final_r`, never place orders, never change scoring/routing. The default
schedule (`run_default_market_schedule.py`) runs them each 2-hour cycle; run manually with:

```powershell
python -m src.cli paper-execution-refresh    # Model-F paper_execution_r → paper_execution_outcomes
python -m src.cli paper-tp-refresh            # PART 3 structural TP   → signal_paper_tp
python -m src.cli paper-stop-refresh          # PART 8 structural stop → signal_stop_plan
python -m src.cli entry-mode-refresh          # PART 4 entry modes     → signal_entry_mode
python -m src.cli stock-direction-refresh     # PART 5 multi-factor dir → stock_direction_score
python -m src.cli entry-latency-audit         # PART 6 latency cause    → entry_latency_audit
```

Each prints a one-line summary (e.g. `structural_used=790`, `non_pullback=610`,
`multi_factor=400`, `data_gap_late=273`). Labels surface in the Mini App trade detail as badges
(`TP: STRUCTURAL`, `entry: …`, `dir: …`, `stop: structural`, `entry latency: …`).

## Paper-shadow A/B execution lane (NEXT STEP — measurement only)

Runs A (old paper logic) vs B (new logic: entry modes + structural TP/stop + multi-factor stock
direction + maker-first) over the SAME signals/OHLCV/fees, splitting **historical_backfill**
(look-ahead — NOT proof) from **forward_since_activation** (the only valid evidence). Lives on the
Mini App **System** tab → *Paper Shadow A/B*. Never places orders / mutates final_r / no live.

```powershell
python -m src.cli paper-shadow-execution-refresh --lookback-hours 336        # cycle refresh
python -m src.cli paper-shadow-execution-refresh --rebuild                    # full recompute
python -m src.cli paper-shadow-execution-refresh --signal-id sig_xxx          # single signal
python -m src.cli paper-shadow-execution-refresh --fee-profile conservative_taker
```

**Promotion gate:** decide only on the FORWARD window after ~2–4 weeks — promote the new logic into
the production fill path ONLY if forward B net R > A net R **after real fees**, drawdown not worse,
and with explicit operator sign-off. The backfill number is a hypothesis, never the decision.

Operational monitoring (read-only):

```python
from src.execution.paper_shadow_monitor import forward_quality, promotion_gate
forward_quality()   # forward A/B net R/$, warnings (sample<60, window<14d, DATA_GAP, fee-fragile)
promotion_gate()    # evaluates 5 criteria → READY/NOT_READY; executed=False (never auto-promotes)
from src.notifiers.paper_shadow_telegram import compose, send_daily
print(compose())            # daily A/B summary text (forward-only valid, look-ahead caveat)
send_daily(dry_run=True)    # compose without sending; dry_run=False sends via the notifier
```

App: Mini App **System** tab → *Paper Shadow A/B* (forward vs backfill A/B + promotion-gate verdict).
Risk tab is reconciled to the ledger profile: **$5000 / 0.5% / max 5x / bybit_non_vip_usdt_perp**.

Operational hardening:

```powershell
python -m src.cli stock-intraday-coverage-report           # DATA_OK/PARTIAL/DATA_GAP_LATE/NO_DATA
python -m src.cli stock-intraday-ohlcv-backfill --symbols MSTR,TSLA --lookback-days 60 --interval 15m
```

* **Maker fill realism** — the shadow engine tracks maker_entry_posted/filled/missed, taker_fallback,
  maker_tp_fills (LIMIT_THEN_TAKER_TIMEOUT falls back to taker after 8 bars). Fill-rate shown in the
  A/B panel; the gate warns if maker fill-rate < 50%.
* **Keeper build-id drift** — `app_keeper.ps1` restarts the stack (via launch_robust.ps1) when the
  served `ui_build_id` ≠ on-disk `dist/build_info.json` build_id, logging
  `scripts/keeper_last_restart.json {reason: build_id_drift}` (shown on the System tab).
* **DATA_GAP_LATE** trades are excluded from A/B edge stats (forward monitor + entry_latency_audit).

Safe observability + DB hygiene (2026-06-26) — observability/diagnostics, no scoring/actionability/threshold/final_r change:

```powershell
python -m src.cli paper-shadow-digest-send --dry-run        # compose daily A/B digest (--no-dry-run to send; scheduler runs it once/day)
python -m src.cli catalyst-linkage-shadow-audit --days 7    # DIAGNOSTIC coverage @ ~5h/24h/48h → catalyst_shadow_audit (not fed to scoring)
python -m src.cli signal-outcomes-retention --dry-run       # plan per-bar retention (--no-dry-run --days 14 --archive [--vacuum])
```

* **Per-mode A/B breakdown** — Mini App System → Paper Shadow A/B → *By mode* (forward-emphasized; backfill behind a labelled toggle). API `/api/paper-shadow/breakdown`.
* **A-tier diagnostic** — `from src.diagnostics.a_tier_strictness import analyze` (A correctly rare ~3.78%; caps gate it; threshold unchanged).
* **Stocks-mode readiness** — `from src.diagnostics.stocks_mode_readiness import analyze` (swing best paper-shadow candidate; scalp/invest research-only; **modes stay non-actionable unless separately approved**).

## Telegram setup / test

```powershell
python -m src.cli telegram-setup     # detect chat_id after /start
python -m src.cli telegram-test -m "hello"
```

## Review

```powershell
python -m src.cli review
```

Writes `data/reports/reviews/YYYY-MM-DD_HH-MM_review.md`.

## Natural-language ask

```powershell
python -m src.cli ask "Analyze the market today and give me the best trade ideas"
python -m src.cli ask "Update the data and check if morning ideas are still valid"
python -m src.cli ask "Find where money and attention are flowing today"
python -m src.cli ask "Review today ideas and tell me what worked and failed"
```

## PowerShell shortcuts

```powershell
.\scripts\daily.ps1
.\scripts\intraday.ps1
.\scripts\review.ps1
.\scripts\latest.ps1
.\scripts\quick_check.ps1
.\scripts\open_latest_daily.ps1
```

## Related

- [[Update_Universe]]
- [[Scalp_Commands]]
- [[Intraday_Commands]]
- [[Swing_Commands]]
- [[Long_Term_Commands]]
- [[Candidate_Debug]]
- [[Telegram_Commands]]
- [[Obsidian_Export_Commands]]
- [[How_to_use_daily]]

## Implemented status

- **Implemented**.
