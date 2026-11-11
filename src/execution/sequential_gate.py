"""Move 2 — Sequential promotion gate (Wald SPRT / early-stopping). READ-ONLY, evaluation-only.

The fixed gate (paper_shadow_monitor.GATE) makes every mode wait a FULL window — ≥14 forward
days AND ≥60 forward trades — before it will even say READY. That is slow: a mode that is
already clearly better (or clearly not-better) than the old logic still sits in "NOT_READY"
until the calendar/sample wall is reached.

This module replaces the wall with a SEQUENTIAL test on the PAIRED per-signal forward edge
(d_i = B.net_r − A.net_r, same signal under new vs old logic, in chronological fill order):

  H0: E[d] ≤ 0  (new logic is NOT better after fees)
  H1: E[d] ≥ min_edge_r  (new logic beats old by at least a meaningful margin)

Wald's SPRT accumulates the log-likelihood ratio and stops the moment it crosses a boundary:
  * SEQ_ACCEPT  — LLR ≥ ln((1−β)/α): edge confirmed EARLY (needs operator sign-off; NOT auto-promote)
  * SEQ_REJECT  — LLR ≤ ln(β/(1−α)): no edge; stop the forward test early, don't keep waiting
  * SEQ_CONTINUE — between boundaries: keep accumulating

Guards (truncated SPRT — practical trading safety):
  * ACCEPT needs ≥ min_n_accept paired obs (a couple of lucky trades must not promote).
  * REJECT needs ≥ min_n_reject paired obs (don't kill on 2 noisy trades).
  * At max_n the sequential test truncates and defers to the fixed gate's decision, so the
    worst-case wait is never longer than today — SPRT only ever shortens it.

Only FORWARD, clean (DATA_GAP_LATE excluded), FILLED, PAIRED rows count. Backfill never counts.
Reads paper_shadow_execution_outcomes; writes ONLY the read-model table sequential_promotion_gate
(+ optional report). Never promotes, never touches final_r / proposed_signals / live.
"""

from __future__ import annotations

import math
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.execution.entry_mode_calibration import load_calibration_config
from src.execution.paper_shadow_monitor import GATE, promotion_gate

_DEFAULTS = {
    "enabled": True, "alpha": 0.05, "beta": 0.20, "min_edge_r": 0.10,
    "min_n_accept": 20, "min_n_reject": 10, "max_n": 60,
}


def _cfg() -> dict:
    try:
        c = (load_calibration_config() or {}).get("sequential_gate") or {}
    except Exception:
        c = {}
    return {**_DEFAULTS, **{k: c[k] for k in _DEFAULTS if k in c}}


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------- pure SPRT
def sprt(diffs: list[float], *, alpha: float, beta: float, min_edge_r: float,
         min_n_accept: int, min_n_reject: int) -> dict:
    """Gaussian Wald SPRT on the mean of `diffs` (H0 μ=0 vs H1 μ=min_edge_r), plug-in σ.

    Returns {n, mean, sigma, llr, upper, lower, decision}. decision ∈
    {SEQ_ACCEPT, SEQ_REJECT, SEQ_CONTINUE}. Distribution-free companion (sign test) not used for
    the decision but the mean/σ are reported so a human can sanity-check the normal approximation.
    """
    n = len(diffs)
    upper = math.log((1.0 - beta) / alpha)          # accept-H1 boundary (>0)
    lower = math.log(beta / (1.0 - alpha))          # accept-H0 boundary (<0)
    out = {"n": n, "mean": None, "sigma": None, "llr": None,
           "upper": round(upper, 4), "lower": round(lower, 4), "decision": "SEQ_CONTINUE"}
    if n < 2:
        return out
    mean = sum(diffs) / n
    var = sum((d - mean) ** 2 for d in diffs) / (n - 1)
    sigma = math.sqrt(var)
    out["mean"] = round(mean, 4)
    out["sigma"] = round(sigma, 4)
    if sigma <= 0:
        # zero variance: decide by the sign of the (constant) edge vs the hypotheses
        if mean >= min_edge_r and n >= min_n_accept:
            out["decision"] = "SEQ_ACCEPT"
        elif mean <= 0 and n >= min_n_reject:
            out["decision"] = "SEQ_REJECT"
        return out
    mu0, mu1 = 0.0, float(min_edge_r)
    # cumulative Gaussian log-likelihood ratio for known σ
    llr = (mu1 - mu0) / (sigma ** 2) * (sum(diffs) - n * (mu1 + mu0) / 2.0)
    out["llr"] = round(llr, 4)
    if llr >= upper and n >= min_n_accept:
        out["decision"] = "SEQ_ACCEPT"
    elif llr <= lower and n >= min_n_reject:
        out["decision"] = "SEQ_REJECT"
    return out


