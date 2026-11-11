# Opus Enriched Review — US open reaction review — Auto Cycle 18:42 EEST

- **Generated:** 2026-06-10 18:42 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`, **18:30 "US open reaction review" slot**, executing `opus-enriched-review-4h/SKILL.md`)
- **Slot context:** ~2h into the US cash session (open 16:30 EEST / 09:30 ET; now ≈11:42 ET). First US-session reaction read: which pre-open ideas confirmed or failed, which stocks triggered and whether the entry was clean, fake/gap moves, breadth, whether A-tier looks trustworthy, crypto reaction to US flows.
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-10_1623.md` (pre-US-open decision review, 16:23 EEST, ~2.3h ago — see §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch). BTC confirmed $61,693 (-2.35% 24h), RSI(14) **23.95 oversold**, vol 2.11× avg, Crypto Fear & Greed **10 / Extreme Fear**, spot-BTC-ETF outflows $2B+ (est. $3.4–4.2B over ~11 days), $60K critical support. Macro: US-Iran tensions + strong June-5 labor report dampened rate-cut hopes (S&P −2.64% / Nasdaq −4.18% earlier in the week). UNH DOJ legal actions re Medicare **corroborated in UNH's own SEC 10-Q risk factors**; the specific June-10 antitrust-probe headline + −16% drop remains **single_source** (internal Yahoo Finance / QuiverQuant).
- **Chart tools:** TradingView / Chrome MCP not loaded — no fabricated chart observations. OHLCV/ATR/EMA from internal reports + cited external sources only.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

**18:42 EEST, ~2h into the US session. Risk-off both sides — and this slot the data finally agrees with the regime label: shorts are the working side.**

**Decisive in-session facts:**
- **The healthcare-long thesis from 16:23 BROKE.** UNH was hit by a DOJ antitrust/fraud probe (shares reported −16%). Stocks **by-direction flipped hard**: longs went from +15R (PF 1.9 at 16:23) to **−28R (PF 0.52)**; shorts went from −33R (PF 0.44) to **+11R (PF 1.46)**. Tech shorts confirmed in-session — **PLTR and AVGO B-shorts hit TP1**; TSLA / AMZN / NVDA / MSTR / GOOGL B-shorts triggered. Risk-off is now stat-confirmed, not just regime-labeled.
- **Crypto bleeds but is oversold.** BTC ~$61.7K (−2.35%), RSI **23.95**, Fear & Greed **10 (Extreme Fear)**, 11-day ETF-outflow bleed, sitting on the $60K shelf. Downtrend intact → shorts preferred, **but oversold + Extreme Fear = real squeeze/bounce risk**. Route crypto shorts to *failed-retest entries only — do NOT chase the flush.*
- **No A-tier either class. A-tier stocks remain broken** (PF 0.14, 1W/7L, avgR −0.60) — do not trust A-tier promotion this run.
- **Legal AVOIDs persist and one worsened:** UNH (DOJ probe, active C-longs contradict the crash) and SMCI (export-control indictment 8-K, active C invest/swing longs). Both → AVOID / manual review.
- **Catalyst mapping weak this run (≈82% unmapped) — use the catalyst layer as context, not a final decision input.**

**Best candidates this window:**
- **Best short-watch (stocks):** TSLA — B intraday short (65.2) waiting_for_entry 385.13–388.54, inval 395.35; the in-session shorts already worked, so this is a *short-the-retest-bounce* idea, not a breakdown chase. Trigger = price rallies back into 385–388 and fails; invalidation above 395.35.
- **Best short-watch (crypto):** SAHARA/USDT — B intraday short (68.7) waiting_for_entry 0.01746–0.01786, inval 0.018355. Trigger = failed retest, NOT a chase into oversold BTC. Caveat = thin alt + Extreme-Fear squeeze risk.
- **Best catalyst-backed:** HYPE/USDT — Coinbase futures live + ETF inflows (basket `perps_dex_narrative`, `wait_pullback`); after a 27% crash → catalyst-watch, wait for pullback structure, not a fresh long.
- **Best long-watch:** none clean. Risk-off both sides and the healthcare-long bucket just broke. If forced: only an oversold BTC reclaim of ~$63–64K on volume would re-open RS-leader longs — purely reactive, not actionable now.
- **What to avoid now:** UNH / SMCI (legal); chasing already-worked tech shorts (PLTR/AVGO TP1 done); chasing the BTC/alt short into oversold + Extreme Fear; new crypto longs into the ETF-outflow downtrend; momentum-basket chases (STRAX +48.6% / STG +43.5% / HMSTR +37.1% = `avoid_chase`).

