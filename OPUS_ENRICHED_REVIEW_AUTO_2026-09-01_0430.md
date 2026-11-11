# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:30 EEST

## 1. Executive Summary

Slot: **crypto overnight / Asia review** (04:30 EEST target, written 04:41 EEST). **Advisory only — no auto-trade.** Scheduler is fresh and actively progressing (log updated 04:31, current step "stocks intraday report") — **not deferred**. Crypto price action is genuinely bullish (BTC/ETH uptrend, altcoin breadth 56.25%/66.67% above EMA20/50) but this sits against a maxed-out 100/100 macro risk score driven by real, externally-verified Iran/Strait-of-Hormuz escalation headlines — a **price-bullish / macro-risk-off divergence** that argues for selective, pullback-only longs rather than chasing. No A-tier crypto setups; all B-tier ideas are no-catalyst momentum plays that the desk's own playbook flags as a historically net-negative bucket (WR 23%/PF 0.70/−3R) absent RS-leader or breakout confirmation. Stocks are closed (planning/watchlist only per market-closed gate) — all raw A-tier stock candidates (COP, CRWD, NOW, XOM, QCOM, NVDA, etc.) are demoted to C. Two operational issues carry weight tonight: (1) a **fresh, smaller recurrence of the scheduler timeout storm** flagged in the last two reviews — 9 `CMD TIMEOUT` events today, including 4 consecutive on paper-execution steps (03:57–04:12), before the pipeline recovered cleanly by 04:15; and (2) **direct DB confirmation that the known bias-tag contradiction bug is still live** — both ONG/USDT and PROM/USDT carry open paper LONG swing positions while tonight's intraday report tags them `bias=short` with double-digit negative 24h moves. Catalyst mapping is weak (66.4% unmapped) — treat catalyst context as directional only.

## 2. Data Used

