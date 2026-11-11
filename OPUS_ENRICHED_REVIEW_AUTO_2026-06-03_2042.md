# Opus Enriched Review — Auto Cycle 20:42 EEST

- **Generated:** 2026-06-03 20:42 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`)
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-03_2032.md` (≈10 m ago — same scheduler cycle, see §4)
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). Every external claim cited in §13 with source + date + URL. One WebFetch (tokenist) returned 403; a second (Blockhead) verified successfully.
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; all price/structure data is from local OHLCV/ATR/EMA report fields.
- **Advisory only. No auto-trade.**

---

## 1. Executive Summary

- **This run sits ~10 min after the 20:32 scheduled review and shares its underlying data — the one new input is a fresher stocks intraday report (17:37 UTC vs 17:16).** Desk posture is **re-confirmed, not changed**: crypto no-trade (bearish/high-vol), stocks long-biased but RR-capped and event-gated into AVGO's earnings tonight.
- **AVGO reports earnings TONIGHT (Wed Jun 3, after US close ≈ 23:00 EEST) — NOT yet reported as of this run.** Externally re-confirmed: guide rev **~$22B (+47% YoY)**, AI-semi **~$10.7B (+140% YoY)**, GAAP EPS consensus **~$1.73**, EBITDA margin ~68%. System still labels earnings **"today (unknown)"** with a **−24 penalty / swing-blocked**. **No fresh AVGO position into the print.** It sets AI-semi direction (NVDA/AMD/SMH/SMCI/XLK) for tomorrow.
- **AMD is the freshest high-conviction stock name (intraday B 76.68, "high" confidence, `waiting_for_entry`).** Leader RS **+45.89% vs SPY 20d**, +28.24% vs sector, bullish regime, earnings-safe. External this run: AMD **opened +3.41% on Jun 3** and an analyst **upgraded it to Strong Buy** (AI-inference demand). Caveats unchanged: **RR-to-TP1 only 1.0** (below the 1.5 floor) and it sits directly in front of AVGO's print. Already up on the day → **pullback-into-zone (529.65–533.67) only, not a chase, reduced size, ideally after AVGO clears.**
- **SMCI legal overhang still live and unresolved — AVOID (canonical regression).** Active signals still feed SMCI as **B-tier "triggered" across swing (~72) and invest (~67)**; intraday it scores `no_trade / rejected (51.0)`. Only fresh item is a **routine Form 8-K (FY2026)** — no legal resolution. The **Mar 19 2026 SDNY indictment** (alleged ~$2.5B export-control scheme; stock −33% to $20.53 on Mar 20) + securities class action remain unresolved. **SMCI → AVOID** (TODO-smci-atier-legal, §14).
- **Stocks A-tier remains a statistically untrustworthy bucket.** `signal-stats` (stocks) prints **tier=A triggered winrate 5%, PF 0.29 (n=27)** — below the 0.8 floor; tier=B 25%, tier=C 24% also low. The active A-tier names (**AMD A 87 / SMH A 82 / NVDA swing A 80** in `active-signals`) inherit that skepticism — treat A-tier as an *attention flag, not a green light* (TODO-stocks-atier-winrate, §14).
- **Crypto stays in a high-vol bearish tape; zero fresh A/B setups** across scalp and intraday — every idea is C-tier watchlist. **BTC ~$65.7K** (externally confirmed), support **$65K → $60K**, **~$2.8–3.5B ETF outflows over 10–11 days**, **$1.8B liquidations (largest since Feb)**. RS leaders (XPL/GPS/NEAR/ZRO/ONDO/ZEC/WLD) are counter-tape and mostly extended (>2 ATR from EMA20 → "do not chase"). **Catalyst mapping weak this run (79.8% unmapped) — context only.** Desk no-trade for fresh crypto entries is correct.

---

## 2. Data Used