---

## 2. Data Used

**Internal — crypto reports:**

| Report | Generated | Age at 18:42 | Status |
|--------|-----------|--------------|--------|
| Scalp | 2026-06-10 14:44 EEST (file mtime 17:44) | ~1.0h | **FRESH** |
| Intraday | 2026-06-10 14:58 EEST (file mtime 17:58) | ~0.7h | **FRESH** |
| Swing | 2026-06-10 01:28 EEST (file mtime 04:28) | ~14h | **STALE** (excluded from fresh swing verdict) |

**Internal — stocks reports:**

| Report | Generated | Age at 18:42 | Status |
|--------|-----------|--------------|--------|
| Stocks intraday | 2026-06-10 15:19 EEST (file mtime 18:19) | ~23 min | **FRESH** (live RTH) |
| Stocks swing | 2026-06-10 01:31 EEST (file mtime 04:31) | ~14h | **STALE** (carry-forward only) |
| Stocks invest | 2026-06-10 01:34 EEST (file mtime 04:34) | ~14h | **STALE** (carry-forward only) |

**CLI (captured 18:39–18:42 EEST):**
- `active-signals crypto`: **9 active** — SAHARA (B intraday short 68.7 waiting; B scalp short 71.1 **expired** 16:43), MORPHO (B scalp long 66.6 **expired** 17:36), plus TP-stack longs CHIP (swing tp2), ALLO (swing tp1; intraday tp1 expired), BANK (swing tp1), BABY (swing tp1), ZEC (intraday tp2, expired). Live actionable = **SAHARA intraday short**.
- `active-signals stocks`: **50 active** — B-tier are **all shorts**: TSLA (65.2 **waiting**, exp 06-11), NVDA (66.8 triggered, exp 19:44), PLTR (71.0 **tp1_hit**, exp 19:44), AVGO (66.5 **tp1_hit**, exp 18:31), plus GOOGL/MSTR/TSLA/AMZN B-shorts **expired 17:31**. C-tier healthcare/index longs (UNH/LLY/XLV/SMH/SMCI) triggered or waiting.
- `signal-stats crypto`: A/B PF **1.52**, +14R, WR 23.9% (n=94). By-mode: **scalp 0W/7L, −7R, PF 0.0 (broken)**; intraday PF 1.50 (+6R); swing PF 2.88 (+15R). By-direction: long PF 1.53 (+8R) ≈ short PF 1.50 (+6R). By exchange-confirm: cross-exchange PF 1.56 best.
- `signal-stats stocks`: A/B PF **1.08**, +2R, WR 27.8% (n=81). By-tier: B PF 1.44 (+8R); C PF 0.67 (−19R); **A PF 0.14, 1W/7L, −6R (broken)**. By-mode: intraday PF 1.20 (+10R); invest 0W/9L (−9R); swing PF 0.25 (−18R). By-direction: **short PF 1.46 (+11R) vs long PF 0.52 (−28R)**.
- `detect_untracked_legacy_alerts --since 2026-06-10`: **0 (clean).**

**Catalyst / narrative:** cumulative today **2,625 events**, **475 mapped / 2,150 unmapped (81.9% unmapped)**, **4 baskets**. Latest cycle (14-58): 479 rows, types other_news 458 (~96%), regulatory_sector_headline 7, legal_risk 4, exploit_hack 2, product_launch 3.

**Fresh Telegram-channel news (≤4h, n=45):** macro/geopolitical dominated — Hegseth/Iran warnings, Trump signs Secure America Act, "Altman expects OpenAI to go public within a year", NC Treasurer rejects SpaceX valuation. Risk-off tone, no clean single-symbol crypto catalyst surfaced in the window.

**LLM packets:** `llm_analysis_packet.md` (crypto) + `llm_stocks_packet.md` (stocks) refreshed in Cycle 3 (17:58 / 18:19).

**External:** InteractiveCrypto + Yahoo Finance (BTC price/RSI/ETF/Fear&Greed), SEC EDGAR (UNH 10-Q DOJ-Medicare risk factor). See §13.

---

## 3. Scheduler / Data Freshness

