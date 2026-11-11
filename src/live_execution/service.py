from __future__ import annotations

import json
import hashlib
import math
import sqlite3
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from src.config import load_config
from src.execution.stop_contract import is_structural_stop_contract, stop_contract_label

from .config import LiveCanaryConfig, load_live_canary_config
from .mexc_client import MexcAPIError, MexcFuturesClient
from .bybit_client import BybitAPIError, BybitFuturesClient
from .bybit_execution import reconcile_once as reconcile_bybit_once, submit_entry as submit_bybit_entry
from .candle_extremes import completed_post_entry_extreme
from .venue_router import (
    VenueCandidate, bybit_client as make_bybit_client, prepare_candidate, select_candidate,
)
from .policy import evaluate_paper_candidate
from .routing_registry import route as registered_route
from .sizing import (
    PlanRejected, allocate_partial_tp_volumes, build_mexc_pretrade_parity,
    build_order_plan, model_f_stop, rebase_filled_plan, stop_risk_components,
)
from . import store as ls


_LIVE_CAPTURE_DB_TIMEOUT_SECONDS = 15.0
_LIVE_CAPTURE_DB_BUSY_TIMEOUT_MS = 15_000
_LAST_STALE_QUEUE_MAINTENANCE_MONOTONIC = 0.0


def _emit_live_latency(db: Any, event_type: str, decision: dict[str, Any], *,
                       note: dict[str, Any] | None = None,
                       event_at: datetime | None = None) -> None:
    """Best-effort MEXC handoff telemetry; never participates in execution."""
    try:
        from src.signals import latency_telemetry

        venue = "bybit" if str(event_type).lower().startswith("bybit_") else "mexc"
        latency_telemetry.emit_once(
            db,
            event_type=event_type,
            signal_id=str(decision.get("signal_id") or "") or None,
            symbol=str(decision.get("symbol") or "") or None,
            asset_class=str(decision.get("asset_class") or "crypto"),
            mode=str(decision.get("mode") or "") or None,
            source=f"{venue}-live",
            event_at=(event_at or datetime.now(timezone.utc)).isoformat(),
            entry_time_basis=decision.get("entry_time_basis"),
            current_price_revalidated=decision.get("current_price_revalidated"),
            note=json.dumps(note or {}, sort_keys=True),
        )
    except Exception:
        pass


def _db_path(db: str | Path | None) -> Path:
    return Path(db) if db else load_config().db_path


def _record_venue_route_attempts(
    conn: Any,
    *,
    decision_id: str,
    diagnostic: dict[str, Any] | None,
) -> bool:
    """Persist every venue result from one parallel route preflight.

    ``select_candidate`` already runs both exchanges against the same immutable
    decision. This helper only makes those facts queryable; it never changes
    selection, sizing, retries or fallback policy.
    """
    try:
        data = dict(diagnostic or {})
        candidates = data.get("candidates") if isinstance(data.get("candidates"), dict) else {}
        rejected = data.get("rejected") if isinstance(data.get("rejected"), dict) else {}
        # NO_ELIGIBLE_EXECUTION_VENUE returns per-venue evidence here because no
        # normal route diagnostic can be constructed.
        if not rejected and isinstance(data.get("venues"), dict):
            rejected = data["venues"]
        selected = str(data.get("selected") or "").lower()
        selection_reason = str(data.get("selection_reason") or "") or None
        for venue, details in candidates.items():
            ls.record_venue_attempt(
                conn, decision_id=decision_id, venue=str(venue), stage="PREFLIGHT",
                status="PASSED", diagnostic=(details if isinstance(details, dict) else {"detail": details}),
            )
        for venue, details in rejected.items():
            item = details if isinstance(details, dict) else {"detail": details}
            ls.record_venue_attempt(
                conn, decision_id=decision_id, venue=str(venue), stage="PREFLIGHT",
                status="REJECTED", reason=str(item.get("reason") or "venue preflight rejected"), diagnostic=item,
            )
        if selected:
            ls.record_venue_attempt(
                conn, decision_id=decision_id, venue=selected, stage="ROUTE_SELECTION",
                status="SELECTED", reason=selection_reason, diagnostic=data,
            )
    except sqlite3.DatabaseError:
        # Routing facts are valuable, but an audit write must never be the
        # reason an already-validated exchange submission is delayed or lost.
        return False
    return True


def _live_notification_config_path() -> Path:
    return Path(__file__).resolve().parents[2] / "config" / "notifications.yaml"


def _render_live_fill_notification(row: dict[str, Any], plan: dict[str, Any], *, active_exit_legs: int) -> str:
    """Render an operator message from exchange-confirmed, persisted facts only."""
    symbol = str(row.get("symbol") or plan.get("symbol") or "?").replace("_", "/")
    direction = str(row.get("direction") or plan.get("direction") or "").upper()
    venue = str(row.get("venue") or plan.get("venue") or "mexc").upper()
    entry = float(row.get("entry_price") or 0.0)
    stop = float(row.get("current_stop") or row.get("original_stop") or 0.0)
    risk = float(row.get("risk_usdt") or 0.0)
    leverage = int(row.get("leverage") or 0)
    tps = [plan.get("tp1"), plan.get("tp2"), plan.get("tp3")]
    tps_line = " · ".join(f"{float(value):.8g}" for value in tps if value not in (None, "")) or "—"
    protection = (
        f"✅ Защита: {active_exit_legs} TP + stop активны"
        if active_exit_legs else "⏳ Защита: устанавливается"
    )
    return "\n".join([
        f"🟢 LIVE FILLED · {venue}",
        f"{symbol} · {direction}",
        "",
        f"Вход  {entry:.8g}   ·   {leverage}x",
        f"SL      {stop:.8g}",
        f"Риск при входе  ${risk:.2f}",
        f"TP      {tps_line}",
        "",
        protection,
    ])


def _render_live_preflight_rejection_notification(decision: dict[str, Any], reason: str) -> str:
    """Explain a definitive live preflight rejection without implying an order existed."""
    symbol = str(decision.get("display_symbol") or decision.get("symbol") or "?").replace("_", "/")
    direction = str(decision.get("direction") or "").upper()
    explanations = {
        "MEXC_NATIVE_GEOMETRY_INVALID": (
            "биржевая цена или шаг цены уже не сохраняли связку вход -> SL -> 3 TP."
        ),
        "NO_ELIGIBLE_EXECUTION_VENUE": "ни одна доступная биржа не прошла безопасный preflight.",
        "ENTRY_DRIFT_TOO_LARGE": "цена ушла дальше допустимого входа.",
        "MEXC_PARITY_REQUIRED": "MEXC не подтвердил соответствие цены и защитных ордеров.",
        "INSUFFICIENT_AVAILABLE_MARGIN": "на бирже не хватило доступной маржи для рассчитанного риска.",
    }
    detail = explanations.get(str(reason), f"preflight отклонён: {reason}.")
    return "\n".join([
        "🟡 LIVE НЕ ОТКРЫТ",
        f"{symbol} · {direction}",
        "",
        f"Причина: {detail}",
        "Paper-сделка остаётся только в Paper; реальный ордер не отправлялся.",
    ])


def _stage_live_preflight_rejection_notification(
    path: Path, *, decision_id: str, decision: dict[str, Any], reason: str,
) -> bool:
    """Persist a one-time operator notice; notification delivery never affects execution."""
    with ls.connect(path) as conn:
        ls.ensure_tables(conn)
        staged = ls.enqueue_notification(
            conn,
            decision_id=decision_id,
            notification_kind="LIVE_PREFLIGHT_REJECTED",
            message_text=_render_live_preflight_rejection_notification(decision, reason),
        )
        if staged:
            ls.event(
                conn, "LIVE_PREFLIGHT_REJECTION_NOTIFICATION_STAGED",
                decision_id=decision_id, severity="WARNING", payload={"reason": reason},
            )
        conn.commit()
    return staged


def _stage_missing_live_fill_notifications(path: Path, *, now: datetime | None = None) -> int:
    """Stage exchange-confirmed fills that have no delivery record yet.

    A position can hit its stop before the next Telegram retry.  Reading only
    OPEN positions permanently lost those confirmations, so the repair source
    is now the immutable FILLED order joined to its position, open or closed.
    """
    now = now or datetime.now(timezone.utc)
    cutoff = (now - timedelta(days=7)).isoformat()
    staged = 0
    with ls.connect(path) as conn:
        ls.ensure_tables(conn)
        rows = [dict(row) for row in conn.execute(
            "SELECT p.*,o.plan_json,o.updated_at AS fill_recorded_at,o.venue AS order_venue "
            "FROM mexc_canary_orders o LEFT JOIN mexc_canary_positions p "
            "ON p.decision_id=o.decision_id "
            "WHERE o.status='FILLED' AND o.updated_at>=? "
            "AND p.decision_id IS NOT NULL "
            "AND NOT EXISTS (SELECT 1 FROM mexc_canary_notification_outbox n "
            "WHERE n.decision_id=o.decision_id AND n.notification_kind='LIVE_ENTRY_FILLED')",
            (cutoff,),
        ).fetchall()]
        for row in rows:
            try:
                plan = json.loads(str(row.get("plan_json") or "{}"))
            except (TypeError, ValueError):
                plan = {}
            active_exit_legs = int(conn.execute(
                "SELECT COUNT(*) FROM mexc_canary_exit_legs "
                "WHERE decision_id=? AND status='ACTIVE'", (row["decision_id"],)
            ).fetchone()[0])
            message = _render_live_fill_notification(row, plan, active_exit_legs=active_exit_legs)
            if ls.enqueue_notification(
                conn, decision_id=str(row["decision_id"]),
                notification_kind="LIVE_ENTRY_FILLED", message_text=message,
            ):
                ls.event(conn, "LIVE_ENTRY_NOTIFICATION_STAGED", decision_id=str(row["decision_id"]),
                         payload={"venue": row.get("venue"), "symbol": row.get("symbol")})
                staged += 1
        conn.commit()
    return staged


def _deliver_live_fill_notifications(path: Path, *, notifier: Any | None = None,
                                     now: datetime | None = None, limit: int = 5) -> dict[str, int | str]:
    """Deliver fill confirmations after persistence; failures stay retryable and never affect orders."""
    now = now or datetime.now(timezone.utc)
    staged = _stage_missing_live_fill_notifications(path, now=now)
    # Staging timestamps with the actual wall clock.  Refresh the due horizon
    # so a newly staged message is sent in this monitor tick rather than being
    # held until the next tick by a sub-second timestamp difference.
    delivery_now = datetime.now(timezone.utc)
    if notifier is None:
        try:
            from src.notifiers.telegram import TelegramNotifier
            notifier = TelegramNotifier(_live_notification_config_path())
        except Exception as exc:
            return {"staged": staged, "sent": 0, "failed": 0, "status": f"notifier_error:{type(exc).__name__}"}
    if not bool(getattr(notifier, "enabled", False)):
        return {"staged": staged, "sent": 0, "failed": 0, "status": "notifier_disabled"}
    sent = failed = 0
    for _ in range(max(1, int(limit))):
        with ls.connect(path) as conn:
            ls.ensure_tables(conn)
            item = ls.claim_next_notification(conn, now=delivery_now.isoformat())
        if item is None:
            break
        try:
            sender = getattr(notifier, "send_fast", None) or notifier.send
            sender(str(item["message_text"]), parse_mode="")
        except Exception as exc:
            with ls.connect(path) as conn:
                state = ls.defer_notification(
                    conn, notification_id=str(item["notification_id"]),
                    attempts=int(item.get("attempts") or 0), error=type(exc).__name__,
                )
                ls.event(conn, "LIVE_ENTRY_NOTIFICATION_FAILED", decision_id=str(item["decision_id"]),
                         severity="WARNING", payload={"state": state, "error": type(exc).__name__})
                conn.commit()
            failed += 1
            continue
        with ls.connect(path) as conn:
            ls.complete_notification(conn, notification_id=str(item["notification_id"]))
            ls.event(conn, "LIVE_ENTRY_NOTIFICATION_SENT", decision_id=str(item["decision_id"]),
                     payload={"notification_kind": item["notification_kind"]})
            conn.commit()
        sent += 1
    return {"staged": staged, "sent": sent, "failed": failed, "status": "OK"}


def _is_sqlite_locked(exc: BaseException) -> bool:
    return isinstance(exc, sqlite3.OperationalError) and "locked" in str(exc).lower()


def _reconcile_db_write(*, path: Path, cfg: LiveCanaryConfig, operation: Any) -> Any:
    """Retry a local, idempotent reconciliation write after a brief DB lock.

    This is intentionally unavailable to order submission. It is used only for
    local leases and persisted reconciliation telemetry after exchange actions,
    so retrying it cannot duplicate a live order.
    """
    attempts = max(1, int(cfg.get("position_reconcile_db_retry_attempts", 3)))
    timeout_ms = max(0, int(cfg.get("position_reconcile_db_busy_timeout_ms", 750)))
    backoff = max(0.0, float(cfg.get("position_reconcile_db_retry_backoff_seconds", 0.10)))
    for attempt in range(attempts):
        try:
            with ls.connect(
                path,
                timeout_seconds=timeout_ms / 1000.0,
                busy_timeout_ms=timeout_ms,
            ) as conn:
                return operation(conn)
        except Exception as exc:
            if not _is_sqlite_locked(exc) or attempt + 1 >= attempts:
                raise
            time.sleep(backoff * (attempt + 1))
    raise RuntimeError("reconciliation DB retry exhausted")


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


def _client(cfg: LiveCanaryConfig, *, private: bool = False) -> MexcFuturesClient:
    access, secret = cfg.credentials() if private else ("", "")
    return MexcFuturesClient(
        access_key=access,
        secret_key=secret,
        base_url=str(cfg.get("api_base_url", "https://api.mexc.com")),
        recv_window_seconds=int(cfg.get("recv_window_seconds", 10)),
        timeout_seconds=float(cfg.get("request_timeout_seconds", 8)),
        safe_read_retry_attempts=int(cfg.get("safe_read_retry_attempts", 1)),
        safe_read_retry_backoff_seconds=float(cfg.get("safe_read_retry_backoff_seconds", 0.25)),
    )


def _open_positions_for_symbol(client: MexcFuturesClient, symbol: str) -> list[dict[str, Any]]:
    """Read a symbol's positions from the fastest authoritative account snapshot.

    The MEXC symbol-filtered endpoint intermittently stalls while the global
    private snapshot is available. Reconciliation first reads that one
    snapshot and filters it exactly in-process. If the broader endpoint itself
    fails, fall back to the narrower call; a successful empty global snapshot
    is still only a *not currently open* result and the caller must confirm a
    close from history before releasing risk.
    """
    native_symbol = MexcFuturesClient.native_symbol(symbol)
    try:
        positions = client.open_positions()
    except MexcAPIError:
        return client.open_positions(symbol)
    return [
        position for position in positions
        if str(position.get("symbol") or "").upper() == native_symbol
    ]


