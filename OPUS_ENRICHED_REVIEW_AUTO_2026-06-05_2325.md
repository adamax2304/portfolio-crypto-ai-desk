# Opus Enriched Review — post-close final daily review — Auto Cycle 23:25 EEST

- **Generated:** 2026-06-05 23:25 EEST (auto-enriched-review, scheduled task `opus-enriched-review-postclose`, **post-close final daily review** slot 23:15). US cash session **closed** at 23:00 EEST / 16:00 ET. This is the daily wrap — how the day resolved, what worked/failed, end-of-day exposure, and the overnight-into-Asia setup for crypto.
- **Slot focus:** daily wrap of a hard risk-off Friday — the AVGO-led, jobs-report-fueled AI/semiconductor rout that ended the S&P's 9-week winning streak, and the overnight read for crypto into the weekend.
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-05_2139.md` (late-session risk review, 21:39 EEST, ~1h45m ago — §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). Verified the **final close**: **S&P 500 −2.65% to 7,357 (9-week win streak ended), Nasdaq Composite −~4% to ~25,725 (biggest drop since the early-2025 tariff turmoil), Nasdaq-100 −4.77% to 28,765, Dow −1.20%/−1.35% to ~50,715, VIX ~21.5**; driver = **hot May jobs (172k vs ~88k est, unemployment 4.3%)** → 10y >4.5%, 30y >5%, Fed-hike repricing, on top of **AVGO's soft AI guidance** (2-day chip rout: MRVL −12%, MU −11%, INTC −9%, AMD −10%, NVDA −4/−6%, AVGO −6% after −13% Thu); **META −7%** on news of a tens-of-billions secondary share offering (FT); ~**$1T** market cap wiped (TheStreet). WebFetch verified on TradingEconomics (HTTP 200); TheStreet + CNBC live blogs returned 403 (numbers cross-confirmed via WebSearch snippets).
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; all internal price/structure is local OHLCV/ATR/EMA report fields + cited external prints.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

- **The day closed as a confirmed, broad risk-off session, and the engine is now fully aligned with it — the multi-timeframe regime conflict that ran all day has resolved.** At the close all three stock horizons read **risk_off / bias short**: intraday (VIX 20.10, breadth 25%), swing (VIX 18.87, watchlist-only), and the post-close stale-bullish A-tier LONGS (LLY/AAPL/AMD) that dominated the 18:30–21:30 reviews are **gone**. The swing book now lists only AMD as a capped C-long and the intraday book demotes LLY/UNH longs to penalized C while **rejecting** JPM/XLV/XLF longs as `long_in_risk_off_regime`. The day's central tension self-corrected — but late.
- **What worked today: the short / risk-off read.** The intraday engine flipped to risk_off and led with shorts (META A 81.41, AMZN/TSLA/QQQ/XLK/AMD B) — direction-correct into a −2.65% S&P / −4% Nasdaq close. The crypto book stayed short-biased (TON/ETH/FET/NEAR/ADA breakdown shorts) and aligned with the de-risking tape.
- **What failed today: the stale-bullish A-tier stock LONGS.** AMD's A-tier swing long (scored under the morning bullish regime, `news_supported=0`) sat live while AMD printed **−10%** in the chip rout; AAPL/LLY A-longs were carried for hours against a confirmed −4% Nasdaq. The cost is in the tape: **stocks A-tier week PF 0.30, winrate 11.8%, −7R** — the single worst bucket. The `regime-vs-catalyst` / `swing-invest-regime-staleness` TODOs are now fully realized, not hypothetical (carried forward in §14).
- **End-of-day exposure is clean by accident of the close, not by design.** Because the market is shut, all stock A/B ideas are demoted to non-actionable C; there is no fresh long on the board and nothing new to act on overnight in equities. The residual live risk is **crypto**, which trades through the weekend on **~10h-stale levels** (scalp/intraday reports failed to regenerate this cycle — see §3).
- **Overnight-into-Asia (crypto):** the hawkish-Fed / yields-up macro that drove the equity rout is the through-line bleeding into crypto risk. Regime **bearish trend (risk-off)**, BTC/ETH downtrend, altcoin breadth 27%, deeply oversold (elevated ATR pct). **Short-biased / no-chase**, but oversold relief-bounce + weekend-gap risk cap any short-chasing. **Re-pull fresh crypto levels before any execution** — direction-only tonight.
- **Net verdict:** **No clean fresh long anywhere. Stocks = no action (market closed, all ideas C).** **Crypto = short-biased no-chase into Asia on stale levels — direction context only, respect oversold bounce + weekend gap.** Catalyst layer **context-only (72.7% unmapped).**

---

## 2. Data Used

**Internal — fresh (<4 h):**
- `data/reports/stocks/intraday/2026-06-05_20-17_stocks_intraday_report.md` (data 20:16 UTC; regenerated end-of-cycle ~23:03 EEST — **fresh**). Header: **MARKET CLOSED — planning/watchlist only.** Regime **risk_off** (VIX 20.10, breadth above EMA20 25%, bias short). Top (demoted) ideas: META short A 81.41, AMZN short B 76.99, TSLA short B 75.16; longs LLY/UNH only C (penalty −12).
- `data/reports/stocks/swing/2026-06-05_19-07_stocks_swing_report.md` (data 19:07 UTC; **~1.3 h — fresh**). Regime **risk_off** (VIX 18.87); **watchlist-only** (48h audit −12R, 0W/12L). Only AMD C-long (capped), NVDA C-short.

**Internal — carry-forward / stale (>4 h):**
- `data/reports/scalp/2026-06-05_13-30_scalp_report.md` (data 13:30 UTC; **~10 h — STALE**). Crypto scalp; **did not regenerate this cycle** (binance fetch timeout — see §3/§14).
- `data/reports/intraday/2026-06-05_13-54_intraday_report.md` (data 13:54 UTC; **~9.5 h — STALE**). Crypto intraday; report generation **timed out** this cycle (45-min CLI timeout).
- `data/reports/swing/2026-06-05_14-34_swing_report.md` (data 14:34 UTC; **~9 h — stale**). Crypto swing.
- `data/reports/stocks/invest/2026-06-05_14-55_stocks_invest_report.md` (data 14:55 UTC; **~8.5 h — carry-forward**, not re-read in detail; superseded by the fresh intraday/swing risk_off read).

**Catalyst / narrative:** `data/catalysts/2026-06-05/` — `catalyst_events.jsonl` (**2803 rows**), `narrative_baskets.jsonl` (**3 baskets**), latest `catalyst_cycle_20-03.md` (mtime 23:03).

**LLM packets:** `data/processed/llm_stocks_packet.md` (mtime 23:17 — fresh), `data/processed/llm_analysis_packet.md` (mtime 17:34).

**CLI / DB (read-only, from the 23:0x scheduler cycle — <30 min):** `active-signals` (crypto **16**, stocks **20**), `signal-stats` (crypto + stocks, week), `detect_untracked_legacy_alerts --since 2026-06-05` → **1 untracked** (FET/USDT B scalp short, carry-forward). Cycle `cycle_01_22-07_summary.md` (mtime 23:20).

**External (this run — cited §13):** final-close indices/VIX (TradingEconomics WebFetch-verified HTTP 200; CNBC/TheStreet via WebSearch); jobs-report / rate-hike / yields driver; AVGO chip-rout + META secondary-offering.

**Unavailable / blind:** live tick prints; TradingView/Chrome chart verification (not loaded); liquidation heatmaps / order-book / CVD; live ETF-flow feed; **fresh crypto scalp/intraday levels (reports ~9.5–10 h stale, regen failed this cycle).**

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-05_default_schedule/`.
- `scheduler.log` mtime **23:21 EEST → ~4 min** (fresh). Latest cycle summary `cycle_01_22-07_summary.md` mtime **23:20 EEST → ~5 min** (fresh, well under 3 h).
- **NO DEFER** — both freshness anchors are <5 min; the BOTH-older-than-3 h defer condition is not met.
- **Report freshness this run:**
  - **Fresh (<4 h):** stocks intraday (regenerated ~23:03 post-close), stocks swing (~1.3 h).
  - **STALE (>9 h):** crypto scalp (~10 h), crypto intraday (~9.5 h), crypto swing (~9 h). **The crypto scalp + intraday report generators FAILED this cycle** — the cycle summary shows step 2 *crypto scalp report* exited 1 (`RequestTimeout: binance GET .../exchangeInfo`) and step 3 *crypto intraday report* exited −1 (timed out after 2700 s). Crypto direction context is still valid (bearish trend persists) but **execution levels are stale — re-pull before any crypto entry.** → §14 `TODO-crypto-report-staleness` (now with a concrete root cause: Binance API timeout + intraday CLI 45-min timeout).

