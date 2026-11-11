"""Integration-bug fix #4 — the SI-6 advisory LLM-review routing helper must be WIRED into the
paper-entry path: a fresh reject/wait review routes a stocks-intraday A/B paper candidate to
review-only/shadow; missing review does NOT block by default; crypto + stocks non-intraday are
unaffected. Advisory only — no tier/score/TP/SL mutation, no live.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock

from src.notifiers import paper_entry as pe
from src.stocks import intraday_llm_review as lr


def _db(tmp_path: Path):
    p = tmp_path / "t.sqlite"
    c = sqlite3.connect(p)
    c.execute("CREATE TABLE signal_alerts (alert_id TEXT PRIMARY KEY, signal_id TEXT, asset_class TEXT, "
              "mode TEXT, symbol TEXT, tier TEXT, score REAL, direction TEXT, sent_at TEXT, "
              "alert_type TEXT, telegram_status TEXT, message_hash TEXT, payload_json TEXT)")
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, asset_class TEXT, mode TEXT)")
    c.executescript(lr._DDL)
    c.commit(); c.close()
    return p


class _Store:
    def __init__(self, path):
        self.db_path = path

    def connect(self):
        c = sqlite3.connect(self.db_path)
        c.row_factory = sqlite3.Row
        return c

    def last_alert_by_type(self, *a, **k):
        return None

    def record_signal_alert(self, **kw):
        with self.connect() as c:
            c.execute("INSERT INTO signal_alerts(alert_id, signal_id, asset_class, mode, symbol, tier, "
                      "score, direction, sent_at, alert_type, telegram_status, message_hash, payload_json) "
                      "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                      (kw["alert_id"], kw["signal_id"], kw["asset_class"], kw.get("mode"), kw["symbol"],
                       kw["tier"], kw.get("score"), kw.get("direction"), kw["sent_at"], kw["alert_type"],
                       kw.get("telegram_status"), kw.get("message_hash"), json.dumps(kw.get("payload") or {})))


def _seed_review(path, signal_id, decision, when=None):
    when = when or datetime.now(timezone.utc).isoformat()
    c = sqlite3.connect(path)
    c.execute("INSERT OR REPLACE INTO stocks_intraday_llm_reviews VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
              (signal_id, when, "midday", decision, 0.8, None, None, None, None, None, None, None, None))
    c.commit(); c.close()


def _stock_intraday_a(sid="sig_stk_1"):
    return {"signal_id": sid, "asset_class": "stocks", "symbol": "AAPL", "direction": "long",
            "mode": "intraday", "tier": "A", "score": 82.0, "data_confidence": "high",
            "entry_low": 254.0, "entry_high": 254.5, "entry_trigger": 254.5, "suggested_entry": 254.5,
            "stop_loss": 251.0, "invalidation": 251.0, "tp1": 257.0, "tp2": 259.5, "tp3": 263.0,
            "thesis": "AAPL RTH momentum.", "news_supported": 0, "setup_type": "breakout",
            "market_regime": "risk_on", "funding_context": "", "raw_idea_json": json.dumps({})}


def _send(store, signal):
    return pe.send_paper_entry_alert(
        store=store, notifier=MagicMock(), signal=signal, prev_status="waiting_for_entry",
        outcome_entry_triggered=True,
        outcome_entry_triggered_at=datetime.now(timezone.utc).isoformat(),  # fresh → not late
        outcome_entry_price_used=254.5)


def test_fresh_reject_routes_stock_intraday_ab_to_shadow(tmp_path):
    path = _db(tmp_path)
    _seed_review(path, "sig_stk_1", "reject")
    out = _send(_Store(path), _stock_intraday_a())
    assert out["telegram_status"] == "shadow_llm_review"
    assert out["payload"]["llm_review_routed_to_shadow"] is True
    assert out["payload"]["llm_review_reason"] == "llm_review_reject"


def test_fresh_wait_routes_stock_intraday_ab_to_shadow(tmp_path):
    path = _db(tmp_path)
    _seed_review(path, "sig_stk_1", "wait")
    out = _send(_Store(path), _stock_intraday_a())
    assert out["telegram_status"] == "shadow_llm_review"


def test_missing_review_does_not_block_by_default(tmp_path):
    path = _db(tmp_path)                       # no review row seeded
    out = _send(_Store(path), _stock_intraday_a())
    assert out["telegram_status"] != "shadow_llm_review"
    assert out["payload"].get("llm_review_routed_to_shadow") in (False, None)


def test_require_fresh_blocks_missing_review(tmp_path, monkeypatch):
    path = _db(tmp_path)
    import types
    fake = types.SimpleNamespace(risk={"intraday_guards": {"llm_review": {
        "require_fresh_llm_review_for_stocks_intraday_ab": True, "freshness_minutes": 90}}})
    monkeypatch.setattr("src.stocks.load_stocks_config", lambda: fake)
    out = _send(_Store(path), _stock_intraday_a())
    assert out["telegram_status"] == "shadow_llm_review"
    assert out["payload"]["llm_review_reason"] == "no_fresh_llm_review"


def test_crypto_unaffected_by_llm_routing(tmp_path):
    path = _db(tmp_path)
    _seed_review(path, "sig_crypto_1", "reject")   # even a matching review id must not route crypto
    crypto = {"signal_id": "sig_crypto_1", "asset_class": "crypto", "symbol": "ZEC/USDT",
              "direction": "long", "mode": "intraday", "tier": "B", "score": 74.0,
              "primary_exchange": "binance", "data_confidence": "medium", "entry_low": 42.0,
              "entry_high": 42.3, "entry_trigger": 42.15, "suggested_entry": 42.15, "stop_loss": 40.8,
              "invalidation": 40.8, "tp1": 43.2, "tp2": 44.5, "tp3": 46.0, "thesis": "x",
              "news_supported": 1, "setup_type": "breakout", "market_regime": "risk_on",
              "funding_context": "funding=0.00005, crowding=normal", "raw_idea_json": json.dumps({})}
    out = _send(_Store(path), crypto)
    assert out["telegram_status"] != "shadow_llm_review"
