"""Catalyst integrity monitoring after the ASTER fix (profitability guardrails PART 7).

Asserts: a high-importance symbol-tagged news row makes its symbol catalyst-backed
per-signal; a no-catalyst basket containing a direct-news symbol raises a regression
warning; and the ASTER-like case stays catalyst-backed (never promoted).
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

from src.catalysts.integrity import (
    catalyst_integrity_for_signal,
    scan_catalyst_integrity,
)

NOW = datetime.now(timezone.utc)


def _mem_news(rows):
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE news_items (id INTEGER PRIMARY KEY, title TEXT, "
        "published_at TEXT, importance REAL, detected_symbols_json TEXT)"
    )
    for i, r in enumerate(rows, 1):
        conn.execute(
            "INSERT INTO news_items (id,title,published_at,importance,detected_symbols_json) "
            "VALUES (?,?,?,?,?)",
            (i, r["title"], r["published_at"], r.get("importance"), r["symbols"]),
        )
    conn.commit()
    return conn


ASTER = {"title": "Aster Expands its Token Buyback Program",
         "published_at": NOW.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
         "importance": 1.9, "symbols": '["ASTER"]'}


def test_per_signal_catalyst_backed_confirmed():
    conn = _mem_news([ASTER])
    out = catalyst_integrity_for_signal(conn, {"symbol": "ASTER/USDT"}, lookback_hours=48)
    assert out["catalyst_integrity_status"] == "catalyst_backed_confirmed"
    assert out["direct_news_items_checked"] is True
    assert out["catalyst_mapping_confidence"] == "high"


def test_per_signal_no_direct_news():
    conn = _mem_news([ASTER])
    out = catalyst_integrity_for_signal(conn, {"symbol": "FOO/USDT"}, lookback_hours=48)
    assert out["catalyst_integrity_status"] == "no_direct_news_catalyst"
    assert out["direct_news_items_checked"] is True


def test_per_signal_fails_open_to_unknown():
    bad = sqlite3.connect(":memory:")  # no news_items table
    out = catalyst_integrity_for_signal(bad, {"symbol": "ASTER/USDT"})
    assert out["catalyst_integrity_status"] == "unknown"
    assert out["direct_news_items_checked"] is False


def test_daily_scan_counts_high_importance_symbol_tagged():
    conn = _mem_news([ASTER, dict(ASTER, symbols='["BNB"]', importance=1.2)])
    res = scan_catalyst_integrity(conn, now=NOW, lookback_hours=48)
    assert res["high_importance_symbol_tagged"] == 2
    assert "ASTER" in res["catalyst_symbols"]
    assert res["direct_news_items_checked"] is True


def test_daily_scan_treats_artifact_scope_gap_as_diagnostic_not_regression(tmp_path, monkeypatch):
    conn = _mem_news([ASTER])
    day = NOW.astimezone(timezone.utc).strftime("%Y-%m-%d")
    cat_dir = tmp_path / "data" / "catalysts" / day
    cat_dir.mkdir(parents=True)
    (cat_dir / "catalyst_events.jsonl").write_text(json.dumps({
        "symbol": "OTHER/USDT", "related_symbols": [],
    }) + "\n", encoding="utf-8")

    import src.catalysts.integrity as integ
    monkeypatch.setattr(integ, "_catalyst_dir", lambda now: cat_dir)

    res = scan_catalyst_integrity(conn, now=NOW, lookback_hours=48)

    assert res["unmapped_high_importance_symbols"] == ["ASTER"]
    assert res["artifact_scope_gap_symbols"] == ["ASTER"]
    assert res["warning"] is False
    assert res["catalyst_integrity_status"] == "ok"


def test_daily_scan_no_catalyst_basket_news_hit_warns(tmp_path, monkeypatch):
    conn = _mem_news([ASTER])
    # point load_config().root at a tmp dir holding a regression-signature basket
    day = NOW.astimezone(timezone.utc).strftime("%Y-%m-%d")
    cat_dir = tmp_path / "data" / "catalysts" / day
    cat_dir.mkdir(parents=True)
    (cat_dir / "narrative_baskets.jsonl").write_text(json.dumps({
        "basket_name": "momentum_breakout",
        "catalyst_summary": "Top gainers without confirmed news catalyst — pure momentum.",
        "primary_symbols": ["ASTER/USDT"], "related_symbols": [],
    }) + "\n", encoding="utf-8")

    import src.catalysts.integrity as integ

    class _Cfg:
        root = tmp_path
    monkeypatch.setattr(integ, "_catalyst_dir", lambda now: cat_dir)
    res = scan_catalyst_integrity(conn, now=NOW, lookback_hours=48)
    assert "ASTER" in res["no_catalyst_basket_news_hits"]
    assert res["warning"] is True
    assert res["catalyst_integrity_status"] == "warning"


def test_daily_scan_unknown_when_news_table_missing():
    bad = sqlite3.connect(":memory:")
    res = scan_catalyst_integrity(bad, now=NOW)
    assert res["warning"] is True
    assert res["catalyst_integrity_status"] == "unknown"
