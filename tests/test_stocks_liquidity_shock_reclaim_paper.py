from __future__ import annotations

import inspect
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import yaml

from src.execution import stocks_liquidity_shock_reclaim_paper as strategy
from src.notifiers import trade_telegram
from src.notifiers.telegram_outbox import mark_sent, stage_alert
from src.storage.sqlite import SQLiteStore


UTC = timezone.utc


def _cfg() -> dict:
    cfg = strategy.load_strategy_config()
    cfg.update(min_flush_atr=1.2, max_flush_atr=4.0, min_flush_pct=0.5,
               min_rvol=1.3, min_level_breach_atr=0.05,
               min_idiosyncratic_drop_pct=0.25,
               min_bar_dollar_volume=1_000_000.0)
    return cfg


def test_candidate_refresh_cap_round_robins_symbols_without_alpha_starvation():
    old_offset = strategy._CANDIDATE_REFRESH_OFFSET
    try:
        strategy._CANDIDATE_REFRESH_OFFSET = 0
        setups = [(f"T{index:02d}", {}, pd.DataFrame()) for index in range(30)]
        first = strategy._select_candidate_refresh_symbols(setups, 24)
        second = strategy._select_candidate_refresh_symbols(setups, 24)
        assert len(first) == len(set(first)) == 24
        assert len(second) == len(set(second)) == 24
        assert set(first) | set(second) == {f"T{index:02d}" for index in range(30)}
        assert set(first) - set(second)
    finally:
        strategy._CANDIDATE_REFRESH_OFFSET = old_offset


def test_stock_candidate_refresh_default_is_expanded():
    assert strategy.load_strategy_config()["max_candidate_refresh_symbols"] == 24


def test_manual_sweep_close_waits_for_all_alerted_profiles_then_sends_once(tmp_path, monkeypatch):
    class Notifier:
        def __init__(self):
            self.messages = []

        def send_fast(self, text, parse_mode=""):
            self.messages.append((text, parse_mode))
            return {"ok": True}

    notifier = Notifier()
    monkeypatch.setattr(trade_telegram, "notifier_for", lambda _root: notifier)
    db = tmp_path / "stock-close.sqlite"
    store = SQLiteStore(db)
    store.init_db()
    signal_id = "manual-paper:stocks:raw-event-1"
    profile_ids = ["profile-base", "profile-structure"]
    labels = {"profile-base": "Стандарт", "profile-structure": "Структура"}
    entry_variants = [{"label": labels[profile_id]} for profile_id in profile_ids]
    stage_alert(
        store, alert_id="entry-alert", signal_id=signal_id,
        alert_type="manual_paper_entry", asset_class="stocks", symbol="PANW",
        tier="PAPER", sent_at="2026-10-12T14:00:00+00:00",
        message="entry", mode="Liquidity Shock Reclaim · Paper", direction="long",
        payload={"variants": entry_variants},
    )
    mark_sent(store, alert_id="entry-alert")

    rows = []
    for candidate_id, profile_id, status in [
        ("candidate-base", "profile-base", "closed"),
        ("candidate-structure", "profile-structure", "open"),
    ]:
        row = {
            "candidate_id": candidate_id, "raw_event_id": "raw-event-1",
            "strategy_id": "stocks_liquidity_shock_reclaim_v1",
            "profile_id": profile_id, "paper_lane": "paper_stocks_liquidity_shock_reclaim_v1",
            "window": "RTH", "generated_at": "2026-10-12T14:00:00+00:00",
            "decision_at": "2026-10-12T14:00:00+00:00",
            "shock_at": "2026-10-12T13:59:00+00:00", "symbol": "PANW",
            "direction": "long", "entry_profile": profile_id,
            "confirmation_timeframe": "1m", "eligibility_status": "eligible",
            "is_clean_for_edge": 1, "entry_ts": "2026-10-12T14:00:00+00:00",
            "entry_price": 400.0, "stop_price": 398.0, "tp1": 402.0,
            "tp2": 403.0, "outcome_status": status,
            "close_reason": "time_exit" if status == "closed" else None,
            "exit_price": 400.5 if status == "closed" else None,
            "exit_ts": "2026-10-12T15:00:00+00:00" if status == "closed" else None,
            "net_pnl_usd": 1.0 if status == "closed" else None,
            "net_r": 0.5 if status == "closed" else None,
        }
        rows.append(row)
    with store.connect() as conn:
        strategy.ensure_tables(conn)
        for row in rows:
            strategy._upsert(conn, row)

    cfg = {"manual_telegram_signals": {
        "enabled": True, "profile_ids": profile_ids, "profile_labels": labels,
    }}
    now = datetime(2026, 10, 12, 15, 1, tzinfo=UTC)
    with store.connect() as conn:
        waiting = strategy._send_manual_paper_close_alerts(
            conn, cfg, db, ["candidate-base"], now,
        )
    assert waiting["sent"] == 0
    assert notifier.messages == []

    with store.connect() as conn:
        conn.execute(
            f"UPDATE {strategy.OUTCOME_TABLE} SET outcome_status='closed',"
            "close_reason='tp2',exit_price=403,exit_ts=?,net_pnl_usd=2,net_r=1 "
            "WHERE candidate_id='candidate-structure'",
            (now.isoformat(),),
        )
    with store.connect() as conn:
        sent = strategy._send_manual_paper_close_alerts(
            conn, cfg, db, ["candidate-structure"], now,
        )

    assert sent["sent"] == 1
    assert len(notifier.messages) == 1
    message, parse_mode = notifier.messages[0]
    assert parse_mode == ""
    assert "Стандарт: ВЫХОД ПО ВРЕМЕНИ" in message
    assert "Структура: TP2" in message


