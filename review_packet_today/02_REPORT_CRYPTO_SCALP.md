# Crypto AI Desk Report

Date: 2026-05-25
Generated at: 2026-05-25 16:52:02 EEST
Mode: scalp
Data freshness: 2026-05-25 13:45:00+00:00
Market regime: transition (mixed)

## 0. Exchange Coverage & Candidate Funnel

- Anchor exchange: binance
- binance: role=anchor, universe=411, ohlcv_fetched=108, failed=3, high_risk=False
- bybit: role=derivatives, universe=434, ohlcv_fetched=92, failed=7, high_risk=False
- mexc: role=discovery, universe=1836, ohlcv_fetched=120, failed=0, high_risk=True

- Scanned on binance: 36
- Scanned on bybit: 2
- Scanned on mexc: 38
- After liquidity filter: 38
- After momentum filter: 5
- Fused candidates: 48
- Deep analysis: 30
- Full agent analysis: 15

## 1. Market Regime

- BTC trend: transition_up
- ETH trend: range
- Altcoin breadth above EMA20: 65.52%
- Altcoin breadth above EMA50: 58.62%
- Volatility: {'btc_atr_percentile': 35.0, 'state': 'normal/unknown'}
- Recommended trading style: selective only; demand clean invalidation
- Explanation: BTC trend is transition_up, ETH trend is range, and 65.5% of tracked symbols are above EMA20.

## 2. Where Money Is Flowing

### Strongest Symbols
- SAGA/USDT: score 96.2, 24h 37.07%, RS vs BTC 36.38%, volume 1.92x
- RENDER/USDT: score 95.7, 24h 8.96%, RS vs BTC 8.26%, volume 2.06x
- NIL/USDT: score 92.4, 24h 19.26%, RS vs BTC 18.56%, volume 1.16x
- INJ/USDT: score 91.5, 24h 10.34%, RS vs BTC 9.65%, volume 2.59x
- NEAR/USDT: score 81.5, 24h 7.07%, RS vs BTC 6.37%, volume 1.94x
- SAHARA/USDT: score 80.9, 24h 6.81%, RS vs BTC 6.11%, volume 1.23x
- EDEN/USDT: score 76.8, 24h -7.23%, RS vs BTC -7.93%, volume 0.92x
- BNB/USDT: score 69.1, 24h 2.12%, RS vs BTC 1.42%, volume 2.29x

### Weakest Symbols
- GENIUS/USDT: bias short, 24h -16.75%, RS vs BTC -17.44%
- BSB/USDT: bias short, 24h -7.55%, RS vs BTC -8.24%
- EDEN/USDT: bias short, 24h -7.23%, RS vs BTC -7.93%
- FIDA/USDT: bias short, 24h -3.07%, RS vs BTC -3.77%
- ASTER/USDT: bias short, 24h -2.09%, RS vs BTC -2.78%

### Unusual Volume
- SAGA/USDT: 1.92x 20-period average, tags relative_strength, volume_expansion, breakout, overextended
- RENDER/USDT: 2.06x 20-period average, tags relative_strength, volume_expansion, breakout, overextended
- INJ/USDT: 2.59x 20-period average, tags relative_strength, volume_expansion, overextended
- NEAR/USDT: 1.94x 20-period average, tags relative_strength, volume_expansion, overextended
- BNB/USDT: 2.29x 20-period average, tags volume_expansion, breakout, overextended
- DASH/USDT: 2.51x 20-period average, tags volume_expansion

### Narrative Heatmap
- Memes: heat 48.4/100, attention 100.0/100, momentum 46.1/100, volume 17.0/100, risk 35.0/100, status mixed, coins DOGE/USDT
- AI: heat 43.5/100, attention 35.0/100, momentum 71.2/100, volume 79.2/100, risk 37.5/100, status mixed, coins TAO/USDT, NEAR/USDT
- RWA: heat 25.1/100, attention 18.0/100, momentum 49.1/100, volume 30.5/100, risk 20.0/100, status mixed, coins ONDO/USDT
- L2: heat 3.3/100, attention 18.0/100, momentum 0.0/100, volume 0.0/100, risk 20.0/100, status quiet, coins n/a
- Gaming: heat 3.3/100, attention 18.0/100, momentum 0.0/100, volume 0.0/100, risk 20.0/100, status quiet, coins n/a
- DePIN: heat 0.0/100, attention 0.0/100, momentum 0.0/100, volume 0.0/100, risk 0.0/100, status quiet, coins n/a

