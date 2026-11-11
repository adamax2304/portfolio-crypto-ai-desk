"""Old-paper (old_paper) vs new-logic-shadow (new_logic_shadow) underperformance diagnostic.
2026-07-12 — READ-ONLY DIAGNOSTIC (audit item #3). Answers WHY old_paper loses to new_logic_shadow:
worse entries, worse exits/protection, chase/late entry, fee drag, mode/entry_mode-specific, or
asset/session/setup-specific.

Reads:
  * entry_mode_calibration_paired (persisted asset/mode/entry_mode/window slices + tails_json) for
    the headline ranking and the global top-worst/top-best signal examples. Merging each slice's own
    persisted worse_tail/better_tail and re-sorting is mathematically valid for a GLOBAL top-N: a
    signal can only be in the global top-10 worst if it is also in its own slice's top-10 worst
    (otherwise >=10 slice-mates already rank worse than it, which would also place them above it
    globally).
  * paper_shadow_execution_outcomes directly, restricted to each signal+branch's AUTHORITATIVE
    fee_profile (paper_shadow_engine.select_fee_profile — crypto vs stock/ETF cost model; never
    mixes fee_profiles for the same signal) for the finer dimensions this module adds: fee_profile,
    session bucket, close_reason/exit-cause, entry_fill_status/skip-reason, DATA_GAP/clean status,
    chase (NO_CHASE_SKIP) attribution, and fee/slippage attribution.

Writes NOTHING to the database — pure read + markdown report (reports/OLD_PAPER_UNDERPERFORMANCE_
DIAGNOSTIC.md). Never touches signal_outcomes / final_r / proposed_signals / live / scoring / TP /
SL / entry / routing. Model F (paper_execution_accounting.py) is a SEPARATE protection-only
accounting layer for the PRODUCTION paper book and is not read or changed here — this module
compares the two SHADOW branches only (paper_shadow_execution_outcomes).

Evidence class: uses paper_shadow_execution_outcomes.window (forward_since_activation vs
historical_backfill) — the same concept entry_mode_calibration.py already gates its own verdicts on.
Tables below combine both windows for statistical power (the mechanisms being diagnosed here — fee
drag, chase logic, exit classification — are fixed logic differences, not backfill-tuned parameters
the way Model F's thresholds were) but a dedicated forward-only cross-check section confirms whether
each pattern holds up in the (currently thin) live sample, and every top-level number states its
window mix explicitly. historical_backfill is never presented as proof on its own.
"""
from __future__ import annotations

import json
import sqlite3
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.execution.entry_mode_calibration import BRANCH_OLD, BRANCH_NEW, FORWARD, BACKFILL
from src.execution.paper_shadow_engine import select_fee_profile

VERSION = "old_paper_diag_v1"
_ROOT = Path(__file__).resolve().parents[2]


# --------------------------------------------------------------------------- helpers
def _num(v):
    try:
        return None if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return None


def _parse_dt(v):
    if not v:
        return None
    try:
        s = str(v).strip().replace("Z", "+00:00")
        dt = datetime.fromisoformat(s)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None


def _avg(vals):
    vals = [v for v in vals if v is not None]
    return round(sum(vals) / len(vals), 3) if vals else None


def _db_path(db: str | None) -> Path:
    if db:
        return Path(db)
    from src.config import load_config
    return Path(load_config().db_path)


def _has_table(conn, name: str) -> bool:
    return bool(conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)).fetchone())


def _is_filled(row: dict) -> bool:
    return row.get("entry_fill_status") == "filled" and row.get("net_pnl_usdt") is not None


def _exit_class(row: dict) -> str:
    """Coarse, honest exit bucket from close_reason + net_r sign. paper_shadow_engine's own
    close_reason taxonomy doesn't distinguish 'stopped at original level' from 'stopped after moving
    to BE/lock' — net_r>=0 on a stop/stopped_full close means the stop had already moved favorably
    (protective) before being hit; net_r<0 means the ORIGINAL stop was hit."""
    close = str(row.get("close_reason") or "")
    net_r = _num(row.get("net_r"))
    if close in ("stop", "stopped_full"):
        return "protective_stop" if (net_r is not None and net_r >= 0) else "original_stop"
    if close == "closed_win":
        return "win"
    if close in ("expired_exit", "expired_no_fill"):
        return "expired_win" if (net_r is not None and net_r > 0) else "expired_flat"
    if close in ("skipped", "invalid_geometry", "invalidated_before_entry"):
        return "no_entry"
    return "other"


# --------------------------------------------------------------------------- load + pair
def _authoritative_rows(conn) -> list[dict]:
    """paper_shadow_execution_outcomes rows, each stamped with its own authoritative_fee_profile.
    Caller filters to fee_profile == authoritative_fee_profile before pairing -- never mixes
    fee_profiles for the same signal/branch."""
    cols = {r[1] for r in conn.execute("PRAGMA table_info(paper_shadow_execution_outcomes)")}
    optional = [c for c in ("data_coverage_status", "is_clean_for_edge", "coverage_gap_minutes")
                if c in cols]
    extra_sel = ("," + ",".join(f"s.{c}" for c in optional)) if optional else ""
    rows = conn.execute(
        f"""
        SELECT s.signal_id, s.branch, s.fee_profile, s.symbol, s.asset_class, s.entry_mode,
               s.entry_fill_status, s.entry_fill_time, s.entry_late_status, s.missed_entry_reason,
               s.skipped_shadow_reason, s.close_reason, s.outcome_status, s.net_pnl_usdt, s.net_r,
               s.gross_r, s.fees_usdt, s.slippage_usdt, s.mfe_r, s.window, s.created_at,
               p.mode AS trade_mode, p.market_regime, p.tier, p.created_at AS signal_created_at{extra_sel}
        FROM paper_shadow_execution_outcomes s
        LEFT JOIN proposed_signals p ON p.signal_id = s.signal_id
        """
    ).fetchall()
    out = []
    for r in rows:
        d = dict(r)
        d["authoritative_fee_profile"] = select_fee_profile(d.get("asset_class"))
        out.append(d)
    return out


