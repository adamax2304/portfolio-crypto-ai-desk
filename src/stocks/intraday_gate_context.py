"""Builds the market/sector/liquidity/catalyst context that feeds the SI-1..SI-5 gates, from cached
OHLCV + already-computed idea fields. READ-MODEL only — loads data, computes nothing that trades.

Fail-conservative: if the confirming data is missing/stale, the produced status is unknown/stale so
the gates demote (never assume confirmation). Market context (SPY/QQQ) is cached for one UTC minute:
candidates in the same scoring batch share a read, while a newly closed benchmark bar can become
visible on the next minute instead of being hidden by an hour-long ``unknown`` cache entry.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from src.stocks import intraday_actionability_gates as _g

_MARKET_CACHE: dict = {}
_MARKET_CACHE_MAX_ENTRIES = 180
_NY = ZoneInfo("America/New_York")


def _fs():
    from src.config import load_config
    from src.storage.file_store import FileStore
    return FileStore(load_config())


def _load(fs, symbol, tf):
    try:
        df = fs.load_stocks_ohlcv(symbol, tf)
    except Exception:
        return None
    if df is None or getattr(df, "empty", True) or "timestamp" not in getattr(df, "columns", []):
        return None
    return df


def _rth_slice(df, now):
    """Rows visible at ``now`` from the current RTH day.

    The cached OHLCV archive can already contain bars after an injected ``now``
    (for example, while replaying a historical candidate).  Those future bars
    must never supply market context or make a historical decision look stale.
    """
    import pandas as pd
    d = df.copy()
    d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
    d = d.dropna(subset=["timestamp"]).sort_values("timestamp")
    as_of = pd.Timestamp(now)
    if as_of.tzinfo is None:
        as_of = as_of.tz_localize("UTC")
    else:
        as_of = as_of.tz_convert("UTC")
    # 15m timestamps mark bar OPEN. Only completed bars are decision evidence;
    # treating an in-progress row as closed inflated RVOL and made freshness
    # depend on the provider's partial-bar update behaviour.
    d = d[d["timestamp"] + pd.Timedelta(minutes=15) <= as_of]
    if d.empty:
        return d
    last_day = _ny_date(d["timestamp"].iloc[-1])
    ny = d["timestamp"].dt.tz_convert(_NY)
    minutes = ny.dt.hour * 60 + ny.dt.minute
    try:
        from src.stocks.market_calendar import us_cash_session_close
        close = us_cash_session_close(d["timestamp"].iloc[-1].to_pydatetime())
        close_ny = close.astimezone(_NY) if close is not None else None
        close_minutes = close_ny.hour * 60 + close_ny.minute if close_ny is not None else 16 * 60
    except Exception:
        close_minutes = 16 * 60
    rth = d[(ny.dt.date == last_day) & (minutes >= 9 * 60 + 30) & (minutes < close_minutes)]
    return rth.reset_index(drop=True)


def _ny_date(ts):
    """NY calendar date for a tz-aware datetime / pandas Timestamp (None-safe)."""
    if ts is None:
        return None
    dt = ts.to_pydatetime() if hasattr(ts, "to_pydatetime") else ts
    if getattr(dt, "tzinfo", None) is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(_NY).date()


def _market_context_stale(now, last_ts, cfg) -> bool:
    """Fresh market context must be from the CURRENT NY session and recent. A stale archive
    (e.g. yesterday's SPY/QQQ while today is RTH) must not look like a confirmed regime.
    Returns True → the gate demotes via market_context_unknown_or_stale."""
    if last_ts is None:
        return True
    # different NY trading day than `now` → stale (archive, pre-open, weekend/holiday carryover)
    if _ny_date(last_ts) != _ny_date(now):
        return True
    dt = last_ts.to_pydatetime() if hasattr(last_ts, "to_pydatetime") else last_ts
    if getattr(dt, "tzinfo", None) is None:
        dt = dt.replace(tzinfo=timezone.utc)
    # secondary age guard (lenient default so normal 15m cadence is not flagged)
    max_age = float(cfg.get("market_context_max_age_sec")
                    or cfg.get("max_data_age_sec") or 900)
    bar_closed_at = dt + timedelta(minutes=15)
    return (now - bar_closed_at).total_seconds() > max_age


def _return_and_vwap(df, now):
    day = _rth_slice(df, now)
    if day is None or len(day) < 2:
        return None, "unknown", None
    o = float(day["open"].iloc[0]) if "open" in day else float(day["close"].iloc[0])
    c = float(day["close"].iloc[-1])
    ret = ((c / o) - 1.0) * 100.0 if o else None
    tp = (day.get("high", day["close"]).astype(float) + day.get("low", day["close"]).astype(float)
          + day["close"].astype(float)) / 3.0
    vol = day.get("volume")
    vwap = float((tp * vol).sum() / vol.sum()) if vol is not None and float(vol.sum()) > 0 else float(tp.mean())
    pos = "above" if c >= vwap else "below"
    last_ts = day["timestamp"].iloc[-1]
    return ret, pos, last_ts


def _market_cache_key(now: datetime) -> tuple[str, int, int]:
    """One-minute cache key on the injected decision clock (UTC, replay-safe)."""
    moment = now if now.tzinfo is not None else now.replace(tzinfo=timezone.utc)
    moment = moment.astimezone(timezone.utc)
    return moment.date().isoformat(), moment.hour, moment.minute


def market_context(now, cfg) -> dict:
    """SPY + QQQ RTH return / vs-VWAP → intraday regime. Cached for one UTC minute."""
    key = _market_cache_key(now)
    if key in _MARKET_CACHE:
        return _MARKET_CACHE[key]
    fs = _fs()
    out = {"status": "unknown", "spy_rth_return_pct": None, "qqq_rth_return_pct": None,
           "spy_vs_vwap": "unknown", "qqq_vs_vwap": "unknown", "regime": "unknown",
           "market_context_age_status": "unknown", "spy_last_ts": None, "qqq_last_ts": None}
    got = 0
    last_ts_by_sym: dict[str, object] = {}    # per-symbol last bar — checked INDEPENDENTLY for freshness
    for sym, rk, vk, tk in (("SPY", "spy_rth_return_pct", "spy_vs_vwap", "spy_last_ts"),
                            ("QQQ", "qqq_rth_return_pct", "qqq_vs_vwap", "qqq_last_ts")):
        df = _load(fs, sym, "15m")
        if df is None:                       # explicit fallback — `df or _load(...)` raises on a DataFrame
            df = _load(fs, sym, "1h")
        if df is None:
            continue
        ret, pos, last_ts = _return_and_vwap(df, now)
        if ret is None:
            continue
        got += 1
        out[rk] = round(ret, 3)
        out[vk] = pos
        last_ts_by_sym[sym] = last_ts
        try:
            out[tk] = last_ts.isoformat() if last_ts is not None else None
        except Exception:
            out[tk] = str(last_ts) if last_ts is not None else None
    if got == 2:
        # Freshness FIRST, and per-symbol: SPY AND QQQ must BOTH be current-session + recent. A stale
        # leg (e.g. QQQ from yesterday while SPY is fresh) must NOT present as a confirmed regime — do
        # not take the newest of the two. Check every leg; the oldest stale one wins.
        all_fresh = all(not _market_context_stale(now, ts, cfg) for ts in last_ts_by_sym.values())
        if not all_fresh:
            out["status"] = "stale"
            out["market_context_age_status"] = "stale"
        else:
            out["market_context_age_status"] = "fresh"
            spy, qqq = out["spy_rth_return_pct"], out["qqq_rth_return_pct"]
            thr = float(cfg.get("index_return_conflict_pct", 0.15))
            if spy <= -thr and qqq <= -thr and out["spy_vs_vwap"] == "below":
                out["regime"] = "risk_off" if (spy <= -1.0 or qqq <= -1.2) else "trend_down"
            elif spy >= thr and qqq >= thr and out["spy_vs_vwap"] == "above":
                out["regime"] = "trend_up"
            else:
                out["regime"] = "chop"
            out["status"] = "ok"
    # Bound a long-lived monitor's cache. Entries are only one minute wide, so retaining the
    # newest few hours is sufficient and prevents unbounded growth.
    while len(_MARKET_CACHE) >= _MARKET_CACHE_MAX_ENTRIES:
        _MARKET_CACHE.pop(next(iter(_MARKET_CACHE)))
    _MARKET_CACHE[key] = out
    return out


def _intraday_rvol(frame, now):
    """Return time-of-day-normalised 15m RVOL and the last eligible bar."""
    import pandas as pd
    d = frame.copy()
    d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
    d = d.dropna(subset=["timestamp"]).sort_values("timestamp")
    as_of = pd.Timestamp(now)
    as_of = as_of.tz_localize("UTC") if as_of.tzinfo is None else as_of.tz_convert("UTC")
    d = d[d["timestamp"] + pd.Timedelta(minutes=15) <= as_of]
    if d.empty or "volume" not in d:
        return None, None
    ny = d["timestamp"].dt.tz_convert(_NY)
    mins = ny.dt.hour * 60 + ny.dt.minute
    try:
        from src.stocks.market_calendar import us_cash_session_close
        last_close = us_cash_session_close(d["timestamp"].iloc[-1].to_pydatetime())
        close_ny = last_close.astimezone(_NY) if last_close is not None else None
        close_minutes = close_ny.hour * 60 + close_ny.minute if close_ny is not None else 16 * 60
    except Exception:
        close_minutes = 16 * 60
    d = d[(mins >= 9 * 60 + 30) & (mins < close_minutes)].copy()
    if d.empty:
        return None, None
    ny = d["timestamp"].dt.tz_convert(_NY)
    last = d.iloc[-1]
    last_ny = last["timestamp"].tz_convert(_NY)
    same_slot_previous_days = (
        (ny.dt.hour == last_ny.hour)
        & (ny.dt.minute == last_ny.minute)
        & (ny.dt.date < last_ny.date())
    )
    baseline = d.loc[same_slot_previous_days, "volume"].astype(float).tail(20)
    if baseline.empty or float(baseline.mean()) <= 0:
        return None, last["timestamp"]
    return round(float(last["volume"]) / float(baseline.mean()), 4), last["timestamp"]


def liquidity_from_ohlcv(fs, symbol, setup, now, cfg) -> dict:
    """RVOL / dollar-volume / spread-proxy / freshness from the stock's own 15m OHLCV. Spread proxy =
    median intrabar (high-low)/close in bps (conservative — no live quote source exists)."""
    # Technical-agent volume_ratio is 1h context; never use it as 15m RVOL.
    rvol = None
    df = _load(fs, symbol, "15m")
    dv = spread_bps = None
    fresh = "unknown"
    age_seconds = None
    bar_close_ts = None
    if df is not None:
        import pandas as pd
        d = df.copy()
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
        d = d.dropna(subset=["timestamp"]).sort_values("timestamp")
        as_of = pd.Timestamp(now)
        if as_of.tzinfo is None:
            as_of = as_of.tz_localize("UTC")
        else:
            as_of = as_of.tz_convert("UTC")
        # Keep the liquidity calculation on the same no-look-ahead clock as
        # market_context.  A future high-volume bar cannot make an older idea
        # look liquid or fresh.
        d = d[d["timestamp"] + pd.Timedelta(minutes=15) <= as_of]
        if not d.empty and "volume" in d and "close" in d:
            rvol, last_rth_ts = _intraday_rvol(d, now)
            current_rth = _rth_slice(d, now)
            if not current_rth.empty:
                dv = float((current_rth["close"].astype(float) * current_rth["volume"].astype(float)).sum())
            if "high" in d and "low" in d:
                proxy_frame = current_rth if not current_rth.empty else d.tail(30)
                rng = ((proxy_frame["high"].astype(float) - proxy_frame["low"].astype(float)) / proxy_frame["close"].astype(float)).median()
                spread_bps = round(float(rng) * 10000 / 4.0, 1)   # intrabar-range proxy, not a bid/ask spread
            last_ts = last_rth_ts if last_rth_ts is not None else d["timestamp"].iloc[-1]
            bar_close_ts = last_ts + pd.Timedelta(minutes=15)
            age_seconds = max(
                0.0,
                (as_of.to_pydatetime() - bar_close_ts.to_pydatetime()).total_seconds(),
            )
            age_min = age_seconds / 60.0
            max_age = float(cfg.get("max_data_age_sec", 900)) / 60.0
            fresh = "fresh" if age_min <= max_age else "stale"
    return {"rvol": rvol, "dollar_volume": dv, "spread_bps_est": spread_bps,
            "spread_estimation_method": "intrabar_range_proxy_not_bid_ask",
            "data_freshness_status": fresh, "data_gap_late": bool(setup.get("data_gap_late")),
            "data_age_seconds": age_seconds,
            "last_closed_bar_at": bar_close_ts.isoformat() if bar_close_ts is not None else None,
            "liquidity_whitelisted": symbol in set(cfg.get("liquidity_whitelist", []))}


def sector_context(fs, symbol, direction, idea_ctx, now, cfg) -> dict:
    """Sector ETF direction/VWAP + RS vs SPY/sector → confirmation status. Uses cached sector ETF
    OHLCV where available; falls back to the strict tri-state already computed by the agent."""
    sector_etf = ""
    try:
        from src.stocks.configs.loader import load_stocks_config
        sector_etf = load_stocks_config().sector_etf_for(symbol)
    except Exception:
        sector_etf = ""
    sret = svwap = stock_ret = spy_ret = None
    if sector_etf:
        df = _load(fs, sector_etf, "15m")
        if df is None:                       # explicit fallback — `df or _load(...)` raises on a DataFrame
            pass  # 15m confirmation is required; a 1h fallback is not intraday evidence.
        if df is not None:
            sret, svwap, _ = _return_and_vwap(df, now)
    stock_df = _load(fs, symbol, "15m")
    if stock_df is not None:
        stock_ret, _stock_vwap, _ = _return_and_vwap(stock_df, now)
    spy_df = _load(fs, "SPY", "15m")
    if spy_df is not None:
        spy_ret, _spy_vwap, _ = _return_and_vwap(spy_df, now)
    rs_spy = round(stock_ret - spy_ret, 4) if stock_ret is not None and spy_ret is not None else None
    # RS vs sector: reuse the agent's strict tri-state (sector_contradicts / sector_weak)
    sector_contradicts = False
    sector_weak = None
    rs_sector = round(stock_ret - sret, 4) if stock_ret is not None and sret is not None else None
    if sret is not None and svwap is not None and rs_spy is not None and rs_sector is not None:
        status = _g.classify_sector(direction=direction, sector_rth_return_pct=sret, sector_vs_vwap=svwap,
                                    rs_vs_spy=rs_spy, rs_vs_sector=rs_sector, cfg=cfg)
    else:  # no sector ETF data → fall back to the strict tri-state
        if sector_contradicts:
            status = "conflict"
        elif sector_weak:
            status = "weak"
        elif sector_weak is False:
            status = "confirmed"
        else:
            status = "unknown"
    return {"sector_etf": sector_etf, "sector_rth_return_pct": sret, "sector_vs_vwap": svwap,
            "stock_rth_return_pct": stock_ret, "spy_rth_return_pct": spy_ret,
            "rs_vs_spy": rs_spy, "rs_vs_sector": rs_sector,
            "rs_timeframe": "15m_rth_same_session", "status": status}


def catalyst_context(catalyst_meta, cfg, now=None) -> dict:
    """Map the existing per-idea catalyst meta → catalyst quality (never fabricated)."""
    cm = catalyst_meta or {}
    primary = cm.get("catalyst_type") or cm.get("primary_type")
    src_count = cm.get("source_count")
    if src_count is None:
        src_count = 1 if (cm.get("source") or cm.get("headline_short")) else 0
    age_min = cm.get("catalyst_age_minutes")
    if age_min is None and cm.get("age_hours") is not None:
        try:
            age_min = float(cm["age_hours"]) * 60.0
        except (TypeError, ValueError):
            age_min = None
    if age_min is None and cm.get("published_at") and now is not None:
        try:
            published = datetime.fromisoformat(str(cm["published_at"]).replace("Z", "+00:00"))
            published = published if published.tzinfo else published.replace(tzinfo=timezone.utc)
            current = now if now.tzinfo else now.replace(tzinfo=timezone.utc)
            age_min = max(0.0, (current.astimezone(timezone.utc) - published.astimezone(timezone.utc)).total_seconds() / 60.0)
        except (TypeError, ValueError):
            age_min = None
    quality = _g.classify_catalyst_quality(primary_type=primary, age_minutes=age_min,
                                           source_count=src_count,
                                           source_quality=cm.get("source_quality", "medium"), cfg=cfg)
    return {"catalyst_quality": quality, "catalyst_age_minutes": age_min,
            "catalyst_source_count": src_count, "catalyst_primary_type": primary,
            "catalyst_direction_hint": str(cm.get("direction_hint") or "").lower()}


def build_context(*, symbol, direction, setup, now, idea_ctx, catalyst_meta, cfg,
                  fs=None) -> dict:
    """Assemble the full gate context. now is tz-aware UTC."""
    if now is None:
        now = datetime.now(timezone.utc)
    fs = fs or _fs()
    return {
        "phase": _g.session_phase(now),
        "market_ctx": market_context(now, cfg),
        "sector_ctx": sector_context(fs, symbol, direction, idea_ctx or {}, now, cfg),
        "liquidity": liquidity_from_ohlcv(fs, symbol, setup or {}, now, cfg),
        "catalyst": catalyst_context(catalyst_meta, cfg, now),
    }


__all__ = ["build_context", "market_context", "sector_context", "liquidity_from_ohlcv", "catalyst_context"]
