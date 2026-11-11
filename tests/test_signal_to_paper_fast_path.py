from datetime import datetime, timezone
import json
import sqlite3

from src.execution import crypto_quality_overlay as cqo
from src.execution.paper_execution_accounting import build_record_from_signal, ensure_table, upsert_outcome
from src.execution.paper_entry_provenance import execution_mode_for_signal
from src.notifiers.telegram_outbox import mark_sent, stage_alert
from src.signals import latency_telemetry as telemetry
from src.signals.pending_monitor import (
    _default_refresh, pending_closed_bar_pairs, pending_refresh_requirements,
)
from src.storage.sqlite import SQLiteStore


def test_versioned_paper_profile_is_authoritative_execution_mode(tmp_path, monkeypatch):
    db = str(tmp_path / "overlay.sqlite")
    sqlite3.connect(db).close()
    signal = {
        "signal_id": "hft", "symbol": "HFT/USDT", "asset_class": "crypto",
        "mode": "intraday", "direction": "long", "score": 72,
        "paper_entry_profile": "crypto_intraday_level_hold_1bar_paper_v1",
        "paper_execution_entry_mode": "LEVEL_HOLD_1BAR",
    }
    provenance = execution_mode_for_signal(signal)
    assert provenance is not None
    assert provenance.entry_mode == "LEVEL_HOLD_1BAR"

    monkeypatch.setattr(
        "src.execution.preentry_classifier.ensure_for_signal",
        lambda *_a, **_kw: (_ for _ in ()).throw(AssertionError("must not reclassify")),
    )
    monkeypatch.setattr(cqo, "market_context", lambda *_a, **_kw: {})
    monkeypatch.setattr(cqo, "symbol_context", lambda *_a, **_kw: {})
    monkeypatch.setattr(cqo, "session_bucket", lambda *_a, **_kw: "us")
    monkeypatch.setattr(cqo, "session_quality", lambda *_a, **_kw: "normal")
    monkeypatch.setattr(cqo, "read_cooldowns", lambda *_a, **_kw: {})
    monkeypatch.setattr(cqo, "open_exposure", lambda *_a, **_kw: {})
    monkeypatch.setattr(cqo, "_catalyst_labels_for", lambda *_a, **_kw: {})
    captured = {}

    def _evaluate(candidate, *_args):
        captured.update(candidate)
        return cqo.OverlayDecision(signal_id="hft", action="FULL_SIZE")

    monkeypatch.setattr(cqo, "evaluate", _evaluate)
    decision = cqo.decide_for_signal(signal, db=db, fs=object(), now=datetime.now(timezone.utc))
    assert decision.action == "FULL_SIZE"
    assert captured["entry_mode"] == "LEVEL_HOLD_1BAR"
    assert decision.ctx["entry_mode_source"] == "paper_execution_profile"


def test_profile_mode_mismatch_is_not_trusted():
    signal = {
        "paper_entry_profile": "crypto_intraday_level_hold_1bar_paper_v1",
        "paper_execution_entry_mode": "BREAKOUT_CONTINUATION",
    }
    assert execution_mode_for_signal(signal) is None


def test_level_hold_v2_profile_has_its_own_authoritative_mode():
    provenance = execution_mode_for_signal({
        "paper_entry_profile": "crypto_intraday_level_hold_v2_paper_v1",
        "paper_execution_entry_mode": "LEVEL_HOLD_V2",
    })
    assert provenance is not None
    assert provenance.entry_mode == "LEVEL_HOLD_V2"


def test_crypto_swing_pullback_v2_profiles_have_authoritative_modes():
    confirmed = execution_mode_for_signal({
        "paper_entry_profile": "crypto_swing_pullback_confirmed_retest_paper_v1",
        "paper_execution_entry_mode": "PULLBACK_CONFIRMED_RETEST",
    })
    fib = execution_mode_for_signal({
        "paper_entry_profile": "crypto_swing_fib_impulse_retest_paper_v1",
        "paper_execution_entry_mode": "FIB_IMPULSE_RETEST",
    })
    assert confirmed is not None
    assert confirmed.entry_mode == "PULLBACK_CONFIRMED_RETEST"
    assert fib is not None
    assert fib.entry_mode == "FIB_IMPULSE_RETEST"


def test_crypto_swing_breakout_reclaim_profile_has_authoritative_mode():
    provenance = execution_mode_for_signal({
        "paper_entry_profile": "crypto_swing_breakout_reclaim_paper_v2",
        "paper_execution_entry_mode": "BREAKOUT_RECLAIM_V2",
    })
    assert provenance is not None
    assert provenance.entry_mode == "BREAKOUT_RECLAIM_V2"


