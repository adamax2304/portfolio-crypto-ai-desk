"""PART 7 + 10 — Paper-shadow forward quality monitor + promotion gate (read-only).

Reads `paper_shadow_execution_outcomes` and reports the FORWARD window (the only valid evidence)
with quality warnings, and EVALUATES (does not execute) the promotion gate. Never promotes B,
never touches final_r, no live.
"""
from __future__ import annotations

import sqlite3

from src.config import load_config
from src.execution.paper_shadow_engine import (
    CRYPTO_FEE_PROFILE, STOCK_FEE_PROFILE, _asset_is_stock,
)

# promotion-gate thresholds (definition only — never auto-executed)
GATE = {
    "min_forward_days": 14,
    "min_forward_trades": 60,
    "max_drawdown_worse_r": 5.0,        # B maxDD may be at most this much worse than A (in R)
    "max_data_gap_share": 0.30,         # ≤30% of forward trades may be DATA_GAP excluded
}
DEPRECATED_STOCKS_MODES = {("stocks", "swing"), ("stocks", "invest")}


def _conn(db=None):
    cfg = load_config()
    c = sqlite3.connect(db or cfg.db_path)
    c.row_factory = sqlite3.Row
    return c


def _book(rows):
    net_r = round(sum((r["net_r"] or 0) for r in rows), 3)
    net_usd = round(sum((r["net_pnl_usdt"] or 0) for r in rows), 2)
    fees = round(sum((r["fees_usdt"] or 0) for r in rows), 2)
    gross_r = round(sum((r["gross_r"] or 0) for r in rows), 3)
    # simple running-sum drawdown in R over chronological order
    peak = dd = run = 0.0
    for r in sorted(rows, key=lambda x: x.get("entry_fill_time") or ""):
        run += (r["net_r"] or 0)
        peak = max(peak, run)
        dd = min(dd, run - peak)
    return {"trades": len(rows), "net_r": net_r, "gross_r": gross_r, "net_usd": net_usd,
            "fees_usd": fees, "max_drawdown_r": round(dd, 3),
            "fee_drag_r": round(gross_r - net_r, 3)}


