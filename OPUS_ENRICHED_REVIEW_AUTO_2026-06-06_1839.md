# Opus Enriched Review — US-open reaction review (Saturday → crypto-only) — Auto Cycle 18:39 EEST

- **Generated:** 2026-06-06 18:39 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`, **US open reaction review** slot 18:30, executing `opus-enriched-review-4h/SKILL.md`).
- **⚠ It is SATURDAY — US & EU cash equities are CLOSED.** There is no live US open to react to. This slot pivots to: (a) **crypto is the only live market pricing the weekend**, and (b) **gap-risk staging for Monday's actual US open.** All stock signals = planning/watchlist context only.
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-06_1624.md` (pre-US-open decision review, 16:24 EEST, ~2.25h ago — see §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). Verified this run: **BTC ~$61,924 (−2.7% 1d), ETH ~$1,656 (−6.8% 1d)** (Blockchain.com/Coinbase aggregate via search) — a modest bounce off the 16:24 lows (~$59.6k / ~$1,550) but still downtrend, ETH still pinned near its 13-month low. **Zcash Orchard counterfeiting bug** confirmed across 6+ outlets + WebFetch HTTP 200 on news.bitcoin.com (ZEC −41–50%, low ~$324, unprovable residual risk). **US–Iran conflict** carried forward from 16:24 (Strait of Hormuz closure, Kuwait airport strike) — no fresh escalation print this 2.25h window.
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; price/structure = local OHLCV/ATR/EMA report fields + cited external prints.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

- **The dominant regime is unchanged and bearish: broad risk-off + a crypto-specific credibility shock (Zcash).** BTC and ETH remain in confirmed downtrend, altcoin breadth above EMA20 is **16.7%** (worsened from ~21% at 16:24), and BTC ATR percentile is **92 (elevated)**. The fresh swing report's own verdict: *"short bias or no trade; avoid weak altcoin longs."*
- **Modest dead-cat bounce, not a turn.** BTC clawed back from ~$59.6k to **~$61,924** and ETH from ~$1,550 to **~$1,656** since 16:24, but both 1-day changes are still negative (−2.7% / −6.8%) and ETH is at a 13-month low. This is relief inside a downtrend — **the edge remains risk hygiene + patience, not initiating either side into chop.**
- **#1 actionable finding — the active ZEC/USDT swing LONG is a hard contradiction and must be treated as AVOID / effectively dead.** Signal entry zone was **$561.89–$567.42, invalidation $555.12**; ZEC has since crashed **~40–50%** to a **~$324 low (now ~$340)** on the **Orchard counterfeiting vulnerability** (Claude/Taylor Hornby audit; emergency soft fork Jun 2 + NU6.2 hard fork Jun 3). Price is far below invalidation — the `tp2_hit` status is a stale pre-crash artifact. The residual risk is structural: *there is no cryptographic way to prove the bug was never abused.* **Do not hold or initiate any ZEC long.**
- **No A-tier and no fresh B-tier crypto setup. Every "active" crypto signal is expired or managed.** Of the 6 listed: NEAR / ADA / EPIC (intraday) and C (scalp) are all **past `expires_at` and `tp2/tp1_hit`** (realized/lapsed); only **ZEC and XLM swing** are still inside their expiry window — ZEC is contradicted (above), XLM is a counter-trend long that is `tp1_hit` (manage, do not add).
- **Net verdict: Crypto = short-biased but NO-CHASE; stand-down / manage-only this slot.** No clean long (fighting the tape + breadth 16.7%), no clean fresh short (post-bounce, no fresh setup, oversold). **For Monday's US open: stage for a risk-off / energy-&-defense-bid gap if Hormuz/Iran headlines persist over the weekend** — size down, no counter-tape longs, no breakdown-chasing shorts into support. **Stocks = no action (closed); Monday watch = A-tier LLY/AAPL/AMD planning + legal-risk avoids SMCI & UNH.** Catalyst layer is **context-only (66% unmapped).**

