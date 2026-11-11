from __future__ import annotations

import json
import sqlite3
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import requests

from src.live_execution.config import LiveCanaryConfig, load_live_canary_config
from src.live_execution.bybit_client import BybitAPIError
from src.live_execution.mexc_client import MexcAPIError, MexcFuturesClient
from src.live_execution.policy import evaluate_paper_candidate
from src.live_execution.service import (
    _exit_leg_verification_due, _open_positions_for_symbol, capture_paper_candidate,
    _maybe_reprice_swing_recovery,
    _authoritative_paper_execution_revalidation,
    _deliver_live_fill_notifications,
    _confirmed_active_exit_orders,
    _install_or_reconcile_exit_legs,
    _stage_live_preflight_rejection_notification,
    monitor_tick, operator_order_probe, recalculate_open_position_risk_accounting,
    recapture_terminal_preflight_rejection, invalidate_stale_queues,
    recover_closed_protection_failure, reconcile_once,
    status as canary_status, worker_once,
)
from src.live_execution.sizing import (
    PlanRejected, allocate_partial_tp_volumes, build_order_plan, model_f_stop,
    rebase_filled_plan, stop_risk_components,
)
from src.live_execution.venue_router import prepare_candidate
from src.live_execution import store as ls


class FakeStore:
    def __init__(self, path: Path):
        self.db_path = path

    def connect(self):
        conn = sqlite3.connect(self.db_path, timeout=30)
        conn.row_factory = sqlite3.Row
        return conn


class FakeNotifier:
    def __init__(self):
        self.messages = []
        self.enabled = True

    def send_fast(self, text, parse_mode=""):
        self.messages.append({"text": text, "parse_mode": parse_mode})
        return {"ok": True}


def cfg(**updates) -> LiveCanaryConfig:
    raw = deepcopy(load_live_canary_config().raw)
    raw.update({
        "submission_enabled": False,
        "execution_mode": "dry_run",
        "live_route_registry_path": str(
            Path(__file__).parent / "fixtures" / "live_routes_order_engine_test.yaml"
        ),
    })
    raw.update(updates)
    return LiveCanaryConfig(raw=raw)


def make_db(path: Path) -> FakeStore:
    conn = sqlite3.connect(path)
    conn.executescript("""
      CREATE TABLE entry_latency_audit (
        signal_id TEXT PRIMARY KEY, cause TEXT, data_gap_min REAL
      );
      CREATE TABLE proposed_signals(signal_id TEXT PRIMARY KEY);
      CREATE TABLE signal_outcomes(id INTEGER PRIMARY KEY, final_r REAL);
      CREATE TABLE paper_portfolio_ledger(id INTEGER PRIMARY KEY);
      CREATE TABLE signal_alerts(alert_id TEXT PRIMARY KEY);
      CREATE TABLE paper_execution_outcomes(
        signal_id TEXT PRIMARY KEY,
        computed_at TEXT,
        lifecycle_state TEXT,
        execution_validity TEXT,
        entry_at TEXT,
        entry_price_used REAL,
        stop_initial REAL,
        entry_time_basis TEXT,
        current_price_revalidated INTEGER,
        paper_entry_profile TEXT,
        paper_execution_entry_mode TEXT,
        close_reason TEXT
      );
    """)
    conn.execute("INSERT INTO entry_latency_audit VALUES('sig-live-1','OK',0)")
    conn.execute(
        "INSERT INTO paper_execution_outcomes VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
        (
            "sig-live-1", "2026-07-17T00:00:00+00:00", "OPEN", "valid",
            "2026-07-17T00:00:00+00:00", 100.0, 98.0,
            "point_in_time_current_bar", 1,
            "crypto_swing_paper_t130_v1", "LIMIT_THEN_TAKER_TIMEOUT", None,
        ),
    )
    conn.commit()
    conn.close()
    return FakeStore(path)


def signal() -> dict:
    return {
        "signal_id": "sig-live-1", "asset_class": "crypto", "mode": "swing",
        "direction": "long", "tier": "A", "score": 82, "symbol": "BTC/USDT",
        "created_at": "2026-07-17T00:00:00+00:00",
    }


def payload(**updates) -> dict:
    out = {
        "entry_used": 100.0, "stop": 98.0, "tp1": 103.0, "tp2": 106.0, "tp3": 110.0,
        "entry_triggered_at": "2026-07-17T00:00:00+00:00", "entry_age_seconds": 10,
        "entry_time_basis": "point_in_time_current_bar",
        "current_price_revalidated": True,
        "telegram_channel": "telegram", "size_weight": 1.0,
        "cqo_quality_action": "FULL_SIZE", "crypto_swing_main_paper_action": "FULL_SIZE",
        "cqo_entry_mode": "LIMIT_THEN_TAKER_TIMEOUT", "cqo_entry_mode_source": "entry_path",
        "cqo_preentry_data_quality": "ok", "cqo_snapshot_persisted": True,
        "cqo_overlay_version": "cqo_v1", "cqo_overlay_config_hash": "abc123",
        "paper_entry_profile": "crypto_swing_paper_t130_v1",
    }
    out.update(updates)
    return out


def test_stock_candidate_exits_crypto_policy_without_database_reads():
    class NoReadStore:
        calls = 0

        def connect(self):
            self.calls += 1
            raise AssertionError("out-of-scope stock candidate must not read crypto policy DB")

    store = NoReadStore()
    result = evaluate_paper_candidate(
        signal={**signal(), "asset_class": "stocks", "mode": "intraday"},
        payload=payload(),
        cfg=cfg(),
        store=store,
    )

    assert result == {"in_scope": False, "reasons": ["OUT_OF_SCOPE"]}
    assert store.calls == 0


def live_grade_decision_snapshot(**updates) -> dict:
    out = {
        "signal_id": "sig-live-1",
        "source_signal_id": "sig-live-1",
        "paper_alert_id": "alert-live-grade-1",
        "symbol": "PROVE/USDT",
        "asset_class": "crypto",
        "mode": "intraday",
        "direction": "long",
        "entry_mode": "BREAKOUT_CONTINUATION",
        "source_paper_profile": "crypto_intraday_breakout_paper_v1",
        "paper_entry_profile": "crypto_intraday_breakout_paper_v1",
        "strategy_version": "crypto_intraday_breakout_paper_v1",
        "decision_context_type": "point_in_time",
        "entry_time_basis": "point_in_time_current_bar",
        "current_price_revalidated": True,
        "entry_age_seconds": 1.0,
        "max_entry_age_seconds": 90.0,
        "entry_price": 100.0,
        "original_stop": 98.0,
        "tp1": 103.0,
        "tp2": 106.0,
        "tp3": 110.0,
    }
    out.update(updates)
    return out


def test_paper_revalidation_accepts_live_grade_frozen_snapshot_when_outcome_row_is_wrong_branch(tmp_path):
    store = make_db(tmp_path / "paper-row-wrong-branch.sqlite")
    with store.connect() as conn:
        conn.execute(
            "UPDATE paper_execution_outcomes "
            "SET paper_entry_profile=?,paper_execution_entry_mode=?,entry_price_used=?,"
            "stop_initial=?,entry_time_basis=?,current_price_revalidated=? "
            "WHERE signal_id='sig-live-1'",
            (
                "crypto_intraday_level_hold_v2_paper_v1",
                "LEVEL_HOLD_V2",
                101.0,
                99.0,
                "historical_not_currently_executable",
                0,
            ),
        )
        conn.commit()

    result = _authoritative_paper_execution_revalidation(
        db=store.db_path,
        decision=live_grade_decision_snapshot(),
    )

    assert result["ok"] is True
    assert result["authoritative_source"] == "frozen_live_decision_snapshot"
    assert result["paper_row_mismatch_accepted_from_frozen_decision"] is True
    assert result["paper_row_mismatch_reason"] == "PAPER_EXECUTION_ENTRY_MODE_MISMATCH"


def test_paper_revalidation_still_rejects_late_frozen_snapshot_when_outcome_row_is_wrong_branch(tmp_path):
    store = make_db(tmp_path / "paper-row-wrong-branch-late.sqlite")
    with store.connect() as conn:
        conn.execute(
            "UPDATE paper_execution_outcomes "
            "SET paper_entry_profile=?,paper_execution_entry_mode=? "
            "WHERE signal_id='sig-live-1'",
            ("crypto_intraday_level_hold_v2_paper_v1", "LEVEL_HOLD_V2"),
        )
        conn.commit()

    result = _authoritative_paper_execution_revalidation(
        db=store.db_path,
        decision=live_grade_decision_snapshot(
            entry_time_basis="historical_not_currently_executable",
            current_price_revalidated=False,
        ),
    )

    assert result["ok"] is False
    assert result["reason"] == "FROZEN_DECISION_NOT_POINT_IN_TIME"


def test_mexc_handoff_emits_capture_and_preflight_latency_events(tmp_path):
    store = make_db(tmp_path / "mexc-telemetry.sqlite")
    captured = capture_paper_candidate(
        store=store, signal=signal(), payload=payload(), cfg=cfg(),
        now=datetime.now(timezone.utc),
    )
    assert captured["status"] == "QUEUED"
    result = worker_once(db=store.db_path, cfg=cfg(), client=FakePublicClient())
    assert result["status"] == "DRY_RUN_PLANNED"
    with sqlite3.connect(store.db_path) as conn:
        events = {row[0] for row in conn.execute(
            "SELECT event_type FROM execution_latency_events WHERE signal_id='sig-live-1'"
        )}
    assert "mexc_decision_captured" in events
    assert "mexc_preflight_started" in events
    assert "mexc_preflight_passed" in events


def test_new_entry_waits_while_open_position_reconciliation_is_stale(tmp_path):
    store = make_db(tmp_path / "stale-position-entry-gate.sqlite")
    live_cfg = cfg(
        block_new_entries_when_open_position_reconciliation_stale=True,
        open_position_reconciliation_entry_block_seconds=60,
    )
    captured = capture_paper_candidate(
        store=store, signal=signal(), payload=payload(), cfg=live_cfg,
    )
    stale_at = (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat()
    with store.connect() as conn:
        conn.execute(
            "INSERT INTO mexc_canary_positions("
            "position_row_id,decision_id,symbol,status,entry_price,original_stop,current_stop,"
            "tp3,volume_contracts,notional_usdt,risk_usdt,leverage,opened_at,updated_at,"
            "last_reconciled_at,venue) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                "existing-position", "existing-decision", "ETH_USDT", "OPEN",
                100.0, 98.0, 98.0, 110.0, 1.0, 100.0, 5.0, 5,
                stale_at, stale_at, stale_at, "mexc",
            ),
        )
        conn.commit()

    result = worker_once(db=store.db_path, cfg=live_cfg, client=FakePublicClient())

    assert captured["queued"] is True
    assert result["status"] == "BLOCKED_STALE_OPEN_POSITION_RECONCILIATION"
    assert result["reason"] == "OPEN_POSITION_RECONCILIATION_STALE"
    with store.connect() as conn:
        queued = conn.execute(
            "SELECT status,attempt_count FROM mexc_canary_outbox"
        ).fetchone()
    assert tuple(queued) == ("QUEUED", 0)


def contract() -> dict:
    return {
        "symbol": "BTC_USDT", "state": 0, "apiAllowed": True, "futureType": 1,
        "quoteCoin": "USDT", "preMarket": False, "typeLabel": 0,
        "contractSize": 0.01, "priceUnit": 0.01, "volUnit": 1, "minVol": 1,
        "maxVol": 100000, "limitMaxVol": 100000, "minLeverage": 1, "maxLeverage": 200,
        "countryConfigContractMaxLeverage": 0, "makerFeeRate": 0.0,
        "takerFeeRate": 0.0001, "maintenanceMarginRate": 0.004,
        "liquidationFeeRate": 0.0004,
    }


def depth(ask=100.0, bid=99.95) -> dict:
    return {"asks": [[ask, 10, 1]], "bids": [[bid, 10, 1]], "timestamp": 1}


def test_bybit_rejects_stock_symbol_without_explicit_alias_marker():
    stock_decision = {
        "signal_id": "sig-stock-old",
        "asset_class": "stock_futures",
        "mode": "stock_intraday",
        "direction": "long",
        "tier": "B",
        "score": 91.0,
        "symbol": "AAPL/USDT",
        "entry_mode": "BREAKOUT_CONTINUATION",
        "entry_price": 100.0,
        "original_stop": 99.0,
        "tp1": 101.0,
        "tp2": 102.0,
        "tp3": 103.0,
        "venue_symbols": {"bybit": "AAPLUSDT"},
    }
    live_cfg = cfg(
        venue_routing={
            "enabled": True,
            "bybit": {
                "enabled": True,
                "submission_enabled": True,
                "require_explicit_stock_symbol": True,
            },
        }
    )
    with pytest.raises(PlanRejected, match="BYBIT_STOCK_SYMBOL_NOT_CONFIGURED"):
        prepare_candidate(
            venue="bybit",
            decision=stock_decision,
            cfg=live_cfg,
            captured_at="2026-07-17T00:00:00+00:00",
        )


class FakePublicClient:
    _access_key = ""

    def __init__(self, *, ask=100.0, bid=99.95):
        self.create_calls = 0
        self.ask = ask
        self.bid = bid

    def contract_info(self, symbol):
        return contract()

    def depth(self, symbol, limit=20):
        return depth(ask=self.ask, bid=self.bid)

    def create_order(self, order):
        self.create_calls += 1
        raise AssertionError("dry-run must never call private create_order")


def test_capture_reprices_late_crypto_swing_at_current_mexc_price(monkeypatch, tmp_path):
    store = make_db(tmp_path / "swing-reprice.sqlite")
    monkeypatch.setattr(
        "src.live_execution.service._client",
        lambda _cfg, *, private=False: FakePublicClient(ask=99.0, bid=98.95),
    )
    late_payload = payload(
        telegram_channel="shadow_only_late",
        size_weight=0.0,
        entry_time_basis="historical_bar_range",
        current_price_revalidated=False,
        entry_age_seconds=900,
        cqo_quality_action="HALF_SIZE",
        crypto_swing_main_paper_action="SHADOW_ONLY",
        cqo_requested_size_weight=0.5,
    )
    captured = capture_paper_candidate(
        store=store,
        signal=signal(),
        payload=late_payload,
        cfg=cfg(),
        now=datetime(2026, 7, 17, 0, 1, tzinfo=timezone.utc),
    )
    assert captured["status"] == "QUEUED"
    assert captured["queued"] is True
    assert captured["payload_overrides"]["mexc_live_repriced"] is True
    assert captured["payload_overrides"]["telegram_channel"] == "telegram"
    assert captured["payload_overrides"]["size_weight"] == 0.5

    with store.connect() as conn:
        saved = json.loads(conn.execute(
            "SELECT decision_json FROM mexc_canary_decisions"
        ).fetchone()[0])
        assert saved["entry_price"] == 99.0
        assert saved["entry_time_basis"] == "point_in_time_current_bar"
        assert saved["current_price_revalidated"] is True
        assert saved["entry_age_seconds"] == 0
        assert saved["paper_action"] == "HALF_SIZE"
        assert saved["paper_size_weight"] == 0.5
        assert saved["original_stop"] < saved["entry_price"] < saved["tp1"] < saved["tp2"] < saved["tp3"]


def test_late_crypto_swing_reprice_uses_recovery_adverse_drift_cap(monkeypatch, tmp_path):
    store = make_db(tmp_path / "swing-reprice-cap.sqlite")
    monkeypatch.setattr(
        "src.live_execution.service._client",
        lambda _cfg, *, private=False: FakePublicClient(ask=101.0, bid=100.95),
    )
    live_cfg = cfg(
        max_entry_drift_bps={"BREAKOUT_CONTINUATION": 15},
        swing_live_recovery={
            "enabled": True,
            "entry_modes": ["BREAKOUT_CONTINUATION"],
            "max_adverse_drift_bps": {"BREAKOUT_CONTINUATION": 150},
        },
        swing_live_reprice={"enabled": True},
    )
    captured = capture_paper_candidate(
        store=store,
        signal=signal(),
        payload=payload(
            telegram_channel="live_handoff",
            entry_time_basis="operator_recovery_requires_current_price",
            current_price_revalidated=False,
            entry_age_seconds=0,
            cqo_quality_action="HALF_SIZE",
            crypto_swing_main_paper_action="HALF_SIZE",
            size_weight=0.5,
        ),
        cfg=live_cfg,
    )

    assert captured["queued"] is True
    with store.connect() as conn:
        saved = json.loads(conn.execute(
            "SELECT decision_json FROM mexc_canary_decisions"
        ).fetchone()[0])
    assert saved["entry_price"] == 101.0
    assert saved["current_price_revalidated"] is True
    assert saved["entry_time_basis"] == "point_in_time_current_bar"
    assert saved["mexc_live_repriced"] is True


def test_terminal_notional_rejection_can_be_recaptured_without_order(monkeypatch, tmp_path):
    store = make_db(tmp_path / "terminal-recapture.sqlite")
    initial = capture_paper_candidate(
        store=store, signal=signal(), payload=payload(), cfg=cfg(),
        now=datetime(2026, 7, 17, 0, 0, tzinfo=timezone.utc),
    )
    assert initial["queued"]
    with store.connect() as conn:
        conn.execute(
            "UPDATE mexc_canary_outbox SET status='REJECTED_RISK_LIMIT',last_error='max_gross_notional'"
        )
        conn.execute("UPDATE mexc_canary_decisions SET state='REJECTED_RISK_LIMIT'")
        conn.commit()
    monkeypatch.setattr(
        "src.live_execution.service._client",
        lambda _cfg, *, private=False: FakePublicClient(ask=99.0, bid=98.95),
    )
    recovered = recapture_terminal_preflight_rejection(
        store=store,
        signal=signal(),
        payload=payload(),
        expected_error="max_gross_notional",
        cfg=cfg(),
        now=datetime(2026, 7, 17, 0, 1, tzinfo=timezone.utc),
    )
    assert recovered["queued"] is True
    with store.connect() as conn:
        outbox = conn.execute("SELECT status,attempt_count,last_error FROM mexc_canary_outbox").fetchone()
        frozen = json.loads(conn.execute("SELECT decision_json FROM mexc_canary_decisions").fetchone()[0])
        assert tuple(outbox) == ("QUEUED", 0, None)
        assert frozen["entry_price"] == 99.0
        assert conn.execute("SELECT COUNT(*) FROM mexc_canary_orders").fetchone()[0] == 0
        event = conn.execute(
            "SELECT payload_json FROM mexc_canary_events "
            "WHERE event_type='OPERATOR_RECAPTURED_TERMINAL_PRE_SUBMISSION_REJECTION'"
        ).fetchone()
        assert json.loads(event[0])["prior"]["outbox_error"] == "max_gross_notional"


def test_closed_protection_failure_gets_a_new_execution_key(monkeypatch, tmp_path):
    store = make_db(tmp_path / "protection-recovery.sqlite")
    captured = capture_paper_candidate(
        store=store, signal=signal(), payload=payload(), cfg=cfg(),
        now=datetime(2026, 7, 17, 0, 0, tzinfo=timezone.utc),
    )
    decision_id = captured["decision_id"]
    with store.connect() as conn:
        conn.execute("UPDATE mexc_canary_outbox SET status='SUBMITTED' WHERE decision_id=?", (decision_id,))
        conn.execute(
            "INSERT INTO mexc_canary_orders(order_row_id,decision_id,external_oid,symbol,status,updated_at,plan_json) "
            "VALUES(?,?,?,?,?,?,?)",
            ("old-order", decision_id, "old-external", "BTC_USDT", "FILLED", "2026-07-17T00:00:01+00:00", "{}"),
        )
        conn.execute(
            "INSERT INTO mexc_canary_positions(position_row_id,decision_id,symbol,status,entry_price,original_stop,"
            "current_stop,tp3,volume_contracts,notional_usdt,risk_usdt,leverage,max_favorable_r,protection_stage,opened_at,updated_at) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("old-position", decision_id, "BTC_USDT", "CLOSED", 100, 98, 98, 110, 1, 1, 1, 1, 0, "ORIGINAL_STOP",
             "2026-07-17T00:00:01+00:00", "2026-07-17T00:00:01+00:00"),
        )
        ls.event(conn, "MEXC_THREE_TP_INSTALL_FAILED", decision_id=decision_id, severity="CRITICAL")
        conn.commit()
    monkeypatch.setattr(
        "src.live_execution.service._client",
        lambda _cfg, *, private=False: FakePublicClient(ask=99.0, bid=98.95),
    )
    recovered = recover_closed_protection_failure(
        store=store, signal=signal(), payload=payload(), cfg=cfg(),
        now=datetime(2026, 7, 17, 0, 1, tzinfo=timezone.utc),
    )
    assert recovered["queued"] is True
    assert recovered["decision_id"] != decision_id
    with store.connect() as conn:
        rows = conn.execute("SELECT signal_id,decision_json FROM mexc_canary_decisions ORDER BY captured_at").fetchall()
        assert len(rows) == 2
        assert rows[1]["signal_id"].startswith("sig-live-1:mexc-recovery:")
        assert json.loads(rows[1]["decision_json"])["signal_id"] == "sig-live-1"


def test_capture_does_not_reprice_swing_after_unfavourable_drift(monkeypatch, tmp_path):
    store = make_db(tmp_path / "swing-reprice-reject.sqlite")
    monkeypatch.setattr(
        "src.live_execution.service._client",
        lambda _cfg, *, private=False: FakePublicClient(ask=105.0, bid=104.95),
    )
    captured = capture_paper_candidate(
        store=store,
        signal=signal(),
        payload=payload(
            telegram_channel="shadow_only_late",
            size_weight=0.0,
            entry_time_basis="historical_bar_range",
            current_price_revalidated=False,
            entry_age_seconds=900,
                cqo_quality_action="HALF_SIZE",
                crypto_swing_main_paper_action="SHADOW_ONLY",
                cqo_requested_size_weight=0.5,
                paper_execution_entry_mode="BREAKOUT_CONTINUATION",
            ),
            cfg=cfg(),
            now=datetime(2026, 7, 17, 0, 1, tzinfo=timezone.utc),
    )
    assert captured["status"] == "REJECTED"
    assert captured["queued"] is False
    assert "ENTRY_NOT_POINT_IN_TIME" in captured["reasons"]
    assert "CURRENT_PRICE_NOT_REVALIDATED" in captured["reasons"]
    assert not captured["payload_overrides"]


def test_capture_reprices_late_crypto_swing_short(monkeypatch, tmp_path):
    store = make_db(tmp_path / "swing-reprice-short.sqlite")
    monkeypatch.setattr(
        "src.live_execution.service._client",
        lambda _cfg, *, private=False: FakePublicClient(ask=100.56, bid=100.51),
    )
    sig = signal()
    sig["direction"] = "short"
    captured = capture_paper_candidate(
        store=store,
        signal=sig,
        payload=payload(
            entry_used=100.0, stop=102.0, tp1=97.0, tp2=94.0, tp3=90.0,
            telegram_channel="shadow_only_late",
            size_weight=0.0,
            entry_time_basis="historical_bar_range",
            current_price_revalidated=False,
            entry_age_seconds=900,
            cqo_quality_action="HALF_SIZE",
            crypto_swing_main_paper_action="SHADOW_ONLY",
            cqo_requested_size_weight=0.5,
        ),
        cfg=cfg(),
        now=datetime(2026, 7, 17, 0, 1, tzinfo=timezone.utc),
    )
    assert captured["status"] == "QUEUED"
    with store.connect() as conn:
        saved = json.loads(conn.execute(
            "SELECT decision_json FROM mexc_canary_decisions"
        ).fetchone()[0])
        assert saved["direction"] == "short"
        assert saved["tp3"] < saved["tp2"] < saved["tp1"] < saved["entry_price"] < saved["original_stop"]
        assert saved["paper_size_weight"] == 0.5


