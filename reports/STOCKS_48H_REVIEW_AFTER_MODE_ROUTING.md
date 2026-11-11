# 48h Stocks Review After Mode Routing (PART 8)

**Window:** 2026-06-08 12:10 UTC → 2026-06-10 12:10 UTC · Read-only.

## 1. Stocks intraday A/B performance
- n = 24 A/B closed (intraday)
- W=5, L=6, expired=11, **WR 45%, PF 1.00, netR 0R**
- Softer than 14d baseline (WR 55%, PF 2.03, +84R). 2-day sample is small.
- A-tier: 1 closed (XOM A long, loss). 14d audit's A-tier overpromotion warning materialized once in this window.
- Shorts subset: 1 closed (AVGO B short, win + intrabar flagged). Stocks shorts edge holds qualitatively but sample is tiny.

| Best wins | XLV +2R intraday-long, XLV +1R, JPM +1R, AAPL +1R, AVGO +1R (ambiguous) |
| Worst losses | XLF, XOM, GOOGL, NVDA pattern losses; **XOM A long −1R** = A-tier symptom |

## 2. A/B leaks from swing / invest?
- **Stocks swing post-pause A/B**: **0 leaks** ✅ — gate `stocks_swing_paused_after_48h_audit` holds.
- **Stocks invest post-pause A/B**: **0 leaks** ✅ — gate `stocks_invest_paused_after_mode_viability_audit` holds.
- All 9 stocks_swing closures + 18 stocks_invest closures in window were C-tier (paused as designed).

## 3. NVDA / SMCI / A-tier long behavior
- **NVDA** no closed A/B intraday in this 48h window (none triggered A/B during this period after the 14d warning surfaced)
- **SMCI** no closed A/B intraday
- **A-tier longs**: 1 closure → loss (XOM long −1R) — confirms the A-tier overpromotion pattern is still real
- 14d audit's recommendation to manually scrutinize A-tier longs remains valid

## 4. Stocks shorts performance
- AVGO B short on 06-09 → win (+1R, but ambiguous intrabar_entry_tp flag) — 1 of 1 sample
- XLY B short on 06-09 → loss (−1R)
- GOOGL B short on 06-08 → loss (−1R)
- Net: 1W/2L (33% WR), small sample, weaker than 14d 86% WR cohort
- **Verdict:** the 14d shorts edge requires more sample to confirm or reject in this window

## 5. Market-closed / stale / earnings / legal gates
- `market_closed_intraday_planning_only` gate fired on pre-RTH signals as expected
- No `stale_post_earnings_setup` markers in the window's losses (the ETF UNKNOWN false-positive fix appears to be holding — no spurious gates)
- No legal-risk gate triggers observed in the losing trades — consistent with the headline/legal filter working

## 6. Counterfactual value (watchlist-only modes)
- **Stocks swing C-tier**: 1W / 8L over 48 h → would have been catastrophic if actionable A/B. Pause **justified**.
- **Stocks invest C-tier**: 0W / 18L over 48 h → pause **STRONGLY justified**. The 30-day thesis trade is still systematically losing on the same pipeline.

## 7. Stocks symbols that need manual caution
- **NVDA / SMCI longs** — flagged 14d ago; still flagged. Manually skeptical on any new A/B.
- **XOM A long** — the A-tier overpromotion symptom is recurrent; verify chart structure before trusting A-tier scores.
- **Tech-sector longs (XLK, XLV) during chop** — XLV worked +2R then +1R on 06-08/09, but the same XLF and XLK longs lost. Sector lean unreliable.

## 8. Verdict
- Stocks intraday: **still actionable, but window is softer than 14d**. Need more sample before declaring regression.
- Stocks swing: **pause justified** by 8-loss counterfactual.
- Stocks invest: **pause STRONGLY justified** by 18-loss counterfactual.
- Stocks shorts: small sample, neutral.
- NVDA/SMCI longs: continue manual caution.

```
STOCKS_48H_REVIEW_COMPLETE
```
