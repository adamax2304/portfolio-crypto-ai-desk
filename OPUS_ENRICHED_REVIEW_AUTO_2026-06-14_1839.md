# Opus Enriched Review — US-open reaction review (Sunday — US equities CLOSED) — Auto Cycle 18:39 EEST

## 1. Executive Summary

**Sunday 18:39 EEST "US-open reaction" slot — but US cash equity markets are CLOSED today (weekend). There is no US session to react to; stocks stay closed until Monday RTH. Crypto is the only live actionable class; all stock A/B are paused-invest / planning-only.** External web research **AVAILABLE** this run (WebSearch ×3 + WebFetch verified on CryptoBriefing).

Little has changed since the 16:23 pre-open read, and that itself is the signal: crypto tape remains **cautious risk-on / transition, pinned at the wall**. Desk reads **BTC transition_up / ETH downtrend**, altcoin breadth **67.5% > EMA20 / 55% > EMA50**, BTC ATR percentile a very compressed **3** (expansion risk both ways). Externally **BTC ~$64,385** (Jun 14) — still sitting on the **$64K "weekend wall"**, down hard from the late-May ~$82K highs; recent tape is risk-off-leaning (sub-$64K dips triggered ~$1.1B liquidations in the prior 24h per CryptoBriefing). The **US–Iran de-escalation** headline (14-point draft MoU: Hormuz reopening / oil-sanction waiver / uranium dilution) remains a mild **risk-on** tilt toward $65K — but it is **still an unconfirmed draft needing Trump's sign-off** (Iran FM: "no final decision"), and a counter-headline crossed Telegram at 14:10 EEST ("**Israeli military preparing for possible fire** in coming hours") — so the macro overlay is now **two-sided / binary at the wall, not clean risk-on**. Route, don't chase.

**No A-tier in any live class. No A/B in crypto scalp or intraday — both are entirely C-tier watchlist.** No new A/B signal has triggered since the 14:53 batch. The carried crypto A/B have resolved further: **TAO swing B and PHA swing B are now triggered (managed positions), MEGA intraday B triggered**, while **FET / OPG / WLD / RIF swing B stopped out (FET booked −1R)** during the day. Best **long-watch remains TAO** (AI/Bittensor, externally corroborated) — but it is now *triggered*, so it is manage-not-initiate; the cleanest *fresh* long-watch is **MITO** on a held pullback. **No clean short** — weakest names already dumped (STG −37%, HMSTR −8%) and STG carries squeeze risk (price-down + OI-up); short only on a failed retest if BTC loses the wall.

Weekend mode is active (size-down, demand retests); the weekend signal bucket is statistically poor (prior signal-stats: weekend n=21, WR 5%, PF 0.25, −3R). Advisory only; scanner / data-collection continue regardless of verdict.

## 2. Data Used

- **Crypto scalp report** `data/reports/scalp/2026-06-14_12-46_scalp_report.md` — generated 15:46 EEST → **fresh** (~2.9h; data freshness 12:30 UTC).
- **Crypto intraday report** `data/reports/intraday/2026-06-14_13-22_intraday_report.md` — generated 16:21 EEST → **fresh** (~2.3h; data freshness 13:00 UTC).
- **Crypto swing report** `data/reports/swing/2026-06-14_01-32_swing_report.md` — ~14h → **stale** (>14h; excluded from final-verdict swing — active swing signals read live from DB instead).
- **Stocks intraday/swing/invest** — dated 2026-06-12 (Fri), 43–49h → **stale**; markets CLOSED Sunday → planning context only.
- **Catalysts** `data/catalysts/2026-06-14/` — events.jsonl + narrative_baskets.jsonl (3) + cycle md (latest `catalyst_cycle_09-29.md` → 12:29 EEST). ⚠️ Catalyst layer last refreshed **12:29 EEST (~6.2h old)** — aging; treat as context.
- **LLM packet** `data/processed/llm_analysis_packet.md` (16:22 EEST, fresh); stocks packet 44h stale (weekend).
- **DB (read-only)** `db/crypto_ai_desk.sqlite` (1.33 GB, mtime 18:07): proposed_signals, signal_outcomes, signal_alerts, news_items (Telegram + 24h), watchlist_alerts.
- **External:** WebSearch ×3 (US–Iran/Hormuz macro, BTC weekend price, Arthur-Hayes/HYPE) + WebFetch (CryptoBriefing Iran-US MoU — verified, Jun 12).
- **Note — CLI:** the read-only `src.cli` subcommands were **extremely slow** this run (`active-signals --asset-class crypto` returned only after ~15 min, well past drafting), so figures were derived in parallel by **direct read-only SQL** on the DB (permitted under §A.1). When `active-signals` finally returned it **confirmed** the DB-derived set: **11 active crypto signals — MEGA intraday / TAO swing / PHA swing `triggered` (weekend-mode), the rest (NOT, ALLO, ATOM, CRV, CHIP, BANANAS) at tp1/tp2 (managed).** `signal-stats` / `detect_untracked_legacy_alerts` not awaited; integrity check run directly instead: **0 orphan watchlist_alerts / 7 in 24h → no untracked-alert anomaly.** See §14 TODO on CLI latency.

