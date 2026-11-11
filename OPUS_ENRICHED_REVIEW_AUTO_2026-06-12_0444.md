# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:44 EEST

_Slot: 04:30 crypto overnight / Asia review · Friday 2026-06-12 · ~21:44 ET Thu / Asia mid-session. Focus: overnight crypto action, Asia-session BTC/ETH regime, alt breadth & RS leadership, new overnight A/B signals, overnight news/macro into Europe. US stocks **closed** → stock signals are planning/watchlist context only; crypto is the live actionable class. Advisory-only, read-mostly — no auto-trade, no code edits, paper-trading. §14 TODOs only, no fixes._

## 1. Executive Summary

**Overnight the de-escalation thesis that drove yesterday's risk-on US close has been challenged — Iran headlines flipped back toward escalation, and crypto is chopping, not trending.** The fresh catalyst feed is dominated by Iran re-escalation lines ("IRAN SAYS US STRIKES RENDER CEASEFIRE MEANINGLESS", "EXPLOSION HEARD NEAR SIRIK COAST", "TRUMP SEEKS STRONGER IMPACT FROM IRAN STRIKES"). External confirmation: markets are repricing **from a ceasefire to a "long grind"**, Asia equities broadly lower, oil +~2% but still < $100 (CNBC, web §13). This is a risk-off macro overlay sitting on top of an already-fragile crypto tape.

**Crypto regime: range/chop with a selective alt-RS rotation underneath.** Desk read (data 23:45 UTC): **BTC trend range, ETH trend range, "transition (mixed)"**, btc_atr_percentile 43 (normal vol), recommended style **"selective only; demand clean invalidation."** The constructive wrinkle vs yesterday's close: **alt breadth firmed to 68.3% > EMA20** (up from ~47.8% at the 23:24 post-close review) / 46.3% > EMA50 — overnight alts are rotating, not bleeding. But the leaders are mostly **already extended**: ID +30%, STG +56% (flagged overextended), LUMIA +37%, CRV +21%, PYTH +22%. External price check: **BTC ~$62,561 (+2.5%/24h), ETH ~$1,649 (+2.0%/24h, still stuck < $1,700)** (web §13).

**The structural headwind is intact and decisive: ETF outflows.** Spot BTC+ETH ETFs have bled **$4.33B across a 13-session streak**, with institutional selling running ~450% of daily mined supply (~2,000 BTC/day), "capping recovery attempts despite improved macro" (web §13). So the overnight alt pop is **relief/rotation, not a trend turn** — until **BTC reclaims and holds > $63.5K**, treat RS-leader strength as **sellable / wait-pullback**, not chase.

**No A-tier crypto signals this run** — all 8 active crypto signals are **B-tier longs**, and **most have already realized** (ATOM tp2, CHIP tp2, ALLO/BANK/BABY/CRV-scalp tp1). The only fresh-ish actionable B's are **CRV/USDT (swing, triggered, OI-confirmed)** and **ID/USDT (intraday, triggered, but +30% extended & thin volume 0.12×)**. System health clean: untracked-alert detector **0**, scheduler fresh (~1.6h).

**Routed verdict (this decision window only — never a stop command):**
- **Best long-watch:** **CRV/USDT** — desk score 91.6, RS +17% vs BTC, OI-confirmed (price↑+OI↑, funding +0.0001, L/S 1.66, crowding normal). Already ran +21% → **only on a held pullback into 0.2443–0.2481, invalidation 0.2396**, with BTC holding > $62K. No fresh chase at highs.
- **Best short-watch:** **none clean.** ETH (laggard < $1,700) is the relative-weakness short-watch **only on a failed bounce / rejection at $1,700 with BTC losing $61K**. Thin laggards (HOME/OPN/MORPHO/TRX) are squeeze-prone low-float — avoid.
- **Best catalyst-backed:** **HYPE/USDT** — Kalshi launched HYPE perpetuals (exchange_listing, importance 0.71–0.75), perps_dex narrative primary, fresh < 6h. Playbook is **wait_pullback** and price has largely reacted → watch, don't chase.
- **What to avoid:** chasing extended RS-leaders at the highs (ID +30%, STG +56% overextended, LUMIA +37%) into persistent ETF outflows + Iran risk; ETH longs < $1,700; thin low-float momentum dumps; **fresh stock entries** (US closed; Iran re-escalation = gap-down reopen risk).
- **What would change the view:** BTC reclaim + hold **> $63.5K** on firm breadth → RS-leader pops become trend longs; a clean Iran **de-escalation** headline → risk-on revival; **BTC loses $61K** → flip to risk-off shorts on laggards.

