"""Point-in-time derivatives trajectory cache.

Computes descriptive funding/OI context from the canonical SQL archive.  The
module never emits a trade direction and never writes trading state.  Historical
calls use ``provider_ts <= now`` so counterfactual evaluation cannot look ahead.
"""
from __future__ import annotations

import math
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean, median, pstdev
from typing import Any

from src.data_collectors.market_intelligence_store import default_db_path, normalize_symbol
from src.intelligence import store

ROOT = Path(__file__).resolve().parent.parent.parent
ARCHIVE = ROOT / "data" / "archive" / "ohlcv"
CACHE = ROOT / "data" / "raw" / "ohlcv"
EXCHANGES = ("binance", "bybit", "mexc")


def _price_frame(symbol: str):
    import pandas as pd

    sym = symbol.replace("/", "_").upper()
    for tf in ("5m", "15m", "1h"):
        for ex in EXCHANGES:
            for base in (ARCHIVE, CACHE):
                path = base / ex / tf / f"{sym}.csv"
                if not path.exists():
                    continue
                try:
                    frame = pd.read_csv(path)
                    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
                    return frame.sort_values("timestamp"), tf
                except Exception:
                    continue
    return None, None


def _pct_change_over(frame, hours: float):
    try:
        import pandas as pd

        last = frame.iloc[-1]
        prior = frame[frame["timestamp"] <= last["timestamp"] - pd.Timedelta(hours=hours)]
        if prior.empty:
            return None
        p0, p1 = float(prior.iloc[-1]["close"]), float(last["close"])
        return round((p1 - p0) / p0 * 100, 2) if p0 else None
    except Exception:
        return None


def _empty(symbol: str) -> dict[str, Any]:
    return {
        "funding_current": None, "funding_8h_slope": None, "funding_24h_slope": None,
        "funding_24h_zscore": None, "funding_peak_value_24h": None,
        "funding_peak_time_24h": None, "funding_turning_down": None,
        "funding_extreme_positive": None, "funding_extreme_negative": None,
        "oi_current": None, "oi_6h_change_pct": None, "oi_24h_change_pct": None,
        "oi_peak_value_24h": None, "oi_stall_hours": None, "oi_stall_detected": None,
        "price_6h_change_pct": None, "price_24h_change_pct": None,
        "oi_price_divergence": None, "cross_exchange_funding_confirmed": None,
        "cross_exchange_oi_confirmed": None, "derivatives_venue_count": 0,
        "derivatives_context": "unknown", "squeeze_risk_context": "unknown",
        "derivatives_warning": None, "derivatives_data_confidence": "unknown",
        "derivatives_data_freshness_sec": None, "diagnostic_only": True,
    }


def _dt(value: Any) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def _db_rows(
    symbol: str,
    now: datetime,
    *,
    source_conn: sqlite3.Connection | None = None,
) -> tuple[list[dict], list[dict]]:
    db = default_db_path()
    if source_conn is None and not db.exists():
        return [], []
    own_conn = source_conn is None
    conn = source_conn
    if conn is None:
        conn = sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True, timeout=2.0)
        conn.row_factory = sqlite3.Row
    norm = normalize_symbol(symbol)
    cutoff = (now - timedelta(hours=24)).isoformat()
    try:
        history = [dict(r) for r in conn.execute(
            "SELECT * FROM derivative_snapshots WHERE normalized_symbol=? AND provider_ts>=? "
            "AND provider_ts<=? ORDER BY provider_ts,id",
            (norm, cutoff, now.isoformat()),
        ).fetchall()]
        # Only rows recent enough to influence the 45-minute freshness gate are
        # useful here.  Bounding the window prevents the latest-per-venue query
        # from walking the full multi-million-row archive for every symbol.
        latest = [dict(r) for r in conn.execute(
            "SELECT * FROM (SELECT d.*,ROW_NUMBER() OVER(PARTITION BY exchange "
            "ORDER BY provider_ts DESC,id DESC) rn FROM derivative_snapshots d "
            "WHERE normalized_symbol=? AND provider_ts>=? AND provider_ts<=?) WHERE rn=1",
            (norm, cutoff, now.isoformat()),
        ).fetchall()]
        return history, latest
    except sqlite3.Error:
        return [], []
    finally:
        if own_conn:
            conn.close()


