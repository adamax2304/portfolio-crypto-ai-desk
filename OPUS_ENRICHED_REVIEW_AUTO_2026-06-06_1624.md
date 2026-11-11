# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:24 EEST

- **Generated:** 2026-06-06 16:24 EEST (auto-enriched-review, scheduled task `opus-enriched-review-preus`, **pre-US-open decision review** slot 16:20, executing `opus-enriched-review-4h/SKILL.md`).
- **⚠ It is SATURDAY — US (and EU) cash equities are CLOSED today.** The literal "US cash open" is **Monday**. This slot therefore pivots to: (a) **crypto is the only live market pricing the weekend**, and (b) **gap-risk setup for Monday's actual US open**. Stock signals = planning/watchlist context only.
- **Slot focus:** the final pre-open read — what the weekend geopolitical re-escalation + the multi-day risk-off mean for crypto right now and for Monday's equity gap; which (if any) A/B setups are actionable.
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-06_1140.md` (Europe / pre-US context, 11:40 EEST, ~4.7h ago — see §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). Verified this run: (a) **BTC ~$59,654 (−6.1%)**, **ETH ~$1,550 (−12.7%)** — BTC decisively below $60k (Yahoo Finance/CoinDesk live print); (b) **Iran–US conflict RE-ESCALATING** — Iran drone/missile strike on Kuwait's international airport (Jun 3, **1 killed, 63 injured**), ongoing US-Iran strike exchanges, fragile ceasefire under strain (CNN/NBC/Al Jazeera/RFERL search; Wikipedia *2026 Iran war* WebFetch HTTP 200 confirms US naval blockade + **Iran closed Strait of Hormuz → "largest supply disruption in history of the global oil market"** + financial-market volatility). **WebFetch on NBC and RFERL returned HTTP 403** — substituted Wikipedia (200) + search snippets; all geopolitical claims cited §13.
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; internal price/structure is local OHLCV/ATR/EMA report fields + cited external prints.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

- **The dominant driver has shifted back to GEOPOLITICS into the weekend, and it is a fresh re-escalation — not the receding item the 11:40 review filed it as.** New Telegram macro prints landed *after* the last review: **12:07 UTC "Kuwait army says Iranian attack causes material damage"** and **13:23 UTC "Iran foreign ministry: U.S. to face consequences for illegal actions."** External sources confirm an active **2026 Iran war**: Iran struck Kuwait's airport Jun 3 (1 dead, 63 hurt), US-Iran exchanges continue, a Pakistan-brokered ceasefire is under strain, and **Iran has closed the Strait of Hormuz — described as the largest oil-supply disruption in market history.** This is a live **weekend gap-risk** for Monday's US open (energy/defense bid, broad risk-off) and crypto is the only venue pricing it now.
- **The risk-off bleed extended again: BTC ~$59,654 (−6.1%), ETH ~$1,550 (−12.7%).** Verified live. BTC has lost $60k decisively (vs ~$60,768 at the 11:40 print); ETH is pinned at its 13-month low. The bearish thesis kept paying, but price is **at/through the major liquidation magnets** — the edge is *manage / wait for a bounce*, not initiate fresh shorts.
- **No A-tier, no B-tier fresh setup. The one live conditional from last slot (TON intraday short) is now expiring (~16:54 EEST) and needs a bounce it likely won't get.** Every other "active" crypto signal is already `tp1_hit/tp2_hit` (managed/realized) or lapsed. Regime: high-volatility **danger**, BTC+ETH downtrend, breadth ~21% above EMA20, **BTC ATR percentile 97 (extreme)**.
- **Crypto reports have gone MORE stale, not less.** Scalp is now **~10.8h** (was ~6h at 11:40 — no regen since), intraday **~23.5h**, swing **~22.8h** — same generator regression flagged in the last 4 reviews (§14). Direction valid; **every execution price must be re-pulled live before any entry.**
- **Net verdict: Crypto = short-biased but NO-CHASE; the actionable edge this slot is risk hygiene + patience, with a NEW overlay of weekend geopolitical gap-risk.** Stand down at BTC ~$60k / ETH ~$1,550. **For Monday's US open: expect a risk-off / energy-and-defense-bid gap if Hormuz/Iran headlines persist over the weekend** — size down, no fresh breakdown shorts into support, no counter-tape longs. **Stocks = no action (closed).** Catalyst layer **context-only (63% unmapped).**

---

## 2. Data Used

**Internal — crypto reports:**
- `data/reports/scalp/2026-06-06_02-38_scalp_report.md` (generated 05:38 EEST, data 02:15 UTC; **~10.8h — stale-context**; regime *high-volatility danger*, BTC+ETH downtrend, breadth above EMA20 **20.83%**, BTC ATR pct **97**). **No A-tier, no B-tier — all watchlist** (top ZRO 59.6, ETH 59.3).
- `data/reports/intraday/2026-06-05_13-54_intraday_report.md` (data 06-05 13:54 UTC; **~23.5h — STALE**).
- `data/reports/swing/2026-06-05_14-34_swing_report.md` (data 06-05 14:34 UTC; **~22.8h — STALE**).
- Stocks reports (intraday 06-05 20:17, swing 19:07, invest 14:55) — **weekend, market closed → context only.**

**Catalyst / narrative:** `data/catalysts/2026-06-06/` — `catalyst_events.jsonl` (**327 rows** today), `narrative_baskets.jsonl` (**3 baskets**), latest `catalyst_cycle_08-25.md` (mtime 11:25). New: catalyst types now include **`exploit_hack` (1)** and **`legal_risk` (8)** — Zcash bug is now categorized.

**LLM packets:** `data/processed/llm_analysis_packet.md` (crypto, ~10.8h), `data/processed/llm_stocks_packet.md` (~17.1h) — present; not the decision driver this slot.

**CLI / DB (read-only, this run):** `active-signals` crypto **7** (TON waiting; NEAR/ADA/EPIC/C intraday/scalp tp-hit managed; ZEC/XLM swing); stocks (closed, context); `signal-stats` crypto week — **headline A/B sample=70, triggered=53, 13W/19L, winrate 24.5%, PF 1.63, avgR 0.23, totalR +12.0**; `detect_untracked_legacy_alerts --since 2026-06-06` → **None (0)**. DB `db/crypto_ai_desk.sqlite` (live, 770 MB, mtime 16:24 — collector writing).

**External (this run — cited §13):** BTC ~$59,654 / ETH ~$1,550 (Yahoo Finance/CoinDesk); Iran–US/Kuwait re-escalation + Strait of Hormuz closure (CNN/NBC/Al Jazeera/RFERL search + Wikipedia *2026 Iran war* WebFetch 200).

**Unavailable / blind:** live tick prints beyond the cited round-numbers; TradingView/Chrome chart verification (not loaded); liquidation heatmaps / order-book / CVD; **fresh crypto execution levels (reports 11–23h stale)**; NBC/RFERL article bodies (HTTP 403 — substituted).

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-06_default_schedule/`.
- `scheduler.log` mtime **16:19:59 EEST** (~4m); latest cycle summary `cycle_01_09-48_summary.md` mtime **11:27:07** (~5.0h). **scheduler.log < 3h → NO DEFER** (defer requires BOTH > 3h; log is fresh).
- Only **one** cycle summary exists today (`cycle_01_09-48`, 11:27). No new cycle since the 11:40 review → **crypto reports did not regenerate.** Scalp slipped from ~6h to **~10.8h**, intraday/swing to **~23.5h / ~22.8h**. Same regression as the last 4 reviews → §14 `TODO-crypto-report-staleness`. **Direction context valid; re-pull all execution levels before any entry.**

