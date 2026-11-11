"""Tests for news content/entity coverage observability and Telegram recovery selection."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone

from src.news import content_coverage, coverage_gaps, telegram_recovery


NOW = datetime(2026, 7, 13, 12, 0, tzinfo=timezone.utc)


def _db(tmp_path):
    path = str(tmp_path / "news.sqlite")
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE news_items (title TEXT, source TEXT, url TEXT, published_at TEXT, asset_class TEXT, "
        "raw_json TEXT, content_text TEXT, importance REAL, trusted_symbols_json TEXT, resolution_status TEXT)"
    )
    return path, conn


def test_content_coverage_distinguishes_body_summary_and_title_only(tmp_path):
    db, conn = _db(tmp_path)
    stamp = (NOW - timedelta(hours=1)).isoformat()
    conn.executemany(
        "INSERT INTO news_items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [
            ("Title body", "Body Feed", "u1", stamp, "crypto", "{}", "This is a full retained body.", 1, "[]", "ok"),
            ("Title summary", "Summary Feed", "u2", stamp, "stocks", json.dumps({"summary": "More detail"}), None, 1, "[]", "ok"),
            ("Title only", "Title Feed", "u3", stamp, "stocks", "{}", None, 1, "[]", "ok"),
        ],
    )
    conn.commit(); conn.close()
    report = content_coverage.compute_content_coverage(db, now=NOW)
    assert report["summary"] == {"rows": 3, "full_body": 1, "body_equals_title": 0,
                                 "summary_only": 1, "title_only": 1, "full_body_rate": 0.333,
                                 "retained_body_rate": 0.333, "title_only_rate": 0.333}
    assert report["by_asset_class"]["stocks"]["title_only"] == 1


def test_content_coverage_keeps_short_complete_message_separate_from_missing_body():
    assert content_coverage.content_level({"title": "Short Telegram message", "content_text": "Short Telegram message"}) == \
        "body_equals_title"


def test_coverage_gaps_surfaces_untracked_high_impact_listing(tmp_path):
    db, conn = _db(tmp_path)
    conn.execute(
        "INSERT INTO news_items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("MEXC to list VEXAIUSDT perpetual futures", "t.me/listings", "u1", (NOW - timedelta(minutes=10)).isoformat(),
         "crypto", "{}", None, 2.0, "[]", "resolver_confirmed"),
    )
    conn.commit(); conn.close()
    report = coverage_gaps.compute_coverage_gaps(db, now=NOW)
    assert report["potential_gaps"] == 1
    item = report["items"][0]
    assert item["state"] == "untracked_entity" and "listing" in item["impact_labels"]
    assert "VEXAI" in item["untracked_entities"]


def test_coverage_gaps_does_not_queue_generic_legal_context_without_a_candidate(tmp_path):
    db, conn = _db(tmp_path)
    conn.execute(
        "INSERT INTO news_items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("Restaurant faces an expanding food safety lawsuit", "wire", "u1", (NOW - timedelta(minutes=10)).isoformat(),
         "stocks", "{}", None, 2.0, "[]", "resolver_confirmed"),
    )
    conn.commit(); conn.close()
    report = coverage_gaps.compute_coverage_gaps(db, now=NOW)
    assert report["potential_gaps"] == 0
    assert report["non_symbol_impact_rows"] == 1


def test_coverage_gaps_labels_explicit_stock_outside_trade_universe(tmp_path):
    db, conn = _db(tmp_path)
    conn.execute(
        "INSERT INTO news_items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("Tiny issuer (ZZZZ) announces secondary offering", "wire", "u1", (NOW - timedelta(minutes=10)).isoformat(),
         "stocks", "{}", None, 2.0, "[]", "resolver_confirmed"),
    )
    conn.commit(); conn.close()
    report = coverage_gaps.compute_coverage_gaps(db, now=NOW)
    assert report["items"][0]["state"] == "outside_trade_universe"
    assert report["items"][0]["explicit_candidates"] == ["ZZZZ"]


def test_coverage_gaps_excludes_editorial_winner_headline_with_earnings_language(tmp_path):
    db, conn = _db(tmp_path)
    conn.execute(
        "INSERT INTO news_items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("IBM Could Be a Massive Winner as Encryption Becomes Urgent", "publisher", "u1",
         (NOW - timedelta(minutes=10)).isoformat(), "stocks", "{}",
         "The article discusses IBM (NYSE: IBM), revenue and earnings potential.",
         1.5, "[]", "preexisting_unverified"),
    )
    conn.commit(); conn.close()
    report = coverage_gaps.compute_coverage_gaps(db, now=NOW)
    assert report["by_state"]["unmapped_impact"] == 0
    assert report["non_symbol_impact_rows"] == 1


def test_coverage_gaps_excludes_editorial_heres_why_headline(tmp_path):
    db, conn = _db(tmp_path)
    conn.execute(
        "INSERT INTO news_items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("IBM shareholders remain worried after the rally. Here's why.", "publisher", "u1",
         (NOW - timedelta(minutes=10)).isoformat(), "stocks", "{}",
         "IBM (NYSE: IBM) shareholders discuss an acquisition and revenue.",
         2.0, "[]", "preexisting_unverified"),
    )
    conn.commit(); conn.close()
    report = coverage_gaps.compute_coverage_gaps(db, now=NOW)
    assert report["by_state"]["unmapped_impact"] == 0
    assert report["non_symbol_impact_rows"] == 1


def test_coverage_gaps_keeps_factual_earnings_headline_with_explicit_ticker(tmp_path):
    db, conn = _db(tmp_path)
    conn.execute(
        "INSERT INTO news_items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("IBM (NYSE: IBM) reports earnings and raises revenue guidance", "wire", "u1",
         (NOW - timedelta(minutes=10)).isoformat(), "stocks", "{}", None,
         2.0, "[]", "preexisting_unverified"),
    )
    conn.commit(); conn.close()
    report = coverage_gaps.compute_coverage_gaps(db, now=NOW)
    assert report["by_state"]["unmapped_impact"] == 1
    assert report["items"][0]["explicit_candidates"] == ["IBM"]


def test_coverage_gap_crypto_candidate_does_not_treat_a_dollar_amount_as_ticker():
    assert coverage_gaps._explicit_candidates("Revenue reached $419M", "crypto") == []


def test_telegram_recovery_targets_errors_not_normal_quiet_channels(tmp_path):
    health = {"sources": [
        {"source": "t.me/quiet", "source_type": "telegram", "enabled": True, "stale_status": "STALE",
         "rows_72h": 4, "last_fetch_status": "heartbeat", "primary_source": True},
        {"source": "t.me/dead", "source_type": "telegram", "enabled": True, "stale_status": "DEAD",
         "rows_72h": 0, "last_fetch_status": None, "primary_source": False},
        {"source": "t.me/no_rows", "source_type": "telegram", "enabled": True, "stale_status": "STALE",
         "rows_72h": 0, "last_fetch_status": "heartbeat", "primary_source": False},
        {"source": "t.me/error", "source_type": "telegram", "enabled": True, "stale_status": "ERROR",
         "rows_72h": 0, "last_fetch_status": "timeout", "primary_source": True},
    ]}
    db = str(tmp_path / "recovery.sqlite")
    targets = telegram_recovery.select_recovery_targets(health, db=db, now=NOW)
    assert [item["handle"] for item in targets] == ["error", "dead", "no_rows"]
    telegram_recovery.record_attempts([{"source": "t.me/error", "status": "failed", "detail": "timeout"}], db=db, now=NOW)
    later = telegram_recovery.select_recovery_targets(health, db=db, now=NOW + timedelta(hours=1))
    assert [item["handle"] for item in later] == ["dead", "no_rows"]


def test_source_health_exposes_reachable_empty_targeted_recovery(tmp_path):
    from src.news.source_health import compute_source_health
    from src.storage.sqlite import SQLiteStore

    db = tmp_path / "health.sqlite"
    SQLiteStore(db).init_db()
    telegram_recovery.record_attempts(
        [{"source": "t.me/BWEnews", "status": "reachable_empty", "detail": "catch-up reachable"}], db=db, now=NOW,
    )
    row = next(item for item in compute_source_health(str(db), now=NOW)["sources"] if item["source"] == "t.me/BWEnews")
    assert row["targeted_recovery_status"] == "reachable_empty"
    assert "targeted catch-up confirmed" in " ".join(row["warnings"])
    assert "broken feed" not in " ".join(row["warnings"])
