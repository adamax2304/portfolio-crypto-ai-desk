# Playbook-Aware Sizing — Implementation Report

**Date:** 2026-06-10 · **Scope:** Reporting / paper-PnL annotation layer only. **No** changes to signal generation, scoring, thresholds, TP/SL, entry/stop/TP, mode routing, Telegram alerts, or `proposed_signals` / `signal_outcomes` data.
**References:** [PROFITABILITY_LEVERS_AUDIT.md](PROFITABILITY_LEVERS_AUDIT.md) (Lever 1) · [PLAYBOOK_POSITION_SIZING_SIMULATION.md](PLAYBOOK_POSITION_SIZING_SIMULATION.md).

## 1. What was added

| File | Purpose |
|---|---|
| **`config/sizing_weights.yaml`** (new) | Per-playbook weight schedule with explicit tier overrides and fine `(playbook × tier × direction)` overrides. v1 schema (`version: 1`). |
| **`src/signals/sizing.py`** (new, ~180 lines) | Single source of truth. Exposes `size_decision(signal)` and `size_signals(list)` returning `(weight, playbook, reason, raw_r, sized_r)`. LRU-cached YAML load. |
| **`tests/test_sizing.py`** (new) | 19 tests pinning the cohort routing matrix + invariants. |
| `scripts/refresh_obsidian_dashboard.py` (touched) | Tab 10 `Performance by Mode` gains a "💰 Raw R vs Sized R" section with portfolio totals + by-playbook contribution + top positive/negative + sizing notes. Also: per_setup CTE now carries `news_supported`. |
| `scripts/write_obsidian_current_state_dashboard.py` (touched) | Tab 11 `## 8b. Playbook Performance Snapshot` gains a one-line **`Raw R total: X · sized total: Y`** annotation. |
| `src/analysis/packet.py` (touched) | New `_build_sizing_context_block()` wired into the crypto packet sections list (placed right after the playbook context block). |
| `src/stocks/llm_packet.py` (touched) | Same sizing block included in stocks packet. |

## 2. Routing matrix (cohort → weight)

| Cohort | Weight | Source |
|---|---:|---|
| `crypto_swing_narrative_rs_momentum` | 1.0× | playbook base |
| `crypto_intraday_catalyst_or_momentum` | 1.0× | playbook base |
| `crypto_failed_bounce_short` | 1.0× | playbook base |
| `crypto_rs_leader_long`, `crypto_catalyst_backed_setup` | 1.0× | playbook base |
| **`crypto_scalp_momentum_continuation`** | **0.5×** | playbook base (low-confidence) |
| `stocks_intraday_rth_momentum` B-tier | 1.0× | playbook base |
| `stocks_intraday_rth_momentum` shorts | 1.0× | playbook base |
| **`stocks_intraday_rth_momentum` A-tier long** | **0.5×** | fine override (overpromotion) |
| **`stocks_swing_watchlist_rs_rotation`** | **0×** | playbook base (paused) |
| **`stocks_invest_watchlist_30d_thesis`** | **0×** | playbook base (paused) |
| **C-tier / rejected (any playbook)** | **0×** | tier override |
| anything else | 1.0× | default |

Resolution order: fine override > tier override > playbook base > default. Configurable in YAML — no code change required to retune.

## 3. Live numbers after deploy

### Tab 10 `Performance by Mode` — portfolio totals (all-time, deduped)

| Metric | equal 1× (raw) | playbook-aware (sized) |
|---|---:|---:|
| **Total R** | **−73.4R** | **+34.5R** |
| n setups | 764 | 279 (sized > 0) |
| Wins (sized > 0) | — | 67 |
| Losses (sized < 0) | — | 89 |
| WR (sized closed) | — | 43% |
| PF (sized) | — | 1.53 |

The −107.9R swing matches the audit's projection (the small delta vs the audit's +33.6R comes from later-arriving closures since the audit ran).

### By-playbook contribution (top 3 positive, top 2 negative)