class WideSpreadPublicClient(FakePublicClient):
    def depth(self, symbol, limit=20):
        return depth(100.30, 100.0)


class RateLimitedPublicClient(FakePublicClient):
    def contract_info(self, symbol):
        raise MexcAPIError(
            "MEXC request rejected: Requests are too frequent, please try again later",
            status_code=429,
        )


class PumpAliasPublicClient(FakePublicClient):
    def __init__(self):
        super().__init__()
        self.symbols = []

    def contract_info(self, symbol):
        self.symbols.append(("contract", symbol))
        assert symbol == "PUMPFUN_USDT"
        row = contract()
        row.update({
            "symbol": "PUMPFUN_USDT", "contractSize": 100.0,
            "priceUnit": 0.000001, "maxLeverage": 100,
        })
        return row

    def depth(self, symbol, limit=20):
        self.symbols.append(("depth", symbol))
        assert symbol == "PUMPFUN_USDT"
        return depth(0.002239, 0.002238)


class FakePrivateClient(FakePublicClient):
    _access_key = "fake"

    def __init__(self, *, direction="long"):
        super().__init__()
        self.direction = direction
        self.created = []
        self.modified = []
        self.probe_canceled = False
        self.tpsl = []
        self._next_tpsl_id = 100
        self.close_limits = []
        self._next_close_id = 200

    def account_asset(self, currency="USDT"):
        return {"equity": 100.0, "availableOpen": 100.0}

    def open_positions(self, symbol=None):
        if not self.created:
            return []
        return [{
            "positionId": 77, "symbol": "BTC_USDT", "holdVol": self.created[-1]["vol"],
            "positionType": 1 if self.direction == "long" else 2,
            "openType": 1, "state": 1, "openAvgPrice": 100.0,
            "liquidatePrice": 90.0 if self.direction == "long" else 110.0,
            "leverage": self.created[-1]["leverage"],
        }]

    def create_order(self, order):
        self.create_calls += 1
        self.created.append(order)
        if order.get("side") in {1, 3} and order.get("stopLossPrice"):
            self.tpsl = [{
                "id": 88, "positionId": 77, "state": 1,
                "stopLossPrice": order["stopLossPrice"], "takeProfitPrice": 0,
                "vol": order["vol"],
            }]
        return {"orderId": "9001", "ts": 1}

    def order_by_external_id(self, symbol, external_oid):
        if external_oid.startswith("probe_"):
            return {
                "orderId": "probe-1", "externalOid": external_oid,
                "state": 4 if self.probe_canceled else 1, "dealVol": 0,
            }
        return {
            "orderId": "9001", "externalOid": external_oid, "state": 3, "positionId": 77,
            "dealAvgPrice": 100.0, "dealVol": self.created[-1]["vol"],
        }

    def ticker(self, symbol):
        price = 102.0 if self.direction == "long" else 98.0
        return {"fairPrice": price, "lastPrice": price}

    def recent_high(self, symbol, *, start_seconds, end_seconds=None):
        return 102.0

    def recent_low(self, symbol, *, start_seconds, end_seconds=None):
        return 98.0

    def open_tpsl_orders(self, symbol=None):
        return list(self.tpsl)

    def modify_tpsl(self, **kwargs):
        self.modified.append(kwargs)
        for item in self.tpsl:
            if int(item["id"]) == int(kwargs["stop_plan_order_id"]):
                item["stopLossPrice"] = kwargs["stop_loss"]
                if kwargs.get("take_profit") is not None:
                    item["takeProfitPrice"] = kwargs["take_profit"]
        return True

    def place_position_tpsl(self, **kwargs):
        self._next_tpsl_id += 1
        self.tpsl.append({
            "id": self._next_tpsl_id, "positionId": kwargs["position_id"], "state": 1,
            "stopLossPrice": kwargs["stop_loss"], "takeProfitPrice": kwargs["take_profit"],
            "vol": kwargs["volume"],
        })
        return self._next_tpsl_id

    def place_close_limit(self, **kwargs):
        self._next_close_id += 1
        side = 4 if kwargs["direction"] == "long" else 2
        order = {
            "orderId": str(self._next_close_id),
            "externalOid": kwargs["external_oid"],
            "positionId": kwargs["position_id"],
            "symbol": "BTC_USDT",
            "state": 1,
            "side": side,
            "price": kwargs["price"],
            "vol": kwargs["volume"],
        }
        self.close_limits.append(order)
        return {"orderId": order["orderId"]}

    def order_by_id(self, order_id):
        return dict(next(
            item for item in self.close_limits if str(item["orderId"]) == str(order_id)
        ))

    def cancel_tpsl_order_ids(self, order_ids):
        wanted = {str(value) for value in order_ids}
        self.tpsl = [item for item in self.tpsl if str(item["id"]) not in wanted]
        return True

    def historical_positions(self, symbol=None, page_size=100):
        return []

    def emergency_close_long(self, **kwargs):
        raise AssertionError("safe fake position must not be emergency-closed")

    def emergency_close_short(self, **kwargs):
        raise AssertionError("safe fake position must not be emergency-closed")

    def cancel_external(self, symbol, external_oid):
        self.probe_canceled = True
        return {"orderId": "probe-1", "errorCode": 0, "errorMsg": "success"}

    def cancel_order_ids(self, order_ids):
        self.probe_canceled = True
        wanted = {str(value) for value in order_ids}
        for item in self.close_limits:
            if str(item["orderId"]) in wanted:
                item["state"] = 4
        return [{"orderId": order_ids[0], "errorCode": 0, "errorMsg": "success"}]


def test_default_config_uses_fixed_ten_usdt_risk_with_fifty_usdt_portfolio_cap(monkeypatch):
    # ``live_armed`` is true when either configured venue is armed.  Keep this
    # config-default test independent of an operator's MEXC/Bybit environment.
    for name in (
        "MEXC_CANARY_ACCESS_KEY", "MEXC_CANARY_SECRET", "MEXC_LIVE_CANARY_ARMED",
        "BYBIT_LIVE_ACCESS_KEY", "BYBIT_LIVE_SECRET", "BYBIT_LIVE_ARMED",
        "BYBIT_API_KEY", "BYBIT_API_SECRET",
    ):
        monkeypatch.delenv(name, raising=False)
    c = load_live_canary_config()
    assert c.risk_per_trade_usdt == 10.0
    assert c.max_concurrent_risk_usdt == 50.0
    assert c.submission_enabled is True
    assert c.execution_mode == "live"
    assert c.live_armed() is False
    assert c.get("strategy_profile") == "production_t130_targets"
    assert c.get("strategy_version") == "crypto_swing_paper_t130_v1"
    assert c.allowed_modes() == {"swing", "intraday", "invest"}
    assert c.allowed_profiles("intraday") == {
        "crypto_intraday_breakout_paper_v1",
        "crypto_intraday_pullback_paper_v1",
    }
    assert c.allowed_profiles("invest") == {"crypto_invest_regime_conditioned_v1"}
    assert c.allowed_profiles("liquidity_sweep") == set()
    assert c.get("allowed_entry_modes_by_mode", {}).get("swing") == [
        "LIMIT_THEN_TAKER_TIMEOUT",
    ]
    assert c.get("allowed_entry_modes_by_mode", {}).get("intraday") == [
        "BREAKOUT_CONTINUATION",
        "PULLBACK_LIMIT",
    ]
    assert not c.get("allow_unprofiled_strategy_versions_by_mode", {}).get("intraday")
    assert c.get("swing_live_recovery", {}).get("entry_modes") == [
        "LIMIT_THEN_TAKER_TIMEOUT",
    ]
    assert c.get("allowed_entry_modes_by_mode", {}).get("liquidity_sweep") is None
    assert c.get("liquidity_sweep_live_recovery", {}).get("enabled") is False
    assert c.get("allowed_directions") == ["long", "short"]
    text = Path("config/mexc_live_canary.yaml").read_text(encoding="utf-8")
    assert "mx0vgl" not in text
    assert "ea8203" not in text


def test_policy_accepts_clean_point_in_time_production_paper(tmp_path):
    store = make_db(tmp_path / "t.sqlite")
    rec = evaluate_paper_candidate(signal=signal(), payload=payload(), cfg=cfg(), store=store,
                                   now=datetime(2026, 7, 17, tzinfo=timezone.utc))
    assert rec["eligible"] == 1
    assert rec["reasons"] == []
    frozen = json.loads(rec["decision_json"])
    assert frozen["decision_context_type"] == "point_in_time"
    assert frozen["entry_mode"] == "LIMIT_THEN_TAKER_TIMEOUT"


def test_policy_prefers_paper_execution_mode_over_cqo_hint(tmp_path):
    store = make_db(tmp_path / "paper-mode-authority.sqlite")
    rec = evaluate_paper_candidate(
        signal=signal(),
        payload=payload(
            cqo_entry_mode="BREAKOUT_CONTINUATION",
            paper_execution_entry_mode="LIMIT_THEN_TAKER_TIMEOUT",
        ),
        cfg=cfg(),
        store=store,
        now=datetime(2026, 7, 17, tzinfo=timezone.utc),
    )
    assert rec["eligible"] == 1
    frozen = json.loads(rec["decision_json"])
    assert frozen["entry_mode"] == "LIMIT_THEN_TAKER_TIMEOUT"
    assert rec["reasons"] == []


def test_capture_hydrates_missing_paper_profile_before_live_policy(tmp_path):
    store = make_db(tmp_path / "paper-provenance-hydration.sqlite")
    captured = capture_paper_candidate(
        store=store,
        signal=signal(),
        payload=payload(
            cqo_entry_mode="LIMIT_THEN_TAKER_TIMEOUT",
            paper_entry_profile=None,
            paper_execution_entry_mode=None,
        ),
        cfg=cfg(),
        now=datetime(2026, 7, 17, tzinfo=timezone.utc),
    )
    assert captured["status"] == "QUEUED"
    assert captured["payload_overrides"]["paper_execution_provenance_hydrated"] is True
    with store.connect() as conn:
        saved = json.loads(conn.execute(
            "SELECT decision_json FROM mexc_canary_decisions"
        ).fetchone()[0])
    assert saved["paper_entry_profile"] == "crypto_swing_paper_t130_v1"
    assert saved["entry_mode"] == "LIMIT_THEN_TAKER_TIMEOUT"


def test_policy_rejects_legacy_crypto_swing_pullback_while_v2_is_paper_only(tmp_path):
    entry_mode = "PULLBACK_LIMIT"
    store = make_db(tmp_path / f"{entry_mode.lower()}.sqlite")
    rec = evaluate_paper_candidate(
        signal=signal(),
        payload=payload(cqo_entry_mode=entry_mode, entry_age_seconds=30),
        cfg=cfg(), store=store, now=datetime(2026, 7, 17, tzinfo=timezone.utc),
    )
    assert rec["eligible"] == 0
    assert "ENTRY_MODE_NOT_ALLOWED" in rec["reasons"]
    assert "LIVE_ROUTE_DISABLED" in rec["reasons"]


def test_policy_accepts_intraday_breakout_canary_with_versioned_profile(tmp_path):
    store = make_db(tmp_path / "intraday-breakout-canary.sqlite")
    sig = signal()
    sig["mode"] = "intraday"
    rec = evaluate_paper_candidate(
        signal=sig,
        payload=payload(
            cqo_entry_mode="PULLBACK_LIMIT",
            paper_entry_profile="crypto_intraday_breakout_paper_v1",
            paper_execution_entry_mode="BREAKOUT_CONTINUATION",
            entry_age_seconds=30,
        ),
        cfg=cfg(), store=store, now=datetime(2026, 7, 17, tzinfo=timezone.utc),
    )

    assert rec["eligible"] == 1
    assert rec["reasons"] == []
    frozen = json.loads(rec["decision_json"])
    assert frozen["mode"] == "intraday"
    assert frozen["entry_mode"] == "BREAKOUT_CONTINUATION"
    assert frozen["live_risk_multiplier"] == 0.5


def test_policy_accepts_intraday_pullback_canary_with_versioned_profile(tmp_path):
    store = make_db(tmp_path / "intraday-pullback-canary.sqlite")
    sig = signal()
    sig["mode"] = "intraday"
    rec = evaluate_paper_candidate(
        signal=sig,
        payload=payload(
            cqo_entry_mode="PULLBACK_LIMIT",
            paper_entry_profile="crypto_intraday_pullback_paper_v1",
            paper_execution_entry_mode="PULLBACK_LIMIT",
            entry_age_seconds=30,
        ),
        cfg=cfg(), store=store, now=datetime(2026, 7, 17, tzinfo=timezone.utc),
    )

    assert rec["eligible"] == 1
    assert rec["reasons"] == []
    frozen = json.loads(rec["decision_json"])
    assert frozen["mode"] == "intraday"
    assert frozen["entry_mode"] == "PULLBACK_LIMIT"
    assert frozen["paper_entry_profile"] == "crypto_intraday_pullback_paper_v1"
    assert frozen["live_risk_multiplier"] == 0.5


def test_policy_rejects_unprofiled_intraday_pullback_canary(tmp_path):
    store = make_db(tmp_path / "intraday-pullback-unprofiled.sqlite")
    sig = signal()
    sig["mode"] = "intraday"
    rec = evaluate_paper_candidate(
        signal=sig,
        payload=payload(
            cqo_entry_mode="PULLBACK_LIMIT",
            paper_entry_profile=None,
            paper_execution_entry_mode="PULLBACK_LIMIT",
            entry_age_seconds=30,
        ),
        cfg=cfg(), store=store, now=datetime(2026, 7, 17, tzinfo=timezone.utc),
    )

    assert rec["eligible"] == 0
    assert "PAPER_STRATEGY_VERSION_MISSING" in rec["reasons"]


def test_timeout_fallback_rejects_handoff_beyond_live_window(tmp_path):
    store = make_db(tmp_path / "timeout-stale.sqlite")
    rec = evaluate_paper_candidate(
        signal=signal(),
        payload=payload(cqo_entry_mode="LIMIT_THEN_TAKER_TIMEOUT", entry_age_seconds=301),
        cfg=cfg(), store=store,
    )
    assert rec["eligible"] == 0
    assert "ENTRY_TOO_OLD" in rec["reasons"]


def test_legacy_swing_pullback_no_longer_reaches_dry_run_preflight(tmp_path):
    entry_mode = "PULLBACK_LIMIT"
    store = make_db(tmp_path / f"{entry_mode.lower()}-handoff.sqlite")
    captured = capture_paper_candidate(
        store=store,
        signal=signal(),
        payload=payload(
            cqo_entry_mode=entry_mode,
            paper_execution_entry_mode=entry_mode,
            entry_age_seconds=10,
        ),
        cfg=cfg(),
        now=datetime.now(timezone.utc),
    )
    assert captured["status"] == "REJECTED"
    assert captured["queued"] is False
    assert "ENTRY_MODE_NOT_ALLOWED" in captured["reasons"]


def test_policy_accepts_clean_short_t130_paper_with_directional_geometry(tmp_path):
    store = make_db(tmp_path / "short.sqlite")
    short_signal = {**signal(), "signal_id": "sig-live-1", "direction": "short"}
    rec = evaluate_paper_candidate(
        signal=short_signal,
        payload=payload(entry_used=100.0, stop=102.0, tp1=97.0, tp2=94.0, tp3=90.0),
        cfg=cfg(), store=store, now=datetime(2026, 7, 17, tzinfo=timezone.utc),
    )
    assert rec["eligible"] == 1
    assert json.loads(rec["decision_json"])["direction"] == "short"


def test_policy_accepts_verified_intraday_breakout_execution_profile(tmp_path):
    store = make_db(tmp_path / "intraday-profile.sqlite")
    intraday_signal = {**signal(), "mode": "intraday"}
    intraday_payload = payload(
        cqo_entry_mode="BREAKOUT_CONTINUATION",
        cqo_entry_mode_source="paper_execution_profile",
        cqo_quality_action="HALF_SIZE",
        crypto_swing_main_paper_action="HALF_SIZE",
        size_weight=0.5,
        paper_entry_profile="crypto_intraday_breakout_paper_v1",
    )
    rec = evaluate_paper_candidate(
        signal=intraday_signal, payload=intraday_payload, cfg=cfg(), store=store,
        now=datetime(2026, 7, 17, tzinfo=timezone.utc),
    )
    assert rec["eligible"] == 1
    assert rec["reasons"] == []
    frozen = json.loads(rec["decision_json"])
    assert frozen["entry_mode"] == "BREAKOUT_CONTINUATION"
    assert frozen["live_risk_multiplier"] == 0.5


def test_intraday_breakout_missing_latency_override_is_live_eligible_when_fresh(tmp_path):
    store = make_db(tmp_path / "intraday-no-data-latency.sqlite")
    with store.connect() as conn:
        conn.execute("UPDATE entry_latency_audit SET cause='NO_DATA',data_gap_min=NULL")
        conn.commit()
    intraday_signal = {**signal(), "mode": "intraday"}
    intraday_payload = payload(
        cqo_entry_mode="BREAKOUT_CONTINUATION",
        cqo_entry_mode_source="paper_execution_profile",
        cqo_quality_action="HALF_SIZE",
        crypto_swing_main_paper_action="HALF_SIZE",
        size_weight=0.5,
        paper_entry_profile="crypto_intraday_breakout_paper_v1",
        entry_age_seconds=1.0,
    )
    rec = evaluate_paper_candidate(
        signal=intraday_signal, payload=intraday_payload, cfg=cfg(), store=store,
        now=datetime(2026, 7, 17, tzinfo=timezone.utc),
    )
    assert rec["eligible"] == 1
    assert rec["reasons"] == []
    assert json.loads(rec["decision_json"])["latency_missing_override"] is True


def test_missing_latency_override_does_not_bypass_entry_age(tmp_path):
    store = make_db(tmp_path / "intraday-no-data-stale.sqlite")
    with store.connect() as conn:
        conn.execute("UPDATE entry_latency_audit SET cause='NO_DATA',data_gap_min=NULL")
        conn.commit()
    intraday_signal = {**signal(), "mode": "intraday"}
    intraday_payload = payload(
        cqo_entry_mode="BREAKOUT_CONTINUATION",
        cqo_entry_mode_source="paper_execution_profile",
        cqo_quality_action="HALF_SIZE",
        crypto_swing_main_paper_action="HALF_SIZE",
        size_weight=0.5,
        paper_entry_profile="crypto_intraday_breakout_paper_v1",
        entry_age_seconds=999.0,
    )
    rec = evaluate_paper_candidate(
        signal=intraday_signal, payload=intraday_payload, cfg=cfg(), store=store,
        now=datetime(2026, 7, 17, tzinfo=timezone.utc),
    )
    assert rec["eligible"] == 0
    assert "ENTRY_TOO_OLD" in rec["reasons"]
    assert "LATENCY_NOT_CLEAN" in rec["reasons"]


@pytest.mark.parametrize(("change", "reason"), [
    ({"cqo_entry_mode_source": "scheduler_backfill"}, "PREENTRY_NOT_POINT_IN_TIME"),
    ({"entry_age_seconds": 301}, "ENTRY_TOO_OLD"),
    ({"entry_time_basis": "historical_bar_range"}, "ENTRY_NOT_POINT_IN_TIME"),
    ({"current_price_revalidated": False}, "CURRENT_PRICE_NOT_REVALIDATED"),
    ({"paper_entry_dry_run": True}, "PAPER_DRY_RUN"),
])
def test_policy_rejects_non_live_evidence(tmp_path, change, reason):
    store = make_db(tmp_path / "t.sqlite")
    rec = evaluate_paper_candidate(signal=signal(), payload=payload(**change), cfg=cfg(), store=store)
    assert rec["eligible"] == 0
    assert reason in rec["reasons"]


def test_policy_rejects_unversioned_legacy_paper_alert(tmp_path):
    store = make_db(tmp_path / "legacy-profile.sqlite")
    rec = evaluate_paper_candidate(
        signal=signal(), payload=payload(paper_entry_profile=""), cfg=cfg(), store=store,
    )
    assert rec["eligible"] == 0
    assert "PAPER_STRATEGY_VERSION_MISSING" in rec["reasons"]


def test_policy_rejects_data_gap_late(tmp_path):
    store = make_db(tmp_path / "t.sqlite")
    with store.connect() as conn:
        conn.execute("UPDATE entry_latency_audit SET cause='DATA_GAP_LATE',data_gap_min=90")
        conn.commit()
    rec = evaluate_paper_candidate(signal=signal(), payload=payload(), cfg=cfg(), store=store)
    assert rec["eligible"] == 0
    assert "LATENCY_NOT_CLEAN" in rec["reasons"]


def test_policy_allows_legitimate_swing_wait_when_entry_is_revalidated(tmp_path):
    store = make_db(tmp_path / "legitimate-wait.sqlite")
    with store.connect() as conn:
        conn.execute("UPDATE entry_latency_audit SET cause='LEGITIMATE_LATE',data_gap_min=180")
        conn.commit()
    rec = evaluate_paper_candidate(signal=signal(), payload=payload(), cfg=cfg(), store=store)
    assert rec["eligible"] == 1
    assert "LATENCY_NOT_CLEAN" not in rec["reasons"]


def test_policy_accepts_clean_detection_latency_with_fresh_revalidated_entry(tmp_path):
    store = make_db(tmp_path / "detection-latency.sqlite")
    with store.connect() as conn:
        conn.execute("UPDATE entry_latency_audit SET cause='DETECTION_LATENCY',data_gap_min=5")
        conn.commit()
    rec = evaluate_paper_candidate(signal=signal(), payload=payload(), cfg=cfg(), store=store)
    assert rec["eligible"] == 1
    assert "LATENCY_NOT_CLEAN" not in rec["reasons"]


def test_policy_rejects_clean_detection_latency_when_gap_is_genuinely_large(tmp_path):
    store = make_db(tmp_path / "detection-latency-large-gap.sqlite")
    with store.connect() as conn:
        conn.execute("UPDATE entry_latency_audit SET cause='DETECTION_LATENCY',data_gap_min=90")
        conn.commit()
    rec = evaluate_paper_candidate(signal=signal(), payload=payload(), cfg=cfg(), store=store)
    assert rec["eligible"] == 0
    assert "LATENCY_NOT_CLEAN" in rec["reasons"]


def test_intraday_shadow_action_does_not_claim_swing_policy_rejection(tmp_path):
    store = make_db(tmp_path / "intraday-reason-label.sqlite")
    intraday = {**signal(), "mode": "intraday"}
    rec = evaluate_paper_candidate(
        signal=intraday,
        payload=payload(
            cqo_entry_mode="BREAKOUT_CONTINUATION",
            cqo_entry_mode_source="paper_execution_profile",
            cqo_quality_action="SHADOW_ONLY",
            crypto_swing_main_paper_action="SHADOW_ONLY",
            size_weight=0.0,
            paper_entry_profile="crypto_intraday_breakout_paper_v1",
        ),
        cfg=cfg(), store=store,
    )
    assert rec["eligible"] == 0
    assert "PAPER_ACTION_NOT_LIVE_ENABLED" in rec["reasons"]
    assert "SWING_POLICY_ACTION_NOT_LIVE_ENABLED" not in rec["reasons"]


