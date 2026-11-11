# Opus Enriched Review — post-close final daily review — Auto Cycle 23:24 EEST

## 1. Executive Summary

**Monday 2026-06-15, 23:24 EEST "post-close final daily review" slot — US cash close was ~24 min ago (23:00 EEST / 16:00 ET). Daily wrap + overnight-into-Asia setup.** External web research **AVAILABLE** this run (WebSearch ×2 verified the US close and BTC level; WebFetch verified Fortune BTC page — TheStreet 403'd but the index closes are corroborated by the WebSearch summary).

**The two-day risk-on thesis worked — today closed strongly risk-on and the desk's longs-only / semis-leadership routing was on the right side.** US close: **S&P 500 +1.49%, Nasdaq +2.38% (leader), Dow +1.20%, Russell 2000 +0.79%**, driven by the confirmed US–Iran peace deal reopening the Strait of Hormuz; **oil tumbled**, semis/tech led (matching the desk's SMH RS +14% read). Crypto closed risk-on but **late / into resistance**: **BTC ~$66,521 (+3.51% 24h)** pressing the **$67.5K** band, with **1D ETF inflow positive (+$66M internal / +$85.8M external) but 7D flows still net-negative (−6,155 BTC / −$410M)** → relief rally on a headline, distribution underneath.

**Daily paper-trading outcome (closed events today, by asset/tier):** **Crypto B: 109 TP1 / 31 TP2 / 81 stops on 238 entries → net-positive day** (TP1 hits clearly outran stops) — the RS-leader momentum lane did its job in a clean uptrend. **Stocks C: 32 TP1 / 16 TP2 / 14 stops → net-positive.** **Stocks A: 9 entries triggered, 0 closed** (entered late into the session, carry overnight). **Stocks B: 0 closed.** So: a **good trend day where the risk-on longs paid and the avoids were correct** — but this is one favourable-regime day, not a structural edge change (see §12 track record).

**What worked today:** risk-on longs — semis (**AMD** RS +26% vs SPY, SMH), crypto RS leaders (**GPS, ZEC, NEAR, ZRO, BABY, XLM**). **What the avoids caught:** **UNH** (DOJ criminal Medicare-fraud probe, shares −16%) stayed out of the actionable set correctly; **JTO (+44%) / XLM (+24%, vol 2.01×, tagged overextended)** chase-risk; **SMCI** (export-control indictment); **ZRO** into a **$23M token unlock**.

**Overnight-into-Asia setup:** crypto stays the live actionable class (stocks closed). BTC is **risk-on but capped at $66–67.5K** — **accept above $67.5K on volume → headroom/continuation; lose $64K → flush risk** toward $61.8K. **Geopolitical fragility flag:** a fresh overnight Telegram headline reports **Israel intercepting Hezbollah rockets** — the peace-deal narrative carrying this rally is headline-dependent and can reverse on re-escalation. Prefer **RS-leader longs on pullback, no chasing extended movers overnight.**

**Integrity (worsening):** untracked legacy crypto alerts **8 (21:39) → 10 now** (added ADA, XPL late-session) — Telegram-sent B alerts with no `proposed_signal`, never feeding PF/winrate. §14 TODO, trend 2→5→8→10 across the day. **Routing for tomorrow:** crypto/stock A/B track record stays weak (crypto B WR ~15–24%, stock A-tier longs 0% WR n=5, stock shorts −18R, crypto scalp PF 0.14) → **longs-only, B-grade-clean with confirmation, no fresh shorts, scalp research-grade only.** **Advisory only. Scanner / collection / tracking continue in all moods — nothing here says stop the system.**

## 2. Data Used

