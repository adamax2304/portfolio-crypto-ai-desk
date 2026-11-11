"""PART 3 — Per-signal structural paper TP set (paper-only, add-only).

For each actionable paper trade, compute take-profits from REAL chart structure
(swing H/L, range bounds, round numbers, volume profile) using the SAME OHLCV the
tracker reads, and persist a labelled set into `signal_paper_tp`:

  mechanical_tp1/2/3   — the production ATR-ladder TPs (UNCHANGED, copied for reference)
  active_paper_tp1/2/3 — the paper TPs actually used (structural when levels exist)
  tp_set_type          — STRUCTURAL | HYBRID | ATR_FALLBACK | NO_VALID_TP

Production TP generation (`proposed_signals.tp1/2/3`) and `signal_outcomes.final_r`
are NEVER touched. This is a read-model enrichment consumed by the paper lifecycle /
UI / close alerts. The whole point vs the old backfill (which passed candles=None and
therefore could only ATR-fallback) is that here we feed real candles, so STRUCTURAL /
HYBRID actually fire when the chart has levels.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

from src.config import load_config
from src.storage.file_store import FileStore
from src.execution.structural_tp_engine import generate_structural_tps

# engine tp_set_label → public tp_set_type (per the PART 3 contract)
_LABEL_TO_TYPE = {
    "STRUCTURAL": "STRUCTURAL",
    "HYBRID": "HYBRID",
    "STRUCTURAL_FALLBACK_ATR": "ATR_FALLBACK",
    "NO_VALID_TP": "NO_VALID_TP",
}

_DDL = """
CREATE TABLE IF NOT EXISTS signal_paper_tp (
  signal_id TEXT PRIMARY KEY, symbol TEXT, direction TEXT,
  entry REAL, stop REAL,
  mechanical_tp1 REAL, mechanical_tp2 REAL, mechanical_tp3 REAL,
  active_paper_tp1 REAL, active_paper_tp2 REAL, active_paper_tp3 REAL,
  tp1_r REAL, tp2_r REAL, tp3_r REAL,
  tp1_source TEXT, tp2_source TEXT, tp3_source TEXT,
  tp_set_type TEXT, confidence REAL,
  volume_profile_supported INTEGER, candles_used INTEGER,
  reasons TEXT, warnings TEXT, computed_at TEXT
);
"""


def ensure_table(conn: sqlite3.Connection) -> None:
    conn.execute(_DDL)
    conn.commit()


def _candles_for(fs, cfg, symbol, mode, asset_class, exchange_focus, created_at=None):
    """Load the OHLCV window the tracker would use and return it as a list of
    {open,high,low,close} dicts (what the structure engine expects). None on miss.

    PART 6 (look-ahead safety): the structural TP/stop overlay PLACES levels from pre-signal
    context, so — when ``created_at`` is given — only candles with ``timestamp <= created_at`` are
    used. This mirrors the tracker's ``_filter_candles_after`` (which walks OUTCOMES on candles
    ``>= created_at``). Without this, ``.tail(200)`` of the rolling cache leaked future bars into
    the placement, contaminating backfilled overlays with look-ahead."""
    try:
        if str(asset_class or "").lower().startswith("stock"):
            from src.signals.tracker import _load_stocks_ohlcv_for_signal
            df, _, _ = _load_stocks_ohlcv_for_signal(fs, symbol, mode or "intraday")
        else:
            from src.signals.tracker import _load_ohlcv_for_signal
            df, _, _ = _load_ohlcv_for_signal(fs, cfg, symbol, mode or "intraday",
                                              exchange_focus or "")
        if df is None or getattr(df, "empty", True):
            return None
        cols = ("open", "high", "low", "close")
        if not all(c in df.columns for c in cols):
            return None
        if created_at and "timestamp" in df.columns:
            from src.signals.tracker import _parse_ts
            cutoff = _parse_ts(created_at)
            if cutoff is not None:
                df = df.loc[df["timestamp"] <= cutoff]
        if df is None or getattr(df, "empty", True):
            return None
        return df[list(cols)].tail(200).to_dict("records")
    except Exception:
        return None


def compute_record(trade: dict, meta: dict, fs, cfg) -> dict:
    """Compute the labelled paper-TP record for one trade. Pure given inputs."""
    entry, stop = trade.get("entry"), trade.get("stop")
    candles = _candles_for(fs, cfg, trade.get("symbol"), meta.get("mode"),
                           trade.get("asset_class"), meta.get("exchange_focus"),
                           created_at=trade.get("created_at"))
    risk_abs = abs((entry or 0) - (stop or 0)) or None
    stp = generate_structural_tps(
        entry=entry, stop=stop, direction=trade.get("direction") or "long",
        candles=candles, atr=risk_abs, market_regime=trade.get("regime"),
        playbook=trade.get("playbook"),
        mechanical_tp1=trade.get("tp1"), mechanical_tp2=trade.get("tp2"),
        mechanical_tp3=trade.get("tp3"),
    )
    return {
        "signal_id": trade.get("signal_id"), "symbol": trade.get("symbol"),
        "direction": trade.get("direction"), "entry": entry, "stop": stop,
        "mechanical_tp1": trade.get("tp1"), "mechanical_tp2": trade.get("tp2"),
        "mechanical_tp3": trade.get("tp3"),
        "active_paper_tp1": stp.tp1, "active_paper_tp2": stp.tp2, "active_paper_tp3": stp.tp3,
        "tp1_r": stp.tp1_r, "tp2_r": stp.tp2_r, "tp3_r": stp.tp3_r,
        "tp1_source": stp.tp1_source, "tp2_source": stp.tp2_source, "tp3_source": stp.tp3_source,
        "tp_set_type": _LABEL_TO_TYPE.get(stp.tp_set_label, stp.tp_set_label),
        "confidence": stp.confidence,
        "volume_profile_supported": 1 if stp.volume_profile_supported else 0,
        "candles_used": len(candles) if candles else 0,
        "reasons": json.dumps(stp.reasons), "warnings": json.dumps(stp.warnings),
        "computed_at": datetime.now(timezone.utc).isoformat(),
    }


def _upsert(conn: sqlite3.Connection, rec: dict) -> None:
    cols = list(rec.keys())
    conn.execute(
        f"INSERT OR REPLACE INTO signal_paper_tp ({','.join(cols)}) "
        f"VALUES ({','.join('?' * len(cols))})",
        [rec[c] for c in cols],
    )


def _f(v):
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


_REFRESH_TABLES = {
    "signal_paper_tp",
    "signal_entry_mode",
    "signal_stop_plan",
}


def _entry_triggered_signals(
    conn: sqlite3.Connection,
    limit: int,
    *,
    refresh_table: str = "signal_paper_tp",
) -> list[dict]:
    """Every entry-triggered signal (latest outcome), keyed by its REAL signal_id — no
    economic-key dedup — so each trade the UI can open has its own paper-TP record.
    Mirrors load_trades' entry/stop derivation. exchange_focus optional on older DBs."""
    if refresh_table not in _REFRESH_TABLES:
        raise ValueError(f"unsupported refresh table: {refresh_table}")
    # signal_outcomes has millions of lifecycle snapshots but only thousands of
    # proposed signals. Drive the lookup from proposed_signals and use the
    # existing (signal_id,id) index to fetch one latest row per signal. The old
    # ROW_NUMBER() CTE scanned and sorted the complete outcome history on every
    # bounded refresh, making a 200-row batch take several minutes.
    base = (
        "SELECT p.signal_id, p.symbol, p.direction, p.mode, p.asset_class, p.setup_type, "
        "p.market_regime, p.created_at, {extra} p.suggested_entry, p.entry_trigger, p.entry_low, "
        "p.stop_loss, p.invalidation, p.tp1, p.tp2, p.tp3, o.entry_triggered_at "
        "FROM proposed_signals p "
        "JOIN signal_outcomes o ON o.id=("
        "  SELECT so.id FROM signal_outcomes so WHERE so.signal_id=p.signal_id "
        "  ORDER BY so.id DESC LIMIT 1"
        ") "
        f"LEFT JOIN {refresh_table} existing ON existing.signal_id=p.signal_id "
        "WHERE o.entry_triggered=1 "
        # Work through missing/old records first.  A bounded scheduler batch
        # then refreshes the entire active set over successive cycles instead
        # of repeatedly repricing the same newest rows until it times out.
        "ORDER BY CASE WHEN existing.computed_at IS NULL THEN 0 ELSE 1 END, "
        "existing.computed_at ASC, o.entry_triggered_at DESC LIMIT ?"
    )
    try:
        rows = conn.execute(base.format(extra="p.exchange_focus,"), (limit,)).fetchall()
    except sqlite3.OperationalError:
        rows = conn.execute(base.format(extra=""), (limit,)).fetchall()
    trades = []
    for r in rows:
        d = dict(r)
        entry = _f(d.get("entry_trigger")) or _f(d.get("suggested_entry")) or _f(d.get("entry_low"))
        stop = _f(d.get("invalidation")) or _f(d.get("stop_loss"))
        if not entry or not stop or abs(entry - stop) <= 0:
            continue
        trades.append({
            "signal_id": d["signal_id"], "symbol": d["symbol"],
            "direction": (d.get("direction") or "long").lower(),
            "asset_class": d.get("asset_class"), "entry": entry, "stop": stop,
            "created_at": d.get("created_at"),  # PART 6: cutoff for look-ahead-safe context candles
            "tp1": _f(d.get("tp1")), "tp2": _f(d.get("tp2")), "tp3": _f(d.get("tp3")),
            "playbook": d.get("setup_type") or "", "regime": d.get("market_regime") or "",
            "_meta": {"mode": d.get("mode"), "exchange_focus": d.get("exchange_focus") or ""},
        })
    return trades


