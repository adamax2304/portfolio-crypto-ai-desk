from __future__ import annotations

import inspect
import sqlite3
from datetime import datetime, timedelta, timezone

import pandas as pd

from src.execution import crypto_short_retest_shadow as strategy


UTC = timezone.utc


def _profile() -> dict:
    return dict(strategy.load_strategy_config()["profiles"]["short_retest_intraday_v1"])


def _frame(*, reclaim: bool = False, chased: bool = False) -> pd.DataFrame:
    start = datetime(2026, 7, 28, 0, 0, tzinfo=UTC)
    rows = [
        {
            "timestamp": start + timedelta(minutes=15 * idx),
            "open": 100.0, "high": 100.2, "low": 99.8, "close": 100.0,
            "volume": 100.0,
        }
        for idx in range(24)
    ]
    rows.append({
        "timestamp": start + timedelta(minutes=15 * 24),
        "open": 100.0, "high": 100.05, "low": 99.45, "close": 99.55,
        "volume": 120.0,
    })
    rows.append({
        "timestamp": start + timedelta(minutes=15 * 25),
        "open": 99.50, "high": 100.10 if reclaim else 99.90, "low": 99.68,
        "close": 100.05 if reclaim else 99.72, "volume": 100.0,
    })
    rows.append({
        "timestamp": start + timedelta(minutes=15 * 26),
        "open": 99.70, "high": 99.74, "low": 99.35 if chased else 99.50,
        "close": 99.35 if chased else 99.70, "volume": 100.0,
    })
    return pd.DataFrame(rows)


def _event(frame: pd.DataFrame, profile: dict) -> dict:
    seed = strategy.detect_breakdown(frame, 24, profile)
    assert seed["ok"]
    seed["break_volume"] = 120.0
    cfg = strategy.load_strategy_config()
    return strategy._event_row(
        cfg, "short_retest_intraday_v1", profile, "TEST/USDT",
        seed, seed["breakdown_at"],
    )


def test_breakdown_requires_a_closed_move_below_support():
    frame = _frame()
    profile = _profile()
    assert strategy.detect_breakdown(frame, 24, profile)["ok"] is True
    frame.loc[24, "close"] = 99.78
    result = strategy.detect_breakdown(frame, 24, profile)
    assert result["ok"] is False
    assert result["reason"] == "BREAK_NOT_CONFIRMED"


def test_exhausted_initial_break_is_not_armed():
    frame = _frame()
    frame.loc[24, ["low", "close"]] = [98.8, 99.0]
    result = strategy.detect_breakdown(frame, 24, _profile())
    assert result["ok"] is False
    assert result["reason"] == "BREAK_TOO_EXTENDED"


def test_retest_enters_only_after_the_next_closed_confirmation_bar():
    frame = _frame()
    profile = _profile()
    event = _event(frame, profile)
    retest_close = pd.Timestamp(frame.loc[25, "timestamp"]).to_pydatetime() + timedelta(minutes=15)
    early = strategy.confirm_retest(
        frame.iloc[:26], event, profile, now=retest_close,
    )
    assert early["ok"] is False
    assert early["reason"] == "RETEST_NOT_REACHED"

    confirm_close = pd.Timestamp(frame.loc[26, "timestamp"]).to_pydatetime() + timedelta(minutes=15)
    confirmed = strategy.confirm_retest(frame, event, profile, now=confirm_close)
    assert confirmed["ok"] is True
    assert confirmed["decision_at"] == confirm_close
    assert confirmed["entry"] == 99.70
    assert confirmed["stop"] > confirmed["entry"]
    assert confirmed["targets"][0] < confirmed["entry"]


def test_level_acceptance_above_broken_support_invalidates_short():
    frame = _frame(reclaim=True)
    profile = _profile()
    result = strategy.confirm_retest(
        frame, _event(frame, profile), profile,
        now=pd.Timestamp(frame.loc[26, "timestamp"]).to_pydatetime() + timedelta(minutes=15),
    )
    assert result["ok"] is False
    assert result["reason"] == "LEVEL_RECLAIMED"


def test_confirmation_that_already_ran_away_is_not_chased():
    frame = _frame(chased=True)
    profile = _profile()
    result = strategy.confirm_retest(
        frame, _event(frame, profile), profile,
        now=pd.Timestamp(frame.loc[26, "timestamp"]).to_pydatetime() + timedelta(minutes=15),
    )
    assert result["ok"] is False
    assert result["reason"] == "ENTRY_TOO_EXTENDED"


def test_missing_auxiliary_context_is_exploratory_not_rejected():
    cfg = strategy.load_strategy_config()
    assert strategy.context_rejection(
        derivatives={
            "state": "unknown", "spread_bps": None, "quote_volume_usd": None,
        },
        market={"state": "compatible"},
        positive_fast_catalyst=False,
        onchain_hard_risk=False,
        cfg=cfg,
    ) is None


