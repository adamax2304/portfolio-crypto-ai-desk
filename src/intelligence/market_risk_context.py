"""Free point-in-time stablecoin peg and cross-exchange quote collectors."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from statistics import median
from typing import Any

import requests

from src.config import load_config
from src.data_collectors import market_intelligence_store as mi
from src.intelligence.context_config import section
from src.intelligence.context_store import connect, insert_named

PEG_COLS = ("provider_ts", "received_at", "exchange", "stablecoin", "quote_currency",
            "bid", "ask", "mid", "quality_status", "raw_json")
QUOTE_COLS = ("provider_ts", "received_at", "exchange", "symbol", "bid", "ask", "mid",
              "mark_price", "index_price", "quote_volume_24h", "quality_status", "raw_json")


def _f(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _mid(bid: Any, ask: Any, fallback: Any = None) -> float | None:
    b, a, f = _f(bid), _f(ask), _f(fallback)
    if b is not None and a is not None and b > 0 and a > 0:
        return (b + a) / 2.0
    return f


def _get(url: str, *, params: dict[str, Any] | None = None) -> Any:
    res = requests.get(url, params=params, timeout=15, headers={"User-Agent": "crypto-ai-desk research"})
    res.raise_for_status()
    return res.json()


def _peg_quotes(now_iso: str) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for stable in ("USDT", "USDC"):
        # Coinbase Exchange does not list USDC-USD as a public product. USDC
        # still has two independent direct-USD venues below (Kraken + Gemini).
        if stable == "USDT":
            try:
                raw = _get(f"https://api.exchange.coinbase.com/products/{stable}-USD/ticker")
                rows.append({"provider_ts": str(raw.get("time") or now_iso), "received_at": now_iso,
                             "exchange": "coinbase", "stablecoin": stable, "quote_currency": "USD",
                             "bid": _f(raw.get("bid")), "ask": _f(raw.get("ask")),
                             "mid": _mid(raw.get("bid"), raw.get("ask"), raw.get("price")),
                             "quality_status": "ok", "raw_json": raw})
            except Exception as exc:
                errors.append(f"coinbase:{stable}:{type(exc).__name__}")
        try:
            pair = f"{stable}USD"
            raw = _get("https://api.kraken.com/0/public/Ticker", params={"pair": pair})
            result = raw.get("result") or {}
            item = next(iter(result.values())) if result else {}
            rows.append({"provider_ts": now_iso, "received_at": now_iso, "exchange": "kraken",
                         "stablecoin": stable, "quote_currency": "USD",
                         "bid": _f((item.get("b") or [None])[0]), "ask": _f((item.get("a") or [None])[0]),
                         "mid": _mid((item.get("b") or [None])[0], (item.get("a") or [None])[0],
                                     (item.get("c") or [None])[0]),
                         "quality_status": "ok", "raw_json": raw})
        except Exception as exc:
            errors.append(f"kraken:{stable}:{type(exc).__name__}")
        try:
            raw = _get(f"https://api.gemini.com/v1/pubticker/{stable.lower()}usd")
            provider_ts = now_iso
            if raw.get("volume", {}).get("timestamp"):
                provider_ts = datetime.fromtimestamp(
                    float(raw["volume"]["timestamp"]) / 1000.0, tz=timezone.utc).isoformat()
            rows.append({"provider_ts": provider_ts, "received_at": now_iso, "exchange": "gemini",
                         "stablecoin": stable, "quote_currency": "USD",
                         "bid": _f(raw.get("bid")), "ask": _f(raw.get("ask")),
                         "mid": _mid(raw.get("bid"), raw.get("ask"), raw.get("last")),
                         "quality_status": "ok", "raw_json": raw})
        except Exception as exc:
            errors.append(f"gemini:{stable}:{type(exc).__name__}")
    return [r for r in rows if r.get("mid")], errors


def _native_symbols() -> tuple[list[str], dict[str, str], dict[str, str]]:
    cfg = load_config()
    symbols = list(cfg.symbols)
    binance, bybit = {}, {}
    for canonical in symbols:
        binance[str(cfg.exchange_alias("binance", canonical)).replace("/", "")] = canonical
        bybit[str(cfg.exchange_alias("bybit", canonical)).replace("/", "")] = canonical
    return symbols, binance, bybit


def _market_quotes(now_iso: str) -> tuple[list[dict[str, Any]], list[str]]:
    _, binance_map, bybit_map = _native_symbols()
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    try:
        raw = _get("https://api.binance.com/api/v3/ticker/24hr")
        for item in raw if isinstance(raw, list) else []:
            canonical = binance_map.get(str(item.get("symbol") or ""))
            if not canonical:
                continue
            rows.append({"provider_ts": now_iso, "received_at": now_iso, "exchange": "binance",
                         "symbol": canonical, "bid": _f(item.get("bidPrice")), "ask": _f(item.get("askPrice")),
                         "mid": _mid(item.get("bidPrice"), item.get("askPrice"), item.get("lastPrice")),
                         "mark_price": None, "index_price": None,
                         "quote_volume_24h": _f(item.get("quoteVolume")), "quality_status": "ok",
                         "raw_json": item})
    except Exception as exc:
        errors.append(f"binance:{type(exc).__name__}")
    try:
        raw = _get("https://api.bybit.com/v5/market/tickers", params={"category": "linear"})
        for item in ((raw.get("result") or {}).get("list") or []):
            canonical = bybit_map.get(str(item.get("symbol") or ""))
            if not canonical:
                continue
            rows.append({"provider_ts": now_iso, "received_at": now_iso, "exchange": "bybit",
                         "symbol": canonical, "bid": _f(item.get("bid1Price")), "ask": _f(item.get("ask1Price")),
                         "mid": _mid(item.get("bid1Price"), item.get("ask1Price"), item.get("lastPrice")),
                         "mark_price": _f(item.get("markPrice")), "index_price": _f(item.get("indexPrice")),
                         "quote_volume_24h": _f(item.get("turnover24h")), "quality_status": "ok",
                         "raw_json": item})
    except Exception as exc:
        errors.append(f"bybit:{type(exc).__name__}")
    return [r for r in rows if r.get("mid")], errors


def refresh(*, db_path=None, now: datetime | None = None) -> dict[str, Any]:
    stamp = (now or datetime.now(timezone.utc)).isoformat()
    pegs, peg_errors = _peg_quotes(stamp)
    quotes, quote_errors = _market_quotes(stamp)
    peg_written = quote_written = 0
    with connect(db_path) as conn:
        for row in pegs:
            peg_written += int(insert_named(conn, "stablecoin_peg_snapshots", row, PEG_COLS))
        for row in quotes:
            quote_written += int(insert_named(conn, "cross_exchange_quote_snapshots", row, QUOTE_COLS))
        mi.record_source_health(conn, "context:stablecoin_pegs",
                                status="ok" if pegs else "error", success=bool(pegs),
                                records_written=peg_written, latest_provider_ts=stamp if pegs else None,
                                error=";".join(peg_errors) or None)
        mi.record_source_health(conn, "context:cross_exchange_quotes",
                                status="ok" if quotes else "error", success=bool(quotes),
                                records_written=quote_written, latest_provider_ts=stamp if quotes else None,
                                error=";".join(quote_errors) or None)
        conn.commit()
    return {"at": stamp, "peg_rows": len(pegs), "peg_written": peg_written,
            "quote_rows": len(quotes), "quote_written": quote_written,
            "errors": peg_errors + quote_errors}


def _parse(value: Any) -> datetime | None:
    try:
        out = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return out.replace(tzinfo=timezone.utc) if out.tzinfo is None else out.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def _canonical_symbol(symbol: str) -> str:
    value = str(symbol or "").upper().replace("-", "/").split(":", 1)[0]
    if "/" in value:
        return value
    for quote in ("USDT", "USDC", "USD"):
        if value.endswith(quote) and len(value) > len(quote):
            return f"{value[:-len(quote)]}/{quote}"
    return value


def stablecoin_state(*, as_of: datetime | None = None, db_path=None,
                     cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = cfg or section("stablecoin_depeg")
    now = as_of or datetime.now(timezone.utc)
    trusted = {str(x).lower() for x in cfg.get("trusted_venues", ["coinbase", "kraken", "gemini"])}
    max_age = timedelta(seconds=float(cfg.get("max_quote_age_seconds", 240)))
    states: list[dict[str, Any]] = []
    with connect(db_path) as conn:
        for stable in cfg.get("stablecoins", ["USDT", "USDC"]):
            rows = conn.execute(
                "SELECT * FROM (SELECT p.*,ROW_NUMBER() OVER (PARTITION BY exchange ORDER BY provider_ts DESC,id DESC) rn "
                "FROM stablecoin_peg_snapshots p WHERE stablecoin=? AND provider_ts<=?) WHERE rn=1",
                (stable, now.isoformat()),
            ).fetchall()
            fresh = [dict(r) for r in rows if str(r["exchange"]).lower() in trusted and _parse(r["provider_ts"])
                     and timedelta(0) <= now - _parse(r["provider_ts"]) <= max_age]
            mids = [float(r["mid"]) for r in fresh if r["mid"] is not None]
            deviation = abs(median(mids) - 1.0) * 100.0 if mids else None
            states.append({"stablecoin": stable, "fresh_venues": len(mids), "deviation_pct": deviation,
                           "median_price": median(mids) if mids else None,
                           "latest_ts": max((r["provider_ts"] for r in fresh), default=None)})
        min_v = int(cfg.get("min_confirming_venues", 2))
        eligible = [s for s in states if s["fresh_venues"] >= min_v and s["deviation_pct"] is not None]
        worst = max(eligible, key=lambda x: x["deviation_pct"], default=None)
        if not worst:
            return {"state": "UNKNOWN", "action": None, "reason": "insufficient_fresh_peg_venues",
                    "stablecoins": states, "routing_enabled": bool(cfg.get("paper_routing_enabled"))}
        dev = float(worst["deviation_pct"])
        watch = float(cfg.get("watch_deviation_pct", 0.5))
        stress = float(cfg.get("stress_deviation_pct", 1.0))
        crisis = float(cfg.get("crisis_deviation_pct", 2.0))
        state = "CRISIS" if dev >= crisis else "STRESS" if dev >= stress else "WATCH" if dev >= watch else "NORMAL"
        persistent = True
        if state in ("STRESS", "CRISIS"):
            cutoff = now - timedelta(minutes=float(cfg.get("persistence_minutes", 10)))
            venues = sorted(trusted)
            marks = ",".join("?" for _ in venues)
            tolerance = timedelta(seconds=max(300.0, float(cfg.get("max_quote_age_seconds", 240))))
            old = conn.execute(
                "SELECT mid FROM (SELECT p.*, ROW_NUMBER() OVER "
                "(PARTITION BY exchange ORDER BY provider_ts DESC,id DESC) rn "
                f"FROM stablecoin_peg_snapshots p WHERE stablecoin=? AND exchange IN ({marks}) "
                "AND provider_ts<=? AND provider_ts>=?) WHERE rn=1",
                (worst["stablecoin"], *venues, cutoff.isoformat(),
                 (cutoff - tolerance).isoformat()),
            ).fetchall()
            persistent = len(old) >= min_v and all(abs(float(r[0]) - 1.0) * 100.0 >= stress for r in old)
            if not persistent:
                state = "WATCH"
        action = None
        if cfg.get("paper_routing_enabled") and persistent:
            if state == "CRISIS":
                action = str(cfg.get("crisis_action", "SHADOW_ONLY"))
            elif state == "STRESS":
                action = str(cfg.get("stress_action", "SHADOW_ONLY"))
        return {"state": state, "action": action, "reason": f"{worst['stablecoin']}_peg_{state.lower()}",
                "stablecoin": worst["stablecoin"], "deviation_pct": round(dev, 4),
                "median_price": worst["median_price"], "fresh_venues": worst["fresh_venues"],
                "persistent": persistent, "context_ts": worst["latest_ts"], "stablecoins": states,
                "routing_enabled": bool(cfg.get("paper_routing_enabled"))}


def cross_exchange_state(symbol: str, *, as_of: datetime | None = None, db_path=None,
                         cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = cfg or section("cross_exchange")
    now = as_of or datetime.now(timezone.utc)
    trusted = {str(x).lower() for x in cfg.get("trusted_venues", ["binance", "bybit"])}
    max_age = timedelta(seconds=float(cfg.get("max_quote_age_seconds", 240)))
    canonical = _canonical_symbol(symbol)
    with connect(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM (SELECT q.*,ROW_NUMBER() OVER (PARTITION BY exchange ORDER BY provider_ts DESC,id DESC) rn "
            "FROM cross_exchange_quote_snapshots q WHERE symbol=? AND provider_ts<=?) WHERE rn=1",
            (canonical, now.isoformat()),
        ).fetchall()
        fresh = [dict(r) for r in rows if str(r["exchange"]).lower() in trusted and _parse(r["provider_ts"])
                 and timedelta(0) <= now - _parse(r["provider_ts"]) <= max_age]
        mids = [float(r["mid"]) for r in fresh if r["mid"] is not None and float(r["mid"]) > 0]
        min_v = int(cfg.get("min_fresh_trusted_venues", 2))
        if len(mids) < min_v:
            return {"status": "unknown", "action": "FULL_SIZE", "would_action": "FULL_SIZE",
                    "reason": "insufficient_fresh_trusted_venues", "fresh_venues": len(mids)}
        ref = median(mids)
        divergence = max(abs(v - ref) / ref * 10000.0 for v in mids)
        base = canonical.split("/", 1)[0]
        major = base in {str(x).upper() for x in cfg.get("major_symbols", [])}
        half = float(cfg.get("half_divergence_bps_major" if major else "half_divergence_bps_alt", 25 if major else 50))
        shadow = float(cfg.get("shadow_divergence_bps_major" if major else "shadow_divergence_bps_alt", 75 if major else 150))
        would = "SHADOW_ONLY" if divergence >= shadow else "HALF_SIZE" if divergence >= half else "FULL_SIZE"
        samples = int(cfg.get("persistence_samples", 2))
        persistent = True
        if would != "FULL_SIZE" and samples > 1:
            history = conn.execute(
                "SELECT provider_ts,exchange,mid FROM cross_exchange_quote_snapshots WHERE symbol=? "
                "AND provider_ts<? AND provider_ts>=? ORDER BY provider_ts DESC,id DESC LIMIT ?",
                (canonical, now.isoformat(),
                 (now - timedelta(minutes=float(cfg.get("persistence_max_minutes", 15)))).isoformat(),
                 samples * max(2, len(trusted))),
            ).fetchall()
            groups: dict[str, list[float]] = {}
            for r in history:
                if str(r[1]).lower() in trusted and r[2] is not None:
                    groups.setdefault(str(r[0]), []).append(float(r[2]))
            confirmations = 1
            for vals in groups.values():
                if len(vals) >= min_v:
                    med = median(vals)
                    if max(abs(v - med) / med * 10000.0 for v in vals) >= half:
                        confirmations += 1
                if confirmations >= samples:
                    break
            persistent = confirmations >= samples
            if not persistent:
                would = "FULL_SIZE"
        action = would if cfg.get("paper_routing_enabled") else "FULL_SIZE"
        return {"status": "ok", "action": action, "would_action": would,
                "reason": "cross_exchange_divergence" if would != "FULL_SIZE" else "venues_consistent",
                "divergence_bps": round(divergence, 3), "reference_mid": ref,
                "fresh_venues": len(mids), "persistent": persistent,
                "context_ts": max(r["provider_ts"] for r in fresh),
                "routing_enabled": bool(cfg.get("paper_routing_enabled"))}


__all__ = ["refresh", "stablecoin_state", "cross_exchange_state", "_peg_quotes", "_market_quotes"]
