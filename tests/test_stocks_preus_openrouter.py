from __future__ import annotations

import json
import sqlite3
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from src.execution import stocks_preus_review as preus
from src.llm_router import LLMRouter, LLMTier
from src.llm_router.config import load_llm_router_config
from src.llm_router.provider import LLMProviderError, ProviderResult
from src.quality_agents.stocks_preus_openrouter import (
    PROMPT_VERSION,
    SCOPE,
    run_preus_openrouter_review,
)


NOW = datetime(2026, 8, 20, 12, 55, tzinfo=timezone.utc)  # 08:55 ET


def _enabled_test_router(*, db_path: Path, provider) -> LLMRouter:
    cfg = load_llm_router_config()
    return LLMRouter(
        cfg=replace(cfg, raw={**cfg.raw, "enabled": True}),
        db_path=db_path,
        provider=provider,
    )


def _make_db(path: Path) -> None:
    raw = {
        "thesis": "AAPL long with aligned technical structure",
        "structured": {
            "sector": "technology",
            "sector_etf": "XLK",
            "rs_vs_spy": 1.2,
            "rs_vs_sector": 0.8,
            "volume_ratio": 1.4,
        },
        "raw_score": {"components": {"technical_setup": 20}, "blocks": []},
        "raw_setup": {
            "entry_low": 190.0,
            "entry_high": 191.0,
            "invalidation": 187.0,
            "tp1": 195.0,
        },
        "pre_gate_tier": "B",
        "cap_reasons": [f"{preus.PLAN_MARKER}: US cash session closed"],
    }
    with sqlite3.connect(path) as conn:
        conn.execute("""CREATE TABLE proposed_signals (
            signal_id TEXT PRIMARY KEY, symbol TEXT, asset_class TEXT, mode TEXT,
            direction TEXT, tier TEXT, score REAL, status TEXT, created_at TEXT,
            updated_at TEXT, entry_trigger REAL, suggested_entry REAL,
            entry_low REAL, entry_high REAL, stop_loss REAL, invalidation REAL,
            raw_idea_json TEXT
        )""")
        conn.execute("""CREATE TABLE stocks_paper_decision_snapshots (
            signal_id TEXT PRIMARY KEY, funnel_state TEXT,
            target_session_open_at TEXT, target_session_close_at TEXT
        )""")
        created = (NOW - timedelta(minutes=15)).isoformat()
        conn.execute(
            "INSERT INTO proposed_signals VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                "sig-preus-1", "AAPL", "stocks", "intraday", "long", "C", 64.0,
                "waiting_for_entry", created, created, 191.0, 191.0, 190.0,
                191.0, 187.0, 187.0, json.dumps(raw),
            ),
        )
        conn.execute(
            "INSERT INTO stocks_paper_decision_snapshots VALUES(?,?,?,?)",
            (
                "sig-preus-1", "PREOPEN_PLAN",
                datetime(2026, 8, 20, 13, 30, tzinfo=timezone.utc).isoformat(),
                datetime(2026, 8, 20, 20, 0, tzinfo=timezone.utc).isoformat(),
            ),
        )


def _bundle() -> dict:
    return {
        "eligible": [{
            "signal_id": "sig-preus-1",
            "symbol": "AAPL",
            "direction": "long",
            "tier": "C",
            "pre_gate_tier": "B",
            "base_score": 64.0,
            "funnel_state": "PREOPEN_PLAN",
            "promotable": True,
            "created_at": (NOW - timedelta(minutes=15)).isoformat(),
            "entry_trigger": 191.0,
            "stop_loss": 187.0,
            "cap_reasons": [f"{preus.PLAN_MARKER}: US cash session closed"],
            "paper_entry_profile": "stocks_intraday_breakout_1bar_paper_v1",
            "paper_entry_confirmation": "closed_bar",
        }],
        "excluded": [],
        "generated_at": NOW.isoformat(),
        "status": "ok",
    }


class _NeutralProvider:
    def __init__(self) -> None:
        self.calls = 0

    def call(self, *, model, task, **kwargs) -> ProviderResult:
        self.calls += 1
        assert "deterministic_evidence" in task.user_payload
        assert task.user_payload["candidate"]["signal_id"] == "sig-preus-1"
        assert task.metadata["max_tokens"] == 400
        assert task.metadata["max_retries"] == 0
        assert task.metadata["json_schema"]["additionalProperties"] is False
        return ProviderResult(
            payload={
                "verdict": "NEUTRAL",
                "confidence": 0.78,
                "requested_adjustment": 0,
                "reason_codes": ["CONTEXT_BALANCED"],
                "short_rationale": "No additional promotion evidence beyond the baseline.",
            },
            text="{}",
            model=model.model_id,
            latency_ms=12.5,
        )


class _FailingProvider:
    def __init__(self) -> None:
        self.calls = 0

    def call(self, **kwargs) -> ProviderResult:
        self.calls += 1
        raise LLMProviderError("timeout")


class _InsufficientProvider:
    def call(self, *, model, task, **kwargs) -> ProviderResult:
        return ProviderResult(
            payload={
                "verdict": "INSUFFICIENT_DATA",
                "confidence": 0.35,
                "requested_adjustment": 0,
                "reason_codes": ["NO_INCREMENTAL_EVIDENCE"],
                "short_rationale": "The supplied evidence does not change the baseline.",
            },
            text="{}",
            model=model.model_id,
            latency_ms=10.0,
        )


