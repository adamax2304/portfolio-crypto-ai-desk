# Opus Enriched Review — Post-Close Final Daily Review — Auto Cycle 23:29 EEST

## 1. Executive Summary

**Post-close final daily review, 23:29 EEST (nearest fired slot to 23:15).** **Advisory only — no auto-trade.** No A-tier setups anywhere today (scalp/intraday/swing, crypto or stocks) — consistent all day. Stocks were closed all session (Sunday); no fresh stocks data beyond Friday's carry-forward. Crypto closed a **net-positive day**: PORTAL/USDT (swing) hit **TP3** and HEMI/USDT (intraday) hit **TP3**, against one loss (DOLO/USDT swing **stopped**) — in line with the weekly B-tier edge (PF 3.08, n=99 reliable). Regime stays downtrend/risk-off-leaning chop into the close (BTC downtrend, ETH range, macro risk ~67–70/100 on persistent Iran/Strait-of-Hormuz tension), so no fresh entries are being pushed overnight. The recurring finding worth operator attention: the **stale-OHLCV / false-"OPEN"** defect on HOLO/USDT, BMT/USDT, MUBARAK/USDT (flagged in the 02:00, 18:49 and 21:39 reviews) is **still present** — 5th consecutive cycle — though BABY/USDT (previously also stuck) has since correctly resolved to CLOSED FLAT, showing the fetch path recovers for some pairs but not others. Overnight-into-Asia: no clean new long/short; watch ALICE/USDT (RS + short-covering) and ACE/USDT (weak-RS short, squeeze-capped) for confirmation, SOL/USDT for the single-source Bitwise/Superstate staking-ETF catalyst.

**External web research used this cycle** (BTC/ETH price context, Coldcard exploit status) — both corroborate internal data; see §13.

## 2. Data Used

