# Opus Enriched Review — late-session risk review (Saturday → crypto-only) — Auto Cycle 21:45 EEST

- **Generated:** 2026-06-06 21:45 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`, **late-session risk review** slot 21:30, executing `opus-enriched-review-4h/SKILL.md`).
- **⚠ It is SATURDAY — US & EU cash equities are CLOSED.** No live US session to risk-check; this slot pivots to: (a) **crypto is the only live market pricing the weekend**, (b) **end-of-week exposure / risk hygiene**, and (c) **gap-staging for Monday's US open.** All 50 active stock signals = planning/watchlist context only.
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-06_1839.md` (US-open-reaction slot, 18:39 EEST, ~3.1h ago — see §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). Verified this run: **BTC ~$61,928, ETH ~$1,666** (Fortune/Yahoo June 5 prints — most recent reliable closes; weekend tick is sparse, no fresh reversal evidence). **Zcash Orchard counterfeiting bug** re-verified (Decrypt + news.bitcoin.com WebFetch HTTP 200): ZEC peak $624 (Jun 4) → intraday low **$264.80** (Jun 5) → rebound to **~$356** (back above 23.6% Fib). **Material nuance vs 18:39:** turnstile-accounting framing reported (BitMEX/crypto.news) suggests **no unauthorised value creation while the flaw was live**, but news.bitcoin.com confirms developers' own caveat — *"there is no cryptographic way to prove the bug was never abused."* Net: operational confidence up, structural residual doubt remains.
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; price/structure = local OHLCV/ATR/EMA report fields + cited external prints.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

- **Regime unchanged and bearish: broad risk-off, no participation.** Both the carry-forward swing report (14:46) and the **freshly regenerated intraday report (21:13)** independently print *"bearish trend (risk-off); short bias or no trade; avoid weak altcoin longs."* Altcoin breadth above EMA20 is **16.67%** (unchanged from 18:39). **Neither report produced a single A-tier or B-tier setup.**
- **No dead-cat improvement; prices flat-to-soft vs 18:39.** BTC ~$61,928 / ETH ~$1,666 (June 5 prints) — essentially the same level cited 3h ago; weekend liquidity is thin and there is **no evidence of a weekend reversal**. ETH remains pinned near its multi-month low. The edge is risk hygiene + patience, not initiating either side into low-liquidity weekend chop.
- **#1 risk item — the active ZEC/USDT swing LONG remains a hard contradiction → AVOID / effectively dead.** Signal entry zone **$561.89–$567.42, invalidation $555.12**; ZEC is ~$356, **far below invalidation**, after the Orchard counterfeiting crash. The `tp2_hit` status is a stale pre-crash artifact. The only update is a slightly *less* apocalyptic residual-risk read (turnstile accounting → no confirmed exploit), but that does **not** revive a long entered 55–60% above current price. Do not hold or initiate any ZEC long.
- **Every "active" crypto signal is expired or managed — no fresh actionable.** Of 5: **NEAR & ADA** (intraday short) and **C** (scalp long) are all **past `expires_at` and tp-hit** (realized/lapsed); only **ZEC and XLM swing** are still inside their expiry window — ZEC is contradicted (above), **XLM** is a counter-trend long, `tp1_hit` → manage / no-add only.
- **Net verdict: Crypto = short-biased but NO-CHASE; end-of-week STAND-DOWN / manage-only.** No clean long (fighting tape + breadth 16.7%), no clean fresh short (no setup printed, post-flush, thin weekend book). Carry minimal/zero weekend exposure. **For Monday's US open: stage for a risk-off gap** if Iran/Hormuz headlines persist over the weekend — size down, no counter-tape longs, no breakdown-chasing. **Stocks = no action (closed)**; Monday planning skews **short** (active B-tier signals QQQ 74, AMAT 70, SPY/XLK/MSFT all short) with **legal-risk avoids SMCI & UNH carried forward** (not re-verified this closed-market slot). Catalyst layer is **context-only (67% unmapped).**

---

## 2. Data Used

