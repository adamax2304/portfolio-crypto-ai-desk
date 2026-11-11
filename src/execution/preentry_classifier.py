"""Pre-entry entry-mode classifier (SHADOW-ONLY, LOOKAHEAD-SAFE, READ-MODEL).

Prepares the "true new strategy" test (B): classify the entry_mode that WOULD have
been chosen at signal creation/registration time — BEFORE the entry-triggered stage,
for EVERY registered signal (including ones that never entered). This differs from the
existing `signal_entry_mode` (post-entry classifier), which only labels entered signals.

Writes ONLY `signal_entry_mode_preentry`. STRICTLY lookahead-safe: only candles with
timestamp <= created_at inform the label (enforced here, independent of the loader).
NEVER changes proposed_signals / routing / actionability / Telegram / live / final_r.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from src.execution.entry_mode_classifier import classify
from src.storage.file_store import FileStore

_DDL = """
CREATE TABLE IF NOT EXISTS signal_entry_mode_preentry (
  signal_id TEXT PRIMARY KEY, computed_at TEXT, created_at TEXT, asset_class TEXT, mode TEXT,
  entry_mode TEXT, suggested_entry REAL, confidence REAL, reason TEXT, candles_used INTEGER,
  data_quality TEXT, source TEXT
);
"""

MIN_CANDLES_OK = 20   # >= this -> data_quality 'ok'; 1..N-1 -> 'thin'; 0 -> 'no_data'


def ensure_tables(conn) -> None:
    """Create the additive pre-entry table and migrate older local databases.

    ``source`` is provenance, not a trading input.  It distinguishes a classifier
    result captured in the entry path from a later scheduler backfill, so a
    post-hoc row is never presented as real-time evidence.
    """
    conn.execute(_DDL)
    cols = {r[1] for r in conn.execute("PRAGMA table_info(signal_entry_mode_preentry)")}
    if "source" not in cols:
        conn.execute("ALTER TABLE signal_entry_mode_preentry ADD COLUMN source TEXT")
        conn.execute("UPDATE signal_entry_mode_preentry SET source='legacy_backfill' WHERE source IS NULL")
    conn.commit()


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def _f(v):
    try:
        return None if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return None


_TF_SECONDS = {
    "1m": 60, "3m": 180, "5m": 300, "15m": 900, "30m": 1800,
    "1h": 3600, "2h": 7200, "4h": 14400, "6h": 21600, "8h": 28800, "12h": 43200,
    "1d": 86400, "3d": 259200, "1w": 604800,
}


def _tf_to_timedelta(tf: str):
    """Bar duration for a timeframe string ('1h','15m','1d'...). Returns a pandas Timedelta,
    or None if unknown (caller then falls back to a strict open-time guard)."""
    import pandas as pd
    secs = _TF_SECONDS.get(str(tf or "").strip().lower())
    return pd.Timedelta(seconds=secs) if secs else None


def closed_candles(df, tf, created_at):
    """Return only FULLY-CLOSED candles as of created_at (lookahead-safe): candle_close_time =
    open_time + timeframe, keep rows where close_time <= created_at. If the bar timestamp is the
    OPEN time (Binance/MEXC/Bybit convention), this drops the in-progress candle that contains
    created_at. Unknown tf -> conservative strict open-time guard (timestamp < created_at)."""
    import pandas as pd
    if df is None or getattr(df, "empty", True) or "timestamp" not in getattr(df, "columns", []):
        return df
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    if not created_at:
        return df
    cre = pd.to_datetime(created_at, utc=True)
    tf_delta = _tf_to_timedelta(tf)
    if tf_delta is not None:
        return df[df["timestamp"] + tf_delta <= cre]   # close_time <= created_at
    return df[df["timestamp"] < cre]                    # unknown tf -> strict open-time guard


def _candles_le_created(fs, cfg, symbol, mode, asset_class, exchange_focus, created_at) -> list[dict]:
    """Load real OHLCV and keep only FULLY-CLOSED bars as of created_at (candle_close_time <=
    created_at). Uses the loader's timeframe so an in-progress candle is never seen."""
    try:
        if str(asset_class or "").lower().startswith("stock"):
            from src.signals.tracker import _load_stocks_ohlcv_for_signal
            df, _, tf = _load_stocks_ohlcv_for_signal(fs, symbol, mode or "intraday")
        else:
            from src.signals.tracker import _load_ohlcv_for_signal
            df, _, tf = _load_ohlcv_for_signal(fs, cfg, symbol, mode or "intraday", exchange_focus or "")
    except Exception:
        return []
    df = closed_candles(df, tf, created_at)
    if df is None or getattr(df, "empty", True):
        return []
    return [{"open": _f(r.get("open")), "high": _f(r.get("high")),
             "low": _f(r.get("low")), "close": _f(r.get("close"))}
            for _, r in df.iterrows()]