@pytest.fixture
def db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "preus-openrouter.sqlite"
    _make_db(path)
    monkeypatch.setattr(preus, "select_candidates", lambda **_: _bundle())
    monkeypatch.setattr(preus, "_hard_gate_reason", lambda *args, **kwargs: None)
    return path


@pytest.fixture(autouse=True)
def enable_preus_llm_in_unit_tests(monkeypatch: pytest.MonkeyPatch) -> None:
    original = preus.load_cfg

    def load_enabled_cfg(*args, **kwargs):
        cfg = original(*args, **kwargs)
        cfg["llm_agent"]["enabled"] = True
        return cfg

    monkeypatch.setattr(preus, "load_cfg", load_enabled_cfg)


def test_openrouter_review_is_audited_but_cannot_overwrite_preus_gate(db: Path) -> None:
    router = _enabled_test_router(db_path=db, provider=_NeutralProvider())
    result = run_preus_openrouter_review(db=db, now=NOW, router=router)

    assert result["status"] == "OK"
    assert result["reviewed"] == 1
    assert result["ingested"] == 0
    assert result["advisory_only"] is True
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        review = conn.execute(
            "SELECT * FROM stocks_preus_review WHERE signal_id='sig-preus-1'"
        ).fetchone()
        assessment = conn.execute(
            "SELECT * FROM quality_agent_llm_assessments WHERE signal_id='sig-preus-1'"
        ).fetchone()
    assert review["review_verdict"] == "NEUTRAL"
    assert review["review_model"] == preus.BASELINE_REVIEW_MODEL
    assert review["review_cycle"] == "preus_baseline"
    assert assessment["scope"] == SCOPE
    assert assessment["prompt_version"] == PROMPT_VERSION
    assert assessment["status"] == "OK"


def test_disabled_preus_llm_keeps_baseline_without_calling_provider(
    db: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    disabled_cfg = preus.load_cfg()
    disabled_cfg["llm_agent"]["enabled"] = False
    monkeypatch.setattr(preus, "load_cfg", lambda: disabled_cfg)
    provider = _NeutralProvider()
    router = _enabled_test_router(db_path=db, provider=provider)

    result = run_preus_openrouter_review(db=db, now=NOW, router=router)

    assert result["status"] == "DISABLED"
    assert result["baseline_reviewed"] == 1
    assert provider.calls == 0


def test_successful_insufficient_treatment_is_complete_without_overwriting_baseline(
    db: Path,
) -> None:
    router = _enabled_test_router(db_path=db, provider=_InsufficientProvider())
    result = run_preus_openrouter_review(db=db, now=NOW, router=router)

    assert result["status"] == "OK"
    assert result["treatment"] == 1
    assert result["control"] == 0
    assert result["health"]["status"] == "READY_ADVISORY_OPTIONAL"
    with sqlite3.connect(db) as conn:
        model = conn.execute(
            "SELECT review_model FROM stocks_preus_review WHERE signal_id='sig-preus-1'"
        ).fetchone()[0]
    assert model == preus.BASELINE_REVIEW_MODEL


def test_openrouter_failure_keeps_deterministic_baseline_and_records_error(db: Path) -> None:
    router = _enabled_test_router(db_path=db, provider=_FailingProvider())
    result = run_preus_openrouter_review(db=db, now=NOW, router=router)

    assert result["status"] == "DEGRADED"
    assert result["reviewed"] == 0
    assert result["baseline_reviewed"] == 1
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        review = conn.execute(
            "SELECT * FROM stocks_preus_review WHERE signal_id='sig-preus-1'"
        ).fetchone()
        assessment = conn.execute(
            "SELECT * FROM quality_agent_llm_assessments WHERE signal_id='sig-preus-1'"
        ).fetchone()
    assert review["review_model"] == preus.BASELINE_REVIEW_MODEL
    assert review["review_verdict"] == "NEUTRAL"
    assert assessment["status"] == "ERROR"
    assert assessment["error_type"] == "timeout"


def test_openrouter_review_resumes_completed_same_session_candidates(db: Path) -> None:
    provider = _NeutralProvider()
    router = _enabled_test_router(db_path=db, provider=provider)

    first = run_preus_openrouter_review(db=db, now=NOW, router=router)
    second = run_preus_openrouter_review(
        db=db, now=NOW + timedelta(minutes=1), router=router,
    )

    assert first["submitted"] == 1
    assert second["status"] == "OK"
    assert second["submitted"] == 0
    assert second["reused"] == 1
    assert second["reviewed"] == 1
    assert provider.calls == 1


def test_openrouter_failure_stops_after_single_session_attempt(db: Path) -> None:
    provider = _FailingProvider()
    router = _enabled_test_router(db_path=db, provider=provider)

    first = run_preus_openrouter_review(db=db, now=NOW, router=router)
    second = run_preus_openrouter_review(
        db=db, now=NOW + timedelta(minutes=1), router=router,
    )
    third = run_preus_openrouter_review(
        db=db, now=NOW + timedelta(minutes=2), router=router,
    )

    assert first["submitted"] == 1
    assert second["submitted"] == 0
    assert second["retry_suppressed"] == 1
    assert third["submitted"] == 0
    assert third["retry_suppressed"] == 1
    assert provider.calls == 1
