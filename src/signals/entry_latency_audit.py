"""PART 6 — Entry-latency root-cause classifier (read-only diagnostic, add-only).

The "MSTR 184-min late entry" was NOT a monitor/fill bug: the 15m OHLCV had no bars
between signal creation and the recorded entry — the first *available* bar was already
in the entry band, so the tracker recorded entry at the earliest data it could see. The
true lateness is a **data-coverage gap** (yfinance intraday delay + shallow rolling window
dropping early-session bars), distinct from a genuine detection-latency miss.

For each entry-triggered signal this computes, from the real OHLCV the tracker uses:
  recorded_latency_min  entry_triggered_at − created_at
  data_gap_min          first available bar after creation − created_at
  cause ∈ DATA_GAP_LATE | SESSION_GAP | DETECTION_LATENCY | LEGITIMATE_LATE | FAST | NO_DATA

DETECTION_LATENCY means a fillable in-band bar existed *strictly before* the recorded entry
(a real miss). DATA_GAP_LATE means the first bar we have is already past creation (coverage,
not logic). Read-only: never touches signal_outcomes / final_r / production logic.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

import pandas as pd

from src.config import load_config
from src.storage.file_store import FileStore

_FAST_MIN = 30        # ≤ this recorded latency → FAST (not late)
_GAP_MIN = 30         # data gap beyond this → coverage-limited for intraday
_MODE_GAP_MIN = {"swing": 2 * 24 * 60, "position": 3 * 24 * 60, "invest": 7 * 24 * 60}

_DDL = """
CREATE TABLE IF NOT EXISTS entry_latency_audit (
  signal_id TEXT PRIMARY KEY, symbol TEXT, asset_class TEXT, mode TEXT,
  created_at TEXT, entry_triggered_at TEXT,
  recorded_latency_min REAL, data_gap_min REAL,
  first_bar_after_creation TEXT, first_in_band_bar TEXT,
  in_band_before_recorded INTEGER, cause TEXT, reason TEXT, computed_at TEXT,
  snapshot_kind TEXT, latency_truth TEXT, observation_delay_min REAL
);
"""


def ensure_table(conn):
    conn.execute(_DDL)
    cols = {r[1] for r in conn.execute("PRAGMA table_info(entry_latency_audit)")}
    if "snapshot_kind" not in cols:
        conn.execute("ALTER TABLE entry_latency_audit ADD COLUMN snapshot_kind TEXT")
        conn.execute("UPDATE entry_latency_audit SET snapshot_kind='backfill_refresh' WHERE snapshot_kind IS NULL")
    if "latency_truth" not in cols:
        conn.execute("ALTER TABLE entry_latency_audit ADD COLUMN latency_truth TEXT")
        conn.execute(
            "UPDATE entry_latency_audit SET latency_truth=CASE "
            "WHEN snapshot_kind='backfill_refresh' THEN 'historical_reconstruction' "
            "WHEN snapshot_kind='entry_transition' THEN 'legacy_unclassified' "
            "ELSE 'legacy_unclassified' END WHERE latency_truth IS NULL"
        )
    # A database may have been migrated by an earlier build which could not
    # distinguish a frozen transition from a later refresh. Repair only the
    # add-only diagnostic label; no signal/outcome/PnL data is touched.
    conn.execute(
        "UPDATE entry_latency_audit SET latency_truth='historical_reconstruction' "
        "WHERE snapshot_kind='backfill_refresh' AND latency_truth='legacy_unclassified'"
    )
    if "observation_delay_min" not in cols:
        conn.execute("ALTER TABLE entry_latency_audit ADD COLUMN observation_delay_min REAL")
    conn.commit()


def _mins(a, b):
    try:
        return round((pd.to_datetime(a) - pd.to_datetime(b)).total_seconds() / 60.0, 1)
    except Exception:
        return None


def _bar_interval_min(df) -> float | None:
    try:
        ts = pd.to_datetime(df["timestamp"], utc=True).sort_values().drop_duplicates()
        diffs = ts.diff().dropna().dt.total_seconds().div(60.0)
        diffs = diffs[diffs > 0]
        return float(diffs.median()) if not diffs.empty else None
    except Exception:
        return None


def classify(*, created_at, entry_triggered_at, entry_low, entry_high, candles_df,
             mode: str | None = None, asset_class: str | None = None,
             latency_truth: str | None = None):
    """Pure-ish classifier given the tracker's OHLCV frame. Returns a dict."""
    rec_lat = _mins(entry_triggered_at, created_at)
    out = {"recorded_latency_min": rec_lat, "data_gap_min": None,
           "first_bar_after_creation": None, "first_in_band_bar": None,
           "in_band_before_recorded": 0, "cause": "FAST", "reason": ""}
    if candles_df is None or candles_df.empty or "timestamp" not in candles_df.columns:
        if latency_truth == "point_in_time" and rec_lat is not None and rec_lat <= _FAST_MIN:
            out["cause"] = "FAST_POINT_IN_TIME_REVALIDATED"
            out["reason"] = (
                "entry was current-price revalidated at the transition; "
                "rolling OHLCV unavailable for diagnostic reconstruction"
            )
            return out
        out["cause"] = "NO_DATA"
        out["reason"] = "no OHLCV available for the signal"
        return out
    df = candles_df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    bar_min = _bar_interval_min(df)
    created = pd.to_datetime(created_at, utc=True)
    rec = pd.to_datetime(entry_triggered_at, utc=True)
    after = df[df["timestamp"] >= created]
    if after.empty:
        if latency_truth == "point_in_time" and rec_lat is not None and rec_lat <= _FAST_MIN:
            out["cause"] = "FAST_POINT_IN_TIME_REVALIDATED"
            out["reason"] = (
                "entry was current-price revalidated at the transition; "
                "rolling OHLCV has no bar at/after signal creation"
            )
            return out
        out["cause"] = "NO_DATA"
        out["reason"] = "no bars at/after creation in the rolling window"
        return out
    first_bar = after.iloc[0]["timestamp"]
    out["first_bar_after_creation"] = str(first_bar)
    out["data_gap_min"] = _mins(first_bar, created)
    lo, hi = min(entry_low, entry_high), max(entry_low, entry_high)
    in_band = after[(after["low"] <= hi) & (after["high"] >= lo)]
    if not in_band.empty:
        fib = in_band.iloc[0]["timestamp"]
        out["first_in_band_bar"] = str(fib)
        # was there a fillable in-band bar strictly before the recorded entry?
        before = in_band[in_band["timestamp"] < (rec - pd.Timedelta(minutes=1))]
        out["in_band_before_recorded"] = int(not before.empty)

    # An intraday stock idea created outside RTH is planning data, not a missing-feed incident.
    # Keep it excluded from edge, but do not let the inevitable next-open bar poison DGL health.
    if str(asset_class or "").lower().startswith("stock") and str(mode or "").lower() == "intraday":
        try:
            from src.stocks.market_calendar import is_us_cash_session_open, us_session_label
            if not is_us_cash_session_open(created.to_pydatetime()):
                out["cause"] = "SESSION_GAP"
                out["reason"] = ("stock intraday idea created outside RTH "
                                 f"({us_session_label(created.to_pydatetime())}); planning-only")
                return out
        except Exception:
            pass

    ac = str(asset_class or "").lower()
    md = str(mode or "").lower()
    if ac.startswith("stock"):
        gap_limit = _MODE_GAP_MIN.get(md, _GAP_MIN)
    else:
        # A normal next 1h/4h bar is not a feed gap. Permit one bar plus a
        # bounded scheduling margin, while retaining the 30m floor for 5m/15m.
        gap_limit = max(_GAP_MIN, (bar_min or 0.0) * 1.25)
    impossible_backfill_gap = (
        rec_lat is not None and out["data_gap_min"] is not None and
        out["data_gap_min"] > rec_lat + max(1.0, (bar_min or 0.0) * 0.25) and
        out["data_gap_min"] > gap_limit
    )

    if impossible_backfill_gap:
        out["cause"] = "DATA_GAP_LATE"
        out["reason"] = (f"first archived bar is {out['data_gap_min']}min after creation, "
                         f"later than the recorded {rec_lat}min entry; rolling-cache backfill gap")
    elif rec_lat is not None and rec_lat <= _FAST_MIN:
        out["cause"], out["reason"] = "FAST", f"entered {rec_lat}min after creation"
    elif out["in_band_before_recorded"]:
        out["cause"] = "DETECTION_LATENCY"
        out["reason"] = ("price was inside the entry band before the recorded fill — "
                         "a genuine detection miss")
    elif _mode_gap_is_expected(created_at, out["data_gap_min"], mode=mode, asset_class=asset_class):
        out["cause"] = "LEGITIMATE_LATE"
        out["reason"] = ("session/next-bar gap is expected for the stock "
                          f"{str(mode or 'higher-horizon')} mode; no bar was missing in-session")
    elif (out["data_gap_min"] or 0) > gap_limit:
        out["cause"] = "DATA_GAP_LATE"
        out["reason"] = (f"first available bar is {out['data_gap_min']}min after creation "
                         "(mode-aware coverage gap) — not a fill bug")
    else:
        out["cause"] = "LEGITIMATE_LATE"
        out["reason"] = "continuous data; price only reached the band at the recorded time"
    # Historical candle walks can establish coverage quality but cannot prove
    # the worker actually observed a fill then. Do not label reconstructed
    # rows FAST/DETECTION_LATENCY; preserve only genuine data/session failures.
    if latency_truth == "historical_reconstruction" and out["cause"] not in {
        "DATA_GAP_LATE", "SESSION_GAP", "NO_DATA",
    }:
        out["cause"] = "HISTORICAL_RECONSTRUCTION"
        out["reason"] = "historical candle reconstruction; not valid system-latency evidence"
    return out