# ---------------------------------------------------------------- data (read-only)
def _paired_diffs_by_mode(db=None, *, source: str = "primary") -> dict[tuple, list[dict]]:
    """Per (asset_class, mode): list of paired rows {signal_id, d_r, d_usd, t} in fill-time order.

    A pair exists only when BOTH old_paper and new_logic_shadow FILLED the same forward signal and
    the signal is not in the DATA_GAP_LATE cohort.

    source='primary' → the authoritative live rolling-cache lane (paper_shadow_execution_outcomes).
    source='wide'    → the Move-3 deep-history wide-net lane (paper_shadow_wide_outcomes): bigger,
                       faster-accumulating, PROVISIONAL (not the authoritative promotion evidence)."""
    from src.config import load_config
    cfg = load_config()
    conn = sqlite3.connect(f"file:{db or cfg.db_path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        if source == "wide":
            try:
                rows = [dict(r) for r in conn.execute(
                    "SELECT signal_id, branch, net_r, net_pnl_usdt, entry_fill_status, "
                    "entry_fill_time, asset_class AS e_asset, asset_class AS p_asset, mode "
                    "FROM paper_shadow_wide_outcomes WHERE window='forward_since_activation'").fetchall()]
            except sqlite3.OperationalError:
                return {}
            dgl = set()   # wide lane is deep-history clean; no DATA_GAP_LATE cohort
        else:
            try:
                shadow_cols = {r[1] for r in conn.execute(
                    "PRAGMA table_info(paper_shadow_execution_outcomes)")}
                lane_filter = (" AND COALESCE(e.shadow_lane,'ab_main') != 'stocks_intraday_forward'"
                               if "shadow_lane" in shadow_cols else "")
                rows = [dict(r) for r in conn.execute(
                    "SELECT e.signal_id, e.branch, e.net_r, e.net_pnl_usdt, e.entry_fill_status, "
                    "e.entry_fill_time, e.asset_class AS e_asset, p.asset_class AS p_asset, p.mode AS mode "
                    "FROM paper_shadow_execution_outcomes e "
                    "LEFT JOIN proposed_signals p ON e.signal_id = p.signal_id "
                    "WHERE e.window='forward_since_activation'" + lane_filter).fetchall()]
            except sqlite3.OperationalError:
                return {}
            try:
                dgl = {r[0] for r in conn.execute(
                    "SELECT signal_id FROM entry_latency_audit WHERE cause='DATA_GAP_LATE'")}
            except sqlite3.OperationalError:
                dgl = set()
    finally:
        conn.close()

    # Index by signal_id/branch. old (A) requires a FILL; new (B) keeps ALL statuses so a deliberate
    # SKIP can be scored as an avoided-trade decision (books 0R).
    a: dict[str, dict] = {}
    b: dict[str, dict] = {}
    meta: dict[str, tuple] = {}
    for r in rows:
        if r["signal_id"] in dgl:
            continue
        ac = str(r.get("e_asset") or r.get("p_asset") or "?")
        mode = str(r.get("mode") or "?")
        if r["branch"] == "old_paper":
            if r.get("entry_fill_status") != "filled":
                continue
            a[r["signal_id"]] = r
            meta[r["signal_id"]] = (ac, mode, r.get("entry_fill_time") or "")
        elif r["branch"] == "new_logic_shadow":
            b[r["signal_id"]] = r

    groups: dict[tuple, list[dict]] = {}
    if source == "wide":
        # WITH-AVOIDED edge: every signal the OLD logic took is a decision for the new logic —
        # it either took it (filled → its realized edge) or deliberately SKIPPED it (books 0R,
        # i.e. it avoided old's trade). MISSED (post-only fill failure) is ambiguous → excluded.
        # This widens the sample from "both filled" to "every old-filled decision".
        for sid, arow in a.items():
            ac, mode, t = meta[sid]
            brow = b.get(sid)
            bstatus = (brow or {}).get("entry_fill_status")
            if bstatus == "filled":
                b_r, b_usd = (brow.get("net_r") or 0.0), (brow.get("net_pnl_usdt") or 0.0)
            elif bstatus == "skipped" or brow is None:
                b_r, b_usd = 0.0, 0.0                # new logic avoided the trade
            else:
                continue                             # missed → ambiguous, drop
            groups.setdefault((ac, mode), []).append(
                {"signal_id": sid, "d_r": b_r - (arow.get("net_r") or 0.0),
                 "d_usd": b_usd - (arow.get("net_pnl_usdt") or 0.0), "t": t})
    else:
        for sid in set(a) & set(b):                 # authoritative lane: executed-vs-executed only
            if b[sid].get("entry_fill_status") != "filled":
                continue
            ac, mode, t = meta[sid]
            d_r = (b[sid].get("net_r") or 0.0) - (a[sid].get("net_r") or 0.0)
            d_usd = (b[sid].get("net_pnl_usdt") or 0.0) - (a[sid].get("net_pnl_usdt") or 0.0)
            groups.setdefault((ac, mode), []).append(
                {"signal_id": sid, "d_r": d_r, "d_usd": d_usd, "t": t})
    for key in groups:
        groups[key].sort(key=lambda x: x["t"])      # chronological for the sequential test
    return groups


_DDL = """
CREATE TABLE IF NOT EXISTS sequential_promotion_gate (
  generated_at TEXT, asset_class TEXT, mode TEXT, n_pairs INTEGER, mean_edge_r REAL, sigma_r REAL,
  sum_edge_r REAL, sum_edge_usd REAL, llr REAL, upper REAL, lower REAL, decision TEXT,
  fixed_gate_verdict TEXT, PRIMARY KEY (asset_class, mode)
);
"""


def refresh(*, db: str | None = None, persist: bool = True, source: str = "primary",
            write_report_file: bool | None = None, report_dir: str | None = None,
            now_iso: str | None = None) -> dict[str, Any]:
    """Sequential-gate verdicts per (asset_class, mode). Read-only source; writes ONLY the
    sequential_promotion_gate read-model table (+ optional report). Never promotes.

    source='primary' (default) → authoritative live lane. source='wide' → Move-3 deep-history
    wide-net lane (provisional, bigger sample)."""
    from src.config import load_config
    cfg_proj = load_config()
    p = _cfg()
    path = db or str(cfg_proj.db_path)
    groups = _paired_diffs_by_mode(db, source=source)
    generated_at = (now_iso or datetime.now(timezone.utc).isoformat())

    # fixed-gate verdict is aggregate (not per-mode) — reuse it as the truncation fallback signal
    try:
        fixed = promotion_gate(db).get("verdict")
    except Exception:
        fixed = None

    out_rows: list[dict] = []
    for (ac, mode), items in sorted(groups.items()):
        diffs = [it["d_r"] for it in items]
        s = sprt(diffs, alpha=p["alpha"], beta=p["beta"], min_edge_r=p["min_edge_r"],
                 min_n_accept=p["min_n_accept"], min_n_reject=p["min_n_reject"])
        decision = s["decision"]
        truncated = False
        if decision == "SEQ_CONTINUE" and s["n"] >= int(p["max_n"]):
            truncated = True
            decision = "TRUNCATED_" + (fixed or "NOT_READY")   # defer to the fixed gate at max_n
        out_rows.append({
            "asset_class": ac, "mode": mode, "n_pairs": s["n"],
            "mean_edge_r": s["mean"], "sigma_r": s["sigma"],
            "sum_edge_r": round(sum(it["d_r"] for it in items), 3),
            "sum_edge_usd": round(sum(it["d_usd"] for it in items), 2),
            "llr": s["llr"], "upper": s["upper"], "lower": s["lower"],
            "decision": decision, "truncated": truncated, "fixed_gate_verdict": fixed,
        })

    table = "sequential_promotion_gate" if source != "wide" else "sequential_promotion_gate_wide"
    result = {"db_path": str(path), "generated_at": generated_at, "persisted": bool(persist),
              "source": source, "table": table, "params": p, "fixed_gate": GATE,
              "fixed_gate_verdict": fixed, "modes_evaluated": len(out_rows), "modes": out_rows}

    persisted_rows = None
    if persist:
        wconn = sqlite3.connect(path)
        try:
            wconn.execute(f"DROP TABLE IF EXISTS {table}")
            wconn.execute(_DDL.replace("sequential_promotion_gate", table))
            for r in out_rows:
                wconn.execute(
                    f"INSERT OR REPLACE INTO {table} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (generated_at, r["asset_class"], r["mode"], r["n_pairs"], r["mean_edge_r"],
                     r["sigma_r"], r["sum_edge_r"], r["sum_edge_usd"], r["llr"], r["upper"],
                     r["lower"], r["decision"], r["fixed_gate_verdict"]))
            wconn.commit()
            persisted_rows = wconn.execute(
                f"SELECT count(*), max(generated_at) FROM {table}").fetchone()
        finally:
            wconn.close()
    result["matches_persisted_table"] = bool(
        persist and persisted_rows and persisted_rows[0] == len(out_rows)
        and persisted_rows[1] == generated_at)

    do_report = (db is None) if write_report_file is None else bool(write_report_file)
    if do_report:
        write_report(result, out_dir=report_dir)
    return result


