# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:39 EEST

- **Generated:** 2026-06-07 04:39 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`, **crypto overnight / Asia review** slot 04:30, executing `opus-enriched-review-4h/SKILL.md`).
- **⚠ It is SUNDAY — US & EU cash equities are CLOSED.** Stock signals = planning/watchlist context only; **crypto is the only live, actionable class this slot.**
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-06_2324.md` (post-close final daily, 23:24 EEST Saturday, ~5.1h ago — see §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). **Fresh prints this run: BTC ~$60,880 (−2.3% 24h, June 6), ETH ~$1,559 (June 7 open, prev close $1,618 → −3.6%).** WebFetch on interactivecrypto returned HTTP 200 (verified). BeInCrypto returned HTTP 403 (used WebSearch summary + reachable mirrors instead).
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; structure = local OHLCV/ATR/EMA report fields + cited external prints.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

- **Overnight crypto stayed risk-off; no reversal into Asia.** A **fresh full cycle ran** at the top of the hour — scalp (03:19) and intraday (04:00) both regenerated and both independently print *"bearish trend (risk-off); short bias or no trade; avoid weak altcoin longs."* Altcoin breadth above EMA20 **15.0%** (thin). **Neither report produced a single A-tier or B-tier setup.** BTC ATR percentile 80–81 (elevated vol).
- **Prices grind lower, confirmed external (§13):** BTC ~$60,880 (June 6, −2.3%); **ETH ~$1,559 at the June-7 open vs $1,618 prev close (−3.6%)** — fresh leg down, now testing the report's $1,566 print from below. Drivers unchanged: record **10–11-day spot-ETF outflow streak (~$2.8–3.5B)**, a Strategy (MSTR) BTC sale, the post-May-jobs "higher-for-longer" repricing, and lingering US–Iran/Hezbollah geopolitics.
- **Active book = manage/stand-down.** 5 active crypto signals: **NEAR & ADA intraday SHORTS realized (`tp2_hit`, expired)**; **C scalp long expired**; **ZEC swing LONG = AVOID/dead** (price ~$362 vs invalidation $555, ~35% below — defunct post-counterfeiting-crash artifact); **XLM swing LONG = manage-only/no-add.** No fresh actionable in any mode.
- **What's working (feedback-only, n=69):** scalp bucket remains best (PF 12.0, +11R), **intraday remains the worst (PF 0.14, 1W/7L, −6R)**, longs +14R (PF 2.75) vs shorts −5R (PF 0.58). Untracked legacy alerts **0** (clean).
- **Positive system delta:** the **scalp-report-staleness regression appears RESOLVED this cycle** — scalp regenerated 03:19 alongside intraday, no longer ~18h stale (see §4 / §14).
- **Asia-session setup:** thin Sunday book, crypto is the only live expression of any weekend headline. **Key levels: BTC $60K handle / ~$59.2K prior overnight low; ETH ~$1,540 shelf.** No-chase both directions. Catalyst layer is **context-only (68.7% unmapped).**

---

## 2. Data Used

**Internal — crypto reports (mtime / freshness):**
- `data/reports/scalp/2026-06-07_00-19_scalp_report.md` — gen **03:19 EEST, ~1.3h FRESH**. Regime bearish risk-off; breadth EMA20 15%; **No A-tier, No B-tier**; best watchlist LTC 61.4.
- `data/reports/intraday/2026-06-07_01-00_intraday_report.md` — gen **04:00 EEST, ~0.7h FRESH**. Same regime; breadth 15%; **No A-tier, No B-tier**; best watchlist LTC 59.5.
- `data/reports/swing/2026-06-06_14-46_swing_report.md` — gen 17:46 EEST, **~10.9h CARRY-FORWARD** (4–12h band; direction context only). No A/B; best watchlist NEAR 63.6.
- Stocks reports (intraday 06-05 ~29h, swing 06-05 ~31h, invest 06-05 ~35h) — **weekend, closed → context only.**

**Catalyst / narrative:** `data/catalysts/2026-06-07/` — `catalyst_events.jsonl` (**252 rows**), `narrative_baskets.jsonl` (**4 baskets**), latest cycle `catalyst_cycle_01-01.md`. Mapped **79 / 252 (31.3%)**, unmapped **173 / 252 (68.7%)** → **weak (§5).** Telegram-source events: 13.

