from __future__ import annotations

import inspect
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import yaml

from src.execution import crypto_fast_flush_reclaim_paper as strategy


UTC = timezone.utc


def _cfg() -> dict:
    cfg = strategy.load_strategy_config()
    cfg.update(allowed_sessions=["asia", "europe", "us", "off"], min_rvol=1.0,
               min_liquidation_notional_usd=20_000.0, min_liquidation_percentile=0.70,
               min_oi_drop_pct=0.35, max_oi_drop_pct=3.0)
    return cfg


def _base_frame() -> pd.DataFrame:
    start = datetime(2026, 9, 20, 12, 0, tzinfo=UTC)
    rows = []
    price = 100.0
    for index in range(30):
        rows.append({"timestamp": start + timedelta(minutes=5 * index), "open": price,
                     "high": price + 0.20, "low": price - 0.20, "close": price,
                     "volume": 100.0})
    rows[25].update(open=100.0, high=100.1, low=98.9, close=99.25, volume=180.0)
    return pd.DataFrame(rows)


def _events() -> list[dict]:
    return [{"side": "SELL", "notional_usd": 80_000.0, "event_id": "liq-1"}]


def _context(oi: float = -0.8) -> dict:
    return {"ok": True, "oi_change_pct": oi, "spread_bps": 4.0}


def test_detects_bounded_strong_flush_with_liquidation_and_oi_drop():
    frame, cfg = _base_frame(), _cfg()
    result = strategy.detect_flush(frame, 25, _events(), _context(), cfg,
                                   liquidation_percentile=0.90,
                                   liquidation_history_count=100)
    assert result["ok"] is True
    assert 1.25 <= result["flush_atr"] <= 3.25
    assert result["reclaim_level"] > result["sweep_extreme"]
    assert result["stop"] < result["sweep_extreme"]


def test_rejects_ordinary_move_and_uncontrolled_cascade():
    cfg = _cfg()
    ordinary = _base_frame()
    ordinary.loc[25, ["low", "close", "volume"]] = [99.75, 99.90, 120.0]
    assert strategy.detect_flush(ordinary, 25, _events(), _context(), cfg,
                                 liquidation_percentile=0.9,
                                 liquidation_history_count=100)["reason"] in {
                                     "FLUSH_TOO_SMALL", "FLUSH_PCT_TOO_SMALL"
                                 }
    cascade = _base_frame()
    cascade.loc[25, ["low", "close", "volume"]] = [94.0, 95.0, 500.0]
    assert strategy.detect_flush(cascade, 25, _events(), _context(), cfg,
                                 liquidation_percentile=0.9,
                                 liquidation_history_count=100)["reason"] == "UNCONTROLLED_CASCADE"


def test_two_bar_profile_waits_while_fast_profile_enters():
    start = datetime(2026, 9, 20, 14, 5, tzinfo=UTC)
    frame = pd.DataFrame([
        {"timestamp": start, "open": 99.20, "high": 99.55, "low": 99.18, "close": 99.50, "volume": 100},
        {"timestamp": start + timedelta(minutes=1), "open": 99.50, "high": 99.70, "low": 99.45, "close": 99.66, "volume": 90},
    ])
    setup = {"decision_at": start, "reclaim_level": 99.40}
    cfg = _cfg()
    fast = cfg["confirmation_profiles"]["FAST_1M_RECLAIM"]
    held = cfg["confirmation_profiles"]["HELD_1M_RECLAIM"]

    at_first_close = start + timedelta(minutes=1)
    assert strategy.detect_confirmation(frame, setup, at_first_close, fast)["status"] == "entry"
    assert strategy.detect_confirmation(frame, setup, at_first_close, held)["status"] == "pending"
    assert strategy.detect_confirmation(frame, setup, start + timedelta(minutes=2), held)["status"] == "entry"