def refresh(limit: int = 600, db: str | None = None) -> dict:
    """Recompute + persist structural paper TPs for recent entry-triggered signals.
    Returns {processed, by_type, structural_used, candles_hit}."""
    cfg = load_config()
    fs = FileStore(cfg)
    db = db or cfg.db_path
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    ensure_table(conn)
    conn.commit()
    trades = _entry_triggered_signals(
        conn, limit, refresh_table="signal_paper_tp"
    )
    by_type: dict[str, int] = {}
    candles_hit = 0
    records = []
    for t in trades:
        rec = compute_record(t, t.get("_meta", {}), fs, cfg)
        records.append(rec)
        by_type[rec["tp_set_type"]] = by_type.get(rec["tp_set_type"], 0) + 1
        if rec["candles_used"] > 0:
            candles_hit += 1
    for index, rec in enumerate(records, start=1):
        _upsert(conn, rec)
        if index % 50 == 0:
            conn.commit()
    conn.commit()
    conn.close()
    structural_used = by_type.get("STRUCTURAL", 0) + by_type.get("HYBRID", 0)
    return {"processed": len(trades), "by_type": by_type,
            "structural_used": structural_used, "candles_hit": candles_hit}


def get_paper_tp(signal_id: str, db: str | None = None) -> dict | None:
    """Read-only accessor for a single signal's persisted paper-TP set."""
    cfg = load_config()
    conn = sqlite3.connect(db or cfg.db_path)
    conn.row_factory = sqlite3.Row
    try:
        ensure_table(conn)
        row = conn.execute(
            "SELECT * FROM signal_paper_tp WHERE signal_id=?", (signal_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()
