# Monitoring — 6h Shadow Sanity Check

**Date:** 2026-06-18 ~15:13 UTC · **Type:** post-~6h technical sanity (NOT profitability, NOT strategy). Read-only + dry-runs.

## 1. Overall verdict
**MONITORING_6H_MINOR_ISSUES** — every layer is correctly wired, healthy, and does NOT slow the monitor (p95 78ms, no network in alert path). Two **operational** (not code/trade-math) nuances to action: (a) the scheduler **loop is not currently running** (it ran 2 clean cycles then the session-launched background loop ended); (b) intelligence fields won't appear on **live** alerts until the monitor processes restart with the new code. Both are "restart the scheduler", not bugs.

## 2. Scheduler status
- Ran **2 clean cycles**: CYCLE 1 END `ok=19 failed=0 telegram=sent` (08:53→09:37 UTC), CYCLE 2 END `ok=19 failed=0 telegram=sent` (≈10:5x→12:29 UTC). No fatal errors, no duplicate steps.
- Dry-run plan = 24 steps, no duplicates, intelligence steps present + `command_nonfatal`, no LLM/live/execution steps.
- **Now (15:13 UTC): no `run_default_market_schedule` process alive** — the loop stopped after cycle 2 (~2.7h ago); no cycle 3. The 90-min monitors from cycle 2 have also expired. → restart via the permanent autostart.

## 3. Last successful cycle
Cycle 2, ended **2026-06-18 12:29 UTC** (15:29 local). Cycles in window: 2. Errors/warnings: none fatal.

## 4. New shadow layers status
All wired + exercised in the 2 cycles. `data/intelligence/intelligence.sqlite` present: timeline_events **594**, deriv_cache **31**, phase_cache **31**, phase_history **31**, onchain_cache **0** (no config — expected). Aggregator fail-open verified.

## 5. Intelligence cache freshness
Last computed **12:53 UTC** (cycle 2's `intelligence layer update`); timeline last event 12:50 UTC. Now 15:13 UTC → **~2.3h stale** — purely because no cycle 3 ran (scheduler stopped), not a module fault. Refreshes on the next cycle. On-chain status: `interface_ready_config_missing`.

## 6. Performance
Sample enrichment over 100 cached symbols: **p50 63ms · p95 78ms · p99 93ms · max 93ms** (target p95<100, p99<300 — met). No network calls inside the aggregator (socket-block test passes). Price-trajectory fields compute; funding/OI degrade to unknown (no history) — expected.

## 7. Telegram status
Latest live paper_entry alert `sig_1a248d97afa82812` (11:07 UTC): **Stop/SL line present**, freshness present, risk-guard diagnostic fields present, `diagnostic_only=true`, no spam/markdown crash. **Intelligence lines absent on this alert** — it was emitted by a monitor started at cycle 1 (~08:53 UTC) that loaded `paper_entry.py` BEFORE the intel block was added this session (stale in-memory module). A freshly-started monitor includes them (paper-entry integration test passes). → appears after restart.

## 8. Control Plane status
`backend/app/desk_adapter.py` + `actionability.py` compile. Read-only `.get()` pass-through incl. the new intelligence fields; TS `Signal` optional fields. `enable_live_commands=False`, `auto_live_locked=True` (unchanged). Absent fields don't crash.

## 9. Catalyst ASTER status
**CLEARED ✅** — fresh catalyst-scan (12:11 UTC) → `regression signature: none`. (Overall status still `warning` from the benign "unmapped high-importance" count, NOT ASTER — informational, leave for Friday.)

## 10. Circuit breaker dry-run
Works — today scope=1, `would_pause=False` (calm day). No Telegram sent in dry-run.

## 11. Shadow exit ledger
`shadow_exit_ledger_update` + `shadow_exit_summary` run; **146/146 covered (100%)**; summary written. (Verdict still PROFIT_PROTECTION_STILL_DISABLED — shadow only.)

## 12. OHLCV archive status
Append-only growth confirmed: +643 (5m) / +420 (15m) genuinely-new candles over the window (deduped by timestamp — not duplicates). Rolling cache untouched.

## 13. Errors / warnings
- No fatal scheduler errors; both cycles ok=19/0.
- yfinance 404s for some stock ETFs during the prior full-suite run = upstream data gaps + a concurrently-running scheduler; not a layer fault.
- The one failed test last run (`test_stocks_telegram_safe::test_dedup_unchanged_after_transport_fix`) = pre-existing flaky test (real shared DB + live yfinance disturbed by the concurrent scheduler), not in the intelligence path.

## 14. What to fix now
- **Restart the scheduler loop via the permanent autostart** (Windows Task / `.bat`) so cycle 3+ run and the monitors reload the intel-wired `paper_entry.py`. This is the only "now" item; it's operational, not code/trade-math.
- (Optional, tiny, non-trade-math) harden the flaky stocks-tg test to mock `_refresh_report` / use a temp DB — can wait.

## 15. Leave until Friday review
- Shadow-intelligence forward comparison (does squeeze_phase / no_chase / thesis-invalidation predict outcomes).
- The benign catalyst "unmapped high-importance" warning (14 symbols not mapped to catalyst_events).
- Shadow exit / profit-protection decision (still disabled).

## Trade-math lock verification (CHECK 5) — all unchanged ✅
live off · auto-live off · exchange execution off · crypto scalp actionable off · TP/SL unchanged · scoring unchanged · thresholds unchanged · BE/partial/trailing in real trade logic disabled · `partial_exit_model.enabled=false` · leverage execution off · no force-close · stocks-intraday C-tier shadow_review_only. **No critical lock changed.**