**Internal — crypto reports (mtime / freshness):**
- `data/reports/intraday/2026-06-06_18-13_intraday_report.md` — generated **21:13 EEST, ~0.5h FRESH** (regenerated this cycle). Regime bearish risk-off; funnel 88 fused → 48 deep → 20 full-agent; **No A-tier, No B-tier.**
- `data/reports/swing/2026-06-06_14-46_swing_report.md` — **~7.0h, CARRY-FORWARD** (4–12h band; last regen prior cycle). Breadth above EMA20/EMA50 **16.67%**, *"short bias or no trade."* No A-tier, no B-tier.
- `data/reports/scalp/2026-06-06_02-38_scalp_report.md` (gen 05:38 EEST) — **~16.1h, STALE** (>14h → excluded from execution-level use; was "high-volatility danger" regime).
- Stocks reports (intraday 06-05 20:17 ~25.5h, swing 06-05 19:07 ~26.6h, invest 06-05 14:55 ~30.8h) — **weekend, closed → context only.**

**Catalyst / narrative:** `data/catalysts/2026-06-06/` — `catalyst_events.jsonl` (**773 rows**), `narrative_baskets.jsonl` (**3 baskets**), latest cycle `catalyst_cycle_18-13.md`. Mapped **254 / 773 (32.9%)**, unmapped **519 / 773 (67.1%)** → **weak (see §5).**

**LLM packets:** `data/processed/llm_analysis_packet.md` (crypto), `data/processed/llm_stocks_packet.md` (stocks, closed-market context).

**CLI / DB (read-only, this run):**
- `active-signals` crypto = **5** (NEAR/ADA intraday short + C scalp = tp-hit & past-expiry; ZEC/XLM swing still in-window); stocks = **50** (closed → context; B-tier shorts QQQ 74, MEDP 77, AMAT 70, SPY/XLK/MSFT 65–67).
- `signal-stats` crypto week — headline A/B **sample=69, triggered=52, 12W/20L, winrate 23.1%, PF 1.45, avgR 0.173, totalR +9.0**; direction split: **longs n=36 PF 2.75 totalR +14; shorts n=33 PF 0.58 totalR −5.** Intraday mode net **−6R** (PF 0.14, 1W/7L) — weakest bucket.
- `detect_untracked_legacy_alerts --since 2026-06-06` → **None (0)** — clean, headline stats uncontaminated.
- DB `db/crypto_ai_desk.sqlite` (live, ~779 MB, collector writing). news_items total 5,468; **last 24h = 427 rows.**

**External (this run — cited §13):** BTC ~$61,928 / ETH ~$1,666 (Fortune 06-05, Yahoo 06-05); Zcash Orchard bug + price path (Decrypt, news.bitcoin.com WebFetch 200, crypto.news/Bitget). Internal news_items (not §13 web): ZEC −38% (CryptoBriefing 13:55), $13M ZEC Binance withdrawal (CryptoBriefing 15:04), XMR −10% audit-queue contagion (BeInCrypto 16:31); ADA 4-year lows / "Is Cardano Dead" (CoinDesk 03:30, BeInCrypto 05:25); WLD −20% Hayes dump (catalyst basket).

