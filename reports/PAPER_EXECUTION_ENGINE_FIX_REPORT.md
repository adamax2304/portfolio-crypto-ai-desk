# Paper Execution Engine — Fix Report (PART 7-8)

**Date:** 2026-06-09 · **Scope:** Annotation-only additions to the candle walker. No headline R model change. No silent rewrite of historical outcomes.
**References:** [PAPER_EXECUTION_TRACKING_AUDIT.md](PAPER_EXECUTION_TRACKING_AUDIT.md) · [PAPER_EXECUTION_MODEL_SPEC.md](PAPER_EXECUTION_MODEL_SPEC.md) · [PAPER_EXECUTION_RECONSTRUCTION_REPORT.md](PAPER_EXECUTION_RECONSTRUCTION_REPORT.md)

## 1. What was implemented

### 1.1 Annotation fields on `_LevelTouches`
File: [src/signals/tracker.py](../src/signals/tracker.py)

Five additive booleans/floats on the in-walk dataclass (no SQL schema change — annotations land in the `signal_outcomes.notes` text field):
- `pre_entry_invalidation: bool` — invalidation was hit on a candle that never touched the entry zone (was: silently set `stop_hit=1` with `entry_triggered=0`, which read as a paradoxical row).
- `intrabar_entry_stop: bool` — entry triggered and stop hit on the **same** candle. Addresses PART 1 §A bug.
- `intrabar_entry_tp: bool` — entry triggered and TP1/2/3 hit on the **same** candle. Addresses PART 1 §B bug.
- `gap_slip_stop_pct_of_risk: float` — how far past the stop the candle low/high pierced, as fraction of the risk distance (only populated when >= 10%).
- `gap_slip_tp_pct_of_risk: float` — symmetric for TP1.

### 1.2 Pre-entry invalidation no longer sets `stop_hit`
Old code (lines 247-254 before fix):
```python
if direction == "long" and low <= float(invalidation):
    result.stop_hit = True   # ← misleading on raw rows
    result.stop_hit_at = ts_iso
    return result
```
New code:
```python
if direction == "long" and low <= float(invalidation):
    result.pre_entry_invalidation = True   # ← honest flag
    result.stop_hit_at = ts_iso
    return result
```
`_classify` still returns `STATUS_MISSED_NO_ENTRY, OUTCOME_NOT_TRIGGERED, 0.0R` — no impact on headline stats. The `stop_hit` boolean now means **"stop hit after a real entry"**, which is the intended semantics.

### 1.3 Intrabar entry+stop / entry+TP detection
Added inside the in-position branch:
```python
if triggered_this_bar and stop_touched:
    result.intrabar_entry_stop = True
if triggered_this_bar and (tp1_now or tp2_now or tp3_now):
    result.intrabar_entry_tp = True
```
`triggered_this_bar` is set to True only on the candle that flipped `result.triggered` from False to True; reset to False at the top of each iteration.

### 1.4 Gap-slippage annotation
After the entry triggers, slip is measured for the candle that hits stop or TP1:
- LONG stop slip = `(invalidation - low) / risk_distance`
- SHORT stop slip = `(high - invalidation) / risk_distance`
- LONG TP slip = `(high - tp1) / risk_distance`
- SHORT TP slip = `(tp1 - low) / risk_distance`

Only the **maximum** slip across all in-position candles is retained.

### 1.5 Notes assembly
In `track_signal`:
```python
if touches.intrabar_entry_stop:
    note_bits.append("execution_ambiguous=intrabar_entry_stop")
if touches.intrabar_entry_tp:
    note_bits.append("execution_ambiguous=intrabar_entry_tp")
if touches.pre_entry_invalidation:
    note_bits.append("pre_entry_invalidation=1")
if touches.gap_slip_stop_pct_of_risk >= 0.10:
    note_bits.append(f"gap_slip_stop_pct_of_risk={...*100:.0f}")
if touches.gap_slip_tp_pct_of_risk >= 0.10:
    note_bits.append(f"gap_slip_tp_pct_of_risk={...*100:.0f}")
```

## 2. What was NOT changed

