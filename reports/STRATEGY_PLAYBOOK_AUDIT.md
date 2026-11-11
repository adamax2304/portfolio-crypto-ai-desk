# Strategy Playbook Audit

**Date:** 2026-06-09 · **Scope:** Documentation only. No code, scoring, threshold, TP/SL, or auto-trade changes. Describes what the system **actually** generates today, derived from `src/agents/*`, `src/stocks/agents/*`, `src/signals/config.py`, the latest reports, and 14d signal_outcomes evidence.
**Companion:** [CURRENT_TRADING_PLAYBOOKS.md](CURRENT_TRADING_PLAYBOOKS.md) — one-page summary.

## How to read this document

For each playbook the system trades in paper today, I describe (1) what it is, (2) when it should work, (3) entry/stop/TP mechanics as they exist in code, (4) what current 14d evidence shows, (5) its production status, and (6) what we still need.

Performance numbers in §11 of each section are **14d, deduped, A/B only**, from `proposed_signals × latest signal_outcomes` (anchor 2026-06-09 11:00 UTC, cutoff 2026-05-26).

---

## 1. Crypto Scalp

| Field | Value |
|---|---|
| **1. Name** | Momentum continuation scalp |
| **2. Regime** | Range-with-volatility OR shallow trend; works less in danger/chop |
| **3. Setup** | A momentum or breakout candidate that already cleared the multi-exchange momentum / liquidity filters and has a clean **15m / 5m structure**. The technical setup agent computes an ATR-based entry zone right under (long) or above (short) the latest swing, intended to catch a small pullback before continuation. |
| **4. Entry** | Limit order at `[entry_low, entry_high]` zone. Filled on a candle whose OHLC envelope overlaps the zone; the candle open is preferred when it falls inside the zone (paper model). |
| **5. Stop** | Stop-market at `invalidation` (ATR-derived, typically 1× ATR(5m–15m) on the wrong side of the swing). Wick touch fires the stop. |
| **6. TP** | TP1 ≈ +1R, TP2 ≈ +2R, TP3 ≈ +3R off the entry midpoint. First wick touch counts as fill. No partials. |
| **7. Required confirmations** | Liquidity filter pass, momentum >= threshold, RS bias matches direction, derivatives not contradicting (OI/funding), regime not `high-volatility danger`. |
| **8. Pre-entry invalidator** | Price hits `invalidation` before touching the zone → `missed_no_entry`. Validity window 2 h (per `signal_tracking.yaml`). |
| **9. Works on** | Liquid binance-listed alts with normal vol; BTC/ETH scalps via the same path. |
| **10. Avoid** | Thin MEXC-only listings, extreme funding (squeeze risk against the direction), regimes labeled `high-volatility danger` or `range/chop` with no momentum. |
| **11. Performance (14d A/B)** | n=59, closed=8, **WR 12%, PF 0.14, netR −6R**. 27/27 expired triggered scalps had **positive MFE** (avg +0.54R). The entry edge is real; the 2h validity window and TP1 distance (~1.86R) are mismatched. |
| **12. Failure modes** | (a) TP1/2h horizon mismatch — most edge captured to +0.5R then mean-reverts before TP1; (b) catalyst-backed scalp NOT better in 14d (0W/2L) — news isn't the discriminator here. |
| **13. Status** | **ACTIVE, LOW-CONFIDENCE.** Banner in scalp reports + Telegram alert annotation. Re-audit at 20 closed A/B. |
| **14. Data still needed** | Tick / 1m OHLCV to resolve same-candle entry+stop / entry+TP ambiguity (paper-execution audit identified 3/40 sample). |

---

## 2. Crypto Intraday