---

## 2. Data Used

**Internal — crypto reports (mtime / freshness):**
- `data/reports/swing/2026-06-06_14-46_swing_report.md` — **~0.9h, FRESH** (regenerated this cycle). Regime: BTC+ETH downtrend, breadth above EMA20 **16.67%**, BTC ATR pct **92 (elevated)**, style *"short bias or no trade."* No A-tier, no B-tier — all watchlist.
- `data/reports/scalp/2026-06-06_02-38_scalp_report.md` — **~13.0h, STALE** (no regen this cycle).
- `data/reports/intraday/2026-06-05_13-54_intraday_report.md` — **~25.8h, STALE** (no regen this cycle).
- Stocks reports (intraday 06-05 20:17 ~19.4h, swing 06-05 19:07 ~20.6h, invest 06-05 14:55 ~24.7h) — **weekend, market closed → context only.**

**Catalyst / narrative:** `data/catalysts/2026-06-06/` — `catalyst_events.jsonl` (**512 rows**, mtime 17:05 EEST), `narrative_baskets.jsonl` (**3 baskets**), latest `catalyst_cycle_14-05.md`. Mapped **174 / 512 (34%)**, unmapped **338 / 512 (66%)** → **weak (see §5)**.

**LLM packets:** `data/processed/llm_analysis_packet.md` (crypto, **~0.9h FRESH**), `data/processed/llm_stocks_packet.md` (~19.4h, closed-market context).

**CLI / DB (read-only, this run):**
- `active-signals` crypto = **6** (NEAR/ADA/EPIC intraday + C scalp = all `tp_hit` & past-expiry; ZEC/XLM swing still in-window); stocks = **50** (closed → context; A-tier: LLY, AAPL, AMD).
- `signal-stats` crypto week — headline A/B **sample=70, triggered=54, 13W/20L, winrate 24.1%, PF 1.55, avgR 0.20, totalR +11.0**; direction split: **longs n=36 PF 2.75 totalR +14; shorts n=34 PF 0.75 totalR −3.** Crypto intraday mode net **−6R** (PF 0.14).
- `signal-stats` stocks week — headline A/B **sample=215, triggered=157, 45W/58L, winrate 28.7%, PF 1.26, totalR +15.0**; C-tier PF 0.93 totalR −3 (watchlist drag).
- `detect_untracked_legacy_alerts --since 2026-06-06` → **None (0)** — clean, headline stats uncontaminated.
- DB `db/crypto_ai_desk.sqlite` (live, ~738 MB, mtime 18:39 — collector writing). news_items last 6h = **132 rows**.

**External (this run — cited §13):** BTC ~$61,924 / ETH ~$1,656 (Blockchain.com/Coinbase via search); Zcash Orchard counterfeiting bug + price (news.bitcoin.com WebFetch 200, KuCoin, BanklessTimes, CryptoBriefing, Genfinity, TheStreet); US–Iran/Hormuz carried from 16:24 (TradingKey, usethebitcoin).

