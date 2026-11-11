# B-Tier Setups

## Definition

- `final_score ≥ 65` (and < 80, OR ≥ 80 with at least one active cap that pinned it below A).
- `setup.direction ∈ {long, short}`.
- Invalidation present.

## When you'll see B-tier

- A valid setup with one or two missing pieces of evidence (e.g. derivatives data missing).
- A setup that would have been A-tier but is on a high-risk venue (MEXC-only) or not on anchor.
- A clean structure setup that doesn't quite cross 80 because momentum was modest.

## What B-tier means in practice

- Tradable, but smaller size than A-tier.
- Respect invalidation strictly.
- Reduced confidence — `confidence` is usually "medium" or "medium-high".
- Use partials at TP1; consider exiting most of position then.

## B-tier ≠ "almost A"

A score 79 with a 70 cap that pinned it = B-tier (the cap reason matters). Treat it according to the cap reason:

- MEXC-only cap → expect higher slippage, treat as discovery.
- Not on anchor cap → reduced data confidence.
- Low liquidity cap → reduce size; respect slippage.
- Rumor cap → wait for primary source before sizing up.
- Extreme funding cap → expect squeeze risk in either direction.

## B-tier in Telegram alerts

- `Supervisor._maybe_send_trade_alerts` pushes B-tier alongside A-tier.
- `WatchlistMonitor` pushes any C→B upgrade.
- Alerts include `caps:` line when caps are active.

## Related

- [[Scoring_Overview]]
- [[Score_Caps]]
- [[A_Tier_Setups]]
- [[C_Tier_Watchlist_Setups]]

## Implemented status

- **Implemented**.
