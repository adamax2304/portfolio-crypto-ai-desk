# Opus Enriched Review — pre-US-open decision review (Sunday) — Auto Cycle 16:23 EEST

## 1. Executive Summary

**Sunday 16:23 EEST "pre-US-open" slot — but US cash equity markets are CLOSED today (weekend). There is no US cash open this session; stocks stay closed until Monday RTH. Crypto is the only live actionable class; all stock A/B are paused-invest / planning-only.** External web research **AVAILABLE** this run (WebSearch ×2 + WebFetch verified on CryptoBriefing).

Crypto tape is **cautious risk-on / transition, cooling slightly** versus the 11:45 Europe read: desk reads **BTC transition_up / ETH downtrend**, altcoin breadth **67.5% > EMA20** (down from 75% at 11:45), BTC ATR percentile a very compressed **3**. Externally **BTC ~$64,385** (Jun 14) — sitting on the **$64K "weekend wall"**; a fresh **US–Iran de-escalation** headline (draft memorandum to reopen the Strait of Hormuz / waive oil sanctions / dilute enriched uranium — Telegram WalterBloomberg ~13:00 EEST + Cointelegraph) is a mild **risk-on** tilt nudging BTC toward $65K. This is a breakout-or-reject binary at the wall, not a confirmed trend — **route, don't chase**.

**No A-tier in any live class. No A/B in crypto scalp or intraday — both are entirely C-tier watchlist.** The only live actionable A/B are four crypto **swing/intraday** signals carried from earlier: **TAO swing B (waiting, news=1)**, **FET swing B (triggered)**, **PHA swing B (triggered)**, **MEGA intraday B (waiting)**. Best **catalyst-backed long-watch is TAO** (Bittensor subnet-demand / supply-squeeze, externally corroborated). **MEGA stays chase-risk** (no catalyst, **Jun-23 token unlock** overhang, $72M micro-cap). **No clean short** — weakest names already dumped (STG −37%, HMSTR −8%); short only on a failed retest if BTC loses the wall.

Weekend mode is active (size-down, demand retests); the weekend signal bucket is statistically poor. Advisory only; scanner / data-collection continue regardless of verdict.

## 2. Data Used

- **Crypto scalp report** `data/reports/scalp/2026-06-14_12-46_scalp_report.md` — mtime 12:46 EEST → **fresh** (~3.6h).
- **Crypto intraday report** `data/reports/intraday/2026-06-14_13-22_intraday_report.md` — mtime 13:22 EEST → **fresh** (~3h; data freshness 13:00 UTC).
- **Crypto swing report** `data/reports/swing/2026-06-14_01-32_swing_report.md` — mtime 01:32 EEST → **stale** (~15h; >14h — excluded from final-verdict swing unless no fresher source; active swing signals read live from DB instead).
- **Stocks intraday/swing/invest** — all dated 2026-06-12 (Fri) → **stale**; markets CLOSED Sunday → planning context only.
- **Catalysts** `data/catalysts/2026-06-14/` — events.jsonl (1,453 rows) + narrative_baskets.jsonl (3) + cycle md (09:29 → 12:29 EEST) — fresh.
- **LLM packet** `data/processed/llm_analysis_packet.md` (13:22, fresh; weekend mode active=True); stocks packet stale.
- **DB (read-only)** `db/crypto_ai_desk.sqlite`: proposed_signals (active A/B), news_items (Telegram + 24h), watchlist_alerts, catalyst_events.
- **External:** WebSearch (BTC/Iran macro, TAO/Bittensor) + WebFetch (CryptoBriefing Bittensor — verified, Jun 13).
- **Note:** the read-only CLIs ran very slowly this run. `signal-stats --asset-class crypto` eventually completed and **confirms** the figures below (A/B n=88, WR 17%, PF 1.00; **weekend bucket n=21, WR 5%, PF 0.25, −3R**; non-weekend n=67, PF 1.12). `active-signals` ×2 returned very late (after drafting) and **confirm** the DB-sourced set: actionable crypto A/B = exactly the four deep-dived (MEGA intraday/waiting, FET+PHA swing/triggered, TAO swing/waiting); the other crypto rows are managed positions already at TP1/TP2. Stocks active-signals (50) are all intraday/swing/invest at C-tier or already-triggered — closed/planning-only (Sunday). `signal-stats --asset-class stocks` and `detect_untracked_legacy_alerts` completed late: stocks A/B all paused/planning (B-tier WR 31% n=42, C-tier WR 14% n=293 — invest-mode, 0× sizing); **untracked-legacy-alerts = None — no integrity anomaly** (every crypto alert has a backing proposed_signal). See §14 TODO.

