# Opus Enriched Review — US open reaction review — Auto Cycle 18:30 EEST

## 1. Executive Summary

**Tuesday 2026-06-16, 18:42 EEST "US open reaction review" slot — ~2h into the RTH session (cash open was 16:30 EEST / 09:30 ET).** External web research **AVAILABLE** this run (WebSearch ×4 + WebFetch — one fetch surfaced and rejected a **stale/mis-dated article**, see below).

**The open-reaction read: the risk-on open confirmed, broad but Dow/financials/small-cap-led, mega-cap tech flat.** Tape today: **S&P 500 +0.13%, Dow +0.78%, Nasdaq +0.02%, Russell 2000 +0.72%, VIX ~16** ([TheStreet via search summary](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-16-2026)). Regime stays **risk_on** (desk: VIX 15.97, breadth 100% > EMA20/EMA50, QQQ/IWM/DIA uptrend, SPY range). FOMC is **mid-meeting; decision tomorrow Wed Jun 17** (Warsh's first, ~97% hold) — the tape is a pre-decision drift, not a clean trend day. Dominant single-stock story: **SpaceX to acquire AI-coding startup Anysphere for $60B** (SpaceX +8.9% premarket) — IPO/M&A momentum, **not** a desk signal.

**Two stock A/B intraday longs are live and confirmed-triggered — but both carry caveats.** **JPM (A-tier 80.9, triggered)** is a financials RS-leader (RS +8.7% vs SPY, above prev-day high, earnings-safe) and is regime-aligned (Dow +0.78%, XLF strong) — **but its RR-to-TP1 is only 1.0 (below 1.5)**, and the season-long signal-stats show **stock intraday longs are the worst bucket (PF 0.6, −17R) and longs overall −23R**, vs shorts +15R. **AMD (B-tier 76.5, triggered)** is the strongest RS name (+22% vs SPY) **but has already run to ~$548.80 today — above the desk entry zone 520.64–526.03 and past TP1 (542.20)** → entering now is a **chase**, not a clean entry. **Verdict: JPM = actionable with RTH/retest confirmation + modest size (tight RR); AMD = do NOT chase, wait for a pullback into the zone.**

**Crypto stays risk-on but range-capped and pinned under the $67K pivot into tomorrow's FOMC.** BTC ~**$66,449–66,700** (two-week high, fourth straight up session); tagged **~$67K and was rejected**, settled +0.5%. Range $65–66K, resistance **$67K** (→ $68.5–70K on a clean break), support **$64K → $63.3K**. Tailwind: **US–Iran peace deal finalized + Strait of Hormuz reopening** (geopolitical relief) ([FinanceMagnates](https://www.financemagnates.com/trending/why-is-bitcoin-going-up-today-btc-price-eyes-70k-test/), [Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-tuesday-june-16-2026-highest-opening-values-in-two-weeks-113313567.html)). Crypto desk reports are ~3h old (data 12:15–12:30 UTC) → BTC/ETH uptrend, alt breadth 79.5% > EMA20, normal vol; best crypto long-watch carry-forward **INJ / ETH** (catalyst-backed, pullback-only).

**Routing — RS-leader longs with confirmation; no fresh shorts (both classes); do NOT chase extended names.** Crypto **A/B winrate 14.7%, PF 1.13**; shorts PF 0.5 (−3R) vs longs PF ~1.2 (+10R); exchange-confirmed signals PF 1.5 (+12R) vs unconfirmed 0.8 (−3R) — **prefer exchange-confirmed longs**. Stocks **A/B winrate 18.2%, PF 0.94 (−1R)**; the recent 14d window + risk_on favor RS-leader longs, but the season-long sample warns stock longs bleed — so **size modest, confirmation-gated**. **Integrity: 17 untracked legacy crypto alerts** (up from 14 at 16:24) sent to Telegram with no `proposed_signal` → §14 TODO. **Catalyst mapping weak (76.5% unmapped) — context only.** Advisory only; scanner/collection/tracking continue in all moods — nothing here says stop the system.

## 2. Data Used

- **Crypto scalp report** `data/reports/scalp/2026-06-16_12-33_scalp_report.md` — **carry-forward** (mtime 15:33 EEST, ~3.1h; data 12:15 UTC).
- **Crypto intraday report** `data/reports/intraday/2026-06-16_12-48_intraday_report.md` — **carry-forward** (mtime 15:48 EEST, ~2.9h; data 12:30 UTC).
- **Crypto swing report** `data/reports/swing/2026-06-16_13-32_swing_report.md` — **FRESH** (mtime 16:32 EEST, ~2.2h).
- **Stocks intraday report** `data/reports/stocks/intraday/2026-06-16_15-20_stocks_intraday_report.md` — **FRESH** (mtime 18:20 EEST, ~0.4h; data 15:20 UTC) — **the key US-open-reaction report this slot.**
- **Stocks swing** `…13-44…` (mtime 16:44 EEST, ~2h) + **invest** `…13-54…` (mtime 16:54 EEST, ~1.8h) → **FRESH** planning context.
- **Catalysts** `data/catalysts/2026-06-16/` present: `catalyst_cycle_12-49.md` (latest), `catalyst_events.jsonl`, `narrative_baskets.jsonl` (5 baskets). No catalyst-scan needed.
- **LLM packets** `data/processed/llm_analysis_packet.md` (crypto) + `llm_stocks_packet.md` (stocks) present.
- **Internal CLI:** `active-signals` crypto (**36 active, all long B**, scores 65–76) + stocks (**50 active**; **A-tier JPM intraday 80.9 + B-tier JPM 77.3 / AMD 76.5 / SMH 71.5 triggered**, plus QQQ/XLK/XLF/DIA/IWM B-tier, rest C); `signal-stats` ×2; `detect_untracked_legacy_alerts --since 2026-06-16` → **17 untracked**.
- **External:** WebSearch ×4 (US tape + JPM/AMD; JPM legal; BTC/FOMC; AMD/semis). WebFetch: Yahoo "Dow slips as JPMorgan slides" → **HTTP 200 but dated 2025-12-09 (stale, JPM −4% on a 2025 credit-card cost warning) → REJECTED, not used as today's data.** TheStreet Jun-16 URL → **HTTP 403** (consistent recurring block) → fell back to search summary for the tape (declared here).
- **§M ingest:** built `data/raw/enriched_review_sources/2026-06-16T1542Z.json` (4 cited sources); ingest CLI results in §10/§13.

## 3. Scheduler / Data Freshness

- Latest run folder: `data/scheduled_runs/2026-06-16_default_schedule/`.
- `scheduler.log` mtime **16:55:53 EEST** (~1.8h old) → **FRESH**.
- Latest `cycle_*_summary.md`: `cycle_02_15-08_summary.md` mtime **16:55:51 EEST** (~1.8h).
- **Defer rule needs BOTH log AND latest cycle summary > 3h. Both ~1.8h → review proceeds.**
- Freshness labels: stocks intraday **FRESH** (~0.4h, the slot-relevant report); stocks swing/invest **FRESH** (~1.8–2h); crypto swing **FRESH** (~2.2h); crypto scalp/intraday **carry-forward** (~2.9–3.1h, data 12:15–12:30 UTC — still inside the <4h fresh band, but crypto levels below are reconciled against live web quotes).

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-06-16_1624.md` (pre-US-open decision review):

- **Window moved pre-open (T-6 min) → ~2h into RTH.** Posture shifts from "what to do at the open / gap + stale-data risk" → **"which pre-open ideas confirmed; clean entry vs chase; fake-move check."**
- **The open confirmed risk-on** — S&P +0.13% / Dow +0.78% / Nasdaq +0.02% / Russell +0.72%, VIX ~16. Broad and Dow/financials/small-cap-led; mega-cap tech flat. Breadth on the desk firmed to **100% > EMA20** (was 75% pre-open).
- **Stock A-tier is BACK and live:** the AMD/SMH/JPM A-tier triggers that had *expired pre-open* at 16:24 have re-fired post-open — **JPM is now a fresh A-tier intraday long (80.9, triggered)**; AMD/SMH are triggered B-tier. The 16:24 "all C-tier (market-closed demotion)" report has been replaced by a live RTH report with real A/B.
- **AMD has already run:** at 16:24 AMD was "planning long, RTH-confirmation required" on fresh levels; it has now **moved to ~$548.80 — above the 520–526 entry zone and past TP1 (542.20)** → the idea flipped from "best stock long after open" to **"confirmed but now a chase — wait for pullback."**
- **SpaceX story concretized:** "SpaceX +8.9% premarket" (16:24) is now backed by a concrete catalyst — **SpaceX acquiring Anysphere for $60B**. Still not a desk signal.
- **Crypto little changed:** BTC ~$65,940 (16:24) → **~$66,449–66,700** now, still rejected at $67K, range-bound into FOMC. **Iran deal moved from "signing scheduled Fri Jun 19" → "finalized + Strait of Hormuz reopening"** (geopolitical relief realized).
- **Integrity worsened again:** untracked legacy crypto alerts **14 (16:24) → 17 (now)** — recurring §14 TODO, now spanning ETH/JTO/XLM/WLD/ZRO/INJ/GPS scalp+intraday+swing.
- **Catalyst mapping unchanged-weak:** 76.5% unmapped (same as 16:24) — recurring §14.

## 5. Catalyst Coverage

- Raw `catalyst_events.jsonl` today: **2,731 rows; mapped (non-null symbol) 642; unmapped 2,089 = 76.5%.** Narrative baskets: **5**.
- **⚠ Catalyst mapping weak this run (76.5% unmapped) — use the catalyst layer as context, not final decision.**
- **Top 3 unmapped (by importance, all DeFi-exploit / macro):** (1) "Humanity Protocol sunsets H token after hack, launches airdrop to restore holders" (CryptoBriefing, 0.75); (2) "Deprecated Thetanuts Vault Exploited for $2.1 Million in Latest DeFi Attack" (BeInCrypto, 0.75); (3) "Exploit-Driven TVL Drop Pushes DeFi Leverage Back to 2021 Levels" (BeInCrypto, 0.73). DeFi-exploit cluster again dominates the high-importance unmapped tail → background risk-off tail in alts, not symbol-specific.
- **Narrative baskets (5):** **perps_dex_narrative** primary **HYPE/USDT** (<1h); **rwa_narrative** (ONDO/XLM, <1h); **ai_narrative** (NEAR/RENDER/TAO/FET, <6h); **delisting_thin_liquidity** (avoid_low_liquidity, <24h); **momentum_breakout** primary **PORTAL/USDT** (+41.7%, <1h — overextended).

## 6. Market Landscape

- **Stocks (US, ~2h into RTH):** regime **risk_on, bias long, VIX 15.97**, breadth **100% > EMA20/EMA50**; QQQ +4.3%/IWM +3.1%/DIA +2.4% (20d) uptrend, SPY range. Tape today S&P +0.13% / Dow +0.78% / Nasdaq +0.02% / Russell +0.72% — **broad but Dow/financials/small-cap-led, mega-cap tech flat**. Strongest sectors: **semis SMH (RS +14.1% 20d), tech XLK (+5.4%), financials XLF (+4.1%)**; weakest energy XLE (−9.2%), comms XLC (−6.5%). Live A/B: **JPM A 80.9 / AMD B 76.5 / SMH B 71.5** (all intraday longs, triggered, actionable). Catalyst: SpaceX/Anysphere $60B. FOMC decision **tomorrow** → drift, not trend.
- **Crypto (desk data ~3h old, reconciled to live web):** bullish trend / risk-on, **range-capped, pinned under $67K into FOMC**. BTC + ETH uptrend; alt breadth **79.5% > EMA20 / 84.1% > EMA50**, BTC ATR percentile **32 (normal vol)**. **BTC ~$66,449–66,700** (briefly ~$67K, rejected), resistance **$67K** (→ $68.5–70K on break), support **$64K → $63.3K**. Active crypto signals **all B-tier longs** (scores 65–76); strongest tags relative_strength/volume. Tailwind: Iran peace + Hormuz reopening.

### Market Mood / Risk Routing  (REQUIRED — PART 4)
- **Crypto mood:**           **risk-on but range-capped + pre-FOMC** ($67K tagged & rejected, decision tomorrow, geopolitical relief tailwind).
- **Stocks mood:**           **risk-on, RTH open confirmed** (broad, Dow/financials/small-cap-led, mega-cap tech flat; FOMC drift; SpaceX/Anysphere M&A story).
- **Dominant narrative:**    **AI/semis leadership** (AMD/SMH RS leaders) + **financials strength** (JPM, XLF, Dow leg); **SpaceX $60B Anysphere acquisition**; **US–Iran peace / Hormuz reopening** (risk relief, BTC tailwind); BTC pinned under $67K into FOMC.
- **Preferred side now:**    **RS-leader longs with confirmation** (no chasing extended names); **no fresh shorts** (crypto shorts PF 0.5; stock shorts season-long +15R but disfavoured in a confirmed risk-on open).
- **Best long candidate:**   **JPM** (stocks, A-tier 80.9, triggered, RS-leader, financials/Dow-aligned) — actionable on a retest into 328.35–329.46 with modest size (tight RR 1.0); crypto: **INJ** long-watch on pullback, BTC-gated >$64K.
- **Best short candidate:**  **none clean** — confirmed risk-on open + crypto range-up disfavour shorts. Short-watch only **after a failed retest of broken support AND BTC losing $64K** (thin/squeeze-prone alts only).
- **Best catalyst-backed candidate:** **ETH** (crypto — RWA-flow + geopolitical relief, pullback-only) / **AMD** (stocks — AI-semis + Iran-relief, but now EXTENDED → pullback-only, not a chase).
- **What to avoid:**         **chasing AMD ~$548 above its 520–526 zone / past TP1 542**, chasing SPCX/SpaceX-spillover, overextended crypto (PORTAL +41%, JTO), fresh shorts into a risk-on open, oversizing into tomorrow's FOMC, crypto scalp lane (worst mode PF ~0.33, −4R).
- **What would change the view:** BTC **clean acceptance >$67K on volume** (→ $68.5–70K) or **loses $64K** (→ $63.3K flush); **FOMC tomorrow hawkish surprise / Warsh hawkish guidance** (→ risk-off, invalidates the long routing); SPY breaking its intraday range down (would void the stock longs); a clean **AMD pullback into 520–526** (re-arms the AMD long).

## 7. Candidate Deep Dives (≤ 5)

### Candidate 1 — JPM (stocks, A-tier intraday LONG 80.9, triggered) · best stock long
- **Setup:** A-tier intraday long, score 80.93, status **triggered/actionable**. Entry 328.3489–329.4550, invalidation close beyond 326.1368, TP1 332.7732 / TP2 334.9853 / TP3 338.3035. Expires 2026-06-17 15:20 UTC. RS leader (RS +8.68% vs SPY, +4.61% vs sector 20d), above prev-day high, earnings-safe. Also active B-tier intraday 77.3 + C-tier swing/invest — multi-mode agreement.
- **Catalyst check (internal-first + external):** no fresh symbol-specific bullish catalyst; the driver is **financials/Dow strength** (Dow +0.78%, XLF RS +4.1%) in a risk-on open. **Legal/headline (§I):** background items found — **"JPM Sued Over $328M Crypto Scam"** and an **industry-wide DOJ "debanking" subpoena** (multiple banks, not a JPM-specific indictment); also a 2025 sexual-assault civil suit. None is a *fresh material* price driver today and none is a JPM-specific indictment/SEC action → **not an auto-AVOID**, but a standing background headline-risk line. (Note: a Yahoo "JPMorgan slides −4%" headline surfaced in search but was **dated 2025-12-09** — a credit-card cost warning — and was **rejected as stale**, NOT today's data.)
- **Contradiction risk (§F-2):** the signal is an **intraday long**, but season-long `signal-stats` show **stock intraday longs are the worst bucket (PF 0.6, −17R)** and **longs overall −23R** (vs shorts +15R). The recent 14d window + risk_on regime favor RS-leader longs, but A/B winrate is only 18.2% and the A-tier sample is thin (overpromotion caveat in the playbook). **RR-to-TP1 is only 1.0 (below the 1.5 bar)** — the single biggest quality weakness.
- **Price/chase:** has price reacted? JPM participated in the Dow/financials leg but is not parabolic. Overextended >2 ATR? No. Mood-aligned: yes (risk-on, financials strong). Long/short/wait: **long**. Actionable now? **Yes, but only on a retest into 328.35–329.46 with modest size** — not on a stretch above the zone. Invalidation: close beyond 326.14. Chase-risk: moderate if entered extended; low on a zone retest.
- **Decision:** **ACTIONABLE LONG — retest-into-zone (328.35–329.46), modest size, RR-aware (TP1 only 1.0R).** Best stock long this slot. Tight RR + losing-bucket history cap conviction → confirmation-gated, not a size-up.

### Candidate 2 — AMD (stocks, B-tier intraday LONG 76.5, triggered) · strongest RS but now EXTENDED
- **Setup:** B-tier intraday long 76.47, **triggered**. Entry 520.6398–526.0293, invalidation 509.8608, TP1 542.1978 / TP2 552.9768 / TP3 569.1454. RS leader (RS +22.06% vs SPY, +7.92% vs sector). Also C-tier swing 75.2 / invest 71.0.
- **Catalyst check:** AI-semis leadership + **Iran peace / geopolitical relief** ([GuruFocus: "AMD Stock Surges Amid Positive Geopolitical Developments"](https://www.gurufocus.com/news/8912543/amd-stock-surges-amid-positive-geopolitical-developments)). No earnings/legal risk. Caveat: simplywall.st flags AMD **"~21.6% overvalued, trading above analyst price target"** after a +130% YTD / +174% 90d run — momentum, but stretched valuation.
- **Price/chase:** **AMD is ~$548.80 today (range $530.14–558.37)** ([stockanalysis](https://stockanalysis.com/stocks/amd/)) — that is **above the desk entry zone 520.64–526.03 and already past TP1 (542.20)**. So the move has run; **entering now is a chase**, likely >2 ATR from planned entry (the report's own "do not chase if > 2 ATR from entry" guard applies). Mood-aligned: yes. Long/short/wait: **long, but pullback-only**. Actionable now? **No — do not chase.**
- **Decision:** **DO NOT CHASE — re-arm only on a pullback into 520–526** (or a fresh higher-base setup). Confirmed-but-extended; the clean entry is gone for now.

### Candidate 3 — SMH (stocks, B-tier intraday LONG 71.5, triggered) · semis-leader ETF
- **Setup:** B-tier 71.5, triggered. Entry 630.5560–634.0050, invalidation 623.6579, TP1 644.3521. RS +14.14% vs SPY; semis strongest sector. ETF → no earnings risk.
- **Price/chase:** RR-to-TP1 again only ~1.0 (below 1.5). Semis are the leadership sector (risk-on aligned) but SMH is an index expression of the same AMD/NVDA run that is already extended; NVDA "back above $5T" headline = late-stage froth risk. Mood-aligned: yes. Long/short/wait: **long, confirmation-gated**. Actionable: on a retest into the entry zone with SPY/QQQ holding up; avoid if entered stretched.
- **Decision:** **SECONDARY LONG — retest-into-zone only, modest size.** Cleaner-diversified than single-name AMD but same tight-RR + extended-semis caveat. Prefer JPM (different sector) for the primary long to avoid doubling semis exposure.

### Candidate 4 — ETH/USDT (crypto, active B-tier LONG) · best catalyst-backed crypto long-watch
- **Setup:** carry-forward from the crypto cohort (desk data ~3h old). ETH ~$1,817 area, uptrend, was the unusual-volume name (2.33×) with RWA-flow catalyst at 16:24. Now backed by **geopolitical-relief risk-on** (Iran/Hormuz) + BTC two-week high.
- **Catalyst check:** RWA-flow narrative (ONDO/XLM basket) + macro relief; single_source items, consistent. No legal flags.
- **Price/chase:** BTC pinned under $67K → ETH continuation is BTC-gated. Not overextended. Long/short/wait: **long, pullback-only, BTC-gated >$64K**. Chase-risk: low-moderate. Note OI-down character at 16:24 (partly short-covering) → size modestly.
- **Decision:** **LONG-WATCH, pullback-only, BTC-gated >$64K; re-confirm on a fresh crypto report (current data ~3h old).** Best catalyst-backed crypto long.

### Candidate 5 — System integrity: 17 untracked legacy crypto alerts (§F-7 anomaly)
- **Setup:** `detect_untracked_legacy_alerts --since 2026-06-16` → **17 untracked crypto alerts** (ETH/JTO/XLM/WLD/ZRO/INJ/GPS, scalp+intraday+swing, scores 65–76.5) sent to Telegram with **no `proposed_signal`** → they will NOT contribute to PF/winrate/avgR. Count escalated **1 → 14 → 17** across today's slots.
- **Impact:** silent under-counting of crypto B-tier performance; the tracked sample (crypto A/B n=226) is missing these legacy emissions. Not a trading decision — a data-integrity regression.
- **Decision:** **No trade. §14 TODO (recurring, escalating).** Advisory-only run cannot fix — handed to a manual session.

## 8. Best Candidates Ranked

1. **JPM (stocks, A-tier long)** — ACTIONABLE LONG on retest into **328.35–329.46**, invalidation 326.14, modest size (RR-to-TP1 only 1.0). Best stock long; financials/Dow-aligned, RS leader.
2. **SMH (stocks, B-tier long)** — secondary long on retest into **630.56–634.01**, invalidation 623.66; semis leader but extended + tight RR.
3. **ETH (crypto, B-tier long)** — long-watch, pullback-only, **BTC-gated >$64K**; best catalyst-backed crypto idea (data ~3h old → re-confirm).
4. **INJ (crypto, B-tier long)** — long-watch, pullback-only, BTC-gated >$64K (carry-forward RS leader).

**Best long-watch:** JPM (trigger: retest into 328.35–329.46 holding above 326.14, SPY range intact). **Best short-watch:** none clean — trigger would be **failed retest of broken support + BTC losing $64K** on a hawkish FOMC tomorrow. **Best catalyst-watch:** ETH (trigger: pullback into prior zone with BTC reclaiming/holding >$64K and RWA-flow confirmation).

**AMD is NOT ranked actionable** — confirmed but extended (~$548 vs 520–526 zone, past TP1) → chase risk; re-arms only on a pullback into 520–526.

## 9. Avoid / No Trade (this decision window only — never "stop system")

- **AMD chase ~$548** above its 520–526 entry zone / past TP1 542 — wait for a pullback.
- **Chasing SPCX / SpaceX-spillover** (Anysphere M&A momentum is not a desk signal).
- **Overextended crypto:** PORTAL +41.7% (momentum basket, vol only 0.74×), JTO — squeeze/mean-reversion risk.
- **Fresh shorts** in a confirmed risk-on open (crypto shorts PF 0.5 / −3R; stock shorts disfavoured intraday despite season-long +15R).
- **Crypto scalp lane** — worst crypto mode (PF ~0.33, −4R) → prefer intraday/1h framing.
- **Oversizing into tomorrow's FOMC** (Warsh's first, ~97% hold but forward-guidance/dot-plot risk).
- *(Scanning, candidate generation, tracking, and monitors continue in all moods — this is window-level caution, not a system stop.)*

## 10. Main Risks

- **FOMC tomorrow (Wed Jun 17), Warsh's first meeting** — a hawkish guidance/dot-plot surprise flips the long routing risk-off for both classes; today's tape is pre-decision drift.
- **JPM RR-to-TP1 only 1.0 + stock-intraday-longs are the season-long losing bucket (−17R; longs overall −23R)** — the A-tier score does not guarantee edge; confirmation + modest size required.
- **AMD/SMH/NVDA semis are extended** (AMD +130% YTD, "overvalued vs target"; NVDA "back above $5T") — late-stage froth; reversal risk if risk-on fades.
- **Stale-data risk:** crypto desk reports are ~3h old (data 12:15–12:30 UTC) — crypto levels reconciled to live web, but crypto candidate scores should be re-confirmed on the next cycle.
- **Web-source staleness:** search surfaced a Dec-2025 JPM article as if current — verified and rejected; underscores that single search snippets can be mis-dated (handled this run).
- **DeFi-exploit tail** (Thetanuts $2.1M, Humanity Protocol hack, TVL/leverage stress) — background risk-off pressure on thin alts.
- **Catalyst mapping weak (76.5% unmapped)** — symbol resolver under-maps; treat catalyst layer as context only.
- **Ingest CLI result:** see §13 (run post-write; failure logged here if any, non-blocking).

## 11. Action Plan — next 4 hours

1. **JPM:** if price retests **328.35–329.46** and holds above **326.14** with SPY range intact → **long, modest size, target TP1 332.77** (RR ~1.0 → take partials early). Skip if stretched above the zone.
2. **AMD:** **stand down on chase**; set an alert for a pullback into **520–526**; only then consider a long with the same risk-on/SPY-intact conditions.
3. **SMH:** treat as a secondary long on a retest into **630.56–634.01**; do NOT double semis exposure if already long AMD — prefer JPM (financials) for diversification.
4. **Crypto:** watch **BTC $67K (resistance) and $64K (support)**. Long-watch **ETH/INJ on pullbacks, BTC-gated >$64K**; re-confirm scores on the next (fresh) crypto cycle before acting.
5. **All:** **size modest into tomorrow's FOMC**; no fresh shorts; no chasing extended names. Re-check at the 21:30 late-session risk slot.

## 12. Final Verdict per Mode

- **Crypto scalp:** **NO fresh entries** — worst mode (PF ~0.33, −4R); range-capped pre-FOMC. Watchlist only.
- **Crypto intraday:** **Long-watch only** — ETH/INJ on pullbacks, BTC-gated >$64K; prefer exchange-confirmed signals (PF 1.5). Data ~3h old → re-confirm.
- **Crypto swing:** **Hold/long-watch** — risk-on but pinned under $67K into FOMC; no chase.
- **Stocks intraday:** **JPM long actionable on retest** (modest size, tight RR); **AMD do-not-chase / pullback-only**; **SMH secondary**. RS-leader longs with confirmation; no shorts.
- **Stocks swing/invest:** **Long bias, planning** — AMD/JPM C-tier swing/invest active; act off intraday levels, not stale swing triggers; size into FOMC carefully.

## 13. Sources

- [Why Is Bitcoin Going Up Today? BTC Price Eyes $70K Test — FinanceMagnates, 2026-06-16](https://www.financemagnates.com/trending/why-is-bitcoin-going-up-today-btc-price-eyes-70k-test/) — BTC ~$66.4–66.7K, tested $67K, Iran/Hormuz relief, FOMC. *confirms.*
- [Bitcoin and ethereum prices today, June 16, 2026: highest opening values in two weeks — Yahoo Finance, 2026-06-16](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-tuesday-june-16-2026-highest-opening-values-in-two-weeks-113313567.html) — BTC/ETH two-week high. *confirms.*
- [AMD Stock Surges Amid Positive Geopolitical Developments — GuruFocus, 2026-06-16](https://www.gurufocus.com/news/8912543/amd-stock-surges-amid-positive-geopolitical-developments) — AMD up on Iran relief; AI-semis. *confirms (but extended).*
- [Advanced Micro Devices (AMD) Stock Price & Overview — stockanalysis.com, 2026-06-16](https://stockanalysis.com/stocks/amd/) — AMD ~$548.80, range $530.14–558.37 today. *confirms AMD extended above entry zone.*
- [JPM Sued Over $328M Crypto Scam: Compliance Failures Under Spotlight — Yahoo Finance, 2026-06-16](https://finance.yahoo.com/news/jpm-sued-over-328m-crypto-151200917.html) — background JPM headline risk. *weakens (minor, not a fresh driver).*
- [Stock Market Today (June 16, 2026): S&P 500 holds steady ahead of Fed meeting — TheStreet (search summary; URL HTTP 403)](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-16-2026) — tape S&P +0.13% / Dow +0.78% / Nasdaq +0.02% / Russell +0.72%; SpaceX/Anysphere $60B. *confirms tape; fetch blocked, summary only.*
- *Rejected (not used):* Yahoo "Dow slips as JPMorgan slides" — fetched content dated **2025-12-09** (JPM −4% on 2025 credit-card cost warning), NOT today → excluded.

## 14. Fix Requests / TODO

### TODO-untracked-legacy-alerts
- **issue:** Untracked legacy crypto alerts climbing across today's slots (1 → 14 → **17**); Telegram-sent B-tier alerts have no `proposed_signal`, so they never contribute to PF/winrate/avgR — crypto performance is silently under-counted.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-06-16` → "**17 untracked legacy crypto alert(s)**" (ETH/JTO/XLM/WLD/ZRO/INJ/GPS, scalp+intraday+swing, scores 65–76.5).
- **suggested manual fix:** investigate the PART-1 regression — why these alert emissions skip `proposed_signal` creation; backfill signal_ids or suppress the legacy alert path so tracked + emitted sets reconcile.
- **priority:** high
- **first observed:** 2026-06-16 16:24 EEST (escalated by 18:42 EEST)

### TODO-catalyst-mapping-weak
- **issue:** Catalyst symbol mapping persistently weak — 76.5% of events unmapped (null symbol) for multiple consecutive slots; high-importance unmapped tail (DeFi exploits, macro) and known legal names (SMCI/UNH) mis-resolved as `…/USDT`.
- **evidence:** `catalyst_events.jsonl` 2026-06-16: total 2,731, mapped 642, unmapped 2,089 = 76.5%; top unmapped = Humanity Protocol hack / Thetanuts exploit / DeFi TVL stress.
- **suggested manual fix:** improve the catalyst-layer symbol resolver (entity→ticker mapping, handle equities/sector/macro vs crypto-pair namespace; stop forcing `/USDT` on equity tickers).
- **priority:** medium
- **first observed:** recurring (carried from prior slots)

### TODO-stock-intraday-long-bucket
- **issue:** Season-long signal-stats show stock **intraday longs are the worst bucket (PF 0.6, −17R)** and **longs overall −23R** (vs shorts +15R), yet the desk keeps emitting A/B intraday longs (JPM A 80.9, AMD/SMH B) in risk-on. Possible structural mismatch between scoring optimism and realized long-side edge.
- **evidence:** `signal-stats --asset-class stocks`: by-direction long PF 0.4 / −23R, short PF 2.1 / +15R; by-mode intraday PF 0.6 / −17R, swing/invest PF 2.0 / +9R.
- **suggested manual fix:** review whether stock intraday long scoring (regime_alignment + RS weighting) is over-promoting in risk-on; consider an RR-floor (TP1 RR 1.0 is being scored A-tier) and a long/short performance-aware adjustment.
- **priority:** medium
- **first observed:** 2026-06-16 18:42 EEST

### TODO-thestreet-403
- **issue:** TheStreet "stock-market-today" URL returns HTTP 403 to WebFetch on consecutive runs, forcing reliance on the search snippet for the equity tape.
- **evidence:** WebFetch `…june-16-2026` → HTTP 403 (also noted in the 16:24 review).
- **suggested manual fix:** audit/replace TheStreet as a fetch source for the daily tape (e.g. prefer CNBC/Yahoo live-blog URLs that return 200), or whitelist a working equity-tape source.
- **priority:** low
- **first observed:** 2026-06-16 16:24 EEST (recurring)
