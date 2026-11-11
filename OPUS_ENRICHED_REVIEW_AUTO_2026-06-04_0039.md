# Opus Enriched Review — Auto Cycle 00:39 EEST

- **Generated:** 2026-06-04 00:39 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`)
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-03_2042.md` (≈4 h ago — §4)
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). Every external claim cited in §13 with source + date + URL. CNBC WebFetch returned HTTP 403; StockTitan WebFetch verified the AVGO print independently.
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; all price/structure data is from local OHLCV/ATR/EMA report fields + cited external prints.
- **Clock:** 00:39 EEST Thursday. **US stock market is CLOSED** (regular session reopens ~16:30 EEST). Stock *intraday* signals below are NOT executable this cycle; crypto trades 24/7 and is the only actionable class right now.
- **Advisory only. No auto-trade.**

---

## 1. Executive Summary

- **The dominant event since the last review has resolved: AVGO reported after the US close and SOLD OFF HARD despite a record beat.** Q2 FY26 revenue **$22.19B (+48% YoY)**, AI-semi **$10.8B (+143% YoY)**, non-GAAP EPS **$2.44** (vs ~$2.40), and a very strong Q3 guide (**rev ~$29.4B / +84%**, **AI >$16B / +200%**). Yet the stock fell **−6.5% to −13.41% in extended trading (to ~$415)** — a textbook **"sell the news"** on elevated expectations / no raise to the $100B full-year AI target. **This is a NEGATIVE read-through for the whole semi complex (NVDA / AMD / SMH / SMCI / XLK) into the 2026-06-04 session.**
- **Posture shift vs the 20:42 pre-print review: from "wait, event-gated" to "negative semi catalyst now in — avoid fresh semi longs / manage risk at the open."** The active A-tier semi signals are now technically bullish (triggered) *against* a fresh bearish catalyst — that is the defining contradiction of this cycle.
- **Active A-tier signals (all stocks): SMH A 82.5 (triggered), AMD A 87.5 (triggered), NVDA A 80.6 swing (triggered); AAPL A 90 and SMCI A 82.3 already STOPPED.** All are `news_supported=0`. Per the A-tier reliability problem below, treat these as *attention flags, not green lights* — and now they carry AVGO gap-down risk.
- **Stocks A-tier remains a statistically losing bucket.** `signal-stats` (stocks) prints **tier=A: triggered, wins 1 / losses 7, PF 0.286, avgR −0.25, totalR −5.0 (n=27)** — net negative, while **tier=B is positive (PF 2.22, totalR +56)** and tier=C negative. A-tier underperforming B-tier is a persistent regression (TODO-stocks-atier-winrate, §14).
- **SMCI legal overhang still live and unresolved — AVOID.** No June development found: the **Mar 19 2026 SDNY indictment** of three SMCI-associated individuals (alleged ~$2.5B export-control scheme; one a board member who resigned Mar 20), **SEC/securities-fraud investigation**, and **class actions** all remain open with no clearing event. SMCI A-tier intraday already stopped; AVOID stands (TODO-smci-atier-legal).
- **Crypto stays bearish / risk-off; zero fresh A/B-quality setups.** BTC **~$66K**, **record $3.4B weekly ETF outflows** (largest ever; AUM **$104B → $94B**, 11 straight outflow days). Crypto regime: BTC/ETH downtrend, breadth **35.4% > EMA20**, BTC ATR percentile **96 (elevated)**. RS leaders (EPIC/WLD/ENA/MEME) are counter-tape with **very low volume (0.01–0.59×)** = momentum without confirmation → "do not chase." **Catalyst mapping weak this run (80.4% unmapped) — context only.** Crypto no-trade for fresh entries is correct.

---

## 2. Data Used

**Internal — fresh (<2.5 h):**
- `data/reports/scalp/2026-06-03_21-19_scalp_report.md` (gen 00:19 EEST, ~0.3 h). Regime: **bearish trend (risk-off)**.
- `data/reports/intraday/2026-06-03_21-36_intraday_report.md` (gen 00:36 EEST, ~0.05 h). Regime: **bearish trend (risk-off)**.
- `data/reports/stocks/intraday/2026-06-03_20-33_stocks_intraday_report.md` (mtime ~23:33 EEST, ~1.1 h; session = regular, now closed). Weekday.
- `data/catalysts/2026-06-03/` — `catalyst_events.jsonl` (3468 rows), `narrative_baskets.jsonl` (3 baskets), latest `catalyst_cycle_21-42.md`. (App keys catalysts by UTC date → live dir is `2026-06-03`; the `2026-06-04` dir does not yet exist. Ran the allowed `catalyst-scan --no-print` — events=500, baskets=3, rejected_test=0.)
- CLI / DB: `active-signals` (crypto 10 / stocks 50), `signal-stats` (crypto + stocks), `detect_untracked_legacy_alerts --since 2026-06-04` (**None**).
- LLM packets `data/processed/llm_analysis_packet.md` (00:37) / `llm_stocks_packet.md` (23:35) — reused as written context.

