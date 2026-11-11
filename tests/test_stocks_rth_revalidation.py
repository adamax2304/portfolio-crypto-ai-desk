"""Stocks next-RTH revalidation is audit-only and never promotes an old plan."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

from src.stocks import paper_funnel, rth_revalidation as rr

UTC = timezone.utc
RTH_CONFIRMED = datetime(2026, 7, 8, 13, 45, tzinfo=UTC)  # 09:45 ET, first 15m is closed
PREMARKET = "2026-07-08T12:00:00+00:00"


def _db(tmp_path):
    path = tmp_path / "stocks.sqlite"
    with sqlite3.connect(path) as conn:
        conn.execute("""
            CREATE TABLE proposed_signals (
                signal_id TEXT, created_at TEXT, symbol TEXT, direction TEXT,
                tier TEXT, score REAL, status TEXT, raw_idea_json TEXT,
                asset_class TEXT, mode TEXT
            )
        """)
    return path


def _insert(conn, signal_id, created_at, symbol, direction, tier, *, planning=False, reasons=None):
    raw = {
        "pre_gate_tier": "A" if planning else tier,
        "cap_reasons": (["market_closed_intraday_planning_only"] if planning else list(reasons or [])),
    }
    conn.execute(
        "INSERT INTO proposed_signals VALUES (?,?,?,?,?,?,?,?,?,?)",
        (signal_id, created_at, symbol, direction, tier, 80.0, "open", json.dumps(raw), "stocks", "intraday"),
    )


def _cfg(**extra):
    base = {
        "enabled": True, "version": "test", "min_minutes_after_open": 15,
        "max_minutes_after_open": 90, "max_plan_age_hours": 20, "require_pre_gate_ab": True,
    }
    base.update(extra)
    return base


def test_fresh_rth_ab_is_linked_but_plan_is_never_promoted(tmp_path):
    path = _db(tmp_path)
    with sqlite3.connect(path) as conn:
        _insert(conn, "plan-1", PREMARKET, "AMD", "long", "C", planning=True)
        _insert(conn, "fresh-1", "2026-07-08T13:44:00+00:00", "AMD", "long", "A")
        conn.commit()

    result = rr.refresh(db=path, now=RTH_CONFIRMED, cfg=_cfg())
    assert result["status"] == "ok"
    assert result["plans"] == result["ready"] == 1
    assert result["rows"][0]["decision"] == "READY_FOR_EXISTING_PAPER_TRACKER"
    assert result["rows"][0]["rth_signal_id"] == "fresh-1"

    with sqlite3.connect(path) as conn:
        # The original plan remains a C plan. The bridge writes only its own table.
        assert conn.execute("SELECT tier FROM proposed_signals WHERE signal_id='plan-1'").fetchone()[0] == "C"
        row = conn.execute(
            "SELECT decision, rth_signal_id FROM stocks_intraday_rth_revalidations"
        ).fetchone()
    assert row == ("READY_FOR_EXISTING_PAPER_TRACKER", "fresh-1")


def test_preus_mexc_filled_route_is_not_reported_as_generic_rth_rejection(tmp_path):
    path = _db(tmp_path)
    with sqlite3.connect(path) as conn:
        _insert(conn, "plan-1", PREMARKET, "AMD", "long", "C", planning=True)
        conn.execute("""
            CREATE TABLE mexc_stock_futures_paper_orders (
                source_signal_id TEXT, session_date TEXT, status TEXT
            )
        """)
        conn.execute(
            "INSERT INTO mexc_stock_futures_paper_orders VALUES (?,?,?)",
            ("plan-1", "2026-07-08", "FILLED"),
        )
        conn.commit()

    result = rr.refresh(db=path, now=RTH_CONFIRMED, cfg=_cfg())

    assert result["ready"] == 0
    assert result["rejected"] == 0
    assert result["mexc_handled"] == 1
    assert result["rows"][0]["decision"] == "PREUS_MEXC_PAPER_FILLED"


def test_same_plan_actionable_preus_review_needs_no_duplicate_rth_candidate(tmp_path):
    path = _db(tmp_path)
    with sqlite3.connect(path) as conn:
        _insert(conn, "plan-1", PREMARKET, "AMD", "long", "C", planning=True)
        conn.execute("""
            CREATE TABLE stocks_preus_actionability (
                signal_id TEXT PRIMARY KEY, target_session_open_at TEXT,
                decision TEXT, effective_tier TEXT, effective_score REAL,
                reason_codes_json TEXT, evaluated_at TEXT, valid_until TEXT
            )
        """)
        conn.execute(
            "INSERT INTO stocks_preus_actionability VALUES (?,?,?,?,?,?,?,?)",
            (
                "plan-1", "2026-07-08T13:30:00+00:00", "ACTIONABLE", "B", 79.0,
                "[]", "2026-07-08T13:00:00+00:00", "2026-07-08T20:00:00+00:00",
            ),
        )
        conn.commit()

    result = rr.refresh(db=path, now=RTH_CONFIRMED, cfg=_cfg())

    assert result["ready"] == result["preus_actionable"] == 1
    row = result["rows"][0]
    assert row["decision"] == "READY_FOR_PREUS_ACTIONABILITY_TRACKER"
    assert row["rth_signal_id"] == "plan-1"
    assert row["rth_tier"] == "B"


def test_historical_generic_rejection_is_reconciled_when_mexc_route_filled(tmp_path):
    path = _db(tmp_path)
    with sqlite3.connect(path) as conn:
        rr.ensure_tables(conn)
        conn.execute("""
            INSERT INTO stocks_intraday_rth_revalidations(
                plan_signal_id,session_open_at,plan_created_at,symbol,direction,
                decision,reasons_json,evaluated_at,version
            ) VALUES(?,?,?,?,?,?,?,?,?)
        """, (
            "plan-1", "2026-07-08T13:30:00+00:00", PREMARKET, "AMD", "long",
            "REJECTED_NO_FRESH_RTH_CANDIDATE", "[]", "2026-07-08T15:15:00+00:00", "old",
        ))
        conn.execute("""
            CREATE TABLE mexc_stock_futures_paper_orders (
                source_signal_id TEXT, session_date TEXT, status TEXT
            )
        """)
        conn.execute(
            "INSERT INTO mexc_stock_futures_paper_orders VALUES (?,?,?)",
            ("plan-1", "2026-07-08", "FILLED"),
        )
        conn.commit()

    result = rr.refresh(
        db=path, now=datetime(2026, 7, 9, 12, 0, tzinfo=UTC), cfg=_cfg()
    )

    assert result["status"] == "outside_revalidation_window"
    assert result["mexc_reconciled"] == 1
    with sqlite3.connect(path) as conn:
        decision = conn.execute(
            "SELECT decision FROM stocks_intraday_rth_revalidations"
        ).fetchone()[0]
    assert decision == "PREUS_MEXC_PAPER_FILLED"


def test_snapshot_c_pre_gate_plan_is_not_sent_to_rth_confirmation(tmp_path):
    path = _db(tmp_path)
    with sqlite3.connect(path) as conn:
        _insert(conn, "plan-c", PREMARKET, "AMD", "long", "C", planning=True)
        conn.execute("""
            CREATE TABLE stocks_paper_decision_snapshots (
                signal_id TEXT PRIMARY KEY, signal_created_at TEXT, symbol TEXT,
                direction TEXT, pre_gate_tier TEXT, funnel_state TEXT,
                target_session_open_at TEXT, snapshot_json TEXT
            )
        """)
        conn.execute(
            "INSERT INTO stocks_paper_decision_snapshots VALUES (?,?,?,?,?,?,?,?)",
            (
                "plan-c", PREMARKET, "AMD", "long", "C", "PREOPEN_PLAN",
                "2026-07-08T13:30:00+00:00",
                json.dumps({
                    "pre_gate_tier": "C",
                    "cap_reasons": ["market_closed_intraday_planning_only"],
                }),
            ),
        )
        conn.commit()

    result = rr.refresh(db=path, now=RTH_CONFIRMED, cfg=_cfg())

    assert result["plans"] == 0
    with sqlite3.connect(path) as conn:
        assert conn.execute(
            "SELECT COUNT(*) FROM stocks_intraday_rth_revalidations"
        ).fetchone()[0] == 0


def test_historical_c_pre_gate_rejection_is_marked_excluded(tmp_path):
    path = _db(tmp_path)
    with sqlite3.connect(path) as conn:
        rr.ensure_tables(conn)
        conn.execute("""
            INSERT INTO stocks_intraday_rth_revalidations(
                plan_signal_id,session_open_at,plan_created_at,symbol,direction,
                plan_pre_gate_tier,decision,reasons_json,evaluated_at,version
            ) VALUES(?,?,?,?,?,?,?,?,?,?)
        """, (
            "plan-c", "2026-07-08T13:30:00+00:00", PREMARKET, "AMD", "long", "C",
            "REJECTED_NO_FRESH_RTH_CANDIDATE", "[]", "2026-07-08T15:15:00+00:00", "old",
        ))
        conn.commit()

    result = rr.refresh(
        db=path, now=datetime(2026, 7, 9, 12, 0, tzinfo=UTC), cfg=_cfg()
    )

    assert result["pre_gate_reconciled"] == 1
    with sqlite3.connect(path) as conn:
        decision = conn.execute(
            "SELECT decision FROM stocks_intraday_rth_revalidations"
        ).fetchone()[0]
    assert decision == "EXCLUDED_PRE_GATE_NOT_AB"


def test_same_signal_id_recomputed_after_open_is_fresh(tmp_path):
    path = _db(tmp_path)
    with sqlite3.connect(path) as conn:
        _insert(conn, "stable-1", PREMARKET, "AMD", "long", "C", planning=True)
        conn.execute("ALTER TABLE proposed_signals ADD COLUMN updated_at TEXT")
        conn.execute(
            "UPDATE proposed_signals SET tier='A',updated_at=?,raw_idea_json=? "
            "WHERE signal_id='stable-1'",
            (
                "2026-07-08T13:44:00+00:00",
                json.dumps({"pre_gate_tier": "A", "cap_reasons": []}),
            ),
        )
        conn.execute("""
            CREATE TABLE stocks_paper_decision_snapshots (
                signal_id TEXT PRIMARY KEY, signal_created_at TEXT, symbol TEXT,
                direction TEXT, pre_gate_tier TEXT, funnel_state TEXT,
                target_session_open_at TEXT, snapshot_json TEXT
            )
        """)
        conn.execute(
            "INSERT INTO stocks_paper_decision_snapshots VALUES (?,?,?,?,?,?,?,?)",
            (
                "stable-1", PREMARKET, "AMD", "long", "A", "PREOPEN_PLAN",
                "2026-07-08T13:30:00+00:00",
                json.dumps({
                    "pre_gate_tier": "A",
                    "cap_reasons": ["market_closed_intraday_planning_only"],
                }),
            ),
        )
        conn.commit()

    result = rr.refresh(db=path, now=RTH_CONFIRMED, cfg=_cfg())
    assert result["plans"] == result["ready"] == 1
    assert result["rows"][0]["rth_signal_id"] == "stable-1"
    assert result["rows"][0]["rth_created_at"] == "2026-07-08T13:44:00+00:00"


def test_fresh_rth_c_is_rejected_with_current_gate_reason(tmp_path):
    path = _db(tmp_path)
    with sqlite3.connect(path) as conn:
        _insert(conn, "plan-1", PREMARKET, "NVDA", "long", "C", planning=True)
        _insert(conn, "fresh-c", "2026-07-08T13:44:00+00:00", "NVDA", "long", "C",
                reasons=["liquidity_rvol_below_min"])
        conn.commit()

    result = rr.refresh(db=path, now=RTH_CONFIRMED, cfg=_cfg())
    assert result["ready"] == 0 and result["rejected"] == 1
    row = result["rows"][0]
    assert row["decision"] == "REJECTED_BY_FRESH_GATES"
    assert "liquidity_rvol_below_min" in json.loads(row["reasons_json"])
    assert row["rth_tier"] == "C"
    assert row["rth_score"] == 80.0


def test_missing_fresh_candidate_is_finalized_after_confirmation_window(tmp_path):
    path = _db(tmp_path)
    with sqlite3.connect(path) as conn:
        _insert(conn, "plan-1", PREMARKET, "AMD", "long", "C", planning=True)
        conn.commit()

    after_window = datetime(2026, 7, 8, 15, 15, tzinfo=UTC)
    result = rr.refresh(db=path, now=after_window, cfg=_cfg())
    assert result["status"] == "ok"
    assert result["finalizing"] is True
    assert result["awaiting"] == 0
    assert result["rejected"] == 1
    assert result["rows"][0]["decision"] == "REJECTED_PREUS_REVIEW_OR_RTH_CANDIDATE_MISSING"
    with sqlite3.connect(path) as conn:
        decision = conn.execute(
            "SELECT decision FROM stocks_intraday_rth_revalidations"
        ).fetchone()[0]
        event = conn.execute(
            "SELECT stage FROM stocks_paper_funnel_events WHERE signal_id='plan-1'"
        ).fetchone()[0]
    assert decision == "REJECTED_PREUS_REVIEW_OR_RTH_CANDIDATE_MISSING"
    assert event == "RTH_REJECTED_PREUS_REVIEW_OR_RTH_CANDIDATE_MISSING"


def test_legacy_awaiting_row_is_terminalized_on_a_later_cycle(tmp_path):
    path = _db(tmp_path)
    with sqlite3.connect(path) as conn:
        _insert(conn, "plan-1", PREMARKET, "AMD", "long", "C", planning=True)
        conn.commit()

    first = rr.refresh(db=path, now=RTH_CONFIRMED, cfg=_cfg(finalize_grace_minutes=180))
    assert first["awaiting"] == 1
    later = rr.refresh(
        db=path, now=datetime(2026, 7, 9, 12, 0, tzinfo=UTC),
        cfg=_cfg(finalize_grace_minutes=180),
    )
    assert later["finalized_stale"] == 1
    with sqlite3.connect(path) as conn:
        decision = conn.execute(
            "SELECT decision FROM stocks_intraday_rth_revalidations"
        ).fetchone()[0]
    assert decision == "REJECTED_PREUS_REVIEW_OR_RTH_CANDIDATE_MISSING"


def test_finalizer_never_uses_candidate_updated_after_window(tmp_path):
    path = _db(tmp_path)
    with sqlite3.connect(path) as conn:
        _insert(conn, "stable-1", PREMARKET, "AMD", "long", "C", planning=True)
        conn.execute("ALTER TABLE proposed_signals ADD COLUMN updated_at TEXT")
        conn.execute(
            "UPDATE proposed_signals SET tier='A',updated_at=?,raw_idea_json=? WHERE signal_id='stable-1'",
            ("2026-07-08T15:05:00+00:00", json.dumps({"pre_gate_tier": "A", "cap_reasons": []})),
        )
        conn.execute("""
            CREATE TABLE stocks_paper_decision_snapshots (
                signal_id TEXT PRIMARY KEY, signal_created_at TEXT, symbol TEXT,
                direction TEXT, pre_gate_tier TEXT, funnel_state TEXT,
                target_session_open_at TEXT, snapshot_json TEXT
            )
        """)
        conn.execute(
            "INSERT INTO stocks_paper_decision_snapshots VALUES (?,?,?,?,?,?,?,?)",
            ("stable-1", PREMARKET, "AMD", "long", "A", "PREOPEN_PLAN",
             "2026-07-08T13:30:00+00:00", json.dumps({
                 "pre_gate_tier": "A", "cap_reasons": ["market_closed_intraday_planning_only"]
             })),
        )
        conn.commit()

    result = rr.refresh(
        db=path, now=datetime(2026, 7, 8, 15, 15, tzinfo=UTC), cfg=_cfg()
    )
    assert result["rows"][0]["decision"] == "REJECTED_PREUS_REVIEW_OR_RTH_CANDIDATE_MISSING"
    assert result["rows"][0]["rth_signal_id"] is None


def test_append_only_observation_preserves_rth_ab_before_lunch_rescore(tmp_path):
    path = _db(tmp_path)
    with sqlite3.connect(path) as conn:
        _insert(conn, "stable-1", PREMARKET, "AMD", "long", "C", planning=True)
        conn.commit()
    paper_funnel.snapshot_signals(
        path, ["stable-1"], now=datetime(2026, 7, 8, 12, 0, tzinfo=UTC)
    )
    with sqlite3.connect(path) as conn:
        conn.execute(
            "UPDATE proposed_signals SET tier='A',score=84,raw_idea_json=? WHERE signal_id='stable-1'",
            (json.dumps({"pre_gate_tier": "A", "cap_reasons": []}),),
        )
        conn.commit()
    paper_funnel.snapshot_signals(
        path, ["stable-1"], now=datetime(2026, 7, 8, 13, 45, tzinfo=UTC)
    )
    with sqlite3.connect(path) as conn:
        conn.execute(
            "UPDATE proposed_signals SET tier='C',score=62,raw_idea_json=? WHERE signal_id='stable-1'",
            (json.dumps({"pre_gate_tier": "A", "cap_reasons": ["lunch_requires_strong_confirmation"]}),),
        )
        conn.commit()
    paper_funnel.snapshot_signals(
        path, ["stable-1"], now=datetime(2026, 7, 8, 15, 5, tzinfo=UTC)
    )

    result = rr.refresh(
        db=path, now=datetime(2026, 7, 8, 15, 15, tzinfo=UTC), cfg=_cfg()
    )
    row = result["rows"][0]
    assert row["decision"] == "READY_FOR_EXISTING_PAPER_TRACKER"
    assert row["rth_tier"] == "A"
    assert row["rth_score"] == 84.0
    with sqlite3.connect(path) as conn:
        assert conn.execute(
            "SELECT COUNT(*) FROM stocks_paper_candidate_observations WHERE signal_id='stable-1'"
        ).fetchone()[0] == 3


def test_revalidation_does_not_run_before_first_confirmation_bar(tmp_path):
    path = _db(tmp_path)
    with sqlite3.connect(path) as conn:
        _insert(conn, "plan-1", PREMARKET, "AMD", "long", "C", planning=True)
        conn.commit()

    before_opening_bar = datetime(2026, 7, 8, 13, 40, tzinfo=UTC)
    result = rr.refresh(db=path, now=before_opening_bar, cfg=_cfg())
    assert result["status"] == "outside_revalidation_window"
    with sqlite3.connect(path) as conn:
        assert conn.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='stocks_intraday_rth_revalidations'"
        ).fetchone()[0] == 0


def test_old_or_non_ab_plans_are_not_eligible(tmp_path):
    path = _db(tmp_path)
    with sqlite3.connect(path) as conn:
        _insert(conn, "old", "2026-07-07T12:00:00+00:00", "AMD", "long", "C", planning=True)
        raw = json.dumps({"pre_gate_tier": "C", "cap_reasons": ["market_closed_intraday_planning_only"]})
        conn.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?,?,?,?,?,?)",
                     ("weak-plan", PREMARKET, "MSFT", "long", "C", 60.0, "open", raw, "stocks", "intraday"))
        conn.commit()

    result = rr.refresh(db=path, now=RTH_CONFIRMED, cfg=_cfg())
    assert result["plans"] == 0


def test_module_is_audit_only():
    source = open(rr.__file__, encoding="utf-8").read().lower()
    for forbidden in ("insert into proposed_signals", "update proposed_signals", "create_order(",
                      "paper_portfolio_ledger", "signal_outcomes", "final_r"):
        assert forbidden not in source