## 3. Scheduler / Data Freshness

- Latest run folder: `data/scheduled_runs/2026-06-14_default_schedule/`.
- `scheduler.log` mtime **18:39 EEST** (~0 min) → **fresh**.
- Latest cycle summary `cycle_05_14-29_summary.md` mtime **18:39 EEST** (~0 min) → **fresh**. Scheduler just completed cycle 05.
- Defer rule needs **BOTH** older than 3h; both fresh → **review proceeds (no defer)**.
- Crypto scalp/intraday fresh (~2.3–2.9h); crypto swing **stale (~14h)**; all stock reports stale (Friday — weekend, expected). Catalyst layer **~6h old** (aging).

## 4. What Changed vs Previous Review

Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-14_1623.md` (Sunday pre-US-open, ~2.3h ago).

- **Regime essentially unchanged:** BTC still **transition_up** at the **$64K wall** (~$64.4K), ETH **downtrend**, breadth **67.5% > EMA20** (flat vs 16:23). No new scalp/intraday report has been generated since 16:21, so the desk snapshot is the same — the change is time/decay, not a new read.
- **Active A/B decayed further:** at 16:23 the live set was TAO (waiting), FET+PHA (triggered), MEGA (waiting). Now: **TAO swing → triggered, PHA swing → triggered, MEGA intraday → triggered** (all managed), and **FET swing → stopped (−1R)**; **OPG / WLD / RIF swing also stopped**. **No new A/B triggered since 14:53.** Scalp/intraday still produce zero A/B.
- **Macro overlay turned two-sided:** US–Iran draft MoU persists (mild risk-on) but is **still unsigned/disputed** (WebFetch Jun 12: "no final decision," needs Trump sign-off), and a **risk-off counter-headline** ("Israeli military preparing for possible fire," Telegram 14:10) now sits alongside it. Net: binary at the wall, less cleanly risk-on than the 16:23 framing.
- **HYPE / perps-DEX basket de-rated:** external check shows the Arthur-Hayes **$18M HYPE exit was Jun 4 (~10 days old)** — the `perps_dex_narrative` basket primary rests on a **stale, bearish** catalyst, not a fresh long trigger. Treat HYPE basket as avoid/context, not actionable.
- **Leaders unchanged:** ZKC (+39%, 12.4× vol), BANANAS31 (+27%), OPG (+19%) still lead but all **>2 ATR extended → do-not-chase**; MEGA/MITO/TAO still present.
- **Stocks:** unchanged — closed; invest-mode A/B paused. UNH legal flag (DOJ probe) persists.
- **Thesis:** unchanged but **marginally more cautious** — same cautious-risk-on transition, with a more balanced (two-sided) macro and a day of swing stop-outs confirming the chop.

## 5. Catalyst Coverage

- **news_items today: 241**; **mapped (non-null symbol): 35**; **unmapped: 206 → 85.5% unmapped.** **narrative_baskets: 3.** (Report §5b "unique events today: 513" — same weak-mapping picture on the larger denominator.)
- ⚠️ **CATALYST MAPPING WEAK THIS RUN — USE CATALYST LAYER AS CONTEXT, NOT FINAL DECISION.**
- **Top unmapped "high-importance" rows are noise, not catalysts** — they are `t.me/lookonchain` join/welcome messages ("Hey @user, welcome to Lookonchain") and a share-link, all carrying an **anomalous importance = 1.88** (>1.0). This is an ingestion/normalization defect inflating both the unmapped count and the importance ranking → see §14 TODO `lookonchain-spam` and `importance-overflow`.
- Active baskets: **momentum_breakout** (wait_pullback; primary MITO, CHIP; fresh <1h) · **perps_dex_narrative** (wait_pullback; HYPE +DYDX/GMX/ASTER — **stale, bearish, avoid**) · **delisting_thin_liquidity** (avoid_low_liquidity; no primary — World-Cup fan-token noise).
- Recurring >50% unmapped across runs → §14 TODO (symbol-resolver + source-filtering).

## 6. Market Landscape

- **Crypto (fresh, desk 13:00 UTC snapshot):** BTC **transition_up**, ETH **downtrend**; breadth **67.5% > EMA20 / 55% > EMA50**; BTC ATR pct **3** (very compressed → expansion risk both ways). Strongest: ZKC (100, +39%, chase), BANANAS31 (94, +27%), OPG (92, +19%), MEGA (92, +17%), MITO (84, +20%), RIF (81). Weakest: STG (−37%), TRUMP (−9%), HMSTR (−8%), NIGHT (−8%). Narrative: **AI mixed** (TAO/FET/NEAR), Memes mixed, RWA/L2/Gaming quiet. Derivatives: leaders mostly price-up + OI-up (fresh positioning, crowding normal/low); funding broadly neutral; ZKC funding −0.02 + crowding elevated → squeeze-prone if chased.
- **External macro:** BTC **~$64,385** (Jun 14) on the $64K weekend wall, down from late-May ~$82K; sub-$64K dips triggered ~$1.1B liquidations in the prior 24h. US–Iran de-escalation draft supports a $65K test **if** it firms; "Israeli military preparing for possible fire" headline is the offsetting risk-off tail. Desk macro/geopolitics risk **25/100**, BTC bias neutral/data-watch. Recovery/transition, **not** a confirmed uptrend.
- **Stocks: CLOSED (Sunday) — no US session.** Live A/B are invest/swing-mode, **paused (watchlist_only, 0× sizing)**: LLY (A long), AMD/SMH (B long), META/NFLX (B short), UNH (B long — **DOJ legal flag, see §7 Candidate 4**). Planning only; re-evaluate at **Monday RTH**.

### Market Mood / Risk Routing  (REQUIRED — PART 4)
- **Crypto mood:** cautious **risk-on / transition, two-sided** — BTC transition_up but pinned on the $64K wall, breadth flat 67.5%, vol compressed, macro now binary. Route, don't chase.
- **Stocks mood:** **closed** (weekend) — planning only; no RTH confirmation until Monday.
- **Dominant narrative:** **AI** (Bittensor/TAO, FET, NEAR) + small-cap **momentum_breakout** (MITO, CHIP); macro overlay = US–Iran de-escalation **vs** Israel-fire tail.
- **Preferred side now:** **longs on a held pullback** in AI/RS leaders; **catalyst-backed** preferred; **wait-for-trigger** otherwise. Shorts only on a failed retest if BTC loses the wall.
- **Best long candidate:** **none fresh-clean** — TAO (best catalyst-backed) is already **triggered** (manage, not initiate). Fresh long-watch: **MITO/USDT** — trigger: held pullback into **0.0202–0.0209** with volume, BTC holding the wall.
- **Best short candidate:** **none clean** — weakest names already dumped (STG −37% but squeeze-prone OI-up; HMSTR −8%). Trigger: BTC loses transition_up / the $64K wall, then short the **failed retest** of a weak high (e.g. STG into 0.2638–0.2732, NIGHT into 0.0316–0.0319).
- **Best catalyst-backed candidate:** **TAO/USDT** (Bittensor subnet-demand / supply-squeeze; externally corroborated) — but now triggered → manage toward target, add only on a pullback-hold.
- **What to avoid:** chasing extended leaders (ZKC/BANANAS31/OPG >2 ATR); MEGA chase + Jun-23 token-unlock overhang; HYPE/perps-DEX (stale bearish catalyst); thin/MEXC + World-Cup fan-token (delisting_thin_liquidity) names; no-catalyst weekend momentum longs (weekend bucket negative); any stock entry (closed).
- **What would change the view:** BTC **breaking and holding above the $64K wall toward $65K** with breadth >EMA50 rising = add long conviction; BTC **rejecting/losing the wall** (or Israel-fire headline confirming) = shift to failed-retest shorts; Monday RTH for any stock idea.

## 7. Candidate Deep Dives (≤5)

### Candidate 1 — TAO/USDT (crypto, swing, LONG B 65.4, **triggered**) — BEST CATALYST-BACKED, NOW MANAGE
- Entry ~259.77–263.39, SL ~255.34, tp1 ~273.05; current desk price ~265.8; AI/momentum_breakout narrative; RS vs BTC +6.8%.
- **Catalyst (internal + externally corroborated prior run):** Bittensor subnet-demand / post-halving supply squeeze; AI is the dominant live narrative.
- Mood-aligned? **Yes** (AI, risk-on-transition favors RS-leader longs). Reacted? Partly. Chasing? Signal already **triggered** → manage, do not initiate. Overextended? Price near upper zone — fresh adds only on a held pullback. Actionable now? **Manage** toward tp1; invalidate <255.34 / BTC losing the wall.
- **Final verdict: HOLD / MANAGE (triggered). Manage toward tp1 ~273; SL ~255.34; add only on a held pullback into 259.77–263.39 with volume; size down (weekend).**

### Candidate 2 — MITO/USDT (crypto, scalp 64.4 / intraday 59.2, C — WATCHLIST) — BEST FRESH LONG-WATCH
- Watch-only pullback zone **0.0202–0.0209**; invalidation 1h close <0.0193; tp1 0.0228. Current ~0.0212; ATR 0.0016; support 0.0178 / resistance 0.0257. RS vs BTC +19.5%, vol 1.25×, +19.9% 24h / −6.3% 7d. `momentum_breakout` basket primary.
- Mood-aligned? Yes (RS-leader long). Reacted? Yes (+20% 24h) — **price has already moved**; entry-now would be late/chasing. Retest structure? Yes — plan **demands** a pullback into 0.0202–0.0209, not a chase. Overextended? Not >2 ATR, but no fresh verified catalyst (pure momentum). Actionable? **Only** on a held pullback into the zone with volume + BTC holding the wall.
- **Final verdict: LONG-WATCH (best fresh). Pullback-only into 0.0202–0.0209 with volume; no chase; invalidate <0.0193. Below active threshold — watchlist, not a Telegram-actionable.**

### Candidate 3 — STG/USDT (crypto, scalp 59.8 / intraday 56.3, C — WATCHLIST) — BEST SHORT-WATCH (SQUEEZE-CAUTION)
- Failed-bounce/retest short zone **0.2638–0.2732**; invalidation 1h close >0.2848; tp1 0.2386. Current ~0.2596; 24h **−36.99%** but **7d +21.65%** (the dump is mean-reversion off a pump). Derivatives: **price-down + OI-up = fresh shorts pressing, squeeze risk if price reclaims.**
- Mood-aligned? Only if BTC weakens (two-sided macro). Reacted? Yes — already −37%, **late to initiate fresh**. Chase-risk? **Yes on the short side** — pressing a name already down 37% into rising OI is squeeze-prone. Actionable? Only on a **failed retest** into 0.2638–0.2732 with a clear stop above the swing high.
- **Final verdict: SHORT-WATCH (caution). Failed-retest only into 0.2638–0.2732, stop >0.2848; do NOT press the breakdown — OI-up squeeze risk. Watchlist, not actionable now.**

### Candidate 4 — UNH (stocks, invest/swing, LONG — paused) — LEGAL/HEADLINE RISK, AVOID
- **LEGAL/HEADLINE RISK:** UnitedHealth faces a **DOJ criminal probe** extending to Optum Rx / physician reimbursement; shares fell ~16% on the fraud-investigation news (QuiverQuant; Fierce Healthcare — internal catalyst rows, single_source, importance 0.73). A **long** UNH signal contradicts an active DOJ-probe headline.
- Mood-aligned? N/A — stocks closed. Actionable? No. Even at Monday RTH a long into an open DOJ criminal probe is a contradiction.
- **Final verdict: AVOID / MANUAL REVIEW REQUIRED. Do not treat UNH long as actionable while the DOJ probe headline is live; revisit only with verified resolution at Monday RTH.**

### Candidate 5 — BTC/USDT (macro proxy, no live A/B) — THE BINARY AT THE WALL
- No tradable A/B; this is the regime gate for every crypto idea. **~$64,385**, on the $64K weekend wall; ATR pct 3 (coiled). Two-sided macro: US–Iran de-escalation (unsigned draft, risk-on tilt) vs Israel-fire Telegram headline (risk-off tail).
- Mood-aligned? It **defines** the mood. Actionable? Not directly — it is the trigger condition. Hold >$64K toward $65K = green-light pullback longs; lose the wall = green-light failed-retest shorts.
- **Final verdict: REGIME GATE — wait for the wall to resolve. No direct trade; gates all candidates above.**

## 8. Best Candidates Ranked

No clean Telegram-actionable A/B this window (crypto scalp/intraday are all C-tier; carried A/B are triggered/managed or stopped; stocks closed). Per PART 9, the watch list with exact triggers:

1. **Long-watch (fresh):** **MITO/USDT** — trigger: held pullback into **0.0202–0.0209** with volume + BTC holding $64K wall; invalidate <0.0193.
2. **Catalyst-backed (manage):** **TAO/USDT** (triggered) — manage toward tp1 ~273, SL ~255.34; fresh adds only on a held pullback into 259.77–263.39.
3. **Short-watch:** **STG/USDT** — trigger: **failed retest** into 0.2638–0.2732 with stop >0.2848 **and** BTC losing the wall; do not press (OI-up squeeze risk). Alt: NIGHT failed retest 0.0316–0.0319.
4. **Avoid:** UNH (DOJ probe), HYPE/perps-DEX (stale bearish catalyst), ZKC/BANANAS31/OPG (>2 ATR chase), MEGA (Jun-23 unlock + chase).

## 9. Avoid / No Trade (this decision window only — scanner continues)

- **Chase-extended longs:** ZKC (+39%, 12.4×), BANANAS31 (+27%), OPG (+19%) — all >2 ATR from EMA20; wait for pullback.
- **MEGA/USDT:** no fresh catalyst + Jun-23 token-unlock overhang + micro-cap; pullback-only, no carry into the unlock.
- **HYPE / perps-DEX basket:** catalyst (Hayes $18M exit) is ~10 days old and bearish — avoid as a long thesis.
- **STG breakdown chase (short):** OI-up squeeze risk; failed-retest only.
- **Thin/MEXC + World-Cup fan-token names** (delisting_thin_liquidity basket): avoid low-float dumps.
- **All stocks:** closed (Sunday) — no entries; UNH additionally legal-flagged.
- This "no clean trade" verdict applies to **this 4-hour window only** — it is **never** an instruction to pause the scanner, tracking, or data collection.

## 10. Main Risks

- **Macro binary at the wall:** BTC pinned at $64K with compressed ATR (pct 3) → a sharp expansion is likely; direction hinges on the unsigned US–Iran draft (could firm = up, or the Israel-fire tail confirming = down). Headline-reversal risk both ways.
- **Weekend bucket is statistically poor** (prior signal-stats weekend WR ~5%, PF 0.25); thin liquidity amplifies fakeouts.
- **Authoritative performance is weak, not strong:** the report headline A/B metric is **WR 16.9%, PF 1.00, stop-rate 39.8%** over 89 signals — breakeven at best. (NB: a raw row-count of `signal_outcomes` yields absurd 94–100% winrates because that table stores repeated per-cycle snapshot rows, not unique resolutions — do **not** use it for performance; see §14 `outcomes-snapshot-overcount`.)
- **Catalyst layer is ~6h stale and 85% unmapped** → low confidence; use as context only.
- **Source ingestion:** WebSearch/WebFetch available and used; internal news is mostly single_source. CLI import hung — DB read directly instead (no data loss, but the convenience path is degraded). Source-ingest CLI status noted at end of §13.

## 11. Action Plan — next 4 hours

1. **Watch the BTC $64K wall.** Hold-above toward $65K with rising breadth → enable pullback longs (MITO zone first). Lose-the-wall (or Israel-fire confirmation) → enable failed-retest shorts (STG/NIGHT).
2. **Manage, don't initiate, the triggered crypto A/B:** TAO swing (→ tp1 ~273, SL 255.34), PHA swing, MEGA intraday — respect stops; no fresh size into the weekend chop.
3. **MITO long-watch:** only on a held pullback into 0.0202–0.0209 with volume; otherwise stand aside.
4. **No shorts pressed into squeeze risk** (STG OI-up); require a failed retest.
5. **Stocks:** nothing actionable until **Monday RTH**; queue UNH as AVOID pending DOJ-probe resolution, and re-confirm LLY/AMD/SMH/META/NFLX at the open.
6. Scanner, tracking, catalyst collection, and outcome recording continue unchanged.

## 12. Final Verdict per Mode

- **Crypto scalp:** **NO clean A/B — watchlist only.** Best name MITO (64.4) pullback-only. Low-confidence bucket; wait for cleaner execution.
- **Crypto intraday:** **NO clean A/B — watchlist only.** MITO/STG/NIGHT watch; no-catalyst momentum in chop is net-negative — demand RS-leader + breakout confirmation.
- **Crypto swing:** report stale (~14h); live A/B = TAO/PHA triggered (manage), FET/OPG/WLD/RIF stopped. **Manage existing; no fresh swing initiation off stale data.**
- **Stocks intraday/swing/invest:** **CLOSED (Sunday)** — planning only; UNH AVOID (legal). Re-evaluate Monday RTH.

## 13. Sources

External (this run):
- [Iran confirms memorandum of understanding with US in final stages — CryptoBriefing (Jun 12, 2026, WebFetch-verified)](https://cryptobriefing.com/iran-us-memorandum-understanding-final-stages/)
- [Iran and US outline 14-point draft understanding to halt conflict and lift sanctions — CryptoBriefing](https://cryptobriefing.com/iran-us-14-point-draft-understanding/)
- [Bitcoin falls below $64,000, triggers $1.1B in liquidations — CryptoBriefing](https://cryptobriefing.com/bitcoin-falls-below-64000-triggers-11b-in-liquidations/)
- [Bitcoin price today ~$64,385 (Jun 14, 2026) — MetaMask price page](https://metamask.io/price/bitcoin)
- [Arthur Hayes Shocks Hyperliquid Holders With $18M HYPE Exit (Jun 4, 2026) — Coinlaw](https://coinlaw.io/arthur-hayes-hype-exit-hyperliquid-price-drop/)
- [Hyperliquid (HYPE) Tumbles After Arthur Hayes Exits $18M Stake — Blockonomi](https://blockonomi.com/hyperliquid-hype-tumbles-after-arthur-hayes-exits-18m-stake-despite-150-forecast/)

Internal (read-only): `data/reports/scalp/2026-06-14_12-46_scalp_report.md`; `data/reports/intraday/2026-06-14_13-22_intraday_report.md`; `data/catalysts/2026-06-14/{catalyst_events.jsonl,narrative_baskets.jsonl,catalyst_cycle_09-29.md}`; `db/crypto_ai_desk.sqlite` (proposed_signals, signal_outcomes, signal_alerts, news_items, watchlist_alerts). UNH/SMCI legal rows: SEC EDGAR / QuiverQuant / Fierce Healthcare (single_source, internal news_items).

_Source-ingest CLI (`scripts.ingest_enriched_review_sources --asset-class crypto`) status: **succeeded** — `input: 6 | valid: 6 | rejected: 0; wrote 6 row(s) to news_items` (idempotent UPSERT on url). Citations JSON: `data/raw/enriched_review_sources/2026-06-14T18-39-00.json`._

_No fabricated TradingView/chart observations — only local OHLCV/ATR/EMA fields used. Telegram "welcome"/share-link rows filtered out as non-news (see §14). No uncited stats; where a figure was unavailable it is marked so._

## 14. Fix Requests / TODO

### TODO-lookonchain-spam
- **issue:** `t.me/lookonchain` join/welcome messages ("Hey @user, welcome to Lookonchain") and share-links are ingested as `news_items` and surface as top catalysts, polluting catalyst coverage.
- **evidence:** `news_items` today — top unmapped rows are `t.me/lookonchain` "welcome to Lookonchain" with importance 1.88; 206/241 unmapped (85.5%).
- **suggested manual fix:** add a source/title filter in the Telegram-ingest path to drop welcome/join/share-link messages from `lookonchain` before they enter `news_items`.
- **priority:** medium
- **first observed:** 2026-06-14 18:39 EEST

### TODO-importance-overflow
- **issue:** `news_items.importance` exceeds its expected 0–1 range (value **1.88** on Lookonchain spam), inflating the importance ranking used by catalyst diagnostics.
- **evidence:** multiple `news_items` rows today with `importance = 1.88`.
- **suggested manual fix:** audit the importance-scoring/normalization step; clamp or normalize to [0,1] and re-check why spam rows score >1.
- **priority:** medium
- **first observed:** 2026-06-14 18:39 EEST

### TODO-catalyst-mapping-weak
- **issue:** symbol mapping for catalysts remains <50% (14.5% mapped this run; ~84% unmapped in the prior run too) — recurring across runs.
- **evidence:** 35/241 `news_items` mapped today; prior review 236/1453.
- **suggested manual fix:** improve the symbol resolver in the catalyst layer (ticker/entity extraction) and exclude non-market sources; track mapped% as a health metric.
- **priority:** medium
- **first observed:** carried (re-confirmed 2026-06-14 18:39 EEST)

### TODO-outcomes-snapshot-overcount
- **issue:** `signal_outcomes` appears to store repeated per-cycle snapshot rows per signal; naive row-count aggregation yields impossible winrates (e.g. stocks-intraday-B n=22,871 WR 100%, crypto-swing-B n=998 WR 98%), wildly inconsistent with the authoritative headline (A/B WR 16.9%, PF 1.00).
- **evidence:** direct SQL `group by asset/mode/tier on final_outcome in ('win','loss')` over 14d returns n in the tens of thousands; report `signal-stats` returns n=89 for the same week.
- **suggested manual fix:** confirm whether `signal_outcomes` is append-per-check; if so, ensure any ad-hoc analytics dedupe to latest-per-signal_id (the `signal-stats` CLI likely already does — document this so future manual queries don't misread it).
- **priority:** low
- **first observed:** 2026-06-14 18:39 EEST

### TODO-cli-import-slow
- **issue:** `python -m src.cli ...` read-only subcommands (active-signals / signal-stats / detect_untracked_legacy_alerts) are **extremely slow to start** — `active-signals` took **~15 minutes** to return this cycle, forcing a fallback to direct read-only SQL (which it later confirmed). NB: `scripts.ingest_enriched_review_sources` (same `src.config`/`src.storage` imports) returned in <120s — so the latency is specific to the `src.cli` entrypoint, likely eager exchange/data/agent init at module load rather than the storage layer.
- **evidence:** `active-signals --asset-class crypto` produced no output for >15 min then returned 11 rows; same session `ingest_enriched_review_sources` returned <120s and wrote 6 rows. (Also flagged "very slow / returned after drafting" at 16:23.)
- **suggested manual fix:** profile the `src/cli` entrypoint specifically; lazy-load heavy deps (exchange clients, agents, models) so read-only subcommands like `active-signals`/`signal-stats` start in seconds.
- **priority:** medium
- **first observed:** 2026-06-14 18:39 EEST (recurring — also 16:23)

### TODO-perps-basket-stale-catalyst
- **issue:** `perps_dex_narrative` basket lists HYPE as primary on a catalyst (Hayes $18M exit) that is ~10 days old and bearish, with `freshness: unknown` — risks being read as a fresh long trigger.
- **evidence:** `narrative_baskets.jsonl` perps_dex_narrative freshness "unknown"; external sources date the Hayes exit to Jun 4, 2026.
- **suggested manual fix:** require a freshness window on basket catalysts; demote/flag baskets whose only event is >72h old or directionally bearish vs the basket's long playbook.
- **priority:** low
- **first observed:** 2026-06-14 18:39 EEST
