# Opus Enriched Review — Crypto Overnight / Asia Review — Auto Cycle 04:40 EEST

## 1. Executive Summary

**Crypto overnight / Asia review, 04:40 EEST.** **Advisory only — no auto-trade.** No A-tier setups anywhere (scalp/intraday/swing) this cycle — consistent with the day's pattern. Regime stays **downtrend/chop**: BTC downtrend, ETH range, altcoin breadth ~52.6% above EMA20 — external check corroborates (BTC pinned near $63K needing $64K reclaim, ETH stuck below $1,900–1,922). Macro risk elevated (81.5/100) on Coldcard BTC-wallet exploit follow-through and Iran/Strait-of-Hormuz tension. **Headline finding this cycle: the previously-flagged stale-OHLCV/false-"OPEN" defect (5 consecutive prior reviews, symbols HOLO/BMT/MUBARAK) is confirmed still present — and is now shown to be materially wider than previously reported.** Direct OHLCV inspection found **13 of the 50 active crypto signals (26%)** — including today's two highest-scoring "new" swing triggers, THE/USDT and MUBARAK/USDT (both scored 74.7) — are running on a price feed frozen at **2026-08-15 22:30–23:00 UTC**, i.e. **~27–30 hours stale**, while liquid pairs (WLFI, CHIP, ADA, ONG, ETHFI, PORTAL) refresh normally (~15 min lag). This means the day's two best-looking B-tier swing entries cannot currently be trusted and are downgraded to **NEEDS REVIEW**, not clean actionable. A second, distinct lifecycle bug: PORTAL/USDT's scalp signal shows `waiting_for_entry` ~2h **past its own `expires_at`**, with fresh price now ~13% above the entry zone — it should have auto-expired to NO-ENTRY/MOVED-AWAY. Clean, fresh-data candidates: **CHIP/USDT** (best long — RS+OI confirmation, no catalyst) and **ADA/USDT** (best short — fresh data, catalyst/price divergence: bullish Cardano ecosystem news but price falling, a bearish continuation tell). Catalyst-watch: **SOL/USDT** (Bitwise/Superstate staking-ETF tokenization talk, no live signal yet). Catalyst mapping is weak this run (51.8% unmapped) — use catalyst layer as context only. Stocks closed (planning-only); 20 fresh C-tier intraday watchlist ideas queued for the US open, none actionable pre-market.

**External web research used this cycle** (BTC/ETH overnight price context) — corroborates internal downtrend/chop read; see §13.

## 2. Data Used