- **Crypto scalp report** `data/reports/scalp/2026-06-15_20-19_scalp_report.md` — generated 23:19 EEST → **fresh** (header), data freshness 20:00 UTC.
- **Crypto intraday report** `data/reports/intraday/2026-06-15_17-41_intraday_report.md` — mtime 20:41 EEST → **carry-forward** (~2h43m, <4h; flagged §3).
- **Crypto swing report** `data/reports/swing/2026-06-15_14-49_swing_report.md` — mtime 17:49 EEST → **carry-forward** (~5h35m; 4–12h band, flagged §3).
- **Stocks intraday report** `data/reports/stocks/intraday/2026-06-15_19-34_stocks_intraday_report.md` — data freshness 19:34 UTC → **final pre-close snapshot** (US now closed; planning context for tomorrow).
- **Stocks swing report** `data/reports/stocks/swing/2026-06-15_15-02_stocks_swing_report.md` + **invest** `…_15-08_…` — playbooks **watchlist_only (paused)** → context only.
- **Catalysts** `data/catalysts/2026-06-15/` — `catalyst_events.jsonl` + `narrative_baskets.jsonl` + `catalyst_cycle_17-42.md` (mtime 20:42 EEST).
- **LLM packets** `data/processed/llm_analysis_packet.md` (23:19) + `llm_stocks_packet.md` (20:58).
- **Internal CLI:** `active-signals` crypto (B-tier active) + stocks (active **A-tier AMD 88 / SMH 82 / JPM 80** carry-forward, plus B/C); `signal-stats` ×2; `detect_untracked_legacy_alerts --since 2026-06-15` → **10 untracked**.
- **DB:** `db/crypto_ai_desk.sqlite` (per `config/settings.yaml`) — healthy; `news_items` total **14,016**. §F priority-6 `t.me` last-4h = **8 items** (lookonchain ×4, WalterBloomberg ×4) — all macro/equity/geopolitical (SpaceX stock, Israel–Hezbollah, Trump polls); **no fresh single-symbol crypto catalyst that changes a candidate.** Daily outcome counts queried directly (see §1/§12).
- **External:** WebSearch ×2 (US market close 15 Jun; BTC level 15 Jun) + WebFetch verified (Fortune BTC page: $66,521.59, +3.51%).
- **§M ingest:** built `data/raw/enriched_review_sources/2026-06-15T2324Z.json` (3 cited sources). Ingest CLI attempted (see §10).

## 3. Scheduler / Data Freshness

