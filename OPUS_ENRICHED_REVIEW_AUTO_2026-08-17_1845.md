# Opus Enriched Review — US open reaction review — Auto Cycle 18:45 EEST

## 1. Executive Summary

**US open reaction review, 18:45 EEST (15:45 UTC / ~11:45 ET) — US cash session ~2h15m old. Advisory only — no auto-trade.** Stocks tape is clean risk-on: VIX 14.98, all 4 major indices in uptrend, breadth 100% above EMA20/50 — but the stocks-intraday report itself is a **pre-open snapshot (generated 15:35 UTC / 8:35 ET, before the 9:30 ET open)**, so none of today's actual post-open price action is reflected in the scored candidates; treat all stock verdicts below as pre-open-context, not post-open-confirmed. Crypto stays **range/chop**: BTC range-bound, ETH transition_up, altcoin breadth ~52%, macro/geopolitics risk scored **100/100** (Houthi attack on a Saudi vessel, Russia-Ukraine escalation, Coldcard hardware-wallet exploit now ~1,700-2,055 BTC stolen) — a risk-off macro overlay sitting on top of range-bound price action, not a clean risk-off tape. **Carried-forward critical data-integrity issue, now confirmed a 4th consecutive cycle: 11 crypto symbols remain frozen on OHLCV at 2026-08-15 22:30 UTC (~41h stale)** — six of them (HOLO, AVNT, PROM ×2, LUNA, MMT, BABY) are live open crypto swing positions whose displayed price/TP/SL state is unverified; no remediation in ~44h of tracking. Best stocks long-watch: **GE** (A-tier, capex/industrial-AI tailwind, cleanest actionable). Best stocks short-watch: **META**, but downgraded to **manual review** for a fresh, primary-sourced legal-risk headline (CNBC: federal child-safety trial reaching a "critical moment," today). Best crypto long-watch: **WLFI/USDT** (B-tier swing, triggered) — flagged for a bias-tag contradiction (system labels it short-biased today while an active long position runs). Avoid: chasing **GPS/USDT** or **ACE/USDT** — both are overextended momentum-breakout names explicitly tagged `avoid_chase`/`wait_pullback`, not fresh entries.

## 2. Data Used