def _frames() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, int]:
    previous = datetime(2026, 9, 28, 14, 0, tzinfo=UTC)
    current = datetime(2026, 9, 29, 13, 30, tzinfo=UTC)  # 09:30 New York
    stamps = [previous + timedelta(minutes=15 * index) for index in range(20)]
    stamps.extend(current + timedelta(minutes=15 * index) for index in range(5))
    rows = [{"timestamp": stamp, "open": 100.0, "high": 100.25, "low": 99.75,
             "close": 100.0, "volume": 1_000_000.0} for stamp in stamps]
    event_idx = len(rows) - 1  # 10:30 ET decision
    rows[event_idx].update(open=100.0, high=100.05, low=98.80, close=99.05,
                           volume=2_000_000.0)
    stock = pd.DataFrame(rows)
    benchmark = pd.DataFrame([{**row, "low": 99.90, "high": 100.10,
                               "volume": 10_000_000.0} for row in rows])
    sector = benchmark.copy()
    return stock, benchmark, sector, event_idx


def test_detects_idiosyncratic_rth_liquidity_shock():
    stock, market, sector, idx = _frames()
    setup = strategy.detect_shock(
        stock, idx, market, sector,
        {"ok": True, "avg_dollar_volume_30d": 1_000_000_000.0}, _cfg(),
    )
    assert setup["ok"] is True
    assert setup["flush_atr"] >= 1.2
    assert setup["level_breach_atr"] > 0
    assert setup["reclaim_level"] > setup["shock_extreme"]
    assert setup["stop"] < setup["shock_extreme"]


def test_rejects_broad_market_cascade_and_outside_window():
    stock, market, sector, idx = _frames()
    market.loc[idx, "low"] = 98.5
    result = strategy.detect_shock(
        stock, idx, market, sector,
        {"ok": True, "avg_dollar_volume_30d": 1_000_000_000.0}, _cfg(),
    )
    assert result["reason"] == "BROAD_MARKET_CASCADE"

    cfg = _cfg()
    cfg["allowed_windows_et"] = ["13:30-15:15"]
    result = strategy.detect_shock(
        stock, idx, market.assign(low=99.9), sector,
        {"ok": True, "avg_dollar_volume_30d": 1_000_000_000.0}, cfg,
    )
    assert result["reason"] == "RTH_WINDOW_NOT_ALLOWED"


