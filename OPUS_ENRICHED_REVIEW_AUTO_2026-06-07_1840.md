# Opus Enriched Review — US open reaction review (Sunday → late-US-session crypto) — Auto Cycle 18:40 EEST

- **Generated:** 2026-06-07 18:40 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`, **18:30 "US open reaction" slot**, executing `opus-enriched-review-4h/SKILL.md`).
- **⚠ It is SUNDAY — US & EU cash equities are CLOSED.** There is no US cash session today; the "US-open-reaction" label maps to **late-weekend / pre-Monday crypto**. The next US open is **Monday 2026-06-08**. **Crypto is the only live, actionable class; all stock signals are planning/watchlist context for the Monday reopen.**
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-07_1630.md` (pre-US-open decision review, 16:30 EEST, ~2.2h ago — see §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). **WebFetch verified live Binance ticker this run: BTC $62,088 (+1.99% 24h), ETH $1,633 (+4.41% 24h).**
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; structure = local OHLCV/ATR/EMA report fields + cited external prints.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

- **Relief bounce continues, still ZERO fresh A/B in any crypto mode.** Live tape this run: **BTC $62,088 (+1.99% 24h)**, **ETH $1,633 (+4.41% 24h)** — ETH again leading the bounce off the $59–60K BTC floor. But the **fresh 18:29 scalp report (data 15:15 UTC) flipped the regime label back to "bearish trend (risk-off)"** (BTC & ETH downtrend, breadth EMA20 37.2%), slightly more cautious than the 16:30 intraday "transition (mixed)". Net read: **basing/relief, not a confirmed reversal — no clean setup either direction.** Scalp: **No A-tier, No B-tier**; best watchlist OPN 64.2. Intraday (carry-forward 15:48): **No A/B**; best watchlist BANK 59.1.
- **⚠ DATA CONTRADICTION FLAGGED:** the fresh scalp report's macro headline reads **"Iran launches drones toward Strait of Hormuz… Bitcoin slides below $73K"** — but live BTC is **$62,088**, i.e. ~$11K *below* $73K. That RSS headline is **stale** (BTC first slid below $73K weeks ago) and is being surfaced as a current macro driver. Context only; does not change the bearish-but-basing read. See §14 TODO.
- **Active book = realized winners + management only, nothing fresh to chase.** 6 active crypto signals, all mature: **NEAR & ADA intraday SHORTS (`tp2_hit`, expired 06-06 — realized runners), C scalp LONG (`tp1_hit`, realized), ZEC & XLM swing LONGS (`tp2_hit`/`tp1_hit`) that EXPIRE TONIGHT ~22:5x EEST**, plus a **PORTAL B scalp LONG `waiting_for_entry` whose `expires_at` (15:46 EEST) has already passed → expired UNFILLED, dead.** No A/B triggered this cycle in any mode.
- **Signal-stats (feedback-only, n=70, week):** A/B PF **1.45**, **+9R**, winrate 23.1%. By-mode: **swing +11R (PF 12.0), intraday +4R (PF 1.33), scalp worst −6R (PF 0.14, 1W/7L).** By-direction: **SHORT +14R (PF 2.75) vs LONG −5R (PF 0.58)** — the week's edge was the short side into the down-move, but with the tape bouncing and no fresh A/B short triggered, that edge is **not actionable at market.** Untracked legacy alerts **0** (clean).
- **Catalyst layer context-only — 75.3% unmapped (weak, ≥5 consecutive runs).** Same JSONL as 16:30 (no newer catalyst cycle since 15:48). One basket: `momentum_breakout` (primary **FIDA/JTO/BANK**, playbook **`avoid_chase`**, FIDA overextended +75%). Top mapped catalysts remain **stocks legal-risk** (SMCI export-control indictment 8-K; UNH DOJ probe −16%) — closed-market context.
- **Stocks (closed, Sunday):** active count **dropped 264 → 50** vs the 16:30 run (notable — realized intraday shorts appear to have aged out; §14). Standouts for the **Monday** reopen: **A-tier swing LONGS triggered — AAPL 83.8, LLY 83.8, AMD 81.8**; **A-tier invest LONGS waiting — LLY 82.1, AAPL 80.6.** **LLY now carries FRESH headline risk** (FDA delayed obesity-drug ruling + an FDA liver-failure report tied to Foundayo/orforglipron) → verify trigger live, not a clean long. SMCI/UNH legal-risk flags persist.
- **Posture into Monday:** crypto **stand-down / no-chase both directions.** Only level that matters: **BTC $60K / 200-week MA** — acceptance → first long-side A/B becomes plausible on a clean retest; loss of **$59.1K** (June-5 low) → downside re-opens. Manage the two expiring swing longs; no new weekend initiations.