def _authoritative_pairs(rows: list[dict]) -> list[dict]:
    """Keep only each row's own authoritative-fee_profile row, then pair BRANCH_OLD/BRANCH_NEW by
    signal_id. A pair requires BOTH branches to have an authoritative row (a branch that never wrote
    a row at all -- as opposed to writing a 'skipped'/'missed' row -- is excluded, since there is
    nothing to compare)."""
    by_key: dict[tuple, dict] = {}
    for d in rows:
        if d.get("fee_profile") != d.get("authoritative_fee_profile"):
            continue
        by_key[(d["signal_id"], d["branch"])] = d
    by_signal: dict[str, dict] = defaultdict(dict)
    for (sid, branch), d in by_key.items():
        by_signal[sid][branch] = d
    pairs = []
    for sid, branches in by_signal.items():
        old, new = branches.get(BRANCH_OLD), branches.get(BRANCH_NEW)
        if old and new:
            pairs.append({"signal_id": sid, "old": old, "new": new})
    return pairs


# --------------------------------------------------------------------------- aggregation
def _book(vals_usd: list[float]) -> dict:
    wins = [x for x in vals_usd if x > 0]
    losses = [x for x in vals_usd if x < 0]
    gl, gw = abs(sum(losses)), sum(wins)
    pf = (gw / gl) if gl > 0 else (float("inf") if wins else None)
    return {"n": len(vals_usd), "net_usd": round(sum(vals_usd), 2),
            "winrate": round(len(wins) / len(vals_usd), 3) if vals_usd else None,
            "pf": round(pf, 2) if isinstance(pf, float) and pf != float("inf") else pf}


def slice_stats(pairs: list[dict]) -> dict[str, Any]:
    """Full stat bundle for one bucket of (old,new) pairs -- mirrors entry_mode_calibration._paired()'s
    executed_vs_executed / with_skips_or_avoided split, plus fee/latency attribution this module adds."""
    executed = [p for p in pairs if _is_filled(p["old"]) and _is_filled(p["new"])]
    old_usd = [_num(p["old"]["net_pnl_usdt"]) or 0.0 for p in executed]
    new_usd = [_num(p["new"]["net_pnl_usdt"]) or 0.0 for p in executed]
    old_r = [_num(p["old"]["net_r"]) for p in executed if _num(p["old"]["net_r"]) is not None]
    new_r = [_num(p["new"]["net_r"]) for p in executed if _num(p["new"]["net_r"]) is not None]
    deltas_usd = [n - o for o, n in zip(old_usd, new_usd)]
    new_better = sum(1 for d in deltas_usd if d > 0.01)
    old_better = sum(1 for d in deltas_usd if d < -0.01)
    flat = len(deltas_usd) - new_better - old_better

    ws_deltas = []
    avoided_bad_n = avoided_bad_usd = missed_good_n = missed_good_usd = 0
    for p in pairs:
        of, nf = _is_filled(p["old"]), _is_filled(p["new"])
        o_usd = (_num(p["old"]["net_pnl_usdt"]) or 0.0) if of else 0.0
        n_usd = (_num(p["new"]["net_pnl_usdt"]) or 0.0) if nf else 0.0
        ws_deltas.append(n_usd - o_usd)
        if of and not nf:
            if o_usd < 0:
                avoided_bad_n += 1; avoided_bad_usd += o_usd
            elif o_usd > 0:
                missed_good_n += 1; missed_good_usd += o_usd

    old_fee = [(_num(p["old"]["fees_usdt"]) or 0.0) + (_num(p["old"]["slippage_usdt"]) or 0.0) for p in executed]
    new_fee = [(_num(p["new"]["fees_usdt"]) or 0.0) + (_num(p["new"]["slippage_usdt"]) or 0.0) for p in executed]
    old_gross_r = [_num(p["old"]["gross_r"]) for p in executed if _num(p["old"]["gross_r"]) is not None]
    new_gross_r = [_num(p["new"]["gross_r"]) for p in executed if _num(p["new"]["gross_r"]) is not None]

    def _latency_min(row):
        # row["created_at"] is paper_shadow_execution_outcomes' OWN compute timestamp (when the
        # shadow refresh wrote this row), not the signal's real creation time -- using it here would
        # measure "minutes before this row was computed" (nonsense, often deeply negative since
        # refreshes replay history). signal_created_at (proposed_signals.created_at) is correct.
        a, b = _parse_dt(row.get("signal_created_at")), _parse_dt(row.get("entry_fill_time"))
        return (b - a).total_seconds() / 60.0 if a and b else None

    old_lat = [_latency_min(p["old"]) for p in executed]
    new_lat = [_latency_min(p["new"]) for p in executed]
    gap_min = [_num(p[b].get("coverage_gap_minutes")) for p in pairs for b in ("old", "new")]

    return {
        "pairs_total": len(pairs),
        "executed_common": len(executed),
        "new_better_count": new_better, "old_better_count": old_better, "flat_count": flat,
        "old_book": _book(old_usd), "new_book": _book(new_usd),
        "old_net_r_sum": round(sum(old_r), 3) if old_r else None,
        "new_net_r_sum": round(sum(new_r), 3) if new_r else None,
        "executed_sum_delta_usd": round(sum(deltas_usd), 2) if deltas_usd else 0.0,
        "executed_avg_delta_usd": round(sum(deltas_usd) / len(deltas_usd), 2) if deltas_usd else None,
        "with_skips_common": len(pairs),
        "with_skips_sum_delta_usd": round(sum(ws_deltas), 2) if ws_deltas else 0.0,
        "avoided_bad_count": avoided_bad_n, "avoided_bad_usd": round(avoided_bad_usd, 2),
        "missed_good_count": missed_good_n, "missed_good_usd": round(missed_good_usd, 2),
        "old_avg_fee_usd": _avg(old_fee), "new_avg_fee_usd": _avg(new_fee),
        "fee_delta_usd": round(sum(old_fee) - sum(new_fee), 2) if (old_fee or new_fee) else None,
        "old_gross_r_sum": round(sum(old_gross_r), 3) if old_gross_r else None,
        "new_gross_r_sum": round(sum(new_gross_r), 3) if new_gross_r else None,
        "old_avg_entry_latency_min": _avg(old_lat), "new_avg_entry_latency_min": _avg(new_lat),
        "avg_coverage_gap_min": _avg(gap_min),
    }


