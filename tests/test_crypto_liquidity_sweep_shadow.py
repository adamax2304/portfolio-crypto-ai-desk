from __future__ import annotations

import inspect
import sqlite3
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pandas as pd

from src.execution import crypto_liquidity_sweep_shadow as strategy


UTC = timezone.utc


def _cfg() -> dict:
    cfg = dict(strategy.load_strategy_config())
    cfg.update(feature_flag=True, block_sessions=[], min_rvol=1.0, max_symbols=0)
    return cfg


def _frame() -> pd.DataFrame:
    start = datetime(2026, 8, 20, 12, 0, tzinfo=UTC)
    rows = [
        {"timestamp": start + timedelta(minutes=5 * index), "open": 100.0,
         "high": 100.2, "low": 99.8, "close": 100.0, "volume": 100.0}
        for index in range(58)
    ]
    # A stop sweep below the established range that closes back above the
    # range low. It is evaluated only once this 5m candle closes.
    rows[52].update(open=99.95, high=100.22, low=98.8, close=100.1, volume=230.0)
    return pd.DataFrame(rows)


def test_downside_sweep_requires_matching_observed_long_liquidation():
    cfg, frame, idx = _cfg(), _frame(), 52
    decision_at = frame.iloc[idx]["timestamp"].to_pydatetime() + timedelta(minutes=5)
    events = [{"event_id": "force-1", "event_at": decision_at - timedelta(minutes=1),
               "side": "SELL", "notional_usd": 60_000.0}]

    setup = strategy.detect_sweep(frame, idx, events, cfg)

    assert setup["ok"] is True
    assert setup["direction"] == "long"
    assert setup["sweep_at"] == frame.iloc[idx]["timestamp"].to_pydatetime()
    assert setup["decision_at"] == decision_at
    assert setup["entry"] > setup["stop"]
    assert setup["level_touch_count"] >= 2
    assert setup["would_pass_two_touch_level"] is True


def test_sweep_rejects_force_order_on_the_wrong_side():
    cfg, frame, idx = _cfg(), _frame(), 52
    decision_at = frame.iloc[idx]["timestamp"].to_pydatetime() + timedelta(minutes=5)
    setup = strategy.detect_sweep(
        frame, idx,
        [{"event_id": "force-1", "event_at": decision_at, "side": "BUY", "notional_usd": 90_000.0}],
        cfg,
    )
    assert setup["ok"] is False
    assert setup["reason"] == "LIQUIDATION_SIDE_MISMATCH"


def test_healthy_liquidation_feed_without_a_matching_event_is_not_a_data_gap():
    cfg, frame, idx = _cfg(), _frame(), 52
    setup = strategy.detect_sweep(frame, idx, [], cfg, liquidation_feed_available=True)
    assert setup["ok"] is False
    assert setup["reason"] == "LIQUIDATION_NOT_OBSERVED"


def test_unavailable_liquidation_feed_is_a_data_gap():
    cfg, frame, idx = _cfg(), _frame(), 52
    setup = strategy.detect_sweep(frame, idx, [], cfg, liquidation_feed_available=False)
    assert setup["ok"] is False
    assert setup["reason"] == "LIQUIDATION_DATA_MISSING"


def test_event_query_honours_the_configured_liquidation_sources():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE liquidation_events(exchange TEXT,event_id TEXT,event_at TEXT,side TEXT,notional_usd REAL,normalized_symbol TEXT)")
    at = datetime(2026, 8, 20, 12, 10, tzinfo=UTC)
    for exchange in ("binance", "bybit"):
        conn.execute("INSERT INTO liquidation_events VALUES(?,?,?,?,?,?)",
                     (exchange, exchange, (at - timedelta(minutes=1)).isoformat(), "SELL", 100_000.0, "TESTUSDT"))
    cfg = _cfg(); cfg["liquidation_sources"] = ["bybit"]
    rows = strategy._event_rows(conn, "TEST/USDT", at, cfg)
    assert [row["exchange"] for row in rows] == ["bybit"]


def test_okx_observation_never_changes_binance_bybit_feed_availability():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE liquidation_events(exchange TEXT,event_id TEXT,event_at TEXT,side TEXT,notional_usd REAL,normalized_symbol TEXT)")
    conn.execute("CREATE TABLE intelligence_source_health(source TEXT,status TEXT,last_success_at TEXT,error TEXT)")
    now = datetime(2026, 8, 20, 12, 10, tzinfo=UTC)
    conn.execute("INSERT INTO intelligence_source_health VALUES(?,?,?,?)",
                 ("liquidations:binance_ws", "ok", now.isoformat(), None))
    cfg = _cfg()
    cfg.update(liquidation_sources=["binance"], liquidation_observation_sources=["binance", "okx"])

    status = strategy._liquidation_source_status(conn, cfg, now)

    assert status["feed_available"] is True
    assert status["observation"]["venues"] == ["binance", "okx"]
    assert status["observation"]["event_count"] == 0


