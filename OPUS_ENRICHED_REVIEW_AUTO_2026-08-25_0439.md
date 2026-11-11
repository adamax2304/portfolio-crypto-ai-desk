# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:39 EEST

## 1. Executive Summary

Slot: **crypto overnight / Asia review** (04:30 EEST). Advisory only / no auto-trade. Scheduler is live and mid-cycle (paper accounting + structural TP/stop refresh ran clean in the last 10 min). Crypto regime is **risk-on** (BTC/ETH uptrend, 83-85% of tracked symbols above EMA20/50) but sits against a **risk-off macro backdrop** (desk macro score 100/100 — Iran sanctions/Strait-of-Hormuz headlines) that has not yet shown up in crypto price action — a divergence worth watching into Europe, not a reason to flip bearish tonight. No A-tier crypto setups this cycle; 50 active B-tier crypto signals, all long, mostly triggered/tp1-tp2_hit and tracking cleanly. Stocks are closed (US session) — treated as carry-forward/watchlist context only; stocks book-wide performance remains weak (B PF 0.56, C PF 0.46) so no urgency there. Best long: **VIRTUAL/USDT** (RS-leader, fresh OI). Best catalyst-backed: **NEAR/USDT** / **TAO/USDT** (AI-narrative basket, TAO already tp2_hit — narrative delivering). Best short-watch: **ACE/USDT** (weakest RS symbol with live data, but negative funding + elevated crowding = squeeze risk, so watch not chase). Avoid: **ZRO/USDT** (fresh exploit-adjacent headline, operator-review flagged).

## 2. Data Used

