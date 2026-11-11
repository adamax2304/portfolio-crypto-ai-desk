# 📌 Trade History — completed signals with outcomes

_Refreshed: **2026-11-11 23:42 EEST**. Last 80 unique setups (deduped) from `proposed_signals` × `signal_outcomes`._

Outcome legend: 🟢 TP1 hit · 🟢🟢 TP2 hit · 🟢🟢🟢 TP3 hit · 🔴 stop-loss · ⚪ expired · ⚫ missed (no entry).

---

## 📊 Aggregate stats — counted as UNIQUE setups (the honest view)

A **unique setup** = one row per ``(asset_class, symbol, mode, direction, calendar day)``. Multiple signal_ids that share that tuple are collapsed into one outcome — see footer for why this matters.

| Class | Unique trades | Wins | Losses | WR | Avg R | Raw signal_ids (inflated) |
|-------|--------------:|-----:|-------:|---:|------:|--------------------------:|
| crypto | **2651** | 494 | 1203 | 19% | -0.02 | 2659 |
| stocks | **8728** | 589 | 887 | 7% | -0.00 | 10835 |

---

## 📜 History (most recent 80 unique setups)

| | Symbol | Dir | Mode | Tier | Score | Outcome | Final R | MFE / MAE | Date |
|---|--------|-----|------|------|------:|---------|---------|-----------|------|
| • | `PEPE/USDT` | short | intraday | **B** | 65.4 | win | +2.00R | MFE +2.58R / MAE +0.00R | 2026-11-11 |
| ⚪ | `AMD` | long | intraday | **C** | 56.3 | expired | +0.00R | MFE +0.95R / MAE -0.34R | 2026-11-11 |
| • | `AMGN` | short | intraday | **C** | 58.3 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-11-11 |
| ⚪ | `ANET` | long | intraday | **C** | 69.4 | expired | +0.00R | MFE +0.02R / MAE -0.49R | 2026-11-11 |
| • | `ARM` | long | intraday | **B** | 69.0 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-10-29 |
| • | `ASML` | long | intraday | **C** | 56.3 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-11-11 |
| • | `CLSK` | long | intraday | **C** | 55.0 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-11-11 |
| • | `COIN` | short | intraday | **B** | 78.8 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-10-23 |
| • | `COST` | short | intraday | **B** | 85.2 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-08-20 |
| • | `CRCL` | long | intraday | **B** | 93.6 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-08-19 |
| • | `CRWD` | long | intraday | **C** | 57.8 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-11-11 |
| • | `CSCO` | long | intraday | **B** | 86.9 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-10-05 |
| • | `CSCO` | long | intraday | **B** | 76.9 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-10-09 |
| • | `DDOG` | short | intraday | **B** | 76.2 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-09-01 |
| • | `DDOG` | short | intraday | **B** | 84.2 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-10-29 |
| • | `DELL` | short | intraday | **B** | 81.6 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-10-22 |
| • | `ETN` | long | intraday | **C** | 59.6 | loss | -1.00R | MFE +0.41R / MAE -1.13R | 2026-11-11 |
| • | `GOOGL` | long | intraday | **C** | 54.6 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-11-11 |
| ⚪ | `HUT` | long | intraday | **C** | 54.6 | expired | +0.00R | MFE +0.46R / MAE -0.54R | 2026-11-11 |
| • | `LLY` | long | intraday | **A** | 97.0 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-10-22 |
| • | `MAR` | long | intraday | **B** | 82.5 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-10-21 |
| • | `MRVL` | short | intraday | **B** | 85.5 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-11-02 |
| • | `MSTR` | long | intraday | **B** | 76.8 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-10-21 |
| • | `NET` | long | intraday | **C** | 69.4 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-11-11 |
| ⚪ | `NFLX` | long | intraday | **C** | 54.6 | expired | +0.00R | MFE +0.73R / MAE -0.78R | 2026-11-11 |
| • | `NFLX` | short | intraday | **B** | 65.2 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-10-20 |
| • | `NVDA` | long | intraday | **B** | 68.2 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-09-04 |
| ⚪ | `ORCL` | long | intraday | **C** | 70.3 | expired | +0.00R | MFE +0.04R / MAE -1.29R | 2026-11-11 |
| ⚪ | `PLTR` | long | intraday | **C** | 52.5 | expired | +0.00R | MFE +0.44R / MAE -0.21R | 2026-11-11 |
| ⚪ | `QQQ` | long | intraday | **C** | 65.3 | expired | +0.00R | MFE +0.33R / MAE -0.77R | 2026-11-11 |
| • | `REGN` | long | intraday | **A** | 95.6 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-11-11 |
| • | `RIOT` | long | intraday | **C** | 68.8 | win | +1.00R | MFE +2.07R / MAE -0.24R | 2026-11-11 |
| • | `RIOT` | short | intraday | **B** | 74.9 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-09-25 |
| • | `SMCI` | long | intraday | **C** | 55.6 | not_triggered | +0.00R | MFE +0.00R / MAE +0.00R | 2026-11-11 |
| • | `SMH` | long | intraday | **C** | 54.6 | loss | -1.00R | MFE +0.28R / MAE -1.03R | 2026-11-11 |
| • | `SOFI` | long | intraday | **C** | 88.7 | loss | -1.00R | MFE +0.03R / MAE -1.07R | 2026-11-11 |
| • | `TSLA` | long | intraday | **C** | 75.7 | win | +2.00R | MFE +3.41R / MAE +0.00R | 2026-11-10 |
| • | `TSLA` | long | intraday | **C** | 86.1 | win | +2.00R | MFE +3.41R / MAE +0.00R | 2026-11-11 |
| • | `TSM` | long | intraday | **C** | 57.7 | win | +2.00R | MFE +3.41R / MAE +0.00R | 2026-11-11 |
| ⚪ | `VRT` | long | intraday | **C** | 68.2 | expired | +0.00R | MFE +0.10R / MAE -1.05R | 2026-11-11 |
| • | `XLK` | long | intraday | **C** | 54.6 | loss | -1.00R | MFE +0.34R / MAE -1.04R | 2026-11-11 |
| • | `UNI/USDT` | short | intraday | **B** | 66.8 | loss | -1.00R | MFE +0.92R / MAE -1.21R | 2026-11-11 |
| • | `ZEC/USDT` | short | intraday | **B** | 67.3 | loss | -1.00R | MFE +0.71R / MAE -1.07R | 2026-11-11 |
| • | `AFRM` | short | intraday | **C** | 63.7 | win | +1.00R | MFE +1.04R / MAE -0.88R | 2026-11-05 |
| • | `AMGN` | short | intraday | **C** | 74.9 | win | +1.00R | MFE +1.47R / MAE -0.93R | 2026-10-02 |
| • | `AMGN` | short | intraday | **C** | 82.0 | win | +1.00R | MFE +1.98R / MAE -0.46R | 2026-11-05 |
| • | `AMGN` | short | intraday | **C** | 63.0 | win | +1.00R | MFE +1.75R / MAE -0.41R | 2026-11-06 |
| • | `ANET` | long | intraday | **C** | 76.6 | win | +2.00R | MFE +2.77R / MAE -0.23R | 2026-09-25 |
| • | `ANET` | short | intraday | **C** | 81.3 | win | +1.00R | MFE +1.10R / MAE -0.39R | 2026-10-30 |
| • | `APP` | long | intraday | **C** | 99.4 | win | +1.00R | MFE +2.50R / MAE -0.01R | 2026-09-21 |
| • | `APP` | short | intraday | **C** | 72.7 | win | +1.00R | MFE +2.48R / MAE -0.04R | 2026-10-21 |
| • | `ASML` | long | intraday | **C** | 56.1 | win | +2.00R | MFE +3.00R / MAE -0.37R | 2026-09-20 |
| • | `ASML` | long | intraday | **C** | 64.7 | win | +2.00R | MFE +3.00R / MAE -0.37R | 2026-09-21 |
| • | `ASML` | long | intraday | **C** | 59.5 | win | +1.00R | MFE +1.21R / MAE -0.54R | 2026-10-29 |
| • | `ASML` | short | intraday | **C** | 81.4 | win | +2.00R | MFE +2.26R / MAE -0.23R | 2026-10-30 |
| • | `AVGO` | long | intraday | **C** | 84.4 | not_triggered | +0.00R | MFE — / MAE — | 2026-09-22 |
| • | `AVGO` | short | intraday | **C** | 89.3 | win | +1.00R | MFE +1.70R / MAE -0.13R | 2026-10-30 |
| • | `AXP` | long | intraday | **C** | 51.5 | win | +1.00R | MFE +2.08R / MAE -0.08R | 2026-10-11 |
| • | `AXP` | long | intraday | **C** | 51.5 | win | +1.00R | MFE +2.08R / MAE -0.08R | 2026-10-12 |
| • | `AXP` | long | intraday | **C** | 61.2 | not_triggered | +0.00R | MFE — / MAE — | 2026-10-22 |
| • | `AXP` | long | intraday | **C** | 92.8 | win | +1.00R | MFE +0.92R / MAE -0.68R | 2026-10-28 |
| • | `BAC` | short | intraday | **C** | 85.6 | win | +1.00R | MFE +1.25R / MAE -0.89R | 2026-09-28 |
| • | `BIIB` | long | intraday | **C** | 61.7 | win | +1.00R | MFE +0.36R / MAE -0.78R | 2026-10-30 |
| • | `BIIB` | long | intraday | **C** | 76.0 | win | +1.00R | MFE +0.61R / MAE -0.08R | 2026-11-04 |
| • | `BIIB` | short | intraday | **C** | 71.7 | win | +1.00R | MFE +0.87R / MAE -0.18R | 2026-09-15 |
| • | `BIIB` | short | intraday | **C** | 90.2 | win | +1.00R | MFE +1.26R / MAE -1.35R | 2026-10-01 |
| • | `BIIB` | short | intraday | **C** | 78.7 | win | +1.00R | MFE +1.31R / MAE -0.86R | 2026-10-02 |
| • | `BIIB` | short | intraday | **C** | 85.1 | win | +1.00R | MFE +0.93R / MAE -0.15R | 2026-11-05 |
| • | `BKNG` | short | intraday | **C** | 76.9 | win | +1.00R | MFE +0.66R / MAE -0.27R | 2026-10-23 |
| • | `BKNG` | short | intraday | **C** | 59.9 | win | +1.00R | MFE +1.57R / MAE -0.13R | 2026-10-30 |
| • | `BLK` | long | intraday | **C** | 55.0 | win | +1.00R | MFE +2.04R / MAE -1.10R | 2026-09-24 |
| • | `BLK` | long | intraday | **C** | 55.0 | win | +1.00R | MFE +2.04R / MAE -1.10R | 2026-09-25 |
| • | `BX` | long | intraday | **C** | 64.7 | win | +1.00R | MFE +1.18R / MAE -0.98R | 2026-11-02 |
| • | `BX` | short | intraday | **C** | 85.5 | win | +1.00R | MFE +1.28R / MAE -0.48R | 2026-10-13 |
| • | `CLSK` | long | intraday | **C** | 81.0 | win | +1.00R | MFE +1.78R / MAE +0.00R | 2026-09-20 |
| • | `CLSK` | long | intraday | **C** | 76.3 | win | +1.00R | MFE +1.78R / MAE +0.00R | 2026-09-21 |
| • | `CLSK` | short | intraday | **C** | 59.5 | win | +1.00R | MFE +1.43R / MAE -0.15R | 2026-09-15 |
| • | `CLSK` | short | intraday | **C** | 87.4 | win | +2.00R | MFE +3.36R / MAE -0.36R | 2026-10-01 |
| • | `CLSK` | short | intraday | **C** | 64.0 | win | +2.00R | MFE +3.51R / MAE +0.00R | 2026-10-07 |
| • | `CLSK` | short | intraday | **C** | 80.2 | win | +1.00R | MFE +1.94R / MAE -0.10R | 2026-10-30 |

