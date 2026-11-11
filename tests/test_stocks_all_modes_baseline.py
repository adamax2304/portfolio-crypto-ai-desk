from pathlib import Path

from src.backtest import stocks_all_modes as baseline
from src.backtest import stocks_position_v2_historical as position_history


def test_metric_uses_net_usd_and_drawdown():
    assert baseline._metric([10.0, -4.0, 2.0]) == {
        "closed": 3,
        "net_pnl_usd": 8.0,
        "profit_factor": 3.0,
        "winrate": 0.6667,
        "max_drawdown_usd": 4.0,
    }


def test_baseline_module_is_read_only():
    source = Path(baseline.__file__).read_text(encoding="utf-8").upper()
    for forbidden in ("INSERT INTO", "UPDATE PROPOSED_SIGNALS", "DELETE FROM", "ALTER TABLE", "DROP TABLE"):
        assert forbidden not in source


def test_markdown_states_that_report_does_not_promote():
    result = {
        "modes": [{
            "family": "test", "implementation": "test", "evidence": "forward",
            "metrics": {"closed": 1, "net_pnl_usd": 1.0, "profit_factor": None},
            "verdict": "UNDERPOWERED", "reason": "test", "source": "fixture",
        }],
        "news_attribution": {
            "canonical_stock_events": {"n": 0, "first_at": None, "last_at": None},
            "causal_preus_reviews": {"n": 0, "causal": 0},
            "paper_exit_catalyst_label_coverage": {"exits": 0, "labelled": 0},
            "preus_outcomes_by_review_verdict": [],
            "technical_outcomes_by_causal_news_state": [],
            "conclusion": "No evidence.",
        },
    }
    rendered = baseline.render_markdown(result)
    assert "No strategy was changed or promoted" in rendered
    assert "UNDERPOWERED" in rendered


def test_position_historical_metrics_are_net_usd_based():
    rows = [
        {"status": "closed", "net_pnl_usd": 8.0, "symbol": "AAPL", "entry_date": "2026-01-01"},
        {"status": "closed", "net_pnl_usd": -2.0, "symbol": "MSFT", "entry_date": "2026-01-02"},
        {"status": "no_entry", "net_pnl_usd": 100.0, "symbol": "NVDA", "entry_date": None},
    ]
    result = position_history._metrics(rows)
    assert result["closed"] == 2
    assert result["net_pnl_usd"] == 6.0
    assert result["profit_factor"] == 4.0


def test_position_historical_adapter_cannot_route_or_open_trading_db():
    source = Path(position_history.__file__).read_text(encoding="utf-8").upper()
    for forbidden in ("PROPOSED_SIGNALS", "PAPER_PORTFOLIO_LEDGER", "LIVE_EXECUTION", "SQLITE3.CONNECT"):
        assert forbidden not in source