## 3. Derivatives Overview

- SAGA/USDT: price up + OI up: fresh positioning confirms trend, monitor crowding; funding -0.00373788; OI 24h 15.49%; long/short 1.387; crowding unknown.
- RENDER/USDT: price up + OI up: fresh positioning confirms trend, monitor crowding; funding 5e-05; OI 24h 6.57%; long/short 1.645; crowding normal.
- NIL/USDT: price up + OI up: fresh positioning confirms trend, monitor crowding; funding -9.179e-05; OI 24h 35.74%; long/short 0.904; crowding normal.
- INJ/USDT: price up + OI up: fresh positioning confirms trend, monitor crowding; funding -0.00024033; OI 24h 7.1%; long/short 1.312; crowding normal.
- NEAR/USDT: price up + OI up: fresh positioning confirms trend, monitor crowding; funding -7.244e-05; OI 24h 3.38%; long/short 1.111; crowding normal.
- SAHARA/USDT: price up + OI down: short covering, weaker continuation quality; funding 5e-05; OI 24h -0.41%; long/short 0.511; crowding normal.
- EDEN/USDT: price down + OI down: deleveraging or long liquidation; funding -0.00070458; OI 24h -7.36%; long/short 1.0; crowding unknown.
- BNB/USDT: price up + OI up: fresh positioning confirms trend, monitor crowding; funding 9.073e-05; OI 24h 2.82%; long/short 2.295; crowding normal.

### Bybit/OKX Cross-Check
- SAGA/USDT: negative funding across external venues; venues bybit; funding {'bybit': -0.0042498}; crowding elevated.
- RENDER/USDT: external funding is neutral; venues bybit, okx; funding {'bybit': 5e-05, 'okx': 5e-05}; crowding elevated.
- NIL/USDT: external funding is neutral; venues bybit; funding {'bybit': 5e-05}; crowding elevated.
- INJ/USDT: external funding is neutral; venues bybit, okx; funding {'bybit': 9.027e-05, 'okx': -0.0002173201805173}; crowding low.
- NEAR/USDT: external funding is neutral; venues bybit, okx; funding {'bybit': 4.39e-06, 'okx': -0.0003774236829226}; crowding low.
- SAHARA/USDT: external funding is neutral; venues bybit, okx; funding {'bybit': 5e-05, 'okx': 5e-05}; crowding elevated.
- EDEN/USDT: negative funding across external venues; venues bybit, okx; funding {'bybit': -0.00082706, 'okx': -4.79843806922e-05}; crowding moderate.
- BNB/USDT: external funding is neutral; venues bybit, okx; funding {'bybit': 0.0001, 'okx': 0.0001}; crowding elevated.

## 4. Macro, Geopolitics, Crowd

- Macro/geopolitics: risk 35.0/100, BTC bias neutral / data-watch. Macro risk score 35/100 from 1 risk-off hit(s), 0 risk-on hit(s), and 0 calendar/watch hit(s).
- Macro headline: BTC price to attack $80K shorts on Iran peace deal: Five things to know in Bitcoin this week
- Social attention leaders:
- BTC/USDT: attention 100.0/100 from 15 mention(s); sources Reddit Bitcoin, Reddit CryptoCurrency
- ETH/USDT: attention 96.8/100 from 8 mention(s); sources Reddit CryptoCurrency, Reddit Ethereum
- SOL/USDT: attention 12.2/100 from 1 mention(s); sources Reddit CryptoCurrency
- BNB/USDT: attention 9.5/100 from 1 mention(s); sources Reddit CryptoCurrency
- No manual KOL/crowd notes found; X/Telegram/Discord context is not live yet.
- KOL watchlist still contains the placeholder account; replace it with trusted sources.

## 5. News and Catalysts

