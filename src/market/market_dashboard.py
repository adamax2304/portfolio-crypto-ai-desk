"""Market dashboard snapshot store + Opus-output parser (PART 10/11).

Writes `market_dashboard_snapshots` in the desk DB (the Control Plane backend reads it
read-only). The Opus enriched-review routine appends a `market_dashboard_update` JSON
block at the END of its output; `parse_and_store` extracts it and persists a snapshot.
Fail-open: invalid/missing JSON keeps the previous snapshot. A deterministic fallback
builds a minimal snapshot when Opus is unavailable.

Does NOT change the enriched-review body/logic — it only consumes a trailing block.
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
from datetime import datetime, timezone
from typing import Any

DB = os.environ.get("CRYPTO_AI_DESK_DB", "db/crypto_ai_desk.sqlite")

_COLS = [
    "timestamp", "crypto_fear_greed", "crypto_market_mode", "stocks_market_mode",
    "crypto_main_risk", "stocks_main_risk", "today_news", "long_term_news",
    "crypto_regime", "stocks_regime", "btc_dominance", "eth_btc", "vix",
    "spy_trend", "qqq_trend", "confidence", "source_summary", "generated_by", "raw_json",
]


def ensure_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS market_dashboard_snapshots ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "timestamp TEXT, crypto_fear_greed REAL, crypto_market_mode TEXT, stocks_market_mode TEXT, "
        "crypto_main_risk TEXT, stocks_main_risk TEXT, today_news TEXT, long_term_news TEXT, "
        "crypto_regime TEXT, stocks_regime TEXT, btc_dominance REAL, eth_btc REAL, vix REAL, "
        "spy_trend TEXT, qqq_trend TEXT, confidence REAL, source_summary TEXT, "
        "generated_by TEXT, raw_json TEXT, created_at TEXT)")
    conn.commit()


def store_snapshot(conn: sqlite3.Connection, snap: dict[str, Any]) -> int:
    ensure_table(conn)
    now = datetime.now(timezone.utc).isoformat()
    row = {k: snap.get(k) for k in _COLS}
    for jk in ("today_news", "long_term_news"):
        if isinstance(row.get(jk), (list, dict)):
            row[jk] = json.dumps(row[jk], ensure_ascii=False)
    row["created_at"] = now
    cols = ", ".join(_COLS + ["created_at"])
    ph = ", ".join("?" * (len(_COLS) + 1))
    cur = conn.execute(f"INSERT INTO market_dashboard_snapshots ({cols}) VALUES ({ph})",
                       tuple(row[c] for c in _COLS + ["created_at"]))
    conn.commit()
    return cur.lastrowid


_BLOCK_RE = re.compile(r'"market_dashboard_update"\s*:\s*\{', re.IGNORECASE)


def extract_market_block(text: str) -> dict | None:
    """Pull the {"market_dashboard_update": {...}} JSON object out of arbitrary text.
    Tolerant of surrounding markdown / prose. Returns the inner dict or None."""
    if not text:
        return None
    m = _BLOCK_RE.search(text)
    if not m:
        return None
    # find the brace that opens the inner object, then balance braces
    start = text.index("{", m.end() - 1)
    depth = 0
    for i in range(start, len(text)):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                blob = text[start:i + 1]
                try:
                    return json.loads(blob)
                except Exception:
                    return None
    return None


def _norm_snapshot(upd: dict) -> dict:
    """Map an Opus market_dashboard_update dict → snapshot row dict."""
    def news_list(key):
        out = []
        for n in (upd.get(key) or [])[:8]:
            out.append({"title": n.get("title"), "asset_or_sector": n.get("asset_or_sector"),
                        "impact": n.get("impact"), "horizon": n.get("horizon"),
                        "confidence": n.get("confidence"), "why_it_matters": n.get("why_it_matters")})
        return out
    return {
        "timestamp": upd.get("timestamp") or datetime.now(timezone.utc).isoformat(),
        "crypto_fear_greed": upd.get("crypto_fear_greed"),
        "crypto_market_mode": upd.get("crypto_market_mode"),
        "stocks_market_mode": upd.get("stocks_market_mode"),
        "crypto_main_risk": upd.get("crypto_main_risk"),
        "stocks_main_risk": upd.get("stocks_main_risk"),
        "today_news": news_list("today_important_news"),
        "long_term_news": news_list("long_term_important_news"),
        "crypto_regime": upd.get("crypto_regime"),
        "stocks_regime": upd.get("stocks_regime"),
        "btc_dominance": upd.get("btc_dominance"), "eth_btc": upd.get("eth_btc"),
        "vix": upd.get("vix"), "spy_trend": upd.get("spy_trend"), "qqq_trend": upd.get("qqq_trend"),
        "confidence": upd.get("confidence"),
        "source_summary": upd.get("source_summary"),
        "generated_by": "opus_enriched_review",
        "raw_json": json.dumps(upd, ensure_ascii=False),
    }


def fetch_market_extras() -> dict:
    """Deterministic market extras (VIX, SPY/QQQ trend, ETH/BTC) via yfinance. Fail-open
    per field → None + a source/reason string, never raises. Used to populate/backfill the
    Market dashboard so VIX is never silently blank."""
    out = {"vix": None, "vix_source": "unavailable", "spy_trend": None, "qqq_trend": None,
           "eth_btc": None, "btc_dominance": None}
    try:
        import yfinance as yf
    except Exception:
        out["vix_source"] = "yfinance not installed"
        return out

    def _last(ticker, period="5d", interval="1d"):
        try:
            h = yf.Ticker(ticker).history(period=period, interval=interval)
            return float(h["Close"].iloc[-1]) if len(h) else None
        except Exception:
            return None

    def _trend(ticker):
        try:
            h = yf.Ticker(ticker).history(period="1mo", interval="1d")
            if len(h) < 6:
                return None
            last = float(h["Close"].iloc[-1])
            sma = float(h["Close"].tail(10).mean())
            if last > sma * 1.005:
                return "up"
            if last < sma * 0.995:
                return "down"
            return "flat"
        except Exception:
            return None

    vix = _last("^VIX")
    if vix is not None:
        out["vix"] = round(vix, 2); out["vix_source"] = "yfinance ^VIX"
    out["spy_trend"] = _trend("SPY")
    out["qqq_trend"] = _trend("QQQ")
    eth = _last("ETH-USD"); btc = _last("BTC-USD")
    if eth and btc:
        out["eth_btc"] = round(eth / btc, 6)
    return out


def _backfill_extras(snap: dict) -> dict:
    """Fill null vix/spy/qqq/eth_btc on a snapshot from the deterministic fetch."""
    if snap.get("vix") is not None and snap.get("spy_trend") and snap.get("eth_btc") is not None:
        return snap
    ex = fetch_market_extras()
    for k in ("vix", "spy_trend", "qqq_trend", "eth_btc", "btc_dominance"):
        if snap.get(k) in (None, "", "null"):
            snap[k] = ex.get(k)
    snap["vix_source"] = ex.get("vix_source")
    return snap


def parse_and_store(text: str, db_path: str = DB, fill_extras: bool = True) -> dict:
    """Extract the Opus market block from review text and store it. Fail-open."""
    upd = extract_market_block(text)
    if not upd:
        return {"stored": False, "reason": "no valid market_dashboard_update block found"}
    snap = _norm_snapshot(upd)
    if fill_extras:
        snap = _backfill_extras(snap)   # ensure VIX/SPY/QQQ/ETH-BTC even if Opus left them null
    conn = sqlite3.connect(db_path)
    try:
        sid = store_snapshot(conn, snap)
        return {"stored": True, "id": sid, "timestamp": snap["timestamp"],
                "crypto_market_mode": snap["crypto_market_mode"], "vix": snap.get("vix")}
    finally:
        conn.close()


def deterministic_fallback(db_path: str = DB) -> dict:
    """Minimal snapshot from deterministic signals when Opus is unavailable.
    Reads the most recent proposed_signals regime hints — no external calls."""
    conn = sqlite3.connect(db_path); conn.row_factory = sqlite3.Row
    try:
        ensure_table(conn)
        try:
            reg = conn.execute(
                "SELECT market_regime, COUNT(*) n FROM proposed_signals "
                "WHERE asset_class='crypto' AND created_at >= datetime('now','-1 day') "
                "GROUP BY market_regime ORDER BY n DESC LIMIT 1").fetchone()
            crypto_reg = (reg["market_regime"] if reg else None) or "unknown"
        except Exception:
            crypto_reg = "unknown"
        snap = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "crypto_fear_greed": None, "crypto_market_mode": "unknown", "stocks_market_mode": "unknown",
            "crypto_main_risk": "deterministic fallback — Opus snapshot unavailable",
            "stocks_main_risk": "deterministic fallback — Opus snapshot unavailable",
            "today_news": [], "long_term_news": [],
            "crypto_regime": crypto_reg, "stocks_regime": "unknown",
            "btc_dominance": None, "eth_btc": None, "vix": None, "spy_trend": None, "qqq_trend": None,
            "confidence": 0.2, "source_summary": "deterministic fallback (no Opus block)",
            "generated_by": "deterministic_fallback", "raw_json": "{}",
        }
        snap = _backfill_extras(snap)   # still fetch VIX/SPY/QQQ/ETH-BTC even without Opus
        snap["source_summary"] = f"deterministic fallback (no Opus block) + {snap.get('vix_source')}"
        sid = store_snapshot(conn, snap)
        return {"stored": True, "id": sid, "fallback": True, "vix": snap.get("vix")}
    finally:
        conn.close()