def test_policy_accepts_t130_paper_profile_after_explicit_live_reconfiguration(tmp_path):
    store = make_db(tmp_path / "t130.sqlite")
    rec = evaluate_paper_candidate(
        signal=signal(), payload=payload(paper_entry_profile="crypto_swing_paper_t130_v1"), cfg=cfg(), store=store,
    )
    assert rec["eligible"] == 1
    assert rec["reasons"] == []


def test_policy_mirrors_actionable_half_size_paper_with_half_live_risk(tmp_path):
    store = make_db(tmp_path / "t.sqlite")
    rec = evaluate_paper_candidate(
        signal=signal(),
        payload=payload(cqo_quality_action="HALF_SIZE", crypto_swing_main_paper_action="HALF_SIZE",
                        size_weight=0.5, cqo_reasons=["exposure_alt_beta_same_direction"]),
        cfg=cfg(), store=store,
    )
    assert rec["eligible"] == 1 and rec["reasons"] == []
    frozen = json.loads(rec["decision_json"])
    assert frozen["paper_action"] == "HALF_SIZE"
    assert frozen["live_risk_multiplier"] == 0.5
    frozen["decision_id"] = "half-risk-decision"
    plan = build_order_plan(decision=frozen, contract=contract(), depth=depth(), cfg=cfg())
    assert plan.risk_budget_usdt == 5.0
    assert plan.actual_risk_usdt <= 5.0


def test_policy_accepts_swing_limit_then_taker_with_half_live_risk(tmp_path):
    store = make_db(tmp_path / "swing-limit-then-taker.sqlite")
    rec = evaluate_paper_candidate(
        signal=signal(),
        payload=payload(cqo_entry_mode="LIMIT_THEN_TAKER_TIMEOUT", entry_age_seconds=120),
        cfg=cfg(), store=store,
    )
    assert rec["eligible"] == 1 and rec["reasons"] == []
    frozen = json.loads(rec["decision_json"])
    assert frozen["entry_mode"] == "LIMIT_THEN_TAKER_TIMEOUT"
    assert frozen["live_route_key"] == "crypto_swing_limit_then_taker"
    assert frozen["live_risk_multiplier"] == 0.5


def test_policy_rejects_intraday_level_hold_v2_after_live_demotion(tmp_path):
    store = make_db(tmp_path / "intraday-level-hold-v2.sqlite")
    intraday = {**signal(), "mode": "intraday"}
    rec = evaluate_paper_candidate(
        signal=intraday,
        payload=payload(
            cqo_entry_mode="LEVEL_HOLD_V2",
            paper_execution_entry_mode="LEVEL_HOLD_V2",
            cqo_entry_mode_source="paper_execution_profile",
            paper_entry_profile="crypto_intraday_level_hold_v2_paper_v1",
            entry_age_seconds=30,
        ),
        cfg=cfg(), store=store,
    )
    assert rec["eligible"] == 0
    assert "ENTRY_MODE_NOT_ALLOWED" in rec["reasons"]
    assert "LIVE_ROUTE_DISABLED" in rec["reasons"]


@pytest.mark.parametrize("entry_mode", ["MOMENTUM_TAKER_NOW", "NO_CHASE_SKIP"])
def test_policy_keeps_unapproved_swing_taker_like_routes_out_of_live(tmp_path, entry_mode):
    store = make_db(tmp_path / f"{entry_mode.lower()}.sqlite")
    rec = evaluate_paper_candidate(
        signal=signal(),
        payload=payload(
            cqo_entry_mode=entry_mode,
            cqo_quality_action="FULL_SIZE",
            crypto_swing_main_paper_action="FULL_SIZE",
            size_weight=1.0,
        ),
        cfg=cfg(), store=store,
    )
    assert rec["eligible"] == 0
    assert "ENTRY_MODE_NOT_ALLOWED" in rec["reasons"]


def test_policy_does_not_expand_intraday_to_taker_like_entry_modes(tmp_path):
    store = make_db(tmp_path / "intraday-momentum-block.sqlite")
    intraday = {**signal(), "mode": "intraday"}
    rec = evaluate_paper_candidate(
        signal=intraday,
        payload=payload(
            cqo_entry_mode="MOMENTUM_TAKER_NOW",
            cqo_entry_mode_source="paper_execution_profile",
            cqo_quality_action="HALF_SIZE",
            crypto_swing_main_paper_action="HALF_SIZE",
            size_weight=0.5,
            paper_entry_profile="crypto_intraday_breakout_paper_v1",
        ),
        cfg=cfg(), store=store,
    )
    assert rec["eligible"] == 0
    assert "ENTRY_MODE_NOT_ALLOWED" in rec["reasons"]


@pytest.mark.parametrize("entry_mode", ["LIMIT_THEN_TAKER_TIMEOUT"])
def test_intraday_unapproved_limit_routes_stay_blocked(tmp_path, entry_mode):
    store = make_db(tmp_path / f"intraday-{entry_mode.lower()}-block.sqlite")
    intraday = {**signal(), "mode": "intraday"}
    rec = evaluate_paper_candidate(
        signal=intraday,
        payload=payload(
            cqo_entry_mode=entry_mode,
            cqo_entry_mode_source="paper_execution_profile",
            cqo_quality_action="HALF_SIZE",
            crypto_swing_main_paper_action="HALF_SIZE",
            size_weight=0.5,
            paper_entry_profile="crypto_intraday_breakout_paper_v1",
        ),
        cfg=cfg(), store=store,
    )
    assert rec["eligible"] == 0
    assert "ENTRY_MODE_NOT_ALLOWED" in rec["reasons"]


def test_intraday_breakout_is_live_eligible_with_versioned_paper_profile(tmp_path):
    store = make_db(tmp_path / "breakout-half.sqlite")
    intraday = {**signal(), "mode": "intraday"}
    rec = evaluate_paper_candidate(
        signal=intraday,
        payload=payload(
            cqo_entry_mode="BREAKOUT_CONTINUATION",
            paper_entry_profile="crypto_intraday_breakout_paper_v1",
            paper_execution_entry_mode="BREAKOUT_CONTINUATION",
            paper_source_entry_mode="BREAKOUT_CONTINUATION",
            entry_age_seconds=89,
        ),
        cfg=cfg(), store=store,
    )
    assert rec["eligible"] == 1
    assert rec["reasons"] == []


def test_intraday_breakout_live_window_accepts_fresh_edge(tmp_path):
    store = make_db(tmp_path / "breakout-window.sqlite")
    intraday = {**signal(), "mode": "intraday"}
    base = payload(
        cqo_entry_mode="BREAKOUT_CONTINUATION",
        paper_entry_profile="crypto_intraday_breakout_paper_v1",
        paper_execution_entry_mode="BREAKOUT_CONTINUATION",
        paper_source_entry_mode="BREAKOUT_CONTINUATION",
        entry_age_seconds=90,
    )
    rec = evaluate_paper_candidate(signal=intraday, payload=base, cfg=cfg(), store=store)
    assert rec["eligible"] == 1
    assert rec["reasons"] == []


def test_intraday_breakout_requires_matching_canonical_paper_before_outbox(tmp_path):
    store = make_db(tmp_path / "intraday-breakout-handoff.sqlite")
    intraday = {**signal(), "mode": "intraday"}
    captured = capture_paper_candidate(
        store=store,
        signal=intraday,
        payload=payload(
            cqo_entry_mode="BREAKOUT_CONTINUATION",
            paper_entry_profile="crypto_intraday_breakout_paper_v1",
            paper_execution_entry_mode="BREAKOUT_CONTINUATION",
            paper_source_entry_mode="BREAKOUT_CONTINUATION",
            entry_age_seconds=10,
        ),
        cfg=cfg(), now=datetime.now(timezone.utc),
    )
    assert captured["status"] == "REJECTED"
    assert "PAPER_EXECUTION_REVALIDATION_FAILED" in captured["reasons"]


def test_policy_rejects_shadow_or_guard_routed_swing(tmp_path):
    store = make_db(tmp_path / "t.sqlite")
    rec = evaluate_paper_candidate(
        signal=signal(),
        payload=payload(cqo_quality_action="SHADOW_ONLY", crypto_swing_main_paper_action="SHADOW_ONLY",
                        size_weight=0.0, telegram_channel="shadow_only_risk_guard"),
        cfg=cfg(), store=store,
    )
    assert rec["eligible"] == 0
    assert {"PAPER_ACTION_NOT_LIVE_ENABLED", "SWING_POLICY_ACTION_NOT_LIVE_ENABLED",
            "PAPER_SIZE_INVALID", "PAPER_NOT_ACTIONABLE"} <= set(rec["reasons"])


def test_policy_allows_only_allowlisted_half_size_breakout_experiment(tmp_path):
    store = make_db(tmp_path / "experiment.sqlite")
    rec = evaluate_paper_candidate(
        signal=signal(),
        payload=payload(cqo_entry_mode="BREAKOUT_CONTINUATION", cqo_quality_action="HALF_SIZE",
                        crypto_swing_main_paper_action="HALF_SIZE", size_weight=0.5,
                        crypto_swing_breakout_experiment_id="crypto_swing_breakout_paper_experiment_v1"),
        cfg=cfg(), store=store,
    )
    assert rec["eligible"] == 0
    assert {"ENTRY_MODE_NOT_ALLOWED", "LIVE_ROUTE_DISABLED"} <= set(rec["reasons"])


def test_policy_rejects_unallowlisted_or_oversized_breakout_experiment(tmp_path):
    store = make_db(tmp_path / "experiment-reject.sqlite")
    rec = evaluate_paper_candidate(
        signal=signal(),
        payload=payload(cqo_entry_mode="BREAKOUT_CONTINUATION", cqo_quality_action="FULL_SIZE",
                        crypto_swing_main_paper_action="FULL_SIZE", size_weight=1.0,
                        crypto_swing_breakout_experiment_id="unknown_experiment"),
        cfg=cfg(), store=store,
    )
    assert rec["eligible"] == 0
    assert {"PAPER_EXPERIMENT_NOT_LIVE_ENABLED", "PAPER_EXPERIMENT_SIZE_INVALID"} & set(rec["reasons"])


def _seed_active_canary_reservation(store: FakeStore, *, decision_id: str, signal_id: str,
                                    symbol: str, direction: str = "long") -> None:
    with store.connect() as conn:
        ls.ensure_tables(conn)
        conn.execute(
            "INSERT INTO mexc_canary_decisions "
            "(decision_id,signal_id,captured_at,paper_alert_id,symbol,mode,entry_mode,eligible,state,"
            "rejection_reasons_json,decision_json,decision_hash,config_hash,decision_context_type) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (decision_id, signal_id, "2026-07-20T00:00:00+00:00", None, symbol, "swing",
             "PULLBACK_LIMIT", 1, "QUEUED", "[]", json.dumps({"direction": direction}),
             "hash", "cfg", "point_in_time"),
        )
        conn.execute(
            "INSERT INTO mexc_canary_risk_reservations "
            "(reservation_id,decision_id,symbol,status,risk_usdt,margin_usdt,notional_usdt,created_at,updated_at) "
            "VALUES(?,?,?,?,?,?,?,?,?)",
            (f"res-{decision_id}", decision_id, symbol, "OPEN", 2.0, 5.0, 20.0,
             "2026-07-20T00:00:00+00:00", "2026-07-20T00:00:00+00:00"),
        )
        conn.commit()


def _seed_open_canary_position(
    store: FakeStore, *, decision_id: str = "open-decision",
    opened_at: str = "2026-07-17T00:00:00+00:00",
    last_reconciled_at: str | None = None,
    tpsl_order_id: str | None = None,
    tp_legs: int = 0,
    virtual_tp3: bool = False,
) -> None:
    with store.connect() as conn:
        ls.ensure_tables(conn)
        conn.execute(
            "INSERT INTO mexc_canary_decisions "
            "(decision_id,signal_id,captured_at,paper_alert_id,symbol,mode,entry_mode,eligible,state,"
            "rejection_reasons_json,decision_json,decision_hash,config_hash,decision_context_type) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (decision_id, f"sig-{decision_id}", opened_at, None, "BTC_USDT", "swing",
             "PULLBACK_LIMIT", 1, "SUBMITTED", "[]", json.dumps({"direction": "long"}),
             "hash", "cfg", "point_in_time"),
        )
        conn.execute(
            "INSERT INTO mexc_canary_orders "
            "(order_row_id,decision_id,external_oid,exchange_order_id,symbol,status,submitted_at,updated_at,"
            "plan_json,exchange_json,last_error) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (f"ord-{decision_id}", decision_id, f"entry-{decision_id}", "9001", "BTC_USDT",
             "FILLED", opened_at, opened_at, json.dumps({"direction": "long"}), "{}", None),
        )
        conn.execute(
            "INSERT INTO mexc_canary_positions "
            "(position_row_id,decision_id,exchange_position_id,symbol,direction,status,entry_price,"
            "original_stop,current_stop,tp3,volume_contracts,notional_usdt,risk_usdt,leverage,"
            "liquidation_price,highest_price,favorable_price,max_favorable_r,protection_stage,"
            "tpsl_order_id,opened_at,updated_at,last_reconciled_at,last_price_at,exchange_json) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (f"pos-{decision_id}", decision_id, "77", "BTC_USDT", "long", "OPEN",
             100.0, 98.0, 98.0, 110.0, 3.0, 300.0, 6.0, 10, 80.0, 100.0,
             100.0, 0.0, "ORIGINAL_STOP", tpsl_order_id, opened_at, opened_at,
             last_reconciled_at, last_reconciled_at, "{}"),
        )
        for idx in range(1, tp_legs + 1):
            order_kind = "VIRTUAL_TP3_MONITOR" if virtual_tp3 and idx == 3 else "CLOSE_LIMIT_TP"
            conn.execute(
                "INSERT INTO mexc_canary_exit_legs "
                "(decision_id,leg_index,exchange_tpsl_id,exchange_order_id,external_oid,order_kind,"
                "target_price,stop_price,volume_contracts,status,created_at,updated_at,exchange_json) "
                "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (decision_id, idx, None, None if order_kind == "VIRTUAL_TP3_MONITOR" else f"tp-{idx}",
                 f"tp{idx}-{decision_id}", order_kind,
                 102.0 + idx, 98.0, 1.0, "ACTIVE", opened_at, opened_at, "{}"),
            )
        conn.execute(
            "INSERT INTO mexc_canary_risk_reservations "
            "(reservation_id,decision_id,symbol,status,risk_usdt,margin_usdt,notional_usdt,created_at,updated_at) "
            "VALUES(?,?,?,?,?,?,?,?,?)",
            (f"res-{decision_id}", decision_id, "BTC_USDT", "OPEN", 6.0, 10.0, 300.0,
             opened_at, opened_at),
        )
        conn.commit()


def test_capture_is_immutable_idempotent_and_does_not_touch_paper_tables(tmp_path):
    store = make_db(tmp_path / "t.sqlite")
    before = {}
    with store.connect() as conn:
        for table in ("proposed_signals", "signal_outcomes", "paper_portfolio_ledger", "signal_alerts"):
            before[table] = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    one = capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=cfg())
    two = capture_paper_candidate(store=store, signal=signal(), payload=payload(entry_used=101), cfg=cfg())
    assert one["queued"] is True
    assert two["inserted"] is False
    with store.connect() as conn:
        assert conn.execute("SELECT COUNT(*) FROM mexc_canary_decisions").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM mexc_canary_outbox").fetchone()[0] == 1
        saved = json.loads(conn.execute("SELECT decision_json FROM mexc_canary_decisions").fetchone()[0])
        assert saved["entry_price"] == 100.0
        for table, count in before.items():
            assert conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] == count


def test_capture_blocks_mexc_untradable_symbol_before_outbox(tmp_path):
    store = make_db(tmp_path / "blocked-symbol.sqlite")
    sig = signal()
    sig["symbol"] = "LUNA/USDT"
    captured = capture_paper_candidate(
        store=store,
        signal=sig,
        payload=payload(),
        cfg=cfg(blocked_symbols=["LUNA/USDT"]),
    )
    assert captured["status"] == "REJECTED"
    assert captured["queued"] is False
    assert captured["reasons"] == ["MEXC_SYMBOL_NOT_TRADABLE"]
    with store.connect() as conn:
        assert conn.execute("SELECT COUNT(*) FROM mexc_canary_decisions").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM mexc_canary_outbox").fetchone()[0] == 0


def test_outbox_completion_updates_operational_decision_state(tmp_path):
    store = make_db(tmp_path / "outbox-state.sqlite")
    captured = capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=cfg())
    assert captured["queued"] is True
    with store.connect() as conn:
        item = ls.claim_next(conn)
        assert item is not None
        assert conn.execute(
            "SELECT state FROM mexc_canary_decisions WHERE decision_id=?", (captured["decision_id"],)
        ).fetchone()[0] == "PROCESSING"
        ls.complete_outbox(conn, str(item["outbox_id"]), "REJECTED_PREFLIGHT", error="test")
        assert conn.execute(
            "SELECT state FROM mexc_canary_decisions WHERE decision_id=?", (captured["decision_id"],)
        ).fetchone()[0] == "REJECTED_PREFLIGHT"


def test_live_watchdog_alerts_dedupes_and_recovers_stale_queue(tmp_path):
    from src.live_execution.watchdog import audit

    store = make_db(tmp_path / "watchdog-stale.sqlite")
    captured = capture_paper_candidate(
        store=store,
        signal=signal(),
        payload=payload(entry_age_seconds=10),
        cfg=cfg(),
        now=datetime(2026, 7, 17, tzinfo=timezone.utc),
    )
    notifier = FakeNotifier()
    first = audit(
        db=store.db_path,
        cfg=cfg(watchdog={"alert_cooldown_seconds": 900}),
        send_telegram=True,
        notifier=notifier,
        check_heartbeat=False,
        now=datetime(2026, 7, 17, 0, 6, tzinfo=timezone.utc),
    )
    assert first["status"] == "CRITICAL"
    assert any(issue["key"] == f"stale_outbox:{captured['decision_id']}" for issue in first["issues"])
    assert len(notifier.messages) == 1

    second = audit(
        db=store.db_path,
        cfg=cfg(watchdog={"alert_cooldown_seconds": 900}),
        send_telegram=True,
        notifier=notifier,
        check_heartbeat=False,
        now=datetime(2026, 7, 17, 0, 6, 10, tzinfo=timezone.utc),
    )
    assert second["alerts_sent"] == []
    assert len(notifier.messages) == 1

    with store.connect() as conn:
        outbox_id = conn.execute("SELECT outbox_id FROM mexc_canary_outbox").fetchone()[0]
        ls.complete_outbox(conn, outbox_id, "REJECTED_STALE_QUEUE", error="test")
    recovered = audit(
        db=store.db_path,
        cfg=cfg(watchdog={"alert_cooldown_seconds": 900}),
        send_telegram=True,
        notifier=notifier,
        check_heartbeat=False,
        now=datetime(2026, 7, 17, 0, 7, tzinfo=timezone.utc),
    )
    assert recovered["status"] == "OK"
    assert recovered["recoveries_sent"] == [f"stale_outbox:{captured['decision_id']}"]
    assert len(notifier.messages) == 2


def test_live_watchdog_retries_control_state_write_when_database_is_locked(tmp_path, monkeypatch):
    from src.live_execution import watchdog

    store = make_db(tmp_path / "watchdog-control-retry.sqlite")
    monkeypatch.setattr(watchdog.time, "sleep", lambda *_args, **_kwargs: None)

    class FlakyControlConn:
        def __init__(self, inner):
            self.inner = inner
            self.fail_once = True

        def execute(self, sql, params=()):
            if "watchdog_active_issues" in sql and self.fail_once:
                self.fail_once = False
                raise sqlite3.OperationalError("database is locked")
            return self.inner.execute(sql, params)

    with store.connect() as conn:
        ls.ensure_tables(conn)
        watchdog._store_active_issue_keys(
            FlakyControlConn(conn),
            {"stale_outbox:d1", "open_position_unprotected:d2"},
            datetime(2026, 7, 17, tzinfo=timezone.utc),
        )
        conn.commit()
        row = conn.execute(
            "SELECT control_value FROM mexc_canary_control "
            "WHERE control_key='watchdog_active_issues'"
        ).fetchone()

    assert json.loads(row[0]) == ["open_position_unprotected:d2", "stale_outbox:d1"]


def test_live_watchdog_can_mute_recovery_telegrams(tmp_path):
    from src.live_execution.watchdog import audit

    store = make_db(tmp_path / "watchdog-muted-recovery.sqlite")
    captured = capture_paper_candidate(
        store=store,
        signal=signal(),
        payload=payload(entry_age_seconds=10),
        cfg=cfg(),
        now=datetime(2026, 7, 17, tzinfo=timezone.utc),
    )
    notifier = FakeNotifier()
    audit(
        db=store.db_path,
        cfg=cfg(watchdog={"alert_cooldown_seconds": 900, "send_recovery_alerts": False}),
        send_telegram=True,
        notifier=notifier,
        check_heartbeat=False,
        now=datetime(2026, 7, 17, 0, 6, tzinfo=timezone.utc),
    )
    with store.connect() as conn:
        outbox_id = conn.execute("SELECT outbox_id FROM mexc_canary_outbox").fetchone()[0]
        ls.complete_outbox(conn, outbox_id, "REJECTED_STALE_QUEUE", error="test")
    recovered = audit(
        db=store.db_path,
        cfg=cfg(watchdog={"alert_cooldown_seconds": 900, "send_recovery_alerts": False}),
        send_telegram=True,
        notifier=notifier,
        check_heartbeat=False,
        now=datetime(2026, 7, 17, 0, 7, tzinfo=timezone.utc),
    )
    assert recovered["status"] == "OK"
    assert recovered["recoveries_sent"] == []
    assert len(notifier.messages) == 1


def test_live_watchdog_uses_persistent_alert_repeat_cooldown(tmp_path):
    from src.live_execution.watchdog import audit

    store = make_db(tmp_path / "watchdog-persistent-repeat.sqlite")
    capture_paper_candidate(
        store=store,
        signal=signal(),
        payload=payload(entry_age_seconds=10),
        cfg=cfg(),
        now=datetime(2026, 7, 17, tzinfo=timezone.utc),
    )
    notifier = FakeNotifier()
    first = audit(
        db=store.db_path,
        cfg=cfg(watchdog={
            "alert_cooldown_seconds": 60,
            "persistent_alert_repeat_seconds": 3600,
        }),
        send_telegram=True,
        notifier=notifier,
        check_heartbeat=False,
        now=datetime(2026, 7, 17, 0, 6, tzinfo=timezone.utc),
    )
    second = audit(
        db=store.db_path,
        cfg=cfg(watchdog={
            "alert_cooldown_seconds": 60,
            "persistent_alert_repeat_seconds": 3600,
        }),
        send_telegram=True,
        notifier=notifier,
        check_heartbeat=False,
        now=datetime(2026, 7, 17, 0, 30, tzinfo=timezone.utc),
    )
    assert first["alerts_sent"]
    assert second["alerts_sent"] == []
    assert len(notifier.messages) == 1


