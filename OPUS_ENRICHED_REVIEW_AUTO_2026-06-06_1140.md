# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:40 EEST

- **Generated:** 2026-06-06 11:40 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`, **Europe / pre-US context** slot 11:30). **Saturday — US/EU equity markets CLOSED**; crypto is the only live actionable class. Stock signals (50 active) = planning/watchlist context only.
- **Slot focus:** how crypto traded through the EU morning after Friday's hot-jobs risk-off + the Zcash-bug shock, and whether the multi-day breakdown is still shortable into the weekend or now too late/oversold to chase.
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-06_0445.md` (crypto overnight / Asia review, 04:45 EEST, ~7h ago — see §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). Verified this run: (a) **BTC below $60,000** — lowest since Oct 2024, hot US jobs report (172k vs 85k est) killed rate-cut hopes, ~$1.6–1.7B 24h liquidations, Saylor/Strategy turned seller + 10-day ETF outflows (CoinDesk WebFetch HTTP 200, ~$60,768 at print); (b) **Zcash critical Orchard counterfeiting bug** — disclosed Jun 5, present since May 2022, found via Anthropic Opus 4.8, ZEC −38% to ~$458 (CoinDesk WebFetch HTTP 200); (c) **ETH 13-month low ~$1,540** on Bitcoin slide + Zcash DeFi-contagion fear.
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; all internal price/structure is local OHLCV/ATR/EMA report fields + cited external prints.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

- **The bearish thesis kept paying, but every short is now late and the books are sitting on capitulation levels.** The cause that drove Friday's risk-off — a **hot US jobs print (172k vs ~85k est, unemployment 4.3%)** that crushed rate-cut hopes and revived rate-*hike* odds — is verified, and the move extended: **BTC broke below $60,000** (lowest since Oct 2024, −~20% on the week, −52% from the Oct-2024 peak), with **~$1.6–1.7B liquidated in 24h**. Layered on top: **Strategy (Saylor) turned seller** and spot-BTC ETFs saw persistent outflows.
- **The Zcash bug is now a confirmed, primary-sourced supply-integrity event, and the desk is still carrying a ZEC LONG.** Zcash disclosed a **critical Orchard-pool counterfeiting vulnerability** (could mint undetectable counterfeit ZEC; live since May 2022; found via Opus 4.8) on Jun 5 → ZEC **−38% to ~$458**. The active-signals table still shows **ZEC/USDT B swing LONG (tp2_hit, expires 06-07)** — a direct signal-vs-catalyst **contradiction**. Any residual long must be treated as **AVOID / close**, not a live position (§7.1).
- **Report generators failed AGAIN this cycle — crypto intraday levels are ~19h stale.** Cycle 1 (09:48→11:27) `[FAIL]`ed both scalp and intraday reports (timeout 2700s each), the same regression flagged in the last 3 reviews. The scalp report *did* regenerate once at 05:38 (~6h old, usable for context); **intraday has not regenerated since 06-05 13:54 UTC (~19h — stale).** Direction is valid; **execution prices must be re-pulled before any entry.**
- **No A-tier, no B-tier fresh setups; the engine is correctly short-biased but the edge has shifted from "initiate" to "manage / wait for a bounce."** Regime: high-volatility danger, BTC+ETH downtrend, altcoin breadth ~21% above EMA20, **BTC ATR percentile 97 (extreme)**. The only live conditional trigger is **TON/USDT intraday short on a retest of 1.551** (expires ~13:54).
- **Net verdict: Crypto = short-biased but NO-CHASE into the weekend.** Manage runners, sell *retests* not weakness, and stand down at BTC $60k / ETH $1.5k liquidation magnets. **Close/avoid the contradicted ZEC long.** **Stocks = no action (closed).** Catalyst layer **context-only (63% unmapped).**

---

## 2. Data Used

**Internal — crypto reports:**
- `data/reports/scalp/2026-06-06_02-38_scalp_report.md` (generated 05:38 EEST, data 02:15 UTC; **~6h — usable context**; regime *high-volatility danger*, BTC+ETH downtrend, breadth above EMA20 **20.83%**, BTC ATR pct **97 "elevated/extreme"**). **No A-tier, no B-tier — all watchlist** (top ZRO 59.6, ETH 59.3).
- `data/reports/intraday/2026-06-05_13-54_intraday_report.md` (data 06-05 13:54 UTC; **~19h — STALE**, regen failed this cycle).
- `data/reports/swing/2026-06-05_14-34_swing_report.md` (data 06-05 14:34 UTC; **~18h — STALE**).
- Stocks reports (intraday 06-05 20:17, swing 19:07, invest 14:55) — **weekend, market closed → context only, not re-read in detail.**

