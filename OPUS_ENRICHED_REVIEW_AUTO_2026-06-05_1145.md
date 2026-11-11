# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:30 EEST

- **Generated:** 2026-06-05 11:45 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`, **Europe / pre-US context** slot 11:30).
- **Slot focus:** EU morning, setting up the US day. US cash session opens **16:30 EEST (09:30 ET) — ~4.75 h away**. Crypto is the **live actionable class**; stock signals are **pre-open planning/watchlist** and become actionable only on fresh post-open levels.
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-05_0439.md` (≈7.1 h ago, Asia/overnight slot — §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). Verified UNH DOJ Medicare-fraud investigation (Yahoo/Phemex/SEC), Broadcom AVGO AI-guidance miss + semis contagion (CNBC/Bloomberg/Yahoo, 5+ sources), SMCI export-control board review (StockTitan/SEC). One WebFetch (UNH Yahoo) opened cleanly; one (CNBC Broadcom) returned **HTTP 403** → fell back to 4+ corroborating search sources.
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; all price/structure is local OHLCV/ATR/EMA report fields + cited external prints.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

- **Both asset classes are risk-off / downside-skewed, driven by one macro event: Broadcom's AI-guidance miss unwinding the AI trade.** External research **confirms** AVGO guided Q3 AI revenue ~$16B vs ~$17.3B expected and declined to raise the FY AI forecast ($56B vs $57.6B est.), shares **−14%, ~$300B market cap wiped**, dragging AMD/NVDA/Micron. Crypto fell in sympathy: **BTC plunged to ~$62,000 as the AI trade unwinds, HYPE −14%** (CoinDesk, internal). Crypto regime **bearish trend (risk-off)**, BTC/ETH downtrend, breadth 22.9% > EMA20, **BTC ATR percentile 93 (elevated)**. Stocks regime **risk_off, bias short, VIX 16.06**.
- **Integrity carry-over (still unfixed): the desk is STILL emitting UNH as an A-tier (81.3) intraday LONG while UNH is under an active DOJ Medicare-fraud investigation (criminal + civil).** Same defect flagged at 04:30 (`TODO-unh-legal-gate`) — **7 hours later the legal-risk gate has not caught it.** Per §I this is a hard gate: **UNH → AVOID / MANUAL REVIEW REQUIRED regardless of the A-tier score.** Reinforcing internal evidence: the **current fresh** stocks intraday scoring demotes UNH long to **31.64 (rejected, "long_in_risk_off_regime")** — the A-tier 81.3 is a **stale carry-forward** from a prior US session, not a current read. There is also a **price discrepancy** worth manual check (signal entry ~394 vs analyst target $354 and 2025 prints near $280) → `TODO-unh-price-staleness`.
- **No clean active crypto actionable.** The live crypto B-shorts (FET 67–69, NEAR 66–70.5) are **catalyst-aligned but LATE**: the desk's own current analysis scores them 37.7 / 40.1 with **"Price is more than 2 ATR from EMA20; do not chase … late_short_after_exhaustion"** — both already **−12% on 24h**. NEAR's catalyst (Arthur Hayes dumping HYPE+NEAR before a SpaceX IPO, AMBCrypto) is real but **already priced in**. Crypto B-tier triggered winrate is **25% (weak)**; the short bucket demands a fresh failed-bounce, not a chase.
- **Stocks (pre-open planning):** The cleanest *names* (AMD B-invest 78.3, NVDA 76, SMCI 79.7) are **all long AI/semis into a confirmed sector derating + risk_off regime** — fighting both the tape and the catalyst. **AMD** = wait for the **496–516** invest zone (still `waiting_for_entry` below price), half-size, post-open confirmation only. **SMCI** carries an unresolved **board-led export-control review** → caution/AVOID (the fresh intraday report itself rejected it, no_trade 41.96). **A-tier stocks remain the worst bucket (PF 0.20, −8R, 6% winrate).**
- **Net verdict:** **Crypto = no-trade / watchlist, downside-skewed** — respect BTC $60–62K. **Stocks pre-open: UNH AVOID (DOJ); AMD wait-for-pullback half-size; SMCI avoid/caution; NVDA watch (regulatory overhang).** Catalyst layer is **context-only** this run (74% unmapped).

---

## 2. Data Used

