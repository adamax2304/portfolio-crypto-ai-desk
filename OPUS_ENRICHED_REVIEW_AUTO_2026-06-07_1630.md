# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:30 EEST

- **Generated:** 2026-06-07 16:30 EEST (auto-enriched-review, scheduled task `opus-enriched-review-preus`, **pre-US-open decision review** slot 16:20, executing `opus-enriched-review-4h/SKILL.md`).
- **⚠ It is SUNDAY — US & EU cash equities are CLOSED.** There is **no US cash open today**; the next US open is **Monday 2026-06-08**. This slot's "pre-US-open" read therefore = **into-the-Monday-open + weekend→Monday gap risk**. **Crypto is the only live, actionable class.**
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-07_1143.md` (Europe / pre-US context, 11:43 EEST, ~4.8h ago — see §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). **WebFetch verified HTTP 200 on coinpaper (June 5): BTC ~$62,116, support $60K / $58–55K, BTC at 200-week MA first time since 2023.** Live Binance public ticker (this run, ~16:30): **BTC $61,844 (+1.57% 24h), ETH $1,622 (+3.71% 24h).**
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; structure = local OHLCV/ATR/EMA report fields + cited external prints.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

- **First sign of stabilization after a brutal week — but still NO fresh A/B in any crypto mode.** Live tape this run is modestly **green**: BTC **$61,844 (+1.6% 24h)** defending the $60K handle at its **200-week MA (first test since 2023)**; ETH **$1,622 (+3.7% 24h)** leading the bounce. The fresh 15:15 scalp and 15:48 intraday reports both still print regime **"transition (mixed)" — selective only, demand clean invalidation; zero A-tier, zero B-tier.** This is a *basing/relief* read, not a confirmed reversal — the desk does not yet see a clean setup either way.
- **Two genuinely new positives vs the 11:43 bearish read (§4):** (1) the record **13-day spot-BTC-ETF outflow streak ENDED June 5** with a small **+$3.05M net inflow** (first June inflow); (2) a **Trump "no reason to raise rates" Fed headline** (13:12 EEST, single_source) — mild risk-on tone vs the prior "higher-for-longer" repricing. Neither is a green light; both lift the floor slightly.
- **Active book = all winners banked, two swings expiring tonight — clean, nothing to chase.** The 5 active crypto signals are mature **runners already in profit**: NEAR & ADA intraday SHORTS (`tp2_hit`), C scalp LONG (`tp1_hit`), and **ZEC & XLM swing LONGS (`tp2_hit` / `tp1_hit`) that EXPIRE TONIGHT ~22:5x EEST** → realized; let expire / close runner, **no re-entry, no adds.** No fresh actionable in any mode.
- **Signal-stats (feedback-only, n=69, week):** A/B PF **1.45**, **+9R**, winrate 23.1%. By-mode: **swing +11R (PF 12.0), intraday +4R (PF 1.33), scalp worst −6R (PF 0.14, 1W/7L).** The week's edge was the **short side into the down-move** — but with the tape now bouncing and no fresh A/B short triggered, that edge is *not* actionable at market here. Untracked legacy alerts **0** (clean).
- **Catalyst layer is context-only — 75.3% unmapped this run (weak, recurring).** One narrative basket: `momentum_breakout` (primary **FIDA/JTO/BANK**, playbook **`avoid_chase`**, FIDA flagged overextended at +75% 24h). Top mapped catalysts remain **stocks legal-risk** (SMCI export-control indictment 8-K; UNH DOJ probe −16%) — closed-market context only.
- **Pre-Monday-open posture:** crypto **stand-down / no-chase both directions.** The only thing that matters into Monday is whether **BTC holds $60K / the 200-week MA** (basing → potential first long-side A/B if a clean retest triggers) **or loses $59.1K** (June-5 low → downside re-opens). Manage the two expiring swing longs; do not initiate on ~bouncing-but-unconfirmed price.

---

## 2. Data Used

**Internal — crypto reports (mtime / freshness):**
- `data/reports/scalp/2026-06-07_12-15_scalp_report.md` — gen **15:15 EEST, ~1.3h → FRESH.** Regime transition (mixed); breadth EMA20 39.0%; BTC ATR pct 73; **No A-tier, No B-tier**; best watchlist BANK 60.6.
- `data/reports/intraday/2026-06-07_12-48_intraday_report.md` — gen **15:48 EEST, ~0.7h → FRESH.** Same regime; breadth 39.0%; **No A-tier, No B-tier**; best watchlist BANK 59.1.
- `data/reports/swing/2026-06-06_14-46_swing_report.md` — gen 17:46 EEST 06-06, **~22.8h STALE** (>14h band; excluded from final swing verdict except as direction context — see §3).
- Stocks reports (intraday/swing/invest all 06-05, ~45–49h) — **weekend, closed → context only.**

**Catalyst / narrative:** `data/catalysts/2026-06-07/` — `catalyst_events.jsonl` (**958 rows**, fresh 15:48), `narrative_baskets.jsonl` (**1 basket**, `momentum_breakout`), latest cycle `catalyst_cycle_12-48.md` (scanned 202 rows). Day-cumulative mapped **237 / 958 (24.7%)**, unmapped **721 / 958 (75.3%)** → **weak (§5).**

**LLM packets:** `data/processed/llm_analysis_packet.md` (crypto), `data/processed/llm_stocks_packet.md` (closed-market context).

**Scheduler:** latest folder `data/scheduled_runs/2026-06-07_default_schedule/`; `scheduler.log` mtime **15:51 (~0.6h)**; latest cycle summary `cycle_02_14-36_summary.md` mtime **15:51 (~0.6h)** — **NO DEFER.** Cycle 2 (14:36→15:51, weekend/crypto-only) completed **11/11 steps OK, 0 failed.**

**CLI / DB (read-only, this run):**
- `active-signals` crypto = **5** (NEAR/ADA intraday short `tp2_hit`; C scalp long `tp1_hit`; ZEC swing long `tp2_hit`; XLM swing long `tp1_hit` — all realized; ZEC & XLM expire tonight). `active-signals` stocks ≈ **264** (Friday-dated, weekend-frozen — predominantly index/mega-cap intraday SHORTS QQQ/SPY/XLK/MSFT/AMZN/META at B-tier already tp1/tp2_hit; plus a few C/A names incl. **LLY invest LONG A-tier `waiting_for_entry`** — management/planning context only).
- `signal-stats` crypto week — headline A/B **n=69, triggered=52, 12W/20L, winrate 23.1%, PF 1.45, avgR 0.17, totalR +9.0**; by-mode **scalp −6R (PF 0.14, 1W/7L)**, **swing +11R (PF 12.0)**, **intraday +4R (PF 1.33)**; by-setup top n=36 PF 2.75 (+14R).
- `detect_untracked_legacy_alerts` (cycle step 8) → **None (0)** — clean.

**External (cited §13):** live BTC $61,844 (+1.6%) / ETH $1,622 (+3.7%) (Binance public ticker, this run); BTC ~$62,116 June-5 (coinpaper, HTTP 200 verified), at 200-week MA first since 2023, support $60K/$58–55K; BTC opened $63,812 → $62,046 Friday June-5, low $59,227 overnight (Yahoo); 13-day BTC-ETF outflow streak ~$4.33B / 59.4K BTC **ended June 5 with +$3.05M inflow** (bitcoinfoundation/beincrypto); AUM $104.3B→$80.4B over the streak.

**Unavailable / blind:** intraday tick beyond the single live ticker snapshot; TradingView/Chrome chart verification (not loaded); liquidation heatmaps / order-book / CVD; live social/KOL feeds (lookonchain rows this run are bot welcome-spam, no symbols).

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-07_default_schedule/`.
- `scheduler.log` mtime **15:51 EEST (~0.6h)**; latest cycle summary `cycle_02_14-36_summary.md` mtime **15:51 (~0.6h)**. Both << 3h → **NO DEFER** (both-stale defer condition not met).
- **This is a fresh-data slot** (unlike the 04:39/11:43 runs which ran on ~8h-old reports): the 14:36 cycle completed at 15:51 and emitted a brand-new scalp (15:15) + intraday (15:48). Regime/landscape read is on **current** data.
- Freshness labels: scalp **FRESH (~1.3h)**, intraday **FRESH (~0.7h)**, swing **STALE (~22.8h, excluded from final swing verdict)**. Stocks **stale/closed → context only.**