- **No defer.** Latest folder `2026-06-10_default_schedule`; `scheduler.log` mtime **18:21 EEST** (~18 min ago); latest `cycle_03_17-28_summary.md` mtime **18:21 EEST**. Both ≪ 3h → fresh, review proceeds.
- **Cycle 3 status:** 17:28→18:21 EEST, **steps ok=16, failed=0**. Pre-track: checked=343, tp_hits=197, stopped=6. Post-track: checked=342, stopped=7. Revalidation: 5 stale / 1 moved_away / 0 regime_changed (pre); 2 stale (post).
- **Minor data gaps (Cycle 3):** yfinance returned empty frames for **SPY/1h** and **^VIX/1h** (3 attempts each); fundamentals 404 for index ETFs (SPY/QQQ/XLK/XLF/XLV etc.) — daily candles still fetched, so intraday levels stand but hourly VIX/SPY context is thin (→ §14 low-priority TODO). Reddit social sources 403-blocked again (non-fatal).
- **Swing/invest reports ~14h old → STALE.** Excluded from fresh swing/invest verdicts; used only as carry-forward context.

---

## 4. What Changed vs Previous Review (16:23 EEST)

| Signal / Candidate | Prior (16:23) | Current (18:42) | Assessment |
|---|---|---|---|
| **Stocks by-direction** | long **+15R** (PF 1.9), short **−33R** (PF 0.44) | long **−28R** (PF 0.52), short **+11R** (PF 1.46) | **Full reversal in ~2h** — shorts now the working side; UNH crash drove long losses (also §14 stats-window note) |
| **Healthcare-long thesis** | best long-watch (LLY/XLV defensive longs winning) | **BROKEN** — UNH −16% on DOJ probe | Long-watch withdrawn; UNH C-longs now contradict price → AVOID |
| **Tech shorts** | triggered but bucket −33R (low-conviction) | **PLTR + AVGO B-shorts TP1 hit; TSLA/AMZN/NVDA/MSTR/GOOGL triggered** | In-session confirmation; shorts now regime- *and* stat-aligned |
| **Best crypto short** | ZEC/USDT (B short, waiting) | ZEC **closed/expired**; **SAHARA/USDT** B intraday short waiting | Replaced; SAHARA inval 0.018355 |
| **BTC** | ~$62.1K, −14% MTD, 13-day ETF bleed | **$61.7K, RSI 23.95 oversold, Fear&Greed 10, on $60K shelf** | Downtrend intact + **bounce/squeeze risk added** |
| **May CPI** | just printed (4.2% YoY hot / core 0.2% soft) | fully digested | No longer a live gap-risk event |
| **A-tier stocks** | broken (1W/10L, PF 0.13) | still broken (1W/7L, PF 0.14) | Do not trust A-tier promotion |
| **Legal AVOIDs** | SMCI, UNH | SMCI persists; **UNH materially worse** (−16%) | Both AVOID / manual review |
| **Crypto active count** | 11 | 9 | ZEC/TAO/WLFI/BTC ideas rolled off; MORPHO + SAHARA new |

Confirmed vs prior: risk-off both classes; A-tier broken; SMCI/UNH legal AVOIDs. Invalidated vs prior: the defensive-healthcare-long route (UNH headline killed it). New: SAHARA crypto short; in-session tech-short confirmation.

---

## 5. Catalyst Coverage

- **Total events today (cumulative):** 2,625 · **mapped (non-null symbol):** 475 · **unmapped:** 2,150 → **81.9% unmapped.**
- **Latest cycle (14-58):** 479 events, of which `other_news` = 458 (~96%), `regulatory_sector_headline` 7, `legal_risk` 4, `exploit_hack` 2, `product_launch` 3, `insider_activity`/`platform_growth`/`buyback_burn`/`partnership`/`exchange_listing` 1 each.
- **Narrative baskets (4):** `binance_ecosystem_teaser` (BNB/ASTER, `related_beta_rotation`, sell-the-news risk) · `perps_dex_narrative` (HYPE + DYDX/GMX/ASTER, `wait_pullback`) · `ai_narrative` (NEAR/RENDER/TAO/FET + WLD/ASTER, `related_beta_rotation`) · `momentum_breakout` (STRAX/STG/HMSTR, `wait_pullback`, **`avoid_chase` — +48.6%/+43.5%/+37.1%**).
- **⚠️ Catalyst mapping weak this run (82% unmapped) — use the catalyst layer as context, not a final decision.**
- **Top 3 unmapped (null-symbol) headlines by importance:** (1) "xAI and SpaceX face class action lawsuit over data center noise…" (0.75); (2) "New Windows zero-day exploit RoguePlanet targets Microsoft Defender…" (0.75); (3) "Claude Fable 5: The World's Most Powerful Hacking AI Should Make DeFi Worried" (0.73).
- **Mapped high-signal catalysts:** HYPE (Coinbase futures live + ETF inflows $91M; GENIUS-Act pushback) · **SMCI legal_risk** (export-control indictment 8-K, SEC EDGAR) · **UNH legal_risk** (DOJ probe, Yahoo/QuiverQuant) · BTC ETF outflows (CoinGlass; 3rd consecutive weekly outflow ~$4.21B/3wk).