**Internal — fresh (<4 h):**
- `data/reports/scalp/2026-06-05_08-39_scalp_report.md` (mtime 11:39 EEST; data freshness 08:30 UTC). Regime **bearish trend (risk-off)**; BTC/ETH downtrend; breadth 22.9% > EMA20; BTC ATR pct 93.
- `data/reports/intraday/2026-06-05_05-56_intraday_report.md` (mtime 08:56 EEST; ~2.8 h). Bearish; FET/NEAR fresh-catalyst shorts; macro = treasury-company drawdowns + AI-trade unwind.
- `data/reports/stocks/intraday/2026-06-05_06-10_stocks_intraday_report.md` (mtime 09:10 EEST; ~2.5 h) — **MARKET CLOSED / after-hours**; regime risk_off; A/B demoted to C; UNH/NVDA/AMD/SMCI all rejected at current levels.

**Internal — STALE (>14 h, planning-only, excluded from final swing/invest verdicts):**
- `data/reports/swing/2026-06-04_14-44_swing_report.md` (crypto; mtime 06-04 17:44 → **~18 h**).
- `data/reports/stocks/swing/2026-06-04_14-55_stocks_swing_report.md` (mtime 06-04 17:55 → **~18 h**).
- `data/reports/stocks/invest/2026-06-04_15-01_stocks_invest_report.md` (mtime 06-04 18:01 → **~18 h**).

**Catalyst / narrative / packets:**
- `data/catalysts/2026-06-05/` — `catalyst_events.jsonl` (**1124 rows**), `narrative_baskets.jsonl` (2 baskets), `catalyst_cycle_05-57.md` (mtime 08:57).
- LLM packets: `data/processed/llm_analysis_packet.md` (mtime 11:39), `llm_stocks_packet.md` (mtime 09:10).

**CLI / DB:** `active-signals` (crypto **13** / stocks large carry-forward set), `signal-stats` (crypto + stocks, week), `detect_untracked_legacy_alerts --since 2026-06-05` → **0 untracked** (clean). DB: `db/crypto_ai_desk.sqlite` (~723 MB, mtime 11:40). `news_items` queried read-only (t.me 4h, candidate 24h).

**External (this run — cited §13):** UNH DOJ Medicare-fraud investigation (Yahoo Finance 2025-07-31, Phemex Academy, SEC EDGAR 10-Q FY2026); Broadcom AVGO AI-guidance miss + semis contagion (CNBC, Bloomberg, Yahoo Finance, Motley Fool, Investing.com); SMCI export-control board review + Q3 FY26 results (StockTitan/SEC).

