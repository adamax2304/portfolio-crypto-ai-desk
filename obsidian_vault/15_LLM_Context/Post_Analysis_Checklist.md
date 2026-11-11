# Post-Analysis Checklist

Run this checklist **after** producing trade ideas / analysis. This is where the desk's memory grows.

---

## A — Output sanity

- [ ] Every trade idea has direction / entry / invalidation / risk / counter-thesis / tier / data_confidence / caps.
- [ ] A-tier ideas have zero active caps. (If any cap is active → must be B-tier, not A.)
- [ ] No idea is below score 65 marked as actionable.
- [ ] Rejected ideas are listed with `primary_reason`.

## B — Trade journal logging

- [ ] A-tier ideas → created under `obsidian_vault/11_Trade_Journal/Potential_Trades/`?
  - Filename: `YYYY-MM-DD_SYMBOL_MODE_DIRECTION_A_SCORE.md`.
  - Template: `Potential_Trade_Template.md`.
- [ ] B-tier ideas (actionable) → same folder, tier=B in filename.
- [ ] C-tier with clear trigger → `Watchlist_Ideas/` folder.
- [ ] Rejected ideas (educational only) → `Rejected_Ideas/`.

## C — News intelligence journal

- [ ] Any new useful news item → `Useful_News/` with `News_Item_Template`.
- [ ] Any market-moving news (even untraded) → `Market_Moving_News/`.
- [ ] Any noise items → `Useless_News/` (keep entries short).
- [ ] Any fake / unverified → `Fake_or_Unverified_News/`.
- [ ] Default Telegram landing files in `Telegram_News/` if classification pending.

## D — Memory refresh

- [ ] [[Current_Context_For_LLM]] refreshed with:
  - Mode just run.
  - Regime label + risk_mode + breadth.
  - Top candidates.
  - Active A/B-tier ideas.
  - C-tier watchlist.
  - Top rejected reasons.
  - Latest watchlist monitor upgrades (if known).
  - Latest Telegram alerts.
  - News pulse summary.
  - Top narratives.
  - Risk warnings / coverage gaps.
  - Focus for next session.

## E — Lessons / improvements

- [ ] Any pattern noticed during analysis that should change a rule?
  - If yes → add a bullet to `obsidian_vault/13_Debugging_and_Improvement/Improvement_Backlog.md`.
- [ ] Any vault page that's outdated?
  - If yes → fix the page, or file the discrepancy in `Improvement_Backlog`.
- [ ] Any source / channel that earned or lost trust today?
  - If yes → note in the daily News_Reviews entry.

## F — Statistics maintenance (manual, weekly)

- [ ] Counts: A / B / C / rejected for the session.
- [ ] Watchlist promotions (C → B/A).
- [ ] Telegram alerts sent.
- [ ] If end-of-day: prepare daily review.
- [ ] If end-of-week: prepare weekly review + source reliability ranking.

## G — Conflict flags

- [ ] Code vs vault conflict spotted? → state it explicitly.
- [ ] Vault page vs reality conflict? → fix or file.
- [ ] Cap behavior unexpected? → file in `Improvement_Backlog`.

## H — Closing summary

Always end with:

- Compact trade table (symbol / tier / score / direction / entry / SL / TP1 / caps).
- Risk warnings (caps, regime cautions, coverage gaps).
- What to monitor next (BTC structure, funding shifts, narrative heatmap, watchlist upgrades).
- Data that was weak / missing.
- Logging actions taken (file paths created / updated).

If any line above is unchecked, **stop**, finish it, then close the session.

## Related

- [[Pre_Analysis_Checklist]]
- [[Post_Trade_Review_Checklist_For_LLM]] (per-trade after close)
- `prompts/system/REVIEW_AND_LEARNING_PROTOCOL.md`

## Implemented status

- **Operator framework / checklist**.
