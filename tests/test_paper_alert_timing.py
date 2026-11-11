"""Paper-entry alert timing + latency-module guardrails (2026-07-05).

Item 8: the paper-entry alert must be dispatched in the SAME lightweight pending tick that detects
the entry — not deferred to a later heavy refresh/scoring step. Item 9: none of the new latency
modules place live orders or touch score/tier/actionability/final_r/proposed_signals.
"""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

from src.signals import latency_telemetry as tel


def test_swing_lower_timeframe_probe_resolves_first_touch_without_changing_execution():
    """A 1h candle open is not an execution timestamp; a 5m probe is evidence only."""
    import pandas as pd
    from src.signals import tracker as tr
    from src.signals.tracker import _LevelTouches

    frame = pd.DataFrame({
        "timestamp": pd.to_datetime(["2026-07-27T15:10:00Z", "2026-07-27T15:15:00Z"]),
        "low": [102.0, 100.5], "high": [103.0, 101.5], "close": [102.5, 101.0],
    })
    fs = MagicMock()
    fs.load_ohlcv.side_effect = lambda _ex, _sym, tf: frame if tf == "5m" else None
    signal = {"asset_class": "crypto", "mode": "swing", "symbol": "BTC/USDT",
              "direction": "long", "created_at": "2026-07-27T15:00:00+00:00",
              "entry_low": 100.0, "entry_high": 101.0, "exchange_focus": "binance"}
    at, basis = tr._resolve_crypto_swing_touch(
        signal=signal, promoted_entry=None, touches=_LevelTouches(triggered=True),
        file_store=fs, project_config=SimpleNamespace(anchor_exchange="binance"),
        now=pd.Timestamp("2026-07-27T15:18:00Z").to_pydatetime(), execution_timeframe="1h")
    assert at == "2026-07-27T15:15:00+00:00"
    assert basis == "lower_tf_5m_first_touch"


class _Cfg:
    def __init__(self, root):
        self.root = root


def test_alert_dispatched_in_same_lightweight_tick(tmp_path, monkeypatch):
    from src.storage.sqlite import SQLiteStore
    from src.signals import tracker as tr
    from src.signals.models import SignalOutcome, STATUS_TRIGGERED
    from src.signals.config import load_signal_tracking_config

    st = SQLiteStore(Path(tmp_path) / "t.sqlite")
    st.init_db()
    with st.connect() as c:
        c.execute(
            "INSERT INTO proposed_signals(signal_id, created_at, updated_at, symbol, direction, "
            "mode, tier, score, asset_class, status) VALUES(?,?,?,?,?,?,?,?,?,?)",
            ("sigX", "2026-07-05T10:00:00+00:00", "2026-07-05T10:00:00+00:00", "BTC/USDT",
             "long", "intraday", "A", 80.0, "crypto", "waiting_for_entry"))
        c.commit()

    # spy on the alert dispatcher — records EACH call synchronously; returns a real "sent" result
    calls: list = []

    def _spy(**kw):
        calls.append(kw)
        return {"sent": True, "reason_skipped": None}
    monkeypatch.setattr("src.notifiers.paper_entry.send_paper_entry_alert", _spy)

    # simulate the entry-touch detection inside the tick
    def _fake_track_signal(*, signal, file_store, project_config, tracker_config, now):
        oc = SignalOutcome(signal_id=signal["signal_id"], checked_at="2026-07-05T10:05:00+00:00",
                           status=STATUS_TRIGGERED, entry_triggered=True,
                           entry_triggered_at="2026-07-05T10:05:00+00:00", entry_price_used=100.0)
        return (oc, STATUS_TRIGGERED)
    monkeypatch.setattr(tr, "track_signal", _fake_track_signal)

    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])
    res = tr.track_pending_entries(
        store=st, file_store=MagicMock(), project_config=_Cfg(tmp_path),
        tracker_config=cfg, paper_entry_notifier=MagicMock())

    assert res.checked == 1
    # the alert was dispatched exactly once, WITHIN the same track_pending_entries call/tick
    assert len(calls) == 1 and calls[0]["signal"]["signal_id"] == "sigX"
    # and the latency telemetry recorded detection + send (sent=True) in that same tick
    events = {e["event_type"] for e in tel.load_events(st)}
    assert "entry_condition_detected" in events
    assert "paper_entry_alert_sent" in events
    assert "paper_entry_alert_skipped" not in events


