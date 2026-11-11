# News Evaluation Checklist For LLM

Use when the user asks "is this news useful / actionable / fake?".

## A — Identify the news

- [ ] Source: Telegram channel / RSS feed / manual / exchange announcement / X / project blog?
- [ ] Timestamp: how fresh (< 30 min / 30–120 min / > 120 min)?
- [ ] Related symbol(s) and narrative(s)?
- [ ] Was the headline already in `news_trader_bridge` aggregation? (mention_count, strong_tier_count)

## B — Verification

- [ ] Primary source available? (project page, exchange page, regulator)
- [ ] Multiple secondary sources reporting the same thing?
- [ ] Single source only? → `verification = single_source`.
- [ ] Words like "rumor", "reportedly", "insider" present? → cap at 55.
- [ ] Bridge cluster has a `tier=strong` signal? → `verification = confirmed`.

## C — Market reaction

- [ ] Price reaction at 5m / 15m / 1h / 4h?
- [ ] Volume_ratio above 1.5x on the news bar?
- [ ] OI / funding shift consistent with direction?
- [ ] Cross-exchange agreement (Binance + Bybit move together)?

## D — Trade relevance

- [ ] Does this support an existing setup?
- [ ] Does this contradict an existing setup?
- [ ] Could this create a new setup (with structure + invalidation)?
- [ ] Or is it just attention with no actionable setup?

## E — Classification

| Outcome | Classification |
|---|---|
| Created or confirmed a tradable setup | Useful |
| No measurable reaction within 60 min | Useless |
| ≥ 2% move within 60 min | Market-moving (regardless of trade) |
| Turned out false or no primary verification within 24h | Fake / unverified |
| Verified but arrived after the move already played | Late / priced in |
| Interesting but not actionable today | Watch only |

## F — Where to file in the vault

- `obsidian_vault/12_News_Intelligence_Journal/Telegram_News/` — default landing.
- `Useful_News/` / `Useless_News/` / `Fake_or_Unverified_News/` / `Market_Moving_News/` — after classification.
- `News_Reviews/` — for weekly source-reliability summaries.

Use the matching template from `12_News_Intelligence_Journal/Templates/`.

## G — Output template

```
News item: {short title}
Source: {channel / feed}
Symbols: [SOL/USDT, ETH/USDT, ...]
Verification: confirmed / multiple / single_source / unverified / rumor / fake
Reaction 1h: +X% / no move
Volume reaction: spike / muted
OI / funding reaction: agree / disagree / n/a
Classification: useful / useless / market-moving / fake-unverified / late-priced-in / watch-only
Trade implication: take / watchlist / reject / no impact
Where to file: <folder>
Lesson: ...
```

## Hard rules

- Telegram message alone is never a trade.
- Rumor-only never reaches A-tier (cap 55).
- An unconfirmed listing rumor must be verified on the official exchange page before sizing.
- Macro headlines need confirmation across multiple primary sources (Bloomberg + Reuters + official).

## Related

- [[Telegram_News_Evaluation]]
- [[News_Verification]]
- [[Primary_vs_Secondary_Sources]]
- [[Useful_vs_Useless_News]]
- [[Templates/News_Item_Template]]

## Implemented status

- **Operator framework / checklist**.
