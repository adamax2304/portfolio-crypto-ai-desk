"""SI-7 — deterministic post-trade classifier for stock-intraday PAPER trades. READ-MODEL only.

After a stock-intraday paper trade closes, classify WHY it won / lost / expired using deterministic
rules over the outcome (Model-F `paper_execution_r`, close_reason) + the actionability-gate context
that was recorded at signal creation. No realtime LLM dependency (the scheduled LLM review may
comment later, but the core classifier is pure). Profitability is R-based (paper_execution_r) —
never legacy final_r.

Writes ONLY the additive read-model table `stocks_intraday_post_trade_diagnostics`. Never touches
proposed_signals / signal_outcomes / final_r / live / crypto.
"""

from __future__ import annotations

import json
import sqlite3
from typing import Any

from src.execution.paper_execution_accounting import EVIDENCE_FORWARD, EVIDENCE_BACKFILL

VERSION = "si7_post_trade_v1"

FAILURE_CATEGORIES = (
    "market_reversal", "sector_failed", "no_volume_followthrough", "late_entry", "chase_entry",
    "weak_or_stale_catalyst", "spread_slippage_cost", "data_gap_late", "stop_too_tight",
    "tp_too_far", "earnings_or_news_risk", "correlated_sector_drawdown",
    # honest bucket for trades that predate the SI-1..5 gates (no recorded market/sector/session/
    # liquidity/catalyst context) — never fabricate a specific cause where none was measured.
    "no_gate_context", "unknown",
)
SUCCESS_CATEGORIES = (
    "catalyst_followthrough", "sector_momentum_confirmed", "market_trend_aligned", "vwap_hold",
    "orb_followthrough", "rvol_expansion", "clean_pullback_retest",
)

_DDL = """
CREATE TABLE IF NOT EXISTS stocks_intraday_post_trade_diagnostics (
  signal_id TEXT PRIMARY KEY, closed_at TEXT, outcome TEXT, net_pnl_usdt REAL, paper_execution_r REAL,
  entry_mode TEXT, setup_type TEXT, session_phase TEXT, market_context_status TEXT,
  sector_confirmation_status TEXT, liquidity_status TEXT, catalyst_quality TEXT,
  failure_reason_primary TEXT, failure_reason_secondary TEXT, success_reason_primary TEXT,
  notes_json TEXT, computed_at TEXT, version TEXT
);
"""

# ALTER TABLE migration for any DB created before evidence_class existed (mirrors
# paper_execution_accounting._NEW_COLUMNS — never touches signal_outcomes/final_r).
_NEW_COLUMNS = (("evidence_class", "TEXT"),)


def _ensure_table(conn) -> None:
    conn.execute(_DDL)
    existing = {r[1] for r in conn.execute("PRAGMA table_info(stocks_intraday_post_trade_diagnostics)")}
    for col, typ in _NEW_COLUMNS:
        if col not in existing:
            try:
                conn.execute(f"ALTER TABLE stocks_intraday_post_trade_diagnostics ADD COLUMN {col} {typ}")
            except Exception:
                pass


def _num(v):
    try:
        return None if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return None


def _active_fee_profile() -> str:
    """The authoritative paper fee profile (same one the UI / control-plane headline uses):
    config/paper_portfolio.yaml:paper_portfolio.fee_profile, default bybit_non_vip_usdt_perp. The
    ledger stores one exit row PER profile per signal — we must read the ACTIVE profile only, never an
    arbitrary one (for stocks the fee math may map to stock_etf_default internally, but the ledger
    row's outer fee_profile is this active key)."""
    try:
        from src.execution.paper_portfolio import load_cfg
        return str((load_cfg() or {}).get("fee_profile") or "bybit_non_vip_usdt_perp")
    except Exception:
        return "bybit_non_vip_usdt_perp"