def test_live_watchdog_aggregates_and_suppresses_recent_internal_critical_events(tmp_path):
    from src.live_execution.watchdog import audit

    store = make_db(tmp_path / "watchdog-aggregated-events.sqlite")
    with store.connect() as conn:
        ls.ensure_tables(conn)
        ls.event(conn, "OPEN_POSITION_MONITOR_DEGRADED", severity="CRITICAL")
        ls.event(conn, "OPERATOR_FAILURE", decision_id="d1", severity="CRITICAL", payload={"error": "one"})
        ls.event(conn, "OPERATOR_FAILURE", decision_id="d2", severity="CRITICAL", payload={"error": "two"})
        conn.commit()
    result = audit(
        db=store.db_path,
        cfg=cfg(watchdog={
            "aggregate_recent_critical_events": True,
            "suppress_recent_event_types": ["OPEN_POSITION_MONITOR_DEGRADED"],
        }),
        send_telegram=False,
        check_heartbeat=False,
        now=datetime.now(timezone.utc),
    )
    keys = {issue["key"]: issue for issue in result["issues"]}
    assert "critical_event_type:OPEN_POSITION_MONITOR_DEGRADED" not in keys
    issue = keys["critical_event_type:OPERATOR_FAILURE"]
    assert issue["active"] is False
    assert issue["payload"]["count"] == 2
    assert set(issue["payload"]["sample_decision_ids"]) == {"d1", "d2"}


def test_live_watchdog_alerts_recent_preflight_rejection(tmp_path):
    from src.live_execution.watchdog import audit

    store = make_db(tmp_path / "watchdog-preflight-reject.sqlite")
    captured = capture_paper_candidate(
        store=store,
        signal=signal(),
        payload=payload(),
        cfg=cfg(),
        now=datetime(2026, 7, 17, tzinfo=timezone.utc),
    )
    with store.connect() as conn:
        item = ls.claim_next(conn)
        assert item is not None
        ls.complete_outbox(
            conn,
            str(item["outbox_id"]),
            "REJECTED_PREFLIGHT",
            result={"reason": "MEXC request rejected: Contract not exists"},
            error="MEXC request rejected: Contract not exists",
        )
    notifier = FakeNotifier()
    result = audit(
        db=store.db_path,
        cfg=cfg(watchdog={
            "alert_cooldown_seconds": 900,
            "alert_preflight_rejections": True,
            "preflight_rejection_lookback_minutes": 60,
        }),
        send_telegram=True,
        notifier=notifier,
        check_heartbeat=False,
        now=datetime.now(timezone.utc),
    )
    assert result["status"] == "WARNING"
    assert result["alerts_sent"] == [f"preflight_rejected:{captured['decision_id']}"]
    assert len(notifier.messages) == 1
    text = notifier.messages[0]["text"]
    assert "MEXC live preflight rejected" in text
    assert "No real order was sent" in text
    assert "Contract not exists" in text


def test_preflight_transport_degraded_is_critical_only_with_open_risk(tmp_path):
    from src.live_execution.watchdog import _preflight_transport_degraded_issue

    store = make_db(tmp_path / "watchdog-preflight-transport-severity.sqlite")
    moment = datetime.now(timezone.utc)
    live_cfg = cfg(watchdog={
        "preflight_transport_failure_lookback_seconds": 180,
        "preflight_transport_failure_threshold": 2,
    })
    with store.connect() as conn:
        ls.ensure_tables(conn)
        for _ in range(2):
            ls.event(
                conn, "ORDER_PREFLIGHT_TRANSIENT_RETRY", severity="INFO",
                payload={"reason": "MEXC transport error: ConnectTimeout"},
            )
        conn.commit()
        without_position = _preflight_transport_degraded_issue(
            conn, live_cfg, moment,
        )
        conn.execute(
            "INSERT INTO mexc_canary_positions("
            "position_row_id,decision_id,symbol,status,entry_price,original_stop,current_stop,"
            "tp3,volume_contracts,notional_usdt,risk_usdt,leverage,opened_at,updated_at,venue) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                "open-risk", "open-risk-decision", "BTC_USDT", "OPEN",
                100.0, 98.0, 98.0, 110.0, 1.0, 100.0, 5.0, 5,
                moment.isoformat(), moment.isoformat(), "mexc",
            ),
        )
        conn.commit()
        with_position = _preflight_transport_degraded_issue(conn, live_cfg, moment)

    assert without_position[0]["severity"] == "WARNING"
    assert without_position[0]["payload"]["open_positions"] == 0
    assert with_position[0]["severity"] == "CRITICAL"
    assert with_position[0]["payload"]["open_positions"] == 1


def test_fill_rebase_preserves_valid_short_targets_when_first_target_rounds_to_fill():
    plan = {
        "symbol": "MARSTOCK_USDT",
        "external_oid": "x",
        "direction": "short",
        "limit_price": 334.8,
        "original_stop": 340.07,
        "tp1": 334.79,
        "tp2": 332.67,
        "tp3": 329.49,
        "price_tick": 0.01,
        "volume_contracts": 81.0,
        "contract_size": 0.01,
        "taker_fee_rate": 0.0008,
        "slippage_rate": 0.0005,
        "actual_risk_usdt": 4.97933811,
    }

    rebased = rebase_filled_plan(plan, fill_price=337.69)

    assert rebased["tp3"] < rebased["tp2"] < rebased["tp1"] < 337.69 < rebased["original_stop"]
    assert rebased["tp1"] == pytest.approx(337.68)
    assert rebased["fill_rebase_min_target_gap_applied"] is True
    assert rebased["actual_risk_usdt"] <= 4.97933811 + 0.05


def test_live_watchdog_detects_open_position_without_verified_stop_and_three_tps(tmp_path):
    from src.live_execution.watchdog import audit

    store = make_db(tmp_path / "watchdog-unprotected.sqlite")
    _seed_open_canary_position(store)
    result = audit(
        db=store.db_path,
        cfg=cfg(watchdog={"alert_cooldown_seconds": 900}),
        send_telegram=False,
        check_heartbeat=False,
        now=datetime(2026, 7, 17, 0, 2, tzinfo=timezone.utc),
    )
    keys = {issue["key"] for issue in result["issues"]}
    assert result["status"] == "CRITICAL"
    assert "position_tp_legs_incomplete:open-decision" in keys
    assert "position_stop_missing:open-decision" in keys
    assert "position_reconcile_stale:open-decision" in keys


def test_live_watchdog_accepts_recently_reconciled_protected_position(tmp_path):
    from src.live_execution.watchdog import audit

    store = make_db(tmp_path / "watchdog-protected.sqlite")
    _seed_open_canary_position(
        store,
        last_reconciled_at="2026-07-17T00:01:55+00:00",
        tpsl_order_id="88",
        tp_legs=3,
    )
    result = audit(
        db=store.db_path,
        cfg=cfg(watchdog={"alert_cooldown_seconds": 900}),
        send_telegram=False,
        check_heartbeat=False,
        now=datetime(2026, 7, 17, 0, 2, tzinfo=timezone.utc),
    )
    assert result["status"] == "OK"
    assert result["issues"] == []


def test_live_watchdog_accepts_two_native_tps_and_monitored_tp3(tmp_path):
    from src.live_execution.watchdog import audit

    store = make_db(tmp_path / "watchdog-virtual-tp3.sqlite")
    _seed_open_canary_position(
        store,
        last_reconciled_at="2026-07-17T00:01:55+00:00",
        tpsl_order_id="88",
        tp_legs=3,
        virtual_tp3=True,
    )
    result = audit(
        db=store.db_path,
        cfg=cfg(watchdog={"alert_cooldown_seconds": 900}),
        send_telegram=False,
        check_heartbeat=False,
        now=datetime(2026, 7, 17, 0, 2, tzinfo=timezone.utc),
    )
    assert result["status"] == "OK"


def test_cost_aware_contract_sizing_and_liquidation_buffer():
    decision = json.loads(evaluate_record_decision_json())
    decision["decision_id"] = "11111111-2222-3333-4444-555555555555"
    plan = build_order_plan(decision=decision, contract=contract(), depth=depth(), cfg=cfg())
    assert plan.actual_risk_usdt <= 10.0
    assert plan.volume_contracts >= 1
    assert plan.leverage <= 50
    assert plan.liquidation_distance_multiple >= 3.0
    assert plan.maker_fee_rate == 0.0006
    assert plan.taker_fee_rate == 0.0008
    assert plan.order_type == 3
    assert plan.mexc_order()["stopLossPrice"] == 98.0


def test_unset_operator_leverage_ceiling_uses_maximum_safe_contract_leverage():
    """Margin is minimized without allowing liquidation to approach the stop."""
    decision = json.loads(evaluate_record_decision_json())
    decision.update(
        decision_id="max-safe-leverage", entry_mode="TEST_MAX_SAFE",
        original_stop=99.9,
        # This sizing-only synthetic mode uses the default 15 bps IOC cap.
        # Targets remain above that worst permitted long entry.
        tp1=101.0, tp2=102.0, tp3=103.0,
    )
    plan = build_order_plan(
        decision=decision,
        contract=contract(),
        depth=depth(),
        cfg=cfg(
            exchange_leverage_ceiling=None,
            min_stop_distance_pct=0.0005,
            min_live_entry_to_stop_buffer_pct=0.0005,
        ),
    )
    assert plan.leverage > 50
    assert plan.leverage <= 200
    assert plan.liquidation_distance_multiple >= 3.0


def test_actual_fill_risk_uses_fill_price_and_mexc_contract_multiplier():
    """A favourable IOC fill must not retain the worst-case IOC risk locally."""
    detail = stop_risk_components(
        entry_price=1907.04,
        stop_price=1897.48,
        volume_contracts=34,
        contract_size=0.01,
        taker_fee_rate=0.0008,
        slippage_rate=0.0005,
    )
    # This is the price-only loss MEXC displays in its TP/SL form.
    assert detail["gross_stop_loss_usdt"] == pytest.approx(3.2504)
    # The risk reservation is intentionally more conservative: it includes
    # both legs' fees and bounded slippage, but never the stale IOC cap.
    assert detail["net_stop_risk_usdt"] == pytest.approx(4.932, abs=0.01)


def test_open_position_risk_repair_uses_actual_fill_without_touching_exchange(tmp_path):
    store = make_db(tmp_path / "risk-repair.sqlite")
    _seed_open_canary_position(store, decision_id="eth-fill")
    plan = {
        "contract_size": 0.01, "taker_fee_rate": 0.0008,
        "slippage_rate": 0.0005,
    }
    with store.connect() as conn:
        conn.execute(
            "UPDATE mexc_canary_orders SET plan_json=? WHERE decision_id='eth-fill'",
            (json.dumps(plan),),
        )
        conn.execute(
            "UPDATE mexc_canary_positions SET entry_price=?,original_stop=?,volume_contracts=?,risk_usdt=? "
            "WHERE decision_id='eth-fill'",
            (1907.04, 1897.48, 34.0, 9.73784741),
        )
        conn.execute(
            "UPDATE mexc_canary_risk_reservations SET risk_usdt=? WHERE decision_id='eth-fill'",
            (9.73784741,),
        )
        conn.commit()

    result = recalculate_open_position_risk_accounting(db=store.db_path)

    assert result == {"status": "OK", "checked": 1, "corrected": 1, "skipped": []}
    with store.connect() as conn:
        position_risk = conn.execute(
            "SELECT risk_usdt FROM mexc_canary_positions WHERE decision_id='eth-fill'"
        ).fetchone()[0]
        reservation_risk = conn.execute(
            "SELECT risk_usdt FROM mexc_canary_risk_reservations WHERE decision_id='eth-fill'"
        ).fetchone()[0]
        event = json.loads(conn.execute(
            "SELECT payload_json FROM mexc_canary_events "
            "WHERE decision_id='eth-fill' AND event_type='OPEN_POSITION_RISK_ACCOUNTING_CORRECTED'"
        ).fetchone()[0])
    assert position_risk == pytest.approx(4.932, abs=0.01)
    assert reservation_risk == pytest.approx(position_risk)
    assert event["gross_stop_loss_usdt"] == pytest.approx(3.2504)


def evaluate_record_decision_json() -> str:
    return json.dumps({
        "signal_id": "sig-live-1", "symbol": "BTC/USDT", "entry_mode": "PULLBACK_LIMIT",
        "entry_price": 100.0, "original_stop": 98.0,
        "tp1": 103.0, "tp2": 106.0, "tp3": 110.0,
    })


def test_entry_drift_and_nonstandard_contract_fail_closed():
    decision = json.loads(evaluate_record_decision_json())
    decision["decision_id"] = "d"
    # Keep the synthetic BTC book inside the tighter major spread cap so this
    # test reaches the distinct adverse-entry-drift gate.
    with pytest.raises(PlanRejected, match="ENTRY_DRIFT_TOO_LARGE"):
        build_order_plan(decision=decision, contract=contract(), depth=depth(101, 100.96), cfg=cfg())
    bad = contract()
    bad["preMarket"] = True
    with pytest.raises(PlanRejected, match="NOT_STANDARD"):
        build_order_plan(decision=decision, contract=bad, depth=depth(), cfg=cfg())


def test_live_spread_caps_match_major_alt_policy_and_expose_diagnostics():
    decision = json.loads(evaluate_record_decision_json())
    decision["decision_id"] = "d"
    # BTC stays on the tighter major cap (8 bps in the production config).
    with pytest.raises(PlanRejected) as major_exc:
        build_order_plan(decision=decision, contract=contract(), depth=depth(100.10, 100.0), cfg=cfg())
    assert str(major_exc.value) == "SPREAD_TOO_WIDE"
    assert major_exc.value.details["spread_cap_bps"] == 8.0
    assert major_exc.value.details["spread_bps"] > 8.0

    # The same 10-bps book is valid for an alt, matching the Paper overlay's 20-bps cap.
    decision["symbol"] = "GIGGLE/USDT"
    plan = build_order_plan(decision=decision, contract=contract(), depth=depth(100.10, 100.0), cfg=cfg())
    assert plan.spread_bps > 8.0 and plan.spread_bps < 20.0


def test_crypto_invest_can_express_ten_usdt_risk_with_tight_stop():
    decision = json.loads(evaluate_record_decision_json())
    decision.update({
        "decision_id": "invest-tight-stop", "mode": "invest",
        "entry_mode": "REGIME_RECLAIM", "risk_bucket": "crypto_invest",
        "entry_price": 100.0, "original_stop": 99.5,
        "tp1": 100.65, "tp2": 101.15, "tp3": 101.8,
    })
    plan = build_order_plan(
        decision=decision, contract=contract(), depth=depth(100.0, 99.99), cfg=cfg()
    )
    assert plan.notional_usdt > 500.0
    assert 9.5 <= plan.actual_risk_usdt <= 10.0
    assert plan.risk_budget_usdt == 10.0


def test_pump_alias_is_used_at_mexc_boundary_without_changing_canonical_signal(tmp_path):
    store = make_db(tmp_path / "pump-alias.sqlite")
    pump_signal = signal()
    pump_signal["symbol"] = "PUMP/USDT"
    pump_payload = payload(
        entry_used=0.002238, stop=0.002197,
        tp1=0.002305, tp2=0.002348, tp3=0.002405,
        cqo_entry_mode="BREAKOUT_CONTINUATION",
    )
    live_cfg = cfg()
    assert live_cfg.exchange_symbol("PUMP/USDT") == "PUMPFUN_USDT"
    captured = capture_paper_candidate(
        store=store, signal=pump_signal, payload=pump_payload, cfg=live_cfg,
        now=datetime.now(timezone.utc),
    )
    assert captured["queued"] is True
    client = PumpAliasPublicClient()
    result = worker_once(db=store.db_path, cfg=live_cfg, client=client)
    assert result["status"] == "DRY_RUN_PLANNED"
    assert result["plan"]["symbol"] == "PUMPFUN_USDT"
    assert client.symbols == [
        ("contract", "PUMPFUN_USDT"), ("depth", "PUMPFUN_USDT")
    ]


def test_contract_preflight_reports_closed_and_api_disabled_separately():
    decision = json.loads(evaluate_record_decision_json())
    decision["decision_id"] = "d"
    closed = contract()
    closed.update({"symbol": "OLD_USDT", "state": 3})
    with pytest.raises(PlanRejected, match="CONTRACT_STATE_NOT_OPEN") as closed_exc:
        build_order_plan(decision=decision, contract=closed, depth=depth(), cfg=cfg())
    assert closed_exc.value.details == {"native_symbol": "OLD_USDT", "contract_state": 3}

    api_disabled = contract()
    api_disabled.update({"symbol": "NOAPI_USDT", "apiAllowed": False})
    with pytest.raises(PlanRejected, match="CONTRACT_API_DISABLED") as api_exc:
        build_order_plan(decision=decision, contract=api_disabled, depth=depth(), cfg=cfg())
    assert api_exc.value.details == {"native_symbol": "NOAPI_USDT", "api_allowed": False}


def test_risk_reservation_blocks_third_two_percent_trade(tmp_path):
    conn = ls.connect(tmp_path / "t.sqlite")
    ls.ensure_tables(conn)
    for i in range(2):
        r = ls.reserve_risk(conn, decision_id=f"d{i}", symbol="BTC_USDT", risk_usdt=2.0,
                            margin_usdt=5.0, notional_usdt=80.0, max_risk_usdt=5.0,
                            max_margin_usdt=50.0, max_notional_usdt=500.0)
        assert r["ok"] is True
    third = ls.reserve_risk(conn, decision_id="d2", symbol="ETH_USDT", risk_usdt=2.0,
                            margin_usdt=5.0, notional_usdt=80.0, max_risk_usdt=5.0,
                            max_margin_usdt=50.0, max_notional_usdt=500.0)
    assert third == {"ok": False, "reason": "max_concurrent_risk", "active_risk_usdt": 4.0}
    conn.close()


def test_ten_percent_portfolio_cap_allows_five_two_percent_slots_and_blocks_sixth(tmp_path):
    conn = ls.connect(tmp_path / "t.sqlite")
    ls.ensure_tables(conn)
    for i in range(5):
        r = ls.reserve_risk(conn, decision_id=f"slot-{i}", symbol=f"S{i}_USDT",
                            risk_usdt=2.0, margin_usdt=5.0, notional_usdt=80.0,
                            max_risk_usdt=10.0, max_margin_usdt=50.0,
                            max_notional_usdt=500.0)
        assert r["ok"] is True
    blocked = ls.reserve_risk(conn, decision_id="slot-5", symbol="S5_USDT",
                              risk_usdt=2.0, margin_usdt=5.0, notional_usdt=80.0,
                              max_risk_usdt=10.0, max_margin_usdt=50.0,
                              max_notional_usdt=500.0)
    assert blocked == {"ok": False, "reason": "max_concurrent_risk", "active_risk_usdt": 10.0}
    conn.close()


def test_unlimited_notional_still_enforces_risk_and_margin_caps(tmp_path):
    conn = ls.connect(tmp_path / "t.sqlite")
    ls.ensure_tables(conn)
    first = ls.reserve_risk(
        conn, decision_id="wide", symbol="ETH_USDT", risk_usdt=7.5,
        margin_usdt=21.7, notional_usdt=499.2, max_risk_usdt=50.0,
        max_margin_usdt=50.0, max_notional_usdt=None,
    )
    assert first["ok"] is True
    margin_blocked = ls.reserve_risk(
        conn, decision_id="margin", symbol="BTC_USDT", risk_usdt=7.5,
        margin_usdt=29.0, notional_usdt=900.0, max_risk_usdt=50.0,
        max_margin_usdt=50.0, max_notional_usdt=None,
    )
    assert margin_blocked["reason"] == "max_total_margin"
    conn.close()


def test_unlimited_margin_relies_on_risk_cap_not_a_duplicate_local_margin_cap(tmp_path):
    conn = ls.connect(tmp_path / "unlimited-margin.sqlite")
    ls.ensure_tables(conn)
    result = ls.reserve_risk(
        conn, decision_id="wide", symbol="ETH_USDT", risk_usdt=5.0,
        margin_usdt=500.0, notional_usdt=1_000.0, max_risk_usdt=10.0,
        max_margin_usdt=None, max_notional_usdt=None,
    )
    assert result["ok"] is True
    blocked = ls.reserve_risk(
        conn, decision_id="risk-cap", symbol="BTC_USDT", risk_usdt=6.0,
        margin_usdt=1.0, notional_usdt=1.0, max_risk_usdt=10.0,
        max_margin_usdt=None, max_notional_usdt=None,
    )
    assert blocked["reason"] == "max_concurrent_risk"
    conn.close()


def test_transactional_reservation_enforces_same_symbol_cap(tmp_path):
    same_store = make_db(tmp_path / "same.sqlite")
    _seed_active_canary_reservation(same_store, decision_id="active-btc", signal_id="active-btc-s",
                                    symbol="BTC/USDT")
    with same_store.connect() as conn:
        same = ls.reserve_risk(
            conn, decision_id="next-btc", symbol="BTC_USDT", risk_usdt=2.0,
            margin_usdt=5.0, notional_usdt=20.0, max_risk_usdt=10.0,
            max_margin_usdt=50.0, max_notional_usdt=500.0, max_open_same_symbol=1,
        )
    assert same == {"ok": False, "reason": "max_open_same_symbol", "active_risk_usdt": 2.0}


def test_operator_probe_accepts_queries_and_cancels_minimum_order(tmp_path, monkeypatch):
    monkeypatch.setenv("MEXC_CANARY_ACCESS_KEY", "dummy-access")
    monkeypatch.setenv("MEXC_CANARY_SECRET", "dummy-secret")
    monkeypatch.setenv("MEXC_LIVE_CANARY_ARMED", "I_UNDERSTAND_REAL_MEXC_ORDERS")
    live_cfg = cfg(submission_enabled=True, execution_mode="live")
    fake = FakePrivateClient()
    result = operator_order_probe(execute=True, db=tmp_path / "probe.sqlite",
                                  cfg=live_cfg, client=fake)
    assert result["status"] == "PASSED_CANCELED_UNFILLED"
    assert result["order_accepted"] is True
    assert result["cancel_response_ok"] is True
    assert result["terminal_state"] == 4
    assert result["deal_volume"] == 0
    assert fake.created[-1]["type"] == 2
    assert fake.created[-1]["openType"] == 1
    assert fake.created[-1]["positionMode"] == 1
    assert fake.created[-1]["leverage"] == 1
    with ls.connect(tmp_path / "probe.sqlite") as conn:
        assert ls.kill_switch_state(conn) == "CLEAR"


def test_worker_dry_run_uses_public_data_only(tmp_path):
    store = make_db(tmp_path / "t.sqlite")
    captured = capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=cfg())
    fake = FakePublicClient()
    result = worker_once(db=store.db_path, cfg=cfg(), client=fake)
    assert captured["queued"] is True
    assert result["status"] == "DRY_RUN_PLANNED"
    assert fake.create_calls == 0
    with store.connect() as conn:
        assert conn.execute("SELECT status FROM mexc_canary_outbox").fetchone()[0] == "DRY_RUN_PLANNED"
        assert conn.execute("SELECT status FROM mexc_canary_orders").fetchone()[0] == "DRY_RUN_PLANNED"
        assert conn.execute("SELECT COUNT(*) FROM mexc_canary_risk_reservations").fetchone()[0] == 0
        parity = conn.execute(
            "SELECT source,clean,evidence_class,validation_json,plan_json "
            "FROM mexc_canary_parity_plans"
        ).fetchone()
        validation = json.loads(parity["validation_json"])
        plan = json.loads(parity["plan_json"])
        assert tuple(parity[:3]) == ("mexc_preflight_v2", 1, "forward_post_activation")
        assert validation["clean"] is True
        assert validation["contract"]["symbol"] == "BTC_USDT"
        assert len(validation["legs"]) == 3
        assert sum(leg["volume_contracts"] for leg in validation["legs"]) == plan["volume_contracts"]