- Top news:
- Price predictions 5/22: BTC, ETH, BNB, XRP, SOL, DOGE, HYPE, ADA, ZEC, BCH (Cointelegraph; symbols ['DOGE', 'BTC', 'XRP', 'ETH', 'SOL', 'BNB']; verification single_source)
- MicroStrategy buys more (MSTR) (test_source; symbols ['MSTR']; verification single_source)
- Coinbase reports record revenue (COIN) (test_source; symbols ['COIN']; verification single_source)
- AAPL announces share buyback (test_source; symbols ['AAPL']; verification single_source)
- NVDA beats earnings (test_source; symbols ['NVDA']; verification single_source)
- Bitcoin risks drop to $72K as demand metric hits 2026 lows (Cointelegraph; symbols ['BTC']; verification single_source)
- Buterin fires back at Ethereum Foundation critics, recommits to neutrality (Cointelegraph; symbols ['ETH']; verification single_source)
- Strategy Now Holds $65 Billion in Bitcoin—These Are Its Biggest BTC Buys (Decrypt; symbols ['BTC']; verification single_source)
- Catalysts/events:
- BNB/USDT: fresh attention/catalyst detected; catalysts ['news: Price predictions 5/22: BTC, ETH, BNB, XRP, SOL, DOGE, HYPE, ADA, ZEC, BCH (Cointelegraph)']; risks []
- ETH/USDT: fresh attention/catalyst detected; catalysts ['news: Price predictions 5/22: BTC, ETH, BNB, XRP, SOL, DOGE, HYPE, ADA, ZEC, BCH (Cointelegraph)', 'news: Buterin fires back at Ethereum Foundation critics, recommits to neutrality (Cointelegraph)']; risks []
- SOL/USDT: fresh attention/catalyst detected; catalysts ['news: Price predictions 5/22: BTC, ETH, BNB, XRP, SOL, DOGE, HYPE, ADA, ZEC, BCH (Cointelegraph)']; risks []
- BTC/USDT: fresh attention/catalyst detected; catalysts ['news: Price predictions 5/22: BTC, ETH, BNB, XRP, SOL, DOGE, HYPE, ADA, ZEC, BCH (Cointelegraph)', 'news: Bitcoin risks drop to $72K as demand metric hits 2026 lows (Cointelegraph)']; risks []
- XRP/USDT: fresh attention/catalyst detected; catalysts ['news: Price predictions 5/22: BTC, ETH, BNB, XRP, SOL, DOGE, HYPE, ADA, ZEC, BCH (Cointelegraph)', 'news: HYPE funds attract millions as investors dump bitcoin and ether ETFs (CoinDesk)']; risks []
- DOGE/USDT: fresh attention/catalyst detected; catalysts ['news: Price predictions 5/22: BTC, ETH, BNB, XRP, SOL, DOGE, HYPE, ADA, ZEC, BCH (Cointelegraph)']; risks []

## 6. Top Trade Ideas

### A-tier (high conviction, no active caps)

- No A-tier setups found. Do not force a trade.

### B-tier (valid but one or two confirmations missing)

- No B-tier setups found.

## 7. C-tier / Watchlist

### Trade Idea #1 - WATCHLIST ONLY NIL/USDT

Score: 60.4/100
Confidence: medium
Trade Type: 1h thesis / 5m execution (scalp 30m-2h)
Risk: low

**Thesis**
NIL/USDT is interesting, but the evidence is not strong enough for an active trade. Keep it on watch and demand a better entry or cleaner confirmation.

**Evidence**
- Market regime: transition (mixed); style: selective only; demand clean invalidation.
- 24h return: 19.26%; 7d return: 68.48%.
- Relative strength vs BTC: 18.56%.
- Volume ratio vs 20-period average: 1.16x.
- Trend: uptrend; setup quality: 68.1/100; RR to TP1: 1.31R.
- Score breakdown: {'market_regime': 8.7, 'technical_setup': 13.6, 'momentum': 14.1, 'derivatives': 13.6, 'catalyst_news': 5.4, 'narrative': 3.4, 'execution_quality': 7.9}; risk penalty: -6.3.
- Derivatives: price up + OI up: fresh positioning confirms trend, monitor crowding; funding -9.179e-05; OI change 35.74%; crowding normal.
- Catalyst/news: no fresh verified catalyst detected.
- Risk gate: low risk, score 35.0/100.

**Score Breakdown**
- market_regime: 8.7
- technical_setup: 13.6
- momentum: 14.1
- derivatives: 13.6
- catalyst_news: 5.4
- narrative: 3.4
- execution_quality: 7.9
- Risk penalty: -6.3

**Entry Plan**
Watch only. Conditional pullback zone: 0.0769-0.0791. Do not treat this as active until regime, volume, or confirmation improves.

**Invalidation**
Potential invalidation if activated: 1h close beyond 0.0727. Not active while score is below threshold.

