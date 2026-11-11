# Opus Enriched Review — Auto Cycle 20:32 EEST

- **Generated:** 2026-06-03 20:32 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`)
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-03_1445.md` (≈5 h 47 m ago)
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). Every external claim cited in §13 with source + date + URL.
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; all price/structure data is from local OHLCV/ATR/EMA report fields.
- **Advisory only. No auto-trade.**

---

## 1. Executive Summary

- **SMCI legal overhang is still live and unresolved — AVOID (canonical regression).** The system feeds SMCI as **B-tier "triggered" across swing (72.5) and invest (67.8/65.2)**. Externally re-verified this run: the **March 19, 2026 SDNY indictment** of three SMCI-associated individuals (incl. a board member) over an alleged **~$2.5B export-control scheme** diverting AI servers to China; the stock collapsed **33.3% to $20.53** on Mar 20; securities class-action lead-plaintiff deadline **May 26, 2026 (now passed)**. The only fresh SMCI item is a **routine Form 8-K (FY2026)** — no legal resolution. **SMCI → AVOID** (TODO-smci-atier-legal, §14).
- **Stocks A-tier remains a statistically untrustworthy bucket.** `signal-stats` (stocks) prints **tier=A triggered winrate 5%, profit factor 0.29 (n=28)** — below the 0.8 floor. The lone A-tier name today (**NVDA swing A 80.6, triggered**) inherits that skepticism. Treat A-tier as an *attention flag, not a green light* (TODO-stocks-atier-winrate, §14).
- **NVDA carries the same tier-conflict as prior runs.** The active swing signal is **A-tier 80.6 (triggered)**, but the system's own swing re-scores show NVDA at **B-tier 69.6** — a one-tier downgrade the open A-tier signal never absorbed. Not a clean A-tier long; B-quality at best, in an **extended AI-semi tape into AVGO's earnings tonight** (TODO-nvda-tier-conflict, §14).
- **AMD is the freshest high-conviction stock name (B 76.0, "high" confidence, intraday `waiting_for_entry`).** Leader RS (**+45.7% vs SPY 20d**), bullish regime, no earnings. But it shares the universal stocks flaw — **RR-to-TP1 of only 1.0** (below the 1.5 floor) — and sits directly in front of the **AVGO AI-semi print tonight**. Pullback-into-zone (529.12–533.13) only; not a chase, and event risk is high.
- **AVGO reports earnings TONIGHT (Wed Jun 3, after US close).** Externally confirmed: consensus EPS **~$2.40**, rev **~$22B (+47% YoY)**, AI-semi guide **~$10.7B (~+140% YoY)**. System has it **C/B-tier with a −24 earnings penalty / swing-blocked**, and the stocks report still labels earnings status **"unknown."** **No fresh AVGO position into the print.** It sets AI-semi direction for NVDA / AMD / SMH / SMCI tomorrow.
- **GOOGL has a genuine contradiction (short signal vs bullish regime + a verified $84.75B equity raise).** Alphabet priced an **$84.75B equity capital raise on Jun 2** (upsized from $80B) to fund AI compute — a real dilution overhang. The system carries **GOOGL short C 58.3 (triggered, intraday)** but *rejects* it as `short_in_bullish_regime, rr_below_1.5`. Net: **no clean trade — manual review.**
- **Crypto remains in a high-volatility bearish tape; zero fresh A/B setups** across scalp and intraday — every idea is C-tier watchlist. **BTC ~$65.7–66K** (externally confirmed), support **$65K → $60K**, **~$3.5B ETF outflows over 10–11 days**, **$1.8B liquidations**, Strategy selling. **ZEC's emergency Orchard fix is verified resolved (no exploit, funds safe)** but already +10% and counter-tape — watchlist, not a chase. **Catalyst mapping weak this run (79.8% unmapped) — context only.** Desk no-trade for fresh crypto entries is correct.

---

## 2. Data Used

