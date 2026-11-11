"""Stock OHLCV coverage gate + prewarm/backfill + source fallback (S2 / S5 / S6).

Extends the 15m-only intraday coverage model to every stock mode/timeframe, archives OHLCV locally
so yfinance rolling-window/delay stops manufacturing false late entries, and runs a fallback chain
(primary intraday → coarser daily/weekly → cached local archive). If a source is stale/partial the
data is marked NOT CLEAN — never silently used, never counted as edge.

READ-MODEL / DATA-QUALITY only. Writes: the `stock_coverage_by_mode` read-model table + local OHLCV
archive CSVs (data/raw/stocks/...). Never touches proposed_signals / signal_outcomes / final_r / live.

Итоговое правило this enforces: do not conclude stocks B / position is good/bad until coverage is
clean AND the clean forward sample is sufficient.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Any

import pandas as pd

from src.config import load_config
from src.storage.file_store import FileStore
from src.stocks.market_calendar import latest_us_cash_session

# Expected coverage per mode: ordered timeframe preference (finest first) + clean-data thresholds.
# intraday needs dense RTH 15m; swing/position/invest live on daily(+weekly) — a daily gap is far
# less likely than the intraday coverage holes that break the shadow lane.
MODE_COVERAGE: dict[str, dict] = {
    "intraday": {"timeframes": ["15m", "5m", "1m"], "min_bars": 13, "max_first_gap_min": 60},
    "swing":    {"timeframes": ["1d", "1h"], "min_bars": 20, "max_first_gap_min": 2 * 1440},
    "position": {"timeframes": ["1d", "1wk"], "min_bars": 30, "max_first_gap_min": 3 * 1440},
    "invest":   {"timeframes": ["1d", "1wk"], "min_bars": 30, "max_first_gap_min": 7 * 1440},
}
_INTRADAY_MINUTES = {"1m": 1, "5m": 5, "15m": 15, "30m": 30, "1h": 60}

_DDL = """
CREATE TABLE IF NOT EXISTS stock_coverage_by_mode (
  symbol TEXT, mode TEXT, timeframe TEXT, status TEXT, is_clean INTEGER, bars INTEGER,
  first_bar TEXT, last_bar TEXT, first_bar_gap_min REAL, missing_bars INTEGER, source TEXT,
  computed_at TEXT, PRIMARY KEY (symbol, mode)
);
"""


def _norm(df) -> pd.DataFrame | None:
    if df is None or getattr(df, "empty", True):
        return None
    d = df.copy()
    if "timestamp" not in d.columns:
        d = d.reset_index()
        for cand in ("Date", "Datetime", "index", "Unnamed: 0"):
            if cand in d.columns:
                d = d.rename(columns={cand: "timestamp"})
                break
    d = d.rename(columns={c: str(c).lower() for c in d.columns})
    if "timestamp" not in d.columns:
        return None
    d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
    d = d.dropna(subset=["timestamp"]).sort_values("timestamp")
    return d if not d.empty else None


def classify_series(df, timeframe: str, mode: str, *, now: datetime | None = None) -> dict:
    """Coverage status + is_clean for one (symbol,timeframe) series under a mode's thresholds."""
    thr = MODE_COVERAGE.get(mode, MODE_COVERAGE["intraday"])
    d = _norm(df)
    if d is None:
        return {"status": "NO_DATA", "is_clean": False, "bars": 0, "first_bar": None,
                "last_bar": None, "first_bar_gap_min": None, "missing_bars": None}
    now = now or datetime.now(timezone.utc)
    bars = len(d)
    first_bar, last_bar = d["timestamp"].iloc[0], d["timestamp"].iloc[-1]
    gap_min = None
    if timeframe in _INTRADAY_MINUTES and mode == "intraday":
        session_open, session_close, session_complete = latest_us_cash_session(now)
        interval_min = _INTRADAY_MINUTES[timeframe]
        session = d[(d["timestamp"] >= session_open) & (d["timestamp"] < session_close)]
        if session.empty:
            return {"status": "NO_SESSION_DATA", "is_clean": False, "bars": bars,
                    "first_bar": first_bar.isoformat(), "last_bar": last_bar.isoformat(),
                    "first_bar_gap_min": None, "missing_bars": None}
        fb = session["timestamp"].iloc[0].to_pydatetime()
        gap_min = max(0.0, (fb - session_open).total_seconds() / 60.0)
        expected_until = session_close if session_complete else min(now, session_close)
        expected_count = max(
            0, int((expected_until - session_open).total_seconds() // (60 * interval_min))
        )
        if expected_count == 0:
            return {"status": "SESSION_WARMUP", "is_clean": False, "bars": bars,
                    "first_bar": first_bar.isoformat(), "last_bar": last_bar.isoformat(),
                    "first_bar_gap_min": round(gap_min, 1), "missing_bars": 0}
        observed = {
            int((ts.to_pydatetime() - session_open).total_seconds() // 60)
            for ts in session["timestamp"] if ts.to_pydatetime() >= session_open
        }
        expected = {i * interval_min for i in range(expected_count)}
        session_missing = len(expected - observed)
        clean = (
            bars >= int(thr.get("min_bars", 13))
            and gap_min <= float(thr.get("max_first_gap_min", 60))
            and session_missing == 0
        )
        if gap_min > float(thr.get("max_first_gap_min", 60)):
            status = "DATA_GAP_LATE"
        elif session_missing:
            status = "PARTIAL_DATA"
        else:
            status = "DATA_OK_CLOSED_SESSION" if session_complete else "DATA_OK"
        return {"status": status, "is_clean": bool(clean), "bars": bars,
                "first_bar": first_bar.isoformat(), "last_bar": last_bar.isoformat(),
                "first_bar_gap_min": round(gap_min, 1),
                "missing_bars": max(session_missing, int(thr.get("min_bars", 13)) - bars, 0)}

    # Higher-horizon staleness stays wall-clock based; intraday is handled against a concrete RTH
    # interval grid above, including weekends, holidays and daylight saving time.
    stale_min = (now - last_bar.to_pydatetime()).total_seconds() / 60.0
    stale_cap = {"1m": 30, "5m": 60, "15m": 120, "1h": 240, "1d": 3 * 1440, "1wk": 10 * 1440}.get(timeframe, 1440)
    status, clean = "DATA_OK", True
    if bars < int(thr.get("min_bars", 13)):
        status, clean = "PARTIAL_DATA", False
    if gap_min is not None and gap_min > float(thr.get("max_first_gap_min", 60)):
        status, clean = "DATA_GAP_LATE", False
    if stale_min > stale_cap:
        status, clean = ("STALE" if status == "DATA_OK" else status), False
    missing = max(0, int(thr.get("min_bars", 13)) - bars)
    return {"status": status, "is_clean": bool(clean), "bars": bars,
            "first_bar": first_bar.isoformat(), "last_bar": last_bar.isoformat(),
            "first_bar_gap_min": (round(gap_min, 1) if gap_min is not None else None),
            "missing_bars": missing}


def _fetch_with_fallback(symbol: str, mode: str, fs: FileStore, *, archive: bool,
                         fetch: bool = True, now=None) -> dict:
    """Fallback chain: finest tf → coarser → cached archive. Returns the FIRST clean series; if none
    is clean, returns the least-bad with is_clean=False (never silently promoted). fetch=False =
    cache-only (no network) — used for the cheap per-cycle re-classification."""
    from src.stocks.data_collectors import yf_client
    tfs = MODE_COVERAGE.get(mode, MODE_COVERAGE["intraday"])["timeframes"]
    best = None
    for tf in tfs:
        df, source = None, None
        if fetch:
            try:
                result = yf_client.fetch_ohlcv(symbol, tf)
                df = result.dataframe if result is not None else None
                source = result.source if result is not None else None
            except Exception:
                df = None
        if _norm(df) is None:                               # fallback: cached local archive
            df = fs.load_stocks_ohlcv(symbol, tf)
            source = "archive_cache" if _norm(df) is not None else None
        cls = classify_series(df, tf, mode, now=now)
        cls.update({"timeframe": tf, "source": source or "none"})
        if (
            archive
            and _norm(df) is not None
            and source not in {None, "none", "archive_cache"}
        ):
            try:
                path = fs.stocks_ohlcv_path(symbol, tf)
                path.parent.mkdir(parents=True, exist_ok=True)
                _norm(df).to_csv(path, index=False)         # local archive so delay ≠ false late entry
            except Exception:
                pass
        if best is None or (cls["is_clean"] and not best["is_clean"]):
            best = cls
        if cls["is_clean"]:
            break
    return best or {"status": "NO_DATA", "is_clean": False, "bars": 0, "timeframe": tfs[0],
                    "first_bar": None, "last_bar": None, "first_bar_gap_min": None,
                    "missing_bars": None, "source": "none"}


def _has(conn, t) -> bool:
    return bool(conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (t,)).fetchone())


def mark_outcome_coverage(db: str | None = None) -> dict[str, Any]:
    """Populate the per-outcome coverage columns on paper_shadow_execution_outcomes for STOCK rows,
    joining entry_latency_audit (per-signal DGL) + stock_coverage_by_mode (per symbol/mode). Sets
    is_clean_for_edge=0 for any DATA_GAP_LATE or non-clean-coverage row. PAPER read-model write to
    the shadow outcomes table only — never proposed_signals / signal_outcomes / final_r / live."""
    from src.execution.paper_shadow_engine import ensure_tables
    cfg = load_config()
    path = db or str(cfg.db_path)
    conn = sqlite3.connect(path)
    try:
        ensure_tables(conn)                              # idempotent: guarantees coverage columns exist
        if not _has(conn, "paper_shadow_execution_outcomes"):
            return {"updated": 0}
        lat = {}
        if _has(conn, "entry_latency_audit"):
            for r in conn.execute("SELECT signal_id, cause, data_gap_min, first_bar_after_creation "
                                  "FROM entry_latency_audit"):
                lat[r[0]] = r
        cov = {}
        if _has(conn, "stock_coverage_by_mode"):
            for r in conn.execute("SELECT symbol, mode, status, is_clean, timeframe, missing_bars "
                                  "FROM stock_coverage_by_mode"):
                cov[(r[0], r[1])] = r
        rows = conn.execute(
            "SELECT DISTINCT e.signal_id, e.symbol, p.mode FROM paper_shadow_execution_outcomes e "
            "JOIN proposed_signals p ON p.signal_id = e.signal_id "
            "WHERE lower(COALESCE(e.asset_class, p.asset_class)) LIKE 'stock%'").fetchall()
        updated = 0
        for sid, sym, mode in rows:
            la = lat.get(sid)
            cause = (la[1] if la else None)
            gap_min = (la[2] if la else None)
            first_bar = (la[3] if la else None)
            cv = cov.get((sym, mode))
            if cv is None:
                # CONSERVATIVE: no coverage row for (symbol, mode) → we cannot vouch for the data,
                # so it is NOT clean and never counts as edge (don't silently trust unverified data).
                cov_status, cov_clean, tf, missing = "NO_COVERAGE_ROW", False, None, None
            else:
                cov_status, cov_clean, tf, missing = cv[2], bool(cv[3]), cv[4], cv[5]
            # A filled shadow row must have a frozen latency classification as
            # well as a clean symbol/timeframe coverage row.  Missing latency
            # evidence is not permission to count the fill as edge.
            latency_clean = bool(la) and cause not in ("DATA_GAP_LATE", "NO_DATA", "SESSION_GAP")
            is_clean = 1 if (latency_clean and cov_clean) else 0
            conn.execute(
                "UPDATE paper_shadow_execution_outcomes SET data_coverage_status=?, coverage_timeframe=?, "
                "first_bar_after_signal=?, missing_bars_count=?, coverage_gap_minutes=?, is_clean_for_edge=? "
                "WHERE signal_id=?", (cov_status, tf, first_bar, missing, gap_min, is_clean, sid))
            updated += 1
            if updated % 50 == 0:
                conn.commit()
        conn.commit()
        return {"updated": updated}
    finally:
        conn.close()


def refresh(*, symbols: list[str] | None = None, modes: list[str] | None = None,
            prewarm: bool = True, mark_outcomes: bool = True,
            db: str | None = None, now_iso: str | None = None) -> dict[str, Any]:
    """Compute coverage per (symbol, mode) with the fallback chain; optionally prewarm/archive.
    Writes ONLY stock_coverage_by_mode + local OHLCV archive. Read-only on all signal/live tables."""
    cfg = load_config()
    fs = FileStore(cfg)
    path = db or str(cfg.db_path)
    now = datetime.fromisoformat(now_iso) if now_iso else datetime.now(timezone.utc)
    modes = modes or ["intraday", "swing", "position", "invest"]
    if symbols is None:
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        try:
            symbols = [r[0] for r in conn.execute(
                "SELECT DISTINCT symbol FROM proposed_signals WHERE asset_class='stocks' "
                "AND symbol IS NOT NULL").fetchall()]
        finally:
            conn.close()
    rows: list[dict] = []
    for sym in symbols:
        for mode in modes:
            # prewarm=True → fetch from provider + archive; prewarm=False → cache-only (no network)
            cov = _fetch_with_fallback(sym, mode, fs, archive=prewarm, fetch=prewarm, now=now)
            rows.append({"symbol": sym, "mode": mode, **cov})
    generated_at = now.isoformat()
    wconn = sqlite3.connect(path)
    try:
        wconn.execute(_DDL)
        wconn.execute("DELETE FROM stock_coverage_by_mode")
        for r in rows:
            wconn.execute("INSERT OR REPLACE INTO stock_coverage_by_mode VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                          (r["symbol"], r["mode"], r.get("timeframe"), r["status"], int(r["is_clean"]),
                           r.get("bars"), r.get("first_bar"), r.get("last_bar"),
                           r.get("first_bar_gap_min"), r.get("missing_bars"), r.get("source"), generated_at))
        wconn.commit()
    finally:
        wconn.close()
    clean = sum(1 for r in rows if r["is_clean"])
    marked = mark_outcome_coverage(db=path) if mark_outcomes else {"updated": 0}
    return {"generated_at": generated_at, "symbols": len(symbols), "series": len(rows),
            "clean": clean, "dirty": len(rows) - clean, "prewarmed": bool(prewarm),
            "outcomes_marked": marked.get("updated", 0), "rows": rows}


__all__ = ["classify_series", "refresh", "mark_outcome_coverage", "MODE_COVERAGE"]
