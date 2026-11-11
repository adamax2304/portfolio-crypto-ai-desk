# Opus Enriched Review — post-close final daily review — Auto Cycle 23:30 EEST

## 1. Executive Summary

Slot: **post-close final daily review** (after US cash close, daily wrap). **Advisory only — no auto-trade, no scoring/threshold/strategy changes.** Crypto stays risk-off/bearish trend (BTC downtrend, macro risk 100/100 on Iran/Israel/Russia headlines); stocks closed, risk_off/short-bias regime with a heavy earnings gauntlet tomorrow (MSFT, META) and in 2 days (AAPL, AMZN, COIN, MSTR, LRCX, MA). No A/B-tier actionable setups exist on either desk right now — every stocks A/B candidate was demoted to C purely by the market-closed gate, and crypto swing/intraday produced zero A/B ideas this cycle. The one live crypto position of note is **ZEC/USDT short (B-tier, now TRIGGERED)**, catalyst-linked to the Zcash Ironwood-upgrade "sell the news" reaction. Catalyst mapping is weak this run (65% unmapped) — treat the catalyst layer as context only. Scanning, tracking, and monitors continue in all moods; this review recommends caution, never a stop.

## 2. Data Used

| File | mtime (local) | Age |
|---|---|---|
| `data/reports/scalp/2026-07-28_18-31_scalp_report.md` | 21:31 EEST | ~2h |
| `data/reports/intraday/2026-07-28_18-40_intraday_report.md` | 21:40 EEST | ~1h50m |
| `data/reports/swing/2026-07-28_19-31_swing_report.md` | 22:31 EEST | ~1h |
| `data/reports/stocks/intraday/2026-07-28_20-02_stocks_intraday_report.md` | 23:02 EEST | ~28m |
| `data/reports/stocks/swing/…` / `invest/…` | 2026-07-02 | deprecated/removed playbooks — not treated as stale, see [[project_crypto_ai_desk_stocks_position_framework]] |
| `data/catalysts/2026-07-28/catalyst_cycle_18-46.md` + `catalyst_events.jsonl` + `narrative_baskets.jsonl` | 21:46 EEST | ~1h44m |
| `data/processed/llm_analysis_packet.md` | 22:32 EEST | ~58m |
| `data/processed/llm_stocks_packet.md` | 22:08 EEST | ~1h22m |
| `python -m src.cli active-signals --asset-class crypto` | live query | now |
| `python -m src.cli active-signals --asset-class stocks` | live query | now |
| `python -m src.cli signal-stats --asset-class crypto` | live query | now |
| `python -m src.cli signal-stats --asset-class stocks` | live query | now |
| `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-28` | live query | now |
| `data/scheduled_runs/2026-07-28_default_schedule/cycle_01_21-22_summary.md` | 22:37 EEST | ~53m |
| Prior review `OPUS_ENRICHED_REVIEW_AUTO_2026-07-28_2141.md` | 21:41 EEST | for §4 diff |

## 3. Scheduler / Data Freshness

