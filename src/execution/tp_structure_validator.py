"""Structural TP validator (PAPER / DISPLAY ONLY).

Labels whether TP1/TP2/TP3 sit near a real chart structure (swing high/low,
support/resistance, range boundary, round number, ATR extension, volume-profile
node when available) or are just a mechanical R/ATR ladder. Does NOT change TP
generation, routing, or execution — it only annotates + warns.

Context (2026-06-24 audit): production TPs are generated as a MECHANICAL ATR
ladder (`close ± 1/2/3·ATR`) in `src/agents/technical_setup_agent.py`; stops are
semi-structural (swing support/resistance, ATR fallback). No volume-profile
module exists yet → `volume_profile_supported = unknown` (never fabricated).
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

# playbooks where a far TP3 runner is structurally justifiable
_TP3_RUNNER_PLAYBOOKS = {
    "crypto_swing_narrative_rs_momentum", "crypto_failed_bounce_short",
    "crypto_intraday_catalyst_or_momentum",
}
_CHOP_REGIMES = {"chop", "range/chop", "transition", "mixed"}


@dataclass
class TPValidation:
    tp_quality_score: float            # 0..100
    tp_quality_label: str              # STRUCTURAL | MIXED | MECHANICAL_R_ONLY | UNKNOWN
    tp_is_mechanical_r_ladder: bool
    tp1_source: str
    tp2_source: str
    tp3_source: str
    tp_near_chart_level: bool
    nearest_structure_distance_pct: float | None
    volume_profile_supported: str      # yes | no | unknown
    tp_reasons: list[str]
    tp_warnings: list[str]
    tp3_allowed_reason: str | None
    tp3_warning: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _near(price: float, levels: list[float], tol_pct: float) -> tuple[bool, float | None, float | None]:
    """Closest level within tol_pct of price → (hit, level, dist_pct)."""
    best = None
    best_d = None
    for lv in levels or []:
        if lv is None or lv <= 0 or price <= 0:
            continue
        d = abs(price - lv) / price
        if best_d is None or d < best_d:
            best_d, best = d, lv
    if best_d is None:
        return False, None, None
    return (best_d <= tol_pct), best, best_d


def _round_number_levels(price: float) -> list[float]:
    """Psychological round numbers near a price (1/2/5 × power of 10)."""
    if price <= 0:
        return []
    import math
    mag = 10 ** math.floor(math.log10(price))
    out = []
    for m in (mag * 0.5, mag, mag * 2, mag * 5, mag * 0.1):
        if m <= 0:
            continue
        lo = math.floor(price / m) * m
        out += [lo, lo + m]
    return sorted(set(round(x, 10) for x in out if x > 0))


def validate_tps(
    *,
    entry: float,
    stop: float,
    tp1: float | None,
    tp2: float | None,
    tp3: float | None,
    direction: str = "long",
    atr: float | None = None,
    swing_levels: list[float] | None = None,    # swing highs/lows, support/resistance, range bounds
    volume_profile_levels: list[float] | None = None,
    market_regime: str | None = None,
    playbook: str | None = None,
    tol_pct: float = 0.004,                       # 0.4% "near a level"
) -> TPValidation:
    reasons: list[str] = []
    warnings: list[str] = []
    swing_levels = [s for s in (swing_levels or []) if s]
    vp_levels = [s for s in (volume_profile_levels or []) if s]
    vp_supported = "yes" if vp_levels else "unknown"   # no VP module yet → unknown, never "no-data fabricated"

    risk = abs(entry - stop) if (entry and stop) else None
    structural_levels = swing_levels + vp_levels + _round_number_levels(entry)

    def classify(tp: float | None, idx: int) -> tuple[str, float | None]:
        if tp is None:
            return "none", None
        hit_struct, lvl, d_struct = _near(tp, swing_levels + vp_levels, tol_pct)
        if hit_struct:
            return ("volume_profile" if lvl in vp_levels else "swing_or_sr"), d_struct
        hit_round, _, d_round = _near(tp, _round_number_levels(entry), tol_pct)
        if hit_round:
            return "round_number", d_round
        # ATR extension: tp ≈ entry ± k·ATR (k≈1..3)
        if atr and atr > 0:
            k = abs(tp - entry) / atr
            if any(abs(k - n) <= 0.25 for n in (1, 2, 3)):
                return f"atr_extension_{round(k)}x", None
        return "mechanical_r_ladder", None

    s1, d1 = classify(tp1, 1)
    s2, d2 = classify(tp2, 2)
    s3, d3 = classify(tp3, 3)
    sources = [s1, s2, s3]

    structural_hits = sum(1 for s in sources if s in ("swing_or_sr", "volume_profile", "round_number"))
    atr_hits = sum(1 for s in sources if s.startswith("atr_extension"))
    mech_hits = sum(1 for s in sources if s == "mechanical_r_ladder")
    dists = [d for d in (d1, d2, d3) if d is not None]
    nearest = round(min(dists), 6) if dists else None

    # quality score: structural strongest, ATR weak-structural, mechanical worst
    score = structural_hits * 30 + atr_hits * 12 + mech_hits * 0
    score = min(100.0, float(score))
    is_mech_ladder = (structural_hits == 0)   # nothing near a real level → pure ladder
    if structural_hits >= 2:
        label = "STRUCTURAL"
    elif structural_hits == 1 or (atr_hits >= 1 and structural_hits == 0 and mech_hits == 0):
        label = "MIXED"
    elif atr_hits + mech_hits >= 1:
        label = "MECHANICAL_R_ONLY"
    else:
        label = "UNKNOWN"

    if is_mech_ladder:
        warnings.append("TP levels are a mechanical ATR/R ladder (entry ± k·ATR) — "
                        "not validated against swing/liquidity/volume-profile structure.")
    if vp_supported == "unknown":
        reasons.append("volume_profile_supported=unknown (no volume-profile module yet — see proposal).")
    for i, s in enumerate((s1, s2, s3), 1):
        if s != "none":
            reasons.append(f"TP{i} source: {s}")

    # TP3 justification
    tp3_reason = None
    tp3_warn = None
    if tp3 is not None:
        pb = (playbook or "")
        regime = (market_regime or "").lower()
        runner_ok = pb in _TP3_RUNNER_PLAYBOOKS
        chop = any(c in regime for c in _CHOP_REGIMES)
        if s3 in ("swing_or_sr", "volume_profile", "round_number"):
            tp3_reason = f"TP3 near structure ({s3})"
        elif runner_ok and not chop:
            tp3_reason = f"TP3 runner allowed by playbook {pb}"
        else:
            tp3_warn = ("TP3 is a far mechanical extension with no structural basis and "
                        f"playbook/regime ({pb or 'n/a'}/{regime or 'n/a'}) does not justify a runner.")
            warnings.append(tp3_warn)

    _, _, nearest_any = _near(tp1 or entry, structural_levels, tol_pct=1.0)

    return TPValidation(
        tp_quality_score=score,
        tp_quality_label=label,
        tp_is_mechanical_r_ladder=is_mech_ladder,
        tp1_source=s1, tp2_source=s2, tp3_source=s3,
        tp_near_chart_level=structural_hits > 0,
        nearest_structure_distance_pct=nearest,
        volume_profile_supported=vp_supported,
        tp_reasons=reasons, tp_warnings=warnings,
        tp3_allowed_reason=tp3_reason, tp3_warning=tp3_warn,
    )
