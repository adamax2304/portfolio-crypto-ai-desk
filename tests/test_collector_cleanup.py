from __future__ import annotations

from src.data_collectors.binance_collector import BinanceOHLCVCollector
from src.data_collectors.exchange_ohlcv_collector import ExchangeOHLCVCollector


class _Exchange:
    def __init__(self):
        self.markets = {"BTC/USDT": {}}
        self.closed = 0

    def load_markets(self):
        return self.markets

    def fetch_ohlcv(self, symbol, timeframe, limit):
        return [[1_700_000_000_000, 1, 2, 0.5, 1.5, 100]]

    def close(self):
        self.closed += 1


class _Store:
    def save_ohlcv(self, *args, **kwargs):
        return None


class _Config:
    exchange_id = "binance"
    symbols = ["BTC/USDT"]
    timeframes = ["1m"]

    def candle_limit(self, timeframe):
        return 1

    def exchange_enabled(self, exchange):
        return True

    def exchange_ccxt_id(self, exchange):
        return exchange

    def exchange_alias(self, exchange, symbol):
        return symbol


def test_binance_collector_closes_exchange_session(monkeypatch):
    exchange = _Exchange()
    collector = BinanceOHLCVCollector(_Config(), _Store())
    monkeypatch.setattr(collector, "_build_exchange", lambda: exchange)
    assert collector.fetch().fetched == ["BTC/USDT 1m"]
    assert exchange.closed == 1


def test_generic_collector_closes_exchange_session(monkeypatch):
    exchange = _Exchange()
    collector = ExchangeOHLCVCollector("bybit", _Config(), _Store())
    monkeypatch.setattr(collector, "_build_exchange", lambda: exchange)
    assert collector.fetch().fetched == ["BTC/USDT 1m"]
    assert exchange.closed == 1