**Internal — carry-forward / stale (swing/invest):**
- `data/reports/stocks/swing/2026-06-03_13-11_stocks_swing_report.md` — ~8.5 h → **carry-forward (flagged)**.
- `data/reports/stocks/invest/2026-06-03_13-15_stocks_invest_report.md` — ~8.4 h → **carry-forward (flagged)**.
- `data/reports/swing/2026-06-03_01-20_swing_report.md` (crypto) — ~20.3 h → **STALE (>14 h)**. Excluded from fresh swing final-verdict; active ZEC/XLM swing *signals* used instead.

**External (this run — cited §13):** StockTitan (AVGO Q2 FY26 print + Q3 guide + after-hours −13.41%/−6.5%, WebFetch-verified); CNBC/PRNewswire search snippets (AVGO consensus + AI guide); Bitcoin.com News + CoinGlass + Coinfomania (BTC ~$66K, record $3.4B weekly ETF outflows, AUM $104B→$94B); SEC EDGAR + BusinessWire + Supermicro IR (SMCI Mar-2026 indictment / SEC probe / class action — no June update).

**Unavailable / blind:** live US equity prices (market closed — last-close + after-hours prints only); TradingView / Chrome chart verification (tool not loaded); liquidation heatmaps, order-book depth/CVD, ETF-flow live feed, on-chain whale flows, token-unlock calendar (manual/unconnected); live social beyond RSS-bridged `t.me/WalterBloomberg` + `t.me/lookonchain`.

---

## 3. Scheduler / Data Freshness

- **Scheduler: FRESH — review proceeds.** Latest run folder `data/scheduled_runs/2026-06-03_default_schedule/`. `scheduler.log` mtime **00:37 EEST (~0.04 h)**; latest `cycle_01_20-50_summary.md` mtime **21:56 EEST (~2.7 h)**. Defer rule requires BOTH > 3 h — not met (log is fresh).
- Crypto scalp / intraday: **fresh** (~0.05–0.3 h).
- Stocks intraday: **fresh** (~1.1 h) but **market closed** → not executable this cycle.
- Stocks swing / invest: **carry-forward** (≈8.4–8.5 h, 4–12 h band) — context only, excluded from fresh swing/invest final call.
- Crypto swing report: **STALE (≈20.3 h)** — excluded from swing final-verdict.

---

## 4. What Changed vs Previous Review (20:42 EEST)

- **AVGO earnings RESOLVED — the single biggest change.** The 20:42 review was *pre-print* ("no position into the print; it sets AI-semi direction"). The print is now in: **record beat + very strong Q3 guide, but the stock sold off −6.5% to −13.41% after hours (~$415)** on a "sell the news" reaction / no raise to the $100B AI target. **Net: a fresh NEGATIVE catalyst for the semi complex into 06-04** — the opposite of a green light.
- **US market is now CLOSED** (was mid-session at 20:42). Stock intraday signals are frozen at last close; the AVGO after-hours drop implies **gap-down risk at the 06-04 open** for semis.
- **A-tier roster shifted:** AAPL A 90 and SMCI A 82.3 have **STOPPED** since the prior run; SMH / AMD / NVDA(swing) remain **triggered**.
- **Crypto macro worsened/quantified:** BTC ETF outflows now confirmed at a **record $3.4B in a single week** (AUM **$104B → $94B**) vs the prior review's "~$2.8–3.5B over 10–11 days" framing. Tape unchanged: bearish/high-vol.
- **Catalyst mapping:** **80.4% unmapped** (vs 79.8% at 20:42) — still weak, recurring.
- **Confirmed / unchanged:** SMCI legal overhang (no clearing event); stocks A-tier losing bucket; NVDA A-vs-B tier conflict; universal stocks RR≈1.0 flaw; untracked-alert detector clean (None).
- **Thesis changed?** **Partially — yes.** Crypto no-trade is unchanged. **Stocks posture updates from "wait, event-gated into AVGO" to "AVGO printed and sold off — avoid fresh semi longs and respect gap-down risk at the open."**

