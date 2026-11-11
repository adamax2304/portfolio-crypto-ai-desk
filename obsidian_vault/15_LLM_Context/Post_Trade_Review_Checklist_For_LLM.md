# Post-Trade Review Checklist For LLM

Run after a trade closes (winner, loser, or unresolved).

## A — Recap

- [ ] Symbol / direction / mode / entry / invalidation / TP plan?
- [ ] Tier / score / caps at the time the idea was generated?
- [ ] Original `confidence` and `data_confidence`?
- [ ] Critic counter-thesis and Risk warnings at the time?

## B — Outcome

- [ ] Did price enter the entry zone?
- [ ] Did TP1 / TP2 / TP3 hit?
- [ ] Did invalidation hit? On which timeframe close?
- [ ] R multiple realized?
- [ ] MFE / MAE relative to entry?

## C — Process

- [ ] Did I (the operator) follow the entry plan, or chase?
- [ ] Was the stop respected on close, or was it wick-triggered?
- [ ] Did I take partials at TP1 as planned?
- [ ] Did I move stop to entry after TP1?
- [ ] Did I exit early because of fear vs. by plan?

## D — Which agent was right / wrong

- [ ] MarketRegimeAgent — regime call correct?
- [ ] MomentumScannerAgent — direction_bias correct?
- [ ] DerivativesAgent — alignment correct?
- [ ] CatalystAgent — verification correct? Risk_events flagged correctly?
- [ ] NarrativeAgent — heat score predictive?
- [ ] CrowdAttentionAgent — stage call correct?
- [ ] RiskAgent — warnings useful or noise?
- [ ] CriticAgent — counter-thesis predictive?
- [ ] ScoringAgent — was the tier the right call in hindsight?

## E — Telegram / news impact

- [ ] Did Telegram-derived attention help, mislead, or do nothing?
- [ ] Did any news during the trade window invalidate or support?
- [ ] Should source X be trusted more / less next time?
- [ ] File the relevant news item into [[Useful_News]] or [[Useless_News]] or [[Fake_or_Unverified_News]].

## F — Lessons

- [ ] What I should keep doing:
- [ ] What I should stop doing:
- [ ] What pattern this trade reinforces:
- [ ] Vault page that needs an edit (if any):
- [ ] [[Improvement_Backlog]] item to add (if any):

## Output template

```
Trade: {SYMBOL} {DIRECTION} {MODE} — {DATE}
Outcome: winner +X R / loser -Y R / scratch / unresolved
Original tier / score / caps:
Agent calibration:
  - regime: correct / wrong
  - momentum: ...
  - derivatives: ...
  - catalyst: ...
  - critic: ...
News impact: useful / useless / mixed
Top lesson: ...
Notes to add to vault: [pages]
Improvement backlog suggestions: [items]
```

## Where to write the review

- Per-idea: `obsidian_vault/11_Trade_Journal/Reviews/YYYY-MM-DD_SYMBOL_Review.md` using [[Review_Template]].
- Daily roll-up: `obsidian_vault/11_Trade_Journal/Reviews/YYYY-MM-DD_Daily_Review.md`.
- Weekly: `obsidian_vault/11_Trade_Journal/Reviews/YYYY-Www_Weekly_Review.md`.

## Related

- [[LLM_Operating_Instructions]]
- [[Review_Agent]]
- [[Review_Template]]
- [[Daily_Review_Template]]
- [[Weekly_Review_Template]]

## Implemented status

- **Operator framework**.
