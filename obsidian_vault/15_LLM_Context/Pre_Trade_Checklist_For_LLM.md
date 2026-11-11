# Pre-Trade Checklist For LLM

Before approving any trade idea, go through this list in order. If any line is unknown, say so — do not guess.

## A — Setup integrity

- [ ] Is the **trading mode** correct for the user's stated horizon? (scalp / intraday / swing)
- [ ] Is there a clean **invalidation** in the idea? (If not → STOP. No trade.)
- [ ] Is **stale data** suspected (>3h since last cached candle)? (If yes → STOP.)
- [ ] Is **ATR** present and reasonable for the mode?
- [ ] Are **entry zone, TP1, TP2** numerically defined?
- [ ] Is **R/R to TP1 ≥ 1**?

## B — Regime alignment

- [ ] What is the current **regime label**?
- [ ] Does the direction align (`bullish trend` favors longs, `bearish trend` favors shorts)?
- [ ] If counter-trend, is the justification exceptional?
- [ ] Is regime in `high-volatility danger`? (If yes → halve size or skip.)

## C — Cross-exchange and data

- [ ] Is the symbol **listed on anchor (Binance)**?
- [ ] If **MEXC-only**, is the cap (70/65) acceptable for the trade size?
- [ ] Is **derivatives data available**? (Funding rate, OI change?)
- [ ] What is **data_confidence** ∈ {high, medium, low}?

## D — Crowding and overextension

- [ ] Is **distance from EMA20 in ATR** ≤ 2?
- [ ] Is **funding rate** in healthy band? (|funding| ≤ 0.0005 ideal; > 0.001 caps trade.)
- [ ] Is OI rising **with** the trade direction?
- [ ] What is the **CrowdAttention stage**? (`euphoria` / `rumor_driven` / `exhaustion` = warn.)

## E — Catalyst / news

- [ ] Is there a **fresh catalyst** for the move?
- [ ] What is **verification_status**? (none / news_mention / manual_event / single_source / rumor / confirmed)
- [ ] Is this **already priced in**?
- [ ] Is there a **risk_event** (unlock / delisting / migration) within 7 days?

## F — Counter-thesis

- [ ] What does **CriticAgent** say? (verdict + counter_thesis)
- [ ] What does **RiskAgent** add to `reasons_to_avoid`?
- [ ] What invalidates this if BTC structure breaks?
- [ ] What is the early-warning signal that the thesis is failing?

## G — Tier and score

- [ ] Final **score**?
- [ ] Active **score caps**?
- [ ] **Tier**: A / B / C / rejected?
- [ ] If A-tier — verify all caps are inactive.
- [ ] If B-tier — note the cap and reduce size accordingly.
- [ ] If C-tier or rejected — do not recommend trade; recommend watch or skip.

## Output template

Once the checklist is done, give the user this exact structure:

```
Verdict: take / watchlist / reject
Tier requested: A / B / C / rejected
Score: NN.N
Caps active: [...]
Top reasons to take: ...
Top reasons to avoid: ...
Invalidation: 1h close beyond <level>
Suggested R/R: <to TP1> R / <to TP2> R
Confidence: high / medium-high / medium / low
Data confidence: high / medium / low
```

## Hard rules — never override

- No invalidation → no trade.
- Stale data → no trade.
- Tier rejected → no trade (unless the user wants to override and you have flagged it).
- Telegram-only signal → not a trade; attention only.
- Caps active → A-tier impossible.

## Related

- [[LLM_Operating_Instructions]]
- [[System_Principles]]
- [[Score_Caps]]
- [[No_Trade_Conditions]]
- [[Trade_Idea_Template]]

## Implemented status

- **Operator framework / checklist**.
