# Shadow Promotion — Dataset Summary (PART 3)

**Date:** 2026-06-19 · Window: 2026-06-18 15:39 → 2026-06-19 18:08 UTC (~26.5h). CSV: `data/research/shadow_promotion_dataset_2026-06-19.csv`.

## Population
- Signals created in window: **73** (crypto 22, stocks 51 [B 6, C 45]).
- Tier/asset: crypto all B (22); stocks B 6 / C 45 (C-tier = shadow by policy).
- **Closed actionable paper decisions** (tier A/B, non-scalp crypto, non-swing/invest stocks) = **5** — the only rows with a realized outcome to evaluate any trade-affecting feature against.

## The 5 closed actionable decisions (the entire evaluable trade sample)
| created (UTC) | asset/mode | symbol | dir | status | R | setup |
|---|---|---|---|---|---|---|
| 06-18 10:55* | crypto intraday | ALLO/USDT | long | stopped | −1.0 | breakout |
| 06-18 16:26 | stocks intraday | JPM | long | stopped | −1.0 | continuation |
| 06-18 18:58 | crypto intraday | ONDO/USDT | short | stopped | −1.0 | breakdown |
| 06-19 01:26 | crypto intraday | JTO/USDT | long | stopped | −1.0 | pullback |
| 06-19 12:58 | crypto intraday | AVAX/USDT | short | tp1_hit | +1.0 | breakdown |

**1 win / 4 losses, net −3R.** (*ALLO created pre-window but closed in-window; included via the `T`-vs-space timestamp comparison — a harmless inclusivity edge noted below.)

## Pre-decision vs hindsight (no-hindsight rule)
- **Before/near decision** (label exists at decision time, cached): intelligence labels (squeeze phase, derivatives trajectory, timeline bias), catalyst labels, risk-guard fields, lifecycle/status, regime. These are computed in the per-cycle `intelligence layer update` / `catalyst-scan` and read from cache by the alert path → usable for promotion *if* there were enough outcomes.
- **`post_factum=true` (hindsight — EXCLUDED from promotion):** shadow exit ledger, profit-protection path-aware replay, MFE/MAE-derived "would have worked" — these are computed by re-walking OHLCV *after* the fact.

## Caveats
- Sample = **5 closed actionable decisions**. Any per-feature win-rate/PF/counterfactual on this is statistical noise.
- Timestamp comparison uses string compare; `T`-separated `created_at` sorts slightly after a space-separated window bound — a ≤1-row inclusivity edge, immaterial to the conclusion. Flagged as a display-query nuance (not a trade-data issue).
- C-tier stocks (45) and crypto scalp signals have outcomes too, but they are **shadow by locked policy** — not part of the actionable promotion sample.

## Verdict
**SHADOW_PROMOTION_DATASET_READY** — and it shows the actionable sample (5, net −3R) is far too small for any trade-affecting promotion.