def _mode_gap_is_expected(created_at, gap_min, *, mode, asset_class) -> bool:
    """Return True only for a normal off-session/next-bar gap in a higher-horizon stock mode."""
    ac = str(asset_class or "").lower()
    md = str(mode or "").lower()
    if not ac.startswith("stock") or md == "intraday" or gap_min is None:
        return False
    try:
        from src.stocks.market_calendar import is_us_cash_session_open
        from datetime import datetime, timezone
        raw = str(created_at).replace("Z", "+00:00")
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        if not is_us_cash_session_open(dt):
            return gap_min <= _MODE_GAP_MIN.get(md, 2 * 24 * 60)
    except Exception:
        return False
    return False


def _load(fs, cfg, symbol, mode, asset_class, exchange_focus=""):
    try:
        if str(asset_class or "").lower().startswith("stock"):
            from src.signals.tracker import _load_stocks_ohlcv_for_signal
            df, _, _ = _load_stocks_ohlcv_for_signal(fs, symbol, mode or "intraday")
        else:
            from src.signals.tracker import _load_ohlcv_for_signal
            df, _, _ = _load_ohlcv_for_signal(fs, cfg, symbol, mode or "intraday", exchange_focus or "")
        return df
    except Exception:
        return None


def capture_entry_snapshot(*, signal: dict, outcome_row, file_store=None, project_config=None,
                           db: str | None = None) -> bool:
    """Freeze latency diagnostics at the real waiting->triggered transition.

    A rolling cache can no longer rewrite a historical signal as a multi-day
    data gap.  A later refresh may backfill legacy rows, but never overwrites an
    ``entry_transition`` snapshot.
    """
    entry_at = getattr(outcome_row, "entry_triggered_at", None)
    if entry_at is None and isinstance(outcome_row, dict):
        entry_at = outcome_row.get("entry_triggered_at")
    if not entry_at or signal.get("entry_low") is None or signal.get("entry_high") is None:
        return False
    cfg = project_config or load_config()
    fs = file_store or FileStore(cfg)
    path = db or str(cfg.db_path)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        ensure_table(conn)
        sid = str(signal.get("signal_id") or "")
        if not sid:
            return False
        prior = conn.execute("SELECT snapshot_kind FROM entry_latency_audit WHERE signal_id=?", (sid,)).fetchone()
        if prior and prior["snapshot_kind"] == "entry_transition":
            return False
        df = _load(fs, cfg, signal.get("symbol"), signal.get("mode"), signal.get("asset_class"),
                   signal.get("exchange_focus") or "")
        basis = getattr(outcome_row, "_entry_time_basis", None)
        revalidated = getattr(outcome_row, "_entry_currently_executable", None)
        if isinstance(outcome_row, dict):
            basis = outcome_row.get("entry_time_basis", basis)
            revalidated = outcome_row.get("current_price_revalidated", revalidated)
        latency_truth = (
            "point_in_time" if basis == "point_in_time_current_bar" and bool(revalidated)
            else "historical_reconstruction"
        )
        computed_at = datetime.now(timezone.utc).isoformat()
        c = classify(created_at=signal.get("created_at"), entry_triggered_at=entry_at,
                     entry_low=signal.get("entry_low"), entry_high=signal.get("entry_high"), candles_df=df,
                     mode=signal.get("mode"), asset_class=signal.get("asset_class"),
                     latency_truth=latency_truth)
        rec = {"signal_id": sid, "symbol": signal.get("symbol"), "asset_class": signal.get("asset_class"),
               "mode": signal.get("mode"), "created_at": signal.get("created_at"),
               "entry_triggered_at": entry_at, **c,
               "computed_at": computed_at, "snapshot_kind": "entry_transition",
               "latency_truth": latency_truth,
               "observation_delay_min": _mins(computed_at, entry_at)}
        cols = list(rec)
        conn.execute("INSERT OR REPLACE INTO entry_latency_audit (" + ",".join(cols) + ") VALUES ("
                     + ",".join("?" * len(cols)) + ")", tuple(rec[k] for k in cols))
        conn.commit()
        return True
    finally:
        conn.close()


