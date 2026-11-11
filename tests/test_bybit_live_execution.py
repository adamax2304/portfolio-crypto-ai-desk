from __future__ import annotations

import json
import sqlite3
import time
from copy import deepcopy

from src.live_execution import store as ls
from src.live_execution.bybit_client import BybitAPIError, BybitFuturesClient
from src.live_execution.bybit_execution import reconcile_once
from src.live_execution.config import LiveCanaryConfig, load_live_canary_config
from src.live_execution.service import _is_definitive_bybit_submission_rejection
from src.live_execution.venue_router import prepare_candidate, select_candidate


def _raw() -> dict:
    raw = deepcopy(load_live_canary_config().raw)
    raw["submission_enabled"] = True
    raw["execution_mode"] = "live"
    raw["venue_routing"] = {
        "enabled": True,
        "preference_order": ["mexc", "bybit"],
        "min_cost_improvement_bps": 2.0,
        "bybit": {
            "enabled": True, "submission_enabled": True,
            "fallback_maker_fee_rate": 0.0002,
            "fallback_taker_fee_rate": 0.00055,
            "credentials": {
                "access_key_env": "TEST_BYBIT_KEY", "secret_key_env": "TEST_BYBIT_SECRET",
                "arm_env": "TEST_BYBIT_ARM", "arm_value": "ARMED",
            },
        },
    }
    raw["credentials"] = {
        "access_key_env": "TEST_MEXC_KEY", "secret_key_env": "TEST_MEXC_SECRET",
        "arm_env": "TEST_MEXC_ARM", "arm_value": "ARMED",
    }
    return raw


def _arm(monkeypatch) -> LiveCanaryConfig:
    for name in ("TEST_BYBIT_KEY", "TEST_BYBIT_SECRET", "TEST_MEXC_KEY", "TEST_MEXC_SECRET"):
        monkeypatch.setenv(name, "x")
    monkeypatch.setenv("TEST_BYBIT_ARM", "ARMED")
    monkeypatch.setenv("TEST_MEXC_ARM", "ARMED")
    return LiveCanaryConfig(raw=_raw())


def _contract(symbol: str, *, venue: str) -> dict:
    return {
        "symbol": symbol, "state": 0, "apiAllowed": True, "futureType": 1,
        "quoteCoin": "USDT", "preMarket": False, "typeLabel": 0,
        "contractSize": 1.0, "priceUnit": 0.01, "volUnit": 0.01, "minVol": 0.01,
        "maxVol": 100000.0, "limitMaxVol": 100000.0, "minLeverage": 1,
        "maxLeverage": 100, "countryConfigContractMaxLeverage": 0,
        "makerFeeRate": 0.0002 if venue == "bybit" else 0.0006,
        "takerFeeRate": 0.00055 if venue == "bybit" else 0.0008,
        "maintenanceMarginRate": 0.005, "liquidationFeeRate": 0.0,
    }


class VenueFake:
    def __init__(self, venue: str, ask: float, bid: float, *, missing: bool = False,
                 delay_seconds: float = 0.0):
        self.venue, self.ask, self.bid, self.missing = venue, ask, bid, missing
        self.delay_seconds = delay_seconds

    def contract_info(self, symbol):
        if self.delay_seconds:
            time.sleep(self.delay_seconds)
        if self.missing:
            raise BybitAPIError("contract metadata missing")
        native = "BTCUSDT" if self.venue == "bybit" else "BTC_USDT"
        return _contract(native, venue=self.venue)

    def depth(self, symbol, limit=20):
        return {"asks": [[self.ask, 1000]], "bids": [[self.bid, 1000]]}

    def account_asset(self, currency="USDT"):
        return {"equity": 1000, "availableOpen": 1000}


def _decision() -> dict:
    return {
        "decision_id": "decision-1", "signal_id": "signal-1", "symbol": "BTC/USDT",
        "asset_class": "crypto", "mode": "swing", "entry_mode": "PULLBACK_LIMIT",
        "direction": "long", "entry_price": 100.0, "original_stop": 98.0,
        "tp1": 103.0, "tp2": 106.0, "tp3": 110.0, "live_risk_multiplier": 0.5,
        "risk_bucket": "crypto_swing",
    }