---

## 6. Market Landscape

US session ~2h in. Tape is risk-off and the short side is doing the work today: tech-mega-cap B-shorts triggered and PLTR/AVGO already booked TP1, while the defensive-healthcare-long trade that looked best pre-open was knocked out by the UNH DOJ headline. Breadth skews bearish (B-book is uniformly short across TSLA/NVDA/PLTR/AVGO/GOOGL/MSTR/AMZN). Crypto is in an extended downtrend (BTC −2.35% to $61.7K, 11-day ETF bleed) but technically stretched — RSI 23.95, Extreme-Fear 10, parked on $60K — so the highest-probability error here is *chasing a short into a flush* rather than missing fresh downside. Geopolitics (Iran) and a strong labor print remain the macro overhang dampening rate-cut hopes.

### Market Mood / Risk Routing      (REQUIRED — PART 4)
- **Crypto mood:**            risk-off, but oversold/stretched → **risk-off + chop** (squeeze-prone)
- **Stocks mood:**            risk-off (live RTH, ~2h in) — short side confirmed
- **Dominant narrative:**     macro risk-off (Iran + sticky inflation + ETF outflows); single-name legal shocks (UNH DOJ, SMCI indictment)
- **Preferred side now:**     **shorts (both classes) — on failed-retest / confirmation, not chase**
- **Best long candidate:**    none clean — trigger: BTC reclaims & holds ~$63–64K on volume, then RS-leader longs only
- **Best short candidate:**   TSLA (stocks, short-the-retest 385–388) · SAHARA/USDT (crypto, failed-retest)
- **Best catalyst-backed candidate:** HYPE/USDT (Coinbase futures + ETF inflows; `wait_pullback`)
- **What to avoid:**          UNH/SMCI (legal); chasing PLTR/AVGO (TP1 done); chasing BTC/alt shorts into Extreme Fear; new crypto longs; STRAX/STG/HMSTR momentum chases
- **What would change the view:** stocks → a broad RTH reversal up (shorts failing, breadth flipping); crypto → BTC reclaim of $63–64K (longs re-open) OR clean failed retest of $60K (shorts re-open with room)

---

## 7. Candidate Deep Dives (≤ 5)

### 1. TSLA — stocks, B intraday **short** 65.2, waiting_for_entry (PRIORITY: new/fresh B + regime-aligned)
- Entry 385.13–388.54 · invalidation 395.35 · exp 2026-06-11T15:19. Freshest live B-tier stock short (15:19 cycle).
- **Price reaction:** TSLA shorts already worked this session (C-tier TSLA intraday short tp1_hit ~395→below). The live B entry sits *above* current action → this is a **short-the-bounce-retest**, not a breakdown chase.
- **Chase risk:** HIGH if entered at market now; LOW if it rallies back into 385–388 and fails. Entry zone is above current price (not >2 ATR extended into the entry).
- **Mood-aligned:** yes (risk-off, shorts working). **Type:** short, **after confirmation** (retest into zone). **Invalidation:** reclaim/hold above 395.35.
- **Catalyst:** no clean TSLA-specific headline in the 4h window; pure regime/technical.
- **Verdict:** **SHORT-WATCH** — short the retest into 385–388, stop 395.35; do not chase below.

