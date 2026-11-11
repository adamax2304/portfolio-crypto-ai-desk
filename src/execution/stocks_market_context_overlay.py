"""Shadow-first GEX and IV/RV context for stocks paper candidates.

The overlay never upgrades a signal. Its routing switch is off by default; in
that state it persists the point-in-time counterfactual only.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Any

from src.intelligence.context_config import section
from src.intelligence.context_store import connect, insert_named
from src.intelligence.options_context import latest


DECISION_COLS = (
    "signal_id", "filter_name", "filter_version", "decision_at", "context_ts",
    "action", "reason", "shadow_only", "features_json",
)


def _f(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _underlying(signal: dict[str, Any]) -> str:
    sector = str(signal.get("sector") or signal.get("sector_name") or "").lower()
    sector_etf = str(signal.get("sector_etf") or "").upper()
    if sector_etf in {"QQQ", "XLK", "SOXX", "SMH"} or any(
            word in sector for word in ("technology", "semiconductor", "software")):
        return "QQQ"
    return "SPY"


def evaluate(signal: dict[str, Any], *, as_of: datetime | None = None, context_db_path=None,
             gex_cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    now = as_of or datetime.now(timezone.utc)
    gex_cfg = gex_cfg or section("gex")
    underlying = _underlying(signal)
    ctx = latest("stocks", underlying, as_of=now, db_path=context_db_path)
    base = {
        "filter_name": "stocks_gex_vrp", "filter_version": "stocks_gex_vrp_v1",
        "underlying": underlying, "status": ctx.get("status", "unknown"),
        "action": "FULL_SIZE", "would_action": "FULL_SIZE",
        "reason": ctx.get("reason", "options_context_unknown"),
        "paper_routing_enabled": bool(gex_cfg.get("paper_routing_enabled", False)),
        "context_ts": ctx.get("provider_ts"), "iv30": ctx.get("iv30"),
        "rv30": ctx.get("rv30"), "vrp": ctx.get("vrp"), "iv_rank": ctx.get("iv_rank"),
        "net_gex": ctx.get("net_gex"), "gamma_flip": ctx.get("gamma_flip"),
        "call_wall": ctx.get("call_wall"), "put_wall": ctx.get("put_wall"),
    }
    accepted_quality = {str(value).lower() for value in gex_cfg.get("accepted_quality", [])}
    required_quality = str(gex_cfg.get("required_quality") or "").lower()
    if required_quality:
        accepted_quality.add(required_quality)
    if (ctx.get("status") == "ok" and accepted_quality
            and str(ctx.get("quality_status") or "").lower() not in accepted_quality):
        return {**base, "status": "unknown", "reason": "gex_quality_not_point_in_time"}
    if not gex_cfg.get("enabled", True) or ctx.get("status") != "ok":
        return base
    entry_mode = str(signal.get("entry_mode") or signal.get("setup_type") or "").upper()
    entry = _f(signal.get("entry_used") or signal.get("suggested_entry") or signal.get("entry_trigger"))
    atr = _f(signal.get("atr") or signal.get("atr14") or signal.get("adr20"))
    net_gex = _f(ctx.get("net_gex"))
    call_wall = _f(ctx.get("call_wall"))
    positive_gamma = net_gex is not None and net_gex > 0
    near_call_wall = bool(entry is not None and atr is not None and atr > 0 and call_wall is not None
                          and abs(call_wall - entry) / atr <= float(gex_cfg.get("near_wall_atr", 0.5)))
    breakout = "BREAKOUT" in entry_mode or "MOMENTUM" in entry_mode
    would = "FULL_SIZE"
    reason = "gex_context_observed"
    if positive_gamma and breakout and near_call_wall:
        would = str(gex_cfg.get("positive_gamma_breakout_action", "HALF_SIZE"))
        reason = "positive_gamma_breakout_near_call_wall"
    action = would if gex_cfg.get("paper_routing_enabled", False) else "FULL_SIZE"
    return {**base, "action": action, "would_action": would, "reason": reason,
            "positive_gamma": positive_gamma, "near_call_wall": near_call_wall,
            "entry_mode": entry_mode, "entry": entry, "atr": atr}


def decide_and_persist(signal: dict[str, Any], *, as_of: datetime | None = None,
                       trading_db_path=None, context_db_path=None) -> dict[str, Any]:
    now = as_of or datetime.now(timezone.utc)
    effective = dict(signal)
    if not effective.get("entry_mode") and trading_db_path and effective.get("signal_id"):
        conn = None
        try:
            conn = sqlite3.connect(str(trading_db_path))
            row = conn.execute(
                "SELECT entry_mode FROM signal_entry_mode_preentry WHERE signal_id=? "
                "AND data_quality='ok' LIMIT 1", (effective["signal_id"],)).fetchone()
            if row:
                effective["entry_mode"] = row[0]
        except sqlite3.Error:
            pass
        finally:
            if conn is not None:
                conn.close()
    result = evaluate(effective, as_of=now, context_db_path=context_db_path)
    sid = str(signal.get("signal_id") or "")
    if sid:
        row = {"signal_id": sid, "filter_name": result["filter_name"],
               "filter_version": result["filter_version"], "decision_at": now.isoformat(),
               "context_ts": result.get("context_ts"), "action": result.get("would_action", "FULL_SIZE"),
               "reason": result.get("reason"), "shadow_only": int(not result.get("paper_routing_enabled")),
               "features_json": result}
        with connect(context_db_path) as conn:
            insert_named(conn, "context_filter_decisions", row, DECISION_COLS)
            conn.commit()
    return result


__all__ = ["evaluate", "decide_and_persist", "DECISION_COLS"]
