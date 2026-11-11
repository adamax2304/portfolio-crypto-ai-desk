from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import sqlite3

import numpy as np
import pandas as pd

from src.stocks.position_framework import (
    v2_detector,
    v2_llm_packet,
    v2_outcome,
    v2_report,
    v2_store,
)
from src.stocks.position_framework import v2_runner
from src.stocks.position_framework.v2_config import load_config, safety_invariants


def _daily_frame() -> pd.DataFrame:
    index = pd.date_range("2025-10-01 20:00:00+00:00", periods=260, freq="D")
    close = np.linspace(80.0, 98.0, 260)
    frame = pd.DataFrame(
        {
            "open": close - 0.3,
            "high": close + 0.8,
            "low": close - 0.8,
            "close": close,
            "volume": np.full(260, 1_000_000.0),
        },
        index=index,
    )
    frame.iloc[-22:-2, frame.columns.get_loc("open")] = 98.5
    frame.iloc[-22:-2, frame.columns.get_loc("high")] = 100.0
    frame.iloc[-22:-2, frame.columns.get_loc("low")] = 97.5
    frame.iloc[-22:-2, frame.columns.get_loc("close")] = 98.8
    frame.iloc[-2] = [99.2, 102.0, 99.0, 101.4, 2_000_000]
    frame.iloc[-1] = [100.2, 101.5, 99.8, 100.9, 1_200_000]
    return frame


def _features() -> dict:
    return {
        "available": True,
        "last_close": 100.9,
        "ema21": 100.0,
        "sma50": 98.0,
        "sma200": 85.0,
        "atr14": 2.0,
        "above_50d": True,
        "above_200d": True,
        "weekly_above_30w": True,
        "weekly_30w_slope_positive": True,
        "rs_spy": 0.12,
        "rs_sector": 0.08,
        "near_high": {"63": 1.0, "126": 2.0, "252": 3.0},
        "dollar_volume_30d": 100_000_000,
        "volume_ratio": 1.2,
    }


MARKET_ON = {
    "spy_above_50d": True,
    "spy_above_200d": True,
    "vix": 16.0,
}
SECTOR_OK = {
    "sector": "Technology",
    "sector_etf": "XLK",
    "sector_above_50d": True,
    "sector_rs_positive": True,
}
EARNINGS_SAFE = {"calendar_available": True, "days": 30}
EVENT_SAFE = {"blocking": False, "blocking_types": [], "event_types": []}


def test_v2_config_is_shadow_isolated():
    cfg = load_config()
    assert safety_invariants(cfg) == []
    assert cfg["shadow_only"] is True
    assert cfg["write_proposed_signals"] is False
    assert cfg["strategy_id"] == "stocks_position_swing_v2"


def test_breakout_retest_requires_completed_sequence_and_builds_plan():
    result = v2_detector.detect(
        "TEST",
        _daily_frame(),
        _features(),
        market_ctx=MARKET_ON,
        sector_ctx=SECTOR_OK,
        earnings=EARNINGS_SAFE,
        event_ctx=EVENT_SAFE,
        cfg=load_config(),
    )
    assert result["passed"] is True
    assert result["setup_variant"] == "BREAKOUT_RETEST"
    assert result["entry_price"] > 101.5
    assert result["risk_plan"]["stop_price"] < result["entry_price"]
    assert result["risk_plan"]["risk_usd"] == 12.5


def test_breakout_without_bullish_retest_is_rejected():
    frame = _daily_frame()
    frame.iloc[-1] = [101.4, 102.0, 99.8, 100.4, 1_200_000]
    result = v2_detector.detect(
        "TEST",
        frame,
        _features(),
        market_ctx=MARKET_ON,
        sector_ctx=SECTOR_OK,
        earnings=EARNINGS_SAFE,
        event_ctx=EVENT_SAFE,
        cfg=load_config(),
    )
    assert result["passed"] is False
    assert "NO_CONFIRMED_V2_SETUP" in result["rejection_reasons"]


