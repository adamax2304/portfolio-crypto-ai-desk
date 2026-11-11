# Opus Enriched Review — post-close final daily review (Saturday → crypto-only) — Auto Cycle 23:24 EEST

- **Generated:** 2026-06-06 23:24 EEST (auto-enriched-review, scheduled task `opus-enriched-review-postclose`, **post-close final daily review** slot 23:15, executing `opus-enriched-review-4h/SKILL.md`).
- **⚠ It is SATURDAY — US & EU cash equities were CLOSED all day.** There is no US cash "close" to wrap today; this post-close slot pivots to: (a) **the daily/weekly crypto wrap** (crypto is the only market that priced today), (b) **end-of-day risk & exposure hygiene into the weekend**, and (c) **the overnight-into-Asia / Sunday setup.** All 50 active stock signals = planning/watchlist context only.
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-06_2145.md` (late-session risk slot, 21:45 EEST, ~1.6h ago — see §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). **Fresh prints this run: BTC ~$60,652 (-1.8% 24h; intraday low ~$59,227 overnight — weakest since Oct 2024, lost the $60K handle), ETH ~$1,558 (-3.3% 24h, pinned near its 13-month low).** Lower than the $61,928 / $1,666 June-5 prints cited at 21:45 → **the "no reversal" thesis is confirmed; the tape closed the week slightly weaker, not stronger.** WebFetch on cryptoticker returned HTTP 200 (served a cached June-3 piece — figures above are the fresher June-6 WebSearch aggregation of CoinDesk/cryptoticker live data).
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; price/structure = local OHLCV/ATR/EMA report fields + cited external prints.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

- **Daily wrap: crypto closed the week deep in risk-off, no reversal.** The freshly-regenerated intraday report (21:13) and carry-forward swing report (14:46) both independently print *"bearish trend (risk-off); short bias or no trade; avoid weak altcoin longs."* Altcoin breadth above EMA20 is **10.42%** (intraday) / 16.67% (swing) — thin participation. **Neither report produced a single A-tier or B-tier setup.** BTC printed a fresh overnight low (~$59,227), lost $60K, and sits at its weakest since Oct 2024; ETH is glued to ~$1,558.
- **What drove the day (external, verified §13):** Friday's May jobs report (172k, unemployment 4.3%) set off a cross-asset selloff (Nasdaq −5%) that bled into crypto; **US–Iran tensions** (OFAC sanctioned Iran's largest exchange Nobitex + Wallex/Bitpin/Ramzinex) plus **Hezbollah's rejection of Israel's ceasefire offer**; **record 10 straight days of spot-BTC-ETF net outflows (~$2.97B)**; and the "AI capital drain" narrative. Crypto-specific: the Zcash Orchard counterfeiting bug **and** a separate operational scare (no new ZEC blocks for ~4h post-upgrade).
- **What worked / what failed today (internal):** Realized **intraday SHORTS were the winners** — NEAR & ADA both `tp2_hit` (now expired). Scalp bucket remains the week's best (5W/1L, PF 12.0, +11R). **What failed:** the **ZEC/USDT swing LONG** is a hard contradiction — entry $561.89–$567.42, **invalidation $555.12**, ZEC trades ~$356 (≈37% below invalidation) after the counterfeiting crash; `tp2_hit` is a stale pre-crash artifact. Week-to-date the **intraday mode is the worst bucket** (PF 0.14, 1W/7L, −6R) and **shorts net −5R** (PF 0.58) vs **longs +14R** (PF 2.75) — feedback-only, small sample.
- **End-of-day risk/exposure: STAND-DOWN / manage-only.** No fresh actionable in any mode. Of 5 active crypto signals, NEAR/ADA/C are expired/realized; **ZEC long = AVOID (dead)**; **XLM long = manage runner, NO-ADD.** Carry minimal/zero fresh weekend exposure.
- **Overnight-into-Asia / Sunday setup:** thin weekend book — crypto is the only live expression of any weekend headline. **Key level: BTC $59.2K overnight low / $60K handle** — losing $59,227 opens the next leg; ETH support shelf ~$1,540. **No-chase both directions.** A weekend Iran/Hormuz or Hezbollah escalation is the main thing that would gap risk assets at Monday's US open. Catalyst layer is **context-only (67.1% unmapped).**

---

## 2. Data Used

**Internal — crypto reports (mtime / freshness):**
- `data/reports/intraday/2026-06-06_18-13_intraday_report.md` — generated **21:13 EEST, ~2.2h FRESH**. Regime bearish risk-off; funnel 88 fused → 48 deep → 20 full-agent; breadth EMA20 **10.42%**; **No A-tier, No B-tier.**
- `data/reports/swing/2026-06-06_14-46_swing_report.md` — generated 17:46 EEST, **~5.6h CARRY-FORWARD** (4–12h band). Breadth EMA20 **16.67%**, *"short bias or no trade."* No A-tier, no B-tier.
- `data/reports/scalp/2026-06-06_02-38_scalp_report.md` (gen 05:38 EEST) — **~17.8h STALE** (>14h → excluded from execution use; regime was "high-volatility danger").
- Stocks reports (intraday 06-05 23:17 ~24h, swing 06-05 22:07 ~25h, invest 06-05 17:56 ~29.5h) — **weekend, closed → context only.**

**Catalyst / narrative:** `data/catalysts/2026-06-06/` — `catalyst_events.jsonl` (**773 rows**), `narrative_baskets.jsonl` (**3 baskets**), latest cycle `catalyst_cycle_18-13.md`. Mapped **254 / 773 (32.9%)**, unmapped **519 / 773 (67.1%)** → **weak (see §5).**

**LLM packets:** `data/processed/llm_analysis_packet.md` (crypto), `data/processed/llm_stocks_packet.md` (stocks, closed-market context).

**CLI / DB (read-only, this run):**
- `active-signals` crypto = **5**: NEAR/ADA intraday short (`tp2_hit`, past-expiry 13:01/11:58), C scalp long (`tp1_hit`, expired 06-04), ZEC swing long (`tp2_hit`, in-window to 06-07T22:56 — contradicted), XLM swing long (`tp1_hit`, in-window to 06-07T22:36 — manage-only). Stocks = **50** (closed → context).
- `signal-stats` crypto week — headline A/B **sample=69, triggered=52, 12W/20L, winrate 23%, PF 1.45, avgR 0.17, totalR +9.0**; by-mode intraday **−6R (PF 0.14, 1W/7L)**, scalp **+11R (PF 12.0, 5W/1L)**, swing **+4R (PF 1.33)**; by-direction longs **+14R (PF 2.75)** vs shorts **−5R (PF 0.58)**. Stocks A/B sample=215, triggered=157, PF 1.26, totalR +15, winrate 28.7% (context).
- `detect_untracked_legacy_alerts --since 2026-06-06` → **None (0)** — clean, headline stats uncontaminated.

**External (this run — cited §13):** BTC ~$60,652 / ETH ~$1,558 (June-6 WebSearch aggregation); BTC overnight low ~$59,227, "lost $60K / weakest since Oct 2024"; US-Iran tensions + Nobitex/Wallex/Bitpin/Ramzinex OFAC sanctions; record 10-day ETF outflow streak ~$2.97B; Hezbollah ceasefire rejection; Zcash Orchard bug + ~4h no-blocks operational scare. Yahoo (06-05), Crypto Times (06-04), UseTheBitcoin, CoinDesk (06-01).

**Unavailable / blind:** live tick beyond cited June-5/6 prints; TradingView/Chrome chart verification (not loaded); liquidation heatmaps / order-book / CVD; **fresh scalp execution levels (~18h stale)** — re-pull live before any entry.

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-06_default_schedule/`.
- `scheduler.log` mtime **~23:15 EEST** (fresh, < 1h); latest cycle summary `cycle_03_19-47_summary.md` mtime **~21:14 EEST (~2.2h)**. **Both < 3h → NO DEFER.**
- **No new full cycle has run since the 21:45 review** — the intraday report is still the 21:13 (`cycle_03_19-47`) generation (now ~2.2h, still FRESH). Internal data this run is therefore identical to what the 21:45 review consumed; **the delta this run is external (lower prices, fresh overnight low, ETF/sanctions detail).**
- Freshness labels: intraday **FRESH** (~2.2h); swing **CARRY-FORWARD** (~5.6h, direction context); scalp **STALE** (~17.8h → excluded from execution).

