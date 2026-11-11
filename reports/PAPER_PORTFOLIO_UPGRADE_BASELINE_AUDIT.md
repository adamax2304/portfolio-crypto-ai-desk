# Paper Portfolio Upgrade — Baseline Audit (PART 1)

**Date:** 2026-06-24. Pre-change verification. Read-only.

| check | result |
|---|---|
| Model F active for paper/accounting | ✅ `src/execution/paper_execution_accounting.py` (early_mfe_protection_v1), tracker hook + scheduler step |
| `paper_execution_r` is main paper PnL | ✅ headline in app/Telegram; `paper_execution_outcomes` table |
| `final_r` still touch-based/optimistic | ✅ `_classify` highest-TP-touched; labelled "optimistic" in app |
| `paper_execution_outcomes` populated & fresh | ✅ 1610 rows, refreshed by scheduler step |
| `/api/health` live/auto-live locked | ✅ `live_locked:true, auto_live_locked:true` |
| `signal_outcomes.final_r` not rewritten | ✅ no `paper_*` column on signal_outcomes; rows only appended |
| app shows Paper Execution R + Touch R separately | ✅ headline + secondary "optimistic" card |
| Paper Features panel exists | ✅ `/api/paper-features` + dashboard panel + `config/paper_features.yaml` |

## Verdicts
`PAPER_EXECUTION_BASELINE_OK` · `LIVE_LOCKS_INTACT` · `SAFE_TO_START_PAPER_PORTFOLIO_UPGRADE`
