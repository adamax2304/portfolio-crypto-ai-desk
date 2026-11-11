# Opus Enriched Review — post-close final daily review — Auto Cycle 23:31 EEST

## 1. Executive Summary

**Slot: post-close final daily review (advisory only / no auto-trade).** US cash session has closed. Scheduler is fresh (`scheduler.log` 22:57 EEST, ~34m old) — no defer; two `cycle_*_summary.md` files now exist today (cycle_01 18:40, cycle_02 22:57), improving further on the cycle-summary-gap TODO. **Crypto**: regime split by mode — intraday/scalp still read range/chop while the freshest swing scan (22:37 EEST) flipped to **transition (mixed)** with breadth thinning to 33.3%/58.3% (>EMA20/50, down from ~48%/73% four hours earlier) — a real deterioration heading into the Asia session, not noise. Macro/geopolitical risk unchanged at **100/100** (Iran war, oil-tanker economics, Russia drone/missile activity). Zero A-tier crypto all day; book stays structurally 100% long. Weekly headline actionable PF eased to **1.26/+21.9R** (was 1.33-1.39 earlier today) — scalp bucket confirmed the day's clear loser (0 wins / 11 losses, ~-10R). **TUT/USDT and ONG/USDT open-long contradictions remain unresolved for a 4th+ consecutive cycle** — TUT partially bounced (-20.5% latest vs -24.2% mid-cycle) but ONG deepened further (-15.1% vs -11.2% four hours ago), both still "triggered" against invalidations that should have been breached; this is now an end-of-day priority for operator/monitor resolution before Asia. TRUMP/USDT's swing-vs-intraday model disagreement (flagged new at 21:46) is unchanged and still unresolved. **Stocks**: session closed **risk_on** (VIX 14.56, breadth 100% >EMA50); the rolling paper-R drawdown guard again demoted every fresh A/B to C (14d net -5.7R PF 0.39) — **MU's bullish news thesis from the last review evaporated**, its score collapsed from 93.4 to 52.05 (no_directional_setup) this cycle, no longer even reaching a tier. Three new B-tier stocks shorts armed in the last ~2h **not seen in the prior review**: **VRT** (carries a genuine Pomerantz-firm investor-alert legal risk — forces manual review regardless of direction), **CRCL** (a risk-on RS-*leader* being shorted — squeeze-risk setup), and **LLY** (a legacy pre-hardening signal now failing the desk's own current ATR-extension gate, and directly contradicted by today's bullish FDA/Mounjaro cardio-approval news — should not be treated as live). COST's open intraday short remains the one clean, current-hardening-compliant stocks position. Untracked legacy alerts unchanged at **4 today** (MOVR, HEMI×2, CHIP) — same recurring bug. Catalyst mapping unchanged at 70.9% unmapped — **still weak, context only**. Scanning, tracking, and the scheduler continue overnight into Asia regardless of this window's verdict.

## 2. Data Used