- Scheduler: `data/scheduled_runs/2026-08-17_default_schedule/scheduler.log` (mtime 18:06 EEST, ~39min old — fresh). No `cycle_*_summary.md` present in today's folder (only raw monitor logs); scheduler.log freshness alone clears the 3h defer threshold.
- Reports: scalp `2026-08-17_11-13` (gen 14:13 EEST, ~4h32m old), intraday `2026-08-17_14-05` (gen 17:05 EEST, ~1h40m old, freshest crypto read), swing `2026-08-17_04-22` (gen 07:22 EEST, ~14h17m old — **stale**, no fresher swing scan today, used with caveat), stocks intraday `2026-08-17_15-35` (gen ~18:35 EEST, freshest file but data as-of 15:35 UTC = 8:35 ET, **pre-open** — planning context only for today's post-open reaction), stocks swing/invest `2026-07-02` (6+ weeks stale, expected/deprecated per prior context).
- Catalysts: `data/catalysts/2026-08-17/catalyst_events.jsonl` (1,672 events today, mtime 17:11 EEST), `narrative_baskets.jsonl` (3 baskets), `catalyst_cycle_14-11.md` (latest cycle summary, 500 events scanned this cycle).
- LLM packets: `llm_analysis_packet.md` (17:06 EEST), `llm_stocks_packet.md` (17:38 EEST) — both fresh.
- CLI: `active-signals --asset-class crypto` (n=46), `active-signals --asset-class stocks` (n=50), `signal-stats --asset-class crypto` (A/B headline sample=71, PF 2.72, totalR +24.1), `signal-stats --asset-class stocks` (A/B headline sample=23, PF 0.0, totalR -1.0; C-tier n=575, PF 0.14, totalR -9.5), `detect_untracked_legacy_alerts --since 2026-08-17` → **clean, no untracked alerts**.
- Direct SQL: `news_items` last-4h scan (40 rows, mostly PR-wire noise, one AMZN/WMT partnership rumor later self-corrected) and per-symbol 24h scan for the 5 stocks A/B candidates.
- Direct OHLCV CSV re-check (`data/raw/ohlcv/binance/15m/*.csv`) for the 6 previously-flagged frozen crypto swing symbols plus 2 fresh control symbols (WLFI, CHIP) — confirms the freeze is still pair-specific, not global.
- `reports/PAPER_MONITOR_STATUS_LATEST.md` — present but stale this cycle (mtime 15:35 EEST, ~3h old at session start); not used as the primary lifecycle source this cycle, active-signals CLI output used instead.
- Prior review for comparison: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-17_1559.md` (pre-US-open decision review, 15:59 EEST).
- **External web research not attempted this cycle** — internal data (fresh reports, live news_items, live OHLCV re-check) was sufficient and internally consistent for every candidate; no contradiction requiring external verification per §G. **External web research unavailable-by-choice, not by tool failure** — noted per source-discipline checklist.

## 3. Scheduler / Data Freshness

- Scheduler fresh (~39min). No cycle-summary file exists in today's folder (only `derivatives_monitor_*.log` / `fast_news_monitor_*.log`, both actively updating within the last minute) — does not block the review per §D (only scheduler.log + latest cycle summary jointly stale triggers deferral, and scheduler.log alone is fresh).
- Crypto reports: scalp 4h32m old (stale relative to a scalp horizon, but no fresher scan exists), intraday 1h40m old (fresh), swing 14h17m old (**stale**, >14h threshold — used only because no fresher swing source exists, flagged).
- Stocks intraday: freshest file this cycle but its data-as-of timestamp (8:35 ET) predates the 9:30 ET open by ~1h — **this is a pre-open snapshot being read at post-open time**; no post-open stocks scan has run yet this cycle. Treat all stocks scores/entries below as pre-open-context.
- **Data-integrity carry-forward, confirmed for the 4th consecutive cycle today (04:40 → 11:40 → 15:59 → now):** 11 crypto symbols frozen on 15m OHLCV at 2026-08-15 22:30:00 UTC (now ~41h stale). Direct re-check of HOLO, AVNT, PROM, LUNA, MMT, BABY (all 6 are open crypto swing signals in the current active-signals pull) confirms all 6 are still frozen at the exact same last row. Control symbols WLFI (last row 2026-08-17 13:45 UTC) and CHIP (last row 2026-08-17 15:30 UTC) are fresh — confirms this is pair-specific, not a global feed outage. No progress on remediation in ~44h. See TODO-1.
- `detect_untracked_legacy_alerts --since 2026-08-17`: **clean** — every legacy crypto alert has a backing proposed_signal.
- Signal-duplication anomaly observed this cycle (new): the stocks active-signals pull shows INTC ×4, BAC ×2, and GE ×3 as separate `signal_id` rows sharing identical entry_low/entry_high/invalidation/expires_at within the same tier+mode — consistent with duplicate signal emission rather than 4/2/3 genuinely distinct setups. See TODO-2.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-08-17 18:45 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "bad", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["stocks swing/invest 6wk+ stale (expected/deprecated)", "no post-open stocks scan yet this cycle", "PAPER_MONITOR_STATUS_LATEST.md stale (~3h) so not used as primary lifecycle source"],
      "suggested_effect": "advisory_only",
      "facts_used": ["11 crypto symbols frozen at 2026-08-15 22:30 UTC (~41h stale), confirmed 4th consecutive cycle, 6 are live open swing positions", "stocks intraday report is a pre-open (8:35 ET) snapshot being read ~2h15m after the 9:30 ET open", "duplicate signal_id rows for INTC/BAC/GE with identical entry/expiry"] },
    { "agent": "market_regime", "verdict": "mixed", "confidence": 0.7,
      "reason_codes": ["mixed", "risk_on", "chop", "wait_for_trigger"],
      "data_missing": ["no live post-open stocks price action"],
      "suggested_effect": "advisory_only",
      "facts_used": ["stocks: bullish regime label, VIX 14.98, breadth 100% above EMA20/50, all 4 indices uptrend", "crypto: BTC trend range, ETH transition_up, altcoin breadth 52.5% above EMA20", "macro/geopolitics risk 100/100 (Houthi attack on Saudi vessel, Russia-Ukraine, Coldcard exploit) sitting on top of range-bound crypto price action"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "catalyst_contradicted", "narrative_supported"],
      "data_missing": ["most C-tier stocks symbols: zero internal catalyst hits"],
      "suggested_effect": "advisory_only",
      "facts_used": ["1,672 catalyst events today, 68% unmapped (534/1672 mapped) — mapping weak this run", "3 narrative baskets: delisting_thin_liquidity (ATOM), rwa_narrative (ONDO/XLM), momentum_breakout (GPS/ACE/BTW, avoid_chase)", "META legal-risk headline is fresh and primary-sourced (CNBC)", "AMZN/WMT OpenAI-ChatGPT-shopping partnership rumor was published then explicitly denied same day by another outlet"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.4,
      "reason_codes": ["data_unavailable", "squeeze_risk"],
      "data_missing": ["OI 24h% n/a for several MEXC-fallback symbols (ACE, GPS, BTW)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ACE/BICO: negative funding across external venues (bybit+mexc), crowding elevated", "PORTAL/ONG: price up + OI up, fresh positioning confirms trend, crowding normal"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["chase_risk", "overextended", "entry_fresh", "stale_before_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["GPS +48.6%/24h vol 4.31x and ACE +30.2%/24h vol 3.17x both explicitly tagged overextended/breakout, momentum_breakout basket playbook is avoid_chase/wait_pullback", "GE (A-tier stocks) triggered off a real capex-tailwind catalyst, cleaner technical setup", "INTC/BAC waiting_for_entry, not yet triggered, so chase risk is lower but pre-open pricing not yet confirmed by post-open tape"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"],
      "data_missing": ["authoritative PAPER_MONITOR_STATUS_LATEST.md stale by ~3h, not used as primary source"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active-signals (n=46): waiting_for_entry=4, triggered=16, tp1_hit=17, tp2_hit=9", "stocks active-signals (n=50): waiting_for_entry=30 (incl. duplicate rows), triggered=9, tp1_hit=9, tp2_hit=2", "6 open crypto swing positions (HOLO/AVNT/PROM×2/LUNA/MMT/BABY) run on frozen OHLCV — needs_review"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["META: fresh CNBC report — federal trial over child-safety claims reaching a critical moment in California, 'astronomical' potential penalties, published today 14:09 UTC", "macro/geopolitics risk 100/100 from Houthi/Red Sea, Russia-Ukraine, and ongoing Coldcard BTC exploit", "Coldcard exploit estimated 1,700-2,055 BTC stolen across multiple attacker wallets, still being tracked"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto A/B headline: sample=71, winrate 19.7%, PF 2.72, totalR +24.1 — edge driven almost entirely by swing mode (avgR +0.74, totalR +25.2); intraday and scalp modes both slightly negative avgR", "crypto shorts: 0/3 wins, totalR -3.0 — direction=short is currently a losing bucket, n small", "stocks A/B headline: sample=23, winrate 0%, PF 0.0, totalR -1.0 (mostly unresolved/waiting, only 2 triggered) — too small to read, but tier=B specifically shows PF 0.0 on 7 triggered", "stocks C-tier: sample=575, PF 0.14, totalR -9.5 — consistently negative, watchlist/research only by design"] },
    { "agent": "head_trader", "verdict": "advisory_synthesis_only", "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["see section 8 below"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "GE", "trigger": "already triggered 367.10-368.33, A-tier, capex/industrial-AI tailwind (Google/Amazon/Meta capex raises), no legal flag" },
    "best_short_candidate":    { "symbol": "AMZN", "trigger": "waiting_for_entry 261.15-261.94, B-tier short — but see manual-review note, tape is broadly risk-on which works against fresh shorts" },
    "best_catalyst_candidate": { "symbol": "GE", "trigger": "same as long candidate — cleanest catalyst-to-signal linkage this cycle" },
    "avoid_candidate":         { "symbol": "META", "reason": "fresh primary-sourced federal legal-risk headline (child-safety trial, 'astronomical' consequences) hit today — downgrade to manual review regardless of directional alignment with the short signal" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | bad | 0.80 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | mixed | 0.70 | mixed, risk_on, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, fresh_catalyst, catalyst_contradicted, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.40 | data_unavailable, squeeze_risk | advisory_only |
| technical_entry | caution | 0.65 | chase_risk, overextended, entry_fresh, stale_before_entry | advisory_only |
| execution_lifecycle | needs_review | 0.70 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.75 | legal_risk, headline_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.55 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | advisory_synthesis_only | 0.65 | — | advisory_only |

## 4. What Changed vs Previous Review (vs 15:59 EEST pre-US-open review)

- **New:** duplicate signal_id emission observed for INTC (×4), BAC (×2), GE (×3) with identical entry/expiry — not flagged in the 15:59 review (TODO-2, new).
- **New:** stocks intraday report is now stale-relative-to-market — 15:59 review had a genuine pre-open snapshot at the right time; this cycle's "freshest" stocks file (15:35 UTC / 8:35 ET) is still pre-open even though the US session has been running ~2h15m, because no post-open scan has completed yet.
- **Unchanged / carried forward:** OHLCV freeze on 11 crypto symbols (2026-08-15 22:30 UTC), now confirmed a 4th consecutive cycle, still no remediation (TODO-1, escalating).
- **Unchanged:** catalyst mapping still weak (68% unmapped now vs 64.2% at 15:59, 57% at 11:40, 51.8% at 04:40) — degradation trend continues (see 15:59 review TODO-6, still open).
- **Unchanged:** GPS/ACE momentum-breakout cluster still tagged avoid_chase/overextended, same as 15:59 and 11:40.
- **Unchanged:** `detect_untracked_legacy_alerts` clean both cycles.
- **Confirmed vs 15:59:** META and AMZN were already downgraded to CAUTION in the 15:59 pre-US stocks overlay for contradicted catalysts; this cycle's direct check confirms the META legal-risk story is real, fresh, and primary-sourced (CNBC) — consistent with, not contradicting, the earlier caution flag.
- No prior review's specific candidate picks (COP long-watch, GRVT short-watch) remain active in this cycle's top candidate set — COP does not appear in the current active-signals pull; GRVT is crypto and not present in the current active B/A crypto set either. Treat as expired ideas, not invalidated theses.

## 5. Catalyst Coverage

- Total catalyst_events today: **1,672**. Mapped (non-null symbol): **534** (32%). Unmapped: **1,138** (68%).
- Narrative baskets: **3** — `delisting_thin_liquidity` (ATOM, avoid_low_liquidity), `rwa_narrative` (ONDO/XLM, related_beta_rotation), `momentum_breakout` (GPS/ACE/BTW, avoid_chase).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (68% unmapped, continuing the intraday degradation trend: 51.8%→57%→64.2%→68% across today's cycles.)
- Top 3 unmapped headlines this cycle: "SK Hynix's Stock Trades at Around 5 Times Next Year's Earnings Even After Revenue Grew 257%..."; "Navy SEALs criticize Trump over Pacific military base readiness issues"; "US businesses' AI spending surges to $7,400 per employee monthly as corporate divide widens."

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **chop** (BTC range, ETH transition_up, altcoin breadth ~52% — directionless, with a heavy risk-off macro overlay from geopolitics/exploit headlines sitting on top, not yet expressed in price)
- Stocks mood: **risk-on** (VIX 14.98, breadth 100% above EMA20/50, all 4 indices uptrend) — **but read from a pre-open snapshot**, not confirmed by live post-open tape this cycle
- Dominant narrative: stocks — AI capex tailwind (Google/Amazon/Meta raised capex guidance, benefits GE/industrials and semis); crypto — momentum-breakout cluster (GPS/ACE) plus a live BTC exploit overhang (Coldcard, ~1,700-2,055 BTC)
- Preferred side now: **mixed** — longs favored on the stocks side (risk-on tape, capex tailwind), wait-for-trigger on crypto (chop + unresolved data-integrity risk on 6 open swing names)
- Best long candidate: **GE** (A-tier stocks, triggered, catalyst-backed)
- Best short candidate: **AMZN** (B-tier stocks, waiting_for_entry) — counter-trend against a risk-on tape, treat as lower-conviction until confirmed by price action, not a clean short
- Best catalyst-backed candidate: **GE** (industrial-AI capex tailwind, direct news-to-signal linkage)
- What to avoid: chasing **GPS/USDT**/**ACE/USDT** (overextended, avoid_chase basket); treating **META** short as clean (legal-risk headline requires manual review); relying on displayed price for **HOLO/AVNT/PROM/LUNA/MMT/BABY** (frozen OHLCV, unverified)
- What would change the view: a post-open stocks scan confirming GE/INTC/BAC hold their pre-open levels; OHLCV feed remediation for the 6 frozen crypto symbols; BTC reclaiming range highs on volume to resolve the chop

## 7. Candidate Deep Dives

**1. GE — stocks, A-tier, long, intraday, triggered (367.10-368.33, invalidation 365.86)**
- Catalyst: capex-tailwind read-through from "Google, Amazon, and Meta All Just Raised Capex Guidance Again" (Motley Fool, today) plus a direct GE Aerospace/Kratos US Air Force contract win (Finnhub, today). Two independent, corroborating internal sources — reused internal data, no external research needed.
- Price reaction: signal already triggered — has price reacted to the catalyst? Yes, partially (score 91.0-99.7 across the 3 rows, all above the entry zone historically). Chasing risk: low-moderate, already triggered rather than a fresh breakout print.
- Legal/headline risk: none found in 24h scan.
- Aligned with market mood: yes — risk-on stocks tape, capex/industrial-AI narrative is a live theme.
- Actionable now: yes, per the desk's own trigger logic; treat the pre-open-vs-post-open timing gap as the main caveat (no post-open confirmation scan yet this cycle).
- Invalidates at: 365.86.
- Note: 3 GE rows share the same entry/expiry (99.7/91.0/91.0) — likely duplicate signal emission (TODO-2), treat as one setup, not three.

**2. META — stocks, B-tier, short, intraday, waiting_for_entry (578.58-580.58, invalidation 582.58)**
- Catalyst/risk: CNBC, today 14:09 UTC, primary source — "Meta faces 'astronomical' consequences as legal fight reaches critical moment in California," a federal trial over child-safety claims with potential major financial penalties and platform changes.
- Per source-discipline protocol (§I): this is a verified legal/headline risk event on a stocks A/B candidate. **Final verdict downgraded to MANUAL REVIEW REQUIRED — not a clean actionable short**, even though the headline is directionally bearish-aligned with the existing short thesis.
- Price reaction: not yet observable (pre-open snapshot); chase risk unknown until post-open confirmation.
- Would invalidate: price back above 582.58, or the legal story resolving/being walked back.

**3. AMZN — stocks, B-tier, short, intraday, mixed triggered/waiting rows (261.15-261.94, invalidation 262.74)**
- Catalyst check: a "Synchrony partners with OpenAI for ChatGPT shopping (AMZN, WMT)" story published today was **explicitly denied same-day** by a separate CryptoBriefing item ("No confirmed partnership between Synchrony and OpenAI for ChatGPT shopping") — contradiction noted, low materiality to the technical short thesis either way.
- Contradiction: Bill Ackman's Pershing Square disclosed AMZN as its 4th-largest holding this quarter (Motley Fool) — a fundamental long signal from a well-known allocator, working against a fresh technical short. This is 13F positioning data (lagging, quarter-old), so it is a caution flag, not an invalidation.
- Market-mood alignment: **counter-trend** — stocks tape is broadly risk-on; a fresh short here is fighting the tape.
- Actionable now: only after confirmation — treat as **shorts only after failed retest**, not a chase.
- Invalidates at: 262.74.

**4. INTC — stocks, A-tier, long, intraday, waiting_for_entry (103.14-103.96, invalidation 102.32)**
- Contradiction: Motley Fool/Finnhub report today that Stanley Druckenmiller's Duquesne Family Office **dumped Intel** (along with Micron and Broadcom) in its latest 13F, rotating into AI-datacenter names (IREN). This is quarter-old positioning data disclosed today, not a same-day price-reactive event — lagging indicator, moderate-not-high materiality.
- No legal/headline risk found in 24h scan.
- Market-mood alignment: aligned with risk-on stocks tape and strong technology-sector RS (+4.08% vs SPY, 20d).
- Actionable now: waiting_for_entry, not yet triggered — require the entry zone (103.14-103.96) to print before acting; treat the Druckenmiller 13F story as background caution, not a blocker.
- Note: 4 INTC rows (all tier A, identical entry/expiry) — likely duplicate signal emission (TODO-2), treat as one setup.

**5. WLFI/USDT — crypto, B-tier, swing, long, triggered (0.05633-0.05679 / 0.05976-0.06020, two rows, invalidation ~0.0556-0.0592)**
- Bias-tag contradiction: the current intraday report's "Weakest Symbols" list tags WLFI/USDT **bias short, 24h -3.35%, RS vs BTC -4.42%** on the same date an active swing LONG position is open and triggered. This is the same class of open-long-tagged-bias-short contradiction flagged as a recurring pattern in prior sessions (not new to this run, but re-confirmed live here).
- Feed integrity: WLFI itself is on a **fresh** OHLCV feed (control symbol, last row 13:45 UTC today) — the contradiction is a scoring/labeling inconsistency, not a stale-data artifact.
- Actionable now: **needs review**, not a clean long — the directional bias tag and the open position disagree; do not add to this position until the contradiction is resolved.
- Would invalidate: per position, ~0.0556 (first row) / ~0.0592 (second row).

## 8. Best Candidates Ranked

1. **GE (long)** — cleanest actionable, catalyst-backed, already triggered, no legal flag. Trigger: already active at 367.10-368.33.
2. **META (short-watch, manual review)** — directionally interesting but held for legal-risk verification per protocol. Trigger to re-open as clean: legal story clarifies/resolves, or price confirms post-open weakness below entry zone.
3. **AMZN (short-watch)** — counter-trend short, wait for confirmation. Trigger: clean failed retest of 261.15-261.94 with post-open price action, not a fresh chase.
4. **INTC (long-watch)** — highest score on the desk (97.6) but not yet triggered. Trigger: clean print into 103.14-103.96 with post-open volume confirmation.
5. **WLFI (needs-review, not a fresh add)** — existing long position flagged for bias-tag contradiction. Trigger to clear: bias tag reconciles with an up-close on fresh data, or position management on the existing open trade.

**Crypto watch-only (not deep-dived, capped by chase risk):** GPS/USDT and ACE/USDT — both explicitly tagged overextended/avoid_chase in the momentum_breakout basket; would become actionable only on a clean pullback into the tagged zones, not at current extended prices.

**Excess candidate not deep-dived (slot cap):** BAC (A-tier, long, waiting_for_entry, 64.84-65.01) — clean, no legal flag, no contradiction found, but held out of the 5-slot cap in favor of higher-signal items (contradiction/legal-risk cases and the top-score/catalyst-backed picks). Same actionability logic as INTC: wait for post-open confirmation into the entry zone.

## 9. Avoid / No Trade (this decision window only)

- **META** as a clean short — legal-risk headline requires manual review before acting, per protocol, regardless of directional alignment.
- **GPS/USDT, ACE/USDT** as fresh crypto longs — both overextended, explicitly tagged avoid_chase.
- **HOLO, AVNT, PROM, LUNA, MMT, BABY** — do not add to or manage these open crypto swing positions off the displayed price/TP/SL state; the feed has been frozen for ~41h and is unverified. Existing positions continue running per system logic; this is a data-quality caution, not a stop-the-system instruction.
- This is a decision-window-only read — scanning, candidate generation, and tracking continue uninterrupted regardless of this section.

## 10. Main Risks

- **Frozen OHLCV on 6 open crypto swing positions**, 4th consecutive cycle unresolved (~41h stale) — displayed price/TP/SL for these positions cannot be trusted until the feed is fixed.
- **Stocks intraday report is pre-open while the US session has been running ~2h15m** — every stocks verdict in this review is pre-open-context, not post-open-confirmed; a fresher scan later in the cycle could change all five stocks candidates materially.
- **Catalyst mapping weak and worsening intraday (68% unmapped, up from 51.8% at 04:40)** — catalyst-backed conclusions should be treated as directional context, not proof.
- **Macro/geopolitics risk scored 100/100** (Red Sea, Russia-Ukraine, ongoing BTC exploit) sitting on top of a still-orderly crypto range and a still-bullish stocks tape — a headline-risk overhang that hasn't yet forced price, but could.
- **Duplicate signal emission** (INTC ×4, BAC ×2, GE ×3) inflates the apparent number of independent setups on the desk this cycle — read active-signal counts with that in mind.
- **Crypto short bucket is currently a losing playbook** (0/3 wins, totalR -3.0, n small) — any new crypto short idea should be treated with extra skepticism until sample size improves.

## 11. Action Plan — next 4 hours

- Re-pull `active-signals --asset-class stocks` and a fresh stocks-intraday report once a genuine post-open scan lands, to confirm or invalidate GE/META/AMZN/INTC/BAC before treating any of them as more than pre-open watchlist.
- Do not act on META short until the legal-risk headline is either corroborated by a second source or shows up as resolved/dismissed.
- Watch for OHLCV feed remediation on the 6 frozen crypto symbols; re-check next cycle regardless (5th consecutive check).
- Watch GPS/ACE for a pullback into their tagged wait_pullback zones rather than chasing current extension.
- No new crypto swing adds recommended this window given the frozen-feed exposure already on the book.

## 12. Final Verdict per Mode

- **Crypto scalp:** no clean actionable this window; desk-documented low-confidence mode (PF 0.14 on 14d re-audit per report header) — continue data collection only.
- **Crypto intraday:** chop, wait-for-trigger; GPS/ACE avoid-chase; no fresh clean intraday long/short this window.
- **Crypto swing:** existing book carries data-integrity risk on 6 positions (needs review); WLFI flagged for bias-tag contradiction; no new adds recommended.
- **Stocks intraday:** pre-open-context only this cycle; GE cleanest long-watch, INTC/BAC longer-watch pending confirmation, META held for manual review, AMZN short-watch pending confirmation.
- **Stocks swing/invest:** deprecated framework, no signal (per known project state).

## 13. Sources

- [Meta faces 'astronomical' consequences as legal fight reaches critical moment in California](https://www.cnbc.com/2026/08/17/meta-attorneys-general-california-federal-trial-astronomical-consequences.html) — CNBC Markets, 2026-08-17 14:09 UTC, primary_source, confirms META legal-risk flag.
- [Billionaire Stanley Druckenmiller Dumped Micron and Intel](https://www.fool.com/investing/2026/08/17/billionaire-stanley-druckenmiller-mu-intc-buy-amzn/?source=iedfolrf0000001) — The Motley Fool Investing, 2026-08-17, single_source, weakens (caution on) INTC long thesis.
- [Stanley Druckenmiller Just Made a Big Bet on IREN While Dumping Broadcom, Intel and Micron](https://finnhub.io/api/news?id=476c91d56b69809ec33fde86aa1a6143a6d1f4ed46b543e7175bd4346036b058) — Finnhub company-news, 2026-08-17, single_source, corroborates the above (same underlying 13F event, second outlet).
- [Synchrony, credit card issuer to Amazon and Walmart, partners with OpenAI for ChatGPT shopping](https://www.cnbc.com/2026/08/17/synchrony-openai-chatgpt-shopping.html) — CNBC Markets, 2026-08-17 15:26 UTC, single_source at time of publication.
- [No confirmed partnership between Synchrony and OpenAI for ChatGPT shopping](https://cryptobriefing.com/synchrony-openai-chatgpt-shopping-partnership/) — CryptoBriefing, 2026-08-17 15:16 UTC, single_source, contradicts/corrects the item above (published earlier same day, denial noted).
- [Bill Ackman's Pershing Square Made Amazon Its Fourth-Largest Holding by Dumping Alphabet](https://www.fool.com/investing/2026/08/17/bill-ackmans-pershing-square-amazon-alphabet/?source=iedfolrf0000001) — The Motley Fool Investing, 2026-08-17, single_source, caution flag on AMZN short (fundamental positioning, lagging).
- [GE Aerospace, Kratos Land US Air Force Contract](https://finnhub.io/api/news?id=aa13fa2b54b5d9459f3d0577f68ef10283cdaece03e8e0cf5b8d3103818796e7) — Finnhub company-news, 2026-08-17 09:33 UTC, single_source, supports GE catalyst.
- [Google, Amazon, and Meta All Just Raised Capex Guidance Again](https://www.fool.com/investing/2026/08/17/google-amazon-and-meta-all-just-raised-capex-guida/?source=iedfolrf0000001) — The Motley Fool Investing, 2026-08-17 06:30 ET, single_source, supports GE/industrial-AI narrative.
- Internal: `data/catalysts/2026-08-17/catalyst_cycle_14-11.md` — momentum_breakout basket (GPS/ACE/BTW, avoid_chase), used for crypto chase-risk flags.
- Internal: direct OHLCV CSV timestamps, `data/raw/ohlcv/binance/15m/{HOLO,AVNT,PROM,LUNA,MMT,BABY,WLFI,CHIP}_USDT_15m.csv`, read 2026-08-17 ~18:40 EEST, used for the frozen-feed finding.

## 14. Fix Requests / TODO

### TODO-1 (carried forward, escalating — 4th consecutive cycle)
- **issue:** 11 crypto symbols frozen on 15m OHLCV at 2026-08-15 22:30:00 UTC; 6 of them (HOLO, AVNT, PROM, LUNA, MMT, BABY) are live open crypto swing positions whose displayed price/TP/SL state is unverified.
- **evidence:** `data/raw/ohlcv/binance/15m/{HOLO,AVNT,PROM,LUNA,MMT,BABY}_USDT_15m.csv` all last-row `2026-08-15 22:30:00+00:00`, checked 2026-08-17 ~18:40 EEST (~41h stale). Control symbols WLFI (13:45 UTC today) and CHIP (15:30 UTC today) are fresh — pair-specific, not a global outage. Also flagged in `OPUS_ENRICHED_REVIEW_AUTO_2026-08-17_0440.md`, `_1140.md`, and `_1559.md`.
- **suggested manual fix:** investigate the OHLCV ingest/refresh path for this specific symbol set — likely a per-pair fetch failure that isn't retried or alerted on; verify whether the paper-monitor TP/SL logic for these 6 open positions is using this frozen data or a separate live-price source.
- **priority:** high
- **first observed:** 2026-08-17 02:00 EEST (carried through 04:40, 11:40, 15:59, now 18:45)

### TODO-2 (new this cycle)
- **issue:** Duplicate signal_id emission for the same underlying setup — INTC shows 4 separate `signal_id` rows, BAC 2, and GE 3, all sharing identical tier/mode/entry_low/entry_high/invalidation/expires_at within the current active-signals pull.
- **evidence:** `python -m src.cli active-signals --asset-class stocks` output, 2026-08-17 ~18:40 EEST — e.g. INTC rows `sig_0f8f09cd3bc068b3`, `sig_82a6b4b220a52335`, `sig_d194c83a5a73021a`, `sig_aa4f96cd878d0984` all show entry 103.1397-103.9601, invalidation 102.3194, expires 2026-08-18T15:19:57 (three identical, one at a slightly later expires_at for the C-tier duplicate).
- **suggested manual fix:** investigate the stocks signal-generation path for a dedup gate on symbol+tier+mode+entry-zone within a short time window; confirm whether this inflates `signal-stats` sample counts (n=23 A/B headline this cycle may be double/triple-counting real setups).
- **priority:** medium
- **first observed:** 2026-08-17 18:40 EEST
