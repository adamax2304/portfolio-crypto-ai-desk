# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:40 EEST

## 1. Executive Summary

Slot: **Europe / pre-US context (11:30 EEST)**. Advisory only / no auto-trade — this review never places orders, changes scoring, or touches live execution.

Crypto stays risk-off across scalp/intraday/swing (BTC downtrend, ETH transition_down, altcoin breadth 13–16% above EMA20) with **zero new A/B triggers this cycle** — the desk is purely managing 19 already-open crypto positions plus one waiting-for-entry short (ADA/USDT). DEXE/USDT (flagged "elevated caution — squeeze risk" in the 04:45 review) was **stopped out** overnight, confirming that caution was warranted. Stocks are **closed / pre-market** — all raw A-tier stock setups (XLE, NVDA, AMZN, UNH, GOOGL, AMD, SMH, XLK, QQQ, AVGO short) are correctly demoted to C/watchlist by the market-closed gate; treat them as **US-open planning only**, not confirmed trades. A genuine, externally-**confirmed** macro catalyst landed overnight: the KOSPI/Asia chip-stock crash (SK Hynix ‑11%, Samsung ‑9.5%) directly supports the model's own semis/AI-hardware short basket (NVDA/AMD/SMH/XLK). UNH's DOJ investigation is externally **confirmed** (standing avoid); AMZN's `going_concern` gate tag is **not** corroborated externally (only investor cash-flow worry, no auditor/regulator going-concern designation found) — carried forward as an open TODO, now with an external check attached. Crypto scalp mode remains deliberately disabled via kill-switch (0W/9L, PF 0.11 this week) — working as designed, not a new issue.

## 2. Data Used