### 2. UNH — stocks, C-tier **longs** (invest 59 / swing 68.2 / intraday) + **LEGAL/HEADLINE RISK** (PRIORITY: contradiction + legal)
- **LEGAL/HEADLINE RISK:** DOJ antitrust/fraud probe; shares reported **−16%** (internal Yahoo Finance + QuiverQuant, single_source). **Corroborated** by UNH's own SEC 10-Q risk factors acknowledging "the DOJ's legal actions concerning our participation in the Medicare program."
- **Contradiction:** active C-tier *longs* directly contradict a −16% legal-driven crash → integrity flag.
- **Verdict:** **AVOID / MANUAL REVIEW REQUIRED** — never a clean long here. Treat C-long signals as stale vs the headline.

### 3. SAHARA/USDT — crypto, B intraday **short** 68.7, waiting_for_entry (PRIORITY: best live crypto B)
- Entry 0.017459–0.017862 · invalidation 0.018355 · exp 2026-06-11T14:58. (Scalp short 71.1 already **expired** 16:43.)
- **Price reaction / chase:** thin alt; risk-off macro supports downside, but **BTC oversold (RSI 23.95) + Extreme Fear 10** = elevated bounce/squeeze risk for crypto shorts broadly.
- **Mood-aligned:** yes (risk-off) but **chop/squeeze caveat.** **Type:** short, **after failed retest only.** **Invalidation:** 0.018355.
- **Catalyst:** none mapped to SAHARA; no fresh Telegram catalyst.
- **Verdict:** **SHORT-WATCH** — failed-retest entry only; size small (thin alt + squeeze risk); do not chase the flush.

### 4. SMCI — stocks, C invest/swing **longs** (62.9 / 70.6, waiting) + **LEGAL/HEADLINE RISK** (PRIORITY: integrity/legal)
- **LEGAL/HEADLINE RISK:** Form 8-K (FY2026) — indictment of three individuals re alleged export-control violation conspiracy (SEC EDGAR, single_source); prior export-control flag persists.
- **Contradiction:** active C *longs* vs an unresolved indictment headline.
- **Verdict:** **AVOID** — do not treat SMCI longs as actionable while the legal overhang is live.

### 5. PLTR / AVGO — stocks, B intraday **shorts** (71.0 / 66.5), **TP1 already hit** (PRIORITY: in-session confirmation)
- PLTR exp 19:44, AVGO exp 18:31 (expiring ~now). Both confirmed the risk-off short thesis intraday.
- **Price reaction:** move already played — entering fresh now = **chase/late.** Manage existing only (trail to entry/partial), do not initiate new.
- **Verdict:** **CONFIRMATION ONLY / NO NEW ENTRY** — evidence that shorts work today, not a fresh trigger.

---

## 8. Best Candidates Ranked

1. **TSLA (stocks short-watch)** — short the retest into 385.13–388.54, stop 395.35. Regime- and stat-aligned (stocks short PF 1.46, +11R). Best risk/reward of the live set. *Actionable on retest, not now.*
2. **SAHARA/USDT (crypto short-watch)** — failed-retest short into 0.01746–0.01786, stop 0.018355, small size. *Caveat: oversold-BTC squeeze risk.*
3. **HYPE/USDT (catalyst-watch)** — Coinbase futures live + ETF inflows; `wait_pullback` after −27%. *Re-engage on pullback structure, not a fresh long.*

**No clean immediately-actionable trade this window** (everything is wait-for-confirmation). Per PART 9:
- **Best long-watch:** none clean — **trigger:** BTC reclaims & holds ~$63–64K on rising volume → then crypto RS-leader longs; until then no long.
- **Best short-watch:** **TSLA** — **trigger:** rally back into 385–388 that fails (stop 395.35).
- **Best catalyst-watch:** **HYPE/USDT** — **trigger:** pullback completes + holds, single_source catalyst upgraded to multi-source confirmation.

---

## 9. Avoid / No Trade (this decision window only — scanner keeps running)

- **UNH** — DOJ probe / −16%; active longs contradict the crash → AVOID / manual review.
- **SMCI** — export-control indictment 8-K; active longs vs legal overhang → AVOID.
- **PLTR / AVGO** — B-shorts already TP1; chasing now is late → no new entry.
- **STRAX / STG / HMSTR** — momentum basket +48.6% / +43.5% / +37.1%, `avoid_chase` (overextended, no confirmed catalyst).
- **New crypto longs** into the 11-day ETF-outflow downtrend — wait for a reclaim.
- **Chasing BTC/alt shorts** into RSI 23.95 + Extreme-Fear 10 near $60K — squeeze risk; require a failed retest.