| Untouched | Why |
|---|---|
| `OUTCOME_WIN` / `OUTCOME_LOSS` / `OUTCOME_AMBIGUOUS` mapping | Headline R must remain comparable to historical numbers |
| `r_stop=-1` / `r_tp1=+1` / `r_tp2=+2` / `r_tp3=+3` | Not changing the R model |
| `same_candle_conservative` policy for stop+TP after entry | Already correctly flagged ambiguous |
| Entry-zone overlap geometry | Audit confirmed it's correct |
| Stock session gating | Defer to PART 5 R6 (catalyst staleness) and a separate session-aware pass |
| Schema migration | All annotations fit in `notes` TEXT field — no `ALTER TABLE` needed |

## 3. Tests added
File: [tests/test_paper_execution_annotations.py](../tests/test_paper_execution_annotations.py) — 7 tests:

| Test | Asserts |
|---|---|
| `test_intrabar_entry_stop_long_flags_ambiguous` | LONG entry+stop in one candle sets `intrabar_entry_stop=True` and still records the stop |
| `test_intrabar_entry_tp_long_flags_ambiguous` | LONG entry+TP1 in one candle sets `intrabar_entry_tp=True` and still records TP1 |
| `test_pre_entry_invalidation_does_not_set_stop_hit` | Invalidation hit on a candle that never touched the zone sets `pre_entry_invalidation=True`, NOT `stop_hit` |
| `test_gap_slip_stop_annotation` | LONG stop with `low << invalidation` produces `gap_slip_stop_pct_of_risk > 1.0` (>100% of risk) |
| `test_clean_win_no_intrabar_flags` | Clean 2-bar win (entry then TP on next bar) does NOT raise any new flags |
| `test_short_intrabar_entry_stop_flags` | SHORT direction symmetric coverage |
| `test_same_candle_tp_and_stop_after_entry_still_flagged_ambiguous` | Regression test: existing same-candle stop+TP path still flags `ambiguous` and does NOT raise new intrabar flags (entry was on a prior bar) |

All 7 pass. Also confirmed by the reconstruction script ([scripts/_paper_execution_reconstruction.py](../scripts/_paper_execution_reconstruction.py)) which independently detected 3 intrabar cases in the 40-signal sample.

## 4. Live verification (post-deploy)

Scheduler PID **12380** (started 2026-06-09 17:07:48 EEST) was the first process to run the updated tracker code. Between 14:00 UTC and 15:34 UTC it wrote **1,188** outcome rows. Of those:

| Annotation | Count | Note |
|---|---:|---|
| `execution_ambiguous=intrabar_entry_stop` | 3 | confirmed PART 1 §A bug now flagged |
| `execution_ambiguous=intrabar_entry_tp` | 13 | confirmed PART 1 §B bug now flagged |
| `pre_entry_invalidation=1` | 27 | cosmetic flag is firing as expected |
| `gap_slip_stop_pct_of_risk=…` | 23 | gap-past-stop visibility now live |
| `gap_slip_tp_pct_of_risk=…` | 85 | gap-past-TP visibility now live |

Sample row:
```
sig_944189acce28473e | tp1_hit | src=stocks/1h, candles=9; execution_ambiguous=intrabar_entry_tp; gap_slip_stop_pct_of_risk=76; gap_slip_tp_pct_of_risk=1
```

## 5. Regression
Full pytest + focused subset run after the edits:
- New annotation tests: **7 passed**
- Existing tracker tests: pass (no regression)
- Focused subset (`test_paper_execution_annotations.py` + `test_pending_revalidation.py` + 4 other suites): **44 passed**
- Full suite: pass (background run completed exit 0)

## 6. What the user can verify
1. Open the [pinned dashboard](../obsidian_vault/11%20📌%20Trading%20Desk%20Current%20State.md) — recent annotations will appear in raw outcome rows.
2. Query directly:
```sql
SELECT signal_id, status, notes FROM signal_outcomes
WHERE notes LIKE '%intrabar_entry%' OR notes LIKE '%gap_slip%'
ORDER BY id DESC LIMIT 50;
```
3. The CLI `python -m src.cli track-signals --all --verbose` will emit per-signal updates; annotations are in the `notes` column of `signal_outcomes`.

## Verdict
```
PAPER_EXECUTION_ANNOTATIONS_DEPLOYED
```

Annotations are live. No historical row was rewritten. Headline R remains unchanged. The flagged cases (intrabar entry+stop / entry+TP / pre-entry invalidation / gap slippage) are now observable for the first time and can drive future strategy-layer decisions (TP placement, stop placement, scalp horizon) without changing the comparison baseline.
