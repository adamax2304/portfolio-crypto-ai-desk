"""Central strategy evidence lifecycle and micro-canary guard.

The module is deliberately small and deterministic. It reads immutable
configuration plus execution ledgers, emits an auditable verdict, and may stop
*new* canary captures after the configured evidence boundary. It never edits a
route, mutates a trade, closes a position, or promotes a strategy.
"""
from __future__ import annotations

import hashlib
import json
import math
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import yaml

from src.config import load_config


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "strategy_governance.yaml"
REPORT_PATH = ROOT / "reports" / "STRATEGY_GOVERNANCE_LATEST.md"
EVALUATION_VERSION = "strategy_governance_v1"

EVALUATION_DDL = """
CREATE TABLE IF NOT EXISTS strategy_governance_evaluations (
  evaluation_id TEXT PRIMARY KEY,
  evaluated_at TEXT NOT NULL,
  strategy_id TEXT NOT NULL,
  stage TEXT NOT NULL,
  verdict TEXT NOT NULL,
  new_entries_allowed INTEGER NOT NULL,
  metrics_json TEXT NOT NULL,
  reasons_json TEXT NOT NULL,
  config_fingerprint TEXT,
  version TEXT NOT NULL
)
"""


def _utc(value: datetime | None = None) -> datetime:
    moment = value or datetime.now(timezone.utc)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone.utc)


