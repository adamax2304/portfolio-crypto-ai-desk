from __future__ import annotations

import pandas as pd

from src.config import load_config
from src.data_collectors.binance_universe_collector import BinanceUniverseCollector
from src.storage.file_store import FileStore


def _collector() -> BinanceUniverseCollector:
    config = load_config()
    return BinanceUniverseCollector(config, FileStore(config))


def _market(
    symbol: str = "SOL/USDT",
    *,
    base: str = "SOL",
    quote: str = "USDT",
    active: bool = True,
    spot: bool = True,
    swap: bool = False,
    market_id: str | None = None,
) -> dict:
    return {
        "symbol": symbol,
        "base": base,
        "quote": quote,
        "active": active,
        "spot": spot,
        "swap": swap,
        "id": market_id or symbol.replace("/", ""),
    }


def test_universe_excludes_invalid_or_non_ascii_symbols() -> None:
    collector = _collector()
    reason = collector._exclusion_reason(
        "å¸币/USDT",
        _market("å¸币/USDT", base="å¸币"),
        "spot",
        "USDT",
    )
    assert reason == "invalid_or_non_ascii_symbol"


def test_universe_excludes_stable_and_fiat_bases() -> None:
    collector = _collector()
    reason = collector._exclusion_reason(
        "FRAX/USDT",
        _market("FRAX/USDT", base="FRAX"),
        "spot",
        "USDT",
    )
    assert reason == "stable_or_fiat_base"


def test_universe_excludes_wrong_market_type() -> None:
    collector = _collector()
    reason = collector._exclusion_reason(
        "SOL/USDT",
        _market("SOL/USDT", base="SOL", spot=False, swap=True),
        "spot",
        "USDT",
    )
    assert reason == "not_spot"


def test_universe_accepts_clean_spot_usdt_symbol() -> None:
    collector = _collector()
    reason = collector._exclusion_reason(
        "SOL/USDT",
        _market("SOL/USDT", base="SOL"),
        "spot",
        "USDT",
    )
    assert reason is None


def test_universe_spread_percent_handles_missing_or_valid_ticker() -> None:
    assert BinanceUniverseCollector._spread_pct({}) is None
    assert BinanceUniverseCollector._spread_pct({"bid": 99, "ask": 101}) == 2.0


def test_universe_change_horizons_use_scalp_timeframes() -> None:
    collector = _collector()
    frame = pd.DataFrame(
        {
            "timestamp": pd.date_range("2026-01-01", periods=120, freq="15min", tz="UTC"),
            "open": range(100, 220),
            "high": range(101, 221),
            "low": range(99, 219),
            "close": range(100, 220),
            "volume": [1000] * 120,
        }
    )
    frames = {"15m": frame}
    assert collector._change_for_horizon(frames, "4h") is not None
    assert collector._change_for_horizon(frames, "24h") is not None