def _aggregate_oi(rows: list[dict]) -> list[tuple[datetime, float]]:
    # Sum venue OI by hourly bucket. Multiple source kinds on one venue/hour
    # are reduced to the latest row first to avoid double counting history and
    # current observations.
    per_venue_bucket: dict[tuple[str, str], tuple[datetime, float]] = {}
    for row in rows:
        value, ts = row.get("oi_usd"), _dt(row.get("provider_ts"))
        if value is None or ts is None or float(value) <= 0:
            continue
        key = (str(row.get("exchange")), ts.strftime("%Y-%m-%dT%H"))
        if key not in per_venue_bucket or ts > per_venue_bucket[key][0]:
            per_venue_bucket[key] = (ts, float(value))
    buckets: dict[str, tuple[datetime, float]] = {}
    for (_, hour), (ts, value) in per_venue_bucket.items():
        if hour not in buckets:
            buckets[hour] = (ts, 0.0)
        prior_ts, prior_value = buckets[hour]
        buckets[hour] = (max(prior_ts, ts), prior_value + value)
    return sorted(buckets.values(), key=lambda item: item[0])


def compute_derivatives_trajectory(
    symbol: str,
    now: datetime | None = None,
    *,
    source_conn: sqlite3.Connection | None = None,
) -> dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    out = _empty(symbol)
    try:
        frame, _ = _price_frame(symbol)
        if frame is not None:
            frame = frame[frame["timestamp"] <= now]
        if frame is not None and len(frame):
            out["price_6h_change_pct"] = _pct_change_over(frame, 6)
            out["price_24h_change_pct"] = _pct_change_over(frame, 24)

        history, latest = _db_rows(symbol, now, source_conn=source_conn)
        fresh = [r for r in latest if _dt(r.get("provider_ts")) and
                 timedelta(0) <= now - _dt(r["provider_ts"]) <= timedelta(minutes=45)]
        out["derivatives_venue_count"] = len(fresh)
        current_funding = [float(r["funding_rate_8h"]) for r in fresh
                           if r.get("funding_rate_8h") is not None]
        funding_history = [float(r["funding_rate_8h"]) for r in history
                           if r.get("funding_rate_8h") is not None]
        fcur = median(current_funding) if current_funding else None
        out["funding_current"] = fcur
        if funding_history:
            peak = max(funding_history)
            out["funding_peak_value_24h"] = peak
            peak_rows = [r for r in history if r.get("funding_rate_8h") is not None and
                         float(r["funding_rate_8h"]) == peak]
            out["funding_peak_time_24h"] = peak_rows[-1]["provider_ts"] if peak_rows else None
            out["funding_24h_slope"] = funding_history[-1] - funding_history[0] if len(funding_history) >= 2 else None
            eight = [r for r in history if _dt(r.get("provider_ts")) and
                     now - _dt(r["provider_ts"]) <= timedelta(hours=8) and
                     r.get("funding_rate_8h") is not None]
            out["funding_8h_slope"] = (float(eight[-1]["funding_rate_8h"]) -
                                       float(eight[0]["funding_rate_8h"])) if len(eight) >= 2 else None
            sd = pstdev(funding_history) if len(funding_history) >= 2 else 0.0
            out["funding_24h_zscore"] = ((fcur - mean(funding_history)) / sd) if fcur is not None and sd else None
            if fcur is not None and peak > 0:
                out["funding_turning_down"] = fcur < peak * 0.7
        if fcur is not None:
            out["funding_extreme_positive"] = fcur >= 0.0008
            out["funding_extreme_negative"] = fcur <= -0.0008

        current_oi = [float(r["oi_usd"]) for r in fresh
                      if r.get("oi_usd") is not None and float(r["oi_usd"]) > 0]
        out["oi_current"] = sum(current_oi) if current_oi else None
        series = _aggregate_oi(history)
        out["oi_peak_value_24h"] = max((v for _, v in series), default=None)
        if out["oi_current"] and series:
            def change(hours: int):
                prior = [v for ts, v in series if ts <= now - timedelta(hours=hours)]
                return ((out["oi_current"] / prior[-1]) - 1.0) * 100.0 if prior and prior[-1] else None
            out["oi_6h_change_pct"] = change(6)
            out["oi_24h_change_pct"] = change(24)
        if len(series) >= 3:
            peak = max(v for _, v in series)
            tail = [v for _, v in series[-3:]]
            out["oi_stall_detected"] = bool(peak > 0 and max(tail) <= peak * 1.01 and min(tail) >= peak * 0.94)
        if out["oi_24h_change_pct"] is not None and out["price_24h_change_pct"] is not None:
            oi_up, px = out["oi_24h_change_pct"] >= 5, out["price_24h_change_pct"]
            out["oi_price_divergence"] = ("price_up_oi_down" if px >= 3 and not oi_up else
                                           "price_down_oi_up" if px <= -3 and oi_up else "none")
        out["cross_exchange_funding_confirmed"] = len(current_funding) >= 2
        out["cross_exchange_oi_confirmed"] = len(current_oi) >= 2
        if fresh:
            newest = max(_dt(r["provider_ts"]) for r in fresh)
            out["derivatives_data_freshness_sec"] = max(0, int((now - newest).total_seconds()))

        p24 = out["price_24h_change_pct"]
        if p24 is not None:
            if p24 >= 20:
                out["derivatives_context"], out["squeeze_risk_context"] = "strong_up_move", "elevated"
            elif p24 >= 8:
                out["derivatives_context"], out["squeeze_risk_context"] = "up_move", "moderate"
            elif p24 <= -8:
                out["derivatives_context"], out["squeeze_risk_context"] = "down_move", "unwind"
            else:
                out["derivatives_context"], out["squeeze_risk_context"] = "range", "low"
        if out["funding_turning_down"] and (p24 or 0) >= 8:
            out["derivatives_warning"] = "funding peaked and is turning down after a strong move"

        have_price = p24 is not None
        out["derivatives_data_confidence"] = (
            "high" if have_price and len(fresh) >= 2 and fcur is not None and out["oi_current"] is not None else
            "medium" if have_price and fresh and (fcur is not None or out["oi_current"] is not None) else
            "low" if have_price else "unknown"
        )
        return out
    except Exception:
        return out