def _parse(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def _sha(value: Any) -> str:
    return hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


def load_policy(path: str | Path | None = None) -> dict[str, Any]:
    selected = Path(path) if path else CONFIG_PATH
    raw = yaml.safe_load(selected.read_text(encoding="utf-8")) or {}
    block = raw.get("strategy_governance") or {}
    if not isinstance(block, dict):
        raise ValueError("strategy_governance must be a mapping")
    return block


def _read_block(path: Path, block: str) -> dict[str, Any]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    value = raw.get(block) or {}
    if not isinstance(value, dict):
        raise ValueError(f"{path}: {block} must be a mapping")
    return value


def frozen_fingerprint(
    strategy_id: str, *, policy: dict[str, Any] | None = None,
    root: Path | None = None,
) -> str:
    policy = policy or load_policy()
    root = root or ROOT
    spec = (policy.get("frozen_strategies") or {}).get(strategy_id) or {}
    if not spec:
        raise KeyError(f"unknown frozen strategy: {strategy_id}")
    payload: list[dict[str, Any]] = []
    for item in spec.get("inputs") or []:
        relative = str(item.get("path") or "")
        block_name = str(item.get("block") or "")
        source = _read_block(root / relative, block_name)
        fields = [str(field) for field in (item.get("fields") or [])]
        missing = [field for field in fields if field not in source]
        if missing:
            raise ValueError(f"{relative}:{block_name} missing frozen fields {missing}")
        payload.append({
            "path": relative,
            "block": block_name,
            "values": {field: source[field] for field in fields},
        })
    return _sha(payload)


def verify_frozen_strategy(
    strategy_id: str, *, policy: dict[str, Any] | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    policy = policy or load_policy()
    spec = (policy.get("frozen_strategies") or {}).get(strategy_id) or {}
    expected = str(spec.get("expected_sha256") or "")
    try:
        actual = frozen_fingerprint(strategy_id, policy=policy, root=root)
    except Exception as exc:
        return {
            "ok": False,
            "strategy_id": strategy_id,
            "expected": expected,
            "actual": None,
            "reason": f"FROZEN_CONFIG_UNREADABLE:{type(exc).__name__}",
        }
    return {
        "ok": bool(expected and expected != "PENDING_GENERATION" and actual == expected),
        "strategy_id": strategy_id,
        "expected": expected,
        "actual": actual,
        "reason": None if actual == expected else "FROZEN_CONFIG_FINGERPRINT_MISMATCH",
    }


def validate_profile_registry(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    policy = policy or load_policy()
    owners: dict[str, str] = {}
    duplicates: list[dict[str, str]] = []
    empty: list[str] = []
    for strategy_id, raw_profiles in (policy.get("profile_registry") or {}).items():
        profiles = raw_profiles if isinstance(raw_profiles, list) else [raw_profiles]
        if not profiles:
            empty.append(str(strategy_id))
        for raw in profiles:
            profile = str(raw or "").strip()
            if not profile:
                empty.append(str(strategy_id))
                continue
            previous = owners.get(profile)
            if previous and previous != strategy_id:
                duplicates.append({
                    "profile_id": profile,
                    "first_strategy": previous,
                    "second_strategy": str(strategy_id),
                })
            owners[profile] = str(strategy_id)
    return {
        "ok": not duplicates and not empty,
        "profiles": len(owners),
        "duplicates": duplicates,
        "empty_strategies": sorted(set(empty)),
    }


def _profit_factor(values: list[float]) -> float | None:
    wins = sum(value for value in values if value > 0)
    losses = abs(sum(value for value in values if value < 0))
    if losses > 0:
        return round(wins / losses, 4)
    return math.inf if wins > 0 else None


def _drawdown_r(values: list[float]) -> float:
    peak = running = maximum = 0.0
    for value in values:
        running += value
        peak = max(peak, running)
        maximum = max(maximum, peak - running)
    return round(maximum, 4)


def _connect(path: Path, *, readonly: bool = False) -> sqlite3.Connection:
    if readonly:
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=20.0)
    else:
        conn = sqlite3.connect(path, timeout=20.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=20000")
    return conn


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    return bool(conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
    ).fetchone())


def paper_profile_metrics(
    conn: sqlite3.Connection, *, profiles: list[str], activation_at: str,
    exit_version: str,
) -> dict[str, Any]:
    conn.row_factory = sqlite3.Row
    if not profiles or not _table_exists(conn, "paper_execution_outcomes"):
        return {"available": False, "reason": "PAPER_OUTCOMES_UNAVAILABLE"}
    placeholders = ",".join("?" for _ in profiles)
    rows = conn.execute(
        "SELECT o.signal_id,o.paper_execution_r,o.entry_at,o.exit_at,o.computed_at,"
        "o.path_data_quality,l.net_pnl_usdt,l.fees_usdt,l.slippage_usdt,l.funding_usdt "
        "FROM paper_execution_outcomes o "
        "LEFT JOIN paper_portfolio_ledger l ON l.id=("
        " SELECT MAX(x.id) FROM paper_portfolio_ledger x "
        " WHERE x.signal_id=o.signal_id AND x.event_type='exit') "
        f"WHERE o.paper_entry_profile IN ({placeholders}) AND o.version=? "
        "AND COALESCE(o.exit_at,o.computed_at)>=? AND o.lifecycle_state='CLOSED' "
        "AND o.paper_execution_r IS NOT NULL "
        "AND COALESCE(o.current_price_revalidated,0)=1 "
        "AND COALESCE(o.entry_time_basis,'')='point_in_time_current_bar' "
        "AND COALESCE(o.execution_validity,'valid')='valid' "
        "AND COALESCE(o.path_data_quality,'complete')='complete' "
        "ORDER BY COALESCE(o.exit_at,o.computed_at),o.signal_id",
        (*profiles, exit_version, activation_at),
    ).fetchall()
    r_values = [float(row["paper_execution_r"]) for row in rows]
    usd_values = [float(row["net_pnl_usdt"]) for row in rows if row["net_pnl_usdt"] is not None]
    sessions = {
        parsed.astimezone(ZoneInfo("America/New_York")).date().isoformat()
        for parsed in (_parse(row["entry_at"]) for row in rows) if parsed is not None
    }
    return {
        "available": True,
        "clean_closed": len(rows),
        "net_r": round(sum(r_values), 4),
        "expectancy_r": round(sum(r_values) / len(r_values), 4) if r_values else None,
        "profit_factor_r": _profit_factor(r_values),
        "net_pnl_usdt": round(sum(usd_values), 4),
        "costed_closed": len(usd_values),
        "fees_usdt": round(sum(float(row["fees_usdt"] or 0.0) for row in rows), 4),
        "slippage_usdt": round(sum(float(row["slippage_usdt"] or 0.0) for row in rows), 4),
        "funding_usdt": round(sum(float(row["funding_usdt"] or 0.0) for row in rows), 4),
        "max_drawdown_r": _drawdown_r(r_values),
        "rth_sessions": len(sessions),
        "exit_version": exit_version,
    }


def _live_metrics(
    conn: sqlite3.Connection, *, activation_at: str, live_strategy_version: str,
) -> dict[str, Any]:
    if not (_table_exists(conn, "mexc_canary_positions")
            and _table_exists(conn, "mexc_canary_decisions")):
        return {"available": False, "reason": "LIVE_LEDGER_UNAVAILABLE"}
    rows = conn.execute(
        "SELECT p.realized_pnl_usdt,p.risk_usdt,p.closed_at,d.signal_id,d.decision_json "
        "FROM mexc_canary_positions p JOIN mexc_canary_decisions d "
        "ON d.decision_id=p.decision_id "
        "WHERE p.status='CLOSED' AND p.closed_at>=? ORDER BY p.closed_at,d.decision_id",
        (activation_at,),
    ).fetchall()
    selected: list[sqlite3.Row] = []
    for row in rows:
        try:
            payload = json.loads(row["decision_json"] or "{}")
        except (TypeError, ValueError, json.JSONDecodeError):
            payload = {}
        if str(payload.get("strategy_version") or "") == live_strategy_version:
            selected.append(row)
    pnl = [float(row["realized_pnl_usdt"] or 0.0) for row in selected]
    r_values = [
        float(row["realized_pnl_usdt"] or 0.0) / float(row["risk_usdt"])
        for row in selected if float(row["risk_usdt"] or 0.0) > 0
    ]
    return {
        "available": True,
        "closed": len(selected),
        "net_pnl_usdt": round(sum(pnl), 4),
        "profit_factor": _profit_factor(pnl),
        "net_r": round(sum(r_values), 4),
        "expectancy_r": round(sum(r_values) / len(r_values), 4) if r_values else None,
        "max_drawdown_r": _drawdown_r(r_values),
    }


def evaluate_strategy(
    strategy_id: str, *, db: str | Path | None = None,
    policy: dict[str, Any] | None = None, now: datetime | None = None,
) -> dict[str, Any]:
    policy = policy or load_policy()
    strategy = (policy.get("strategies") or {}).get(strategy_id) or {}
    if not strategy:
        raise KeyError(f"unknown strategy: {strategy_id}")
    stage = str(strategy.get("stage") or "shadow")
    activation_at = str(strategy.get("activation_at") or policy.get("activated_at") or "")
    db_path = Path(db) if db else load_config().db_path
    freeze = (
        verify_frozen_strategy(strategy_id, policy=policy)
        if strategy_id in (policy.get("frozen_strategies") or {})
        else {"ok": True, "actual": None, "reason": None}
    )
    profiles = [str(value) for value in (strategy.get("profile_ids") or [])]
    evidence = policy.get("evidence_contract") or {}
    metrics: dict[str, Any] = {}
    reasons: list[str] = []
    verdict = "PAPER_ACCUMULATING" if stage == "paper" else "SHADOW_ONLY"
    allowed = False

    try:
        conn = _connect(db_path, readonly=True)
    except sqlite3.Error as exc:
        return {
            "strategy_id": strategy_id, "stage": stage,
            "verdict": "EVIDENCE_UNAVAILABLE", "new_entries_allowed": False,
            "reasons": [f"SQLITE:{type(exc).__name__}"], "metrics": {},
            "config_freeze": freeze,
        }
    try:
        if stage == "micro_canary":
            metrics["live"] = _live_metrics(
                conn,
                activation_at=activation_at,
                live_strategy_version=str(strategy.get("live_strategy_version") or ""),
            )
            live = metrics["live"]
            canary = policy.get("micro_canary") or {}
            minimum = int(canary.get("minimum_closed_before_decision", 10))
            target = int(canary.get("target_closed", 20))
            closed = int(live.get("closed") or 0)
            if not freeze.get("ok"):
                verdict = "AUTO_DEMOTED_CONFIG_DRIFT"
                reasons.append(str(freeze.get("reason") or "CONFIG_DRIFT"))
            elif not live.get("available"):
                verdict = "AUTO_DEMOTED_EVIDENCE_UNAVAILABLE"
                reasons.append(str(live.get("reason") or "LIVE_LEDGER_UNAVAILABLE"))
            elif closed < minimum:
                verdict, allowed = "MICRO_CANARY_WARMUP", True
                reasons.append(f"closed={closed}<{minimum}")
            else:
                pf = live.get("profit_factor")
                failing = []
                if bool(canary.get("require_positive_net_after_costs", True)) \
                        and float(live.get("net_pnl_usdt") or 0.0) <= 0:
                    failing.append("LIVE_NET_NOT_POSITIVE")
                if pf is None or float(pf) < float(canary.get("minimum_profit_factor", 1.0)):
                    failing.append("LIVE_PF_BELOW_MINIMUM")
                if float(live.get("max_drawdown_r") or 0.0) > float(canary.get("maximum_drawdown_r", 5.0)):
                    failing.append("LIVE_DRAWDOWN_EXCEEDED")
                # No v3-compatible paired sweep ledger exists yet. It is safe
                # to gather the micro sample, but it cannot roll into normal
                # live after the target sample without that parity evidence.
                metrics["paired_v3"] = {"closed": 0, "available": False}
                if closed >= target:
                    required = int(canary.get("minimum_paired_v3_trades_at_target", 10))
                    if int(metrics["paired_v3"]["closed"]) < required:
                        failing.append("PAIRED_V3_EVIDENCE_MISSING_AT_CANARY_TARGET")
                if failing:
                    verdict = "AUTO_DEMOTED_MICRO_CANARY"
                    reasons.extend(failing)
                else:
                    verdict, allowed = "MICRO_CANARY_CONTINUE", True
        elif stage == "paper":
            # Only the shared execution ledger can claim v3 parity. Dedicated
            # strategy tables remain visible but cannot silently qualify.
            metrics["paper"] = paper_profile_metrics(
                conn,
                profiles=profiles,
                activation_at=activation_at,
                exit_version=str(evidence.get("paper_exit_version") or ""),
            )
            paper = metrics["paper"]
            if not paper.get("available"):
                verdict = "PAPER_EVIDENCE_UNAVAILABLE"
                reasons.append(str(paper.get("reason") or "PAPER_EVIDENCE_UNAVAILABLE"))
            else:
                checks = {
                    "sample": int(paper.get("clean_closed") or 0) >= int(evidence.get("minimum_clean_closed", 30)),
                    "profit_factor": paper.get("profit_factor_r") is not None and float(paper["profit_factor_r"]) >= float(evidence.get("minimum_profit_factor", 1.25)),
                    "expectancy": paper.get("expectancy_r") is not None and float(paper["expectancy_r"]) > float(evidence.get("minimum_expectancy_r", 0.0)),
                    "net_after_costs": (not bool(evidence.get("require_positive_net_after_costs", True)) or (int(paper.get("costed_closed") or 0) == int(paper.get("clean_closed") or 0) and float(paper.get("net_pnl_usdt") or 0.0) > 0)),
                    "drawdown": float(paper.get("max_drawdown_r") or 0.0) <= float(evidence.get("maximum_drawdown_r", 8.0)),
                }
                required_sessions = int(strategy.get("require_rth_sessions") or 0)
                if required_sessions:
                    checks["rth_sessions"] = int(paper.get("rth_sessions") or 0) >= required_sessions
                metrics["checks"] = checks
                if all(checks.values()):
                    verdict = "READY_FOR_OPERATOR_MICRO_CANARY_REVIEW"
                else:
                    verdict = "PAPER_ACCUMULATING"
                    reasons.extend(name.upper() for name, ok in checks.items() if not ok)
        else:
            verdict = "SHADOW_ONLY"
    finally:
        conn.close()
    return {
        "strategy_id": strategy_id,
        "stage": stage,
        "activation_at": activation_at,
        "evaluated_at": _utc(now).isoformat(),
        "verdict": verdict,
        "new_entries_allowed": bool(allowed),
        "reasons": reasons,
        "metrics": metrics,
        "config_freeze": freeze,
    }


def runtime_route_gate(
    strategy_id: str, *, db: str | Path | None = None,
    policy: dict[str, Any] | None = None, now: datetime | None = None,
) -> dict[str, Any]:
    result = evaluate_strategy(strategy_id, db=db, policy=policy, now=now)
    return {
        "allowed": bool(result.get("new_entries_allowed")),
        "verdict": result.get("verdict"),
        "reasons": list(result.get("reasons") or []),
        "metrics": result.get("metrics") or {},
        "config_freeze": result.get("config_freeze") or {},
    }


def evaluate_all(
    *, db: str | Path | None = None, policy: dict[str, Any] | None = None,
    now: datetime | None = None, persist: bool = True,
) -> dict[str, Any]:
    policy = policy or load_policy()
    profile_registry = validate_profile_registry(policy)
    strategies = [
        evaluate_strategy(strategy_id, db=db, policy=policy, now=now)
        for strategy_id in (policy.get("strategies") or {})
    ]
    result = {
        "version": EVALUATION_VERSION,
        "evaluated_at": _utc(now).isoformat(),
        "profile_registry": profile_registry,
        "llm_policy": policy.get("llm_policy") or {},
        "strategies": strategies,
    }
    if persist:
        evaluation_db = ROOT / str(
            policy.get("evaluation_db_path") or "db/strategy_governance.sqlite"
        )
        evaluation_db.parent.mkdir(parents=True, exist_ok=True)
        try:
            with _connect(evaluation_db) as conn:
                conn.execute(EVALUATION_DDL)
                for row in strategies:
                    evaluation_id = _sha({
                        "strategy_id": row["strategy_id"],
                        "evaluated_at": result["evaluated_at"],
                        "version": EVALUATION_VERSION,
                    })
                    conn.execute(
                        "INSERT OR REPLACE INTO strategy_governance_evaluations("
                        "evaluation_id,evaluated_at,strategy_id,stage,verdict,"
                        "new_entries_allowed,metrics_json,reasons_json,config_fingerprint,version) "
                        "VALUES(?,?,?,?,?,?,?,?,?,?)",
                        (
                            evaluation_id, result["evaluated_at"], row["strategy_id"],
                            row["stage"], row["verdict"], int(row["new_entries_allowed"]),
                            _json(row["metrics"]), _json(row["reasons"]),
                            (row.get("config_freeze") or {}).get("actual"), EVALUATION_VERSION,
                        ),
                    )
                conn.commit()
            result["persistence"] = {"status": "OK", "path": str(evaluation_db)}
        except sqlite3.Error as exc:
            # Audit persistence must never compete with or interrupt trading.
            result["persistence"] = {
                "status": "DEGRADED",
                "path": str(evaluation_db),
                "error": type(exc).__name__,
            }
    return result


def render_markdown(result: dict[str, Any]) -> str:
    profile = result.get("profile_registry") or {}
    lines = [
        "# Strategy Governance",
        "",
        f"Generated: `{result.get('evaluated_at')}`",
        f"Profile registry: **{'OK' if profile.get('ok') else 'FAILED'}** "
        f"({profile.get('profiles', 0)} unique profiles)",
        "",
        "| strategy | stage | verdict | new entries | evidence |",
        "|---|---|---|---:|---|",
    ]
    for row in result.get("strategies") or []:
        metrics = row.get("metrics") or {}
        live = metrics.get("live") or {}
        paper = metrics.get("paper") or {}
        evidence = (
            f"live closed={live.get('closed', 0)}, PF={live.get('profit_factor')}, "
            f"net=${live.get('net_pnl_usdt', 0)}"
            if live else
            f"paper v3={paper.get('clean_closed', 0)}, PF={paper.get('profit_factor_r')}, "
            f"sessions={paper.get('rth_sessions', 0)}"
            if paper else "n/a"
        )
        lines.append(
            f"| {row['strategy_id']} | {row['stage']} | {row['verdict']} | "
            f"{'yes' if row['new_entries_allowed'] else 'no'} | {evidence} |"
        )
        if row.get("reasons"):
            lines.append(f"|  |  | reasons |  | `{', '.join(row['reasons'])}` |")
    lines += [
        "",
        "## Rules",
        "",
        "- Paper promotion uses only point-in-time `live_exit_parity_v3_incremental` closes.",
        "- Promotion is never automatic; a passing Paper gate only requests operator review.",
        "- Micro-canary auto-demotion stops new captures only. It never closes existing positions.",
        "- LLM output is advisory context only and cannot change entry, veto, score, risk, stops, targets, or routing.",
    ]
    return "\n".join(lines) + "\n"


def write_report(result: dict[str, Any], path: str | Path | None = None) -> Path:
    target = Path(path) if path else REPORT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_markdown(result), encoding="utf-8")
    return target


__all__ = [
    "evaluate_all", "evaluate_strategy", "frozen_fingerprint", "load_policy",
    "paper_profile_metrics", "render_markdown", "runtime_route_gate",
    "validate_profile_registry", "verify_frozen_strategy", "write_report",
]
