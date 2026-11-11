from __future__ import annotations

import json
import sqlite3
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from src.config import load_config
from src.execution.paper_portfolio import resolve_cost_context, simulate_portfolio
from src.execution.stocks_preus_review import (
    active_actionable_signal_ids,
    source_decision_fingerprint,
)
from src.stocks import mexc_stock_futures_paper as paper
from src.stocks.monitor import MonitorTickResult, StocksMonitorSession


UTC = timezone.utc
PREOPEN = datetime(2026, 7, 27, 13, 10, tzinfo=UTC)  # 09:10 New York


class FakeMexc:
    def __init__(self) -> None:
        self.bid = 99.99
        self.ask = 100.01
        self.fair = 100.0
        self.index = 100.0
        self.hold = 50_000.0
        self.candles = [
            {
                "candle_at": int((PREOPEN - timedelta(minutes=2)).timestamp()),
                "open": 100.0,
                "high": 100.10,
                "low": 99.90,
                "close": 100.0,
            }
        ]

    def contracts(self):
        return [{
            "symbol": "AAPLSTOCK_USDT",
            "baseCoin": "AAPLSTOCK",
            "baseCoinName": "AAPL",
            "conceptPlate": ["Stock", "tradfi"],
            "state": 0,
            "apiAllowed": True,
            "priceUnit": 0.01,
            "volUnit": 1,
            "minVol": 1,
            "contractSize": 0.01,
            "maxLeverage": 100,
            "makerFeeRate": 0.0,
            "takerFeeRate": 0.0002,
        }]

    def ticker(self, _symbol):
        return {
            "fairPrice": self.fair,
            "indexPrice": self.index,
            "lastPrice": self.fair,
            "fundingRate": 0.0001,
            "holdVol": self.hold,
        }

    def depth(self, _symbol, *, limit=5):
        del limit
        return {
            "bids": [[self.bid - i * 0.01, 1000] for i in range(5)],
            "asks": [[self.ask + i * 0.01, 1000] for i in range(5)],
        }

    def klines(self, _symbol, **_kwargs):
        return list(self.candles)


