"""Latency SLA report (read-only, 2026-07-05). Market-wait vs SYSTEM latency split, sent-only,
DATA_GAP_LATE share, SLA flags. No live."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.signals import latency_sla as sla

NOW = datetime(2026, 7, 5, 12, 5, tzinfo=timezone.utc)


def _seed(tmp_path, *, signals=(), outcomes=(), ela=(), telemetry=()):
    db = str(Path(tmp_path) / "sla.sqlite")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, mode TEXT, "
              "asset_class TEXT, created_at TEXT)")
    c.execute("CREATE TABLE signal_outcomes (signal_id TEXT, entry_triggered INTEGER, "
              "entry_triggered_at TEXT)")
    c.execute("CREATE TABLE entry_latency_audit (signal_id TEXT, symbol TEXT, asset_class TEXT, "
              "mode TEXT, cause TEXT, data_gap_min REAL, recorded_latency_min REAL, created_at TEXT)")
    for s in signals:
        c.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?)", s)
    for o in outcomes:
        c.execute("INSERT INTO signal_outcomes VALUES (?,?,?)", o)
    for r in ela:
        c.execute("INSERT INTO entry_latency_audit VALUES (?,?,?,?,?,?,?,?)", r)
    c.commit(); c.close()
    if telemetry:
        from src.signals import latency_telemetry as t
        for ev in telemetry:
            t.emit(db, **ev)
    return db


def test_market_wait_vs_system_latency_split(tmp_path):
    # signal created 10:00, entry at 12:00 → market wait 7200s (price action, NOT SLA).
    # detected at 12:00:05 (system detect ~5s), alert sent at 12:00:06 (dispatch ~1s).
    c0 = datetime(2026, 7, 5, 10, 0, tzinfo=timezone.utc)
    entry = datetime(2026, 7, 5, 12, 0, tzinfo=timezone.utc)
    db = _seed(
        tmp_path,
        signals=[("s1", "BTC/USDT", "intraday", "crypto", c0.isoformat())],
        outcomes=[("s1", 1, entry.isoformat())],
        telemetry=[
            {"event_type": "entry_condition_detected", "signal_id": "s1", "asset_class": "crypto",
             "mode": "intraday", "source": "pending-monitor", "latency_from_entry_touch_sec": 5.0,
             "event_at": (entry + timedelta(seconds=5)).isoformat()},
            {"event_type": "paper_entry_alert_sent", "signal_id": "s1", "asset_class": "crypto",
             "mode": "intraday", "source": "pending-monitor", "latency_from_entry_touch_sec": 6.0,
             "event_at": (entry + timedelta(seconds=6)).isoformat()},
        ])
    r = sla.sla_report(db, recent_days=14, now=NOW)
    assert r["market_wait_sec"]["p50"] == 7200.0            # market wait is huge …
    assert r["plan_age_to_entry_sec"] == r["market_wait_sec"]
    assert r["system_detection_sec"]["p50"] == 5.0          # … but SYSTEM detect is ~5s
    assert r["entry_to_alert_sec"]["p50"] == 6.0
    m = next(x for x in r["by_mode"] if x["mode"] == "crypto intraday")
    assert m["alert_dispatch_sec"]["p50"] == 1.0            # detected→sent ~1s
    # The 7200s market wait must NOT produce an SLA breach.
    assert not any("7200" in b or "market" in b.lower() for b in r["sla_breaches"])
    assert r["approx_from_candle_timestamp"] is True


def test_mexc_capture_latency_uses_detection_not_later_telegram_send(tmp_path):
    entry = datetime(2026, 7, 5, 12, 0, tzinfo=timezone.utc)
    db = _seed(tmp_path, telemetry=[
        {"event_type": "entry_condition_detected", "signal_id": "mx1", "asset_class": "crypto",
         "mode": "swing", "source": "pending-monitor",
         "event_at": (entry + timedelta(seconds=5)).isoformat()},
        {"event_type": "mexc_decision_captured", "signal_id": "mx1", "asset_class": "crypto",
         "mode": "swing", "source": "mexc-live",
         "event_at": (entry + timedelta(seconds=6)).isoformat()},
        # Telegram can be slow without making the execution handoff slow.
        {"event_type": "paper_entry_alert_sent", "signal_id": "mx1", "asset_class": "crypto",
         "mode": "swing", "source": "pending-monitor",
         "event_at": (entry + timedelta(seconds=40)).isoformat()},
    ])
    report = sla.sla_report(db, recent_days=14, now=NOW)
    assert report["detect_to_mexc_capture_sec"] == {
        "n": 1, "p50": 1.0, "p90": 1.0, "p95": 1.0, "max": 1.0,
    }
    assert report["paper_to_mexc_capture_sec"] == report["detect_to_mexc_capture_sec"]


def test_alert_acceptance_is_forward_only_after_fast_path_activation(tmp_path, monkeypatch):
    cutover = datetime(2026, 8, 3, 16, 25, tzinfo=timezone.utc)
    events = []
    for i in range(10):
        detected = cutover - timedelta(hours=1, seconds=i)
        events.extend([
            {"event_type": "entry_condition_detected", "signal_id": f"old{i}",
             "asset_class": "crypto", "mode": "intraday", "source": "pending-monitor",
             "latency_from_entry_touch_sec": 2.0, "event_at": detected.isoformat(),
             "current_price_revalidated": True, "entry_time_basis": "point_in_time_current_bar",
             "note": "system_latency_basis=current_revalidation"},
            {"event_type": "paper_entry_alert_sent", "signal_id": f"old{i}",
             "asset_class": "crypto", "mode": "intraday", "source": "pending-monitor",
             "event_at": (detected + timedelta(seconds=45)).isoformat()},
        ])
    db = _seed(tmp_path, telemetry=events)
    cfg = dict(sla._DEFAULT_SLA)
    cfg["alert_fast_path_activated_at"] = cutover.isoformat()
    monkeypatch.setattr(sla, "_sla_cfg", lambda: cfg)
    report = sla.sla_report(db, recent_days=7, now=cutover + timedelta(hours=1))
    acceptance = report["acceptance"]["crypto"]
    assert acceptance["verdict"] == "INSUFFICIENT_SAMPLE"
    assert acceptance["sent_alerts"] == 0
    assert not any("detect-to-alert dispatch" in reason for reason in acceptance["breaches"])
    assert report["alert_fast_path_activated_at"] == cutover.isoformat()


def test_duplicate_and_skipped_excluded_from_sent_latency(tmp_path):
    entry = datetime(2026, 7, 5, 12, 0, tzinfo=timezone.utc)
    db = _seed(
        tmp_path,
        signals=[("s1", "BTC/USDT", "intraday", "crypto", "2026-07-05T11:00:00+00:00")],
        outcomes=[("s1", 1, entry.isoformat())],
        telemetry=[
            # two SENT rows for the same signal (a race) + a skipped row → dedup to ONE sent
            {"event_type": "paper_entry_alert_sent", "signal_id": "s1", "asset_class": "crypto",
             "mode": "intraday", "source": "pending-monitor", "latency_from_entry_touch_sec": 6.0,
             "event_at": (entry + timedelta(seconds=6)).isoformat()},
            {"event_type": "paper_entry_alert_sent", "signal_id": "s1", "asset_class": "crypto",
             "mode": "intraday", "source": "pending-monitor", "latency_from_entry_touch_sec": 99.0,
             "event_at": (entry + timedelta(seconds=200)).isoformat()},
            {"event_type": "paper_entry_alert_skipped", "signal_id": "s1", "asset_class": "crypto",
             "mode": "intraday", "source": "pending-monitor", "latency_from_entry_touch_sec": 500.0,
             "event_at": (entry + timedelta(seconds=500)).isoformat()},
        ])
    r = sla.sla_report(db, recent_days=14, now=NOW)
    assert r["entry_to_alert_sec"]["n"] == 1                # only ONE sent counted (earliest)
    assert r["entry_to_alert_sec"]["p50"] == 6.0           # skipped/dup 99/500 excluded
    assert r["sent_alert_events"] == 1


def test_stocks_intraday_data_gap_blocked_flag(tmp_path):
    ela = [(f"g{i}", "AAPL", "stocks", "intraday", "DATA_GAP_LATE", 120.0, 130.0, NOW.isoformat())
           for i in range(7)]
    ela += [(f"f{i}", "MSFT", "stocks", "intraday", "FAST", 3.0, 5.0, NOW.isoformat()) for i in range(3)]
    db = _seed(tmp_path, ela=ela)
    r = sla.sla_report(db, now=NOW)
    assert "STOCKS_INTRADAY_DATA_GAP_BLOCKED" in r["flags"]
    assert "LIVE_BLOCKED_UNTIL_LATENCY_SLA" in r["flags"]
    m = next(x for x in r["by_mode"] if x["mode"] == "stocks intraday")
    assert m["data_gap_late_share"] == 0.7


def test_insufficient_forward_telemetry_when_no_events(tmp_path):
    # market wait present, but NO telemetry → cannot judge system SLA
    db = _seed(tmp_path,
               signals=[("s1", "BTC/USDT", "intraday", "crypto", "2026-07-05T11:00:00+00:00")],
               outcomes=[("s1", 1, "2026-07-05T12:00:00+00:00")])
    r = sla.sla_report(db, now=NOW)
    assert r["insufficient_forward_telemetry"] is True
    assert "INSUFFICIENT_FORWARD_TELEMETRY" in r["flags"]
    # no crypto SYSTEM-latency breach can be asserted from market wait alone
    assert not any("SYSTEM detect" in b for b in r["sla_breaches"])


def test_render_markdown_read_only(tmp_path):
    db = _seed(tmp_path,
               signals=[("s0", "BTC/USDT", "intraday", "crypto", "2026-07-05T11:00:00+00:00")],
               outcomes=[("s0", 1, "2026-07-05T12:00:00+00:00")])
    md = sla.render_markdown(db)
    assert "Latency SLA report" in md and "read-only" in md.lower()
    assert "PLAN AGE" in md and "SYSTEM" in md
    assert "LIVE_BLOCKED_UNTIL_LATENCY_SLA" in md


def test_crypto_and_stocks_acceptance_are_independent_and_bar_bounded(tmp_path):
    base = datetime(2026, 7, 5, 11, 0, tzinfo=timezone.utc)
    events = []
    for i in range(20):
        sid = f"c{i}"
        detected_at = base + timedelta(seconds=i * 10)
        events.append({
            "event_type": "entry_condition_detected", "signal_id": sid,
            "asset_class": "crypto", "mode": "scalp", "source": "pending-monitor",
            "latency_from_entry_touch_sec": 150.0, "event_at": detected_at.isoformat(),
            "note": "entry_bar_timeframe=5m",
        })
        if i < 10:
            events.append({
                "event_type": "paper_entry_alert_sent", "signal_id": sid,
                "asset_class": "crypto", "mode": "scalp", "source": "pending-monitor",
                "latency_from_entry_touch_sec": 152.0,
                "event_at": (detected_at + timedelta(seconds=2)).isoformat(),
                "note": "entry_bar_timeframe=5m",
            })
    for i in range(20):
        sid = f"st{i}"
        detected_at = base + timedelta(minutes=10, seconds=i * 10)
        events.append({
            "event_type": "entry_condition_detected", "signal_id": sid,
            "asset_class": "stocks", "mode": "intraday", "source": "stocks-monitor-session",
            "latency_from_entry_touch_sec": 1300.0, "event_at": detected_at.isoformat(),
            "note": "entry_bar_timeframe=15m",
        })
        if i < 5:
            events.append({
                "event_type": "paper_entry_alert_sent", "signal_id": sid,
                "asset_class": "stocks", "mode": "intraday", "source": "stocks-monitor-session",
                "latency_from_entry_touch_sec": 1302.0,
                "event_at": (detected_at + timedelta(seconds=2)).isoformat(),
                "note": "entry_bar_timeframe=15m",
            })
    db = _seed(tmp_path, telemetry=events)
    r = sla.sla_report(db, recent_days=14, now=NOW)
    assert r["acceptance"]["crypto"]["verdict"] == "PASS"
    assert r["acceptance"]["crypto"]["after_bar_close_lower_bound_sec"]["p90"] == 0.0
    assert r["acceptance"]["stocks_intraday"]["verdict"] == "SLA_BREACH"
    assert r["acceptance"]["stocks_intraday"]["after_bar_close_lower_bound_sec"]["p90"] == 400.0


def test_acceptance_requires_the_fast_monitor_source(tmp_path):
    events = [{
        "event_type": "entry_condition_detected", "signal_id": f"c{i}",
        "asset_class": "crypto", "mode": "scalp", "source": "track-signals",
        "latency_from_entry_touch_sec": 30.0,
        "event_at": (NOW - timedelta(minutes=1, seconds=i)).isoformat(),
        "note": "entry_bar_timeframe=5m",
    } for i in range(20)]
    db = _seed(tmp_path, telemetry=events)
    r = sla.sla_report(db, recent_days=14, now=NOW)
    acc = r["acceptance"]["crypto"]
    assert acc["verdict"] == "SLA_BREACH"
    assert any("fast-source pending-monitor" in reason for reason in acc["breaches"])


def test_stock_acceptance_uses_live_ab_cohort_not_c_tier(tmp_path, monkeypatch):
    base = NOW - timedelta(minutes=2)
    signals = []
    events = []
    for i in range(20):
        sid = f"live{i}"
        signals.append((sid, f"S{i}", "intraday", "stocks", base.isoformat()))
        detected_at = base + timedelta(seconds=i)
        events.append({
            "event_type": "entry_condition_detected", "signal_id": sid,
            "asset_class": "stocks", "mode": "intraday",
            "source": "stocks-monitor-session", "latency_from_entry_touch_sec": 2.0,
            "event_at": detected_at.isoformat(), "current_price_revalidated": True,
            "entry_time_basis": "point_in_time_current_bar",
            "note": "entry_bar_timeframe=15m; system_latency_basis=current_revalidation",
        })
        if i < 5:
            events.append({
                "event_type": "paper_entry_alert_sent", "signal_id": sid,
                "asset_class": "stocks", "mode": "intraday",
                "source": "stocks-monitor-session",
                "event_at": (detected_at + timedelta(seconds=1)).isoformat(),
            })
    for i in range(18):
        sid = f"nonlive{i}"
        signals.append((sid, f"C{i}", "intraday", "stocks", base.isoformat()))
        events.append({
            "event_type": "entry_condition_detected", "signal_id": sid,
            "asset_class": "stocks", "mode": "intraday", "source": "track-signals",
            "latency_from_entry_touch_sec": 120.0,
            "event_at": (base + timedelta(seconds=30 + i)).isoformat(),
            "current_price_revalidated": True,
            "entry_time_basis": "point_in_time_current_bar",
            "note": "entry_bar_timeframe=15m; system_latency_basis=current_revalidation",
        })
    db = _seed(tmp_path, signals=signals, telemetry=events)
    c = sqlite3.connect(db)
    c.execute("ALTER TABLE proposed_signals ADD COLUMN tier TEXT")
    c.executemany("UPDATE proposed_signals SET tier=? WHERE signal_id=?",
                  [("A" if i % 2 == 0 else "B", f"live{i}") for i in range(20)])
    c.executemany("UPDATE proposed_signals SET tier='C' WHERE signal_id=?",
                  [(f"nonlive{i}",) for i in range(18)])
    c.commit()
    c.close()
    monkeypatch.setattr(sla, "_sla_cfg", lambda: dict(sla._DEFAULT_SLA))

    report = sla.sla_report(db, recent_days=14, now=NOW)
    acc = report["acceptance"]["stocks_intraday"]
    assert acc["verdict"] == "PASS"
    assert acc["acceptance_detection_sec"]["n"] == 20
    assert acc["fast_source_share"] == 1.0
    assert acc["non_live_tier_excluded"] == 18


def test_legacy_revalidated_first_touch_does_not_create_fake_swing_breach(tmp_path):
    events = []
    for i in range(20):
        events.append({
            "event_type": "entry_condition_detected", "signal_id": f"old{i}",
            "asset_class": "crypto", "mode": "swing", "source": "pending-monitor",
            "latency_from_entry_touch_sec": 13_200.0,
            "current_price_revalidated": True,
            "entry_time_basis": "point_in_time_current_bar",
            "event_at": (NOW - timedelta(minutes=2, seconds=i)).isoformat(),
            "note": "entry_bar_timeframe=1h; entry_touch_time_basis=lower_tf_1m_first_touch",
        })
    for i in range(5):
        events.append({
            "event_type": "entry_condition_detected", "signal_id": f"new{i}",
            "asset_class": "crypto", "mode": "swing", "source": "pending-monitor",
            "latency_from_entry_touch_sec": 2.0,
            "current_price_revalidated": True,
            "entry_time_basis": "point_in_time_current_bar",
            "event_at": (NOW - timedelta(minutes=1, seconds=i)).isoformat(),
            "note": "entry_bar_timeframe=1h; system_latency_basis=current_revalidation",
        })
    for i in range(20):
        events.append({
            "event_type": "entry_condition_detected", "signal_id": f"invalid{i}",
            "asset_class": "crypto", "mode": "swing", "source": "pending-monitor",
            "latency_from_entry_touch_sec": 31_680.0,
            "current_price_revalidated": False,
            "entry_time_basis": "current_price_invalidated",
            "event_at": (NOW - timedelta(minutes=3, seconds=i)).isoformat(),
            "note": "entry_bar_timeframe=1h; entry_touch_time_basis=lower_tf_1m_first_touch",
        })
    db = _seed(tmp_path, telemetry=events)
    acc = sla.sla_report(db, recent_days=14, now=NOW)["acceptance"]["crypto"]
    assert acc["legacy_revalidation_excluded"] == 20
    assert acc["non_actionable_unrevalidated_excluded"] == 20
    assert acc["point_in_time_detect_sec"]["n"] == 5
    assert acc["raw_touch_to_detect_sec"]["n"] == 45
    assert acc["verdict"] == "INSUFFICIENT_SAMPLE"
    assert not acc["breaches"]