def classify_preentry_from_candles(*, direction, entry_low, entry_high, entry, stop, candles) -> dict:
    """Pure: classify entry_mode from a pre-supplied (already-filtered) candle list."""
    atr_hint = (abs((entry or 0) - (stop or 0)) / 1.2) or None
    c = classify(entry_low=entry_low, entry_high=entry_high,
                 direction=direction or "long", candles=candles, atr_hint=atr_hint)
    used = int(c.get("candles_used") or 0)
    dq = "ok" if used >= MIN_CANDLES_OK else ("thin" if used > 0 else "no_data")
    return {"entry_mode": c["entry_mode"], "suggested_entry": c["suggested_entry"],
            "confidence": c["confidence"], "reason": c["reason"], "candles_used": used,
            "data_quality": dq}


def _classify_signal_row(row, *, fs, cfg) -> dict:
    """Classify one proposed-signal row using only closed pre-creation candles."""
    candles = _candles_le_created(fs, cfg, row["symbol"], row["mode"], row["asset_class"],
                                  row["exchange_focus"], row["created_at"])
    return classify_preentry_from_candles(
        direction=row["direction"], entry_low=_f(row["entry_low"]), entry_high=_f(row["entry_high"]),
        entry=_f(row["suggested_entry"]), stop=_f(row["stop_used"]), candles=candles)


def _write_record(conn, row, rec: dict, *, source: str) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    out = {"signal_id": row["signal_id"], "computed_at": now, "created_at": row["created_at"],
           "asset_class": row["asset_class"], "mode": row["mode"], **rec, "source": source}
    cols = ("signal_id", "computed_at", "created_at", "asset_class", "mode", "entry_mode",
            "suggested_entry", "confidence", "reason", "candles_used", "data_quality", "source")
    conn.execute("INSERT OR REPLACE INTO signal_entry_mode_preentry (" + ",".join(cols) + ") VALUES ("
                 + ",".join("?" * len(cols)) + ")", tuple(out[k] for k in cols))
    return out


def ensure_for_signal(signal: dict, *, db: str | None = None, fs=None, cfg=None) -> dict | None:
    """Capture a lookahead-safe pre-entry label for one signal before paper routing.

    A valid EXISTING ``entry_path`` result is immutable: this is the only caller
    (the live paper-entry hook), so a prior real-time capture must never be
    recomputed. A ``scheduler_backfill``/``legacy_backfill`` row, however, is not
    immutable against this call: ``refresh()`` scans every recent signal
    (including ones still ``waiting_for_entry``) and may have pre-populated the
    row hours before the signal actually triggered. Since the underlying
    classification is a deterministic function of candles closed by
    ``created_at`` (see ``closed_candles``), recomputing here changes nothing
    about lookahead-safety — it only replaces a premature label with the
    genuine real-time one, matching the source the live-canary policy requires.
    """
    from src.config import load_config
    cfg = cfg or load_config()
    fs = fs or FileStore(cfg)
    path = db or str(cfg.db_path)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        ensure_tables(conn)
        sid = str(signal.get("signal_id") or "")
        if not sid:
            return None
        existing = conn.execute("SELECT * FROM signal_entry_mode_preentry WHERE signal_id=?", (sid,)).fetchone()
        if existing and str(existing["data_quality"] or "") == "ok" and str(existing["source"] or "") == "entry_path":
            return dict(existing)
        row = conn.execute(
            "SELECT signal_id, symbol, direction, mode, asset_class, exchange_focus, created_at, "
            "entry_low, entry_high, suggested_entry, COALESCE(invalidation, stop_loss) AS stop_used "
            "FROM proposed_signals WHERE signal_id=?", (sid,)).fetchone()
        if not row:
            return dict(existing) if existing else None
        rec = _classify_signal_row(row, fs=fs, cfg=cfg)
        out = _write_record(conn, row, rec, source="entry_path")
        conn.commit()
        return out
    finally:
        conn.close()