---

## 4. What Changed vs Previous Review (Europe 11:30 → pre-US-open 16:20)

- **GEOPOLITICS re-took the lead — the single most important change.** The 11:40 review explicitly **downgraded Iran/Hormuz to "receded, carry-forward LOW-MEDIUM, off the dominant driver set."** That call is now **reversed by fresh events:** Telegram macro prints at **12:07 UTC (Kuwait material damage)** and **13:23 UTC (Iran "consequences for illegal actions")** — both *after* the last review — plus external confirmation of the Jun-3 Kuwait airport attack, ongoing US-Iran exchanges, and the **Strait of Hormuz closure** (largest oil-supply disruption in history). Iran is back to a **HIGH** weekend gap-risk overlay.
- **Bleed extended modestly.** BTC ~$60,768 (11:40 print) → **~$59,654** now; ETH held its **~$1,550** 13-month low. Move still down, runway shrinking, oversold deepening.
- **The only live trigger is lapsing.** At 11:40 the TON intraday short (sell-the-retest 1.551–1.5695, SL 1.592) was the lone live conditional, expiring 13:54 UTC. It is now at/near expiry (**16:54 EEST**) and never got the clean bounce it needed → effectively done.
- **Active crypto signals: 8 → 7.** Mix unchanged in character — TON waiting; NEAR/ADA/EPIC `tp2_hit`, C `tp1_hit` (managed/realized); ZEC/XLM swing. No new B-tier generated.
- **Zcash bug now categorized in the catalyst layer** (`exploit_hack` type appears) — improvement vs the prior "contagion rumor" handling.
- **Untracked legacy alerts still 0** (clean, unchanged) — headline PF/winrate not contaminated.
- **Signal-stats flat:** winrate 24.5%, PF 1.63, totalR +12 (unchanged from 11:40). Direction split notable: **longs n=36 PF 3.14 totalR +15; shorts n=34 PF 0.75 totalR −3** (shorts underperforming despite the bear tape) — small-sample, feedback-only.
- **Report staleness WORSENED** (scalp ~6h → ~10.8h; no regen) vs the prior review.
- **Thesis: direction unchanged (short-biased risk-off); conviction-on-fresh-entries still LOW; NEW high-weight geopolitical gap-risk overlay for the weekend / Monday open.**

