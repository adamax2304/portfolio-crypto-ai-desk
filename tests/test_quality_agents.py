from __future__ import annotations

import json
import sqlite3
from dataclasses import replace
from copy import deepcopy
from datetime import datetime, timedelta, timezone

from src.quality_agents.config import (
    DEFAULTS,
    QualityAgentsConfig,
    load_quality_agents_config,
)
from src.quality_agents.event_risk_agent import EventRiskAgent
from src.quality_agents.execution_sanity_agent import ExecutionSanityAgent
from src.quality_agents.market_regime_agent import MarketRegimeAgent
from src.quality_agents.news_entity_agent import NewsEntityAgent
from src.quality_agents.llm_advisory import refresh_openrouter_advisory
from src.quality_agents.llm_cached_advisory_agent import LLMCachedAdvisoryAgent
from src.llm_router import LLMRouter
from src.llm_router.config import load_llm_router_config
from src.llm_router.provider import ProviderResult
from src.quality_agents.post_trade_forensics_agent import PostTradeForensicsAgent
from src.quality_agents.reducer import reduce_verdicts
from src.quality_agents.report import build_effectiveness_report
from src.quality_agents.runner import evaluate_signal, record_watchdog_observations
from src.quality_agents.schemas import SignalContext, Verdict, utc_now
from src.quality_agents.store import (
    assign_experiment_cohorts,
    connect,
    ensure_tables,
    prune,
    upsert_execution_incident,
)


def _context(*, payload: dict | None = None) -> SignalContext:
    return SignalContext.from_records(
        {
            "signal_id": "sig_quality_1",
            "symbol": "BTC/USDT",
            "asset_class": "crypto",
            "mode": "intraday",
            "direction": "long",
        },
        payload or {},
        decision_at=datetime(2026, 9, 19, 12, 0, tzinfo=timezone.utc),
    )


def _enabled_test_router(*, db_path, provider) -> LLMRouter:
    cfg = load_llm_router_config()
    return LLMRouter(
        cfg=replace(cfg, raw={**cfg.raw, "enabled": True}),
        db_path=db_path,
        provider=provider,
    )


def test_production_quality_config_disables_llm_advisory() -> None:
    cfg = load_quality_agents_config()
    assert cfg.agent_enabled("llm_cached_advisory") is False
    assert cfg.llm_advisory_refresh["enabled"] is False


def test_experiment_assignment_is_stable_and_cost_bounded(tmp_path) -> None:
    db = tmp_path / "quality.sqlite"
    signal_ids = [f"sig_{index}" for index in range(10)]
    now = datetime(2026, 9, 25, 12, 50, tzinfo=timezone.utc)
    with connect(db) as conn:
        first = assign_experiment_cohorts(
            conn,
            experiment_name="stocks_preus_gemini_v1",
            session_key="2026-09-25",
            signal_ids=signal_ids,
            treatment_count=5,
            assigned_at=now,
            assignment_salt="test",
        )
        conn.commit()
        second = assign_experiment_cohorts(
            conn,
            experiment_name="stocks_preus_gemini_v1",
            session_key="2026-09-25",
            signal_ids=list(reversed(signal_ids)),
            treatment_count=5,
            assigned_at=now + timedelta(minutes=1),
            assignment_salt="test",
        )
    assert first == {signal_id: second[signal_id] for signal_id in signal_ids}
    assert sum(cohort == "treatment" for cohort in first.values()) == 5
    assert sum(cohort == "control" for cohort in first.values()) == 5


def test_execution_hard_block_is_recommendation_only_in_shadow() -> None:
    cfg = QualityAgentsConfig(DEFAULTS)
    context = _context(payload={
        "entry_used": 100,
        "stop": 105,
        "tp1": 101,
        "tp2": 102,
        "tp3": 103,
        "size_weight": 1,
        "current_price_revalidated": True,
        "entry_time_basis": "point_in_time_current_bar",
    })
    verdict = ExecutionSanityAgent().evaluate(sqlite3.connect(":memory:"), context, cfg)
    assert verdict.verdict == Verdict.BLOCK_HARD
    assert "INVALID_DIRECTIONAL_GEOMETRY" in verdict.reason_codes
    reduced = reduce_verdicts([("v1", verdict)], cfg)
    assert reduced.recommended_action.value == "BLOCK_HARD"
    assert reduced.applied_action.value == "ALLOW"


