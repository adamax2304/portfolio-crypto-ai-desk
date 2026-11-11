# 📌 Trading Desk — Current State

_Refreshed: **2026-11-12 02:05 EEST** · Source: `proposed_signals` × latest `signal_outcomes`, live reports, catalyst JSONL, Opus reviews, process probe._

_Canonical dashboard file: `obsidian_vault/11 📌 Trading Desk Current State.md` (single pinned tab; no duplicates)._

> ✅ **Data freshness:** 8 min behind newest DB row (`2026-11-11 22:56 UTC`).

> **System status:** ⚠️ PARTIAL
> **Current focus:** crypto swing/intraday + crypto scalp (low-confidence); stocks intraday actionable; old stocks swing/invest DEPRECATED/REMOVED; new stocks_swing_growth_breakout shadow-only research.

This page is a single-screen sweep for a manual monitoring pass — top-to-bottom: what the system is doing → live trades → just-closed → news → recap → risks → mode routing → performance → manual checks. Sibling tabs: [[01 📌 Active Signals]] (raw active list), [[02 📌 Trade History]] (full history), [[10 📌 Performance by Mode]] (deep performance), [[07 📌 Schedule Status]] (raw health).

---

## 1. System Health

- Scheduler (default market schedule): ✅ running (PID `15496`, born `2026-11-11T10:54:57+00:00`)
- Telegram collector: ✅ running (PID `11156`, born `2026-11-11T10:54:38+00:00`)
- Crypto watchlist monitor: ✅ running (PID `13204`, born `2026-11-11T10:54:58+00:00`)
- Stocks intraday monitor: ✅ running (PID `15184`, born `2026-11-11T10:55:06+00:00`)

- Crypto LLM packet: `data/processed/llm_analysis_packet.md` (refreshed `2026-09-30 13:25 UTC`)
- Stocks LLM packet: `data/processed/llm_stocks_packet.md` (refreshed `2026-11-11 20:55 UTC`)
- Latest Opus enriched review: `OPUS_ENRICHED_REVIEW_AUTO_2026-09-09_1608.md` (`2026-09-09 13:13 UTC`)
- Untracked legacy crypto alerts (24h): ⚠️ `1`

**Issues:** 1 untracked legacy alerts.

## 2. Currently Open / Active Paper Trades

### Crypto

- _none_