def _db(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE proposed_signals (
            signal_id TEXT PRIMARY KEY,
            asset_class TEXT,
            mode TEXT,
            symbol TEXT,
            direction TEXT,
            created_at TEXT,
            updated_at TEXT,
            raw_idea_json TEXT,
            tier TEXT,
            score REAL,
            status TEXT,
            setup_type TEXT,
            suggested_entry REAL,
            entry_trigger REAL,
            entry_low REAL,
            stop_loss REAL,
            invalidation REAL,
            tp1 REAL,
            tp2 REAL,
            tp3 REAL
        );
        CREATE TABLE stocks_preus_actionability (
            signal_id TEXT PRIMARY KEY,
            target_session_open_at TEXT,
            target_session_close_at TEXT,
            evaluated_at TEXT,
            decision TEXT,
            effective_score REAL,
            effective_tier TEXT,
            reason_codes_json TEXT,
            review_expires_at TEXT,
            valid_until TEXT,
            current_signal_updated_at TEXT,
            source_fingerprint TEXT,
            geometry_json TEXT,
            reactivated INTEGER,
            version TEXT
        );
        CREATE TABLE news_canonical_events (
            event_id TEXT PRIMARY KEY,
            title TEXT,
            source TEXT,
            url TEXT,
            published_at TEXT,
            asset_class TEXT,
            trusted_symbols_json TEXT,
            event_type TEXT,
            direction_hint TEXT,
            source_quality TEXT,
            content_level TEXT,
            confidence REAL,
            linkage_allowed INTEGER,
            risk_action TEXT,
            expires_at TEXT,
            is_cluster_primary INTEGER
        );
        CREATE TABLE signal_outcomes (id INTEGER PRIMARY KEY, final_r REAL);
        CREATE TABLE live_orders (id INTEGER PRIMARY KEY, status TEXT);
        """
    )
    return conn


def _seed(
    conn: sqlite3.Connection,
    *,
    now: datetime = PREOPEN,
    event_type: str = "partnership",
    direction: str = "long",
    cap_reasons: list[str] | None = None,
) -> None:
    hint = "bullish" if direction == "long" else "bearish"
    event_at = now - timedelta(minutes=30)
    conn.execute(
        """
        INSERT INTO news_canonical_events(
            event_id,title,source,url,published_at,asset_class,
            trusted_symbols_json,event_type,direction_hint,source_quality,
            content_level,confidence,linkage_allowed,risk_action,expires_at,
            is_cluster_primary
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            "evt_1", "Apple signs a material partnership", "Reuters", "https://example.test/1",
            event_at.isoformat(), "stocks", '["AAPL"]', event_type, hint, "reputable",
            "full_body", 0.90, 1, "allow", (now + timedelta(hours=6)).isoformat(), 1,
        ),
    )
    raw = {
        "pre_gate_tier": "A",
        "cap_reasons": cap_reasons or [paper.PLAN_MARKER],
        "news_influence_contract": {
            "supported": True,
            "source": "canonical_event",
            "event_type": event_type,
            "direction_hint": hint,
            "content_level": "full_body",
            "confidence": 0.90,
        },
    }
    conn.execute(
        """
        INSERT INTO proposed_signals(
            signal_id,asset_class,mode,symbol,direction,created_at,
            updated_at,
            raw_idea_json,tier,score,status,setup_type,suggested_entry,entry_trigger,
            entry_low,stop_loss,invalidation,tp1,tp2,tp3
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            "sig_1", "stocks", "intraday", "AAPL", direction,
            (now - timedelta(minutes=5)).isoformat(),
            (now - timedelta(minutes=5)).isoformat(), json.dumps(raw),
            "C", 82.0, "generated", "continuation", 100.0, 100.0, 99.9,
            98.0 if direction == "long" else 102.0,
            98.0 if direction == "long" else 102.0,
            103.0 if direction == "long" else 97.0,
            105.0 if direction == "long" else 95.0,
            108.0 if direction == "long" else 92.0,
        ),
    )
    conn.commit()


def _seed_preus_actionable(
    conn: sqlite3.Connection,
    *,
    now: datetime = PREOPEN,
    effective_score: float = 82.0,
    effective_tier: str = "A",
) -> None:
    """Seed an independently materialized pre-US decision without an event."""
    raw = {
        "pre_gate_tier": "A",
        "cap_reasons": [paper.PLAN_MARKER],
        # This is deliberately unsupported by canonical linkage. The test
        # proves MEXC Paper consumes the reviewed permission, not an invented
        # canonical news event.
        "news_influence_contract": {"supported": False},
    }
    conn.execute(
        """
        INSERT INTO proposed_signals(
            signal_id,asset_class,mode,symbol,direction,created_at,
            updated_at,
            raw_idea_json,tier,score,status,setup_type,suggested_entry,entry_trigger,
            entry_low,stop_loss,invalidation,tp1,tp2,tp3
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            "sig_preus", "stocks", "intraday", "AAPL", "long",
            (now - timedelta(minutes=15)).isoformat(), now.isoformat(), json.dumps(raw),
            "C", 55.0, "generated", "continuation", 100.0, 100.0, 99.9,
            98.0, 98.0, 103.0, 105.0, 108.0,
        ),
    )
    geometry = {
        "suggested_entry": 100.0,
        "entry_trigger": 100.0,
        "entry_low": 99.9,
        "stop_loss": 98.0,
        "invalidation": 98.0,
        "tp1": 103.0,
        "tp2": 105.0,
        "tp3": 108.0,
    }
    conn.execute(
        """
        INSERT INTO stocks_preus_actionability(
            signal_id,target_session_open_at,target_session_close_at,evaluated_at,
            decision,effective_score,effective_tier,reason_codes_json,review_expires_at,
            valid_until,current_signal_updated_at,source_fingerprint,geometry_json,reactivated,version
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            "sig_preus", now.isoformat(), (now + timedelta(hours=7)).isoformat(),
            now.isoformat(), "ACTIONABLE", effective_score, effective_tier, "[]",
            (now + timedelta(minutes=90)).isoformat(),
            (now + timedelta(minutes=90)).isoformat(), now.isoformat(),
            source_decision_fingerprint({
                "symbol": "AAPL",
                "direction": "long", "setup_type": "continuation", "tier": "C", "score": 55.0,
                "entry_low": 99.9, "entry_trigger": 100.0, "suggested_entry": 100.0,
                "stop_loss": 98.0, "invalidation": 98.0, "tp1": 103.0,
                "tp2": 105.0, "tp3": 108.0,
            }), json.dumps(geometry), 1, "preus_test_v1",
        ),
    )
    conn.commit()


def _cfg(**updates):
    cfg = paper.load_cfg()
    cfg.update(updates)
    return cfg


def test_candidate_decision_starts_twenty_minutes_before_open():
    cfg = _cfg()
    assert paper.in_refresh_window(PREOPEN - timedelta(minutes=5), cfg)
    assert not paper.in_candidate_window(PREOPEN - timedelta(minutes=1), cfg)
    assert paper.in_candidate_window(PREOPEN, cfg)


def test_dynamic_contract_discovery_and_idempotent_stage(tmp_path):
    db = tmp_path / "desk.sqlite"
    with _db(db) as conn:
        _seed(conn)
        paper.ensure_tables(conn)
        first = paper.stage_candidates(conn, client=FakeMexc(), now=PREOPEN, cfg=_cfg())
        second = paper.stage_candidates(conn, client=FakeMexc(), now=PREOPEN, cfg=_cfg())
        row = conn.execute(
            "SELECT ticker,mexc_symbol,status FROM mexc_stock_futures_paper_orders"
        ).fetchone()
        assert first == {
            "status": "ok", "evaluated": 1, "staged": 1, "rejected": 0,
            "preus_actionable": 0, "preus_processed": 0,
        }
        assert second["staged"] == 0
        assert tuple(row) == ("AAPL", "AAPLSTOCK/USDT", "STAGED")
        assert conn.execute(
            "SELECT COUNT(*) FROM mexc_stock_futures_paper_orders"
        ).fetchone()[0] == 1


def test_duplicate_session_symbol_orders_are_reconciled_without_deleting_history(tmp_path):
    db = tmp_path / "desk.sqlite"
    with _db(db) as conn:
        _seed(conn)
        paper.ensure_tables(conn)
        paper.stage_candidates(conn, client=FakeMexc(), now=PREOPEN, cfg=_cfg())
        original = dict(conn.execute(
            "SELECT * FROM mexc_stock_futures_paper_orders"
        ).fetchone())
        duplicate = dict(original)
        duplicate.update({
            "order_id": "msp_duplicate_race",
            "source_signal_id": "sig_duplicate_race",
            "event_id": "event_duplicate_race",
            "created_at": (PREOPEN + timedelta(seconds=1)).isoformat(),
            "updated_at": (PREOPEN + timedelta(seconds=1)).isoformat(),
        })
        paper._store_order(conn, duplicate)

        repaired = paper.reconcile_session_symbol_duplicates(
            conn, now=PREOPEN + timedelta(seconds=2)
        )
        states = dict(conn.execute(
            "SELECT status,COUNT(*) FROM mexc_stock_futures_paper_orders GROUP BY status"
        ).fetchall())
        duplicate_row = conn.execute(
            "SELECT status,reject_reason FROM mexc_stock_futures_paper_orders "
            "WHERE order_id='msp_duplicate_race'"
        ).fetchone()

        assert repaired == {"invalidated": 1, "unresolved_filled": 0}
        assert states == {"INVALIDATED": 1, "STAGED": 1}
        assert tuple(duplicate_row) == (
            "INVALIDATED", "DUPLICATE_SYMBOL_SESSION_RECONCILED"
        )


def test_filled_order_cannot_be_demoted_and_existing_position_repairs_legacy_state(tmp_path):
    db = tmp_path / "desk.sqlite"
    with _db(db) as conn:
        _seed(conn)
        paper.ensure_tables(conn)
        paper.stage_candidates(conn, client=FakeMexc(), now=PREOPEN, cfg=_cfg())
        order = dict(conn.execute(
            "SELECT * FROM mexc_stock_futures_paper_orders"
        ).fetchone())
        order.update({
            "status": "FILLED",
            "filled_at": PREOPEN.isoformat(),
            "fill_price": 100.0,
            "updated_at": PREOPEN.isoformat(),
        })
        paper._store_order(conn, order)

        rejected = dict(order)
        rejected.update({
            "status": "REJECTED",
            "reject_reason": "PREUS_SOURCE_CHANGED_AFTER_REVIEW",
            "updated_at": (PREOPEN + timedelta(minutes=1)).isoformat(),
        })
        paper._store_order(conn, rejected)
        assert tuple(conn.execute(
            "SELECT status,reject_reason FROM mexc_stock_futures_paper_orders"
        ).fetchone()) == ("FILLED", None)

        position = paper._position_from_fill(
            conn, order=order, fill_at=PREOPEN, fill_price=100.0, cfg=_cfg()
        )
        assert position is not None
        conn.execute(
            "UPDATE mexc_stock_futures_paper_orders "
            "SET status='REJECTED',reject_reason='LEGACY_BAD_STATE'"
        )
        repaired = paper.reconcile_order_position_lifecycle(
            conn, now=PREOPEN + timedelta(minutes=2)
        )
        assert repaired == {"orders_restored_to_filled": 1}
        assert tuple(conn.execute(
            "SELECT status,reject_reason FROM mexc_stock_futures_paper_orders"
        ).fetchone()) == ("FILLED", None)


def test_preus_actionable_plan_stages_without_direct_canonical_event(tmp_path):
    db = tmp_path / "desk.sqlite"
    with _db(db) as conn:
        _seed_preus_actionable(conn)
        paper.ensure_tables(conn)
        source_before = tuple(conn.execute(
            "SELECT tier,score,raw_idea_json FROM proposed_signals WHERE signal_id='sig_preus'"
        ).fetchone())
        result = paper.stage_candidates(conn, client=FakeMexc(), now=PREOPEN, cfg=_cfg())
        row = conn.execute(
            "SELECT source_signal_id,event_source,status,reject_reason "
            "FROM mexc_stock_futures_paper_orders"
        ).fetchone()
        source_after = tuple(conn.execute(
            "SELECT tier,score,raw_idea_json FROM proposed_signals WHERE signal_id='sig_preus'"
        ).fetchone())

        assert result["preus_actionable"] == 1
        assert result["preus_processed"] == 1
        assert result["staged"] == 1
        assert tuple(row) == ("sig_preus", "stocks_preus_actionability", "STAGED", None)
        assert source_after == source_before
        snapshot = json.loads(conn.execute(
            "SELECT snapshot_json FROM mexc_stock_futures_paper_orders"
        ).fetchone()[0])
        assert snapshot["preus_actionability"]["effective_tier"] == "A"
        assert snapshot["source_signal"]["signal_id"] == "sig_preus"
        assert snapshot["source_signal"]["source_fingerprint_reviewed"]
        assert snapshot["source_signal"]["source_fingerprint_current"]
        assert snapshot["source_signal"]["raw_context"]["news_influence_contract"] == {
            "supported": False
        }
        assert conn.execute("SELECT COUNT(*) FROM signal_outcomes").fetchone()[0] == 0
        assert conn.execute("SELECT COUNT(*) FROM live_orders").fetchone()[0] == 0


def test_preus_too_tight_source_stop_is_normalized_not_rejected(tmp_path):
    db = tmp_path / "desk.sqlite"
    with _db(db) as conn:
        _seed_preus_actionable(conn)
        geometry = {
            "suggested_entry": 100.0,
            "entry_trigger": 100.0,
            "entry_low": 99.9,
            "stop_loss": 99.8,
            "invalidation": 99.8,
            "tp1": 101.0,
            "tp2": 102.0,
            "tp3": 103.0,
        }
        conn.execute(
            "UPDATE proposed_signals SET stop_loss=?,invalidation=?,tp1=?,tp2=?,tp3=? "
            "WHERE signal_id='sig_preus'",
            (
                geometry["stop_loss"],
                geometry["invalidation"],
                geometry["tp1"],
                geometry["tp2"],
                geometry["tp3"],
            ),
        )
        conn.execute(
            "UPDATE stocks_preus_actionability SET geometry_json=?,source_fingerprint=? "
            "WHERE signal_id='sig_preus'",
            (
                json.dumps(geometry),
                source_decision_fingerprint({
                    "symbol": "AAPL",
                    "direction": "long",
                    "setup_type": "continuation",
                    "tier": "C",
                    "score": 55.0,
                    **geometry,
                }),
            ),
        )
        paper.ensure_tables(conn)
        result = paper.stage_candidates(conn, client=FakeMexc(), now=PREOPEN, cfg=_cfg())
        row = conn.execute(
            "SELECT status,reject_reason,trigger_price,stop_price,source_stop,snapshot_json "
            "FROM mexc_stock_futures_paper_orders"
        ).fetchone()
        snapshot = json.loads(row["snapshot_json"])

        assert result["staged"] == 1
        assert tuple(row[:2]) == ("STAGED", None)
        assert row["source_stop"] == 99.8
        assert row["stop_price"] < row["trigger_price"] * 0.996
        assert snapshot["stop_normalization"] == (
            "source_stop_too_tight_normalized_to_min_distance"
        )


def test_preus_actionable_plan_survives_tracker_stale_status(tmp_path):
    db = tmp_path / "desk.sqlite"
    with _db(db) as conn:
        _seed_preus_actionable(conn)
        conn.executescript(
            "CREATE TABLE stocks_paper_decision_snapshots ("
            "signal_id TEXT PRIMARY KEY,funnel_state TEXT)"
        )
        conn.execute(
            "INSERT INTO stocks_paper_decision_snapshots(signal_id,funnel_state) "
            "VALUES('sig_preus','PREOPEN_PLAN')"
        )
        conn.execute(
            "UPDATE proposed_signals SET status='stale_before_entry' "
            "WHERE signal_id='sig_preus'"
        )
        conn.commit()

    assert active_actionable_signal_ids(db, now=PREOPEN) == ["sig_preus"]


def test_preus_ineligible_plan_has_durable_rejection_reason(tmp_path):
    db = tmp_path / "desk.sqlite"
    with _db(db) as conn:
        _seed_preus_actionable(conn, effective_score=64.99)
        paper.ensure_tables(conn)
        result = paper.stage_candidates(conn, client=FakeMexc(), now=PREOPEN, cfg=_cfg())
        row = conn.execute(
            "SELECT status,reject_reason,event_source FROM mexc_stock_futures_paper_orders"
        ).fetchone()

        assert result["preus_actionable"] == 1
        assert result["preus_processed"] == 1
        assert result["staged"] == 0
        assert result["rejected"] == 1
        assert tuple(row) == (
            "REJECTED", "PREUS_EFFECTIVE_SCORE_BELOW_MIN", "stocks_preus_actionability"
        )


def test_preus_actionable_plan_is_rejected_if_source_changed_after_review(tmp_path):
    db = tmp_path / "desk.sqlite"
    with _db(db) as conn:
        _seed_preus_actionable(conn)
        conn.execute(
            "UPDATE proposed_signals SET updated_at=?,entry_trigger=? WHERE signal_id='sig_preus'",
            ((PREOPEN + timedelta(minutes=1)).isoformat(), 100.5),
        )
        paper.ensure_tables(conn)
        result = paper.stage_candidates(conn, client=FakeMexc(), now=PREOPEN, cfg=_cfg())
        row = conn.execute(
            "SELECT status,reject_reason FROM mexc_stock_futures_paper_orders"
        ).fetchone()
        assert result["staged"] == 0
        assert result["rejected"] == 1
        assert tuple(row) == ("REJECTED", "PREUS_SOURCE_CHANGED_AFTER_REVIEW")


def test_preus_actionable_plan_survives_housekeeping_timestamp_update(tmp_path):
    db = tmp_path / "desk.sqlite"
    with _db(db) as conn:
        _seed_preus_actionable(conn)
        conn.execute(
            "UPDATE proposed_signals SET updated_at=? WHERE signal_id='sig_preus'",
            ((PREOPEN + timedelta(minutes=1)).isoformat(),),
        )
        paper.ensure_tables(conn)
        result = paper.stage_candidates(conn, client=FakeMexc(), now=PREOPEN, cfg=_cfg())
        row = conn.execute(
            "SELECT status,reject_reason FROM mexc_stock_futures_paper_orders"
        ).fetchone()
        assert result["staged"] == 1
        assert tuple(row) == ("STAGED", None)


def test_preus_actionable_plan_survives_score_and_tier_recompute(tmp_path):
    db = tmp_path / "desk.sqlite"
    with _db(db) as conn:
        _seed_preus_actionable(conn)
        conn.execute(
            "UPDATE proposed_signals SET updated_at=?,tier=?,score=? WHERE signal_id='sig_preus'",
            ((PREOPEN + timedelta(minutes=1)).isoformat(), "B", 66.1),
        )
        paper.ensure_tables(conn)
        result = paper.stage_candidates(conn, client=FakeMexc(), now=PREOPEN, cfg=_cfg())
        row = conn.execute(
            "SELECT status,reject_reason FROM mexc_stock_futures_paper_orders"
        ).fetchone()
        snapshot = json.loads(conn.execute(
            "SELECT snapshot_json FROM mexc_stock_futures_paper_orders"
        ).fetchone()[0])
        assert result["staged"] == 1
        assert tuple(row) == ("STAGED", None)
        assert snapshot["source_signal"]["tier"] == "A"
        assert snapshot["source_signal"]["score"] == 82.0


def test_preopen_health_alerts_if_actionable_plan_was_not_processed(tmp_path):
    db = tmp_path / "desk.sqlite"
    due = PREOPEN + timedelta(minutes=10)  # 09:20 ET
    with _db(db) as conn:
        _seed_preus_actionable(conn, now=PREOPEN)
        paper.ensure_tables(conn)
        health = paper.preopen_health(conn, now=due, cfg=_cfg())
        first = paper.consume_new_preopen_health_alerts(conn, health=health, now=due)
        repeated = paper.consume_new_preopen_health_alerts(
            conn,
            health=paper.preopen_health(conn, now=due + timedelta(minutes=1), cfg=_cfg()),
            now=due + timedelta(minutes=1),
        )
        persisted = conn.execute(
            "SELECT actionable_count,processed_count,status,reason,alerted_at "
            "FROM mexc_stock_futures_preopen_health"
        ).fetchone()

        assert health["status"] == "ACTIONABLE_UNPROCESSED"
        assert health["reason"] == "preus_actionable_candidates_unprocessed"
        assert len(first) == 1
        assert repeated == []
        assert tuple(persisted[:4]) == (
            1, 0, "ACTIONABLE_UNPROCESSED", "preus_actionable_candidates_unprocessed"
        )
        assert persisted[4] is not None
        assert conn.execute(
            "SELECT COUNT(*) FROM mexc_stock_futures_preopen_health_history"
        ).fetchone()[0] == 2


def test_quote_health_is_persisted_and_alerted_once(tmp_path):
    db = tmp_path / "desk.sqlite"
    client = FakeMexc()
    with _db(db) as conn:
        paper.ensure_tables(conn)
        paper.refresh_contract_catalog(conn, client=client, now=PREOPEN)
        cfg = _cfg(health_probe_tickers=["AAPL"])
        health = paper.probe_quote_health(conn, client=client, now=PREOPEN, cfg=cfg)
        assert health["healthy"] == 1
        row = conn.execute(
            "SELECT status,bid,ask,top5_depth_usdt FROM mexc_stock_futures_quote_health "
            "WHERE ticker='AAPL'"
        ).fetchone()
        assert row[0] == "HEALTHY" and row[1] is not None and row[2] is not None and row[3] > 0
        # A recovery clears future outage alerts, but a healthy probe itself is
        # not an operator warning.
        assert paper.consume_new_quote_health_alerts(conn, now=PREOPEN) == []
        client.bid = 0.0
        client.ask = 0.0
        unhealthy = paper.probe_quote_health(
            conn, client=client, now=PREOPEN + timedelta(minutes=6), cfg=cfg
        )
        assert unhealthy["unhealthy"] >= 1
        first = paper.consume_new_quote_health_alerts(conn, now=PREOPEN + timedelta(minutes=6))
        assert any(row["ticker"] == "AAPL" for row in first)
        assert paper.consume_new_quote_health_alerts(conn, now=PREOPEN + timedelta(minutes=6)) == []


def test_quote_health_retries_one_transient_mexc_api_error(tmp_path, monkeypatch):
    class FlakyMexc(FakeMexc):
        def __init__(self):
            super().__init__()
            self.ticker_calls = 0

        def ticker(self, symbol):
            self.ticker_calls += 1
            if self.ticker_calls == 1:
                from src.live_execution.mexc_client import MexcAPIError
                raise MexcAPIError("temporary public endpoint rejection")
            return super().ticker(symbol)

    db = tmp_path / "desk.sqlite"
    client = FlakyMexc()
    monkeypatch.setattr(paper.time, "sleep", lambda _seconds: None)
    with _db(db) as conn:
        paper.ensure_tables(conn)
        paper.refresh_contract_catalog(conn, client=client, now=PREOPEN)
        health = paper.probe_quote_health(
            conn, client=client, now=PREOPEN, cfg=_cfg(health_probe_tickers=["AAPL"])
        )
        assert health["healthy"] == 1
        assert client.ticker_calls == 2
        assert conn.execute(
            "SELECT status FROM mexc_stock_futures_quote_health WHERE ticker='AAPL'"
        ).fetchone()[0] == "HEALTHY"


def test_quote_health_retries_two_transient_mexc_api_errors(tmp_path, monkeypatch):
    class VeryFlakyMexc(FakeMexc):
        def __init__(self):
            super().__init__()
            self.ticker_calls = 0

        def ticker(self, symbol):
            self.ticker_calls += 1
            if self.ticker_calls <= 2:
                from src.live_execution.mexc_client import MexcAPIError
                raise MexcAPIError("temporary public endpoint rejection")
            return super().ticker(symbol)

    db = tmp_path / "desk.sqlite"
    client = VeryFlakyMexc()
    monkeypatch.setattr(paper.time, "sleep", lambda _seconds: None)
    with _db(db) as conn:
        paper.ensure_tables(conn)
        paper.refresh_contract_catalog(conn, client=client, now=PREOPEN)
        health = paper.probe_quote_health(
            conn, client=client, now=PREOPEN, cfg=_cfg(health_probe_tickers=["AAPL"])
        )
        assert health["healthy"] == 1
        assert client.ticker_calls == 3
        assert conn.execute(
            "SELECT status FROM mexc_stock_futures_quote_health WHERE ticker='AAPL'"
        ).fetchone()[0] == "HEALTHY"


@pytest.mark.parametrize(
    ("event_type", "extra_cap"),
    [
        ("earnings", None),
        ("partnership", "legal_risk_active"),
    ],
)
def test_event_and_source_guard_fail_closed(tmp_path, event_type, extra_cap):
    db = tmp_path / "desk.sqlite"
    caps = [paper.PLAN_MARKER] + ([extra_cap] if extra_cap else [])
    with _db(db) as conn:
        _seed(conn, event_type=event_type, cap_reasons=caps)
        paper.ensure_tables(conn)
        result = paper.stage_candidates(
            conn, client=FakeMexc(), now=PREOPEN, cfg=_cfg()
        )
        assert result["staged"] == 0
        assert conn.execute(
            "SELECT COUNT(*) FROM mexc_stock_futures_paper_orders"
        ).fetchone()[0] == 0


def test_mexc_parity_rejects_wide_spread(tmp_path):
    db = tmp_path / "desk.sqlite"
    client = FakeMexc()
    client.bid = 98.0
    client.ask = 102.0
    with _db(db) as conn:
        _seed(conn)
        paper.ensure_tables(conn)
        result = paper.stage_candidates(
            conn, client=client, now=PREOPEN,
            cfg=_cfg(execution_liquidity_gates_enabled=True),
        )
        row = conn.execute(
            "SELECT status,reject_reason FROM mexc_stock_futures_paper_orders"
        ).fetchone()
        assert result["rejected"] == 1
        assert tuple(row) == ("REJECTED", "MEXC_SPREAD_TOO_WIDE")


def test_small_account_mode_does_not_block_on_book_liquidity(tmp_path):
    db = tmp_path / "desk.sqlite"
    client = FakeMexc()
    client.bid = 98.0
    client.ask = 102.0
    client.hold = 1.0
    with _db(db) as conn:
        _seed(conn)
        paper.ensure_tables(conn)
        result = paper.stage_candidates(
            conn, client=client, now=PREOPEN,
            cfg=_cfg(execution_liquidity_gates_enabled=False),
        )
        row = conn.execute(
            "SELECT status,reject_reason FROM mexc_stock_futures_paper_orders"
        ).fetchone()
        assert result["staged"] == 1
        assert tuple(row) == ("STAGED", None)


def test_same_bar_entry_and_stop_is_counted_as_loss(tmp_path):
    db = tmp_path / "desk.sqlite"
    client = FakeMexc()
    with _db(db) as conn:
        _seed(conn)
        paper.ensure_tables(conn)
        staged = paper.stage_candidates(conn, client=client, now=PREOPEN, cfg=_cfg())
        assert staged["staged"] == 1
        client.candles = [{
            "candle_at": int((PREOPEN + timedelta(minutes=1)).timestamp()),
            "open": 100.0,
            "high": 101.0,
            "low": 97.0,
            "close": 98.0,
        }]
        active = paper.process_active(
            conn, client=client, now=PREOPEN + timedelta(minutes=2), cfg=_cfg()
        )
        position = conn.execute(
            "SELECT status,paper_execution_r,close_reason "
            "FROM mexc_stock_futures_paper_positions"
        ).fetchone()
        assert active["filled"] == 1
        assert active["closed"] == 1
        assert tuple(position) == ("CLOSED", -1.0, "same_bar_original_stop")


def test_preus_plan_cannot_fill_before_opening_confirmation(tmp_path):
    db = tmp_path / "desk.sqlite"
    client = FakeMexc()
    with _db(db) as conn:
        _seed_preus_actionable(conn)
        paper.ensure_tables(conn)
        staged = paper.stage_candidates(conn, client=client, now=PREOPEN, cfg=_cfg())
        assert staged["staged"] == 1
        client.candles = [{
            "candle_at": int((PREOPEN + timedelta(minutes=1)).timestamp()),
            "open": 100.0,
            "high": 101.0,
            "low": 99.9,
            "close": 100.8,
        }]

        active = paper.process_active(
            conn, client=client, now=PREOPEN + timedelta(minutes=2), cfg=_cfg()
        )

        assert active["filled"] == 0
        assert conn.execute(
            "SELECT status FROM mexc_stock_futures_paper_orders"
        ).fetchone()[0] == "STAGED"
        assert conn.execute(
            "SELECT COUNT(*) FROM mexc_stock_futures_paper_positions"
        ).fetchone()[0] == 0


def test_preus_plan_requires_directional_opening_drive(tmp_path):
    db = tmp_path / "desk.sqlite"
    client = FakeMexc()
    opening = datetime(2026, 7, 27, 13, 30, tzinfo=UTC)
    with _db(db) as conn:
        _seed_preus_actionable(conn)
        paper.ensure_tables(conn)
        paper.stage_candidates(conn, client=client, now=PREOPEN, cfg=_cfg())
        client.candles = [
            {
                "candle_at": int((opening + timedelta(minutes=index)).timestamp()),
                "open": 100.0,
                "high": 100.5,
                "low": 99.7,
                "close": 99.8,
            }
            for index in range(5)
        ]

        active = paper.process_active(
            conn, client=client, now=opening + timedelta(minutes=5), cfg=_cfg()
        )
        row = conn.execute(
            "SELECT status,reject_reason FROM mexc_stock_futures_paper_orders"
        ).fetchone()

        assert active["filled"] == 0
        assert active["invalidated"] == 1
        assert tuple(row) == ("INVALIDATED", "OPENING_DRIVE_NOT_CONFIRMED")


def test_preus_opening_drive_can_fill_at_half_risk_after_confirmation(tmp_path):
    db = tmp_path / "desk.sqlite"
    client = FakeMexc()
    opening = datetime(2026, 7, 27, 13, 30, tzinfo=UTC)
    with _db(db) as conn:
        _seed_preus_actionable(conn)
        paper.ensure_tables(conn)
        paper.stage_candidates(conn, client=client, now=PREOPEN, cfg=_cfg())
        client.candles = [
            {
                "candle_at": int((opening + timedelta(minutes=index)).timestamp()),
                "open": 100.0,
                "high": 100.6,
                "low": 99.9,
                "close": 100.5,
            }
            for index in range(5)
        ] + [{
            "candle_at": int((opening + timedelta(minutes=5)).timestamp()),
            "open": 100.5,
            "high": 101.0,
            "low": 100.3,
            "close": 100.8,
        }, {
            "candle_at": int((opening + timedelta(minutes=6)).timestamp()),
            "open": 100.4,
            "high": 101.0,
            "low": 100.1,
            "close": 100.8,
        }]

        active = paper.process_active(
            conn, client=client, now=opening + timedelta(minutes=7), cfg=_cfg()
        )
        position = conn.execute(
            "SELECT status,risk_pct FROM mexc_stock_futures_paper_positions"
        ).fetchone()

        assert active["filled"] == 1
        assert position[0] == "OPEN"
        assert position[1] == pytest.approx(_cfg()["risk_per_trade_pct"] * 0.5, rel=0.02)


def test_three_partial_targets_and_model_f_are_deterministic():
    position = {
        "position_id": "p1",
        "direction": "long",
        "status": "OPEN",
        "entry_at": PREOPEN.isoformat(),
        "entry_price": 100.0,
        "stop_initial": 98.0,
        "stop_current": 98.0,
        "tp1": 103.0,
        "tp2": 105.0,
        "tp3": 108.0,
        "highest_tp_touched": 0,
        "remaining_weight": 1.0,
        "realized_r_accum": 0.0,
        "max_favorable_r": 0.0,
        "max_adverse_r": 0.0,
        "protection_stage": "INITIAL",
        "last_evaluated_at": PREOPEN.isoformat(),
    }
    candles = [
        {
            "candle_at": int((PREOPEN + timedelta(minutes=i)).timestamp()),
            "open": 100.0,
            "high": high,
            "low": 99.5 if i == 1 else 101.2,
            "close": high - 0.1,
        }
        for i, high in ((1, 103.1), (2, 105.1), (3, 108.1))
    ]
    result = paper._process_position_candles(
        position,
        candles,
        cfg=_cfg(),
        force_flat_at=PREOPEN + timedelta(hours=6),
    )
    assert result["status"] == "CLOSED"
    assert result["highest_tp_touched"] == 3
    assert result["close_reason"] == "tp3"
    assert result["paper_execution_r"] == pytest.approx(2.68)


def test_force_flat_uses_candle_open_before_later_tp_or_stop():
    force_at = datetime(2026, 7, 27, 19, 55, tzinfo=UTC)
    position = {
        "position_id": "p2",
        "direction": "long",
        "status": "OPEN",
        "entry_at": PREOPEN.isoformat(),
        "entry_price": 100.0,
        "stop_initial": 98.0,
        "stop_current": 98.0,
        "tp1": 103.0,
        "tp2": 105.0,
        "tp3": 108.0,
        "highest_tp_touched": 0,
        "remaining_weight": 1.0,
        "realized_r_accum": 0.0,
        "max_favorable_r": 0.0,
        "max_adverse_r": 0.0,
        "protection_stage": "INITIAL",
        "last_evaluated_at": PREOPEN.isoformat(),
    }
    result = paper._process_position_candles(
        position,
        [{
            "candle_at": int(force_at.timestamp()),
            "open": 101.0,
            "high": 109.0,
            "low": 97.0,
            "close": 108.0,
        }],
        cfg=_cfg(),
        force_flat_at=force_at,
    )
    assert result["close_reason"] == "same_day_time_exit"
    assert result["exit_price"] == 101.0
    assert result["paper_execution_r"] == pytest.approx(0.5)


def test_tick_never_mutates_source_or_live_tables(tmp_path, monkeypatch):
    db = tmp_path / "desk.sqlite"
    with _db(db) as conn:
        _seed(conn)
        before_signal = conn.execute("SELECT COUNT(*) FROM proposed_signals").fetchone()[0]
        before_outcome = conn.execute("SELECT COUNT(*) FROM signal_outcomes").fetchone()[0]
        before_live = conn.execute("SELECT COUNT(*) FROM live_orders").fetchone()[0]
    project = load_config()
    monkeypatch.setattr(
        paper,
        "load_config",
        lambda: replace(project, root=tmp_path),
    )
    result = paper.tick(db=db, now=PREOPEN, client=FakeMexc(), cfg=_cfg())
    assert result["status"] == "ok"
    with sqlite3.connect(db) as conn:
        assert conn.execute("SELECT COUNT(*) FROM proposed_signals").fetchone()[0] == before_signal
        assert conn.execute("SELECT COUNT(*) FROM signal_outcomes").fetchone()[0] == before_outcome
        assert conn.execute("SELECT COUNT(*) FROM live_orders").fetchone()[0] == before_live


def test_stock_futures_use_mexc_costs_funding_and_fixed_contract_size():
    cfg = {
        **paper.load_cfg(),
        "initial_equity_usdt": 5000,
        "risk_basis": "equity",
        "fee_profile": "bybit_non_vip_usdt_perp",
        "stock_futures_fee_profile": "mexc_default_futures",
        "stock_futures_slippage": {
            "major": 0.0003,
            "liquid_alt": 0.0008,
            "illiquid_alt": 0.0015,
        },
        "stock_majors": ["AAPL"],
    }
    profile, _, _, funding = resolve_cost_context(
        asset_class="stock_futures",
        mode="intraday",
        notional_usdt=1000,
        fee_profile="bybit_non_vip_usdt_perp",
        cfg=cfg,
    )
    assert profile == "mexc_default_futures"
    assert funding is None
    trade = {
        "signal_id": "s",
        "economic_trade_key": "mexc-stock-futures:p",
        "symbol": "AAPL",
        "asset_class": "stock_futures",
        "mode": "intraday",
        "direction": "long",
        "entry": 100.0,
        "stop": 98.0,
        "paper_execution_r": 1.0,
        "close_reason": "same_day_time_exit",
        "entry_at": PREOPEN.isoformat(),
        "exit_at": (PREOPEN + timedelta(hours=1)).isoformat(),
        "entry_order_type": "maker",
        "entry_funding_rate": 0.0001,
        "fixed_qty": 10.0,
        "fixed_risk_usdt": 20.0,
        "fixed_notional_usdt": 1000.0,
        "fixed_margin_used_usdt": 200.0,
        "fixed_leverage": 5,
        "size_weight": 1.0,
    }
    ledger = simulate_portfolio(
        [trade], cfg=cfg, fee_profile="bybit_non_vip_usdt_perp"
    )["ledger"][0]
    assert ledger["qty"] == 10.0
    assert ledger["risk_usdt"] == 20.0
    assert ledger["position_notional_usdt"] == 1000.0
    assert ledger["fees_usdt"] > 0
    assert ledger["slippage_usdt"] > 0
    assert ledger["funding_usdt"] == pytest.approx(0.1)
    assert ledger["funding_source"] == "mexc_entry_rate_estimate"


def test_monitor_forces_one_refresh_from_0910_et(tmp_path):
    session = object.__new__(StocksMonitorSession)
    session._preopen_decision_refresh_session = None
    cfg = _cfg()
    assert not session._preopen_decision_refresh_due(
        PREOPEN - timedelta(minutes=1), cfg
    )
    assert session._preopen_decision_refresh_due(PREOPEN, cfg)
    session._preopen_decision_refresh_session = "2026-07-27"
    assert not session._preopen_decision_refresh_due(
        PREOPEN + timedelta(minutes=1), cfg
    )


def test_standard_paper_live_bridge_runs_when_mexc_stock_paper_tick_fails(monkeypatch, tmp_path):
    """A public MEXC quote outage cannot hide a fresh standard Paper breakout."""

    class FailingPaper:
        def tick(self, **_kwargs):
            raise RuntimeError("MEXC transport error: ReadTimeout")

    captured: list[dict] = []

    def capture_standard(**kwargs):
        captured.append(kwargs)
        return {"status": "OK", "seen": 1, "queued": 1, "duplicate": 0,
                "rejected": 0, "reasons": {}, "risk_usdt": 5.0}

    monkeypatch.setattr(
        "src.live_execution.stocks_breakout_bridge.capture_standard_paper_breakouts",
        capture_standard,
    )
    session = object.__new__(StocksMonitorSession)
    session.config = SimpleNamespace(db_path=tmp_path / "monitor.sqlite")
    session.send_telegram = False
    result = MonitorTickResult(started_at=PREOPEN.isoformat(), finished_at=PREOPEN.isoformat())

    session._run_mexc_stock_paper(
        module=FailingPaper(), cfg={}, now=PREOPEN, notifier=None, result=result
    )

    assert result.mexc_stock_paper_failed == 1
    assert captured and captured[0]["db"] == session.config.db_path
    assert any(
        row.get("action") == "mexc_stock_standard_paper_live_bridge"
        and row.get("queued") == 1
        for row in result.decisions
    )