def test_event_halt_is_point_in_time_and_objective() -> None:
    cfg = QualityAgentsConfig(DEFAULTS)
    context = _context()
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE news_canonical_events("
        "news_item_id INTEGER,event_id TEXT,title TEXT,source TEXT,published_at TEXT,"
        "available_at TEXT,effective_at TEXT,expires_at TEXT,event_latency_class TEXT,"
        "trusted_symbols_json TEXT,event_type TEXT,direction_hint TEXT,source_quality TEXT,"
        "confidence REAL,linkage_allowed INTEGER,linkage_reason TEXT,risk_action TEXT)"
    )
    conn.execute(
        "INSERT INTO news_canonical_events VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (
            1, "evt_1", "Exchange suspends BTC contract", "MEXC announcement",
            "2026-09-19T11:50:00+00:00", "2026-09-19T11:51:00+00:00",
            "2026-09-19T11:51:00+00:00", "2026-09-20T00:00:00+00:00",
            "FAST_EVENT", '["BTC"]', "maintenance", "bearish", "exchange",
            0.95, 1, "trusted_directional_event", "operator_review",
        ),
    )
    verdict = EventRiskAgent().evaluate(conn, context, cfg)
    assert verdict.verdict == Verdict.BLOCK_HARD
    assert verdict.reason_codes == ("EVENT_HALT_ACTIVE",)


def test_runner_is_idempotent_and_persists_all_signal_verdicts(tmp_path) -> None:
    db = tmp_path / "quality.sqlite"
    signal = {
        "signal_id": "sig_runner_1",
        "symbol": "ETH/USDT",
        "asset_class": "crypto",
        "mode": "intraday",
        "direction": "long",
        "tier": "B",
    }
    payload = {
        "decision_at": "2026-09-19T12:00:00+00:00",
        "paper_execution_entry_mode": "BREAKOUT_CONTINUATION",
        "entry_used": 2000,
        "stop": 1980,
        "tp1": 2020,
        "tp2": 2040,
        "tp3": 2060,
        "entry_age_seconds": 2,
        "entry_time_basis": "point_in_time_current_bar",
        "current_price_revalidated": True,
        "size_weight": 0.5,
    }
    first = evaluate_signal(signal, payload, db=db)
    second = evaluate_signal(signal, payload, db=db)
    assert first["applied_action"] == "ALLOW"
    assert second["applied_action"] == "ALLOW"
    with connect(db) as conn:
        ensure_tables(conn)
        assert conn.execute("SELECT COUNT(*) FROM quality_agent_runs").fetchone()[0] == 4
        assert conn.execute("SELECT COUNT(*) FROM quality_agent_signal_verdicts").fetchone()[0] == 4
        assert conn.execute(
            "SELECT COUNT(*) FROM quality_agent_runs WHERE agent_name='llm_cached_advisory'"
        ).fetchone()[0] == 0
        assert conn.execute("SELECT COUNT(*) FROM quality_agent_reducer_decisions").fetchone()[0] == 1


def test_stale_or_missing_context_remains_fail_open(tmp_path) -> None:
    db = tmp_path / "quality.sqlite"
    result = evaluate_signal(
        {
            "signal_id": "sig_missing_context",
            "symbol": "AAPL",
            "asset_class": "stocks",
            "mode": "intraday",
            "direction": "long",
        },
        {
            "entry_used": 200,
            "stop": 198,
            "tp1": 202,
            "tp2": 204,
            "tp3": 206,
            "entry_age_seconds": 1,
            "entry_time_basis": "point_in_time_current_bar",
            "current_price_revalidated": True,
            "size_weight": 1,
        },
        db=db,
    )
    assert result["status"] == "OK"
    assert result["applied_action"] == "ALLOW"
    assert any(
        row["verdict"] == "INSUFFICIENT_DATA" for row in result["verdicts"]
    )