def classify_trade(row: dict) -> dict:
    """Pure: map a closed trade + its gate context to outcome + failure/success reasons.

    `row` keys: paper_execution_r, close_reason, session_phase, market_context_status,
    sector_confirmation_status, liquidity_status, catalyst_quality, setup_type, entry_mode.
    """
    r = _num(row.get("paper_execution_r"))
    close = str(row.get("close_reason") or "").lower()
    phase = str(row.get("session_phase") or "").lower()
    mkt = str(row.get("market_context_status") or "").lower()
    sec = str(row.get("sector_confirmation_status") or "").lower()
    liq = str(row.get("liquidity_status") or "").lower()
    cat = str(row.get("catalyst_quality") or "").lower()
    setup = str(row.get("setup_type") or "").lower()
    # Whether ANY SI-1..5 gate context was recorded for this trade. Trades created before the gate
    # hook have all-empty context — we must NOT invent a specific failure cause for them (that would
    # be unexplainable). `cat in (weak/none/stale)` is an explicit verdict; `cat == ""` is missing data.
    has_ctx = any((phase, mkt, sec, liq, cat))
    cat_weak = cat in ("weak", "none", "stale")

    if r is None:
        outcome = "unknown"
    elif close in ("expired_flat",) or (abs(r) < 0.15 and close not in ("original_stop",)):
        outcome = "expired" if "expired" in close else ("scratch" if abs(r) < 0.15 else "win" if r > 0 else "loss")
    else:
        outcome = "win" if r > 0 else ("loss" if r < 0 else "scratch")

    fail1 = fail2 = success1 = None
    if outcome == "loss":
        # ordered by explanatory priority; first match = primary, next = secondary
        reasons = []
        if liq == "blocked" or "data_gap" in liq:
            reasons.append("data_gap_late" if "data_gap" in liq else "spread_slippage_cost")
        if mkt in ("conflict", "unknown"):
            reasons.append("market_reversal")
        if sec in ("conflict", "weak", "unknown"):
            reasons.append("sector_failed")
        if cat_weak:
            reasons.append("weak_or_stale_catalyst")
        if phase in ("first_15m", "premarket"):
            reasons.append("chase_entry")
        if phase == "last_30m":
            reasons.append("late_entry")
        # `stop_too_tight` is only a defensible hypothesis when context WAS recorded and every gate
        # was confirmed yet it still stopped out. With no context we cannot claim the stop was tight.
        if close in ("original_stop", "breakeven_stop") and not reasons and has_ctx:
            reasons.append("stop_too_tight")
        if not reasons:
            # No gate reason matched: attribute to missing context (pre-gate trade) vs a genuine
            # no-follow-through loss where context WAS recorded but all gates were confirmed.
            reasons.append("no_gate_context" if not has_ctx else "no_volume_followthrough")
        fail1 = reasons[0]
        fail2 = reasons[1] if len(reasons) > 1 else None
    elif outcome == "expired":
        fail1 = ("no_volume_followthrough" if cat_weak
                 else ("no_gate_context" if not has_ctx else "tp_too_far"))
    elif outcome == "win":
        if cat == "strong":
            success1 = "catalyst_followthrough"
        elif sec == "confirmed":
            success1 = "sector_momentum_confirmed"
        elif mkt == "ok":
            success1 = "market_trend_aligned"
        elif "orb" in setup or "opening" in setup:
            success1 = "orb_followthrough"
        else:
            success1 = "clean_pullback_retest"
    return {"outcome": outcome, "failure_reason_primary": fail1,
            "failure_reason_secondary": fail2, "success_reason_primary": success1}


def _gate_fields_from_raw(raw_json) -> dict:
    try:
        d = json.loads(raw_json) if raw_json else {}
    except (TypeError, ValueError):
        return {}
    g = d.get("intraday_actionability") or {}      # persisted by the trade-idea gate hook
    return {k: g.get(k) for k in ("session_phase", "market_context_status",
                                  "sector_confirmation_status", "liquidity_status", "catalyst_quality")}