- Scalp report `2026-08-25_01-18` (21 min old), Intraday report `2026-08-25_01-28` (11 min old) — both fresh.
- Swing report `2026-08-24_15-35` (~10h old) — **carry-forward**, flagged.
- Stocks intraday report `2026-08-24_22-48` (~6h old, pre-market/overnight) — context only, market closed.
- Stocks swing/invest reports last dated **2026-07-02** — stale by ~7.5 weeks, see §14 TODO.
- `data/catalysts/2026-08-25/` (catalyst_cycle_01-35.md, catalyst_events.jsonl, narrative_baskets.jsonl) — fresh, 04:35.
- `data/processed/llm_analysis_packet.md` (04:31) and `llm_stocks_packet.md` (01:50, market closed).
- CLI: `active-signals` (crypto, stocks), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts --since 2026-08-25`.

## 3. Scheduler / Data Freshness

- `scheduler.log` last write: **04:39** (mid-cycle, actively running paper structural-stop and entry-mode-classify steps). **Fresh.**
- Latest completed cycle summary: `cycle_04_00-39_summary.md` (02:04) — 2h35m old, within the 3h defer threshold. **Not deferred.**
- Monitor: `CRYPTO-INVEST-FORWARD MONITOR` restarted twice in this window (01:26 → 01:32, new pid); no error entries visible in the tail. Paper execution accounting, structural TP refresh, structural stop plan all completed exit=0 in the last 10 minutes.
- `detect_untracked_legacy_alerts --since 2026-08-25`: **0 untracked alerts** — clean this cycle (contrast with prior review's "20 unresolved Telegram alerts" note — appears to have cleared/reset; not independently re-verified against [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]], keep watching).
- `signal-stats` CLI took **>5 minutes** to return (both asset classes) — unusually slow vs. typical CLI response; flagged in §14 as a possible perf regression, not blocking this review.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-08-25 04:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "catalyst_missing"], "data_missing": ["stocks_swing_stale_7wk"],
      "suggested_effect": "advisory_only", "facts_used": ["scheduler.log mtime 04:39", "cycle_04_00-39_summary.md 02:04", "stocks swing/invest reports dated 2026-07-02"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["risk_on", "mixed", "longs_preferred"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["BTC/ETH uptrend, altcoin breadth 83-85% above EMA20/50", "macro risk score 100/100 risk-off (Iran sanctions) not yet reflected in price"] },
    { "agent": "catalyst_narrative", "verdict": "ok", "confidence": 0.65,
      "reason_codes": ["fresh_catalyst", "narrative_supported", "mapping_weak"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["ai_narrative basket (NEAR/RENDER/TAO/FET) <1h fresh", "72.6% unmapped catalyst events this cycle"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["squeeze_risk", "oi_supports", "funding_extreme"], "data_missing": ["OI history for PROM/ONG/POL (mexc fallback, n/a)"],
      "suggested_effect": "advisory_only", "facts_used": ["ACE/USDT funding -0.0059(bybit)/-0.0035(mexc), crowding elevated", "VIRTUAL/USDT price up + OI up +23.22%, crowding normal"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "entry_fresh", "overextended"], "data_missing": ["TradingView/manual chart check unavailable"],
      "suggested_effect": "advisory_only", "facts_used": ["TUT/HEMI already -18% to -23% 24h, HEMI tagged overextended", "VIRTUAL 24h +14.16%, RS +10.48%, no-catalyst momentum playbook known failure mode"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["open_actionable", "waiting_for_entry", "no_entry"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["crypto: 40 open (triggered/tp1/tp2), 10 waiting_for_entry, 0 expired", "stocks: 44 tp1/tp2 (resolved-in-progress), 5 triggered, 1 waiting, market closed"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["headline_risk", "manual_review"], "data_missing": ["could not independently re-verify XPL/USDT bias-tag status this cycle"],
      "suggested_effect": "advisory_only", "facts_used": ["ZRO/USDT exploit_hack block_requires_operator_review", "prior review flagged XPL/USDT filled-long-vs-bias-short unresolved 3 cycles running"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["crypto scalp PF 0.10 / totalR -4.5 (n=106) vs intraday PF 2.51 / totalR +53.0 (n=155)", "crypto weekend=Y underperforms (winrate 11%, n=137)", "stocks B-tier PF 0.56 winrate 3%, C-tier PF 0.46 winrate 12%"] }
  ],
  "head_trader": {
    "overall_verdict": "normal",
    "confidence": 0.65,
    "preferred_side": "longs",
    "best_long_candidate": { "symbol": "VIRTUAL/USDT", "trigger": "already actionable — hold/add only on confirmed pullback to 0.78-0.80 zone, not at market", "reason": "RS-leader tag, price up + OI up +23.22%, crowding normal, top-2 strongest symbol two cycles running" },
    "best_short_candidate": { "symbol": "ACE/USDT", "trigger": "wait for funding to normalize toward zero AND a confirmed 1h close below the last swing low with rising OI before entering short — do not chase the -10.45% move as-is", "reason": "weakest RS symbol with usable derivatives data, but negative funding + elevated crowding across bybit/mexc signals a possible short squeeze, not a clean short yet" },
    "best_catalyst_candidate": { "symbol": "NEAR/USDT", "trigger": "already triggered/open on the swing leg (ai_narrative basket, <1h fresh); size only on confirmed AI-sector breadth follow-through, not on the basket headline alone", "reason": "AI narrative basket primary, TAO/USDT (same basket) already realized tp2_hit tonight — narrative proof-of-concept" },
    "avoid_candidate": { "symbol": "ZRO/USDT", "reason": "fresh exploit-adjacent headline (LayerZero axing chains post-KelpDAO exploit), desk-flagged block_requires_operator_review — do not add new exposure until an operator clears it" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, catalyst_missing(resolved by rerun) | advisory_only |
| market_regime | caution | 0.70 | risk_on, mixed, longs_preferred | advisory_only |
| catalyst_narrative | ok | 0.65 | fresh_catalyst, narrative_supported, mapping_weak | advisory_only |
| derivatives_squeeze | caution | 0.60 | squeeze_risk, oi_supports, funding_extreme | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, entry_fresh, overextended | advisory_only |
| execution_lifecycle | ok | 0.85 | open_actionable, waiting_for_entry, no_entry | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.75 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | normal | 0.65 | (synthesis — see JSON) | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-24_2332.md` (23:34):

