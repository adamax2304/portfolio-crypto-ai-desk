from __future__ import annotations

import json
import math
import sqlite3
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from src.config import load_config
from src.notifiers.telegram import TelegramNotConfigured, TelegramNotifier

from .config import LiveCanaryConfig, load_live_canary_config
from . import store as ls


def _db_path(db: str | Path | None = None) -> Path:
    if db:
        return Path(db)
    return Path(load_config().db_path)


def _parse_utc(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _age_seconds(value: Any, now: datetime) -> float | None:
    parsed = _parse_utc(value)
    if parsed is None:
        return None
    return max(0.0, (now - parsed).total_seconds())


def _load_json(value: Any, default: Any) -> Any:
    try:
        return json.loads(str(value))
    except (TypeError, json.JSONDecodeError):
        return default


def _severity_rank(severity: str) -> int:
    return {"OK": 0, "INFO": 1, "WARNING": 2, "CRITICAL": 3}.get(str(severity).upper(), 1)


def _status_from_issues(issues: list[dict[str, Any]]) -> str:
    # Historical critical events remain visible for audit, but a recovered or
    # closed incident must not keep the *current* watchdog status CRITICAL.
    active = [issue for issue in issues if issue.get("active", True)]
    if any(_severity_rank(issue.get("severity", "")) >= 3 for issue in active):
        return "CRITICAL"
    if active:
        return "WARNING"
    return "OK"


def _issue(key: str, severity: str, title: str, detail: str,
           *, decision_id: str | None = None, symbol: str | None = None,
           payload: dict[str, Any] | None = None, active: bool = True) -> dict[str, Any]:
    return {
        "key": key,
        "severity": severity,
        "title": title,
        "detail": detail,
        "decision_id": decision_id,
        "symbol": symbol,
        "payload": payload or {},
        "active": active,
    }


def _alert_cooldown_seconds(cfg: LiveCanaryConfig) -> float:
    block = cfg.get("watchdog", {}) or {}
    return float(block.get("alert_cooldown_seconds", 900))


def _persistent_alert_repeat_seconds(cfg: LiveCanaryConfig) -> float:
    block = cfg.get("watchdog", {}) or {}
    return float(block.get("persistent_alert_repeat_seconds", _alert_cooldown_seconds(cfg)))


def _watchdog_cfg(cfg: LiveCanaryConfig, key: str, default: float) -> float:
    block = cfg.get("watchdog", {}) or {}
    return float(block.get(key, default))


def _watchdog_bool(cfg: LiveCanaryConfig, key: str, default: bool) -> bool:
    block = cfg.get("watchdog", {}) or {}
    value = block.get(key, default)
    if isinstance(value, str):
        return value.strip().lower() not in {"0", "false", "no", "off"}
    return bool(value)


def _control_write_with_retry(
    conn: sqlite3.Connection,
    sql: str,
    params: tuple[Any, ...],
    *,
    attempts: int = 5,
    sleep_seconds: float = 0.25,
) -> None:
    """Persist watchdog control state through short live-monitor DB locks."""
    for attempt in range(max(1, int(attempts))):
        try:
            conn.execute(sql, params)
            return
        except sqlite3.OperationalError as exc:
            if not ls.is_database_busy(exc) or attempt + 1 >= attempts:
                raise
            time.sleep(max(0.0, sleep_seconds) * (attempt + 1))


def _format_issue_alert(issue: dict[str, Any], *, recovered: bool = False) -> str:
    prefix = "LIVE WATCHDOG RECOVERED" if recovered else "LIVE WATCHDOG ALERT"
    lines = [
        f"{prefix}: {issue.get('severity', 'WARNING')}",
        str(issue.get("title") or issue.get("key") or "unknown issue"),
    ]
    if issue.get("symbol"):
        lines.append(f"Symbol: {issue['symbol']}")
    if issue.get("decision_id"):
        lines.append(f"Decision: {issue['decision_id']}")
    detail = str(issue.get("detail") or "").strip()
    if detail:
        lines.append(detail)
    payload = issue.get("payload") or {}
    if payload:
        compact = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        if len(compact) > 900:
            compact = compact[:900] + "..."
        lines.append(f"Context: {compact}")
    return "\n".join(lines)


def _should_send(conn: sqlite3.Connection, *, key: str, now: datetime,
                 cooldown_seconds: float) -> bool:
    control_key = f"watchdog_alert:{key}"
    row = conn.execute(
        "SELECT control_value FROM mexc_canary_control WHERE control_key=?",
        (control_key,),
    ).fetchone()
    if row:
        payload = _load_json(row[0], {})
        last = _parse_utc(payload.get("sent_at"))
        if last and (now - last).total_seconds() < cooldown_seconds:
            return False
        count = int(payload.get("count") or 0) + 1
        first_sent_at = payload.get("first_sent_at") or now.isoformat()
    else:
        count = 1
        first_sent_at = now.isoformat()
    _control_write_with_retry(
        conn,
        "INSERT INTO mexc_canary_control(control_key,control_value,updated_at) VALUES(?,?,?) "
        "ON CONFLICT(control_key) DO UPDATE SET control_value=excluded.control_value,updated_at=excluded.updated_at",
        (
            control_key,
            json.dumps(
                {"sent_at": now.isoformat(), "first_sent_at": first_sent_at, "count": count},
                sort_keys=True,
            ),
            now.isoformat(),
        ),
    )
    return True


def _load_active_issue_keys(conn: sqlite3.Connection) -> set[str]:
    row = conn.execute(
        "SELECT control_value FROM mexc_canary_control WHERE control_key='watchdog_active_issues'"
    ).fetchone()
    if not row:
        return set()
    payload = _load_json(row[0], [])
    if not isinstance(payload, list):
        return set()
    return {str(item) for item in payload}


def _store_active_issue_keys(conn: sqlite3.Connection, keys: set[str], now: datetime) -> None:
    _control_write_with_retry(
        conn,
        "INSERT INTO mexc_canary_control(control_key,control_value,updated_at) VALUES(?,?,?) "
        "ON CONFLICT(control_key) DO UPDATE SET control_value=excluded.control_value,updated_at=excluded.updated_at",
        ("watchdog_active_issues", json.dumps(sorted(keys)), now.isoformat()),
    )


def _send_deduped_alerts(
    *, conn: sqlite3.Connection, issues: list[dict[str, Any]], cfg: LiveCanaryConfig,
    notifier: Any | None, send_telegram: bool, now: datetime,
) -> dict[str, Any]:
    active_issues = [issue for issue in issues if issue.get("active", True)]
    active_keys = {str(issue["key"]) for issue in active_issues}
    previous_keys = _load_active_issue_keys(conn)
    recovered = previous_keys - active_keys
    _store_active_issue_keys(conn, active_keys, now)
    alerts_sent: list[str] = []
    alert_errors: list[str] = []
    recoveries_sent: list[str] = []
    if not send_telegram:
        return {
            "alerts_sent": alerts_sent,
            "recoveries_sent": recoveries_sent,
            "alert_errors": alert_errors,
        }
    notifier = notifier or TelegramNotifier(load_config().root / "config" / "notifications.yaml")
    cooldown = _alert_cooldown_seconds(cfg)
    persistent_cooldown = _persistent_alert_repeat_seconds(cfg)
    max_alerts = max(1, int((cfg.get("watchdog", {}) or {}).get("max_alerts_per_tick", 3)))
    prioritized = sorted(
        active_issues,
        key=lambda issue: _severity_rank(str(issue.get("severity") or "")),
        reverse=True,
    )
    for issue in prioritized[:max_alerts]:
        key = str(issue["key"])
        if not _should_send(conn, key=key, now=now, cooldown_seconds=persistent_cooldown):
            continue
        try:
            send = getattr(notifier, "send_fast", None) or notifier.send
            send(_format_issue_alert(issue), parse_mode="")
            alerts_sent.append(key)
        except TelegramNotConfigured as exc:
            alert_errors.append(f"{key}:TelegramNotConfigured:{exc}")
        except Exception as exc:
            alert_errors.append(f"{key}:{type(exc).__name__}:{str(exc)[:160]}")
    if _watchdog_bool(cfg, "send_recovery_alerts", True):
        for key in sorted(recovered)[:max_alerts]:
            issue = {"key": key, "severity": "OK", "title": key, "detail": "Issue is no longer active."}
            if not _should_send(conn, key=f"recovered:{key}", now=now, cooldown_seconds=cooldown):
                continue
            try:
                send = getattr(notifier, "send_fast", None) or notifier.send
                send(_format_issue_alert(issue, recovered=True), parse_mode="")
                recoveries_sent.append(key)
            except Exception as exc:
                alert_errors.append(f"recovered:{key}:{type(exc).__name__}:{str(exc)[:160]}")
    return {
        "alerts_sent": alerts_sent,
        "recoveries_sent": recoveries_sent,
        "alert_errors": alert_errors,
    }


def _outbox_issues(conn: sqlite3.Connection, cfg: LiveCanaryConfig,
                   now: datetime) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    processing_stale = _watchdog_cfg(cfg, "processing_stale_seconds", 45)
    rows = [dict(row) for row in conn.execute(
        "SELECT o.*,d.symbol,d.mode,d.entry_mode,d.decision_json,d.captured_at "
        "FROM mexc_canary_outbox o JOIN mexc_canary_decisions d ON d.decision_id=o.decision_id "
        "WHERE o.status IN ('QUEUED','PROCESSING')"
    ).fetchall()]
    for row in rows:
        decision = _load_json(row.get("decision_json"), {})
        entry_mode = str(row.get("entry_mode") or decision.get("entry_mode") or "").upper()
        mode = str(row.get("mode") or decision.get("mode") or "").lower()
        max_age = cfg.entry_limit("max_entry_age_seconds", entry_mode, 45.0, mode=mode)
        wait_age = _age_seconds(row.get("captured_at") or row.get("created_at"), now)
        total_age = (wait_age or 0.0) + max(0.0, float(decision.get("entry_age_seconds") or 0.0))
        if math.isfinite(total_age) and total_age > max_age:
            issues.append(_issue(
                f"stale_outbox:{row['decision_id']}",
                "CRITICAL",
                "Queued live decision exceeded its point-in-time entry window",
                "The watchdog will not submit a stale order; invalidate/requeue requires a fresh Paper event.",
                decision_id=str(row["decision_id"]),
                symbol=str(row.get("symbol") or ""),
                payload={
                    "status": row.get("status"),
                    "entry_mode": entry_mode,
                    "total_entry_age_seconds": round(total_age, 3),
                    "max_entry_age_seconds": max_age,
                },
            ))
        if str(row.get("status") or "").upper() == "PROCESSING":
            processing_age = _age_seconds(row.get("claimed_at"), now)
            if processing_age is None or processing_age > processing_stale:
                issues.append(_issue(
                    f"stuck_processing:{row['decision_id']}",
                    "CRITICAL",
                    "Live decision is stuck in PROCESSING",
                    "The worker may have died during preflight/submission; manual review is required before retry.",
                    decision_id=str(row["decision_id"]),
                    symbol=str(row.get("symbol") or ""),
                    payload={"processing_age_seconds": processing_age, "limit_seconds": processing_stale},
                ))
    return issues


def _position_issues(conn: sqlite3.Connection, cfg: LiveCanaryConfig,
                     now: datetime) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    stale_limit = _watchdog_cfg(cfg, "open_position_reconcile_stale_seconds", 20)
    grace = _watchdog_cfg(cfg, "unprotected_position_grace_seconds", 30)
    positions = [dict(row) for row in conn.execute(
        "SELECT * FROM mexc_canary_positions WHERE status='OPEN'"
    ).fetchall()]
    for pos in positions:
        decision_id = str(pos["decision_id"])
        opened_age = _age_seconds(pos.get("opened_at"), now)
        reconciled_age = _age_seconds(pos.get("last_reconciled_at"), now)
        old_enough = opened_age is None or opened_age > grace
        if old_enough and (reconciled_age is None or reconciled_age > stale_limit):
            issues.append(_issue(
                f"position_reconcile_stale:{decision_id}",
                "CRITICAL",
                "Open live position has stale reconciliation",
                "Protective stop/TP state may be stale. The monitor should reconcile this position every few seconds.",
                decision_id=decision_id,
                symbol=str(pos.get("symbol") or ""),
                payload={
                    "opened_age_seconds": opened_age,
                    "last_reconciled_age_seconds": reconciled_age,
                    "limit_seconds": stale_limit,
                },
            ))
        if int(pos.get("monitor_error_count") or 0) > 0:
            issues.append(_issue(
                f"position_monitor_errors:{decision_id}",
                "CRITICAL",
                "Open live position has monitor errors",
                "The latest reconcile tick failed for this position.",
                decision_id=decision_id,
                symbol=str(pos.get("symbol") or ""),
                payload={
                    "monitor_error_count": int(pos.get("monitor_error_count") or 0),
                    "last_monitor_error_at": pos.get("last_monitor_error_at"),
                },
            ))
        legs = [dict(row) for row in conn.execute(
            "SELECT * FROM mexc_canary_exit_legs WHERE decision_id=?",
            (decision_id,),
        ).fetchall()]
        trusted_legs = [
            leg for leg in legs
            if (
                str(leg.get("order_kind") or "") == "CLOSE_LIMIT_TP"
                and str(leg.get("status") or "") in {"ACTIVE", "FILLED"}
            ) or (
                int(leg.get("leg_index") or 0) == 3
                and str(leg.get("order_kind") or "") == "VIRTUAL_TP3_MONITOR"
                and str(leg.get("status") or "") in {"ACTIVE", "SUBMITTED", "FILLED"}
            ) or (
                str(leg.get("order_kind") or "") == "BYBIT_REDUCE_ONLY_TP"
                and str(leg.get("status") or "") in {"ACTIVE", "FILLED"}
            )
        ]
        if old_enough and len(trusted_legs) != 3:
            issues.append(_issue(
                f"position_tp_legs_incomplete:{decision_id}",
                "CRITICAL",
                "Open live position does not have three trusted TP lifecycle legs recorded",
                "The reconcile path must verify the native limits and any configured monitored TP3 runner.",
                decision_id=decision_id,
                symbol=str(pos.get("symbol") or ""),
                payload={
                    "trusted_tp_legs": len(trusted_legs),
                    "total_leg_rows": len(legs),
                    "expected": 3,
                },
            ))
        if old_enough and not str(pos.get("tpsl_order_id") or "").strip():
            issues.append(_issue(
                f"position_stop_missing:{decision_id}",
                "CRITICAL",
                "Open live position has no verified protective stop id recorded",
                "The reconcile path must verify a position-wide stop before the trade can be considered protected.",
                decision_id=decision_id,
                symbol=str(pos.get("symbol") or ""),
            ))
    return issues


def _risk_issues(conn: sqlite3.Connection, cfg: LiveCanaryConfig) -> list[dict[str, Any]]:
    row = conn.execute(
        "SELECT COALESCE(SUM(risk_usdt),0),COALESCE(SUM(margin_usdt),0),COALESCE(SUM(notional_usdt),0) "
        "FROM mexc_canary_risk_reservations WHERE status IN ('RESERVED','OPEN')"
    ).fetchone()
    active_risk = float(row[0] or 0.0)
    if active_risk <= cfg.max_concurrent_risk_usdt + 1e-9:
        return []
    return [_issue(
        "active_risk_over_cap",
        "CRITICAL",
        "Canary-owned active risk exceeds configured cap",
        "New entries should be blocked by reservation logic; review reservations and exchange state.",
        payload={
            "active_risk_usdt": active_risk,
            "max_concurrent_risk_usdt": cfg.max_concurrent_risk_usdt,
            "active_margin_usdt": float(row[1] or 0.0),
            "active_notional_usdt": float(row[2] or 0.0),
        },
    )]


def _lifecycle_integrity_issues(
    conn: sqlite3.Connection, cfg: LiveCanaryConfig, now: datetime
) -> list[dict[str, Any]]:
    """Check the one-to-one decision -> queue -> order -> position -> alert chain."""
    issues: list[dict[str, Any]] = []
    grace = _watchdog_cfg(cfg, "lifecycle_integrity_grace_seconds", 30)
    cutoff = (now - timedelta(seconds=grace)).isoformat()
    notification_cutoff = (now - timedelta(days=7)).isoformat()
    missing_outbox = conn.execute(
        "SELECT d.decision_id,d.symbol FROM mexc_canary_decisions d "
        "LEFT JOIN mexc_canary_outbox o ON o.decision_id=d.decision_id "
        "WHERE d.eligible=1 AND d.captured_at<? AND o.decision_id IS NULL LIMIT 20",
        (cutoff,),
    ).fetchall()
    for row in missing_outbox:
        issues.append(_issue(
            f"eligible_without_outbox:{row['decision_id']}", "CRITICAL",
            "Eligible live decision has no execution outbox row",
            "The capture transaction did not produce a queue item.",
            decision_id=str(row["decision_id"]), symbol=str(row["symbol"]),
        ))
    missing_order = conn.execute(
        "SELECT o.decision_id,d.symbol,o.status FROM mexc_canary_outbox o "
        "JOIN mexc_canary_decisions d ON d.decision_id=o.decision_id "
        "LEFT JOIN mexc_canary_orders x ON x.decision_id=o.decision_id "
        "WHERE o.status IN ('SUBMITTED','SUBMISSION_UNKNOWN') AND o.completed_at<? "
        "AND x.decision_id IS NULL LIMIT 20",
        (cutoff,),
    ).fetchall()
    for row in missing_order:
        issues.append(_issue(
            f"submitted_without_order:{row['decision_id']}", "CRITICAL",
            "Submitted outbox item has no persisted exchange order",
            "Submission state cannot be reconciled safely without its deterministic order id.",
            decision_id=str(row["decision_id"]), symbol=str(row["symbol"]),
        ))
    missing_position = conn.execute(
        "SELECT o.decision_id,o.symbol FROM mexc_canary_orders o "
        "LEFT JOIN mexc_canary_positions p ON p.decision_id=o.decision_id "
        "WHERE o.status='FILLED' AND o.updated_at<? AND p.decision_id IS NULL LIMIT 20",
        (cutoff,),
    ).fetchall()
    for row in missing_position:
        issues.append(_issue(
            f"filled_without_position:{row['decision_id']}", "CRITICAL",
            "Exchange-confirmed fill has no local position lifecycle",
            "Risk and protective orders cannot be proven from the local ledger.",
            decision_id=str(row["decision_id"]), symbol=str(row["symbol"]),
        ))
    missing_alert = conn.execute(
        "SELECT o.decision_id,o.symbol FROM mexc_canary_orders o "
        "LEFT JOIN mexc_canary_notification_outbox n ON n.decision_id=o.decision_id "
        "AND n.notification_kind='LIVE_ENTRY_FILLED' "
        "WHERE o.status='FILLED' AND o.updated_at<? AND o.updated_at>=? "
        "AND n.notification_id IS NULL LIMIT 20",
        (cutoff, notification_cutoff),
    ).fetchall()
    if missing_alert:
        issues.append(_issue(
            "filled_notifications_missing", "WARNING",
            "Recent live fill confirmations have not been staged",
            "Execution is authoritative; the notification repair queue will stage these independently.",
            payload={
                "count": len(missing_alert),
                "decisions": [str(row["decision_id"]) for row in missing_alert],
                "symbols": sorted({str(row["symbol"]) for row in missing_alert}),
                "lookback_days": 7,
            },
        ))
    duplicate_keys = conn.execute(
        "SELECT economic_trade_key,COUNT(*) n,GROUP_CONCAT(decision_id) ids "
        "FROM mexc_canary_decisions WHERE economic_trade_key IS NOT NULL AND economic_trade_key<>'' "
        "AND (state IN ('QUEUED','PROCESSING','SUBMITTED','SUBMISSION_UNKNOWN') OR EXISTS("
        "SELECT 1 FROM mexc_canary_positions p WHERE p.decision_id=mexc_canary_decisions.decision_id)) "
        "GROUP BY economic_trade_key HAVING COUNT(*)>1 LIMIT 20"
    ).fetchall()
    for row in duplicate_keys:
        issues.append(_issue(
            f"duplicate_economic_trade:{row['economic_trade_key']}", "CRITICAL",
            "The same economic trade is active more than once",
            "New recovery and alternate signal ids must not create duplicate exposure.",
            payload={"decisions": str(row["ids"]).split(","), "count": int(row["n"])},
        ))
    return issues


def _heartbeat_issues(conn: sqlite3.Connection, cfg: LiveCanaryConfig,
                      now: datetime) -> list[dict[str, Any]]:
    heartbeat = ls.monitor_heartbeat(conn)
    stale_limit = _watchdog_cfg(cfg, "heartbeat_stale_seconds", 120)
    if not heartbeat:
        return [_issue(
            "monitor_heartbeat_missing",
            "CRITICAL",
            "MEXC live monitor heartbeat is missing",
            "The execution monitor may not be running.",
        )]
    age = _age_seconds(heartbeat.get("at") or heartbeat.get("updated_at"), now)
    if age is None or age > stale_limit:
        return [_issue(
            "monitor_heartbeat_stale",
            "CRITICAL",
            "MEXC live monitor heartbeat is stale",
            "The execution monitor may be dead or blocked.",
            payload={"heartbeat_age_seconds": age, "limit_seconds": stale_limit, "heartbeat": heartbeat},
        )]
    return []


def _recent_event_issues(conn: sqlite3.Connection, cfg: LiveCanaryConfig,
                         now: datetime) -> list[dict[str, Any]]:
    lookback = _watchdog_cfg(cfg, "critical_event_lookback_minutes", 60)
    block = cfg.get("watchdog", {}) or {}
    suppressed = {
        str(value).strip().upper()
        for value in (block.get("suppress_recent_event_types") or [])
        if str(value).strip()
    }
    aggregate = _watchdog_bool(cfg, "aggregate_recent_critical_events", False)
    since = (now - timedelta(minutes=lookback)).isoformat()
    events = [dict(row) for row in conn.execute(
        "SELECT event_id,event_at,decision_id,event_type,severity,payload_json "
        "FROM mexc_canary_events WHERE severity='CRITICAL' AND event_at>=? "
        "ORDER BY event_id DESC LIMIT 20",
        (since,),
    ).fetchall()]
    issues: list[dict[str, Any]] = []
    grouped: dict[str, dict[str, Any]] = {}
    for event in events:
        event_type = str(event.get("event_type") or "")
        if event_type.startswith("LIVE_WATCHDOG_"):
            continue
        if event_type.upper() in suppressed:
            continue
        payload = _load_json(event.get("payload_json"), {})
        if event_type == "KILL_SWITCH_CHANGED" and str(payload.get("state") or "").upper() != "TRIPPED":
            continue
        if aggregate:
            group = grouped.setdefault(event_type, {
                "count": 0,
                "latest_event_at": event.get("event_at"),
                "latest_event_id": event.get("event_id"),
                "latest_payload": payload,
                "sample_decision_ids": [],
            })
            group["count"] += 1
            decision_id = str(event.get("decision_id") or "").strip()
            if decision_id and decision_id not in group["sample_decision_ids"]:
                group["sample_decision_ids"].append(decision_id)
            continue
        issues.append(_issue(
            f"critical_event:{event['event_id']}",
            "CRITICAL",
            f"Recent critical live event: {event_type}",
            str(event.get("event_at") or ""),
            decision_id=str(event.get("decision_id") or "") or None,
            payload=payload,
            active=False,
        ))
    if aggregate:
        for event_type, payload in grouped.items():
            issues.append(_issue(
                f"critical_event_type:{event_type}",
                "CRITICAL",
                f"Recent critical live events: {event_type}",
                str(payload.get("latest_event_at") or ""),
                payload={
                    "count": payload.get("count"),
                    "latest_event_id": payload.get("latest_event_id"),
                    "latest_event_at": payload.get("latest_event_at"),
                    "sample_decision_ids": payload.get("sample_decision_ids")[:5],
                    "latest_payload": payload.get("latest_payload") or {},
                },
                active=False,
            ))
    return issues


def _recent_preflight_rejection_issues(conn: sqlite3.Connection, cfg: LiveCanaryConfig,
                                       now: datetime) -> list[dict[str, Any]]:
    block = cfg.get("watchdog", {}) or {}
    if block.get("alert_preflight_rejections", True) is False:
        return []
    lookback = _watchdog_cfg(cfg, "preflight_rejection_lookback_minutes", 60)
    since = (now - timedelta(minutes=lookback)).isoformat()
    rows = [dict(row) for row in conn.execute(
        "SELECT o.outbox_id,o.decision_id,o.status,o.completed_at,o.last_error,o.result_json,"
        "d.symbol,d.mode,d.entry_mode "
        "FROM mexc_canary_outbox o "
        "JOIN mexc_canary_decisions d ON d.decision_id=o.decision_id "
        "WHERE o.status IN ('REJECTED_PREFLIGHT','REJECTED_SUBMISSION') "
        "AND COALESCE(o.completed_at,o.created_at)>=? "
        "ORDER BY COALESCE(o.completed_at,o.created_at) DESC LIMIT 20",
        (since,),
    ).fetchall()]
    issues: list[dict[str, Any]] = []
    for row in rows:
        result = _load_json(row.get("result_json"), {})
        reason = str(result.get("reason") or row.get("last_error") or "preflight rejected")
        submission = str(row.get("status") or "") == "REJECTED_SUBMISSION"
        issues.append(_issue(
            f"{'submission' if submission else 'preflight'}_rejected:{row['decision_id']}",
            "WARNING",
            ("MEXC rejected a live order submission" if submission
             else "MEXC live preflight rejected a queued candidate"),
            "No real order was sent. Review the reason before assuming the Paper signal reached MEXC.",
            decision_id=str(row["decision_id"]),
            symbol=str(row.get("symbol") or ""),
            payload={
                "reason": reason,
                "mode": row.get("mode"),
                "entry_mode": row.get("entry_mode"),
                "completed_at": row.get("completed_at"),
            },
        ))
    return issues


def _preflight_transport_degraded_issue(conn: sqlite3.Connection, cfg: LiveCanaryConfig,
                                        now: datetime) -> list[dict[str, Any]]:
    """Surface a MEXC API incident before it silently costs several live fills."""
    block = cfg.get("watchdog", {}) or {}
    window = float(block.get("preflight_transport_failure_lookback_seconds", 180))
    threshold = int(block.get("preflight_transport_failure_threshold", 2))
    if threshold <= 0:
        return []
    since = (now - timedelta(seconds=window)).isoformat()
    row = conn.execute(
        "SELECT COUNT(*) FROM mexc_canary_events "
        "WHERE event_type='ORDER_PREFLIGHT_TRANSIENT_RETRY' AND event_at>=? "
        "AND lower(payload_json) LIKE '%transport%'",
        (since,),
    ).fetchone()
    failures = int(row[0] or 0)
    if failures < threshold:
        return []
    open_positions = int(conn.execute(
        "SELECT COUNT(*) FROM mexc_canary_positions WHERE status='OPEN'"
    ).fetchone()[0] or 0)
    return [_issue(
        "mexc_preflight_transport_degraded",
        "CRITICAL" if open_positions else "WARNING",
        "MEXC preflight transport is degraded",
        "Several candidates hit temporary MEXC transport failures. Valid rows are isolated and retried only inside their own entry windows.",
        payload={
            "transient_failures": failures,
            "window_seconds": window,
            "threshold": threshold,
            "open_positions": open_positions,
        },
    )]


def _quality_agent_issues(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """Surface only ongoing objective incidents on an active live lifecycle.

    Point-in-time rejected candidates are stored as OBSERVED evidence and do
    not create Telegram noise. ACTIVE is reserved for a condition that still
    affects a queued order or open position.
    """
    if not conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' "
        "AND name='quality_agent_execution_incidents'"
    ).fetchone():
        return []
    rows = [dict(row) for row in conn.execute(
        "SELECT q.* FROM quality_agent_execution_incidents q "
        "WHERE q.status='ACTIVE' AND q.objective=1 AND q.decision_id IS NOT NULL "
        "AND q.stage<>'live_post_ack' AND ("
        " EXISTS(SELECT 1 FROM mexc_canary_outbox o WHERE o.decision_id=q.decision_id "
        "        AND o.status IN ('QUEUED','PROCESSING','SUBMITTED','SUBMISSION_UNKNOWN')) OR "
        " EXISTS(SELECT 1 FROM mexc_canary_positions p WHERE p.decision_id=q.decision_id "
        "        AND p.status='OPEN'))"
    ).fetchall()]
    return [
        _issue(
            f"quality_agent:{row['incident_key']}", str(row.get("severity") or "WARNING"),
            f"Quality-agent execution incident: {row.get('incident_type')}",
            "The objective execution condition remains active on a live lifecycle.",
            decision_id=str(row.get("decision_id") or "") or None,
            symbol=str(row.get("symbol") or "") or None,
            payload=_load_json(row.get("detail_json"), {}),
        )
        for row in rows
    ]


def audit(
    *, db: str | Path | None = None, cfg: LiveCanaryConfig | None = None,
    reconcile_result: dict[str, Any] | None = None,
    send_telegram: bool = False, notifier: Any | None = None,
    check_heartbeat: bool = True, now: datetime | None = None,
) -> dict[str, Any]:
    """Audit live execution safety and optionally alert on issue transitions.

    The watchdog does not create entries and does not bypass the canary policy.
    It observes the live DB state after the normal worker/reconcile path has had
    a chance to repair stop/TP state.
    """
    cfg = cfg or load_live_canary_config()
    path = _db_path(db)
    now = now or datetime.now(timezone.utc)
    issues: list[dict[str, Any]] = []
    db_busy_timeout_ms = int(_watchdog_cfg(cfg, "db_busy_timeout_ms", 15000))
    with ls.connect(path, busy_timeout_ms=db_busy_timeout_ms) as conn:
        ls.ensure_tables(conn)
        kill_switch = ls.kill_switch_state(conn)
        if kill_switch != "CLEAR":
            issues.append(_issue(
                "kill_switch_tripped",
                "CRITICAL",
                "MEXC live kill switch is TRIPPED",
                "No new canary orders should be submitted until the cause is reviewed.",
                payload={"kill_switch": kill_switch},
            ))
        if check_heartbeat:
            issues.extend(_heartbeat_issues(conn, cfg, now))
        issues.extend(_outbox_issues(conn, cfg, now))
        issues.extend(_position_issues(conn, cfg, now))
        issues.extend(_risk_issues(conn, cfg))
        if bool((cfg.get("watchdog", {}) or {}).get("lifecycle_integrity_enabled", False)):
            issues.extend(_lifecycle_integrity_issues(conn, cfg, now))
        issues.extend(_recent_preflight_rejection_issues(conn, cfg, now))
        issues.extend(_preflight_transport_degraded_issue(conn, cfg, now))
        issues.extend(_quality_agent_issues(conn))
        issues.extend(_recent_event_issues(conn, cfg, now))
        if reconcile_result and str(reconcile_result.get("status") or "") == "DEGRADED":
            nested = reconcile_result.get("venues") or {}
            venue_errors = []
            venue_orders = 0
            venue_positions = 0
            for venue, result in nested.items():
                if not isinstance(result, dict):
                    continue
                venue_errors.extend(
                    {"venue": venue, "error": error}
                    for error in (result.get("errors") or [])
                )
                venue_orders += int(result.get("orders_checked") or 0)
                venue_positions += int(result.get("positions_checked") or 0)
            issues.append(_issue(
                "current_reconcile_degraded",
                "CRITICAL",
                "Current live execution reconcile tick is DEGRADED",
                "The monitor reported errors while checking orders or positions.",
                payload={
                    "errors": (reconcile_result.get("errors") or []) + venue_errors,
                    "orders_checked": reconcile_result.get("orders_checked") or venue_orders,
                    "positions_checked": reconcile_result.get("positions_checked") or venue_positions,
                },
            ))
        # Persist the same post-ack facts for agent effectiveness/forensics.
        # The existing watchdog remains the only alert owner, avoiding duplicate
        # Telegram messages for one protection or reconciliation defect.
        try:
            from src.quality_agents.runner import record_watchdog_observations

            record_watchdog_observations(conn, issues)
        except Exception as exc:
            ls.event_if_due(
                conn,
                "QUALITY_AGENT_POST_ACK_CAPTURE_FAILED",
                severity="WARNING",
                payload={"error_type": type(exc).__name__},
                cooldown_seconds=300,
            )
        alert_result = _send_deduped_alerts(
            conn=conn, issues=issues, cfg=cfg, notifier=notifier,
            send_telegram=send_telegram, now=now,
        )
        journaled = set(alert_result.get("alerts_sent") or [])
        for issue in issues:
            if str(issue.get("key") or "") not in journaled:
                continue
            ls.event(
                conn,
                "LIVE_WATCHDOG_ALERT_SENT",
                decision_id=issue.get("decision_id"),
                severity=str(issue.get("severity") or "WARNING"),
                payload={
                    "key": issue.get("key"),
                    "title": issue.get("title"),
                    "detail": issue.get("detail"),
                    "symbol": issue.get("symbol"),
                    "payload": issue.get("payload") or {},
                },
            )
        for key in alert_result.get("recoveries_sent") or []:
            ls.event(
                conn,
                "LIVE_WATCHDOG_RECOVERED",
                severity="INFO",
                payload={"key": key},
            )
        conn.commit()
    status = _status_from_issues([i for i in issues if i.get("active", True)])
    return {
        "status": status,
        "issues": issues,
        "issue_count": len(issues),
        **alert_result,
    }
