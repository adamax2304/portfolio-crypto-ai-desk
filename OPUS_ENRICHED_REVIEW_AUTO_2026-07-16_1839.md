# Opus Enriched Review — US open reaction review — Auto Cycle 18:39 EEST

## 1. Executive Summary

Slot: **US open reaction review** (first US-session reaction / early confirmation), run **2026-07-16, 18:39-18:55 EEST**, ~2h25m after the 16:30 EEST / 09:30 ET US cash open. **Advisory only — no auto-trade, no code/scoring/routing changes.** Data pipeline is healthy: cycle 5 (16:43-17:31 EEST) completed **69/69 steps, 0 failures**; crypto scalp/intraday fresh (~1h48m/1h42m old at review start), crypto swing carry-forward (~2h12m old, still within the fresh band), stocks intraday very fresh (report cadence every ~10min, latest 15:33 UTC / 18:33 EEST, ~6min old). **The pre-open thesis from the 16:20 EEST review has partly confirmed and partly stalled**: the semiconductor short thesis (AMD) is externally confirmed — chip stocks fell for a **second consecutive day** at the open (TSM -2.2% to -4% intraday despite a beat, WDC/SNDK down 7-8%, Nasdaq -0.7% to -0.76%) — but **no fresh stocks A/B has actually fired since the open**: every 10-minute stocks-intraday cycle from 13:33 through 15:33 UTC (six consecutive cycles spanning the entire post-open session) shows **zero actionable A/B**, with every high-scoring name (AAPL, JPM, XLE, XOM, LLY, all scoring 83-100 pre-gate) blocked by `stocks_intraday_7d_drawdown_guard` / `stocks_intraday_long_guard` or `rr_below_min_required`. **UNH's situation has sharpened, not resolved**: the beat-and-raise (+6% premarket, now +3.5% intraday) is now stacked against an **externally-confirmed widened DOJ probe** — new civil investigative demands into the Claritev unit alleging insurer collusion, on top of the existing Medicare-billing probe — reinforcing AVOID/MANUAL REVIEW, now on stronger grounds than at 16:20 EEST. **Crypto produced two new B-tier swing/intraday BANK/USDT longs** (waiting_for_entry, pullback zone 0.0561-0.0574, current price 0.0579 — within ~0.2 ATR of trigger) since the last review, while ONDO/USDT and XLM/USDT both progressed from tp1_hit to **tp2_hit**. **Geopolitical escalation continues, externally confirmed as still live** (new US strikes reported on Qeshm Island/Bandar Abbas/Chabahar); crypto continues to absorb it (BTC ~$64.7k -0.4%, ETH ~$1,917 +1.5%). Catalyst mapping remains weak (19.9% mapped / 80.1% unmapped, direct count — context only). **One new untracked legacy crypto alert** (ALLO/USDT swing) appeared this cycle — the first non-zero reading after several consecutive clean reviews. All 4 monitors healthy.

## 2. Data Used