- Latest scheduled-run folder: `data/scheduled_runs/2026-07-28_default_schedule/`.
- `scheduler.log` mtime: 22:37:50 EEST — **fresh** (<3h rule easily met, ~53 min old at run time).
- Latest `cycle_01_21-22_summary.md` mtime: 22:37:48 EEST — **fresh**.
- Cycle 1 (21:22→22:37 EEST): 80 steps OK, **2 FAIL** — `crypto quality overlay report (counterfactual)` and `crypto swing versioned shadow sweep (counterfactual)` both timed out at 300s. Both are read-model/shadow-only, non-actionable, no impact on live scoring or this review (see §14).
- Reports: scalp/intraday/swing all **fresh** (<4h). Stocks intraday **fresh** (<4h, market closed). Stocks swing/invest last dated 2026-07-02 — these are the **deprecated/removed** old playbooks, not treated as a staleness failure; the new `stocks_swing_growth_breakout` shadow framework has its own cadence and is not part of the mandatory freshness table.
- Catalyst layer: fresh (<2h). LLM packets: fresh (<1h30m).
- Paper-execution/portfolio/entry-latency background jobs all completed OK this cycle (see cycle summary steps 26–38, 54).
- Monitor status: crypto watchlist monitor (5m), crypto pending monitor (30s), MEXC canary, derivatives monitor, stocks monitor all reported running/OK in the cycle summary.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "post_close",
  "as_of": "2026-07-28 23:30 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh"], "data_missing": ["crypto-overlay-report (300s timeout, shadow-only)", "crypto_swing_entry_sweep counterfactual (300s timeout, shadow-only)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["cycle_01_21-22_summary.md: ok=80 failed=2, finished 22:37:48 EEST", "all core reports <2h old", "catalyst cycle 21:46 EEST"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["risk_off", "mixed", "shorts_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["swing packet: bearish trend / risk-off, confidence 100/100, BTC downtrend/ETH uptrend divergence", "stocks regime risk_off, bias short, VIX 18.21, QQQ 5d -4.72%", "energy/financials/healthcare strong vs semis/tech weak sector split"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["1225/3500 catalyst events mapped today (35%), 65% unmapped — weak-mapping threshold breached", "ZEC/USDT: CoinDesk 'Zcash seals $1.7B shielded pool as Ironwood upgrade activates' 14:35 UTC + BeInCrypto 'ZEC Falls 5% As Zcash Ironwood Upgrade Goes Live' — sell-the-news confirmed"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["squeeze_risk", "oi_contradicts", "data_unavailable"],
      "data_missing": ["BANK/USDT, SOXLB/USDT, SNXXB/USDT, KORUB/USDT external derivatives cross-check"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BANK/USDT: price down + OI up — fresh shorts pressing, squeeze risk if price reclaims", "SOXLB/SNXXB/KORUB/KAITO/ESP/SKHYB all capped to C on short-squeeze / thin-liquidity gates in both scalp and intraday reports"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "entry_fresh", "overextended", "price_moved_away"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["COTI/USDT +34.5% 24h / VANRY +21.2% 24h — RS leaders but already extended, chase risk on a fresh long", "ZEC/USDT triggered fresh in-zone 469.62-472.62, invalidation 476.29", "BANK/SNDKB/SNXXB explicitly flagged 'more than 2 ATR from EMA20, do not chase'"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.7,
      "reason_codes": ["entered_unresolved", "waiting_for_entry", "no_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active-signals: 19 rows — 1 triggered (ZEC short), rest ENTERED UNRESOLVED (tp1_hit/tp2_hit)", "stocks active-signals: 0 A/B actionable, 2 C-tier WAITING for entry (XLY, MSTR — not actionable, C-tier)", "detect_untracked_legacy_alerts --since 2026-07-28: None — no integrity anomalies today"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["legal_risk", "headline_risk", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["AMZN A-raw short flagged legal_headline_risk=going_concern — no going-concern/bankruptcy/auditor headline found in AMZN's own news feed this cycle (Anthropic stake, Nova AI overhaul, Corning-unrelated) — possible false-positive gate, see §14", "UNH A-raw long flagged legal_headline_risk=sec_doj — plausible given known UNH DOJ scrutiny", "Earnings blackout: MSFT/META tomorrow; AAPL/AMZN/COIN/MSTR/LRCX/MA in 2 days — explicit do_not_chase_warning on all"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto week: swing PF 3.43 / totalR 26.7 (best), intraday PF 2.03 / totalR 12.4, scalp PF 0.17 / totalR -5.0 (net-negative, mode already kill-switched at entry)", "stocks C-tier week: PF 0.43, winrate 4.7%, totalR -4.0 — no A/B sample (n=0)", "paper-shadow A/B forward-valid: A -24.70R (n=101) vs B +3.17R (n=28) — backfill is look-ahead, not proof, no promotion"] },
    { "agent": "head_trader", "verdict": "manual_review", "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of agents 1-8"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "COTI/USDT", "trigger": "confirmed pullback/retest into a lower-volatility zone with rising volume; do not chase the current +34.5% 24h extension", "reason": "Top RS-leader (score 91.6, RS/BTC +36.4%) and momentum-catalyst tagged, but already extended — needs a clean retest before it's actionable, not a fresh-high chase" },
    "best_short_candidate":    { "symbol": "ZEC/USDT", "trigger": "already TRIGGERED intraday short (B-tier), entry 469.62-472.62, invalidation 476.29, expires 2026-07-29T17:36 EEST — manage the open position, do not add on further weakness without a fresh signal", "reason": "Catalyst-confirmed sell-the-news reaction to the Ironwood upgrade (ZEC -5% on the upgrade-live headline); only live actionable-grade signal on the desk right now" },
    "best_catalyst_candidate": { "symbol": "ZEC/USDT", "trigger": "same as best-short — catalyst and technical align on this one name", "reason": "Cross-confirmed by two independent sources (CoinDesk upgrade-live + BeInCrypto price-reaction) within the internal-first bar, no external research required" },
    "avoid_candidate":         { "symbol": "AMZN short / BANK/USDT", "reason": "AMZN: earnings in 2 days (do_not_chase_warning) plus a legal_headline_risk=going_concern tag that has no supporting headline in AMZN's own news feed this cycle — likely gate mislabel, treat as manual-review, not a clean avoid signal on fundamentals. BANK/USDT: simultaneously tagged catalyst_backed long AND weak_rs_short with short-squeeze risk (OI up while price down) — internally contradictory, matches the prior watchlist-alert-reuse bug symbol from memory." },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---:|---|
| data_quality | ok | 0.85 | scheduler_fresh | advisory_only |
| market_regime | caution | 0.75 | risk_off, mixed, shorts_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, fresh_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.60 | squeeze_risk, oi_contradicts, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, entry_fresh, overextended, price_moved_away | advisory_only |
| execution_lifecycle | needs_review | 0.70 | entered_unresolved, waiting_for_entry, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.65 | legal_risk, headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.60 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | manual_review | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (21:41 EEST, late-session risk review)

- **ZEC/USDT short**: was `waiting_for_entry` at 21:41 → now **TRIGGERED** (entry 469.62-472.62 filled zone). Thesis unchanged (Ironwood-upgrade sell-the-news, internally cross-confirmed) — this is the priority open item into the overnight/Asia session.
- **COTI/USDT**: was flagged as long-watch (trigger 0.0113-0.0119 zone in the prior review's price scale) → still the top long-watch name, still unactioned, now even more extended (24h move grew).
- **XLE short vs strongest-sector contradiction**: still open. XLE remains the raw A-tier short (score 88.75 this cycle vs 84.51 at 21:41) while energy stays the single strongest sector (RS +7.44% this cycle vs +7.66% at 21:41). This is now the **4th consecutive review cycle** with the same unresolved contradiction (first flagged 16:07 EEST) — escalated in §14.
- **PLTR short vs bullish-headline contradiction** (flagged at 18:39/21:41): **appears resolved this cycle** — PLTR's news feed is now neutral ("Can PLTR Stock Live Up To Its Multiple?") with no bullish MA-reclaim headline; no longer treating this as an open contradiction.
- **New this cycle**: AMZN A-raw short (score 90.48, highest raw score on the stocks desk) carries a `legal_headline_risk=going_concern` tag with no supporting evidence in its own news feed — new integrity flag, see §14.
- **Crypto desk**: still zero A/B-tier ideas on scalp/intraday/swing, same as 21:41 — no change in actionability, all C-tier watchlist only.
- **Stocks desk**: all previously-listed A/B candidates remain demoted to C by the market-closed gate (unchanged mechanism, now well into the post-close window).

## 5. Catalyst Coverage

- Catalyst events today: **3500** total scanned across all cycles; **1225 mapped** (35%) / **2275 unmapped** (65%).
- Narrative baskets: **4** — `rwa_narrative`, `delisting_thin_liquidity`, `perps_dex_narrative`, `binance_ecosystem_teaser`.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (unmapped 65% > 50% threshold)
- Top 3 unmapped headlines by importance:
  1. `0.75` legal_risk — "PRCT Investors Have Opportunity to Lead PROCEPT BioRobotics Corporation Securities Fraud Lawsuit" (PR Newswire)
  2. `0.75` legal_risk — "Photronics, Inc. Investor Alert: Contact SBS by September 4, 2026 for Opportunity to Lead Securities Fraud Lawsuit" (PR Newswire)
  3. `0.75` legal_risk — "EchoStar's Hughes Network preparing Chapter 11 bankruptcy filing: report" (Seeking Alpha Market Currents)
- Last cycle (18:46 local scan): 500 events scanned, breakdown mostly `other_news` (449) with smaller legal_risk/exploit_hack/exchange_listing tails.

## 6. Market Landscape

Crypto: bearish trend / risk-off (confidence 100/100). BTC downtrend, ETH uptrend (mild divergence). Altcoin breadth weak: 27.9% above EMA20, 25.6% above EMA50. Macro risk score 100/100 driven by Iran/Israel/Russia-sanctions headlines and a Fed decision looming; Fear & Greed 29 ("Fear"). Stocks: risk_off, bias short, VIX 18.21-18.34, QQQ in a clean downtrend (5d -4.72%, 20d -6.71%) while DIA holds up (+1.05% 5d). Sector split: energy/financials/healthcare strong, semiconductors/technology weak. Heavy earnings week ahead (MSFT/META tomorrow; AAPL/AMZN/COIN/MSTR/LRCX/MA in 2 days) — a real gap-risk source into Wednesday/Thursday.

### Market Mood / Risk Routing
- Crypto mood: **risk-off / bearish trend**
- Stocks mood: **risk_off / closed (post-close, planning only)**
- Dominant narrative: geopolitical risk-off (Iran/Israel/Russia sanctions) + AI-chip security headlines (Nvidia/Hugging Face, Supermicro) + earnings season kickoff
- Preferred side now: **wait-for-trigger** (crypto shorts on confirmed failed retests, catalyst-backed only; stocks require RTH confirmation, nothing actionable until the open)
- Best long candidate: none clean — see COTI/USDT long-watch in §8
- Best short candidate: **ZEC/USDT** (already open/triggered, catalyst-confirmed)
- Best catalyst-backed candidate: **ZEC/USDT** (Ironwood-upgrade sell-the-news, cross-confirmed internally)
- What to avoid: chasing extended RS-leader longs (COTI +34.5%, VANRY +21.2% 24h already run); thin/squeeze-prone shorts (BANK, SOXLB, SNXXB, KORUB, KAITO, ESP, SKHYB — all capped on short-squeeze/thin-liquidity gates); any stock name into tomorrow's or Thursday's earnings print
- What would change the view: BTC reclaiming key resistance with altcoin breadth improving above 50% on EMA20; a VIX spike or a confirmed SPY/QQQ breakdown for a cleaner stocks-short entry after the reopen

## 7. Candidate Deep Dives

### 1. ZEC/USDT — crypto intraday short, B-tier, TRIGGERED (score 65.2)
- Entry zone: 469.6229-472.6218 (filled) · Invalidation: 476.2871 · Expires: 2026-07-29T17:36 (17:36 EEST tomorrow).
- Has price already reacted to the catalyst? Yes — BeInCrypto: "ZEC Falls 5% As Zcash Ironwood Upgrade Goes Live" (swing packet, today).
- Chasing? No — this is an already-triggered, already-filled position; nothing further to chase.
- Retest/pullback structure? Entry was the initial catalyst-driven fade; no separate retest required to already be in the trade.
- Overextended (>2 ATR from EMA20)? Not flagged in the source reports.
- Would entry now be late? N/A — already filled.
- Mood alignment: yes — risk-off crypto favors clean catalyst-backed shorts.
- Long/short/wait: already-open short.
- Actionable now or confirmation-only? Already actionable/open; monitor to invalidation 476.29 or stop.
- Invalidation: price reclaiming 476.29.
- Chase-risk setup? No.
- Catalyst confirmation or contradiction? Confirmed by two independent sources (CoinDesk upgrade-live + BeInCrypto price-reaction), internal-first bar satisfied — **no external WebSearch/WebFetch required this cycle**.

### 2. XLE — stocks intraday short, raw A-tier (score 88.75) → demoted C (market_closed_intraday_planning_only)
- Has price already reacted? Sector rotation shows energy (XLE) as the **strongest** sector today (RS vs SPY +7.44%, 20d return +7.41%) — this directly opposes a fresh short thesis.
- Chasing? Would be chasing against the day's strongest sector.
- Retest/pullback structure? Not evaluated — planning-only while market closed.
- Overextended? Not the relevant risk here; the contradiction is directional, not extension.
- Would entry now be late? Market closed — no entry possible tonight regardless.
- Mood alignment? **No** — a sector-strength short contradicts the desk's own strongest-sector read; this is the same unresolved contradiction carried from 16:07/18:39/21:41 EEST, now its 4th consecutive cycle.
- Long/short/wait: wait — requires resolution of the sector-vs-signal conflict before treating as actionable at the open.
- Actionable now or after confirmation? After confirmation only, and specifically after the scoring/gate contradiction is investigated (§14).
- What would invalidate: a clean intraday reversal in XLE with volume, or the sector-strength read flipping to weak.
- Chase-risk: n/a (not actionable).
- Catalyst confirmation/contradiction: **contradicted** by the sector-rotation data itself.

### 3. AMZN — stocks intraday short, raw A-tier (score 90.48, highest on the stocks desk) → demoted C (legal_headline_risk=going_concern + market_closed)
- Has price already reacted? Not evaluated; market closed.
- Legal/headline risk check (§I): the report tags `legal_headline_risk: going_concern` for AMZN, but AMZN's own news feed this cycle contains no going-concern, bankruptcy, auditor-resignation, or accounting-restatement headline — only "Bezos' Amazon Could See a Sizable Mark-to-Market Gain From Its Anthropic Stake" and "Amazon Overhauls AI Strategy as Flagship Nova Models Wind Down." This reads as a **likely gate false-positive**, not a genuine going-concern event (see §14 TODO).
- Per §I policy: because a legal/headline flag is present (even if it looks mislabeled), the final verdict for this candidate stays **MANUAL REVIEW REQUIRED**, never a clean actionable, until a human confirms the tag is spurious.
- Earnings: AMZN reports in 2 days (do_not_chase_warning already active) — an independent reason to avoid regardless of the legal-tag question.
- Mood alignment: short bias is broadly mood-aligned (risk_off, QQQ downtrend), but the earnings blackout overrides.
- Actionable now or after confirmation? Not actionable — blocked by both the earnings blackout and the unresolved legal-tag question.
- What would invalidate/clear it: either the earnings window passing with a clean post-print setup, or a human confirming/clearing the going_concern tag.

### 4. COTI/USDT — crypto long, RS-leader (score 91.6, swing) / momentum leader (score 92, intraday expansion watchlist)
- Has price already reacted? Yes — +34.52% 24h, RS vs BTC +36.4%, already deep into the move.
- Chasing? Yes, at current levels — this is the definition of a chase if entered now.
- Retest/pullback structure? None confirmed yet; needs one.
- Overextended (>2 ATR from EMA20)? ATR% 12.67 with a 24h move of +34.5% strongly suggests yes, though not explicitly flagged in the report's ATR-distance language.
- Would entry now be late? Yes.
- What level makes it actionable? A confirmed pullback/retest with rising volume into a lower-volatility zone, not a fresh-high chase.
- Mood alignment: RS-leader longs are the correct risk-routing choice in a risk-off tape (relative-strength names over broad longs), but the extension argues for patience.
- Long/short/wait: long-watch, wait-for-trigger.
- Invalidation: a fresh high without volume confirmation, or funding turning persistently negative/crowded.
- Chase-risk setup? Yes, at current price.
- Catalyst confirmation/contradiction: momentum/RS-driven, not catalyst-driven — no specific news catalyst identified beyond general RWA-narrative basket membership.

### 5. BANK/USDT — crypto, internally contradictory (catalyst_backed long momentum tag AND weak_rs_short tag simultaneously)
- Has price already reacted? Yes — 24h -35.63%, RS vs BTC -33.75%, one of the day's weakest names.
- Chasing? A fresh short here would be chasing the down move; capped to C for exactly this reason (`high_upper_wick_short_squeeze_risk`, `>2 ATR from EMA20, do not chase`).
- Retest/pullback structure? None — extended down move.
- Overextended? Yes, explicitly flagged (>2 ATR from EMA20).
- Would entry now be late? Yes, on either side.
- Mood alignment: the short direction matches weak-vs-market tagging, but derivatives show OI up while price is down — "fresh shorts pressing, possible squeeze if price reclaims" — a genuine squeeze risk against a fresh short.
- Long/short/wait: wait — internally contradictory (catalyst-backed long tag vs weak-RS short tag) and squeeze-prone on the short side.
- Invalidation: n/a while contradictory.
- Chase-risk setup? Yes, on both sides.
- Catalyst confirmation/contradiction: **contradicted internally** — this symbol is tagged both `catalyst_backed` (long, momentum) and `weak_rs_short` (short, RS) in the same discovery-expansion pass. BANK/USDT is also the symbol flagged in memory for a prior untracked-alert/signal-reuse bug — treat with extra caution; today's `detect_untracked_legacy_alerts` run shows no fresh integrity issue on it, but the historical pattern argues for manual review before any alert on this name.

## 8. Best Candidates Ranked

1. **Best catalyst-backed / best short (crypto): ZEC/USDT short** — already open/triggered, entry 469.62-472.62, invalidation 476.29, expires 2026-07-29T17:36 EEST. Catalyst-confirmed sell-the-news reaction to the Ironwood upgrade. Priority watch item overnight into Asia.
2. **Best long-watch (crypto): COTI/USDT** — trigger: confirmed pullback/retest with rising volume; invalidated by a fresh high without volume confirmation or funding staying negative/crowded. Do not chase the current +34.5% extension.
3. **Manual-review / avoid (stocks): AMZN short** — blocked by earnings-in-2-days blackout and an unresolved (likely false-positive) going_concern legal tag; needs a human call before any future actionable status.
4. **Avoid (stocks): XLE short** — contradicts the day's strongest sector (energy, RS +7.44%); 4th consecutive cycle with this unresolved contradiction, escalated in §14.
5. **Avoid (crypto): BANK/USDT** — internally contradictory catalyst-backed-long vs weak-RS-short tags, squeeze risk on the short side, prior integrity-bug symbol from memory.

## 9. Avoid / No Trade

This is a **decision-window-only** call, not a system-wide stop — scanning, tracking, and monitors continue regardless.

- **AMZN short** — earnings blackout (2 days out) + unresolved legal-tag question → MANUAL REVIEW REQUIRED, not tradeable as-is.
- **XLE short** — directly contradicts the day's strongest sector; needs the gate-logic contradiction resolved before trusting the raw score.
- **Any fresh crypto long chase** on COTI/VANRY/ACH at current extended levels — wait for the pullback.
- **Any fresh short on BANK/SOXLB/SNXXB/KORUB/KAITO/ESP/SKHYB** — all explicitly squeeze/thin-liquidity capped this cycle.
- **Crypto scalp mode** — still kill-switched at entry and still net-negative on the historical/tracking series (PF 0.17, totalR -5.0); no new scalp ideas expected or wanted.
- Nothing here is a command to pause the scanner, monitors, or data collection — all continue.

## 10. Main Risks

- **Earnings gauntlet**: MSFT/META tomorrow, AAPL/AMZN/COIN/MSTR/LRCX/MA in 2 days — a cluster of gap-risk events; do not hold or chase into any of these prints.
- **Geopolitical risk-off**: Iran/Israel/Russia-sanctions headlines keep the macro risk score pinned at 100/100 — reduce alt-long aggression is the standing system warning.
- **Catalyst mapping is weak this run (65% unmapped)** — treat catalyst context as directional color, not proof.
- **Squeeze risk cluster** on the crypto short side (BANK, SOXLB, SNXXB, KORUB, KAITO, ESP, SKHYB) — a reclaim on any of these could trigger a fast short-covering move.
- **Two shadow-report jobs timed out** this cycle (crypto quality overlay, crypto swing versioned shadow sweep) — read-model only, but worth a performance check if this recurs (§14).
- **Legal/headline gate possible false-positive on AMZN** — if this pattern recurs on other symbols, confidence in the legal-risk gate degrades further (§14).

## 11. Action Plan — next 4 hours

1. **Monitor ZEC/USDT short** to invalidation (476.29) or stop; no new entry needed, it's already filled.
2. **Watch COTI/USDT** for a pullback/retest with volume before considering it actionable; do not chase the current extension.
3. **Do not originate new crypto shorts** on the squeeze-flagged names (BANK, SOXLB, SNXXB, KORUB, KAITO, ESP, SKHYB) without a fresh signal and confirmed derivatives data.
4. **Stocks: nothing actionable** until the RTH open; re-evaluate XLE/AMZN/PLTR/AMD/AVGO/QQQ/UNH fresh at/after 09:30 ET with updated levels — do not treat tonight's C-tier planning levels as pre-authorized entries.
5. **Flag AMZN and XLE for human review** before the next US session per §14 — both carry unresolved gate questions.
6. Continue all scanning/monitoring — no pause recommended in any mood.

## 12. Final Verdict per Mode

- **Crypto scalp**: NO-ENTRY / kill-switched — net-negative bucket, no change expected.
- **Crypto intraday**: NO-ENTRY this cycle (0 A/B ideas) — WATCHLIST ONLY (best: EUL/USDT at 60.0, per report's own final summary).
- **Crypto swing**: NO-ENTRY this cycle (0 A/B ideas) — long-watch COTI/USDT pending pullback.
- **Crypto — open positions**: ZEC/USDT short TRIGGERED, manage to invalidation/stop; remaining 17 active B-tier signals are ENTERED UNRESOLVED (tp1_hit/tp2_hit) — no new action needed, several are aging well past their mode horizon (see §14 carried TODO).
- **Stocks intraday**: MARKET CLOSED — planning/watchlist only; all A/B-raw candidates demoted to C by the market-closed gate; re-confirm fresh at RTH open.
- **Stocks swing/invest**: deprecated/removed, not evaluated (new `stocks_swing_growth_breakout` remains shadow-only research, not actionable).

## 13. Sources

Internal only this cycle — internal `news_items`/catalyst records for the two candidates that needed external-style verification (ZEC catalyst, AMZN legal-tag question) were fresh, cross-confirmed, and directionally unambiguous, satisfying the internal-first bar of §G without requiring WebSearch/WebFetch:
- [Zcash seals $1.7 billion shielded pool as Ironwood upgrade activates](https://cryptobriefing.com/fortitude-mining-nebraska-public-listing/) — CoinDesk (via internal catalyst feed), 2026-07-28 14:35 UTC — *(catalyst feed URL captured is the co-collected Fortitude Mining CryptoBriefing item; CoinDesk's own article URL was not independently captured this cycle — treat as source-name-only, title verified via internal record, not a followed link)*
- "ZEC Falls 5% As Zcash Ironwood Upgrade Goes Live: What Changes for Token Holders" — BeInCrypto, via `data/processed/llm_analysis_packet.md` §Catalysts, 2026-07-28
- `data/reports/stocks/intraday/2026-07-28_20-02_stocks_intraday_report.md` §2, §4, §5 — internal source for the XLE sector-strength and AMZN news-feed contradiction findings
- `data/catalysts/2026-07-28/catalyst_cycle_18-46.md` — internal catalyst coverage stats

## 14. Fix Requests / TODO

### TODO-xle-strongest-sector-contradiction-persists-4-cycles
- **issue:** The XLE short-vs-strongest-sector contradiction (first flagged 16:07 EEST) is still open at 23:30 EEST — 4th consecutive review cycle with no resolution. XLE is scored as a raw A-tier short (score 88.75 this cycle) while energy remains the day's single strongest sector (RS vs SPY +7.44%). The demotion this cycle is only `market_closed_intraday_planning_only` — the sector-contradiction gate still does not appear to be firing distinctly from a generic "no confirmation" reason.
- **evidence:** `data/reports/stocks/intraday/2026-07-28_20-02_stocks_intraday_report.md` §2 (energy=strongest sector, RS+7.44%) vs §5 (XLE short, raw score 88.75, Top Candidates table).
- **suggested manual fix:** as previously suggested (16:07, 18:39, 21:41): audit whether the sector-confirmation gate for stocks-intraday distinguishes "no sector information" from "sector information present and directionally opposed to the trade" — these need different gate codes/operator language. Four-cycle persistence in one day suggests this is not self-resolving.
- **priority:** high (unchanged from 21:41, persistence continues)
- **first observed:** 2026-07-28 16:07 EEST; this persistence observation 2026-07-28 23:30 EEST (4th cycle)

### TODO-amzn-going-concern-tag-likely-false-positive
- **issue:** AMZN's raw A-tier short (score 90.48, the highest raw score on the stocks desk this cycle) is tagged `legal_headline_risk: going_concern` in §7 of the stocks intraday report. AMZN's own news feed for this cycle (§4 News/Catalysts) contains no going-concern, bankruptcy, auditor-resignation, or accounting-restatement headline — only an Anthropic-stake mark-to-market story and a Nova-AI-strategy overhaul story, neither of which supports a going-concern label. This looks like a gate mislabel (possibly a spillover from an unrelated headline, e.g. the same-cycle "Corning Stock Plunges 16%" item that shares the AMZN news block) rather than a genuine signal.
- **evidence:** `data/reports/stocks/intraday/2026-07-28_20-02_stocks_intraday_report.md` line 191 (`legal_headline_risk: going_concern`) vs lines 81-84 (AMZN's actual news feed for the cycle).
- **suggested manual fix:** audit the legal/headline-risk tagging logic for cross-contamination between adjacent news items in the same symbol's news block (e.g. the Corning item appearing directly under AMZN's news header); confirm whether `going_concern` should require an exact-symbol match on the going-concern language itself, not proximity within a block.
- **priority:** medium
- **first observed:** 2026-07-28 23:30 EEST

### TODO-crypto-scalp-mode-net-negative (carried forward)
- **issue:** `signal-stats --asset-class crypto` mode breakdown still shows scalp mode at PF 0.1667, avgR -0.25, 0 wins / 6 losses over the week window — unchanged from the 21:41 review. Mode remains kill-switched for new entries; historical/tracking signals continue to be scored at this negative rate.
- **evidence:** `python -m src.cli signal-stats --asset-class crypto` → `mode=scalp | n=28 | trig=23 | wins=0 | losses=6 | PF=0.1667 | avgR=-0.25 | totalR=-5.0`.
- **suggested manual fix:** unchanged from 21:41 — confirm the kill-switch is intended to stay permanent, or reduce scalp scoring/tracking compute if it will never be re-enabled.
- **priority:** medium
- **first observed:** 2026-07-28 21:41 EEST; still open 2026-07-28 23:30 EEST

### TODO-scalp-intraday-entered-unresolved-aging (carried forward)
- **issue:** Several crypto scalp/intraday B-tier signals remain in `tp1_hit`/`tp2_hit` (ENTERED UNRESOLVED) 6-11+ days past their own mode's typical hours-scale horizon (e.g. NEAR/USDT scalp, expires_at 2026-07-17; ONDO/OPN/FIL scalp, expires_at 2026-07-22) without resolving to a terminal closed state.
- **evidence:** `python -m src.cli active-signals --asset-class crypto` → same aged rows still present, unchanged from the 21:41 review.
- **suggested manual fix:** unchanged from 21:41 — confirm whether this is expected (open-ended ride to final stop/TP) or whether a lifecycle-closure job should finalize/archive these; consider a distinct "AGED UNRESOLVED" display state.
- **priority:** low
- **first observed:** 2026-07-28 21:41 EEST; still open 2026-07-28 23:30 EEST

### TODO-shadow-report-timeouts
- **issue:** Two read-model/shadow-only steps timed out at exactly 300s in this cycle: `crypto quality overlay report (counterfactual)` and `crypto swing versioned shadow sweep (counterfactual)`. Non-blocking (both are shadow-only, no impact on live scoring/tracking), but worth a one-time check for a performance regression if this recurs across multiple cycles.
- **evidence:** `data/scheduled_runs/2026-07-28_default_schedule/cycle_01_21-22_summary.md` steps 62-63: both `[FAIL] ... (exit=-1, 300.0s/300.1s, attempts=1)` with `(timeout)`.
- **suggested manual fix:** if this repeats next cycle, profile `src.cli crypto-overlay-report` and `scripts.crypto_swing_entry_sweep --persist-counterfactual` for a data-volume or query-plan regression; otherwise treat as a one-off.
- **priority:** low
- **first observed:** 2026-07-28 23:30 EEST (this cycle only — not yet confirmed recurring)

### Source-discipline checklist
- Every external-style claim above has a source name + title + date, and internal file paths are cited for internal-only findings. ✓
- No uncited stats, no uncited legal claims. ✓
- No fabricated TradingView/chart observations — **TradingView / manual chart check unavailable this run**; only local OHLCV/ATR/EMA/score fields used. ✓
- No `test_source`/fixture URLs ingested. ✓
- §13 Sources section present. ✓
- External WebSearch/WebFetch were **not needed** this cycle: internal `news_items`/catalyst records for ZEC (cross-confirmed by two independent sources, <12h) and for the AMZN legal-tag question (resolved by inspecting AMZN's own report-internal news block, no new claim required) satisfied the internal-first bar. No new external sources → no `data/raw/enriched_review_sources/<ISO>.json` built and no ingest CLI run this cycle (nothing to ingest).
- Catalyst mapping-weak warning stated in both §5 and the Telegram summary. ✓