def test_pending_refresh_requirements_are_mode_specific():
    class _Db:
        def load_active_signals(self):
            return [
                {"symbol": "BTC/USDT", "asset_class": "crypto", "tier": "A",
                 "mode": "intraday", "status": "waiting_for_entry"},
                {"symbol": "ETH/USDT", "asset_class": "crypto", "tier": "B",
                 "mode": "swing", "status": "waiting_for_entry"},
                {"symbol": "SOL/USDT", "asset_class": "crypto", "tier": "A",
                 "mode": "intraday", "status": "triggered"},
            ]

    req = pending_refresh_requirements(_Db(), ["1m", "5m", "15m", "1h"])
    assert req["BTC/USDT"] == ("1m", "15m")
    assert req["ETH/USDT"] == ("5m", "1h")
    assert req["SOL/USDT"] == ("1m",)


def test_structural_timeframe_is_not_refetched_inside_same_bar(monkeypatch):
    from src.data_collectors.binance_collector import CollectionSummary

    calls = []

    def _fetch(_self, symbols=None, timeframes=None):
        calls.append((tuple(symbols or ()), tuple(timeframes or ())))
        return CollectionSummary(
            exchange="binance",
            fetched=[f"{symbol} {tf}" for symbol in symbols for tf in timeframes],
        )

    monkeypatch.setattr(
        "src.data_collectors.binance_collector.BinanceOHLCVCollector.fetch", _fetch)
    cache = {}
    requirements = {"BTC/USDT": ("1m", "15m")}
    first = _default_refresh(
        None, object(), ["BTC/USDT"], ["1m", "15m"], concurrency=1,
        cache=cache, ttl_sec=7.5, mono=100.0, requirements=requirements)
    second = _default_refresh(
        None, object(), ["BTC/USDT"], ["1m", "15m"], concurrency=1,
        cache=cache, ttl_sec=7.5, mono=108.0, requirements=requirements)
    assert first["refresh_attempted_pairs"] == 2
    assert second["refresh_attempted_pairs"] == 1
    assert calls[-1] == (("BTC/USDT",), ("1m",))


def test_swing_5m_probe_is_cached_but_scalp_5m_stays_fast(monkeypatch):
    from src.data_collectors.binance_collector import CollectionSummary

    class _Db:
        def __init__(self, modes):
            self.modes = modes

        def load_active_signals(self):
            return [
                {"symbol": "ETH/USDT", "asset_class": "crypto", "tier": "A", "mode": mode}
                for mode in self.modes
            ]

    assert pending_closed_bar_pairs(_Db(["swing"]), ["5m", "1h"]) == {
        ("ETH/USDT", "5m")
    }
    assert pending_closed_bar_pairs(_Db(["swing", "scalp"]), ["5m", "1h"]) == set()

    calls = []

    def _fetch(_self, symbols=None, timeframes=None):
        calls.append((tuple(symbols or ()), tuple(timeframes or ())))
        return CollectionSummary(
            exchange="binance",
            fetched=[f"{symbol} {tf}" for symbol in symbols for tf in timeframes],
        )

    monkeypatch.setattr(
        "src.data_collectors.binance_collector.BinanceOHLCVCollector.fetch", _fetch)
    cache = {}
    requirements = {"ETH/USDT": ("5m", "1h")}
    closed = {("ETH/USDT", "5m")}
    first = _default_refresh(
        None, object(), ["ETH/USDT"], ["5m", "1h"], concurrency=1,
        cache=cache, ttl_sec=7.5, mono=100.0, requirements=requirements,
        closed_bar_pairs=closed,
    )
    second = _default_refresh(
        None, object(), ["ETH/USDT"], ["5m", "1h"], concurrency=1,
        cache=cache, ttl_sec=7.5, mono=108.0, requirements=requirements,
        closed_bar_pairs=closed,
    )
    assert first["refresh_attempted_pairs"] == 2
    assert second["refresh_attempted_pairs"] == 0
    assert len(calls) == 1


def test_binance_market_metadata_is_loaded_once(monkeypatch):
    from types import SimpleNamespace
    from src.data_collectors import binance_collector as module

    module._MARKETS_CACHE.pop("unit_test_exchange", None)
    exchanges = []

    class _Exchange:
        def __init__(self):
            self.markets = {}
            self.loaded = 0
            self.set_count = 0

        def load_markets(self):
            self.loaded += 1
            self.markets = {"BTC/USDT": {}}
            return self.markets

        def set_markets(self, markets):
            self.set_count += 1
            self.markets = markets

        def fetch_ohlcv(self, *_a, **_kw):
            return [[1_700_000_000_000, 1, 1, 1, 1, 1]]

    def _build(_self):
        exchange = _Exchange()
        exchanges.append(exchange)
        return exchange

    monkeypatch.setattr(module.BinanceOHLCVCollector, "_build_exchange", _build)
    cfg = SimpleNamespace(
        exchange_id="unit_test_exchange", symbols=["BTC/USDT"], timeframes=["1m"],
        candle_limit=lambda _tf: 1,
    )
    store = SimpleNamespace(save_ohlcv=lambda *_a, **_kw: None)
    module.BinanceOHLCVCollector(cfg, store).fetch()
    module.BinanceOHLCVCollector(cfg, store).fetch()
    assert exchanges[0].loaded == 1
    assert exchanges[1].loaded == 0
    assert exchanges[1].set_count == 1


