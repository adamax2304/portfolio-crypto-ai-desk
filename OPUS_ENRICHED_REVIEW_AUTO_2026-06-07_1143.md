# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:43 EEST

- **Generated:** 2026-06-07 11:43 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`, **Europe / pre-US context** slot 11:30, executing `opus-enriched-review-4h/SKILL.md`).
- **⚠ It is SUNDAY — US & EU cash equities are CLOSED.** Stock signals = planning/watchlist context only; **crypto is the only live, actionable class this slot.**
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-07_0439.md` (crypto overnight / Asia review, 04:39 EEST, ~7.1h ago — see §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). **WebFetch verified HTTP 200 on CoinDesk (June 4): BTC $62,437.70, ETH $1,619.66, $1.5B 24h liquidations.** Invezz fetch returned HTTP 403 (used WebSearch summary instead: BTC sub-$60K / $59.1K on June 5).
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; structure = local OHLCV/ATR/EMA report fields + cited external prints.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

- **No reversal into Europe — crypto remains bearish risk-off, no actionable setup.** Latest scalp (03:19) and intraday (04:00) reports both independently print *"bearish trend (risk-off); short bias or no trade; avoid weak altcoin longs."* Altcoin breadth above EMA20 **15.0%** (thin). **Neither report produced a single A-tier or B-tier setup.** BTC ATR percentile 80–81 (elevated vol). A fresh full scheduler cycle is **running right now** (booted 11:08, mid-cycle) but had not emitted a new scalp/intraday report at review time — current reports are ~7.6–8.4h old but the regime read is unchanged and corroborated externally.
- **Prices grind lower in the same band, confirmed external (§13):** BTC traded **$62,437 (June 4) → sub-$60K / ~$59,100 (June 5)**; ETH **$1,619 (June 4 CoinDesk) → ~$1,565 internal (June-7 freshness)**. Drivers unchanged and intensifying: a **record 13-session spot-BTC-ETF outflow streak (~$4.3–4.4B / ~59.3K BTC)**, a 17-day ETH-ETF outflow streak, a Strategy (MSTR) BTC sale, the post-jobs "higher-for-longer" Fed repricing, and capital rotation into gold/AI equities.
- **Active book = manage/stand-down, unchanged from 04:39.** Same **5 active crypto signals**: **NEAR & ADA intraday SHORTS** (realized `tp2_hit`/expired); **C scalp long** (expired); **ZEC swing LONG = AVOID/dead** (price ~$362 vs invalidation ~$555, ~35% below — defunct post-counterfeiting-crash artifact); **XLM swing LONG = manage-only/no-add.** No fresh actionable in any mode.
- **Signal-stats (feedback-only, n=69, week):** A/B PF **1.45**, +9R, winrate 23.1%. **Direction edge is decisive — shorts +14R (PF 2.75) vs longs −5R (PF 0.58)** in this bear tape; cross-exchange-confirmed +10R (PF 2.11) vs Binance-only −3R (PF 0.57). By-mode (current CLI): **swing best +11R (PF 12.0), intraday +4R (PF 1.33), scalp worst −6R (PF 0.14, 1W/7L).** Untracked legacy alerts **0** (clean).
- **Catalyst layer is context-only — 73% unmapped this run (weak).** Top mapped catalysts are **stocks legal-risk** (SMCI export-control indictment 8-K; UNH DOJ probe −16%) — closed-market context only. One narrative basket: `momentum_breakout` primary **PARTI/USDT** (+18.5%, pure-momentum, no confirmed news, `wait_pullback`).
- **Europe → pre-US setup:** thin Sunday book; crypto is the only live expression of weekend headlines. **Key levels: BTC $60K handle / ~$59.1K June-5 low (Kalshi ~80% odds of sub-$60K close in 2026); ETH ~$1,540 shelf.** No-chase both directions — the desk's own edge says *don't fight the short tape with weak-volume altcoin longs.*

---

## 2. Data Used

