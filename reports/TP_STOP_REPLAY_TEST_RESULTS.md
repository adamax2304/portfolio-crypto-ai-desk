# TP/Stop Replay — Tests & Validation (PART 10)

**Date:** 2026-06-23.

## Replay correctness (internal consistency)
- **Reconstruction vs production:** `m_prod_best` (reconstructed best-TP-touched R) matches recorded `final_r` on **1401/1404 (99.8%)**. The **3** mismatches are exactly the **3 same-candle-ambiguous** trades (production conservatively books stop-first −1R; the reconstruction sees the TP touched). Expected, bounded, documented — does not affect any aggregate materially.
- **Same-candle handling:** ambiguous flag = 3 trades, inherited stop-first conservative from production. Not decisive for any conclusion.
- **Exit-model monotonicity:** net R hold→TP1 (−259.8) ≥ hold→TP2 (−341.3) ≥ hold→TP3 (−403.1) — correct (a nearer single target gives back less). Validates the hold-model logic.
- **Dedup/economic-trade consistency:** rows == unique economic keys (no duplicate collapse leakage).
- **TP reach-rate calc:** cross-checked (TP1⊇TP2⊇TP3 monotone; reached+stop+expired partition consistent).

## Production-safety / regression
- `pytest tests/test_display_status.py tests/test_catalyst_label_refresh.py tests/test_default_market_schedule.py tests/test_project_state_docs.py` → **58 passed**.
- Scheduler dry-run guard → `LLM-auto-invoke check OK (no Opus/Claude tokens in plan)` — no live/exec step.
- Docs validator → `PROJECT STATE DOCS: OK`.
- **No production trade-logic files changed.** Only NEW artifacts added: `scripts/tp_stop_replay.py`, `data/research/tp_stop_replay_dataset_2026-06-23.csv`, reports/*. `tracker.py`, scoring, routing, filters, validity, config/signal_tracking.yaml — untouched.

## Verdict
`TP_STOP_REPLAY_TESTS_PASS`
