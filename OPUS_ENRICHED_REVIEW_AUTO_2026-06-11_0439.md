# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:39 EEST

_Slot: 04:30 crypto overnight / Asia review · Thursday 2026-06-11 · ~21:39 ET prev day. US cash CLOSED → stocks = planning/carry-forward only; crypto is the live actionable class. Focus: overnight crypto action, Asia regime, alt breadth, new overnight A/B, clean-vs-crowded shorts, catalyst-backed weakness, what to watch into Europe._

## 1. Executive Summary

**Risk-off persists overnight but with a bid underneath — the defining fact is a US/Iran geopolitical shock met by visible dip-accumulation. The clean playbook is short-the-failed-retest in a downtrend, NOT chase the flush; the cleanest catalyst-backed short is ZEC, and there is still no clean long until BTC reclaims its shelf on volume.**

Decisive overnight facts:
- **Macro = geopolitical risk-off, escalating overnight but stabilizing at the margin.** US struck Iran again overnight; Iran retaliated against the US Fifth Fleet in Bahrain; Strait of Hormuz tension. BTC tumbled on the strikes (web-confirmed: BTC toward ~$62K, ~$350M liquidations). BUT **S&P futures recouped early losses (+0.3%, Nasdaq +0.5%, 01:13 EEST)** and on-chain shows **accumulation** (whale withdrew **2,341 BTC / $144.7M**; Tom Lee's Bitmine bought **+25,000 ETH / $41M**). So: risk-off in regime, dip being bought at the edge → **squeeze/bounce hazard, not a fresh long signal yet.**
- **Crypto desk regime = bearish trend (risk-off).** BTC+ETH downtrend; **altcoin breadth above EMA20 = 25% (scalp) / 33% (intraday)** — *weaker* than the 40% at yesterday's close. Recommended style (desk): short bias or no trade; avoid weak altcoin longs.
- **Best actionable = catalyst-backed short ZEC/USDT.** ZEC's critical Orchard **counterfeiting vulnerability** is web-confirmed primary (−38%, $624→$309 on Jun 4–5, found via Anthropic Opus 4.8, emergency-patched). Caveat: that crash is **~6 days old and largely priced** — so this is a *short-the-retest on continued weakness* (CoinDesk 06-10 "Zcash leads losses"), not a fresh-catalyst chase.
- **Two clean B-tier shorts active, both `waiting_for_entry`:** **ZEC** (414.79–420.71, TP1 399, inval 427.95, catalyst-backed) and **NEAR** (1.98–2.01, TP1 1.912, inval 2.039, technical-only, expires 23:53 today). Both `weak_vs_market`, both aligned with risk-off.
- **What's working / failing (stats):** crypto **swing** PF **2.88 / +15R** and **intraday** PF **2.0 / +8R** are the live edge; the crypto **scalp** bucket is bleeding (**0W/4L, PF 0.00, −4R**) — treat scalp ideas as low-confidence (the report header says so). Stocks **A-tier remains the worst tier** (1W/7L, PF 0.14, −6R) — do not trust A-tier promotion.
- **Catalyst mapping weak again — 81.4% unmapped (3358/4125).** Use the catalyst layer as context, not a final decision input. The `ai_narrative` basket is **contaminated** (its sample headlines are Iran/Hormuz geopolitics, not AI-coin news) → mapping-quality TODO (§14).

**Best candidates this window (overnight-into-Europe):**
- **Best short-watch / catalyst-backed (crypto):** **ZEC/USDT** — B intraday breakdown/retest short. Trigger: **failed retest into 414.79–420.71**, TP1 399 / TP2 385.8, invalidation 427.95. Do not short below the zone (chasing a priced catalyst into a possible squeeze).
- **Best short-watch #2:** **NEAR/USDT** — B intraday short, **retest 1.98–2.01**, TP1 1.912, inval 2.039. Lower conviction (no fresh catalyst); expires 23:53 today.
- **Best long-watch:** **none clean.** Trigger = **BTC reclaim of ~$63–64K on volume** re-opens RS-leader longs (STG/STRAX/HMSTR on a *pullback*). Until then the oversold bounce is a squeeze hazard, not a long.
- **What to avoid:** chasing the overnight meme RS-leaders (**HMSTR +45–52%, STRAX +62%, STG +24%** = `avoid_chase`, no catalyst, OI-extended); shorting ZEC/NEAR *below* their zones; the stale-overnight B-**swing LONGS** (ALLO/BANK/BABY/CHIP) still showing active and still contradicting risk-off.
- **Stocks:** market **closed** → all stock ideas are planning/carry-forward. Carry MSFT (398.13–399.75) / PLTR (130.56–131.59) / TSLA (381.34–384.60) intraday-short retest levels to the US open; **require RTH confirmation**, do not pre-position on the gap. TSLA carries a prior headline flag (see §6).

## 2. Data Used

- Crypto **scalp** report — `data/reports/scalp/2026-06-11_01-36_scalp_report.md` (mtime 04:36, data 01:30Z) — **fresh** (<1h).
- Crypto **intraday** report — `data/reports/intraday/2026-06-10_23-22_intraday_report.md` (mtime 02:22, data 23:15Z) — **carry-forward** (~2.4h; freshest crypto with full agent pass).
- Crypto **swing** report — `data/reports/swing/2026-06-10_01-28_swing_report.md` (mtime 06-10 04:28) — **stale (~24h)**, excluded from fresh swing verdict.
- **Stocks** intraday report — `data/reports/stocks/intraday/2026-06-10_23-26_stocks_intraday_report.md` (mtime 02:26) — captures prior US close; **planning only** (market closed).
- Stocks swing/invest — both 06-10 01:3x — **stale (~27h)**, planning context only.
- Catalysts — `data/catalysts/2026-06-10/` (events.jsonl + narrative_baskets.jsonl + `catalyst_cycle_23-22.md`, mtime 02:22; the 23:22-cycle is filed under the 06-10 schedule-day → today's `2026-06-11/` dir not yet created, catalyst data itself is ~2.4h fresh, so `catalyst-scan` was **not** re-run).
- LLM packets — `data/processed/llm_analysis_packet.md` (mtime 04:36), `llm_stocks_packet.md` (mtime 02:26).
- DB (read-only) — `db/crypto_ai_desk.sqlite`: `news_items` (telegram + RSS), `proposed_signals` (ZEC/NEAR theses), integrity tables.
- CLI: `active-signals` crypto (7) + stocks (50); `signal-stats` crypto + stocks; `detect_untracked_legacy_alerts --since 2026-06-11` (**clean — 0 untracked**).
- External: WebSearch ×2 (Zcash counterfeiting bug; BTC reaction to US/Iran strikes) — both **confirmed primary/multi-source**. See §13.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime **04:36** (≈3 min ago) — **fresh**.
- Latest cycle summary `cycle_06_02-05_summary.md` mtime **02:27** (≈2.2h ago) — fresh, well within the 3h defer threshold → **review proceeds normally** (defer requires BOTH > 3h).
- Crypto scalp is fresh (<1h); intraday/catalysts are ~2.4h carry-forward (no newer full crypto cycle rendered yet); swing/invest and stocks swing/invest are overnight (01:3x → ~24–27h) → **stale, excluded from fresh verdict / planning only**.

## 4. What Changed vs Previous Review (23:24 post-close)

- **BTC clawed further off the $60K shelf toward ~$62K**, with overnight **accumulation flows** (whale +2,341 BTC, Tom Lee +25K ETH) and S&P futures recouping — the squeeze/bounce hazard flagged at the close is **now playing out**, but it is still a bounce-in-a-downtrend, not a trend change.
- **Iran conflict escalated overnight** (US re-struck; Iran hit the Fifth Fleet in Bahrain) — macro risk *higher* in headline terms, yet futures/risk assets are *stabilizing* → two-sided, do not lean fully short on the geopolitics alone.
- **ZEC moved from "watchlist-only two-sided catalyst" (prior) to an ACTIVE B intraday short** with `news_supported=1`. The counterfeit-bug catalyst is now web-confirmed and unambiguously bearish-fundamental (vs the prior Garrett-Jin-bull-bet ambiguity), but it is **stale/priced** — so the edge is now technical (failed-retest), not fresh-news.
- **TON short-watch (prior best short-watch) is no longer in the active list**; the two clean crypto shorts now are **ZEC + NEAR**.
- **Alt breadth deteriorated overnight** (40% at close → 25–33% now) — risk-off slightly *deeper* under the surface even as BTC bounces.
- **No new A-tier** in either class. A-tier remains the worst-performing tier.
- **Stale B-swing crypto LONGS persist** (ALLO/BANK/BABY/CHIP, all tp1/tp2-hit) — same contradiction-with-risk-off as prior; treat as already-moved, not fresh.
- **Catalyst mapping unchanged-weak** (81.4% unmapped now vs 81.8% prior).

## 5. Catalyst Coverage

- total `catalyst_events` (06-10 dir, last cycle 02:22): **4125**
- mapped (non-null symbol): **767** (BTC 312, TSLA 40, XRP 39, ETH 36, SMCI 35, NVDA 30, HYPE 28, SOL 27, UNH 20, ZEC 14, AVGO 14, AMD 12 …)
- unmapped (null symbol): **3358** → **81.4% unmapped**
- `narrative_baskets`: **4** — `rwa_narrative` (ONDO/XLM, `related_beta_rotation`, <6h); `ai_narrative` (NEAR/RENDER/TAO/FET + WLD/ASTER, `related_beta_rotation`, <6h — **contaminated with Iran headlines**); `binance_ecosystem_teaser` (BNB/ASTER, <24h); `perps_dex_narrative` (HYPE/DYDX/GMX/ASTER, `wait_pullback`, <24h).
- High-importance NULL-symbol events: **45** (top: xAI/SpaceX class action; Windows zero-day "RoguePlanet"; the Iran-strike macro headlines that should map to BTC-risk, not to a coin).

> **Catalyst mapping weak this run (81.4% unmapped) — use the catalyst layer as context, not a final decision input.** Top-3 unmapped: (1) "xAI and SpaceX face class action over data-center noise"; (2) "New Windows zero-day exploit RoguePlanet targets Microsoft Defender"; (3) macro Iran/Hormuz strike headlines (belong on BTC risk-routing, currently null-symbol).

## 6. Market Landscape

- **BTC/ETH:** both downtrend; BTC ~$62K area after the strike-driven flush, bouncing off the $60K shelf on accumulation; ETH soft. RSI was deeply oversold at the close (~24) → mean-reversion/squeeze risk is elevated.
- **Alt breadth:** 25% (scalp) / 33% (intraday) above EMA20 — narrow, risk-off under the surface.
- **Overnight RS-leaders (strength in a weak tape):** STRAX +62%, HMSTR +45–52% (OI +31%), STG +24%, KAT, CRV, WLFI — momentum/meme, mostly **no catalyst → `avoid_chase`**.
- **Overnight laggards (weakness):** ZBT −24%, SAHARA −18%, SENT −11%, CHIP −11%, WLD −10% — the clean-short universe in a downtrend.
- **Derivatives:** KAT/HMSTR show price-up + OI-up (fresh positioning, monitor crowding); HMSTR funding only mildly positive, L/S 0.88 → not yet euphoric, but +45–52% with thin volume = squeeze-prone both ways.
- **Crypto-specific catalysts:** Raydium **$1.34M exploit** (Solana DeFi, importance 0.86) — small $ but adds to risk-off DeFi tone; Aave risk-framework post-April-exploit; HYPE GENIUS-Act AML pushback.

### Market Mood / Risk Routing  (REQUIRED)
- **Crypto mood:** **risk-off** (bearish trend, narrow breadth) — but with active dip-accumulation = *risk-off with a bid*, squeeze-prone.
- **Stocks mood:** **closed** (overnight; planning/carry-forward only).
- **Dominant narrative:** **geopolitical macro (US/Iran strikes, Strait of Hormuz)** dwarfs coin-level narratives; secondary = ZEC supply-integrity overhang, Solana DeFi-exploit tone.
- **Preferred side now:** **shorts on failed retests** (risk-off routing) · **wait-for-trigger** on longs.
- **Best long candidate:** **none clean** — trigger: BTC reclaim ~$63–64K on volume → RS-leader longs (STG/STRAX/HMSTR on pullback) re-open.
- **Best short candidate:** **ZEC/USDT** — failed retest 414.79–420.71, TP1 399, inval 427.95.
- **Best catalyst-backed candidate:** **ZEC/USDT** (counterfeit-bug overhang + "leads losses"; note catalyst is priced → retest, not chase).
- **What to avoid:** HMSTR/STRAX/STG momentum chases; shorting ZEC/NEAR below their zones; stale B-swing crypto LONGS; leaning fully short on Iran headlines while futures stabilize.
- **What would change the view:** BTC reclaim $63–64K on volume (→ longs re-open) · OR a clean failed retest of ZEC/NEAR zones (→ shorts trigger) · OR a fresh Hormuz-closure / hard escalation headline (→ deeper risk-off, shorts press).

## 7. Candidate Deep Dives (≤ 5)

### 7.1 ZEC/USDT — B intraday SHORT — `waiting_for_entry` (BEST catalyst-backed short)
- **Setup:** breakdown/retest, score 66.5, `weak_vs_market`. Entry 414.79–420.71, TP1 399.0, TP2 385.8, invalidation/stop 427.95. `news_supported=1`. Expires 2026-06-12 00:43.
- **Catalyst (web-confirmed primary):** Zcash Orchard **critical counterfeiting vulnerability** (2 lines in the Orchard circuit, present since May 2022, allowed unlimited undetectable shielded-pool minting; found by Taylor Hornby using Anthropic Opus 4.8, emergency-patched ~Jun 1). ZEC **−38% ($624→$309) on Jun 4–5**, ~50% in 48h. Supply-integrity overhang persists (no cryptographic proof it wasn't exploited pre-fix). Internal corroboration: "AI identifies critical bug in Zcash…" (CryptoBriefing 06-10 22:38), "Zcash leads losses…" (CoinDesk 06-10).
- **Has price already reacted?** **Yes — heavily, ~6 days ago.** The bug is *priced*; today's edge is the continued `weak_vs_market` downtrend + supply-confidence overhang, not a fresh news pop.
- **Chasing? / Overextended? / Late?** Entry zone is **above** current price (waiting for a bounce to short) → by design *not* a chase IF taken on the failed retest. Shorting below the zone = chasing a priced catalyst into oversold/squeeze risk = late.
- **Mood-aligned?** Yes — clean liquid short in risk-off. **Long/short/wait:** short-on-trigger. **Actionable?** Only on the failed retest into 414.79–420.71.
- **Invalidation:** reclaim of 427.95 (and/or BTC reclaiming ~$63–64K lifting all risk).
- **Verdict:** **SHORT-WATCH (catalyst-backed), retest-only.** Cleanest crypto idea this window.

### 7.2 NEAR/USDT — B intraday SHORT — `waiting_for_entry`
- **Setup:** breakdown/retest, score 66.1, `weak_vs_market`. Entry 1.98–2.01, TP1 1.912, TP2 1.855, inval/stop 2.039. `news_supported=0`. **Expires today 23:53.**
- **Catalyst:** none symbol-specific (only a generic CoinDesk-20 index-drop mention). NEAR is listed as `ai_narrative` basket primary, but that basket is **contaminated** with Iran macro headlines → treat the "AI momentum" tag as unreliable here.
- **Has price reacted / chasing?** Technical short into a downtrend; entry above current = retest short, not a chase if disciplined.
- **Mood-aligned?** Yes (risk-off). **Lower conviction** than ZEC (no catalyst). **Actionable?** Retest 1.98–2.01 only; the short clock runs out tonight.
- **Invalidation:** reclaim 2.039 / BTC risk-on reclaim.
- **Verdict:** **SHORT-WATCH (secondary), retest-only, technical.**

### 7.3 HMSTR/USDT — overnight RS-leader (best long-watch / avoid-chase)
- **Read:** +45–52% / 24h, RS vs BTC +46–51%, **OI +31%**, volume only 0.11–0.34x (thin), funding mildly +, L/S 0.88. **No fresh catalyst** (no HMSTR news in last 24h).
- **Has price reacted / overextended / chasing?** Massively extended; entry now is the definition of a chase. Thin volume + OI-up = squeeze-prone **both** ways.
- **Mood-aligned?** No — a parabolic meme long in a risk-off tape is the lowest-quality long. **Verdict:** **AVOID CHASE.** It is the nominal "best long-watch" only because it's the strongest RS name, but it is not a clean trade; a clean long requires BTC reclaiming its shelf + an HMSTR *pullback that holds*, not the parabola.

### 7.4 SOL/USDT — Raydium exploit (catalyst-watch, context only)
- **Catalyst:** Raydium **$1.34M exploit** on legacy Solana AMM pools (importance 0.86; Decrypt/BeInCrypto 06-10; treasury to cover losses). Adds to risk-off DeFi tone.
- **Read:** $1.34M is *small* and contained (legacy pools, treasury-covered) → limited fundamental SOL damage. SOL is **not** in the active signal set. **Verdict:** **context only** — a tone input, not an actionable short. Watch only if SOL loses a structural level on volume.

### 7.5 BTC/USDT — the macro pivot (not a signal, drives everything)
- **Read:** strike-driven flush toward ~$62K, bouncing off the $60K shelf on **accumulation** (whale +2,341 BTC, Tom Lee +25K ETH), RSI deeply oversold, S&P futures recouping. Downtrend intact but two-sided.
- **Verdict / trigger:** **wait.** BTC reclaim **~$63–64K on volume** = the single switch that flips alt longs back on and weakens the alt shorts; a fresh Hormuz-closure/escalation headline = the switch that presses shorts. Until one fires, route to *short failed retests / no fresh longs*.

## 8. Best Candidates Ranked

1. **ZEC/USDT — SHORT-WATCH (catalyst-backed)** — failed retest 414.79–420.71, TP1 399, inval 427.95. *Trigger:* price tags the zone and rejects; do NOT short below 414.79.
2. **NEAR/USDT — SHORT-WATCH (technical, secondary)** — retest 1.98–2.01, TP1 1.912, inval 2.039. *Trigger:* failed retest into the zone before 23:53 expiry.
3. **Long-watch (no clean long) — RS-leaders on a reclaim** — STG/STRAX/HMSTR. *Trigger:* BTC reclaims ~$63–64K on volume AND the name gives a *pullback that holds* (not the parabola).
4. **Catalyst-watch — ZEC (same as #1)** + SOL (Raydium exploit, context-only). *Trigger for SOL:* loses a structural level on volume.

_No clean *triggered* trade exists in this window (both crypto shorts are `waiting_for_entry`, all longs are chases or pending a BTC reclaim) — but the routed watch-list above stands; scanning/tracking continue normally._

## 9. Avoid / No Trade (this decision window only)

- **HMSTR / STRAX / STG / KAT** — parabolic momentum/meme longs, no catalyst, OI-extended, thin volume → `avoid_chase`.
- **ZEC / NEAR shorts taken BELOW their zones** — chasing a priced/oversold move into squeeze risk.
- **Stale B-swing crypto LONGS (ALLO/BANK/BABY/CHIP)** — all tp1/tp2-hit, overnight, contradict risk-off → already moved, not fresh entries.
- **Leaning fully short on the Iran headlines** while S&P futures recoup and BTC is bid — geopolitics is two-sided here.
- _(Stocks closed — no stock entries this window regardless.)_
- **Not a system-stop:** scanning, candidate generation, tracking, and monitors continue in all moods.

## 10. Main Risks

- **Squeeze risk:** BTC oversold + accumulation + futures recouping → a sharp short-squeeze bounce could stop alt shorts (ZEC/NEAR invalidations). Demand the failed retest.
- **Geopolitical gap risk:** a Strait-of-Hormuz closure or hard escalation could gap BTC down hard (shorts pay) OR a ceasefire headline could gap it up (shorts trapped) — binary, headline-driven.
- **Catalyst-layer reliability:** 81.4% unmapped + a contaminated `ai_narrative` basket → do not let the catalyst layer drive a final decision.
- **Stale swing/invest data (~24–27h):** excluded from fresh verdicts; do not treat overnight swing LONGS as fresh.
- **Source-ingest:** if `ingest_enriched_review_sources` fails, sources are still cited in §13 (no decision depends on the ingest).

## 11. Action Plan — next 4 hours (into Europe)

1. **Watch ZEC** for a failed retest into 414.79–420.71 → if it rejects with BTC still heavy, that's the cleanest short (TP1 399). No tag, no trade.
2. **Watch NEAR** retest 1.98–2.01 (before 23:53 expiry) as the secondary short.
3. **Watch BTC ~$63–64K** as the long-switch: a volume reclaim re-opens RS-leader longs on pullbacks (not parabolas) and weakens the alt shorts.
4. **Monitor Iran/Hormuz headlines** — a closure/escalation presses shorts; a ceasefire traps them. Size for binary risk.
5. **Do nothing on HMSTR/STRAX/STG** except watch for a *pullback-that-holds* after a BTC reclaim.
6. Stocks: carry MSFT/PLTR/TSLA short-retest levels to the US open; **RTH confirmation required**, no gap pre-positioning.

## 12. Final Verdict per Mode

- **Crypto scalp:** **low-confidence / data-collection only** (bucket 0W/4L, PF 0.00). No scalp entries; let it scan.
- **Crypto intraday:** **short-the-failed-retest** — ZEC (catalyst-backed) primary, NEAR secondary; both retest-only, both `waiting_for_entry`. No fresh longs.
- **Crypto swing:** **stale data (~24h) → no fresh verdict.** Existing B-swing LONGS are already-moved (tp-hit), not new entries.
- **Stocks (all modes):** **closed → planning/carry-forward only.** Carry MSFT/PLTR/TSLA short levels to the open with RTH confirmation; distrust A-tier promotion; TSLA headline flag stands.

## 13. Sources

External (this run, WebSearch — confirmed primary/multi-source):
- [CoinDesk — Zcash plummets 38% as Shielded Labs reveals a major bug (Jun 5 2026)](https://www.coindesk.com/markets/2026/06/05/zcash-plummets-30-as-developer-reveals-a-major-bug-that-went-undetected-for-four-years) — *primary, confirms ZEC short overhang*
- [Decrypt — ZEC Crashes 38% as Zcash Discloses 'Critical Counterfeiting Vulnerability'](https://decrypt.co/370105/zec-crashes-38-as-zcash-discloses-critical-counterfeiting-vulnerability) — *primary*
- [The Block — Security researcher finds Zcash vulnerability allowing 'unlimited' counterfeit minting; ZEC drops 31%](https://www.theblock.co/post/403698/zcash-vulnerability-zec-drops) — *primary*
- [BeInCrypto — US attacks Iran: Bitcoin, Gold, Oil react (Jun 2026)](https://beincrypto.com/united-states-attacks-iran-bitcoin-gold-oil-june-2026/) — *confirms risk-off macro*
- [CryptoBriefing — Iran closes Strait of Hormuz and launches missile attacks](https://cryptobriefing.com/iran-strait-hormuz-bitcoin-crypto-impact/) — *macro escalation*
- [Bitget News — The Fed, Iran, and Saylor: anatomy of the June crypto crash](https://www.bitget.com/news/detail/12560605448772) — *context: multi-factor selloff (Fed + Iran)*
- [news.bitcoin.com — Bitcoin Reclaims $62K as Trump Strikes Iran, $94M wiped out](https://news.bitcoin.com/bitcoin-reclaims-62k-as-trump-strikes-iran-leaving-94m-in-trades-wiped-out/) — *confirms bounce/dip-buying*

Internal (DB `news_items`, dates as stored):
- CryptoBriefing — "AI identifies critical bug in Zcash that could have enabled unlimited counterfeit minting" — 2026-06-10 22:38 (ZEC, primary)
- CoinDesk — "Zcash, Hyperliquid tokens lead losses as traders bet against a bitcoin bounce" — 2026-06-10 10:52 (ZEC, confirms weakness)
- Decrypt / BeInCrypto — Raydium $1.34M exploit on legacy Solana pools — 2026-06-10 17:39 / 20:19 (SOL, primary)
- t.me/lookonchain — whale withdrew 2,341 BTC ($144.68M) — 2026-06-11 01:37 (accumulation, social_only)
- t.me/lookonchain — Tom Lee's Bitmine bought +25,000 ETH ($41.09M) — 2026-06-10 23:53 (accumulation, social_only)
- t.me/WalterBloomberg — "S&P 500 futures recoup early losses to rise 0.3%, Nasdaq +0.5%" — 2026-06-11 01:13 (social_only)
- CNBC Markets / CryptoBriefing — US strikes on Iran; "US strikes send Bitcoin tumbling" — 2026-06-11 01:09–01:40 (macro, single_source ×multiple)

## 14. Fix Requests / TODO

### TODO-catalyst-basket-contamination
- **issue:** `ai_narrative` basket's `catalyst_summary` sample headlines are Iran/Strait-of-Hormuz geopolitical macro lines, not AI-coin news — the basket is contaminated and would mislead a reader trusting the "AI momentum" tag on NEAR/RENDER/TAO/FET.
- **evidence:** `data/catalysts/2026-06-10/narrative_baskets.jsonl` (ai_narrative basket) + `catalyst_cycle_23-22.md`.
- **suggested manual fix:** in the basket builder, exclude macro/geopolitical null-symbol headlines from per-basket sample selection, or gate sample headlines to events actually mapped to the basket's symbols.
- **priority:** medium
- **first observed:** 2026-06-11 04:39 EEST

### TODO-catalyst-mapping-weak-persistent
- **issue:** catalyst symbol-mapping stuck at ~81% unmapped across consecutive runs (81.4% now, 81.8% prior) — macro/risk headlines (Iran strikes) sit null-symbol instead of routing to BTC-risk; high-importance NULL-symbol count = 45.
- **evidence:** events.jsonl coverage (mapped 767 / 4125); §5 here and §5 of `OPUS_ENRICHED_REVIEW_AUTO_2026-06-10_2324.md`.
- **suggested manual fix:** add a macro→BTC/ETH risk-routing rule and improve the symbol resolver (alias/ticker dictionary) in the catalyst layer; consider a "macro_risk" pseudo-symbol bucket so geopolitical headlines are usable for risk-routing rather than dropped.
- **priority:** medium
- **first observed:** 2026-06-11 04:39 EEST (recurring)

### TODO-crypto-scalp-bucket-losing
- **issue:** crypto **scalp** mode bucket is a reproducible loser (0W/4L, PF 0.00, avgR −0.13, −4R) while intraday (PF 2.0) and swing (PF 2.88) are positive — the scalp report itself flags TP/2h-horizon mismatch.
- **evidence:** `signal-stats --asset-class crypto` (By mode); scalp report header note.
- **suggested manual fix:** re-audit scalp TP/horizon sizing at the next 20 closed A/B scalp signals (as the report header proposes); consider widening scalp TP1 or shortening the tracking horizon so capture matches the 2h frame.
- **priority:** low
- **first observed:** 2026-06-11 04:39 EEST (recurring)

### TODO-stocks-a-tier-overpromotion
- **issue:** stocks **A-tier** remains the worst-performing tier (1W/7L, PF 0.14, avgR −0.60, −6R, stopR 0.90) — A-tier promotion is anti-predictive; sample weak (n=12) but the sign is persistent across reviews.
- **evidence:** `signal-stats --asset-class stocks` (By tier).
- **suggested manual fix:** audit the A-tier promotion criteria for stocks (what pushes B→A) and consider requiring an extra confirmation gate before A-tier; keep collecting until n≥20 before a hard change.
- **priority:** medium
- **first observed:** 2026-06-11 04:39 EEST (recurring)