def refresh(limit: int = 400, asset_class: str | None = "stocks", db: str | None = None) -> dict:
    cfg = load_config()
    fs = FileStore(cfg)
    conn = sqlite3.connect(db or cfg.db_path)
    conn.row_factory = sqlite3.Row
    ensure_table(conn)
    where = "AND p.asset_class=?" if asset_class else ""
    params = ([asset_class, limit] if asset_class else [limit])
    rows = conn.execute(
        "SELECT p.signal_id, p.symbol, p.asset_class, p.mode, p.created_at, "
        "p.entry_low, p.entry_high, o.entry_triggered_at "
        "FROM proposed_signals p "
        "JOIN signal_outcomes o ON o.id=("
        "  SELECT so.id FROM signal_outcomes so WHERE so.signal_id=p.signal_id "
        "  ORDER BY so.id DESC LIMIT 1"
        ") "
        "LEFT JOIN entry_latency_audit existing ON existing.signal_id=p.signal_id "
        f"WHERE o.entry_triggered=1 AND o.entry_triggered_at IS NOT NULL {where} "
        "AND COALESCE(existing.snapshot_kind,'') != 'entry_transition' "
        "ORDER BY CASE WHEN existing.computed_at IS NULL THEN 0 ELSE 1 END, "
        "existing.computed_at ASC, o.entry_triggered_at DESC LIMIT ?", params).fetchall()
    by_cause: dict[str, int] = {}
    frozen_skipped = 0
    now = datetime.now(timezone.utc).isoformat()
    records: list[dict] = []
    for r in rows:
        d = dict(r)
        if d["entry_low"] is None or d["entry_high"] is None:
            continue
        frozen = conn.execute("SELECT snapshot_kind FROM entry_latency_audit WHERE signal_id=?",
                              (d["signal_id"],)).fetchone()
        if frozen and frozen[0] == "entry_transition":
            frozen_skipped += 1
            continue
        df = _load(fs, cfg, d["symbol"], d["mode"], d["asset_class"])
        c = classify(created_at=d["created_at"], entry_triggered_at=d["entry_triggered_at"],
                     entry_low=d["entry_low"], entry_high=d["entry_high"], candles_df=df,
                     mode=d.get("mode"), asset_class=d.get("asset_class"),
                     latency_truth="historical_reconstruction")
        rec = {"signal_id": d["signal_id"], "symbol": d["symbol"], "asset_class": d["asset_class"],
               "mode": d["mode"], "created_at": d["created_at"],
               "entry_triggered_at": d["entry_triggered_at"], **c, "computed_at": now,
               "snapshot_kind": "backfill_refresh", "latency_truth": "historical_reconstruction",
               "observation_delay_min": _mins(now, d["entry_triggered_at"])}
        records.append(rec)
        by_cause[c["cause"]] = by_cause.get(c["cause"], 0) + 1
    for index, rec in enumerate(records, start=1):
        cols = list(rec.keys())
        conn.execute(f"INSERT OR REPLACE INTO entry_latency_audit ({','.join(cols)}) "
                     f"VALUES ({','.join('?' * len(cols))})", [rec[x] for x in cols])
        if index % 50 == 0:
            conn.commit()
    conn.commit()
    conn.close()
    return {"processed": len(rows) - frozen_skipped, "frozen_skipped": frozen_skipped,
            "by_cause": by_cause}


def get_latency(signal_id: str, db: str | None = None) -> dict | None:
    cfg = load_config()
    conn = sqlite3.connect(db or cfg.db_path)
    conn.row_factory = sqlite3.Row
    try:
        ensure_table(conn)
        row = conn.execute(
            "SELECT * FROM entry_latency_audit WHERE signal_id=?", (signal_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()