---

## 4. What Changed vs Previous Review (21:30 → post-close 23:15)

- **The market closed; the regime conflict resolved.** At 21:30 the stocks swing/invest book was still *bullish* with **active A-tier LONGS** (LLY/AAPL/AMD) fighting a flipped intraday risk_off read. Post-close, **the swing book itself flipped to risk_off** (watchlist-only) and **the A-tier longs are gone** — intraday now carries LLY/UNH only as penalized C-longs and *rejects* JPM/XLV/XLF longs. The primary `TODO-stocks-swing-invest-regime-staleness` resolved on its own, but only after the lag cost was realized.
- **The selloff resolved into the final print (verified).** 21:30 had intraday Nasdaq −3.8% / VIX 19.1; the **close** was worse: **S&P −2.65% (7,357), Nasdaq Composite ~−4% (~25,725), Dow −1.2/−1.35%, VIX ~21.5** — the S&P's **9-week winning streak ended**, ~$1T wiped. The "wait for an AMD reclaim" condition never triggered; price closed at/near lows.
- **New end-of-day catalyst detail:** **META −7% on a tens-of-billions secondary share offering (FT)** — an idiosyncratic dilutive overhang on top of the macro/AI-derating tape (the 21:30 META short thesis was risk-off beta; now there is a name-specific bearish catalyst too). JPM upgraded TSLA to neutral (PT $475) — a lone constructive note in a red tape.
- **A-tier failure realized, then cleared.** AMD A-long closed −10% on the day; stocks **A-tier week PF fell to 0.30 / winrate 11.8% / −7R**. The post-close re-score removed the A-longs, so the live exposure is now clean — but the week's A-tier R confirms the regime-gate gap was costly.
- **Crypto reports went from ~5 h stale (21:30) to ~9.5–10 h stale and FAILED to regenerate** this cycle (concrete failures logged) — a worsening freshness regression.
- **Untracked legacy alert: still 1** (FET/USDT B scalp short, 13:38) — unchanged carry-forward.
- **Catalyst mapping:** 72.9% unmapped (21:30) → **72.7% unmapped** — essentially flat, still context-only.

