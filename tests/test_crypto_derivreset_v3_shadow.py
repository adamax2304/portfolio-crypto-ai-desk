from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone

import pandas as pd

from src.execution import crypto_derivreset_v3_shadow as strategy


UTC = timezone.utc


def _cfg() -> dict:
    cfg = strategy.load_strategy_config()
    cfg.update(feature_flag=True, max_symbols=0, min_rvol=1.0)
    return cfg


def _frame() -> pd.DataFrame:
    start = datetime(2026, 7, 26, 9, 0, tzinfo=UTC)
    rows = []
    for index in range(40):
        close = 100.0 + index * 0.08
        rows.append({"timestamp": start + timedelta(minutes=index * 5), "open": close - 0.05,
                     "high": close + 0.18, "low": close - 0.18, "close": close, "volume": 100.0})
    # Index 27 is an observable downside flush. Its reclaim arrives only at
    # bars 32/33, after the initial flush bar has already closed.
    level = rows[26]["close"]
    rows[27].update(open=level, high=level + 0.2, low=level - 1.1, close=level - 0.30, volume=220.0)
    for index in range(28, 32):
        rows[index].update(close=level - 0.15, low=level - 0.28, high=level + 0.05, volume=110.0)
    rows[32].update(close=level + 0.20, low=level - 0.02, high=level + 0.35, volume=180.0)
    rows[33].update(close=level + 0.38, low=level + 0.12, high=level + 0.55, volume=190.0)
    return pd.DataFrame(rows)


def _derivatives(as_of: datetime) -> list[dict]:
    points = [
        (as_of - timedelta(minutes=110), 100.0, 0.00030),
        (as_of - timedelta(minutes=75), 104.0, 0.00028),
        (as_of - timedelta(minutes=35), 99.0, 0.00016),
        (as_of - timedelta(minutes=5), 98.0, 0.00008),
    ]
    return [{"provider_ts": at.isoformat(), "received_at": at.isoformat(), "oi_usd": oi,
             "funding_rate_8h": funding, "raw_json": json.dumps({"turnover24h": "30000000", "bid1Price": "100",
                                                                        "ask1Price": "100.02"})}
            for at, oi, funding in points]


def test_fresh_universe_query_uses_exchange_time_index_and_canonical_case():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE derivative_snapshots(id INTEGER PRIMARY KEY, normalized_symbol TEXT, "
                 "raw_json TEXT, exchange TEXT, provider_ts TEXT)")
    conn.execute("CREATE INDEX idx_deriv_exchange_ts ON derivative_snapshots(exchange, provider_ts)")
    now = datetime(2026, 10, 20, 16, 0, tzinfo=UTC)
    recent = (now - timedelta(minutes=2)).isoformat()
    conn.executemany("INSERT INTO derivative_snapshots VALUES(?,?,?,?,?)", [
        (1, "BTCUSDT", json.dumps({"turnover24h": 30_000_000}), "bybit", recent),
        (2, "ETHUSDT", json.dumps({"turnover24h": 20_000_000}), "BYBIT", recent),
    ])
    cfg = {"primary_exchange": "bybit", "derivative_freshness_minutes": 12, "max_symbols": 60}

    assert strategy._symbols(conn, now, cfg) == ["BTC/USDT"]
    plan = conn.execute(
        "EXPLAIN QUERY PLAN SELECT normalized_symbol,raw_json,provider_ts FROM derivative_snapshots "
        "WHERE exchange=? AND provider_ts>=? AND provider_ts<=? "
        "ORDER BY normalized_symbol,provider_ts DESC,id DESC",
        ("bybit", (now - timedelta(minutes=12)).isoformat(), now.isoformat()),
    ).fetchall()
    assert any("SEARCH derivative_snapshots USING INDEX idx_deriv_exchange_ts" in row[3]
               for row in plan)
    conn.close()


def test_event_sequence_can_confirm_after_the_initial_two_bar_window():
    cfg, frame = _cfg(), _frame()
    seed = strategy._seed_structure(frame, 27, cfg)
    assert seed["ok"] is True
    event = strategy._event_row(cfg, "TEST/USDT", seed, seed["flush_at"], {"oi_peak": 104.0,
                                                                                "funding_extreme": 0.0003})
    reclaim = strategy._reclaim_structure(frame, 33, event, cfg)
    assert reclaim["ok"] is True
    assert reclaim["decision_at"] - seed["flush_at"] == timedelta(minutes=30)


def test_confirmation_requires_measurable_reset_and_neutral_funding():
    cfg, frame = _cfg(), _frame()
    seed = strategy._seed_structure(frame, 27, cfg)
    decision_at = frame.loc[33, "timestamp"].to_pydatetime() + timedelta(minutes=5)
    good = strategy._derivative_context(_derivatives(decision_at), as_of=decision_at,
                                         flush_at=seed["flush_at"], direction="long", cfg=cfg,
                                         require_reset=True)
    assert good["ok"] is True
    assert good["oi_drop_pct"] >= cfg["min_oi_drop_from_peak_pct"]

    no_reset = _derivatives(decision_at)
    no_reset[-1]["oi_usd"] = 103.9
    failed = strategy._derivative_context(no_reset, as_of=decision_at, flush_at=seed["flush_at"],
                                           direction="long", cfg=cfg, require_reset=True)
    assert failed["reason"] == "OI_DID_NOT_RESET"