def group_pairs(pairs: list[dict], key_fn) -> dict[Any, dict]:
    buckets: dict[Any, list[dict]] = defaultdict(list)
    for p in pairs:
        buckets[key_fn(p)].append(p)
    return {k: slice_stats(v) for k, v in buckets.items()}


# --------------------------------------------------------------------------- dimension keys
def key_asset_mode(p):
    return (p["new"].get("asset_class") or "?", p["new"].get("trade_mode") or "?")


def key_entry_mode(p):
    return p["new"].get("entry_mode") or "?"


def key_fee_profile(p):
    return p["new"].get("authoritative_fee_profile") or "?"


def key_close_reason_pair(p):
    return (_exit_class(p["old"]), _exit_class(p["new"]))


def key_entry_fill_status_pair(p):
    return (p["old"].get("entry_fill_status") or "?", p["new"].get("entry_fill_status") or "?")


def key_data_gap(p):
    return p["old"].get("data_coverage_status") or p["new"].get("data_coverage_status") or "unknown"


def _session_key_fn(cfg):
    from src.execution import crypto_quality_overlay as cqo

    def key(p):
        # entry_fill_time (actual fill) preferred; fall back to the signal's real creation time
        # (proposed_signals.created_at) -- NOT the shadow row's own compute timestamp.
        t = _parse_dt(p["old"].get("entry_fill_time")) or _parse_dt(p["old"].get("signal_created_at"))
        if t is None:
            return "unknown"
        b = cqo.session_bucket(t, cfg)
        # config/crypto_quality_overlay.yaml's unquoted `off:` bucket key is parsed by YAML 1.1 as the
        # boolean False (a bareword-boolean quirk, same family as on/yes/no) -- session_bucket() then
        # returns that same False straight through. Cosmetic-only here (self-consistent lookups
        # elsewhere aren't broken by it), but never let a raw False leak into this report's labels.
        return "off" if b is False else str(b)

    return key


# --------------------------------------------------------------------------- chase attribution
def chase_avoided_stats(pairs: list[dict]) -> dict[str, Any]:
    """NO_CHASE_SKIP: new_logic_shadow's entry per signal_entry_mode was flagged too-extended /
    no-continuation by entry_mode_classifier.classify (skipped_shadow_reason='no_chase_skip').
    old_paper has no such gate and always fills its mechanical pullback-limit entry. Isolates this
    specific chase-avoidance from the broader avoided_bad/missed_good buckets (which cover ALL skip
    reasons, e.g. policy-disabled entry_mode too)."""
    chase = [p for p in pairs if p["new"].get("skipped_shadow_reason") == "no_chase_skip"]
    old_losses = [p for p in chase if _is_filled(p["old"]) and (_num(p["old"]["net_pnl_usdt"]) or 0) < 0]
    old_wins = [p for p in chase if _is_filled(p["old"]) and (_num(p["old"]["net_pnl_usdt"]) or 0) > 0]
    return {
        "chase_pairs_total": len(chase),
        "old_losses_avoided_n": len(old_losses),
        "old_losses_avoided_usd": round(sum(_num(p["old"]["net_pnl_usdt"]) or 0 for p in old_losses), 2),
        "old_wins_also_missed_n": len(old_wins),
        "old_wins_also_missed_usd": round(sum(_num(p["old"]["net_pnl_usdt"]) or 0 for p in old_wins), 2),
    }


# --------------------------------------------------------------------------- persisted paired reuse
def _read_persisted_paired(conn) -> list[dict]:
    if not _has_table(conn, "entry_mode_calibration_paired"):
        return []
    return [dict(r) for r in conn.execute("SELECT * FROM entry_mode_calibration_paired").fetchall()]