**Internal — fresh (<2.5 h):**
- `data/reports/scalp/2026-06-03_15-41_scalp_report.md` (mtime 18:41 EEST, ~2.0 h). Regime: **bearish trend (risk-off)**.
- `data/reports/intraday/2026-06-03_16-04_intraday_report.md` (mtime 19:04 EEST, ~1.6 h). Regime: bearish.
- `data/reports/stocks/intraday/2026-06-03_17-37_stocks_intraday_report.md` (mtime ~20:37 EEST, ~0.04 h; session = regular). **Fresher than the 17:16 report the 20:32 review used.** Weekday. Regime: **bullish**.
- `data/catalysts/2026-06-03/` — `catalyst_events.jsonl` (1968 rows / 780 unique), `narrative_baskets.jsonl` (5 baskets), latest `catalyst_cycle_16-05.md`.
- CLI / DB: `active-signals` (crypto 9 rows / stocks 50 rows), `signal-stats` (crypto + stocks), `detect_untracked_legacy_alerts --since 2026-06-03` (**None**).
- LLM packets `data/processed/llm_analysis_packet.md` / `llm_stocks_packet.md` (reused as written context).

**Internal — carry-forward / stale (swing/invest):**
- `data/reports/swing/2026-06-03_01-20_swing_report.md` — ~16.3 h old → **STALE (>14 h)**. Excluded from fresh swing final-verdict; context only.
- `data/reports/stocks/swing/2026-06-03_13-11_stocks_swing_report.md` — ~4.5 h → **carry-forward (flagged)**.
- `data/reports/stocks/invest/2026-06-03_13-15_stocks_invest_report.md` — ~4.4 h → **carry-forward (flagged)**.

**External (this run — cited §13):** Tokenist + Blockhead (BTC ~$65.7K, $65K/$60K support, ETF outflows, $1.8B liquidations; Blockhead WebFetch-verified); Money Morning + Seeking Alpha (AVGO earnings tonight + consensus); TradingKey + TheStreet (AMD +3.41% open, Strong Buy upgrade). SMCI / AVGO / BTC legal & event facts cross-checked against the 20:32 run's verified citations (≈10 min old, consistent).

**Unavailable / blind:** TradingView / Chrome chart verification (tool not loaded); live social attention beyond RSS-bridged `t.me/WalterBloomberg` + `t.me/lookonchain`; liquidation heatmaps, order-book depth/CVD, ETF-flow feed, on-chain whale flows, token-unlock calendar (manual/unconnected).

---

## 3. Scheduler / Data Freshness

- **Scheduler: FRESH — review proceeds.** Latest run folder `data/scheduled_runs/2026-06-03_default_schedule/`. `scheduler.log` mtime **19:18 EEST (~1.4 h)**; latest `cycle_02_18-16_summary.md` mtime **19:18 EEST (~1.4 h)**. Defer rule requires BOTH > 3 h — not met.
- Scalp / intraday (crypto) + stocks intraday: **fresh** (~0.04 h – 2.0 h).
- Stocks swing / invest: **carry-forward** (≈4.4–4.5 h, within 4–12 h band) — context only, excluded from fresh swing/invest final call.
- Crypto swing report: **STALE (≈16.3 h)** — excluded from swing final-verdict; active ZEC/XLM swing *signals* (from `active-signals`) used instead.

---

## 4. What Changed vs Previous Review (20:32 EEST)

