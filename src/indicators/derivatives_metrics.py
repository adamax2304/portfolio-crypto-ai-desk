from __future__ import annotations


def interpret_oi_price_change(price_change_pct: float | None, oi_change_pct: float | None) -> str:
    if price_change_pct is None or oi_change_pct is None:
        return "data unavailable"
    if price_change_pct > 0 and oi_change_pct > 0:
        return "price up + OI up: trend confirmation, monitor crowding"
    if price_change_pct > 0 and oi_change_pct < 0:
        return "price up + OI down: likely short covering, weaker continuation"
    if price_change_pct < 0 and oi_change_pct > 0:
        return "price down + OI up: fresh shorts, possible squeeze later"
    if price_change_pct < 0 and oi_change_pct < 0:
        return "price down + OI down: deleveraging or long liquidation"
    return "neutral"