---

## 5. Catalyst Coverage

- Raw `catalyst_events.jsonl`: **2803 rows.**
- Mapped (non-null symbol): **766** · Unmapped (null symbol): **2037** · **Unmapped = 72.7%.**
- `narrative_baskets`: **3** — `perps_dex_narrative` (primary HYPE; related DYDX/GMX/ASTER; playbook wait_pullback; <24h; Hyperliquid UK-FCA-warning headline), `ai_narrative` (primary NEAR/RENDER/TAO/FET; related WLD/ASTER; related_beta_rotation; <6h — note this is a *downside* rotation: FET −18%/day, NEAR −24%), `momentum_breakout` (primary HEI +14.7%; <1h; no confirmed news).
- **⚠ CATALYST MAPPING WEAK THIS RUN (72.7% unmapped > 50%) — use the catalyst layer as CONTEXT, NOT a final decision input.**
- **Top unmapped headlines (representative):** the unmapped set is structurally dominated by **US-equity / macro headlines** — the AI-semis slide, the May jobs report, the Fed-hike/yield commentary, the META secondary-offering wire — that the crypto-oriented resolver cannot map to a `/USDT` pair, plus equity tickers mis-routed to fake `/USDT` symbols (UNH/USDT, JPM/USDT, TSLA/USDT, SMCI/USDT appear in the crypto catalyst stream). See §14 `TODO-catalyst-stock-usdt-mismap`.
- Highest-importance mapped catalysts today: **ZEC** exploit ("Massive ZCash Exploit Found by Claude", 0.78), **SMCI** legal (Form 8-K / Mar-19 export-control indictment, 0.77), **UNH** DOJ-probe legal cluster (0.73 ×3).

---

## 6. Market Landscape

