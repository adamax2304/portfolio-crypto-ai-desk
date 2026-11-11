"""Resilience tests for the isolated Catalyst-RS Shadow lane."""
from __future__ import annotations

import pandas as pd

from src.execution.stocks_catalyst_rs_shadow import _return_between


def test_missing_sector_frame_is_a_rejection_input_not_a_key_error():
    """A missing ETF cache must later become SECTOR_CONTEXT_MISSING, never
    terminate the whole Shadow refresh with KeyError('timestamp')."""
    assert _return_between(pd.DataFrame(), None, None, 15) is None