def test_mature_open_maps_simulator_status_to_outcome_status(monkeypatch):
    cfg, conn = _cfg(), sqlite3.connect(":memory:")
    cfg["max_holding_bars"] = 1
    conn.row_factory = sqlite3.Row
    strategy.ensure_tables(conn)
    entry_at = datetime(2026, 8, 20, 12, 0, tzinfo=UTC)
    row = {column: None for column in strategy.OUTCOME_COLUMNS}
    row.update({
        "candidate_id": "candidate-1", "strategy_id": cfg["strategy_id"], "profile_id": cfg["profile_id"],
        "shadow_lane": cfg["shadow_lane"], "window": "forward_post_activation",
        "generated_at": entry_at.isoformat(), "decision_at": entry_at.isoformat(), "sweep_at": entry_at.isoformat(),
        "symbol": "TEST/USDT", "direction": "long", "eligibility_status": "eligible",
        "is_clean_for_edge": 1, "entry_ts": entry_at.isoformat(), "entry_price": 100.0,
        "stop_price": 99.0, "tp1": 101.0, "tp2": 102.0, "tp3": 103.0,
        "outcome_status": "open", "last_checked_at": entry_at.isoformat(),
        "liquidation_event_ids_json": ["force-1", "force-2"],
        "features_json": {"rvol": 2.3, "wick_share": 0.7},
        "notes_json": {"paper_untouched": True},
    })
    strategy._upsert(conn, row)
    json_before = conn.execute(
        "SELECT liquidation_event_ids_json,features_json,notes_json "
        "FROM crypto_liquidity_sweep_v1_shadow_outcomes WHERE candidate_id='candidate-1'"
    ).fetchone()
    future = pd.DataFrame([
        {"timestamp": entry_at + timedelta(minutes=5), "open": 100.0,
         "high": 103.2, "low": 100.0, "close": 103.0, "volume": 100.0},
    ])
    monkeypatch.setattr(strategy, "_load_frame", lambda symbol, current_cfg: future)

    assert strategy._mature_open(conn, entry_at + timedelta(minutes=10), cfg) == 1
    result = dict(conn.execute(
        "SELECT outcome_status,close_reason,net_pnl_usd FROM crypto_liquidity_sweep_v1_shadow_outcomes "
        "WHERE candidate_id='candidate-1'"
    ).fetchone())
    assert result["outcome_status"] == "closed"
    assert result["close_reason"] == "tp3_runner"
    assert result["net_pnl_usd"] is not None
    json_after = conn.execute(
        "SELECT liquidation_event_ids_json,features_json,notes_json "
        "FROM crypto_liquidity_sweep_v1_shadow_outcomes WHERE candidate_id='candidate-1'"
    ).fetchone()
    assert tuple(json_after) == tuple(json_before)


def test_private_shadow_tables_are_isolated_and_dry_run_rolls_back(monkeypatch, tmp_path):
    db = tmp_path / "desk.sqlite"
    conn = sqlite3.connect(db)
    forbidden = ("proposed_signals", "signal_outcomes", "final_r", "paper_ledger", "live_routing")
    for table in forbidden:
        conn.execute(f"CREATE TABLE {table}(value TEXT)")
        conn.execute(f"INSERT INTO {table} VALUES('stable')")
    conn.commit()
    conn.close()

    intelligence = sqlite3.connect(":memory:")
    intelligence.execute("CREATE TABLE liquidation_events(event_id TEXT,event_at TEXT,side TEXT,notional_usd REAL,normalized_symbol TEXT)")
    monkeypatch.setattr("src.data_collectors.market_intelligence_store.connect", lambda ensure=False: intelligence)
    monkeypatch.setattr(strategy, "_symbols", lambda intelligence_conn, now, cfg: [])
    result = strategy.tick(db=str(db), persist=False, now=datetime(2026, 8, 20, 12, tzinfo=UTC), cfg=_cfg())
    assert result["enabled"] is True

    conn = sqlite3.connect(db)
    for table in ("crypto_liquidity_sweep_v1_shadow_outcomes", "crypto_liquidity_sweep_v1_shadow_observations"):
        assert conn.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE name=?", (table,)
        ).fetchone()[0] == 0
    for table in forbidden:
        assert conn.execute(f"SELECT value FROM {table}").fetchone()[0] == "stable"
    conn.close()


def test_module_contains_no_writes_to_trading_tables():
    source = inspect.getsource(strategy).lower()
    for table in ("proposed_signals", "signal_outcomes", "final_r", "paper_ledger", "live_routing"):
        assert f"insert into {table}" not in source
        assert f"update {table}" not in source
        assert f"delete from {table}" not in source


def test_monitor_runs_liquidity_sweep_after_fresh_derivatives():
    from scripts import derivatives_monitor

    source = inspect.getsource(derivatives_monitor.current_loop)
    assert source.index("pipeline.refresh_current") < source.index("liquidity_sweep.tick")
    assert "liquidity_sweep_report" in source