def test_router_selects_materially_better_bybit(monkeypatch):
    cfg = _arm(monkeypatch)
    chosen, diagnostic = select_candidate(
        decision=_decision(), cfg=cfg, captured_at="2026-08-18T00:00:00+00:00",
        mexc_override=VenueFake("mexc", 100.0, 99.95),
        bybit_override=VenueFake("bybit", 99.8, 99.79),
    )
    assert chosen.venue == "bybit"
    assert set(diagnostic["candidates"]) == {"mexc", "bybit"}


def test_bybit_legacy_environment_names_are_supported_but_still_require_arm(monkeypatch):
    raw = _raw()
    cfg = LiveCanaryConfig(raw=raw)
    monkeypatch.delenv("TEST_BYBIT_KEY", raising=False)
    monkeypatch.delenv("TEST_BYBIT_SECRET", raising=False)
    monkeypatch.setenv("BYBIT_API_KEY", "legacy-key")
    monkeypatch.setenv("BYBIT_API_SECRET", "legacy-secret")
    assert cfg.bybit_credentials() == ("legacy-key", "legacy-secret")
    assert cfg.bybit_credentials_present() is True
    assert cfg.bybit_live_armed() is False
    monkeypatch.setenv("TEST_BYBIT_ARM", "ARMED")
    assert cfg.bybit_live_armed() is True


def test_router_uses_bybit_when_mexc_contract_is_missing(monkeypatch):
    cfg = _arm(monkeypatch)
    chosen, diagnostic = select_candidate(
        decision=_decision(), cfg=cfg, captured_at="2026-08-18T00:00:00+00:00",
        mexc_override=VenueFake("mexc", 100.0, 99.95, missing=True),
        bybit_override=VenueFake("bybit", 100.0, 99.99),
    )
    assert chosen.venue == "bybit"
    assert "mexc" in diagnostic["rejected"]


def test_router_honors_bounded_parallel_preflight_timeout(monkeypatch):
    cfg = _arm(monkeypatch)
    raw = deepcopy(cfg.raw)
    raw["venue_routing"]["compare_timeout_seconds"] = 0.25
    cfg = LiveCanaryConfig(raw=raw)
    started = time.perf_counter()

    chosen, diagnostic = select_candidate(
        decision=_decision(), cfg=cfg, captured_at="2026-08-18T00:00:00+00:00",
        mexc_override=VenueFake("mexc", 100.0, 99.95, delay_seconds=1.0),
        bybit_override=VenueFake("bybit", 100.0, 99.99),
    )

    assert time.perf_counter() - started < 0.7
    assert chosen.venue == "bybit"
    assert diagnostic["rejected"]["mexc"]["reason"] == "VENUE_PREFLIGHT_TIMEOUT"


def test_router_keeps_preferred_venue_inside_hysteresis(monkeypatch):
    cfg = _arm(monkeypatch)
    raw = deepcopy(cfg.raw)
    raw["venue_routing"]["min_cost_improvement_bps"] = 20.0
    cfg = LiveCanaryConfig(raw=raw)
    chosen, _ = select_candidate(
        decision=_decision(), cfg=cfg, captured_at="2026-08-18T00:00:00+00:00",
        mexc_override=VenueFake("mexc", 100.0, 99.99),
        bybit_override=VenueFake("bybit", 99.99, 99.98),
    )
    assert chosen.venue == "mexc"


def test_bybit_signature_matches_v5_formula():
    expected = __import__("hmac").new(
        b"secret", b"123key5000category=linear&symbol=BTCUSDT",
        __import__("hashlib").sha256,
    ).hexdigest()
    assert BybitFuturesClient.signature(
        "secret", "123", "key", 5000, "category=linear&symbol=BTCUSDT"
    ) == expected


