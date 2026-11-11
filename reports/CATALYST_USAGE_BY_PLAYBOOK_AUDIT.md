# Catalyst Usage By Playbook (PART 2)

**Date:** 2026-06-15 · Read-only.

| Playbook | Should use catalyst? | Actually uses? | Evidence |
|---|---|---|---|
| **crypto scalp** | No — technical by design | ✅ correct: BTC/ETH tape + volume + momentum + funding/OI; news intentionally not required | scoring weights are momentum/regime-dominant; scalp is the lowest-catalyst cohort by design. Confirmed mostly-technical. |
| **crypto intraday (catalyst/momentum)** | Yes — fresh catalyst ≤ 6h | ⚠️ partial: catalyst_quality component exists + funding/OI used, but **no freshness gate** (old catalysts stay actionable); RS-vs-BTC used | `scoring_agent.py` catalyst_quality (baseline 0.3 + importance/10); derivatives alignment penalty live |
| **crypto swing (narrative/RS)** | Yes — narrative + RS + catalyst | ✅ yes: catalyst reaches signal, Opus packet includes catalyst thesis, scorer rewards importance | best catalyst integration; swing is the strongest cohort |
| **crypto failed-bounce short** | Yes — fresh negative catalyst OR breakdown confirmation + squeeze data | ✅ funding/OI + squeeze-guard used; ⚠️ doesn't strictly require *fresh* negative catalyst | derivatives_agent squeeze interpretation + short_bounce_guard live |
| **stocks intraday** | Yes — company news + sector + earnings/legal gates | ⚠️ partial: scorer uses news binary + earnings risk + sector; **but `news_supported` flag never set on the signal row** → catalyst-backed stocks are unlabelled and unmeasurable | `stocks/scoring_agent.py` news_catalyst binary + earnings_risk_adjustment; legal_risk gate live |
| **stocks swing/invest** (paused) | Receive catalysts correctly | ✅ same packet path; paused at 0× so no live impact | watchlist-only |

## Performance evidence (catalyst on vs off)

### Crypto A/B (closed)
| news_supported | n | W | L | raw R |
|---|---:|---:|---:|---:|
| **1 (catalyst-backed)** | 34 | 12 | 11 | **+15.0** |
| 0 (technical-only) | 126 | 25 | 59 | **−3.0** |

**Catalyst-backed crypto signals trade dramatically better** (+15R on 34 vs −3R on 126). But only ~21% of triggered A/B crypto signals carry the catalyst flag.

### Stocks A/B (closed)
| news_supported | n | raw R |
|---|---:|---:|
| 0 (ALL of them) | 533 | +78.0 |
| 1 | 0 | — |

**Stocks catalyst impact is unmeasurable** because the `news_supported` flag is never set to 1, despite 7,547 stock news items collected in 14d. This is a labelling gap, not a collection gap (the scorer does use news internally).

## Conclusion

- Catalyst data is **collected and reaches scoring** for every playbook that should use it.
- The crypto catalyst signal is **real and strong** (+18R swing in raw R between cohorts).
- Two gaps: (1) **no freshness gate** on crypto intraday catalysts; (2) **stocks signals never carry the `news_supported` label**, blocking measurement and Telegram labelling.