def _structure_confirmation_frame(decision_at: datetime, *, confirm_volume: float = 150.0,
                                  confirm_low: float = 100.25,
                                  confirm_close: float = 100.75,
                                  prior_high: float = 100.20) -> pd.DataFrame:
    rows = []
    for offset in range(-20, 0):
        rows.append({"timestamp": decision_at + timedelta(minutes=offset),
                     "open": 100.0, "high": prior_high, "low": 99.8,
                     "close": 100.0, "volume": 100.0})
    rows.append({"timestamp": decision_at, "open": 100.2, "high": 100.9,
                 "low": confirm_low, "close": confirm_close,
                 "volume": confirm_volume})
    return pd.DataFrame(rows)


def test_structural_fast_profile_confirms_higher_low_break_with_rvol():
    decision_at = datetime(2026, 10, 12, 22, 0, tzinfo=UTC)
    cfg = strategy.load_strategy_config()
    profile = cfg["confirmation_profiles"]["FAST_1M_STRUCTURE_CONFIRM"]
    setup = {"decision_at": decision_at, "reclaim_level": 100.4, "sweep_extreme": 99.0}
    result = strategy.detect_confirmation(
        _structure_confirmation_frame(decision_at), setup, decision_at + timedelta(minutes=1), profile,
    )
    assert result["status"] == "entry"
    assert result["entry"] == 100.75
    assert result["entry_at"] == decision_at + timedelta(minutes=1)
    assert result["confirmation_rvol"] == 1.5
    assert result["previous_high"] == 100.2


def test_structural_fast_profile_rejects_weak_volume_or_broken_sweep_low():
    decision_at = datetime(2026, 10, 12, 22, 0, tzinfo=UTC)
    cfg = strategy.load_strategy_config()
    profile = cfg["confirmation_profiles"]["FAST_1M_STRUCTURE_CONFIRM"]
    setup = {"decision_at": decision_at, "reclaim_level": 100.4, "sweep_extreme": 99.0}
    weak_volume = strategy.detect_confirmation(
        _structure_confirmation_frame(decision_at, confirm_volume=110.0),
        setup, decision_at + timedelta(minutes=1), profile,
    )
    retest_sweep_low = strategy.detect_confirmation(
        _structure_confirmation_frame(decision_at, confirm_low=98.99),
        setup, decision_at + timedelta(minutes=1), profile,
    )
    assert weak_volume["status"] == "pending"
    assert retest_sweep_low["status"] == "pending"


def test_cost_gate_rejects_too_tight_stop():
    cfg = _cfg()
    result = strategy.entry_geometry({"stop": 99.70}, 100.0, cfg)
    assert result == {"ok": False, "reason": "STOP_TOO_TIGHT_FOR_COSTS", "stop_distance_pct": 0.003}


def test_expired_pending_reclaim_is_terminalized_after_scan_horizon():
    cfg = strategy.load_strategy_config()
    profile = cfg["confirmation_profiles"]["FAST_1M_RECLAIM"]
    decision_at = datetime(2026, 9, 30, 18, 10, tzinfo=UTC)
    now = decision_at + timedelta(minutes=20)
    setup = {"decision_at": decision_at, "sweep_at": decision_at - timedelta(minutes=5)}

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    strategy.ensure_tables(conn)
    row = strategy._row(cfg, "ENA/USDT", setup, "FAST_1M_RECLAIM", profile,
                        now - timedelta(minutes=14), "pending", None)
    strategy._upsert(conn, row)

    assert strategy._expire_stale_pending(conn, cfg, now, persist=True) == 1
    expired = conn.execute(
        f"SELECT eligibility_status,rejection_reason,outcome_status,is_clean_for_edge "
        f"FROM {strategy.OUTCOME_TABLE} WHERE candidate_id=?", (row["candidate_id"],),
    ).fetchone()
    assert tuple(expired) == ("rejected", "RECLAIM_WINDOW_EXPIRED", "skipped", 0)
    conn.close()


def test_paper_report_includes_latest_funnel_and_stage_timings():
    report = strategy.render_markdown({
        "enabled": True,
        "liquidation_source": {"status": "HEALTHY"},
        "funnel": {"symbols_scanned": 60, "base_rejections": {"OI_NOT_FLUSHING": 2}},
        "timings_ms": {"total": 125.0},
    })
    assert "Latest scan funnel" in report
    assert "OI_NOT_FLUSHING" in report
    assert "125.0" in report


