from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from typing import Any

from .schemas import parse_utc
from .store import record_post_trade_diagnostic, table_exists


def _number(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


@dataclass(frozen=True)
class ForensicFinding:
    outcome: str
    primary_category: str
    secondary_categories: tuple[str, ...]
    evidence: dict[str, Any]


class PostTradeForensicsAgent:
    name = "post_trade_forensics"
    version = "post_trade_forensics_v1"

    def classify(self, row: dict[str, Any], market_codes: list[str]) -> ForensicFinding:
        result_r = _number(row.get("result_r"))
        result_usdt = _number(row.get("result_usdt"))
        close_reason = str(row.get("close_reason") or "").lower()
        validity = str(row.get("execution_validity") or "valid").lower()
        touch_r = _number(row.get("touch_r"))
        entry_drift_bps = _number(row.get("entry_drift_bps"))
        secondary: list[str] = []
        if validity not in {"", "valid"}:
            primary = "execution_error"
            outcome = "invalid"
        elif result_r is None and result_usdt is None:
            primary = "unresolved_outcome"
            outcome = "unknown"
        else:
            positive = (result_r is not None and result_r > 0) or (
                result_r is None and result_usdt is not None and result_usdt > 0
            )
            negative = (result_r is not None and result_r < 0) or (
                result_r is None and result_usdt is not None and result_usdt < 0
            )
            outcome = "win" if positive else "loss" if negative else "scratch"
            if outcome == "win":
                primary = "normal_win"
            elif outcome == "scratch":
                primary = "normal_scratch"
            elif entry_drift_bps is not None and abs(entry_drift_bps) >= 75:
                primary = "late_entry"
            elif "original_stop" in close_reason and touch_r is not None and touch_r >= 0.6:
                primary = "stop_too_tight_hypothesis"
            elif "MARKET_DIRECTION_CONFLICT" in market_codes:
                primary = "regime_conflict"
            elif any(token in close_reason for token in ("protection_error", "tpsl_error", "failsafe")):
                primary = "protection_error"
            else:
                primary = "normal_loss"
        if bool(row.get("giveback")):
            secondary.append("profit_giveback")
        if bool(row.get("same_candle_ambiguous")):
            secondary.append("same_candle_ambiguous")
        if "NEWS_DIRECTION_CONFLICT" in market_codes:
            secondary.append("news_conflict")
        evidence = {
            "close_reason": close_reason,
            "execution_validity": validity,
            "touch_r": touch_r,
            "entry_drift_bps": entry_drift_bps,
            "market_reason_codes": market_codes,
            "giveback": bool(row.get("giveback")),
            "same_candle_ambiguous": bool(row.get("same_candle_ambiguous")),
        }
        return ForensicFinding(outcome, primary, tuple(secondary), evidence)

    @staticmethod
    def _latest_reason_codes(conn: sqlite3.Connection, signal_id: str) -> list[str]:
        if not table_exists(conn, "quality_agent_signal_verdicts"):
            return []
        rows = conn.execute(
            "SELECT reason_codes_json FROM quality_agent_signal_verdicts "
            "WHERE signal_id=? AND agent_name IN ('market_regime','news_entity') "
            "ORDER BY created_at DESC LIMIT 4", (signal_id,),
        ).fetchall()
        codes: list[str] = []
        for row in rows:
            try:
                codes.extend(json.loads(row[0] or "[]"))
            except (TypeError, json.JSONDecodeError):
                continue
        return list(dict.fromkeys(str(code) for code in codes))

    def refresh(self, conn: sqlite3.Connection) -> dict[str, int]:
        paper = live = 0
        if table_exists(conn, "paper_execution_outcomes") and table_exists(conn, "proposed_signals"):
            ledger_expr = (
                "(SELECT l.net_pnl_usdt FROM paper_portfolio_ledger l "
                "WHERE l.signal_id=p.signal_id AND l.event_type='exit' ORDER BY l.rowid DESC LIMIT 1)"
                if table_exists(conn, "paper_portfolio_ledger") else "NULL"
            )
            rows = [dict(row) for row in conn.execute(
                "SELECT p.signal_id,p.asset_class,p.mode,"
                "COALESCE(o.paper_execution_entry_mode,p.entry_type) AS entry_mode,"
                "o.paper_execution_r AS result_r," + ledger_expr + " AS result_usdt,"
                "o.close_reason,o.execution_validity,o.touch_r,o.entry_drift_bps,o.giveback,"
                "o.same_candle_ambiguous,o.exit_at,o.computed_at "
                "FROM paper_execution_outcomes o JOIN proposed_signals p ON p.signal_id=o.signal_id "
                "WHERE o.paper_execution_r IS NOT NULL AND o.close_reason NOT IN ('open','no_entry')"
            ).fetchall()]
            for row in rows:
                codes = self._latest_reason_codes(conn, str(row["signal_id"]))
                finding = self.classify(row, codes)
                record_post_trade_diagnostic(
                    conn, signal_id=str(row["signal_id"]), source_book="paper",
                    outcome_payload=row, asset_class=row.get("asset_class"), mode=row.get("mode"),
                    entry_mode=row.get("entry_mode"), outcome=finding.outcome,
                    result_r=_number(row.get("result_r")), result_usdt=_number(row.get("result_usdt")),
                    primary_category=finding.primary_category,
                    secondary_categories=finding.secondary_categories, evidence=finding.evidence,
                    agent_version=self.version,
                    created_at=parse_utc(row.get("exit_at") or row.get("computed_at")),
                )
                paper += 1

        if table_exists(conn, "mexc_canary_positions") and table_exists(conn, "mexc_canary_decisions"):
            rows = [dict(row) for row in conn.execute(
                "SELECT d.signal_id,d.mode,d.entry_mode,d.decision_json,p.realized_pnl_usdt AS result_usdt,"
                "p.risk_usdt,p.closed_at,p.exchange_json FROM mexc_canary_positions p "
                "JOIN mexc_canary_decisions d ON d.decision_id=p.decision_id "
                "WHERE p.status='CLOSED' AND p.closed_at IS NOT NULL"
            ).fetchall()]
            for row in rows:
                try:
                    decision = json.loads(row.get("decision_json") or "{}")
                except (TypeError, json.JSONDecodeError):
                    decision = {}
                risk = _number(row.get("risk_usdt"))
                pnl = _number(row.get("result_usdt"))
                result_r = pnl / risk if pnl is not None and risk and risk > 0 else None
                normalized = {
                    **row, "result_r": result_r,
                    "asset_class": decision.get("asset_class"),
                    "close_reason": "live_exchange_close",
                    "execution_validity": "valid",
                }
                codes = self._latest_reason_codes(conn, str(row["signal_id"]))
                finding = self.classify(normalized, codes)
                record_post_trade_diagnostic(
                    conn, signal_id=str(row["signal_id"]), source_book="live",
                    outcome_payload=normalized, asset_class=normalized.get("asset_class"),
                    mode=row.get("mode"), entry_mode=row.get("entry_mode"), outcome=finding.outcome,
                    result_r=result_r, result_usdt=pnl, primary_category=finding.primary_category,
                    secondary_categories=finding.secondary_categories, evidence=finding.evidence,
                    agent_version=self.version,
                    created_at=parse_utc(row.get("closed_at")),
                )
                live += 1
        return {"paper_rows_seen": paper, "live_rows_seen": live}


__all__ = ["ForensicFinding", "PostTradeForensicsAgent"]