def test_worker_rejects_when_authoritative_paper_outcome_is_no_entry(tmp_path):
    store = make_db(tmp_path / "paper-revalidation-no-entry.sqlite")
    captured = capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=cfg())
    with store.connect() as conn:
        conn.execute(
            "UPDATE paper_execution_outcomes SET lifecycle_state='NO_ENTRY',close_reason='no_entry' "
            "WHERE signal_id='sig-live-1'"
        )
        conn.commit()

    result = worker_once(db=store.db_path, cfg=cfg(), client=FakePublicClient())

    assert captured["queued"] is True
    assert result["status"] == "REJECTED_PAPER_EXECUTION_REVALIDATION"
    assert result["reason"] == "PAPER_EXECUTION_NOT_OPEN"
    assert result["paper_lifecycle_state"] == "NO_ENTRY"
    with store.connect() as conn:
        assert conn.execute("SELECT status FROM mexc_canary_outbox").fetchone()[0] == (
            "REJECTED_PAPER_EXECUTION_REVALIDATION"
        )
        assert conn.execute("SELECT COUNT(*) FROM mexc_canary_orders").fetchone()[0] == 0


def test_capture_rejects_when_authoritative_paper_outcome_is_no_entry(tmp_path):
    store = make_db(tmp_path / "paper-capture-revalidation-no-entry.sqlite")
    with store.connect() as conn:
        conn.execute(
            "UPDATE paper_execution_outcomes SET lifecycle_state='NO_ENTRY',close_reason='no_entry' "
            "WHERE signal_id='sig-live-1'"
        )
        conn.commit()

    captured = capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=cfg())

    assert captured["queued"] is False
    assert captured["status"] == "REJECTED"
    assert "PAPER_EXECUTION_REVALIDATION_FAILED" in captured["reasons"]
    assert "PAPER_EXECUTION_NOT_OPEN" in captured["reasons"]
    with store.connect() as conn:
        decision = conn.execute(
            "SELECT eligible,state,rejection_reasons_json,decision_json FROM mexc_canary_decisions"
        ).fetchone()
        assert decision["eligible"] == 0
        assert decision["state"] == "REJECTED"
        assert conn.execute("SELECT COUNT(*) FROM mexc_canary_outbox").fetchone()[0] == 0
        frozen = json.loads(decision["decision_json"])
        assert frozen["live_capture_contract_ok"] is False
        assert frozen["live_capture_contract_validation"]["reason"] == "PAPER_EXECUTION_NOT_OPEN"


def test_worker_retries_transient_wide_spread_within_frozen_entry_age(tmp_path):
    store = make_db(tmp_path / "spread-retry.sqlite")
    capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=cfg())
    result = worker_once(db=store.db_path, cfg=cfg(), client=WideSpreadPublicClient())
    assert result["status"] == "RETRY_SPREAD"
    assert result["reason"] == "SPREAD_TOO_WIDE"
    assert result["spread_bps"] > result["spread_cap_bps"]
    with store.connect() as conn:
        row = conn.execute("SELECT status,attempt_count,last_error,result_json FROM mexc_canary_outbox").fetchone()
        assert row["status"] == "QUEUED"
        assert row["attempt_count"] == 1
        assert row["last_error"] == "SPREAD_TOO_WIDE"
        assert json.loads(row["result_json"])["retry_in_seconds"] == 3.0


def test_worker_retries_transient_mexc_preflight_rate_limit_within_entry_age(tmp_path):
    store = make_db(tmp_path / "rate-limit-retry.sqlite")
    retry_cfg = cfg(
        transient_preflight_retry_interval_seconds=0,
        max_transient_preflight_retry_attempts=3,
    )
    capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=retry_cfg)
    result = worker_once(db=store.db_path, cfg=retry_cfg, client=RateLimitedPublicClient())
    assert result["status"] == "RETRY_TRANSIENT_PREFLIGHT"
    assert "Requests are too frequent" in result["reason"]
    with store.connect() as conn:
        row = conn.execute("SELECT status,attempt_count,last_error,result_json FROM mexc_canary_outbox").fetchone()
        assert row["status"] == "QUEUED"
        assert row["attempt_count"] == 1
        assert "Requests are too frequent" in row["last_error"]
        assert json.loads(row["result_json"])["retry_in_seconds"] == 0.0


def test_worker_retries_when_every_live_venue_has_a_temporary_preflight_failure(tmp_path, monkeypatch):
    class MexcUnavailable:
        def contract_info(self, _symbol):
            raise MexcAPIError("MEXC transport error: ConnectTimeout")

    class BybitTimestampWindowRejected:
        def contract_info(self, _symbol):
            raise BybitAPIError(
                "Bybit request rejected: invalid request, please check your server timestamp or recv_window param",
                code=10002, status_code=200,
            )

    for name, value in {
        "MEXC_CANARY_ACCESS_KEY": "mexc-key",
        "MEXC_CANARY_SECRET": "mexc-secret",
        "MEXC_LIVE_CANARY_ARMED": "I_UNDERSTAND_REAL_MEXC_ORDERS",
        "BYBIT_LIVE_ACCESS_KEY": "bybit-key",
        "BYBIT_LIVE_SECRET": "bybit-secret",
        "BYBIT_LIVE_ARMED": "I_UNDERSTAND_REAL_BYBIT_ORDERS",
    }.items():
        monkeypatch.setenv(name, value)
    store = make_db(tmp_path / "multi-venue-transient-retry.sqlite")
    retry_cfg = cfg(
        submission_enabled=True,
        execution_mode="live",
        transient_preflight_retry_interval_seconds=0,
        max_transient_preflight_retry_attempts=3,
    )
    capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=retry_cfg)

    result = worker_once(
        db=store.db_path, cfg=retry_cfg,
        client=MexcUnavailable(), bybit_execution_client=BybitTimestampWindowRejected(),
    )

    assert result["status"] == "RETRY_TRANSIENT_PREFLIGHT"
    assert result["reason"] == "NO_ELIGIBLE_EXECUTION_VENUE"
    assert result["retry_scope"] == "multi_venue_preflight"
    with store.connect() as conn:
        row = conn.execute(
            "SELECT status,attempt_count,last_error,result_json FROM mexc_canary_outbox"
        ).fetchone()
        assert row["status"] == "QUEUED"
        assert row["attempt_count"] == 1
        assert row["last_error"] == "NO_ELIGIBLE_EXECUTION_VENUE"
        diagnostic = json.loads(row["result_json"])
        assert diagnostic["venues"]["mexc"]["reason"] == "MEXC transport error: ConnectTimeout"
        assert diagnostic["venues"]["bybit"]["exchange_code"] == "10002"
        assert conn.execute(
            "SELECT COUNT(*) FROM mexc_canary_notification_outbox"
        ).fetchone()[0] == 0


def test_monitor_drains_two_queued_candidates_without_head_of_line_blocking(tmp_path, monkeypatch):
    """A stalled preflight must not consume the only live-worker slot."""
    store = make_db(tmp_path / "parallel-preflight.sqlite")
    second = signal()
    second["signal_id"] = "sig-live-2"
    with store.connect() as conn:
        conn.execute("INSERT INTO entry_latency_audit VALUES('sig-live-2','OK',0)")
        conn.execute(
            "INSERT INTO paper_execution_outcomes VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                "sig-live-2", "2026-07-17T00:00:01+00:00", "OPEN", "valid",
                "2026-07-17T00:00:01+00:00", 100.0, 98.0,
                "point_in_time_current_bar", 1,
                "crypto_swing_paper_t130_v1", "LIMIT_THEN_TAKER_TIMEOUT", None,
            ),
        )
        conn.commit()
    assert capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=cfg())["queued"]
    second_payload = payload()
    second_payload["economic_trade_key"] = "test-distinct-economic-trade"
    assert capture_paper_candidate(
        store=store, signal=second, payload=second_payload, cfg=cfg()
    )["queued"]
    calls: list[str] = []

    def isolated_worker(*, db, **_kwargs):
        calls.append(str(db))
        return {"status": "RETRY_TRANSIENT_PREFLIGHT"}

    monkeypatch.setattr("src.live_execution.service.worker_once", isolated_worker)
    result = monitor_tick(
        db=store.db_path,
        cfg=cfg(preflight_parallel_workers=2, preflight_batch_size=2),
    )
    assert result["worker"]["status"] == "BATCH"
    assert result["worker"]["parallel_workers"] == 2
    assert len(calls) == 2


def test_monitor_drains_bounded_follow_up_batch_in_same_tick(tmp_path, monkeypatch):
    """The third queued entry must not wait for another full monitor cycle."""
    store = make_db(tmp_path / "burst-preflight.sqlite")
    calls: list[bool] = []
    queue_counts = iter((3, 3, 1))

    def isolated_worker(*, reconcile_after_submission=True, **_kwargs):
        calls.append(bool(reconcile_after_submission))
        return {"status": "SUBMITTED"}

    monkeypatch.setattr("src.live_execution.service.worker_once", isolated_worker)
    monkeypatch.setattr(
        "src.live_execution.service._queued_outbox_count",
        lambda _path: next(queue_counts),
    )
    result = monitor_tick(
        db=store.db_path,
        cfg=cfg(
            preflight_parallel_workers=2,
            preflight_batch_size=2,
            preflight_max_batches_per_tick=2,
        ),
    )
    assert result["worker"]["status"] == "BATCH"
    assert result["worker"]["batches_processed"] == 2
    assert len(calls) == 3
    assert calls == [False, False, True]


def test_swing_preflight_recovers_small_adverse_drift_with_same_r_geometry(tmp_path):
    store = make_db(tmp_path / "swing-recovery.sqlite")
    recovery_cfg = cfg(swing_live_recovery={
        "enabled": True,
        "entry_modes": ["LIMIT_THEN_TAKER_TIMEOUT"],
        "max_adverse_drift_bps": {"LIMIT_THEN_TAKER_TIMEOUT": 150},
    })
    assert capture_paper_candidate(
        store=store,
        signal=signal(),
        payload=payload(cqo_entry_mode="LIMIT_THEN_TAKER_TIMEOUT"),
        cfg=recovery_cfg,
    )["queued"]
    result = worker_once(
        db=store.db_path,
        cfg=recovery_cfg,
        client=FakePublicClient(ask=101.0, bid=100.95),
    )
    assert result["status"] == "DRY_RUN_PLANNED"
    plan = result["plan"]
    assert plan["live_recovery_reprice"]["reference_entry"] == 100.0
    assert plan["live_recovery_reprice"]["current_entry"] == 101.0
    assert plan["original_stop"] < plan["limit_price"] < plan["tp1"] < plan["tp2"] < plan["tp3"]


def test_stock_preflight_recovers_three_distinct_targets_on_coarse_tick() -> None:
    decision = {
        "asset_class": "stock_futures", "mode": "stock_intraday",
        "direction": "long", "entry_mode": "BREAKOUT_CONTINUATION",
        "entry_price": 100.0, "original_stop": 98.0,
        "tp1": 103.0, "tp2": 106.0, "tp3": 110.0,
    }
    recovered, detail = _maybe_reprice_swing_recovery(
        decision=decision,
        contract={"priceUnit": 2.0},
        depth={"asks": [[101.0, 10.0]], "bids": [[100.0, 10.0]]},
        cfg=cfg(stock_intraday_live_recovery={
            "enabled": True,
            "entry_modes": ["BREAKOUT_CONTINUATION"],
            "max_adverse_drift_bps": {"BREAKOUT_CONTINUATION": 150},
        }),
    )
    assert detail is not None
    assert detail["reason"] == "stock_intraday_exchange_tick_reprice"
    assert recovered["original_stop"] < recovered["entry_price"] < recovered["tp1"] < recovered["tp2"] < recovered["tp3"]


def test_worker_returns_retry_status_when_claim_database_is_locked(tmp_path, monkeypatch):
    store = make_db(tmp_path / "t.sqlite")
    with ls.connect(store.db_path) as conn:
        ls.ensure_tables(conn)

    real_connect = ls.connect

    def fast_connect(path):
        conn = sqlite3.connect(path, timeout=0.01)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA busy_timeout=1")
        return conn

    lock = sqlite3.connect(store.db_path, timeout=1)
    lock.execute("BEGIN IMMEDIATE")
    monkeypatch.setattr(ls, "connect", fast_connect)
    try:
        result = worker_once(db=store.db_path, cfg=cfg(), client=FakePublicClient())
    finally:
        lock.rollback()
        lock.close()
        monkeypatch.setattr(ls, "connect", real_connect)

    assert result == {"status": "RETRY_DB_BUSY", "stage": "claim"}


def test_monitor_tick_keeps_running_when_worker_raises_database_locked(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "src.live_execution.service.worker_once",
        lambda **_kwargs: (_ for _ in ()).throw(sqlite3.OperationalError("database is locked")),
    )
    db = tmp_path / "monitor.sqlite"
    result = monitor_tick(db=db, cfg=cfg())
    with ls.connect(db) as conn:
        heartbeat = ls.monitor_heartbeat(conn)
    assert result["worker"] == {"status": "RETRY_DB_BUSY", "error_type": "OperationalError"}
    assert result["reconcile"]["status"] == "BLOCKED_NOT_ARMED"
    assert result["heartbeat"]["status"] == "OK"
    assert heartbeat["status"] == "BLOCKED_NOT_ARMED"


def test_monitor_tick_reuses_the_supplied_private_reconciliation_client(monkeypatch, tmp_path):
    monkeypatch.setenv("MEXC_CANARY_ACCESS_KEY", "dummy-access")
    monkeypatch.setenv("MEXC_CANARY_SECRET", "dummy-secret")
    monkeypatch.setenv("MEXC_LIVE_CANARY_ARMED", "I_UNDERSTAND_REAL_MEXC_ORDERS")
    seen: list[object] = []
    client = object()

    def fake_reconcile(**kwargs):
        seen.append(kwargs.get("client"))
        return {"status": "OK", "errors": []}

    monkeypatch.setattr("src.live_execution.service.reconcile_once", fake_reconcile)
    result = monitor_tick(
        db=tmp_path / "persistent-client.sqlite",
        cfg=cfg(submission_enabled=True, execution_mode="live"),
        reconciliation_client=client,
    )

    assert result["reconcile"]["status"] == "OK"
    assert seen == [client]


def test_monitor_tick_reuses_the_supplied_execution_client(monkeypatch, tmp_path):
    seen: list[object] = []
    client = object()

    def fake_worker(**kwargs):
        seen.append(kwargs.get("client"))
        return {"status": "IDLE"}

    monkeypatch.setattr("src.live_execution.service.worker_once", fake_worker)
    result = monitor_tick(
        db=tmp_path / "persistent-execution-client.sqlite",
        cfg=cfg(),
        execution_client=client,
    )

    assert result["worker"]["status"] == "IDLE"
    assert seen == [client]


def test_monitor_tick_writes_start_heartbeat_before_worker(monkeypatch, tmp_path):
    observed = {}

    def worker_observes_heartbeat(*, db, **_kwargs):
        with ls.connect(db) as conn:
            observed["heartbeat"] = ls.monitor_heartbeat(conn)
        return {"status": "IDLE"}

    monkeypatch.setattr("src.live_execution.service.worker_once", worker_observes_heartbeat)
    db = tmp_path / "monitor-start-heartbeat.sqlite"

    result = monitor_tick(db=db, cfg=cfg())

    assert result["start_heartbeat"]["status"] == "OK"
    assert observed["heartbeat"]["status"] == "OK"
    assert observed["heartbeat"]["detail"]["worker"] == "TICK_RUNNING"
    assert observed["heartbeat"]["detail"]["reconcile"] == "PENDING"


def test_monitor_tick_reuses_worker_submit_protection_without_second_reconcile(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "src.live_execution.service.worker_once",
        lambda **_kwargs: {
            "status": "SUBMITTED",
            "decision_id": "d1",
            "protection": {"status": "OK", "orders_checked": 1, "positions_checked": 1},
        },
    )
    calls = {"reconcile": 0}

    def reconcile_should_not_run(**_kwargs):
        calls["reconcile"] += 1
        raise AssertionError("monitor must not immediately repeat worker submit protection")

    monkeypatch.setattr("src.live_execution.service.reconcile_once", reconcile_should_not_run)
    db = tmp_path / "monitor-reuse.sqlite"

    result = monitor_tick(db=db, cfg=cfg())

    assert result["reconcile"]["status"] == "OK"
    assert result["reconcile"]["source"] == "worker_submit_protection"
    assert calls["reconcile"] == 0


def test_control_lease_blocks_concurrent_position_reconcile(tmp_path):
    db = tmp_path / "lease.sqlite"
    with ls.connect(db) as conn:
        ls.ensure_tables(conn)
        assert ls.try_claim_control_lease(
            conn, key="position_reconcile:d1", owner="owner-a", ttl_seconds=60
        )
        assert not ls.try_claim_control_lease(
            conn, key="position_reconcile:d1", owner="owner-b", ttl_seconds=60
        )
        ls.release_control_lease(conn, key="position_reconcile:d1", owner="owner-b")
        assert not ls.try_claim_control_lease(
            conn, key="position_reconcile:d1", owner="owner-b", ttl_seconds=60
        )
        ls.release_control_lease(conn, key="position_reconcile:d1", owner="owner-a")
        assert ls.try_claim_control_lease(
            conn, key="position_reconcile:d1", owner="owner-b", ttl_seconds=60
        )


def test_ensure_tables_is_read_only_after_bootstrap(tmp_path):
    path = tmp_path / "t.sqlite"
    with ls.connect(path) as conn:
        ls.ensure_tables(conn)
        statements: list[str] = []
        conn.set_trace_callback(statements.append)
        ls.ensure_tables(conn)
    assert statements == ["PRAGMA database_list"]


def test_ensure_tables_first_call_in_new_process_is_read_only_when_schema_is_current(tmp_path):
    path = tmp_path / "current.sqlite"
    with ls.connect(path) as conn:
        ls.ensure_tables(conn)
    ls._INITIALIZED_DATABASES.clear()
    with ls.connect(path) as conn:
        statements: list[str] = []
        conn.set_trace_callback(statements.append)
        ls.ensure_tables(conn)
    assert statements
    assert not any(
        statement.lstrip().upper().startswith(("CREATE", "ALTER", "INSERT", "UPDATE", "DELETE"))
        for statement in statements
    )


def test_ensure_tables_migrates_old_position_schema_without_rebuilding_rows(tmp_path):
    path = tmp_path / "old.sqlite"
    with sqlite3.connect(path) as conn:
        conn.executescript("""
            CREATE TABLE mexc_canary_control (
              control_key TEXT PRIMARY KEY, control_value TEXT NOT NULL, updated_at TEXT NOT NULL
            );
            CREATE TABLE mexc_canary_positions (
              position_row_id TEXT PRIMARY KEY, decision_id TEXT NOT NULL UNIQUE, symbol TEXT NOT NULL,
              status TEXT NOT NULL, entry_price REAL NOT NULL, original_stop REAL NOT NULL,
              current_stop REAL NOT NULL, tp3 REAL NOT NULL, volume_contracts REAL NOT NULL,
              notional_usdt REAL NOT NULL, risk_usdt REAL NOT NULL, leverage INTEGER NOT NULL,
              opened_at TEXT NOT NULL, updated_at TEXT NOT NULL
            );
            INSERT INTO mexc_canary_positions VALUES
              ('p1','d1','BTC_USDT','OPEN',100,98,98,110,1,100,2,5,'t0','t0');
        """)
    with ls.connect(path) as conn:
        ls.ensure_tables(conn)
        columns = {row[1] for row in conn.execute("PRAGMA table_info(mexc_canary_positions)")}
        row = conn.execute("SELECT decision_id,status FROM mexc_canary_positions").fetchone()
    assert {
        "direction", "favorable_price", "last_reconciled_at", "last_price_at",
        "last_monitor_error_at", "monitor_error_count",
    } <= columns
    assert tuple(row) == ("d1", "OPEN")


def test_ensure_tables_adds_economic_trade_columns_before_creating_index(tmp_path):
    path = tmp_path / "old-decisions.sqlite"
    with sqlite3.connect(path) as conn:
        conn.executescript("""
            CREATE TABLE mexc_canary_control (
              control_key TEXT PRIMARY KEY, control_value TEXT NOT NULL, updated_at TEXT NOT NULL
            );
            CREATE TABLE mexc_canary_decisions (
              decision_id TEXT PRIMARY KEY, signal_id TEXT NOT NULL UNIQUE, captured_at TEXT NOT NULL,
              paper_alert_id TEXT, symbol TEXT NOT NULL, mode TEXT NOT NULL, entry_mode TEXT,
              eligible INTEGER NOT NULL, state TEXT NOT NULL, rejection_reasons_json TEXT NOT NULL,
              decision_json TEXT NOT NULL, decision_hash TEXT NOT NULL, config_hash TEXT NOT NULL,
              decision_context_type TEXT NOT NULL
            );
            INSERT INTO mexc_canary_decisions VALUES
              ('d1','s1','t0',NULL,'BTC_USDT','swing','BREAKOUT_CONTINUATION',1,
               'QUEUED','[]','{}','h1','h2','paper_alert');
        """)
    with ls.connect(path) as conn:
        ls.ensure_tables(conn)
        columns = {row[1] for row in conn.execute("PRAGMA table_info(mexc_canary_decisions)")}
        indexes = {row[1] for row in conn.execute("PRAGMA index_list(mexc_canary_decisions)")}
        row = conn.execute(
            "SELECT decision_id,economic_trade_key,parent_decision_id,recovery_sequence "
            "FROM mexc_canary_decisions"
        ).fetchone()
    assert {"economic_trade_key", "parent_decision_id", "recovery_sequence"} <= columns
    assert "idx_mexc_canary_decisions_economic_key" in indexes
    assert tuple(row) == ("d1", None, None, 0)


def test_ensure_tables_migrates_old_parity_schema_and_preserves_evidence(tmp_path):
    path = tmp_path / "old-parity.sqlite"
    with sqlite3.connect(path) as conn:
        conn.executescript("""
            CREATE TABLE mexc_canary_control (
              control_key TEXT PRIMARY KEY, control_value TEXT NOT NULL, updated_at TEXT NOT NULL
            );
            CREATE TABLE mexc_canary_parity_plans (
              decision_id TEXT PRIMARY KEY, signal_id TEXT NOT NULL, symbol TEXT NOT NULL,
              plan_json TEXT NOT NULL, source TEXT NOT NULL, captured_at TEXT NOT NULL,
              created_at TEXT NOT NULL, updated_at TEXT NOT NULL
            );
            CREATE TABLE mexc_canary_parity_outcomes (
              decision_id TEXT NOT NULL, profile_id TEXT NOT NULL, signal_id TEXT NOT NULL,
              symbol TEXT NOT NULL, entry_at TEXT NOT NULL, entry_price REAL NOT NULL,
              original_stop REAL NOT NULL, tp1 REAL, tp2 REAL, tp3 REAL NOT NULL,
              risk_usdt REAL, closed INTEGER NOT NULL, clean INTEGER NOT NULL, status TEXT NOT NULL,
              close_at TEXT, close_price REAL, close_reason TEXT, gross_pnl_usdt REAL,
              fees_usdt REAL, slippage_usdt REAL, funding_usdt REAL, net_pnl_usdt REAL,
              max_favorable_r REAL, execution_json TEXT NOT NULL, created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL, PRIMARY KEY(decision_id,profile_id)
            );
            INSERT INTO mexc_canary_parity_plans VALUES
              ('d1','s1','BTC_USDT','{}','existing_canary_order','t0','t0','t0');
        """)
    with ls.connect(path) as conn:
        ls.ensure_tables(conn)
        plan_cols = {row[1] for row in conn.execute("PRAGMA table_info(mexc_canary_parity_plans)")}
        outcome_cols = {row[1] for row in conn.execute("PRAGMA table_info(mexc_canary_parity_outcomes)")}
        row = conn.execute(
            "SELECT decision_id,clean,evidence_class FROM mexc_canary_parity_plans"
        ).fetchone()
    assert {"validation_json", "clean", "evidence_class"} <= plan_cols
    assert "evidence_class" in outcome_cols
    assert tuple(row) == ("d1", 0, "historical_backfill")


