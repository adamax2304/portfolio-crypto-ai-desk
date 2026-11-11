# How to use the desk daily

A practical operating routine. Adjust to your hours; the desk does not care about wall-clock time, only data freshness.

## Morning open (your local morning)

1. `python -m src.cli update-data` — refresh OHLCV + derivatives + news.
2. `python -m src.cli intraday-report --auto-universe` — fresh 15m/1h/4h report.
3. `python -m src.cli latest --kind intraday --show` — print to terminal.
4. Skim:
   - Regime + bias.
   - A/B-tier ideas.
   - Rejected-with-reason block (this is where most of the signal lives).
   - Coverage audit (which data streams are missing right now).
5. If a setup looks promising but is C-tier, do **not** force it. Log it in [[11_Trade_Journal/Watchlist_Ideas/README|Watchlist_Ideas]] with the [[Watchlist_Template]] and wait.

## Continuous

1. `python -m src.cli monitor-watchlist --interval 600` — re-checks the C/rejected names every 10 minutes, fires Telegram alerts on C→B / rejected→B/A upgrades. Runs the same scoring pipeline as a full report but only on the previously-surfaced watch list.
2. Telegram alerts include entry zone, SL level, TP1/TP2, score, mode, confidence. They are dedup'd with a 30-minute cooldown per symbol.

## Mid-session

- If volatility regime changed (e.g. BTC broke a key level), run an intraday refresh instead of trusting the morning snapshot.
- For scalp focus, switch to `scalp-report --auto-universe`. Don't mix scalp and intraday signals on one trade.

## Evening review

1. `python -m src.cli review` — runs `ReviewAgent` against saved ideas and writes `data/reports/reviews/YYYY-MM-DD_HH-MM_review.md`.
2. For any executed trade, copy the report excerpt into a new note inside `11_Trade_Journal/Executed_Trades/` using [[Executed_Trade_Template]].
3. For any rejected idea you almost took, log it in `11_Trade_Journal/Rejected_Ideas/` using [[Rejected_Trade_Template]] — these are the most informative entries.
4. For any Telegram or news headline that actually moved price, log it in `12_News_Intelligence_Journal/Market_Moving_News/` using [[News_Item_Template]].
5. End the day with a `Reviews/YYYY-MM-DD_Daily_Review.md` note using [[Daily_Review_Template]].

## Weekly

- Run [[Weekly_Review_Template]] each Sunday. Tag patterns: which agent was repeatedly right / wrong, which Telegram channels actually mattered, which sectors over/underperformed expectations.
- Update [[06_Sectors_and_Narratives/Sector_Overview]] notes when narratives clearly shift.
- Move stale notes out of `Useful_News/` if a re-review shows they were actually noise.

## Related

- [[Daily_Commands]]
- [[How_to_use_with_Claude_or_Codex]]
- [[Current_Context_For_LLM]]

## Implemented status

- **Implemented** — all referenced commands exist in [src/cli.py](../../src/cli.py).