def forward_quality(db=None) -> dict:
    conn = _conn(db)
    try:
        try:
            cols = {r[1] for r in conn.execute("PRAGMA table_info(paper_shadow_execution_outcomes)")}
            lane_filter = (" AND COALESCE(shadow_lane,'ab_main') != 'stocks_intraday_forward'"
                           if "shadow_lane" in cols else "")
            rows = [dict(r) for r in conn.execute(
                "SELECT * FROM paper_shadow_execution_outcomes "
                "WHERE window='forward_since_activation'" + lane_filter).fetchall()]
            # The retired stocks swing/invest proposals are kept for audit history,
            # but they are not part of the active A/B promotion book.
            try:
                legacy_ids = {r[0] for r in conn.execute(
                    "SELECT e.signal_id FROM paper_shadow_execution_outcomes e "
                    "JOIN proposed_signals p ON p.signal_id=e.signal_id "
                    "WHERE e.window='forward_since_activation' "
                    "AND lower(COALESCE(p.asset_class,''))='stocks' "
                    "AND lower(COALESCE(p.mode,'')) IN ('swing','invest')").fetchall()}
                rows = [r for r in rows if r.get("signal_id") not in legacy_ids]
            except sqlite3.OperationalError:
                pass
        except sqlite3.OperationalError:
            return {"available": False, "reason": "shadow lane not populated"}
        act = conn.execute("SELECT v FROM paper_shadow_meta WHERE k='activated_at'").fetchone()
        activated = act[0] if act else None
        pre = conn.execute("SELECT v FROM paper_shadow_meta WHERE k='preentry_v2_activated_at'").fetchone()
        preentry_v2_activated = pre[0] if pre else None
        # PART 8: the DATA_GAP_LATE cohort (entry_latency_audit.cause) is dirty — the entry
        # timestamp is a coverage artifact, not a real fill. Exclude it from the primary edge stats.
        try:
            dgl = {r[0] for r in conn.execute(
                "SELECT signal_id FROM entry_latency_audit WHERE cause='DATA_GAP_LATE'")}
        except sqlite3.OperationalError:
            dgl = set()
    finally:
        conn.close()
    clean = [r for r in rows if r["signal_id"] not in dgl]  # primary edge = clean cohort only
    dgl_rows = len(rows) - len(clean)
    A = [r for r in clean if r["branch"] == "old_paper" and r.get("entry_fill_status") == "filled"]
    Ball = [r for r in clean if r["branch"] == "new_logic_shadow"]
    B = [r for r in Ball if r.get("entry_fill_status") == "filled"]
    a_book, b_book = _book(A), _book(B)
    n_fwd = len({r["signal_id"] for r in clean})   # primary = clean cohort (DATA_GAP_LATE excluded)
    n_total = len({r["signal_id"] for r in rows})
    dgl_signals = len({r["signal_id"] for r in rows if r["signal_id"] in dgl})
    maker = sum(1 for r in B if r.get("entry_order_type") == "maker")
    mk_posted = sum(int(r.get("maker_entry_posted") or 0) for r in Ball)
    mk_filled = sum(int(r.get("maker_entry_filled") or 0) for r in Ball)
    mk_missed = sum(int(r.get("maker_entry_missed") or 0) for r in Ball)
    mk_taker_fb = sum(int(r.get("taker_fallback_used") or 0) for r in Ball)
    data_gap = sum(1 for r in Ball if r.get("close_reason") == "data_gap" or r.get("outcome_status") == "no_data")
    warnings = []
    if b_book["trades"] < GATE["min_forward_trades"]:
        warnings.append(f"forward B sample {b_book['trades']} < {GATE['min_forward_trades']} trades")
    # days since activation
    days = None
    if activated:
        import datetime as _dt
        try:
            days = (_dt.datetime.now(_dt.timezone.utc) - _dt.datetime.fromisoformat(activated)).days
            if days < GATE["min_forward_days"]:
                warnings.append(f"forward window {days}d < {GATE['min_forward_days']}d")
        except Exception:
            pass
    if n_fwd and (data_gap / max(1, n_fwd)) > GATE["max_data_gap_share"]:
        warnings.append(f"DATA_GAP share {round(100*data_gap/n_fwd)}% > {int(GATE['max_data_gap_share']*100)}%")
    if b_book["net_r"] <= a_book["net_r"] and (b_book["gross_r"] > a_book["gross_r"]):
        warnings.append("B wins on GROSS but not NET — edge is fee-fragile")
    if b_book["max_drawdown_r"] < a_book["max_drawdown_r"] - GATE["max_drawdown_worse_r"]:
        warnings.append("B drawdown materially worse than A")
    if n_total and (dgl_signals / n_total) > 0.20:
        warnings.append(f"DATA_GAP_LATE cohort {round(100*dgl_signals/n_total)}% of forward — excluded from edge; stock intraday coverage suspect")
    return {
        "available": True, "activated_at": activated, "forward_days": days,
        "forward_signals": n_fwd, "A": a_book, "B": b_book,
        "delta_net_r": round(b_book["net_r"] - a_book["net_r"], 3),
        "delta_net_usd": round(b_book["net_usd"] - a_book["net_usd"], 2),
        "B_gt_A": sum(1 for r in B if (r["net_r"] or 0) > 0),
        "B_missed": sum(1 for r in Ball if r.get("entry_fill_status") == "missed"),
        "B_skipped": sum(1 for r in Ball if r.get("entry_fill_status") == "skipped"),
        "B_dir_flips": sum(1 for r in Ball if r.get("direction_changed")),
        "B_maker_entries": maker, "data_gap_excluded": data_gap,
        "data_gap_late_excluded_signals": dgl_signals, "forward_signals_total": n_total,
        "primary_cohort": "clean (DATA_GAP_LATE excluded)",
        "maker_posted": mk_posted, "maker_filled": mk_filled, "maker_missed": mk_missed,
        "maker_taker_fallback": mk_taker_fb,
        "maker_fill_rate": round(100 * mk_filled / mk_posted, 1) if mk_posted else None,
        "warnings": warnings,
    }


