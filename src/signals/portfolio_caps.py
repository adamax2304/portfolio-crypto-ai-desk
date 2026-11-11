"""Stocks concentration-cap overlay (2026-06-16).

A PORTFOLIO-AWARE sizing/actionability overlay — NOT a scoring change. It reduces
correlated stacking in the stocks book by:

  Rule A (proxy collapse): within a trading day + direction, redundant proxies
    (QQQ/XLK, SPY/DIA/IWM, …) and duplicate signals on the same symbol keep only the
    single best candidate actionable; the rest become shadow_proxy_duplicate (0×).

  Rule B (sector exposure cap): per risk_bucket + direction, counting pre-existing open
    exposure + surviving batch candidates ranked best-first:
        1st → 1.0×, 2nd → 0.5×, 3rd+ → 0.0× (shadow_sector_cap).

It NEVER changes score / tier / TP / SL / raw R / generation, never deletes signals, and
applies ONLY to stocks intraday A/B. Everything else passes through unchanged. Effective
weight combines conservatively with the playbook weight: ``min(playbook, cap)``.
"""

from __future__ import annotations

from typing import Any, Iterable

from src.signals.sizing import size_decision
from src.stocks.risk_clusters import get_stock_proxy_group, get_stock_risk_bucket, normalize_symbol

_NON_TERMINAL = {"generated", "waiting_for_entry", "triggered", "tp1_hit", "tp2_hit"}
_RANK_WEIGHT = {1: 1.0, 2: 0.5}  # 3rd and beyond → 0.0


def _is_eligible(sig: dict[str, Any]) -> bool:
    """Only stocks intraday A/B participate in the cap."""
    return (
        str(sig.get("asset_class") or "").lower() == "stocks"
        and str(sig.get("mode") or "").lower() == "intraday"
        and str(sig.get("tier") or "").upper() in {"A", "B"}
    )


def _day(sig: dict[str, Any]) -> str:
    return str(sig.get("created_at") or "")[:10]


def _priority(sig: dict[str, Any]) -> tuple:
    """Best candidate first: A>B, higher score, catalyst-backed, higher data
    confidence, then earlier created_at as final tie-break."""
    tier_rank = {"A": 0, "B": 1}.get(str(sig.get("tier") or "").upper(), 2)
    score = -float(sig.get("score") or 0.0)
    catalyst = 0 if int(sig.get("news_supported") or 0) > 0 else 1
    dconf = {"high": 0, "medium": 1, "low": 2}.get(str(sig.get("data_confidence") or "").lower(), 3)
    created = str(sig.get("created_at") or "")
    return (tier_rank, score, catalyst, dconf, created)


def _collapse_key(sig: dict[str, Any]) -> tuple:
    """Proxy-collapse key. `*_proxy` groups collapse across symbols (redundant ETF
    baskets); everything else collapses only against the SAME symbol (duplicate
    signals), so two distinct names (AAPL vs MSFT) are never merged by Rule A —
    that is Rule B's job."""
    pg = get_stock_proxy_group(sig.get("symbol"))
    if "_proxy" in pg:
        return (pg,)
    return (pg, normalize_symbol(sig.get("symbol")))


def _base_weight(sig: dict[str, Any]) -> float:
    try:
        d = size_decision(sig)
        return float(d.weight) if d.weight is not None else 1.0
    except Exception:
        return 1.0


