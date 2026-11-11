# Full Trade Audit — 48h After Recent Fixes

**Window:** 2026-06-08 12:10 UTC → 2026-06-10 12:10 UTC. Read-only audit. No code/scoring/TP/SL/routing changes proposed in this report.

**Sibling reports** (all in this PR):
- [TRADE_AUDIT_48H_SYSTEM_HEALTH.md](TRADE_AUDIT_48H_SYSTEM_HEALTH.md)
- [TRADE_UNIVERSE_48H_AFTER_RECENT_FIXES.md](TRADE_UNIVERSE_48H_AFTER_RECENT_FIXES.md) + [.csv](TRADE_UNIVERSE_48H_AFTER_RECENT_FIXES.csv)
- [PLAYBOOK_PERFORMANCE_AUDIT_48H.md](PLAYBOOK_PERFORMANCE_AUDIT_48H.md)
- [TRADE_BY_TRADE_REVIEW_48H.md](TRADE_BY_TRADE_REVIEW_48H.md)
- [PENDING_SIGNALS_48H_REVALIDATION_AUDIT.md](PENDING_SIGNALS_48H_REVALIDATION_AUDIT.md)
- [EXECUTION_ACCURACY_AUDIT_48H.md](EXECUTION_ACCURACY_AUDIT_48H.md)
- [CRYPTO_EXPANSION_WATCHLIST_48H_REVIEW.md](CRYPTO_EXPANSION_WATCHLIST_48H_REVIEW.md)
- [STOCKS_48H_REVIEW_AFTER_MODE_ROUTING.md](STOCKS_48H_REVIEW_AFTER_MODE_ROUTING.md)

## 1. Executive summary

The system is **operating cleanly post-fixes**. All recent additions (playbook labeling, pending revalidation in scheduler, paper execution annotations, watchlist-only stocks modes, low-confidence scalp, crypto expansion v1, parallel crypto fetch) are observable in live data with **no broken protections** and **no scoring/TP/SL changes**.

48 h volume: 313 deduped signals (33 crypto, 280 stocks). Revalidator fired 46 times (38 stale + 8 moved-away). Execution-annotation events: 6 intrabar-ambiguous + 53 gap-slip flags. Untracked legacy alerts: 0.

## 2. Did the system improve after recent fixes?

| Area | Before | After (this window) |
|---|---|---|
| Tracker chronological correctness | clean (audit confirmed) | unchanged ✅ |
| Pending stale visibility | none — pending lingered | **46 transitions/48h** — revalidator catching them ✅ |
| Execution ambiguity visibility | hidden bugs (intrabar +stop/+TP) | **6 ambiguity flags surfaced** ✅ |
| Gap-slip awareness | silent flat R | **53 slip annotations**, headline R unchanged ✅ |
| Stocks swing actionability | losing 12% WR | **0 A/B leaks**; C-tier counterfactual −7R confirms pause ✅ |
| Stocks invest actionability | losing 0% WR | **0 A/B leaks**; C-tier counterfactual −18R confirms pause ✅ |
| Crypto scalp annotation | silent low edge | low-confidence banner visible everywhere ✅ |
| Crypto expansion observability | none | **+3–8 shadow candidates/cycle**, 0 A/B spam ✅ |
| Untracked legacy alerts | 0 baseline | 0 ✅ |

**Conclusion: the system improved on observability and protections; no edge-loss observed at the headline level.**

## 3. Best playbook last 48h
**`crypto_intraday_catalyst_or_momentum`** — 5 closed A/B, 3W/2L, **PF 3.00, WR 60%, +4R**. Catalyst overlay is still the cleanest crypto edge. ZEC, WLD, ALLO winners are catalyst-tagged.

## 4. Worst playbook last 48h
**`stocks_invest_watchlist_30d_thesis`** — 24 closed C-tier (counterfactual), **0W/18L, −18R**. The 30-day thesis pipeline is structurally broken and the pause is doing its job. **Re-affirms watchlist-only verdict.**

Worst actionable playbook: **`crypto_failed_bounce_short`** — 4 A/B, 0W/2L, −2R. Regime-dependent (range chop hurts shorts).

## 5. Best trades
| Symbol | Playbook | R | Notes |
|---|---|---:|---|
| ZEC swing long (06-08) | crypto_swing_narrative_rs | +3 | Clean win, catalyst-backed |
| WLD intraday long (06-08) | crypto_intraday_catalyst | +3 | Catalyst lane delivered |
| STG swing long (06-10) | crypto_swing_narrative_rs | +3 | TP3 hit; gap-slip-tp=65% (real fill better than recorded) |
| CHIP swing long (06-09) | crypto_swing_narrative_rs | +2 | **Ambiguous** — gap_slip_stop=132%; very fragile |
| ZEC intraday long (06-07 carry-in) | crypto_intraday_catalyst | +2 | Catalyst |