**Targets**
- Conditional TP1: 0.0851
- Conditional TP2: 0.0900
- Conditional TP3: 0.0949

**Counter-Thesis**
- The long fails if NIL/USDT is just a beta bounce inside a transition market and buyers do not defend the planned pullback zone.
- The broad tape is not decisive; momentum can mean-revert.
- No fresh catalyst is verified for this symbol.
- Market regime is mixed; breakout failure risk is elevated.
- No fresh verified catalyst detected.
- Market regime is not clean; breakouts can fail quickly.
- Score is below active-trade threshold; this is watchlist/no-trade.

**Conditions To Avoid**
- Do not enter if price is more than 2 ATR away from the planned entry.
- Do not enter if BTC breaks down against the regime thesis.
- Avoid if fresh news is unverified or contradicts the setup.

**What To Monitor**
- BTC and ETH structure around local support/resistance.
- Volume on pullback or breakout retest.
- Whether price accepts inside the entry zone instead of chasing.
- Funding, OI change, and long/short skew for crowding.

**Desk Notes**
- Current price: 0.0801
- ATR: 0.0049
- Support: 0.0734
- Resistance: 0.0899

**Chart**

![NIL/USDT setup chart](../charts/20260525_1351_NIL_USDT.png)


### Trade Idea #2 - WATCHLIST ONLY SAHARA/USDT

Score: 57.9/100
Confidence: low
Trade Type: 1h thesis / 5m execution (scalp 30m-2h)
Risk: low

**Thesis**
SAHARA/USDT is interesting, but the evidence is not strong enough for an active trade. Keep it on watch and demand a better entry or cleaner confirmation.

**Evidence**
- Market regime: transition (mixed); style: selective only; demand clean invalidation.
- 24h return: 6.81%; 7d return: 7.97%.
- Relative strength vs BTC: 6.11%.
- Volume ratio vs 20-period average: 1.23x.
- Trend: uptrend; setup quality: 67.1/100; RR to TP1: 1.84R.
- Score breakdown: {'market_regime': 8.7, 'technical_setup': 13.4, 'momentum': 12.4, 'derivatives': 9.9, 'catalyst_news': 5.4, 'narrative': 3.4, 'execution_quality': 11.0}; risk penalty: -6.3.
- Derivatives: price up + OI down: short covering, weaker continuation quality; funding 5e-05; OI change -0.41%; crowding normal.
- Catalyst/news: no fresh verified catalyst detected.
- Risk gate: low risk, score 35.0/100.

**Score Breakdown**
- market_regime: 8.7
- technical_setup: 13.4
- momentum: 12.4
- derivatives: 9.9
- catalyst_news: 5.4
- narrative: 3.4
- execution_quality: 11.0
- Risk penalty: -6.3

**Entry Plan**
Watch only. Conditional pullback zone: 0.0352-0.0356. Do not treat this as active until regime, volume, or confirmation improves.

**Invalidation**
Potential invalidation if activated: 1h close beyond 0.0348. Not active while score is below threshold.

**Targets**
- Conditional TP1: 0.0366
- Conditional TP2: 0.0374
- Conditional TP3: 0.0382

**Counter-Thesis**
- The long fails if SAHARA/USDT is just a beta bounce inside a transition market and buyers do not defend the planned pullback zone.
- The broad tape is not decisive; momentum can mean-revert.
- No fresh catalyst is verified for this symbol.
- Market regime is mixed; breakout failure risk is elevated.
- No fresh verified catalyst detected.
- Market regime is not clean; breakouts can fail quickly.
- Score is below active-trade threshold; this is watchlist/no-trade.

**Conditions To Avoid**
- Do not enter if price is more than 2 ATR away from the planned entry.
- Do not enter if BTC breaks down against the regime thesis.
- Avoid if fresh news is unverified or contradicts the setup.

**What To Monitor**
- BTC and ETH structure around local support/resistance.
- Volume on pullback or breakout retest.
- Whether price accepts inside the entry zone instead of chasing.
- Funding, OI change, and long/short skew for crowding.

**Desk Notes**
- Current price: 0.0358
- ATR: 0.0008
- Support: 0.0339
- Resistance: 0.0364

**Chart**

![SAHARA/USDT setup chart](../charts/20260525_1351_SAHARA_USDT.png)


### Trade Idea #3 - WATCHLIST ONLY BSB/USDT

Score: 54.4/100
Confidence: low
Trade Type: 1h thesis / 5m execution (scalp 30m-2h)
Risk: low