def test_point_in_time_negative_news_blocks_only_after_available_at():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE news_canonical_events (trusted_symbols_json TEXT,event_type TEXT,"
        "direction_hint TEXT,risk_action TEXT,available_at TEXT,effective_at TEXT,"
        "published_at TEXT,asset_class TEXT,is_cluster_primary INTEGER)"
    )
    available = datetime(2026, 9, 29, 14, 0, tzinfo=UTC)
    conn.execute(
        "INSERT INTO news_canonical_events VALUES(?,?,?,?,?,?,?,?,?)",
        (json.dumps(["AAPL"]), "guidance", "bearish", "block", available.isoformat(),
         available.isoformat(), available.isoformat(), "stocks", 1),
    )
    before = strategy.news_risk(conn, "AAPL", available - timedelta(seconds=1), _cfg())
    after = strategy.news_risk(conn, "AAPL", available + timedelta(seconds=1), _cfg())
    assert before["blocked"] is False
    assert after == {"blocked": True, "status": "negative_fundamental_catalyst",
                     "event_type": "guidance"}


def test_fast_enters_one_bar_before_held_profile():
    decision = datetime(2026, 9, 29, 14, 30, tzinfo=UTC)
    frame = pd.DataFrame([
        {"timestamp": decision, "open": 99.10, "high": 99.55, "low": 99.05,
         "close": 99.50, "volume": 100_000},
        {"timestamp": decision + timedelta(minutes=1), "open": 99.50, "high": 99.75,
         "low": 99.45, "close": 99.70, "volume": 90_000},
    ])
    setup = {"decision_at": decision, "reclaim_level": 99.40}
    profiles = _cfg()["confirmation_profiles"]
    first_close = decision + timedelta(minutes=1)
    assert strategy.detect_confirmation(frame, setup, first_close,
                                        profiles["FAST_1M_RECLAIM"])["status"] == "entry"
    assert strategy.detect_confirmation(frame, setup, first_close,
                                        profiles["HELD_1M_RECLAIM"])["status"] == "pending"
    assert strategy.detect_confirmation(frame, setup, decision + timedelta(minutes=2),
                                        profiles["HELD_1M_RECLAIM"])["status"] == "entry"


def test_structural_stop_costs_and_stop_first_are_conservative():
    cfg = _cfg()
    geometry = strategy.entry_geometry({"stop": 99.0}, 100.0, cfg)
    assert geometry["ok"] is True
    at = datetime(2026, 9, 29, 14, 30, tzinfo=UTC)
    same_bar = pd.DataFrame([{"timestamp": at, "open": 100.0, "high": 100.9,
                              "low": 98.9, "close": 100.4, "volume": 100_000}])
    result = strategy.simulate_two_target(
        entry=100.0, stop=99.0, tp1=100.8, tp2=101.35,
        candles=same_bar, symbol="AAPL", cfg=cfg, force_close=True,
    )
    assert result["close_reason"] == "original_stop"
    assert result["net_pnl_usd"] < result["gross_pnl_usd"]
    assert result["net_r"] < -1.0