def test_two_target_simulation_is_net_of_costs_and_stop_first():
    cfg = _cfg()
    at = datetime(2026, 9, 20, 14, 0, tzinfo=UTC)
    frame = pd.DataFrame([{"timestamp": at, "open": 100.0, "high": 100.9,
                           "low": 98.9, "close": 100.5, "volume": 100}])
    result = strategy.simulate_two_target(entry=100.0, stop=99.0, tp1=100.8, tp2=101.35,
                                          candles=frame, symbol="TEST/USDT", cfg=cfg,
                                          bar_minutes=1, force_close=True)
    assert result["close_reason"] == "original_stop"
    assert result["net_pnl_usd"] < result["gross_pnl_usd"]
    assert result["net_r"] < -1.0


def test_unique_profiles_and_no_live_bridge():
    cfg = strategy.load_strategy_config()
    profile_ids = [item["profile_id"] for item in cfg["confirmation_profiles"].values()]
    assert len(profile_ids) == len(set(profile_ids)) == 14
    active = strategy.active_confirmation_profiles(cfg)
    strict_names = {"FAST_1M_ASIA", "FAST_1M_EUROPE", "FAST_1M_RECLAIM"}
    shallow_name = "FAST_1M_SHALLOW_MODERATE"
    flex_name = "FAST_1M_SHALLOW_FLEX"
    assert set(active) == strict_names | {shallow_name, flex_name}
    assert all(not profile["enabled"] for name, profile in cfg["confirmation_profiles"].items()
               if name not in active)
    assert {name: tuple(profile["allowed_sessions"]) for name, profile in active.items()} == {
        "FAST_1M_ASIA": ("asia",),
        "FAST_1M_EUROPE": ("europe",),
        "FAST_1M_RECLAIM": ("us",),
        shallow_name: ("europe", "us"),
        flex_name: ("europe", "us"),
    }
    strict_keys = ("min_flush_atr", "max_flush_atr", "min_flush_pct", "max_flush_pct",
                   "min_rvol", "min_oi_drop_pct", "max_oi_drop_pct",
                   "min_liquidation_percentile", "min_stop_distance_pct", "max_stop_distance_pct")
    strict_values = {key: active["FAST_1M_RECLAIM"][key] for key in strict_keys}
    assert all({key: active[name][key] for key in strict_keys} == strict_values
               for name in strict_names)
    shallow = active[shallow_name]
    assert shallow["profile_id"] == "crypto_fast_flush_reclaim_shallow_1m_paper_v1"
    assert (shallow["min_flush_pct"], shallow["max_flush_pct"]) == (0.60, 1.20)
    assert (shallow["min_flush_atr"], shallow["max_flush_atr"]) == (1.25, 2.25)
    assert (shallow["min_rvol"], shallow["min_oi_drop_pct"],
            shallow["max_oi_drop_pct"], shallow["min_liquidation_percentile"]) == (
                1.00, 1.00, 5.00, 0.80,
            )
    assert shallow["confirmation_timeframe"] == "1m"
    assert shallow["confirmation_window_bars"] == 8 and shallow["require_green"] is True
    assert shallow["hold_bars"] == 1
    assert shallow["enabled"] is True
    flex = active[flex_name]
    assert flex["profile_id"] == "crypto_fast_flush_reclaim_shallow_flex_1m_paper_v1"
    assert (flex["min_flush_pct"], flex["max_flush_pct"]) == (0.45, 2.50)
    assert (flex["min_flush_atr"], flex["max_flush_atr"]) == (1.25, 3.25)
    assert (flex["min_oi_drop_pct"], flex["max_oi_drop_pct"],
            flex["min_liquidation_percentile"]) == (0.40, 5.00, 0.80)
    assert flex["confirmation_timeframe"] == "1m"
    assert flex["confirmation_window_bars"] == 8 and flex["hold_bars"] == 1
    assert flex["max_holding_bars"] == 45
    shallow_near_miss = {
        "decision_at": datetime(2026, 10, 29, 7, 20, tzinfo=UTC),
        "flush_pct": 0.46296, "flush_atr": 1.5254, "rvol": 4.3793,
        "oi_change_pct": -0.4448, "liquidation_percentile": 0.9671,
    }
    assert strategy._profile_gate_reason(shallow_near_miss, shallow) == "PROFILE_FLUSH_PCT"
    assert strategy._profile_gate_reason(shallow_near_miss, flex) is None
    assert cfg["manual_telegram_signals"]["profile_ids"] == [
        "crypto_fast_flush_reclaim_fast_1m_paper_v3",
        "crypto_fast_flush_reclaim_asia_1m_paper_v1",
        "crypto_fast_flush_reclaim_europe_1m_paper_v1",
    ]
    root = Path(__file__).resolve().parents[1]
    profile_id = shallow["profile_id"]
    paper_index = yaml.safe_load(
        (root / "config/paper/crypto/index.yaml").read_text(encoding="utf-8")
    )
    governance = yaml.safe_load(
        (root / "config/strategy_governance.yaml").read_text(encoding="utf-8")
    )["strategy_governance"]
    live_configs = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in (root / "config").rglob("*live*.yaml")
    )
    assert profile_id in paper_index["strategies"][1]["profile_ids"]
    assert profile_id in governance["strategies"]["crypto_fast_flush_reclaim_v3"]["profile_ids"]
    assert profile_id in governance["profile_registry"]["crypto_fast_flush_reclaim_v3"]
    assert governance["strategies"]["crypto_fast_flush_reclaim_v3"]["stage"] == "paper"
    assert governance["strategies"]["crypto_fast_flush_reclaim_v3"]["live_allowed"] is False
    assert profile_id not in live_configs
    flex_id = flex["profile_id"]
    assert flex_id in paper_index["strategies"][1]["profile_ids"]
    assert flex_id in governance["strategies"]["crypto_fast_flush_reclaim_v3"]["profile_ids"]
    assert flex_id in governance["profile_registry"]["crypto_fast_flush_reclaim_v3"]
    assert flex_id not in live_configs
    assert cfg["allowed_sessions"] == ["asia", "europe", "us"]
    assert cfg["confirmation_profiles"]["FAST_1M_ATR_TARGETS"]["target_policy"] == "atr_multiple"
    assert cfg["confirmation_profiles"]["MEDIUM_DEEP_R_CONTROL"]["target_r"] == [0.8, 1.35]
    assert cfg["confirmation_profiles"]["MEDIUM_DEEP_R_EXTENDED"]["target_r"] == [1.0, 1.75]
    assert cfg["confirmation_profiles"]["MEDIUM_DEEP_STRUCTURE_HYBRID"]["target_policy"] == (
        "structure_hybrid_vwap_previous_close"
    )
    source = inspect.getsource(strategy).lower()
    for forbidden in ("capture_forward_sweeps", "place_order", "live_routing", "proposed_signals"):
        assert forbidden not in source