**Thesis**
BSB/USDT is interesting, but the evidence is not strong enough for an active trade. Keep it on watch and demand a better entry or cleaner confirmation.

**Evidence**
- Market regime: transition (mixed); style: selective only; demand clean invalidation.
- 24h return: -7.55%; 7d return: 40.91%.
- Relative strength vs BTC: -8.24%.
- Volume ratio vs 20-period average: 1.47x.
- Trend: range; setup quality: 49.9/100; RR to TP1: 1.84R.
- Score breakdown: {'market_regime': 8.7, 'technical_setup': 10.0, 'momentum': 10.3, 'derivatives': 12.0, 'catalyst_news': 5.4, 'narrative': 3.4, 'execution_quality': 11.0}; risk penalty: -6.3.
- Derivatives: price down + OI up: fresh shorts pressing, possible squeeze if price reclaims; funding 0.00036993; OI change 13.77%; crowding normal.
- Catalyst/news: no fresh verified catalyst detected.
- Risk gate: low risk, score 35.0/100.

**Score Breakdown**
- market_regime: 8.7
- technical_setup: 10.0
- momentum: 10.3
- derivatives: 12.0
- catalyst_news: 5.4
- narrative: 3.4
- execution_quality: 11.0
- Risk penalty: -6.3

**Entry Plan**
Watch only. Conditional failed bounce/retest zone: 0.9770-1.006. Do not treat this as active until regime, volume, or confirmation improves.

**Invalidation**
Potential invalidation if activated: 1h close beyond 1.042. Not active while score is below threshold.

**Targets**
- Conditional TP1: 0.8994
- Conditional TP2: 0.8346
- Conditional TP3: 0.7699

**Counter-Thesis**
- The short fails if BSB/USDT is a late breakdown into exhausted sellers and BTC/ETH reclaim local levels.
- The broad tape is not decisive; momentum can mean-revert.
- No fresh catalyst is verified for this symbol.
- Market regime is mixed; breakout failure risk is elevated.
- No fresh verified catalyst detected.
- Market regime is not clean; breakouts can fail quickly.
- Score is below active-trade threshold; this is watchlist/no-trade.

**Conditions To Avoid**
- Do not enter if price is more than 2 ATR away from the planned entry.
- Do not enter if BTC breaks down against the regime thesis.
- Avoid if fresh news is unverified or contradicts the setup.

**What To Monitor**
- BTC and ETH structure around local support/resistance.
- Volume on pullback or breakout retest.
- Whether price accepts inside the entry zone instead of chasing.
- Funding, OI change, and long/short skew for crowding.

**Desk Notes**
- Current price: 0.9641
- ATR: 0.0647
- Support: 0.7863
- Resistance: 1.124

**Chart**

![BSB/USDT setup chart](../charts/20260525_1352_BSB_USDT.png)


### Trade Idea #4 - WATCHLIST ONLY TAO/USDT

Score: 52.6/100
Confidence: low
Trade Type: 1h thesis / 5m execution (scalp 30m-2h)
Risk: low

**Thesis**
TAO/USDT is interesting, but the evidence is not strong enough for an active trade. Keep it on watch and demand a better entry or cleaner confirmation.

**Evidence**
- Market regime: transition (mixed); style: selective only; demand clean invalidation.
- 24h return: 1.09%; 7d return: 6.87%.
- Relative strength vs BTC: 0.39%.
- Volume ratio vs 20-period average: 1.23x.
- Trend: uptrend; setup quality: 58.2/100; RR to TP1: 1.84R.
- Score breakdown: {'market_regime': 8.7, 'technical_setup': 11.6, 'momentum': 9.3, 'derivatives': 9.9, 'catalyst_news': 5.4, 'narrative': 2.9, 'execution_quality': 11.0}; risk penalty: -6.3.
- Derivatives: price up + OI down: short covering, weaker continuation quality; funding 5e-05; OI change -0.09%; crowding normal.
- Catalyst/news: no fresh verified catalyst detected.
- Risk gate: low risk, score 35.0/100.
- Narrative: AI is mixed, heat 43.5/100, risk 37.5/100.

**Score Breakdown**
- market_regime: 8.7
- technical_setup: 11.6
- momentum: 9.3
- derivatives: 9.9
- catalyst_news: 5.4
- narrative: 2.9
- execution_quality: 11.0
- Risk penalty: -6.3