def _open_outcome_conn(entry_at: datetime, profile_name: str = "HELD_1M_RECLAIM"):
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    strategy._SCHEMA_READY_DATABASES.discard(f":memory:{id(conn)}")
    strategy.ensure_tables(conn)
    profile = strategy.load_strategy_config()["confirmation_profiles"][profile_name]
    strategy._upsert(conn, {
        "candidate_id": f"open-{profile_name}", "raw_event_id": "event",
        "strategy_id": "stocks_liquidity_shock_reclaim_v1",
        "profile_id": profile["profile_id"], "paper_lane": "paper",
        "window": "test", "generated_at": entry_at.isoformat(),
        "decision_at": entry_at.isoformat(), "shock_at": entry_at.isoformat(),
        "symbol": "AAPL", "direction": "long", "entry_profile": profile_name,
        "confirmation_timeframe": "1m", "eligibility_status": "eligible",
        "is_clean_for_edge": 1, "outcome_status": "open",
        "entry_ts": entry_at.isoformat(),
        "entry_price": 100.0, "stop_price": 99.0, "tp1": 101.0, "tp2": 102.0,
        "data_status": "ok", "notes_json": "{}",
    })
    return conn


def test_pending_reclaims_expire_when_profile_is_archived_or_window_passes():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    strategy.ensure_tables(conn)
    cfg = strategy.load_strategy_config()
    now = datetime(2026, 10, 19, 14, 0, tzinfo=UTC)
    cases = [
        ("HELD_1M_RECLAIM", now - timedelta(minutes=1), "PROFILE_ARCHIVED_NO_ENTRY"),
        ("HELD_1M_STRUCTURE_TARGETS", now - timedelta(minutes=13), "RECLAIM_WINDOW_EXPIRED"),
    ]
    for profile_name, decision_at, _reason in cases:
        profile = cfg["confirmation_profiles"][profile_name]
        row = strategy._row(
            cfg, "AAPL", {"decision_at": decision_at, "shock_at": decision_at},
            profile_name, profile, now, "pending", None,
        )
        strategy._upsert(conn, row)

    assert strategy._expire_stale_pending(conn, cfg, now) == 2
    rows = conn.execute(
        f"SELECT entry_profile,outcome_status,eligibility_status,rejection_reason,"
        f"entry_ts,is_clean_for_edge FROM {strategy.OUTCOME_TABLE} ORDER BY entry_profile"
    ).fetchall()
    assert [tuple(row) for row in rows] == [
        ("HELD_1M_RECLAIM", "skipped", "rejected", "PROFILE_ARCHIVED_NO_ENTRY", None, 0),
        ("HELD_1M_STRUCTURE_TARGETS", "skipped", "rejected", "RECLAIM_WINDOW_EXPIRED", None, 0),
    ]
    conn.close()


def _flat_minute_bars(start: datetime, count: int) -> pd.DataFrame:
    return pd.DataFrame([
        {"timestamp": start + timedelta(minutes=index), "open": 100.0,
         "high": 100.2, "low": 99.8, "close": 100.0, "volume": 10_000}
        for index in range(count)
    ])


def test_open_stock_position_exits_on_max_holding_bar(monkeypatch):
    entry = datetime(2026, 10, 9, 14, 0, tzinfo=UTC)
    conn = _open_outcome_conn(entry)
    cfg = _cfg()
    cfg["confirmation_profiles"]["HELD_1M_RECLAIM"]["max_holding_bars"] = 3
    monkeypatch.setattr(strategy, "_cache_frame", lambda _symbol, _tf: _flat_minute_bars(entry, 3))

    assert strategy._mature_open(conn, cfg, entry + timedelta(minutes=3)) == 1
    row = conn.execute(
        f"SELECT outcome_status,close_reason,bars_held,data_status FROM {strategy.OUTCOME_TABLE}"
    ).fetchone()
    assert tuple(row) == ("closed", "time_exit", 3, "closed_complete")


def test_open_stock_position_does_not_count_an_unclosed_minute_bar(monkeypatch):
    entry = datetime(2026, 10, 9, 14, 0, tzinfo=UTC)
    conn = _open_outcome_conn(entry)
    cfg = _cfg()
    cfg["confirmation_profiles"]["HELD_1M_RECLAIM"]["max_holding_bars"] = 3
    monkeypatch.setattr(strategy, "_cache_frame", lambda _symbol, _tf: _flat_minute_bars(entry, 3))

    assert strategy._mature_open(conn, cfg, entry + timedelta(minutes=2, seconds=30)) == 0
    row = conn.execute(
        f"SELECT outcome_status,bars_held,data_status FROM {strategy.OUTCOME_TABLE}"
    ).fetchone()
    assert tuple(row) == ("open", 2, "tracking")


