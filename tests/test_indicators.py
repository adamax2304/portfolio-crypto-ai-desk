from __future__ import annotations

import pandas as pd

from src.indicators.technicals import enrich_ohlcv, pct_return
from src.indicators.volume_anomaly import volume_ratio


def sample_frame(rows: int = 80) -> pd.DataFrame:
    values = list(range(1, rows + 1))
    return pd.DataFrame(
        {
            "timestamp": pd.date_range("2026-01-01", periods=rows, freq="h", tz="UTC"),
            "open": values,
            "high": [v + 1 for v in values],
            "low": [v - 1 for v in values],
            "close": values,
            "volume": [100 + v for v in values],
        }
    )


def test_enrich_ohlcv_adds_core_columns() -> None:
    frame = enrich_ohlcv(sample_frame())
    for column in ["ema20", "ema50", "atr14", "rsi14", "volume_sma20"]:
        assert column in frame.columns
    assert frame["ema20"].notna().sum() > 0


def test_pct_return_and_volume_ratio() -> None:
    frame = sample_frame()
    assert pct_return(frame, 24) is not None
    assert volume_ratio(frame, 20) is not None
