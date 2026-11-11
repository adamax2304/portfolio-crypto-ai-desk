"""DefiLlama free provider (2026-07-04) — production crypto context ingest.

Fetches protocol TVL + stablecoin supply from DefiLlama's FREE public API (no key) and normalizes
large moves into `news_items` as context events (source='DefiLlama', event_type tvl_change /
stablecoin_flow / chain_flow). Advisory/context ONLY — never a trade signal, never score/tier/live.
Fail-open network; the normalizer is pure and unit-tested. Covered by source-health.
"""
from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime, timezone
from typing import Any

_TVL_CHANGE_PCT = 8.0     # |1d TVL change| ≥ this% → emit a context event
_MIN_TVL = 50_000_000     # ignore tiny protocols
_VALID_TICKER = re.compile(r"^[A-Z0-9]{2,12}$")   # clean ticker shape (kills "-", "?", "", "BTC-USD")


def _tradable_universe() -> set[str]:
    """The set of tickers we actually track/trade — the crypto entity-alias canonical set. Used to
    gate which DefiLlama protocol symbols are allowed into detected_symbols_json. Best-effort: an
    empty set (matcher unavailable) means NO symbol is written (conservative — never pollute)."""
    try:
        from src.catalysts.entity_aliases import get_matcher
        from src.config import load_config
        return {str(t).upper() for t in get_matcher(str(load_config().root)).by_ticker.keys()}
    except Exception:
        return set()


def _valid_symbol(sym: str | None, tradable: set[str]) -> bool:
    """A DefiLlama symbol is writeable only if it is a clean ticker AND in our tradable universe.
    Rejects None / "" / "-" / "?" / junk and any non-tradable/obscure token."""
    if not sym:
        return False
    s = str(sym).strip().upper()
    if not _VALID_TICKER.match(s):
        return False
    return s in tradable


def _symbol_base(sym: str | None) -> str:
    return str(sym or "").strip().upper().split("/")[0]


def normalize_protocol_event(*, name: str, symbol: str | None, tvl: float, change_1d_pct: float,
                             category: str | None, chain: str | None, day: str,
                             tradable: set[str] | None = None) -> dict[str, Any]:
    """Pure: one DefiLlama protocol snapshot → a news_items-shaped context row. No I/O.

    Only writes ``detected_symbols_json`` when the protocol symbol is a clean ticker AND in the
    tradable universe (``tradable`` set; loaded from the crypto alias set when omitted). Non-tradable
    / junk symbols ("-", "?", "SYRUP", "BARD"…) are kept as ``raw_json.protocol_symbol`` context only
    — NEVER as a trading symbol. Advisory/context row; never a score/tier/signal/live change.
    """
    uni = tradable if tradable is not None else _tradable_universe()
    raw_sym = (str(symbol).strip().upper() if symbol else "")
    tradable_sym = raw_sym if _valid_symbol(raw_sym, uni) else ""
    direction = "bullish" if change_1d_pct > 0 else "bearish"
    imp = 1.4 + min(abs(change_1d_pct) / 20.0, 1.0)     # bigger move → higher importance
    title = (f"{name} TVL {change_1d_pct:+.1f}% (24h) to ${tvl/1e6:.0f}M"
             + (f" · {category}" if category else ""))
    return {
        "title": title, "source": "DefiLlama", "asset_class": "crypto",
        "url": f"https://defillama.com/protocol/{name.lower().replace(' ', '-')}#{day}",
        "published_at": f"{day}T00:00:00+00:00", "importance": round(imp, 2),
        "detected_symbols_json": json.dumps([f"{tradable_sym}/USDT"] if tradable_sym else []),
        "raw_json": json.dumps({"provider": "DefiLlama", "event_type": "tvl_change",
                                "source_quality": "primary", "direction_hint": direction,
                                "tvl_usd": tvl, "change_1d_pct": change_1d_pct, "category": category,
                                "chain": chain, "protocol": name,
                                "protocol_symbol": raw_sym or None,
                                "symbol_tradable": bool(tradable_sym)}),
    }


