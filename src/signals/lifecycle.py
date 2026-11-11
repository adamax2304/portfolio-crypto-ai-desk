"""Intraday lifecycle labels / revalidation flags (alert-only).

Labels filled intraday trades for age, overnight carry, RTH state, and
next-session revalidation. It NEVER force-closes, hard-expires, or resizes —
every output is a label/flag for the operator + Control Plane.

Prior evidence (INTRADAY_REVALIDATION_WOULD_EXPIRE_AUDIT.md): overnight carry was
net-positive, so the correct action is relabel + revalidate, not auto-flatten.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

# US cash-equity close ~20:00 UTC (16:00 ET, ignoring DST nuance — coarse on
# purpose; this only drives a "close approaching" label, never an action).
_RTH_CLOSE_HOUR_UTC = 20
_RTH_OPEN_HOUR_UTC = 13  # ~09:30 ET rounded down


def _parse_iso(ts: str | None) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    except Exception:
        return None


def compute_lifecycle_label(
    signal: dict[str, Any],
    *,
    now: datetime | None = None,
    entry_triggered_at: str | None = None,
    status: str | None = None,
    regime_at_entry: str | None = None,
    regime_now: str | None = None,
) -> dict[str, Any]:
    """Return lifecycle fields for a (possibly filled) signal. Pure + fail-open.

    held_hours measures time since entry (or since creation if not yet filled).
    Crypto intraday ages at 6h/12h/16h; stocks intraday is RTH-aware. Carryover
    across a UTC day → revalidation flag. No action is ever taken here.
    """
    now = now or datetime.now(timezone.utc)
    asset = str(signal.get("asset_class") or "crypto").lower()
    mode = str(signal.get("mode") or "").lower()
    status = (status or signal.get("status") or "").lower()
    created = _parse_iso(signal.get("created_at"))
    entry = _parse_iso(entry_triggered_at or signal.get("entry_triggered_at"))

    anchor = entry or created
    held_hours = None
    if anchor is not None:
        held_hours = round((now - anchor).total_seconds() / 3600.0, 2)

    terminal = status in {
        "stopped", "tp1_hit", "tp2_hit", "tp3_hit", "expired",
        "invalidated_before_entry", "missed_no_entry", "expired_no_entry",
        "cancelled_by_regime_change", "cancelled_by_news",
    }

    # carryover = created on an earlier UTC day, or held across a day boundary
    carryover = False
    if created is not None:
        carryover = created.astimezone(timezone.utc).date() < now.astimezone(timezone.utc).date()
    if anchor is not None and not carryover:
        carryover = anchor.astimezone(timezone.utc).date() < now.astimezone(timezone.utc).date()

    regime_changed = None
    if regime_at_entry and regime_now:
        regime_changed = str(regime_at_entry).lower() != str(regime_now).lower()

    out: dict[str, Any] = {
        "lifecycle_label": "n/a",
        "held_hours": held_hours,
        "next_day_revalidation_required": False,
        "carryover_warning": False,
        "rth_close_approaching": None,
        "rth_overnight_hold": None,
        "catalyst_stale": None,
        "regime_changed_since_entry": regime_changed,
        "diagnostic_only": True,
    }

    if mode != "intraday" or terminal:
        # Only filled/active intraday trades get a lifecycle label.
        out["lifecycle_label"] = "n/a" if mode != "intraday" else "closed"
        return out

    # catalyst staleness: only if we can derive it (news-supported + aged out
    # of the intraday validity window). Otherwise leave None (never fake).
    if int(signal.get("news_supported") or 0) > 0 and held_hours is not None:
        out["catalyst_stale"] = held_hours > 24

    if asset == "stocks":
        hour = now.astimezone(timezone.utc).hour
        in_rth = _RTH_OPEN_HOUR_UTC <= hour < _RTH_CLOSE_HOUR_UTC
        out["rth_close_approaching"] = (hour == _RTH_CLOSE_HOUR_UTC - 1)
        out["rth_overnight_hold"] = bool(carryover or not in_rth)
        if carryover:
            out["lifecycle_label"] = "intraday_carryover_requires_review"
            out["carryover_warning"] = True
            out["next_day_revalidation_required"] = True
        elif out["rth_overnight_hold"]:
            out["lifecycle_label"] = "intraday_carryover"
            out["carryover_warning"] = True
            out["next_day_revalidation_required"] = True
        elif out["rth_close_approaching"]:
            out["lifecycle_label"] = "aging_intraday"
        else:
            out["lifecycle_label"] = "fresh_intraday"
        return out

    # crypto intraday
    h = held_hours if held_hours is not None else 0.0
    if carryover or h >= 16:
        out["lifecycle_label"] = "intraday_carryover_requires_review" if (
            carryover or regime_changed) else "stale_intraday"
        out["carryover_warning"] = bool(carryover)
        out["next_day_revalidation_required"] = bool(carryover or h >= 16)
    elif h >= 12:
        out["lifecycle_label"] = "stale_intraday"
        out["next_day_revalidation_required"] = True
    elif h >= 6:
        out["lifecycle_label"] = "aging_intraday"
    else:
        out["lifecycle_label"] = "fresh_intraday"

    # an intraday trade still open past its 24h validity is an expire-at-0R
    # candidate (label only — the tracker decides actual expiry separately)
    if h >= 24:
        out["lifecycle_label"] = "expired_at_0R_candidate"
        out["next_day_revalidation_required"] = True

    return out