def test_missing_minute_cache_keeps_position_open_and_marks_it_stale(monkeypatch):
    entry = datetime(2026, 10, 9, 14, 0, tzinfo=UTC)
    conn = _open_outcome_conn(entry)
    monkeypatch.setattr(strategy, "_cache_frame", lambda _symbol, _tf: pd.DataFrame())

    assert strategy._mature_open(conn, _cfg(), entry + timedelta(minutes=90)) == 0
    row = conn.execute(
        f"SELECT outcome_status,data_status FROM {strategy.OUTCOME_TABLE}"
    ).fetchone()
    assert tuple(row) == ("open", "tracking_stale")


def test_incomplete_eod_cache_keeps_position_open_and_marks_tracking_stale(monkeypatch):
    entry = datetime(2026, 10, 9, 19, 0, tzinfo=UTC)
    conn = _open_outcome_conn(entry)
    cfg = _cfg()
    cfg["confirmation_profiles"]["HELD_1M_RECLAIM"]["max_holding_bars"] = 60
    monkeypatch.setattr(strategy, "_cache_frame", lambda _symbol, _tf: _flat_minute_bars(entry, 30))

    assert strategy._mature_open(conn, cfg, datetime(2026, 10, 9, 20, 5, tzinfo=UTC)) == 0
    row = conn.execute(
        f"SELECT outcome_status,data_status,notes_json FROM {strategy.OUTCOME_TABLE}"
    ).fetchone()
    assert row["outcome_status"] == "open"
    assert row["data_status"] == "tracking_stale"
    tracking = json.loads(row["notes_json"])["tracking"]
    assert tracking["status"] == "tracking_stale"
    assert tracking["reason"] == "session_bars_incomplete"


def test_complete_eod_cache_exits_position_even_before_max_holding_bars(monkeypatch):
    entry = datetime(2026, 10, 9, 19, 30, tzinfo=UTC)
    conn = _open_outcome_conn(entry)
    cfg = _cfg()
    cfg["confirmation_profiles"]["HELD_1M_RECLAIM"]["max_holding_bars"] = 60
    monkeypatch.setattr(strategy, "_cache_frame", lambda _symbol, _tf: _flat_minute_bars(entry, 30))

    assert strategy._mature_open(conn, cfg, datetime(2026, 10, 9, 20, 1, tzinfo=UTC)) == 1
    row = conn.execute(
        f"SELECT outcome_status,close_reason,bars_held FROM {strategy.OUTCOME_TABLE}"
    ).fetchone()
    assert tuple(row) == ("closed", "time_exit", 30)


def test_later_session_bars_cannot_mask_incomplete_entry_session(monkeypatch):
    entry = datetime(2026, 10, 9, 19, 0, tzinfo=UTC)
    conn = _open_outcome_conn(entry)
    cfg = _cfg()
    cfg["confirmation_profiles"]["HELD_1M_RECLAIM"]["max_holding_bars"] = 60
    friday = _flat_minute_bars(entry, 16)
    monday = _flat_minute_bars(datetime(2026, 10, 12, 13, 30, tzinfo=UTC), 390)
    monkeypatch.setattr(strategy, "_cache_frame", lambda _symbol, _tf: pd.concat([friday, monday]))

    assert strategy._mature_open(conn, cfg, datetime(2026, 10, 12, 20, 5, tzinfo=UTC)) == 0
    row = conn.execute(
        f"SELECT outcome_status,data_status FROM {strategy.OUTCOME_TABLE}"
    ).fetchone()
    assert tuple(row) == ("open", "tracking_stale")


