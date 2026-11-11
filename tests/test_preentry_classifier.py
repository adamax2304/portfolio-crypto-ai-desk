"""pre-entry classifier: candle CLOSE-time lookahead guard (item 3) + data-quality labels."""
from __future__ import annotations

import pandas as pd

from src.execution import preentry_classifier as pe


def _df(rows):
    return pd.DataFrame(rows)


def test_closed_candles_excludes_in_progress_candle():
    # 1h bars; timestamp = OPEN time. created_at is INSIDE the 12:00 candle (12:30).
    df = _df([
        {"timestamp": "2026-06-05T10:00:00+00:00", "open": 1, "high": 10, "low": 1, "close": 5},
        {"timestamp": "2026-06-05T11:00:00+00:00", "open": 1, "high": 11, "low": 1, "close": 5},
        {"timestamp": "2026-06-05T12:00:00+00:00", "open": 1, "high": 999, "low": 1, "close": 5},  # in-progress
    ])
    out = pe.closed_candles(df, "1h", "2026-06-05T12:30:00+00:00")
    highs = list(out["high"])
    assert highs == [10, 11]                       # 12:00 candle (high=999, close 13:00) is excluded
    assert 999 not in highs                         # its future high/low/close never seen


def test_closed_candle_exactly_at_created_at_is_kept():
    df = _df([
        {"timestamp": "2026-06-05T11:00:00+00:00", "open": 1, "high": 11, "low": 1, "close": 5},  # closes 12:00
        {"timestamp": "2026-06-05T12:00:00+00:00", "open": 1, "high": 12, "low": 1, "close": 5},  # closes 13:00
    ])
    out = pe.closed_candles(df, "1h", "2026-06-05T12:00:00+00:00")
    assert list(out["high"]) == [11]                # close_time(11:00)=12:00 <= 12:00 kept; 12:00 excluded


def test_unknown_timeframe_falls_back_to_strict_open_guard():
    df = _df([
        {"timestamp": "2026-06-05T11:00:00+00:00", "open": 1, "high": 11, "low": 1, "close": 5},
        {"timestamp": "2026-06-05T12:00:00+00:00", "open": 1, "high": 12, "low": 1, "close": 5},
    ])
    out = pe.closed_candles(df, "weird", "2026-06-05T12:00:00+00:00")  # unknown tf
    assert list(out["high"]) == [11]                # strict: timestamp < created_at


def test_tf_to_timedelta():
    assert pe._tf_to_timedelta("1h") == pd.Timedelta(hours=1)
    assert pe._tf_to_timedelta("15m") == pd.Timedelta(minutes=15)
    assert pe._tf_to_timedelta("1d") == pd.Timedelta(days=1)
    assert pe._tf_to_timedelta("nope") is None


def test_data_quality_labels():
    thin = pe.classify_preentry_from_candles(direction="long", entry_low=99, entry_high=101,
                                              entry=100, stop=98, candles=[{"open":1,"high":1,"low":1,"close":1}])
    assert thin["data_quality"] == "thin"
    none = pe.classify_preentry_from_candles(direction="long", entry_low=99, entry_high=101,
                                             entry=100, stop=98, candles=[])
    assert none["data_quality"] == "no_data"


def test_candles_le_created_uses_close_time(monkeypatch):
    # full loader returns bars straddling created_at; the guard must drop the in-progress one
    df = _df([
        {"timestamp": "2026-06-05T10:00:00+00:00", "open": 1, "high": 10, "low": 1, "close": 5},
        {"timestamp": "2026-06-05T11:00:00+00:00", "open": 1, "high": 11, "low": 1, "close": 5},
        {"timestamp": "2026-06-05T12:00:00+00:00", "open": 1, "high": 999, "low": 1, "close": 5},
    ])
    monkeypatch.setattr("src.signals.tracker._load_ohlcv_for_signal", lambda *a, **k: (df, "binance", "1h"))
    out = pe._candles_le_created(fs=None, cfg=None, symbol="X/USDT", mode="intraday",
                                 asset_class="crypto", exchange_focus="", created_at="2026-06-05T12:30:00+00:00")
    assert len(out) == 2 and all(c["high"] != 999 for c in out)


def test_preentry_prefers_invalidation_over_stop_loss(tmp_path, monkeypatch):
    import sqlite3
    from src.execution import preentry_classifier as pe
    p = str(tmp_path / "pe.sqlite")
    c = sqlite3.connect(p)
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, direction TEXT, mode TEXT, "
              "asset_class TEXT, exchange_focus TEXT, created_at TEXT, entry_low REAL, entry_high REAL, "
              "suggested_entry REAL, stop_loss REAL, invalidation REAL)")
    c.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
              ("s1", "AAA", "long", "intraday", "crypto", "", "2026-06-25T12:00:00+00:00",
               99, 101, 100, 97.5, 98.0))       # stop_loss=97.5, invalidation=98.0
    c.commit(); c.close()
    df = _df([{"timestamp": "2026-06-25T11:00:00+00:00", "open": 100, "high": 101, "low": 99, "close": 100}])
    monkeypatch.setattr("src.signals.tracker._load_ohlcv_for_signal", lambda *a, **k: (df, "binance", "1h"))
    captured = {}
    real = pe.classify_preentry_from_candles

    def _spy(**kw):
        captured["stop"] = kw.get("stop")
        return real(**kw)
    monkeypatch.setattr(pe, "classify_preentry_from_candles", _spy)
    pe.refresh(db=p, limit=10)
    assert captured["stop"] == 98.0              # COALESCE(invalidation, stop_loss) -> invalidation


