# 📌 Dashboard — crypto-ai-desk

_Last refreshed: **2026-11-11 23:42 EEST**_

This is the daily landing page. Pinned tabs (📌) refresh on every scheduler cycle.

---

## 🔥 Live trade desk

- [[11 📌 Trading Desk Current State]] — **single-screen sweep**: system health + open paper trades + last 5 closures + today's events + top risks + mode routing + performance + manual checklist
- [[01 📌 Active Signals]] — current B/A signals awaiting entry or already triggered
- [[02 📌 Trade History]] — completed signals with outcomes (wins/losses/missed)
- [[03 📌 Todays Catalysts]] — fresh catalyst events + narrative baskets
- [[06 📌 Telegram Feed]] — last 50 Telegram-channel headlines (lookonchain, BWEnews, bloomberg…)

## 📋 Reports & reviews

- [[04 📌 Latest Reports]] — most-recent scalp / intraday / stocks reports
- [[05 📌 Opus Auto Reviews]] — auto-generated enriched-reviews (6×/day)
- [[Daily_Reviews]] — daily Obsidian summaries

## ⚙️ System health

- [[07 📌 Schedule Status]] — scheduler + Telegram collector + watchlist monitor status

## 🔬 Diagnostic & performance

- [[08 📌 Rejected Ideas]] — what the system declined and why (override candidates)
- [[09 📌 Macro Risk Heatmap]] — risk-on / risk-off score + headlines
- [[10 📌 Performance by Mode]] — signal-stats breakdown per mode and tier

---

## Existing knowledge folders

| # | Folder | What it contains |
|---|--------|------------------|
| 00 | [[00_System_Overview]] | Principles, glossary, LLM ops |
| 01 | [[01_Market_Regime]] | Regime classification |
| 02 | [[02_Trading_Modes]] | Scalp / intraday / swing / invest |
| 03 | [[03_Risk_Management]] | Position sizing, stops, R-multiple |
| 04 | [[04_Indicators_and_Metrics]] | RS, momentum, volume |
| 05 | [[05_News_Telegram_Catalysts_Sentiment]] | News sources, catalyst classes |
| 06 | [[06_Sectors_and_Narratives]] | Sector rotation, narrative baskets |
| 07 | [[07_Exchange_Logic]] | Multi-exchange fusion |
| 08 | [[08_Agents]] | Agent architecture |
| 09 | [[09_Scoring_System]] | Scoring weights + tiers |
| 10 | [[10_Trade_Idea_Format]] | TradeIdea template |
| 11 | [[11_Trade_Journal]] | Trade journal (legacy folder, populated by `review-day`) |
| 12 | [[12_News_Intelligence_Journal]] | News intelligence |
| 13 | [[13_Debugging_and_Improvement]] | System debugging notes |
| 14 | [[14_Project_Commands]] | CLI commands reference |
| 15 | [[15_LLM_Context]] | LLM prompts + checklists |
| 16 | [[16_Stocks]] | Stocks-specific docs |

---

## ⚠️ Safety contract (always)

- No auto-trade
- No scoring / threshold / agent / strategy changes
- The 6×/day Opus auto-reviews run via Claude `routines` (scheduled-tasks)
- Telegram alerts only fire on B/A tier promotions (with 30–45 min cooldown per PART 2)

_File generated automatically by `scripts/refresh_obsidian_dashboard.py`._
