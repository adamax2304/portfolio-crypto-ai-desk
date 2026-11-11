"""Operational health for derivatives/on-chain sources (alert-only)."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from src.config import load_config
from src.data_collectors import market_intelligence_store as mi

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "data" / "diagnostics" / "market_intelligence_health.json"
STATE = ROOT / "data" / "diagnostics" / "market_intelligence_alert_state.json"
JOURNAL = ROOT / "logs" / "market_intelligence_errors.jsonl"


def _dt(value: Any) -> datetime | None:
    try:
        result = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return result.replace(tzinfo=timezone.utc) if result.tzinfo is None else result.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def _p95(values: list[float]) -> float | None:
    if not values:
        return None
    values = sorted(values)
    return values[min(len(values) - 1, int(0.95 * (len(values) - 1)))]


def _fast_row_high_watermark(conn, table: str) -> int:
    """Return a cheap append-only row estimate for operational health.

    Exact ``COUNT(*)`` calls across the multi-gigabyte intelligence archive can
    hold the scheduler for minutes.  These values are only used as source
    activity indicators, so the AUTOINCREMENT high-water mark is sufficient.
    Fall back to an exact count for small/non-autoincrement tables.
    """
    try:
        sequence = conn.execute(
            "SELECT seq FROM sqlite_sequence WHERE name=?", (table,)
        ).fetchone()
    except sqlite3.OperationalError:
        sequence = None
    if sequence is not None and sequence[0] is not None:
        return int(sequence[0])
    return int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])


def build_health(now: datetime | None = None) -> dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    issues = []
    with mi.connect() as conn:
        sources = [dict(r) for r in conn.execute(
            "SELECT * FROM intelligence_source_health ORDER BY source").fetchall()]
        for source in sources:
            last = _dt(source.get("last_success_at"))
            source_name = str(source["source"])
            max_age = 20 if source_name.startswith(("derivatives:", "liquidity:")) else 1800
            if source["source"].startswith("liquidations:"):
                max_age = 20
            if source_name in {"context:stablecoin_pegs", "context:cross_exchange_quotes"}:
                max_age = 10
            elif source_name == "context:deribit_dvol":
                max_age = 180
            elif source_name in {"context:token_unlocks", "context:sec_form4_bulk"}:
                max_age = 1800
            age_min = (now - last).total_seconds() / 60 if last else None
            source["age_minutes"] = age_min
            disabled = str(source.get("status") or "").startswith("disabled_")
            if disabled:
                continue
            if int(source.get("consecutive_failures") or 0) >= 2:
                issues.append({"key": source["source"], "severity": "critical", "reason": "consecutive_failures",
                               "detail": source.get("error")})
            elif age_min is not None and age_min > max_age:
                issues.append({"key": source["source"], "severity": "warning", "reason": "stale_source",
                               "detail": f"age={age_min:.1f}m"})

        majors = {}
        liquidity_coverage = {}
        for symbol in ("BTC/USDT", "ETH/USDT", "SOL/USDT"):
            ctx = mi.latest_derivatives_context(conn, symbol, as_of=now, max_age_minutes=15)
            rows = conn.execute(
                "SELECT exchange,provider_ts,funding_rate_8h,oi_usd FROM derivative_snapshots "
                "WHERE normalized_symbol=? AND source_kind='current_poll' AND provider_ts>=? "
                "AND provider_ts<=? ORDER BY provider_ts",
                (mi.normalize_symbol(symbol), (now - timedelta(hours=24)).isoformat(), now.isoformat()),
            ).fetchall()
            by_venue: dict[str, list[datetime]] = {}
            for row in rows:
                ts = _dt(row[1])
                if ts:
                    by_venue.setdefault(str(row[0]), []).append(ts)
            gaps = []
            for venue_times in by_venue.values():
                times = sorted(set(venue_times))
                gaps.extend((b - a).total_seconds() / 60 for a, b in zip(times, times[1:]))
            total = len(rows)
            null_funding = sum(1 for r in rows if r[2] is None)
            null_oi = sum(1 for r in rows if r[3] is None)
            majors[symbol] = {
                **ctx, "rows_24h": total, "p95_gap_minutes": _p95(gaps),
                "funding_null_rate": null_funding / total if total else None,
                "oi_usd_null_rate": null_oi / total if total else None,
            }
            if ctx["venue_count"] < 2:
                issues.append({"key": f"coverage:{symbol}", "severity": "warning",
                               "reason": "fewer_than_two_fresh_venues", "detail": ctx["venues"]})
            if majors[symbol]["p95_gap_minutes"] is not None and majors[symbol]["p95_gap_minutes"] > 10:
                issues.append({"key": f"gap:{symbol}", "severity": "warning", "reason": "p95_gap_gt_10m",
                               "detail": majors[symbol]["p95_gap_minutes"]})
            liquidity = mi.latest_liquidity_context(conn, symbol, as_of=now, max_age_minutes=15)
            liquidity_coverage[symbol] = liquidity
            if liquidity["venue_count"] < 1:
                issues.append({"key": f"liquidity:{symbol}", "severity": "warning",
                               "reason": "no_fresh_public_orderbook", "detail": liquidity["venues"]})

        counts = {}
        for table in ("derivative_snapshots", "funding_rate_events", "liquidation_events", "liquidity_snapshots",
                      "asset_contract_registry", "onchain_metric_snapshots", "token_security_snapshots",
                      "holder_concentration_snapshots", "wallet_flow_events",
                      "token_unlock_events", "stablecoin_peg_snapshots",
                      "cross_exchange_quote_snapshots", "options_context_snapshots",
                      "insider_transactions", "context_filter_decisions"):
            exists = conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone()
            counts[table] = _fast_row_high_watermark(conn, table) if exists else 0
    return {"as_of": now.isoformat(), "status": "critical" if any(i["severity"] == "critical" for i in issues)
            else "degraded" if issues else "ok", "issues": issues, "sources": sources,
            "major_coverage": majors, "liquidity_coverage": liquidity_coverage, "counts": counts,
            "policy": {"alert_after_consecutive_failures": 2, "paper_fail_open_on_missing": True,
                       "counts_are_append_high_watermarks": True}}


def _load_state() -> dict:
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:
        return {"active": []}


def refresh(*, send_telegram: bool = False, now: datetime | None = None) -> dict[str, Any]:
    health = build_health(now)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(health, indent=2, default=str), encoding="utf-8")
    active = sorted(i["key"] + ":" + i["reason"] for i in health["issues"])
    state = _load_state(); prior = sorted(state.get("active") or [])
    new, recovered = sorted(set(active) - set(prior)), sorted(set(prior) - set(active))
    if new or recovered:
        JOURNAL.parent.mkdir(parents=True, exist_ok=True)
        with JOURNAL.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"at": health["as_of"], "new": new, "recovered": recovered},
                                    default=str) + "\n")
    sent = False
    if send_telegram and (new or recovered):
        try:
            from src.notifiers.telegram import TelegramNotifier
            notifier = TelegramNotifier(ROOT / "config" / "notifications.yaml")
            text = "Market intelligence health\n"
            if new:
                text += "NEW: " + "; ".join(new[:12]) + "\n"
            if recovered:
                text += "RECOVERED: " + "; ".join(recovered[:12])
            notifier.send(text, parse_mode="")
            sent = True
        except Exception as exc:
            health["telegram_error"] = str(exc)
    STATE.write_text(json.dumps({"active": active, "updated_at": health["as_of"]}, indent=2), encoding="utf-8")
    health.update({"new_issues": new, "recovered": recovered, "telegram_sent": sent})
    return health
