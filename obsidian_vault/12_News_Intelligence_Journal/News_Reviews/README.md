# News_Reviews

Weekly and monthly summary notes that aggregate the news intelligence dataset.

## File types

- **Daily impact review** — `YYYY-MM-DD_News_Impact_Review.md` (use [[News_Impact_Review_Template]]).
- **Weekly source reliability review** — `YYYY-Www_Source_Reliability_Review.md`.
- **Monthly mute/whitelist update** — `YYYY-MM_Source_Update.md`.

## Weekly review skeleton

```
# Source Reliability — Week W of YYYY

## Channels / sources observed
- For each source: count of items, market-moving %, useless %, fake %.

## Top 5 reliable sources this week
- ...

## Bottom 5 (mute candidates)
- ...

## Patterns
- Which categories (listing / unlock / partnership / macro) produced highest hit rate?
- Time-of-day patterns?
- Symbol-cluster patterns?

## Actions
- Sources to mentally up-weight:
- Sources to mute:
- Categories to track more carefully:
- Improvement backlog entries to file:
```

## Recommended automation (future)

`python -m src.cli review-news-impact --date YYYY-MM-DD` would auto-generate the daily skeleton by joining `news_items` with subsequent price action. Not implemented; see [[Obsidian_Export_Commands]].

## Related

- [[News_Impact_Review_Template]]
- [[Useful_vs_Useless_News]]
