# Opus Enriched Review — US open reaction review — Auto Cycle 18:30 EEST

- **Generated:** 2026-06-05 18:39 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`, **US open reaction review** slot 18:30). US cash session has been open ~2h09m (opened 16:30 EEST / 09:30 ET; now ~12:09 ET). Crypto and stocks are **both live actionable** this slot.
- **Slot focus:** first US-session reaction / early confirmation — did the pre-open AI/semis derating follow through after the open, and which A/B setups confirmed vs. invalidated.
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-05_1624.md` (pre-US-open decision review, 16:24 EEST, ~2.25 h ago — §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). This run externally verified: (1) the **Broadcom-led semiconductor selloff** (AVGO −14%, ~$350B mcap erased; Q3 AI-chip guide $16B vs $17.2B est; FY $56B, no 2026 AI raise) and its **second-day follow-through** (AMD opened **−3.88%**, ~−2.8% intraday; NVDA −1.4%; Micron premarket −3.3%); (2) the **LLY GLP-1 catalyst** (TD Cowen raised GLP-1 to $150B by 2030, reiterated **Buy, PT $1,250**, LLY 62% share). WebFetch on the Seeking Alpha LLY URL returned **HTTP 403** (auth-walled) → search-corroborated across TradingView/Stocktwits + Investing.com; the TradingKey AMD URL WebFetch opened cleanly.
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; all price/structure is local OHLCV/ATR/EMA report fields + cited external prints.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

- **The defining tension this slot: the signal engine is bullish-by-regime, but today's live catalyst is a confirmed second-day semiconductor derating.** The stocks intraday report labels the regime **bullish** (VIX 16.29, breadth 100% > EMA20, 4/4 indices uptrend, SMH/XLK still RS-leaders on a 20-day lookback) and so emits **long** A-tier signals with a full +15 `market_regime_alignment` bonus. But the dominant intraday catalyst — Broadcom's soft AI-chip guide — has now **followed through for a second session**: **AMD opened −3.88% (≈−2.8% second day), NVDA −1.4%, Micron −3.3% premarket**. The 20-day trend is up; the last 48 hours are down. Any fresh **AMD/NVDA long is a continuation setup fired against a confirmed 2-day downtrend** → these are the contradiction-risk candidates, not clean actionables.
- **LLY is the cleanest long on the board and it strengthened this slot.** Eli Lilly A-tier **intraday score rose 86.1 → 94.7** and now carries a **fresh, externally-verified positive catalyst**: TD Cowen raised the GLP-1 market to **$150B by 2030** (from $139B), reiterated **Buy, PT $1,250**, with LLY holding **62% share** and ~59M patients projected by 2030. LLY sits **outside** the AI-trade derating (pharma/GLP-1, healthcare is an RS-strong sector +4.53% 20d). Current ~$1,156–1,163, entry trigger 1162.6, SL 1143.8, TP1 1181.5 — PT well above entry. **The one A-tier long whose catalyst confirms its thesis.**
- **Crypto is a clean, catalyst-aligned SHORT bias — the mirror of the AI risk-off.** Regime **bearish trend (risk-off)**: BTC downtrend, ETH downtrend, altcoin breadth **27.1% > EMA20**. Verified context: **BTC dropped below $61,000 (−$18K in 10 days)**, BTC-ETF outflows continuing (−196 BTC 1D, though BlackRock paused its outflow), **$547M ETH at risk of liquidation** in DeFi (lookonchain). All active crypto signals are **B-tier breakdown SHORTS** (ETH 67.7, TON 68.2, FET 67.0, NEAR/ADA/PUMP triggered) — direction-aligned with the tape. The caution is the same as 16:24: deeply oversold → **relief-bounce squeeze risk**, so shorts only on failed bounces into entry zones, not chasing the flush.
- **Net verdict:** **LLY = the one clean stock long** (defensive, off-AI, catalyst-confirmed — half-size on a hold above the open). **AMD / NVDA A-tier longs = AVOID / MANUAL REVIEW** (fighting a confirmed 2-day semis selloff + AMD analyst downgrade + insider selling). **AAPL A-tier long = WATCH only** (tech leader but soft tape, waiting_for_entry). **Crypto = short-biased no-chase** — ETH/BTC/alt breakdown shorts are valid on failed bounces; respect BTC $60K. Catalyst layer **context-only (73% unmapped)**.