def test_regional_profiles_use_existing_utc_session_buckets_and_leave_off_hours_disabled():
    assert strategy._session(datetime(2026, 10, 20, 0, 0, tzinfo=UTC)) == "asia"
    assert strategy._session(datetime(2026, 10, 20, 6, 59, tzinfo=UTC)) == "asia"
    assert strategy._session(datetime(2026, 10, 20, 7, 0, tzinfo=UTC)) == "europe"
    assert strategy._session(datetime(2026, 10, 20, 12, 59, tzinfo=UTC)) == "europe"
    assert strategy._session(datetime(2026, 10, 20, 13, 0, tzinfo=UTC)) == "us"
    assert strategy._session(datetime(2026, 10, 20, 20, 59, tzinfo=UTC)) == "us"
    assert strategy._session(datetime(2026, 10, 20, 21, 0, tzinfo=UTC)) == "off"


def test_archived_profiles_are_disabled_and_absent_from_active_registries():
    cfg = strategy.load_strategy_config()
    profile = cfg["confirmation_profiles"]["FAST_1M_EUROPE_MODERATE"]
    assert profile["enabled"] is False
    assert profile["allowed_sessions"] == ["europe"]
    assert profile["min_flush_pct"] == 0.60
    assert profile["min_liquidation_percentile"] == 0.80
    assert strategy._profile_activation_allows(
        {"decision_at": datetime(2026, 10, 4, 13, 0, tzinfo=UTC)}, profile,
    ) is False
    assert strategy._profile_activation_allows(
        {"decision_at": datetime(2026, 10, 4, 13, 15, tzinfo=UTC)}, profile,
    ) is True
    root = Path(__file__).resolve().parents[1]
    profile_id = profile["profile_id"]
    paper_index = yaml.safe_load(
        (root / "config/paper/crypto/index.yaml").read_text(encoding="utf-8")
    )
    governance = yaml.safe_load(
        (root / "config/strategy_governance.yaml").read_text(encoding="utf-8")
    )["strategy_governance"]
    live_configs = "\n".join(path.read_text(encoding="utf-8", errors="ignore")
                               for path in (root / "config").rglob("*live*.yaml"))
    assert profile_id not in paper_index["strategies"][1]["profile_ids"]
    assert profile_id not in governance["strategies"]["crypto_fast_flush_reclaim_v3"]["profile_ids"]
    assert profile_id not in governance["profile_registry"]["crypto_fast_flush_reclaim_v3"]
    assert profile_id not in live_configs
    new_profile_id = "crypto_fast_flush_reclaim_structure_confirm_1m_paper_v1"
    assert cfg["confirmation_profiles"]["FAST_1M_STRUCTURE_CONFIRM"]["enabled"] is False
    assert new_profile_id not in paper_index["strategies"][1]["profile_ids"]
    assert new_profile_id not in governance["strategies"]["crypto_fast_flush_reclaim_v3"]["profile_ids"]
    assert new_profile_id not in governance["profile_registry"]["crypto_fast_flush_reclaim_v3"]
    assert new_profile_id not in live_configs