**Internal — fresh (<2.5 h):**
- `data/reports/scalp/2026-06-03_15-41_scalp_report.md` (mtime 18:41 EEST, ~1 h 51 m). Regime: **bearish trend (risk-off)**.
- `data/reports/intraday/2026-06-03_16-04_intraday_report.md` (mtime 19:04 EEST, ~1 h 28 m).
- `data/reports/stocks/intraday/2026-06-03_17-16_stocks_intraday_report.md` (mtime 20:16 EEST, ~16 m; session = regular). Weekday.
- `data/catalysts/2026-06-03/` — `catalyst_events.jsonl` (**1968 events**), `narrative_baskets.jsonl` (**5 baskets**), latest `catalyst_cycle_16-05.md`.
- CLI / DB: `active-signals` (crypto 9 rows / stocks ~39 rows), `signal-stats` (crypto + stocks), `detect_untracked_legacy_alerts --since 2026-06-03` (**None**), direct `news_items` queries (DB `db/crypto_ai_desk.sqlite`) on NVDA / AMD / SMCI / GOOGL / ZEC.

**Internal — carry-forward / stale (swing/invest):**
- `data/reports/swing/2026-06-03_01-20_swing_report.md` — mtime 04:20 EEST, **≈16 h old → STALE (>14 h)**. Excluded from fresh swing final-verdict; context only.
- `data/reports/stocks/swing/2026-06-03_13-11_stocks_swing_report.md` — mtime 16:11 EEST, **≈4 h 21 m → carry-forward (flagged)**.
- `data/reports/stocks/invest/2026-06-03_13-15_stocks_invest_report.md` — mtime 16:15 EEST, **≈4 h 17 m → carry-forward (flagged)**.
- LLM packets `data/processed/llm_analysis_packet.md` / `llm_stocks_packet.md` (reused as written context).

**External (this run — cited §13):** Bitcoin.com / Blockhead (BTC ~$65.7–66K, $65K/$60K support, ETF outflows, liquidations, Strategy sale); CryptoTimes (WebFetch-verified ZEC NU6.2 hard-fork resolution) + Decrypt/Yahoo (ZEC surge); Alphabet IR (GOOGL $84.75B raise); Seeking Alpha (AVGO earnings tonight + consensus); Super Micro IR (SMCI indictment / class action).

**Unavailable / blind:** TradingView / Chrome chart verification (tool not loaded); live social attention beyond RSS-bridged `t.me/WalterBloomberg` + `t.me/lookonchain`; liquidation heatmaps, order-book depth/CVD, ETF-flow feed, on-chain whale flows, token-unlock calendar (manual/unconnected).

---

## 3. Scheduler / Data Freshness

- **Scheduler: FRESH — review proceeds.** Latest run folder `data/scheduled_runs/2026-06-03_default_schedule/`. `scheduler.log` mtime **19:18 EEST (~1 h 14 m)**; latest `cycle_02_18-16_summary.md` mtime **19:18 EEST (~1 h 14 m)**. Defer rule requires BOTH > 3 h — not met.
- Scalp / intraday (crypto + stocks): **fresh** (~16 m – 1 h 51 m).
- Stocks swing / invest: **carry-forward** (≈4.2–4.3 h, within 4–12 h band) — used for context, flagged, excluded from fresh swing/invest final call.
- Crypto swing report: **STALE (≈16 h)** — excluded from swing final-verdict; the active ZEC/XLM swing *signals* (from `active-signals`) are used instead.

---

## 4. What Changed vs Previous Review (14:45 EEST)

- **New regime context:** Crypto regime label held at **bearish trend (risk-off)**; BTC has slid further from the 14:45 ~$67K read toward **~$65.7–66K**, with $65K the immediate line and $60K below it. ETF-outflow streak extended to **~$3.5B over 10–11 days** (was being tracked at record pace last run).
- **New verified catalyst:** **ZEC Orchard / NU6.2** is now fully resolved (hard fork activated Jun 3 00:05 EDT, no exploitation, supply intact) — last run this was nascent. ZEC ~$629, +10%/24h; active swing signal at **tp2_hit**.
- **New stock catalyst:** **GOOGL's $84.75B equity raise** priced Jun 2 (upsized from $80B) — added as a candidate this run (dilution overhang vs bullish regime).
- **Confirmed / unchanged:** SMCI legal overhang (no clearing event); stocks A-tier untrustworthy bucket; NVDA A-vs-B tier conflict; AVGO earnings tonight + swing-block. AAPL still the cleanest stock long but RR-capped.
- **Removed:** TSLA-SpaceX merger headline is no longer a top-5 driver (narrative, 2027 horizon) — demoted to watchlist context.
- **Thesis changed?** No — the desk posture (crypto no-trade; stocks long-biased but RR-capped and event-gated into AVGO) is **unchanged and re-confirmed**.

