"""Entry-mode calibration read-model (PAPER / READ-ONLY / ACCOUNTING ONLY).

Turns the coarse `new_logic_shadow` branch into a precise per-slice forward-testing
map. It reads existing paper/shadow evidence and produces, per

    asset_class x trade_mode x entry_mode x branch x window (forward|backfill)

a full metric set (USD-authoritative), a paired old_paper-vs-new_logic_shadow delta,
Model-F profit-protection metrics (from the authoritative `paper_execution_outcomes`),
and a config-driven verdict per slice.

STRICT GUARDRAILS:
  - Reads only. Writes ONLY its own read-model tables (entry_mode_calibration_*).
  - NEVER writes proposed_signals / signal_outcomes / final_r; no live/orders;
    no scoring/routing/actionability/Telegram change.
  - Decisions are made ONLY on window == 'forward_since_activation'.
    'historical_backfill' is reported separately and is HYPOTHESIS-ONLY.
  - USD PnL is authoritative; R is auxiliary.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from src.execution.paper_entry_mode_policy import disabled_shadow_reason, paper_promotion_reason

RISK_USD = 25.0  # EQUITY 5000 * 0.5% — mirrors the paper book (auxiliary USD for R-only deltas)

BRANCH_OLD = "old_paper"
BRANCH_NEW = "new_logic_shadow"
FORWARD = "forward_since_activation"
BACKFILL = "historical_backfill"

VERDICTS = (
    "DISABLED_BY_POLICY", "UNSUPPORTED_LEGACY", "SKIP_POLICY", "NEED_MORE_DATA",
    "DATA_QUALITY_BLOCKED", "INSUFFICIENT_CLEAN_SAMPLE", "KEEP_SHADOW", "WATCH",
    "PAPER_CANDIDATE", "PROMOTE_REVIEW", "DISABLE",
)
# Verdicts that BLOCK any good/bad conclusion (data-quality / insufficient clean evidence). A slice
# with one of these must never be read as promotion/disable evidence.
BLOCKED_VERDICTS = {"DATA_QUALITY_BLOCKED", "INSUFFICIENT_CLEAN_SAMPLE", "UNSUPPORTED_LEGACY",
                    "SKIP_POLICY", "DISABLED_BY_POLICY"}

# Legacy / unsupported modes: retired stocks swing + invest frameworks. Kept in a report appendix,
# never promotable, never summed with the active paper/shadow modes.
LEGACY_UNSUPPORTED = {("stocks", "swing"), ("stocks", "invest")}
SKIP_ENTRY_MODES = {"NO_CHASE_SKIP"}   # not an economic entry mode -> skip-policy diagnostics only


def _is_legacy_unsupported(asset_class: str, mode: str, entry_mode: str = "") -> bool:
    a = str(asset_class or "").lower()
    m = str(mode or "").lower()
    if a.startswith("stock") and m == "swing" and str(entry_mode or "").upper() == "EVENT_RS_PULLBACK":
        return False
    return (a.startswith("stock") and m in ("swing", "invest"))


def _is_skip_mode(entry_mode: str) -> bool:
    return str(entry_mode or "").upper() in SKIP_ENTRY_MODES


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_calibration_config() -> dict[str, Any]:
    p = _root() / "config" / "entry_mode_calibration.yaml"
    try:
        with p.open("r", encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    except Exception:
        return {}


def _db_path(db: str | None) -> str:
    if db:
        return db
    from src.config import load_config
    return str(load_config().db_path)


def _pct(vals: list[float], q: float) -> float | None:
    if not vals:
        return None
    s = sorted(vals)
    if len(s) == 1:
        return round(s[0], 3)
    idx = min(len(s) - 1, max(0, int(round(q * (len(s) - 1)))))
    return round(s[idx], 3)


def _max_drawdown(seq_usd: list[float]) -> float:
    """Max peak-to-trough drawdown of a cumulative-PnL series (positive number)."""
    peak = 0.0
    cum = 0.0
    dd = 0.0
    for x in seq_usd:
        cum += x
        peak = max(peak, cum)
        dd = max(dd, peak - cum)
    return round(dd, 4)


def _table_exists(conn, name: str) -> bool:
    r = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)).fetchone()
    return bool(r)


# --------------------------------------------------------------------------- load
def _activation(conn) -> str | None:
    try:
        r = conn.execute("SELECT v FROM paper_shadow_meta WHERE k='activated_at'").fetchone()
        return r[0] if r else None
    except sqlite3.OperationalError:
        return None


def _load_latency_cause(conn) -> dict[str, dict]:
    out: dict[str, dict] = {}
    if not _table_exists(conn, "entry_latency_audit"):
        return out
    for row in conn.execute(
        "SELECT signal_id, cause, recorded_latency_min FROM entry_latency_audit"):
        out[row[0]] = {"cause": row[1], "latency_min": row[2]}
    return out


def _load_shadow_rows(conn) -> list[dict]:
    if not _table_exists(conn, "paper_shadow_execution_outcomes"):
        return []
    shadow_cols = {r[1] for r in conn.execute("PRAGMA table_info(paper_shadow_execution_outcomes)")}
    version_sel = "s.entry_mode_version" if "entry_mode_version" in shadow_cols else "NULL AS entry_mode_version"
    lane_filter = (" AND COALESCE(s.shadow_lane,'ab_main') != 'stocks_intraday_forward'"
                   if "shadow_lane" in shadow_cols else "")
    sql = """
      SELECT s.signal_id, s.branch, s.window, s.entry_mode, s.asset_class,
             p.mode AS trade_mode, p.market_regime, s.playbook,
             p.news_supported, s.entry_fill_status, s.skipped_shadow_reason,
             s.net_r, s.net_pnl_usdt, s.gross_r, s.fees_usdt, s.slippage_usdt,
             s.mfe_r, s.mae_r, s.missed_move_r, s.tp1_r, s.close_reason, s.outcome_status,
             s.maker_entry_posted, s.maker_entry_filled, s.maker_entry_missed,
             s.taker_fallback_used, s.maker_tp_fills, s.cost_model_status,
             s.entry_fill_time, s.fee_profile, s.created_at, """ + version_sel + """
      FROM paper_shadow_execution_outcomes s
      LEFT JOIN proposed_signals p ON p.signal_id = s.signal_id
          WHERE 1=1
    """ + lane_filter
    cols = [d[0] for d in conn.execute(sql).description]
    rows = [dict(zip(cols, r)) for r in conn.execute(sql).fetchall()]
    # Crypto B rows produced before the pre-entry v2 lane used a post-entry
    # label. Keep them in the database for audit, but never let them influence
    # calibration or promotion evidence.
    return [r for r in rows if not (
        str(r.get("asset_class") or "").lower() == "crypto"
        and str(r.get("branch") or "") == BRANCH_NEW
        and str(r.get("entry_mode_version") or "") != "preentry_v2"
    )]


def _load_protection_by_signal(conn) -> dict[str, dict]:
    """Authoritative Model-F protection keyed by signal_id (so protection metrics can be aggregated
    per SLICE using the slice's own signal_ids — never mixing forward/backfill or branches).

    ``evidence_class`` (2026-07-09 Model-F freeze) is read defensively — a DB/fixture predating the
    freeze migration simply won't have the column; every row then falls back to unclassified rather
    than the whole protection lookup silently going empty."""
    out: dict[str, dict] = {}
    if not _table_exists(conn, "paper_execution_outcomes"):
        return out
    cols_present = {r[1] for r in conn.execute("PRAGMA table_info(paper_execution_outcomes)")}
    has_evidence = "evidence_class" in cols_present
    sql = ("SELECT signal_id, paper_execution_r, touch_r, protection_armed, lock_armed, giveback, "
           "close_reason, highest_tp_touched, same_candle_ambiguous, risk_model"
           + (", evidence_class" if has_evidence else "")
           + " FROM paper_execution_outcomes WHERE paper_execution_r IS NOT NULL")
    try:
        cols = [d[0] for d in conn.execute(sql).description]
        for r in conn.execute(sql).fetchall():
            d = dict(zip(cols, r))
            if not has_evidence:
                d["evidence_class"] = None
            out[str(d["signal_id"])] = d  # latest wins if duplicated
    except sqlite3.OperationalError:
        return {}
    return out


# --------------------------------------------------------------------------- aggregate
def _slice_metrics(rows: list[dict], latency: dict[str, dict]) -> dict[str, Any]:
    n = len(rows)
    # DATA_GAP_LATE = dirty entry timestamp (a coverage artifact, not a real fill). It is NEVER
    # counted as edge: PnL / PF / winrate / drawdown / promotion metrics are computed on the CLEAN
    # cohort ONLY. Dirty rows are retained solely for two-cohort diagnostics.
    def _is_dgl(r):
        # dirty = DATA_GAP_LATE (per-signal latency) OR the materialized coverage flag says not-clean.
        if r.get("is_clean_for_edge") == 0:
            return True
        return latency.get(r["signal_id"], {}).get("cause") == "DATA_GAP_LATE"
    clean_rows = [r for r in rows if not _is_dgl(r)]
    dirty_rows = [r for r in rows if _is_dgl(r)]
    dgl = len(dirty_rows)
    # --- edge cohort = CLEAN only (dirty excluded) ---
    filled = [r for r in clean_rows if r.get("entry_fill_status") == "filled"]
    skipped = [r for r in clean_rows if r.get("entry_fill_status") == "skipped"]
    missed = [r for r in clean_rows if r.get("entry_fill_status") == "missed"]
    closed = [r for r in filled if r.get("net_pnl_usdt") is not None
              and r.get("outcome_status") in ("closed", None)]
    dirty_closed = sum(1 for r in dirty_rows if r.get("entry_fill_status") == "filled"
                       and r.get("net_pnl_usdt") is not None
                       and r.get("outcome_status") in ("closed", None))
    # order closed by entry time for drawdown
    closed_sorted = sorted(closed, key=lambda r: str(r.get("entry_fill_time") or r.get("created_at") or ""))
    net_usd_seq = [float(r["net_pnl_usdt"]) for r in closed_sorted]
    net_r_seq = [float(r["net_r"]) for r in closed_sorted if r.get("net_r") is not None]

    wins = [x for x in net_usd_seq if x > 0]
    losses = [x for x in net_usd_seq if x < 0]
    gross_profit = sum(wins)
    gross_loss = abs(sum(losses))
    fees = sum(float(r["fees_usdt"]) for r in filled if r.get("fees_usdt") is not None)
    slip = sum(float(r["slippage_usdt"]) for r in filled if r.get("slippage_usdt") is not None)
    total_cost = round(fees + slip, 4)
    gross_pos = sum(float(r["gross_r"]) for r in closed if (r.get("gross_r") or 0) > 0) * RISK_USD
    lat_vals = [latency[r["signal_id"]]["latency_min"] for r in rows
                if r["signal_id"] in latency and latency[r["signal_id"]].get("latency_min") is not None]

    def rate(cnt, denom):
        return round(cnt / denom, 4) if denom else 0.0

    m = {
        "trades": n,
        "filled": len(filled),
        "skipped": len(skipped),
        "missed": len(missed),
        "fill_rate": rate(len(filled), n),
        "missed_entry_rate": rate(len(missed), n),
        "closed": len(closed),
        "net_pnl_usd": round(sum(net_usd_seq), 4),
        "net_r_sum": round(sum(net_r_seq), 4),
        "net_r_avg": round(sum(net_r_seq) / len(net_r_seq), 4) if net_r_seq else None,
        "gross_r_sum": round(sum(float(r["gross_r"]) for r in closed if r.get("gross_r") is not None), 4),
        "fees_usd": round(fees, 4),
        "slippage_usd": round(slip, 4),
        "total_cost_usd": total_cost,
        "cost_to_gross_profit": round(total_cost / gross_pos, 4) if gross_pos > 0 else None,
        "winrate": rate(len(wins), len(closed)),
        "profit_factor": round(gross_profit / gross_loss, 4) if gross_loss > 0 else (
            None if gross_profit == 0 else float("inf")),
        "avg_win_usd": round(sum(wins) / len(wins), 4) if wins else None,
        "avg_loss_usd": round(sum(losses) / len(losses), 4) if losses else None,
        "max_drawdown_usd": _max_drawdown(net_usd_seq),
        "max_drawdown_r": _max_drawdown(net_r_seq),
        "tp1_hit_rate": rate(sum(1 for r in closed if (r.get("maker_tp_fills") or 0) >= 1), len(closed)),
        "tp3_runner_rate": rate(sum(1 for r in closed if (r.get("maker_tp_fills") or 0) >= 3), len(closed)),
        "stop_rate": rate(sum(1 for r in closed if str(r.get("close_reason") or "") in
                              ("stopped_full", "stop")), len(closed)),
        "missed_move_r_avg": round(sum(float(r["missed_move_r"]) for r in missed
                                       if r.get("missed_move_r") is not None) / len(missed), 4) if missed else None,
        "missed_move_r_sum": round(sum(float(r["missed_move_r"]) for r in missed
                                       if r.get("missed_move_r") is not None), 4),
        "mfe_r_avg": round(sum(float(r["mfe_r"]) for r in filled if r.get("mfe_r") is not None) / len(filled), 4) if filled else None,
        "mae_r_avg": round(sum(float(r["mae_r"]) for r in filled if r.get("mae_r") is not None) / len(filled), 4) if filled else None,
        "data_gap_late_share": rate(dgl, n),
        # two-cohort accounting: edge metrics above are CLEAN only; dirty (DGL) shown for diagnostics.
        "clean_trades": len(clean_rows),
        "dirty_trades_dgl": dgl,
        "clean_closed": len(closed),
        "dirty_closed_dgl": dirty_closed,
        "latency_p50_min": _pct(lat_vals, 0.50),
        "latency_p90_min": _pct(lat_vals, 0.90),
        "latency_p95_min": _pct(lat_vals, 0.95),
        "maker_entry_posted": sum(int(r.get("maker_entry_posted") or 0) for r in rows),
        "maker_entry_filled": sum(int(r.get("maker_entry_filled") or 0) for r in rows),
        "maker_entry_missed": sum(int(r.get("maker_entry_missed") or 0) for r in rows),
        "taker_fallback_rate": rate(sum(1 for r in rows if int(r.get("taker_fallback_used") or 0) == 1), n),
        "maker_tp_fills": sum(int(r.get("maker_tp_fills") or 0) for r in rows),
        "stale_cost_model_rows": sum(1 for r in rows if r.get("cost_model_status") == "stale_cost_model"),
    }
    return m


EVIDENCE_FORWARD = "forward_postfreeze"
EVIDENCE_BACKFILL = "backfill_pretrained"
# min forward_postfreeze trades before Model-F evidence for a slice may be cited as validated edge —
# mirrors this module's own min_clean_trades_for_verdict default (30), for consistency.
MIN_FORWARD_PROTECTION_TRADES = 30


def _evidence_bucket_stats(rows: list[dict]) -> dict[str, Any]:
    pe = [float(r["paper_execution_r"]) for r in rows if r.get("paper_execution_r") is not None]
    return {"n": len(rows), "resolved": len(pe),
            "net_r_sum": round(sum(pe), 4) if pe else None,
            "avg_r": round(sum(pe) / len(pe), 4) if pe else None}


def protection_evidence_status(prot: dict, *, min_forward_trades: int = MIN_FORWARD_PROTECTION_TRADES) -> str:
    """Whether this slice's Model-F protection numbers may be cited as edge evidence.
    NEVER call the backfill_pretrained bucket "profitable" — it is the same in-sample replay that
    chose Model F's own thresholds, not independent evidence.

    Gated on `resolved` (forward_postfreeze rows with paper_execution_r actually populated), NOT `n`
    — `n` also counts no-entry/open/unresolved forward rows, which carry no R and would let an
    all-open slice falsely look FORWARD_VALIDATED."""
    if not prot or not prot.get("protection_trades"):
        return "NO_PROTECTION_DATA"
    fwd = prot.get("evidence_forward_postfreeze") or {}
    if not fwd.get("n", 0):
        return "NO_FORWARD_EVIDENCE"
    if fwd.get("resolved", 0) >= min_forward_trades:
        return "FORWARD_VALIDATED"
    return "INSUFFICIENT_FORWARD_SAMPLE"


def _protection_metrics(rows: list[dict]) -> dict[str, Any]:
    n = len(rows)
    if not n:
        return {}
    def rate(cnt):
        return round(cnt / n, 4)
    pe_r = [float(r["paper_execution_r"]) for r in rows if r.get("paper_execution_r") is not None]
    # touch_r in paper_execution_outcomes is the LEGACY highest-TP-touched R -> this delta is
    # protected-vs-legacy-touch, NOT protected-vs-true-no-protection. Named honestly.
    deltas = [float(r["paper_execution_r"]) - float(r["touch_r"]) for r in rows
              if r.get("paper_execution_r") is not None and r.get("touch_r") is not None]
    models = sorted({str(r.get("risk_model") or "") for r in rows})
    # 2026-07-09: Model-F evidence-class split. forward_postfreeze = genuine forward evidence (the
    # underlying trade entered at/after the freeze — usable as edge proof). backfill_pretrained =
    # the in-sample replay that chose Model F's own thresholds — hypothesis/context only, NEVER
    # "profitable" evidence. Unclassified = predates the evidence_class column entirely.
    fwd = [r for r in rows if r.get("evidence_class") == EVIDENCE_FORWARD]
    bfd = [r for r in rows if r.get("evidence_class") == EVIDENCE_BACKFILL]
    unc = [r for r in rows if r.get("evidence_class") not in (EVIDENCE_FORWARD, EVIDENCE_BACKFILL)]
    out = {
        "protection_trades": n,
        "protection_model": models[0] if len(models) == 1 else "/".join(models),
        "protection_armed_rate": rate(sum(1 for r in rows if r.get("protection_armed"))),
        "lock_armed_rate": rate(sum(1 for r in rows if r.get("lock_armed"))),
        "breakeven_exit_rate": rate(sum(1 for r in rows if str(r.get("close_reason") or "") == "breakeven_stop")),
        "profit_lock_exit_rate": rate(sum(1 for r in rows if str(r.get("close_reason") or "") == "profit_lock_stop")),
        "giveback_rate": rate(sum(1 for r in rows if r.get("giveback"))),
        "tp3_runner_rate": rate(sum(1 for r in rows if str(r.get("close_reason") or "") == "tp3_runner")),
        "same_candle_ambiguity_rate": rate(sum(1 for r in rows if r.get("same_candle_ambiguous"))),
        "avg_protected_exit_r": round(sum(pe_r) / len(pe_r), 4) if pe_r else None,
        "delta_vs_legacy_touch_r": round(sum(deltas) / len(deltas), 4) if deltas else None,
        "delta_vs_legacy_touch_usd": round((sum(deltas) / len(deltas)) * RISK_USD, 4) if deltas else None,
        "evidence_forward_postfreeze": _evidence_bucket_stats(fwd),
        "evidence_backfill_pretrained": _evidence_bucket_stats(bfd),
        "evidence_unclassified": _evidence_bucket_stats(unc),
    }
    out["protection_evidence_status"] = protection_evidence_status(out)
    return out


# --------------------------------------------------------------------------- paired
def _is_filled(row) -> bool:
    return row.get("entry_fill_status") == "filled" and row.get("net_pnl_usdt") is not None


def _paired(shadow_rows: list[dict]) -> list[dict]:
    """Per (signal_id, fee_profile): old_paper vs new_logic_shadow, aggregated by
    (asset, mode, new_entry_mode, window), split into:
      - executed_vs_executed: BOTH branches actually filled (pure execution delta) -> drives verdict.
      - with_skips_or_avoided: skips/misses counted as 0 PnL; surfaces avoided-bad + missed-good."""
    by_key: dict[tuple, dict[str, dict]] = {}
    for r in shadow_rows:
        k = (r["signal_id"], r.get("fee_profile"))
        by_key.setdefault(k, {})[r["branch"]] = r
    groups: dict[tuple, dict] = {}
    for (_sid, _fp), branches in by_key.items():
        o = branches.get(BRANCH_OLD)
        nw = branches.get(BRANCH_NEW)
        if not o or not nw:
            continue
        slice_key = (str(nw.get("asset_class") or ""), str(nw.get("trade_mode") or ""),
                     str(nw.get("entry_mode") or ""), str(nw.get("window") or ""))
        g = groups.setdefault(slice_key, {
            "ex_common": 0, "new_better": 0, "old_better": 0, "flat": 0,
            "ex_sum_usd": 0.0, "ex_sum_r": 0.0, "examples": [],
            "ws_common": 0, "ws_sum_usd": 0.0,
            "avoided_bad": 0, "avoided_bad_usd": 0.0, "missed_good": 0, "missed_good_usd": 0.0})
        of, nf = _is_filled(o), _is_filled(nw)
        o_usd = float(o["net_pnl_usdt"]) if of else 0.0
        n_usd = float(nw["net_pnl_usdt"]) if nf else 0.0
        # with-skips (skips = 0 PnL)
        g["ws_common"] += 1
        g["ws_sum_usd"] += (n_usd - o_usd)
        if (not nf) and of and float(o["net_pnl_usdt"]) < 0:
            g["avoided_bad"] += 1
            g["avoided_bad_usd"] += -float(o["net_pnl_usdt"])   # loss new-logic sidestepped (good)
        if (not nf) and of and float(o["net_pnl_usdt"]) > 0:
            g["missed_good"] += 1
            g["missed_good_usd"] += float(o["net_pnl_usdt"])    # win new-logic passed up (bad)
        # executed-only (both filled)
        if of and nf:
            d_usd = float(nw["net_pnl_usdt"]) - float(o["net_pnl_usdt"])
            d_r = (float(nw["net_r"]) - float(o["net_r"])) if (nw.get("net_r") is not None and o.get("net_r") is not None) else 0.0
            g["ex_common"] += 1
            g["ex_sum_usd"] += d_usd
            g["ex_sum_r"] += d_r
            if d_usd > 0.01:
                g["new_better"] += 1
            elif d_usd < -0.01:
                g["old_better"] += 1
            else:
                g["flat"] += 1
            g["examples"].append({"signal_id": nw["signal_id"], "delta_usd": round(d_usd, 4),
                                  "delta_r": round(d_r, 4), "entry_mode": nw.get("entry_mode"),
                                  "new_close": nw.get("close_reason"), "old_close": o.get("close_reason")})
    out = []
    for k, g in groups.items():
        ex = sorted(g["examples"], key=lambda e: e["delta_usd"])
        out.append({
            "asset_class": k[0], "mode": k[1], "entry_mode": k[2], "window": k[3],
            # executed_vs_executed (verdict-relevant)
            "executed_common": g["ex_common"], "new_better_count": g["new_better"],
            "old_better_count": g["old_better"], "flat_count": g["flat"],
            "executed_sum_delta_usd": round(g["ex_sum_usd"], 4),
            "executed_avg_delta_usd": round(g["ex_sum_usd"] / g["ex_common"], 4) if g["ex_common"] else None,
            "executed_sum_delta_r": round(g["ex_sum_r"], 4),
            # with_skips_or_avoided (context, NOT verdict-driving)
            "with_skips_common": g["ws_common"], "with_skips_sum_delta_usd": round(g["ws_sum_usd"], 4),
            "avoided_bad_count": g["avoided_bad"], "avoided_bad_usd": round(g["avoided_bad_usd"], 4),
            "missed_good_count": g["missed_good"], "missed_good_usd": round(g["missed_good_usd"], 4),
            "worse_tail": ex[:10], "better_tail": list(reversed(ex[-10:])),
        })
    return out


# --------------------------------------------------------------------------- verdict
def slice_verdict(*, asset_class: str, mode: str, entry_mode: str, window: str,
                  metrics: dict, paired_delta_usd: float | None, old_max_dd_usd: float | None,
                  cfg: dict) -> tuple[str, list[str]]:
    """Config-driven verdict for a slice. Only forward slices get promotable verdicts."""
    v = (cfg.get("verdicts") or {})
    reasons: list[str] = []

    # (item 6) NO_CHASE_SKIP is not an economic entry mode -> skip-policy diagnostics only.
    if _is_skip_mode(entry_mode):
        return "SKIP_POLICY", ["NO_CHASE_SKIP is a skip decision, not a promotable entry mode"]
    # (item 5) retired stocks swing/invest -> legacy appendix, never promotable, never summed.
    if _is_legacy_unsupported(asset_class, mode, entry_mode):
        return "UNSUPPORTED_LEGACY", ["retired stocks swing/invest framework — legacy, not promotable"]

    disabled = disabled_shadow_reason(asset_class=asset_class, trade_mode=mode, entry_mode=entry_mode)
    if disabled:
        return "DISABLED_BY_POLICY", [disabled]

    if window != FORWARD:
        return "KEEP_SHADOW", ["backfill/hypothesis-only — not eligible for promotion verdict"]

    trades = metrics.get("closed") or 0          # CLEAN closed trades (DGL already excluded in _slice_metrics)
    dgl = metrics.get("data_gap_late_share") or 0.0
    pf = metrics.get("profit_factor")
    net_usd = metrics.get("net_pnl_usd") or 0.0
    max_dd_r = metrics.get("max_drawdown_r") or 0.0
    max_dd_usd = metrics.get("max_drawdown_usd") or 0.0
    pd_usd = paired_delta_usd if paired_delta_usd is not None else None

    # (item 7) data-quality blocker BEFORE the min-trades gate, so a thin-but-gappy slice can never
    # be read as a promising NEED_MORE_DATA.
    if dgl > float(v.get("data_gap_late_block_pct", 0.30)):
        return "DATA_QUALITY_BLOCKED", [f"DATA_GAP_LATE {dgl:.0%} > {v.get('data_gap_late_block_pct', 0.30):.0%} of trades"]
    # (S3) the sample gate is CLEAN-based: too few clean (non-DGL) closed trades → no conclusion is
    # allowed. This can NEVER read as KEEP/PROMOTE/DISABLE — it blocks on insufficient clean evidence.
    min_clean = int(v.get("min_clean_trades_for_verdict", v.get("min_trades_for_verdict", 30)))
    if trades < min_clean:
        return "INSUFFICIENT_CLEAN_SAMPLE", [f"clean closed={trades} < {min_clean} "
                                             f"(dirty DGL excluded: {metrics.get('dirty_closed_dgl', 0)})"]

    pf_num = pf if (pf is not None and pf != float("inf")) else (999.0 if pf == float("inf") else 0.0)
    dis = v.get("disable", {})
    if net_usd <= float(dis.get("net_pnl_usd_max", 0.0)) or pf_num < float(dis.get("profit_factor_min", 1.15)):
        return "DISABLE", [f"net_usd={net_usd:.0f}, PF={pf_num:.2f} below disable gate"]

    pc = v.get("paper_candidate", {})
    pr = v.get("promote_review", {})
    is_candidate = (pf_num >= float(pc.get("profit_factor_min", 1.25)) and net_usd > 0
                    and (pd_usd is None or pd_usd > float(pc.get("paired_delta_usd_min", 0.0)))
                    and max_dd_r <= float(pc.get("max_drawdown_r_acceptable", 8.0)))
    dd_ok_vs_old = True
    if pr.get("drawdown_not_worse_than_old", True) and old_max_dd_usd is not None:
        dd_ok_vs_old = max_dd_usd <= old_max_dd_usd + 1e-6
    is_promote = (trades >= int(pr.get("trades_min", 100)) and pf_num >= float(pr.get("profit_factor_min", 1.35))
                  and (pd_usd is None or pd_usd > float(pr.get("paired_delta_usd_min", 0.0))) and dd_ok_vs_old)

    if is_promote:
        return "PROMOTE_REVIEW", [f"trades={trades}, PF={pf_num:.2f}, paired_delta_usd={pd_usd}, DD_ok_vs_old={dd_ok_vs_old}"]
    if is_candidate:
        return "PAPER_CANDIDATE", [f"PF={pf_num:.2f}, net_usd={net_usd:.0f}, paired_delta_usd={pd_usd}, maxDD_r={max_dd_r:.1f}"]
    if pf_num >= float(v.get("watch", {}).get("profit_factor_min", 1.20)) and net_usd > 0:
        return "WATCH", [f"PF={pf_num:.2f} positive but below candidate gate"]
    return "KEEP_SHADOW", [f"PF={pf_num:.2f}, net_usd={net_usd:.0f} — alive, not yet candidate"]


# --------------------------------------------------------------------------- compute
def compute(conn, *, now_iso: str | None = None) -> dict[str, Any]:
    cfg = load_calibration_config()
    now_iso = now_iso or datetime.now(timezone.utc).isoformat()
    latency = _load_latency_cause(conn)
    shadow_rows = _load_shadow_rows(conn)
    protection_by_signal = _load_protection_by_signal(conn)

    # group shadow rows by primary slice key
    groups: dict[tuple, list[dict]] = {}
    for r in shadow_rows:
        key = (str(r.get("asset_class") or ""), str(r.get("trade_mode") or ""),
               str(r.get("entry_mode") or ""), str(r.get("branch") or ""), str(r.get("window") or ""))
        groups.setdefault(key, []).append(r)

    paired = _paired(shadow_rows)
    paired_by_key = {(p["asset_class"], p["mode"], p["entry_mode"], p["window"]): p for p in paired}
    # old-branch drawdown per (asset,mode,entry_mode,window) for the promote gate
    old_dd: dict[tuple, float] = {}
    for key, rows in groups.items():
        if key[3] == BRANCH_OLD:
            old_dd[(key[0], key[1], key[2], key[4])] = _slice_metrics(rows, latency).get("max_drawdown_usd")

    slices = []
    for key, rows in sorted(groups.items()):
        asset, mode, em, branch, window = key
        metrics = _slice_metrics(rows, latency)
        # Protection is auxiliary and must use exactly the same clean, resolved
        # economic trades as the USD edge metrics. Including skipped/missed rows
        # made coverage exceed 100%, which overstated how complete the evidence
        # was without changing any PnL.
        closed_sids = {
            r["signal_id"] for r in rows
            if r.get("entry_fill_status") == "filled"
            and r.get("net_pnl_usdt") is not None
            and r.get("outcome_status") in ("closed", None)
            and r.get("is_clean_for_edge") != 0
            and latency.get(r["signal_id"], {}).get("cause") != "DATA_GAP_LATE"
        }
        pe_rows = [protection_by_signal[s] for s in closed_sids if s in protection_by_signal]
        prot = _protection_metrics(pe_rows)
        closed = metrics.get("closed") or 0
        coverage = (len(pe_rows) / closed) if closed else 0.0
        if prot:
            prot["protection_coverage"] = round(coverage, 3)
            prot["protection_auxiliary_non_comparable"] = bool(coverage < 0.5)
        verdict, vreasons = "KEEP_SHADOW", []
        executed_paired_delta = None
        with_skips_paired_delta = None
        if branch == BRANCH_NEW:
            pk = paired_by_key.get((asset, mode, em, window))
            executed_paired_delta = pk.get("executed_sum_delta_usd") if pk else None
            with_skips_paired_delta = pk.get("with_skips_sum_delta_usd") if pk else None
            # (item 7) verdict uses EXECUTED-ONLY paired delta, never the mixed with-skips delta.
            verdict, vreasons = slice_verdict(
                asset_class=asset, mode=mode, entry_mode=em, window=window, metrics=metrics,
                paired_delta_usd=executed_paired_delta,
                old_max_dd_usd=old_dd.get((asset, mode, em, window)), cfg=cfg)
        slices.append({
            "asset_class": asset, "mode": mode, "entry_mode": em, "branch": branch, "window": window,
            "policy_disabled_reason": disabled_shadow_reason(asset_class=asset, trade_mode=mode, entry_mode=em),
            "policy_promoted_reason": paper_promotion_reason(asset_class=asset, trade_mode=mode, entry_mode=em),
            "verdict": verdict, "verdict_reasons": vreasons,
            "executed_paired_delta_usd": executed_paired_delta,
            "with_skips_paired_delta_usd": with_skips_paired_delta,
            **metrics, **prot,
        })

    return {
        "generated_at": now_iso,
        "activated_at": _activation(conn),
        "risk_usd_per_trade": RISK_USD,
        "slices": slices,
        "paired": paired,
        "config": {"verdicts": cfg.get("verdicts", {})},
    }


# --------------------------------------------------------------------------- persist
_DDL_SLICES = """
CREATE TABLE IF NOT EXISTS entry_mode_calibration_slices (
  generated_at TEXT, asset_class TEXT, mode TEXT, entry_mode TEXT, branch TEXT, window TEXT,
  verdict TEXT, trades INTEGER, filled INTEGER, closed INTEGER, net_pnl_usd REAL, net_r_sum REAL,
  profit_factor REAL, winrate REAL, max_drawdown_usd REAL, max_drawdown_r REAL,
  data_gap_late_share REAL, executed_paired_delta_usd REAL, with_skips_paired_delta_usd REAL,
  protection_model TEXT, giveback_rate REAL, delta_vs_legacy_touch_usd REAL,
  protection_auxiliary_non_comparable INTEGER, metrics_json TEXT,
  protection_evidence_status TEXT, evidence_forward_n INTEGER, evidence_backfill_n INTEGER,
  evidence_unclassified_n INTEGER,
  PRIMARY KEY (asset_class, mode, entry_mode, branch, window)
);
"""
_DDL_PAIRED = """
CREATE TABLE IF NOT EXISTS entry_mode_calibration_paired (
  generated_at TEXT, asset_class TEXT, mode TEXT, entry_mode TEXT, window TEXT,
  executed_common INTEGER, new_better_count INTEGER, old_better_count INTEGER, flat_count INTEGER,
  executed_sum_delta_usd REAL, executed_avg_delta_usd REAL, executed_sum_delta_r REAL,
  with_skips_common INTEGER, with_skips_sum_delta_usd REAL,
  avoided_bad_count INTEGER, avoided_bad_usd REAL, missed_good_count INTEGER, missed_good_usd REAL,
  tails_json TEXT, PRIMARY KEY (asset_class, mode, entry_mode, window)
);
"""


def _persist(conn, result: dict) -> None:
    # drop+recreate the read-model tables so schema changes migrate cleanly (they are OWNED
    # read-model tables, never source data).
    conn.execute("DROP TABLE IF EXISTS entry_mode_calibration_slices")
    conn.execute("DROP TABLE IF EXISTS entry_mode_calibration_paired")
    conn.execute(_DDL_SLICES)
    conn.execute(_DDL_PAIRED)
    g = result["generated_at"]
    for s in result["slices"]:
        conn.execute(
            "INSERT OR REPLACE INTO entry_mode_calibration_slices "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (g, s["asset_class"], s["mode"], s["entry_mode"], s["branch"], s["window"], s["verdict"],
             s.get("trades"), s.get("filled"), s.get("closed"), s.get("net_pnl_usd"), s.get("net_r_sum"),
             _num(s.get("profit_factor")), s.get("winrate"), s.get("max_drawdown_usd"), s.get("max_drawdown_r"),
             s.get("data_gap_late_share"), s.get("executed_paired_delta_usd"), s.get("with_skips_paired_delta_usd"),
             s.get("protection_model"), s.get("giveback_rate"), s.get("delta_vs_legacy_touch_usd"),
             1 if s.get("protection_auxiliary_non_comparable") else 0, json.dumps(s),
             s.get("protection_evidence_status"),
             (s.get("evidence_forward_postfreeze") or {}).get("n"),
             (s.get("evidence_backfill_pretrained") or {}).get("n"),
             (s.get("evidence_unclassified") or {}).get("n")))
    for p in result["paired"]:
        conn.execute(
            "INSERT OR REPLACE INTO entry_mode_calibration_paired VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (g, p["asset_class"], p["mode"], p["entry_mode"], p["window"], p["executed_common"],
             p["new_better_count"], p["old_better_count"], p["flat_count"], p["executed_sum_delta_usd"],
             p["executed_avg_delta_usd"], p["executed_sum_delta_r"], p["with_skips_common"],
             p["with_skips_sum_delta_usd"], p["avoided_bad_count"], p["avoided_bad_usd"],
             p["missed_good_count"], p["missed_good_usd"],
             json.dumps({"worse_tail": p["worse_tail"], "better_tail": p["better_tail"]})))
    conn.commit()


def _num(v):
    if v == float("inf"):
        return 999.0
    return v


def refresh(*, db: str | None = None, persist: bool = True, now_iso: str | None = None,
            write_artifacts: bool | None = None, artifacts_dir: str | None = None) -> dict[str, Any]:
    """Compute the calibration read-model. persist=True writes the read-model TABLES into the
    given db. GLOBAL artifacts (data/diagnostics/entry_mode_calibration.json) are written ONLY when
    write_artifacts is True — which DEFAULTS TO (db is None), i.e. the production DB. A test/temp db
    NEVER overwrites production diagnostics unless it passes artifacts_dir or write_artifacts=True.
    Reads source tables only; never writes proposed_signals / signal_outcomes / final_r."""
    path = _db_path(db)
    result = {"db_path": str(path)}
    conn = sqlite3.connect(path)
    try:
        result.update(compute(conn, now_iso=now_iso))
        if persist:
            _persist(conn, result)
    finally:
        conn.close()
    do_artifacts = (db is None) if write_artifacts is None else bool(write_artifacts)
    if do_artifacts:
        try:
            base = Path(artifacts_dir) if artifacts_dir else (_root() / "data" / "diagnostics")
            base.mkdir(parents=True, exist_ok=True)
            with (base / "entry_mode_calibration.json").open("w", encoding="utf-8") as fh:
                json.dump(result, fh, indent=2, default=str)
        except Exception:
            pass
    return result


# --------------------------------------------------------------------------- policy summary
def policy_summary(result: dict) -> dict[str, Any]:
    """Reflect the entry-mode policy against actual slices: what is disabled/promoted,
    trades that WOULD be affected, trades ACTUALLY affected forward-only, and any
    disabled mode still leaking into a promoted-paper slice (integrity breach)."""
    disabled, promoted, leaks = [], [], []
    for s in result["slices"]:
        if s["branch"] != BRANCH_NEW:
            continue
        base = {"asset_class": s["asset_class"], "mode": s["mode"], "entry_mode": s["entry_mode"],
                "window": s["window"], "trades": s.get("trades", 0), "closed": s.get("closed", 0)}
        if s.get("policy_disabled_reason"):
            disabled.append({**base, "reason": s["policy_disabled_reason"]})
            if s.get("policy_promoted_reason"):
                leaks.append({**base, "disabled_reason": s["policy_disabled_reason"],
                              "promoted_reason": s["policy_promoted_reason"]})
        if s.get("policy_promoted_reason"):
            promoted.append({**base, "reason": s["policy_promoted_reason"]})
    fwd = lambda lst: [x for x in lst if x["window"] == FORWARD]
    return {
        "disabled_slices": disabled,
        "promoted_slices": promoted,
        "disabled_trades_would_affect": sum(x["trades"] for x in disabled),
        "disabled_trades_forward_actual": sum(x["trades"] for x in fwd(disabled)),
        "promoted_trades_would_affect": sum(x["trades"] for x in promoted),
        "promoted_trades_forward_actual": sum(x["trades"] for x in fwd(promoted)),
        "integrity_ok": len(leaks) == 0,
        "policy_leaks": leaks,
    }


# --------------------------------------------------------------------------- report
def _fmt(v, nd=2, dash="-"):
    if v is None:
        return dash
    if v == float("inf"):
        return "inf"
    try:
        return f"{float(v):.{nd}f}"
    except (TypeError, ValueError):
        return str(v)


def render_markdown(result: dict) -> str:
    slices = result["slices"]
    _all_new_fwd = [s for s in slices if s["branch"] == BRANCH_NEW and s["window"] == FORWARD]

    def _bucket(s):
        if _is_legacy_unsupported(s["asset_class"], s["mode"], s["entry_mode"]):
            return "legacy"
        if _is_skip_mode(s["entry_mode"]):
            return "skip"
        if s.get("policy_disabled_reason"):
            return "disabled"
        # (S4) data-quality / insufficient clean sample → NEVER evidence; own diagnostics block.
        if s.get("verdict") in ("DATA_QUALITY_BLOCKED", "INSUFFICIENT_CLEAN_SAMPLE"):
            return "blocked"
        return "eligible"

    # ELIGIBLE forward evidence = NOT legacy, NOT skip (NO_CHASE), NOT disabled-by-policy, NOT
    # data-quality/insufficient-clean-sample blocked. Only eligible drives headline net USD / verdict
    # counts. Legacy -> appendix; skip -> skip-policy diagnostics; disabled -> policy-disabled block;
    # blocked -> data-quality diagnostics. None are summed into the eligible headline.
    legacy_fwd = [s for s in _all_new_fwd if _bucket(s) == "legacy"]
    skip_fwd = [s for s in _all_new_fwd if _bucket(s) == "skip"]
    disabled_fwd = [s for s in _all_new_fwd if _bucket(s) == "disabled"]
    blocked_fwd = [s for s in _all_new_fwd if _bucket(s) == "blocked"]
    new_fwd = [s for s in _all_new_fwd if _bucket(s) == "eligible"]
    new_bf = [s for s in slices if s["branch"] == BRANCH_NEW and s["window"] == BACKFILL and _bucket(s) == "eligible"]
    pol = policy_summary(result)
    L: list[str] = []
    L.append("# Entry-Mode Calibration (paper / read-model)")
    L.append("")
    L.append(f"- generated_at: `{result['generated_at']}`  · activated_at: `{result.get('activated_at')}`")
    L.append(f"- risk/trade: `${result['risk_usd_per_trade']:.0f}`  · USD PnL is authoritative; R auxiliary")
    L.append("- **Decisions are made ONLY on forward_since_activation. Historical backfill is hypothesis-only.**")
    L.append("- **Source tables READ-ONLY** (paper_shadow_execution_outcomes, paper_execution_outcomes, "
             "proposed_signals, signal_entry_mode, entry_latency_audit). **Read-model writes ONLY** to "
             "entry_mode_calibration_slices / entry_mode_calibration_paired + JSON/CSV.")
    L.append("- Live / auto-live / manual-live locked; NO writes to proposed_signals / signal_outcomes / final_r.")
    L.append("- paired delta is **executed_vs_executed** (both branches filled) for verdicts; "
             "**with_skips_or_avoided** is context only (avoided-bad / missed-good).")
    L.append("")

    # headline — ELIGIBLE forward evidence only (legacy + skip + policy-disabled broken out below)
    counts: dict[str, int] = {}
    for s in new_fwd:
        counts[s["verdict"]] = counts.get(s["verdict"], 0) + 1
    L.append("## Headline — ELIGIBLE forward evidence (new_logic_shadow)")
    L.append("")
    L.append(f"- eligible forward slices: **{len(new_fwd)}**  · " +
             ("  ".join(f"{k}: {v}" for k, v in sorted(counts.items())) or "(none)"))
    tot_usd = sum((s.get("net_pnl_usd") or 0) for s in new_fwd)
    L.append(f"- eligible forward net USD: **${tot_usd:,.0f}**  (EXCLUDES policy-disabled "
             f"[{len(disabled_fwd)}] + legacy stocks swing/invest [{len(legacy_fwd)}] + "
             f"NO_CHASE_SKIP [{len(skip_fwd)}] + data-quality/insufficient-clean [{len(blocked_fwd)}])")
    L.append("- **Edge metrics (net USD / PF / winrate) are CLEAN-cohort only — DATA_GAP_LATE trades "
             "are NEVER counted as edge (shown as dirty diagnostics).**")
    L.append("- **Legacy stocks swing/invest evidence is NOT valid for the new stocks_position_framework "
             "(stocks_swing_growth_breakout / earnings_drift / stage2_position) — evaluated separately.**")
    L.append("")

    def _table(rows, title):
        L.append(f"## {title}")
        L.append("")
        if not rows:
            L.append("_none_")
            L.append("")
            return
        L.append("| asset | mode | entry_mode | trades | filled | closed | net USD | PF | maxDD $ | maxDD R | DGL% | exec Δ$ | w/skips Δ$ | verdict | reason |")
        L.append("|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|---|")
        for s in sorted(rows, key=lambda x: (x.get("net_pnl_usd") or 0)):
            L.append("| {a} | {m} | {e} | {t} | {fi} | {c} | {u} | {pf} | {dd} | {ddr} | {dgl} | {ex} | {ws} | {v} | {r} |".format(
                a=s["asset_class"], m=s["mode"], e=s["entry_mode"], t=s.get("trades", 0),
                fi=s.get("filled", 0), c=s.get("closed", 0), u=_fmt(s.get("net_pnl_usd"), 0),
                pf=_fmt(s.get("profit_factor")), dd=_fmt(s.get("max_drawdown_usd"), 0),
                ddr=_fmt(s.get("max_drawdown_r"), 1), dgl=_fmt((s.get("data_gap_late_share") or 0) * 100, 0),
                ex=_fmt(s.get("executed_paired_delta_usd"), 0), ws=_fmt(s.get("with_skips_paired_delta_usd"), 0),
                v=s["verdict"], r=("; ".join(s.get("verdict_reasons") or []))[:60]))
        L.append("")

    _table(new_fwd, "Eligible forward evidence — by asset / mode / entry_mode (new_logic_shadow)")
    _table(new_bf, "Historical backfill (HYPOTHESIS-ONLY — not for promotion)")

    # (S4/S7) data-quality / insufficient-clean-sample diagnostics — NEVER promotion evidence. The
    # reason column carries clean-vs-dirty counts + why promotion is blocked by data quality.
    if blocked_fwd:
        _table(blocked_fwd, "Data-quality / insufficient-clean-sample diagnostics "
                            "(DATA_QUALITY_BLOCKED / INSUFFICIENT_CLEAN_SAMPLE — promotion blocked, NOT evidence)")

    # policy-disabled diagnostics — excluded from eligible evidence + ranking (never promotable)
    if disabled_fwd:
        _table(disabled_fwd, "Policy-disabled diagnostics (DISABLED_BY_POLICY — not eligible, not ranked)")

    # legacy appendix (retired stocks swing/invest) — NOT promotable, NOT summed above
    if legacy_fwd:
        _table(legacy_fwd, "APPENDIX — legacy stocks swing/invest (UNSUPPORTED_LEGACY, not promotable)")

    # skip-policy diagnostics (NO_CHASE_SKIP) — not an economic entry mode
    if skip_fwd:
        L.append("## Skip-policy diagnostics (NO_CHASE_SKIP — not an economic entry mode)")
        L.append("")
        L.append("| asset | mode | entry_mode | trades | skipped | verdict |")
        L.append("|---|---|---|--:|--:|---|")
        for s in skip_fwd:
            L.append(f"| {s['asset_class']} | {s['mode']} | {s['entry_mode']} | {s.get('trades',0)} | "
                     f"{s.get('skipped',0)} | {s['verdict']} |")
        L.append("")

    # paired — ELIGIBLE only: exclude legacy + NO_CHASE_SKIP + policy-disabled from the ranking
    def _paired_eligible(p):
        return (p["window"] == FORWARD and not _is_legacy_unsupported(p["asset_class"], p["mode"], p["entry_mode"])
                and not _is_skip_mode(p["entry_mode"])
                and not disabled_shadow_reason(asset_class=p["asset_class"], trade_mode=p["mode"], entry_mode=p["entry_mode"]))
    L.append("## Paired old_paper vs new_logic_shadow (forward — ELIGIBLE modes)")
    L.append("")
    pf_rows = [p for p in result["paired"] if _paired_eligible(p)]
    if pf_rows:
        L.append("_executed_vs_executed (both branches filled) — drives verdicts:_")
        L.append("")
        L.append("| asset | mode | entry_mode | exec common | new✓ | old✓ | flat | exec sum Δ$ | exec avg Δ$ | exec sum ΔR |")
        L.append("|---|---|---|--:|--:|--:|--:|--:|--:|--:|")
        for p in sorted(pf_rows, key=lambda x: x["executed_sum_delta_usd"]):
            L.append(f"| {p['asset_class']} | {p['mode']} | {p['entry_mode']} | {p['executed_common']} | "
                     f"{p['new_better_count']} | {p['old_better_count']} | {p['flat_count']} | "
                     f"{_fmt(p['executed_sum_delta_usd'],0)} | {_fmt(p['executed_avg_delta_usd'])} | "
                     f"{_fmt(p['executed_sum_delta_r'])} |")
        L.append("")
        L.append("_with_skips_or_avoided (skips = 0 PnL) — CONTEXT ONLY, not verdict-driving:_")
        L.append("")
        L.append("| asset | mode | entry_mode | w/skips common | w/skips sum Δ$ | avoided bad (n / $) | missed good (n / $) |")
        L.append("|---|---|---|--:|--:|--:|--:|")
        for p in sorted(pf_rows, key=lambda x: x["with_skips_sum_delta_usd"]):
            L.append(f"| {p['asset_class']} | {p['mode']} | {p['entry_mode']} | {p['with_skips_common']} | "
                     f"{_fmt(p['with_skips_sum_delta_usd'],0)} | {p['avoided_bad_count']} / "
                     f"{_fmt(p['avoided_bad_usd'],0)} | {p['missed_good_count']} / {_fmt(p['missed_good_usd'],0)} |")
    else:
        L.append("_no paired forward slices_")
    L.append("")

    # protection metrics
    L.append("## Profit-protection metrics (authoritative Model F book, by entry_mode slice)")
    L.append("")
    L.append("_Protection is the authoritative Model-F paper book, aggregated over EACH slice's own "
             "signal_ids (never mixing forward/backfill). Δ vs legacy-touch = paper_execution_r − touch_r "
             "(touch_r is the legacy highest-TP baseline). `aux` = auxiliary_non_comparable (coverage < 50%)._")
    L.append("")
    L.append("_`evidence` gates whether these numbers may be cited as proof of edge: FORWARD_VALIDATED "
             f"(≥{MIN_FORWARD_PROTECTION_TRADES} resolved forward_postfreeze trades) is the only status usable as evidence. "
             "INSUFFICIENT_FORWARD_SAMPLE and NO_FORWARD_EVIDENCE mean the numbers above are backfill_pretrained "
             "(in-sample replay that chose Model F's own thresholds) — hypothesis/context only, NEVER \"profitable\" evidence._")
    L.append("")
    prot_rows = [s for s in new_fwd if s.get("protection_trades")]
    if prot_rows:
        L.append("| asset | mode | entry_mode | model | cov% | aux | armed% | lock% | BE-exit% | lock-exit% | giveback% | TP3run% | avg prot R | Δ vs legacy-touch $ | evidence |")
        L.append("|---|---|---|---|--:|:-:|--:|--:|--:|--:|--:|--:|--:|--:|:-:|")
        for s in prot_rows:
            L.append("| {a} | {m} | {e} | {mo} | {cov} | {aux} | {ar} | {lk} | {be} | {pl} | {gb} | {t3} | {ap} | {dv} | {ev} |".format(
                a=s["asset_class"], m=s["mode"], e=s["entry_mode"], mo=s.get("protection_model", "-"),
                cov=_fmt((s.get("protection_coverage") or 0) * 100, 0),
                aux=("Y" if s.get("protection_auxiliary_non_comparable") else "n"),
                ar=_fmt((s.get("protection_armed_rate") or 0) * 100, 0),
                lk=_fmt((s.get("lock_armed_rate") or 0) * 100, 0),
                be=_fmt((s.get("breakeven_exit_rate") or 0) * 100, 0),
                pl=_fmt((s.get("profit_lock_exit_rate") or 0) * 100, 0),
                gb=_fmt((s.get("giveback_rate") or 0) * 100, 0),
                t3=_fmt((s.get("tp3_runner_rate") or 0) * 100, 0),
                ap=_fmt(s.get("avg_protected_exit_r")), dv=_fmt(s.get("delta_vs_legacy_touch_usd"), 0),
                ev=s.get("protection_evidence_status", "-")))
        L.append("")
        L.append("### Evidence-class breakdown (forward_postfreeze vs backfill_pretrained vs unclassified)")
        L.append("")
        L.append("| asset | mode | entry_mode | forward_postfreeze n/resolved/netR | backfill_pretrained n/resolved/netR | unclassified n |")
        L.append("|---|---|---|--:|--:|--:|")
        for s in prot_rows:
            fwd = s.get("evidence_forward_postfreeze") or {}
            bfd = s.get("evidence_backfill_pretrained") or {}
            unc = s.get("evidence_unclassified") or {}
            L.append("| {a} | {m} | {e} | {fn}/{fr}/{fnr} | {bn}/{br}/{bnr} | {un} |".format(
                a=s["asset_class"], m=s["mode"], e=s["entry_mode"],
                fn=fwd.get("n", 0), fr=fwd.get("resolved", 0), fnr=_fmt(fwd.get("net_r_sum")),
                bn=bfd.get("n", 0), br=bfd.get("resolved", 0), bnr=_fmt(bfd.get("net_r_sum")),
                un=unc.get("n", 0)))
    else:
        L.append("_no protection data joined_")
    L.append("")

    # policy summary
    L.append("## Policy (paper_entry_mode_policy.yaml) reflected against slices")
    L.append("")
    L.append(f"- integrity_ok (no disabled mode in promoted paper): **{pol['integrity_ok']}**")
    if pol["policy_leaks"]:
        L.append("- **LEAKS:** " + "; ".join(f"{x['asset_class']}/{x['mode']}/{x['entry_mode']}" for x in pol["policy_leaks"]))
    L.append(f"- disabled slices: {len(pol['disabled_slices'])} (forward trades actually affected: {pol['disabled_trades_forward_actual']})")
    L.append(f"- promoted-to-paper slices: {len(pol['promoted_slices'])} (forward trades: {pol['promoted_trades_forward_actual']})")
    for x in pol["promoted_slices"]:
        L.append(f"  - PROMOTED {x['asset_class']}/{x['mode']}/{x['entry_mode']} — {x['reason']} (fwd trades={x['trades']})")
    L.append("")

    # verdict buckets
    def bucket(vs):
        return [s for s in new_fwd if s["verdict"] in vs]
    L.append("## Recommendations")
    L.append("")
    for label, vs in (("Promising — PROMOTE_REVIEW / PAPER_CANDIDATE", ("PROMOTE_REVIEW", "PAPER_CANDIDATE")),
                      ("Watch — WATCH / KEEP_SHADOW", ("WATCH", "KEEP_SHADOW")),
                      ("Disable — DISABLE", ("DISABLE",)),
                      ("Blocked — DATA_QUALITY_BLOCKED / DISABLED_BY_POLICY", ("DATA_QUALITY_BLOCKED", "DISABLED_BY_POLICY")),
                      ("Insufficient data — NEED_MORE_DATA", ("NEED_MORE_DATA",))):
        rows = bucket(vs)
        L.append(f"### {label}  ({len(rows)})")
        for s in sorted(rows, key=lambda x: -(x.get("net_pnl_usd") or 0)):
            L.append(f"- `{s['asset_class']}/{s['mode']}/{s['entry_mode']}` — {s['verdict']} "
                     f"(closed={s.get('closed')}, PF={_fmt(s.get('profit_factor'))}, "
                     f"net=${_fmt(s.get('net_pnl_usd'),0)}, exec Δ=${_fmt(s.get('executed_paired_delta_usd'),0)}) "
                     f"{'; '.join(s.get('verdict_reasons') or [])}")
        L.append("")
    return "\n".join(L)


def write_report(result: dict, out_dir: str | None = None) -> str:
    """Write ENTRY_MODE_CALIBRATION.md (global reports/ by default, or out_dir if given)."""
    md = render_markdown(result)
    base = Path(out_dir) if out_dir else (_root() / "reports")
    base.mkdir(parents=True, exist_ok=True)
    out = base / "ENTRY_MODE_CALIBRATION.md"
    with out.open("w", encoding="utf-8") as fh:
        fh.write(md)
    return str(out)


def export(result: dict, fmt: str = "json", out_dir: str | None = None) -> str:
    """Export the flat slice table as csv or json (global data/diagnostics by default)."""
    base = Path(out_dir) if out_dir else (_root() / "data" / "diagnostics")
    base.mkdir(parents=True, exist_ok=True)
    if fmt == "csv":
        import csv
        out = base / "entry_mode_calibration.csv"
        rows = result["slices"]
        cols = sorted({k for r in rows for k in r.keys() if not isinstance(r.get(k), (list, dict))})
        with out.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            for r in rows:
                w.writerow({k: r.get(k) for k in cols})
        return str(out)
    out = base / "entry_mode_calibration.json"
    with out.open("w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, default=str)
    return str(out)


__all__ = ["compute", "refresh", "slice_verdict", "load_calibration_config", "policy_summary",
           "render_markdown", "write_report", "export",
           "VERDICTS", "RISK_USD", "FORWARD", "BACKFILL", "BRANCH_OLD", "BRANCH_NEW"]