def test_bybit_safe_read_retries_with_a_fresh_signature_after_timestamp_window_error():
    class Response:
        status_code = 200

        def __init__(self, payload):
            self.payload = payload

        def json(self):
            return self.payload

    class Session:
        def __init__(self):
            self.headers = []
            self.responses = [
                Response({"retCode": 10002, "retMsg": "invalid request, please check your server timestamp or recv_window param"}),
                Response({"retCode": 0, "retMsg": "OK", "result": {"value": "fresh"}}),
            ]

        def request(self, _method, _url, *, headers, **_kwargs):
            self.headers.append(dict(headers))
            return self.responses.pop(0)

    session = Session()
    client = BybitFuturesClient(
        access_key="key", secret_key="secret", session=session,
        safe_read_retry_attempts=2, safe_read_retry_backoff_seconds=0,
    )

    assert client._request("GET", "/v5/test", private=True) == {"value": "fresh"}
    assert len(session.headers) == 2
    assert all(item["X-BAPI-RECV-WINDOW"] == "5000" for item in session.headers)
    assert all(item["X-BAPI-SIGN"] for item in session.headers)


def test_bybit_stock_perpetuals_terms_use_the_documented_agreement_endpoint(monkeypatch):
    client = BybitFuturesClient(access_key="key", secret_key="secret")
    captured = {}

    def fake_request(method, path, **kwargs):
        captured.update(method=method, path=path, **kwargs)
        return {}

    monkeypatch.setattr(client, "_request", fake_request)

    assert client.sign_stock_perpetuals_agreement() == {}
    assert captured == {
        "method": "POST",
        "path": "/v5/user/agreement",
        "private": True,
        "body": {"agree": True, "categoryV2": 1},
    }


def test_bybit_isolated_uta_uses_coin_wallet_available_balance():
    class Response:
        status_code = 200

        @staticmethod
        def json():
            return {
                "retCode": 0,
                "result": {"list": [{
                    "accountType": "UNIFIED", "totalEquity": "16.95",
                    "totalAvailableBalance": "",
                    "coin": [{"coin": "USDT", "walletBalance": "17.00",
                              "totalOrderIM": "0.25", "totalPositionIM": "0.50",
                              "locked": "0.10", "equity": "16.95"}],
                }]},
            }

    class Session:
        @staticmethod
        def request(*args, **kwargs):
            return Response()

    client = BybitFuturesClient(
        access_key="key", secret_key="secret", session=Session(),
    )
    asset = client.account_asset("USDT")
    assert asset["equity"] == "16.95"
    assert asset["availableOpen"] == 16.15
    assert asset["availableOpenBasis"] == "isolated_coin_wallet_less_reserved"


def test_bybit_candidate_inherits_the_same_live_risk_as_mexc(monkeypatch):
    cfg = _arm(monkeypatch)
    candidate = prepare_candidate(
        venue="bybit", decision=_decision(), cfg=cfg,
        captured_at="2026-08-18T00:00:00+00:00",
        client=VenueFake("bybit", 100.0, 99.99),
    )
    assert 4.0 < candidate.plan["actual_risk_usdt"] <= 5.0


class StockVenueFake(VenueFake):
    def contract_info(self, symbol):
        if self.delay_seconds:
            time.sleep(self.delay_seconds)
        if self.missing:
            raise BybitAPIError("contract metadata missing")
        if self.venue == "bybit":
            contract = _contract(str(symbol), venue="bybit")
            contract.update(symbolType="stock", conceptPlate=["stock"], baseCoin="AAPL")
            return contract
        contract = _contract(str(symbol), venue="mexc")
        contract.update(
            conceptPlate=["Stock", "tradfi"], baseCoin="AAPLSTOCK",
            baseCoinName="AAPL", contractSize=0.01, volUnit=1.0, minVol=1.0,
        )
        return contract


