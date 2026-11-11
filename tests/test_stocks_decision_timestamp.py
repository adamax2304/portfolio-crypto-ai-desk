"""Stocks intraday must use one timestamp for decision, session gate and registration."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from src.config import load_config
from src.models import TradeIdea
from src.signals.config import SignalTrackingConfig
from src.signals.registry import register_ideas
from src.storage.sqlite import SQLiteStore
from src.stocks.pipelines import stocks_pipeline as pipe


UTC = timezone.utc


def test_pipeline_passes_fixed_decision_time_to_trade_idea_agent(monkeypatch, tmp_path):
    captured: dict[str, object] = {}

    def agent(payload):
        class _Agent:
            def __init__(self, *args, **kwargs):
                pass

            def run(self, *args, **kwargs):
                captured["now"] = kwargs.get("now")
                return payload
        return _Agent

    monkeypatch.setattr(pipe, "StocksMarketRegimeAgent", agent({"regime": {"label": "bullish"}}))
    monkeypatch.setattr(pipe, "SectorRotationAgent", agent({}))
    monkeypatch.setattr(pipe, "StockRelativeStrengthAgent", agent({"rows": []}))
    monkeypatch.setattr(pipe, "EarningsRiskAgent", agent({"risks": []}))
    monkeypatch.setattr(pipe, "CompanyNewsAgent", agent({"hits_by_symbol": {}}))
    monkeypatch.setattr(pipe, "StockTechnicalAgent", agent({"setups": []}))
    monkeypatch.setattr(pipe, "StockRiskAgent", agent({"by_symbol": {}}))
    monkeypatch.setattr(pipe, "StockScoringAgent", agent({"scores": []}))
    monkeypatch.setattr(pipe, "StockTradeIdeaAgent", agent({"ideas": []}))

    class _Calendar:
        def __init__(self, *args, **kwargs):
            pass

        def collect(self, **kwargs):
            return SimpleNamespace(events=[], failed_symbols=[])

    monkeypatch.setattr(pipe, "EarningsCalendarCollector", _Calendar)
    moment = datetime(2026, 7, 24, 14, 15, tzinfo=UTC)
    pipeline = pipe.StocksPipeline(load_config())
    pipeline.db = SQLiteStore(tmp_path / "stocks.sqlite")
    pipeline.db.init_db()
    result = pipeline.run_report(
        mode="intraday", skip_data_update=True, shadow_only=True, now=moment
    )
    assert captured["now"] == moment
    assert result.decision_at == moment.isoformat()


def test_registry_uses_supplied_decision_time_for_expiry(tmp_path):
    store = SQLiteStore(tmp_path / "signals.sqlite")
    store.init_db()
    moment = datetime(2026, 7, 24, 14, 15, tzinfo=UTC)
    idea = TradeIdea(
        symbol="AMD", direction="long", score=80.0, confidence="high", risk_level="low",
        timeframe="15m", tier="A", mode="intraday", asset_class="stocks", thesis="test",
        evidence=[], counterarguments=[], entry_plan="zone", invalidation="98", targets=[],
        what_to_monitor=[], avoid_conditions=[], data_sources_used=[],
        raw={"setup": {"entry_low": 100.0, "entry_high": 101.0, "invalidation": 98.0}},
    )
    tracking = SignalTrackingConfig(
        enabled=True,
        track_tiers=("A",),
        default_validity_hours={"intraday": 6},
    )
    result = register_ideas(
        store, [idea], config=tracking, report_id="decision-time", asset_class="stocks",
        created_at=moment.isoformat(),
    )
    row = store.load_signal(result.signal_ids[0])
    assert row["created_at"] == moment.isoformat()
    assert row["expires_at"] == (moment + timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%S+00:00")
