# 11 — Trade Journal

The trade journal is where every potential, executed, watchlist, rejected, and reviewed trade is recorded. Each entry is a single Markdown file in the appropriate folder, created from a template in `Templates/`.

## Folder layout

```
11_Trade_Journal/
  Potential_Trades/        # A/B-tier ideas being considered or waiting for entry
  Executed_Trades/         # Trades you actually entered
  Watchlist_Ideas/         # C-tier ideas the desk surfaced
  Rejected_Ideas/          # Ideas the desk rejected (or you rejected)
  Reviews/                 # Daily / weekly / per-idea reviews
  Templates/               # The 6 templates to copy
```

## Filename convention

```
YYYY-MM-DD_SYMBOL_MODE_DIRECTION_SCORE.md
```

Examples:

- `2026-05-23_SOL_intraday_LONG_78.md`
- `2026-05-23_ETH_intraday_SHORT_66.md`
- `2026-05-23_BTC_scalp_LONG_72.md`
- `2026-05-23_PEPE_swing_WATCH_60.md`
- `2026-05-23_INJ_intraday_REJECTED_44.md`

For reviews:

- `2026-05-23_Daily_Review.md`
- `2026-W21_Weekly_Review.md`

## Workflow

1. The desk generates a report → copy A/B-tier ideas into `Potential_Trades/`.
2. When you enter a trade → copy the file into `Executed_Trades/` and apply [[Executed_Trade_Template]].
3. C-tier ideas go straight into `Watchlist_Ideas/`.
4. Rejected ideas worth tracking → `Rejected_Ideas/`.
5. End of day → write a `Reviews/YYYY-MM-DD_Daily_Review.md`.
6. End of week → write a `Reviews/YYYY-Www_Weekly_Review.md`.
7. After each closed trade → cross-link a per-idea review using [[Review_Template]].

## Recommended automation (not implemented yet)

CLI commands that would help — see [[Obsidian_Export_Commands]]:

- `python -m src.cli log-trade-to-obsidian --idea-id <id>` — write a Potential_Trades file.
- `python -m src.cli review-news-impact --date YYYY-MM-DD` — produce a daily review skeleton.
- `python -m src.cli obsidian-daily-context` — refresh `[[Current_Context_For_LLM]]` from the latest desk state.

Until those exist, the workflow is manual.

## Related

- [[Trade_Idea_Template]]
- [[Templates/Potential_Trade_Template|Potential_Trade_Template]]
- [[Templates/Executed_Trade_Template|Executed_Trade_Template]]
- [[Templates/Watchlist_Template|Watchlist_Template]]
- [[Templates/Rejected_Trade_Template|Rejected_Trade_Template]]
- [[Templates/Daily_Review_Template|Daily_Review_Template]]
- [[Templates/Weekly_Review_Template|Weekly_Review_Template]]

## Implemented status

- **Folder + templates implemented**. Automated CLI export **Recommended**.