---

## 2. Data Used

**Internal — crypto reports (mtime / freshness):**
- `data/reports/scalp/2026-06-07_15-29_scalp_report.md` — gen **18:29 EEST**, data 15:15 UTC, **~11 min → FRESH.** Regime **bearish trend (risk-off)**; BTC & ETH downtrend; breadth EMA20 37.2%; BTC ATR pct 73; **No A-tier, No B-tier**; best watchlist OPN 64.2.
- `data/reports/intraday/2026-06-07_12-48_intraday_report.md` — gen **15:48 EEST, ~2.9h → CARRY-FORWARD.** Regime transition (mixed); breadth 39.0%; **No A-tier, No B-tier**; best watchlist BANK 59.1.
- `data/reports/swing/2026-06-06_14-46_swing_report.md` — gen 17:46 EEST 06-06, **~25h STALE** (>14h band; excluded from final swing verdict except direction context — §3).
- Stocks reports (intraday/swing/invest all 06-05, ~43–49h) — **weekend, closed → context only.**

**Catalyst / narrative:** `data/catalysts/2026-06-07/` — `catalyst_events.jsonl` (**958 rows**, mtime 15:48), `narrative_baskets.jsonl` (**1 basket**, `momentum_breakout`), latest cycle `catalyst_cycle_12-48.md`. Day-cumulative mapped **237/958 (24.7%)**, unmapped **721/958 (75.3%)** → **weak (§5).** No newer catalyst cycle since the 16:30 run.

**LLM packets:** `data/processed/llm_analysis_packet.md` (crypto, mtime 18:30), `data/processed/llm_stocks_packet.md` (06-05, closed-market context).

**Scheduler:** latest folder `data/scheduled_runs/2026-06-07_default_schedule/`; `scheduler.log` mtime **18:30 EEST (~10 min)**; latest cycle summary `cycle_02_14-36_summary.md` mtime **15:51 (~2.8h)**. scheduler.log fresh → **NO DEFER** (both-stale condition not met; a cycle is mid-run, having just emitted the 18:29 scalp).

**CLI / DB (read-only, this run):**
- `active-signals` crypto = **6** (PORTAL B scalp long `waiting_for_entry` exp 15:46 → **expired unfilled**; NEAR/ADA intraday short `tp2_hit`; C scalp long `tp1_hit`; ZEC swing long `tp2_hit` exp ~22:56; XLM swing long `tp1_hit` exp ~22:36 — all crypto longs realized/expiring, shorts realized).
- `active-signals` stocks = **50** (Friday-dated, weekend-frozen): A-tier swing longs **AAPL/LLY/AMD `triggered`**; A-tier invest longs **LLY/AAPL `waiting_for_entry`**; B invest longs AMD/SMH/XLK; C invest longs SMCI (legal)/UNH (legal); intraday shorts QQQ/META `tp1/tp2_hit`; NVDA swing short `triggered`.
- `signal-stats` crypto week — headline A/B **n=70, triggered=52, 12W/20L, winrate 23.1%, PF 1.45, avgR 0.17, totalR +9.0**; by-mode **scalp −6R (PF 0.14, 1W/7L)**, **swing +11R (PF 12.0, 5W/1L)**, **intraday +4R (PF 1.33)**; by-direction **short +14R (PF 2.75) / long −5R (PF 0.58)**; by-setup losing bucket n=27 PF 0.41 (−7R) vs winning n=36 PF 2.75 (+14R).
- `detect_untracked_legacy_alerts --since 2026-06-07` → **None (0)** — clean.