---

## 2. Data Used

**Internal — fresh (<4 h):**
- `data/reports/scalp/2026-06-05_13-30_scalp_report.md` (mtime 16:30 EEST; ~2.1 h). Regime **bearish trend (risk-off)**; BTC/ETH downtrend; altcoin breadth 27.1% > EMA20; recommended style "short bias or no trade." Top RS-down: ZEC −39.05% 24h, PORTAL −16.4%, ZEN −16.1%.
- `data/reports/intraday/2026-06-05_13-54_intraday_report.md` (mtime 16:54 EEST; ~1.8 h).
- `data/reports/swing/2026-06-05_14-34_swing_report.md` (mtime 17:34 EEST; ~1.1 h) — **fresh this run** (no longer the >22 h stale file flagged at 16:24).
- `data/reports/stocks/intraday/2026-06-05_15-30_stocks_intraday_report.md` (mtime 18:30 EEST; ~9 min — **very fresh, regular session**). Regime **bullish** (VIX 16.29, breadth 100%). Top ideas: #1 LLY A 94.7, #2 AAPL A long, #3 XLV long, #4 JPM long. NVDA/AMD/SMCI carry the Broadcom headline.
- `data/reports/stocks/swing/2026-06-05_14-51_stocks_swing_report.md` (mtime 17:51 EEST; ~0.8 h — **fresh**).
- `data/reports/stocks/invest/2026-06-05_14-55_stocks_invest_report.md` (mtime 17:56 EEST; ~0.7 h — **fresh**).
- LLM packets: `data/processed/llm_analysis_packet.md` (17:34), `data/processed/llm_stocks_packet.md` (17:56).

**Catalyst / narrative:** `data/catalysts/2026-06-05/` — `catalyst_events.jsonl` (**2058 rows**), `narrative_baskets.jsonl` (**3 baskets**), latest `catalyst_cycle_13-54.md` (mtime 16:54).

**CLI / DB (read-only):** `active-signals` (crypto **19**, stocks **50**), `signal-stats` (crypto + stocks, week), `detect_untracked_legacy_alerts --since 2026-06-05` → **1 untracked** (FET/USDT). DB: `db/crypto_ai_desk.sqlite` (743 MB, mtime 18:36) — `proposed_signals` 167 active, 10 A-tier (all stocks long); `news_items` queried for LLY/AAPL/AMD/NVDA/ETH/BTC + `t.me/*` (last 6 h).

**External (this run — cited §13):** Broadcom selloff (Bloomberg, CNBC, 24/7 Wall St, Stocktwits); AMD/NVDA second-day reaction (TradingKey WebFetch-verified, Stocktwits); LLY GLP-1 (TradingView/Stocktwits, Investing.com); BTC <$61K (CryptoBriefing, internal news_item).

