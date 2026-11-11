from __future__ import annotations

import sqlite3
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import pytest

from scripts.run_default_market_schedule import build_cycle_steps
from src.execution import stocks_catalyst_rs_shadow as stocks
from src.execution.shadow_strategy_common import (
    clean_forward_summary, preserve_first_observation, simulate_confirmed_close_entry,
)


UTC = timezone.utc


def _daily_frame() -> pd.DataFrame:
    rows = []
    start = datetime(2026, 6, 10, 20, 0, tzinfo=UTC)
    for i in range(24):
        rows.append({"timestamp": start + timedelta(days=i), "open": 99.0, "high": 102.0,
                     "low": 98.0, "close": 100.0, "volume": 1_000_000})
    return pd.DataFrame(rows)


def _intraday_symbol(*, impulse_high: float = 105.0, impulse_volume: float = 1500.0,
                     next_session_close: float = 110.0) -> pd.DataFrame:
    rows = []
    prior = datetime(2026, 7, 13, 13, 30, tzinfo=UTC)
    for i in range(20):
        px = 100.0
        rows.append({"timestamp": prior + timedelta(minutes=15 * i), "open": px, "high": px + .2,
                     "low": px - .2, "close": px, "volume": 1000.0})
    day = datetime(2026, 7, 14, 13, 30, tzinfo=UTC)
    rows.extend([
        {"timestamp": day, "open": 104.8, "high": impulse_high, "low": 104.5,
         "close": min(impulse_high, 104.95), "volume": impulse_volume},
        {"timestamp": day + timedelta(minutes=15), "open": 105.0, "high": 106.2, "low": 104.9,
         "close": 106.0, "volume": impulse_volume},
        {"timestamp": day + timedelta(minutes=30), "open": 106.0, "high": 106.6, "low": 105.8,
         "close": 106.4, "volume": 1800.0},
        {"timestamp": day + timedelta(minutes=45), "open": 106.4, "high": 106.7, "low": 106.1,
         "close": 106.5, "volume": 1800.0},
        {"timestamp": datetime(2026, 7, 14, 19, 45, tzinfo=UTC), "open": 106.5,
         "high": 106.7, "low": 106.3, "close": 106.5, "volume": 1800.0},
        {"timestamp": datetime(2026, 7, 15, 13, 30, tzinfo=UTC), "open": next_session_close,
         "high": next_session_close + .2, "low": next_session_close - .2,
         "close": next_session_close, "volume": 1500.0},
        {"timestamp": datetime(2026, 7, 15, 19, 45, tzinfo=UTC), "open": next_session_close,
         "high": next_session_close + .2, "low": next_session_close - .2,
         "close": next_session_close, "volume": 1500.0},
    ])
    return pd.DataFrame(rows)


def _benchmark(base: float = 100.0) -> pd.DataFrame:
    prior = datetime(2026, 7, 13, 13, 30, tzinfo=UTC)
    rows = [{"timestamp": prior + timedelta(minutes=15 * i), "open": base, "high": base + .1,
             "low": base - .1, "close": base, "volume": 1_000_000} for i in range(20)]
    day = datetime(2026, 7, 14, 13, 30, tzinfo=UTC)
    rows.extend([
        {"timestamp": day, "open": base, "high": base + .1, "low": base - .1,
         "close": base + .02, "volume": 1_000_000},
        {"timestamp": day + timedelta(minutes=15), "open": base + .02, "high": base + .08,
         "low": base, "close": base + .05, "volume": 1_000_000},
    ])
    return pd.DataFrame(rows)


def _stock_event() -> dict:
    return {"event_id": "event-1", "event_type": "partnership", "source_quality": "primary",
            "published_at": "2026-07-14T13:29:00+00:00", "available_at": "2026-07-14T13:29:00+00:00",
            "linkage_allowed": 1, "trusted_symbols": ["TEST"]}