---

## 4. What Changed vs Previous Review (late-session risk 21:45 → post-close 23:24)

- **Prices lower, not higher — descent confirmed.** BTC ~$61,928 (21:45 cited, June-5) → **~$60,652** (June-6), with a fresh **overnight low ~$59,227** and loss of the $60K handle (weakest since Oct 2024). ETH ~$1,666 → **~$1,558**. The 21:45 "no weekend reversal" read is **confirmed and marginally worse.**
- **New macro detail surfaced (external):** record **10 consecutive days of spot-BTC-ETF outflows (~$2.97B)**; **US sanctioned Iran's Nobitex** (+Wallex/Bitpin/Ramzinex); **Hezbollah rejected Israel's ceasefire** — all reinforcing the risk-off + weekend-gap thesis carried from 16:24/18:39/21:45. Zcash adds a second operational scare (~4h no new blocks) on top of the counterfeiting bug.
- **Internal state unchanged:** same **5 active signals** (NEAR/ADA/C expired-or-realized; ZEC contradicted; XLM manage-only); same signal-stats (n=69, PF 1.45, +9R; longs PF 2.75 vs shorts PF 0.58; intraday −6R); **untracked legacy alerts still 0**; catalyst **773 events / 67.1% unmapped** (identical to 21:45); baskets unchanged (ai_narrative, binance_ecosystem_teaser, momentum_breakout).
- **ZEC verdict unchanged:** still AVOID/dead — long entered 55–60% above current price; the only nuance (turnstile accounting → no confirmed exploit) does not revive it.
- **No new report cycle** since 21:13; scalp still stale (TODO carried, §14).

