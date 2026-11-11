# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:45 EEST

- **Generated:** 2026-06-06 04:45 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`, **crypto overnight / Asia review** slot 04:30). Saturday — **US/EU equity markets CLOSED**; crypto is the only live actionable class. Stock signals = planning/watchlist context only.
- **Slot focus:** how crypto traded overnight after Friday's hard risk-off close, the Asia-session read into the weekend, and whether the multi-day breakdown is still shortable or now too late/oversold to chase.
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-05_2325.md` (post-close final daily review, 23:25 EEST, ~5h20m ago — §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). Verified (a) the **Iran / Strait of Hormuz drone escalation** (US shot down 4 Iranian drones launched toward the strait Fri June 5, then struck Iranian coastal radar — multiple primary outlets), and (b) **crypto's worst week since July 2024** — BTC ~$62.5k (−14.5% wk), ETH lowest since Apr 2025 (−17% wk), critical levels BTC $60,900 liq / ETH $1,420 support, $1.2B 24h liquidations, ZEC exploit contagion. WebFetch verified on CoinDesk (HTTP 200).
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; all internal price/structure is local OHLCV/ATR/EMA report fields + cited external prints.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

- **The bearish thesis kept paying overnight, and the macro behind it got worse, not better.** Friday's risk-off close (S&P −2.65%, Nasdaq-100 −4.77%, ~$1T wiped) bled straight into crypto. Overnight, **ETH broke below $1,550** (on-chain feed: 21,540 ETH / $34.1M liquidated across DeFi as it cracked $1,550) — extending the move from ~$1,700 at the prior review toward the **$1,420 critical support** CoinDesk flags as the gate to "2022 bear-market territory." BTC sits ~$62.5k, just above the **$60,900 core liquidation level**.
- **New, verified macro escalation:** the **Iran / Strait of Hormuz drone strike** (US downed 4 drones, hit Iranian radar sites Fri) is a fresh geopolitical risk-off layer on top of the AI-derating / hawkish-Fed tape. It cuts **both ways** over a thin weekend — directionally bearish for risk, but a headline-driven oil/safe-haven spike + crypto short-squeeze is a real gap risk.
- **The engine is correctly short-biased, but every short is now LATE.** All 13 active crypto signals are **B-tier, almost entirely breakdown shorts** (TON, FET, PUMP, ADA, NEAR, AVAX, DASH) in a regime the desk already labels *bearish trend (risk-off) / "short bias or no trade; avoid weak altcoin longs."* With BTC at $60,900 and ETH at $1,420 — both major support / liquidation magnets — fresh short *initiation* here is chasing into the zone where capitulation bounces start.
- **Execution levels are stale and the report generators are failing.** Crypto scalp + intraday reports **timed out again** this cycle (2700s each) — the **third consecutive cycle** they failed to regenerate. Scalp/intraday levels are now ~11–12h old. Direction context is valid (bearish persists); **execution prices must be re-pulled before any entry.**
- **Net verdict:** **Crypto = short-biased but no-chase into Asia/weekend.** Manage existing short *runners* (AVAX swing tp2 hit, PUMP triggered) with trailing stops; do **not** initiate fresh breakdown shorts at support/liquidation levels on 11–12h-stale prices with a live geopolitical gap risk. **Stocks = no action (closed).** Catalyst layer **context-only (72.2% unmapped).**

---

## 2. Data Used

**Internal — crypto reports (all STALE, regen failed this cycle):**
- `data/reports/scalp/2026-06-05_13-30_scalp_report.md` (data 13:15 UTC; **~11.5h — STALE**; regime *bearish trend (risk-off)*, BTC/ETH downtrend, altcoin breadth above EMA20 27.1%, BTC ATR pct 91 "elevated"). No A-tier, no B-tier setups — all watchlist.
- `data/reports/intraday/2026-06-05_13-54_intraday_report.md` (data 13:54 UTC; **~11.7h — STALE**).
- `data/reports/swing/2026-06-05_14-34_swing_report.md` (data 14:34 UTC; **~11h — borderline-stale carry-forward**).
- Stocks reports (intraday 20:17, swing 19:07, invest 14:55) — **weekend, market closed → context only, not re-read in detail.**

**Catalyst / narrative:** `data/catalysts/2026-06-05/` (active trading-day folder; the 06-06 folder is not created until the trading day rolls) — `catalyst_events.jsonl` (**2982 rows**), `narrative_baskets.jsonl` (**3 baskets**), latest `catalyst_cycle_23-54.md` (mtime 02:55 — fresh).