def _stocks_cfg() -> dict:
    cfg = stocks.load_strategy_config()
    cfg.update(feature_flag=True, min_dollar_volume=100_000, catalyst_freshness_hours=48,
               min_gap_or_impulse_pct=5.0, min_rvol=1.5, min_rs_spy_pct=0.25,
               min_rs_sector_pct=0.15)
    return cfg


def _stock_eval(**kwargs):
    frame = kwargs.pop("stock_bars", _intraday_symbol())
    spy = kwargs.pop("spy_bars", _benchmark())
    sector_bars = kwargs.pop("sector_bars", _benchmark())
    generated_at = kwargs.pop("generated_at", datetime(2026, 7, 14, 20, 0, tzinfo=UTC))
    return stocks.evaluate_candidate(
        event=_stock_event(), symbol="TEST", stock_bars=frame, daily_bars=_daily_frame(),
        spy_bars=spy, sector_bars=sector_bars, sector="technology", sector_etf="XLK",
        coverage_clean=True, cfg=_stocks_cfg(), generated_at=generated_at,
        **kwargs,
    )


@pytest.mark.parametrize("high,expected", [(105.0, "eligible"), (104.99, "rejected"), (105.01, "eligible")])
def test_stocks_gap_boundary(high, expected):
    result = _stock_eval(stock_bars=_intraday_symbol(impulse_high=high))
    assert result["eligibility_status"] == expected
    if expected == "rejected":
        assert result["rejection_reason"] == "IMPULSE_BELOW_THRESHOLD"


@pytest.mark.parametrize("volume,expected", [(1500.0, "eligible"), (1499.0, "rejected"), (1501.0, "eligible")])
def test_stocks_rvol_boundary(volume, expected):
    result = _stock_eval(stock_bars=_intraday_symbol(impulse_volume=volume))
    assert result["eligibility_status"] == expected
    if expected == "rejected":
        assert result["rejection_reason"] == "RVOL_BELOW_THRESHOLD"


def test_stocks_never_enters_on_first_impulse_bar_and_forces_same_day_exit():
    result = _stock_eval()
    assert result["eligibility_status"] == "eligible"
    assert result["entry_ts"] == "2026-07-14T14:00:00+00:00"  # second 15m bar closes at 14:00
    assert result["outcome_status"] == "closed"
    assert result["close_reason"] in {"time_exit", "original_stop", "breakeven_stop", "profit_lock_stop", "tp3_runner"}
    assert result["would_have_held_close_next_session"] == 110.0
    assert result["fees_usd"] >= 0 and result["slippage_usd"] >= 0 and result["funding_usd"] == 0


def test_next_session_information_never_changes_official_pnl():
    a = _stock_eval(stock_bars=_intraday_symbol(next_session_close=80.0))
    b = _stock_eval(stock_bars=_intraday_symbol(next_session_close=150.0))
    assert a["net_pnl_usd"] == b["net_pnl_usd"]
    assert a["close_reason"] == b["close_reason"]
    assert a["would_have_held_close_next_session"] != b["would_have_held_close_next_session"]


def test_stock_evaluation_is_deterministic():
    first = _stock_eval()
    second = _stock_eval()
    keys = ("candidate_id", "entry_ts", "entry_price", "stop_price", "exit_price",
            "close_reason", "net_pnl_usd", "fees_usd", "slippage_usd")
    assert {k: first[k] for k in keys} == {k: second[k] for k in keys}


def test_stock_refresh_time_does_not_make_point_in_time_catalyst_stale():
    result = _stock_eval(generated_at=datetime(2026, 7, 20, 20, 0, tzinfo=UTC))
    assert result["eligibility_status"] == "eligible"


