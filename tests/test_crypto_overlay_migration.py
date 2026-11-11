"""crypto_quality_overlay_decisions idempotent migration — a persisted refresh must survive an OLD DB
schema (one created before the decision_context_type column existed). READ-MODEL / no drop / no data loss.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

from src.execution import crypto_quality_overlay as cqo

NOW = datetime(2026, 7, 8, 15, 0, tzinfo=timezone.utc)

# the OLD 28-column schema (no decision_context_type) — what the real DB actually had.
_OLD_DDL = (
    "CREATE TABLE crypto_quality_overlay_decisions (signal_id TEXT PRIMARY KEY, symbol TEXT, mode TEXT, "
    "entry_mode TEXT, side TEXT, score REAL, timestamp TEXT, btc_regime_state TEXT, btc_15m_return REAL, "
    "btc_1h_return REAL, btc_ema_slope_state TEXT, eth_confirm_state TEXT, volume_rvol REAL, oi_change REAL, "
    "funding_state TEXT, spread_bps REAL, estimated_slippage_bps REAL, session_bucket_utc TEXT, "
    "session_quality_state TEXT, symbol_cooldown_state TEXT, mode_session_cooldown_state TEXT, "
    "crypto_quality_score REAL, crypto_quality_verdict TEXT, quality_action TEXT, quality_reasons_json TEXT, "
    "would_have_been_action_without_overlay TEXT, overlay_version TEXT, computed_at TEXT)"
)


def test_ensure_tables_migrates_old_schema(tmp_path):
    db = str(tmp_path / "old.sqlite")
    c = sqlite3.connect(db)
    c.execute(_OLD_DDL)
    c.execute("INSERT INTO crypto_quality_overlay_decisions (signal_id, quality_action) VALUES ('old1','FULL_SIZE')")
    c.commit()
    cqo.ensure_tables(c); c.commit()
    cols = {r[1] for r in c.execute("PRAGMA table_info(crypto_quality_overlay_decisions)")}
    assert "decision_context_type" in cols
    # old row preserved (no drop / no data loss) + labelled current_snapshot
    row = c.execute("SELECT quality_action, decision_context_type FROM crypto_quality_overlay_decisions "
                    "WHERE signal_id='old1'").fetchone()
    assert row == ("FULL_SIZE", "current_snapshot")
    # a new explicit-column insert now works
    c.execute("INSERT OR REPLACE INTO crypto_quality_overlay_decisions (" + ",".join(cqo._DECISION_COLS) +
              ") VALUES (" + ",".join("?" * len(cqo._DECISION_COLS)) + ")",
              tuple(["new1"] + [None] * (len(cqo._DECISION_COLS) - 2) + ["point_in_time"]))
    c.commit()
    assert c.execute("SELECT COUNT(*) FROM crypto_quality_overlay_decisions").fetchone()[0] == 2
    # idempotent second call — no error, no change
    cqo.ensure_tables(c); c.commit()
    c.close()


def test_persisted_refresh_survives_old_schema(tmp_path):
    # the actual bug: a PERSISTED refresh (not --dry-run) must not crash on an old-schema DB.
    db = str(tmp_path / "old2.sqlite")
    c = sqlite3.connect(db)
    c.execute(_OLD_DDL)
    c.execute("INSERT INTO crypto_quality_overlay_decisions (signal_id, quality_action) VALUES ('legacy','HALF_SIZE')")
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT, symbol TEXT, mode TEXT, direction TEXT, "
              "score REAL, news_supported INT, asset_class TEXT, created_at TEXT)")
    c.execute("INSERT INTO proposed_signals VALUES ('s1','DOGE/USDT','intraday','long',70,0,'crypto',?)",
              (NOW.isoformat(),))
    c.commit(); c.close()
    res = cqo.refresh(db=db, persist=True, now_iso=NOW.isoformat())   # must NOT raise
    assert res["evaluated"] >= 1
    c = sqlite3.connect(db)
    # new decision persisted with the snapshot label; legacy row backfilled to current_snapshot
    new = c.execute("SELECT decision_context_type FROM crypto_quality_overlay_decisions WHERE signal_id='s1'").fetchone()
    leg = c.execute("SELECT quality_action, decision_context_type FROM crypto_quality_overlay_decisions "
                    "WHERE signal_id='legacy'").fetchone()
    c.close()
    assert new and new[0] == "current_snapshot"
    assert leg == ("HALF_SIZE", "current_snapshot")   # preserved + labelled
