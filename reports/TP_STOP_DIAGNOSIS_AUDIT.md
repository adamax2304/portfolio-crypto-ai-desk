# TP / Stop Diagnosis Audit (PART 3)

**Date:** 2026-06-11 · **Method:** For every triggered, closed, or expired A/B signal, classify the exit reason using stored notes + MFE/MAE. Read-only.

---

## 1. Exit-reason taxonomy (all-time A/B)

| Reason | n | raw R | sized R | Top playbook (n) |
|---|---:|---:|---:|---|
| **never_filled** | 230 | +0.0 | +0.0 | stocks_intraday_rth_momentum (197) |
| **expired_with_positive_mfe** (MFE > +0.3R, then expired flat) | 189 | +0.0 | +0.0 | stocks_intraday_rth_momentum (145) |
| **clean_stop** | 132 | −132.0 | −78.5 | stocks_intraday_rth_momentum (70) |
| **gap_slippage** (entry/TP/stop slip from candle gap, mostly favorable) | 90 | +66.0 | +71.5 | stocks_intraday_rth_momentum (55) |
| **expired_no_edge** (no meaningful MFE, ran out of time) | 82 | +0.0 | +0.0 | stocks_intraday_rth_momentum (70) |
| **clean_tp** | 73 | +150.0 | +146.5 | stocks_intraday_rth_momentum (58) |
| **reached_+0.5R_but_stopped** | 37 | −37.0 | −22.0 | stocks_swing_watchlist (12) |
| **no_entry: None outcome** (pending) | 35 | +0.0 | +0.0 | crypto_scalp (21) |
| **ambiguous_intrabar** (same-candle TP+stop) | 26 | +29.0 | +19.0 | stocks_intraday_rth_momentum (24) |
| **tp_hit_then_reversed** (MFE > 1.5× final_r) | 10 | +12.0 | +11.0 | stocks_intraday_rth_momentum (7) |
| **reached_+1R_but_stopped** | 7 | −7.0 | −6.0 | stocks_intraday_rth_momentum (4) |
| **bad_entry_immediate_adverse** | 3 | −3.0 | −3.0 | crypto_intraday_catalyst (2) |

---

## 2. Headline reads from the taxonomy

### What's working
- **Clean TPs**: 73 wins at +150R raw (+146.5 sized). PF contribution dominant.
- **Gap slippage NET POSITIVE**: 90 cases, +66R raw, +71.5R sized. Gaps tend to favor our entries because the stocks intraday playbook breaks out into the gap.
- **Ambiguous intrabar resolved positively**: 26 cases, +29R raw. Our conservative-stop policy proves not to be a chronic drag.
- **bad_entry_immediate_adverse** is rare (3 cases): entry-zone logic is not a problem.

### What's draining
- **Clean stops**: 132 cases, −132R raw / −78.5R sized. The sizing layer absorbs ~40% of stop-out drag. Stops themselves are NOT chronically wrong — they're hitting because the thesis is wrong, not because they're tight.
- **reached_+0.5R then stopped**: 37 cases, −37R raw / −22R sized. This is the **single most actionable bucket** — partial TP at +0.5R would have saved 18.5R (50% × +0.5R × 37 cases) and converted these from −37R to ~−18R. But ~25% of this bucket lives in `stocks_swing_watchlist_rs_rotation` which is already paused.
- **reached_+1R then stopped**: 7 cases, −7R. **TINY** — a "BE-after-+1R" rule would have saved ~7R. Not worth the policy change to enforce.
- **expired_with_positive_mfe**: 189 cases (huge!) but **0R contribution** because they ran out of time without ever stopping out. A tighter expiry or partial-TP-at-+0.5R rule would convert some of these to small wins (~50% × 0.5R × 189 = ~+47R upper bound, but most have MFE < 0.5R so realistic capture is ~20R).
- **tp_hit_then_reversed**: 10 cases, **already counted as wins** (+12R). Trailing stops would not improve net (they'd compress winning R).

---

## 3. Impact estimates by potential policy change

| Hypothetical change | Affected bucket | Naive raw R uplift | Naive sized R uplift | Risk |
|---|---|---:|---:|---|
| Partial-TP @ +0.5R, 50% off | reached_+0.5R_but_stopped (37) | +9.25R | +5.5R | Compresses winners that go past +0.5R to TP1 (would lose ~50% of those gains) → net might be NEUTRAL. |
| Hard-TP @ +0.5R (full close) | reached_+0.5R_but_stopped (37) | +18.5R | +11R | Same risk × 2: cuts every winner short. PF likely drops. |
| BE stop after +1R MFE | reached_+1R_but_stopped (7) | +7R | +6R | Negligible sample; risk of cutting winners. |
| Earlier expiry (4h crypto scalp) | expired (positive MFE) bucket subset | +5R est. | +2.5R est. | None for closed sample; for new signals, may cut some winners that needed 6-8h. |
| Trail stop after +0.7R MFE | clean_tp + tp_reversed | unchanged or slightly negative | unchanged | Trail premature would chop existing winners. |

**No single bucket is large enough relative to portfolio (+144.5R sized) to justify a TP/SL change.**

---

## 4. Per-playbook diagnosis

### `stocks_intraday_rth_momentum` (646 signals, +133R sized, PF 2.50)
- Clean TP: 58 of 73 winners come from here.
- Clean stop: 70 of 132 stop-outs from here.
- Expired with positive MFE: 145 of 189 (huge undefined opportunity).
- Gap slip: 55 of 90 favorable gap fills.
- **Diagnosis:** working as designed. NO TP/SL change recommended. The 145-strong expired-with-positive-MFE bucket suggests a "partial @ +0.5R" *might* unlock more — but the headline PF 2.50 says don't risk it without 60+ more days of data.

### `crypto_intraday_catalyst_or_momentum` (33, −14R sized, PF 0.33)
- 21 losses out of 24 triggered.
- Most losses are bulk shorts on BTC/ETH/alt breakdowns that mean-revert.
- **Diagnosis:** TP/SL is NOT the issue. **Entry filter / catalyst freshness is.** Shorting `breakdown/retest` without a *fresh* (≤ 6h) bearish catalyst is the failure mode. This is an entry-side fix, not exit-side.

### `crypto_scalp_momentum_continuation` (85, −4.5R sized)
- 0 wins / 9 losses / 34 expired / 42 never filled.
- **Diagnosis:** insufficient 1m candle data to adjudicate. The 0.5× sizing already mitigates. Wait for 1m archive.

### `crypto_swing_narrative_rs_momentum` (33, +12R sized, PF 1.80)
- Working. NO change.

### `crypto_failed_bounce_short` (24, +11R sized, PF 2.10)
- Working. The "fresh catalyst" requirement is implicit in the playbook gate. NO change.

### `stocks_swing_watchlist` (54, −32R counterfactual, sized 0×)
- Already paused. Pause confirmed correct.

### `stocks_invest_watchlist` (39, −26R counterfactual, sized 0×)
- Already paused. Pause confirmed correct.

---

## 5. Bottom line

- **No TP change is justified by the data alone.** The single most attractive bucket (reached_+0.5R_but_stopped, 37 cases, −22R sized) has a balancing risk of cutting winners short.
- **No stop change is justified.** Most stops hit because the thesis failed, not because the stop was wrong.
- **The actionable insight is upstream**: crypto intraday catalyst shorts need a *fresh-catalyst* filter, not a TP/SL change.