def test_stock_partial_rth_does_not_force_premature_time_exit():
    frame = _intraday_symbol()
    frame = frame[frame["timestamp"] < pd.Timestamp("2026-07-14T14:15:00Z")].copy()
    frame.loc[frame["timestamp"] == pd.Timestamp("2026-07-14T14:00:00Z"),
              ["high", "low", "close"]] = [106.2, 105.9, 106.0]
    result = _stock_eval(stock_bars=frame)
    assert result["eligibility_status"] == "eligible"
    assert result["outcome_status"] == "open"
    assert result["close_reason"] == "still_open"


def test_after_hours_catalyst_separates_news_age_from_tradable_latency():
    event = _stock_event()
    event["published_at"] = event["available_at"] = "2026-07-13T22:00:00+00:00"
    result = stocks.evaluate_candidate(
        event=event, symbol="TEST", stock_bars=_intraday_symbol(), daily_bars=_daily_frame(),
        spy_bars=_benchmark(), sector_bars=_benchmark(), sector="technology", sector_etf="XLK",
        coverage_clean=True, cfg=_stocks_cfg(), generated_at=datetime(2026, 7, 14, 20, 0, tzinfo=UTC),
    )
    assert result["eligibility_status"] == "eligible"
    assert result["latency_seconds"] == result["tradable_latency_seconds"] == 30 * 60
    assert result["catalyst_age_at_entry_seconds"] == 16 * 60 * 60
    assert result["source_ingestion_latency_seconds"] == 0


def test_catalyst_diagnostics_exclude_legacy_wall_clock_latency():
    rows = [
        {
            "window": "forward_post_activation", "eligibility_status": "eligible",
            "outcome_status": "closed", "is_clean_for_edge": 1, "net_pnl_usd": 1.0,
            "latency_seconds": 80_000.0, "tradable_latency_seconds": None,
        },
        {
            "window": "forward_post_activation", "eligibility_status": "eligible",
            "outcome_status": "closed", "is_clean_for_edge": 1, "net_pnl_usd": 1.0,
            "latency_seconds": 1_800.0, "tradable_latency_seconds": 1_800.0,
            "catalyst_age_at_entry_seconds": 60_000.0,
            "source_ingestion_latency_seconds": 120.0,
        },
    ]
    diagnostics = stocks._latency_aware_diagnostics(rows, group_keys=())
    assert diagnostics["avg_latency_seconds"] == 1_800.0
    assert diagnostics["legacy_wall_clock_latency_rows_excluded"] == 1
    assert diagnostics["avg_catalyst_age_at_entry_seconds"] == 60_000.0


def test_stock_market_context_does_not_read_unclosed_bar():
    spy = _benchmark()
    future_open = pd.DataFrame([{
        "timestamp": datetime(2026, 7, 14, 14, 0, tzinfo=UTC), "open": 100.0,
        "high": 150.0, "low": 99.0, "close": 150.0, "volume": 1_000_000,
    }])
    result = _stock_eval(spy_bars=pd.concat([spy, future_open], ignore_index=True))
    assert result["eligibility_status"] == "eligible"


def test_stock_event_materialized_after_decision_is_not_visible():
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE news_canonical_events (asset_class TEXT, linkage_allowed INTEGER, "
        "is_cluster_primary INTEGER, effective_at TEXT, published_at TEXT, created_at TEXT, "
        "trusted_symbols_json TEXT)"
    )
    conn.execute(
        "INSERT INTO news_canonical_events VALUES (?,?,?,?,?,?,?)",
        ("stocks", 1, 1, "2026-07-14T13:29:00+00:00", "2026-07-14T13:29:00+00:00",
         "2026-07-15T00:00:01+00:00", '["TEST"]'),
    )
    cfg = _stocks_cfg()
    cfg["catalyst_lookback_hours"] = 48
    rows = stocks._event_rows(conn, cfg, datetime(2026, 7, 15, 0, 0, tzinfo=UTC))
    conn.close()
    assert rows == []


