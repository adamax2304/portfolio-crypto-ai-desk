"""PART 8 — Per-signal structural stop-move plan (paper read-model, add-only).

The control-plane lifecycle currently moves the protective stop with an R-based placeholder
(BE after TP1, +0.5R lock after TP2). The structural stop manager exists but was never fed
chart data. This module computes, per signal, where the stop should move after TP1 and TP2 —
**preferring chart structure** (higher-low / lower-high / support / resistance / VWAP) and only
falling back to BE/lock when no structure protects — using the real OHLCV, and persists it into
`signal_stop_plan` so the lifecycle can drive the moved stop from structure and show the basis.

Read-model / accounting only: never places an order, never moves a production stop, never
touches signal_outcomes / final_r.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

from src.config import load_config
from src.storage.file_store import FileStore
from src.execution.structural_stop_manager import structural_stop_after_tp
from src.execution.signal_paper_tp import _candles_for, _entry_triggered_signals

_STRUCT_BASES = {"higher_low", "lower_high", "support", "resistance", "vwap"}

_DDL = """
CREATE TABLE IF NOT EXISTS signal_stop_plan (
  signal_id TEXT PRIMARY KEY, symbol TEXT, direction TEXT, entry REAL, initial_stop REAL,
  stop_after_tp1 REAL, stop_after_tp1_r REAL, stop_after_tp1_basis TEXT,
  stop_after_tp2 REAL, stop_after_tp2_r REAL, stop_after_tp2_basis TEXT,
  prefers_structure INTEGER, candles_used INTEGER, reason TEXT, computed_at TEXT,
  sanity_review INTEGER
);
"""

# PART 9: a stop-after-TP that "locks" more than this many R is not a plausible structural stop —
# flag it for review instead of silently trusting absurd structure detection.
SANITY_MAX_STOP_R = 15.0


def ensure_table(conn):
    conn.execute(_DDL)
    # migrate older tables that predate sanity_review
    if "sanity_review" not in {r[1] for r in conn.execute("PRAGMA table_info(signal_stop_plan)")}:
        conn.execute("ALTER TABLE signal_stop_plan ADD COLUMN sanity_review INTEGER")
    conn.commit()


def compute_record(trade: dict, meta: dict, fs, cfg) -> dict:
    entry, stop0 = trade.get("entry"), trade.get("stop")
    direction = trade.get("direction") or "long"
    candles = _candles_for(fs, cfg, trade.get("symbol"), meta.get("mode"),
                           trade.get("asset_class"), meta.get("exchange_focus"),
                           created_at=trade.get("created_at"))  # PART 6: look-ahead-safe context
    # after TP1 — from the initial stop
    m1 = structural_stop_after_tp(tp_index=1, entry=entry, initial_stop=stop0,
                                  current_stop=stop0, direction=direction, candles=candles)
    # after TP2 — from wherever TP1 left the stop
    m2 = structural_stop_after_tp(tp_index=2, entry=entry, initial_stop=stop0,
                                  current_stop=m1.new_stop, direction=direction, candles=candles)
    prefers = (m1.structure_used in _STRUCT_BASES) or (m2.structure_used in _STRUCT_BASES)
    # PART 9: sanity — a stop that locks an absurd amount of R is not a real structural level.
    worst_r = max(abs(m1.protection_r or 0), abs(m2.protection_r or 0))
    sanity_review = 1 if worst_r > SANITY_MAX_STOP_R else 0
    reason = f"TP1→{m1.structure_used} {m1.protection_r:+.2f}R; TP2→{m2.structure_used} {m2.protection_r:+.2f}R"
    if sanity_review:
        reason += f" [REVIEW: stop_after_tp {worst_r:.1f}R > {SANITY_MAX_STOP_R:.0f}R sanity bound]"
    return {
        "signal_id": trade.get("signal_id"), "symbol": trade.get("symbol"),
        "direction": direction, "entry": entry, "initial_stop": stop0,
        "stop_after_tp1": m1.new_stop, "stop_after_tp1_r": m1.protection_r,
        "stop_after_tp1_basis": m1.structure_used,
        "stop_after_tp2": m2.new_stop, "stop_after_tp2_r": m2.protection_r,
        "stop_after_tp2_basis": m2.structure_used,
        "prefers_structure": 1 if prefers else 0,
        "candles_used": len(candles) if candles else 0,
        "reason": reason, "sanity_review": sanity_review,
        "computed_at": datetime.now(timezone.utc).isoformat(),
    }


def _upsert(conn, rec):
    cols = list(rec.keys())
    conn.execute(f"INSERT OR REPLACE INTO signal_stop_plan ({','.join(cols)}) "
                 f"VALUES ({','.join('?' * len(cols))})", [rec[c] for c in cols])


def refresh(limit: int = 800, db: str | None = None) -> dict:
    cfg = load_config()
    fs = FileStore(cfg)
    conn = sqlite3.connect(db or cfg.db_path)
    conn.row_factory = sqlite3.Row
    ensure_table(conn)
    conn.commit()
    trades = _entry_triggered_signals(
        conn, limit, refresh_table="signal_stop_plan"
    )
    structure_moves = candles_hit = 0
    by_basis: dict[str, int] = {}
    records = []
    for t in trades:
        rec = compute_record(t, t.get("_meta", {}), fs, cfg)
        records.append(rec)
        if rec["prefers_structure"]:
            structure_moves += 1
        if rec["candles_used"] > 0:
            candles_hit += 1
        for b in (rec["stop_after_tp1_basis"], rec["stop_after_tp2_basis"]):
            by_basis[b] = by_basis.get(b, 0) + 1
    for index, rec in enumerate(records, start=1):
        _upsert(conn, rec)
        if index % 50 == 0:
            conn.commit()
    conn.commit()
    conn.close()
    return {"processed": len(trades), "candles_hit": candles_hit,
            "structure_moves": structure_moves, "by_basis": by_basis}


def get_stop_plan(signal_id: str, db: str | None = None) -> dict | None:
    cfg = load_config()
    conn = sqlite3.connect(db or cfg.db_path)
    conn.row_factory = sqlite3.Row
    try:
        ensure_table(conn)
        row = conn.execute(
            "SELECT * FROM signal_stop_plan WHERE signal_id=?", (signal_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()