---

## 5. Catalyst Coverage

- Total `catalyst_events` today: **1968**
- Mapped (non-null symbol): **397**
- Unmapped (null symbol): **1571** → **79.8% unmapped**
- `narrative_baskets`: **5** (ai_narrative, rwa_narrative, perps_dex_narrative, momentum_breakout + 1)
- **⚠️ catalyst mapping weak this run (79.8% unmapped) — use the catalyst layer as context, not a final decision.** This is a persistent pattern (80.4% last run) → TODO-catalyst-mapping (§14).
- Top 3 unmapped (by importance), all sector-level / non-symbol headlines (expected to be unmapped):
  1. *"DeFi won't win over big banks until it fixes its hacking problem, executives say"* (CoinDesk) — exploit_hack sector theme.
  2. *"Trezor Reveals Hardware Wallet Vulnerability, But Funds 'Safe'"* — sector security theme.
  3. *"DOJ, CFTC probe George Santos over Kalshi trades tied to State of the Union appearance"* — regulatory headline.

---

## 6. Market Landscape

- **Crypto — bearish / risk-off.** BTC downtrend, ETH downtrend, altcoin breadth **40% > EMA20**, BTC ATR percentile **98 (elevated volatility)**. Recommended style: short bias or no trade; avoid weak altcoin longs. Externally: **BTC ~$65.7–66K**, support **$65K → $60K**, **~$3.5B ETF outflows (10–11 days)**, **$1.8B liquidations (largest since Feb)**, Strategy selling. RS leaders (XPL, GPS, NEAR, ZRO, ONDO, ZEC, WLD) are bouncing *against* a weak tape — counter-trend, capped, mostly extended (>2 ATR from EMA20 → "do not chase").
- **Stocks — bullish / risk-on.** Regime **bullish**, VIX **16.31**, breadth **100% > EMA20/50**, all 4 indices uptrending. Leadership: **semiconductors (SMH RS +17.2%)** and **technology (XLK RS +13.8%)**. Laggards: utilities, communications, staples. **The whole semi complex is event-gated into AVGO's print tonight.** Persistent structural flaw: nearly every stock idea shows **RR-to-TP1 ≈ 1.0** (below the 1.5 floor).
- **Crypto–equity divergence persists** — equities firm/at-highs while BTC slides.

---

## 7. Candidate Deep Dives (≤5)

### Candidate 1 — NVDA (stocks) — swing A 80.6 (triggered) → treat as B-quality, event-gated
- **Internal:** Active swing signal A 80.6 triggered (expires Jun 10); system swing re-scores show NVDA at B 69.6 — **unabsorbed one-tier downgrade**. Invest C 64.6. News (internal, fresh): Jensen Huang "AI job losses complete nonsense"; "underrated AI infra stock" pieces; Cramer Amazon-AI-chip-threat angle.
- **External:** No adverse catalyst; AI-semi sentiment constructive but the sector is **extended into AVGO tonight**.
- **Legal/headline risk:** None.
- **Price-reaction / chase check:** Signal triggered days ago; entry zone 218.65–222.82, invalidation 210.31. In a bullish trend but the *bucket* (A-tier stocks) has a 5% winrate this week. **Entry now = chasing an already-triggered, extended A-tier signal the system itself downgraded.**
- **Verdict:** **MANUAL REVIEW / HOLD-ONLY.** Not a fresh A-tier long. If already in, manage against 210.31; do not add into AVGO.