**Unavailable / blind:** live tick beyond cited prints; TradingView/Chrome chart verification (not loaded); liquidation heatmaps / order-book / CVD; **fresh scalp & intraday crypto execution levels (reports 13–26h stale)** — re-pull live before any entry.

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-06_default_schedule/`.
- `scheduler.log` mtime **17:47:33 EEST** (~0.9h); latest cycle summary `cycle_02_15-30_summary.md` mtime **17:47:31** (~0.9h). **Both < 3h → NO DEFER.**
- **Partial improvement vs prior reviews:** a **new cycle (`cycle_02_15-30`) ran since 16:24**, regenerating the **swing report + LLM crypto packet** (both now ~0.9h fresh). **However scalp (~13h) and intraday (~25.8h) did NOT regenerate** — the generator-staleness regression flagged in the last several reviews is now **partial: swing fixed, scalp/intraday still lagging.** See §14 `TODO-crypto-report-staleness`.
- Swing freshness label: **< 4h → fresh this run.** Scalp/intraday: **stale → excluded from execution-level use; direction context only.**

---

## 4. What Changed vs Previous Review (pre-US-open 16:24 → US-open-reaction 18:30)

- **A new scheduler cycle ran — crypto data partially un-staled.** This is the most material operational change: `cycle_02_15-30` regenerated the **swing report (06-05 22.8h-stale → 06-06 0.9h fresh)** and the LLM crypto packet. Scalp/intraday still stale. The "no cycle since 11:40" condition the 16:24 review flagged has cleared for swing.
- **Bleed paused → modest bounce.** BTC ~$59,654 → **~$61,924**; ETH ~$1,550 → **~$1,656**. Direction still down (1d −2.7% / −6.8%) but the freefall stalled — consistent with the 16:24 "at/through liquidation magnets, expect a bounce" read. **Bounce, not reversal.**
- **Breadth deteriorated** despite the bounce: above-EMA20 **~21% → 16.7%** — fewer names participating, bounce is thin/large-cap-led.
- **Active crypto signals 7 → 6.** TON intraday short (the 16:24 lone live conditional) has **expired/dropped off**. Remaining mix unchanged in character: NEAR/ADA/EPIC/C tp-hit & expired, ZEC/XLM swing.
- **ZEC thesis hardened, not softened.** External verification this run pins the crash at **−41–50% to a ~$324 low** with **unprovable residual counterfeiting risk** — the active ZEC long is now unambiguously AVOID (price << invalidation $555).
- **Catalyst volume grew 327 → 512 events** (baskets still 3); unmapped ratio **63% → 66%** (still weak). New basket detail: **ai_narrative** (NEAR/RENDER/TAO/FET, Hayes-dump driven) and **momentum_breakout HEI** (+14.7%, no news).
- **Untracked legacy alerts still 0** (clean, unchanged).
- **Signal-stats essentially flat** (winrate ~24%, PF ~1.55, totalR +11); long-vs-short divergence persists (longs PF 2.75 / shorts PF 0.75) — feedback-only, small sample.

---

## 5. Catalyst Coverage

- **Total catalyst_events today: 512.** Mapped (non-null symbol): **174 (34%)**. Unmapped (null symbol): **338 (66%)**. `narrative_baskets`: **3**.
- **⚠ Catalyst mapping weak this run (66% unmapped > 50%) — use the catalyst layer as CONTEXT, not for final decisions.**
- Top unmapped headlines (symbol resolver missed):
  1. *"Big thanks to Kathy Lien for stepping in with expert financial help…"* — **spam/scam-style text ingested as a catalyst** (RSS hygiene issue; see §14).
  2. *"Stock Market Today, June 5: NuScale Power Falls as Speculative Technology Names Tank"* (Navitas / NuScale — equity names, no ticker mapped).
  3. *"Prediction: This Will Be the Next Supercycle After AI Memory. 1 Stock to Buy Now…"* (clickbait, no ticker).
- Active narrative baskets (all `single_source`):
  - **ai_narrative** (fresh <6h) — primary NEAR/RENDER/TAO/FET (+ WLD/ASTER) — driven by Arthur Hayes' WLD/NEAR/ZEC exit; *bearish/distribution*, not a long trigger.
  - **binance_ecosystem_teaser** (<24h) — BNB/ASTER — BNB's $3.6B RWA milestone failed to lift price → sell-the-news.
  - **momentum_breakout** (<1h) — HEI/USDT +14.7% on 0.63x vol, no news, playbook `wait_pullback`; cross-venue funding negative (bybit −2.47%) → short-covering pop, low quality.

---

## 6. Market Landscape

- **Regime (fresh swing report):** BTC downtrend, ETH downtrend, altcoin breadth above EMA20 **16.67%**, volatility **elevated (BTC ATR pct 92)**, recommended style **"short bias or no trade; avoid weak altcoin longs."**
- **Macro / geopolitics:** internal macro risk **55/100** (3 risk-off hits). External: total crypto market cap **−48% from peak**; **Strategy (MSTR) sold BTC** for the first time in ~4 years; **longest-ever US spot-BTC-ETF outflow streak (~13 days)**; Fed pricing **~69% probability of zero 2026 rate cuts**; **US–Iran conflict** with **Strait of Hormuz closure** (largest oil-supply disruption framing) — a live **weekend gap-risk** for Monday equities (energy/defense bid, broad risk-off).
- **Flow:** strongest names are thin, low-volume pops (HEI +64% 0.64x vol, EPIC +12% 0.04x vol, ALLO +116% 0.2x vol) — **breakouts on weak volume + short-covering**, not durable demand. Weakest: NFP −20%, OPN −18%, BABY −16%, WLD −15%. Derivatives skew to **deleveraging / long-liquidation** with **negative funding** on the movers (HEI, WLD, GENIUS) → bounce is short-driven, fragile.
- **Net:** thin large-cap-led relief bounce inside a confirmed downtrend with deteriorating breadth and a structural crypto-trust shock (Zcash). Low-conviction, two-sided chop; the actionable edge is to **wait**.

---

## 7. Candidate Deep Dives (≤ 5)

### Candidate 1 — ZEC/USDT (B swing long) — **CONTRADICTION → AVOID / dead signal**
- **Signal:** sig_5a9e5f5386306226, B swing long, score 65.2, status `tp2_hit`, entry $561.89–$567.42, invalidation $555.12, expires 2026-06-07T22:56 (still in window).
- **Contradiction (verified, multi-source + WebFetch 200):** Zcash **Orchard counterfeiting vulnerability** (under-constrained Orchard Action circuit, present since 2022; could mint unlimited undetectable counterfeit ZEC). Disclosed May 29 (Taylor Hornby / Claude AI audit), emergency **soft fork Jun 2** (Orchard disabled, ZEC ~$587), **NU6.2 hard fork Jun 3** (patched). **ZEC crashed −41–50%, low ~$324, now ~$340.** Arthur Hayes sold all ZEC.
- **LEGAL/HEADLINE-EQUIVALENT (technical-trust) RISK:** residual is structural — *"no cryptographic way to prove the bug was never abused"*; a privacy coin's value proposition is mathematical certainty, now reduced to "reasonable confidence."
- **Price-reaction / chase:** price is **~40% below the signal's invalidation ($555)** — the catalyst has fully (over)reacted; `tp2_hit` is a stale pre-crash artifact. Entry NOW would be catching a knife on impaired fundamentals.
- **Verdict: AVOID. Treat the active long as invalidated/closed.** Long-bias of any kind on ZEC is uninvestable until supply-verification upgrades land.

### Candidate 2 — XLM/USDT (B swing long) — **MANAGE-ONLY, no add**
- **Signal:** sig_5ce208fbfdea8d31, B swing long, score 65.4, status `tp1_hit`, entry $0.2544–$0.2587, invalidation $0.2490, expires 2026-06-07T22:36.
- **Internal/external news:** **none in 48h** (0 ZEC-style catalyst) — the only "clean" active crypto signal by news. (Note: an earlier-week CoinDesk piece tagged XLM as a relative gainer, but nothing fresh this window.)
- **Price-reaction / chase:** counter-trend long (BTC/ETH downtrend, breadth 16.7%) that already booked tp1. With the regime "avoid weak altcoin longs," **adding here fights the tape.**
- **Verdict: MANAGE the existing partial only — trail stop above invalidation $0.2490; do NOT add / do NOT initiate fresh.** Crypto longs PF 2.75 this week is the only supportive datapoint, and it is small-sample/feedback-only.

### Candidate 3 — NEAR/USDT (AI-basket primary; prior intraday short, now expired) — **bearish context / watchlist**
- **Signal:** sig_9ca0b338 intraday short `tp2_hit`, **expired 13:01 today** — realized/lapsed, not actionable.
- **Catalyst:** primary in **ai_narrative** basket; Arthur Hayes **sold NEAR** near the top and turned bearish ("back to pre-call levels"). Distribution, not accumulation.
- **Verdict: WATCHLIST, bearish lean.** No fresh setup; any new entry would be re-pulled live. Do not chase the down-move (already reverted).

### Candidate 4 — WLD/USDT (AI-basket; Hayes exit) — **short-side context, NO-CHASE**
- **Catalyst:** Hayes dumped WLD (token −10–20% over the episode); flagged among **weakest symbols (−15% 24h)**, negative cross-venue funding (bybit −0.06%, okx −0.11%), deleveraging/long-liquidation derivs.
- **Price-reaction / chase:** already down 15–20% — the short is **late / overextended**; no clean retest structure in the fresh report (watchlist-only, invalidation if activated 1h close beyond 0.4565).
- **Verdict: WATCHLIST short bias, but NO-CHASE here.** Wait for a lower-high retest; do not sell into the hole.

### Candidate 5 — Stocks A-tier + legal flags (weekend planning, market CLOSED) — **Monday gap watch**
- **A-tier (closed → planning only):** **LLY** (intraday score 82 `waiting`, swing 83 `trail`, long), **AAPL** (intraday 80 `waiting`, swing 83 `trail`, long), **AMD** (swing 81 `trail`, intraday 79 `waiting`, long). These are the highest-conviction names *into Monday* — but subject to the weekend Iran/Hormuz gap-risk overlay (risk-off, energy/defense bid). Confirm fresh on Monday's open; do not pre-position blind.
- **§I LEGAL/HEADLINE RISK — AVOID list (verified in catalyst layer):**
  - **SMCI** — Form 8-K: **indictment of three individuals re alleged export-control violation conspiracy** (SEC EDGAR) → AVOID until clarified.
  - **UNH** — **DOJ antitrust + fraud probe, shares −16%** (QuiverQuant/Yahoo/Phemex) → AVOID; the C-tier UNH signals are not actionable.
- **Verdict: No stock action this slot (closed).** Monday: watch LLY/AAPL/AMD for confirmation, hard-avoid SMCI & UNH.

---

## 8. Best Candidates Ranked

**No clean actionable candidates this slot.**

1. *(manage-only)* **XLM/USDT** — existing `tp1_hit` swing long: trail above $0.2490, no add. Lowest-risk way to stay involved; counter-trend, low conviction.
2. *(planning, closed)* **LLY / AAPL / AMD** (stocks A-tier) — Monday-open watch, gap-risk caveat.
3. *(watchlist short, no-chase)* **WLD, NEAR** — wait for lower-high retest; do not chase extended down-moves.

Everything else is expired, managed, contradicted, or watchlist. **The honest read is stand-down / manage.**

---

## 9. Avoid / No Trade

- **ZEC/USDT (long, any timeframe)** — counterfeiting bug, unprovable residual risk, −40–50%; active long is invalidated.
- **SMCI** — export-control indictment (legal).
- **UNH** — DOJ antitrust/fraud probe, −16% (legal).
- **Fresh crypto longs broadly** — downtrend + breadth 16.7% + "avoid weak altcoin longs."
- **Chasing the bounce either way** — BTC ~$62k / ETH ~$1.66k are relief levels, not confirmed reversals; no fresh setup.
- **HEI/USDT** — +14.7% on 0.63x vol, short-covering pop, no news; `wait_pullback`.
- **Thin low-volume "strong" names** (EPIC 0.04x, ALLO 0.2x vol) — illiquid, not durable.

## 10. Main Risks

- **Weekend geopolitical gap-risk (HIGH):** US–Iran / Strait of Hormuz — a fresh headline can gap crypto (live) and Monday equities (closed now) hard risk-off. Largest single overlay.
- **Crypto-trust contagion (MEDIUM):** Zcash bug + the auditor adding **Monero** to the queue could pressure the privacy-coin complex; broader "AI-found-a-4-year-bug" sentiment hit.
- **Bounce-failure / lower-high (MEDIUM-HIGH):** breadth deteriorating into the bounce → high odds the relief fades; counter-tape longs get trapped.
- **Stale scalp/intraday execution levels (OPERATIONAL):** scalp 13h, intraday 26h — any intraday/scalp action must re-pull live prices first.
- **Catalyst mapping weak (66% unmapped) + spam ingestion** — do not let the catalyst layer drive decisions this run.
- **Source quality:** all narrative baskets `single_source`; macro Telegram prints `single_source`. (Source-ingest step result logged in §13.)

## 11. Action Plan — next 4 hours

1. **Crypto: stand down / manage.** No fresh entries. Hold XLM partial with a trail above $0.2490; treat ZEC long as closed/invalid.
2. **Watch BTC $62k pivot:** a clean reclaim+hold of ~$62k with breadth improving = first sign the bounce has legs (still not a long trigger alone); rejection back under ~$60k = downtrend resumes, watch for clean lower-high shorts (WLD/NEAR) on a retest, not at the lows.
3. **Monitor Iran/Hormuz headlines** through the weekend — the single biggest gap-risk into Monday's US open.
4. **Re-pull live prices** before acting on any scalp/intraday idea (reports stale).
5. **Stocks: no action (closed).** Pre-build Monday watchlist — LLY/AAPL/AMD long-confirm candidates; SMCI & UNH hard-avoid (legal). Expect a risk-off / energy-&-defense gap if Iran persists.
6. **Next scheduled slot:** 21:30 EEST (late-session risk review).

## 12. Final Verdict per Mode

- **Crypto scalp:** NO-TRADE — stale levels (13h), thin bounce, no setup. Wait.
- **Crypto intraday:** NO-CHASE / short-bias-only — no fresh trigger; mode is net −6R this week; only act on a clean lower-high short on a retest, never at the lows.
- **Crypto swing:** MANAGE-ONLY — trail XLM; **ZEC long = AVOID/closed**; no new swing longs into a downtrend with 16.7% breadth.
- **Stocks (all modes):** NO-ACTION (market closed). Monday: LLY/AAPL/AMD watch; AVOID SMCI, UNH.

---

## 13. Sources

External (this run):
- [news.bitcoin.com — Zcash Patches Critical Bug Enabling Unlimited Counterfeit ZEC Minting as Price Crashes 41%](https://news.bitcoin.com/zcash-orchard-counterfeiting-bug-patched/) — 2026-06-05 (WebFetch HTTP 200; primary timeline + residual-risk).
- [KuCoin — ZEC Price Declines by 50% due to Concerns over Zcash's Orchard Pool Bug](https://www.kucoin.com/blog/ZEC-Price-Declines-by-50-percent) — 2026-06 (price reaction).
- [BanklessTimes — Zcash Price Crashes 50% on Orchard Bug](https://www.banklesstimes.com/articles/2026/06/05/zcash-price-crashes-50-as-orchard-counterfeit-bug-breaks-trust/) — 2026-06-05.
- [CryptoBriefing — Zcash faces governance concerns after emergency hard fork over critical vulnerability](https://cryptobriefing.com/zcash-governance-concerns-emergency-hard-fork/) — 2026-06 (internal news_items corroboration).
- [Genfinity — Zcash Plunges as Claude AI Audit Uncovers Four-Year Orchard Counterfeiting Flaw](https://genfinity.io/2026/06/05/zcash-claude-vulnerability-zec-crash-ai/) — 2026-06-05.
- [TradingKey — 2026 Crypto Crash Causes: Why Bitcoin Broke Through Key Levels](https://www.tradingkey.com/analysis/cryptocurrencies/btc/261945885-crypto-bitcoin-btc-price-crashing-usd-strategy-fed-tradingkey) — 2026-06 (market-cap −48%, Strategy selling, Fed, ETF outflows).
- [usethebitcoin — Crypto Market US-Iran Tensions Trigger ETF Outflows in June](https://usethebitcoin.com/news/crypto-market-us-iran-tensions/) — 2026-06 (US–Iran macro).
- [Yahoo Finance — Bitcoin and ethereum prices today, Friday, June 5, 2026](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-friday-june-5-2026-prices-continue-their-descent---5-reasons-why-113631165.html) — 2026-06-05 (BTC/ETH open prints).
- BTC ~$61,924 / ETH ~$1,656 (Blockchain.com / Coinbase aggregate via WebSearch, 2026-06-06; live tick — date-stamped to run).

Internal (this run): `data/reports/swing/2026-06-06_14-46_swing_report.md`; `data/catalysts/2026-06-06/{catalyst_events.jsonl, narrative_baskets.jsonl, catalyst_cycle_14-05.md}`; `data/processed/llm_analysis_packet.md`; `db/crypto_ai_desk.sqlite` (news_items: ZEC ×6 / Telegram ×8 last 4h); CLI `active-signals`/`signal-stats`/`detect_untracked_legacy_alerts`.

## 14. Fix Requests / TODO

### TODO-crypto-report-staleness
- **issue:** scalp & intraday crypto reports still do not regenerate every cycle — swing now refreshes but scalp (~13h) and intraday (~26h) lag persistently.
- **evidence:** swing `2026-06-06_14-46` (fresh ~0.9h) vs scalp `2026-06-06_02-38` (~13h) & intraday `2026-06-05_13-54` (~25.8h); only `cycle_02_15-30_summary.md` produced swing+packet this cycle. Flagged in ≥4 prior reviews.
- **suggested manual fix:** audit the scheduler's per-mode report-generation step — confirm scalp/intraday generators are invoked each cycle (or document the intended cadence); the swing path now works and can serve as the reference.
- **priority:** medium
- **first observed:** carried forward (≥ 2026-06-05); re-confirmed 2026-06-06 18:39 EEST.

### TODO-catalyst-mapping-weak
- **issue:** catalyst symbol-mapping persistently weak — 66% of events unmapped (null symbol), above the 50% context-only threshold for multiple runs.
- **evidence:** 338/512 unmapped today (63% at 16:24, 66% now); top unmapped are equity headlines + clickbait the resolver can't ticker-map.
- **suggested manual fix:** improve the catalyst-layer symbol resolver (entity-alias coverage for equity names like NuScale/Navitas; consider an importance-gated drop for unmappable items).
- **priority:** medium
- **first observed:** carried forward; re-confirmed 2026-06-06 18:39 EEST.

### TODO-rss-spam-ingestion
- **issue:** scam/spam text ingested as a catalyst event ("Big thanks to Kathy Lien for stepping in with expert financial help… profitable trades, quick support and withdrawals…").
- **evidence:** unmapped catalyst_events row, 2026-06-06 catalyst layer (importance 0.444).
- **suggested manual fix:** add a spam/promo filter to the news/RSS ingest (keyword + sender heuristics: "withdrawals that actually hit my bank", "expert financial help", testimonial patterns) before it reaches the catalyst scorer.
- **priority:** low
- **first observed:** 2026-06-06 18:39 EEST.

### TODO-stale-signal-lifecycle
- **issue:** signals whose price has blown far past invalidation still surface in `active-signals` with a stale `tp2_hit` status (e.g. ZEC long, entry $561, now ~$340 — ~40% below invalidation $555).
- **evidence:** `active-signals --asset-class crypto` lists sig_5a9e5f5386306226 ZEC as active despite price << invalidation and a confirmed −40–50% catalyst crash.
- **suggested manual fix:** add an invalidation-breach auto-close / "invalidated" status so contradicted signals don't linger as apparent actionable entries.
- **priority:** medium
- **first observed:** 2026-06-06 18:39 EEST.