**Unavailable / blind:** live tick prints; TradingView/Chrome chart verification (not loaded); liquidation heatmaps, order-book/CVD, live ETF-flow feed; live social beyond RSS-bridged `t.me/*` (this run = lookonchain "welcome" noise + one ZEC-short line + zachxbt Kraken downgrade).

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-04_default_schedule/`.
- `scheduler.log` mtime **11:39 EEST → ~0 h** (fresh, actively writing). Latest cycle summary `cycle_06_08-01_summary.md` mtime **09:11 EEST → ~2.6 h** (fresh, under 3 h).
- **NO DEFER** — both freshness checks under the 3 h rule.
- **Fresh (<4 h):** crypto scalp (~0 h), crypto intraday (~2.8 h), stocks intraday (~2.5 h).
- **STALE (>14 h, excluded from final swing/invest verdicts):** crypto swing (~18 h), stocks swing (~18 h), stocks invest (~18 h). The overnight scheduler does not appear to have regenerated swing/invest reports since the 06-04 14:44–15:01 batch → `TODO-swing-invest-staleness` (§14). Stocks are closed regardless, so swing/invest are planning-only this slot.

---

## 4. What Changed vs Previous Review (04:30 → 11:30)

- **Slot advanced from Asia/overnight to Europe/pre-US.** US opens in ~4.75 h. No new US session has printed since 04:30, so the stock picture is the same carry-forward set re-evaluated against fresh pre-open scoring.
- **`TODO-unh-legal-gate` STILL OPEN.** 04:30 flagged UNH A-tier-while-under-DOJ as a high-priority gate defect. **7 h later UNH is still emitted as A-tier 81.3 intraday long** — the legal-risk layer has not been patched (expected — this routine is advisory-only; a manual session must fix it). **CONFIRMED still AVOID.**
- **Broadcom/AVGO catalyst now fully confirmed and quantified.** 04:30 framed AMD's drop as "AVGO soft AI guide, sympathy." This run external research pins it precisely: AVGO −14%, ~$300B wiped, Q3 AI guide $16B vs $17.3B est., FY $56B vs $57.6B — "exposes the fragility of the AI trade." The semis derating is **macro-confirmed, not a one-name event.**
- **BTC held the cascade zone — roughly flat vs 04:30.** 04:30: BTC ~$61.4K intraday, testing the $61–62K cascade level. This run: internal macro headline "**Bitcoin plunges to near $62,000 as the AI trade unwinds**" — still pinned to the $62K zone, no breakdown yet, no reclaim. Treasury-company stress deepened (Strategy down $11.07B on BTC, Bitmine down $9.58B on ETH — t.me/lookonchain).
- **New crypto names rotated into the B-short list: FET + NEAR** (replacing 04:30's SUI). Both are **late/extended** (−12% 24h, >2 ATR from EMA20) — same "don't chase a flush" discipline. NEAR carries the Arthur Hayes-dump catalyst (confirmed, but priced in).
- **Catalyst mapping degraded slightly:** 72.4% unmapped → **74% unmapped** (832/1124). Still context-only.
- **Untracked legacy alerts: still 0** (clean, no regression).
- **AMD shifted from A-tier swing (04:30) to B-tier invest (78.3) this run** — same long bias, same 496–516 zone discipline, still `waiting_for_entry` below price.

---

## 5. Catalyst Coverage

- Total `catalyst_events` today: **1124**.
- Mapped (non-null symbol): **292** · Unmapped (null symbol): **832** · **Unmapped = 74.0%**.
- `narrative_baskets`: **2** — `perps_dex_narrative` (HYPE/USDT primary; Arthur Hayes dumping HYPE+NEAR before SpaceX IPO; single_source; <6h) and `momentum_breakout` (HOME/USDT +40.8%, no confirmed news; <1h).
- **⚠ CATALYST MAPPING WEAK THIS RUN (74% unmapped > 50%) — use the catalyst layer as CONTEXT, NOT a final decision input.**
- **Top-3 unmapped headlines:** (1) "South Korea is the ultimate backdoor tech play — but stock investors now face a looming threat" (MarketWatch); (2) "White House crypto adviser Witt defends Clarity Act, calls it 'pro-law enforcement'" (The Block); (3) "Crypto Clarity Act in spotlight for bad-actor provisions as Senate process grinds forward" (CoinDesk).
- **Resolver quirk (integrity):** stock tickers are being mapped to fake crypto pairs in the catalyst layer — `AVGO/USDT` (37), `NVDA/USDT` (20), `UNH/USDT` (9), `TSLA/USDT` (7), `JPM/USDT` (6), `COIN/USDT` (6), `MSFT/USDT` (5), `SMCI/USDT` (3). These are equities news suffixed `/USDT` → `TODO-catalyst-stock-usdt-mismap` (§14).

---

## 6. Market Landscape

- **Macro driver:** Broadcom's AI-revenue guidance miss (06-03) → broad AI/semis derating. AVGO −14%, Micron −7%, AMD/Intel/NVDA dragged. "Exposes the fragility of the AI trade" (Investing.com). This is the single thread connecting weak stocks AND weak crypto this slot.
- **Crypto:** regime **bearish trend (risk-off)**; BTC downtrend, ETH downtrend; altcoin breadth **22.9% > EMA20 / 18.75% > EMA50**; BTC ATR percentile **93 (elevated vol)**. BTC ~**$62,000**. Broad altcoin flush: ZEC −36.98%, ADA −16.07%, NIGHT −14.56%, INJ −13.19%, ENA −13.01%, FET/NEAR ~−12%. Crypto-treasury companies deeply underwater (Strategy −$11.07B BTC). Recommended style (desk): **short bias or no trade; avoid weak altcoin longs.**
- **Stocks:** regime **risk_off, bias short**; **VIX 16.06**; breadth above EMA20 = 0.0% (note: index 5d/20d returns are **NaN** across SPY/QQQ/IWM/DIA — a data-quality defect, see §10 / `TODO-stocks-index-nan`). News skew: AI/semis weakness (AVGO/Micron), NVDA regulatory overhang (Warren Senate hearing invite, Trump-officials China-Blackwell-loophole report), but also NVDA positive (cleared Samsung/SK Hynix/Micron for Vera Rubin HBM4 supply).

---

## 7. Candidate Deep Dives (≤5)

### 7.1 UNH — stocks, A-tier 81.3, intraday LONG (triggered) — **AVOID / MANUAL REVIEW REQUIRED**
- **Signal:** entry 394.43–396.82, invalidation 389.64, expires 2026-06-05T16:35:08 (carry-forward from prior US session).
- **LEGAL / HEADLINE RISK (verified §G/§I):** UnitedHealth is under an **active DOJ Medicare-fraud investigation — both criminal and civil** — examining whether it inflated Medicare Advantage diagnoses to trigger higher payments; the company is cooperating with formal DOJ requests and launched a third-party review (Yahoo Finance 2025-07-31; Phemex Academy 2026; SEC 10-Q FY2026). Stock has fallen sharply (analyst target $354.42 cited vs prints near $280 in later coverage; first guided revenue decline in a decade).
- **Internal contradiction:** the fresh stocks-intraday run scores UNH long at **31.64 (rejected, "long_in_risk_off_regime, rr_below_1.5")** — the A-tier 81.3 is a **stale carry-forward**, not a current read.
- **Price-reaction / chase (§J):** signal entry ~394 sits well **above** the analyst target ($354) and the reported post-crash range — a likely **stale price feed** (`TODO-unh-price-staleness`). Cannot verify live (no chart MCP).
- **Verdict:** **AVOID** — a clean long on a stock under active federal fraud investigation, fighting a risk_off regime, on stale levels. Never actionable this run.

### 7.2 AMD — stocks, B-tier 78.3, invest LONG (waiting_for_entry) — **WAIT (pullback, half-size, post-open only)**
- **Signal:** entry 496.69–520.82, invalidation 448.43, expires 2026-07-04 (invest horizon). Also appears B swing earlier; demoted/rejected (32.89, no_trade) in the fresh intraday run.
- **Catalyst (verified §G):** AMD is in the **Broadcom-led semis selloff** — "Why AMD Stock Is Sinking Today" (Motley Fool 06-04); AVGO −14% guide miss dragged the whole semi complex (CNBC/Bloomberg/Yahoo). No AMD-specific bad news, but the **sector derating is the headwind.**
- **Price-reaction / chase (§J):** long into a **confirmed sector derating + risk_off + bearish breadth**. `waiting_for_entry` = price is below the trigger zone; entering NOW would be catching a falling semis knife. Actionable only on a **reclaim of the 496–516 zone with post-open confirmation**, half-size.
- **Verdict:** **WAIT** — best of the stock longs but fighting the tape; no chase.

### 7.3 SMCI — stocks, C-tier 79.7 intraday (triggered) + invest 76.4 + swing 76.3 — **CAUTION / AVOID (legal flag)**
- **Catalyst (verified §G/§I):** SMCI has an **ongoing board-led review of certain export-control-related transactions**; BDO ratified as auditor; Q3 FY26 results strong ($10.2B sales, $483M net income) (StockTitan/SEC). Carries a **history of accounting/auditor issues** — exactly the §I legal-flag profile.
- **Internal:** the **fresh intraday report rejected SMCI** (no_trade, 41.96, no_directional_setup) — the C-tier 79.7 active signal is a carry-forward, not a current read.
- **Verdict:** **CAUTION / AVOID** — unresolved export-control review + semis selloff + no fresh directional setup. Not a clean actionable.

### 7.4 FET/USDT — crypto, B-tier 67–69, intraday/scalp SHORT (waiting/expired) — **NO-TRADE (late/extended)**
- **Signal:** FET intraday short 67.0 (waiting, expires 06-06 05:56), scalp 69.3 (expired 07:48). Entry 0.2149–0.2175, invalidation 0.2208.
- **Price-reaction / chase (§J):** current fresh desk scoring = **37.7 (short), "Price is more than 2 ATR from EMA20; do not chase … volume below average; breakout confirmation weak."** FET already **−12.81% on 24h** with OI down (deleveraging / long-liquidation). The short has **already played out.**
- **Verdict:** **NO-TRADE** — late short after a vertical flush; would need a bounce back into the entry zone to reset.

### 7.5 NEAR/USDT — crypto, B-tier 66–70.5, intraday/swing SHORT — **NO-TRADE (catalyst priced in, late)**
- **Signal:** NEAR intraday short 66.0 (waiting, expires 18:00 today), swing 70.5 (tp2_hit). Entry 2.44–2.49, invalidation 2.54.
- **Catalyst (verified internal):** **Arthur Hayes dumping HYPE+NEAR before a SpaceX IPO** (AMBCrypto, single_source) — confirmed bearish, and it is the `perps_dex_narrative` basket's driver.
- **Price-reaction / chase (§J):** current fresh desk scoring = **40.1 (short), "Price is more than 2 ATR from EMA20; do not chase … late_short_after_exhaustion."** NEAR already **−12.21% 24h** (RS vs BTC −10.66%). **Catalyst is real but already priced in.**
- **Verdict:** **NO-TRADE** — catalyst-aligned but late; swing leg already hit tp2. Don't chase.

---

## 8. Best Candidates Ranked

**No clean actionable candidates this slot.** Ranked by least-bad / conditional quality:

1. **AMD (stocks, invest long)** — *conditional WAIT.* Cleanest name but fighting a confirmed semis derating + risk_off; only on a 496–516 reclaim with post-open confirmation, half-size.
2. **NVDA (stocks, watch)** — mixed (regulatory overhang vs Vera Rubin HBM4 win); watch for a reclaim, no entry pre-open.
3. **FET / NEAR (crypto, short)** — valid bias, wrong price — wait for a failed bounce back into the entry zones; do not chase the flush.

Everything else = watchlist / no-trade.

---

## 9. Avoid / No Trade

- **UNH (A-tier long)** — **AVOID.** Active DOJ criminal+civil Medicare-fraud investigation; stale carry-forward A-tier; fresh score 31.64 rejected. (§7.1)
- **SMCI (C 79.7 long)** — **AVOID/CAUTION.** Unresolved board-led export-control review; fresh intraday rejected (no_trade). (§7.3)
- **FET / NEAR (B shorts)** — **NO-TRADE.** Late/extended >2 ATR; already −12%; "do not chase." (§7.4/7.5)
- **ZEC (swing long, tp2_hit)** — **INVALIDATED.** ZEC −36.98% on 24h with fresh shorts pressing (t.me/lookonchain: Garrett Jin shorting the rally); the long thesis is gone — treat as closed/no-trade.
- **All long AI/semis (NVDA 76, SMH, LLY, AAPL)** — fighting risk_off + AI-trade derating; no pre-open entries.

---

## 10. Main Risks

- **Stale-carry-forward A/B signals contradict fresh scoring.** UNH (A 81.3 → fresh 31.64 rejected) and SMCI (C 79.7 → fresh no_trade) are emitting actionable-looking tiers that the current regime rejects. Anyone reading `active-signals` without the fresh report context could be misled. (→ §14 TODOs)
- **Legal-risk gate not enforced (UNH).** A federal-fraud-investigation name is still surfacing as the top A-tier long. High-priority defect.
- **Stocks index trends are NaN** (SPY/QQQ/IWM/DIA 5d & 20d returns all `nan`; breadth 0.0%) — the risk_off label may be partly an artifact of a broken returns computation, not pure tape. Treat the stocks regime label with caution.
- **Catalyst layer 74% unmapped + stock→/USDT mismaps** — low signal; context only.
- **Swing/invest reports ~18 h stale** — no overnight regeneration; excluded from final swing/invest verdicts.
- **Chase risk in crypto** — the desk's own analysis explicitly tags FET/NEAR as "do not chase"; the active B-shorts could lure a late entry.
- **BTC $60–62K cascade zone** — a clean break of $60K opens $50K (per prior-review framing); elevated ATR (pct 93) = wide stops required.
- **Source-ingest note:** if `ingest_enriched_review_sources` fails for the cited stocks JSON it is logged here and the review still stands (ingest is idempotent, advisory-only).

---

## 11. Action Plan — next 4 hours (into the 16:30 EEST US open)

1. **Crypto:** stand aside / watchlist. Respect BTC **$60–62K**; only consider shorts on a **failed bounce** back into FET 0.2149–0.2175 / NEAR 2.44–2.49 — not at current extended prints. No longs in a bearish/elevated-vol tape.
2. **Stocks (pre-open):** **no pre-open entries.** Re-evaluate on fresh 09:30 ET levels. UNH = do-not-touch (DOJ). AMD = watch the 496–516 invest zone for a post-open reclaim, half-size. NVDA = watch for a reclaim given mixed catalysts. SMCI = avoid pending export-control clarity.
3. **At/after 16:30 EEST:** expect the stocks engine to regenerate fresh intraday levels; the carry-forward A/B set should be re-scored — re-read before acting on any stock signal.
4. **Monitor:** BTC $60K line; any AVGO/semis follow-through or stabilization; any fresh UNH DOJ headline.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** **NO-TRADE / watchlist.** Bearish/elevated-vol; FET/NEAR shorts late & extended ("do not chase"); B-tier triggered winrate 25%.
- **Crypto intraday:** **NO-TRADE.** No fresh A/B; only conditional FET/NEAR shorts on a failed bounce; otherwise stand aside.
- **Crypto swing:** **NO-TRADE.** Report ~18 h stale (excluded); NEAR swing already tp2_hit; ZEC swing-long invalidated by −37% flush.
- **Stocks intraday (closed — pre-open):** **UNH AVOID (DOJ); AMD watch 496–516 (half-size, post-open only); SMCI avoid/caution; NVDA watch → long only on a reclaim.** No pre-open entries.
- **Stocks swing (stale ~18 h — planning only):** **AMD long bias intact (wait for zone); UNH excluded (legal).** Not actionable on stale data.
- **Stocks invest (stale ~18 h — planning only):** **AMD entry 496–520 bias consistent; SMCI/UNH excluded.** Re-confirm on fresh data.

---

## 13. Sources

- [With UnitedHealth Under DOJ Investigation, Should You Buy, Sell, or Hold UNH Stock Now? — Yahoo Finance, 2025-07-31](https://finance.yahoo.com/news/unitedhealth-under-doj-investigation-buy-110002685.html)
- [UnitedHealth Group (UNH) Stock in 2026: DOJ Probe, Medicare Reset, Key Risks — Phemex Academy, date unavailable](https://phemex.com/academy/unitedhealth-group-unh-stock-2026)
- [UNITEDHEALTH GROUP INC — Form 10-Q FY2026 (Q1 2026) — SEC EDGAR, date unavailable](https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000127/unh-20260331.htm)
- [Broadcom (AVGO) earnings report Q2 2026 — CNBC, 2026-06-03 (WebFetch 403; corroborated below)](https://www.cnbc.com/2026/06/03/broadcom-avgo-earnings-report-q2-2026.html)
- [Broadcom Slides by Most in More Than a Year on AI Outlook Miss — Bloomberg, 2026-06-03](https://www.bloomberg.com/news/articles/2026-06-03/broadcom-outlook-disappoints-investors-seeking-ai-fueled-blowout)
- [Micron Drops 7% as Broadcom's Disappointing AI Outlook Triggers a Semiconductor Selloff — Yahoo Finance, 2026-06-04](https://finance.yahoo.com/markets/stocks/articles/micron-drops-7-broadcom-disappointing-151544845.html)
- [Broadcom's Guidance Miss Exposes the Fragility of the AI Trade — Investing.com, 2026-06-04](https://www.investing.com/analysis/broadcoms-guidance-miss-exposes-the-fragility-of-the-ai-trade-200681543)
- [SMCI SEC Filings (Q3 FY26 results; board-led export-control review; BDO auditor) — StockTitan, 2026-05-05](https://www.stocktitan.net/sec-filings/SMCI/)
- Internal: `data/catalysts/2026-06-05/` (Arthur Hayes dumps HYPE+NEAR — AMBCrypto, single_source; "Bitcoin plunges to near $62,000 as the AI trade unwinds" — CoinDesk, single_source).

---

## 14. Fix Requests / TODO

### TODO-unh-legal-gate
- **issue:** UNH still emitted as A-tier 81.3 intraday LONG while under an active DOJ criminal+civil Medicare-fraud investigation; the legal/headline-risk gate does not block or demote it. Same defect flagged at 04:30, still open ~7 h later.
- **evidence:** `active-signals --asset-class stocks` row `sig_aba948056b8fc1ab UNH stocks A intraday long 81.3 triggered`; DOJ probe verified (Yahoo 2025-07-31, Phemex, SEC 10-Q). Fresh intraday run separately rejects UNH long (31.64, long_in_risk_off_regime).
- **suggested manual fix:** add a hard legal-risk gate (DOJ/SEC/indictment/antitrust keyword → cap tier at C or force AVOID) in the stocks scoring/risk-penalty layer; backtest against UNH/SMCI.
- **priority:** high
- **first observed:** 2026-06-05 04:30 EEST (re-confirmed 2026-06-05 11:45 EEST)

### TODO-unh-price-staleness
- **issue:** UNH A-tier signal entry (~394–397) is far above the cited analyst target ($354) and post-crash prints (~$280) — suggests a stale/incorrect price feed for the carry-forward signal.
- **evidence:** `active-signals` UNH entry_low 394.43 / entry_high 396.82 vs external target $354.42 (Yahoo) and ~$280 (Phemex 2026).
- **suggested manual fix:** verify the stocks price-feed timestamp on carry-forward signals; consider auto-expiring/repricing A/B signals whose underlying quote is >N hours old.
- **priority:** medium
- **first observed:** 2026-06-05 11:45 EEST

### TODO-stocks-index-nan
- **issue:** Stocks intraday report shows all index 5d/20d returns as `nan` (SPY/QQQ/IWM/DIA) and breadth 0.0%, while VIX (16.06) reads correctly. The risk_off regime label may be partly an artifact of a broken returns computation.
- **evidence:** `data/reports/stocks/intraday/2026-06-05_06-10_stocks_intraday_report.md` §1–2 ("5d=+nan%, 20d=+nan%", "Benchmark (SPY) 20d return: +nan%", breadth 0.0%).
- **suggested manual fix:** investigate the index-return/breadth computation (likely insufficient OHLCV history or a NaN-propagation bug) in the stocks regime module; ensure the regime label degrades gracefully when returns are NaN.
- **priority:** medium
- **first observed:** 2026-06-05 11:45 EEST

### TODO-swing-invest-staleness
- **issue:** Crypto swing, stocks swing, and stocks invest reports are all ~18 h old (06-04 14:44–15:01) — the overnight scheduler did not regenerate them, so swing/invest verdicts run on stale data.
- **evidence:** mtimes — `swing/2026-06-04_14-44` (17:44), `stocks/swing/2026-06-04_14-55` (17:55), `stocks/invest/2026-06-04_15-01` (18:01).
- **suggested manual fix:** confirm the swing/invest cadence in the scheduler config; if intended (lower frequency), surface the expected next-regen time in reports so staleness is not mistaken for a failure.
- **priority:** low
- **first observed:** 2026-06-05 11:45 EEST

### TODO-catalyst-stock-usdt-mismap
- **issue:** The catalyst symbol resolver maps equities news to fake crypto pairs — AVGO/USDT (37), NVDA/USDT (20), UNH/USDT (9), TSLA/USDT (7), JPM/USDT (6), COIN/USDT (6), MSFT/USDT (5), SMCI/USDT (3). Pollutes crypto catalyst mapping and inflates noise.
- **evidence:** `data/catalysts/2026-06-05/catalyst_events.jsonl` top mapped symbols include 8 stock tickers suffixed `/USDT`.
- **suggested manual fix:** in the catalyst symbol resolver, gate `/USDT` suffixing to known crypto bases (or carry asset_class through) so equity tickers don't resolve to crypto pairs.
- **priority:** low
- **first observed:** 2026-06-05 11:45 EEST

### TODO-catalyst-mapping-weak (recurring)
- **issue:** Catalyst unmapped rate 74% this run (72.4% at 04:30) — persistently above 50%, keeping the catalyst layer context-only across runs.
- **evidence:** 832/1124 unmapped today; 04:30 review reported 72.4%.
- **suggested manual fix:** improve the catalyst→symbol resolver (alias table, entity extraction) to push mapped rate above 50% so the layer can contribute to decisions.
- **priority:** medium
- **first observed:** 2026-06-05 04:30 EEST (recurring)