**Entry Plan**
Watch only. Conditional pullback zone: 276.68-277.94. Do not treat this as active until regime, volume, or confirmation improves.

**Invalidation**
Potential invalidation if activated: 1h close beyond 275.13. Not active while score is below threshold.

**Targets**
- Conditional TP1: 281.31
- Conditional TP2: 284.11
- Conditional TP3: 286.92

**Counter-Thesis**
- The long fails if TAO/USDT is just a beta bounce inside a transition market and buyers do not defend the planned pullback zone.
- The broad tape is not decisive; momentum can mean-revert.
- No fresh catalyst is verified for this symbol.
- Market regime is mixed; breakout failure risk is elevated.
- No fresh verified catalyst detected.
- Market regime is not clean; breakouts can fail quickly.
- Score is below active-trade threshold; this is watchlist/no-trade.

**Conditions To Avoid**
- Do not enter if price is more than 2 ATR away from the planned entry.
- Do not enter if BTC breaks down against the regime thesis.
- Avoid if fresh news is unverified or contradicts the setup.

**What To Monitor**
- BTC and ETH structure around local support/resistance.
- Volume on pullback or breakout retest.
- Whether price accepts inside the entry zone instead of chasing.
- Funding, OI change, and long/short skew for crowding.

**Desk Notes**
- Current price: 278.50
- ATR: 2.807
- Support: 268.40
- Resistance: 280.80

**Chart**

![TAO/USDT setup chart](../charts/20260525_1352_TAO_USDT.png)


### Trade Idea #5 - WATCHLIST ONLY LTC/USDT

Score: 51.7/100
Confidence: low
Trade Type: 1h thesis / 5m execution (scalp 30m-2h)
Risk: low

**Thesis**
LTC/USDT is interesting, but the evidence is not strong enough for an active trade. Keep it on watch and demand a better entry or cleaner confirmation.

**Evidence**
- Market regime: transition (mixed); style: selective only; demand clean invalidation.
- 24h return: -0.7%; 7d return: -1.86%.
- Relative strength vs BTC: -1.39%.
- Volume ratio vs 20-period average: 1.15x.
- Trend: downtrend; setup quality: 54.4/100; RR to TP1: 1.4R.
- Score breakdown: {'market_regime': 8.7, 'technical_setup': 10.9, 'momentum': 9.2, 'derivatives': 12.0, 'catalyst_news': 5.4, 'narrative': 3.4, 'execution_quality': 8.4}; risk penalty: -6.3.
- Derivatives: price down + OI up: fresh shorts pressing, possible squeeze if price reclaims; funding 0.0001; OI change 2.03%; crowding normal.
- Catalyst/news: no fresh verified catalyst detected.
- Risk gate: low risk, score 35.0/100.

**Score Breakdown**
- market_regime: 8.7
- technical_setup: 10.9
- momentum: 9.2
- derivatives: 12.0
- catalyst_news: 5.4
- narrative: 3.4
- execution_quality: 8.4
- Risk penalty: -6.3

**Entry Plan**
Watch only. Conditional failed bounce/retest zone: 52.866-52.971. Do not treat this as active until regime, volume, or confirmation improves.

**Invalidation**
Potential invalidation if activated: 1h close beyond 53.155. Not active while score is below threshold.

**Targets**
- Conditional TP1: 52.588
- Conditional TP2: 52.356
- Conditional TP3: 52.124

**Counter-Thesis**
- The short fails if LTC/USDT is a late breakdown into exhausted sellers and BTC/ETH reclaim local levels.
- The broad tape is not decisive; momentum can mean-revert.
- No fresh catalyst is verified for this symbol.
- Market regime is mixed; breakout failure risk is elevated.
- No fresh verified catalyst detected.
- Market regime is not clean; breakouts can fail quickly.
- Score is below active-trade threshold; this is watchlist/no-trade.

**Conditions To Avoid**
- Do not enter if price is more than 2 ATR away from the planned entry.
- Do not enter if BTC breaks down against the regime thesis.
- Avoid if fresh news is unverified or contradicts the setup.

**What To Monitor**
- BTC and ETH structure around local support/resistance.
- Volume on pullback or breakout retest.
- Whether price accepts inside the entry zone instead of chasing.
- Funding, OI change, and long/short skew for crowding.

**Desk Notes**
- Current price: 52.820
- ATR: 0.2321
- Support: 51.970
- Resistance: 53.120