def apply_stock_concentration_caps(
    signals: Iterable[dict[str, Any]],
    existing_positions: Iterable[dict[str, Any]] | None = None,
    now: Any = None,
) -> list[dict[str, Any]]:
    """Return copies of ``signals`` with concentration_* fields added. Original
    score/tier/playbook/raw_r/entry/stop/TP/created_at are preserved untouched."""
    out: list[dict[str, Any]] = []
    eligible_idx: list[int] = []

    for i, sig in enumerate(signals):
        s = dict(sig)
        sym = s.get("symbol")
        is_stock = str(s.get("asset_class") or "").lower() == "stocks"
        s["risk_bucket"] = get_stock_risk_bucket(sym) if is_stock else "n/a"
        s["proxy_group"] = get_stock_proxy_group(sym) if is_stock else "n/a"
        base = _base_weight(s)
        # preserve a snapshot of the originals
        s.setdefault("original_score", s.get("score"))
        s.setdefault("original_tier", s.get("tier"))
        s.setdefault("original_playbook", (lambda d: d.playbook if d else None)(_safe_decision(s)))
        if "raw_r" in s or "final_r" in s:
            s.setdefault("original_raw_r", s.get("raw_r", s.get("final_r")))
        s["concentration_base_weight"] = base
        # default: pass-through (non-eligible keep playbook weight, no cap)
        s["concentration_rank"] = None
        s["concentration_effective_weight"] = base
        if not _is_eligible(s):
            s["concentration_status"] = "not_applicable"
            s["concentration_reason"] = "overlay applies to stocks intraday A/B only"
        else:
            eligible_idx.append(i)
            s["concentration_status"] = "actionable"
            s["concentration_reason"] = ""
        out.append(s)

    if not eligible_idx:
        return out

    # ---- Rule A: proxy-duplicate collapse (per day + direction + collapse_key) ----
    groups: dict[tuple, list[int]] = {}
    for i in eligible_idx:
        s = out[i]
        key = (_day(s), str(s.get("direction") or "").lower(), _collapse_key(s))
        groups.setdefault(key, []).append(i)

    survivors: list[int] = []
    for key, idxs in groups.items():
        idxs_sorted = sorted(idxs, key=lambda j: _priority(out[j]))
        keep = idxs_sorted[0]
        survivors.append(keep)
        for j in idxs_sorted[1:]:
            out[j]["concentration_status"] = "shadow_proxy_duplicate"
            out[j]["concentration_effective_weight"] = 0.0
            out[j]["concentration_rank"] = None
            out[j]["concentration_reason"] = (
                f"proxy duplicate: better candidate exists in same proxy group "
                f"({out[j]['proxy_group']})"
            )

    # ---- Rule B: per risk_bucket + direction exposure cap ----
    existing_counts: dict[tuple, int] = {}
    for pos in (existing_positions or []):
        if str(pos.get("asset_class") or "").lower() != "stocks":
            continue
        if str(pos.get("mode") or "").lower() != "intraday":
            continue
        if str(pos.get("tier") or "").upper() not in {"A", "B"}:
            continue
        if str(pos.get("status") or "").lower() not in _NON_TERMINAL:
            continue
        bucket = get_stock_risk_bucket(pos.get("symbol"))
        if bucket == "unknown":
            continue
        k = (bucket, str(pos.get("direction") or "").lower())
        existing_counts[k] = existing_counts.get(k, 0) + 1

    # rank survivors within each (bucket, direction), best first
    by_bucket: dict[tuple, list[int]] = {}
    for i in survivors:
        s = out[i]
        if s["risk_bucket"] == "unknown":
            s["concentration_status"] = "unknown_bucket_actionable"
            s["concentration_reason"] = "unknown risk bucket — not correlation-capped"
            continue
        k = (s["risk_bucket"], str(s.get("direction") or "").lower())
        by_bucket.setdefault(k, []).append(i)

    for k, idxs in by_bucket.items():
        start = existing_counts.get(k, 0)
        for n, i in enumerate(sorted(idxs, key=lambda j: _priority(out[j]))):
            rank = start + n + 1
            cap_w = _RANK_WEIGHT.get(rank, 0.0)
            s = out[i]
            base = s["concentration_base_weight"]
            eff = min(base, cap_w)
            s["concentration_rank"] = rank
            s["concentration_effective_weight"] = eff
            if rank >= 3 or cap_w == 0.0:
                s["concentration_status"] = "shadow_sector_cap"
                s["concentration_reason"] = (
                    f"{_ord(rank)} correlated exposure in {k[0]} {k[1]} bucket — shadow"
                )
            elif rank == 2:
                s["concentration_status"] = "half_size"
                s["concentration_reason"] = (
                    f"2nd exposure in {k[0]} {k[1]} bucket — 0.5x only"
                )
            else:
                s["concentration_status"] = "actionable"
                s["concentration_reason"] = f"1st exposure in {k[0]} {k[1]} bucket"
                if eff < cap_w:
                    s["concentration_reason"] += " (playbook override caps size)"

    return out


