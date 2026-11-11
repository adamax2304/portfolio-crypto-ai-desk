"""Primary/Fallback stocks OHLCV provider chain: Alpaca/Finnhub -> yfinance."""
from __future__ import annotations

import sys
from types import SimpleNamespace

import pandas as pd
import requests

from src.stocks import realtime_provider as rp
from src.stocks.data_collectors import yf_client


class _Response:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def test_yfinance_hourly_period_stays_inside_provider_hard_limit():
    assert yf_client.DEFAULT_PERIODS["1h"] == "729d"


def test_finnhub_is_primary_and_normalizes_candles(monkeypatch):
    monkeypatch.setenv("FINNHUB_API_KEY", "test-key")
    monkeypatch.setattr(rp, "active_provider", lambda: rp.ProviderStatus(
        "finnhub", False, True, "test provider", "FINNHUB_API_KEY"
    ))
    seen = {}

    def fake_get(url, *, params, timeout):
        seen.update({"url": url, "params": params, "timeout": timeout})
        return _Response({"s": "ok", "t": [1_720_000_000, 1_720_000_900],
                          "o": [100.0, 101.0], "h": [101.0, 102.0],
                          "l": [99.0, 100.0], "c": [100.5, 101.5], "v": [10, 11]})

    monkeypatch.setattr("requests.get", fake_get)
    result = yf_client.fetch_ohlcv("AAPL", "15m", period="2d")

    assert result is not None and result.source == "finnhub"
    assert list(result.dataframe.columns) == ["open", "high", "low", "close", "volume"]
    assert str(result.dataframe.index.tz) == "UTC"
    assert seen["params"]["resolution"] == "15"
    assert seen["params"]["token"] == "test-key"


def test_primary_failure_uses_yfinance_fallback(monkeypatch):
    monkeypatch.setenv("FINNHUB_API_KEY", "test-key")
    monkeypatch.setattr(yf_client, "_fetch_primary", lambda *args: None)
    frame = pd.DataFrame({"Open": [10.0], "High": [11.0], "Low": [9.0],
                          "Close": [10.5], "Volume": [50]},
                         index=pd.DatetimeIndex(["2026-07-28"], tz="UTC"))

    class _Ticker:
        def __init__(self, symbol):
            self.symbol = symbol

        def history(self, **kwargs):
            return frame

    monkeypatch.setitem(sys.modules, "yfinance", SimpleNamespace(Ticker=_Ticker, download=lambda *a, **k: frame))
    result = yf_client.fetch_ohlcv("AAPL", "1d", retries=0)

    assert result is not None and result.source == "yfinance"
    assert result.last_close == 10.5


def test_alpaca_market_data_endpoint_is_separate_from_paper_trading(monkeypatch):
    monkeypatch.setenv("ALPACA_API_KEY", "key")
    monkeypatch.setenv("ALPACA_API_SECRET", "secret")
    monkeypatch.setenv("ALPACA_DATA_BASE_URL", "https://data.example.test/v2")
    monkeypatch.setattr(rp, "active_provider", lambda: rp.ProviderStatus(
        "alpaca", True, True, "test provider", "ALPACA_API_KEY"
    ))
    seen = {}

    def fake_get(url, *, params, headers, timeout):
        seen.update(url=url, params=params, headers=headers, timeout=timeout)
        return _Response({"bars": [{
            "t": "2026-09-22T13:30:00Z", "o": 100.0, "h": 101.0,
            "l": 99.5, "c": 100.5, "v": 1000,
        }]})

    monkeypatch.setattr("requests.get", fake_get)
    result = yf_client.fetch_ohlcv("AAPL", "15m", period="2d")

    assert result is not None and result.source == "alpaca"
    assert seen["url"] == "https://data.example.test/v2/stocks/AAPL/bars"
    assert seen["params"]["feed"] == "iex"
    assert seen["params"]["sort"] == "desc"