**Chart**

![LTC/USDT setup chart](../charts/20260525_1352_LTC_USDT.png)



## 7b. Rejected / Not Ready

- SAGA/USDT: score 43.6 (long) — Price is more than 2 ATR from EMA20; do not chase.. Reasons: Price is more than 2 ATR from EMA20; do not chase.; Entry quality is weak because the move is extended.; Converted to watchlist only: wait for pullback.. Exchanges: binance.
- RENDER/USDT: score 42.3 (long) — Price is more than 2 ATR from EMA20; do not chase.. Reasons: Price is more than 2 ATR from EMA20; do not chase.; Entry quality is weak because the move is extended.; Converted to watchlist only: wait for pullback.. Exchanges: binance.
- INJ/USDT: score 41.2 (long) — Price is more than 2 ATR from EMA20; do not chase.. Reasons: Price is more than 2 ATR from EMA20; do not chase.; Entry quality is weak because the move is extended.; Converted to watchlist only: wait for pullback.. Exchanges: binance, mexc.
- NEAR/USDT: score 38.4 (long) — Price is more than 2 ATR from EMA20; do not chase.. Reasons: Price is more than 2 ATR from EMA20; do not chase.; Entry quality is weak because the move is extended.; Market regime is mixed; breakout failure risk is elevated.. Exchanges: binance, mexc.
- EDEN/USDT: score 46.1 (short) — Market regime is mixed; breakout failure risk is elevated.. Reasons: Market regime is mixed; breakout failure risk is elevated.; Funding is negative; shorts may be crowded.; No fresh verified catalyst detected.. Exchanges: binance.
- BNB/USDT: score 38.1 (long) — Price is more than 2 ATR from EMA20; do not chase.. Reasons: Price is more than 2 ATR from EMA20; do not chase.; Entry quality is weak because the move is extended.; Converted to watchlist only: wait for pullback.. Exchanges: binance, mexc.
- GENIUS/USDT: score 38.6 (short) — Market regime is mixed; breakout failure risk is elevated.. Reasons: Market regime is mixed; breakout failure risk is elevated.; Volume is below average; breakout confirmation is weak.; No fresh verified catalyst detected.. Exchanges: binance.
- ZEC/USDT: score 48.1 (long) — Market regime is mixed; breakout failure risk is elevated.. Reasons: Market regime is mixed; breakout failure risk is elevated.; Volume is below average; breakout confirmation is weak.; Global long/short ratio is heavily short skewed.. Exchanges: binance, mexc.
- TRX/USDT: score 33.9 (long) — Price is more than 2 ATR from EMA20; do not chase.. Reasons: Price is more than 2 ATR from EMA20; do not chase.; Entry quality is weak because the move is extended.; Converted to watchlist only: wait for pullback.. Exchanges: binance, mexc.
- UNI/USDT: score 44.8 (short) — Market regime is mixed; breakout failure risk is elevated.. Reasons: Market regime is mixed; breakout failure risk is elevated.; Volume is below average; breakout confirmation is weak.; No fresh verified catalyst detected.. Exchanges: binance.

## 7c. Multi-Exchange Confirmation