- Scheduler: `data/scheduled_runs/2026-08-16_default_schedule/scheduler.log` — fresh (mtime 04:32 EEST, ~8 min old); latest `cycle_03_00-32_summary.md` (mtime 02:30 EEST, ~2h10m old). Both well under the 3h defer threshold.
- Reports: scalp `2026-08-16_22-10` (generated 01:10:52 EEST, ~3.5h old), intraday `2026-08-16_22-51` (generated 01:51 EEST, ~2h50m old), swing `2026-08-16_15-42` (generated 18:42 EEST, ~10h old — **carry-forward**, no fresher swing scan ran overnight), stocks intraday `2026-08-16_23-16` (02:16 EEST, fresh but market closed — planning-only), stocks swing/invest `2026-07-02` (six weeks stale — expected/deprecated, per prior project context, not investigated further).
- Catalysts: `data/catalysts/2026-08-16/catalyst_events.jsonl` (1,077 cumulative events, mtime 01:55 EEST), `narrative_baskets.jsonl` (5 baskets, same mtime). This is the active "today" folder (scheduler run started 2026-08-16, still current — `2026-08-17/` does not exist yet, expected).
- LLM packets: `llm_analysis_packet.md` fresh (01:51 EEST), `llm_stocks_packet.md` fresh (02:17 EEST).
- CLI: `active-signals` (crypto n=50, stocks n=50 all C-tier `waiting_for_entry` fresh from the 23:15 EEST stocks-intraday cycle), `signal-stats` (crypto: n=92 stronger-confidence, PF 3.25, totalR +31.5; stocks: n=595 reliable but PF 0.17/totalR −10 over a stale/degraded C-tier-only sample — not actionable), `detect_untracked_legacy_alerts --since 2026-08-17` → **clean**, no untracked alerts.
- Direct OHLCV CSV timestamp checks (`data/raw/ohlcv/binance/15m/*.csv`) across the full active-signals book — the primary diagnostic this cycle (see §3).
- `reports/PAPER_MONITOR_STATUS_LATEST.md` (mtime 02:26 EEST) — cross-checked against raw OHLCV for HOLO/BMT/MUBARAK.
- Prior review for comparison: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-16_2329.md` (post-close final daily review, 23:29 EEST).
- **External web research run this cycle** (1 WebSearch: BTC/ETH price context for Aug 17 2026) — corroborates internal regime read, does not contradict.

## 3. Scheduler / Data Freshness

- Scheduler: **fresh**, cycle 3 completed 02:30 EEST (~2h10m old, well under 3h defer threshold).
- Scalp: **fresh** (~3.5h, weak sample). Intraday: **fresh** (~2h50m). Swing: **carry-forward** (~10h, still the latest snapshot). Stocks intraday: **fresh** (~2h20m) but market closed, planning-only. Stocks swing/invest: **stale** (6 weeks, expected/deprecated).
- Catalyst folder: fresh (1,077 cumulative events, mtime 01:55 EEST), 5 narrative baskets, mapping **weak** (51.8% unmapped — see §5).
- **Monitor/price-feed integrity: CONFIRMED DEGRADED and WIDER than previously scoped.** Raw OHLCV timestamp check (binance 15m) across all 50 active crypto signals:
  - **Severely stale (~27–30h, frozen at 2026-08-15 22:30–23:00 UTC), currently shown OPEN/TRIGGERED:** HOLO/USDT, BMT/USDT, MUBARAK/USDT (the original 3, unchanged since the 23:29 review — **6th consecutive cycle**), plus **newly confirmed** in the same frozen state: THE/USDT, PEOPLE/USDT, BANANAS31/USDT, TST/USDT (swing), AVNT/USDT, PROM/USDT (×2 signals), LUNA/USDT, MMT/USDT, BABY/USDT. **13 of 50 active crypto signals (26%) affected.**
  - `PAPER_MONITOR_STATUS_LATEST.md` still displays HOLO/BMT/MUBARAK as `🟢 OPEN — entry filled, monitoring TP/SL`, which cannot be trusted given the frozen price feed.
  - Control check: liquid/fresh pairs (WLFI, CHIP, ONG, ETHFI, PUMP, ADA, HOME, PORTAL, ZEC, KAITO, ALLO) all refresh normally, last candle ≤15–20 min old — this is a **pair-specific fetch failure, not a global outage**.
  - `BABY/USDT` — the prior review reported this symbol had "resolved" to `CLOSED FLAT 0R`; raw OHLCV for BABY_USDT is **still frozen at the same 2026-08-15 22:30 UTC timestamp**, so that resolution likely came from an expiry-timeout close path, not from a genuinely fresh price read. The underlying fetch defect for this symbol is not actually fixed.
  - **Second, distinct defect:** PORTAL/USDT scalp signal (`sig_3d9797eb42e0d678`, score 66.3, entry zone 0.015028–0.015985) has `expires_at=2026-08-17T02:51:44`, already **~2h in the past**, but status is still `waiting_for_entry`. Its own OHLCV is fresh (current price ~0.0169, ~13% above the entry zone) — this is a **status-transition bug** (failure to auto-expire past-window signals), separate from the OHLCV-freshness bug above.
- `detect_untracked_legacy_alerts --since 2026-08-17`: **clean**.
- See §14 TODO-1 (raised to **critical**, scope widened) and TODO-2 (new).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-08-17 04:40 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "bad", "confidence": 0.9,
      "reason_codes": ["scheduler_fresh", "report_stale", "onchain_config_missing", "catalyst_missing"],
      "data_missing": ["stocks swing/invest 6wk stale (expected)", "on-chain whale flows not connected", "OI 24h% n/a for several MEXC-fallback symbols"],
      "suggested_effect": "advisory_only",
      "facts_used": ["13/50 active crypto signals on frozen OHLCV (2026-08-15 22:30-23:00 UTC)", "scheduler fresh 8min", "6th consecutive cycle with this defect"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["chop", "risk_off", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC downtrend, ETH range, breadth 52.6%/47.4%", "external: BTC ~$63K needs $64K reclaim, ETH stuck <$1900-1922", "macro risk 81.5/100"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"],
      "data_missing": ["THE/MUBARAK/BMT/PEOPLE/PORTAL/CHIP/WLFI/ONG/ETHFI/PENGU: zero internal catalyst hits"],
      "suggested_effect": "advisory_only",
      "facts_used": ["1077 events, 51.8% unmapped", "SOL: fresh Bitwise/Superstate staking-ETF news", "ADA: 25 news hits, price falling despite ecosystem updates (bearish divergence)"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.4,
      "reason_codes": ["data_unavailable", "funding_extreme"],
      "data_missing": ["OI 24h% n/a for several MEXC-fallback symbols", "no live squeeze/crowding feed beyond per-symbol funding snapshot"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTW extreme long crowding (unrelated to active book)", "CHIP/WLFI: price up + OI up, normal crowding"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["entry_late", "stale_before_entry", "price_moved_away"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PORTAL scalp: price ~13% above entry zone, past expiry", "CHIP/WLFI/ADA: fresh triggered, in-book"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["entered_unresolved", "needs_review", "waiting_for_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["50 active crypto signals: 1 waiting_for_entry, 25 triggered, 15 tp1_hit, 9 tp2_hit", "13 of these on frozen OHLCV -> needs_review", "PORTAL past-expiry still waiting_for_entry"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.8,
      "reason_codes": ["manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["26% of active crypto book running on a broken price feed -> P&L/TP/SL for those symbols not trustworthy", "macro risk 81.5/100", "BTC exploit operator-review warning still open"] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.65,
      "reason_codes": ["playbook_working", "low_sample"],
      "data_missing": ["scalp sample weak (n=18)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["tier=B PF 3.25 n=92", "swing PF 5.37 n=49 stronger", "intraday PF 1.37 n=25 weak", "stocks C-tier PF 0.17 reliable-but-losing"] },
    { "agent": "head_trader", "verdict": "manual_review", "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": { "symbol": "CHIP/USDT", "trigger": "already triggered (swing+intraday), hold structure above 0.0270 support / RS+OI confirmation intact", "reason": "fresh OHLCV, price up + OI up, no catalyst but clean RS/momentum, swing PF 5.37 cohort" },
    "best_short_candidate": { "symbol": "ADA/USDT", "trigger": "already triggered (swing short, entry 0.1869-0.1876), invalidation 0.1884", "reason": "fresh OHLCV, catalyst/price divergence (bullish Leios-testnet news, price still falling) = weak demand tell, BTC downtrend regime favors shorts" },
    "best_catalyst_candidate": { "symbol": "SOL/USDT", "trigger": "no live signal yet — watch for a swing/intraday setup to trigger on confirmation of the Bitwise/Superstate staking-ETF tokenization story", "reason": "single_source but primary-adjacent, fresh <6h, no proposed_signal yet" },
    "avoid_candidate": { "symbol": "THE/USDT and MUBARAK/USDT (today's two highest-score new triggers)", "reason": "both running on OHLCV frozen since 2026-08-15 22:30-23:00 UTC (~28h stale) — entry/TP/SL levels cannot be trusted until the fetch defect is fixed; treat as NEEDS REVIEW, not actionable" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | bad | 0.90 | scheduler_fresh, report_stale, onchain_config_missing, catalyst_missing | advisory_only |
| market_regime | caution | 0.75 | chop, risk_off, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.40 | data_unavailable, funding_extreme | advisory_only |
| technical_entry | caution | 0.55 | entry_late, stale_before_entry, price_moved_away | advisory_only |
| execution_lifecycle | caution | 0.70 | entered_unresolved, needs_review, waiting_for_entry | advisory_only |
| risk_manager | caution | 0.80 | manual_review, reduce_risk | advisory_only |
| playbook_performance | ok | 0.65 | playbook_working, low_sample | advisory_only |
| head_trader | manual_review | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

- **New (confirmed):** stale-OHLCV defect scope widened from 3 symbols (HOLO/BMT/MUBARAK) to **13 confirmed** — THE, PEOPLE, BANANAS31, TST, AVNT, PROM (×2), LUNA, MMT, BABY added. This is the same underlying defect, now shown to be materially larger.
- **New:** PORTAL/USDT scalp status-transition bug (past-expiry signal not auto-closing) — first time flagged.
- **New triggers since 23:29 review:** THE, MUBARAK, BMT, PEOPLE, TST, PENGU, BANANAS31, CYS swing signals all show `triggered` with expiry timestamps around 02:43–02:52 EEST — but at least 6 of these 8 sit on the frozen-OHLCV list, so their "freshness" is questionable; treat as NEEDS REVIEW rather than genuinely new confirmations.
- **Not new:** no A-tier anywhere (unchanged all day). Market regime unchanged (downtrend/chop). Catalyst mapping still weak (~50%).
- **Correction to prior review:** the 23:29 review's claim that BABY/USDT "resolved" the stale-data defect is likely a false negative — BABY's OHLCV is still frozen at the same timestamp; its status change was probably an expiry-timeout close, not a genuine fresh-price resolution.

## 5. Catalyst Coverage

- Total catalyst events (cumulative, `data/catalysts/2026-08-16/`): **1,077**. Mapped (symbol present): **519** (48.2%). Unmapped: **558** (51.8%).
- Narrative baskets: **5** — rwa_narrative, binance_ecosystem_teaser, ai_narrative, momentum_breakout, plus one additional.
- **Catalyst mapping weak this run (51.8% unmapped) — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines: "Pope calls for an end to West Bank violence against Palestinians" (Reuters); "Family Dental Care Experts... cosmetic dental" (HelloNation, clearly off-topic noise); "$10,000 in NuScale at Its 52-Week High Is Worth About $1,650 Today" (unmapped despite naming a tradeable symbol — resolver miss).
- None of today's active crypto candidates (CHIP, WLFI, ONG, ETHFI, PENGU, THE, MUBARAK, BMT, PEOPLE, PORTAL) have a mapped catalyst event. ADA has 25 mapped hits (Cardano Leios testnet, ecosystem updates) — notable divergence: price falling despite the good news.

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **chop, risk-off-leaning** (BTC downtrend, ETH range, breadth ~52.6%/47.4%, macro risk 81.5/100)
- Stocks mood: **closed** (pre-market, no fresh RTH data; 20 fresh C-tier intraday ideas queued for the open)
- Dominant narrative: none decisively fresh — meme heat mixed (30.6/100), AI/RWA/L2/Gaming all "quiet"; SOL staking-ETF tokenization is the closest thing to a live narrative thread
- Preferred side now: **wait-for-trigger, lean shorts on confirmation** (BTC downtrend regime, but no clean breakdown yet — chop caps conviction either way)
- Best long candidate: CHIP/USDT (fresh data, RS+OI confirmed, already triggered)
- Best short candidate: ADA/USDT (fresh data, catalyst/price divergence, already triggered)
- Best catalyst-backed candidate: SOL/USDT (watch — no live signal yet)
- What to avoid: THE/USDT, MUBARAK/USDT, and the other 11 frozen-OHLCV symbols (BMT, PEOPLE, BANANAS31, TST, AVNT, PROM, LUNA, MMT, BABY, HOLO) — data integrity failure, not a market call
- What would change the view: BTC reclaiming $64K + ETH reclaiming $1,900–1,922 (risk-on flip); a confirmed clean breakdown below BTC's recent range low (risk-off confirmation, favors shorts); the stale-OHLCV defect being fixed (would restore trust in THE/MUBARAK/BMT/PEOPLE tier)

## 7. Candidate Deep Dives

### 1. Data Integrity Cluster — THE/USDT, MUBARAK/USDT, BMT/USDT, PEOPLE/USDT, BANANAS31/USDT, TST/USDT, AVNT/USDT, PROM/USDT, LUNA/USDT, MMT/USDT, BABY/USDT, HOLO/USDT (13 signals, 26% of active crypto book)

- **Status: NEEDS REVIEW** (not a trade call — a data-integrity call).
- Evidence: raw `binance/15m` OHLCV for all 13 symbols is frozen at 2026-08-15 22:30:00–23:00:00 UTC (~27–30h stale as of this review), while 37 other active-book symbols refresh normally (≤20 min lag).
- Has price already reacted to anything? Unknown — the desk cannot see current price for these symbols.
- Is this chasing / actionable now? No — cannot verify entry, invalidation, or TP levels against live price.
- What would make it actionable again? The OHLCV fetch path for these specific pairs resuming normal 15m cadence; a manual operator spot-check against exchange price before trusting any TP/SL/PnL display for these symbols.
- Aligned with market mood? Not assessable — no live price.
- Legal/headline risk: none flagged beyond the general macro risk items.
- This is the same defect flagged in the 02:00, 18:49, 21:39, 23:29 reviews (originally 3 symbols) — now confirmed wider. See TODO-1.

### 2. CHIP/USDT — LONG (best long candidate)

- Status: **OPEN actionable** (triggered, swing sig_781f738640222db5 score 69.0 + intraday sig_616042a3e9294e9f score 65.8), fresh OHLCV (last candle 2026-08-17 01:30 UTC, ~14 min old).
- Has price reacted to a catalyst? No catalyst found internally (0 hits) — pure RS/momentum/derivatives setup: "price up + OI up: fresh positioning confirms trend," funding near-zero, crowding normal.
- Chasing? 24h return was ~7.4% at last report generation (01:10–01:51 EEST); not vertical, OI confirms it's not just a wick.
- Retest/pullback structure? Entry zone 0.028775–0.029561 (swing); already triggered, no fresh pullback needed.
- Overextended? Not flagged in the report (setup quality 69–75/100 range typical for this cohort).
- Actionable now or wait? Already open; monitor for TP1/TP2 or invalidation at 0.027815 (swing) / 0.026896 (intraday).
- Mood alignment: mixed — chop regime generally favors caution on longs, but this is an isolated RS-leader long in a fusion-momentum symbol, not a beta bet on the whole tape.
- Chase risk: low (already triggered, not a fresh chase decision).
- Catalyst confirmation/contradiction: none — pure technical/momentum thesis.

### 3. ADA/USDT — SHORT (best short candidate)

- Status: **OPEN actionable** (triggered, swing sig_8b60893020d24644, score 65.3), fresh OHLCV (last candle 01:30 UTC).
- Has price reacted to the catalyst? Yes, and this is the notable part: 25 mapped news hits including "Cardano Launches Leios Testnet, ADA Price Falls Despite Major Ecosystem Updates" — genuinely bullish fundamental news, but price continuing to fall. This is a **bearish divergence / weak-demand tell**, which supports rather than contradicts the short thesis.
- Chasing? No — short was triggered on a breakdown setup (setup=breakdown cohort, direction=short).
- Retest structure? Entry zone 0.186906–0.187594, invalidation 0.188434 (tight risk, ~0.8% stop).
- Overextended? Not flagged.
- Actionable now or wait? Already open; monitor invalidation at 0.188434.
- Mood alignment: strong — BTC downtrend regime + risk-off macro (81.5/100) favors shorts; ADA underperforming despite good news reinforces the read.
- Chase risk: low.
- Catalyst confirmation/contradiction: **catalyst_contradicted** — good news, weak price action. Flagged for the derivatives_squeeze/catalyst_narrative agents as a genuine signal, not noise.
- Caveat: `setup=breakdown` cohort has a weak/anecdotal sample overall (n=9, PF 1.07) per signal-stats — treat conviction as moderate, not high.

### 4. SOL/USDT — CATALYST-WATCH (best catalyst-backed candidate, no live signal)

- Status: **WATCH ONLY** — no active `proposed_signal` for SOL in the current book.
- Catalyst: "Bitwise mulls tokenizing its Solana staking ETF via Superstate partnership" (The Block, fresh <6h per report §5b) plus 8 mapped catalyst_events hits (staking/ETF/Grayscale scarcity projections theme).
- Has price already reacted? Not assessed this cycle — no OHLCV/technical read was run for SOL since it has no active signal; would need a fresh scan pass.
- What would make it actionable? A swing or intraday proposed_signal triggering on SOL with RS confirmation vs BTC, ideally with the staking-ETF narrative basket still fresh (<6h window).
- Verification status of the catalyst: single_source (The Block) — reputable but not yet corroborated by a second outlet; treat as narrative-supported, not catalyst-confirmed.
- Chase risk: n/a (no entry proposed yet).

### 5. PORTAL/USDT — scalp signal, lifecycle anomaly

- Status: shown `waiting_for_entry` (sig_3d9797eb42e0d678, score 66.3) but `expires_at=2026-08-17T02:51:44` is **~2h in the past**. Fresh OHLCV shows current price ~0.0169, roughly 13% above the entry zone (0.015028–0.015985).
- Correct status per PART-16 lifecycle vocabulary: **NO-ENTRY / STALE / MOVED AWAY** — price moved away before entry was reached and the window has closed.
- Root cause guess (not verified, needs operator check): the status-transition job that marks past-expiry `waiting_for_entry` signals as expired/no-entry did not run or did not match this signal.
- Separately, scalp mode carries a kill-switch note this cycle ("crypto_scalp_disabled (kill-switch: mode off, any hour/day)") on several §7b rejected candidates — worth confirming this is intentional and not itself masking the transition bug.
- Not aligned with any trade decision — flagged as a second, smaller data-integrity item. See TODO-2.

## 8. Best Candidates Ranked

1. **CHIP/USDT — LONG** (already open, fresh data, RS+OI confirmed) — best actionable long this window.
2. **ADA/USDT — SHORT** (already open, fresh data, catalyst-divergence bearish tell, BTC downtrend regime alignment) — best actionable short this window.
3. **SOL/USDT — catalyst-watch** (no live signal; trigger = a fresh swing/intraday proposed_signal on SOL with RS confirmation while the staking-ETF narrative basket is still <6h fresh).
4. **WLFI/USDT — long-watch, secondary** (two triggered swing signals, fresh OHLCV, scores 67.5/69.1, no catalyst) — same cohort as CHIP but lower conviction (funding negative on one leg, "shorts may be crowded" caveat).
5. **THE/USDT and MUBARAK/USDT — NEEDS REVIEW, not ranked as tradeable** despite highest raw scores (74.7 each) — excluded from ranking pending the stale-OHLCV fix.

## 9. Avoid / No Trade

- **This decision window only** — never a command to stop the system; scanning, tracking, and outcome recording continue as normal.
- **Avoid:** THE/USDT, MUBARAK/USDT, BMT/USDT, PEOPLE/USDT, BANANAS31/USDT, TST/USDT (swing leg), AVNT/USDT, PROM/USDT, LUNA/USDT, MMT/USDT, BABY/USDT, HOLO/USDT — all on frozen OHLCV, entry/TP/SL cannot be trusted until the fetch defect is confirmed fixed by an operator.
- **Avoid:** PORTAL/USDT scalp entry — price has moved ~13% above the entry zone; do not chase.
- **Caution, not avoid:** crypto scalp mode generally — several §7b candidates show a kill-switch note this cycle; low-confidence cohort anyway (PF 3.7 but n=18, "weak" confidence label).
- **Caution:** stocks — closed, all candidates are pre-market planning only; do not treat any C-tier stocks idea as actionable before RTH confirmation (per stocks-intraday hardening: C-tier is never actionable regardless of session).

## 10. Main Risks

1. **Data integrity — 26% of the active crypto book on a frozen price feed.** Highest-priority risk this cycle; directly compromises trust in today's two best-scoring new signals (THE, MUBARAK) and in the paper P&L/TP-SL display for 13 symbols. See TODO-1.
2. **Status-transition bug** — at least one past-expiry signal (PORTAL) not auto-closing to NO-ENTRY. If systemic, could be masking other stale `waiting_for_entry` signals across the book. See TODO-2.
3. Macro risk elevated (81.5/100): Coldcard BTC exploit follow-through (Galaxy Research estimates up to ~2,055 BTC stolen across multiple waves, still under operator-review flag per §5c) and Iran/Strait-of-Hormuz tension.
4. Catalyst mapping weak (51.8% unmapped) — the catalyst layer is directionally useful but should not be the deciding factor for any candidate this cycle.
5. Scalp mode: weak-confidence cohort (n=18) with a kill-switch note on several candidates this cycle — treat as data-collection only, not a source of ideas right now.
6. `setup=breakdown` cohort (relevant to the ADA short) is thin (n=9, PF 1.07, "anecdotal") — moderate conviction only, size accordingly in paper tracking.

## 11. Action Plan — next 4 hours

- **Operator (manual, outside this automated run):** spot-check exchange price for HOLO/BMT/MUBARAK/THE/PEOPLE/BANANAS31/TST/AVNT/PROM/LUNA/MMT/BABY against the frozen local OHLCV; if confirmed still broken, treat this as a data-pipeline incident, not a market read, per §14 TODO-1.
- **Operator:** check why PORTAL/USDT's `waiting_for_entry` signal did not transition past its `expires_at`; check whether other symbols share this pattern.
- **Desk (no action needed, system continues automatically):** keep tracking CHIP/USDT and ADA/USDT toward their existing TP/SL levels; keep watching SOL/USDT for a fresh signal on the staking-ETF narrative; keep the 20 stocks C-tier ideas queued for RTH confirmation at the US open.
- **Next review (11:30 EEST, Europe/pre-US context):** re-check whether the stale-OHLCV defect is resolved; re-verify THE/MUBARAK's tradability; confirm whether BTC/ETH broke out of the current range overnight.

## 12. Final Verdict per Mode

- **Crypto scalp:** No trade — kill-switch noted on several candidates this cycle, weak-confidence cohort, PORTAL entry has moved away. Data collection only.
- **Crypto intraday:** No A/B setups this cycle (watchlist-only ideas below threshold). CHIP/USDT intraday leg already open — hold/monitor.
- **Crypto swing:** Mixed — CHIP/WLFI/ADA/ONG/ETHFI legs on fresh data are hold/monitor as normal; THE/MUBARAK/BMT/PEOPLE/BANANAS31/TST/AVNT/PROM/LUNA/MMT/BABY legs are **NEEDS REVIEW**, do not size up or trust displayed P&L until the OHLCV defect is resolved.
- **Stocks intraday:** Planning-only — market closed, 20 fresh C-tier ideas queued, none actionable until RTH confirmation per the C-tier-never-actionable rule.
- **Stocks swing/invest:** No trade — legacy modes deprecated, data 6 weeks stale as expected.

## 13. Sources

- [Crypto Price Prediction August 17, 2026: Bitcoin, Ethereum and XRP Face Key Support Levels as Traders Await Breakout Signals](https://sundayguardianlive.com/business/crypto-price-prediction-august-17-2026-bitcoin-ethereum-and-xrp-face-key-support-levels-as-traders-await-breakout-signals-262800/) — Aug 17 2026, corroborates BTC ~$63K/needs $64K, ETH stuck <$1,900-1,922, thin/cautious range regime.
- Internal: `data/catalysts/2026-08-16/catalyst_events.jsonl` (1,077 events) — ADA Leios-testnet news, SOL Bitwise/Superstate staking-ETF item, BTC Coldcard exploit updates (t.me/CoinMarketCapAnnouncements, primary_source).
- Internal: `reports/PAPER_MONITOR_STATUS_LATEST.md` (mtime 02:26 EEST) and raw `data/raw/ohlcv/binance/15m/*.csv` — primary evidence for the stale-OHLCV finding (direct file inspection, not modeled).

## 14. Fix Requests / TODO

### TODO-1: Stale OHLCV / false-"OPEN" defect — scope widened to 13 symbols, 6th consecutive cycle
- **issue:** binance 15m OHLCV fetch frozen at 2026-08-15 22:30–23:00 UTC for at least 13 symbols in the active crypto book (HOLO, BMT, MUBARAK, THE, PEOPLE, BANANAS31, TST, AVNT, PROM, LUNA, MMT, BABY — plus the monitor still reports HOLO/BMT/MUBARAK as green/OPEN). Other pairs refresh normally, so this is pair-specific, not a global outage. First flagged 02:00 EEST today for 3 symbols; now confirmed present in the 18:49, 21:39, 23:29, and this 04:40 review, and materially wider each time it's been re-checked.
- **evidence:** `data/raw/ohlcv/binance/15m/{HOLO,BMT,MUBARAK,THE,PEOPLE,BANANAS31,TST,AVNT,PROM,LUNA,MMT,BABY}_USDT.csv` last row all dated 2026-08-15 22:30:00+00:00 or 23:00:00+00:00; control symbols (WLFI, CHIP, ONG, ADA, ETHFI, PUMP, HOME, PORTAL, ZEC, KAITO, ALLO) last row 2026-08-17 01:15:00–01:30:00+00:00. `reports/PAPER_MONITOR_STATUS_LATEST.md` lines ~144/155/159 still show these as `🟢 OPEN`.
- **suggested manual fix:** identify why the OHLCV ingest job silently stopped updating these specific symbols ~2026-08-15 22:30 UTC (rate limit? symbol-list drift? exchange-side listing issue?) while others in the same batch continued; add an automated staleness alarm (e.g. flag any active-signal symbol whose latest OHLCV candle is >2h behind the freshest candle in the same batch) so this doesn't require manual cross-file diffing to catch; audit whether any of today's newly-triggered swing signals (THE, MUBARAK, etc.) were scored/entered using this stale price data, which would mean their entry/invalidation/TP levels are themselves unreliable, not just their current display.
- **priority:** critical (raised from high — confirmed 6th consecutive cycle, scope quadrupled from 3 to 13 symbols, now directly contaminating today's top-scoring new signals).
- **first observed:** 2026-08-17 02:00 EEST (3 symbols); scope confirmed widened 2026-08-17 04:40 EEST (13 symbols).

### TODO-2: Signal status not transitioning past expires_at (PORTAL/USDT scalp)
- **issue:** `sig_3d9797eb42e0d678` (PORTAL/USDT scalp, score 66.3) has `expires_at=2026-08-17T02:51:44`, already ~2h in the past at review time, but `status` is still `waiting_for_entry` in `active-signals` output. Price has moved ~13% above the entry zone in the meantime — this should have been auto-marked NO-ENTRY/expired.
- **evidence:** `python -m src.cli active-signals --asset-class crypto` row for `sig_3d9797eb42e0d678`; `data/raw/ohlcv/binance/15m/PORTAL_USDT.csv` last row 2026-08-17 01:30:00+00:00 price ~0.0169 vs entry_high 0.015985.
- **suggested manual fix:** check the job responsible for closing out past-expiry `waiting_for_entry` signals (likely the same "track-signals" or pending-monitor step); verify it is actually querying/updating this signal_id; check whether this is isolated or affects other scalp signals whose short expiry windows may be getting missed by the monitor's cadence.
- **priority:** medium (does not affect currently-open positions' P&L, but could let stale watchlist items linger and confuse the active-signals view).
- **first observed:** 2026-08-17 04:40 EEST.

### TODO-3 (carried forward, unrelated): untracked-alert / signal-reuse bug
- **issue:** per prior project memory, watchlist re-fires have previously reused a stale/closed `signal_id` instead of minting a new `proposed_signal` (confirmed on ALLO/USDT and BANK/USDT in an earlier session).
- **evidence:** this cycle's `detect_untracked_legacy_alerts --since 2026-08-17` came back clean, so no new instance was observed this run — carrying forward as a watch item, not re-flagging as newly confirmed.
- **suggested manual fix:** no action needed this cycle; keep running the detector each review.
- **priority:** high (per prior escalation; unchanged, not re-verified this cycle).
- **first observed:** 2026-07-17 (prior session).