def test_neutral_market_allows_only_half_size_pullback():
    cfg = deepcopy(load_config())
    cfg["setups"]["breakout_retest"]["enabled"] = False
    frame = _daily_frame()
    frame.iloc[-2] = [101.0, 101.5, 99.8, 100.2, 900_000]
    frame.iloc[-1] = [100.1, 101.4, 99.7, 101.2, 1_200_000]
    result = v2_detector.detect(
        "TEST",
        frame,
        _features(),
        market_ctx={"spy_above_50d": False, "spy_above_200d": True, "vix": 23.0},
        sector_ctx=SECTOR_OK,
        earnings=EARNINGS_SAFE,
        event_ctx=EVENT_SAFE,
        cfg=cfg,
    )
    assert result["passed"] is True
    assert result["setup_variant"] == "TREND_PULLBACK_RECLAIM"
    assert result["risk_plan"]["size_weight"] == 0.5
    assert result["risk_plan"]["risk_usd"] == 6.25


def test_risk_off_earnings_and_blocking_events_reject():
    risk_off = v2_detector.detect(
        "TEST", _daily_frame(), _features(),
        market_ctx={"spy_above_50d": False, "spy_above_200d": False, "vix": 35},
        sector_ctx=SECTOR_OK, earnings=EARNINGS_SAFE, event_ctx=EVENT_SAFE,
        cfg=load_config(),
    )
    assert "MARKET_RISK_OFF" in risk_off["rejection_reasons"]

    event = v2_detector.detect(
        "TEST", _daily_frame(), _features(),
        market_ctx=MARKET_ON, sector_ctx=SECTOR_OK,
        earnings={"calendar_available": True, "days": 3},
        event_ctx={"blocking": True, "blocking_types": ["offering_dilution"], "event_types": []},
        cfg=load_config(),
    )
    assert "EARNINGS_WITHIN_HOLD_WINDOW" in event["rejection_reasons"]
    assert "BLOCKING_EVENT:offering_dilution" in event["rejection_reasons"]


def test_missing_event_or_earnings_data_is_dirty_and_fail_closed():
    result = v2_detector.detect(
        "TEST", _daily_frame(), _features(),
        market_ctx=MARKET_ON, sector_ctx=SECTOR_OK,
        earnings={"calendar_available": False, "days": None},
        event_ctx={"event_data_unavailable": True, "blocking": False},
        cfg=load_config(),
    )
    assert result["passed"] is False
    assert result["data_clean"] is False
    assert "EVENT_DATA_UNAVAILABLE" in result["rejection_reasons"]
    assert "EARNINGS_CALENDAR_UNAVAILABLE" in result["rejection_reasons"]


def test_earnings_window_counts_us_trading_sessions():
    from datetime import date
    from src.stocks.market_calendar import us_trading_days_until

    # Friday July 3, 2026 is an NYSE holiday; Monday July 6 is the next session.
    assert us_trading_days_until(date(2026, 7, 6), today=date(2026, 7, 2)) == 1


def _ohlc(rows) -> pd.DataFrame:
    index = pd.date_range("2026-07-29 20:00:00+00:00", periods=len(rows), freq="D")
    frame = pd.DataFrame(rows, columns=["open", "high", "low", "close"], index=index)
    frame["volume"] = 1_000_000
    return frame


def _candidate(**overrides) -> dict:
    row = {
        "entry_price": 100.0,
        "stop_price": 95.0,
        "atr14": 2.0,
        "qty": 10.0,
        "tp1": 110.0,
        "tp2": 115.0,
        "tp1_pct": 0.5,
        "tp2_pct": 0.25,
        "trail_ema_days": 21,
        "hard_exit_sma_days": 50,
        "max_holding_days": 3,
    }
    row.update(overrides)
    return row


EXECUTION = {
    "entry_valid_sessions": 3,
    "max_chase_atr": 0.5,
    "slippage_bps": 7,
    "commission_per_share": 0.0,
    "min_forward_bars": 2,
}


def test_entry_starts_strictly_after_scan_session():
    frame = _ohlc([
        (99, 102, 98, 101),
        (100, 103, 99, 102),
        (102, 104, 101, 103),
    ])
    scan_at = "2026-07-29T22:00:00+00:00"
    assert v2_outcome.first_bar_after_scan(frame, scan_at) == 1


def test_excessive_gap_chase_is_no_entry():
    frame = _ohlc([
        (99, 99.5, 98, 99),
        (103, 106, 102, 105),
        (103, 105, 102, 104),
    ])
    result = v2_outcome.simulate(frame, 1, _candidate(), EXECUTION)
    assert result["status"] == "no_entry"
    assert result["close_reason"] == "EXCESSIVE_GAP_CHASE"
    assert result["net_pnl_usd"] is None


