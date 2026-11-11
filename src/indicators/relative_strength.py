from __future__ import annotations

import pandas as pd

from src.indicators.technicals import pct_return


def relative_strength_return(
    asset_frame: pd.DataFrame, benchmark_frame: pd.DataFrame, periods: int
) -> float | None:
    asset_return = pct_return(asset_frame, periods)
    benchmark_return = pct_return(benchmark_frame, periods)
    if asset_return is None or benchmark_return is None:
        return None
    return asset_return - benchmark_return
