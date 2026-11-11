from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

from src.execution.paper_operational_audit import build_report, render_markdown


NOW = datetime(2026, 8, 3, 12, 0, tzinfo=timezone.utc)


def _db(path):
    with sqlite3.connect(path) as conn:
        conn.executescript(
            """
            CREATE TABLE proposed_signals (
              signal_id TEXT, asset_class TEXT, mode TEXT, direction TEXT, symbol TEXT,
              tier TEXT, score REAL, setup_type TEXT
            );
            CREATE TABLE paper_portfolio_ledger (
              id INTEGER PRIMARY KEY, signal_id TEXT, event_type TEXT, exit_at TEXT,
              timestamp TEXT, net_pnl_usdt REAL, gross_pnl_usdt REAL, fees_usdt REAL,
              slippage_usdt REAL, funding_usdt REAL, fee_profile TEXT
            );
            CREATE TABLE paper_execution_outcomes (
              signal_id TEXT, evidence_class TEXT, execution_validity TEXT,
              lifecycle_state TEXT, paper_execution_outcome TEXT, entry_at TEXT,
              exit_at TEXT, decision_at TEXT, computed_at TEXT, paper_execution_r REAL
            );
            CREATE TABLE crypto_quality_overlay_decisions (
              signal_id TEXT, mode TEXT, quality_action TEXT, quality_reasons_json TEXT,
              computed_at TEXT
            );
            CREATE TABLE signal_alerts (
              asset_class TEXT, mode TEXT, telegram_status TEXT, payload_json TEXT,
              alert_type TEXT, sent_at TEXT
            );
            CREATE TABLE stocks_paper_decision_snapshots (
              funnel_state TEXT, decision_at TEXT
            );
            CREATE TABLE stocks_intraday_rth_revalidations (
              plan_signal_id TEXT, symbol TEXT, direction TEXT, session_open_at TEXT,
              decision TEXT, reasons_json TEXT, evaluated_at TEXT
            );
            CREATE TABLE mexc_canary_decisions (
              decision_id TEXT, captured_at TEXT, eligible INTEGER, state TEXT,
              rejection_reasons_json TEXT
            );
            CREATE TABLE mexc_canary_outbox (
              decision_id TEXT, status TEXT
            );
            CREATE TABLE mexc_canary_positions (
              status TEXT, risk_usdt REAL
            );
            CREATE TABLE mexc_canary_parity_outcomes (
              profile_id TEXT, net_pnl_usdt REAL, gross_pnl_usdt REAL,
              fees_usdt REAL, slippage_usdt REAL, funding_usdt REAL,
              updated_at TEXT, close_at TEXT, closed INTEGER, clean INTEGER,
              evidence_class TEXT
            );
            """
        )
        for idx, (pnl, side) in enumerate(((100, "long"), (-20, "long"), (5, "short"), (-5, "short")), 1):
            signal_id = f"c{idx}"
            conn.execute(
                "INSERT INTO proposed_signals VALUES(?,?,?,?,?,?,?,?)",
                (signal_id, "crypto", "swing", side, "BTC/USDT", "B", 70, "PULLBACK_LIMIT"),
            )
            conn.execute(
                "INSERT INTO paper_portfolio_ledger VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (idx, signal_id, "exit", "2026-08-02T12:00:00+00:00", None, pnl,
                 pnl + 2, 1, 1, 0, "bybit_non_vip_usdt_perp"),
            )
            conn.execute(
                "INSERT INTO paper_execution_outcomes VALUES(?,?,?,?,?,?,?,?,?,?)",
                (signal_id, "forward_postfreeze", "valid", "closed", "win" if pnl > 0 else "stop",
                 "2026-08-02T10:00:00+00:00", "2026-08-02T12:00:00+00:00",
                 "2026-08-02T10:00:00+00:00", "2026-08-02T12:00:00+00:00", pnl / 20),
            )
        conn.execute(
            "INSERT INTO paper_portfolio_ledger VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (99, "c1", "exit", "2026-08-02T12:00:00+00:00", None, 9999, 9999, 0, 0, 0, "zero"),
        )
        conn.execute("INSERT INTO proposed_signals VALUES(?,?,?,?,?,?,?,?)",
                     ("s1", "stocks", "intraday", "long", "AAPL", "B", 75, "BREAKOUT"))
        conn.execute(
            "INSERT INTO paper_portfolio_ledger VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (100, "s1", "exit", "2026-08-02T16:00:00+00:00", None, 12, 14, 1, 1, 0,
             "mexc_default_futures"),
        )
        conn.execute(
            "INSERT INTO paper_execution_outcomes VALUES(?,?,?,?,?,?,?,?,?,?)",
            ("s1", "forward_postfreeze", "valid", "CLOSED", "expired",
             "2026-08-02T14:00:00+00:00", "2026-08-02T16:00:00+00:00",
             "2026-08-02T14:00:00+00:00", "2026-08-02T16:00:00+00:00", 0.0),
        )
        conn.executemany(
            "INSERT INTO crypto_quality_overlay_decisions VALUES(?,?,?,?,?)",
            [
                ("c1", "swing", "HALF_SIZE", '["btc_regime_weak"]', "2026-08-02T10:00:00+00:00"),
                ("c1", "swing", "FULL_SIZE", "[]", "2026-08-02T11:00:00+00:00"),
                ("c2", "swing", "HALF_SIZE", '["funding_against"]', "2026-08-02T11:00:00+00:00"),
            ],
        )
        conn.execute(
            "INSERT INTO signal_alerts VALUES(?,?,?,?,?,?)",
            ("crypto", "swing", "late_shadow", json.dumps({
                "current_price_revalidated": False,
                "entry_time_basis": "historical_not_currently_executable",
                "cqo_reasons": ["btc_regime_weak"],
                "cqo_effective_paper_action": "HALF_SIZE",
                "paper_risk_floor_action": "HALF_SIZE",
                "paper_risk_floor_reason": "MODE_ISOLATED_L2",
                "size_weight": 0.5,
            }), "paper_entry", "2026-08-02T11:01:00+00:00"),
        )
        conn.execute("INSERT INTO stocks_paper_decision_snapshots VALUES(?,?)",
                     ("PREOPEN_PLAN", "2026-08-02T12:00:00+00:00"))
        conn.execute(
            "INSERT INTO stocks_intraday_rth_revalidations VALUES(?,?,?,?,?,?,?)",
            ("plan1", "AAPL", "long", "2026-08-02T13:30:00+00:00",
             "AWAITING_FRESH_RTH_CANDIDATE", '["no current candidate"]',
             "2026-08-02T13:50:00+00:00"),
        )
        conn.execute("INSERT INTO mexc_canary_decisions VALUES(?,?,?,?,?)", (
            "d1", "2026-08-02T11:01:02+00:00", 0, "REJECTED", '["ENTRY_TOO_OLD"]'))
        conn.execute("INSERT INTO mexc_canary_outbox VALUES(?,?)", ("d1", "REJECTED_PREFLIGHT"))
        conn.execute("INSERT INTO mexc_canary_positions VALUES(?,?)", ("OPEN", 5.0))
        conn.execute("INSERT INTO mexc_canary_parity_outcomes VALUES(?,?,?,?,?,?,?,?,?,?,?)", (
            "paper_equivalent", 4.0, 5.0, 0.4, 0.5, 0.1,
            "2026-08-02T12:00:00+00:00", "2026-08-02T12:00:00+00:00",
            1, 1, "forward_post_activation"))