def test_gap_through_stop_uses_open_and_costs_are_split():
    frame = _ohlc([
        (99, 99.5, 98, 99),
        (100, 102, 99, 101),
        (92, 94, 90, 91),
    ])
    result = v2_outcome.simulate(frame, 1, _candidate(), EXECUTION)
    assert result["status"] == "closed"
    assert result["close_reason"] == "STOP"
    assert result["exit_px"] == 92.0
    assert result["gross_pnl_usd"] < 0
    assert result["slippage_usd"] > 0
    assert result["funding_usd"] == 0.0
    assert result["net_pnl_usd"] < result["gross_pnl_usd"]


def test_same_bar_entry_and_stop_is_conservative_stop_first():
    frame = _ohlc([
        (99, 99.5, 98, 99),
        (99, 101, 94, 100),
        (100, 103, 99, 102),
    ])
    result = v2_outcome.simulate(frame, 1, _candidate(), EXECUTION)
    assert result["status"] == "closed"
    assert result["same_bar_ambiguous"] is True
    assert result["close_reason"] == "SAME_BAR_STOP_FIRST"
    assert result["net_pnl_usd"] < 0


def test_store_uses_isolated_tables_and_never_source_trading_tables(tmp_path):
    db = tmp_path / "v2.sqlite"
    v2_store.ensure_tables(db)
    conn = sqlite3.connect(db)
    names = {row[0] for row in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )}
    conn.close()
    assert v2_store.CANDIDATE_TABLE in names
    assert v2_store.OUTCOME_TABLE in names
    assert "proposed_signals" not in names
    assert "signal_outcomes" not in names
    assert "paper_portfolio_ledger" not in names


def test_store_idempotency_readiness_report_and_enriched_packet(tmp_path, monkeypatch):
    db = tmp_path / "v2.sqlite"
    detected = v2_detector.detect(
        "TEST", _daily_frame(), _features(),
        market_ctx=MARKET_ON, sector_ctx=SECTOR_OK,
        earnings=EARNINGS_SAFE, event_ctx=EVENT_SAFE, cfg=load_config(),
    )
    created = "2026-07-30T22:00:00+00:00"
    assert v2_store.insert_candidates([detected], created_at=created, db_path=db) == 1
    assert v2_store.insert_candidates([detected], created_at=created, db_path=db) == 0
    ready = v2_store.readiness(load_config(), db_path=db)
    assert ready["candidate_count"] == 1
    assert ready["verdict"] == "INSUFFICIENT_FORWARD_EVIDENCE"
    report = v2_report.render(load_config(), db_path=db)
    assert "SHADOW ONLY" in report
    assert "stocks_position_swing_v2" in report
    monkeypatch.setattr(v2_llm_packet, "ticker_context", lambda *a, **k: {"lines": []})
    packet = v2_llm_packet.build_packet(limit=2, db_path=db)
    assert "review can only narrow" in packet
    assert "cannot change entry" in packet


def test_default_scheduler_contains_v2_steps():
    from scripts.run_default_market_schedule import daily_long_horizon_steps

    commands = [
        " ".join(step[1]) for step in daily_long_horizon_steps(include_stocks=True)
        if isinstance(step[1], list)
    ]
    assert any("stocks-position-v2-scan" in command for command in commands)
    assert any("stocks-position-v2-outcome-refresh" in command for command in commands)
    assert any("prepare-stocks-position-v2-analysis" in command for command in commands)


def test_raw_split_like_discontinuity_is_fail_closed():
    frame = _daily_frame()
    frame.iloc[-20:, frame.columns.get_loc("open")] /= 2
    frame.iloc[-20:, frame.columns.get_loc("high")] /= 2
    frame.iloc[-20:, frame.columns.get_loc("low")] /= 2
    frame.iloc[-20:, frame.columns.get_loc("close")] /= 2
    assert v2_runner._corporate_action_rejections(frame, load_config()) == [
        "UNADJUSTED_CORPORATE_ACTION"
    ]


def test_last_market_date_handles_timezone_aware_daily_index():
    frame = pd.DataFrame(
        {"close": [100.0]},
        index=pd.DatetimeIndex(["2026-07-29 00:00:00-04:00"]),
    )
    assert str(v2_runner._last_market_date(frame)) == "2026-07-29"


def test_expected_completed_session_uses_prior_day_before_us_close():
    premarket = datetime(2026, 7, 30, 12, 0, tzinfo=timezone.utc)
    after_close = datetime(2026, 7, 30, 21, 0, tzinfo=timezone.utc)
    assert str(v2_runner._expected_completed_session_date(premarket)) == "2026-07-29"
    assert str(v2_runner._expected_completed_session_date(after_close)) == "2026-07-30"