**Unavailable / blind:** live weekend tick beyond cited June-5 prints; TradingView/Chrome chart verification (not loaded); liquidation heatmaps / order-book / CVD; **fresh scalp execution levels (16h stale)** — re-pull live before any entry.

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-06_default_schedule/`.
- `scheduler.log` mtime **21:14:50 EEST** (~0.5h); latest cycle summary `cycle_03_19-47_summary.md` mtime ~1.9h. **Both < 3h → NO DEFER.**
- **Operational improvement vs 18:39:** a **new cycle ran (`cycle_03_19-47`)** and the **intraday report regenerated at 21:13 (now ~0.5h FRESH)** — at 18:39 intraday was 25.8h stale. **The intraday leg of the generator-staleness regression has cleared this run.** Swing is now carry-forward (~7h, last regen prior cycle, not this one). **Scalp still did NOT regenerate (~16h stale)** — the staleness regression is now **scalp-only.** See §14 `TODO-scalp-report-staleness`.
- Swing freshness label: **4–12h → carry-forward** (direction context, flagged). Scalp: **stale → excluded.** Intraday: **fresh.**

---

## 4. What Changed vs Previous Review (US-open-reaction 18:39 → late-session risk 21:45)

- **Intraday report un-staled — the headline operational change.** `cycle_03_19-47` regenerated the intraday report (25.8h stale → 0.5h fresh). It **independently confirms the swing read** (bearish risk-off, no A/B). The "intraday 25.8h stale" condition the 18:39 review flagged has cleared; only scalp remains stale.
- **Prices flat, no reversal.** BTC ~$61,924 (18:39) → ~$61,928; ETH ~$1,656 → ~$1,666. The modest bounce noted at 18:39 has **not extended**; weekend tape is going sideways near the lows. No new dead-cat leg, no breakdown either.
- **ZEC residual-risk read softened slightly, thesis unchanged.** New this run: turnstile-accounting framing (no unauthorised value creation while flaw live) + rebound to ~$356 from the $264.80 low. **But** the long signal ($561–567 entry) is still far underwater → still AVOID. Net direction of the ZEC verdict is identical to 18:39; only the *severity* of the tail-risk narrative eased.
- **Active crypto signals 6 → 5.** EPIC intraday short (live at 18:39) has expired/dropped off. Remaining character unchanged: NEAR/ADA/C tp-hit & expired, ZEC/XLM swing in-window.
- **Catalyst volume grew 512 → 773 events** (baskets still 3); unmapped ratio **66% → 67.1%** (still weak). Baskets refreshed: **ai_narrative** (NEAR/RENDER/TAO/FET/WLD, Hayes-dump driven, WLD −20%), **binance_ecosystem_teaser** (BNB/ASTER, sell-the-news), **momentum_breakout** (HEI +75.7% overextended, PORTAL +26.9% — `avoid_chase`, no news).
- **Untracked legacy alerts still 0** (clean, unchanged).
- **Signal-stats essentially flat / marginally softer** (sample 70→69, totalR +11→+9, winrate ~24%→23%, PF 1.55→1.45). Long-vs-short divergence persists (longs PF 2.75 / shorts PF 0.58) — feedback-only, small sample.

---

## 5. Catalyst Coverage

- Total `catalyst_events` today: **773**
- Mapped (non-null symbol): **254 (32.9%)**
- Unmapped (null symbol): **519 (67.1%)**
- `narrative_baskets`: **3** (binance_ecosystem_teaser, ai_narrative, momentum_breakout)
- **⚠ catalyst mapping weak this run (67.1% unmapped > 50%) — use catalyst layer as CONTEXT, not final decision.**
- Additional integrity note: many "mapped" rows are **stock tickers mis-suffixed as `/USDT`** (UNH/USDT ×17, NVDA/USDT ×13, LLY/USDT ×8, MSFT/USDT ×6, AMD/USDT ×5, QQQ/USDT ×3) — the symbol resolver is tagging equity-news catalysts as crypto pairs, inflating apparent crypto mapping. See §14 `TODO-catalyst-stock-usdt-mislabel`.
- Top 3 unmapped headlines (by importance):
  1. (0.748) *"South Korea is the ultimate backdoor tech play — but stock investors now face a looming…"*
  2. (0.678) *"Senate Calendar Crunch Forces Galaxy to Cut Clarity Act Odds by 15%"*
  3. (0.676) *"Anthropic Is Helping the NSA Hack China. It Also Wants Everyone to Pause AI"*

---

## 6. Market Landscape

- **Crypto regime: bearish trend / risk-off, confirmed by two independent reports (swing 14:46 + fresh intraday 21:13).** BTC downtrend, ETH downtrend, breadth above EMA20 **16.67%** — thin participation, any strength is large-cap-led relief inside a downtrend.
- **Macro overhang:** BTC slump continues post-May-jobs (172k added, unemployment 4.3%); headlines on US government BTC holdings halving to ~$21B and "AI's $800B spending boom becoming Bitcoin's Fed problem" (CryptoSlate). **Geopolitics:** Iran / Strait of Hormuz warning-shot headlines persist (carried from 16:24/18:39) — weekend escalation risk = Monday gap risk.
- **Crypto-specific credibility shock:** Zcash Orchard counterfeiting bug (privacy-coin counterfeiting class) → ZEC −50% peak-to-trough, **contagion to XMR −10%** (same researcher adding Monero to audit queue). Privacy-coin basket carries a fresh structural discount.
- **Narrative pockets (context only):** AI-rotation basket bleeding on the Arthur Hayes WLD dump (−20%); BNB/ASTER sell-the-news; **momentum cluster HEI +75.7% / PORTAL +26.9% with no news → `avoid_chase`, overextended.**
- **Stocks (closed, Monday planning):** active B-tier signals are uniformly **short** (QQQ, AMAT, SPY, XLK, MSFT, MEDP) — consistent with the risk-off macro; no live action this slot.

---

## 7. Candidate Deep Dives (≤ 5)

### 7.1 ZEC/USDT — swing LONG — **CONTRADICTION / HEADLINE RISK → AVOID (dead)**
- **Signal:** B, swing long, score 65.2, `tp2_hit`, entry $561.89–$567.42, invalidation $555.12, expires 2026-06-07T22:56 (nominally still in-window).
- **Internal records:** 17 catalyst events + 4 news_items in 24h for ZEC — all bearish (counterfeiting bug, $13M Binance withdrawal, XMR contagion). Internal data is recent and consistent → external re-verify done (major contradiction with a LONG).
- **External (verified §G):** Orchard circuit counterfeiting vulnerability (Taylor Hornby, AI-assisted audit, disclosed Jun 5); soft fork Jun 2 + NU6.2 hard fork Jun 3. Price: peak $624 (Jun 4) → low **$264.80** (Jun 5) → rebound **~$356**. Decrypt + news.bitcoin.com (WebFetch HTTP 200) + crypto.news.
- **LEGAL/HEADLINE RISK:** structural credibility shock — *"no cryptographic way to prove the bug was never abused"* (developers' own statement). Turnstile accounting reportedly shows no unauthorised value creation, but residual doubt is permanent for a privacy coin.
- **Price-reaction / chase check:** price has fully reacted and is **~37% below the signal's invalidation** ($356 vs $555). `tp2_hit` is a stale pre-crash artifact. Entry now would be catching a structurally-impaired falling knife. **No actionable level — this is not a setup, it is a defunct signal.**
- **Verdict: AVOID. Do not hold, do not initiate, do not "buy the dip" on the bug.**

### 7.2 XLM/USDT — swing LONG — **MANAGE-ONLY / NO-ADD**
- **Signal:** B, swing long, score 65.4, `tp1_hit`, entry $0.2544–$0.2587, invalidation $0.2490, expires 2026-06-07T22:36 (in-window).
- **Internal records:** **0 news_items in 24h**, no catalyst event for XLM this run → no fresh thesis, no fresh contradiction. (Note: XLM had a positive futures/hype mention back on Jun 1 per CoinDesk, now stale.)
- **Price-reaction / chase check:** counter-trend long (regime is "avoid weak altcoin longs") that already took TP1. With breadth at 16.7% and no fresh catalyst, **adding here fights the tape.** No fabricated chart read (chart MCP unavailable) — local fields only.
- **Verdict: MANAGE the runner to invalidation/TP per original plan; NO new entry, NO add.**

### 7.3 ADA/USDT — intraday SHORT — **REALIZED / EXPIRED (context)**
- **Signal:** B, intraday short, score 66.4, `tp2_hit`, expired 2026-06-06T11:58. Realized winner.
- **News (internal):** ADA under $0.20 at **4-year lows**, "social activity surges" (CoinDesk 03:30), "Is Cardano Dead after Hoskinson's confession" (BeInCrypto 05:25) — bearish thesis confirmed the short, now played out.
- **Verdict: No fresh entry. Capitulation/4-year-low zone — chasing a new short here is late (extended into a known support shelf). Watch for relief-bounce mean-reversion, not continuation.**

### 7.4 NEAR/USDT — intraday SHORT — **REALIZED / EXPIRED (context)**
- **Signal:** B, intraday short, score 66.7, `tp2_hit`, expired 2026-06-06T13:01. Realized winner.
- **News (internal):** Arthur Hayes "called $ZEC, $NEAR, $WLD… sold near the top" (Lookonchain 04:32); NEAR sits in the **ai_narrative basket** now bleeding on the Hayes exit. Geopolitics (Iran/Hormuz) adds risk-off pressure.
- **Verdict: No fresh entry. Short thesis realized; basket is crowded/unwinding — `related_beta_rotation` watch only.**

### 7.5 Market-level no-trade — **HEI / PORTAL momentum cluster → AVOID CHASE**
- `momentum_breakout` basket: **HEI/USDT +75.7%** (vol 1.87x, flagged overextended), **PORTAL/USDT +26.9%** (vol 9.37x), **no confirmed news catalyst.** Playbook = `avoid_chase`.
- **Verdict: AVOID. Pure momentum with no fundamental driver into a risk-off tape is the textbook weekend bull-trap. No entry.**

---

## 8. Best Candidates Ranked

**No clean candidates.** No A-tier anywhere; no fresh B-tier setup printed by either swing or the freshly-regenerated intraday report; every active crypto signal is either expired/realized (NEAR, ADA, C) or contradicted/manage-only (ZEC, XLM). This is a **stand-down / manage-only** slot.

---

## 9. Avoid / No Trade

- **ZEC/USDT long** — defunct, ~37% below invalidation, permanent structural credibility risk. AVOID.
- **HEI/USDT, PORTAL/USDT** — overextended momentum, no news, `avoid_chase`. AVOID.
- **New altcoin longs generally** — regime "avoid weak altcoin longs," breadth 16.7%. AVOID.
- **Chasing ADA/NEAR shorts** — thesis realized, extended into support / crowded unwind. NO new entry.
- **Stocks (Monday planning, NOT re-verified today):** carry-forward legal/headline avoids **SMCI** and **UNH** from prior reviews — flagged but NOT re-checked this closed-market slot (full legal re-verification deferred to a weekday slot, see §14).

---

## 10. Main Risks

- **Weekend gap risk into Monday's US open** — Iran/Strait-of-Hormuz escalation over the weekend would gap risk assets down and energy/defense up; crypto is the only live hedge/expression.
- **Thin weekend liquidity** — both directions are slippage-prone; the absence of a fresh setup is itself the signal to wait.
- **Privacy-coin contagion** — ZEC→XMR audit-queue spread could widen if other shielded-pool coins get flagged.
- **Data blind spots** — scalp report 16h stale (no live scalp levels); no chart/liquidation/order-book tooling; weekend price relies on June-5 prints.
- **Catalyst layer unreliable this run** — 67.1% unmapped + stock-as-USDT mislabeling; treat as context only.
- **Source-ingest** — see §13/§M; logged here if the ingest CLI errors: ingest result recorded below.

---

## 11. Action Plan — next 4 hours (into the 23:15 post-close slot)

1. **Stand down on new crypto entries.** No A/B setup, risk-off, thin book — patience is the edge.
2. **ZEC long:** treat as closed/dead; remove from any "active long" mental book. Do NOT dip-buy.
3. **XLM long:** manage existing runner to plan only; no add.
4. **Carry minimal/zero fresh weekend crypto exposure;** if holding, keep size down and stops honored.
5. **Monitor Iran/Hormuz headlines** — a weekend escalation is the main thing that would change the Monday gap thesis.
6. **Monday stocks prep (no action now):** short-skewed book (QQQ/AMAT/SPY/XLK/MSFT); keep SMCI & UNH on the legal-avoid list pending a weekday legal re-check.
7. **Re-pull live scalp/intraday levels before any entry** (scalp report stale).

---

## 12. Final Verdict per Mode

- **Crypto scalp:** NO TRADE. Report 16h stale, regime was "high-volatility danger"; re-pull live before acting. Stand down.
- **Crypto intraday:** NO TRADE. Fresh report (21:13) printed **No A-tier / No B-tier**, "short bias or no trade." No fresh setup; do not chase ADA/NEAR shorts or HEI/PORTAL momentum.
- **Crypto swing:** MANAGE-ONLY. ZEC long **AVOID/dead**; XLM long **no-add**; no new swing entry (breadth 16.7%, "avoid weak altcoin longs").
- **Stocks (all modes):** NO ACTION — market closed (Saturday). Monday planning skews **short**; legal-avoids SMCI/UNH carried forward (un-verified this slot).

---

## 13. Sources

External (verified this run):
- [Decrypt — ZEC Crashes 38% as Zcash Discloses 'Critical Counterfeiting Vulnerability'](https://decrypt.co/370105/zec-crashes-38-as-zcash-discloses-critical-counterfeiting-vulnerability) — 2026-06-05
- [news.bitcoin.com — Zcash Patches Critical Bug Enabling Unlimited Counterfeit ZEC Minting as Price Crashes 41%](https://news.bitcoin.com/zcash-orchard-counterfeiting-bug-patched/) — 2026-06-05 (WebFetch HTTP 200; "no cryptographic way to prove the bug was never abused")
- [crypto.news — Zcash price plunges 50% amid bug fallout and Hayes selloff](https://crypto.news/zcash-price-plunges-50-amid-bug-fallout-and-hayes-selloff-can-whales-reverse-the-trend/) — 2026-06-05 (low $264.80, rebound ~$356, turnstile framing)
- [Fortune — Current price of Bitcoin for June 5, 2026](https://fortune.com/article/price-of-bitcoin-06-05-2026/) — 2026-06-05 (BTC ~$61,928)
- [Yahoo Finance — Bitcoin and ethereum prices today, Friday, June 5, 2026](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-friday-june-5-2026-prices-continue-their-descent---5-reasons-why-113631165.html) — 2026-06-05 (ETH ~$1,666)

Internal news_items (DB `news_items`, not external-web; source + date, no URL fabricated):
- ZEC −38% counterfeiting disclosure — CryptoBriefing, 2026-06-06 13:55
- New wallet withdraws 37,316 ZEC ($13M) from Binance post-disclosure — CryptoBriefing, 2026-06-06 15:04
- Researcher adds Monero to audit queue, XMR −10% — BeInCrypto, 2026-06-06 16:31
- Cardano social activity surges as ADA falls under $0.20 to 4-year lows — CoinDesk, 2026-06-06 03:30
- Arthur Hayes called $ZEC/$NEAR/$WLD, sold near top — t.me/lookonchain, 2026-06-06 04:32

_Source-discipline: every external claim above has source + title + date + URL; no uncited stats; no fabricated chart observations (chart MCP unavailable, stated); internal-only claims labeled as such with date; no test/fixture sources. External web research was AVAILABLE this run._

---

## 14. Fix Requests / TODO

### TODO-scalp-report-staleness
- **issue:** Scalp report did not regenerate this cycle (~16h stale) while intraday + swing did; the generator-staleness regression has narrowed to scalp-only but persists.
- **evidence:** `data/reports/scalp/2026-06-06_02-38_scalp_report.md` gen 05:38 EEST vs intraday regenerated 21:13 EEST in the same `cycle_03_19-47` window.
- **suggested manual fix:** audit the scalp generator's schedule trigger / gating in the default scheduler; confirm scalp is wired into each cycle like intraday.
- **priority:** medium
- **first observed:** 2026-06-06 21:45 EEST (narrowed from the broader scalp+intraday regression flagged 18:39)

### TODO-catalyst-stock-usdt-mislabel
- **issue:** Equity-news catalysts are being mapped to crypto `/USDT` pairs (UNH/USDT, NVDA/USDT, LLY/USDT, MSFT/USDT, AMD/USDT, QQQ/USDT), inflating apparent crypto catalyst mapping and polluting crypto symbol resolution.
- **evidence:** `data/catalysts/2026-06-06/catalyst_events.jsonl` — symbol counter: UNH/USDT ×17, NVDA/USDT ×13, LLY/USDT ×8, MSFT/USDT ×6, AMD/USDT ×5, QQQ/USDT ×3 (all are NYSE/Nasdaq tickers, asset_class should be stocks).
- **suggested manual fix:** in the catalyst symbol resolver, gate `/USDT` suffixing on asset_class=crypto and/or a crypto-symbol allowlist; route equity tickers to the stocks asset class.
- **priority:** medium
- **first observed:** 2026-06-06 21:45 EEST

### TODO-catalyst-mapping-weak (recurring)
- **issue:** Catalyst mapping has been <50% for multiple consecutive runs (66% unmapped @18:39 → 67.1% @21:45).
- **evidence:** 519/773 unmapped this run; 338/512 prior run.
- **suggested manual fix:** improve the catalyst-layer symbol resolver (entity extraction + ticker dictionary); partly overlaps TODO-catalyst-stock-usdt-mislabel.
- **priority:** medium
- **first observed:** carried forward (recurring across recent reviews)

### TODO-intraday-mode-bucket (feedback)
- **issue:** Intraday mode is the worst-performing bucket (PF 0.14, 1W/7L, net −6R, week) per signal-stats; long-vs-short divergence (longs PF 2.75 vs shorts PF 0.58) persists.
- **evidence:** `signal-stats --asset-class crypto` by-mode + by-direction tables, this run.
- **suggested manual fix:** review intraday-mode scoring/thresholds; small sample, monitor before acting.
- **priority:** low
- **first observed:** 2026-06-06 21:45 EEST (feedback-only, small sample)
