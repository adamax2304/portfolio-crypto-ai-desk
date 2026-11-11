# Strategy Reset V1

Activated at `2026-09-28T20:05:00+00:00`.

## Scope

1. Liquidity Sweep v1 remains the only micro-canary live strategy at `$2.50` fixed protected-stop risk.
2. Its trading parameters are frozen by SHA-256 fingerprint. A drift blocks new captures and requires a new version/cohort.
3. Promotion evidence accepts only point-in-time closes produced by `live_exit_parity_v3_incremental`; legacy Paper accounting is excluded.
4. Liquidity Sweep/Reclaim v2 remains Paper-only.
5. Stocks use one active RTH research lane: `stocks_intraday_breakout_1bar_paper_v1`. Pullback and Catalyst RS Paper producers are paused. At least 30 distinct RTH sessions are required.
6. Every strategy owns separate profile IDs. Duplicate ownership fails the governance registry validation.
7. Paper review requires 30 clean closes, targets 50, positive expectancy and net PnL after costs, PF at least 1.25, and maximum drawdown no greater than 8R.
8. A passing Paper gate requests operator review only. The next stage is 10-20 real fills at `$2.50` risk. Negative net/PF, excessive drawdown, or missing v3 parity at the target sample stops new canary entries automatically.

## LLM Boundary

LLM calls remain available for news context, entity linkage, narrative summaries, research, and post-trade diagnostics. They are advisory-only. They cannot change entry permission, veto a deterministic trade, adjust score/tier/size, change stop/targets, or alter live routing.

## Operational Interfaces

- Policy: `config/strategy_governance.yaml`
- Evaluator: `src/execution/strategy_governance.py`
- Latest report: `reports/STRATEGY_GOVERNANCE_LATEST.md`
- Audit database: `db/strategy_governance.sqlite`
- CLI: `python -m src.cli strategy-governance-refresh`

The micro-canary guard only blocks future captures. It never closes or modifies an existing position.