**Unavailable / blind:** live tick prints; TradingView/Chrome chart verification (not loaded); liquidation heatmaps / order-book / CVD; live ETF-flow feed; Seeking Alpha (403, auth-walled).

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-05_default_schedule/`.
- `scheduler.log` mtime **17:56 EEST → ~0.7 h** (fresh). Latest cycle summary `cycle_01_16-01_summary.md` mtime **17:56 EEST → ~0.7 h** (fresh, well under 3 h).
- **NO DEFER** — both freshness anchors are < 1 h; the BOTH-older-than-3 h condition is not met.
- **Report freshness:** all six reports are **fresh (<4 h)** this run — crypto scalp ~2.1 h, intraday ~1.8 h, swing ~1.1 h; stocks intraday ~0.15 h, swing ~0.8 h, invest ~0.7 h. The swing/invest **staleness flagged at 16:24 (~22 h) has cleared** — fresh batches regenerated 17:34–17:56. `TODO-swing-invest-staleness` can be considered **resolved this run** (monitor for recurrence).

---

## 4. What Changed vs Previous Review (16:20 → 18:30)

- **Slot advanced from pre-open to ~2 h into the US session.** The pre-open *forecast* (AVGO −13% premarket, Nasdaq-100 futures −1.12%) is now **realized intraday**: chip stocks fell for a **second consecutive day** — AMD **−3.88% at the open / ≈−2.8% on the day**, NVDA −1.4%. The "wait for an AMD 496–516 reclaim" condition from 16:24 **did not trigger** — price went lower, not higher. The AMD/NVDA longs are now clearly *fighting* the tape, not merely "in the selloff."
- **LLY upgraded and catalyst-confirmed.** Intraday score **86.1 → 94.7**; the TD Cowen **$150B GLP-1 / Buy / PT $1,250** print is fresh today and directly supports the long. LLY moves from "watch a defensive leader hold" to **the single cleanest actionable long** this slot.
- **New AMD bear inputs surfaced:** an analyst **downgrade (strong-buy → hold)** and **$122.1M of insider selling over 3 months** (TradingKey), plus strong May jobs data fueling Fed-hawkish pressure on growth stocks — all incremental negatives on top of the Broadcom catalyst.
- **UNH de-escalated from A-tier to B-tier.** At 16:24 UNH was an A-tier 81.3 long under the `TODO-unh-legal-gate` (DOJ-probe) flag; this run it is **B-tier 78.59 long**. The legal-gate concern is lower-priority but **not cleared** — carry-forward (could not re-verify DOJ status without spending the run's web budget on a non-top-5 name).
- **Untracked legacy alerts: 0 → 1 (regression this run).** `FET/USDT` B scalp short (65.7, sent 13:38) has **no matching `proposed_signal`** → it won't contribute to PF/winrate. New occurrence vs the clean 0 at 16:24 → `TODO-untracked-legacy-alert` (§14).
- **Crypto: ZEC swing-long still INVALIDATED, deeper.** ZEC −39% 24h (scalp report); the active ZEC **swing LONG** (B 65) remains a live thesis contradiction — carry-forward INVALIDATED.
- **Catalyst mapping ~unchanged:** 73.4% unmapped (16:24) → **73.1% unmapped** this run (1505/2058). Still context-only.

---

## 5. Catalyst Coverage

- Raw `catalyst_events.jsonl`: **2058 rows.**
- Mapped (non-null symbol): **553** · Unmapped (null symbol): **1505** · **Unmapped = 73.1%.**
- `narrative_baskets`: **3** (all freshness <1h; basket name/member fields parsed as null in the JSONL — structural quirk, see §14 `TODO-basket-fields-null`).
- **⚠ CATALYST MAPPING WEAK THIS RUN (73.1% unmapped > 50%) — use the catalyst layer as CONTEXT, NOT a final decision input.**
- **Top-3 unmapped headlines:** (1) "Asia-Pacific markets set to open subdued after Wall Street's AI-linked stocks slide" (macro/AI-derating, importance 0.444); (2) "Palantir partners with Kirkland & Ellis to develop AI tools for private equity" (0.579); (3) "5 Top Artificial Intelligence (AI) Stocks to Buy With $5,000 Right Now" (0.444). Note the #1 unmapped headline independently corroborates the AI-slide theme that the mapped AMD/NVDA news already captured.

---

## 6. Market Landscape

- **Stocks (live, ~2 h into session):** Engine regime **bullish** (VIX 16.29, breadth 100% > EMA20/EMA50, SPY/QQQ/IWM/DIA all uptrend on 20d). BUT 5-day returns are red across the board (SPY −1.09%, QQQ −2.16%, IWM −1.40%) — the bullish label is a **lagging 20-day read**; the **near-term tape is a sector-specific AI/semis derating**. Sector RS (20d): semiconductors +7.44%, technology +7.00%, healthcare +4.53% (LLY's sector — strong and *not* the one being sold today). Communications weakest (−6.49%). Net: **rotation out of AI-semis, healthcare/value holding** — favorable for LLY, hostile for fresh AMD/NVDA longs.
- **Crypto (live):** Regime **bearish trend (risk-off)**; BTC & ETH downtrend; altcoin breadth 27.1% > EMA20. **BTC < $61K (−$18K/10 days)**, ETF outflows continuing, $547M ETH liquidation risk. Macro risk 39/100 (risk-off tilt). Style: **short bias or no trade; avoid weak altcoin longs.** Oversold → relief-bounce risk caps short-chasing.
- **Macro cross-asset:** May jobs beat → Fed-hawkish lean pressuring growth/AI; USMCA trade talks missed the July deadline (trade-tension risk rising, WalterBloomberg). Risk-off skew across both books, with healthcare/defensives the relative haven.

---

## 7. Candidate Deep Dives (5)

### 7.1 LLY — stocks A intraday long (score 94.7) — **CLEAN ACTIONABLE (best)**
- **Setup:** continuation, trend=uptrend, RS=leader, regime=bullish. Entry 1156.33–1162.62 (trigger 1162.62), SL/inval 1143.75, TP1 1181.49, TP2 1194.07 (rr_tp1 ~1.0). Also A swing (83.78, entry→1160.7, TP1 1216) and A invest (82.13, TP1 1282).
- **Catalyst (verified, confirms):** TD Cowen raised GLP-1 market to **$150B by 2030**, reiterated **Buy, PT $1,250**, LLY **62% share**, ~59M GLP-1 patients by 2030. Internal news_items corroborate: "UnitedHealth, Eli Lilly lead healthcare rankings" (Seeking Alpha), "3 Reasons Eli Lilly Remains a Buy" (Motley Fool). `news_supported=0` in the DB row (engine scored it purely technically) — but the **external catalyst is aligned**, the opposite of the AMD/NVDA problem.
- **LEGAL/HEADLINE RISK:** none found (GLP-1 pricing deal previously digested; no indictment/SEC/auditor/guidance-withdrawal flags).
- **Price-reaction / chase check:** healthcare sector RS-strong and NOT the sector being sold; the move is catalyst-supported, not an overextended chase. Entry trigger 1162.6 is just above spot (~1156–1163) → **not late** if it holds above the open. Risk: it is still a long into a broadly red 5-day tape → **half-size, require a post-open hold above ~1156, no chase above 1170**.
- **Verdict:** **ACTIONABLE LONG (half-size, on a hold).** Highest-conviction name on the board.

### 7.2 AMD — stocks A swing long (score 81.79, triggered) — **AVOID / MANUAL REVIEW**
- **Setup:** continuation long, entry 501.05–515.74, SL 471.67, TP1 559.82. Multiple A swing instances (493–507, 479–495) + B intraday.
- **Catalyst (verified, CONTRADICTS):** Broadcom's soft AI-chip guide (Q3 $16B vs $17.2B est) triggered a sector selloff; **AMD opened −3.88%, ≈−2.8% for a second day**; plus an analyst **downgrade strong-buy→hold** and **$122.1M insider selling/3 mo** (TradingKey), P/E 173x flagged as rich. `news_supported=0` — the engine never ingested the bearish catalyst into the score.
- **Price-reaction / chase check:** price has **already reacted to the downside** for two sessions; a long-continuation entry here is **chasing strength that isn't there / catching a falling knife**. No reclaim of the entry band; the move is below, not above, trigger. **Entry now would be fighting a confirmed downtrend.**
- **Verdict:** **AVOID / MANUAL REVIEW REQUIRED** — technical-only A-tier long contradicted by a verified 2-day sector derating + name-specific downgrade/insider selling. Reconsider only on a decisive reclaim of 501–516 with the semis complex stabilizing.

### 7.3 NVDA — stocks A swing long (score 80.64, triggered) — **AVOID / MANUAL REVIEW**
- **Setup:** continuation long (RS=follower), entry 218.65–222.82, SL 210.31, TP1 235.33.
- **Catalyst (verified, CONTRADICTS):** same Broadcom-led semiconductor selloff; **NVDA −1.4%** on the session, second down day; the stocks intraday report attaches the "Nasdaq Futures Plunge … AMD −4%" headline to NVDA. `news_supported=0`.
- **Price-reaction / chase check:** less hard-hit than AMD (−1.4% vs −3.9%) but still red and inside the same derating; long-continuation is counter-tape. Not late to a move that is going the *other* way.
- **Verdict:** **AVOID / MANUAL REVIEW** — same logic as AMD, milder magnitude. Watch for a sector-wide stabilization before any long.

### 7.4 AAPL — stocks A intraday long (score 86.99) — **WATCH (conditional)**
- **Setup:** continuation long, RS=leader, regime=bullish. Entry 312.17–313.11 (trigger 313.11), SL 310.29, TP1 315.93, TP2 317.81. Tight rr (~1.0), `waiting_for_entry`.
- **Catalyst:** no AAPL-specific bullish catalyst today; the only fresh hit is the broad "US PREMARKET MOVERS … S&P futures down 0.5%" (WalterBloomberg). Not chip-exposed in the Broadcom sense, but caught in the broad soft tape.
- **Price-reaction / chase check:** `waiting_for_entry` with a tight band; trigger 313.11 just above spot. In a red-leaning tape the breakout-trigger long has elevated failure odds. Not a contradiction (no negative AAPL catalyst), but no positive confirmation either.
- **Verdict:** **WATCH** — only on a clean trigger break >313.11 that holds; otherwise stand aside. Lower priority than LLY.

### 7.5 ETH/USDT — crypto B scalp short (score 67.7) — **ACTIONABLE SHORT (no-chase) — represents the crypto book**
- **Setup:** breakdown short, entry 1662.2–1675.4 (trigger 1662.2), SL/inval 1691.6, TP1 1627.0, rr_tp1 ~1.2. (Other aligned B shorts: TON 68.2, FET 67.0, NEAR/ADA/PUMP triggered.)
- **Catalyst (verified, CONFIRMS):** BTC <$61K (−$18K/10d), ETF outflows, **$547M ETH at liquidation risk** (lookonchain) — bearish, direction-aligned.
- **Price-reaction / chase check:** regime bearish, breadth 27% — the short bias is correct, but BTC/ETH are **deeply oversold** → relief-bounce squeeze risk. **Do not chase the flush**; short only on a *failed bounce* back into 1662–1675, honoring the 1691.6 invalidation.
- **Verdict:** **ACTIONABLE SHORT on a failed bounce, no-chase, honor invalidation.** Crypto is the catalyst-aligned book this slot.

**Excess candidates (>5, deferred):** other crypto B shorts (TON, FET, NEAR, ADA, PUMP, AVAX, DAR, BTC, EPIC, ZRX) — same bearish-aligned thesis as ETH, no separate research needed; stock B/C longs (JPM, SMH, XLK, QQQ, XLV, SMCI) — index/sector betas, no idiosyncratic catalyst; **ZEC swing long** — excluded as INVALIDATED (see §9).

---

## 8. Best Candidates Ranked

1. **LLY (stocks, A intraday long, 94.7)** — *ACTIONABLE, half-size on a hold.* Cleanest long: catalyst-confirmed (TD Cowen $150B GLP-1, Buy PT $1,250), defensive/off-AI, RS-strong sector.
2. **ETH/USDT (crypto, B scalp short, 67.7)** — *ACTIONABLE short on a failed bounce.* Catalyst-aligned with the risk-off tape; no-chase, honor 1691.6.
3. **AAPL (stocks, A intraday long, 86.99)** — *WATCH.* Only on a clean >313.11 hold; soft tape, no positive catalyst.
4. **NVDA (stocks, A swing long, 80.64)** — *AVOID/MANUAL REVIEW.* Inside the 2-day semis selloff (−1.4%).
5. **AMD (stocks, A swing long, 81.79)** — *AVOID/MANUAL REVIEW.* Worst contradiction: −3.88% open, downgrade, insider selling, P/E 173x.

---

## 9. Avoid / No Trade

- **AMD / NVDA A-tier longs** — AVOID. Technical-only longs (`news_supported=0`) contradicted by a verified 2-day Broadcom-led semiconductor selloff; AMD additionally downgraded + heavy insider selling.
- **ZEC swing LONG (crypto, B 65)** — **INVALIDATED.** ZEC −39% 24h (scalp report) on the prior counterfeiting-vulnerability exploit thesis; a long remains active against a collapsing chart. Carry-forward from 16:24.
- **UNH long (stocks, B 78.59)** — **GATED / caution.** De-escalated from A→B this run; prior DOJ Medicare-fraud-probe flag (16:24) not re-verified this run → treat as MANUAL REVIEW for any long, do not auto-action. Carry-forward `TODO-unh-legal-gate`.
- **SMCI (stocks, C short 55.14)** — penalized (−12) in-report; prior export-control flag — avoid as a clean long; not actionable.
- **Crypto longs generally** — avoid; regime bearish, breadth 27%, "avoid weak altcoin longs."
- **Chasing crypto shorts into the oversold flush** — no-chase; wait for failed bounces.

---

## 10. Main Risks

- **Regime-label vs catalyst divergence (model risk):** the engine's 20-day "bullish" regime grants +15 alignment to longs (AMD/NVDA) whose live 48-hour catalyst is bearish. Acting on the score alone here would buy a falling knife. Mitigation: this review gates AMD/NVDA to AVOID.
- **Oversold relief-bounce (crypto):** BTC/ETH deeply oversold; a sharp squeeze could stop breakdown shorts. Mitigation: failed-bounce entries only, honor invalidations.
- **LLY long into a red broad tape:** even off-AI, a market-wide risk-off leg could drag LLY. Mitigation: half-size, require a post-open hold.
- **Catalyst layer weak (73% unmapped):** symbol resolver still maps equities to fake /USDT pairs (recurring) — context-only this run.
- **Ingest:** if the source-ingest CLI fails, sources still live in the §13 markdown + the JSON artifacts (no data loss).

---

## 11. Action Plan — next 4 hours

1. **LLY:** watch for a post-open **hold above ~1156 and trigger >1162.6** → half-size long, SL 1143.8, first target 1181.5. The cleanest setup; size up only on confirmation.
2. **AMD / NVDA:** **no long.** Re-evaluate only if the semis complex (SMH) stabilizes and AMD reclaims 501–516 / NVDA reclaims its 218.65–222.82 band on volume.
3. **AAPL:** only on a clean break-and-hold >313.11; otherwise stand aside.
4. **Crypto (ETH/TON/FET/NEAR/ADA):** short bias intact — enter only on **failed bounces** into the breakdown zones, honor invalidations (ETH 1691.6); **no chasing** the oversold flush. Respect BTC $60K as the line — a clean break opens lower, a reclaim of $62–63K neutralizes shorts.
5. **Re-read fresh reports before acting** — the scheduler is cycling; newer levels may print within minutes.
6. **No pre-emptive entries on AVOID/MANUAL names.**

---

## 12. Final Verdict per Mode

- **Crypto scalp:** **SHORT-BIASED, no-chase.** ETH/TON/FET breakdown shorts valid on failed bounces; bearish regime + oversold relief-bounce risk; respect BTC $60K. B-tier triggered winrate ~20% / PF 1.17 → small size.
- **Crypto intraday:** **SHORT-BIASED / selective.** NEAR/ADA/PUMP triggered shorts aligned; no longs; same no-chase discipline.
- **Crypto swing:** **NO-TRADE / caution.** Report fresh (~1.1 h) but regime bearish; **ZEC swing-long INVALIDATED**; avoid weak altcoin longs.
- **Stocks intraday:** **LLY = ACTIONABLE long (half-size, on a hold) — best name; AAPL = WATCH (>313.11); AMD/NVDA = AVOID (semis selloff); UNH = MANUAL REVIEW (legal gate); SMCI = avoid.**
- **Stocks swing (fresh ~0.8 h):** **LLY long bias intact (PT $1,250); AMD/NVDA longs gated by the selloff (wait for sector stabilization); UNH excluded (legal).**
- **Stocks invest (fresh ~0.7 h):** **LLY long-term bias constructive (GLP-1 secular); AMD invest long bias intact structurally but de-prioritized while the AI-chip derating plays out; SMCI/UNH excluded.**

---

## 13. Sources

**Semiconductor selloff / AMD / NVDA (CONTRADICT the AMD-NVDA longs):**
- [Broadcom Outlook Falls Short of Investor Expectations for AI Revenue Growth — Bloomberg, 2026-06-03](https://www.bloomberg.com/news/articles/2026-06-03/broadcom-outlook-disappoints-investors-seeking-ai-fueled-blowout)
- [Broadcom stock plunges on weak software sales, unchanged AI chip forecast — CNBC, 2026-06-03](https://www.cnbc.com/2026/06/03/broadcom-avgo-earnings-report-q2-2026.html)
- [Micron Drops 7% as Broadcom's Disappointing AI Outlook Triggers a Semiconductor Selloff — 24/7 Wall St., 2026-06-04](https://247wallst.com/investing/2026/06/04/micron-drops-7-as-broadcoms-disappointing-ai-outlook-triggers-a-semiconductor-selloff/)
- [NVDA, INTC, AMD, MU: Major Chip Stocks Fall For Second Day After AVGO's Soft AI Guidance — Stocktwits, 2026-06-05](https://stocktwits.com/news-articles/markets/equity/nvda-intc-amd-mu-major-chip-stocks-fall-for-second-day-after-avgo-s-soft-ai-guidance/cZ0FhbSRez6)
- [Advanced Micro Devices (AMD) Opened Down 3.88% on Jun 5 — downgrade strong-buy→hold, $122.1M insider selling — TradingKey, 2026-06-05 (WebFetch-verified)](https://www.tradingkey.com/news/market-movers/261949643-market-movers-amd-20260605)

**LLY GLP-1 (CONFIRMS the LLY long):**
- [TD Cowen Raises GLP-1 Sales Forecast To $150B By 2030 — LLY/NVO dominant; LLY 62% share — TradingView/Stocktwits, 2026-06-05](https://www.tradingview.com/news/stocktwits:cb0a2c4cf094b:0-td-cowen-raises-glp-1-sales-forecast-to-150b-by-2030-industry-leaders-lly-nvo-to-remain-dominant/)
- [Eli Lilly maintains Buy rating at TD Cowen on oral GLP-1 potential (PT $1,250) — Investing.com, 2026-06-05](https://www.investing.com/news/analyst-ratings/eli-lilly-stock-maintains-buy-rating-at-td-cowen-on-oral-glp1-potential-93CH-4490757)
- _Seeking Alpha "GLP-1 sales forecast raised to $150B at TD Cowen" — WebFetch returned HTTP 403 (auth-walled); not citable as opened, corroborated by the two sources above._

**Crypto macro (CONFIRMS the short bias):**
- [Bitcoin drops below $61,000, losing $18,000 in 10 days — CryptoBriefing, 2026-06-05 (internal news_item)](https://cryptobriefing.com/bitcoin-drops-below-61000-june-2026/)

---

## 14. Fix Requests / TODO

### TODO-untracked-legacy-alert
- **issue:** 1 untracked legacy crypto alert this run — `FET/USDT` B scalp short (65.7, sent 13:38) has no matching `proposed_signal`, so it won't contribute to PF/winrate/avgR. Regression vs the clean 0 at the 16:24 slot.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-06-05` → "1 untracked legacy crypto alert(s)"; `watchlist_alerts` row FET/USDT 2026-06-05T13:38:48Z.
- **suggested manual fix:** investigate the PART-1 alert→signal registration path (the same intermittent gap documented in `AUDIT_NOTE_UNTRACKED_LEGACY_CRYPTO_ALERTS.md`); ensure every Telegram-sent alert writes a `proposed_signal` with a `signal_id` the tracker can follow.
- **priority:** medium
- **first observed:** 2026-06-05 18:39 EEST (recurrence of a known class)

