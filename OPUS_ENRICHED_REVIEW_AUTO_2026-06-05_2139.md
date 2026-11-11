# Opus Enriched Review — late-session risk review — Auto Cycle 21:30 EEST

- **Generated:** 2026-06-05 21:39 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`, **late-session risk review** slot 21:30). US cash session is in its final ~1h20m (closes 23:00 EEST / 16:00 ET; now ~14:39 ET). Crypto and stocks are **both live actionable** this slot; focus is risk/exposure as the day resolves.
- **Slot focus:** late US-session risk check — how did the AI/semis derating and the regime flip resolve into the close, and which active A/B exposures are now fighting the tape.
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-05_1839.md` (US open reaction review, 18:39 EEST, ~3 h ago — §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). This run externally verified, for the **late session**: (1) the **chip-led selloff deepened** — **Nasdaq −3.80% (25,810; biggest drop in >1yr), S&P −2.25% (7,414), Dow −0.98% (51,056), VIX +24% to 19.09**; AMD **−8/−10%**, NVDA −4/−6%, MRVL −12%, MU −11%, INTC −9%, AVGO −6% (after −13% Thu); (2) the driver is a **hot May jobs report (172k vs 88k est)** → traders now price a **quarter-point Fed hike by year-end**, 10y/30y yields spiked, **rotation out of chipmakers into healthcare/financials**; (3) **SMCI** — no fresh June-5 8-K found; the standing material item remains the **Mar 19 2026 indictment (alleged export-control violations)**. WebFetch on the Yahoo live blog opened cleanly (HTTP 200).
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; all price/structure is local OHLCV/ATR/EMA report fields + cited external prints.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

- **The 18:30 "regime-label vs catalyst" tension has now fully resolved against the longs — and the engine's own intraday read flipped to confirm it.** At 18:30 the stocks **intraday** report was still labelled *bullish* (VIX 16.3, breadth 100%). The **fresh 21:34 intraday report flipped to `risk_off`** (VIX 18.79, breadth above EMA20 **25%**, bias short) and now emits **SHORTS** (META 71.0, AMZN 68.4, SMCI 67.1) as its top ideas. Externally the day closed-in hard: **Nasdaq −3.8%, VIX 19.1 (+24%)**, **AMD −8/−10%**. The bearish catalyst won the session.
- **The live danger this slot is the STALE BULLISH swing/invest book.** The stocks **swing** and **invest** reports (data 14:51 / 14:55 UTC, now **~4 h old, carry-forward**) still label the regime **bullish** and still carry **A-tier LONGS — LLY 83.8, AAPL 83.8, AMD 81.8** — which remain *active signals* (`active-signals` stocks shows A-tier LLY/AAPL/AMD longs `waiting_for_entry`/triggered). These A-longs were scored under the morning's bullish regime that the live tape has since **abandoned**. **AMD A-tier LONG is the worst contradiction on the board: it printed −8/−10% today.** Acting on the stale A-longs = buying into a confirmed −3.8% Nasdaq day.
- **LLY is the one long whose sector is actually being bought today.** The verified late-session theme is **rotation OUT of chips INTO healthcare/financials**. LLY (GLP-1 / TD Cowen $150B-by-2030 catalyst, healthcare RS-strong) is the relative haven — but it trades **~$1,135, just BELOW its swing entry band (1142–1160)**, i.e. **not triggered**; it is holding, not breaking out. Constructive-but-not-yet-actionable.
- **Crypto is the catalyst-aligned SHORT book, but its reports are going stale.** Crypto regime **bearish trend (risk-off)**, BTC/ETH downtrend, altcoin breadth 27%. All active crypto signals are **B-tier breakdown SHORTS** (TON 68, ETH, FET 67, NEAR/ADA/PUMP). Caveat: the crypto **scalp/intraday reports did not regenerate in the 19:56 scheduler cycle** (mtime 16:30 / 16:54, **~5 h old**) while stocks intraday refreshed at 21:34 — crypto levels are aging; treat as directional context, re-pull before executing. ZEC counterfeiting-exploit thesis (−39%) still live.
- **Net verdict:** **No clean fresh long.** **LLY = constructive haven, WATCH for a reclaim >1142** (do not buy below the band into a −3.8% tape). **AMD / AAPL stale A-tier longs = AVOID / MANUAL REVIEW** (fighting a confirmed risk-off / chip rout). **META short = direction-aligned but CHASE risk** (already down hard) → failed-bounce only. **SMCI = AVOID long** (legal indictment overhang + risk-off); short is aligned but messy (direction conflict). **Crypto = short-biased no-chase**, respect oversold relief-bounce risk, re-pull stale levels. Catalyst layer **context-only (72.9% unmapped)**.