def _stock_decision() -> dict:
    return {
        "decision_id": "stock-decision", "signal_id": "stock-signal",
        "symbol": "AAPL/USDT", "display_symbol": "AAPL",
        "venue_symbols": {"mexc": "AAPLSTOCK_USDT", "bybit": "AAPLUSDT"},
        "bybit_stock_symbol_explicit": True,
        "asset_class": "stock_futures", "mode": "stock_intraday",
        "entry_mode": "BREAKOUT_CONTINUATION", "direction": "long",
        "entry_price": 100.0, "original_stop": 98.0,
        "tp1": 103.0, "tp2": 106.0, "tp3": 110.0,
        "live_risk_multiplier": 0.5, "risk_bucket": "stock_intraday_breakout",
    }


def test_stock_route_uses_each_venues_native_symbol_and_same_risk(monkeypatch):
    cfg = _arm(monkeypatch)
    chosen, diagnostic = select_candidate(
        decision=_stock_decision(), cfg=cfg,
        captured_at="2026-08-18T00:00:00+00:00",
        mexc_override=StockVenueFake("mexc", 100.02, 100.0),
        bybit_override=StockVenueFake("bybit", 99.99, 99.98),
    )
    assert chosen.venue == "bybit"
    assert diagnostic["candidates"]["mexc"]["symbol"] == "AAPLSTOCK_USDT"
    assert diagnostic["candidates"]["bybit"]["symbol"] == "AAPLUSDT"
    assert 4.0 < chosen.plan["actual_risk_usdt"] <= 5.0


def test_stock_route_uses_bybit_when_mexc_symbol_is_locally_blocked(monkeypatch):
    cfg = _arm(monkeypatch)
    decision = _stock_decision()
    decision["blocked_venues"] = ["mexc"]
    chosen, diagnostic = select_candidate(
        decision=decision, cfg=cfg, captured_at="2026-08-18T00:00:00+00:00",
        mexc_override=StockVenueFake("mexc", 100.0, 99.99),
        bybit_override=StockVenueFake("bybit", 100.0, 99.99),
    )
    assert chosen.venue == "bybit"
    assert diagnostic["rejected"]["mexc"]["reason"] == "VENUE_BLOCKED_FOR_SYMBOL"


def test_faster_venue_wins_only_inside_the_cost_band(monkeypatch):
    cfg = _arm(monkeypatch)
    raw = deepcopy(cfg.raw)
    raw["venue_routing"].update(
        latency_tiebreak_cost_band_bps=1.0, min_latency_improvement_ms=5.0,
    )
    raw["venue_routing"]["bybit"]["fallback_taker_fee_rate"] = 0.0008
    cfg = LiveCanaryConfig(raw=raw)
    chosen, diagnostic = select_candidate(
        decision=_decision(), cfg=cfg, captured_at="2026-08-18T00:00:00+00:00",
        mexc_override=VenueFake("mexc", 100.0, 99.99, delay_seconds=0.03),
        bybit_override=VenueFake("bybit", 100.0, 99.99),
    )
    assert chosen.venue == "bybit"
    assert diagnostic["selection_reason"] == "faster_inside_cost_band"


def test_latency_does_not_override_a_materially_better_price(monkeypatch):
    cfg = _arm(monkeypatch)
    raw = deepcopy(cfg.raw)
    raw["venue_routing"].update(
        latency_tiebreak_cost_band_bps=1.0, min_latency_improvement_ms=1.0,
    )
    cfg = LiveCanaryConfig(raw=raw)
    chosen, _ = select_candidate(
        decision=_decision(), cfg=cfg, captured_at="2026-08-18T00:00:00+00:00",
        mexc_override=VenueFake("mexc", 99.5, 99.49, delay_seconds=0.03),
        bybit_override=VenueFake("bybit", 100.0, 99.99),
    )
    assert chosen.venue == "mexc"


def test_only_explicit_bybit_business_error_is_definitive_submission_rejection():
    assert _is_definitive_bybit_submission_rejection(
        BybitAPIError("bad quantity", code=10001, status_code=200)
    ) is True
    assert _is_definitive_bybit_submission_rejection(
        BybitAPIError("Bybit transport error: ReadTimeout")
    ) is False
    assert _is_definitive_bybit_submission_rejection(
        BybitAPIError("success response missing orderId", status_code=200)
    ) is False
    assert _is_definitive_bybit_submission_rejection(
        BybitAPIError("gateway failure", code=10000, status_code=503)
    ) is False