def test_news_lookup_filters_by_symbol_before_limit() -> None:
    cfg = QualityAgentsConfig(DEFAULTS)
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE news_canonical_events("
        "news_item_id INTEGER,event_id TEXT,title TEXT,source TEXT,published_at TEXT,"
        "available_at TEXT,effective_at TEXT,expires_at TEXT,event_latency_class TEXT,"
        "trusted_symbols_json TEXT,event_type TEXT,direction_hint TEXT,source_quality TEXT,"
        "confidence REAL,linkage_allowed INTEGER,linkage_reason TEXT,risk_action TEXT)"
    )
    conn.execute(
        "INSERT INTO news_canonical_events VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (1, "btc_old", "BTC catalyst", "exchange", "2026-09-19T11:40:00+00:00",
         "2026-09-19T11:41:00+00:00", "2026-09-19T11:41:00+00:00",
         "2026-09-20T00:00:00+00:00", "FAST_EVENT", '["BTC"]', "listing",
         "bullish", "exchange", 0.9, 1, "trusted", "none"),
    )
    for item_id in range(2, 20):
        conn.execute(
            "INSERT INTO news_canonical_events VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (item_id, f"other_{item_id}", "Other", "wire", "2026-09-19T11:50:00+00:00",
             "2026-09-19T11:51:00+00:00", "2026-09-19T11:51:00+00:00",
             "2026-09-20T00:00:00+00:00", "FAST_EVENT", '["ETH"]', "other",
             "neutral", "wire", 0.5, 1, "trusted", "none"),
        )
    verdict = NewsEntityAgent().evaluate(conn, _context(), cfg)
    assert verdict.verdict == Verdict.SUPPORT
    assert verdict.evidence["matched_event_count"] == 1


def test_market_regime_uses_only_point_in_time_snapshot() -> None:
    cfg = QualityAgentsConfig(DEFAULTS)
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE market_dashboard_snapshots("
        "id INTEGER PRIMARY KEY,timestamp TEXT,crypto_market_mode TEXT,crypto_regime TEXT,"
        "stocks_market_mode TEXT,stocks_regime TEXT,confidence REAL,generated_by TEXT,"
        "spy_trend TEXT,qqq_trend TEXT,vix REAL,raw_json TEXT)"
    )
    conn.execute(
        "INSERT INTO market_dashboard_snapshots VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
        (1, "2026-09-19T11:30:00+00:00", "risk_on", "bullish", "neutral", "range",
         0.8, "test", None, None, None, '{"btc_trend":"up"}'),
    )
    conn.execute(
        "INSERT INTO market_dashboard_snapshots VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
        (2, "2026-09-19T12:30:00+00:00", "risk_off", "bearish", "neutral", "range",
         0.8, "future", None, None, None, '{"btc_trend":"down"}'),
    )
    verdict = MarketRegimeAgent().evaluate(conn, _context(), cfg)
    assert verdict.verdict == Verdict.SUPPORT
    assert verdict.evidence["snapshot_id"] == 1


def test_post_trade_forensics_separates_stop_hypothesis() -> None:
    finding = PostTradeForensicsAgent().classify(
        {
            "result_r": -1.0,
            "close_reason": "original_stop_hit",
            "execution_validity": "valid",
            "touch_r": 0.8,
            "entry_drift_bps": 5,
        },
        [],
    )
    assert finding.outcome == "loss"
    assert finding.primary_category == "stop_too_tight_hypothesis"


def test_watchdog_observations_are_recorded_and_recovered_without_alert_ownership(tmp_path) -> None:
    db = tmp_path / "quality.sqlite"
    with connect(db) as conn:
        ensure_tables(conn)
        conn.execute(
            "CREATE TABLE mexc_canary_decisions("
            "decision_id TEXT PRIMARY KEY,signal_id TEXT,symbol TEXT)"
        )
        conn.execute(
            "INSERT INTO mexc_canary_decisions VALUES('decision_1','sig_1','BTC_USDT')"
        )
        first = record_watchdog_observations(conn, [{
            "key": "position_stop_missing:decision_1",
            "severity": "CRITICAL",
            "title": "missing stop",
            "detail": "no stop id",
            "decision_id": "decision_1",
            "symbol": "BTC_USDT",
            "payload": {},
            "active": True,
        }])
        assert first == {"recorded": 1, "recovered": 0}
        row = conn.execute(
            "SELECT incident_type,status,signal_id FROM quality_agent_execution_incidents"
        ).fetchone()
        assert tuple(row) == ("PROTECTIVE_STOP_MISSING", "ACTIVE", "sig_1")
        second = record_watchdog_observations(conn, [])
        assert second == {"recorded": 0, "recovered": 1}
        assert conn.execute(
            "SELECT status FROM quality_agent_execution_incidents"
        ).fetchone()[0] == "RECOVERED"


