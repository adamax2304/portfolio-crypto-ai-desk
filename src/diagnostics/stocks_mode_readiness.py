"""PART 6 — stocks scalp/swing/invest readiness diagnostic (READ-ONLY; no actionability change).

Evaluates each stocks mode on signal volume, data coverage, forward-shadow A/B (if any), typical
holding window, and structural risks, and emits a readiness verdict:
  research_only · paper_shadow_candidate · not_ready
This NEVER enables a mode, changes routing/actionability, or touches scoring/final_r.
"""
from __future__ import annotations

import sqlite3
from typing import Any

from src.config import load_config

MODES = ("scalp", "intraday", "swing", "invest")


def _conn(db: str | None = None) -> sqlite3.Connection:
    cfg = load_config()
    c = sqlite3.connect(db or cfg.db_path)
    c.row_factory = sqlite3.Row
    return c


def analyze(days: int = 30, db: str | None = None) -> dict[str, Any]:
    conn = _conn(db)
    try:
        sig = {m: dict(r) for m, r in (
            (row["mode"], row) for row in conn.execute(
                "SELECT mode, COUNT(*) n, ROUND(AVG(score),1) avg_score, "
                "ROUND(AVG(validity_window_hours),1) avg_validity_h, "
                "SUM(CASE WHEN tier='A' THEN 1 ELSE 0 END) a_tier, "
                "COUNT(DISTINCT sector) sectors "
                "FROM proposed_signals WHERE asset_class='stocks' AND created_at >= datetime('now', ?) "
                "GROUP BY mode", (f"-{days} day",)))}
        # forward shadow A/B per stocks mode
        shadow: dict[str, dict] = {}
        try:
            for r in conn.execute(
                "SELECT p.mode mode, e.branch branch, e.net_r net_r, e.entry_fill_status fs, "
                "e.outcome_status os, e.close_reason cr "
                "FROM paper_shadow_execution_outcomes e JOIN proposed_signals p ON e.signal_id=p.signal_id "
                "WHERE p.asset_class='stocks' AND e.window='forward_since_activation'"):
                if r["os"] == "no_data" or r["cr"] == "data_gap" or r["fs"] != "filled":
                    continue
                g = shadow.setdefault(r["mode"], {"a_r": 0.0, "b_r": 0.0, "a_t": 0, "b_t": 0})
                if r["branch"] == "old_paper":
                    g["a_r"] += (r["net_r"] or 0); g["a_t"] += 1
                else:
                    g["b_r"] += (r["net_r"] or 0); g["b_t"] += 1
        except sqlite3.OperationalError:
            pass
        # data coverage (DATA_OK share)
        cov = {r["status"]: r["n"] for r in conn.execute(
            "SELECT status, COUNT(*) n FROM stock_intraday_coverage GROUP BY status")} \
            if conn.execute("SELECT name FROM sqlite_master WHERE name='stock_intraday_coverage'").fetchone() else {}
    finally:
        conn.close()

    cov_total = sum(cov.values()) or 0
    cov_ok = cov.get("DATA_OK", 0)
    out = {}
    for m in MODES:
        s = sig.get(m, {})
        n = int(s.get("n") or 0)
        sh = shadow.get(m)
        sh_b = round(sh["b_r"], 2) if sh else None
        sh_a = round(sh["a_r"], 2) if sh else None
        sh_delta = round((sh["b_r"] - sh["a_r"]), 2) if sh else None
        # readiness rule (conservative; data-driven; NEVER enables anything)
        if n == 0:
            verdict = "research_only"
            why = "mode generates no signals currently (not produced by the pipeline)"
        elif sh and sh["b_t"] >= 3 and sh_delta is not None and sh_delta >= 0:
            verdict = "paper_shadow_candidate"
            why = f"{n} signals/{days}d + forward shadow B {sh_b}R ≥ A {sh_a}R on {sh['b_t']} filled (still small)"
        elif n > 0:
            verdict = "research_only"
            why = (f"{n} signals/{days}d but forward shadow {'absent' if not sh else 'B<A or sample<3'} "
                   "— measure longer before paper-shadow")
        else:
            verdict = "not_ready"
            why = "insufficient data"
        out[m] = {
            "signals_30d": n, "avg_score": s.get("avg_score"), "a_tier": int(s.get("a_tier") or 0),
            "avg_validity_hours": s.get("avg_validity_h"), "distinct_sectors": int(s.get("sectors") or 0),
            "forward_shadow_B_r": sh_b, "forward_shadow_A_r": sh_a, "forward_shadow_delta_r": sh_delta,
            "forward_shadow_filled_B": (sh["b_t"] if sh else 0),
            "readiness": verdict, "why": why,
        }
    return {
        "days": days,
        "data_coverage": {"DATA_OK": cov_ok, "total": cov_total,
                          "data_ok_pct": round(100 * cov_ok / cov_total, 1) if cov_total else None,
                          "by_status": cov},
        "modes": out,
        "actionability_changed": False,
        "note": ("Diagnostic only. stocks scalp/swing/invest remain non-actionable; any enablement is a "
                 "separate, explicitly-approved step. 15m data is coarse for true scalp."),
    }
