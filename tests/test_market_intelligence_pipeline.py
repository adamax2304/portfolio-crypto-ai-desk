from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.data_collectors import market_intelligence_store as mi

NOW = datetime(2026, 7, 14, 12, 0, tzinfo=timezone.utc)


def test_default_store_is_a_dedicated_sidecar(tmp_path, monkeypatch):
    from src.data_collectors.derivatives_pipeline import DerivativesPipeline

    target = tmp_path / "intelligence.sqlite"
    trading = tmp_path / "trading.sqlite"
    monkeypatch.setenv("MARKET_INTELLIGENCE_DB", str(target))
    assert mi.default_db_path() == target.resolve()
    pipeline = DerivativesPipeline(trading_db_path=trading)
    assert pipeline.db_path == target.resolve()
    assert pipeline.trading_db_path == trading
    assert pipeline.mexc == "https://api.mexc.com"


def test_market_intelligence_migration_is_idempotent(tmp_path):
    from scripts.migrate_market_intelligence_store import migrate

    source, target = tmp_path / "trading.sqlite", tmp_path / "intelligence.sqlite"
    with mi.connect(source) as conn:
        mi.insert_derivative_snapshot(
            conn, provider_ts=NOW.isoformat(), exchange="binance", symbol="BTC/USDT",
            funding_rate=0.001, funding_interval_hours=8,
        )
        mi.insert_funding_event(
            conn, event_at=NOW.isoformat(), exchange="bybit", symbol="BTC/USDT",
            funding_rate=0.001, funding_interval_hours=8,
        )
        conn.commit()
    first = migrate(source, target)
    second = migrate(source, target)
    assert first["tables"]["derivative_snapshots"]["after"] == 1
    assert first["tables"]["funding_rate_events"]["after"] == 1
    assert second["tables"]["derivative_snapshots"]["copied"] == 0
    assert second["tables"]["funding_rate_events"]["copied"] == 0


def test_funding_normalization_and_empty_row_rejection(tmp_path):
    with mi.connect(tmp_path / "x.sqlite") as conn:
        assert mi.normalize_funding_8h(0.0001, 1) == 0.0008
        assert mi.insert_derivative_snapshot(
            conn, provider_ts=NOW.isoformat(), exchange="x", symbol="BTC/USDT") is False
        assert conn.execute("SELECT COUNT(*) FROM derivative_snapshots").fetchone()[0] == 0


def test_bybit_http_200_business_error_is_not_silently_accepted(tmp_path):
    from src.data_collectors.derivatives_pipeline import DerivativesPipeline

    class Response:
        def raise_for_status(self):
            return None

        def json(self):
            return {"retCode": 10001, "retMsg": "startTime only is not allowed"}

    class Session:
        def get(self, *args, **kwargs):
            return Response()

    pipeline = DerivativesPipeline(db_path=tmp_path / "x.sqlite", session=Session())
    with pytest.raises(RuntimeError, match="retCode=10001"):
        pipeline._get(pipeline.bybit, "/v5/market/funding/history")


def test_bybit_backfill_sends_both_bounds_and_uses_real_interval(tmp_path):
    from datetime import timedelta
    from src.data_collectors.derivatives_pipeline import DerivativesPipeline

    event_ms = int((datetime.now(timezone.utc) - timedelta(hours=4)).timestamp() * 1000)

    class Pipeline(DerivativesPipeline):
        def __init__(self):
            super().__init__(db_path=tmp_path / "x.sqlite")
            self.funding_calls = 0

        def _post(self, base, path, payload):
            return {"universe": []}

        def _get(self, base, path, params=None):
            params = params or {}
            if path == "/v5/market/instruments-info":
                return {"result": {"list": [{"symbol": "BTCUSDT", "fundingInterval": "60"}]}}
            if path == "/v5/market/funding/history":
                assert "startTime" in params and "endTime" in params
                self.funding_calls += 1
                rows = ([{"fundingRateTimestamp": str(event_ms), "fundingRate": "0.001"}]
                        if self.funding_calls == 1 else [])
                return {"result": {"list": rows}}
            if path == "/v5/market/open-interest":
                return {"result": {"list": []}}
            if path == "/api/v5/public/funding-rate-history":
                return {"data": []}
            if path in ("/fapi/v1/fundingRate", "/futures/data/openInterestHist"):
                return []
            raise AssertionError((base, path, params))

    pipeline = Pipeline()
    result = pipeline.backfill(["BTC/USDT"], days=1)
    assert result["errors"] == {}
    assert result["funding_events"] == 1
    with mi.connect(tmp_path / "x.sqlite") as conn:
        row = conn.execute(
            "SELECT exchange, funding_interval_hours FROM funding_rate_events"
        ).fetchone()
    assert tuple(row) == ("bybit", 1.0)