- **NEAR/USDT** — unchanged as a top candidate for a 4th straight cycle (was "best overall candidate" three cycles running); still open/actionable, now reinforced by the fresh (<1h) ai_narrative basket rather than carried on an older catalyst.
- **TAO/USDT** — new since last review: joined the ai_narrative basket and its swing leg went to **tp2_hit** — a concrete narrative-delivers data point, not just a thesis.
- **TUT/USDT** (prior short-watch) — downgraded from "cleanest relative-weakness idea" to **avoid-as-chase**: 24h move has extended to -23.31% (was less extreme at last review), no confirming derivatives data — now overextended rather than a clean entry.
- **XPL/USDT** (prior AVOID/MANUAL REVIEW, filled-long-vs-bias-short, unresolved 3 cycles) — could not be independently re-verified this cycle (no bias-tag field surfaced in the read-only sources available under this run's permission contract); carried forward as **NEEDS REVIEW**, not cleared. See §14.
- **BLK** (prior AVOID, legal/headline) — not present in this cycle's active-signal or catalyst data at all; treat as resolved/rotated-out rather than confirmed-clear.
- **Crypto scalp mode** — still showing PF 0.10 / totalR -4.5R over the sampled window (prior review noted it was kill-switched); however 10 scalp-mode signals are currently active/waiting in tonight's active-signals pull, so the kill-switch state could not be confirmed from read-only data this cycle — flagged in §14.
- **Untracked-alert leakage** — prior review noted 20 stalled untracked Telegram alerts; tonight's detector returns **0**. Improvement, but not independently reconciled against the underlying bug in [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]].

## 5. Catalyst Coverage

- Catalyst events today: **500** scanned → **137 mapped** / **363 unmapped** (**72.6% unmapped**).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Narrative baskets: **4** (`ai_narrative`, `binance_ecosystem_teaser`, `rwa_narrative`, `perps_dex_narrative`).
- Top 3 unmapped headlines (macro, not symbol-specific — expected, not a mapper failure per se):
  1. "RBA says cash rate is at top end of neutral rate estimates from models and markets, with uncertainty around estimates"
  2. "RBA board: current cash rate seen as effective in moving economy toward balance"
  3. "RBA: board to receive fresh inflation, labour market and GDP data before September meeting"
- Legal/regulatory feed this cycle is dominated by routine class-action "investors have opportunity to lead" PR-Newswire boilerplate (PLNT, GPGI/CMPO, BABA, HDB, RXT, CAPR, GNS, SPRY, AARD) — treat as low-signal ambulance-chaser notices, not fresh fraud findings, unless a specific symbol is an active desk candidate (none of these are tonight).

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **risk-on** (BTC uptrend, ETH uptrend, altcoin breadth 83.3% > EMA20 / 85.4% > EMA50, ATR percentile 78 — normal/elevated vol)
- Stocks mood: **closed** (overnight EEST; last snapshot shows book-wide weakness — B-tier PF 0.56/winrate 3%, C-tier PF 0.46/winrate 12% — carry into the pre-US context review, not actionable now)
- Dominant narrative: **AI-sector rotation** (NEAR/RENDER/TAO/FET primary, WLD/ASTER related) — momentum 67.8/100, heat only 32/100 (attention/volume have not caught up to price yet)
- Preferred side now: **longs, selective** — desk's own recommended style is "selective longs; prefer pullbacks on relative strength," which matches tonight's data
- Best long candidate: **VIRTUAL/USDT** (see §7)
- Best short candidate: **ACE/USDT** — watch only, squeeze risk (see §7)
- Best catalyst-backed candidate: **NEAR/USDT** (ai_narrative, TAO/USDT proof-of-concept via tp2_hit)
- What to avoid: **ZRO/USDT** (exploit-adjacent headline, operator-review flag); chasing **TUT/USDT or HEMI/USDT** shorts at current extension (-23% / -18.5%, HEMI explicitly tagged overextended)
- What would change the view: a confirmed break of BTC/ETH uptrend structure, or the 100/100 macro risk-off score (Iran/Strait-of-Hormuz) finally showing up as real crypto downside — currently a **divergence to monitor**, not yet a trigger

## 7. Candidate Deep Dives

### 1. VIRTUAL/USDT — LONG (best long candidate)
- Status: multiple open legs — intraday `triggered`, scalp `tp1_hit`, another scalp `triggered`; entry zone ~0.78-0.80, score 69.3-71.9 across modes.
- Has price already reacted? Yes — 24h +14.16%, RS vs BTC +10.48%; some of the move is behind it.
- Chasing? Not badly — still inside the desk's tracked entry bands on the open legs; fresh adds at market would be later than the tracked entries.
- Retest/pullback structure? Playbook is explicitly "no-catalyst intraday momentum," whose known failure mode is "net-negative in chop — needs RS-leader or breakout confirmation." VIRTUAL is tagged `relative_strength`, satisfying that confirmation requirement.
- Overextended (>2 ATR from EMA20)? Not flagged as such in this cycle's data.
- Derivatives: price up + OI up (+23.22%), long/short 1.41, crowding normal — fresh positioning, not stale.
- Catalyst confirmation/contradiction: none — pure momentum/RS thesis, no catalyst tailwind or headwind.
- Aligned with mood? Yes — textbook "selective long, RS-leader" per the desk's own regime read.
- Actionable now or wait? Existing legs are actionable as tracked; treat fresh sizing as pullback-only.
- Invalidation: loss of RS vs BTC or a break back below the tracked entry band.

### 2. NEAR/USDT — LONG (best catalyst-backed candidate)
- Status: swing `triggered`, score 67.4, part of the fresh (<1h) `ai_narrative` basket (primary, with RENDER/TAO/FET).
- Catalyst confirmation: fresh basket-level (multi-symbol AI-sector rotation), not a single-symbol news item — narrative strength, not idiosyncratic catalyst strength.
- Price reaction: narrative heat is still low (32/100) relative to momentum (67.8/100) — attention/volume have not caught up, so this is not a stale/priced-in move yet.
- Chase risk: low-to-moderate — the basket is fresh, but multi-symbol AI rotation baskets carry crowding risk if attention catches up fast (flagged explicitly by the basket's own summary: "watch for crowding").
- Confirmation from within the same basket: **TAO/USDT already hit tp2** tonight — real evidence the AI-narrative thesis is paying, not just a story.
- Invalidation: AI-sector narrative heat/momentum rolling over, or NEAR losing RS vs BTC.
- Actionable now or wait? Already open/actionable on the existing swing leg; treat as hold, not as a fresh chase.

### 3. TAO/USDT — LONG (catalyst proof-point, same basket as NEAR)
- Status: swing leg already **tp2_hit** (score 65.0), intraday leg **tp1_hit** (score 67.8) — both realized partial/full wins tonight.
- This is the "receipts" behind the ai_narrative basket rather than a fresh entry idea — nothing new to size here; included to substantiate the catalyst-backed thesis above.
- No new action needed; treat as evidence, not as an open trigger.

### 4. ASTER/USDT — LONG (catalyst-backed, dual-basket, caution)
- Status: swing `triggered`, score 67.2 — sits in **two** narrative baskets simultaneously (`binance_ecosystem_teaser` related, `perps_dex_narrative` related alongside HYPE/DYDX/GMX).
- Catalyst confirmation: basket-level, both flagged with explicit "early rotation / sell-the-news risk" (binance basket) and playbook `wait_pullback` (perps basket) rather than an immediate-momentum playbook.
- Chase risk: **elevated** relative to VIRTUAL/NEAR — being in two hype-adjacent baskets at once (Binance ecosystem teaser + Hyperliquid/perps rotation, the latter itself carrying a $1.2B token-unlock risk warning on HYPE) raises sell-the-news risk if either narrative cools.
- Actionable now or wait? Existing leg stands; do not add fresh size without a confirmed pullback per the `wait_pullback` playbook the desk itself assigned.
- Invalidation: HYPE/DYDX/GMX basket rolling over, or a confirmed break of ASTER's structure.

### 5. ACE/USDT — SHORT-WATCH (best short candidate, not yet clean)
- Status: **not currently an active desk signal** — surfaced from the "weakest symbols" / derivatives cross-check data as a watch idea, not a live position.
- Price: 24h -10.45%, RS vs BTC -14.13%, tagged `weak_vs_market` — genuinely the weakest symbol tonight with usable derivatives data (TUT/HEMI are weaker on price but lack derivatives confirmation and HEMI is explicitly `overextended`).
- Derivatives: funding **negative** across both bybit (-0.0059) and mexc (-0.0035), crowding **elevated** — this is the key caution: negative funding with elevated crowding typically means shorts are already crowded/paying to hold, raising squeeze risk on a fresh short entry.
- Actionable now? **No** — this is a watch-only idea. Trigger: wait for funding to normalize toward neutral/positive (signaling short crowding has eased) AND a confirmed 1h close below the recent swing low with OI rising (fresh short positioning, not squeeze fuel) before treating it as an entry.
- Invalidation: funding stays deeply negative while price stabilizes (squeeze setup, avoid) or RS recovers vs BTC.

**Excess candidates not deep-dived (priority-ranked out):** ZRO/USDT (avoid, see §9), XPL/USDT (needs review, see §9/§14), TUT/USDT and HEMI/USDT (short ideas, but overextended/unconfirmed — chase risk too high to rank above ACE).

## 8. Best Candidates Ranked

1. **VIRTUAL/USDT** — LONG, RS-leader, fresh OI, hold/pullback-add only.
2. **NEAR/USDT** — LONG, catalyst-backed (ai_narrative), hold — 4th straight cycle as a top idea.
3. **TAO/USDT** — LONG, catalyst proof-point (tp2_hit tonight), no new action, evidence only.
4. **ASTER/USDT** — LONG, catalyst-backed but dual-narrative chase risk — hold existing leg, wait_pullback for adds.
5. **ACE/USDT** — SHORT-WATCH only — squeeze risk, needs funding normalization + confirmed breakdown before entry.

## 9. Avoid / No Trade

*(This decision window only — never a command to stop scanning, tracking, or the scheduler.)*

- **ZRO/USDT** — exploit-adjacent headline (LayerZero axing 14 low-activity chains post-KelpDAO exploit), desk-flagged `block_requires_operator_review`. Do not add new exposure until an operator clears it.
- **XPL/USDT** — prior review flagged a filled-long-vs-bias-short contradiction unresolved for 3 consecutive cycles; this run's read-only sources did not surface the bias-tag field to confirm either way. Treat as **NEEDS REVIEW**, not cleared — do not add size until an operator resolves it. See §14.
- **TUT/USDT, HEMI/USDT** — both are the most extended weak symbols (-23.3% / -18.5% 24h), HEMI explicitly tagged `overextended`; chasing either as a fresh short now is late. Wait for a confirmed retest/bounce-failure, not the current extension.
- **Fresh crypto scalp adds generally** — mode-level PF is 0.10 / totalR -4.5R on the sampled window (worst-performing mode by far); existing scalp legs can run to their stops/targets, but this is not the mode to add fresh size in.

## 10. Main Risks

- **Macro-vs-price divergence**: desk macro score is 100/100 risk-off (Iran sanctions, Strait of Hormuz) while crypto price action remains firmly risk-on. Historically this kind of divergence either resolves via a delayed risk-off reaction or macro noise gets ignored — worth monitoring into the Europe slot rather than dismissing.
- **XPL/USDT bias-tag question unresolved** — carried forward from the prior review without independent reconfirmation this cycle; matches the open [[project_crypto_ai_desk_bias_tag_contradiction]] pattern (open longs tagged bias=short, previously confirmed on ZBT/ACE). Needs an operator session with DB access to check directly.
- **Crypto scalp mode dragging performance** — PF 0.10, totalR -4.5R (n=106) vs. intraday's PF 2.51/+53R — yet scalp signals are still actively firing tonight; unclear from read-only data whether this mode is meant to be disabled.
- **Weekend-mode signals underperform** (winrate 11%, n=137) — several active swing legs tonight are weekend-flagged (PUMP, POL, DOGE, ZEN, ENA, ETH, FF, COTI); size/confidence should stay conservative on those regardless of score.
- **Touch-based `final_r` accounting caveat** (per [[project_crypto_ai_desk_touch_based_pnl]]): tonight's crypto intraday/swing PF figures (2.51 / 1.69) are directionally positive but likely overstate realistic net PnL — do not read them as literal achievable returns.
- **Stocks book-wide weakness persists**: B-tier PF 0.56 (winrate 3%), C-tier PF 0.46 (winrate 12%) — consistent with continued drawdown-guard engagement; nothing actionable while the market is closed, but don't expect a clean stocks session on reopen without confirmation.

## 11. Action Plan — next 4 hours

1. Hold VIRTUAL/USDT and NEAR/USDT open legs; no fresh sizing at market — pullback-only for VIRTUAL, hold-as-is for NEAR.
2. Watch ACE/USDT for funding normalization + confirmed breakdown before treating it as a short entry; do not short into the current negative-funding/elevated-crowding setup.
3. Do not add fresh exposure to ZRO/USDT pending operator review of the exploit-adjacent headline.
4. Escalate XPL/USDT bias-tag question to an operator session with direct DB access — this is now unresolved across 4+ review cycles per the pattern in §14/§10.
5. Keep scalp-mode adds minimal given PF 0.10 this window; let existing scalp legs run to stop/target rather than adding new ones.
6. Re-check the macro-vs-price divergence (Iran/Strait-of-Hormuz risk-off score vs. still-risk-on crypto tape) at the 11:30 Europe/pre-US slot.

## 12. Final Verdict per Mode

- **Crypto scalp**: CAUTION — weak PF this window (0.10), let existing legs run, minimal new adds.
- **Crypto intraday**: NORMAL — best-performing mode tonight (PF 2.51), VIRTUAL/USDT is the standout; selective longs only.
- **Crypto swing**: NORMAL, catalyst-tilted — NEAR/TAO/ASTER (ai_narrative + adjacent baskets) are the strongest theses; PF 1.69 overall, weekend-flagged legs should stay conservative.
- **Stocks (all modes)**: CLOSED / WATCHLIST-ONLY — book-wide weak stats persist (B PF 0.56, C PF 0.46); nothing actionable until RTH confirmation at a later slot.

## 13. Sources

- Internal: [`data/processed/llm_analysis_packet.md`](data/processed/llm_analysis_packet.md) (generated 2026-08-25T01:28:42Z)
- Internal: [`data/catalysts/2026-08-25/catalyst_cycle_01-35.md`](data/catalysts/2026-08-25/catalyst_cycle_01-35.md)
- Internal: `active-signals` / `signal-stats` CLI outputs (crypto + stocks), captured 2026-08-25 ~04:40-04:50 EEST
- Internal: `data/scheduled_runs/2026-08-24_default_schedule/scheduler.log`, `data/scheduled_runs/2026-08-25_default_schedule/scheduler.log`
- Internal: prior review `OPUS_ENRICHED_REVIEW_AUTO_2026-08-24_2332.md` (23:34 EEST)
- **External web research unavailable this cycle** — no WebSearch/WebFetch tool call was made; all catalyst/legal claims above are sourced from the desk's own ingested `news_items`/catalyst pipeline (t.me/Bybit_Announcements, t.me/wublockchainenglish, BeInCrypto, CryptoSlate, PR Newswire, AMBCrypto, per the packet's own source attributions) rather than independently re-verified externally. Candidates whose verdict depends critically on external verification (none reached that threshold tonight — all are internal-data-consistent) would be demoted to manual-review; none required it this cycle.

## 14. Fix Requests / TODO

### TODO-stocks-swing-invest-stale
- **issue:** `data/reports/stocks/swing/` and `data/reports/stocks/invest/` last generated 2026-07-02 — roughly 7.5 weeks stale on a weekday run, despite stocks intraday reports generating normally every cycle.
- **evidence:** `ls -lat data/reports/stocks/swing/*.md` / `data/reports/stocks/invest/*.md` newest file dated 2026-07-02_13-03; today is 2026-08-25 (Tuesday).
- **suggested manual fix:** check the stocks swing/invest report-generation step in the scheduler pipeline for a silent failure or a stage that got disabled without the intraday stage being affected.
- **priority:** medium
- **first observed:** 2026-08-25 04:39 EEST

### TODO-xpl-bias-tag-unresolved
- **issue:** prior review (`OPUS_ENRICHED_REVIEW_AUTO_2026-08-24_2332.md`) flagged XPL/USDT as filled-long-vs-bias-short, unresolved for 3 consecutive cycles. This run's read-only sources (active-signals CLI, llm_analysis_packet.md) do not surface a bias-tag field, so the contradiction could not be independently reconfirmed or cleared this cycle.
- **evidence:** `OPUS_ENRICHED_REVIEW_AUTO_2026-08-24_2332.md` §8-10; this cycle's `active-signals --asset-class crypto` shows XPL/USDT swing `triggered`, direction=long, no bias field in the CLI table.
- **suggested manual fix:** an operator session with direct DB read access should query `proposed_signals` for XPL/USDT's `bias_tag` vs `direction` and resolve per [[project_crypto_ai_desk_bias_tag_contradiction]] (same pattern previously confirmed on ZBT/ACE, escalated to HIGH 2026-08-08).
- **priority:** high
- **first observed (this pattern):** 2026-08-08 (per memory); carried forward again 2026-08-25 04:39 EEST.

### TODO-crypto-scalp-mode-status-unclear
- **issue:** prior review referenced crypto scalp mode as "kill-switched off entirely" (`crypto_scalp_disabled`), but tonight's `active-signals --asset-class crypto` shows 10 scalp-mode signals actively waiting/triggered, and scalp-mode PF this window is 0.10 (totalR -4.5R, n=106) — the worst-performing mode by a wide margin.
- **evidence:** `active-signals --asset-class crypto` (this cycle) rows with `mode=scalp`; `signal-stats --asset-class crypto` "By mode" table, mode=scalp row.
- **suggested manual fix:** confirm current intended state of the crypto-scalp kill-switch in config (this run has no permission to inspect config directly under the read-only contract); if scalp is meant to stay disabled, investigate why signals are still being generated/tracked.
- **priority:** medium
- **first observed:** 2026-08-25 04:39 EEST (contradicts prior review's 2026-08-24 23:34 note)

### TODO-signal-stats-cli-slow
- **issue:** `signal-stats` CLI (both `--asset-class crypto` and `--asset-class stocks`) took over 5 minutes combined to return this cycle, well beyond the tool's normal response time and long enough to trip a 120s background-task timeout.
- **evidence:** command started ~04:42 EEST, completed ~04:50 EEST per this session's own tool timing.
- **suggested manual fix:** profile the `signal-stats` query path for a possible missing index or growing table-scan cost as `proposed_signals`/`signal_outcomes` accumulate rows.
- **priority:** low
- **first observed:** 2026-08-25 04:39 EEST