def refresh(*, db: str | None = None, limit: int = 1200) -> dict[str, Any]:
    """Classify pre-entry entry_mode for ALL recent registered signals. Reads only;
    writes ONLY signal_entry_mode_preentry."""
    from src.config import load_config
    from src.storage.file_store import FileStore
    cfg = load_config()
    fs = FileStore(cfg)
    path = db or str(cfg.db_path)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    ensure_tables(conn)
    rows = conn.execute(
        "SELECT signal_id, symbol, direction, mode, asset_class, exchange_focus, created_at, "
        "entry_low, entry_high, suggested_entry, COALESCE(invalidation, stop_loss) AS stop_used "
        "FROM proposed_signals ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    by_mode: dict[str, int] = {}
    dq_counts: dict[str, int] = {}
    for r in rows:
        existing = conn.execute("SELECT * FROM signal_entry_mode_preentry WHERE signal_id=?", (r["signal_id"],)).fetchone()
        if existing and str(existing["data_quality"] or "") == "ok":
            rec = dict(existing)
        else:
            rec = _classify_signal_row(r, fs=fs, cfg=cfg)
            _write_record(conn, r, rec, source="scheduler_backfill")
        by_mode[rec["entry_mode"]] = by_mode.get(rec["entry_mode"], 0) + 1
        dq_counts[rec["data_quality"]] = dq_counts.get(rec["data_quality"], 0) + 1
    conn.commit()
    conn.close()
    return {"processed": len(rows), "by_mode": by_mode, "data_quality": dq_counts}


def divergence(conn) -> dict[str, Any]:
    """Compare post-entry (signal_entry_mode) vs pre-entry (signal_entry_mode_preentry) for
    signals present in both. Returns agreement + a per-transition matrix (read-only)."""
    def _has(t):
        return bool(conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (t,)).fetchone())
    if not (_has("signal_entry_mode") and _has("signal_entry_mode_preentry")):
        return {"available": False}
    rows = conn.execute(
        "SELECT a.signal_id, a.entry_mode AS post, b.entry_mode AS pre "
        "FROM signal_entry_mode a JOIN signal_entry_mode_preentry b ON b.signal_id=a.signal_id").fetchall()
    total = len(rows)
    agree = sum(1 for r in rows if (r[1] or "") == (r[2] or ""))
    matrix: dict[str, int] = {}
    for r in rows:
        if (r[1] or "") != (r[2] or ""):
            matrix[f"{r[2]}->{r[1]}"] = matrix.get(f"{r[2]}->{r[1]}", 0) + 1
    return {"available": True, "common": total, "agree": agree,
            "agreement_rate": round(agree / total, 4) if total else None,
            "transitions": dict(sorted(matrix.items(), key=lambda kv: -kv[1]))}


__all__ = ["refresh", "ensure_for_signal", "ensure_tables", "classify_preentry_from_candles",
           "divergence", "closed_candles", "_tf_to_timedelta", "MIN_CANDLES_OK"]
