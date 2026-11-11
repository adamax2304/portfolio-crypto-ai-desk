"""PART 1 catalyst-integrity regression tests (ASTER buyback case).

A high-importance symbol-tagged news_items row must (a) be found by the direct
per-symbol lookup, and (b) prevent the momentum_breakout basket from labeling that
mover "no confirmed news catalyst". Label/enrichment only — no scoring/entry change,
no promotion to actionable (catalyst-backed-but-extended → watch pullback, not chase).
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone

from src.catalysts.baskets import build_momentum_breakout_basket
from src.catalysts.collector import news_catalyst_symbols

NOW = datetime.now(timezone.utc)


def _mem_news(rows, *, sym_col="detected_symbols_json", with_importance=True):
    conn = sqlite3.connect(":memory:")
    imp = "importance REAL," if with_importance else ""
    conn.execute(
        f"CREATE TABLE news_items (id INTEGER PRIMARY KEY, title TEXT, "
        f"published_at TEXT, {imp} {sym_col} TEXT)"
    )
    for i, r in enumerate(rows, 1):
        if with_importance:
            conn.execute(
                f"INSERT INTO news_items (id,title,published_at,importance,{sym_col}) VALUES (?,?,?,?,?)",
                (i, r["title"], r["published_at"], r.get("importance"), r["symbols"]),
            )
        else:
            conn.execute(
                f"INSERT INTO news_items (id,title,published_at,{sym_col}) VALUES (?,?,?,?)",
                (i, r["title"], r["published_at"], r["symbols"]),
            )
    conn.commit()
    return conn


ASTER_ROW = {
    "title": "Aster Expands its Token Buyback Program, Price Jumps 10%",
    "published_at": NOW.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
    "importance": 1.9,
    "symbols": '["ASTER"]',
}
MOVERS = [
    {"symbol": "ASTER/USDT", "score": 72, "return_24h_pct": 14.0, "volume_ratio": 1.4,
     "overextension_risk": True},
    {"symbol": "FOO/USDT", "score": 60, "return_24h_pct": 11.0, "volume_ratio": 0.9},
]


def test_news_catalyst_symbols_finds_aster():
    conn = _mem_news([ASTER_ROW])
    assert "ASTER" in news_catalyst_symbols(conn, lookback_hours=48, min_importance=1.0)


def test_news_catalyst_symbols_importance_threshold_excludes_low():
    low = dict(ASTER_ROW, importance=0.3)
    assert "ASTER" not in news_catalyst_symbols(_mem_news([low]), lookback_hours=48, min_importance=1.0)


def test_news_catalyst_symbols_schema_discovery_legacy_column():
    # Legacy DB with a bare `detected_symbols` column must still resolve.
    conn = _mem_news([ASTER_ROW], sym_col="detected_symbols")
    assert "ASTER" in news_catalyst_symbols(conn, lookback_hours=48, min_importance=1.0)


def test_news_catalyst_symbols_old_row_excluded_by_window():
    old = dict(ASTER_ROW, published_at=(NOW - timedelta(hours=72)).strftime("%Y-%m-%dT%H:%M:%S+00:00"))
    assert "ASTER" not in news_catalyst_symbols(_mem_news([old]), lookback_hours=24, min_importance=1.0)


def test_momentum_basket_does_not_call_catalyst_backed_no_catalyst():
    b = build_momentum_breakout_basket(MOVERS, catalyst_symbols={"ASTER"})
    assert b is not None
    s = b.catalyst_summary
    assert "ASTER" in s and "CATALYST-BACKED" in s
    # ASTER must NOT be in the "without confirmed catalyst" clause
    without = s.split("Without confirmed catalyst:")[1].split(".")[0] if "Without confirmed catalyst:" in s else ""
    assert "ASTER" not in without
    # catalyst-backed + overextended → watch pullback (NOT a blind no-catalyst chase)
    assert b.suggested_playbook == "wait_pullback"


def test_momentum_basket_regression_no_catalyst_when_set_empty():
    # Without a catalyst set, behavior is the prior "no confirmed news catalyst" label.
    b = build_momentum_breakout_basket(MOVERS, catalyst_symbols=set())
    assert b is not None
    assert "without confirmed news catalyst" in b.catalyst_summary.lower()


def test_momentum_basket_does_not_promote_to_actionable():
    # The basket never sets an actionable/entry field — it's enrichment only.
    b = build_momentum_breakout_basket(MOVERS, catalyst_symbols={"ASTER"})
    assert b.basket_name == "momentum_breakout"
    assert b.suggested_playbook in {"wait_pullback", "avoid_chase"}  # never "enter"/"buy"
