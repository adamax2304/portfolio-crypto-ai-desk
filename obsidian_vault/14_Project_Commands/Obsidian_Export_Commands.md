# Obsidian Export Commands (Recommended / Not Implemented)

These CLI commands would automate exporting desk state into the Obsidian vault. **None of them exist yet** — track as recommended in [[Improvement_Backlog]].

## Proposed surface

```powershell
# refresh the LLM context snapshot inside the vault
python -m src.cli obsidian-daily-context

# write a Potential_Trades file for a specific idea
python -m src.cli log-trade-to-obsidian --idea-id IDEA_ID

# write a Telegram_News or News_Item file for a news_items row
python -m src.cli log-news-to-obsidian --news-id NEWS_ID

# generate the daily News_Impact_Review skeleton
python -m src.cli review-news-impact --date YYYY-MM-DD

# bulk export the entire knowledge base (state-of-desk) as Obsidian-compatible markdown
python -m src.cli export-knowledge-base --format obsidian
```

## Where each would write

- `obsidian-daily-context` → `obsidian_vault/15_LLM_Context/Current_Context_For_LLM.md` (overwrite).
- `log-trade-to-obsidian` → `obsidian_vault/11_Trade_Journal/Potential_Trades/YYYY-MM-DD_SYMBOL_MODE_DIRECTION_SCORE.md`.
- `log-news-to-obsidian` → `obsidian_vault/12_News_Intelligence_Journal/Telegram_News/YYYY-MM-DD_HHMM_SOURCE_SYMBOL_SLUG.md`.
- `review-news-impact` → `obsidian_vault/12_News_Intelligence_Journal/News_Reviews/YYYY-MM-DD_News_Impact_Review.md`.
- `export-knowledge-base` → bulk write across `00_System_Overview`, `15_LLM_Context`, etc.

## Implementation outline

Each command would:

1. Open the corresponding SQLite row or agent_outputs JSON.
2. Render via a Python f-string template that mirrors the matching `Templates/` file in the vault.
3. Write to the file path. Refuse to overwrite without `--force`.
4. Log to stdout the file path.

## Critical constraint

Any future implementation must:

- **Never write to `news_trader/`**.
- **Never overwrite an existing trade journal entry without `--force`**.
- **Respect Obsidian link syntax** (`[[Name]]`).
- **Skip secrets** — do not write `bot_token` into vault notes.

## Until implemented

Manual workflow:

1. Open the latest report at `data/reports/{kind}/...md`.
2. Copy the relevant idea / news block.
3. Paste into the matching template in `Templates/` and save under the right folder.

## Related

- [[Trade_Idea_Template]]
- [[News_Item_Template]]
- [[Current_Context_For_LLM]]
- [[Improvement_Backlog]]

## Implemented status

- **Recommended / not implemented**.
