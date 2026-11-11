from __future__ import annotations

import inspect
import sqlite3
from datetime import datetime, timedelta, timezone

import pandas as pd

from src.execution import crypto_htf_liquidity_reclaim_shadow as strategy


UTC = timezone.utc


def _cfg() -> dict:
    cfg = dict(strategy.load_strategy_config())
    cfg.update(
        feature_flag=True,
        max_symbols=0,
        require_btc_alignment=False,
        min_rvol=1.0,
        min_sweep_atr=0.05,
        min_liquidation_notional_usd=50_000.0,
        min_oi_drop_pct=0.25,
        block_sessions=[],
    )
    return cfg


def _structure() -> pd.DataFrame:
    start = datetime(2026, 8, 1, tzinfo=UTC)
    rows = []
    for index in range(36):
        # A gentle drift avoids fabricating flat-price local extrema around
        # every bar. The two explicit pivots are the only structural zones.
        low, high = 100.0 + index * 0.005, 105.0 + index * 0.01
        if index == 18:
            low = 96.0
        if index == 28:
            high = 118.0
        rows.append({"timestamp": start + timedelta(hours=4 * index), "open": 105.0,
                     "high": high, "low": low, "close": 105.0, "volume": 100.0})
    return pd.DataFrame(rows)


def _hourly() -> pd.DataFrame:
    start = datetime(2026, 8, 6, 10, tzinfo=UTC)
    rows = [{"timestamp": start + timedelta(hours=index), "open": 105.0, "high": 106.0,
             "low": 100.0, "close": 105.0, "volume": 100.0} for index in range(30)]
    # Raids the confirmed 4h low (96), rejects it and closes back above it.
    rows[25].update(open=98.0, high=101.0, low=94.0, close=98.5, volume=220.0)
    return pd.DataFrame(rows)


def _fifteen(start: datetime) -> pd.DataFrame:
    rows = []
    for index in range(24):
        rows.append({"timestamp": start + timedelta(minutes=15 * index), "open": 98.5,
                     "high": 99.3, "low": 97.7, "close": 98.3, "volume": 100.0})
    rows[15].update(open=98.2, high=99.8, low=97.7, close=98.9)
    rows[16].update(open=98.8, high=100.2, low=98.0, close=99.4)
    return pd.DataFrame(rows)


def test_confirmed_pivots_do_not_exist_until_right_hand_bars_close():
    cfg, frame = _cfg(), _structure()
    pivot = frame.iloc[18]["timestamp"].to_pydatetime()
    too_early = pivot + timedelta(hours=4 * (int(cfg["pivot_right_bars"]) + 1)) - timedelta(minutes=1)
    known = pivot + timedelta(hours=4 * (int(cfg["pivot_right_bars"]) + 1))

    assert not [item for item in strategy.confirmed_pivot_levels(frame, as_of=too_early, cfg=cfg)
                if item["kind"] == "support" and item["price"] == 96.0]
    assert [item for item in strategy.confirmed_pivot_levels(frame, as_of=known, cfg=cfg)
            if item["kind"] == "support" and item["price"] == 96.0]


def test_structural_sweep_requires_matching_observed_force_order():
    cfg, structure, hourly = _cfg(), _structure(), _hourly()
    idx = 25
    decision = hourly.iloc[idx]["timestamp"].to_pydatetime() + timedelta(hours=1)
    events = [{"event_id": "forced-long", "event_at": decision - timedelta(minutes=2),
               "side": "SELL", "notional_usd": 80_000.0, "exchange": "binance"}]

    setup = strategy.detect_structural_sweep(structure, hourly, idx, events, cfg)
    assert setup["ok"] is True
    assert setup["direction"] == "long"
    assert setup["level"]["kind"] == "support"
    assert setup["opposing_level"]["kind"] == "resistance"

    wrong = strategy.detect_structural_sweep(
        structure, hourly, idx,
        [{"event_id": "wrong", "event_at": decision, "side": "BUY", "notional_usd": 100_000.0}], cfg,
    )
    assert wrong["ok"] is False
    assert wrong["reason"] == "LIQUIDATION_SIDE_MISMATCH"


def test_missing_liquidation_transport_is_a_data_gap_not_a_reversal_signal():
    cfg, structure, hourly = _cfg(), _structure(), _hourly()
    setup = strategy.detect_structural_sweep(
        structure, hourly, 25, [], cfg, liquidation_feed_available=False,
    )
    assert setup["ok"] is False
    assert setup["reason"] == "LIQUIDATION_DATA_MISSING"


def test_early_and_held_profiles_enter_on_one_and_two_closed_reclaims():
    cfg = _cfg()
    decision = datetime(2026, 8, 6, 12, 0, tzinfo=UTC)
    # Preserve an ordinary 15m history before the post-sweep confirmation.
    frame = _fifteen(decision - timedelta(minutes=15 * 15))
    base = {"decision_at": decision.isoformat(), "direction": "long", "structure_level": 96.0,
            "structure_zone_width": 1.0}
    early = strategy._confirmation_entry(frame, {**base, "entry_profile": "EARLY_RECLAIM"},
                                         decision + timedelta(minutes=45), cfg)
    held = strategy._confirmation_entry(frame, {**base, "entry_profile": "HELD_RECLAIM"},
                                        decision + timedelta(minutes=45), cfg)
    assert early["status"] == "entry"
    assert held["status"] == "entry"
    assert early["entry_at"] < held["entry_at"]
    assert early["confirmation_bars"] == 1
    assert held["confirmation_bars"] == 2