---

## 5. Catalyst Coverage

- Raw `catalyst_events.jsonl` (2026-06-06): **327 rows total** · mapped (non-empty symbol) **120** · unmapped **207** · **Unmapped = 63.3%.**
- Catalyst types: other_news 314, **legal_risk 8**, product_launch 2, **exploit_hack 1**, sell_the_news_risk 1, regulatory_sector_headline 1.
- `narrative_baskets` (3): `ai_narrative` (related_beta_rotation, <6h — NEAR/RENDER/TAO/FET; sample headline is **Arthur Hayes turning bearish** → downside rotation, not a long basket); `perps_dex_narrative` (wait_pullback, <24h — HYPE/DYDX/GMX); `momentum_breakout` (wait_pullback, <1h — HEI +14.7%, no confirmed catalyst).
- **⚠ CATALYST MAPPING WEAK THIS RUN (63.3% unmapped > 50%) — use the catalyst layer as CONTEXT, NOT a final decision input.** Top unmapped headlines are macro/equity/AI-policy noise ("Anthropic helping NSA hack China," "Congress 7 new crypto tax bills," "Amazon warehouse robot / AI layoffs," "sell-the-news space stocks"). Same resolver root cause as prior runs (§14 `TODO-catalyst-symbol-resolver`).

---

## 6. Market Landscape

- **Regime (internal, scalp 05:38):** high-volatility **danger**; BTC+ETH downtrend; breadth above EMA20 **20.83%**, above EMA50 18.75%; **BTC ATR percentile 97 (extreme)**. Recommended style: *reduce size or no trade until structure settles.*
- **External levels (verified this run):** **BTC ~$59,654 (−6.1%)**, **ETH ~$1,550 (−12.7%)**. Total crypto mcap ~$2.18T (near Feb lows), −48% from the 2025 ~$4.2T peak.
- **GEOPOLITICAL OVERLAY (NEW, verified):** active **2026 Iran war** — US/Israel vs Iran + Axis; **Iran closed the Strait of Hormuz** (US naval blockade in place) → *largest oil-supply disruption in market history*; Kuwait airport struck Jun 3 (1 dead, 63 injured); fresh strike/rhetoric exchanges today (12:07 / 13:23 UTC). **Implication for Monday US open:** risk-off gap, **energy & defense bid**, oil spike, bid for USD/safe havens; crypto historically trades risk-off on oil/war shocks. Crypto is pricing this *now* over the weekend; equities gap into it Monday.
- **Money flow (internal):** every "strongest" name is down double-digits on the day (PUMP/XPL/AR/ICP/ZEN/FIL/AAVE all −11% to −16%) — the score is ranking *least-bad shorts in a bleed*, not strength. Lone green outlier ALLO +29.8% (low-liquidity, MEXC). Narrative heat: Memes rising (attention 100, DOGE), RWA/AI mixed, L2/DePIN/Gaming quiet.
- **Derivatives:** funding mostly mildly negative across venues, crowding normal/low — deleveraging tape, not a crowded-long blowup; squeeze risk is *reflexive bounce*, not positioning-forced. On-chain: a fresh **20x short on 1,588 BTC ($96.8M)** opened in the past 5h (Lookonchain) — aggressive late shorts add squeeze fuel on any reclaim.
- **Equities (closed, context):** weekend, no cash anchor until Monday. The geopolitical/oil shock is the dominant gap-risk into that open.