- Scheduler: `data/scheduled_runs/2026-08-16_default_schedule/scheduler.log` — fresh (mtime 22:32 EEST, ~57 min old); latest `cycle_02_20-48_summary.md` (mtime 22:32). Both well under the 3h defer threshold.
- Reports: scalp `2026-08-16_18-28` (generated 21:28:54 EEST, fresh), intraday `2026-08-16_19-08` (generated 22:08:32 EEST, fresh), swing `2026-08-16_15-42` (generated 18:42:07 EEST, ~5h old — carry-forward, borderline-stale band but still the latest swing snapshot this weekend), stocks intraday `2026-08-14_20-09` (Friday close, market closed Sunday — planning-only), stocks swing/invest `2026-07-02` (six weeks stale — **not a fresh defect**: per prior project context these legacy stocks swing/invest modes were intentionally deprecated in favor of the new shadow-only `stocks_swing_growth_breakout` framework, so this staleness is expected, not investigated further).
- Catalysts: `data/catalysts/2026-08-16/catalyst_events.jsonl` (692 events today cumulative, latest cycle file `catalyst_cycle_19-12.md`, mtime 22:12 EEST), `narrative_baskets.jsonl` (5 baskets, same mtime).
- LLM packet: `data/processed/llm_analysis_packet.md` fresh (22:09 EEST). `llm_stocks_packet.md` stale (Aug 14, expected — weekend).
- CLI: `active-signals` (crypto n=50, stocks n=50), `signal-stats` (crypto: headline sample=99 reliable, PF 3.08, totalR +33.2; stocks: headline sample=8 anecdotal, PF 0.0, totalR −1.0 — too small/stale to act on), `detect_untracked_legacy_alerts --since 2026-08-16` → **clean**, no untracked alerts.
- Direct DB reads (`db/crypto_ai_desk.sqlite`, `proposed_signals`): today's closed crypto trades, current `triggered` book by mode/direction.
- `reports/PAPER_MONITOR_STATUS_LATEST.md` (mtime 22:30 EEST, fresh) + direct OHLCV CSV timestamp checks for the previously-flagged stale symbols.
- Prior review for comparison: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-16_2139.md` (late-session risk review, 21:39 EEST).
- **External web research run this cycle** (2 WebSearch queries: BTC/ETH price context, Coldcard exploit status/scale) — both used to corroborate, not contradict, internal risk flags. No WebFetch needed (search results were sufficiently multi-source on their own).

## 3. Scheduler / Data Freshness

- Scheduler: **fresh**, cycle 2/12 (weekend, crypto-only) completed at 22:32 EEST.
- Scalp: **fresh** (~2h). Intraday: **fresh** (~1h20m). Swing: **carry-forward** (~5h, still usable — no fresher swing scan ran this weekend cycle by review time). Stocks: closed for the weekend, planning-only.
- Catalyst folder: fresh this cycle (692 cumulative events, mtime 22:12 EEST), 5 narrative baskets.
- **Monitor/price-feed integrity: STILL DEGRADED for 3 of 4 previously-flagged symbols, 1 resolved.** Direct OHLCV inspection: `HOLO_USDT`, `BMT_USDT`, `MUBARAK_USDT` last real 15m candle is still **2026-08-15 22:30–23:00 UTC** — unchanged since the 21:39 review, i.e. still ~21–22h stale — yet `PAPER_MONITOR_STATUS_LATEST.md` (lines 79, 90, 94) displays all three as `🟢 OPEN — entry filled, monitoring TP/SL`. `BABY_USDT`, flagged stale in the 21:39 review, has since correctly transitioned to `⚪ CLOSED FLAT 0R` — confirming the underlying fetch/monitor path is not universally broken, just pair-specific and still unresolved for the other three. `WLFI_USDT` (control) is fresh (last candle 2026-08-16 20:15 UTC).
- `detect_untracked_legacy_alerts --since 2026-08-16`: **clean**.
- This is the **5th consecutive review cycle** (02:00, 11:39-blocked, 18:49, 21:39, now 23:29) touching the same underlying stale-OHLCV-with-false-OPEN-badge defect for at least one of these four symbols. See §14 TODO-1 (priority raised to high).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "post_close",
  "as_of": "2026-08-16 23:29 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale", "onchain_config_missing"],
      "data_missing": ["stocks intraday >2 days stale (weekend, expected)", "stocks swing/invest >6 weeks stale (expected — deprecated legacy modes, per prior project context)", "on-chain whale flows / exchange in-out flows not connected", "OI 24h% n/a for several MEXC-fallback symbols"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log + cycle_02_20-48_summary.md mtime 22:32 EEST, ~57 min old", "scalp report 21:28 fresh, intraday 22:08 fresh, swing 18:42 ~5h carry-forward", "catalyst folder mtime 22:12, 692 cumulative events / 5 baskets"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.72,
      "reason_codes": ["risk_off", "chop", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["intraday report: BTC downtrend, ETH range, altcoin breadth 52.6% above EMA20", "swing report: altcoin breadth 56.4% above EMA20", "macro risk 66.5-69.7/100 across today's reports, driven by Iran/Strait-of-Hormuz headlines, unchanged all day", "external WebSearch: BTC ~$62-63k / ETH ~$1,880-1,912 as of mid-Aug 2026, crypto softer than gold on the same inflation data — corroborates internal risk-off read"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["fresh_catalyst", "mapping_weak", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl: 692 total, 346 mapped / 346 unmapped = exactly 50.0% unmapped — right at the flag threshold, borderline-weak mapping tonight", "5 active narrative baskets: perps_dex (HYPE), binance_ecosystem_teaser (BNB), rwa_narrative (ONDO/XLM), ai_narrative (NEAR/RENDER/TAO/FET), momentum_breakout (PORTAL/DOLO/WLFI — PORTAL and DOLO already resolved today)", "SOL/USDT single-source catalyst: Bitwise mulls tokenizing Solana staking ETF via Superstate (The Block)", "BTC/ETH catalysts risk-flagged: Coldcard exploit (multi-source, ~1,778 BTC/$112-116M per external search), ETH SHA/BLAKE quantum-migration roadmap (single-source, long-horizon, low urgency)"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "oi_supports", "data_unavailable"],
      "data_missing": ["OI 24h% n/a for several MEXC/fallback-venue symbols (PORTAL, CHIP, VELVET, ONG, DOLO in the scalp snapshot)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Multiple C-tier short candidates capped for squeeze risk: ACE/USDT, BEAT/USDT, CYS/USDT, KAITO/USDT, HOME/USDT, DOS/USDT (thin-liquidity / high-upper-wick short-squeeze-risk tags)", "ONG/USDT: price up + OI up +60-65%, fresh positioning confirms trend", "ALICE/USDT: price up + OI down -4.6%, short covering — weaker continuation quality, worth watching not chasing"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.62,
      "reason_codes": ["entry_late", "chase_risk", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["DOLO/USDT and PORTAL/USDT swing longs (flagged chase-risk in the 21:39 review) both resolved today: DOLO stopped 16:16 UTC, PORTAL tp3_hit 18:28 UTC — the chase-risk flag was directionally correct for DOLO, wrong (missed a clean continuation) for PORTAL", "no new fresh B-tier technical setups this closing cycle (scalp: none; intraday: none, only C-tier watchlist)", "existing open swing longs (ONG, CHIP, WLFI, ETHFI) remain inside their invalidation levels, no new information"] },
    { "agent": "execution_lifecycle", "verdict": "manual_review", "confidence": 0.75,
      "reason_codes": ["open_actionable", "review_shadow", "closed_flat", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PAPER_MONITOR_STATUS_LATEST.md (22:30 EEST): OPEN_ACTIVE 25, WAITING_FOR_ENTRY 0, REVIEW_ONLY_SHADOW 21, ENTERED_UNRESOLVED_EXPIRED 0, NO_ENTRY_EXPIRED 5, CLOSED_WIN 162, CLOSED_LOSS 8, CLOSED_FLAT 37, UNKNOWN_INCONSISTENT 3", "proposed_signals DB: today's crypto closes — PORTAL/USDT swing tp3_hit (18:28 UTC), HEMI/USDT intraday tp3_hit (09:50 UTC), DOLO/USDT swing stopped (16:16 UTC); no stocks closes today (market closed)", "HOLO/BMT/MUBARAK still incorrectly displayed OPEN off ~21-22h-stale OHLCV; BABY resolved to CLOSED_FLAT since the 21:39 review"] },
    { "agent": "risk_manager", "verdict": "manual_review", "confidence": 0.78,
      "reason_codes": ["manual_review", "reduce_risk", "headline_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["HOLO/USDT, BMT/USDT, MUBARAK/USDT still shown OPEN off stale price feed — 5th consecutive review cycle raising this defect; treat any displayed unrealized P&L on these 3 symbols with active distrust until an operator manually verifies live price", "UNH: DOJ criminal probe into Medicare/Optum Rx fraud reported deepening across 4 independent sources today (QuiverQuant, Phemex, FierceHealthcare, TipRanks) — stocks C-tier only, never actionable, but legal/headline risk confirmed, avoid for any manual override", "BTC: Coldcard exploit remains an active operator-review flag (block_requires_operator_review); external search confirms ~1,778 BTC / $112-116M across three attack waves since 2026-07-30, root cause a 2021 firmware RNG flaw — no new escalation beyond what internal reports already carried"] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.68,
      "reason_codes": ["playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto headline actionable (A/B, week): sample=99 reliable, PF 3.08, winrate 18.6%, totalR +33.2 — mode split: swing PF ~5.4 (n=49, strongest), intraday PF ~1.5 (n=34), scalp PF ~3.7 (n=16, weak confidence, small sample)", "scalp report's own banner separately flags a narrower TP1/2h-horizon cut at PF 0.14 (1W/7L, 14d) — a stricter execution-window metric than the mode-level signal-stats PF; scalp stays low-confidence by the report's own framing despite decent mode-level PF", "stocks headline actionable: sample=8 anecdotal, 0 wins/2 losses, PF 0.0 — far too small and weekend-affected to act on"] },
    { "agent": "head_trader", "verdict": "watch_only", "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "none — watch ALICE/USDT", "trigger": "hold/reclaim above the 0.1402 pullback zone on ≥1x 20-period volume with BTC not breaking local support", "reason": "short-covering + RS-leader tag but currently only a low-confidence C-tier watchlist idea, no fresh catalyst" },
    "best_short_candidate":    { "symbol": "none — watch ACE/USDT", "trigger": "clean bearish HTF structure + confirmed fresh-short OI increase + 1h close below ~0.36 without a high-upper-wick squeeze signal", "reason": "weak-RS short (-15 to -17% 24h) but currently squeeze-capped to C-tier, thin volume" },
    "best_catalyst_candidate": { "symbol": "SOL/USDT", "trigger": "second independent source corroborating the Bitwise/Superstate staking-ETF tokenization report, plus a clean technical entry structure", "reason": "only single-source news attention right now (The Block), no proposed_signal yet" },
    "avoid_candidate":         { "symbol": "BTC/USDT (new sizing) and UNH (stocks, any manual override)", "reason": "BTC carries an active operator-review flag from the ongoing Coldcard exploit plus risk-off macro; UNH carries a multi-source-confirmed deepening DOJ criminal probe" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.75 | scheduler_fresh, report_stale, onchain_config_missing | advisory_only |
| market_regime | caution | 0.72 | risk_off, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.60 | fresh_catalyst, mapping_weak, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk, oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.62 | entry_late, chase_risk, clean_retest | advisory_only |
| execution_lifecycle | manual_review | 0.75 | open_actionable, review_shadow, closed_flat, needs_review | advisory_only |
| risk_manager | manual_review | 0.78 | manual_review, reduce_risk, headline_risk | advisory_only |
| playbook_performance | ok | 0.68 | playbook_working, low_sample | advisory_only |
| head_trader | watch_only | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-16_2139.md` (late-session risk review, 21:39 EEST).

