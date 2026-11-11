# Paper Execution Model — Spec (PART 4)

**Date:** 2026-06-09 · **Scope:** Document the paper execution model the tracker implements and the additions PART 7 will deploy. No behavior changes in this document — this is the contract.

## 1. Order types

### Entry
| Field present | Order type | Rationale |
|---|---|---|
| `entry_low + entry_high` (zone) | **Limit order at zone boundary** | A pullback / reclaim setup waits for price to come into a defined area |
| `entry_trigger` only | **Stop-entry at trigger** | A breakout setup waits for price to push through a level |

### Stop
- **Stop-market** at `invalidation` (or `stop_loss` if set; `invalidation` is the source-of-truth field).
- Fill assumption: **at `invalidation` level** (no slippage modeling in headline R).
- Trigger: candle **wick touch** (`low <= invalidation` long, `high >= invalidation` short).
- See §5 for new slip-tracking annotation.

### TP1 / TP2 / TP3
- **Limit order at TP level.**
- Trigger: candle **wick touch** (`high >= tp` long, `low <= tp` short).
- TP1 hitting first is a **full win at +1R** in the headline model. There is no partial-position model; TP2/TP3 are tracked but a single signal exits at the first TP touched (this is consistent with the existing `_classify` behavior).

## 2. Fill price selection

### Entry zone (limit)
For a candle that overlaps the zone:
1. **If the candle open is inside the zone** → fill at the open price. This is the realistic "limit order resting in the book, filled by the opening print" case.
2. **If the candle gapped through the zone (open outside, range overlaps)**:
   - LONG: fill at the **closer edge to where price came from** (entry_high if approaching from above; entry_low if approaching from below).
   - SHORT: symmetric.
3. **If the candle did not touch the zone** (`low > entry_high` long, or `high < entry_low` long) → no fill.

### Single trigger price
Fill at the trigger level exactly. (Modeled as a stop-market for breakouts.)

## 3. Chronological ordering

Hard rules:
- **TP/stop cannot be counted before entry.** The walk has explicit pre-entry / in-position branches; pre-entry only checks invalidation (which marks "missed_no_entry", not a stop loss).
- **Same-candle TP+stop AFTER entry** is detected and marked `ambiguous` with conservative loss (`-1R`) per the existing `same_candle_conservative=True` config default.

New (PART 7):
- **Same-candle ENTRY+stop** (entry and stop hit in the SAME bar after triggering): `execution_ambiguous = "intrabar_entry_stop"`. Headline outcome is still applied (current model), but the row is flagged so downstream analytics may exclude it from clean-win/clean-loss buckets.
- **Same-candle ENTRY+TP** (entry and TP1 hit in the SAME bar): `execution_ambiguous = "intrabar_entry_tp"`. Same treatment.
- The 14d reconstruction sample (PART 2-3) found 3 of 40 signals affected; we expect a steady-state rate of ~5–10% on scalps.

## 4. Gap handling

| Case | Behavior today | PART 7 addition |
|---|---|---|
| Gap UP through long entry zone (no overlap) | No entry recorded. ✅ | `notes` gets `gap_past_entry_zone=up` for visibility |
| Gap DOWN through long entry zone (no overlap) | No entry recorded. ✅ | `notes` gets `gap_past_entry_zone=down` |
| Gap INTO long entry zone (open inside) | Fill at open. ✅ | no change |
| Gap past long stop (low << invalidation) | `stop_hit=True`; reported R = flat `-1R` | `notes` gets `gap_slippage_stop_pct=NN` if slip > 10% of risk. Headline R unchanged. |
| Gap past long TP (high >> tp) | `tp_hit=True`; reported R = flat `+1R`/`+2R`/`+3R` | `notes` gets `gap_slippage_tp_pct=NN` if slip > 10% of risk. Headline R unchanged. |

Headline R-model is **not modified** in PART 7. Annotations enable a future slip-aware audit without disturbing historical comparisons.

## 5. Slippage / bid-ask

- The tracker uses **OHLCV only**. No bid/ask, no spread, no fees, no liquidity penalty.
- This is acceptable for paper trading on liquid majors and standard stocks. It systematically **understates losses on thin alts and gappy stocks**.
- Slip annotations (§4) provide observability without changing reported R.

## 6. Ambiguity policy summary

| Event combo (in one candle) | Today | PART 7 |
|---|---|---|
| pre-entry invalidation | mark `missed_no_entry`, R=0 | unchanged + cosmetic rename of `stop_hit` flag to `pre_entry_invalidation` |
| entry + stop | clean loss −1R | mark `execution_ambiguous=intrabar_entry_stop`, still −1R, but exposed |
| entry + TP1 | clean win +1R | mark `execution_ambiguous=intrabar_entry_tp`, still +1R, but exposed |
| stop + TP (after entry) | already flagged ambiguous, conservative −1R | unchanged |
| missing OHLCV | `skipped_no_ohlcv` counter incremented, no outcome row written | unchanged |
| stock outside RTH | implicit — yfinance excludes pre/post bars | unchanged (rely on data source) |

## 7. Headline-stats inclusion rules

| Bucket | Included in WR/PF headline? |
|---|---|
| clean win | yes |
| clean loss | yes |
| ambiguous (stop+TP after entry) | counted as loss in headline (conservative model) |
| **intrabar_entry_stop / intrabar_entry_tp** (new) | **counted with current outcome in headline**, but flagged for separate analysis. We do not silently exclude them — silently excluding would inflate WR. |
| expired flat | not counted in WR; counted as 0R |
| not_triggered | not counted in WR; counted as 0R |
| `signal_outcomes` row with `gap_slippage_*_pct > 0` annotation | counted with current outcome in headline |

## 8. Non-goals (explicit)

- We do **not** model bid-ask spread or fees.
- We do **not** model slippage in reported R (only flagged).
- We do **not** model partial position exits (TP1+remainder).
- We do **not** retroactively change historical `signal_outcomes` rows. New annotations apply forward only.
- We do **not** treat stock session times as a hard guard in code; we rely on the data source (yfinance) being session-correct.

## 9. Acceptance criteria for the PART 7 implementation
1. New annotation fields are populated on every fresh outcome row going forward.
2. Existing signal_outcomes rows are untouched.
3. Headline `track-signals` / `signal-stats` output is unchanged numerically (annotations only add visibility).
4. Tests confirm:
   - intrabar entry+stop sets the flag and still returns the conservative outcome.
   - intrabar entry+TP1 sets the flag and still returns the win.
   - gap slip annotations populate when low/high pierces >10% of risk past stop/TP.
   - pre-entry invalidation no longer sets `stop_hit=1` (cosmetic).
5. Documentation in this file matches code behavior exactly (kept in sync per fix-report).
