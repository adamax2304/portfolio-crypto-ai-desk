"""entry_mode_parameter_sweep: forward-only source, persistence, read-only, uses protection."""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.execution import entry_mode_parameter_sweep as sw
from src.execution import entry_mode_calibration as cal


def test_sweep_signal_uses_protection_and_has_current_baseline():
    cfg = cal.load_calibration_config()
    candles = [{"open": 100, "high": 100, "low": 100, "close": 100},
               {"open": 100, "high": 101.4, "low": 100, "close": 101.4},   # +0.7R
               {"open": 101, "high": 101, "low": 97.9, "close": 98}]        # reverse to stop
    geom = {"direction": "long", "entry_low": 99.5, "entry_high": 100.5, "entry_trigger": 100.0,
            "entry": 100.0, "stop": 98.0, "tp1": 104, "tp2": 106, "tp3": 110,
            "entry_mode": "BREAKOUT_CONTINUATION", "symbol": "X/USDT"}
    out = sw.sweep_signal(geom, candles, cfg)
    assert "structural_stop_atr_buffer" in out and "current" in out["structural_stop_atr_buffer"]
    cur = out["structural_stop_atr_buffer"]["current"]
    assert cur["close_reason"] == "breakeven_stop" and cur["net_r"] == 0.0     # Model-F protection applied


def test_variant_geometry_maker_bps_is_fill_not_cost():
    geom = {"direction": "long", "entry": 100.0, "stop": 98.0}
    g, kw = sw._variant_geometry("maker_trade_through_bps", 10, geom)
    assert kw["maker_trade_through_bps"] == 0.001 and g["stop"] == 98.0        # no stop/cost mutation


def _seed(path):
    c = sqlite3.connect(path)
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, direction TEXT, mode TEXT, "
              "asset_class TEXT, exchange_focus TEXT, created_at TEXT, entry_low REAL, entry_high REAL, "
              "entry_trigger REAL, suggested_entry REAL, stop_loss REAL, invalidation REAL, "
              "tp1 REAL, tp2 REAL, tp3 REAL)")
    c.execute("CREATE TABLE signal_entry_mode (signal_id TEXT PRIMARY KEY, entry_mode TEXT)")
    c.execute("CREATE TABLE paper_shadow_execution_outcomes (signal_id TEXT, branch TEXT, window TEXT, "
              "asset_class TEXT, entry_mode TEXT, entry_fill_status TEXT)")
    for i in range(4):
        sid = f"s{i}"
        # invalidation present -> COALESCE(invalidation, stop_loss) must pick invalidation
        c.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  (sid, "AAA", "long", "intraday", "crypto", "", "2026-06-25T12:00:00+00:00",
                   99.5, 100.5, 100.0, 100.0, 97.5, 98.0, 104, 106, 110))
        c.execute("INSERT INTO signal_entry_mode VALUES (?,?)", (sid, "BREAKOUT_CONTINUATION"))
        c.execute("INSERT INTO paper_shadow_execution_outcomes VALUES (?,?,?,?,?,?)",
                  (sid, "new_logic_shadow", "forward_since_activation", "crypto", "BREAKOUT_CONTINUATION", "filled"))
        # a BACKFILL row that must NOT be picked by the default forward-only loader
        c.execute("INSERT INTO paper_shadow_execution_outcomes VALUES (?,?,?,?,?,?)",
                  (sid, "new_logic_shadow", "historical_backfill", "crypto", "BREAKOUT_CONTINUATION", "filled"))
    c.commit()
    c.close()


def test_forward_only_source_excludes_backfill(tmp_path):
    p = str(tmp_path / "s.sqlite")
    _seed(p)
    conn = sqlite3.connect(p)
    fwd = sw._load_forward_sample(conn, limit=100)          # defaults: new_logic_shadow / forward
    conn.close()
    assert len(fwd) == 4                                    # only the 4 forward rows, not the 4 backfill
    # COALESCE(invalidation, stop_loss) prefers invalidation (98.0) over stop_loss (97.5)
    assert all(abs(float(r["stop_used"]) - 98.0) < 1e-6 for r in fwd)