- **DOLO/USDT swing long** — flagged chase-risk/watch at 21:39 — **invalidated**: stopped 16:16 UTC (before the prior review even ran, confirming the "score below active-trade threshold" caution was warranted).
- **PORTAL/USDT swing long** — flagged chase-risk/watch at 21:39 — **confirmed**: tp3_hit 18:28 UTC. Thesis worked despite the chase-risk flag; a reminder the caution label is directional, not a hard block.
- **HEMI/USDT intraday long** — tp3_hit 09:50 UTC (earlier today, not mentioned in the 21:39 review's headline but visible in today's closes).
- **BABY/USDT stale-price defect** — **resolved**: correctly transitioned to CLOSED FLAT since 21:39.
- **HOLO/USDT, BMT/USDT, MUBARAK/USDT stale-price defect** — **unchanged/still open**: same ~21–22h-stale last candle as the 21:39 review, still displayed OPEN. Now the 5th consecutive cycle.
- **New catalysts**: none material beyond what the 21:39 review already carried (Coldcard exploit, Iran/Hormuz, SOL staking-ETF chatter) — catalyst mapping ticked from ~45.9% unmapped (21:39) to exactly 50.0% unmapped now (borderline).
- No new A-tier or fresh B-tier appeared this closing cycle.

## 5. Catalyst Coverage

