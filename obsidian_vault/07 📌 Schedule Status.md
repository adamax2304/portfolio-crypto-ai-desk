# 📌 Schedule Status — system health

_Refreshed: **2026-11-11 16:51 EEST**_

---

## ⚙️ Running components (expected)

| Process | Purpose |
|---------|---------|
| `scripts/run_default_market_schedule.py` | 2-hour cycle scheduler (12 cycles/day): scalp + intraday + (weekday) stocks-intraday + background monitors |
| `src.cli monitor-watchlist` | Crypto watchlist monitor — tickes every 5 min, alerts on tier upgrades |
| `src.cli stocks-monitor-session` | Stocks watchlist monitor — tickes every 10 min during US RTH only |
| `scripts/run_telegram_collector.py` | 18-channel Telegram listener |
| Claude routine `opus-enriched-review-4h` | 6×/day auto-Opus enriched reviews (00:30 / 04:30 / 08:30 / 12:30 / 16:30 / 20:30 EEST) |

---

## 🟢 Today's activity (2026-11-11)

- Long-horizon (swing/invest) ran already today: **no — will run on next cycle**
- Crypto watchlist Telegram alerts in last 24h: **2**
- Stocks Telegram alerts in last 24h: **10**
- Telegram-channel news ingested in last 24h: **1244**

## 📜 Recent scheduler cycles

- [cycle_01_12-55_summary.md](../data/scheduled_runs/2026-11-11_default_schedule/cycle_01_12-55_summary.md) · _11:59 UTC_

---

## How to operate

| Action | Command |
|--------|---------|
| Restart scheduler | `py -3 scripts/run_default_market_schedule.py --hours 24 --interval-hours 2 --send-telegram` |
| Restart TG collector | `py -3 scripts/run_telegram_collector.py` |
| Manual single cycle (test) | `py -3 scripts/run_default_market_schedule.py --run-once --dry-run` |
| Check scheduler log | `data/scheduled_runs/<today>_default_schedule/scheduler.log` |
| List Claude routines | (Claude Desktop → left sidebar → Scheduled) |

---

## Safety contract reminder

- Scheduler never auto-trades.
- Scheduler never invokes Opus / LLM (auto-LLM happens via the Claude routine only, which the user explicitly opted in).
- `news_trader/` directory is READ-ONLY.

_File generated automatically by `scripts/refresh_obsidian_dashboard.py`._