def _seed_pending(st, sid="sigZ", tier="A", mode="intraday", asset="crypto"):
    with st.connect() as c:
        c.execute(
            "INSERT INTO proposed_signals(signal_id, created_at, updated_at, symbol, direction, "
            "mode, tier, score, asset_class, status) VALUES(?,?,?,?,?,?,?,?,?,?)",
            (sid, "2026-07-05T10:00:00+00:00", "2026-07-05T10:00:00+00:00", "BTC/USDT",
             "long", mode, tier, 80.0, asset, "waiting_for_entry"))
        c.commit()


def _fake_triggered(signal, **_):
    from src.signals.models import SignalOutcome, STATUS_TRIGGERED
    oc = SignalOutcome(signal_id=signal["signal_id"], checked_at="2026-07-05T10:05:00+00:00",
                       status=STATUS_TRIGGERED, entry_triggered=True,
                       entry_triggered_at="2026-07-05T10:05:00+00:00", entry_price_used=100.0)
    return (oc, STATUS_TRIGGERED)


def test_duplicate_return_records_skipped_not_sent(tmp_path, monkeypatch):
    from src.storage.sqlite import SQLiteStore
    from src.signals import tracker as tr
    from src.signals.config import load_signal_tracking_config

    st = SQLiteStore(Path(tmp_path) / "t.sqlite"); st.init_db()
    _seed_pending(st, sid="dupSig")
    # send returns a DUPLICATE skip — must NOT be logged as sent
    monkeypatch.setattr("src.notifiers.paper_entry.send_paper_entry_alert",
                        lambda **kw: {"sent": False, "reason_skipped": "duplicate"})
    monkeypatch.setattr(tr, "track_signal", lambda **kw: _fake_triggered(kw["signal"]))
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])
    tr.track_pending_entries(store=st, file_store=MagicMock(), project_config=_Cfg(tmp_path),
                             tracker_config=cfg, paper_entry_notifier=MagicMock())
    events = [e for e in tel.load_events(st)]
    types = {e["event_type"] for e in events}
    assert "paper_entry_alert_skipped" in types
    assert "paper_entry_alert_sent" not in types           # duplicate must NOT count as sent
    skipped = [e for e in events if e["event_type"] == "paper_entry_alert_skipped"]
    assert str(skipped[0]["note"]).endswith("duplicate")


def test_repeated_ticks_do_not_duplicate_transition_events(tmp_path, monkeypatch):
    from src.storage.sqlite import SQLiteStore
    from src.signals import tracker as tr
    from src.signals.config import load_signal_tracking_config

    st = SQLiteStore(Path(tmp_path) / "t.sqlite"); st.init_db()
    _seed_pending(st, sid="rep")
    monkeypatch.setattr("src.notifiers.paper_entry.send_paper_entry_alert",
                        lambda **kw: {"sent": True, "reason_skipped": None})
    monkeypatch.setattr(tr, "track_signal", lambda **kw: _fake_triggered(kw["signal"]))
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])
    for _ in range(4):                                     # four ticks on the SAME entered signal
        tr.track_pending_entries(store=st, file_store=MagicMock(), project_config=_Cfg(tmp_path),
                                 tracker_config=cfg, paper_entry_notifier=MagicMock())
    events = tel.load_events(st)
    n_detected = sum(1 for e in events if e["event_type"] == "entry_condition_detected")
    n_sent = sum(1 for e in events if e["event_type"] == "paper_entry_alert_sent")
    assert n_detected == 1 and n_sent == 1                 # emit-once + transition gate → no floods