- Total `catalyst_events` today (cumulative): **692**. Mapped (non-null symbol): **346**. Unmapped: **346** → **50.0% unmapped** — exactly at the flag threshold (not technically over 50%, but no margin). **Treat the catalyst layer as context, not the final decision, tonight.**
- `narrative_baskets`: **5** (perps_dex_narrative/HYPE, binance_ecosystem_teaser/BNB, rwa_narrative/ONDO+XLM, ai_narrative/NEAR+RENDER+TAO+FET, momentum_breakout/PORTAL+DOLO+WLFI).
- Top unmapped headlines tonight (symbol-resolver misses): "Pope calls for an end to West Bank violence against Palestinians" (Reuters, geopolitics, not tradable); "Wendy's Jumps on Report That Nelson Peltz Wants to Take His Old Company Private" (should likely map to WEN, resolver miss); "$10,000 in NuScale at Its 52-Week High Is Worth About $1,650 Today" (should map to SMR, resolver miss).
- Notable mapped events: TSLA legal_risk (Musk SEC Twitter-disclosure settlement, $1.5M fine — minor, resolved item, not an ongoing risk), BTC exploit_hack (Coldcard, multi-source), UNH legal_risk ×4 (DOJ criminal probe deepening, multi-source).

## 6. Market Landscape