def _dedupe_keep_extreme(examples: list[dict], pick_min: bool) -> list[dict]:
    best_by_sid: dict[str, dict] = {}
    for ex in examples:
        sid, d = ex.get("signal_id"), ex.get("delta_usd")
        if sid is None or d is None:
            continue
        cur = best_by_sid.get(sid)
        if cur is None or (d < cur["delta_usd"] if pick_min else d > cur["delta_usd"]):
            best_by_sid[sid] = ex
    return list(best_by_sid.values())


def global_tails(persisted_paired: list[dict], n: int = 10) -> dict[str, list[dict]]:
    """Global top-N worst/best signal examples, reusing each persisted slice's own worse_tail/
    better_tail (see module docstring for why merging + re-sorting per-slice top-10s is valid for a
    GLOBAL top-N). Every example is tagged with its window so forward vs backfill is visible."""
    worst_raw, best_raw = [], []
    for row in persisted_paired:
        try:
            tj = json.loads(row.get("tails_json") or "{}")
        except (TypeError, ValueError):
            tj = {}
        tag = {"asset_class": row.get("asset_class"), "mode": row.get("mode"), "window": row.get("window")}
        for ex in (tj.get("worse_tail") or []):
            worst_raw.append({**ex, **tag})
        for ex in (tj.get("better_tail") or []):
            best_raw.append({**ex, **tag})
    worst = sorted(_dedupe_keep_extreme(worst_raw, pick_min=True), key=lambda e: e["delta_usd"])[:n]
    best = sorted(_dedupe_keep_extreme(best_raw, pick_min=False), key=lambda e: -e["delta_usd"])[:n]
    return {"worst": worst, "best": best}


# --------------------------------------------------------------------------- expiry-fix audit
def expiry_audit_before(conn) -> dict[str, Any]:
    """Snapshot, BEFORE an expiry-aware paper_shadow_engine rebuild, how many currently-'filled'
    shadow rows actually filled AFTER their own signal's entry validity window -- i.e. how many rows
    the expiry-aware fix will reclassify. Read-only; call before paper_shadow_engine.refresh(rebuild=True)."""
    from src.execution.paper_shadow_engine import entry_deadline_for
    if not _has_table(conn, "paper_shadow_execution_outcomes"):
        return {"filled_rows_checked": 0, "late_filled_n": 0, "late_filled_by_mode": {}}
    rows = conn.execute(
        "SELECT s.entry_fill_time, p.created_at, p.expires_at, p.validity_window_hours, p.mode "
        "FROM paper_shadow_execution_outcomes s JOIN proposed_signals p ON p.signal_id = s.signal_id "
        "WHERE s.entry_fill_status='filled' AND s.entry_fill_time IS NOT NULL").fetchall()
    late_n = 0
    late_by_mode: dict[str, int] = defaultdict(int)
    for r in rows:
        d = dict(r)
        sig = {"created_at": d.get("created_at"), "expires_at": d.get("expires_at"),
              "validity_window_hours": d.get("validity_window_hours"), "mode": d.get("mode")}
        deadline = entry_deadline_for(sig)
        fill_t = _parse_dt(d.get("entry_fill_time"))
        if deadline is not None and fill_t is not None:
            ft = fill_t if fill_t.tzinfo else fill_t.replace(tzinfo=timezone.utc)
            if ft > deadline:
                late_n += 1
                late_by_mode[str(d.get("mode") or "?")] += 1
    return {"filled_rows_checked": len(rows), "late_filled_n": late_n,
            "late_filled_by_mode": dict(late_by_mode)}


def expiry_audit_after(conn) -> dict[str, Any]:
    """Snapshot, AFTER an expiry-aware paper_shadow_engine rebuild, how many rows are now classified
    after_expiry_blocked (the fix caught and blocked a would-be-late fill). Read-only."""
    if not _has_table(conn, "paper_shadow_execution_outcomes"):
        return {"after_expiry_blocked_n": 0, "after_expiry_blocked_by_mode": {}}
    cols = {r[1] for r in conn.execute("PRAGMA table_info(paper_shadow_execution_outcomes)")}
    if "entry_late_status" not in cols:
        return {"after_expiry_blocked_n": 0, "after_expiry_blocked_by_mode": {}}
    rows = conn.execute(
        "SELECT p.mode, COUNT(*) FROM paper_shadow_execution_outcomes s "
        "JOIN proposed_signals p ON p.signal_id = s.signal_id "
        "WHERE s.entry_late_status='after_expiry_blocked' GROUP BY p.mode").fetchall()
    by_mode = {str(m or "?"): n for m, n in rows}
    return {"after_expiry_blocked_n": sum(by_mode.values()), "after_expiry_blocked_by_mode": by_mode}


