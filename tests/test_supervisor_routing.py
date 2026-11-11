from __future__ import annotations

from src.agents.supervisor import Supervisor


def test_plain_language_routing_prioritizes_intraday_validation() -> None:
    query = "update the data and check if morning ideas are still valid"
    assert Supervisor._infer_action(query) == "intraday-report"
    assert Supervisor._should_refresh(query)


def test_plain_language_routing_scan_is_explicit() -> None:
    assert Supervisor._infer_action("scan BTC and SOL") == "scan"
    assert Supervisor._infer_action("find where money and attention are flowing today") == "daily-report"


def test_intraday_no_update_is_strictly_cache_only() -> None:
    supervisor = object.__new__(Supervisor)
    captured = {}

    def fake_daily_report(**kwargs):
        captured.update(kwargs)
        return "cached-report"

    supervisor.daily_report = fake_daily_report

    result = supervisor.intraday_report(symbols=["BTC/USDT"], update=False)

    assert result == "cached-report"
    assert captured["allow_network_fallback"] is False
