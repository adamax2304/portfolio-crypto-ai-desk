# 📌 Active Signals — waiting / triggered (B & A tier)

_Refreshed: **2026-11-11 23:42 EEST**. Source: `proposed_signals` SQLite, last 72h, dedup by (symbol, mode, direction)._

Status meanings: `waiting_for_entry` = price has not reached the entry zone yet; `triggered` = price entered the zone; `tp1_hit` / `tp2_hit` = partial take-profit reached.

---

## 🪙 Crypto

| Tier | Symbol | Dir | Mode | Score | Status | Entry | SL | TP1 | RR | Narrative |
|------|--------|-----|------|------:|--------|-------|----|-----|----|-----------|
| **B** | `PEPE/USDT` | short | intraday | 65.4 | tp2_hit | 0.0000 – 0.0000 | 0.0000 | 0.0000 | 1 | — |


## 📈 Stocks

_No active stocks signals._


---

## How to use this table

1. **Sort priority:** A-tier on top, then B-tier by score.
2. **`waiting_for_entry`** = the bot watches the price and will fire a Telegram alert when it approaches the entry zone (every 5 min for crypto, every 10 min for stocks during US RTH).
3. **`triggered`** = price has already entered the zone. Decide manually whether to honour the setup (system does not auto-trade).
4. **Score < 80** = B-tier (one or two confirmations missing). Use these for smaller-size positions or as watchlist.

Total active rows: **1** (crypto: 1, stocks: 0).

_File generated automatically by `scripts/refresh_obsidian_dashboard.py`._