def test_stock_unconfirmed_social_catalyst_is_rejected():
    event = _stock_event()
    event["source_quality"] = "social"
    result = stocks.evaluate_candidate(
        event=event, symbol="TEST", stock_bars=_intraday_symbol(), daily_bars=_daily_frame(),
        spy_bars=_benchmark(), sector_bars=_benchmark(), sector="technology", sector_etf="XLK",
        coverage_clean=True, cfg=_stocks_cfg(), generated_at=datetime(2026, 7, 14, 20, 0, tzinfo=UTC),
    )
    assert result["rejection_reason"] == "CATALYST_UNTRUSTED"


def test_catalyst_shadow_taxonomy_and_subject_recovery_are_conservative():
    event = {
        "event_type": "macro_headline",
        "title": "AMD launches Helios, its first rack AI system, against NVDA",
        "trusted_symbols_json": "[]", "mentioned_symbols_json": '["AMD","NVDA"]',
    }
    event_type, origin = stocks._local_event_type(event)
    symbols, symbol_origin = stocks._shadow_subject_symbols(event, {"AMD", "NVDA"}, event_type)
    assert (event_type, origin) == ("product_launch", "shadow_taxonomy_v1")
    assert symbols == {"AMD"}
    assert symbol_origin == "shadow_title_ticker"

    named_issuer = {
        "event_type": "product_launch", "title": "Apple unveils a new on-device AI platform",
        "trusted_symbols_json": "[]", "mentioned_symbols_json": '["AAPL"]',
    }
    assert stocks._shadow_subject_symbols(named_issuer, {"AAPL"}, "product_launch")[0] == {"AAPL"}

    medical_acronym = {
        "event_type": "fda_clinical",
        "title": "4DMT reports positive clinical trial data in a broad wet AMD population",
        "trusted_symbols_json": "[]", "mentioned_symbols_json": "[]",
    }
    assert stocks._shadow_subject_symbols(medical_acronym, {"AMD"}, "fda_clinical")[0] == set()

    partner_context = {
        "event_type": "partnership",
        "title": "Nokia expands its Nvidia partnership to power new products",
        "trusted_symbols_json": '["NVDA"]', "mentioned_symbols_json": '["NVDA"]',
    }
    assert stocks._shadow_subject_symbols(partner_context, {"NVDA"}, "partnership")[0] == set()


def test_catalyst_management_comment_is_not_a_management_change():
    event_type, origin = stocks._local_event_type({
        "event_type": "management_change",
        "title": "Nvidia CEO dismisses hardware delay report and confirms production volume",
    })
    assert (event_type, origin) == ("other_news", "shadow_taxonomy_correction_v1")


def test_secondary_catalyst_admission_requires_factual_non_title_only_news():
    cfg = _stocks_cfg()
    cfg.update(exploratory_single_secondary_enabled=True,
               exploratory_secondary_event_types=["partnership"],
               exploratory_blocked_title_markers=["?", "could "])
    factual = {**_stock_event(), "source_quality": "secondary", "source": "wire-a",
               "content_level": "full_body", "title": "TEST partners with ACME"}
    tier, _, _, _ = stocks._trust_trigger([factual], cfg)
    assert tier == "exploratory_single_secondary"
    speculative = {**factual, "title": "Could TEST partner with ACME?"}
    assert stocks._trust_trigger([speculative], cfg)[0] == "untrusted"
    title_only = {**factual, "content_level": "title_only"}
    assert stocks._trust_trigger([title_only], cfg)[0] == "untrusted"


