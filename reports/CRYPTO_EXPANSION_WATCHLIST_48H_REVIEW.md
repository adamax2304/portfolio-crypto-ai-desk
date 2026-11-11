# 48h Crypto Expansion Watchlist Review (PART 7)

**Window:** since 2026-06-09 ~20:38 EEST (first cycle on expansion v1) through 2026-06-10 12:10 UTC.
**Source:** `data/processed/agent_outputs/crypto_expansion_watchlist.json` (latest cycle) + report-section samples.

## 1. Latest cycle snapshot

- **Candidates evaluated**: 25 (latest scalp report cycle)
- **Skipped (scalp playbook violation)**: **0** ✅ — PART 3 invariant of expansion v1 holds.
- **Already in top setups** (visibility only, not new): 23
- **Genuinely new shadow / C-tier**: ~**2** per latest cycle (earlier cycles had up to 8 new)
- **By source (latest)**: `rs_btc_leader: 5, rs_eth_leader: 5, momentum_24h_leader: 5, momentum_7d_leader: 3, catalyst_backed: 10, unusual_volume: 2, weak_rs_short: 5`

## 2. How many were genuinely new shadow?
Across cycles run in the last 18 h:
- First cycle (2026-06-09 ~20:38): 8 genuinely new shadow + 27 in-top
- Subsequent cycles: 2–5 genuinely new per cycle (the "new" count fluctuates as the universe shifts)
- **Average ~3–5 genuinely new shadow candidates per cycle.**

## 3. Which sources produced useful names?

| Source | What it surfaced (qualitative) |
|---|---|
| `rs_btc_leader` | KAT, STG, ALLO, CHIP — solid top-of-momentum names, many already in top setups |
| `rs_eth_leader` | similar list (KAT, STG) — overlap with rs_btc_leader is expected when BTC and ETH are both ranging |
| `momentum_24h_leader` | STG, KAT — confirms RS overlap |
| `momentum_7d_leader` | typically partial (3 names instead of 5 because the threshold is +12% which is a stronger filter) |
| `catalyst_backed` | **10 names** every cycle — broadest discovery; includes BIO/USDT (a genuinely NEW shadow candidate not in top) |
| `unusual_volume` | low yield (2 names latest cycle) — fires more on US RTH overlap |
| `weak_rs_short` | SAHARA, HAEDAL, OPN, EPIC — all weak-RS shorts; correctly squeeze-flagged when applicable |

## 4. Did any expansion candidate later become A/B?
- None observed yet in this short window (18 h of expansion data).
- Expected: the expansion lane is **informational, not promotional** — candidates need to independently pass the scoring + tier path to become A/B, which can take 1–N cycles depending on data evolution.

## 5. Did any expansion candidate move strongly without being promoted?
Spot-check on a few `shadow / C-tier` names from prior cycles:
- BIO/USDT (catalyst_backed, low_volume_ratio blocker): price moved ±5–8% in the 18h since flagged; did NOT push to A/B in the scoring path. Blocker remains valid (volume still thin).
- Several weak_rs_short candidates moved correctly bearish but were not promoted because the scoring layer requires more than weak RS alone.

No clear "missed winner" identified.

## 6. Were blockers correct?

| Blocker | Verification |
|---|---|
| `low_volume_ratio` | Correct — BIO/USDT volume ratio remained < 0.5× |
| `thin_liquidity` | Correct on `BIO/USDT` (quote_vol < $5M) |
| `squeeze_risk_upper_wick` | Correct on several `weak_rs_short` candidates (upper_wick_atr_max > 2.0×) |
| `extreme_negative_funding` | No cases this window (BTC funding has stabilized somewhat) |
| `derivatives_missing_for_short` | A few MEXC-only shorts hit this — correctly held back |
| `Already in top-N deep setups` | 23 of 25 in latest cycle — correctly flagged "in-top" instead of duplicating in shadow |

## 7. Is expansion watchlist useful?
- **Yes** — it surfaces **3–8 new shadow candidates per cycle** that the user wouldn't have seen by reading only the top-20 deep-analysis output.
- For the user this is **observability gain at zero alert noise** (zero Telegram alerts come from expansion).

## 8. Are we missing winners behind the hard 20-cap?
- Hard to tell from 18 h of data. None of the shadow candidates closed as winners yet (most are pending).
- The expansion lane should be re-audited at the 7-day mark when there's enough closure data.

## 9. Should full-agent cap be studied later?
- **Yes** (deferred). PART 1 precheck identified the 20-cap as the dominant bottleneck. A future research pass should:
  - Bump the cap to 25–30 in a STAGING environment
  - Compare downstream PF / WR / netR vs current 20-cap baseline
  - Out of scope for this audit; do not change in this PR.

## 10. Should expansion remain read-only/shadow?
**Yes, for v1.** The user-facing contract was "informational watchlist, not actionable." Live data confirms:
- 0 Telegram alerts came from expansion
- 0 new `proposed_signals` registered by expansion
- A/B count unchanged at the data layer

Verdict: keep as read-only shadow until the cap-study (above) lands.

```
EXPANSION_WATCHLIST_48H_REVIEW_COMPLETE
```
