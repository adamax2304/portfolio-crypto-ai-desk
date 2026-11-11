"""News Source Health read-model (2026-07-03) — READ-ONLY diagnostics.

Cross-references `config/sources.yaml` (what SHOULD be ingesting) against `news_items` (what IS
landing) plus the last RSS/failure state, and classifies every source OK / STALE / DEAD / DISABLED
with warnings. Writes a Markdown report + a machine-readable JSON the control-plane reads. NEVER
fetches network, NEVER changes ingestion, scoring, tiers, or actionability — pure observability.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from src.config import load_config
from src.news.source_telemetry import latest_runs, source_key

STALE_HOURS = 48    # enabled + rows in 72h but none in this window → STALE
TRANSPORT_IDLE_HOURS = 6  # fresh poll/listener heartbeat can prove a quiet feed is alive
DEAD_HOURS = 72     # enabled but NO rows in this window → DEAD (config lists it, but it isn't writing)
LOW_MATCH_RATE = 0.15


def _parse_ts(s) -> datetime | None:
    """Robustly parse a news_items.published_at into an aware UTC datetime across the mixed formats
    seen in the wild: `...+00:00`, `...Z`, `YYYY-MM-DDTHH:MM:SS`, `YYYY-MM-DD HH:MM:SS`, date-only
    `YYYY-MM-DD`. Returns None for missing / `date_unavailable` / unparseable (→ 'unknown' bucket)."""
    if s is None:
        return None
    t = str(s).strip()
    if not t or t.lower() in ("date_unavailable", "none", "null", "nat"):
        return None
    t = t.replace("Z", "+00:00").replace(" ", "T", 1) if ("T" not in t and " " in t) else t.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(t)
        return (dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)).astimezone(timezone.utc)
    except Exception:
        pass
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(t[:19] if len(t) >= 19 else t, fmt).replace(tzinfo=timezone.utc)
        except Exception:
            continue
    return None


def window_news_rows(conn, *, hours: int, now: datetime | None = None, limit: int | None = None,
                     columns: str = "*", where: str | None = None,
                     params: tuple = ()) -> list[dict] | None:
    """Return `news_items` rows whose ``published_at`` PARSES (via :func:`_parse_ts`) into the last
    ``hours`` — the single robust rolling-window helper shared by every news read-model.

    Why this exists: a raw ``published_at >= datetime('now', ?)`` SQL filter mis-counts on this DB
    because ``published_at`` mixes ``Z`` / offset / date-only / ``date_unavailable`` formats that
    SQLite compares lexically. This helper parses each timestamp in Python, drops
    ``date_unavailable`` / ``None`` / invalid rows from the window, sorts by the PARSED datetime
    (desc), and applies ``limit`` AFTER filtering+sorting (so e.g. 24h vs 48h never collapse to the
    same LIMITed slice). ``conn`` must have ``row_factory = sqlite3.Row``. Read-only.

    Each returned dict has an extra ``_ts`` (aware UTC ``datetime``). Returns ``None`` on
    ``OperationalError`` (missing table/column) so callers can fail-open.
    """
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=int(hours))
    q = f"SELECT {columns} FROM news_items"
    if where:
        q += f" WHERE {where}"
    try:
        raw = conn.execute(q, params).fetchall()
    except sqlite3.OperationalError:
        return None
    out: list[dict] = []
    for r in raw:
        d = dict(r)
        dt = _parse_ts(d.get("published_at"))
        if dt is None or dt < cutoff:
            continue
        d["_ts"] = dt
        out.append(d)
    out.sort(key=lambda d: d["_ts"], reverse=True)
    if limit is not None:
        out = out[: int(limit)]
    return out


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_sources() -> dict[str, Any]:
    import yaml
    p = _root() / "config" / "sources.yaml"
    try:
        with open(p, "r", encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    except Exception:
        return {}


def _configured_sources(cfg: dict) -> list[dict[str, Any]]:
    """One descriptor per configured source (rss / telegram / api), with the exact `match_key`
    used to find its rows in news_items (RSS name; telegram `t.me/<handle>`)."""
    out: list[dict[str, Any]] = []
    for f in cfg.get("rss_feeds") or []:
        name = f.get("name") or "?"
        stype = "api" if ("edgar" in name.lower() or name.lower().startswith("sec ")) else "rss"
        out.append({"name": name, "match_key": name, "asset_class": f.get("asset_class", "crypto"),
                    "source_type": stype, "enabled": bool(f.get("enabled", True)),
                    "primary": bool(f.get("primary_source")), "disabled_reason": f.get("disabled_reason"),
                    "transport_error_grace_hours": float(f.get("transport_error_grace_hours", 0) or 0)})
    tg = cfg.get("telegram_channels") or {}
    tg_on = bool(tg.get("enabled", False))
    for ch in tg.get("channels") or []:
        h = ch.get("handle") or "?"
        out.append({"name": f"t.me/{h}", "match_key": f"t.me/{h}",
                    "asset_class": ch.get("asset_class", "crypto"), "source_type": "telegram",
                    "enabled": tg_on, "primary": bool(ch.get("primary_source")),
                    "disabled_reason": None if tg_on else "telegram_channels.enabled=false"})
    for api in cfg.get("fast_api_sources") or []:
        name = str(api.get("name") or "?")
        out.append({"name": name, "match_key": name,
                    "asset_class": api.get("asset_class", "stocks"), "source_type": "api",
                    "enabled": bool(api.get("enabled", True)),
                    "primary": bool(api.get("primary_source")), "disabled_reason": None})
    # Whole-listener transport health is separate from per-channel freshness.
    # A connected Telethon process with a quiet channel is not a dead channel,
    # while a failed session must still be visible immediately.
    out.append({"name": "Telegram collector", "match_key": "__telegram_collector__",
                "asset_class": "all", "source_type": "telegram_collector",
                "enabled": tg_on, "primary": True,
                "disabled_reason": None if tg_on else "telegram_channels.enabled=false"})
    # SEC EDGAR is ingested by src/news/edgar.py (CIK-mapped submissions API), NOT the RSS collector,
    # so it writes rows under source='SEC EDGAR'. Register it as an api primary source so health
    # matches those rows (the old 'SEC EDGAR Filings' RSS entry stays disabled with its reason).
    out.append({"name": "SEC EDGAR", "match_key": "SEC EDGAR", "asset_class": "stocks",
                "source_type": "api", "enabled": True, "primary": True, "disabled_reason": None})
    # optional paid / provider adapters (item 5) — api sources, disabled until a key is set
    for name, state in (cfg.get("optional_paid_sources") or {}).items():
        out.append({"name": name, "match_key": name, "asset_class": "crypto", "source_type": "api",
                    "enabled": str(state).lower() not in ("disabled", "false", "0", "off"),
                    "primary": False, "disabled_reason": None if str(state).lower() != "disabled"
                    else "optional_paid_sources: disabled (no API key)"})
    return out


def _aggregate(conn, *, now: datetime | None = None) -> dict[str, dict]:
    """Per-source rows_24h/72h + 24h match count + latest, computed with a Python timestamp parser so
    mixed published_at formats (Z / offset / date-only / invalid) are handled correctly. A single
    bounded scan of news_items; invalid timestamps land in `unknown_ts` (never crash, never counted
    into a window)."""
    now = now or datetime.now(timezone.utc)
    c24, c72 = now - timedelta(hours=24), now - timedelta(hours=72)
    try:
        rows = conn.execute(
            "SELECT source, published_at, detected_symbols_json FROM news_items").fetchall()
    except sqlite3.OperationalError:
        return {}
    agg: dict[str, dict] = {}
    for r in rows:
        src = r["source"]
        if src is None:
            continue
        a = agg.setdefault(src, {"total": 0, "r24": 0, "r72": 0, "matched24": 0,
                                 "latest": None, "unknown_ts": 0})
        a["total"] += 1
        dt = _parse_ts(r["published_at"])
        if dt is None:
            a["unknown_ts"] += 1
            continue
        matched = bool(r["detected_symbols_json"] and str(r["detected_symbols_json"]) not in ("[]", ""))
        if dt >= c72:
            a["r72"] += 1
        if dt >= c24:
            a["r24"] += 1
            if matched:
                a["matched24"] += 1
        iso = dt.isoformat()
        if a["latest"] is None or iso > a["latest"]:
            a["latest"] = iso
    return agg


def _failures() -> dict[str, str]:
    """Merge the last RSS-run failures + the supervisor last_update.json news_failures."""
    out: dict[str, str] = {}
    for rel in ("data/raw/news/rss_latest.json", "data/processed/market_summary/last_update.json"):
        p = _root() / rel
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            for k, v in ((d.get("failed_sources") or {}) | (d.get("news_failures") or {})).items():
                out[str(k)] = str(v)[:160]
        except Exception:
            continue
    return out


def _classify(src: dict, agg: dict, failed: str | None,
              now: datetime | None = None, transport: dict | None = None) -> tuple[str, list[str]]:
    r24, r72 = int(agg.get("r24") or 0), int(agg.get("r72") or 0)
    total = int(agg.get("total") or 0)
    match_rate = round((int(agg.get("matched24") or 0) / r24), 3) if r24 else None
    warnings: list[str] = []
    if not src["enabled"]:
        return "DISABLED", ([src["disabled_reason"]] if src.get("disabled_reason") else [])
    if r72 == 0:
        status = "DEAD"
        warnings.append("enabled but NO rows in 72h — in config yet not writing data "
                        "(broken feed / blocked / auth expired)")
        if total == 0:
            warnings.append("zero rows all-time")
        ref = now or datetime.now(timezone.utc)
        if src.get("name") == "SEC EDGAR" and ref.weekday() >= 5:
            status = "STALE"
            warnings = ["SEC EDGAR has no rows in 72h during a weekend/regulatory quiet window; "
                        "not counted as DEAD primary unless this persists on a business day"]
    elif r24 == 0:
        status = "STALE"
        warnings.append("no fresh rows in 24h (had rows in 72h)")
    else:
        status = "OK"
    transport_status = str((transport or {}).get("status") or "").lower()
    transport_finished = _parse_ts((transport or {}).get("finished_at"))
    ref = now or datetime.now(timezone.utc)
    transport_fresh = bool(
        transport_finished and 0 <= (ref - transport_finished).total_seconds() <= TRANSPORT_IDLE_HOURS * 3600
    )
    if src["enabled"] and transport_fresh and transport_status in {"ok", "ok_empty", "heartbeat", "reachable_empty"}:
        # No publication is not itself a broken source.  This distinction is
        # crucial on weekends and for quiet Telegram/RSS/API feeds: collection
        # health must come from a fresh per-source successful poll, while the
        # catalyst gate separately still requires fresh actual news.
        if r24 == 0:
            status = "OK_IDLE"
            warnings = ["fresh successful transport; no eligible publication in the last 24h"]
        elif src.get("source_type") == "telegram_collector":
            status = "OK"
            warnings = ["Telethon listener connected and this channel is fresh"]
    if src["enabled"] and transport_status in {"error", "timeout", "unauthorized", "disconnected"}:
        latest_publication = _parse_ts(agg.get("latest"))
        grace_hours = float(src.get("transport_error_grace_hours") or 0)
        publication_age_hours = (
            (ref - latest_publication).total_seconds() / 3600.0
            if latest_publication is not None else float("inf")
        )
        transient_redundant_failure = bool(
            grace_hours > 0
            and r24 > 0
            and 0 <= publication_age_hours <= grace_hours
            and transport_status in {"error", "timeout"}
        )
        status = "DEGRADED" if transient_redundant_failure else "ERROR"
        code = (transport or {}).get("error_code") or transport_status
        message = (transport or {}).get("error_message") or "transport failure"
        warnings.append(f"latest transport {transport_status} ({code}): {str(message)[:160]}")
        if transient_redundant_failure:
            warnings.append(
                f"feed still has publications within its configured {grace_hours:g}h transport grace; "
                "incident journaled as degraded, pipeline not declared down"
            )
    if failed:
        warnings.append(f"last run failed: {failed}")
    if src["primary"] and status not in {"OK", "OK_IDLE"}:
        warnings.append("PRIMARY source is not healthy")
    if match_rate is not None and match_rate < LOW_MATCH_RATE and r24 >= 10:
        warnings.append(f"low symbol_match_rate {int(match_rate*100)}% (mostly untagged headlines)")
    unknown = int(agg.get("unknown_ts") or 0)
    if unknown and total and unknown / total > 0.5:
        warnings.append(f"{unknown}/{total} rows have unparseable published_at (excluded from windows)")
    return status, warnings


def compute_source_health(db: str | None = None, *, now: datetime | None = None) -> dict[str, Any]:
    cfg = _load_sources()
    srcs = _configured_sources(cfg)
    conn = sqlite3.connect(db or str(load_config().db_path))
    conn.row_factory = sqlite3.Row
    try:
        agg = _aggregate(conn, now=now)
    finally:
        conn.close()
    failed = _failures()
    try:
        from src.news.telegram_recovery import latest_attempts as latest_recovery_attempts
        recovery = latest_recovery_attempts(db)
    except Exception:
        recovery = {}
    rows: list[dict[str, Any]] = []
    configured_keys = {s["match_key"] for s in srcs}
    telemetry = latest_runs(db)
    for s in srcs:
        a = agg.get(s["match_key"], {})
        r24, r72 = int(a.get("r24") or 0), int(a.get("r72") or 0)
        match_rate = round((int(a.get("matched24") or 0) / r24), 3) if r24 else None
        t = telemetry.get(source_key(s["match_key"], s["source_type"]))
        if s.get("source_type") == "telegram_collector":
            # The listener writes a heartbeat for each subscribed channel.
            # Those fresh per-channel heartbeats are stronger evidence that the
            # collector is running than an old process-start row, so derive
            # parent health from the newest child when needed.
            children = [v for k, v in telemetry.items() if k.startswith("telegram:t.me/")]
            freshest = max(children, key=lambda v: str(v.get("finished_at") or ""), default=None)
            if freshest and (not t or str(freshest.get("finished_at") or "") > str(t.get("finished_at") or "")):
                t = {**freshest, "status": "heartbeat", "source_name": "collector (child heartbeat)"}
        status, warns = _classify(
            s, a, failed.get(s["name"]) or failed.get(s["match_key"]), now=now, transport=t,
        )
        recovery_row = recovery.get(str(s["name"]).lower()) if s.get("source_type") == "telegram" else None
        if recovery_row and str(recovery_row.get("status")) == "reachable_empty":
            warns = [warning for warning in warns if "enabled but NO rows in 72h" not in warning]
            status = "OK_IDLE"
            warns.append("targeted catch-up confirmed channel reachable but zero eligible messages; "
                         "retry is cooldown-limited")
        elif recovery_row and str(recovery_row.get("status")) == "failed":
            # The targeted historical catch-up may fail while the live channel
            # has subsequently recovered.  Preserve the warning for audit but
            # do not overwrite a fresh per-channel heartbeat with a stale
            # label; an actually stale transport is still classified above.
            warns.append("last targeted catch-up failed; live channel heartbeat is evaluated separately")
        transport_ok = t and str(t.get("status") or "").lower() in {"ok", "ok_empty", "heartbeat"}
        rows.append({
            "source": s["name"], "asset_class": s["asset_class"], "source_type": s["source_type"],
            "enabled": s["enabled"], "primary_source": s["primary"],
            "rows_24h": r24, "rows_72h": r72, "rows_total": int(a.get("total") or 0),
            "symbol_match_rate_24h": match_rate, "latest_published_at": a.get("latest"),
            "last_success_at": (a.get("latest") if r24 > 0 else None),
            "last_failure": failed.get(s["name"]) or failed.get(s["match_key"]),
            "last_fetch_status": t.get("status") if t else None,
            "last_fetch_started_at": t.get("started_at") if t else None,
            "last_fetch_finished_at": t.get("finished_at") if t else None,
            "last_fetch_error": t.get("error_message") if t else None,
            "last_fetch_success_at": t.get("finished_at") if transport_ok else None,
            "last_fetch_item_count": int(t.get("item_count") or 0) if t else None,
            "targeted_recovery_status": recovery_row.get("status") if recovery_row else None,
            "targeted_recovery_at": recovery_row.get("attempted_at") if recovery_row else None,
            "stale_status": status, "warnings": warns,
        })
    # structured / keyless providers (item 5 + 2026-07-05 fix) — reconciled against REAL news_items
    # rows by provider source name, so an enabled free provider that IS ingesting (DefiLlama) shows
    # its true rows and its rows don't ALSO leak into `unregistered`. Statuses:
    #   DISABLED    — key-gated provider with no key
    #   OK / STALE  — enabled AND actually writing rows (fresh / had-rows-72h-but-not-24h)
    #   CONFIGURED  — enabled/known but NOT currently ingesting (free/fallback not wired or idle);
    #                 informational, NOT a health alarm like DEAD (which is a broken configured feed)
    try:
        from src.news.providers import all_provider_statuses as provider_statuses
        for p in provider_statuses():
            key = p["source"]
            configured_keys.add(key)              # provider rows must NOT double-count as unregistered
            a = agg.get(key, {})
            r24, r72, tot = int(a.get("r24") or 0), int(a.get("r72") or 0), int(a.get("total") or 0)
            mr = round((int(a.get("matched24") or 0) / r24), 3) if r24 else None
            if not p["enabled"]:
                status, warns = "DISABLED", ([p["reason"]] if p.get("reason") else [])
            elif r72 > 0:
                status = "OK" if r24 > 0 else "STALE"
                warns = [] if r24 > 0 else ["no fresh rows in 24h (had rows in 72h)"]
            else:
                status = "CONFIGURED"
                warns = ["enabled provider but 0 rows ingested in 72h — free/fallback source not "
                         "actively writing (run its refresh to ingest); not counted as OK"]
            rows.append({
                "source": key, "asset_class": p["asset_class"], "source_type": "api",
                "enabled": p["enabled"], "primary_source": False,
                "rows_24h": r24, "rows_72h": r72, "rows_total": tot,
                "symbol_match_rate_24h": mr, "latest_published_at": a.get("latest"),
                "last_success_at": (a.get("latest") if r24 > 0 else None), "last_failure": None,
                "stale_status": status, "warnings": warns})
    except Exception:
        pass
    # sources landing in news_items that are NOT in sources.yaml or a provider → bridge/enriched/manual
    unregistered = []
    for src_name, a in agg.items():
        if src_name in configured_keys or not src_name:
            continue
        stype = "telegram" if str(src_name).startswith("t.me/") else "enriched_review_or_manual"
        unregistered.append({"source": src_name, "source_type": stype,
                             "rows_24h": int(a.get("r24") or 0), "rows_72h": int(a.get("r72") or 0),
                             "rows_total": int(a.get("total") or 0), "latest_published_at": a.get("latest")})
    unregistered.sort(key=lambda x: x["rows_72h"], reverse=True)
    _ORDER = {"ERROR": 0, "DEAD": 1, "DEGRADED": 2, "STALE": 3, "CONFIGURED": 4,
              "DISABLED": 5, "OK_IDLE": 6, "OK": 7}
    rows.sort(key=lambda r: (_ORDER.get(r["stale_status"], 9), -r["rows_72h"]))
    summary = {
        "total_configured": len(rows),
        "ok": sum(1 for r in rows if r["stale_status"] == "OK"),
        "idle": sum(1 for r in rows if r["stale_status"] == "OK_IDLE"),
        "stale": sum(1 for r in rows if r["stale_status"] == "STALE"),
        "dead": sum(1 for r in rows if r["stale_status"] == "DEAD"),
        "error": sum(1 for r in rows if r["stale_status"] == "ERROR"),
        "degraded": sum(1 for r in rows if r["stale_status"] == "DEGRADED"),
        "disabled": sum(1 for r in rows if r["stale_status"] == "DISABLED"),
        "configured": sum(1 for r in rows if r["stale_status"] == "CONFIGURED"),
        "dead_primary": [r["source"] for r in rows if r["stale_status"] == "DEAD" and r["primary_source"]],
        "error_primary": [r["source"] for r in rows if r["stale_status"] == "ERROR" and r["primary_source"]],
        "blocking_error_dead": sum(
            1 for r in rows if r["primary_source"] and r["stale_status"] in {"ERROR", "DEAD"}
        ),
        "unregistered_sources": len(unregistered),
    }
    return {"generated_at": datetime.now(timezone.utc).isoformat(), "stale_hours": STALE_HOURS,
            "dead_hours": DEAD_HOURS, "summary": summary, "sources": rows,
            "unregistered": unregistered[:40],
            "note": "READ-ONLY. Health combines news_items freshness with optional transport telemetry. "
                    "Never changes ingestion/scoring/tiers/actionability. ERROR = latest collector transport "
                    "failure; DEAD = enabled in config but not writing and no transport success."}


def render_markdown(health: dict) -> str:
    s = health["summary"]
    lines = ["# News Source Health", "",
             f"_Generated: {health['generated_at'][:19]}Z · read-only diagnostic (no ingest/scoring change)._", "",
             f"- Configured: {s['total_configured']} — **OK {s['ok']} · DEGRADED {s.get('degraded', 0)} · "
             f"STALE {s['stale']} · "
             f"DEAD {s['dead']} · CONFIGURED {s.get('configured', 0)} · DISABLED {s['disabled']}**",
             f"- Dead PRIMARY sources: {', '.join(s['dead_primary']) or 'none'}",
             f"- Unregistered (bridge/enriched) sources writing data: {s['unregistered_sources']}", ""]
    lines.insert(3, f"- Transport errors: {s.get('error', 0)}")
    lines.append("| Source | class | type | status | 24h | 72h | match% | primary | warnings |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for r in health["sources"]:
        mr = f"{int(r['symbol_match_rate_24h']*100)}%" if r["symbol_match_rate_24h"] is not None else "—"
        w = "; ".join(r["warnings"])[:80] if r["warnings"] else ""
        lines.append(f"| {r['source']} | {r['asset_class']} | {r['source_type']} | {r['stale_status']} "
                     f"| {r['rows_24h']} | {r['rows_72h']} | {mr} | {'Y' if r['primary_source'] else ''} | {w} |")
    if health["unregistered"]:
        lines.append("")
        lines.append("**Unregistered sources (writing to news_items but not in sources.yaml):**")
        for u in health["unregistered"][:15]:
            lines.append(f"- {u['source']} ({u['source_type']}): 24h {u['rows_24h']} · 72h {u['rows_72h']}")
    return "\n".join(lines)


def refresh(db: str | None = None, *, write: bool = True) -> dict[str, Any]:
    """Compute health and (optionally) write reports/NEWS_SOURCE_HEALTH.md +
    data/diagnostics/news_source_health.json. Read-only w.r.t. the pipeline."""
    health = compute_source_health(db)
    if write:
        root = _root()
        (root / "reports").mkdir(parents=True, exist_ok=True)
        (root / "data" / "diagnostics").mkdir(parents=True, exist_ok=True)
        (root / "reports" / "NEWS_SOURCE_HEALTH.md").write_text(render_markdown(health), encoding="utf-8")
        (root / "data" / "diagnostics" / "news_source_health.json").write_text(
            json.dumps(health, indent=2, default=str), encoding="utf-8")
    return health