| Field | Value |
|---|---|
| **1. Name** | Catalyst-or-momentum intraday continuation |
| **2. Regime** | Best in bullish trend or risk-on transition; underperforms in chop without catalyst |
| **3. Setup** | Same momentum/RS funnel as scalp but on the 15m–1h frame. The technical setup agent looks for a structural pullback or a clean breakout with a multi-hour follow-through path. Catalyst layer is the highest-PF kicker. |
| **4. Entry** | Limit at `[entry_low, entry_high]` zone (most common) OR stop at `entry_trigger` for breakouts. Filled on wick touch / open-inside-zone. |
| **5. Stop** | Stop-market at ATR-derived invalidation, typically 1× ATR(1h) below swing low (long) or above swing high (short). |
| **6. TP** | TP1 ≈ +1R, TP2 ≈ +2R, TP3 ≈ +3R. |
| **7. Required confirmations** | Liquidity + RS + regime alignment + (catalyst OR strong narrative basket OR derivatives confirmation). |
| **8. Pre-entry invalidator** | Invalidation touched before entry → `missed_no_entry`. Validity window 24h. |
| **9. Works on** | Catalyst-backed names (news=1 cut: WR 50%, PF 2.75) and clear RS leaders. ZEC, WLD, NEAR are recent recurring tickers. |
| **10. Avoid** | No-catalyst intraday in chop (no_news cut: WR 23%, PF 0.70). Late-cycle longs after a 25%+ vertical (chase risk). |
| **11. Performance (14d A/B)** | n=28, closed=21, **WR 33%, PF 1.29, netR +4R**. With news=1 cut: n=10, closed=8, **WR 50%, PF 2.75, netR +7R**. With news=0 cut: n=18, closed=13, **WR 23%, PF 0.70, netR −3R**. **Catalyst is the discriminator.** |
| **12. Failure modes** | No-catalyst intraday in range regime is net-negative. Long-only bias amplifies chop losses. |
| **13. Status** | **ACTIONABLE.** Catalyst-backed especially. |
| **14. Data still needed** | Tighter catalyst→symbol mapping (still partial). Better regime tag persistence on the signal row (currently empty for most rows). |

---

## 3. Crypto Swing

| Field | Value |
|---|---|
| **1. Name** | Multi-day momentum + narrative-aligned swing |
| **2. Regime** | Strongest in trending markets and during narrative rotations; survives chop better than other modes |
| **3. Setup** | Structural pullback within a clearly trending higher-timeframe move (4h/1d). The narrative basket layer (perps_dex, ai_narrative, binance_ecosystem, momentum_breakout) is a meaningful kicker. |
| **4. Entry** | Limit zone (usual) or trigger breakout. Filled on wick / open-inside-zone. |
| **5. Stop** | ATR(4h)-based invalidation, structurally below/above the prior swing pivot. |
| **6. TP** | TP1 +1R, TP2 +2R, TP3 +3R (same R model as other modes). |
| **7. Required confirmations** | RS leadership OR narrative-basket membership OR catalyst. |
| **8. Pre-entry invalidator** | Invalidation hit pre-entry → `missed_no_entry`. Validity 168h (7d). |
| **9. Works on** | RS leaders (ALLO sc91.6 RS+27.6%, ZEC, BANK, WLD). Narrative-basket members. |
| **10. Avoid** | Tickers that already ran > 30% in 24h without pullback (chase risk). Names with no RS support. |
| **11. Performance (14d A/B)** | n=18, closed=18, **WR 72%, PF 5.80, netR +24R**. With news=1: n=2, closed=2, **WR 100%, PF ∞, netR +6R** (tiny sample). Without catalyst still strong: 11/2 (sample of non-news rows in 14d). **Best mode in the system.** |
| **12. Failure modes** | Sudden BTC dump invalidates correlated swing longs; squeezes can stop fairly large swing shorts. Sample of swing shorts is small. |
| **13. Status** | **ACTIONABLE — primary playbook.** |
| **14. Data still needed** | Persistent narrative-basket → signal tag on `proposed_signals` for cleaner attribution. |

---

## 4. Crypto Shorts (cross-mode strategy lens)

