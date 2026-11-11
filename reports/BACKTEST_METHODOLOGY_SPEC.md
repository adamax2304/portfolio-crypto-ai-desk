# Backtest Methodology — Replay Levels

**Date:** 2026-06-11 · **Companion to:** [BACKTEST_FEASIBILITY_AUDIT.md](BACKTEST_FEASIBILITY_AUDIT.md).

This spec defines the three replay levels, their inputs/outputs, their lookahead-avoidance rules, and which one is implemented in this pass.

---

## Level A — Signal Execution Replay (IMPLEMENTED IN THIS PASS)

**Goal:** Given the historical signals our system already proposed, replay how entry / TP / stop would have executed against the actual candle tape, and compute raw R and playbook-aware sized R.

### Inputs
| Source | Use |
|---|---|
| `proposed_signals` row | direction, mode, tier, entry zone, stop, TP1/2/3, created_at, validity window |
| `signal_outcomes` (last per signal) | for cross-check only — never used as input to the replay decision |
| `raw_idea_json` | for direction sanity check, playbook label derivation, pending revalidation rules |
| OHLCV CSV | candle tape from `created_at` to outcome or now |
| `config/sizing_weights.yaml` | per-cohort weight for sized R |

### Execution rules
1. **No look-ahead.** Process candles strictly forward from `created_at`.
2. **Entry must come first.** No TP/stop touch counts before entry is filled.
3. **Entry fill model:**
   - `entry_type=zone` (entry_low/entry_high): filled when price enters the zone after `created_at` (limit-like behavior for longs: low touched; for shorts: high touched).
   - `entry_type=trigger`: filled when price closes past `entry_trigger` (breakout) or touches it (retest), determined by `setup_type`.
   - If `created_at` candle already has price inside the zone, entry is filled on the **next** candle (no look-ahead from same candle that produced the idea).
4. **Pending revalidation:**
   - If price drifts > 2 ATR from entry before fill → mark `stale_before_entry`, no fill.
   - If price moves past the **invalidation** level before entry → mark `entry_moved_away`, no fill.
   - These mirror the production rules in `src.signals.pending_revalidation`.
5. **Post-entry adjudication:**
   - Walk candles from entry+1.
   - On each candle, check stop first **if conservative-intrabar-policy** (default), else check TPs first.
   - If TP and stop appear in same candle: drop to the finest available timeframe (1m → 5m → 15m → 1h). If still same-candle, mark **ambiguous** with `_ambiguous=True` flag, and apply policy:
     - conservative → adverse event counts first (stop hit) → loss of −1R
     - aggressive → favorable event (TP1) counts → +1R
6. **Expiry:** if validity_window_hours elapses without TP1 or stop, status = `expired`, R = 0 (or running MFE/MAE if open).
7. **Fees & slippage** (when `--include-fees` / `--include-slippage`):
   - Crypto: maker 0.02% per side default, taker 0.05%; ±1 tick slippage on entry; 0.05% slippage on TP/stop. MEXC and any symbol with `data_confidence=low` adds extra 0.10%.
   - Stocks: $0 commission, ±1 cent slippage on entry/exit at 15m granularity; gap fills marked as **lower-confidence**.

### Outputs (per signal, one CSV row + summary MD)
- `signal_id, asset_class, symbol, playbook, mode, direction, tier, score, created_at`
- `entry, stop, tp1, tp2, tp3`
- `original_outcome, original_final_r`
- `replay_outcome, replay_raw_r, replay_sized_r, size_weight`
- `fees_slippage_r_adjustment, candle_timeframe_used, data_coverage_quality, ambiguous, notes`

### Confidence label
- `high` — stocks signals OR crypto signals where 15m/1h candle window fully spans `[created_at .. closed_at]`.
- `medium` — crypto signals where only 1h candles are available, or where same-candle ambiguity rate > 0.
- `low` — signals where candle window does not cover the full lifetime → replay falls back to original tracker outcome with a marker.

---

## Level B — Point-in-Time Signal Replay (NOT IMPLEMENTED — FEASIBILITY ONLY)

**Goal:** Given archived reports / candidate snapshots, reconstruct what the system **knew** at each cycle, and verify that signal generation is reproducible.

### Required inputs (must be **frozen** at cycle time)
- regime / sector / narrative snapshots (currently latest-cache only — **gap**)
- catalyst event JSONL day-scoped (available 2026-06-01+ — partial)
- news_items with `published_at` (available — ✅)
- OHLCV historical archive ≥ 30 days at the timeframes the agents query (currently 1h for ~9d only — partial)
- funding/OI snapshots at cycle time (latest-cache only — **gap**)

### Decision
Feasibility is **PARTIAL**:
- Stocks: enough archives to attempt Level B for 2026-06-01 → 2026-06-10 only.
- Crypto: derivative gap blocks full reproduction. Could replay scoring **without** derivatives weight.

### Why not implemented now
1. Two source-of-truth fields (funding, OI) are not snapshotted; any Level B result would have a structural confound.
2. Building Level B before the snapshotting layer exists would yield false-positive "system is reproducible" results.
3. Audit-trail discipline first: start snapshotting context blobs in production cycles, then run Level B after ≥ 7 days of clean snapshots.

---

## Level C — Full Strategy Replay (NOT IMPLEMENTED — NOT FEASIBLE NOW)

**Goal:** Rerun the scanner / scoring / trade-idea agents over a historical period and check whether the same signals would emerge.

### Required inputs (none of which currently exist as a continuous archive)
- 1m and 5m crypto OHLCV for all symbols ever scanned, ≥ 30 days continuous
- 1m and 5m stocks OHLCV during RTH, ≥ 30 days continuous
- Historical funding rate every 8h for every venue ever queried
- Historical OI every cycle
- Historical news+catalyst with `received_at` (not just `published_at`) so we can avoid look-ahead from publisher-side back-dating
- Historical narrative/regime computations (or deterministic re-derivation thereof)
- Frozen scoring weights, frozen YAML configs at each historical cycle

### Decision
**Not feasible** before a multi-week data-collection campaign. Even if data were collected starting today, we'd need ≥ 4-6 weeks before Level C results could be statistically meaningful.

### What would make Level C feasible
1. Switch all data collectors from "rolling 220 candles" to "append-only archive".
2. Begin snapshotting derivatives (funding, OI) every cycle, indexed by timestamp.
3. Snapshot full LLM packets per cycle (already mostly done — just stop overwriting).
4. Tag every YAML config with a commit-hash so we can replay against the exact rule set in force at cycle time.

---

## Decision for this pass

| Level | Status |
|---|---|
| A | ✅ implement — `scripts/replay_signal_execution.py` |
| B | 🟡 document only — feasibility partial, blocked by missing snapshots |
| C | ❌ document only — not feasible until data archive grows |

All Level A outputs go to `reports/SIGNAL_EXECUTION_REPLAY_*` files and `reports/CRYPTO_SCALP_1M_EXIT_REPLAY.md` / `reports/STOCKS_A_TIER_RTH_OPEN_REPLAY.md` / `reports/EXPANSION_WATCHLIST_BACKTEST.md` / `reports/PLAYBOOK_SIZING_WALK_FORWARD_BACKTEST.md` / `reports/BACKTEST_EXECUTION_COST_MODEL.md`. **Nothing is written back to `proposed_signals` / `signal_outcomes` / `signal_alerts` / `watchlist_alerts`.**