def test_audit_uses_authoritative_asset_fee_profiles_and_concentration(tmp_path):
    path = tmp_path / "audit.sqlite"
    _db(path)
    report = build_report(path, recent_days=7, now=NOW)
    rows = {(r["asset_class"], r["mode"], r["direction"]): r for r in report["performance"]}
    assert rows[("crypto", "swing", "long")]["net_pnl_usdt"] == 80.0
    assert rows[("crypto", "swing", "long")]["fee_profile"] == "bybit_non_vip_usdt_perp"
    assert rows[("stocks", "intraday", "long")]["net_pnl_usdt"] == 12.0
    assert rows[("stocks", "intraday", "long")]["fee_profile"] == "mexc_default_futures"
    assert rows[("crypto", "swing", "long")]["top1_positive_pnl_share"] == 1.0


def test_audit_deduplicates_overlay_and_surfaces_routing_and_stocks_gap(tmp_path):
    path = tmp_path / "audit.sqlite"
    _db(path)
    report = build_report(path, recent_days=7, now=NOW)
    swing = next(row for row in report["overlay"] if row["mode"] == "swing")
    assert swing["unique_signals"] == 2
    assert swing["actions"] == {"FULL_SIZE": 1, "HALF_SIZE": 1}
    alert = report["alerts"][0]
    assert dict(alert["top_reasons"])["CURRENT_PRICE_NOT_REVALIDATED"] == 1
    assert alert["size_weights"] == {"0.5": 1}
    assert alert["overlay_actions"] == {"HALF_SIZE": 1}
    assert alert["guard_actions"] == {"HALF_SIZE": 1}
    assert report["stocks_funnel"]["snapshots"] == {"PREOPEN_PLAN": 1}
    assert len(report["stocks_funnel"]["pending_plans"]) == 1
    assert report["mexc_handoff"]["rejection_reasons"] == [("ENTRY_TOO_OLD", 1)]
    assert report["mexc_handoff"]["open_risk_usdt"] == 5.0
    assert report["mexc_handoff"]["parity"][0]["net_pnl_usdt"] == 4.0
    assert "STOCKS_PLANS_AWAITING_FRESH_RTH:1" in report["warnings"]
    reconciliation = report["stocks_ledger_reconciliation"]
    assert reconciliation["available"] is True
    assert reconciliation["actionable_closed"] == 1
    assert reconciliation["ledger_present"] == 1
    assert reconciliation["expected_ledger_missing"] == 0


