from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.data_collectors import market_intelligence_store as mi
from src.data_collectors.liquidity_collector import LiquidityCollector, book_metrics


NOW = datetime(2026, 7, 23, 12, 0, tzinfo=timezone.utc)


def test_book_metrics_calculates_spread_and_visible_usd_depth():
    result = book_metrics(
        bids=[[100.0, 2.0], [99.85, 3.0], [99.60, 4.0]],
        asks=[[100.10, 1.0], [100.20, 3.0], [100.50, 5.0]],
    )
    assert result["quality_status"] == "ok"
    assert round(result["spread_bps"], 3) == 10.0
    assert result["bid_depth_10bps_usd"] == 200.0
    assert result["ask_depth_10bps_usd"] == 100.1
    assert result["bid_depth_25bps_usd"] == pytest.approx(499.55)
    assert result["ask_depth_25bps_usd"] == pytest.approx(400.7)


def test_book_metrics_refuses_to_label_contract_count_as_usd_depth():
    result = book_metrics(bids=[[100, 2]], asks=[[100.1, 2]], quantity_multiplier=None)
    assert result["quality_status"] == "bbo_only_multiplier_unknown"
    assert result["spread_bps"] is not None
    assert result["bid_depth_10bps_usd"] is None
    assert result["ask_depth_10bps_usd"] is None


def test_liquidity_context_is_point_in_time_and_ignores_future_book(tmp_path):
    with mi.connect(tmp_path / "intelligence.sqlite") as conn:
        for exchange in ("binance", "mexc"):
            assert mi.insert_liquidity_snapshot(
                conn, provider_ts="2026-07-23T11:58:00+00:00", exchange=exchange,
                symbol="BTC/USDT", best_bid=100, best_ask=100.1, mid_price=100.05,
                spread_bps=10, bid_depth_10bps_usd=1_000, ask_depth_10bps_usd=1_000,
            )
            assert mi.insert_liquidity_snapshot(
                conn, provider_ts="2026-07-23T12:05:00+00:00", exchange=exchange,
                symbol="BTC/USDT", best_bid=90, best_ask=110, mid_price=100,
                spread_bps=2_000, bid_depth_10bps_usd=1, ask_depth_10bps_usd=1,
            )
        context = mi.latest_liquidity_context(conn, "BTC/USDT", as_of=NOW, max_age_minutes=10)
    assert context["status"] == "ok"
    assert context["venue_count"] == 2
    assert context["spread_bps"] == 10
    assert context["bid_depth_10bps_usd"] == 1_000


def test_collector_persists_public_binance_bybit_and_mexc_rows(tmp_path, monkeypatch):
    class Response:
        def __init__(self, payload):
            self.payload = payload

        def raise_for_status(self):
            return None

        def json(self):
            return self.payload

    class Session:
        def get(self, url, params=None, timeout=None):
            if "fapi.binance.com" in url:
                return Response({"E": 1_785_000_000_000, "bids": [["100", "2"]], "asks": [["100.1", "3"]]})
            if "api.bybit.com" in url:
                return Response({"retCode": 0, "result": {"ts": 1_785_000_000_000,
                                                           "b": [["100", "4"]], "a": [["100.1", "5"]]}})
            if url.endswith("/contract/detail"):
                return Response({"data": [{"contractSize": "0.1"}]})
            if "/contract/depth/" in url:
                return Response({"data": {"timestamp": 1_785_000_000_000,
                                           "bids": [["100", "20"]], "asks": [["100.1", "30"]]}})
            raise AssertionError(url)

    collector = LiquidityCollector(db_path=tmp_path / "intelligence.sqlite", session=Session())
    getters = {"binance": collector._binance_row, "bybit": collector._bybit_row, "mexc": collector._mexc_row}
    monkeypatch.setattr(collector, "_collect_exchange", lambda name, symbols: ([getters[name]("BTC/USDT")], []))
    result = collector.refresh(["BTC/USDT"])
    assert result["written"] == 3
    with mi.connect(tmp_path / "intelligence.sqlite") as conn:
        rows = conn.execute(
            "SELECT exchange, quality_status, bid_depth_10bps_usd FROM liquidity_snapshots ORDER BY exchange"
        ).fetchall()
        health = conn.execute("SELECT status FROM intelligence_source_health WHERE source='liquidity:bybit'").fetchone()
    assert [tuple(row)[:2] for row in rows] == [("binance", "ok"), ("bybit", "ok"), ("mexc", "ok")]
    assert rows[2][2] == 200.0
    assert health[0] == "ok"


def test_bybit_alias_uses_native_linear_instrument(tmp_path):
    collector = LiquidityCollector(db_path=tmp_path / "intelligence.sqlite")
    assert collector._bybit_symbol("PEPE/USDT") == "1000PEPEUSDT"