def test_disabled_profile_still_matures_existing_open_position(monkeypatch):
    entry = datetime(2026, 10, 9, 14, 0, tzinfo=UTC)
    conn = _open_outcome_conn(entry, "FAST_1M_RECLAIM")
    cfg = _cfg()
    cfg["confirmation_profiles"]["FAST_1M_RECLAIM"]["max_holding_bars"] = 1
    monkeypatch.setattr(strategy, "_cache_frame", lambda _symbol, _tf: _flat_minute_bars(entry, 1))

    assert "FAST_1M_RECLAIM" not in strategy.active_confirmation_profiles(cfg)
    assert strategy._mature_open(conn, cfg, entry + timedelta(minutes=1)) == 1
    row = conn.execute(
        f"SELECT outcome_status,close_reason FROM {strategy.OUTCOME_TABLE}"
    ).fetchone()
    assert tuple(row) == ("closed", "time_exit")


def test_open_position_history_refresh_is_throttled_and_restart_recoverable(monkeypatch):
    entry = datetime(2026, 10, 9, 14, 0, tzinfo=UTC)
    conn = _open_outcome_conn(entry)
    calls = []
    monkeypatch.setattr(strategy, "_refresh_candidates", lambda symbols: (
        calls.append(list(symbols)) or {"attempted": len(symbols), "fetched": len(symbols), "failed": 0}
    ))
    strategy._LAST_OPEN_POSITION_REFRESH.pop("unit-test-db", None)

    first = strategy._refresh_open_position_frames(conn, _cfg(), entry, "unit-test-db")
    second = strategy._refresh_open_position_frames(
        conn, _cfg(), entry + timedelta(seconds=10), "unit-test-db",
    )
    third = strategy._refresh_open_position_frames(
        conn, _cfg(), entry + timedelta(seconds=31), "unit-test-db",
    )
    assert first["status"] == "ok"
    assert second["status"] == "throttled"
    assert third["status"] == "ok"
    assert calls == [["AAPL"], ["AAPL"]]


def test_four_unique_profiles_are_paper_only_and_not_in_live_configs():
    cfg = strategy.load_strategy_config()
    ids = [profile["profile_id"] for profile in cfg["confirmation_profiles"].values()]
    assert len(ids) == len(set(ids)) == 4
    assert set(strategy.active_confirmation_profiles(cfg)) == {"HELD_1M_STRUCTURE_TARGETS"}
    assert all(cfg["confirmation_profiles"][name]["enabled"] is False for name in (
        "FAST_1M_RECLAIM", "HELD_1M_RECLAIM", "HELD_1M_WIDER_STOP_015",
    ))
    assert cfg["confirmation_profiles"]["HELD_1M_STRUCTURE_TARGETS"]["target_policy"] == (
        "pure_structure"
    )
    assert cfg["live_enabled"] is False
    source = inspect.getsource(strategy).lower()
    assert "proposed_signals" not in source
    root = Path(__file__).resolve().parents[1]
    live_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore")
                            for path in (root / "config").rglob("*live*.yaml"))
    assert all(profile_id not in live_text for profile_id in ids)
    profile_id = cfg["confirmation_profiles"]["HELD_1M_WIDER_STOP_015"]["profile_id"]
    paper_index = yaml.safe_load(
        (root / "config/paper/stocks/index.yaml").read_text(encoding="utf-8")
    )
    governance = yaml.safe_load(
        (root / "config/strategy_governance.yaml").read_text(encoding="utf-8")
    )["strategy_governance"]
    assert profile_id not in paper_index["strategies"][0]["profile_ids"]
    assert profile_id not in governance["strategies"]["stocks_liquidity_shock_reclaim_v1"]["profile_ids"]
    assert profile_id not in governance["profile_registry"]["stocks_liquidity_shock_reclaim_v1"]


