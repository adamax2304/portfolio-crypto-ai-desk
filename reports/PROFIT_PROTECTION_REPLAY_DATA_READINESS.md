# Profit-Protection Replay — Data Readiness (PART 6)

**Date:** 2026-06-17 · **Status:** **NOT READY YET** — archive started today; coverage grows forward.

## Current path-aware replay coverage (archive-first)
| Metric | Value |
|---|---|
| Crypto intraday/swing closed trades (30d) | 146 |
| Path-coverable today | **26 (17.8%)**, all 5m |
| Reason | archive ≈ rolling window on day 1; deep history not yet accumulated |

## Readiness target
- **≥70% coverage** of the 30d closed-trade population on 5m/15m, spanning **both up and down regimes**.
- Estimated time to reach: ~2–4 weeks of scheduler cycles appending 5m/15m (the archive captures ~18h of 5m and ~2.3d of 15m per cycle window, deduped).

## Gating rule (unchanged)
`partial_exit_model.enabled` stays **false**. Profit protection (BE-after-1R / partial-TP1) is enabled (still paper, with explicit approval) **only after** a path-aware replay on the readiness target shows **net-positive incl. winners and PF > 1**. The front-runner to *shadow-measure* first is **partial 50% @ +1R** (best PF in the coverage-limited replay).

## How to check readiness later
1. `python -m scripts.archive_ohlcv_history --coverage-report` → confirm 5m/15m span ≥30d for most symbols.
2. `python -m scripts.replay_profit_protection_path_aware` → confirm coverage ≥70%.
3. Only then interpret the variant net-R/PF as decision-grade.

## Limitation
Bybit/MEXC rolling windows are shorter than binance's; binance 5m/15m will reach depth first. Symbols that drop out of the active universe stop accumulating. The coverage report surfaces per-exchange oldest/newest honestly.
