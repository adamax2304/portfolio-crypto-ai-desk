"""Volume profile (POC / HVN / LVN) from OHLCV+volume (PAPER analysis, read-only).

If volume is missing or there are too few candles, returns `supported=False` and
NO levels — never invents VP levels. Pure, no network.
"""
from __future__ import annotations

from typing import Any


def _hlcv(c) -> tuple[float, float, float, float]:
    if isinstance(c, dict):
        return (float(c.get("high", c.get("h", 0))), float(c.get("low", c.get("l", 0))),
                float(c.get("close", c.get("c", 0))), float(c.get("volume", c.get("v", 0) or 0)))
    # tuple [ts,o,h,l,c,v]
    v = float(c[5]) if len(c) > 5 and c[5] is not None else 0.0
    return float(c[2]), float(c[3]), float(c[4]), v


def volume_profile(candles: list, bins: int = 24, min_candles: int = 40) -> dict[str, Any]:
    """Histogram close-volume into price bins. Returns POC + top HVN/LVN."""
    if not candles or len(candles) < min_candles:
        return {"supported": False, "reason": "too few candles", "poc": None, "hvn": [], "lvn": []}
    rows = [_hlcv(c) for c in candles]
    if sum(v for *_h, v in rows) <= 0:
        return {"supported": False, "reason": "no volume data", "poc": None, "hvn": [], "lvn": []}
    prices = [c for _h, _l, c, _v in rows]
    lo, hi = min(prices), max(prices)
    if hi <= lo:
        return {"supported": False, "reason": "flat range", "poc": None, "hvn": [], "lvn": []}
    width = (hi - lo) / bins
    buckets = [0.0] * bins
    for _h, _l, c, v in rows:
        idx = min(bins - 1, int((c - lo) / width))
        buckets[idx] += v
    centers = [round(lo + (i + 0.5) * width, 10) for i in range(bins)]
    poc_i = max(range(bins), key=lambda i: buckets[i])
    total = sum(buckets) or 1.0
    ranked = sorted(range(bins), key=lambda i: buckets[i], reverse=True)
    hvn = [centers[i] for i in ranked[:3] if buckets[i] / total > 0.06]
    nonzero = [i for i in range(bins) if buckets[i] > 0]
    lvn = [centers[i] for i in sorted(nonzero, key=lambda i: buckets[i])[:3]] if nonzero else []
    return {"supported": True, "poc": centers[poc_i], "hvn": hvn, "lvn": lvn,
            "bins": bins, "reason": "ok"}
