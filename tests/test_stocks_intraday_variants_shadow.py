from __future__ import annotations

import sqlite3
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pandas as pd

from scripts.run_default_market_schedule import build_cycle_steps
from src.execution import stocks_intraday_variants_shadow as variants
from src.models import TradeIdea


UTC = timezone.utc
START = datetime(2026, 7, 14, 13, 30, tzinfo=UTC)  # 09:30 New York


def _bars() -> pd.DataFrame:
    values = [
        # The source observation is at 09:30. The next 15m bar touches the
        # pullback zone, then the following bars hold/reclaim above VWAP.
        (102.0, 102.3, 101.7, 102.0, 1000.0),
        (101.2, 101.5, 100.5, 101.0, 1200.0),
        (101.0, 102.4, 100.9, 102.1, 1400.0),
        (102.1, 103.0, 101.0, 102.6, 1500.0),
        (102.6, 103.5, 102.3, 103.2, 1600.0),
        (103.2, 103.4, 102.4, 102.8, 1600.0),
    ]
    return pd.DataFrame([
        {"timestamp": START + timedelta(minutes=15 * i), "open": op, "high": hi,
         "low": lo, "close": close, "volume": volume}
        for i, (op, hi, lo, close, volume) in enumerate(values)
    ])


def _setup() -> dict:
    return {"entry_low": 100.5, "entry_high": 101.0, "invalidation": 99.0,
            "tp1": 103.0, "tp2": 104.0, "tp3": 105.0}


def _profile(rule: str, **kwargs) -> dict:
    return {"profile_id": f"test_{rule}", "entry_mode": "PULLBACK_LIMIT" if rule == "pullback_vwap_hold"
            else "BREAKOUT_CONTINUATION", "rule": rule, **kwargs}


def test_pullback_requires_touch_then_closed_vwap_hold():
    entry, reason = variants._profile_entry(
        profile=_profile("pullback_vwap_hold"), direction="long", setup=_setup(), bars=_bars(),
        decision_at=START + timedelta(minutes=15), bar_minutes=15,
    )
    assert reason is None
    assert entry is not None
    # It does not enter on the touch candle; it waits for the next closed hold.
    assert entry["idx"] == 2
    assert entry["entry"] == 102.1


def test_breakout_one_and_two_bar_profiles_are_distinct():
    one, one_reason = variants._profile_entry(
        profile=_profile("breakout_confirm", confirmation_bars=1), direction="long", setup=_setup(),
        bars=_bars(), decision_at=START + timedelta(minutes=15), bar_minutes=15,
    )
    two, two_reason = variants._profile_entry(
        profile=_profile("breakout_confirm", confirmation_bars=2), direction="long", setup=_setup(),
        bars=_bars(), decision_at=START + timedelta(minutes=15), bar_minutes=15,
    )
    assert one_reason is two_reason is None
    assert one is not None and two is not None
    assert one["idx"] < two["idx"]
    assert one["idx"] == 2
    assert two["idx"] == 3


def test_breakout_retest_waits_for_retest_after_first_close():
    entry, reason = variants._profile_entry(
        profile=_profile("breakout_retest"), direction="long", setup=_setup(), bars=_bars(),
        decision_at=START + timedelta(minutes=15), bar_minutes=15,
    )
    assert reason is None
    assert entry is not None
    # Index 2 is the first breakout close. Index 3 revisits the level and
    # closes back above it, which is the first valid entry.
    assert entry["idx"] == 3


def test_strict_breakout_profile_requires_confirmed_context():
    idea = _idea()
    idea.raw["intraday_actionability"] = {
        **idea.raw["intraday_actionability"],
        "market_context_status": "unknown",
    }
    profile = _profile("breakout_confirm", confirmation_bars=1, require_market_sector_confirmed=True)
    row = variants.evaluate_idea(
        cfg=_cfg(), profile=profile, idea=idea, stock_bars=_bars(),
        generated_at=START + timedelta(hours=1), window="forward_post_activation",
    )
    assert row["rejection_reason"] == "MARKET_CONTEXT_UNAVAILABLE"
    assert row["is_clean_for_edge"] == 0