| Field | Value |
|---|---|
| **1. Name** | Failed-bounce / weak-RS short |
| **2. Regime** | Best in bearish trend or risk-off / topping pattern; dangerous when funding is extremely negative (squeeze risk) |
| **3. Setup** | A weak-RS or failed-reclaim setup; technical agent identifies the rejection at resistance with ATR-based invalidation above. Often emerges around macro-risk-off windows (ETF outflows, tariff/geopolitical headlines). |
| **4. Entry** | Limit at the rejection zone (`entry_low/entry_high` ABOVE current price for a short pullback) or stop at trigger BELOW current price for a breakdown. |
| **5. Stop** | ATR-based invalidation above the rejection / sweep level. |
| **6. TP** | TP1 +1R, TP2 +2R, TP3 +3R toward the prior demand area or measured-move target. |
| **7. Required confirmations** | RS lower than BTC, sector/narrative not in active rotation, derivatives not flashing extreme negative funding (squeeze risk). |
| **8. Pre-entry invalidator** | Invalidation hit before entry. |
| **9. Works on** | Names without active catalyst tailwind. Recent winners: NEAR shorts, FET shorts, AVAX swing-short (+3R), ETH short, BTC short during risk-off pulse. |
| **10. Avoid** | Extreme negative funding crowded shorts (BTC perp funding -453% recently — squeeze pile). Active narrative-basket members. |
| **11. Performance (14d A/B)** | n=45, closed=15, **WR 40%, PF 2.00, netR +9R**. Better PF than longs (1.76) on much smaller sample. |
| **12. Failure modes** | Short squeezes from oversold negative funding. Catalyst news pop against the position (ICP loss came right after a news event). |
| **13. Status** | **ACTIONABLE.** Treat as risk-aware: avoid extreme-funding setups. |
| **14. Data still needed** | Persistent funding/OI/squeeze flags on the signal row to enable a "skip extreme funding" filter in future. |

---

## 5. Catalyst-Backed Setups (cross-mode strategy lens)

