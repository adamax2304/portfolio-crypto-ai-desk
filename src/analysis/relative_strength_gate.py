"""Relative-strength leader gate (PART 20, 2026-06-03).

Problem the audit surfaced: in ``bearish trend`` / ``high-volatility danger``
regimes the desk produced **zero** long signals for days, because the
technical-setup agent stamped *every* long with
"Long setup conflicts with current market regime." and the risk agent piled
on a flat +25 risk. That is correct for a coin merely drifting with a falling
BTC — but it is exactly **wrong** for a coin that is *rising against* a weak
BTC tape (e.g. NEAR +10% / RS vs BTC +13% while BTC is in a downtrend).
A coin defying the tape is showing relative strength, not conflicting with it.

This module centralises the single definition of a "relative-strength leader"
so the technical-setup, risk and scoring agents all agree on who qualifies.

A leader is **not** given a free pass: downstream it is still
* capped at B-tier (counter-trend — never a clean A against the broad tape),
* charged a reduced-but-non-zero risk penalty, and
* subject to the normal overextension / invalidation / liquidity gates.

The gate is pure and side-effect free.
"""

from __future__ import annotations

from typing import Any


DEFAULT_MIN_RS_BTC = 5.0
DEFAULT_REQUIRE_POSITIVE_24H = True


def is_relative_strength_leader(
    candidate: Any,
    *,
    min_rs_btc: float = DEFAULT_MIN_RS_BTC,
    require_positive_24h: bool = DEFAULT_REQUIRE_POSITIVE_24H,
) -> bool:
    """Return True iff *candidate* is rising against a weak BTC tape.

    Conditions:
      1. ``relative_strength_btc`` >= ``min_rs_btc`` (default +5%). The coin
         is meaningfully outperforming BTC over the momentum window.
      2. (when ``require_positive_24h``) ``return_24h`` > 0 — the coin is
         *actually rising*, not merely "falling less than BTC". This is the
         difference between a genuine outlier and a slow bleed.

    ``candidate`` is a ``MomentumCandidate`` (or any object exposing the two
    attributes). ``None`` / missing data → not a leader (fail safe).
    """

    if candidate is None:
        return False
    rs = getattr(candidate, "relative_strength_btc", None)
    if rs is None:
        return False
    try:
        if float(rs) < float(min_rs_btc):
            return False
    except (TypeError, ValueError):
        return False
    if require_positive_24h:
        ret24 = getattr(candidate, "return_24h", None)
        if ret24 is None:
            return False
        try:
            if float(ret24) <= 0:
                return False
        except (TypeError, ValueError):
            return False
    return True


def is_trend_aligned_short(
    candidate: Any,
    regime: Any,
    *,
    max_rs_btc: float = DEFAULT_MIN_RS_BTC,
) -> bool:
    """Return True iff a short moves WITH a falling market (PART 21).

    The mirror of :func:`is_relative_strength_leader`. A short is
    "trend-aligned" — and therefore disciplined rather than a coin-flip — when:

      1. the broad tape is falling: ``regime.btc_trend`` is ``downtrend`` or
         ``transition_down``; and
      2. the candidate is not itself a strong outperformer (``relative_strength_btc``
         below ``max_rs_btc``) — we never classify a coin that is *rising* hard
         against BTC as a tape-aligned short.

    Used so a short pressing a weak coin in a *volatile bear* regime
    (``high-volatility danger`` with BTC in a downtrend) gets a reduced — not
    flat-+25 — risk penalty, matching how long leaders are treated.
    """

    if regime is None:
        return False
    btc_trend = (getattr(regime, "btc_trend", "") or "").strip().lower()
    if btc_trend not in {"downtrend", "transition_down"}:
        return False
    if candidate is not None:
        rs = getattr(candidate, "relative_strength_btc", None)
        try:
            if rs is not None and float(rs) >= float(max_rs_btc):
                return False
        except (TypeError, ValueError):
            pass
    return True


def gate_params(config: Any) -> dict[str, Any]:
    """Read gate thresholds from ``config.scoring['relative_strength_gate']``.

    Falls back to module defaults when the block or config is absent, so the
    gate works even if the YAML is missing the section.
    """

    block: dict[str, Any] = {}
    try:
        block = (config.scoring.get("relative_strength_gate") or {}) if config else {}
    except Exception:
        block = {}
    return {
        "min_rs_btc": float(block.get("min_rs_btc", DEFAULT_MIN_RS_BTC)),
        "require_positive_24h": bool(
            block.get("require_positive_24h", DEFAULT_REQUIRE_POSITIVE_24H)
        ),
    }