---

## Field meanings

- **Unique trades** — distinct setups (symbol × mode × direction × day). The fair count.
- **Raw signal_ids (inflated)** — what `proposed_signals` actually holds. Inflated because every 2h cycle re-registers the same setup with a new id (see diagnostic note below).
- **Final R** — realized R-multiple. Positive = winner, negative = stopped.
- **MFE / MAE** — maximum favourable / adverse excursion in R units while the trade was open. Even a winning trade with a large MAE indicates poor entry timing.
- **Missed (no entry)** = system fired a setup, but price never reached the entry zone before expiry → no trade.

For per-signal detail, see `11_Trade_Journal/Signal_Performance/Signal_Logs/` (one Markdown file per signal).

---

## ⚠️ Diagnostic note — why "Unique trades" ≠ "Raw signal_ids"

The default scheduler refreshes intraday reports every 2 hours. Each cycle generates new signal_ids for the SAME setup because:

1. The deterministic `signal_id_for()` hash includes `report_id` — which is unique per cycle.
2. Entry / stop floats slightly differ each cycle as fresh OHLCV recomputes ATR-based zones.

Result: one logical trade idea like `AAPL intraday long 2026-05-27` can appear as **15 separate signal_ids** in the DB. The dashboard already corrects for this by collapsing by ``(symbol, mode, direction, day)``. The underlying registry should also be fixed in a future sprint so `proposed_signals` itself stops duplicating — but the deduplication here gives an immediately honest read.

_File generated automatically by `scripts/refresh_obsidian_dashboard.py`._