| Field | Value |
|---|---|
| **1. Name** | Catalyst confirmation overlay |
| **2. Regime** | Mode-agnostic; the catalyst classifier (CryptoBriefing, AMBCrypto, TheBlock, BeInCrypto, Lookonchain TG, etc.) attaches `news_supported=1` to signals whose symbol overlaps the catalyst entity-alias map. |
| **3. Setup** | A normal technical setup with an aligned, time-fresh catalyst (e.g., regulatory news, listing, governance change, exchange teaser, on-chain whale activity). The catalyst is **not** the entry trigger by itself; it confirms the direction. |
| **4. Entry / Stop / TP** | Same mechanics as the host mode (scalp / intraday / swing) — catalyst does not change the geometry. |
| **7. Required confirmations** | A catalyst classified at non-zero importance + matched to the symbol via entity aliases. |
| **8. Invalidates pre-entry** | Catalyst contradiction (a follow-up headline that flips the thesis) — not currently auto-detected; the user judges manually. |
| **9. Works on** | Crypto INTRADAY and SWING — where the catalyst lifts PF noticeably. |
| **10. Does NOT improve** | **Crypto scalp** — catalyst-backed scalp 0W/2L vs no-catalyst 1W/5L in 14d. Catalyst-on-scalp adds noise, not edge. |
| **11. Performance (14d A/B, catalyst=1)** | All crypto news-supported A/B: n=26, closed=12, **WR 50%, PF 2.83, netR +11R** (half the net came from 1/3 of the signals — clear edge). |
| **12. Failure modes** | Catalyst classifier mismatches (NVDA tagged as "NVDA/USDT" — see today's dashboard). Sell-the-news on already-priced catalysts. |
| **13. Status** | **ACTIONABLE OVERLAY on intraday+swing.** Not a standalone playbook (catalyst alone never enters a trade). |
| **14. Data still needed** | Persistent `catalyst_id` on `proposed_signals` so revalidator R6 (catalyst staleness) can fire. Better symbol mapping for stocks-related catalysts. |

---

## 6. RS-Leader Longs (cross-mode strategy lens)

| Field | Value |
|---|---|
| **1. Name** | Relative-strength leader pullback |
| **2. Regime** | Bullish or transition with positive breadth; the leader's RS vs BTC must be clearly positive |
| **3. Setup** | A symbol whose 24h, 7d, or RS-vs-BTC reading puts it in the strongest decile of the universe, pulling back to a structural support without breaking trend. ALLO, ZEC, WLD recently. |
| **4. Entry** | Pullback limit zone OR breakout-of-flag trigger. |
| **5. Stop** | ATR-based below the pullback structure. |
| **6. TP** | Mode-specific (scalp / intraday / swing) R-multiples. |
| **7. Required confirmations** | RS vs BTC > +20% recent, momentum score top-decile, volume not zeroing out on the pullback. |
| **8. Pre-entry invalidator** | Loss of the trend HL on the host timeframe. |
| **9. Works on** | The top 5 strongest symbols per cycle (the dashboard's "Strongest Symbols" list). Recent winners: ALLO +3R swing, ZEC +5R (multiple modes), WLD +3R intraday. |
| **10. Avoid** | Late-stage extensions (24h > +30% without consolidation). Thin-volume RS leaders (RS computed on tiny tape). |
| **11. Performance (14d, embedded in crypto swing+intraday)** | The strongest-symbols cohort drives the crypto swing 72% WR and the catalyst-backed intraday 50% WR. Not separately tagged in DB. |
| **12. Failure modes** | RS leader that became leader via short squeeze (the squeeze unwinds). Chasing a vertical 30%+ candle. |
| **13. Status** | **ACTIONABLE OVERLAY**, particularly when combined with catalyst (catalyst + RS-leader is the sharpest crypto edge). |
| **14. Data still needed** | An explicit `rs_decile` field on the signal row would let us audit this playbook directly instead of inferring it. |

---

## 7. Stocks Intraday

| Field | Value |
|---|---|
| **1. Name** | RTH momentum / RS continuation |
| **2. Regime** | Best when SPY/QQQ have direction; weakest in chop. Pre-market hyped names handled via headline/legal-risk gate. |
| **3. Setup** | An A-or-B technical setup on the 15m/1h yfinance bar, scored against sector regime + RS vs SPY + earnings calendar + headline-risk filter. ATR-based zone with structural invalidation. |
| **4. Entry** | Limit zone. Tracker walks 15m bars (RTH only — yfinance excludes pre/post). |
| **5. Stop** | ATR-derived invalidation. |
| **6. TP** | TP1 +1R, TP2 +2R, TP3 +3R. |
| **7. Required confirmations** | Earnings calendar `severity != UNKNOWN-and-no-news` (ETF false-positive fix). No legal-risk flag. RTH session open at signal time (otherwise demoted to C). |
| **8. Pre-entry invalidator** | Invalidation hit on the candle; market_closed gate also pulls A/B → C if signal lives outside RTH. |
| **9. Works on** | Large-cap tech (XOM, LLY, AAPL, JPM longs; META, AMZN, SPY, QQQ, XLK shorts during selloffs). |
| **10. Avoid** | NVDA long (0W/4L 14d), SMCI long (0W/3L), SMH long (0W/2L) — flagged in the dashboard. |
| **11. Performance (14d A/B)** | n=479, closed=173, **WR 55%, PF 2.03, netR +80R**. Shorts cohort: n=25, closed=7, **WR 86%, PF 9.00, netR +8R** (small but clean). Longs: n=454, closed=166, WR 54%, PF 1.94, netR +72R. |
| **12. Failure modes** | Persistent A-tier overpromotion on losing names (NVDA/SMCI longs); A-tier overall is 18% WR for stocks. |
| **13. Status** | **ACTIONABLE — primary stocks playbook.** |
| **14. Data still needed** | Pre-market gap detection to feed the R3 regime-changed revalidation rule. |

---

## 8. Stocks Swing — watchlist-only

| Field | Value |
|---|---|
| **1. Name** | Multi-day RS / sector-rotation swing (currently paused) |
| **2. Regime** | Designed for trending markets with clear sector leadership; failed in the tested range/chop tape |
| **3. Setup** | A 1d/4h pullback to structural support on an RS leader. Identical pipeline to swing for crypto, just with stocks data. |
| **4. Entry** | Limit zone. |
| **5. Stop** | ATR-derived invalidation. |
| **6. TP** | TP1/2/3 = +1R/+2R/+3R. |
| **7. Required confirmations** | Same as intraday + structural alignment on the higher timeframe. |
| **8. Pre-entry invalidator** | Same as the other modes. |
| **9. Works on** (when re-enabled) | RS-leader large caps with sector tailwind. |
| **10. Avoid** | The pre-pause pipeline systematically overpromoted late-cycle tech longs (AAPL, AMD, LLY, NVDA, SMCI) into A-tier swing during a topping pattern. |
| **11. Performance (14d A/B, all pre-pause)** | n=54, closed=44, **WR 11%, PF 0.15, netR −33R**. |
| **12. Failure modes** | A-tier-long bias in chop / top. Stops fire within 1–6 days while the thesis horizon is 7 days. |
| **13. Status** | **PAUSED — watchlist/research only.** Gate cap `stocks_swing_paused_after_48h_audit` demotes any A/B to C. |
| **14. Data still needed** | 20+ closures of the post-pause C-tier counterfactual (currently <20). Once that's hit, re-audit. |

---

## 9. Stocks Invest — watchlist-only

| Field | Value |
|---|---|
| **1. Name** | 30-day thesis trade (currently paused) |
| **2. Regime** | Designed for clear macro thesis (e.g., AI build-out, healthcare tailwind); same A-tier-long bias as swing |
| **3. Setup** | A higher-timeframe (1d/1wk) trend continuation with 30-day validity. |
| **4. Entry** | Limit zone. |
| **5. Stop** | ATR-based, **tight relative to horizon** — stops fire in 1–6 days while the thesis would need weeks. Identified as the binding constraint. |
| **6. TP** | +1R/+2R/+3R but TPs are 30-day-distance multi-percent moves. |
| **7. Required confirmations** | Same as swing. |
| **8. Pre-entry invalidator** | Same. Validity 720h (30d). |
| **9. Works on** (when re-enabled) | Genuine multi-week structural setups with macro thesis. |
| **10. Avoid** | Anything the swing pipeline catches — same pipeline, same failure. |
| **11. Performance (14d A/B)** | n=39, closed=24, **WR 0%, PF 0.00, netR −24R**. 13/13 closed losses were all longs (tech/large-cap basket). |
| **12. Failure modes** | Stop-to-horizon mismatch — invalidates fast, never reaches 30d-thesis targets. Pipeline overlap with the paused swing. |
| **13. Status** | **PAUSED — watchlist/research only.** Gate cap `stocks_invest_paused_after_mode_viability_audit`. |
| **14. Data still needed** | Either (a) a separate longer-stop invest pipeline (out of scope), or (b) news-supported flag for invest signals to enable a catalyst-only re-enable lane. |

---

## Cross-playbook observations

- **Best edges today (by PF):** crypto swing (5.80), crypto intraday + catalyst (2.75), stocks intraday shorts (9.00 small sample). All three carry a clear structural/regime confirmation.
- **Worst edges today:** crypto scalp (0.14), stocks swing (0.15), stocks invest (0.00). Two of three are paused; the third (scalp) is annotated low-confidence pending strategy work.
- **Catalyst overlay** is only a strong kicker on **intraday + swing crypto**. It is neutral-to-negative on scalp. It is largely absent from stocks signals (the pipeline does not populate `news_supported=1` for stocks invest/swing).
- **Shorts** outperform longs in PF on both crypto (2.00 vs 1.76) and stocks (9.00 vs 1.94) but on much smaller absolute volume — the system structurally generates more longs than shorts.

## What this audit explicitly did NOT do
- No edits to scoring weights, no edits to TP/SL geometry, no edits to thresholds.
- No new gates, no new pauses, no scheduler restart.
- No re-tagging of historical rows.
- No auto-trade enablement.

## Verdict
```
STRATEGY_PLAYBOOK_AUDIT_COMPLETE
```
