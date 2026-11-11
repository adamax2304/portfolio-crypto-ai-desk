# Backtest Engine — Implementation Report (PART 10a)

**Date:** 2026-06-11 · **Scope:** Level A signal execution replay engine + 6 follow-up studies. Read-only.

---

## 1. What was added

### New scripts (all under `scripts/`)
| File | Purpose |
|---|---|
| `scripts/replay_signal_execution.py` | Core Level A engine. Loads proposed_signals, locates candle files, simulates entry/TP/stop with no look-ahead, applies fees+slippage, computes raw R and sized R. Outputs CSV + summary MD. CLI flags per spec: `--asset-class`, `--since`, `--mode`, `--playbook`, `--timeframe-preference`, `--use-1m-if-available`, `--conservative-intrabar-policy`, `--include-fees`, `--include-slippage`, `--output-prefix`. |
| `scripts/replay_crypto_scalp_1m_exits.py` | PART 4. Tests 6 exit policies (A=current, B=TP1@0.5R, C=partial, D=TP1@0.7R, E=BE after 0.6R, F=4h expiry) against existing scalp signals. Counterfactual only. |
| `scripts/replay_sizing_walk_forward.py` | PART 5. Tests 4 sizing configs (equal-1×, current YAML, conservative, aggressive) on a 60/30/10 temporal split. Validation+forward reported OOS. |
| `scripts/replay_stocks_a_tier_rth.py` | PART 6. Stocks A-tier intraday-long RTH-open behaviour: by-window, cluster vs rest, half-size simulation, would-a-gate-have-helped. Read-only. |
| `scripts/replay_expansion_watchlist.py` | PART 7. C-tier follow-through: promotion rate, direction correctness, missed winners. |

### New reports (all under `reports/`)
| File | Description |
|---|---|
| `BACKTEST_FEASIBILITY_AUDIT.md` | PART 1 — data coverage audit; Level A/B/C feasibility verdicts. |
| `BACKTEST_METHODOLOGY_SPEC.md` | PART 2 — three replay levels defined with execution rules. |
| `SIGNAL_EXECUTION_REPLAY_RESULTS.csv` + `SIGNAL_EXECUTION_REPLAY_SUMMARY.md` | PART 3 — full Level A replay output (all 1,470 signals). |
| `SIGNAL_EXECUTION_REPLAY_14D_RESULTS.csv` + `SIGNAL_EXECUTION_REPLAY_14D_SUMMARY.md` | PART 10 — 14-day verification run (980 signals). |
| `CRYPTO_SCALP_1M_EXIT_REPLAY.md` | PART 4 output. |
| `PLAYBOOK_SIZING_WALK_FORWARD_BACKTEST.md` | PART 5 output. |
| `STOCKS_A_TIER_RTH_OPEN_REPLAY.md` | PART 6 output. |
| `EXPANSION_WATCHLIST_BACKTEST.md` | PART 7 output. |
| `BACKTEST_EXECUTION_COST_MODEL.md` | PART 8 — fees/slippage/liquidity assumptions. |
| `LIVE_READINESS_FROM_BACKTEST.md` | PART 9 — verdict + allowed/forbidden playbooks + risk envelope. |
| `BACKTEST_ENGINE_IMPLEMENTATION_REPORT.md` | This file. |
| `POST_BACKTEST_REPLAY_VERIFICATION.md` | PART 10 verification checklist. |

---

## 2. Engine design

### No-lookahead invariant
- Candles strictly after `created_at` are used. The candle that produced the idea is **not** treated as a fill candle even if it shows the entry zone touched.
- TP/stop only adjudicated after the entry candle.
- Same-candle TP+stop events are flagged `ambiguous=True` and resolved by the conservative policy (stop counts first).

### Entry-fill model
- `zone` entries fill when price first touches the zone post-creation (long → low touches zone-low; short → high touches zone-high).
- `trigger` entries fill when price crosses the trigger.
- Pre-entry invalidation: if price moves through `invalidation` BEFORE entry, mark `entry_moved_away`.
- Stale: if `validity_window_hours` elapses with no fill, mark `stale_before_entry`.

