"""Pending-symbol universe for the Option B coverage fix (2026-06-16).

Selects the distinct symbols of actionable pending/triggered A/B signals so the monitor
tick can refresh their OHLCV cache BEFORE running ``track_pending_entries`` — closing the
coverage gap where discovery alts (not in the watchlist) had stale candles and were
detected hours late.

Read-only over the store. No scoring / generation / scalp reactivation.
"""

from __future__ import annotations

from typing import Any

# proposed_signals.status values that are still "in play" (mirror tracker._NON_TERMINAL).
NON_TERMINAL = {"generated", "waiting_for_entry", "triggered", "tp1_hit", "tp2_hit"}


def _norm(symbol: str | None) -> str:
    return str(symbol or "").strip().upper()


def _created(r: dict[str, Any]) -> str:
    return str(r.get("created_at") or "")


def select_pending_tracking_symbols(
    store: Any,
    now: Any = None,
    asset_class: str = "crypto",
    tiers: tuple[str, ...] = ("A", "B"),
    include_scalp: bool = True,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """Distinct pending/triggered A/B symbols for `asset_class`, priority-ordered.

    Priority: actionable modes (intraday/swing/short) before scalp; within that, most
    recently created first — so a per-tick cap always keeps the freshest actionable
    candidates. Scalp is included by default (keeps shadow research tracking fresh) but is
    deprioritized and dropped first under a cap; it is NEVER pushed (routing handles that).
    C-tier, rejected, and terminal statuses are excluded. Returns metadata dicts (one per
    distinct normalized symbol). Never raises — returns [] on store error."""
    try:
        rows = store.load_active_signals()
    except Exception:
        return []
    ac = asset_class.lower()
    tset = {t.upper() for t in tiers}

    eligible: list[dict[str, Any]] = []
    for r in rows:
        if str(r.get("asset_class") or "").lower() != ac:
            continue
        if str(r.get("tier") or "").upper() not in tset:
            continue
        if str(r.get("status") or "").lower() not in NON_TERMINAL:
            continue
        mode = str(r.get("mode") or "").lower()
        if mode == "scalp" and not include_scalp:
            continue
        if not _norm(r.get("symbol")):
            continue
        eligible.append(r)

    # priority sort (two stable passes): most-recent first, then non-scalp before scalp
    eligible.sort(key=lambda r: _created(r), reverse=True)               # recent first
    eligible.sort(key=lambda r: 1 if str(r.get("mode") or "").lower() == "scalp" else 0)

    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for r in eligible:
        norm = _norm(r.get("symbol"))
        if norm in seen:
            continue
        seen.add(norm)
        out.append({
            "symbol": r.get("symbol"),
            "norm": norm,
            "mode": str(r.get("mode") or "").lower(),
            "tier": str(r.get("tier") or "").upper(),
            "status": str(r.get("status") or "").lower(),
            "created_at": r.get("created_at"),
        })
    if limit is not None and limit >= 0:
        out = out[:limit]
    return out


def pending_symbols(store: Any, **kw) -> list[str]:
    """Convenience: just the original-form symbol strings, priority-ordered."""
    return [d["symbol"] for d in select_pending_tracking_symbols(store, **kw)]
