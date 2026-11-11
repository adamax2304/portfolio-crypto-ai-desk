"""Authoritative, read-only Paper operational audit.

Combines USD accounting, evidence quality, routing, latency, overlay actions,
and the stocks pre-open funnel.  It deliberately does not infer edge from R
or from historical/backfilled rows.
"""
from __future__ import annotations

import json
import math
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

from src.config import load_config
from src.execution.paper_portfolio import load_cfg as load_portfolio_cfg

VERSION = "paper_operational_audit_v2"


def _utc(value: datetime | None = None) -> datetime:
    moment = value or datetime.now(timezone.utc)
    return moment.replace(tzinfo=timezone.utc) if moment.tzinfo is None else moment.astimezone(timezone.utc)


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
    ).fetchone() is not None


def _json(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    try:
        parsed = json.loads(value or "{}")
        return parsed if isinstance(parsed, dict) else {}
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}


def _safe_ratio(numerator: float, denominator: float) -> float | None:
    if denominator <= 0:
        return None
    return round(numerator / denominator, 3)


def _drawdown(values: Iterable[float]) -> float:
    cumulative = peak = worst = 0.0
    for value in values:
        cumulative += float(value or 0.0)
        peak = max(peak, cumulative)
        worst = max(worst, peak - cumulative)
    return round(worst, 2)


def _trade_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    pnls = [float(row.get("net_pnl_usdt") or 0.0) for row in rows]
    wins = [value for value in pnls if value > 0]
    losses = [value for value in pnls if value < 0]
    positive = sum(wins)
    total = sum(pnls)
    ranked = sorted((abs(value) for value in pnls), reverse=True)
    return {
        "closed": len(rows),
        "net_pnl_usdt": round(total, 2),
        "gross_pnl_usdt": round(sum(float(row.get("gross_pnl_usdt") or 0.0) for row in rows), 2),
        "fees_usdt": round(sum(float(row.get("fees_usdt") or 0.0) for row in rows), 2),
        "slippage_usdt": round(sum(float(row.get("slippage_usdt") or 0.0) for row in rows), 2),
        "funding_usdt": round(sum(float(row.get("funding_usdt") or 0.0) for row in rows), 2),
        "winrate": round(len(wins) / len(rows), 3) if rows else None,
        "profit_factor": round(positive / abs(sum(losses)), 3) if losses else (math.inf if wins else None),
        "max_drawdown_usdt": _drawdown(pnls),
        "top1_abs_pnl_share": _safe_ratio(sum(ranked[:1]), sum(ranked)),
        "top3_abs_pnl_share": _safe_ratio(sum(ranked[:3]), sum(ranked)),
        "top1_positive_pnl_share": _safe_ratio(max(wins, default=0.0), positive),
        "top3_positive_pnl_share": _safe_ratio(sum(sorted(wins, reverse=True)[:3]), positive),
    }


def _authoritative_ledger(conn: sqlite3.Connection, *, cutoff: datetime) -> list[dict[str, Any]]:
    if not (_table_exists(conn, "paper_portfolio_ledger") and _table_exists(conn, "proposed_signals")):
        return []
    cfg = load_portfolio_cfg()
    crypto_profile = str(cfg.get("fee_profile") or "bybit_non_vip_usdt_perp")
    stock_profile = str(cfg.get("stock_futures_fee_profile") or "mexc_default_futures")
    rows = conn.execute(
        "SELECT l.*,p.asset_class,p.mode,p.direction,p.symbol,p.tier,p.score,p.setup_type "
        "FROM paper_portfolio_ledger l JOIN proposed_signals p ON p.signal_id=l.signal_id "
        "WHERE lower(l.event_type)='exit' AND COALESCE(l.exit_at,l.timestamp)>=? "
        "AND ((p.asset_class='stocks' AND l.fee_profile=?) "
        "OR (p.asset_class!='stocks' AND l.fee_profile=?)) "
        "ORDER BY COALESCE(l.exit_at,l.timestamp),l.id",
        (cutoff.isoformat(), stock_profile, crypto_profile),
    ).fetchall()
    return [dict(row) for row in rows]