### Coverage labels
- `high` — candle window fully covers `[created_at .. expiry]` AND timeframe is 15m or finer.
- `medium` — candle window covers part of the window, OR timeframe is 1h/1d.
- `low` — no candle file found; fallback to recorded `final_r` from `signal_outcomes` (marked).

### Fees & slippage
See [BACKTEST_EXECUTION_COST_MODEL.md](BACKTEST_EXECUTION_COST_MODEL.md). Crypto: 10 bps round-trip + 5 bps slip + 10 bps thin-penalty (MEXC/low-confidence). Stocks: $0.02 per share.

### Sizing
Uses `src.signals.sizing.size_decision()` with `config/sizing_weights.yaml`. No code-path duplication; same logic that powers the production dashboard.

---

## 3. Headline replay numbers

### All-time (1,470 signals, fees+slippage on)
| Metric | Value |
|---|---:|
| Raw R sum | **+161.34** |
| Sized R sum (playbook-aware) | **+215.95** |
| Fees/slippage adjustment | −6.73 |
| Wins / Losses | 535 / 481 |
| WR (closed) | 52.7% |
| PF | 1.51 |
| Same-bar ambiguous | 0 (0.0%) |
| Coverage: high / medium / low | 1219 / 251 / 0 |

### 14-day (980 signals, fees+slippage on)
| Metric | Value |
|---|---:|
| Raw R sum | **+33.94** |
| Sized R sum | **+103.28** |
| Fees | −4.10 |
| WR | 45.1% |
| PF | 1.14 |

### Cross-check vs production tracker
- Mean |ΔR| (replay vs tracker) = **0.428 R** over 1,425 compared signals on all-time, **0.18 R** when restricted to `coverage_quality == 'high'`.
- The divergence is concentrated in 1h-timeframe crypto signals where intrabar adjudication differs.

---

## 4. What is explicitly NOT touched

| Surface | Status |
|---|---|
| `proposed_signals` | untouched (replay reads only) |
| `signal_outcomes` | untouched (replay reads only) |
| `signal_alerts` | untouched |
| `watchlist_alerts` | untouched |
| `final_r` column | untouched and still source of truth for raw R |
| Scoring agents | untouched |
| TP/SL geometry | untouched (replay tests counterfactual policies; production keeps current) |
| Telegram alert path | untouched |
| Scheduler script | untouched (no scheduler change needed) |
| `config/sizing_weights.yaml` | untouched (used as-is) |
| Production DB writes | NONE from any replay script |

---

## 5. What's not implemented (and why)

| Capability | Status | Reason |
|---|---|---|
| Level B point-in-time replay | not implemented | derivatives + regime snapshots missing; see [BACKTEST_METHODOLOGY_SPEC.md](BACKTEST_METHODOLOGY_SPEC.md) §B |
| Level C full strategy replay | not implemented | OHLCV/news/derivatives historical archives too thin |
| 1m crypto scalp evidence-strong study | counterfactual only | 1m archive is rolling ~4h |
| Long-horizon walk-forward | not yet meaningful | 20 days of history |
| Per-symbol spread proxy for crypto | not implemented | additional feature; not required for current verdict |

---

## 6. How to re-run

```bash
# Full replay with fees + slippage
python scripts/replay_signal_execution.py --asset-class all --include-fees --include-slippage

# 14-day verification window
python scripts/replay_signal_execution.py --asset-class all --since 2026-05-28 \
       --include-fees --include-slippage --output-prefix SIGNAL_EXECUTION_REPLAY_14D

# Crypto scalp counterfactual
python scripts/replay_crypto_scalp_1m_exits.py

# Sizing walk-forward
python scripts/replay_sizing_walk_forward.py

# Stocks A-tier RTH
python scripts/replay_stocks_a_tier_rth.py

# Expansion watchlist
python scripts/replay_expansion_watchlist.py
```

All scripts are idempotent (writes overwrite, no DB writes). Safe to schedule weekly.

---

## 7. Runtime

| Script | Runtime |
|---|---|
| `replay_signal_execution.py` (1,470 signals) | ~25 s |
| 14-day subset (980 signals) | ~17 s |
| Other 4 scripts | < 5 s each |

Acceptable for weekly scheduling. No external API calls; only local CSV + SQLite.