def refresh(*, db: str | None = None, now_iso: str | None = None) -> dict[str, Any]:
    """Classify all CLOSED stock-intraday paper trades. Reads proposed_signals + paper_execution_outcomes
    (read-only); writes ONLY stocks_intraday_post_trade_diagnostics."""
    from datetime import datetime, timezone
    from src.config import load_config
    cfg = load_config()
    path = db or str(cfg.db_path)
    now = now_iso or datetime.now(timezone.utc).isoformat()
    conn = sqlite3.connect(path)
    try:
        _ensure_table(conn)
        def _has(t):
            return bool(conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (t,)).fetchone())
        if not (_has("proposed_signals") and _has("paper_execution_outcomes")):
            return {"updated": 0}
        # Authoritative USD PnL: the ledger stores one exit row PER fee_profile per signal, so we must
        # select the ACTIVE profile only (else the value is non-deterministic). Among the active
        # profile's exit rows we take the terminal one deterministically (MAX rowid). LEFT-joined in
        # code so a missing active-profile exit leaves net_pnl_usdt NULL + a note (never fabricated,
        # never a different profile). paper_execution_r stays auxiliary. Read-only — no ledger/final_r writes.
        has_ledger = _has("paper_portfolio_ledger")
        active_profile = _active_fee_profile()
        usd_by_sid: dict[str, float] = {}
        if has_ledger:
            for sid, pnl in conn.execute(
                "SELECT l.signal_id, l.net_pnl_usdt FROM paper_portfolio_ledger l "
                "JOIN (SELECT signal_id, MAX(rowid) AS rid FROM paper_portfolio_ledger "
                "      WHERE event_type='exit' AND fee_profile=? GROUP BY signal_id) t "
                "  ON t.signal_id=l.signal_id AND l.rowid=t.rid",
                (active_profile,)).fetchall():
                usd_by_sid[sid] = _num(pnl)
        has_evidence = any(r[1] == "evidence_class"
                          for r in conn.execute("PRAGMA table_info(paper_execution_outcomes)"))
        evidence_col = "o.evidence_class" if has_evidence else "NULL"
        rows = conn.execute(
            f"SELECT p.signal_id, p.setup_type, p.raw_idea_json, o.paper_execution_r, o.close_reason, "
            f"o.paper_execution_outcome, o.computed_at, {evidence_col} "
            "FROM paper_execution_outcomes o JOIN proposed_signals p ON p.signal_id=o.signal_id "
            "WHERE p.asset_class='stocks' AND p.mode='intraday' AND o.paper_execution_r IS NOT NULL "
            "AND o.close_reason NOT IN ('open','no_entry')").fetchall()
        updated = 0
        for sid, setup_type, raw, per, close, outcome_status, closed_at, evid in rows:
            gf = _gate_fields_from_raw(raw)
            row = {"paper_execution_r": per, "close_reason": close, "setup_type": setup_type, **gf}
            cls = classify_trade(row)
            net_usd = usd_by_sid.get(sid)   # authoritative USD PnL; NULL when no ledger exit row
            conn.execute(
                "INSERT OR REPLACE INTO stocks_intraday_post_trade_diagnostics VALUES "
                "(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (sid, closed_at, cls["outcome"], net_usd, _num(per),
                 None, setup_type, gf.get("session_phase"), gf.get("market_context_status"),
                 gf.get("sector_confirmation_status"), gf.get("liquidity_status"), gf.get("catalyst_quality"),
                 cls["failure_reason_primary"], cls["failure_reason_secondary"],
                 cls["success_reason_primary"],
                 json.dumps({"close_reason": close, "fee_profile": active_profile,
                             "net_pnl_usdt_source": (f"paper_portfolio_ledger.exit[{active_profile}]"
                                                     if net_usd is not None
                                                     else "unavailable_active_profile_missing")}),
                 now, VERSION, evid))
            updated += 1
            if updated % 50 == 0:
                conn.commit()
        conn.commit()
        return {"updated": updated, "generated_at": now}
    finally:
        conn.close()