def test_universe_liquidation_batch_matches_per_symbol_reads():
    from src.data_collectors.market_intelligence_store import normalize_symbol

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE liquidation_events (normalized_symbol TEXT, exchange TEXT, event_id TEXT, "
                 "event_at TEXT, side TEXT, notional_usd REAL)")
    now = datetime(2026, 10, 20, 16, 0, tzinfo=UTC)
    records = [
        ("BTC/USDT", "binance", "a", now - timedelta(minutes=2), "SELL", 25000.0),
        ("BTC/USDT", "bybit", "b", now - timedelta(minutes=4), "BUY", 5000.0),
        ("ETH/USDT", "bybit", "c", now - timedelta(minutes=3), "SELL", 30000.0),
        ("ETH/USDT", "other", "d", now - timedelta(minutes=2), "SELL", 80000.0),
        ("SOL/USDT", "binance", "e", now - timedelta(minutes=40), "SELL", 40000.0),
    ]
    conn.executemany(
        "INSERT INTO liquidation_events VALUES(?,?,?,?,?,?)",
        [(normalize_symbol(symbol), exchange, event_id, at.isoformat(), side, notional)
         for symbol, exchange, event_id, at, side, notional in records],
    )
    cfg = _cfg()
    symbols = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
    batched = strategy._recent_event_rows_by_symbol(conn, symbols, now, cfg)
    for symbol in symbols:
        assert sorted(batched[symbol], key=lambda row: row["event_id"]) == sorted(
            strategy._recent_event_rows(conn, symbol, now, cfg), key=lambda row: row["event_id"],
        )
    conn.close()


