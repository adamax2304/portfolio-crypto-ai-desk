from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

from src.execution import stocks_catalyst_rs_shadow as catalyst
from src.execution import stocks_earnings_gap_shadow as earnings


UTC = timezone.utc


def _news_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE news_canonical_events (event_id TEXT, news_item_id INTEGER, asset_class TEXT, "
        "linkage_allowed INTEGER, effective_at TEXT, published_at TEXT, created_at TEXT, event_type TEXT, "
        "title TEXT, trusted_symbols_json TEXT, mentioned_symbols_json TEXT, source_quality TEXT)"
    )
    base = ("stocks", 1, "2026-07-14T13:00:00+00:00", "2026-07-14T13:00:00+00:00",
            "2026-07-14T13:01:00+00:00", '["AAPL"]', '["AAPL"]', "primary")
    conn.execute("INSERT INTO news_canonical_events VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
        "earnings", 1, *base[:5], "earnings", "AAPL reports earnings", *base[5:],
    ))
    conn.execute("INSERT INTO news_canonical_events VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
        "guidance", 2, *base[:5], "guidance", "AAPL raises guidance", *base[5:],
    ))
    return conn


def test_earnings_allowed_scope_is_not_additive():
    conn = _news_db()
    cfg = earnings.load_cfg()
    candidates, _ = catalyst._event_candidates(
        conn, cfg, datetime(2026, 7, 15, tzinfo=UTC), {"AAPL"}, {"AAPL": "technology"},
        {"technology": "XLK"}, start_at=datetime(2026, 7, 14, tzinfo=UTC),
    )
    conn.close()
    assert [item["event"]["event_type"] for item in candidates] == ["earnings"]


def test_earnings_session_dedupe_keeps_only_first_executable_row():
    rows = [
        {"candidate_id": "first", "symbol": "AAPL", "catalyst_at": "2026-07-14T13:00:00+00:00",
         "decision_at": "2026-07-14T14:00:00+00:00", "entry_ts": "2026-07-14T14:00:00+00:00",
         "eligibility_status": "eligible", "outcome_status": "closed", "net_pnl_usd": 12.0,
         "fees_usd": 1.0, "slippage_usd": 1.0, "funding_usd": 0.0, "evidence_cohort": "strict_v1"},
        {"candidate_id": "second", "symbol": "AAPL", "catalyst_at": "2026-07-14T13:05:00+00:00",
         "decision_at": "2026-07-14T14:15:00+00:00", "entry_ts": "2026-07-14T14:15:00+00:00",
         "eligibility_status": "eligible", "outcome_status": "closed", "net_pnl_usd": 99.0,
         "fees_usd": 1.0, "slippage_usd": 1.0, "funding_usd": 0.0, "evidence_cohort": "strict_v1"},
    ]
    result = earnings._deduplicate_entries(rows)
    assert result[0]["dedupe_status"] == "unique"
    assert result[1]["dedupe_status"] == "duplicate_skipped"
    assert result[1]["duplicate_of_candidate_id"] == "first"
    assert result[1]["eligibility_status"] == "rejected"
    assert result[1]["rejection_reason"] == "EVENT_SESSION_DUPLICATE"
    assert result[1]["net_pnl_usd"] == 0.0


def test_earnings_summary_counts_only_real_unique_closed_trades():
    rows = [
        {"window": "forward_post_activation", "is_clean_for_edge": 1,
         "outcome_status": "closed", "dedupe_status": "unique", "net_pnl_usd": 10.0},
        {"window": "forward_post_activation", "is_clean_for_edge": 1,
         "outcome_status": "skipped", "dedupe_status": "unique", "net_pnl_usd": 0.0},
        {"window": "forward_post_activation", "is_clean_for_edge": 1,
         "outcome_status": "closed", "dedupe_status": "duplicate_skipped", "net_pnl_usd": 99.0},
    ]
    summary = earnings._summary(rows, "2026-07-01T00:00:00+00:00")
    assert summary["clean_closed"] == 1
    assert summary["net_pnl_usd"] == 10.0


def test_earnings_v2_has_a_fresh_profile_and_lane():
    cfg = earnings.load_cfg()
    assert cfg["strategy_id"].endswith("_v2")
    assert cfg["profile_id"].endswith("_v2")
    assert cfg["shadow_lane"].endswith("_v2")


def test_earnings_refresh_never_writes_paper_or_live_tables(tmp_path):
    db = tmp_path / "earnings-guard.sqlite"
    conn = sqlite3.connect(db)
    protected = ("proposed_signals", "signal_outcomes", "final_r", "paper_ledger", "live_routing")
    for table in protected:
        conn.execute(f"CREATE TABLE {table}(value TEXT)")
        conn.execute(f"INSERT INTO {table} VALUES ('stable')")
    conn.commit()
    before = {table: conn.execute(f"SELECT * FROM {table}").fetchall() for table in protected}
    conn.close()

    earnings.refresh(db=str(db), now=datetime(2026, 7, 15, tzinfo=UTC), persist=True)

    conn = sqlite3.connect(db)
    for table, expected in before.items():
        assert conn.execute(f"SELECT * FROM {table}").fetchall() == expected
    assert conn.execute("SELECT name FROM sqlite_master WHERE name=?", (earnings.TABLE,)).fetchone()
    conn.close()