**LLM packets:** `data/processed/llm_analysis_packet.md` (crypto, ~0.7h fresh); `data/processed/llm_stocks_packet.md` (~29h, closed-market context).

**CLI / DB (read-only, this run):**
- `active-signals` crypto = **5**: NEAR/ADA intraday short (`tp2_hit`, expired), C scalp long (expired), ZEC swing long (in-window to 06-07T22:56 — contradicted), XLM swing long (in-window to 06-07T22:36 — manage-only).
- `signal-stats` crypto week — headline A/B **n=69, triggered=52, 12W/20L, winrate 23.1%, PF 1.45, avgR 0.17, totalR +9.0**; by-mode intraday **−6R (PF 0.14, 1W/7L)**, scalp **+11R (PF 12.0, 5W/1L)**, swing **+4R (PF 1.33)**; by-direction longs **+14R (PF 2.75)** vs shorts **−5R (PF 0.58)**; exchange-confirmed bucket PF 2.11 (+10R) vs unconfirmed PF 0.57 (−3R).
- `detect_untracked_legacy_alerts --since 2026-06-07` → **None (0)** — clean.

**External (cited §13):** BTC ~$60,880 (June 6, −2.3%); ETH ~$1,559 (June 7 open, −3.6% vs prev close); ETF outflows ~$2.8–3.5B over 10–11 sessions; $1.76B 24h liquidations / $560M BTC; ZEC Orchard counterfeiting bug (found via Opus 4.8 audit, May 29; patched June 2; ZEC −38–50%; exploitation "appears unlikely" but unprovable).

