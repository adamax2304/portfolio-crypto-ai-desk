"""Setup detector — `stocks_swing_growth_breakout` ONLY (Phase 1, long-only, shadow research).

Applies market → sector → stock gates, then classifies one of four setup variants and attaches a
risk/exit plan. Pure function of a feature dict + context; no network, no DB, no side effects.
A record with `passed=False` still carries `rejection_reasons` (for the report's rejected view).
"""
from __future__ import annotations

from typing import Any

from . import PLAYBOOK, ASSET_CLASS, MODE, SETUP_VARIANTS
from .risk_plan import build_risk_plan


def _num(v):
    try:
        return None if v is None else float(v)
    except (TypeError, ValueError):
        return None


def _min_near_high(feats: dict) -> float | None:
    vals = [v for v in (feats.get("near_high") or {}).values() if v is not None]
    return min(vals) if vals else None


def _classify_variant(feats: dict, cfg: dict) -> tuple[str | None, dict]:
    """Return (variant, entry_zone) for the first enabled+matching setup, else (None, {})."""
    setups = cfg.get("setups") or {}
    last = _num(feats.get("last_close"))
    ema21, sma50 = _num(feats.get("ema21")), _num(feats.get("sma50"))
    hi20 = _num(feats.get("high_20"))
    vr = _num(feats.get("volume_ratio")) or 0.0
    atr = _num(feats.get("atr14")) or 0.0

    # breakout — close pushing to/through the 20D base high on expanding volume, not over-extended
    b = setups.get("breakout") or {}
    if b.get("enabled", True) and last and hi20:
        ext_atr = ((last - ema21) / atr) if (ema21 and atr) else 0.0
        if last >= hi20 * 0.995 and vr >= float(b.get("require_volume_ratio", 1.2)) \
                and ext_atr <= float(b.get("max_extension_atr", 2.0)):
            return "breakout", {"entry_low": round(hi20, 4), "entry_high": round(hi20 * 1.02, 4),
                                "entry_price": round(max(last, hi20), 4)}

    # pullback_21d_50d — holding/reclaiming the 21D EMA or 50D SMA, still above the MA
    p = setups.get("pullback_21d_50d") or {}
    if p.get("enabled", True) and last:
        d21 = feats.get("dist_to_ema21_pct")
        d50 = feats.get("dist_to_sma50_pct")
        near21 = d21 is not None and abs(d21) <= float(p.get("max_distance_to_ema21_pct", 3.0))
        near50 = d50 is not None and abs(d50) <= float(p.get("max_distance_to_sma50_pct", 5.0))
        above = (not p.get("require_close_above_ma", True)) or (
            (ema21 and last > ema21) or (sma50 and last > sma50))
        if (near21 or near50) and above:
            zlo = min([x for x in (ema21, sma50) if x] or [last]) * 0.99
            return "pullback_21d_50d", {"entry_low": round(zlo, 4), "entry_high": round(last, 4),
                                        "entry_price": round(last, 4)}

    # reclaim_after_shakeout — dipped below the 50D then closed back above it
    r = setups.get("reclaim_after_shakeout") or {}
    if r.get("enabled", True) and last and sma50:
        swing_low = _num(feats.get("swing_low_10"))
        if last > sma50 and swing_low is not None and swing_low < sma50:
            return "reclaim_after_shakeout", {"entry_low": round(sma50, 4), "entry_high": round(last, 4),
                                              "entry_price": round(last, 4)}

    # consolidation_continuation — tight range near highs then a push up
    cc = setups.get("consolidation_continuation") or {}
    if cc.get("enabled", True) and last and hi20 and atr:
        rng = hi20 - (_num(feats.get("swing_low_20")) or hi20)
        if rng / atr <= float(cc.get("max_range_atr", 2.5)) and last >= hi20 * 0.98:
            return "consolidation_continuation", {"entry_low": round(hi20, 4),
                                                  "entry_high": round(hi20 * 1.02, 4),
                                                  "entry_price": round(max(last, hi20), 4)}
    return None, {}