Crypto: BTC downtrend, ETH range-to-neutral, altcoin breadth 45–56% above EMA20 (mixed, leaning weak), macro risk 66.5–69.7/100 all day on Iran/Strait-of-Hormuz naval-blockade headlines that have not de-escalated since the morning cycles. External check (WebSearch) confirms BTC trading roughly $62–63k and ETH ~$1,880–1,912 in the days leading into today, with crypto underperforming gold on the same inflation data — consistent with the internal risk-off read, not contradicting it. Stocks: closed all day (Sunday); Friday's carry-forward book (AVGO, MSTR, APP, SMCI, IWM, ABNB) is all closed/expired, nothing live to size Monday's open off of yet.

### Market Mood / Risk Routing

- Crypto mood: **risk-off-leaning chop** (downtrend BTC, elevated macro risk, no A-tier all day)
- Stocks mood: **closed** (Sunday; Monday open unconfirmed)
- Dominant narrative: momentum_breakout basket (PORTAL/DOLO/WLFI) already largely played out today; perps_dex (HYPE) and binance_ecosystem_teaser (BNB) baskets still open/unconfirmed
- Preferred side now: **wait-for-trigger** (mixed — hold existing swing longs, no fresh sizing)
- Best long candidate: none clean — see best long-watch (ALICE/USDT) in §8
- Best short candidate: none clean — see best short-watch (ACE/USDT) in §8, squeeze-capped
- Best catalyst-backed candidate: SOL/USDT (single-source staking-ETF chatter, needs corroboration) — see §8
- What to avoid: fresh BTC sizing while the Coldcard exploit operator-review flag is live; UNH for any manual override (DOJ probe deepening)
- What would change the view: BTC reclaiming local structure + macro headlines cooling on Hormuz, or a second independent source confirming the SOL staking-ETF story

## 7. Candidate Deep Dives

### 7.1 ALICE/USDT — long-watch (crypto, intraday+swing C-tier)
- Has price already reacted to the catalyst? No verified fresh catalyst — this is a technical/derivatives setup (short covering), not catalyst-driven.
- Is the setup chasing? Moderately — up 9.5–12.2% 24h already; not yet at the 2-ATR overextension flag.
- Retest/pullback structure? Yes — the report defines a specific conditional pullback zone (intraday: 0.1372–0.1402; swing: 0.1352–0.1377).
- Overextended (>2 ATR from EMA20)? No, per the report's own gating (no such flag raised for ALICE).
- Would entry now be late? Only if bought at market; the defined pullback zone is not yet late.
- What level makes it actionable? A hold/reclaim inside the pullback zone with volume ≥1x 20-period average and no BTC breakdown.
- Aligned with current mood? Partially — mood is risk-off-leaning, so this needs to be an RS-leader confirmation, not a blind bounce-buy.
- Long, short, or wait-for-trigger? Wait-for-trigger long.
- Actionable now or after confirmation? After confirmation (score currently below active-trade threshold — 58.8/54.9 in the two reports).
- What would invalidate it? 1h close beyond ~0.133 (intraday) / ~0.132 (swing) invalidation levels; funding is negative (shorts crowded) which is itself a weak positive but not sufficient alone.
- Chase-risk setup? Moderate.
- Catalyst confirmation or contradiction? None — no fresh verified catalyst either way.