- `data/scheduled_runs/2026-09-01_default_schedule/scheduler.log` — actively progressing, last step start 04:31:27 ("stocks intraday report"). Full-day timeout audit: **9 `CMD TIMEOUT` events**: isolated ones at 00:43 (`paper execution accounting refresh`), 01:02 (`paper portfolio ledger refresh`), 01:11 (`intelligence layer update`), 01:32 (`monitor heartbeat watchdog`), 01:34 (`refresh obsidian dashboard`), then a **4-in-a-row cluster 03:57–04:12** on `paper execution accounting refresh` → `paper structural TP refresh` → `paper structural stop plan` → `paper entry-mode classify` (all non-fatal, cycle continued each time). Clean, unbroken successful-step run from 04:15:18 through write time (04:31).
- Reports: `data/reports/intraday/2026-09-01_00-45_intraday_report.md` (generated 03:45 EEST, ~1h old, **fresh**), `data/reports/swing/2026-08-31_04-40_swing_report.md` (generated 07:40 EEST yesterday, data as-of 04:40 EEST yesterday — **~24h old, stale** per the >14h rule; no fresher swing report exists so used as context only, excluded from fresh-verdict weighting), `data/reports/stocks/intraday/2026-09-01_01-37_stocks_intraday_report.md` (generated 04:37 EEST, **fresh**, but market-closed gate demotes all A/B to C). Stocks swing/invest reports are from 2026-07-02 (~2 months stale) — confirmed deprecated pipelines per prior project state, not evaluated.
- Catalyst: `data/catalysts/2026-09-01/catalyst_cycle_00-52.md` + `catalyst_events.jsonl` (500 events scanned, generated 03:52 EEST, fresh), `narrative_baskets.jsonl` (4 baskets).
- `data/processed/llm_analysis_packet.md` (crypto, 03:47 EEST) and `data/processed/llm_stocks_packet.md` (stocks, 01:20 EEST).
- CLI (this run): `active-signals --asset-class crypto` (50 rows, all B-tier, mix of intraday/swing/scalp, no A-tier), `active-signals --asset-class stocks` (50 rows, all C-tier post market-closed demotion), `signal-stats --asset-class crypto` (tier B n=209, triggered=195, wins=21/losses=54, winrate 10.8%, PF 1.2528, avgR +0.0595, totalR +9.1 — consistent with the 23:37 snapshot (n=213, PF 1.23, totalR +8.6), slight uptick; by-mode split shows one badly losing bucket n=58/PF 0.16/totalR −5.0/0W-6L, consistent with the known disabled-scalp losing bucket; exchange_confirmation split again shows cross-exchange n=73 PF 0.42/totalR −11.x losing vs Binance-only n=133 PF 2.4x/totalR +21.7 winning — persistent, unresolved finding, several reviews running), `signal-stats --asset-class stocks` (A/B headline n=39, PF=inf, winrate 28.6%, totalR +4.0 — unchanged from 23:37), `detect_untracked_legacy_alerts --since 2026-09-01` (**0 rows — clean**).
- SQL (read-only, direct sqlite queries against `proposed_signals`): confirmed ONG/USDT open swing LONG (triggered, score 73.9, created 2026-08-26) and scalp LONG (tp1_hit, created 2026-08-25); confirmed PROM/USDT open swing LONG (triggered, score 73.9, created 2026-08-30) and an earlier swing LONG (triggered, score 69.2, created 2026-08-27); confirmed TUT/USDT open swing LONG (triggered) and scalp LONGs (tp1_hit); confirmed MANTRA/USDT open swing LONG (triggered, score 66.3, news_supported=0, created 2026-08-28) — no conflicting bias found for MANTRA this run. ZKC/USDT and ZKP/USDT show **no** active proposed_signals — no formal short setup exists for either despite appearing in "Weakest Symbols."
- External: 2 WebSearch queries (Lazarus/Hyperliquid wallet flows; CME Emerging Crypto Index composition) — both verified, see §13. No WebFetch needed — search results were sufficiently corroborating across independent outlets.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-31_2337.md` (post-close final daily review, 23:37 EEST) — this review supersedes it as `LATEST`.

## 3. Scheduler / Data Freshness

- `scheduler.log` actively progressing through write time → **not deferred** per §D (both freshness checks pass easily — log is 10 minutes old).
- **Timeout recurrence (smaller than last night's storm, same class of issue)**: 9 distinct `CMD TIMEOUT` events today (00:43–04:12 EEST), most notably a **4-in-a-row cluster** on the paper-execution/structural-TP/structural-stop/entry-mode-classify steps (03:57:49→04:12:51). All non-fatal (`cycle continues`); the pipeline then ran 15+ consecutive successful steps from 04:15:18 onward through write time (paper-shadow A/B execution, paper portfolio ledger refresh, intelligence layer update, stocks post-trade classifier, stocks intraday report — all exit=0). This is a **materially smaller echo** of the 24-event storm flagged at 23:37 last night (19:06–23:04:58), not a new failure mode — same step family affected (paper-execution/paper-structural steps), same self-recovery pattern. `monitor heartbeat watchdog` also timed out once (01:32) — worth watching given prior project history of stale-deploy risk tied to watchdog health.
- Report freshness: crypto **intraday** ~1h old (fresh), crypto **swing** ~24h old (**stale**, no fresher source — used as background-position context only, not for new-entry weighting), stocks **intraday** ~4min old (fresh, but market-closed gate applies — see §6).
- Catalyst layer: `catalyst_cycle_00-52.md` (03:52 EEST, ~49min old, fresh) but **66.4% of today's 500 catalyst events are unmapped (332/500)** — **catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- `detect_untracked_legacy_alerts --since 2026-09-01`: **0 rows** — clean.
- Paper/monitor status: paper-shadow A/B execution and paper portfolio ledger refresh both completed successfully this cycle (04:20, 04:24) despite the earlier same-family timeouts — the paper book is not stuck, just delayed within-cycle.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-09-01 04:41 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["fresh crypto swing report (24h old, no regen since yesterday 04:40)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log fresh (10min old), actively progressing", "9 CMD TIMEOUT events today incl. 4-in-a-row cluster 03:57-04:12 on paper-execution family, all non-fatal", "clean recovery: 15+ consecutive successful steps since 04:15", "crypto swing report ~24h stale, no fresher source", "catalyst mapping 66.4% unmapped"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mixed", "longs_preferred", "wait_for_trigger"],
      "data_missing": ["live Asia-session price action beyond the 03:45 report snapshot"],
      "suggested_effect": "advisory_only",
      "facts_used": ["intraday report labels regime bullish trend / risk-on: BTC uptrend, ETH uptrend, altcoin breadth 56.25%/66.67% above EMA20/50", "macro/geopolitics risk score 100/100 from 7 risk-off hits (Iran/Strait of Hormuz escalation headlines, Kyiv missile barrage) vs 1 risk-on hit -- externally confirmed as a real, ongoing conflict per the 23:37 review's verified sourcing", "this is a genuine price-bullish / macro-risk-off divergence, not a clean risk-on read"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "catalyst_confirmed", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["66.4% unmapped catalyst events (332/500) this cycle", "CME Emerging Crypto Index launch (BNB/XRP/SOL/HYPE = 92.7% combined weight) verified externally via WebSearch, matches internal primary_source t.me/CoinMarketCapAnnouncements item", "Lazarus-linked wallets moving $30M+ through Hyperliquid verified externally via WebSearch (CoinDesk, crypto.news, multiple independent outlets), matches internal single_source item -- now corroborated to a higher confidence tier than internal alone", "momentum_breakout basket (0G/UNI/AUCTION/DOGS) explicitly labeled 'without confirmed news catalyst -- pure momentum cluster' by the desk's own narrative engine"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.45,
      "reason_codes": ["squeeze_risk", "oi_supports", "funding_extreme"],
      "data_missing": ["OI 24h% is n/a (fallback_via_mexc) for most top movers -- funding-only read"],
      "suggested_effect": "advisory_only",
      "facts_used": ["0G/USDT: negative funding across bybit/okx/mexc, cross-venue crowding flagged 'elevated' -- crowded shorts, squeeze-supportive for the existing long but also signals the move may already be extended", "BICO/USDT and LA/USDT: same negative-funding/elevated-crowding pattern", "HEMI/USDT and DASH/USDT: neutral funding, low/normal crowding -- cleaner reads", "UNI/USDT: price up + OI down = short covering, weaker continuation quality per the report's own derivatives read"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["entry_late", "chase_risk", "clean_retest"],
      "data_missing": ["live intraday chart / TradingView -- MCP not loaded, using only local OHLCV/ATR/EMA fields from the report"],
      "suggested_effect": "advisory_only",
      "facts_used": ["0G/USDT current price 0.2175 sits ABOVE the report's own pullback entry zone (0.2057-0.2139) -- buying now would be chasing a +29.85% 24h move; the setup is only clean on a retracement into the stated zone with volume confirmation", "DASH/USDT and UNI/USDT similarly require pullback into stated entry bands, not market-buy at current price", "ZKC/USDT and ZKP/USDT have no formal desk-generated entry levels at all (no proposed_signal minted) -- any short here would need a manual technical trigger, not a desk level"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.55,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active-signals: 50 rows returned, all B-tier -- WAITING FOR ENTRY (0G, DOGS x2 duplicated across cycles), TRIGGERED / ENTERED UNRESOLVED (majority, incl. DASH, PROM, ONG, MANTRA, TUT), TP-HIT (ZKC scalp, HEMI, GIB, CORE, VIC, IND) -- no A-tier open", "stocks active-signals: 50 rows, all C-tier WAITING FOR ENTRY post market-closed demotion, none actionable", "ONG/USDT and PROM/USDT: OPEN LONG (triggered) positions directly contradicted by tonight's bias=short tag on the same symbols -- NEEDS REVIEW before treating either position's health as normal"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["headline_risk", "correlation_cluster", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ONG/USDT and PROM/USDT open longs vs. bias=short tag + double-digit negative 24h (-17.31% and -12.69% respectively) -- known systemic bug (project memory: bias-tag contradiction, previously confirmed on ZBT/ACE 08-08 and ONG/PROM/PUMP/BICO 08-31, still unfixed, HIGH priority) -- recurring again tonight, same symbols", "HYPE/USDT: active exploit_hack operator-review flag (Lazarus-linked $30M+ wallet flow through Hyperliquid), externally corroborated -- correlated regulatory/reputational tail risk for any HYPE-adjacent exposure (perps_dex_narrative basket)", "MANTRA/USDT open long carries forward with no fresh news either way -- standing watch item, not escalating tonight", "macro Iran/Hormuz risk is a cross-asset correlation cluster into the Asia session"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["playbook_failing", "low_sample", "old_tail_expired"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto_intraday_catalyst_or_momentum playbook explicitly self-flags: 14d no-news cut WR 23% / PF 0.70 / -3R -- every B-tier intraday idea tonight (0G, DASH, UNI, BICO, DOGS, HEMI) runs this exact no-catalyst variant", "signal-stats crypto: cross-exchange-confirmation cohort PF 0.42 (n=73, totalR -11.x) vs Binance-only PF 2.4x (n=133, totalR +21.7) -- persistent multi-review gap, unresolved", "weekend_mode cohort (n=35) winrate 12%, flagged low by the tool's own observation" ] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.5,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": [] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.5,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "0G/USDT", "trigger": "wait for pullback into 0.2057-0.2139 with volume confirmation on the retest -- do NOT chase at the current 0.2175 (already above the stated entry zone, +29.85% 24h)", "reason": "highest-scoring B-tier idea (72.6), RS vs BTC +28.77%, negative funding + elevated cross-venue short crowding supports a continuation/squeeze read, but the move is already extended -- entry discipline matters more than the thesis here" },
    "best_short_candidate":    { "symbol": "ZKC/USDT", "trigger": "no formal desk level exists -- manual trigger only: break of the recent session low with volume, invalidate above the prior swing high", "reason": "weakest RS vs BTC (-14.81%) with no conflicting open long (unlike ONG/PROM which ARE conflicted); regime is bullish-biased so the scanner never generated a formal short setup -- this is a genuinely low-confidence, manual-only idea, not a desk signal" },
    "best_catalyst_candidate": { "symbol": "BNB/USDT", "trigger": "watch for beta-rotation follow-through into BNB/ASTER (binance_ecosystem_teaser basket) after CME Emerging Crypto Index inclusion -- no formal signal minted yet, needs a technical confirmation before treating as actionable", "reason": "cleanest verified catalyst tonight: CME's new Emerging Crypto Index gives BNB/XRP/SOL/HYPE a combined 92.7% weight, confirmed via 2 independent external sources plus a matching internal primary_source item -- unlike HYPE, BNB carries no legal/security overhang" },
    "avoid_candidate":         { "symbol": "HYPE/USDT", "reason": "externally verified (CoinDesk, crypto.news, multiple independent outlets): Lazarus Group-linked wallets moved $30M+ through Hyperliquid amid active US regulated-entry talks -- genuine regulatory/reputational tail risk on the platform itself; the CME index inclusion tailwind does not offset this for new entries" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.55 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | caution | 0.50 | mixed, longs_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, fresh_catalyst, catalyst_confirmed, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.45 | squeeze_risk, oi_supports, funding_extreme | advisory_only |
| technical_entry | caution | 0.50 | entry_late, chase_risk, clean_retest | advisory_only |
| execution_lifecycle | needs_review | 0.55 | open_actionable, waiting_for_entry, review_shadow, needs_review | advisory_only |
| risk_manager | caution | 0.55 | headline_risk, correlation_cluster, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.55 | playbook_failing, low_sample, old_tail_expired | advisory_only |
| head_trader | caution | 0.50 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (vs `..._2337.md`)

- **New (smaller echo)**: 9 fresh `CMD TIMEOUT` events today (00:43–04:12), including a 4-in-a-row cluster on the same paper-execution/structural-TP/structural-stop family that stalled last night — same failure class, self-recovered again by 04:15. Not yet at last night's severity (24 events) but the second consecutive cycle showing this pattern.
- **Confirmed via direct DB query (new evidence, same underlying known bug)**: ONG/USDT and PROM/USDT open paper LONGS directly contradicted by tonight's bias=short tags — this is the bias-tag contradiction bug from `[[project_crypto_ai_desk_bias_tag_contradiction]]` recurring on the same symbols flagged in that memory's 08-31 entry.
- **New / externally verified**: CME's Emerging Crypto Index launched 2026-08-31 with BNB/XRP/SOL/HYPE carrying 92.7% combined weight — corroborates the internal primary_source item, gives BNB the cleanest catalyst-backed watch tonight.
- **New / externally corroborated**: the Lazarus/Hyperliquid $30M+ wallet-flow story (previously internal single_source only) is now confirmed across multiple independent outlets (CoinDesk, crypto.news, etc.) — raises confidence on the HYPE avoid call.
- **Unchanged**: MANTRA/USDT headline-overhang watch (no new news, carries forward); catalyst mapping still weak (66.4% unmapped tonight vs 62.9% last night — essentially flat); crypto scalp bucket still the confirmed losing tail (PF 0.16-0.17 range); cross-exchange-confirmation cohort still materially underperforming Binance-only.
- **Not re-checked this run** (stocks market closed overnight, lower priority for this slot): the duplicate-signal-id bug on 7+ stocks-short symbols (ABNB, BA, UBER, SBUX, GOOGL, AFRM, CRCL) flagged at 23:37 — assume still open, carried forward to §14 without new evidence.
- **Regime shift**: last night's packet read "transition (mixed)"; tonight's fresh intraday report reads "bullish trend (risk-on)" for crypto — a genuine improvement in breadth (56.25%/66.67% above EMA20/50 tonight vs weaker readings in the stale swing snapshot), even as the macro geopolitical score stays maxed at 100/100.

## 5. Catalyst Coverage

- Total `catalyst_events` today (cycle_00-52, 03:52 EEST): 500. Mapped: 168 (33.6%). Unmapped: 332 (**66.4%**).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines: "VENEZUELA OIL DEAL RAISES TROUBLE NOT CAPITAL - RTRS", "YIELD ON JAPAN'S 5-YEAR JGB RISES 3.0 BPS TO 2.235%", "ASIA-PACIFIC COMPANIES OUTSIDE CHINA ARE SET TO BENEFIT FROM AI... MOODY'S RATINGS SAYS" — mostly macro/rates wire content, low symbol-mapping value; one exception — "UKMTO REPORTS TANKER STRUCK BY THREE PROJECTILES DURING OUTBOUND TRANSIT OF STRAIT OF HORMUZ" is directly relevant to tonight's macro-risk thesis and should ideally map to a macro/risk-off theme tag, another instance of the mapping gap costing real signal (same class of issue flagged for the Iran/oil headlines in the prior review).
- Narrative baskets (4 tonight): `perps_dex_narrative` (HYPE primary, wait_pullback, <6h), `rwa_narrative` (ONDO/XLM primary, related_beta_rotation, <6h), `binance_ecosystem_teaser` (BNB primary, related_beta_rotation, <6h — CME index catalyst), `momentum_breakout` (0G/UNI/AUCTION primary, DOGS related, wait_pullback, <1h — explicitly "without confirmed news catalyst").

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **mixed — price-bullish / macro-risk-off divergence.** BTC and ETH both in uptrend, altcoin breadth 56.25%/66.67% above EMA20/50 (genuinely improved vs the stale swing snapshot), but macro/geopolitics risk score is maxed at 100/100 on real, externally-verified Iran/Strait-of-Hormuz escalation and Kyiv missile-barrage headlines. Stocks are closed overnight (Tuesday, pre-market) — treat as planning/watchlist context only.
- Stocks mood: **closed — planning only.** VIX 14.92 (calm) as of the last snapshot before close; all raw A-tier candidates (COP, CRWD, NOW, XOM, QCOM, XLE, CRCL, INTU, NVDA, XLK, CRM, MAR, ABNB, MU, DXCM) demoted to C by the market-closed gate. Two of these (INTU: class-action/securities-fraud; NVDA: indictment) carry active legal/headline flags that would block promotion to A/B even after the open, pending manual review.
- Dominant narrative: **US-Iran military escalation / Strait of Hormuz risk** as the cross-asset macro overhang, alongside a genuine crypto altcoin-breadth improvement and the CME Emerging Crypto Index launch (BNB/XRP/SOL/HYPE) as the freshest structural crypto catalyst.
- Preferred side now: **longs, selective, pullback-only** — no clean short setup exists in the desk's own scoring (bullish-regime bias means the scanner didn't generate short ideas even for the weakest symbols); catalyst-backed BNB is watch-only pending technical confirmation.
- Best long candidate: **0G/USDT** (crypto) — pullback entry only, do not chase.
- Best short candidate: **ZKC/USDT** (crypto) — manual/low-confidence, no formal desk level.
- Best catalyst-backed candidate: **BNB/USDT** (crypto) — CME index inclusion, watch-only.
- What to avoid: **HYPE/USDT** new entries (Lazarus/Hyperliquid regulatory overhang, externally verified); **fresh crypto swing entries off the 24h-stale swing report**; treating ONG/USDT or PROM/USDT bias tags at face value without first resolving the contradiction against their open long positions.
- What would change the view: a fresh crypto swing report clearing the 24h backlog; de-escalation or further escalation on the Iran/Hormuz conflict overnight (single biggest swing factor into the EU handoff); resolution of the ONG/PROM bias-tag contradiction (human review of whether those longs should be held, tightened, or flagged for exit); confirmed technical follow-through on BNB before treating it as more than a watch.

## 7. Candidate Deep Dives

### 0G/USDT (crypto, B-tier, intraday, long, score 72.6)
- Entry band 0.2057-0.2139, invalidation 0.1956 (1h close), TP1 0.2357.
- Has price already reacted? Yes — +29.85% 24h, +31.34% 7d; current price 0.2175 sits above the entry band already.
- Is the setup chasing? **Yes, if bought at current price.** Only clean on a genuine retracement into the stated pullback zone.
- Retest/pullback structure? The desk's own entry plan explicitly requires this — "pullback into 0.2057-0.2139... no market buy if extended."
- Overextended (>2 ATR from EMA20)? Not explicitly computed in the report, but the entry-vs-current-price gap plus the "no market buy if extended" language both point that way.
- Aligned with mood? Yes for the momentum-breakout narrative basket, but the basket itself is explicitly flagged "without confirmed news catalyst."
- Actionable now? **No — watch for pullback only.** Chase risk is real at current levels.
- Invalidation: 0.1956 (1h close).
- Derivatives: negative funding across bybit/okx/mexc, cross-venue crowding "elevated" — crowded shorts, some squeeze-support for continuation, but also a sign the move may be late.
- Catalyst confirmation or contradiction? No fresh verified catalyst — pure momentum + short-crowding thesis.

### ZKC/USDT (crypto, no formal signal, short-watch only)
- No `proposed_signal` exists for this symbol in either direction — the scanner is running a bullish-regime playbook that only generates long ideas, so the weakest symbols (ONG, ZKP, ZKC, TUT, PROM) never get a formal short setup even when RS vs BTC is deeply negative.
- RS vs BTC: -14.81%, 24h -13.73% (from tonight's "Weakest Symbols" list).
- Is this a chase-risk setup? Unknown without a formal entry plan — treat any short here as fully discretionary/manual.
- What level makes it actionable? A confirmed break of the recent session low with volume would be the minimum bar; no desk-computed invalidation exists.
- Legal/headline risk: none found.
- Actionable now? **No — manual-only, low confidence.** This is a genuine "no clean trade, here's the watch trigger" case per PART 9, not a real desk signal.

### BNB/USDT (crypto, no formal signal, catalyst-watch)
- Catalyst: CME launched its Emerging Crypto Index on 2026-08-31, tracking 10 assets (BNB, XRP, SOL, HYPE, LINK, XLM, SUI, UNI, AVAX, AAVE) with BNB/XRP/SOL/HYPE carrying a combined 92.7% weight — verified via 2 independent external sources (thedefiant.io, news.bitcoin.com) plus a matching internal primary_source Telegram item.
- Has price already reacted? Not confirmed this run — no live BNB quote pulled, and no formal signal was minted for it tonight.
- Is there a retest/pullback structure? Unknown — would need the next intraday/swing cycle to surface a formal setup, or manual chart confirmation.
- Aligned with mood? Yes — a genuine, verified structural catalyst independent of the Iran/Hormuz macro overhang.
- Actionable now? **No — watch only**, pending either a desk-generated setup in the next cycle or manual technical confirmation of a clean entry.
- What would invalidate the idea? A broader risk-off flush (Iran escalation) overriding the structural-flow narrative, or the basket's own "early rotation / sell-the-news risk" flag materializing.

### ONG/USDT & PROM/USDT (crypto, existing B-tier swing longs, needs review)
- ONG/USDT: open swing long, triggered, score 73.9, entry 0.09561-0.09824, invalidation 0.09240, TP1 0.10700, created 2026-08-26. Tonight's report tags ONG bias=short, 24h -17.31%, RS vs BTC -18.39%.
- PROM/USDT: open swing long, triggered, score 73.9, entry 6.583-6.836, invalidation 6.273, TP1 7.679, created 2026-08-30. Tonight's report tags PROM bias=short, 24h -12.69%, RS vs BTC -13.77%.
- This is the same bias-tag contradiction bug flagged in `[[project_crypto_ai_desk_bias_tag_contradiction]]` (previously confirmed on these same symbols 2026-08-31) — the desk's own current-bias read has flipped against two live long positions without an automatic exit/re-flag mechanism.
- Actionable now? **Not a new entry either way — flag both for risk-manager/human review** of whether to hold to invalidation, tighten manually, or treat the bias flip as an early warning. No auto-action taken (per PART 16 permission contract).

### MANTRA/USDT (crypto, B-tier swing long, status=triggered) — unchanged
- Entry 0.004443-0.004572, invalidation 0.004285, news_supported=0. No new MANTRA/OM news found this run. Headline-overhang risk-manager watch carries forward unchanged from the 23:37 review.

## 8. Best Candidates Ranked

1. **Best long-watch: 0G/USDT** — wait for pullback into 0.2057-0.2139 with volume confirmation; do not chase the current +29.85% extension.
2. **Best catalyst-watch: BNB/USDT** — CME Emerging Crypto Index inclusion, verified; needs technical confirmation before actionable.
3. **Best short-watch: ZKC/USDT** — manual-only, no formal desk level; break of session low with volume as the minimum trigger.
4. Existing-exposure flags (not new candidates): **ONG/USDT, PROM/USDT** — bias-tag contradiction, needs risk-manager review; **MANTRA/USDT** — headline overhang, unchanged watch.
5. Manual review / avoid (not ranked as actionable): **HYPE/USDT** — see §9.

## 9. Avoid / No Trade

- **HYPE/USDT new entries** — externally verified Lazarus-Group wallet flows through Hyperliquid amid active US regulatory-entry talks; genuine platform-level regulatory/reputational tail risk. Applies to this decision window only.
- **Fresh crypto swing entries off the 24h-stale swing report** — treat the swing book as existing-position context only until a fresh report lands.
- **Stocks — all symbols** — market closed, C-tier only, planning/watchlist context until the 09:30 ET open with fresh technical confirmation.
- This is **not** an instruction to pause scanning, tracking, or the scheduler — the pipeline is currently mid-cycle and healthy as of write time, and data collection continues regardless of this verdict.

## 10. Main Risks

- **US-Iran / Strait of Hormuz escalation** — macro risk score maxed at 100/100, externally verified as real and ongoing per the prior review's sourcing; single biggest cross-asset swing factor into the EU/US handoff.
- **Scheduler timeout recurrence** — 9 events today, second consecutive cycle showing the same paper-execution-family stall pattern that produced last night's 24-event storm; self-recovered both times, but root cause still unknown (carried TODO).
- **Bias-tag contradiction bug, confirmed live again** — ONG/USDT and PROM/USDT open longs directly contradicted by current bias=short tags; a human should confirm these positions are still sound before treating their status as normal.
- **Catalyst mapping weak** (66.4% unmapped) — treat catalyst-driven verdicts as directional context, not proof.
- **Persistent cross-exchange-confirmation underperformance** (PF 0.42 vs Binance-only PF 2.4x) — unresolved across multiple reviews, worth a scoring-weight look in a human session.
- **HYPE two-sidedness** — a genuine structural tailwind (CME index) sits alongside a genuine regulatory overhang (Lazarus flows) on the same asset; do not read the CME catalyst as clearing the risk flag.

## 11. Action Plan — next 4 hours

- Watch 0G/USDT for a genuine pullback into 0.2057-0.2139 with volume before considering a long; do not chase at current levels.
- Watch BNB/USDT for a desk-generated setup or manual technical confirmation of the CME-index catalyst before treating it as actionable.
- Monitor overnight Iran/Strait-of-Hormuz headlines into the EU session — the single biggest swing factor for both crypto risk appetite and the 11:30 EU/pre-US review.
- Flag ONG/USDT and PROM/USDT open longs for human risk-manager review given the bias-tag contradiction — do not auto-close or auto-adjust (outside this run's permissions).
- If the paper-execution timeout cluster recurs a third consecutive cycle, escalate beyond a §14 TODO in the next human-driven session — two consecutive occurrences of the same step family stalling is now a pattern, not a one-off.
- Re-check stocks INTU (class-action/securities-fraud) and NVDA (indictment) legal flags before either could be considered for promotion after the US open.

## 12. Final Verdict per Mode

- **Crypto scalp**: disabled by design (unchanged, 2026-07-07 policy) — no verdict needed; signal-stats confirms this bucket remains a confirmed loser (PF 0.16-0.17 range) where still tracked historically.
- **Crypto intraday**: **selective / pullback-only** — fresh report (1h old), bullish regime, but every B-tier idea is a no-catalyst momentum play with a known net-negative playbook tail; 0G is the best of the group, watch-only pending pullback.
- **Crypto swing**: **hold existing / no new entries** — report ~24h stale, no regen since yesterday; existing book (incl. MANTRA, ONG, PROM, TUT and others) carries forward, with ONG/PROM flagged for the bias-contradiction review.
- **Stocks intraday**: **closed / planning only** — all C-tier post market-closed gate; watch COP, CRWD, NOW, XOM, QCOM for the open, with INTU and NVDA excluded pending legal-risk review; earnings today (PANW, DELL, CRWD) and tomorrow (AVGO, CRM, SNOW) — avoid chasing into prints.
- **Stocks swing/invest**: deprecated pipelines, not evaluated.

## 13. Sources

- [North Korean hackers are moving tens of millions on Hyperliquid as Trump pushes to onshore the crypto platform — CoinDesk](https://www.coindesk.com/business/2026/08/31/north-korean-hackers-are-moving-tens-of-millions-on-hyperliquid-as-trump-pushes-to-onshore-the-crypto-platform) (2026-08-31)
- [Lazarus moves $30M through Hyperliquid as US talks advance — crypto.news](https://crypto.news/lazarus-moves-30m-through-hyperliquid-us-talks-advance/) (2026-08-31)
- [CME Launches Crypto Index That Excludes Bitcoin and Ether — The Defiant](https://thedefiant.io/converge/markets/cme-launches-crypto-index-that-excludes-bitcoin-and-ether) (2026-08-31)
- [CME Group Launches Crypto Index Futures Tracking Bitcoin, Solana and XRP — news.bitcoin.com](https://news.bitcoin.com/cme-group-launches-crypto-index-futures-tracking-bitcoin-solana-and-xrp/) (2026-08-31)
- Internal: `data/reports/intraday/2026-09-01_00-45_intraday_report.md` (2026-09-01 03:45 EEST); `data/reports/stocks/intraday/2026-09-01_01-37_stocks_intraday_report.md` (2026-09-01 04:37 EEST); `data/catalysts/2026-09-01/catalyst_cycle_00-52.md` + `catalyst_events.jsonl` (2026-09-01 03:52 EEST); `db/crypto_ai_desk.sqlite` `proposed_signals` table (direct read, ONG/PROM/TUT/MANTRA/ZKC/ZKP queries, 2026-09-01 04:40 EEST); `data/scheduled_runs/2026-09-01_default_schedule/scheduler.log` (full-day timeout audit).

## 14. Fix Requests / TODO

### TODO-bias-tag-contradiction-recurrence-sept1 (recurrence of `[[project_crypto_ai_desk_bias_tag_contradiction]]`)
- **issue:** Direct DB query this run confirms ONG/USDT and PROM/USDT both carry **open paper LONG swing positions** (`status='triggered'`) while the current-cycle intraday report tags both symbols `bias=short` with double-digit negative 24h moves (-17.31% and -12.69% respectively). This is the same systemic, symbol-agnostic bug previously logged against these exact two symbols (plus PUMP/BICO) on 2026-08-31 — still unfixed, still recurring.
- **evidence:** `db/crypto_ai_desk.sqlite` `proposed_signals`: ONG/USDT `signal created_at=2026-08-26T02:59:24Z, mode=swing, direction=long, status=triggered`; PROM/USDT `signal created_at=2026-08-30T04:34:08Z, mode=swing, direction=long, status=triggered`; both symbols appear in tonight's `2026-09-01_00-45_intraday_report.md` §2 "Weakest Symbols" list tagged `bias short`.
- **suggested manual fix:** as previously recommended — audit whether the "bias" field computed for the market-flow section is meant to reconcile against open positions in the same symbol, or add an explicit cross-check/alert when a symbol's current bias contradicts an open position's direction, surfaced to the risk-manager layer rather than silently coexisting.
- **priority:** high
- **first observed:** 2026-08-08 (ZBT/ACE per project memory); escalated 2026-08-31 (ONG/PROM/PUMP/BICO); confirmed recurring 2026-09-01 04:41 EEST (this run, same ONG/PROM pair).

### TODO-scheduler-timeout-second-consecutive-cycle
- **issue:** For the second consecutive review cycle, the same paper-execution/structural-TP/structural-stop step family has hit a multi-event `CMD TIMEOUT` cluster: last night 24 events across nearly every non-report step (19:06-23:04:58, including the swing report itself); tonight a smaller 9-event recurrence, with a clean 4-in-a-row cluster specifically on `paper execution accounting refresh` → `paper structural TP refresh` → `paper structural stop plan` → `paper entry-mode classify` (03:57:49-04:12:51). Both nights self-recovered within ~20-45 minutes without intervention.
- **evidence:** `data/scheduled_runs/2026-09-01_default_schedule/scheduler.log`, lines `2026-09-01 03:57:49,083 [ERROR] CMD TIMEOUT: paper execution accounting refresh` through `2026-09-01 04:12:51,182 [ERROR] CMD TIMEOUT: paper entry-mode classify`; prior occurrence in `data/scheduled_runs/2026-08-31_default_schedule/scheduler.log` per the 23:37 review.
- **suggested manual fix:** given the same step family is implicated two cycles running, prioritize this over other scheduler-health TODOs — profile the paper-execution/structural-TP/structural-stop code path specifically (DB lock contention, growing dataset scan cost, or a shared resource with the retention/report jobs that also stalled last night) rather than treating each night's storm as an isolated incident.
- **priority:** high
- **first observed (this occurrence):** 2026-09-01 03:57:49 EEST; pattern first flagged per `[[project_crypto_ai_desk_scheduler_hang]]` and escalated across the 21:50/23:37 reviews on 2026-08-31.

### TODO-cross-exchange-confirmation-persistent-underperformance (carried forward, unchanged)
- **issue:** `signal-stats --asset-class crypto` continues to show the `exchange_confirmation` cohort requiring cross-exchange confirmation materially underperforming the Binance-only cohort — tonight: cross-exchange n=73, PF 0.42, totalR -11.x vs Binance-only n=133, PF 2.4x, totalR +21.7. This gap has now appeared consistently across multiple review cycles without a fix.
- **evidence:** `signal-stats --asset-class crypto` output this run, "By exchange_confirmation" table.
- **suggested manual fix:** review whether the cross-exchange-confirmation requirement is filtering in weaker setups (e.g. picking up thinner/less liquid symbols only tradeable on secondary exchanges) rather than adding confirmation value; consider tightening or removing this path if the gap persists after another sample-size check.
- **priority:** medium
- **first observed:** prior to 2026-08-31 (carried forward across multiple reviews); reconfirmed 2026-09-01 04:41 EEST.

_Carried forward, unchanged, no new evidence this run (stocks market closed overnight, lower priority for this slot): TODO-duplicate-stock-signal-ids (7+ symbols: ABNB, BA, UBER, SBUX, GOOGL, AFRM, CRCL — see `OPUS_ENRICHED_REVIEW_AUTO_2026-08-31_2337.md` §14); TODO-catalyst-symbol-resolver-miss-GE-vernova; TODO-mantra-headline-overhang-risk-review — all still open, no action needed here beyond re-flagging._