def test_batched_liquidation_percentiles_match_reference_queries():
    from src.data_collectors.market_intelligence_store import normalize_symbol

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE liquidation_events (normalized_symbol TEXT, side TEXT, event_at TEXT, notional_usd REAL)")
    decision_a = datetime(2026, 10, 20, 14, 0, tzinfo=UTC)
    decision_b = decision_a + timedelta(minutes=5)
    symbol = "BTC/USDT"
    records = []
    for offset in range(1, 13):
        at = decision_a - timedelta(hours=offset)
        records.append((normalize_symbol(symbol), "SELL", at.isoformat(), offset * 1000.0))
    records.extend([
        (normalize_symbol(symbol), "BUY", (decision_a - timedelta(minutes=1)).isoformat(), 999999.0),
        (normalize_symbol(symbol), "SELL", (decision_a + timedelta(seconds=30)).isoformat(), 999999.0),
    ])
    conn.executemany("INSERT INTO liquidation_events VALUES(?,?,?,?)", records)
    episodes = {symbol: [(decision_a, [], 6500.0), (decision_b, [], 7500.0)]}
    batched = strategy._episode_percentiles(conn, episodes, _cfg())
    for decision_at, _events, notional in episodes[symbol]:
        assert batched[(symbol, decision_at.isoformat())] == strategy._episode_percentile(
            conn, symbol, decision_at, notional, _cfg(),
        )
    conn.close()


def test_readonly_intelligence_connection_cannot_write(tmp_path):
    path = tmp_path / "intelligence.sqlite"
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE probe (value INTEGER)")
    conn.commit()
    conn.close()

    readonly = strategy._connect_intelligence_readonly(path)
    assert readonly.execute("PRAGMA query_only").fetchone()[0] == 1
    try:
        readonly.execute("INSERT INTO probe VALUES(1)")
    except sqlite3.OperationalError as exc:
        assert "readonly" in str(exc).lower()
    else:
        raise AssertionError("intelligence connection unexpectedly accepted a write")
    readonly.close()


def test_flush_defers_expensive_context_until_cheap_gates_pass():
    frame, cfg = _base_frame(), _cfg()
    weak = frame.copy()
    weak.loc[25, ["low", "close", "volume"]] = [99.75, 99.90, 120.0]
    weak_result = strategy.detect_flush(
        weak, 25, _events(), None, cfg,
        liquidation_percentile=0.9, liquidation_history_count=100,
    )
    assert weak_result["reason"] in {"FLUSH_TOO_SMALL", "FLUSH_PCT_TOO_SMALL"}

    deferred = strategy.detect_flush(
        frame, 25, _events(), None, cfg,
        liquidation_percentile=0.9, liquidation_history_count=100,
    )
    assert deferred["reason"] == "CONTEXT_REQUIRED"
    verified = strategy.detect_flush(
        frame, 25, _events(), _context(), cfg,
        liquidation_percentile=0.9, liquidation_history_count=100,
    )
    assert verified["ok"] is True


def test_fast_price_prefilter_keeps_only_flush_windows_that_can_reach_full_validation():
    frame, cfg = _base_frame(), _cfg()
    decision_at = frame.loc[25, "timestamp"].to_pydatetime() + timedelta(minutes=5)
    candidates = strategy._candidate_price_windows(frame, decision_at, cfg)
    assert candidates == [(decision_at, 25)]
    assert strategy.detect_flush(
        frame, 25, [], None, cfg, liquidation_percentile=None, liquidation_history_count=0,
    )["reason"] == "LIQUIDATION_NOTIONAL_TOO_SMALL"


def test_medium_deep_hybrid_uses_bounded_vwap_and_previous_close_targets():
    cfg = strategy.load_strategy_config()
    profile = cfg["confirmation_profiles"]["MEDIUM_DEEP_STRUCTURE_HYBRID"]
    entry_at = datetime(2026, 9, 29, 16, 0, tzinfo=UTC)
    frame = pd.DataFrame([
        {"timestamp": entry_at - timedelta(minutes=2), "open": 100.8,
         "high": 101.0, "low": 100.8, "close": 100.9, "volume": 100.0},
        {"timestamp": entry_at - timedelta(minutes=1), "open": 100.8,
         "high": 101.0, "low": 100.8, "close": 100.9, "volume": 100.0},
    ])

    geometry = strategy.entry_geometry(
        {"stop": 99.0, "prior_close": 102.0}, 100.0, cfg,
        profile=profile, frame=frame, entry_at=entry_at,
    )

    assert geometry["ok"] is True
    assert geometry["target_policy"] == "structure_hybrid_vwap_previous_close"
    assert geometry["target_r"] == [0.9, 1.8]
    assert round(geometry["tp1"], 8) == 100.9
    assert round(geometry["tp2"], 8) == 101.8