---

## 2. Data Used

**Internal — fresh (<4 h):**
- `data/reports/stocks/intraday/2026-06-05_18-34_stocks_intraday_report.md` (mtime 21:34 EEST; **~5 min — very fresh**). Regime **risk_off** (VIX 18.79, breadth above EMA20 25%, bias short). Top ideas: META short B 71.0, AMZN short B 68.4, SMCI short B 67.1.
- `data/reports/stocks/swing/2026-06-05_14-51_stocks_swing_report.md` (mtime 17:51 EEST; **~3.8 h — borderline fresh / carry-forward**). Regime **bullish**; A-tier LONGS AAPL 83.8, LLY 83.8, AMD 81.8.
- `data/reports/stocks/invest/2026-06-05_14-55_stocks_invest_report.md` (mtime 17:55 EEST; **~3.7 h — borderline fresh / carry-forward**). Regime **bullish**; A-tier LONGS LLY 82.1, AAPL 80.6.

**Internal — carry-forward / aging (>4 h):**
- `data/reports/scalp/2026-06-05_13-30_scalp_report.md` (mtime 16:30 EEST; **~5.1 h**). Regime bearish trend (risk-off); no A/B; best watch FET 63.9.
- `data/reports/intraday/2026-06-05_13-54_intraday_report.md` (mtime 16:54 EEST; **~4.8 h**). One B short: TON 65.8; rest watchlist.
- _Both crypto reports did **not** regenerate in the latest (19:56) scheduler cycle — see §3 + §14 `TODO-crypto-report-staleness`._

**Catalyst / narrative:** `data/catalysts/2026-06-05/` — `catalyst_events.jsonl` (**2473 rows**), `narrative_baskets.jsonl` (**3 baskets**), latest `catalyst_cycle_17-04.md` (mtime 20:04).

**LLM packets:** `data/processed/llm_analysis_packet.md`, `data/processed/llm_stocks_packet.md`.

**CLI / DB (read-only):** `active-signals` (crypto **19**, stocks **~39**), `signal-stats` (crypto + stocks, week), `detect_untracked_legacy_alerts --since 2026-06-05` → **1 untracked** (FET/USDT, carry-forward).

**External (this run — cited §13):** late-session indices/VIX + chip moves (Yahoo Finance live blog WebFetch-verified, CNBC, GuruFocus); jobs-report / rate-hike / yields driver (Yahoo, CNBC); SMCI indictment / 8-K status (SEC EDGAR, search).