def test_worker_rejects_legacy_queue_without_point_in_time_entry(tmp_path):
    store = make_db(tmp_path / "t.sqlite")
    captured = capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=cfg())
    assert captured["queued"] is True
    with store.connect() as conn:
        row = conn.execute("SELECT decision_id,decision_json FROM mexc_canary_decisions").fetchone()
        body = json.loads(row["decision_json"])
        body.pop("entry_time_basis", None)
        body.pop("current_price_revalidated", None)
        conn.execute("UPDATE mexc_canary_decisions SET decision_json=? WHERE decision_id=?",
                     (json.dumps(body), row["decision_id"]))
        conn.commit()
    result = worker_once(db=store.db_path, cfg=cfg(), client=FakePublicClient())
    assert result["status"] == "REJECTED_ENTRY_PROVENANCE"


def test_worker_rejects_queue_that_expired_after_capture_without_exchange_io(tmp_path):
    store = make_db(tmp_path / "stale-queue.sqlite")
    captured = capture_paper_candidate(
        store=store, signal=signal(), payload=payload(), cfg=cfg())
    assert captured["queued"] is True
    with store.connect() as conn:
        conn.execute(
            "UPDATE mexc_canary_decisions SET captured_at='2026-07-01T00:00:00+00:00'"
        )
        conn.commit()
    fake = FakePublicClient()
    result = worker_once(db=store.db_path, cfg=cfg(), client=fake)
    assert result["status"] == "REJECTED_STALE_QUEUE"
    assert fake.create_calls == 0
    with store.connect() as conn:
        assert conn.execute(
            "SELECT status FROM mexc_canary_outbox"
        ).fetchone()[0] == "REJECTED_STALE_QUEUE"


def test_maintenance_rejects_stale_processing_with_no_exchange_footprint(tmp_path):
    store = make_db(tmp_path / "stale-processing.sqlite")
    captured = capture_paper_candidate(
        store=store, signal=signal(), payload=payload(), cfg=cfg())
    assert captured["queued"] is True
    with store.connect() as conn:
        assert ls.claim_next(conn) is not None
        conn.execute(
            "UPDATE mexc_canary_decisions SET captured_at='2026-07-01T00:00:00+00:00'"
        )
        conn.commit()

    result = invalidate_stale_queues(db=store.db_path, cfg=cfg())

    assert result["invalidated"][0]["reason"] == "STALE_PROCESSING_NO_EXCHANGE_FOOTPRINT"
    with store.connect() as conn:
        assert conn.execute(
            "SELECT status FROM mexc_canary_outbox"
        ).fetchone()[0] == "REJECTED_STALE_QUEUE"


def test_maintenance_keeps_stale_processing_when_risk_was_reserved(tmp_path):
    store = make_db(tmp_path / "stale-processing-reserved.sqlite")
    captured = capture_paper_candidate(
        store=store, signal=signal(), payload=payload(), cfg=cfg())
    assert captured["queued"] is True
    with store.connect() as conn:
        assert ls.claim_next(conn) is not None
        conn.execute(
            "UPDATE mexc_canary_decisions SET captured_at='2026-07-01T00:00:00+00:00'"
        )
        conn.commit()
        reservation = ls.reserve_risk(
            conn, decision_id=captured["decision_id"], symbol="BTC_USDT",
            risk_usdt=1.0, margin_usdt=1.0, notional_usdt=10.0,
            max_risk_usdt=50.0, max_margin_usdt=None, max_notional_usdt=None,
        )
        assert reservation["ok"] is True
        conn.commit()

    result = invalidate_stale_queues(db=store.db_path, cfg=cfg())

    assert result["invalidated"] == []
    with store.connect() as conn:
        assert conn.execute(
            "SELECT status FROM mexc_canary_outbox"
        ).fetchone()[0] == "PROCESSING"


def test_favorable_breakout_drift_is_accepted_when_frozen_stop_remains_safe():
    decision = {
        "decision_id": "drift", "signal_id": "drift-signal", "symbol": "BTC_USDT",
        "direction": "long", "entry_mode": "BREAKOUT_CONTINUATION", "entry_price": 100.0,
        "original_stop": 98.0, "tp1": 103.0, "tp2": 106.0, "tp3": 110.0,
        "live_risk_multiplier": 1.0,
    }
    plan = build_order_plan(
        decision=decision, contract=contract(), depth=depth(ask=99.0, bid=98.95),
        cfg=cfg(),
    )
    assert plan.reference_entry == 100.0
    assert plan.limit_price > plan.reference_entry
    assert plan.original_stop == 98.0
    assert (plan.tp1, plan.tp2, plan.tp3) == (103.0, 106.0, 110.0)
    assert plan.actual_risk_usdt <= 10.0


def test_favorable_short_breakout_drift_is_accepted_when_frozen_stop_remains_safe():
    decision = {
        "decision_id": "short-drift", "signal_id": "short-drift-signal", "symbol": "BTC_USDT",
        "direction": "short", "entry_mode": "BREAKOUT_CONTINUATION", "entry_price": 100.0,
        "original_stop": 102.0, "tp1": 97.0, "tp2": 94.0, "tp3": 90.0,
        "live_risk_multiplier": 1.0,
    }
    plan = build_order_plan(
        decision=decision, contract=contract(), depth=depth(ask=101.05, bid=101.0),
        cfg=cfg(),
    )
    assert plan.reference_entry == 100.0
    assert plan.limit_price < plan.reference_entry
    assert plan.original_stop == 102.0
    assert plan.actual_risk_usdt <= 10.0


def test_favorable_swing_breakout_fill_is_allowed_when_frozen_stop_remains_safe():
    decision = {
        "decision_id": "swing-drift", "signal_id": "swing-drift-signal", "symbol": "ALT_USDT",
        "direction": "long", "mode": "swing", "entry_mode": "BREAKOUT_CONTINUATION", "entry_price": 100.0,
        "original_stop": 98.0, "tp1": 103.0, "tp2": 106.0, "tp3": 110.0,
        "live_risk_multiplier": 1.0,
    }
    # 80 bps better than the Paper entry, but still 1.2% above the frozen stop.
    plan = build_order_plan(
        decision=decision, contract=contract(), depth=depth(ask=99.2, bid=99.15), cfg=cfg(),
    )
    assert plan.reference_entry == 100.0
    assert plan.limit_price == 100.75
    assert plan.actual_risk_usdt <= 10.0


def test_swing_breakout_accepts_small_adverse_cross_venue_move_with_capped_ioc():
    decision = {
        "decision_id": "swing-adverse", "signal_id": "swing-adverse-signal", "symbol": "ALT_USDT",
        "direction": "long", "mode": "swing", "entry_mode": "BREAKOUT_CONTINUATION", "entry_price": 100.0,
        "original_stop": 98.0, "tp1": 103.0, "tp2": 106.0, "tp3": 110.0,
        "live_risk_multiplier": 1.0,
    }
    plan = build_order_plan(
        decision=decision, contract=contract(), depth=depth(ask=100.6, bid=100.55), cfg=cfg(),
    )
    assert plan.limit_price == 100.75
    assert plan.actual_risk_usdt <= 10.0


def test_favorable_swing_breakout_near_frozen_stop_is_rejected():
    decision = {
        "decision_id": "swing-near-stop", "signal_id": "swing-near-stop-signal", "symbol": "ALT_USDT",
        "direction": "long", "mode": "swing", "entry_mode": "BREAKOUT_CONTINUATION", "entry_price": 100.0,
        "original_stop": 98.0, "tp1": 103.0, "tp2": 106.0, "tp3": 110.0,
        "live_risk_multiplier": 1.0,
    }
    with pytest.raises(PlanRejected, match="ENTRY_TOO_CLOSE_TO_FROZEN_STOP"):
        build_order_plan(
            decision=decision, contract=contract(), depth=depth(ask=98.2, bid=98.15), cfg=cfg(),
        )


def test_swing_can_use_wider_structural_stop_without_relaxing_intraday_limit():
    decision = {
        "decision_id": "swing-wide-stop", "signal_id": "swing-wide-stop-signal", "symbol": "ALT_USDT",
        "direction": "long", "mode": "swing", "entry_mode": "BREAKOUT_CONTINUATION", "entry_price": 100.0,
        "original_stop": 90.5, "tp1": 112.0, "tp2": 124.0, "tp3": 136.0,
        "live_risk_multiplier": 1.0,
    }
    plan = build_order_plan(decision=decision, contract=contract(), depth=depth(), cfg=cfg())
    assert plan.stop_distance_pct > 0.08
    assert plan.stop_distance_pct < 0.12
    assert plan.actual_risk_usdt <= 10.0

    decision["mode"] = "intraday"
    with pytest.raises(PlanRejected, match="STOP_TOO_WIDE"):
        build_order_plan(decision=decision, contract=contract(), depth=depth(), cfg=cfg())


def test_config_uses_fixed_daily_loss_limit_aligned_with_open_risk_cap():
    assert cfg().daily_loss_limit_usdt == 50.0


def test_status_is_read_only_and_does_not_reconcile_decision_state(tmp_path):
    store = make_db(tmp_path / "status-read-only.sqlite")
    capture_paper_candidate(
        store=store, signal=signal(), payload=payload(), cfg=cfg())
    with store.connect() as conn:
        conn.execute("UPDATE mexc_canary_outbox SET status='REJECTED_TEST'")
        conn.execute("UPDATE mexc_canary_decisions SET state='QUEUED'")
        ls.set_monitor_heartbeat(
            conn,
            status="OK",
            live_armed=True,
            active_positions=0,
            detail={"worker": "IDLE", "reconcile": "OK", "armed_venues": ["mexc", "bybit"]},
        )
        conn.commit()
    result = canary_status(db=store.db_path, cfg=cfg())
    assert result["initialized"] is True
    assert result["worker_armed_venues"] == ["bybit", "mexc"]
    assert result["venues"]["mexc"]["worker_armed"] is True
    assert result["venues"]["bybit"]["worker_armed"] is True
    with store.connect() as conn:
        assert conn.execute(
            "SELECT state FROM mexc_canary_decisions"
        ).fetchone()[0] == "QUEUED"


def test_close_limit_uses_documented_hedge_mode_close_side(monkeypatch):
    client = MexcFuturesClient(access_key="a", secret_key="b")
    captured = {}

    def _request(method, path, **kwargs):
        captured.update({"method": method, "path": path, **kwargs})
        return {"orderId": "close-1"}

    monkeypatch.setattr(client, "_request", _request)
    result = client.place_close_limit(
        symbol="BTC/USDT", position_id=77, direction="long", volume=3,
        price=103.0, leverage=4, external_oid="tp1_test",
    )
    assert result["orderId"] == "close-1"
    assert captured["path"] == "/api/v1/private/order/submit"
    assert captured["body"]["side"] == 4
    assert captured["body"]["type"] == 1
    assert captured["body"]["positionId"] == 77
    assert "reduceOnly" not in captured["body"]


def test_stop_only_tpsl_modify_omits_zero_take_profit(monkeypatch):
    client = MexcFuturesClient(access_key="a", secret_key="b")
    captured = {}

    def _request(method, path, **kwargs):
        captured.update({"method": method, "path": path, **kwargs})
        return {"success": True}

    monkeypatch.setattr(client, "_request", _request)
    client.modify_tpsl(stop_plan_order_id=88, stop_loss=101.0, take_profit=None)

    assert captured["path"] == "/api/v1/private/stoporder/change_plan_price"
    assert captured["body"]["stopPlanOrderId"] == 88
    assert captured["body"]["stopLossPrice"] == 101.0
    assert "takeProfitPrice" not in captured["body"]
    assert "profitTrend" not in captured["body"]


def test_fake_live_submit_fill_and_model_f_reconcile(tmp_path, monkeypatch):
    monkeypatch.setenv("MEXC_CANARY_ACCESS_KEY", "dummy-access")
    monkeypatch.setenv("MEXC_CANARY_SECRET", "dummy-secret")
    monkeypatch.setenv("MEXC_LIVE_CANARY_ARMED", "I_UNDERSTAND_REAL_MEXC_ORDERS")
    live_cfg = cfg(submission_enabled=True, execution_mode="live")
    store = make_db(tmp_path / "t.sqlite")
    captured = capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=live_cfg)
    fake = FakePrivateClient()
    submitted = worker_once(db=store.db_path, cfg=live_cfg, client=fake)
    assert captured["queued"] is True
    assert submitted["status"] == "SUBMITTED"
    assert fake.create_calls == 1
    assert fake.created[0]["openType"] == 1
    assert fake.created[0]["stopLossPrice"] == 98.0
    assert "takeProfitPrice" not in fake.created[0]
    assert submitted["protection"]["status"] == "OK"
    assert submitted["protection"]["stops_moved"] == 1
    assert len(fake.tpsl) == 1
    assert fake.tpsl[0]["takeProfitPrice"] == 0
    with store.connect() as conn:
        filled_plan = json.loads(conn.execute(
            "SELECT plan_json FROM mexc_canary_orders WHERE decision_id=?",
            (captured["decision_id"],),
        ).fetchone()[0])
    assert [item["price"] for item in fake.close_limits] == [
        filled_plan["tp1"], filled_plan["tp2"],
    ]
    assert sum(item["vol"] for item in fake.close_limits) < fake.created[0]["vol"]

    rec = reconcile_once(db=store.db_path, cfg=live_cfg, client=fake)
    assert rec["status"] == "OK"
    assert rec["filled"] == 0
    assert rec["stops_moved"] == 0
    assert fake.modified[-1]["stop_loss"] == 100.0
    assert fake.modified[-1]["take_profit"] is None
    assert len(fake.modified) == 2
    assert fake.modified[0]["stop_loss"] == filled_plan["original_stop"]
    with store.connect() as conn:
        pos = conn.execute("SELECT * FROM mexc_canary_positions").fetchone()
        assert pos["status"] == "OPEN"
        assert pos["protection_stage"] == "BREAKEVEN"
        assert pos["current_stop"] == 100.0
        assert pos["last_reconciled_at"] is not None
        assert pos["last_price_at"] is not None
        assert pos["monitor_error_count"] == 0
        legs = conn.execute(
            "SELECT leg_index,target_price,stop_price,status FROM mexc_canary_exit_legs "
            "ORDER BY leg_index"
        ).fetchall()
        assert [tuple(row) for row in legs] == [
            (1, filled_plan["tp1"], 100.0, "ACTIVE"),
            (2, filled_plan["tp2"], 100.0, "ACTIVE"),
            (3, filled_plan["tp3"], 100.0, "ACTIVE"),
        ]
        assert conn.execute("SELECT status FROM mexc_canary_risk_reservations").fetchone()[0] == "OPEN"


def test_burst_submit_defers_only_three_tp_installation_behind_native_stop(tmp_path, monkeypatch):
    """Burst handling may defer TP reconciliation, never the entry's native stop."""
    monkeypatch.setenv("MEXC_CANARY_ACCESS_KEY", "dummy-access")
    monkeypatch.setenv("MEXC_CANARY_SECRET", "dummy-secret")
    monkeypatch.setenv("MEXC_LIVE_CANARY_ARMED", "I_UNDERSTAND_REAL_MEXC_ORDERS")
    live_cfg = cfg(submission_enabled=True, execution_mode="live")
    store = make_db(tmp_path / "burst-native-stop.sqlite")
    assert capture_paper_candidate(
        store=store, signal=signal(), payload=payload(), cfg=live_cfg,
    )["queued"]
    fake = FakePrivateClient()

    submitted = worker_once(
        db=store.db_path, cfg=live_cfg, client=fake,
        reconcile_after_submission=False,
    )

    assert submitted["status"] == "SUBMITTED"
    assert submitted["protection"]["status"] == "DEFERRED_NATIVE_STOP_ATTACHED"
    assert fake.created[0]["stopLossPrice"] == 98.0
    assert len(fake.tpsl) == 1
    assert fake.tpsl[0]["stopLossPrice"] == 98.0
    assert fake.tpsl[0]["takeProfitPrice"] == 0
    assert fake.close_limits == []


def test_live_fill_notification_is_confirmed_and_deduplicated(tmp_path, monkeypatch):
    monkeypatch.setenv("MEXC_CANARY_ACCESS_KEY", "dummy-access")
    monkeypatch.setenv("MEXC_CANARY_SECRET", "dummy-secret")
    monkeypatch.setenv("MEXC_LIVE_CANARY_ARMED", "I_UNDERSTAND_REAL_MEXC_ORDERS")
    live_cfg = cfg(submission_enabled=True, execution_mode="live")
    store = make_db(tmp_path / "live-fill-notification.sqlite")
    capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=live_cfg)
    worker_once(db=store.db_path, cfg=live_cfg, client=FakePrivateClient())

    notifier = FakeNotifier()
    first = _deliver_live_fill_notifications(store.db_path, notifier=notifier)
    second = _deliver_live_fill_notifications(store.db_path, notifier=notifier)

    assert first["staged"] == 1
    assert first["sent"] == 1
    assert second["sent"] == 0
    assert len(notifier.messages) == 1
    assert "LIVE FILLED" in notifier.messages[0]["text"]
    assert "BTC/USDT · LONG" in notifier.messages[0]["text"]
    assert "Защита: 3 TP + stop активны" in notifier.messages[0]["text"]
    with store.connect() as conn:
        row = conn.execute(
            "SELECT notification_kind,status,attempts FROM mexc_canary_notification_outbox"
        ).fetchone()
    assert tuple(row) == ("LIVE_ENTRY_FILLED", "SENT", 1)


def test_live_preflight_rejection_notification_is_clear_and_deduplicated(tmp_path) -> None:
    path = tmp_path / "live-preflight-notification.sqlite"
    decision = {"symbol": "NVO/USDT", "display_symbol": "NVO", "direction": "long"}

    assert _stage_live_preflight_rejection_notification(
        path, decision_id="decision-nvo", decision=decision,
        reason="MEXC_NATIVE_GEOMETRY_INVALID",
    ) is True
    assert _stage_live_preflight_rejection_notification(
        path, decision_id="decision-nvo", decision=decision,
        reason="MEXC_NATIVE_GEOMETRY_INVALID",
    ) is False

    notifier = FakeNotifier()
    delivered = _deliver_live_fill_notifications(path, notifier=notifier)
    assert delivered["sent"] == 1
    assert len(notifier.messages) == 1
    assert "LIVE НЕ ОТКРЫТ" in notifier.messages[0]["text"]
    assert "NVO · LONG" in notifier.messages[0]["text"]
    assert "вход -> SL -> 3 TP" in notifier.messages[0]["text"]


def test_definitive_exchange_rejection_does_not_trip_unknown_submission_kill_switch(
    tmp_path, monkeypatch,
):
    class RegionRejectedClient(FakePrivateClient):
        def create_order(self, order):
            self.create_calls += 1
            raise MexcAPIError(
                "MEXC request rejected: opening positions unavailable in this region",
                code=403,
                status_code=200,
            )

        def order_by_external_id(self, *_args, **_kwargs):
            raise AssertionError("a definitive business rejection must not be queried as unknown")

    monkeypatch.setenv("MEXC_CANARY_ACCESS_KEY", "dummy-access")
    monkeypatch.setenv("MEXC_CANARY_SECRET", "dummy-secret")
    monkeypatch.setenv("MEXC_LIVE_CANARY_ARMED", "I_UNDERSTAND_REAL_MEXC_ORDERS")
    live_cfg = cfg(submission_enabled=True, execution_mode="live")
    store = make_db(tmp_path / "submission-rejected.sqlite")
    capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=live_cfg)

    result = worker_once(db=store.db_path, cfg=live_cfg, client=RegionRejectedClient())

    assert result["status"] == "REJECTED_SUBMISSION"
    assert result["order_accepted"] is False
    with store.connect() as conn:
        assert ls.kill_switch_state(conn) == "CLEAR"
        assert conn.execute("SELECT status FROM mexc_canary_outbox").fetchone()[0] == "REJECTED_SUBMISSION"
        assert conn.execute("SELECT status FROM mexc_canary_orders").fetchone()[0] == "REJECTED_SUBMISSION"
        risk = conn.execute("SELECT status,release_reason FROM mexc_canary_risk_reservations").fetchone()
        assert risk["status"] == "RELEASED"
        assert "definitively rejected" in risk["release_reason"]


def test_definitive_mexc_rejection_falls_back_once_to_bybit(tmp_path, monkeypatch):
    class RegionRejectedClient(FakePrivateClient):
        def create_order(self, order):
            self.create_calls += 1
            raise MexcAPIError(
                "MEXC request rejected: opening positions unavailable in this region",
                code=403, status_code=200,
            )

    class BybitFallbackClient:
        def __init__(self):
            self.created = []

        def contract_info(self, symbol):
            row = contract()
            row.update({"symbol": "BTCUSDT", "contractSize": 1.0,
                        "volUnit": 0.001, "minVol": 0.001})
            return row

        def depth(self, symbol, limit=20):
            return {"asks": [[100.05, 1000]], "bids": [[100.0, 1000]]}

        def account_asset(self, currency="USDT"):
            return {"equity": 100.0, "availableOpen": 100.0}

        def fee_rate(self, symbol):
            # Keep MEXC as the initial cost winner so this exercises the
            # post-submission definitive-rejection fallback.
            return {"makerFeeRate": 0.001, "takerFeeRate": 0.001}

        def set_leverage(self, symbol, leverage):
            return {}

        def create_entry(self, **kwargs):
            self.created.append(kwargs)
            return {"orderId": "bybit-fallback-entry"}

        def order_by_external_id(self, symbol, order_link_id):
            return {"orderId": "bybit-fallback-entry", "externalOid": order_link_id,
                    "state": 2, "dealVol": 0}

        def open_positions(self, symbol=None):
            return []

    for name, value in {
        "MEXC_CANARY_ACCESS_KEY": "mexc-key",
        "MEXC_CANARY_SECRET": "mexc-secret",
        "MEXC_LIVE_CANARY_ARMED": "I_UNDERSTAND_REAL_MEXC_ORDERS",
        "BYBIT_LIVE_ACCESS_KEY": "bybit-key",
        "BYBIT_LIVE_SECRET": "bybit-secret",
        "BYBIT_LIVE_ARMED": "I_UNDERSTAND_REAL_BYBIT_ORDERS",
    }.items():
        monkeypatch.setenv(name, value)
    live_cfg = cfg(submission_enabled=True, execution_mode="live")
    store = make_db(tmp_path / "mexc-region-bybit-fallback.sqlite")
    capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=live_cfg)
    mexc = RegionRejectedClient()
    bybit = BybitFallbackClient()

    result = worker_once(
        db=store.db_path, cfg=live_cfg, client=mexc,
        bybit_execution_client=bybit,
    )

    assert result["status"] == "SUBMITTED"
    assert result["venue"] == "bybit"
    assert result["fallback_from"] == "mexc"
    assert mexc.create_calls == 1
    assert len(bybit.created) == 1
    with store.connect() as conn:
        order = conn.execute(
            "SELECT venue,symbol,status,plan_json FROM mexc_canary_orders"
        ).fetchone()
        assert tuple(order[:3]) == ("bybit", "BTCUSDT", "PENDING")
        assert json.loads(order["plan_json"])["venue"] == "bybit"
        assert conn.execute("SELECT status FROM mexc_canary_outbox").fetchone()[0] == "SUBMITTED"
        assert conn.execute(
            "SELECT COUNT(*) FROM mexc_canary_events "
            "WHERE event_type='MEXC_REJECTION_FALLBACK_TO_BYBIT'"
        ).fetchone()[0] == 1