def render_markdown(result: dict) -> str:
    mark = "PERSISTED (read-model table written)" if result.get("persisted") else "DRY-RUN"
    p = result.get("params", {})
    src = result.get("source", "primary")
    src_line = ("- source: **PRIMARY** — authoritative live rolling-cache lane, executed-vs-executed pairs"
                if src != "wide" else
                "- source: **WIDE (provisional)** — Move-3 deep-history lane, WITH-AVOIDED edge (every "
                "old-filled decision; new-logic SKIP books 0R = avoided trade). Bigger/faster sample; "
                "NOT the authoritative promotion evidence.")
    L = [f"# Sequential Promotion Gate — SPRT early-stopping ({src}, read-model, evaluation-only)", "",
         f"- db_path: `{result.get('db_path')}`",
         f"- generated_at: `{result['generated_at']}`  ·  **{mark}**",
         src_line,
         f"- matches persisted table: **{str(bool(result.get('matches_persisted_table'))).lower()}**",
         f"- test: paired per-signal edge d = B.net_r − A.net_r; H0 μ≤0 vs H1 μ≥{p.get('min_edge_r')}R; "
         f"α={p.get('alpha')} β={p.get('beta')}; ACCEPT needs n≥{p.get('min_n_accept')}, "
         f"REJECT needs n≥{p.get('min_n_reject')}, truncate at n={p.get('max_n')}",
         f"- fixed-gate fallback verdict (aggregate): **{result.get('fixed_gate_verdict')}**", "",
         "> **SEQ_ACCEPT is NOT auto-promotion** — it means the forward edge crossed the accept "
         "boundary EARLY and is ready for operator review sooner than the fixed 14d/60-trade window. "
         "Promotion still requires explicit operator sign-off. Backfill never counts; live locked.", "",
         "| asset | mode | n pairs | mean edge R | ΣR | Σ$ | LLR | [lower, upper] | decision |",
         "|---|---|--:|--:|--:|--:|--:|:--:|:--|"]
    order = {"SEQ_ACCEPT": 0, "SEQ_CONTINUE": 1}
    for r in sorted(result.get("modes", []), key=lambda r: (order.get(r["decision"], 2), r["asset_class"], r["mode"])):
        me = "" if r["mean_edge_r"] is None else f"{r['mean_edge_r']:+.3f}"
        llr = "" if r["llr"] is None else f"{r['llr']:+.2f}"
        L.append(f"| {r['asset_class']} | {r['mode']} | {r['n_pairs']} | {me} | {r['sum_edge_r']:+.2f} | "
                 f"{r['sum_edge_usd']:+.0f} | {llr} | [{r['lower']}, {r['upper']}] | **{r['decision']}** |")
    L.append("")
    L.append("Legend: **SEQ_ACCEPT** edge confirmed early (→ operator review) · **SEQ_REJECT** no edge, "
             "stop early · **SEQ_CONTINUE** keep accumulating · **TRUNCATED_…** hit n_max, deferred to the "
             "fixed gate.")
    return "\n".join(L)


def write_report(result: dict, out_dir: str | None = None) -> str:
    base = Path(out_dir) if out_dir else (_root() / "reports")
    base.mkdir(parents=True, exist_ok=True)
    name = "SEQUENTIAL_GATE.md" if result.get("source") != "wide" else "SEQUENTIAL_GATE_WIDE.md"
    out = base / name
    with out.open("w", encoding="utf-8") as fh:
        fh.write(render_markdown(result))
    return str(out)


__all__ = ["sprt", "refresh", "render_markdown", "write_report"]
