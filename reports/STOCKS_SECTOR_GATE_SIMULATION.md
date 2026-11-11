# Stocks Sector-Aware Long-Gate — Simulation (READ-ONLY)

**Date:** 2026-06-03
**Window:** last 14 days. **Nature:** read-only. No scoring / thresholds /
live logic / DB changed. Source: `scripts/_sector_diag.py`.

## Population

Actionable **A/B-tier LONG** stock signals (the only set a sector gate would
affect — C-tier is watchlist-only and never alerted):

```
CURRENT A/B longs: n=641 · triggered=440 · wins=119 · losses=74
                   avgR=+0.273 · totR=+120.0R · PF=2.62 · stop%=18 · tp1%=27
```

**Data coverage in the population:**
- stock **RS vs SPY**: **641/641 (100 %)**
- stock **RS vs sector ETF**: 246/641 (38 %)
- sector-ETF RS vs SPY (for the spec's "sector RS > 0" / "laggard bucket"):
  **only 2 sectors** (tech, semis) — **insufficient** to back-test the
  sector-level clauses (see diagnostic report).

Because the spec's sector-RS clauses are not reconstructable from the DB, the
variants were re-based on the **stock-level RS that IS reliably stored**, using
the stock's RS-vs-sector-ETF (`rs_sec`) as the available proxy for "weak
relative to its sector". Signals with no parsed RS are **kept** (never
penalised on missing data).

## Variants tested

| Variant | Rule (keep A/B long iff) |
|---|---|
| **A — strict** | stock RS vs SPY > 0 **and** RS vs sector ETF > 0 |
| **B — moderate** | stock RS vs SPY > 0 |
| **C — catalyst exception** | stock RS vs SPY > 0 **or** fresh catalyst present |

## Results

| Variant | kept n | kept totR | kept PF | removed n | winners removed | losers removed | NET totR Δ |
|---|---|---|---|---|---|---|---|
| **A** | 641 | +120.0 | 2.62 | **0** | 0 | 0 | **+0.0** |
| **B** | 641 | +120.0 | 2.62 | **0** | 0 | 0 | **+0.0** |
| **C** | 641 | +120.0 | 2.62 | **0** | 0 | 0 | **+0.0** |

**Every variant removes nothing.** Reason, confirmed directly:

- **100 % of A/B longs already have RS vs SPY > 0.**
- A/B longs split by stock-vs-own-sector RS:
  ```
  rs_sec > 0 : n=145  totR=+23.0  avgR=+0.159
  rs_sec < 0 : n=0    totR= +0.0           ← NONE exist
  rs_sec None: n=295  totR=+97.0  avgR=+0.329
  ```
  **No A/B long ever lagged its own sector (`rs_sec<0` ⇒ 0 signals).**

The existing scoring already enforces positive relative strength (RS is a
scored component; weak-RS names are demoted to C before they can alert). A
sector-aware long gate therefore has **nothing left to filter** in the
actionable set — net benefit **0R, PF unchanged 2.62**.

The earlier sector-RS variant (requiring sector-ETF RS > 0) actively **hurt**
(−82R, PF 2.62→1.79) purely because sector-RS was unknown for SMCI/LLY/etc. and
wrongly excluded those **winners** — an artifact of missing data, not a real
signal. That confirms a sector-RS gate is both un-backtestable and risky here.

## Where the drag actually is (from the diagnostic)

- **C-tier** −21R / PF 0.68 — and the symbol bleeders (XLV −23, IWM −11,
  AMZN −11, XLY −10) are **~100 % C-tier**, i.e. already non-actionable and
  never Telegram-alerted. They drag the *headline* weekly PF only because the
  stat **includes C-tier**.
- **swing mode** −6R (small sample).
- **AAPL** −13R — the one real A/B bleeder; a leader-sector stock that was
  RS-positive at entry then rolled over intraday. Not a sector problem and not
  catchable by an RS-at-entry gate.

---

# PART 3 — Recommendation

## ✅ Option 4 — Do NOT implement the sector-aware gate. The issue is C-tier / stat-reporting noise, not weak-sector A/B longs.

Justification:
1. The actionable A/B long set is **healthy** (+120R, PF 2.62) and **already
   100 % RS-positive vs SPY**, with **zero** signals lagging their own sector.
2. All three gate variants remove **0** signals → **0R / 0 PF** benefit.
3. The perceived PF drop (weekly 1.70→1.49) is dominated by **C-tier watchlist
   signals counted in the headline stat** (−21R) plus a small swing drag and
   one A/B name (AAPL). None of these is a "broad longs into weak sectors"
   problem — the gate's premise does not hold in the data.
4. The sector-RS data required to even build the spec'd gate is **not stored**
   per signal (only tech/semis), so it cannot be validly back-tested today.

**Net: implementing the gate would add complexity + risk (it mis-fires on
missing sector-RS data) for no measured gain.**

## Smaller, optional follow-ups (NOT the sector gate, separate decisions)

- **(R1) Headline PF should report A/B-only** (exclude C-tier watchlist from the
  dashboard/`signal-stats` headline, or show A/B and "incl. C" separately).
  C-tier is non-actionable and never alerted, yet it drags the perceived number
  — this is a **reporting** change, not a scoring change. Highest-value, lowest-risk.
- **(R2) Swing mode** (−6R, n=57) — monitor; revisit with more data.
- **(R3) AAPL-type A/B rollovers** — separate intraday-exit / tighter-invalidation
  study; unrelated to sectors.

---

# PART 4 — Implementation plan

**Not applicable.** The simulation did **not** show improvement (0R across all
variants), so per the task's gating condition ("do not implement until the
simulation proves improvement"), **no sector-gate implementation plan is
proposed.** If you want to pursue **R1** (A/B-only headline PF — a pure
reporting change), that can be planned separately on request.

---

## Final answer

```
READY_FOR_SECTOR_GATE_DECISION
```

Recommended decision: **#4 — do not implement the sector-aware gate**
(drag is C-tier/stat-noise). Optional next step: **R1 reporting split**
(A/B-only headline PF), pending your approval.