def test_definitive_bybit_rejection_falls_back_once_to_mexc(tmp_path, monkeypatch):
    class AgreementRejectedBybitClient:
        def __init__(self):
            self.created = []

        def contract_info(self, symbol):
            row = contract()
            row.update({"symbol": "BTCUSDT", "contractSize": 1.0,
                        "volUnit": 0.001, "minVol": 0.001})
            return row

        def depth(self, symbol, limit=20):
            # Make Bybit the initial cheapest candidate; its explicit business
            # rejection must then use the one-way MEXC fallback.
            return {"asks": [[100.01, 1000]], "bids": [[100.0, 1000]]}

        def account_asset(self, currency="USDT"):
            return {"equity": 100.0, "availableOpen": 100.0}

        def fee_rate(self, symbol):
            return {"makerFeeRate": 0.0, "takerFeeRate": 0.0}

        def set_leverage(self, symbol, leverage):
            return {}

        def create_entry(self, **kwargs):
            self.created.append(kwargs)
            raise BybitAPIError(
                "You must sign the required agreement before trading this contract.",
                code=110126, status_code=200,
            )

        def order_by_external_id(self, *_args, **_kwargs):
            raise AssertionError("a definitive Bybit business rejection must not be queried")

    for name, value in {
        "MEXC_CANARY_ACCESS_KEY": "mexc-key",
        "MEXC_CANARY_SECRET": "mexc-secret",
        "MEXC_LIVE_CANARY_ARMED": "I_UNDERSTAND_REAL_MEXC_ORDERS",
        "BYBIT_LIVE_ACCESS_KEY": "bybit-key",
        "BYBIT_LIVE_SECRET": "bybit-secret",
        "BYBIT_LIVE_ARMED": "I_UNDERSTAND_REAL_BYBIT_ORDERS",
    }.items():
        monkeypatch.setenv(name, value)
    live_cfg = cfg(submission_enabled=True, execution_mode="live")
    store = make_db(tmp_path / "bybit-agreement-mexc-fallback.sqlite")
    capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=live_cfg)
    mexc = FakePrivateClient()
    bybit = AgreementRejectedBybitClient()

    result = worker_once(
        db=store.db_path, cfg=live_cfg, client=mexc,
        bybit_execution_client=bybit,
    )

    assert result["status"] == "SUBMITTED"
    assert result["venue"] == "mexc"
    assert result["fallback_from"] == "bybit"
    assert len(bybit.created) == 1
    assert mexc.create_calls == 1
    with store.connect() as conn:
        order = conn.execute(
            "SELECT venue,symbol,status,plan_json FROM mexc_canary_orders "
            "WHERE venue='mexc' ORDER BY updated_at DESC LIMIT 1"
        ).fetchone()
        assert tuple(order[:2]) == ("mexc", "BTC_USDT")
        assert order["status"] in {"PENDING", "FILLED"}
        assert json.loads(order["plan_json"])["venue"] == "mexc"
        assert conn.execute("SELECT status FROM mexc_canary_outbox").fetchone()[0] == "SUBMITTED"
        assert conn.execute(
            "SELECT COUNT(*) FROM mexc_canary_events "
            "WHERE event_type='BYBIT_REJECTION_FALLBACK_TO_MEXC'"
        ).fetchone()[0] == 1
        assert conn.execute(
            "SELECT COUNT(*) FROM mexc_canary_events "
            "WHERE event_type='MEXC_REJECTION_FALLBACK_TO_BYBIT'"
        ).fetchone()[0] == 0


def test_model_f_stop_modify_is_rounded_to_contract_tick(tmp_path, monkeypatch):
    monkeypatch.setenv("MEXC_CANARY_ACCESS_KEY", "dummy-access")
    monkeypatch.setenv("MEXC_CANARY_SECRET", "dummy-secret")
    monkeypatch.setenv("MEXC_LIVE_CANARY_ARMED", "I_UNDERSTAND_REAL_MEXC_ORDERS")
    live_cfg = cfg(submission_enabled=True, execution_mode="live")
    store = make_db(tmp_path / "rounded-stop.sqlite")
    capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=live_cfg)
    fake = FakePrivateClient()
    worker_once(db=store.db_path, cfg=live_cfg, client=fake)
    fake.modified.clear()

    monkeypatch.setattr(
        "src.live_execution.service.model_f_stop",
        lambda **_: ("PROFIT_LOCK", 101.037, 2.0),
    )
    result = reconcile_once(db=store.db_path, cfg=live_cfg, client=fake)

    assert result["status"] == "OK"
    assert fake.modified[-1]["stop_loss"] == 101.03


def test_position_reconcile_retries_one_sqlite_lock_without_order_side_effect(tmp_path, monkeypatch):
    """A transient local lock must not turn a healthy live position into DEGRADED.

    The retry wraps only the reconciliation lease/state write; entry submission
    has already completed before this path and is never retried here.
    """
    monkeypatch.setenv("MEXC_CANARY_ACCESS_KEY", "dummy-access")
    monkeypatch.setenv("MEXC_CANARY_SECRET", "dummy-secret")
    monkeypatch.setenv("MEXC_LIVE_CANARY_ARMED", "I_UNDERSTAND_REAL_MEXC_ORDERS")
    live_cfg = cfg(
        submission_enabled=True,
        execution_mode="live",
        position_reconcile_db_busy_timeout_ms=1,
        position_reconcile_db_retry_attempts=2,
        position_reconcile_db_retry_backoff_seconds=0,
    )
    store = make_db(tmp_path / "reconcile-lock-retry.sqlite")
    capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=live_cfg)
    fake = FakePrivateClient()
    worker_once(db=store.db_path, cfg=live_cfg, client=fake)

    original_claim = ls.try_claim_control_lease
    calls = {"n": 0}

    def locked_once(conn, **kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            raise sqlite3.OperationalError("database is locked")
        return original_claim(conn, **kwargs)

    monkeypatch.setattr(ls, "try_claim_control_lease", locked_once)
    result = reconcile_once(db=store.db_path, cfg=live_cfg, client=fake)

    assert result["status"] == "OK"
    assert calls["n"] == 2
    assert fake.create_calls == 1  # only the original entry submission
    with store.connect() as conn:
        row = conn.execute("SELECT monitor_error_count,status FROM mexc_canary_positions").fetchone()
    assert row["status"] == "OPEN"
    assert row["monitor_error_count"] == 0


def test_position_reconcile_error_event_includes_message(tmp_path, monkeypatch):
    class RejectingStopModifyClient(FakePrivateClient):
        def __init__(self):
            super().__init__()
            self.modify_calls = 0

        def modify_tpsl(self, **kwargs):
            self.modify_calls += 1
            if self.modify_calls > 1:
                raise MexcAPIError("bad stop precision")
            return super().modify_tpsl(**kwargs)

    monkeypatch.setenv("MEXC_CANARY_ACCESS_KEY", "dummy-access")
    monkeypatch.setenv("MEXC_CANARY_SECRET", "dummy-secret")
    monkeypatch.setenv("MEXC_LIVE_CANARY_ARMED", "I_UNDERSTAND_REAL_MEXC_ORDERS")
    live_cfg = cfg(submission_enabled=True, execution_mode="live")
    store = make_db(tmp_path / "reconcile-error-message.sqlite")
    capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=live_cfg)
    fake = RejectingStopModifyClient()
    worker_once(db=store.db_path, cfg=live_cfg, client=fake)

    monkeypatch.setattr(
        "src.live_execution.service.model_f_stop",
        lambda **_: ("PROFIT_LOCK", 101.03, 2.0),
    )
    result = reconcile_once(db=store.db_path, cfg=live_cfg, client=fake)

    assert result["status"] == "DEGRADED"
    with store.connect() as conn:
        event_payload = json.loads(conn.execute(
            "SELECT payload_json FROM mexc_canary_events "
            "WHERE event_type='POSITION_RECONCILE_ERROR'"
        ).fetchone()[0])
        assert event_payload == {
            "error_type": "MexcAPIError",
            "stage": "move_protective_stop",
            "error": "bad stop precision",
        }


def test_position_reconcile_error_is_journaled_once_per_outage_window(tmp_path, monkeypatch):
    class RejectingStopModifyClient(FakePrivateClient):
        def modify_tpsl(self, **kwargs):
            raise MexcAPIError("bad stop precision")

    monkeypatch.setenv("MEXC_CANARY_ACCESS_KEY", "dummy-access")
    monkeypatch.setenv("MEXC_CANARY_SECRET", "dummy-secret")
    monkeypatch.setenv("MEXC_LIVE_CANARY_ARMED", "I_UNDERSTAND_REAL_MEXC_ORDERS")
    live_cfg = cfg(submission_enabled=True, execution_mode="live")
    store = make_db(tmp_path / "reconcile-error-rate-limit.sqlite")
    capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=live_cfg)
    fake = RejectingStopModifyClient()
    worker_once(db=store.db_path, cfg=live_cfg, client=fake)
    monkeypatch.setattr(
        "src.live_execution.service.model_f_stop",
        lambda **_: ("PROFIT_LOCK", 101.03, 2.0),
    )

    assert reconcile_once(db=store.db_path, cfg=live_cfg, client=fake)["status"] == "DEGRADED"
    assert reconcile_once(db=store.db_path, cfg=live_cfg, client=fake)["status"] == "DEGRADED"
    with store.connect() as conn:
        events = conn.execute(
            "SELECT COUNT(*) FROM mexc_canary_events WHERE event_type='POSITION_RECONCILE_ERROR'"
        ).fetchone()[0]
        error_count = conn.execute(
            "SELECT monitor_error_count FROM mexc_canary_positions"
        ).fetchone()[0]
    assert events == 1
    # The initial post-submit protection attempt plus both explicit retries
    # all remain visible on the position even though the event journal is
    # deliberately rate-limited to one outage event.
    assert error_count == 3


def test_live_allows_manual_exchange_position_when_configured(tmp_path, monkeypatch):
    """A discretionary MEXC position must not block an isolated bot lane."""
    monkeypatch.setenv("MEXC_CANARY_ACCESS_KEY", "dummy-access")
    monkeypatch.setenv("MEXC_CANARY_SECRET", "dummy-secret")
    monkeypatch.setenv("MEXC_LIVE_CANARY_ARMED", "I_UNDERSTAND_REAL_MEXC_ORDERS")

    class ManualPositionClient(FakePrivateClient):
        def open_positions(self, symbol=None):
            manual = {
                "positionId": 999, "symbol": "BXSTOCK_USDT", "holdVol": 68,
                "positionType": 1, "state": 1, "openAvgPrice": 131.71,
                "liquidatePrice": 111.09, "leverage": 6,
            }
            own = super().open_positions(symbol)
            if symbol in {"BTC/USDT", "BTC_USDT"}:
                return own
            return [manual, *own]

    live_cfg = cfg(
        submission_enabled=True,
        execution_mode="live",
        allow_manual_exchange_positions=True,
    )
    store = make_db(tmp_path / "manual-position.sqlite")
    capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=live_cfg)
    result = worker_once(db=store.db_path, cfg=live_cfg, client=ManualPositionClient())

    assert result["status"] == "SUBMITTED"


def test_symbol_position_lookup_uses_exact_global_snapshot_before_filtered_endpoint():
    class SnapshotClient:
        def __init__(self):
            self.calls: list[str | None] = []

        def open_positions(self, symbol=None):
            self.calls.append(symbol)
            return [
                {"positionId": 1, "symbol": "BTC_USDT"},
                {"positionId": 2, "symbol": "GPS_USDT"},
            ]

    client = SnapshotClient()
    positions = _open_positions_for_symbol(client, "GPS/USDT")

    assert client.calls == [None]
    assert positions == [{"positionId": 2, "symbol": "GPS_USDT"}]


def test_symbol_position_lookup_uses_filtered_endpoint_only_when_global_snapshot_times_out():
    class SnapshotTimeoutClient:
        def open_positions(self, symbol=None):
            if symbol is None:
                raise MexcAPIError("MEXC transport error: ReadTimeout")
            assert symbol == "GPS/USDT"
            return [{"positionId": 2, "symbol": "GPS_USDT"}]

    assert _open_positions_for_symbol(SnapshotTimeoutClient(), "GPS/USDT") == [
        {"positionId": 2, "symbol": "GPS_USDT"}
    ]


def test_native_exit_legs_are_rechecked_on_a_short_independent_cadence(tmp_path):
    store = make_db(tmp_path / "exit-cadence.sqlite")
    opened = "2026-07-17T00:00:00+00:00"
    _seed_open_canary_position(
        store, decision_id="exit-cadence", opened_at=opened, tpsl_order_id="stop-1", tp_legs=3,
    )
    local = {"decision_id": "exit-cadence", "tpsl_order_id": "stop-1"}
    live_cfg = cfg(exit_leg_verify_interval_seconds=12)
    base = datetime(2026, 7, 17, tzinfo=timezone.utc)

    assert not _exit_leg_verification_due(
        path=store.db_path, local=local, cfg=live_cfg, now=base + timedelta(seconds=11)
    )
    assert _exit_leg_verification_due(
        path=store.db_path, local=local, cfg=live_cfg, now=base + timedelta(seconds=12)
    )


def test_partial_tp_keeps_exit_leg_cadence_after_first_fill(tmp_path):
    store = make_db(tmp_path / "partial-exit-cadence.sqlite")
    opened = "2026-07-17T00:00:00+00:00"
    _seed_open_canary_position(
        store, decision_id="partial-exit-cadence", opened_at=opened,
        tpsl_order_id="stop-1", tp_legs=3, virtual_tp3=True,
    )
    with store.connect() as conn:
        conn.execute(
            "UPDATE mexc_canary_exit_legs SET status='FILLED' "
            "WHERE decision_id='partial-exit-cadence' AND leg_index=1"
        )
        conn.commit()
    local = {"decision_id": "partial-exit-cadence", "tpsl_order_id": "stop-1"}
    live_cfg = cfg(exit_leg_verify_interval_seconds=12)
    base = datetime(2026, 7, 17, tzinfo=timezone.utc)

    assert not _exit_leg_verification_due(
        path=store.db_path, local=local, cfg=live_cfg, now=base + timedelta(seconds=11)
    )
    assert _exit_leg_verification_due(
        path=store.db_path, local=local, cfg=live_cfg, now=base + timedelta(seconds=12)
    )


def test_partial_tp_read_order_race_does_not_falsely_fail_protection() -> None:
    class PartialFillRaceClient(FakePrivateClient):
        def __init__(self):
            super().__init__()
            self.close_limits = [
                {"orderId": "201", "state": 3, "vol": 34},
                {"orderId": "202", "state": 1, "vol": 35},
            ]
            self.second_leg_reads = 0

        def open_positions(self, symbol=None):
            # Position has already reduced to the TP3 runner, while MEXC still
            # reports TP2 as active on its first close-order read.
            return [{"positionId": 77, "symbol": "BTC_USDT", "holdVol": 36}]

        def order_by_id(self, order_id):
            if str(order_id) == "202":
                self.second_leg_reads += 1
                if self.second_leg_reads >= 2:
                    self.close_limits[1]["state"] = 3
            return super().order_by_id(order_id)

    client = PartialFillRaceClient()
    stored = [
        {"order_kind": "CLOSE_LIMIT_TP", "exchange_order_id": "201", "status": "ACTIVE"},
        {"order_kind": "CLOSE_LIMIT_TP", "exchange_order_id": "202", "status": "ACTIVE"},
        {"order_kind": "VIRTUAL_TP3_MONITOR", "volume_contracts": 36, "status": "ACTIVE"},
    ]
    active = _confirmed_active_exit_orders(
        client=client, local={"symbol": "BTC_USDT", "volume_step": 1}, stored=stored,
        position_id="77", cfg=cfg(
            exit_visibility_timeout_seconds=0.1, exit_visibility_poll_seconds=0.001,
        ),
    )
    assert active is not None
    assert sum(float(item["vol"]) for item in active) == 36
    assert client.second_leg_reads >= 2


def test_tp_volume_mismatch_does_not_emergency_close_when_stop_is_verified(tmp_path):
    store = make_db(tmp_path / "tp-degraded-stop-safe.sqlite")
    opened = "2026-07-17T00:00:00+00:00"
    _seed_open_canary_position(
        store, decision_id="tp-degraded-stop-safe", opened_at=opened,
        tpsl_order_id="88", tp_legs=3, virtual_tp3=True,
    )
    with store.connect() as conn:
        conn.execute(
            "UPDATE mexc_canary_orders SET plan_json=? WHERE decision_id=?",
            (json.dumps({
                "direction": "long", "tp1": 103.0, "tp2": 106.0, "tp3": 110.0,
                "price_tick": 0.01, "volume_step": 1.0, "min_volume": 1.0,
                "leverage": 10, "open_type": 1,
            }), "tp-degraded-stop-safe"),
        )
        conn.execute(
            "UPDATE mexc_canary_positions SET volume_contracts=100,current_stop=98,"
            "original_stop=98,tp3=110 WHERE decision_id='tp-degraded-stop-safe'"
        )
        conn.execute(
            "UPDATE mexc_canary_exit_legs SET volume_contracts=33,status='FILLED',"
            "exchange_order_id='201' WHERE decision_id='tp-degraded-stop-safe' AND leg_index=1"
        )
        conn.execute(
            "UPDATE mexc_canary_exit_legs SET volume_contracts=33,status='ACTIVE',"
            "exchange_order_id='202' WHERE decision_id='tp-degraded-stop-safe' AND leg_index=2"
        )
        conn.execute(
            "UPDATE mexc_canary_exit_legs SET volume_contracts=34,status='ACTIVE' "
            "WHERE decision_id='tp-degraded-stop-safe' AND leg_index=3"
        )
        conn.commit()

    class MissingTpButStopSafeClient(FakePrivateClient):
        def __init__(self):
            super().__init__()
            self.tpsl = [{
                "id": 88, "positionId": 77, "state": 1,
                "stopLossPrice": 98.0, "takeProfitPrice": 0, "vol": 67,
            }]
            self.close_limits = [
                {"orderId": "201", "externalOid": "tp1", "state": 3, "vol": 33},
                {"orderId": "202", "externalOid": "tp2", "state": 4, "vol": 33},
            ]
            self.emergency_calls = 0

        def open_positions(self, symbol=None):
            return [{
                "positionId": 77, "symbol": "BTC_USDT", "holdVol": 67,
                "positionType": 1, "openType": 1, "state": 1,
                "openAvgPrice": 100.0, "liquidatePrice": 90.0, "leverage": 10,
            }]

        def emergency_close_long(self, **kwargs):
            self.emergency_calls += 1
            raise AssertionError("verified stop must prevent emergency close on TP mismatch")

    client = MissingTpButStopSafeClient()
    local = {
        "decision_id": "tp-degraded-stop-safe", "exchange_position_id": "77",
        "symbol": "BTC_USDT", "direction": "long", "current_stop": 98.0,
        "volume_contracts": 100.0, "plan_json": json.dumps({
            "direction": "long", "tp1": 103.0, "tp2": 106.0, "tp3": 110.0,
            "price_tick": 0.01, "volume_step": 1.0, "min_volume": 1.0,
            "leverage": 10, "open_type": 1,
        }),
    }

    fallback_stop, observed = _install_or_reconcile_exit_legs(
        path=store.db_path, client=client, local=local,
        pos={"holdVol": 67}, cfg=cfg(
            exit_visibility_timeout_seconds=0,
            exit_visibility_poll_seconds=0.01,
            position_reconcile_error_event_cooldown_seconds=0,
        ),
    )

    assert fallback_stop["id"] == 88
    assert client.emergency_calls == 0
    assert len(observed) == 3
    with store.connect() as conn:
        assert ls.kill_switch_state(conn) == "CLEAR"
        event = conn.execute(
            "SELECT payload_json FROM mexc_canary_events "
            "WHERE event_type='MEXC_TP_COVERAGE_DEGRADED'"
        ).fetchone()
    assert event is not None
    assert json.loads(event["payload_json"])["action"] == (
        "kept_position_open_because_fallback_stop_is_verified"
    )


def test_new_tp_install_visibility_failure_retries_when_stop_is_verified(tmp_path):
    store = make_db(tmp_path / "tp-install-retry-stop-safe.sqlite")
    opened = "2026-07-17T00:00:00+00:00"
    _seed_open_canary_position(
        store, decision_id="tp-install-retry-stop-safe", opened_at=opened,
        tpsl_order_id=None, tp_legs=0,
    )
    with store.connect() as conn:
        conn.execute(
            "UPDATE mexc_canary_orders SET plan_json=? WHERE decision_id=?",
            (json.dumps({
                "direction": "long", "tp1": 103.0, "tp2": 106.0, "tp3": 110.0,
                "price_tick": 0.01, "volume_step": 1.0, "min_volume": 1.0,
                "leverage": 10, "open_type": 1,
            }), "tp-install-retry-stop-safe"),
        )
        conn.execute(
            "UPDATE mexc_canary_positions SET volume_contracts=100,current_stop=98,"
            "original_stop=98,tp3=110 WHERE decision_id='tp-install-retry-stop-safe'"
        )
        conn.commit()

    class SecondTpTemporarilyInvisible(FakePrivateClient):
        def __init__(self):
            super().__init__()
            self.tpsl = [{
                "id": 88, "positionId": 77, "state": 1,
                "stopLossPrice": 98.0, "takeProfitPrice": 0, "vol": 100,
            }]
            self.emergency_calls = 0
            self.cancel_calls = 0

        def open_positions(self, symbol=None):
            return [{
                "positionId": 77, "symbol": "BTC_USDT", "holdVol": 100,
                "positionType": 1, "openType": 1, "state": 1,
                "openAvgPrice": 100.0, "liquidatePrice": 90.0, "leverage": 10,
            }]

        def order_by_id(self, order_id):
            order = super().order_by_id(order_id)
            if str(order.get("externalOid") or "").startswith("tp2_"):
                raise MexcAPIError("MEXC external order missing")
            return order

        def order_by_external_id(self, symbol, external_oid):
            if str(external_oid).startswith("tp2_"):
                raise MexcAPIError("MEXC external order missing")
            for order in self.close_limits:
                if str(order.get("externalOid") or "") == str(external_oid):
                    return dict(order)
            raise MexcAPIError("MEXC external order missing")

        def cancel_order_ids(self, order_ids):
            self.cancel_calls += 1
            return super().cancel_order_ids(order_ids)

        def emergency_close_long(self, **kwargs):
            self.emergency_calls += 1
            raise AssertionError("verified stop must keep position open during TP visibility lag")

    fake = SecondTpTemporarilyInvisible()
    local = {
        "decision_id": "tp-install-retry-stop-safe", "exchange_position_id": "77",
        "symbol": "BTC_USDT", "direction": "long", "current_stop": 98.0,
        "volume_contracts": 100.0, "plan_json": json.dumps({
            "direction": "long", "tp1": 103.0, "tp2": 106.0, "tp3": 110.0,
            "price_tick": 0.01, "volume_step": 1.0, "min_volume": 1.0,
            "leverage": 10, "open_type": 1,
        }),
    }

    fallback_stop, observed = _install_or_reconcile_exit_legs(
        path=store.db_path, client=fake, local=local, pos={"holdVol": 100},
        cfg=cfg(
            exit_visibility_timeout_seconds=0,
            exit_visibility_poll_seconds=0.01,
            position_reconcile_error_event_cooldown_seconds=0,
        ),
    )

    assert fallback_stop["id"] == 88
    assert len(observed) == 1
    assert fake.emergency_calls == 0
    assert fake.cancel_calls == 0
    with store.connect() as conn:
        assert ls.kill_switch_state(conn) == "CLEAR"
        assert conn.execute(
            "SELECT COUNT(*) FROM mexc_canary_exit_legs WHERE decision_id=?",
            ("tp-install-retry-stop-safe",),
        ).fetchone()[0] == 1
        assert conn.execute(
            "SELECT 1 FROM mexc_canary_events WHERE decision_id=? "
            "AND event_type='MEXC_THREE_TP_INSTALL_FAILED'",
            ("tp-install-retry-stop-safe",),
        ).fetchone() is None
        event = conn.execute(
            "SELECT payload_json FROM mexc_canary_events WHERE decision_id=? "
            "AND event_type='MEXC_TP_INSTALL_INCOMPLETE_RETRYING'",
            ("tp-install-retry-stop-safe",),
        ).fetchone()
    assert event is not None
    assert json.loads(event["payload_json"])["action"] == (
        "kept_position_open_because_fallback_stop_is_verified"
    )