---

## 4. What Changed vs Previous Review (Europe 11:43 Sun → pre-US-open 16:30 Sun)

- **Tape flipped from "descending/bearish" to "basing/modestly green."** 11:43 read BTC sub-$60K/~$59.1K and "no reversal, grind lower." This run: **BTC $61,844 (+1.6% 24h), ETH $1,622 (+3.7% 24h)** — a relief bounce off the $59–60K floor, ETH leading. **Regime label upgraded from "bearish risk-off" (on 8h-old reports at 11:43) to "transition (mixed)" on FRESH 15:15/15:48 reports; breadth EMA20 15% → 39.0%.** Still **no A/B** either run.
- **ETF-outflow narrative inflected POSITIVE.** 11:43 had the record 13-day / ~$4.3–4.4B outflow streak as ongoing. This run confirms (external) the **streak ENDED June 5 with a +$3.05M net inflow** — the first June inflow. Stabilization signal, not reversal.
- **New macro headline:** **Trump "there's no reason to raise interest rates"** (13:12, t.me/WalterBloomberg, single_source) — mild dovish/risk-on counter to the prior "higher-for-longer" repricing. Context only.
- **Reports now FRESH (was the prior run's biggest caveat).** 11:43 flagged ~8h-old actionable reports + a report-cadence gap. This run consumes <1.5h-old scalp/intraday — the latency caveat is resolved for this slot.
- **Active book unchanged in composition, clearer in framing.** Same 5 signals. **Reframe of ZEC:** prior review called the ZEC long "AVOID/DEAD." DB confirms ZEC swing long is `tp2_hit` (entry $561–567, tp1 $582, tp2 $594 already banked historically) — i.e. a **realized winner** now pulled back to ~$412; the position's gains are captured. It **expires tonight ~22:56**; XLM (`tp1_hit`, entry $0.254, tp1 $0.270 banked) expires ~22:36. Both = realized, let-expire/close-runner, no adds. Untracked legacy alerts still **0**.
- **Catalyst day-cumulative grew** 601 (11:43) → **958** events; unmapped 73.0% → **75.3%** (still weak); baskets 1 → **1** but **primary rotated PARTI → FIDA/JTO/BANK** and **playbook hardened `wait_pullback` → `avoid_chase`** (top gainers now overextended).
- **Signal-stats stable** (n=69, PF 1.45, +9R; scalp −6R / swing +11R / intraday +4R) — identical triplet to 11:43; mode-label ordering matches the canonical CLI (scalp worst).

---

## 5. Catalyst Coverage

- Total `catalyst_events` today (06-07, day-cumulative): **958**
- Mapped (non-null symbol): **237 (24.7%)**
- Unmapped (null symbol): **721 (75.3%)**
- `narrative_baskets`: **1** (`momentum_breakout`, primary **FIDA/JTO/BANK**, playbook **`avoid_chase`**, single_source, fresh <1h; FIDA flagged overextended).
- **⚠ CATALYST MAPPING WEAK THIS RUN (75.3% unmapped > 50%) — use the catalyst layer as context, NOT a final decision input.** Now >50% unmapped for ≥4 consecutive runs (67.1% → 68.7% → 73.0% → **75.3%**) → recurring; see §14 TODO.
- Top 3 unmapped / null-symbol high-importance headlines this run:
  1. `1.82` **TRUMP ON FED: THERE'S NO REASON TO RAISE INTEREST RATES** (t.me/WalterBloomberg) — macro/rates, no ticker (basket-level risk-on).
  2. `1.80` Pump.fun Bounty Backfires After Man Inks Misspelled Meme Coin on Forehead (BeInCrypto) — sector color, no resolvable ticker.
  3. `0.53` Microsoft unveils IQ platform and hosted agents at Build 2026 (CryptoBriefing) — TradFi/AI, no crypto ticker.
- Latest cycle (`cycle_12-48`) by type: other_news 196, legal_risk 4, product_launch 1, analyst_action 1.

---

## 6. Market Landscape

- **Regime: transition (mixed) / basing after the weekly washout.** Crypto: BTC range (defending $60K at the 200-week MA), ETH downtrend on the report but **+3.7% live today** (RS leader of the bounce), breadth above EMA20 **39.0%** (up from 15% at 11:43), BTC ATR pct 73 (still elevated but off the 80–81 highs). The fresh reports demand **"selective only; clean invalidation"** — no clean trend to lean on either way.
- **Macro drivers (external, §13):** the bearish stack is **easing at the margin** — ETF-outflow streak broke June 5 (+$3.05M), a dovish Trump-on-Fed headline, ETH bid +3.7%. Still-unresolved overhangs: AUM down to $80.4B (from $104.3B), capital rotation into AI equities/gold, BCH/AVGO-led equity weakness into Friday, lingering geopolitics. Net: **floor lifting, ceiling intact.**
- **Where money flows (internal):** top momentum is the `momentum_breakout` cluster — **FIDA +63–75%**, **JTO +26% (vol 1.8x, the only real-volume name)**, EDEN +34%, BANK +12% — but all are **single_source / no confirmed news**, the basket playbook is **`avoid_chase`**, and FIDA is explicitly overextended. ETH/SOL/BTC carry only the (single_source) James-Wynn long-flip on-chain note.
- **Stocks (frozen, closed):** 264 weekend-frozen signals, overwhelmingly index + mega-cap **SHORTS** (QQQ/SPY/XLK/MSFT/AMZN/META, mostly already tp1/tp2_hit) = the system's risk-off read into Friday's close. One **A-tier LLY invest LONG (`waiting_for_entry`)** is the standout for the Monday reopen (defensive-pharma bid). SMCI / UNH legal-risk flags persist.
- **Bottom line:** the down-move's short edge has largely played out (shorts banked, tape bouncing); the long side is not yet confirmed (no A/B, breakout/volume weak, regime mixed). **The disciplined read into Monday is no-chase both ways — let BTC prove $60K acceptance or rejection first.**

---

## 7. Candidate Deep Dives (≤5)

### 7.1 BTC/USDT — macro anchor / $60K & 200-week-MA pivot → **NO TRADE (watch the level)**
- **State:** live $61,844 (+1.6% 24h), range/basing above the $60K handle. External: at its **200-week moving average for the first time since 2023** (coinpaper, HTTP 200) — a historically significant support shelf; support stack $60K → $58–55K, overhead resistance $70–74K (broken channel).
- **Price-reaction / chase check:** the down-leg already reacted (−14% MTD); the +1.6% bounce is a *relief* off the floor, not a breakout. No A/B trigger. Entry NOW = mid-no-man's-land between $59.1K support and far overhead resistance — no edge.
- **Catalyst:** ETF-outflow streak broke June 5 (+$3.05M, first June inflow); dovish Trump-on-Fed headline. Marginally supportive, unconfirmed.
- **Verdict: NO TRADE. The pivot, not a position.** Hold $60K / 200-wk MA with acceptance → first long-side A/B becomes plausible on a clean retest. Lose **$59.1K (June-5 low)** → downside re-opens. This level governs the whole book into Monday.

### 7.2 ETH/USDT — RS leader of the bounce → **NO TRADE / WATCH**
- **State:** live $1,622 (**+3.7% 24h**, outperforming BTC) — the strongest major today. Internal trend still "downtrend" on the report (~$1,565 freshness print) but the live bid is leading. Counter-context: **$168M ETH-ETF exodus / whale-absorption question** (AMBCrypto, single_source) + 17-day ETH-ETF outflow streak overhang.
- **Price-reaction / chase check:** +3.7% bounce off a deeply-sold base; no A/B trigger; the report still frames ETH as a downtrend laggard. Chasing the bounce mid-move into an active ETF-exodus overhang = poor RR.
- **Verdict: NO TRADE. Watch as the relative-strength tell** — if ETH leads and BTC holds $60K together, the basing thesis firms. Not actionable at market.

### 7.3 ZEC/USDT + XLM/USDT — swing LONGS expiring tonight → **REALIZED / LET-EXPIRE, NO ADDS**
- **State:** **ZEC** swing long `tp2_hit` (entry $561–567; tp1 $582 / tp2 $594 banked historically; now ~$412, +12.7% 24h bounce but far below the runner's tp3 $606), **expires ~22:56 EEST tonight.** **XLM** swing long `tp1_hit` (entry $0.254; tp1 $0.270 banked), **expires ~22:36 EEST tonight.**
- **Price-reaction / chase check:** both gains already captured; swing report is **STALE (~22.8h, excluded)** so no fresh swing structure to justify holding/adding past expiry. ZEC still carries the protocol-integrity (Orchard counterfeiting) discount from earlier in the week.
- **Verdict: REALIZED / MANAGE-ONLY.** Let both expire on schedule tonight (or close any residual runner into the bounce). **No new adds, no re-entry** — counter-tape longs on a stale report with the win banked.

### 7.4 momentum_breakout basket (FIDA / JTO / BANK) → **AVOID-CHASE / WAIT-PULLBACK**
- **State:** the single active narrative basket — **FIDA +63–75% 24h** (overextended, vol only 0.01–0.56x), **JTO +26%** (vol 1.8x — the *only* real-volume name, but flagged "do not chase, >2 ATR from EMA20"), BANK +12% (best watchlist, 60.6). All **single_source, no confirmed news**; playbook hardened to **`avoid_chase`**.
- **Price-reaction / chase check:** moves already happened; FIDA is the textbook overextended-spike-on-thin-volume profile; JTO explicitly rejected for being >2 ATR extended. Entry NOW = chasing.
- **Verdict: AVOID-CHASE.** BANK is the only name with a structured conditional pullback plan (zone ~0.0326–0.0345) but it's watchlist/below-threshold. No momentum long is tolerated at market here.

### 7.5 NEAR/USDT + ADA/USDT — intraday SHORTS (realized) → **REALIZED / NO RE-ENTRY**
- **State:** both `tp2_hit` from the June-5 down-move (banked, aligned with the winning short tape). Now reappear as downtrend watchlist names, but the tape is **bouncing** (+1.6% BTC / +3.7% ETH) — short re-entry fights the relief move.
- **Price-reaction / chase check:** the down-move that paid these shorts is the move now mean-reverting. Conditional retest shorts are **not active** (score < threshold) and would be counter to today's bid.
- **Verdict: REALIZED / NO RE-ENTRY.** Banked. Only a fresh, clean failed-bounce short trigger (BTC rejecting $60K back down) would re-qualify — not present.

---

## 8. Best Candidates Ranked

**No clean candidates.** No A-tier or B-tier setup triggered in any crypto mode; every name above is watchlist, realized, or avoid-chase. Ordered by "closest to becoming actionable into Monday":

1. **BTC/USDT long** — only on a *clean retest that holds* the $60K / 200-week-MA shelf with volume → would be the first tape-aligned long-side A/B; **not triggered.**
2. **ETH/USDT long** — the RS tell; needs BTC confirmation + a real trigger; **not triggered.**
3. **A fresh failed-bounce SHORT** (NEAR/ADA-style) — only if BTC *rejects* $60K back toward $59.1K; **not triggered.**

The directional bias remains short on the week's stats, but the live bounce neutralizes it intraday — **nothing to action at market.**

---

## 9. Avoid / No Trade

- **FIDA / JTO momentum at market — AVOID-CHASE.** +26–75% spikes, thin/over-extended, no confirmed news, basket playbook `avoid_chase`.
- **ZEC / XLM long adds — NO.** Wins banked; expiring tonight; stale swing report; no re-entry.
- **NEAR / ADA short re-entry at market — NO.** Fights today's relief bounce; not triggered.
- **Any weak-volume altcoin long chasing the bounce** — exactly the "selective only / clean invalidation" the fresh regime engine warns against.
- **Stocks (LLY, QQQ/SPY/XLK/MSFT shorts, all 264 signals) — NO ACTION.** Market closed (Sunday). Planning/management context only for the **Monday** open.
  - **SMCI — LEGAL/HEADLINE RISK:** SEC 8-K (FY2026) — indictment of three individuals re alleged export-control-violation conspiracy. AVOID clean longs at reopen until clarified.
  - **UNH — LEGAL/HEADLINE RISK:** DOJ antitrust + fraud probe; shares −16%. AVOID clean longs; headline-driven.
  - **LLY invest long (A-tier, waiting_for_entry)** — the one constructive stock setup for Monday; no legal flag found, but verify the entry trigger live when equities reopen (do not assume fill from a Friday-dated level).

---

## 10. Main Risks

- **Bounce-fade / false-dawn:** the +1.6%/+3.7% relief is off a deeply-sold base into a thin Sunday book; one June-5 inflow does not end a $4.3B outflow regime. A failure back under **$59.1K** re-opens downside (AUM still −23% from streak start). Do not treat the bounce as a confirmed bottom.
- **Weekend → Monday gap risk:** thin weekend liquidity + the Monday US-equity reopen (risk-off short book frozen Friday) can gap crypto either way at/after the Monday cash open. The book is flat/realized, so gap exposure is low — keep it that way; no new weekend initiations.
- **Catalyst layer unreliable (75.3% unmapped, recurring)** — do not let it drive decisions this run.
- **Stale swing report (~22.8h):** ZEC/XLM swing structure is not fresh; rely on the realized/expiry framing, not on stale swing levels.
- **Blind spots:** single live-ticker snapshot only (no continuous tick); no chart MCP, no liquidation/order-book/CVD/social feeds (all noted unavailable — not fabricated). lookonchain Telegram rows this run are bot welcome-spam (no signal).
- **Ingest:** sources for this run built into `data/raw/enriched_review_sources/2026-06-07_1630.json` and UPSERTed into `news_items` (crypto) — see §13 / §14.

---

## 11. Action Plan — next 4 hours (into the Monday US open)

1. **Crypto: stand down / no new entries.** No A/B triggered; regime mixed/basing. Do not chase the bounce or re-short into it.
2. **Watch the one level that matters — BTC $60K / 200-week MA:** clean *acceptance* (hold + retest with volume) → first long-side A/B becomes plausible; *rejection* back under **$59.1K** → downside re-opens and a fresh failed-bounce short re-qualifies. ETH leading (+3.7%) is the confirming tell.
3. **Manage the two expiring swing longs:** ZEC (~22:56) and XLM (~22:36) — let expire on schedule or close residual runner into strength; **no adds, no re-entry.**
4. **Momentum basket:** FIDA/JTO/BANK = `avoid_chase`; only a structured pullback that holds (BANK ~0.033) with volume would be watch-worthy — not at market.
5. **Stocks (closed):** no action. Carry **SMCI/UNH legal-risk** flags and the **LLY A-tier invest long** into the Monday open slots; verify LLY's entry trigger live before any execution at reopen.
6. **Next slot (18:30 — US-open-reaction label, but Sunday → effectively late-US-session crypto):** re-scan the fresh cycle for any newly-triggered A/B and re-check BTC's $60K acceptance/rejection.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** **NO TRADE / WATCHLIST.** Fresh 15:15 report, regime mixed; no A/B; best watchlist BANK 60.6 (below threshold). Stand down; no-chase the bounce.
- **Crypto intraday:** **NO TRADE / WATCHLIST.** Fresh 15:48 report; no A/B; realized NEAR/ADA shorts banked; ETH +3.7% is a watch-tell, not a trigger.
- **Crypto swing:** **MANAGE-ONLY.** Swing report stale (~22.8h, excluded). ZEC & XLM longs = realized, expire tonight, no adds/re-entry.
- **Stocks (all modes):** **NO ACTION — market closed (Sunday).** Risk-off short book frozen; LLY A-tier long + SMCI/UNH legal-risk flagged for the Monday reopen.

---

## 13. Sources

- [coinpaper — Bitcoin Price Today: BTC Tests $60K After $4.4B ETF Outflows, What Next? (June 5, 2026)](https://coinpaper.com/17498/bitcoin-price-today-btc-tests-60-k-after-4-4-b-etf-outflows-what-next) — **WebFetch verified HTTP 200**; BTC ~$62,116, −3% 24h / −14% MTD, support $60K / $58–55K, resistance $70–74K, **BTC at 200-week MA first time since 2023**, ADX 36.74. _single_source._
- [Yahoo Finance — Bitcoin and ethereum prices today, Friday, June 5, 2026: Prices continue their descent — 5 reasons why](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-friday-june-5-2026-prices-continue-their-descent---5-reasons-why-113631165.html) — BTC opened $63,812 → $62,046; ETH opened $1,768.86 → $1,666.52; low $59,227 overnight; jobs report + Hezbollah-ceasefire-rejection drivers. _single_source._
- [BeInCrypto — Bitcoin ETF Outflows Hit 13-Day Streak as $4.3 Billion Exits the Funds (June 2026)](https://beincrypto.com/bitcoin-etf-outflows-record-streak-june-2026/) — record 13-day BTC-ETF outflow streak ~$4.33B / 59.4K BTC; 17-day ETH-ETF outflow streak. _single_source._
- [bitcoinfoundation.org — Bitcoin ETF Outflows June 2026: 13-Day $4.4B Record](https://bitcoinfoundation.org/news/crypto-etfs-news/etf-outflows-june-first-week/) — streak **ENDED June 5 with +$3.05M net inflow** (first June inflow); AUM $104.29B → $80.40B; holdings 1.277M BTC. _single_source._
- [Binance public ticker API — /api/v3/ticker/24hr (this run, ~16:30 EEST 2026-06-07)](https://api.binance.com/api/v3/ticker/24hr) — **BTC $61,844 (+1.57% 24h), ETH $1,622 (+3.71% 24h).** _primary_source (exchange API)._

_Source-discipline (§N): every external claim above carries source + title + date + URL; no uncited stats; no fabricated chart observations (chart MCP not loaded — declared); no test_source/fixture URLs; §13 present; external research was AVAILABLE this run._

---

## 14. Fix Requests / TODO

### TODO-catalyst-mapping-weak (recurring)
- **issue:** Catalyst symbol-mapping has been <50% for ≥4 consecutive runs (unmapped 67.1% → 68.7% → 73.0% → **75.3%** today), forcing the catalyst layer to "context-only" every slot.
- **evidence:** `data/catalysts/2026-06-07/catalyst_events.jsonl` 237/958 mapped (24.7%); `catalyst_cycle_12-48.md` other_news=196 of 202. Top unmapped are macro/rates/sector headlines (Trump-on-Fed, Pump.fun color, MSFT Build) with no resolvable crypto ticker.
- **suggested manual fix:** improve the catalyst symbol resolver — add market-wide/macro tagging (map rates/Fed/ETF-flow headlines → BTC+ETH basket; sector headlines → narrative basket) so macro items stop counting as fully unmapped; or split the metric into "macro/no-symbol-expected" vs "should-have-mapped-but-didn't."
- **priority:** medium
- **first observed:** 2026-06-06 (carried); reconfirmed 2026-06-07 16:30 EEST

### TODO-expired-signals-still-active (low)
- **issue:** Two intraday shorts (NEAR, ADA) created 2026-06-05 with `expires_at` 2026-06-06 are still returned by `active-signals` (status `tp2_hit`) a full day past expiry. Likely intended (realized-runner tracking), but it inflates the "active" count and can read as live exposure.
- **evidence:** `proposed_signals`: NEAR/USDT short intraday created 2026-06-05T12:58 exp 2026-06-06T13:01 status `tp2_hit`; ADA/USDT short intraday created 2026-06-05T11:58 exp 2026-06-06T11:58 status `tp2_hit` — both surfaced in `active-signals --asset-class crypto` on 2026-06-07.
- **suggested manual fix:** confirm whether `tp2_hit` past `expires_at` should remain in the "active" set; if it's runner-tracking, consider a distinct `status`/label (e.g. `runner` / `realized_open`) so the active-count reflects genuinely live, unexpired signals.
- **priority:** low
- **first observed:** 2026-06-07 16:30 EEST

### TODO-stocks-active-count-264 (low)
- **issue:** `active-signals --asset-class stocks` returns ~264 signals on a closed-market Sunday, dominated by Friday-dated index/mega-cap shorts already at `tp1_hit`/`tp2_hit`. Same realized-runner-vs-live ambiguity as above, at larger scale; risks reading as 264 live equity exposures over the weekend.
- **evidence:** DB query of `proposed_signals` asset_class='stocks' status in (triggered, waiting_for_entry, tp1_hit, tp2_hit) = 264; sample QQQ/SPY/XLK/MSFT/AMZN/META intraday shorts all tp1/tp2_hit, created Friday.
- **suggested manual fix:** apply the same realized/runner labeling to stocks; optionally auto-archive realized intraday stock signals at the weekly close so the weekend "active" view reflects only genuinely open exposure.
- **priority:** low
- **first observed:** 2026-06-07 16:30 EEST
