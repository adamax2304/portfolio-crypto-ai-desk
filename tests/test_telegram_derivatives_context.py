"""Funding/OI Telegram rendering is read-only and explicit."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from src.data_collectors import market_intelligence_store as mi
from src.notifiers.close_alert import decide_close
from src.notifiers.derivatives_context import current_snapshot, telegram_lines
from src.notifiers.paper_entry import decide_paper_entry
from src.notifiers.setup_alert import render_setup_alert
from src.signals.catalyst_labels import telegram_block


NOW = datetime(2026, 7, 22, 10, 0, tzinfo=timezone.utc)


def _signal() -> dict:
    return {
        "signal_id": "sig_deriv_telegram",
        "asset_class": "crypto",
        "symbol": "EPIC/USDT",
        "direction": "long",
        "mode": "intraday",
        "tier": "B",
        "score": 72.0,
        "entry_low": 0.55,
        "entry_high": 0.56,
        "entry_trigger": 0.56,
        "suggested_entry": 0.56,
        "stop_loss": 0.54,
        "invalidation": 0.54,
        "tp1": 0.58,
        "tp2": 0.60,
        "tp3": 0.64,
        "thesis": "EPIC continuation setup.",
        "setup_type": "pullback",
        "news_supported": 0,
        "raw_idea_json": "{}",
    }


def _write_context(path):
    with mi.connect(path) as conn:
        for exchange, funding, oi_now, oi_then in (
            ("binance", 0.00005, 6_000_000.0, 5_000_000.0),
            ("bybit", 0.00007, 4_000_000.0, 3_000_000.0),
        ):
            mi.insert_derivative_snapshot(
                conn, provider_ts=(NOW - timedelta(hours=24)).isoformat(),
                exchange=exchange, symbol="EPIC/USDT", funding_rate=funding,
                funding_interval_hours=8, oi_usd=oi_then, mark_price=0.50,
            )
            mi.insert_derivative_snapshot(
                conn, provider_ts=(NOW - timedelta(minutes=5)).isoformat(),
                exchange=exchange, symbol="EPIC/USDT", funding_rate=funding,
                funding_interval_hours=8, oi_usd=oi_now, mark_price=0.56,
            )
        conn.commit()


def test_fresh_multi_venue_values_render_in_setup_and_paper(monkeypatch, tmp_path):
    path = tmp_path / "market_intelligence.sqlite"
    _write_context(path)
    monkeypatch.setattr(mi, "default_db_path", lambda: path)

    snapshot = current_snapshot("EPIC/USDT", now=NOW)
    assert snapshot["source"] == "fresh_multi_venue_snapshot"
    assert snapshot["funding_rate_8h"] == pytest.approx(0.00006)
    assert snapshot["oi_usd"] == 10_000_000.0
    assert snapshot["oi_change_24h_pct"] == pytest.approx(26.66666667)

    lines, resolved = telegram_lines(_signal(), now=NOW)
    assert resolved["source"] == "fresh_multi_venue_snapshot"
    assert lines[0] == "Funding (8h): +0.0060% · normal · 2 venues · 5m old"
    assert lines[1] == "Open interest: $10.00M · 24h median +26.7% · 2 venues · 5m old"

    from src.notifiers import derivatives_context
    monkeypatch.setattr(derivatives_context, "current_snapshot", lambda *args, **kwargs: snapshot)
    setup = render_setup_alert(_signal())
    paper = decide_paper_entry(
        _signal(), prev_status="waiting_for_entry", entry_triggered=True,
        entry_triggered_at=NOW.isoformat(), entry_price_used=0.56,
    )
    assert "Funding (8h): +0.0060%" in setup
    assert "Open interest: $10.00M" in setup
    assert paper.should_send is True
    assert "Funding (8h): +0.0060%" in paper.message
    assert "Open interest: $10.00M" in paper.message


def test_proposal_snapshot_is_labelled_when_fresh_data_is_missing(monkeypatch):
    from src.notifiers import derivatives_context

    monkeypatch.setattr(derivatives_context, "current_snapshot", lambda *args, **kwargs: {})
    signal = {
        **_signal(),
        "derivatives_at_proposal": {
            "funding_rate": -0.0002,
            "crowding_risk": "short_crowded",
            "open_interest_value": 1_250_000.0,
            "oi_change_pct": -7.5,
        },
    }
    lines, resolved = telegram_lines(signal, now=NOW)
    assert resolved["source"] == "proposal_snapshot"
    assert "-0.0200%" in lines[0] and "at proposal" in lines[0]
    assert "$1.25M" in lines[1] and "24h -7.5%" in lines[1]


def test_supervisor_setup_keeps_proposal_snapshot_when_collector_is_late(monkeypatch):
    from src.agents.supervisor import Supervisor
    from src.models import TradeIdea
    from src.notifiers import derivatives_context

    monkeypatch.setattr(derivatives_context, "current_snapshot", lambda *args, **kwargs: {})
    idea = TradeIdea(
        symbol="EPIC/USDT", direction="long", score=72.0, confidence="medium",
        risk_level="medium", timeframe="15m", tier="B", mode="intraday",
        asset_class="crypto", exchange_focus="binance", exchanges_confirmed=["binance"],
        data_confidence="medium", thesis="EPIC continuation.", evidence=["level hold"],
        counterarguments=["liquidity"], entry_plan="zone", invalidation="0.54",
        targets=["0.58", "0.60", "0.64"], what_to_monitor=["BTC"],
        avoid_conditions=["spread"], data_sources_used=["derivatives"], raw={
            "setup": {"entry_low": 0.55, "entry_high": 0.56, "invalidation": 0.54,
                      "tp1": 0.58, "tp2": 0.60, "tp3": 0.64},
            "derivatives": {
                "data_available": True, "funding_rate": 0.0001,
                "crowding_risk": "normal", "open_interest_value": 3_500_000.0,
            },
        },
    )
    message = Supervisor._format_idea_alert(idea, mode="intraday", report_id="r1", signal_id="sig_ivy")
    assert "Funding (8h): +0.0100%" in message
    assert "Open interest: $3.50M" in message
    assert "at proposal" in message


def test_stocks_remain_explicitly_not_applicable():
    lines = telegram_block({"asset_class": "stocks", "news_supported": 0, "symbol": "AAPL"}, now=NOW)
    assert lines == ["Catalyst: none", "Funding/OI: not available for stocks", "Move type: technical momentum"]


def test_close_alert_carries_derivatives_context(monkeypatch):
    from src.notifiers import derivatives_context

    snapshot = {
        "source": "fresh_multi_venue_snapshot", "funding_rate_8h": 0.00005,
        "funding_state": "normal", "oi_usd": 2_000_000.0,
        "venue_count": 2, "age_seconds": 120,
    }
    monkeypatch.setattr(derivatives_context, "current_snapshot", lambda *args, **kwargs: snapshot)
    outcome = {
        "final_outcome": "loss", "status": "stopped", "entry_triggered": 1,
        "entry_triggered_at": NOW.isoformat(), "stop_hit": 1,
        "stop_hit_at": (NOW + timedelta(minutes=10)).isoformat(), "final_r": -1.0,
    }
    decision = decide_close(_signal(), outcome, prev_status="triggered")
    assert decision.should_send is True
    assert "Funding (8h): +0.0050%" in decision.message
    assert "Open interest: $2.00M" in decision.message
    assert decision.payload["derivatives_at_alert"]["source"] == "fresh_multi_venue_snapshot"