**Unavailable / blind:** live tick prints; TradingView/Chrome chart verification (not loaded); liquidation heatmaps / order-book / CVD; live ETF-flow feed; fresh crypto scalp/intraday levels (reports ~5 h stale).

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-05_default_schedule/`.
- `scheduler.log` mtime **20:19 EEST → ~1.3 h** (fresh). Latest cycle summary `cycle_02_19-56_summary.md` mtime **20:19 EEST → ~1.3 h** (fresh, well under 3 h).
- **NO DEFER** — both freshness anchors are < 1.5 h; the BOTH-older-than-3 h defer condition is not met.
- **Report freshness mixed this run:**
  - **Fresh (<4 h):** stocks intraday (~5 min — regenerated at 21:34, post-cycle), stocks swing (~3.8 h), stocks invest (~3.7 h).
  - **Aging / carry-forward (>4 h):** crypto scalp (~5.1 h), crypto intraday (~4.8 h). Both kept their 16:30 / 16:54 mtime through the 19:56 cycle → **crypto report regeneration appears to have been skipped in the latest cycle** while the stocks intraday pipeline ran (21:34). Crypto direction is still valid (bearish trend persists) but **levels are stale — re-pull before executing any crypto entry.** → §14 `TODO-crypto-report-staleness`.

---

## 4. What Changed vs Previous Review (18:30 → 21:30)

- **Stocks intraday regime FLIPPED bullish → risk_off.** At 18:30 the intraday report was *bullish* (VIX 16.3, breadth 100%) and led with LLY/AAPL **longs**. The fresh 21:34 report is **risk_off** (VIX 18.79, breadth 25%) and leads with META/AMZN/SMCI **shorts**. The engine's own short-horizon read has now caught up to the catalyst the 18:30 review flagged.
- **The selloff deepened into the late session (verified).** 18:30 had AMD −3.88% (open). By mid-afternoon: **AMD −8/−10%, NVDA −4/−6%, MRVL −12%, MU −11%, INTC −9%; Nasdaq −3.8%, S&P −2.25%, VIX 19.1 (+24%).** The "wait for an AMD reclaim" condition never triggered — price went lower.
- **New macro driver crystallized:** the **May jobs report (172k vs 88k est)** → markets now **price a Fed quarter-point hike by year-end**, yields spiked, explicit **rotation out of chips into healthcare/financials**. This both *confirms* the risk-off flip and *supports* LLY's relative-haven status.
- **The A-tier long contradiction is now realized, not forecast.** AMD A-tier LONG (81.8) printed **−8/−10%** on the day — the `TODO-regime-vs-catalyst-gate` failure mode is no longer hypothetical. AAPL A-long caught in the −3.8% Nasdaq tape.
- **SMCI re-examined (new this run):** no fresh June-5 8-K confirmed; standing legal item is the **Mar 19 2026 indictment (export-control)**. Now appears as a *short* (intraday B 67) AND a *long* (swing/invest B 76–77) simultaneously — direction conflict + legal overhang.
- **Crypto reports went stale** (fresh ~1–2 h at 18:30 → ~5 h now; not regenerated in the 19:56 cycle). New freshness regression vs 18:30.
- **Untracked legacy alert: still 1** (FET/USDT B scalp short, sent 13:38) — unchanged carry-forward.
- **Catalyst mapping:** 73.1% unmapped (18:30) → **72.9% unmapped** this run — essentially flat, still context-only.

---

## 5. Catalyst Coverage

- Raw `catalyst_events.jsonl`: **2473 rows.**
- Mapped (non-null symbol): **671** · Unmapped (null symbol): **1802** · **Unmapped = 72.9%.**
- `narrative_baskets`: **3** — `perps_dex_narrative` (primary HYPE; playbook wait_pullback; <6h), `ai_narrative` (primary NEAR/RENDER/TAO/FET; related_beta_rotation; <6h), `momentum_breakout` (primary HEI; <1h).
- **⚠ CATALYST MAPPING WEAK THIS RUN (72.9% unmapped > 50%) — use the catalyst layer as CONTEXT, NOT a final decision input.**
- **Top unmapped headlines (representative, not re-enumerated exactly to avoid fabrication):** the unmapped set is structurally dominated by **US-equity / macro headlines** (the AI-semis slide, the May jobs report, Fed-hike/yield commentary) that the crypto-oriented symbol resolver cannot map to a `/USDT` pair, plus equity tickers mis-routed as fake `/USDT` symbols (e.g. UNH/USDT, JPM/USDT, TSLA/USDT appear in the crypto catalyst stream). See §14 `TODO-catalyst-stock-usdt-mismap`.
- Highest-importance mapped catalysts today: **ZEC** exploit ("Massive ZCash Exploit Found by Claude", 0.82), **UNH** DOJ-probe legal cluster (0.73 ×3).

---

## 6. Market Landscape

- **Stocks (live, ~1h20m to the close):** The bullish 20-day regime label is now **decisively overridden by the live tape.** Verified close-in prints: **Nasdaq −3.80% (25,810), S&P −2.25% (7,414), Dow −0.98% (51,056), VIX +24% to 19.09.** Driver: hot May jobs (172k vs 88k) → **Fed-hike-by-year-end now priced**, 10y/30y yields up, growth/AI derating for a **second consecutive session**. Sector action: **money rotating OUT of semiconductors (AMD −8/−10%, MRVL −12%, MU −11%, INTC −9%, NVDA −4/−6%, AVGO −6%) INTO healthcare/financials.** The Dow (−0.98%) far outperforming the Nasdaq (−3.8%) confirms the value/defensive rotation. Net: **hostile to AI-semis longs, relatively favorable to healthcare/value (LLY).**
- **Crypto (live, levels ~5 h stale):** Regime **bearish trend (risk-off)**; BTC & ETH downtrend; altcoin breadth 27% > EMA20; BTC ATR percentile 91 (elevated vol). Macro risk 39/100, risk-off tilt mirrors the equity de-risking. Style: **short bias or no trade; avoid weak altcoin longs.** ZEC −39% on the counterfeiting-vulnerability exploit; the AI-token basket (NEAR/FET/TAO) is in a *downside* rotation (FET −18%/day, NEAR −24% headlines), not a bid. Deeply oversold → relief-bounce squeeze risk caps short-chasing.
- **Macro cross-asset:** strong jobs → hawkish Fed repricing is the through-line hitting **both** books (growth equities and crypto risk). Healthcare/defensives + financials are the only equity havens; in crypto there is no haven, only "less-short."

---

## 7. Candidate Deep Dives (5)

### 7.1 AMD — stocks A swing long (81.8, active/triggered) — **AVOID / MANUAL REVIEW (worst contradiction)**
- **Setup:** continuation LONG, swing entry ~479–495 / 501–516, SL ~449–472, TP1 ~540–564; also A invest long (79.3). `news_supported=0` — engine scored it technically, under the morning **bullish** regime.
- **Catalyst (verified, CONTRADICTS):** AMD **−8/−10% today**, second straight down session, inside the Broadcom-led chip rout (MRVL −12%, MU −11%, INTC −9%); hot jobs → rate-hike repricing piling on growth/AI. The stocks intraday report itself attaches "Nasdaq Futures Plunge … AMD −4%" to AMD and now scores AMD a **C short**, not a long.
- **Price-reaction / chase check:** price has reacted **hard to the downside** for two days; a long-continuation entry is catching a falling knife. No reclaim of the entry band — price is well below, not above, the trigger. **Entry now fights a confirmed downtrend + macro headwind.**
- **LEGAL/HEADLINE RISK:** none specific to AMD (sector/macro, not name-legal).
- **Verdict:** **AVOID / MANUAL REVIEW REQUIRED.** The stale A-tier long is the single most dangerous active exposure. Reconsider only on a decisive reclaim of 501–516 with the semis complex (SMH) stabilizing and VIX cooling.

### 7.2 LLY — stocks A swing/invest long (83.8 / 82.1) — **CONSTRUCTIVE HAVEN, WATCH (best long, not yet triggered)**
- **Setup:** continuation LONG, swing entry 1142.3–1160.7 (SL 1105.3, TP1 1216.1), invest entry 1123.3–1162.9 (TP1 1282.1). Catalyst-supported, `news_catalyst=10`.
- **Catalyst (verified, CONFIRMS):** TD Cowen raised the GLP-1 market to **$150B by 2030**, Buy / PT $1,250, LLY ~62% share (verified 18:30, still valid). Today's verified macro theme — **rotation INTO healthcare** — directly supports the thesis; LLY is *outside* the AI-semis derating.
- **Price-reaction / chase check:** LLY trades **~$1,135 — just BELOW the swing entry band (1142–1160)**, i.e. holding but **not triggered**. Buying below the band in a −3.8% Nasdaq tape is premature; the constructive read needs a **reclaim of 1142 that holds.** Not overextended, not a chase — simply not yet confirmed.
- **LEGAL/HEADLINE RISK:** none found (GLP-1 pricing/PBM coverage already digested; no indictment/SEC/auditor/guidance flags).
- **Verdict:** **WATCH — the cleanest long and the only one in a bid sector, but conditional.** Half-size long ONLY on a hold/reclaim above ~1142; do not buy the dip below the band into a broad risk-off close.

### 7.3 AAPL — stocks A swing long (83.8, active) — **AVOID / WATCH (caught in the tape)**
- **Setup:** continuation LONG, RS=leader, swing entry 311.7–314.4 (SL 306.3, TP1 322.6). `news_catalyst=10` but the only "catalyst" is the broad "US PREMARKET MOVERS … S&P futures down 0.5%" wire — a *bearish* macro note, not a bullish AAPL catalyst.
- **Catalyst (verified context, CONTRADICTS):** not chip-exposed in the Broadcom sense, but caught in a **−3.8% Nasdaq / "AI trade weakening"** session; megacap tech led the indices lower.
- **Price-reaction / chase check:** `waiting_for_entry`; a breakout-trigger long in a hard red tape has elevated failure odds. No positive idiosyncratic confirmation.
- **Verdict:** **AVOID for fresh entry / WATCH only** on a clean reclaim that holds after the dust settles. Lower priority than LLY; stale-regime A-long against a risk-off close.

### 7.4 SMCI — stocks short intraday B (67.1) / long swing-invest B (76–77) — **AVOID LONG (legal overhang); short messy**
- **Setup:** **direction conflict** — fresh intraday report ranks SMCI a **SHORT** (B 67.1, aligned with risk_off); the ~4 h swing/invest reports rank it a **LONG** (B 76.3 / 77.6, under the stale bullish regime).
- **LEGAL/HEADLINE RISK (verified, §I):** the standing material item is the **Mar 19 2026 indictment of three individuals associated with SMCI re: alleged export-control violation conspiracy** (SEC EDGAR / StockTitan). No *fresh* June-5 8-K confirmed — the report's "Form 8-K (FY2026), date unavailable" is a stale/generic EDGAR feed row, not a new catalyst. SMCI also carries a long history of accounting/auditor-resignation flags (prior reviews, memory).
- **Price-reaction / chase check:** chip-adjacent (AI-server) name in a −3.8% Nasdaq/chip-rout session — a long is fighting both the tape and the legal overhang; a short is direction-correct but late after a 2-day rout.
- **Verdict:** **AVOID the LONG (legal indictment + risk-off — never a clean actionable per §I). Short is direction-aligned but messy** (conflicting signals, already extended) → MANUAL REVIEW, no fresh chase.

### 7.5 META — stocks short intraday B (71.0, top fresh stock score) / crypto book proxy — **SHORT direction-aligned, CHASE risk → failed-bounce only**
- **Setup:** breakdown SHORT, entry 585.9–590.0, SL/inval 598.2, TP1 573.6 (rr_tp1 ~1.0). Highest-scoring fresh stock idea; communications is the weakest sector (RS −6.35%), aligned with risk_off.
- **Catalyst:** no META-specific catalyst; pure risk-off / weak-sector beta. Caught in the broad "AI-trade weakening" tape.
- **Price-reaction / chase check:** with Nasdaq −3.8% on the day, META has likely already moved a long way toward/through the short zone — **entering now risks chasing the flush.** Short only on a **failed bounce back into 585.9–590.0**, honoring the 598.2 invalidation; no late short after a vertical leg into the close.
- **Verdict:** **ACTIONABLE SHORT on a failed bounce, no-chase, honor invalidation** — the cleanest *direction-aligned* fresh stock idea, but timing-sensitive into the close.

**Crypto representation:** no crypto name clears a clean A/B this slot — the entire crypto book is **B-tier breakdown SHORTS** (TON 68, ETH, FET 67, NEAR/ADA/PUMP triggered) on ~5 h-stale levels. Direction (short) is correct and catalyst-aligned, but **re-pull fresh levels before executing**; treated as the crypto-book proxy rather than a separate deep dive given the staleness.

**Excess candidates (>5, deferred):** AMZN (stocks short B 68.4 — risk-off beta, no idiosyncratic catalyst); other stock C shorts (PLTR, NFLX, TSLA, MSTR, COIN); crypto B shorts (TON, NEAR, ADA, FET, ZRO) — same bearish-aligned thesis, no separate research; **ZEC** (crypto, exploit catalyst −39%) — watchlist only, no clean setup; LLY swing-long covered as 7.2.

---

## 8. Best Candidates Ranked

1. **LLY (stocks, A swing/invest long, 83.8/82.1)** — *WATCH → ACTIONABLE on a reclaim >1142.* Cleanest long: catalyst-confirmed + the one sector being bought today; but trades below its entry band, not yet triggered.
2. **META (stocks, B intraday short, 71.0)** — *ACTIONABLE short on a failed bounce.* Direction-aligned with the risk_off close; chase-risk → no late short.
3. **Crypto B shorts (TON 68 / ETH / FET 67 …)** — *Direction-aligned, re-pull stale levels.* Bearish regime + oversold relief-bounce risk; no-chase.
4. **AAPL (stocks, A swing long, 83.8)** — *AVOID/WATCH.* Stale-regime A-long caught in a −3.8% Nasdaq tape; no positive catalyst.
5. **AMD (stocks, A swing long, 81.8)** — *AVOID/MANUAL REVIEW.* Worst contradiction: −8/−10% on the day inside the chip rout; `news_supported=0`.

---

## 9. Avoid / No Trade

- **AMD / AAPL stale A-tier LONGS** — AVOID. Scored under the morning bullish regime that the live tape abandoned; AMD printed −8/−10% in a confirmed chip rout, AAPL caught in the −3.8% Nasdaq. Technical-only (`news_supported=0`).
- **SMCI LONG** — AVOID (per §I): standing **Mar 19 indictment / export-control** legal overhang + chip-adjacent name in a risk-off rout. Short is direction-aligned but messy (conflicting signals) → MANUAL REVIEW.
- **UNH long (stocks)** — **GATED / caution.** Prior DOJ Medicare-fraud-probe legal cluster (importance 0.73 ×3 today) not cleared → MANUAL REVIEW for any long. Carry-forward `TODO-unh-legal-gate`.
- **ZEC (crypto)** — exploit-driven −39% collapse; any long against it is INVALIDATED; short is late/extended. Watchlist only.
- **Crypto longs generally** — avoid; regime bearish, breadth 27%, "avoid weak altcoin longs."
- **Chasing META / crypto shorts into the flush** — no-chase; wait for failed bounces into entry zones.
- **Acting on ~5 h-stale crypto levels** — re-pull before any crypto execution.

---

## 10. Main Risks

- **Stale bullish swing/invest book vs flipped intraday regime (model risk, primary):** the engine simultaneously holds a *bullish* swing/invest regime (4 h old) and a *risk_off* intraday regime (fresh), and the A-tier LONGS ride the stale one. Acting on the A-longs buys a −3.8% day. Mitigation: this review gates AMD/AAPL/SMCI-long to AVOID; LLY conditional.
- **Friday close / weekend gap risk:** entering shorts (META, crypto) into the final hour risks an end-of-day mean-reversion bounce; crypto carries weekend-gap risk with no fresh levels. Mitigation: failed-bounce entries only, small size, honor invalidations.
- **Oversold relief-bounce (crypto):** BTC/ETH deeply oversold (ATR pct 91); a squeeze could stop breakdown shorts. Mitigation: no-chase.
- **LLY long into a broad red close:** even off-AI, a market-wide risk-off leg could drag LLY below 1142. Mitigation: require a reclaim/hold, half-size.
- **Crypto report staleness:** scalp/intraday levels ~5 h old (not regenerated in the 19:56 cycle) — entry/SL/TP numbers may be off. Mitigation: re-pull; direction-only until refreshed.
- **Catalyst layer weak (72.9% unmapped):** equity tickers mis-routed to `/USDT`; context-only this run.
- **Ingest:** if the source-ingest CLI fails, sources still live in §13 + the JSON artifact (no data loss).

---

## 11. Action Plan — next 4 hours (through the close + into the evening)

1. **LLY:** WATCH for a **reclaim and hold above ~1142** → half-size long, SL 1105, first target 1216. **Do not buy below the band** into a risk-off close. The one long in a bid sector.
2. **AMD / AAPL / NVDA:** **no long.** Stale A-tier longs are AVOID. Re-evaluate only after the semis complex (SMH) stabilizes, VIX cools back under ~17, and the name reclaims its entry band on volume.
3. **META:** short ONLY on a **failed bounce into 585.9–590.0**, SL 598.2, TP1 573.6 — **no late short** after a vertical leg into the close.
4. **SMCI:** no long (legal). Treat any short as MANUAL REVIEW; do not chase.
5. **Crypto (TON/ETH/FET/NEAR/ADA):** short bias intact — **re-pull fresh levels first** (reports ~5 h stale), then enter only on **failed bounces**, honor invalidations; **no chasing** the oversold flush. Respect BTC support; a reclaim of $62–63K neutralizes shorts.
6. **Weekend posture:** keep size small into the Friday close; avoid initiating new crypto exposure on stale levels over the weekend gap.
7. **Re-read the next fresh reports before acting** — scheduler is cycling; the crypto pipeline should regenerate levels shortly.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** **SHORT-BIASED, no-chase, levels stale.** Bearish regime persists; re-pull scalp levels (report ~5.1 h old) before any entry; oversold relief-bounce risk → small size. B-tier triggered winrate ~23% / PF 1.28 → small size.
- **Crypto intraday:** **SHORT-BIASED / selective, levels stale.** TON short (B 65.8) the best name; NEAR/ADA/PUMP triggered shorts aligned; no longs; re-pull levels, no-chase.
- **Crypto swing:** **NO-TRADE / caution.** Regime bearish; ZEC long INVALIDATED (−39% exploit); avoid weak altcoin longs.
- **Stocks intraday (fresh, risk_off):** **META = short on a failed bounce (best fresh idea, chase-risk); AMZN = risk-off-beta short, lower priority; SMCI/AMD/AAPL longs = AVOID; LLY = WATCH (>1142 reclaim).**
- **Stocks swing (carry-forward ~3.8 h, stale-bullish):** **LLY long bias intact but conditional on a 1142 reclaim; AMD/AAPL A-longs GATED by the confirmed risk-off/chip rout — do not action; SMCI/UNH excluded (legal).**
- **Stocks invest (carry-forward ~3.7 h):** **LLY long-term bias constructive (GLP-1 secular + healthcare rotation); AMD invest long structurally intact but de-prioritized while the AI-chip derating + rate-hike repricing plays out; SMCI/UNH excluded.**

---

## 13. Sources

**Late-session market / chip selloff / macro (CONFIRM the risk-off flip; CONTRADICT the AMD/AAPL longs):**
- [Stock market today: Dow, S&P 500, Nasdaq sink as jobs report fuels Fed hike bets, chip stocks sell off — Yahoo Finance, 2026-06-05 (WebFetch-verified: Nasdaq −3.80%/25,810, S&P −2.25%/7,414, Dow −0.98%/51,056, VIX +24%/19.09; AMD >−8%, NVDA >−4%)](https://finance.yahoo.com/markets/live/stock-market-today-dow-sp-500-nasdaq-sink-as-jobs-report-fuels-fed-hike-bets-chip-stocks-sell-off-230134285.html)
- [Nasdaq drops the most in more than a year as chips tumble; S&P 500's 9-week winning streak set to end — CNBC, 2026-06-05](https://www.cnbc.com/2026/06/04/stock-market-today-live-updates.html)
- [US Markets Decline Amid Chip Stock Selloff (MRVL −12%, MU −11%, INTC −9%, AMD −10%, AVGO −6%) — GuruFocus, 2026-06-05](https://www.gurufocus.com/news/8903336/us-markets-decline-amid-chip-stock-selloff)

**SMCI legal / 8-K status (LEGAL/HEADLINE RISK — gates the SMCI long):**
- [Super Micro Computer, Inc. — Form 8-K (FY2026), indictment of three individuals re alleged export-control violation conspiracy (filed Mar 19, 2026) — SEC EDGAR](https://www.sec.gov/Archives/edgar/data/0001375365/000137536526000011/a991.htm)
- [Super Micro Computer (SMCI) SEC Filings index — StockTitan](https://www.stocktitan.net/sec-filings/SMCI/)

_LLY GLP-1 catalyst (TD Cowen $150B by 2030, Buy / PT $1,250) was externally verified in the 18:39 prior review (TradingView/Stocktwits, Investing.com); not re-fetched this run — carried forward as still-valid context._

---

## 14. Fix Requests / TODO

### TODO-stocks-swing-invest-regime-staleness (new — primary this run)
- **issue:** the stocks **swing/invest** reports keep a *bullish* regime label and keep emitting **A-tier LONGS** (LLY/AAPL/AMD) for ~4 h after the **intraday** regime flipped to `risk_off` on the same day. The A-longs remain active signals against a confirmed −3.8% Nasdaq / chip rout. There is no cross-timeframe regime reconciliation, so the stalest regime can keep the highest-conviction (A-tier) longs live.
- **evidence:** stocks intraday report (21:34) = `risk_off`, top ideas META/AMZN/SMCI **short**; stocks swing (17:51) + invest (17:55) = `bullish`, A-tier AAPL/LLY/AMD **long**; `active-signals` stocks still lists A-tier LLY/AAPL/AMD longs; external AMD −8/−10% on the day.
- **suggested manual fix:** when the freshest intraday regime contradicts the swing/invest regime intraday, down-tier or flag the longer-horizon long signals (or force a swing/invest re-score on an intraday regime flip); surface the regime-age + cross-timeframe disagreement in `active-signals`.
- **priority:** high
- **first observed:** 2026-06-05 21:39 EEST

### TODO-regime-vs-catalyst-gate (carry-forward — now realized)
- **issue:** A-tier long signals inherit a +15 `market_regime_alignment` bonus from a 20-day "bullish" label even when the live catalyst is strongly bearish for the name/sector. AMD A-tier long (81.8, `news_supported=0`) printed **−8/−10% today** in the chip rout — the failure mode flagged at 18:30 is now realized, not hypothetical.
- **evidence:** AMD A swing 81.8 long `news_supported=0`; external AMD −8/−10%, MRVL −12%, MU −11% (Yahoo, GuruFocus); intraday report scores AMD a C **short**.
- **suggested manual fix:** add a catalyst/headline gate that demotes long signals when fresh high-importance bearish news for the symbol/sector exists (mirror the §I legal-gate); surface `news_supported` + a sector-derating penalty in the A-tier ranking.
- **priority:** high
- **first observed:** 2026-06-05 18:39 EEST (carry-forward)

### TODO-crypto-report-staleness (new)
- **issue:** the crypto **scalp** and **intraday** reports were **not regenerated in the latest (19:56) scheduler cycle** — they kept their 16:30 / 16:54 mtime (~5 h old) while the stocks intraday pipeline refreshed at 21:34. Crypto execution levels (entry/SL/TP) are stale even though the scheduler cycle completed.
- **evidence:** `cycle_02_19-56_summary.md` mtime 20:19; latest crypto scalp report `2026-06-05_13-30_scalp_report.md` mtime 16:30, intraday `13-54` mtime 16:54; stocks intraday `18-34` mtime 21:34.
- **suggested manual fix:** confirm whether the 19:56 cycle ran the crypto report generators (vs stocks-only); inspect `scheduler.log` for a crypto-mode skip/error; ensure each cycle regenerates all asset-class reports or logs the skip explicitly.
- **priority:** medium
- **first observed:** 2026-06-05 21:39 EEST

### TODO-untracked-legacy-alert (carry-forward)
- **issue:** still 1 untracked legacy crypto alert — `FET/USDT` B scalp short (65.7, sent 13:38) has no matching `proposed_signal`, so it won't contribute to PF/winrate/avgR. Unchanged from 18:30.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-06-05` → "1 untracked legacy crypto alert(s)"; `watchlist_alerts` FET/USDT 2026-06-05T13:38:48Z.
- **suggested manual fix:** investigate the PART-1 alert→signal registration path (per `AUDIT_NOTE_UNTRACKED_LEGACY_CRYPTO_ALERTS.md`); ensure every Telegram-sent alert writes a `proposed_signal` with a trackable `signal_id`.
- **priority:** medium
- **first observed:** 2026-06-05 18:39 EEST (carry-forward)