- **Stocks (CLOSED — daily wrap):** A confirmed broad risk-off Friday. **Verified close: S&P 500 −2.65% to 7,357 (first down week in 10 — 9-week streak broken), Nasdaq Composite ~−4% to ~25,725 (worst day since early-2025 tariff turmoil), Nasdaq-100 −4.77% to 28,765, Dow −1.20/−1.35% to ~50,715, VIX ~21.5.** Two drivers stacked: (1) **AVGO's soft AI guidance** ignited a 2-day semiconductor rout (MRVL −12%, MU −11%, INTC −9%, AMD −10%, NVDA −4/−6%, AVGO −6% after −13% Thu); (2) the **hot May jobs report (172k vs ~88k est, unemployment 4.3%)** spiked yields (10y >4.5%, 30y >5%) and repriced a hawkish Fed. Plus **META −7%** on a multi-tens-of-billions secondary offering. The Dow's relative outperformance (−1.2% vs Nasdaq −4%) confirms the **value/defensive-over-growth rotation**; healthcare/financials were the only relative havens, but in a −2.65% tape even they bled. **All A/B stock ideas are non-actionable into the close; nothing to do overnight in equities.**
- **Crypto (live 24/7, levels ~9.5–10 h stale):** Regime **bearish trend (risk-off)**; BTC & ETH downtrend; altcoin breadth ~27%; elevated ATR percentile (high vol). The equity de-risking + hawkish-Fed repricing carries straight into crypto risk appetite. The AI-token basket (NEAR/FET/TAO) is in a *downside* rotation, not a bid; ZEC sits −39% on the counterfeiting-exploit. Style: **short bias or no trade; avoid weak altcoin longs.** Deep oversold → relief-bounce squeeze risk caps short-chasing; weekend liquidity thins.
- **Macro cross-asset through-line:** strong jobs → hawkish Fed → yields up is the single force hitting **both** books. Equities found defensives as a haven; **crypto has no haven, only "less-short."** Into Asia, watch whether the yields/Fed repricing extends or fades on any weekend headline.

---

## 7. Candidate Deep Dives (≤5)

This is a post-close wrap: **stocks are closed → no fresh actionable stock entries exist.** Deep dives focus on (a) the day's resolved A-tier-long failure as a lesson, (b) the META name-specific catalyst, and (c) the only live book — crypto — for the overnight read.

### 7.1 AMD — stocks A swing long (day's failure, now cleared) — **AVOID confirmed; lesson logged**
- **What happened:** the A-tier swing long (scored ~81 under the morning bullish regime, `news_supported=0`) stayed live while AMD closed **−10%** in the chip rout. Post-close the swing book demoted AMD to a **C-long (61.59, penalty −12)** and intraday lists AMD only as a **B short (72.14, penalty −10)**.
- **Price-reaction / chase check:** price closed at/near the lows after a 2-day vertical decline; any long-continuation entry would have been a falling knife. The entry band was never reclaimed.
- **Verdict:** **AVOID (realized).** The exposure is now cleared by the post-close re-score. Reconsider only on a decisive reclaim of the entry band with SMH stabilizing and VIX back under ~17. Feeds §14 `TODO-regime-vs-catalyst-gate`.

### 7.2 META — stocks short A intraday (81.41, top fresh stock score) — **direction-aligned + NEW name catalyst, but CLOSED / chase risk**
- **Setup:** breakdown SHORT, top intraday score (A 81.41, high confidence); communications the weakest sector.
- **Catalyst (verified, CONFIRMS short):** **META −7% on news it weighs raising tens of billions in a new secondary share sale (FT)** — a dilutive overhang, idiosyncratic and bearish, layered on the AI-derating tape. This upgrades the 21:30 "risk-off beta" thesis to a name-specific bearish catalyst.
- **Price-reaction / chase check:** already down ~7% on the day into the close; **the move is largely spent for today.** Market is shut — not actionable now. If it remains a setup at the next open, short only on a **failed bounce into the entry zone**, never chasing a gap-down.
- **Verdict:** **WATCH for the next session** — direction-aligned with a real catalyst, but closed + extended; no chase.