def _evidence(conn: sqlite3.Connection, *, cutoff: datetime) -> list[dict[str, Any]]:
    if not (_table_exists(conn, "paper_execution_outcomes") and _table_exists(conn, "proposed_signals")):
        return []
    rows = conn.execute(
        "SELECT p.asset_class,p.mode,p.direction,o.evidence_class,o.execution_validity," 
        "o.lifecycle_state,o.paper_execution_outcome,o.entry_at,o.exit_at "
        "FROM paper_execution_outcomes o JOIN proposed_signals p ON p.signal_id=o.signal_id "
        "WHERE COALESCE(o.decision_at,o.entry_at,o.computed_at)>=?",
        (cutoff.isoformat(),),
    ).fetchall()
    groups: dict[tuple[str, str, str], Counter[str]] = defaultdict(Counter)
    for raw in rows:
        row = dict(raw)
        key = (str(row.get("asset_class") or "?"), str(row.get("mode") or "?"),
               str(row.get("direction") or "?"))
        evidence_class = str(row.get("evidence_class") or "unclassified").lower()
        validity = str(row.get("execution_validity") or "").lower()
        lifecycle = str(row.get("lifecycle_state") or "").lower()
        closed = bool(row.get("exit_at")) or lifecycle in {"closed", "resolved", "terminal"}
        forward = evidence_class == "forward_postfreeze"
        clean = validity in {"valid", "clean", "point_in_time"} or (
            not validity and evidence_class == "forward_postfreeze"
        )
        bucket = "open_or_unresolved"
        if closed and forward and clean:
            bucket = "forward_clean_closed"
        elif closed and forward:
            bucket = "forward_dirty_closed"
        elif closed:
            bucket = "historical_or_unclassified_closed"
        groups[key][bucket] += 1
    return [
        {"asset_class": key[0], "mode": key[1], "direction": key[2], **dict(counts)}
        for key, counts in sorted(groups.items())
    ]


def _overlay(conn: sqlite3.Connection, *, cutoff: datetime) -> list[dict[str, Any]]:
    if not _table_exists(conn, "crypto_quality_overlay_decisions"):
        return []
    rows = conn.execute(
        "SELECT signal_id,mode,quality_action,quality_reasons_json,computed_at FROM "
        "crypto_quality_overlay_decisions WHERE computed_at>=? ORDER BY computed_at",
        (cutoff.isoformat(),),
    ).fetchall()
    latest: dict[str, dict[str, Any]] = {}
    for raw in rows:
        row = dict(raw)
        latest[str(row.get("signal_id") or "")] = row
    by_mode: dict[str, Counter[str]] = defaultdict(Counter)
    reasons: dict[str, Counter[str]] = defaultdict(Counter)
    for row in latest.values():
        mode = str(row.get("mode") or "?")
        by_mode[mode][str(row.get("quality_action") or "UNKNOWN")] += 1
        try:
            values = json.loads(row.get("quality_reasons_json") or "[]")
        except (TypeError, ValueError, json.JSONDecodeError):
            values = []
        for reason in values if isinstance(values, list) else []:
            reasons[mode][str(reason)] += 1
    return [
        {"mode": mode, "unique_signals": sum(actions.values()), "actions": dict(actions),
         "top_reasons": reasons[mode].most_common(10)}
        for mode, actions in sorted(by_mode.items())
    ]


