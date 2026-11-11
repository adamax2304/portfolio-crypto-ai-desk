from __future__ import annotations

import pandas as pd

from src.agents.review_agent import ReviewAgent


def test_post_idea_window_does_not_reuse_pre_idea_candle() -> None:
    frame = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(["2026-01-01T10:00:00Z"], utc=True),
            "open": [100.0],
            "high": [101.0],
            "low": [99.0],
            "close": [100.5],
            "volume": [1000.0],
        }
    )
    window = ReviewAgent._post_idea_window(frame, "2026-01-01T11:00:00Z")
    assert window.empty