def test_tp_install_failure_diagnostic_surfaces_the_swallowed_create_error(tmp_path):
    # Regression: the leg loop used to discard client.place_close_limit()'s own
    # exception entirely (`except Exception: submitted = {}`), so a bounded
    # verification failure never revealed whether MEXC actually rejected the
    # create call or the read side merely lagged. This is what made the real
    # 2026-09-05 LTC/MUBARAK incident unexplainable after the fact -- the
    # persisted MEXC_THREE_TP_INSTALL_FAILED event only ever showed the
    # secondary "not visible" symptom.
    store = make_db(tmp_path / "tp-install-create-error.sqlite")
    opened = "2026-07-17T00:00:00+00:00"
    _seed_open_canary_position(
        store, decision_id="tp-install-create-error", opened_at=opened,
        tpsl_order_id=None, tp_legs=0,
    )
    plan = {
        "direction": "long", "tp1": 103.0, "tp2": 106.0, "tp3": 110.0,
        "price_tick": 0.01, "volume_step": 1.0, "min_volume": 1.0,
        "leverage": 10, "open_type": 1,
    }
    with store.connect() as conn:
        conn.execute(
            "UPDATE mexc_canary_orders SET plan_json=? WHERE decision_id=?",
            (json.dumps(plan), "tp-install-create-error"),
        )
        conn.execute(
            "UPDATE mexc_canary_positions SET volume_contracts=100,current_stop=98,"
            "original_stop=98,tp3=110 WHERE decision_id='tp-install-create-error'"
        )
        conn.commit()

    class SecondLegCreateRejected(FakePrivateClient):
        def place_close_limit(self, **kwargs):
            if kwargs["price"] == 106.0:  # tp2
                raise MexcAPIError("MEXC request rejected: risk limit exceeded")
            return super().place_close_limit(**kwargs)

        def order_by_id(self, order_id):
            order = super().order_by_id(order_id)
            if str(order.get("externalOid") or "").startswith("tp2_"):
                raise MexcAPIError("MEXC external order missing")
            return order

        def order_by_external_id(self, symbol, external_oid):
            if str(external_oid).startswith("tp2_"):
                raise MexcAPIError("MEXC external order missing")
            for order in self.close_limits:
                if str(order.get("externalOid") or "") == str(external_oid):
                    return dict(order)
            raise MexcAPIError("MEXC external order missing")

    fake = SecondLegCreateRejected()
    local = {
        "decision_id": "tp-install-create-error", "exchange_position_id": "77",
        "symbol": "BTC_USDT", "direction": "long", "current_stop": 98.0,
        "volume_contracts": 100.0, "plan_json": json.dumps(plan),
    }

    with pytest.raises(MexcAPIError):
        _install_or_reconcile_exit_legs(
            path=store.db_path, client=fake, local=local, pos={"holdVol": 100},
            cfg=cfg(
                exit_visibility_timeout_seconds=0, exit_visibility_poll_seconds=0.01,
                partial_take_profit={
                    "enabled": True, "native_limit_legs": 2,
                    "keep_open_on_tp_install_failure_with_verified_stop": False,
                },
            ),
        )

    with store.connect() as conn:
        event = conn.execute(
            "SELECT payload_json FROM mexc_canary_events WHERE decision_id=? "
            "AND event_type='MEXC_THREE_TP_INSTALL_FAILED'",
            ("tp-install-create-error",),
        ).fetchone()
    assert event is not None
    payload = json.loads(event["payload_json"])
    assert payload["failed_leg"] == 2
    assert "risk limit exceeded" in payload["create_call_errors"]["2"]
    assert payload["action"] == "emergency_close_because_no_verified_fallback_stop"


def test_fake_live_short_submit_install_three_tps_and_move_profit_stop(tmp_path, monkeypatch):
    monkeypatch.setenv("MEXC_CANARY_ACCESS_KEY", "dummy-access")
    monkeypatch.setenv("MEXC_CANARY_SECRET", "dummy-secret")
    monkeypatch.setenv("MEXC_LIVE_CANARY_ARMED", "I_UNDERSTAND_REAL_MEXC_ORDERS")
    live_cfg = cfg(submission_enabled=True, execution_mode="live")
    store = make_db(tmp_path / "short-live.sqlite")
    short_signal = {**signal(), "direction": "short"}
    captured = capture_paper_candidate(
        store=store, signal=short_signal,
        payload=payload(stop=102.0, tp1=97.0, tp2=94.0, tp3=90.0), cfg=live_cfg,
    )
    fake = FakePrivateClient(direction="short")
    submitted = worker_once(db=store.db_path, cfg=live_cfg, client=fake)
    assert captured["queued"] is True
    assert submitted["status"] == "SUBMITTED"
    assert fake.created[0]["side"] == 3
    with store.connect() as conn:
        filled_plan = json.loads(conn.execute(
            "SELECT plan_json FROM mexc_canary_orders WHERE decision_id=?",
            (captured["decision_id"],),
        ).fetchone()[0])
    assert [item["price"] for item in fake.close_limits] == [
        filled_plan["tp1"], filled_plan["tp2"],
    ]
    assert fake.tpsl[0]["stopLossPrice"] == 100.0
    with store.connect() as conn:
        position = conn.execute("SELECT direction,protection_stage,current_stop FROM mexc_canary_positions").fetchone()
    assert tuple(position) == ("short", "BREAKEVEN", 100.0)


def test_live_exit_install_tolerates_delayed_mexc_stop_and_tp_visibility(tmp_path, monkeypatch):
    """MEXC can accept writes before its read endpoints expose them."""
    class DelayedVisibilityFake(FakePrivateClient):
        def __init__(self):
            super().__init__()
            self.stop_reads_hidden = 2
            self.tp_reads_hidden = 4

        def open_tpsl_orders(self, symbol=None):
            if self.stop_reads_hidden:
                self.stop_reads_hidden -= 1
                return []
            return super().open_tpsl_orders(symbol)

        def order_by_id(self, order_id):
            if self.tp_reads_hidden:
                self.tp_reads_hidden -= 1
                raise MexcAPIError("MEXC order not visible yet")
            return super().order_by_id(order_id)

        def order_by_external_id(self, symbol, external_oid):
            if external_oid.startswith("tp"):
                if self.tp_reads_hidden:
                    raise MexcAPIError("MEXC external order not visible yet")
                return dict(next(
                    item for item in self.close_limits if item["externalOid"] == external_oid
                ))
            return super().order_by_external_id(symbol, external_oid)

    monkeypatch.setenv("MEXC_CANARY_ACCESS_KEY", "dummy-access")
    monkeypatch.setenv("MEXC_CANARY_SECRET", "dummy-secret")
    monkeypatch.setenv("MEXC_LIVE_CANARY_ARMED", "I_UNDERSTAND_REAL_MEXC_ORDERS")
    live_cfg = cfg(
        submission_enabled=True, execution_mode="live",
        exit_visibility_timeout_seconds=0.5,
        exit_visibility_poll_seconds=0.01,
        exit_visibility_transient_backoff_seconds=0.01,
    )
    store = make_db(tmp_path / "delayed.sqlite")
    capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=live_cfg)
    fake = DelayedVisibilityFake()

    result = worker_once(db=store.db_path, cfg=live_cfg, client=fake)

    assert result["status"] == "SUBMITTED"
    assert result["protection"]["errors"] == []
    assert len(fake.close_limits) == 2
    with store.connect() as conn:
        assert ls.kill_switch_state(conn) == "CLEAR"
        assert conn.execute("SELECT COUNT(*) FROM mexc_canary_exit_legs").fetchone()[0] == 3


def test_live_exit_install_waits_for_slow_third_tp_without_kill_switch(tmp_path, monkeypatch):
    class SlowThirdTpFake(FakePrivateClient):
        def __init__(self):
            super().__init__()
            self.third_tp_hidden_reads = 5

        def _is_third_tp(self, order_id=None, external_oid=None):
            for item in self.close_limits:
                if (
                    (order_id is not None and str(item["orderId"]) == str(order_id))
                    or (external_oid is not None and item["externalOid"] == external_oid)
                ):
                    return item["externalOid"].startswith("tp3_")
            return bool(str(external_oid or "").startswith("tp3_"))

        def order_by_id(self, order_id):
            if self._is_third_tp(order_id=order_id) and self.third_tp_hidden_reads:
                self.third_tp_hidden_reads -= 1
                raise MexcAPIError("Requests are too frequent", status_code=429)
            return super().order_by_id(order_id)

        def order_by_external_id(self, symbol, external_oid):
            if self._is_third_tp(external_oid=external_oid) and self.third_tp_hidden_reads:
                raise MexcAPIError("MEXC external order missing")
            if external_oid.startswith("tp"):
                return dict(next(
                    item for item in self.close_limits if item["externalOid"] == external_oid
                ))
            return super().order_by_external_id(symbol, external_oid)

    monkeypatch.setenv("MEXC_CANARY_ACCESS_KEY", "dummy-access")
    monkeypatch.setenv("MEXC_CANARY_SECRET", "dummy-secret")
    monkeypatch.setenv("MEXC_LIVE_CANARY_ARMED", "I_UNDERSTAND_REAL_MEXC_ORDERS")
    live_cfg = cfg(
        submission_enabled=True, execution_mode="live",
        partial_take_profit={
            **(cfg().get("partial_take_profit", {}) or {}),
            "native_limit_legs": 3,
        },
        exit_visibility_timeout_seconds=1.0,
        exit_visibility_poll_seconds=0.01,
        exit_visibility_transient_backoff_seconds=0.01,
    )
    store = make_db(tmp_path / "slow-third-tp.sqlite")
    capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=live_cfg)
    fake = SlowThirdTpFake()

    result = worker_once(db=store.db_path, cfg=live_cfg, client=fake)

    assert result["status"] == "SUBMITTED"
    assert result["protection"]["errors"] == []
    assert fake.third_tp_hidden_reads == 0
    with store.connect() as conn:
        assert ls.kill_switch_state(conn) == "CLEAR"
        assert conn.execute(
            "SELECT COUNT(*) FROM mexc_canary_exit_legs WHERE order_kind='CLOSE_LIMIT_TP'"
        ).fetchone()[0] == 3


def test_live_exit_install_creates_explicit_stop_when_attached_stop_never_appears(tmp_path, monkeypatch):
    class MissingAttachedStopFake(FakePrivateClient):
        def __init__(self):
            super().__init__()
            self.explicit_stop_calls = 0
            self.explicit_stop_visible = False

        def create_order(self, order):
            result = super().create_order(order)
            if order.get("side") in {1, 3}:
                self.tpsl = []
            return result

        def place_position_tpsl(self, **kwargs):
            self.explicit_stop_calls += 1
            self.explicit_stop_visible = True
            return super().place_position_tpsl(**kwargs)

        def open_tpsl_orders(self, symbol=None):
            return super().open_tpsl_orders(symbol) if self.explicit_stop_visible else []

    monkeypatch.setenv("MEXC_CANARY_ACCESS_KEY", "dummy-access")
    monkeypatch.setenv("MEXC_CANARY_SECRET", "dummy-secret")
    monkeypatch.setenv("MEXC_LIVE_CANARY_ARMED", "I_UNDERSTAND_REAL_MEXC_ORDERS")
    live_cfg = cfg(submission_enabled=True, execution_mode="live",
                   exit_visibility_timeout_seconds=0, exit_visibility_poll_seconds=0.01)
    store = make_db(tmp_path / "explicit-stop.sqlite")
    capture_paper_candidate(store=store, signal=signal(), payload=payload(), cfg=live_cfg)
    fake = MissingAttachedStopFake()

    result = worker_once(db=store.db_path, cfg=live_cfg, client=fake)

    assert result["status"] == "SUBMITTED"
    assert fake.explicit_stop_calls == 1
    assert len(fake.tpsl) == 1
    assert fake.tpsl[0]["takeProfitPrice"] is None
    with store.connect() as conn:
        assert ls.kill_switch_state(conn) == "CLEAR"


def test_partial_tp_split_is_exact_and_rejects_too_small_positions():
    assert allocate_partial_tp_volumes(
        total_volume=14, volume_step=1, min_volume=1, weights=(0.33, 0.33, 0.34),
    ) == (4.0, 5.0, 5.0)
    with pytest.raises(PlanRejected, match="PARTIAL_TP_VOLUME_TOO_SMALL"):
        allocate_partial_tp_volumes(
            total_volume=2, volume_step=1, min_volume=1, weights=(0.33, 0.33, 0.34),
        )


def test_model_f_stop_is_monotonic():
    c = cfg()
    assert model_f_stop(entry=100, original_stop=98, highest_price=100.5, cfg=c)[:2] == (
        "ORIGINAL_STOP", 98)
    assert model_f_stop(entry=100, original_stop=98, highest_price=101.2, cfg=c)[:2] == (
        "BREAKEVEN", 100)
    assert model_f_stop(entry=100, original_stop=98, highest_price=102.0, cfg=c)[:2] == (
        "PROFIT_LOCK", 101)


def test_short_order_plan_uses_bid_open_short_and_mirrored_model_f():
    decision = {
        "decision_id": "short-decision", "signal_id": "short-signal", "symbol": "BTC_USDT",
        "direction": "short", "entry_mode": "BREAKOUT_CONTINUATION", "entry_price": 100.0,
        "original_stop": 102.0, "tp1": 97.0, "tp2": 94.0, "tp3": 90.0,
        "live_risk_multiplier": 1.0,
    }
    plan = build_order_plan(decision=decision, contract=contract(), depth=depth(), cfg=cfg())
    assert plan.direction == "short"
    assert plan.side == 3
    assert plan.limit_price <= plan.current_bid
    assert plan.mexc_order()["side"] == 3
    assert plan.actual_risk_usdt <= 10.0
    assert plan.estimated_liquidation_price > plan.original_stop
    assert model_f_stop(
        entry=100, original_stop=102, favorable_price=99.5, direction="short", cfg=cfg(),
    )[:2] == ("ORIGINAL_STOP", 102)
    assert model_f_stop(
        entry=100, original_stop=102, favorable_price=98.8, direction="short", cfg=cfg(),
    )[:2] == ("BREAKEVEN", 100)
    assert model_f_stop(
        entry=100, original_stop=102, favorable_price=98.0, direction="short", cfg=cfg(),
    )[:2] == ("PROFIT_LOCK", 99)


def test_mexc_signature_and_symbol_are_deterministic():
    sig = MexcFuturesClient.signature("access", "secret", "123", '{"symbol":"BTC_USDT"}')
    assert sig == MexcFuturesClient.signature("access", "secret", "123", '{"symbol":"BTC_USDT"}')
    assert len(sig) == 64
    assert MexcFuturesClient.native_symbol("btc/usdt") == "BTC_USDT"
    assert MexcFuturesClient._query_string({"b": 2, "a": 1}) == "a=1&b=2"


def test_mexc_client_retries_safe_get_after_transport_timeout():
    class Response:
        status_code = 200

        @staticmethod
        def json():
            return {"success": True, "data": {"symbol": "BTC_USDT"}}

    class Session:
        def __init__(self):
            self.calls = []

        def request(self, method, *args, **kwargs):
            self.calls.append(method)
            if len(self.calls) == 1:
                raise requests.ReadTimeout("temporary timeout")
            return Response()

    session = Session()
    client = MexcFuturesClient(
        session=session, safe_read_retry_attempts=2,
        safe_read_retry_backoff_seconds=0,
    )
    assert client.contract_info("BTC_USDT")["symbol"] == "BTC_USDT"
    assert session.calls == ["GET", "GET"]


def test_mexc_client_never_retries_post_submission_timeout():
    class Session:
        def __init__(self):
            self.calls = []

        def request(self, method, *args, **kwargs):
            self.calls.append(method)
            raise requests.ReadTimeout("submit timeout")

    session = Session()
    client = MexcFuturesClient(
        access_key="access", secret_key="secret", session=session,
        safe_read_retry_attempts=3, safe_read_retry_backoff_seconds=0,
    )
    with pytest.raises(MexcAPIError, match="ReadTimeout"):
        client.create_order({"symbol": "BTC_USDT"})
    assert session.calls == ["POST"]


def test_contract_info_uses_documented_detail_endpoint(monkeypatch):
    client = MexcFuturesClient()
    captured = {}

    def fake_request(method, path, **kwargs):
        captured.update({"method": method, "path": path, **kwargs})
        return {"symbol": "PUMPFUN_USDT", "state": 0, "apiAllowed": True}

    monkeypatch.setattr(client, "_request", fake_request)
    result = client.contract_info("PUMPFUN_USDT")
    assert result["symbol"] == "PUMPFUN_USDT"
    assert captured["path"] == "/api/v1/contract/detail"
    assert captured["params"] == {"symbol": "PUMPFUN_USDT"}


def test_create_order_uses_documented_futures_submit_endpoint(monkeypatch):
    client = MexcFuturesClient(access_key="access", secret_key="secret")
    captured = {}

    def fake_request(method, path, **kwargs):
        captured.update({"method": method, "path": path, **kwargs})
        return {"orderId": "123"}

    monkeypatch.setattr(client, "_request", fake_request)
    assert client.create_order({"symbol": "BTC_USDT"})["orderId"] == "123"
    assert captured["method"] == "POST"
    assert captured["path"] == "/api/v1/private/order/submit"
    assert captured["private"] is True


def test_create_order_normalizes_documented_scalar_order_id(monkeypatch):
    client = MexcFuturesClient(access_key="access", secret_key="secret")
    monkeypatch.setattr(client, "_request", lambda *_args, **_kwargs: 123456789)
    assert client.create_order({"symbol": "BTC_USDT"}) == {"orderId": "123456789"}


def test_mexc_kline_normalization(monkeypatch):
    client = MexcFuturesClient()
    monkeypatch.setattr(client, "_request", lambda *_args, **_kwargs: {
        "time": [2, 1], "open": [101, 100], "high": [102, 101],
        "low": [100, 99], "close": [101.5, 100.5],
    })
    assert client.klines("BTC/USDT", start_seconds=1, end_seconds=2) == [
        {"candle_at": 2, "open": 101.0, "high": 102.0, "low": 100.0, "close": 101.5},
        {"candle_at": 1, "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.5},
    ]


def test_cancel_external_uses_live_singular_payload(monkeypatch):
    client = MexcFuturesClient(access_key="a", secret_key="s")
    captured = {}

    def fake_request(method, path, **kwargs):
        captured.update({"method": method, "path": path, **kwargs})
        return {"orderId": "1", "errorCode": 0, "errorMsg": "success"}

    monkeypatch.setattr(client, "_request", fake_request)
    result = client.cancel_external("BTC/USDT", "probe-1")
    assert result["errorCode"] == 0
    assert captured["body"] == {"symbol": "BTC_USDT", "externalOid": "probe-1"}
    assert captured["private"] is True


def test_cancel_tpsl_uses_documented_stop_plan_payload(monkeypatch):
    client = MexcFuturesClient(access_key="a", secret_key="s")
    captured = {}

    def fake_request(method, path, **kwargs):
        captured.update({"method": method, "path": path, **kwargs})
        return True

    monkeypatch.setattr(client, "_request", fake_request)
    client.cancel_tpsl_order_ids([11, "12"])
    assert captured["path"] == "/api/v1/private/stoporder/cancel"
    assert captured["body"] == [{"stopPlanOrderId": 11}, {"stopPlanOrderId": 12}]
    assert captured["private"] is True


def test_emergency_close_short_uses_mexc_close_short_side(monkeypatch):
    client = MexcFuturesClient(access_key="a", secret_key="s")
    captured = {}

    def fake_create(order):
        captured.update(order)
        return {"orderId": "42"}

    monkeypatch.setattr(client, "create_order", fake_create)
    client.emergency_close_short(
        symbol="BTC/USDT", position_id=77, volume=3, external_oid="close-short",
    )
    assert captured["symbol"] == "BTC_USDT"
    assert captured["side"] == 2
    assert captured["type"] == 5
    assert captured["positionId"] == 77


def test_scheduler_contains_dedicated_background_canary():
    from scripts.run_default_market_schedule import build_cycle_steps
    steps = build_cycle_steps(now=datetime(2026, 7, 17, 12, tzinfo=timezone.utc),
                              crypto_only=True, include_long_horizon=False,
                              monitor_minutes=10, skip_reports=False)
    selected = [s for s in steps if s[2] == "mexc_canary_monitor"]
    assert len(selected) == 1
    assert "mexc-canary-monitor" in selected[0][1]


def test_scheduler_refreshes_mexc_parity_as_a_nonfatal_read_model_step():
    from scripts.run_default_market_schedule import build_cycle_steps
    steps = build_cycle_steps(now=datetime(2026, 7, 17, 12, tzinfo=timezone.utc),
                              crypto_only=True, include_long_horizon=False,
                              monitor_minutes=10, skip_reports=False)
    selected = [step for step in steps if "MEXC parity exits" in step[0]]
    assert len(selected) == 1
    assert selected[0][2] == "command_nonfatal"
    assert "mexc-parity-refresh" in selected[0][1]


def test_scheduler_contains_post_track_mexc_execution_watchdog():
    from scripts.run_default_market_schedule import build_cycle_steps
    steps = build_cycle_steps(now=datetime(2026, 7, 17, 12, tzinfo=timezone.utc),
                              crypto_only=True, include_long_horizon=False,
                              monitor_minutes=10, skip_reports=False)
    selected = [step for step in steps if "MEXC live execution watchdog" in step[0]]
    assert len(selected) == 1
    assert selected[0][2] == "command_nonfatal"
    assert "mexc-canary-watchdog" in selected[0][1]
    assert "--no-repair" in selected[0][1]
    assert "--send-telegram" in selected[0][1]