**Internal — crypto reports (mtime / freshness):**
- `data/reports/scalp/2026-06-07_00-19_scalp_report.md` — gen **03:19 EEST, ~8.4h** (borderline; regime read corroborated externally, used for structure). Regime bearish risk-off; breadth EMA20 15%; **No A-tier, No B-tier**; best watchlist LTC 61.4.
- `data/reports/intraday/2026-06-07_01-00_intraday_report.md` — gen **04:00 EEST, ~7.7h**. Same regime; breadth 15%; **No A-tier, No B-tier**; best watchlist LTC 59.5.
- `data/reports/swing/2026-06-06_14-46_swing_report.md` — gen 17:46 EEST 06-06, **~18.0h STALE** (>14h band; excluded from final swing verdict except as direction context — see §3).
- Stocks reports (intraday/swing/invest all 06-05, ~36–42h) — **weekend, closed → context only.**

**Catalyst / narrative:** `data/catalysts/2026-06-07/` — `catalyst_events.jsonl` (**601 rows**, fresh 11:04), `narrative_baskets.jsonl` (**1 basket**), latest cycle `catalyst_cycle_08-04.md` (scanned 151 rows). Day-cumulative mapped **162 / 601 (27.0%)**, unmapped **439 / 601 (73.0%)** → **weak (§5).**

**LLM packets:** `data/processed/llm_analysis_packet.md` (crypto), `data/processed/llm_stocks_packet.md` (closed-market context).

**CLI / DB (read-only, this run):**
- `active-signals` crypto = **5** (NEAR/ADA intraday short realized; C scalp long expired; ZEC swing long contradicted; XLM swing long manage-only). `active-signals` stocks = **50** (mostly B-tier index/single-name intraday SHORTS — QQQ/SPY/XLK/MSFT/AMD/MELI etc.; Friday-dated, weekend-frozen → management/planning context only).
- `signal-stats` crypto week — headline A/B **n=69, triggered=52, 12W/20L, winrate 23.1%, PF 1.45, avgR 0.17, totalR +9.0**; by-direction longs **−5R (PF 0.58, 4W/12L)** vs shorts **+14R (PF 2.75, 8W/8L)**; by-mode swing **+11R (PF 12.0)**, intraday **+4R (PF 1.33)**, scalp **−6R (PF 0.14, 1W/7L)**; exchange-confirmed cross-exchange **+10R (PF 2.11)** vs Binance-only **−3R (PF 0.57)**.
- `detect_untracked_legacy_alerts --since 2026-06-07` → **None (0)** — clean.

**External (cited §13):** BTC $62,437 (June 4, CoinDesk, verified) → ~$59,100 (June 5); ETH $1,619 (June 4) → ~$1,565 internal; record 13-session BTC-ETF outflow streak ~$4.3–4.4B / 59.3K BTC; 17-day ETH-ETF outflow streak; $1.5B 24h liquidations (BTC $800M / ETH $386M); MSTR BTC sale; Fed "higher-for-longer" repricing post-jobs; Kalshi ~80% sub-$60K-in-2026.

