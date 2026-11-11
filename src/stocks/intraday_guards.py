"""Read-only rolling-performance guards for stocks INTRADAY (paper / actionability only).

Computes recent A/B performance from `paper_execution_r` (NOT legacy final_r) by joining
`proposed_signals` → `paper_execution_outcomes`, then decides whether NEW A/B ideas should be
demoted to C (watchlist/review). This module ONLY reads and returns cap_reasons — it never writes,
never changes scoring math, never touches live/auto-live/manual-live, and only ever looks at
`asset_class='stocks' AND mode='intraday'` (crypto is never affected).

Guards:
  * global 7-day circuit breaker (both directions) → `stocks_intraday_7d_drawdown_guard`
  * per-direction guard (long / short cohorts, 7d + 14d) → `stocks_intraday_long_guard` /
    `stocks_intraday_short_guard`; a LONG can survive its weak-cohort guard with extra confirmation.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Any

from src.execution.paper_execution_accounting import EVIDENCE_FORWARD, EVIDENCE_BACKFILL

CB_REASON = "stocks_intraday_7d_drawdown_guard"
LONG_REASON = "stocks_intraday_long_guard"
SHORT_REASON = "stocks_intraday_short_guard"


def _conn(store_or_conn):
    """Accept a SQLiteStore (has .connect()) or a live sqlite3.Connection; return (conn, own)."""
    if isinstance(store_or_conn, sqlite3.Connection):
        return store_or_conn, False
    if hasattr(store_or_conn, "connect"):
        return store_or_conn.connect(), True
    raise TypeError("expected SQLiteStore or sqlite3.Connection")


def _now(now: datetime | None) -> datetime:
    return now or datetime.now(timezone.utc)


def _parse_dt(value: Any) -> datetime | None:
    if value is None:
        return None
    try:
        text = str(value).strip()
        if not text:
            return None
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def _reset_at(cfg_risk: dict | None = None, reset_at_utc: Any = None) -> datetime | None:
    if reset_at_utc is not None:
        return _parse_dt(reset_at_utc)
    g = (cfg_risk or {}).get("intraday_guards") or {}
    return _parse_dt(g.get("reset_at_utc"))


def _cutoff_iso(*, lookback_days: int, now: datetime | None = None,
                cfg_risk: dict | None = None, reset_at_utc: Any = None) -> str:
    cutoff = _now(now).astimezone(timezone.utc) - timedelta(days=int(lookback_days))
    reset = _reset_at(cfg_risk, reset_at_utc)
    if reset and reset > cutoff:
        cutoff = reset
    return cutoff.isoformat()


def rolling_ab_performance(store_or_conn, *, direction: str | None = None,
                           paper_entry_profile: str | None = None,
                           lookback_days: int = 7, now: datetime | None = None,
                           cfg_risk: dict | None = None,
                           reset_at_utc: Any = None) -> dict[str, Any]:
    """Return a clean rolling cohort for stocks intraday.

    A versioned Paper profile must be judged only on its own resolved,
    point-in-time forward outcomes.  Older generic callers can omit
    ``paper_entry_profile`` and retain the legacy broad cohort while the
    per-profile Paper adapters supply their own profile id.
    """
    conn, own = _conn(store_or_conn)
    try:
        cutoff = _cutoff_iso(lookback_days=lookback_days, now=now,
                             cfg_risk=cfg_risk, reset_at_utc=reset_at_utc)
        outcome_cols = {
            str(row[1]) for row in conn.execute("PRAGMA table_info(paper_execution_outcomes)")
        }
        if paper_entry_profile and "paper_entry_profile" not in outcome_cols:
            return {"n": 0, "net_r": 0.0, "pf": None, "winrate": None,
                    "wins": 0, "losses": 0}
        order = "o.rowid DESC"
        if "computed_at" in outcome_cols:
            order = "COALESCE(o.computed_at, '') DESC, o.rowid DESC"
        sql = (
            "WITH latest AS ("
            "SELECT o.*, ROW_NUMBER() OVER (PARTITION BY o.signal_id ORDER BY " + order + ") rn "
            "FROM paper_execution_outcomes o) "
            "SELECT o.paper_execution_r AS r FROM proposed_signals p "
            "JOIN latest o ON o.signal_id = p.signal_id AND o.rn=1 "
            "WHERE p.asset_class='stocks' AND p.mode='intraday' AND p.tier IN ('A','B') "
            "AND o.paper_execution_r IS NOT NULL AND p.created_at >= ?"
        )
        params: list[Any] = [cutoff]
        if paper_entry_profile:
            sql += " AND o.paper_entry_profile = ?"
            params.append(str(paper_entry_profile))
            # A profile-level circuit breaker must never be armed by an old
            # backfill, an invalid session, or a simulated no-entry row.
            if "evidence_class" in outcome_cols:
                sql += " AND o.evidence_class = 'forward_postfreeze'"
            if "execution_validity" in outcome_cols:
                sql += " AND COALESCE(o.execution_validity, 'valid') = 'valid'"
            if "lifecycle_state" in outcome_cols:
                sql += " AND o.lifecycle_state = 'CLOSED'"
        if direction:
            sql += " AND p.direction = ?"
            params.append(direction)
        rows = [float(x["r"]) for x in conn.execute(sql, params).fetchall() if x["r"] is not None]
    except sqlite3.Error:
        rows = []
    finally:
        if own:
            conn.close()
    n = len(rows)
    wins = [r for r in rows if r > 0]
    losses = [r for r in rows if r < 0]
    gross_win = sum(wins)
    gross_loss = abs(sum(losses))
    pf = (gross_win / gross_loss) if gross_loss > 0 else (float("inf") if wins else None)
    return {"n": n, "net_r": round(sum(rows), 3), "pf": (round(pf, 3) if isinstance(pf, float) and pf != float("inf") else pf),
            "winrate": (round(len(wins) / n, 4) if n else None), "wins": len(wins), "losses": len(losses)}


def _is_weak(perf: dict, *, pf_below: float, netr_below: float, min_trades: int) -> bool:
    if perf["n"] < min_trades:
        return False
    pf = perf["pf"]
    pf_weak = pf is not None and pf != float("inf") and pf < pf_below
    return bool(pf_weak or perf["net_r"] < netr_below)


def guard_cap_reasons(store_or_conn, cfg_risk: dict, *, direction: str,
                      long_confirmation_ok: bool = False,
                      paper_entry_profile: str | None = None,
                      now: datetime | None = None) -> list[str]:
    """Return the cap_reasons a NEW stocks-intraday A/B idea earns from the rolling guards (empty =
    healthy). The caller demotes the idea to C if this list is non-empty. Read-only."""
    g = (cfg_risk or {}).get("intraday_guards") or {}
    reasons: list[str] = []
    conn, own = _conn(store_or_conn)
    try:
        # --- global 7-day circuit breaker (both directions) ---
        # `global_guard_blocks_all_directions` (default True): when the overall 7d A/B cohort is in
        # drawdown this blocks NEW A/B of BOTH directions — the most conservative safety stop, even
        # if e.g. shorts are individually profitable. Set False to rely only on the per-direction
        # guards. Either way the report/packet show side-specific stats so the asymmetry is visible.
        cb = g.get("circuit_breaker") or {}
        global_blocks = bool(g.get("global_guard_blocks_all_directions", True))
        both = rolling_ab_performance(
            conn, direction=None, paper_entry_profile=paper_entry_profile,
            lookback_days=int(cb.get("lookback_days", 7)), now=now, cfg_risk=cfg_risk,
        )
        cb_weak = _is_weak(both, pf_below=float(cb.get("demote_if_pf_below", 0.8)),
                           netr_below=float(cb.get("demote_if_netr_below", -3.0)),
                           min_trades=int(cb.get("min_cohort_trades", 4)))
        # 2026-07-13 audit: the global breaker previously had no per-idea escape at all -- it demotes
        # every new A/B for the full lookback_days regardless of that idea's own quality. Opt-in
        # (default off): a LONG that already clears the existing strict long_extra_confirmation bar
        # also survives the GLOBAL block, same as it already does for the per-direction guard below.
        cb_bypassed = (direction == "long" and long_confirmation_ok
                      and bool(cb.get("long_confirmation_bypass", False)))
        if global_blocks and cb_weak and not cb_bypassed:
            reasons.append(CB_REASON)

        # --- per-direction guard (7d + the configured primary window) ---
        dg = g.get("direction_guard") or {}
        primary = int(dg.get("lookback_days", 14))
        windows = sorted({7, primary})
        weak_dir = any(
            _is_weak(rolling_ab_performance(
                conn, direction=direction, paper_entry_profile=paper_entry_profile,
                lookback_days=w, now=now, cfg_risk=cfg_risk,
            ),
                     pf_below=float(dg.get("demote_if_pf_below", 0.8)),
                     netr_below=float(dg.get("demote_if_netr_below", -3.0)),
                     min_trades=int(dg.get("min_cohort_trades", 4)))
            for w in windows)
        if weak_dir:
            # A long can survive with extra confirmation; a short (no confirmation set) is demoted.
            if direction == "long" and long_confirmation_ok:
                pass
            else:
                reasons.append(LONG_REASON if direction == "long" else SHORT_REASON)
    finally:
        if own:
            conn.close()
    return reasons


def long_confirmation_ok(idea: dict, cfg_risk: dict) -> bool:
    """Extra confirmation that lets a LONG survive a weak-long-cohort guard.

    STRICT — missing / unknown data is NEVER treated as confirmation. `rs_vs_spy > 0` is always
    required. The volume / sector / ATR-extension checks only apply when they are configured, but
    when a check applies the value must be EXPLICITLY known and pass; an absent value fails it.
    """
    conf = ((cfg_risk or {}).get("intraday_guards") or {}).get("long_extra_confirmation") or {}

    def _num(v):
        try:
            return None if v is None else float(v)
        except (TypeError, ValueError):
            return None

    # 1) RS vs SPY — always required; missing or <= 0 → not confirmed.
    if conf.get("require_rs_vs_spy_positive", True):
        rs = _num(idea.get("rs_vs_spy"))
        if rs is None or rs <= 0:
            return False

    # 2) Relative volume — if a minimum is configured, volume_ratio MUST be known and >= it.
    vmin = conf.get("min_volume_ratio", conf.get("volume_ratio_min"))
    if vmin is not None:
        vr = _num(idea.get("volume_ratio"))
        if vr is None or vr < float(vmin):
            return False

    # 3) Sector — if required, we must EXPLICITLY know the sector is not weak/contradicting.
    #    Both flags unknown (None) → not confirmation.
    if conf.get("require_sector_not_weak", conf.get("require_sector_not_contradict", True)):
        sc = idea.get("sector_contradicts")
        sw = idea.get("sector_weak")
        if sc is True or sw is True:
            return False
        if sc is None and sw is None:
            return False

    # 4) ATR extension — if a max is configured, atr_extension MUST be known and <= it.
    amax = conf.get("max_atr_extension_from_entry", conf.get("max_atr_extension"))
    if amax is not None:
        ext = idea.get("atr_extension")
        if ext is None:
            ext = idea.get("atr_from_entry")
        ext = _num(ext)
        if ext is None or ext > float(amax):
            return False

    return True


def _raw_json(v):
    import json
    try:
        return json.loads(v) if v else {}
    except Exception:
        return {}


def _sector_from(sector_col, raw: dict) -> str | None:
    """Sector with a read-time fallback: the proposed_signals.sector column first, then
    raw_idea_json.structured.sector / .candidate.sector. Only None if truly nowhere. Non-destructive
    (never rewrites the row)."""
    if sector_col and str(sector_col).strip():
        return str(sector_col)
    st = raw.get("structured") or {}
    cand = raw.get("candidate") or {}
    for src in (st.get("sector"), cand.get("sector")):
        if src and str(src).strip():
            return str(src)
    return None


def recovery_stats(store_or_conn, *, lookback_days: int = 14, direction: str | None = None,
                   now: datetime | None = None, cfg_risk: dict | None = None,
                   reset_at_utc: Any = None) -> dict[str, Any]:
    """Would-have-been-A/B diagnostics: stocks-intraday signals whose PRE-GATE tier was A/B (from
    raw_idea_json.pre_gate_tier), INCLUDING those a gate demoted to C, joined to their
    paper_execution_r outcome. Read-only and SEPARATE from the authoritative rolling guard (which
    uses the FINAL tier) — lets us see whether demoted near-A/B setups would have recovered."""
    conn, own = _conn(store_or_conn)
    try:
        cutoff = _cutoff_iso(lookback_days=lookback_days, now=now,
                             cfg_risk=cfg_risk, reset_at_utc=reset_at_utc)
        try:
            rows = conn.execute(
                "SELECT p.direction AS direction, p.tier AS final_tier, p.raw_idea_json AS raw, "
                "o.paper_execution_r AS r FROM proposed_signals p "
                "JOIN paper_execution_outcomes o ON o.signal_id = p.signal_id "
                "WHERE p.asset_class='stocks' AND p.mode='intraday' "
                "AND o.paper_execution_r IS NOT NULL AND p.created_at >= ?", (cutoff,)).fetchall()
        except sqlite3.Error:
            rows = []
    finally:
        if own:
            conn.close()
    would = []           # (direction, r, pre_gate_tier, final_tier)
    for row in rows:
        raw = _raw_json(row["raw"])
        pre = str(raw.get("pre_gate_tier") or "")
        final = str(row["final_tier"] or "")
        if pre in ("A", "B") or final in ("A", "B"):
            if direction and row["direction"] != direction:
                continue
            would.append((row["direction"], float(row["r"]), pre, final))
    nets = [r for _, r, _, _ in would]
    demoted = [w for w in would if w[2] in ("A", "B") and w[3] not in ("A", "B")]
    wins = [r for r in nets if r > 0]
    losses = [r for r in nets if r < 0]
    gl, gw = abs(sum(losses)), sum(wins)
    pf = (gw / gl) if gl > 0 else (float("inf") if wins else None)
    return {"n": len(would), "demoted_n": len(demoted), "net_r": round(sum(nets), 3),
            "pf": (round(pf, 3) if isinstance(pf, float) and pf != float("inf") else pf),
            "winrate": round(len(wins) / len(would), 4) if would else None,
            "demoted_net_r": round(sum(r for _, r, _, _ in demoted), 3)}


def _rr_bucket(rr) -> str:
    try:
        rr = float(rr)
    except (TypeError, ValueError):
        return "unknown"
    if rr < 1.5:
        return "<1.5R"
    if rr < 2.0:
        return "1.5-2R"
    return ">2R"


def ab_breakdowns(store_or_conn, *, lookback_days: int = 30, now: datetime | None = None,
                  cfg_risk: dict | None = None, reset_at_utc: Any = None) -> dict[str, Any]:
    """A/B stocks-intraday paper performance (paper_execution_r) sliced by direction / regime /
    setup_type / sector / catalyst / RR-bucket over the window. Read-only. Each slice → {n, net_r,
    winrate}."""
    conn, own = _conn(store_or_conn)
    try:
        cutoff = _cutoff_iso(lookback_days=lookback_days, now=now,
                             cfg_risk=cfg_risk, reset_at_utc=reset_at_utc)
        try:
            rows = conn.execute(
                "SELECT p.direction AS direction, p.market_regime AS regime, p.setup_type AS setup, "
                "p.sector AS sector, p.news_supported AS news, p.expected_rr_tp1 AS rr, "
                "p.raw_idea_json AS raw, o.paper_execution_r AS r "
                "FROM proposed_signals p JOIN paper_execution_outcomes o ON o.signal_id = p.signal_id "
                "WHERE p.asset_class='stocks' AND p.mode='intraday' AND p.tier IN ('A','B') "
                "AND o.paper_execution_r IS NOT NULL AND p.created_at >= ?", (cutoff,)).fetchall()
        except sqlite3.Error:
            rows = []
    finally:
        if own:
            conn.close()

    def agg(keyfn):
        d: dict[str, dict] = {}
        for row in rows:
            k = keyfn(row) or "unknown"
            a = d.setdefault(str(k), {"n": 0, "net_r": 0.0, "_w": 0})
            r = float(row["r"])
            a["n"] += 1
            a["net_r"] = round(a["net_r"] + r, 3)
            a["_w"] += 1 if r > 0 else 0
        for a in d.values():
            a["winrate"] = round(a.pop("_w") / a["n"], 3) if a["n"] else None
        return d

    return {
        "lookback_days": lookback_days, "n": len(rows),
        "by_direction": agg(lambda r: r["direction"]),
        "by_regime": agg(lambda r: r["regime"]),
        "by_setup": agg(lambda r: r["setup"]),
        "by_catalyst": agg(lambda r: "news_supported" if r["news"] else "no_news"),
        "by_rr_bucket": agg(lambda r: _rr_bucket(r["rr"])),
        # sector uses the read-time fallback (column → raw_idea_json.structured/candidate)
        "by_sector": agg(lambda r: _sector_from(r["sector"], _raw_json(r["raw"]))),
    }


def evidence_class_breakdown(store_or_conn, *, lookback_days: int = 7, now: datetime | None = None,
                             cfg_risk: dict | None = None, reset_at_utc: Any = None) -> dict[str, Any]:
    """Model-F evidence-class split (forward_postfreeze vs backfill_pretrained vs unclassified) over the
    SAME A/B stocks-intraday population rolling_ab_performance draws from. DIAGNOSTIC ONLY — does NOT
    feed cap_reasons / the circuit breaker, which intentionally looks at ALL recent trades regardless of
    evidence class (a drawdown guard must not ignore recent losses just because they predate the freeze).
    Only cites forward_postfreeze as validated edge; backfill_pretrained is the in-sample data that chose
    Model F's own thresholds and must never be read as "profitable" on its own."""
    conn, own = _conn(store_or_conn)
    try:
        cutoff = _cutoff_iso(lookback_days=lookback_days, now=now, cfg_risk=cfg_risk, reset_at_utc=reset_at_utc)
        try:
            has_evidence = any(r[1] == "evidence_class"
                               for r in conn.execute("PRAGMA table_info(paper_execution_outcomes)"))
            evidence_col = "o.evidence_class" if has_evidence else "NULL"
            rows = conn.execute(
                f"SELECT o.paper_execution_r AS r, {evidence_col} AS ec FROM proposed_signals p "
                "JOIN paper_execution_outcomes o ON o.signal_id = p.signal_id "
                "WHERE p.asset_class='stocks' AND p.mode='intraday' AND p.tier IN ('A','B') "
                "AND o.paper_execution_r IS NOT NULL AND p.created_at >= ?", (cutoff,)).fetchall()
        except sqlite3.Error:
            rows = []
    finally:
        if own:
            conn.close()
    fwd = [float(x["r"]) for x in rows if x["ec"] == EVIDENCE_FORWARD]
    bfd = [float(x["r"]) for x in rows if x["ec"] == EVIDENCE_BACKFILL]
    unc = [float(x["r"]) for x in rows if x["ec"] not in (EVIDENCE_FORWARD, EVIDENCE_BACKFILL)]

    def stats(vals):
        return {"n": len(vals), "resolved": len(vals), "net_r_sum": round(sum(vals), 4) if vals else None}

    return {"forward_postfreeze": stats(fwd), "backfill_pretrained": stats(bfd), "unclassified": stats(unc)}


def cohort_stats_for_report(store_or_conn, *, now: datetime | None = None,
                            cfg_risk: dict | None = None,
                            reset_at_utc: Any = None) -> dict[str, Any]:
    """Compact rolling stats for the report / LLM packet: global + long + short over 7/14/30d.
    Read-only; uses paper_execution_r. `evidence` is the Model-F forward/backfill/unclassified
    split for the 'all' cohort at each window — diagnostic context only, never feeds the guard math."""
    conn, own = _conn(store_or_conn)
    try:
        out: dict[str, Any] = {}
        for label, direction in (("all", None), ("long", "long"), ("short", "short")):
            out[label] = {f"{w}d": rolling_ab_performance(conn, direction=direction, lookback_days=w,
                                                          now=now, cfg_risk=cfg_risk,
                                                          reset_at_utc=reset_at_utc)
                          for w in (7, 14, 30)}
        out["evidence"] = {f"{w}d": evidence_class_breakdown(conn, lookback_days=w, now=now,
                                                              cfg_risk=cfg_risk, reset_at_utc=reset_at_utc)
                           for w in (7, 14, 30)}
        return out
    finally:
        if own:
            conn.close()
