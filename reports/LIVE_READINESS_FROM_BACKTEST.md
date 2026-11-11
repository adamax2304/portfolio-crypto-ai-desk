# Live Readiness — From Backtest (PART 9)

**Date:** 2026-06-11 · **Companion to:**
[BACKTEST_FEASIBILITY_AUDIT.md](BACKTEST_FEASIBILITY_AUDIT.md),
[BACKTEST_METHODOLOGY_SPEC.md](BACKTEST_METHODOLOGY_SPEC.md),
[BACKTEST_EXECUTION_COST_MODEL.md](BACKTEST_EXECUTION_COST_MODEL.md),
[PLAYBOOK_SIZING_WALK_FORWARD_BACKTEST.md](PLAYBOOK_SIZING_WALK_FORWARD_BACKTEST.md).

---

## Verdict

```
READY_FOR_MANUAL_LIVE_SHADOW
```

**Auto-execution is forbidden.** No real orders. All trades must be entered manually by the operator after independent verification of the alert.

---

## Why not `READY_FOR_MICRO_LIVE_*`

| Required condition | Status |
|---|---|
| Replay positive after fees/slippage | ✅ all-time +161 raw / +216 sized; 14d +34 raw / +103 sized |
| Playbook-aware sized R positive | ✅ +215.95 across full sample |
| Ambiguity rate acceptable | ✅ 0% same-bar TP/stop ambiguity in current sample |
| Data coverage sufficient | ⚠️ **only 20 days of signal history**. Statistical power is below the floor for committing capital. |
| Allowed playbooks limited | partially defined below |
| Forbidden playbooks explicit | partially defined below |
| Auto-execution forbidden | ✅ stance is unchanged |

The single condition that blocks `READY_FOR_MICRO_LIVE_*` is **sample size**: even with ~1,470 signals in 20 days, the per-playbook n is too low to commit real money. The walk-forward sizing OOS window has < 150 signals.

---

## Backtest evidence used

### All-time replay (n = 1,470)
- Raw R sum: **+161.34**
- Sized R sum (playbook-aware): **+215.95**
- Fees/slippage adjustment: **−6.73 R**
- Wins / losses: 535 / 481 → WR 52.7%, PF 1.51

### Last 14d replay (n = 980)
- Raw R: +33.94, Sized R: +103.28, Fees: −4.10
- WR 45.1%, PF 1.14
- Coverage: 731 high / 249 medium / 0 low

### Sizing walk-forward (closed = 1,424, 60/30/10 split)
- Validation (n ≈ 425): equal-1× = **−41R**, current YAML = **+30R**, conservative = **+27.5R**, aggressive = **+37R**
- Forward (n ≈ 145): equal-1× = **−14R**, current YAML = **+4.5R**, conservative = **+3.75R**, aggressive = **+4.5R**
- Current YAML beats baseline in **both OOS windows**.

### Scalp 1m study
- Lower-confidence (0 signals had 1m candles). Policy B (TP1@+0.5R) wins on 5m fallback but cannot be committed without a real 1m archive.

---

## Allowed playbooks under MANUAL_LIVE_SHADOW

Manual shadow = operator may enter the trade in a separate paper or micro-real account, but the system MUST NOT place any order. The operator owns the execution decision.

| Playbook | Allowed? | Reason |
|---|---|---|
| `stocks_intraday_rth_momentum` (B-tier long, shorts) | ✅ | Strongest cohort: 61% WR over 1,084 signals, +237R raw. Sizing 1.0×. |
| `crypto_failed_bounce_short` | ✅ (small size only) | 100% WR but n=22 — tiny sample. Size at 0.5× of risk budget, not the 1.0× current YAML weight, until n ≥ 60. |
| `stocks_intraday_rth_momentum` (A-tier long) | 🟡 conditional | Allowed only at YAML's 0.5× weight. Operator must reject any signal in the AAPL/NVDA/SMCI/SMH/XLK cluster without an independent fundamental catalyst. |
| `crypto_swing_narrative_rs_momentum` | 🟡 conditional | n=18 with sized R = −1.45. Allow only if score ≥ 80 AND catalyst confirmed. |
| `crypto_intraday_catalyst_or_momentum` | 🟡 conditional | n=21 with sized R ≈ 0. Allow only with confirmed catalyst inside the last 6h. |

