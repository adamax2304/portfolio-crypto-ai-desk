# Stocks AI Desk — LLM Analysis Packet

Generated: 2026-05-24 23:00 UTC
Mode: intraday
Asset class: stocks

## Read me first

- This packet is for STOCKS analysis only. Do not include crypto candidates, crypto regime references, or USDT pair logic.
- Index direction (SPY/QQQ/IWM) and sector ETF alignment are first-class signals. Treat them with the same weight as fundamentals for intraday/swing decisions.
- Earnings risk overrides clean technicals. Refuse swing entries into earnings unless the user explicitly asks for an earnings trade.
- yfinance is the data source; treat it as best-effort, not tick-accurate. If data freshness is suspect, mark trades watchlist.

## Latest stocks report
_File: `data\reports\stocks\intraday\2026-05-24_23-00_stocks_intraday_report.md`_

# Stocks AI Desk Report

Date: 2026-05-24
Mode: intraday
Asset class: stocks
Market session: weekend
Data freshness: 2026-05-24 23:00 UTC

## 0. Data Coverage
- Earnings events tracked: 0

## 1. Stock Market Regime
- Label: **bullish**
- Bias: long
- Risk-on: True
- VIX: 16.70
- Breadth above EMA20: 100.0%
- Breadth above EMA50: 100.0%
- Explanation: 4/4 indices trending up; breadth_above_ema20=1.0; VIX=16.70

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
- No fresh stock-tagged catalysts in the lookback window.

## 5. Top Candidates

| Symbol | Direction | Tier | Score | Confidence | Risk Penalty |
|--------|-----------|------|-------|------------|--------------|
| AAPL | long | B | 77.46 | high | -4.0 |
| TSLA | long | B | 70.15 | medium | -4.0 |
| NVDA | short | rejected | 30.54 | low | -18.0 |
| MSFT | no_trade | rejected | 25.87 | low | 0.0 |

## 6. Trade Ideas (A/B-tier)

### Idea #1 — B AAPL long
- Score: 77.46
- Confidence: high
- Risk level: low
- Timeframe: 15m/1h
- Thesis: AAPL long (intraday) | trend=uptrend | RS=leader | regime=bullish | earnings:unknown
- Evidence:
  - RR to TP1 below 1.5 (1.0)
  - above prev day high
  - RS vs SPY (20d): +9.49%
  - RS vs sector ETF (20d): +1.34%
- Entry: long zone 308.0356–308.8800
- Invalidation: close beyond 306.3468
- Targets: TP1: 311.4132, TP2: 313.1020, TP3: 315.6352
- Counter-thesis:
  - earnings risk: unknown
- Avoid:
  - do not chase if price is > 2 ATR from planned entry
  - do not enter against a clear SPY breakdown

### Idea #2 — B TSLA long
- Score: 70.15
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
- No C-tier symbols.

## 8. Rejected / Not Ready
- NVDA (short): 30.54 — short_in_bullish_regime, short_in_strong_sector, rr_below_1.5
- MSFT (no_trade): 25.87 — no_directional_setup

## 9. Final Summary
- Regime: **bullish** (bias=long)
- Trade ideas: A/B=2, C=0, rejected=2


## Latest stocks agent outputs
### Trade idea agent output
_File: `data\processed\agent_outputs\20260524_230030_stocks_stock_trade_idea.json`_

