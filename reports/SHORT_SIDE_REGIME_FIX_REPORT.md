# Short-Side Regime Fix — Implementation Report (PART 21)

**Date:** 2026-06-03
**Severity:** HIGH (no short signals despite a week-long BTC downtrend)
**Scope:** crypto pipeline only — stocks untouched.

## Question that triggered this

"BTC has been falling all week — why doesn't the system go into short mode?"

## Diagnosis

There is **no global long/short switch** — direction is decided per symbol.
Shorts *were* being generated (BCH/SOL/DOGE/BNB were short-biased last cycle)
but never reached A/B. Four reasons:

1. **Regime stuck on `high-volatility danger`, not `bearish trend`.** The
   classifier checks conditions in order and the **first** wins:
   ```python
   if high_vol and abs(btc_ret_24h) > 4:   label = "high-volatility danger"
   elif btc_trend == "downtrend" ...:        label = "bearish trend"
   ```
   With ATR percentile 98–100, the market is permanently tagged "danger"
   (= reduce size / no trade) and never reaches the short-friendly
   "bearish trend" label (alignment 0.88, short-bias style).
2. **In `danger`, shorts were penalised like longs** — RiskAgent added a flat
   **+25** to *every* direction.
3. **Short candidates failed data/volume/RR gates** — falling alts often lack
   Binance futures (derivatives "unavailable"), thin volume, RR < 1.5.
4. **Funnel crowded by pumping alts** — `opportunity_score` rewards risers, so
   the biggest losers (prime shorts) ranked below the deep-analysis cut and
   were never analysed.

## Fixes (mirror of PART 20's long-leader logic, for the short side)

### A. `is_trend_aligned_short()` — `src/analysis/relative_strength_gate.py`

New shared helper: a short is **trend-aligned** when the tape is falling
(`btc_trend` downtrend/transition_down) and the coin is not itself a strong
outperformer (`relative_strength_btc` < +5%). The mirror of the RS-leader.

### B. Directional `danger` alignment — `scoring_agent.py`

`_market_alignment` for shorts: `high-volatility danger` + BTC downtrend now
returns **0.84** (was 0.74), close to a clean bearish short (0.88). A volatile
bear is still a bear — a short with that trend is aligned, not a coin-flip.

### C. Reduced risk for tape-aligned shorts — `risk_agent.py`

In `high-volatility danger`, a trend-aligned short gets **+14** risk (was +25),
with an explicit "size down — squeeze risk in extreme volatility" note, instead
of the full danger penalty. (Counter-trend shorts — btc uptrend — still +25.)

### D. Funnel short reservation — `multi_exchange_universe_collector.py`

New `_reserve_short_slots()` appends up to `max_short_reserved_candidates`
(default **8**) anchor-listed symbols that are actually falling
(`change_24h < 0`), most-negative first, into the deep-analysis set — so the
biggest losers always get analysed (and their MEXC/Bybit derivatives fallback
fetched, which transitively addresses reason #3). Config key added to
`config/universe.yaml`.

### E. Runtime — scalp step timeout

`scripts/run_default_market_schedule.py`: scalp step timeout **1800 s → 2700 s**
(45 min) to accommodate the widened deep tier (~48 symbols) without truncating
a healthy scan. Still well under the 2 h cycle interval.

## How direction actually flips to short now

Once a short is in the deep set (reservation), the MomentumScanner ranks it by
`max(long_score, short_score)`; a coin down ~10% has a high short_score, so it
enters full agent analysis, gets alignment 0.84 (danger+downtrend), a reduced
+14 risk, and — with clean RR + real volume — reaches **B-tier**. Weak setups
(RR < 1.5, thin volume) still correctly stay rejected.

## Tests — `tests/test_relative_strength_gate.py` (+9, now 22 total)

- `is_trend_aligned_short`: downtrend+weak → True; uptrend → False; strong
  outperformer → False; None regime → False.
- alignment: short in danger+downtrend == 0.84 and > danger+uptrend.
- scoring: a clean short in a volatile-bear tape reaches **B** (≥65).
- risk: trend-aligned short penalised less than a counter-trend short.
- funnel: `_reserve_short_slots` appends biggest losers (most-negative first),
  ignores non-fallers, respects cap, no-op at reserve_n=0.

Regression: scoring/tiering/regime/crowd → 25/25 green.

## Safety / discipline preserved

- ✅ No auto-trade. ✅ Global A/B thresholds unchanged. ✅ Stocks untouched.
- ✅ Counter-trend shorts (btc uptrend) still get the full +25 danger penalty —
  only *tape-aligned* shorts are relieved.
- ✅ Shorts still need clean RR + real volume + invalidation to reach B.
- ✅ No historical data deleted.

## Deployment

Scheduler **restarted at 20:50:49** to load the new code (the long-lived
process had cached the old code; verified the prior PID 17188 was replaced).
Fresh cycle 1 is running with PART 20 + PART 21 active.

## Files touched

- `src/analysis/relative_strength_gate.py` — `is_trend_aligned_short()`
- `src/agents/scoring_agent.py` — short alignment in danger
- `src/agents/risk_agent.py` — reduced danger penalty for tape-aligned shorts
- `src/data_collectors/multi_exchange_universe_collector.py` — `_reserve_short_slots()`
- `config/universe.yaml` — `max_short_reserved_candidates`
- `scripts/run_default_market_schedule.py` — scalp timeout 1800→2700 s
- `tests/test_relative_strength_gate.py` — +9 tests (22 total)

## Note on the "danger vs bearish" label

The deepest cause (#1) is the regime classifier prioritising the volatility
label over trend. PARTs 20/21 make BOTH directions tradable *inside* danger
(longs for RS-leaders, shorts for tape-aligned). A future option is to add an
explicit "volatile bearish" sub-label so the report wording itself reflects the
directional bias — left as a follow-up since the scoring already routes
correctly now.