### 7.3 Crypto B-tier short book (TON 68 / ETH / FET 67 / NEAR / ADA / PUMP) — **the only live book; SHORT-biased no-chase on STALE levels**
- **Setup:** entire active crypto book is **B-tier breakdown SHORTS** — TON (scalp 68 waiting, intraday 65.8), ETH (scalp tp1), FET 67, NEAR/ADA/PUMP intraday triggered. Direction aligns with the bearish regime and the risk-off macro.
- **Catalyst:** AI-token downside rotation (FET −18%/day, NEAR −24% headlines); ZEC −39% exploit (separate, long-invalidated). No bullish crypto catalyst on the board.
- **Price-reaction / chase check:** **levels are ~9.5–10 h stale and failed to regenerate this cycle** — entry/SL/TP numbers may be materially off. BTC/ETH are deeply oversold; a relief-bounce squeeze is the main risk to fresh shorts. Weekend-gap / thin-liquidity risk into Saturday.
- **Verdict:** **SHORT-biased, NO-CHASE, direction-only.** Re-pull fresh levels before any execution; enter only on **failed bounces** with honored invalidations; a BTC reclaim of recent support (~$62–63K, per prior review context) neutralizes the short. Small size given B-tier triggered winrate ~22% / PF 1.33.

### 7.4 ZEC — crypto (exploit −39%) — **NO TRADE / watchlist**
- **Catalyst (verified internal, importance 0.78):** "Massive ZCash Exploit Found by Claude, extent unknown" (Decrypt) — counterfeiting/supply vulnerability; ZEC −39%.
- **Verdict:** any long INVALIDATED; short is late/extended after a −39% collapse. Watchlist only.

### 7.5 UNH / SMCI — stocks legal-gated (carry-forward) — **AVOID LONG**
- **LEGAL/HEADLINE RISK (verified internal, §I):** **UNH** DOJ Medicare/antitrust probe (legal cluster importance 0.73 ×3; shares −16% on the fraud-probe headline); **SMCI** standing **Mar-19-2026 indictment of three individuals re alleged export-control violation conspiracy** (SEC EDGAR Form 8-K) plus accounting/auditor history. Post-close UNH appears only as a penalized C-long (−12); SMCI not in the fresh top book.
- **Verdict:** **AVOID any long** on both per §I — never a clean actionable while the legal overhang stands. MANUAL REVIEW. Feeds §14 `TODO-unh-legal-gate`.

**Excess candidates (>5, deferred):** AMZN/TSLA/QQQ/XLK/SPY/SMH/NVDA/AAPL intraday B-shorts (all risk-off beta, closed, non-actionable); other crypto B-shorts (ZRO, etc.) — same bearish-aligned thesis; HEI (crypto momentum_breakout +14.7%, no news) — watchlist only.

---

## 8. Best Candidates Ranked

*(Post-close: equities closed → ranking reflects overnight actionability. Crypto is the only live book.)*

1. **Crypto B-tier short book (TON/ETH/FET/NEAR/ADA)** — *the only live, direction-aligned book.* SHORT-biased, NO-CHASE, **re-pull stale levels first**; oversold relief-bounce + weekend-gap risk → small size, failed-bounce entries only.
2. **META (stocks, A intraday short, 81.41)** — *WATCH next session.* Direction-aligned + new dilutive secondary-offering catalyst, but closed and already −7%; no chase.
3. **AMZN / TSLA / QQQ / XLK (stocks, B intraday shorts)** — *WATCH.* Risk-off beta, non-actionable into the close; re-evaluate on fresh levels at the next open.
4. *(no long candidate clears)* — every long on the board is a penalized C or rejected `long_in_risk_off_regime`; no clean fresh long anywhere.

---

## 9. Avoid / No Trade

- **All stock LONGS** — AVOID. Regime risk_off across intraday + swing; JPM/XLV/XLF longs rejected `long_in_risk_off_regime`; LLY/UNH demoted to penalized C. The morning's A-tier LLY/AAPL/AMD longs already cost the A-tier bucket (−7R, PF 0.30).
- **UNH / SMCI LONG** — AVOID (per §I): DOJ probe (UNH) and Mar-19 export-control indictment (SMCI) legal overhangs uncleared → MANUAL REVIEW.
- **Chasing crypto shorts into the oversold flush / weekend gap** — no-chase; failed bounces only; re-pull stale levels first.
- **Acting on ~9.5–10 h-stale crypto levels** — re-pull before any crypto execution; tonight is direction-only.
- **ZEC (crypto)** — exploit-driven −39%; long invalidated, short late. Watchlist only.
- **Crypto longs generally** — regime bearish, breadth 27%, AI-token basket in downside rotation; avoid weak altcoin longs.

