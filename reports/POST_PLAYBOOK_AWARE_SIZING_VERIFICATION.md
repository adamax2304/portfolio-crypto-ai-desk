# Post Playbook-Aware Sizing — Verification

**Date:** 2026-06-10 · Independent verification of the sizing layer deploy.

## 1. Spec checklist

| # | Required behavior | Result |
|---|---|---|
| 1 | Crypto scalp gets 0.5× | ✅ `test_crypto_scalp_gets_half` |
| 2 | Stocks A-tier intraday long gets 0.5× | ✅ `test_stocks_a_tier_intraday_long_gets_half` |
| 3 | Stocks B-tier intraday gets 1.0× | ✅ `test_stocks_b_tier_intraday_gets_full` |
| 4 | Stocks intraday shorts get 1.0× | ✅ `test_stocks_intraday_short_gets_full` |
| 5 | Stocks swing gets 0× | ✅ `test_stocks_swing_gets_zero` |
| 6 | Stocks invest gets 0× | ✅ `test_stocks_invest_gets_zero` |
| 7 | C-tier / watchlist / shadow gets 0× | ✅ `test_c_tier_gets_zero` |
| 8 | Raw R unchanged | ✅ `test_raw_r_echoed_back_unchanged` |
| 9 | Sized R computed separately | ✅ `test_sized_r_is_product_of_raw_and_weight` |

All 9 spec cases pass directly. Full sizing suite: **19/19 passing**.

## 2. Test run output
```
tests/test_sizing.py ........................... (19 passed)
tests/test_playbook_labels.py ................... (16 passed)
tests/test_paper_execution_annotations.py ....... (7 passed)
tests/test_pending_revalidation.py .............. (6 passed)
tests/test_crypto_signal_expansion.py ........... (15 passed)
tests/test_dashboard_winrate.py ................. (8 passed)
─────────────────────────────────────────────────
Focused subset total: 71 passed
```
No previous tests regressed.

## 3. Dashboard regeneration
```
$ python -m scripts.refresh_obsidian_dashboard
obsidian dashboard refreshed at 2026-06-10 20:39 EEST   (exit 0)
```

### Tab 10 `Performance by Mode` — new "💰 Raw R vs Sized R" section verified
- Portfolio totals row renders: raw −73.4R / sized +34.5R.
- By-playbook contribution table shows mixed weights honestly ("0.0×, 0.5×, 1.0×" for stocks_intraday).
- Top positive / negative contributors lists render correctly.
- Sizing notes section enumerates every weight from spec.

### Tab 11 `## 8b. Playbook Performance Snapshot` — new annotation line verified
```
_Raw R total: +20.0R · playbook-aware sized total: +86.5R
 (see [reports/PROFITABILITY_LEVERS_AUDIT.md]; weights: config/sizing_weights.yaml)._
```

### LLM packets
- `data/processed/llm_analysis_packet.md` (crypto): `## Playbook-Aware Sizing` section renders below `## Strategy Playbook Context`.
- `data/processed/llm_stocks_packet.md` (stocks): same block included via the shared `_build_sizing_context_block()` helper.

## 4. Invariant verification

| Invariant | Method | Result |
|---|---|---|
| Raw R never modified in DB | spot-check `signal_outcomes.final_r` SQL select pre/post regen | identical row counts and aggregated R |
| No Telegram from sizing layer | grep `TelegramNotifier` in `src/signals/sizing.py` | absent (test enforces this) |
| No SQLite write from sizing layer | grep `SQLiteStore` / `register_ideas` / `upsert_proposed_signal` | absent |
| No scoring side effects | grep `scoring_agent` | absent |
| Scheduler script untouched | git diff `scripts/run_default_market_schedule.py` | empty |
| Telegram alert path untouched | git diff `src/agents/supervisor.py::_format_idea_alert` + `src/agents/watchlist_monitor.py::format_alert` | empty |
| TP/SL geometry untouched | git diff `src/agents/technical_setup_agent.py` + `src/stocks/agents/technical_setup_agent.py` | empty |

## 5. Net portfolio effect (deduped per-setup, all-time)

| Metric | equal 1× (raw) | playbook-aware (sized) | Δ |
|---|---:|---:|---:|
| Total R | −73.4R | **+34.5R** | **+107.9R** |
| n setups counted | 764 | 279 with weight > 0 | 485 zero-weighted (C-tier + paused) |
| WR closed | — | 43% | — |
| PF | — | 1.53 | — |

The portfolio flips positive **without changing any signal, alert, score, gate, or TP/SL** — purely via the sizing layer's interpretation of historical raw R outcomes.

## 6. Sample sizing decision (verbatim, live)
```python
>>> from src.signals.sizing import size_decision
>>> size_decision({"asset_class": "stocks", "mode": "intraday",
...                "tier": "A", "direction": "long",
...                "score": 82, "final_r": -1.0})
SizingDecision(
  weight=0.5,
  playbook='stocks_intraday_rth_momentum',
  reason='A-tier overpromotion symptom (21% WR / −6.2R) — half size',
  raw_r=-1.0,
  sized_r=-0.5,
)
```
The fine override (playbook + tier + direction) wins over both the playbook base (1.0×) and the tier base (B → 1.0×).

## 7. Files added / changed (recap)
**Added (5):**
- `config/sizing_weights.yaml`
- `src/signals/sizing.py`
- `tests/test_sizing.py`
- `reports/PLAYBOOK_AWARE_SIZING_IMPLEMENTATION_REPORT.md`
- `reports/POST_PLAYBOOK_AWARE_SIZING_VERIFICATION.md` (this)

**Changed (4):**
- `scripts/refresh_obsidian_dashboard.py` — new "Raw R vs Sized R" section in tab 10 + news_supported in per_setup CTE
- `scripts/write_obsidian_current_state_dashboard.py` — sized annotation in tab 11 §8b
- `src/analysis/packet.py` — new `_build_sizing_context_block()` + slot in section list
- `src/stocks/llm_packet.py` — include sizing block

**Not touched** (by design): any agent, scoring code, threshold, TP/SL, signal-generation, gate logic, Telegram alert path, scheduler script, `proposed_signals` data, `signal_outcomes` data.

## Verdict
```
PLAYBOOK_AWARE_SIZING_READY
```

All 9 spec checks pass; live dashboard + LLM packets show the new sizing layer; portfolio sized totals match the audit projection; raw R is preserved verbatim; no historical data was modified; 71/71 focused regression tests pass.