- Reports: scalp (09:24), intraday (09:31), swing (04:25, carry-forward), stocks intraday (09:49). Stocks swing/invest are stale since 2026-07-02 and remain excluded (known deprecated framework, see project memory).
- Catalyst layer: `data/catalysts/2026-07-28/catalyst_events.jsonl` (1,500 events), `narrative_baskets.jsonl` (3 baskets).
- LLM packets: `llm_analysis_packet.md` (09:32), `llm_stocks_packet.md` (09:50).
- CLI: `active-signals` (crypto n=19, stocks n=50), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts --since 2026-07-28` (0 hits).
- `news_items` / `proposed_signals` SQLite read queries (db/crypto_ai_desk.sqlite) for ADA, XLE, COTI, DEXE symbol history.
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-28_0445.md`.
- External web research: 3 WebSearch queries (UNH DOJ, AMZN going-concern, KOSPI chip selloff) — all with source lists attached (§13). **External web research available and used this run.**

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime 09:59 EEST, current time ~11:40 EEST → **~1h41m old, fresh** (well under the 3h defer threshold).
- Latest cycle: `cycle_06_09-15_summary.md` (09:59).
- Swing report: 7h15m old → **carry-forward** band (4–12h), used with that label.
- Stocks swing/invest: last dated 2026-07-02 → **stale/deprecated**, excluded per standing project decision (framework removed, replaced by shadow-only `stocks_swing_growth_breakout`).
- Stocks monitor last log activity: 09:16 EEST (fresh). Pending-monitor: leader lock held by an active process (`pending-monitor: leader_active`) — normal single-leader behavior, not a fault.
- Catalyst folder present for today (no need to run the fallback scan CLI).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-07-28 11:40 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh"], "data_missing": ["stocks swing/invest reports (deprecated, no fresh source)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log 09:59 EEST", "intraday/scalp/stocks-intraday reports <2.5h old", "swing report 7h15m = carry-forward"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["risk_off", "shorts_preferred", "mixed"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC downtrend, ETH transition_down, altcoin breadth 13-16% above EMA20", "stocks VIX 18.67, 0/4 indices trending up, energy/financials strong vs semis/tech weak", "KOSPI -8/-11% chip selloff confirmed externally"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["mapping_weak", "no_catalyst", "fresh_catalyst", "narrative_supported"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["61% of today's 1500 catalyst events unmapped (no symbol)", "momentum_breakout basket (COTI/ZAMA/REZ) has no news backing = avoid_chase", "KOSPI/Asia chip crash externally confirmed via Bloomberg/WaPo/AP, supports semis short thesis"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "data_unavailable"], "data_missing": ["OI 24h for several crypto symbols (n/a via mexc fallback)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ADA/USDT: price down + OI up (fresh shorts pressing), possible squeeze if price reclaims; funding -0.00026, OI +2.75%"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["chase_risk", "overextended", "entry_late"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["COTI/ZAMA/REZ +13-77% 24h extensions, no catalyst", "ADA already -5.84%/-11.23% (7d) before any new short entry", "no new A/B triggers in scalp/intraday/swing this cycle"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.85,
      "reason_codes": ["waiting_for_entry", "closed_flat", "review_shadow", "no_entry"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["19 open crypto positions (mostly tp1_hit/tp2_hit, manage-only)", "ADA/USDT B-tier short = WAITING for entry, not yet filled", "DEXE/USDT stopped (CLOSED LOSS) 2026-07-28T03:21:44Z, confirming prior squeeze-risk caution", "stocks: 0 A/B open this week, 50 C-tier watchlist rows, most with expires_at in the past (management/history, not fresh)"] },
    { "agent": "risk_manager", "verdict": "manual_review", "confidence": 0.75,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review", "repeated_losses"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: DOJ criminal/antitrust probe into Medicare Advantage billing + Optum, externally confirmed via Yahoo Finance/Simply Wall St/FierceHealthcare", "AMZN: going_concern tag NOT corroborated externally — only investor cash-flow/capex worry found, no auditor/regulator designation", "GOOGL: securities-fraud investigation, confirmed unchanged since prior review", "crypto scalp: 0W/9L, PF 0.11 this week — kill-switch already disabled (working as designed)"] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": ["stocks A/B this week (sample=0, anecdotal)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto B-tier week: winrate 24.8%, PF 1.94, totalR +31.1", "crypto swing PF 3.43/totalR +26.7 (best), intraday PF 1.95, scalp PF 0.11/totalR -8.0 (0W/9L, disabled)", "stocks C-tier week: winrate 2.8%, PF 0.57, totalR -3.0 (watchlist only, not actionable)"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.72,
    "preferred_side": "shorts",
    "best_long_candidate": { "symbol": "COTI/USDT", "trigger": "wait for a confirmed pullback/retest of the breakout zone with volume — do not chase the +65-77% 24h extension; no catalyst backing found, basket playbook is explicitly avoid_chase" },
    "best_short_candidate": { "symbol": "ADA/USDT", "trigger": "existing B-tier short is WAITING for entry at 0.156609-0.157303, invalidation 0.158151 — let it fill on its own terms; do not chase the already -5.84%/-11.23% move, and watch for a squeeze if price reclaims (fresh shorts + rising OI)" },
    "best_catalyst_candidate": { "symbol": "SMH / NVDA / AMD (semis basket, short)", "trigger": "KOSPI -8/-11% chip-sector crash confirmed (SK Hynix -11%, Samsung -9.5%, AI-bubble + China chipmaker breakthrough fears) — wait for RTH confirmation at the US open, do not chase the pre-market gap; SMH already tagged weakest sector (RS -11.7% vs SPY)" },
    "avoid_candidate": { "symbol": "UNH", "reason": "confirmed DOJ criminal/antitrust investigation (Medicare Advantage billing, Optum) — multiple corroborating sources; standing legal-risk demotion" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh | advisory_only |
| market_regime | caution | 0.75 | risk_off, shorts_preferred, mixed | advisory_only |
| catalyst_narrative | caution | 0.70 | mapping_weak, no_catalyst, fresh_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.70 | chase_risk, overextended, entry_late | advisory_only |
| execution_lifecycle | needs_review | 0.85 | waiting_for_entry, closed_flat, review_shadow, no_entry | advisory_only |
| risk_manager | manual_review | 0.75 | legal_risk, headline_risk, manual_review, repeated_losses | advisory_only |
| playbook_performance | ok | 0.80 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution (synthesis) | 0.72 | — | advisory_only |

## 4. What Changed vs Previous Review (04:45 EEST)

- **DEXE/USDT: stopped out** (2026-07-28T03:21:44Z) — the 04:45 review's "manage with elevated caution — squeeze-risk contradiction" call was validated; this is now a **CLOSED LOSS**, no longer an open position.
- **ZAMA/USDT swing** (flagged "new, no independent deep dive yet" last cycle) has since gone to `tp1_hit` — now manage-only toward TP2/TP3.
- **AMZN going_concern**: still open, still unresolved 7+ hours later (first observed 04:01 EEST). This run added an **external check**: no auditor/regulator "going concern" designation found — only general investor worry over AMZN's cash-flow/capex profile. Raises, rather than resolves, suspicion of tag misclassification (see §14).
- **UNH** newly carries a `legal_headline_risk: sec_doj` gate this cycle (not present in the 04:45 review) — this run externally **confirmed** it's a real, actively-reported DOJ probe, not a stale/misfired tag.
- **New macro catalyst since last review**: KOSPI/Asia chip-stock crash (confirmed externally), directly reinforcing the stocks model's own semis/AI-hardware short cluster.
- No new A/B-tier crypto signals fired in any of the three cycles since 04:45 (scalp/intraday/swing all show "No A-tier setups found" / "No B-tier setups found" this cycle).
- GOOGL: unchanged, still a confirmed avoid (securities-fraud investigation).

## 5. Catalyst Coverage

- Total catalyst events today: **1,500**. Mapped (symbol present): **583** (38.9%). Unmapped: **917** (61.1%).
- Narrative baskets: **3** (`perps_dex_narrative`/HYPE, `rwa_narrative`/ONDO+XLM, `momentum_breakout`/COTI+ZAMA+REZ).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (sample):
  1. "$250,000,000 USDC minted at USDC Treasury" (exchange-flow noise, no symbol resolver hit)
  2. "Bitget Announcement: AEONUSDT now launched for futures trading and trading bots" (exchange-listing noise, ticker not in resolver map)
  3. "POSCO International testing onchain trade receivables with LG CNS" (real story, no crypto-native symbol to map to)

This matches the already-tracked, known-weak catalyst-resolver issue (see project memory on catalyst linkage); not a new regression.

## 6. Market Landscape

Crypto: BTC in a confirmed downtrend, ETH transition_down, altcoin breadth only 13.6–16.3% above EMA20 across scalp/intraday/swing scans — consistently "short bias or no trade; avoid weak altcoin longs" per the model's own regime read. Fear & Greed at 30 (Fear) per the latest Telegram channel snapshot (BTC ~$65.4k +1.55%, ETH ~$1,967 +4.46% on the day, so there is a same-day bounce inside the larger downtrend — treat as relief, not reversal, until EMA structure changes). A handful of RS leaders (COTI, TAO, ZAMA) are pumping without catalyst backing — high chase risk.

Stocks: cash market closed (pre-market). VIX 18.67, breadth thin (25% above EMA20), 0/4 major indices in a confirmed uptrend. Sector rotation is genuinely split: energy (XLE +8.4% 20d, RS +7.0%) and financials (XLF +6.2% 20d, RS +4.8%) are the strongest sectors, while semiconductors (SMH ‑10.3% 20d, RS ‑11.7%) and technology (XLK) are the weakest — and that weakness now has a fresh, externally-confirmed macro trigger (KOSPI chip-stock crash). The model's own top-candidates table (raw A-tier) is short-heavy in exactly the weak sectors (NVDA, AMZN, GOOGL, AMD, SMH, XLK, QQQ, AVGO) plus, notably, **XLE short** — which is a genuine contradiction against the strong-sector read (see §7 deep dive).

### Market Mood / Risk Routing

- Crypto mood: **risk-off** (downtrend, weak breadth, same-day bounce only)
- Stocks mood: **pre-market / mixed** (closed; energy/financials strong, semis/tech weak — sector divergence, not a single verdict)
- Dominant narrative: overnight Asia AI-chip selloff (KOSPI, confirmed) bleeding into US semis/tech short thesis; crypto momentum names (COTI/ZAMA/TAO) pumping without catalyst support
- Preferred side now: **shorts** — crypto (short bias regime) and stocks (semis/tech, catalyst-reinforced) both lean short; exception is catalyst-backed RS-leader longs on confirmed pullback only
- Best long candidate: COTI/USDT (watch-only, needs pullback confirmation — see §8)
- Best short candidate: ADA/USDT (crypto, live waiting_for_entry signal) / SMH-NVDA-AMD (stocks, pre-US watchlist)
- What to avoid: UNH (confirmed legal risk), GOOGL (confirmed legal risk), chasing COTI/ZAMA/REZ, chasing ADA short below current waiting-for-entry zone
- What would change the view: crypto — BTC reclaiming EMA20/EMA50 with breadth expansion; stocks — a clean RTH confirmation candle at/after the US open, or a de-escalation of the Asia chip-selloff narrative

## 7. Candidate Deep Dives

### 1. ADA/USDT — short, B-tier, WAITING for entry (crypto, live/actionable class)

- Signal `sig_9c26161be680e6a4`: entry 0.156609–0.157303, invalidation 0.158151, expires 2026-07-29T06:37:34Z.
- Has price already reacted? Yes — ADA is already down ‑5.84% (24h) / ‑11.23% (7d), RS vs BTC ‑2.89%. Entering fresh here would be **chasing an already-extended move**, not a fresh breakdown.
- Chase risk: **yes** if forced; the signal itself is correctly sitting in `waiting_for_entry` rather than market-ordering in.
- Squeeze risk (derivatives_squeeze agent): price down + OI up (+2.75%) = fresh shorts pressing into the move; report explicitly flags "possible squeeze if price reclaims." Funding -0.00026 (mildly negative, consistent with short-side crowding, not yet extreme).
- Catalyst support: none found — Hoskinson "best days are ahead" quote (2026-07-28 02:41 UTC, BeInCrypto) is bullish-framed but did not move price; no bearish catalyst either. This is a pure technical/momentum short.
- Actionable now or after confirmation? Let the existing limit-style entry fill on its own terms (0.1566–0.1573); do not chase below that zone.
- Invalidates on: reclaim above 0.158151 (also the squeeze trigger level).
- Aligned with mood: yes (risk-off, short-bias regime), but the "no-catalyst intraday in chop" playbook note on this exact symbol/mode carries a documented 14-day track record of WR 23% / PF 0.70 / ‑3R — treat as **watch, not high-conviction**.

### 2. COTI/USDT — long-watch, no active signal (crypto)

- Strongest RS symbol across both intraday (score 91.6, 24h +77.5%, RS +80.4%) and swing (score 91.6, 24h +65.1%, RS +68.1%) scans, two cycles running.
- No news coverage found in the last 48h (`news_items` query empty) — this is a pure technical/momentum extension, not catalyst-driven.
- Basket: `momentum_breakout` (COTI/ZAMA/REZ), playbook explicitly **`avoid_chase`**, freshness <1h.
- Is this chasing? Yes, at current price. Would entry now be late? Yes.
- Actionable only after a confirmed pullback/retest with volume defense — no specific level published this cycle (no active signal exists yet); treat as a watchlist name, not a trigger.
- Invalidates the long-watch thesis: momentum fails to hold any retest and rolls over into the broader BTC downtrend.

### 3. Semis/AI-hardware short basket — NVDA, AMD, SMH, XLK, QQQ (stocks, pre-US planning only)

- All raw A-tier scores (81–93) demoted to C by `market_closed_intraday_planning_only` — **not actionable pre-open**, planning levels only.
- Catalyst confirmed externally this run: KOSPI ‑8/‑11% (SK Hynix ‑11.0%, Samsung ‑9.45%), Nikkei ‑3.9%, driven by AI-bubble fears + reports of a Chinese chipmaker (Shanghai Yuliangsheng) breakthrough in tech long dominated by ASML, plus Nvidia competitive-supply-deal concerns (Bloomberg, Washington Post, AP via clickondetroit/clickorlando, USNews — see §13).
- This directly reinforces the model's own sector-rotation read: semiconductors already the weakest US sector (RS ‑11.7% vs SPY, 20d ‑10.3%), technology second-weakest.
- Has price already reacted (US names)? Not yet at the cash-market level — Asia sold off overnight, US is still pre-market. This is a **pre-open thesis**, genuinely fresh, not a chase yet.
- Actionable trigger: RTH confirmation — a clean break/continuation below pre-market lows in the first 15–30 minutes of the US cash session, not a blind pre-market short. AVGO also carries a small existing risk-penalty (‑4.0) worth re-checking at the open.
- Legal/headline overlay: NVDA also carries an `exploit_hack` risk-only warning (Hugging Face-linked industry security alliance news) — advisory only, does not itself block the setup.
- Would invalidate: a sharp Asia/US risk reversal (chip stocks bounce hard at the US open) or confirmation the "China chipmaker breakthrough" report is overstated.

### 4. UNH — short, was A-tier (stocks, AVOID / manual review)

- Demoted A→C for `legal_headline_risk: sec_doj`, plus the standard `market_closed_intraday_planning_only` gate.
- External verification (WebSearch + WebFetch, this run): **confirmed genuine and active.** WebFetch on the Yahoo Finance article confirms the underlying Medicare-billing DOJ probe was first disclosed 2025-07-23 (stock -4.7% on disclosure) and has since **expanded** per the more recent 2026 reporting to a wider antitrust probe covering Optum/Claritev. Multiple independent outlets (Yahoo Finance, Simply Wall St, Medical Economics, FierceHealthcare) corroborate — this is a long-running, escalating legal matter, not a stale or one-off item.
- Verdict: **AVOID** as a clean actionable — legal/headline risk overwhelms the technical short thesis; if traded at all, this belongs to a discretionary/event-risk desk, not the systematic pipeline.
- Also carries an `earnings today (2026-07-28)` do-not-chase warning independent of the legal risk — double reason to stay out today specifically.

### 5. AMZN — short, was A-tier (stocks, contradiction / manual review)

- Demoted A→C for `legal_headline_risk: going_concern`, first observed 04:01 EEST, still present unchanged in the 09:49 EEST report (7h45m stale on this specific tag with no update).
- External verification (WebSearch, this run): **not corroborated.** No reporting found of an actual auditor/regulator "going concern" designation for Amazon. What does exist: real investor worry over ~$200B 2026 capex, TTM free cash flow down ~95% to $1.2B, long-term debt up to $119.1B from $65.6B, and a ~4.5% pre-earnings stock pullback (FXLeaders, Benzinga, TIKR — see §13) ahead of the 2026-07-30 earnings print.
- This is a genuine **contradiction**: the internal tag name ("going_concern") implies a formal, severe designation, but the external evidence only supports "elevated cash-flow/capex investor anxiety," a materially different and less severe classification.
- Verdict: **manual review required**, not a confirmed avoid — likely tag over-classification, but cannot rule out the tag is drawing on a source this review didn't surface. Do not treat AMZN as "confirmed avoid" the way UNH/GOOGL are. See TODO update in §14.

## 8. Best Candidates Ranked

1. **Best short-watch (crypto, live): ADA/USDT** — let the existing waiting_for_entry short fill at 0.1566–0.1573; do not chase; squeeze risk above 0.1582.
2. **Best catalyst-backed short-watch (stocks, pre-US): SMH / NVDA / AMD** — KOSPI chip-crash confirmed; wait for RTH confirmation at the US open, do not chase the pre-market gap.
3. **Best long-watch (crypto): COTI/USDT** — no catalyst, momentum-only; wait for a confirmed pullback/retest with volume before considering a long.
4. **Manage-only (crypto, already open): ZAMA/USDT (swing tp1_hit + multiple fills), AKE/USDT x2 (tp1_hit), ONDO/OPN/FIL/KITE/VIRTUAL/PENGU/PUMP/KAITO/ALLO/NEAR** — 18 open crypto positions total, hold toward existing TP/SL, no new entries.
5. **Manual review, not tradeable: AMZN** — going_concern tag unresolved and now externally doubted; needs a human to confirm the source event.
6. **Avoid (confirmed, current window): UNH, GOOGL** — both carry externally-confirmed legal/regulatory risk; excluded from actionable consideration today.

## 9. Avoid / No Trade

This applies to the **current decision window only** — scanning, tracking, and monitors continue regardless.

- **UNH**: confirmed active DOJ investigation (antitrust + Medicare billing).
- **GOOGL**: confirmed active securities-fraud investigation, unchanged since prior review.
- **Chasing COTI/ZAMA/REZ** at current extended prices — no catalyst, momentum-only, avoid_chase playbook.
- **Chasing ADA short** below the published waiting-for-entry zone (0.1566–0.1573) — already an extended move.
- **Pre-market stock shorts (NVDA/AMD/SMH/XLK/QQQ/AVGO/XLE)** as live entries right now — market is closed; these are RTH-confirmation-only ideas until the US cash session opens.

## 10. Main Risks

- AMZN earnings 2026-07-30 (2 trading days out) — heavy pre-earnings positioning risk on a name whose gate tag is itself in question.
- MSFT/META earnings tomorrow (2026-07-29), UNH/V earnings today — do-not-chase warnings active on all four independent of any legal-risk flags.
- Asia chip-selloff could either extend into a broader US risk-off gap at the open, or mean-revert sharply (chip stocks are already down double digits in Asia — a relief bounce at the US open is plausible and would invalidate the short-basket thesis fast).
- Crypto same-day BTC/ETH bounce (+1.55%/+4.46%) inside a still-confirmed downtrend — risk of a short-lived short squeeze on the crowded ADA-style setups if BTC extends the bounce.
- Catalyst-mapping coverage weak (61% unmapped) this run — treat the news layer as context, not confirmation, across all candidates.

## 11. Action Plan — next 4 hours

- Crypto: no new entries; manage the 19 open positions to TP/SL; let ADA/USDT short fill passively at its published zone; do not chase COTI/ZAMA/TAO longs without a pullback.
- Stocks: build/refresh the US-open watchlist around the semis/AI-hardware short basket (NVDA/AMD/SMH/XLK/QQQ) using the KOSPI catalyst as context; wait for RTH confirmation before treating any as actionable; keep UNH and GOOGL off the actionable list entirely; flag AMZN for manual review before it can re-enter actionable consideration.
- Watch for the 16:20 EEST pre-US-open decision review to reassess gap risk and confirm/kill the semis short thesis with fresh pre-market data.

## 12. Final Verdict per Mode

- **Crypto scalp:** No trade — kill-switch deliberately disabled (working as designed), 0W/9L, PF 0.11, totalR ‑8.0 this week.
- **Crypto intraday:** Watchlist only — no A/B this cycle; ADA/USDT (short, waiting_for_entry) is the one live actionable item, managed passively.
- **Crypto swing:** Manage the open book (ZAMA tp1_hit, AKE x2 tp1_hit, PUMP tp1_hit, plus older fills); DEXE closed via stop overnight; no new adds this window.
- **Stocks intraday:** No trade — market closed, zero A/B actionable; semis/AI-hardware short basket is the pre-US watchlist idea pending RTH confirmation; UNH and GOOGL confirmed-avoid; AMZN pending manual review.
- **Stocks swing/invest:** Deprecated/stale (last report 2026-07-02) — not evaluated, consistent with the standing project decision to run only the shadow-only replacement framework.

## 13. Sources

- [UnitedHealth Group (UNH) Faces Wider DOJ Antitrust Probe As Claritev Review Expands (Yahoo Finance)](https://finance.yahoo.com/healthcare/articles/unitedhealth-group-unh-faces-wider-221504204.html)
- [UnitedHealth (UNH) Faces Broader DOJ Antitrust Probe Into Claritev (Simply Wall St)](https://simplywall.st/stocks/us/healthcare/nyse-unh/unitedhealth-group/news/unitedhealth-unh-faces-broader-doj-antitrust-probe-into-clar/amp)
- [UnitedHealth Group under DOJ investigation over Medicare billing practices (Medical Economics)](https://www.medicaleconomics.com/view/unitedhealth-group-under-doj-investigation-over-medicare-billing-practices)
- [UnitedHealth stock sinks 4.7% after company confirms DOJ investigation into Medicare billing practices (Yahoo Finance)](https://finance.yahoo.com/news/unitedhealth-stock-sinks-47-after-company-confirms-doj-investigation-into-medicare-billing-practices-133527260.html)
- [DOJ's criminal probe into UnitedHealth extends to Optum Rx, physician reimbursement (FierceHealthcare)](https://www.fiercehealthcare.com/payers/wsj-report-doj-interviewing-former-employees-about-medicare-billing-practices-unitedhealth)
- [Amazon Stock AMZN Tests Support as Competition and $59B Capex Raises Cash Flow Concerns (FX Leaders, 2026-07-23)](https://www.fxleaders.com/news/2026/07/23/amazon-stock-amzn-tests-support-as-competition-and-59b-capex-raises-cash-flow-concerns/)
- [What's Going on With Amazon Stock Wednesday? (Benzinga)](https://www.benzinga.com/analyst-stock-ratings/reiteration/26/07/60616005/amazons-aws-growth-could-top-expectations-analyst-says)
- [Amazon Has Fallen 13% From Its High. Is 2026 the Turning Point? (TIKR.com)](https://www.tikr.com/blog/amazon-has-fallen-13-from-its-high-is-2026-the-turning-point)
- [KOSPI Crashes 8% as AI Chip Selloff Slams Asian Markets (BeInCrypto)](https://beincrypto.com/kospi-crash-ai-chip-selloff/)
- [Japanese, Korean Stocks Tumble as Chip Selloff Intensifies (Bloomberg, 2026-07-28)](https://www.bloomberg.com/news/articles/2026-07-28/japanese-korean-stocks-tumble-as-chip-selloff-intensifies)
- [Asian shares slip and South Korea's Kospi index sinks nearly 11% on heavy selling of chipmakers (Washington Post, 2026-07-28)](https://www.washingtonpost.com/business/2026/07/28/stock-markets-ai-chips-oil/3e8f2910-8a3a-11f1-8912-d71e69d679d7_story.html)
- Internal: `data/reports/intraday/2026-07-28_06-31_intraday_report.md`, `data/reports/swing/2026-07-28_01-25_swing_report.md`, `data/reports/scalp/2026-07-28_06-24_scalp_report.md`, `data/reports/stocks/intraday/2026-07-28_06-49_stocks_intraday_report.md` (all 2026-07-28).
- Internal: `news_items` (BeInCrypto, "Cardano's Hoskinson Says 'Best Days Are Ahead': ADA Price Down 95% From Top", 2026-07-28T02:41:55Z).

## 14. Fix Requests / TODO

### TODO-amzn-going-concern-unverified (carried forward, updated)
- **issue:** AMZN's `legal_headline_risk: going_concern` gate tag, first observed 2026-07-28 04:01 EEST, remains unresolved 7h45m later with no source event surfaced internally. This run's external WebSearch check found no reporting of an official auditor/regulator "going concern" designation for Amazon — only general investor anxiety over capex/cash-flow (TTM FCF down ~95%, LT debt up to $119.1B) ahead of the 2026-07-30 earnings print.
- **evidence:** `data/reports/stocks/intraday/2026-07-28_06-49_stocks_intraday_report.md` §5/§7 (AMZN demoted A→C, `legal_headline_risk: going_concern`); external search (FXLeaders 2026-07-23, TIKR, Benzinga) shows cash-flow worry, not a formal going-concern designation.
- **suggested manual fix:** A human-driven session should trace the exact internal event/source that fired the `going_concern` tag (likely a news/legal-risk classifier hit misreading a cash-flow-concern article as a formal going-concern event) and either confirm it against a primary source (10-Q auditor language, SEC filing) or correct the classifier. Until then, treat AMZN as "manual review" rather than "confirmed avoid" like UNH/GOOGL.
- **priority:** medium (raised from the 04:45 review given the external check now actively contradicts the tag's apparent severity)
- **first observed:** 2026-07-28 04:01 EEST (this run: re-confirmed stale + externally checked at 11:40 EEST)

### TODO-catalyst-mapping-weak-recurring
- **issue:** Catalyst symbol-resolver mapping was 61.1% unmapped today (917/1500 events), consistent with the already-tracked weak-mapping issue.
- **evidence:** `data/catalysts/2026-07-28/catalyst_events.jsonl` — mapped=583, unmapped=917 (this run's count).
- **suggested manual fix:** No new action needed beyond what's already tracked in the project's catalyst-linkage backlog (symbol resolver widening); flagging only to keep the diff-vs-prior-review trail intact per §14 policy.
- **priority:** low (known, already deferred with prior sign-off — not a new regression)
- **first observed:** pre-existing, re-observed 2026-07-28 11:40 EEST

_No system-integrity issues this run — `detect_untracked_legacy_alerts` returned 0 hits, scheduler/report freshness both cleared, no new catalyst-ingest failures._