def test_stocks_reconciliation_recognizes_deduplicated_economic_trade(tmp_path):
    path = tmp_path / "audit.sqlite"
    _db(path)
    with sqlite3.connect(path) as conn:
        conn.execute("ALTER TABLE paper_execution_outcomes ADD COLUMN economic_trade_key TEXT")
        conn.execute("ALTER TABLE paper_portfolio_ledger ADD COLUMN economic_trade_key TEXT")
        conn.execute(
            "UPDATE paper_portfolio_ledger SET economic_trade_key='AAPL|stocks|intraday|long|A|breakout|1|2026-08-02' "
            "WHERE signal_id='s1'"
        )
        conn.execute(
            "UPDATE paper_execution_outcomes SET economic_trade_key='AAPL|stocks|intraday|long|A|breakout|1|2026-08-02' "
            "WHERE signal_id='s1'"
        )
        conn.execute(
            "INSERT INTO proposed_signals VALUES(?,?,?,?,?,?,?,?)",
            ("s2", "stocks", "intraday", "long", "AAPL", "A", 80, "BREAKOUT"),
        )
        conn.execute(
            "INSERT INTO paper_execution_outcomes("
            "signal_id,evidence_class,execution_validity,lifecycle_state,paper_execution_outcome,"
            "entry_at,exit_at,decision_at,computed_at,paper_execution_r,economic_trade_key"
            ") VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            ("s2", "forward_postfreeze", "valid", "CLOSED", "expired",
             "2026-08-02T14:05:00+00:00", "2026-08-02T16:00:00+00:00",
             "2026-08-02T14:05:00+00:00", "2026-08-02T16:00:00+00:00", 0.0,
             "AAPL|stocks|intraday|long|A|breakout|1|2026-08-02"),
        )
    report = build_report(path, recent_days=7, now=NOW)
    reconciliation = report["stocks_ledger_reconciliation"]
    assert reconciliation["actionable_closed"] == 2
    assert reconciliation["ledger_present"] == 1
    assert reconciliation["deduplicated_equivalent"] == 1
    assert reconciliation["expected_ledger_missing"] == 0


def test_audit_is_read_only_and_markdown_is_human_readable(tmp_path):
    path = tmp_path / "audit.sqlite"
    _db(path)
    with sqlite3.connect(path) as conn:
        before = conn.total_changes, conn.execute("SELECT COUNT(*) FROM proposed_signals").fetchone()[0]
    report = build_report(path, recent_days=7, now=NOW)
    text = render_markdown(report)
    with sqlite3.connect(path) as conn:
        after = conn.total_changes, conn.execute("SELECT COUNT(*) FROM proposed_signals").fetchone()[0]
    assert before == after
    assert "Authoritative net USD" in text
    assert "Stocks funnel" in text
    assert "MEXC handoff" in text
