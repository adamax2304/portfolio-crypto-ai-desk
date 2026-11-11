# Review and Learning Protocol

The desk improves only when its ideas are reviewed against outcomes. This protocol covers per-trade, daily, weekly, and source-level reviews.

---

## When to review

| Trigger | Review type | Output location |
|---|---|---|
| Trade closes (winner / loser / scratch) | Per-trade review | `obsidian_vault/11_Trade_Journal/Reviews/YYYY-MM-DD_SYMBOL_Review.md` |
| End of trading session | Daily review | `obsidian_vault/11_Trade_Journal/Reviews/YYYY-MM-DD_Daily_Review.md` |
| End of week (Sunday) | Weekly review | `obsidian_vault/11_Trade_Journal/Reviews/YYYY-Www_Weekly_Review.md` |
| End of day, news pulse summary | News impact review | `obsidian_vault/12_News_Intelligence_Journal/News_Reviews/YYYY-MM-DD_News_Impact_Review.md` |
| End of week, source ranking | Source reliability review | `obsidian_vault/12_News_Intelligence_Journal/News_Reviews/YYYY-Www_Source_Reliability_Review.md` |
| Pattern observed during review | Improvement backlog entry | `obsidian_vault/13_Debugging_and_Improvement/Improvement_Backlog.md` |

## Per-trade review checklist

Run `python -m src.cli review` first to refresh `idea_checks` against latest candles. Then:

### Recap

- Symbol / direction / mode / entry zone / invalidation / TP plan.
- Tier / score / caps at idea generation.
- Original `confidence` and `data_confidence`.
- Original critic counter_thesis and risk warnings.

### Outcome

- Did price enter the entry zone?
- Did TP1 / TP2 / TP3 hit?
- Did invalidation hit? On which timeframe close?
- R multiple realized.
- MFE / MAE (from idea_checks).

### Process

- Did I follow the entry plan, or chase?
- Was the stop respected on close, or wick-triggered?
- Did I take partials at TP1 as planned?
- Did I move stop to entry after TP1?
- Did I exit early because of fear vs. by plan?

### Which agent was right / wrong

- `MarketRegimeAgent` — regime call correct?
- `MomentumScannerAgent` — direction_bias correct?
- `DerivativesAgent` — alignment correct?
- `CatalystAgent` — verification correct? risk_events flagged correctly?
- `NarrativeAgent` — heat score predictive?
- `CrowdAttentionAgent` — stage call correct?
- `RiskAgent` — warnings useful or noise?
- `CriticAgent` — counter-thesis predictive?
- `ScoringAgent` — was the tier the right call in hindsight?

### News / Telegram impact

- Did Telegram-derived attention help, mislead, or do nothing?
- Did news during the trade window invalidate or support?
- Should source X be trusted more / less next time?
- File the relevant news item into `Useful_News` / `Useless_News` / `Fake_or_Unverified_News`.

### Lessons

- What I should keep doing.
- What I should stop doing.
- Vault page that needs an edit.
- Improvement_Backlog item to add.

## Daily review checklist

See `obsidian_vault/11_Trade_Journal/Templates/Daily_Review_Template.md`. Fill at end of session:

- Market recap (BTC / ETH %, regime journey, sectors that worked).
- Desk outputs (A/B/C/rejected counts, monitor upgrades, Telegram alerts).
- Trades you took (wins / losses / scratches, best / worst).
- News / Telegram impact (useful / useless / fake / market-moving + sources to weight more / less).
- Agent calibration (was each agent right today?).
- Lessons / adjustments.
- Tomorrow plan.

## Weekly review checklist

See `Templates/Weekly_Review_Template.md`. Sunday work:

- Market summary (BTC / ETH week, regime journey day-by-day, top / bottom sectors).
- Desk output totals.
- Trade stats (total R, hit rate, average R per win / loss, worst DD, best winner).
- What worked / what failed (setups, sectors, venues, modes).
- News intelligence recap (sources that earned / lost trust, categories with highest moving rate).
- Calibration (cap reasons validated, warnings to re-weight).
- Adjustments (config changes, vault edits, backlog items).
- Next week (sector / symbols / events to respect, one behavior change to commit).

## News impact review

Daily skeleton (recommended automation `python -m src.cli review-news-impact --date YYYY-MM-DD` not implemented):

- Items reviewed today (Telegram / RSS / manual counts).
- Classification breakdown (useful / useless / market-moving / fake / late / watch-only).
- Highlights (top market-moving, top fake, biggest surprise).
- Sources observed (reliable / noisy / new to track).
- Cross-link to trades (helped / hurt / unaffected).
- Improvements to file.

## Source reliability review (weekly)

For each source / channel:

- Count of items.
- Market-moving %.
- Useless %.
- Fake / unverified %.

Then:

- Top 5 sources → mentally up-weight.
- Bottom 5 sources → mute.
- New sources to track.

## What gets added to `Improvement_Backlog.md`

- A consistent cap that's hurting expectancy.
- A warning that consistently fires before losers (keep).
- A warning that consistently fires before winners (consider removing or re-weighting).
- A source that earned trust → propose per-source reliability weighting.
- A source that consistently misleads → propose blacklisting.
- An indicator missing (VWAP, MACD, etc.) that would have helped.
- A regime label that's miscalibrated.

## Statistics to maintain (manual today)

Track these in weekly reviews. Until the CLI ships, do them by hand:

- A-tier idea outcomes (win / loss / R distribution).
- B-tier idea outcomes.
- C-tier watchlist → B/A conversion rate.
- Rejected ideas that later worked (false negatives).
- Rejected ideas that failed correctly (true negatives).
- Useful news sources (hit rate).
- Noisy news sources.
- Telegram channels with good / bad signal quality.
- Per-mode performance (scalp vs intraday vs swing).

## Learning discipline

- **Refuse to learn from a single trade.** Wait for ≥ 5 data points before changing a rule.
- **Distinguish bad outcomes from bad process.** A trade with a clean A-tier setup that lost is still a process win.
- **Don't tune to the last loss.** That's recency bias.
- **One change at a time.** If you adjust scoring + filters + caps in the same week, you can't tell which moved the needle.
- **Document the reasoning.** Every rule change should have a backlog entry explaining the data behind it.

## Related

- [[AI_TRADING_DESK_SYSTEM_PROMPT]]
- [[ANALYSIS_WORKFLOW_PROTOCOL]]
- [[OBSIDIAN_MEMORY_PROTOCOL]]
- [[TRADE_IDEA_LOGGING_PROTOCOL]]
- [[NEWS_INTELLIGENCE_PROTOCOL]]