def test_current_refresh_continues_when_sqlite_writer_is_busy(tmp_path, monkeypatch):
    import sqlite3
    from src.data_collectors import derivatives_pipeline as module

    pipeline = module.DerivativesPipeline(db_path=tmp_path / "x.sqlite")
    for name in ("_current_binance", "_current_bybit", "_current_hyperliquid",
                 "_current_okx", "_current_mexc"):
        monkeypatch.setattr(pipeline, name, lambda symbols: [])
    real_connect = module.mi.connect
    calls = 0

    def locked_after_initial_ensure(*args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 1:
            return real_connect(*args, **kwargs)
        raise sqlite3.OperationalError("database is locked")

    monkeypatch.setattr(module.mi, "connect", locked_after_initial_ensure)
    result = pipeline.refresh_current(["BTC/USDT"])
    assert set(result["sources"]) == {"binance", "bybit", "hyperliquid", "okx", "mexc"}
    assert all("database is locked" in source["error"] for source in result["sources"].values())


def test_point_in_time_context_never_uses_future_rows(tmp_path):
    with mi.connect(tmp_path / "x.sqlite") as conn:
        for exchange in ("binance", "bybit"):
            mi.insert_derivative_snapshot(
                conn, provider_ts="2026-07-14T11:55:00+00:00", exchange=exchange,
                symbol="BTC/USDT", funding_rate=0.0001, funding_interval_hours=8,
                oi_usd=1000, mark_price=100,
            )
            mi.insert_derivative_snapshot(
                conn, provider_ts="2026-07-14T12:05:00+00:00", exchange=exchange,
                symbol="BTC/USDT", funding_rate=0.5, funding_interval_hours=8,
                oi_usd=999999, mark_price=999,
            )
        ctx = mi.latest_derivatives_context(conn, "BTC/USDT", as_of=NOW, max_age_minutes=30)
        assert ctx["venue_count"] == 2
        assert ctx["funding_rate_8h"] == 0.0001
        assert ctx["oi_usd"] == 2000


def test_actual_funding_cost_long_short_and_window(tmp_path):
    with mi.connect(tmp_path / "x.sqlite") as conn:
        for ts, rate in (("2026-07-14T08:00:00+00:00", 0.001),
                         ("2026-07-14T16:00:00+00:00", 0.5)):
            mi.insert_funding_event(conn, event_at=ts, exchange="bybit", symbol="BTC/USDT",
                                    funding_rate=rate, funding_interval_hours=8)
        long = mi.actual_funding_cost(
            conn, symbol="BTC/USDT", exchange="bybit", direction="long", notional_usdt=1000,
            entry_at="2026-07-14T07:00:00+00:00", exit_at="2026-07-14T12:00:00+00:00")
        short = mi.actual_funding_cost(
            conn, symbol="BTC/USDT", exchange="bybit", direction="short", notional_usdt=1000,
            entry_at="2026-07-14T07:00:00+00:00", exit_at="2026-07-14T12:00:00+00:00")
        assert long["events"] == 1 and long["funding_usdt"] == 1.0
        assert short["funding_usdt"] == -1.0


def test_multi_archive_preserves_real_venue_and_skips_empty(tmp_path):
    from src.data_collectors.derivatives_archive import archive_derivatives_records
    from src.storage.sqlite import SQLiteStore

    store = SQLiteStore(tmp_path / "x.sqlite"); store.init_db()
    records = {"BTC/USDT": {
        "fetched_at": NOW.isoformat(), "exchanges": {
            "bybit": {"funding_rate": 0.0001, "open_interest": 10, "open_interest_value": 1000},
            "okx": {"funding_rate": -0.0001, "open_interest_usd": 2000},
            "mexc": {"funding_rate": None, "open_interest": None},
        }}}
    out = archive_derivatives_records(store, records, exchange="multi")
    assert out["canonical"] == 2
    with store.connect() as conn:
        venues = {r[0] for r in conn.execute("SELECT DISTINCT exchange FROM derivative_snapshots")}
        assert venues == {"bybit", "okx"}
        assert "multi" not in venues


def test_ambiguous_verified_contract_has_no_paper_authority(tmp_path):
    with mi.connect(tmp_path / "x.sqlite") as conn:
        for chain, address in (("ethereum", "0x1"), ("bsc", "0x2")):
            mi.upsert_contract(
                conn, asset_symbol="ABC", canonical_asset_id=f"abc-{chain}", chain=chain,
                chain_id="1", contract_address=address, source_primary="test",
                source_secondary="test2", verification_status="verified", verified_at=NOW.isoformat())
        assert mi.verified_contract(conn, "ABC") is None
        assert mi.latest_onchain_context(conn, "ABC/USDT", as_of=NOW)["contract_verified"] is False


def _overlay_inputs(sym):
    from src.execution.crypto_quality_overlay import load_cfg
    cand = {"signal_id": "x", "symbol": "ABC/USDT", "mode": "intraday", "side": "long",
            "score": 80, "entry_mode": "PULLBACK_LIMIT", "news_supported": 0}
    mkt = {"status": "ok", "btc_regime_state": "uptrend", "btc_15m_return": 1,
           "btc_1h_return": 1, "btc_ema_slope_state": "up", "eth_confirm_state": "up"}
    session = {"session_bucket_utc": "europe", "session_quality_state": "strong"}
    base_sym = {"volume_rvol": 2, "funding_state": "normal", "spread_bps": 2,
                "derivatives_status": "unknown", **sym}
    return cand, mkt, base_sym, session, load_cfg()


def test_onchain_hard_block_requires_two_confirmations():
    from src.execution.crypto_quality_overlay import evaluate, BLOCK

    cand, mkt, sym, session, cfg = _overlay_inputs({
        "paper_guard_eligible": True, "contract_verified": True, "honeypot_risk": True,
        "honeypot_confirmations": 1, "onchain_data_confidence": "medium"})
    one = evaluate(cand, mkt, sym, session, {}, {}, cfg)
    assert one.action != BLOCK
    sym["honeypot_confirmations"] = 2; sym["onchain_data_confidence"] = "high"
    two = evaluate(cand, mkt, sym, session, {}, {}, cfg)
    assert two.action == BLOCK
    assert "onchain_verified_honeypot" in two.reasons


def test_onchain_soft_risk_can_only_reduce_size():
    from src.execution.crypto_quality_overlay import evaluate, HALF_SIZE

    cand, mkt, sym, session, cfg = _overlay_inputs({
        "paper_guard_eligible": True, "contract_verified": True,
        "sell_tax": 10, "onchain_data_confidence": "medium"})
    decision = evaluate(cand, mkt, sym, session, {}, {}, cfg)
    assert decision.action == HALF_SIZE
    assert "onchain_elevated_sell_tax" in decision.reasons


def test_holder_concentration_excludes_contract_and_burn_addresses(tmp_path):
    from src.data_collectors.onchain_pipeline import OnchainPipeline

    pipeline = OnchainPipeline(db_path=tmp_path / "x.sqlite")
    security = {
        "token_symbol": "ABC",
        "holder_count": "1000",
        "holders": [
            {"address": "0xcontract", "percent": "0.80", "is_contract": "1"},
            {"address": "0x000000000000000000000000000000000000dead", "percent": "0.04"},
            {"address": "0xeoa1", "percent": "0.10", "is_contract": "0"},
            {"address": "0xeoa2", "percent": "0.05", "is_contract": "0"},
        ],
    }
    with mi.connect(tmp_path / "x.sqlite") as conn:
        assert pipeline._write_goplus_security(
            conn, "ABC", "abc", "ethereum", "0xtoken", security
        ) == 2
        token = conn.execute(
            "SELECT top10_holder_pct FROM token_security_snapshots"
        ).fetchone()
        holders = conn.execute(
            "SELECT top10_pct, excluded_contracts, quality_status "
            "FROM holder_concentration_snapshots"
        ).fetchone()
    assert token[0] == 15.0
    assert holders[0] == 15.0
    assert holders[1] == 1
    assert holders[2] == "contract_and_burn_addresses_excluded"


def test_paper_ledger_prefers_actual_funding_events(tmp_path):
    from src.execution.paper_portfolio import load_cfg, simulate_portfolio

    db = tmp_path / "x.sqlite"
    with mi.connect(db) as conn:
        mi.insert_funding_event(conn, event_at="2026-07-14T08:00:00+00:00", exchange="bybit",
                                symbol="BTC/USDT", funding_rate=0.001, funding_interval_hours=8)
    cfg = load_cfg(); cfg["db_path"] = str(db)
    trade = {"signal_id": "x", "economic_trade_key": "x", "symbol": "BTC/USDT",
             "asset_class": "crypto", "mode": "intraday", "direction": "long",
             "entry": 100, "stop": 99, "paper_execution_r": 1,
             "entry_at": "2026-07-14T07:00:00+00:00", "exit_at": "2026-07-14T12:00:00+00:00"}
    ledger = simulate_portfolio([trade], cfg=cfg, fee_profile="bybit_non_vip_usdt_perp")["ledger"][0]
    assert ledger["funding_source"] == "actual_bybit_funding_events"
    assert ledger["funding_estimated"] == 0 and ledger["funding_event_count"] == 1


def test_scheduler_contains_derivatives_monitor_health_and_backfill():
    from scripts.run_default_market_schedule import build_cycle_steps

    steps = build_cycle_steps(now=NOW, crypto_only=False, include_long_horizon=True,
                              monitor_minutes=90, skip_reports=False)
    labels = [s[0] for s in steps]
    assert any("derivatives monitor" in label for label in labels)
    assert any("market intelligence health" in label for label in labels)
    assert any("derivatives funding/OI public backfill" in label for label in labels)