---

## 10. Main Risks

- **Crypto execution on stale levels (primary live risk):** scalp/intraday reports ~9.5–10 h old and **failed to regenerate** (Binance API timeout + intraday CLI 45-min timeout). Entry/SL/TP numbers may be materially wrong. Mitigation: direction-only tonight; re-pull before any entry.
- **Weekend-gap risk:** crypto trades through Sat/Sun on thinning liquidity; a weekend macro headline (Fed/yields follow-through, or a relief bid) can gap positions. Mitigation: small size, no new exposure on stale levels.
- **Oversold relief-bounce (crypto):** BTC/ETH deeply oversold (elevated ATR pct); a squeeze could stop breakdown shorts. Mitigation: no-chase, failed-bounce entries.
- **Monday gap risk (stocks):** the close at/near lows in a −2.65% S&P / −4% Nasdaq tape, with the streak broken and VIX ~21.5, leaves elevated weekend-headline and Monday-gap risk in equities; no positions are live, so this is watch-only.
- **A-tier-long regime-gate gap (model risk, realized this week):** the A-tier stock bucket sits at PF 0.30 / −7R because long signals inherited a stale bullish-regime bonus against bearish catalysts. Self-corrected post-close but the lag is the lesson. §14 `TODO-regime-vs-catalyst-gate` / `TODO-stocks-swing-invest-regime-staleness`.
- **Catalyst layer weak (72.7% unmapped):** equity tickers mis-routed to `/USDT`; context-only this run.
- **Ingest:** if the source-ingest CLI fails, sources still live in §13 + the JSON artifact (no data loss).

---

## 11. Action Plan — next 4 hours (overnight into Asia)

1. **Stocks:** **no action — market closed.** Nothing actionable overnight. Re-evaluate on fresh levels at/after the 09:30 ET open (16:30 EEST Mon). Carry META (short, new secondary-offering catalyst) and the AMZN/TSLA/QQQ/XLK shorts to the next-open watchlist; longs stay off until the regime turns.
2. **Crypto (TON/ETH/FET/NEAR/ADA):** short bias intact — **re-pull fresh levels first** (reports ~10 h stale, regen failed), then enter only on **failed bounces**, honor invalidations; **no chasing** the oversold flush. A BTC reclaim of recent support (~$62–63K) neutralizes shorts. Small size (B-tier winrate ~22%).
3. **ZEC:** no trade — exploit-invalidated long, late short. Monitor for an exploit-resolution headline only.
4. **Weekend posture:** keep size minimal into the weekend; avoid initiating new crypto exposure on stale levels over the Sat/Sun gap; treat any weekend bounce as relief, not reversal, until BTC reclaims structure.
5. **Operational:** flag the crypto report-regen failure (Binance timeout) for the next manual session (§14) — the overnight crypto read is degraded until the scalp/intraday generators succeed.
6. **Re-read the next fresh crypto reports before acting** — the scheduler will retry next cycle; direction-only until levels refresh.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** **SHORT-BIASED, no-chase, levels STALE (~10 h, regen failed).** Bearish regime persists; re-pull scalp levels before any entry; oversold relief-bounce risk → small size. B-tier triggered winrate ~22% / PF 1.33.
- **Crypto intraday:** **SHORT-BIASED / selective, levels STALE.** TON short best name; NEAR/ADA/PUMP triggered shorts aligned; no longs; re-pull levels, no-chase, weekend-gap aware.
- **Crypto swing:** **NO-TRADE / caution.** Regime bearish; ZEC long INVALIDATED (−39% exploit); avoid weak altcoin longs.
- **Stocks intraday (fresh, risk_off, CLOSED):** **No actionable setups — market closed, all A/B demoted to C.** Top idea META short A 81.41 carries a new secondary-offering catalyst → WATCH next open, no chase. Longs rejected `long_in_risk_off_regime`.
- **Stocks swing (fresh, risk_off, watchlist-only):** **No-trade.** Swing capped to C pending 48h audit (−12R, 0W/12L); AMD C-long / NVDA C-short research-only; no A/B alerts.
- **Stocks invest (carry-forward ~8.5 h):** **Longs de-prioritized** while the AI-chip derating + hawkish-Fed repricing plays out; LLY's secular GLP-1 thesis intact for the longer horizon but not actionable into a risk-off close; SMCI/UNH excluded (legal).

