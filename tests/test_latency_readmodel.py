"""Read-only latency read-model + DATA_GAP_LATE diagnostics (items 4 & 8). No network/live."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.signals import latency_readmodel as lr

NOW = datetime(2026, 7, 3, 12, 0, tzinfo=timezone.utc)


def _seed(tmp_path, rows, alerts=0):
    db = str(Path(tmp_path) / "lat.sqlite")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE entry_latency_audit (signal_id TEXT PRIMARY KEY, symbol TEXT, "
              "asset_class TEXT, mode TEXT, created_at TEXT, cause TEXT, data_gap_min REAL, "
              "recorded_latency_min REAL, computed_at TEXT)")
    c.execute("CREATE TABLE signal_alerts (alert_id TEXT PRIMARY KEY, alert_type TEXT)")
    for i, (sym, ac, mode, cause, gap, lat, days_ago) in enumerate(rows):
        created = (NOW - timedelta(days=days_ago)).isoformat()
        c.execute("INSERT INTO entry_latency_audit VALUES (?,?,?,?,?,?,?,?,?)",
                  (f"s{i}", sym, ac, mode, created, cause, gap, lat, NOW.isoformat()))
    for i in range(alerts):
        c.execute("INSERT INTO signal_alerts VALUES (?,?)", (f"a{i}", "late_shadow_route"))
    c.commit(); c.close()
    return db


def test_data_gap_diagnostics_stocks_intraday_warns_over_threshold(tmp_path):
    # 7 DATA_GAP_LATE of 10 stock-intraday signals → 70% > 30% → BLOCK warning
    rows = [("AAPL", "stocks", "intraday", "DATA_GAP_LATE", 120.0, 130.0, 1) for _ in range(4)]
    rows += [("MSFT", "stocks", "intraday", "DATA_GAP_LATE", 200.0, 210.0, 1) for _ in range(3)]
    rows += [("NVDA", "stocks", "intraday", "FAST", 5.0, 8.0, 1) for _ in range(3)]
    db = _seed(tmp_path, rows)
    dg = lr.data_gap_diagnostics(db, now=NOW)
    assert dg["available"] is True
    m = next(x for x in dg["by_mode"] if x["asset_class"] == "stocks" and x["mode"] == "intraday")
    assert m["data_gap_late"] == 7 and m["data_gap_late_share"] == 0.7
    assert m["recent_actionable_n"] == 10
    assert m["recent_actionable_data_gap_late_share"] == 0.7
    assert m["avg_data_gap_min"] is not None
    assert any("STOCKS INTRADAY promotion BLOCKED" in w for w in dg["warnings"])
    # top gap symbols surface AAPL (4) ahead of MSFT (3)
    assert dg["top_gap_symbols"][0][0] == "AAPL"
    # root cause hint points at rolling-window/coverage for ~2h gaps
    assert "ROLLING-WINDOW" in dg["root_cause_hint"] or "SCHEDULE" in dg["root_cause_hint"]


def test_data_gap_diagnostics_no_warning_when_low(tmp_path):
    rows = [("BTC/USDT", "crypto", "scalp", "FAST", 2.0, 3.0, 1) for _ in range(9)]
    rows += [("ETH/USDT", "crypto", "scalp", "DATA_GAP_LATE", 40.0, 50.0, 1)]
    db = _seed(tmp_path, rows)
    dg = lr.data_gap_diagnostics(db)
    m = next(x for x in dg["by_mode"] if x["asset_class"] == "crypto")
    assert m["data_gap_late_share"] == 0.1
    assert dg["warnings"] == []          # 10% < 30% and not stocks-intraday


def test_latency_summary_breakdown_and_recent_and_alerts(tmp_path):
    rows = [("AAPL", "stocks", "intraday", "DATA_GAP_LATE", 120.0, 130.0, 1),   # recent
            ("AAPL", "stocks", "intraday", "FAST", 5.0, 8.0, 1),                # recent
            ("AAPL", "stocks", "intraday", "LEGITIMATE_LATE", 10.0, 45.0, 40)]  # old (>7d)
    db = _seed(tmp_path, rows, alerts=3)
    s = lr.latency_summary(db, recent_days=7, now=NOW)
    assert s["available"] is True
    m = next(x for x in s["by_mode"] if x["mode"] == "intraday")
    assert m["all_time"]["by_cause"]["DATA_GAP_LATE"] == 1
    assert m["all_time"]["n"] == 3 and m["recent_7d"]["n"] == 2     # one row is older than 7d
    assert m["all_time"]["avg_recorded_latency_min"] is not None
    assert s["late_shadow_alerts"] == 3                              # signal_alerts late→shadow count


def test_latency_summary_separates_expected_waits_from_true_gaps(tmp_path):
    rows = [("BTC/USDT", "crypto", "swing", "DATA_GAP_LATE", 120.0, 130.0, 1),
            ("BTC/USDT", "crypto", "swing", "LEGITIMATE_LATE", 180.0, 180.0, 1)]
    db = _seed(tmp_path, rows)
    summary = lr.latency_summary(db, recent_days=7, now=NOW)
    mode = next(x for x in summary["by_mode"] if x["mode"] == "swing")
    assert mode["all_time"]["true_data_gap_n"] == 1
    assert mode["all_time"]["expected_wait_n"] == 1
    assert mode["all_time"]["avg_true_data_gap_min"] == 120.0


def test_latency_summary_excludes_historical_reconstruction_from_sla_average(tmp_path):
    rows = [("BTC/USDT", "crypto", "swing", "HISTORICAL_RECONSTRUCTION", 0.0, 900.0, 1),
            ("BTC/USDT", "crypto", "swing", "FAST", 1.0, 2.0, 1)]
    db = _seed(tmp_path, rows)
    c = sqlite3.connect(db)
    c.execute("ALTER TABLE entry_latency_audit ADD COLUMN latency_truth TEXT")
    c.execute("UPDATE entry_latency_audit SET latency_truth='historical_reconstruction' WHERE signal_id='s0'")
    c.execute("UPDATE entry_latency_audit SET latency_truth='point_in_time' WHERE signal_id='s1'")
    c.commit(); c.close()
    summary = lr.latency_summary(db, recent_days=7, now=NOW)
    mode = next(x for x in summary["by_mode"] if x["mode"] == "swing")
    assert mode["all_time"]["factual_latency_n"] == 1
    assert mode["all_time"]["historical_reconstruction_n"] == 1


def test_recent_actionable_gap_health_does_not_inherit_lifetime_warning(tmp_path):
    rows = [("AAPL", "stocks", "intraday", "DATA_GAP_LATE", 120.0, 130.0, 40)] * 4
    rows += [("MSFT", "stocks", "intraday", "FAST", 5.0, 8.0, 1) for _ in range(6)]
    db = _seed(tmp_path, rows)
    dg = lr.data_gap_diagnostics(db, recent_days=7, now=NOW)
    mode = next(x for x in dg["by_mode"] if x["asset_class"] == "stocks")
    assert mode["actionable_data_gap_late_share"] == 0.4  # lifetime history
    assert mode["recent_actionable_n"] == 6
    assert mode["recent_actionable_data_gap_late_share"] == 0.0
    assert any("promotion BLOCKED" in warning for warning in dg["warnings"])


def test_render_markdown_read_only(tmp_path):
    rows = [("AAPL", "stocks", "intraday", "DATA_GAP_LATE", 120.0, 130.0, 1) for _ in range(4)]
    rows += [("NVDA", "stocks", "intraday", "FAST", 5.0, 8.0, 1)]
    db = _seed(tmp_path, rows)
    md = lr.render_markdown(db)
    assert "Entry-latency read-model" in md
    assert "DATA_GAP_LATE" in md
    assert "read-only" in md.lower()