### TODO-regime-vs-catalyst-gate
- **issue:** A-tier long signals inherit a +15 `market_regime_alignment` bonus from a 20-day "bullish" regime label even when the live intraday catalyst is strongly bearish for the name's sector (AMD/NVDA scored 80–82 long into a confirmed 2-day Broadcom semiconductor selloff; `news_supported=0`). The score does not see the contradicting catalyst.
- **evidence:** `proposed_signals` AMD A swing 81.79 long / NVDA A swing 80.64 long, both `news_supported=0`; stocks intraday report attaches "Nasdaq Futures Plunge … AMD −4%" to both; external: AMD −3.88% open / 2nd down day (TradingKey, Stocktwits).
- **suggested manual fix:** add a catalyst/headline gate that demotes or flags long signals when fresh high-importance bearish news for the symbol/sector exists (mirror the §I legal-gate pattern); at minimum surface `news_supported` and a sector-derating penalty in the A-tier ranking.
- **priority:** high
- **first observed:** 2026-06-05 18:39 EEST

### TODO-unh-legal-gate (carry-forward)
- **issue:** UNH still emitted as a long signal (B 78.59 this run; was A 81.3 at 16:24) without an enforced legal-risk gate for the prior DOJ Medicare-fraud-probe flag.
- **evidence:** stocks intraday report row `| UNH | long | B | 78.59 | high | -4.0 |`; prior reviews 04:30/11:45/16:24.
- **suggested manual fix:** implement a hard legal-risk gate (indictment/DOJ/SEC investigation) that blocks or down-tiers affected long signals and re-verify UNH's current DOJ status.
- **priority:** medium
- **first observed:** 2026-06-05 04:30 EEST (carry-forward)