def _f(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _exchange_symbol(cfg: LiveCanaryConfig, symbol: str) -> str:
    return cfg.exchange_symbol(symbol)


def _swing_live_reprice_enabled(cfg: LiveCanaryConfig) -> bool:
    raw = cfg.get("swing_live_reprice", {})
    if isinstance(raw, dict):
        return bool(raw.get("enabled", True))
    return True


def _allowed_entry_modes(cfg: LiveCanaryConfig, mode: str) -> set[str]:
    by_mode = cfg.get("allowed_entry_modes_by_mode", {}) or {}
    configured = by_mode.get(str(mode).lower())
    if not isinstance(configured, (list, tuple, set)):
        configured = cfg.get("allowed_entry_modes", []) or []
    return {str(value).strip().upper() for value in configured if str(value).strip()}


def _table_exists(conn: sqlite3.Connection, name: str) -> bool:
    return bool(conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone())


def _db_truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _decision_hash(value: dict[str, Any]) -> str:
    body = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def _paper_execution_revalidation_required(decision: dict[str, Any]) -> bool:
    context = str(decision.get("decision_context_type") or "").strip()
    # These contexts are produced by the normal production Paper alert path.
    # Custom live bridges (crypto invest, liquidity sweep, MEXC-stock paper
    # simulator) have their own point-in-time ledgers and remain validated by
    # their bridge plus venue preflight.
    return context in {"point_in_time", "point_in_time_stock_paper_entry"}


def _source_paper_execution_signal_id(decision: dict[str, Any]) -> str:
    signal_id = str(
        decision.get("source_signal_id")
        or decision.get("signal_id")
        or ""
    ).strip()
    if signal_id.startswith("stock_paper:"):
        signal_id = signal_id.split(":", 1)[1]
    return signal_id


def _frozen_paper_alert_revalidation(
    *,
    decision: dict[str, Any],
    diagnostic: dict[str, Any],
    mismatch_reason: str,
) -> dict[str, Any]:
    """Validate the immutable Paper alert snapshot when the outcome row is stale.

    ``paper_execution_outcomes`` is keyed by ``signal_id`` while one signal can
    legitimately be evaluated by several experimental paper profiles. A later
    profile update can therefore overwrite the row used by live revalidation.
    In that case the frozen decision captured from the original Telegram/Paper
    alert is safer than the mismatched outcome row, but only if it is still a
    complete point-in-time, current-price-revalidated live-grade snapshot.
    """
    context = str(decision.get("decision_context_type") or "").strip()
    if context not in {"point_in_time", "point_in_time_stock_paper_entry"}:
        return {"ok": False, "reason": "FROZEN_DECISION_CONTEXT_NOT_LIVE_GRADE", **diagnostic}

    if not str(
        decision.get("paper_alert_id")
        or decision.get("source_paper_alert_id")
        or ""
    ).strip():
        return {"ok": False, "reason": "FROZEN_DECISION_ALERT_ID_MISSING", **diagnostic}

    entry_basis = str(decision.get("entry_time_basis") or "").strip()
    if entry_basis != "point_in_time_current_bar":
        return {"ok": False, "reason": "FROZEN_DECISION_NOT_POINT_IN_TIME", **diagnostic}

    if decision.get("current_price_revalidated") is not True:
        return {"ok": False, "reason": "FROZEN_DECISION_PRICE_NOT_REVALIDATED", **diagnostic}

    age = _f(decision.get("entry_age_seconds"))
    max_age = _f(decision.get("max_entry_age_seconds"))
    if age is None or not math.isfinite(age) or age < 0:
        return {"ok": False, "reason": "FROZEN_DECISION_ENTRY_AGE_INVALID", **diagnostic}
    if max_age is not None and math.isfinite(max_age) and age > max_age:
        return {"ok": False, "reason": "FROZEN_DECISION_ENTRY_TOO_OLD", **diagnostic}

    entry = _f(decision.get("entry_price") or decision.get("entry_used"))
    stop = _f(decision.get("original_stop") or decision.get("stop"))
    tp1 = _f(decision.get("tp1"))
    tp2 = _f(decision.get("tp2"))
    tp3 = _f(decision.get("tp3"))
    prices = [entry, stop, tp1, tp2, tp3]
    if any(value is None or not math.isfinite(value) or value <= 0 for value in prices):
        return {"ok": False, "reason": "FROZEN_DECISION_GEOMETRY_INCOMPLETE", **diagnostic}

    direction = str(decision.get("direction") or "").lower()
    if direction == "short":
        geometry_ok = bool(tp3 < tp2 < tp1 < entry < stop)  # type: ignore[operator]
    else:
        geometry_ok = bool(stop < entry < tp1 < tp2 < tp3)  # type: ignore[operator]
    if not geometry_ok:
        return {"ok": False, "reason": "FROZEN_DECISION_GEOMETRY_INVALID", **diagnostic}

    return {
        "ok": True,
        **diagnostic,
        "authoritative_source": "frozen_live_decision_snapshot",
        "paper_row_mismatch_accepted_from_frozen_decision": True,
        "paper_row_mismatch_reason": mismatch_reason,
    }


def _authoritative_paper_execution_revalidation(
    *, db: str | Path, decision: dict[str, Any],
) -> dict[str, Any]:
    if not _paper_execution_revalidation_required(decision):
        return {"ok": True, "skipped": True, "reason": "NOT_PAPER_EXECUTION_CONTEXT"}
    signal_id = _source_paper_execution_signal_id(decision)
    if not signal_id:
        return {"ok": False, "reason": "PAPER_EXECUTION_SIGNAL_ID_MISSING"}
    with ls.connect(db, busy_timeout_ms=_LIVE_CAPTURE_DB_BUSY_TIMEOUT_MS) as conn:
        if not _table_exists(conn, "paper_execution_outcomes"):
            return {"ok": False, "reason": "PAPER_EXECUTION_TABLE_MISSING",
                    "source_signal_id": signal_id}
        row = conn.execute(
            "SELECT * FROM paper_execution_outcomes WHERE signal_id=? "
            "ORDER BY datetime(computed_at) DESC,rowid DESC LIMIT 1",
            (signal_id,),
        ).fetchone()
    if row is None:
        return {"ok": False, "reason": "PAPER_EXECUTION_OUTCOME_MISSING",
                "source_signal_id": signal_id}
    outcome = dict(row)
    lifecycle = str(outcome.get("lifecycle_state") or "")
    validity = str(outcome.get("execution_validity") or "")
    entry_basis = str(outcome.get("entry_time_basis") or "")
    expected_mode = str(decision.get("entry_mode") or "").upper()
    paper_mode = str(outcome.get("paper_execution_entry_mode") or "").upper()
    expected_profile = str(
        decision.get("source_paper_profile")
        or decision.get("paper_entry_profile")
        or decision.get("strategy_version")
        or ""
    ).strip()
    paper_profile = str(outcome.get("paper_entry_profile") or "").strip()
    diagnostic = {
        "source_signal_id": signal_id,
        "paper_lifecycle_state": lifecycle,
        "paper_execution_validity": validity,
        "paper_close_reason": outcome.get("close_reason"),
        "paper_entry_mode": paper_mode,
        "expected_entry_mode": expected_mode,
        "paper_entry_profile": paper_profile,
        "expected_paper_profile": expected_profile,
        "computed_at": outcome.get("computed_at"),
    }
    if expected_mode and paper_mode and expected_mode != paper_mode:
        return _frozen_paper_alert_revalidation(
            decision=decision,
            diagnostic=diagnostic,
            mismatch_reason="PAPER_EXECUTION_ENTRY_MODE_MISMATCH",
        )
    if expected_profile and paper_profile and expected_profile != paper_profile:
        return _frozen_paper_alert_revalidation(
            decision=decision,
            diagnostic=diagnostic,
            mismatch_reason="PAPER_EXECUTION_PROFILE_MISMATCH",
        )
    if lifecycle != "OPEN":
        return {"ok": False, "reason": "PAPER_EXECUTION_NOT_OPEN", **diagnostic}
    if validity != "valid":
        return {"ok": False, "reason": "PAPER_EXECUTION_NOT_VALID", **diagnostic}
    if entry_basis != "point_in_time_current_bar":
        return {"ok": False, "reason": "PAPER_EXECUTION_NOT_POINT_IN_TIME", **diagnostic}
    if not _db_truthy(outcome.get("current_price_revalidated")):
        return {"ok": False, "reason": "PAPER_EXECUTION_PRICE_NOT_REVALIDATED", **diagnostic}
    return {"ok": True, **diagnostic}


def _apply_capture_paper_contract_guard(
    rec: dict[str, Any],
    *,
    db: str | Path,
) -> tuple[dict[str, Any], list[str]]:
    """Reject a live capture before queuing when canonical Paper is not live-grade.

    The worker performs the same authoritative check right before preflight.
    Running it at capture time prevents stale/historical Telegram snapshots
    from being stored as apparently actionable live queue items.
    """
    reasons = list(json.loads(str(rec.get("rejection_reasons_json") or "[]")))
    if int(rec.get("eligible") or 0) != 1:
        return rec, reasons
    try:
        decision = json.loads(str(rec.get("decision_json") or "{}"))
    except json.JSONDecodeError:
        decision = {}
    validation = _authoritative_paper_execution_revalidation(db=db, decision=decision)
    if validation.get("ok") is True:
        return rec, reasons

    reason = str(validation.get("reason") or "PAPER_EXECUTION_REVALIDATION_FAILED")
    reasons = sorted({*reasons, "PAPER_EXECUTION_REVALIDATION_FAILED", reason})
    frozen = dict(decision)
    frozen["live_capture_contract_ok"] = False
    frozen["live_capture_contract_validation"] = validation
    frozen["rejection_reasons"] = reasons

    updated = dict(rec)
    updated["eligible"] = 0
    updated["state"] = "REJECTED"
    updated["rejection_reasons_json"] = json.dumps(reasons, sort_keys=True)
    updated["decision_json"] = json.dumps(frozen, sort_keys=True)
    updated["decision_hash"] = _decision_hash(frozen)
    return updated, reasons


def _hydrate_payload_from_paper_execution(*, store: Any, signal: dict[str, Any],
                                          payload: dict[str, Any]) -> dict[str, Any]:
    """Fill missing live provenance from the authoritative Paper execution row.

    Paper alerts can be rendered before every derived field is present on the
    message payload. The durable ``paper_execution_outcomes`` row is the safer
    source at the exchange boundary, so live capture uses it to repair missing
    profile/mode fields without changing the original Paper record.
    """
    out = dict(payload)
    signal_id = str(out.get("signal_id") or signal.get("signal_id") or "").strip()
    if not signal_id:
        return out
    has_profile = bool(str(out.get("paper_entry_profile") or signal.get("paper_entry_profile") or "").strip())
    has_mode = bool(str(
        out.get("paper_execution_entry_mode")
        or signal.get("paper_execution_entry_mode")
        or ""
    ).strip())
    if has_profile and has_mode:
        return out
    try:
        with store.connect() as conn:
            row = conn.execute(
                "SELECT paper_entry_profile,paper_execution_entry_mode,computed_at "
                "FROM paper_execution_outcomes WHERE signal_id=? "
                "ORDER BY datetime(computed_at) DESC LIMIT 1",
                (signal_id,),
            ).fetchone()
    except sqlite3.DatabaseError:
        return out
    if row is None:
        return out
    data = dict(row) if hasattr(row, "keys") else {
        "paper_entry_profile": row[0],
        "paper_execution_entry_mode": row[1],
        "computed_at": row[2],
    }
    hydrated = False
    profile = str(data.get("paper_entry_profile") or "").strip()
    mode = str(data.get("paper_execution_entry_mode") or "").strip().upper()
    if not has_profile and profile:
        out["paper_entry_profile"] = profile
        hydrated = True
    if not has_mode and mode:
        out["paper_execution_entry_mode"] = mode
        hydrated = True
    if hydrated:
        out["paper_execution_provenance_hydrated"] = True
        out["paper_execution_provenance_hydrated_from"] = "paper_execution_outcomes"
        if data.get("computed_at"):
            out["paper_execution_provenance_computed_at"] = data.get("computed_at")
    return out


def _maybe_reprice_late_crypto_swing(*, signal: dict[str, Any], payload: dict[str, Any],
                                     cfg: LiveCanaryConfig,
                                     now: datetime) -> dict[str, Any]:
    """Re-freeze a late crypto-swing alert at the current MEXC executable price.

    This is deliberately live-capture only. It does not rewrite Paper outcomes,
    proposed_signals or Telegram evidence. It only turns a stale-but-otherwise
    allowed swing setup into a new point-in-time live decision when the current
    MEXC book still preserves directional geometry and adverse drift is inside
    the configured swing limit.
    """
    if not _swing_live_reprice_enabled(cfg):
        return payload
    if str(signal.get("asset_class") or "crypto").lower() != "crypto":
        return payload
    if str(signal.get("mode") or "").lower() != "swing":
        return payload
    channel = str(payload.get("telegram_channel") or "")
    needs_reprice = (
        channel == "shadow_only_late"
        or str(payload.get("entry_time_basis") or "") != "point_in_time_current_bar"
        or payload.get("current_price_revalidated") is not True
    )
    if not needs_reprice:
        return payload

    action = str(payload.get("cqo_quality_action") or "").upper()
    if action not in {"FULL_SIZE", "HALF_SIZE"}:
        return payload

    direction = str(signal.get("direction") or "long").lower()
    entry_mode = str(
        payload.get("paper_execution_entry_mode")
        or signal.get("paper_execution_entry_mode")
        or payload.get("cqo_entry_mode")
        or ""
    ).upper()
    reference = _f(payload.get("entry_used"))
    stop = _f(payload.get("stop"))
    targets = [_f(payload.get("tp1")), _f(payload.get("tp2")), _f(payload.get("tp3"))]
    if direction not in {"long", "short"} or entry_mode not in _allowed_entry_modes(cfg, "swing"):
        return payload
    if any(v is None for v in [reference, stop, *targets]) or reference <= 0:
        return payload
    if not (stop < reference < targets[0] < targets[1] < targets[2]
            if direction == "long"
            else targets[2] < targets[1] < targets[0] < reference < stop):
        return payload

    public_client = _client(cfg, private=False)
    symbol = str(signal.get("symbol") or "")
    exchange_symbol = _exchange_symbol(cfg, symbol)
    contract = public_client.contract_info(exchange_symbol)
    depth = public_client.depth(exchange_symbol, limit=20)
    asks, bids = depth.get("asks") or [], depth.get("bids") or []
    if not asks or not bids:
        return payload
    ask, bid = _f(asks[0][0]), _f(bids[0][0])
    if ask is None or bid is None or ask <= 0 or bid <= 0 or ask < bid:
        return payload
    current = ask if direction == "long" else bid

    adverse_bps = (
        (current - reference) / reference * 10_000.0
        if direction == "long"
        else (reference - current) / reference * 10_000.0
    )
    max_adverse_bps = None
    for block_name in ("swing_live_reprice", "swing_live_recovery"):
        block = cfg.get(block_name, {}) or {}
        caps = block.get("max_adverse_drift_bps", {}) or {}
        if entry_mode in caps:
            try:
                max_adverse_bps = float(caps[entry_mode])
                break
            except (TypeError, ValueError):
                return payload
    if max_adverse_bps is None:
        max_adverse_bps = cfg.entry_limit(
            "max_reprice_adverse_drift_bps", entry_mode,
            cfg.entry_limit("max_entry_drift_bps", entry_mode, 75.0, mode="swing"),
            mode="swing",
        )
    if adverse_bps > max_adverse_bps:
        return payload

    tick = _f(contract.get("priceUnit")) or 0.0
    def _round_price(value: float, rounding) -> float:
        if tick <= 0:
            return round(value, 10)
        units = Decimal(str(value)) / Decimal(str(tick))
        rounded = units.to_integral_value(rounding=rounding)
        return float(rounded * Decimal(str(tick)))

    old_risk = abs(reference - stop)
    if old_risk <= 0:
        return payload
    risk_pct = old_risk / reference
    multipliers = [abs(tp - reference) / old_risk for tp in targets]
    entry_price = _round_price(
        current,
        ROUND_CEILING if direction == "long" else ROUND_FLOOR,
    )
    new_risk = entry_price * risk_pct
    if direction == "long":
        new_stop = _round_price(entry_price - new_risk, ROUND_FLOOR)
        new_targets = [_round_price(entry_price + new_risk * m, ROUND_FLOOR) for m in multipliers]
        valid = new_stop < entry_price < new_targets[0] < new_targets[1] < new_targets[2]
    else:
        new_stop = _round_price(entry_price + new_risk, ROUND_CEILING)
        new_targets = [_round_price(entry_price - new_risk * m, ROUND_CEILING) for m in multipliers]
        valid = new_targets[2] < new_targets[1] < new_targets[0] < entry_price < new_stop
    if not valid:
        return payload

    out = dict(payload)
    out.update({
        "entry_used": entry_price,
        "stop": new_stop,
        "tp1": new_targets[0],
        "tp2": new_targets[1],
        "tp3": new_targets[2],
        "entry_triggered_at": now.isoformat(),
        "entry_age_seconds": 0,
        "entry_time_basis": "point_in_time_current_bar",
        "current_price_revalidated": True,
        "entry_revalidation_reason": "mexc_live_crypto_swing_reprice",
        "entry_detected_at": now.isoformat(),
        "telegram_channel": "telegram",
        "size_weight": float(out.get("cqo_requested_size_weight") or (0.5 if action == "HALF_SIZE" else 1.0)),
        "mexc_live_repriced": True,
        "mexc_live_reprice_reference_entry": reference,
        "mexc_live_reprice_current_entry": current,
        "mexc_live_reprice_adverse_bps": round(adverse_bps, 6),
        "mexc_live_reprice_exchange_symbol": str(contract.get("symbol") or exchange_symbol),
    })
    if str(out.get("crypto_swing_main_paper_action") or "").upper() not in {"FULL_SIZE", "HALF_SIZE"}:
        out["crypto_swing_main_paper_action"] = action
    return out


def capture_paper_candidate(*, store: Any, signal: dict[str, Any], payload: dict[str, Any],
                            paper_alert_id: str | None = None,
                            cfg: LiveCanaryConfig | None = None,
                            now: datetime | None = None) -> dict[str, Any]:
    """Freeze a point-in-time Paper decision into the isolated MEXC outbox.

    Out-of-scope Paper alerts are ignored. In-scope rejected decisions are kept
    for audit, but only clean/eligible decisions get an outbox row.
    """
    cfg = cfg or load_live_canary_config()
    now = now or datetime.now(timezone.utc)
    if not cfg.capture_enabled:
        return {"status": "CAPTURE_DISABLED", "queued": False}
    original_payload = dict(payload)
    payload = _hydrate_payload_from_paper_execution(
        store=store, signal=signal, payload=dict(payload))
    try:
        payload = _maybe_reprice_late_crypto_swing(
            signal=signal, payload=dict(payload), cfg=cfg, now=now)
    except Exception:
        payload = dict(payload)
    rec = evaluate_paper_candidate(signal=signal, payload=payload, cfg=cfg, store=store,
                                   paper_alert_id=paper_alert_id, now=now)
    if not rec.pop("in_scope"):
        return {"status": "OUT_OF_SCOPE", "queued": False}
    reasons = list(rec.pop("reasons"))
    live_path = Path(getattr(store, "db_path", None) or load_config().db_path)
    rec, reasons = _apply_capture_paper_contract_guard(rec, db=live_path)
    # Use the live store's bounded five-second writer path.  The general
    # application store waits up to thirty seconds and runs WAL PRAGMAs on
    # every connection; either behaviour can turn a point-in-time handoff into
    # a stale live candidate while the scheduler holds SQLite's writer lock.
    connection = (
        ls.connect(
            live_path,
            timeout_seconds=_LIVE_CAPTURE_DB_TIMEOUT_SECONDS,
            busy_timeout_ms=_LIVE_CAPTURE_DB_BUSY_TIMEOUT_MS,
        )
        if live_path is not None else store.connect()
    )
    with connection as conn:
        result = ls.insert_decision(conn, rec, queue=bool(rec["eligible"]))
    frozen = json.loads(rec.get("decision_json") or "{}")
    _emit_live_latency(
        store,
        "mexc_decision_captured" if result["queued"] else "mexc_decision_rejected",
        frozen,
        note={"decision_id": result["decision_id"], "reasons": reasons,
              "inserted": result["inserted"], "queued": result["queued"]},
        event_at=now,
    )
    return {
        "status": "QUEUED" if result["queued"] else "REJECTED" if rec["eligible"] == 0 else "DUPLICATE",
        "queued": result["queued"],
        "inserted": result["inserted"],
        "decision_id": result["decision_id"],
        "reasons": reasons,
        "execution_mode": cfg.execution_mode,
        "payload_overrides": {
            key: value for key, value in payload.items()
            if original_payload.get(key) != value
        },
    }


def recapture_terminal_preflight_rejection(
    *,
    store: Any,
    signal: dict[str, Any],
    payload: dict[str, Any],
    expected_error: str,
    cfg: LiveCanaryConfig | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Re-freeze one never-submitted decision after a corrected preflight policy.

    This is deliberately an operator-only recovery path.  It is restricted to
    a terminal preflight rejection with no exchange-order row, captures a new
    current-price snapshot, and preserves the prior snapshot in the append-only
    event journal before returning the existing outbox item to ``QUEUED``.  It
    cannot retry an order which reached MEXC, nor bypass the normal risk,
    margin, spread, liquidation, or three-exit-leg preflight checks.
    """
    cfg = cfg or load_live_canary_config()
    now = now or datetime.now(timezone.utc)
    if not cfg.capture_enabled:
        return {"status": "CAPTURE_DISABLED", "queued": False}

    # Force the normal swing reprice helper to take a fresh executable quote.
    # The original Paper record remains untouched; this snapshot only powers a
    # new MEXC preflight after a terminal pre-submission policy correction.
    candidate_payload = _hydrate_payload_from_paper_execution(
        store=store, signal=signal, payload=dict(payload))
    candidate_payload.update({
        "entry_time_basis": "operator_recapture_requires_current_price",
        "current_price_revalidated": False,
        "entry_age_seconds": 0.0,
        "entry_triggered_at": now.isoformat(),
        "entry_detected_at": now.isoformat(),
    })
    try:
        candidate_payload = _maybe_reprice_late_crypto_swing(
            signal=signal, payload=candidate_payload, cfg=cfg, now=now)
    except Exception as exc:
        return {
            "status": "RECAPTURE_REPRICE_ERROR",
            "queued": False,
            "error_type": type(exc).__name__,
        }

    rec = evaluate_paper_candidate(
        signal=signal, payload=candidate_payload, cfg=cfg, store=store,
        paper_alert_id=None, now=now,
    )
    if not rec.pop("in_scope"):
        return {"status": "OUT_OF_SCOPE", "queued": False}
    reasons = list(rec.pop("reasons"))
    if not rec["eligible"]:
        return {"status": "RECAPTURE_REJECTED", "queued": False, "reasons": reasons}

    decision_id = str(rec["decision_id"])
    with store.connect() as conn:
        ls.ensure_tables(conn)
        prior = conn.execute(
            "SELECT * FROM mexc_canary_decisions WHERE decision_id=?", (decision_id,)
        ).fetchone()
        outbox = conn.execute(
            "SELECT * FROM mexc_canary_outbox WHERE decision_id=?", (decision_id,)
        ).fetchone()
        order = conn.execute(
            "SELECT 1 FROM mexc_canary_orders WHERE decision_id=?", (decision_id,)
        ).fetchone()
        if not prior or not outbox:
            return {"status": "RECAPTURE_SOURCE_MISSING", "queued": False}
        if order:
            return {"status": "RECAPTURE_ORDER_ALREADY_SUBMITTED", "queued": False}
        if (str(outbox["status"]) != "REJECTED_RISK_LIMIT"
                or str(outbox["last_error"] or "") != str(expected_error)):
            return {
                "status": "RECAPTURE_SOURCE_NOT_ELIGIBLE",
                "queued": False,
                "outbox_status": str(outbox["status"]),
                "last_error": outbox["last_error"],
            }

        prior_snapshot = {
            "captured_at": prior["captured_at"],
            "state": prior["state"],
            "config_hash": prior["config_hash"],
            "decision_hash": prior["decision_hash"],
            "decision_json": json.loads(prior["decision_json"]),
            "outbox_id": outbox["outbox_id"],
            "outbox_status": outbox["status"],
            "outbox_error": outbox["last_error"],
        }
        cols = (
            "captured_at", "paper_alert_id", "symbol", "mode", "entry_mode", "eligible",
            "state", "rejection_reasons_json", "decision_json", "decision_hash", "config_hash",
            "decision_context_type",
        )
        conn.execute(
            "UPDATE mexc_canary_decisions SET "
            + ",".join(f"{column}=?" for column in cols)
            + " WHERE decision_id=?",
            [rec[column] for column in cols] + [decision_id],
        )
        conn.execute(
            "UPDATE mexc_canary_outbox SET created_at=?,available_at=?,status='QUEUED',"
            "attempt_count=0,claimed_at=NULL,completed_at=NULL,last_error=NULL,result_json=NULL "
            "WHERE decision_id=?",
            (now.isoformat(), now.isoformat(), decision_id),
        )
        ls.event(
            conn,
            "OPERATOR_RECAPTURED_TERMINAL_PRE_SUBMISSION_REJECTION",
            decision_id=decision_id,
            severity="WARNING",
            payload={
                "expected_error": str(expected_error),
                "prior": prior_snapshot,
                "replacement": {
                    "captured_at": rec["captured_at"],
                    "config_hash": rec["config_hash"],
                    "decision_hash": rec["decision_hash"],
                    "decision_json": json.loads(rec["decision_json"]),
                },
            },
        )
        conn.commit()

    frozen = json.loads(rec["decision_json"])
    _emit_live_latency(
        store, "mexc_decision_recaptured", frozen,
        note={"decision_id": decision_id, "replaced_terminal_error": expected_error},
        event_at=now,
    )
    return {
        "status": "QUEUED",
        "queued": True,
        "decision_id": decision_id,
        "reasons": reasons,
        "payload_overrides": {
            key: value for key, value in candidate_payload.items()
            if payload.get(key) != value
        },
    }


def recover_closed_protection_failure(
    *,
    store: Any,
    signal: dict[str, Any],
    payload: dict[str, Any],
    cfg: LiveCanaryConfig | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Create one new current-price attempt after a safety-closed TP failure.

    This path is intentionally never part of the automatic scheduler.  It is
    for an explicit operator decision after MEXC filled an entry, protection
    installation failed, and the fail-safe close has been independently proven
    closed.  The prior execution remains immutable; the recovery uses a new
    database execution key and therefore cannot submit the old external order.
    """
    cfg = cfg or load_live_canary_config()
    now = now or datetime.now(timezone.utc)
    if not cfg.capture_enabled:
        return {"status": "CAPTURE_DISABLED", "queued": False}
    source_signal_id = str(signal.get("signal_id") or "")
    if not source_signal_id:
        return {"status": "RECOVERY_SOURCE_MISSING", "queued": False}

    with store.connect() as conn:
        source = conn.execute(
            "SELECT d.decision_id,o.status AS outbox_status,ord.status AS order_status,p.status AS position_status "
            "FROM mexc_canary_decisions d "
            "JOIN mexc_canary_outbox o ON o.decision_id=d.decision_id "
            "JOIN mexc_canary_orders ord ON ord.decision_id=d.decision_id "
            "JOIN mexc_canary_positions p ON p.decision_id=d.decision_id "
            "WHERE d.signal_id=? ORDER BY d.captured_at DESC LIMIT 1",
            (source_signal_id,),
        ).fetchone()
        protection_failure = conn.execute(
            "SELECT 1 FROM mexc_canary_events WHERE decision_id=? "
            "AND event_type='MEXC_THREE_TP_INSTALL_FAILED' LIMIT 1",
            (source["decision_id"],),
        ).fetchone() if source else None
        prior_recovery = conn.execute(
            "SELECT 1 FROM mexc_canary_decisions WHERE parent_decision_id=? LIMIT 1",
            (source["decision_id"],),
        ).fetchone() if source else None
    if not source or not protection_failure:
        return {"status": "RECOVERY_SOURCE_NOT_PROVEN", "queued": False}
    if str(source["order_status"]) != "FILLED" or str(source["position_status"]) != "CLOSED":
        return {"status": "RECOVERY_SOURCE_NOT_CLOSED", "queued": False}
    if prior_recovery:
        return {"status": "RECOVERY_LIMIT_REACHED", "queued": False}

    candidate_payload = _hydrate_payload_from_paper_execution(
        store=store, signal=signal, payload=dict(payload))
    candidate_payload.update({
        "entry_time_basis": "operator_recovery_requires_current_price",
        "current_price_revalidated": False,
        "entry_age_seconds": 0.0,
        "entry_triggered_at": now.isoformat(),
        "entry_detected_at": now.isoformat(),
    })
    try:
        candidate_payload = _maybe_reprice_late_crypto_swing(
            signal=signal, payload=candidate_payload, cfg=cfg, now=now)
    except Exception as exc:
        return {"status": "RECOVERY_REPRICE_ERROR", "queued": False,
                "error_type": type(exc).__name__}
    rec = evaluate_paper_candidate(
        signal=signal, payload=candidate_payload, cfg=cfg, store=store,
        paper_alert_id=None, now=now,
    )
    if not rec.pop("in_scope"):
        return {"status": "OUT_OF_SCOPE", "queued": False}
    reasons = list(rec.pop("reasons"))
    if not rec["eligible"]:
        return {"status": "RECOVERY_REJECTED", "queued": False, "reasons": reasons}

    execution_key = f"{source_signal_id}:mexc-recovery:{now.strftime('%Y%m%dT%H%M%S%f')}"
    rec["signal_id"] = execution_key
    rec["decision_id"] = str(uuid.uuid5(uuid.NAMESPACE_URL, f"mexc-canary:{execution_key}"))
    rec["parent_decision_id"] = str(source["decision_id"])
    rec["recovery_sequence"] = 1
    with store.connect() as conn:
        result = ls.insert_decision(conn, rec, queue=True)
        if result["queued"]:
            ls.event(
                conn, "OPERATOR_RECOVERY_AFTER_PROTECTION_FAILURE",
                decision_id=rec["decision_id"], severity="WARNING",
                payload={
                    "source_signal_id": source_signal_id,
                    "source_decision_id": str(source["decision_id"]),
                    "execution_key": execution_key,
                    "reason": "prior entry was safety-closed after incomplete three-TP installation",
                },
            )
            conn.commit()
    frozen = json.loads(rec["decision_json"])
    _emit_live_latency(
        store, "mexc_decision_recovery_captured", frozen,
        note={"decision_id": rec["decision_id"], "source_signal_id": source_signal_id},
        event_at=now,
    )
    return {
        "status": "QUEUED" if result["queued"] else "DUPLICATE",
        "queued": result["queued"],
        "decision_id": rec["decision_id"],
        "source_signal_id": source_signal_id,
        "reasons": reasons,
        "payload_overrides": {
            key: value for key, value in candidate_payload.items()
            if payload.get(key) != value
        },
    }


def _daily_realized_loss(conn: sqlite3.Connection) -> float:
    today = datetime.now(timezone.utc).date().isoformat()
    row = conn.execute(
        "SELECT COALESCE(SUM(CASE WHEN realized_pnl_usdt<0 THEN -realized_pnl_usdt ELSE 0 END),0) "
        "FROM mexc_canary_positions WHERE status='CLOSED' AND substr(closed_at,1,10)=?",
        (today,),
    ).fetchone()
    return float(row[0] or 0.0)


def _daily_loss_guard_applies(decision: dict[str, Any], cfg: LiveCanaryConfig) -> bool:
    exempt_buckets = {
        str(value).strip().lower()
        for value in (cfg.get("daily_loss_exempt_risk_buckets", []) or [])
    }
    risk_bucket = str(decision.get("risk_bucket") or "default").strip().lower()
    return risk_bucket not in exempt_buckets


def _is_transient_preflight_error(exc: Exception) -> bool:
    """Only retry pre-submission exchange reads that are provably temporary.

    ``select_candidate`` folds simultaneous venue failures into one
    ``NO_ELIGIBLE_EXECUTION_VENUE`` decision. The old single-MEXC predicate
    treated that wrapper as terminal, even when MEXC merely timed out and/or
    Bybit rejected an expired signed GET. A fresh retry is safe because no
    candidate has reached order submission at this point.
    """
    if isinstance(exc, PlanRejected) and str(exc) == "NO_ELIGIBLE_EXECUTION_VENUE":
        venues = getattr(exc, "details", {}).get("venues")
        if not isinstance(venues, dict):
            return False
        return any(
            _is_transient_venue_preflight_rejection(item, venue=str(venue))
            for venue, item in venues.items()
        )

    if not isinstance(exc, (MexcAPIError, BybitAPIError)):
        return False
    return _is_transient_exchange_preflight_error(
        message=str(exc),
        status_code=getattr(exc, "status_code", None),
        exchange_code=getattr(exc, "code", None),
        venue="bybit" if isinstance(exc, BybitAPIError) else "mexc",
    )


def _is_transient_exchange_preflight_error(*, message: str, status_code: Any = None,
                                            exchange_code: Any = None, venue: str = "") -> bool:
    """Classify only read/preflight failures; never submission outcomes."""
    text = str(message or "").lower()
    try:
        http_status = int(status_code) if status_code is not None else None
    except (TypeError, ValueError):
        http_status = None
    return bool(
        http_status in {408, 425, 429, 500, 502, 503, 504}
        or str(exchange_code or "") == "10002"
        or "requests are too frequent" in text
        or "rate limit" in text
        or "transport error" in text
        or "connectionerror" in text
        or "connecttimeout" in text
        or "readtimeout" in text
        or "venue_preflight_timeout" in text
        or "temporarily unavailable" in text
        or (
            str(venue).lower() == "bybit"
            and ("server timestamp" in text or "recv_window" in text)
        )
    )


def _is_transient_venue_preflight_rejection(value: Any, *, venue: str = "") -> bool:
    """Interpret structured diagnostics saved by the parallel venue router."""
    if not isinstance(value, dict):
        return False
    return _is_transient_exchange_preflight_error(
        message=str(value.get("reason") or ""),
        status_code=value.get("status_code"),
        exchange_code=value.get("exchange_code"),
        venue=str(value.get("venue") or value.get("exchange") or venue),
    )


def _transient_preflight_retry_delay(cfg: LiveCanaryConfig, item: dict[str, Any]) -> float:
    """Use bounded backoff while preserving the frozen entry freshness window."""
    base = max(0.0, float(cfg.get("transient_preflight_retry_interval_seconds", 1.0)))
    multiplier = max(1.0, float(cfg.get("transient_preflight_retry_backoff_multiplier", 1.0)))
    maximum = max(base, float(cfg.get("transient_preflight_retry_max_interval_seconds", 5.0)))
    prior_attempts = max(0, int(item.get("attempt_count") or 0))
    return min(maximum, base * (multiplier ** prior_attempts))


def _is_definitive_submission_rejection(exc: Exception) -> bool:
    """True only when MEXC explicitly rejected the POST before acceptance.

    A transport timeout, non-JSON response or malformed success payload remains
    unknown because the exchange may have accepted the order.  A parsed MEXC
    ``success=false`` business response is authoritative: no order was created.
    """
    return (
        isinstance(exc, MexcAPIError)
        and str(exc).lower().startswith("mexc request rejected:")
    )


def _transient_preflight_retry_limit(cfg: LiveCanaryConfig, decision: dict[str, Any]) -> int:
    """Use a small mode-specific retry budget without letting one route stall another."""
    by_mode = cfg.get("transient_preflight_retry_attempts_by_mode", {}) or {}
    mode = str(decision.get("mode") or "").lower()
    value = by_mode.get(mode, cfg.get("max_transient_preflight_retry_attempts", 1))
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 1


def _round_native_price(value: float, tick: float, rounding: str) -> float:
    if tick <= 0:
        return round(value, 10)
    units = Decimal(str(value)) / Decimal(str(tick))
    mode = ROUND_CEILING if rounding == "up" else ROUND_FLOOR
    return float(units.to_integral_value(rounding=mode) * Decimal(str(tick)))


def _maybe_reprice_swing_recovery(*, decision: dict[str, Any], contract: dict[str, Any],
                                  depth: dict[str, Any], cfg: LiveCanaryConfig) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """Recover a valid live geometry after an exchange tick-size rejection.

    Crypto swing retains its established adverse-drift policy.  Stock intraday
    applies the same deterministic rebasing only when the chosen stock-futures
    contract's coarse price tick collapses an otherwise valid Paper ladder.
    Paper evidence stays immutable in both cases.
    """
    asset_class = str(decision.get("asset_class") or "").lower()
    mode = str(decision.get("mode") or "").lower()
    crypto_swing = asset_class == "crypto" and mode == "swing"
    liquidity_sweep = asset_class == "crypto" and mode == "liquidity_sweep"
    stock_intraday = asset_class == "stock_futures" and mode == "stock_intraday"
    if crypto_swing:
        block = cfg.get("swing_live_recovery", {}) or {}
    elif liquidity_sweep:
        block = cfg.get("liquidity_sweep_live_recovery", {}) or {}
    elif stock_intraday:
        block = cfg.get("stock_intraday_live_recovery", {}) or {}
    else:
        return decision, None
    if not bool(block.get("enabled", True)):
        return decision, None
    entry_mode = str(decision.get("entry_mode") or "").upper()
    allowed = {str(value).upper() for value in (block.get("entry_modes") or [])}
    if entry_mode not in allowed:
        return decision, None
    direction = str(decision.get("direction") or "").lower()
    reference = _f(decision.get("entry_price"))
    stop = _f(decision.get("original_stop"))
    targets = [_f(decision.get("tp1")), _f(decision.get("tp2")), _f(decision.get("tp3"))]
    asks, bids = depth.get("asks") or [], depth.get("bids") or []
    if direction not in {"long", "short"} or any(value is None for value in [reference, stop, *targets]):
        return decision, None
    if not asks or not bids:
        return decision, None
    ask, bid = _f(asks[0][0]), _f(bids[0][0])
    if ask is None or bid is None or ask <= 0 or bid <= 0 or ask < bid:
        return decision, None
    current = ask if direction == "long" else bid
    adverse_bps = ((current - reference) / reference * 10_000.0 if direction == "long"
                   else (reference - current) / reference * 10_000.0)
    if crypto_swing and adverse_bps <= 0:
        return decision, None
    caps = block.get("max_adverse_drift_bps", {}) or {}
    try:
        cap = float(caps.get(entry_mode, cfg.entry_limit(
            "max_reprice_adverse_drift_bps", entry_mode, 50.0, mode="swing")))
    except (TypeError, ValueError):
        return decision, None
    observed_drift_bps = adverse_bps if crypto_swing else abs(adverse_bps)
    if observed_drift_bps > cap:
        return decision, None
    old_risk = abs(reference - stop)
    if old_risk <= 0:
        return decision, None
    if not (stop < reference < targets[0] < targets[1] < targets[2]
            if direction == "long" else targets[2] < targets[1] < targets[0] < reference < stop):
        return decision, None
    tick = _f(contract.get("priceUnit")) or 0.0
    entry = _round_native_price(current, tick, "up" if direction == "long" else "down")
    multipliers = [abs(target - reference) / old_risk for target in targets]
    stop_contract = decision.get("stop_contract") if isinstance(decision.get("stop_contract"), dict) else None
    preserve_structural_stop = is_structural_stop_contract(stop_contract)
    if preserve_structural_stop:
        new_stop = _round_native_price(stop, tick, "up" if direction == "long" else "down")
        new_risk = abs(entry - new_stop)
        if new_risk <= 0:
            return decision, None
    else:
        risk_pct = old_risk / reference
        new_risk = entry * risk_pct
    if direction == "long":
        if not preserve_structural_stop:
            new_stop = _round_native_price(entry - new_risk, tick, "down")
        target_rounding = "down" if (crypto_swing or liquidity_sweep) else "up"
        new_targets = [_round_native_price(entry + new_risk * multiple, tick, target_rounding) for multiple in multipliers]
        if stock_intraday and tick > 0:
            new_targets[0] = max(new_targets[0], entry + tick)
            new_targets[1] = max(new_targets[1], new_targets[0] + tick)
            new_targets[2] = max(new_targets[2], new_targets[1] + tick)
        valid = new_stop < entry < new_targets[0] < new_targets[1] < new_targets[2]
    else:
        if not preserve_structural_stop:
            new_stop = _round_native_price(entry + new_risk, tick, "up")
        target_rounding = "up" if (crypto_swing or liquidity_sweep) else "down"
        new_targets = [_round_native_price(entry - new_risk * multiple, tick, target_rounding) for multiple in multipliers]
        if stock_intraday and tick > 0:
            new_targets[0] = min(new_targets[0], entry - tick)
            new_targets[1] = min(new_targets[1], new_targets[0] - tick)
            new_targets[2] = min(new_targets[2], new_targets[1] - tick)
        valid = new_targets[2] < new_targets[1] < new_targets[0] < entry < new_stop
    if not valid:
        return decision, None
    updated = dict(decision)
    updated.update({
        "entry_price": entry,
        "original_stop": new_stop,
        "tp1": new_targets[0],
        "tp2": new_targets[1],
        "tp3": new_targets[2],
        "stop_contract": stop_contract,
        "stop_label": stop_contract_label(stop_contract),
        "structural_stop_preserved_on_reprice": preserve_structural_stop,
    })
    return updated, {
        "reason": (
            "mexc_live_swing_recovery_reprice"
            if crypto_swing else "liquidity_sweep_exchange_reprice"
            if liquidity_sweep else "stock_intraday_exchange_tick_reprice"
        ),
        "reference_entry": reference,
        "current_entry": entry,
        "adverse_drift_bps": round(adverse_bps, 6),
        "max_adverse_drift_bps": cap,
        "entry_mode": entry_mode,
    }


def _is_transient_mexc_visibility_error(exc: Exception) -> bool:
    """Read-after-write lag and rate limits while verifying already submitted exits."""
    if _is_transient_preflight_error(exc):
        return True
    message = str(exc).lower()
    return bool(
        "not visible yet" in message
        or "not found" in message
        or "external order missing" in message
        or "order not visible" in message
    )


def _insert_order(conn: sqlite3.Connection, *, decision_id: str, plan: dict[str, Any],
                  status: str, exchange: dict[str, Any] | None = None,
                  error: str | None = None) -> None:
    now = ls.utc_now()
    conn.execute(
        "INSERT INTO mexc_canary_orders(" 
        "order_row_id,decision_id,external_oid,exchange_order_id,symbol,status,submitted_at,updated_at,"
        "plan_json,exchange_json,last_error,venue) VALUES(?,?,?,?,?,?,?,?,?,?,?,?) "
        "ON CONFLICT(decision_id) DO UPDATE SET external_oid=excluded.external_oid,"
        "symbol=excluded.symbol,plan_json=excluded.plan_json,"
        "exchange_order_id=COALESCE(excluded.exchange_order_id,exchange_order_id),"
        "status=excluded.status,updated_at=excluded.updated_at,exchange_json=excluded.exchange_json,"
        "last_error=excluded.last_error,venue=excluded.venue",
        (str(uuid.uuid4()), decision_id, plan["external_oid"],
         str((exchange or {}).get("orderId") or "") or None, plan["symbol"], status,
         now if status in {"SUBMITTING", "SUBMITTED", "FILLED"} else None, now,
         json.dumps(plan, sort_keys=True), json.dumps(exchange or {}, sort_keys=True), error,
         str(plan.get("venue") or "mexc").lower()),
    )
    conn.commit()


def preflight(*, db: str | Path | None = None, symbol: str = "BTC/USDT",
              cfg: LiveCanaryConfig | None = None, private: bool = False) -> dict[str, Any]:
    cfg = cfg or load_live_canary_config()
    path = _db_path(db)
    checks: dict[str, Any] = {
        "capture_enabled": cfg.capture_enabled,
        "submission_enabled": cfg.submission_enabled,
        "execution_mode": cfg.execution_mode,
        "live_armed": cfg.live_armed(),
        "credentials_present": cfg.credentials_present(),
        "risk_per_trade_usdt": cfg.risk_per_trade_usdt,
        "max_concurrent_risk_usdt": cfg.max_concurrent_risk_usdt,
        "config_hash": cfg.config_hash,
        "venues": {
            "mexc": {"armed": cfg.mexc_live_armed(),
                     "credentials_present": cfg.credentials_present()},
            "bybit": {"armed": cfg.bybit_live_armed(),
                      "credentials_present": cfg.bybit_credentials_present(),
                      "enabled": bool(cfg.bybit_config().get("enabled", False))},
        },
    }
    with ls.connect(path) as conn:
        ls.ensure_tables(conn)
        checks["kill_switch"] = ls.kill_switch_state(conn)
    client = _client(cfg, private=private)
    try:
        exchange_symbol = _exchange_symbol(cfg, symbol)
        contract = client.contract_info(exchange_symbol)
        depth = client.depth(exchange_symbol, limit=5)
        checks.update({
            "public_api": "ok",
            "native_symbol": contract.get("symbol"),
            "api_allowed": contract.get("apiAllowed"),
            "contract_state": contract.get("state"),
            "best_ask": (depth.get("asks") or [[None]])[0][0],
            "best_bid": (depth.get("bids") or [[None]])[0][0],
        })
        checks["venues"]["mexc"].update({
            "public_api": "ok", "native_symbol": contract.get("symbol"),
            "best_ask": checks["best_ask"], "best_bid": checks["best_bid"],
        })
        ask = float(checks["best_ask"])
        bid = float(checks["best_bid"])
        if ask > 0 and bid > 0 and ask >= bid:
            checks["spread_bps"] = round((ask - bid) / ((ask + bid) / 2.0) * 10_000.0, 4)
            checks["spread_cap_bps"] = cfg.spread_limit_bps(symbol)
    except Exception as exc:
        checks["public_api"] = f"error:{type(exc).__name__}"
        checks["venues"]["mexc"]["public_api"] = checks["public_api"]
    if private:
        if not cfg.mexc_live_armed():
            checks["private_api"] = "blocked_not_armed"
            checks["venues"]["mexc"]["private_api"] = "blocked_not_armed"
        else:
            try:
                asset = client.account_asset("USDT")
                checks["private_api"] = "ok"
                checks["exchange_equity_usdt"] = float(asset.get("equity") or 0)
                checks["available_open_usdt"] = float(asset.get("availableOpen") or 0)
                checks["effective_risk_per_trade_usdt"] = cfg.risk_per_trade_usdt
                checks["effective_max_concurrent_risk_usdt"] = cfg.max_concurrent_risk_usdt
                checks["open_positions"] = len(client.open_positions())
                checks["venues"]["mexc"].update({
                    "private_api": "ok",
                    "exchange_equity_usdt": checks["exchange_equity_usdt"],
                    "available_open_usdt": checks["available_open_usdt"],
                    "open_positions": checks["open_positions"],
                })
            except Exception as exc:
                checks["private_api"] = f"error:{type(exc).__name__}"
                checks["venues"]["mexc"]["private_api"] = checks["private_api"]
    if bool(cfg.bybit_config().get("enabled", False)):
        try:
            bybit = make_bybit_client(cfg, private=private and cfg.bybit_live_armed())
            bybit_contract = bybit.contract_info(symbol)
            bybit_depth = bybit.depth(symbol, limit=5)
            bybit_check: dict[str, Any] = {
                "public_api": "ok", "native_symbol": bybit_contract.get("symbol"),
                "best_ask": (bybit_depth.get("asks") or [[None]])[0][0],
                "best_bid": (bybit_depth.get("bids") or [[None]])[0][0],
                "effective_risk_per_trade_usdt": float(
                    cfg.bybit_config().get("fixed_risk_per_trade_usdt", cfg.risk_per_trade_usdt)
                ),
            }
            if private:
                if cfg.bybit_live_armed():
                    try:
                        bybit_asset = bybit.account_asset("USDT")
                        fee_rate = bybit.fee_rate(symbol)
                        api_info = bybit.api_key_info()
                        permissions = api_info.get("permissions") or {}
                        contract_permissions = permissions.get("ContractTrade") or []
                        read_only = api_info.get("readOnly")
                        trade_permission_ok = (
                            str(read_only).lower() in {"0", "false", "none"}
                            and "Order" in {str(value) for value in contract_permissions}
                        )
                        bybit_check.update(
                            private_api="ok",
                            exchange_equity_usdt=float(bybit_asset.get("equity") or 0),
                            available_open_usdt=float(bybit_asset.get("availableOpen") or 0),
                            open_positions=len(bybit.open_positions()),
                            maker_fee_rate=fee_rate.get("makerFeeRate"),
                            taker_fee_rate=fee_rate.get("takerFeeRate"),
                            api_read_only=read_only,
                            contract_trade_permissions=contract_permissions,
                            trade_permission_ok=trade_permission_ok,
                        )
                    except BybitAPIError as exc:
                        bybit_check["private_api"] = f"error:{type(exc).__name__}"
                        bybit_check["private_error"] = str(exc)[:200]
                        bybit_check["private_error_code"] = exc.code
                        bybit_check["private_http_status"] = exc.status_code
                    except Exception as exc:
                        bybit_check["private_api"] = f"error:{type(exc).__name__}"
                else:
                    bybit_check["private_api"] = "blocked_not_armed"
            checks["venues"]["bybit"].update(bybit_check)
        except Exception as exc:
            checks["venues"]["bybit"]["public_api"] = f"error:{type(exc).__name__}"
    ready_venues = [
        venue for venue, detail in checks["venues"].items()
        if detail.get("armed") is True
        and detail.get("public_api") == "ok"
        and (not private or detail.get("private_api") == "ok")
        and (venue != "bybit" or not private or detail.get("trade_permission_ok") is True)
    ]
    checks["ready_venues"] = ready_venues
    checks["ready_for_real_orders"] = bool(
        ready_venues and checks.get("kill_switch") == "CLEAR"
    )
    return checks


def _floor_to_step(value: float, step: float) -> float:
    if step <= 0:
        return value
    units = (Decimal(str(value)) / Decimal(str(step))).to_integral_value(rounding=ROUND_FLOOR)
    return float(units * Decimal(str(step)))


def _round_to_step(value: float, step: float, rounding: str) -> float:
    if step <= 0:
        return value
    mode = ROUND_FLOOR if rounding == "down" else ROUND_CEILING
    units = (Decimal(str(value)) / Decimal(str(step))).to_integral_value(rounding=mode)
    return float(units * Decimal(str(step)))


def _partial_tp_weights(cfg: LiveCanaryConfig) -> tuple[float, float, float]:
    raw = tuple(float(value) for value in (
        (cfg.get("partial_take_profit", {}) or {}).get("weights") or (0.33, 0.33, 0.34)
    ))
    if len(raw) != 3 or min(raw) <= 0 or abs(sum(raw) - 1.0) > 1e-9:
        raise PlanRejected("PARTIAL_TP_WEIGHTS_INVALID")
    return raw


def _native_limit_tp_leg_count(cfg: LiveCanaryConfig) -> int:
    """Number of partial exits MEXC keeps as native limit orders.

    Some MEXC gateways accept only two simultaneous position-bound close
    limits. In that profile TP3 remains a monitored deterministic market close,
    while the native position stop continues to protect all remaining volume.
    """
    raw = (cfg.get("partial_take_profit", {}) or {}).get("native_limit_legs", 3)
    try:
        count = int(raw)
    except (TypeError, ValueError):
        count = 3
    return min(max(count, 2), 3)


def operator_order_probe(*, execute: bool = False, symbol: str = "BTC/USDT",
                         db: str | Path | None = None,
                         cfg: LiveCanaryConfig | None = None,
                         client: MexcFuturesClient | None = None) -> dict[str, Any]:
    """Validate MEXC create/query/cancel with a minimum, off-market order.

    This is an operator action, never a strategy entry. Any unexpected fill or
    unprovable cancellation trips the local kill switch. The probe only runs
    with an empty exchange position set so an emergency close cannot target an
    unrelated position.
    """
    cfg = cfg or load_live_canary_config()
    path = _db_path(db)
    with ls.connect(path) as conn:
        ls.ensure_tables(conn)
        if ls.kill_switch_state(conn) != "CLEAR":
            return {"status": "BLOCKED_KILL_SWITCH"}
    if not cfg.mexc_live_armed():
        return {"status": "BLOCKED_NOT_ARMED"}

    client = client or _client(cfg, private=True)
    asset = client.account_asset("USDT")
    positions_before = client.open_positions()
    if positions_before:
        return {"status": "BLOCKED_OPEN_POSITIONS", "open_positions": len(positions_before)}

    exchange_symbol = _exchange_symbol(cfg, symbol)
    contract = client.contract_info(exchange_symbol)
    depth = client.depth(exchange_symbol, limit=5)
    bids = depth.get("bids") or []
    if (int(contract.get("state", -1)) != 0 or contract.get("apiAllowed") is not True
            or not bids):
        return {"status": "BLOCKED_CONTRACT_OR_BOOK"}
    best_bid = float(bids[0][0])
    tick = float(contract.get("priceUnit") or 0)
    min_vol = float(contract.get("minVol") or 0)
    vol_step = float(contract.get("volUnit") or 0)
    contract_size = float(contract.get("contractSize") or 0)
    if min(best_bid, tick, min_vol, vol_step, contract_size) <= 0:
        return {"status": "BLOCKED_CONTRACT_METADATA"}

    offset_bps = float(cfg.get("operator_probe_offset_bps", 500.0))
    exchange_limit_bps = float(contract.get("bidLimitPriceRate") or 0.1) * 10_000.0
    offset_bps = min(max(offset_bps, 100.0), max(100.0, exchange_limit_bps * 0.8))
    price = _floor_to_step(best_bid * (1.0 - offset_bps / 10_000.0), tick)
    # Keep even an accidental probe fill inside the tiny account's risk budget.
    stop = _floor_to_step(price * 0.999, tick)
    take_profit = _floor_to_step(price * 1.001, tick)
    volume = max(min_vol, vol_step)
    probe_notional = volume * contract_size * price
    available_open = float(asset.get("availableOpen") or 0)
    maintenance = float(contract.get("maintenanceMarginRate") or 0)
    liquidation_fee = float(contract.get("liquidationFeeRate") or 0)
    max_safe_leverage = max(1, math.floor(1.0 / (0.01 + maintenance + liquidation_fee)))
    required_leverage = max(1, math.ceil(probe_notional / max(available_open * 0.8, 1e-12)))
    exchange_max = int(contract.get("maxLeverage") or 1)
    country_max = int(contract.get("countryConfigContractMaxLeverage") or 0)
    if country_max > 0:
        exchange_max = min(exchange_max, country_max)
    configured_ceiling = cfg.get("exchange_leverage_ceiling")
    leverage_caps = [max_safe_leverage, exchange_max]
    if configured_ceiling not in (None, "") and float(configured_ceiling) > 0:
        leverage_caps.append(int(float(configured_ceiling)))
    leverage = min(leverage_caps)
    if required_leverage > leverage:
        return {
            "status": "BLOCKED_INSUFFICIENT_PROBE_MARGIN",
            "required_margin_usdt": round(probe_notional / max(leverage, 1), 8),
            "available_open_usdt": available_open,
        }
    leverage = required_leverage
    external_oid = "probe_" + uuid.uuid4().hex[:25]
    order = {
        "symbol": str(contract.get("symbol") or MexcFuturesClient.native_symbol(symbol)),
        "price": price,
        "vol": volume,
        "leverage": leverage,
        "side": 1,
        "type": 2,
        "openType": 1,
        "externalOid": external_oid,
        "stopLossPrice": stop,
        "takeProfitPrice": take_profit,
        "lossTrend": 2,
        "profitTrend": 2,
        "positionMode": 1,
        "stpMode": 1,
    }
    result: dict[str, Any] = {
        "status": "PLANNED",
        "symbol": order["symbol"],
        "notional_usdt": round(probe_notional, 8),
        "price_offset_bps": round((best_bid - price) / best_bid * 10_000.0, 2),
        "leverage": leverage,
        "attached_stop": True,
        "attached_take_profit": True,
        "exchange_equity_usdt": float(asset.get("equity") or 0),
    }
    if not execute:
        return result

    try:
        created = client.create_order(order)
        result["order_accepted"] = True
        result["exchange_order_id"] = str(created.get("orderId") or "")
        try:
            cancel = client.cancel_external(order["symbol"], external_oid)
        except MexcAPIError:
            cancel = client.cancel_order_ids([created["orderId"]])
        cancel_row = cancel[0] if isinstance(cancel, list) and cancel else cancel
        result["cancel_response_ok"] = bool(
            isinstance(cancel_row, dict) and int(cancel_row.get("errorCode") or 0) == 0
        )

        deadline = time.monotonic() + float(cfg.get("operator_probe_timeout_seconds", 8.0))
        observed: dict[str, Any] | None = None
        while time.monotonic() < deadline:
            observed = client.order_by_external_id(order["symbol"], external_oid)
            state = int(observed.get("state") or 0)
            if state in {3, 4, 5}:
                break
            time.sleep(0.25)
        state = int((observed or {}).get("state") or 0)
        result["terminal_state"] = state
        result["deal_volume"] = float((observed or {}).get("dealVol") or 0)

        if state == 4 and result["deal_volume"] == 0 and result["cancel_response_ok"]:
            result["status"] = "PASSED_CANCELED_UNFILLED"
            with ls.connect(path) as conn:
                ls.event(conn, "OPERATOR_ORDER_PROBE_PASSED", payload={
                    "symbol": order["symbol"], "order_id": result["exchange_order_id"],
                    "notional_usdt": result["notional_usdt"], "terminal_state": state,
                })
                conn.commit()
            return result

        probe_position_id = str((observed or {}).get("positionId") or "")
        if probe_position_id:
            positions_after = client.open_positions(order["symbol"])
            for position in positions_after:
                if str(position.get("positionId") or "") != probe_position_id:
                    continue
                client.emergency_close_long(
                    symbol=order["symbol"], position_id=int(position["positionId"]),
                    volume=float(position.get("holdVol") or volume),
                    external_oid="probeclose_" + uuid.uuid4().hex[:20],
                )
                result["emergency_close_submitted"] = True
        with ls.connect(path) as conn:
            ls.set_kill_switch(conn, "TRIPPED", "operator order probe did not prove clean cancellation")
            ls.event(conn, "OPERATOR_ORDER_PROBE_FAILED", severity="CRITICAL", payload={
                "symbol": order["symbol"], "order_id": result.get("exchange_order_id"),
                "terminal_state": state, "deal_volume": result["deal_volume"],
            })
            conn.commit()
        result["status"] = "FAILED_KILL_TRIPPED"
        return result
    except Exception as exc:
        # Once create returned successfully, cancellation is best-effort retried
        # before tripping. Do not blind-retry create and do not close any position
        # unless the probe order itself can be tied to its positionId.
        if result.get("order_accepted"):
            try:
                client.cancel_external(order["symbol"], external_oid)
            except Exception:
                try:
                    client.cancel_order_ids([result["exchange_order_id"]])
                except Exception:
                    pass
            try:
                observed = client.order_by_external_id(order["symbol"], external_oid)
                position_id = str(observed.get("positionId") or "")
                if position_id:
                    for position in client.open_positions(order["symbol"]):
                        if str(position.get("positionId") or "") != position_id:
                            continue
                        client.emergency_close_long(
                            symbol=order["symbol"], position_id=int(position_id),
                            volume=float(position.get("holdVol") or volume),
                            external_oid="probeclose_" + uuid.uuid4().hex[:20],
                        )
                        result["emergency_close_submitted"] = True
            except Exception:
                pass
        with ls.connect(path) as conn:
            ls.set_kill_switch(conn, "TRIPPED", "operator order probe raised before clean cancellation")
            ls.event(conn, "OPERATOR_ORDER_PROBE_ERROR", severity="CRITICAL",
                     payload={"error_type": type(exc).__name__, "symbol": order["symbol"]})
            conn.commit()
        result.update({"status": "ERROR_KILL_TRIPPED", "error_type": type(exc).__name__})
        return result


def _is_definitive_bybit_submission_rejection(exc: Exception) -> bool:
    if not isinstance(exc, BybitAPIError):
        return False
    if "transport error" in str(exc).lower():
        return False
    if exc.status_code is not None and int(exc.status_code) >= 500:
        return False
    # Only an explicit Bybit business retCode proves that no order was
    # accepted. A malformed success response must be resolved by orderLinkId.
    return exc.code not in (None, 0, "0")


def _execute_bybit_candidate(*, path: Path, cfg: LiveCanaryConfig,
                             item: dict[str, Any], decision: dict[str, Any],
                             candidate: VenueCandidate,
                             route_diagnostic: dict[str, Any],
                             preserve_outbox_for_mexc_fallback: bool = False,
                             ) -> dict[str, Any]:
    """Submit one already-claimed immutable decision to Bybit exactly once."""
    outbox_id = str(item["outbox_id"])
    decision_id = str(item["decision_id"])
    plan = dict(candidate.plan)
    plan["venue"] = "bybit"
    plan["venue_route"] = route_diagnostic
    preflight_at = ls.utc_now()
    with ls.connect(path) as conn:
        ls.ensure_tables(conn)
        ls.upsert_parity_plan(
            conn, decision_id=decision_id, signal_id=str(decision["signal_id"]),
            symbol=str(plan["symbol"]), plan=plan, validation=candidate.parity,
            clean=True, evidence_class="forward_post_activation",
            source="bybit_preflight_v1", captured_at=preflight_at,
        )
        ls.event(conn, "LIVE_VENUE_SELECTED", decision_id=decision_id,
                 payload=route_diagnostic)
        conn.commit()
    _emit_live_latency(
        path, "bybit_preflight_passed", decision,
        note={"decision_id": decision_id, "symbol": plan.get("symbol")},
    )
    if cfg.execution_mode != "live":
        with ls.connect(path) as conn:
            _insert_order(conn, decision_id=decision_id, plan=plan, status="DRY_RUN_PLANNED")
            ls.complete_outbox(conn, outbox_id, "DRY_RUN_PLANNED", result=plan)
            conn.commit()
        return {"status": "DRY_RUN_PLANNED", "decision_id": decision_id,
                "venue": "bybit", "plan": plan}

    with ls.connect(path) as conn:
        if (_daily_loss_guard_applies(decision, cfg)
                and _daily_realized_loss(conn) >= cfg.daily_loss_limit_usdt):
            ls.complete_outbox(conn, outbox_id, "REJECTED_DAILY_LOSS", error="daily loss limit")
            return {"status": "REJECTED_DAILY_LOSS", "decision_id": decision_id,
                    "venue": "bybit"}
        reservation = ls.reserve_risk(
            conn, decision_id=decision_id,
            symbol=str(plan.get("canonical_symbol") or decision["symbol"]).upper(),
            risk_usdt=float(plan["actual_risk_usdt"]),
            margin_usdt=float(plan["estimated_margin_usdt"]),
            notional_usdt=float(plan["notional_usdt"]),
            max_risk_usdt=cfg.max_concurrent_risk_usdt,
            max_margin_usdt=cfg.execution_limit(
                "max_total_margin_usdt", decision, 50.0, allow_unlimited=True),
            max_notional_usdt=cfg.execution_limit(
                "max_gross_notional_usdt", decision, 500.0, allow_unlimited=True),
            max_open_same_symbol=int(cfg.get("max_open_same_symbol", 1)),
            venue="bybit",
            allow_rebind_released=(
                str(route_diagnostic.get("selection_reason") or "")
                == "mexc_definitive_rejection_fallback"
            ),
        )
        if not reservation.get("ok"):
            ls.complete_outbox(
                conn, outbox_id, "REJECTED_RISK_LIMIT", error=reservation.get("reason")
            )
            return {"status": "REJECTED_RISK_LIMIT", "decision_id": decision_id,
                    "venue": "bybit", "reason": reservation.get("reason")}
        _insert_order(conn, decision_id=decision_id, plan=plan, status="SUBMITTING")

    client = candidate.client
    with ls.connect(path) as conn:
        ls.record_venue_attempt(
            conn, decision_id=decision_id, venue="bybit", stage="SUBMISSION",
            status="SUBMITTING", diagnostic={"symbol": plan.get("symbol")},
        )
        conn.commit()
    try:
        exchange_result = submit_bybit_entry(client=client, plan=plan)
    except BybitAPIError as exc:
        if _is_definitive_bybit_submission_rejection(exc):
            diagnostic = {"reason": str(exc), "code": exc.code,
                          "status_code": exc.status_code, "order_accepted": False}
            with ls.connect(path) as conn:
                ls.record_venue_attempt(
                    conn, decision_id=decision_id, venue="bybit", stage="SUBMISSION",
                    status="REJECTED", reason=str(exc), diagnostic=diagnostic,
                )
                _insert_order(conn, decision_id=decision_id, plan=plan,
                              status="REJECTED_SUBMISSION", error=str(exc))
                ls.release_risk(conn, decision_id, "Bybit definitively rejected entry")
                if not preserve_outbox_for_mexc_fallback:
                    ls.complete_outbox(conn, outbox_id, "REJECTED_SUBMISSION",
                                       result=diagnostic, error=str(exc))
                ls.event(conn, "BYBIT_ORDER_SUBMISSION_REJECTED", decision_id=decision_id,
                         severity="WARNING", payload=diagnostic)
                conn.commit()
            return {"status": "REJECTED_SUBMISSION", "decision_id": decision_id,
                    "venue": "bybit", "definitive_rejection": True, **diagnostic}
        try:
            exchange_result = client.order_by_external_id(
                str(plan["symbol"]), str(plan["external_oid"])
            )
        except BybitAPIError:
            with ls.connect(path) as conn:
                ls.record_venue_attempt(
                    conn, decision_id=decision_id, venue="bybit", stage="SUBMISSION",
                    status="UNKNOWN", reason=str(exc), diagnostic={"reason": str(exc)},
                )
                _insert_order(conn, decision_id=decision_id, plan=plan,
                              status="SUBMISSION_UNKNOWN", error=str(exc))
                ls.set_kill_switch(conn, "TRIPPED", "Bybit order submission state unknown")
                ls.complete_outbox(conn, outbox_id, "SUBMISSION_UNKNOWN", error=str(exc))
                conn.commit()
            return {"status": "SUBMISSION_UNKNOWN", "decision_id": decision_id,
                    "venue": "bybit"}

    with ls.connect(path) as conn:
        ls.record_venue_attempt(
            conn, decision_id=decision_id, venue="bybit", stage="SUBMISSION",
            status="SUBMITTED", diagnostic={"order_id": exchange_result.get("orderId")},
        )
        _insert_order(conn, decision_id=decision_id, plan=plan, status="SUBMITTED",
                      exchange=exchange_result)
        ls.complete_outbox(conn, outbox_id, "SUBMITTED",
                           result={"orderId": exchange_result.get("orderId"), "venue": "bybit"})
        ls.event(conn, "ORDER_SUBMITTED", decision_id=decision_id,
                 payload={"venue": "bybit", "orderId": exchange_result.get("orderId"),
                          "externalOid": plan["external_oid"]})
        conn.commit()
    _emit_live_latency(path, "bybit_order_submitted", decision,
                       note={"decision_id": decision_id, "symbol": plan.get("symbol")})
    protection = reconcile_bybit_once(db=path, cfg=cfg, client=client)
    return {"status": "SUBMITTED", "decision_id": decision_id, "venue": "bybit",
            "order_id": exchange_result.get("orderId"), "protection": protection}


def _stale_open_position_reconciliation(
    conn: sqlite3.Connection,
    cfg: LiveCanaryConfig,
    *,
    now: datetime | None = None,
) -> dict[str, Any] | None:
    """Return the oldest stale open position that must gate new live risk."""
    if not bool(cfg.get("block_new_entries_when_open_position_reconciliation_stale", True)):
        return None
    limit = max(
        1.0,
        float(cfg.get("open_position_reconciliation_entry_block_seconds", 60.0)),
    )
    moment = now or datetime.now(timezone.utc)
    rows = conn.execute(
        "SELECT decision_id,symbol,venue,opened_at,last_reconciled_at "
        "FROM mexc_canary_positions WHERE status='OPEN'"
    ).fetchall()
    stale: list[dict[str, Any]] = []
    for row in rows:
        reconciled_at = _parse_utc(row["last_reconciled_at"])
        age_basis = reconciled_at or _parse_utc(row["opened_at"])
        age = float("inf") if age_basis is None else max(
            0.0, (moment - age_basis).total_seconds()
        )
        if age > limit:
            stale.append({
                "decision_id": str(row["decision_id"]),
                "symbol": str(row["symbol"]),
                "venue": str(row["venue"] or "mexc"),
                "last_reconciled_at": (
                    reconciled_at.isoformat() if reconciled_at is not None else None
                ),
                "reconciliation_age_seconds": (
                    None if not math.isfinite(age) else round(age, 3)
                ),
            })
    if not stale:
        return None
    stale.sort(
        key=lambda item: (
            float("-inf")
            if item["reconciliation_age_seconds"] is None
            else -float(item["reconciliation_age_seconds"])
        )
    )
    return {
        "reason": "OPEN_POSITION_RECONCILIATION_STALE",
        "limit_seconds": limit,
        "stale_position_count": len(stale),
        "oldest_position": stale[0],
    }


def worker_once(*, db: str | Path | None = None, cfg: LiveCanaryConfig | None = None,
                client: MexcFuturesClient | None = None,
                bybit_execution_client: BybitFuturesClient | None = None,
                reconcile_after_submission: bool = True) -> dict[str, Any]:
    cfg = cfg or load_live_canary_config()
    path = _db_path(db)
    try:
        with ls.connect(path) as conn:
            ls.ensure_tables(conn)
            if ls.kill_switch_state(conn) != "CLEAR":
                return {"status": "KILL_SWITCH_TRIPPED"}
            due = conn.execute(
                "SELECT 1 FROM mexc_canary_outbox "
                "WHERE status='QUEUED' AND available_at<=? LIMIT 1",
                (ls.utc_now(),),
            ).fetchone()
            stale_reconciliation = (
                _stale_open_position_reconciliation(conn, cfg) if due else None
            )
            if stale_reconciliation is not None:
                # Keep the decision queued. Reconciliation still runs later in
                # the same monitor tick, so a recovered venue releases this
                # gate immediately without spending a preflight retry.
                return {
                    "status": "BLOCKED_STALE_OPEN_POSITION_RECONCILIATION",
                    **stale_reconciliation,
                }
            item = ls.claim_next(conn)
    except sqlite3.OperationalError as exc:
        if ls.is_database_busy(exc):
            return {"status": "RETRY_DB_BUSY", "stage": "claim"}
        raise
    if not item:
        return {"status": "IDLE"}

    outbox_id = str(item["outbox_id"])
    decision_id = str(item["decision_id"])
    decision = json.loads(item["decision_json"])
    decision["decision_id"] = decision_id
    route = registered_route(
        mode=str(decision.get("mode") or ""),
        entry_mode=str(decision.get("entry_mode") or ""),
        asset_class=str(decision.get("asset_class") or "crypto"),
        path=cfg.get("live_route_registry_path") or None,
    )
    if route is None or route.get("enabled") is not True:
        diagnostic = {
            "reason": "LIVE_ROUTE_DISABLED_AT_DEQUEUE",
            "route_key": (route or {}).get("route_key"),
            "mode": decision.get("mode"),
            "entry_mode": decision.get("entry_mode"),
        }
        with ls.connect(path) as conn:
            ls.complete_outbox(
                conn, outbox_id, "REJECTED_LIVE_ROUTE_DISABLED",
                result=diagnostic, error="authoritative live route is disabled",
            )
            ls.event(
                conn, "LIVE_ROUTE_DISABLED_AT_DEQUEUE", decision_id=decision_id,
                severity="WARNING", payload=diagnostic,
            )
            conn.commit()
        return {"status": "REJECTED_LIVE_ROUTE_DISABLED", "decision_id": decision_id, **diagnostic}
    # The immutable policy decision already validated the point-in-time entry
    # age. Add only the time spent waiting in the outbox. This avoids trusting
    # provider timestamps while still preventing a delayed queue from trading.
    age_basis = (
        _parse_utc(item.get("decision_captured_at"))
        or _parse_utc(item.get("created_at"))
    )
    entry_mode = str(decision.get("entry_mode") or "").upper()
    max_queue_age = cfg.entry_limit(
        "max_entry_age_seconds", entry_mode, 45.0,
        mode=str(decision.get("mode") or "").lower(),
    )
    wait_age = (
        (datetime.now(timezone.utc) - age_basis).total_seconds()
        if age_basis is not None else float("inf")
    )
    frozen_entry_age = float(decision.get("entry_age_seconds") or 0.0)
    total_entry_age = wait_age + max(0.0, frozen_entry_age)
    if wait_age < 0 or total_entry_age > max_queue_age:
        diagnostic = {
            "reason": "STALE_QUEUE_AT_DEQUEUE",
            "queue_wait_seconds": None if not math.isfinite(wait_age) else round(wait_age, 3),
            "total_entry_age_seconds": (
                None if not math.isfinite(total_entry_age) else round(total_entry_age, 3)
            ),
            "max_entry_age_seconds": max_queue_age,
            "entry_mode": entry_mode,
            "age_basis": age_basis.isoformat() if age_basis else None,
        }
        with ls.connect(path) as conn:
            ls.complete_outbox(
                conn, outbox_id, "REJECTED_STALE_QUEUE",
                result=diagnostic, error="stale queue invalidated before exchange preflight",
            )
            ls.event(
                conn, "STALE_QUEUE_INVALIDATED", decision_id=decision_id,
                severity="WARNING", payload=diagnostic,
            )
            conn.commit()
        _emit_live_latency(path, "mexc_preflight_rejected", decision, note=diagnostic)
        return {"status": "REJECTED_STALE_QUEUE", "decision_id": decision_id, **diagnostic}
    if (str(decision.get("entry_time_basis") or "") != "point_in_time_current_bar"
            or decision.get("current_price_revalidated") is not True):
        with ls.connect(path) as conn:
            ls.complete_outbox(conn, outbox_id, "REJECTED_ENTRY_PROVENANCE",
                               error="queued decision lacks point-in-time revalidated entry")
            ls.event(conn, "ORDER_PLAN_REJECTED", decision_id=decision_id, severity="WARNING",
                     payload={"reason": "ENTRY_PROVENANCE_NOT_LIVE_GRADE"})
            conn.commit()
        return {"status": "REJECTED_ENTRY_PROVENANCE", "decision_id": decision_id}
    if str(item["config_hash"]) != cfg.config_hash:
        with ls.connect(path) as conn:
            ls.complete_outbox(conn, outbox_id, "REJECTED_CONFIG_CHANGED",
                               error="config changed after immutable decision")
        return {"status": "REJECTED_CONFIG_CHANGED", "decision_id": decision_id}

    paper_revalidation = _authoritative_paper_execution_revalidation(
        db=path, decision=decision,
    )
    if paper_revalidation.get("ok") is not True:
        diagnostic = {"reason": "PAPER_EXECUTION_REVALIDATION_FAILED",
                      **paper_revalidation}
        with ls.connect(path) as conn:
            ls.complete_outbox(
                conn, outbox_id, "REJECTED_PAPER_EXECUTION_REVALIDATION",
                result=diagnostic, error=str(paper_revalidation.get("reason") or ""),
            )
            ls.event(
                conn, "ORDER_PLAN_REJECTED", decision_id=decision_id,
                severity="WARNING", payload=diagnostic,
            )
            conn.commit()
        _emit_live_latency(path, "mexc_preflight_rejected", decision, note=diagnostic)
        return {"status": "REJECTED_PAPER_EXECUTION_REVALIDATION",
                "decision_id": decision_id, **diagnostic}

    route_diagnostic: dict[str, Any] | None = None
    selected_mexc: VenueCandidate | None = None
    bybit_definitively_rejected = False
    if cfg.execution_mode == "live" and cfg.bybit_live_armed():
        try:
            selected, route_diagnostic = select_candidate(
                decision=decision, cfg=cfg, captured_at=ls.utc_now(),
                mexc_override=client,
                bybit_override=bybit_execution_client,
                reprice_callback=_maybe_reprice_swing_recovery,
            )
        except (PlanRejected, MexcAPIError, BybitAPIError, ValueError) as exc:
            diagnostic = {"reason": str(exc), **dict(getattr(exc, "details", {}) or {})}
            transient_retry = (
                _is_transient_preflight_error(exc)
                and total_entry_age < max_queue_age
                and int(item.get("attempt_count") or 0) < _transient_preflight_retry_limit(cfg, decision)
            )
            with ls.connect(path) as conn:
                _record_venue_route_attempts(
                    conn, decision_id=decision_id, diagnostic=diagnostic,
                )
                if transient_retry:
                    delay = _transient_preflight_retry_delay(cfg, item)
                    diagnostic.update(
                        retry_in_seconds=delay,
                        total_entry_age_seconds=round(total_entry_age, 3),
                        max_entry_age_seconds=max_queue_age,
                        retry_scope="multi_venue_preflight",
                    )
                    ls.defer_outbox(conn, outbox_id, delay_seconds=delay,
                                    result=diagnostic, error=str(exc))
                    ls.event(conn, "ORDER_PREFLIGHT_TRANSIENT_RETRY",
                             decision_id=decision_id, severity="INFO", payload=diagnostic)
                    conn.commit()
                    return {
                        "status": "RETRY_TRANSIENT_PREFLIGHT",
                        "decision_id": decision_id,
                        **diagnostic,
                    }
                ls.complete_outbox(conn, outbox_id, "REJECTED_PREFLIGHT",
                                   result=diagnostic, error=str(exc))
                ls.event(conn, "LIVE_VENUE_SELECTION_REJECTED", decision_id=decision_id,
                         severity="WARNING", payload=diagnostic)
                conn.commit()
            _stage_live_preflight_rejection_notification(
                path, decision_id=decision_id, decision=decision, reason=str(exc),
            )
            return {"status": "REJECTED_PREFLIGHT", "decision_id": decision_id,
                    **diagnostic}
        with ls.connect(path) as conn:
            ls.ensure_tables(conn)
            _record_venue_route_attempts(
                conn, decision_id=decision_id, diagnostic=route_diagnostic,
            )
            conn.commit()
        if selected.venue == "bybit":
            bybit_result = _execute_bybit_candidate(
                path=path, cfg=cfg, item=item, decision=decision,
                candidate=selected, route_diagnostic=route_diagnostic,
                preserve_outbox_for_mexc_fallback=True,
            )
            if not bybit_result.get("definitive_rejection"):
                return bybit_result

            # A definitive Bybit business error proves that no order exists.
            # Re-preflight the same immutable, still-fresh decision once on MEXC.
            # Unknown/transport outcomes never enter this branch: duplicating an
            # order is worse than missing an entry.
            fallback_age = (
                (datetime.now(timezone.utc) - age_basis).total_seconds()
                + max(0.0, frozen_entry_age)
                if age_basis is not None else float("inf")
            )
            try:
                if not cfg.mexc_live_armed():
                    raise PlanRejected("MEXC_LIVE_NOT_ARMED")
                if fallback_age > max_queue_age:
                    raise PlanRejected("MEXC_FALLBACK_ENTRY_STALE")
                mexc_fallback_client = (
                    client if getattr(client, "_access_key", "") else _client(cfg, private=True)
                )
                selected_mexc = prepare_candidate(
                    venue="mexc", decision=decision, cfg=cfg,
                    captured_at=ls.utc_now(), client=mexc_fallback_client,
                    reprice_callback=_maybe_reprice_swing_recovery,
                )
            except (PlanRejected, MexcAPIError, ValueError) as fallback_exc:
                fallback_diagnostic = {
                    **bybit_result,
                    "fallback_venue": "mexc",
                    "fallback_reason": str(fallback_exc),
                }
                with ls.connect(path) as conn:
                    ls.complete_outbox(
                        conn, outbox_id, "REJECTED_SUBMISSION",
                        result=fallback_diagnostic, error=str(bybit_result.get("reason") or fallback_exc),
                    )
                    ls.event(
                        conn, "MEXC_FALLBACK_PREFLIGHT_REJECTED",
                        decision_id=decision_id, severity="WARNING",
                        payload=fallback_diagnostic,
                    )
                    conn.commit()
                _stage_live_preflight_rejection_notification(
                    path, decision_id=decision_id, decision=decision,
                    reason="BYBIT_REJECTED_MEXC_FALLBACK_UNAVAILABLE",
                )
                return {
                    "status": "REJECTED_SUBMISSION", "decision_id": decision_id,
                    **fallback_diagnostic,
                }
            route_diagnostic = {
                "selected": "mexc",
                "selection_reason": "bybit_definitive_rejection_fallback",
                "candidates": {
                    "mexc": {
                        "all_in_cost_bps": selected_mexc.all_in_cost_bps,
                        "spread_bps": selected_mexc.plan_obj.spread_bps,
                        "preflight_latency_ms": selected_mexc.preflight_latency_ms,
                        "symbol": selected_mexc.plan_obj.symbol,
                    },
                },
                "rejected": {"bybit": bybit_result},
            }
            bybit_definitively_rejected = True
            client = selected_mexc.client
            with ls.connect(path) as conn:
                _record_venue_route_attempts(
                    conn, decision_id=decision_id, diagnostic=route_diagnostic,
                )
                ls.event(
                    conn, "BYBIT_REJECTION_FALLBACK_TO_MEXC",
                    decision_id=decision_id, severity="WARNING", payload=route_diagnostic,
                )
                conn.commit()
        else:
            selected_mexc = selected
            client = selected.client

    client = client or _client(cfg, private=False)
    _emit_live_latency(path, "mexc_preflight_started", decision,
                       note={"decision_id": decision_id, "queue_wait_seconds": round(wait_age, 3)})
    try:
        if selected_mexc is not None:
            contract = selected_mexc.contract
            depth = selected_mexc.depth
            equity = selected_mexc.equity_usdt
            available_open = selected_mexc.available_open_usdt
            plan_obj = selected_mexc.plan_obj
            plan = dict(selected_mexc.plan)
            parity = selected_mexc.parity
            recovery = plan.get("live_recovery_reprice")
            private_client = selected_mexc.client
        else:
            exchange_symbol = _exchange_symbol(cfg, decision["symbol"])
            contract = client.contract_info(exchange_symbol)
            depth = client.depth(exchange_symbol, limit=20)
            equity = None
            available_open = None
            private_client = client
        if cfg.execution_mode == "live":
            if not cfg.mexc_live_armed():
                raise PlanRejected("MEXC_LIVE_NOT_ARMED")
            if selected_mexc is None:
                private_client = client if getattr(client, "_access_key", "") else _client(cfg, private=True)
                asset = private_client.account_asset("USDT")
                equity = float(asset.get("equity") or 0.0)
                available_open = float(asset.get("availableOpen") or 0.0)
                if equity <= 0:
                    raise PlanRejected("NO_EXCHANGE_EQUITY")
            exchange_positions = private_client.open_positions()
            with ls.connect(path) as _local_conn:
                local_ids = {str(r[0]) for r in _local_conn.execute(
                    "SELECT exchange_position_id FROM mexc_canary_positions "
                    "WHERE status='OPEN' AND venue='mexc'"
                ).fetchall() if r[0] not in (None, "")}
                orphan = _local_conn.execute(
                    "SELECT 1 FROM mexc_canary_positions p LEFT JOIN mexc_canary_risk_reservations r "
                    "ON r.decision_id=p.decision_id AND r.status='OPEN' "
                    "WHERE p.status='OPEN' AND r.decision_id IS NULL LIMIT 1"
                ).fetchone()
            if orphan:
                raise PlanRejected("RISK_LEDGER_INCONSISTENT")
            untracked = [p for p in exchange_positions
                         if str(p.get("positionId") or "") not in local_ids]
            if untracked and not bool(cfg.get("allow_manual_exchange_positions", False)):
                raise PlanRejected("UNTRACKED_EXCHANGE_POSITION")
            client = private_client
        if selected_mexc is None:
            recovery = None
            try:
                plan_obj = build_order_plan(decision=decision, contract=contract, depth=depth,
                                            cfg=cfg, exchange_equity_usdt=equity)
            except PlanRejected as initial_error:
                recovered_decision, recovery = _maybe_reprice_swing_recovery(
                    decision=decision, contract=contract, depth=depth, cfg=cfg)
                if recovery is None:
                    raise initial_error
                decision = recovered_decision
                plan_obj = build_order_plan(decision=decision, contract=contract, depth=depth,
                                            cfg=cfg, exchange_equity_usdt=equity)
            plan = plan_obj.to_dict()
            plan["venue"] = "mexc"
            plan["canonical_symbol"] = str(decision["symbol"]).upper()
            if recovery is not None:
                plan["live_recovery_reprice"] = recovery
            parity = build_mexc_pretrade_parity(
                plan=plan_obj,
                contract=contract,
                depth=depth,
                captured_at=ls.utc_now(),
                weights=_partial_tp_weights(cfg),
            )
        if route_diagnostic is not None:
            plan["venue_route"] = route_diagnostic
        preflight_at = ls.utc_now()
        if (cfg.get("mexc_native_parity", {}) or {}).get("required_before_submit", True):
            if parity.get("clean") is not True:
                raise PlanRejected("MEXC_PARITY_REQUIRED")
        plan["mexc_pretrade_parity"] = parity
        plan["partial_tp_legs"] = parity["legs"]
        if available_open is not None and float(plan["estimated_margin_usdt"]) > available_open:
            raise PlanRejected("INSUFFICIENT_AVAILABLE_MARGIN")
        with ls.connect(path) as conn:
            ls.ensure_tables(conn)
            ls.upsert_parity_plan(
                conn,
                decision_id=decision_id,
                signal_id=str(decision["signal_id"]),
                symbol=str(plan["symbol"]),
                plan=plan,
                validation=parity,
                clean=True,
                evidence_class="forward_post_activation",
                source="mexc_preflight_v2",
                captured_at=preflight_at,
            )
            ls.record_venue_attempt(
                conn, decision_id=decision_id, venue="mexc", stage="PRE_SUBMISSION_CHECK",
                status="PASSED", diagnostic={
                    "symbol": plan.get("symbol"),
                    "parity_clean": bool(parity.get("clean")),
                    "estimated_margin_usdt": plan.get("estimated_margin_usdt"),
                },
            )
            if route_diagnostic is not None:
                ls.event(conn, "LIVE_VENUE_SELECTED", decision_id=decision_id,
                         payload=route_diagnostic)
            conn.commit()
        _emit_live_latency(path, "mexc_preflight_passed", decision,
                           note={"decision_id": decision_id, "symbol": plan.get("symbol")})
    except (PlanRejected, MexcAPIError, ValueError) as exc:
        details = dict(getattr(exc, "details", {}) or {})
        diagnostic = {"reason": str(exc), **details}
        # Retry only transient pre-submission failures inside the frozen entry
        # window. Every subsequent attempt re-runs price, spread, parity and
        # risk checks before an order can be created.
        spread_retry = (
            str(exc) == "SPREAD_TOO_WIDE"
            and total_entry_age < max_queue_age
            and int(item.get("attempt_count") or 0) < int(cfg.get("max_spread_retry_attempts", 4))
        )
        transient_retry = (
            _is_transient_preflight_error(exc)
            and total_entry_age < max_queue_age
            and int(item.get("attempt_count") or 0) < _transient_preflight_retry_limit(cfg, decision)
        )
        with ls.connect(path) as conn:
            ls.record_venue_attempt(
                conn, decision_id=decision_id, venue="mexc", stage="PREFLIGHT",
                status="REJECTED", reason=str(exc), diagnostic=diagnostic,
            )
            if spread_retry or transient_retry:
                delay = (
                    float(cfg.get("spread_retry_interval_seconds", 3.0))
                    if spread_retry else _transient_preflight_retry_delay(cfg, item)
                )
                diagnostic.update(
                    retry_in_seconds=delay,
                    total_entry_age_seconds=round(total_entry_age, 3),
                    max_entry_age_seconds=max_queue_age,
                )
                ls.defer_outbox(conn, outbox_id, delay_seconds=delay,
                                result=diagnostic, error=str(exc))
                event_type = "ORDER_PREFLIGHT_SPREAD_RETRY" if spread_retry else "ORDER_PREFLIGHT_TRANSIENT_RETRY"
                ls.event(conn, event_type, decision_id=decision_id,
                         severity="INFO", payload=diagnostic)
                conn.commit()
                return {
                    "status": "RETRY_SPREAD" if spread_retry else "RETRY_TRANSIENT_PREFLIGHT",
                    "decision_id": decision_id,
                    **diagnostic,
                }
            ls.complete_outbox(conn, outbox_id, "REJECTED_PREFLIGHT", result=diagnostic, error=str(exc))
            ls.event(conn, "ORDER_PLAN_REJECTED", decision_id=decision_id, severity="WARNING",
                     payload=diagnostic)
            conn.commit()
        _stage_live_preflight_rejection_notification(
            path, decision_id=decision_id, decision=decision, reason=str(exc),
        )
        _emit_live_latency(path, "mexc_preflight_rejected", decision, note=diagnostic)
        return {"status": "REJECTED_PREFLIGHT", "decision_id": decision_id, **diagnostic}

    if cfg.execution_mode != "live":
        with ls.connect(path) as conn:
            _insert_order(conn, decision_id=decision_id, plan=plan, status="DRY_RUN_PLANNED")
            ls.complete_outbox(conn, outbox_id, "DRY_RUN_PLANNED", result=plan)
            ls.event(conn, "DRY_RUN_ORDER_PLANNED", decision_id=decision_id, payload=plan)
            conn.commit()
        return {"status": "DRY_RUN_PLANNED", "decision_id": decision_id, "plan": plan}

    with ls.connect(path) as conn:
        equity_basis = min(cfg.allocated_equity_usdt, float(equity or cfg.allocated_equity_usdt))
        if (_daily_loss_guard_applies(decision, cfg)
                and _daily_realized_loss(conn) >= cfg.daily_loss_limit_usdt):
            ls.complete_outbox(conn, outbox_id, "REJECTED_DAILY_LOSS", error="daily loss limit")
            ls.event(
                conn, "MODE_DAILY_LOSS_REJECTED", decision_id=decision_id,
                severity="WARNING",
                payload={"risk_bucket": str(decision.get("risk_bucket") or "default")},
            )
            conn.commit()
            return {"status": "REJECTED_DAILY_LOSS", "decision_id": decision_id}
        reservation = ls.reserve_risk(
            conn, decision_id=decision_id,
            symbol=str(plan.get("canonical_symbol") or decision["symbol"]).upper(),
            risk_usdt=float(plan["actual_risk_usdt"]), margin_usdt=float(plan["estimated_margin_usdt"]),
            notional_usdt=float(plan["notional_usdt"]),
            max_risk_usdt=cfg.max_concurrent_risk_usdt,
            max_margin_usdt=cfg.execution_limit(
                "max_total_margin_usdt", decision, 50.0, allow_unlimited=True),
            max_notional_usdt=cfg.execution_limit(
                "max_gross_notional_usdt", decision, 500.0, allow_unlimited=True),
            max_open_same_symbol=int(cfg.get("max_open_same_symbol", 1)),
            venue="mexc",
            allow_rebind_released=bybit_definitively_rejected,
        )
        if not reservation.get("ok"):
            ls.complete_outbox(conn, outbox_id, "REJECTED_RISK_LIMIT", error=reservation.get("reason"))
            return {"status": "REJECTED_RISK_LIMIT", "decision_id": decision_id,
                    "reason": reservation.get("reason")}
        _insert_order(conn, decision_id=decision_id, plan=plan, status="SUBMITTING")

    exchange_result: dict[str, Any]
    with ls.connect(path) as conn:
        ls.record_venue_attempt(
            conn, decision_id=decision_id, venue="mexc", stage="SUBMISSION",
            status="SUBMITTING", diagnostic={"symbol": plan.get("symbol")},
        )
        conn.commit()
    try:
        exchange_result = client.create_order(plan_obj.mexc_order())
    except MexcAPIError as exc:
        if _is_definitive_submission_rejection(exc):
            diagnostic = {
                "reason": str(exc),
                "code": exc.code,
                "status_code": exc.status_code,
                "order_accepted": False,
            }
            with ls.connect(path) as conn:
                ls.record_venue_attempt(
                    conn, decision_id=decision_id, venue="mexc", stage="SUBMISSION",
                    status="REJECTED", reason=str(exc), diagnostic=diagnostic,
                )
                _insert_order(
                    conn, decision_id=decision_id, plan=plan,
                    status="REJECTED_SUBMISSION", error=str(exc),
                )
                ls.release_risk(conn, decision_id, "exchange definitively rejected entry submission")
                ls.event(
                    conn, "ORDER_SUBMISSION_REJECTED", decision_id=decision_id,
                    severity="WARNING", payload=diagnostic,
                )
                conn.commit()
            _emit_live_latency(
                path, "mexc_order_submission_rejected", decision,
                note={"decision_id": decision_id, **diagnostic},
            )
            # A definitive MEXC business rejection proves that no order was
            # accepted. Only in that state may the same immutable decision be
            # re-preflighted on Bybit without risking a duplicate position.
            # Transport timeouts and unknown submission states never enter
            # this branch.
            if cfg.bybit_live_armed() and not bybit_definitively_rejected:
                fallback_age = (
                    (datetime.now(timezone.utc) - age_basis).total_seconds()
                    + max(0.0, frozen_entry_age)
                    if age_basis is not None else float("inf")
                )
                try:
                    if fallback_age > max_queue_age:
                        raise PlanRejected("BYBIT_FALLBACK_ENTRY_STALE")
                    fallback_candidate = prepare_candidate(
                        venue="bybit", decision=decision, cfg=cfg,
                        captured_at=ls.utc_now(),
                        client=bybit_execution_client or make_bybit_client(cfg, private=True),
                        reprice_callback=_maybe_reprice_swing_recovery,
                    )
                except (PlanRejected, BybitAPIError, ValueError) as fallback_exc:
                    fallback_diagnostic = {
                        **diagnostic,
                        "fallback_venue": "bybit",
                        "fallback_reason": str(fallback_exc),
                    }
                    with ls.connect(path) as conn:
                        _record_venue_route_attempts(
                            conn, decision_id=decision_id, diagnostic={
                                "rejected": {"bybit": {
                                    "reason": str(fallback_exc),
                                    "error_type": type(fallback_exc).__name__,
                                }},
                            },
                        )
                        ls.complete_outbox(
                            conn, outbox_id, "REJECTED_SUBMISSION",
                            result=fallback_diagnostic, error=str(exc),
                        )
                        ls.event(
                            conn, "BYBIT_FALLBACK_PREFLIGHT_REJECTED",
                            decision_id=decision_id, severity="WARNING",
                            payload=fallback_diagnostic,
                        )
                        conn.commit()
                    _stage_live_preflight_rejection_notification(
                        path, decision_id=decision_id, decision=decision,
                        reason="MEXC_REJECTED_BYBIT_FALLBACK_UNAVAILABLE",
                    )
                    return {
                        "status": "REJECTED_SUBMISSION", "decision_id": decision_id,
                        **fallback_diagnostic,
                    }
                fallback_route = {
                    "selected": "bybit",
                    "selection_reason": "mexc_definitive_rejection_fallback",
                    "candidates": {
                        "bybit": {
                            "all_in_cost_bps": fallback_candidate.all_in_cost_bps,
                            "spread_bps": fallback_candidate.plan_obj.spread_bps,
                            "preflight_latency_ms": fallback_candidate.preflight_latency_ms,
                            "symbol": fallback_candidate.plan_obj.symbol,
                        },
                    },
                    "rejected": {"mexc": diagnostic},
                }
                with ls.connect(path) as conn:
                    _record_venue_route_attempts(
                        conn, decision_id=decision_id, diagnostic=fallback_route,
                    )
                    ls.event(
                        conn, "MEXC_REJECTION_FALLBACK_TO_BYBIT",
                        decision_id=decision_id, severity="WARNING",
                        payload=fallback_route,
                    )
                    conn.commit()
                result = _execute_bybit_candidate(
                    path=path, cfg=cfg, item=item, decision=decision,
                    candidate=fallback_candidate, route_diagnostic=fallback_route,
                )
                return {**result, "fallback_from": "mexc"}
            with ls.connect(path) as conn:
                ls.complete_outbox(
                    conn, outbox_id, "REJECTED_SUBMISSION",
                    result=diagnostic, error=str(exc),
                )
                conn.commit()
            return {
                "status": "REJECTED_SUBMISSION", "decision_id": decision_id,
                **diagnostic,
            }
        # A timeout can occur after MEXC accepted the order. Query the deterministic
        # externalOid before deciding it failed; never blind-retry a create.
        try:
            exchange_result = client.order_by_external_id(plan["symbol"], plan["external_oid"])
        except MexcAPIError:
            with ls.connect(path) as conn:
                ls.record_venue_attempt(
                    conn, decision_id=decision_id, venue="mexc", stage="SUBMISSION",
                    status="UNKNOWN", reason=str(exc), diagnostic={"reason": str(exc)},
                )
                _insert_order(conn, decision_id=decision_id, plan=plan, status="SUBMISSION_UNKNOWN",
                              error=str(exc))
                ls.set_kill_switch(conn, "TRIPPED", "order submission state unknown")
                ls.complete_outbox(conn, outbox_id, "SUBMISSION_UNKNOWN", error=str(exc))
            _emit_live_latency(path, "mexc_order_submission_unknown", decision,
                               note={"decision_id": decision_id, "error": type(exc).__name__})
            return {"status": "SUBMISSION_UNKNOWN", "decision_id": decision_id}

    with ls.connect(path) as conn:
        ls.record_venue_attempt(
            conn, decision_id=decision_id, venue="mexc", stage="SUBMISSION",
            status="SUBMITTED", diagnostic={"order_id": exchange_result.get("orderId")},
        )
        _insert_order(conn, decision_id=decision_id, plan=plan, status="SUBMITTED",
                      exchange=exchange_result)
        ls.complete_outbox(conn, outbox_id, "SUBMITTED", result={"orderId": exchange_result.get("orderId")})
        ls.event(conn, "ORDER_SUBMITTED", decision_id=decision_id,
                 payload={"orderId": exchange_result.get("orderId"), "externalOid": plan["external_oid"]})
        conn.commit()
    _emit_live_latency(path, "mexc_order_submitted", decision,
                       note={"decision_id": decision_id, "symbol": plan.get("symbol")})
    # The entry itself carries MEXC's native stop.  In a burst, defer only the
    # slower three-TP reconciliation until every claimed MEXC entry has been
    # submitted; this prevents a first position's TP installation from making
    # a later fresh signal stale.  The enclosing monitor tick immediately runs
    # one reconciliation for the whole burst.  Bybit never uses this path: its
    # order needs a separate immediate stop installation.
    if reconcile_after_submission:
        protection = reconcile_once(db=path, cfg=cfg, client=client)
    else:
        protection = {
            "status": "DEFERRED_NATIVE_STOP_ATTACHED",
            "reason": "burst_preflight",
        }
    result = {"status": "SUBMITTED", "decision_id": decision_id,
              "order_id": exchange_result.get("orderId"), "protection": protection,
              "venue": "mexc"}
    if bybit_definitively_rejected:
        result["fallback_from"] = "bybit"
    return result


def _queued_outbox_count(path: Path) -> int:
    with ls.connect(path) as conn:
        ls.ensure_tables(conn)
        row = conn.execute(
            "SELECT COUNT(*) FROM mexc_canary_outbox WHERE status='QUEUED' AND available_at<=?",
            (ls.utc_now(),),
        ).fetchone()
    return int(row[0] or 0)


def _drain_outbox(path: Path, cfg: LiveCanaryConfig,
                  client: MexcFuturesClient | None = None,
                  bybit_execution_client: BybitFuturesClient | None = None) -> dict[str, Any]:
    """Drain a bounded burst before one consolidated position reconciliation.

    A former one-batch implementation left the third and later signal waiting
    behind the next full monitor cycle.  That was enough for a valid short-lived
    entry to become stale even when capture itself took only a few seconds.
    Each MEXC entry is protected by its native stop on creation; the monitor
    reconciles all deferred MEXC TP legs immediately after this bounded burst.
    """
    try:
        queued_at_start = _queued_outbox_count(path)
    except Exception as exc:
        return {"status": "RETRY_DB_BUSY" if ls.is_database_busy(exc) else "WORKER_ERROR",
                "error_type": type(exc).__name__}
    if queued_at_start <= 0:
        return worker_once(
            db=path, cfg=cfg, client=client,
            bybit_execution_client=bybit_execution_client,
        )

    workers = max(1, int(cfg.get("preflight_parallel_workers", 1)))
    batch_limit = max(1, int(cfg.get("preflight_batch_size", workers)))
    max_batches = max(1, int(cfg.get("preflight_max_batches_per_tick", 1)))
    results: list[dict[str, Any]] = []
    batches_processed = 0
    max_parallel_workers = 0

    for _ in range(max_batches):
        try:
            queued = _queued_outbox_count(path)
        except Exception as exc:
            results.append({
                "status": "RETRY_DB_BUSY" if ls.is_database_busy(exc) else "WORKER_ERROR",
                "error_type": type(exc).__name__,
            })
            break
        if queued <= 0:
            break
        take = min(queued, workers, batch_limit)
        batches_processed += 1
        max_parallel_workers = max(max_parallel_workers, take)
        # One isolated order keeps the immediate post-submit reconciliation.
        # A true burst defers only MEXC TP installation: its native stop is
        # already attached to the entry and the caller performs one consolidated
        # reconciliation once this bounded drain completes.
        defer_mexc_reconciliation = take > 1 or queued > take
        if take == 1:
            try:
                results.append(worker_once(
                    db=path, cfg=cfg, client=client,
                    bybit_execution_client=bybit_execution_client,
                    reconcile_after_submission=not defer_mexc_reconciliation,
                ))
            except Exception as exc:
                results.append({"status": "WORKER_ERROR", "error_type": type(exc).__name__})
            continue
        with ThreadPoolExecutor(max_workers=take, thread_name_prefix="mexc-preflight") as executor:
            # Reuse the monitor's persistent authenticated session for one worker.
            # Additional burst workers get isolated sessions so requests.Session is
            # never shared concurrently between threads.
            futures = [
                executor.submit(
                    worker_once, db=path, cfg=cfg,
                    client=client if index == 0 else None,
                    bybit_execution_client=bybit_execution_client if index == 0 else None,
                    reconcile_after_submission=False,
                )
                for index in range(take)
            ]
            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as exc:
                    results.append({"status": "WORKER_ERROR", "error_type": type(exc).__name__})

        # Retried rows remain queued with their own availability time.  Do not
        # immediately reclaim the same temporarily rate-limited/locked work
        # within this tick; later independent entries will be picked up on the
        # next fast tick once the short backoff has elapsed.
        if any(
            str(result.get("status") or "") in {
                "RETRY_TRANSIENT_PREFLIGHT", "RETRY_DB_BUSY",
            }
            for result in results[-take:]
        ):
            break

    if len(results) == 1 and batches_processed == 1:
        return results[0]
    return {
        "status": "BATCH",
        "queued_at_start": queued_at_start,
        "batches_processed": batches_processed,
        "parallel_workers": max_parallel_workers,
        "results": results,
    }


def monitor_tick(*, db: str | Path | None = None, cfg: LiveCanaryConfig | None = None,
                 reconciliation_client: MexcFuturesClient | None = None,
                 execution_client: MexcFuturesClient | None = None,
                 bybit_reconciliation_client: BybitFuturesClient | None = None,
                 bybit_execution_client: BybitFuturesClient | None = None) -> dict[str, Any]:
    """Run one canary worker/reconciliation tick without letting a transient failure kill the monitor."""
    cfg = cfg or load_live_canary_config()
    path = _db_path(db)
    global _LAST_STALE_QUEUE_MAINTENANCE_MONOTONIC
    stale_queue_maintenance: dict[str, Any] = {"status": "NOT_DUE"}
    monotonic_now = time.monotonic()
    maintenance_interval = max(
        5.0, float(cfg.get("stale_queue_maintenance_interval_seconds", 15.0))
    )
    if monotonic_now - _LAST_STALE_QUEUE_MAINTENANCE_MONOTONIC >= maintenance_interval:
        _LAST_STALE_QUEUE_MAINTENANCE_MONOTONIC = monotonic_now
        try:
            # Safe recovery only: expired rows without an order, reservation,
            # or submission footprint are terminalized. It can never requeue
            # or create a trade.
            stale_queue_maintenance = invalidate_stale_queues(db=path, cfg=cfg)
        except Exception as exc:
            stale_queue_maintenance = {
                "status": "RETRY_DB_BUSY" if ls.is_database_busy(exc) else "ERROR",
                "error_type": type(exc).__name__,
            }
    start_heartbeat: dict[str, Any] = {"status": "SKIPPED"}
    try:
        def _write_start_heartbeat(conn: sqlite3.Connection) -> None:
            ls.ensure_tables(conn)
            active_positions = int(conn.execute(
                "SELECT COUNT(*) FROM mexc_canary_positions WHERE status='OPEN'"
            ).fetchone()[0])
            ls.set_monitor_heartbeat(
                conn,
                status="OK",
                live_armed=cfg.live_armed(),
                active_positions=active_positions,
                detail={
                    "worker": "TICK_RUNNING",
                    "reconcile": "PENDING",
                    "armed_venues": cfg.enabled_live_venues(asset_class="stocks"),
                },
            )
            conn.commit()
        _reconcile_db_write(path=path, cfg=cfg, operation=_write_start_heartbeat)
        start_heartbeat = {"status": "OK"}
    except Exception as exc:
        start_heartbeat = {
            "status": "RETRY_DB_BUSY" if ls.is_database_busy(exc) else "START_HEARTBEAT_ERROR",
            "error_type": type(exc).__name__,
        }
    try:
        worker = _drain_outbox(
            path, cfg, client=execution_client,
            bybit_execution_client=bybit_execution_client,
        )
    except Exception as exc:  # A monitor must keep retrying its isolated outbox.
        worker = {
            "status": "RETRY_DB_BUSY" if ls.is_database_busy(exc) else "WORKER_ERROR",
            "error_type": type(exc).__name__,
        }
    worker_protection = worker.get("protection") if isinstance(worker, dict) else None
    if (
        isinstance(worker_protection, dict)
        and worker.get("status") == "SUBMITTED"
        and str(worker_protection.get("status") or "") in {"OK", "DEGRADED"}
        and not cfg.bybit_live_armed()
    ):
        reconcile = {**worker_protection, "source": "worker_submit_protection"}
    else:
        try:
            venue_results: dict[str, Any] = {}
            if cfg.mexc_live_armed():
                venue_results["mexc"] = reconcile_once(
                    db=path, cfg=cfg, client=reconciliation_client
                )
            if cfg.bybit_live_armed():
                venue_results["bybit"] = reconcile_bybit_once(
                    db=path, cfg=cfg,
                    client=bybit_reconciliation_client or make_bybit_client(cfg, private=True),
                )
            if not venue_results:
                reconcile = {"status": "BLOCKED_NOT_ARMED", "venues": {}}
            else:
                statuses = {str(value.get("status") or "UNKNOWN") for value in venue_results.values()}
                combined_status = "OK" if statuses == {"OK"} else (
                    "DEGRADED" if "DEGRADED" in statuses else sorted(statuses)[0]
                )
                reconcile = {"status": combined_status, "venues": venue_results}
        except Exception as exc:  # Existing positions must be retried on the next fast tick.
            reconcile = {
                "status": "RETRY_DB_BUSY" if ls.is_database_busy(exc) else "RECONCILE_ERROR",
                "error_type": type(exc).__name__,
            }
    try:
        def _write_finish_heartbeat(conn: sqlite3.Connection) -> None:
            ls.ensure_tables(conn)
            active_positions = int(conn.execute(
                "SELECT COUNT(*) FROM mexc_canary_positions WHERE status='OPEN'"
            ).fetchone()[0])
            status = str(reconcile.get("status") or "UNKNOWN")
            ls.set_monitor_heartbeat(
                conn,
                status=status,
                live_armed=cfg.live_armed(),
                active_positions=active_positions,
                detail={
                    "worker": worker.get("status"),
                    "reconcile": status,
                    "armed_venues": cfg.enabled_live_venues(asset_class="stocks"),
                },
            )
            if active_positions and status != "OK":
                ls.event_if_due(
                    conn,
                    "OPEN_POSITION_MONITOR_DEGRADED",
                    severity="CRITICAL",
                    payload={"reconcile": status, "worker": worker.get("status")},
                    cooldown_seconds=float(
                        cfg.get("position_reconcile_error_event_cooldown_seconds", 60)
                    ),
                )
            conn.commit()
        _reconcile_db_write(path=path, cfg=cfg, operation=_write_finish_heartbeat)
    except Exception as exc:
        heartbeat = {"status": "HEARTBEAT_ERROR", "error_type": type(exc).__name__}
    else:
        heartbeat = {"status": "OK", "reconcile": reconcile.get("status")}
    # Delivery is intentionally after worker/reconcile persistence.  A Telegram
    # timeout can delay only this informational path; it cannot delay, repeat,
    # cancel, or alter an exchange order or its protection.
    try:
        live_notifications = _deliver_live_fill_notifications(path)
    except Exception as exc:
        live_notifications = {"status": f"delivery_error:{type(exc).__name__}", "sent": 0, "failed": 1}
    watchdog = {"status": "DISABLED"}
    watchdog_cfg = cfg.get("watchdog", {}) or {}
    if bool(watchdog_cfg.get("enabled", True)):
        try:
            from .watchdog import audit as watchdog_audit
            watchdog = watchdog_audit(
                db=path,
                cfg=cfg,
                reconcile_result=reconcile,
                send_telegram=bool(watchdog_cfg.get("send_telegram_on_monitor_tick", True)),
                check_heartbeat=True,
            )
        except Exception as exc:
            watchdog = {
                "status": "WATCHDOG_ERROR",
                "error_type": type(exc).__name__,
                "error": str(exc)[:240],
            }
    return {
        "worker": worker,
        "reconcile": reconcile,
        "heartbeat": heartbeat,
        "start_heartbeat": start_heartbeat,
        "stale_queue_maintenance": stale_queue_maintenance,
        "live_notifications": live_notifications,
        "watchdog": watchdog,
    }


def _upsert_filled_position(conn: sqlite3.Connection, *, decision_id: str, plan: dict[str, Any],
                            order: dict[str, Any], position: dict[str, Any]) -> None:
    now = ls.utc_now()
    entry = float(order.get("dealAvgPrice") or position.get("openAvgPrice") or plan["limit_price"])
    rebased = rebase_filled_plan(plan, fill_price=entry)
    plan.clear()
    plan.update(rebased)
    volume = float(order.get("dealVol") or position.get("holdVol") or plan["volume_contracts"])
    notional = volume * float(plan["contract_size"]) * entry
    risk_detail = stop_risk_components(
        entry_price=entry,
        stop_price=float(plan["original_stop"]),
        volume_contracts=volume,
        contract_size=float(plan["contract_size"]),
        taker_fee_rate=float(plan.get("taker_fee_rate") or 0.0),
        slippage_rate=float(plan.get("slippage_rate") or 0.0),
    )
    risk = risk_detail["net_stop_risk_usdt"]
    liq = position.get("liquidatePrice")
    conn.execute(
        "INSERT INTO mexc_canary_positions(" 
        "position_row_id,decision_id,exchange_position_id,symbol,direction,status,entry_price,original_stop,"
        "current_stop,tp3,volume_contracts,notional_usdt,risk_usdt,leverage,liquidation_price,"
        "highest_price,favorable_price,max_favorable_r,protection_stage,opened_at,updated_at,exchange_json,venue) "
        "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
        "ON CONFLICT(decision_id) DO UPDATE SET exchange_position_id=excluded.exchange_position_id,"
        "direction=excluded.direction,status='OPEN',entry_price=excluded.entry_price,volume_contracts=excluded.volume_contracts,"
        "notional_usdt=excluded.notional_usdt,risk_usdt=excluded.risk_usdt,"
        "liquidation_price=excluded.liquidation_price,updated_at=excluded.updated_at,"
        "exchange_json=excluded.exchange_json,venue='mexc'",
        (str(uuid.uuid4()), decision_id, str(position.get("positionId") or order.get("positionId") or ""),
         plan["symbol"], str(plan.get("direction") or "long"), "OPEN", entry,
         float(plan["original_stop"]), float(plan["original_stop"]),
         float(plan["tp3"]), volume, notional, risk, int(plan["leverage"]),
         float(liq) if liq not in (None, "") else None, entry, entry, 0.0, "ORIGINAL_STOP", now, now,
         json.dumps(position, sort_keys=True), "mexc"),
    )
    conn.execute(
        "UPDATE mexc_canary_risk_reservations SET status='OPEN',risk_usdt=?,notional_usdt=?,updated_at=? "
        "WHERE decision_id=? AND status='RESERVED'", (risk, notional, now, decision_id))
    ls.event(conn, "FILLED_RISK_RECALCULATED", decision_id=decision_id, payload={
        "fill_price": entry,
        "volume_contracts": volume,
        "contract_size": float(plan["contract_size"]),
        **risk_detail,
        "planned_worst_case_risk_usdt": float(plan.get("actual_risk_usdt") or 0.0),
        "fill_rebased": True,
        "rebased_stop": float(plan["original_stop"]),
        "rebased_targets": [float(plan["tp1"]), float(plan["tp2"]), float(plan["tp3"])],
    })
    conn.commit()


def recalculate_open_position_risk_accounting(*, db: str | Path | None = None) -> dict[str, Any]:
    """Correct local reservations for already-filled positions without exchange writes.

    Early live positions stored the entry plan's IOC-cap risk after a better
    actual fill.  This maintenance pass uses the persisted fill, contract
    multiplier and frozen stop.  It does not modify orders, stops, TPs or the
    position at MEXC.
    """
    path = _db_path(db)
    result = {"status": "OK", "checked": 0, "corrected": 0, "skipped": []}
    with ls.connect(path) as conn:
        rows = conn.execute(
            "SELECT p.decision_id,p.symbol,p.entry_price,p.original_stop,p.volume_contracts,p.risk_usdt,"
            "(SELECT o.plan_json FROM mexc_canary_orders o "
            " WHERE o.decision_id=p.decision_id AND o.status='FILLED' "
            " ORDER BY o.updated_at DESC LIMIT 1) AS plan_json "
            "FROM mexc_canary_positions p WHERE p.status='OPEN'"
        ).fetchall()
        for row in rows:
            result["checked"] += 1
            try:
                plan = json.loads(str(row["plan_json"] or "{}"))
                detail = stop_risk_components(
                    entry_price=float(row["entry_price"]),
                    stop_price=float(row["original_stop"]),
                    volume_contracts=float(row["volume_contracts"]),
                    contract_size=float(plan["contract_size"]),
                    taker_fee_rate=float(plan.get("taker_fee_rate") or 0.0),
                    slippage_rate=float(plan.get("slippage_rate") or 0.0),
                )
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
                result["skipped"].append({
                    "decision_id": str(row["decision_id"]),
                    "reason": f"RISK_ACCOUNTING_METADATA_UNAVAILABLE:{type(exc).__name__}",
                })
                continue
            corrected = detail["net_stop_risk_usdt"]
            previous = float(row["risk_usdt"])
            if abs(previous - corrected) <= 1e-8:
                continue
            now = ls.utc_now()
            conn.execute(
                "UPDATE mexc_canary_positions SET risk_usdt=?,updated_at=? WHERE decision_id=? AND status='OPEN'",
                (corrected, now, str(row["decision_id"])),
            )
            conn.execute(
                "UPDATE mexc_canary_risk_reservations SET risk_usdt=?,updated_at=? "
                "WHERE decision_id=? AND status='OPEN'",
                (corrected, now, str(row["decision_id"])),
            )
            ls.event(conn, "OPEN_POSITION_RISK_ACCOUNTING_CORRECTED",
                     decision_id=str(row["decision_id"]), payload={
                         "symbol": str(row["symbol"]),
                         "previous_net_stop_risk_usdt": previous,
                         **detail,
                     })
            result["corrected"] += 1
        conn.commit()
    return result


def _tpsl_id(order: dict[str, Any]) -> str:
    return str(order.get("id") or order.get("stopPlanOrderId") or "")


def _exit_leg_verification_due(*, path: Path, local: dict[str, Any],
                               cfg: LiveCanaryConfig, now: datetime | None = None) -> bool:
    """Throttle only redundant remote exit-leg reads after native protection exists."""
    if not str(local.get("tpsl_order_id") or ""):
        return True
    interval = max(3.0, float(cfg.get("exit_leg_verify_interval_seconds", 12.0)))
    moment = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    with ls.connect(path) as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS n, MAX(updated_at) AS latest_at "
            "FROM mexc_canary_exit_legs WHERE decision_id=?",
            (str(local["decision_id"]),),
        ).fetchone()
    if row is None or int(row["n"] or 0) != 3:
        return True
    latest = _parse_utc(row["latest_at"])
    return latest is None or (moment - latest).total_seconds() >= interval


def _emergency_close(*, client: MexcFuturesClient, direction: str, symbol: str,
                     position_id: int, volume: float, external_oid: str) -> dict[str, Any]:
    if str(direction).lower() == "short":
        return client.emergency_close_short(
            symbol=symbol, position_id=position_id, volume=volume, external_oid=external_oid,
        )
    return client.emergency_close_long(
        symbol=symbol, position_id=position_id, volume=volume, external_oid=external_oid,
    )


def _active_position_tpsl(client: MexcFuturesClient, symbol: str,
                          position_id: str | int) -> list[dict[str, Any]]:
    return [
        item for item in client.open_tpsl_orders(symbol)
        if str(item.get("positionId") or "") == str(position_id)
        and int(item.get("state") or 0) == 1
        and _tpsl_id(item)
    ]


def _exit_visibility_timeout(cfg: LiveCanaryConfig) -> tuple[float, float]:
    """Bounded MEXC read-after-write wait for a just-filled position."""
    timeout = max(float(cfg.get("exit_visibility_timeout_seconds", 6.0)), 0.0)
    poll = max(float(cfg.get("exit_visibility_poll_seconds", 0.25)), 0.05)
    return timeout, poll


def _matching_fallback_stop(*, client: MexcFuturesClient, symbol: str,
                            position_id: str, stop: float, tick: float) -> dict[str, Any] | None:
    active = _active_position_tpsl(client, symbol, position_id)
    if len(active) > 1:
        raise MexcAPIError("MEXC position has multiple active TP/SL plans; refusing ambiguous protection")
    if not active:
        return None
    candidate = active[0]
    if float(candidate.get("takeProfitPrice") or 0) > 0:
        raise MexcAPIError("MEXC fallback stop unexpectedly contains a take-profit")
    if abs(float(candidate.get("stopLossPrice") or 0) - stop) > max(tick, 1e-12):
        return None
    return candidate


def _wait_for_fallback_stop(*, client: MexcFuturesClient, symbol: str,
                            position_id: str, hold_volume: float, stop: float,
                            tick: float, cfg: LiveCanaryConfig) -> dict[str, Any]:
    """Wait for the entry-attached stop, then create one exactly once if absent."""
    timeout, poll = _exit_visibility_timeout(cfg)
    modified_existing = False

    def observe_and_rebase() -> dict[str, Any] | None:
        nonlocal modified_existing
        active = _active_position_tpsl(client, symbol, position_id)
        if len(active) > 1:
            raise MexcAPIError(
                "MEXC position has multiple active TP/SL plans; refusing ambiguous protection"
            )
        if not active:
            return None
        candidate = active[0]
        if float(candidate.get("takeProfitPrice") or 0) > 0:
            raise MexcAPIError("MEXC fallback stop unexpectedly contains a take-profit")
        if abs(float(candidate.get("stopLossPrice") or 0) - stop) <= max(tick, 1e-12):
            return candidate
        if not modified_existing:
            client.modify_tpsl(
                stop_plan_order_id=int(_tpsl_id(candidate)), stop_loss=stop, take_profit=None,
            )
            modified_existing = True
        return None

    deadline = time.monotonic() + timeout
    while True:
        found = observe_and_rebase()
        if found:
            return found
        if time.monotonic() >= deadline:
            break
        time.sleep(poll)

    if modified_existing:
        raise MexcAPIError("MEXC rebased fallback stop was not visible after bounded verification")

    # The entry was filled but its attached stop is not visible. Install a single
    # explicit position stop, then prove it is visible before placing any TP legs.
    client.place_position_tpsl(
        position_id=int(position_id), volume=hold_volume, stop_loss=stop, take_profit=None,
    )
    deadline = time.monotonic() + timeout
    while True:
        found = _matching_fallback_stop(
            client=client, symbol=symbol, position_id=position_id, stop=stop, tick=tick,
        )
        if found:
            return found
        if time.monotonic() >= deadline:
            raise MexcAPIError("MEXC fallback stop was not visible after bounded verification")
        time.sleep(poll)


def _wait_for_close_limit_order(*, client: MexcFuturesClient, symbol: str,
                                order_id: str | int | None, external_oid: str,
                                cfg: LiveCanaryConfig) -> dict[str, Any]:
    """Read a close order by idempotency key until MEXC's read model catches up."""
    timeout, poll = _exit_visibility_timeout(cfg)
    transient_backoff = max(
        float(cfg.get("exit_visibility_transient_backoff_seconds", poll)),
        poll,
    )
    deadline = time.monotonic() + timeout
    last_error: Exception | None = None
    while True:
        transient = False
        if order_id not in (None, ""):
            try:
                observed = client.order_by_id(order_id)
                if observed:
                    return observed
            except Exception as exc:  # MEXC can briefly return not-found after create.
                last_error = exc
                transient = _is_transient_mexc_visibility_error(exc)
        try:
            observed = client.order_by_external_id(symbol, external_oid)
            if observed:
                return observed
        except Exception as exc:
            last_error = exc
            transient = transient or _is_transient_mexc_visibility_error(exc)
        if time.monotonic() >= deadline:
            suffix = f": {last_error}" if last_error else ""
            raise MexcAPIError(f"MEXC close-limit order was not visible after bounded verification{suffix}")
        time.sleep(min(transient_backoff if transient else poll, max(0.0, deadline - time.monotonic())))


def _persist_exit_legs(conn: sqlite3.Connection, *, decision_id: str,
                       orders: list[dict[str, Any]], targets: tuple[float, ...],
                       volumes: tuple[float, ...], stop: float, tick: float,
                       volume_step: float, leg_indices: tuple[int, ...] | None = None) -> None:
    now = ls.utc_now()
    if not orders or len(orders) != len(targets) or len(orders) != len(volumes):
        raise MexcAPIError("MEXC close-limit TP persistence inputs are inconsistent")
    indexes = leg_indices or tuple(range(1, len(orders) + 1))
    if len(indexes) != len(orders) or any(index not in {1, 2, 3} for index in indexes):
        raise MexcAPIError("MEXC close-limit TP leg indexes are inconsistent")
    for index, order, target, volume in zip(indexes, orders, targets, volumes):
        order_id = str(order.get("orderId") or "")
        external_oid = str(order.get("externalOid") or "")
        state = int(order.get("state") or 1)
        if not order_id or not external_oid:
            raise MexcAPIError(f"MEXC close-limit TP{index} identity is missing")
        if abs(float(order.get("price") or 0) - target) > max(tick, 1e-12):
            raise MexcAPIError(f"MEXC close-limit TP{index} price mismatch")
        if abs(float(order.get("vol") or 0) - volume) > max(volume_step * 1e-6, 1e-9):
            raise MexcAPIError(f"MEXC close-limit TP{index} volume mismatch")
        if state not in {1, 2, 3}:
            raise MexcAPIError(f"MEXC close-limit TP{index} is not active or filled")
        cols = (
            "decision_id", "leg_index", "exchange_tpsl_id", "exchange_order_id",
            "external_oid", "order_kind", "target_price", "stop_price",
            "volume_contracts", "status", "created_at", "updated_at", "exchange_json",
        )
        values = (
            decision_id, index, None, order_id, external_oid, "CLOSE_LIMIT_TP",
            target, stop, volume, "FILLED" if state == 3 else "ACTIVE",
            now, now, json.dumps(order, sort_keys=True),
        )
        conn.execute(
            f"INSERT INTO mexc_canary_exit_legs({','.join(cols)}) "
            f"VALUES({','.join('?' for _ in cols)}) "
            "ON CONFLICT(decision_id,leg_index) DO UPDATE SET "
            "exchange_tpsl_id=NULL,exchange_order_id=excluded.exchange_order_id,"
            "external_oid=excluded.external_oid,order_kind=excluded.order_kind,"
            "target_price=excluded.target_price,"
            "stop_price=excluded.stop_price,volume_contracts=excluded.volume_contracts,"
            "status=excluded.status,updated_at=excluded.updated_at,exchange_json=excluded.exchange_json",
            values,
        )


def _persist_virtual_tp3_leg(conn: sqlite3.Connection, *, decision_id: str,
                              target: float, volume: float, stop: float) -> None:
    """Persist a monitored TP3 runner when MEXC supports two native limits."""
    now = ls.utc_now()
    conn.execute(
        "INSERT INTO mexc_canary_exit_legs("
        "decision_id,leg_index,exchange_tpsl_id,exchange_order_id,external_oid,order_kind,"
        "target_price,stop_price,volume_contracts,status,created_at,updated_at,exchange_json) "
        "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) "
        "ON CONFLICT(decision_id,leg_index) DO UPDATE SET "
        "order_kind=excluded.order_kind,target_price=excluded.target_price,"
        "stop_price=excluded.stop_price,volume_contracts=excluded.volume_contracts,"
        "status=excluded.status,updated_at=excluded.updated_at,exchange_json=excluded.exchange_json",
        (
            decision_id, 3, None, None,
            "vtp3_" + decision_id.replace("-", "")[:26],
            "VIRTUAL_TP3_MONITOR", target, stop, volume, "ACTIVE", now, now,
            json.dumps({"execution": "monitor_market_close", "target_price": target}, sort_keys=True),
        ),
    )


def _confirmed_active_exit_orders(
    *, client: MexcFuturesClient, local: dict[str, Any], stored: list[dict[str, Any]],
    position_id: str, cfg: LiveCanaryConfig,
) -> list[dict[str, Any]] | None:
    """Prove active TP coverage after MEXC's partial-fill read models converge.

    MEXC can expose a reduced holding before it changes the immediately
    preceding close-limit order from ACTIVE to FILLED.  Treating that tiny
    read-order skew as an unprotected position trips the global kill switch
    unnecessarily.  A stable mismatch remains a real protection failure.
    """
    timeout, poll = _exit_visibility_timeout(cfg)
    deadline = time.monotonic() + timeout
    while True:
        positions = _open_positions_for_symbol(client, str(local["symbol"]))
        position = next(
            (row for row in positions if str(row.get("positionId") or "") == position_id), None,
        )
        if position is None:
            raise MexcAPIError("position disappeared while confirming partial TP coverage")
        hold_volume = float(position.get("holdVol") or 0)
        if hold_volume <= 0:
            raise MexcAPIError("open MEXC position has no hold volume during TP confirmation")
        active: list[dict[str, Any]] = []
        for leg in stored:
            if str(leg.get("order_kind") or "") == "VIRTUAL_TP3_MONITOR":
                if str(leg.get("status") or "") == "ACTIVE":
                    active.append({
                        "state": 1, "vol": float(leg.get("volume_contracts") or 0),
                        "orderId": None, "virtual": True,
                    })
                continue
            order_id = str(leg.get("exchange_order_id") or "")
            if not order_id:
                raise MexcAPIError("stored close-limit TP has no exchange order id")
            exchange = client.order_by_id(order_id)
            if int(exchange.get("state") or 0) in {1, 2}:
                active.append(exchange)
        active_volume = sum(float(item.get("vol") or 0) for item in active)
        if active and abs(active_volume - hold_volume) <= max(
            float(local.get("volume_step") or 0) * 1e-6, 1e-9,
        ):
            return active
        if time.monotonic() >= deadline:
            return None
        time.sleep(poll)


def _install_or_reconcile_exit_legs(*, path: Path, client: MexcFuturesClient,
                                    local: dict[str, Any], pos: dict[str, Any],
                                    cfg: LiveCanaryConfig) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    decision_id = str(local["decision_id"])
    position_id = str(local["exchange_position_id"])
    plan = json.loads(str(local["plan_json"]))
    targets = (float(plan["tp1"]), float(plan["tp2"]), float(plan["tp3"]))
    stop = float(local["current_stop"])
    tick = float(plan.get("price_tick") or 0)
    volume_step = float(plan.get("volume_step") or 0)
    min_volume = float(plan.get("min_volume") or 0)
    hold_volume = float(pos.get("holdVol") or 0)
    if hold_volume <= 0:
        raise MexcAPIError("open MEXC position has no hold volume")
    volumes = allocate_partial_tp_volumes(
        total_volume=float(local["volume_contracts"]),
        volume_step=volume_step,
        min_volume=min_volume,
        weights=_partial_tp_weights(cfg),
    )
    native_leg_count = _native_limit_tp_leg_count(cfg)
    with ls.connect(path) as conn:
        stored = [dict(row) for row in conn.execute(
            "SELECT * FROM mexc_canary_exit_legs WHERE decision_id=? ORDER BY leg_index",
            (decision_id,),
        ).fetchall()]

    fallback_stop = _wait_for_fallback_stop(
        client=client, symbol=local["symbol"], position_id=position_id,
        hold_volume=hold_volume, stop=stop, tick=tick, cfg=cfg,
    )
    if len(stored) != 3:
        observed_by_index: dict[int, dict[str, Any]] = {}
        created_order_ids: list[str] = []
        # The create call's own exception used to be discarded entirely (see below),
        # so a bounded-verification failure never revealed whether the leg was ever
        # actually submitted (a genuine MEXC rejection -- waiting longer never helps)
        # or the create call merely timed out on our side (idempotent externalOid
        # resubmission-safe -- a read-lag the poll can still catch). Captured here so
        # the eventual MEXC_THREE_TP_INSTALL_FAILED diagnostic carries the real cause.
        create_call_errors: dict[int, str] = {}
        failed_leg = 0
        try:
            stored_by_index = {int(leg["leg_index"]): leg for leg in stored}
            if len(stored_by_index) != len(stored) or any(index not in {1, 2, 3} for index in stored_by_index):
                raise MexcAPIError("stored close-limit TP legs are inconsistent")
            direction = str(local.get("direction") or plan.get("direction") or "long").lower()
            expected_side = 4 if direction == "long" else 2
            for index, (volume, target) in enumerate(
                zip(volumes[:native_leg_count], targets[:native_leg_count]), start=1
            ):
                failed_leg = index
                existing = stored_by_index.get(index)
                external_oid = str(existing.get("external_oid")) if existing else (
                    f"tp{index}_" + decision_id.replace("-", "")[:26]
                )
                submitted: dict[str, Any] = {}
                if existing:
                    submitted["orderId"] = str(existing.get("exchange_order_id") or "")
                else:
                    try:
                        submitted = client.place_close_limit(
                            symbol=local["symbol"], position_id=int(position_id),
                            direction=direction, volume=volume, price=target,
                            leverage=int(plan["leverage"]), external_oid=external_oid,
                            open_type=int(plan.get("open_type") or 1),
                        )
                    except Exception as create_exc:
                        # A create timeout may still have accepted the idempotent externalOid.
                        # Resolve it through the exchange instead of blindly resubmitting.
                        create_call_errors[index] = f"{type(create_exc).__name__}: {str(create_exc)[:300]}"
                        submitted = {}
                observed = _wait_for_close_limit_order(
                    client=client, symbol=local["symbol"], order_id=submitted.get("orderId"),
                    external_oid=external_oid, cfg=cfg,
                )
                observed.setdefault("orderId", submitted.get("orderId") or observed.get("orderId"))
                observed.setdefault("externalOid", external_oid)
                if str(observed.get("positionId") or "") != position_id:
                    raise MexcAPIError(f"MEXC close-limit TP{index} position mismatch")
                if int(observed.get("side") or expected_side) != expected_side:
                    raise MexcAPIError(f"MEXC close-limit TP{index} side mismatch")
                observed_by_index[index] = observed
                if not existing:
                    created_order_ids.append(str(observed.get("orderId") or ""))
                    # Persist confirmed legs immediately. A worker restart can resume
                    # the remaining legs through their deterministic externalOid values.
                    with ls.connect(path) as conn:
                        _persist_exit_legs(
                            conn, decision_id=decision_id, orders=[observed], targets=(target,),
                            volumes=(volume,), stop=stop, tick=tick, volume_step=volume_step,
                            leg_indices=(index,),
                        )
                        conn.commit()
            created = [observed_by_index[index] for index in range(1, native_leg_count + 1)]
            with ls.connect(path) as conn:
                _persist_exit_legs(
                    conn, decision_id=decision_id, orders=created,
                    targets=targets[:native_leg_count], volumes=volumes[:native_leg_count],
                    stop=stop, tick=tick, volume_step=volume_step,
                )
                if native_leg_count == 2:
                    _persist_virtual_tp3_leg(
                        conn, decision_id=decision_id, target=targets[2],
                        volume=volumes[2], stop=stop,
                    )
                ls.event(conn, "MEXC_THREE_TP_INSTALLED", decision_id=decision_id,
                         payload={
                             "targets": targets, "volumes": volumes, "stop": stop,
                             "fallback_stop_id": _tpsl_id(fallback_stop),
                             "close_order_ids": [str(item["orderId"]) for item in created],
                             "virtual_tp3": native_leg_count == 2,
                         })
                conn.commit()
            virtual = []
            if native_leg_count == 2:
                virtual = [{
                    "state": 1,
                    "vol": volumes[2],
                    "orderId": None,
                    "virtual": True,
                    "target": targets[2],
                }]
            return fallback_stop, created + virtual
        except Exception as exc:
            diagnostic = {
                "error_type": type(exc).__name__,
                "error": str(exc)[:500],
                "failed_leg": failed_leg,
                "created_order_ids": [
                    str(item.get("orderId") or "") for item in observed_by_index.values()
                    if item.get("orderId")
                ],
                # Surfaces the leg's own create-call exception, if any, alongside the
                # eventual "not visible" verification failure -- distinguishes a genuine
                # MEXC rejection from a same-side transport timeout going forward.
                "create_call_errors": create_call_errors,
                "fallback_stop_id": _tpsl_id(fallback_stop),
                "stop_price": stop,
            }
            keep_open_when_stop_verified = bool(
                (cfg.get("partial_take_profit", {}) or {}).get(
                    "keep_open_on_tp_install_failure_with_verified_stop", True
                )
            )
            if _tpsl_id(fallback_stop) and keep_open_when_stop_verified:
                diagnostic.update({
                    "emergency_close_submitted": False,
                    "emergency_close_error": None,
                    "action": "kept_position_open_because_fallback_stop_is_verified",
                    "retry": "next_reconcile_tick",
                })
                with ls.connect(path) as conn:
                    ls.event_if_due(
                        conn, "MEXC_TP_INSTALL_INCOMPLETE_RETRYING",
                        decision_id=decision_id, severity="WARNING",
                        payload=diagnostic, cooldown_seconds=float(
                            cfg.get("position_reconcile_error_event_cooldown_seconds", 60)
                        ),
                    )
                    conn.execute(
                        "UPDATE mexc_canary_orders SET last_error=?,updated_at=? WHERE decision_id=?",
                        (json.dumps(diagnostic, sort_keys=True), ls.utc_now(), decision_id),
                    )
                    conn.commit()
                return fallback_stop, [
                    observed_by_index[index] for index in sorted(observed_by_index)
                ]

            # If no protective stop was proven, the position is genuinely
            # unprotected and the fail-safe close remains mandatory.
            try:
                ids = [item for item in created_order_ids if item]
                if ids:
                    client.cancel_order_ids(ids)
            except Exception:
                pass
            emergency_submitted = False
            emergency_error: str | None = None
            try:
                _emergency_close(
                    client=client, direction=str(local.get("direction") or plan.get("direction") or "long"),
                    symbol=local["symbol"], position_id=int(position_id), volume=hold_volume,
                    external_oid="xtp_" + decision_id.replace("-", "")[:27],
                )
                emergency_submitted = True
            except Exception as close_exc:
                emergency_error = f"{type(close_exc).__name__}: {str(close_exc)[:500]}"
            diagnostic.update({
                "emergency_close_submitted": emergency_submitted,
                "emergency_close_error": emergency_error,
                "action": "emergency_close_because_no_verified_fallback_stop",
            })
            with ls.connect(path) as conn:
                ls.set_kill_switch(conn, "TRIPPED", "three-part MEXC TP/SL installation failed")
                ls.event(conn, "MEXC_THREE_TP_INSTALL_FAILED", decision_id=decision_id,
                         severity="CRITICAL", payload=diagnostic)
                conn.execute(
                    "UPDATE mexc_canary_orders SET last_error=?,updated_at=? WHERE decision_id=?",
                    (json.dumps(diagnostic, sort_keys=True), ls.utc_now(), decision_id),
                )
                conn.commit()
            raise exc

    allowed_kinds = {"CLOSE_LIMIT_TP", "VIRTUAL_TP3_MONITOR"}
    if any(str(leg.get("order_kind") or "") not in allowed_kinds for leg in stored):
        raise MexcAPIError("legacy TP/SL leg rows cannot be trusted for live reconciliation")
    observed_orders: list[dict[str, Any]] = []
    leg_updates: list[tuple[str, str, str, int]] = []
    for leg in stored:
        if str(leg.get("order_kind") or "") == "VIRTUAL_TP3_MONITOR":
            observed_orders.append({
                "state": 1 if str(leg.get("status") or "") == "ACTIVE" else 3,
                "vol": float(leg["volume_contracts"]),
                "orderId": None,
                "virtual": True,
            })
            continue
        order_id = str(leg.get("exchange_order_id") or "")
        if not order_id:
            raise MexcAPIError("stored close-limit TP has no exchange order id")
        exchange = client.order_by_id(order_id)
        exchange.setdefault("orderId", order_id)
        exchange.setdefault("externalOid", str(leg.get("external_oid") or ""))
        state = int(exchange.get("state") or 0)
        status = "ACTIVE" if state in {1, 2} else "FILLED" if state == 3 else "TERMINAL"
        observed_orders.append(exchange)
        leg_updates.append((status, ls.utc_now(), json.dumps(exchange, sort_keys=True), int(leg["leg_index"])))
    if leg_updates:
        def _persist_leg_updates(conn):
            conn.executemany(
                "UPDATE mexc_canary_exit_legs SET status=?,updated_at=?,exchange_json=? "
                "WHERE decision_id=? AND leg_index=?",
                [
                    (status, updated_at, exchange_json, decision_id, leg_index)
                    for status, updated_at, exchange_json, leg_index in leg_updates
                ],
            )
            conn.commit()
        _reconcile_db_write(path=path, cfg=cfg, operation=_persist_leg_updates)
    active_orders = [
        item for item in observed_orders if int(item.get("state") or 0) in {1, 2}
    ]
    expected_active_volume = sum(float(item.get("vol") or 0) for item in active_orders)
    if not active_orders or abs(expected_active_volume - hold_volume) > max(volume_step * 1e-6, 1e-9):
        confirmed = _confirmed_active_exit_orders(
            client=client, local={**local, "volume_step": volume_step}, stored=stored,
            position_id=position_id, cfg=cfg,
        )
        if confirmed:
            return fallback_stop, confirmed
        def _record_degraded_tp_coverage(conn):
            ls.event_if_due(
                conn, "MEXC_TP_COVERAGE_DEGRADED", decision_id=decision_id,
                severity="WARNING", payload={
                    "reason": "active close-limit TP volume does not match holding",
                    "hold_volume": hold_volume,
                    "active_exit_volume": expected_active_volume,
                    "active_exit_orders": len(active_orders),
                    "fallback_stop_id": _tpsl_id(fallback_stop),
                    "stop_price": stop,
                    "action": "kept_position_open_because_fallback_stop_is_verified",
                }, cooldown_seconds=float(
                    cfg.get("position_reconcile_error_event_cooldown_seconds", 60)
                ),
            )
            conn.commit()
        _reconcile_db_write(path=path, cfg=cfg, operation=_record_degraded_tp_coverage)
    return fallback_stop, observed_orders


def _virtual_tp3_due(*, path: Path, decision_id: str, current_price: float,
                     direction: str) -> bool:
    with ls.connect(path) as conn:
        row = conn.execute(
            "SELECT target_price,status FROM mexc_canary_exit_legs "
            "WHERE decision_id=? AND leg_index=3 AND order_kind='VIRTUAL_TP3_MONITOR'",
            (decision_id,),
        ).fetchone()
    if not row or str(row["status"] or "") != "ACTIVE":
        return False
    target = float(row["target_price"])
    return current_price >= target if direction == "long" else current_price <= target


def _submit_virtual_tp3_close(*, path: Path, client: MexcFuturesClient, local: dict[str, Any],
                              pos: dict[str, Any], current_price: float) -> None:
    decision_id = str(local["decision_id"])
    direction = str(local.get("direction") or "long").lower()
    result = _emergency_close(
        client=client, direction=direction, symbol=local["symbol"],
        position_id=int(local["exchange_position_id"]),
        volume=float(pos.get("holdVol") or local["volume_contracts"]),
        external_oid="vtp3_" + decision_id.replace("-", "")[:27],
    )
    with ls.connect(path) as conn:
        conn.execute(
            "UPDATE mexc_canary_exit_legs SET status='SUBMITTED',updated_at=?,exchange_json=? "
            "WHERE decision_id=? AND leg_index=3 AND status='ACTIVE'",
            (ls.utc_now(), json.dumps(result, sort_keys=True), decision_id),
        )
        ls.event(conn, "MEXC_VIRTUAL_TP3_SUBMITTED", decision_id=decision_id,
                 payload={"price": current_price, "target": local["tp3"], "result": result})
        conn.commit()


def reconcile_once(*, db: str | Path | None = None, cfg: LiveCanaryConfig | None = None,
                   client: MexcFuturesClient | None = None) -> dict[str, Any]:
    cfg = cfg or load_live_canary_config()
    if not cfg.mexc_live_armed():
        return {"status": "BLOCKED_NOT_ARMED", "orders_checked": 0, "positions_checked": 0}
    path = _db_path(db)
    client = client or _client(cfg, private=True)
    stats = {"status": "OK", "orders_checked": 0, "positions_checked": 0,
             "positions_locked": 0, "filled": 0, "stops_moved": 0, "closed": 0,
             "tp_install_degraded": 0,
             "errors": []}

    with ls.connect(path) as conn:
        ls.ensure_tables(conn)
        orders = [dict(r) for r in conn.execute(
            "SELECT * FROM mexc_canary_orders WHERE venue='mexc' "
            "AND status IN ('SUBMITTED','PENDING','SUBMISSION_UNKNOWN')"
        ).fetchall()]
    for local in orders:
        stats["orders_checked"] += 1
        decision_id = local["decision_id"]
        plan = json.loads(local["plan_json"])
        # Repair rows created by the former over-broad unknown-submission
        # classifier. A parsed MEXC business rejection proves no entry order
        # existed; keeping it in reconciliation only creates permanent noise.
        if (str(local.get("status") or "") == "SUBMISSION_UNKNOWN"
                and _is_definitive_submission_rejection(
                    MexcAPIError(str(local.get("last_error") or "")))):
            def _persist_reconciliation(conn):
                conn.execute(
                    "UPDATE mexc_canary_orders SET status='REJECTED_SUBMISSION',updated_at=? "
                    "WHERE decision_id=? AND status='SUBMISSION_UNKNOWN'",
                    (ls.utc_now(), decision_id),
                )
                conn.execute(
                    "UPDATE mexc_canary_outbox SET status='REJECTED_SUBMISSION' "
                    "WHERE decision_id=? AND status='SUBMISSION_UNKNOWN'",
                    (decision_id,),
                )
                conn.execute(
                    "UPDATE mexc_canary_decisions SET state='REJECTED_SUBMISSION' "
                    "WHERE decision_id=? AND state='SUBMISSION_UNKNOWN'",
                    (decision_id,),
                )
                ls.release_risk(conn, decision_id, "reclassified definitive exchange rejection")
                ls.event(
                    conn, "SUBMISSION_UNKNOWN_RECLASSIFIED", decision_id=decision_id,
                    severity="WARNING", payload={"reason": local.get("last_error")},
                )
                conn.commit()
            _reconcile_db_write(path=path, cfg=cfg, operation=_persist_reconciliation)
            continue
        try:
            order = client.order_by_external_id(local["symbol"], local["external_oid"])
            state = int(order.get("state") or 0)
            with ls.connect(path) as conn:
                if state == 3:
                    positions = _open_positions_for_symbol(client, local["symbol"])
                    pos_id = str(order.get("positionId") or "")
                    position = next((p for p in positions if str(p.get("positionId") or "") == pos_id), None)
                    if not position:
                        raise MexcAPIError("filled order has no matching open position")
                    expected_position_type = 1 if str(plan.get("direction") or "long") == "long" else 2
                    actual_position_type = int(position.get("positionType") or expected_position_type)
                    if actual_position_type != expected_position_type:
                        _emergency_close(
                            client=client,
                            direction="long" if actual_position_type == 1 else "short",
                            symbol=local["symbol"], position_id=int(position["positionId"]),
                            volume=float(position.get("holdVol") or plan["volume_contracts"]),
                            external_oid="dir_" + str(decision_id).replace("-", "")[:27],
                        )
                        ls.set_kill_switch(conn, "TRIPPED", "MEXC filled opposite position direction")
                        conn.commit()
                        raise MexcAPIError("MEXC filled opposite position direction")
                    _upsert_filled_position(conn, decision_id=decision_id, plan=plan,
                                            order=order, position=position)
                    _insert_order(conn, decision_id=decision_id, plan=plan, status="FILLED", exchange=order)
                    stats["filled"] += 1
                elif state in {4, 5}:
                    _insert_order(conn, decision_id=decision_id, plan=plan, status="CANCELED_OR_INVALID",
                                  exchange=order)
                    ls.release_risk(conn, decision_id, "entry order canceled or invalid")
                else:
                    _insert_order(conn, decision_id=decision_id, plan=plan, status="PENDING", exchange=order)
        except Exception as exc:
            stats["errors"].append(f"order:{decision_id}:{type(exc).__name__}:{str(exc)[:160]}")

    with ls.connect(path) as conn:
        positions_local = [dict(r) for r in conn.execute(
            "SELECT p.*,o.plan_json FROM mexc_canary_positions p "
            "JOIN mexc_canary_orders o ON o.decision_id=p.decision_id "
            "WHERE p.status='OPEN' AND p.venue='mexc'"
        ).fetchall()]
    for local in positions_local:
        stats["positions_checked"] += 1
        decision_id = local["decision_id"]
        plan = json.loads(str(local["plan_json"]))
        lease_key = f"position_reconcile:{decision_id}"
        lease_owner = f"reconcile-{uuid.uuid4()}"
        lease_acquired = False
        reconcile_stage = "claim_lease"
        try:
            lease_acquired = _reconcile_db_write(
                path=path,
                cfg=cfg,
                operation=lambda conn: ls.try_claim_control_lease(
                    conn,
                    key=lease_key,
                    owner=lease_owner,
                    ttl_seconds=float(cfg.get("position_reconcile_lease_seconds", 45)),
                ),
            )
            if not lease_acquired:
                stats["positions_locked"] += 1
                continue
            reconcile_stage = "position_snapshot"
            current = _open_positions_for_symbol(client, local["symbol"])
            pos = next((p for p in current if str(p.get("positionId") or "") ==
                        str(local.get("exchange_position_id") or "")), None)
            if not pos:
                history = client.historical_positions(local["symbol"])
                closed = next((p for p in history if str(p.get("positionId") or "") ==
                               str(local.get("exchange_position_id") or "")), None)
                if not closed:
                    raise MexcAPIError("position disappeared without historical record")
                def _load_remaining_tp_ids(conn):
                    return [
                        str(row[0]) for row in conn.execute(
                            "SELECT exchange_order_id FROM mexc_canary_exit_legs "
                            "WHERE decision_id=? AND status='ACTIVE' AND exchange_order_id IS NOT NULL",
                            (decision_id,),
                        ).fetchall()
                    ]
                remaining_tp_ids = _reconcile_db_write(
                    path=path, cfg=cfg, operation=_load_remaining_tp_ids,
                )
                if remaining_tp_ids:
                    try:
                        client.cancel_order_ids(remaining_tp_ids)
                    except Exception:
                        # The position is already closed. Preserve the exchange
                        # result and retry stale-order cleanup on the next audit.
                        pass
                pnl = float(closed.get("closeProfitLoss") or 0) - abs(float(closed.get("totalFee") or 0))
                funding = float(closed.get("holdFee") or 0)
                def _persist_exchange_close(conn):
                    conn.execute(
                        "UPDATE mexc_canary_positions SET status='CLOSED',closed_at=?,updated_at=?,last_reconciled_at=?,"
                        "realized_pnl_usdt=?,fees_usdt=?,funding_usdt=?,exchange_json=? WHERE decision_id=?",
                        (ls.utc_now(), ls.utc_now(), ls.utc_now(), pnl + funding, abs(float(closed.get("totalFee") or 0)),
                         funding, json.dumps(closed, sort_keys=True), decision_id),
                    )
                    conn.execute(
                        "UPDATE mexc_canary_exit_legs SET status='TERMINAL',updated_at=? "
                        "WHERE decision_id=? AND status='ACTIVE'",
                        (ls.utc_now(), decision_id),
                    )
                    ls.release_risk(conn, decision_id, "position closed on exchange")
                _reconcile_db_write(path=path, cfg=cfg, operation=_persist_exchange_close)
                stats["closed"] += 1
                continue

            reconcile_stage = "ticker"
            ticker = client.ticker(local["symbol"])
            current_price = float(ticker.get("fairPrice") or ticker.get("lastPrice") or 0)
            if current_price <= 0:
                raise MexcAPIError("ticker has no usable price")
            direction = str(local.get("direction") or plan.get("direction") or "long").lower()
            try:
                opened_at = datetime.fromisoformat(str(local["opened_at"]).replace("Z", "+00:00"))
                favorable_candle_extreme = completed_post_entry_extreme(
                    client, local["symbol"], direction=direction, entry_at=opened_at,
                    observed_at=datetime.now(timezone.utc),
                )
            except Exception:
                # The 3-second fair-price poll remains a conservative fallback.
                favorable_candle_extreme = None
            prior_favorable = float(
                local.get("favorable_price") or local.get("highest_price") or local["entry_price"]
            )
            favorable = (
                max(prior_favorable, current_price, float(favorable_candle_extreme or 0))
                if direction == "long"
                else min(prior_favorable, current_price, float(favorable_candle_extreme or float("inf")))
            )
            stage, wanted_stop, mfe_r = model_f_stop(
                entry=float(local["entry_price"]), original_stop=float(local["original_stop"]),
                favorable_price=favorable, direction=direction, cfg=cfg)
            tick = float(plan.get("price_tick") or 0)
            wanted_stop = _round_to_step(
                wanted_stop, tick, "down" if direction == "long" else "up"
            )
            liq = float(pos.get("liquidatePrice") or 0)
            stop_distance = abs(float(local["entry_price"]) - float(local["original_stop"]))
            min_multiple = float(cfg.get("liquidation_buffer_to_stop", 3.0))
            min_extra = float(cfg.get("min_stop_to_liquidation_buffer_pct", 0.005)) * float(local["entry_price"])
            distance_to_liq = (
                float(local["entry_price"]) - liq if direction == "long" else liq - float(local["entry_price"])
            )
            stop_to_liq = (
                float(local["original_stop"]) - liq if direction == "long" else liq - float(local["original_stop"])
            )
            if liq > 0 and (distance_to_liq < min_multiple * stop_distance or stop_to_liq < min_extra):
                _emergency_close(
                    client=client, direction=direction, symbol=local["symbol"],
                    position_id=int(local["exchange_position_id"]),
                    volume=float(pos.get("holdVol") or local["volume_contracts"]),
                    external_oid="emg_" + decision_id.replace("-", "")[:27])
                with ls.connect(path) as conn:
                    ls.set_kill_switch(conn, "TRIPPED", "exchange liquidation buffer failed after fill")
                raise MexcAPIError("unsafe liquidation buffer; emergency close submitted")

            if _virtual_tp3_due(
                path=path, decision_id=decision_id, current_price=current_price, direction=direction,
            ):
                reconcile_stage = "virtual_tp3_close"
                _submit_virtual_tp3_close(
                    path=path, client=client, local=local, pos=pos, current_price=current_price,
                )
                continue

            current_stop = float(local["current_stop"])
            stop_should_move = (
                wanted_stop > current_stop + 1e-12 if direction == "long"
                else wanted_stop < current_stop - 1e-12
            )
            reconcile_stage = "exit_protection"
            if stop_should_move or _exit_leg_verification_due(path=path, local=local, cfg=cfg):
                fallback_stop, observed_exit_orders = _install_or_reconcile_exit_legs(
                    path=path, client=client, local=local, pos=pos, cfg=cfg,
                )
                if len(observed_exit_orders) < 3:
                    stats["tp_install_degraded"] += 1
                    stats["status"] = "DEGRADED"
            else:
                # Native stop and all three close-limit TPs were just verified.
                # Reuse the stored native stop id for a Model F move without
                # polling four independent MEXC protection endpoints again.
                fallback_stop = {"id": str(local["tpsl_order_id"])}
            if stop_should_move:
                reconcile_stage = "move_protective_stop"
                client.modify_tpsl(
                    stop_plan_order_id=int(_tpsl_id(fallback_stop)),
                    stop_loss=wanted_stop,
                    take_profit=None,
                )
                current_stop = wanted_stop
                stats["stops_moved"] += 1
            reconcile_stage = "persist_reconciliation"
            now = ls.utc_now()
            def _persist_reconciliation(conn):
                conn.execute(
                    "UPDATE mexc_canary_positions SET highest_price=?,favorable_price=?,max_favorable_r=?,protection_stage=?,"
                    "current_stop=?,tpsl_order_id=?,liquidation_price=?,updated_at=?,last_reconciled_at=?,"
                    "last_price_at=?,last_monitor_error_at=NULL,monitor_error_count=0,exchange_json=? "
                    "WHERE decision_id=?",
                    (favorable if direction == "long" else local.get("highest_price"), favorable, mfe_r, stage, current_stop,
                     _tpsl_id(fallback_stop), liq or None,
                     now, now, now, json.dumps(pos, sort_keys=True), decision_id),
                )
                if stop_should_move:
                    conn.execute(
                        "UPDATE mexc_canary_exit_legs SET stop_price=?,updated_at=? "
                        "WHERE decision_id=? AND status='ACTIVE'",
                        (current_stop, now, decision_id),
                    )
                if stop_should_move:
                    ls.event(conn, "MODEL_F_STOP_MOVED", decision_id=decision_id,
                             payload={"stage": stage, "stop": current_stop, "mfe_r": mfe_r})
                conn.commit()
            _reconcile_db_write(path=path, cfg=cfg, operation=_persist_reconciliation)
        except Exception as exc:
            stats["errors"].append(
                f"position:{decision_id}:{type(exc).__name__}:{str(exc)[:240]}"
            )
            try:
                def _record_reconcile_error(conn):
                    conn.execute(
                        "UPDATE mexc_canary_positions SET last_monitor_error_at=?,"
                        "monitor_error_count=monitor_error_count+1 WHERE decision_id=?",
                        (ls.utc_now(), decision_id),
                    )
                    ls.event_if_due(conn, "POSITION_RECONCILE_ERROR", decision_id=decision_id,
                             severity="CRITICAL", payload={
                                 "error_type": type(exc).__name__,
                                 "stage": reconcile_stage,
                                 "error": str(exc)[:500],
                             }, cooldown_seconds=float(
                                 cfg.get("position_reconcile_error_event_cooldown_seconds", 60)
                             ))
                    conn.commit()
                _reconcile_db_write(path=path, cfg=cfg, operation=_record_reconcile_error)
            except Exception:
                pass
        finally:
            if lease_acquired:
                try:
                    _reconcile_db_write(
                        path=path,
                        cfg=cfg,
                        operation=lambda conn: ls.release_control_lease(
                            conn, key=lease_key, owner=lease_owner,
                        ),
                    )
                except Exception:
                    pass
    if stats["errors"]:
        stats["status"] = "DEGRADED"
    return stats


def status(*, db: str | Path | None = None, cfg: LiveCanaryConfig | None = None) -> dict[str, Any]:
    cfg = cfg or load_live_canary_config()
    path = _db_path(db)
    if not path.exists():
        return {
            "execution_mode": cfg.execution_mode,
            "submission_enabled": cfg.submission_enabled,
            "live_armed": cfg.live_armed(),
            "initialized": False,
            "kill_switch": "TRIPPED",
            "pending_outbox": 0,
            "tables": {},
        }
    # Apply additive observability migrations before switching the reporting
    # connection to query-only mode. This never changes orders or positions.
    with ls.connect(path) as bootstrap:
        ls.ensure_tables(bootstrap)
    with sqlite3.connect(str(path), timeout=5.0) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA query_only=ON")
        required = {
            str(row[0]) for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'mexc_canary_%'"
            ).fetchall()
        }
        expected = {
            "mexc_canary_control", "mexc_canary_decisions", "mexc_canary_outbox",
            "mexc_canary_risk_reservations", "mexc_canary_orders",
            "mexc_canary_positions", "mexc_canary_exit_legs",
        }
        if not expected.issubset(required):
            return {
                "execution_mode": cfg.execution_mode,
                "submission_enabled": cfg.submission_enabled,
                "live_armed": cfg.live_armed(),
                "initialized": False,
                "kill_switch": "TRIPPED",
                "pending_outbox": 0,
                "tables": {},
            }
        counts = {
            table: {str(r[0]): int(r[1]) for r in conn.execute(
                f"SELECT status,COUNT(*) FROM {table} GROUP BY status").fetchall()}
            for table in ("mexc_canary_outbox", "mexc_canary_risk_reservations",
                          "mexc_canary_orders", "mexc_canary_positions", "mexc_canary_exit_legs")
        }
        decisions = {str(r[0]): int(r[1]) for r in conn.execute(
            "SELECT state,COUNT(*) FROM mexc_canary_decisions GROUP BY state").fetchall()}
        pending_outbox = int(conn.execute(
            "SELECT COUNT(*) FROM mexc_canary_outbox WHERE status IN ('QUEUED','PROCESSING')"
        ).fetchone()[0] or 0)
        active = conn.execute(
            "SELECT COALESCE(SUM(risk_usdt),0),COALESCE(SUM(margin_usdt),0),"
            "COALESCE(SUM(notional_usdt),0) FROM mexc_canary_risk_reservations "
            "WHERE status IN ('RESERVED','OPEN')").fetchone()
        venue_positions = {
            str(row[0]): int(row[1]) for row in conn.execute(
                "SELECT venue,COUNT(*) FROM mexc_canary_positions "
                "WHERE status='OPEN' GROUP BY venue"
            ).fetchall()
        }
        venue_orders = {
            str(row[0]): int(row[1]) for row in conn.execute(
                "SELECT venue,COUNT(*) FROM mexc_canary_orders GROUP BY venue"
            ).fetchall()
        }
        heartbeat = ls.monitor_heartbeat(conn)
        worker_armed_venues = {
            str(value).strip().lower()
            for value in ((heartbeat or {}).get("detail") or {}).get("armed_venues", [])
            if str(value).strip()
        }
        return {
            "execution_mode": cfg.execution_mode,
            "submission_enabled": cfg.submission_enabled,
            "live_armed": cfg.live_armed(),
            "initialized": True,
            "kill_switch": ls.kill_switch_state(conn),
            "risk_per_trade_usdt": cfg.risk_per_trade_usdt,
            "max_concurrent_risk_usdt": cfg.max_concurrent_risk_usdt,
            "active_risk_usdt": float(active[0]),
            "active_margin_usdt": float(active[1]),
            "active_notional_usdt": float(active[2]),
            "decisions": decisions,
            "pending_outbox": pending_outbox,
            "tables": counts,
            "monitor_heartbeat": heartbeat,
            "worker_armed_venues": sorted(worker_armed_venues),
            "venues": {
                "mexc": {
                    "armed": cfg.mexc_live_armed(),
                    "worker_armed": "mexc" in worker_armed_venues,
                    "credentials_present": cfg.credentials_present(),
                    "open_positions": venue_positions.get("mexc", 0),
                    "orders": venue_orders.get("mexc", 0),
                },
                "bybit": {
                    "enabled": bool(cfg.bybit_config().get("enabled", False)),
                    "armed": cfg.bybit_live_armed(),
                    "worker_armed": "bybit" in worker_armed_venues,
                    "credentials_present": cfg.bybit_credentials_present(),
                    "risk_per_trade_usdt": float(
                        cfg.bybit_config().get("fixed_risk_per_trade_usdt", cfg.risk_per_trade_usdt)
                    ),
                    "open_positions": venue_positions.get("bybit", 0),
                    "orders": venue_orders.get("bybit", 0),
                },
            },
        }