def test_unsafe_oi_rebuild_is_detectable_after_a_reclaim():
    cfg, frame = _cfg(), _frame()
    seed = strategy._seed_structure(frame, 27, cfg)
    decision_at = frame.loc[33, "timestamp"].to_pydatetime() + timedelta(minutes=5)
    rows = _derivatives(decision_at)
    rows.append({"provider_ts": (decision_at - timedelta(minutes=20)).isoformat(),
                 "received_at": (decision_at - timedelta(minutes=20)).isoformat(), "oi_usd": 96.0,
                 "funding_rate_8h": 0.00012, "raw_json": "{}"})
    rows[-2]["oi_usd"] = 98.0
    values = strategy._derivative_context(rows, as_of=decision_at, flush_at=seed["flush_at"],
                                           direction="long", cfg=cfg, require_reset=True)
    assert values["ok"] is True
    assert values["oi_rebuild_pct"] > cfg["max_oi_rebuild_from_trough_pct"]


def test_v3_tick_never_writes_trading_tables(monkeypatch, tmp_path):
    db = tmp_path / "desk.sqlite"
    conn = sqlite3.connect(db)
    for table in ("proposed_signals", "signal_outcomes", "final_r", "paper_ledger", "live_routing"):
        conn.execute(f"CREATE TABLE {table}(id INTEGER PRIMARY KEY, value TEXT)")
        conn.execute(f"INSERT INTO {table}(value) VALUES ('stable')")
    conn.commit()
    before = {table: conn.execute(f"SELECT * FROM {table}").fetchall() for table in (
        "proposed_signals", "signal_outcomes", "final_r", "paper_ledger", "live_routing"
    )}
    conn.close()

    intelligence = sqlite3.connect(":memory:")
    intelligence.execute("CREATE TABLE derivative_snapshots(id INTEGER PRIMARY KEY, normalized_symbol TEXT, raw_json TEXT, "
                         "exchange TEXT, provider_ts TEXT, received_at TEXT, oi_usd REAL, funding_rate_8h REAL)")
    monkeypatch.setattr("src.data_collectors.market_intelligence_store.connect", lambda ensure=False: intelligence)
    result = strategy.tick(db=str(db), cfg=_cfg(), now=datetime(2026, 7, 26, 12, tzinfo=UTC))
    assert result["enabled"] is True
    assert result["summary"]["clean_closed"] == 0
    assert "Event Funnel" in strategy.render_markdown(result)

    conn = sqlite3.connect(db)
    for table, expected in before.items():
        assert conn.execute(f"SELECT * FROM {table}").fetchall() == expected
    assert conn.execute("SELECT COUNT(*) FROM crypto_derivreset_v3_shadow_evaluations").fetchone()[0] == 1
    conn.close()


def test_v3_dry_run_rolls_back_its_private_tables(monkeypatch, tmp_path):
    db = tmp_path / "desk.sqlite"
    intelligence = sqlite3.connect(":memory:")
    intelligence.execute("CREATE TABLE derivative_snapshots(id INTEGER PRIMARY KEY, normalized_symbol TEXT, raw_json TEXT, "
                         "exchange TEXT, provider_ts TEXT, received_at TEXT, oi_usd REAL, funding_rate_8h REAL)")
    monkeypatch.setattr("src.data_collectors.market_intelligence_store.connect", lambda ensure=False: intelligence)
    strategy.tick(db=str(db), persist=False, cfg=_cfg(), now=datetime(2026, 7, 26, 12, tzinfo=UTC))
    conn = sqlite3.connect(db)
    assert conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE name='crypto_derivreset_v3_shadow_events'").fetchone()[0] == 0
    conn.close()


def test_crypto_catalyst_context_queries_the_canonical_event_table():
    now = datetime(2026, 7, 26, 12, tzinfo=UTC)
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE news_canonical_events(trusted_symbols_json TEXT, effective_at TEXT, published_at TEXT, "
                 "available_at TEXT, event_latency_class TEXT, created_at TEXT, asset_class TEXT, "
                 "linkage_allowed INTEGER, is_cluster_primary INTEGER)")
    conn.execute("INSERT INTO news_canonical_events VALUES (?,?,?,?,?,?,?,?,?)",
                 (json.dumps(["TEST"]), now.isoformat(), now.isoformat(), now.isoformat(), "FAST_EVENT",
                  now.isoformat(), "crypto", 1, 1))
    assert strategy._catalyst_state(conn, "TEST/USDT", now, _cfg()) == "fresh"
    conn.close()