```json
{
  "mode": "intraday",
  "asset_class": "stocks",
  "ideas": [
    {
      "symbol": "AAPL",
      "direction": "long",
      "score": 77.46,
      "confidence": "high",
      "risk_level": "low",
      "timeframe": "15m/1h",
      "tier": "B",
      "mode": "intraday",
      "asset_class": "stocks",
      "exchange_focus": "US",
      "exchanges_confirmed": [
        "US"
      ],
      "data_confidence": "high",
      "thesis": "AAPL long (intraday) | trend=uptrend | RS=leader | regime=bullish | earnings:unknown",
      "evidence": [
        "RR to TP1 below 1.5 (1.0)",
        "above prev day high",
        "RS vs SPY (20d): +9.49%",
        "RS vs sector ETF (20d): +1.34%"
      ],
      "counterarguments": [
        "earnings risk: unknown"
      ],
      "entry_plan": "long zone 308.0356\u2013308.8800",
      "invalidation": "close beyond 306.3468",
      "targets": [
        "TP1: 311.4132",
        "TP2: 313.1020",
        "TP3: 315.6352"
      ],
      "what_to_monitor": [
        "SPY/QQQ direction and intraday VIX moves",
        "sector ETF trend (alignment with the trade)",
        "relative volume vs 20-day average"
      ],
      "avoid_conditions": [
        "do not chase if price is > 2 ATR from planned entry",
        "do not enter against a clear SPY breakdown"
      ],
      "data_sources_used": [
        "yfinance",
        "rss_news"
      ],
      "cap_reasons": [],
      "status": "open",
      "raw": {
        "setup": {
          "entry_low": 308.03560420445035,
          "entry_high": 308.8800048828125,
          "invalidation": 306.34680284772605,
          "tp1": 311.413206917899,
          "tp2": 313.1020082746233,
          "tp3": 315.6352103097098,
          "rr_to_tp1": 1.0
        },
        "score": {
          "symbol": "AAPL",
          "direction": "long",
          "final_score": 77.46,
          "tier": "B",
          "confidence": "high",
          "components": {
            "market_regime_alignment": 15.0,
            "index_confirmation": 10.0,
            "sector_confirmation": 10.0,
            "relative_strength": 16.54,
            "technical_setup": 16.17,
            "volume_relative_volume": 5.75,
            "news_catalyst": 0.0,
            "earnings_risk_adjustment": 0.0,
            "risk_reward": 0.0,
            "data_confidence": 8.0
          },
          "risk_penalty": -4.0,
          "cap_reasons": [],
          "blocks": []
        },
        "relative_strength": {
          "symbol": "AAPL",
          "sector": "technology",
          "sector_etf": "XLK",
          "return_5d": 2.8611384683597807,
          "return_20d": 13.930498821561699,
          "rs_vs_spy_20d": 9.49,
          "rs_vs_qqq_20d": 5.848,
          "rs_vs_sector_20d": 1.342,
          "classification": "leader"
        },
        "earnings": {
          "symbol": "AAPL",
          "next_earnings_date": null,
          "days_ahead": null,
          "report_time": "unknown",
          "severity": "unknown",
          "note": "no earnings date known",
          "blocks_swing": false,
          "intraday_high_risk": false
        },
        "regime": {
          "label": "bullish"
        },
        "news_count": 0
      }
    },
    {
      "symbol": "TSLA",
      "direction": "long",
      "score": 70.15,
      "confidence": "medium",
      "risk_level": "low",
      "timeframe": "15m/1h",
      "tier": "B",
      "mode": "intraday",
      "asset_class": "stocks",
      "exchange_focus": "US",
      "exchanges_confirmed": [
        "US"
      ],
      "data_confidence": "medium",
      "thesis": "TSLA long (intraday) | trend=uptrend | RS=leader | regime=bullish | earnings:unknown",
      "evidence": [
        "RR to TP1 below 1.5 (1.0)",
        "RS vs SPY (20d): +8.77%",
        "RS vs sector ETF (20d): +12.80%"
      ],
      "counterarguments": [
        "earnings risk: unknown"
      ],
      "entry_plan": "long zone 423.3290\u2013425.9482",
      "invalidation": "close beyond 418.0905",
     
…(truncated)
```

### Scoring agent output
_File: `data\processed\agent_outputs\20260524_230030_stocks_stock_scoring.json`_

```json
{
  "mode": "intraday",
  "regime_label": "bullish",
  "regime_bias": "long",
  "scores": [
    {
      "symbol": "AAPL",
      "direction": "long",
      "final_score": 77.46,
      "tier": "B",
      "confidence": "high",
      "components": {
        "market_regime_alignment": 15.0,
        "index_confirmation": 10.0,
        "sector_confirmation": 10.0,
        "relative_strength": 16.54,
        "technical_setup": 16.17,
        "volume_relative_volume": 5.75,
        "news_catalyst": 0.0,
        "earnings_risk_adjustment": 0.0,
        "risk_reward": 0.0,
        "data_confidence": 8.0
      },
      "risk_penalty": -4.0,
      "cap_reasons": [],
      "blocks": []
    },
    {
      "symbol": "TSLA",
      "direction": "long",
      "final_score": 70.15,
      "tier": "B",
      "confidence": "medium",
      "components": {
        "market_regime_alignment": 15.0,
        "index_confirmation": 10.0,
        "sector_confirmation": 5.0,
        "relative_strength": 16.54,
        "technical_setup": 13.86,
        "volume_relative_volume": 5.75,
        "news_catalyst": 0.0,
        "earnings_risk_adjustment": 0.0,
        "risk_reward": 0.0,
        "data_confidence": 8.0
      },
      "risk_penalty": -4.0,
      "cap_reasons": [],
      "blocks": []
    },
    {
      "symbol": "NVDA",
      "direction": "short",
      "final_score": 30.54,
      "tier": "rejected",
      "confidence": "low",
      "components": {
        "market_regime_alignment": 0.0,
        "index_confirmation": 10.0,
        "sector_confirmation": 2.0,
        "relative_strength": 6.62,
        "technical_setup": 16.17,
        "volume_relative_volume": 5.75,
        "news_catalyst": 0.0,
        "earnings_risk_adjustment": 0.0,
        "risk_reward": 0.0,
        "data_confidence": 8.0
      },
      "risk_penalty": -18.0,
      "cap_reasons": [],
      "blocks": []
    },
    {
      "symbol": "MSFT",
      "direction": "no_trade",
      "final_score": 25.87,
      "tier": "rejected",
      "confidence": "low",
      "components": {
        "market_regime_alignment": 0.0,
        "index_confirmation": 2.0,
        "sector_confirmation": 2.0,
        "relative_strength": 1.65,
        "technical_setup": 3.47,
        "volume_relative_volume": 5.75,
        "news_catalyst": 0.0,
        "earnings_risk_adjustment": 0.0,
        "risk_reward": 3.0,
        "data_confidence": 8.0
      },
      "risk_penalty": 0.0,
      "cap_reasons": [],
      "blocks": [
        "no_directional_setup"
      ]
    }
  ]
}
```