def forward_by_mode(db=None) -> list[dict]:
    """Forward A/B net-R delta per (asset_class, mode), joined from proposed_signals. Read-only."""
    conn = _conn(db)
    try:
        try:
            cols = {r[1] for r in conn.execute("PRAGMA table_info(paper_shadow_execution_outcomes)")}
            lane_filter = (" AND COALESCE(e.shadow_lane,'ab_main') != 'stocks_intraday_forward'"
                           if "shadow_lane" in cols else "")
            rows = [dict(r) for r in conn.execute(
                "SELECT e.branch, e.net_r, e.entry_fill_status, e.outcome_status, e.close_reason, "
                "p.asset_class AS asset_class, p.mode AS mode "
                "FROM paper_shadow_execution_outcomes e "
                "LEFT JOIN proposed_signals p ON e.signal_id = p.signal_id "
                "WHERE e.window='forward_since_activation'" + lane_filter +
                " AND NOT (lower(COALESCE(p.asset_class,''))='stocks' "
                "AND lower(COALESCE(p.mode,'')) IN ('swing','invest'))").fetchall()]
        except sqlite3.OperationalError:
            return []
    finally:
        conn.close()
    groups: dict[str, dict] = {}
    for r in rows:
        if r.get("outcome_status") == "no_data" or r.get("close_reason") == "data_gap":
            continue
        if r.get("entry_fill_status") != "filled":
            continue
        key = f"{r.get('asset_class') or '?'} {r.get('mode') or '?'}"
        g = groups.setdefault(key, {"mode": key, "a_r": 0.0, "b_r": 0.0, "a_t": 0, "b_t": 0})
        if r["branch"] == "old_paper":
            g["a_r"] += (r.get("net_r") or 0); g["a_t"] += 1
        else:
            g["b_r"] += (r.get("net_r") or 0); g["b_t"] += 1
    out = []
    for g in groups.values():
        g["a_r"] = round(g["a_r"], 2); g["b_r"] = round(g["b_r"], 2)
        g["delta_r"] = round(g["b_r"] - g["a_r"], 2)
        out.append(g)
    out.sort(key=lambda g: g["delta_r"], reverse=True)
    return out


def promotion_gate(db=None) -> dict:
    """Evaluate (NOT execute) the promotion gate. Returns verdict NOT_READY/READY + per-criterion."""
    fq = forward_quality(db)
    if not fq.get("available"):
        return {"verdict": "NOT_READY", "reason": "no forward data", "criteria": [], "thresholds": GATE}
    A, B = fq["A"], fq["B"]
    crit = [
        {"name": "forward_days >= 14", "ok": (fq.get("forward_days") or 0) >= GATE["min_forward_days"],
         "value": fq.get("forward_days")},
        {"name": "forward_trades >= 60", "ok": B["trades"] >= GATE["min_forward_trades"], "value": B["trades"]},
        {"name": "B net R > A net R (after fees)", "ok": B["net_r"] > A["net_r"],
         "value": f"{B['net_r']} vs {A['net_r']}"},
        {"name": "B net $ > A net $ (after fees)", "ok": B["net_usd"] > A["net_usd"],
         "value": f"{B['net_usd']} vs {A['net_usd']}"},
        {"name": "B drawdown not materially worse", "ok": B["max_drawdown_r"] >= A["max_drawdown_r"] - GATE["max_drawdown_worse_r"],
         "value": f"{B['max_drawdown_r']} vs {A['max_drawdown_r']}"},
        {"name": "no excessive DATA_GAP", "ok": not any("DATA_GAP" in w for w in fq["warnings"]),
         "value": fq["data_gap_excluded"]},
    ]
    ready = all(c["ok"] for c in crit)
    return {"verdict": "READY" if ready else "NOT_READY", "executed": False,
            "note": "Gate is evaluation-only; promotion requires explicit operator sign-off. "
                    "Backfill never counts.", "criteria": crit, "thresholds": GATE,
            "warnings": fq["warnings"]}