def _alerts(conn: sqlite3.Connection, *, cutoff: datetime) -> list[dict[str, Any]]:
    if not _table_exists(conn, "signal_alerts"):
        return []
    rows = conn.execute(
        "SELECT asset_class,mode,telegram_status,payload_json FROM signal_alerts "
        "WHERE alert_type='paper_entry' AND sent_at>=?", (cutoff.isoformat(),)
    ).fetchall()
    groups: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    reasons: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    sizing: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    overlay_actions: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    guard_actions: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for raw in rows:
        row = dict(raw)
        key = (str(row.get("asset_class") or "?"), str(row.get("mode") or "?"))
        groups[key][str(row.get("telegram_status") or "UNKNOWN")] += 1
        payload = _json(row.get("payload_json"))
        weight = payload.get("size_weight")
        sizing[key]["unknown" if weight is None else str(round(float(weight), 3))] += 1
        overlay_actions[key][str(payload.get("cqo_effective_paper_action") or "UNKNOWN")] += 1
        guard_actions[key][str(payload.get("paper_risk_floor_action") or "NO_GUARD_ACTION")] += 1
        if payload.get("current_price_revalidated") is not True:
            reasons[key]["CURRENT_PRICE_NOT_REVALIDATED"] += 1
        basis = str(payload.get("entry_time_basis") or "")
        if basis and basis != "point_in_time_current_bar":
            reasons[key]["ENTRY_NOT_POINT_IN_TIME"] += 1
        for reason in payload.get("cqo_reasons") or []:
            reasons[key][str(reason)] += 1
        for reason in payload.get("paper_decision_reason_codes") or []:
            reasons[key][str(reason)] += 1
        if payload.get("paper_risk_floor_reason"):
            reasons[key][str(payload["paper_risk_floor_reason"])] += 1
    return [
        {"asset_class": key[0], "mode": key[1], "routes": dict(statuses),
         "size_weights": dict(sizing[key]), "overlay_actions": dict(overlay_actions[key]),
         "guard_actions": dict(guard_actions[key]), "top_reasons": reasons[key].most_common(10)}
        for key, statuses in sorted(groups.items())
    ]


def _mexc_handoff(conn: sqlite3.Connection, *, cutoff: datetime) -> dict[str, Any]:
    result: dict[str, Any] = {
        "decisions": {}, "eligible": {}, "rejection_reasons": [], "outbox": {},
        "positions": {}, "open_risk_usdt": 0.0, "parity": [],
        "venue_attempts": {}, "venue_rejections": [],
    }
    if _table_exists(conn, "mexc_canary_decisions"):
        rows = conn.execute(
            "SELECT eligible,state,rejection_reasons_json FROM mexc_canary_decisions "
            "WHERE captured_at>=?", (cutoff.isoformat(),)
        ).fetchall()
        states: Counter[str] = Counter()
        eligibility: Counter[str] = Counter()
        reasons: Counter[str] = Counter()
        for row in rows:
            states[str(row["state"] or "UNKNOWN")] += 1
            eligibility["eligible" if int(row["eligible"] or 0) else "ineligible"] += 1
            try:
                values = json.loads(row["rejection_reasons_json"] or "[]")
            except (TypeError, ValueError, json.JSONDecodeError):
                values = []
            for reason in values if isinstance(values, list) else []:
                reasons[str(reason)] += 1
        result["decisions"] = dict(states)
        result["eligible"] = dict(eligibility)
        result["rejection_reasons"] = reasons.most_common(15)
    if _table_exists(conn, "mexc_canary_venue_attempts"):
        rows = conn.execute(
            "SELECT venue,stage,status,reason FROM mexc_canary_venue_attempts "
            "WHERE attempted_at>=?", (cutoff.isoformat(),)
        ).fetchall()
        attempts: Counter[str] = Counter()
        venue_reasons: Counter[str] = Counter()
        for row in rows:
            venue = str(row[0] or "unknown").lower()
            stage = str(row[1] or "UNKNOWN").upper()
            status = str(row[2] or "UNKNOWN").upper()
            attempts[f"{venue}:{stage}:{status}"] += 1
            if status == "REJECTED":
                venue_reasons[f"{venue}:{str(row[3] or 'unknown')}"] += 1
        result["venue_attempts"] = dict(attempts)
        result["venue_rejections"] = venue_reasons.most_common(15)
    if _table_exists(conn, "mexc_canary_outbox") and _table_exists(conn, "mexc_canary_decisions"):
        rows = conn.execute(
            "SELECT o.status,COUNT(*) n FROM mexc_canary_outbox o "
            "JOIN mexc_canary_decisions d ON d.decision_id=o.decision_id "
            "WHERE d.captured_at>=? GROUP BY o.status", (cutoff.isoformat(),)
        ).fetchall()
        result["outbox"] = {str(row["status"]): int(row["n"]) for row in rows}
    if _table_exists(conn, "mexc_canary_positions"):
        rows = conn.execute(
            "SELECT status,COUNT(*) n FROM mexc_canary_positions GROUP BY status"
        ).fetchall()
        result["positions"] = {str(row["status"]): int(row["n"]) for row in rows}
        result["open_risk_usdt"] = round(float(conn.execute(
            "SELECT COALESCE(SUM(risk_usdt),0) FROM mexc_canary_positions WHERE status='OPEN'"
        ).fetchone()[0] or 0.0), 2)
    if _table_exists(conn, "mexc_canary_parity_outcomes"):
        rows = conn.execute(
            "SELECT profile_id,net_pnl_usdt,gross_pnl_usdt,fees_usdt,slippage_usdt,funding_usdt "
            "FROM mexc_canary_parity_outcomes WHERE updated_at>=? AND closed=1 AND clean=1 "
            "AND evidence_class='forward_post_activation' ORDER BY close_at,updated_at",
            (cutoff.isoformat(),),
        ).fetchall()
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            grouped[str(row["profile_id"] or "?")].append(dict(row))
        result["parity"] = [
            {"profile_id": profile, **_trade_metrics(values)}
            for profile, values in sorted(grouped.items())
        ]
    return result