- **Same scheduler cycle.** The 20:32 review and this one read the same scalp (18:41) and intraday (19:04) crypto reports and the same catalyst/active-signal snapshot. The only material new input is a **fresher stocks intraday report (17:37 UTC)** that re-scored the top names: **AMD B 76.68 (high), SMH B 71.02, XLK B 66.4, LLY B 66.06** — same lineup/posture as the 17:16 read, scores within noise.
- **AMD external freshness:** AMD **opened +3.41% on Jun 3** with an analyst **Strong Buy upgrade** (AI-inference demand, ~70% YoY Q2 rev growth narrative). Net adds *chase risk* to an otherwise clean B — reinforces pullback-only.
- **AVGO:** still pre-print (reports after today's US close). No new earnings data yet.
- **Confirmed / unchanged:** SMCI legal overhang (no clearing event); stocks A-tier untrustworthy bucket; NVDA A-vs-B tier conflict; AVGO swing-block + "unknown" earnings label; universal stocks RR≈1.0 flaw; catalyst mapping weak (79.8%); untracked-alert detector clean (None).
- **Thesis changed?** **No** — desk posture (crypto no-trade; stocks long-biased but RR-capped and event-gated into AVGO) is **unchanged and re-confirmed**.

---

## 5. Catalyst Coverage

- Total `catalyst_events` (rows today): **1968** (780 unique per report)
- Mapped (non-null symbol): **397**
- Unmapped (null symbol): **1571** → **79.8% unmapped**
- `narrative_baskets`: **5** (ai_narrative, rwa_narrative, perps_dex_narrative, momentum_breakout + 1)
- **⚠️ catalyst mapping weak this run (79.8% unmapped) — use the catalyst layer as context, not a final decision.** Persistent pattern (79.8% at 20:32, 80.4% prior) → TODO-catalyst-mapping (§14).
- Top 3 unmapped (by importance) — all sector-level / non-symbol headlines (expected to be unmapped):
  1. *"DeFi won't win over big banks until it fixes its hacking problem, executives say"* (CoinDesk) — exploit_hack sector theme.
  2. *"DOJ, CFTC probe George Santos over Kalshi trades tied to State of the Union appearance"* — regulatory headline.
  3. *"Trezor Reveals Hardware Wallet Vulnerability, But Funds 'Safe'"* — sector security theme.

---

## 6. Market Landscape

- **Crypto — bearish / risk-off.** BTC downtrend, ETH downtrend, altcoin breadth **40% > EMA20**, BTC ATR percentile **98 (elevated)**. Recommended style: short bias or no trade; avoid weak altcoin longs. Externally: **BTC ~$65.7K**, support **$65K → $60K**, **~$2.8–3.5B ETF outflows (10–11 days)**, **$1.8B liquidations (largest since Feb, $1.35B longs)**. RS leaders bouncing *against* a weak tape — counter-trend, capped, mostly extended (>2 ATR from EMA20 → "do not chase").
- **Stocks — bullish / risk-on.** Regime **bullish**, VIX **16.23**, breadth **100% > EMA20/50**, all 4 indices uptrending. Leadership: **semiconductors (SMH RS +17.65%)** and **technology (XLK RS +14.03%)**. Laggards: utilities (−9.06%), communications (−7.24%), staples (−6.07%). **The whole semi complex is event-gated into AVGO's print tonight.** Structural flaw persists: nearly every stock idea shows **RR-to-TP1 ≈ 1.0** (below the 1.5 floor).
- **Crypto–equity divergence persists** — equities firm/at-highs while BTC slides.

---

## 7. Candidate Deep Dives (≤5)

### Candidate 1 — AMD (stocks) — intraday B 76.68 "high" (`waiting_for_entry`)
- **Internal:** Top-scored stock idea, **high confidence**, leader RS **+45.89% vs SPY**, +28.24% vs sector. Bullish regime, index + sector confirm; earnings safe. Entry zone **529.65–533.67**, invalidation **521.62**, TP1 **545.71**. Also shows A 87 / B 76 / B 74 across active-signals modes (some `waiting_for_entry`, some `triggered`).
- **External (this run):** AMD **opened +3.41% on Jun 3**; analyst **upgrade to Strong Buy** citing AI-inference demand; sector forecast revised up Jun 2. Constructive — but the +3.41% day adds chase risk.
- **Legal/headline risk:** None.
- **Price-reaction / chase check:** Signal is `waiting_for_entry` (price not yet in the planned zone) → **not a chase if it pulls back into 529.65–533.67**. But it's already +3.41% on the day and **RR-to-TP1 is only 1.0** (system-wide flaw). A weak AVGO guide tonight hits AMD hardest.
- **Verdict:** **CONDITIONAL LONG — pullback-only into 529.65–533.67, reduced size, ideally after AVGO clears.** Best fresh stock setup but RR-capped and event-gated. Do not chase the +3.41% move.

### Candidate 2 — SMH (stocks) — intraday B 71.02 (`waiting_for_entry`) — semis leader, event-gated
- **Internal:** Semiconductor ETF, **B 71.02 medium**, leader RS **+17.65% vs SPY 20d**, bullish regime + index confirm, no earnings (ETF). Entry **634.08–637.26**, invalidation **627.72**, TP1 **646.80**. Active A 82 (waiting) also on the book.
- **External:** No single-name catalyst; SMH is a direct proxy for the AI-semi tape → **AVGO print tonight is the dominant event risk** (AVGO is a top SMH constituent).
- **Legal/headline risk:** None.
- **Price-reaction / chase check:** `waiting_for_entry` → pullback into 634–637 is not a chase, but **RR≈1.0** and the entire basket re-prices on AVGO's guide tonight. Buying the ETF directly into its largest single-name earnings event is poor timing.
- **Verdict:** **WAIT — no fresh add into AVGO.** Clean trend/RS but event-gated; re-evaluate the semi complex post-print.

### Candidate 3 — SMCI (stocks) — active B "triggered" (swing/invest) — LEGAL/HEADLINE RISK
- **Internal:** B-tier triggered across swing (~72) and invest (~67) in `active-signals`; intraday it scores `no_trade / rejected (51.0, no_directional_setup)`. Fresh filing: **Form 8-K (FY2026)** — routine, no resolution.
- **External — LEGAL/HEADLINE RISK (verified, carried from 20:32 run ≈10 min ago):** SDNY indictment **Mar 19, 2026** of 3 SMCI-associated individuals (incl. a board member) over an alleged **~$2.5B export-control scheme** (AI servers diverted to China); company not named defendant; stock fell **33.3% to $20.53** on Mar 20; securities **class actions** (lead-plaintiff deadline May 26 2026, now passed). **No clearing event.**
- **Price-reaction / chase check:** Price recovered to ~$47–50 where signals score, but the **legal overhang is unresolved** — a clean technical long ignores live indictment/class-action risk.
- **Verdict:** **AVOID.** Canonical scoring regression — invest/swing engine keeps surfacing SMCI without a legal gate (TODO-smci-atier-legal).

### Candidate 4 — AVGO (stocks) — earnings TONIGHT — no position into the print
- **Internal:** C/B-tier with **−24 earnings penalty / swing-blocked**; stocks report §3 labels it **"earnings today (unknown)."** Active intraday B 65 (triggered) and C rows exist but the engine itself blocks it on event risk.
- **External (verified this run):** Reports **after today's US close (≈23:00 EEST)**. Consensus: rev **~$22.12B (+47% YoY)**, AI-semi **~$10.7B (+140% YoY)**, GAAP EPS **~$1.73**, EBITDA margin ~68%. HSBC raised its target into the print.
- **Legal/headline risk:** None.
- **Price-reaction / chase check:** Pre-print; any entry now is a binary-event gamble. The print sets AI-semi direction (NVDA/AMD/SMH/SMCI/XLK) for tomorrow.
- **Verdict:** **NO TRADE into the print.** Re-evaluate post-earnings next cycle. (TODO-avgo-earnings-unknown for the "unknown" label.)

### Candidate 5 — LLY (stocks) — intraday B 66.06 (`waiting_for_entry`) — cleanest non-semi long
- **Internal:** **B 66.06 medium**, healthcare, RS **follower** (+5.74% vs SPY, +8.19% vs sector), bullish regime + index confirm, **earnings safe**. Entry **1083.23–1088.09**, invalidation **1073.52**, TP1 **1102.66**. Not tied to the semi/AVGO event.
- **External:** No adverse single-name catalyst surfaced this run; healthcare sector is *mixed* (RS −2.46% vs SPY 20d) — a follower long, not a leader.
- **Legal/headline risk:** None surfaced.
- **Price-reaction / chase check:** `waiting_for_entry` → pullback into 1083–1088 is not a chase. **RR≈1.0** (same structural flaw). Advantage: **decoupled from AVGO event risk**, so it does not need to wait on the print.
- **Verdict:** **CONDITIONAL LONG — pullback-only into 1083–1088, reduced size.** The cleanest event-independent stock long this cycle, but RR-capped and only a sector follower; modest conviction.

**Excess candidates (noted, not deep-dived — §F cap reached):**
- **NVDA (stocks)** — active swing **A 80 (triggered)** but the engine's own swing re-score shows **B ~69** (unabsorbed downgrade); extended AI-semi tape into AVGO + untrustworthy A-tier bucket → **HOLD-only / manual review, no fresh add** (TODO-nvda-tier-conflict).
- **XLK (stocks)** — B 66.4 tech-ETF leader long, same event-gated/RR-capped profile as SMH.
- **Crypto (ZEC / ONDO / XPL / NEAR / EPIC)** — active B signals are counter-tape RS-leader longs (ZEC swing tp2_hit running; EPIC/NEAR intraday); reduced-size/hold-only per desk discipline. ZEC's Orchard/NU6.2 fix is verified-resolved (no exploit, funds safe) but already +8–10% and counter-tape → watchlist, not a chase.

---

## 8. Best Candidates Ranked

1. **AMD (stocks)** — best *fresh* setup: high-conviction B, leader RS, `waiting_for_entry`. **Conditional long on pullback into 529.65–533.67, reduced size, ideally after AVGO clears.** RR-capped (1.0); already +3.41% on the day — do not chase.
2. **LLY (stocks)** — cleanest *event-independent* long (no AVGO exposure), earnings-safe; pullback into 1083–1088 only. RR≈1.0, sector follower → modest conviction.
3. **SMH / XLK (stocks)** — clean semi/tech-ETF leaders but **wait — no fresh add into AVGO's print tonight.**
4. **NVDA (stocks)** — hold-only / manual review; A-tier signal but downgraded + untrustworthy bucket + extended into AVGO.
5. *(crypto)* **No clean fresh candidate** — RS leaders counter-tape; hold existing runners only.

> Net: only **AMD** (event-gated) and **LLY** (event-independent) qualify as *conditional* fresh longs, both RR-capped. No high-quality, clean actionable this cycle.

---

## 9. Avoid / No Trade

- **SMCI — AVOID.** Live SDNY indictment + class-action overhang; no clearing event. (§7 Candidate 3)
- **AVGO — NO fresh position into tonight's earnings.** Binary event after close; re-evaluate post-print.
- **SMH / XLK / NVDA — no fresh semi exposure into the AVGO print.** Hold existing only.
- **Crypto fresh entries — NO TRADE.** Bearish/high-vol tape; all ideas C-tier watchlist; RS leaders extended (>2 ATR from EMA20).
- **Chasing ZEC / XPL / WLD / NEAR / ENA longs** — already extended; "do not chase" per system. Chasing AMD's +3.41% intraday move — wait for the pullback zone.

---

## 10. Main Risks

- **AVGO earnings tonight is the dominant near-term risk** — a soft AI-semi guide hits NVDA/AMD/SMH/SMCI/XLK in tomorrow's session; an upside guide extends an already-stretched semi tape.
- **BTC structure fragile** — losing **$65K** opens **$60K**; ~$2.8–3.5B ETF outflows + $1.8B liquidations + Strategy selling = ongoing forced-seller risk. Any crypto long is counter-trend.
- **Stocks RR structurally capped** — nearly every idea is RR-to-TP1 ≈ 1.0 (below the 1.5 floor); even "clean" longs (AMD/LLY/SMH) have poor reward geometry (TODO-stocks-rr).
- **A-tier (stocks) bucket unreliable** — 5% triggered winrate / PF 0.29 this week; B 25% / C 24% also low. Do not treat tier scores as conviction.
- **Catalyst mapping weak (79.8% unmapped)** — symbol-level catalyst signal thin; context only.
- **Data blind spots** — no liquidation heatmaps, order-book/CVD, ETF-flow feed, on-chain flows, or live social; chart tools not loaded.
- **Source ingest** (§12) attempted; if it fails it does not affect the verdicts above (advisory only).

---

## 11. Action Plan — next 4 hours

1. **Crypto:** No fresh entries. Hold ZEC (swing, tp2_hit) / XLM (swing) runners against their stops. Watch BTC **$65K** — a clean loss = de-risk all crypto longs immediately.
2. **Stocks (pre-AVGO):** No new semi exposure into the print. If holding NVDA A-tier swing, manage against its stop; do not add.
3. **AMD:** Only if it pulls back into **529.65–533.67** *and* AVGO's guide is not a negative shock — reduced size, invalidation 521.62, accept the 1.0 RR knowingly. Do not chase the +3.41% day.
4. **LLY:** Event-independent pullback-long candidate into **1083–1088**; reduced size, not a chase. Watch SPY/QQQ + VIX.
5. **Post-AVGO (after US close ~23:00 EEST):** Re-read the semi complex next cycle; AVGO guide sets NVDA/AMD/SMH/SMCI/XLK direction.
6. **Avoid:** SMCI (legal), any extended crypto RS-leader chase, fresh AVGO/semi exposure into the print.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** **NO TRADE.** Bearish/high-vol; best watchlist HOME/USDT 61.2 — wait. Do not chase RS leaders.
- **Crypto intraday:** **NO TRADE (fresh).** Best watchlist ONDO/USDT 60.4. Active EPIC/NEAR B signals are counter-tape — reduced size only if discipline allows.
- **Crypto swing:** **HOLD runners only** (ZEC tp2_hit, XLM). Swing report stale (≈16 h) — no fresh swing call.
- **Stocks intraday:** **SELECTIVE LONG.** AMD (pullback, post-AVGO) / LLY (pullback, event-independent) only; RR-capped. AVOID SMCI; no fresh semi exposure into AVGO.
- **Stocks swing:** **CAUTION (carry-forward data).** Long bias intact but no fresh high-quality entry; SMCI excluded; semis event-gated.
- **Stocks invest:** **CAUTION (carry-forward data).** Long bias; SMCI invest signals excluded on legal grounds.

---

## 13. Sources

- [Bitcoin Price Falls to $65,710 as Record ETF Outflows and Strategy Sale Rattle Market — Tokenist, 2026-06-03](https://tokenist.com/bitcoin-price-falls-65710-etf-outflows-strategy-sale/)
- [Crypto Markets: Bitcoin Slides Below $67,000 as ETF Outflows Mount — Blockhead, 2026-06-03 (WebFetch-verified)](https://www.blockhead.co/2026/06/03/crypto-markets-bitcoin-slides-below-67-000-as-etf-outflows-mount/)
- [Broadcom (AVGO) Reports Wednesday — Wall Street Expects 140% AI Revenue Growth — Money Morning, 2026-05-30](https://moneymorning.com/2026/05/30/broadcom-avgo-q2-2026-earnings-preview-ai-revenue-june)
- [Broadcom heads into earnings with AI backlog, guidance in focus — Seeking Alpha, 2026-06-03](https://seekingalpha.com/news/4599887-broadcom-q2-2026-earnings-preview)
- [AMD Stock Opened Up by 3.41% on Jun 3: Facts Behind the Movement — TradingKey, 2026-06-03](https://www.tradingkey.com/news/market-movers/261944011-market-movers-amd-20260603)
- [DA Davidson analyst resets AMD stock price target for 2026 — TheStreet, 2026-06-03](https://www.thestreet.com/investing/stocks/da-davidson-resets-amd-stock-price-target-for-the-rest-of-2026-intel-earning)

_SMCI legal facts (SDNY indictment Mar 19 2026, −33% to $20.53, class action), GOOGL $84.75B raise, and ZEC NU6.2 resolution were externally verified in the 20:32 run ≈10 min ago and are consistent — reused, not re-fetched. No fabricated dates: where a publish date was unavailable it is not invented. The tokenist WebFetch returned HTTP 403 (link retained from WebSearch result; Blockhead fetch verified the BTC narrative independently)._

---

## 14. Fix Requests / TODO

### TODO-smci-atier-legal
- **issue:** SMCI keeps surfacing as B-tier "triggered" (swing ~72 / invest ~67) with no legal-risk gate despite a live SDNY indictment + securities class action.
- **evidence:** `active-signals --asset-class stocks` (SMCI B swing/invest triggered); stocks report §5 shows only routine Form 8-K; external: SDNY indictment Mar 19 2026, stock −33% to $20.53.
- **suggested manual fix:** Add a legal/headline-risk gate (indictment / DOJ / SEC / class-action flag) that caps or rejects affected symbols in the stocks scoring engine.
- **priority:** high
- **first observed:** carried from prior runs; re-confirmed 2026-06-03 20:42 EEST.

### TODO-stocks-atier-winrate
- **issue:** Stocks A-tier bucket statistically unreliable — triggered winrate 5%, PF 0.29 (n=27), below the 0.8 floor; B 25% / C 24% also low.
- **evidence:** `signal-stats --asset-class stocks` observations: "(weak, n=27) tier=A: triggered winrate 5% is low … profit factor 0.29 below 0.8"; tier=B/C winrate 25%/24%.
- **suggested manual fix:** Review A-tier promotion thresholds / entry geometry for stocks; consider demoting borderline A's until the bucket stabilizes.
- **priority:** high
- **first observed:** carried from prior runs; re-confirmed 2026-06-03 20:42 EEST.

### TODO-nvda-tier-conflict
- **issue:** NVDA open swing signal is A 80 but the engine's own re-scores show B ~69 — a one-tier downgrade the live signal never absorbs.
- **evidence:** `active-signals` NVDA swing A 80 (triggered) alongside NVDA swing B ~69 rows for the same symbol/mode.
- **suggested manual fix:** When a re-score downgrades tier, propagate the downgrade (or close+reopen) so active signals reflect the current tier.
- **priority:** medium
- **first observed:** carried from prior runs; re-confirmed 2026-06-03 20:42 EEST.

### TODO-stocks-rr
- **issue:** Nearly every stocks idea reports RR-to-TP1 ≈ 1.0, below the stated 1.5 floor, yet still scores B-tier — reward geometry is structurally weak.
- **evidence:** stocks intraday report ideas #1–#4 (AMD/SMH/XLK/LLY) all list "RR to TP1 below 1.5 (1.0)"; risk_reward score component = 0.00.
- **suggested manual fix:** Audit TP1 placement / ATR multiple in stocks target generation so passing setups carry ≥1.5 RR, or down-weight low-RR setups harder.
- **priority:** medium
- **first observed:** recurring; re-confirmed 2026-06-03 20:42 EEST.

### TODO-catalyst-mapping
- **issue:** Catalyst symbol-mapping weak again — 79.8% of 1968 events unmapped.
- **evidence:** computed from `data/catalysts/2026-06-03/catalyst_events.jsonl` (mapped 397 / unmapped 1571).
- **suggested manual fix:** Improve the symbol resolver in the catalyst layer (ticker/entity extraction, alias table) to lift mapped share above 50%.
- **priority:** medium
- **first observed:** recurring; re-confirmed 2026-06-03 20:42 EEST.

### TODO-avgo-earnings-unknown
- **issue:** AVGO earnings status shows "today (unknown)" in the stocks report even though the date/time is externally confirmed (Wed Jun 3, after close).
- **evidence:** stocks report §3 "AVGO: earnings today (unknown)"; earnings lookup failed for SPY/QQQ/IWM/DIA/SMH/XLK/XLF/XLE/XLY/XLV.
- **suggested manual fix:** Audit the earnings-calendar source (yfinance fallback) so confirmed near-dated earnings resolve to a known time instead of "unknown."
- **priority:** medium
- **first observed:** recurring (earnings UNKNOWN pattern); re-confirmed 2026-06-03 20:42 EEST.

### TODO-expired-waiting-signals
- **issue:** Several crypto scalp signals remain `waiting_for_entry` with `expires_at` likely already in the past (XPL/ZRO/ONDO scalp rows persisted from earlier cycles).
- **evidence:** `active-signals --asset-class crypto` shows XPL/ZRO/ONDO scalp `waiting_for_entry` rows still listed as active (flagged in the 20:32 run with past `expires_at`).
- **suggested manual fix:** Add an expiry sweep that transitions past-`expires_at` `waiting_for_entry` signals to `expired` so the active list reflects reality.
- **priority:** low
- **first observed:** carried from 20:32; re-confirmed 2026-06-03 20:42 EEST.