---

## 7. Candidate Deep Dives (≤5)

### 7.1 Geopolitical / oil shock — MACRO LANDSCAPE (the dominant driver this slot)
- **External (verified):** active 2026 Iran war; **Strait of Hormuz closed** (largest oil-supply disruption in history); Kuwait airport attack Jun 3 (1 dead, 63 injured); fresh exchanges today (12:07 Kuwait material damage / 13:23 Iran "consequences," both UTC, both *after* the 11:40 review); ceasefire under strain. Sources CNN/NBC/Al Jazeera/RFERL + Wikipedia (WebFetch 200).
- **Price-reaction / chase:** crypto has *already* sold off into the broad risk-off (BTC −6%, ETH −12.7%) but the **geopolitical leg is not separately priced** — a weekend escalation headline can gap crypto lower and will gap **Monday equities** (energy/defense up, broad indices down, oil up). This is a *live, unpriced tail*, not a stale one.
- **Verdict:** **Risk-management overlay, not a trade.** Reduce size, keep dry powder, expect two-way weekend gap risk. For Monday: do NOT chase the equity gap in either direction at the open; let the first 30–60 min print. No crypto long-chase on any relief bounce until BTC reclaims structure.

### 7.2 BTC/USDT — macro anchor — SHORT-biased but NO fresh chase
- **External (verified):** BTC ~$59,654 (−6.1%), below $60k, lowest since Oct 2024; hot-jobs/Fed + Saylor-seller + ETF-outflows backdrop (carry-forward) now layered with the Iran/oil shock.
- **Internal:** scalp watchlist-only; no active BTC signal in the 7 (the prior triggered scalp short has lapsed). ATR pct 97.
- **Price-reaction / chase (§J):** fully reacted; price sits **at the $60k / $59k liquidation magnet** with a fresh $96.8M 20x short stacked on top — shorting weakness here is asymmetric *against* you (squeeze fuel). Would-be-actionable only on a **failed retest of broken structure**, not at market.
- **Verdict:** **NO fresh short at market. Direction down, conviction-on-new-entry LOW.** Re-pull live level (reports 11–23h stale). Watch a reclaim of structure vs a flush through $59k.

### 7.3 ETH/USDT — 13-month low — Zcash-contagion + risk-off — NO chase
- **External (verified):** ETH ~$1,550 (−12.7%), pinned at 13-month low; Zcash counterfeiting-bug DeFi-contagion fear (carry-forward, now `exploit_hack` in catalyst layer) + broad risk-off.
- **Internal:** scalp watchlist short score 59.3, support 1,540, ATR 35.8, volume 0.16x (thin). No active ETH signal.
- **Price-reaction / chase (§J):** fully reacted; ETH *at* $1,550/$1,540 support; thin 0.16x volume = weak breakout confirmation. Fresh short = chasing into a squeeze/capitulation magnet. A $1,500 hold + reclaim is a *manual* nimble mean-reversion watch only.
- **Verdict:** **NO fresh short-chase. Watch $1,540/$1,500 — break = continuation (largely priced), hold = squeeze risk. Manual / no-trade.**

### 7.4 TON/USDT — B / intraday / SHORT — waiting_for_entry — LAPSING
- Active-signals row: score 65.8, entry **1.5512–1.5695**, **SL 1.5919**, tp1 1.5022, status `waiting_for_entry`, **expires 2026-06-06T13:54 UTC (~16:54 EEST — ~30 min left)**.
- **Internal-first:** no fresh TON `news_items`/catalyst match — pure technical breakdown short, regime-aligned.
- **Price-reaction / chase (§J):** the structure is correct (sell-the-retest at 1.551–1.5695, not weakness) but it required a bounce back into the zone that hasn't come; with ~30 min to expiry and the level from a ~23h-stale intraday report, the practical window is gone.
- **Verdict:** **Effectively expired — do NOT arm a fresh market short. If (and only if) price bounces into 1.551–1.5695 before 16:54 EEST, the SL-1.592 retest short is still structurally valid; otherwise let it expire.** Re-pull live level first.

