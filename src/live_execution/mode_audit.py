from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from src.config import load_config
from src.execution.paper_live_exit_path import VERSION as LIVE_EXIT_PARITY_VERSION
from src.live_execution.config import load_live_canary_config
from src.live_execution.routing_registry import load_registry, route, route_key

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT = ROOT / "reports" / "CRYPTO_LIVE_MODE_AUDIT_LATEST.md"
DEFAULT_JSON = ROOT / "reports" / "CRYPTO_LIVE_MODE_AUDIT_LATEST.json"
INVEST_DB = ROOT / "research_labs" / "regime_conditioned_continuation" / "research.sqlite"


def _parse_utc(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _json_value(value: Any, fallback: Any) -> Any:
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(str(value or ""))
    except (TypeError, ValueError, json.JSONDecodeError):
        return fallback


def _table_exists(conn: sqlite3.Connection, name: str) -> bool:
    return bool(conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone())


def _columns(conn: sqlite3.Connection, table: str) -> set[str]:
    if not _table_exists(conn, table):
        return set()
    return {str(row[1]) for row in conn.execute(f"PRAGMA table_info({table})")}


def _connect(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path, timeout=20.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=20000")
    return conn


def _group(conn: sqlite3.Connection, sql: str, params: tuple[Any, ...]) -> list[dict[str, Any]]:
    return [dict(row) for row in conn.execute(sql, params).fetchall()]


def _lookup_live_decision(conn: sqlite3.Connection, signal_id: str) -> dict[str, Any] | None:
    if not _table_exists(conn, "mexc_canary_decisions"):
        return None
    row = conn.execute(
        "SELECT decision_id,signal_id,eligible,state,rejection_reasons_json,captured_at "
        "FROM mexc_canary_decisions "
        "WHERE signal_id=? OR signal_id=? OR json_extract(decision_json,'$.source_signal_id')=? "
        "ORDER BY eligible DESC,captured_at DESC LIMIT 1",
        (signal_id, f"stock_paper:{signal_id}", signal_id),
    ).fetchone()
    return dict(row) if row else None


def _lookup_alert_capture(conn: sqlite3.Connection, signal_id: str) -> dict[str, Any] | None:
    if not _table_exists(conn, "signal_alerts"):
        return None
    row = conn.execute(
        "SELECT sent_at,payload_json FROM signal_alerts "
        "WHERE signal_id=? AND alert_type='paper_entry' "
        "ORDER BY sent_at DESC,rowid DESC LIMIT 1",
        (signal_id,),
    ).fetchone()
    if not row:
        return None
    payload = _json_value(row["payload_json"], {})
    if not isinstance(payload, dict):
        return None
    status = str(payload.get("mexc_canary_capture_status") or "").upper()
    if status not in {"REJECTED", "DUPLICATE"}:
        return None
    return {
        "decision_id": None,
        "signal_id": signal_id,
        "eligible": 0,
        "state": status,
        "rejection_reasons_json": json.dumps(payload.get("mexc_canary_capture_reasons") or []),
        "captured_at": row["sent_at"],
        "source": "signal_alert_payload",
    }


def _recent_live(conn: sqlite3.Connection, since: datetime, limit: int) -> dict[str, Any]:
    if not _table_exists(conn, "mexc_canary_decisions"):
        return {"decisions": [], "rejections": [], "venue_attempts": [], "orders": [], "positions": []}
    since_text = since.isoformat()
    decisions = _group(
        conn,
        "SELECT COALESCE(mode,'?') mode,COALESCE(entry_mode,'?') entry_mode,"
        "eligible,state,COUNT(*) n FROM mexc_canary_decisions WHERE captured_at>=? "
        "GROUP BY 1,2,3,4 ORDER BY n DESC",
        (since_text,),
    )
    reason_counts: dict[str, int] = {}
    rejected_rows = conn.execute(
        "SELECT rejection_reasons_json FROM mexc_canary_decisions WHERE captured_at>=? AND eligible=0",
        (since_text,),
    ).fetchall()
    for row in rejected_rows:
        for reason in _json_value(row[0], []):
            reason_counts[str(reason)] = reason_counts.get(str(reason), 0) + 1
    venue_attempts = []
    if _table_exists(conn, "mexc_canary_venue_attempts"):
        venue_attempts = _group(
            conn,
            "SELECT venue,stage,status,COALESCE(reason,'') reason,COUNT(*) n "
            "FROM mexc_canary_venue_attempts WHERE attempted_at>=? "
            "GROUP BY 1,2,3,4 ORDER BY n DESC LIMIT 25",
            (since_text,),
        )
    orders = []
    if _table_exists(conn, "mexc_canary_orders"):
        orders = _group(
            conn,
            "SELECT venue,status,COUNT(*) n,MAX(updated_at) latest "
            "FROM mexc_canary_orders WHERE updated_at>=? GROUP BY 1,2 ORDER BY n DESC",
            (since_text,),
        )
    positions = []
    if _table_exists(conn, "mexc_canary_positions"):
        positions = _group(
            conn,
            "SELECT venue,status,COUNT(*) n,MAX(updated_at) latest "
            "FROM mexc_canary_positions WHERE updated_at>=? GROUP BY 1,2 ORDER BY n DESC",
            (since_text,),
        )
    recent_rejections = [
        dict(row) for row in conn.execute(
            "SELECT captured_at,signal_id,symbol,mode,entry_mode,state,rejection_reasons_json "
            "FROM mexc_canary_decisions WHERE captured_at>=? AND eligible=0 "
            "ORDER BY captured_at DESC LIMIT ?",
            (since_text, int(limit)),
        ).fetchall()
    ]
    return {
        "decisions": decisions,
        "rejection_reasons": [
            {"reason": reason, "n": n}
            for reason, n in sorted(reason_counts.items(), key=lambda item: (-item[1], item[0]))
        ],
        "venue_attempts": venue_attempts,
        "orders": orders,
        "positions": positions,
        "recent_rejections": recent_rejections,
    }


def _paper_live_reconciliation(conn: sqlite3.Connection, since: datetime, limit: int) -> dict[str, Any]:
    if not (_table_exists(conn, "paper_execution_outcomes") and _table_exists(conn, "proposed_signals")):
        return {"available": False, "reason": "missing paper/proposed tables"}
    cols = _columns(conn, "paper_execution_outcomes")
    time_expr = "COALESCE(o.entry_at,o.decision_at,p.created_at,o.computed_at)"
    rows = conn.execute(
        f"SELECT o.signal_id,{time_expr} AS observed_at,o.lifecycle_state,o.close_reason,"
        "o.paper_entry_profile,o.paper_execution_entry_mode,"
        "p.asset_class,p.mode,p.entry_type,p.symbol,p.direction,p.tier,p.score "
        "FROM paper_execution_outcomes o "
        "JOIN proposed_signals p ON p.signal_id=o.signal_id "
        f"WHERE {time_expr}>=? "
        "AND COALESCE(o.lifecycle_state,'') NOT IN ('NO_ENTRY','INVALID') "
        "AND COALESCE(o.close_reason,'') NOT IN ('no_entry','invalid_stock_intraday_entry_not_point_in_time') "
        "AND COALESCE(o.current_price_revalidated,0)=1 "
        "AND COALESCE(o.entry_time_basis,'')='point_in_time_current_bar' "
        "ORDER BY observed_at DESC LIMIT 1000",
        (since.isoformat(),),
    ).fetchall()
    summary: dict[str, int] = {
        "paper_rows": 0,
        "live_routable": 0,
        "not_live_route": 0,
        "missing_live_decision": 0,
        "live_rejected": 0,
        "live_queued_or_processing": 0,
        "live_submitted_or_active": 0,
    }
    missing: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for raw in rows:
        row = dict(raw)
        summary["paper_rows"] += 1
        asset = str(row.get("asset_class") or "crypto").lower()
        mode = str(row.get("mode") or "").lower()
        entry_mode = str(row.get("paper_execution_entry_mode") or row.get("entry_type") or "").upper()
        routed = route(mode=mode, entry_mode=entry_mode, asset_class=asset)
        if not routed or routed.get("enabled") is not True:
            summary["not_live_route"] += 1
            continue
        summary["live_routable"] += 1
        live_decision = _lookup_live_decision(conn, str(row.get("signal_id") or ""))
        if live_decision is None:
            live_decision = _lookup_alert_capture(conn, str(row.get("signal_id") or ""))
        if not live_decision:
            summary["missing_live_decision"] += 1
            if len(missing) < limit:
                missing.append({
                    "observed_at": row.get("observed_at"),
                    "signal_id": row.get("signal_id"),
                    "symbol": row.get("symbol"),
                    "mode": mode,
                    "entry_mode": entry_mode,
                    "route_key": route_key(mode=mode, entry_mode=entry_mode, asset_class=asset),
                })
            continue
        if int(live_decision.get("eligible") or 0) == 0:
            summary["live_rejected"] += 1
            if len(rejected) < limit:
                rejected.append({
                    "captured_at": live_decision.get("captured_at") or row.get("observed_at"),
                    "signal_id": row.get("signal_id"),
                    "symbol": row.get("symbol"),
                    "mode": mode,
                    "entry_mode": entry_mode,
                    "state": live_decision.get("state"),
                    "reasons": _json_value(live_decision.get("rejection_reasons_json"), []),
                })
            continue
        state = str(live_decision.get("state") or "")
        if state in {"QUEUED", "PROCESSING"}:
            summary["live_queued_or_processing"] += 1
        else:
            summary["live_submitted_or_active"] += 1
    return {
        "available": True,
        "summary": summary,
        "missing_live_decision": missing,
        "live_rejected": rejected,
        "paper_execution_columns_present": sorted(cols),
    }


def _truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _pf(rows: list[float]) -> dict[str, Any]:
    wins = [value for value in rows if value > 0]
    losses = [value for value in rows if value < 0]
    gross_win = round(sum(wins), 4)
    gross_loss = round(abs(sum(losses)), 4)
    if gross_loss > 0:
        pf_value: float | str | None = round(gross_win / gross_loss, 3)
    elif gross_win > 0:
        pf_value = "inf"
    else:
        pf_value = None
    return {
        "closed": len(rows),
        "wins": len(wins),
        "losses": len(losses),
        "winrate": None if not rows else round(len(wins) / len(rows), 3),
        "net_r": round(sum(rows), 4),
        "gross_win_r": gross_win,
        "gross_loss_r": gross_loss,
        "profit_factor": pf_value,
    }


def _select_col(cols: set[str], name: str, fallback: str = "NULL") -> str:
    return f"o.{name}" if name in cols else f"{fallback} AS {name}"


def _live_compatible_paper_pf(conn: sqlite3.Connection, since: datetime) -> dict[str, Any]:
    if not (_table_exists(conn, "paper_execution_outcomes") and _table_exists(conn, "proposed_signals")):
        return {"available": False, "reason": "missing paper/proposed tables"}
    cols = _columns(conn, "paper_execution_outcomes")
    if "paper_execution_r" not in cols:
        return {"available": False, "reason": "paper_execution_r missing"}
    time_candidates = [
        name for name in ("exit_at", "entry_at", "decision_at", "computed_at")
        if name in cols
    ]
    time_expr = (
        "COALESCE(" + ",".join(f"o.{name}" for name in time_candidates) + ",p.created_at)"
        if time_candidates else "p.created_at"
    )
    rows = conn.execute(
        f"""
        SELECT
          o.signal_id,
          {time_expr} AS observed_at,
          o.paper_execution_r,
          {_select_col(cols, "lifecycle_state", "''")},
          {_select_col(cols, "execution_validity", "''")},
          {_select_col(cols, "entry_time_basis", "''")},
          {_select_col(cols, "current_price_revalidated", "0")},
          {_select_col(cols, "close_reason", "''")},
          {_select_col(cols, "paper_entry_profile", "''")},
          {_select_col(cols, "paper_execution_entry_mode", "''")},
          {_select_col(cols, "version", "''")},
          p.asset_class,p.mode,p.entry_type,p.symbol,p.direction,p.tier,p.score
        FROM paper_execution_outcomes o
        JOIN proposed_signals p ON p.signal_id=o.signal_id
        WHERE {time_expr}>=?
          AND o.paper_execution_r IS NOT NULL
        ORDER BY observed_at DESC
        """,
        (since.isoformat(),),
    ).fetchall()
    excluded: dict[str, int] = {}
    by_route_values: dict[str, list[float]] = {}
    by_route_meta: dict[str, dict[str, Any]] = {}
    all_values: list[float] = []

    def exclude(reason: str) -> None:
        excluded[reason] = excluded.get(reason, 0) + 1

    for raw in rows:
        row = dict(raw)
        lifecycle = str(row.get("lifecycle_state") or "")
        validity = str(row.get("execution_validity") or "")
        close_reason = str(row.get("close_reason") or "")
        if lifecycle != "CLOSED":
            exclude("NOT_CLOSED")
            continue
        if validity != "valid":
            exclude("EXECUTION_NOT_VALID")
            continue
        if str(row.get("version") or "") != LIVE_EXIT_PARITY_VERSION:
            exclude("LEGACY_PAPER_EXIT_MODEL")
            continue
        if close_reason in {"no_entry", "invalid_stock_intraday_entry_not_point_in_time", "expired_flat"}:
            exclude("NON_ACTIONABLE_CLOSE_REASON")
            continue
        if str(row.get("entry_time_basis") or "") != "point_in_time_current_bar":
            exclude("ENTRY_NOT_POINT_IN_TIME")
            continue
        if not _truthy(row.get("current_price_revalidated")):
            exclude("CURRENT_PRICE_NOT_REVALIDATED")
            continue
        asset = str(row.get("asset_class") or "crypto").lower()
        mode = str(row.get("mode") or "").lower()
        entry_mode = str(row.get("paper_execution_entry_mode") or row.get("entry_type") or "").upper()
        routed = route(mode=mode, entry_mode=entry_mode, asset_class=asset)
        if not routed or routed.get("enabled") is not True:
            exclude("CURRENT_LIVE_ROUTE_DISABLED")
            continue
        key = str(routed.get("route_key") or route_key(mode=mode, entry_mode=entry_mode, asset_class=asset) or "?")
        value = float(row["paper_execution_r"])
        by_route_values.setdefault(key, []).append(value)
        by_route_meta.setdefault(key, {
            "route_key": key,
            "mode": mode,
            "entry_mode": entry_mode,
            "asset_class": asset,
        })
        all_values.append(value)

    by_route = []
    for key, values in sorted(by_route_values.items()):
        by_route.append({**by_route_meta[key], **_pf(values)})
    return {
        "available": True,
        "overall": _pf(all_values),
        "by_route": by_route,
        "excluded": [
            {"reason": reason, "n": n}
            for reason, n in sorted(excluded.items(), key=lambda item: (-item[1], item[0]))
        ],
        "rows_seen": len(rows),
    }


def _crypto_invest(now: datetime, since: datetime) -> dict[str, Any]:
    if not INVEST_DB.exists():
        return {"available": False, "reason": "research.sqlite missing"}
    conn = _connect(INVEST_DB)
    try:
        if not _table_exists(conn, "forward_decisions"):
            return {"available": False, "reason": "forward tables missing"}
        last_scan = None
        if _table_exists(conn, "forward_meta"):
            row = conn.execute(
                "SELECT value_json,updated_at FROM forward_meta WHERE key='last_scan'"
            ).fetchone()
            if row:
                last_scan = _json_value(row[0], {})
                scan_time = _parse_utc((last_scan or {}).get("observed_at") or row[1])
                if scan_time:
                    last_scan["age_minutes"] = round((now - scan_time).total_seconds() / 60.0, 2)
        decisions = _group(
            conn,
            "SELECT status,COALESCE(rejection_reason,'') rejection_reason,COUNT(*) n,MAX(created_at) latest "
            "FROM forward_decisions WHERE created_at>=? GROUP BY 1,2 ORDER BY n DESC",
            (since.isoformat(),),
        )
        outcomes = []
        if _table_exists(conn, "forward_outcomes"):
            outcomes = _group(
                conn,
                "SELECT outcome_status,COALESCE(close_reason,'') close_reason,COUNT(*) n,MAX(updated_at) latest "
                "FROM forward_outcomes WHERE updated_at>=? GROUP BY 1,2 ORDER BY n DESC",
                (since.isoformat(),),
            )
        return {"available": True, "last_scan": last_scan, "decisions": decisions, "outcomes": outcomes}
    finally:
        conn.close()


def _liquidity_sweep_v2(conn: sqlite3.Connection, since: datetime) -> dict[str, Any]:
    outcome_table = "crypto_liquidity_sweep_reclaim_v2_paper_outcomes"
    obs_table = "crypto_liquidity_sweep_reclaim_v2_paper_observations"
    eval_table = "crypto_liquidity_sweep_reclaim_v2_paper_evaluations"
    if not _table_exists(conn, obs_table):
        return {"available": False, "reason": "v2 tables missing"}
    observations = _group(
        conn,
        f"SELECT rejection_reason,COUNT(*) n,MAX(decision_at) latest "
        f"FROM {obs_table} WHERE evaluated_at>=? GROUP BY 1 ORDER BY n DESC LIMIT 15",
        (since.isoformat(),),
    )
    outcomes = []
    slices = []
    if _table_exists(conn, outcome_table):
        outcomes = _group(
            conn,
            f"SELECT eligibility_status,outcome_status,COALESCE(rejection_reason,'') rejection_reason,"
            f"COUNT(*) n,MAX(last_checked_at) latest FROM {outcome_table} "
            f"WHERE generated_at>=? GROUP BY 1,2,3 ORDER BY n DESC LIMIT 15",
            (since.isoformat(),),
        )
        slices = _group(
            conn,
            f"SELECT COALESCE(entry_profile,'?') entry_profile,"
            f"COALESCE(confirmation_timeframe,'?') confirmation_timeframe,"
            f"COALESCE(session_bucket,'?') session_bucket,"
            f"COALESCE(outcome_status,'?') outcome_status,"
            f"COALESCE(close_reason,'') close_reason,"
            f"COUNT(*) n,"
            f"SUM(CASE WHEN COALESCE(net_r,0)>0 THEN 1 ELSE 0 END) wins,"
            f"ROUND(SUM(COALESCE(net_r,0)),3) net_r,"
            f"ROUND(SUM(COALESCE(net_pnl_usd,0)),2) net_pnl_usd,"
            f"ROUND(AVG(COALESCE(latency_seconds,0)),1) avg_latency_sec "
            f"FROM {outcome_table} WHERE generated_at>=? AND COALESCE(eligibility_status,'')='eligible' "
            f"GROUP BY 1,2,3,4,5 ORDER BY n DESC LIMIT 25",
            (since.isoformat(),),
        )
    evaluations = []
    if _table_exists(conn, eval_table):
        evaluations = _group(
            conn,
            f"SELECT generated_at,profile_id,forward_rows,clean_rows,clean_closed,net_pnl_usd,profit_factor,verdict "
            f"FROM {eval_table} ORDER BY generated_at DESC LIMIT 4",
            (),
        )
    return {
        "available": True,
        "observations": observations,
        "outcomes": outcomes,
        "slices": slices,
        "evaluations": evaluations,
    }


def _limit_then_taker_quality(conn: sqlite3.Connection, since: datetime) -> dict[str, Any]:
    table = "paper_shadow_execution_outcomes"
    if not _table_exists(conn, table):
        return {"available": False, "reason": "paper shadow outcomes missing"}
    cols = _columns(conn, table)
    if not {"entry_mode", "net_r"}.issubset(cols):
        return {"available": False, "reason": "required LTT columns missing"}
    time_expr = "COALESCE(updated_at,created_at,entry_fill_time)"
    rows = _group(
        conn,
        f"SELECT COALESCE(branch,'?') branch,"
        f"COALESCE(entry_order_type,'?') entry_order_type,"
        f"COALESCE(exit_order_type,'?') exit_order_type,"
        f"COALESCE(taker_fallback_used,0) taker_fallback_used,"
        f"COALESCE(maker_entry_filled,0) maker_entry_filled,"
        f"COALESCE(maker_entry_missed,0) maker_entry_missed,"
        f"COUNT(*) n,"
        f"SUM(CASE WHEN COALESCE(net_r,0)>0 THEN 1 ELSE 0 END) wins,"
        f"ROUND(SUM(COALESCE(net_r,0)),3) net_r,"
        f"ROUND(SUM(COALESCE(net_pnl_usdt,0)),2) net_pnl_usdt,"
        f"ROUND(AVG(COALESCE(fees_usdt,0)+COALESCE(slippage_usdt,0)),4) avg_cost_usdt "
        f"FROM {table} WHERE UPPER(COALESCE(entry_mode,''))='LIMIT_THEN_TAKER_TIMEOUT' "
        f"AND {time_expr}>=? AND COALESCE(is_clean_for_edge,1)=1 "
        f"GROUP BY 1,2,3,4,5,6 ORDER BY n DESC LIMIT 25",
        (since.isoformat(),),
    )
    rejects = _group(
        conn,
        f"SELECT COALESCE(missed_entry_reason,'') missed_entry_reason,"
        f"COALESCE(entry_fill_status,'') entry_fill_status,COUNT(*) n,MAX({time_expr}) latest "
        f"FROM {table} WHERE UPPER(COALESCE(entry_mode,''))='LIMIT_THEN_TAKER_TIMEOUT' "
        f"AND {time_expr}>=? AND COALESCE(entry_fill_status,'') NOT IN ('filled','') "
        f"GROUP BY 1,2 ORDER BY n DESC LIMIT 15",
        (since.isoformat(),),
    )
    return {"available": True, "quality": rows, "missed_or_unfilled": rejects}


def _stock_live_filter_cfg() -> dict[str, Any]:
    path = ROOT / "config" / "stocks" / "mexc_stock_futures_live_bridge.yaml"
    if not yaml or not path.exists():
        return {}
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        bridge = raw.get("mexc_stock_futures_live_bridge") or {}
        return bridge.get("live_quality_filter") or {}
    except Exception:
        return {}


def _stock_post_filter_cohort(conn: sqlite3.Connection, since: datetime, limit: int) -> dict[str, Any]:
    cfg = _stock_live_filter_cfg()
    start = _parse_utc(cfg.get("post_filter_cohort_start_at")) or since
    if start < since:
        start = since
    if not _table_exists(conn, "mexc_canary_decisions"):
        return {"available": False, "reason": "live decisions missing"}
    start_text = start.isoformat()
    decisions = _group(
        conn,
        "SELECT COALESCE(entry_mode,'?') entry_mode,eligible,state,COUNT(*) n "
        "FROM mexc_canary_decisions "
        "WHERE captured_at>=? AND LOWER(COALESCE(mode,'')) LIKE 'stock%' "
        "GROUP BY 1,2,3 ORDER BY n DESC",
        (start_text,),
    )
    rejects = _group(
        conn,
        "SELECT captured_at,signal_id,symbol,entry_mode,state,rejection_reasons_json "
        "FROM mexc_canary_decisions "
        "WHERE captured_at>=? AND LOWER(COALESCE(mode,'')) LIKE 'stock%' AND eligible=0 "
        "ORDER BY captured_at DESC LIMIT ?",
        (start_text, int(limit)),
    )
    positions: list[dict[str, Any]] = []
    by_entry: list[dict[str, Any]] = []
    if _table_exists(conn, "mexc_canary_positions"):
        positions = _group(
            conn,
            "SELECT COALESCE(p.status,'?') status,COUNT(*) n,"
            "ROUND(SUM(COALESCE(p.realized_pnl_usdt,0)),2) realized_pnl_usdt,"
            "ROUND(SUM(COALESCE(p.fees_usdt,0)),2) fees_usdt,"
            "MAX(p.updated_at) latest "
            "FROM mexc_canary_positions p "
            "LEFT JOIN mexc_canary_decisions d ON d.decision_id=p.decision_id "
            "WHERE p.opened_at>=? AND LOWER(COALESCE(d.mode,'')) LIKE 'stock%' "
            "GROUP BY 1 ORDER BY n DESC",
            (start_text,),
        )
        by_entry = _group(
            conn,
            "SELECT COALESCE(d.entry_mode,'?') entry_mode,COALESCE(p.status,'?') status,COUNT(*) n,"
            "ROUND(SUM(COALESCE(p.realized_pnl_usdt,0)),2) realized_pnl_usdt,"
            "ROUND(AVG(COALESCE(p.risk_usdt,0)),2) avg_risk_usdt "
            "FROM mexc_canary_positions p "
            "LEFT JOIN mexc_canary_decisions d ON d.decision_id=p.decision_id "
            "WHERE p.opened_at>=? AND LOWER(COALESCE(d.mode,'')) LIKE 'stock%' "
            "GROUP BY 1,2 ORDER BY n DESC",
            (start_text,),
        )
    return {
        "available": True,
        "filter_version": cfg.get("version") or "?",
        "cohort_start": start_text,
        "decisions": decisions,
        "positions": positions,
        "by_entry_mode": by_entry,
        "recent_rejections": rejects,
    }


def build_report(*, db: str | Path | None = None, hours: int = 96,
                 now: datetime | None = None, limit: int = 25) -> dict[str, Any]:
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    since = now - timedelta(hours=max(1, int(hours)))
    db_path = Path(db) if db else load_config().db_path
    conn = _connect(db_path)
    try:
        live_cfg = load_live_canary_config()
        registry = load_registry()
        return {
            "generated_at": now.isoformat(),
            "since": since.isoformat(),
            "hours": int(hours),
            "live_config": {
                "capture_enabled": live_cfg.capture_enabled,
                "submission_enabled": live_cfg.submission_enabled,
                "execution_mode": live_cfg.execution_mode,
                "allowed_modes": sorted(live_cfg.allowed_modes()),
                "allowed_entry_modes": sorted(str(value).upper() for value in (live_cfg.get("allowed_entry_modes") or [])),
                "risk_per_trade_usdt": live_cfg.risk_per_trade_usdt,
                "max_concurrent_risk_usdt": live_cfg.max_concurrent_risk_usdt,
                "venue_order": live_cfg.venue_routing().get("preference_order"),
                "armed_venues": live_cfg.enabled_live_venues(asset_class="crypto"),
            },
            "live_routes": {
                key: {
                    "enabled": bool(value.get("enabled")),
                    "mode": value.get("mode"),
                    "entry_mode": value.get("entry_mode"),
                    "risk_bucket": value.get("risk_bucket"),
                }
                for key, value in sorted((registry.get("routes") or {}).items())
            },
            "paper_live_reconciliation": _paper_live_reconciliation(conn, since, limit),
            "live_compatible_paper_pf": _live_compatible_paper_pf(conn, since),
            "recent_live": _recent_live(conn, since, limit),
            "limit_then_taker_quality": _limit_then_taker_quality(conn, since),
            "stock_post_filter_cohort": _stock_post_filter_cohort(conn, since, limit),
            "liquidity_sweep_v2": _liquidity_sweep_v2(conn, since),
            "crypto_invest": _crypto_invest(now, since),
        }
    finally:
        conn.close()


def _table(rows: list[dict[str, Any]], columns: list[str]) -> list[str]:
    if not rows:
        return ["_No rows._"]
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return lines


def render_markdown(report: dict[str, Any]) -> str:
    recon = report["paper_live_reconciliation"]
    recon_summary = recon.get("summary") or {}
    live_compat_pf = report["live_compatible_paper_pf"]
    live = report["recent_live"]
    ltt = report["limit_then_taker_quality"]
    stock_cohort = report["stock_post_filter_cohort"]
    sweep = report["liquidity_sweep_v2"]
    invest = report["crypto_invest"]
    cfg = report["live_config"]
    lines = [
        "# Crypto Live Mode Audit",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Window: `{report['since']}` -> `{report['generated_at']}`",
        f"- Live: capture `{cfg['capture_enabled']}`, submission `{cfg['submission_enabled']}`, mode `{cfg['execution_mode']}`",
        f"- Allowed modes: `{', '.join(cfg['allowed_modes'])}`",
        f"- Risk: `${cfg['risk_per_trade_usdt']:.2f}` per full trade, `${cfg['max_concurrent_risk_usdt']:.2f}` concurrent cap",
        f"- Armed venues: `{', '.join(cfg.get('armed_venues') or []) or 'none'}`",
        "",
        "## Enabled Routes",
        "",
        *_table([
            {"route": key, **value}
            for key, value in report["live_routes"].items()
            if value.get("enabled")
        ], ["route", "mode", "entry_mode", "risk_bucket"]),
        "",
        "## Paper To Live Reconciliation",
        "",
        *_table([recon_summary], [
            "paper_rows", "live_routable", "missing_live_decision", "live_rejected",
            "live_queued_or_processing", "live_submitted_or_active", "not_live_route",
        ]),
        "",
        "### Missing Live Decision",
        "",
        *_table(recon.get("missing_live_decision") or [], ["observed_at", "signal_id", "symbol", "mode", "entry_mode", "route_key"]),
        "",
        "### Live Rejected",
        "",
        *_table(recon.get("live_rejected") or [], ["captured_at", "signal_id", "symbol", "mode", "entry_mode", "state", "reasons"]),
        "",
        "## Live-Compatible Paper PF",
        "",
    ]
    if live_compat_pf.get("available"):
        lines.extend(_table([live_compat_pf.get("overall") or {}], [
            "closed", "wins", "losses", "winrate", "net_r",
            "gross_win_r", "gross_loss_r", "profit_factor",
        ]))
        lines.extend(["", "### By Live Route", ""])
        lines.extend(_table(live_compat_pf.get("by_route") or [], [
            "route_key", "asset_class", "mode", "entry_mode", "closed",
            "wins", "losses", "winrate", "net_r", "profit_factor",
        ]))
        lines.extend(["", "### Excluded From Live-Compatible PF", ""])
        lines.extend(_table(live_compat_pf.get("excluded") or [], ["reason", "n"]))
    else:
        lines.append(f"_Unavailable: {live_compat_pf.get('reason')}_")
    lines.extend([
        "",
        "## Live Decisions",
        "",
        *_table(live.get("decisions") or [], ["mode", "entry_mode", "eligible", "state", "n"]),
        "",
        "## Venue Attempts",
        "",
        *_table(live.get("venue_attempts") or [], ["venue", "stage", "status", "reason", "n"]),
        "",
        "## Limit Then Taker Timeout Quality",
        "",
    ])
    if ltt.get("available"):
        lines.extend(_table(ltt.get("quality") or [], [
            "branch", "entry_order_type", "exit_order_type", "taker_fallback_used",
            "maker_entry_filled", "maker_entry_missed", "n", "wins", "net_r",
            "net_pnl_usdt", "avg_cost_usdt",
        ]))
        lines.extend(["", "### LTT Missed Or Unfilled", ""])
        lines.extend(_table(ltt.get("missed_or_unfilled") or [], [
            "missed_entry_reason", "entry_fill_status", "n", "latest",
        ]))
    else:
        lines.append(f"_Unavailable: {ltt.get('reason')}_")
    lines.extend([
        "",
        "## Stock Post-Filter Live Cohort",
        "",
    ])
    if stock_cohort.get("available"):
        lines.extend([
            f"- Filter: `{stock_cohort.get('filter_version')}`",
            f"- Cohort start: `{stock_cohort.get('cohort_start')}`",
            "",
            "### Stock Decisions",
            "",
            *_table(stock_cohort.get("decisions") or [], ["entry_mode", "eligible", "state", "n"]),
            "",
            "### Stock Positions",
            "",
            *_table(stock_cohort.get("positions") or [], ["status", "n", "realized_pnl_usdt", "fees_usdt", "latest"]),
            "",
            "### Stock By Entry Mode",
            "",
            *_table(stock_cohort.get("by_entry_mode") or [], ["entry_mode", "status", "n", "realized_pnl_usdt", "avg_risk_usdt"]),
            "",
            "### Stock Recent Rejections",
            "",
            *_table(stock_cohort.get("recent_rejections") or [], [
                "captured_at", "signal_id", "symbol", "entry_mode", "state", "rejection_reasons_json",
            ]),
        ])
    else:
        lines.append(f"_Unavailable: {stock_cohort.get('reason')}_")
    lines.extend([
        "",
        "## Liquidity Sweep V2 Paper",
        "",
    ])
    if sweep.get("available"):
        lines.extend(_table(sweep.get("observations") or [], ["rejection_reason", "n", "latest"]))
        lines.extend(["", "### Sweep V2 Slices", ""])
        lines.extend(_table(sweep.get("slices") or [], [
            "entry_profile", "confirmation_timeframe", "session_bucket", "outcome_status",
            "close_reason", "n", "wins", "net_r", "net_pnl_usd", "avg_latency_sec",
        ]))
        lines.extend(["", "### Latest Evaluations", ""])
        lines.extend(_table(sweep.get("evaluations") or [], [
            "generated_at", "profile_id", "forward_rows", "clean_rows", "clean_closed",
            "net_pnl_usd", "profit_factor", "verdict",
        ]))
    else:
        lines.append(f"_Unavailable: {sweep.get('reason')}_")
    lines.extend(["", "## Crypto Invest", ""])
    if invest.get("available"):
        last_scan = invest.get("last_scan") or {}
        lines.extend([
            f"- Last scan: `{last_scan.get('observed_at') or '-'}` age minutes `{last_scan.get('age_minutes', '-')}` status `{last_scan.get('status', '-')}`",
            f"- Evaluated: `{last_scan.get('evaluated', '-')}` decisions seen `{last_scan.get('decisions_seen', '-')}` inserted `{last_scan.get('decisions_inserted', '-')}`",
            "",
            "### Invest Decisions",
            "",
            *_table(invest.get("decisions") or [], ["status", "rejection_reason", "n", "latest"]),
            "",
            "### Invest Outcomes",
            "",
            *_table(invest.get("outcomes") or [], ["outcome_status", "close_reason", "n", "latest"]),
        ])
    else:
        lines.append(f"_Unavailable: {invest.get('reason')}_")
    return "\n".join(lines) + "\n"


def write_report(*, db: str | Path | None = None, hours: int = 96,
                 out: str | Path | None = None, now: datetime | None = None) -> Path:
    report = build_report(db=db, hours=hours, now=now)
    md = Path(out) if out else DEFAULT_REPORT
    js = md.with_suffix(".json") if out else DEFAULT_JSON
    md.parent.mkdir(parents=True, exist_ok=True)
    md.write_text(render_markdown(report), encoding="utf-8")
    js.write_text(json.dumps(report, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    return md


__all__ = ["build_report", "render_markdown", "write_report"]
