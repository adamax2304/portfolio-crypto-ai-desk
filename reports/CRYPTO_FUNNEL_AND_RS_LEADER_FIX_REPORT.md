# Crypto Funnel Widening + Relative-Strength Leader Gate — Fix Report (PART 20)

**Date:** 2026-06-03
**Severity:** HIGH (signal generation — zero crypto signals for ~2 days)
**Scope:** crypto pipeline only — stocks untouched.

## Symptom

No crypto A/B signals (and therefore no Telegram alerts) for ~2 days. The
desk was scanning hundreds of symbols but producing only C-tier watchlist
rows even while genuine outperformers (NEAR +10% / RS vs BTC +13%, ENA +20%,
ONDO +13%) were printing.

## Root causes

### 1. Regime gate killed *every* long indiscriminately

`technical_setup_agent.py` stamped **every** long in a `bearish trend` /
`high-volatility danger` regime with *"Long setup conflicts with current
market regime."* That warning:
- triggered the `regime_conflict` scoring penalty (−8), and
- `risk_agent.py` independently added **+25** risk for the same regime,
  which the scoring agent converted into another ~−9..−18 penalty.

Net: a coin **rising against** a falling BTC — the textbook relative-strength
setup — was treated identically to a coin **drifting down with** the tape, and
buried to a ~34 score → rejected. The system could not distinguish *defying*
the regime from *conflicting* with it.

### 2. Funnel too narrow

High per-exchange volume floors + small deep/idea caps (deep 30, ideas 15)
kept the actionable pool tiny, so even the few survivors were the same names
each cycle.

## Fixes

### A. Relative-strength leader gate (new) — `src/analysis/relative_strength_gate.py`

Single shared definition used by all three agents. A candidate is a **leader**
when:
- `relative_strength_btc ≥ 5.0%` (configurable), **and**
- `return_24h > 0` (actually rising, not merely falling slower than BTC).

Thresholds live in `config/scoring.yaml → relative_strength_gate`.

A leader is **not** given a free pass. Downstream it is:
- capped at **B-tier** (counter-trend — never a clean A against the broad tape),
- charged a **reduced-but-non-zero** risk penalty (size-down discipline), and
- still subject to overextension / invalidation / liquidity / funding gates.

### B. `technical_setup_agent.py`

For a leader long in bearish/danger, the old conflict warning is replaced with
a **counter-tape note** (`"Relative-strength leader: rising vs a weak BTC tape
(RS vs BTC +X%); counter-tape long — reduce size."`). The note carries no
`conflict`/`fights` keyword, so it no longer trips the scoring penalty.
Non-leaders keep the original conflict warning.

### C. `risk_agent.py`

Leader longs in `high-volatility danger` / `bearish trend` get **+12** risk
(was +25) plus an explicit half-size / tight-invalidation instruction, instead
of the full adverse-regime penalty.

### D. `scoring_agent.py`

- `_market_alignment` boosts leader longs: ambiguous/danger `0.58 → 0.72`,
  bearish `0.25 → 0.60`.
- The PART 11 intraday cap now lets a leader reach **B (70)** instead of being
  demoted to C (60); a danger-regime leader long gets an explicit B-cap too.
- Non-leaders are unchanged (still C-capped / rejected).

### E. Funnel widening — `config/universe.yaml`

| Knob | Before | After |
|---|---|---|
| binance 24h vol floor | 10,000,000 | 5,000,000 |
| bybit 24h vol floor | 5,000,000 | 3,000,000 |
| mexc 24h vol floor | 1,500,000 | 1,000,000 |
| max_symbols_for_rank_scan | 120 | 180 |
| max_symbols_for_deep_analysis | 30 | 40 |
| max_symbols_for_trade_ideas | 20 | 20 (15→20) |

The wider pool still passes the same per-candle volume / spread / ATR risk-flag
gates downstream — junk is filtered later, not at the door.

### F. Universe expansion — `config/universe.yaml` + `config/watchlist.yaml`

`preferred_symbols` and the monitored `symbols` list expanded **20 → 45**
(added ADA, DOT, LTC, BCH, ATOM, UNI, AAVE, FET, RENDER, FIL, ICP, HBAR, IMX,
STX, TON, JUP, PYTH, WLD, ONDO, RUNE, ETC, LDO, DYDX, GALA, ALGO). Dynamic
universe `max_symbols` 40 → 60. Narrative baskets updated (RNDR→RENDER, +ICP,
+PYTH).

## Tests

`tests/test_relative_strength_gate.py` — 13 tests, all green:
- gate helper (leader / low-RS / negative-24h / missing data / config read);
- `_market_alignment` leader > non-leader in bearish + danger;
- scoring: danger leader long → **B**, cap 70, RS-leader reason;
- scoring: bearish leader capped at 70, non-leader still capped at 60;
- risk: leader penalised less than laggard;
- technical agent: leader → counter-tape note (no "conflict"); non-leader →
  conflict warning.

Regression: `test_scoring`, `test_tiering`, `test_regime_weights`,
`test_crowd_attention` → 25 passed. Full suite: see verification report.

## Safety / discipline preserved

- ✅ No auto-trade.
- ✅ Global A/B thresholds unchanged (a_tier 80 / b_tier 65 / c_tier 50).
- ✅ Stocks logic untouched.
- ✅ Leaders are **capped at B** — the desk never fires a clean A long against
  a bearish/danger tape. Counter-tape trades carry an explicit reduce-size /
  tight-invalidation instruction.
- ✅ No historical data deleted.

## Runtime note

deep-analysis 30 → 40 adds OHLCV fetches per cycle. Scalp already ran ~1455s
against an 1800s step timeout — monitor the next scheduled scalp; if it times
out, bump the scalp step timeout in `scripts/run_default_market_schedule.py`.

## Files touched

- `src/analysis/relative_strength_gate.py` — NEW
- `src/agents/technical_setup_agent.py`
- `src/agents/risk_agent.py`
- `src/agents/scoring_agent.py`
- `config/scoring.yaml` — `relative_strength_gate` block
- `config/universe.yaml` — floors, funnel caps, preferred_symbols
- `config/watchlist.yaml` — symbols, dynamic_universe, narratives
- `tests/test_relative_strength_gate.py` — NEW (13 tests)