class FilledBybit:
    def __init__(self):
        self.stops = []
        self.tps: dict[str, dict] = {}

    def order_by_external_id(self, symbol, external_oid):
        if external_oid.startswith("cad_"):
            return {"orderId": "entry-1", "state": 3, "dealAvgPrice": 100,
                    "dealVol": 2.5, "externalOid": external_oid}
        if external_oid in self.tps:
            return self.tps[external_oid]
        raise BybitAPIError("Bybit external order missing")

    def open_positions(self, symbol=None):
        return [{"positionId": "BTCUSDT:0:Buy", "positionType": 1, "holdVol": 2.5,
                 "openAvgPrice": 100, "liquidatePrice": 90}]

    def set_full_stop(self, **kwargs):
        self.stops.append(kwargs)
        return {}

    def place_reduce_only_limit(self, **kwargs):
        result = {"orderId": f"tp-{len(self.tps)+1}",
                  "externalOid": kwargs["order_link_id"], "state": 2}
        self.tps[kwargs["order_link_id"]] = result
        return result

    def ticker(self, symbol):
        return {"fairPrice": 100.5}

    def recent_high(self, *args, **kwargs):
        return 100.5


def test_bybit_reconcile_installs_full_stop_and_three_tp_legs(monkeypatch, tmp_path):
    cfg = _arm(monkeypatch)
    db = tmp_path / "bybit.sqlite"
    plan = {
        "venue": "bybit", "external_oid": "cad_decision1", "symbol": "BTCUSDT",
        "direction": "long", "limit_price": 100.0, "original_stop": 98.0,
        "tp1": 103.0, "tp2": 106.0, "tp3": 110.0, "volume_contracts": 2.5,
        "contract_size": 1.0, "taker_fee_rate": 0.00055, "slippage_rate": 0.0005,
        "leverage": 10, "price_tick": 0.01,
        "partial_tp_legs": [
            {"leg": 1, "target": 103.0, "volume_contracts": 0.83},
            {"leg": 2, "target": 106.0, "volume_contracts": 0.83},
            {"leg": 3, "target": 110.0, "volume_contracts": 0.84},
        ],
    }
    with ls.connect(db) as conn:
        ls.ensure_tables(conn)
        conn.execute(
            "INSERT INTO mexc_canary_orders(order_row_id,decision_id,external_oid,symbol,status,"
            "updated_at,plan_json,venue) VALUES(?,?,?,?,?,?,?,?)",
            ("row", "decision-1", "cad_decision1", "BTCUSDT", "SUBMITTED",
             ls.utc_now(), json.dumps(plan), "bybit"),
        )
        conn.execute(
            "INSERT INTO mexc_canary_risk_reservations(reservation_id,decision_id,symbol,status,"
            "risk_usdt,margin_usdt,notional_usdt,created_at,updated_at,venue) "
            "VALUES(?,?,?,?,?,?,?,?,?,?)",
            ("risk", "decision-1", "BTCUSDT", "RESERVED", 5, 25, 250,
             ls.utc_now(), ls.utc_now(), "bybit"),
        )
        conn.commit()
    client = FilledBybit()
    result = reconcile_once(db=db, cfg=cfg, client=client)
    assert result["status"] == "OK"
    assert len(client.stops) == 1
    assert len(client.tps) == 3
    with sqlite3.connect(db) as conn:
        assert conn.execute(
            "SELECT COUNT(*) FROM mexc_canary_exit_legs WHERE venue='bybit' AND status='ACTIVE'"
        ).fetchone()[0] == 3
        position = conn.execute(
            "SELECT venue,tpsl_order_id FROM mexc_canary_positions WHERE decision_id='decision-1'"
        ).fetchone()
    assert position == ("bybit", "bybit-full-position-stop")