def invalidate_stale_queues(
    *, db: str | Path | None = None, cfg: LiveCanaryConfig | None = None
) -> dict[str, Any]:
    """Reject expired queued entries without clearing or bypassing the kill switch."""
    cfg = cfg or load_live_canary_config()
    path = _db_path(db)
    now = datetime.now(timezone.utc)
    invalidated: list[dict[str, Any]] = []
    with ls.connect(path) as conn:
        ls.ensure_tables(conn)
        kill_switch = ls.kill_switch_state(conn)
        rows = [dict(row) for row in conn.execute(
            "SELECT o.outbox_id,o.created_at,o.status,o.claimed_at,d.decision_id,d.captured_at,d.decision_json "
            "FROM mexc_canary_outbox o JOIN mexc_canary_decisions d "
            "ON d.decision_id=o.decision_id WHERE o.status IN ('QUEUED','PROCESSING')"
        ).fetchall()]
        for row in rows:
            decision = json.loads(str(row["decision_json"]))
            entry_mode = str(decision.get("entry_mode") or "").upper()
            limit = cfg.entry_limit(
                "max_entry_age_seconds", entry_mode, 45.0,
                mode=str(decision.get("mode") or "").lower(),
            )
            captured_at = _parse_utc(row.get("captured_at")) or _parse_utc(row.get("created_at"))
            wait_age = (
                (now - captured_at).total_seconds()
                if captured_at is not None else float("inf")
            )
            total_age = wait_age + max(0.0, float(decision.get("entry_age_seconds") or 0.0))
            if wait_age >= 0 and total_age <= limit:
                continue
            if str(row.get("status") or "").upper() == "PROCESSING":
                submitted = conn.execute(
                    "SELECT 1 FROM mexc_canary_orders WHERE decision_id=?",
                    (row["decision_id"],),
                ).fetchone()
                reserved = conn.execute(
                    "SELECT 1 FROM mexc_canary_risk_reservations "
                    "WHERE decision_id=? AND status IN ('RESERVED','OPEN')",
                    (row["decision_id"],),
                ).fetchone()
                attempted = conn.execute(
                    "SELECT 1 FROM mexc_canary_venue_attempts "
                    "WHERE decision_id=? AND stage='SUBMISSION'",
                    (row["decision_id"],),
                ).fetchone()
                if submitted or reserved or attempted:
                    continue
            diagnostic = {
                "reason": (
                    "STALE_PROCESSING_NO_EXCHANGE_FOOTPRINT"
                    if str(row.get("status") or "").upper() == "PROCESSING"
                    else "STALE_QUEUE_MAINTENANCE"
                ),
                "entry_mode": entry_mode,
                "prior_status": str(row.get("status") or ""),
                "total_entry_age_seconds": (
                    None if not math.isfinite(total_age) else round(total_age, 3)
                ),
                "max_entry_age_seconds": limit,
            }
            ls.complete_outbox(
                conn, str(row["outbox_id"]), "REJECTED_STALE_QUEUE",
                result=diagnostic, error="stale queue invalidated before live resume",
            )
            ls.event(
                conn, "STALE_QUEUE_INVALIDATED", decision_id=str(row["decision_id"]),
                severity="WARNING", payload=diagnostic,
            )
            invalidated.append({
                "decision_id": str(row["decision_id"]),
                **diagnostic,
            })
        conn.commit()
    return {
        "status": "OK",
        "kill_switch": kill_switch,
        "queued_checked": len(rows),
        "invalidated": invalidated,
    }


