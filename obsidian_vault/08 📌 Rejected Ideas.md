# 📌 Rejected Ideas — what the system declined and why

_Refreshed: **2026-11-11 16:51 EEST** · Last 48h. Source: `rejected_ideas` SQLite._

Total rejections in window: **145**. This view explains why otherwise interesting symbols never made it to A/B tier — useful for spotting filter strictness, regime mismatches, or override candidates worth a manual Opus look.

---

## 🔢 Top rejection reasons (last 48h)

| Primary reason | Count |
|----------------|------:|
| crypto intraday long against bearish-trend regime (audit cap) | 55 |
| Derivatives data unavailable for this symbol. | 18 |
| short squeeze risk → capped to C: high_upper_wick_short_squeeze_risk | 15 |
| short squeeze risk → capped to C: thin_liquidity_short_squeeze_risk, no_derivatives_thin_short | 12 |
| short squeeze risk → capped to C: thin_liquidity_short_squeeze_risk | 6 |
| RS-leader long vs bearish tape (counter-trend, capped B) | 6 |
| Catalyst risk event reduces setup quality. | 5 |
| short squeeze risk → capped to C: thin_liquidity_short_squeeze_risk (+exhaustion) | 4 |
| No fresh verified catalyst detected. | 4 |
| short squeeze risk → capped to C: thin_liquidity_short_squeeze_risk, high_upper_wick_short_squeeze_risk | 3 |
| Volume is below average; breakout confirmation is weak. | 3 |
| Price is more than 2 ATR from EMA20; do not chase. | 3 |

---

## 🪙 Crypto rejections (top 25 by score)

| Symbol | Dir | Score | Primary reason | When |
|--------|-----|------:|----------------|------|
| `PENGU/USDT` | short | 49.9 | short squeeze risk → capped to C: thin_liquidity_short_squeeze_risk | 2026-11-10 11:03 |
| `ENA/USDT` | short | 49.8 | Volume is below average; breakout confirmation is weak. | 2026-11-10 11:03 |
| `RAY/USDT` | short | 49.2 | short squeeze risk → capped to C: thin_liquidity_short_squeeze_risk, no_derivatives_thin_s | 2026-11-10 16:23 |
| `0G/USDT` | long | 49.1 | RS-leader long vs bearish tape (counter-trend, capped B) | 2026-11-10 23:23 |
| `PEPE/USDT` | long | 48.9 | RS-leader long vs bearish tape (counter-trend, capped B) | 2026-11-10 11:03 |
| `RAY/USDT` | short | 48.7 | short squeeze risk → capped to C: thin_liquidity_short_squeeze_risk, no_derivatives_thin_s | 2026-11-11 11:02 |
| `ZRO/USDT` | short | 48.7 | short squeeze risk → capped to C: thin_liquidity_short_squeeze_risk, high_upper_wick_short | 2026-11-10 12:57 |
| `UNI/USDT` | short | 48.5 | short squeeze risk → capped to C: high_upper_wick_short_squeeze_risk | 2026-11-10 04:50 |
| `HBAR/USDT` | short | 48.5 | short squeeze risk → capped to C: thin_liquidity_short_squeeze_risk | 2026-11-10 01:38 |
| `RAY/USDT` | short | 48.4 | short squeeze risk → capped to C: thin_liquidity_short_squeeze_risk, no_derivatives_thin_s | 2026-11-10 12:57 |
| `ETH/USDT` | short | 48.2 | short squeeze risk → capped to C: high_upper_wick_short_squeeze_risk | 2026-11-10 19:55 |
| `BERA/USDT` | short | 48.0 | short squeeze risk → capped to C: thin_liquidity_short_squeeze_risk | 2026-11-10 23:23 |
| `RAY/USDT` | short | 47.8 | short squeeze risk → capped to C: thin_liquidity_short_squeeze_risk, no_derivatives_thin_s | 2026-11-10 11:03 |
| `ASTER/USDT` | short | 47.8 | short squeeze risk → capped to C: thin_liquidity_short_squeeze_risk | 2026-11-09 19:37 |
| `RAY/USDT` | short | 47.0 | short squeeze risk → capped to C: thin_liquidity_short_squeeze_risk, no_derivatives_thin_s | 2026-11-11 14:02 |
| `ETH/USDT` | short | 47.0 | Catalyst risk event reduces setup quality. | 2026-11-11 11:02 |
| `ADA/USDT` | short | 46.7 | short squeeze risk → capped to C: thin_liquidity_short_squeeze_risk, no_derivatives_thin_s | 2026-11-11 11:02 |
| `BTC/USDT` | short | 46.7 | short squeeze risk → capped to C: high_upper_wick_short_squeeze_risk | 2026-11-10 19:55 |
| `AVAX/USDT` | long | 46.7 | RS-leader long vs bearish tape (counter-trend, capped B) | 2026-11-10 07:57 |
| `ETH/USDT` | short | 46.6 | Catalyst risk event reduces setup quality. | 2026-11-10 23:23 |
| `BTC/USDT` | short | 46.4 | short squeeze risk → capped to C: high_upper_wick_short_squeeze_risk | 2026-11-10 12:57 |
| `MSTRB/USDT` | short | 46.3 | short squeeze risk → capped to C: high_upper_wick_short_squeeze_risk, no_derivatives_thin_ | 2026-11-09 19:37 |
| `BTC/USDT` | short | 46.2 | short squeeze risk → capped to C: high_upper_wick_short_squeeze_risk | 2026-11-10 04:50 |
| `ETH/USDT` | short | 46.0 | short squeeze risk → capped to C: high_upper_wick_short_squeeze_risk | 2026-11-09 19:37 |
| `ETH/USDT` | short | 45.8 | short squeeze risk → capped to C: high_upper_wick_short_squeeze_risk | 2026-11-09 16:11 |


## 📈 Stocks rejections (top 25 by score)

_No stocks rejections in last 48h._


---

## How to read this

- **Score ≥ 50 with regime-mismatch reason** = the setup itself is technically OK, only blocked because the broader regime contradicts it. These are the canonical "wait for regime flip" candidates.
- **Score ≥ 50 with "no fresh verified catalyst" reason** = manual Opus review can override if news landed late. The 6×/day auto-Opus picks up these cases as override candidates per the routine prompt.
- **"Derivatives data unavailable"** = crypto symbol without good futures data — usually a small alt or stocks-only ticker. Often safe to ignore.

_File generated automatically by `scripts/refresh_obsidian_dashboard.py`._