def test_alpaca_batch_fetches_multiple_symbols_in_one_request(monkeypatch):
    monkeypatch.setenv("ALPACA_API_KEY", "key")
    monkeypatch.setenv("ALPACA_API_SECRET", "secret")
    monkeypatch.setenv("ALPACA_DATA_BASE_URL", "https://data.example.test/v2")
    monkeypatch.setattr(rp, "active_provider", lambda: rp.ProviderStatus(
        "alpaca", True, True, "test provider", "ALPACA_API_KEY"
    ))
    seen = {}

    def fake_get(url, *, params, headers, timeout):
        seen.update(url=url, params=params, headers=headers, timeout=timeout)
        return _Response({"bars": {
            "AAPL": [{"t": "2026-09-22T13:30:00Z", "o": 100.0, "h": 101.0,
                      "l": 99.5, "c": 100.5, "v": 1000}],
            "MSFT": [{"t": "2026-09-22T13:30:00Z", "o": 200.0, "h": 201.0,
                      "l": 199.5, "c": 200.5, "v": 2000}],
        }, "next_page_token": None})

    monkeypatch.setattr("requests.get", fake_get)
    result = yf_client.fetch_ohlcv_batch(["AAPL", "MSFT"], "15m", period="2d")

    assert set(result) == {"AAPL", "MSFT"}
    assert all(item.source == "alpaca_batch" for item in result.values())
    assert seen["url"] == "https://data.example.test/v2/stocks/bars"
    assert seen["params"]["symbols"] == "AAPL,MSFT"
    assert seen["params"]["sort"] == "asc"


def test_yfinance_batch_fallback_normalizes_multi_ticker(monkeypatch):
    index = pd.DatetimeIndex(["2026-09-22T13:30:00Z"])
    columns = pd.MultiIndex.from_product([
        ["AAPL", "MSFT"], ["Open", "High", "Low", "Close", "Volume"],
    ])
    frame = pd.DataFrame(
        [[100.0, 101.0, 99.0, 100.5, 1000, 200.0, 201.0, 199.0, 200.5, 2000]],
        index=index, columns=columns,
    )
    monkeypatch.setitem(
        sys.modules, "yfinance",
        SimpleNamespace(download=lambda **kwargs: frame),
    )

    result = yf_client._fetch_yfinance_batch(["AAPL", "MSFT"], "15m", period="2d")

    assert set(result) == {"AAPL", "MSFT"}
    assert result["AAPL"].source == "yfinance_batch"
    assert result["AAPL"].last_close == 100.5
    assert result["MSFT"].last_close == 200.5


def test_alpaca_auth_failure_stops_chunk_retries_and_uses_fallback(monkeypatch):
    monkeypatch.setenv("ALPACA_API_KEY", "key")
    monkeypatch.setenv("ALPACA_API_SECRET", "secret")
    monkeypatch.setattr(yf_client, "_ALPACA_AUTH_DISABLED_UNTIL", 0.0)
    monkeypatch.setattr(rp, "active_provider", lambda: rp.ProviderStatus(
        "alpaca", True, True, "test provider", "ALPACA_API_KEY"
    ))
    calls = []

    class Unauthorized:
        status_code = 401

        def raise_for_status(self):
            error = requests.HTTPError("unauthorized")
            error.response = self
            raise error

    monkeypatch.setattr(
        "requests.get",
        lambda *args, **kwargs: calls.append((args, kwargs)) or Unauthorized(),
    )
    monkeypatch.setattr(
        yf_client, "_fetch_yfinance_batch",
        lambda symbols, interval, period=None: {symbol: object() for symbol in symbols},
    )
    symbols = [f"S{index}" for index in range(30)]

    result = yf_client.fetch_ohlcv_batch(symbols, "15m", period="2d", chunk_size=10)

    assert len(calls) == 1
    assert set(result) == set(symbols)
    assert yf_client._alpaca_auth_disabled() is True


def test_missing_finnhub_credential_falls_back_to_yfinance_status(monkeypatch):
    monkeypatch.setenv("FINNHUB_API_KEY", "")
    for env in ("ALPACA_API_KEY", "POLYGON_API_KEY", "IEX_API_KEY", "IBKR_ACCOUNT"):
        monkeypatch.setenv(env, "")
    assert rp.active_provider().name == "yfinance"


def test_finnhub_quote_is_explicit_and_never_synthetic_ohlcv(monkeypatch):
    monkeypatch.setenv("FINNHUB_API_KEY", "test-key")

    def fake_get(url, *, params, timeout):
        assert url.endswith("/quote")
        assert params["symbol"] == "AAPL"
        return _Response({"c": 123.45, "t": 1_720_000_000})

    monkeypatch.setattr("requests.get", fake_get)
    quote = rp.finnhub_quote("aapl")
    assert quote["ok"] is True and quote["price"] == 123.45
    assert quote["source"] == "finnhub" and quote["observed_at"]

