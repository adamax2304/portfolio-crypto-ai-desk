# Crypto Fast Flush Reclaim v3 - Implementation and Audit

Generated: `2026-09-28T22:40:00Z`

## Scope completed

1. Added four isolated Paper profiles: strict fast 1m, balanced fast 1m, held 1m and 5m control reclaim.
2. Built a resumable Binance/Bybit one-minute event-window archive from independent liquidation episodes.
3. Replayed the profiles point-in-time with local liquidation, OI and spread evidence.
4. Attached an append-only forward collector to the running derivatives monitor.

The strategy is Paper-only. It has no live route and no call to the live execution bridge.

## Strategy logic

All profiles first require a bounded, abnormal five-minute sell-off rather than an ordinary red candle:

- liquidation notional and per-symbol liquidation percentile;
- price displacement in both percent and ATR units;
- abnormal volume;
- a bounded OI decrease, excluding both weak moves and uncontrolled cascades;
- acceptable spread and fresh derivatives/liquidity context;
- a permitted market session.

They differ in reclaim confirmation or in the strict-vs-balanced admission gate:

- `crypto_fast_flush_reclaim_fast_1m_paper_v3`: first valid green 1m reclaim; US session; fastest entry.
- `crypto_fast_flush_reclaim_balanced_1m_paper_v3`: the same 1m entry/exit mechanics, but Europe+US, OI drop from 0.25% and stop distance from 0.75%; this is the higher-frequency A/B branch.
- `crypto_fast_flush_reclaim_held_1m_paper_v3`: two 1m bars must hold and progress; slower confirmation.
- `crypto_fast_flush_reclaim_control_5m_paper_v3`: one confirmed 5m reclaim; Europe/US control branch.

The stop is structural, below the sweep low plus an ATR buffer, and must pass a cost-aware minimum/maximum distance gate. Risk is fixed at `$10`. The replay takes 70% at `0.8R`, 30% at `1.35R`, moves the remainder to break-even after TP1 and resolves same-bar stop/target ambiguity stop-first.

## Data and replay integrity

- Candidate liquidation episodes: `2,680`, selected before looking at outcomes.
- 1m candles archived: `1,061,195` across Binance and Bybit.
- Requested exchange/event windows: `1,676`; failed exchange windows: `348`, predominantly Binance HTTP 418 after the initial historical burst.
- Replay OHLC gaps: `0` candidate events.
- Point-in-time replay period with usable local context: `2026-09-07 22:40Z` to `2026-09-28 20:45Z`.
- Chronological split: 70% train / 30% untouched holdout at `2026-09-24 15:50Z`.
- Parameter selection used train only, with three temporal train folds; holdout was not used for selection.
- Fees and slippage are modeled; correlated market-wide flushes count once using the strongest event.
- Missing context: `1,462` early events, mostly from before the local liquidity archive existed. They were excluded, not filled with future data.

## Backtest result

| Profile | Train | Holdout | All cascade-adjusted | Decision |
|---|---:|---:|---:|---|
| FAST 1m | 15 trades, +8.05R, PF 7.11 | 5 trades, +1.61R, PF 2.41 | 20 trades, +9.66R, PF 4.93 | Modest OOS edge; Paper only |
| HELD 1m | 11 trades, +1.14R, PF 1.38 | 8 trades, -0.59R, PF 0.83 | 19 trades, +0.54R, PF 1.08 | No OOS edge yet |
| CONTROL 5m | 13 trades, +8.17R, PF 119.23 | 4 trades, -1.66R, PF 0.32 | 17 trades, +6.51R, PF 3.61 | Train-overfit warning |

Only strict FAST 1m remained profitable on the original untouched chronological holdout. Its holdout sample is five trades, so this is evidence of a small candidate edge, not proof suitable for Live promotion. BALANCED was added later from a frequency sensitivity analysis: 45 cascade-adjusted trades, +7.20R and PF 1.54 historically, but this is not a fresh holdout because the original holdout had already been inspected. HELD and CONTROL remain useful negative/control branches.

## Paper and runtime audit

- Activation timestamp: `2026-09-28T22:28:30.618477Z`.
- Latest monitor heartbeat: `OK`, stage `current_refresh_completed`.
- Latest v3 cycle: `fast_flush_v3_paper_new=0`; no qualifying event occurred in that cycle.
- Forward archive advanced through the monitor cycle; latest archive update `2026-09-28T22:39:13Z`.
- Each of the four profiles has a unique `profile_id`, evaluation row and shared append-only outcome schema.
- Paper observations already record rejected near-misses; 363 observations existed at audit time.
- Current clean closed sample is zero because the Paper activation is new; all four verdicts correctly read `INSUFFICIENT_CLEAN_SAMPLE`.
- A temporary Binance public API 418 occurred after the historical burst. Bybit remained the primary complete replay source, while the production monitor retained Bybit/MEXC/Hyperliquid/OKX coverage. The backfill now has lower concurrency, pacing and explicit 418/429 backoff.

## Verification

- Focused integration/governance tests after the balanced-profile change: `20 passed`.
- Full repository test run after the balanced-profile change: `2,596 passed`.
- Python compilation: passed.
- Live-route scan: no v3 references under `config/live_routes` or live execution modules.
- Monitor restart: successful; one active process owns the derivatives-monitor lock and all four profile verdicts appeared in its first completed cycle.

## Promotion gate

No v3 profile should enter Live before at least 28 forward days and 30 clean closed Paper trades. Strict FAST is the quality leader; BALANCED is the frequency challenger. Their edge must survive the forward sample, costs, event clustering and at least one different volatility regime. HELD and CONTROL need a positive forward result before any promotion discussion.