def test_relaxed_shadow_candidate_is_executed_but_labeled_exploratory():
    cfg = _stocks_cfg()
    cfg.update(min_gap_or_impulse_pct=2.0, min_rvol=1.25, min_rs_spy_pct=0.10,
               min_rs_sector_pct=0.05, strict_min_gap_or_impulse_pct=5.0,
               strict_min_rvol=1.5, exploratory_single_secondary_enabled=True)
    event = {**_stock_event(), "source_quality": "secondary", "content_level": "full_body",
             "title": "TEST partners with ACME", "source_trust_tier": "exploratory_single_secondary"}
    result = stocks.evaluate_candidate(
        event=event, symbol="TEST", stock_bars=_intraday_symbol(impulse_high=102.0, impulse_volume=1300.0),
        daily_bars=_daily_frame(), spy_bars=_benchmark(), sector_bars=_benchmark(),
        sector="technology", sector_etf="XLK", coverage_clean=True, cfg=cfg,
        generated_at=datetime(2026, 7, 14, 20, 0, tzinfo=UTC),
    )
    assert result["eligibility_status"] == "eligible"
    assert result["evidence_cohort"] == "exploratory_v1"
    assert result["outcome_status"] == "closed"


def test_exploratory_profit_cannot_promote_the_strict_cohort():
    now = datetime(2026, 7, 20, tzinfo=UTC)
    cfg = _stocks_cfg()
    cfg.update(min_clean_closed=2, min_forward_days=0, min_profit_factor=1.0,
               max_review_drawdown_usd=1000.0)
    base = {"window": "forward_post_activation", "is_clean_for_edge": 1,
            "outcome_status": "closed", "fees_usd": 0.0, "slippage_usd": 0.0,
            "funding_usd": 0.0, "net_r": 1.0, "entry_ts": now.isoformat()}
    rows = [
        {**base, "evidence_cohort": "strict_v1", "net_pnl_usd": 1.0},
        {**base, "evidence_cohort": "exploratory_v1", "net_pnl_usd": 100.0},
        {**base, "evidence_cohort": "exploratory_v1", "net_pnl_usd": 100.0},
    ]
    summary, strict, exploratory = stocks._evidence_summaries(
        rows, activated_at=(now - timedelta(days=30)).isoformat(), now=now, cfg=cfg,
    )
    assert summary["net_pnl_usd"] == 201.0
    assert exploratory["clean_closed"] == 2
    assert strict["clean_closed"] == 1
    assert summary["verdict"] == strict["verdict"] == "INSUFFICIENT_CLEAN_SAMPLE"


def test_stock_late_materialization_does_not_make_old_news_fresh():
    event = _stock_event()
    event["published_at"] = "2026-07-10T13:29:00+00:00"
    event["available_at"] = "2026-07-14T13:29:00+00:00"
    result = stocks.evaluate_candidate(
        event=event, symbol="TEST", stock_bars=_intraday_symbol(), daily_bars=_daily_frame(),
        spy_bars=_benchmark(), sector_bars=_benchmark(), sector="technology", sector_etf="XLK",
        coverage_clean=True, cfg=_stocks_cfg(), generated_at=datetime(2026, 7, 14, 20, 0, tzinfo=UTC),
    )
    assert result["rejection_reason"] == "CATALYST_STALE"


def test_dirty_stock_coverage_never_counts_as_edge():
    result = stocks.evaluate_candidate(
        event=_stock_event(), symbol="TEST", stock_bars=_intraday_symbol(), daily_bars=_daily_frame(),
        spy_bars=_benchmark(), sector_bars=_benchmark(), sector="technology", sector_etf="XLK",
        coverage_clean=False, cfg=_stocks_cfg(), generated_at=datetime(2026, 7, 14, 20, 0, tzinfo=UTC),
    )
    assert result["rejection_reason"] == "DATA_COVERAGE_DIRTY"
    assert result["is_clean_for_edge"] == 0