def _news_quality(path: Path) -> dict[str, Any]:
    """Read the scheduler-produced verdict only for the configured production DB."""
    cfg = load_config()
    try:
        if path.resolve() != Path(cfg.db_path).resolve():
            return {"status": "NOT_EVALUATED_FOR_NON_PRODUCTION_DB"}
    except OSError:
        return {"status": "NOT_EVALUATED"}
    diagnostic = Path(cfg.root) / "data" / "diagnostics" / "news_quality_gate.json"
    try:
        payload = json.loads(diagnostic.read_text(encoding="utf-8"))
    except (OSError, TypeError, ValueError, json.JSONDecodeError):
        return {"status": "MISSING"}
    replay = payload.get("production_replay") or {}
    latency = replay.get("resolution_latency_seconds") or {}
    return {
        "status": "READY" if payload.get("ready") else "NOT_READY",
        "generated_at": payload.get("generated_at"),
        "reasons": payload.get("reasons") or [],
        "resolution_p95_seconds": latency.get("p95"),
        "source_error": replay.get("source_error", 0),
        "source_dead": replay.get("source_dead", 0),
        "source_stale": replay.get("source_stale", 0),
        "unmapped_impact": replay.get("unmapped_impact", 0),
        "resolver_pending_persist": replay.get("resolver_pending_persist", 0),
    }


def _latency(path: Path, *, recent_days: int) -> dict[str, Any]:
    try:
        from src.signals.latency_sla import sla_report

        report = sla_report(str(path), recent_days=recent_days)
    except Exception as exc:
        return {"available": False, "error": type(exc).__name__}
    return {
        "available": bool(report.get("available")),
        "acceptance": report.get("acceptance") or {},
        # Explicitly preserve the informational plan-age statistic separately
        # from the execution handoff metrics below.
        "plan_age_to_entry_sec": report.get("plan_age_to_entry_sec") or report.get("market_wait_sec") or {},
        "execution_latency": report.get("execution_latency") or {},
        "detect_to_mexc_capture_sec": (
            report.get("detect_to_mexc_capture_sec")
            or report.get("paper_to_mexc_capture_sec")
            or {}
        ),
        "mexc_queue_to_preflight_sec": report.get("mexc_queue_to_preflight_sec") or {},
        "mexc_preflight_to_submit_sec": report.get("mexc_preflight_to_submit_sec") or {},
        "by_mode": report.get("by_mode") or [],
        "flags": report.get("flags") or [],
        "sla_breaches": report.get("sla_breaches") or [],
    }


