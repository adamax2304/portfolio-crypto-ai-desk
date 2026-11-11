"""Sector-cap SHADOW-ONLY / would-bind diagnostics (alert-only).

The live concentration path (`concentration_for_live_signal`) ranks a signal
only against *concurrently-open* peers, so it fired 0x live while the day-batch
view would bind 18/92 cluster-day groups (see STOCK_SECTOR_CAP_LIVE_PATH_WIRING_
AUDIT.md). This module runs the EXISTING, tested batch cap
(`apply_stock_concentration_caps`) over the day's eligible candidates and reports
what it WOULD do — without changing the cap value and without touching routing.

`diagnostic_only=True` on every result. Nothing here resizes or blocks a trade.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.signals.portfolio_caps import apply_stock_concentration_caps


def would_bind_from_batch(
    batch_signals: list[dict[str, Any]],
    signal_id: str,
) -> dict[str, Any]:
    """Run the day-batch cap over ``batch_signals`` and read off the would-be
    concentration decision for ``signal_id``. Pure (delegates to the tested
    batch function). Fails open to a neutral result."""
    try:
        capped = apply_stock_concentration_caps(batch_signals, existing_positions=[])
        row = next((r for r in capped if str(r.get("signal_id")) == str(signal_id)), None)
        if row is None:
            return _neutral()
        return {
            "would_bind_sector_cap": row.get("concentration_status"),
            "would_sector_rank": row.get("concentration_rank"),
            "would_sector_bucket": row.get("risk_bucket"),
            "would_sector_reason": row.get("concentration_reason"),
            "diagnostic_only": True,
        }
    except Exception:
        return _neutral()


def _neutral() -> dict[str, Any]:
    return {
        "would_bind_sector_cap": "not_applicable",
        "would_sector_rank": None,
        "would_sector_bucket": None,
        "would_sector_reason": "",
        "diagnostic_only": True,
    }


def _start_of_utc_day(now: datetime) -> str:
    return now.astimezone(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0).isoformat()


def would_bind_sector_cap(
    store: Any,
    signal: dict[str, Any],
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Store-driven wrapper for the paper-entry path. Gathers today's stocks-
    intraday A/B candidates (day-batch view) including this signal, runs the
    batch cap in shadow, and reports the would-bind status + the ACTUAL live
    concentration status for comparison. Fails open."""
    now = now or datetime.now(timezone.utc)
    base = _neutral()
    base["actual_concentration_status"] = signal.get("concentration_status")
    try:
        if str(signal.get("asset_class") or "").lower() != "stocks" or \
           str(signal.get("mode") or "").lower() != "intraday":
            return base
        day_rows = store.load_signals_for_period(
            since=_start_of_utc_day(now),
            asset_class="stocks",
            mode="intraday",
        )
        batch = [r for r in day_rows
                 if str(r.get("tier") or "").upper() in {"A", "B"}]
        # ensure the current signal participates even if not yet persisted
        if not any(str(r.get("signal_id")) == str(signal.get("signal_id")) for r in batch):
            batch.append(dict(signal))
        result = would_bind_from_batch(batch, signal.get("signal_id"))
        result["actual_concentration_status"] = signal.get("concentration_status")
        return result
    except Exception:
        return base
