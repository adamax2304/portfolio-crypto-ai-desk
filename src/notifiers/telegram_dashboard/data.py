"""Read-only SQLite queries backing the Telegram dashboard.

Every connection uses SQLite's read-only URI mode.  The module intentionally
does not import execution, scoring, risk, or live-routing code.
"""

from __future__ import annotations

import json
import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable


def _active_paper_fee_profile() -> str | None:
    """Return the portfolio scenario shown to an operator.

    The ledger intentionally persists several cost scenarios (zero, active,
    conservative, etc.) for research. A dashboard must never add those books
    together: one economic trade would otherwise appear once per scenario.
    """
    try:
        from src.execution.paper_portfolio import load_cfg

        value = str(load_cfg().get("fee_profile") or "").strip()
        return value or None
    except Exception:
        return None


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_timestamp(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def _float(value: Any) -> float:
    try:
        return float(value or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _safe_json(value: Any) -> dict[str, Any]:
    try:
        loaded = json.loads(value or "{}")
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}
    return loaded if isinstance(loaded, dict) else {}


class DashboardData:
    """Small, schema-tolerant, read-only view over desk evidence tables."""

    def __init__(self, db_path: Path):
        self.db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        uri = f"file:{self.db_path.resolve().as_posix()}?mode=ro"
        conn = sqlite3.connect(uri, uri=True, timeout=3)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA query_only = ON")
        conn.execute("PRAGMA busy_timeout = 3000")
        return conn

    @staticmethod
    def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
        return bool(conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?", (table,)
        ).fetchone())

    @staticmethod
    def _columns(conn: sqlite3.Connection, table: str) -> set[str]:
        return {str(row[1]) for row in conn.execute(f"PRAGMA table_info({table})")}

    @staticmethod
    def _in_clause(values: Iterable[str]) -> tuple[str, list[str]]:
        values = list(values)
        return ",".join("?" for _ in values), values

    def snapshot(self) -> dict[str, Any]:
        """Return the compact home-page model from authoritative read models."""
        health = self.health_summary()
        observed = [_parse_timestamp(item.get("latest")) for item in health["freshness"]]
        latest = max((value for value in observed if value is not None), default=_utc_now())
        return {
            # This is evidence freshness, not render time. Keeping it stable
            # prevents no-op scheduler cycles from editing Telegram needlessly.
            "generated_at": latest.isoformat(),
            "paper": self.paper_summary(days=7),
            "shadow": self.shadow_summary(days=7),
            "positions": self.open_positions(),
            "health": health,
        }

    def paper_summary(self, *, days: int = 7) -> dict[str, Any]:
        result: dict[str, Any] = {
            "available": False,
            "balance": None,
            "starting_balance": None,
            "week_pnl": 0.0,
            "week_closed": 0,
            "week_winrate": None,
            "costs": {"fees": 0.0, "slippage": 0.0, "funding": 0.0},
            "by_mode": [],
        }
        with self._connect() as conn:
            if not self._table_exists(conn, "paper_portfolio_ledger"):
                return result
            result["available"] = True
            columns = self._columns(conn, "paper_portfolio_ledger")
            active_profile = (
                _active_paper_fee_profile() if "fee_profile" in columns else None
            )
            profile_where = ""
            profile_params: list[Any] = []
            if active_profile:
                profile_where = " WHERE fee_profile = ?"
                profile_params.append(active_profile)
            if "equity_after" in columns:
                latest = conn.execute(
                    "SELECT equity_after, equity_before FROM paper_portfolio_ledger "
                    f"{profile_where} ORDER BY rowid DESC LIMIT 1",
                    profile_params,
                ).fetchone()
                if latest:
                    result["balance"] = latest["equity_after"]
                    result["starting_balance"] = latest["equity_before"]

            cutoff = (_utc_now() - timedelta(days=days)).isoformat()
            rows = conn.execute(
                f"""
                SELECT l.signal_id, l.net_pnl_usdt, l.fees_usdt, l.slippage_usdt,
                       l.funding_usdt, l.exit_at, l.timestamp, l.close_reason,
                       COALESCE(s.asset_class, 'crypto') AS asset_class,
                       COALESCE(s.mode, 'unknown') AS mode
                 FROM paper_portfolio_ledger l
             LEFT JOIN proposed_signals s ON s.signal_id = l.signal_id
                 WHERE COALESCE(l.exit_at, l.timestamp) >= ?
                   AND l.event_type = 'exit'
                   {"AND l.fee_profile = ?" if active_profile else ""}
                """,
                (cutoff, *profile_params),
            ).fetchall()
            per_mode: dict[tuple[str, str], dict[str, Any]] = {}
            winners = 0
            for row in rows:
                pnl = _float(row["net_pnl_usdt"])
                result["week_pnl"] += pnl
                result["week_closed"] += 1
                winners += int(pnl > 0)
                result["costs"]["fees"] += _float(row["fees_usdt"])
                result["costs"]["slippage"] += _float(row["slippage_usdt"])
                result["costs"]["funding"] += _float(row["funding_usdt"])
                key = (str(row["asset_class"]), str(row["mode"]))
                item = per_mode.setdefault(key, {
                    "asset_class": key[0], "mode": key[1], "closed": 0,
                    "pnl": 0.0, "wins": 0,
                })
                item["closed"] += 1
                item["pnl"] += pnl
                item["wins"] += int(pnl > 0)
            result["week_winrate"] = (winners / result["week_closed"] * 100.0
                                      if result["week_closed"] else None)
            result["by_mode"] = sorted(
                ({**item, "winrate": item["wins"] / item["closed"] * 100.0}
                 for item in per_mode.values()),
                key=lambda item: (item["asset_class"], item["mode"]),
            )
        return result

    def paper_trades(self, *, days: int | None = None, limit: int = 10,
                     offset: int = 0, mode_key: str | None = None) -> dict[str, Any]:
        result: dict[str, Any] = {"rows": [], "total": 0, "days": days}
        with self._connect() as conn:
            if not self._table_exists(conn, "paper_portfolio_ledger"):
                return result
            params: list[Any] = []
            where = ["l.event_type = 'exit'"]
            columns = self._columns(conn, "paper_portfolio_ledger")
            active_profile = (
                _active_paper_fee_profile() if "fee_profile" in columns else None
            )
            if active_profile:
                where.append("l.fee_profile = ?")
                params.append(active_profile)
            if days is not None:
                cutoff = (_utc_now() - timedelta(days=days)).isoformat()
                where.append("COALESCE(l.exit_at, l.timestamp) >= ?")
                params.append(cutoff)
            if mode_key:
                asset_class, _, mode = mode_key.partition(":")
                where.extend(["COALESCE(s.asset_class, 'crypto') = ?", "COALESCE(s.mode, 'unknown') = ?"])
                params.extend([asset_class, mode])
            where_sql = " AND ".join(where)
            total_row = conn.execute(
                f"SELECT COUNT(*) AS n FROM paper_portfolio_ledger l "
                f"LEFT JOIN proposed_signals s ON s.signal_id = l.signal_id WHERE {where_sql}",
                params,
            ).fetchone()
            result["total"] = int(total_row["n"] if total_row else 0)
            query_params = [*params, limit, offset]
            rows = conn.execute(
                f"""
                SELECT l.signal_id, l.net_pnl_usdt, l.fees_usdt, l.slippage_usdt,
                       l.funding_usdt, COALESCE(e.entry_at, l.entry_at) AS entry_at,
                       l.exit_at, l.timestamp, l.close_reason,
                       COALESCE(s.symbol, '?') AS symbol, COALESCE(s.direction, '?') AS direction,
                       COALESCE(s.asset_class, 'crypto') AS asset_class,
                       COALESCE(s.mode, 'unknown') AS mode
                  FROM paper_portfolio_ledger l
             LEFT JOIN proposed_signals s ON s.signal_id = l.signal_id
             LEFT JOIN paper_execution_outcomes e ON e.signal_id = l.signal_id
                 WHERE {where_sql}
              ORDER BY COALESCE(l.exit_at, l.timestamp) DESC, l.rowid DESC
                 LIMIT ? OFFSET ?
                """,
                query_params,
            ).fetchall()
            result["rows"] = [dict(row) for row in rows]
        return result

    def open_positions(self) -> list[dict[str, Any]]:
        positions: list[dict[str, Any]] = []
        with self._connect() as conn:
            if self._table_exists(conn, "paper_execution_outcomes"):
                rows = conn.execute(
                    """
                    SELECT e.signal_id, e.entry_at, e.entry_price_used, e.stop_initial,
                           e.lifecycle_state, e.paper_execution_outcome,
                           s.symbol, s.direction, s.mode, s.asset_class, s.tier
                      FROM paper_execution_outcomes e
                      JOIN proposed_signals s ON s.signal_id = e.signal_id
                     WHERE COALESCE(e.lifecycle_state, '') IN ('OPEN', 'ENTERED', 'WAITING')
                        OR COALESCE(e.paper_execution_outcome, '') = 'open'
                  ORDER BY e.entry_at DESC
                     LIMIT 12
                    """
                ).fetchall()
                positions.extend(dict(row) for row in rows)
            if self._table_exists(conn, "mexc_stock_futures_paper_positions"):
                mexc_rows = conn.execute(
                    """
                    SELECT source_signal_id AS signal_id, entry_at,
                           entry_price AS entry_price_used,
                           stop_current AS stop_initial, status AS lifecycle_state,
                           'open' AS paper_execution_outcome,
                           ticker AS symbol, direction, 'intraday' AS mode,
                           'stocks' AS asset_class, 'paper' AS tier
                      FROM mexc_stock_futures_paper_positions
                     WHERE status='OPEN'
                  ORDER BY entry_at DESC
                     LIMIT 12
                    """
                ).fetchall()
                positions.extend(dict(row) for row in mexc_rows)
            if self._table_exists(conn, "stocks_position_candidates") and self._table_exists(conn, "stocks_position_outcomes"):
                stock_rows = conn.execute(
                    """
                    SELECT c.candidate_id AS signal_id, c.symbol, c.direction, c.mode,
                           c.asset_class, c.entry_price AS entry_price_used,
                           c.stop_price AS stop_initial, c.created_at AS entry_at,
                           o.status AS lifecycle_state, o.unrealized_pnl_usd
                      FROM stocks_position_candidates c
                 LEFT JOIN stocks_position_outcomes o ON o.candidate_id = c.candidate_id
                     WHERE COALESCE(o.status, c.status, 'pending') IN ('pending', 'open', 'shadow_open')
                  ORDER BY c.created_at DESC
                     LIMIT 12
                    """
                ).fetchall()
                positions.extend({**dict(row), "tier": "shadow"} for row in stock_rows)
        return positions[:12]

    def shadow_summary(self, *, days: int = 7) -> dict[str, Any]:
        result: dict[str, Any] = {"lanes": [], "days": days}
        cutoff = (_utc_now() - timedelta(days=days)).isoformat()
        with self._connect() as conn:
            if self._table_exists(conn, "paper_shadow_execution_outcomes"):
                rows = conn.execute(
                    """
                    SELECT COALESCE(shadow_lane, 'ab_main') AS lane,
                           COALESCE(asset_class, 'crypto') AS asset_class,
                           COALESCE(playbook, mode_source, 'unknown') AS mode,
                           outcome_status, is_clean_for_edge, net_pnl_usdt,
                           fees_usdt, slippage_usdt, updated_at
                      FROM paper_shadow_execution_outcomes
                     WHERE COALESCE(updated_at, created_at) >= ?
                    """,
                    (cutoff,),
                ).fetchall()
                self._accumulate_shadow_rows(result["lanes"], rows, "lane", "net_pnl_usdt")
            self._append_strategy_evaluation(
                conn, result["lanes"], "crypto_derivreset_v3_shadow_evaluations",
                "shadow_derivreset_v3", "crypto", "Derivatives Reset v3 (event sequence)",
            )
            self._append_strategy_evaluation(
                conn, result["lanes"], "stocks_catalyst_rs_shadow_evaluations",
                "shadow_catalyst_rs", "stocks", "Catalyst RS",
            )
            self._append_stocks_intraday_evaluations(conn, result["lanes"])
            self._append_position_framework(conn, result["lanes"])
        result["lanes"] = sorted(result["lanes"], key=lambda item: (item["asset_class"], item["lane"]))
        return result

    @staticmethod
    def _accumulate_shadow_rows(target: list[dict[str, Any]], rows: Iterable[sqlite3.Row],
                                lane_key: str, pnl_key: str) -> None:
        buckets: dict[tuple[str, str], dict[str, Any]] = {}
        for row in rows:
            lane = str(row[lane_key])
            asset_class = str(row["asset_class"])
            key = (lane, asset_class)
            item = buckets.setdefault(key, {
                "key": f"{asset_class}:{lane}", "lane": lane, "asset_class": asset_class,
                "label": f"{asset_class.title()} - {lane}", "forward_rows": 0,
                "raw_closed": 0, "raw_pnl": 0.0, "clean_closed": 0,
                "dirty_rows": 0, "dirty_closed": 0, "dirty_pnl": 0.0,
                "unclassified_rows": 0, "unclassified_closed": 0,
                "unclassified_pnl": 0.0, "pnl": 0.0, "fees": 0.0, "slippage": 0.0,
                "winrate": None, "verdict": "MEASUREMENT_ONLY", "source": "outcomes",
            })
            item["forward_rows"] += 1
            clean = row["is_clean_for_edge"]
            if clean == 0:
                item["dirty_rows"] += 1
            elif clean is None:
                item["unclassified_rows"] += 1
            status = str(row["outcome_status"] or "").lower()
            pnl = row[pnl_key]
            terminal = status in {"closed", "win", "loss", "stopped", "tp3_hit"} and pnl is not None
            if terminal:
                item["raw_closed"] += 1
                item["raw_pnl"] += _float(pnl)
            if clean == 1 and terminal:
                item["clean_closed"] += 1
                item["pnl"] += _float(pnl)
                item["fees"] += _float(row["fees_usdt"])
                item["slippage"] += _float(row["slippage_usdt"])
                item.setdefault("wins", 0)
                item["wins"] += int(_float(pnl) > 0)
            elif clean == 0 and terminal:
                item["dirty_closed"] += 1
                item["dirty_pnl"] += _float(pnl)
            elif clean is None and terminal:
                item["unclassified_closed"] += 1
                item["unclassified_pnl"] += _float(pnl)
        for item in buckets.values():
            if item["clean_closed"]:
                item["winrate"] = item.pop("wins", 0) / item["clean_closed"] * 100.0
            else:
                item.pop("wins", None)
            target.append(item)

    @staticmethod
    def _append_strategy_evaluation(conn: sqlite3.Connection, target: list[dict[str, Any]],
                                    table: str, lane: str, asset_class: str, label: str) -> None:
        if not DashboardData._table_exists(conn, table):
            return
        row = conn.execute(f"SELECT * FROM {table} ORDER BY rowid DESC LIMIT 1").fetchone()
        if not row:
            return
        target.append({
            "key": f"{asset_class}:{lane}", "lane": lane,
            "asset_class": asset_class,
            "label": label,
            "forward_rows": int(row["forward_rows"] or 0),
            "raw_closed": int(row["clean_closed"] or 0),
            "raw_pnl": _float(row["net_pnl_usd"]),
            "clean_closed": int(row["clean_closed"] or 0),
            "dirty_rows": int(row["dirty_rows"] or 0),
            "dirty_closed": 0, "dirty_pnl": 0.0,
            "unclassified_rows": 0, "unclassified_closed": 0, "unclassified_pnl": 0.0,
            "pnl": _float(row["net_pnl_usd"]),
            "fees": _float(row["fees_usd"]),
            "slippage": _float(row["slippage_usd"]),
            "funding": _float(row["funding_usd"]),
            "winrate": row["winrate"],
            "profit_factor": row["profit_factor"],
            "verdict": str(row["verdict"] or "MEASUREMENT_ONLY"),
            "source": "evaluation",
            "rejections": _safe_json(row["rejection_counts_json"]),
        })

    @staticmethod
    def _append_stocks_intraday_evaluations(conn: sqlite3.Connection, target: list[dict[str, Any]]) -> None:
        table = "stocks_intraday_forward_shadow_evaluations"
        if not DashboardData._table_exists(conn, table):
            return
        rows = conn.execute(
            f"SELECT * FROM {table} WHERE id IN (SELECT MAX(id) FROM {table} GROUP BY entry_mode) "
            "ORDER BY entry_mode"
        ).fetchall()
        for row in rows:
            raw_closed = int(row["clean_closed"] or 0) + int(row["dirty_closed"] or 0)
            raw_pnl = _float(row["net_pnl_usd"])
            raw_dirty_rows = int(row["dirty_rows"] or 0)
            raw_dirty_closed = int(row["dirty_closed"] or 0)
            raw_dirty_pnl = 0.0
            if DashboardData._table_exists(conn, "paper_shadow_execution_outcomes"):
                raw = conn.execute(
                    """
                    SELECT COUNT(*) AS closed, SUM(COALESCE(net_pnl_usdt, 0)) AS pnl,
                           SUM(CASE WHEN is_clean_for_edge = 0 THEN 1 ELSE 0 END) AS dirty_rows,
                           SUM(CASE WHEN is_clean_for_edge = 0 THEN 1 ELSE 0 END) AS dirty_closed,
                           SUM(CASE WHEN is_clean_for_edge = 0 THEN COALESCE(net_pnl_usdt, 0) ELSE 0 END) AS dirty_pnl
                      FROM paper_shadow_execution_outcomes
                     WHERE shadow_lane = 'stocks_intraday_forward'
                       AND entry_mode = ?
                       AND LOWER(COALESCE(outcome_status, '')) = 'closed'
                    """,
                    (row["entry_mode"],),
                ).fetchone()
                raw_closed = int(raw["closed"] or 0)
                raw_pnl = _float(raw["pnl"])
                raw_dirty_rows = int(raw["dirty_rows"] or 0)
                raw_dirty_closed = int(raw["dirty_closed"] or 0)
                raw_dirty_pnl = _float(raw["dirty_pnl"])
            target.append({
                "key": f"stocks:stocks_intraday:{row['entry_mode']}",
                "lane": f"stocks_intraday:{row['entry_mode']}", "asset_class": "stocks",
                "label": f"Stocks intraday {row['entry_mode']}",
                "forward_rows": int(row["forward_rows"] or 0),
                "raw_closed": raw_closed, "raw_pnl": raw_pnl,
                "clean_closed": int(row["clean_closed"] or 0),
                "dirty_rows": raw_dirty_rows,
                "dirty_closed": raw_dirty_closed,
                "dirty_pnl": raw_dirty_pnl, "unclassified_rows": 0,
                "unclassified_closed": 0, "unclassified_pnl": 0.0,
                "pnl": _float(row["net_pnl_usd"]), "fees": _float(row["fees_usd"]),
                "slippage": _float(row["slippage_usd"]), "winrate": row["winrate"],
                "profit_factor": row["profit_factor"], "verdict": str(row["verdict"]),
                "source": "evaluation", "rejections": _safe_json(row["reasons_json"]),
            })

    @staticmethod
    def _append_position_framework(conn: sqlite3.Connection, target: list[dict[str, Any]]) -> None:
        if not (DashboardData._table_exists(conn, "stocks_position_candidates") and
                DashboardData._table_exists(conn, "stocks_position_outcomes")):
            return
        row = conn.execute(
            """
            SELECT COUNT(*) AS forward_rows,
                   SUM(CASE WHEN COALESCE(o.status, '') IN ('closed', 'win', 'loss') THEN 1 ELSE 0 END) AS clean_closed,
                   SUM(CASE WHEN COALESCE(o.net_pnl_usd, 0) > 0 THEN 1 ELSE 0 END) AS wins,
                   SUM(COALESCE(o.net_pnl_usd, 0)) AS pnl
              FROM stocks_position_candidates c
         LEFT JOIN stocks_position_outcomes o ON o.candidate_id = c.candidate_id
            """
        ).fetchone()
        target.append({
            "key": "stocks:stocks_position_framework", "lane": "stocks_position_framework", "asset_class": "stocks",
            "label": "Stocks Position Framework", "forward_rows": int(row["forward_rows"] or 0),
            "raw_closed": int(row["clean_closed"] or 0), "raw_pnl": _float(row["pnl"]),
            "clean_closed": int(row["clean_closed"] or 0), "dirty_rows": 0,
            "dirty_closed": 0, "dirty_pnl": 0.0, "unclassified_rows": 0,
            "unclassified_closed": 0, "unclassified_pnl": 0.0,
            "pnl": _float(row["pnl"]), "fees": 0.0, "slippage": 0.0,
            "winrate": (int(row["wins"] or 0) / int(row["clean_closed"] or 1) * 100.0
                        if row["clean_closed"] else None),
            "verdict": "SHADOW_ONLY", "source": "position_framework", "rejections": {},
        })

    def shadow_lane_detail(self, lane: str, *, asset_class: str | None = None,
                           limit: int = 10) -> dict[str, Any]:
        summary = next((item for item in self.shadow_summary()["lanes"]
                        if item["lane"] == lane and item["asset_class"] == asset_class), None)
        result = {"summary": summary, "rows": []}
        if not summary:
            return result
        with self._connect() as conn:
            if lane == "shadow_derivreset_v3" and self._table_exists(conn, "crypto_derivreset_v3_shadow_outcomes"):
                rows = conn.execute(
                    "SELECT symbol, direction, decision_at, entry_ts, exit_ts, eligibility_status, rejection_reason, "
                    "outcome_status, net_pnl_usd, close_reason, is_clean_for_edge "
                    "FROM crypto_derivreset_v3_shadow_outcomes ORDER BY observed_at DESC LIMIT ?", (limit,)
                ).fetchall()
            elif lane == "shadow_catalyst_rs" and self._table_exists(conn, "stocks_catalyst_rs_shadow_outcomes"):
                rows = conn.execute(
                    "SELECT symbol, direction, decision_at, entry_ts, exit_ts, eligibility_status, rejection_reason, "
                    "outcome_status, net_pnl_usd, close_reason, is_clean_for_edge FROM stocks_catalyst_rs_shadow_outcomes "
                    "ORDER BY generated_at DESC LIMIT ?", (limit,)
                ).fetchall()
            elif lane.startswith("stocks_intraday:"):
                entry_mode = lane.split(":", 1)[1]
                rows = conn.execute(
                    "SELECT symbol, side AS direction, created_at AS decision_at, entry_fill_time AS entry_ts, "
                    "updated_at AS exit_ts, entry_fill_status AS eligibility_status, skipped_shadow_reason AS rejection_reason, "
                    "outcome_status, net_pnl_usdt AS net_pnl_usd, close_reason, is_clean_for_edge "
                    "FROM paper_shadow_execution_outcomes WHERE shadow_lane = 'stocks_intraday_forward' "
                    "AND entry_mode = ? ORDER BY updated_at DESC LIMIT ?", (entry_mode, limit),
                ).fetchall()
            else:
                params: list[Any] = [lane]
                where = "COALESCE(shadow_lane, 'ab_main') = ?"
                if asset_class:
                    where += " AND COALESCE(asset_class, 'crypto') = ?"
                    params.append(asset_class)
                params.append(limit)
                rows = conn.execute(
                    "SELECT symbol, side AS direction, created_at AS decision_at, entry_fill_time AS entry_ts, "
                    "updated_at AS exit_ts, entry_fill_status AS eligibility_status, skipped_shadow_reason AS rejection_reason, "
                    "outcome_status, net_pnl_usdt AS net_pnl_usd, close_reason, is_clean_for_edge "
                    f"FROM paper_shadow_execution_outcomes WHERE {where} "
                    "ORDER BY updated_at DESC LIMIT ?", params,
                ).fetchall()
            result["rows"] = [dict(row) for row in rows]
        return result

    def health_summary(self) -> dict[str, Any]:
        result: dict[str, Any] = {"freshness": [], "data_quality": [], "mexc_live": None}
        watched = (
            ("Paper", "paper_execution_outcomes", "computed_at"),
            ("Shadow A/B", "paper_shadow_execution_outcomes", "updated_at"),
            ("Deriv reset v3", "crypto_derivreset_v3_shadow_evaluations", "generated_at"),
            ("Catalyst RS", "stocks_catalyst_rs_shadow_evaluations", "generated_at"),
            ("Position scan", "stocks_position_scan_runs", "created_at"),
        )
        with self._connect() as conn:
            for label, table, column in watched:
                if self._table_exists(conn, table) and column in self._columns(conn, table):
                    row = conn.execute(f"SELECT MAX({column}) AS latest FROM {table}").fetchone()
                    result["freshness"].append({"label": label, "latest": row["latest"] if row else None})
            if self._table_exists(conn, "paper_shadow_execution_outcomes"):
                row = conn.execute(
                    "SELECT SUM(CASE WHEN is_clean_for_edge = 1 THEN 1 ELSE 0 END) AS clean, "
                    "SUM(CASE WHEN is_clean_for_edge = 0 THEN 1 ELSE 0 END) AS dirty, "
                    "SUM(CASE WHEN is_clean_for_edge IS NULL THEN 1 ELSE 0 END) AS unknown "
                    "FROM paper_shadow_execution_outcomes WHERE asset_class = 'stocks'"
                ).fetchone()
                result["data_quality"].append({"label": "Stocks shadow coverage", **dict(row)})
            if (self._table_exists(conn, "mexc_canary_decisions")
                    and self._table_exists(conn, "mexc_canary_outbox")):
                decision_counts = {
                    str(row[0]): int(row[1]) for row in conn.execute(
                        "SELECT state,COUNT(*) FROM mexc_canary_decisions GROUP BY state"
                    ).fetchall()
                }
                pending = int(conn.execute(
                    "SELECT COUNT(*) FROM mexc_canary_outbox WHERE status IN ('QUEUED','PROCESSING')"
                ).fetchone()[0] or 0)
                heartbeat = None
                if self._table_exists(conn, "mexc_canary_control"):
                    row = conn.execute(
                        "SELECT control_value,updated_at FROM mexc_canary_control "
                        "WHERE control_key='monitor_heartbeat'"
                    ).fetchone()
                    if row:
                        heartbeat = _safe_json(row[0])
                        heartbeat["updated_at"] = row[1]
                result["mexc_live"] = {
                    "pending": pending,
                    "submitted": int(decision_counts.get("SUBMITTED", 0)),
                    "rejected_preflight": int(decision_counts.get("REJECTED_PREFLIGHT", 0)),
                    "heartbeat": heartbeat,
                }
        return result
