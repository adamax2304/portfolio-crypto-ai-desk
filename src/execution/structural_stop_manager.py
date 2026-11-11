"""Structural stop movement after TP1/TP2 (PAPER ONLY).

After a partial TP, move the protective stop to a STRUCTURAL level when one exists
(long: below a recent higher-low / support / VWAP; short: above a recent lower-high /
resistance / VWAP), else fall back to BE / +0.5R lock. Never moves the stop worse than
current protection, never beyond entry-logic (no looser than invalidation).

Read-model / accounting only — never places an order, never moves a production stop.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from src.analysis.market_structure_levels import structure_levels


@dataclass
class StopMove:
    previous_stop: float
    new_stop: float
    moved: bool
    stop_move_reason: str
    structure_used: str            # higher_low | lower_high | support | resistance | vwap | be | lock | none
    structure_confidence: float    # 0..1
    protection_r: float            # R locked by the new stop (>= 0 after TP)
    remaining_qty_affected: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _r(price, entry, risk, long):
    return ((price - entry) if long else (entry - price)) / risk if risk else 0.0


def structural_stop_after_tp(
    *,
    tp_index: int,                 # 1 after TP1, 2 after TP2
    entry: float,
    initial_stop: float,
    current_stop: float,
    direction: str = "long",
    candles: list | None = None,
    vwap: float | None = None,
    remaining_qty: float = 0.0,
    min_lock_r: float | None = None,
) -> StopMove:
    long = str(direction).lower() != "short"
    risk = abs(entry - initial_stop)
    if risk <= 0:
        return StopMove(current_stop, current_stop, False, "invalid geometry", "none", 0.0, 0.0, remaining_qty)

    # candidate structural stops in the protected zone (between entry and TP direction)
    lv = structure_levels(candles or [], entry)
    cands: list[tuple[float, str, float]] = []   # (price, structure, confidence)
    if long:
        for s in lv.get("swing_lows", []):
            if s > current_stop and s < entry * 1.5:
                cands.append((s, "higher_low", 0.8))
        rl = lv.get("range_low")
        if rl is not None and rl > current_stop:
            cands.append((rl, "support", 0.6))
        if vwap is not None and vwap > current_stop and vwap < entry:
            cands.append((vwap, "vwap", 0.5))
    else:
        for s in lv.get("swing_highs", []):
            if s < current_stop and s > entry * 0.5:
                cands.append((s, "lower_high", 0.8))
        rh = lv.get("range_high")
        if rh is not None and rh < current_stop:
            cands.append((rh, "resistance", 0.6))
        if vwap is not None and vwap < current_stop and vwap > entry:
            cands.append((vwap, "vwap", 0.5))

    # default fallback: BE after TP1, +0.5R lock after TP2 (or min_lock_r)
    fb_r = 0.0 if tp_index <= 1 else 0.5
    if min_lock_r is not None:
        fb_r = max(fb_r, min_lock_r)
    fallback = entry + (fb_r * risk if long else -fb_r * risk)

    # choose the structural candidate that gives the best (highest for long) protection
    # but not beyond a sane ceiling; must be better than current stop.
    best = None
    for price, struct, conf in cands:
        prot_r = _r(price, entry, risk, long)
        if prot_r < (fb_r - 1e-9):   # structure weaker than fallback → skip
            continue
        better_than_cur = (price > current_stop) if long else (price < current_stop)
        if not better_than_cur:
            continue
        if best is None or (price > best[0] if long else price < best[0]):
            best = (price, struct, conf, prot_r)

    if best is not None:
        new_stop, struct, conf, prot_r = best
        reason = f"after TP{tp_index} → {struct} at {prot_r:+.2f}R (structural protection)"
    else:
        new_stop, struct, conf, prot_r = fallback, ("be" if fb_r == 0 else "lock"), 0.4, fb_r
        reason = f"after TP{tp_index} → {struct} {prot_r:+.2f}R (no structure; fallback)"

    # never worse than current protection
    better = (new_stop > current_stop) if long else (new_stop < current_stop)
    if not better:
        return StopMove(current_stop, current_stop, False,
                        f"after TP{tp_index} → kept current (already better)", "none",
                        0.0, _r(current_stop, entry, risk, long), remaining_qty)
    return StopMove(round(current_stop, 10), round(new_stop, 10), True, reason, struct,
                    round(conf, 3), round(prot_r, 3), remaining_qty)