**External (cited §13):** live BTC $62,088 (+1.99%) / ETH $1,633 (+4.41%) (Binance ticker, WebFetch verified this run); record ~$3.4B weekly spot-BTC-ETF outflow / ~$4.21B over three weeks; ~$1.8B liquidations June 3 (largest since Feb 2026); Fear & Greed 12 (Extreme Fear, June 3); BTC ~−51% from Oct-2025 ATH ~$126,200; support ~$60K. LLY: FDA delayed obesity-drug ruling + FDA liver-failure report on Foundayo/orforglipron; 340B antitrust class action + insulin-pricing MDL (long-standing).

**Unavailable / blind:** continuous intraday tick (single live snapshot only); TradingView/Chrome chart verification (not loaded); liquidation heatmaps / order-book / CVD; live social/KOL feeds (lookonchain rows are bot/single_source).

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-07_default_schedule/`.
- `scheduler.log` mtime **18:30 EEST (~10 min)** → fresh; latest cycle summary `cycle_02_14-36_summary.md` mtime **15:51 (~2.8h)**. scheduler.log << 3h → **NO DEFER** (both-stale defer condition not met). A new cycle is mid-run — it just emitted the **18:29 scalp** (data 15:15 UTC).
- Freshness labels: scalp **FRESH (~11 min)**, intraday **CARRY-FORWARD (~2.9h)**, swing **STALE (~25h, excluded from final swing verdict)**. Stocks **stale/closed → context only.**
- Note: the fresh scalp regime label is **"bearish trend (risk-off)"** — a step *more cautious* than the 16:30 intraday "transition (mixed)" read; both are pre-A/B (no clean setup).

---

## 4. What Changed vs Previous Review (pre-US-open 16:30 → US-open-reaction 18:40, ~2.2h)

- **Bounce held / extended slightly.** 16:30: BTC $61,844 (+1.6%), ETH $1,622 (+3.7%). This run: **BTC $62,088 (+1.99%), ETH $1,633 (+4.41%)** — same relief structure, ETH still the RS leader, marginally firmer. No regime breakout; still **no A/B**.
- **Fresh scalp regime label re-hardened to "bearish (risk-off)."** The 16:30 read leaned on a "transition (mixed)" 15:15-data scalp + 15:48 intraday; the brand-new **18:29 scalp** (also 15:15-UTC data) prints **bearish trend (risk-off)**, breadth EMA20 39.0% → **37.2%**. Marginally more cautious; still pre-A/B.
- **New active signal: PORTAL B scalp long** appears in the active set (was 5 → now 6) — but its `expires_at` is **15:46 EEST (already past)** and status is `waiting_for_entry` → it **expired UNFILLED**, never triggered (price ~0.0179 stayed below the 0.0182–0.0187 entry). Dead, not a new actionable. (Another instance of the expired-still-active hygiene issue — §14.)
- **Stocks active count dropped 264 → 50.** A large change vs 16:30. Appears the realized Friday intraday shorts aged out of the active set; the residual 50 are the weekly swing/invest book + a handful of `tp1/tp2_hit` intraday shorts. Reduces the weekend "phantom exposure" read — net positive, but worth confirming the cause (§14).
- **NEW headline risk on LLY (A-tier long).** Not present in the 16:30 review's clean LLY framing: **FDA delayed the obesity-drug ruling + an FDA liver-failure report tied to Foundayo (orforglipron)**; plus standing 340B/insulin litigation. LLY long is now "verify trigger live, headline risk" not a clean Monday actionable.
- **Catalyst layer unchanged** (same 958-row JSONL, 75.3% unmapped, 1 `momentum_breakout` basket) — no new catalyst cycle ran in the ~2.2h gap.
- **Signal-stats: n 69 → 70** (one new signal entered the week sample); headline PF 1.45 / +9R and the mode/direction triplet unchanged. Untracked alerts still **0**.
- **Two expiring swing longs (ZEC ~22:56, XLM ~22:36) now ~4h from expiry** (were ~6.5h at 16:30) — same realized/let-expire framing, closer to the event.

---

## 5. Catalyst Coverage

- Total `catalyst_events` today (06-07, day-cumulative): **958**
- Mapped (non-null symbol): **237 (24.7%)**
- Unmapped (null symbol): **721 (75.3%)**
- `narrative_baskets`: **1** (`momentum_breakout`, primary **FIDA/JTO/BANK**, playbook **`avoid_chase`**, single_source, fresh <1h; FIDA overextended +75%).
- By type: other_news 889, legal_risk 24, analyst_action 17, partnership 11, regulatory_sector_headline 5, product_launch 4, exchange_delisting 2, insider_activity 2.
- **⚠ CATALYST MAPPING WEAK THIS RUN (75.3% unmapped > 50%) — use the catalyst layer as context, NOT a final decision input.** Now >50% unmapped for **≥5 consecutive runs** (67.1% → 68.7% → 73.0% → 75.3% → **75.3%**) → recurring; see §14 TODO.
- Top 3 unmapped / null-symbol high-importance headlines:
  1. `0.71` US Supreme Court backs FCC and SEC in key regulatory rulings that reshape enforcement landscape (CryptoBriefing) — macro/regulatory, no resolvable ticker.
  2. `0.68` Why is the crypto market down today? ETF outflows, $1.3B liquidations, and more (AMBCrypto) — market-wide (BTC+ETH-relevant but mapped null).
  3. `0.68` South Korea is the ultimate backdoor tech play — but stock investors now face a looming threat (MarketWatch) — equities color, no crypto ticker.

---

## 6. Market Landscape

- **Regime: bearish-but-basing after the weekly washout.** Fresh scalp = **bearish trend (risk-off)** (BTC & ETH downtrend on report data; breadth EMA20 37.2%, EMA50 23.3%; BTC ATR pct 73 — elevated but off the 80–81 highs). Live tape, however, is the **third consecutive relief read**: BTC $62,088 (+1.99%) defending the $60K shelf / 200-week MA, **ETH $1,633 (+4.41%) leading**. Floor lifting at the margin, ceiling intact — no clean trend to lean on.
- **Macro drivers (external, §13):** the bearish stack is **easing but not cleared** — record ~$3.4B weekly spot-BTC-ETF outflow (~$4.21B over three weeks) is the dominant overhang; ~$1.8B liquidations June 3 (largest since Feb, $1.35B longs); Fear & Greed hit **12 (Extreme Fear)** June 3; BTC ~**−51% from the Oct-2025 ATH ~$126,200**. Offsetting positives carried from 16:30: ETF-outflow streak broke June 5 (+$3.05M first June inflow), dovish Trump-on-Fed headline, ETH bid. Net: **capitulation-then-relief, unconfirmed bottom.**
- **Where money flows (internal):** the `momentum_breakout` cluster — **FIDA +68% 24h** (overextended, vol 0.23x), **JTO +24% (vol 0.43x)**, GIGGLE +15% (vol 2.36x), SAHARA +9% (vol 5.01x but >2 ATR from EMA20, rejected) — all **single_source / no confirmed news**, playbook **`avoid_chase`**. ETH/SOL/BTC carry only single_source on-chain/Telegram notes (ZEC short-close, Solana USDC mint).
- **Stocks (frozen, closed):** 50 weekend signals. The bullish weekly book is intact for the Monday reopen — **A-tier swing longs AAPL/LLY/AMD `triggered`**, **A-tier invest longs LLY/AAPL `waiting`** — alongside residual index/mega-cap intraday SHORTS (QQQ/META `tp1/tp2_hit`) and NVDA swing short. Legal/headline overhangs: **SMCI** (export-control indictment 8-K), **UNH** (DOJ probe −16%), and now **LLY** (FDA delay + liver-failure report).
- **Bottom line:** the short edge that paid the week is largely realized (shorts banked, tape bouncing); the long side is unconfirmed (no A/B, weak volume, regime bearish-basing). **Disciplined read into Monday = no-chase both ways; let BTC prove $60K acceptance or rejection.**

---

## 7. Candidate Deep Dives (≤5)

### 7.1 BTC/USDT — macro anchor / $60K & 200-week-MA pivot + stale-headline contradiction → **NO TRADE (watch the level)**
- **State:** live **$62,088 (+1.99% 24h)**, range/basing above the $60K handle (at the 200-week MA, first test since 2023). Support stack $60K → $58–55K; overhead resistance $70–74K. Internal scalp trend = downtrend (bearish regime), so report and live tape diverge (report bearish, live bouncing).
- **Data contradiction:** scalp macro headline says **"Bitcoin slides below $73K"** — stale; BTC is at $62K, ~$11K below $73K. The headline mis-states the current level and is surfaced as a live macro driver. Verified against live ticker; treat the headline as noise (§14).
- **Price-reaction / chase check:** down-leg already reacted (−14% MTD, −51% from ATH); the +2% bounce is *relief*, not a breakout. No A/B trigger. Entry NOW = mid-no-man's-land between $59.1K support and far overhead resistance — no edge.
- **Verdict: NO TRADE — the pivot, not a position.** Hold $60K / 200-wk MA with acceptance → first long-side A/B plausible on a clean retest. Lose **$59.1K (June-5 low)** → downside re-opens. This level governs the book into Monday.

### 7.2 ETH/USDT — RS leader of the bounce → **NO TRADE / WATCH (the confirming tell)**
- **State:** live **$1,633 (+4.41% 24h)** — strongest major again, outperforming BTC. Internal trend "downtrend" on the report; live bid leading. Overhang: $168M ETH-ETF exodus / whale-absorption question + multi-day ETH-ETF outflow streak.
- **Price-reaction / chase check:** +4.4% bounce off a deeply-sold base; no A/B trigger; report still frames ETH as a downtrend laggard. Chasing mid-bounce into an active ETF-exodus overhang = poor RR.
- **Verdict: NO TRADE. Watch as the relative-strength tell** — ETH leading + BTC holding $60K together would firm the basing thesis. Not actionable at market.

### 7.3 ZEC/USDT + XLM/USDT — swing LONGS expiring tonight → **REALIZED / LET-EXPIRE, NO ADDS**
- **State:** **ZEC** swing long `tp2_hit` (entry $561–567; tp1/tp2 banked historically; now far below), **expires ~22:56 EEST.** **XLM** swing long `tp1_hit` (entry $0.254; tp1 $0.270 banked), **expires ~22:36 EEST.**
- **Price-reaction / chase check:** gains already captured; swing report **STALE (~25h, excluded)** → no fresh structure to justify holding/adding past expiry. ZEC still carries the earlier protocol-integrity discount.
- **Verdict: REALIZED / MANAGE-ONLY.** Let both expire on schedule (or close residual runner into strength). **No adds, no re-entry** — counter-tape longs on a stale report with the win banked.

### 7.4 momentum_breakout basket (FIDA / JTO / BANK) → **AVOID-CHASE**
- **State:** the single active narrative basket — **FIDA +68% 24h** (overextended, vol 0.23x), **JTO +24%** (vol 0.43x), BANK +9–12% (best intraday watchlist). All **single_source, no confirmed news**; playbook **`avoid_chase`**; FIDA explicitly flagged overextended; SAHARA (+9%, vol 5.01x) rejected as >2 ATR from EMA20.
- **Price-reaction / chase check:** moves already happened on thin volume; textbook overextended-spike profile. Entry NOW = chasing into a bearish-regime tape.
- **Verdict: AVOID-CHASE.** Only a structured pullback that holds with volume (BANK conditional zone ~0.0326–0.0334) would be watch-worthy — not at market.

### 7.5 Stocks A-tier longs (LLY / AAPL / AMD) — Monday-reopen planning → **NO ACTION (closed); LLY = HEADLINE RISK / verify live**
- **State:** **A-tier swing longs `triggered`: AAPL 83.8, LLY 83.8, AMD 81.8**; **A-tier invest longs `waiting_for_entry`: LLY 82.1, AAPL 80.6** (entries below Friday close). Market CLOSED (Sunday) — these are Friday-dated and frozen.
- **LEGAL/HEADLINE RISK (LLY):** FDA **delayed its obesity-drug ruling** and an **FDA liver-failure report is tied to Foundayo (orforglipron, a GLP-1 drug)**; standing 340B antitrust class action + insulin-pricing MDL (long-standing, lower-acuity). The FDA safety signal + delayed ruling is a genuine near-term overhang. Sources §13. → LLY is **not a clean long**; verify the entry trigger live at the Monday reopen and weigh the FDA headline before any execution.
- **Price-reaction / chase check:** N/A live (closed). AAPL/AMD A-tier longs show no fresh adverse headline this run — standard "verify fill from a live level, not a Friday print" caveat applies. SMCI (export-control indictment 8-K) and UNH (DOJ probe −16%) remain **AVOID clean longs**.
- **Verdict: NO ACTION (market closed).** Carry into the Monday open slots: AAPL/AMD A-tier longs as the cleanest constructive names; **LLY long gated by FDA headline risk**; SMCI/UNH legal-risk avoid.

---

## 8. Best Candidates Ranked

**No clean candidates.** No A-tier or B-tier setup triggered in any *crypto* mode; every crypto name is watchlist, realized, or avoid-chase. Stocks A-tier names exist but the market is **closed**. Ordered by "closest to becoming actionable":

1. **BTC/USDT long** — only on a *clean retest that holds* the $60K / 200-week-MA shelf with volume → first tape-aligned long-side A/B; **not triggered.**
2. **ETH/USDT long** — the RS tell; needs BTC confirmation + a real trigger; **not triggered.**
3. **A fresh failed-bounce SHORT** (NEAR/ADA-style) — only if BTC *rejects* $60K back toward $59.1K; **not triggered.**
4. **(Stocks, Monday) AAPL / AMD A-tier longs** — cleanest constructive equities for the reopen; verify live, not actionable today (closed).

The week's directional edge is short, but the live bounce neutralizes it intraday — **nothing to action at market.**

---

## 9. Avoid / No Trade

- **FIDA / JTO / SAHARA momentum at market — AVOID-CHASE.** +24–68% spikes, thin/overextended, no confirmed news, basket playbook `avoid_chase`.
- **ZEC / XLM long adds — NO.** Wins banked; expiring tonight; stale swing report; no re-entry.
- **NEAR / ADA short re-entry at market — NO.** Fights today's relief bounce; not triggered.
- **PORTAL B scalp — DEAD.** `waiting_for_entry` past its 15:46 expiry → expired unfilled; not an entry.
- **Any weak-volume altcoin long chasing the bounce** — exactly what the bearish-regime engine warns against ("short bias or no trade; avoid weak altcoin longs").
- **Stocks (all 50 signals) — NO ACTION.** Market closed (Sunday). Planning/management for the **Monday** open only.
  - **LLY — LEGAL/HEADLINE RISK:** FDA delayed obesity-drug ruling + FDA liver-failure report on Foundayo/orforglipron. Verify live before any long; not clean.
  - **SMCI — LEGAL/HEADLINE RISK:** SEC 8-K (FY2026) export-control-violation indictment of three individuals. AVOID clean longs at reopen.
  - **UNH — LEGAL/HEADLINE RISK:** DOJ antitrust/fraud probe; shares −16%. AVOID clean longs.

---

## 10. Main Risks

- **Bounce-fade / false-dawn:** the +2%/+4.4% relief is off a deeply-sold base into a thin Sunday book; one June-5 inflow does not end a $3.4–4.2B outflow regime. A failure back under **$59.1K** re-opens downside. Do not treat the bounce as a confirmed bottom (Fear & Greed was 12 / Extreme Fear on June 3).
- **Weekend → Monday gap risk:** thin weekend liquidity + the Monday US-equity reopen (frozen Friday risk-off short book, plus A-tier longs waiting) can gap crypto and equities either way. The crypto book is flat/realized → gap exposure low; keep it that way (no new weekend initiations).
- **Report-vs-live regime divergence:** the fresh scalp says bearish-downtrend while live BTC/ETH are green — trade the level (BTC $60K), not the label.
- **Stale-headline contamination:** the "$73K" macro headline in the fresh report is weeks old; the RSS/news layer is surfacing stale items as current drivers (§14). Cross-check any headline-driven thesis against live price.
- **Catalyst layer unreliable (75.3% unmapped, recurring ≥5 runs)** — do not let it drive decisions.
- **Stale swing report (~25h):** ZEC/XLM swing structure is not fresh; rely on realized/expiry framing.
- **Blind spots:** single live-ticker snapshot only; no chart MCP, no liquidation/order-book/CVD/social feeds (noted unavailable — not fabricated).
- **Ingest:** sources for this run built into `data/raw/enriched_review_sources/2026-06-07_1840.json` and UPSERTed into `news_items` (crypto, 3 rows) — see §13.

---

## 11. Action Plan — next 4 hours (into the Monday US open)

1. **Crypto: stand down / no new entries.** No A/B triggered; fresh regime bearish-basing. Do not chase the bounce or re-short into it.
2. **Watch the one level — BTC $60K / 200-week MA:** clean *acceptance* (hold + retest with volume) → first long-side A/B plausible; *rejection* under **$59.1K** → downside re-opens and a failed-bounce short re-qualifies. ETH leading (+4.4%) is the confirming tell.
3. **Manage the two expiring swing longs:** ZEC (~22:56) and XLM (~22:36) — let expire on schedule or close residual runner into strength; **no adds, no re-entry.**
4. **Momentum basket:** FIDA/JTO/BANK = `avoid_chase`; only a structured pullback that holds (BANK ~0.033) with volume would be watch-worthy — not at market.
5. **Stocks (closed):** no action. Carry **AAPL/AMD A-tier longs** (cleanest) and **LLY (FDA headline risk — verify live)** into the Monday open; keep **SMCI/UNH legal-risk** avoid flags.
6. **Next slot (21:30 — late-session risk review):** re-scan the fresh cycle for any newly-triggered A/B; re-check BTC $60K acceptance/rejection; confirm ZEC/XLM expired cleanly.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** **NO TRADE / WATCHLIST.** Fresh 18:29 report, regime bearish (risk-off); no A/B; best watchlist OPN 64.2 (below threshold). Stand down; no-chase the bounce.
- **Crypto intraday:** **NO TRADE / WATCHLIST.** Carry-forward 15:48 report; no A/B; realized NEAR/ADA shorts banked; ETH +4.4% is a watch-tell, not a trigger.
- **Crypto swing:** **MANAGE-ONLY.** Swing report stale (~25h, excluded). ZEC & XLM longs = realized, expire tonight, no adds/re-entry.
- **Stocks (all modes):** **NO ACTION — market closed (Sunday).** A-tier longs (AAPL/AMD cleanest; LLY gated by FDA headline risk) + SMCI/UNH legal-risk flagged for the Monday reopen. Verify any fill from a live level, not a Friday print.

---

## 13. Sources

- [Binance public ticker API — /api/v3/ticker/24hr (this run, ~18:40 EEST 2026-06-07)](https://api.binance.com/api/v3/ticker/24hr?symbols=BTCUSDT,ETHUSDT) — **WebFetch verified: BTC $62,088.18 (+1.99% 24h), ETH $1,633.05 (+4.41% 24h).** _primary_source (exchange API)._
- [StealthEX — Bitcoin Price Drop Today: Why Is BTC Crashing Right Now? (June 2026)](https://stealthex.io/blog/why-is-bitcoin-dropping/) — record ~$3.4B weekly spot-BTC-ETF outflow (largest since 2024 launch); ~$1.8B liquidations June 3 ($1.35B longs, largest since Feb 2026); Fear & Greed 12 (Extreme Fear) June 3; BTC ~−51% from Oct-2025 ATH ~$126,200; support ~$60K. _single_source (WebSearch snippet, date unavailable on snippet)._
- [bitcoinfoundation.org — Bitcoin ETF Outflows June 2026: $1.67B Weekly](https://bitcoinfoundation.org/news/crypto-etfs-news/crypto-etfs-june/) — third consecutive weekly outflow; ~$4.21B over three weeks. _single_source (WebSearch snippet, date unavailable on snippet)._
- [Yahoo Finance — LLY Stock Falls After FDA Reportedly Delays Obesity Drug Ruling](https://finance.yahoo.com/news/lly-stock-falls-fda-reportedly-154700821.html) — FDA reportedly delayed an Eli Lilly obesity-drug ruling. _single_source (WebSearch snippet, date unavailable on snippet)._
- [TheStreet — Eli Lilly stock swings after FDA liver failure report for GLP-1 drug](https://www.thestreet.com/investing/stocks/eli-lilly-stock-swings-after-fda-liver-failure-report-for-glp-1-drug) — one FDA liver-failure report tied to Foundayo (orforglipron). _single_source (WebSearch snippet, date unavailable on snippet)._
- Internal (no external URL): scalp `2026-06-07_15-29_scalp_report.md`, intraday `2026-06-07_12-48_intraday_report.md`, `catalyst_events.jsonl` (958 rows), `narrative_baskets.jsonl`, `signal-stats`/`active-signals`/`detect_untracked_legacy_alerts` CLI outputs (this run).

_Source-discipline (§N): every external claim carries source + title + (date where available) + URL; published_at marked null/"date unavailable" where the snippet did not state one (never invented); no uncited stats; no uncited legal claims; no fabricated chart observations (chart MCP not loaded — declared); no test_source/fixture URLs (ingest rejected 0); §13 present; external research was AVAILABLE this run. WebSearch-snippet sources are labelled as such (only the Binance ticker was individually WebFetch-verified)._

---

## 14. Fix Requests / TODO

### TODO-stale-macro-headline-surfaced (NEW)
- **issue:** The fresh 18:29 scalp report surfaces **"Iran launches drones toward Strait of Hormuz… Bitcoin slides below $73K"** as a current macro headline/driver, but live BTC is **$62,088** (~$11K below $73K) — the headline is weeks old and mis-states the current level. Stale RSS items are being presented as live macro context.
- **evidence:** `data/reports/scalp/2026-06-07_15-29_scalp_report.md` §4 Macro headline + §5 Top news ("…Bitcoin slides below $73K", CryptoBriefing); contradicted by Binance live ticker BTC $62,088 this run.
- **suggested manual fix:** add a recency/price-sanity filter to the macro/news layer — drop or de-rank headlines whose embedded price level is far from current spot, and/or hard-cap headline age (e.g. exclude items older than 24–48h from the "Macro headline / Top news" slots).
- **priority:** medium
- **first observed:** 2026-06-07 18:40 EEST

### TODO-catalyst-mapping-weak (recurring)
- **issue:** Catalyst symbol-mapping has been <50% for **≥5 consecutive runs** (unmapped 67.1% → 68.7% → 73.0% → 75.3% → **75.3%** today), forcing the catalyst layer to "context-only" every slot.
- **evidence:** `data/catalysts/2026-06-07/catalyst_events.jsonl` 237/958 mapped (24.7%); by-type other_news=889 of 958. Top unmapped are macro/regulatory/sector headlines (US Supreme Court FCC/SEC ruling, "why is the market down" ETF-flow piece, MarketWatch South Korea) with no resolvable single ticker.
- **suggested manual fix:** improve the resolver — add market-wide/macro tagging (map rates/Fed/ETF-flow/regulatory headlines → BTC+ETH basket; sector headlines → narrative basket) so macro items stop counting as fully unmapped; or split the metric into "macro/no-symbol-expected" vs "should-have-mapped-but-didn't."
- **priority:** medium
- **first observed:** 2026-06-06 (carried); reconfirmed 2026-06-07 18:40 EEST

### TODO-expired-signals-still-active (carried)
- **issue:** Signals past `expires_at` still surface in `active-signals`. This run: **PORTAL/USDT B scalp `waiting_for_entry` with `expires_at` 2026-06-07T15:46 (already past)** appears as active though it expired unfilled (never triggered); plus the prior NEAR/ADA `tp2_hit` shorts past their 06-06 expiry. Inflates the "active" count / can read as live exposure.
- **evidence:** `active-signals --asset-class crypto` (this run) shows PORTAL `waiting_for_entry` exp 15:46:28; NEAR exp 2026-06-06T13:01 `tp2_hit`; ADA exp 2026-06-06T11:58 `tp2_hit`.
- **suggested manual fix:** exclude `waiting_for_entry` signals whose `expires_at` has passed from the active set (mark `expired_unfilled`); and give realized-but-expired runners a distinct status/label (e.g. `runner`/`realized_open`) so the active count reflects genuinely live, unexpired signals.
- **priority:** low
- **first observed:** 2026-06-07 16:30 EEST (carried)

### TODO-stocks-active-count-swing (low / observation)
- **issue:** `active-signals --asset-class stocks` returned **~264 at 16:30 but 50 at 18:40** the same closed-market day. The drop is plausibly the realized Friday intraday shorts aging out (net positive for the "phantom weekend exposure" read), but a ~5× swing in the active count within ~2h with the market closed warrants a sanity check on the count's status filter / expiry handling.
- **evidence:** 16:30 review §2 reported stocks active ≈264; this run `active-signals --asset-class stocks` header = "Active signals (50)".
- **suggested manual fix:** confirm what changed the count (expiry of `tp1/tp2_hit` intraday shorts vs a filter change); apply consistent realized/runner labeling to stocks so the weekend "active" view is stable and reflects only genuinely open exposure.
- **priority:** low
- **first observed:** 2026-06-07 18:40 EEST
