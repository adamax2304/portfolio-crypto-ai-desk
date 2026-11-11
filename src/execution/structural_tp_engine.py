"""Structural TP engine for PAPER trades (read-model / paper-only).

Generates `paper_structural_tp1/2/3` from real chart structure (swing H/L,
range bounds, round numbers, volume-profile POC/HVN/LVN) instead of the
production mechanical ATR ladder. Production TP generation is UNCHANGED — the
mechanical TPs stay as `mechanical_tp*`; these are paper-only proposals.

Never invents volume-profile levels (supported=False → none). Falls back to ATR
only when no structure exists (labelled STRUCTURAL_FALLBACK_ATR). If even the
fallback isn't viable after fees → NO_VALID_TP.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from src.analysis.market_structure_levels import structure_levels
from src.analysis.volume_profile import volume_profile

_TP3_RUNNER_PLAYBOOKS = {
    "crypto_swing_narrative_rs_momentum", "crypto_failed_bounce_short",
    "crypto_intraday_catalyst_or_momentum",
}
_CHOP_REGIMES = {"chop", "range/chop", "transition", "mixed", "range"}


@dataclass
class StructuralTP:
    tp_set_label: str            # STRUCTURAL | HYBRID | STRUCTURAL_FALLBACK_ATR | NO_VALID_TP
    tp1: float | None
    tp2: float | None
    tp3: float | None
    tp1_r: float | None
    tp2_r: float | None
    tp3_r: float | None
    tp1_source: str
    tp2_source: str
    tp3_source: str
    confidence: float            # 0..100
    volume_profile_supported: bool
    reasons: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _r(price, entry, risk, long):
    if price is None or risk <= 0:
        return None
    return round(((price - entry) if long else (entry - price)) / risk, 3)


def generate_structural_tps(
    *,
    entry: float,
    stop: float,
    direction: str = "long",
    candles: list | None = None,
    atr: float | None = None,
    market_regime: str | None = None,
    playbook: str | None = None,
    mechanical_tp1: float | None = None,
    mechanical_tp2: float | None = None,
    mechanical_tp3: float | None = None,
    min_tp1_r_after_fees: float = 0.60,
    fee_r_buffer: float = 0.0,
    max_tp_r: float = 15.0,
) -> StructuralTP:
    long = str(direction).lower() != "short"
    risk = abs(entry - stop)
    reasons: list[str] = []
    warnings: list[str] = []
    if risk <= 0 or entry <= 0:
        return StructuralTP("NO_VALID_TP", None, None, None, None, None, None,
                            "none", "none", "none", 0.0, False, reasons,
                            ["invalid geometry"])

    have_candles = bool(candles)
    lv = structure_levels(candles or [], entry)
    vp = volume_profile(candles or []) if candles else {"supported": False, "poc": None, "hvn": [], "lvn": []}
    vp_supported = bool(vp.get("supported"))

    # candidate levels in the profit direction, beyond a minimum R and within max_tp_r.
    min_dist = risk * (min_tp1_r_after_fees + fee_r_buffer)
    max_dist = risk * max_tp_r
    structural_pool: list[tuple[float, str]] = []
    for s in lv.get("swing_highs" if long else "swing_lows", []):
        structural_pool.append((s, "swing"))
    rb = lv.get("range_high") if long else lv.get("range_low")
    if rb is not None:
        structural_pool.append((rb, "range_bound"))
    # round numbers only meaningful WITH chart context (too coarse standalone)
    if have_candles:
        for r in lv.get("round_numbers", []):
            structural_pool.append((r, "round_number"))
    if vp_supported:
        for p in ([vp["poc"]] + (vp.get("hvn") or [])):
            if p is not None:
                structural_pool.append((p, "volume_profile"))

    # keep only levels in profit direction within [min_dist, max_dist], sorted by distance
    cands = []
    for price, src in structural_pool:
        if price is None:
            continue
        d = abs(price - entry)
        favorable = (price > entry + min_dist) if long else (price < entry - min_dist)
        if favorable and d <= max_dist:
            cands.append((d, price, src))
    cands.sort()

    chop = any(c in (market_regime or "").lower() for c in _CHOP_REGIMES)
    runner_ok = (playbook in _TP3_RUNNER_PLAYBOOKS) and not chop

    if cands:
        tp1, s1 = cands[0][1], cands[0][2]
        tp2, s2 = (cands[1][1], cands[1][2]) if len(cands) > 1 else (None, "none")
        tp3, s3 = (None, "none")
        if len(cands) > 2 and (runner_ok or cands[2][2] in ("volume_profile", "round_number", "swing")):
            tp3, s3 = cands[2][1], cands[2][2]
        elif not runner_ok:
            warnings.append("TP3 omitted: not a trend-runner/HTF-liquidity setup or chop regime.")
        # fill TP2 from ATR if only one structural level found
        label = "STRUCTURAL"
        if tp2 is None and atr:
            tp2 = entry + (2 * atr if long else -2 * atr)
            s2 = "atr_extension_2x"
            label = "HYBRID"
        confidence = min(100.0, 35.0 * sum(1 for s in (s1, s2, s3) if s in
                         ("swing", "range_bound", "volume_profile", "round_number")))
        reasons.append(f"TP1 {s1}, TP2 {s2}, TP3 {s3}")
        if vp_supported:
            reasons.append("volume profile supported (POC/HVN used where closer)")
        else:
            reasons.append("volume_profile_supported=false (not invented)")
        return StructuralTP(label, _round(tp1), _round(tp2), _round(tp3),
                            _r(tp1, entry, risk, long), _r(tp2, entry, risk, long),
                            _r(tp3, entry, risk, long), s1, s2, s3, confidence,
                            vp_supported, reasons, warnings)

    # fallback: ATR ladder (only if viable after fees)
    if atr:
        tp1 = entry + (1 * atr if long else -1 * atr)
        if _r(tp1, entry, risk, long) is not None and _r(tp1, entry, risk, long) >= min_tp1_r_after_fees:
            tp2 = entry + (2 * atr if long else -2 * atr)
            tp3 = entry + (3 * atr if long else -3 * atr) if runner_ok else None
            warnings.append("no structural level → STRUCTURAL_FALLBACK_ATR")
            return StructuralTP("STRUCTURAL_FALLBACK_ATR", _round(tp1), _round(tp2), _round(tp3),
                                _r(tp1, entry, risk, long), _r(tp2, entry, risk, long),
                                _r(tp3, entry, risk, long), "atr_extension_1x",
                                "atr_extension_2x", "atr_extension_3x" if tp3 else "none",
                                10.0, vp_supported, reasons, warnings)
    warnings.append("no structural level and ATR fallback not viable after fees")
    return StructuralTP("NO_VALID_TP", None, None, None, None, None, None,
                        "none", "none", "none", 0.0, vp_supported, reasons, warnings)


def _round(v):
    return round(v, 10) if v is not None else None
