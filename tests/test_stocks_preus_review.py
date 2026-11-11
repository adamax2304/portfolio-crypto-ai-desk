"""Pre-US-open stocks review overlay: candidate selection, verdict enforcement,
tier recompute, idempotency, and the narrow Paper pre-open promotion path.

Covers spec items #1-#10 (schedule test lives in test_scheduled_tasks_preus.py).
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from src.execution import stocks_preus_review as preus


def _make_db(path: Path) -> None:
    conn = sqlite3.connect(str(path))
    conn.execute("""CREATE TABLE proposed_signals (
        signal_id TEXT PRIMARY KEY, symbol TEXT, asset_class TEXT, mode TEXT, direction TEXT,
        tier TEXT, score REAL, status TEXT, created_at TEXT, entry_trigger REAL, suggested_entry REAL,
        entry_low REAL, entry_high REAL, stop_loss REAL, invalidation REAL, raw_idea_json TEXT
    )""")
    # Mirrors src/stocks/paper_funnel.py's snapshot table. Left empty in most
    # tests so select_candidates() falls back to its cap_reasons-based
    # PREOPEN_PLAN/RTH_ELIGIBLE detection (the same detection production uses
    # before a snapshot has been captured for a brand-new signal).
    conn.execute("""CREATE TABLE stocks_paper_decision_snapshots (
        signal_id TEXT PRIMARY KEY, funnel_state TEXT
    )""")
    conn.commit()
    conn.close()


def _insert_signal(path: Path, *, signal_id: str, symbol: str = "AAPL", tier: str = "C",
                   score: float = 62.0, status: str = "waiting_for_entry",
                   created_at: str | None = None, pre_gate_tier: str = "B",
                   cap_reasons: list[str] | None = None, mode: str = "intraday") -> None:
    now = created_at or datetime.now(timezone.utc).isoformat()
    if cap_reasons is None:
        cap_reasons = [f"{preus.PLAN_MARKER}: US cash session closed"]
    raw = json.dumps({"pre_gate_tier": pre_gate_tier, "cap_reasons": cap_reasons})
    conn = sqlite3.connect(str(path))
    conn.execute(
        "INSERT OR REPLACE INTO proposed_signals VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (signal_id, symbol, "stocks", mode, "long", tier, score, status, now,
         190.0, 190.0, None, None, 185.0, 185.0, raw),
    )
    conn.commit()
    conn.close()


@pytest.fixture
def db(tmp_path) -> Path:
    path = tmp_path / "preus.sqlite"
    _make_db(path)
    return path


def _clear_gate(monkeypatch):
    """Bypass the (separately-tested) hard-gate submodule calls so verdict-
    enforcement tests are deterministic and independent of news_items/legal/
    earnings fixtures."""
    monkeypatch.setattr(preus, "_hard_gate_reason", lambda conn, row, *, now, cfg, **kwargs: None)


# ---------------------------------------------------------------------------
# 4. SUPPORT +5 recomputes tier only via the shared threshold function
# ---------------------------------------------------------------------------

def test_support_adjustment_recomputes_tier_via_shared_function(db, monkeypatch):
    _clear_gate(monkeypatch)
    _insert_signal(db, signal_id="s1", score=62.0)  # 62 + 5 = 67 -> B (threshold 65)
    res = preus.record_verdict(
        signal_id="s1", verdict="SUPPORT", requested_adjustment=5,
        evidence={k: True for k in preus.load_cfg()["support_requires"]}, db=db,
    )
    assert res["status"] == "OK"
    assert res["adjustment"] == 5.0
    assert res["adjusted_score"] == 67.0
    from src.signals.tier_policy import tier_from_score
    assert res["tier"] == tier_from_score(67.0) == "B"


def test_support_request_within_range_is_not_forced_to_max(db, monkeypatch):
    _clear_gate(monkeypatch)
    _insert_signal(db, signal_id="s1", score=60.0)
    res = preus.record_verdict(
        signal_id="s1", verdict="SUPPORT", requested_adjustment=2,
        evidence={k: True for k in preus.load_cfg()["support_requires"]}, db=db,
    )
    assert res["adjustment"] == 2.0
    assert res["adjusted_score"] == 62.0


def test_support_request_clamped_to_configured_max(db, monkeypatch):
    _clear_gate(monkeypatch)
    _insert_signal(db, signal_id="s1", score=60.0)
    res = preus.record_verdict(
        signal_id="s1", verdict="SUPPORT", requested_adjustment=100,
        evidence={k: True for k in preus.load_cfg()["support_requires"]}, db=db,
    )
    assert res["adjustment"] == 5.0  # config max


def test_caution_clamped_into_configured_range(db, monkeypatch):
    _clear_gate(monkeypatch)
    _insert_signal(db, signal_id="s1", score=70.0)
    res = preus.record_verdict(signal_id="s1", verdict="CAUTION", requested_adjustment=-1, db=db)
    assert res["adjustment"] == -3.0  # clamped to range max (least negative)
    res2 = preus.record_verdict(signal_id="s1", verdict="CAUTION", requested_adjustment=-50, db=db)
    assert res2["adjustment"] == -7.0  # clamped to range min


def test_neutral_forces_zero_adjustment(db, monkeypatch):
    _clear_gate(monkeypatch)
    _insert_signal(db, signal_id="s1", score=70.0)
    res = preus.record_verdict(signal_id="s1", verdict="NEUTRAL", requested_adjustment=5, db=db)
    assert res["adjustment"] == 0.0
    assert res["adjusted_score"] == 70.0


def test_insufficient_data_forces_zero_and_is_not_treated_as_positive(db, monkeypatch):
    _clear_gate(monkeypatch)
    _insert_signal(db, signal_id="s1", score=70.0)
    res = preus.record_verdict(signal_id="s1", verdict="INSUFFICIENT_DATA", requested_adjustment=5, db=db)
    assert res["adjustment"] == 0.0


# ---------------------------------------------------------------------------
# 3. Hard-block present forbids ANY positive adjustment, regardless of verdict
# ---------------------------------------------------------------------------

def test_hard_block_forces_support_adjustment_to_zero(db, monkeypatch):
    monkeypatch.setattr(preus, "_hard_gate_reason",
                        lambda conn, row, *, now, cfg, **kwargs: preus.EXCLUDE_LEGAL_RISK)
    _insert_signal(db, signal_id="s1", score=60.0, tier="C")
    res = preus.record_verdict(
        signal_id="s1", verdict="SUPPORT", requested_adjustment=5,
        evidence={k: True for k in preus.load_cfg()["support_requires"]}, db=db,
    )
    assert res["adjustment"] == 0.0
    assert res["clamped_by_gate"] is True
    review = preus.active_review(db, "s1")
    assert "server_clamped_hard_block" in json.loads(review["review_reason_codes_json"])
    assert preus.EXCLUDE_LEGAL_RISK in json.loads(review["review_reason_codes_json"])


def test_support_missing_precondition_clamped_to_zero(db, monkeypatch):
    _clear_gate(monkeypatch)
    _insert_signal(db, signal_id="s1", score=60.0)
    res = preus.record_verdict(
        signal_id="s1", verdict="SUPPORT", requested_adjustment=5,
        evidence={"catalyst_entity_resolved": True},  # missing the rest
        db=db,
    )
    assert res["adjustment"] == 0.0
    review = preus.active_review(db, "s1")
    codes = json.loads(review["review_reason_codes_json"])
    assert "server_clamped_missing_precondition" in codes


# ---------------------------------------------------------------------------
# 5. BLOCK never touches the base proposed_signals row; writes a separate table
# ---------------------------------------------------------------------------

def test_block_does_not_modify_original_signal_row(db, monkeypatch):
    _clear_gate(monkeypatch)
    _insert_signal(db, signal_id="s1", score=60.0, tier="C")
    conn = sqlite3.connect(str(db))
    before = dict(zip((c[1] for c in conn.execute("PRAGMA table_info(proposed_signals)")),
                       conn.execute("SELECT * FROM proposed_signals WHERE signal_id='s1'").fetchone()))
    conn.close()

    res = preus.record_verdict(signal_id="s1", verdict="BLOCK",
                               reason_codes=["legal_risk_flagged"], db=db)
    assert res["status"] == "OK"

    conn = sqlite3.connect(str(db))
    after = dict(zip((c[1] for c in conn.execute("PRAGMA table_info(proposed_signals)")),
                      conn.execute("SELECT * FROM proposed_signals WHERE signal_id='s1'").fetchone()))
    conn.close()
    assert before == after  # base record byte-identical

    block = preus.active_block(db, "s1")
    assert block is not None
    assert block["signal_id"] == "s1"


# ---------------------------------------------------------------------------
# 2/3/6/7. is_review_supported_for_preopen narrow-promotion path
# ---------------------------------------------------------------------------

def test_session_cap_only_c_becomes_promotable_with_supportive_review(db, monkeypatch):
    _clear_gate(monkeypatch)
    review_at = datetime(2026, 8, 20, 12, 55, tzinfo=timezone.utc)  # 08:55 ET
    _insert_signal(
        db, signal_id="s1", score=62.0, tier="C", pre_gate_tier="B",
        created_at=(review_at - timedelta(minutes=15)).isoformat(),
    )
    preus.record_verdict(
        signal_id="s1", verdict="SUPPORT", requested_adjustment=5,
        evidence={k: True for k in preus.load_cfg()["support_requires"]}, db=db, now=review_at,
    )
    conn = sqlite3.connect(str(db))
    row = dict(zip((c[1] for c in conn.execute("PRAGMA table_info(proposed_signals)")),
                    conn.execute("SELECT * FROM proposed_signals WHERE signal_id='s1'").fetchone()))
    conn.close()
    supported, reason = preus.is_review_supported_for_preopen(db, row, now=review_at)
    assert supported is True, reason


def test_substantive_c_tier_never_promotable_even_with_review_row(db, monkeypatch):
    _clear_gate(monkeypatch)
    # C-tier for a DIFFERENT (substantive) reason — no market_closed marker.
    _insert_signal(db, signal_id="s1", score=62.0, tier="C", pre_gate_tier="C",
                   cap_reasons=["legal_headline_risk: SEC investigation"])
    preus.record_verdict(
        signal_id="s1", verdict="SUPPORT", requested_adjustment=5,
        evidence={k: True for k in preus.load_cfg()["support_requires"]}, db=db,
    )
    conn = sqlite3.connect(str(db))
    row = dict(zip((c[1] for c in conn.execute("PRAGMA table_info(proposed_signals)")),
                    conn.execute("SELECT * FROM proposed_signals WHERE signal_id='s1'").fetchone()))
    conn.close()
    supported, reason = preus.is_review_supported_for_preopen(db, row)
    assert supported is False
    assert reason == "not_market_closed_session_cap"


def test_fresh_block_vetoes_even_a_would_be_supportive_review(db, monkeypatch):
    _clear_gate(monkeypatch)
    _insert_signal(db, signal_id="s1", score=62.0, tier="C", pre_gate_tier="B")
    preus.record_verdict(
        signal_id="s1", verdict="SUPPORT", requested_adjustment=5,
        evidence={k: True for k in preus.load_cfg()["support_requires"]}, db=db,
    )
    preus.record_verdict(signal_id="s1", verdict="BLOCK", reason_codes=["late_breaking_risk"], db=db)
    conn = sqlite3.connect(str(db))
    row = dict(zip((c[1] for c in conn.execute("PRAGMA table_info(proposed_signals)")),
                    conn.execute("SELECT * FROM proposed_signals WHERE signal_id='s1'").fetchone()))
    conn.close()
    supported, reason = preus.is_review_supported_for_preopen(db, row)
    assert supported is False
    assert reason == "fresh_block_active"


def test_expired_review_is_not_used(db, monkeypatch):
    _clear_gate(monkeypatch)
    _insert_signal(db, signal_id="s1", score=62.0, tier="C", pre_gate_tier="B")
    past = datetime.now(timezone.utc) - timedelta(hours=5)
    preus.record_verdict(
        signal_id="s1", verdict="SUPPORT", requested_adjustment=5,
        evidence={k: True for k in preus.load_cfg()["support_requires"]}, db=db, now=past,
    )
    conn = sqlite3.connect(str(db))
    row = dict(zip((c[1] for c in conn.execute("PRAGMA table_info(proposed_signals)")),
                    conn.execute("SELECT * FROM proposed_signals WHERE signal_id='s1'").fetchone()))
    conn.close()
    supported, reason = preus.is_review_supported_for_preopen(db, row)  # "now" defaults to real now
    assert supported is False
    assert reason == "no_fresh_review"


# ---------------------------------------------------------------------------
# 9. Idempotency: re-running review ingestion overwrites, never duplicates
# ---------------------------------------------------------------------------

def test_reingest_same_signal_does_not_duplicate(db, monkeypatch):
    _clear_gate(monkeypatch)
    _insert_signal(db, signal_id="s1", score=60.0)
    preus.record_verdict(signal_id="s1", verdict="NEUTRAL", db=db)
    preus.record_verdict(signal_id="s1", verdict="SUPPORT", requested_adjustment=5,
                         evidence={k: True for k in preus.load_cfg()["support_requires"]}, db=db)
    conn = sqlite3.connect(str(db))
    count = conn.execute("SELECT COUNT(*) FROM stocks_preus_review WHERE signal_id='s1'").fetchone()[0]
    conn.close()
    assert count == 1
    review = preus.active_review(db, "s1")
    assert review["review_verdict"] == "SUPPORT"  # last write wins


def test_batch_ingest_materializes_once_after_all_verdicts(db, monkeypatch):
    _clear_gate(monkeypatch)
    _insert_signal(db, signal_id="batch-1", score=70.0)
    _insert_signal(db, signal_id="batch-2", score=72.0)
    calls = []
    monkeypatch.setattr(
        preus,
        "_refresh_actionability_best_effort",
        lambda *args, **kwargs: calls.append((args, kwargs)),
    )

    results = preus.record_verdicts([
        {"signal_id": "batch-1", "verdict": "NEUTRAL"},
        {"signal_id": "batch-2", "verdict": "CAUTION", "requested_adjustment": -3},
    ], db=db)

    assert [row["status"] for row in results] == ["OK", "OK"]
    assert len(calls) == 1
    conn = sqlite3.connect(str(db))
    assert conn.execute("SELECT COUNT(*) FROM stocks_preus_review").fetchone()[0] == 2
    conn.close()


def test_unknown_signal_id_rejected(db, monkeypatch):
    _clear_gate(monkeypatch)
    res = preus.record_verdict(signal_id="does-not-exist", verdict="SUPPORT", db=db)
    assert res["status"] == "REJECTED"


def test_invalid_verdict_rejected(db, monkeypatch):
    _clear_gate(monkeypatch)
    _insert_signal(db, signal_id="s1")
    res = preus.record_verdict(signal_id="s1", verdict="MAYBE", db=db)
    assert res["status"] == "REJECTED"


# ---------------------------------------------------------------------------
# 8. Never writes to signal_outcomes / final_r / any live module
# ---------------------------------------------------------------------------

def test_module_never_touches_live_or_final_r_or_signal_outcomes():
    src = Path(preus.__file__).read_text(encoding="utf-8").lower()
    for forbidden in ("update proposed_signals", "update signal_outcomes", "final_r =",
                      "src.live_execution", "create_order", "auto_live", "manual_live"):
        assert forbidden not in src, f"forbidden pattern found: {forbidden}"


# ---------------------------------------------------------------------------
# Candidate selection: eligible/excluded split, terminal filtering
# ---------------------------------------------------------------------------

def test_select_candidates_includes_session_cap_c_and_current_ab(db, monkeypatch):
    monkeypatch.setattr(preus, "_hard_gate_reason", lambda conn, row, *, now, cfg, **kwargs: None)
    _insert_signal(db, signal_id="c1", symbol="AAPL", tier="C", pre_gate_tier="B",
                   status="waiting_for_entry")
    _insert_signal(db, signal_id="ab1", symbol="MSFT", tier="B", pre_gate_tier="B",
                   status="waiting_for_entry", cap_reasons=[])
    bundle = preus.select_candidates(db=db)
    ids = {c["signal_id"] for c in bundle["eligible"]}
    assert {"c1", "ab1"} <= ids


def test_session_cap_c_requires_original_pre_gate_ab(db, monkeypatch):
    monkeypatch.setattr(preus, "_hard_gate_reason", lambda conn, row, *, now, cfg, **kwargs: None)
    _insert_signal(
        db,
        signal_id="weak-c",
        tier="C",
        pre_gate_tier="C",
        status="waiting_for_entry",
    )
    bundle = preus.select_candidates(db=db)
    promotable = {
        row["signal_id"] for row in bundle["eligible"] if row.get("promotable")
    }
    assert "weak-c" not in promotable


def test_supported_plan_materializes_for_pending_tracker(db, monkeypatch):
    _clear_gate(monkeypatch)
    review_at = datetime(2026, 8, 20, 12, 55, tzinfo=timezone.utc)  # 08:55 ET
    _insert_signal(
        db,
        signal_id="reviewed-c",
        score=62.0,
        tier="C",
        pre_gate_tier="B",
        status="waiting_for_entry",
        created_at=(review_at - timedelta(minutes=15)).isoformat(),
    )
    result = preus.record_verdict(
        signal_id="reviewed-c",
        verdict="SUPPORT",
        requested_adjustment=5,
        evidence={key: True for key in preus.load_cfg()["support_requires"]},
        db=db,
        now=review_at,
    )
    assert result["tier"] == "B"
    active = preus.active_actionability(db, "reviewed-c", now=review_at)
    assert active is not None
    assert active["decision"] == "ACTIONABLE"
    assert active["effective_tier"] == "B"
    assert "reviewed-c" in preus.active_actionable_signal_ids(db, now=review_at)


def test_insufficient_data_cannot_materialize_session_capped_plan(db, monkeypatch):
    _clear_gate(monkeypatch)
    _insert_signal(
        db,
        signal_id="unknown-evidence",
        score=72.0,
        tier="C",
        pre_gate_tier="B",
        status="waiting_for_entry",
    )

    preus.record_verdict(
        signal_id="unknown-evidence",
        verdict="INSUFFICIENT_DATA",
        db=db,
    )

    conn = sqlite3.connect(str(db))
    row = conn.execute(
        "SELECT decision,reason_codes_json FROM stocks_preus_actionability "
        "WHERE signal_id='unknown-evidence'"
    ).fetchone()
    conn.close()
    assert row is not None
    assert row[0] == "BLOCKED"
    assert "REVIEW_INSUFFICIENT_DATA" in json.loads(row[1])


def test_late_review_is_audit_only_and_cannot_materialize_a_plan(db, monkeypatch):
    _clear_gate(monkeypatch)
    deadline = datetime(2026, 8, 20, 13, 12, tzinfo=timezone.utc)  # 09:12 ET
    _insert_signal(
        db,
        signal_id="late-review",
        score=72.0,
        tier="C",
        pre_gate_tier="B",
        created_at=(deadline - timedelta(minutes=15)).isoformat(),
    )

    result = preus.record_verdict(
        signal_id="late-review",
        verdict="SUPPORT",
        requested_adjustment=5,
        evidence={key: True for key in preus.load_cfg()["support_requires"]},
        db=db,
        now=deadline + timedelta(seconds=1),
    )

    assert result["tier"] == "B"
    conn = sqlite3.connect(str(db))
    decision, reasons_json = conn.execute(
        "SELECT decision,reason_codes_json FROM stocks_preus_actionability "
        "WHERE signal_id='late-review'"
    ).fetchone()
    conn.close()
    assert decision == "BLOCKED"
    assert "REVIEW_INGEST_AFTER_DEADLINE" in json.loads(reasons_json)


def test_baseline_revalidation_remains_actionable_while_llm_is_still_within_deadline(db, monkeypatch):
    _clear_gate(monkeypatch)
    review_at = datetime(2026, 8, 20, 12, 55, tzinfo=timezone.utc)  # 08:55 ET
    _insert_signal(
        db,
        signal_id="baseline-candidate",
        score=72.0,
        tier="C",
        pre_gate_tier="B",
        created_at=(review_at - timedelta(minutes=15)).isoformat(),
    )
    bundle = preus.select_candidates(db=db, now=review_at)
    preus.record_candidate_bundle(bundle, db=db, now=review_at)

    results = preus.record_baseline_revalidations(
        bundle["eligible"], db=db, now=review_at
    )
    health = preus.review_health(db=db, now=review_at + timedelta(minutes=5))

    assert len(results) == 1
    assert results[0]["verdict"] == "NEUTRAL"
    assert results[0]["tier"] == "B"
    assert health["status"] == "READY_ADVISORY_OPTIONAL"
    assert health["baseline_signal_ids"] == ["baseline-candidate"]
    active = preus.active_actionability(db, "baseline-candidate", now=review_at + timedelta(minutes=5))
    assert active is not None
    assert active["decision"] == "ACTIONABLE"


def test_baseline_only_review_alerts_only_after_the_configured_deadline(db, monkeypatch):
    _clear_gate(monkeypatch)
    review_at = datetime(2026, 8, 20, 12, 50, tzinfo=timezone.utc)  # 08:50 ET
    _insert_signal(
        db,
        signal_id="baseline-deadline",
        score=72.0,
        tier="C",
        pre_gate_tier="B",
        created_at=(review_at - timedelta(minutes=15)).isoformat(),
    )
    bundle = preus.select_candidates(db=db, now=review_at)
    preus.record_candidate_bundle(bundle, db=db, now=review_at)
    preus.record_baseline_revalidations(bundle["eligible"], db=db, now=review_at)

    before_deadline = preus.review_health(db=db, now=review_at + timedelta(minutes=20))
    at_deadline = preus.review_health(db=db, now=review_at + timedelta(minutes=22))

    assert before_deadline["status"] == "READY_ADVISORY_OPTIONAL"
    assert preus.consume_new_review_health_alert(
        db=db, health=before_deadline, now=review_at + timedelta(minutes=20)
    ) == []
    assert at_deadline["status"] == "READY_ADVISORY_OPTIONAL"
    assert preus.consume_new_review_health_alert(
        db=db, health=at_deadline, now=review_at + timedelta(minutes=22)
    ) == []


def test_candidate_bundle_is_immutable_within_a_preus_session(db, monkeypatch):
    _clear_gate(monkeypatch)
    first_at = datetime(2026, 8, 20, 12, 50, tzinfo=timezone.utc)  # 08:50 ET
    _insert_signal(
        db,
        signal_id="first-candidate",
        score=72.0,
        tier="C",
        pre_gate_tier="B",
        created_at=(first_at - timedelta(minutes=15)).isoformat(),
    )
    first = preus.record_candidate_bundle(preus.select_candidates(db=db, now=first_at), db=db, now=first_at)

    _insert_signal(
        db,
        signal_id="late-candidate",
        score=72.0,
        tier="C",
        pre_gate_tier="B",
        created_at=(first_at + timedelta(minutes=5)).isoformat(),
    )
    later = preus.record_candidate_bundle(
        preus.select_candidates(db=db, now=first_at + timedelta(minutes=8)),
        db=db,
        now=first_at + timedelta(minutes=8),
    )

    assert json.loads(first["eligible_signal_ids_json"]) == ["first-candidate"]
    assert json.loads(later["eligible_signal_ids_json"]) == ["first-candidate"]
    assert later["preserved_existing_snapshot"] is True


def test_insufficient_llm_review_preserves_timely_baseline_actionability(db, monkeypatch):
    """A non-decision from the external reviewer must not erase the hard-gated fallback."""
    _clear_gate(monkeypatch)
    review_at = datetime(2026, 8, 20, 12, 55, tzinfo=timezone.utc)  # 08:55 ET
    _insert_signal(
        db,
        signal_id="baseline-insufficient",
        score=72.0,
        tier="C",
        pre_gate_tier="B",
        status="waiting_for_entry",
        created_at=(review_at - timedelta(minutes=15)).isoformat(),
    )
    bundle = preus.select_candidates(db=db, now=review_at)
    preus.record_candidate_bundle(bundle, db=db, now=review_at)
    preus.record_baseline_revalidations(bundle["eligible"], db=db, now=review_at)

    result = preus.record_verdict(
        signal_id="baseline-insufficient",
        verdict="INSUFFICIENT_DATA",
        reason_codes=["time_constrained_no_verification"],
        model="external-reviewer",
        db=db,
        now=review_at + timedelta(minutes=5),
    )

    assert result["status"] == "ADVISORY_ONLY_NOT_APPLIED"
    review = preus.active_review(db, "baseline-insufficient", now=review_at + timedelta(minutes=5))
    assert review is not None
    assert review["review_model"] == preus.BASELINE_REVIEW_MODEL
    active = preus.active_actionability(db, "baseline-insufficient", now=review_at + timedelta(minutes=5))
    assert active is not None
    assert active["decision"] == "ACTIONABLE"


def test_late_non_veto_review_preserves_the_timely_baseline(db, monkeypatch):
    _clear_gate(monkeypatch)
    review_at = datetime(2026, 8, 20, 12, 55, tzinfo=timezone.utc)  # 08:55 ET
    _insert_signal(
        db,
        signal_id="baseline-preserved",
        score=72.0,
        tier="C",
        pre_gate_tier="B",
        created_at=(review_at - timedelta(minutes=15)).isoformat(),
    )
    bundle = preus.select_candidates(db=db, now=review_at)
    preus.record_candidate_bundle(bundle, db=db, now=review_at)
    preus.record_baseline_revalidations(bundle["eligible"], db=db, now=review_at)

    late = preus.record_verdict(
        signal_id="baseline-preserved",
        verdict="CAUTION",
        requested_adjustment=-7,
        db=db,
        now=review_at + timedelta(minutes=18),
    )

    assert late["status"] == "IGNORED_LATE_PRESERVED_TIMELY_REVIEW"
    review = preus.active_review(db, "baseline-preserved", now=review_at + timedelta(minutes=18))
    assert review is not None
    assert review["review_model"] == preus.BASELINE_REVIEW_MODEL
    active = preus.active_actionability(db, "baseline-preserved", now=review_at + timedelta(minutes=18))
    assert active is not None
    assert active["decision"] == "ACTIONABLE"


def test_review_health_marks_late_bundle_as_operational_failure(db, monkeypatch):
    _clear_gate(monkeypatch)
    deadline = datetime(2026, 8, 20, 13, 12, tzinfo=timezone.utc)
    _insert_signal(
        db,
        signal_id="late-bundle",
        tier="C",
        score=72.0,
        pre_gate_tier="B",
        created_at=(deadline - timedelta(minutes=15)).isoformat(),
    )

    preus.record_candidate_bundle(
        preus.select_candidates(db=db, now=deadline + timedelta(minutes=1)),
        db=db,
        now=deadline + timedelta(minutes=1),
    )
    health = preus.review_health(db=db, now=deadline + timedelta(minutes=1))

    assert health["status"] == "BUNDLE_LATE"
    assert health["reason"] == "structured_preus_candidate_bundle_recorded_after_deadline"


def test_actionability_history_preserves_expired_actionable_decision(db, monkeypatch):
    _clear_gate(monkeypatch)
    review_at = datetime(2026, 8, 12, 12, 55, tzinfo=timezone.utc)  # 08:55 NY
    _insert_signal(
        db,
        signal_id="reviewed-history",
        score=62.0,
        tier="C",
        pre_gate_tier="B",
        status="waiting_for_entry",
        created_at=(review_at - timedelta(hours=1)).isoformat(),
    )
    result = preus.record_verdict(
        signal_id="reviewed-history",
        verdict="SUPPORT",
        requested_adjustment=5,
        evidence={key: True for key in preus.load_cfg()["support_requires"]},
        db=db,
        now=review_at,
    )
    assert result["tier"] == "B"

    expired_at = review_at + timedelta(minutes=95)
    refresh = preus.refresh_actionability(db, now=expired_at)
    assert refresh["blocked"] == 1

    conn = sqlite3.connect(str(db))
    history = conn.execute(
        "SELECT decision,snapshot_json FROM stocks_preus_actionability_history "
        "WHERE signal_id='reviewed-history' ORDER BY id"
    ).fetchall()
    current = conn.execute(
        "SELECT decision FROM stocks_preus_actionability WHERE signal_id='reviewed-history'"
    ).fetchone()[0]
    conn.close()

    assert [row[0] for row in history] == ["ACTIONABLE", "BLOCKED"]
    assert current == "BLOCKED"
    first_snapshot = json.loads(history[0][1])
    assert first_snapshot["source_signal"]["signal_id"] == "reviewed-history"
    assert first_snapshot["session_cap_only"] is True


def test_select_candidates_excludes_terminal_status(db, monkeypatch):
    monkeypatch.setattr(preus, "_hard_gate_reason", lambda conn, row, *, now, cfg, **kwargs: None)
    _insert_signal(db, signal_id="done1", tier="A", status="tp1_hit")
    bundle = preus.select_candidates(db=db)
    all_ids = {c["signal_id"] for c in bundle["eligible"]} | {c["signal_id"] for c in bundle["excluded"]}
    assert "done1" not in all_ids


def test_select_candidates_keeps_fresh_preopen_snapshot_after_tracker_terminal_label(db, monkeypatch):
    """The historical tracker may finish its simulated path before the real
    pre-US review runs.  A fresh PREOPEN_PLAN remains reviewable; ordinary
    terminal rows still stay excluded by the preceding test."""
    monkeypatch.setattr(preus, "_hard_gate_reason", lambda conn, row, *, now, cfg, **kwargs: None)
    _insert_signal(db, signal_id="plan1", tier="C", pre_gate_tier="B", status="missed_no_entry")
    conn = sqlite3.connect(str(db))
    conn.execute("INSERT INTO stocks_paper_decision_snapshots VALUES (?,?)",
                 ("plan1", "PREOPEN_PLAN"))
    conn.commit()
    conn.close()

    bundle = preus.select_candidates(db=db)
    eligible = {row["signal_id"] for row in bundle["eligible"]}
    assert "plan1" in eligible


def test_select_candidates_keeps_weekend_preopen_snapshot_for_target_session(db, monkeypatch):
    """Friday after-close plans remain reviewable for Monday pre-US handoff."""
    monkeypatch.setattr(preus, "_hard_gate_reason", lambda conn, row, *, now, cfg, **kwargs: None)
    created = datetime(2026, 9, 18, 20, 59, tzinfo=timezone.utc).isoformat()
    monday_preus = datetime(2026, 9, 21, 12, 50, tzinfo=timezone.utc)
    _insert_signal(
        db,
        signal_id="weekend-plan",
        tier="C",
        pre_gate_tier="B",
        status="stale_before_entry",
        created_at=created,
    )
    conn = sqlite3.connect(str(db))
    conn.execute("ALTER TABLE stocks_paper_decision_snapshots ADD COLUMN target_session_open_at TEXT")
    conn.execute("ALTER TABLE stocks_paper_decision_snapshots ADD COLUMN target_session_close_at TEXT")
    conn.execute(
        "INSERT INTO stocks_paper_decision_snapshots VALUES (?,?,?,?)",
        (
            "weekend-plan", "PREOPEN_PLAN",
            "2026-09-21T13:30:00+00:00", "2026-09-21T20:00:00+00:00",
        ),
    )
    conn.commit()
    conn.close()

    bundle = preus.select_candidates(db=db, now=monday_preus)
    eligible = {row["signal_id"] for row in bundle["eligible"]}
    assert "weekend-plan" in eligible


def test_select_candidates_excludes_stale_plan_beyond_max_age(db, monkeypatch):
    monkeypatch.setattr(preus, "_hard_gate_reason", lambda conn, row, *, now, cfg, **kwargs: None)
    old = (datetime.now(timezone.utc) - timedelta(hours=30)).isoformat()
    _insert_signal(db, signal_id="old1", tier="C", pre_gate_tier="B", created_at=old)
    bundle = preus.select_candidates(db=db)
    all_ids = {c["signal_id"] for c in bundle["eligible"]} | {c["signal_id"] for c in bundle["excluded"]}
    assert "old1" not in all_ids  # older than max_candidate_age_hours -> filtered by the SQL window itself


# ---------------------------------------------------------------------------
# 10. Configured pre-US structured-review hand-off health
# ---------------------------------------------------------------------------

def test_review_health_alerts_when_routine_never_records_candidate_bundle(db):
    deadline = datetime(2026, 8, 20, 13, 12, tzinfo=timezone.utc)  # 09:12 ET
    health = preus.review_health(db=db, now=deadline)
    alert = preus.consume_new_review_health_alert(db=db, health=health, now=deadline)

    assert health["status"] == "BUNDLE_MISSING"
    assert health["reason"] == "structured_preus_candidate_bundle_not_recorded"
    assert len(alert) == 1


def test_review_health_alerts_once_when_due_candidate_has_no_verdict(db, monkeypatch):
    _clear_gate(monkeypatch)
    deadline = datetime(2026, 8, 20, 13, 12, tzinfo=timezone.utc)  # 09:12 ET
    _insert_signal(
        db,
        signal_id="handoff-missing",
        tier="C",
        pre_gate_tier="B",
        created_at=(deadline - timedelta(minutes=15)).isoformat(),
    )
    preus.record_candidate_bundle(
        preus.select_candidates(db=db, now=deadline), db=db, now=deadline
    )

    health = preus.review_health(db=db, now=deadline)
    first = preus.consume_new_review_health_alert(db=db, health=health, now=deadline)
    repeated = preus.consume_new_review_health_alert(
        db=db,
        health=preus.review_health(db=db, now=deadline + timedelta(minutes=1)),
        now=deadline + timedelta(minutes=1),
    )

    assert health["status"] == "REVIEW_MISSING"
    assert (health["eligible_count"], health["reviewed_count"], health["missing_count"]) == (1, 0, 1)
    assert len(first) == 1
    assert repeated == []


def test_review_health_is_ready_after_fresh_structured_ingest(db, monkeypatch):
    _clear_gate(monkeypatch)
    reviewed_at = datetime(2026, 8, 20, 13, 0, tzinfo=timezone.utc)  # 09:00 ET
    _insert_signal(
        db,
        signal_id="handoff-ready",
        tier="C",
        score=62.0,
        pre_gate_tier="B",
        created_at=(reviewed_at - timedelta(minutes=15)).isoformat(),
    )
    preus.record_candidate_bundle(
        preus.select_candidates(db=db, now=reviewed_at), db=db, now=reviewed_at
    )
    result = preus.record_verdict(
        signal_id="handoff-ready",
        verdict="SUPPORT",
        requested_adjustment=5,
        evidence={key: True for key in preus.load_cfg()["support_requires"]},
        review_cycle="preus_0900",
        db=db,
        now=reviewed_at,
    )
    health = preus.review_health(db=db, now=reviewed_at + timedelta(minutes=5))

    assert result["tier"] == "B"
    assert health["status"] == "READY_ADVISORY_OPTIONAL"
    assert (health["eligible_count"], health["reviewed_count"], health["missing_count"]) == (1, 1, 0)
    assert preus.consume_new_review_health_alert(db=db, health=health, now=reviewed_at) == []