### 7.5 ZEC/USDT — B / swing / LONG — CARRY-FORWARD CONTRADICTION / AVOID
- Active swing **LONG** still surfaces while ZEC is undergoing the confirmed **critical Orchard-pool counterfeiting bug** (disclosed Jun 5, live since May 2022, found via Opus 4.8) and a 38–60% crash — a supply-integrity impairment, not a dip. Now also reflected as `exploit_hack` in the catalyst types.
- **Verdict:** **AVOID / CLOSE. Do not treat the active row as a live long.** Unchanged from 11:40; integrity TODO `TODO-zec-long-contradiction` still open (§14).

---

## 8. Best Candidates Ranked

1. **(Risk overlay, not a trade) Geopolitical/oil gap-risk** — the dominant input this slot; reduce size, keep powder, no open-chase Monday.
2. **TON/USDT intraday short** — *conditional, ~30 min left*: valid only as a sell-the-retest at 1.551–1.5695 (SL 1.592) **if** price bounces there before 16:54 EEST; otherwise let it expire. Re-pull level.
3. *(everything else is manage / avoid — see §9.)*

**No clean fresh A-tier entry; no fresh long; no B-tier setup generated this cycle.** The actionable edge is **risk hygiene + patience under a live geopolitical tail**, not initiation.

---

## 9. Avoid / No Trade

- **Fresh BTC short at market** — at the $60k/$59k liquidation magnet, ATR pct 97, fresh $96.8M 20x short stacked → squeeze-against-you risk. Short failed retests only, never weakness.
- **Fresh ETH short at market** — 13-month low, at $1,540/$1,550 support, thin 0.16x volume. Chasing.
- **Any counter-tape long / green-outlier chase** (HEI +14.7%, ALLO +29.8% MEXC low-liq) — risk-off downtrend, no catalyst, breadth ~21%.
- **ZEC/USDT long** — confirmed counterfeiting bug; fundamental impairment. Close/avoid.
- **Chasing the Monday equity gap in either direction at the open** — let the geopolitical/oil shock print the first 30–60 min before acting.
- **All stocks** — market CLOSED (weekend); planning/watchlist only. Legal-risk flags carry-forward: **SMCI** (8-K indictment, export-control conspiracy) and **UNH** (DOJ antitrust/fraud probe, −16%) — both surfaced as `legal_risk` mis-paired to `/USDT`; re-check before any stock action Monday.

---

## 10. Main Risks

- **Geopolitical weekend gap-risk (HIGH, NEW).** Active Iran war, Hormuz closed (record oil-supply disruption), fresh strike/rhetoric exchanges today. Crypto prices it live over a thin weekend; Monday equities gap into it. Two-way tail — escalation = risk-off/oil-spike; de-escalation/ceasefire headline = sharp relief squeeze.
- **Oversold squeeze / capitulation bounce (HIGH).** BTC ~$60k and ETH ~$1,550 are major support/liquidation levels; ATR pct 97; fresh aggressive late shorts. Short-chasing here is asymmetric against you.
- **Stale execution levels (HIGH).** Reports 11–23h old, regen failed again. Every §7 price must be re-pulled live before action. Dominant operational risk.
- **ZEC integrity / contagion (MEDIUM-HIGH).** Confirmed counterfeiting bug; "similar-hidden-flaw" fear is an ETH/DeFi driver; desk still carrying a ZEC *long* row.
- **Catalyst layer unreliable (MEDIUM).** 63.3% unmapped; tail is macro/equity/AI-policy noise. Context-only.
- **Ingest CLI risk (LOW).** If `ingest_enriched_review_sources` fails it is logged here and does not block the review.

---

## 11. Action Plan — next 4 hours (US-closed weekend → into Monday open)