**System health:** untracked-alert detector **clean (0)** — no PART-1 regression. Scheduler **fresh** (~1.6h). Catalyst mapping **weak again — 81.4% unmapped** → catalyst layer is context, not a decision input. §14 TODOs persist (catalyst mapper; stock A-tier 0/6 wins; stock C-tier losing book).

## 2. Data Used

- Crypto **scalp** — `data/reports/scalp/2026-06-11_23-57_scalp_report.md` (data 23:45 UTC) — **fresh** (~4.7h, near top of band but the live scalp source).
- Crypto **intraday** — `data/reports/intraday/2026-06-12_00-02_intraday_report.md` (data 23:45 UTC) — **fresh** (~4.6h).
- Crypto **swing** — `data/reports/swing/2026-06-11_14-18_swing_report.md` — **stale** (~14.3h; > 14h → excluded from fresh swing verdict, planning context only; flagged §3).
- **Stocks** intraday/swing/invest — `..._00-05_` / `..._14-23_` / `..._14-27_` — **closed-market / carry-forward** (planning only; US cash closed overnight).
- Catalysts — `data/catalysts/2026-06-12/` (events.jsonl + narrative_baskets.jsonl + `catalyst_cycle_00-02.md`, mtime 03:02) — **fresh** (~1.7h). `catalyst-scan` NOT re-run (dir present).
- LLM packets present: `data/processed/llm_analysis_packet.md`, `llm_stocks_packet.md`.
- CLI (this run): `active-signals` crypto (8) + stocks (50); `signal-stats` crypto + stocks; `detect_untracked_legacy_alerts` (**clean — 0 untracked**).
- External: WebSearch ×2 (BTC/ETH overnight June 11–12; Iran escalation + market reaction), WebFetch ×2 attempts — analyticsinsight June 11 **opened & cited §13**; CNBC Iran escalation **HTTP 403 (search-snippet only, cited as single_source)**. External research **AVAILABLE** this run.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime **03:06** (~1.6h) — **fresh**. Latest cycle summary `cycle_07_02-49_summary.md` mtime **03:06** (~1.6h) — **fresh**. Crypto monitor log actively writing (**04:36**, ~8 min). Both well inside the 3h defer threshold → **review proceeds normally**.
- Crypto scalp/intraday + catalysts are **fresh** (~1.7–4.7h).
- **Stale flag:** crypto **swing** report is ~14.3h (> 14h) → excluded from the fresh swing verdict; used only as planning context. Stock swing/invest (~14h) likewise planning-only (and market closed regardless).
- **Stocks data is closed-market.** The 50 active stock signals are last-session leftovers (mostly C-tier `waiting_for_entry`/`triggered` from Thursday's US session). They are **planning/watchlist context only** overnight, with gap-down reopen risk if Iran escalation holds into Friday's RTH.

## 4. What Changed vs Previous Review

Prior: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-11_2324.md` (post-close final daily review, 23:24 EEST Thu).

- **Macro thesis flipped from de-escalation → re-escalation.** 23:24 wrapped the day on an Iran **de-escalation** risk-on close (Russell +3.06%, Nasdaq +2.53%). Overnight the catalyst feed + web now show **escalation** ("ceasefire meaningless", Trump pressing for stronger strikes; markets repricing to a "long grind", Asia lower). This is the single biggest change and it is **risk-negative** into Europe.
- **Crypto alt breadth firmed** 47.8% → **68.3% > EMA20** — overnight alts rotated up, an improvement vs the post-close "narrowing breadth" read. But it is RS-leader-led and **extended**, not a BTC-led trend turn.
- **BTC/ETH roughly unchanged / still capped.** BTC ~$62.8K → ~$62.5K, ETH ~$1.647K → ~$1.649K (still < $1,700). The relief is **not** confirming; **ETF outflows extended to a 13-session, $4.33B streak** (web §13) — institutional conviction still absent.
- **Carried crypto B-longs largely realized.** Since 23:24: **ATOM advanced to tp2_hit** (was `waiting_for_entry`), ALLO/BANK/BABY/CRV-scalp at tp1, CHIP tp2. ID intraday still `triggered`. → manage/trail, not fresh entries.
- **Catalyst mapping** still weak: 80.6% → **81.4% unmapped**. TODO persists.
- **Untracked-alert detector** still **clean (0)** — no regression.
- Prior best long-watch (ATOM on held pullback) has **already advanced to tp2** → thesis confirmed and largely played out; rotate the long-watch to **CRV** (next OI-confirmed RS-leader not yet exhausted).

## 5. Catalyst Coverage

- Total `catalyst_events` today (`2026-06-12/catalyst_events.jsonl`): **500** scanned this cycle.
- Mapped (non-null symbol): **93**.
- Unmapped (null symbol): **407** → **81.4% unmapped**.
- `narrative_baskets`: **6** (perps_dex_narrative, ai_narrative, binance_ecosystem_teaser, delisting_thin_liquidity, rwa_narrative, momentum_breakout).
- **⚠ catalyst mapping weak this run — use the catalyst layer as context, not a final decision input.** (>50% unmapped, persistent across every run.)
- Top 3 unmapped / basket-level headlines (context only):
  1. "SPACEX'S IPO DRAWS AT LEAST $5B ORDER FROM BLACKROCK, SOURCES SAY" (t.me/WalterBloomberg — rumour).
  2. "TRUMP SEEKS STRONGER IMPACT FROM IRAN STRIKES, SOURCES SAY" (t.me/WalterBloomberg — macro, basket).
  3. "Federal Reserve's latest financial accounts still pretend crypto doesn't exist" (CryptoBriefing — regulatory, basket).
- Mapped top catalysts: XRP/USDT (Ripple CEO vs Dimon over Clarity Act, importance 0.78–0.80), HYPE/USDT (Kalshi perps + SpaceX perps pricing, 0.71), BTC/USDT (Nakamoto sells BTC, buyback, 0.71).

## 6. Market Landscape

- **BTC** ~$62,561 (+2.5%/24h), trend **range**; key reclaim **$63.5K**, downside pivot **$61K** (web §13 + desk).
- **ETH** ~$1,649 (+2.0%/24h), trend **range**, still capped **< $1,700** (relative laggard).
- **Alt breadth:** 68.3% > EMA20 / 46.3% > EMA50 — firm but EMA50 still sub-50% (rotation, not full risk-on).
- **Volatility:** btc_atr_percentile 43 — normal.
- **Leaders (RS vs BTC):** CRV +17%, FIDA +15%, ID +27%, PYTH +18%, EPIC +17%, DEXE +13%, STG +53% (overextended), LUMIA +34%. **Laggards:** HOME, OPN, MORPHO, BABY, TRX (short bias, thin).
- **Derivatives:** CRV price↑+OI↑ (funding +0.0001, L/S 1.66, crowding normal) — clean fresh positioning. FIDA price↑+OI↑ but funding negative (−0.0012) — short-covering-flavored.
- **Narratives:** Iran war escalation (macro risk-off overlay, dominant); perps_dex (HYPE/Kalshi, wait_pullback); AI rotation (NEAR/RENDER/TAO/FET, related-beta); RWA (ONDO/XLM, multi-week); momentum_breakout (STG/LUMIA/EPIC — **avoid_chase**).
- **Stocks:** closed overnight. Carry-forward: Thursday closed risk-on, but Iran re-escalation overnight = **gap-down reopen risk** into Friday RTH. Stock signal book remains the structurally weaker book (A-tier 0/6 wins, C-tier −24R; see §12 / §14).

### Market Mood / Risk Routing      (REQUIRED — PART 4)
- **Crypto mood:**           **chop / mixed** (range BTC/ETH + firm-but-extended alt rotation, under a fresh Iran risk-off overlay and a 13-session ETF-outflow drag)
- **Stocks mood:**           **closed** (overnight; carry-forward risk-on but gap-down reopen risk)
- **Dominant narrative:**    Iran war re-escalation (macro risk-off); secondary: perps_dex (HYPE), AI rotation, RWA
- **Preferred side now:**    **wait-for-trigger** — selective RS-leader longs *only on pullback*; shorts only on *failed bounce* of laggards (but thin = avoid)
- **Best long candidate:**   **none clean now — CRV/USDT** long-watch; trigger: held pullback into 0.2443–0.2481 (invalidation 0.2396), BTC > $62K
- **Best short candidate:**  **none clean — ETH/USDT** short-watch; trigger: failed bounce / rejection at $1,700 with BTC losing $61K (avoid thin low-float laggards)
- **Best catalyst-backed candidate:** **HYPE/USDT** (Kalshi perps listing) — wait_pullback, price reacted → watch only
- **What to avoid:**         chasing ID/STG/LUMIA at extended highs into ETF outflows + Iran risk; ETH longs < $1,700; thin delisting/low-float dumps; fresh stock entries (closed + gap risk)
- **What would change the view:** BTC reclaim+hold > $63.5K (→ trend longs) · clean Iran de-escalation (→ risk-on) · BTC loses $61K (→ risk-off shorts)

## 7. Candidate Deep Dives        (≤ 5)

### 1. CRV/USDT — B swing(65.1, triggered) + scalp(68.5, tp1_hit) — long — **BEST LONG-WATCH**
- Desk score 91.6 (top of flows), RS vs BTC +17%, 24h +21%, volume 0.45×. OI-confirmed: price↑+OI↑, funding +0.0001, L/S 1.66, crowding normal.
- Internal records: active swing B `triggered` (entry 0.2443–0.2481, invalidation 0.2396, expires 2026-06-18); scalp B already tp1_hit. No fresh adverse `news_items`/catalyst for CRV.
- **Price already reacted?** Yes (+21% over 24h). **Chasing?** Entry at current highs would be chasing. **Retest structure?** Pullback into the 0.2443–0.2481 zone is the clean re-entry. **Overextended (>2 ATR from EMA20)?** Elevated but OI-confirmed, not parabolic. **Entry now late?** Yes at the high; no on a held pullback. **Actionable level:** 0.2443–0.2481 holding > 0.2396.
- **Mood-aligned?** Yes for a *selective* RS-leader long. **Side:** long, **wait-for-trigger** (pullback). **Invalidates:** loss of 0.2396, or BTC < $61K. **Chase-risk:** yes if entered at spot. **Catalyst:** none required (pure RS/flow); no contradiction.

### 2. ID/USDT — B intraday(65.3, triggered) — long — **CHASE-RISK / DEMOTE**
- Desk score 90.5, RS vs BTC +27%, 24h **+30%**, **volume only 0.12×** (thin participation). Active intraday B `triggered`, **expires today 14:01 EEST**.
- **Price already reacted?** Strongly (+30%). **Chasing?** Yes — buying a +30% thin-volume pop is a chase. **Retest?** Needs a deep pullback to be clean. **Overextended?** Likely > 2 ATR. **Entry now late?** Yes. **Actionable level:** only a sharp pullback that holds the entry band; otherwise let it expire.
- **Mood-aligned?** Marginal (extended into risk-off macro). **Side:** long but **avoid fresh** — manage if already in. **Invalidates:** loss of entry band / failure to hold the breakout. **Chase-risk:** high (thin volume + parabolic). **Catalyst:** none confirmed → pure momentum, treat as such.

### 3. ATOM/USDT — B swing(67.9, **tp2_hit**) — long — **MANAGE / TRAIL**
- RS-leader +14%, OI-confirmed; prior review's long-watch — has now **advanced to tp2_hit**. Thesis confirmed and largely played out.
- **Price reacted?** Yes (ran to tp2). **Chasing?** Yes at spot. **Actionable:** **manage/trail the existing position**, no fresh entry. **Side:** long (held). **Invalidates:** loss of 1.9028. **Chase-risk:** yes for new entries. No adverse catalyst.

### 4. BABY/USDT — B swing(65.1, tp1_hit) — long — **CONTRADICTION / MANUAL REVIEW**
- **Contradiction risk:** held as a **long** B (tp1_hit) yet the live flows list ranks **BABY among the weakest (short bias, 24h −1.42%, RS vs BTC −4.70%)**. The long signal looks stale vs current relative weakness.
- **Price reacted?** Long thesis already took tp1 then faded. **Actionable:** **no fresh adds; trail/tighten the tp1 runner; manual review** of whether the signal should flip/expire. **Side:** flat-to-exit. **Invalidates:** loss of 0.016545. **Chase-risk:** n/a. **Catalyst:** none — direction conflict is technical/staleness, logged as a §14 watch-item.

### 5. HYPE/USDT — catalyst-backed (perps_dex narrative primary) — **CATALYST-WATCH**
- Catalyst: **Kalshi launched HYPE perpetuals** — "first regulated platform to list a Hyperliquid-native perp" (exchange_listing, importance 0.71–0.75, single_source); plus SpaceX-perps pricing chatter. Basket freshness < 6h, playbook **wait_pullback**.
- Internal: appears in `catalyst_events` + perps_dex basket; no active HYPE signal in the book.
- **Price reacted?** Likely largely priced (listing already live). **Chasing?** Yes at spot. **Retest?** wait_pullback per playbook. **Actionable level:** a pullback that holds + perps-volume follow-through; **verify no sell-the-news**. **Side:** long-watch (catalyst). **Invalidates:** failure to hold post-listing range / narrative fade. **Chase-risk:** moderate (listing-pop). **Verification:** single_source — demote to "watch" until corroborated.

## 8. Best Candidates Ranked

No clean fresh-entry candidate this window (all live A/B longs are extended or already realized). Per PART 9, the routed watch-list:

1. **Best long-watch — CRV/USDT.** Trigger: **held pullback into 0.2443–0.2481, above invalidation 0.2396, with BTC holding > $62K.** OI-confirmed RS-leader, score 91.6. Highest-conviction watch.
2. **Best short-watch — ETH/USDT.** Trigger: **failed bounce / rejection at $1,700 while BTC loses $61K.** Relative laggard < $1,700. Low conviction; avoid thin low-float laggards (squeeze-prone).
3. **Best catalyst-watch — HYPE/USDT.** Trigger: **post-listing pullback that holds + perps-volume follow-through; corroborate the Kalshi listing beyond single_source and confirm no sell-the-news.** wait_pullback playbook.

## 9. Avoid / No Trade            (this decision window only — scanner keeps running)

- **STG/USDT** — +56%/24h, flagged **overextended**, momentum_breakout basket `avoid_chase`. No catalyst. Avoid chasing.
- **LUMIA/USDT** — +37%, **ID/USDT** at spot (+30% thin) — extended momentum into a risk-off macro tape; no fresh chase.
- **ETH longs < $1,700** — relative laggard; wrong side until $1,700 reclaims.
- **Thin low-float laggards** (HOME/OPN/MORPHO/TRX) — squeeze-prone both ways; avoid.
- **Fresh stock entries** — US closed; Iran re-escalation = gap-down reopen risk; the stock book is structurally weak (A-tier 0/6, C-tier −24R). Plan, don't pre-position.
- _This is a current-window caution only. Scanner, candidate generation, tracking, and monitors continue uninterrupted._

## 10. Main Risks

- **Iran re-escalation** is the dominant overnight risk — a sharp headline could gap risk assets down into Europe; oil > $100 would amplify the inflation/rate overhang (June 17 FOMC ahead).
- **Persistent ETF outflows** (13 sessions, $4.33B) cap every crypto bounce — the overnight alt pop can fade fast if BTC rejects $63.5K.
- **Extended RS-leaders** (ID/STG/LUMIA) are mean-reversion risk; chasing late = poor R.
- **Stocks gap risk** on the Friday reopen if escalation holds.
- **Catalyst mapping weak (81.4% unmapped)** — symbol-level catalyst conviction is low this run; treat catalysts as context.
- **Ingest note:** see §13/§14 for source-ingest result; CNBC fetch returned 403 (search-snippet citation only).

## 11. Action Plan — next 4 hours (into Europe)

1. **Watch BTC $63.5K (reclaim) and $61K (breakdown).** Reclaim+hold → upgrade CRV/RS-leader longs to trend; breakdown → flip to laggard short-watch.
2. **CRV/USDT:** wait for a pullback into 0.2443–0.2481; only then a long with invalidation 0.2396. No chase at highs.
3. **Manage realized B-longs** (ATOM tp2, CHIP tp2, ALLO/BANK/BABY/CRV-scalp tp1) — trail stops, bank into strength; **BABY** flat-to-exit (contradiction).
4. **HYPE:** monitor for a wait_pullback entry + corroborate the Kalshi listing; do not chase the listing pop.
5. **Track the Iran headline tape** — a clean de-escalation re-opens risk-on; further escalation = stay defensive / favor laggard shorts on failed bounces.
6. **Stocks:** planning only — pre-mark AMD (C 79.9)/JPM/LLY levels for Friday RTH, but no overnight pre-positioning given gap risk.

## 12. Final Verdict per Mode

- **Crypto scalp:** _selective / low-confidence._ Leaders extended; only CRV-type OI-confirmed pullbacks. No fresh chase. (Scalp horizon-mismatch caveat per report — data collection ongoing.)
- **Crypto intraday:** _wait-for-trigger._ ID `triggered` but extended/thin → manage only; new intraday longs need a held pullback + BTC > $62K.
- **Crypto swing:** _carry-forward / manage._ Swing report stale (>14h); existing swing B-longs (ATOM/CHIP/CRV/ALLO/BANK) mostly realized → trail. No fresh swing entry off stale data.
- **Stocks intraday/swing/invest:** _planning only — market closed._ Gap-down reopen risk; no overnight entries. Stock book structurally weak (A-tier 0/6 wins).
- **Overall:** **wait-for-trigger / selective RS-leader longs on pullback.** No clean fresh entry this window; CRV is the cleanest watch. Scanner continues.

## 13. Sources

- [Crypto Prices Today: Bitcoin Climbs Near $62,561… ETH at $1,649 — Analytics Insight, June 11, 2026](https://www.analyticsinsight.net/price-analysis/crypto-prices-today-bitcoin-climbs-near-62561-as-cpi-clears-eth-at-1649-as-japan-megabanks-target-stablecoin-launch) — **primary price/ETF source, WebFetch opened.** BTC $62,561 (+2.5%), ETH $1,649 (+2.0%), ETF outflows $4.33B/13 sessions, May CPI 4.2%, June 17 FOMC. _verification: single_source._
- [Investors brace for a 'long grind' as Iran war escalation dims hopes of an early end — CNBC, June 11, 2026](https://www.cnbc.com/amp/2026/06/11/iran-war-us-trump-strikes-centcom-oil-investors.html) — markets repricing ceasefire→long grind; Asia lower; oil +~2% < $100. _verification: single_source (WebFetch 403 — search-snippet only; corroborated by catalyst feed headlines)._
- [Bitcoin and ethereum prices today, Thursday, June 11, 2026 — Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-thursday-june-11-2026-prices-lifting-off-low-opening-figures-114705725.html) — BTC opened $61,456 → $63,020 intraday; ETH $1,620 → $1,660. _verification: single_source._
- Internal: `catalyst_cycle_00-02.md`, `narrative_baskets.jsonl` (2026-06-12), `signal-stats`/`active-signals` CLI, `detect_untracked_legacy_alerts` (clean).

## 14. Fix Requests / TODO

### TODO-catalyst-mapper
- **issue:** Catalyst symbol-mapping weak again — 81.4% of events unmapped (407/500), persistent across every run.
- **evidence:** `data/catalysts/2026-06-12/catalyst_events.jsonl` → mapped 93 / unmapped 407; `catalyst_cycle_00-02.md` "other_news: 482".
- **suggested manual fix:** strengthen the symbol/entity resolver in the catalyst layer (alias coverage, headline-NER) so basket/macro headlines map to tickers; until then catalyst layer is context-only.
- **priority:** medium
- **first observed:** carried (recurring); re-confirmed 2026-06-12 04:44 EEST

### TODO-stock-atier-anemic
- **issue:** Stock A-tier remains anemic — n=8, 0 wins / 6 losses, PF 0.0, totalR −6.0 (avgR −0.75). A-tier should be the strongest bucket, not the worst.
- **evidence:** `signal-stats --asset-class stocks` By tier: `tier=A n=8 wins=0 losses=6 PF=0.0 totalR=-6.0`.
- **suggested manual fix:** audit stock A-tier promotion gating (over-promotion); consider raising the A threshold or adding confirmation before A-tier on stocks.
- **priority:** high
- **first observed:** carried; re-confirmed 2026-06-12 04:44 EEST

### TODO-stock-ctier-losing-book
- **issue:** Stock C-tier research book bleeding — n=308, PF 0.61, totalR −24.0 (avgR −0.098).
- **evidence:** `signal-stats --asset-class stocks` C-tier Watchlist row + By tier `tier=C`.
- **suggested manual fix:** review stock C-tier intraday scoring/filters (mode=intraday −10R, swing −10R, invest 0 wins/3 losses); tighten or down-weight the consistently-losing buckets. Research-only (not Telegram-actionable) but worth a scoring pass.
- **priority:** medium
- **first observed:** carried; re-confirmed 2026-06-12 04:44 EEST

### TODO-baby-direction-contradiction
- **issue:** BABY/USDT held as an active **long** B (tp1_hit) while live flows rank it among the **weakest / short-bias** (24h −1.42%, RS −4.70%) — a stale long not invalidating against current relative weakness.
- **evidence:** `active-signals --asset-class crypto` (BABY long, tp1_hit) vs `scalp_report` §2 Weakest Symbols (BABY short bias).
- **suggested manual fix:** investigate whether realized-then-faded longs should auto-tighten/expire when the symbol flips to relative-weakness; verify the invalidation/trail logic on post-tp1 signals.
- **priority:** low
- **first observed:** 2026-06-12 04:44 EEST