### Regime snapshot
_File: `data\processed\agent_outputs\20260524_230029_stocks_stocks_market_regime.json`_

```json
{
  "regime": {
    "label": "bullish",
    "bias": "long",
    "risk_on": true,
    "high_volatility": false,
    "breadth_above_ema20": 1.0,
    "breadth_above_ema50": 1.0,
    "vix_level": 16.700000762939453,
    "explanation": "4/4 indices trending up; breadth_above_ema20=1.0; VIX=16.70",
    "indices": [
      {
        "symbol": "SPY",
        "trend": "uptrend",
        "return_5d": 0.8753104005669199,
        "return_20d": 4.440150726759828,
        "above_ema20": true,
        "above_ema50": true,
        "last_close": 745.6400146484375
      },
      {
        "symbol": "QQQ",
        "trend": "uptrend",
        "return_5d": 1.2145043150262325,
        "return_20d": 8.082781940992966,
        "above_ema20": true,
        "above_ema50": true,
        "last_close": 717.5399780273438
      },
      {
        "symbol": "IWM",
        "trend": "uptrend",
        "return_5d": 2.7089297004077473,
        "return_20d": 3.061630727478848,
        "above_ema20": true,
        "above_ema50": true,
        "last_close": 285.1199951171875
      },
      {
        "symbol": "DIA",
        "trend": "uptrend",
        "return_5d": 2.170095101835323,
        "return_20d": 2.82603033331128,
        "above_ema20": true,
        "above_ema50": true,
        "last_close": 506.1199951171875
      }
    ]
  },
  "indices": [
    {
      "symbol": "SPY",
      "trend": "uptrend",
      "return_5d": 0.8753104005669199,
      "return_20d": 4.440150726759828,
      "above_ema20": true,
      "above_ema50": true,
      "last_close": 745.6400146484375
    },
    {
      "symbol": "QQQ",
      "trend": "uptrend",
      "return_5d": 1.2145043150262325,
      "return_20d": 8.082781940992966,
      "above_ema20": true,
      "above_ema50": true,
      "last_close": 717.5399780273438
    },
    {
      "symbol": "IWM",
      "trend": "uptrend",
      "return_5d": 2.7089297004077473,
      "return_20d": 3.061630727478848,
      "above_ema20": true,
      "above_ema50": true,
      "last_close": 285.1199951171875
    },
    {
      "symbol": "DIA",
      "trend": "uptrend",
      "return_5d": 2.170095101835323,
      "return_20d": 2.82603033331128,
      "above_ema20": true,
      "above_ema50": true,
      "last_close": 506.1199951171875
    }
  ]
}
```

### Sector rotation snapshot
_File: `data\processed\agent_outputs\20260524_230029_stocks_sector_rotation.json`_