### Stocks
- **REGN** · LONG · intraday · tier A · score 94 · [TradingView](https://www.tradingview.com/chart/?symbol=REGN)
  - Created: `2026-11-11 20:46 UTC` | Expires: `2026-11-12 20:46 UTC`, sector `healthcare`
  - Paper entry: not triggered yet.
  - SETUP — WAITING FOR ENTRY · No paper entry yet.
  - Entry zone: `917.29 – 921.53` | SL: `913.05` | TP1 `934.24` / TP2 `942.72` / TP3 `955.43`
  - Status: `missed_no_entry` | Legacy touch R (not PnL): +0.00R | MFE: +0.00R | MAE: +0.00R | catalyst: no
  - Playbook: `stocks_intraday_rth_momentum` · status **actionable** · overlays: —
  - Failure mode: _A-tier overpromotion on losing names — NVDA/SMCI/SMH longs structurally lose in this regime_
  - Manual review hint: _Spot-check chart structure against thesis; avoid NVDA/SMCI longs without strong catalyst._
  - Source report: `C:\Users\adama\Documents\crypto-ai-desk\data\reports\stocks\intraday\2026-11-11_20-50_stocks_intraday_report.md`
  - **Comment:** waiting for entry

- **REGN** · LONG · intraday · tier A · score 96 · [TradingView](https://www.tradingview.com/chart/?symbol=REGN)
  - Created: `2026-11-11 18:39 UTC` | Expires: `2026-11-12 18:39 UTC`, sector `healthcare`
  - Paper entry: not triggered yet.
  - SETUP — WAITING FOR ENTRY · No paper entry yet.
  - Entry zone: `917.29 – 921.53` | SL: `913.05` | TP1 `934.24` / TP2 `942.72` / TP3 `955.43`
  - Status: `missed_no_entry` | Legacy touch R (not PnL): +0.00R | MFE: +0.00R | MAE: +0.00R | catalyst: no
  - Playbook: `stocks_intraday_rth_momentum` · status **actionable** · overlays: —
  - Failure mode: _A-tier overpromotion on losing names — NVDA/SMCI/SMH longs structurally lose in this regime_
  - Manual review hint: _Spot-check chart structure against thesis; avoid NVDA/SMCI longs without strong catalyst._
  - Source report: —
  - **Comment:** waiting for entry

- **REGN** · LONG · intraday · tier A · score 96 · [TradingView](https://www.tradingview.com/chart/?symbol=REGN)
  - Created: `2026-11-11 18:39 UTC` | Expires: `2026-11-12 18:39 UTC`, sector `healthcare`
  - Paper entry: not triggered yet.
  - SETUP — WAITING FOR ENTRY · No paper entry yet.
  - Entry zone: `917.29 – 921.53` | SL: `913.05` | TP1 `934.24` / TP2 `942.72` / TP3 `955.43`
  - Status: `missed_no_entry` | Legacy touch R (not PnL): +0.00R | MFE: +0.00R | MAE: +0.00R | catalyst: no
  - Playbook: `stocks_intraday_rth_momentum` · status **actionable** · overlays: —
  - Failure mode: _A-tier overpromotion on losing names — NVDA/SMCI/SMH longs structurally lose in this regime_
  - Manual review hint: _Spot-check chart structure against thesis; avoid NVDA/SMCI longs without strong catalyst._
  - Source report: —
  - **Comment:** waiting for entry

## 3. Last 5 Crypto Trades

- **PEPE/USDT** · SHORT · intraday · tier B · score 65 · playbook `crypto_failed_bounce_short` · [TradingView](https://www.tradingview.com/chart/?symbol=BINANCE:PEPEUSDT)
  - Created: `2026-11-11 14:55 UTC` | Paper entry: `2026-11-11 15:14 UTC` | Time in trade: `4.4h`
  - Entry zone: `0.0000–0.0000` | SL: `0.0000` | TP1 `0.0000` / TP2 `0.0000` / TP3 `0.0000`
  - Outcome: **`win`** | Legacy touch R (not PnL): **+2.00R** | MFE: +3.00R | MAE: +0.00R | catalyst: no
  - **Comment:** Reached TP on momentum alone (no catalyst flag).

- **ZEC/USDT** · SHORT · intraday · tier B · score 65 · playbook `crypto_failed_bounce_short` · [TradingView](https://www.tradingview.com/chart/?symbol=BINANCE:ZECUSDT)
  - Created: `2026-11-11 14:40 UTC` | Paper entry: `2026-11-11 15:30 UTC` | Time in trade: `0.8h`
  - Entry zone: `988.79–1,000.05` | SL: `1,013.81` | TP1 `958.78` / TP2 `933.76` / TP3 `908.75`
  - Outcome: **`loss`** | Legacy touch R (not PnL): **-1.00R** | MFE: +0.71R | MAE: -1.07R | catalyst: no
  - **Comment:** Stopped: thesis invalidated.

- **UNI/USDT** · SHORT · intraday · tier B · score 67 · playbook `crypto_failed_bounce_short` · [TradingView](https://www.tradingview.com/chart/?symbol=BINANCE:UNIUSDT)
  - Created: `2026-11-11 10:59 UTC` | Paper entry: `2026-11-11 13:15 UTC` | Time in trade: `3.8h`
  - Entry zone: `6.50–6.55` | SL: `6.61` | TP1 `6.37` / TP2 `6.26` / TP3 `6.14`
  - Outcome: **`loss`** | Legacy touch R (not PnL): **-1.00R** | MFE: +0.92R | MAE: -1.21R | catalyst: no
  - **Comment:** Stopped after favorable run — possible squeeze/reversal. ⚠ gap slip past stop (real fill worse than reported R)

- **ZEC/USDT** · SHORT · intraday · tier B · score 66 · playbook `crypto_failed_bounce_short` · [TradingView](https://www.tradingview.com/chart/?symbol=BINANCE:ZECUSDT)
  - Created: `2026-11-10 02:44 UTC` | Paper entry: `2026-11-10 02:45 UTC` | Time in trade: `7.5h`
  - Entry zone: `1,160.54–1,171.07` | SL: `1,183.95` | TP1 `1,132.46` / TP2 `1,109.05` / TP3 `1,085.65`
  - Outcome: **`win`** | Legacy touch R (not PnL): **+1.00R** | MFE: +1.23R | MAE: -1.22R | catalyst: no
  - **Comment:** Reached TP on momentum alone (no catalyst flag). ⚠ gap slip past stop (real fill worse than reported R)

- **ZEC/USDT** · SHORT · intraday · tier B · score 67 · playbook `crypto_failed_bounce_short` · [TradingView](https://www.tradingview.com/chart/?symbol=BINANCE:ZECUSDT)
  - Created: `2026-11-09 16:44 UTC` | Paper entry: `2026-11-09 16:45 UTC` | Time in trade: `6.2h`
  - Entry zone: `1,183.59–1,194.88` | SL: `1,208.66` | TP1 `1,153.51` / TP2 `1,128.44` / TP3 `1,103.37`
  - Outcome: **`win`** | Legacy touch R (not PnL): **+3.00R** | MFE: +4.30R | MAE: -0.65R | catalyst: no
  - **Comment:** Reached TP on momentum alone (no catalyst flag).

## 4. Last 5 Stocks Trades

- **REGN** · LONG · intraday · tier A · score 94 · playbook `stocks_intraday_rth_momentum` · [TradingView](https://www.tradingview.com/chart/?symbol=REGN)
  - Created: `2026-11-11 20:46 UTC` | Paper entry: `not triggered` | Time in trade: `—`
  - Entry zone: `917.29–921.53` | SL: `913.05` | TP1 `934.24` / TP2 `942.72` / TP3 `955.43`
  - Outcome: **`not_triggered`** | Legacy touch R (not PnL): **+0.00R** | MFE: +0.00R | MAE: +0.00R | catalyst: no
  - **Comment:** Did not trigger: entry zone never reached.

- **REGN** · LONG · intraday · tier A · score 96 · playbook `stocks_intraday_rth_momentum` · [TradingView](https://www.tradingview.com/chart/?symbol=REGN)
  - Created: `2026-11-11 18:39 UTC` | Paper entry: `not triggered` | Time in trade: `—`
  - Entry zone: `917.29–921.53` | SL: `913.05` | TP1 `934.24` / TP2 `942.72` / TP3 `955.43`
  - Outcome: **`not_triggered`** | Legacy touch R (not PnL): **+0.00R** | MFE: +0.00R | MAE: +0.00R | catalyst: no
  - **Comment:** Did not trigger: entry zone never reached.

- **REGN** · LONG · intraday · tier A · score 96 · playbook `stocks_intraday_rth_momentum` · [TradingView](https://www.tradingview.com/chart/?symbol=REGN)
  - Created: `2026-11-11 18:39 UTC` | Paper entry: `not triggered` | Time in trade: `—`
  - Entry zone: `917.29–921.53` | SL: `913.05` | TP1 `934.24` / TP2 `942.72` / TP3 `955.43`
  - Outcome: **`not_triggered`** | Legacy touch R (not PnL): **+0.00R** | MFE: +0.00R | MAE: +0.00R | catalyst: no
  - **Comment:** Did not trigger: entry zone never reached.

- **NOW** · SHORT · intraday · tier B · score 75 · playbook `stocks_intraday_rth_momentum` · [TradingView](https://www.tradingview.com/chart/?symbol=NOW)
  - Created: `2026-11-10 20:23 UTC` | Paper entry: `not triggered` | Time in trade: `—`
  - Entry zone: `98.29–98.99` | SL: `99.68` | TP1 `96.20` / TP2 `94.81` / TP3 `92.72`
  - Outcome: **`not_triggered`** | Legacy touch R (not PnL): **+0.00R** | MFE: — | MAE: — | catalyst: no
  - **Comment:** Did not trigger: entry zone never reached.

- **TXN** · SHORT · intraday · tier B · score 90 · playbook `stocks_intraday_rth_momentum` · [TradingView](https://www.tradingview.com/chart/?symbol=TXN)
  - Created: `2026-11-06 20:47 UTC` | Paper entry: `not triggered` | Time in trade: `—`
  - Entry zone: `274.86–278.09` | SL: `281.32` | TP1 `265.17` / TP2 `258.70` / TP3 `249.01`
  - Outcome: **`not_triggered`** | Legacy touch R (not PnL): **+0.00R** | MFE: +0.00R | MAE: +0.00R | catalyst: no
  - **Comment:** Did not trigger: entry zone never reached.

## 5. Main Events Today

### Crypto

- _no notable catalysts captured in the last 24h_

### Stocks / Macro
- **GERMANY'S CHANCELLOR MERZ: GERMANY MUST DO EVERYTHING TO PRESERVE AAA CREDIT RATING ...** — _t.me/marketfeed_ · `2026-11-11 11:11 UTC`
  - Symbols: `—` | Type: `other_news` | Importance: `0.444`
- **RUSSIA’S MEDINSKY: BUSINESS-FRIENDLY ATMOSPHERE AT TALKS IN ABU DHABI; THE TALKS WILL CONTINUE, WORLD NEEDS NEW SECURITY SYSTEM ...** — _t.me/marketfeed_ · `2026-11-11 11:11 UTC`
  - Symbols: `—` | Type: `other_news` | Importance: `0.5`
- **RUSSIA: US ENVOYS HAVE CONSTRUCTIVE ROLE ...** — _t.me/marketfeed_ · `2026-11-11 11:10 UTC`
  - Symbols: `—` | Type: `other_news` | Importance: `0.5`
- **MEDINSKY: UNCLEAR WHAT RUSSIA CAN DISCUSS WITH EU AMID LACK OF PROPOSALS ...** — _t.me/marketfeed_ · `2026-11-11 11:10 UTC`
  - Symbols: `—` | Type: `other_news` | Importance: `0.5`
- **RUSSIA: RECEIVED NO SPECIFIC PEACE OFFERS FROM EUROPE ...** — _t.me/marketfeed_ · `2026-11-11 11:09 UTC`
  - Symbols: `—` | Type: `other_news` | Importance: `0.5`
- **EUROPE SECURITY WAS KEY FOCUS AT DISCUSSIONS ...** — _t.me/marketfeed_ · `2026-11-11 11:09 UTC`
  - Symbols: `—` | Type: `other_news` | Importance: `0.444`

_Note: catalyst→symbol mapping is partial — use as context, not as a trade trigger._

## 6. Main Events This Week

### Crypto narratives & catalysts (7d)
- **momentum_breakout** (source: single_source) — members: `UNI/USDT, AUCTION/USDT`
  - _Top gainers without confirmed news catalyst — pure momentum cluster. Movers: UNI/USDT +19.5% (vol 0.84x), AUCTION/USDT +15.7% (vol 0.57x). Threshold: 24h >= 10._
- **ai_narrative** (source: single_source) — members: `NEAR/USDT, RENDER/USDT, TAO/USDT, FET/USDT, WLD/USDT, ASTER/USDT`
  - _AI sector rotation — multi-symbol momentum, watch for crowding. Sample headlines: LATVIA ARMY: PEOPLE IN LUDZA REGION NEAR BELARUS BORDER TOLD TO SEEK SHELTER O_

- **Crypto winners (7d):** ZEC/USDT +4.00R, PEPE/USDT +2.00R
- **Crypto losers (7d):** ZEC/USDT -2.00R, UNI/USDT -2.00R

### Stocks / macro recap (7d)
- **Stocks winners (7d):** IWM +3.00R, XLI +2.00R, QQQ +1.00R, SMH +1.00R, XLK +1.00R
- **Stocks losers (7d):** NVDA -2.00R, CRWD -1.00R, INTC -1.00R, META -1.00R

## 7. Top Risks

### Crypto risks

- **P1** — BTC/ETH range/transition regime: breadth EMA50 only ~22%, edge is narrow. Treat broad longs cautiously.
- **P1** — Crypto scalp mode is **low-confidence** (1W/7L over 14d, PF 0.14); entry edge real but TP/horizon mismatch — see scalp banner.
- **P2** — Short funding still skewed: open shorts on majors face squeeze risk on news pops.
- **P2** — Thin-liquid alt scalps: avoid mid/low-cap shorts without volume confirmation.
- **P2** — Catalyst→symbol mapping partial: news-supported flag is reliable for swing/intraday but not for scalp.
- **P3** — A few crypto reports may carry stale `last_update` if a source 429s; the parallel-fetch fix improved this, monitor next 24h.

### Stocks risks

- **P1** — Stocks **swing** paused (12% WR, −30R over 14d); pause stays until C-tier counterfactual reaches 20 closures.
- **P1** — Stocks **invest** newly watchlist-only (0W/7L; same failure mode as swing).
- **P1** — **NVDA / SMCI longs** structurally losing (0/4 + 0/3 in 14d intraday) — treat any fresh A/B long on them with extreme skepticism.
- **P2** — A-tier stocks lifetime WR 18.8% (mostly the failed pre-pause swing/invest A's); intraday A-tier sample too small to grade post-pause.
- **P2** — Earnings calendar: confirm `severity != UNKNOWN` before acting; the ETF-UNKNOWN false-positive fix should hold but spot-check.
- **P2** — Headline/legal risk filter only catches matched RSS items; a fresh out-of-band catalyst can slip through.
- **P3** — Market-closed banner active outside RTH; do not chase pre-market without RTH confirmation.

## 8. Mode Routing Status

### Crypto
- **scalp** — ✅ active (annotated `low confidence`). Reason: real entry edge (100% expired with positive MFE, avg +0.54R) but TP1/2h horizon mismatch — capture limited.
- **intraday** — ✅ actionable. Catalyst-backed intraday strongly outperforms (PF 2.75) vs no-catalyst (PF 0.70).
- **swing** — ✅ actionable. Strongest mode: 12W/3L 14d, PF 9.00, +24R; catalyst not required.

### Stocks
- **intraday** — ✅ actionable. +84R / PF 2.17 / WR 56% over 14d B-tier.
- **swing** — 🛑 watchlist-only. Pre-pause 5W/36L (12% WR, −30R); pause cap = `stocks_swing_paused_after_48h_audit`.
- **invest** — 🛑 watchlist-only (new, 2026-06-09). 0W/7L 14d; cap = `stocks_invest_paused_after_mode_viability_audit`. Same failure mode as swing.

## 8b. Playbook Performance Snapshot (14d, A/B, deduped)

_Raw R total: **+20.0R** · playbook-aware sized total: **+18.5R** (see [reports/PROFITABILITY_LEVERS_AUDIT.md]; weights: `config/sizing_weights.yaml`)._

_R/PF columns = LEGACY TOUCH R (optimistic highest-TP-touched) — NOT PnL. Authoritative PnL is USD net (`paper_portfolio_ledger.net_pnl_usdt`) in the app._

| Playbook | n | closed | W | WR | PF(leg) | legacyTouchR |
|---|---:|---:|---:|---:|---:|---:|
| `crypto_swing_narrative_rs_momentum` (long) | 0 | 0 | 0 | — | — | +0 |
| `crypto_intraday_catalyst_or_momentum` (catalyst=1) | 0 | 0 | 0 | — | — | +0 |
| `crypto_intraday_catalyst_or_momentum` (no catalyst) | 32 | 26 | 8 | 31% | 0.78 | -4 |
| `crypto_scalp_momentum_continuation` (low-confidence) | 0 | 0 | 0 | — | — | +0 |
| `crypto_failed_bounce_short` | 12 | 10 | 6 | 60% | 2.75 | +7 |
| `stocks_intraday_rth_momentum` (long) | 51 | 7 | 4 | 57% | 4.00 | +9 |
| `stocks_intraday_rth_momentum` (short) | 135 | 14 | 9 | 64% | 4.00 | +15 |
| `stocks_swing_watchlist_rs_rotation` (DEPRECATED/REMOVED) | 0 | 0 | 0 | — | — | +0 |
| `stocks_invest_watchlist_30d_thesis` (DEPRECATED/REMOVED) | 0 | 0 | 0 | — | — | +0 |

Source: deduped `proposed_signals × latest signal_outcomes`, 14d. See [reports/STRATEGY_PLAYBOOK_AUDIT.md] for the full per-playbook contract.

## 9. Performance Snapshot

### Window: 48h
- **Crypto A/B overall:** n=4 closed=4 W=2 L=2 WR=50% PF(legacy-touch)=1.50 legacyTouchR=+1R (optimistic · NOT PnL)
  - intraday: n=4 closed=4 W=2 L=2 WR=50% PF(legacy-touch)=1.50 legacyTouchR=+1R (optimistic · NOT PnL)
  - short: n=4 closed=4 W=2 L=2 WR=50% PF(legacy-touch)=1.50 legacyTouchR=+1R (optimistic · NOT PnL)
  - news=0: n=4 closed=4 W=2 L=2 WR=50% PF(legacy-touch)=1.50 legacyTouchR=+1R (optimistic · NOT PnL)
- **Stocks A/B overall:** n=4 closed=0 W=0 L=0 WR=— PF(legacy-touch)=— legacyTouchR=+0R (optimistic · NOT PnL)
  - intraday: n=4 closed=0 W=0 L=0 WR=— PF(legacy-touch)=— legacyTouchR=+0R (optimistic · NOT PnL)
  - long: n=3 closed=0 W=0 L=0 WR=— PF(legacy-touch)=— legacyTouchR=+0R (optimistic · NOT PnL)
  - short: n=1 closed=0 W=0 L=0 WR=— PF(legacy-touch)=— legacyTouchR=+0R (optimistic · NOT PnL)
  - A-tier: n=3 closed=0 W=0 L=0 WR=— PF(legacy-touch)=— legacyTouchR=+0R (optimistic · NOT PnL)
  - B-tier: n=1 closed=0 W=0 L=0 WR=— PF(legacy-touch)=— legacyTouchR=+0R (optimistic · NOT PnL)

### Window: 7d
- **Crypto A/B overall:** n=9 closed=7 W=3 L=4 WR=43% PF(legacy-touch)=1.50 legacyTouchR=+2R (optimistic · NOT PnL)
  - intraday: n=9 closed=7 W=3 L=4 WR=43% PF(legacy-touch)=1.50 legacyTouchR=+2R (optimistic · NOT PnL)
  - long: n=2 closed=1 W=0 L=1 WR=0% PF(legacy-touch)=— legacyTouchR=-1R (optimistic · NOT PnL)
  - short: n=7 closed=6 W=3 L=3 WR=50% PF(legacy-touch)=2.00 legacyTouchR=+3R (optimistic · NOT PnL)
  - news=0: n=9 closed=7 W=3 L=4 WR=43% PF(legacy-touch)=1.50 legacyTouchR=+2R (optimistic · NOT PnL)
- **Stocks A/B overall:** n=50 closed=10 W=5 L=5 WR=50% PF(legacy-touch)=1.60 legacyTouchR=+3R (optimistic · NOT PnL)
  - intraday: n=50 closed=10 W=5 L=5 WR=50% PF(legacy-touch)=1.60 legacyTouchR=+3R (optimistic · NOT PnL)
  - long: n=3 closed=0 W=0 L=0 WR=— PF(legacy-touch)=— legacyTouchR=+0R (optimistic · NOT PnL)
  - short: n=47 closed=10 W=5 L=5 WR=50% PF(legacy-touch)=1.60 legacyTouchR=+3R (optimistic · NOT PnL)
  - A-tier: n=10 closed=0 W=0 L=0 WR=— PF(legacy-touch)=— legacyTouchR=+0R (optimistic · NOT PnL)
  - B-tier: n=40 closed=10 W=5 L=5 WR=50% PF(legacy-touch)=1.60 legacyTouchR=+3R (optimistic · NOT PnL)

### Window: 14d
- **Crypto A/B overall:** n=32 closed=26 W=8 L=18 WR=31% PF(legacy-touch)=0.78 legacyTouchR=-4R (optimistic · NOT PnL)
  - intraday: n=32 closed=26 W=8 L=18 WR=31% PF(legacy-touch)=0.78 legacyTouchR=-4R (optimistic · NOT PnL)
  - long: n=20 closed=16 W=2 L=14 WR=12% PF(legacy-touch)=0.21 legacyTouchR=-11R (optimistic · NOT PnL)
  - short: n=12 closed=10 W=6 L=4 WR=60% PF(legacy-touch)=2.75 legacyTouchR=+7R (optimistic · NOT PnL)
  - news=0: n=32 closed=26 W=8 L=18 WR=31% PF(legacy-touch)=0.78 legacyTouchR=-4R (optimistic · NOT PnL)
- **Stocks A/B overall:** n=186 closed=21 W=13 L=8 WR=62% PF(legacy-touch)=4.00 legacyTouchR=+24R (optimistic · NOT PnL)
  - intraday: n=186 closed=21 W=13 L=8 WR=62% PF(legacy-touch)=4.00 legacyTouchR=+24R (optimistic · NOT PnL)
  - long: n=51 closed=7 W=4 L=3 WR=57% PF(legacy-touch)=4.00 legacyTouchR=+9R (optimistic · NOT PnL)
  - short: n=135 closed=14 W=9 L=5 WR=64% PF(legacy-touch)=4.00 legacyTouchR=+15R (optimistic · NOT PnL)
  - A-tier: n=28 closed=1 W=1 L=0 WR=100% PF(legacy-touch)=∞ legacyTouchR=+3R (optimistic · NOT PnL)
  - B-tier: n=158 closed=20 W=12 L=8 WR=60% PF(legacy-touch)=3.62 legacyTouchR=+21R (optimistic · NOT PnL)

## 10. Manual Review Checklist

- **Stocks A-tier active candidates (manual gut-check):** AAPL (intraday), LLY (intraday), MSFT (intraday), AMD (intraday), AVGO (intraday), UNH (intraday), JPM (intraday), XLV (intraday)
- **NVDA/SMCI longs active (historically losing — extra scrutiny):** NVDA (intraday, B), SMCI (intraday, B), SMCI (swing, B)

Always also verify by hand:
- Open trades where the chart structure no longer matches the system thesis.
- Any signal with legal/headline/earnings risk in news feed.
- Any thin-liquid crypto short (squeeze risk).
- Any signal where TradingView shows a different regime than the report.

## 12. Low-Risk Diagnostics (additive, read-only)

### 12a. Skipped opportunity monitor (last 14d)

- C-tier signals: **1332** (0× weight, never produced sized R).
- Rejected ideas whose symbol LATER became A/B: **19** distinct symbols (= skip reversal candidates).
- Top skip reasons:
  - crypto intraday long against bearish-trend regime (audit cap): **291**
  - Derivatives data unavailable for this symbol.: **188**
  - Price is more than 2 ATR from EMA20; do not chase.: **121**
  - Catalyst risk event reduces setup quality.: **114**
  - Market regime is mixed; breakout failure risk is elevated.: **103**
- Detail: see [reports/SKIPPED_SIGNAL_OPPORTUNITY_AUDIT.md] + `reports/SKIPPED_SIGNAL_FOLLOWUP.csv`

### 12b. Expired positive-MFE monitor

- A/B trades expired with positive MFE (>+0.05R): **997**
- Of those, MFE ≥ +0.5R (potential partial-TP candidates): **453**
- Theoretical partial @+0.5R uplift: ≈ **+113.2R** (50% × 0.5R × n)
- Winner-cut risk: see [reports/EXPIRED_POSITIVE_MFE_OPPORTUNITY_AUDIT.md] — research only, no TP change.

### 12c. Crypto intraday short caution

- Total A/B crypto intraday shorts: **100**
- No-news shorts: **76** (caution label candidates)
- Realized R from no-news shorts (closed): **-1.0R**
- Caution label only; no hard filter — see [reports/CRYPTO_INTRADAY_SHORT_CAUTION_STUDY.md].

### 12d. Stocks intraday cluster ranking

- A/B stocks intraday signals in last 24h: **1**
- Cluster rank is **additive** (`#N/M` shown per signal); no alert suppression.
- Per-day ranking by cluster: see [reports/STOCKS_INTRADAY_CLUSTER_RANKING_AUDIT.md].

## 13. Manual Live Shadow Cockpit

_Operator-facing snapshot. Manual shadow only — auto-execution forbidden._

- Open paper trades: **9**
- Waiting setups (valid): **0**
- Stale / moved-away (do NOT manual-fill): **0**
- Paper-entry alerts today: **3** · last 48h: **12**
- Today legacy-touch R (optimistic · NOT PnL): **+0.0R**
- 48h legacy-touch R (optimistic · NOT PnL): **+4.0R**
  - _Authoritative PnL = USD net (gross − fees − slippage − funding) from `paper_portfolio_ledger.net_pnl_usdt`; realistic R = `paper_execution_r` (control-plane app). The R above is the legacy highest-TP-touched metric._
- Telegram sync: ⚠️ 12 failed sends

### Top allowed manual-shadow candidates (active or waiting)

| Symbol | Asset | Mode | Tier | Dir | Score | Status |
|---|---|---|---|---|---:|---|
| UNI/USDT | crypto | intraday | B | short | 66.8 | stopped |
| ZEC/USDT | crypto | intraday | B | short | 65.7 | stopped |
| PEPE/USDT | crypto | intraday | B | short | 65.4 | tp2_hit |
| ZEC/USDT | crypto | intraday | B | short | 65.1 | stopped |

### Forbidden / caution
- `crypto_scalp_momentum_continuation` — **SHADOW ONLY (0× sized weight)**. Generated for research only; do NOT mirror manually. 12m backtest net-negative after fees — see [reports/SCALP_KEEP_REWORK_DISABLE_DECISION.md]
- `stocks_swing_watchlist_rs_rotation` — DEPRECATED/REMOVED (0×; never sized; not paused-to-return)
- `stocks_invest_watchlist_30d_thesis` — DEPRECATED/REMOVED (0×; never sized; not paused-to-return)
- `stocks_swing_growth_breakout` — NEW shadow-only research framework (separate; not actionable/sized)
- Crypto intraday no-news shorts — caution per [reports/CRYPTO_INTRADAY_SHORT_CAUTION_STUDY.md]
- All C-tier / shadow / expansion candidates

### Journal
- [`reports/LIVE_SHADOW_TRADING_JOURNAL.md`](../reports/LIVE_SHADOW_TRADING_JOURNAL.md)
- [`reports/LIVE_SHADOW_TRADING_JOURNAL.csv`](../reports/LIVE_SHADOW_TRADING_JOURNAL.csv) — preserves manual decision / fill / R / notes columns across refreshes
- Today's verdict: [`reports/MANUAL_LIVE_SHADOW_TODAY_VERDICT.md`](../reports/MANUAL_LIVE_SHADOW_TODAY_VERDICT.md)

## 14. Catalyst & Derivatives Visibility (additive)

### 14a. Catalyst-backed vs technical (crypto A/B, closed)

| news_supported | n | wins | raw R |
|---|---:|---:|---:|
| 0 (technical-only) | 2248 | 463 | -9.0 |
| 1 (catalyst-backed) | 187 | 31 | -25.0 |

### 14b. Funding/OI archive status

- funding_snapshots rows: **22434** · oi_snapshots rows: **22416**
- Append-only; written best-effort each crypto report cycle. NOT read by scoring.

### 14c. Stocks catalyst labelling

- Stocks signals now labelled news_supported=1: **1414** (forward-only; flag fix landed 2026-06-15).

### 14d. Derived catalyst labels (signal_catalyst_labels)

- freshness: {'none': 14180, 'old(1022.9h)': 1, 'old(103.4h)': 1, 'old(105.1h)': 3, 'old(111.8h)': 1, 'old(126.8h)': 1, 'old(129.1h)': 2, 'old(129.8h)': 1, 'old(130.1h)': 2, 'old(1304.1h)': 1, 'old(131.0h)': 1, 'old(131.1h)': 1, 'old(131.5h)': 1, 'old(131.9h)': 1, 'old(132.0h)': 1, 'old(133.0h)': 1, 'old(133.9h)': 1, 'old(14.2h)': 1, 'old(141.3h)': 2, 'old(142.3h)': 1, 'old(143.1h)': 3, 'old(145.7h)': 2, 'old(145.9h)': 3, 'old(146.7h)': 1, 'old(148.3h)': 1, 'old(149.0h)': 1, 'old(149.2h)': 1, 'old(153.8h)': 2, 'old(154.0h)': 2, 'old(154.9h)': 1, 'old(155.5h)': 2, 'old(156.8h)': 1, 'old(158.5h)': 3, 'old(158.6h)': 4, 'old(159.3h)': 1, 'old(159.5h)': 1, 'old(160.8h)': 1, 'old(161.5h)': 1, 'old(161.7h)': 1, 'old(161.8h)': 1, 'old(162.0h)': 1, 'old(162.5h)': 1, 'old(162.7h)': 2, 'old(164.3h)': 1, 'old(164.4h)': 5, 'old(164.5h)': 3, 'old(164.7h)': 1, 'old(164.8h)': 2, 'old(1641.4h)': 1, 'old(165.2h)': 4, 'old(165.3h)': 1, 'old(165.4h)': 2, 'old(165.6h)': 1, 'old(165.8h)': 1, 'old(166.1h)': 1, 'old(166.2h)': 2, 'old(166.3h)': 1, 'old(166.4h)': 1, 'old(166.5h)': 2, 'old(166.7h)': 5, 'old(166.8h)': 1, 'old(167.0h)': 2, 'old(167.2h)': 1, 'old(167.3h)': 2, 'old(167.5h)': 2, 'old(167.7h)': 3, 'old(167.8h)': 7, 'old(168.0h)': 4, 'old(168.1h)': 2, 'old(168.2h)': 1, 'old(168.3h)': 1, 'old(168.4h)': 1, 'old(168.5h)': 1, 'old(168.7h)': 3, 'old(168.8h)': 4, 'old(168.9h)': 6, 'old(169.0h)': 4, 'old(169.1h)': 1, 'old(169.2h)': 3, 'old(169.3h)': 1, 'old(169.4h)': 1, 'old(169.5h)': 3, 'old(169.6h)': 4, 'old(169.7h)': 1, 'old(169.8h)': 13, 'old(169.9h)': 2, 'old(170.0h)': 1, 'old(170.1h)': 3, 'old(170.2h)': 5, 'old(170.3h)': 2, 'old(170.4h)': 7, 'old(170.6h)': 5, 'old(170.7h)': 3, 'old(170.8h)': 7, 'old(170.9h)': 1, 'old(171.0h)': 1, 'old(171.1h)': 3, 'old(171.2h)': 2, 'old(171.3h)': 5, 'old(171.4h)': 5, 'old(171.5h)': 3, 'old(171.6h)': 3, 'old(171.7h)': 3, 'old(171.8h)': 2, 'old(171.9h)': 5, 'old(172.0h)': 4, 'old(172.1h)': 3, 'old(172.2h)': 5, 'old(172.3h)': 3, 'old(172.4h)': 2, 'old(172.5h)': 3, 'old(172.6h)': 1, 'old(172.7h)': 5, 'old(172.8h)': 1, 'old(172.9h)': 1, 'old(173.0h)': 2, 'old(173.1h)': 1, 'old(173.2h)': 2, 'old(173.3h)': 3, 'old(173.4h)': 2, 'old(173.5h)': 2, 'old(173.6h)': 4, 'old(173.7h)': 2, 'old(173.8h)': 2, 'old(173.9h)': 2, 'old(174.0h)': 3, 'old(174.1h)': 7, 'old(174.2h)': 1, 'old(174.4h)': 1, 'old(174.5h)': 4, 'old(174.6h)': 3, 'old(174.7h)': 2, 'old(174.8h)': 1, 'old(174.9h)': 2, 'old(175.0h)': 2, 'old(175.1h)': 3, 'old(175.2h)': 2, 'old(175.3h)': 5, 'old(175.4h)': 3, 'old(175.5h)': 7, 'old(175.6h)': 4, 'old(175.7h)': 2, 'old(175.8h)': 4, 'old(175.9h)': 3, 'old(176.0h)': 1, 'old(176.1h)': 1, 'old(176.2h)': 3, 'old(176.3h)': 3, 'old(176.4h)': 4, 'old(176.5h)': 3, 'old(176.6h)': 2, 'old(176.7h)': 1, 'old(176.8h)': 2, 'old(176.9h)': 2, 'old(177.0h)': 4, 'old(177.1h)': 2, 'old(177.2h)': 1, 'old(177.3h)': 6, 'old(177.4h)': 2, 'old(177.5h)': 5, 'old(177.6h)': 1, 'old(177.7h)': 2, 'old(177.8h)': 3, 'old(177.9h)': 1, 'old(178.0h)': 4, 'old(178.1h)': 2, 'old(178.2h)': 6, 'old(178.3h)': 3, 'old(178.4h)': 5, 'old(178.6h)': 5, 'old(178.7h)': 4, 'old(178.8h)': 1, 'old(179.0h)': 4, 'old(179.1h)': 6, 'old(179.2h)': 3, 'old(179.3h)': 5, 'old(179.4h)': 4, 'old(179.5h)': 2, 'old(179.6h)': 6, 'old(179.7h)': 1, 'old(179.8h)': 3, 'old(179.9h)': 2, 'old(180.0h)': 4, 'old(180.1h)': 2, 'old(180.2h)': 5, 'old(180.3h)': 4, 'old(180.5h)': 2, 'old(180.6h)': 3, 'old(180.7h)': 2, 'old(180.8h)': 2, 'old(180.9h)': 2, 'old(181.0h)': 1, 'old(181.1h)': 5, 'old(181.2h)': 3, 'old(181.3h)': 5, 'old(181.4h)': 3, 'old(181.5h)': 1, 'old(181.6h)': 3, 'old(181.7h)': 3, 'old(181.8h)': 1, 'old(182.0h)': 3, 'old(182.1h)': 2, 'old(182.2h)': 4, 'old(182.3h)': 5, 'old(182.4h)': 2, 'old(182.5h)': 4, 'old(182.6h)': 2, 'old(182.7h)': 1, 'old(182.8h)': 2, 'old(183.1h)': 4, 'old(183.2h)': 1, 'old(183.3h)': 5, 'old(183.5h)': 2, 'old(183.6h)': 4, 'old(183.8h)': 6, 'old(183.9h)': 2, 'old(184.0h)': 1, 'old(184.1h)': 1, 'old(184.2h)': 2, 'old(184.3h)': 3, 'old(184.4h)': 2, 'old(184.7h)': 1, 'old(184.8h)': 2, 'old(185.0h)': 2, 'old(185.1h)': 6, 'old(185.2h)': 1, 'old(185.3h)': 1, 'old(185.4h)': 2, 'old(185.7h)': 1, 'old(185.9h)': 1, 'old(186.0h)': 2, 'old(186.1h)': 1, 'old(186.4h)': 2, 'old(186.5h)': 3, 'old(186.6h)': 1, 'old(186.7h)': 1, 'old(186.8h)': 1, 'old(186.9h)': 1, 'old(187.6h)': 1, 'old(188.1h)': 1, 'old(188.2h)': 1, 'old(188.3h)': 3, 'old(188.5h)': 1, 'old(188.6h)': 2, 'old(189.1h)': 3, 'old(189.3h)': 1, 'old(189.4h)': 2, 'old(189.5h)': 10, 'old(189.6h)': 3, 'old(189.9h)': 1, 'old(190.0h)': 1, 'old(190.3h)': 1, 'old(190.4h)': 2, 'old(190.9h)': 1, 'old(191.2h)': 1, 'old(191.4h)': 3, 'old(191.5h)': 1, 'old(191.6h)': 1, 'old(191.7h)': 2, 'old(191.8h)': 2, 'old(191.9h)': 1, 'old(192.1h)': 1, 'old(192.2h)': 2, 'old(192.3h)': 2, 'old(192.5h)': 1, 'old(192.7h)': 1, 'old(192.8h)': 1, 'old(193.1h)': 1, 'old(193.3h)': 1, 'old(193.5h)': 1, 'old(194.0h)': 1, 'old(194.1h)': 1, 'old(194.2h)': 1, 'old(194.4h)': 2, 'old(194.6h)': 1, 'old(194.9h)': 1, 'old(195.0h)': 1, 'old(195.1h)': 1, 'old(195.2h)': 1, 'old(195.5h)': 1, 'old(195.6h)': 1, 'old(195.8h)': 3, 'old(196.0h)': 1, 'old(196.3h)': 1, 'old(196.4h)': 1, 'old(196.5h)': 2, 'old(196.7h)': 3, 'old(196.8h)': 5, 'old(196.9h)': 1, 'old(197.1h)': 2, 'old(197.3h)': 1, 'old(197.7h)': 1, 'old(197.8h)': 2, 'old(198.0h)': 1, 'old(198.3h)': 1, 'old(198.4h)': 2, 'old(198.7h)': 4, 'old(198.9h)': 5, 'old(199.0h)': 1, 'old(199.1h)': 1, 'old(199.5h)': 1, 'old(199.6h)': 1, 'old(199.7h)': 1, 'old(199.9h)': 3, 'old(200.1h)': 1, 'old(200.4h)': 2, 'old(200.6h)': 1, 'old(200.7h)': 1, 'old(200.9h)': 2, 'old(201.0h)': 1, 'old(201.1h)': 2, 'old(201.2h)': 1, 'old(201.4h)': 3, 'old(201.6h)': 4, 'old(202.0h)': 2, 'old(202.1h)': 1, 'old(202.2h)': 2, 'old(202.3h)': 1, 'old(202.4h)': 1, 'old(202.6h)': 2, 'old(202.8h)': 1, 'old(203.3h)': 1, 'old(203.9h)': 1, 'old(204.0h)': 3, 'old(204.1h)': 2, 'old(204.6h)': 1, 'old(204.8h)': 1, 'old(204.9h)': 1, 'old(205.4h)': 2, 'old(205.6h)': 2, 'old(205.7h)': 1, 'old(205.8h)': 1, 'old(206.1h)': 1, 'old(206.4h)': 2, 'old(206.5h)': 1, 'old(206.7h)': 3, 'old(207.6h)': 1, 'old(207.9h)': 1, 'old(208.1h)': 2, 'old(208.4h)': 2, 'old(209.0h)': 2, 'old(209.1h)': 2, 'old(210.6h)': 2, 'old(211.1h)': 1, 'old(211.4h)': 1, 'old(211.5h)': 1, 'old(211.8h)': 1, 'old(212.8h)': 1, 'old(213.4h)': 1, 'old(213.6h)': 1, 'old(214.1h)': 2, 'old(214.3h)': 1, 'old(215.2h)': 1, 'old(215.6h)': 1, 'old(223.9h)': 1, 'old(224.8h)': 1, 'old(225.0h)': 1, 'old(226.8h)': 1, 'old(227.2h)': 1, 'old(244.3h)': 1, 'old(249.3h)': 1, 'old(25.3h)': 2, 'old(25.6h)': 1, 'old(259.6h)': 1, 'old(259.9h)': 1, 'old(26.5h)': 2, 'old(29.0h)': 1, 'old(299.9h)': 1, 'old(30.6h)': 1, 'old(314.9h)': 1, 'old(357.1h)': 1, 'old(364.0h)': 1, 'old(47.8h)': 1, 'old(49.4h)': 1, 'old(51.6h)': 2, 'old(52.0h)': 1, 'old(53.0h)': 2, 'old(55.7h)': 2, 'old(56.0h)': 1, 'old(561.6h)': 1, 'old(59.9h)': 1, 'old(606.5h)': 2, 'old(620.5h)': 1, 'old(627.0h)': 2, 'old(69.7h)': 1, 'old(708.5h)': 1, 'old(71.8h)': 1, 'old(742.0h)': 1, 'old(83.5h)': 2, 'old(85.0h)': 2, 'old(850.6h)': 1, 'old(871.7h)': 1, 'recent(?)': 881}
- derivatives: {'OI-up': 2261, 'funding-supportive': 662, 'no-squeeze': 501, 'not-available': 12454, 'squeeze-risk': 14}
- Display-only derived table; safe to rebuild. See [reports/CATALYST_LABEL_BACKFILL_REPORT.md].

---

_Page generated: `2026-11-11T23:05:04+00:00`_  
_Source: `scripts/write_obsidian_current_state_dashboard.py` — read-only._  
_Re-run: `python -m scripts.write_obsidian_current_state_dashboard`._

