"""Symbol Timeline Memory (Shadow Intelligence PART 1).

Compact per-symbol memory of recent context + signal history. Foundation for the
other modules. Append-only event log + a compact summary for the alert path.
Shadow/diagnostic only; no trade effect; no network.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from typing import Any

from src.intelligence import store

EVENT_TYPES = {
    "signal_generated", "paper_entry_alert", "catalyst_seen", "funding_snapshot",
    "oi_snapshot", "phase_label", "onchain_risk_snapshot", "thesis_generated",
    "outcome_recorded",
}


def _now(now: datetime | None = None) -> datetime:
    return now or datetime.now(timezone.utc)


def _base(symbol: str) -> str:
    return str(symbol or "").split("/")[0].strip().upper()


def record_symbol_event(symbol: str, event_type: str, payload: dict[str, Any] | None,
                        now: datetime | None = None, conn=None) -> bool:
    """Append an event (idempotent via dedupe_key). Returns True if inserted.
    Fails open (returns False) — never raises into a caller."""
    try:
        sym = _base(symbol)
        if not sym or event_type not in EVENT_TYPES:
            return False
        at = _now(now).isoformat()
        payload = payload or {}
        dedupe = hashlib.sha256(
            f"{sym}|{event_type}|{at[:16]}|{json.dumps(payload, sort_keys=True, default=str)}"
            .encode()).hexdigest()[:24]
        own = conn is None
        c = conn or store.connect()
        try:
            c.execute(
                "INSERT OR IGNORE INTO timeline_events(symbol,event_type,event_at,"
                "payload_json,dedupe_key) VALUES(?,?,?,?,?)",
                (sym, event_type, at, json.dumps(payload, default=str), dedupe))
            if own:
                c.commit()
            return True
        finally:
            if own:
                c.close()
    except Exception:
        return False


def get_symbol_timeline_summary(symbol: str, now: datetime | None = None,
                                lookback_hours: int = 168) -> dict[str, Any]:
    """Compute a compact summary from the event log. RO + fail-open to 'unknown'."""
    sym = _base(symbol)
    out = {
        "symbol": sym, "first_seen_at": None, "first_seen_price": None,
        "last_seen_at": None, "last_seen_price": None, "exchanges_seen": [],
        "recent_alert_count_24h": 0, "recent_alert_count_7d": 0,
        "prior_tiers": [], "prior_modes": [], "prior_signal_directions": [],
        "prior_catalyst_count": 0, "prior_squeeze_phase": None,
        "phase_transition_count": 0, "prior_onchain_risk_flags": [],
        "prior_thesis_summary": None, "last_invalidated_reason": None,
        "recent_outcome_bias": None, "funding_peak_value": None,
        "oi_peak_value": None, "timeline_confidence": "unknown",
        "data_freshness_sec": None, "event_count": 0,
    }
    conn = store.connect_ro()
    if conn is None:
        return out
    try:
        now_dt = _now(now)
        since = (now_dt - timedelta(hours=lookback_hours)).isoformat()
        rows = conn.execute(
            "SELECT event_type,event_at,payload_json FROM timeline_events "
            "WHERE symbol=? AND event_at>=? ORDER BY event_at ASC", (sym, since)
        ).fetchall()
        if not rows:
            return out
        out["event_count"] = len(rows)
        first = conn.execute(
            "SELECT event_at,payload_json FROM timeline_events WHERE symbol=? "
            "ORDER BY event_at ASC LIMIT 1", (sym,)).fetchone()
        if first:
            out["first_seen_at"] = first["event_at"]
            out["first_seen_price"] = json.loads(first["payload_json"] or "{}").get("price")
        c24 = (now_dt - timedelta(hours=24)).isoformat()
        tiers, modes, dirs, exch, outcomes = set(), set(), set(), set(), []
        cat = phases = 0
        last_phase = thesis = invalid = None
        funding_peak = oi_peak = None
        for r in rows:
            p = json.loads(r["payload_json"] or "{}")
            et = r["event_type"]
            out["last_seen_at"] = r["event_at"]
            if p.get("price") is not None:
                out["last_seen_price"] = p.get("price")
            if p.get("exchange"):
                exch.add(p["exchange"])
            if et == "paper_entry_alert" and r["event_at"] >= c24:
                out["recent_alert_count_24h"] += 1
            if et in ("signal_generated", "paper_entry_alert"):
                out["recent_alert_count_7d"] += 1
                if p.get("tier"):
                    tiers.add(p["tier"])
                if p.get("mode"):
                    modes.add(p["mode"])
                if p.get("direction"):
                    dirs.add(p["direction"])
            if et == "catalyst_seen":
                cat += 1
            if et == "phase_label":
                phases += 1
                last_phase = p.get("phase")
            if et == "thesis_generated":
                thesis = p.get("summary")
            if et == "outcome_recorded":
                if p.get("final_r") is not None:
                    outcomes.append(float(p["final_r"]))
                if p.get("invalidated_reason"):
                    invalid = p["invalidated_reason"]
            if et == "funding_snapshot" and p.get("funding") is not None:
                funding_peak = max(funding_peak, float(p["funding"])) if funding_peak is not None else float(p["funding"])
            if et == "oi_snapshot" and p.get("oi") is not None:
                oi_peak = max(oi_peak, float(p["oi"])) if oi_peak is not None else float(p["oi"])
            if et == "onchain_risk_snapshot" and p.get("flags"):
                out["prior_onchain_risk_flags"] = p["flags"]
        out["exchanges_seen"] = sorted(exch)
        out["prior_tiers"] = sorted(tiers)
        out["prior_modes"] = sorted(modes)
        out["prior_signal_directions"] = sorted(dirs)
        out["prior_catalyst_count"] = cat
        out["prior_squeeze_phase"] = last_phase
        out["phase_transition_count"] = phases
        out["prior_thesis_summary"] = thesis
        out["last_invalidated_reason"] = invalid
        out["funding_peak_value"] = funding_peak
        out["oi_peak_value"] = oi_peak
        if outcomes:
            avg = sum(outcomes) / len(outcomes)
            out["recent_outcome_bias"] = ("positive" if avg > 0.1 else
                                          "negative" if avg < -0.1 else "flat")
        try:
            last_dt = datetime.fromisoformat(out["last_seen_at"].replace("Z", "+00:00"))
            out["data_freshness_sec"] = int((now_dt - last_dt).total_seconds())
        except Exception:
            pass
        out["timeline_confidence"] = ("high" if len(rows) >= 8 else
                                      "medium" if len(rows) >= 3 else "low")
        return out
    except Exception:
        return out
    finally:
        conn.close()


def compact_timeline_for_payload(symbol: str, now: datetime | None = None) -> dict[str, Any]:
    """Small dict of timeline_* fields for the alert payload. Fail-open."""
    s = get_symbol_timeline_summary(symbol, now=now)
    return {
        "timeline_first_seen_at": s["first_seen_at"],
        "timeline_first_seen_price": s["first_seen_price"],
        "timeline_alerts_24h": s["recent_alert_count_24h"],
        "timeline_alerts_7d": s["recent_alert_count_7d"],
        "timeline_prior_phase": s["prior_squeeze_phase"],
        "timeline_prior_catalyst_count": s["prior_catalyst_count"],
        "timeline_recent_outcome_bias": s["recent_outcome_bias"],
        "timeline_confidence": s["timeline_confidence"],
        "timeline_data_freshness_sec": s["data_freshness_sec"],
    }


def cleanup_old_events(retention_days: int = 90, now: datetime | None = None) -> int:
    """Delete events older than retention. Returns rows deleted. Fail-open."""
    try:
        cutoff = (_now(now) - timedelta(days=retention_days)).isoformat()
        conn = store.connect()
        try:
            cur = conn.execute("DELETE FROM timeline_events WHERE event_at < ?", (cutoff,))
            conn.commit()
            return cur.rowcount or 0
        finally:
            conn.close()
    except Exception:
        return 0


def timeline_health_report() -> dict[str, Any]:
    conn = store.connect_ro()
    if conn is None:
        return {"status": "empty", "symbols": 0, "events": 0}
    try:
        ev = conn.execute("SELECT COUNT(*) n FROM timeline_events").fetchone()["n"]
        sy = conn.execute("SELECT COUNT(DISTINCT symbol) n FROM timeline_events").fetchone()["n"]
        last = conn.execute("SELECT MAX(event_at) m FROM timeline_events").fetchone()["m"]
        return {"status": "ok" if ev else "empty", "symbols": sy, "events": ev,
                "last_event_at": last}
    except Exception:
        return {"status": "unavailable", "symbols": 0, "events": 0}
    finally:
        conn.close()