## 3. Scheduler / Data Freshness

- Latest run folder: `data/scheduled_runs/2026-06-14_default_schedule/`.
- `scheduler.log` mtime **16:22:07 EEST** (~1 min old) → **fresh**.
- Latest cycle summary `cycle_04_12-13_summary.md` mtime **12:29 EEST** (~3h54m old).
- Defer rule needs **BOTH** older than 3h; the log is fresh → **review proceeds (no defer)**.
- Crypto scalp/intraday fresh; crypto swing **stale (~15h)**; all stock reports stale (Friday — weekend, expected).

## 4. What Changed vs Previous Review

Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-14_1145.md` (Sunday Europe / pre-US context, ~4.6h ago).

- **Regime cooled slightly:** breadth **75% → 67.5% > EMA20**; **ETH range → downtrend**; BTC still **transition_up** but now pinned at the **$64K wall** (~$64.4K). Still cautious risk-on, marginally less constructive.
- **New macro catalyst:** **US–Iran draft memorandum** (Hormuz reopening / oil-sanction waiver / uranium dilution) hit Telegram (WalterBloomberg ~13:00 EEST) + Cointelegraph "BTC nears $65K." De-escalation = mild risk-on; not yet signed → headline-reversal risk.
- **Leaders rotated:** new #1 is **ZKC (+39%, 12.4× vol)** — but >2 ATR extended → rejected/chase; **BANANAS31 (+27%), OPG (+19%)** lead the gainers; MEGA/MITO/TAO still present. ZKC/BANANAS31/OPG all "do not chase — wait for pullback."
- **Active A/B unchanged:** same four crypto (TAO/FET/PHA/MEGA). **No new A/B triggered since 11:45.** Scalp/intraday still produce zero A/B.
- **FIFA World Cup kicked off today (Jun 14):** crypto-partnership + fan-token headlines (Kraken/AVAX/CHZ, $SFA) are feeding the **delisting_thin_liquidity** basket — noise, avoid.
- **Stocks:** unchanged — closed; invest-mode A/B still paused/planning. UNH legal flag persists; LLY headwind persists.
- **Thesis:** crypto stays **cautious risk-on, wait-for-pullback in AI/RS leaders**; marginally more cautious as breadth cooled and BTC sits on the wall.

## 5. Catalyst Coverage

- **catalyst_events.jsonl rows today: 1,453**; **mapped (non-null symbol): 236**; **unmapped: 1,217 → 83.8% unmapped.** **baskets: 3.**
- ⚠️ **CATALYST MAPPING WEAK THIS RUN — USE CATALYST LAYER AS CONTEXT, NOT FINAL DECISION.**
- Top 3 unmapped headlines (generic finance, no ticker): "Here's How Much a $2,400 401(k) Match Could Be Worth by Retirement"; "How Insurance Companies Turn Their Premiums Into Billions in Profit"; "Americans Are Looking at a 40% Social Security Tax Hike Unless This Happens."
- Active baskets: **momentum_breakout** (wait_pullback; primary MITO, CHIP; fresh <1h) · **perps_dex_narrative** (wait_pullback; HYPE; +DYDX/GMX/ASTER) · **delisting_thin_liquidity** (avoid_low_liquidity; no primary — World-Cup fan-token noise).
- Recurring high-unmapped rate (>50% across runs) → see §14 TODO.

## 6. Market Landscape

- **Crypto (fresh, desk 13:00 UTC snapshot):** BTC **transition_up**, ETH **downtrend**; breadth **67.5% > EMA20 / 55% > EMA50**; BTC ATR pct **3** (very compressed → expansion risk both ways). Strongest: ZKC (100, +39%, chase), BANANAS31 (94, +27%), OPG (92, +19%), MEGA (92, +17%), MITO (84, +20%), RIF (81). Weakest: STG (−37%), TRUMP (−9%), HMSTR (−8%), NIGHT (−8%). Narrative: **AI mixed** (heat 29; TAO/FET/NEAR), Memes mixed, RWA/L2/Gaming quiet. Derivatives: leaders mostly price-up + OI-up (fresh positioning, crowding normal/low); funding broadly neutral; external venues confirm low crowding ex-ZKC (ZKC funding −0.02, crowding elevated → squeeze-prone if chased).
- **External macro:** BTC **~$64,385** (Jun 14) at the $64K weekend wall; US–Iran de-escalation headline supports a $65K test. Desk macro/geopolitics risk **25/100**, BTC bias neutral/data-watch. Recovery/transition, **not** a confirmed uptrend.
- **Stocks: CLOSED (Sunday) — no US cash open today.** Live A/B are all **invest-mode, paused (watchlist_only, 0× sizing)**: LLY (A 82), AMD/NVDA/SMH (B long), META/PLTR (B short), UNH (B long). Planning only; re-evaluate at **Monday RTH**.

### Market Mood / Risk Routing  (REQUIRED — PART 4)
- **Crypto mood:** cautious **risk-on / transition, cooling** (BTC transition_up but on the $64K wall, breadth 67.5% down from 75%, vol compressed) — route, don't chase.
- **Stocks mood:** **closed** (weekend) — planning only; no RTH confirmation possible until Monday.
- **Dominant narrative:** **AI** (Bittensor/TAO, FET, NEAR) + small-cap **momentum_breakout** (MITO, CHIP); macro overlay = US–Iran de-escalation.
- **Preferred side now:** **longs on pullback** in AI/RS leaders; **catalyst-backed** preferred; **wait-for-trigger** otherwise. Shorts only on failed retest if BTC loses the wall.
- **Best long candidate:** **TAO/USDT** — catalyst-backed, **waiting** pullback into **259.77–263.39** (SL 255.34).
- **Best short candidate:** **none clean** — weakest names already dumped (STG −37%, HMSTR −8%); trigger: BTC loses transition_up / the $64K wall, then short the *failed retest* of a weak high.
- **Best catalyst-backed candidate:** **TAO/USDT** (Bittensor subnet-demand / supply-squeeze; externally corroborated).
- **What to avoid:** MEGA chase + Jun-23 unlock exposure; no-catalyst weekend momentum longs (weekend bucket negative); chasing extended leaders (ZKC/BANANAS31/OPG >2 ATR); thin/MEXC + World-Cup fan-token (delisting_thin_liquidity) names; any stock entry (closed).
- **What would change the view:** BTC **breaking and holding above $64K wall toward $65K** with breadth >EMA50 rising = add long conviction; BTC **rejecting/losing the wall** = shift to failed-retest shorts; Monday RTH for any stock idea.

## 7. Candidate Deep Dives (≤5)

### Candidate 1 — TAO/USDT (crypto, swing, LONG B 65.4, waiting_for_entry) — BEST LONG-WATCH / CATALYST-BACKED
- Entry **259.77–263.39**, SL **255.34**, tp1 **273.05**, tp2 281.10; news_supported=1; AI/momentum_breakout narrative; desk score ~86, RS vs BTC +6.8% (scalp) / current price ~265.8 (desk).
- **Catalyst (internal reused + externally verified):** Bittensor subnet registration cost rose **6.5× to 1,500 TAO (~$470K/slot)** amid AI demand; **73% of circulating TAO staked**; post-Dec-2025 halving cut daily emissions to 3,600 (supply squeeze) — CryptoBriefing (Jun 13, **WebFetch-verified**). Additional context (CMC-AI): a US AI-model ban validated decentralized alternatives (TAO +16%); Grayscale/Bitwise spot-TAO ETF filings, decisions possibly by Aug 2026.
- Mood-aligned? **Yes** — AI is the dominant narrative; risk-on-transition favors RS-leader longs. Price reacted? Partly (+16% earlier). Chasing? No — signal **waits for a pullback** into 259.77–263.39, not a market buy. Overextended? Current ~265.8 sits just above the zone → demand the pullback. Actionable now? Only on a pullback-hold into the zone with volume. Invalidation: 255.34 / BTC losing the wall.
- **Final verdict: LONG-WATCH (best catalyst-backed). Actionable only on a held pullback into 259.77–263.39 with volume; size down for weekend; invalidate <255.34.**

### Candidate 2 — MEGA/USDT (crypto, intraday, LONG B 65.2, waiting_for_entry) — CHASE-RISK / UNLOCK OVERHANG
- Entry **0.06077–0.06250**, SL **0.05866**, tp1 0.06711 (expires 2026-06-15 05:57); no internal catalyst (news=0); score 92, +17% 24h, +40% 7d, RS +17%; current ~0.0621 → just inside the upper entry zone but extended vs structure.
- **External (verified prior run, CoinMarketCap):** ~$72M micro-cap, ~11% float (1.13B/10B), **token unlock 2026-06-23 (~2.5% supply)** ~9 days out; launched Apr 30, already −25–30% off highs — speculative bounce, no fresh fundamental catalyst.
- Mood-aligned? Partially (RS-leader long fits risk-on) but **no catalyst + unlock overhang + tiny cap = high chase-risk** under weekend mode. Chasing? Buying extended = chasing; plan needs a held pullback into 0.0608–0.0625. Actionable? Pullback-only, low size; do **not** carry size into the Jun-23 unlock.
- **Final verdict: LONG-WATCH (speculative) — pullback-only into 0.0608–0.0625 with volume; no chase; avoid Jun-23-unlock exposure.**

### Candidate 3 — FET/USDT (crypto, swing, LONG B 66.0, triggered) — AI BETA, MANAGE
- Entry 0.20687–0.20918, SL **0.20405**, tp1 **0.21532**, tp2 0.22044; triggered; AI narrative; no fresh single-name catalyst (news=0) — rides AI/Bittensor beta-rotation.
- Mood-aligned? Yes (AI). Reacted? Yes. Chasing? Already triggered → manage, don't initiate. Actionable? Manage toward tp1 0.21532; respect SL 0.20405; new adds only on a clean pullback-hold.
- **Final verdict: HOLD/MANAGE (triggered) — manage to tp1 0.21532, SL 0.20405; no fresh chase. AI beta, not a standalone catalyst.**

### Candidate 4 — PHA/USDT (crypto, swing, LONG B 65.2, triggered) — MANAGE, NO FRESH CATALYST
- Entry 0.03495–0.03540, SL **0.0344**, tp1 **0.0366**, tp2 0.0376; triggered; no internal catalyst (news=0); not surfaced in today's top-movers/RS leaders → momentum has cooled relative to entry.
- Mood-aligned? Weakly (no catalyst, not an RS leader today). Reacted? Triggered. Chasing? N/A — manage. Actionable? Manage to tp1 0.0366; respect SL 0.0344; do not add. Flag: low conviction, demand SL discipline given weekend gap risk.
- **Final verdict: HOLD/MANAGE (triggered) — manage to tp1 0.0366, SL 0.0344; no adds; low conviction (no catalyst, not an RS leader this run).**

### Candidate 5 — UNH (stocks, invest, LONG B 70.53, triggered) — AVOID / LEGAL RISK (planning, closed)
- **LEGAL/HEADLINE RISK (verified, carry-forward):** UnitedHealth under **DOJ civil + criminal Medicare-Advantage billing probe** (extends to Optum Rx / physician reimbursement); internal catalyst stream importance 0.73 ("Shares Dive 16% on Fraud Investigation"). Sources: CNN Business (2025-07-24), Fierce Healthcare, QuiverQuant.
- Stocks closed (Sunday) → planning only; invest-mode is paused (0× sizing) regardless. Long thesis directly contradicted by the active legal overhang.
- **Final verdict: AVOID (long). Manual review required before any UNH long is treated as actionable; not tradeable this window (closed).**
- _Legal/headline check for the other live stock A/B (all invest-mode, paused, planning-only): **SMCI** export-control indictment 8-K (no live A/B — flag only); **LLY (A)** thesis intact but weight-loss-coverage demand headwind (Jun 12); **AMD / NVDA / SMH (long)**, **META / PLTR (short)** — no fresh disqualifying legal/earnings flag surfaced in today's catalyst stream; all require Monday RTH confirmation before being treated as actionable._

## 8. Best Candidates Ranked

No clean *immediate* entry this window (crypto leaders extended / awaiting pullback; stocks closed). Per PART 9, routed watch list with triggers:

1. **TAO/USDT (long-watch, catalyst-backed)** — trigger: held pullback into **259.77–263.39** + volume; invalidate <255.34. *Best long + best catalyst-backed.*
2. **FET/USDT (manage, triggered long)** — manage to tp1 0.21532, SL 0.20405; add only on pullback-hold.
3. **PHA/USDT (manage, triggered long)** — manage to tp1 0.0366, SL 0.0344; no adds; low conviction.
4. **MEGA/USDT (long-watch, speculative)** — trigger: held pullback into **0.0608–0.0625** + volume; avoid chase / Jun-23-unlock.
- **Best long-watch:** **TAO** — trigger: pullback into 259.77–263.39 holding with volume.
- **Best short-watch:** **none clean** — trigger: BTC loses the $64K wall / transition_up, then short the *failed retest* of a weak high (STG/HMSTR-type) with stop above the swing high (no candidate qualifies now).
- **Best catalyst-watch:** **TAO** — trigger: continued Bittensor/AI subnet-demand confirmation + pullback entry.

## 9. Avoid / No Trade _(this decision window only — never "stop system")_

- **MEGA chase here (~0.062)** — extended, no catalyst, **Jun-23 unlock (2.5% supply)** overhang, $72M micro-cap; pullback-only, no chase.
- **Chasing extended leaders** — ZKC (+39%, funding −0.02 / crowding elevated → squeeze-prone), BANANAS31 (+27%), OPG (+19%) all >2 ATR; wait for pullback.
- **No-catalyst weekend momentum longs** — weekend bucket statistically negative; weekend mode demands retests, wider wicks, A-tier margin.
- **UNH long** — active DOJ Medicare-fraud probe (verified). AVOID until resolved/manual review.
- **Initiating new shorts on already-dumped names** (STG −37%, HMSTR −8%) — too extended; wait for failed retest.
- **Thin/MEXC high-risk discovery + World-Cup fan-token (delisting_thin_liquidity) names** — avoid_low_liquidity.
- **Any stock entry this window** — market CLOSED; no fills, no RTH confirmation until Monday.
- _Scanner, candidate generation, tracking, and data collection continue as normal — decision-window caution only._

## 10. Main Risks

- **BTC at the $64K weekend wall** — breakout-or-reject binary; compressed ATR (pct 3) → sharp expansion either way.
- **US–Iran headline is a draft memorandum, not signed** — de-escalation could reverse; treat as context, not a confirmed driver.
- **Weekend gap / thin-liquidity risk** in crypto; weekend signal bucket negative; wider wicks can hit tight stops.
- **Catalyst mapping 83.8% unmapped** → catalyst layer is context-only; decisions lean on technical + verified external.
- **No US session today** — stock A/B cannot be confirmed/entered until Monday RTH; pre-market reads don't apply (closed weekend).
- **Read-only CLIs hung this run** — performance/active-signals taken from direct DB + report-embedded metrics; ingest CLI may also fail (logged in §13 if so).

## 11. Action Plan — next 4 hours

1. **Crypto (live):** Wait for **TAO** pullback into **259.77–263.39** (vol confirm) as the preferred catalyst-backed long-watch; invalidate <255.34. **Manage FET** to tp1 0.21532 (SL 0.20405) and **PHA** to tp1 0.0366 (SL 0.0344). Treat **MEGA** as pullback-only into 0.0608–0.0625, low size, no chase.
2. **No new no-catalyst weekend momentum longs**; size down for weekend gap risk; demand retests over breakouts.
3. **Watch the $64K BTC wall:** hold/break toward $65K (Iran de-escalation tailwind) = add long conviction; reject/lose the wall = pivot to failed-retest shorts (none qualify yet).
4. **Stocks:** no action — market closed. Build Monday watchlist; **UNH = AVOID (legal)**, **LLY = planning w/ coverage headwind**, invest-mode paused (0×) — require Monday RTH confirmation.
5. Re-assess at the next slot (**18:30 US-open reaction** — note: Sunday, US still closed; crypto-only until Monday's cash open).

## 12. Final Verdict per Mode

- **Crypto scalp:** cautious risk-on chop — **wait-for-pullback**; no A/B (all C-tier); no fresh no-catalyst entries; low size for weekend.
- **Crypto intraday:** no A/B (all C-tier); **MEGA** pullback-only into 0.0608–0.0625, no chase; no-catalyst momentum longs underperform in chop.
- **Crypto swing:** **TAO long-watch (pullback 259.77–263.39 + vol)**; **manage FET → tp1 0.21532 / PHA → tp1 0.0366**; respect SLs; ride AI beta-rotation with size discipline. (Swing report stale ~15h → active signals read live from DB.)
- **Stocks intraday:** **MARKET CLOSED (Sunday) — planning only.** Re-evaluate Monday RTH.
- **Stocks invest/swing:** stale (Fri) + **paused (watchlist_only, 0×)** → planning only. **LLY (A)** thesis intact w/ weight-loss-coverage headwind; **UNH AVOID (DOJ probe)**; no weekend action.

## 13. Sources

- [Bitcoin price today is $64,385 — MetaMask Price](https://metamask.io/price/bitcoin) — 2026-06-14 — confirms (single_source): BTC ~$64,385, sitting on the $64K weekend wall.
- [Bitcoin nears $65K as Trump says Hormuz will 'open to all' in Sunday Iran peace deal — Cointelegraph](https://cointelegraph.com/news/bitcoin-nears-65k-trump-hormuz-iran-peace-deal) — 2026-06-14 — confirms (single_source): US–Iran de-escalation draft memorandum; corroborated by internal Telegram WalterBloomberg rows (~13:00 EEST: Hormuz reopening / oil-sanction waiver / uranium dilution).
- [Bittensor subnet registration cost rises 6.5x to 1,500 TAO amid AI demand — CryptoBriefing](https://cryptobriefing.com/bittensor-subnet-registration-cost-rises/) — 2026-06-13 — confirms (single_source, **WebFetch-verified**): subnet cost 230→1,500 TAO; 73% of TAO staked; post-halving 3,600/day emissions — supply-squeeze supporting TAO long.
- [Bittensor (TAO) price analysis — CoinMarketCap CMC-AI](https://coinmarketcap.com/cmc-ai/bittensor/price-analysis/) — date unavailable — confirms (single_source): US AI-model ban validated decentralized alternatives (TAO +16%); Grayscale/Bitwise spot-TAO ETF filings (decisions ~Aug 2026); 128→256 subnet scaling.
- Internal `news_items` (Telegram t.me/WalterBloomberg, 2026-06-14 ~09:56–10:09 UTC) — confirms (social_only): senior Iranian official — draft memorandum to reopen Strait of Hormuz, waive oil sanctions, dilute high-enriched uranium.
- Internal `proposed_signals` (DB, read-only) — active A/B crypto: TAO swing B (waiting, news=1), FET swing B (triggered), PHA swing B (triggered), MEGA intraday B (waiting); levels cited in §7.

## 14. Fix Requests / TODO

### TODO-readonly-cli-hang
- **issue:** The read-only review CLIs were extremely slow this run. `signal-stats --asset-class crypto` returned only after ~several minutes (well after the review body was drafted); `active-signals` ×2 never returned (review used direct read-only DB queries instead). `signal-stats --asset-class stocks` + `detect_untracked_legacy_alerts` (blpdt6a87) and `signal-stats --asset-class crypto` (bwjqyqgho) both completed late (after the review body was drafted) — integrity check came back clean (untracked alerts = None).
- **evidence:** background task b19z6acq8 (active-signals) emitted only the echo header (no command output); bwjqyqgho / blpdt6a87 completed but only after multi-minute delays; same CLIs returned promptly in prior runs.
- **suggested manual fix:** investigate whether `src.cli` blocks on a network/exchange call or DB lock at startup (esp. weekend/Sunday); add a `--offline`/`--fast` path or a hard timeout so read-only stats + the untracked-alert detector return deterministically within the review window.
- **priority:** medium
- **first observed:** 2026-06-14 16:23 EEST

### TODO-catalyst-mapping-low
- **issue:** Catalyst symbol mapping very low again — 236/1,453 mapped (83.8% unmapped); recurring >50% across runs.
- **evidence:** `data/catalysts/2026-06-14/catalyst_events.jsonl` (1,453 rows, 1,217 null-symbol; top unmapped are generic finance headlines like "How Insurance Companies Turn Their Premiums Into Billions"). World-Cup fan-token headlines also inflating the delisting_thin_liquidity basket.
- **suggested manual fix:** improve the catalyst-layer symbol resolver / pre-filter generic macro-finance + sports/fan-token RSS items before they enter the event stream; consider a ticker-bearing-source allow-list or NER tightening.
- **priority:** medium
- **first observed:** 2026-06-14 11:45 EEST (pattern recurring)

### TODO-weekend-bucket-negative
- **issue:** Weekend-mode signal bucket persistently negative — **confirmed this run: n=21, WR 5%, PF 0.25, −3R** vs non-weekend n=67, PF 1.12.
- **evidence:** `signal-stats --asset-class crypto` "By weekend_mode" + observation "(weak, n=21) weekend=Y: weekend signals underperform (winrate 5%, n=21)" (2026-06-14 16:23 run).
- **suggested manual fix:** consider a weekend size/threshold overlay (raise activation bar or reduce size on weekend_mode_active) — advisory; do not auto-apply.
- **priority:** medium
- **first observed:** 2026-06-14 11:45 EEST

### TODO-tier-b-triggered-winrate
- **issue:** A/B crypto headline winrate low — week sample n=89, WR 16.9%, PF 1.00 (report-embedded), all B-tier (no A-tier crypto).
- **evidence:** "Recent Signal Performance" in both 12:46 scalp and 13:22 intraday reports.
- **suggested manual fix:** human review of entry timing / weak-setup bucket scoring at next manual session (advisory; no auto-change).
- **priority:** low
- **first observed:** 2026-06-14 11:45 EEST
