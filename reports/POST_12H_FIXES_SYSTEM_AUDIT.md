# Post-12H Fixes System Audit

**Date:** 2026-06-04 ~13:30 EEST · **Window:** last ~14h · **Mode:** READ-ONLY
(no code/scoring/threshold/agent/data changes; scheduler not restarted — alive).

## 1. Executive Summary
- **System health: GREEN.** Scheduler + Telegram collector + crypto/stocks
  monitors all Running; cycles ran ~every 2h; **1 non-fatal failure** in 12h
  (crypto swing report exit=1, recurring); no tracebacks / DLL / SQLite-lock /
  stale-cycle issues. Telegram delivering (3 transient ReadTimeouts only).
- **Fixes work mechanically (live-verified):** funnel widened, RS-leader longs
  fire and win (ZRO/XPL/C/EPIC), shorts fire and register, **0 untracked legacy
  alerts**, SMCI demoted to C with legal flag, ETF earnings = N/A, A/B-only
  headline reporting live, catalyst importance non-zero & ranked.
- **Best signals:** crypto **ZRO +2R, XPL +2R** (RS-leader scalps); stocks
  **XLK/QQQ/AVGO +1R** B-tier.
- **Worst signals:** stocks overnight cluster (NVDA/SMCI/AMD/SMH/AAPL all −1R,
  MFE≈0) + **AVGO stale A-tier long**; crypto late shorts (BCH/OPG/DEXE −1R).
- **Main issue:** **stale / market-closed stock signal generation** — intraday
  stock setups issued on after-hours prices, and **AVGO re-issued A-tier LONG at
  a pre-earnings entry ~13% above market with `earnings: UNKNOWN`** (Opus-caught,
  4 reviews running). Secondary: **A-tier underperforms B** (PF ~0.2 vs ~1.4).
- **Next action:** treat as **NEEDS_SIGNAL_LOGIC_FIX** — but **implement nothing
  yet**; P0/P1 TODOs below with evidence.

## 2. Health and Infrastructure
| Component | Status | Evidence | Issues |
|---|---|---|---|
| Default scheduler | ✅ Running | PID 10068 (boot 20:50); cycles 2h apart through 12:32 | none |
| Telegram collector | ✅ Running | PID 26656 | none |
| Crypto/Stocks monitors | ✅ Running | PID 17232/3300 (12:31 cycle) | none |
| Cycles | ✅ on cadence | CYCLE …END ok=16 every ~2h, `telegram=sent` | 1× swing exit=1 (recurring) |
| Errors/Tracebacks/DLL/Locks | ✅ none | log scan clean | — |
| Telegram delivery | ✅ mostly | 3× `failed:ReadTimeout` (transient) | minor |
| Untracked legacy alerts | ✅ none | detector: "None" | — |

## 3. Fix Verification Matrix
| Fix | Live status | Evidence |
|---|---|---|
| Crypto funnel widened | ✅ | scalp deep=48 (40+8 short reserve), ohlcv 192 |
| RS-leader longs | ✅ win | ZRO +2, XPL +2, C +1, EPIC +1 registered+alerted |
| Short side | ✅ fire | SAHARA/BCH/OPG/DEXE/GPS/ETH registered+alerted (perf weak) |
| Alert registration | ✅ | 0 untracked legacy alerts (detector) |
| SMCI legal gate | ✅ | latest SMCI = C-tier + ACTIVE LEGAL HEADLINE RISK flag |
| ETF earnings | ✅ | "earnings: N/A (ETF — does not report earnings)" |
| Stocks symbol mapping | ✅ partial | Broadcom→AVGO, Apple/Nvidia/AMD map; 24% catalyst coverage |
| A/B-only headline | ✅ | signal-stats shows A/B headline + C separate + diagnostic |
| Catalyst importance | ✅ | 1424 events, all non-zero (avg 0.44), top-ranked sensibly |

## 4. Opus Auto-Review Quality
Ran ~every 4h, used WebSearch+WebFetch with cited URLs, compared prior review,
no fabricated charts, market-closed aware, handled SMCI/legal. **Added real
value**: caught the AVGO stale-A-tier bug and the A-tier-losing-bucket
regression. See `OPUS_AUTO_REVIEW_12H_AUDIT.md`.

## 5. News / Catalyst / Narrative Quality
news_items 1,101/14h (crypto 499 / stocks 602); catalyst_events 1,424 (all
non-zero importance); top narratives caught (BTC Treasury reserve, AVGO AI,
risk-off). **Weak spot: 24% symbol mapping.** See `CATALYST_NARRATIVE_12H_AUDIT.md`.

## 6. Crypto Signal Outcomes
26 B-tier setups; wins ZRO×2/XPL/C/EPIC, ~10 stops, ~5 flat-expired.
Net A/B ≈ +4R PF 1.25 (week). Losses = chop/danger whipsaw + late shorts.
Detail: `CRYPTO_12H_SIGNAL_OUTCOME_AUDIT.md`.