---

## 5. Catalyst Coverage

- Total `catalyst_events` today (cumulative file): **3468**
- Mapped (non-null symbol): **680**
- Unmapped (null symbol): **2788** → **80.4% unmapped**
- `narrative_baskets`: **3** — `perps_dex_narrative` (primary HYPE/USDT; DYDX/GMX/ASTER), `binance_ecosystem_teaser` (primary BNB; ASTER), `momentum_breakout` (primary MEME/USDT +17%, vol 0.59× — no confirmed news).
- **⚠️ catalyst mapping weak this run (80.4% unmapped) — use the catalyst layer as context, not a final decision.** Persistent pattern (79.8% at 20:42, 80.4% now) → TODO-catalyst-mapping (§14).
- Top 3 unmapped (by importance) — all sector-level / non-symbol headlines (expected to be unmapped):
  1. *"DeFi won't win over big banks until it fixes its hacking problem, executives say"* — exploit_hack sector theme.
  2. *"69-year-old furniture store chain files for Chapter 11 bankruptcy"* (Yahoo Finance) — generic legal_risk headline (not a tracked symbol).
  3. *"Trezor Reveals Hardware Wallet Vulnerability, But Funds 'Safe'"* (Decrypt) — sector security theme.

---

## 6. Market Landscape

- **Crypto — bearish / risk-off.** BTC downtrend, ETH downtrend, altcoin breadth **35.4% > EMA20**, BTC ATR percentile **96 (elevated)**. Recommended style per the desk: **short bias or no trade; avoid weak altcoin longs.** Externally: **BTC ~$66K**, **record $3.4B weekly spot-ETF outflows** (largest ever; AUM **$104B → $94B**; 11 straight outflow days), driven by rising Treasury yields / shifting Fed expectations / profit-taking. RS leaders (EPIC +24–26%, WLD +30%, ENA +16–20%, MEME +14–17%) are bouncing *against* the tape on **very thin volume (0.01–0.59×)** → momentum without volume confirmation, "do not chase." Weakest: JST/GPS/PORTAL/BCH/HOME (−12% to −20%).
- **Stocks — bullish-trend regime but freshly event-shocked.** The underlying stocks intraday report regime is bullish (semis/tech leadership), BUT **AVGO's after-hours sell-off is a fresh negative catalyst the report pre-dates.** The semi complex (SMH/AMD/NVDA/SMCI/XLK) now faces gap-down risk at the 06-04 open. Structural flaw persists: nearly every stock idea shows **RR-to-TP1 ≈ 1.0** (below the 1.5 floor; TODO-stocks-rr).
- **Crypto–equity divergence persists**, and equities just lost their strongest single-name AI-semi proof point to a "sell the news."

---

## 7. Candidate Deep Dives (≤5)

### Candidate 1 — AVGO (stocks) — earnings PRINTED → "sell the news" (sets the semi tape)
- **External (verified this run):** Q2 FY26 **rev $22.187B (+48% YoY)**, **AI-semi $10.8B (+143% YoY)**, **GAAP EPS $1.91 / non-GAAP $2.44**. Q3 guide **rev ~$29.4B (+84% YoY)**, **AI >$16B (+200% YoY)**. Despite the record beat + guide, the stock **fell −6.5% to −13.41% in extended trading (to ~$415)**; CEO Hock Tan **did not raise** the $100B full-year AI target.
- **Internal:** The engine had AVGO swing-blocked with a −24 earnings penalty and an "earnings today (unknown)" label going into the print (TODO-avgo-earnings-unknown) — so no position was carried in. Correct.
- **Legal/headline risk:** None.
- **Price-reaction / chase check:** The catalyst has fully fired and reversed — **price already reacted hard to the downside.** Any AVGO long here would be catching a post-earnings knife; any short is chasing a gap. **Late either way without a 06-04 session structure to read.**
- **Verdict:** **NO TRADE on AVGO directly. Treat the after-hours drop as a NEGATIVE read-through for NVDA/AMD/SMH/SMCI/XLK at the 06-04 open.**

