"""PART 5 — Multi-factor stock direction score (paper read-model, add-only).

Production `StockTechnicalAgent` sets direction from the EMA trend ALONE
(`_direction(self._trend(close, ema20, ema50))`). This module computes a fused, multi-factor
direction beside it — EMA trend + VWAP position + prior-day-high/low break + momentum +
relative strength vs SPY + (for MSTR) BTC-trend sensitivity — and persists a labelled record
into `stock_direction_score`:

  direction       long / short / neutral (fused)
  direction_score signed sum of weighted component votes
  dir_label       EMA_ONLY | MULTI_FACTOR_CONFIRMED | MULTI_FACTOR_CONFLICT | MULTI_FACTOR_WEAK
  agrees_with_production  did the fused call match the stored production direction?

Production direction (`proposed_signals.direction`) and `signal_outcomes` are NEVER touched —
this is an additive transparency overlay consumed by the paper lifecycle / UI.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

import pandas as pd

from src.config import load_config
from src.storage.file_store import FileStore
from src.indicators.technicals import ema, pct_return

# component weights (ema kept at the production weight; others additive)
_W = {"ema": 1.0, "vwap": 0.8, "pdhl": 1.0, "momentum": 0.6, "rs_spy": 1.0, "mstr_btc": 1.2}

_DDL = """
CREATE TABLE IF NOT EXISTS stock_direction_score (
  signal_id TEXT PRIMARY KEY, symbol TEXT, mode TEXT, production_direction TEXT,
  direction TEXT, direction_score REAL, dir_label TEXT,
  vote_ema INTEGER, vote_vwap INTEGER, vote_pdhl INTEGER, vote_momentum INTEGER,
  vote_rs_spy INTEGER, vote_mstr_btc INTEGER,
  factors_used INTEGER, agreement INTEGER, agrees_with_production INTEGER,
  rs_spy_20d REAL, vwap REAL, prev_day_high REAL, prev_day_low REAL,
  candles_used INTEGER, reason TEXT, computed_at TEXT,
  as_of_at TEXT, data_cutoff_at TEXT, is_point_in_time INTEGER DEFAULT 0,
  version TEXT
);
"""

_VERSION = "stock_direction_score_pit_v2"
_ADDITIVE_COLUMNS = (
    ("as_of_at", "TEXT"),
    ("data_cutoff_at", "TEXT"),
    ("is_point_in_time", "INTEGER DEFAULT 0"),
    ("version", "TEXT"),
)


def ensure_table(conn: sqlite3.Connection) -> None:
    conn.execute(_DDL)
    existing = {row[1] for row in conn.execute("PRAGMA table_info(stock_direction_score)")}
    for name, declaration in _ADDITIVE_COLUMNS:
        if name not in existing:
            conn.execute(f"ALTER TABLE stock_direction_score ADD COLUMN {name} {declaration}")
    conn.commit()


def _vwap(frame: pd.DataFrame) -> float | None:
    if frame is None or frame.empty or "volume" not in frame.columns:
        return None
    tp = (frame["high"] + frame["low"] + frame["close"]) / 3.0
    vol = frame["volume"].fillna(0)
    denom = float(vol.sum())
    return float((tp * vol).sum() / denom) if denom > 0 else None


def score_direction(*, close, ema20, ema50, vwap, prev_day_high, prev_day_low,
                    mom_ret, rs_spy, symbol, btc_trend) -> dict:
    """Pure scorer. Each factor casts a -1/0/+1 vote; weighted sum → direction."""
    votes: dict[str, int] = {}
    reason: list[str] = []
    # EMA trend (production factor)
    if ema20 is not None and ema50 is not None and close is not None:
        votes["ema"] = 1 if (close > ema20 and ema20 >= ema50) else (-1 if (close < ema20 and ema20 <= ema50) else 0)
    else:
        votes["ema"] = 0
    # VWAP position (intraday conviction)
    votes["vwap"] = 0 if (vwap is None or close is None) else (1 if close > vwap else -1)
    # prior-day high/low break
    if close is not None and prev_day_high is not None and prev_day_low is not None:
        votes["pdhl"] = 1 if close > prev_day_high else (-1 if close < prev_day_low else 0)
    else:
        votes["pdhl"] = 0
    # short-horizon momentum
    votes["momentum"] = 0 if mom_ret is None else (1 if mom_ret > 0 else (-1 if mom_ret < 0 else 0))
    # relative strength vs SPY
    votes["rs_spy"] = 0 if rs_spy is None else (1 if rs_spy > 0 else (-1 if rs_spy < 0 else 0))
    # MSTR ↔ BTC sensitivity (MSTR tracks BTC; let BTC trend tilt direction)
    if str(symbol).upper() == "MSTR" and btc_trend in (1, -1):
        votes["mstr_btc"] = btc_trend
        reason.append(f"MSTR·BTC trend {'up' if btc_trend > 0 else 'down'}")
    else:
        votes["mstr_btc"] = 0

    score = round(sum(_W[k] * v for k, v in votes.items()), 3)
    nonzero = [k for k, v in votes.items() if v != 0]
    pos = sum(1 for v in votes.values() if v > 0)
    neg = sum(1 for v in votes.values() if v < 0)
    agreement = max(pos, neg)
    direction = "long" if score >= 1.0 else ("short" if score <= -1.0 else "neutral")

    if nonzero == ["ema"] or (len(nonzero) == 1 and "ema" in nonzero):
        label = "EMA_ONLY"
    elif pos and neg:
        label = "MULTI_FACTOR_CONFLICT"
    elif agreement >= 3:
        label = "MULTI_FACTOR_CONFIRMED"
    else:
        label = "MULTI_FACTOR_WEAK"
    reason.append(f"{len(nonzero)} factors, {pos}↑/{neg}↓, score {score}")
    return {"direction": direction, "direction_score": score, "dir_label": label,
            "votes": votes, "factors_used": len(nonzero), "agreement": agreement,
            "reason": "; ".join(reason)}


def _parse_as_of(value) -> pd.Timestamp | None:
    try:
        parsed = pd.to_datetime(value, utc=True, errors="coerce")
    except Exception:
        return None
    return None if pd.isna(parsed) else pd.Timestamp(parsed)


def _closed_bars_as_of(
    frame: pd.DataFrame | None,
    as_of: pd.Timestamp | None,
    *,
    timeframe: str,
    daily: bool = False,
) -> pd.DataFrame:
    """Return only evidence that was closed before ``as_of``.

    Cached CSVs are mutable and normally contain bars newer than the signal.
    A research overlay must therefore slice them at the original decision time;
    otherwise a score recomputed weeks later silently sees the future.
    """
    if frame is None or frame.empty or as_of is None or "timestamp" not in frame.columns:
        return pd.DataFrame(columns=getattr(frame, "columns", None))
    out = frame.copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True, errors="coerce")
    out = out.dropna(subset=["timestamp"]).sort_values("timestamp")
    if daily:
        as_of_ny_date = as_of.tz_convert("America/New_York").date()
        bar_dates = out["timestamp"].dt.tz_convert("America/New_York").dt.date
        return out.loc[bar_dates < as_of_ny_date].reset_index(drop=True)
    unit = str(timeframe or "15m").lower().strip()
    try:
        if unit.endswith("m"):
            delta = pd.Timedelta(minutes=max(1, int(unit[:-1])))
        elif unit.endswith("h"):
            delta = pd.Timedelta(hours=max(1, int(unit[:-1])))
        else:
            delta = pd.Timedelta(minutes=15)
    except (TypeError, ValueError):
        delta = pd.Timedelta(minutes=15)
    return out.loc[out["timestamp"] + delta <= as_of].reset_index(drop=True)


def _btc_trend(conn: sqlite3.Connection, as_of=None) -> int:
    """+1/-1/0 from the latest dashboard snapshot available at ``as_of``."""
    try:
        point = _parse_as_of(as_of)
        if point is None:
            row = conn.execute(
                "SELECT crypto_regime FROM market_dashboard_snapshots "
                "ORDER BY id DESC LIMIT 1").fetchone()
        else:
            row = conn.execute(
                "SELECT crypto_regime FROM market_dashboard_snapshots "
                "WHERE COALESCE(timestamp,created_at) <= ? "
                "ORDER BY COALESCE(timestamp,created_at) DESC, id DESC LIMIT 1",
                (point.isoformat(),),
            ).fetchone()
        s = str((row[0] if row else "") or "").lower()
        if any(w in s for w in ("bull", "up", "risk_on", "risk on")):
            return 1
        if any(w in s for w in ("bear", "down", "risk_off", "risk off")):
            return -1
    except Exception:
        pass
    return 0


def compute_record(sig: dict, fs, cfg, btc_trend: int) -> dict:
    from src.signals.tracker import _load_stocks_ohlcv_for_signal
    symbol, mode = sig["symbol"], (sig.get("mode") or "intraday")
    as_of = _parse_as_of(sig.get("created_at"))
    exec_frame, _, exec_tf = _load_stocks_ohlcv_for_signal(fs, symbol, mode)
    exec_frame = _closed_bars_as_of(exec_frame, as_of, timeframe=exec_tf)
    day_frame = _closed_bars_as_of(
        fs.load_stocks_ohlcv(symbol, "1d"), as_of, timeframe="1d", daily=True)
    spy = _closed_bars_as_of(
        fs.load_stocks_ohlcv("SPY", "1d"), as_of, timeframe="1d", daily=True)

    close = ema20 = ema50 = vwap = pdh = pdl = mom = rs = None
    candles = 0
    if exec_frame is not None and not exec_frame.empty:
        candles = len(exec_frame)
        cl = exec_frame["close"]
        close = float(cl.iloc[-1])
        e20, e50 = ema(cl, 20), ema(cl, 50)
        ema20 = None if pd.isna(e20.iloc[-1]) else float(e20.iloc[-1])
        ema50 = None if pd.isna(e50.iloc[-1]) else float(e50.iloc[-1])
        if len(cl) > 6:
            mom = float((cl.iloc[-1] - cl.iloc[-6]) / cl.iloc[-6])
        if mode == "intraday":
            vwap = _vwap(exec_frame)
    if day_frame is not None and len(day_frame) >= 1:
        prev = day_frame.iloc[-1]
        pdh, pdl = float(prev["high"]), float(prev["low"])
    if day_frame is not None and spy is not None:
        r20 = pct_return(day_frame, 20)
        s20 = pct_return(spy, 20)
        if r20 is not None and s20 is not None:
            rs = round(r20 - s20, 4)

    sc = score_direction(close=close, ema20=ema20, ema50=ema50, vwap=vwap,
                         prev_day_high=pdh, prev_day_low=pdl, mom_ret=mom, rs_spy=rs,
                         symbol=symbol, btc_trend=btc_trend)
    v = sc["votes"]
    prod = (sig.get("direction") or "").lower()
    cutoff = None
    if exec_frame is not None and not exec_frame.empty:
        cutoff = pd.Timestamp(exec_frame["timestamp"].iloc[-1]).isoformat()
    return {
        "signal_id": sig["signal_id"], "symbol": symbol, "mode": mode,
        "production_direction": prod, "direction": sc["direction"],
        "direction_score": sc["direction_score"], "dir_label": sc["dir_label"],
        "vote_ema": v["ema"], "vote_vwap": v["vwap"], "vote_pdhl": v["pdhl"],
        "vote_momentum": v["momentum"], "vote_rs_spy": v["rs_spy"], "vote_mstr_btc": v["mstr_btc"],
        "factors_used": sc["factors_used"], "agreement": sc["agreement"],
        "agrees_with_production": 1 if (sc["direction"] != "neutral" and sc["direction"] == prod) else 0,
        "rs_spy_20d": rs, "vwap": vwap, "prev_day_high": pdh, "prev_day_low": pdl,
        "candles_used": candles, "reason": sc["reason"],
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "as_of_at": as_of.isoformat() if as_of is not None else None,
        "data_cutoff_at": cutoff,
        "is_point_in_time": 1 if as_of is not None else 0,
        "version": _VERSION,
    }


def _upsert(conn, rec):
    cols = list(rec.keys())
    conn.execute(
        f"INSERT OR REPLACE INTO stock_direction_score ({','.join(cols)}) "
        f"VALUES ({','.join('?' * len(cols))})", [rec[c] for c in cols])


def refresh(limit: int = 400, db: str | None = None) -> dict:
    cfg = load_config()
    fs = FileStore(cfg)
    conn = sqlite3.connect(db or cfg.db_path)
    conn.row_factory = sqlite3.Row
    ensure_table(conn)
    conn.commit()
    rows = conn.execute(
        "SELECT p.signal_id, p.symbol, p.direction, p.mode, p.created_at, p.asset_class "
        "FROM proposed_signals p "
        "LEFT JOIN stock_direction_score existing ON existing.signal_id=p.signal_id "
        "WHERE p.asset_class='stocks' AND p.created_at IS NOT NULL "
        "ORDER BY CASE WHEN existing.is_point_in_time=1 AND existing.version=? THEN 1 ELSE 0 END, "
        "p.created_at DESC, existing.computed_at ASC LIMIT ?", (_VERSION, limit,)).fetchall()
    by_label: dict[str, int] = {}
    non_ema = flips = 0
    records = []
    for r in rows:
        signal = dict(r)
        rec = compute_record(signal, fs, cfg, _btc_trend(conn, signal.get("created_at")))
        records.append(rec)
        by_label[rec["dir_label"]] = by_label.get(rec["dir_label"], 0) + 1
        if rec["dir_label"] != "EMA_ONLY":
            non_ema += 1
        if rec["direction"] != "neutral" and rec["direction"] != rec["production_direction"]:
            flips += 1
    for index, rec in enumerate(records, start=1):
        _upsert(conn, rec)
        if index % 50 == 0:
            conn.commit()
    conn.commit()
    conn.close()
    return {"processed": len(rows), "by_label": by_label,
            "multi_factor": non_ema, "would_flip_vs_production": flips,
            "point_in_time": sum(int(r.get("is_point_in_time") or 0) for r in records),
            "version": _VERSION}


def get_direction(signal_id: str, db: str | None = None) -> dict | None:
    cfg = load_config()
    conn = sqlite3.connect(db or cfg.db_path)
    conn.row_factory = sqlite3.Row
    try:
        ensure_table(conn)
        row = conn.execute(
            "SELECT * FROM stock_direction_score WHERE signal_id=?", (signal_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()