def test_fast_atr_profile_uses_setup_atr_for_both_targets():
    cfg = strategy.load_strategy_config()
    profile = cfg["confirmation_profiles"]["FAST_1M_ATR_TARGETS"]
    geometry = strategy.entry_geometry(
        {"stop": 99.0, "atr": 1.5}, 100.0, cfg, profile=profile,
    )

    assert geometry["ok"] is True
    assert geometry["target_policy"] == "atr_multiple"
    assert geometry["tp1"] == 101.5
    assert geometry["tp2"] == 103.0
    assert geometry["target_r"] == [1.5, 3.0]


def test_balanced_profile_is_less_restrictive_without_weakening_strict_fast():
    cfg = strategy.load_strategy_config()
    strict = cfg["confirmation_profiles"]["FAST_1M_RECLAIM"]
    balanced = cfg["confirmation_profiles"]["FAST_1M_BALANCED"]
    setup = {
        "flush_atr": 1.5, "flush_pct": 1.0, "rvol": 1.2,
        "oi_change_pct": -0.30, "liquidation_percentile": 0.95,
        "decision_at": datetime(2026, 9, 28, 14, 0, tzinfo=UTC),
    }
    assert strategy._profile_gate_reason(setup, strict) == "PROFILE_OI_RANGE"
    assert strategy._profile_gate_reason(setup, balanced) is None
    assert balanced["min_stop_distance_pct"] < strict["min_stop_distance_pct"]


def test_derivatives_monitor_runs_v3_without_live_capture():
    from scripts import derivatives_monitor

    source = inspect.getsource(derivatives_monitor.fast_flush_paper_loop)
    assert "fast_flush_v3_paper_tick" in source
    assert "capture_forward_sweeps" not in source
    assert "fast_flush_v3_1m_archive" not in source
    archive_source = inspect.getsource(derivatives_monitor.fast_flush_archive_loop)
    assert "fast_flush_v3_1m_archive" in archive_source
    run_source = inspect.getsource(derivatives_monitor.run)
    assert "fast_flush_paper_loop" in run_source
    assert "fast_flush_archive_loop" in run_source
    assert derivatives_monitor.FAST_FLUSH_ARCHIVE_SECONDS == 900


def test_archive_reads_bybit_linear_runtime_cache(monkeypatch, tmp_path):
    from src.data_collectors import fast_flush_research_store as archive

    frame = pd.DataFrame([
        {"timestamp": datetime(2026, 9, 28, 12, minute, tzinfo=UTC),
         "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.5,
         "volume": 1000.0}
        for minute in range(3)
    ])

    class Store:
        def __init__(self, _cfg):
            pass

        def load_ohlcv(self, exchange, symbol, timeframe):
            assert timeframe == "1m"
            return frame if exchange == "bybit_linear" else None

    monkeypatch.setattr("src.storage.file_store.FileStore", Store)
    monkeypatch.setattr(archive, "DEFAULT_PATH", tmp_path / "archive.sqlite")

    result = archive.archive_runtime_frames(["TEST/USDT"])

    assert result["bybit"] == 3
    with archive.connect() as conn:
        assert conn.execute(
            "SELECT COUNT(*) FROM ohlcv_1m WHERE exchange='bybit'"
        ).fetchone()[0] == 3


def test_direct_bybit_candidate_refresh_normalizes_and_sorts(monkeypatch):
    class Response:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "retCode": 0,
                "result": {"list": [
                    ["1727000060000", "101", "102", "100", "101.5", "20", "0"],
                    ["1727000000000", "100", "101", "99", "100.5", "10", "0"],
                ]},
            }

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: Response())
    frames, failed = strategy._refresh_bybit_public(["BTC/USDT"], "1m")

    assert failed == {}
    assert list(frames) == ["BTC/USDT"]
    frame = frames["BTC/USDT"]
    assert frame["timestamp"].is_monotonic_increasing
    assert list(frame["close"]) == [100.5, 101.5]
