# Stocks AI Desk Report

Date: 2026-05-25
Mode: intraday
Asset class: stocks
Market session: regular session
Data freshness: 2026-05-25 14:12 UTC

## 0. Data Coverage
- Indices: ok=10, fail=0
- Sector ETFs: ok=12, fail=0
- Symbols: ok=84, fail=0
- Earnings events tracked: 18
- Earnings lookup failed for: SPY, QQQ, IWM, DIA, SMH, XLK, XLF, XLE, XLY, XLV

## 1. Stock Market Regime
- Label: **bullish**
- Bias: long
- Risk-on: True
- VIX: 16.64
- Breadth above EMA20: 100.0%
- Breadth above EMA50: 100.0%
- Explanation: 4/4 indices trending up; breadth_above_ema20=1.0; VIX=16.64

### Index Trends
- SPY: trend=uptrend, 5d=+0.88%, 20d=+4.44%
- QQQ: trend=uptrend, 5d=+1.21%, 20d=+8.08%
- IWM: trend=uptrend, 5d=+2.71%, 20d=+3.06%
- DIA: trend=uptrend, 5d=+2.17%, 20d=+2.83%

## 2. Sector Rotation
- Benchmark (SPY) 20d return: +4.44%

### Strongest Sectors
- semiconductors (SMH): status=strong, RS vs SPY 20d=+9.36%, 20d return=+13.80%
- technology (XLK): status=strong, RS vs SPY 20d=+8.15%, 20d return=+12.59%
- energy (XLE): status=mixed, RS vs SPY 20d=+0.17%, 20d return=+4.61%

### Weakest Sectors
- materials (XLB): status=weak, RS vs SPY 20d=-7.58%, 20d return=-3.14%
- utilities (XLU): status=weak, RS vs SPY 20d=-6.24%, 20d return=-1.80%
- industrials (XLI): status=mixed, RS vs SPY 20d=-4.85%, 20d return=-0.41%

## 3. Earnings / Event Risk

## 4. News / Catalysts
### AAPL
- AAPL announces share buyback (test_source, 2026-05-25)
### NVDA
- NVDA beats earnings (test_source, 2026-05-25)
### COIN
- Coinbase reports record revenue (COIN) (test_source, 2026-05-25)
### MSTR
- MicroStrategy buys more (MSTR) (test_source, 2026-05-25)

## 5. Top Candidates

| Symbol | Direction | Tier | Score | Confidence | Risk Penalty |
|--------|-----------|------|-------|------------|--------------|
| AAPL | long | A | 88.64 | high | -4.0 |
| LLY | long | A | 80.33 | high | -4.0 |
| AMD | long | B | 78.77 | high | -4.0 |
| XLK | long | B | 74.91 | medium | -4.0 |
| SMCI | long | B | 74.26 | medium | -4.0 |
| SMH | long | B | 73.93 | medium | -4.0 |
| UNH | long | B | 68.59 | medium | -4.0 |
| TSLA | long | B | 67.3 | medium | -4.0 |
| QQQ | long | C | 64.77 | medium | -4.0 |
| IWM | long | C | 56.47 | medium | -4.0 |
| SPY | long | C | 54.12 | low | -4.0 |
| XLV | long | C | 52.46 | low | -4.0 |
| MSTR | short | C | 51.54 | medium | -12.0 |
| DIA | long | C | 50.27 | low | -4.0 |
| COIN | short | rejected | 49.61 | medium | -12.0 |

## 6. Trade Ideas (A/B-tier)

### Idea #1 — A AAPL long
- Score: 88.64
- Confidence: high
- Risk level: low
- Timeframe: 15m/1h
- Thesis: AAPL long (intraday) | trend=uptrend | RS=leader | regime=bullish | earnings:unknown
- Evidence:
  - RR to TP1 below 1.5 (1.0)
  - above prev day high
  - RS vs SPY (20d): +9.49%
  - RS vs sector ETF (20d): +1.34%
  - 1 news catalyst(s) in lookback window
- Entry: long zone 308.0356–308.8800
- Invalidation: close beyond 306.3468
- Targets: TP1: 311.4132, TP2: 313.1020, TP3: 315.6352
- Counter-thesis:
  - earnings risk: unknown
- Avoid:
  - do not chase if price is > 2 ATR from planned entry
  - do not enter against a clear SPY breakdown

### Idea #2 — A LLY long
- Score: 80.33
- Confidence: high
- Risk level: low
- Timeframe: 15m/1h
- Thesis: LLY long (intraday) | trend=uptrend | RS=leader | regime=bullish | earnings:unknown
- Evidence:
  - RR to TP1 below 1.5 (1.0)
  - above prev day high
  - RS vs SPY (20d): +16.04%
  - RS vs sector ETF (20d): +16.52%
- Entry: long zone 1060.8258–1065.6500
- Invalidation: close beyond 1051.1775
- Targets: TP1: 1080.1226, TP2: 1089.7710, TP3: 1104.2435
- Counter-thesis:
  - earnings risk: unknown
- Avoid:
  - do not chase if price is > 2 ATR from planned entry
  - do not enter against a clear SPY breakdown

### Idea #3 — B AMD long
- Score: 78.77
- Confidence: high
- Risk level: low
- Timeframe: 15m/1h
- Thesis: AMD long (intraday) | trend=uptrend | RS=leader | regime=bullish | earnings:unknown
- Evidence:
  - RR to TP1 below 1.5 (1.0)
  - above prev day high
  - RS vs SPY (20d): +29.98%
  - RS vs sector ETF (20d): +20.62%
