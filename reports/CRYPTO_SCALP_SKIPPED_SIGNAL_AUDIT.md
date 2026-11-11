# Crypto Scalp — Skipped-Signal Audit (PART 1)

**Date:** 2026-06-15 · Read-only. Source: `proposed_signals` × latest `signal_outcomes`, crypto mode=scalp, tier A/B.

## 1. Status breakdown by window

| Window | n | triggered | non-trig/stale/skip | W | L | raw R |
|---|---:|---:|---:|---:|---:|---:|
| 48h | 46 | 19 (41%) | 27 (59%) | 2 | 1 | +1.0 |
| 7d | 73 | 28 (38%) | 45 (62%) | 2 | 2 | +0.0 |
| 14d | 114 | 54 (47%) | 60 (53%) | 2 | 9 | −7.0 |
| all | 125 | 61 (49%) | 64 (51%) | 2 | 10 | −8.0 |

All-time status distribution: `expired=48, stale_before_entry=35, missed_no_entry=22, stopped=10, waiting=8, entry_moved_away=1, tp1_hit=1`.

## 2. Triggered-trade quality (all-time, n=61)

| Metric | Value |
|---|---:|
| avg MFE | **+0.559R** |
| avg MAE | **−0.51R** |
| expired flat (triggered) | **49 / 61** |
| of those, reached ≥ +0.5R MFE before expiring | **27** |
| clean wins (tp) | 2 |
| clean losses (stop) | 10 |

## 3. The core finding

Scalp's **entry edge is real but its exit is broken**:
- A triggered scalp reaches **+0.56R favorable on average** — the entry is not random.
- But TP1 sits at **+1R with a ~2h validity horizon**, so **49 of 61 triggered trades expire flat** (0R) before reaching TP1. 27 of those touched +0.5R first.
- Net result is slightly negative (−8R all-time) driven by 10 stops vs 2 captured wins.

This is a **TP/horizon mismatch**, not an entry-quality problem — consistent with every prior scalp audit.

## 4. Skip / stale rate interpretation

- 51% all-time non-triggered (stale/missed/moved-away/waiting). The user's "80-90%" perception over-states it, but on a bad 48h it climbs to ~59%.
- High skip rate is **expected for a zone-fill scalp model in chop** — the pending revalidator kills setups that drift before fill. PART 2 tests whether those skips were protective.

## 5. Data limitation

1m candle archive is **rolling ~3.7h only**. Any exit-policy conclusion (e.g. TP1@+0.5R) cannot be validated at true 1m fidelity → all such results are LOW-CONFIDENCE / NEED_MORE_1M_DATA.
