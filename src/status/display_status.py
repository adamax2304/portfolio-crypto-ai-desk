"""Canonical display-status taxonomy (read-only, presentation only).

Single source of truth for turning raw signal/trade lifecycle fields into
operator-facing display semantics, so Telegram / Control Plane / reports stop
showing a bare ``expired`` or a context-free ``+0R``.

ABSOLUTE: this module is *descriptive only*. It never mutates `status`,
`entry_triggered`, `final_r`, `final_outcome`, alerts, or any stored value, and it
never changes scoring / TP-SL / routing / actionability / entry logic. It reads a
row dict and returns display fields.

Key empirical fact this encodes (see reports/PRE_STATUS_CLARITY_BASELINE.md):
  * status == "expired"  AND entry_triggered  → ENTERED then UNRESOLVED (a trade
    was opened; it just didn't hit TP/SL before the validity window). NOT a miss.
  * status in {missed_no_entry, stale_before_entry, entry_moved_away, ...} with
    entry_triggered = 0 → the price never reached the entry zone. A real no-entry.
"""
from __future__ import annotations

import json
from typing import Any

# ---- canonical display groups -------------------------------------------------
OPEN_ACTIVE = "OPEN_ACTIVE"
WAITING_FOR_ENTRY = "WAITING_FOR_ENTRY"
REVIEW_ONLY_SHADOW = "REVIEW_ONLY_SHADOW"
ENTERED_UNRESOLVED_EXPIRED = "ENTERED_UNRESOLVED_EXPIRED"
NO_ENTRY_EXPIRED = "NO_ENTRY_EXPIRED"
CLOSED_WIN = "CLOSED_WIN"
CLOSED_LOSS = "CLOSED_LOSS"
CLOSED_FLAT = "CLOSED_FLAT"
UNKNOWN_INCONSISTENT = "UNKNOWN_INCONSISTENT"

DISPLAY_GROUPS = (
    OPEN_ACTIVE, WAITING_FOR_ENTRY, REVIEW_ONLY_SHADOW,
    ENTERED_UNRESOLVED_EXPIRED, NO_ENTRY_EXPIRED,
    CLOSED_WIN, CLOSED_LOSS, CLOSED_FLAT, UNKNOWN_INCONSISTENT,
)

# raw status buckets ------------------------------------------------------------
_OPEN_ENTERED = {"triggered", "tp1_hit", "tp2_hit"}
_WAITING = {"generated", "waiting_for_entry"}
_NO_ENTRY_STATUSES = {
    "missed_no_entry", "stale_before_entry", "entry_moved_away",
    "invalidated_before_entry", "cancelled_by_regime_change", "cancelled_by_news",
}
_NO_ENTRY_REASON = {
    "missed_no_entry": "price never touched the entry zone before the window ended",
    "stale_before_entry": "signal aged out waiting for entry (stale)",
    "entry_moved_away": "price ran away from the entry zone before a fill",
    "invalidated_before_entry": "invalidated before entry",
    "cancelled_by_regime_change": "cancelled — market regime changed",
    "cancelled_by_news": "cancelled — news event",
}
STOCKS_SWING_EVENT_RS_PROFILES = {
    "stocks_swing_event_rs_pullback_quality_paper_v1",
    "stocks_swing_event_rs_pullback_flow_paper_v1",
}


def _truthy(v: Any) -> bool | None:
    """Tri-state truthiness: True/False, or None when genuinely unknown."""
    if v is None or v == "":
        return None
    if isinstance(v, str):
        return v.strip().lower() in {"1", "true", "yes", "y"}
    try:
        return bool(int(v))
    except Exception:
        return bool(v)


def _to_float(v: Any) -> float | None:
    try:
        if v is None or v == "":
            return None
        return float(v)
    except Exception:
        return None