def test_explicit_crowding_and_violent_rebound_still_reject():
    cfg = strategy.load_strategy_config()
    assert strategy.context_rejection(
        derivatives={"state": "crowded_short"},
        market={"state": "compatible"},
        positive_fast_catalyst=False, onchain_hard_risk=False, cfg=cfg,
    ) == "CROWDED_SHORT"
    assert strategy.context_rejection(
        derivatives={"state": "supportive"},
        market={"state": "violent_rebound"},
        positive_fast_catalyst=False, onchain_hard_risk=False, cfg=cfg,
    ) == "BTC_ETH_VIOLENT_REBOUND"


def test_strategy_tables_are_isolated_and_idempotent():
    conn = sqlite3.connect(":memory:")
    forbidden = (
        "proposed_signals", "signal_outcomes", "paper_execution_outcomes",
        "paper_portfolio_ledger", "mexc_canary_outbox", "live_routing",
    )
    for table in forbidden:
        conn.execute(f"CREATE TABLE {table}(value TEXT)")
        conn.execute(f"INSERT INTO {table} VALUES('stable')")
    strategy.ensure_tables(conn)
    strategy.ensure_tables(conn)
    own = {
        row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name LIKE 'crypto_short_retest_shadow_%'"
        )
    }
    assert own == {
        "crypto_short_retest_shadow_events",
        "crypto_short_retest_shadow_outcomes",
        "crypto_short_retest_shadow_evaluations",
        "crypto_short_retest_shadow_meta",
    }
    for table in forbidden:
        assert conn.execute(f"SELECT value FROM {table}").fetchone()[0] == "stable"
    conn.close()


def test_module_contains_no_forbidden_trading_writes():
    source = inspect.getsource(strategy).lower()
    for table in (
        "proposed_signals", "signal_outcomes", "paper_execution_outcomes",
        "paper_portfolio_ledger", "mexc_canary_outbox",
    ):
        assert f"insert into {table}" not in source
        assert f"update {table}" not in source
        assert f"delete from {table}" not in source


def test_monitor_wires_short_retest_after_fresh_derivatives():
    from scripts import derivatives_monitor

    source = inspect.getsource(derivatives_monitor.current_loop)
    assert source.index("pipeline.refresh_current") < source.index("short_retest.tick")
    assert "short_retest_report" in source


def test_monitor_refreshes_cooldowns_after_fresh_derivatives():
    from scripts import derivatives_monitor

    source = inspect.getsource(derivatives_monitor.current_loop)
    assert derivatives_monitor.COOLDOWN_REFRESH_SECONDS == 300
    assert source.index("pipeline.refresh_current") < source.index("quality_overlay.refresh_cooldowns")
    assert '"crypto_quality_cooldowns": cooldown_result' in source


def test_monitor_global_lock_prevents_duplicate_writer(monkeypatch, tmp_path):
    from scripts import derivatives_monitor

    lock = tmp_path / "derivatives_monitor.pid"
    monkeypatch.setattr(derivatives_monitor, "MONITOR_LOCK", lock)
    assert derivatives_monitor._acquire_monitor_lock() is True
    assert derivatives_monitor._acquire_monitor_lock() is False
    derivatives_monitor._release_monitor_lock()
    assert not lock.exists()


def test_swing_uses_existing_native_hourly_history(monkeypatch):
    now = datetime(2026, 7, 29, 0, 0, tzinfo=UTC)
    native = pd.DataFrame([
        {
            "timestamp": now - timedelta(hours=40 - idx),
            "open": 100.0, "high": 100.2, "low": 99.8,
            "close": 100.0, "volume": 100.0,
        }
        for idx in range(40)
    ])
    monkeypatch.setattr(strategy.market_data, "_load_frame", lambda symbol, cfg: (native, "binance"))
    profile = strategy.load_strategy_config()["profiles"]["short_retest_swing_v1"]
    result = strategy._profile_frame(
        "TEST/USDT", pd.DataFrame(), profile, strategy.load_strategy_config(), now=now,
    )
    assert len(result) >= int(profile["structure_lookback_bars"]) + 1


def test_source_freshness_is_mode_specific_for_swing_vs_intraday():
    cfg = strategy.load_strategy_config()
    assert strategy._source_bar_age_limit(cfg, "intraday") == 480.0
    assert strategy._source_bar_age_limit(cfg, "swing") == 900.0


def test_feature_flag_defaults_off_without_operator_config(monkeypatch, tmp_path):
    monkeypatch.setattr(strategy, "CONFIG_PATH", tmp_path / "missing.yaml")
    assert strategy.load_strategy_config()["feature_flag"] is False