---

## 5. Catalyst Coverage

- Total `catalyst_events` today: **773**
- Mapped (non-null symbol): **254 (32.9%)**
- Unmapped (null symbol): **519 (67.1%)**
- `narrative_baskets`: **3** (binance_ecosystem_teaser → BNB/ASTER; ai_narrative → NEAR/RENDER/TAO/FET +WLD; momentum_breakout → HEI/PORTAL, `avoid_chase`)
- **⚠ catalyst mapping weak this run (67.1% unmapped > 50%) — use catalyst layer as CONTEXT, not final decision.**
- Integrity note (recurring): many "mapped" rows are **equity tickers mis-suffixed as `/USDT`** (UNH/USDT, NVDA/USDT, LLY/USDT, MSFT/USDT, AMD/USDT, QQQ/USDT) — the resolver is tagging equity-news catalysts as crypto pairs. See §14 `TODO-catalyst-stock-usdt-mislabel`.
- Top 3 unmapped headlines (by importance):
  1. (~0.75) *"South Korea is the ultimate backdoor tech play — but stock investors now face a looming…"*
  2. (~0.68) *"Senate Calendar Crunch Forces Galaxy to Cut Clarity Act Odds by 15%"*
  3. (~0.68) *"Anthropic Is Helping the NSA Hack China. It Also Wants Everyone to Pause AI"*

---

## 6. Market Landscape

- **Crypto regime: bearish trend / risk-off, confirmed by two independent reports.** BTC downtrend, ETH downtrend, breadth above EMA20 **10.4% (intraday)** — even thinner than the swing read; any strength is large-cap relief inside a downtrend. BTC ATR percentile 92 (elevated vol).
- **Macro overhang (how the week closed):** post-May-jobs cross-asset selloff (Nasdaq −5%), **record 10-day spot-ETF outflows (~$2.97B)**, "AI's $800B spending boom becoming Bitcoin's Fed problem," and US government BTC-holdings headlines. **Geopolitics escalating into the weekend:** US sanctions on Iran's Nobitex, Hezbollah ceasefire rejection, Iran/Hormuz warning-shots — **weekend escalation = Monday gap risk.**
- **Crypto-specific credibility shock:** Zcash Orchard counterfeiting bug (ZEC −50% peak-to-trough) **+** a ~4h no-new-blocks operational scare; contagion to **XMR −10%** (same researcher adding Monero to audit queue). Privacy-coin basket carries a fresh structural discount.
- **Narrative pockets (context only):** AI-rotation basket bleeding on the Arthur Hayes WLD dump (−20%); BNB/ASTER sell-the-news; **momentum cluster HEI +75.7% / PORTAL +26.9% with no news → `avoid_chase`, overextended.**
- **Stocks (closed, Monday planning):** active B-tier signals uniformly **short** (QQQ, AMAT, SPY, XLK, MSFT, MEDP) — consistent with risk-off macro; no live action this slot.

