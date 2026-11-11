# PRE — Shadow Intelligence Layer Baseline (PART 0)

**Date:** 2026-06-18 · **Type:** new shadow/diagnostic/add-only intelligence layer. **No trade-math / routing / live change.**

## Current state (from PROJECT_STATE.md + latest decisions)
- **Locked:** live/auto-live/exchange-exec, scoring, TP/SL, thresholds, sector-cap value, BE/partial/trailing in trade logic, hard breaker/throttle/cap, leverage exec, force-close, historical outcomes, Control Plane commands/locks.
- **Operational (alert-only/read-only):** circuit breaker, catalyst integrity, OHLCV archive+backfill, lifecycle review, sector-cap would-bind, position advisor, Telegram/Control-Plane risk fields.
- **Shadow-only:** shadow exit manager + profit-protection variants.
- **Tests:** 766 passed, 0 failed (latest).
- **Scheduler:** `run_default_market_schedule` (currently running) — steps incl. catalyst-scan → catalyst integrity → ohlcv archive → lifecycle review (all non-fatal).

## Data availability (what the new modules can actually use)
| Source | Status | Implication |
|---|---|---|
| OHLCV archive (5m/15m, 60d, 70 symbols) | ✅ deep | price slopes / distance-to-high / accel **work now** |
| proposed_signals (`funding_context`, `oi_context`, `sector`, `narrative` strings) | ✅ text only | weak/contextual funding-OI labels; no numeric history |
| Funding/OI numeric **history** | ❌ only `data/raw/funding/binance_futures_latest.json` (one snapshot, 0 CSV history) | derivatives **slopes/zscore mostly `unknown`** until accumulated forward via timeline snapshots |
| signal_alerts / signal_outcomes | ✅ | timeline bootstrap + outcome bias |
| news_items / catalyst layer | ✅ | catalyst freshness for phase/thesis |
| Token **contract addresses** | ❌ none found in config/src | on-chain layer = **interface + unknown mode** (no config) |
| GoPlus/honeypot API key/config | ❌ none | on-chain = `INTERFACE_READY_CONFIG_MISSING` |
| active universe | `config/universe.yaml`, `config/watchlist.yaml` | scope updates to active symbols |

## Where data will be stored
- `data/intelligence/intelligence.sqlite` — single new DB, tables: `timeline_events`, `deriv_cache`, `phase_cache`, `phase_history`, `onchain_cache`. **Never** touches `db/crypto_ai_desk.sqlite` (trading DB) or `data/raw/ohlcv` (rolling cache).

## Where fields will be wired
- `src/intelligence/intelligence_layer.assemble_intelligence_fields()` → add-only into the paper-entry `payload` (read **cached** summaries only, fail-open, budgeted) + ≤3 compact Telegram lines + Control-Plane read-only pass-through.
- Heavy compute (derivatives, squeeze, on-chain, timeline compaction) → **background scheduler scripts**, non-fatal.

## What will NOT be touched
TP/SL, scoring, thresholds, routing/actionability, size_weight, leverage, exits, hard filters, auto-short, risk-off throttle, hard breaker, force-close, historical outcomes, real tracker results, live/auto-live, Control Plane commands/locks.

## Performance risk assessment
- The alert path will only **read** the latest cached row per symbol from `intelligence.sqlite` (indexed by symbol) — O(1) lookups, no compute, no network. Target <100ms p95 / <300ms hard cap; partial+`timeout_partial` if exceeded.
- All external fetches (only on-chain, if ever configured) run in background scripts with TTL + timeout + rate-limit. **No network or LLM call in the alert/monitor path.**

## Rollback plan
- Remove the `assemble_intelligence_fields` block from `paper_entry.py` + the scheduler intelligence steps.
- Delete `src/intelligence/` + `data/intelligence/` + the new scripts/tests.
- Control Plane: revert the additive `.get()` keys + optional TS fields.
- Zero impact on trades (the layer never touched them).
