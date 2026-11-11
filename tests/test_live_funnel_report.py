from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

from src.live_execution import funnel_report


NOW = datetime(2026, 8, 15, 12, tzinfo=timezone.utc)


def test_live_funnel_report_counts_handoff_stages(tmp_path):
    db = tmp_path / "funnel.sqlite"
    conn = sqlite3.connect(db)
    conn.executescript("""
        CREATE TABLE proposed_signals(
            signal_id TEXT PRIMARY KEY, asset_class TEXT, mode TEXT, created_at TEXT
        );
        CREATE TABLE signal_alerts(
            alert_id TEXT PRIMARY KEY, signal_id TEXT, asset_class TEXT, mode TEXT,
            telegram_status TEXT, sent_at TEXT, alert_type TEXT
        );
        CREATE TABLE mexc_canary_decisions(
            decision_id TEXT PRIMARY KEY, signal_id TEXT, captured_at TEXT, paper_alert_id TEXT,
            symbol TEXT, mode TEXT, entry_mode TEXT, eligible INTEGER, state TEXT,
            rejection_reasons_json TEXT, decision_json TEXT, decision_hash TEXT, config_hash TEXT,
            decision_context_type TEXT
        );
        CREATE TABLE mexc_canary_outbox(
            outbox_id TEXT PRIMARY KEY, decision_id TEXT, created_at TEXT, available_at TEXT,
            status TEXT, attempt_count INTEGER
        );
        CREATE TABLE mexc_canary_orders(
            order_row_id TEXT PRIMARY KEY, decision_id TEXT, external_oid TEXT,
            exchange_order_id TEXT, symbol TEXT, status TEXT, submitted_at TEXT,
            updated_at TEXT, plan_json TEXT
        );
    """)
    conn.execute("INSERT INTO proposed_signals VALUES (?,?,?,?)",
                 ("sig1", "crypto", "swing", "2026-08-15T11:00:00+00:00"))
    conn.execute("INSERT INTO signal_alerts VALUES (?,?,?,?,?,?,?)",
                 ("a1", "sig1", "crypto", "swing", "sent", "2026-08-15T11:01:00+00:00", "paper_entry"))
    conn.execute("INSERT INTO signal_alerts VALUES (?,?,?,?,?,?,?)",
                 ("a2", "sig1", "crypto", "swing", "sent", "2026-08-15T11:04:00+00:00", "close_expired"))
    conn.execute("INSERT INTO mexc_canary_decisions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                 ("d1", "sig1", "2026-08-15T11:02:00+00:00", "a1", "BTC_USDT",
                  "swing", "PULLBACK_LIMIT", 0, "REJECTED", json.dumps(["ENTRY_TOO_OLD"]),
                  "{}", "h", "cfg", "point_in_time"))
    conn.execute("INSERT INTO mexc_canary_outbox VALUES (?,?,?,?,?,?)",
                 ("o1", "d1", "2026-08-15T11:02:00+00:00",
                  "2026-08-15T11:02:00+00:00", "QUEUED", 0))
    conn.execute("INSERT INTO mexc_canary_orders VALUES (?,?,?,?,?,?,?,?,?)",
                 ("ord1", "d1", "x", "ex", "BTC_USDT", "SUBMITTED",
                  "2026-08-15T11:03:00+00:00", "2026-08-15T11:03:00+00:00", "{}"))
    conn.commit()
    conn.close()

    report = funnel_report.build_report(db=db, now=NOW, hours=24)
    assert report["proposed"][0]["n"] == 1
    assert report["alerts"][0]["telegram_status"] == "sent"
    assert report["alerts"][0]["n"] == 1
    assert report["close_alerts"] == [{
        "asset_class": "crypto", "mode": "swing", "alert_type": "close_expired",
        "telegram_status": "sent", "n": 1,
    }]
    assert report["mexc_decisions"][0]["state"] == "REJECTED"
    assert report["mexc_rejection_reasons"] == [{"reason": "ENTRY_TOO_OLD", "n": 1}]
    assert report["mexc_outbox"][0]["status"] == "QUEUED"
    assert report["mexc_orders"][0]["status"] == "SUBMITTED"
    assert "ENTRY_TOO_OLD" in funnel_report.render_markdown(report)
    rendered = funnel_report.render_markdown(report)
    assert "## Paper Entry Alerts" in rendered
    assert "## Close Alerts" in rendered