def test_sweep_persists_results_table(tmp_path, monkeypatch):
    p = str(tmp_path / "s.sqlite")
    _seed(p)
    # avoid OHLCV files: feed a synthetic candle path (+0.7R then reverse)
    df = pd.DataFrame([
        {"timestamp": "2026-06-25T12:05:00+00:00", "open": 100, "high": 100.5, "low": 99.9, "close": 100.2},
        {"timestamp": "2026-06-25T12:10:00+00:00", "open": 100.2, "high": 101.4, "low": 100.0, "close": 101.3},
        {"timestamp": "2026-06-25T12:15:00+00:00", "open": 101.0, "high": 101.0, "low": 97.4, "close": 97.6},
    ])
    monkeypatch.setattr("src.execution.paper_shadow_engine._load_candles", lambda *a, **k: (df, "5m"))
    res = sw.refresh(db=p, persist=True, limit=10)
    assert res["persisted"] is True and res["signals_swept"] == 4
    conn = sqlite3.connect(p)
    tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    assert "entry_mode_parameter_sweep_results" in tables
    n = conn.execute("SELECT count(*) FROM entry_mode_parameter_sweep_results").fetchone()[0]
    # source tables untouched
    ps = conn.execute("SELECT count(*) FROM proposed_signals").fetchone()[0]
    conn.close()
    assert n > 0 and ps == 4


def test_insufficient_coverage_status_and_no_best_star(tmp_path, monkeypatch):
    p = str(tmp_path / "s.sqlite")
    _seed(p)
    df = pd.DataFrame([
        {"timestamp": "2026-06-25T12:05:00+00:00", "open": 100, "high": 101.4, "low": 100, "close": 101.3},
        {"timestamp": "2026-06-25T12:10:00+00:00", "open": 101, "high": 101, "low": 97.4, "close": 97.6}])
    monkeypatch.setattr("src.execution.paper_shadow_engine._load_candles", lambda *a, **k: (df, "5m"))
    res = sw.refresh(db=p, persist=True, limit=10)              # only 4 signals swept < 30
    assert res["coverage_status"] == "INSUFFICIENT_COVERAGE"
    assert res["matches_persisted_table"] is True              # report attests it matches the table
    md = sw.render_markdown(res)
    assert "INSUFFICIENT COVERAGE" in md and "*(best)*" not in md
    assert "matches persisted table: **true**" in md and "signals_swept: **4**" in md


def test_temp_db_refresh_does_not_touch_production_report(tmp_path, monkeypatch):
    prod = Path(sw._root()) / "reports" / "ENTRY_MODE_PARAMETER_SWEEP.md"
    before = prod.read_bytes() if prod.exists() else None
    p = str(tmp_path / "s.sqlite")
    _seed(p)
    df = pd.DataFrame([{"timestamp": "2026-06-25T12:05:00+00:00", "open": 100, "high": 101.4, "low": 100, "close": 101.3},
                       {"timestamp": "2026-06-25T12:10:00+00:00", "open": 101, "high": 101, "low": 97.4, "close": 97.6}])
    monkeypatch.setattr("src.execution.paper_shadow_engine._load_candles", lambda *a, **k: (df, "5m"))
    sw.refresh(db=p, persist=True, limit=10)                   # custom db -> report NOT written globally
    after = prod.read_bytes() if prod.exists() else None
    assert after == before


def test_sweep_dry_run_writes_nothing(tmp_path, monkeypatch):
    p = str(tmp_path / "s.sqlite")
    _seed(p)
    df = pd.DataFrame([{"timestamp": "2026-06-25T12:05:00+00:00", "open": 100, "high": 101.4, "low": 100, "close": 101.3},
                       {"timestamp": "2026-06-25T12:10:00+00:00", "open": 101, "high": 101, "low": 97.4, "close": 97.6}])
    monkeypatch.setattr("src.execution.paper_shadow_engine._load_candles", lambda *a, **k: (df, "5m"))
    res = sw.refresh(db=p, persist=False, limit=10)
    assert res["persisted"] is False
    conn = sqlite3.connect(p)
    tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    conn.close()
    assert "entry_mode_parameter_sweep_results" not in tables


def test_module_read_only():
    src = Path(sw.__file__).read_text(encoding="utf-8").lower()
    for bad in ("update proposed_signals", "update signal_outcomes", "final_r =",
                "create_order", "place_order", "auto_live", "manual_live"):
        assert bad not in src
