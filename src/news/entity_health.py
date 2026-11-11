"""News Entity Resolver Health read-model (2026-07-08) — READ-ONLY diagnostics.

Answers one operational question: **after ingest, are news rows getting resolved (resolution_status /
trusted_symbols_json written) promptly, or are symbol-tagged rows piling up unresolved?**

It never fetches network, never resolves anything itself, never touches score / tier / final_r /
signal_outcomes / proposed_signals / live. It only READS `news_items` and reports freshness/coverage of
the entity-resolver enrichment, plus a severity so the scheduler / control-plane can flag a stalled
resolver. Writes reports/NEWS_ENTITY_HEALTH.md + data/diagnostics/news_entity_health.json (same pattern as
`news_source_health.json`).

Definitions (mirrors the trust layer):
  * `detected_symbols_json` = broad candidate set (union of resolver hits + naive ingest bare-ticker scan).
  * `resolution_status IS NOT NULL` = the resolver has processed the row.
  * `trusted_symbols_json NOT IN ('[]','')` = the row has ≥1 symbol with real provenance (drives catalyst).
  * unresolved_symbol_tagged = has detected symbols but the resolver has NOT run on it yet — the exact
    backlog we want to keep near zero.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.config import load_config
from src.news.source_health import _parse_ts

# One default scheduler cycle. The default market schedule runs every ~2h, so a symbol-tagged row older
# than this without a resolution_status means the resolver missed at least one cycle for it.
SCHEDULER_CYCLE_MINUTES = 120
# CRITICAL if this many symbol-tagged rows in 24h are still unresolved, OR the unresolved share is high,
# OR the resolver itself has not written anything in 24h.
CRITICAL_UNRESOLVED_24H = 50
CRITICAL_UNRESOLVED_SHARE = 0.5
RESOLVER_STALE_MINUTES = 24 * 60


def _has_symbols(v) -> bool:
    return bool(v is not None and str(v).strip() not in ("", "[]", "null", "[ ]"))


def compute_entity_health(db: str | None = None, *, now: datetime | None = None,
                          cycle_minutes: int = SCHEDULER_CYCLE_MINUTES,
                          examples: int = 8) -> dict[str, Any]:
    """Single bounded scan of news_items → resolver freshness/coverage metrics + severity. Read-only.

    Robust to the mixed `published_at` formats on this DB (parsed in Python via source_health._parse_ts),
    and fail-open: if the trust-layer columns don't exist yet, everything reports as unresolved rather
    than crashing.
    """
    now = now or datetime.now(timezone.utc)
    path = db or str(load_config().db_path)
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(news_items)")}
        has_status = "resolution_status" in cols
        has_trusted = "trusted_symbols_json" in cols
        has_resolved_at = "resolved_at" in cols
        sel = ["published_at", "detected_symbols_json", "source", "title", "asset_class"]
        if has_status:
            sel.append("resolution_status")
        if has_trusted:
            sel.append("trusted_symbols_json")
        if has_resolved_at:
            sel.append("resolved_at")
        try:
            rows = conn.execute(f"SELECT {', '.join(sel)} FROM news_items").fetchall()
        except sqlite3.OperationalError:
            rows = []
    finally:
        conn.close()

    def _blank():
        return {"rows": 0, "resolved": 0, "unresolved_symbol_tagged": 0, "trusted_symbol_tagged": 0,
                "preexisting_unverified": 0, "symbol_tagged": 0}

    win = {24: _blank(), 72: _blank()}
    unresolved_examples: list[dict[str, Any]] = []
    max_unresolved_age_min = 0.0
    oldest_unresolved_iso: str | None = None
    last_resolved_dt: datetime | None = None

    for r in rows:
        d = dict(r)
        # track resolver last-run regardless of the published_at window.
        if has_resolved_at:
            rdt = _parse_ts(d.get("resolved_at"))
            if rdt is not None and (last_resolved_dt is None or rdt > last_resolved_dt):
                last_resolved_dt = rdt
        pdt = _parse_ts(d.get("published_at"))
        if pdt is None:
            continue
        age_min = (now - pdt).total_seconds() / 60.0
        if age_min < 0:
            age_min = 0.0
        status = d.get("resolution_status") if has_status else None
        resolved = status is not None
        symbol_tagged = _has_symbols(d.get("detected_symbols_json"))
        trusted_tagged = _has_symbols(d.get("trusted_symbols_json")) if has_trusted else False
        unresolved_symbol_tagged = symbol_tagged and not resolved
        for h in (24, 72):
            if age_min <= h * 60:
                w = win[h]
                w["rows"] += 1
                if resolved:
                    w["resolved"] += 1
                if symbol_tagged:
                    w["symbol_tagged"] += 1
                if unresolved_symbol_tagged:
                    w["unresolved_symbol_tagged"] += 1
                if trusted_tagged:
                    w["trusted_symbol_tagged"] += 1
                if status == "preexisting_unverified":
                    w["preexisting_unverified"] += 1
        # oldest-unresolved-symbol-tagged tracking (72h scope; that's the resolver window) + examples.
        if unresolved_symbol_tagged and age_min <= 72 * 60:
            if age_min > max_unresolved_age_min:
                max_unresolved_age_min = age_min
                oldest_unresolved_iso = pdt.isoformat()
            unresolved_examples.append({
                "title": (str(d.get("title") or ""))[:160],
                "source": d.get("source"),
                "published_at": pdt.isoformat(),
                "age_minutes": round(age_min, 1),
                "asset_class": d.get("asset_class"),
                "detected_symbols_json": d.get("detected_symbols_json"),
            })

    unresolved_examples.sort(key=lambda e: e["published_at"], reverse=True)  # newest first
    u24 = win[24]["unresolved_symbol_tagged"]
    st24 = win[24]["symbol_tagged"]
    unresolved_share_24h = round(u24 / st24, 3) if st24 else 0.0
    resolver_age_min = (round((now - last_resolved_dt).total_seconds() / 60.0, 1)
                        if last_resolved_dt else None)
    resolver_stale = (resolver_age_min is None and win[24]["rows"] > 0) or (
        resolver_age_min is not None and resolver_age_min > RESOLVER_STALE_MINUTES)

    # severity — OK / WARN / CRITICAL.
    if (resolver_stale or u24 >= CRITICAL_UNRESOLVED_24H
            or (st24 >= 20 and unresolved_share_24h >= CRITICAL_UNRESOLVED_SHARE)):
        severity, reason = "CRITICAL", (
            "resolver has not run in 24h" if resolver_stale
            else f"unresolved_symbol_tagged_24h={u24} (share {int(unresolved_share_24h*100)}%) — resolver "
                 "is falling behind ingest")
    elif u24 > 0 and max_unresolved_age_min > cycle_minutes:
        severity, reason = "WARN", (
            f"{u24} symbol-tagged row(s) unresolved > one scheduler cycle "
            f"(oldest {int(max_unresolved_age_min)}m); resolver ran but missed these")
    else:
        severity, reason = "OK", (
            "no symbol-tagged rows unresolved beyond one scheduler cycle" if u24 == 0
            else f"{u24} unresolved but all newer than one cycle ({cycle_minutes}m)")

    return {
        "generated_at": now.isoformat(),
        "cycle_minutes": cycle_minutes,
        "trust_layer_present": bool(has_status and has_trusted),
        "severity": severity,
        "severity_reason": reason,
        "resolver_last_run_at": last_resolved_dt.isoformat() if last_resolved_dt else None,
        "resolver_last_run_age_minutes": resolver_age_min,
        "resolver_stale": bool(resolver_stale),
        "windows": {
            "24h": {
                "rows": win[24]["rows"], "resolved": win[24]["resolved"],
                "resolved_pct": round(win[24]["resolved"] / win[24]["rows"], 3) if win[24]["rows"] else None,
                "symbol_tagged": st24, "unresolved_symbol_tagged": u24,
                "unresolved_share": unresolved_share_24h,
                "trusted_symbol_tagged": win[24]["trusted_symbol_tagged"],
                "preexisting_unverified": win[24]["preexisting_unverified"],
            },
            "72h": {
                "rows": win[72]["rows"], "resolved": win[72]["resolved"],
                "resolved_pct": round(win[72]["resolved"] / win[72]["rows"], 3) if win[72]["rows"] else None,
                "symbol_tagged": win[72]["symbol_tagged"],
                "unresolved_symbol_tagged": win[72]["unresolved_symbol_tagged"],
                "trusted_symbol_tagged": win[72]["trusted_symbol_tagged"],
                "preexisting_unverified": win[72]["preexisting_unverified"],
            },
        },
        "max_unresolved_age_minutes": round(max_unresolved_age_min, 1),
        "oldest_unresolved_published_at": oldest_unresolved_iso,
        "newest_unresolved_examples": unresolved_examples[:examples],
        "note": "READ-ONLY. Freshness/coverage of the entity resolver over news_items. Never resolves, "
                "never changes score/tier/final_r/signal_outcomes/proposed_signals/live.",
    }


def render_markdown(h: dict) -> str:
    w24, w72 = h["windows"]["24h"], h["windows"]["72h"]
    icon = {"OK": "🟢", "WARN": "🟡", "CRITICAL": "🔴"}.get(h["severity"], "")
    lines = [
        "# News Entity Resolver Health", "",
        f"_Generated: {h['generated_at'][:19]}Z · read-only diagnostic (no ingest/resolve/scoring change)._", "",
        f"**Severity: {icon} {h['severity']}** — {h['severity_reason']}", "",
        f"- Resolver last run: {h['resolver_last_run_at'] or 'never'}"
        + (f" ({h['resolver_last_run_age_minutes']}m ago)" if h['resolver_last_run_age_minutes'] is not None else "")
        + (" · **STALE**" if h["resolver_stale"] else ""),
        f"- Trust-layer columns present: {'yes' if h['trust_layer_present'] else 'NO (pre-migration DB)'}",
        f"- Max unresolved (symbol-tagged) age: **{h['max_unresolved_age_minutes']}m**"
        + (f" (since {h['oldest_unresolved_published_at'][:19]}Z)" if h["oldest_unresolved_published_at"] else ""),
        "",
        "| window | rows | resolved | resolved% | symbol-tagged | unresolved symbol-tagged | trusted | preexisting_unverified |",
        "|---|---|---|---|---|---|---|---|",
        f"| 24h | {w24['rows']} | {w24['resolved']} | "
        f"{int((w24['resolved_pct'] or 0)*100)}% | {w24['symbol_tagged']} | "
        f"**{w24['unresolved_symbol_tagged']}** | {w24['trusted_symbol_tagged']} | {w24['preexisting_unverified']} |",
        f"| 72h | {w72['rows']} | {w72['resolved']} | "
        f"{int((w72['resolved_pct'] or 0)*100)}% | {w72['symbol_tagged']} | "
        f"**{w72['unresolved_symbol_tagged']}** | {w72['trusted_symbol_tagged']} | {w72['preexisting_unverified']} |",
    ]
    ex = h.get("newest_unresolved_examples") or []
    if ex:
        lines += ["", "**Newest unresolved symbol-tagged rows** (would be resolved on the next resolver pass):"]
        for e in ex:
            lines.append(f"- [{e['asset_class']}] {e['source']} · {e['published_at'][:19]}Z "
                         f"({e['age_minutes']}m) · {e['detected_symbols_json']} — {e['title'][:80]}")
    else:
        lines += ["", "_No symbol-tagged rows are currently unresolved._"]
    return "\n".join(lines)


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


# 2026-07-13 audit: this health check previously had zero alert capability -- even run manually it
# could never notify anyone. Deliberately NOT the full per-source transition-state machinery
# news/source_telemetry.py uses (that model fits N independent RSS/Telegram sources; here there is
# exactly one aggregate severity), so a small single-value dedup file is enough: alert once when
# severity newly becomes CRITICAL, once on recovery, never spam the same state every cycle.
_ALERT_STATE_FILE = "news_entity_health_alert_state.json"
_ALERT_COOLDOWN_HOURS = 12.0


def _load_alert_state(root: Path) -> dict[str, Any]:
    try:
        p = root / "data" / "diagnostics" / _ALERT_STATE_FILE
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    except Exception:
        return {}


def _save_alert_state(root: Path, state: dict[str, Any]) -> None:
    try:
        p = root / "data" / "diagnostics" / _ALERT_STATE_FILE
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(state, default=str), encoding="utf-8")
    except Exception:
        pass


def _notifier_for(root: Path):
    try:
        from src.notifiers.telegram import TelegramNotifier
        return TelegramNotifier(root / "config" / "notifications.yaml")
    except Exception:
        return None


def _maybe_alert(health: dict[str, Any], root: Path) -> list[str]:
    """Fail-open, best-effort Telegram alert on a CRITICAL transition or recovery. Never raises --
    a notifier problem must never affect the (read-only) health computation itself. Returns the
    (possibly empty) list of messages actually sent, for tests/observability."""
    sent: list[str] = []
    try:
        severity = str(health.get("severity") or "UNKNOWN")
        state = _load_alert_state(root)
        last_severity = state.get("last_severity")
        last_alert_iso = state.get("last_alert_at")
        age_h = None
        if last_alert_iso:
            try:
                age_h = (datetime.now(timezone.utc)
                        - datetime.fromisoformat(str(last_alert_iso))).total_seconds() / 3600.0
            except Exception:
                age_h = None
        msg = None
        if severity == "CRITICAL" and (last_severity != "CRITICAL"
                                       or age_h is None or age_h >= _ALERT_COOLDOWN_HOURS):
            msg = f"[NEWS ENTITY HEALTH] CRITICAL: {health.get('severity_reason', '')}"[:700]
        elif severity != "CRITICAL" and last_severity == "CRITICAL":
            msg = f"[NEWS ENTITY HEALTH] RECOVERED: severity now {severity}"
        if msg is None:
            return sent
        notifier = _notifier_for(root)
        if notifier is not None and getattr(notifier, "enabled", False) and getattr(notifier, "chat_id", ""):
            notifier.send(msg, parse_mode="")
            state["last_alert_at"] = datetime.now(timezone.utc).isoformat()
            sent.append(msg)
        state["last_severity"] = severity
        _save_alert_state(root, state)
    except Exception:
        pass
    return sent


def refresh(db: str | None = None, *, write: bool = True, now: datetime | None = None,
           send_telegram: bool = False) -> dict[str, Any]:
    """Compute entity-resolver health and (optionally) write reports/NEWS_ENTITY_HEALTH.md +
    data/diagnostics/news_entity_health.json. Read-only w.r.t. the pipeline. send_telegram=True
    additionally sends a deduped alert on a CRITICAL transition/recovery (fail-open; never raises)."""
    health = compute_entity_health(db, now=now)
    root = _root()
    if write:
        (root / "reports").mkdir(parents=True, exist_ok=True)
        (root / "data" / "diagnostics").mkdir(parents=True, exist_ok=True)
        (root / "reports" / "NEWS_ENTITY_HEALTH.md").write_text(render_markdown(health), encoding="utf-8")
        (root / "data" / "diagnostics" / "news_entity_health.json").write_text(
            json.dumps(health, indent=2, default=str), encoding="utf-8")
    if send_telegram:
        _maybe_alert(health, root)
    return health


__all__ = ["compute_entity_health", "render_markdown", "refresh",
           "SCHEDULER_CYCLE_MINUTES", "RESOLVER_STALE_MINUTES"]