def rebuild_and_diagnose(*, db: str | None = None, now_iso: str | None = None,
                         refresh_source: bool = True) -> dict[str, Any]:
    """Full safe-recompute flow for the expiry-aware fix: snapshot the pre-fix after-expiry
    contamination, recompute paper_shadow_execution_outcomes (shadow/read-model table ONLY -- see
    paper_shadow_engine.refresh docstring) so every row picks up the fix, snapshot the post-fix
    blocked count, then run the normal diagnose(). Invariants (proposed_signals count, signal_outcomes
    count/SUM(final_r), live locked, paper_portfolio_ledger untouched) are the caller's responsibility
    to verify externally (this function only touches paper_shadow_execution_outcomes/
    paper_shadow_events by construction, and reads elsewhere).

    Deliberately does NOT pass rebuild=True to paper_shadow_engine.refresh(): that path DELETEs every
    row unconditionally but only RELOADS the most recent 1200 entered signals (_load_signals' default
    LIMIT) -- on this DB there are 2454+ entered signals, so rebuild=True would silently and
    permanently drop ~1250 older rows (confirmed by direct count before this function was written).
    Instead this uses the idempotent, non-destructive path: refresh(rebuild=False, lookback_hours=None,
    max_signals=None) UPSERTs (INSERT OR REPLACE, keyed by signal_id+branch+fee_profile) EVERY entered
    signal (no row cap) -- recomputing each with the expiry-aware fix now active -- without ever
    deleting a row first. max_signals=None is required here: a first version of this function left the
    default 1200-signal cap in place, which left ~1250 older signals un-recomputed and, by direct
    verification, still contaminated roughly half of the report's executed_common pairs with stale
    after-expiry 'filled' rows. Full coverage is safe (still zero delete) but costs one OHLCV pass per
    entered signal x branch."""
    from src.execution import paper_shadow_engine as pse
    path = _db_path(db)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        before = expiry_audit_before(conn)
    finally:
        conn.close()

    pse.refresh(rebuild=False, lookback_hours=None, max_signals=None, db=str(path))

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        after = expiry_audit_after(conn)
    finally:
        conn.close()

    result = diagnose(db=db, now_iso=now_iso, refresh_source=refresh_source)
    result["expiry_fix_before"] = before
    result["expiry_fix_after"] = after
    return result


# --------------------------------------------------------------------------- top-level compute
def diagnose(*, db: str | None = None, now_iso: str | None = None, refresh_source: bool = True) -> dict[str, Any]:
    """Compute the full diagnostic. refresh_source=True (default) first recomputes+persists
    entry_mode_calibration_paired so the headline ranking + top examples are fresh. READ-ONLY beyond
    that (this module itself writes nothing)."""
    path = _db_path(db)
    now = now_iso or datetime.now(timezone.utc).isoformat()
    result: dict[str, Any] = {"generated_at": now, "db_path": str(path), "version": VERSION}

    if refresh_source:
        try:
            from src.execution import entry_mode_calibration as cal
            cal.refresh(db=db, persist=True, now_iso=now_iso)
        except Exception as exc:  # fail-open -- diagnostic must never block on the source refresh
            result["refresh_source_error"] = str(exc)

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        if not _has_table(conn, "paper_shadow_execution_outcomes"):
            result["available"] = False
            result["reason"] = "paper_shadow_execution_outcomes not populated"
            return result
        result["available"] = True

        rows = _authoritative_rows(conn)
        pairs = _authoritative_pairs(rows)
        fwd_pairs = [p for p in pairs if p["new"].get("window") == FORWARD]
        bfd_pairs = [p for p in pairs if p["new"].get("window") == BACKFILL]

        result["pairs_total"] = len(pairs)
        result["forward_pairs"] = len(fwd_pairs)
        result["backfill_pairs"] = len(bfd_pairs)
        result["overall_all_windows"] = slice_stats(pairs)
        result["overall_forward_only"] = slice_stats(fwd_pairs)
        result["overall_backfill_only"] = slice_stats(bfd_pairs)

        result["by_asset_mode"] = group_pairs(pairs, key_asset_mode)
        result["by_entry_mode"] = group_pairs(pairs, key_entry_mode)
        result["by_fee_profile"] = group_pairs(pairs, key_fee_profile)
        result["by_exit_class_pair"] = group_pairs(pairs, key_close_reason_pair)
        result["by_entry_fill_status_pair"] = group_pairs(pairs, key_entry_fill_status_pair)
        result["by_data_gap_status"] = group_pairs(pairs, key_data_gap)
        try:
            from src.execution import crypto_quality_overlay as cqo
            cfg = cqo.load_cfg()
            result["by_session"] = group_pairs(pairs, _session_key_fn(cfg))
        except Exception as exc:
            result["by_session"] = {}
            result["by_session_error"] = str(exc)

        result["chase"] = chase_avoided_stats(pairs)
        result["chase_forward"] = chase_avoided_stats(fwd_pairs)

        persisted = _read_persisted_paired(conn)
        result["persisted_paired_rows"] = len(persisted)
        result["headline_slices"] = sorted(
            persisted, key=lambda r: (r.get("executed_sum_delta_usd") if r.get("executed_sum_delta_usd") is not None else 0.0)
        )
        result["tails"] = global_tails(persisted, n=10)
        return result
    finally:
        conn.close()


# --------------------------------------------------------------------------- report rendering
def _fmt(v, nd=2, dash="-"):
    if v is None:
        return dash
    if v == float("inf"):
        return "inf"
    try:
        return f"{float(v):.{nd}f}"
    except (TypeError, ValueError):
        return dash


_SLICE_HEADER = ("| {label_col} | n | old $ | new $ | delta $ | old/new R | old/new WR | old/new PF | "
                 "old/new avg fee $ | old/new avg entry-latency min | avg data-gap min |")