def test_portfolio_caps_admit_best_score_then_reject_overflow():
    cfg = deepcopy(load_config())
    cfg["risk"]["max_open_positions"] = 1
    cfg["risk"]["max_sector_exposure_pct"] = 100
    first = {
        "symbol": "AAA", "score": 90, "sector": "Technology", "entry_price": 100,
        "risk_plan": {"risk_usd": 10, "qty": 5}, "data_clean": True,
    }
    second = {
        "symbol": "BBB", "score": 80, "sector": "Technology", "entry_price": 100,
        "risk_plan": {"risk_usd": 10, "qty": 5}, "data_clean": True,
    }
    accepted, rejected = v2_runner._apply_portfolio_caps(
        [second, first], cfg=cfg, open_rows=[]
    )
    assert [row["symbol"] for row in accepted] == ["AAA"]
    assert rejected[0]["rejection_reasons"] == ["PORTFOLIO_MAX_POSITIONS"]


def test_v2_review_is_advisory_and_rejects_unknown_candidate(tmp_path):
    db = tmp_path / "v2.sqlite"
    detected = v2_detector.detect(
        "TEST", _daily_frame(), _features(),
        market_ctx=MARKET_ON, sector_ctx=SECTOR_OK,
        earnings=EARNINGS_SAFE, event_ctx=EVENT_SAFE, cfg=load_config(),
    )
    created = "2026-07-30T22:00:00+00:00"
    assert v2_store.insert_candidates([detected], created_at=created, db_path=db) == 1
    candidate = v2_store.latest_candidates(limit=1, db_path=db)[0]
    before = dict(candidate)
    result = v2_store.ingest_reviews(
        [
            {
                "candidate_id": candidate["candidate_id"],
                "verdict": "REJECT_EVENT_RISK",
                "confidence": 0.9,
                "reasons": ["fresh offering"],
            },
            {"candidate_id": "unknown", "verdict": "KEEP_TRACKING"},
        ],
        review_cycle="cycle-1",
        db_path=db,
    )
    assert result["ingested"] == 1
    assert result["rejected"][0]["reason"] == "UNKNOWN_CANDIDATE"
    review = v2_store.latest_reviews(db_path=db)[0]
    assert review["verdict"] == "REJECT_EVENT_RISK"
    assert v2_store.latest_candidates(limit=1, db_path=db)[0] == before


def test_readiness_blocks_profitable_sample_with_excess_drawdown(tmp_path):
    db = tmp_path / "v2.sqlite"
    cfg = deepcopy(load_config())
    cfg["evidence_gate"].update(
        min_clean_closed_trades=2,
        min_clean_closed_per_setup=0,
        min_forward_days=0,
        min_profit_factor=1.25,
        max_drawdown_pct_of_equity=8,
    )
    first = v2_detector.detect(
        "AAA", _daily_frame(), _features(),
        market_ctx=MARKET_ON, sector_ctx=SECTOR_OK,
        earnings=EARNINGS_SAFE, event_ctx=EVENT_SAFE, cfg=cfg,
    )
    second = deepcopy(first)
    second.update(
        symbol="BBB",
        setup_variant="TREND_PULLBACK_RECLAIM",
        confirmation_date="2026-07-31T20:00:00+00:00",
    )
    created = "2026-07-30T22:00:00+00:00"
    assert v2_store.insert_candidates([first, second], created_at=created, db_path=db) == 2
    rows = sorted(v2_store.latest_candidates(limit=10, db_path=db), key=lambda r: r["symbol"])
    for row, pnl, exit_date in (
        (rows[0], -500.0, "2026-08-01"),
        (rows[1], 1000.0, "2026-08-02"),
    ):
        v2_store.upsert_outcome(
            row["candidate_id"],
            checked_at=f"{exit_date}T20:00:00+00:00",
            status="closed",
            fields={
                "exit_date": exit_date,
                "net_pnl_usd": pnl,
                "gross_pnl_usd": pnl,
                "fees_usd": 0,
                "slippage_usd": 0,
                "data_clean": True,
            },
            db_path=db,
        )
    ready = v2_store.readiness(cfg, db_path=db)
    assert ready["net_pnl_usd"] == 500.0
    assert ready["profit_factor"] == 2.0
    assert ready["max_drawdown_pct"] == 10.0
    assert ready["drawdown_ok"] is False
    assert ready["gate_passed"] is False
