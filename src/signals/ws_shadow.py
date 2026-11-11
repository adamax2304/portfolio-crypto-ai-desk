"""Shadow-only crypto ticker monitor for pending symbols (2026-07-05).

Records a lightweight bid/ask/last/spread/data_age snapshot for pending A/B crypto symbols and,
purely as a SHADOW read-model, notes when the last price is inside a signal's entry band
(hypothetical touch). It is compared against the candle tracker's recorded entry to estimate how
much earlier a tick stream would have seen the touch.

HARD boundary: this stream/snapshot NEVER places a trade, NEVER changes score/tier/actionability/
TP/SL/sizing, and NEVER unlocks live. It only writes to the additive `pending_ticker_shadow` table.

Transport:
  * DEFAULT = polling REST bookTicker (Binance public, no key) — safe, testable, no extra deps.
  * OPTIONAL = a public websocket stream (Binance/Bybit) for lower latency — STAGED (needs the
    `websockets` dependency + a long-running process); if unavailable the system keeps working via
    polling. The normalizer + touch logic below are transport-agnostic and unit-tested.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Any

from src.config import load_config

_CREATE = """
CREATE TABLE IF NOT EXISTS pending_ticker_shadow (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recorded_at TEXT NOT NULL,
    symbol TEXT,
    source TEXT,
    bid REAL, ask REAL, last REAL, spread REAL, spread_bps REAL,
    ticker_ts TEXT, data_age_sec REAL,
    signal_id TEXT, in_entry_band INTEGER, note TEXT
);
"""


def _db_path(db: Any) -> str:
    if db is None:
        return str(load_config().db_path)
    return str(getattr(db, "db_path", db))


def _f(v) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def normalize_ticker(raw: dict, *, symbol: str, source: str = "binance_rest",
                     now: datetime | None = None) -> dict:
    """Pure: a raw exchange ticker payload → a normalized shadow row. Handles Binance bookTicker
    (`bidPrice`/`askPrice`) and generic `last`/`price` shapes. No I/O."""
    now = now or datetime.now(timezone.utc)
    bid = _f(raw.get("bidPrice") if "bidPrice" in raw else raw.get("bid"))
    ask = _f(raw.get("askPrice") if "askPrice" in raw else raw.get("ask"))
    last = _f(raw.get("lastPrice") if "lastPrice" in raw else raw.get("last") or raw.get("price"))
    if last is None and bid is not None and ask is not None:
        last = round((bid + ask) / 2.0, 10)
    spread = (ask - bid) if (bid is not None and ask is not None) else None
    mid = ((bid + ask) / 2.0) if (bid is not None and ask is not None) else last
    spread_bps = round(spread / mid * 10000.0, 2) if (spread is not None and mid) else None
    tts = raw.get("time") or raw.get("ts") or raw.get("E")
    ticker_ts = None
    data_age = None
    if tts is not None:
        try:
            # exchange epoch ms
            tdt = datetime.fromtimestamp(float(tts) / 1000.0, tz=timezone.utc)
            ticker_ts = tdt.isoformat()
            data_age = round((now - tdt).total_seconds(), 2)
        except Exception:
            ticker_ts = None
    return {"recorded_at": now.isoformat(), "symbol": symbol, "source": source,
            "bid": bid, "ask": ask, "last": last, "spread": spread, "spread_bps": spread_bps,
            "ticker_ts": ticker_ts, "data_age_sec": data_age, "signal_id": None,
            "in_entry_band": None, "note": None}


def hypothetical_touch(*, entry_low: float | None, entry_high: float | None,
                       last: float | None) -> bool | None:
    """True if `last` is inside the [entry_low, entry_high] band (hypothetical entry touch). None if
    inputs are missing. Pure."""
    if last is None or entry_low is None or entry_high is None:
        return None
    lo, hi = (entry_low, entry_high) if entry_low <= entry_high else (entry_high, entry_low)
    return lo <= last <= hi


def record_snapshot(db: Any, rows: list[dict]) -> int:
    """Append shadow rows (self-creating table). FAIL-OPEN — returns count written, 0 on error.
    Never touches signals/outcomes/alerts."""
    if not rows:
        return 0
    try:
        conn = sqlite3.connect(_db_path(db), timeout=30.0)
        try:
            conn.execute("PRAGMA busy_timeout=30000")
            conn.execute(_CREATE)
            for r in rows:
                conn.execute(
                    "INSERT INTO pending_ticker_shadow (recorded_at, symbol, source, bid, ask, last, "
                    "spread, spread_bps, ticker_ts, data_age_sec, signal_id, in_entry_band, note) "
                    "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (r.get("recorded_at"), r.get("symbol"), r.get("source"), r.get("bid"), r.get("ask"),
                     r.get("last"), r.get("spread"), r.get("spread_bps"), r.get("ticker_ts"),
                     r.get("data_age_sec"), r.get("signal_id"),
                     (1 if r.get("in_entry_band") else 0) if r.get("in_entry_band") is not None else None,
                     r.get("note")))
            conn.commit()
        finally:
            conn.close()
        return len(rows)
    except Exception:
        return 0


def _fetch_book_tickers(symbols: list[str]) -> dict[str, dict]:
    """Polling REST bookTicker (Binance public, no key). Fail-open: returns {} on any error."""
    if not symbols:
        return {}
    try:
        import requests
        out: dict[str, dict] = {}
        # binance bookTicker returns all symbols; filter to ours (mapped SYMBOL/USDT → SYMBOLUSDT)
        wanted = {s.replace("/", "").upper(): s for s in symbols}
        r = requests.get("https://api.binance.com/api/v3/ticker/bookTicker", timeout=15,
                         headers={"User-Agent": "crypto-ai-desk research"})
        r.raise_for_status()
        for item in r.json() or []:
            key = str(item.get("symbol") or "").upper()
            if key in wanted:
                out[wanted[key]] = item
        return out
    except Exception:
        return {}


def snapshot_pending(supervisor: Any, *, cap: int = 40, source: str = "binance_rest",
                     now: datetime | None = None) -> dict:
    """Take one shadow snapshot of pending A/B crypto symbols: fetch bid/ask, note hypothetical band
    touch vs the live signal entry, and record. SHADOW ONLY — never trades. Fail-open."""
    now = now or datetime.now(timezone.utc)
    db = supervisor.db
    try:
        active = [dict(r) for r in db.load_active_signals()]
    except Exception:
        active = []
    pend = [s for s in active if str(s.get("asset_class") or "crypto").lower() == "crypto"
            and str(s.get("tier") or "").upper() in ("A", "B") and s.get("symbol")]
    pend = pend[:cap]
    symbols = sorted({str(s["symbol"]) for s in pend})
    tickers = _fetch_book_tickers(symbols)
    rows: list[dict] = []
    for s in pend:
        raw = tickers.get(str(s["symbol"]))
        if not raw:
            continue
        row = normalize_ticker(raw, symbol=str(s["symbol"]), source=source, now=now)
        touch = hypothetical_touch(entry_low=_f(s.get("entry_low")), entry_high=_f(s.get("entry_high")),
                                   last=row["last"])
        row["signal_id"] = s.get("signal_id")
        row["in_entry_band"] = touch
        rows.append(row)
    written = record_snapshot(db, rows)
    return {"available": bool(tickers), "symbols": len(symbols), "recorded": written,
            "in_band": sum(1 for r in rows if r.get("in_entry_band")),
            "transport": "polling_rest", "note": "shadow-only; never places a trade."}


def compare_touches(db: Any = None, *, recent_hours: int = 24, pending_only: bool = True,
                    asset_class: str = "crypto", now: datetime | None = None) -> dict:
    """Compare shadow in-band first-sighting vs the candle tracker's recorded entry, SCOPED to a
    recent crypto A/B universe (default: last ``recent_hours``, currently-active signals).

    Scoping fixes the earlier bug where every historical outcome inflated `missed`: the scope is the
    set of recent crypto A/B signals, and `missed`/`false_touches` are only counted WITHIN it:
      * missed        = scoped signals whose tracker saw an entry but shadow never saw the band.
      * false_touches = scoped signals where shadow saw the band but the tracker never triggered.
    Read-only / illustrative (polling shadow)."""
    now = now or datetime.now(timezone.utc)
    from datetime import timedelta
    cutoff = (now - timedelta(hours=int(recent_hours))).isoformat()
    want_ac = str(asset_class).lower() if asset_class else None
    _ACTIVE = ("generated", "waiting_for_entry", "triggered", "tp1_hit", "tp2_hit")
    try:
        conn = sqlite3.connect(_db_path(db), timeout=30.0)
        conn.row_factory = sqlite3.Row
        try:
            # 1) scope = recent crypto A/B signals (active-only when pending_only)
            try:
                sig_rows = [dict(r) for r in conn.execute(
                    "SELECT signal_id, asset_class, tier, status, created_at FROM proposed_signals").fetchall()]
            except sqlite3.OperationalError:
                sig_rows = []
            scope: set[str] = set()
            for s in sig_rows:
                if str(s.get("tier") or "").upper() not in ("A", "B"):
                    continue
                if want_ac and str(s.get("asset_class") or "crypto").lower() != want_ac:
                    continue
                if str(s.get("created_at") or "") < cutoff:
                    continue
                if pending_only and str(s.get("status") or "") not in _ACTIVE:
                    continue
                if s.get("signal_id"):
                    scope.add(str(s["signal_id"]))
            # 2) shadow in-band sightings, restricted to scope + recent window
            try:
                shadow = [dict(r) for r in conn.execute(
                    "SELECT signal_id, recorded_at FROM pending_ticker_shadow "
                    "WHERE in_entry_band=1 AND signal_id IS NOT NULL AND recorded_at >= ? "
                    "ORDER BY recorded_at", (cutoff,)).fetchall()]
            except sqlite3.OperationalError:
                shadow = []
            # 3) tracker entries, restricted to scope + recent entry
            try:
                outs = {r["signal_id"]: dict(r) for r in conn.execute(
                    "SELECT signal_id, MIN(entry_triggered_at) AS entry_triggered_at FROM signal_outcomes "
                    "WHERE entry_triggered=1 AND entry_triggered_at >= ? GROUP BY signal_id",
                    (cutoff,)).fetchall()}
            except sqlite3.OperationalError:
                outs = {}
        finally:
            conn.close()
    except Exception:
        return {"available": False, "reason": "db error"}

    first_band: dict[str, str] = {}
    for r in shadow:
        if r["signal_id"] in scope:
            first_band.setdefault(r["signal_id"], r["recorded_at"])
    outs = {sid: o for sid, o in outs.items() if sid in scope}   # tracker entries within scope only

    saved_min: list[float] = []
    false_touch = 0
    for sid, ts in first_band.items():
        o = outs.get(sid)
        if not o or not o.get("entry_triggered_at"):
            false_touch += 1                      # shadow band but no tracker entry IN SCOPE
            continue
        a, b = _pdt(ts), _pdt(o["entry_triggered_at"])
        if a and b:
            saved_min.append(round((b - a).total_seconds() / 60.0, 1))
    missed = sum(1 for sid in outs if sid not in first_band)   # tracker entry but shadow blind, IN SCOPE
    pos = [s for s in saved_min if s > 0]
    return {"available": bool(scope or shadow or outs), "scope_signals": len(scope),
            "recent_hours": recent_hours, "pending_only": pending_only, "asset_class": asset_class,
            "signals_with_shadow_band": len(first_band),
            "avg_minutes_saved": round(sum(pos) / len(pos), 1) if pos else None,
            "false_touches": false_touch, "missed": missed,
            "insufficient_sample": len(scope) < 3,
            "note": "polling shadow is illustrative; true savings need a real tick stream (staged)."}


def _pdt(ts):
    try:
        t = str(ts).strip().replace("Z", "+00:00")
        dt = datetime.fromisoformat(t)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except Exception:
        return None