def test_effectiveness_report_matches_live_decision_insert_stage(tmp_path) -> None:
    db = tmp_path / "quality.sqlite"
    signal = {
        "signal_id": "sig_report_1",
        "symbol": "ETH/USDT",
        "asset_class": "crypto",
        "mode": "intraday",
        "direction": "long",
    }
    evaluate_signal(signal, {
        "paper_execution_entry_mode": "BREAKOUT_CONTINUATION",
        "entry_used": 2000,
        "stop": 1980,
        "tp1": 2020,
        "tp2": 2040,
        "tp3": 2060,
        "entry_age_seconds": 1,
        "entry_time_basis": "point_in_time_current_bar",
        "current_price_revalidated": True,
        "size_weight": 1,
    }, db=db, stage="live_decision_insert")
    with connect(db) as conn:
        conn.execute(
            "CREATE TABLE paper_execution_outcomes("
            "signal_id TEXT PRIMARY KEY,paper_execution_r REAL,close_reason TEXT)"
        )
        conn.execute(
            "INSERT INTO paper_execution_outcomes VALUES('sig_report_1',1.25,'tp_hit')"
        )
        conn.commit()
    _, summary = build_effectiveness_report(db=db, lookback_days=30)
    assert summary["effectiveness"]
    assert sum(
        bucket["n"]
        for agent in summary["effectiveness"].values()
        for bucket in agent.values()
    ) == 4


def test_openrouter_advisory_refresh_records_cache_and_hot_path_reads_it(tmp_path) -> None:
    class FakeProvider:
        def call(self, *, model, task, **kwargs) -> ProviderResult:
            assert "trading-desk" in task.system_prompt
            assert task.user_payload["symbol"] == "BTC/USDT"
            return ProviderResult(
                payload={
                    "verdict": "SUPPORT",
                    "confidence": 0.86,
                    "reason_codes": ["trusted_directional_news"],
                    "direction_hint": "bullish",
                    "event_type": "listing",
                    "event_latency_class": "FAST_EVENT",
                    "risk_action": "none",
                    "short_rationale": "Trusted directional event supports the setup.",
                },
                text="{}",
                model=model.model_id,
                latency_ms=12.5,
            )

    raw = deepcopy(DEFAULTS)
    raw["llm_advisory_refresh"]["enabled"] = True
    raw["llm_advisory_refresh"]["lookback_hours"] = 2
    raw["llm_advisory_refresh"]["max_events"] = 3
    raw["llm_advisory_refresh"]["max_assessments_per_run"] = 8
    cfg = QualityAgentsConfig(raw)
    db = tmp_path / "quality.sqlite"
    now = utc_now()
    with connect(db) as conn:
        ensure_tables(conn)
        conn.execute(
            "CREATE TABLE news_canonical_events("
            "news_item_id INTEGER,event_id TEXT,title TEXT,source TEXT,published_at TEXT,"
            "available_at TEXT,effective_at TEXT,expires_at TEXT,event_latency_class TEXT,"
            "trusted_symbols_json TEXT,related_symbols_json TEXT,event_type TEXT,"
            "direction_hint TEXT,source_quality TEXT,confidence REAL,importance REAL,"
            "linkage_allowed INTEGER,linkage_reason TEXT,risk_action TEXT,asset_class TEXT,"
            "content TEXT)"
        )
        conn.execute(
            "CREATE TABLE proposed_signals("
            "signal_id TEXT,symbol TEXT,asset_class TEXT,mode TEXT,tier TEXT,status TEXT,"
            "score REAL,created_at TEXT,updated_at TEXT)"
        )
        conn.execute(
            "INSERT INTO proposed_signals VALUES(?,?,?,?,?,?,?,?,?)",
            (
                "sig_llm_cache", "BTC/USDT", "crypto", "intraday", "B",
                "waiting_for_entry", 75.0, now.isoformat(), now.isoformat(),
            ),
        )
        conn.execute(
            "INSERT INTO news_canonical_events VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                1, "evt_btc", "BTC listing catalyst", "exchange",
                now.isoformat(), now.isoformat(), now.isoformat(),
                (now + timedelta(hours=2)).isoformat(), "FAST_EVENT",
                '["BTC"]', "[]", "listing", "bullish", "exchange", 0.91, 0.8,
                1, "trusted", "none", "crypto", "BTC listed on a new venue.",
            ),
        )
        conn.execute(
            "INSERT INTO news_canonical_events VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                2, "evt_eth", "Unrelated ETH catalyst", "exchange",
                now.isoformat(), now.isoformat(), now.isoformat(),
                (now + timedelta(hours=2)).isoformat(), "FAST_EVENT",
                '["ETH"]', "[]", "listing", "bullish", "exchange", 0.91, 0.8,
                1, "trusted", "none", "crypto", "ETH listed on a new venue.",
            ),
        )
        conn.commit()
    router = _enabled_test_router(db_path=db, provider=FakeProvider())
    result = refresh_openrouter_advisory(db=db, cfg=cfg, router=router)
    assert result["status"] == "OK"
    assert result["recorded"] == 1
    assert result["active_symbols"] == 1
    assert result["targets"] == 1
    with connect(db) as conn:
        ensure_tables(conn)
        count = conn.execute("SELECT COUNT(*) FROM quality_agent_llm_assessments").fetchone()[0]
        assert count == 1
        context = SignalContext.from_records(
            {
                "signal_id": "sig_llm_cache",
                "symbol": "BTC/USDT",
                "asset_class": "crypto",
                "mode": "intraday",
                "direction": "long",
            },
            {},
            decision_at=utc_now(),
        )
        verdict = LLMCachedAdvisoryAgent().evaluate(conn, context, cfg)
    assert verdict.verdict == Verdict.SUPPORT
    assert "LLM_TRUSTED_DIRECTIONAL_NEWS" in verdict.reason_codes