| Playbook | weights | n_sized | rawR | sizedR |
|---|---|---:|---:|---:|
| `stocks_intraday_rth_momentum` | 0.0×, 0.5×, 1.0× | 162 | +11.1 | **+22.8** |
| `crypto_swing_narrative_rs_momentum` | 1.0× | 18 | +11.0 | **+11.0** |
| `crypto_failed_bounce_short` | 1.0× | 21 | +10.0 | **+10.0** |
| `crypto_intraday_catalyst_or_momentum` | 1.0× | 20 | −5.0 | −5.0 |
| `crypto_scalp_momentum_continuation` | 0.5× | 58 | −8.5 | **−4.2** |
| `stocks_swing_watchlist_rs_rotation` | 0.0× | 0 | −49.0 | **+0.0** (paused) |
| `stocks_invest_watchlist_30d_thesis` | 0.0× | 0 | −43.0 | **+0.0** (paused) |

The two paused stocks playbooks contribute zero to the sized total — −92R of historical paper losses removed from the portfolio scoreboard without altering a single `signal_outcomes` row.

The `stocks_intraday_rth_momentum` row shows three weights (0.0× for C-tier, 0.5× for A-tier long, 1.0× for B-tier + shorts) honestly displayed via the new "weight(s)" column.

### Tab 11 `## 8b. Playbook Performance Snapshot` — 14d annotation line
```
_Raw R total: +20.0R · playbook-aware sized total: +86.5R
 (see [reports/PROFITABILITY_LEVERS_AUDIT.md]; weights: config/sizing_weights.yaml)._
```

## 4. Tests
**`tests/test_sizing.py` — 19 passed**:

| Group | Cases |
|---|---|
| Cohort routing | scalp / A-tier-long / B-tier intraday / shorts / stocks swing / stocks invest / C-tier / crypto swing / crypto intraday catalyst / crypto shorts |
| Math | raw_r echoed unchanged; sized_r = raw_r × weight; zero when paused; None when raw_r missing; explicit `raw_r` key accepted alongside `final_r` |
| Robustness | does not raise on empty dict; `size_signals` does not mutate input |
| Portfolio totals | watchlist / paused signals excluded from sized WR/PF; sum_raw_r preserved across all rows |
| Invariant | source has no `TelegramNotifier`, `SQLiteStore`, `register_ideas`, `upsert_proposed_signal`, or `scoring_agent` references |

**71 tests passing** in the focused regression subset (sizing + paper-execution + revalidation + playbook labels + expansion + dashboard winrate). No previous tests regressed.

## 5. What is explicitly NOT touched

| Surface | Status |
|---|---|
| `proposed_signals` table | untouched (no SQL UPDATE/INSERT from the sizing layer) |
| `signal_outcomes` table | untouched (raw_r preserved verbatim) |
| `final_r` column | untouched and STILL the source of truth for raw R |
| Scoring agents | untouched |
| Trade idea agent gates | untouched |
| Telegram alert path | untouched (`_format_idea_alert`, watchlist monitor unchanged) |
| Scheduler script | untouched |
| TP/SL geometry | untouched |
| Tier thresholds | untouched |

## 6. How to retune later (no code change)
- Edit `config/sizing_weights.yaml`:
  - Change a `playbooks:` weight to up/down-size a cohort.
  - Add a new entry under `fine_overrides:` to address a (playbook × tier × direction) cell specifically.
- The next call to `size_decision()` re-reads the YAML (LRU-cached per path string; cache invalidates per process restart). For dashboards: regenerate.

## 7. Files added / changed (recap)
**Added:** `config/sizing_weights.yaml`, `src/signals/sizing.py`, `tests/test_sizing.py`, `reports/PLAYBOOK_AWARE_SIZING_IMPLEMENTATION_REPORT.md` (this), `reports/POST_PLAYBOOK_AWARE_SIZING_VERIFICATION.md`.
**Changed:** `scripts/refresh_obsidian_dashboard.py`, `scripts/write_obsidian_current_state_dashboard.py`, `src/analysis/packet.py`, `src/stocks/llm_packet.py`.

## Verdict
```
PLAYBOOK_AWARE_SIZING_DEPLOYED
```

A new reporting-only layer is live across tabs 10 & 11 + both LLM packets. Portfolio sized totals match the audit's projection (raw −73R → sized +34R). Raw R is unchanged in the database; only the dashboard view of "what the portfolio would have done under sizing discipline" was added. 19 sizing tests + 52 focused regression tests pass.
