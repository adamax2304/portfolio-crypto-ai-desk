# Crypto Profit-Protection — Path-Aware Replay (PART 4)

**Date:** 2026-06-17 · **Script:** `scripts/replay_profit_protection_path_aware.py` · **CSV:** `CRYPTO_PROFIT_PROTECTION_PATH_AWARE_REPLAY.csv`
**Verdict:** **DATA_COVERAGE_INSUFFICIENT** → **DO_NOT_ENABLE_PROFIT_PROTECTION_YET.** `partial_exit_model.enabled` stays `false`; no config changed.

## Method
Walks OHLCV candle-by-candle in sequence (entry first, then each candle), so BE/partial/trailing triggers respect path order and BE-stop whipsaw is modeled — unlike the prior MFE/MAE counterfactual. Uses the finest timeframe that **fully covers** each trade's entry→exit window (5m → 15m → 1h; 1m excluded as today-only). Conservative same-candle rule (stop taken first), matching the production tracker. R computed from actual entry/stop/TP prices.

## ⚠ Coverage is the headline finding
The live OHLCV store keeps only rolling ~220-candle windows: **1m ≈ 4h, 5m ≈ 18h, 15m ≈ 2.3d, 1h ≈ 9d.** A clean 7–30d high-fidelity path replay is therefore **not possible** with the on-disk data.

| Metric | Value |
|---|---|
| Crypto intraday/swing closed trades (30d) | 146 |
| Trades with full path coverage | **28 (19.2%)** |
| Timeframe used | 5m (all 28) |
| Coverage bias | the covered 28 are the most-recent ~18h — i.e. the recent losing streak, NOT a representative sample |

## Variant results on the covered (recent, bleeding) subset (n=28)
| Variant | Net R | PF | Winrate |
|---|---|---|---|
| A current (as-traded) | **−19.76** | 0.21 | 10.7% |
| B BE after +0.5R | **−3.0** | 0.0 | 0% |
| C BE after +1R | −13.8 | 0.19 | 3.6% |
| D partial 50% @ +1R | **−10.22** | 0.40 | 25.0% |
| E 33/33/runner | −16.8 | 0.22 | 14.3% |
| F trailing after +1R | −12.68 | 0.25 | 39.3% |
| G candle-close stop | −18.09 | 0.25 | 14.3% |
| H one re-entry | −19.76 | 0.21 | 10.7% |
| I no re-entry (baseline) | −19.76 | 0.21 | 10.7% |

## Honest interpretation
- On this covered slice **every protection variant reduces the loss** vs current (B BE+0.5R: −19.8R → −3.0R; D partial: −10.2R; F trail: −12.7R). Directionally consistent with "the recent losses are exit-management."
- **But the sample is 19.2% and regime-skewed** to the recent down-trend window with almost no winners. BE/partial look great precisely because there were few runners to clip. On the breakeven full population (PF≈1.0), BE+0.5R would clip winners — that cost is **invisible here**.
- B's 0% winrate (everything exits at BE≈0 or −1) is a window artifact, not a strategy result.

## Why not enable
- Coverage 19.2% + recent-loss bias → cannot project net positive to the real book.
- The most defensible candidate **if** deeper data later confirms is **partial 50% @ +1R** (best PF 0.40 here, books real R while leaving a runner) or **BE after +1R** (fewer false BE triggers than +0.5R).

## Next (measurement, not enabling)
1. **Archive 5m/15m history** (extend the rolling window or pull from an archive) so ≥30d of trades are path-coverable, across both up and down regimes.
2. Re-run this script; require **net-positive incl. winners and PF>1** on the full population before discussing enabling `partial_exit_model` (still paper, with explicit approval).
3. Secondary verdict tag: **ENABLE_PARTIAL_TP1_SHADOW_ONLY_CANDIDATE** — partial-TP1 is the front-runner to *shadow-measure* first, not to enable.