**Catalyst / narrative:** `data/catalysts/2026-06-06/` — `catalyst_events.jsonl` (**327 rows** today, cumulative), `narrative_baskets.jsonl` (**3 baskets**), latest `catalyst_cycle_08-25.md` (mtime 11:25 — fresh).

**LLM packets:** `data/processed/llm_analysis_packet.md` (crypto), `data/processed/llm_stocks_packet.md` — present; not the decision driver this slot (reports + CLI + external lead).

**CLI / DB (read-only, this run):** `active-signals` crypto **8** (was 13 at prior review), stocks **50** (closed, context); cycle `signal-stats` crypto week — **headline A/B sample=70, triggered=53, 13W/19L, winrate 24.5%, PF 1.63, avgR 0.23, totalR +12.0**; `detect_untracked_legacy_alerts --since 2026-06-06` → **None (0)** (was 2 at prior review — improved). DB `data/crypto_ai_desk.db` (live, collector writing).

**External (this run — cited §13):** BTC <$60k / hot-jobs / liquidations (CoinDesk WebFetch HTTP 200; crypto.news, CNBC, Coinpaper); Zcash Orchard counterfeiting bug (CoinDesk WebFetch HTTP 200; Decrypt, Yahoo Finance); ETH 13-month low (SquaredTech).