def set_kill_switch(*, state: str, reason: str, db: str | Path | None = None) -> dict[str, Any]:
    with ls.connect(_db_path(db)) as conn:
        ls.set_kill_switch(conn, state, reason)
        return {"kill_switch": ls.kill_switch_state(conn), "reason": reason}


def trip_kill_switch(*, reason: str, flatten: bool = False,
                     db: str | Path | None = None,
                     cfg: LiveCanaryConfig | None = None,
                     client: MexcFuturesClient | None = None) -> dict[str, Any]:
    """Trip first, then optionally flatten only positions owned by this canary."""
    cfg = cfg or load_live_canary_config()
    path = _db_path(db)
    with ls.connect(path) as conn:
        ls.set_kill_switch(conn, "TRIPPED", reason)
        owned = [dict(r) for r in conn.execute(
            "SELECT * FROM mexc_canary_positions WHERE status='OPEN'").fetchall()]
    result: dict[str, Any] = {
        "kill_switch": "TRIPPED", "reason": reason, "flatten_requested": flatten,
        "owned_open_positions": len(owned), "flatten_submitted": 0, "errors": [],
    }
    if not flatten:
        return result
    if not cfg.live_armed():
        result["flatten_status"] = "BLOCKED_NOT_ARMED"
        return result
    mexc_private = client or (_client(cfg, private=True) if cfg.mexc_live_armed() else None)
    bybit_private = make_bybit_client(cfg, private=True) if cfg.bybit_live_armed() else None
    for pos in owned:
        try:
            venue = str(pos.get("venue") or "mexc").lower()
            venue_client = bybit_private if venue == "bybit" else mexc_private
            if venue_client is None:
                raise RuntimeError(f"{venue} is not armed for flatten")
            exchange = venue_client.open_positions(pos["symbol"])
            current = next((p for p in exchange if str(p.get("positionId") or "") ==
                            str(pos.get("exchange_position_id") or "")), None)
            if not current:
                continue
            external_oid = "kill_" + str(pos["decision_id"]).replace("-", "")[:26]
            if venue == "bybit":
                venue_client.close_market(
                    symbol=pos["symbol"], direction=str(pos.get("direction") or "long"),
                    qty=float(current.get("holdVol") or pos["volume_contracts"]),
                    order_link_id=external_oid, position_idx=0,
                )
            else:
                _emergency_close(
                    client=venue_client, direction=str(pos.get("direction") or "long"),
                    symbol=pos["symbol"], position_id=int(pos["exchange_position_id"]),
                    volume=float(current.get("holdVol") or pos["volume_contracts"]),
                    external_oid=external_oid,
                )
            result["flatten_submitted"] += 1
            with ls.connect(path) as conn:
                ls.event(conn, "KILL_FLATTEN_SUBMITTED", decision_id=pos["decision_id"],
                         severity="CRITICAL", payload={"reason": reason, "venue": venue})
                conn.commit()
        except Exception as exc:
            result["errors"].append(f"{pos['decision_id']}:{type(exc).__name__}")
    result["flatten_status"] = "SUBMITTED" if not result["errors"] else "DEGRADED"
    return result