def test_bybit_reconcile_is_idempotent_and_keeps_filled_tp_terminal(monkeypatch, tmp_path):
    cfg = _arm(monkeypatch)
    db = tmp_path / "bybit-repeat.sqlite"
    plan = {
        "venue": "bybit", "external_oid": "cad_repeat", "symbol": "BTCUSDT",
        "direction": "long", "limit_price": 100.0, "original_stop": 98.0,
        "tp1": 103.0, "tp2": 106.0, "tp3": 110.0, "volume_contracts": 2.5,
        "contract_size": 1.0, "taker_fee_rate": 0.00055, "slippage_rate": 0.0005,
        "leverage": 10, "price_tick": 0.01,
        "partial_tp_legs": [
            {"leg": 1, "target": 103.0, "volume_contracts": 0.83},
            {"leg": 2, "target": 106.0, "volume_contracts": 0.83},
            {"leg": 3, "target": 110.0, "volume_contracts": 0.84},
        ],
    }
    with ls.connect(db) as conn:
        ls.ensure_tables(conn)
        conn.execute(
            "INSERT INTO mexc_canary_orders(order_row_id,decision_id,external_oid,symbol,status,"
            "updated_at,plan_json,venue) VALUES(?,?,?,?,?,?,?,?)",
            ("row", "repeat", "cad_repeat", "BTCUSDT", "SUBMITTED",
             ls.utc_now(), json.dumps(plan), "bybit"),
        )
        conn.commit()
    client = FilledBybit()
    assert reconcile_once(db=db, cfg=cfg, client=client)["status"] == "OK"
    first_tp = sorted(client.tps)[0]
    client.tps[first_tp]["state"] = 3
    assert reconcile_once(db=db, cfg=cfg, client=client)["status"] == "OK"
    assert reconcile_once(db=db, cfg=cfg, client=client)["status"] == "OK"
    assert len(client.stops) == 1
    assert len(client.tps) == 3
    with sqlite3.connect(db) as conn:
        statuses = dict(conn.execute(
            "SELECT leg_index,status FROM mexc_canary_exit_legs "
            "WHERE decision_id='repeat' ORDER BY leg_index"
        ).fetchall())
    assert statuses == {1: "FILLED", 2: "ACTIVE", 3: "ACTIVE"}


class StopFailureBybit(FilledBybit):
    def __init__(self):
        super().__init__()
        self.emergency_closes = []

    def set_full_stop(self, **kwargs):
        raise BybitAPIError("protection transport failure")

    def close_market(self, **kwargs):
        self.emergency_closes.append(kwargs)
        return {"orderId": "emergency-1", "externalOid": kwargs["order_link_id"], "state": 2}


def test_bybit_unprotected_fill_emergency_closes_and_trips_kill(monkeypatch, tmp_path):
    cfg = _arm(monkeypatch)
    db = tmp_path / "bybit-unprotected.sqlite"
    plan = {
        "venue": "bybit", "external_oid": "cad_unsafe", "symbol": "BTCUSDT",
        "direction": "long", "limit_price": 100.0, "original_stop": 98.0,
        "tp1": 103.0, "tp2": 106.0, "tp3": 110.0, "volume_contracts": 2.5,
        "contract_size": 1.0, "taker_fee_rate": 0.00055, "slippage_rate": 0.0005,
        "leverage": 10, "price_tick": 0.01,
        "partial_tp_legs": [
            {"leg": 1, "target": 103.0, "volume_contracts": 0.83},
            {"leg": 2, "target": 106.0, "volume_contracts": 0.83},
            {"leg": 3, "target": 110.0, "volume_contracts": 0.84},
        ],
    }
    with ls.connect(db) as conn:
        ls.ensure_tables(conn)
        conn.execute(
            "INSERT INTO mexc_canary_orders(order_row_id,decision_id,external_oid,symbol,status,"
            "updated_at,plan_json,venue) VALUES(?,?,?,?,?,?,?,?)",
            ("row", "unsafe", "cad_unsafe", "BTCUSDT", "SUBMITTED",
             ls.utc_now(), json.dumps(plan), "bybit"),
        )
        conn.commit()
    client = StopFailureBybit()
    result = reconcile_once(db=db, cfg=cfg, client=client)
    assert result["status"] == "DEGRADED"
    assert len(client.emergency_closes) == 1
    with ls.connect(db) as conn:
        assert ls.kill_switch_state(conn) == "TRIPPED"
        event = conn.execute(
            "SELECT event_type FROM mexc_canary_events "
            "WHERE decision_id='unsafe' AND event_type='BYBIT_UNPROTECTED_POSITION_EMERGENCY_CLOSE'"
        ).fetchone()
    assert event is not None


