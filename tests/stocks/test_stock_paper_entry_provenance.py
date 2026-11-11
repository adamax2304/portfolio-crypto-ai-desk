from src.stocks.entry_provenance import (
    accepted_stock_intraday_paper_bases,
    is_accepted_stock_intraday_paper_basis,
    paper_provenance_rank,
)


def test_delayed_provider_is_config_gated():
    enabled = {"intraday_guards": {"paper_entry_provenance": {
        "accept_provider_delayed_current_bar": True,
    }}}
    disabled = {"intraday_guards": {"paper_entry_provenance": {
        "accept_provider_delayed_current_bar": False,
    }}}
    assert "provider_delayed_current_bar" in accepted_stock_intraday_paper_bases(enabled)
    assert is_accepted_stock_intraday_paper_basis("provider_delayed_current_bar", enabled)
    assert not is_accepted_stock_intraday_paper_basis("provider_delayed_current_bar", disabled)


def test_point_in_time_remains_valid_and_ranks_above_delayed():
    enabled = {"intraday_guards": {"paper_entry_provenance": {
        "accept_provider_delayed_current_bar": True,
    }}}
    assert is_accepted_stock_intraday_paper_basis("point_in_time_current_bar", enabled)
    assert paper_provenance_rank(
        "point_in_time_current_bar", stocks_intraday=True, risk=enabled,
    ) > paper_provenance_rank(
        "provider_delayed_current_bar", stocks_intraday=True, risk=enabled,
    )


def test_crypto_does_not_gain_delayed_provider_acceptance():
    enabled = {"intraday_guards": {"paper_entry_provenance": {
        "accept_provider_delayed_current_bar": True,
    }}}
    assert paper_provenance_rank(
        "provider_delayed_current_bar", stocks_intraday=False, risk=enabled,
    ) == 0