def test_strict_breakout_profile_rejects_weak_confirmation_body():
    profile = _profile(
        "breakout_confirm", confirmation_bars=1, min_body_atr=0.10,
        min_close_location=0.65, min_rvol=1.0, rvol_lookback=1,
        max_trigger_extension_atr=1.0, max_stop_atr=2.0,
    )
    bars = _bars()
    # The first qualifying close is above trigger/VWAP, but it closes in the
    # middle of the bar, so a strict quality profile cannot call it momentum.
    bars.loc[2, ["open", "high", "low", "close"]] = [101.9, 102.5, 100.9, 101.8]
    entry, reason = variants._profile_entry(
        profile=profile, direction="long", setup=_setup(), bars=bars,
        decision_at=START + timedelta(minutes=15), bar_minutes=15,
    )
    assert entry is None
    assert reason == "CONFIRMATION_BODY_TOO_WEAK"


def _idea() -> SimpleNamespace:
    return SimpleNamespace(
        symbol="TEST", direction="long", tier="C", generated_at=START.isoformat(),
        raw={
            "pre_gate_tier": "A", "setup": _setup(),
            "candidate": {"sector": "technology", "sector_etf": "XLK"},
            "intraday_actionability": {"market_context_status": "ok", "sector_confirmation_status": "confirmed",
                                        "session_phase": "morning", "liquidity_status": "ok", "catalyst_quality": "medium"},
        },
    )


def _cfg() -> dict:
    cfg = variants.load_strategy_config()
    cfg.update(feature_flag=True, shadow_symbols=["TEST"], refresh_min_interval_minutes=0,
               profiles=[_profile("pullback_vwap_hold")])
    return cfg


def test_dirty_coverage_is_excluded_from_edge():
    broken = _bars().drop(index=[2, 3]).reset_index(drop=True)
    row = variants.evaluate_idea(cfg=_cfg(), profile=_profile("pullback_vwap_hold"), idea=_idea(),
                                 stock_bars=broken, generated_at=START + timedelta(hours=1),
                                 window="forward_post_activation")
    assert row["rejection_reason"] == "DATA_COVERAGE_DIRTY"
    assert row["is_clean_for_edge"] == 0


def test_partial_rth_cache_does_not_force_a_premature_time_exit():
    row = variants.evaluate_idea(
        cfg=_cfg(), profile=_profile("pullback_vwap_hold"), idea=_idea(), stock_bars=_bars(),
        generated_at=START + timedelta(hours=5), window="forward_post_activation",
    )
    assert row["eligibility_status"] == "eligible"
    assert row["outcome_status"] == "open"
    assert row["close_reason"] == "still_open"


def test_next_day_refresh_closes_intraday_trade_after_final_rth_bar_arrives(tmp_path):
    db = tmp_path / "late-session-close.sqlite"
    cfg = _cfg()
    partial = _bars()
    first = variants.refresh(
        db=str(db), cfg=cfg, ideas=[_idea()], bars_by_symbol={"TEST": partial},
        now=START + timedelta(hours=2), force=True,
    )
    assert first["rows"][0]["outcome_status"] == "open"

    tail_start = partial.iloc[-1]["timestamp"] + timedelta(minutes=15)
    final_bars = pd.DataFrame([{
        "timestamp": tail_start + timedelta(minutes=15 * i),
        "open": 102.8, "high": 102.9, "low": 102.6, "close": 102.7, "volume": 1800.0,
    } for i in range(21)])
    second = variants.refresh(
        db=str(db), cfg=cfg, ideas=[],
        bars_by_symbol={"TEST": pd.concat([partial, final_bars], ignore_index=True)},
        now=START + timedelta(days=1, hours=2), force=True,
    )
    assert len(second["rows"]) == 1
    assert second["rows"][0]["outcome_status"] == "closed"
    assert second["rows"][0]["close_reason"] == "time_exit"


