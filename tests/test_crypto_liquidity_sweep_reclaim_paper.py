from __future__ import annotations

import inspect
import sqlite3
from datetime import datetime, timedelta, timezone

import pandas as pd

from src.execution import crypto_liquidity_sweep_reclaim_paper as strategy


UTC = timezone.utc


def _cfg() -> dict:
    cfg = strategy.load_strategy_config()
    cfg.update(
        feature_flag=True,
        max_symbols=0,
        min_rvol=1.0,
        min_liquidation_notional_usd=50_000.0,
        min_oi_drop_pct=0.25,
        max_stop_distance_pct=0.08,
        max_entry_latency_seconds=900.0,
    )
    cfg["sessions"] = {"blocked": [], "strict": [], "preferred": ["us"]}
    cfg["confirmation_profiles"] = {
        "RECLAIM_HOLD_5M_2BAR": {
            "profile_id": "crypto_liquidity_sweep_reclaim_5m_hold2_paper_v2",
            "confirmation_timeframe": "5m",
            "hold_bars": 2,
            "confirmation_window_bars": 6,
            "level_hold_buffer_atr": 0.08,
            "min_reclaim_close_distance_atr": 0.02,
            "min_progress_atr": 0.03,
            "strict_europe": False,
        }
    }
    return cfg


def _frame(start: datetime | None = None) -> pd.DataFrame:
    start = start or datetime(2026, 8, 20, 12, 0, tzinfo=UTC)
    rows = [
        {
            "timestamp": start + timedelta(minutes=5 * index),
            "open": 100.0,
            "high": 100.2,
            "low": 99.8,
            "close": 100.0,
            "volume": 100.0,
        }
        for index in range(58)
    ]
    rows[52].update(open=99.95, high=100.22, low=98.8, close=100.10, volume=230.0)
    rows[53].update(open=100.10, high=100.35, low=99.96, close=100.18, volume=150.0)
    rows[54].update(open=100.18, high=100.50, low=100.02, close=100.32, volume=140.0)
    return pd.DataFrame(rows)


def _event(decision: datetime) -> dict:
    return {
        "event_id": "force-1",
        "event_at": decision - timedelta(minutes=1),
        "side": "SELL",
        "notional_usd": 80_000.0,
        "exchange": "binance",
    }


def _patch_sources(monkeypatch, frame: pd.DataFrame, *, htf_matches: list[dict] | None = None) -> None:
    intelligence = sqlite3.connect(":memory:")
    intelligence.row_factory = sqlite3.Row
    monkeypatch.setattr("src.data_collectors.market_intelligence_store.connect", lambda ensure=False: intelligence)
    monkeypatch.setattr(strategy, "_symbols", lambda *_args, **_kwargs: ["TEST/USDT"])
    monkeypatch.setattr(strategy, "_load_base_frame", lambda *_args, **_kwargs: frame)
    monkeypatch.setattr(strategy, "_load_confirmation_frame", lambda *_args, **_kwargs: frame)
    monkeypatch.setattr(strategy, "_liquidation_source_status", lambda *_args, **_kwargs: {
        "status": "EVENTS_AVAILABLE", "feed_available": True, "transport_status": "ok", "event_count": 1,
    })
    decision = frame.iloc[52]["timestamp"].to_pydatetime() + timedelta(minutes=5)
    monkeypatch.setattr(strategy, "_event_rows", lambda *_args, **_kwargs: [_event(decision)])
    monkeypatch.setattr(strategy, "_contexts", lambda *_args, **_kwargs: {
        "ok": True, "oi_change_pct": -0.8, "spread_bps": 4.0, "oi_venue_pairs": 2,
    })
    monkeypatch.setattr(strategy, "_htf_matches", lambda *_args, **_kwargs: htf_matches if htf_matches is not None else [{
        "timeframe": "1h", "kind": "support", "price": 99.85, "zone_width": 0.3,
        "pivot_at": "2026-08-20T10:00:00+00:00", "known_at": "2026-08-20T11:00:00+00:00",
        "distance_bps": 5.0,
    }])


def test_reclaim_requires_two_closed_5m_holds_after_the_sweep():
    cfg, frame = _cfg(), _frame()
    decision = frame.iloc[52]["timestamp"].to_pydatetime() + timedelta(minutes=5)
    setup = {
        "decision_at": decision, "direction": "long", "level": 99.8,
        "sweep_close": 100.10, "sweep_extreme": 98.8, "stop": 98.7,
    }
    profile = cfg["confirmation_profiles"]["RECLAIM_HOLD_5M_2BAR"]

    early = strategy.detect_reclaim_entry(frame, setup, decision + timedelta(minutes=5), profile)
    confirmed = strategy.detect_reclaim_entry(frame, setup, decision + timedelta(minutes=10), profile)

    assert early["status"] == "pending"
    assert confirmed["status"] == "entry"
    assert confirmed["entry"] == 100.32
    assert confirmed["confirmation_bars"] == 2