def cleanup_symbol_pollution(db: str | None = None, *, dry_run: bool = True) -> dict[str, Any]:
    """Remove non-tradable DefiLlama protocol symbols from ``detected_symbols_json``.

    Older rows were written before DefiLlama symbols were gated against the tradable universe, so
    context-only protocols such as ``-/USDT`` or ``BARD/USDT`` can still leak into read-models until
    they age out. This is a surgical news_items cleanup: it only touches rows with
    ``source='DefiLlama'``, preserves removed protocol symbols in ``raw_json.removed_detected_symbols``
    / ``raw_json.protocol_symbol``, and never touches scoring, signals, routing, or live state.
    """
    from src.config import load_config

    tradable = _tradable_universe()
    conn = sqlite3.connect(db or str(load_config().db_path), timeout=30)
    conn.row_factory = sqlite3.Row
    scanned = updated = removed = kept = 0
    try:
        try:
            rows = conn.execute(
                "SELECT id, detected_symbols_json, raw_json FROM news_items WHERE source='DefiLlama'"
            ).fetchall()
        except sqlite3.OperationalError:
            return {"available": False, "dry_run": dry_run, "scanned": 0, "updated": 0, "removed": 0}
        scanned = len(rows)
        for r in rows:
            try:
                syms = json.loads(r["detected_symbols_json"] or "[]") or []
            except Exception:
                syms = []
            try:
                raw = json.loads(r["raw_json"] or "{}") or {}
            except Exception:
                raw = {}
            clean: list[str] = []
            bad: list[str] = []
            for s in syms:
                base = _symbol_base(s)
                if _valid_symbol(base, tradable):
                    clean.append(f"{base}/USDT")
                else:
                    bad.append(str(s))
            if not bad:
                kept += len(clean)
                continue
            removed += len(bad)
            old_removed = list(raw.get("removed_detected_symbols") or [])
            raw["removed_detected_symbols"] = sorted(set(old_removed + bad))
            if not raw.get("protocol_symbol") and bad:
                raw["protocol_symbol"] = _symbol_base(bad[0]) or None
            raw["symbol_tradable"] = bool(clean)
            if not dry_run:
                conn.execute(
                    "UPDATE news_items SET detected_symbols_json=?, raw_json=? WHERE id=?",
                    (json.dumps(sorted(set(clean))), json.dumps(raw), r["id"]),
                )
            updated += 1
            kept += len(clean)
        if not dry_run:
            conn.commit()
    finally:
        conn.close()
    return {
        "available": True,
        "dry_run": dry_run,
        "scanned": scanned,
        "updated": updated,
        "removed": removed,
        "kept_tradable_symbols": kept,
        "note": "DefiLlama cleanup only touches news_items.detected_symbols_json/raw_json; no score/tier/live.",
    }


def _get(url: str):
    import requests
    r = requests.get(url, timeout=20, headers={"User-Agent": "crypto-ai-desk research"})
    r.raise_for_status()
    return r.json()


def refresh(db=None, *, top: int = 40, now: datetime | None = None) -> dict[str, Any]:
    """Ingest large DefiLlama TVL moves + stablecoin total into news_items context. Fail-open."""
    day = (now or datetime.now(timezone.utc)).date().isoformat()
    rows: list[dict] = []
    try:
        protocols = _get("https://api.llama.fi/protocols") or []
    except Exception:
        protocols = []
    movers = []
    for p in protocols:
        try:
            tvl = float(p.get("tvl") or 0)
            chg = float(p.get("change_1d") or 0)
        except (TypeError, ValueError):
            continue
        if tvl >= _MIN_TVL and abs(chg) >= _TVL_CHANGE_PCT:
            movers.append((abs(chg), p, tvl, chg))
    movers.sort(key=lambda x: x[0], reverse=True)
    tradable = _tradable_universe()          # load once; gate protocol symbols vs our tradable set
    for _, p, tvl, chg in movers[:top]:
        rows.append(normalize_protocol_event(name=str(p.get("name") or "?"), symbol=p.get("symbol"),
                                             tvl=tvl, change_1d_pct=chg, category=p.get("category"),
                                             chain=p.get("chain"), day=day, tradable=tradable))
    saved = 0
    if rows and db is not False:
        try:
            from src.config import load_config
            from src.storage.sqlite import SQLiteStore
            store = SQLiteStore(load_config().db_path if db is None else db)
            store.init_db()
            saved = store.save_news_rows(rows, asset_class="crypto")
        except Exception:
            saved = 0
    return {"generated_at": datetime.now(timezone.utc).isoformat(), "protocols_seen": len(protocols),
            "movers": len(movers), "saved": saved,
            "note": "DefiLlama TVL context — advisory/context only, never a trade signal or score change."}