---

## 7. Candidate Deep Dives (≤ 5)

### 7.1 ZEC/USDT — swing LONG — **CONTRADICTION / HEADLINE RISK → AVOID (dead)**
- **Signal:** B, swing long, score 65.2, `tp2_hit`, entry $561.89–$567.42, invalidation $555.12, expires 2026-06-07T22:56 (nominally in-window).
- **Internal records:** 17 catalyst events + multiple news_items in 24h for ZEC — all bearish (counterfeiting bug, $13M Binance withdrawal, XMR contagion). Recent and consistent → external re-verify done (major contradiction with a LONG).
- **External (verified §G):** Orchard counterfeiting vulnerability (AI-assisted audit, disclosed Jun 5); price peak $624 (Jun 4) → low ~$264.80 (Jun 5) → rebound ~$356; **plus** a fresh operational scare — explorers showed **no new blocks for >4h** after the Orchard upgrade.
- **LEGAL/HEADLINE RISK:** structural credibility shock — developers' own caveat: *"no cryptographic way to prove the bug was never abused."*
- **Price-reaction / chase check:** price has fully reacted, ~37% **below** invalidation ($356 vs $555). `tp2_hit` is a stale pre-crash artifact. **No actionable level — this is a defunct signal, not a setup.**
- **Verdict: AVOID. Do not hold, do not initiate, do not dip-buy the bug.**

### 7.2 XLM/USDT — swing LONG — **MANAGE-ONLY / NO-ADD**
- **Signal:** B, swing long, score 65.4, `tp1_hit`, entry $0.2544–$0.2587, invalidation $0.2490, expires 2026-06-07T22:36 (in-window).
- **Internal records:** **0 news_items in 24h**, no catalyst event for XLM this run → no fresh thesis, no fresh contradiction. (CoinDesk noted XLM strength back on Jun 1, now stale.)
- **Price-reaction / chase check:** counter-trend long (regime "avoid weak altcoin longs") that already took TP1. Breadth 10–17%, no fresh catalyst → adding here fights the tape. Chart MCP unavailable — local fields only, no fabricated read.
- **Verdict: MANAGE the runner to invalidation/TP per the original plan; NO new entry, NO add.**

### 7.3 NEAR/USDT — intraday SHORT — **REALIZED / EXPIRED (context)**
- **Signal:** B, intraday short, score 66.7, `tp2_hit`, expired 2026-06-06T13:01. Realized winner — a "what worked today" example.
- **News (internal):** Arthur Hayes "called $ZEC/$NEAR/$WLD… sold near the top" (Lookonchain); NEAR sits in the **ai_narrative basket** now bleeding on the Hayes exit.
- **Verdict: No fresh entry. Short thesis realized; basket crowded/unwinding — watch-only.**

### 7.4 ADA/USDT — intraday SHORT — **REALIZED / EXPIRED (context)**
- **Signal:** B, intraday short, score 66.4, `tp2_hit`, expired 2026-06-06T11:58. Realized winner.
- **News (internal):** ADA at 4-year lows under $0.20, "Is Cardano Dead after Hoskinson's confession." Bearish thesis confirmed, now played out.
- **Verdict: No fresh entry — chasing a new short into the capitulation/support shelf is late. Watch for relief-bounce mean-reversion, not continuation.**

### 7.5 Market-level no-trade — **HEI / PORTAL momentum cluster → AVOID CHASE**
- `momentum_breakout` basket: **HEI/USDT +75.7%** (flagged overextended), **PORTAL/USDT +26.9%** (vol 9.37x), **no confirmed news catalyst.** Playbook = `avoid_chase`.
- **Verdict: AVOID. Pure momentum with no driver into a risk-off, thin weekend tape is the textbook bull-trap.**

---

## 8. Best Candidates Ranked

**No clean candidates.** No A-tier anywhere; no fresh B-tier printed by swing or the fresh intraday report; every active crypto signal is expired/realized (NEAR, ADA, C) or contradicted/manage-only (ZEC, XLM). This is a **stand-down / manage-only** end-of-day.

---

## 9. Avoid / No Trade