### Candidate 2 — AMD (stocks) — A 87.5 intraday (`triggered`) — now into AVGO downdraft
- **Internal:** Highest-scored active A-tier (87.5), intraday long, `triggered`. Entry **534.05** (zone 529.74–534.05), invalidation **521.11**, TP1 **546.99** (RR≈1.0). `news_supported=0`.
- **External:** AMD opened +3.41% on Jun 3 with a recent Strong-Buy/upgrade narrative (AI-inference demand) — but that pre-dates AVGO's after-hours sell-off, which now caps near-term semi upside.
- **Legal/headline risk:** None.
- **Price-reaction / chase check:** Signal `triggered` at last close; **manual/live chart unavailable (market closed).** With AVGO −6.5/−13% after hours, AMD carries **gap-down risk at the open** — entering at the triggered level risks buying directly into a negative semi read-through. RR is only 1.0.
- **Verdict:** **NO fresh add. Manual review at the open.** If AMD gaps down and *reclaims* the entry zone on its own strength, only then re-assess — reduced size, accept the 1.0 RR knowingly. Do not buy the frozen triggered level blind into AVGO's downdraft.

### Candidate 3 — SMH (stocks) — A 82.5 intraday (`triggered`) — semis ETF, most exposed to AVGO
- **Internal:** A 82.5, intraday long, `triggered`. Entry **633.44** (zone 630.26–633.44), invalidation **623.91**, TP1 **642.97** (RR≈1.0). `news_supported=0`. ETF → no single-name earnings, but **AVGO is a top SMH constituent.**
- **External:** SMH is a direct proxy for the AI-semi tape; AVGO's "sell the news" is the dominant near-term driver.
- **Legal/headline risk:** None.
- **Price-reaction / chase check:** `triggered` at last close; **live chart unavailable (closed).** Buying the semi ETF directly into its largest constituent's post-earnings sell-off is poor timing → **gap-down risk at the open.**
- **Verdict:** **WAIT / no fresh add.** Re-evaluate the semi complex after the 06-04 open absorbs the AVGO reaction.

### Candidate 4 — NVDA (stocks) — A 80.6 swing (`triggered`) — held into the semi shock
- **Internal:** A 80.6, **swing** long, `triggered`. Entry **222.82** (zone 218.65–222.82), invalidation **210.31**, TP1 **235.33** (RR≈1.0), expires 06-10. `news_supported=0`. Note the recurring **A-vs-B tier conflict**: the engine's own re-scores show NVDA ~B 69 for the same name/mode (TODO-nvda-tier-conflict).
- **External:** Constructive AI-infrastructure narrative on Jun 3, but AVGO's "guide wasn't enough" reaction signals the market is now punishing even strong AI-semi prints — a caution for NVDA's own setup.
- **Legal/headline risk:** None.
- **Price-reaction / chase check:** Swing horizon, so less open-gap sensitive than intraday, but the entry sits into a freshly negative semi tape. Overextension vs EMA20 not verifiable (chart tool unavailable).
- **Verdict:** **HOLD existing against the 210.31 invalidation; NO fresh add into the AVGO downdraft.** Manage as a swing; do not increase exposure.

### Candidate 5 — SMCI (stocks) — A 82.3 intraday (`stopped`) — LEGAL/HEADLINE RISK
- **Internal:** A 82.3 intraday long, **already `stopped`** this cycle. Still surfaces as B-tier in swing/invest active signals.
- **External — LEGAL/HEADLINE RISK (verified, no June change):** **SDNY indictment Mar 19 2026** of three SMCI-associated individuals over an alleged **~$2.5B export-control scheme** (servers/GPUs diverted to China); one (Wally Liaw, board member) **resigned Mar 20**; company placed two on leave, terminated the contractor; company **not named as a defendant**. **SEC / securities-fraud investigation** and **shareholder class actions** announced (Frank R. Cruz et al.). **No clearing event** found in June 2026; latest filings are routine 8-K / 10-Q.
- **Price-reaction / chase check:** Already stopped; moot for entry.
- **Verdict:** **AVOID.** Live indictment + SEC probe + class-action overhang, unresolved. The scoring engine keeps surfacing SMCI without a legal gate (TODO-smci-atier-legal).

