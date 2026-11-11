"""Squeeze Phase Classifier (Shadow Intelligence PART 3).

Classifies a symbol into a squeeze lifecycle phase from price structure (OHLCV
archive) + derivatives context + catalyst/timeline. Diagnostic only: NO auto-short,
NO routing/score/TP-SL change, NO hard filter. Background-computed; alert path reads
the cache. Fail-open to phase_0_unknown.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.intelligence import store
from src.intelligence.derivatives_trajectory import _price_frame

PHASES = ["phase_0_unknown", "phase_1_build_up", "phase_2_squeeze_expansion",
          "phase_3_distribution_near_high", "phase_4_unwind", "phase_5_post_unwind_chop"]


def _metrics(symbol: str):
    """Return (price_24h, price_7d, price_6h, dist_to_local_high_pct) or Nones."""
    import pandas as pd
    df, tf = _price_frame(symbol)
    if df is None or not len(df):
        return None
    last = df.iloc[-1]
    lp = float(last["close"])

    def chg(hours):
        cut = last["timestamp"] - pd.Timedelta(hours=hours)
        pr = df[df["timestamp"] <= cut]
        if pr.empty:
            return None
        p0 = float(pr.iloc[-1]["close"])
        return (lp - p0) / p0 * 100 if p0 else None

    local_high = float(df.tail(2016)["high"].max())  # ~7d of 5m
    dist_to_high = (local_high - lp) / local_high * 100 if local_high else None
    return {"p24": chg(24), "p7d": chg(168), "p6h": chg(6),
            "dist_to_high_pct": round(dist_to_high, 2) if dist_to_high is not None else None,
            "last_price": lp, "local_high": local_high}


def _empty() -> dict[str, Any]:
    return {
        "squeeze_phase": "phase_0_unknown", "squeeze_phase_confidence": "unknown",
        "phase_reason_codes": [], "phase_changed_since_last_seen": None,
        "distribution_risk_score": None, "squeeze_peak_score": None,
        "no_chase_warning": False, "unwind_risk_score": None,
        "data_missing_reason": "no_price_data", "diagnostic_only": True,
    }


def classify_squeeze_phase(symbol: str, now: datetime | None = None,
                           deriv: dict[str, Any] | None = None) -> dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    out = _empty()
    try:
        m = _metrics(symbol)
        if m is None or m["p24"] is None or m["dist_to_high_pct"] is None:
            return out
        out["data_missing_reason"] = None
        p24, p7d, p6h, dist = m["p24"], m["p7d"] or 0.0, m["p6h"] or 0.0, m["dist_to_high_pct"]
        if deriv is None:
            from src.intelligence.derivatives_trajectory import compute_derivatives_trajectory
            deriv = compute_derivatives_trajectory(symbol, now=now)
        funding_turning = deriv.get("funding_turning_down")
        oi_stall = deriv.get("oi_stall_detected")

        codes = []
        near_high = dist <= 3.0
        extreme_pump = (p7d >= 30) or (p24 >= 15)
        accel = p6h >= 4 and p24 >= 10
        phase = "phase_0_unknown"
        if near_high and extreme_pump:
            phase = "phase_3_distribution_near_high"
            codes = [f"near_local_high({dist:.1f}%)", f"pump_7d({p7d:.0f}%)"]
            if funding_turning:
                codes.append("funding_turning_down")
            if oi_stall:
                codes.append("oi_stall")
        elif accel:
            phase = "phase_2_squeeze_expansion"
            codes = [f"accel_6h({p6h:.0f}%)", f"up_24h({p24:.0f}%)"]
        elif 5 <= p7d < 30 and p24 > -3:
            phase = "phase_1_build_up"
            codes = [f"steady_up_7d({p7d:.0f}%)"]
        elif p24 <= -8:
            phase = ("phase_4_unwind" if p7d > 0 or dist < 15 else "phase_5_post_unwind_chop")
            codes = [f"down_24h({p24:.0f}%)"]
        elif abs(p24) < 3 and p7d < 10:
            phase = "phase_5_post_unwind_chop"
            codes = ["low_volatility_chop"]

        # risk scores (0-100, heuristic)
        out["distribution_risk_score"] = int(max(0, min(100,
            (30 if near_high else 0) + min(50, max(0, p7d)) + (20 if funding_turning else 0))))
        out["squeeze_peak_score"] = int(max(0, min(100, min(60, max(0, p24)) + (40 if accel else 0))))
        out["unwind_risk_score"] = int(max(0, min(100, max(0, -p24) * 3)))
        out["no_chase_warning"] = phase in ("phase_3_distribution_near_high",) or (near_high and extreme_pump)
        out["squeeze_phase"] = phase
        out["phase_reason_codes"] = codes
        out["squeeze_phase_confidence"] = (
            "high" if (m["p7d"] is not None and deriv.get("derivatives_data_confidence") in ("medium", "high")) else
            "medium" if phase != "phase_0_unknown" else "low")
        return out
    except Exception:
        return _empty()


def update_phase_history(symbol: str, phase: str, now: datetime | None = None, conn=None) -> bool:
    """Append to phase_history only when the phase changed. Returns True if changed."""
    try:
        sym = symbol.split("/")[0].upper()
        own = conn is None
        c = conn or store.connect()
        try:
            last = c.execute("SELECT phase FROM phase_history WHERE symbol=? "
                             "ORDER BY changed_at DESC LIMIT 1", (sym,)).fetchone()
            if last and last["phase"] == phase:
                return False
            c.execute("INSERT INTO phase_history(symbol,phase,changed_at) VALUES(?,?,?)",
                      (sym, phase, (now or datetime.now(timezone.utc)).isoformat()))
            if own:
                c.commit()
            return True
        finally:
            if own:
                c.close()
    except Exception:
        return False


def update_and_cache(symbol: str, now: datetime | None = None, deriv=None, conn=None) -> dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    fields = classify_squeeze_phase(symbol, now=now, deriv=deriv)
    try:
        own = conn is None
        c = conn or store.connect()
        try:
            prev = store.read_cache("phase_cache", symbol.split("/")[0].upper())
            fields["phase_changed_since_last_seen"] = bool(
                prev and prev.get("squeeze_phase") != fields["squeeze_phase"])
            store.write_cache(c, "phase_cache", symbol.split("/")[0].upper(), now.isoformat(), fields)
            update_phase_history(symbol, fields["squeeze_phase"], now=now, conn=c)
            if own:
                c.commit()
        finally:
            if own:
                c.close()
    except Exception:
        pass
    return fields


def squeeze_phase_for_payload(symbol: str) -> dict[str, Any]:
    cached = store.read_cache("phase_cache", symbol.split("/")[0].upper()) or _empty()
    return {k: cached.get(k) for k in (
        "squeeze_phase", "squeeze_phase_confidence", "phase_reason_codes",
        "phase_changed_since_last_seen", "distribution_risk_score",
        "squeeze_peak_score", "no_chase_warning", "unwind_risk_score")}


def squeeze_phase_health_report() -> dict[str, Any]:
    conn = store.connect_ro()
    if conn is None:
        return {"status": "empty", "cached_symbols": 0}
    try:
        n = conn.execute("SELECT COUNT(*) n FROM phase_cache").fetchone()["n"]
        dist = {r["squeeze_phase"]: r["n"] for r in conn.execute(
            "SELECT json_extract(fields_json,'$.squeeze_phase') squeeze_phase, COUNT(*) n "
            "FROM phase_cache GROUP BY 1")}
        return {"status": "ok" if n else "empty", "cached_symbols": n, "phase_distribution": dist}
    except Exception:
        return {"status": "unavailable", "cached_symbols": 0}
    finally:
        conn.close()