### 7.2 ACE/USDT — short-watch (crypto, intraday/swing C-tier, squeeze-capped)
- Has price already reacted? Yes — already down 15.8–17.2% 24h; the move has substantially happened.
- Is the setup chasing? For a fresh short entry now, yes, somewhat — this is a "failed bounce" playbook (`crypto_failed_bounce_short`), which specifically wants a retest, not a chase of the initial drop.
- Retest/pullback structure? The playbook's design requires a bounce/retest into resistance before shorting, not chasing the current low.
- Overextended? The symbol shows "short squeeze risk → capped to C: high_upper_wick_short_squeeze_risk (+exhaustion)" — i.e. the system itself flags exhaustion/squeeze risk on the short side.
- Would entry now be late? Yes, for a fresh short at current price; only a retest into resistance is clean.
- What level makes it actionable? Confirmed bearish HTF structure + fresh-short OI increase + clear stop above the swing high, without the current high-upper-wick squeeze signal present.
- Aligned with mood? Yes, directionally (risk-off favors shorts) — but the squeeze-risk cap is a real, system-generated caution, not just conservatism.
- Long/short/wait? Wait-for-trigger short.
- Actionable now? No — capped to C-tier specifically for squeeze risk.
- Invalidation? A reclaim of resistance with rising OI would invalidate the short thesis (squeeze scenario).
- Chase-risk? Yes if forced now.
- Catalyst? None fresh; derivatives show funding -0.0045 to -0.0065 (mildly bearish crowding) but OI is rising into a falling price (fresh shorts pressing) — a mixed signal, not a clean confirmation either way.

### 7.3 SOL/USDT — catalyst-watch
- Catalyst: "Bitwise mulls tokenizing its Solana staking ETF via Superstate partnership" (The Block; internal verification_status = single_source; no risks flagged).
- Has price reacted? Not materially yet per today's reports — this is attention-stage, not a confirmed move.
- Actionable now? No — single-source, no technical setup built around it yet, no proposed_signal exists for SOL tonight.
- What would make it actionable? A second independent outlet confirming the Superstate/Bitwise report, combined with a clean technical entry structure (retest, not a chase).
- Legal/headline risk? None identified for SOL specifically tonight.

### 7.4 UNH — avoid (stocks, C-tier only, never actionable, legal/headline risk)
- **LEGAL/HEADLINE RISK confirmed**: DOJ criminal probe into UnitedHealth's Medicare/Optum Rx billing reported deepening, corroborated across 4 independent outlets today (QuiverQuant, Phemex, FierceHealthcare, TipRanks) plus a prior 16% single-day drop referenced in the same coverage.
- Signal history: repeated `missed_no_entry` / `stale_before_entry` on UNH shorts over the past two weeks — the system has not actually entered this name, which is the correct behavior given the standing legal risk.
- Final verdict: **AVOID** for any manual override. C-tier, stocks closed — no live exposure risk tonight, but flag for Monday.

### 7.5 BTC/USDT — avoid for new sizing (system-wide risk context, not a directional signal)
- Coldcard hardware-wallet exploit remains an active operator-review flag inside the desk (`block_requires_operator_review`). External search (2 sources: Cryptobriefing, TRM Labs, TechCrunch, CoinDesk, Fortune, The Hacker News — all corroborating) confirms scale at **~1,778 BTC (~$112–116M)** across three attack waves since 2026-07-30, root cause a 2021 Coldcard firmware RNG flaw; roughly 1,367–1,531 BTC of the stolen total remains unlaundered/untouched in attacker wallets as of mid-August.
- This is a **risk-only** flag — it does not itself gate scoring/routing — but combined with the ongoing risk-off macro (Iran/Hormuz) and BTC's own downtrend, it argues against adding fresh discretionary BTC exposure tonight. No change to any BTC-linked altcoin swing longs already open (ONG, CHIP, WLFI, ETHFI) — those stand on their own invalidation levels.

## 8. Best Candidates Ranked

No clean actionable candidate tonight (no A-tier, no fresh B-tier this closing cycle). Ranked by readiness:

1. **Long-watch: ALICE/USDT** — trigger: hold/reclaim of 0.1352–0.1402 pullback zone on ≥1x 20-period volume, BTC not breaking local support.
2. **Short-watch: ACE/USDT** — trigger: confirmed bearish HTF structure + fresh-short OI + clean stop above swing high, without the current squeeze/exhaustion signal.
3. **Catalyst-watch: SOL/USDT** — trigger: second independent source on the Bitwise/Superstate staking-ETF report + clean technical entry.
4. **Avoid: BTC/USDT (new sizing)** and **UNH (any manual override)** — see §7.4–7.5.