**Excess candidates (noted, not deep-dived — §F A-tier cap reached):**
- **AAPL (stocks)** — A 90 intraday, **STOPPED** this cycle. Telegram (WalterBloomberg) carried UBS "WWDC26 unlikely to boost Apple shares" — mild negative; moot now that it's stopped.
- **Crypto (ZEC / ENA / ZRO / SAHARA)** — no fresh A/B-quality setups; all counter-tape. **ZEC** swing is `tp2_hit` (entry 567, already played out) with a real but **resolved** catalyst (NU6.2 mainnet upgrade; deposits/withdrawals paused; the critical Orchard bug was fixed via emergency upgrade, funds safe) → already extended, **watchlist/hold-runner, not a chase**. **SAHARA** scalp short 67.8 is the only short, aligned with the bearish tape but thin. **ENA/ZRO** B-longs are counter-tape RS leaders on low volume → reduced-size/no-chase only.

---

## 8. Best Candidates Ranked

> **No clean fresh actionable this cycle.** The A-tier stock signals are technically triggered but sit into a fresh negative AVGO catalyst, are from a statistically losing A-tier bucket, carry RR≈1.0, and are *not executable now* (market closed). Crypto has no fresh A/B-quality setup.

1. **NVDA (stocks, swing)** — only *hold-management* idea: hold existing against 210.31, no fresh add. Highest "do something" rank only because the swing horizon survives an open-gap.
2. **AMD / SMH (stocks, intraday)** — **WAIT for the 06-04 open** to absorb AVGO; no blind entry at frozen triggered levels.
3. **SAHARA (crypto, scalp short 67.8)** — the only setup *aligned* with the prevailing tape, but thin/low-conviction; reduced size if discipline allows.
4. *(crypto longs)* **No clean fresh candidate** — RS leaders counter-tape on thin volume; hold existing ZEC/XLM runners only.
5. **SMCI / AVGO** — AVOID / NO TRADE.

---

## 9. Avoid / No Trade

- **SMCI — AVOID.** Live SDNY indictment + SEC probe + class-action overhang; no clearing event. (§7 Candidate 5)
- **AVGO — NO TRADE.** Post-earnings drop already fired; no session structure to read while market is closed.
- **AMD / SMH / NVDA — no fresh semi exposure into the AVGO downdraft.** Hold existing (NVDA swing) only; respect gap-down risk at the open.
- **Crypto fresh longs — NO TRADE.** Bearish/high-vol tape; RS leaders extended on thin volume → "do not chase" (EPIC/WLD/ENA/MEME).
- **Chasing the A-tier triggered levels blind** while the market is closed and a negative catalyst is fresh.

---

## 10. Main Risks

- **Semi gap-down at the 06-04 open** — AVGO's −6.5/−13% after-hours "sell the news" can drag NVDA/AMD/SMH/SMCI/XLK lower at the open despite their triggered status; the active A-tier signals do not reflect this fresh catalyst.
- **BTC structure fragile** — ~$66K with **record $3.4B weekly ETF outflows** + AUM $104B→$94B + 11-day outflow streak = ongoing forced-seller risk; any crypto long is counter-trend. A clean loss of the $65K area opens $60K.
- **Stocks A-tier bucket is net-losing** — PF 0.286 / totalR −5.0 (n=27) this week, worse than B-tier; do not treat A-tier scores as conviction (TODO-stocks-atier-winrate).
- **Stocks RR structurally capped** — nearly every idea is RR-to-TP1 ≈ 1.0, below the 1.5 floor (TODO-stocks-rr).
- **Catalyst mapping weak (80.4% unmapped)** — symbol-level catalyst signal thin; context only.
- **Market-closed blindness** — no live equity prices, no chart tool; stock verdicts are framed as "manual review at the open," not executable calls.
- **Source ingest** (§12) attempted; if it fails it does not affect the verdicts above (advisory only).

---

## 11. Action Plan — next 4 hours

