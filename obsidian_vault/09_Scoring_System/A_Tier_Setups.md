# A-Tier Setups

## Definition

- `final_score ≥ 80`.
- **Zero active score caps**.
- `setup.direction ∈ {long, short}`.
- Invalidation present and within sane distance.

## Why "zero caps" is critical

A-tier is the **highest commitment** the desk will recommend. The cap chain exists specifically to prevent A-tier on:

- MEXC-only listings.
- Not on anchor.
- Low liquidity.
- Stale data.
- Rumor-only catalyst.
- Extreme adversarial funding.

If any of these are active, the score is pinned at or below the cap (70/75/60/50/55/78), preventing A-tier.

## What an A-tier idea typically looks like

- Anchor (Binance) + derivatives (Bybit) both listed.
- price_consistency ≥ 0.7 across venues.
- Direction aligned with regime (`long` in bullish, `short` in bearish, or strongly justified counter).
- Clean structure with invalidation built off recent support/resistance (not just ATR fallback).
- R/R to TP1 ≥ 1.5; ideally to TP2 ≥ 2.5.
- Setup quality ≥ ~70.
- Momentum candidate score ≥ ~65.
- Derivatives healthy (alignment positive for the direction; funding not extreme).
- Catalyst either verified or absent (not unverified).
- Coverage audit reports no missing major streams.

## How to trade A-tier

- Default size; respect the planned invalidation.
- Take partials at TP1 (1 ATR), move stop to entry.
- Hold remainder to TP2 (2 ATR) or invalidation.
- For swing-mode A-tier, use 4h close for stop respect.

## A-tier is rare by design

- In `bearish trend` regime with mid breadth, expect 0 A-tier per report most days.
- In strong `bullish trend` with clean breadth, 1–3 A-tier per day is common.
- A-tier is biased toward majors + ecosystem leaders, not low-cap discovery.

## A-tier in Telegram alerts

`Supervisor._maybe_send_trade_alerts` will push every A-tier idea to Telegram with full setup (entry, invalidation, TPs, caps if any). `WatchlistMonitor.format_alert` will also push C→A upgrades.

## Related

- [[Scoring_Overview]]
- [[Score_Caps]]
- [[B_Tier_Setups]]
- [[Pre_Trade_Checklist_For_LLM]]

## Implemented status

- **Implemented**.