```json
{
  "benchmark": "SPY",
  "benchmark_return_20d": 4.440150726759828,
  "sectors": [
    {
      "sector": "semiconductors",
      "etf": "SMH",
      "return_5d": 3.591325359363462,
      "return_20d": 13.798279074705878,
      "rs_vs_spy_20d": 9.35812834794605,
      "above_ema50": true,
      "status": "strong"
    },
    {
      "sector": "technology",
      "etf": "XLK",
      "return_5d": 2.343132311088514,
      "return_20d": 12.588938968463204,
      "rs_vs_spy_20d": 8.148788241703375,
      "above_ema50": true,
      "status": "strong"
    },
    {
      "sector": "energy",
      "etf": "XLE",
      "return_5d": 0.08412357488740696,
      "return_20d": 4.607003333550441,
      "rs_vs_spy_20d": 0.16685260679061287,
      "above_ema50": true,
      "status": "mixed"
    },
    {
      "sector": "healthcare",
      "etf": "XLV",
      "return_5d": 3.30116683986601,
      "return_20d": 3.960332226335539,
      "rs_vs_spy_20d": -0.4798185004242894,
      "above_ema50": true,
      "status": "mixed"
    },
    {
      "sector": "consumer_staples",
      "etf": "XLP",
      "return_5d": 0.18904024487615967,
      "return_20d": 1.8863386176872332,
      "rs_vs_spy_20d": -2.553812109072595,
      "above_ema50": true,
      "status": "mixed"
    },
    {
      "sector": "real_estate",
      "etf": "XLRE",
      "return_5d": 3.0765714668936184,
      "return_20d": 1.6655247815187346,
      "rs_vs_spy_20d": -2.7746259452410937,
      "above_ema50": true,
      "status": "mixed"
    },
    {
      "sector": "financials",
      "etf": "XLF",
      "return_5d": 1.643835964130802,
      "return_20d": 1.0112805839765926,
      "rs_vs_spy_20d": -3.4288701427832358,
      "above_ema50": true,
      "status": "mixed"
    },
    {
      "sector": "consumer_discretionary",
      "etf": "XLY",
      "return_5d": 2.2740938416191847,
      "return_20d": 0.412838363544088,
      "rs_vs_spy_20d": -4.02731236321574,
      "above_ema50": true,
      "status": "mixed"
    },
    {
      "sector": "communications",
      "etf": "XLC",
      "return_5d": -0.5341167615455222,
      "return_20d": -0.0692416742433477,
      "rs_vs_spy_20d": -4.509392401003176,
      "above_ema50": false,
      "status": "weak"
    },
    {
      "sector": "industrials",
      "etf": "XLI",
      "return_5d": 0.2158753729011309,
      "return_20d": -0.4058659148186705,
      "rs_vs_spy_20d": -4.846016641578499,
      "above_ema50": true,
      "status": "mixed"
    },
    {
      "sector": "utilities",
      "etf": "XLU",
      "return_5d": 3.3736028681793595,
      "return_20d": -1.7973188080764646,
      "rs_vs_spy_20d": -6.237469534836293,
      "above_ema50": false,
      "status": "weak"
    },
    {
      "sector": "materials",
      "etf": "XLB",
      "return_5d": -0.019877379095145642,
      "return_20d": -3.1394401211533807,
      "rs_vs_spy_20d": -7.5795908479132095,
      "above_ema50": false,
      "status": "weak"
    }
  ],
  "strongest": [
    {
      "sector": "semiconductors",
      "etf": "SMH",
      "return_5d": 3.591325359363462,
      "return_20d": 13.798279074705878,
      "rs_vs_spy_20d": 9.35812834794605,
      "above_ema50": true,
      "status": "strong"
    },
    {
      "sector": "technology",
      "etf": "XLK",
      "return_5d": 2.343132311088514,
      "return_20d": 12.588938968463204,
      "rs_vs_spy_20d": 8.148788241703375,
      "above_ema50": true,
      "status": "strong"
    },
    {
      "sector": "energy",
      "etf": "XLE",
      "return_5d": 0.08412357488740696,
      "return_20d": 4.607003333550441,
      "rs_vs_spy_20d": 0.16685260679061287,
      "above_ema50": true,
      "status": "mixed"
    }
  ],
  "weakest": [
    {
      "sector": "materials",
      "etf": "XLB",
      "return_5d": -0.019877379095145642,
      "return_20d": -3.1394401211533807,
      "rs_vs_spy_20d": -7.5795908479132095,
      "above_ema50": false,
      "status": "weak"
    },
    {
      "sector": "utilities",
      "etf": "XLU",
      "return_5
…(truncated)
```


## Stocks signal performance (recent)
- Period: month, sample=2, confidence=anecdotal
- Wins=0 / Losses=0 / Ambiguous=0, avgR=None, totalR=0.0

## Upcoming earnings (next 7 days)
_No tracked earnings within the next 7 days._

## Stocks scoring & risk rules (summary)
- Tiering: A ≥ 80, B ≥ 65, C ≥ 50, rejected otherwise.
- Hard rejects: missing invalidation, no directional setup, earnings_today_blocks_swing (when mode=swing).
- Caps: score capped at 60 when earnings active (swing); capped at 70 when data is partial (no invalidation).
- Regime overrides: in risk_off regime, longs require leader-grade relative strength.
- Sector alignment: short in a strong sector or long in a weak sector incurs a -6 penalty per the risk_penalties block.
- Earnings windows (swing): blocked if ≤2 trading days ahead unless the user invokes an explicit earnings strategy.


## Pre-output checklist
1. Did you reference SPY/QQQ direction for every long/short call?
2. Did you flag earnings risk explicitly for every A/B idea?
3. Did you avoid mixing crypto symbols/funding/OI references?
4. Is there a clean invalidation level for every actionable idea?
5. Did you use the sector ETF (XLK/SMH/XLF/etc) as a confirmation check?
6. If yfinance data is stale or sparse for a symbol, did you downgrade?