1. **Crypto (only tradeable class now):** No fresh longs. Hold ZEC (swing, tp2_hit) / XLM runners against their stops. Watch **BTC $65K** — a clean loss = de-risk all crypto longs immediately. SAHARA scalp short (67.8) is the only tape-aligned idea — reduced size only, thin.
2. **Stocks (market closed until ~16:30 EEST):** No action executable. **Do NOT pre-stage entries at the frozen A-tier triggered levels** — AVGO's after-hours drop changes the open.
3. **NVDA swing:** Hold existing against **210.31**; no add. Manage as a swing through the semi shock.
4. **At the 06-04 open:** Read how SMH/AMD/NVDA absorb the AVGO reaction *before* any semi entry. A gap-down that reclaims is different from a gap-down that bleeds — wait for structure.
5. **Avoid:** SMCI (legal), fresh semi longs into the downdraft, any extended crypto RS-leader chase, blind execution of frozen triggered levels.
6. **Next cycle:** Re-evaluate the semi complex with the 06-04 session in hand; re-check BTC $65K and ETF-flow follow-through.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** **NO TRADE (fresh longs).** Bearish/high-vol. Only tape-aligned idea is SAHARA short (67.8) — reduced size, low conviction. Do not chase RS leaders.
- **Crypto intraday:** **NO TRADE (fresh).** RS leaders (EPIC/WLD/ENA) counter-tape on thin volume; reduced size only if discipline demands.
- **Crypto swing:** **HOLD runners only** (ZEC tp2_hit, XLM). Swing report stale (≈20 h) — no fresh swing call.
- **Stocks intraday:** **NO FRESH TRADE / MANUAL REVIEW AT THE OPEN.** Market closed; A-tier triggered levels sit into AVGO's negative read-through. AVOID SMCI.
- **Stocks swing:** **HOLD / CAUTION.** Hold NVDA swing against 210.31; no fresh add into the semi shock; carry-forward swing data (≈8.5 h). SMCI excluded (legal).
- **Stocks invest:** **CAUTION (carry-forward data).** Long bias intact; SMCI invest signals excluded on legal grounds.

---

## 13. Sources

