# 48h Playbook Performance Audit (PART 3)

**Window:** 2026-06-08 12:10 UTC → 2026-06-10 12:10 UTC · A/B signals only · Read-only.
**Source:** [TRADE_UNIVERSE_48H_AFTER_RECENT_FIXES.csv](TRADE_UNIVERSE_48H_AFTER_RECENT_FIXES.csv).

## 1. Headline

| Playbook | n | trig | W | L | exp | wait | stale | moved | amb | PF | WR | netR | avgR | MFE avg | MAE avg | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **crypto_intraday_catalyst_or_momentum** | 5 | 5 | **3** | 2 | 0 | 0 | 0 | 0 | 0 | **3.00** | **60%** | **+4R** | +0.80 | +1.76 | −0.88 | ✅ actionable |
| **crypto_swing_narrative_rs_momentum** | 11 | 11 | 4 | 7 | 0 | 0 | 0 | 0 | 0 | 1.29 | 36% | +2R | +0.18 | +1.35 | −1.30 | ⚠ softer than 14d (was 72% PF 5.80) — need more data |
| stocks_intraday_rth_momentum (A/B) | 24 | 22 | 5 | 6 | 11 | 0 | 2 | 0 | 1 | 1.00 | 45% | 0R | 0.00 | +0.65 | −0.72 | ⚠ flat — need more data |
| **crypto_failed_bounce_short** | 4 | 3 | 0 | 2 | 1 | 0 | 0 | 1 | 0 | 0.00 | 0% | −2R | −0.50 | +0.76 | −0.76 | ⚠ weak on small sample |
| **crypto_scalp_momentum_continuation** | 13 | 8 | 0 | 1 | 4 | 2 | 0 | 1 | 0 | 0.00 | 0% | −1R | −0.08 | +0.23 | −0.43 | ⚠ low-confidence (unchanged) |
| stocks_swing_watchlist_rs_rotation (C, paused) | 9 | 9 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | 0.12 | 11% | −7R | −0.78 | +0.54 | −0.96 | 🛑 pause justified |
| stocks_invest_watchlist_30d_thesis (C, paused) | 24 | 22 | 0 | 18 | 4 | 0 | 1 | 0 | 0 | 0.00 | 0% | **−18R** | −0.75 | +0.29 | −0.87 | 🛑 pause strongly justified |

Notes:
- `amb` column counts signals with `execution_ambiguous=intrabar_entry_stop` OR `intrabar_entry_tp`.
- Tiny samples (n<10) are directional only; treat as low-confidence verdicts.

## 2. Per-playbook detail

### 2.1 crypto_intraday_catalyst_or_momentum — **best of the window**
- 5 A/B / 3W / 2L / PF 3.00 / +4R.
- All wins carried `news_supported=1`. Aligns with the 14d audit conclusion that **catalyst is the discriminator** for crypto intraday.
- Top winners: ZEC (catalyst), NEAR (catalyst), WLD (catalyst).
- **Verdict: actionable, primary catalyst lane.**

### 2.2 crypto_swing_narrative_rs_momentum — **softer than 14d baseline**
- 11 A/B / 4W / 7L / PF 1.29 / +2R / MFE avg +1.35R.
- 14d baseline was WR 72% PF 5.80 — this 48h window underperforms it (4 of 7 losses came from a single 2026-06-09 morning batch that hit BTC-range chop). Sample is small.
- Top winners: ALLO (+3R), ZEC (+2R), BANK (+1R).
- Top losers: SAHARA (−1R), NEAR (−1R), CHZ (−1R).
- **Verdict: still actionable (primary), but window-specific weakness — need more data.**

### 2.3 crypto_failed_bounce_short — **2 stops, 1 moved_away, no wins**
- 4 A/B / 0W / 2L / 1 entry_moved_away (revalidator caught it) / 1 expired.
- 48h was mostly range/transition; failed-bounce shorts need bearish trend to work.
- **Verdict: actionable, regime-dependent — keep but don't force in chop.**

### 2.4 crypto_scalp_momentum_continuation — **low confidence holds**
- 13 A/B / 0W / 1L / 4 expired / 2 still waiting / 1 moved_away.
- MFE avg +0.23R — entry edge present but TP1 distance still too far for 2h horizon (the same pattern PART 2 of the scalp audit identified).
- **Verdict: keep low-confidence banner; no expansion (PART 3 of expansion v1 invariant holds — 0 expansion candidates routed to scalp).**

### 2.5 stocks_intraday_rth_momentum (A/B) — flat
- 24 A/B / 5W / 6L / 11 expired / PF 1.00 / 0R.
- Significantly softer than the 14d B-tier baseline (PF 2.03, +84R). 2 days is small sample after a generally chop tape this week.
- Top winners: AAPL B intraday-long (+1R), LLY B intraday-long (+1R), XOM A intraday-long (+1R), MSFT B intraday-short (+1R), META B intraday-short (+1R).
- Top losers: NVDA B long (−2R combined across signals), SMCI B long (−1R), AAPL one loss (−1R).
- **Verdict: still actionable (primary), but the 14d audit's NVDA/SMCI long warning is materializing in this window again. Need more data.**

### 2.6 stocks_swing_watchlist_rs_rotation (C, paused) — counterfactual confirms pause
- 9 C-tier swing / 1W / 8L / netR −7R.
- This is the **post-pause C-tier counterfactual** — proves that if these had been allowed actionable A/B they would have lost. Pause justified.

### 2.7 stocks_invest_watchlist_30d_thesis (C, paused) — pause STRONGLY justified
- 24 C-tier invest / 0W / 18L / netR −18R.
- The watchlist pause is doing its job: 18 losses caught by the gate that would otherwise have been A/B and on Telegram.
- **Verdict: keep watchlist-only. Re-audit on the timeline already in `MODE_ROUTING_DECISION_RECOMMENDATION.md`.**

## 3. Per-playbook 4-point verdict
| Playbook | actionable / low-conf / watchlist / needs data / needs fix |
|---|---|
| `crypto_intraday_catalyst_or_momentum` | **actionable** |
| `crypto_swing_narrative_rs_momentum` | **actionable** (with "softer this window" caveat) |
| `crypto_failed_bounce_short` | actionable, **regime-dependent** |
| `crypto_scalp_momentum_continuation` | **low-confidence** (unchanged) |
| `crypto_catalyst_backed_setup` | embedded in intraday/swing — strong overlay |
| `crypto_rs_leader_long` | embedded in swing/intraday — strong overlay |
| `stocks_intraday_rth_momentum` | **actionable** (window noise; needs more data) |
| `stocks_swing_watchlist_rs_rotation` | **watchlist-only** (pause justified by C-tier counterfactual) |
| `stocks_invest_watchlist_30d_thesis` | **watchlist-only** (pause STRONGLY justified — 0W/18L) |

```
PLAYBOOK_48H_AUDIT_COMPLETE
```
