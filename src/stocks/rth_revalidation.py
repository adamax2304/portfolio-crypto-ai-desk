"""Plan-to-RTH bridge for stocks intraday.

An intraday stock idea made while US cash equities are closed is useful as a
watchlist plan, but it is not a valid resting order.  A reviewed pre-US plan
may already have a server-side, time-bounded ``ACTIONABLE`` permission by the
cash open.  Requiring the pipeline to create a second, identical RTH signal
before acknowledging that permission made the audit falsely report legitimate
plans as missing.  This bridge records either that reviewed permission or a
separately rebuilt RTH candidate, with concrete reasons for a rejection.

It never changes a source plan, creates no signal, sends no Telegram message,
and never touches Paper/live accounting.  The MEXC Paper lane remains the only
component that can consume an actionable permission and decide whether price
actually reaches the immutable entry geometry.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from src.config import load_config
from src.stocks import load_stocks_config
from src.stocks.intraday_actionability_gates import FIRST_15M, OUTSIDE_RTH, PREMARKET, session_phase
from src.stocks.market_calendar import is_us_cash_session_open, latest_us_cash_session

VERSION = "stocks_rth_revalidation_v2"
_PLAN_MARKER = "market_closed_intraday_planning_only"
_A_B = {"A", "B"}
_DEFAULTS: dict[str, Any] = {
    "enabled": True,
    "version": VERSION,
    "min_minutes_after_open": 15,
    "max_minutes_after_open": 90,
    "finalize_grace_minutes": 180,
    "max_plan_age_hours": 20,
    "require_pre_gate_ab": True,
}
_DDL = """
CREATE TABLE IF NOT EXISTS stocks_intraday_rth_revalidations (
  plan_signal_id TEXT NOT NULL,
  session_open_at TEXT NOT NULL,
  plan_created_at TEXT NOT NULL,
  symbol TEXT NOT NULL,
  direction TEXT NOT NULL,
  plan_pre_gate_tier TEXT,
  rth_signal_id TEXT,
  rth_created_at TEXT,
  rth_tier TEXT,
  rth_score REAL,
  rth_status TEXT,
  decision TEXT NOT NULL,
  reasons_json TEXT NOT NULL,
  evaluated_at TEXT NOT NULL,
  version TEXT NOT NULL,
  PRIMARY KEY (plan_signal_id, session_open_at)
);
"""
_COLS = (
    "plan_signal_id", "session_open_at", "plan_created_at", "symbol", "direction",
    "plan_pre_gate_tier", "rth_signal_id", "rth_created_at", "decision", "reasons_json",
    "rth_tier", "rth_score", "rth_status",
    "evaluated_at", "version",
)


def load_cfg() -> dict[str, Any]:
    cfg = dict(_DEFAULTS)
    try:
        risk = load_stocks_config(load_config().root).risk
        cfg.update((risk.get("intraday_guards") or {}).get("intraday_rth_revalidation") or {})
    except Exception:
        pass
    return cfg


def ensure_tables(conn: sqlite3.Connection) -> None:
    conn.execute(_DDL)
    existing = {str(row[1]) for row in conn.execute(
        "PRAGMA table_info(stocks_intraday_rth_revalidations)"
    )}
    for name, kind in (("rth_tier", "TEXT"), ("rth_score", "REAL"), ("rth_status", "TEXT")):
        if name not in existing:
            cursor = conn.execute(
                f"ALTER TABLE stocks_intraday_rth_revalidations ADD COLUMN {name} {kind}"
            )


def _finalize_stale_awaiting(
    path: Path, *, moment: datetime, cfg: dict[str, Any]
) -> int:
    """Close legacy/non-revisited awaiting rows after their session is over.

    This repairs audit lifecycle only. It cannot create a candidate or make a
    plan actionable, and it never touches Paper accounting or signals.
    """
    changed = 0
    max_minutes = float(cfg.get("max_minutes_after_open", 90))
    grace = float(cfg.get("finalize_grace_minutes", 180))
    with sqlite3.connect(path, timeout=30.0) as conn:
        conn.row_factory = sqlite3.Row
        if conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' "
            "AND name='stocks_intraday_rth_revalidations'"
        ).fetchone() is None:
            return 0
        ensure_tables(conn)
        rows = conn.execute(
            "SELECT plan_signal_id,session_open_at,decision FROM stocks_intraday_rth_revalidations "
            "WHERE decision IN ('AWAITING_FRESH_RTH_CANDIDATE',"
            "'AWAITING_PREUS_REVIEW_OR_RTH_CANDIDATE')"
        ).fetchall()
        for row in rows:
            opened = _parse(row["session_open_at"])
            if opened is None or moment <= opened + timedelta(minutes=max_minutes + grace):
                continue
            current_decision = str(row["decision"] or "")
            terminal_decision = (
                "REJECTED_PREUS_REVIEW_OR_RTH_CANDIDATE_MISSING"
                if current_decision == "AWAITING_PREUS_REVIEW_OR_RTH_CANDIDATE"
                else "REJECTED_NO_FRESH_RTH_CANDIDATE"
            )
            cursor = conn.execute(
                "UPDATE stocks_intraday_rth_revalidations SET decision=?,reasons_json=?,"
                "evaluated_at=?,version=? WHERE plan_signal_id=? AND session_open_at=? "
                "AND decision=?",
                (terminal_decision,
                 json.dumps([
                     "awaiting state expired without an on-time actionable pre-US review "
                     "or separately rebuilt fresh RTH candidate"
                 ]),
                 moment.isoformat(), str(cfg.get("version") or VERSION),
                 row["plan_signal_id"], row["session_open_at"], current_decision),
            )
            changed += max(0, int(cursor.rowcount or 0))
        conn.commit()
    return changed


def _reconcile_mexc_preus_routes(path: Path, *, moment: datetime) -> int:
    """Correct historical generic-RTH audit rows owned by MEXC Paper.

    Earlier versions recorded ``REJECTED_NO_FRESH_RTH_CANDIDATE`` even when
    the separate pre-US MEXC Paper route had filled the same plan.  The order
    is already immutable evidence; this only replaces the contradictory audit
    label and is safe to run outside the RTH window.
    """
    with sqlite3.connect(path, timeout=30.0) as conn:
        conn.row_factory = sqlite3.Row
        if not (
            _columns(conn, "stocks_intraday_rth_revalidations")
            and {"source_signal_id", "session_date", "status"}.issubset(
                _columns(conn, "mexc_stock_futures_paper_orders")
            )
        ):
            return 0
        rows = conn.execute(
            "SELECT r.plan_signal_id,r.session_open_at,o.status "
            "FROM stocks_intraday_rth_revalidations r "
            "JOIN mexc_stock_futures_paper_orders o "
            "ON o.source_signal_id=r.plan_signal_id "
            "AND o.session_date=substr(r.session_open_at,1,10) "
            "WHERE r.decision IN ('AWAITING_FRESH_RTH_CANDIDATE',"
            "'REJECTED_NO_FRESH_RTH_CANDIDATE') "
            "AND o.status IN ('STAGED','FILLED')"
        ).fetchall()
        for row in rows:
            status = str(row["status"]).upper()
            decision = f"PREUS_MEXC_PAPER_{status}"
            conn.execute(
                "UPDATE stocks_intraday_rth_revalidations "
                "SET decision=?,reasons_json=?,evaluated_at=?,version=? "
                "WHERE plan_signal_id=? AND session_open_at=?",
                (
                    decision,
                    json.dumps([
                        "pre-US MEXC Paper route owns this plan; generic RTH audit is not a second route"
                    ]),
                    moment.isoformat(),
                    VERSION,
                    row["plan_signal_id"],
                    row["session_open_at"],
                ),
            )
        conn.commit()
    return len(rows)


def _reconcile_ineligible_pre_gate_rows(
    path: Path, *, moment: datetime, cfg: dict[str, Any],
) -> int:
    """Label historical C pre-gate plans as excluded, not failed RTH hand-offs."""
    if not cfg.get("require_pre_gate_ab", True):
        return 0
    with sqlite3.connect(path, timeout=30.0) as conn:
        if not _columns(conn, "stocks_intraday_rth_revalidations"):
            return 0
        cursor = conn.execute(
            "UPDATE stocks_intraday_rth_revalidations "
            "SET decision=?,reasons_json=?,evaluated_at=?,version=? "
            "WHERE decision IN ('AWAITING_FRESH_RTH_CANDIDATE',"
            "'REJECTED_NO_FRESH_RTH_CANDIDATE') "
            "AND COALESCE(plan_pre_gate_tier,'') NOT IN ('A','B')",
            (
                "EXCLUDED_PRE_GATE_NOT_AB",
                json.dumps([
                    "pre-open plan was not A/B before the RTH bridge; no fresh-RTH confirmation was required"
                ]),
                moment.isoformat(),
                str(cfg.get("version") or VERSION),
            ),
        )
        conn.commit()
    return max(0, int(cursor.rowcount or 0))


def _parse(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return None


def _json(value: Any) -> dict[str, Any]:
    try:
        decoded = json.loads(value or "{}")
        return decoded if isinstance(decoded, dict) else {}
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}


def _cap_reasons(row: dict[str, Any]) -> list[str]:
    raw = _json(row.get("raw_idea_json"))
    values = raw.get("cap_reasons") or []
    return [str(value) for value in values if value]


def _plan_pre_gate_tier(row: dict[str, Any]) -> str:
    return str(_json(row.get("raw_idea_json")).get("pre_gate_tier") or "").upper()


def _is_planning_row(row: dict[str, Any], cfg: dict[str, Any]) -> bool:
    if _PLAN_MARKER not in " ".join(_cap_reasons(row)):
        return False
    return (not cfg.get("require_pre_gate_ab", True)
            or _plan_pre_gate_tier(row) in _A_B)


def _window(now: datetime, cfg: dict[str, Any]) -> tuple[datetime, datetime, bool] | None:
    phase = session_phase(now)
    if phase in {PREMARKET, FIRST_15M}:
        return None
    opened_at, _closed_at, _complete = latest_us_cash_session(now)
    elapsed = (now - opened_at).total_seconds() / 60.0
    if elapsed < float(cfg.get("min_minutes_after_open", 15)):
        return None
    max_minutes = float(cfg.get("max_minutes_after_open", 90))
    grace = float(cfg.get("finalize_grace_minutes", 180))
    if not is_us_cash_session_open(now) and now > _closed_at + timedelta(minutes=grace):
        return None
    finalizing = elapsed > max_minutes
    candidate_until = min(now, opened_at + timedelta(minutes=max_minutes))
    return opened_at, candidate_until, finalizing


def _columns(conn: sqlite3.Connection, table: str) -> set[str]:
    try:
        return {str(row[1]) for row in conn.execute(f"PRAGMA table_info({table})")}
    except sqlite3.DatabaseError:
        return set()


def _load_stock_rows(conn: sqlite3.Connection, *, since: datetime, until: datetime) -> list[dict[str, Any]]:
    proposed_columns = _columns(conn, "proposed_signals")
    updated_expr = "updated_at" if "updated_at" in proposed_columns else "NULL AS updated_at"
    rows = conn.execute(
        f"SELECT signal_id, created_at, {updated_expr}, symbol, direction, tier, score, status, raw_idea_json "
        "FROM proposed_signals WHERE asset_class='stocks' AND mode='intraday' "
        "AND created_at >= ? AND created_at <= ? ORDER BY created_at ASC",
        (since.isoformat(), until.isoformat()),
    ).fetchall()
    return [dict(row) for row in rows]


def _load_snapshot_plans(
    conn: sqlite3.Connection,
    *,
    since: datetime,
    session_open: datetime,
) -> list[dict[str, Any]]:
    """Load the immutable pre-open decision when the funnel table is present."""
    columns = _columns(conn, "stocks_paper_decision_snapshots")
    required = {
        "signal_id", "signal_created_at", "symbol", "direction",
        "pre_gate_tier", "funnel_state", "snapshot_json",
    }
    if not required.issubset(columns):
        return []
    target_filter = ""
    params: list[str] = [since.isoformat(), session_open.isoformat()]
    if "target_session_open_at" in columns:
        target_filter = " AND (target_session_open_at IS NULL OR target_session_open_at=?)"
        params.append(session_open.isoformat())
    rows = conn.execute(
        "SELECT signal_id,signal_created_at,symbol,direction,pre_gate_tier,snapshot_json "
        "FROM stocks_paper_decision_snapshots "
        "WHERE funnel_state='PREOPEN_PLAN' AND signal_created_at>=? "
        "AND signal_created_at<?" + target_filter,
        tuple(params),
    ).fetchall()
    plans: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        snapshot = _json(item.get("snapshot_json"))
        snapshot["pre_gate_tier"] = (
            item.get("pre_gate_tier") or snapshot.get("pre_gate_tier")
        )
        plans.append({
            "signal_id": item.get("signal_id"),
            "created_at": item.get("signal_created_at"),
            "symbol": item.get("symbol"),
            "direction": item.get("direction"),
            "raw_idea_json": json.dumps(snapshot, sort_keys=True),
        })
    return plans


def _load_rth_observations(
    conn: sqlite3.Connection, *, session_open: datetime, until: datetime,
) -> list[dict[str, Any]]:
    columns = _columns(conn, "stocks_paper_candidate_observations")
    required = {
        "signal_id", "observed_at", "signal_created_at", "symbol", "direction",
        "tier", "score", "status", "cap_reasons_json", "snapshot_json",
    }
    if not required.issubset(columns):
        return []
    rows = conn.execute(
        "SELECT signal_id,observed_at,signal_created_at,symbol,direction,tier,score,status,"
        "cap_reasons_json,snapshot_json FROM stocks_paper_candidate_observations "
        "WHERE observed_at>=? AND observed_at<=? ORDER BY observed_at ASC,observation_id ASC",
        (session_open.isoformat(), until.isoformat()),
    ).fetchall()
    out: list[dict[str, Any]] = []
    for raw in rows:
        row = dict(raw)
        snapshot = _json(row.get("snapshot_json"))
        snapshot["cap_reasons"] = json.loads(row.get("cap_reasons_json") or "[]")
        out.append({
            "signal_id": row.get("signal_id"),
            "created_at": row.get("signal_created_at"),
            "rth_observed_at": row.get("observed_at"),
            "symbol": row.get("symbol"),
            "direction": row.get("direction"),
            "tier": row.get("tier"),
            "score": row.get("score"),
            "status": row.get("status"),
            "raw_idea_json": json.dumps(snapshot, sort_keys=True),
        })
    return out


def _load_mexc_preus_route_statuses(
    conn: sqlite3.Connection, *, session_open: datetime,
) -> dict[str, str]:
    """Return non-terminal MEXC pre-US routing evidence for this session.

    The MEXC stock-futures Paper lane is an independent route for a reviewed
    pre-US permission.  Its source plan must not later be reported as rejected
    merely because the generic cash-RTH revalidation did not build another
    candidate for the same idea.  This helper is audit-only: it reads a route
    decision already made by that lane and never changes its order.
    """
    required = {"source_signal_id", "session_date", "status"}
    if not required.issubset(_columns(conn, "mexc_stock_futures_paper_orders")):
        return {}
    session_date = session_open.date().isoformat()
    rows = conn.execute(
        "SELECT source_signal_id,status FROM mexc_stock_futures_paper_orders "
        "WHERE session_date=? AND status IN ('STAGED','FILLED')",
        (session_date,),
    ).fetchall()
    return {
        str(row["source_signal_id"]): str(row["status"]).upper()
        for row in rows if row["source_signal_id"]
    }


def _load_preus_actionability(
    conn: sqlite3.Connection, *, session_open: datetime,
) -> dict[str, dict[str, Any]]:
    """Return the immutable-review permission for the target cash session.

    This is intentionally only an audit read.  ``stocks_preus_review`` owns
    the server-side score clamp, hard gates, expiry and source fingerprint;
    this module must never reproduce or relax those checks.
    """
    required = {
        "signal_id", "target_session_open_at", "decision", "effective_tier",
        "effective_score", "reason_codes_json", "evaluated_at", "valid_until",
    }
    if not required.issubset(_columns(conn, "stocks_preus_actionability")):
        return {}
    rows = conn.execute(
        "SELECT signal_id,target_session_open_at,decision,effective_tier,effective_score,"
        "reason_codes_json,evaluated_at,valid_until FROM stocks_preus_actionability "
        "WHERE substr(target_session_open_at,1,10)=?",
        (session_open.date().isoformat(),),
    ).fetchall()
    return {str(row["signal_id"]): dict(row) for row in rows if row["signal_id"]}


def _store(conn: sqlite3.Connection, row: dict[str, Any]) -> bool:
    previous = conn.execute(
        "SELECT decision,rth_signal_id FROM stocks_intraday_rth_revalidations "
        "WHERE plan_signal_id=? AND session_open_at=?",
        (row["plan_signal_id"], row["session_open_at"]),
    ).fetchone()
    placeholders = ", ".join("?" for _ in _COLS)
    updates = ", ".join(f"{column}=excluded.{column}" for column in _COLS if column not in {
        "plan_signal_id", "session_open_at", "plan_created_at", "symbol", "direction", "plan_pre_gate_tier",
    })
    conn.execute(
        f"INSERT INTO stocks_intraday_rth_revalidations ({', '.join(_COLS)}) VALUES ({placeholders}) "
        f"ON CONFLICT(plan_signal_id, session_open_at) DO UPDATE SET {updates}",
        tuple(row[column] for column in _COLS),
    )
    return previous is None or tuple(previous) != (row["decision"], row.get("rth_signal_id"))


def refresh(*, db: str | Path | None = None, now: datetime | None = None,
            cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    """Write audit-only revalidation for eligible premarket plans.

    A pre-US ``ACTIONABLE`` permission is a current-session, server-validated
    review of the *same* plan.  It is therefore valid evidence in this audit
    bridge.  A fresh independently rebuilt RTH candidate remains an alternative
    route; neither path changes the immutable plan or submits an order here.
    """
    cfg = {**load_cfg(), **(cfg or {})}
    moment = now or datetime.now(timezone.utc)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    if not cfg.get("enabled", True):
        return {"status": "disabled", "plans": 0, "ready": 0, "rejected": 0, "rows": []}
    path = Path(db or load_config().db_path)
    finalized_stale = _finalize_stale_awaiting(path, moment=moment, cfg=cfg)
    reconciled_mexc = _reconcile_mexc_preus_routes(path, moment=moment)
    reconciled_pre_gate = _reconcile_ineligible_pre_gate_rows(
        path, moment=moment, cfg=cfg,
    )
    session = _window(moment, cfg)
    if session is None:
        return {"status": "outside_revalidation_window", "plans": 0, "ready": 0,
                "rejected": 0, "finalized_stale": finalized_stale,
                "mexc_reconciled": reconciled_mexc,
                "pre_gate_reconciled": reconciled_pre_gate, "rows": []}
    session_open, session_now, finalizing = session
    with sqlite3.connect(path, timeout=30.0) as conn:
        conn.row_factory = sqlite3.Row
        ensure_tables(conn)
        max_age = timedelta(hours=float(cfg.get("max_plan_age_hours", 20)))
        all_rows = _load_stock_rows(conn, since=moment - max_age, until=session_now)
        snapshot_plans = _load_snapshot_plans(
            conn,
            since=moment - max_age,
            session_open=session_open,
        )
        plans = snapshot_plans
        if cfg.get("require_pre_gate_ab", True):
            plans = [plan for plan in plans if _plan_pre_gate_tier(plan) in _A_B]
        # A snapshot is the immutable decision record. Do not fall back to a
        # mutable source row merely because every snapshot plan was C-tier.
        if not snapshot_plans:
            plans = [row for row in all_rows if _is_planning_row(row, cfg)
                     and (_parse(row.get("created_at")) or moment) < session_open]
        latest_rth: dict[tuple[str, str], dict[str, Any]] = {}
        observations = _load_rth_observations(
            conn, session_open=session_open, until=session_now
        )
        mexc_preus_routes = _load_mexc_preus_route_statuses(
            conn, session_open=session_open,
        )
        preus_actionability = _load_preus_actionability(
            conn, session_open=session_open,
        )
        if observations:
            for row in observations:
                if _is_planning_row(row, cfg):
                    continue
                latest_rth[(str(row.get("symbol") or "").upper(),
                            str(row.get("direction") or "").lower())] = row
        else:
            for row in all_rows:
                created = _parse(row.get("created_at"))
                updated = _parse(row.get("updated_at"))
                observed = max(value for value in (created, updated) if value is not None) \
                    if created is not None or updated is not None else None
                if (observed is None or observed < session_open or observed > session_now
                        or _is_planning_row(row, cfg)):
                    continue
                row["rth_observed_at"] = observed.isoformat()
                latest_rth[(str(row.get("symbol") or "").upper(),
                            str(row.get("direction") or "").lower())] = row

        decisions: list[dict[str, Any]] = []
        for plan in plans:
            key = (str(plan.get("symbol") or "").upper(), str(plan.get("direction") or "").lower())
            fresh = latest_rth.get(key)
            mexc_status = mexc_preus_routes.get(str(plan.get("signal_id") or ""))
            preus = preus_actionability.get(str(plan.get("signal_id") or ""))
            if mexc_status == "FILLED":
                decision = "PREUS_MEXC_PAPER_FILLED"
                reasons = [
                    "pre-US MEXC Paper route filled; generic RTH revalidation is not a second route"
                ]
            elif mexc_status == "STAGED":
                decision = "PREUS_MEXC_PAPER_STAGED"
                reasons = [
                    "pre-US MEXC Paper route staged; generic RTH revalidation is not a second route"
                ]
            elif preus and str(preus.get("decision") or "").upper() == "ACTIONABLE":
                decision = "READY_FOR_PREUS_ACTIONABILITY_TRACKER"
                reasons = [
                    "same-plan pre-US structured review is actionable; MEXC Paper owns price/geometry validation"
                ]
            elif fresh is not None and str(fresh.get("tier") or "").upper() in _A_B:
                decision = "READY_FOR_EXISTING_PAPER_TRACKER"
                reasons = ["fresh_rth_ab_candidate", *(_cap_reasons(fresh) or [])]
            elif preus:
                decision = "REJECTED_PREUS_ACTIONABILITY"
                try:
                    reasons = json.loads(preus.get("reason_codes_json") or "[]")
                except (TypeError, ValueError, json.JSONDecodeError):
                    reasons = []
                reasons = [str(reason) for reason in reasons if reason] or [
                    "pre-US structured review did not materialize an actionable permission"
                ]
            elif fresh is None:
                decision = (
                    "REJECTED_PREUS_REVIEW_OR_RTH_CANDIDATE_MISSING"
                    if finalizing else "AWAITING_PREUS_REVIEW_OR_RTH_CANDIDATE"
                )
                reasons = [
                    "neither an on-time actionable pre-US review nor a separately rebuilt current-session candidate was recorded"
                    if finalizing else "awaiting on-time pre-US review permission or separately rebuilt current-session candidate"
                ]
            else:
                decision = "REJECTED_BY_FRESH_GATES"
                reasons = _cap_reasons(fresh) or ["fresh RTH candidate is not A/B"]
            stored = {
                "plan_signal_id": str(plan.get("signal_id") or ""),
                "session_open_at": session_open.isoformat(),
                "plan_created_at": str(plan.get("created_at") or ""),
                "symbol": key[0],
                "direction": key[1],
                "plan_pre_gate_tier": _plan_pre_gate_tier(plan) or None,
                "rth_signal_id": str(fresh.get("signal_id") or "") if fresh else (
                    str(plan.get("signal_id") or "") if preus else None
                ),
                "rth_created_at": str(
                    fresh.get("rth_observed_at") or fresh.get("created_at") or ""
                ) if fresh else (str(preus.get("evaluated_at") or "") if preus else None),
                "rth_tier": str(fresh.get("tier") or "").upper() if fresh else (
                    str(preus.get("effective_tier") or "").upper() if preus else None
                ),
                "rth_score": float(fresh.get("score") or 0.0) if fresh else (
                    float(preus.get("effective_score") or 0.0) if preus else None
                ),
                "rth_status": str(fresh.get("status") or "") if fresh else (
                    str(preus.get("decision") or "") if preus else None
                ),
                "decision": decision,
                "reasons_json": json.dumps(reasons, sort_keys=True),
                "evaluated_at": moment.isoformat(),
                "version": str(cfg.get("version") or VERSION),
            }
            changed = _store(conn, stored)
            if changed:
                try:
                    from src.stocks.paper_funnel import record_event

                    record_event(
                        conn,
                        signal_id=stored["plan_signal_id"],
                        stage=f"RTH_{decision}",
                        reason=(reasons[0] if reasons else decision),
                        payload={
                            "session_open_at": stored["session_open_at"],
                            "rth_signal_id": stored.get("rth_signal_id"),
                            "rth_tier": stored.get("rth_tier"),
                            "rth_score": stored.get("rth_score"),
                            "rth_status": stored.get("rth_status"),
                            "revalidation_version": stored["version"],
                        },
                        now=moment,
                    )
                except Exception:
                    pass
            # Audit-only rows need not form one large transaction. Releasing
            # after each plan keeps the execution observer responsive.
            conn.commit()
            decisions.append(stored)
        conn.commit()
    return {
        "status": "ok", "session_open_at": session_open.isoformat(), "plans": len(plans),
        "ready": sum(row["decision"] in {
            "READY_FOR_EXISTING_PAPER_TRACKER", "READY_FOR_PREUS_ACTIONABILITY_TRACKER",
        } for row in decisions),
        "preus_actionable": sum(
            row["decision"] == "READY_FOR_PREUS_ACTIONABILITY_TRACKER" for row in decisions
        ),
        "mexc_handled": sum(row["decision"].startswith("PREUS_MEXC_PAPER_") for row in decisions),
        "rejected": sum(row["decision"].startswith("REJECTED_") for row in decisions),
        "awaiting": sum(row["decision"] in {
            "AWAITING_FRESH_RTH_CANDIDATE", "AWAITING_PREUS_REVIEW_OR_RTH_CANDIDATE",
        } for row in decisions),
        "finalized_stale": finalized_stale,
        "mexc_reconciled": reconciled_mexc,
        "pre_gate_reconciled": reconciled_pre_gate,
        "finalizing": finalizing,
        "rows": decisions,
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = ["# Stocks Intraday RTH Revalidation", "",
             "Outside-session plans are never orders. A same-plan, server-validated pre-US ACTIONABLE permission or a separately rebuilt RTH A/B candidate can enter the existing Paper tracker.", "",
             f"- status: `{result.get('status')}`",
              f"- plans considered: `{result.get('plans', 0)}`",
              f"- ready Paper paths: `{result.get('ready', 0)}`",
              f"- ready via same-plan pre-US review: `{result.get('preus_actionable', 0)}`",
             f"- handled by pre-US MEXC Paper route: `{result.get('mexc_handled', 0)}`",
             f"- rejected by fresh gates: `{result.get('rejected', 0)}`"]
    rows = result.get("rows") or []
    if rows:
        lines.extend(["", "| plan | symbol | direction | result | fresh RTH signal |", "|---|---|---|---|---|"])
        for row in rows:
            lines.append("| {plan_signal_id} | {symbol} | {direction} | {decision} | {rth_signal_id} |".format(**{
                **row, "rth_signal_id": row.get("rth_signal_id") or "-",
            }))
    return "\n".join(lines) + "\n"


__all__ = ["VERSION", "ensure_tables", "load_cfg", "refresh", "render_markdown"]
