from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone

from src.live_execution import store as ls
from src.live_execution.config import LiveCanaryConfig, load_live_canary_config
from src.live_execution.mexc_client import MexcAPIError
from src.live_execution.mexc_parity import refresh, simulate_profile


def _cfg() -> LiveCanaryConfig:
    return LiveCanaryConfig(raw=load_live_canary_config().raw)


def _decision(base: datetime) -> dict:
    return {
        "signal_id": "sig-parity-1",
        "entry_triggered_at": base.isoformat(),
        "captured_at": base.isoformat(),
        "entry_price": 100.0,
        "original_stop": 98.0,
        "tp1": 102.4,
        "tp2": 104.4,
        "tp3": 106.4,
    }


def _plan() -> dict:
    return {
        "reference_entry": 100.0,
        "original_stop": 98.0,
        "tp3": 106.4,
        "actual_risk_usdt": 2.0,
        "notional_usdt": 100.0,
        "taker_fee_rate": 0.0008,
        "slippage_rate": 0.0005,
    }


def test_parity_uses_contract_geometry_not_all_in_stop_risk_for_gross_pnl():
    base = datetime(2026, 7, 21, tzinfo=timezone.utc)
    plan = {
        **_plan(), "volume_contracts": 10.0, "contract_size": 0.01,
        # All-in stop risk must not be used as a position-size proxy.
        "actual_risk_usdt": 99.0,
    }
    result = simulate_profile(
        candles=[_candle(base + timedelta(minutes=1), 102.5, 101.4),
                 _candle(base + timedelta(minutes=2), 101.8, 100.9)],
        decision=_decision(base), plan=plan,
        profile_id="mexc_model_f_runner_v1", partial_weights=None,
        now=base + timedelta(minutes=3), live_cfg=_cfg(),
    )
    assert result["gross_pnl_usdt"] < 1.0


def _candle(at: datetime, high: float, low: float) -> dict:
    return {"candle_at": int(at.timestamp()), "open": 100.0,
            "high": high, "low": low, "close": 101.0}


def test_partial_tp_shadow_can_outperform_model_f_runner_on_same_mexc_path():
    base = datetime(2026, 7, 21, tzinfo=timezone.utc)
    candles = [
        _candle(base + timedelta(minutes=1), 102.5, 101.4),
        _candle(base + timedelta(minutes=2), 101.8, 100.9),
    ]
    baseline = simulate_profile(
        candles=candles, decision=_decision(base), plan=_plan(),
        profile_id="mexc_model_f_runner_v1", partial_weights=None,
        now=base + timedelta(minutes=3), live_cfg=_cfg(),
    )
    partial = simulate_profile(
        candles=candles, decision=_decision(base), plan=_plan(),
        profile_id="mexc_partial_tp_33_33_34_v1", partial_weights=(0.33, 0.33, 0.34),
        now=base + timedelta(minutes=3), live_cfg=_cfg(),
    )
    assert baseline["status"] == partial["status"] == "CLOSED"
    assert baseline["close_reason"] == "model_f_stop"
    assert partial["execution_json"]["exits"][0]["reason"] == "tp1_partial"
    assert partial["net_pnl_usdt"] > baseline["net_pnl_usdt"]


def test_intrabar_stop_and_new_protection_are_excluded_not_credited():
    base = datetime(2026, 7, 21, tzinfo=timezone.utc)
    result = simulate_profile(
        candles=[_candle(base + timedelta(minutes=1), 102.5, 100.9)],
        decision=_decision(base), plan=_plan(), profile_id="mexc_model_f_runner_v1",
        partial_weights=None, now=base + timedelta(minutes=2), live_cfg=_cfg(),
    )
    assert result["status"] == "AMBIGUOUS_INTRABAR"
    assert result["clean"] == 0
    assert result["net_pnl_usdt"] is None


def test_short_partial_tp_path_is_directional_and_uses_positive_short_pnl():
    base = datetime(2026, 7, 21, tzinfo=timezone.utc)
    decision = {
        **_decision(base), "direction": "short", "original_stop": 102.0,
        "tp1": 97.0, "tp2": 94.0, "tp3": 90.0,
    }
    plan = {**_plan(), "direction": "short", "original_stop": 102.0, "tp3": 90.0}
    candles = [
        _candle(base + timedelta(minutes=1), 98.8, 96.8),
        _candle(base + timedelta(minutes=2), 96.9, 93.8),
        _candle(base + timedelta(minutes=3), 93.9, 89.8),
    ]
    result = simulate_profile(
        candles=candles, decision=decision, plan=plan,
        profile_id="mexc_partial_tp_33_33_34_v1", partial_weights=(0.33, 0.33, 0.34),
        now=base + timedelta(minutes=4), live_cfg=_cfg(),
    )
    assert result["status"] == "CLOSED"
    assert result["clean"] == 1
    assert result["net_pnl_usdt"] > 0
    assert [exit["reason"] for exit in result["execution_json"]["exits"]] == [
        "tp1_partial", "tp2_partial", "tp3_runner",
    ]