- Latest run folder: `data/scheduled_runs/2026-06-15_default_schedule/`.
- `scheduler.log` mtime **23:19:10 EEST** (~5m old) → **fresh**.
- Latest cycle summary `cycle_04_20-10_summary.md` mtime **21:00:51 EEST** (~2h23m old) → **fresh** (< 3h).
- **Both under the 3h defer threshold → review proceeds.**
- Freshness labels: scalp fresh; **crypto intraday carry-forward (~2h43m)**; **crypto swing carry-forward (~5h35m, 4–12h band — used, flagged)**; stocks intraday is the final pre-close snapshot (US closed → planning only). No hard stale-data exclusions, but all stock intraday entries are now **plan-for-tomorrow**, not live.

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-06-15_2139.md` (late-session risk slot):

- **Session moved from ~1h20m-to-close → closed.** Posture shifts from "manage active exposure, don't initiate late" → **"book the day, set the overnight/tomorrow plan."**
- **The day resolved risk-on and the thesis was right.** 21:39 routed longs-only / semis-leadership / protect-active; the cash session closed **SPX +1.49% / Nasdaq +2.38%**, validating that routing. Crypto B closed the day **net-positive** (109 TP1 vs 81 stops).
- **BTC essentially flat into the close** vs 21:39 ($66.8K → ~$66.5K) — still pinned under $67K resistance; **1D ETF flow flipped clearly positive** (+$85.8M external) but 7D still negative. Character unchanged: risk-on but capped.
- **AMD/SMH/UNH unchanged in character** — AMD best semis long (now a tomorrow-RTH-retest plan), SMH structural-loser-cohort caution, **UNH AVOID re-confirmed**.
- **Integrity regression continued: 8 → 10 untracked alerts** (added ADA, XPL). Trend wrong all day.
- **New overnight risk:** Israel–Hezbollah rocket-intercept headline (t.me/WalterBloomberg, last 4h) = re-escalation risk to the peace-deal narrative — was not present at 21:39.
- **Catalyst mapping still weak** (>50% unmapped; see §5).

## 5. Catalyst Coverage

- `catalyst_cycle_17-42.md` (this-cycle scan): **500 rows scanned, 4 narrative baskets.** Cumulative `catalyst_events.jsonl` today is large (≈2.2 MB; scalp report cites **899 unique events**).
- Type mix this cycle: other_news 480, partnership 6, exploit_hack 3, regulatory_sector_headline 2, legal_risk 2, analyst_action 2, token_unlock 1, earnings_event 1.
- **⚠ Catalyst mapping weak this run — use the catalyst layer as context, not final decision.** Symbol-mapping has run >50% unmapped all day (intraday/scalp reports show the bulk of events as macro/sector noise, not single-symbol actionable). Recurring → §14 TODO.
- **Top 3 unmapped (by importance, all macro/sector noise):** (1) "One Indicted Over Crypto 'Wrench Attack' in France" (Decrypt, 0.71); (2) "Did Tether just freeze $72M in USDT … Monero money-laundering sting?" (CryptoSlate, 0.71); (3) "Congress moves to rebuild crypto crime task force…" / "Clarity Act before July 4" (CryptoSlate/CryptoBriefing, 0.66–0.68).
- **Narrative baskets:** **ai_narrative** (NEAR/RENDER/TAO/FET + WLD/ASTER — related_beta_rotation, single_source, <6h); **perps_dex_narrative** (HYPE + DYDX/GMX/ASTER — wait_pullback, <1h); **binance_ecosystem_teaser** (BNB/ASTER — sell-the-news risk, <6h); **momentum_breakout** (JTO/XLM/WLD — pure momentum, no confirmed catalyst, wait_pullback).
- **Legal/regulatory flags from the catalyst layer:** **UNH** (DOJ criminal probe), **SMCI** (export-control indictment, SEC EDGAR 8-K), **ZRO** (token unlock), **IMX** (Aztec Connect $2M exploit — old abandoned contract, low live impact).

## 6. Market Landscape

- **Crypto (close):** bullish trend / risk-on. BTC + ETH uptrend; alt breadth **76.2% > EMA20** (scalp 20:00 read; intraday earlier 81.8%), BTC ATR percentile 24 (low vol). **BTC ~$66.5K into $67.5K resistance**, support $64K / $61.8K. Funding broadly neutral / crowding normal-to-low across leaders (ZEC, BABY, NEAR, GPS) — no crowded-long blowoff, but several leaders show **OI-down-on-price-up = short-covering (weaker continuation quality)** (GPS, BABY, ZEC). Strongest RS: GPS 91.6, ZRO 91.6, BABY 89.8, ZEC 89.7, NEAR 89.2, XLM 88.2, WLD 87.9.
- **Stocks (closed):** risk_on, VIX **16.13**, breadth **100% > EMA20/EMA50**. Closed **SPX +1.49%, Nasdaq +2.38% (led), Dow +1.20%, Russell +0.79%**. Leadership: **semiconductors (SMH RS +14.19%)**, technology (XLK +6.61%), healthcare-ex-UNH. Weak: energy (XLE −8.24% on oil drop), communications. Best technical name AMD (RS vs SPY +26.44%).

### Market Mood / Risk Routing  (REQUIRED — PART 4)
- **Crypto mood:** risk-on but **late / into-resistance** ($67.5K cap, 7D ETF distribution, geopolitical headline fragility).
- **Stocks mood:** **closed** (risk_on into the bell) — planning context for tomorrow's open; overnight gap risk.
- **Dominant narrative:** US–Iran peace deal → Strait of Hormuz reopened, oil down → risk-on rotation into semis/tech (stocks) + BTC relief bid (crypto); AI/RS-leader rotation in alts.
- **Preferred side now:** **longs / wait-for-pullback** (crypto overnight); **no fresh shorts** (risk-on + stock-short −18R history); stocks = plan tomorrow's RTH.
- **Best long candidate:** **AMD** (semis RS leader) — **tomorrow-RTH-retest into 539.17–544.87**, not an overnight trade.
- **Best short candidate:** **none clean** — risk-on disfavours shorts; weakest names (STG −17%, OPG −16%) thin/squeeze-prone. Short-watch only after a failed retest.
- **Best catalyst-backed candidate:** crypto **NEAR** (ai_narrative basket, RS leader) as overnight long-watch on pullback; stocks **AMD** (semis rotation + RS).
- **What to avoid:** UNH (legal), JTO/XLM (overextended chase), SMCI (indictment), ZRO (token unlock), crypto scalp lane (PF 0.14).
- **What would change the view:** BTC **accepting above $67.5K on volume** (→ overnight continuation) or **losing $64K** (→ flush toward $61.8K); a **re-escalation headline** (Israel/Hezbollah) flipping risk-off; tomorrow's **first 30 min of US RTH** confirming or fading today's risk-on.

## 7. Candidate Deep Dives (≤ 5)

### Candidate 1 — AMD (stocks, intraday long) · active A-tier 88 / freshest-report B 77.44
- **Setup:** RS leader, trend uptrend, regime risk_on. Entry zone **539.17–544.87**, invalidation **close beyond 527.77**, TP1 561.96 / TP2 573.35 / TP3 590.44. RR-to-TP1 thin (~1.0).
- **Evidence:** RS vs SPY 20d **+26.44%**, RS vs sector +12.24%, above prev-day high, earnings safe. Catalyst: semis rotation (Nasdaq +2.38% today) + prior Citi Buy upgrade carry.
- **Contradiction check:** active A-tier 88 vs freshest report **B 77.44** — A-tier is a carry-forward; desk playbook marks **A-tier longs overpromoted (0% WR, n=5)** while the **B-tier RTH-momentum lane is the clean one (WR 55%, PF 2.03)**. Treat AMD as **B-grade actionable, not A-tier conviction.**
- **Price/chase:** US closed; AMD ran with semis today → likely above the entry zone. **Not an overnight trade.** Plan: **tomorrow's RTH retest into 539.17–544.87**, do not gap-chase at the open. Mood-aligned: yes (long). Invalidation: close < 527.77. Chase-risk: high if bought at tomorrow's open extended.

### Candidate 2 — SMH (stocks, intraday long) · active A-tier 82 / report B 72.06
- **Setup:** Entry **643.17–646.99**, invalidation close beyond 635.54, TP1 658.43. RS vs SPY +14.19%, semis the strongest sector; ETF (no earnings risk).
- **Contradiction (material):** the stock playbook's known failure mode **explicitly names "NVDA/SMCI/SMH longs structurally lose in this regime"** — the 82/72 score conflicts with the cohort's recorded behaviour.
- **Decision:** same semis thesis as AMD but with a documented structural-loser tag → **MANUAL / caution; prefer AMD for semis exposure.** If taken, pullback-into-zone only, invalidation < 635.54. Plan-for-tomorrow, not overnight.

### Candidate 3 — UNH (stocks, C-tier long, active intraday + swing) · LEGAL/HEADLINE RISK
- **LEGAL/HEADLINE RISK:** **confirmed DOJ criminal Medicare-Advantage fraud probe, extended to Optum Rx / physician reimbursement; shares −16% to a multi-year low** (catalyst layer + prior-run web verification: TipRanks / Healthcare Finance / Newsweek / Fierce Healthcare, 2026-06-15). DOJ has **not** filed charges.
- **Decision:** **AVOID / MANUAL REVIEW REQUIRED — never a clean long** regardless of score. A high momentum/RS read on a name under an active criminal probe is exactly the contradiction this section exists to catch.

### Candidate 4 — NEAR (crypto, RS-leader long-watch / ai_narrative basket)
- **Setup (scalp/swing):** RS leader, momentum 89.2, RS vs BTC +14.8%, trend uptrend. Preferred entry **pullback 2.445–2.470**, invalidation 1h close beyond 2.414, TP1 2.537. Primary in **ai_narrative** basket (related_beta_rotation).
- **Caveats:** **no fresh single-symbol verified catalyst** (narrative is single_source); volume below average (0.5×); intraday derivs show **OI-down-on-price-up = short-covering** (weaker continuation). Crypto B-tier track record weak (WR ~15–24%).
- **Decision:** **overnight LONG-WATCH, pullback-only** — actionable only on acceptance in 2.445–2.470 **with BTC holding >$64K**; not a chase at 2.48. Mood-aligned (risk-on RS-leader long). Best clean crypto long-watch into Asia. Alternatives in the same cohort: GPS, ZEC, BABY (all RS leaders, same pullback-only discipline).

### Candidate 5 — ZRO (crypto, active B swing long) · token-unlock headwind
- **Setup:** RS leader (momentum 91.6, RS vs BTC +22.4%, +26–32% multi-day), but **catalyst layer flags a $23M LayerZero token unlock** ("LayerZero rallies 14% ahead of $23mln token unlock"). 7d +32% → extended; "move may be late relative to EMA20/ATR."
- **Decision:** **AVOID-NEW / caution** — strong RS but overextended into a known unlock (supply headwind + sell-the-news). Not a fresh long here; only re-assess after the unlock clears and price holds a higher low.

## 8. Best Candidates Ranked

This is a post-close window → these are **plan-for-tomorrow / overnight-watch**, not live entries.

1. **AMD (stocks long)** — best technical name; **tomorrow-RTH retest into 539.17–544.87**, invalidation close < 527.77. Treat B-grade, not A. *Trigger: pullback into zone after the open, with SPY/QQQ not breaking down.*
2. **NEAR (crypto long-watch)** — best clean crypto long-watch overnight; *trigger: pullback acceptance 2.445–2.470 with BTC holding >$64K and volume on the retest.*
3. **GPS / ZEC / BABY (crypto RS-leader long-watch)** — same cohort, pullback-only; *trigger: defended higher low + BTC risk-on intact.*

**No clean fresh entry exists right now (market closed / overnight + leaders extended), so per PART 9:**
- **best long-watch:** AMD — trigger: tomorrow RTH retest 539.17–544.87.
- **best short-watch:** none clean — trigger: a crypto RS-loser (e.g. STG/OPG) only **after a failed retest of broken support** AND BTC losing $64K; do not pre-empt in a risk-on tape.
- **best catalyst-watch:** NEAR (ai_narrative) — trigger: a **second independent** AI-sector catalyst source confirming the basket (currently single_source) + pullback entry.

## 9. Avoid / No Trade  (this decision window only — never "stop system")

- **UNH** — DOJ criminal fraud probe; AVOID / manual review.
- **JTO (+44%) / XLM (+24%, vol 2.01×, tagged overextended)** — chase-risk; wait for a pullback structure, no market entries.
- **SMCI** — export-control indictment (SEC EDGAR 8-K).
- **ZRO** — $23M token unlock headwind + extended.
- **Crypto scalp lane** — PF 0.14, structurally broken → **research-grade only**, not Telegram-actionable.
- **Fresh shorts (either class)** — risk-on tape + stock-short −18R history.
- *(Decision-window guidance only. Scanner, candidate generation, tracking, and outcome recording continue overnight in all moods.)*

## 10. Main Risks

- **BTC at $67.5K resistance with 7D ETF distribution** — a rejection + loss of $64K opens a flush toward $61.8K (overnight, thin liquidity amplifies).
- **Geopolitical re-escalation:** Israel–Hezbollah rocket headline overnight; the entire 2-day rally is built on the US–Iran peace narrative — headline reversal = fast risk-off.
- **Overnight gap risk for stocks:** A/B stock entries (9 A triggered) carry unhedged into tomorrow's open; today's strong close can gap-fade.
- **Track-record fragility:** one good trend day does not change weak base rates (crypto B WR ~15–24%, stock A-tier 0% WR, scalp PF 0.14). Avoid over-confidence from today's green.
- **Integrity / measurement:** 10 untracked legacy alerts mean part of today's crypto B activity is invisible to PF/winrate — daily numbers slightly understate true sample.
- **§M ingest:** if the ingest CLI failed this run, cited sources may not be UPSERTed — see §14; does not affect the review's conclusions.

## 11. Action Plan — next 4 hours (overnight into Asia)

1. **Crypto, primary watch:** NEAR (and GPS/ZEC/BABY) — pullback-only long-watch; act only on defended entry zones with **BTC holding >$64K**. No chasing extended leaders.
2. **BTC level discipline:** treat **$67.5K** as the headroom trigger (accept-above-on-volume) and **$64K** as the risk line (loss → step back, expect $61.8K test).
3. **Avoid overnight:** JTO/XLM (extended), ZRO (unlock), UNH/SMCI (legal). No fresh shorts.
4. **Stocks:** no overnight action (closed). Pre-stage **AMD tomorrow-RTH-retest** plan (539.17–544.87); require the first 15–30 min to confirm, do not gap-chase.
5. **Geopolitics:** if a credible Israel/Iran re-escalation headline prints, downgrade all crypto longs to wait-and-flip the routing to risk-off (clean shorts after failed retest).
6. **System:** scanner/collection/tracking continue. No stop, no config change.

## 12. Final Verdict per Mode

- **Crypto scalp:** research-grade only (PF 0.14). RS-leader pullback ideas exist (WLD 77.3, XLM, NEAR) but treat low-confidence; no fresh Telegram-actionable scalp.
- **Crypto intraday:** longs-only, RS-leader + pullback (NEAR/GPS/ZEC/BABY watch). Overnight = wait-for-pullback, BTC-gated. Day closed net-positive (109 TP1 vs 81 stops on B).
- **Crypto swing:** carry-forward report; risk-on bias intact but capped at resistance — manage active, no fresh chase into extension/unlock (ZRO avoid).
- **Stocks intraday:** **closed** — AMD best long for tomorrow's RTH retest (B-grade), SMH caution (structural-loser cohort), UNH AVOID. No overnight entries.
- **Stocks swing / invest:** playbook-paused (watchlist_only) → context only.

## 13. Sources

- [Stock Market Today (June 15, 2026): Nasdaq, S&P 500 jump after U.S.–Iran peace deal — TheStreet](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-15-2026) (2026-06-15; SPX +1.49%, Nasdaq +2.38%, Dow +1.20%, Russell +0.79%; via WebSearch summary — page itself 403'd to WebFetch).
- [Current price of Bitcoin for June 15, 2026 — Fortune](https://fortune.com/article/price-of-bitcoin-06-15-2026/) (2026-06-15; BTC $66,521.59, +3.51% 24h — WebFetch verified).
- [Bitcoin News Today (June 15, 2026) — CoinGabbar](https://www.coingabbar.com/en/crypto-currency-news/bitcoin-news-2026-06-15) (2026-06-15; ETF net inflow $85.8M, resistance $67.5K/$70K, support $64K/$61.8K — single_source).
- Internal: `catalyst_cycle_17-42.md`, `narrative_baskets.jsonl`, `signal-stats` (crypto/stocks), `detect_untracked_legacy_alerts`, `db/crypto_ai_desk.sqlite` daily outcome query (2026-06-15).
- UNH legal flag corroborated in prior run (TipRanks / Healthcare Finance / Newsweek / Fierce Healthcare, 2026-06-15).

## 14. Fix Requests / TODO

### TODO-untracked-alerts-regression
- **issue:** Untracked legacy crypto alerts climbed 2 → 5 → 8 → **10** across today (TAO, EDEN, CHIP×3, XPL×2, ADA×2) — Telegram-sent B alerts with no matching `proposed_signal`, so they never feed PF/winrate/avgR.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-06-15` → 10 rows, all "NO (no proposed_signal)"; trend visible across 18:40/21:39 reviews.
- **suggested manual fix:** trace the watchlist-alert → proposed_signal registration path for crypto B scalp/intraday; ensure every Telegram-sent alert writes a `proposed_signal` with a tracked `signal_id` (PART 1 regression).
- **priority:** high
- **first observed:** 2026-06-15 (escalating all day; logged 18:40, re-logged 23:24 EEST)