def test_wider_stop_profile_reprices_fixed_r_targets_and_activation_is_forward_only():
    cfg = strategy.load_strategy_config()
    profile = cfg["confirmation_profiles"]["HELD_1M_WIDER_STOP_015"]
    setup = {"shock_extreme": 98.0, "atr": 2.0, "stop": 97.8}
    widened = strategy._profile_geometry_setup(setup, profile)
    baseline = strategy._profile_geometry_setup(setup, {})
    assert widened is not None and widened["stop"] == 97.7
    assert baseline is setup and baseline["stop"] == 97.8
    geometry = strategy.entry_geometry(widened, 100.0, cfg, profile=profile)
    assert geometry["ok"] is True
    assert round((geometry["tp1"] - 100.0) / (100.0 - geometry["stop"]), 8) == 0.80
    assert round((geometry["tp2"] - 100.0) / (100.0 - geometry["stop"]), 8) == 1.35
    assert strategy._profile_activation_allows(
        {"decision_at": datetime(2026, 10, 4, 13, 0, tzinfo=UTC)}, profile,
    ) is False
    assert strategy._profile_activation_allows(
        {"decision_at": datetime(2026, 10, 5, 13, 31, tzinfo=UTC)}, profile,
    ) is True


def test_held_structure_profile_requires_real_chart_targets():
    cfg = strategy.load_strategy_config()
    profile = cfg["confirmation_profiles"]["HELD_1M_STRUCTURE_TARGETS"]
    start = datetime(2026, 9, 29, 13, 0, tzinfo=UTC)
    history = pd.DataFrame([
        {"timestamp": start + timedelta(minutes=15 * index), "open": 99.5,
         "high": high, "low": 98.5, "close": 99.5, "volume": 100_000}
        for index, high in enumerate([
            100.1, 100.2, 101.2, 100.3, 100.4, 102.1, 100.2, 100.3,
        ])
    ])
    geometry = strategy.entry_geometry(
        {"stop": 99.0, "atr": 0.8}, 100.0, cfg,
        profile=profile, history=history,
    )

    assert geometry["ok"] is True
    assert geometry["target_policy"] == "pure_structure"
    assert geometry["tp1"] > 100.0
    assert geometry["tp2"] > geometry["tp1"]
    assert not geometry["tp1_source"].startswith("atr_")
    assert not geometry["tp2_source"].startswith("atr_")


def test_held_structure_profile_rejects_atr_only_fallback():
    cfg = strategy.load_strategy_config()
    profile = cfg["confirmation_profiles"]["HELD_1M_STRUCTURE_TARGETS"]
    flat = pd.DataFrame([
        {"timestamp": datetime(2026, 9, 29, 13, 0, tzinfo=UTC),
         "open": 99.5, "high": 99.8, "low": 99.1, "close": 99.5,
         "volume": 100_000},
    ])
    geometry = strategy.entry_geometry(
        {"stop": 99.0, "atr": 0.8}, 100.0, cfg,
        profile=profile, history=flat,
    )
    assert geometry == {"ok": False, "reason": "NO_PURE_STRUCTURAL_TARGETS"}


def test_stock_monitor_invokes_paper_lane_after_pending_tracker():
    from src.stocks.monitor import (
        LIQUIDITY_SHOCK_BAR_SETTLE_SECONDS,
        LIQUIDITY_SHOCK_FAST_CADENCE_SECONDS,
        StocksMonitorSession,
    )

    source = inspect.getsource(StocksMonitorSession.run_once)
    assert "_run_liquidity_shock_paper" in source
    assert source.index("_track_pending_entries") < source.index("_run_liquidity_shock_paper")
    run_source = inspect.getsource(StocksMonitorSession.run)
    assert LIQUIDITY_SHOCK_FAST_CADENCE_SECONDS == 15.0
    assert LIQUIDITY_SHOCK_BAR_SETTLE_SECONDS == 5.0
    assert "_aligned_fast_lane_delay" in run_source