- [Broadcom Inc. Announces Second Quarter Fiscal Year 2026 Financial Results — StockTitan, 2026-06-03 (WebFetch-verified: rev $22.19B/+48%, AI $10.8B/+143%, non-GAAP EPS $2.44, Q3 guide ~$29.4B/AI >$16B, after-hours −13.41%/−6.5% to ~$415)](https://www.stocktitan.net/news/AVGO/broadcom-inc-announces-second-quarter-fiscal-year-2026-financial-if4yrbje8hq6.html)
- [Broadcom (AVGO) earnings report Q2 2026 — CNBC, 2026-06-03 (search snippet; direct WebFetch returned HTTP 403)](https://www.cnbc.com/2026/06/03/broadcom-avgo-earnings-report-q2-2026.html)
- [Broadcom Inc. Announces Q2 FY2026 Financial Results and Quarterly Dividend — PR Newswire, 2026-06-03](https://www.prnewswire.com/news-releases/broadcom-inc-announces-second-quarter-fiscal-year-2026-financial-results-and-quarterly-dividend-302790698.html)
- [Bitcoin Falls to $65,710 as Record ETF Outflows and Strategy Sale Rattle Market — Bitcoin.com News, 2026-06-03](https://news.bitcoin.com/bitcoin-falls-under-66000-etf-outflows-strategy-sale/)
- [Bitcoin ETFs Record Largest-Ever $3.4B Sell-Off — Coinfomania, 2026-06 (record weekly outflow; AUM $104B→$94B)](https://coinfomania.com/bitcoin-etf-outflows-june-2026-record-selloff/)
- [Spot BTC Net Inflow & Holdings — CoinGlass ETF dashboard (live, date unavailable)](https://www.coinglass.com/etf/bitcoin)
- [Super Micro Computer Issues Statement on Action by U.S. Attorney's Office — Supermicro IR / SEC Form 8-K FY2026, 2026-03-20](https://ir.supermicro.com/news/news-details/2026/Super-Micro-Computer-Issues-Statement-on-Action-by-U-S--Attorneys-Office/default.aspx)
- [Securities Fraud Investigation Into Super Micro Computer, Inc. (SMCI) Announced — BusinessWire (Law Offices of Frank R. Cruz), 2026-03-20](https://www.businesswire.com/news/home/20260320952669/en/Securities-Fraud-Investigation-Into-Super-Micro-Computer-Inc.-SMCI-Announced-Shareholders-Who-Lost-Money-Urged-To-Contact-The-Law-Offices-of-Frank-R.-Cruz)

_No fabricated dates: where a publish date was unavailable (CoinGlass live dashboard) it is labelled "date unavailable," not invented. SMCI facts are March-2026 events re-verified this run with no June change found. The CNBC direct WebFetch returned HTTP 403; the AVGO print was independently WebFetch-verified via StockTitan. No fixture/test_source URLs cited._

---

## 14. Fix Requests / TODO

### TODO-stocks-atier-winrate
- **issue:** Stocks A-tier bucket is net-losing and underperforms B-tier — triggered wins 1 / losses 7, PF 0.286, avgR −0.25, totalR −5.0 (n=27); tier=B is positive (PF 2.22, totalR +56), tier=C negative.
- **evidence:** `signal-stats --asset-class stocks` By-tier table: tier=A trig 20 / wins 1 / losses 7 / PF 0.2857 / avgR −0.25 / totalR −5.0.
- **suggested manual fix:** Review A-tier promotion thresholds / entry geometry for stocks; consider demoting borderline A's or gating A-tier on RR until the bucket stabilizes.
- **priority:** high
- **first observed:** recurring; re-confirmed 2026-06-04 00:39 EEST.

### TODO-smci-atier-legal
- **issue:** SMCI keeps surfacing as a high-tier signal (A 82 intraday this cycle; B in swing/invest) with no legal-risk gate despite a live SDNY indictment + SEC probe + securities class action.
- **evidence:** `active-signals --asset-class stocks` (SMCI A intraday stopped, B swing/invest); external: SDNY indictment Mar 19 2026, board member resigned, SEC/class-action investigations open, no clearing event.
- **suggested manual fix:** Add a legal/headline-risk gate (indictment / DOJ / SEC / class-action flag) that caps or rejects affected symbols in the stocks scoring engine.
- **priority:** high
- **first observed:** carried from prior runs; re-confirmed 2026-06-04 00:39 EEST.

### TODO-catalyst-mapping
- **issue:** Catalyst symbol-mapping weak again — 80.4% of 3468 events unmapped (79.8% at 20:42).
- **evidence:** computed from `data/catalysts/2026-06-03/catalyst_events.jsonl` (mapped 680 / unmapped 2788).
- **suggested manual fix:** Improve the symbol resolver in the catalyst layer (ticker/entity extraction, alias table) to lift mapped share above 50%.
- **priority:** medium
- **first observed:** recurring; re-confirmed 2026-06-04 00:39 EEST.

### TODO-stocks-rr
- **issue:** Nearly every stocks idea reports RR-to-TP1 ≈ 1.0, below the stated 1.5 floor, yet still scores A/B-tier — reward geometry is structurally weak.
- **evidence:** active A-tier signals SMH/AMD/NVDA all carry `expected_rr_tp1 = 1.0` in `proposed_signals`.
- **suggested manual fix:** Audit TP1 placement / ATR multiple in stocks target generation so passing setups carry ≥1.5 RR, or down-weight low-RR setups harder.
- **priority:** medium
- **first observed:** recurring; re-confirmed 2026-06-04 00:39 EEST.

### TODO-nvda-tier-conflict
- **issue:** NVDA open swing signal is A 80.6 but the engine's own re-scores show B ~69 for the same symbol/mode — a one-tier downgrade the live signal never absorbs.
- **evidence:** `active-signals --asset-class stocks` shows NVDA swing A 80 (triggered) alongside NVDA swing B ~69 rows.
- **suggested manual fix:** When a re-score downgrades tier, propagate the downgrade (or close+reopen) so active signals reflect the current tier.
- **priority:** medium
- **first observed:** carried from prior runs; re-confirmed 2026-06-04 00:39 EEST.

### TODO-avgo-earnings-unknown
- **issue:** Going into the print, AVGO earnings status showed "today (unknown)" in the stocks report even though the date/time was externally confirmed (Wed Jun 3, after close). The print has now resolved, but the calendar-resolution gap remains for the next event.
- **evidence:** prior stocks report §3 "AVGO: earnings today (unknown)"; broad earnings lookup failures for index ETFs.
- **suggested manual fix:** Audit the earnings-calendar source (yfinance fallback) so confirmed near-dated earnings resolve to a known time instead of "unknown."
- **priority:** medium
- **first observed:** recurring (earnings UNKNOWN pattern); re-confirmed 2026-06-04 00:39 EEST.

### TODO-expired-waiting-signals
- **issue:** Several crypto signals remain `waiting_for_entry` with `expires_at` possibly already in the past (scalp rows persisted from earlier cycles).
- **evidence:** `active-signals --asset-class crypto` shows waiting rows (ENA/ZRO/etc.) carried across cycles; prior runs flagged past `expires_at`.
- **suggested manual fix:** Add an expiry sweep that transitions past-`expires_at` `waiting_for_entry` signals to `expired` so the active list reflects reality.
- **priority:** low
- **first observed:** carried from prior runs; re-confirmed 2026-06-04 00:39 EEST.