def test_pending_row_carries_the_sweep_stop_through_to_a_real_entry(monkeypatch):
    # Regression: _create_pending_rows() used to omit stop_price entirely, so
    # _entry_geometry() crashed with TypeError(float(None)) the moment ANY
    # candidate reached confirmation -- every real candidate, forever, since
    # this path is unconditional once a reclaim confirms.
    cfg, structure, hourly = _cfg(), _structure(), _hourly()
    idx = 25
    decision = hourly.iloc[idx]["timestamp"].to_pydatetime() + timedelta(hours=1)
    events = [{"event_id": "forced-long", "event_at": decision - timedelta(minutes=2),
               "side": "SELL", "notional_usd": 80_000.0, "exchange": "binance"}]
    setup = strategy.detect_structural_sweep(structure, hourly, idx, events, cfg)
    assert setup["ok"] is True

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    strategy.ensure_tables(conn)
    context = {"ok": True, "oi_change_pct": -1.0, "funding_rate_8h": 0.0001, "spread_bps": 5.0}
    rows = strategy._create_pending_rows(conn, cfg, "TEST/USDT", decision, setup, context)
    conn.commit()
    assert len(rows) == 2  # EARLY_RECLAIM + HELD_RECLAIM, independently
    for row in rows:
        assert row["stop_price"] == setup["stop"]

    fifteen = _fifteen(decision - timedelta(minutes=15 * 15))
    monkeypatch.setattr(strategy, "_load_frame",
                        lambda symbol, timeframe: fifteen if timeframe == cfg["confirmation_timeframe"]
                        else pd.DataFrame())
    # This test targets the stop_price wiring through confirmation -> entry
    # geometry, not the separately-covered OI/funding entry-context gating
    # (which needs a full derivative_snapshots/liquidity fixture elsewhere).
    monkeypatch.setattr(strategy, "_entry_context", lambda *_a, **_k: {
        "ok": True, "oi_change_pct": -1.0, "funding_rate_8h": 0.0,
        "spread_bps": 5.0, "oi_rebuild_pct": 0.0, "oi_rebuild_venue_pairs": 1,
    })

    entered, skipped = strategy._mature_pending(conn, conn, decision + timedelta(minutes=45), cfg)
    assert entered == 2 and skipped == 0
    stored = conn.execute(
        "SELECT outcome_status, stop_price, entry_price, tp1, tp2, tp3 "
        "FROM crypto_htf_liquidity_reclaim_v1_shadow_outcomes"
    ).fetchall()
    assert len(stored) == 2
    for row in stored:
        assert row["outcome_status"] == "open"
        assert row["stop_price"] == setup["stop"]
        assert None not in (row["entry_price"], row["tp1"], row["tp2"], row["tp3"])


def test_private_schema_migration_is_idempotent():
    conn = sqlite3.connect(":memory:")
    strategy.ensure_tables(conn)
    strategy.ensure_tables(conn)
    columns = {row[1] for row in conn.execute("PRAGMA table_info(crypto_htf_liquidity_reclaim_v1_shadow_outcomes)")}
    assert {"entry_profile", "structure_level", "opposing_level_price", "is_clean_for_edge"} <= columns


def test_private_tables_and_dry_run_cannot_change_trading_tables(monkeypatch, tmp_path):
    db = tmp_path / "desk.sqlite"
    conn = sqlite3.connect(db)
    forbidden = ("proposed_signals", "signal_outcomes", "final_r", "paper_ledger", "live_routing")
    for table in forbidden:
        conn.execute(f"CREATE TABLE {table}(value TEXT)")
        conn.execute(f"INSERT INTO {table} VALUES('stable')")
    conn.commit()
    conn.close()

    intelligence = sqlite3.connect(":memory:")
    intelligence.row_factory = sqlite3.Row
    intelligence.execute("CREATE TABLE liquidation_events(exchange TEXT,event_id TEXT,event_at TEXT,side TEXT,notional_usd REAL,normalized_symbol TEXT)")
    intelligence.execute("CREATE TABLE intelligence_source_health(source TEXT,status TEXT,last_success_at TEXT)")
    monkeypatch.setattr("src.data_collectors.market_intelligence_store.connect", lambda ensure=False: intelligence)
    monkeypatch.setattr(strategy, "_symbols", lambda *_args, **_kwargs: [])
    result = strategy.tick(db=str(db), persist=False, now=datetime(2026, 8, 20, tzinfo=UTC), cfg=_cfg())
    assert result["enabled"] is True

    conn = sqlite3.connect(db)
    assert conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE name='crypto_htf_liquidity_reclaim_v1_shadow_outcomes'").fetchone()[0] == 0
    for table in forbidden:
        assert conn.execute(f"SELECT value FROM {table}").fetchone()[0] == "stable"
    conn.close()


def test_module_has_no_writes_to_paper_or_live_tables():
    source = inspect.getsource(strategy).lower()
    for table in ("proposed_signals", "signal_outcomes", "final_r", "paper_ledger", "live_routing"):
        assert f"insert into {table}" not in source
        assert f"update {table}" not in source
        assert f"delete from {table}" not in source


def test_monitor_refreshes_htf_cache_before_htf_tick():
    from scripts import derivatives_monitor

    source = inspect.getsource(derivatives_monitor.current_loop)
    assert "htf_liquidity_reclaim_ohlcv" in source
    assert source.index("htf_reclaim.refresh_ohlcv") < source.index("htf_reclaim.tick")