def concentration_for_live_signal(store: Any, signal: dict[str, Any]) -> dict[str, Any]:
    """Live, per-signal concentration decision for the paper-entry path.

    Queries currently-open stock-intraday A/B positions from the store and ranks THIS
    signal within its (risk_bucket, direction) + checks same-proxy-group duplicates.
    Returns the concentration_* fields for a single signal. Non-eligible signals get a
    pass-through ('not_applicable'). Never raises — fails open to actionable."""
    base = {
        "risk_bucket": "n/a", "proxy_group": "n/a",
        "concentration_rank": None, "concentration_base_weight": _base_weight(signal),
        "concentration_effective_weight": _base_weight(signal),
        "concentration_status": "not_applicable", "concentration_reason": "",
    }
    if not _is_eligible(signal):
        return base
    try:
        bucket = get_stock_risk_bucket(signal.get("symbol"))
        pgroup = get_stock_proxy_group(signal.get("symbol"))
        direction = str(signal.get("direction") or "").lower()
        sym = normalize_symbol(signal.get("symbol"))
        base["risk_bucket"] = bucket
        base["proxy_group"] = pgroup
        if bucket == "unknown":
            base["concentration_status"] = "unknown_bucket_actionable"
            base["concentration_reason"] = "unknown risk bucket — not correlation-capped"
            return base
        open_rows = [r for r in store.load_active_signals()
                     if str(r.get("asset_class") or "").lower() == "stocks"
                     and str(r.get("mode") or "").lower() == "intraday"
                     and str(r.get("tier") or "").upper() in {"A", "B"}
                     and str(r.get("status") or "").lower() in _NON_TERMINAL
                     and str(r.get("signal_id")) != str(signal.get("signal_id"))]
        # Rule A live: an already-open redundant proxy in same group+dir → duplicate
        if "_proxy" in pgroup:
            dup = any(get_stock_proxy_group(r.get("symbol")) == pgroup
                      and str(r.get("direction") or "").lower() == direction
                      for r in open_rows)
        else:  # singles: only the same symbol counts as a duplicate
            dup = any(normalize_symbol(r.get("symbol")) == sym
                      and str(r.get("direction") or "").lower() == direction
                      for r in open_rows)
        if dup:
            base["concentration_status"] = "shadow_proxy_duplicate"
            base["concentration_effective_weight"] = 0.0
            base["concentration_reason"] = f"proxy duplicate: open position in same group ({pgroup})"
            return base
        # Rule B live: rank by existing same-bucket+dir open exposure
        existing = sum(1 for r in open_rows
                       if get_stock_risk_bucket(r.get("symbol")) == bucket
                       and str(r.get("direction") or "").lower() == direction)
        rank = existing + 1
        cap_w = _RANK_WEIGHT.get(rank, 0.0)
        eff = min(base["concentration_base_weight"], cap_w)
        base["concentration_rank"] = rank
        base["concentration_effective_weight"] = eff
        if rank >= 3 or cap_w == 0.0:
            base["concentration_status"] = "shadow_sector_cap"
            base["concentration_reason"] = f"{_ord(rank)} correlated exposure in {bucket} {direction} bucket — shadow"
        elif rank == 2:
            base["concentration_status"] = "half_size"
            base["concentration_reason"] = f"2nd exposure in {bucket} {direction} bucket — 0.5x only"
        else:
            base["concentration_status"] = "actionable"
            base["concentration_reason"] = f"1st exposure in {bucket} {direction} bucket"
    except Exception:
        # fail open — never block an alert on the concentration overlay
        return base
    return base


def _safe_decision(sig):
    try:
        return size_decision(sig)
    except Exception:
        return None


def _ord(n: int) -> str:
    return {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")
