# Strategy Governance

Generated: `2026-11-11T21:42:40.830298+00:00`
Profile registry: **OK** (18 unique profiles)

| strategy | stage | verdict | new entries | evidence |
|---|---|---|---:|---|
| crypto_liquidity_sweep_v1 | archived | SHADOW_ONLY | no | n/a |
| crypto_liquidity_sweep_reclaim_v2 | archived | SHADOW_ONLY | no | n/a |
| crypto_fast_flush_reclaim_v3 | paper | PAPER_ACCUMULATING | no | paper v3=0, PF=None, sessions=0 |
|  |  | reasons |  | `SAMPLE, PROFIT_FACTOR, EXPECTANCY, NET_AFTER_COSTS` |
| stocks_rth_breakout_research_v1 | paper | PAPER_ACCUMULATING | no | paper v3=139, PF=0.5317, sessions=19 |
|  |  | reasons |  | `PROFIT_FACTOR, EXPECTANCY, NET_AFTER_COSTS, RTH_SESSIONS` |
| stocks_liquidity_shock_reclaim_v1 | paper | PAPER_ACCUMULATING | no | paper v3=0, PF=None, sessions=0 |
|  |  | reasons |  | `SAMPLE, PROFIT_FACTOR, EXPECTANCY, NET_AFTER_COSTS, RTH_SESSIONS` |

## Rules

- Paper promotion uses only point-in-time `live_exit_parity_v3_incremental` closes.
- Promotion is never automatic; a passing Paper gate only requests operator review.
- Micro-canary auto-demotion stops new captures only. It never closes existing positions.
- LLM output is advisory context only and cannot change entry, veto, score, risk, stops, targets, or routing.
