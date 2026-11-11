from scripts.paper_portfolio_backfill import authoritative_execution_provenance


def test_legacy_rows_remain_visible_for_historical_continuity():
    assert authoritative_execution_provenance({"entry_time_basis": None}) is True


def test_new_historical_bar_only_execution_is_excluded_from_balance():
    assert authoritative_execution_provenance({
        "entry_time_basis": "historical_bar_range",
        "current_price_revalidated": 0,
    }) is False


def test_point_in_time_execution_is_authoritative():
    assert authoritative_execution_provenance({
        "entry_time_basis": "point_in_time_current_bar",
        "current_price_revalidated": 1,
    }) is True