def test_coverage_snapshot_never_marks_old_trade_dirty_and_warmup_is_neutral():
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE stock_coverage_by_mode (symbol TEXT, mode TEXT, is_clean INTEGER, "
        "status TEXT, missing_bars INTEGER, computed_at TEXT)"
    )
    conn.execute("INSERT INTO stock_coverage_by_mode VALUES (?,?,?,?,?,?)", (
        "TEST", "intraday", 0, "SESSION_WARMUP", 0, "2026-07-21T13:45:00+00:00",
    ))
    assert stocks._coverage_status(conn, "TEST", datetime(2026, 7, 14, 14, tzinfo=UTC)) is None
    assert stocks._coverage_status(conn, "TEST", datetime(2026, 7, 21, 14, tzinfo=UTC)) is None
    conn.execute("UPDATE stock_coverage_by_mode SET status='DATA_GAP',missing_bars=3")
    assert stocks._coverage_status(conn, "TEST", datetime(2026, 7, 21, 14, tzinfo=UTC)) is False
    conn.close()


def test_late_first_bar_after_rth_news_is_dirty():
    frame = _intraday_symbol()
    frame = frame[frame["timestamp"] >= pd.Timestamp("2026-07-14T14:00:00Z")].copy()
    event = _stock_event()
    event["published_at"] = event["available_at"] = "2026-07-14T13:31:00+00:00"
    result = stocks.evaluate_candidate(
        event=event, symbol="TEST", stock_bars=frame, daily_bars=_daily_frame(),
        spy_bars=_benchmark(), sector_bars=_benchmark(), sector="technology", sector_etf="XLK",
        coverage_clean=None, cfg=_stocks_cfg(), generated_at=datetime(2026, 7, 14, 20, tzinfo=UTC),
    )
    assert result["rejection_reason"] == "DATA_COVERAGE_DIRTY"
    assert result["is_clean_for_edge"] == 0


def test_migrations_are_idempotent_and_preserve_old_rows(tmp_path):
    db = tmp_path / "migrate.sqlite"
    conn = sqlite3.connect(db)
    conn.execute("CREATE TABLE stocks_catalyst_rs_shadow_outcomes (candidate_id TEXT PRIMARY KEY)")
    conn.execute("INSERT INTO stocks_catalyst_rs_shadow_outcomes VALUES ('old-stock')")
    stocks.ensure_tables(conn); stocks.ensure_tables(conn)
    assert conn.execute("SELECT candidate_id FROM stocks_catalyst_rs_shadow_outcomes").fetchone()[0] == "old-stock"
    assert "would_have_held_close_next_session" in {
        r[1] for r in conn.execute("PRAGMA table_info(stocks_catalyst_rs_shadow_outcomes)")}
    assert {"evidence_cohort", "source_trust_tier", "candidate_origin"}.issubset({
        r[1] for r in conn.execute("PRAGMA table_info(stocks_catalyst_rs_shadow_outcomes)")})
    conn.close()


def test_repeated_refresh_preserves_first_seen_window_and_latency():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE private_outcomes (candidate_id TEXT PRIMARY KEY, generated_at TEXT, "
                 "window TEXT, latency_seconds REAL)")
    conn.execute("INSERT INTO private_outcomes VALUES ('x','2026-07-15T10:00:00+00:00',"
                 "'forward_post_activation',12.0)")
    rows = [{"candidate_id": "x", "generated_at": "2026-07-15T12:00:00+00:00",
             "window": "historical_backfill", "latency_seconds": 7212.0}]
    preserve_first_observation(conn, "private_outcomes", rows)
    conn.close()
    assert rows[0]["generated_at"] == "2026-07-15T10:00:00+00:00"
    assert rows[0]["window"] == "forward_post_activation"
    assert rows[0]["latency_seconds"] == 12.0