def test_tick_records_confirmed_paper_entry_without_live_bridge(monkeypatch, tmp_path):
    cfg, frame = _cfg(), _frame()
    _patch_sources(monkeypatch, frame)
    now = frame.iloc[55]["timestamp"].to_pydatetime() + timedelta(minutes=5)
    db = tmp_path / "desk.sqlite"

    result = strategy.tick(db=str(db), persist=True, now=now, cfg=cfg)

    assert result["enabled"] is True
    assert len(result["rows"]) == 1
    row = result["rows"][0]
    assert row["eligibility_status"] == "eligible"
    assert row["outcome_status"] == "open"
    assert row["entry_price"] == 100.32
    assert row["stop_price"] < row["entry_price"] < row["tp1"] < row["tp2"] < row["tp3"]
    conn = sqlite3.connect(db)
    count = conn.execute(f"SELECT COUNT(*) FROM {strategy.OUTCOME_TABLE} WHERE is_clean_for_edge=1").fetchone()[0]
    assert count == 1
    assert not conn.execute("SELECT 1 FROM sqlite_master WHERE name='live_routing'").fetchone()
    conn.close()


def test_asia_session_is_blocked_before_confirmation(monkeypatch, tmp_path):
    cfg = _cfg()
    cfg["sessions"] = {"blocked": ["asia"], "strict": [], "preferred": ["us"]}
    frame = _frame(datetime(2026, 8, 20, 0, 0, tzinfo=UTC))
    _patch_sources(monkeypatch, frame)
    now = frame.iloc[55]["timestamp"].to_pydatetime() + timedelta(minutes=5)
    db = tmp_path / "desk.sqlite"

    result = strategy.tick(db=str(db), persist=True, now=now, cfg=cfg)

    assert result["rows"] == []
    conn = sqlite3.connect(db)
    reason = conn.execute(
        f"SELECT rejection_reason FROM {strategy.OBS_TABLE} ORDER BY evaluated_at DESC LIMIT 1"
    ).fetchone()[0]
    assert reason == "WEAK_SESSION_BLOCKED"
    conn.close()


def test_default_liquidity_sweep_v2_config_blocks_asia_and_off():
    cfg = strategy.load_strategy_config()
    blocked = {str(value).lower() for value in cfg.get("sessions", {}).get("blocked", [])}
    assert "asia" in blocked
    assert "off" in blocked


def test_missing_htf_level_records_observation_not_trade(monkeypatch, tmp_path):
    cfg, frame = _cfg(), _frame()
    _patch_sources(monkeypatch, frame, htf_matches=[])
    now = frame.iloc[55]["timestamp"].to_pydatetime() + timedelta(minutes=5)
    db = tmp_path / "desk.sqlite"

    result = strategy.tick(db=str(db), persist=True, now=now, cfg=cfg)

    assert result["rows"] == []
    conn = sqlite3.connect(db)
    reason = conn.execute(
        f"SELECT rejection_reason FROM {strategy.OBS_TABLE} ORDER BY evaluated_at DESC LIMIT 1"
    ).fetchone()[0]
    assert reason == "NO_HTF_LEVEL"
    assert conn.execute(f"SELECT COUNT(*) FROM {strategy.OUTCOME_TABLE}").fetchone()[0] == 0
    conn.close()


def test_paper_v2_module_has_no_writes_to_legacy_paper_or_live_tables():
    source = inspect.getsource(strategy).lower()
    for table in ("proposed_signals", "signal_outcomes", "final_r", "paper_ledger", "live_routing"):
        assert f"insert into {table}" not in source
        assert f"update {table}" not in source
        assert f"delete from {table}" not in source


def test_monitor_runs_v2_as_paper_only_after_v1_shadow():
    from scripts import derivatives_monitor

    source = inspect.getsource(derivatives_monitor.current_loop)
    assert "liquidity_sweep_v2_paper_tick" in source
    assert "capture_forward_sweeps" in source
    assert source.index("liquidity_sweep.tick") < source.index("liquidity_sweep_v2.tick")
    assert source.index("capture_forward_sweeps") < source.index("liquidity_sweep_v2.tick")