## 9. Avoid / No Trade

This is a decision-window verdict for the overnight-into-Asia window only — **never** a command to pause scanning, data collection, or the scheduler; the ALWAYS-SCAN rule stays in force regardless.

- No fresh crypto B/A entries clear the bar tonight — existing swing book (ONG, CHIP, WLFI, ETHFI, and the older carried positions) stands on its own invalidation levels; nothing new to size.
- Avoid fresh BTC discretionary sizing while the Coldcard operator-review flag is live (§7.5).
- Avoid UNH for any manual override — DOJ probe risk confirmed multi-source (§7.4).
- Do not treat HOLO/USDT, BMT/USDT, MUBARAK/USDT displayed "OPEN" P&L as trustworthy until an operator manually verifies live price (§3, §14 TODO-1).

## 10. Main Risks

- **Stale-price / false-OPEN-badge defect** — HOLO/BMT/MUBARAK, 5th consecutive cycle, no fix landed (TODO-1, high priority).
- **Macro risk-off** — Iran/Strait-of-Hormuz naval tension persistent all day, no de-escalation signal yet; external search corroborates BTC/ETH softness relative to gold on the same data.
- **Coldcard exploit** — still actively unwinding (multi-source, ~1,778 BTC), operator-review flag live on BTC.
- **Catalyst mapping at exactly 50% unmapped** — right at the desk's own quality threshold; treat catalyst-backed reasoning with extra caution tonight.
- **Stocks book stale** — Friday's carry-forward is fully closed/expired; nothing to carry Monday's open decisions off of yet, will need a fresh pre-market read.

## 11. Action Plan — next 4 hours

- No new crypto entries recommended overnight; hold existing swing book to its defined invalidation levels.
- Watch ALICE/USDT and ACE/USDT for the confirmation triggers in §7.1–7.2 if either sets up cleanly into the Asia session.
- Watch for a second source on the SOL/USDT staking-ETF report.
- Operator: manually verify live price for HOLO/USDT, BMT/USDT, MUBARAK/USDT before trusting any displayed unrealized P&L (TODO-1).
- No stocks action possible until Monday pre-market data exists.

## 12. Final Verdict per Mode

- **Scalp**: No trade. Desk's own banner flags TP1/2h-horizon PF 0.14 (14d) — stays low-confidence regardless of tonight's quiet close.
- **Intraday**: No trade. HEMI/USDT tp3_hit earlier today was the mode's win; no fresh setup remains.
- **Swing**: Hold existing book (ONG, CHIP, WLFI, ETHFI + older carried longs). PORTAL/USDT tp3_hit and DOLO/USDT stopped today — net positive for the mode. No new entries.
- **Stocks (all modes)**: Closed/planning-only. Nothing actionable until Monday; UNH flagged avoid for any manual override.

## 13. Sources