## 7. Stocks Signal Outcomes
39 A/B; net A/B +16R PF 1.30 (week, softened from 1.96 by overnight stops).
SMCI blocked ✅, ETF earnings N/A ✅, A<B confirmed. AVGO stale A-tier = defect.
Detail: `STOCKS_12H_SIGNAL_OUTCOME_AUDIT.md`.

## 8. Performance by Asset / Mode / Tier
**Crypto (week, A/B headline):** n=45, PF **1.25**, avgR +0.10, totalR **+4**,
winrate 27.5%, confidence *stronger*. C-tier n=0. All B-tier; long net positive
(ZRO/XPL/C/EPIC), short net negative (0W this window). *Reliable-ish; small.*

**Stocks (week, A/B headline):** n=294, PF **1.30**, avgR +0.074, totalR **+16**,
winrate 20%, confidence *reliable*. C-tier n=138, PF 1.15, +4R (separate).
Tier split: **A PF ~0.2–0.29 (−5R)** | **B PF ~1.4–2.2 (+33→+56R)** |
C PF 0.93–1.15. intraday carries volume; swing/invest mostly flat-expired/open.
ETF vs single-name: single-name carries the edge.

**Reliability notes:** crypto small (n=45) → directional; stocks A/B reliable
(n=294). All figures here are **deduped unique setups (latest outcome)** — raw
`signal_outcomes` rows are inflated by repeated tracker checks and were NOT used.

## 9. Root Causes of Losses
1. **Stale / market-closed stock signals (dominant stocks loss):** intraday
   stock setups generated overnight on after-hours prices; stops hit at next
   open (01:06 UTC cluster, MFE≈0).
2. **AVGO stale pre-earnings A-tier:** earnings calendar miss → `UNKNOWN` →
   not blocked → entry ~13% above post-earnings price.
3. **Crypto chop/danger whipsaw:** ATR-pct 98–100; stops ≈ noise; counter-tape
   RS-leader longs + late shorts stopped (MFE often <1R).
4. **A-tier overpromotion:** A-tier label not predictive (PF<B).
- *Not* caused by: bad registration, scheduler, stop/TP geometry, or filtering
  of the actionable set (A/B already RS-filtered).

## 10. What Worked
Funnel + RS-leader longs (real winners), short-side plumbing, alert
registration (0 untracked), SMCI legal gate, ETF earnings fix, A/B-only
reporting, catalyst importance, Opus auto-review (caught AVGO + A-tier issues),
infra stability.

## 11. What Failed / Underperformed
AVGO stale post-earnings A-tier (P1); overnight/stale stock intraday signals
(P1); A-tier predictive value (P1); crypto shorts this window (0W — small
sample, regime-driven); catalyst symbol mapping 24% (P2).

## 12. What NOT To Change Yet
- **Stops/TP geometry** — losses are regime/stale-data, not stop width; widening
  would hurt the immediate-adverse majority.
- **Crypto RS-leader / short logic** — works mechanically; sample too small
  (n=45) to retune; behavior is regime-appropriate.
- **Scoring thresholds, A/B cutoffs, scheduler cadence, Telegram logic, catalyst
  importance formula** — all behaving; no evidence to change.

## 13. (merged into §12)

## 14. Recommended Next Fixes (TODOs — evidence attached, DO NOT implement yet)
- **P0:** none (no data loss, no crash, no untracked alerts, no auto-trade risk).
- **P1 `TODO-stocks-stale-postearnings`:** block/ް demote single-name longs whose
  `earnings` is `UNKNOWN` AND a recent earnings event exists, and invalidate
  entry zones older than the last earnings print. Evidence: AVGO A-tier 89.7,
  entry 473–478, actual ~$417 post-earnings, flagged 4 Opus reviews.
- **P1 `TODO-stocks-market-closed-intraday`:** do not issue/keep *intraday* stock
  entries generated while the US cash session is closed (stale extended-hours
  prices). Evidence: 01:06 UTC cluster (NVDA/SMCI/AMD/SMH/AAPL) all −1R, MFE≈0.
- **P1 `TODO-stocks-atier-winrate`:** A-tier PF ~0.2 vs B ~1.4–2.2 — investigate
  A-tier promotion criteria (it over-credits extension/score). Reporting already
  exposes it; logic fix is separate.
- **P2 `TODO-catalyst-symbol-mapping`:** raise catalyst→symbol coverage above
  24% (alias/fuzzy company-name match). Context-only, non-gating.
- **P2 `TODO-catalyst-stock-suffix`:** strip `/USDT` from `asset_class=stocks`
  catalyst symbols (cosmetic).
- **P3:** investigate the recurring crypto **swing report exit=1** (1×/cycle,
  non-fatal).

## 15. Final Verdict
```
NEEDS_SIGNAL_LOGIC_FIX
```
System is **healthy and the 12h fixes work**. The remaining issues are
**signal-generation logic** (stale/market-closed stock entries + AVGO
post-earnings staleness + A-tier overpromotion), not infrastructure, reporting,
stops, or scheduler. All are **P1 TODOs with evidence — not yet implemented**,
per the read-only mandate.