def test_prior_sessions_cannot_shift_current_session_confirmation_index():
    prior = _bars().copy()
    prior["timestamp"] = prior["timestamp"] - pd.Timedelta(days=1)
    row = variants.evaluate_idea(
        cfg=_cfg(), profile=_profile("pullback_vwap_hold"), idea=_idea(),
        stock_bars=pd.concat([prior, _bars()], ignore_index=True), generated_at=START + timedelta(hours=2),
        window="forward_post_activation",
    )
    assert row["eligibility_status"] == "eligible"
    assert row["entry_ts"] == "2026-07-14T14:15:00+00:00"


def test_private_shadow_refresh_never_mutates_authoritative_trade_tables(tmp_path):
    db = tmp_path / "shadow.sqlite"
    conn = sqlite3.connect(db)
    for table in ("proposed_signals", "signal_outcomes", "final_r", "paper_ledger", "live_routing"):
        conn.execute(f"CREATE TABLE {table}(id INTEGER PRIMARY KEY, value TEXT)")
        conn.execute(f"INSERT INTO {table}(value) VALUES ('stable')")
    conn.commit()
    before = {table: conn.execute(f"SELECT * FROM {table}").fetchall()
              for table in ("proposed_signals", "signal_outcomes", "final_r", "paper_ledger", "live_routing")}
    conn.close()

    result = variants.refresh(
        db=str(db), cfg=_cfg(), ideas=[_idea()], bars_by_symbol={"TEST": _bars()},
        now=START + timedelta(hours=2), force=True,
    )
    assert result["paper_unchanged"] is True
    conn = sqlite3.connect(db)
    for table, expected in before.items():
        assert conn.execute(f"SELECT * FROM {table}").fetchall() == expected
    assert conn.execute("SELECT COUNT(*) FROM stocks_intraday_variant_shadow_outcomes").fetchone()[0] == 1
    conn.close()


def test_migration_is_idempotent_and_keeps_old_rows(tmp_path):
    db = tmp_path / "migrate.sqlite"
    conn = sqlite3.connect(db)
    conn.execute("CREATE TABLE stocks_intraday_variant_shadow_outcomes (candidate_id TEXT PRIMARY KEY)")
    conn.execute("INSERT INTO stocks_intraday_variant_shadow_outcomes VALUES ('old-row')")
    variants.ensure_tables(conn)
    variants.ensure_tables(conn)
    assert conn.execute("SELECT candidate_id FROM stocks_intraday_variant_shadow_outcomes").fetchone()[0] == "old-row"
    assert "net_pnl_usd" in {r[1] for r in conn.execute("PRAGMA table_info(stocks_intraday_variant_shadow_outcomes)")}
    conn.close()


def test_primary_catalyst_readiness_counts_only_linked_cluster_primary_rows():
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE news_canonical_events (asset_class TEXT, effective_at TEXT, "
        "source_quality TEXT, is_cluster_primary INTEGER, linkage_allowed INTEGER)"
    )
    stamp = START.isoformat()
    conn.executemany("INSERT INTO news_canonical_events VALUES (?,?,?,?,?)", [
        ("stocks", stamp, "reputable", 1, 1),
        ("stocks", stamp, "reputable", 1, 0),
        ("stocks", stamp, "secondary", 0, 1),
    ])
    result = variants._primary_catalyst_readiness(conn, START + timedelta(hours=1))
    conn.close()
    assert result["canonical_rows"] == 3
    assert result["linked_primary_events"] == 1
    assert result["primary_or_reputable_events"] == 1