- Crypto scalp report: `data/reports/scalp/2026-08-28_17-52_scalp_report.md` (20:52 EEST, ~2h39m old)
- Crypto intraday report: `data/reports/intraday/2026-08-28_18-03_intraday_report.md` (21:02 EEST, ~2h29m old)
- Crypto swing report: `data/reports/swing/2026-08-28_19-37_swing_report.md` (22:37 EEST, ~54m old — **freshest crypto read this cycle**, regime shift noted)
- Stocks intraday report: `data/reports/stocks/intraday/2026-08-28_18-54_stocks_intraday_report.md` (21:54 EEST, ~1h37m old — **fresh**, post-close snapshot)
- Stocks swing/invest reports: both dated 2026-07-02 (~57d stale, deprecated pipeline per `project_crypto_ai_desk_stocks_position_framework` memory, excluded)
- `data/processed/llm_analysis_packet.md` (22:40 EEST), `data/processed/llm_stocks_packet.md` (21:56 EEST) — the stocks packet predates the VRT/CRCL signals (created 21:58/22:54 EEST) but confirms the LLY hardening-exclusion finding
- `data/catalysts/2026-08-28/catalyst_events.jsonl` (2500 rows, direct-counted: 727 mapped/1773 unmapped), `narrative_baskets.jsonl` (5 baskets)
- `reports/CONTEXT_FILTERS_STATUS.md` (21:47 EEST) — paper-routing filter/health status, all clear
- CLI: `active-signals --asset-class crypto` (50 rows), `active-signals --asset-class stocks` (50 rows), `signal-stats --asset-class crypto`, `signal-stats --asset-class stocks`, `detect_untracked_legacy_alerts --since 2026-08-28`
- Direct read-only SQL against `db/crypto_ai_desk.sqlite`: `news_items` (VRT/CRCL/LLY legal/headline check), `proposed_signals` (VRT/CRCL/LLY creation timestamps/thesis)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-28_2146.md`
- **External web research not used this run** — internal reports, catalyst layer, and news_items were sufficient and internally consistent for every candidate reviewed.
- **TradingView / manual chart check unavailable** — all technical reads taken directly from report-stated OHLCV/ATR/EMA/RS fields.

## 3. Scheduler / Data Freshness

- `scheduler.log`: 2026-08-28 22:57 EEST (~34m old) — **fresh**.
- Today's scheduler folder now has **two** `cycle_*_summary.md` files (`cycle_01_15-58` 18:40 EEST, `cycle_02_20-40` 22:57 EEST) — improving further on the carryover TODO (was 1 at 21:46, 0 at 18:39).
- Crypto scalp: 20:52 EEST (~2h39m) — aging but within the mode's normal cadence.
- Crypto intraday: 21:02 EEST (~2h29m) — aging.
- Crypto swing: 22:37 EEST (~54m) — **freshest crypto read this cycle**; used for §6 market landscape in preference to the older scalp/intraday snapshots.
- Stocks intraday: 21:54 EEST (~1h37m) — fresh, captures the post-close snapshot (data freshness 18:53 UTC = 21:53 EEST).
- Stocks swing/invest: 2026-07-02 — stale, deprecated pipeline, excluded.
- `reports/CONTEXT_FILTERS_STATUS.md` (21:47 EEST): `context_filters_v1` **LOCKED**; stablecoin depeg NORMAL; cross-exchange consistency OK (BTC/ETH FULL_SIZE); all context-source health checks `ok`/`ok_provisional` except `stocks_options_import` (`disabled_no_current_file`, non-blocking, unchanged). No reduce-only / paper-blocking condition active.
- No monitor-process-uptime file was read this run (not in the allowed CLI/read list).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "post_close",
  "as_of": "2026-08-28 23:31 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["scalp/intraday crypto snapshots ~2.5h old vs a fresher swing scan available"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 22:57 EEST", "two cycle_*_summary.md files now present today (up from one)", "swing report 22:37 EEST is the freshest crypto read this cycle"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.72,
      "reason_codes": ["mixed", "chop", "risk_on", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing regime flipped to transition (mixed), breadth 33.3%/58.3% (>EMA20/50), down from ~48%/73% four hours earlier", "macro risk 100/100 unchanged", "stocks closed risk_on, VIX 14.56, breadth 100% >EMA50, 3/4 indices uptrend"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["stale_catalyst", "mapping_weak", "narrative_supported", "fresh_catalyst", "catalyst_contradicted"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["70.9% unmapped in catalyst_events.jsonl, unchanged", "SOL/USDT fresh primary-source Schwab catalyst reinforces existing open swing long", "LLY short directly contradicted by today's bullish FDA/Mounjaro cardio-approval news", "no legal/headline risk found for CRCL; VRT carries a genuine Pomerantz investor-alert legal risk"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "funding_extreme", "data_unavailable"],
      "data_missing": ["no OI/derivatives read for TUT/USDT or for any stocks symbol this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ONG/USDT negative funding across venues (bybit 1.25e-05, mexc -0.001538), crowding elevated — supports the bias=short tag against the open long", "CRCL short is tagged RS=leader in a risk_on regime — a classic squeeze-prone short (shorting the market's own leader)"] },
    { "agent": "technical_entry", "verdict": "bad", "confidence": 0.72,
      "reason_codes": ["entry_late", "price_moved_away", "stale_before_entry", "overextended", "chase_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TRUMP/USDT swing-vs-intraday model disagreement carried forward unchanged (intraday score 50.8 C-tier watchlist vs open B-tier swing waiting-entry 2.7908-2.8422)", "LLY short fails the desk's own current ATR-extension hardening gate (2.60 > max 2.00) yet remains armed as a legacy pre-hardening signal", "DEXE/USDT still overextended, do-not-chase flag persists", "TUT/USDT >2 ATR from EMA20, watchlist-only technical read"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review", "closed_flat"],
      "data_missing": ["exhaustive book count beyond the 50-row CLI sample per asset class"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto 50-row sample: TUT/ONG/EDEN/COST-equivalent OPEN actionable (triggered/running), TRUMP/DEXE/RE WAITING for entry, several TP1/TP2-hit partial wins today (HEMI tp2_hit, PROM tp1_hit)", "stocks: COST OPEN actionable (triggered short), VRT/CRCL/LLY WAITING for entry (2 new since 21:46, 1 legacy-excluded), DXCM/AMZN/IWM/KLAC CLOSED WIN today (tp1/tp2_hit)"] },
    { "agent": "risk_manager", "verdict": "bad", "confidence": 0.82,
      "reason_codes": ["manual_review", "correlation_cluster", "reduce_risk", "daily_loss_pressure", "legal_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TUT/USDT open long still 'triggered' for a 4th+ consecutive cycle despite invalidation almost certainly breached", "ONG/USDT bias-tag contradiction deepened this cycle (-15.1% latest vs -11.2% four hours ago), derivatives-confirmed, escalated HIGH since 2026-08-08", "VRT short carries a genuine Pomerantz-firm securities investor-alert — legal/headline risk forces manual review regardless of direction", "crypto book still 100% long, 0 audited shorts", "end-of-day timing raises urgency of TUT/ONG resolution before crypto becomes the only live asset class overnight"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["playbook_failing", "low_sample", "playbook_working"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto scalp weekly: 0 wins, 11 losses, ~-10R over 14d — the day's clear structural loser, confirmed again", "crypto intraday/swing weekly buckets remain net-positive (PF ~1.3-1.5)", "stocks A/B headline sample=13 (up from 11), winrate 75%, PF=inf — still too small to trust as proof", "stocks C-tier sample=589, PF 0.40, winrate 8% — losing bucket, guard rationale holds"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.68,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "manual_review",
    "confidence": 0.68,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "SOL/USDT", "trigger": "already-open triggered swing long (entry ~96.0-96.6), reinforced by a fresh primary-source Schwab-platform catalyst; no contradicting risk tags — hold, do not add fresh size overnight" },
    "best_short_candidate":    { "symbol": "TUT/USDT", "trigger": "not an audited short setup, only a bias/failed-bounce tag (>2 ATR from EMA20) — confirm bearish HTF structure + volume before promoting; the open LONG contradiction on this same symbol takes priority over any new short" },
    "best_catalyst_candidate": { "symbol": "SOL/USDT", "trigger": "same as best-long — Schwab crypto-platform listing plus State-of-Solana platform launch and ETF-inflow tailwind (20%-pullback historical caveat noted)" },
    "avoid_candidate":         { "symbol": "TUT/USDT", "reason": "open long unresolved for a 4th+ consecutive review cycle against a still-deep 24h collapse; needs operator/monitor resolution before Asia, not a new position either direction" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.75 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.72 | mixed, chop, risk_on, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.60 | stale_catalyst, mapping_weak, narrative_supported, fresh_catalyst, catalyst_contradicted | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk, funding_extreme, data_unavailable | advisory_only |
| technical_entry | bad | 0.72 | entry_late, price_moved_away, stale_before_entry, overextended, chase_risk | advisory_only |
| execution_lifecycle | caution | 0.70 | open_actionable, waiting_for_entry, needs_review, closed_flat | advisory_only |
| risk_manager | bad | 0.82 | manual_review, correlation_cluster, reduce_risk, daily_loss_pressure, legal_risk | advisory_only |
| playbook_performance | caution | 0.75 | playbook_failing, low_sample, playbook_working | advisory_only |
| head_trader | caution | 0.68 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-28_2146.md`:
- **New this cycle — three stocks B-tier shorts armed, none seen at 21:46:** VRT (score 71.2, created 22:54 EEST), CRCL (score 82.7, created 21:58 EEST), LLY (score 68.8, created 21:50 EEST — the oldest of the three, present but not yet armed/visible at 21:46). All three are `waiting_for_entry`, all three carry a flag: VRT has a genuine legal/headline risk (Pomerantz investor alert), CRCL is an RS-*leader* being shorted in a risk-on regime (squeeze-prone), and LLY is a legacy pre-hardening signal that **fails the desk's own current ATR-extension gate** (2.60 > max 2.00) and is directly contradicted by today's bullish FDA/Mounjaro news.
- **New this cycle — MU's thesis evaporated:** the 21:46 review's highest-scoring stocks idea (MU, 93.4, genuinely bullish Micron-rival/Nvidia-margin news) collapsed to score 52.05 / `no_directional_setup` / rejected this cycle — the bullish news context no longer produces even a C-tier read.
- **Deepened — ONG/USDT:** 24h move worsened from -11.16%..-14.91% (21:46 window) to -15.12% on the freshest (22:37) swing snapshot — the open long contradiction is not just persisting, it is getting worse.
- **Eased then re-checked — TUT/USDT:** 24h move improved slightly to -20.47% on the freshest swing snapshot (was -20.99%..-24.16% at 21:46); still "triggered," still unresolved for a 4th+ consecutive cycle.
- **Unchanged — TRUMP/USDT model disagreement:** no new information since 21:46; the intraday watchlist score (50.8) and swing waiting-entry zone (2.7908-2.8422) still disagree.
- **Unchanged — untracked alerts:** still 4 today (MOVR, HEMI×2, CHIP), no new ones this cycle.
- **Improved — cycle summary artifact:** today's scheduler folder now has **two** `cycle_*_summary.md` files (was one at 21:46, zero at 18:39) — continued partial resolution.
- **Unchanged — catalyst mapping:** 70.9% unmapped, identical to 21:46 (no fresher catalyst cycle file ran in the interim).
- **Regime shift — crypto swing:** the freshest swing scan (22:37) reads market regime as **transition (mixed)** with narrowing breadth (33.3%/58.3%), versus the range/chop read used at 21:46 (from an older snapshot) — a genuine deterioration into the close, not a data artifact (breadth has been falling steadily across today's cycles: ~54%/77% mid-day → ~48%/73% at 21:46 → 33.3%/58.3% now).
- **Confirmed wins today (no action needed):** HEMI/USDT tp2_hit, PROM/USDT tp1_hit (×2 signals), DXCM tp1_hit, AMZN tp2_hit, IWM tp2_hit, KLAC tp2_hit — genuine daily closes, none require operator input.

## 5. Catalyst Coverage

- `catalyst_events.jsonl` (2026-08-28, direct count): **2500 total, 727 mapped (29.1%), 1773 unmapped (70.9%)**. **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Unchanged from the 21:46 review (no fresher catalyst-cycle file has run since `catalyst_cycle_18-19.md`).
- Top unmapped headlines (macro/political noise, not symbol-mapping regressions): "JAPAN SHOULD NOT RAID ITS FOREX RESERVES..." (macro/FX); "JUDGE BLOCKS KEY PARTS OF TRUMP-BACKED RULE... MAIL-IN VOTING..." (US politics, near-duplicate across sources); "PHILIPPINE PESO FALLS AS MUCH AS 0.6%..." (macro/FX).
- `narrative_baskets.jsonl` (5 baskets, fresh <1h-<6h): rwa_narrative (ONDO/XLM), binance_ecosystem_teaser (BNB), ai_narrative (NEAR/RENDER/TAO/FET), perps_dex_narrative (HYPE/DYDX/GMX), momentum_breakout (DEXE/EDEN — no confirmed catalyst).
- Legal/regulatory items today (REGN, PLAB, CCOI, GDDY, ByHeart, and now VRT via direct `news_items` query) — VRT's Pomerantz investor alert is the only one mapping to a live proposed-signal candidate this cycle; verified via direct SQL, dated 2026-08-27T22:11 UTC.

## 6. Market Landscape

**Crypto** (freshest read: swing report, 22:37 EEST / 19:30 UTC data): regime **transition (mixed)**, altcoin breadth 33.3% >EMA20 / 58.3% >EMA50 — materially narrower than both the mid-day (~54%/77%) and 21:46-review (~48%/73%) snapshots; this is a real, steady deterioration through the day, not a single-cycle blip. Macro/geopolitical risk unchanged at 100.0/100 (Iran war, oil-tanker economics, Russia drone/missile activity, Bessent-Warren yen-intervention friction). Strongest (swing): DEXE (93.7, +18.98% 24h, still overextended/chase-risk), EDEN (91.6, +15.94%), HEMI (90.9, +15.97%), PROM (88.4, +7.34%). Weakest/short-tag list (swing): TUT (-20.47%, contradicts an open long), ONG (-15.12%, contradicts an open long, deepening), OPG (-10.39%), MOVR (-8.99%).

**Stocks** (intraday report, 21:54 EEST — post-close snapshot, 18:53 UTC data): regime **risk_on**, bias long, VIX 14.56 (calm), breadth 75% >EMA20 / 100% >EMA50, 3/4 indices trending up. Rolling paper-R drawdown guard remains active (14d net -5.7R PF 0.39, per-direction: long -4.7R/PF0.26/n36, short -1.0R/PF0.67/n19) and continues to demote every fresh A/B candidate to C — 15 raw-A candidates today (MSFT, NFLX, ADBE, CRM, NOW, UBER, INTU, ABNB, AFRM, PANW, CRWD, DXCM, CRCL, AAPL, CMCSA), all demoted to C by the guard, legal-risk, stale-earnings, or RR-floor gates. 0 actionable A/B after gates this cycle (0 raw, 0 gate-demoted-from-B — nothing new even reached the gate). Genuinely live/current positions: **COST** (open intraday short, `rr_to_tp1` 2.92, structural TP1, current-hardening-compliant) and three newly-armed but flagged shorts (VRT, CRCL, LLY — see §7).

### Market Mood / Risk Routing

- Crypto mood: **mixed / transition**, deteriorating breadth (narrowing steadily through the day), macro risk-off overlay unchanged, no clean RS-leader long left unflagged
- Stocks mood: **risk-on** at the close, but the guard suppresses actionability regardless and today's three fresh short candidates all carry a flag (legal, squeeze, or hardening-exclusion)
- Dominant narrative: momentum-breakout (DEXE/EDEN/HEMI, no confirmed catalyst) on crypto; RWA/AI-sector/perps-DEX baskets simmering; on stocks, no fresh clean actionable narrative — every raw-A idea gate-demoted
- Preferred side now: **mixed, cautious into the Asia handoff** — crypto: hold existing catalyst-backed long (SOL), do not chase TRUMP at either quoted zone, resolve TUT/ONG before anything new; stocks: no new risk this late, COST short is the only clean carry
- Best long candidate: SOL/USDT (already open, catalyst-reinforced, hold only — not a fresh entry)
- Best short candidate: none clean — TUT/USDT is the best short-*watch* bias tag, subordinate to resolving the open long on the same symbol; CRCL is a short but flagged as RS-leader-in-risk-on squeeze risk, not a clean short
- Best catalyst-backed candidate: SOL/USDT (crypto, already-open swing long, Schwab-platform catalyst)
- What to avoid: new entries on TUT/USDT or ONG/USDT in either direction; treating VRT/CRCL/LLY as clean actionable shorts (legal risk / squeeze risk / hardening-exclusion respectively); chasing DEXE/USDT (+19-26% 24h depending on report, overextended); any stocks-intraday C-tier signal; any brand-new stocks risk this close to end-of-day
- What would change the view: operator resolution of TUT/USDT and ONG/USDT; a fresh catalyst-cycle file narrowing the mapping gap; the stocks 7d/14d cohort turning positive to lift the guard; TRUMP/USDT's two model reads converging; crypto breadth stabilizing or reversing its decline into Asia

## 7. Candidate Deep Dives

### 1. TUT/USDT (crypto, **open long contradiction — priority risk, 4th+ consecutive cycle unresolved**, swing, B-tier score 69.2)
- Signal: `sig_c7ce9835f38c40a8`, status **triggered** (ENTERED, unresolved final outcome), entry 0.051638-0.052505, invalidation 0.050579, expires 2026-09-03.
- Has price already reacted? Yes — 24h -20.47% on the freshest (19:30 UTC) swing snapshot, a partial improvement from -24.16% mid-cycle but still far beyond the ~2% invalidation buffer below entry.
- Retest/pullback structure? None stated on the long side; watchlist-only short read persists (>2 ATR from EMA20, score 26.6-44.5 depending on report).
- Aligned with market mood? No — the open long remains unreconciled with the price action against it, now into a 4th+ cycle.
- Long, short, or wait-for-trigger? **Manual review required**, unchanged — this reads as a monitor/outcome-recording gap (was the stop hit and simply not recorded?), not a new-information question.
- What would invalidate it? Already should be invalidated per stated levels.
- Catalyst confirmation or contradiction? None found for TUT/USDT this cycle either.
- Derivatives: no OI/funding read available for TUT this cycle (`data_unavailable`).
- **Urgency**: this needs operator/monitor resolution before the Asia session, where crypto becomes the only live asset class.

### 2. ONG/USDT (crypto, open swing long, escalated manual-review carryover, **deepening this cycle**)
- Signal: `sig_8d3a8fd71bf0bf75`, triggered 2026-08-26, invalidation 0.09240 — still ENTERED UNRESOLVED.
- This cycle's freshest (swing, 19:30 UTC) reading: 24h -15.12%, **worse** than the -11.16%..-14.91% seen across the 21:46 review's reports — the bias=short tag against this open long is not just persisting, it is strengthening.
- Derivatives support the bearish tag: negative funding across venues (bybit 1.25e-05, mexc -0.001538), crowding elevated — the 5th+ consecutive review to find the open long unreconciled with a derivatives-confirmed bearish read.
- Escalated HIGH since 2026-08-08 per prior memory; no new information beyond the deepening contradiction.

### 3. VRT (stocks, **new B-tier short, legal/headline risk — do not treat as clean actionable**)
- Signal (proposed_signals): tier B, score 71.23, direction short, status `waiting_for_entry`, entry zone 258.14-259.99, invalidation 261.85, created 2026-08-28T19:54 UTC (22:54 EEST — very recent), expires 2026-08-29T19:54 UTC.
- Thesis: intraday short, downtrend, RS=follower, regime risk_on.
- **LEGAL/HEADLINE RISK confirmed via direct `news_items` query**: "INVESTOR ALERT: Pomerantz Law Firm Investigates Claims On Behalf of Investors of Vertiv Holdings Co - VRT" (PR Newswire (Stocks), 2026-08-27T22:11 UTC). This is a securities-investigation notice, not yet a filed class action, but per §I discipline it still forces the verdict.
- Actionable now or after confirmation? **Not a clean actionable regardless of guard state** — legal/headline risk on a stocks A/B candidate mandates `AVOID` or `MANUAL REVIEW REQUIRED`, never a clean pass, independent of the direction the risk happens to point.
- What would invalidate it? Not applicable in the normal sense — this is a manual-review gate, not a price-level question. Would need operator confirmation the investor alert is immaterial/stale before this could be treated as a normal short.

### 4. CRCL (stocks, **new B-tier short, RS-leader-in-risk-on squeeze risk**)
- Signal (proposed_signals): tier B, score 82.68, direction short, status `waiting_for_entry`, entry zone 87.06-88.04, invalidation 89.01, created 2026-08-28T18:58 UTC (21:58 EEST), expires 2026-08-29T18:58 UTC.
- Thesis: intraday short, downtrend, **RS=leader**, regime risk_on.
- This is the setup most worth a second look, not because it is clean but because it is structurally unusual: shorting a stated RS-*leader* while the desk's own regime read is risk-on is exactly the squeeze-prone combination flagged elsewhere in this review for crypto (ONG). No legal/headline risk found for CRCL this cycle (only neutral/mixed Chelsea-sponsorship and a modest price-target trim).
- Actionable now or after confirmation? Treat as **manual review** — confirm the RS-leader tag isn't stale and that a genuine bearish trigger (not just mean-reversion hope) is present before arming.

### 5. LLY (stocks, **legacy B-tier short — fails current hardening, catalyst-contradicted, do not treat as live**)
- Signal (proposed_signals): tier B, score 68.78, direction short, status `waiting_for_entry`, created 2026-08-28T18:50 UTC (21:50 EEST), expires 2026-08-29T18:50 UTC.
- Thesis: intraday short, downtrend, RS=laggard, regime risk_on.
- Per `data/processed/llm_stocks_packet.md` §"Legacy open A/B excluded by new hardening": **this exact signal is explicitly excluded by the desk's current ATR-extension gate** (`atr_extension 2.60 > max 2.00`) — it was armed under an older, looser gate and never re-validated against the current rule.
- **Catalyst contradiction confirmed via direct `news_items` query**: today carries genuinely bullish LLY news — "FDA approves Lilly's Mounjaro (tirzepatide) to reduce cardiovascular risk in adults with type 2 diabetes" (multiple sources, 2026-08-28) — directly opposing a short thesis.
- Actionable now or after confirmation? **No** — double-flagged (gate-failing + catalyst-contradicted); should not be treated as a live signal regardless of its `waiting_for_entry` status in the armed-watch table.

## 8. Best Candidates Ranked

1. **TUT/USDT** (manual review, urgent, 4th+ cycle) — open long contradicting a still-deep 24h collapse; resolve before Asia.
2. **ONG/USDT** (manual review, escalated, deepening) — open long, derivatives-confirmed bias-tag contradiction worsening this cycle.
3. **VRT** (stocks, manual review — legal risk) — genuine Pomerantz investor-alert forces non-actionable regardless of direction.
4. **LLY** (stocks, avoid — gate-failing + catalyst-contradicted) — legacy pre-hardening signal that fails the desk's own current rule and fights today's bullish FDA news.
5. **CRCL** (stocks, manual review — squeeze risk) — shorting a stated RS-leader in a risk-on regime; confirm before arming.
6. *(excess, listed for completeness)* **SOL/USDT** (catalyst-watch, already open, reinforced) — clean hold, no new action; **TRUMP/USDT** (reconcile, unchanged carryover) — two live model reads still disagree.

## 9. Avoid / No Trade (this decision window only)

- **TUT/USDT — new entries either direction.** Open long needs operator resolution first.
- **ONG/USDT** — no new long or short action pending operator resolution; contradiction deepening.
- **VRT short** — genuine legal/headline risk (Pomerantz investor alert); manual review required regardless of guard state.
- **LLY short** — fails the desk's own current ATR-extension hardening AND is contradicted by today's bullish FDA news; do not treat the armed `waiting_for_entry` status as live.
- **CRCL short** — RS-leader-in-risk-on squeeze setup; confirm before treating as clean.
- **Chasing DEXE/USDT at market** — +19-26% 24h depending on report window, overextended.
- **New crypto scalp entries** — 0 wins / 11 losses this week, ~-10R, the day's clear structural loser.
- **Acting on the open TRUMP/USDT waiting-entry zone (2.7908-2.8422) as if it were the cleanest read** — unresolved model disagreement, unchanged.
- **Any stocks-intraday C-tier signal treated as actionable** — all 15 raw-A ideas today were gate-demoted; none are Telegram-actionable.
- This is a decision-window verdict only — scanning, candidate generation, tracking, and the scheduler continue in all cases; nothing here recommends pausing any part of the system.

## 10. Main Risks

- **TUT/USDT open long, unresolved for a 4th+ consecutive review cycle** — invalidation almost certainly breached; urgency rising into the Asia handoff.
- **ONG/USDT bias-tag contradiction, deepening this cycle** (-15.12% vs -11.16% four hours ago), derivatives-confirmed, escalated HIGH since 2026-08-08.
- **Three flagged stocks shorts armed in the last two hours** (VRT legal risk, CRCL squeeze risk, LLY gate-failing+catalyst-contradicted) — none should be treated as clean fills if triggered overnight/pre-market without a fresh manual check.
- **Crypto breadth steadily deteriorating through the day** (~54%/77% → ~48%/73% → 33.3%/58.3% >EMA20/50) — worth watching into the Asia open for a broader regime confirmation, not yet a full risk-off call.
- **Crypto book remains 100% long, 0 audited shorts** — concentration risk if BTC/ETH break the current range down.
- **Crypto scalp the day's clear structural loser** (0 wins / 11 losses this week, ~-10R) — unchanged conclusion, worsening slightly.
- **Catalyst mapping still weak** (70.9% unmapped), flat vs the last two reviews — no fresher catalyst-cycle file has run.
- **4 untracked legacy crypto alerts today** (unchanged) — known recurring bug, TODO escalated HIGH 2026-07-17.
- **A gate-integrity gap**: legacy pre-hardening signals (LLY) can remain armed in the watch table after failing the desk's own current rules — worth a structural fix, not just a one-off flag (see §14).

## 11. Action Plan — next 4 hours (overnight into Asia)

- Escalate TUT/USDT for immediate operator/monitor check: confirm whether the position was actually stopped out and not recorded, now a 4th+ cycle unresolved.
- Escalate ONG/USDT alongside TUT — the contradiction is deepening, not just persisting; treat both as one operator task given the shared urgency into Asia.
- Do not treat VRT, CRCL, or LLY as clean fills if they trigger overnight — each needs a manual check (legal alert materiality for VRT, RS-leader/squeeze confirmation for CRCL, re-validation against the current ATR-extension gate for LLY) before being acted on.
- Hold SOL/USDT's existing swing long; catalyst thesis reinforced, no new action needed.
- No new crypto scalp entries (0 wins / 11 losses this week).
- Watch COST's open intraday short overnight; no fresh operator input needed unless a stop/target is hit.
- Re-check TUT/ONG resolution status, the untracked-alert count, and whether crypto breadth stabilizes or continues falling at the next cycle (04:30 EEST overnight/Asia review).
- No new stocks-intraday risk this close to end-of-day regardless of score.

## 12. Final Verdict per Mode

- **Crypto scalp:** aging (~2h39m); weekly 0 wins/11 losses, ~-10R — scanner continues, no new entries.
- **Crypto intraday:** aging (~2h29m); TRUMP/USDT model disagreement unchanged; no new A/B setups beyond the existing book.
- **Crypto swing:** freshest crypto read (~54m); regime flipped to transition (mixed), breadth narrowing; TUT/USDT and ONG/USDT need urgent manual review; SOL/USDT hold, reinforced.
- **Stocks intraday:** fresh (~1h37m), 0 A/B actionable after gates; COST short remains the one clean current position; VRT/CRCL/LLY armed but flagged, not clean.
- **Stocks swing:** stale (2026-07-02) — excluded, deprecated pipeline.
- **Stocks invest:** stale (2026-07-02) — excluded, deprecated pipeline.

## 13. Sources

- Internal: `data/reports/swing/2026-08-28_19-37_swing_report.md`, `data/reports/intraday/2026-08-28_18-03_intraday_report.md`, `data/reports/scalp/2026-08-28_17-52_scalp_report.md`, `data/reports/stocks/intraday/2026-08-28_18-54_stocks_intraday_report.md`, `data/processed/llm_analysis_packet.md`, `data/processed/llm_stocks_packet.md`, `data/catalysts/2026-08-28/catalyst_events.jsonl`, `data/catalysts/2026-08-28/narrative_baskets.jsonl`, `reports/CONTEXT_FILTERS_STATUS.md`, `db/crypto_ai_desk.sqlite` (`news_items`, `proposed_signals` tables, direct read queries).
- CLI: `active-signals --asset-class crypto`, `active-signals --asset-class stocks`, `signal-stats --asset-class crypto`, `signal-stats --asset-class stocks`, `detect_untracked_legacy_alerts --since 2026-08-28`.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-28_2146.md`.
- News items cited (all `published_at` present, no invented dates): "INVESTOR ALERT: Pomerantz Law Firm Investigates Claims On Behalf of Investors of Vertiv Holdings Co - VRT" (PR Newswire (Stocks), 2026-08-27T22:11 UTC); "FDA approves Lilly's Mounjaro (tirzepatide) to reduce cardiovascular risk..." (PR Newswire (Stocks) / Finnhub, 2026-08-28); Circle/Chelsea FC sponsorship coverage (t.me/wublockchainenglish, CryptoBriefing, Finnhub, 2026-08-28).
- No external WebSearch/WebFetch performed this run — internal sources were sufficient and consistent for every candidate.

## 14. Fix Requests / TODO

### TODO-tut-invalidation-unresolved (carryover, escalating — 4th+ cycle)
- **issue:** Open swing long `sig_c7ce9835f38c40a8` (TUT/USDT, entry 0.051638-0.052505, invalidation 0.050579) still shows status `triggered` for a 4th+ consecutive review cycle, despite 24h prints of -20.47% to -24.16% across today's reports — an invalidation buffer of only ~2% below entry means price is almost certainly through it.
- **evidence:** `active-signals --asset-class crypto` row `sig_c7ce9835f38c40a8`; `data/reports/swing/2026-08-28_19-37_swing_report.md` ("TUT/USDT: bias short, 24h -20.47%"); flagged at 18:39, 16:15, 21:46, and now 23:31.
- **suggested manual fix:** a human-driven session should query the exact current TUT/USDT price and the position monitor's state directly, confirm whether the stop was actually hit and simply not yet recorded as a `signal_outcome`, and if so investigate why the monitor didn't close/record it. Now spanning into the Asia session — treat as time-sensitive.
- **priority:** high
- **first observed:** 2026-08-28 18:39 EEST (escalating; still open at 23:31 EEST)

### TODO-ong-invalidation-deepening (carryover, escalating)
- **issue:** Open swing long `sig_8d3a8fd71bf0bf75` (ONG/USDT, triggered 2026-08-26, invalidation 0.09240) remains tagged bias=short, and the contradiction **deepened** this cycle (-15.12% vs -11.16% four hours ago) rather than easing.
- **evidence:** `active-signals --asset-class crypto` row `sig_8d3a8fd71bf0bf75`; `data/reports/swing/2026-08-28_19-37_swing_report.md` ("ONG/USDT: bias short, 24h -15.12%"); derivatives confirm (negative funding across bybit/mexc, elevated crowding); escalated HIGH since 2026-08-08 per prior memory (`project_crypto_ai_desk_bias_tag_contradiction`).
- **suggested manual fix:** same as TUT — verify against live price/monitor state whether invalidation was breached and not recorded.
- **priority:** high
- **first observed:** 2026-08-08 (recurring; deepening as of 2026-08-28 23:31 EEST)

### TODO-legacy-gate-integrity (new)
- **issue:** LLY short (`created 2026-08-28T18:50 UTC`, tier B, `waiting_for_entry`) is explicitly listed in `data/processed/llm_stocks_packet.md` under "Legacy open A/B excluded by new hardening" (`atr_extension 2.60 > max 2.00`) — i.e., the desk's own tooling already knows this signal fails its current rule — yet it remains armed and visible as a normal `waiting_for_entry` B-tier signal in `active-signals`, indistinguishable from a current-hardening-compliant signal like COST.
- **evidence:** `data/processed/llm_stocks_packet.md` §"Legacy open A/B excluded by new hardening"; `active-signals --asset-class stocks` row for LLY (`sig_2096268d07a77e20`); `proposed_signals` table direct query (`created_at 2026-08-28T18:50:55`).
- **suggested manual fix:** a human-driven session should decide whether legacy pre-hardening signals that fail a *newer* gate should be auto-expired/auto-flagged in `active-signals` output (not just noted in the LLM packet's advisory section) so future review cycles don't have to cross-reference the packet to catch this.
- **priority:** medium
- **first observed:** 2026-08-28 23:31 EEST

### TODO-catalyst-window-gap (carryover, unchanged)
- **issue:** `data/catalysts/2026-08-28/catalyst_events.jsonl` unmapped rate flat at 70.9% since the 21:46 review — no fresher catalyst-cycle file has run to improve it further today.
- **evidence:** direct read of `catalyst_events.jsonl` (727/2500 mapped, unchanged); no new `catalyst_cycle_*.md` file since `catalyst_cycle_18-19.md` (21:19 EEST).
- **suggested manual fix:** unchanged from prior reviews — check whether the catalyst-cycle pipeline should be running more frequently late in the day, and whether mapped/unmapped % should be computed from the latest `catalyst_cycle_*.md` instead of the full-day jsonl.
- **priority:** medium
- **first observed:** 2026-08-28 18:39 EEST (still flat, not worsening)

### TODO-cycle-summary-gap (carryover, improving)
- **issue:** Today's `data/scheduled_runs/2026-08-28_default_schedule/` folder now has **two** `cycle_*_summary.md` files (`cycle_01_15-58` 18:40 EEST, `cycle_02_20-40` 22:57 EEST) — improving further from one at 21:46 and zero at 18:39, but still low relative to the 5+ distinct scalp/intraday report timestamps generated today.
- **evidence:** `ls data/scheduled_runs/2026-08-28_default_schedule/*cycle*` — two files; compare against 5+ scalp reports and 5+ intraday reports generated today.
- **suggested manual fix:** a human-driven session should confirm whether cycle-summary generation cadence now matches the scheduler's actual cycle count, or if it is still lagging behind the report-generation cadence.
- **priority:** low
- **first observed:** 2026-08-28 18:39 EEST (downgraded from "missing" to "partial, improving" across successive cycles)

### TODO-untracked-alerts-recurring (carryover, still open, unchanged)
- **issue:** 4 untracked legacy crypto alerts today (MOVR/USDT 12:03, HEMI/USDT 14:39 + 15:28, CHIP/USDT 15:28) — same recurring watchlist-alert/signal-reuse bug escalated to HIGH priority 2026-07-17 (project memory: `project_crypto_ai_desk_watchlist_alert_signal_reuse_bug`). No new alerts since the 21:46 review.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-28` output (identical to the 21:46 review's run).
- **suggested manual fix:** see prior TODO — investigate why these alerts reuse a stale/closed `signal_id` instead of minting a new `proposed_signal`.
- **priority:** high
- **first observed:** 2026-07-17 (recurring; observed again 2026-08-28 23:31 EEST)