### TODO-unh-legal-gate (carry-forward)
- **issue:** UNH still emitted as a long signal without an enforced legal-risk gate for the DOJ Medicare-fraud probe (legal cluster importance 0.73 ×3 again today).
- **evidence:** swing report `| UNH | long | B | 71.79 |`; catalyst cycle legal-risk section lists 3 UNH DOJ-probe rows.
- **suggested manual fix:** implement a hard legal-risk gate (indictment/DOJ/SEC) that blocks or down-tiers affected long signals; re-verify UNH's current DOJ status.
- **priority:** medium
- **first observed:** 2026-06-05 04:30 EEST (carry-forward)

### TODO-catalyst-stock-usdt-mismap (carry-forward)
- **issue:** symbol resolver maps equity news to fake crypto `/USDT` pairs (UNH/USDT, JPM/USDT, TSLA/USDT) and leaves macro/equity headlines unmapped — 72.9% unmapped again this run.
- **evidence:** catalyst coverage 671 mapped / 1802 unmapped today; catalyst cycle shows UNH/USDT, JPM/USDT, TSLA/USDT rows.
- **suggested manual fix:** add an asset-class-aware resolver that routes equity tickers to the stocks namespace instead of fabricating `/USDT` pairs.
- **priority:** medium
- **first observed:** 2026-06-03 (carry-forward)
</content>