### Candidate 2 — AMD (stocks) — intraday B 76.0 "high" (waiting_for_entry)
- **Internal:** Top-scored stock idea, **high confidence**, leader RS **+45.7% vs SPY**, +28.5% vs sector. Bullish regime, index + sector confirm. Earnings: safe. Also B swing 74.6 and B invest 69.8 — both `waiting_for_entry` (price not in zone). Entry 529.12–533.13, invalidation 521.09, TP1 545.17.
- **External:** No adverse catalyst; tied to AI-semi tape → **AVGO print tonight is the key event risk**.
- **Legal/headline risk:** None.
- **Price-reaction / chase check:** `waiting_for_entry` = price not yet in the planned zone, so **not a chase** if it pulls back into 529–533. **RR-to-TP1 only 1.0** (system-wide flaw) — structurally weak reward. A bad AVGO guide tonight would hit AMD hardest.
- **Verdict:** **CONDITIONAL LONG, pullback-only, reduced size.** Best fresh stock setup, but RR-capped and event-gated. Prefer waiting until *after* AVGO clears.

### Candidate 3 — SMCI (stocks) — B triggered (swing 72.5 / invest 67.8) — LEGAL/HEADLINE RISK
- **Internal:** B-tier triggered swing + invest; intraday it scores `no_trade / rejected (51.4, no_directional_setup)`. Fresh filing: **Form 8-K (FY2026)** — routine, no resolution. News_items only show an unrelated YieldMax option-income ETF distribution.
- **External — LEGAL/HEADLINE RISK (verified):** SDNY indictment **Mar 19, 2026** of 3 SMCI-associated individuals (incl. a board member) over an alleged **~$2.5B export-control scheme** (AI servers diverted to China); company not named defendant; stock fell **33.3% to $20.53** on Mar 20; multiple securities **class actions** (lead-plaintiff deadline May 26, 2026, now passed). **No clearing event.**
- **Price-reaction / chase check:** Price has recovered to ~$48–50 (signals scored there) but the **legal overhang is unresolved**; a clean technical long ignores live indictment/class-action risk.
- **Verdict:** **AVOID.** Canonical scoring regression — the invest/swing engine keeps surfacing SMCI without a legal gate.

### Candidate 4 — GOOGL (stocks) — short C 58.3 (triggered, intraday) vs bullish regime — CONTRADICTION
- **Internal:** Active intraday **short** signal C 58.3 (triggered, expires Jun 4), but the stocks report **rejects** it: `short_in_bullish_regime, rr_below_1.5`. So the system simultaneously holds an open short *and* flags it as un-actionable.
- **External (verified):** **$84.75B equity capital raise priced Jun 2** (upsized from $80B Jun 1; $40B ATM + $10B Berkshire private placement; Class A $355.20) to fund AI compute. Real **dilution overhang** — supports a short-term *fade*, but the broad-market regime is bullish and RS for short is weak.
- **Legal/headline risk:** None beyond the dilution event.
- **Price-reaction / chase check:** Price has already absorbed the raise news (priced Jun 2). Shorting into a bullish tape on a 1.0-RR signal is low-quality.
- **Verdict:** **MANUAL REVIEW — no clean trade.** Contradiction (open short vs reject + bullish regime) resolves to *flat*; watch for an AI-capex sentiment shift, don't act on the C-tier short.

### Candidate 5 — ZEC (crypto) — swing B 65.2 (tp2_hit) + verified catalyst — watchlist/hold runner
- **Internal:** Active **swing** signal B (tp2_hit, expires Jun 7) — already a winner running. Scalp watchlist #5 (55.8) and intraday watchlist #7 (56.8) with "fresh attention via 3 catalyst/news items." RS +9.8% vs BTC, but **volume below average (0.18–0.85x)** and counter-tape.
- **External (WebFetch-verified):** **Orchard soundness/double-spend bug fixed via NU6.2 hard fork (Jun 3 00:05 EDT, block 3,364,600)**; bug caught **before any exploitation**; **funds safe, supply intact**; five-day emergency response (May 29 → Jun 3) resolved. ZEC ~$629, +10%/24h. Net: a *resilience-positive* resolution, not an active exploit.
- **Price-reaction / chase check:** Already moved (+10%/24h), counter-trend long in a bearish crypto tape, weak current volume. **Entry now = chasing.** Conditional scalp pullback zone 615.62–623.59 if it ever sets up.
- **Verdict:** **HOLD existing swing runner against its stop; no fresh chase.** Watchlist only for scalp/intraday.

