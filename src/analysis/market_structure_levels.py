"""Market-structure level extraction (PAPER analysis, read-only).

From an OHLCV window, find swing highs/lows, recent range bounds, prior-session
high/low, and round numbers. No production impact — used by the paper structural
TP engine. Pure (takes candle dicts/tuples), no network.
"""
from __future__ import annotations

import math
from typing import Any


def _ohlc(c) -> tuple[float, float, float, float]:
    """Accept dict {open,high,low,close} or tuple/list [ts,o,h,l,c,...]."""
    if isinstance(c, dict):
        return float(c.get("open", c.get("o", 0))), float(c.get("high", c.get("h", 0))), \
               float(c.get("low", c.get("l", 0))), float(c.get("close", c.get("c", 0)))
    return float(c[1]), float(c[2]), float(c[3]), float(c[4])


def swing_levels(candles: list, left: int = 2, right: int = 2) -> tuple[list[float], list[float]]:
    """Pivot swing highs/lows (fractal): a high higher than `left`/`right` neighbours."""
    highs, lows = [], []
    n = len(candles)
    H = [_ohlc(c)[1] for c in candles]
    L = [_ohlc(c)[2] for c in candles]
    for i in range(left, n - right):
        if H[i] == max(H[i - left:i + right + 1]):
            highs.append(round(H[i], 10))
        if L[i] == min(L[i - left:i + right + 1]):
            lows.append(round(L[i], 10))
    return sorted(set(highs)), sorted(set(lows))


def round_number_levels(price: float) -> list[float]:
    if price <= 0:
        return []
    mag = 10 ** math.floor(math.log10(price))
    out = []
    for m in (mag * 0.1, mag * 0.5, mag, mag * 2, mag * 5):
        if m <= 0:
            continue
        base = math.floor(price / m) * m
        out += [base, base + m]
    return sorted(set(round(x, 10) for x in out if x > 0))


def structure_levels(candles: list, entry: float, window: int = 120) -> dict[str, Any]:
    """Aggregate structural levels around `entry` from the last `window` candles."""
    if not candles:
        return {"all": [], "swing_highs": [], "swing_lows": [], "range_high": None,
                "range_low": None, "round_numbers": round_number_levels(entry)}
    cs = candles[-window:]
    hi, lo = swing_levels(cs)
    H = [_ohlc(c)[1] for c in cs]
    L = [_ohlc(c)[2] for c in cs]
    rng_high, rng_low = (round(max(H), 10), round(min(L), 10)) if H else (None, None)
    rounds = round_number_levels(entry)
    allv = sorted(set([x for x in (hi + lo + rounds + ([rng_high, rng_low] if rng_high else [])) if x]))
    return {"all": allv, "swing_highs": hi, "swing_lows": lo,
            "range_high": rng_high, "range_low": rng_low, "round_numbers": rounds}