*This is a current-window decision only. It is NOT a command to disable or pause the scanner, tracking, monitors, or scheduler — those continue in all moods.*

---

## 10. Main Risks

- **Oversold-bounce / short-squeeze (crypto):** RSI 23.95 + Extreme Fear 10 + $60K shelf → a sharp relief bounce can stop out fresh shorts. Highest-probability error this slot = chasing a short into the flush.
- **Stale-data risk:** swing/invest reports ~14h old (excluded from fresh verdicts); thin hourly SPY/VIX context (yfinance 1h empty frames).
- **Single-source legal claims:** UNH −16%/probe and SMCI indictment are single_source internally; UNH partially corroborated via SEC 10-Q risk factors. Verdicts kept conservative (AVOID) so the discipline gap doesn't create false actionables.
- **Stats-window instability:** stocks by-direction flipped sign in ~2h (short −33R→+11R, long +15R→−28R) — coherent with the UNH crash + in-session short wins, but flagged as a possible tracking-window artifact (§14).
- **A-tier untrustworthy:** A-tier stocks PF 0.14 (1W/7L) — any A-tier promotion this run should be treated with suspicion.
- **Catalyst layer weak (82% unmapped):** do not lean on it for final decisions.
- **Ingest note:** external-source ingest attempted in §M; any failure logged here and the review still completes.

---

## 11. Action Plan — next 4 hours (into the 21:30 late-session risk slot)

1. **Stocks:** monitor TSLA for a retest bounce into 385–388 to short (stop 395.35). Do NOT initiate new PLTR/AVGO shorts (TP1 done) — manage only. Keep all UNH/SMCI longs flagged AVOID.
2. **Crypto:** wait on SAHARA short for a failed retest of 0.01786 (stop 0.018355), small size. Watch BTC $60K — a clean failed retest re-opens shorts with room; a reclaim of $63–64K flips toward RS-leader longs.
3. **Catalyst-watch:** HYPE pullback structure; recheck if the Coinbase-futures/ETF-inflow catalyst gets multi-source confirmation.
4. **Avoid:** momentum chases (STRAX/STG/HMSTR), new crypto longs, chasing the BTC short into Extreme Fear.
5. **Re-check at 21:30** late-session risk slot: are TSLA/SAHARA retests in play, did BTC hold $60K, did any active signal hit TP/stop/invalidation.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** NO NEW — scalp bucket broken (0W/7L, −7R); only fresh scalp short was SAHARA (expired). Wait.
- **Crypto intraday:** SHORT-WATCH only — SAHARA failed-retest, small size; no chase into oversold BTC.
- **Crypto swing:** report STALE (~14h) → carry-forward only; existing TP-stack longs (CHIP/ALLO/BANK/BABY) manage/trail, no fresh swing entry.
- **Stocks intraday:** SHORT-BIAS confirmed — TSLA retest-short is the cleanest setup; PLTR/AVGO manage-only; longs avoid (UNH/SMCI legal).
- **Stocks swing/invest:** STALE (~14h) → no fresh verdict; invest bucket 0W/9L and swing PF 0.25 both weak — carry-forward caution only.

---

## 13. Sources