def test_alert_failure_records_failed_event(tmp_path, monkeypatch):
    from src.storage.sqlite import SQLiteStore
    from src.signals import tracker as tr
    from src.signals.models import SignalOutcome, STATUS_TRIGGERED
    from src.signals.config import load_signal_tracking_config

    st = SQLiteStore(Path(tmp_path) / "t.sqlite")
    st.init_db()
    with st.connect() as c:
        c.execute(
            "INSERT INTO proposed_signals(signal_id, created_at, updated_at, symbol, direction, "
            "mode, tier, score, asset_class, status) VALUES(?,?,?,?,?,?,?,?,?,?)",
            ("sigY", "2026-07-05T10:00:00+00:00", "2026-07-05T10:00:00+00:00", "ETH/USDT",
             "long", "intraday", "B", 70.0, "crypto", "waiting_for_entry"))
        c.commit()

    def _boom(**kw):
        raise RuntimeError("telegram down")
    monkeypatch.setattr("src.notifiers.paper_entry.send_paper_entry_alert", _boom)

    def _fake_track_signal(*, signal, file_store, project_config, tracker_config, now):
        oc = SignalOutcome(signal_id=signal["signal_id"], checked_at="2026-07-05T10:05:00+00:00",
                           status=STATUS_TRIGGERED, entry_triggered=True,
                           entry_triggered_at="2026-07-05T10:05:00+00:00", entry_price_used=100.0)
        return (oc, STATUS_TRIGGERED)
    monkeypatch.setattr(tr, "track_signal", _fake_track_signal)

    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])
    # a failing notifier must NOT crash the tracker (fail-open) and must record the failed event
    res = tr.track_pending_entries(
        store=st, file_store=MagicMock(), project_config=_Cfg(tmp_path),
        tracker_config=cfg, paper_entry_notifier=MagicMock())
    assert res.checked == 1
    events = {e["event_type"] for e in tel.load_events(st)}
    assert "paper_entry_alert_failed" in events
    # The lifecycle remains pending so the next fast-monitor tick can retry.
    assert st.load_signal("sigY")["status"] == "waiting_for_entry"


def _run_pending_with_source(tmp_path, monkeypatch, telemetry_source=None):
    from src.storage.sqlite import SQLiteStore
    from src.signals import tracker as tr
    from src.signals.config import load_signal_tracking_config
    st = SQLiteStore(Path(tmp_path) / "t.sqlite"); st.init_db()
    _seed_pending(st, sid="srcSig")
    monkeypatch.setattr("src.notifiers.paper_entry.send_paper_entry_alert",
                        lambda **kw: {"sent": True, "reason_skipped": None})
    monkeypatch.setattr(tr, "track_signal", lambda **kw: _fake_triggered(kw["signal"]))
    cfg = load_signal_tracking_config(Path(__file__).resolve().parents[1])
    kwargs = dict(store=st, file_store=MagicMock(), project_config=_Cfg(tmp_path),
                  tracker_config=cfg, paper_entry_notifier=MagicMock())
    if telemetry_source is not None:
        kwargs["telemetry_source"] = telemetry_source
    tr.track_pending_entries(**kwargs)
    return {e["event_type"]: e for e in tel.load_events(st)}


def test_telemetry_source_attributed_to_pending_monitor(tmp_path, monkeypatch):
    ev = _run_pending_with_source(tmp_path, monkeypatch, telemetry_source="pending-monitor")
    assert ev["entry_condition_detected"]["source"] == "pending-monitor"
    assert ev["paper_entry_alert_sent"]["source"] == "pending-monitor"


def test_telemetry_source_defaults_to_track_signals(tmp_path, monkeypatch):
    ev = _run_pending_with_source(tmp_path, monkeypatch, telemetry_source=None)
    assert ev["entry_condition_detected"]["source"] == "track-signals"
    assert ev["paper_entry_alert_sent"]["source"] == "track-signals"


def test_latency_modules_have_no_live_order_calls():
    import src.signals.latency_telemetry as m1
    import src.signals.latency_sla as m2
    import src.signals.pending_monitor as m3
    import src.signals.monitor_audit as m4
    import src.signals.ws_shadow as m5
    import src.stocks.realtime_provider as m6
    for mod in (m1, m2, m3, m4, m5, m6):
        src = Path(mod.__file__).read_text(encoding="utf-8").lower()
        for bad in ("create_order", "place_order", "submit_order", "manual_live_order",
                    "auto_live", "manual_live", "update proposed_signals",
                    "update signal_outcomes", "final_r ="):
            assert bad not in src, f"{mod.__name__} must be paper/read-only: {bad!r}"
