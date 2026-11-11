"""Read-only latency read-model + DATA_GAP_LATE remediation diagnostics (add-only, 2026-07-03).

Aggregates `entry_latency_audit` (FAST / LEGITIMATE_LATE / DATA_GAP_LATE / DETECTION_LATENCY /
NO_DATA) by asset_class + mode, plus `signal_alerts` late→shadow counts. This is a VISIBILITY
surface only — it NEVER changes execution, entry/alert routing, scoring, tiers, or `final_r`, and it
never promotes anything. Consumed by the CLI and (read-only) by the control plane.

Two views:
  * ``latency_summary``       — item 8: FAST/LATE breakdown by asset/mode, avg recorded latency +
                                data gap, recent-7d vs all-time, late→shadow alert count.
  * ``data_gap_diagnostics``  — item 4: DATA_GAP_LATE share by asset/mode, avg/median data_gap_min,
                                top gap symbols, first-bar-gap stats, root-cause hint, and a hard
                                STOCKS-INTRADAY warning when the share exceeds the block threshold.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone

from src.config import load_config

DATA_GAP_LATE = "DATA_GAP_LATE"
_CAUSES = ("FAST", "LEGITIMATE_LATE", "SESSION_GAP", "DATA_GAP_LATE", "DETECTION_LATENCY", "NO_DATA",
           "HISTORICAL_RECONSTRUCTION")
_EXPECTED_WAIT_CAUSES = {"LEGITIMATE_LATE", "SESSION_GAP"}
# stocks-intraday promotion is BLOCKED above this DATA_GAP_LATE share (mirrors the shadow gate).
STOCKS_DGL_BLOCK_SHARE = 0.30


def _conn(db=None):
    c = sqlite3.connect(db or load_config().db_path)
    c.row_factory = sqlite3.Row
    return c


def _rows(conn):
    try:
        has_signals = bool(conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='proposed_signals'").fetchone())
        cols = {row[1] for row in conn.execute("PRAGMA table_info(entry_latency_audit)")}
        truth = "e.latency_truth" if "latency_truth" in cols else "NULL AS latency_truth"
        if has_signals:
            sql = ("SELECT e.signal_id, e.symbol, e.asset_class, e.mode, e.cause, e.data_gap_min, "
                   f"e.recorded_latency_min, e.created_at, e.computed_at, {truth}, p.tier "
                   "FROM entry_latency_audit e LEFT JOIN proposed_signals p ON p.signal_id=e.signal_id")
        else:
            truth = "latency_truth" if "latency_truth" in cols else "NULL AS latency_truth"
            sql = ("SELECT signal_id, symbol, asset_class, mode, cause, data_gap_min, "
                   f"recorded_latency_min, created_at, computed_at, {truth}, NULL AS tier FROM entry_latency_audit")
        return [dict(r) for r in conn.execute(sql).fetchall()]
    except sqlite3.OperationalError:
        return []


def _nums(vals):
    return [v for v in vals if isinstance(v, (int, float))]


def _avg(vals):
    v = _nums(vals)
    return round(sum(v) / len(v), 1) if v else None


def _median(vals):
    v = sorted(_nums(vals))
    if not v:
        return None
    n = len(v)
    m = n // 2
    return round(v[m] if n % 2 else (v[m - 1] + v[m]) / 2.0, 1)


def _cutoff_iso(days, now=None):
    now = now or datetime.now(timezone.utc)
    return (now - timedelta(days=int(days))).isoformat()


def latency_summary(db=None, *, recent_days: int = 7, now=None) -> dict:
    """Item 8 — FAST/LEGITIMATE_LATE/DATA_GAP_LATE breakdown by asset/mode with avg latencies,
    recent-7d vs all-time, and the late→shadow alert count. Read-only."""
    conn = _conn(db)
    try:
        rows = _rows(conn)
        try:
            late_shadow = conn.execute(
                "SELECT COUNT(*) FROM signal_alerts WHERE lower(COALESCE(alert_type,'')) LIKE '%late%' "
                "OR lower(COALESCE(alert_type,'')) LIKE '%shadow%'").fetchone()[0]
        except sqlite3.OperationalError:
            late_shadow = 0
    finally:
        conn.close()
    if not rows:
        return {"available": False, "reason": "entry_latency_audit empty", "by_mode": [],
                "overall": {}, "late_shadow_alerts": late_shadow}
    cutoff = _cutoff_iso(recent_days, now)

    def _agg(subset):
        n = len(subset)
        by_cause = {c: sum(1 for r in subset if r.get("cause") == c) for c in _CAUSES}
        true_gaps = [r.get("data_gap_min") for r in subset if r.get("cause") == DATA_GAP_LATE]
        factual = [r for r in subset if r.get("latency_truth") in {"point_in_time", "legacy_unclassified", None}]
        historical_n = sum(1 for r in subset if r.get("latency_truth") == "historical_reconstruction")
        return {"n": n, "by_cause": by_cause,
                "data_gap_late_share": round(by_cause["DATA_GAP_LATE"] / n, 3) if n else 0.0,
                "avg_recorded_latency_min": _avg([r.get("recorded_latency_min") for r in factual]),
                "factual_latency_n": len(factual),
                "historical_reconstruction_n": historical_n,
                # Backward-compatible raw first-bar delay. It can include valid
                # session/level waits, so it must never be read as a true gap.
                "avg_data_gap_min": _avg([r.get("data_gap_min") for r in subset]),
                "avg_first_bar_delay_min": _avg([r.get("data_gap_min") for r in subset]),
                "true_data_gap_n": by_cause[DATA_GAP_LATE],
                "avg_true_data_gap_min": _avg(true_gaps),
                "expected_wait_n": sum(1 for r in subset if r.get("cause") in _EXPECTED_WAIT_CAUSES)}

    groups: dict[tuple[str, str], list] = {}
    for r in rows:
        groups.setdefault((str(r.get("asset_class") or "?"), str(r.get("mode") or "?")), []).append(r)
    by_mode = []
    for (ac, mode), sub in sorted(groups.items()):
        by_mode.append({"asset_class": ac, "mode": mode, "all_time": _agg(sub),
                        "recent_7d": _agg([r for r in sub if str(r.get("created_at") or "") >= cutoff])})
    return {"available": True, "recent_days": recent_days,
            "overall": {"all_time": _agg(rows),
                        "recent_7d": _agg([r for r in rows if str(r.get("created_at") or "") >= cutoff])},
            "by_mode": by_mode, "late_shadow_alerts": late_shadow}


def _root_cause(gaps: list) -> str:
    g = _nums(gaps)
    if not g:
        return "no DATA_GAP_LATE rows"
    avg = sum(g) / len(g)
    if avg >= 6 * 60:
        return ("gaps average >6h → SCHEDULE/SESSION gap: signals created outside the US cash "
                "session; the first intraday bar only appears at the next open.")
    if avg >= 30:
        return ("gaps ~0.5-6h → yfinance intraday ROLLING-WINDOW / feed delay: the shallow window "
                "drops early-session bars and the feed lags — the dominant stock-intraday cause.")
    return "gaps small (<30min) → likely STALE CACHE / minor feed delay."


def data_gap_diagnostics(db=None, *, top: int = 8, recent_days: int = 7, now=None) -> dict:
    """Item 4 — DATA_GAP_LATE remediation view: share by asset/mode, avg/median data_gap_min,
    top gap symbols, first-bar-gap stats, root-cause hint, and a recent A/B operational cohort.
    Historical all-time warnings remain visible but are not substituted for recent health. Read-only."""
    conn = _conn(db)
    try:
        rows = _rows(conn)
    finally:
        conn.close()
    if not rows:
        return {"available": False, "reason": "entry_latency_audit empty", "by_mode": [],
                "warnings": [], "top_gap_symbols": [], "block_share_threshold": STOCKS_DGL_BLOCK_SHARE}
    cutoff = _cutoff_iso(recent_days, now)
    groups: dict[tuple[str, str], list] = {}
    for r in rows:
        groups.setdefault((str(r.get("asset_class") or "?"), str(r.get("mode") or "?")), []).append(r)
    sym_counts: dict[str, int] = {}
    gaps_all: list = []
    for r in rows:
        if r.get("cause") == DATA_GAP_LATE:
            sym_counts[r.get("symbol") or "?"] = sym_counts.get(r.get("symbol") or "?", 0) + 1
            gaps_all.append(r.get("data_gap_min"))
    top_syms = sorted(sym_counts.items(), key=lambda kv: kv[1], reverse=True)[:top]
    by_mode, warnings = [], []
    for (ac, mode), sub in sorted(groups.items()):
        n = len(sub)
        dgl = [r for r in sub if r.get("cause") == DATA_GAP_LATE]
        share = round(len(dgl) / n, 3) if n else 0.0
        # Closed-market C-tier planning rows remain visible in totals, but operational stock
        # intraday health is judged on potentially actionable A/B ideas only.
        has_tiers = any(str(r.get("tier") or "").upper() in {"A", "B", "C"} for r in sub)
        primary = ([r for r in sub if str(r.get("tier") or "").upper() in {"A", "B"}]
                   if ac.startswith("stock") and mode == "intraday" and has_tiers else sub)
        primary_dgl = [r for r in primary if r.get("cause") == DATA_GAP_LATE]
        primary_share = round(len(primary_dgl) / len(primary), 3) if primary else 0.0
        recent = [r for r in sub if str(r.get("created_at") or "") >= cutoff]
        recent_has_tiers = any(str(r.get("tier") or "").upper() in {"A", "B", "C"}
                               for r in recent)
        recent_primary = ([r for r in recent if str(r.get("tier") or "").upper() in {"A", "B"}]
                          if ac.startswith("stock") and mode == "intraday" and recent_has_tiers
                          else recent)
        recent_primary_dgl = [r for r in recent_primary if r.get("cause") == DATA_GAP_LATE]
        recent_primary_share = (round(len(recent_primary_dgl) / len(recent_primary), 3)
                                if recent_primary else None)
        by_mode.append({"asset_class": ac, "mode": mode, "n": n, "data_gap_late": len(dgl),
                        "data_gap_late_share": share,
                        "actionable_n": len(primary), "actionable_data_gap_late": len(primary_dgl),
                        "actionable_data_gap_late_share": primary_share,
                        "recent_n": len(recent),
                        "recent_data_gap_late": sum(1 for r in recent if r.get("cause") == DATA_GAP_LATE),
                        "recent_data_gap_late_share": (
                            round(sum(1 for r in recent if r.get("cause") == DATA_GAP_LATE) / len(recent), 3)
                            if recent else None),
                        "recent_actionable_n": len(recent_primary),
                        "recent_actionable_data_gap_late": len(recent_primary_dgl),
                        "recent_actionable_data_gap_late_share": recent_primary_share,
                        "avg_data_gap_min": _avg([r.get("data_gap_min") for r in dgl]),
                        "median_data_gap_min": _median([r.get("data_gap_min") for r in dgl]),
                        "first_bar_gap_min_avg": _avg([r.get("data_gap_min") for r in sub])})
        if ac.startswith("stock") and mode == "intraday" and primary_share > STOCKS_DGL_BLOCK_SHARE:
            warnings.append(
                f"STOCKS INTRADAY promotion BLOCKED: actionable A/B DATA_GAP_LATE share "
                f"{round(primary_share * 100)}% "
                f"> {int(STOCKS_DGL_BLOCK_SHARE * 100)}% — entry timestamps are coverage artifacts, "
                "not real fills; B cannot be promoted until stock-intraday coverage is fixed.")
    return {"available": True, "recent_days": recent_days, "by_mode": by_mode, "top_gap_symbols": top_syms,
            "root_cause_hint": _root_cause(gaps_all), "warnings": warnings,
            "block_share_threshold": STOCKS_DGL_BLOCK_SHARE}


def render_markdown(db=None, *, recent_days: int = 7) -> str:
    """Compact read-only Markdown for the CLI / report. No side effects."""
    ls = latency_summary(db, recent_days=recent_days)
    dg = data_gap_diagnostics(db)
    lines = ["## Entry-latency read-model (read-only; no execution/alert change)"]
    if not ls.get("available"):
        lines.append(f"- unavailable ({ls.get('reason')})")
        return "\n".join(lines)
    o_all = ls["overall"]["all_time"]
    o_rec = ls["overall"]["recent_7d"]
    lines.append(f"- Overall all-time: n {o_all['n']} · DATA_GAP_LATE {int(o_all['data_gap_late_share']*100)}% "
                 f"· avg latency {o_all['avg_recorded_latency_min']}min · avg gap {o_all['avg_data_gap_min']}min")
    lines.append(f"- Overall recent {recent_days}d: n {o_rec['n']} · DATA_GAP_LATE "
                 f"{int(o_rec['data_gap_late_share']*100)}% · late→shadow alerts {ls['late_shadow_alerts']}")
    lines.append(
        f"- Latency evidence: factual/legacy-frozen {o_all['factual_latency_n']} | "
        f"historical reconstruction excluded from SLA {o_all['historical_reconstruction_n']}."
    )
    lines.append("- Semantics: raw first-bar delay can include valid waits; true data gaps are DATA_GAP_LATE only "
                 f"(avg {o_all['avg_true_data_gap_min']}min across {o_all['true_data_gap_n']} rows; "
                 f"expected waits {o_all['expected_wait_n']}).")
    lines.append("")
    lines.append("**By asset/mode (all-time cause split):**")
    for m in ls["by_mode"]:
        bc = m["all_time"]["by_cause"]
        lines.append(f"- {m['asset_class']} {m['mode']}: FAST {bc['FAST']} · LATE {bc['LEGITIMATE_LATE']} "
                     f"· SESSION_GAP {bc['SESSION_GAP']} · DATA_GAP_LATE {bc['DATA_GAP_LATE']} "
                     f"· DETECTION {bc['DETECTION_LATENCY']} "
                     f"· share {int(m['all_time']['data_gap_late_share']*100)}%")
    if dg.get("available"):
        lines.append("")
        lines.append(f"**DATA_GAP_LATE remediation** — root cause: _{dg['root_cause_hint']}_")
        if dg["top_gap_symbols"]:
            lines.append("- Top gap symbols: " + ", ".join(f"{s}×{c}" for s, c in dg["top_gap_symbols"]))
        for w in dg["warnings"]:
            lines.append(f"- WARNING: {w}")
    return "\n".join(lines)