def test_shared_risk_limit_counts_both_venues(tmp_path):
    db = tmp_path / "shared-risk.sqlite"
    with ls.connect(db) as conn:
        ls.ensure_tables(conn)
        first = ls.reserve_risk(
            conn, decision_id="mexc-one", symbol="BTC_USDT", risk_usdt=30,
            margin_usdt=10, notional_usdt=100, max_risk_usdt=50,
            max_margin_usdt=None, max_notional_usdt=None, max_open_same_symbol=2,
            venue="mexc",
        )
        second = ls.reserve_risk(
            conn, decision_id="bybit-two", symbol="ETHUSDT", risk_usdt=25,
            margin_usdt=10, notional_usdt=100, max_risk_usdt=50,
            max_margin_usdt=None, max_notional_usdt=None, max_open_same_symbol=2,
            venue="bybit",
        )
    assert first["ok"] is True
    assert second["ok"] is False
    assert second["reason"] == "max_concurrent_risk"
    assert second["active_risk_usdt"] == 30.0


def test_shared_same_symbol_limit_is_cross_venue(tmp_path):
    db = tmp_path / "shared-symbol.sqlite"
    with ls.connect(db) as conn:
        ls.ensure_tables(conn)
        first = ls.reserve_risk(
            conn, decision_id="mexc-btc", symbol="BTC/USDT", risk_usdt=5,
            margin_usdt=10, notional_usdt=100, max_risk_usdt=50,
            max_margin_usdt=None, max_notional_usdt=None, max_open_same_symbol=1,
            venue="mexc",
        )
        second = ls.reserve_risk(
            conn, decision_id="bybit-btc", symbol="BTC/USDT", risk_usdt=5,
            margin_usdt=10, notional_usdt=100, max_risk_usdt=50,
            max_margin_usdt=None, max_notional_usdt=None, max_open_same_symbol=1,
            venue="bybit",
        )
    assert first["ok"] is True
    assert second["ok"] is False
    assert second["reason"] == "max_open_same_symbol"


def test_existing_live_tables_gain_venue_without_losing_rows(tmp_path):
    db = tmp_path / "old-live-schema.sqlite"
    with sqlite3.connect(db) as conn:
        conn.execute(
            "CREATE TABLE mexc_canary_orders("
            "order_row_id TEXT PRIMARY KEY,decision_id TEXT UNIQUE,external_oid TEXT UNIQUE,"
            "exchange_order_id TEXT,symbol TEXT,status TEXT,submitted_at TEXT,updated_at TEXT,"
            "plan_json TEXT,exchange_json TEXT,last_error TEXT)"
        )
        conn.execute(
            "INSERT INTO mexc_canary_orders(order_row_id,decision_id,external_oid,symbol,status,"
            "updated_at,plan_json) VALUES('old','old-decision','old-oid','BTC_USDT','FILLED','now','{}')"
        )
        conn.commit()
    with ls.connect(db) as conn:
        ls.ensure_tables(conn)
        columns = {row[1] for row in conn.execute(
            "PRAGMA table_info(mexc_canary_orders)"
        ).fetchall()}
        row = conn.execute(
            "SELECT order_row_id,venue FROM mexc_canary_orders WHERE decision_id='old-decision'"
        ).fetchone()
    assert "venue" in columns
    assert tuple(row) == ("old", "mexc")
