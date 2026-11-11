from __future__ import annotations

from src.agents.supervisor import Supervisor
from src.config import load_config


def test_supervisor_initialises_and_reports_exchange_status() -> None:
    supervisor = Supervisor(load_config())
    status = supervisor.exchange_status()
    assert status["anchor_exchange"] == "binance"
    assert "binance" in status["per_exchange"]
    assert "bybit" in status["per_exchange"]
    assert "mexc" in status["per_exchange"]


def test_candidate_debug_handles_unknown_symbol_gracefully() -> None:
    supervisor = Supervisor(load_config())
    payload = supervisor.candidate_debug("NONEXISTENT/USDT")
    assert payload["in_fused_universe"] is False
    assert payload["symbol"] == "NONEXISTENT/USDT"


def test_doctor_returns_ready_flag() -> None:
    supervisor = Supervisor(load_config())
    info = supervisor.doctor()
    assert "ready" in info
    assert isinstance(info["ready"], bool)


def test_db_counts_includes_rejected_ideas_table() -> None:
    supervisor = Supervisor(load_config())
    counts = supervisor.db.counts()
    assert "rejected_ideas" in counts