- NIL/USDT [C]: exchanges=['binance'], anchor=True, derivatives=False, high_risk_only=False, confirmation=68.0/100, focus=binance. Anchor listed but no derivatives confirmation; healthier than MEXC-only but no positioning data.
- SAHARA/USDT [C]: exchanges=['binance'], anchor=True, derivatives=False, high_risk_only=False, confirmation=68.0/100, focus=binance. Anchor listed but no derivatives confirmation; healthier than MEXC-only but no positioning data.
- BSB/USDT [C]: exchanges=['mexc'], anchor=False, derivatives=False, high_risk_only=True, confirmation=38.0/100, focus=mexc. MEXC-only; treat as speculative discovery, demand confirmation from anchor or Bybit.
- TAO/USDT [C]: exchanges=['binance', 'mexc'], anchor=True, derivatives=False, high_risk_only=False, confirmation=81.8/100, focus=binance. Anchor listed but no derivatives confirmation; healthier than MEXC-only but no positioning data.
- LTC/USDT [C]: exchanges=['binance', 'mexc'], anchor=True, derivatives=False, high_risk_only=False, confirmation=87.8/100, focus=binance. Anchor listed but no derivatives confirmation; healthier than MEXC-only but no positioning data.
- ZEC/USDT [rejected]: exchanges=['binance', 'mexc'], anchor=True, derivatives=False, high_risk_only=False, confirmation=83.4/100, focus=binance. Anchor listed but no derivatives confirmation; healthier than MEXC-only but no positioning data.
- EDEN/USDT [rejected]: exchanges=['binance'], anchor=True, derivatives=False, high_risk_only=False, confirmation=68.0/100, focus=binance. Anchor listed but no derivatives confirmation; healthier than MEXC-only but no positioning data.
- UNI/USDT [rejected]: exchanges=['binance'], anchor=True, derivatives=False, high_risk_only=False, confirmation=68.0/100, focus=binance. Anchor listed but no derivatives confirmation; healthier than MEXC-only but no positioning data.
- SAGA/USDT [rejected]: exchanges=['binance'], anchor=True, derivatives=False, high_risk_only=False, confirmation=68.0/100, focus=binance. Anchor listed but no derivatives confirmation; healthier than MEXC-only but no positioning data.
- RENDER/USDT [rejected]: exchanges=['binance'], anchor=True, derivatives=False, high_risk_only=False, confirmation=68.0/100, focus=binance. Anchor listed but no derivatives confirmation; healthier than MEXC-only but no positioning data.
- INJ/USDT [rejected]: exchanges=['binance', 'mexc'], anchor=True, derivatives=False, high_risk_only=False, confirmation=85.0/100, focus=binance. Anchor listed but no derivatives confirmation; healthier than MEXC-only but no positioning data.
- GENIUS/USDT [rejected]: exchanges=['binance'], anchor=True, derivatives=False, high_risk_only=False, confirmation=68.0/100, focus=binance. Anchor listed but no derivatives confirmation; healthier than MEXC-only but no positioning data.

## 7d. Crowd Attention Stages

- BTC/USDT: stage early_attention, attention 100.0/100, momentum 56.3/100, crowding 0.0/100, confidence low
- ETH/USDT: stage unknown, attention 96.8/100, momentum 54.6/100, crowding 0.0/100, confidence low
- SAGA/USDT: stage unknown, attention 10.0/100, momentum 96.2/100, crowding 60.0/100, confidence low
- RENDER/USDT: stage unknown, attention 0.0/100, momentum 95.7/100, crowding 43.0/100, confidence low
- XRP/USDT: stage unknown, attention 20.0/100, momentum 52.6/100, crowding 0.0/100, confidence low
- NIL/USDT: stage unknown, attention 0.0/100, momentum 92.4/100, crowding 35.0/100, confidence low
- INJ/USDT: stage unknown, attention 0.0/100, momentum 91.5/100, crowding 43.0/100, confidence low
- BNB/USDT: stage unknown, attention 9.5/100, momentum 69.1/100, crowding 25.0/100, confidence low
- NEAR/USDT: stage unknown, attention 0.0/100, momentum 81.5/100, crowding 25.0/100, confidence low
- SAHARA/USDT: stage unknown, attention 0.0/100, momentum 80.9/100, crowding 0.0/100, confidence low

## 8. No-Trade Warnings

- Some evidence streams are partial; inspect source health before trading.
- If BTC loses local support, reduce long aggression immediately.
- Avoid extended entries. The system prefers missing a move over chasing a bad one.
- If derivatives/news are stale or missing for a symbol, reduce confidence.

## 9. Data Coverage / Blindspots

- ohlcv: ok: 30 cached symbols
- binance_futures: ok: 29 symbols
- bybit_okx_derivatives: partial/ok: 54 venue-symbol records
- rss_news: ok: 4 sources
- social_attention: partial/ok: 3 live sources, 4 symbols
- Partial/stale: OHLCV failures: 3 symbol/timeframe items
- Important blindspots still not automated:
- Liquidation heatmaps and leverage clusters are not connected yet.
- Order book depth, spreads, and CVD are not connected yet.
- ETF flows, stablecoin liquidity, DXY/yields, and macro calendar are not connected yet.
- On-chain whale flows and exchange inflow/outflow are not connected yet.
- Token unlock calendar is manual until TokenUnlocks/CryptoRank integration is added.
- Live X/Telegram/Discord/KOL feeds are manual until API/connectors are added.

## 10. Final Summary

No active trade clears the desk threshold. Best watchlist name is NIL/USDT at 60.4/100. Wait for cleaner execution.