**Unavailable / blind:** live tick beyond cited June-6/7 prints; TradingView/Chrome chart verification (not loaded); liquidation heatmaps / order-book / CVD; live social/KOL feeds.

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-06_default_schedule/`.
- `scheduler.log` mtime **~04:02 EEST (~0.6h)**; latest cycle summary `cycle_05_02-38_summary.md` mtime **~04:02 EEST (~0.6h)**. **Both < 3h → NO DEFER.**
- **A new full cycle ran since the 23:24 review** — scalp (03:19) AND intraday (04:00) both regenerated this cycle window. Internal data this run is genuinely fresher than the 23:24 post-close review consumed.
- Freshness labels: scalp **FRESH** (~1.3h), intraday **FRESH** (~0.7h), swing **CARRY-FORWARD** (~10.9h, direction context). Stocks **stale/closed → context only.**

---

## 4. What Changed vs Previous Review (post-close 23:24 Sat → Asia 04:39 Sun)

- **Scalp staleness RESOLVED.** The carried `TODO-scalp-report-staleness` (scalp ~18h stale at 23:24) is **cleared this run** — scalp regenerated 03:19 in the same cycle as intraday. Downgrading the TODO pending one more confirming cycle (§14).
- **Prices marginally lower / sideways-down.** ETH printed **~$1,559 at the June-7 open vs $1,618 prev close (−3.6%)**, a fresh down-tick; BTC ~$60,880 (June 6) — broadly the same $60–61K zone the 23:24 review cited (~$60,652 with a $59,227 overnight low). **Descent thesis intact; no reversal overnight.**
- **Internal state largely unchanged:** same **5 active signals** (NEAR/ADA/C expired-or-realized; ZEC contradicted; XLM manage-only); same signal-stats (n=69, PF 1.45, +9R; longs PF 2.75 vs shorts PF 0.58; intraday −6R); **untracked legacy alerts still 0**.
- **Catalyst volume reset for the new day:** 773 events (06-06) → **252 events (06-07, cycle_01-01)**; unmapped 67.1% → **68.7%** (still weak); baskets 3 → **4** (added `delisting_thin_liquidity` + `perps_dex_narrative`/HYPE; `ai_narrative` and `momentum_breakout` carried, momentum primary rotated HEI/PORTAL → **PARTI**).
- **ZEC verdict unchanged:** still AVOID/dead — long entered ~55% above current price; bug now patched (June 2) but the structural credibility discount stands.
- **Legal flags carried (stocks, closed):** SMCI (export-control indictment, SEC 8-K), UNH (DOJ probe) still topping the catalyst legal-risk list — context only this slot.

---

## 5. Catalyst Coverage

- Total `catalyst_events` today (06-07): **252**
- Mapped (non-null symbol): **79 (31.3%)**
- Unmapped (null symbol): **173 (68.7%)**
- `narrative_baskets`: **4**
  - `delisting_thin_liquidity` (`avoid_low_liquidity`, single_source, <6h) — primary —; e.g. "HTX to delist Trump-linked USD1…"
  - `perps_dex_narrative` (`wait_pullback`, single_source, <6h) — primary **HYPE/USDT**; related DYDX/GMX/ASTER
  - `ai_narrative` (`related_beta_rotation`, single_source, <24h) — primary NEAR/RENDER/TAO/FET; related WLD/ASTER
  - `momentum_breakout` (`wait_pullback`, single_source, <1h) — primary **PARTI/USDT** (+18.5%, vol 0.97x) — `avoid_chase`
- **⚠ catalyst mapping weak this run (68.7% unmapped > 50%) — use catalyst layer as CONTEXT, not final decision.**
- Integrity note (recurring): "mapped" rows still include **equity tickers mis-suffixed as `/USDT`** (SMCI/USDT, UNH/USDT, MSFT/USDT) — resolver tagging equity-news as crypto pairs. See §14 `TODO-catalyst-stock-usdt-mislabel`.
- Top 3 unmapped/low-map headlines (by importance):
  1. (~0.71) *"US Supreme Court backs FCC and SEC in key regulatory rulings that reshape enforcement landscape"* (CryptoBriefing)
  2. (~0.68) *"Why is the crypto market down today? ETF outflows, $1.3B liquidations, and more"* (AMBCrypto)
  3. (~0.68) *"South Korea is the ultimate backdoor tech play — but stock investors now face a looming threat"* (MarketWatch)

---

## 6. Market Landscape

- **Crypto regime: bearish trend / risk-off, confirmed by two fresh reports** (scalp 03:19 + intraday 04:00). BTC downtrend, ETH downtrend, breadth above EMA20 **15.0%** — thin; any strength is large-cap relief inside a downtrend. BTC ATR percentile 80–81 (elevated).
- **Macro overhang (external):** record **10–11-day spot-ETF outflow streak (~$2.8–3.5B)**, a Strategy (MSTR) BTC sale, post-May-jobs "higher-for-longer," and the "AI's $800B spending boom = Bitcoin's Fed problem" narrative. **$1.76B of 24h liquidations** (longs hit hardest) accompanied the slide toward $60K.
- **Where money is (intra-crypto, context):** lone green names are **PARTI +18.5%** and **PORTAL +16–20%** — RS leaders vs a weak tape, both flagged counter-trend / `avoid_chase`. Weakest: **OPN −40%**, **WLD −20%**. Funding mostly mildly negative (fresh shorts pressing) — squeeze risk on any BTC reclaim.
- **Crypto-specific:** **ZEC** carries a fresh structural credibility discount post Orchard counterfeiting bug (patched June 2; XMR contagion −10% on the same researcher adding Monero to the audit queue). Privacy basket de-rated.
- **Stocks (closed, Monday planning):** legal-risk avoids **SMCI** (export-control indictment) and **UNH** (DOJ probe) carried; no live action this slot.

---

## 7. Candidate Deep Dives (≤ 5)

### 7.1 ZEC/USDT — swing LONG — **CONTRADICTION / HEADLINE RISK → AVOID (dead)**
- **Signal:** B, swing long, score ~65, `tp2_hit`, entry $561.89–$567.42, invalidation $555.12, nominal expiry 2026-06-07T22:56.
- **Internal:** fresh ZEC catalyst/news items (counterfeiting bug, XMR contagion) — recent and consistent → external re-verify done (major contradiction with a LONG).
- **External (verified §13/§G):** Orchard counterfeiting vulnerability found May 29 (Opus 4.8-assisted audit, Taylor Hornby), undetected since 2022, **patched June 2**; ZEC crashed 38–50% (post-disclosure $409–443, scalp report now prints **$361.91**). Shielded Labs: exploitation "appears unlikely" but **cannot be proven cryptographically.**
- **Price-reaction / chase check:** price has fully reacted, ~**35% below invalidation** ($362 vs $555). `tp2_hit` is a stale pre-crash artifact. **No actionable level — defunct signal, not a setup.**
- **Verdict: AVOID. Do not hold, do not initiate, do not dip-buy the bug.**

### 7.2 XLM/USDT — swing LONG — **MANAGE-ONLY / NO-ADD**
- **Signal:** B, swing long, score ~65, `tp1_hit`, in-window to 06-07T22:36.
- **Internal:** no fresh news_item / catalyst for XLM this run → no fresh thesis, no fresh contradiction.
- **Price-reaction / chase check:** counter-trend long (regime "avoid weak altcoin longs") that already took TP1; breadth 15%, no fresh catalyst → adding fights the tape. Chart MCP unavailable — local fields only.
- **Verdict: MANAGE the runner to plan; NO new entry, NO add.**

### 7.3 PARTI/USDT — momentum LONG (basket primary) — **AVOID CHASE / WATCH PULLBACK**
- **Context:** `momentum_breakout` basket primary, +18.5% 24h, RS vs BTC +19.3%, vol 0.97x, uptrend; scalp watchlist score 59.9, intraday 57.1 — **below active threshold.**
- **Internal:** **no fresh verified news catalyst** — pure momentum cluster (basket summary: "top gainers without confirmed news"). Playbook = `wait_pullback`.
- **Price-reaction / chase check:** already extended (RS leader counter-tape); conditional pullback zone 0.0567–0.0577 vs current 0.0582. **Entry now = chasing a beta-bounce in a bearish tape.** No derivatives confirmation (MEXC-fallback funding only).
- **Verdict: NO CHASE. Watch only for a confirmed pullback hold; reduce size if ever taken counter-tape.**

### 7.4 NEAR/USDT — intraday SHORT — **REALIZED / EXPIRED (context)**
- **Signal:** B intraday short `tp2_hit`, expired. Realized winner. Also `ai_narrative` basket member (bleeding on the prior Arthur Hayes WLD/NEAR/ZEC exit).
- **Verdict: No fresh entry. Short thesis realized; basket crowded/unwinding — watch-only. New short here is late vs support.**

### 7.5 ADA/USDT — intraday SHORT — **REALIZED / EXPIRED (context)**
- **Signal:** B intraday short `tp2_hit`, expired. Fresh catalyst (importance ~0.95) but bearish thesis (ADA ~$0.157, near multi-year lows) already played out.
- **Verdict: No fresh entry — chasing a new short into the capitulation shelf is late; watch for relief-bounce mean-reversion, not continuation.**

---

## 8. Best Candidates Ranked

**No clean candidates.** No A-tier anywhere; no fresh B-tier printed by scalp, intraday, or swing; every active crypto signal is expired/realized (NEAR, ADA, C) or contradicted/manage-only (ZEC, XLM). This is a **stand-down / manage-only** Asia slot.

---

## 9. Avoid / No Trade

- **ZEC/USDT long** — defunct, ~35% below invalidation, permanent structural credibility risk. AVOID.
- **PARTI/USDT (+ PORTAL)** — overextended RS-leader momentum, no confirmed news, `avoid_chase`. NO CHASE.
- **New altcoin longs generally** — regime "avoid weak altcoin longs," breadth 15%. AVOID.
- **Chasing ADA/NEAR shorts** — thesis realized, extended into support / crowded unwind. NO new entry.
- **Stocks (Monday planning, NOT re-verified this closed slot):** carry-forward legal/headline avoids **SMCI** (export-control indictment) and **UNH** (DOJ probe); full legal re-verification deferred to a weekday slot.

---

## 10. Main Risks

- **Sunday/weekend gap risk into Monday's US open** — US–Iran / Hezbollah headlines plus the ETF-outflow + Strategy-sale overhang; a weekend escalation gaps risk assets down. Crypto is the only live expression.
- **BTC technical:** loss of the **$60K handle / ~$59.2K prior overnight low** opens the next leg; ETH shelf ~$1,540 (already pressing it at $1,559).
- **Sustained ETF outflows** — 10–11-day record streak (~$2.8–3.5B) is structural bid-removal, not a one-off.
- **Thin weekend liquidity** — both directions slippage-prone; absence of a fresh setup is itself the signal to wait. Negative funding across many names = squeeze risk on any BTC reclaim.
- **Privacy-coin contagion** — ZEC→XMR audit-queue spread could widen.
- **Data blind spots** — no chart/liquidation/order-book tooling; live social/KOL manual; weekend price relies on June-6/7 prints.
- **Catalyst layer unreliable** — 68.7% unmapped + stock-as-USDT mislabeling; context only.
- **Source-ingest** — result recorded in §13/§14 if the ingest CLI errors.

---

## 11. Action Plan — next 4 hours (Asia session into the 11:30 Europe slot)

1. **Stand down on new crypto entries.** No A/B setup, risk-off, thin Sunday book — patience is the edge.
2. **ZEC long:** treat as closed/dead; do NOT dip-buy.
3. **XLM long:** manage existing runner to plan only; no add.
4. **PARTI/PORTAL:** watch-only for a confirmed pullback; do not chase the green candle.
5. **Watch BTC $60K / ~$59.2K and ETH ~$1,540** — a clean loss is the trigger that changes the Europe-session read; a reclaim above local resistance is the squeeze setup to respect (negative funding).
6. **Monitor US–Iran / Hezbollah / Hormuz + ETF-flow headlines** — the main weekend-gap drivers into Monday.
7. **Monday stocks prep (no action now):** keep SMCI & UNH on the legal-avoid list pending a weekday legal re-check.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** NO TRADE. Fresh report (03:19) printed **No A-tier / No B-tier**, "short bias or no trade." Best watchlist LTC 61.4 — below threshold. Stand down.
- **Crypto intraday:** NO TRADE. Fresh report (04:00) **No A-tier / No B-tier**. Do not chase ADA/NEAR shorts or PARTI/PORTAL momentum. (Bucket is the week's worst, PF 0.14 — extra caution.)
- **Crypto swing:** MANAGE-ONLY. ZEC long **AVOID/dead**; XLM long **no-add**; no new swing entry (breadth 15%, "avoid weak altcoin longs").
- **Stocks (all modes):** NO ACTION — market closed (Sunday). Monday planning skews **short**; legal-avoids SMCI/UNH carried (un-verified this slot).

---

## 13. Sources

External (this run):
- [InteractiveCrypto — Bitcoin's $60,880 Test: ETF Outflows and Liquidations Drive a 2.3% Daily Drop](https://www.interactivecrypto.com/bitcoin-s-60-880-test-etf-outflows-and-liquidations-drive-a-2-3-daily-drop-jun-2026) — 2026-06-06 (**WebFetch HTTP 200 verified**; BTC $60,880.29, −2.31% 24h; ETF outflows ~$2.8–3.5B over 10–11 sessions; $560.72M BTC / $1.75B total 24h liquidations)
- [Yahoo Finance — Bitcoin and ethereum prices today, Friday, June 5, 2026: Prices continue their descent](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-friday-june-5-2026-prices-continue-their-descent---5-reasons-why-113631165.html) — 2026-06-05 (BTC opened $63,812 → $62,046; descent continues; Hezbollah ceasefire rejection)
- WebSearch aggregation, 2026-06-07: **ETH ~$1,559.19 at the June-7 open vs $1,618.05 prev close (−3.6%)** (CoinDesk/Investing.com/Kraken live data)
- [CoinDesk — Bitcoin selloff continues as prices slide below $63,000 for the first time since February](https://www.coindesk.com/markets/2026/06/04/bitcoin-selloff-continues-as-prices-slide-below-usd63-000-for-the-first-time-since-february) — 2026-06-04
- [CoinDesk — Zcash plummets 38% as Shielded Labs reveals a major bug that went undetected for four years](https://www.coindesk.com/markets/2026/06/05/zcash-plummets-30-as-developer-reveals-a-major-bug-that-went-undetected-for-four-years) — 2026-06-05 (Orchard counterfeiting bug; patched June 2; exploitation "appears unlikely" but unprovable)
- [The Block — Security researcher finds Zcash vulnerability allowing 'unlimited' counterfeit minting; ZEC drops 31%](https://www.theblock.co/post/403698/zcash-vulnerability-zec-drops) — 2026-06-05
- [Investing.com — Bitcoin Falls as Record ETF Outflows and Strategy Sale Hit Sentiment](https://www.investing.com/analysis/bitcoin-falls-as-record-etf-outflows-and-strategy-sale-hit-sentiment-200681446) — 2026-06-06 (record ETF outflows + Strategy/MSTR BTC sale)
- [BeInCrypto — An Opus 4.8 Audit Uncovered Zcash's Bug — ZEC Plunged](https://beincrypto.com/zcash-zec-orchard-counterfeiting-bug/) — 2026-06-05 (**WebFetch HTTP 403** — could not load; used WebSearch summary + CoinDesk/The Block mirrors for the same facts)

Internal news_items (DB `news_items`, not external-web; source + date, no URL fabricated):
- ZEC counterfeiting / XMR contagion −10% — Decrypt/BeInCrypto, 2026-06-06/07
- Bitcoin dips below $61,000, $172M long liquidations — CryptoBriefing, 2026-06-07
- As institutions dump Solana, $60 becomes SOL's new battleground — AMBCrypto, 2026-06-07
- Hyperliquid UK warning / perps-DEX narrative — CryptoSlate, 2026-06-07
- SMCI export-control indictment 8-K / UNH DOJ probe (equity legal-risk, mis-suffixed /USDT) — SEC EDGAR / Yahoo / QuiverQuant, 2026-06-07

_Source-discipline: every external claim above has source + title + date (or "date unavailable") + URL; no uncited stats; no fabricated chart observations (chart MCP unavailable, stated); internal-only claims labeled with date; no test/fixture sources; BeInCrypto 403 declared rather than guessed. External web research was AVAILABLE this run._

---

## 14. Fix Requests / TODO

### TODO-scalp-report-staleness (RESOLVING — verify next cycle)
- **issue:** Prior runs (06-06 18:39→23:24) flagged scalp not regenerating (~18h stale) while intraday/swing did. **This run scalp regenerated 03:19 alongside intraday 04:00 — appears fixed.**
- **evidence:** `data/reports/scalp/2026-06-07_00-19_scalp_report.md` gen 03:19 EEST (~1.3h) in the same cycle window as intraday 04:00.
- **suggested manual fix:** none needed if it holds; confirm scalp regenerates again in the next 1–2 cycles before closing.
- **priority:** low (downgraded from medium — apparently resolved)
- **first observed:** 2026-06-06 18:39 EEST; **resolving 2026-06-07 04:39 EEST**

### TODO-catalyst-stock-usdt-mislabel (carried)
- **issue:** Equity-news catalysts mapped to crypto `/USDT` pairs (SMCI/USDT, UNH/USDT, MSFT/USDT), inflating apparent crypto catalyst mapping and polluting crypto symbol resolution.
- **evidence:** `data/catalysts/2026-06-07/catalyst_events.jsonl` — NYSE/Nasdaq tickers carrying `/USDT` suffix; asset_class should be stocks.
- **suggested manual fix:** gate `/USDT` suffixing on asset_class=crypto and/or a crypto-symbol allowlist; route equity tickers to the stocks asset class.
- **priority:** medium
- **first observed:** 2026-06-06 21:45 EEST (carried)

### TODO-catalyst-mapping-weak (recurring)
- **issue:** Catalyst mapping has been <50% for multiple consecutive runs (66% → 67.1% → 67.1% → **68.7%** now).
- **evidence:** 173/252 unmapped this run.
- **suggested manual fix:** improve the catalyst-layer symbol resolver (entity extraction + ticker dictionary); overlaps `TODO-catalyst-stock-usdt-mislabel`.
- **priority:** medium
- **first observed:** carried forward (recurring)

### TODO-intraday-mode-bucket (feedback)
- **issue:** Intraday mode remains the worst-performing bucket (PF 0.14, 1W/7L, net −6R, week); long-vs-short divergence persists (longs PF 2.75 / +14R vs shorts PF 0.58 / −5R); exchange-unconfirmed bucket also negative (PF 0.57 / −3R).
- **evidence:** `signal-stats --asset-class crypto` by-mode / by-direction / by-exchange_confirmation tables, this run.
- **suggested manual fix:** review intraday-mode scoring/thresholds and the exchange-confirmation gate; small sample, monitor before acting.
- **priority:** low
- **first observed:** 2026-06-06 21:45 EEST (feedback-only, small sample)