- Reports: `2026-07-16_13-51_scalp_report.md` (crypto scalp, ~1h48m old, mode kill-switched); `2026-07-16_13-57_intraday_report.md` (crypto intraday, ~1h42m old, regime range/chop); `2026-07-16_14-27_swing_report.md` (crypto swing, ~2h12m old, carry-forward band, regime uptrend/uptrend at run time); `2026-07-16_15-33_stocks_intraday_report.md` (stocks, ~6min old at review start, market open + ~2h03m into RTH) plus six intermediate stocks-intraday cycles (13:33-15:33 UTC) reviewed for the post-open trajectory.
- Stocks swing/invest: last file `2026-07-02_13-03` / `2026-07-02_13-05` — **14 days old, STALE, excluded** (unchanged from prior reviews; deprecated legacy playbooks per project memory, replaced by shadow-only `stocks_swing_growth_breakout`).
- Catalyst / narrative: `data/catalysts/2026-07-16/catalyst_events.jsonl` (direct count: 497/2,500 mapped = 19.9%) and `narrative_baskets.jsonl`; latest scan cycle `catalyst_cycle_14-01.md` (14:01 UTC / 17:01 EEST).
- CLI: `active-signals` (crypto ×4, stocks ×50/14 B-tier), `signal-stats` (crypto: A/B headline PF 1.67, n=168 reliable, winrate 21.5%; stocks: A/B headline PF 0.67, n=14 weak, winrate 28.6%; stocks all-tier diagnostic n=225 reliable PF 0.63), `detect_untracked_legacy_alerts --since 2026-07-16` (**1 result** — ALLO/USDT swing B, sent 14:27 UTC).
- `data/scheduled_runs/2026-07-16_default_schedule/cycle_05_16-43_summary.md` — 69/69 ok, paper monitor status (step #67), scheduler.log mtime 17:31 EEST.
- `reports/PAPER_MONITOR_STATUS_LATEST.md` — Open actionable: 1 (ALLO/USDT crypto/intraday/B, entry filled, monitoring TP/SL, as of 17:31 EEST cycle; no longer in the live active-signals table at review time, implying it resolved between the last cycle and now — exact outcome not queried further, informational only).
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-16_1620.md` (16:20 EEST, pre-US-open decision review) — used for §4 comparison.
- **External web research performed** (needed to confirm whether the pre-open AAPL/AMD theses played out at the open, whether UNH's DOJ situation changed, and whether the Iran/Bahrain/Kuwait escalation continued):
  - WebSearch: "stock market today July 16 2026 S&P Nasdaq Dow US open reaction UNH NFLX chip stocks" — confirmed S&P -0.37%, Nasdaq -0.76%, Dow +0.14% early; TSM fell >4% despite a 77% earnings beat (capex-guidance "sell the news"); WDC -8%, SNDK -8%; UNH +6% premarket (beat, raised guidance); NFLX reports after close, historically weak reaction to its last four reports; June retail sales +0.2% MoM (below 0.3% consensus).
  - WebFetch: Yahoo Finance live-blog — confirmed semis weak for a **second consecutive day**, TSM -2.23% intraday (later reading, softer than the -4% premarket figure — normal intraday fade); UNH +3.48% intraday (moderated from +6% premarket); AAPL/AMD not specifically named in this particular live-blog snapshot (checked, not found — no contradiction either direction).
  - WebSearch: "Bitcoin Ethereum price July 16 2026 Iran Bahrain Kuwait escalation update" — confirmed BTC opened $64,720.36 (-0.4%), ETH opened $1,917.05 (+1.5%); confirmed the Iran/Bahrain/Kuwait situation remains live and escalating, not cooling — new US strikes reported on Qeshm Island, Bandar Abbas, Chabahar; Iran threatening to "crush" regional infrastructure if further attacked.
  - WebSearch: "UnitedHealth UNH stock DOJ investigation July 16 2026 update" — confirmed the DOJ probe has **widened**: new civil investigative demands into the Claritev health-tech unit alleging collusion with major insurers, layered on top of the existing Medicare Advantage billing/risk-score probe. Q2 revenue $112.0B, guidance raised, confirmed same-day.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime 17:31 EEST (~1h08m old at review start), `cycle_05_16-43_summary.md` mtime 17:31 EEST (~1h08m old) — both well under the 3h defer threshold. **Not deferred.**
- Cycle 5: **ok=69, failed=0** — full clean run (16:43-17:31 EEST), including crypto scalp/intraday, stocks intraday, catalyst scan, paper execution accounting, paper-shadow A/B, obsidian refresh. No regressions from cycle 4.
- Crypto scalp (~1h48m old, mode kill-switched, structurally negative playbook, data-collection only) / intraday (~1h42m old, regime range/chop, macro risk 100/100) fresh; crypto swing (~2h12m old, 14:27 UTC) is inside the fresh band (<4h), regime read uptrend/uptrend (BTC+ETH), a **warmer** read than the cooler scalp/intraday range/chop — a genuine intraday regime-drift signal, not a data problem.
- Stocks intraday refreshing every ~10 minutes since the open; the run reviewed spans 6 consecutive post-open cycles (13:33-15:33 UTC) with **zero A/B actionable in every single one** — this is not a data-freshness issue, it is a persistent guard-driven no-new-entries state (`stocks_intraday_7d_drawdown_guard` / `stocks_intraday_long_guard` / `rr_below_min_required`) — see §10 and TODO-1.
- Monitors: all 4 (crypto, pending, stocks, derivatives) healthy, log files updated within the last few minutes as of review start.
- Paper Monitor Status (cycle 5, #67, telegram, 17:31 EEST): **Open actionable: 1 (ALLO/USDT crypto intraday B) · Waiting for entry: 2 (BANK/USDT swing+intraday) · Entered unresolved: 0 · Review/Shadow: 88 · No-entry/stale/moved-away: 13 · Closed today: 205W / 45L / 47flat · Needs review: 0.**
- Untracked legacy crypto alerts: **1** (ALLO/USDT swing B, 65.4, sent 2026-07-16T14:27:05 UTC, no matching proposed_signal within ±6h) — first non-zero reading since this detector's fix was confirmed clean across the last several reviews; see TODO-3.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-07-16 18:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["cycle_05 69/69 ok, 0 failed, finished 17:31 EEST", "crypto scalp/intraday <1h50m old, stocks intraday refreshing every ~10min, latest ~6min old", "crypto swing ~2h12m old, inside fresh band, regime read warmer than scalp/intraday", "stocks swing/invest 14 days old, stale/deprecated, excluded"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["mixed", "chop", "risk_off", "shorts_preferred"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC range/ETH uptrend per scalp/intraday vs BTC/ETH both uptrend per fresher swing read — genuine intraday warming, macro risk still 100/100 on live Iran/Bahrain/Kuwait escalation", "external: BTC $64.7k -0.4%, ETH $1,917 +1.5%, absorbing escalation without breakdown", "stocks: S&P -0.37%, Nasdaq -0.76%, Dow +0.14% at the open; semis weak for a second consecutive day (TSM -2.2% to -4%, WDC/SNDK -7-8%); healthcare/financials/energy strongest sectors (20d RS)", "retail sales +0.2% MoM, below 0.3% consensus — a soft data point, not a shock"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "catalyst_confirmed", "narrative_supported", "catalyst_contradicted"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl today: 497/2,500 mapped (19.9% direct count)", "active baskets: rwa_narrative (ONDO/XLM), momentum_breakout (BANK/ONDO, catalyst-backed on ONDO only), perps_dex_narrative (HYPE), ai_narrative (NEAR/RENDER/TAO/FET), delisting_thin_liquidity (BTC)", "UNH: earnings-beat catalyst now contradicted by an externally-confirmed WIDENED DOJ probe (Claritev antitrust CID added to the existing Medicare-billing probe) — contradiction sharper than at 16:20 EEST"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "oi_supports", "data_unavailable"], "data_missing": ["derivatives for several MEXC-only weak_vs_market names"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BANK/USDT: price +17-40% (report-dependent) + OI +57-61%, but long/short ratio 0.61-0.64 (shorts > longs) despite the rally — fresh positioning with a short-heavy skew, a latent squeeze setup, not a clean crowded-long", "ONDO/USDT: price up + OI up, funding slightly negative, long/short 1.42-1.43, crowding normal — cleaner trend confirmation than BANK", "ALLO/USDT: price up + OI down, short covering, weaker continuation quality"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "clean_retest", "waiting_for_entry", "price_moved_away"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BANK/USDT: explicitly flagged '>2 ATR from EMA20 — do not chase' in scalp/intraday, but the swing B-tier pullback entry (0.0561-0.0574) sits only ~0.2 ATR below the current price (0.0579) — close to trigger, not a chase if it fills there", "AAPL/JPM/XLE/XOM/LLY: all scored A-tier pre-gate at/after the open but blocked every single cycle since 13:33 UTC by the drawdown guard or RR-below-min gate — never actually confirmed as live entries despite the pre-open long-watch thesis", "AMD: sector-level short thesis externally confirmed (semis weak 2nd day) but the specific AMD signal remains gate-blocked (drawdown guard), same as all other names"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.75,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow", "no_entry"], "data_missing": ["exact resolution path for ALLO/USDT between the 17:31 EEST cycle and this review"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Paper Monitor (17:31 EEST): open_actionable=1 (ALLO/USDT crypto intraday B), waiting_for_entry=2 (BANK/USDT swing+intraday), entered_unresolved=0, review_shadow=88, no_entry/stale/moved_away=13, needs_review=0, closed_today=205W/45L/47flat", "live active-signals query (18:39 EEST) shows only 4 crypto signals: BANK swing+intraday waiting, ONDO intraday tp2_hit, XLM swing tp2_hit — ALLO no longer listed, implying it resolved (TP or stop) in the intervening ~1h08m, not confirmed which", "stocks active-signals: 14 B-tier, nearly all tp1/tp2_hit or triggered; several (XOM expires 2026-07-14, multiple SMH/LLY expires June) are legacy-stale non-terminal statuses — see TODO-2 (carried from prior review, still open)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["legal_risk", "headline_risk", "reduce_risk"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: DOJ probe confirmed WIDENED today (Claritev antitrust CID + existing Medicare-billing probe) stacked with a genuine beat-and-raise (+3.5% intraday, moderated from +6% premarket) — contradiction now stronger than at 16:20 EEST, AVOID/MANUAL REVIEW reinforced, not resolved", "NFLX: reports after today's close, historically weak reaction to its last four prints, do_not_chase_warning active", "MSFT: C-tier, active legal/headline risk flag (securities_fraud) in the stocks report — background, not a top candidate this cycle", "geopolitical: Iran/Bahrain/Kuwait escalation externally confirmed as still live (new strikes on Qeshm Island/Bandar Abbas/Chabahar), macro risk 100/100 justified, unchanged in severity from 16:20 EEST"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto weekly headline: PF 1.67, n=168 reliable, winrate 21.5% — consistent with prior reviews, mode=swing (BANK's mode) historically the strongest sub-cohort per the swing report's own text (14d WR 72%/PF 5.80)", "crypto scalp mode structurally negative, kill-switched, unchanged", "stocks weekly headline A/B: PF 0.67, n=14 weak-confidence, winrate 28.6% — still too small a sample to trust a fresh stocks A/B even if one clears the guards", "stocks all-tier diagnostic (n=225, reliable): PF 0.63 — the guard's aggressive blocking this session is consistent with a genuinely weak recent stocks A/B/C track record, not an obviously miscalibrated gate"] },
    { "agent": "head_trader", "verdict": "watch_only", "confidence": 0.6,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of the eight agents above; the desk is data-healthy; crypto has two close-to-trigger BANK swing/intraday longs on its strongest playbook plus two already-running B-tier positions (ONDO, XLM) at tp2_hit; stocks has directionally-confirmed sector theses (semis weak, healthcare/financials strong) but the drawdown guard has kept the book flat on NEW stocks entries for the entire session so far — that is itself the headline of this review, not a data gap"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "BANK/USDT", "trigger": "swing B-tier pullback entry 0.0561-0.0574 (current 0.0579, ~0.2 ATR away); strongest crypto playbook (14d WR 72%/PF 5.80); do not market-buy at the current extended price, only the printed pullback zone" },
    "best_short_candidate":    { "symbol": "AMD", "trigger": "sector-level thesis externally confirmed (chip stocks weak 2nd consecutive day, TSM/WDC/SNDK all down) but the specific AMD signal remains blocked by stocks_intraday_7d_drawdown_guard all session — wait for the guard to lift or a fresh gate-clean signal before treating as live" },
    "best_catalyst_candidate": { "symbol": "ONDO/USDT", "trigger": "dual narrative-basket (rwa_narrative + momentum_breakout), existing B-tier intraday long already tp2_hit and running — manage the open position, do not add fresh exposure at the current extension" },
    "avoid_candidate":         { "symbol": "UNH", "reason": "DOJ probe confirmed WIDENED today (new Claritev antitrust CID) stacked on the existing beat-and-raise gap — contradiction sharper than the last review, not a clean actionable either direction" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh | advisory_only |
| market_regime | caution | 0.65 | mixed, chop, risk_off, shorts_preferred | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, catalyst_confirmed, narrative_supported, catalyst_contradicted | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk, oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, clean_retest, waiting_for_entry, price_moved_away | advisory_only |
| execution_lifecycle | ok | 0.75 | open_actionable, waiting_for_entry, review_shadow, no_entry | advisory_only |
| risk_manager | caution | 0.70 | legal_risk, headline_risk, reduce_risk | advisory_only |
| playbook_performance | caution | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | watch_only | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (2026-07-16 16:20 EEST, pre-US-open decision review)

- **The US cash open happened and produced a partial confirmation**: chip-sector weakness (AMD short-watch thesis) externally confirmed — TSM fell despite a strong beat, WDC/SNDK down 7-8%, Nasdaq -0.76% — but this remains a **sector-level** confirmation, not a live AMD signal; the specific AMD candidate is still gate-blocked.
- **AAPL long-watch did NOT confirm as a fresh live entry**: across all six 10-minute stocks-intraday cycles since the open (13:33-15:33 UTC), AAPL scored A-tier pre-gate every single time (85-97) and was demoted to C every single time by the same drawdown/RR guards — the printed 326.17-327.57 zone from the 16:20 EEST review never became a Telegram-actionable trade this session.
- **UNH's contradiction sharpened**: the DOJ probe is now externally confirmed to have **widened** (new Claritev antitrust civil investigative demand, alleging insurer collusion) on top of the pre-existing Medicare-billing probe — the AVOID/MANUAL REVIEW verdict is unchanged in direction but now rests on stronger, fresher evidence than at 16:20 EEST.
- **Crypto**: two new B-tier BANK/USDT longs (swing + intraday) appeared since the last review — not present in the 16:20 EEST active-signals table. ONDO/USDT and XLM/USDT both progressed from tp1_hit (16:20 EEST) to **tp2_hit** (this review) — both existing positions running correctly.
- **New untracked legacy crypto alert**: 1 (ALLO/USDT swing B) — the detector had been clean (0) across the last several reviews; this is the first recurrence. Not yet a pattern, flagged as a fresh TODO rather than folded into the old (already-resolved) one.
- **Catalyst mapping**: 19.9% mapped this run (direct count) vs. 19.6% at 16:20 EEST — persistently weak, essentially flat, consistent pattern.
- **Geopolitical situation**: unchanged in severity — still live, still escalating (new strikes reported), not de-escalating; crypto continues to absorb it without a breakdown.
- **TODO-2 and TODO-3 from the 16:20 EEST review remain open** (stocks B-tier legacy non-terminal statuses; the 04:30/11:30 EEST review-schedule gap from 2026-07-15/16) — not re-diagnosed this run, still out of scope per §B.

## 5. Catalyst Coverage

- Total catalyst_events rows today (direct JSONL count): **2,500** — mapped (non-null symbol): **497** (19.9%), unmapped: **2,003** (80.1%).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top unmapped headline types (sampled): (1) exchange delisting/listing batch announcements not attributable to one symbol; (2) generic macro/geopolitical headlines (Iran, CLARITY Act) without a clean ticker match; (3) miscellaneous PR/company-notice items with symbols outside the desk's tracked universe (e.g., non-tracked small caps).
- Active narrative baskets (per latest `catalyst_cycle_14-01.md`, 17:01 EEST): **rwa_narrative** (ONDO/XLM, `related_beta_rotation`, fresh <6h); **delisting_thin_liquidity** (BTC, `avoid_low_liquidity`, fresh <1h); **perps_dex_narrative** (HYPE, `wait_pullback`, fresh <1h); **ai_narrative** (NEAR/RENDER/TAO/FET, `related_beta_rotation`, fresh <24h); **momentum_breakout** (BANK+ONDO, `wait_pullback`, fresh <1h — ONDO explicitly flagged catalyst-backed within this basket, BANK explicitly flagged as NOT catalyst-backed, momentum-only).
- Notable mapped events: continued ETH-adjacent DeFi-hack backdrop (Ostium $18-23.75M oracle-manipulation exploit laundered via Tornado Cash; Summer.fi $6M vault exploit wind-down) — elevated caution on DeFi-correlated ETH exposure, not a direct ETH sell signal; TSLA SEC settlement ($1.5M fine, Twitter-disclosure matter, resolved not escalating).

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **mixed, absorbing live geopolitical risk, intraday regime slightly warming** — scalp/intraday reads range/chop (BTC range, ETH uptrend), the fresher swing read has BTC and ETH both in uptrend; external BTC -0.4% to $64.7k, ETH +1.5% to $1,917, both largely unbothered by the still-live Iran/Bahrain/Kuwait escalation; macro risk pinned 100/100. No A-tier anywhere; crypto scalp mode remains globally off.
- Stocks mood: **risk_on regime label but effectively flat on new entries** — VIX ~16 (not elevated), breadth 75%/100% above EMA20/50, S&P -0.37%/Nasdaq -0.76%/Dow +0.14% at the open; healthcare/financials/energy are the strongest 20d-RS sectors, semiconductors/technology/materials the weakest — directly consistent with the AMD short thesis and the UNH (healthcare) long-side backdrop. Despite this, the desk's own drawdown guard has produced **zero** new actionable A/B all session.
- Dominant narrative: crypto — RWA (ONDO/XLM) and momentum (BANK) baskets are the freshest live setups; stocks — the semiconductor unwind (now a second consecutive weak day, "sell the beat" on TSM's capex-heavy guidance) continues to be the session's defining story, alongside UNH's earnings-vs-legal-risk contradiction sharpening.
- Preferred side now: **mixed, asset-class-specific and gate-aware** — crypto: BANK (long, near-trigger pullback) and the existing ONDO/XLM longs (manage, don't add); stocks: directionally short-biased on semis and long-biased on healthcare/financials by sector-RS, but the drawdown guard is overriding almost every individual name into non-actionable C regardless of direction — respect the gate rather than overriding it.
- Best long candidate: BANK/USDT (crypto, near-trigger pullback entry on the desk's strongest playbook).
- Best short candidate: AMD (stocks, sector-confirmed but individually gate-blocked all session — a watch, not a live trigger).
- Best catalyst-backed candidate: ONDO/USDT (crypto, dual-basket, already running at tp2_hit).
- What to avoid: UNH (DOJ probe now confirmed widened, stacked with an earnings-day gap); NFLX (reports after close, do-not-chase pre-print); any BANK/USDT market-buy at the current extended price (only the printed 0.0561-0.0574 pullback zone is the plan); any stocks A-tier-score name treated as live without RR/guard clearance — the gate has held all session, treat that as informative, not an error to route around.
- What would change the view: NFLX's after-close print; further Iran/Bahrain/Kuwait escalation or a genuine de-escalation signal; the stocks drawdown guard actually clearing on a name (would be the first new stocks A/B of the day); BANK/USDT filling its 0.0561-0.0574 pullback zone; any de-escalation or further widening in the UNH DOJ situation.

## 7. Candidate Deep Dives

### 1. UNH — stocks, contradiction case, sharpened (beat-and-raise vs. widening DOJ probe)
- No open UNH signal in the actionable B-tier table; multiple C-tier long/short legacy carryovers exist (waiting/triggered/tp1_hit), not live decision points.
- Has price already reacted to the catalyst? Yes — Q2 revenue $112.0B vs $110.8B est, adjusted EPS beat, FY26 guidance raised to $19.50-$20.00; stock +6% premarket, moderating to **+3.48% intraday** (external, confirmed) as the session progressed.
- Legal/headline check: **confirmed and worse than at 16:20 EEST** — the DOJ probe has **widened**: new civil investigative demands into the Claritev health-tech unit alleging collusion with major insurers, layered on top of the pre-existing Medicare Advantage billing/risk-score probe. Per §I, a confirmed, worsening legal/DOJ risk keeps the final verdict AVOID/MANUAL REVIEW regardless of the strong print — the two facts do not cancel out.
- Chasing? A fresh long here would now be chasing a moderating gap into a probe that just got broader, not narrower — a strictly worse risk/reward than at the open.
- Mood alignment: irrelevant to the verdict — hard avoid-for-fresh-entry regardless of the broader stocks mood or healthcare-sector strength.
- **Verdict: AVOID / MANUAL REVIEW REQUIRED for any fresh exposure, reinforced this cycle. The earnings print is still genuinely strong, but the legal overhang got bigger, not smaller, since the last review.**

### 2. AMD — stocks, short-watch, sector-confirmed but individually gate-blocked
- Score 74-86 (pre-gate B/A across cycles), final tier **C** consistently via `stocks_intraday_7d_drawdown_guard` (every cycle from 13:33 to 15:33 UTC) — sometimes also `atr_only_tp1_capped_to_B`.
- Has price already reacted? Directionally, yes at the sector level — confirmed **externally**: chip stocks fell for a **second consecutive day**, TSM dropped despite a 77% earnings beat and raised capex guidance ($60-64B, up from $52-56B) as investors read the capex increase as a margin worry, not a demand signal; WDC/SNDK down 7-8%; Nasdaq -0.76% at the open, still soft.
- Chasing? The sector move is real and ongoing, but the individual AMD signal has not cleared the desk's own gates all session — entering off the sector narrative alone, bypassing the drawdown guard, would be exactly the kind of override the gate exists to prevent.
- Retest/pullback structure? Not established via a clean gate-cleared signal; the sector weakness itself does not need a retest to be real, but AMD-specific entry structure does.
- Legal/headline/catalyst check: no AMD-specific negative catalyst; pure sector/macro read-through from TSM's earnings-day guidance.
- Mood alignment: strongly aligned — semiconductors remain the weakest 20d-RS sector (SMH -7.28% vs SPY) and today's external price action reinforces it for a second day running.
- **Verdict: SHORT-WATCH, sector-confirmed. Do not treat the confirmed sector weakness as a green light to bypass the gate on the individual name — wait for the drawdown guard to lift or a fresh gate-clean AMD signal.**

### 3. BANK/USDT — crypto, long, best long-watch (near-trigger pullback, strongest playbook)
- Two active B-tier signals: swing (score 69.3, `waiting_for_entry`) and intraday (score 66.1, `waiting_for_entry`), both entry zone 0.0561-0.0574, invalidation 0.0546-0.0546, expiring 2026-07-23 (swing) / 2026-07-17 (intraday).
- Playbook: `crypto_swing_narrative_rs_momentum` — the desk's own text calls out this playbook's 14d track record as WR 72% / PF 5.80 / +24R, the strongest sub-cohort on the crypto side.
- Has price already reacted to the catalyst? Yes, dramatically — 24h return ranges 17-40% across today's reports (report-timing dependent), RS vs BTC +18-41%; both scalp and intraday reports explicitly flag it "more than 2 ATR from EMA20 — do not chase" at the market-price level.
- Chasing? A market entry now would be chasing; the system's own limit-order plan (pullback zone 0.0561-0.0574) is the correct way to engage this name, and per the swing report's most recent desk notes, current price (0.0579) sits only **~0.2 ATR** above the top of that zone — genuinely close to filling, not a distant wish.
- Retest/pullback structure? In progress by design — this is exactly what the waiting_for_entry status represents.
- Legal/headline/catalyst check: none negative found for BANK specifically; the momentum_breakout basket explicitly notes BANK is **not** catalyst-backed (momentum-only), unlike its basket-mate ONDO.
- Derivatives: price up + OI up sharply (+57-61% 24h), but long/short ratio 0.61-0.64 (shorts outnumber longs) — a short-heavy positioning skew alongside a strong rally, a latent squeeze setup rather than a crowded-long risk.
- **Verdict: WATCH for the pullback fill. Close to trigger (~0.2 ATR away); do not market-buy at the extended price — let the printed 0.0561-0.0574 zone do the work. If filled, this sits on the desk's best-performing crypto playbook.**

### 4. AAPL — stocks, long-watch that did not confirm this session
- Score 85-97 (pre-gate A-tier every single cycle since the open), final tier **C** every single time via `stocks_intraday_7d_drawdown_guard` / `stocks_intraday_long_guard`.
- Has price already reacted to the catalyst? The 16:20 EEST review's printed long zone (326.17-327.57) was a pre-open reference; no fresh gate-clean AAPL B/A-tier signal has fired at that zone or any other zone this session — six consecutive 10-minute cycles (13:33-15:33 UTC) all show AAPL demoted to C.
- Chasing? Not applicable — there was never a live trigger to chase; the honest read is that the desk's own risk gate has kept this name out of Telegram-actionable status through the entire post-open window so far, independent of how price actually moved.
- Retest/pullback structure? Unknown from gate-blocked data alone; would need the guard to clear before a live structure read is meaningful.
- Legal/headline check: unchanged from 16:20 EEST — the Cotton/CXMT chip-sourcing political-pressure story remains background regulatory noise, not a hard block.
- Mood alignment: technology sector remains weak on 20d RS (consistent with the broader chip-sector story), AAPL's idiosyncratic RS-leader status unchanged from the last review.
- **Verdict: WATCH, unconfirmed. The pre-open thesis has neither been validated nor invalidated by price — it has simply never been tested, because the desk's own drawdown guard has not let a single stocks A/B through all session. Treat as still-pending, not as a failed or successful call.**

### 5. ONDO/USDT — crypto, long, best catalyst-backed candidate (running position, tp2_hit)
- Active B-tier intraday long, **tp2_hit** (upgraded from tp1_hit at the 16:20 EEST review), expires 2026-07-17T08:36:31.
- Dual narrative-basket primary: `rwa_narrative` (with XLM) and `momentum_breakout` — explicitly flagged catalyst-backed within the momentum basket (unlike basket-mate BANK).
- Has price already reacted? Yes — still extended per today's reports (17-18% 24h range across cycles), RS vs BTC +18%.
- Chasing? A fresh entry now would be chasing an already-running, already-profitable position; the correct action is to manage the existing tp2_hit position per its invalidation level, not add fresh size.
- Derivatives: price up + OI up, funding slightly negative, long/short 1.42-1.43, crowding normal — a cleaner trend-confirmation profile than BANK's short-heavy skew.
- Legal/headline/catalyst check: none negative found for ONDO specifically.
- **Verdict: MANAGE the existing position (tp2_hit, running correctly). Do not add fresh exposure at the current extension.**

## 8. Best Candidates Ranked

1. **BANK/USDT — best long-watch (crypto)** — near-trigger pullback entry (~0.2 ATR away) on the desk's strongest playbook (14d WR 72%/PF 5.80); do not chase the extended market price.
2. **ONDO/USDT — best catalyst-backed, already running (crypto)** — tp2_hit, dual-basket; manage, do not add.
3. **AMD — best short-watch, sector-confirmed but gate-blocked (stocks)** — chip-sector weakness externally confirmed for a second day; the individual signal has not cleared the desk's own drawdown guard all session.
4. **UNH — best catalyst print, but AVOID/MANUAL REVIEW, reinforced (stocks)** — DOJ probe confirmed widened today; contradiction sharper than the last review.
5. **AAPL — pre-open long-watch, unconfirmed either way (stocks)** — never actually tested this session; the drawdown guard has blocked every cycle since the open, independent of price action.

No new, gate-cleared stocks entry has fired since the market opened 2h+ ago — this is a genuine session-wide observation (see TODO-1), not a one-name issue. Crypto has one near-trigger long (BANK) and two running positions (ONDO, XLM) to manage. This is a **manage-and-wait-for-the-gate window** for stocks, not a system pause — scanning, tracking, and monitors continue unchanged.

## 9. Avoid / No Trade (this decision window only)

- UNH — DOJ probe confirmed widened today, stacked with a moderating-but-still-large earnings-day gap (+3.48% intraday) — do-not-chase, reinforced from the last review.
- NFLX — reports after today's close, do-not-chase pre-print, no open signal, historically weak reaction to its last four reports.
- BANK/USDT — do not market-buy at the current extended price; only the printed 0.0561-0.0574 pullback zone is the plan.
- Any AAPL/JPM/XLE/XOM/LLY/AMD entry treating the pre-gate A-tier score as a live trigger — the drawdown/RR guards have held for the entire post-open session (6 consecutive cycles); overriding them manually is exactly the failure mode the gates exist to prevent.
- This is a no-new-entries read for the listed names/situations only; the scanner, monitors, and scheduler continue running unchanged in both asset classes.

## 10. Main Risks

- **The stocks-intraday drawdown guard has produced zero new actionable A/B for the entire post-open session so far (2h+, 6 consecutive cycles)**, despite multiple names scoring 83-100 pre-gate. This is either the gate working exactly as designed against a genuinely weak recent stocks track record (all-tier diagnostic PF 0.63, n=225 reliable) or an overly conservative gate suppressing real opportunity — the data alone cannot distinguish these from inside this review; flagged as TODO-1 for human judgment, not something this run can or should adjust.
- **UNH's legal risk is trending worse, not better** — a probe that widens on the same day as a strong earnings beat is a genuinely unusual and noteworthy combination; worth an explicit human look rather than assuming the situation will resolve favorably just because the print was good.
- **Genuinely active, externally-confirmed geopolitical escalation** continues (new strikes reported on Qeshm Island/Bandar Abbas/Chabahar); crypto has absorbed it so far but the risk has not diminished since the last review.
- **Semiconductor weakness is now a two-day pattern**, not a single-day reaction — a live headwind for any semis-adjacent long heading into the rest of the week.
- Catalyst mapping running at 80.1% unmapped today (direct count) — treat the catalyst layer as context only; persistent pattern, not new.
- Crypto scalp mode remains kill-switched off — unchanged.
- Stocks weekly A/B headline PF is 0.67 on a very weak n=14 sample — do not over-trust a fresh stocks A/B even if the guard eventually clears one this week.
- **New untracked legacy crypto alert** (ALLO/USDT swing, first non-zero reading in several reviews) — see TODO-3.
- Data-lifecycle observation carried forward: several stocks B-tier signals still show non-terminal statuses (tp1_hit/tp2_hit/triggered) past their expires_at, including some from weeks ago (SMH from 2026-06-05) and one from just two days ago (XOM, 2026-07-14) — see TODO-2 (open since the last review, unchanged).

## 11. Action Plan — next 4 hours

- **Priority 1**: watch for BANK/USDT to fill its 0.0561-0.0574 pullback zone (currently ~0.2 ATR away) — this is the desk's closest-to-live crypto idea on its strongest playbook.
- Manage the existing ONDO/USDT (tp2_hit) and XLM/USDT (tp2_hit) positions per their invalidation levels — no fresh entries needed on either.
- Continue watching whether the stocks-intraday drawdown guard clears on any name (AAPL, AMD, JPM, XLE, XOM, LLY all remain pre-gate A/B-scored) — if it does, that will be the session's first new stocks A/B and worth flagging explicitly next cycle.
- Flag UNH for an explicit human/manual review given the DOJ probe widening on an earnings-beat day — no automatic action either direction.
- No new NFLX exposure ahead of tonight's after-close print.
- Monitor the Iran/Bahrain/Kuwait situation for further escalation or de-escalation through the rest of the US session — still the dominant tail-risk driver of today's elevated crypto macro-risk score.
- Continue scanning/tracking as normal in both asset classes — no system changes; both pipelines are healthy.

## 12. Final Verdict per Mode

- Crypto scalp: kill-switched off (structurally negative PF 0.25 playbook, unchanged) — no ideas expected.
- Crypto intraday: BANK/USDT (waiting, near-trigger) and ONDO/USDT (tp2_hit, running) are the two live threads; no fresh A-tier this cycle.
- Crypto swing: fresh this cycle (14:27 UTC), regime read warmer (BTC+ETH both uptrend) than scalp/intraday; BANK/USDT swing is the standout idea on the desk's best-performing playbook, waiting for its pullback zone; XLM/USDT (tp2_hit) remains open and running.
- Stocks intraday: **zero A/B actionable for the entire post-open session so far** — AAPL (long-watch, unconfirmed) and AMD (short-watch, sector-confirmed but gate-blocked) are the two names to keep watching; UNH is a flagged, worsening contradiction, not actionable; no other name has cleared both the guard and the RR bar this session.
- Stocks swing/invest (legacy): deprecated, not used this run. `stocks_swing_growth_breakout` (new framework): shadow-only, unchanged, out of scope for actionability.

## 13. Sources

- [Stock market today: Dow rises, S&P 500 and Nasdaq fall as chip stocks slide amid AI jitters — Yahoo Finance](https://finance.yahoo.com/markets/live/stock-market-today-thursday-july-16-dow-sp-500-nasdaq-103116735.html) (2026-07-16)
- [Stock Market Today (July 16, 2026): Nasdaq slips as tech stocks lose momentum — TheStreet](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-july-16-2026) (2026-07-16)
- [Live Nasdaq Composite: Chip Stocks Buckle Under Capex Pressure as Markets Hunt Leadership — 24/7 Wall St.](https://247wallst.com/investing/2026/07/16/live-nasdaq-composite-chip-stocks-buckle-under-capex-pressure-as-markets-hunt-leadership/) (2026-07-16)
- [Bitcoin and ethereum prices today, Thursday, July 16, 2026 — Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-thursday-july-16-2026-prices-rise-ethereum-becomes-increasingly-compelling-124218108.html) (2026-07-16)
- [Iran war live: sirens in Bahrain, Kuwait; US disables Iranian oil tanker — Al Jazeera](https://www.aljazeera.com/news/liveblog/2026/7/16/iran-war-live-sirens-in-bahrain-kuwait-us-disables-iranian-oil-tanker) (2026-07-16)
- [UnitedHealth Group (UNH) Faces Wider DOJ Antitrust Probe As Claritev Review Expands — Yahoo Finance](https://finance.yahoo.com/healthcare/articles/unitedhealth-group-unh-faces-wider-221504204.html) (2026-07-16)
- [UnitedHealth (UNH) Faces Broader DOJ Antitrust Probe Into Claritev — Simply Wall St News](https://simplywall.st/stocks/us/healthcare/nyse-unh/unitedhealth-group/news/unitedhealth-unh-faces-broader-doj-antitrust-probe-into-clar) (2026-07-16)
- [UnitedHealth Group under DOJ investigation over Medicare billing practices — Medical Economics](https://www.medicaleconomics.com/view/unitedhealth-group-under-doj-investigation-over-medicare-billing-practices) (2026-07-16)
- Internal: `data/reports/scalp/2026-07-16_13-51_scalp_report.md`, `data/reports/intraday/2026-07-16_13-57_intraday_report.md`, `data/reports/swing/2026-07-16_14-27_swing_report.md`, `data/reports/stocks/intraday/2026-07-16_15-33_stocks_intraday_report.md` (+ six intermediate 10-min cycles 13:33-15:33 UTC), `data/catalysts/2026-07-16/*`, `data/scheduled_runs/2026-07-16_default_schedule/cycle_05_16-43_summary.md`, `reports/PAPER_MONITOR_STATUS_LATEST.md`.

## 14. Fix Requests / TODO

### TODO-1
- **issue:** The stocks-intraday `stocks_intraday_7d_drawdown_guard` / `stocks_intraday_long_guard` combination has blocked 100% of A/B-scored candidates across every single 10-minute cycle since the market open (13:33-15:33 UTC, 6+ consecutive cycles), including names scoring 83-100 pre-gate (AAPL, JPM, XLE, XOM, LLY).
- **evidence:** `data/reports/stocks/intraday/2026-07-16_{13-33,13-44,13-54,14-10,14-16,14-26,14-31,14-41,14-51,15-02,15-13,15-23,15-33}_stocks_intraday_report.md` — every single "## 6. A/B Actionable Candidates" section reads "No A/B-tier actionable setups in this run."; §10 of the report shows "actionable A/B (intraday) after gates: 0" every cycle.
- **suggested manual fix:** Have a human review whether the 7-day rolling drawdown guard threshold is calibrated correctly given the current stocks all-tier diagnostic (PF 0.63, n=225 reliable) — i.e., confirm this is the gate working as intended against a genuinely weak track record, not an over-tight threshold suppressing every opportunity regardless of individual setup quality. This is a judgment call outside this run's read-only scope.
- **priority:** medium
- **first observed:** 2026-07-16 18:39 EEST review (the pattern itself may be older; this is the first review to characterize it across a full multi-cycle post-open window)

### TODO-2 (carried forward, unchanged)
- **issue:** Several stocks B-tier signals in `active-signals` show `expires_at` timestamps in the past (ranging from 2 days ago to 6+ weeks ago) while still displaying non-terminal statuses (`tp1_hit`, `tp2_hit`, `triggered`) rather than a closed/expired terminal state.
- **evidence:** `python -m src.cli active-signals --asset-class stocks --tier B` — e.g. `sig_9160e6296262557b` XOM expires 2026-07-14T14:23:20 still `tp2_hit`; `sig_1bc6d2076b02bd2b` SMH expires 2026-06-05T10:59:41 still `tp1_hit`; `sig_20c7c47312a9c1ee` UNH expires 2026-06-11T14:55:38 still `tp1_hit`.
- **suggested manual fix:** unchanged from the 16:20 EEST review — have a human check whether the lifecycle/track-signals job is correctly terminalizing stocks B-tier signals past their `expires_at`.
- **priority:** medium
- **first observed:** 2026-07-16 16:20 EEST review (still open)

### TODO-3
- **issue:** `detect_untracked_legacy_alerts` returned 1 result this run (ALLO/USDT swing B, 65.4, sent 2026-07-16T14:27:05 UTC) after several consecutive clean (0) readings across recent reviews.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-16` output this run vs. 0 at 16:20 EEST and in prior reviews.
- **suggested manual fix:** Have a human check whether this is a one-off (e.g., a timing race between the watchlist-alert send and proposed_signal creation) or the start of a recurrence of the earlier-resolved untracked-alert issue. A single occurrence is not yet a pattern; worth a quick look but not urgent.
- **priority:** low
- **first observed:** 2026-07-16 18:39 EEST review