## Forbidden playbooks

| Playbook | Forbidden because |
|---|---|
| `crypto_scalp_momentum_continuation` | 1m archive insufficient for proper TP/SL adjudication; sized R ≈ 0 over 69 signals. Sizing YAML keeps it at 0.5× — keep paper-only. |
| `stocks_swing_watchlist_rs_rotation` | YAML weight = 0× (paused); replay sized R = +0. No reason to lift the pause. |
| `stocks_invest_watchlist_30d_thesis` | YAML weight = 0× (paused); replay sized R = +0. No reason to lift the pause. |
| Any C-tier signal | YAML weight = 0× across the board. C-tier is research-only. |
| Anything on MEXC primary | MEXC's spread/slippage penalty + thin orderbooks compound risk; defer until liquidity per-symbol gate exists. |
| Anything with `data_confidence == 'low'` | structural risk; replay's thin penalty alone is insufficient buffer for live. |

---

## Risk envelope (shadow / micro-live preparation)

| Control | Value | Why |
|---|---|---|
| Max position size per trade | **0.25% of account** | quarter of normal full-Kelly risk; treats sample size as untrusted |
| Max daily loss | **0.5%** of account | one bad day pauses everything until next session |
| Max weekly loss | **1.5%** of account | pause for the week, manual review |
| Max concurrent positions | **3** | covers correlation in cluster names |
| Min liquidity (crypto) | **24h quote vol ≥ $50M** AND order book depth ≥ 5× position notional within 25 bps | replay does not model thin alts |
| Min liquidity (stocks) | **avg daily vol ≥ 1M shares** AND price > $5 | excludes microcaps |
| Time-of-day gate (stocks) | NO new entries in first 15m of RTH (pending live-window proof) | RTH-open replay is mixed/inconclusive |
| Time-of-day gate (crypto) | NO new entries in 0:00-2:00 UTC funding rebalance window | derivatives unknown |
| Earnings gate | block any swing into earnings ≤ 2 trading days out | already enforced upstream |
| Kill switch — drawdown | Auto-stop alerts if rolling 5-day sized R < −5R | manual reset only |
| Kill switch — data freshness | Stop sending alerts if upstream packet > 90 min stale | already enforced |
| Auto-execution | **FORBIDDEN** | non-negotiable |

---

## Required manual checks before each live entry

1. Operator re-renders the relevant report and confirms the signal is still actionable (not stale, no `entry_moved_away`).
2. Operator independently confirms the catalyst (read at least one external source).
3. Operator verifies liquidity at execution time (order book, not historical 24h vol).
4. Operator verifies no upcoming event blocking the playbook (Fed, CPI, earnings).
5. Operator enters the order manually; no script may place orders on their behalf.

---

## Promotion path: shadow → micro-live

Promote to `READY_FOR_MICRO_LIVE_LIMITED_PLAYBOOKS` only when **all** of these hold:

- Total signal history ≥ 60 days.
- Walk-forward OOS sample ≥ 300 closed signals per allowed playbook.
- Fees/slippage adjustment ≤ 10% of sized R (not 5% — observed: 6.73/215.95 ≈ 3.1%; we have room).
- Operator has logged ≥ 30 manual shadow trades with matching execution (replay R within ±0.2 of manual R for ≥ 80% of trades).
- 1m crypto candle archive backfilled to ≥ 14 days continuous (for scalp; not required for non-scalp playbooks).
- No structural break in the data (no scoring change, no playbook reweight, no major regime shift) during the validation window.

Promote to `READY_FOR_BROADER_LIVE_TEST` only after all of the above plus 4 weeks of clean micro-live performance.

---

## Hard rules that survive any promotion

- Auto-execution remains forbidden until the operator explicitly opts in **per-playbook** with a separate ratification document.
- The replay engine must be re-run weekly against fresh data and the verdict updated.
- Any change to `config/sizing_weights.yaml`, scoring weights, or playbook gates resets the live-shadow timer.