def test_outcome_upsert_keeps_first_forward_window_and_decision_time(tmp_path):
    db = tmp_path / "first-observation.sqlite"
    conn = sqlite3.connect(db)
    variants.ensure_tables(conn)
    cfg = _cfg()
    first = variants.evaluate_idea(
        cfg=cfg, profile=_profile("pullback_vwap_hold"), idea=_idea(), stock_bars=_bars(),
        generated_at=START + timedelta(minutes=45), window="forward_post_activation",
    )
    variants._upsert_outcomes(conn, [first])
    later = dict(first)
    later.update(generated_at=(START + timedelta(hours=3)).isoformat(), window="historical_backfill",
                 decision_at=(START + timedelta(hours=1)).isoformat(), outcome_status="closed", net_pnl_usd=12.34)
    variants._upsert_outcomes(conn, [later])
    row = conn.execute("SELECT generated_at,window,decision_at,outcome_status,net_pnl_usd "
                       "FROM stocks_intraday_variant_shadow_outcomes").fetchone()
    conn.close()
    assert row[0] == first["generated_at"]
    assert row[1] == "forward_post_activation"
    assert row[2] == first["decision_at"]
    assert row[3:] == ("closed", 12.34)


def test_scheduler_runs_variants_after_stock_data_and_as_nonfatal():
    now = datetime(2026, 7, 15, 12, tzinfo=UTC)
    steps = build_cycle_steps(now=now, crypto_only=False, include_long_horizon=False,
                              monitor_minutes=1, skip_reports=False)
    labels = [step[0] for step in steps]
    label = "stocks intraday VWAP/confirmed-breakout variants (isolated shadow)"
    assert label not in labels


def test_shadow_only_stock_pipeline_does_not_save_or_register_ideas(monkeypatch, tmp_path):
    """The wider Shadow scout may reuse analysis, never Paper persistence."""
    from src.config import load_config
    from src.stocks.pipelines import stocks_pipeline as pipe

    class Agent:
        def __init__(self, *args, **kwargs):
            pass

        def run(self, *args, **kwargs):
            return {}

    class Earnings:
        def __init__(self, *args, **kwargs):
            pass

        def collect(self, *args, **kwargs):
            return SimpleNamespace(events=[], failed_symbols=[])

    idea = TradeIdea(
        symbol="TEST", direction="long", score=90, confidence="high", risk_level="low", timeframe="15m",
        tier="A", mode="intraday", asset_class="stocks", thesis="test", evidence=[], counterarguments=[],
        entry_plan="test", invalidation="99", targets=[], what_to_monitor=[], avoid_conditions=[], data_sources_used=[],
    )

    class IdeaAgent(Agent):
        def run(self, *args, **kwargs):
            return {"ideas": [idea.model_dump()]}

    for name in ("StocksMarketRegimeAgent", "SectorRotationAgent", "StockRelativeStrengthAgent",
                 "EarningsRiskAgent", "CompanyNewsAgent", "StockTechnicalAgent", "StockRiskAgent", "StockScoringAgent"):
        monkeypatch.setattr(pipe, name, Agent)
    monkeypatch.setattr(pipe, "StockTradeIdeaAgent", IdeaAgent)
    monkeypatch.setattr(pipe, "EarningsCalendarCollector", Earnings)
    base = load_config()
    settings = dict(base.settings)
    settings["data"] = {**dict(base.settings.get("data") or {}), "db_path": str(tmp_path / "stock-shadow.sqlite")}
    pipeline = pipe.StocksPipeline(replace(base, settings=settings))
    calls: list[str] = []
    monkeypatch.setattr(pipeline.db, "save_trade_ideas", lambda *args, **kwargs: calls.append("ideas"))
    monkeypatch.setattr(pipe, "register_ideas", lambda *args, **kwargs: calls.append("signals"))

    result = pipeline.run_report(mode="intraday", symbols=["TEST"], skip_data_update=True, shadow_only=True)
    assert len(result.ideas) == 1
    assert result.report_path is None
    assert calls == []