**Unavailable / blind:** live tick beyond cited June 4–5 prints + internal June-7 freshness; TradingView/Chrome chart verification (not loaded); liquidation heatmaps / order-book / CVD; live social/KOL feeds; the in-progress 11:08 scheduler cycle's not-yet-emitted reports.

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-07_default_schedule/`.
- `scheduler.log` mtime **~11:09 EEST (~0.6h)**. **A fresh cycle booted 11:08** (CYCLE 1/12, weekend/crypto-only) and is **mid-run** — `track-signals` completed, `crypto scalp report` started at 11:09; **no new cycle summary `.md` emitted yet** this folder. Freshness rule: scheduler.log < 3h → **NO DEFER.** (Both-stale defer condition not met — scheduler is actively running.)
- The latest *completed* scalp (03:19) / intraday (04:00) reports are ~7.7–8.4h old (prior-cycle), borderline by the report-freshness bands, but the regime read ("bearish risk-off, no A/B") is stable across the last 3 cycles and corroborated by external June 4–5 prints, so it is used for the regime/landscape read. A genuinely fresher scalp/intraday will land within minutes as the 11:08 cycle completes.
- Freshness labels: scalp **borderline (~8.4h)**, intraday **borderline (~7.7h)**, swing **STALE (~18h, excluded from final swing verdict)**. Stocks **stale/closed → context only.**

---

## 4. What Changed vs Previous Review (Asia 04:39 Sun → Europe 11:43 Sun)

- **Regime unchanged — still bearish risk-off, still zero A/B in any crypto mode.** The descent thesis from 04:39 is fully intact ~7h later; no reversal through the Asia and into the Europe session.
- **Same scalp/intraday reports consumed.** The 04:39 review read the 03:19 scalp + 04:00 intraday as "fresh"; at 11:43 those same files are now ~8h old (borderline). **No new full report cycle has completed since 04:39** — the 11:08 cycle is still running. The 04:39 review noted the scalp-staleness regression looked *resolved*; this run shows scalp/intraday have **not** regenerated in the ~7h gap, i.e. the default cadence left a long report gap overnight-into-morning (see §14 TODO, downgraded — likely weekend cadence rather than a bug).
- **Prices: marginally lower / same band.** External now anchors BTC $62,437 (June 4) → sub-$60K June 5; the 04:39 review cited BTC ~$60,880 (June 6) / ETH ~$1,559. Same $59–62K BTC / $1,540–1,620 ETH zone. **No reversal; ETF-outflow streak extended to a record 13 sessions / ~$4.3–4.4B.**
- **Active book identical:** same 5 signals, same states (NEAR/ADA/C realized-or-expired; ZEC contradicted/dead; XLM manage-only). Untracked legacy alerts still **0**.
- **Signal-stats stable** (n=69, PF 1.45, +9R; shorts PF 2.75 vs longs PF 0.58; intraday +4R; scalp −6R). **Note:** the 04:39 review's by-mode *labels* (scalp +11R / intraday −6R) are **swapped relative to today's CLI** (swing +11R / scalp −6R) — same R triplet, different mode names. Logged as low TODO to verify which mapping is canonical (§14).
- **Catalyst day-cumulative grew:** 252 events (04:39) → **601 events (11:43)** as the day's cycles accumulated; unmapped 68.7% → **73.0%** (still weak); baskets 4 → **1** (`momentum_breakout`/PARTI carried; the AI/perps/delisting baskets from overnight did not re-trigger this cycle).
- **Legal flags carried (stocks, closed):** SMCI (export-control indictment, SEC 8-K) and UNH (DOJ antitrust/fraud probe, −16%) still top the catalyst legal-risk list — context only this slot.

---

## 5. Catalyst Coverage

- Total `catalyst_events` today (06-07, day-cumulative): **601**
- Mapped (non-null symbol): **162 (27.0%)**
- Unmapped (null symbol): **439 (73.0%)**
- `narrative_baskets`: **1** (`momentum_breakout`, primary PARTI/USDT, `wait_pullback`, single_source, fresh <1h)
- **⚠ CATALYST MAPPING WEAK THIS RUN (73% unmapped > 50%) — use the catalyst layer as context, NOT a final decision input.** This has now been >50% unmapped for multiple consecutive runs (67.1% → 68.7% → 73.0%) → recurring; see §14 TODO.
- Top 3 unmapped (null-symbol) high-importance headlines (from `catalyst_cycle_08-04`):
  1. `0.68` US Supreme Court backs FCC and SEC in key regulatory rulings that reshape enforcement landscape (CryptoBriefing) — sector/regulatory, no symbol.
  2. `0.62` Why is the crypto market down today? ETF outflows, $1.3B liquidations, and more (AMBCrypto) — market-wide, no symbol.
  3. `0.51` Partners Group halts withdrawals on $9B fund amid investor doubts (CryptoBriefing) — TradFi, no symbol.
- Latest cycle (`cycle_08-04`) by type: other_news 142, legal_risk 5, partnership 2, analyst_action 1, regulatory_sector_headline 1.

---

## 6. Market Landscape

- **Regime: bearish trend / risk-off across both crypto and equities.** Crypto: BTC downtrend, ETH downtrend, breadth above EMA20 only 15%, BTC ATR percentile 80–81 (elevated vol). Equities: the 50 active stock signals are overwhelmingly **index + single-name SHORTS** (QQQ/SPY/XLK/MSFT/AMD/MELI), i.e. the system read US equities risk-off into Friday's close — consistent with the crypto tape.
- **Macro driver (external, §13):** record BTC-ETF outflow streak (13 sessions, ~$4.3–4.4B), 17-day ETH-ETF outflow streak, MSTR BTC sale, Fed "higher-for-longer" repricing after a strong jobs print, capital rotating into gold + AI equities, lingering US–Iran/Hezbollah geopolitics. $1.5B+ single-day liquidations (longs ~$1.35B).
- **Internal macro gauge:** risk 57/100, BTC bias neutral/data-watch; macro headlines flag the ETF outflows, MSTR sale, and Hyperliquid UK regulatory warning.
- **Relative strength pockets (counter-tape, low conviction):** PARTI/USDT +18.5% (momentum basket, no news), PORTAL/USDT +16–20%. Both flagged by the desk as *RS-leader longs against a bearish tape — reduce size, demand confirmation, do not chase.* XLM/TON also RS-positive but rejected (counter-trend caps).
- **Bottom line:** the live, profitable expression of this tape per the desk's own stats is the **short side** (shorts +14R PF 2.75); longs are bleeding (−5R PF 0.58). But with no fresh A/B short triggered and prices already extended down, the disciplined read is **no new chase** — wait for the 11:08 cycle's fresh reports or a clean retest.

---

## 7. Candidate Deep Dives (≤5)

### 7.1 ZEC/USDT — swing LONG (active, B) → **AVOID / DEAD**
- **State:** active swing long, in-window, but **contradicted.** Entry ~$555 region; current price ~$362 (scalp desk note 361.91). Price sits **~35% below the long's invalidation (~$555)** — the long is a defunct artifact from before the Orchard-counterfeiting-bug crash (ZEC −31.5% 7d, −7.1% 24h).
- **Catalyst (internal + prior-verified):** Zcash counterfeiting/Orchard bug surfaced via an AI audit (cited in prior 04:39 review, patched ~June 2); ZEC −38–50% on the news. Researcher has since added Monero to the audit queue (XMR −10%).
- **Price-reaction / chase check:** move fully reacted weeks ago; structure is `range` (setup quality 47.8/100), the worst technical of the watchlist. Not a chase candidate in either direction here.
- **LEGAL/HEADLINE RISK:** none new; protocol-integrity discount stands.
- **Verdict: AVOID. Manage/close the stale long; do not add. Not actionable.**

### 7.2 XLM/USDT — swing LONG (active, B) → **MANAGE-ONLY / NO-ADD**
- **State:** active swing long, in-window (to ~06-07T22:36). Scalp report shows XLM +4.3% 24h, RS vs BTC +5.0% — a counter-tape RS-leader, but **rejected at scalp/intraday level** ("RS-leader long vs weak BTC tape — reduce size; volume below average; breakout confirmation weak").
- **Price-reaction / chase check:** RS-positive but on **weak volume** against a bearish tape — exactly the long profile the desk's stats punish (longs −5R PF 0.58). Overextension not flagged, but confirmation is absent.
- **Verdict: MANAGE-ONLY. Hold existing per its own plan; NO new adds. Counter-trend long against a tape where shorts carry the edge.**

### 7.3 NEAR/USDT — intraday SHORT (active, B; realized) → **REALIZED / NO RE-ENTRY HERE**
- **State:** intraday short, `tp2_hit` then expired (worked — aligned with the winning short/bear-tape direction). Now also reappears as a top crypto watchlist *short-bias* name (scalp watchlist #2, score 60.7; intraday #4, 57.7), trend downtrend, RS vs BTC −4.9%.
- **Price-reaction / chase check:** the realized leg already captured the down-move; current watchlist entry is a *conditional failed-bounce/retest* short (~1.881–1.900), **not active** (score < threshold). Volume thin (0.09–0.44x). Entry NOW would be mid-range, not at the retest — **late/no-edge.**
- **Verdict: NO new entry at market. If it tags the conditional retest zone (~1.88–1.90) on a failed bounce with volume, a fresh short aligns with the tape — but it is not triggered. Watchlist.**

### 7.4 ADA/USDT — intraday SHORT (active, B; realized) → **REALIZED / WATCHLIST**
- **State:** intraday short, realized/expired. Watchlist #10 intraday (56.4), downtrend, 7d −33.5% (deeply broken), fresh attention via 1 news item ("Can Cardano's fundamentals still stage a comeback?" — a *weakness* framing, confirms short bias).
- **Price-reaction / chase check:** already −33% over 7d — heavily extended down; conditional retest short ~0.1578–0.1588 is **not active**. Chasing a coin this broken at mid-range = poor RR.
- **Verdict: WATCHLIST. Realized short banked; no fresh actionable. Only a clean retest short qualifies and it is not triggered.**

### 7.5 PARTI/USDT — momentum_breakout basket primary → **NO-CHASE / WAIT-PULLBACK**
- **State:** basket primary, +18.5% 24h, RS vs BTC +19.3%, the single strongest momentum name. **No confirmed news catalyst** (pure-momentum cluster, single_source, `wait_pullback`). Scalp score 59.9 / intraday 57.1 — **watchlist, below active threshold.**
- **Price-reaction / chase check:** big move **already happened** (+18.5%/+32% 7d); the desk plan is an explicit *conditional pullback* long zone (~0.0567–0.0577) with size reduction — i.e. **do not chase the spike.** Counter-tape long against a bear regime; volume 0.97x (not exceptional). Entry NOW (top of range ~0.0582) would be chasing.
- **LEGAL/HEADLINE RISK:** none found; but **no news catalyst at all** means the move is unexplained/fragile.
- **Verdict: NO-CHASE. If it pulls back into ~0.057 and holds with volume, a reduced-size momentum long is the *only* long the desk tolerates here — but it is counter-tape and unconfirmed. Watchlist / wait-pullback.**

---

## 8. Best Candidates Ranked

**No clean candidates.** No A-tier or B-tier setup triggered in any crypto mode; every name above is watchlist, realized, contradicted, or manage-only. The only directional *edge* in the data is generic short-side bias (stats: shorts +14R PF 2.75), but **no fresh A/B short is triggered**, so there is nothing to action at market.

Ordered by "closest to becoming actionable":
1. **NEAR/USDT short** — would qualify on a failed-bounce retest into ~1.88–1.90 with volume (tape-aligned).
2. **PARTI/USDT long (reduced size)** — only on a pullback into ~0.057 holding with volume (counter-tape, unconfirmed — lowest trust).
3. ADA/USDT short — watchlist, needs a clean retest; deeply extended.

---

## 9. Avoid / No Trade

- **ZEC/USDT long — AVOID/DEAD.** Price ~35% below invalidation; defunct post-bug artifact.
- **XLM/USDT long — NO-ADD.** Counter-tape RS long on weak volume; desk edge favors shorts.
- **PARTI/PORTAL longs at market — NO-CHASE.** Already extended +16–20%; chasing into a bear tape is the losing-long profile (−5R PF 0.58).
- **Any weak-volume altcoin long** — explicitly what the regime engine says to avoid.
- **Stocks (SMCI, UNH, QQQ/SPY/XLK shorts, all 50 signals) — NO ACTION.** Market closed (Sunday). Planning/management context only.
  - **SMCI — LEGAL/HEADLINE RISK:** SEC 8-K (FY2026) — indictment of three individuals re alleged export-control-violation conspiracy. AVOID clean longs when equities reopen until clarified.
  - **UNH — LEGAL/HEADLINE RISK:** DOJ antitrust + fraud probe; shares −16%. AVOID clean longs; headline-driven.

---

## 10. Main Risks

- **Report latency:** the actionable scalp/intraday reports are ~8h old; the 11:08 cycle's fresher reports were not yet emitted at review time. The regime read is corroborated externally, but micro levels (entry/ATR) may have drifted. **Re-check the fresh report when the 11:08 cycle completes before any execution.**
- **Catalyst layer unreliable (73% unmapped, recurring)** — do not let it drive decisions this run.
- **Counter-tape long temptation:** PARTI/PORTAL RS-leaders look attractive but are the exact profile the desk's own stats punish. Size discipline / no-chase is the risk control.
- **Downside continuation:** record ETF-outflow streak + MSTR selling + Fed repricing are not exhausted; a BTC break of ~$59.1K (June-5 low) opens lower (Kalshi ~80% sub-$60K-in-2026). Manage any residual longs (ZEC/XLM) tightly.
- **Blind spots:** no live tick, no chart MCP, no liquidation/order-book/CVD/social feeds (all noted unavailable — not fabricated).
- **Ingest:** 5 external sources ingested cleanly into `news_items` (crypto) — no error.

---

## 11. Action Plan — next 4 hours

1. **Crypto: stand down / no new entries.** No A/B triggered; bearish risk-off. Do not chase extended names in either direction.
2. **When the 11:08 cycle's fresh scalp/intraday lands,** re-scan for any newly-triggered A/B short — that is the only tape-aligned actionable. Until then, no execution off ~8h-old levels.
3. **Manage residual longs:** ZEC long = close/stand-down (dead); XLM long = hold-to-plan, no adds.
4. **Watch triggers (not active):** NEAR failed-bounce short ~1.88–1.90 w/ volume; PARTI pullback-long ~0.057 (reduced size, lowest trust); BTC $59.1K break = downside confirmation.
5. **Stocks:** no action (closed). Carry SMCI/UNH legal-risk flags into the pre-US/US-open slots when equities reopen.
6. **Pre-US slot (16:20):** re-evaluate with a fresh cycle + any weekend-gap repricing.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** **NO TRADE / WATCHLIST.** No A/B; bearish risk-off; best watchlist LTC 61.4 (below threshold). Stand down.
- **Crypto intraday:** **NO TRADE / WATCHLIST.** No A/B; realized NEAR/ADA shorts banked; no fresh trigger. Tape-aligned shorts only on a clean retest.
- **Crypto swing:** **MANAGE-ONLY.** Swing report stale (~18h, excluded). ZEC long = AVOID/dead; XLM long = hold-to-plan/no-add.
- **Stocks (all modes):** **NO ACTION — market closed (Sunday).** Risk-off short book frozen; SMCI/UNH legal-risk flagged for reopen.

---

## 13. Sources

- [CoinDesk — Bitcoin briefly drops below $62,000 as $1.5B in crypto longs get wiped out (June 4, 2026)](https://www.coindesk.com/markets/2026/06/04/bitcoin-drops-below-usd62-000-as-usd1-5-billion-in-crypto-longs-get-wiped-out) — **WebFetch verified HTTP 200**; BTC $62,437.70, ETH $1,619.66, $1.5B 24h liquidations (BTC $800M / ETH $386M), ~$1B weekly ETF outflows. _single_source._
- [Invezz — Bitcoin slid below $60,000: why is the crypto market crashing? (June 5, 2026)](https://invezz.com/news/2026/06/05/bitcoin-slid-below-60000-why-is-the-crypto-market-crashing/) — BTC sub-$60K / ~$59,100; MSTR sale; 13-session ETF outflow streak; Fed repricing; US–Iran. _single_source (fetch 403, WebSearch summary)._
- [BeInCrypto — Bitcoin ETF Outflows Hit 13-Day Streak as $4.3B Exits the Funds (June 2026)](https://beincrypto.com/bitcoin-etf-outflows-record-streak-june-2026/) — record 13-day BTC-ETF outflow streak ~$4.33B / 59,351 BTC; 17-day ETH-ETF outflow streak. _single_source._
- [CryptoBriefing — Bitcoin falls below $64,000, triggers $1.1B in liquidations (June 3, 2026)](https://cryptobriefing.com/bitcoin-falls-below-64000-triggers-11b-in-liquidations/) — earlier-week leg; $1.1B liquidations. _single_source._
- [CNBC — Bitcoin set to slump to new lows for 2026 after recent sell-off, traders forecast (June 3, 2026)](https://www.cnbc.com/2026/06/03/bitcoin-to-slump-to-new-lows-after-recent-sell-off-traders-predict.html) — trader forecasts of new 2026 lows. _single_source._

_Source-discipline (§N): every external claim above carries source + title + date + URL; no uncited stats; no fabricated chart observations (chart MCP not loaded — declared); no test_source/fixture URLs (ingest rejected 0); §13 present; external research was AVAILABLE this run._

---

## 14. Fix Requests / TODO

### TODO-catalyst-mapping-weak (recurring)
- **issue:** Catalyst symbol-mapping has been <50% for ≥3 consecutive runs (unmapped 67.1% → 68.7% → **73.0%** today), forcing the catalyst layer to "context-only" every slot.
- **evidence:** `data/catalysts/2026-06-07/catalyst_events.jsonl` 162/601 mapped (27.0%); `catalyst_cycle_08-04.md` other_news=142 of 151. Top unmapped are market-wide/regulatory/TradFi headlines with no resolvable ticker.
- **suggested manual fix:** improve the symbol resolver in the catalyst layer — add market-wide/sector tagging (e.g. map "crypto market down / ETF outflows" → BTC+ETH basket) so macro headlines stop counting as fully unmapped; or split the metric into "macro/no-symbol-expected" vs "should-have-mapped-but-didn't."
- **priority:** medium
- **first observed:** 2026-06-06 (carried); reconfirmed 2026-06-07 11:43 EEST

### TODO-report-cadence-gap
- **issue:** No new scalp/intraday report was emitted between the 04:00 intraday and the 11:08 cycle boot (~7h gap) on a weekend; the actionable reports were ~8h old at this slot. The 04:39 review had flagged scalp-staleness as "resolved" — this run shows a long report gap reappeared (likely weekend cadence rather than the prior bug, but worth confirming).
- **evidence:** latest scalp 2026-06-07_00-19 (03:19), latest intraday 2026-06-07_01-00 (04:00); `scheduler.log` shows next cycle boot 11:08 — ~7h with no report regeneration.
- **suggested manual fix:** confirm whether weekend/crypto-only mode intentionally widens the report interval; if not, investigate why the overnight cycles between ~04:00 and 11:08 did not emit scalp/intraday reports.
- **priority:** low
- **first observed:** 2026-06-07 11:43 EEST

### TODO-signal-stats-mode-label-consistency
- **issue:** The 04:39 review's by-mode performance labels (scalp +11R/PF12, intraday −6R/PF0.14) are **swapped** relative to today's `signal-stats` CLI (swing +11R/PF12, intraday +4R/PF1.33, scalp −6R/PF0.14). Identical R triplet, different mode names — either a prior-review transcription error or a non-deterministic mode-label mapping in the CLI.
- **evidence:** today `python -m src.cli signal-stats --asset-class crypto` By-mode: scalp n=40 PF0.1429 totalR−6, swing n=6 PF12 totalR+11, intraday n=23 PF1.3333 totalR+4. Prior `OPUS_ENRICHED_REVIEW_AUTO_2026-06-07_0439.md` §1/§2 attributes +11R to scalp and −6R to intraday.
- **suggested manual fix:** verify the CLI's mode grouping is stable across runs and that prior reviews transcribed it correctly; if the CLI mapping is stable, treat today's (scalp worst) as canonical and disregard the 04:39 labeling.
- **priority:** low
- **first observed:** 2026-06-07 11:43 EEST