- **ZEC/USDT long** — defunct, ~37% below invalidation, permanent structural credibility risk. AVOID.
- **HEI/USDT, PORTAL/USDT** — overextended momentum, no news, `avoid_chase`. AVOID.
- **New altcoin longs generally** — regime "avoid weak altcoin longs," breadth 10–17%. AVOID.
- **Chasing ADA/NEAR shorts** — thesis realized, extended into support / crowded unwind. NO new entry.
- **Stocks (Monday planning, NOT re-verified this closed slot):** carry-forward legal/headline avoids **SMCI** (export-control indictment) and **UNH** (DOJ probe) — flagged, full legal re-verification deferred to a weekday slot (§14).

---

## 10. Main Risks

- **Weekend/Sunday gap risk into Monday's US open** — US-Iran (Nobitex sanctions), Hezbollah ceasefire rejection, Hormuz headlines; a weekend escalation gaps risk assets down. Crypto is the only live hedge/expression.
- **BTC technical:** loss of the **$59,227 overnight low / $60K handle** opens the next leg lower; ETH shelf ~$1,540.
- **Sustained ETF outflows** — 10-day record streak (~$2.97B) is a persistent structural bid-removal, not a one-off.
- **Thin weekend liquidity** — both directions slippage-prone; absence of a fresh setup is itself the signal to wait.
- **Privacy-coin contagion** — ZEC→XMR audit-queue spread could widen.
- **Data blind spots** — scalp ~18h stale (no live scalp levels); no chart/liquidation/order-book tooling; weekend price relies on June-5/6 prints.
- **Catalyst layer unreliable** — 67.1% unmapped + stock-as-USDT mislabeling; context only.
- **Source-ingest** — result recorded in §13/§14 if the ingest CLI errors.

---

## 11. Action Plan — next 4 hours (overnight into the 04:30 Asia slot)

1. **Stand down on new crypto entries.** No A/B setup, risk-off, thin weekend book — patience is the edge.
2. **ZEC long:** treat as closed/dead; do NOT dip-buy.
3. **XLM long:** manage existing runner to plan only; no add.
4. **Carry minimal/zero fresh weekend crypto exposure;** if holding, size down and honor stops.
5. **Watch BTC $59.2K–$60K and ETH ~$1,540** — a clean loss overnight is the trigger that changes the Asia-session read.
6. **Monitor Iran/Nobitex/Hezbollah/Hormuz headlines** — the main weekend-gap driver into Monday.
7. **Re-pull live scalp/intraday levels before any entry** (scalp ~18h stale).
8. **Monday stocks prep (no action now):** short-skewed book (QQQ/AMAT/SPY/XLK/MSFT); keep SMCI & UNH on the legal-avoid list pending a weekday legal re-check.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** NO TRADE. Report ~18h stale (was "high-volatility danger"); re-pull live before acting. Stand down.
- **Crypto intraday:** NO TRADE. Fresh report (21:13) printed **No A-tier / No B-tier**, "short bias or no trade." Do not chase ADA/NEAR shorts or HEI/PORTAL momentum.
- **Crypto swing:** MANAGE-ONLY. ZEC long **AVOID/dead**; XLM long **no-add**; no new swing entry (breadth 10–17%, "avoid weak altcoin longs").
- **Stocks (all modes):** NO ACTION — market closed (Saturday). Monday planning skews **short**; legal-avoids SMCI/UNH carried forward (un-verified this slot).

---

## 13. Sources