def test_entry_path_preentry_label_is_immutable_after_capture(tmp_path, monkeypatch):
    import sqlite3
    from types import SimpleNamespace
    p = str(tmp_path / "entry_capture.sqlite")
    c = sqlite3.connect(p)
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, direction TEXT, mode TEXT, "
              "asset_class TEXT, exchange_focus TEXT, created_at TEXT, entry_low REAL, entry_high REAL, "
              "suggested_entry REAL, stop_loss REAL, invalidation REAL)")
    c.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
              ("s1", "AAA/USDT", "long", "intraday", "crypto", "", "2026-06-25T12:00:00+00:00",
               99, 101, 100, 98, 98))
    c.commit(); c.close()
    candles = [{"open": 100, "high": 101, "low": 99, "close": 100} for _ in range(25)]
    monkeypatch.setattr(pe, "_candles_le_created", lambda *a, **k: candles)
    cfg = SimpleNamespace(db_path=p)
    first = pe.ensure_for_signal({"signal_id": "s1"}, db=p, cfg=cfg, fs=object())
    assert first["data_quality"] == "ok" and first["source"] == "entry_path"
    monkeypatch.setattr(pe, "_candles_le_created", lambda *a, **k: [])
    second = pe.ensure_for_signal({"signal_id": "s1"}, db=p, cfg=cfg, fs=object())
    assert second["entry_mode"] == first["entry_mode"]
    assert second["data_quality"] == "ok" and second["source"] == "entry_path"


def test_ensure_for_signal_overwrites_stale_scheduler_backfill_source(tmp_path, monkeypatch):
    """A signal_entry_mode_preentry row written by refresh() (scheduler_backfill) before the
    signal actually triggered must not permanently block the live path from ever recording
    an entry_path source. EPIC/USDT (sig_8b39a22bdd99b72f, 2026-07-26) sat waiting_for_entry
    across a scheduler cycle, got backfilled early, then triggered live 7h later — but the
    live-canary policy requires source=='entry_path', so it was wrongly rejected
    (PREENTRY_NOT_POINT_IN_TIME) despite a genuinely fresh, point-in-time entry."""
    import sqlite3
    from types import SimpleNamespace
    p = str(tmp_path / "backfill_then_live.sqlite")
    c = sqlite3.connect(p)
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, direction TEXT, mode TEXT, "
              "asset_class TEXT, exchange_focus TEXT, created_at TEXT, entry_low REAL, entry_high REAL, "
              "suggested_entry REAL, stop_loss REAL, invalidation REAL)")
    c.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
              ("s1", "EPIC/USDT", "long", "swing", "crypto", "", "2026-07-26T15:25:49+00:00",
               99, 101, 100, 98, 98))
    c.commit(); c.close()
    cfg = SimpleNamespace(db_path=p)
    candles = [{"open": 100, "high": 101, "low": 99, "close": 100} for _ in range(25)]
    monkeypatch.setattr(pe, "_candles_le_created", lambda *a, **k: candles)

    # Simulate refresh() running while the signal was still waiting_for_entry: writes
    # a backfill row directly (bypassing ensure_for_signal, mirroring refresh()'s own path).
    conn = sqlite3.connect(p)
    conn.row_factory = sqlite3.Row
    pe.ensure_tables(conn)
    row = conn.execute("SELECT signal_id, symbol, direction, mode, asset_class, exchange_focus, "
                        "created_at, entry_low, entry_high, suggested_entry, "
                        "COALESCE(invalidation, stop_loss) AS stop_used "
                        "FROM proposed_signals WHERE signal_id='s1'").fetchone()
    rec = pe._classify_signal_row(row, fs=object(), cfg=cfg)
    pe._write_record(conn, row, rec, source="scheduler_backfill")
    conn.commit()
    conn.close()

    before = sqlite3.connect(p)
    before.row_factory = sqlite3.Row
    stale = before.execute("SELECT * FROM signal_entry_mode_preentry WHERE signal_id='s1'").fetchone()
    before.close()
    assert stale["source"] == "scheduler_backfill"

    # The signal now triggers live; the paper-entry path calls ensure_for_signal.
    live = pe.ensure_for_signal({"signal_id": "s1"}, db=p, cfg=cfg, fs=object())
    assert live["source"] == "entry_path"
    assert live["data_quality"] == "ok"


def test_module_read_only():
    from pathlib import Path
    src = Path(pe.__file__).read_text(encoding="utf-8").lower()
    for bad in ("update proposed_signals", "update signal_outcomes", "final_r =",
                "create_order", "auto_live", "manual_live"):
        assert bad not in src