def _stocks_funnel(conn: sqlite3.Connection, *, cutoff: datetime) -> dict[str, Any]:
    result: dict[str, Any] = {"snapshots": {}, "rth_revalidation": {}, "pending_plans": []}
    if _table_exists(conn, "stocks_paper_decision_snapshots"):
        rows = conn.execute(
            "SELECT funnel_state,COUNT(*) n FROM stocks_paper_decision_snapshots "
            "WHERE decision_at>=? GROUP BY funnel_state", (cutoff.isoformat(),)
        ).fetchall()
        result["snapshots"] = {str(row[0]): int(row[1]) for row in rows}
    if _table_exists(conn, "stocks_intraday_rth_revalidations"):
        rows = conn.execute(
            "SELECT decision,COUNT(*) n FROM stocks_intraday_rth_revalidations "
            "WHERE evaluated_at>=? GROUP BY decision", (cutoff.isoformat(),)
        ).fetchall()
        result["rth_revalidation"] = {str(row[0]): int(row[1]) for row in rows}
        pending = conn.execute(
            "SELECT plan_signal_id,symbol,direction,session_open_at,decision,reasons_json "
            "FROM stocks_intraday_rth_revalidations WHERE evaluated_at>=? "
            "AND decision IN ('AWAITING_FRESH_RTH_CANDIDATE',"
            "'AWAITING_PREUS_REVIEW_OR_RTH_CANDIDATE') ORDER BY evaluated_at DESC LIMIT 20",
            (cutoff.isoformat(),),
        ).fetchall()
        result["pending_plans"] = [dict(row) for row in pending]
    return result


def _stocks_ledger_reconciliation(conn: sqlite3.Connection, *, cutoff: datetime) -> dict[str, Any]:
    """Explain every clean closed stock-intraday execution's USD-ledger status.

    A closed simulator row is not automatically a Paper trade: a point-in-time
    alert can explicitly mark it ``SHADOW_ONLY``.  Keeping those categories
    separate prevents the dashboard from presenting a Shadow result as missing
    Paper PnL, while still flagging a genuinely actionable closed execution
    that failed to reach the USD ledger.
    """
    result: dict[str, Any] = {
        "available": False,
        "clean_closed": 0,
        "actionable_closed": 0,
        "ledger_present": 0,
        "deduplicated_equivalent": 0,
        "expected_ledger_missing": 0,
        "intentionally_non_actionable": 0,
        "non_actionable_reasons": [],
        "missing_signal_ids": [],
    }
    required_tables = {"paper_execution_outcomes", "proposed_signals", "paper_portfolio_ledger"}
    if not all(_table_exists(conn, table) for table in required_tables):
        return result
    outcome_cols = {str(row[1]) for row in conn.execute("PRAGMA table_info(paper_execution_outcomes)")}
    required_cols = {"evidence_class", "execution_validity", "lifecycle_state", "entry_at", "exit_at"}
    if not required_cols.issubset(outcome_cols):
        return result

    from src.execution.paper_actionability import build_maps, resolve_paper_actionability

    profile = str(load_portfolio_cfg().get("stock_futures_fee_profile") or "mexc_default_futures")
    rows = conn.execute(
        "WITH latest AS ("
        "SELECT o.*, ROW_NUMBER() OVER (PARTITION BY o.signal_id "
        "ORDER BY COALESCE(o.computed_at, '') DESC, o.rowid DESC) rn "
        "FROM paper_execution_outcomes o) "
        "SELECT p.*,o.* FROM latest o JOIN proposed_signals p ON p.signal_id=o.signal_id "
        "WHERE o.rn=1 AND p.asset_class='stocks' AND p.mode='intraday' "
        "AND o.evidence_class='forward_postfreeze' AND o.execution_validity='valid' "
        "AND o.lifecycle_state='CLOSED' AND COALESCE(o.exit_at,o.entry_at)>=?",
        (cutoff.isoformat(),),
    ).fetchall()
    ledger_cols = {str(row[1]) for row in conn.execute("PRAGMA table_info(paper_portfolio_ledger)")}
    ledger_key_expr = "economic_trade_key" if "economic_trade_key" in ledger_cols else "NULL"
    ledger_rows = conn.execute(
        "SELECT DISTINCT signal_id," + ledger_key_expr + " AS economic_trade_key "
        "FROM paper_portfolio_ledger "
        "WHERE lower(event_type)='exit' AND fee_profile=? AND COALESCE(exit_at,timestamp)>=?",
        (profile, cutoff.isoformat()),
    ).fetchall()
    ledger_ids = {str(row[0]) for row in ledger_rows}
    ledger_keys = {str(row[1]) for row in ledger_rows if row[1]}
    maps = build_maps(conn)
    non_actionable: Counter[str] = Counter()
    for source in rows:
        row = dict(source)
        result["clean_closed"] += 1
        action = resolve_paper_actionability(
            conn,
            str(row.get("signal_id") or ""),
            str(row.get("asset_class") or ""),
            str(row.get("mode") or ""),
            row.get("tier"),
            maps=maps,
            signal=row,
        )
        if float(action.get("size_weight") or 0.0) <= 0.0:
            result["intentionally_non_actionable"] += 1
            non_actionable[str(action.get("source") or "unknown")] += 1
            continue
        result["actionable_closed"] += 1
        if str(row.get("signal_id") or "") in ledger_ids:
            result["ledger_present"] += 1
        elif str(row.get("economic_trade_key") or "") in ledger_keys:
            # Multiple profile adapters can recognize the same economic trade.
            # The USD ledger intentionally keeps one row per economic key, so
            # the second signal is covered by that canonical row, not missing.
            result["deduplicated_equivalent"] += 1
        else:
            result["expected_ledger_missing"] += 1
            result["missing_signal_ids"].append(str(row.get("signal_id") or ""))
    result["non_actionable_reasons"] = non_actionable.most_common(10)
    result["available"] = True
    return result


