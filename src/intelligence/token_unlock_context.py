"""Versioned token-unlock calendar and a conservative long-risk context."""
from __future__ import annotations

import json
import os
from html.parser import HTMLParser
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests

from src.data_collectors import market_intelligence_store as mi
from src.intelligence.context_config import ROOT, section
from src.intelligence.context_store import connect, insert_unlock


def _dt(value: Any) -> datetime | None:
    try:
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(float(value), tz=timezone.utc)
        out = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return out.replace(tzinfo=timezone.utc) if out.tzinfo is None else out.astimezone(timezone.utc)
    except (TypeError, ValueError, OSError):
        return None


def _f(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _symbol(value: Any) -> str:
    return str(value or "").upper().split("/", 1)[0].replace("-USDT", "").replace("USDT", "")


def _normalize_event(raw: dict[str, Any], source: str, observed_at: str,
                     parent: dict[str, Any] | None = None) -> dict[str, Any] | None:
    parent = parent or {}
    when = _dt(raw.get("unlock_at") or raw.get("date") or raw.get("timestamp"))
    symbol = _symbol(raw.get("asset_symbol") or raw.get("symbol") or parent.get("symbol")
                     or parent.get("token"))
    if not when or not symbol:
        return None
    tokens = _f(raw.get("unlock_tokens") or raw.get("tokens") or raw.get("noOfTokens"))
    if isinstance(raw.get("noOfTokens"), list):
        vals = [_f(x) for x in raw.get("noOfTokens") or []]
        tokens = sum(x for x in vals if x is not None) or None
    circ = _f(raw.get("circulating_supply") or parent.get("circSupply"))
    pct = _f(raw.get("pct_circulating") or raw.get("percentage") or raw.get("percent"))
    if pct is None and tokens is not None and circ and circ > 0:
        pct = tokens / circ * 100.0
    unlock_usd = _f(raw.get("unlock_usd") or raw.get("value_usd") or raw.get("unlockValue"))
    adv = _f(raw.get("avg_daily_volume_usd") or parent.get("avg_daily_volume_usd"))
    adv_days = _f(raw.get("unlock_adv_days"))
    if adv_days is None and unlock_usd is not None and adv and adv > 0:
        adv_days = unlock_usd / adv
    source_id = str(raw.get("id") or raw.get("source_event_id") or
                    f"{symbol}:{when.isoformat()}:{raw.get('category') or raw.get('recipient_type') or ''}")
    return {
        "source": source, "source_event_id": source_id, "observed_at": observed_at,
        "asset_symbol": symbol, "unlock_at": when.isoformat(), "unlock_tokens": tokens,
        "unlock_usd": unlock_usd, "pct_circulating": pct, "avg_daily_volume_usd": adv,
        "unlock_adv_days": adv_days,
        "recipient_type": str(raw.get("recipient_type") or raw.get("category") or "unknown").lower(),
        "unlock_type": str(raw.get("unlock_type") or raw.get("unlockType") or "unknown").lower(),
        "quality_status": str(raw.get("quality_status") or "ok"), "raw_json": raw,
    }


def _local_rows(path: Path) -> list[dict[str, Any]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return raw if isinstance(raw, list) else list(raw.get("events") or [])
    except Exception:
        return []


class _NextDataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.capture = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "script" and values.get("id") == "__NEXT_DATA__":
            self.capture = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self.capture:
            self.capture = False

    def handle_data(self, data: str) -> None:
        if self.capture:
            self.parts.append(data)


def _public_calendar_events(payload: dict[str, Any], *, now: datetime,
                            cfg: dict[str, Any]) -> list[dict[str, Any]]:
    emissions = (((payload.get("props") or {}).get("pageProps") or {}).get("emissions") or [])
    end_ts = now.timestamp() + float(cfg.get("public_horizon_days", 45)) * 86400.0
    include_types = {str(x).lower() for x in cfg.get("include_unlock_types", ["cliff"])}
    overrides = {str(k).lower(): str(v).upper()
                 for k, v in (cfg.get("symbol_overrides") or {}).items()}
    rows: list[dict[str, Any]] = []
    for parent in emissions:
        if not isinstance(parent, dict):
            continue
        prices = parent.get("tokenPrice") or []
        latest_price = prices[-1] if prices and isinstance(prices[-1], dict) else {}
        slug = str(parent.get("protocolSlug") or "").lower()
        symbol = overrides.get(slug) or parent.get("tSymbol") or latest_price.get("symbol")
        symbol = _symbol(symbol)
        circ = _f(parent.get("circSupply"))
        if not symbol:
            continue
        grouped: dict[int, list[dict[str, Any]]] = {}
        for event in parent.get("events") or []:
            if not isinstance(event, dict):
                continue
            unlock_type = str(event.get("unlockType") or "unknown").lower()
            ts = _f(event.get("timestamp"))
            if unlock_type not in include_types or ts is None or not now.timestamp() <= ts <= end_ts:
                continue
            grouped.setdefault(int(ts), []).append(event)
        for ts, events in grouped.items():
            token_amounts = []
            categories = []
            for event in events:
                values = event.get("noOfTokens") or []
                if not isinstance(values, list):
                    values = [values]
                token_amounts.extend(x for x in (_f(v) for v in values) if x is not None and x > 0)
                categories.append(str(event.get("category") or "unknown"))
            tokens = sum(token_amounts) or None
            pct = tokens / circ * 100.0 if tokens is not None and circ and circ > 0 else None
            when = datetime.fromtimestamp(ts, tz=timezone.utc)
            rows.append({
                "id": f"{slug or symbol}:{ts}:cliff", "asset_symbol": symbol,
                "unlock_at": when.isoformat(), "unlock_tokens": tokens,
                "pct_circulating": pct, "recipient_type": ",".join(sorted(set(categories))),
                "unlock_type": "cliff", "quality_status": "provisional_public_calendar",
                "provider_name": parent.get("name"), "provider_slug": slug,
                "provider_gecko_id": parent.get("gecko_id"), "source_url": cfg.get("public_fallback_url"),
                "raw_events": events,
            })
    return rows


def _read_public_cache(path: Path, *, now: datetime,
                       max_age_hours: float) -> tuple[list[dict[str, Any]], str | None]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        fetched = _dt(payload.get("fetched_at"))
        if fetched is None or (now - fetched).total_seconds() > max_age_hours * 3600.0:
            return [], None
        rows = payload.get("events") or []
        return ([x for x in rows if isinstance(x, dict)], fetched.isoformat())
    except Exception:
        return [], None


def _public_fallback_rows(cfg: dict[str, Any], *, now: datetime) -> tuple[list[dict[str, Any]], str, str | None]:
    if not cfg.get("public_fallback_enabled", False):
        return [], "disabled_public_fallback", None
    url = str(cfg.get("public_fallback_url") or "https://defillama.com/calendar")
    cache_path = ROOT / str(cfg.get("public_cache_path") or
                            "data/reference/token_unlocks_defillama_cache.json")
    try:
        res = requests.get(
            url, timeout=float(cfg.get("public_timeout_seconds", 45)),
            headers={"User-Agent": "crypto-ai-desk token-unlock research context"},
        )
        res.raise_for_status()
        max_bytes = int(float(cfg.get("public_max_payload_mb", 25)) * 1024 * 1024)
        if len(res.content) > max_bytes:
            raise ValueError("public calendar payload exceeds configured limit")
        parser = _NextDataParser()
        parser.feed(res.text)
        if not parser.parts:
            raise ValueError("public calendar missing __NEXT_DATA__")
        payload = json.loads("".join(parser.parts))
        rows = _public_calendar_events(payload, now=now, cfg=cfg)
        if not rows:
            raise ValueError("public calendar contained no eligible future cliff events")
        fetched_at = now.isoformat()
        for row in rows:
            row["snapshot_observed_at"] = fetched_at
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps({"fetched_at": fetched_at, "source_url": url, "events": rows},
                                         indent=2, default=str), encoding="utf-8")
        return rows, "ok_public_fallback", fetched_at
    except Exception as exc:
        rows, fetched_at = _read_public_cache(
            cache_path, now=now, max_age_hours=float(cfg.get("public_cache_max_age_hours", 48)))
        if rows and fetched_at:
            return rows, f"ok_cached_public_fallback:{type(exc).__name__}", fetched_at
        return [], f"error_public_fallback:{type(exc).__name__}", None


def _remote_rows(cfg: dict[str, Any], *, now: datetime) -> tuple[list[dict[str, Any]], str, str | None]:
    url = os.environ.get(str(cfg.get("provider_url_env") or "DEFILLAMA_UNLOCKS_URL"), "").strip()
    key = os.environ.get(str(cfg.get("provider_key_env") or "DEFILLAMA_API_KEY"), "").strip()
    if not url:
        return _public_fallback_rows(cfg, now=now)
    if "{key}" in url:
        if not key:
            return _public_fallback_rows(cfg, now=now)
        url = url.replace("{key}", key)
    try:
        res = requests.get(url, timeout=30, headers={"User-Agent": "crypto-ai-desk research"})
        res.raise_for_status()
        payload = res.json()
        rows = payload if isinstance(payload, list) else list(payload.get("data") or payload.get("protocols") or [])
        return rows, "ok_authenticated_provider", now.isoformat()
    except Exception as exc:
        fallback, status, observed_at = _public_fallback_rows(cfg, now=now)
        if fallback:
            return fallback, f"{status};authenticated_error:{type(exc).__name__}", observed_at
        return [], f"error:{type(exc).__name__}", None


def refresh(*, db_path=None, now: datetime | None = None) -> dict[str, Any]:
    cfg = section("token_unlock")
    current = now or datetime.now(timezone.utc)
    observed = current.isoformat()
    local_path = ROOT / str(cfg.get("local_events_path") or "data/reference/token_unlocks.json")
    raw_local = _local_rows(local_path)
    raw_remote, remote_status, remote_observed = _remote_rows(cfg, now=current)
    written = normalized = 0
    with connect(db_path) as conn:
        for source, rows, source_observed in (
            ("local", raw_local, observed),
            (str(cfg.get("provider") or "provider"), raw_remote, remote_observed or observed),
        ):
            for item in rows:
                events = item.get("events") if isinstance(item, dict) else None
                if events:
                    candidates = list(events)
                    nxt = item.get("nextEvent")
                    if isinstance(nxt, dict):
                        candidates.append(nxt)
                else:
                    candidates = [item]
                for event in candidates:
                    if not isinstance(event, dict):
                        continue
                    row = _normalize_event(event, source, source_observed,
                                           item if isinstance(item, dict) else None)
                    if row:
                        normalized += 1
                        written += int(insert_unlock(conn, row))
        disabled = not raw_local and not raw_remote and remote_status.startswith("disabled_")
        mi.record_source_health(
            conn, "context:token_unlocks", status="ok" if (raw_local or raw_remote) else remote_status,
            success=bool(raw_local or raw_remote) or disabled, records_written=written,
            latest_provider_ts=(remote_observed or observed) if normalized else None,
            details={"local": len(raw_local), "remote": len(raw_remote), "normalized": normalized},
        )
        conn.commit()
    return {"observed_at": observed, "provider_observed_at": remote_observed,
            "local_rows": len(raw_local), "remote_rows": len(raw_remote),
            "normalized": normalized, "written": written, "remote_status": remote_status}


def context(symbol: str, *, as_of: datetime | None = None, db_path=None,
            cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = cfg or section("token_unlock")
    now = as_of or datetime.now(timezone.utc)
    base = _symbol(symbol)
    out = {"status": "unknown", "asset_symbol": base, "action": "FULL_SIZE",
           "would_action": "FULL_SIZE", "reason": "no_verified_upcoming_unlock"}
    warning_days = float(cfg.get("warning_days", 30))
    with connect(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM token_unlock_events WHERE asset_symbol=? AND unlock_at>=? "
            "AND unlock_at<=? AND observed_at<=? ORDER BY unlock_at ASC, observed_at DESC, id DESC",
            (base, now.isoformat(), (now + timedelta(days=warning_days)).isoformat(), now.isoformat()),
        ).fetchall()
    if not rows:
        return out
    seen: set[tuple[str, str]] = set()
    candidates: list[tuple[int, float, float, dict[str, Any], datetime, datetime, str, str]] = []
    stale_items: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        identity = (str(item.get("source") or ""), str(item.get("source_event_id") or ""))
        if identity in seen:
            continue
        seen.add(identity)
        unlock_at = _dt(item.get("unlock_at"))
        observed = _dt(item.get("observed_at"))
        if not unlock_at or not observed:
            continue
        age_h = (now - observed).total_seconds() / 3600.0
        if age_h > float(cfg.get("max_source_age_hours", 36)):
            stale_items.append(item)
            continue
        days = (unlock_at - now).total_seconds() / 86400.0
        pct = _f(item.get("pct_circulating"))
        adv_days = _f(item.get("unlock_adv_days"))
        material = ((pct is not None and pct >= float(cfg.get("min_pct_circulating", 5.0))) or
                    (adv_days is not None and adv_days >= float(cfg.get("min_unlock_adv_days", 3.0))))
        would = "FULL_SIZE"
        reason = "upcoming_unlock_below_materiality"
        severity = 0
        if material and days <= float(cfg.get("shadow_only_days", 3)):
            would, reason, severity = "SHADOW_ONLY", "material_token_unlock_imminent", 3
        elif material and days <= float(cfg.get("half_size_days", 14)):
            would, reason, severity = "HALF_SIZE", "material_token_unlock_near", 2
        elif material and days <= warning_days:
            reason, severity = "material_token_unlock_watch", 1
        candidates.append((severity, pct or 0.0, adv_days or 0.0, item, unlock_at, observed,
                           would, reason))
    if not candidates:
        if stale_items:
            newest = max(stale_items, key=lambda item: str(item.get("observed_at") or ""))
            return {**out, "status": "stale", "context_ts": newest.get("observed_at"),
                    "reason": "unlock_calendar_stale"}
        return out
    severity, _, _, item, unlock_at, observed, would, reason = max(
        candidates, key=lambda value: (value[0], value[1], value[2], -value[4].timestamp()))
    days = (unlock_at - now).total_seconds() / 86400.0
    pct = _f(item.get("pct_circulating"))
    adv_days = _f(item.get("unlock_adv_days"))
    action = would if cfg.get("paper_routing_enabled", False) else "FULL_SIZE"
    return {"status": "ok", "asset_symbol": base, "action": action, "would_action": would,
            "reason": reason, "context_ts": item.get("observed_at"), "unlock_at": item.get("unlock_at"),
            "days_to_unlock": round(days, 3), "pct_circulating": pct,
            "unlock_adv_days": adv_days, "recipient_type": item.get("recipient_type"),
            "unlock_type": item.get("unlock_type"), "source": item.get("source"),
            "quality_status": item.get("quality_status"), "events_considered": len(candidates),
            "severity": severity, "routing_enabled": bool(cfg.get("paper_routing_enabled"))}


__all__ = ["refresh", "context", "_normalize_event", "_public_calendar_events"]
