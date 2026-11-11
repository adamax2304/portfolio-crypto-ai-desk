"""Regression coverage for shadow cache integrity and stocks-intraday forward evidence."""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import pytest

from src.execution.paper_shadow_engine import ensure_tables as ensure_shadow_tables
from src.execution import stocks_intraday_forward_evaluator as evaluator
from src.storage.file_store import FileStore


class _Config:
    def __init__(self, root: Path):
        self.root = root
        self.raw_dir = root / "data" / "raw"


def test_atomic_ohlcv_save_preserves_prior_cache_when_disk_write_fails(tmp_path, monkeypatch):
    store = FileStore(_Config(tmp_path))
    path = store.ohlcv_path("binance", "BTC/USDT", "5m")
    path.parent.mkdir(parents=True)
    original = "timestamp,open\n2026-07-15T00:00:00Z,100\n"
    path.write_text(original, encoding="utf-8")

    def no_space(*_args, **_kwargs):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(pd.DataFrame, "to_csv", no_space)
    with pytest.raises(OSError, match="No space"):
        store.save_ohlcv("binance", "BTC/USDT", "5m", pd.DataFrame({"timestamp": ["x"]}))
    assert path.read_text(encoding="utf-8") == original
    assert not list(path.parent.glob("*.tmp"))


def test_empty_crypto_cache_is_unavailable_not_a_tracker_crash(tmp_path):
    store = FileStore(_Config(tmp_path))
    path = store.ohlcv_path("binance", "BTC/USDT", "5m")
    path.parent.mkdir(parents=True)
    path.write_text("", encoding="utf-8")
    assert store.load_ohlcv("binance", "BTC/USDT", "5m") is None


def test_empty_frame_never_replaces_a_good_ohlcv_cache(tmp_path):
    store = FileStore(_Config(tmp_path))
    path = store.ohlcv_path("binance", "BTC/USDT", "5m")
    path.parent.mkdir(parents=True)
    original = "timestamp,open\n2026-07-15T00:00:00Z,100\n"
    path.write_text(original, encoding="utf-8")
    with pytest.raises(ValueError, match="empty frame"):
        store.save_ohlcv("binance", "BTC/USDT", "5m", pd.DataFrame())
    assert path.read_text(encoding="utf-8") == original


def _evaluator_db(path: Path, *, activated_at: str = "2026-06-01T00:00:00+00:00") -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    ensure_shadow_tables(conn)
    conn.execute("CREATE TABLE proposed_signals (signal_id TEXT PRIMARY KEY, value TEXT)")
    conn.execute("CREATE TABLE signal_outcomes (signal_id TEXT PRIMARY KEY, final_r REAL)")
    conn.execute(
        "INSERT INTO paper_shadow_meta(k,v) VALUES ('stocks_intraday_forward_shadow_v2_activated_at', ?)",
        (activated_at,),
    )
    return conn