def test_openrouter_advisory_budget_pause_is_explicit_and_does_not_call_provider(tmp_path) -> None:
    class BudgetProvider:
        calls = 0

        def daily_usage_usd(self) -> float:
            return 999.0

        def call(self, **kwargs) -> ProviderResult:
            self.calls += 1
            raise AssertionError("budget enforcement should stop before provider.call")

    raw = deepcopy(DEFAULTS)
    raw["llm_advisory_refresh"]["enabled"] = True
    raw["llm_advisory_refresh"]["lookback_hours"] = 2
    raw["llm_advisory_refresh"]["max_events"] = 3
    raw["llm_advisory_refresh"]["max_assessments_per_run"] = 3
    cfg = QualityAgentsConfig(raw)
    db = tmp_path / "quality.sqlite"
    now = utc_now()
    with connect(db) as conn:
        ensure_tables(conn)
        conn.execute(
            "CREATE TABLE news_canonical_events("
            "news_item_id INTEGER,event_id TEXT,title TEXT,source TEXT,published_at TEXT,"
            "available_at TEXT,effective_at TEXT,expires_at TEXT,event_latency_class TEXT,"
            "trusted_symbols_json TEXT,related_symbols_json TEXT,event_type TEXT,"
            "direction_hint TEXT,source_quality TEXT,confidence REAL,importance REAL,"
            "linkage_allowed INTEGER,linkage_reason TEXT,risk_action TEXT,asset_class TEXT,"
            "content TEXT)"
        )
        conn.execute(
            "CREATE TABLE proposed_signals("
            "signal_id TEXT,symbol TEXT,asset_class TEXT,mode TEXT,tier TEXT,status TEXT,"
            "score REAL,created_at TEXT,updated_at TEXT)"
        )
        for item_id, symbol in enumerate(("BTC", "ETH"), start=1):
            conn.execute(
                "INSERT INTO news_canonical_events VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    item_id, f"evt_{symbol}", f"{symbol} catalyst", "exchange",
                    now.isoformat(), now.isoformat(), now.isoformat(),
                    (now + timedelta(hours=2)).isoformat(), "FAST_EVENT",
                    json.dumps([symbol]), "[]", "listing", "bullish", "exchange",
                    0.91, 0.8, 1, "trusted", "none", "crypto",
                    f"{symbol} listed on a new venue.",
                ),
            )
            conn.execute(
                "INSERT INTO proposed_signals VALUES(?,?,?,?,?,?,?,?,?)",
                (
                    f"sig_{symbol}", f"{symbol}/USDT", "crypto", "intraday", "B",
                    "waiting_for_entry", 75.0, now.isoformat(), now.isoformat(),
                ),
            )
        conn.commit()
    provider = BudgetProvider()
    router = _enabled_test_router(db_path=db, provider=provider)

    result = refresh_openrouter_advisory(db=db, cfg=cfg, router=router)

    assert result["status"] == "BUDGET_PAUSED"
    assert result["errors"] == 1
    assert result["recorded"] == 1
    assert result["budget_skipped"] >= 1
    assert result["error"].startswith("llm_daily_budget_exhausted:total:")
    assert provider.calls == 0


def test_retention_prunes_old_observed_incidents(tmp_path) -> None:
    db = tmp_path / "quality.sqlite"
    with connect(db) as conn:
        ensure_tables(conn)
        upsert_execution_incident(
            conn,
            incident_key="observed:old",
            incident_type="INVALID_SYMBOL",
            severity="WARNING",
            stage="live_decision_insert",
            detail={},
            status="OBSERVED",
            now=datetime(2025, 1, 1, tzinfo=timezone.utc),
        )
        removed = prune(conn, {"resolved_incident_days": 90})
        assert removed["quality_agent_execution_incidents"] == 1