def test_bybit_liquidation_side_is_normalized_to_the_forced_order_side():
    from scripts.derivatives_monitor import _bybit_force_order

    long_liquidation = _bybit_force_order({"s": "BTCUSDT", "S": "Buy", "T": 1_770_000_000_000,
                                            "p": "100000", "v": "0.5"})
    short_liquidation = _bybit_force_order({"s": "BTCUSDT", "S": "Sell", "T": 1_770_000_000_001,
                                             "p": "100000", "v": "0.5"})
    assert long_liquidation and long_liquidation[1] == "SELL"
    assert short_liquidation and short_liquidation[1] == "BUY"


def test_okx_liquidation_reads_the_nested_details_array():
    # OKX's real liquidation-orders schema nests per-liquidation fields under
    # event["details"]; the top-level element only carries instId/instType.
    # Reading posSide/side/ts/bkPx/sz off the top level (the previous bug)
    # silently matched nothing on every real message. Confirmed against
    # ccxt's okx.ts parseWsLiquidation, which reads safeList(event,'details').
    from scripts.derivatives_monitor import _okx_force_order

    normalized = _okx_force_order(
        {"instId": "BTC-USDT-SWAP", "instType": "SWAP",
         "details": [{"posSide": "long", "side": "sell", "ts": "1770000000000",
                      "bkPx": "100000", "sz": "2", "ordId": "abc"}]},
        multipliers={"BTC-USDT-SWAP": (0.01, "BTC")},
    )
    assert len(normalized) == 1
    instrument, forced_side, _, price, contracts, notional_usd, _ = normalized[0]
    assert (instrument, forced_side, price, contracts) == ("BTC-USDT-SWAP", "SELL", 100000.0, 2.0)
    assert notional_usd == 2_000.0


def test_okx_liquidation_batches_multiple_details_in_one_push():
    from scripts.derivatives_monitor import _okx_force_order

    normalized = _okx_force_order(
        {"instId": "ETH-USDT-SWAP", "details": [
            {"posSide": "long", "ts": "1770000000000", "bkPx": "3000", "sz": "4"},
            {"posSide": "short", "ts": "1770000001000", "bkPx": "3005", "sz": "1"},
        ]}, multipliers={},
    )
    assert len(normalized) == 2
    assert normalized[0][1] == "SELL" and normalized[0][5] is None  # liquidated long -> forced sell
    assert normalized[1][1] == "BUY"  # liquidated short -> forced buy


def test_okx_liquidation_falls_back_to_flat_payload_without_details():
    # Defensive fallback only -- not the documented shape, but keeps a
    # genuinely flat payload (or an old test fixture) working.
    from scripts.derivatives_monitor import _okx_force_order

    normalized = _okx_force_order(
        {"instId": "ETH-USDT-SWAP", "posSide": "short", "ts": "1770000000000",
         "bkPx": "3000", "sz": "4"}, multipliers={},
    )
    assert len(normalized) == 1
    assert normalized[0][1] == "BUY"
    assert normalized[0][5] is None


def test_monitor_uses_current_binance_market_stream_endpoint():
    from scripts import derivatives_monitor

    source = inspect.getsource(derivatives_monitor.liquidation_loop)
    assert "wss://fstream.binance.com/market/ws/!forceOrder@arr" in source


def test_bybit_monitor_requires_subscription_acknowledgement():
    from scripts import derivatives_monitor

    source = inspect.getsource(derivatives_monitor.bybit_liquidation_loop)
    assert "Bybit liquidation subscription rejected" in source
    assert "_bybit_subscribe_liquidations" in source


def test_okx_monitor_is_observational_and_part_of_the_shared_monitor():
    from scripts import derivatives_monitor

    source = inspect.getsource(derivatives_monitor.okx_liquidation_loop)
    run_source = inspect.getsource(derivatives_monitor.run)
    assert "not an eligibility gate" in source
    assert '"liquidations:okx_ws"' in source
    assert "okx_liquidation_loop" in run_source


def test_bybit_force_order_uses_native_instrument_ids_for_aliases(monkeypatch):
    from scripts import derivatives_monitor

    class Row(dict):
        def __getitem__(self, key):
            return super().__getitem__(key)

    class Conn:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def execute(self, *_args):
            return self
        def fetchall(self):
            return [Row(instrument_id="1000PEPEUSDT")]

    monkeypatch.setattr("src.data_collectors.market_intelligence_store.connect", lambda *args, **kwargs: Conn())
    monkeypatch.setattr(
        "src.execution.crypto_liquidity_sweep_shadow._symbols",
        lambda *_args, **_kwargs: ["PEPE/USDT"],
    )
    assert derivatives_monitor._bybit_liquidation_symbols(SimpleNamespace(db_path="test")) == ["1000PEPEUSDT"]