External (this run):
- [Yahoo Finance — Bitcoin and ethereum prices today, Friday, June 5, 2026: Prices continue their descent](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-friday-june-5-2026-prices-continue-their-descent---5-reasons-why-113631165.html) — 2026-06-05 (BTC opened $63,812 → $62,046 intraday; descent continues, Hezbollah ceasefire rejection)
- [Crypto Times — Today in Crypto: Bitcoin Dips Toward $62K on Continued ETF Outflows, US Sanctions Iran's Nobitex](https://www.cryptotimes.io/2026/06/04/today-in-crypto-bitcoin-dips-toward-62k-on-continued-etf-outflows-us-sanctions-irans-nobitex-and-more/) — 2026-06-04 (OFAC sanctions Nobitex/Wallex/Bitpin/Ramzinex; ETF outflows)
- [UseTheBitcoin — Crypto Market US-Iran Tensions Trigger ETF Outflows in June](https://usethebitcoin.com/news/crypto-market-us-iran-tensions/) — date unavailable (US-Iran tensions; record 10-day ETF outflow streak ~$2.97B)
- [CoinDesk — BTC, ETH prices drop even as futures show growing taste for risk; XLM, HYPE gain](https://www.coindesk.com/markets/2026/06/01/bitcoin-ether-start-june-in-the-red-while-futures-show-taste-for-risk-xlm-hype-gain) — 2026-06-01 (June opened red)
- WebSearch aggregation (CoinDesk/cryptoticker live data), 2026-06-06: **BTC ~$60,652 (−1.8%), ETH ~$1,558 (−3.3%); BTC overnight low ~$59,227, weakest since Oct 2024.** WebFetch on cryptoticker.io returned HTTP 200 (served cached 2026-06-03 content — used only to confirm the source is reachable, not for the June-6 figures).

Internal news_items (DB `news_items`, not external-web; source + date, no URL fabricated):
- ZEC counterfeiting disclosure / −38% — CryptoBriefing/Decrypt, 2026-06-06
- Researcher adds Monero to audit queue, XMR −10% — BeInCrypto, 2026-06-06
- Arthur Hayes called $ZEC/$NEAR/$WLD, sold near top — t.me/lookonchain, 2026-06-06
- WLD −20% Hayes dump (ai_narrative basket) — 2026-06-06
- US adds 172,000 jobs in May, unemployment 4.3% — CryptoBriefing, 2026-06-06

_Source-discipline: every external claim above has source + title + date (or "date unavailable") + URL; no uncited stats; no fabricated chart observations (chart MCP unavailable, stated); internal-only claims labeled as such with date; no test/fixture sources. External web research was AVAILABLE this run._

---

## 14. Fix Requests / TODO

### TODO-scalp-report-staleness (carried)
- **issue:** Scalp report has not regenerated since 05:38 (~18h stale) while intraday + swing regenerated in `cycle_03_19-47`; the generator-staleness regression has narrowed to scalp-only but persists.
- **evidence:** `data/reports/scalp/2026-06-06_02-38_scalp_report.md` gen 05:38 EEST vs intraday regenerated 21:13 EEST same cycle window.
- **suggested manual fix:** audit the scalp generator's schedule trigger / gating in the default scheduler; confirm scalp is wired into each cycle like intraday.
- **priority:** medium
- **first observed:** 2026-06-06 18:39 EEST (narrowed/carried; still open at 23:24)

### TODO-catalyst-stock-usdt-mislabel (carried)
- **issue:** Equity-news catalysts are mapped to crypto `/USDT` pairs (UNH/USDT, NVDA/USDT, LLY/USDT, MSFT/USDT, AMD/USDT, QQQ/USDT), inflating apparent crypto catalyst mapping and polluting crypto symbol resolution.
- **evidence:** `data/catalysts/2026-06-06/catalyst_events.jsonl` — NYSE/Nasdaq tickers carrying `/USDT` suffix, asset_class should be stocks.
- **suggested manual fix:** gate `/USDT` suffixing on asset_class=crypto and/or a crypto-symbol allowlist; route equity tickers to the stocks asset class.
- **priority:** medium
- **first observed:** 2026-06-06 21:45 EEST (carried)

### TODO-catalyst-mapping-weak (recurring)
- **issue:** Catalyst mapping has been <50% for multiple consecutive runs (66% @18:39 → 67.1% @21:45 → 67.1% @23:24).
- **evidence:** 519/773 unmapped this run (identical to 21:45).
- **suggested manual fix:** improve the catalyst-layer symbol resolver (entity extraction + ticker dictionary); overlaps TODO-catalyst-stock-usdt-mislabel.
- **priority:** medium
- **first observed:** carried forward (recurring)

### TODO-intraday-mode-bucket (feedback)
- **issue:** Intraday mode is the worst-performing bucket (PF 0.14, 1W/7L, net −6R, week); long-vs-short divergence persists (longs PF 2.75 / +14R vs shorts PF 0.58 / −5R).
- **evidence:** `signal-stats --asset-class crypto` by-mode + by-direction tables, this run.
- **suggested manual fix:** review intraday-mode scoring/thresholds; small sample, monitor before acting.
- **priority:** low
- **first observed:** 2026-06-06 21:45 EEST (feedback-only, small sample)