def report_sections(db: str | None = None, lookback_days: int = 14) -> str:
    """Markdown: failure-reason table + R by failure_reason / session_phase / catalyst_quality /
    market_context_status / sector_confirmation_status + top avoidable-loss buckets."""
    from src.config import load_config
    path = db or str(load_config().db_path)
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        if not conn.execute("SELECT 1 FROM sqlite_master WHERE name='stocks_intraday_post_trade_diagnostics'").fetchone():
            return ""
        def _by(col, only_failures=False):
            # The failure-reason table is scoped to losses+expired so winners/scratch (which have no
            # failure reason) don't appear as a misleading positive "unknown failure" row. The other
            # breakdowns legitimately span all outcomes (net R by phase/catalyst/etc.).
            extra = " AND outcome IN ('loss','expired')" if only_failures else ""
            return conn.execute(
                f"SELECT COALESCE({col},'unknown'), COUNT(*), ROUND(SUM(paper_execution_r),2) "
                f"FROM stocks_intraday_post_trade_diagnostics WHERE closed_at >= date('now', ?){extra} "
                f"GROUP BY {col} ORDER BY SUM(paper_execution_r) ASC", (f"-{lookback_days} day",)).fetchall()
        L = [f"### Stocks-intraday post-trade diagnostics (last {lookback_days}d, paper R — not legacy final_r)", ""]
        has_evidence = any(r[1] == "evidence_class"
                          for r in conn.execute("PRAGMA table_info(stocks_intraday_post_trade_diagnostics)"))
        if has_evidence:
            ev = conn.execute(
                "SELECT COALESCE(evidence_class,'unclassified'), COUNT(*), ROUND(SUM(paper_execution_r),2) "
                "FROM stocks_intraday_post_trade_diagnostics WHERE closed_at >= date('now', ?) GROUP BY 1",
                (f"-{lookback_days} day",)).fetchall()
            ev_map = {r[0]: (r[1], r[2]) for r in ev}
            fwd = ev_map.get(EVIDENCE_FORWARD, (0, None))
            bfd = ev_map.get(EVIDENCE_BACKFILL, (0, None))
            unc_n = sum(v[0] for k, v in ev_map.items() if k not in (EVIDENCE_FORWARD, EVIDENCE_BACKFILL))
            L.append(f"**Evidence quality (Model F):** forward_postfreeze n={fwd[0]}"
                     f"{'' if fwd[1] is None else f' (ΣR={fwd[1]:+.2f})'} — only bucket usable as proof "
                     f"of edge; backfill_pretrained n={bfd[0]}"
                     f"{'' if bfd[1] is None else f' (ΣR={bfd[1]:+.2f})'} — in-sample data that chose "
                     f"Model F's own thresholds, hypothesis only; unclassified n={unc_n}.")
            L.append("")
        fr = _by("failure_reason_primary", only_failures=True)
        L.append("**By failure reason** (losses+expired only, worst R first):")
        L += [f"- `{r[0]}`: n={r[1]}, ΣR={r[2]:+.2f}" for r in fr if r[0] != "unknown" or r[1]] or ["- _none_"]
        for label, col in (("session_phase", "session_phase"), ("catalyst_quality", "catalyst_quality"),
                           ("market_context_status", "market_context_status"),
                           ("sector_confirmation_status", "sector_confirmation_status")):
            rows = _by(col)
            L.append("")
            L.append(f"**PnL(R) by {label}:**")
            L += [f"- `{r[0]}`: n={r[1]}, ΣR={r[2]:+.2f}" for r in rows] or ["- _none_"]
        # top avoidable loss buckets = failure reasons with the most negative ΣR
        avoid = [r for r in fr if (r[2] or 0) < 0][:3]
        if avoid:
            L.append("")
            L.append("**Top avoidable loss buckets:** " +
                     ", ".join(f"`{r[0]}` ({r[2]:+.2f}R over {r[1]})" for r in avoid))
        return "\n".join(L)
    finally:
        conn.close()


__all__ = ["classify_trade", "refresh", "report_sections", "FAILURE_CATEGORIES", "SUCCESS_CATEGORIES", "VERSION"]
