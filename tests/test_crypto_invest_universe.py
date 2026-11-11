from __future__ import annotations

from datetime import datetime, timezone

from src.data_collectors.crypto_invest_universe import (
    load_selected_symbols, rank_universe,
)


NOW = datetime(2026, 8, 7, tzinfo=timezone.utc)
OLD = int((NOW.timestamp() - 500 * 86400) * 1000)


def _config() -> dict:
    return {
        "selection_count": 2,
        "excluded_bases": ["USDC"],
        "selection_rules": {
            "max_market_cap_rank": 250,
            "min_market_cap_usd": 100,
            "min_global_volume_24h_usd": 10,
            "min_binance_futures_age_days": 365,
            "min_mexc_contract_age_days": 180,
            "min_active_derivatives_venues": 2,
            "score_weights": {
                "global_volume": 0.45,
                "aggregate_derivatives_volume": 0.30,
                "market_cap": 0.20,
                "venue_breadth": 0.05,
            },
        },
    }


def test_rank_requires_old_binance_and_live_mexc_contracts() -> None:
    payloads = {
        "coingecko": [
            {"symbol": "aaa", "name": "AAA", "market_cap_rank": 2,
             "market_cap": 1000, "total_volume": 500},
            {"symbol": "bbb", "name": "BBB", "market_cap_rank": 3,
             "market_cap": 900, "total_volume": 400},
            {"symbol": "new", "name": "NEW", "market_cap_rank": 1,
             "market_cap": 2000, "total_volume": 2000},
            {"symbol": "usdc", "name": "USDC", "market_cap_rank": 4,
             "market_cap": 5000, "total_volume": 5000},
        ],
        "binance_contracts": [
            {"symbol": "AAAUSDT", "status": "TRADING", "contractType": "PERPETUAL", "onboardDate": OLD},
            {"symbol": "BBBUSDT", "status": "TRADING", "contractType": "PERPETUAL", "onboardDate": OLD},
            {"symbol": "NEWUSDT", "status": "TRADING", "contractType": "PERPETUAL",
             "onboardDate": int((NOW.timestamp() - 10 * 86400) * 1000)},
        ],
        "binance_tickers": [
            {"symbol": "AAAUSDT", "quoteVolume": "100"},
            {"symbol": "BBBUSDT", "quoteVolume": "80"},
            {"symbol": "NEWUSDT", "quoteVolume": "5000"},
        ],
        "bybit_tickers": [
            {"symbol": "AAAUSDT", "turnover24h": "50"},
            {"symbol": "BBBUSDT", "turnover24h": "40"},
        ],
        "mexc_contracts": [
            {"symbol": "AAA_USDT", "state": 0, "apiAllowed": True,
             "quoteCoin": "USDT", "createTime": OLD},
            {"symbol": "BBB_USDT", "state": 0, "apiAllowed": True,
             "quoteCoin": "USDT", "createTime": OLD},
            {"symbol": "NEW_USDT", "state": 0, "apiAllowed": True,
             "quoteCoin": "USDT", "createTime": OLD},
        ],
        "mexc_tickers": [
            {"symbol": "AAA_USDT", "amount24": "60"},
            {"symbol": "BBB_USDT", "amount24": "30"},
            {"symbol": "NEW_USDT", "amount24": "5000"},
        ],
    }
    result = rank_universe(payloads, config=_config(), now=NOW)
    assert result.selected_symbols == ["AAA/USDT", "BBB/USDT"]
    assert result.rejected_counts["binance_contract_unavailable_or_too_new"] == 1
    assert result.rejected_counts["excluded_asset"] == 1


def test_checked_in_crypto_invest_universe_is_exactly_60_unique_symbols() -> None:
    symbols = load_selected_symbols()
    assert len(symbols) == 60
    assert len(set(symbols)) == 60
    assert {"BTC/USDT", "ETH/USDT", "FET/USDT", "PYTH/USDT"} <= set(symbols)