_SLICE_SEP = "|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|"


def _slice_row(label: str, s: dict) -> str:
    ob, nb = s["old_book"], s["new_book"]
    return (f"| {label} | {s['executed_common']} | {_fmt(ob['net_usd'], 0)} | {_fmt(nb['net_usd'], 0)} | "
            f"{_fmt(s['executed_sum_delta_usd'], 0)} | {_fmt(s.get('old_net_r_sum'))} / {_fmt(s.get('new_net_r_sum'))} | "
            f"{_fmt((ob['winrate'] or 0) * 100, 0)}% / {_fmt((nb['winrate'] or 0) * 100, 0)}% | "
            f"{_fmt(ob['pf'])} / {_fmt(nb['pf'])} | {_fmt(s['old_avg_fee_usd'])} / {_fmt(s['new_avg_fee_usd'])} | "
            f"{_fmt(s.get('old_avg_entry_latency_min'), 1)} / {_fmt(s.get('new_avg_entry_latency_min'), 1)} | "
            f"{_fmt(s.get('avg_coverage_gap_min'), 1)} |")


def render_markdown(result: dict[str, Any]) -> str:
    L = [f"# Old Paper vs New Logic Shadow — Underperformance Diagnostic ({result['generated_at']})", "",
         "> Audit item #3. No trading-logic, TP/SL, entry, routing, scoring, or Model F changes. "
         "Live/auto-live/manual-live remain locked; signal_outcomes/final_r untouched. Compares the two "
         "PAPER SHADOW branches in `paper_shadow_execution_outcomes` (old_paper vs new_logic_shadow) — "
         "NOT the production paper book (`paper_execution_outcomes` / Model F), which is untouched here. "
         "This module itself writes nothing to the database; the CLI command that generates this report "
         "additionally re-runs entry_mode_calibration.refresh() first by default (writes ONLY the "
         "entry_mode_calibration_* read-model tables, never a trading table) — run with "
         "`--no-refresh-source` for a strictly read-only pass.", ""]
    if not result.get("available"):
        L.append(f"_unavailable ({result.get('reason')})_")
        return "\n".join(L)

    exp_before, exp_after = result.get("expiry_fix_before"), result.get("expiry_fix_after")
    if exp_before is not None or exp_after is not None:
        L.append("## Expiry-aware entry-fill fix — before/after")
        L.append("_paper_shadow_engine now blocks any entry fill past the signal's own validity window "
                 "(expires_at, else created_at+validity_window_hours, else the mode default: "
                 "scalp=2h/intraday=24h/swing=168h/invest=720h) instead of silently accepting a late "
                 "fill. Old late-fill rows are NOT clean evidence — they never should have been 'filled'._")
        if exp_before is not None:
            L.append(f"- **before** the expiry-aware rebuild: {exp_before['filled_rows_checked']} filled "
                     f"rows checked, **{exp_before['late_filled_n']}** filled AFTER their own validity "
                     f"window (by mode: {exp_before['late_filled_by_mode'] or '{}'})")
        if exp_after is not None:
            L.append(f"- **after** the rebuild: **{exp_after['after_expiry_blocked_n']}** rows now "
                     f"correctly classified `entry_late_status=after_expiry_blocked` (never 'filled') "
                     f"(by mode: {exp_after['after_expiry_blocked_by_mode'] or '{}'})")
        L.append("- all PnL/exit-cause/fee numbers below already reflect the post-fix data (blocked rows "
                 "are `entry_fill_status='missed'`, so `_is_filled()` excludes them from executed_common "
                 "automatically — no separate re-filtering needed in this report).")
        L.append("")

    fwd, bfd = result["overall_forward_only"], result["overall_backfill_only"]
    L += ["## Evidence quality",
          f"- forward_since_activation pairs: **{result['forward_pairs']}** "
          f"(executed_common={fwd['executed_common']}, Σdelta_usd={_fmt(fwd['executed_sum_delta_usd'], 0)})",
          f"- historical_backfill pairs: **{result['backfill_pairs']}** "
          f"(executed_common={bfd['executed_common']}, Σdelta_usd={_fmt(bfd['executed_sum_delta_usd'], 0)}) "
          "— hypothesis/context only. Not parameter-overfit the way Model F's thresholds were (old_paper/"
          "new_logic_shadow are fixed, pre-specified logic, not backfill-tuned), but still not accumulated "
          "live experience — see the forward-only cross-check section before treating any pattern as proven.",
          "- Tables below combine both windows for statistical power unless labeled forward-only.", ""]

    ov = result["overall_all_windows"]
    L += ["## Headline (all windows)",
          f"- old_paper: net ${_fmt(ov['old_book']['net_usd'], 0)} / {_fmt(ov['old_net_r_sum'])}R over "
          f"{ov['executed_common']} common executed trades (WR {_fmt((ov['old_book']['winrate'] or 0)*100,0)}%, "
          f"PF {_fmt(ov['old_book']['pf'])})",
          f"- new_logic_shadow: net ${_fmt(ov['new_book']['net_usd'], 0)} / {_fmt(ov['new_net_r_sum'])}R "
          f"(WR {_fmt((ov['new_book']['winrate'] or 0)*100,0)}%, PF {_fmt(ov['new_book']['pf'])})",
          f"- **delta (new − old): ${_fmt(ov['executed_sum_delta_usd'], 0)}** "
          f"(new better {ov['new_better_count']} / old better {ov['old_better_count']} / flat {ov['flat_count']})",
          f"- with-skips-or-avoided delta (unfilled counted as $0): ${_fmt(ov['with_skips_sum_delta_usd'], 0)} "
          f"over {ov['with_skips_common']} pairs — avoided_bad n={ov['avoided_bad_count']} "
          f"(${_fmt(ov['avoided_bad_usd'], 0)}), missed_good n={ov['missed_good_count']} (${_fmt(ov['missed_good_usd'], 0)})",
          ""]
    if result.get("expiry_fix_before") is not None or result.get("expiry_fix_after") is not None:
        L += ["**Entry-latency note:** the multi-day/multi-week entry-fill gaps previously seen here were "
              "the after-expiry contamination fixed above (see 'Expiry-aware entry-fill fix') -- those rows "
              "are now excluded from executed_common instead of skewing these numbers. The avg "
              "entry-latency columns below reflect only genuinely-valid, in-window fills.", ""]
    else:
        L += ["**⚠ Data-quality caveat (entry latency):** the avg entry-latency columns below may show "
              "multi-day (sometimes multi-week) gaps between signal creation and fill for scalp/swing pairs "
              "-- this run did not include the expiry-aware fix (see old_paper_underperformance_diagnostic."
              "rebuild_and_diagnose), so late-fill contamination has not been excluded. Treat latency and "
              "executed_common numbers as directional only until re-run through rebuild_and_diagnose.", ""]

    def _worst_key(item):
        k, s = item
        return s["executed_sum_delta_usd"] if s["executed_sum_delta_usd"] is not None else 0.0

    L.append("## Ranked by asset_class × mode — where old_paper loses most (worst first, all windows)")
    L.append(_SLICE_HEADER.format(label_col="asset/mode"))
    L.append(_SLICE_SEP)
    for k, s in sorted(result["by_asset_mode"].items(), key=_worst_key):
        if s["executed_common"] == 0:
            continue
        L.append(_slice_row(f"{k[0]}/{k[1]}", s))
    L.append("")

    L.append("## By entry_mode")
    L.append(_SLICE_HEADER.format(label_col="entry_mode"))
    L.append(_SLICE_SEP)
    for k, s in sorted(result["by_entry_mode"].items(), key=_worst_key):
        if s["executed_common"] == 0:
            continue
        L.append(_slice_row(str(k), s))
    L.append("")

    L.append("## By authoritative fee_profile")
    L.append(_SLICE_HEADER.format(label_col="fee_profile"))
    L.append(_SLICE_SEP)
    for k, s in sorted(result["by_fee_profile"].items(), key=_worst_key):
        if s["executed_common"] == 0:
            continue
        L.append(_slice_row(str(k), s))
    L.append("")

    if result.get("by_session"):
        L.append("## By session bucket (UTC, entry_fill_time else signal created_at)")
        L.append(_SLICE_HEADER.format(label_col="session"))
        L.append(_SLICE_SEP)
        for k, s in sorted(result["by_session"].items(), key=_worst_key):
            if s["executed_common"] == 0:
                continue
            L.append(_slice_row(str(k), s))
        L.append("")

    L.append("## Data-quality (DATA_GAP_LATE / clean status)")
    L.append("| data_coverage_status | n | old $ | new $ | delta $ | avg gap min |")
    L.append("|---|--:|--:|--:|--:|--:|")
    for k, s in sorted(result["by_data_gap_status"].items(), key=_worst_key):
        if s["pairs_total"] == 0:
            continue
        L.append(f"| {k} | {s['executed_common']} | {_fmt(s['old_book']['net_usd'],0)} | "
                 f"{_fmt(s['new_book']['net_usd'],0)} | {_fmt(s['executed_sum_delta_usd'],0)} | "
                 f"{_fmt(s['avg_coverage_gap_min'])} |")
    L.append("")

    L.append("## Exit-cause matrix (common executed trades only, all windows)")
    L.append("_protective_stop = stop hit after moving to BE/lock favorably; original_stop = stop hit before "
             "any favorable move; expired_win/expired_flat by net_r sign at expiry._")
    L.append("")
    L.append("| old exit | new exit | n | Σdelta $ |")
    L.append("|---|---|--:|--:|")
    for k, s in sorted(result["by_exit_class_pair"].items(), key=lambda kv: kv[1]["with_skips_sum_delta_usd"]):
        if s["pairs_total"] == 0:
            continue
        L.append(f"| {k[0]} | {k[1]} | {s['pairs_total']} | {_fmt(s['with_skips_sum_delta_usd'], 0)} |")
    L.append("")

    L.append("## Entry-fill-status matrix (filled / missed / skipped / invalid / no_entry)")
    L.append("| old status | new status | n | Σdelta $ |")
    L.append("|---|---|--:|--:|")
    for k, s in sorted(result["by_entry_fill_status_pair"].items(), key=lambda kv: kv[1]["with_skips_sum_delta_usd"]):
        L.append(f"| {k[0]} | {k[1]} | {s['pairs_total']} | {_fmt(s['with_skips_sum_delta_usd'], 0)} |")
    L.append("")

    ch, chf = result["chase"], result["chase_forward"]
    L += ["## Chase / late-entry attribution (NO_CHASE_SKIP)",
          "_new_logic_shadow's entry_mode_classifier skips entries that are too extended with no "
          "continuation structure; old_paper's mechanical pullback-limit entry has no such gate and always "
          "fills. This isolates exactly that chase-avoidance from the broader avoided_bad bucket above._",
          f"- all windows: {ch['chase_pairs_total']} chase-flagged pairs — old_paper losses avoided: "
          f"n={ch['old_losses_avoided_n']} (${_fmt(ch['old_losses_avoided_usd'], 0)}); old_paper wins also "
          f"missed: n={ch['old_wins_also_missed_n']} (${_fmt(ch['old_wins_also_missed_usd'], 0)})",
          f"- forward-only: {chf['chase_pairs_total']} chase-flagged pairs — losses avoided "
          f"n={chf['old_losses_avoided_n']} (${_fmt(chf['old_losses_avoided_usd'], 0)}); wins also missed "
          f"n={chf['old_wins_also_missed_n']} (${_fmt(chf['old_wins_also_missed_usd'], 0)})", ""]

    L.append("## Fee / cost attribution (executed_vs_executed, authoritative fee_profile only)")
    L.append("| slice | old avg fee+slip $ | new avg fee+slip $ | Σfee delta (old−new) $ | old ΣgrossR | old ΣnetR | new ΣgrossR | new ΣnetR |")
    L.append("|---|--:|--:|--:|--:|--:|--:|--:|")
    for k, s in sorted(result["by_asset_mode"].items(), key=_worst_key):
        if s["executed_common"] == 0:
            continue
        L.append(f"| {k[0]}/{k[1]} | {_fmt(s['old_avg_fee_usd'])} | {_fmt(s['new_avg_fee_usd'])} | "
                 f"{_fmt(s['fee_delta_usd'])} | {_fmt(s['old_gross_r_sum'])} | {_fmt(s['old_net_r_sum'])} | "
                 f"{_fmt(s['new_gross_r_sum'])} | {_fmt(s['new_net_r_sum'])} |")
        og, on = s.get("old_gross_r_sum"), s.get("old_net_r_sum")
        if og is not None and on is not None and og > 0 and on < 0:
            L.append(f"  - ⚠ {k[0]}/{k[1]}: old_paper has POSITIVE gross R ({_fmt(og)}) but NEGATIVE net R "
                     f"({_fmt(on)}) — costs are eating a real gross edge here.")
    L.append("")

    tails = result["tails"]
    L.append("## Top 10 worst signal_ids (old_paper loses most vs new_logic_shadow)")
    L.append("| signal_id | asset/mode | entry_mode | window | delta $ | delta R | old close | new close |")
    L.append("|---|---|---|---|--:|--:|---|---|")
    for ex in tails["worst"]:
        L.append(f"| {ex.get('signal_id')} | {ex.get('asset_class')}/{ex.get('mode')} | "
                 f"{ex.get('entry_mode')} | {ex.get('window')} | {_fmt(ex.get('delta_usd'), 0)} | "
                 f"{_fmt(ex.get('delta_r'))} | {ex.get('old_close')} | {ex.get('new_close')} |")
    if not tails["worst"]:
        L.append("| _none_ | | | | | | | |")
    L.append("")

    L.append("## Top 10 best signal_ids (old_paper beats new_logic_shadow)")
    L.append("| signal_id | asset/mode | entry_mode | window | delta $ | delta R | old close | new close |")
    L.append("|---|---|---|---|--:|--:|---|---|")
    for ex in tails["best"]:
        L.append(f"| {ex.get('signal_id')} | {ex.get('asset_class')}/{ex.get('mode')} | "
                 f"{ex.get('entry_mode')} | {ex.get('window')} | {_fmt(ex.get('delta_usd'), 0)} | "
                 f"{_fmt(ex.get('delta_r'))} | {ex.get('old_close')} | {ex.get('new_close')} |")
    if not tails["best"]:
        L.append("| _none_ | | | | | | | |")
    L.append("")

    L += ["## Forward-only cross-check",
          "_The same headline numbers, restricted to forward_since_activation pairs only — confirms "
          "whether the all-windows pattern above holds up in the (currently thin) live sample._",
          f"- n={fwd['executed_common']} common executed, old ${_fmt(fwd['old_book']['net_usd'],0)} vs "
          f"new ${_fmt(fwd['new_book']['net_usd'],0)}, delta ${_fmt(fwd['executed_sum_delta_usd'],0)}",
          ""]

    L.append("## Conclusion / recommendations")
    L.append("_Read the numbers above before trusting this section — it is a plain-language summary, not "
             "a substitute for the tables. No production-logic changes were made or are proposed here to "
             "apply automatically; any action requires a separate, explicit change with its own review._")
    return "\n".join(L)


def write_report(result: dict[str, Any] | None = None, *, db: str | None = None,
                 now_iso: str | None = None, path: str | None = None) -> str:
    if result is None:
        result = diagnose(db=db, now_iso=now_iso)
    md = render_markdown(result)
    out = Path(path) if path else _ROOT / "reports" / "OLD_PAPER_UNDERPERFORMANCE_DIAGNOSTIC.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    return str(out)


__all__ = ["diagnose", "rebuild_and_diagnose", "expiry_audit_before", "expiry_audit_after",
           "render_markdown", "write_report", "slice_stats", "group_pairs",
           "global_tails", "chase_avoided_stats", "VERSION"]
