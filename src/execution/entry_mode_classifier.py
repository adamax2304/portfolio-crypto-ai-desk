"""PART 4 — Paper entry-mode classifier (paper-only, add-only).

The production technical-setup agent only ever builds a *pullback limit* band
(`close − 0.65..0.20·ATR` for longs) and, when price is > 2.5 ATR extended, converts
the idea to "watchlist — wait for pullback". That throws away breakout/momentum entries.

This module classifies, per signal, which entry mode the PAPER book should use given the
real chart structure + momentum, and persists a labelled record into `signal_entry_mode`:

  PULLBACK_LIMIT          — limit into a pullback band (the production default)
  STRUCTURAL_RETEST       — limit at a freshly-broken level being retested
  BREAKOUT_CONTINUATION   — stop/marketable entry on a break beyond near resistance/support
  MOMENTUM_TAKER_NOW      — strong, extended momentum; take now, no pullback expected
  LIMIT_THEN_TAKER_TIMEOUT— try the limit; if unfilled in N bars, take market
  NO_CHASE_SKIP           — too extended with no continuation structure; do not chase

Production entry generation (`proposed_signals.entry_*`) and `signal_outcomes` are NEVER
touched — this is an additive read-model overlay consumed by the paper lifecycle / UI.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

from src.config import load_config
from src.storage.file_store import FileStore
from src.analysis.market_structure_levels import structure_levels
from src.execution.signal_paper_tp import _candles_for, _f, _entry_triggered_signals

ENTRY_MODES = (
    "PULLBACK_LIMIT", "STRUCTURAL_RETEST", "BREAKOUT_CONTINUATION",
    "MOMENTUM_TAKER_NOW", "LIMIT_THEN_TAKER_TIMEOUT", "NO_CHASE_SKIP",
)

_DDL = """
CREATE TABLE IF NOT EXISTS signal_entry_mode (
  signal_id TEXT PRIMARY KEY, symbol TEXT, direction TEXT,
  entry_low REAL, entry_high REAL, ref_close REAL, atr REAL,
  extension_atr REAL, momentum_atr REAL,
  near_level REAL, near_level_kind TEXT, dist_to_level_atr REAL,
  entry_mode TEXT, entry_style TEXT, suggested_entry REAL,
  confidence REAL, candles_used INTEGER, reason TEXT, computed_at TEXT
);
"""


def ensure_table(conn: sqlite3.Connection) -> None:
    conn.execute(_DDL)
    conn.commit()


def _o(c, k, alt):  # candle field accessor (dict)
    return float(c.get(k, c.get(alt, 0)) or 0)


def _atr(cs: list, n: int = 14) -> float | None:
    if len(cs) < 2:
        return None
    trs = []
    for i in range(1, len(cs)):
        h, l = _o(cs[i], "high", "h"), _o(cs[i], "low", "l")
        pc = _o(cs[i - 1], "close", "c")
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    tail = trs[-n:]
    return sum(tail) / len(tail) if tail else None


def _sma(cs: list, n: int = 20) -> float | None:
    closes = [_o(c, "close", "c") for c in cs[-n:]]
    return sum(closes) / len(closes) if closes else None


def classify(*, entry_low, entry_high, direction, candles, atr_hint=None) -> dict:
    """Pure classifier. `candles` is a list of {open,high,low,close} dicts (chronological)."""
    long = str(direction).lower() != "short"
    reason: list[str] = []
    if not candles:
        return {"entry_mode": "PULLBACK_LIMIT", "entry_style": "limit",
                "suggested_entry": entry_low if long else entry_high,
                "confidence": 10.0, "ref_close": None, "atr": atr_hint,
                "extension_atr": None, "momentum_atr": None, "near_level": None,
                "near_level_kind": "none", "dist_to_level_atr": None, "candles_used": 0,
                "reason": "no candles → default pullback limit"}
    ref = _o(candles[-1], "close", "c")
    atr = _atr(candles) or atr_hint or 0.0
    sma = _sma(candles) or ref
    ext = abs(ref - sma) / atr if atr else 0.0                       # extension from mean
    look = candles[-11:-1] or candles[:-1]
    base = _o(look[0], "close", "c") if look else ref
    mom = ((ref - base) if long else (base - ref)) / atr if atr else 0.0  # signed momentum

    lv = structure_levels(candles, ref)
    # nearest level in the breakout direction (resistance for long, support for short)
    pool = lv.get("swing_highs" if long else "swing_lows", []) + (
        [lv.get("range_high")] if long else [lv.get("range_low")])
    ahead = [p for p in pool if p and (p > ref if long else p < ref)]
    behind = [p for p in pool if p and (p < ref if long else p > ref)]
    near = (min(ahead, key=lambda p: abs(p - ref)) if ahead else None)
    near_below = (max(behind, key=lambda p: abs(p - ref)) if behind else None)
    dist_lvl = abs(near - ref) / atr if (near and atr) else None
    recently_broken = (near_below is not None and atr and abs(ref - near_below) / atr <= 0.5)

    # ---- decision tree (mirrored for long/short) ----
    if near is not None and dist_lvl is not None and dist_lvl <= 0.5 and mom > 0.5:
        mode, style = "BREAKOUT_CONTINUATION", "stop"
        sug = near + (0.10 * atr if long else -0.10 * atr)
        reason.append(f"coiled {round(dist_lvl,2)}ATR under level with +{round(mom,2)}ATR momentum")
    elif recently_broken and mom > 0:
        mode, style = "STRUCTURAL_RETEST", "limit"
        sug = near_below
        reason.append("level just broke; limit the retest")
    elif ext > 2.5 and mom > 1.5:
        mode, style = "MOMENTUM_TAKER_NOW", "taker"
        sug = ref
        reason.append(f"{round(ext,1)}ATR extended with strong +{round(mom,2)}ATR momentum; no pullback")
    elif ext > 2.5:
        mode, style = "NO_CHASE_SKIP", "none"
        sug = None
        reason.append(f"{round(ext,1)}ATR extended, weak continuation → do not chase")
    else:
        # there is a clean pullback band beneath/above price → limit; else limit-then-taker
        band = entry_high if long else entry_low
        clean_pullback = band is not None and ((band < ref) if long else (band > ref))
        if clean_pullback:
            mode, style = "PULLBACK_LIMIT", "limit"
            sug = (entry_low if long else entry_high)
            reason.append("pullback room below price → limit the band")
        else:
            mode, style = "LIMIT_THEN_TAKER_TIMEOUT", "limit_then_taker"
            sug = (entry_low if long else entry_high)
            reason.append("no clean pullback; limit first, take market on timeout")

    conf = 75.0 if mode in ("BREAKOUT_CONTINUATION", "STRUCTURAL_RETEST", "PULLBACK_LIMIT") else 55.0
    return {"entry_mode": mode, "entry_style": style, "suggested_entry": sug,
            "confidence": conf, "ref_close": ref, "atr": atr,
            "extension_atr": round(ext, 3), "momentum_atr": round(mom, 3),
            "near_level": near, "near_level_kind": ("swing/range" if near else "none"),
            "dist_to_level_atr": round(dist_lvl, 3) if dist_lvl is not None else None,
            "candles_used": len(candles), "reason": "; ".join(reason)}


def compute_record(trade: dict, meta: dict, fs, cfg) -> dict:
    # look-ahead-safe: only candles at/at-or-before the signal's created_at may inform the
    # entry-mode label (mirrors signal_paper_tp / signal_stop_plan). Without this, a backfill
    # would classify entries using bars that printed AFTER the signal existed.
    candles = _candles_for(fs, cfg, trade.get("symbol"), meta.get("mode"),
                           trade.get("asset_class"), meta.get("exchange_focus"),
                           created_at=trade.get("created_at"))
    atr_hint = abs((trade.get("entry") or 0) - (trade.get("stop") or 0)) / 1.2 or None
    c = classify(entry_low=trade.get("entry_low"), entry_high=trade.get("entry_high"),
                 direction=trade.get("direction") or "long", candles=candles, atr_hint=atr_hint)
    return {
        "signal_id": trade.get("signal_id"), "symbol": trade.get("symbol"),
        "direction": trade.get("direction"),
        "entry_low": trade.get("entry_low"), "entry_high": trade.get("entry_high"),
        "ref_close": c["ref_close"], "atr": c["atr"],
        "extension_atr": c["extension_atr"], "momentum_atr": c["momentum_atr"],
        "near_level": c["near_level"], "near_level_kind": c["near_level_kind"],
        "dist_to_level_atr": c["dist_to_level_atr"],
        "entry_mode": c["entry_mode"], "entry_style": c["entry_style"],
        "suggested_entry": c["suggested_entry"], "confidence": c["confidence"],
        "candles_used": c["candles_used"], "reason": c["reason"],
        "computed_at": datetime.now(timezone.utc).isoformat(),
    }


def _upsert(conn: sqlite3.Connection, rec: dict) -> None:
    cols = list(rec.keys())
    conn.execute(
        f"INSERT OR REPLACE INTO signal_entry_mode ({','.join(cols)}) "
        f"VALUES ({','.join('?' * len(cols))})", [rec[c] for c in cols])


def refresh(limit: int = 800, db: str | None = None) -> dict:
    """Classify + persist entry modes for recent entry-triggered signals.
    Needs entry_low/entry_high, so it pulls those alongside the trade fields."""
    cfg = load_config()
    fs = FileStore(cfg)
    db = db or cfg.db_path
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    ensure_table(conn)
    conn.commit()
    trades = _entry_triggered_signals(
        conn, limit, refresh_table="signal_entry_mode"
    )
    # _entry_triggered_signals omits entry_low/high — backfill them for the band geometry
    band = {r["signal_id"]: dict(r) for r in conn.execute(
        "SELECT signal_id, entry_low, entry_high FROM proposed_signals")}
    by_mode: dict[str, int] = {}
    candles_hit = 0
    records: list[dict] = []
    for t in trades:
        b = band.get(t["signal_id"], {})
        t["entry_low"], t["entry_high"] = _f(b.get("entry_low")), _f(b.get("entry_high"))
        rec = compute_record(t, t.get("_meta", {}), fs, cfg)
        records.append(rec)
        by_mode[rec["entry_mode"]] = by_mode.get(rec["entry_mode"], 0) + 1
        if rec["candles_used"] > 0:
            candles_hit += 1
    # Candle loading/classification above can take minutes. It must not own
    # SQLite's single writer slot. Persist only after computation, in short
    # idempotent batches so Paper entry decisions can commit between them.
    for index, rec in enumerate(records, start=1):
        _upsert(conn, rec)
        if index % 50 == 0:
            conn.commit()
    conn.commit()
    conn.close()
    non_pullback = sum(v for k, v in by_mode.items() if k != "PULLBACK_LIMIT")
    return {"processed": len(trades), "by_mode": by_mode,
            "non_pullback": non_pullback, "candles_hit": candles_hit}


def get_entry_mode(signal_id: str, db: str | None = None) -> dict | None:
    cfg = load_config()
    conn = sqlite3.connect(db or cfg.db_path)
    conn.row_factory = sqlite3.Row
    try:
        ensure_table(conn)
        row = conn.execute(
            "SELECT * FROM signal_entry_mode WHERE signal_id=?", (signal_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()