- [Bitcoin and ethereum prices today, Friday, August 14, 2026: Crypto prices backing off further](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-friday-august-14-2026-crypto-prices-backing-off-further-123636029.html) — Yahoo Finance, 2026-08-14
- [Crypto Market Outlook August 2026: Bitcoin, Ethereum & ...](https://intellectia.ai/blog/crypto-market-outlook-august-2026) — Intellectia, 2026-08 (date within article body)
- [Coldcard wallet exploit leads to theft of over 1,778 Bitcoin worth $112M](https://cryptobriefing.com/coldcard-wallet-exploit-bitcoin-theft-112m/) — Crypto Briefing, 2026-08
- [The Largest Hardware Wallet Exploit of 2026: Inside the USD 116 Million Coldcard Hack](https://www.trmlabs.com/resources/blog/the-largest-hardware-wallet-exploit-of-2026-inside-the-usd-116-million-coldcard-hack) — TRM Labs, 2026-08
- [Hackers steal over $130M by exploiting bug in offline hardware wallets](https://techcrunch.com/2026/08/04/hackers-steal-over-130-million-by-exploiting-bug-in-offline-hardware-wallets/) — TechCrunch, 2026-08-04
- [Bitcoin cold-wallet attack spreads to 4,500 addresses as losses near $89 million](https://www.coindesk.com/tech/2026/08/02/bitcoin-cold-wallet-attack-spreads-to-4-500-addresses-as-losses-near-usd89-million) — CoinDesk, 2026-08-02
- [Bitcoin owners rocked by $116 million hack: What we know about the Coldcard exploit](https://fortune.com/2026/08/03/bitcoin-owners-116-million-hack-coldcard-coinkite-exploit/) — Fortune, 2026-08-03
- Internal: `data/catalysts/2026-08-16/catalyst_events.jsonl`, `catalyst_cycle_19-12.md` — UNH DOJ probe (QuiverQuant, Phemex, FierceHealthcare, TipRanks, all dated 2026-08-16), TSLA SEC settlement (Union Leader, 2026-08-16), SOL staking-ETF (The Block, single-source, 2026-08-16).

## 14. Fix Requests / TODO

### TODO-1
- **issue:** Stale-OHLCV / false-"OPEN"-badge defect on HOLO/USDT, BMT/USDT, MUBARAK/USDT — displayed `🟢 OPEN — entry filled, monitoring TP/SL` in `reports/PAPER_MONITOR_STATUS_LATEST.md` while their underlying OHLCV cache has not advanced past 2026-08-15 22:30–23:00 UTC for over 24h and counting. This is the **5th consecutive scheduled review cycle** (02:00, 11:39-blocked, 18:49, 21:39, 23:29) to observe this for at least one of these symbols. BABY/USDT, previously also stuck, has since correctly resolved to CLOSED_FLAT, proving the fetch/monitor path recovers for some pairs — the remaining 3 need investigation into why their specific OHLCV fetch is stuck.
- **evidence:** `data/raw/ohlcv/binance/15m/{HOLO,BMT,MUBARAK}_USDT.csv` — last row unchanged at `2026-08-15 22:30:00`/`23:00:00` across at least 4 review cycles spanning ~5+ hours of wall-clock time; `reports/PAPER_MONITOR_STATUS_LATEST.md` lines 79, 90, 94 (mtime 2026-08-16 22:30 EEST) still show all three as OPEN. Control case `WLFI_USDT.csv` last row `2026-08-16 20:15:00` — fresh, confirming the fetch path itself works for other pairs.
- **suggested manual fix:** Investigate the OHLCV fetch/cache path specifically for HOLO, BMT, MUBARAK on binance 15m — check for a delisting, symbol-mapping mismatch, or per-symbol rate-limit/exception being silently swallowed. Cross-check whether the paper monitor's "OPEN" badge should itself degrade to a stale/needs-review state when its underlying price cache exceeds some staleness threshold (e.g. >2h), rather than continuing to display a live-looking OPEN badge indefinitely.
- **priority:** high (raised from the prior reviews' implicit medium — now 5 consecutive cycles with no resolution for 3 of the original 4 symbols).
- **first observed:** 2026-08-16 02:00 EEST (per the 21:39 review's own history; re-confirmed every cycle since).

### TODO-2
- **issue:** Catalyst symbol-resolver mapping sitting at exactly 50.0% unmapped tonight (346/692) — right at the desk's own "weak mapping" threshold with zero margin. Two concrete resolver misses observed tonight: a Wendy's/Nelson Peltz take-private headline not mapped to WEN, and a NuScale 52-week-high headline not mapped to SMR.
- **evidence:** `data/catalysts/2026-08-16/catalyst_events.jsonl` — computed 346 mapped / 346 unmapped of 692 total; sample unmapped headlines include the Wendy's and NuScale items above.
- **suggested manual fix:** Extend the symbol resolver's company-name → ticker dictionary to catch common-name mentions (e.g. "Wendy's" → WEN, "NuScale" → SMR) that currently fall through to null-symbol.
- **priority:** medium.
- **first observed:** 2026-08-16 23:29 EEST (borderline in prior cycles too — 21:39 review measured 45.9% unmapped on an earlier catalyst snapshot; trending toward the threshold, not yet clearly over it).
