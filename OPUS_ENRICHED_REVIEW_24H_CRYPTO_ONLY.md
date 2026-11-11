# Opus Enriched Review — 24H Crypto-Only Run (cycles 1–3 of 12)

**Methodology:** `prompts/llm_review/enriched_market_review_protocol.md` (incl. §14 source-discipline).
**Cycles covered:** 1–3 of 12 (17:49 → 23:03 EEST, 2026-05-30, Saturday).
**Run folder:** `data/scheduled_runs/2026-05-30_24h_crypto_only/`.
**Mode:** advisory only. No auto-trade. No scoring / threshold / agent changes.

> ⚠️ **External web research unavailable for this review** (per §14 — declared up front). All claims below come from internal SQLite + report markdown. No external news / chart / fundamentals lookup was performed; **no confidence upgrades are made on imagined external context**. The "Sources" section at the bottom lists only internal files.

---

## 1. Executive Summary

- **3/12 cycles done**, all green (`ok=9 failed=0` per cycle, telegram=sent). Scheduler healthy.
- **Zero A-tier, zero B-tier across both scalp and intraday in all three cycles.** The only "active" crypto signals are the **two PART 1 backfilled scalp shorts** (BCH, UNI), both already at `tp1_hit` status. Net new actionable from the 24h run so far: **none**.
- **Regime** is firmly **BTC downtrend / ETH range-to-down**, breadth oscillating 48–54% above EMA20. Recommended style per `MarketRegimeAgent`: *"mean reversion or wait for clean breakouts."* Combined with weekend penalties this is a deliberately quiet desk.
- **Strongest names** (ASTER, BNB, WLD, PORTAL, ID, ALGO, FET) are all flagged **`overextended` + `volume_expansion`** → the universal `>2 ATR from EMA20; do not chase` gate is correctly killing them as long entries. This is the system working as intended, not over-filtering.
- **Weakest names** (OPG, NEAR, ZAMA, GENIUS, ALLO) qualify as `short` bias but score in the 30s–46 range — below the B-tier threshold. Some have missing derivatives (no funding/OI), which adds a data-confidence cap.
- **One macro risk-off headline** in the news pipeline: `DxSale drained for $7.3M in BNB Chain liquidity exploit` (Cointelegraph, primary in internal news_items). Not symbol-specific enough to invalidate any pending signal.
- **Net read:** crypto-only weekend run is correctly producing **NO TRADE** because the desk is doing exactly what the protocol asks — no forcing setups in chop, no chasing extended moves. Stats sample is still weak (n=17, PF 1.6 from prior days' tracked signals).

---

## 2. Data Used

**Internal:**
- 3 scalp reports: `2026-05-30_{15-03,17-27,19-51}_scalp_report.md` (run by cycles 1–3).
- 3 intraday reports: `2026-05-30_{15-14,17-38,20-02}_intraday_report.md`.
- `data/scheduled_runs/2026-05-30_24h_crypto_only/scheduler.log` + 3 cycle summaries.
- `proposed_signals` / `signal_outcomes` via `track-signals --all` (146–171 checked per cycle, 8–17 expired per cycle, 0 stopped).
- `signal-stats --asset-class crypto`.
- `detect_untracked_legacy_alerts --since 2026-05-30` → **zero untracked** every cycle.
- Latest LLM packets (`data/processed/llm_analysis_packet.md` — refreshed by cycle 3).

**External (per §14):** **unavailable for this run** — no WebSearch / WebFetch performed. Cannot verify news beyond what's in `news_items` SQLite.

**Unavailable (declared):**
- TradingView / live chart access — `TradingView manual chart check unavailable`.
- Reddit social attention — every cycle hit `403 Blocked` on `r/CryptoCurrency`, `r/Bitcoin`, `r/ethereum`. Social-attention layer is effectively zero this run.
- KOL X/Telegram/Discord — placeholder list, no live notes (flagged in every report).

---

## 3. Cycle-by-cycle landscape

| Cycle | Time (EEST) | Regime (BTC/ETH/breadth) | A-tier | B-tier | Active crypto | New alerts |
|------:|-------------|--------------------------|-------:|-------:|--------------:|-----------:|
| 1 | 17:49 → 18:14 | down / down / 50% | 0 | 0 | 2 (BCH, UNI, both tp1_hit) | 0 |
| 2 | 20:14 → 20:39 | down / range / 48% | 0 | 0 | 2 | 0 |
| 3 | 22:39 → 23:03 | down / down / 53.6% | 0 | 0 | 2 | 0 |

**Across all three cycles:** identical "No A-tier setups found. Do not force a trade." + "No B-tier setups found." in both scalp AND intraday reports. The system is consistent — not flickering between cycles.

**`track-signals` deltas (combined):**
- checked 170 → 171 → 162 → 146 (declines because expired rows leave the active set).
- `tp_hits` constant at 93 (no new TPs hit in this 5h window — the booked tp1_hits are historic).
- `stopped=0` for all three cycles — no signal hit its invalidation this window.
- `expired=0 → 9 → 16 → 8` — old signals from earlier days rolling off as their `validity_window_hours` elapses.

**Crypto stats snapshot (cycle 3, "week" period):**
```
sample=17 (confidence=weak) | triggered=15 / not_triggered=2 | wins=4 losses=5 amb=0
PF=1.6   avgR=0.2   totalR=+3.0
By tier  : tier-B  n=17  PF=1.60  totalR=+3.0
By mode  : scalp  n=11 PF=2.00 totalR=+1.0  |  swing n=2 PF=inf totalR=+6.0 (anecdotal n=2)
           intraday n=4 PF=0.0  totalR=-4.0 (anecdotal n=4)
By dir   : short n=11 PF=1.20 totalR=+1.0  |  long n=6 PF=inf totalR=+2.0 (anecdotal)
```

Sample still **weak** (well under the 30-sample threshold from `SignalTrackingConfig.minimum_sample_for_recommendations`). Interpretation per §9: **anecdotal** for most splits; no rule changes warranted.

---

## 4. Candidate Deep Dives (per §12 format)

The protocol asks for per-candidate deep dives only on A-tier, B-tier, near-promotion C-tier, alerted, or unusual movers. The system produced no A/B; the relevant candidates this run are the **overextended longs that got rejected** and the **shorts that just missed promotion**.

### ASTER/USDT — crypto / scalp / **rejected (overextended)**
- **Internal system view:**
  - momentum score 92.8 (scalp cycle 3) / 100.0 (intraday cycle 3) — top of the leaderboard.
  - 24h `+11.1%`, RS vs BTC `+10.4%`, volume `3.93×`.
  - Derivatives: price↑ + OI↑ (fresh long positioning), funding `5e-05` (neutral), long/short 2.09, crowding `normal` (per Binance) / `elevated` (per Bybit/OKX cross-check).
  - **Rejected** by universal gate: `Price > 2 ATR from EMA20; do not chase. Entry quality is weak because the move is extended. → watchlist only.`
- **External research:** unavailable.
- **Chart verification:** TradingView unavailable; the +11% 24h with 3.9× volume and OI confirming new longs supports the "fresh positioning, monitor crowding" read.
- **Verdict: WATCHLIST.** The rejection is correct — this is exactly the "do not chase a +11% spike" guardrail the protocol asks for. Re-promote only on a pullback to EMA20 with held structure. **Telegram alert: none, none warranted.**

### BNB/USDT — crypto / scalp / **rejected (overextended)**
- **Internal:** scalp 83.2, intraday 99.0. 24h `+11.2%/+12.5%`, volume `1.67–3.13×`, OI 24h `+26.3%`, funding `1.4e-04` (slightly positive), L/S 1.40, crowding `normal` (Binance) / `elevated` (Bybit). Catalyst: **GENIUS HODLer Airdrop announcement (Binance Announcements, primary source)** + counter-bearish **DxSale BNB Chain $7.3M exploit (Cointelegraph)**.
- **External:** unavailable.
- **Chart:** unavailable; the airdrop catalyst + 26% OI add suggests a genuine catalyst-driven move, but the exploit headline is a clear risk-off counter-bid.
- **Verdict: WATCHLIST.** The two news items pull in opposite directions — net "data confidence" is mixed. The system correctly avoided promotion because price is already extended. Re-evaluate only if BNB pulls back into prior breakout zone with the airdrop narrative still intact.

### OPG/USDT — crypto / scalp / **rejected (short, low score)**
- **Internal:** weakest mover (24h `-12.4%`, RS vs BTC `-13.1%`), `bias=short`, score 36.3 (long) / momentum says short. Derivatives: price↓ + OI↑ (fresh shorts pressing), funding `-4.3e-04` (negative → crowded short risk), L/S 0.62.
- **Rejection:** below B-tier threshold; missing breakout/breakdown confirmation; crowded short cap.
- **Verdict: AVOID** (not WATCHLIST — the crowded-short funding + already-down-12% setup is squeeze territory). Per `CRYPTO_SHORTS_AUDIT.md` PART 4 / PART 5 logic, this is exactly the case the system should reject, and it does.

### NEAR/USDT — crypto / intraday / **C-tier watchlist short (score 59.5)**
- **Internal:** 24h `-9.1%`, RS vs BTC `-9.8%`, volume `1.02×` (no expansion), AI narrative is *rising* but NEAR itself is *bleeding against the narrative*. Setup: `failed bounce/retest 2.315–2.333; inv 2.356; TP1 2.266 TP2 2.226`. Risk 35/100 (low). RR-to-TP1 1.84. Conditional, not active.
- **Verdict: WATCHLIST.** Best of the short candidates — has a structural invalidation, RR ≥ 1.8, deterministic setup. But: weekend mode + below-threshold score + no fresh catalyst → NO TRADE this cycle. Re-check next cycle to see if score promotes or setup voids.

### PORTAL/USDT — crypto / scalp / **noted but not a candidate**
- 24h `+46.9% → +57.3%` (across cycles), volume `0.42–0.58×` (LOW — divergent), OI 24h `+182.7%` (extreme), funding `-0.00650` (deeply negative → heavy short crowding). Bybit cross-check confirms negative funding `-0.011`, crowding `elevated`.
- **Internal verdict:** rejected — "more than 2 ATR from EMA20; do not chase" + market regime mixed.
- **Read:** classic squeeze candidate (negative funding + huge OI build on rising price). But entry is impossible — it's already up 57%. **Verdict: AVOID / do not engage.** The system correctly leaves this alone.

---

## 5. Signal Performance Context

- **Active crypto:** only 2 (BCH, UNI — both PART 1 backfilled shorts, both `tp1_hit`). The 24h run has not produced any new actionable signals yet — consistent with the regime + weekend overlay.
- **Outcomes today (run window):** 0 wins booked, 0 losses booked, 0 stops. The 33 expired rows across cycles 1–3 are old swings/intraday from prior days rolling off their validity window — NOT outcomes; they're "no entry happened before expiry."
- **Crypto edge so far:** PF 1.6, totalR +3.0R, but n=17 is **anecdotal**. Won't be reliable until ≥30 unique setups.
- **Direction split:** shorts n=11 PF 1.20 (+1R), longs n=6 PF ∞ but only 2 wins / 0 losses (anecdotal). Too early to call shorts "the working direction" despite the bearish regime.

---

## 6. Best Candidates (passes internal sanity)

**Nothing actionable this window.** The strongest watchlist candidate is **NEAR/USDT short (intraday, score 59.5, C-tier)** — has a clean structural invalidation, RR ≥ 1.8 — but it's below the B-tier promotion threshold and would need either a regime confirmation (BTC breakdown to new lows with held structure) or a score promotion in the next cycle to become actionable.

## 7. Avoid / No Trade

- **All longs on overextended names** (ASTER, BNB, WLD, PORTAL, ID, ALGO, FET) — `>2 ATR from EMA20`, no acceptable pullback yet.
- **Crowded shorts** (PORTAL, OPG) — negative funding + already-pumped/dumped → squeeze trap risk.
- **Anything on MEXC-only** — universal weekend-mode cap (per `weekend_mode.yaml`: weak MEXC-only → cap at C).
- **All crypto longs in BTC/ETH downtrend** until breadth flips above 60% and BTC reclaims local trend.

## 8. Main Risks

- **Sample is still weak (n=17).** Don't read PF 1.6 as edge — read it as "the system is not catastrophically broken."
- **Reddit social-attention layer = 0** every cycle (403). Crowd-attention signal is degraded; you're flying without the social leg.
- **KOL/X live notes** still placeholder. Manual context is empty.
- **External research unavailable for this review** — there could be news the desk isn't catching (e.g. weekend geopolitical headlines). Per §14 we don't pretend otherwise.
- **DxSale BNB-chain exploit** is internally tagged but not yet propagated as a per-symbol risk to BNB (could matter for the BNB watchlist read).
- **Weekend liquidity** is thinner; wide spreads / wash-out wicks more likely. The weekend overlay (A-tier penalty −5, structural-stop preference) is doing the right thing pre-emptively.

## 9. Action Plan (for the remaining 9 cycles)

- **Continue the run as-is.** The scheduler is healthy; no intervention needed.
- **Monitor at cycle 6 (~03:48 EEST) and cycle 9 (~09:48 EEST)** — those are quieter hours; A-tier should be even less likely. Don't be alarmed by NO TRADE consistency.
- **Re-check this enriched review at cycle 9** — by then ~16h of data + any Asia/EU session moves should be in.
- **Manual TradingView verify** if you sit at the desk: NEAR/USDT (best watchlist short), BTC structure (is the downtrend impulsing or grinding?), ETH range bounds.
- **Do NOT** lower scoring thresholds, weekend penalties, or A-tier cutoffs because of "no trades today." That's exactly what the protocol forbids — and the desk producing NO TRADE in chop is correct behavior.
- **Post-run:** when the 24h `FINAL_24H_CRYPTO_ONLY_REVIEW.md` lands, compare actionable count vs cycle 2 of the 2026-05-29 run (which produced 5 stocks A + B). The drop to 0 here is **expected** (weekend, crypto-only, downtrend) — quantify it as a baseline for future weekend runs.

## 10. Final Verdict

| Mode | Verdict (cycles 1–3) |
|------|----------------------|
| Crypto scalp | **NO TRADE** — overextended longs rejected (correct); shorts under threshold or crowded (correct) |
| Crypto intraday | **NO TRADE** — same picture; NEAR is the only watchlist worth watching |
| Crypto swing/invest | not run this cycle (protocol-aligned) |
| Overall | System is **behaving correctly** in a downtrend + weekend regime. Edge is still **unproven** (n<30). PART 1 fix verified live: detector reports zero untracked across all three cycles. |

**Safety statement:** no auto-trade, no scoring/threshold/agent/strategy change, no fabricated data, TradingView unavailable (declared), external research unavailable (declared per §14), Reddit 403 noted, sample size honestly reported as weak.

---

## Sources

External web research was not performed for this review (§14: "If web/news access is entirely unavailable for a run: state 'External web research unavailable' at the top, rely only on internal collected data, and do not upgrade any confidence based on imagined external context.").

**Internal sources used (auditable):**
- `prompts/llm_review/enriched_market_review_protocol.md` (methodology, incl. §14)
- `data/reports/scalp/2026-05-30_15-03_scalp_report.md`
- `data/reports/scalp/2026-05-30_17-27_scalp_report.md`
- `data/reports/scalp/2026-05-30_19-51_scalp_report.md`
- `data/reports/intraday/2026-05-30_20-02_intraday_report.md`
- `data/scheduled_runs/2026-05-30_24h_crypto_only/scheduler.log`
- `data/scheduled_runs/2026-05-30_24h_crypto_only/cycle_0{1,2,3}_summary.md`
- `data/processed/llm_analysis_packet.md` (post-cycle-3 refresh)
- SQLite tables: `proposed_signals`, `signal_outcomes`, `news_items`, `watchlist_alerts`
- Detector: `scripts/detect_untracked_legacy_alerts.py --since 2026-05-30`
- CRYPTO_SHORTS_AUDIT.md (PART 4 / 5 — confirmed live: 0 untracked)
- `config/weekend_mode.yaml` (weekend overlay parameters)

**News claims surfaced internally (single-source per `news_items.verification`):**
- *Introducing Genius Terminal (GENIUS) on Binance HODLer Airdrops* — Binance Announcements (primary_source).
- *DxSale drained for $7.3M in BNB Chain liquidity exploit* — Cointelegraph (single_source).
- *Bitcoin Whales Are Pulling Back as Activity 'Mirrors' 2022 Bear Market: Analysts* — Decrypt (single_source).
- *XRP ETFs add $35 million as bitcoin and ether funds lost $2 billion in late May* — CoinDesk (single_source).
- *Solana open interest drops 30% as altcoins slump* — Cointelegraph (single_source).

URLs for these are stored in `news_items.url` (not all crawled at write time); per §14 the verification level is single_source for all except the Binance announcement — treat accordingly.
