"""Pending-signal revalidation pass.

Read-mostly: examines `waiting_for_entry` signals (after the candle walker
has finished) and decides whether they are stale, missed by the move, or
otherwise no longer actionable. **Never** mutates entry / stop / TP /
expires_at — only the lifecycle `status` and the appended `notes` field
on `signal_outcomes`.

See reports/PENDING_SIGNAL_REVALIDATION_SPEC.md and PART 6 mode-freshness
windows for the policy.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable

from src.config import ProjectConfig
from src.signals.config import SignalTrackingConfig
from src.signals.models import (
    STATUS_WAITING,
    SignalOutcome,
)
from src.signals.tracker import writer_lock
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore


# New statuses introduced by the revalidator. Defined locally rather than in
# models.STATUS_* so existing constant imports stay stable; downstream code
# treats unknown statuses as "open" until proven otherwise.
STATUS_STALE_BEFORE_ENTRY = "stale_before_entry"
STATUS_ENTRY_MOVED_AWAY = "entry_moved_away"
STATUS_REGIME_CHANGED = "regime_changed"
STATUS_NEEDS_REPRICE = "needs_reprice"
STATUS_MANUAL_REVIEW = "manual_review_required"

# Per-mode freshness horizons (hours since created_at after which a pending
# signal is considered stale). Swing must agree with the registered 7-day
# validity window in ``config/signal_tracking.yaml``; otherwise a legitimate
# medium-term setup was silently retired after only one day.
FRESHNESS_HORIZON_HOURS: dict[str, float] = {
    "scalp": 1.0,
    "intraday": 4.0,
    "swing": 168.0,
    "invest": 72.0,
}

# Per-mode "should have filled by now" horizon used for entry_moved_away
# detection — if signal is older than this AND favorable move > 2R was
# observed, we conclude the entry was missed by the move.
EXPECTED_FILL_HORIZON_HOURS: dict[str, float] = {
    "scalp": 0.5,
    "intraday": 2.0,
    "swing": 8.0,
    "invest": 24.0,
}


@dataclass
class RevalidationResult:
    checked: int = 0
    stale: int = 0
    moved_away: int = 0
    regime_changed: int = 0
    needs_reprice: int = 0
    manual_review: int = 0
    details: list[dict[str, Any]] = field(default_factory=list)


def _parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        cleaned = str(value).replace("Z", "+00:00")
        dt = datetime.fromisoformat(cleaned)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def _iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _favorable_excursion_r(
    signal: dict[str, Any], file_store: FileStore, project_config: ProjectConfig
) -> tuple[float, str | None]:
    """Return (max favorable price excursion in R, ts of that high/low).

    R is measured against (entry_anchor → invalidation). Uses cached OHLCV via
    the same lookup the tracker uses. Read-only.
    """
    from src.signals.tracker import (
        _load_ohlcv_for_signal,
        _load_stocks_ohlcv_for_signal,
        _filter_candles_after,
    )

    direction = str(signal.get("direction", ""))
    invalidation = signal.get("invalidation")
    entry_low = signal.get("entry_low")
    entry_high = signal.get("entry_high")
    if not invalidation or not entry_low or not entry_high:
        return 0.0, None
    asset_class = str(signal.get("asset_class") or "crypto").lower()
    mode = str(signal.get("mode", "intraday"))
    symbol = str(signal.get("symbol", ""))
    if asset_class == "stocks":
        frame, _, _ = _load_stocks_ohlcv_for_signal(file_store, symbol, mode)
    else:
        exchange_focus = str(signal.get("exchange_focus", ""))
        frame, _, _ = _load_ohlcv_for_signal(
            file_store, project_config, symbol, mode, exchange_focus
        )
    if frame is None or frame.empty:
        return 0.0, None
    candles = _filter_candles_after(frame, str(signal.get("created_at", "")))
    if candles.empty:
        return 0.0, None
    entry_anchor = (float(entry_low) + float(entry_high)) / 2
    risk_distance = abs(entry_anchor - float(invalidation))
    if risk_distance <= 0:
        return 0.0, None
    best_r = 0.0
    best_ts: str | None = None
    for _, row in candles.iterrows():
        high = float(row.get("high", row.get("close", 0)))
        low = float(row.get("low", row.get("close", 0)))
        if direction == "long":
            r_now = (high - entry_anchor) / risk_distance
        else:
            r_now = (entry_anchor - low) / risk_distance
        if r_now > best_r:
            best_r = r_now
            ts_val = row.get("timestamp")
            if ts_val is not None:
                try:
                    import pandas as pd
                    best_ts = pd.to_datetime(ts_val, utc=True).strftime(
                        "%Y-%m-%dT%H:%M:%S+00:00"
                    )
                except Exception:
                    best_ts = None
    return best_r, best_ts


def revalidate_signal(
    *,
    signal: dict[str, Any],
    file_store: FileStore,
    project_config: ProjectConfig,
    tracker_config: SignalTrackingConfig,
    now: datetime | None = None,
) -> tuple[SignalOutcome, str] | None:
    """Decide whether a single pending signal needs a non-default status.

    Returns (outcome, new_status) when a transition is decided; None when the
    signal is still cleanly waiting_for_entry.
    """

    now = now or _now()
    status_now = str(signal.get("status") or "")
    if status_now != STATUS_WAITING:
        return None  # only revalidate fresh-pending signals
    created = _parse_ts(signal.get("created_at"))
    if created is None:
        return None
    mode = str(signal.get("mode", "intraday"))
    age_start = created
    age_end = now
    if str(signal.get("asset_class") or "").lower() == "stocks" and mode == "intraday":
        try:
            from src.stocks.market_calendar import stock_intraday_target_session

            target_open, target_close = stock_intraday_target_session(created)
        except Exception:
            target_open = target_close = None
        if target_open is not None and target_close is not None:
            # A stock-intraday plan created after the close, premarket, on a
            # weekend, or holiday belongs to its target RTH session. Do not
            # burn the 4h freshness budget while the cash market cannot trade.
            if now < target_open:
                return None
            age_start = max(created, target_open)
            age_end = min(now, target_close)
            if age_end < age_start:
                return None
    age_hours = (age_end - age_start).total_seconds() / 3600.0

    # Rule R2 — entry_moved_away (favorable move > 2R without fill)
    expected_fill = EXPECTED_FILL_HORIZON_HOURS.get(mode, 2.0)
    if age_hours >= expected_fill:
        excursion, excursion_ts = _favorable_excursion_r(
            signal, file_store, project_config
        )
        if excursion >= 2.0:
            outcome = SignalOutcome(
                signal_id=str(signal["signal_id"]),
                checked_at=_iso(now),
                status=STATUS_ENTRY_MOVED_AWAY,
                entry_triggered=False,
                notes=(
                    f"revalidator: entry_moved_away; favorable_excursion_r={excursion:.2f}, "
                    f"age={age_hours:.1f}h, mode={mode}, peak_at={excursion_ts}"
                ),
            )
            return outcome, STATUS_ENTRY_MOVED_AWAY

    # Rule R1 — stale_before_entry (past freshness horizon)
    horizon = FRESHNESS_HORIZON_HOURS.get(mode, 4.0)
    if age_hours >= horizon:
        outcome = SignalOutcome(
            signal_id=str(signal["signal_id"]),
            checked_at=_iso(now),
            status=STATUS_STALE_BEFORE_ENTRY,
            entry_triggered=False,
            notes=(
                f"revalidator: stale_before_entry; age={age_hours:.1f}h, "
                f"freshness_horizon={horizon:.1f}h, mode={mode}"
            ),
        )
        return outcome, STATUS_STALE_BEFORE_ENTRY

    return None


def revalidate_pending_signals(
    *,
    store: SQLiteStore,
    file_store: FileStore,
    project_config: ProjectConfig,
    tracker_config: SignalTrackingConfig,
    signal_ids: Iterable[str] | None = None,
) -> RevalidationResult:
    """Walk all waiting_for_entry signals and emit revalidation transitions.

    HARD CONSTRAINTS (see PENDING_SIGNAL_REVALIDATION_SPEC.md §5):
      - Never modifies entry/stop/TP/expires_at on proposed_signals.
      - Never deletes rows.
      - Never sends Telegram.
      - Only writes one row to signal_outcomes per transition, and updates
        proposed_signals.status only when a transition occurred.
    """

    result = RevalidationResult()
    if not tracker_config.enabled:
        return result
    now = _now()

    # Strict mutex (matches track_pending_entries, 2026-07-09 fix): this pass writes
    # signal_outcomes/proposed_signals.status just like the full/pending tracker passes do,
    # so it must hold the SAME writer_lock for its entire write phase -- never write
    # unlocked. blocking=False: a revalidation pass is lightweight/occasional, so it yields
    # to an in-flight full pass rather than waiting (the next invocation catches up).
    #
    # 2026-07-13 review: load_active_signals() must run INSIDE the lock, not before it. A
    # pre-lock snapshot can go stale -- another writer (a fast pending tick, or the full pass
    # right before this one) could transition a signal out of waiting_for_entry in the gap
    # between an outer read and this lock acquisition, and update_signal_status() below is an
    # unconditional UPDATE with no compare-and-swap, so a stale snapshot would silently
    # clobber a real, newer status. Matches track_active_signals' own pattern (tracker.py) of
    # always re-reading fresh while already holding the lock.
    root = project_config.root
    with writer_lock(root, blocking=False) as got_lock:
        if not got_lock:
            return result
        rows = store.load_active_signals()
        if signal_ids is not None:
            wanted = {str(s) for s in signal_ids}
            rows = [r for r in rows if r.get("signal_id") in wanted]
        rows = [r for r in rows if str(r.get("status") or "") == STATUS_WAITING]
        for row in rows:
            result.checked += 1
            pair = revalidate_signal(
                signal=row,
                file_store=file_store,
                project_config=project_config,
                tracker_config=tracker_config,
                now=now,
            )
            if pair is None:
                continue
            outcome, new_status = pair
            store.add_signal_outcome(outcome.to_row())
            store.update_signal_status(
                row["signal_id"],
                status=new_status,
                updated_at=_iso(now),
            )
            if new_status == STATUS_STALE_BEFORE_ENTRY:
                result.stale += 1
            elif new_status == STATUS_ENTRY_MOVED_AWAY:
                result.moved_away += 1
            elif new_status == STATUS_REGIME_CHANGED:
                result.regime_changed += 1
            elif new_status == STATUS_NEEDS_REPRICE:
                result.needs_reprice += 1
            elif new_status == STATUS_MANUAL_REVIEW:
                result.manual_review += 1
            result.details.append(
                {
                    "signal_id": row["signal_id"],
                    "symbol": row.get("symbol"),
                    "previous_status": STATUS_WAITING,
                    "new_status": new_status,
                    "notes": outcome.notes,
                }
            )
    return result
