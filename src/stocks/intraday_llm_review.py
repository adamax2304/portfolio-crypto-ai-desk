"""SI-6 — scheduled (NOT realtime) LLM review for stock-intraday A/B candidates. ADVISORY.

The LLM review runs as a routine task (pre-open / after-open / midday / before power-hour / EOD), NOT
in the entry path. This module (a) builds the review PACKET for the LLM to read out-of-band, (b)
ingests the LLM's structured verdict into `stocks_intraday_llm_reviews`, and (c) exposes an ADVISORY
routing helper. The LLM never creates a trade, changes score/tier/TP/SL, or unlocks live — it only
writes an advisory review row. Routing is opt-in via config
`intraday_guards.llm_review.require_fresh_llm_review_for_stocks_intraday_ab` (default false).
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DECISIONS = ("approve", "wait", "reject", "needs_human_review")

_DDL = """
CREATE TABLE IF NOT EXISTS stocks_intraday_llm_reviews (
  signal_id TEXT PRIMARY KEY, reviewed_at TEXT, review_cycle TEXT, decision TEXT, confidence REAL,
  reasons_json TEXT, risks_json TEXT, catalyst_assessment TEXT, market_assessment TEXT,
  sector_assessment TEXT, chase_risk TEXT, stale_data_risk TEXT, source_report_path TEXT
);
"""


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def ensure_table(conn):
    conn.execute(_DDL)


# ---- advisory routing (read-only) --------------------------------------------------------------
def latest_review(conn, signal_id: str) -> dict | None:
    try:  # read-only safe: never CREATE here (may be a mode=ro connection)
        r = conn.execute("SELECT reviewed_at, decision, confidence FROM stocks_intraday_llm_reviews "
                         "WHERE signal_id=?", (signal_id,)).fetchone()
    except sqlite3.OperationalError:
        return None
    return {"reviewed_at": r[0], "decision": r[1], "confidence": r[2]} if r else None


def should_route_to_review(*, db: str, signal_id: str, cfg: dict, now=None) -> tuple[bool, str]:
    """ADVISORY: (route_to_review_only, reason). Config-gated so it never blocks by default.
      - fresh reject/wait review → route to review-only (advisory demote).
      - if require_fresh_llm_review is True and no fresh review exists → route to review-only.
    """
    llm = (cfg or {}).get("llm_review") or {}
    require_fresh = bool(llm.get("require_fresh_llm_review_for_stocks_intraday_ab", False))
    fresh_min = float(llm.get("freshness_minutes", 90))
    now = now or datetime.now(timezone.utc)
    conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    try:
        rev = latest_review(conn, signal_id)
    finally:
        conn.close()
    if rev and rev.get("decision") in ("reject", "wait"):
        age = None
        try:
            age = (now - datetime.fromisoformat(rev["reviewed_at"])).total_seconds() / 60.0
        except Exception:
            age = None
        if age is None or age <= fresh_min:
            return True, f"llm_review_{rev['decision']}"
    if require_fresh:
        fresh_ok = rev is not None and (
            (now - datetime.fromisoformat(rev["reviewed_at"])).total_seconds() / 60.0 <= fresh_min
            if rev.get("reviewed_at") else False)
        if not fresh_ok:
            return True, "no_fresh_llm_review"
    return False, ""


# ---- packet (for the LLM to read out-of-band) --------------------------------------------------
def build_packet(*, db: str | None = None, review_cycle: str = "adhoc", out_dir: str | None = None,
                 lookback_hours: float = 48.0) -> str:
    from src.config import load_config
    cfg_proj = load_config()
    path = db or str(cfg_proj.db_path)
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        ab = conn.execute(
            "SELECT signal_id, symbol, direction, tier, created_at, raw_idea_json FROM proposed_signals "
            "WHERE asset_class='stocks' AND mode='intraday' AND tier IN ('A','B') "
            "AND created_at >= datetime('now', ?) ORDER BY created_at DESC LIMIT 40",
            (f"-{int(lookback_hours)} hour",)).fetchall()
        cwatch = conn.execute(
            "SELECT signal_id, symbol, direction, created_at, raw_idea_json FROM proposed_signals "
            "WHERE asset_class='stocks' AND mode='intraday' AND tier='C' "
            "AND created_at >= datetime('now', ?) ORDER BY created_at DESC LIMIT 40",
            (f"-{int(lookback_hours)} hour",)).fetchall()
    finally:
        conn.close()
    L = [f"# Stocks-Intraday LLM Review packet — cycle: {review_cycle}", "",
         "**ADVISORY / SHADOW. You (the reviewer) MUST NOT create trades, change score/tier/TP/SL, or "
         "unlock live. Output one of: approve / wait / reject / needs_human_review per candidate.**", "",
         f"## Actionable A/B stock-intraday candidates (last {int(lookback_hours)}h): {len(ab)}"]
    for sid, sym, d, tier, created, raw in ab:
        profile = ""
        try:
            payload = json.loads(raw) if raw else {}
            profile = str(payload.get("paper_entry_profile") or "")
        except Exception:
            pass
        label = f" profile={profile}" if profile else ""
        L.append(f"- `{sid}` {sym} {d} tier={tier}{label} @ {created}")
    L.append("")
    L.append(f"## Demoted-to-C watchlist (with gate demotion reasons): {len(cwatch)}")
    for sid, sym, d, created, raw in cwatch[:25]:
        reasons = ""
        profile = ""
        try:
            payload = json.loads(raw) if raw else {}
            g = payload.get("intraday_actionability") or {}
            profile = str(payload.get("paper_entry_profile") or "")
            reasons = ", ".join(v for v in (g.get("market_context_reason"), g.get("sector_confirmation_reason"),
                                            g.get("session_rule_reason"), g.get("liquidity_reason"),
                                            g.get("catalyst_quality_reason")) if v)
        except Exception:
            reasons = ""
        if profile:
            reasons = f"[profile={profile}] {reasons or 'demoted'}"
        L.append(f"- `{sid}` {sym} {d} — {reasons or 'demoted'}")
    L.append("")
    L.append("## Post-trade diagnostics + cohort context")
    try:
        from src.stocks import intraday_post_trade_classifier as ptc
        L.append(ptc.report_sections(db=path, lookback_days=14) or "_none_")
    except Exception:
        L.append("_unavailable_")
    L.append("")
    L.append("## Required output (structured JSON per candidate)")
    L.append("`{signal_id, decision, confidence, reasons, risks, catalyst_assessment, market_assessment, "
             "sector_assessment, chase_risk, stale_data_risk}` — advisory only; nothing is executed.")
    base = Path(out_dir) if out_dir else (_root() / "reports")
    base.mkdir(parents=True, exist_ok=True)
    out = base / "STOCKS_INTRADAY_LLM_REVIEW_LATEST.md"
    out.write_text("\n".join(L), encoding="utf-8")
    return str(out)


def ingest_reviews(*, reviews: list[dict], db: str | None = None, review_cycle: str = "adhoc",
                   source_report_path: str | None = None, now_iso: str | None = None) -> dict[str, Any]:
    """Persist LLM verdicts (advisory) — validates signal_id exists; never mutates proposed_signals /
    signal_outcomes / score / tier / live."""
    from src.config import load_config
    path = db or str(load_config().db_path)
    now = now_iso or datetime.now(timezone.utc).isoformat()
    conn = sqlite3.connect(path)
    try:
        ensure_table(conn)
        valid = {r[0] for r in conn.execute(
            "SELECT signal_id FROM proposed_signals WHERE asset_class='stocks' AND mode='intraday'")}
        n = 0
        for rv in reviews or []:
            sid = rv.get("signal_id")
            if sid not in valid or str(rv.get("decision")) not in DECISIONS:
                continue
            conn.execute(
                "INSERT OR REPLACE INTO stocks_intraday_llm_reviews VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (sid, now, review_cycle, rv.get("decision"), rv.get("confidence"),
                 json.dumps(rv.get("reasons")), json.dumps(rv.get("risks")),
                 rv.get("catalyst_assessment"), rv.get("market_assessment"), rv.get("sector_assessment"),
                 rv.get("chase_risk"), rv.get("stale_data_risk"), source_report_path))
            n += 1
        conn.commit()
        return {"ingested": n}
    finally:
        conn.close()


__all__ = ["build_packet", "ingest_reviews", "latest_review", "should_route_to_review", "ensure_table", "DECISIONS"]