def _raw_payload(row: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(row, dict):
        return {}
    raw = row.get("raw_idea_json")
    if isinstance(raw, dict):
        return dict(raw)
    try:
        parsed = json.loads(raw or "{}")
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def _paper_profile(row: dict[str, Any] | None) -> str:
    if not isinstance(row, dict):
        return ""
    direct = str(row.get("paper_entry_profile") or "").strip()
    if direct:
        return direct
    return str(_raw_payload(row).get("paper_entry_profile") or "").strip()


def _is_actionable_by_policy(tier: str, mode: str, asset: str, conc: str,
                             row: dict[str, Any] | None = None) -> bool | None:
    """Mirror (not authoritative) of `decide_paper_entry` / Control-Plane actionability.

    The authoritative gate stays in src/notifiers/paper_entry.py; this only
    *describes* whether a row is actionable for display bucketing. Pass an explicit
    ``is_actionable`` / ``actionability_status`` in the row to override.
    """
    if not tier:
        return None
    t = tier.upper()
    if t not in {"A", "B"}:
        return False                                   # C / watchlist / rejected
    if asset == "crypto" and mode == "scalp":
        return False                                   # scalp shadow-only (locked)
    if asset == "stocks" and mode == "swing" and _paper_profile(row) in STOCKS_SWING_EVENT_RS_PROFILES:
        return True
    if asset == "stocks" and mode in {"swing", "invest"}:
        return False                                   # not actionable by policy
    if conc in {"shadow_proxy_duplicate", "shadow_sector_cap"}:
        return False
    return True


def derive_display_status(row: dict[str, Any]) -> dict[str, Any]:
    """Return display semantics for a proposed-signal / trade row. Pure + fail-open.

    Recognised (all optional) row keys: status, entry_triggered, final_outcome,
    final_r, tier, mode, asset_class, concentration_status, max_favorable_excursion_r,
    mfe_r, alerts / paper_alert_sent / has_alert, is_actionable, actionability_status.
    """
    status = str(row.get("status") or "").strip().lower()
    final_outcome = str(row.get("final_outcome") or "").strip().lower()
    final_r = _to_float(row.get("final_r"))
    paper_outcome = str(row.get("paper_execution_outcome") or "").strip().lower()
    paper_r = _to_float(row.get("paper_execution_r"))
    paper_close_reason = str(row.get("paper_close_reason") or row.get("close_reason") or "").strip()
    paper_terminal = paper_outcome in {"win", "loss", "flat", "breakeven", "expired"}
    effective_r = paper_r if paper_terminal and paper_r is not None else final_r
    r_source = "paper execution" if paper_terminal else "legacy touch"
    entry_triggered = _truthy(row.get("entry_triggered"))
    # Control-Plane rows carry entry_triggered_at instead of a flag.
    if entry_triggered is None and row.get("entry_triggered_at"):
        entry_triggered = True
    tier = str(row.get("tier") or "")
    mode = str(row.get("mode") or "").strip().lower()
    asset = str(row.get("asset_class") or "crypto").strip().lower()
    conc = str(row.get("concentration_status") or "").strip().lower()
    mfe_r = _to_float(row.get("max_favorable_excursion_r"))
    if mfe_r is None:
        mfe_r = _to_float(row.get("mfe_r"))

    # actionability (override-aware)
    if row.get("is_actionable") is not None:
        is_actionable: bool | None = bool(row.get("is_actionable"))
    elif row.get("actionability_status"):
        a = str(row.get("actionability_status")).lower()
        is_actionable = a == "actionable"
    else:
        is_actionable = _is_actionable_by_policy(tier, mode, asset, conc, row)
    is_shadow = (is_actionable is False)

    # paper-alert evidence (optional)
    alerts_n = row.get("alerts")
    if alerts_n is None:
        alerts_n = row.get("alert_count")
    paper_alert_sent: bool | None
    if row.get("paper_alert_sent") is not None:
        paper_alert_sent = bool(row.get("paper_alert_sent"))
    elif row.get("has_alert") is not None:
        paper_alert_sent = bool(row.get("has_alert"))
    elif alerts_n is not None:
        try:
            paper_alert_sent = int(alerts_n) > 0
        except Exception:
            paper_alert_sent = None
    else:
        paper_alert_sent = None

    has_terminal_close = bool(final_outcome) and final_outcome not in {"expired", "not_triggered", "missed"}

    # ---- precedence resolution -------------------------------------------------
    group: str
    reason: str

    # A. A point-in-time Paper session can be invalidated before an entry, even
    # when legacy touch tracking later labels a TP.  The invalid-session outcome
    # is authoritative for execution: it was never a trade and must not remain
    # an ambiguous lifecycle row in the operator view.
    if (str(paper_outcome or "").lower() in {"invalid_session", "no_entry", "not_triggered"}
            and entry_triggered is not True):
        group, reason = (
            NO_ENTRY_EXPIRED,
            f"paper entry invalidated before execution ({paper_close_reason or paper_outcome})",
        )

    # B. Authoritative Model-F terminal accounting wins over legacy touch/status ambiguity. This is
    # display reconciliation only: no source row is rewritten.
    elif paper_terminal:
        if effective_r is not None and effective_r > 0:
            group, reason = CLOSED_WIN, f"closed by paper execution ({paper_close_reason or paper_outcome})"
        elif effective_r is not None and effective_r < 0:
            group, reason = CLOSED_LOSS, f"closed by paper execution ({paper_close_reason or paper_outcome})"
        else:
            group, reason = CLOSED_FLAT, f"closed flat by paper execution ({paper_close_reason or paper_outcome})"

    # C. inconsistent combinations (impossible lifecycle without a reconciled paper result).
    elif status == "ambiguous" or final_outcome == "ambiguous":
        group, reason = UNKNOWN_INCONSISTENT, "ambiguous lifecycle — needs review"
    elif status in _NO_ENTRY_STATUSES and entry_triggered is True:
        group, reason = (
            UNKNOWN_INCONSISTENT,
            f"status '{status}' but entry_triggered=1 — inconsistent, needs review",
        )

    # D. terminal closed outcomes (a real exit happened). Classify by the SIGN of
    #    final_r when present; if the win/loss label contradicts the sign, surface
    #    it as inconsistent rather than printing a nonsense "+-1.0R".
    elif has_terminal_close or status in {"stopped", "tp3_hit"}:
        win_ish = (final_outcome == "win") or (status == "tp3_hit")
        loss_ish = (final_outcome == "loss") or (status == "stopped")
        if final_r is not None and win_ish and final_r < 0:
            group, reason = UNKNOWN_INCONSISTENT, "labelled win but final_r<0 — inconsistent"
        elif final_r is not None and loss_ish and final_r > 0:
            group, reason = UNKNOWN_INCONSISTENT, "labelled loss but final_r>0 — inconsistent"
        elif final_r is not None and final_r == 0:
            group, reason = CLOSED_FLAT, "closed flat at break-even (0R)"
        elif (final_r is not None and final_r > 0) or (final_r is None and win_ish):
            group, reason = CLOSED_WIN, "closed at a winning R"
        elif (final_r is not None and final_r < 0) or (final_r is None and loss_ish):
            group, reason = CLOSED_LOSS, "stopped out / closed at a losing R"
        else:
            group, reason = UNKNOWN_INCONSISTENT, "terminal close without resolvable R/outcome"

    # E. expired AFTER entry — entered, just unresolved within the window.
    elif status == "expired" and entry_triggered is True:
        group, reason = (
            ENTERED_UNRESOLVED_EXPIRED,
            "entry was filled but neither TP nor SL hit before the validity window ended",
        )

    # F. no-entry / stale / moved-away / expired-without-touch.
    elif status == "expired" and entry_triggered is not True:
        group, reason = NO_ENTRY_EXPIRED, "validity window ended without an entry touch"
    elif status in _NO_ENTRY_STATUSES:
        group, reason = NO_ENTRY_EXPIRED, _NO_ENTRY_REASON.get(status, "no entry")

    # G. non-actionable (policy) and still non-terminal → review/shadow bucket.
    elif is_shadow and status in (_OPEN_ENTERED | _WAITING):
        group, reason = REVIEW_ONLY_SHADOW, "not actionable by policy (C-tier / scalp / shadow)"

    # H. open actionable (entered, running).
    elif entry_triggered is True and status in _OPEN_ENTERED:
        partial = status in {"tp1_hit", "tp2_hit"}
        group = OPEN_ACTIVE
        reason = "partial TP booked, runner open" if partial else "entry filled, monitoring TP/SL"

    # I. waiting actionable (not yet entered).
    elif status in _WAITING and entry_triggered is not True:
        group, reason = WAITING_FOR_ENTRY, "actionable candidate, entry not touched yet"

    else:
        group, reason = UNKNOWN_INCONSISTENT, f"unmapped status '{status or 'n/a'}'"

    # ---- labels + r policy -----------------------------------------------------
    label, r_policy = _label_and_r_policy(group, effective_r, mfe_r, r_source=r_source)

    return {
        "display_status": group.lower(),
        "display_group": group,
        "display_reason": reason,
        "display_r_source": r_source,
        "paper_outcome_authoritative": bool(paper_terminal),
        "operator_label": label,
        "entry_touched": entry_triggered if entry_triggered is not None else "unknown",
        "paper_entered": (bool(entry_triggered) and is_actionable is True)
        if (entry_triggered is not None and is_actionable is not None) else "unknown",
        "paper_alert_sent": paper_alert_sent if paper_alert_sent is not None else "unknown",
        "is_actionable": is_actionable if is_actionable is not None else "unknown",
        "is_shadow_or_review": bool(is_shadow),
        "is_active_for_operator": group == OPEN_ACTIVE,
        "is_waiting_for_entry": group == WAITING_FOR_ENTRY,
        "is_entered_unresolved": group == ENTERED_UNRESOLVED_EXPIRED,
        "is_no_entry_miss": group == NO_ENTRY_EXPIRED,
        "r_display_policy": r_policy,
        "should_show_in_active_monitor": group == OPEN_ACTIVE,
        "should_show_in_waiting_monitor": group == WAITING_FOR_ENTRY,
        "should_show_in_shadow_monitor": group == REVIEW_ONLY_SHADOW,
    }


def _label_and_r_policy(group: str, final_r: float | None, mfe_r: float | None, *,
                        r_source: str = "legacy touch") -> tuple[str, str]:
    if group == OPEN_ACTIVE:
        return "🟢 OPEN — entry filled, monitoring TP/SL", "unrealized"
    if group == WAITING_FOR_ENTRY:
        return "⏳ WAITING — entry not touched yet", "na_waiting"
    if group == REVIEW_ONLY_SHADOW:
        return "👁 REVIEW/SHADOW — not actionable by policy", "na_shadow"
    if group == ENTERED_UNRESOLVED_EXPIRED:
        return (
            "⌛ EXPIRED AFTER ENTRY — entered, no TP/SL within window (not a missed entry)",
            "unresolved_expiry",
        )
    if group == NO_ENTRY_EXPIRED:
        return "❌ NO ENTRY — price never reached the entry before the window ended", "na_no_entry"
    if group == CLOSED_WIN:
        # final_r is guaranteed > 0 (or None) here; `:+.1f` never yields "+-".
        r = f" {final_r:+.1f}R ({r_source})" if final_r is not None else ""
        return f"✅ CLOSED WIN{r}", "terminal"
    if group == CLOSED_LOSS:
        r = f" {final_r:+.1f}R ({r_source})" if final_r is not None else ""
        return f"🔴 CLOSED LOSS{r}", "terminal"
    if group == CLOSED_FLAT:
        return "⚪ CLOSED FLAT 0R", "terminal_flat"
    return "⚠️ STATUS NEEDS REVIEW — inconsistent lifecycle fields", "na_unknown"


def format_r_with_lifecycle(row: dict[str, Any]) -> str:
    """Lifecycle-aware R string — never shows a bare ``+0R`` that reads as profit/flat."""
    d = derive_display_status(row)
    policy = d["r_display_policy"]
    final_r = (_to_float(row.get("paper_execution_r")) if d.get("paper_outcome_authoritative")
               else _to_float(row.get("final_r")))
    r_source = d.get("display_r_source") or "legacy touch"
    if policy == "terminal":
        return f"{final_r:+.1f}R ({r_source})" if final_r is not None else "terminal (R n/a)"
    if policy == "terminal_flat":
        return "CLOSED FLAT 0R"
    if policy == "unresolved_expiry":
        return "0R display / no TP-SL before expiry (unresolved, not a flat trade)"
    if policy == "unrealized":
        return "unrealized (open)"
    if policy == "na_no_entry":
        return "N/A — no entry"
    if policy == "na_waiting":
        return "N/A — waiting for entry"
    if policy == "na_shadow":
        return "N/A — review/shadow"
    return "N/A"


# ---- aggregation + Telegram ---------------------------------------------------
def summarize_display_states(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Count rows by display group + the report-friendly split counts."""
    counts = {g: 0 for g in DISPLAY_GROUPS}
    derived: list[dict[str, Any]] = []
    for r in rows:
        d = derive_display_status(r)
        derived.append({**r, **d})
        counts[d["display_group"]] += 1
    return {
        "counts": counts,
        "open_actionable_count": counts[OPEN_ACTIVE],
        "waiting_for_entry_count": counts[WAITING_FOR_ENTRY],
        "review_shadow_count": counts[REVIEW_ONLY_SHADOW],
        "expired_after_entry_count": counts[ENTERED_UNRESOLVED_EXPIRED],
        "no_entry_expired_count": counts[NO_ENTRY_EXPIRED],
        "closed_win_count": counts[CLOSED_WIN],
        "closed_loss_count": counts[CLOSED_LOSS],
        "closed_flat_count": counts[CLOSED_FLAT],
        "unknown_inconsistent_count": counts[UNKNOWN_INCONSISTENT],
        "rows": derived,
    }


def _sym_line(r: dict[str, Any]) -> str:
    sym = r.get("symbol", "?")
    direction = r.get("direction", "")
    touched = r.get("entry_touched")
    alert = r.get("paper_alert_sent")
    tb = {True: "yes", False: "no"}.get(touched, "?")
    ab = {True: "yes", False: "no"}.get(alert, "?")
    rstr = format_r_with_lifecycle(r)
    return (f"• {sym} {direction} — {r['operator_label']}\n"
            f"    entry touched: {tb} · paper alerted: {ab} · R: {rstr}\n"
            f"    reason: {r['display_reason']}")


def format_paper_monitor_status(rows: list[dict[str, Any]], *, top_n: int = 5,
                                 compact: bool = False, show_legend: bool = True,
                                 detail_link: str = "full details in report / Control Plane") -> str:
    """Compact, honest Telegram monitor summary. Never says a bare 'no active trades'
    when waiting / review / entered-unresolved signals exist; never collapses
    'expired' into one count; never prints '+-'.

    compact=True drops the per-item lists and legend (header + key notes only).
    """
    s = summarize_display_states(rows)
    c = s["counts"]
    lines = ["📊 Paper Monitor Status"]
    lines.append(f"Open actionable: {s['open_actionable_count']}")
    lines.append(f"Waiting for entry: {s['waiting_for_entry_count']}")
    lines.append(f"Entered unresolved: {s['expired_after_entry_count']}")
    lines.append(f"Review/Shadow: {s['review_shadow_count']}")
    lines.append(f"No-entry/stale/moved-away: {s['no_entry_expired_count']}")
    lines.append(f"Closed today: {c[CLOSED_WIN]}W / {c[CLOSED_LOSS]}L / {c[CLOSED_FLAT]}flat")
    lines.append(f"Needs review: {s['unknown_inconsistent_count']}")

    if s["open_actionable_count"] == 0 and (
        s["waiting_for_entry_count"] or s["review_shadow_count"] or s["expired_after_entry_count"]
    ):
        lines.append(
            f"\nNo open actionable trades, but there are {s['waiting_for_entry_count']} "
            f"waiting and {s['review_shadow_count']} review/shadow setups "
            f"(and {s['expired_after_entry_count']} entered-unresolved)."
        )

    # Split expired explicitly — never one raw 'expired' count.
    if s["expired_after_entry_count"] or s["no_entry_expired_count"]:
        lines.append("\nExpired split:")
        lines.append(f"  Expired after entry (entered, no TP/SL): {s['expired_after_entry_count']}")
        lines.append(f"  No-entry / stale / moved-away: {s['no_entry_expired_count']}")

    if not compact and show_legend:
        lines.append("\nLegend:")
        lines.append("  • Entered unresolved = entry filled, no TP/SL before window (NOT a miss)")
        lines.append("  • No-entry = price never touched / stale / moved away")
        lines.append("  • Review/Shadow = not actionable by policy (C-tier / scalp)")

    # Top items per the most operator-relevant buckets (skipped in compact mode).
    if not compact and top_n > 0:
        derived = s["rows"]
        for title, grp in (("Open actionable", OPEN_ACTIVE),
                           ("Waiting", WAITING_FOR_ENTRY),
                           ("Entered unresolved (expired)", ENTERED_UNRESOLVED_EXPIRED)):
            bucket = [r for r in derived if r["display_group"] == grp][:top_n]
            if bucket:
                lines.append(f"\n{title}:")
                lines.extend(_sym_line(r) for r in bucket)

    lines.append(f"\n({detail_link})")
    return "\n".join(lines)