def test_crypto_costs_prefer_actual_funding_events_over_fallback():
    entry_at = datetime(2026, 7, 15, 10, 0, tzinfo=UTC)
    bars = pd.DataFrame([{"timestamp": entry_at, "open": 100.0, "high": 100.1,
                          "low": 99.9, "close": 100.0, "volume": 1.0}])
    result = simulate_confirmed_close_entry(
        direction="long", entry=100.0, stop=99.0, tp1=101.0, tp2=102.0, tp3=103.0,
        future_candles=bars, symbol="BTC/USDT", fee_profile="bybit_non_vip_usdt_perp",
        funding_rate_8h=0.005, funding_intervals=1.0,
        funding_events=[{"event_at": (entry_at + timedelta(minutes=3)).isoformat(),
                         "received_at": (entry_at + timedelta(minutes=3)).isoformat(),
                         "funding_rate_8h": 0.0001}],
        entry_at=entry_at, bar_minutes=5, force_close=True,
    )
    assert result.funding_source == "actual_funding_events"
    assert result.funding_event_count == 1
    assert result.funding_estimated is False
    assert result.funding_usd > 0


def test_enabled_empty_refresh_never_mutates_forbidden_tables(tmp_path):
    db = tmp_path / "guard.sqlite"
    conn = sqlite3.connect(db)
    for table in ("proposed_signals", "signal_outcomes", "final_r", "paper_ledger", "live_routing"):
        conn.execute(f"CREATE TABLE {table}(id INTEGER PRIMARY KEY, value TEXT)")
        conn.execute(f"INSERT INTO {table}(value) VALUES ('stable')")
    conn.commit(); conn.close()
    before = {}
    conn = sqlite3.connect(db)
    for table in ("proposed_signals", "signal_outcomes", "final_r", "paper_ledger", "live_routing"):
        before[table] = conn.execute(f"SELECT * FROM {table}").fetchall()
    conn.close()

    scfg = _stocks_cfg()
    stocks.refresh(db=str(db), cfg=scfg, now=datetime(2026, 7, 15, tzinfo=UTC))
    conn = sqlite3.connect(db)
    for table, expected in before.items():
        assert conn.execute(f"SELECT * FROM {table}").fetchall() == expected
    conn.close()


def test_review_gate_is_never_automatic_promotion():
    now = datetime(2026, 8, 15, tzinfo=UTC)
    rows = [{"window": "forward_post_activation", "is_clean_for_edge": 1,
             "outcome_status": "closed", "net_pnl_usd": 3.0 if i < 25 else -1.0,
             "net_r": 0.1, "fees_usd": .1, "slippage_usd": .1, "funding_usd": 0,
             "entry_ts": f"2026-07-{(i % 20) + 1:02d}T14:00:00+00:00"} for i in range(30)]
    summary = clean_forward_summary(rows, activated_at="2026-07-01T00:00:00+00:00", now=now)
    assert summary["verdict"] == "REVIEW_ONLY"
    assert "PROMOTE" not in summary["verdict"]


def test_scheduler_places_new_strategies_after_required_data_steps():
    now = datetime(2026, 7, 15, 12, 0, tzinfo=UTC)
    steps = build_cycle_steps(now=now, crypto_only=False, include_long_horizon=False,
                              monitor_minutes=1, skip_reports=False)
    labels = [s[0] for s in steps]
    # Derivatives Reset v3 is owned by the continuous two-minute derivatives
    # monitor, immediately after it refreshes funding/OI and its own price cache.
    crypto_idx = next(i for i, label in enumerate(labels) if label.startswith("derivatives monitor"))
    assert crypto_idx < labels.index("intelligence layer update")
    assert "stocks catalyst RS continuation (isolated shadow)" not in labels
    assert "stocks earnings gap continuation (isolated shadow)" not in labels
    stocks_idx = labels.index("stocks intraday breakout one-bar (versioned Paper lane)")
    assert labels.index("news canonical events + influence policy (24h)") < stocks_idx
    assert steps[crypto_idx][2] == "derivatives_monitor"
    assert steps[stocks_idx][2] == "command_nonfatal"


def test_feature_flags_default_off_without_operator_config(monkeypatch, tmp_path):
    monkeypatch.setattr(stocks, "CONFIG_PATH", tmp_path / "missing_stocks.yaml")
    assert stocks.load_strategy_config()["feature_flag"] is False
