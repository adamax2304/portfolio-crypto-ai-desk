# Crypto Scalp — Counterfactual 1m Exit Replay (PART 4)

**Date:** 2026-06-10 23:30 UTC
**Scope:** Counterfactual exit-policy comparison on existing crypto scalp signals.
**Source:** Existing `proposed_signals` (crypto, mode=scalp). No production change.

## Data caveat (CRITICAL)

- Total scalp signals: **69**
- Replayable (entry filled in available candles): **25**
- With 1m candles available: **0** (1m archive is rolling ~4h, so most fall back)
- Skipped — no candle file: 0
- Skipped — no entry fill in window: 44

Candle TF used: 5m=69

**Confidence label:** **LOWER-CONFIDENCE** because most replays use 5m or 15m, not 1m. Same-bar TP-vs-stop is adjudicated conservatively (stop first).

## Policy comparison

| Policy | Description | n | sum R | WR | avg R |
|---|---|---:|---:|---:|---:|
| A — current (TP1 / stop) | | 25 | -9.00 | 25% | -0.360 |
| B — TP1 at +0.5R | | 25 | -2.00 | 60% | -0.080 |
| C — partial 50% at +0.5R, BE for rest, +TP1 | | 25 | -2.60 | 60% | -0.104 |
| D — TP1 at +0.7R | | 25 | -4.70 | 45% | -0.188 |
| E — BE after +0.6R, then TP1 or BE-stop | | 25 | -4.00 | 33% | -0.160 |
| F — current + 4h hard expiry | | 25 | -3.71 | 43% | -0.148 |

## Per-policy exit reason breakdown
### Policy A
- stop: 15
- open: 5
- tp1: 5

### Policy B
- tp_0.5R: 12
- stop: 8
- open: 5

### Policy C
- be_after_partial: 8
- stop: 8
- open: 5
- tp1_after_partial: 4

### Policy D
- stop: 11
- tp_0.7R: 9
- open: 5

### Policy E
- stop_eff: 15
- open: 5
- tp1: 5

### Policy F
- expiry_4h: 20
- stop: 3
- open: 2

## Interpretation

- The relative ranking of policies is informative; the absolute R values are not trustworthy due to the 1m gap.
- Same-bar TP/stop on 5m or 15m may understate B and C (partial / tight TPs).
- This study is research-only; **no production exit change is implemented**.

## Recommendation

- Before considering any TP/SL change, run a sustained 1m collection campaign (≥ 14 days continuous) and re-run this study with full 1m coverage.
- Even with limited data, prefer the policy that **dominates A on both sum R and WR** across re-runs; reject any policy that wins only on one metric.