- Entry: long zone 463.3704–467.5100
- Invalidation: close beyond 455.0912
- Targets: TP1: 479.9289, TP2: 488.2081, TP3: 500.6269
- Counter-thesis:
  - earnings risk: unknown
- Avoid:
  - do not chase if price is > 2 ATR from planned entry
  - do not enter against a clear SPY breakdown

### Idea #4 — B XLK long
- Score: 74.91
- Confidence: medium
- Risk level: low
- Timeframe: 15m/1h
- Thesis: XLK long (intraday) | trend=uptrend | RS=leader | regime=bullish | earnings:unknown
- Evidence:
  - RR to TP1 below 1.5 (1.0)
  - above prev day high
  - RS vs SPY (20d): +8.15%
- Entry: long zone 179.7498–180.3400
- Invalidation: close beyond 178.5693
- Targets: TP1: 182.1107, TP2: 183.2911, TP3: 185.0618
- Counter-thesis:
  - earnings risk: unknown
- Avoid:
  - do not chase if price is > 2 ATR from planned entry
  - do not enter against a clear SPY breakdown

### Idea #5 — B SMCI long
- Score: 74.26
- Confidence: medium
- Risk level: low
- Timeframe: 15m/1h
- Thesis: SMCI long (intraday) | trend=uptrend | RS=leader | regime=bullish | earnings:unknown
- Evidence:
  - RR to TP1 below 1.5 (1.0)
  - above prev day high
  - RS vs SPY (20d): +17.91%
- Entry: long zone 35.2480–35.5800
- Invalidation: close beyond 34.5839
- Targets: TP1: 36.5761, TP2: 37.2402, TP3: 38.2364
- Counter-thesis:
  - earnings risk: unknown
- Avoid:
  - do not chase if price is > 2 ATR from planned entry
  - do not enter against a clear SPY breakdown

### Idea #6 — B SMH long
- Score: 73.93
- Confidence: medium
- Risk level: low
- Timeframe: 15m/1h
- Thesis: SMH long (intraday) | trend=uptrend | RS=leader | regime=bullish | earnings:unknown
- Evidence:
  - RR to TP1 below 1.5 (1.0)
  - above prev day high
  - RS vs SPY (20d): +9.36%
- Entry: long zone 573.4211–575.9900
- Invalidation: close beyond 568.2832
- Targets: TP1: 583.6968, TP2: 588.8346, TP3: 596.5414
- Counter-thesis:
  - earnings risk: unknown
- Avoid:
  - do not chase if price is > 2 ATR from planned entry
  - do not enter against a clear SPY breakdown

### Idea #7 — B UNH long
- Score: 68.59
- Confidence: medium
- Risk level: low
- Timeframe: 15m/1h
- Thesis: UNH long (intraday) | trend=uptrend | RS=follower | regime=bullish | earnings:unknown
- Evidence:
  - RR to TP1 below 1.5 (1.0)
  - above prev day high
  - RS vs SPY (20d): +5.01%
  - RS vs sector ETF (20d): +5.49%
- Entry: long zone 387.3619–388.5800
- Invalidation: close beyond 384.9258
- Targets: TP1: 392.2342, TP2: 394.6704, TP3: 398.3246
- Counter-thesis:
  - earnings risk: unknown
- Avoid:
  - do not chase if price is > 2 ATR from planned entry
  - do not enter against a clear SPY breakdown

### Idea #8 — B TSLA long
- Score: 67.30
- Confidence: medium
- Risk level: low
- Timeframe: 15m/1h
- Thesis: TSLA long (intraday) | trend=uptrend | RS=leader | regime=bullish | earnings:unknown
- Evidence:
  - RR to TP1 below 1.5 (1.0)
  - RS vs SPY (20d): +8.77%
  - RS vs sector ETF (20d): +12.80%
- Entry: long zone 423.3290–425.9482
- Invalidation: close beyond 418.0905
- Targets: TP1: 433.8059, TP2: 439.0443, TP3: 446.9020
- Counter-thesis:
  - earnings risk: unknown
- Avoid:
  - do not chase if price is > 2 ATR from planned entry
  - do not enter against a clear SPY breakdown

## 7. Watchlist (C-tier)
- QQQ (long): score 64.77, penalty -4.0
- IWM (long): score 56.47, penalty -4.0
- SPY (long): score 54.12, penalty -4.0
- XLV (long): score 52.46, penalty -4.0
- MSTR (short): score 51.54, penalty -12.0
- DIA (long): score 50.27, penalty -4.0

## 8. Rejected / Not Ready
- COIN (short): 49.61 — short_in_bullish_regime, rr_below_1.5
- JPM (long): 45.67 — weak_relative_strength, rr_below_1.5
- GOOGL (short): 42.69 — short_in_bullish_regime, rr_below_1.5
- XLF (long): 42.67 — weak_relative_strength, rr_below_1.5
- XLY (long): 41.83 — weak_relative_strength, rr_below_1.5
- NVDA (short): 41.33 — both_index_and_sector_contradict
- PLTR (long): 41.05 — weak_relative_strength, rr_below_1.5
- NFLX (short): 39.61 — short_in_bullish_regime, rr_below_1.5
- XOM (short): 38.4 — short_in_bullish_regime, rr_below_1.5
- META (long): 35.32 — long_in_weak_sector, weak_relative_strength, rr_below_1.5
- XLE (no_trade): 32.05 — no_directional_setup
- AMZN (no_trade): 28.65 — no_directional_setup
- AVGO (short): 23.93 — both_index_and_sector_contradict
- MSFT (no_trade): 22.85 — no_directional_setup

## 9. Final Summary
- Regime: **bullish** (bias=long)
- Trade ideas: A/B=8, C=6, rejected=14