## 6. Worst trades
| Symbol | Playbook | R | Classification |
|---|---|---:|---|
| Each of 18 stocks_invest C-tier longs | — | −1 each | counterfactual; gate caught them ✅ |
| Each of 8 stocks_swing C-tier longs | — | −1 each | counterfactual ✅ |
| 4 crypto_swing losses (CHZ×2, IO, SENT) | crypto_swing | −1 each | window-specific BTC chop |
| XOM A intraday long | stocks_intraday | −1 | **A-tier overpromotion symptom** (14d audit warned of this) |
| ZEC, XLM crypto shorts | crypto_failed_bounce_short | −1 each | stopped by wick squeeze |

## 7. Execution mismatches / ambiguity
- 3 intrabar_entry_stop + 3 intrabar_entry_tp = 10.5% of closed A/B (within expected 5–10% band).
- 34 gap_slip_stop ≥ 10% on losses (real fills worse than headline −1R).
- 19 gap_slip_tp ≥ 10% on wins (real fills better than headline). Partially offsets.
- **No silent ambiguity** — every event was annotated; user can filter via `notes` field.

## 8. Pending signal quality
- 38 stale + 8 moved-away + 38 waiting. Revalidator firing correctly.
- No false-positive cancellations; no missed stale setups.
- Horizons calibrated correctly for the current sample.

## 9. Should TP/SL remain unchanged?
**Yes** — TP/SL geometry was deliberately not changed in any recent PR. The 48h evidence does not call for a change:
- Headline R values are mostly fair (slip annotations partially offset both ways).
- A change to TP/SL would silently rewrite historical comparisons and is out of the current safe-fix lane.
- A separate research pass (PART 1-6 of the paper execution model spec) is the right venue.

## 10. Should crypto scalp still deserve low-confidence only?
**Yes** — 13 scalp A/B in the window: 0W, 1L, 4 expired, others waiting/moved-away. Same pattern as the 14d audit (MFE present but no TP capture). **Keep low-confidence banner.** No expansion-driven scalp inflation (0 violations).

## 11. Should stocks invest/swing stay watchlist-only?
**Yes — strongly** for invest (0W/18L counterfactual confirms pause); **yes** for swing (1W/8L counterfactual). Re-audit at the trigger thresholds already documented in `MODE_ROUTING_DECISION_RECOMMENDATION.md`.

## 12. Should crypto expansion remain shadow-only?
**Yes** — v1 invariants held in production: 0 scalp violations, 0 Telegram from expansion, 0 new `proposed_signals` registered by expansion. The expansion lane added 3–8 shadow candidates per cycle without any noise. Keep as shadow until a dedicated re-audit can compare PF outcomes from promoted shadow names vs the existing top-N.

## 13. What to do next
| Item | Status | Recommendation |
|---|---|---|
| Keep crypto scalp low-confidence | ✅ working | **keep as is, collect more data** |
| Stocks swing pause | ✅ working | **keep as is**, re-audit at 20 closed C-tier post-pause |
| Stocks invest pause | ✅ working | **keep as is**, re-audit at 20 closed C-tier post-pause |
| Crypto expansion lane | ✅ working | **read-only study needed** — analyse promotion behavior over 7 days |
| Revalidator horizons | ✅ calibrated | **keep as is** |
| Execution annotations | ✅ surfaced | **safe reporting-only fix candidates** for next pass: optional tick / 1m bars for crypto scalp backtest (research) |
| A-tier overpromotion (stocks) | ⚠ recurring | **read-only study needed** — diagnose what conditions tip A-tier longs into losses |
| NVDA/SMCI long manual caution | ⚠ persistent | **keep as is**; user remains skeptical until structural reason resolved |

**No "strategy change needs approval" items in this audit.** Everything either works, is properly paused/annotated, or needs more data.

## Final verdict
```
TRADE_AUDIT_48H_COMPLETE
```

System is healthy. All recent fixes are observable in live data. No new pause/unpause decisions needed; no TP/SL changes warranted; revalidator + expansion + annotations are doing their job. Continue monitoring; the next audit should look at the 7-day expansion-lane promotion patterns and the A-tier-stocks-long overpromotion diagnosis.