def build_report(db: str | Path | None = None, *, recent_days: int = 7,
                 now: datetime | None = None) -> dict[str, Any]:
    moment = _utc(now)
    cutoff = moment - timedelta(days=max(1, int(recent_days)))
    path = Path(db or load_config().db_path)
    with sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=30.0) as conn:
        conn.row_factory = sqlite3.Row
        ledger = _authoritative_ledger(conn, cutoff=cutoff)
        grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
        for row in ledger:
            grouped[(str(row.get("asset_class") or "?"), str(row.get("mode") or "?"),
                     str(row.get("direction") or "?"))].append(row)
        performance = [
            {"asset_class": key[0], "mode": key[1], "direction": key[2],
             "fee_profile": rows[0].get("fee_profile"), **_trade_metrics(rows)}
            for key, rows in sorted(grouped.items())
        ]
        report = {
            "version": VERSION,
            "generated_at": moment.isoformat(),
            "cutoff": cutoff.isoformat(),
            "recent_days": recent_days,
            "performance": performance,
            "evidence": _evidence(conn, cutoff=cutoff),
            "overlay": _overlay(conn, cutoff=cutoff),
            "alerts": _alerts(conn, cutoff=cutoff),
            "stocks_funnel": _stocks_funnel(conn, cutoff=cutoff),
            "stocks_ledger_reconciliation": _stocks_ledger_reconciliation(conn, cutoff=cutoff),
            "mexc_handoff": _mexc_handoff(conn, cutoff=cutoff),
            "news_quality": _news_quality(path),
            "latency": _latency(path, recent_days=recent_days),
        }
    report["warnings"] = _warnings(report)
    return report