def update_and_cache(
    symbol: str,
    now: datetime | None = None,
    conn=None,
    *,
    source_conn: sqlite3.Connection | None = None,
) -> dict[str, Any]:
    fields = compute_derivatives_trajectory(symbol, now=now, source_conn=source_conn)
    try:
        own = conn is None
        target = conn or store.connect()
        try:
            store.write_cache(target, "deriv_cache", symbol.split("/")[0].upper(),
                              (now or datetime.now(timezone.utc)).isoformat(), fields)
            if own:
                target.commit()
        finally:
            if own:
                target.close()
    except Exception:
        pass
    return fields


def derivatives_trajectory_for_payload(symbol: str) -> dict[str, Any]:
    cached = store.read_cache("deriv_cache", symbol.split("/")[0].upper())
    src = cached or _empty(symbol)
    keys = ["funding_current", "funding_turning_down", "funding_extreme_positive",
            "funding_24h_zscore", "oi_current", "oi_24h_change_pct", "oi_stall_detected",
            "price_6h_change_pct", "price_24h_change_pct", "oi_price_divergence",
            "derivatives_venue_count", "derivatives_context", "squeeze_risk_context",
            "derivatives_warning", "derivatives_data_confidence", "derivatives_data_freshness_sec"]
    return {key: src.get(key) for key in keys}


def derivatives_trajectory_health_report() -> dict[str, Any]:
    conn = store.connect_ro()
    if conn is None:
        return {"status": "empty", "cached_symbols": 0}
    try:
        n = conn.execute("SELECT COUNT(*) n FROM deriv_cache").fetchone()["n"]
        last = conn.execute("SELECT MAX(computed_at) m FROM deriv_cache").fetchone()["m"]
        return {"status": "ok" if n else "empty", "cached_symbols": n,
                "last_computed_at": last,
                "note": "canonical point-in-time funding/OI; freshness and venue count gate confidence"}
    except Exception:
        return {"status": "unavailable", "cached_symbols": 0}
    finally:
        conn.close()