def test_alert_and_delivery_job_are_staged_atomically(tmp_path):
    store = SQLiteStore(tmp_path / "outbox.sqlite")
    store.init_db()
    kwargs = dict(
        alert_id="a1", signal_id="s1", alert_type="paper_entry",
        asset_class="crypto", symbol="BTC/USDT", tier="A",
        sent_at="2026-08-04T10:00:00+00:00", message="entry",
        mode="intraday", score=80.0, direction="long", payload={"x": 1},
    )
    assert stage_alert(store, **kwargs) is True
    assert stage_alert(store, **dict(kwargs, alert_id="a2")) is False
    with store.connect() as conn:
        alert = conn.execute(
            "SELECT telegram_status FROM signal_alerts WHERE signal_id='s1'"
        ).fetchone()
        outbox = conn.execute(
            "SELECT status FROM telegram_alert_outbox WHERE signal_id='s1'"
        ).fetchone()
    assert tuple(alert) == ("queued",)
    assert tuple(outbox) == ("pending",)
    mark_sent(store, alert_id="a1")
    with store.connect() as conn:
        assert conn.execute(
            "SELECT telegram_status FROM signal_alerts WHERE alert_id='a1'"
        ).fetchone()[0] == "sent"


def test_latency_telemetry_separates_strategy_wait_and_runtime(tmp_path):
    db = tmp_path / "latency.sqlite"
    assert telemetry.emit(
        db, event_type="paper_entry_decision_completed", signal_id="s1",
        strategy_ready_at="2026-08-04T10:10:00+00:00",
        latency_from_strategy_ready_sec=2.5, stage_runtime_ms=123.4,
    )
    row = telemetry.load_events(db)[0]
    assert row["strategy_ready_at"] == "2026-08-04T10:10:00+00:00"
    assert row["latency_from_strategy_ready_sec"] == 2.5
    assert row["stage_runtime_ms"] == 123.4


def test_paper_execution_persists_profile_for_delivery_retry():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    ensure_table(conn)
    signal = {
        "signal_id": "s1", "symbol": "HFT/USDT", "asset_class": "crypto",
        "mode": "intraday", "direction": "long", "tier": "B",
        "entry_low": 100.0, "entry_high": 100.0, "stop_loss": 99.0,
        "tp1": 101.0, "tp2": 102.0, "tp3": 103.0,
        "created_at": "2026-08-04T10:00:00+00:00",
        "paper_entry_profile": "crypto_intraday_level_hold_1bar_paper_v1",
        "paper_execution_entry_mode": "LEVEL_HOLD_1BAR",
    }
    outcome = {
        "status": "triggered", "entry_triggered": 1,
        "entry_triggered_at": "2026-08-04T10:05:00+00:00",
        "entry_price_used": 100.0,
    }
    sid, key, record = build_record_from_signal(signal, outcome)
    upsert_outcome(conn, signal_id=sid, economic_trade_key=key, computed_at="now", record=record)
    row = conn.execute(
        "SELECT paper_entry_profile,paper_execution_entry_mode "
        "FROM paper_execution_outcomes WHERE signal_id='s1'"
    ).fetchone()
    assert tuple(row) == (
        "crypto_intraday_level_hold_1bar_paper_v1", "LEVEL_HOLD_1BAR")


def test_v2_profile_gate_is_frozen_in_the_execution_snapshot():
    signal = {
        "signal_id": "v2", "symbol": "ETH/USDT", "asset_class": "crypto",
        "mode": "intraday", "direction": "long", "tier": "B",
        "entry_low": 100.0, "entry_high": 101.0, "stop_loss": 99.0,
        "tp1": 102.0, "tp2": 103.0, "tp3": 104.0,
        "created_at": "2026-08-24T10:00:00+00:00",
        "paper_entry_profile": "crypto_intraday_level_hold_v2_paper_v1",
        "paper_execution_entry_mode": "LEVEL_HOLD_V2",
        "paper_entry_profile_gate": {
            "confirmation_volume_ratio": 1.2,
            "zone_penetration_fraction": 0.1,
        },
    }
    outcome = {
        "status": "triggered", "entry_triggered": 1,
        "entry_triggered_at": "2026-08-24T10:05:00+00:00", "entry_price_used": 100.5,
    }
    _, _, record = build_record_from_signal(signal, outcome)
    snapshot = json.loads(record["signal_snapshot_json"])
    assert snapshot["paper_entry_profile_gate"] == signal["paper_entry_profile_gate"]