**Excess candidates (noted, not deep-dived — §F cap reached):**
- **AVGO** — earnings tonight; **NO trade into the print** (swing-blocked, −24 penalty, "unknown" earnings label). Re-evaluate post-print.
- **AAPL** — cleanest stock long (B 77.4 intraday triggered / B 76.7 swing), leader RS, no earnings, no legal flag — but **RR-to-TP1 ≈ 1.0**. Trend-respect pullback entry, not a chase.
- **EPIC / NEAR (crypto)** — active B intraday signals (EPIC `waiting_for_entry`, NEAR `triggered`, both expire Jun 4) but counter-tape RS-leader longs; reduced size only, per desk discipline.

---

## 8. Best Candidates Ranked

1. **AMD (stocks)** — best *fresh* setup: high-conviction B, leader RS, `waiting_for_entry`. **Conditional long on pullback into 529–533, reduced size, ideally after AVGO clears.** RR-capped (1.0).
2. **AAPL (stocks)** — clean leader long, no earnings/legal flag, but RR ≈ 1.0; pullback-entry only.
3. **NVDA (stocks)** — hold-only / manual review; A-tier signal but downgraded + untrustworthy bucket + extended into AVGO.
4. *(crypto)* **No clean fresh candidate** — ZEC/EPIC/NEAR are counter-tape; hold existing runners only.

> Net: only AMD/AAPL qualify as *conditional* fresh longs, both RR-capped and event-gated into AVGO. No high-quality, clean actionable this cycle.

---

## 9. Avoid / No Trade

- **SMCI — AVOID.** Live SDNY indictment + class-action overhang; no clearing event. (§7 Candidate 3)
- **GOOGL short — NO TRADE.** Contradiction (open short vs reject) in a bullish regime; dilution already priced. (§7 Candidate 4)
- **AVGO — NO fresh position into tonight's earnings.** Re-evaluate after the print.
- **Crypto fresh entries — NO TRADE.** Bearish/high-vol tape; all ideas C-tier watchlist; RS leaders extended (>2 ATR from EMA20).
- **Chasing ZEC / XPL / WLD / NEAR / ENA longs** — already extended; "do not chase" per system.

---

## 10. Main Risks

- **AVGO earnings tonight is the dominant near-term risk** — a soft AI-semi guide would hit NVDA / AMD / SMH / SMCI / XLK in tomorrow's session; an upside guide extends the already-stretched semi tape.
- **BTC structure fragile** — losing **$65K** opens **$60K**; ~$3.5B ETF outflows + $1.8B liquidations + Strategy selling = ongoing forced-seller risk. Any crypto long is counter-trend.
- **Stocks RR structurally capped** — nearly every idea is RR-to-TP1 ≈ 1.0 (below the 1.5 floor); even "clean" longs have poor reward geometry (TODO-stocks-rr, §14).
- **A-tier (stocks) bucket unreliable** — 5% triggered winrate / PF 0.29 this week; do not treat A-tier scores as conviction.
- **Catalyst mapping weak (79.8% unmapped)** — symbol-level catalyst signal is thin; treat as context only.
- **Data blind spots** — no liquidation heatmaps, order-book/CVD, ETF-flow feed, on-chain flows, or live social; chart tools not loaded.
- **Source ingest** (§12) attempted; if it fails it does not affect the verdicts above (advisory only).

---

## 11. Action Plan — next 4 hours