def _dd_r(rows) -> float:
    """Running-sum max drawdown in R over chronological fill order."""
    peak = dd = run = 0.0
    for r in sorted(rows, key=lambda x: x.get("entry_fill_time") or ""):
        run += (r.get("net_r") or 0)
        peak = max(peak, run)
        dd = min(dd, run - peak)
    return round(dd, 3)


def promotion_readiness_by_mode(db=None) -> dict:
    """READ-ONLY per (asset_class, mode) promotion-readiness read-model. Evaluates — never executes.

    Verdict scale:
      * READY_FOR_OPERATOR_REVIEW — every gate criterion passes (still needs explicit operator
        sign-off; this is NOT auto-promotion).
      * WATCH — B beats A on BOTH net R and net USD and fee-profile integrity holds, but the forward
        window / sample / data-gap quality is not yet sufficient.
      * NOT_READY — B does not beat A, integrity broken, or nothing to judge.

    DATA_GAP_LATE signals are excluded from the A/B edge (dirty entry timestamp) but still counted in
    the data-gap share. fee_profile_integrity_ok = the group's rows all used the correct per-asset
    profile and carry no stale_cost_model rows (item 1/2). Live/auto-live remain locked.
    """
    conn = _conn(db)
    try:
        try:
            cols = {r[1] for r in conn.execute("PRAGMA table_info(paper_shadow_execution_outcomes)")}
            lane_filter = (" AND COALESCE(e.shadow_lane,'ab_main') != 'stocks_intraday_forward'"
                           if "shadow_lane" in cols else "")
            rows = [dict(r) for r in conn.execute(
                "SELECT e.signal_id, e.branch, e.net_r, e.net_pnl_usdt, e.entry_fill_status, "
                "e.entry_fill_time, e.fee_profile, e.cost_model_status, e.asset_class AS e_asset, "
                "p.asset_class AS p_asset, p.mode AS mode "
                "FROM paper_shadow_execution_outcomes e "
                "LEFT JOIN proposed_signals p ON e.signal_id = p.signal_id "
                "WHERE e.window='forward_since_activation'" + lane_filter +
                " AND NOT (lower(COALESCE(p.asset_class,''))='stocks' "
                "AND lower(COALESCE(p.mode,'')) IN ('swing','invest'))").fetchall()]
        except sqlite3.OperationalError:
            return {"available": False, "reason": "shadow lane not populated", "modes": []}
        act = conn.execute("SELECT v FROM paper_shadow_meta WHERE k='activated_at'").fetchone()
        activated = act[0] if act else None
        pre = conn.execute("SELECT v FROM paper_shadow_meta WHERE k='preentry_v2_activated_at'").fetchone()
        preentry_v2_activated = pre[0] if pre else None
        try:
            dgl = {r[0] for r in conn.execute(
                "SELECT signal_id FROM entry_latency_audit WHERE cause='DATA_GAP_LATE'")}
        except sqlite3.OperationalError:
            dgl = set()
    finally:
        conn.close()
    days = None
    if activated:
        import datetime as _dt
        try:
            days = (_dt.datetime.now(_dt.timezone.utc) - _dt.datetime.fromisoformat(activated)).days
        except Exception:
            days = None
    crypto_days = days
    if preentry_v2_activated:
        import datetime as _dt
        try:
            crypto_days = (_dt.datetime.now(_dt.timezone.utc) -
                           _dt.datetime.fromisoformat(preentry_v2_activated)).days
        except Exception:
            crypto_days = None
    groups: dict[str, dict] = {}
    for r in rows:
        ac = str(r.get("e_asset") or r.get("p_asset") or "?")
        mode = str(r.get("mode") or "?")
        g = groups.setdefault(f"{ac}|{mode}", {
            "asset_class": ac, "mode": mode, "A": [], "B": [],
            "sig_ids": set(), "dgl_ids": set(), "profiles": set(), "stale": 0})
        g["sig_ids"].add(r["signal_id"])
        if r["signal_id"] in dgl:
            g["dgl_ids"].add(r["signal_id"])
        if r.get("cost_model_status") == "stale_cost_model":
            g["stale"] += 1
        if r.get("fee_profile"):
            g["profiles"].add(r["fee_profile"])
        if r["signal_id"] in dgl or r.get("entry_fill_status") != "filled":
            continue                                       # edge = clean, filled cohort only
        (g["A"] if r["branch"] == "old_paper" else g["B"]).append(r)
    out = []
    for g in groups.values():
        A, B = g["A"], g["B"]
        a_r = round(sum((x.get("net_r") or 0) for x in A), 3)
        b_r = round(sum((x.get("net_r") or 0) for x in B), 3)
        a_usd = round(sum((x.get("net_pnl_usdt") or 0) for x in A), 2)
        b_usd = round(sum((x.get("net_pnl_usdt") or 0) for x in B), 2)
        n_sig = len(g["sig_ids"]) or 1
        dgl_share = round(len(g["dgl_ids"]) / n_sig, 3)
        expected = STOCK_FEE_PROFILE if _asset_is_stock(g["asset_class"]) else CRYPTO_FEE_PROFILE
        days_for_mode = days if _asset_is_stock(g["asset_class"]) else crypto_days
        integrity = (g["stale"] == 0) and (not g["profiles"] or g["profiles"] <= {expected})
        crit = {
            "forward_days>=14": (days_for_mode or 0) >= GATE["min_forward_days"],
            "forward_trades>=60": len(B) >= GATE["min_forward_trades"],
            "B_net_usd>A_net_usd": b_usd > a_usd,
            "B_net_r>A_net_r": b_r > a_r,
            "data_gap_late<=30%": dgl_share <= GATE["max_data_gap_share"],
            "fee_profile_integrity_ok": bool(integrity),
        }
        b_beats_a = crit["B_net_usd>A_net_usd"] and crit["B_net_r>A_net_r"]
        # WATCH = promising (B beats A, integrity + data quality OK) but not enough forward window /
        # sample yet. A high DATA_GAP_LATE share or broken fee integrity is NEVER just "watch" — it
        # blocks to NOT_READY (a data/accounting problem, not merely "too early").
        if all(crit.values()):
            verdict = "READY_FOR_OPERATOR_REVIEW"
        elif b_beats_a and integrity and crit["data_gap_late<=30%"]:
            verdict = "WATCH"
        else:
            verdict = "NOT_READY"
        out.append({
            "asset_class": g["asset_class"], "mode": g["mode"], "forward_days": days_for_mode,
            "forward_trades": len(B), "A_net_r": a_r, "B_net_r": b_r,
            "A_net_usd": a_usd, "B_net_usd": b_usd,
            "delta_net_r": round(b_r - a_r, 3), "delta_net_usd": round(b_usd - a_usd, 2),
            "B_max_drawdown_r": _dd_r(B), "A_max_drawdown_r": _dd_r(A),
            "data_gap_late_share": dgl_share, "fee_profile_integrity_ok": bool(integrity),
            "fee_profile_expected": expected, "fee_profiles_seen": sorted(g["profiles"]),
            "stale_cost_model_rows": g["stale"], "criteria": crit, "verdict": verdict,
        })
    out.sort(key=lambda g: (g["asset_class"], g["mode"]))
    return {"available": True, "forward_days": days, "crypto_preentry_v2_forward_days": crypto_days,
            "crypto_preentry_v2_activated_at": preentry_v2_activated, "gate": GATE, "executed": False,
            "note": "READY_FOR_OPERATOR_REVIEW is NOT auto-promotion — it requires explicit operator "
                    "sign-off. Live / auto-live / manual-live remain locked; nothing is executed.",
            "modes": out}
