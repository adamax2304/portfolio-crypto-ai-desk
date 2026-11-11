"""SI-6 scheduled LLM review — advisory routing + ingest. LLM never creates/changes trades."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

from src.stocks import intraday_llm_review as lr


def _seed(db):
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, asset_class TEXT, mode TEXT)")
    c.execute("INSERT INTO proposed_signals VALUES ('s1','stocks','intraday')")
    c.execute("INSERT INTO proposed_signals VALUES ('s2','stocks','intraday')")
    c.commit(); c.close()


def test_ingest_validates_signal_id(tmp_path):
    db = str(tmp_path / "r.sqlite")
    _seed(db)
    res = lr.ingest_reviews(reviews=[
        {"signal_id": "s1", "decision": "reject", "confidence": 0.8, "reasons": ["market conflict"]},
        {"signal_id": "ghost", "decision": "approve"},          # unknown → skipped
        {"signal_id": "s2", "decision": "not_a_decision"},      # bad decision → skipped
    ], db=db, review_cycle="midday")
    assert res["ingested"] == 1


def test_routing_reject_routes_to_review(tmp_path):
    db = str(tmp_path / "r2.sqlite")
    _seed(db)
    now = datetime(2026, 7, 8, 16, 0, tzinfo=timezone.utc)
    lr.ingest_reviews(reviews=[{"signal_id": "s1", "decision": "reject"}], db=db,
                      now_iso=now.isoformat())
    route, reason = lr.should_route_to_review(db=db, signal_id="s1",
                                              cfg={"llm_review": {"freshness_minutes": 90}}, now=now)
    assert route is True and reason == "llm_review_reject"


def test_routing_default_does_not_block_without_review(tmp_path):
    db = str(tmp_path / "r3.sqlite")
    _seed(db)
    # no review + require flag default false → do NOT block
    route, _ = lr.should_route_to_review(db=db, signal_id="s2", cfg={"llm_review": {}},
                                         now=datetime(2026, 7, 8, 16, 0, tzinfo=timezone.utc))
    assert route is False


def test_routing_require_fresh_blocks_when_missing(tmp_path):
    db = str(tmp_path / "r4.sqlite")
    _seed(db)
    cfg = {"llm_review": {"require_fresh_llm_review_for_stocks_intraday_ab": True, "freshness_minutes": 90}}
    route, reason = lr.should_route_to_review(db=db, signal_id="s2", cfg=cfg,
                                              now=datetime(2026, 7, 8, 16, 0, tzinfo=timezone.utc))
    assert route is True and reason == "no_fresh_llm_review"


def test_module_is_advisory_only():
    import pathlib
    src = pathlib.Path(lr.__file__).read_text(encoding="utf-8").lower()
    for bad in ("create_order(", "auto_live", "final_r =", "update proposed_signals",
                "update signal_outcomes", "insert into proposed_signals"):
        assert bad not in src, bad
