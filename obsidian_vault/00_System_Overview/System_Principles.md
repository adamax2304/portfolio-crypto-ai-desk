# System Principles

These are the non-negotiable behavioral rules of the desk. They are enforced in code (score caps, no-invalidation rejection, MEXC cap, freshness cap) and in this vault. Future LLM modifications must preserve all of them.

## Discipline (already wired into code)

1. **No idea without invalidation.** Missing invalidation forces `tier = rejected` and `score ≤ 50`. Enforced in [scoring_agent.py](../../src/agents/scoring_agent.py) and [technical_setup_agent.py](../../src/agents/technical_setup_agent.py).
2. **No A-tier from incomplete data.** A-tier requires score ≥ 80 **and** zero active score caps. Caps include: no anchor listing, MEXC-only, low liquidity, rumor-only catalyst, stale data, extreme adversarial funding. See [[Score_Caps]].
3. **No idea on stale data.** OHLCV older than 3h triggers a cap to 50, tier=rejected.
4. **No chasing.** Any setup more than 2 ATR from EMA20 is converted to watchlist_only and warned ("Converted to watchlist only: wait for pullback.").
5. **No A-tier on MEXC-only listings.** MEXC-only caps at 70 (65 if structure is weak). Bybit confirmation does not lift the cap — only anchor (Binance) does.
6. **No silent trades.** Rejected ideas are rendered in the report with the primary reason and supporting reasons.
7. **No hallucinated catalysts.** Unverified rumor-only catalysts cap at 55. Verification states are `none`, `news_mention`, `manual_event`, `single_source`, `rumor`, `confirmed`.
8. **No extra confidence when funding is adversarial.** `funding_rate > +0.001` against a long, or `< -0.001` against a short, caps at 78.

## Skepticism (built into the agent flow)

- `CriticAgent` runs **before** `ScoringAgent` and explicitly argues against each setup. Its verdict + flags (`weak_signal_dependency`, `late_or_crowded`) push penalty up.
- `CoverageAuditAgent` names exactly which data streams are missing or stale in every report.
- `CrowdAttentionAgent` separates **silent / early_attention / growing_hype / euphoria / exhaustion / fear_capitulation / rumor_driven**. Euphoria and rumor_driven raise warnings; they do not raise score.

## Telegram-specific discipline

- Telegram messages from `news_trader` enter only through `CrowdAttentionAgent` as social notes; they do **not** raise trade score directly.
- A Telegram message classified as `tier = strong` in news_trader is treated as `verification = confirmed`; everything else as `single_source`.
- Rumors never reach A-tier. See [[Rumors_and_Unverified_News]].

## Output discipline

- "No trade" is a valid, expected answer. The desk routinely outputs reports with zero A/B-tier ideas and only watchlist / rejected.
- Reports always state freshness, missing data, and rejection reasons. LLMs reading the report must surface those, not paper over them.
- Fewer good ideas beats a pile of weak ones.

## What this means in practice for an LLM session

- Do not invent invalidation levels. If `setup.invalidation is None`, the only honest answer is "no trade".
- Do not promote a C-tier idea to a trade. If you think it deserves promotion, explain why the cap that pinned it should be removed, and check the actual data first.
- Do not treat a single fresh Telegram headline as a catalyst. It bumps attention, not score.
- When asked "should I take this trade?", check [[Pre_Trade_Checklist_For_LLM]] line by line before answering.

## Related

- [[LLM_Operating_Instructions]]
- [[No_Trade_Conditions]]
- [[Score_Caps]]
- [[News_Verification]]

## Implemented status

- **Implemented** — every rule on this page is enforced in code today.
