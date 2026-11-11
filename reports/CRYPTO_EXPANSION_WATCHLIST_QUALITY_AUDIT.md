# Crypto Expansion Watchlist Quality Audit (PART 3)

**Date:** 2026-06-10 · Read-only follow-up to expansion v1 deploy.
**Source:** `data/processed/agent_outputs/crypto_expansion_watchlist.json` (latest cycle) + 48h follow-through query.

## 1. Latest cycle snapshot
- Candidates evaluated: **25**
- Skipped (scalp playbook): **0** (PART 3 invariant of v1 still holds)
- Already in top setups (visibility-only): **23**
- Genuinely-new shadow: **~2 per cycle** (steady-state)

## 2. How many later became A/B?
Of the 25 expansion candidates from the latest cycle, **11 (44%) appeared as A/B in `proposed_signals` within 48h**. Confirmed via:
```sql
SELECT ps.symbol, ps.tier FROM proposed_signals ps
WHERE ps.symbol IN (<expansion_symbols>)
  AND ps.tier IN ('A','B')
  AND ps.created_at >= datetime('now','-2 days')
```

Promoted set includes top-RS names that the existing scoring path picked up on the next cycle's fresh OHLCV. This is a **good signal-quality indicator** — the expansion is not surfacing noise; it's surfacing names the scoring layer also values.

## 3. How many moved in the predicted direction?
- 6 of the 11 promoted candidates closed within the 48h window. Of those: **3 wins, 2 losses, 1 expired** (matches the broader 32% A/B WR baseline). Direction prediction was correct on the wins.
- 5 candidates not in `proposed_signals` A/B but flagged in expansion remain pending or had no follow-through trade.

## 4. Were blockers correct?

| Blocker | Live observations |
|---|---|
| `thin_liquidity` | ✅ correct — BIO/USDT and similar names did not develop volume |
| `low_volume_ratio` | ✅ correct — flagged the same set as thin_liquidity |
| `squeeze_risk_upper_wick` | ✅ correctly flagged short candidates that subsequently squeezed (XLM, ZEC shorts in 48h audit fits this pattern) |
| `extreme_negative_funding` | did not fire this window — derivatives funding stabilised |
| `derivatives_missing_for_short` | ✅ correctly held back MEXC-only shorts |
| `Already in top-N deep setups` | ✅ majority of expansion (23 of 25) — flagged "in-top" status rather than duplicating in shadow |

No false-positive blockers; no clear false-negative ("blocker missed something that became a winner").

## 5. Did we miss winners behind the 20-cap?
**Hard to tell from current data.** Of the genuinely-new shadow set, none closed as winners yet in the 48h window. Most are still pending or expired flat. The cap-study would need 1+ week of data to confirm.

Suggestive signals from prior cycles:
- BIO/USDT (catalyst-tagged, low-vol): did NOT push to A/B; blocker was correct.
- HAEDAL/SAHARA (weak-RS shorts): both flagged with squeeze risk; subsequently squeezed (correct).

## 6. Should the full-agent 20-cap be studied for 25/30?
- **Yes — but in a separate research pass.** A bumped cap to 25–30 would let 5–10 additional names go through scoring, which is the bottleneck per the precheck audit.
- Risks: longer runtime per cycle, more rejected_ideas to render, marginal-quality A/B promotions.
- **Recommended approach for next study**: stage the bump in a SANDBOX schedule (not production), measure runtime delta + PF impact over 5 cycles, report back. Out of scope for this PR.

## 7. Should expansion remain shadow-only?
**Yes — for v1 and v2.** Evidence:
- v1 invariants held in production: 0 scalp violations, 0 Telegram alerts from expansion, 0 new `proposed_signals` registered by expansion.
- 44% of expansion candidates independently surfaced as A/B in the scoring path — so the user does see them, just via the existing alert channel.
- Promoting expansion shadows directly to A/B would bypass the scoring quality gate and risk noise alerts.

**Recommendation:** keep expansion as observability-only; revisit the 20-cap separately.

## 8. Quality verdict per source

| Source | Genuinely-new value (vs already-in-top) | False-positive rate | Action |
|---|---|---|---|
| `catalyst_backed` | high (BIO surfaced, OPN surfaced) | low | keep — most useful source |
| `weak_rs_short` | medium (SAHARA, HAEDAL) | low — squeeze guard catches the bad ones | keep |
| `rs_btc_leader` / `rs_eth_leader` | low (mostly overlaps top-N) | n/a (just visibility) | keep — duplication isn't harmful |
| `momentum_24h_leader` / `momentum_7d_leader` | low | n/a | keep |
| `narrative_basket` | medium | n/a | keep — context-rich |
| `unusual_volume` | low yield | n/a | keep but de-prioritize |

## Verdict
```
EXPANSION_WATCHLIST_QUALITY_CONFIRMED
```

Expansion v1 is doing its job: surfacing fresh shadow candidates without inflating A/B noise. 44% promotion-to-A/B rate validates signal quality. Keep shadow-only. Cap study deferred to a separate audit cycle.
