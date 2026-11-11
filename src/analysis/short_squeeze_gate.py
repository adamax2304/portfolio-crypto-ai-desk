"""Crypto short squeeze-risk guard (PART 22, 2026-06-04).

Read-only diagnosis (`CRYPTO_SHORT_SQUEEZE_AND_SCAM_WICK_AUDIT.md`) found that
recent failed shorts were **late / thin / squeezed**, not mis-stopped:
  * BCH / DEXE / GPS — shorted into an active bounce (price above EMA20 / +1h).
  * SAHARA / OPG / DEXE / GPS — thin (<$15M 24h) and/or high upper-wick coins.
  * ETH — liquid control case, did NOT lose.
  * Stops were fine (2.4–4.5× the 90th-pctile upper wick) → do NOT widen stops.

This module is a **conservative safety layer**: it does NOT disable shorts, it
caps high-squeeze-risk shorts to **C / watchlist** (no A/B Telegram). Pure /
side-effect free; returns a verdict the scoring agent applies via its existing
cap mechanism. Longs are never touched (caller only invokes for direction=short).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# Default thresholds (override via config/scoring.yaml → short_squeeze_guard).
DEFAULTS = {
    "cap_to": 60.0,               # cap value → below b_tier(65) → C tier
    "bounce_1h_pct": 1.5,         # +1h return above this = active bounce
    "bounce_dist_atr": 0.5,       # price > this many ATR above EMA20 = bounced
    "min_quote_volume_usd": 15_000_000.0,
    "max_upper_wick_atr": 1.5,    # max upper wick / ATR over recent window
    "thin_volume_ratio": 0.6,     # relative-volume proxy for thin tape
    "exhaustion_dist_atr": -1.8,  # > this far below EMA20 = overextended down
    "exhaustion_24h_pct": -10.0,  # 24h drop beyond this = overextended down
}


@dataclass
class SqueezeVerdict:
    risk_score: float = 0.0
    flags: list[str] = field(default_factory=list)
    cap: bool = False
    cap_value: float | None = None
    cap_reason: str = ""
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "short_squeeze_risk_score": round(self.risk_score, 2),
            "short_squeeze_risk_flags": list(self.flags),
            "short_squeeze_cap_reason": self.cap_reason,
        }


def gate_params(config: Any) -> dict[str, Any]:
    block: dict[str, Any] = {}
    try:
        block = (config.scoring.get("short_squeeze_guard") or {}) if config else {}
    except Exception:
        block = {}
    out = dict(DEFAULTS)
    for k, v in (block or {}).items():
        if k in out and v is not None:
            try:
                out[k] = float(v)
            except (TypeError, ValueError):
                pass
    return out


def _f(obj: Any, name: str):
    v = getattr(obj, name, None)
    if v is None and isinstance(obj, dict):
        v = obj.get(name)
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


def assess_short_squeeze(
    candidate: Any,
    setup: Any = None,
    derivative: Any = None,
    *,
    params: dict[str, Any] | None = None,
) -> SqueezeVerdict:
    """Assess squeeze risk for a SHORT candidate. Caller guarantees direction==short.

    Caps (→ C) when any of: bounce, thin liquidity, high upper-wick, or
    no-derivatives-on-a-thin-tape. ``late_short_after_exhaustion`` alone is a
    WARNING (no cap) so liquid majors falling cleanly (e.g. ETH) are not capped
    merely for being a counter-tape short — it only contributes to a cap when
    combined with another risk flag.
    """
    p = params or DEFAULTS
    if candidate is None:
        return SqueezeVerdict()

    ret_1h = _f(candidate, "return_1h")
    ret_24h = _f(candidate, "return_24h")
    dist = _f(candidate, "distance_from_ema20_atr")
    vol_ratio = _f(candidate, "volume_ratio")
    qv = _f(candidate, "quote_volume_24h_usd")
    max_wick = _f(candidate, "upper_wick_atr_max")
    deriv_missing = (derivative is None) or (not getattr(derivative, "data_available", False))

    flags: list[str] = []

    bounce = (ret_1h is not None and ret_1h > p["bounce_1h_pct"]) or (
        dist is not None and dist > p["bounce_dist_atr"]
    )
    if bounce:
        flags.append("short_bounce_guard")

    thin = qv is not None and qv < p["min_quote_volume_usd"]
    if thin:
        flags.append("thin_liquidity_short_squeeze_risk")

    high_wick = max_wick is not None and max_wick > p["max_upper_wick_atr"]
    if high_wick:
        flags.append("high_upper_wick_short_squeeze_risk")

    no_deriv_thin = deriv_missing and (
        (qv is not None and qv < p["min_quote_volume_usd"] * 2)
        or (vol_ratio is not None and vol_ratio < p["thin_volume_ratio"])
    )
    if no_deriv_thin:
        flags.append("no_derivatives_thin_short")

    exhaustion = (dist is not None and dist < p["exhaustion_dist_atr"]) or (
        ret_24h is not None and ret_24h < p["exhaustion_24h_pct"]
    )
    if exhaustion:
        flags.append("late_short_after_exhaustion")

    cap_flags = [f for f in flags if f != "late_short_after_exhaustion"]
    cap = bool(cap_flags)
    risk_score = float(len(cap_flags)) + (0.5 if exhaustion else 0.0)

    verdict = SqueezeVerdict(risk_score=risk_score, flags=flags)
    if cap:
        verdict.cap = True
        verdict.cap_value = float(p["cap_to"])
        verdict.cap_reason = (
            "short squeeze risk → capped to C: " + ", ".join(cap_flags)
            + (" (+exhaustion)" if exhaustion else "")
        )
        verdict.note = (
            "Short capped to C: high squeeze risk (bounce / thin liquidity / "
            "high upper-wick). Wait for a failed retest / lower high before shorting."
        )
    elif exhaustion:
        verdict.note = (
            "late_short_after_exhaustion: price already overextended down — "
            "prefer a failed-bounce / lower-high retest over chasing the breakdown."
        )
    return verdict