1. **Crypto:** No fresh entries. Hold ZEC (swing, tp2_hit) and XLM (swing, tp1_hit) runners against their stops. Watch BTC $65K — a clean loss = de-risk all crypto longs immediately.
2. **Stocks (pre-AVGO):** No new semi exposure into the print. If holding NVDA A-tier swing, manage against 210.31; do not add.
3. **AMD:** Only if it pulls back into **529.12–533.13** *and* AVGO's guide is not a negative shock — reduced size, invalidation 521.09, accept the 1.0 RR knowingly.
4. **AAPL:** Trend-respect pullback long candidate; not a chase. Watch SPY/QQQ + VIX.
5. **Post-AVGO (after US close):** Re-read the semi complex next cycle; AVGO guide sets NVDA/AMD/SMH/SMCI direction.
6. **Avoid:** SMCI (legal), GOOGL short (contradiction), any extended crypto RS-leader chase.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** **NO TRADE.** Bearish/high-vol; best watchlist HOME/USDT 61.2 — wait. Do not chase RS leaders.
- **Crypto intraday:** **NO TRADE (fresh).** Best watchlist ONDO/USDT 60.4. Active EPIC/NEAR B signals are counter-tape — reduced size only if discipline allows.
- **Crypto swing:** **HOLD runners only** (ZEC tp2_hit, XLM tp1_hit). Swing report stale (≈16 h) — no fresh swing call.
- **Stocks intraday:** **SELECTIVE LONG.** AMD (pullback, post-AVGO) / AAPL (pullback) only; RR-capped, event-gated. AVOID SMCI; no GOOGL short.
- **Stocks swing:** **CAUTION (carry-forward data).** Long bias intact but no fresh high-quality entry; SMCI excluded.
- **Stocks invest:** **CAUTION (carry-forward data).** Long bias; SMCI invest signals excluded on legal grounds.

---

## 13. Sources

