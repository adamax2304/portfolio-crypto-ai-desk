"""Deterministic setup detector for the Stocks Position Swing V2 shadow lane."""
from __future__ import annotations

from typing import Any

try:
    import pandas as pd
except Exception:  # pragma: no cover
    pd = None

from .v2_risk import build_plan

BREAKOUT_RETEST = "BREAKOUT_RETEST"
TREND_PULLBACK_RECLAIM = "TREND_PULLBACK_RECLAIM"


def _f(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def classify_market(market: dict[str, Any], cfg: dict[str, Any]) -> str:
    vix = _f(market.get("vix"))
    market_cfg = cfg.get("market") or {}
    if market.get("spy_above_200d") is False:
        return "risk_off"
    if vix is not None and vix >= float(market_cfg.get("risk_off_vix_above", 30)):
        return "risk_off"
    if (
        market.get("spy_above_50d") is True
        and market.get("spy_above_200d") is True
        and (vix is None or vix < float(market_cfg.get("warn_vix_above", 22)))
    ):
        return "risk_on"
    return "neutral"


def _bar_volume_ratio(df, idx: int, lookback: int = 20) -> float | None:
    if pd is None or df is None or len(df) < lookback + abs(idx):
        return None
    pos = len(df) + idx if idx < 0 else idx
    if pos < lookback:
        return None
    avg = float(df["volume"].iloc[pos - lookback:pos].mean())
    return float(df["volume"].iloc[pos]) / avg if avg > 0 else None


def _bullish_confirmation(row) -> bool:
    op, hi, lo, close = map(float, (row["open"], row["high"], row["low"], row["close"]))
    span = hi - lo
    return close > op and span > 0 and close >= lo + 0.6 * span


def _breakout_retest(df, feats: dict, setup_cfg: dict) -> dict[str, Any] | None:
    if pd is None or df is None:
        return None
    lookback = int(setup_cfg.get("base_lookback_days", 20))
    if len(df) < lookback + 3:
        return None
    atr = _f(feats.get("atr14"))
    if not atr or atr <= 0:
        return None

    base = df.iloc[-(lookback + 2):-2]
    breakout = df.iloc[-2]
    confirm = df.iloc[-1]
    level = float(base["high"].max())
    breakout_vr = _bar_volume_ratio(df, -2)
    tolerance = float(setup_cfg.get("retest_tolerance_atr", 0.35)) * atr
    max_extension = float(setup_cfg.get("max_extension_atr", 0.5)) * atr
    if float(breakout["close"]) < level:
        return None
    if breakout_vr is None or breakout_vr < float(setup_cfg.get("breakout_volume_ratio_min", 1.2)):
        return None
    if float(confirm["low"]) > level + tolerance:
        return None
    if float(confirm["close"]) < level or not _bullish_confirmation(confirm):
        return None
    if float(confirm["close"]) - level > max_extension:
        return None
    entry = float(confirm["high"]) + float(setup_cfg.get("entry_buffer_atr", 0.05)) * atr
    return {
        "setup_variant": BREAKOUT_RETEST,
        "entry_price": entry,
        "entry_low": level,
        "entry_high": entry,
        "structural_low": min(float(breakout["low"]), float(confirm["low"])),
        "trigger_level": level,
        "setup_volume_ratio": breakout_vr,
        "confirmation_date": str(df.index[-1]),
    }


def _pullback_reclaim(df, feats: dict, setup_cfg: dict) -> dict[str, Any] | None:
    if pd is None or df is None or len(df) < 55:
        return None
    atr = _f(feats.get("atr14"))
    if not atr or atr <= 0:
        return None
    prior = df.iloc[-2]
    confirm = df.iloc[-1]
    if not _bullish_confirmation(confirm):
        return None
    vr = _bar_volume_ratio(df, -1)
    if vr is None or vr < float(setup_cfg.get("confirmation_volume_ratio_min", 1.0)):
        return None

    tolerance = float(setup_cfg.get("touch_tolerance_atr", 0.25)) * atr
    max_extension = float(setup_cfg.get("max_extension_atr", 1.0)) * atr
    selected_name = None
    selected_level = None
    for name in setup_cfg.get("reclaim_levels", ["ema21", "sma50"]):
        level = _f(feats.get(name))
        if level is None:
            continue
        touched = min(float(prior["low"]), float(confirm["low"])) <= level + tolerance
        reclaimed = float(confirm["close"]) > level
        not_extended = float(confirm["close"]) - level <= max_extension
        if touched and reclaimed and not_extended:
            selected_name, selected_level = str(name), level
            break
    if selected_level is None:
        return None
    entry = float(confirm["high"]) + float(setup_cfg.get("entry_buffer_atr", 0.05)) * atr
    return {
        "setup_variant": TREND_PULLBACK_RECLAIM,
        "entry_price": entry,
        "entry_low": selected_level,
        "entry_high": entry,
        "structural_low": min(float(prior["low"]), float(confirm["low"])),
        "trigger_level": selected_level,
        "reclaim_level": selected_name,
        "setup_volume_ratio": vr,
        "confirmation_date": str(df.index[-1]),
    }


def _score(feats: dict[str, Any], setup: dict[str, Any], market_regime: str) -> int:
    score = 55
    rs_spy = _f(feats.get("rs_spy")) or 0.0
    rs_sector = _f(feats.get("rs_sector")) or 0.0
    score += min(14, max(0, int(rs_spy * 100)))
    score += min(10, max(0, int(rs_sector * 100)))
    score += min(10, max(0, int((float(setup.get("setup_volume_ratio") or 1.0) - 1.0) * 20)))
    if feats.get("weekly_30w_slope_positive"):
        score += 5
    if setup.get("setup_variant") == BREAKOUT_RETEST:
        score += 3
    if market_regime == "risk_on":
        score += 3
    return max(0, min(100, score))


def detect(
    symbol: str,
    df,
    feats: dict[str, Any],
    *,
    market_ctx: dict[str, Any],
    sector_ctx: dict[str, Any],
    earnings: dict[str, Any],
    event_ctx: dict[str, Any],
    cfg: dict[str, Any],
    data_ctx: dict[str, Any] | None = None,
) -> dict[str, Any]:
    strategy_id = str(cfg.get("strategy_id"))
    base = {
        "symbol": symbol,
        "asset_class": "stocks",
        "mode": "swing",
        "direction": "long",
        "strategy_id": strategy_id,
        "shadow_lane": cfg.get("shadow_lane"),
        "profile_version": cfg.get("profile_version"),
        "passed": False,
        "rejection_reasons": [],
        "warnings": [],
        "data_clean": True,
    }
    reject = base["rejection_reasons"]
    data_ctx = data_ctx or {}
    for reason in data_ctx.get("rejection_reasons", []):
        reject.append(str(reason))
    if data_ctx.get("clean") is False:
        base["data_clean"] = False
    if not feats.get("available"):
        reject.append("DATA_UNAVAILABLE")
        base["data_clean"] = False
        return base

    market_regime = classify_market(market_ctx, cfg)
    base["market_regime"] = market_regime
    market_policy = (cfg.get("market") or {}).get(market_regime) or {}
    if market_regime == "risk_off":
        reject.append("MARKET_RISK_OFF")

    if event_ctx.get("blocking"):
        reject.extend(f"BLOCKING_EVENT:{x}" for x in event_ctx.get("blocking_types", []))
    if event_ctx.get("event_data_unavailable"):
        reject.append("EVENT_DATA_UNAVAILABLE")
        base["data_clean"] = False
    if not earnings.get("calendar_available"):
        if (cfg.get("event_risk") or {}).get("require_earnings_calendar_available", True):
            reject.append("EARNINGS_CALENDAR_UNAVAILABLE")
            base["data_clean"] = False
    earnings_days = earnings.get("days")
    if earnings_days is not None and earnings_days <= int(
        (cfg.get("event_risk") or {}).get("earnings_block_trading_days", 7)
    ):
        reject.append("EARNINGS_WITHIN_HOLD_WINDOW")

    stock_cfg = cfg.get("stock_filter") or {}
    universe_cfg = cfg.get("universe") or {}
    last = _f(feats.get("last_close"))
    if last is None or last < float(universe_cfg.get("min_price", 10)):
        reject.append("PRICE_TOO_LOW")
    dv = _f(feats.get("dollar_volume_30d"))
    if dv is None or dv < float(universe_cfg.get("min_avg_dollar_volume_30d", 25_000_000)):
        reject.append("DOLLAR_VOLUME_TOO_LOW_OR_MISSING")
    if stock_cfg.get("require_above_50d", True) and feats.get("above_50d") is not True:
        reject.append("NOT_ABOVE_50D")
    if stock_cfg.get("require_above_200d", True) and feats.get("above_200d") is not True:
        reject.append("NOT_ABOVE_200D")
    if stock_cfg.get("require_weekly_above_30w", True) and feats.get("weekly_above_30w") is not True:
        reject.append("NOT_ABOVE_WEEKLY_30W")
    if stock_cfg.get("require_rs_positive_vs_spy", True) and (_f(feats.get("rs_spy")) or 0) <= 0:
        reject.append("RS_SPY_NOT_POSITIVE")
    if stock_cfg.get("require_rs_positive_vs_sector", True) and (_f(feats.get("rs_sector")) or 0) <= 0:
        reject.append("RS_SECTOR_NOT_POSITIVE")
    if sector_ctx.get("sector_above_50d") is not True:
        reject.append("SECTOR_NOT_ABOVE_50D")
    if sector_ctx.get("sector_rs_positive") is not True:
        reject.append("SECTOR_RS_NOT_POSITIVE")
    near_high = min((v for v in (feats.get("near_high") or {}).values() if v is not None), default=None)
    if near_high is None or near_high > float(stock_cfg.get("max_pct_below_52w_high", 15)):
        reject.append("TOO_FAR_FROM_HIGH")
    if reject:
        return base

    setups_cfg = cfg.get("setups") or {}
    setup = None
    breakout_cfg = setups_cfg.get("breakout_retest") or {}
    if breakout_cfg.get("enabled", True) and market_policy.get("allow_breakout_retest", False):
        setup = _breakout_retest(df, feats, breakout_cfg)
    pullback_cfg = setups_cfg.get("trend_pullback_reclaim") or {}
    if (
        setup is None
        and pullback_cfg.get("enabled", True)
        and market_policy.get("allow_trend_pullback_reclaim", False)
    ):
        setup = _pullback_reclaim(df, feats, pullback_cfg)
    if setup is None:
        reject.append("NO_CONFIRMED_V2_SETUP")
        return base

    plan = build_plan(
        entry=setup["entry_price"],
        atr=float(feats["atr14"]),
        structural_low=setup["structural_low"],
        size_weight=float(market_policy.get("size_weight", 1.0)),
        risk_cfg=cfg.get("risk") or {},
        exits_cfg=cfg.get("exits") or {},
    )
    if plan.get("rejected"):
        reject.append(str(plan.get("reason") or "RISK_PLAN_REJECTED"))
        base["risk_plan"] = plan
        return base

    base.update(
        passed=True,
        setup_variant=setup["setup_variant"],
        score=_score(feats, setup, market_regime),
        entry_price=setup["entry_price"],
        entry_low=setup["entry_low"],
        entry_high=setup["entry_high"],
        trigger_level=setup["trigger_level"],
        confirmation_date=setup["confirmation_date"],
        reclaim_level=setup.get("reclaim_level"),
        setup_volume_ratio=setup["setup_volume_ratio"],
        sector=sector_ctx.get("sector"),
        sector_etf=sector_ctx.get("sector_etf"),
        rs_spy=feats.get("rs_spy"),
        rs_sector=feats.get("rs_sector"),
        volume_ratio=feats.get("volume_ratio"),
        atr14=feats.get("atr14"),
        dollar_volume_30d=feats.get("dollar_volume_30d"),
        near_high_pct=near_high,
        earnings_days=earnings_days,
        event_types=event_ctx.get("event_types", []),
        risk_plan=plan,
        thesis=(
            f"{symbol} has a confirmed {setup['setup_variant']} in a {market_regime} market, "
            "with positive relative strength versus SPY and its sector."
        ),
        counter_thesis=(
            "Invalid if the confirmed level fails, the sector loses trend, a blocking corporate "
            "event appears, or the next-session entry requires an excessive chase."
        ),
    )
    return base