def _score(feats: dict, variant: str, market_ok: bool, sector_ctx: dict) -> int:
    s = 40
    rs = _num(feats.get("rs_spy"))
    if rs is not None:
        s += min(20, max(0, int(rs * 200)))                 # +0.10 RS ≈ +20
    vr = _num(feats.get("volume_ratio"))
    if vr is not None:
        s += min(12, max(0, int((vr - 1.0) * 24)))          # 1.5x ≈ +12
    nh = _min_near_high(feats)
    if nh is not None:
        s += max(0, int(12 - nh))                           # right at a high ≈ +12
    if feats.get("above_50d") and feats.get("above_200d"):
        s += 8
    if sector_ctx.get("sector_rs_positive"):
        s += 4
    if variant in ("breakout", "consolidation_continuation"):
        s += 4
    return int(max(0, min(100, s)))


def _confidence(feats: dict) -> float:
    keys = ("sma50", "sma200", "atr14", "volume_ratio", "rs_spy", "ema21")
    present = sum(1 for k in keys if feats.get(k) is not None)
    base = present / len(keys)
    if (feats.get("bars") or 0) >= 200:
        base = min(1.0, base + 0.1)
    return round(base, 3)


def detect(symbol: str, feats: dict, *, market_ctx: dict, sector_ctx: dict,
           cfg: dict, equity_usd: float, earnings_risk: str | None = None) -> dict[str, Any]:
    reasons: list[str] = []
    warnings: list[str] = []
    rejections: list[str] = []

    base = {
        "symbol": symbol, "asset_class": ASSET_CLASS, "mode": MODE, "playbook": PLAYBOOK,
        "direction": "long", "passed": False, "setup_variant": None,
        "reasons": reasons, "warnings": warnings, "rejection_reasons": rejections,
        "market_regime": market_ctx.get("label"), "sector": sector_ctx.get("sector"),
        "sector_etf": sector_ctx.get("sector_etf"),
        "rs_spy": feats.get("rs_spy"), "rs_sector": feats.get("rs_sector"),
        "volume_ratio": feats.get("volume_ratio"), "atr14": feats.get("atr14"),
        "dollar_volume_30d": feats.get("dollar_volume_30d"),
        "near_high_pct": _min_near_high(feats), "earnings_risk": earnings_risk,
        "score": 0, "data_confidence": _confidence(feats),
    }
    if not feats.get("available"):
        rejections.append(feats.get("reason") or "no features")
        return base

    mkt = cfg.get("market_filter") or {}
    sec = cfg.get("sector_filter") or {}
    stk = cfg.get("stock_filter") or {}
    uni = cfg.get("universe") or {}

    # ---- market gate (Phase 1 conservative: missing required regime data → REJECT) ----
    vix = _num(market_ctx.get("vix"))
    if vix is not None and vix > float(mkt.get("reject_if_vix_above", 30)):
        rejections.append(f"VIX {vix:.1f} > {mkt.get('reject_if_vix_above', 30)} (panic)")
    elif vix is not None and vix > float(mkt.get("warn_if_vix_above", 22)):
        warnings.append(f"VIX {vix:.1f} elevated")
    if mkt.get("require_spy_above_50d", True):
        v = market_ctx.get("spy_above_50d")
        if v is False:
            rejections.append("SPY below 50D (risk-off)")
        elif v is None:
            rejections.append("SPY 50D regime data unavailable")
    if mkt.get("reject_if_spy_below_200d", True):
        v = market_ctx.get("spy_above_200d")
        if v is False:
            rejections.append("SPY below 200D (hard risk-off)")
        elif v is None:
            rejections.append("SPY 200D regime data unavailable")
    if mkt.get("require_qqq_above_50d", False):
        v = market_ctx.get("qqq_above_50d")
        if v is False:
            rejections.append("QQQ below 50D")
        elif v is None:
            rejections.append("QQQ 50D regime data unavailable")

    # ---- sector gate (missing data on a mapped sector ETF → REJECT) ----
    sector_etf = sector_ctx.get("sector_etf")
    if sector_etf is None:
        warnings.append("no sector ETF mapped; sector gate skipped")
    else:
        if sec.get("require_sector_above_50d", True):
            v = sector_ctx.get("sector_above_50d")
            if v is False:
                rejections.append("sector ETF below 50D (breaking)")
            elif v is None:
                rejections.append("sector ETF 50D data unavailable")
        if sec.get("require_sector_rs_positive_vs_spy", True):
            v = sector_ctx.get("sector_rs_positive")
            if v is False:
                rejections.append("sector RS negative vs SPY")
            elif v is None:
                rejections.append("sector RS data unavailable")

    # ---- stock gate ----
    last = _num(feats.get("last_close"))
    if last is not None and last < float(uni.get("min_price", 10)):
        rejections.append(f"price ${last:.2f} < ${uni.get('min_price', 10)}")
    dv = _num(feats.get("dollar_volume_30d"))
    if dv is not None and dv < float(uni.get("min_avg_dollar_volume_30d", 25_000_000)):
        rejections.append(f"30d $vol ${dv/1e6:.0f}M < ${uni.get('min_avg_dollar_volume_30d')/1e6:.0f}M")
    if stk.get("require_above_50d", True):
        if feats.get("above_50d") is False:
            rejections.append("below 50D SMA")
        elif feats.get("above_50d") is None:
            rejections.append("insufficient history for 50D")
    if stk.get("require_above_200d", True):
        if feats.get("above_200d") is False:
            rejections.append("below 200D SMA")
        elif feats.get("above_200d") is None:
            rejections.append("insufficient history for 200D")
    rs_spy = _num(feats.get("rs_spy"))
    if stk.get("require_rs_positive_vs_spy", True):
        if rs_spy is None:
            rejections.append("RS vs SPY unavailable (data incomplete)")
        elif rs_spy <= 0:
            rejections.append("RS vs SPY not positive")
    if stk.get("require_rs_positive_vs_sector", False):
        rs_sec = _num(feats.get("rs_sector"))
        if rs_sec is None:
            rejections.append("RS vs sector unavailable (data incomplete)")
        elif rs_sec <= 0:
            rejections.append("RS vs sector not positive")
    vr = _num(feats.get("volume_ratio"))
    if vr is not None and vr < float(stk.get("min_volume_ratio", 1.1)):
        rejections.append(f"volume ratio {vr:.2f} < {stk.get('min_volume_ratio', 1.1)}")
    nh = _min_near_high(feats)
    if nh is not None and nh > float(stk.get("near_high_max_pct_below", 12)):
        rejections.append(f"{nh:.1f}% below nearest 3M/6M/52W high (> {stk.get('near_high_max_pct_below', 12)}%)")

    if rejections:
        return base

    # ---- setup classification + risk plan ----
    variant, zone = _classify_variant(feats, cfg)
    if not variant:
        rejections.append("no qualifying breakout/pullback/reclaim/continuation setup")
        return base

    plan = build_risk_plan(entry=zone["entry_price"], atr=_num(feats.get("atr14")) or 0.0,
                           swing_low=_num(feats.get("swing_low_20")) or _num(feats.get("swing_low_10")),
                           risk_cfg=cfg.get("risk") or {}, exits_cfg=cfg.get("exits") or {},
                           equity_usd=equity_usd)
    warnings.extend(plan.get("warnings") or [])
    if plan.get("rejected"):
        rejections.append(plan.get("rejection_reason") or "risk plan rejected")
        return base

    reasons.append(f"{variant} setup, above 50D & 200D")
    if rs_spy is not None and rs_spy > 0:
        reasons.append(f"RS vs SPY +{rs_spy*100:.1f}%")
    if nh is not None:
        reasons.append(f"{nh:.1f}% below a 3M/6M/52W high")
    if vr is not None:
        reasons.append(f"volume {vr:.2f}× 20d avg")
    # weekly 10W/30W context — Phase 1: confirming reason if present, warning if absent (non-blocking)
    if feats.get("weekly_above_30w") is None:
        warnings.append("weekly 10W/30W data unavailable (Phase 1: not blocking)")
    elif feats.get("weekly_above_30w") and feats.get("weekly_30w_slope_positive"):
        reasons.append("weekly above 30W with rising 30W")

    thesis = (f"{symbol}: growth-name in an uptrend (above 50D/200D) with positive RS and a "
              f"{variant} entry near highs; sector {'firm' if sector_ctx.get('sector_rs_positive') else 'mixed'}.")
    counter = ("Fails if the market rolls over (SPY<50D), the sector breaks, price loses the 50D, "
               "or an earnings/gap event invalidates the base. Legacy stocks swing/invest edge was "
               "negative — this is unproven shadow research until the forward evidence gate passes.")

    base.update({
        "passed": True, "setup_variant": variant,
        "score": _score(feats, variant, not rejections, sector_ctx),
        "entry_price": zone["entry_price"], "entry_low": zone["entry_low"], "entry_high": zone["entry_high"],
        "risk_plan": plan, "thesis": thesis, "counter_thesis": counter,
    })
    return base