### TODO-catalyst-mapping-weak
- **issue:** Catalyst symbol-mapping has run >50% unmapped all day (bulk of events macro/sector noise, not single-symbol actionable) — weakens the catalyst layer's decision value.
- **evidence:** `catalyst_cycle_17-42.md` (500 rows, top importance dominated by unmapped/basket headlines); intraday/scalp reports flag the same.
- **suggested manual fix:** improve the symbol resolver / entity extraction in the catalyst layer (alias table, ticker disambiguation, macro-vs-symbol classifier).
- **priority:** medium
- **first observed:** 2026-06-15 (recurring; re-logged 23:24 EEST)

### TODO-stocks-A-tier-overpromotion
- **issue:** Stock A-tier longs show **0% WR (n=5)** while B-tier RTH-momentum is the clean lane (WR 55%, PF 2.03). A-tier names (AMD/SMH 82–88) are carry-forward promotions of structurally-losing cohorts.
- **evidence:** `signal-stats --asset-class stocks` tier split (A n=5 WR 0%); playbook known-failure-mode note "NVDA/SMCI/SMH longs structurally lose in this regime."
- **suggested manual fix:** review the A-tier promotion logic for stocks; consider demoting/sizing A-tier to match the B-tier-clean evidence, or gating A-promotion on catalyst confirmation.
- **priority:** medium
- **first observed:** 2026-06-15 (re-logged 23:24 EEST)