---

## 13. Sources

**Final close / chip rout / macro driver (daily wrap — CONFIRM risk-off close):**
- [US stock market summary June 5 2026 — S&P 500 7,357.30 (−2.65%), Nasdaq-100 28,765.35 (−4.77%), Dow 50,714.61 (−1.20%), VIX 21.56; jobs 172k, 10y >4.5% / 30y >5% — TradingEconomics (WebFetch-verified HTTP 200)](https://tradingeconomics.com/united-states/stock-market)
- [Stock Market Today (June 5, 2026): Nasdaq falls ~4% (~25,725) as semiconductor slide wipes ~$1T from markets; Meta −7% on secondary offering — TheStreet (403 on fetch; numbers from WebSearch snippet)](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-05-2026)
- [Nasdaq drops the most in more than a year as chips tumble; S&P 500's 9-week winning streak set to end — CNBC live blog, 2026-06-05 (403 on fetch; cross-confirmed via WebSearch)](https://www.cnbc.com/2026/06/04/stock-market-today-live-updates.html)

**Chip selloff / individual names (internal report news rows, 2026-06-05):**
- [Stock market today: Dow, S&P 500, Nasdaq sink as jobs report fuels Fed hike bets, chip stocks sell off (Nasdaq −3.8%, S&P −2.25%, Dow −0.98%, VIX +24% to 19.09 — intraday) — Yahoo Finance](https://finance.yahoo.com/)
- [US Markets Decline Amid Chip Stock Selloff (MRVL −12%, MU −11%, INTC −9%, AMD −10%, AVGO −6%) — GuruFocus, 2026-06-05](https://www.gurufocus.com/)
- [NVDA, INTC, AMD, MU: Major Chip Stocks Fall For Second Day After AVGO's Soft AI Guidance — Stocktwits, 2026-06-05](https://stocktwits.com/)

**SMCI / UNH legal (LEGAL/HEADLINE RISK — gates the longs; internal catalyst rows):**
- [Super Micro Computer, Inc. — Form 8-K (FY2026), indictment of three individuals re alleged export-control violation conspiracy (filed Mar 19, 2026) — SEC EDGAR](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001375365&type=8-K)
- [UnitedHealth (UNH) Faces DOJ Probe, Shares Dive 16% on Fraud Investigation — QuiverQuant, 2026-06-05](https://www.quiverquant.com/)

_Intraday/late-session figures (Nasdaq −3.8% / VIX 19.09) are the pre-close prints carried in the internal report news rows; the final-close figures (S&P −2.65% / Nasdaq Composite ~−4% / VIX ~21.5) are the externally verified TradingEconomics/WebSearch numbers and supersede them for the daily wrap. Some source URLs above are landing pages (the specific article URLs 403'd on fetch); the figures were cross-confirmed across WebSearch snippets and the WebFetch-verified TradingEconomics page._

---

## 14. Fix Requests / TODO

### TODO-crypto-report-staleness (carry-forward — now with concrete root cause)
- **issue:** the crypto **scalp** and **intraday** report generators **failed this cycle**, leaving execution levels ~9.5–10 h stale through the post-close slot. Scalp exited 1 on a Binance API timeout; intraday exited −1 after the 2700 s (45 min) CLI timeout. The overnight crypto read is degraded.
- **evidence:** `cycle_01_22-07_summary.md` step 2 *crypto scalp report* `exit=1 … RequestTimeout: binance GET https://fapi.binance.com/fapi/v1/exchangeInfo`; step 3 *crypto intraday report* `exit=-1 … timed out after 2700 seconds`; latest crypto scalp `2026-06-05_13-30` (data 13:30 UTC), intraday `2026-06-05_13-54`.
- **suggested manual fix:** add a Binance fetch retry/backoff or a fallback exchange for `exchangeInfo`; investigate why crypto intraday exceeds the 45-min timeout (symbol-count / rate-limit); ensure a failed crypto report regen is surfaced louder than a single cycle-summary line.
- **priority:** high
- **first observed:** 2026-06-05 21:39 EEST (carry-forward; root cause identified this run)

### TODO-stocks-swing-invest-regime-staleness (carry-forward — resolved this run, keep for the fix)
- **issue:** the stocks swing/invest book kept a *bullish* regime + **A-tier LONGS** (LLY/AAPL/AMD) for hours after intraday flipped to risk_off; it only reconciled to risk_off at the post-close cycle, after AMD's A-long closed −10%. No real-time cross-timeframe regime reconciliation.
- **evidence:** prior reviews 18:30–21:30 carried A-tier LLY/AAPL/AMD longs vs a risk_off intraday; post-close swing report (19:07) now `risk_off`, A-longs gone; stocks A-tier week PF **0.30**, winrate **11.8%**, **−7R**.
- **suggested manual fix:** when the freshest intraday regime contradicts swing/invest intraday, down-tier/flag the longer-horizon longs or force a swing/invest re-score on an intraday regime flip; surface regime-age + cross-timeframe disagreement in `active-signals`.
- **priority:** high
- **first observed:** 2026-06-05 21:39 EEST (carry-forward)

### TODO-regime-vs-catalyst-gate (carry-forward — realized)
- **issue:** A-tier long signals inherit a +15 `market_regime_alignment` bonus from a 20-day "bullish" label even when the live catalyst is strongly bearish. AMD A-tier long (`news_supported=0`) closed **−10%** in the chip rout.
- **evidence:** AMD A swing long `news_supported=0`; AMD close −10% (GuruFocus); stocks A-tier week PF 0.30 / −7R.
- **suggested manual fix:** add a catalyst/headline gate demoting longs when fresh high-importance bearish news for the symbol/sector exists (mirror the §I legal-gate); surface `news_supported` + a sector-derating penalty in A-tier ranking.
- **priority:** high
- **first observed:** 2026-06-05 18:39 EEST (carry-forward)

### TODO-untracked-legacy-alert (carry-forward)
- **issue:** still 1 untracked legacy crypto alert — `FET/USDT` B scalp short (65.7, sent 13:38) has no matching `proposed_signal`, so it won't contribute to PF/winrate/avgR.
- **evidence:** `detect_untracked_legacy_alerts --since 2026-06-05` → "1 untracked legacy crypto alert(s)"; `watchlist_alerts` FET/USDT 2026-06-05T13:38:48Z.
- **suggested manual fix:** investigate the PART-1 alert→signal registration path; ensure every Telegram-sent alert writes a `proposed_signal` with a trackable `signal_id`.
- **priority:** medium
- **first observed:** 2026-06-05 18:39 EEST (carry-forward)

### TODO-unh-legal-gate (carry-forward)
- **issue:** UNH still emitted as a (now penalized C) long without an enforced legal-risk gate for the DOJ Medicare/antitrust probe (legal cluster importance 0.73 ×3 again today).
- **evidence:** intraday C-long UNH 56.09 (penalty −12); catalyst cycle legal-risk section lists 3 UNH DOJ-probe rows.
- **suggested manual fix:** implement a hard legal-risk gate (indictment/DOJ/SEC) that blocks affected long signals; re-verify UNH's current DOJ status.
- **priority:** medium
- **first observed:** 2026-06-05 04:30 EEST (carry-forward)

### TODO-catalyst-stock-usdt-mismap (carry-forward)
- **issue:** symbol resolver maps equity news to fake crypto `/USDT` pairs (UNH/USDT, JPM/USDT, TSLA/USDT, SMCI/USDT) and leaves macro/equity headlines unmapped — 72.7% unmapped again this run.
- **evidence:** catalyst coverage 766 mapped / 2037 unmapped today; catalyst cycle shows UNH/USDT, JPM/USDT, TSLA/USDT rows.
- **suggested manual fix:** add an asset-class-aware resolver that routes equity tickers to the stocks namespace instead of fabricating `/USDT` pairs.
- **priority:** medium
- **first observed:** 2026-06-03 (carry-forward)