**Unavailable / blind:** live tick prints; TradingView/Chrome chart verification (not loaded); liquidation heatmaps / order-book / CVD; **fresh crypto intraday execution levels (report ~19h stale, regen failed again).**

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-06_default_schedule/`.
- `scheduler.log` mtime **11:27:09 EEST** (~13m); latest cycle summary `cycle_01_09-48_summary.md` mtime **11:27:07** (~13m). Both **< 3h → NO DEFER.**
- Cycle 1 ran in **weekend (crypto-only) mode** (stocks disabled, daily swing/invest disabled): steps **ok=9 failed=2**. The **two failures are crypto scalp report + crypto intraday report, both timed out after 2700s** — same regression as the prior 3 reviews. Track-signals OK (checked 290–291, cum tp_hits 169–170), catalyst scan OK (events=141 this cycle, baskets=3), monitor 90-min background OK, obsidian daily/dashboard OK.
- **Report freshness this run:** scalp **~6h** (regenerated 05:38, *usable*), intraday **~19h STALE**, swing **~18h STALE**. Scalp recovered once since the 04:45 review, but **this cycle's regen FAILED again** → see §14 `TODO-crypto-report-staleness`. Direction context valid; **intraday/swing levels stale — re-pull before any crypto entry.**

---

## 4. What Changed vs Previous Review (Asia 04:30 → Europe 11:30)

- **The breakdown extended and broke another round number.** At 04:45 BTC was ~$62.5k "just above $60,900 liquidation." This slot BTC has **broken below $60,000** (lowest since Oct 2024) and ETH has printed a **13-month low ~$1,540** (was breaking <$1,550 overnight). The thesis kept paying; the *runway left* shrank further.
- **The macro narrative consolidated around jobs/Fed, not geopolitics.** The prior review's headline NEW vector was the **Iran / Strait of Hormuz drone escalation**. That item was **NOT re-verified this slot** and does **not** appear in this morning's BTC-driver coverage (CoinDesk lists jobs/Saylor/ETF-outflows/Zcash, Nasdaq −2% — no Iran). Treat Iran/Hormuz as **carry-forward, receded from the dominant driver set** — still a latent weekend gap risk but no longer the lead.
- **Zcash bug upgraded from "contagion rumor" to primary-sourced supply-integrity event.** 04:45 noted "ZEC exploit contagion (−30/−50%, Hayes dumped ZEC)." This slot it is **confirmed via CoinDesk/Decrypt**: critical Orchard counterfeiting vuln, disclosed Jun 5, undetected since May 2022, ZEC −38% to ~$458. **And a ZEC/USDT swing LONG is now visible in active-signals (new vs the prior set)** — a fresh contradiction case (§7.1).
- **Untracked legacy alerts: 2 → 0 (IMPROVED).** Prior run had FET + ETH untracked; detector now returns **None**. Good — the headline PF/winrate is less contaminated this slot.
- **Active crypto signals: 13 → 8** (overnight expiries: AVAX, FET, PUMP, DASH dropped; BTC scalp short, ZEC/XLM swing longs, EPIC/C surfaced). **BTC scalp short is now EXPIRED (08:38).**
- **Catalyst mapping improved in ratio but still weak:** 72.2% → **63% unmapped** (327 rows today vs 2982 — early-day folder, lower base). Still > 50% → context-only.
- **Signal-stats ≈ flat:** winrate 25.0% → 24.5%, PF 1.56 → 1.63, totalR +10 → +12. Mode split still shows scalp the weak bucket (PF ~0.14) and the "anetdotal/ane" bucket strong (n=6, PF 12) — small-sample, not actionable.
- **Thesis: unchanged in direction (short-biased risk-off), conviction on *fresh entries* still LOW** — price now at/through major support/liq levels; edge = manage runners + the contradicted-ZEC cleanup, not new initiation.

---

## 5. Catalyst Coverage

- Raw `catalyst_events.jsonl` (trading-day 2026-06-06): **327 rows** (cumulative across cycles 03-24 + 08-25).
- Mapped (non-empty symbol): **120** · Unmapped (empty `symbol:""`): **207** · **Unmapped = 63%.**
- This cycle's scan (`cycle_08-25`): 141 events — other_news 136, **legal_risk 4**, product_launch 1. `narrative_baskets`: **3** —
  - `ai_narrative` (playbook related_beta_rotation, <6h, primary **NEAR/RENDER/TAO/FET**, related WLD/ASTER) — note the sample headline is **Arthur Hayes turning bearish** on ZEC/NEAR/WLD after selling the top → this is a *downside* rotation, not a long basket.
  - `perps_dex_narrative` (playbook wait_pullback, <24h, primary **HYPE**, related DYDX/GMX/ASTER) — driven by the Machi/Hyperliquid liquidation saga.
  - `momentum_breakout` (playbook wait_pullback, <1h, primary **HEI** +14.7%, vol 0.63x) — pure momentum, no confirmed catalyst.
- **⚠ CATALYST MAPPING WEAK THIS RUN (63% unmapped > 50%) — use the catalyst layer as CONTEXT, NOT a final decision input.** Top unmapped/low-quality headlines are stock/finance noise and a t.me scam-promo (e.g. "Big thanks to Kathy Lien… my trading account is thriving" — a withdrawal-shill spam row ingested as a catalyst), plus equity legal items mis-paired to `/USDT` (see below). Same resolver root cause as prior runs (§14 `TODO-catalyst-symbol-resolver`).

---

## 6. Market Landscape

- **Regime (internal, scalp 05:38):** high-volatility **danger**; BTC downtrend, ETH downtrend; altcoin breadth above EMA20 **20.83%**, above EMA50 18.75%; **BTC ATR percentile 97 (extreme)**. Recommended style: *reduce size or no trade until structure settles.*
- **External levels (verified this run):** **BTC < $60,000** (~$60,768 at CoinDesk print, −~20% wk, −52% from Oct-2024 ~$126k peak, lowest since Oct 2024). **ETH 13-month low ~$1,540** (scalp desk shows ETH ~1,575, support 1,540). **~$1.6–1.7B** 24h liquidations. Drivers: **hot jobs (172k vs 85k est)** → rate-cut hopes dead, Polymarket ~52% / CME ~43% odds of a *hike* by year-end; **Saylor/Strategy turned seller**; **10-day spot-BTC-ETF outflows**; **Nasdaq −2%** risk-off; **Zcash counterfeiting-bug contagion** draining DeFi TVL on fear of similar hidden flaws.
- **Money flow (internal):** every "strongest" name is down double-digits on the day (PUMP/XPL/AR/ICP/ZEN/FIL/AAVE all −11% to −16%) — the score is ranking *least-bad shorts in a bleed*, not strength. Lone green outlier ALLO +29.8% (low-liquidity, MEXC). Narrative heat: Memes rising (attention 100, DOGE), RWA/AI mixed, L2/DePIN/Gaming quiet.
- **Derivatives:** funding mostly mildly negative across venues (FIL −0.00039 OKX, ICP/AAVE negative), crowding mostly normal/low — deleveraging tape, not a crowded-long blowup setup; squeeze risk is *reflexive bounce*, not positioning-forced.
- **Equities (closed, context):** weekend, no cash anchor. Crypto trades the jobs/Fed + Zcash narrative alone into Sunday.

---

## 7. Candidate Deep Dives (≤5)

### 7.1 ZEC/USDT — B / swing / LONG — tp2_hit (active, expires 06-07) — **CONTRADICTION / INTEGRITY**
- Active-signals row: score 65.2, entry **561.89–567.42**, invalidation 555.12, **status tp2_hit, expires 2026-06-07T22:56**. This is a **LONG**.
- **External (verified, primary):** Zcash disclosed a **critical Orchard-pool counterfeiting vulnerability** Jun 5 (could mint undetectable counterfeit ZEC; live since May 2022; fixed Jun 1; found via Opus 4.8). ZEC **−38% in 24h to ~$458** (CoinDesk), other outlets cite −40/−60% to ~$306. Worst-performing major asset.
- **Contradiction (§F-2):** the desk holds a **LONG** on a token undergoing a confirmed **supply-integrity exploit** and a 38–60% crash. The long *entry* (561) hit tp2 while ZEC was higher; the move since is a vertical collapse far below the 555 invalidation. The signal is effectively a **stale/realized long that should be flat**, yet it surfaces as "active."
- **Price-reaction / chase (§J):** price has fully (violently) reacted; the level structure in the signal (561/555) is obsolete by ~$100+. There is **no clean re-entry** either side — a counterfeiting bug is a fundamental impairment, not a dip.
- **Verdict: AVOID / CLOSE. Do NOT treat as a live long. Manual review to flatten/expire the row.** Integrity flag → §14.

### 7.2 BTC/USDT — B / scalp / SHORT — **TRIGGERED but EXPIRED (08:38)** — macro anchor
- Active-signals row: score 66.6, entry 61,179–61,610, invalidation 62,136, **status triggered, expires 2026-06-06T08:38** → **already lapsed ~3h ago.**
- **External (verified):** BTC broke **< $60,000**, lowest since Oct 2024, on the hot jobs print; $1.6–1.7B liquidations; Saylor selling; ETF outflows.
- **Price-reaction / chase (§J):** the short *worked* (price fell through the entry into the $60k zone) but the signal has **expired** and price is now **at the $60,000 liquidation magnet** — initiating/holding fresh short here is shorting into the level where capitulation bounces start. ATR pct 97 = whipsaw risk both ways.
- **Verdict: NO fresh short. The triggered scalp short is expired — treat as closed/realized. Direction down, conviction-on-new-entry LOW. Re-pull live BTC level (scalp source ~6h, intraday ~19h).**

### 7.3 ETH/USDT — macro driver / watchlist short (no fresh tradable signal)
- Scalp report: **watchlist-only short, score 59.3**, current ~1,575, support 1,540, ATR 35.8; volume 0.16x (thin). No active ETH signal in the 8.
- **External (verified):** ETH **13-month low ~$1,540**, hit by BTC slide + **Zcash-bug DeFi contagion** (fear of similar undetected smart-contract flaws → DeFi TVL withdrawals). Overnight sub-$1,550 triggered tens of millions in DeFi liquidations.
- **Price-reaction / chase (§J):** fully reacted; ETH is *at* its support/round-number ($1,540/$1,500). Fresh short = chasing into a squeeze/capitulation magnet; thin 0.16x volume means breakout-confirmation is weak. A $1,500 hold + reclaim is a *nimble mean-reversion long* watch (manual only), not a signal.
- **Verdict: NO fresh short-chase. Watch $1,540/$1,500 — break = continuation (largely priced), hold = squeeze risk. Manual / no-trade.**

### 7.4 TON/USDT — B / intraday / SHORT — waiting_for_entry (the only LIVE conditional)
- Active-signals row: score 65.8, entry **1.5512–1.5695**, invalidation 1.5919, **status waiting_for_entry, expires 2026-06-06T13:54 (~2h left)**.
- **Internal-first:** no fresh TON `news_items`/catalyst match — pure technical breakdown short, regime-aligned.
- **Price-reaction / chase (§J):** entry 1.551–1.5695 is a **sell-the-retest** trigger — it only fills on a bounce back into the zone then rejection, which is the correct no-chase structure (sell strength, not weakness). That makes it the **cleanest** of the active names *if* price retests before 13:54. Source level is from a **~19h-stale intraday report** — re-pull before arming.
- **Verdict: VALID short-on-retest ONLY at 1.551–1.5695 with SL 1.592 — do not market-sell into weakness; skip if no bounce by ~13:54 expiry. Re-pull live TON level first.**

### 7.5 HEI/USDT — momentum_breakout basket (<1h) / counter-tape LONG — **chase risk**
- Basket primary, **+14.7% / 24h, vol 0.63x**, playbook `wait_pullback`, **no confirmed news catalyst** (pure momentum). Also appears in scalp §7b rejected as an RS-leader long *conflicting with regime*.
- **Price-reaction / chase (§J):** a +14.7% green name in a high-vol-danger, BTC+ETH-downtrend tape with breadth ~21% is a **counter-tape long** — exactly the "missing a move beats chasing a bad one" case. Volume 0.63x is not strong confirmation. No catalyst to anchor it.
- **Verdict: AVOID as a long-chase. Watchlist only — `wait_pullback`; would need a real pullback + volume + BTC stabilization, which the regime does not offer.**

---

## 8. Best Candidates Ranked

1. **TON/USDT intraday short** — *conditional only*: arm as sell-the-retest at 1.551–1.5695, SL 1.592; needs a bounce to fill before ~13:54 expiry; re-pull live level. The one structurally-correct live trigger.
2. *(everything else is manage / avoid — see §9.)*

**No clean fresh A-tier entry anywhere; no fresh long; no B-tier setup generated this cycle.** The actionable edge this slot is **risk hygiene** (close the contradicted ZEC long, let the expired BTC scalp short be closed) and **patience**, not new initiation.

---

## 9. Avoid / No Trade

- **ZEC/USDT long** — confirmed critical counterfeiting bug + 38–60% crash; fundamental impairment. Close/avoid; do not treat the "active" row as a live long (§7.1).
- **BTC/USDT fresh short** — expired scalp short; price at $60,000 liquidation magnet; ATR pct 97. Don't chase weakness here.
- **ETH/USDT fresh short** — 13-month low, at $1,540 support / squeeze magnet, thin 0.16x volume. Chasing.
- **HEI/USDT (and any +double-digit green name) long** — counter-tape long in a risk-off downtrend; no catalyst; chase risk.
- **Any fresh breakdown short initiated at market** — BTC $60k / ETH $1.5k are support/liquidation levels where capitulation bounces begin; weekend thinness = two-way gap risk. Short *retests*, never *weakness*.
- **All stocks (50 active rows)** — market closed (weekend); planning/watchlist only. Carries legal-risk flags **SMCI** (8-K indictment, export-control conspiracy) and **UNH** (DOJ antitrust/fraud probe, −16%) — both surfaced as `legal_risk` catalysts mis-paired to `/USDT`; context only this slot, re-check before any stock action Monday.

---

## 10. Main Risks

- **Stale execution levels (HIGH).** Intraday/swing reports ~18–19h old, regen failed again; scalp ~6h. Every price in §7 must be re-pulled live before any action. Dominant operational risk.
- **Oversold squeeze / capitulation bounce (HIGH).** BTC $60,000 and ETH $1,540 are major support/liquidation levels; ATR pct 97; $1.6–1.7B already liquidated. Short-chasing here is asymmetric *against* you.
- **ZEC integrity / contagion (MEDIUM-HIGH).** A confirmed supply-counterfeiting bug is a tail event; "similar-hidden-flaw" fear is actively pulling DeFi TVL (ETH driver). The desk carrying a ZEC *long* is the clearest single risk-hygiene gap this slot.
- **Catalyst layer unreliable (MEDIUM).** 63% unmapped, includes a t.me withdrawal-shill spam row and equity legal items as `/USDT`; do not let it drive a crypto decision.
- **Carry-forward geopolitical gap (LOW-MEDIUM, unverified this slot).** Iran/Hormuz (prior review) not re-verified and off the dominant driver set; latent weekend headline risk only.
- **Ingest CLI risk (LOW).** If `ingest_enriched_review_sources` fails it is logged here and does not block the review.

---

## 11. Action Plan — next 4 hours (into US-closed weekend afternoon)

1. **Re-pull live BTC/ETH/TON/ZEC levels** before any execution — do not trust the 18–19h-stale intraday/swing prices.
2. **ZEC:** treat the "active" swing long as **flat/closed** — do not add, do not defend; manual review to expire the row (§14). A counterfeiting bug is not a dip.
3. **BTC:** the triggered scalp short is **expired** — book it as closed; no fresh short at $60k. Watch for a reclaim of structure vs a flush through $59k.
4. **TON intraday short:** arm only as a **sell-the-retest** at 1.551–1.5695 (SL 1.592); skip if price never bounces there before ~13:54 expiry. No market-sell into weakness.
5. **ETH:** watch **$1,540/$1,500** — hold + reclaim = nimble scalp-long *watch* (manual only); break = continuation that's largely priced. No fresh short.
6. **HEI / green outliers:** watchlist only — `wait_pullback`; no counter-tape long-chase.
7. **Do not initiate any fresh breakdown short at market** into support/liq levels over a thin weekend.
8. **Monitor** for a weekend relief bounce; treat any sharp green candle as squeeze, not reversal-confirmation, until BTC reclaims structure.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** No fresh entry — BTC scalp short expired, price at $60k support, ATR pct 97. Manage/closed only; sell retests, not weakness. Direction short, conviction-on-new-entry LOW.
- **Crypto intraday:** Short-biased but no-chase. **TON** valid only as sell-the-retest at 1.551–1.5695 (SL 1.592) before ~13:54 expiry; re-pull level (19h stale). No other live trigger.
- **Crypto swing:** **ZEC long = AVOID/CLOSE** (confirmed counterfeiting bug). XLM swing long (tp1_hit, expires 06-07) — runner only, no add into the danger regime. No fresh swing initiation.
- **Stocks (all modes):** No action — market closed (weekend). Context only; SMCI/UNH legal flags noted for Monday.

---

## 13. Sources

- [Bitcoin loses $60,000, falls to weakest price since October 2024 (CoinDesk)](https://www.coindesk.com/markets/2026/06/05/bitcoin-loses-usd60-000-falls-to-weakest-price-since-october-2024) — 2026-06-05, **primary_source** (WebFetch HTTP 200; ~$60,768, −20% wk, −52% from peak, $1.6B liquidations, Saylor seller, ETF outflows, Nasdaq −2%).
- [Zcash plummets 38% as developer reveals a major bug that went undetected for four years (CoinDesk)](https://www.coindesk.com/markets/2026/06/05/zcash-plummets-30-as-developer-reveals-a-major-bug-that-went-undetected-for-four-years) — 2026-06-05, **primary_source** (WebFetch HTTP 200; Orchard counterfeiting vuln, disclosed Jun 5, live since May 2022, fixed Jun 1, found via Opus 4.8, ZEC −38% to ~$458).
- [Bitcoin price falls below $60K as hot U.S. jobs report crushes rate cut hopes (crypto.news)](https://crypto.news/bitcoin-price-falls-below-60k-as-hot-u-s-jobs-report-crushes-rate-cut-hopes/) — 2026-06-05, single_source (jobs 172k vs 85k est, unemployment 4.3%).
- [ZEC Crashes 38% as Zcash Discloses 'Critical Counterfeiting Vulnerability' (Decrypt)](https://decrypt.co/370105/zec-crashes-38-as-zcash-discloses-critical-counterfeiting-vulnerability) — 2026-06-05, single_source.
- [Ethereum Price Crashes To 13-Month Low as Zcash bug rattles DeFi (SquaredTech)](https://www.squaredtech.co/ethereum-price-hits-13-month-low-as-zcash-bug-rattles-defi) — 2026-06-05, single_source (ETH ~$1,540, DeFi-contagion fear).
- [Bitcoin Price Crashes Below $60,000 as US Jobs Report Trigger $1.5B Crypto Liquidations (Coinpaper)](https://coinpaper.com/17514/bitcoin-price-crashes-below-60-000-as-us-jobs-report-trigger-1-5-b-crypto-liquidations) — 2026-06-05, single_source (corroborates liquidation magnitude).
- Internal (no external claim): scalp report 2026-06-06_02-38, active-signals/signal-stats/untracked-detector CLI (this run), catalyst_events.jsonl + narrative_baskets.jsonl (2026-06-06). Iran/Hormuz escalation (prior review) — **not re-verified this slot; carry-forward context only.**

---

## 14. Fix Requests / TODO

### TODO-crypto-report-staleness
- **issue:** Crypto scalp + intraday report generators time out (2700s each) and failed to regenerate **again** this cycle — the same regression flagged in the last 3 reviews. Intraday levels are now ~19h stale (scalp recovered once at 05:38 to ~6h).
- **evidence:** `data/scheduled_runs/2026-06-06_default_schedule/cycle_01_09-48_summary.md` steps 2 & 3 both `[FAIL] (timeout) … timed out after 2700 seconds`; intraday report mtime 2026-06-05 13:54 UTC vs run time 11:27 EEST. Prior reviews trace root cause to a hung Binance `exchangeInfo` / per-exchange fetch with no partial-result fallback.
- **suggested manual fix:** profile the scalp/intraday CLI fetch loop; add per-exchange fetch timeouts + partial-result fallback so a single hung call can't blow the 2700s budget; cache `exchangeInfo`; raise/segment the step timeout.
- **priority:** high
- **first observed:** carried from 2026-06-05 23:25 / 2026-06-06 04:45 EEST; reconfirmed 2026-06-06 11:40 EEST.

### TODO-zec-long-contradiction
- **issue:** An active B swing **LONG** on ZEC/USDT (tp2_hit, expires 06-07) remains in `active-signals` while ZEC is undergoing a confirmed critical Orchard-pool **counterfeiting** bug and a 38–60% crash. A supply-integrity exploit should hard-invalidate / force-expire a long irrespective of price levels.
- **evidence:** `active-signals --asset-class crypto` row `sig_5a9e5f5386306226` ZEC/USDT swing long, entry 561.89–567.42, inval 555.12, expires 2026-06-07T22:56; external CoinDesk/Decrypt (Jun 5) confirm the bug + crash to ~$458 (well below the 555 invalidation — the row should already be stopped/expired).
- **suggested manual fix:** (a) confirm the invalidation/stop sweep is actually transitioning longs whose price has blown through `invalidation`; (b) add a catalyst-driven hard-kill for `legal_risk`/security/exploit events that flips any same-symbol active signal to `invalidated`.
- **priority:** high
- **first observed:** 2026-06-06 11:40 EEST.

### TODO-catalyst-symbol-resolver
- **issue:** 63% of catalyst_events are unmapped (empty symbol); the tail includes equity legal headlines mis-paired to `/USDT` (UNH/USDT DOJ probe, SMCI/USDT 8-K indictment) and a t.me **withdrawal-shill spam** row ("Big thanks to Kathy Lien… my trading account is thriving") ingested as a catalyst. Recurring ~63–73% unmapped over many runs.
- **evidence:** `data/catalysts/2026-06-06/catalyst_events.jsonl` total=327, mapped=120, unmapped=207 (63%); `catalyst_cycle_08-25.md` "Legal / regulatory risk" lists `UNH/USDT` and `SMCI/USDT` (both stocks); event `cat_8f755a9f37ca7d54` is a t.me promo-scam title.
- **suggested manual fix:** add an asset-class gate so equity headlines don't enter the crypto feed as `<TICKER>/USDT`; add a spam/promo filter for t.me withdrawal-shill patterns; route unmapped equity-class events out of the crypto trading-day JSONL.
- **priority:** medium
- **first observed:** recurring; reconfirmed 2026-06-06 11:40 EEST.

### TODO-expired-signal-hygiene
- **issue:** `active-signals` surfaces lapsed rows — BTC/USDT B scalp short shows `status=triggered` with `expires_at` 08:38, still listed ~3h past expiry, which can be misread as a live position.
- **evidence:** `active-signals --asset-class crypto` row `sig_69b9caa528f7d1a3` BTC/USDT scalp short, status triggered, expires 2026-06-06T08:38:18 (run time 11:40).
- **suggested manual fix:** confirm/extend the sweep that transitions past-`expires_at` rows (including `triggered`) to a terminal status so selection logic and the active-signals view don't surface lapsed signals.
- **priority:** low
- **first observed:** 2026-06-06 11:40 EEST.