- [InteractiveCrypto — Bitcoin's 2.35% drop to $61,693 fueled by $2B ETF outflows and macro fears (Jun 2026)](https://www.interactivecrypto.com/bitcoin-s-2-35-drop-to-61-693-fueled-by-2b-etf-outflows-and-macro-fears-jun-2026) — 2026-06-10 — single_source — *confirms* BTC $61,693 / −2.35% / RSI 23.95 / ETF outflows / $60K support.
- [Yahoo Finance — Bitcoin Price Prediction for June 2026: Institutional Exodus Foreshadows a Crash?](https://finance.yahoo.com/markets/crypto/articles/bitcoin-price-prediction-june-2026-070000962.html) — 2026-06-10 — single_source — *confirms* ETF outflows / Extreme Fear / institutional selling.
- [SEC EDGAR — UnitedHealth Group Inc, Form 10-Q FY2026](https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000127/unh-20260331.htm) — 2026-03-31 — primary_source — *corroborates* DOJ legal actions re Medicare in risk factors (partial; specific June-10 antitrust-probe headline remains single_source via internal Yahoo/QuiverQuant).
- **Internal (read-only):** catalyst_cycle_14-58 + catalyst_events.jsonl (UNH DOJ via Yahoo/QuiverQuant; SMCI indictment via SEC EDGAR; HYPE Coinbase/ETF; BTC ETF outflows via CoinGlass), news_items Telegram (WalterBloomberg/lookonchain, ≤4h), cycle_03_17-28_summary.md, signal-stats / active-signals CLI.

---

## 14. Fix Requests / TODO

### TODO-stocks-A-tier-broken
- **issue:** Stocks A-tier remains a losing bucket: PF 0.14, 1 win / 7 losses, avgR −0.60 (n=13). Persisting across multiple reviews (was 1W/10L PF 0.13 at 16:23).
- **evidence:** `python -m src.cli signal-stats --asset-class stocks` → By tier: tier=A PF 0.142857, totalR −6.0; observations: "tier=A profit factor 0.14 below 0.8."
- **suggested manual fix:** audit A-tier promotion criteria for stocks (over-promotion of low-quality setups); consider raising the A threshold or adding a confirmation gate.
- **priority:** high
- **first observed:** 2026-06-10 16:23 EEST (carried forward)

### TODO-crypto-scalp-bucket
- **issue:** Crypto scalp mode is a reproducible losing bucket: 0 wins / 7 losses, totalR −7.0, PF 0.0 (n=50).
- **evidence:** `signal-stats --asset-class crypto` → By mode: mode=scalp PF 0.0, avgR −0.2121, totalR −7.0.
- **suggested manual fix:** tighten crypto scalp entry/confirmation or demote scalp signals to watchlist until the bucket recovers.
- **priority:** medium
- **first observed:** 2026-06-10 16:23 EEST (carried forward)

### TODO-stocks-invest-swing-buckets
- **issue:** Stocks invest mode 0W/9L (−9R, PF 0.0) and swing PF 0.25 (6W/24L, −18R) both deeply negative.
- **evidence:** `signal-stats --asset-class stocks` → By mode: mode=invest totalR −9.0; mode=swing PF 0.25 totalR −18.0.
- **suggested manual fix:** review long-horizon stock scoring (heavily long-skewed into a risk-off tape) and re-weight or pause fresh invest/swing entries pending review.
- **priority:** medium
- **first observed:** 2026-06-10 18:42 EEST

### TODO-catalyst-mapping-weak
- **issue:** Catalyst symbol mapping ≈82% unmapped (2,150 / 2,625 null-symbol events today); latest cycle other_news ≈96%. Persisting multi-run.
- **evidence:** catalyst_events.jsonl count (mapped 475 / unmapped 2,150); cycle_14-58 type breakdown other_news 458/479.
- **suggested manual fix:** improve the symbol resolver in the catalyst layer (ticker/entity extraction) so macro/sector headlines map to affected symbols or are de-prioritized rather than flooding `other_news`.
- **priority:** medium
- **first observed:** 2026-06-10 16:23 EEST (carried forward)

### TODO-bydirection-stats-window-instability
- **issue:** Stocks by-direction stats flipped sign in ~2h (short −33R→+11R, long +15R→−28R). Likely coherent (UNH −16% crash + in-session short wins) but the magnitude/speed suggests the rolling-window may be re-labeling or aging samples abruptly.
- **evidence:** 16:23 review §2 (short PF 0.44 −33R, long PF 1.9 +15R) vs 18:42 `signal-stats stocks` By direction (short PF 1.4583 +11R, long PF 0.5172 −28R).
- **suggested manual fix:** verify the signal_outcomes window logic and whether outcomes are recomputed/relabeled within a session in a way that overstates intraday swings.
- **priority:** low
- **first observed:** 2026-06-10 18:42 EEST

### TODO-yfinance-1h-empty-frames
- **issue:** yfinance returned empty frames for SPY/1h and ^VIX/1h (3 attempts each) in Cycle 3 → thin intraday VIX/SPY context; index-ETF fundamentals 404.
- **evidence:** cycle_03_17-28_summary.md step 6 log: "yfinance fetch failed for SPY/1h … returned empty frame", "yfinance fetch failed for ^VIX/1h …".
- **suggested manual fix:** add a fallback intraday source for SPY/VIX hourly (or retry/backoff), so the risk gauge isn't blind on hourly during US RTH.
- **priority:** low
- **first observed:** 2026-06-10 18:42 EEST