1. **Re-pull live BTC/ETH/TON levels** before any execution — reports are 11–23h stale.
2. **Treat the geopolitical/oil shock as the master risk control:** reduce size, keep dry powder, expect two-way weekend gap risk. Watch for Iran/Hormuz headlines; a ceasefire/de-escalation print = sharp relief squeeze, an escalation = further risk-off/oil-spike.
3. **BTC:** no fresh short at $60k/$59k; watch reclaim-of-structure vs flush through $59k. The lapsed scalp short is closed/realized.
4. **TON intraday short:** arm only as sell-the-retest at 1.551–1.5695 (SL 1.592) **if** price bounces there before ~16:54 EEST; otherwise let it expire. No market-sell into weakness.
5. **ETH:** watch $1,540/$1,500 — hold+reclaim = manual nimble scalp-long *watch* only; break = continuation (largely priced). No fresh short.
6. **ZEC:** treat the active swing long as flat/closed — do not add or defend (counterfeiting bug).
7. **Do not initiate any fresh breakdown short at market** into support/liq levels over a thin, headline-driven weekend.
8. **For Monday US open:** expect a risk-off / energy-and-defense-bid gap if Iran/Hormuz persists; do NOT chase the open — let the first 30–60 min print, re-read the desk on Monday's fresh reports.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** No fresh entry — BTC/ETH at support/liquidation magnets, ATR pct 97. Manage/closed only; sell retests, not weakness. Direction short, conviction-on-new-entry LOW.
- **Crypto intraday:** Short-biased but no-chase. **TON** valid only as sell-the-retest at 1.551–1.5695 (SL 1.592) **if** it bounces before ~16:54 EEST expiry; re-pull level (23h stale). No other live trigger.
- **Crypto swing:** **ZEC long = AVOID/CLOSE** (counterfeiting bug). XLM swing long (tp1_hit, expires 06-07) — runner only, no add into the danger regime. No fresh swing initiation.
- **Stocks (all modes):** No action — market CLOSED (weekend). Context only; SMCI/UNH legal flags + the geopolitical/oil gap-risk noted for Monday's open.

---

## 13. Sources