- [Bitcoin Falls to $65,710 as Record ETF Outflows and Strategy Sale Rattle Market — Bitcoin.com, 2026-06-03](https://news.bitcoin.com/bitcoin-falls-under-66000-etf-outflows-strategy-sale/)
- [Crypto Markets: Bitcoin Slides Below $67,000 as ETF Outflows Mount — Blockhead, 2026-06-03](https://www.blockhead.co/2026/06/03/crypto-markets-bitcoin-slides-below-67-000-as-etf-outflows-mount/)
- [Zcash Activates NU6.2 Hard Fork Following Double-Spend Risk Discovery — CryptoTimes, 2026-06-03 (WebFetch-verified)](https://www.cryptotimes.io/2026/06/03/zcash-activates-nu6-2-hard-fork-following-double-spend-risk-discovery/)
- [Zcash Completes 'Most Ambitious' Network Upgrade as ZEC Resumes Recent Surge — Decrypt/Yahoo, 2026-06-03](https://tech.yahoo.com/cybersecurity/articles/zcash-completes-most-ambitious-network-150553271.html)
- [2026 June Alphabet Equity Capital Raise Press Release — Alphabet IR, 2026-06-02](https://s206.q4cdn.com/479360582/files/doc_news/2026/Jun/01/attachments/2026-June-Alphabet-Equity-Capital-Raise-Press-Release-PDF.pdf)
- [Broadcom heads into earnings with AI backlog, guidance in focus — Seeking Alpha, 2026-06-03](https://seekingalpha.com/news/4599887-broadcom-q2-2026-earnings-preview)
- [Super Micro Computer Issues Statement on Action by U.S. Attorney's Office — Super Micro IR, 2026-03-19](https://ir.supermicro.com/news/news-details/2026/Super-Micro-Computer-Issues-Statement-on-Action-by-U-S--Attorneys-Office/default.aspx)

_Internal records reused (recent + consistent, not re-fetched externally): NVDA, GOOGL, ZEC `news_items` rows (all `published_at` within 24 h). SMCI legal facts cross-checked externally this run. No fabricated dates — where a publish date was unavailable it is not invented._

---

## 14. Fix Requests / TODO

### TODO-smci-atier-legal
- **issue:** SMCI keeps surfacing as B-tier "triggered" (swing 72.5 / invest 67.8/65.2) with no legal-risk gate despite a live SDNY indictment + securities class action.
- **evidence:** `active-signals --asset-class stocks` (SMCI B swing/invest triggered); stocks report §5 shows only routine Form 8-K; external: SDNY indictment Mar 19 2026, stock −33% to $20.53.
- **suggested manual fix:** Add a legal/headline-risk gate (indictment / DOJ / SEC / class-action flag) that caps or rejects affected symbols in the stocks scoring engine.
- **priority:** high
- **first observed:** carried from prior runs; re-confirmed 2026-06-03 20:32 EEST.

### TODO-stocks-atier-winrate
- **issue:** Stocks A-tier bucket statistically unreliable — triggered winrate 5%, PF 0.29 (n=28), below 0.8 floor.
- **evidence:** `signal-stats --asset-class stocks` observations block: "(weak, n=28) tier=A: triggered winrate 5% is low … profit factor 0.29 below 0.8."
- **suggested manual fix:** Review A-tier promotion thresholds / entry geometry for stocks; consider demoting borderline A's until the bucket stabilizes.
- **priority:** high
- **first observed:** carried from prior runs; re-confirmed 2026-06-03 20:32 EEST.

### TODO-nvda-tier-conflict
- **issue:** NVDA open swing signal is A 80.6 but the engine's own re-scores show B 69.6 — a one-tier downgrade the live signal never absorbs.
- **evidence:** `active-signals` NVDA swing A 80.6 (triggered) alongside NVDA swing B 69.6 (triggered) rows for the same symbol/mode.
- **suggested manual fix:** When a re-score downgrades tier, propagate the downgrade (or close+reopen) so active signals reflect the current tier.
- **priority:** medium
- **first observed:** carried from prior runs; re-confirmed 2026-06-03 20:32 EEST.

### TODO-stocks-rr
- **issue:** Nearly every stocks idea reports RR-to-TP1 ≈ 1.0, below the stated 1.5 floor, yet still scores B-tier — reward geometry is structurally weak.
- **evidence:** stocks intraday report ideas #1–#4 all list "RR to TP1 below 1.5 (1.0)"; risk_reward score component = 0.00.
- **suggested manual fix:** Audit TP1 placement / ATR multiple in stocks target generation so passing setups carry ≥1.5 RR, or down-weight low-RR setups harder.
- **priority:** medium
- **first observed:** 2026-06-03 20:32 EEST (recurring pattern in prior reviews).

### TODO-catalyst-mapping
- **issue:** Catalyst symbol-mapping weak again — 79.8% of 1968 events unmapped (80.4% last run).
- **evidence:** computed from `data/catalysts/2026-06-03/catalyst_events.jsonl` (mapped 397 / unmapped 1571).
- **suggested manual fix:** Improve the symbol resolver in the catalyst layer (ticker/entity extraction, alias table) to lift mapped share above 50%.
- **priority:** medium
- **first observed:** recurring; re-confirmed 2026-06-03 20:32 EEST.

### TODO-avgo-earnings-unknown
- **issue:** AVGO earnings status shows "today (unknown)" in the stocks report even though the date is externally confirmed (Wed Jun 3, after close).
- **evidence:** stocks report §3 "AVGO: earnings today (unknown)"; earnings lookup failed for SPY/QQQ/IWM/DIA/SMH/XLK/XLF/XLE/XLY/XLV.
- **suggested manual fix:** Audit the earnings-calendar source (yfinance fallback) so confirmed near-dated earnings resolve to a known time instead of "unknown."
- **priority:** medium
- **first observed:** recurring (earnings UNKNOWN pattern); re-confirmed 2026-06-03 20:32 EEST.

### TODO-expired-waiting-signals
- **issue:** Several crypto scalp signals remain `waiting_for_entry` with `expires_at` already in the past (XPL 18:48, ZRO 18:17, ONDO 17:58 vs now 20:32).
- **evidence:** `active-signals --asset-class crypto` rows with past `expires_at` still listed as active/waiting.
- **suggested manual fix:** Add an expiry sweep that transitions past-`expires_at` `waiting_for_entry` signals to `expired` so the active list reflects reality.
- **priority:** low
- **first observed:** 2026-06-03 20:32 EEST.
