# Fast-Move Detection Latency Audit (PART 6)

**Date:** 2026-06-15 · Read-only.

## Architecture-imposed latency

The system is **cycle-driven**, not event-driven for entries:
- Crypto reports run on a ~2h interval (`run_default_market_schedule --interval-hours 2`).
- Watchlist monitor ticks more frequently (`monitor-watchlist --interval 600` = 10 min) but only on already-A/B watchlist symbols.
- Telegram news collection is real-time; **signal generation is not**.

So the dominant latency is the **report cadence**, not data collection.

| Stage | Typical latency | Bound by |
|---|---|---|
| News collection | seconds–minutes | real-time RSS/Telegram |
| Catalyst classification | next catalyst-scan cycle | scheduler |
| News → A/B signal | up to ~2h | report interval |
| A/B → watchlist monitor pickup | ≤ 10 min | monitor interval |
| Signal → paper entry | when price reaches zone (tracker tick) | candle availability |
| Signal → Telegram | immediate on generation | — |

## Implication for fast moves

- A coin that pumps on a fresh catalyst is **first eligible for an A/B signal at the next 2h report**. For a fast intraday move this is often **too late to enter at a good price** — which is exactly why the system frequently rejects such setups as "more than 2 ATR from EMA20 — do not chase" (446 such rejections in 14d, per the skipped-signal audit).
- The expansion/discovery lane was built to surface fast movers earlier, but it feeds the **next** cycle, not an immediate alert.

## Chase-rejection correctness

From the skipped-opportunity audit: the `> 2 ATR from EMA20` rejection is the #1 skip reason and is **net-protective** (filters mostly lose if entered late). So the system is **correctly rejecting late chases** rather than detecting them late and entering badly.

## What's missing

- **No sub-cycle fast-move detector** that can fire an alert between scheduled reports.
- **No move-start timestamp** captured per signal, so precise detection-latency (move-start → first-notice) cannot be computed from stored data. This is a data gap, not a logic bug.

## Conclusion

- The system **catches catalysts**, but **enters on a ~2h cadence**, so it is structurally **slow for fast intraday pumps** — and it correctly compensates by rejecting late chases rather than entering them.
- Measuring true detection latency requires storing move-start timestamps (additive fix). Recommend a **fast-move latency report** that joins top-gainer candles to first-signal time. See [CATALYST_PIPELINE_SAFE_FIX_PLAN.md](CATALYST_PIPELINE_SAFE_FIX_PLAN.md).
- **No production change recommended** — chase-rejection is working as designed.