def _insert_outcome(conn, sid: str, *, mode: str = "PULLBACK_LIMIT", pnl: float = 10.0,
                    clean: int = 1, window: str = "forward_since_activation",
                    economic_trade_key: str | None = None) -> None:
    conn.execute("INSERT INTO proposed_signals(signal_id,value) VALUES (?,?)", (sid, "source"))
    conn.execute("""
        INSERT INTO paper_shadow_execution_outcomes
        (signal_id, branch, economic_trade_key, asset_class, entry_mode, entry_fill_status, entry_fill_time,
         net_pnl_usdt, net_r, fees_usdt, slippage_usdt, outcome_status, fee_profile,
         cost_model_status, shadow_lane, window, is_clean_for_edge, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (sid, "new_logic_shadow", economic_trade_key, "stocks", mode, "filled", "2026-07-01T15:00:00+00:00",
            pnl, pnl / 10, 0.5, 0.25, "closed", "stock_etf_default", "current",
            "stocks_intraday_forward", window, clean, "2026-07-01T14:00:00+00:00"))


def test_stocks_forward_evaluator_uses_only_clean_forward_rows_and_source_tables_unchanged(tmp_path):
    db = tmp_path / "forward.sqlite"
    conn = _evaluator_db(db)
    _insert_outcome(conn, "clean", pnl=25.0, clean=1)
    _insert_outcome(conn, "dirty", pnl=-99.0, clean=0)
    _insert_outcome(conn, "backfill", pnl=-999.0, clean=1, window="historical_backfill")
    conn.execute("INSERT INTO signal_outcomes(signal_id,final_r) VALUES ('stable', 42.0)")
    conn.commit()
    before = (conn.execute("SELECT COUNT(*) FROM proposed_signals").fetchone()[0],
              conn.execute("SELECT COUNT(*), SUM(final_r) FROM signal_outcomes").fetchone())
    conn.close()

    result = evaluator.evaluate(db=str(db), persist=True, now_iso="2026-07-15T00:00:00+00:00")
    pullback = next(s for s in result["slices"] if s["entry_mode"] == "PULLBACK_LIMIT")
    assert pullback["clean_closed"] == 1 and pullback["dirty_closed"] == 1
    assert pullback["net_pnl_usd"] == 25.0  # dirty loss and backfill never become edge evidence
    assert pullback["verdict"] == "INSUFFICIENT_CLEAN_SAMPLE"
    assert pullback["legacy_evidence_reused"] is False

    conn = sqlite3.connect(db)
    after = (conn.execute("SELECT COUNT(*) FROM proposed_signals").fetchone()[0],
             conn.execute("SELECT COUNT(*), SUM(final_r) FROM signal_outcomes").fetchone())
    assert after == before
    assert conn.execute("SELECT COUNT(*) FROM stocks_intraday_forward_shadow_evaluations").fetchone()[0] == 2
    conn.close()


def test_stocks_forward_evaluator_requires_clean_sample_and_forward_age_before_review(tmp_path):
    db = tmp_path / "review.sqlite"
    conn = _evaluator_db(db, activated_at="2026-07-14T00:00:00+00:00")
    for i in range(30):
        _insert_outcome(conn, f"young-{i}", mode="BREAKOUT_CONTINUATION", pnl=3.0 if i < 20 else -1.0)
    conn.commit(); conn.close()
    young = evaluator.evaluate(db=str(db), persist=False, now_iso="2026-07-15T00:00:00+00:00")
    breakout = next(s for s in young["slices"] if s["entry_mode"] == "BREAKOUT_CONTINUATION")
    assert breakout["clean_closed"] == 30 and breakout["verdict"] == "ACCUMULATING_FORWARD_DAYS"

    mature = evaluator.evaluate(db=str(db), persist=False, now_iso="2026-08-15T00:00:00+00:00")
    breakout = next(s for s in mature["slices"] if s["entry_mode"] == "BREAKOUT_CONTINUATION")
    assert breakout["net_pnl_usd"] > 0 and breakout["profit_factor"] > 1.25
    assert breakout["verdict"] == "REVIEW_ONLY"  # never an automatic paper/live change


def test_stocks_forward_evaluator_keeps_direction_changes_separate(tmp_path):
    db = tmp_path / "direction.sqlite"
    conn = _evaluator_db(db)
    conn.execute("ALTER TABLE proposed_signals ADD COLUMN direction TEXT")
    shadow_columns = {row[1] for row in conn.execute("PRAGMA table_info(paper_shadow_execution_outcomes)")}
    if "side" not in shadow_columns:
        conn.execute("ALTER TABLE paper_shadow_execution_outcomes ADD COLUMN side TEXT")
    if "direction_changed" not in shadow_columns:
        conn.execute("ALTER TABLE paper_shadow_execution_outcomes ADD COLUMN direction_changed INTEGER")
    _insert_outcome(conn, "same", mode="BREAKOUT_CONTINUATION", pnl=10.0)
    _insert_outcome(conn, "flipped", mode="BREAKOUT_CONTINUATION", pnl=20.0)
    conn.execute("UPDATE proposed_signals SET direction='long' WHERE signal_id IN ('same','flipped')")
    conn.execute("UPDATE paper_shadow_execution_outcomes SET side='long', direction_changed=0 WHERE signal_id='same'")
    conn.execute("UPDATE paper_shadow_execution_outcomes SET side='short', direction_changed=1 WHERE signal_id='flipped'")
    conn.commit(); conn.close()

    result = evaluator.evaluate(db=str(db), persist=True, now_iso="2026-07-15T00:00:00+00:00")
    breakout = next(s for s in result["slices"] if s["entry_mode"] == "BREAKOUT_CONTINUATION")
    assert breakout["direction_breakdown"]["unchanged"]["net_pnl_usd"] == 10.0
    assert breakout["direction_breakdown"]["changed"]["net_pnl_usd"] == 20.0
    conn = sqlite3.connect(db)
    cols = {row[1] for row in conn.execute("PRAGMA table_info(stocks_intraday_forward_shadow_evaluations)")}
    assert "direction_breakdown_json" in cols
    conn.close()


def test_stocks_forward_evaluator_counts_one_economic_trade_once(tmp_path):
    db = tmp_path / "dedupe.sqlite"
    conn = _evaluator_db(db)
    _insert_outcome(conn, "first", pnl=-25.0, economic_trade_key="GE|long|intraday|100|2026-07-01")
    _insert_outcome(conn, "repeat-1", pnl=-25.0, economic_trade_key="GE|long|intraday|100|2026-07-01")
    _insert_outcome(conn, "repeat-2", pnl=-25.0, economic_trade_key="GE|long|intraday|100|2026-07-01")
    conn.commit(); conn.close()

    result = evaluator.evaluate(db=str(db), persist=True, now_iso="2026-07-15T00:00:00+00:00")
    pullback = next(s for s in result["slices"] if s["entry_mode"] == "PULLBACK_LIMIT")
    assert pullback["forward_rows"] == 1
    assert pullback["clean_closed"] == 1
    assert pullback["net_pnl_usd"] == -25.0
    assert pullback["duplicate_rows_excluded"] == 2


def test_pending_monitor_critical_disk_skips_refresh_and_tracker(tmp_path, monkeypatch):
    from src.signals import pending_monitor as pm
    from src.signals.config import load_signal_tracking_config
    from src.storage.sqlite import SQLiteStore

    class Supervisor:
        def __init__(self):
            self.db = SQLiteStore(tmp_path / "pending.sqlite")
            self.db.init_db()
            self.config = _Config(tmp_path)
            self.file_store = object()

    supervisor = Supervisor()
    called = {"refresh": False, "tracker": False}
    monkeypatch.setattr(pm, "disk_space_status", lambda *_a, **_k: {"state": "critical", "free_mb": 10,
                                                                      "critical_free_mb": 1024})
    monkeypatch.setattr("src.signals.pending_symbol_universe.pending_symbols", lambda *_a, **_k: ["BTC/USDT"])
    monkeypatch.setattr("src.signals.tracker.track_pending_entries",
                        lambda **_kw: called.__setitem__("tracker", True))

    result = pm.pending_monitor_tick(
        supervisor, tracker_config=load_signal_tracking_config(Path(__file__).resolve().parents[1]),
        refresh_fn=lambda *_a, **_k: called.__setitem__("refresh", True), critical_free_mb=1024,
    )
    assert result["data_integrity_blocked"] is True
    assert result["checked"] == 0 and called == {"refresh": False, "tracker": False}
    assert any(error.startswith("disk_critical:") for error in result["errors"])