def _warnings(report: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    evidence = {
        (row["asset_class"], row["mode"], row["direction"]): int(row.get("forward_clean_closed") or 0)
        for row in report.get("evidence") or []
    }
    for row in report.get("performance") or []:
        label = f"{row['asset_class']} {row['mode']} {row['direction']}"
        clean_forward = evidence.get((row["asset_class"], row["mode"], row["direction"]), 0)
        if clean_forward < 30:
            warnings.append(f"INSUFFICIENT_CLEAN_FORWARD_SAMPLE:{label}:{clean_forward}")
        if (row.get("top3_positive_pnl_share") or 0) >= 0.80 and (row.get("closed") or 0) >= 3:
            warnings.append(f"PNL_CONCENTRATED_TOP3:{label}:{row['top3_positive_pnl_share']}")
        if (row.get("profit_factor") is not None and row.get("profit_factor") != math.inf
                and row["profit_factor"] < 1.10):
            warnings.append(f"WEAK_PROFIT_FACTOR:{label}:{row['profit_factor']}")
    pending = len((report.get("stocks_funnel") or {}).get("pending_plans") or [])
    if pending:
        warnings.append(f"STOCKS_PLANS_AWAITING_FRESH_RTH:{pending}")
    reconciliation = report.get("stocks_ledger_reconciliation") or {}
    missing = int(reconciliation.get("expected_ledger_missing") or 0)
    if missing:
        warnings.append(f"STOCKS_ACTIONABLE_CLOSED_MISSING_USD_LEDGER:{missing}")
    news = report.get("news_quality") or {}
    if news.get("status") == "NOT_READY":
        warnings.append("NEWS_QUALITY_NOT_READY:" + ",".join(news.get("reasons") or ["unknown"]))
    mexc = report.get("mexc_handoff") or {}
    if int((mexc.get("outbox") or {}).get("SUBMISSION_UNKNOWN", 0)):
        warnings.append(f"MEXC_SUBMISSION_UNKNOWN:{mexc['outbox']['SUBMISSION_UNKNOWN']}")
    latency = report.get("latency") or {}
    for breach in latency.get("sla_breaches") or []:
        warnings.append(f"LATENCY_SLA:{breach}")
    return warnings


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Paper Operational Audit", "",
             f"Generated: `{report['generated_at']}` - window: `{report['recent_days']}d`",
             "", "## Authoritative net USD"]
    perf = report.get("performance") or []
    if not perf:
        lines.append("- No authoritative closed Paper ledger rows in this window.")
    else:
        lines.extend(["", "| Asset | Mode | Side | Closed | Net USD | PF | WR | Max DD | Top-3 winner share | Fee profile |",
                      "|---|---|---:|---:|---:|---:|---:|---:|---:|---|"])
        for row in perf:
            pf = row.get("profit_factor")
            pf_text = "inf" if pf == math.inf else ("n/a" if pf is None else f"{pf:.2f}")
            wr = row.get("winrate")
            top3 = row.get("top3_positive_pnl_share")
            lines.append(
                f"| {row['asset_class']} | {row['mode']} | {row['direction']} | {row['closed']} | "
                f"{row['net_pnl_usdt']:+.2f} | {pf_text} | "
                f"{('n/a' if wr is None else f'{wr:.0%}')} | {row['max_drawdown_usdt']:.2f} | "
                f"{('n/a' if top3 is None else f'{top3:.0%}')} | {row.get('fee_profile') or '-'} |"
            )
    lines.extend(["", "## Evidence"])
    for row in report.get("evidence") or []:
        lines.append(
            f"- {row['asset_class']} {row['mode']} {row['direction']}: "
            f"forward clean closed {row.get('forward_clean_closed', 0)} - "
            f"forward dirty closed {row.get('forward_dirty_closed', 0)} - "
            f"historical/unclassified closed {row.get('historical_or_unclassified_closed', 0)} - "
            f"open/unresolved {row.get('open_or_unresolved', 0)}"
        )
    lines.extend(["", "## Routing and overlays"])
    for row in report.get("overlay") or []:
        actions = ", ".join(f"{key} {value}" for key, value in sorted(row["actions"].items()))
        lines.append(f"- crypto {row['mode']}: unique signals {row['unique_signals']} - {actions}")
    for row in report.get("alerts") or []:
        routes = ", ".join(f"{key} {value}" for key, value in sorted(row["routes"].items()))
        sizes = ", ".join(f"{key}x {value}" for key, value in sorted(row["size_weights"].items()))
        overlays = ", ".join(f"{key} {value}" for key, value in sorted(row["overlay_actions"].items()))
        guards = ", ".join(f"{key} {value}" for key, value in sorted(row["guard_actions"].items()))
        lines.append(f"- {row['asset_class']} {row['mode']} alerts: {routes} - sizes {sizes} - "
                     f"overlay {overlays} - guard {guards}")
    stocks = report.get("stocks_funnel") or {}
    lines.extend(["", "## Stocks funnel",
                  f"- snapshots: `{json.dumps(stocks.get('snapshots') or {}, sort_keys=True)}`",
                  f"- RTH decisions: `{json.dumps(stocks.get('rth_revalidation') or {}, sort_keys=True)}`",
                  f"- awaiting fresh RTH candidate: `{len(stocks.get('pending_plans') or [])}`",
                  "", "## Stocks USD-ledger reconciliation"])
    reconciliation = report.get("stocks_ledger_reconciliation") or {}
    if not reconciliation.get("available"):
        lines.append("- unavailable: required execution-accounting columns are absent.")
    else:
        lines.extend([
            f"- clean closed executions: `{reconciliation.get('clean_closed', 0)}`",
            f"- actionable closed / ledger present / same-trade deduplicated / missing: "
            f"`{reconciliation.get('actionable_closed', 0)} / "
            f"{reconciliation.get('ledger_present', 0)} / "
            f"{reconciliation.get('deduplicated_equivalent', 0)} / "
            f"{reconciliation.get('expected_ledger_missing', 0)}`",
            f"- intentionally non-actionable (Shadow): `{reconciliation.get('intentionally_non_actionable', 0)}` "
            f"`{json.dumps(reconciliation.get('non_actionable_reasons') or [])}`",
        ])
        if reconciliation.get("missing_signal_ids"):
            lines.append(f"- missing signal ids: `{', '.join(reconciliation['missing_signal_ids'][:20])}`")
    lines.extend(["", "## MEXC handoff"])
    mexc = report.get("mexc_handoff") or {}
    lines.extend([
                  f"- decisions: `{json.dumps(mexc.get('decisions') or {}, sort_keys=True)}`",
                  f"- eligibility: `{json.dumps(mexc.get('eligible') or {}, sort_keys=True)}`",
                  f"- outbox: `{json.dumps(mexc.get('outbox') or {}, sort_keys=True)}`",
                  f"- venue attempts: `{json.dumps(mexc.get('venue_attempts') or {}, sort_keys=True)}`",
                  f"- venue rejections: `{json.dumps(mexc.get('venue_rejections') or [], ensure_ascii=True)}`",
                  f"- positions: `{json.dumps(mexc.get('positions') or {}, sort_keys=True)}` - "
        f"open risk `${float(mexc.get('open_risk_usdt') or 0):.2f}`",
    ])
    for row in mexc.get("parity") or []:
        lines.append(f"- parity {row['profile_id']}: clean forward closed {row['closed']} - "
                     f"net `${row['net_pnl_usdt']:+.2f}` - PF `{row['profit_factor']}`")
    news = report.get("news_quality") or {}
    latency = report.get("latency") or {}
    lines.extend(["", "## Latency",
                  f"- crypto acceptance: `{((latency.get('acceptance') or {}).get('crypto') or {}).get('verdict', 'n/a')}`",
                   f"- stocks intraday acceptance: "
                   f"`{((latency.get('acceptance') or {}).get('stocks_intraday') or {}).get('verdict', 'n/a')}`",
                   f"- Plan age signal -> entry (not execution latency): "
                   f"`{json.dumps(latency.get('plan_age_to_entry_sec') or {}, sort_keys=True)}`",
                   f"- Detection -> MEXC capture: `{json.dumps(latency.get('detect_to_mexc_capture_sec') or {}, sort_keys=True)}`",
                  f"- MEXC queue -> preflight: `{json.dumps(latency.get('mexc_queue_to_preflight_sec') or {}, sort_keys=True)}`",
                  f"- MEXC preflight -> submit: `{json.dumps(latency.get('mexc_preflight_to_submit_sec') or {}, sort_keys=True)}`",
                  "", "## News quality",
                  f"- status: `{news.get('status', 'UNKNOWN')}` - p95 resolution "
                  f"`{news.get('resolution_p95_seconds', 'n/a')}s` - reasons "
                  f"`{json.dumps(news.get('reasons') or [])}`",
                  "", "## Warnings"])
    for warning in report.get("warnings") or ["none"]:
        lines.append(f"- `{warning}`")
    return "\n".join(lines) + "\n"


def write_report(db: str | Path | None = None, *, recent_days: int = 7,
                 target: str | Path | None = None, now: datetime | None = None) -> Path:
    report = build_report(db, recent_days=recent_days, now=now)
    path = Path(target or (load_config().root / "reports" / "PAPER_OPERATIONAL_AUDIT.md"))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(report), encoding="utf-8")
    return path


__all__ = ["VERSION", "build_report", "render_markdown", "write_report"]