- [Bitcoin USD (BTC-USD) Price — Yahoo Finance](https://finance.yahoo.com/quote/BTC-USD/history/) — 2026-06-06, **single_source** (live: BTC ~$59,654 −6.12%; ETH ~$1,550 −12.67%).
- [Iran attacks Kuwait, trades strikes with U.S. in test to ceasefire — NBC News](https://www.nbcnews.com/world/iran/iran-attacks-kuwait-strikes-us-ceasefire-peace-talks-trump-rcna348213) — 2026-06-03, **single_source** (search snippet; WebFetch HTTP 403 — body not retrieved; Kuwait airport hit, 1 killed/63 injured, US-Iran exchanges).
- [Iranian drone attack kills Indian citizen in Kuwait after US strikes Qeshm — Al Jazeera](https://www.aljazeera.com/news/2026/6/3/iranian-drone-hits-kuwaits-main-airport-after-us-strikes-qeshm-island) — 2026-06-03, **single_source** (search snippet).
- [Iran, US Exchange Attacks As Tensions In Gulf Rise — RFE/RL](https://www.rferl.org/a/iran-united-states-drone-attacks-kuwait-peace-talks/33771717.html) — 2026-06-03, **single_source** (search snippet; WebFetch HTTP 403 — body not retrieved).
- [June 2-3, 2026 — Iranian attacks on Kuwait airport, Bahrain — CNN (live)](https://www.cnn.com/2026/06/02/world/live-news/iran-trump-israel-lebanon-war-intl-hnk) — 2026-06-02/03, **single_source** (search snippet).
- [2026 Iran war — Wikipedia](https://en.wikipedia.org/wiki/2026_Iran_war) — accessed 2026-06-06, **single_source** (WebFetch HTTP 200; US naval blockade, Iran closed Strait of Hormuz = "largest supply disruption in history of the global oil market," financial-market volatility, ceasefire under strain).
- Internal (no external claim): scalp report 2026-06-06_02-38; active-signals / signal-stats / untracked-detector CLI (this run); `catalyst_events.jsonl` + `narrative_baskets.jsonl` + `catalyst_cycle_08-25.md` (2026-06-06); `news_items` fresh Telegram macro prints 12:07 / 13:23 UTC (t.me/WalterBloomberg), BTC 20x-short on-chain print 09:59 UTC (t.me/lookonchain).
- Carry-forward (verified prior reviews, not re-fetched this slot): BTC <$60k hot-jobs/Saylor/ETF-outflows; Zcash Orchard counterfeiting bug (CoinDesk/Decrypt, Jun 5).

---

## 14. Fix Requests / TODO

### TODO-crypto-report-staleness
- **issue:** Crypto scalp + intraday report generators continue to fail to regenerate; no new cycle since 11:27, so scalp slipped from ~6h to ~10.8h and intraday/swing to ~23.5h/~22.8h. Same regression flagged in the last 4 reviews.
- **evidence:** only `cycle_01_09-48_summary.md` (mtime 11:27) exists for 2026-06-06; scalp report mtime 06-06 05:38, intraday 06-05 13:54 UTC, swing 06-05 14:34 UTC; `scheduler.log` touched 16:19 with no new cycle output.
- **suggested manual fix:** profile the scalp/intraday CLI fetch loop; add per-exchange fetch timeouts + partial-result fallback so one hung call can't blow the 2700s budget; cache `exchangeInfo`; raise/segment the step timeout.
- **priority:** high
- **first observed:** carried from 2026-06-05 23:25 / 06-06 04:45 / 11:40 EEST; reconfirmed 2026-06-06 16:24 EEST.

### TODO-zec-long-contradiction
- **issue:** An active B swing **LONG** on ZEC/USDT remains in `active-signals` while ZEC is undergoing a confirmed critical Orchard-pool **counterfeiting** bug + 38–60% crash. A supply-integrity exploit should hard-invalidate / force-expire a long irrespective of price.
- **evidence:** `active-signals --asset-class crypto` ZEC/USDT swing long row; external CoinDesk/Decrypt (Jun 5) confirm bug + crash; catalyst layer now tags an `exploit_hack` event but the long row persists.
- **suggested manual fix:** (a) confirm the invalidation/stop sweep transitions longs whose price blew through `invalidation`; (b) add a catalyst-driven hard-kill that flips any same-symbol active signal to `invalidated` on `legal_risk`/`exploit_hack`/security events.
- **priority:** high
- **first observed:** 2026-06-06 11:40 EEST; reconfirmed 16:24 EEST.

### TODO-catalyst-symbol-resolver
- **issue:** 63.3% of catalyst_events are unmapped (empty symbol); tail includes macro/equity/AI-policy headlines that don't resolve to crypto tickers and equity legal items mis-paired to `/USDT` (UNH/USDT, SMCI/USDT). Recurring ~63–73% unmapped over many runs.
- **evidence:** `data/catalysts/2026-06-06/catalyst_events.jsonl` total=327, mapped=120, unmapped=207 (63.3%); top unmapped: "Anthropic Is Helping the NSA Hack China," "Congress Gets 7 New Crypto Tax Bills," "Amazon warehouse robot / AI layoffs."
- **suggested manual fix:** add an asset-class gate so equity/macro headlines don't enter the crypto feed as `<TICKER>/USDT`; route unmapped equity-class events out of the crypto trading-day JSONL; add a relevance threshold so generic macro noise isn't logged as a tradable catalyst.
- **priority:** medium
- **first observed:** recurring; reconfirmed 2026-06-06 16:24 EEST.

### TODO-geopolitical-macro-coverage
- **issue:** The dominant market driver this slot — an active Iran war with the Strait of Hormuz closed and fresh weekend strike headlines — is reaching the desk only as raw Telegram `news_items` (WalterBloomberg geopolitical prints) with **empty `detected_symbols`** and no narrative-basket / macro-risk synthesis. A war/oil shock of this magnitude should surface as a structured macro-risk signal, not be left to manual review discovery.
- **evidence:** `news_items` rows 2026-06-06 12:07 UTC ("Kuwait army says Iranian attack causes material damage") and 13:23 UTC ("Iran foreign ministry: U.S. to face consequences") both have `detected_symbols=[]`; no geopolitical/oil narrative basket exists in `narrative_baskets.jsonl`; the 11:40 review had even downgraded Iran as "receded."
- **suggested manual fix:** add a geopolitical/macro-risk basket (war, Strait of Hormuz, oil-supply, sanctions) that maps to a BTC/ETH risk-off bias and a defense/energy equity tilt, so major macro shocks get a structured signal instead of relying on manual catch.
- **priority:** medium
- **first observed:** 2026-06-06 16:24 EEST.