class _FakeMexcClient:
    def klines(self, symbol, *, start_seconds, end_seconds, interval):
        start = datetime.fromtimestamp(start_seconds, timezone.utc)
        return [
            _candle(start + timedelta(minutes=1), 102.5, 101.4),
            _candle(start + timedelta(minutes=2), 101.8, 100.9),
        ]


class _FailingMexcClient:
    def klines(self, symbol, *, start_seconds, end_seconds, interval):
        raise MexcAPIError("MEXC transport error: ReadTimeout")


def _seed_plan(path, base: datetime) -> None:
    with ls.connect(path) as conn:
        ls.ensure_tables(conn)
        decision = _decision(base)
        conn.execute(
            "INSERT INTO mexc_canary_decisions "
            "(decision_id,signal_id,captured_at,paper_alert_id,symbol,mode,entry_mode,eligible,state,"
            "rejection_reasons_json,decision_json,decision_hash,config_hash,decision_context_type) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("d-parity-1", "sig-parity-1", base.isoformat(), None, "BTC_USDT", "swing",
             "PULLBACK_LIMIT", 1, "QUEUED", "[]", json.dumps(decision), "hash", "cfg",
             "point_in_time"),
        )
        ls.upsert_parity_plan(
            conn, decision_id="d-parity-1", signal_id="sig-parity-1", symbol="BTC_USDT",
            plan=_plan(), source="test", captured_at=base.isoformat(),
        )
        conn.commit()


def test_refresh_isolated_from_paper_and_live_tables(tmp_path):
    path = tmp_path / "parity.sqlite"
    base = datetime(2026, 7, 21, tzinfo=timezone.utc)
    with sqlite3.connect(path) as conn:
        conn.executescript("""
            CREATE TABLE proposed_signals(signal_id TEXT PRIMARY KEY);
            CREATE TABLE signal_outcomes(id INTEGER PRIMARY KEY, final_r REAL);
            CREATE TABLE paper_portfolio_ledger(id INTEGER PRIMARY KEY);
        """)
        conn.execute("INSERT INTO proposed_signals VALUES('unchanged')")
        conn.execute("INSERT INTO signal_outcomes VALUES(1, 7.0)")
        conn.execute("INSERT INTO paper_portfolio_ledger VALUES(1)")
    _seed_plan(path, base)
    result = refresh(db=path, client=_FakeMexcClient(), now=base + timedelta(minutes=3))
    assert result["status"] == "OK"
    assert result["outcomes"] == 2
    with ls.connect(path) as conn:
        assert conn.execute("SELECT COUNT(*) FROM proposed_signals").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM signal_outcomes").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM paper_portfolio_ledger").fetchone()[0] == 1
        rows = conn.execute(
            "SELECT profile_id,status FROM mexc_canary_parity_outcomes ORDER BY profile_id"
        ).fetchall()
    assert [tuple(row) for row in rows] == [
        ("mexc_model_f_runner_v1", "CLOSED"),
        ("mexc_partial_tp_33_33_34_v1", "CLOSED"),
    ]


def test_refresh_backfills_only_existing_immutable_canary_plans(tmp_path):
    path = tmp_path / "legacy-plan.sqlite"
    base = datetime(2026, 7, 21, tzinfo=timezone.utc)
    _seed_plan(path, base)
    with ls.connect(path) as conn:
        conn.execute("DELETE FROM mexc_canary_parity_plans")
        conn.execute(
            "INSERT INTO mexc_canary_orders "
            "(order_row_id,decision_id,external_oid,exchange_order_id,symbol,status,submitted_at,updated_at,"
            "plan_json,exchange_json,last_error) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            ("order-1", "d-parity-1", "external-1", "exchange-1", "BTC_USDT", "FILLED",
             base.isoformat(), base.isoformat(), json.dumps(_plan()), "{}", None),
        )
        conn.commit()
    result = refresh(db=path, client=_FakeMexcClient(), now=base + timedelta(minutes=3))
    assert result["plans"] == 1
    with ls.connect(path) as conn:
        row = conn.execute("SELECT source FROM mexc_canary_parity_plans").fetchone()
    assert row[0] == "existing_canary_order"


def test_refresh_skips_one_transient_source_error_without_failing_cycle(tmp_path):
    path = tmp_path / "source-error.sqlite"
    base = datetime(2026, 7, 21, tzinfo=timezone.utc)
    _seed_plan(path, base)

    result = refresh(
        db=path,
        client=_FailingMexcClient(),
        now=base + timedelta(minutes=3),
    )

    assert result["status"] == "OK"
    assert result["plans"] == 1
    assert result["outcomes"] == 0
    assert result["skipped_source_error"] == 1