**LLM packets:** `data/processed/llm_analysis_packet.md` (mtime 17:34 — stale, crypto), `data/processed/llm_stocks_packet.md` (mtime 23:17).

**CLI / DB (read-only, this run):** `active-signals` crypto **13** (was 16 at prior review), stocks **50** (closed, context); `signal-stats` crypto week — **headline A/B sample=69, triggered=52, 13W/18L, winrate 25.0%, PF 1.556, avgR 0.19, totalR +10.0**; `detect_untracked_legacy_alerts --since 2026-06-06` → **2 untracked** (FET/USDT B scalp short 13:38; ETH/USDT B scalp short 20:36). DB `db/crypto_ai_desk.sqlite` (mtime 04:35 — live, collector writing).

**External (this run — cited §13):** Iran/Hormuz drone strike (AP/The Hill, CBC, KSAT, TWZ, ABC — primary); crypto worst-week levels (CoinDesk WebFetch HTTP 200; 24/7 Wall St, Yahoo, MEXC News); on-chain ETH <$1,550 liquidation print (t.me/lookonchain — social_only).

**Unavailable / blind:** live tick prints; TradingView/Chrome chart verification (not loaded); liquidation heatmaps / order-book / CVD; **fresh crypto scalp/intraday execution levels (reports ~11.5–11.7h stale, regen failed 3rd cycle).**

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-05_default_schedule/`.
- `scheduler.log` mtime **02:58:47 EEST** (~1h47m); latest cycle summary `cycle_02_01-21_summary.md` mtime **02:58:33** (~1h47m). Both **< 3h → NO DEFER.**
- Cycle 2 ran in **weekend (crypto-only) mode** (stocks disabled, daily swing/invest disabled): steps **ok=9 failed=2**. The **two failures are crypto scalp report + crypto intraday report, both timed out after 2700s.** Track-signals OK (tp_hits cum 171), catalyst scan OK (events=179 this cycle, baskets=3), monitor 90-min background OK.
- **Report freshness this run:** crypto scalp ~11.5h, intraday ~11.7h, swing ~11h — **all stale; scalp+intraday regen FAILED for the 3rd consecutive cycle** (timeout, see §14 `TODO-crypto-report-staleness`). Direction context valid; **levels stale — re-pull before any crypto entry.**

---

## 4. What Changed vs Previous Review (post-close 23:15 → Asia 04:30)

- **Macro got worse and gained a new vector.** At 23:25 the read was "hawkish-Fed/yields-up + AI-derating bleeding into crypto." Overnight adds a **verified geopolitical escalation** (Iran/Hormuz drones + US radar strikes) — a fresh, two-way risk-off/gap catalyst not present at the prior review.
- **ETH broke a level.** Prior review had ETH ~$1,700 "approaching." Overnight **ETH cracked $1,550** with $34M DeFi liquidations and is now at its lowest since Apr 2025, sitting above the **$1,420** make-or-break support. The breakdown thesis extended; the *runway left* shrank.
- **Crypto report staleness worsened again.** 23:25 had scalp/intraday ~9.5–10h stale + failed regen. Now ~11.5–11.7h + **failed regen a 3rd straight cycle** — regression confirmed, not transient.
- **Untracked legacy alerts: 1 → 2.** Prior run had 1 (FET/USDT). Now **2** — ETH/USDT B scalp short (20:36) added, still no backing `proposed_signal`. Worsening.
- **Active crypto signals: 16 → 13** (several overnight expiries: e.g. ETH intraday short tp3, NEAR variants, expired scalp shorts).
- **Catalyst mapping flat:** 72.7% → **72.2% unmapped** (2982 rows, 830 mapped) — still context-only.
- **Thesis: unchanged in direction (short-biased risk-off), but conviction on *fresh entries* lowered** — price has now reached the major support/liq levels, so the edge has shifted from "initiate shorts" to "manage runners / wait for bounce."

---

## 5. Catalyst Coverage

- Raw `catalyst_events.jsonl` (trading-day 2026-06-05): **2982 rows.**
- Mapped (non-null symbol): **830** · Unmapped (null symbol): **2152** · **Unmapped = 72.2%.**
- `narrative_baskets`: **3** — `perps_dex_narrative` (playbook wait_pullback, <6h, primary HYPE), `ai_narrative` (playbook related_beta_rotation, <6h, primary NEAR/RENDER/TAO/FET — note this is a *downside* rotation: AI names −13% to −18%/day), `momentum_breakout` (playbook avoid_chase, <1h, primary BABY/LA/HEI).
- **⚠ CATALYST MAPPING WEAK THIS RUN (72.2% unmapped > 50%) — use the catalyst layer as CONTEXT, NOT a final decision input.** Top-3 unmapped headlines (all equity/IPO noise leaking into the crypto trading-day feed): (1) "Want to Invest in the Hottest Upcoming IPOs… SpaceX, Anthropic, OpenAI?"; (2) "5 Top AI Stocks to Buy With $5,000 Right Now"; (3) "Asia-Pacific markets set to open subdued after Wall Street's AI-linked stocks slide." The unmapped tail is dominated by stock/finance headlines with no crypto symbol — same root cause as the `UNH/USDT` mislabel (§14 `TODO-catalyst-symbol-resolver`).

---

## 6. Market Landscape

- **Regime (internal):** bearish trend (risk-off); BTC downtrend, ETH downtrend; altcoin breadth above EMA20 **27.1%**, above EMA50 22.9%; BTC ATR percentile **91 (elevated)**. Recommended style: *short bias or no trade; avoid weak altcoin longs.*
- **External levels (verified):** **BTC ~$62.5k** (−14.5% wk), core liquidation level **$60,900**. **ETH** lowest since Apr 2025 (−17% wk), critical support **$1,420** (break → sub-$900 risk per CoinDesk); overnight on-chain print shows ETH already traded **<$1,550**. Week = **crypto's worst since July 2024**; total mkt cap −48% from peak; **$1.2B** 24h liquidations (BTC $364M, ETH $291M, ZEC $107M).
- **Drivers (verified):** capital rotation out of crypto into AI IPOs (Saylor's own framing; MSTR reportedly broke "never sell"); 10-consecutive-day spot-BTC-ETF outflows (~$3B); whale selling (~25k BTC/wk); **ZEC exploit contagion** (counterfeiting bug, −30/−50%, Arthur Hayes dumped entire ZEC); derivatives deleveraging (OI −15% to $17B, funding negative). **+ NEW:** Iran/Hormuz military escalation.
- **Equities (closed, context):** Fri S&P −2.65% (7,357), Nasdaq-100 −4.77% (28,765), ~$1T wiped on chip rout; 9-week S&P win streak ended. Asia set to open "subdued." This is the macro backdrop crypto trades against over the weekend with no equity cash market to anchor it.

---

## 7. Candidate Deep Dives (≤5)

### 7.1 PUMP/USDT — B / intraday / SHORT — **TRIGGERED (live)**
- Score 66.7; entry 0.00152536, SL/inval 0.00158214, TP1 0.00145721 (RR 1.2); created 06-05T12:52, **expires 06-06T12:52 (valid)**; setup breakdown; news=0, tg=0; weak_vs_market.
- **Internal-first:** no fresh `news_items` row for PUMP; no catalyst_events match. Pure technical breakdown short, regime-aligned.
- **Price-reaction / chase (§J):** already triggered and aligned with the risk-off tape — this is a *managed runner*, not a fresh entry. With no name-specific catalyst, the risk is a broad-market relief bounce squeezing a low-cap short. **Action: trail stop toward entry / lock partial; do not add.** Stale-level caveat applies (re-pull live price).
- **Verdict: HOLD short with trailing stop (already live). No fresh add.**

### 7.2 TON/USDT — B / intraday / SHORT — waiting_for_entry
- Score 65.8; entry 1.55115714, SL/inval 1.59194286, TP1 1.50221429 (RR 1.2); created 06-05T13:54, **expires 06-06T13:54 (valid ~9h)**; setup breakdown; news=0, tg=0; weak_vs_market (momentum 80.2). (Note a near-duplicate TON scalp short at the same levels created 13:47 is **past its 15:47 expiry** — see §14 hygiene TODO.)
- **Internal-first:** no fresh TON `news_items`/catalyst. Technical-only.
- **Price-reaction / chase (§J):** entry 1.5512 is a breakdown-retest *short trigger* — i.e. it only fills on a bounce back to 1.551 then rejection, which is the correct no-chase structure (sell strength, not weakness). That makes it the **cleaner** of the active shorts IF price retests. Risk: in a deeply oversold tape the "retest" can become a full reversal; SL 1.592 must hold.
- **Verdict: VALID short-on-retest only at 1.551 with SL 1.592 — do not market-sell into weakness. Re-pull live TON level first (11h-stale source).**

### 7.3 FET/USDT — B / intraday / SHORT — waiting_for_entry (+ untracked-alert subject)
- Score 67.0 (highest of the live shorts); entry 0.21488429, SL/inval 0.22080571, TP1 0.20777857 (RR 1.2); created 06-05T05:56, **expires 06-06T05:56 (~1h11m left — about to lapse)**; setup breakdown; weak_vs_market; AI-narrative downside-rotation primary.
- **Integrity flag:** FET is **one of the 2 untracked legacy alerts** (FET/USDT B scalp short 13:38 sent to Telegram with **no backing `proposed_signal`** → not tracked in PF/winrate). Separate from this intraday signal but same symbol — worth noting the alert/signal linkage gap.
- **Price-reaction / chase (§J):** FET already −18%/day per the ai_narrative basket; shorting a name down 18% into the weekend at a near-expired trigger is textbook *late*. Entry zone 0.2149 is above current area, so it's a sell-the-bounce trigger, but the signal lapses within the hour.
- **Verdict: STAND DOWN — near-expired + overextended; let it lapse rather than chase. Do not re-arm without a fresh bounce + fresh level.**

### 7.4 ETH/USDT — macro anchor (no live tradable signal; chase/contradiction case)
- The intraday ETH short (entry 1736) already **hit TP3** and is closed; there is no fresh ETH execution signal. ETH is included as the **dominant macro driver + contradiction case** (catalyst-vs-technical, §F-2).
- **External (verified):** ETH lowest since Apr 2025, broke **<$1,550** overnight ($34M liquidations), now above **$1,420** critical support. A break of $1,420 "opens 2022 bear territory" (CoinDesk).
- **Price-reaction / chase (§J):** ETH has *fully* reacted — the easy short is done. At $1,420 the asymmetry flips: that's a capitulation/bounce magnet, and a geopolitical headline could squeeze. **Initiating a fresh ETH short here is chasing; a $1,420 hold + reclaim is the higher-probability *mean-reversion long* setup for nimble scalpers, not a fresh short.**
- **Verdict: NO fresh short-chase. Watch $1,420 — break = momentum continuation (already priced), hold = squeeze risk. Manual / no-trade until a fresh level prints.**

### 7.5 AVAX/USDT — B / swing / SHORT — **tp2_hit (runner in profit)**
- Score 66.4; entry 7.04507143, SL/inval 7.23042857, TP1 6.82264286; created 06-05T14:34, **expires 06-12 (swing, valid)**; setup breakdown; weak_vs_market; high-volatility-danger regime tag.
- **Price-reaction / chase (§J):** already **TP2 hit** — this is the one place the desk is *winning* and the correct action is **trail the runner toward TP3**, not initiate. SL can be trailed to entry (7.045) to lock a risk-free runner. No fresh add at these extended levels.
- **Verdict: HOLD swing short runner, trail SL to breakeven, target TP3. No add.**

---

## 8. Best Candidates Ranked

1. **AVAX/USDT swing short** — *manage*: TP2 already hit, trail SL to BE, ride to TP3. The cleanest, because the edge is realized, not prospective.
2. **TON/USDT intraday short** — *conditional*: only on a retest of 1.551 + rejection, SL 1.592. Correct no-chase structure; needs a bounce to fill. Re-pull live level.
3. **PUMP/USDT intraday short** — *hold live*: trailing stop on the triggered position; no add.
- *(FET and ETH are explicitly NOT actionable as fresh shorts — see §9.)*

**No clean fresh A-tier entry anywhere; no fresh long.** The actionable edge this slot is **runner management**, not new initiation.

---

## 9. Avoid / No Trade

- **FET/USDT short** — near-expired (lapses ~05:56), −18%/day already, overextended chase. Let it lapse.
- **ETH/USDT fresh short** — fully reacted, sitting on $1,420 critical support / squeeze magnet + live geopolitical gap risk. Chasing.
- **Any fresh breakdown short initiated at market** — BTC $60,900 / ETH $1,420 are liquidation/support levels where capitulation bounces begin; weekend thinness + Iran/Hormuz headline = two-way gap risk. Short *retests*, never *weakness*.
- **All crypto longs** — regime is bearish risk-off; weak-altcoin longs are explicitly disallowed by the desk. The only long *idea* worth watching is a nimble ETH $1,420-hold-and-reclaim mean-reversion scalp — not a signal, manual only.
- **All stocks** — market closed (weekend); planning/watchlist only.

---

## 10. Main Risks

- **Stale execution levels (HIGH).** Crypto scalp/intraday reports 11.5–11.7h old, regen failed 3rd cycle. Every price in §7 must be re-pulled live before any action. This is the dominant operational risk.
- **Oversold squeeze / capitulation bounce (HIGH).** BTC $60,900 and ETH $1,420 are major support/liquidation levels; ATR pct 91. Short-chasing here is asymmetric *against* you. $1.2B already liquidated.
- **Geopolitical gap, both ways (MEDIUM-HIGH).** Iran/Hormuz escalation over a thin weekend can spike risk-off (bearish) OR trigger an oil/safe-haven + short-squeeze reflex. Verified but fast-moving.
- **Untracked alerts contaminating stats (MEDIUM).** 2 alerts (FET, ETH) sent to Telegram with no `proposed_signal` → excluded from PF/winrate; the headline 25% winrate / PF 1.56 is computed on an incomplete set.
- **Catalyst layer unreliable (MEDIUM).** 72.2% unmapped, mostly equity noise; do not let it drive a crypto decision.
- **Ingest CLI risk (LOW).** If `ingest_enriched_review_sources` fails it is logged here and does not block the review.

---

## 11. Action Plan — next 4 hours (into Asia)

1. **Re-pull live BTC/ETH/TON/PUMP/AVAX levels** before any execution — do not trust the 11h-stale report prices.
2. **AVAX swing short:** trail SL to breakeven (7.045), let it run to TP3. Realized edge — protect it.
3. **PUMP intraday short:** trailing stop on the live position; lock partial; no add.
4. **TON intraday short:** arm only as a **sell-the-retest** at 1.551 (SL 1.592); skip if price never bounces there. No market-sell into weakness.
5. **FET:** let the near-expired signal lapse; do not re-arm.
6. **ETH:** watch **$1,420** — a clean hold + reclaim is a *scalp-long* watch (manual only); a break is continuation that's already largely priced. No fresh short.
7. **Do not initiate any fresh breakdown short at market** into support/liq levels over the weekend with a live geopolitical headline.
8. **Monitor** the Iran/Hormuz situation for a weekend gap; treat any sharp green candle as squeeze, not reversal-confirmation, until BTC reclaims structure.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** No fresh entry — levels 11.5h stale + at support. Manage only; sell retests, not weakness. Direction short, conviction-on-new-entries LOW.
- **Crypto intraday:** Short-biased but no-chase. PUMP hold (trailing), TON conditional-on-retest, FET stand-down. Re-pull levels.
- **Crypto swing:** AVAX short runner — trail to BE, ride to TP3. No fresh swing initiation at extended levels.
- **Stocks (all modes):** No action — market closed (weekend). Context only.

---

## 13. Sources

- [U.S. military says it shot down Iranian drones launched toward Strait of Hormuz (AP via The Hill)](https://thehill.com/homenews/ap/ap-international/ap-us-military-shot-down-iranian-drones-launched-toward-strait-of-hormuz/) — 2026-06-05, primary_source.
- [U.S. shoots down Iranian drones launched at Strait of Hormuz; strikes radar sites (The War Zone / TWZ)](https://www.twz.com/news-features/u-s-shoots-down-iranian-drones-launched-at-strait-of-hormuz-official) — 2026-06-05, primary_source.
- [U.S. says its military shot down Iranian drones launched toward Strait of Hormuz (CBC)](https://www.cbc.ca/news/world/us-military-iran-drones-strait-of-hormuz-9.7225829) — 2026-06-05, single_source.
- [Crypto's worst week since July 2024 deepens as bitcoin, ether near critical price levels (CoinDesk)](https://www.coindesk.com/markets/2026/06/05/crypto-s-worst-week-since-july-2024-deepens-as-bitcoin-ether-near-critical-price-levels) — 2026-06-05, primary_source (WebFetch HTTP 200; BTC ~$62.5k, ETH support $1,420, OI −15%, ZEC exploit).
- [Crypto Crash Today: Why Bitcoin, Ethereum, XRP, and Solana Are All Down Double Digits (24/7 Wall St.)](https://247wallst.com/investing/2026/06/04/crypto-crash-today-why-bitcoin-ethereum-xrp-and-solana-are-all-down-double-digits/) — 2026-06-04, single_source.
- [Bitcoin (BTC) Price: Worst Week of 2026 Puts BTC at a Make-or-Break Level (MEXC News)](https://www.mexc.com/news/1130266) — 2026-06-05, single_source.
- [Bitcoin and ethereum prices today, Friday, June 5, 2026: 5 reasons why (Yahoo Finance)](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-friday-june-5-2026-prices-continue-their-descent---5-reasons-why-113631165.html) — 2026-06-05, single_source.
- ETH <$1,550 overnight liquidation print ($34.1M across DeFi) — `t.me/lookonchain`, 2026-06-06T00:23Z, **social_only** (on-chain claim, not independently verified).
- Iran drones toward Strait of Hormuz — `t.me/WalterBloomberg` citing CNN, 2026-06-05T21:11Z, social_only — **now corroborated by AP/The Hill/CBC/TWZ above (primary).**

---

## 14. Fix Requests / TODO

### TODO-crypto-report-staleness
- **issue:** Crypto scalp + intraday report generators time out (2700s each) and have failed to regenerate for **3 consecutive cycles**; execution levels now 11.5–11.7h stale.
- **evidence:** `data/scheduled_runs/2026-06-05_default_schedule/cycle_02_01-21_summary.md` steps 2 & 3 both `[FAIL] (timeout) … timed out after 2700 seconds`; report mtimes 2026-06-05 16:30 / 16:54 vs run time 04:45. Same failure logged in the 23:25 and prior reviews (Binance `exchangeInfo` RequestTimeout root cause noted there).
- **suggested manual fix:** profile the scalp/intraday CLI fetch loop; add per-exchange fetch timeouts + partial-result fallback so a single hung Binance/MEXC call can't blow the 2700s budget; consider caching `exchangeInfo`. Raise/segment the step timeout.
- **priority:** high
- **first observed:** carried from 2026-06-05 23:25 EEST; reconfirmed (worsened) 2026-06-06 04:45 EEST.

### TODO-untracked-alerts-growing
- **issue:** Telegram alerts sent without a backing `proposed_signal` (untracked → excluded from PF/winrate). Count rose 1 → 2.
- **evidence:** `detect_untracked_legacy_alerts --since 2026-06-06` → FET/USDT B scalp short (2026-06-05T13:38), ETH/USDT B scalp short (2026-06-05T20:36), both "NO (no proposed_signal)."
- **suggested manual fix:** trace the alert path that emits a watchlist_alert without persisting a `proposed_signal`; either backfill a signal row at alert time or stop sending untracked alerts. Investigate PART-1 alert/signal linkage regression.
- **priority:** medium
- **first observed:** FET carried from prior reviews; ETH new 2026-06-06 04:45 EEST.

### TODO-catalyst-symbol-resolver
- **issue:** 72.2% of catalyst_events are unmapped (null symbol); the unmapped tail is dominated by equity/IPO/finance headlines (SpaceX/Anthropic/OpenAI IPOs, "5 AI stocks to buy," Visa, Palantir, Ramp) leaking into the crypto trading-day feed. Mapping has been ~72–73% unmapped for multiple consecutive runs.
- **evidence:** `data/catalysts/2026-06-05/catalyst_events.jsonl` total=2982, mapped=830, unmapped=2152 (72.2%); related: stock ticker **`UNH/USDT`** appears in crypto catalysts with a `legal_risk` DOJ-probe tag (UnitedHealth, a stock, mis-paired as a USDT crypto symbol) — same resolver defect.
- **suggested manual fix:** add an asset-class gate to the catalyst symbol resolver so equity headlines don't enter the crypto feed as null/`<TICKER>/USDT`; or route unmapped equity-class events out of the crypto trading-day JSONL entirely.
- **priority:** medium
- **first observed:** recurring; reconfirmed 2026-06-06 04:45 EEST.

### TODO-expired-signal-hygiene
- **issue:** Some `proposed_signals` remain `status='waiting_for_entry'` after their `expires_at` has passed (stale "active" rows).
- **evidence:** DB read query — TON/USDT B scalp short (created 06-05T13:47, expires 06-05T15:47) and DASH/USDT B scalp short (same window) still `waiting_for_entry` at 04:45 06-06, ~13h past expiry.
- **suggested manual fix:** add/confirm a sweep that transitions past-`expires_at` `waiting_for_entry` rows to `expired` so `active-signals` and selection logic don't surface lapsed triggers.
- **priority:** low
- **first observed:** 2026-06-06 04:45 EEST.
