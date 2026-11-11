from __future__ import annotations

from src.models import TradeIdea
from src.storage.sqlite import SQLiteStore


def test_sqlite_store_saves_trade_idea(tmp_path) -> None:
    store = SQLiteStore(tmp_path / "desk.sqlite")
    store.init_db()
    idea = TradeIdea(
        symbol="BTC/USDT",
        direction="watchlist only",
        score=60,
        confidence="medium",
        risk_level="medium",
        timeframe="1h thesis / 15m execution",
        thesis="test",
        evidence=["evidence"],
        counterarguments=["counter"],
        entry_plan="watch",
        invalidation="n/a",
        targets=["n/a"],
        what_to_monitor=["btc"],
        avoid_conditions=["bad rr"],
        data_sources_used=["test"],
        raw={"setup": {}},
    )
    ids = store.save_trade_ideas("test-report", [idea])
    assert len(ids) == 1
    assert store.counts()["trade_ideas"] == 1
