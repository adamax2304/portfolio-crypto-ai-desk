# crypto-ai-desk — Obsidian Vault

This vault is the **operating manual, LLM context base, trade journal, and news intelligence journal** for the local `crypto-ai-desk` research desk.

It is not generic crypto-trading documentation. Every claim about what the system does is grounded in the actual code under `src/` and `config/` of this project. Where something is **not implemented**, the file says so explicitly under `Implemented status`.

## How to use this vault

1. Open it in Obsidian (point the vault at `obsidian_vault/`). All internal `[[links]]` resolve.
2. Before any trading or system-modification work, an LLM (or human) should read [[LLM_Operating_Instructions]] first.
3. New ideas, trades, and notable news items are dropped into [[11_Trade_Journal/README|11_Trade_Journal]] and [[12_News_Intelligence_Journal/README|12_News_Intelligence_Journal]] using the templates in their respective `Templates/` folders.
4. To give the latest desk state to a fresh LLM session, paste [[Current_Context_For_LLM]] into the prompt.

## Top-level map

- [[00_System_Overview/What_is_crypto_ai_desk|00 — System Overview]]
- [[01_Market_Regime/Market_Regime_Overview|01 — Market Regime]]
- [[02_Trading_Modes/Trading_Modes_Overview|02 — Trading Modes]]
- [[03_Risk_Management/Risk_Management_Overview|03 — Risk Management]]
- [[04_Indicators_and_Metrics/Indicators_Overview|04 — Indicators & Metrics]]
- [[05_News_Telegram_Catalysts_Sentiment/News_System_Overview|05 — News / Telegram / Catalysts / Sentiment]]
- [[06_Sectors_and_Narratives/Sector_Overview|06 — Sectors & Narratives]]
- [[07_Exchange_Logic/Exchange_Overview|07 — Exchange Logic]]
- [[08_Agents/Agents_Overview|08 — Agents]]
- [[09_Scoring_System/Scoring_Overview|09 — Scoring System]]
- [[10_Trade_Idea_Format/Trade_Idea_Template|10 — Trade Idea Format]]
- [[11_Trade_Journal/README|11 — Trade Journal]]
- [[12_News_Intelligence_Journal/README|12 — News Intelligence Journal]]
- [[13_Debugging_and_Improvement/Why_No_Trades|13 — Debugging & Improvement]]
- [[14_Project_Commands/Daily_Commands|14 — Project Commands]]
- [[15_LLM_Context/Current_Context_For_LLM|15 — LLM Context]]

## Ground truth files in the project

If anything in this vault conflicts with the code, **the code wins** and the vault should be corrected. Authoritative sources are:

- `config/scoring.yaml` — weights, multipliers, caps, thresholds.
- `config/universe.yaml` — modes, exchange list, liquidity floors, discovery overrides.
- `config/exchanges.yaml` — per-venue role, trust, weight, aliases.
- `config/watchlist.yaml` — base watchlist + narrative-to-symbol mapping.
- `config/sources.yaml` — RSS feeds, macro keywords.
- `config/notifications.yaml` — Telegram bot token + chat_id + cooldown.
- `src/agents/` — all 22 agents.
- `src/cli.py` — every CLI command surface.

## Implementation status legend used in this vault

Every file ends with an `Implemented status` block. Possible values:

- **Implemented** — present in code; behavior matches description.
- **Partially implemented** — present but limited; specifics noted.
- **Recommended** — not in code, would improve the desk.
- **Unknown** — needs code re-inspection before trusting.

The folder structure intentionally allows pages for things that **do not yet exist** in the system (e.g. `Long_Term_Mode.md`, `VWAP.md`) so the gap is visible.