### TODO-catalyst-stock-usdt-mismap (carry-forward)
- **issue:** symbol resolver maps equities news to fake crypto /USDT pairs (e.g. AVGO/USDT, NVDA/USDT, UNH/USDT), inflating unmapped/mismapped catalyst counts. Catalyst mapping 73.1% unmapped again this run.
- **evidence:** recurring across 11:45 / 16:24 reviews; catalyst coverage 553 mapped / 1505 unmapped today.
- **suggested manual fix:** add an asset-class-aware resolver that routes equity tickers to the stocks namespace instead of fabricating /USDT pairs.
- **priority:** medium
- **first observed:** 2026-06-03 (carry-forward)

### TODO-basket-fields-null
- **issue:** `narrative_baskets.jsonl` rows parse with null name/members/size under the field names this review probed (`name`/`narrative`/`basket`, `members`/`symbols`/`size`) — only `freshness` resolved. Prior reviews read basket names fine (e.g. `ai_narrative`), so either the schema changed or the keys differ this run; downstream consumers may silently get empty baskets.
- **evidence:** §5 probe printed "basket: None | members: None" for all 3 baskets while `catalyst_cycle_*` exists.
- **suggested manual fix:** confirm the current `narrative_baskets.jsonl` field schema and align the catalyst-basket reader/consumers to it.
- **priority:** low
- **first observed:** 2026-06-05 18:39 EEST
