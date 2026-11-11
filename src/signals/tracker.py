"""Outcome tracker for proposed signals.

Walks cached OHLCV after the signal's creation time and decides whether entry
triggered, whether stop/TP1/TP2/TP3 hit (and in what order), MFE/MAE in R, and
whether the signal expired without an outcome. Same-candle ambiguity (stop and
TP touched in the same OHLCV bar) is flagged honestly — without tick data we
can't know the order, so we mark such outcomes ambiguous and let the analytics
layer decide whether to include them in winrate calculations.

The tracker is PASSIVE: it never edits scoring, never modifies signal levels,
never changes config. It only writes rows into proposed_signals.status and
into signal_outcomes.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

from src.config import ProjectConfig
from src.signals.config import SignalTrackingConfig
from src.signals.models import (
    OPEN_STATUSES,
    OUTCOME_AMBIGUOUS,
    OUTCOME_EXPIRED,
    OUTCOME_LOSS,
    OUTCOME_NOT_TRIGGERED,
    OUTCOME_WIN,
    STATUS_AMBIGUOUS,
    STATUS_EXPIRED,
    STATUS_MISSED_NO_ENTRY,
    STATUS_STOPPED,
    STATUS_TP1,
    STATUS_TP2,
    STATUS_TP3,
    STATUS_TRIGGERED,
    STATUS_WAITING,
    SignalOutcome,
)
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore


# proposed_status values that mean the trade has GENUINELY closed (a real
# terminal transition). Used to gate the close-alert dispatch. Note: an
# entered-but-still-open trade has status STATUS_TRIGGERED while _classify
# returns OUTCOME_EXPIRED as a *placeholder* final_outcome (see _classify) —
# so the close hook must key on `status`, NOT on `final_outcome`, otherwise it
# fires a bogus close_expired in the same tick the trade enters. (2026-06-16
# Telegram simultaneous open+close fix.)
_TERMINAL_OUTCOME_STATUSES = frozenset(
    {STATUS_TP3, STATUS_STOPPED, STATUS_EXPIRED, STATUS_AMBIGUOUS}
)
_ENTERED_OPEN_STATUSES = frozenset({STATUS_TRIGGERED, STATUS_TP1, STATUS_TP2})


def should_alert_paper_entry(entry_triggered: bool, status: str) -> bool:
    """A paper-entry (open) alert is meaningful only while the trade is OPEN.

    `status == STATUS_TRIGGERED` is the unique "entered and still open" state.
    If a single evaluation already shows a terminal status, the trade round-
    tripped within one tick and the operator never had a live window — no entry
    alert. (2026-06-16 simultaneous open+close fix.)
    """
    return bool(entry_triggered) and status == STATUS_TRIGGERED


def should_alert_close(status: str, prev_status: str) -> bool:
    """A close alert fires only on a genuine terminal transition out of OPEN.

    Keyed on `status` (terminal) — NOT on `final_outcome`, which _classify sets
    to the OUTCOME_EXPIRED placeholder even for still-open trades. Requiring
    `prev_status == STATUS_TRIGGERED` guarantees the close pairs with a prior
    paper-entry: a same-tick enter+close round trip (prev_status pre-entry)
    pushes neither alert. (2026-06-16 simultaneous open+close fix.)
    """
    return status in _TERMINAL_OUTCOME_STATUSES and prev_status in _ENTERED_OPEN_STATUSES


# Preferred OHLCV timeframe per mode. We try the first that exists, then fall
# back to the next. Mode → ordered list of timeframe directory names.
TIMEFRAME_PREFERENCE: dict[str, tuple[str, ...]] = {
    "scalp": ("5m", "15m", "1h"),
    "intraday": ("15m", "1h", "4h"),
    "swing": ("1h", "4h", "1d"),
    "invest": ("4h", "1d"),
}

# Stocks cache layout differs from crypto: data/raw/stocks/{tf}/{SYMBOL}.csv,
# no per-exchange tree. Stocks have no 5m / 4h history under MVP yfinance.
STOCKS_TIMEFRAME_PREFERENCE: dict[str, tuple[str, ...]] = {
    "scalp": ("1m", "15m", "1h", "1d"),
    "intraday": ("1m", "15m", "1h", "1d"),
    "swing": ("1h", "1d"),
    "invest": ("1d", "1wk"),
}
STOCK_PAPER_PROFILE_MODULES: tuple[tuple[str, str], ...] = (
    ("src.execution.stocks_intraday_breakout_1bar_paper", "15m"),
    ("src.execution.stocks_intraday_pullback_paper", "15m"),
    ("src.execution.stocks_catalyst_rs_paper", "15m"),
    ("src.execution.stocks_swing_event_rs_pullback_paper", "1d"),
)


@dataclass
class TrackingResult:
    checked: int = 0
    updated: int = 0
    expired: int = 0
    stopped: int = 0
    tp_hits: int = 0
    not_triggered: int = 0
    ambiguous: int = 0
    skipped_no_ohlcv: int = 0
    skipped_writer_lock: int = 0
    skip_reason: str | None = None
    details: list[dict[str, Any]] = field(default_factory=list)


def _merge_tracking_result(target: TrackingResult, source: TrackingResult) -> None:
    """Merge one independently locked signal result into a full-pass result."""
    for name in (
        "checked", "updated", "expired", "stopped", "tp_hits", "not_triggered",
        "ambiguous", "skipped_no_ohlcv", "skipped_writer_lock",
    ):
        setattr(target, name, int(getattr(target, name)) + int(getattr(source, name)))
    target.details.extend(source.details)
    if source.skip_reason and not target.skip_reason:
        target.skip_reason = source.skip_reason


def _iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")


def _now() -> datetime:
    return datetime.now(timezone.utc)


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


def _load_ohlcv_for_signal(
    file_store: FileStore,
    config: ProjectConfig,
    symbol: str,
    mode: str,
    exchange_focus: str = "",
) -> tuple[pd.DataFrame | None, str, str]:
    """Try preferred timeframes for the given mode on the anchor (or focus)
    exchange. Returns (DataFrame, exchange, timeframe). Empty DataFrame ⇒ no
    data found.

    Crypto path only. Stocks signals use `_load_stocks_ohlcv_for_signal`.
    """

    exchange_candidates: list[str] = []
    if exchange_focus:
        exchange_candidates.append(exchange_focus.lower())
    anchor = (config.anchor_exchange or "binance").lower()
    if anchor not in exchange_candidates:
        exchange_candidates.append(anchor)
    for fallback in ("binance", "bybit", "mexc"):
        if fallback not in exchange_candidates:
            exchange_candidates.append(fallback)
    tf_pref = TIMEFRAME_PREFERENCE.get(mode, TIMEFRAME_PREFERENCE["intraday"])
    # Timeframe priority still wins, but a stale focus-exchange cache must not
    # mask a fresh copy of the same timeframe on an anchor/fallback venue.
    # This used to be a material latency source for MEXC/Bybit discoveries:
    # the pending monitor refreshed Binance while the tracker kept reading an
    # older focus-exchange CSV simply because it appeared first in this loop.
    selected_by_tf: list[tuple[int, str, pd.DataFrame, datetime | None, str]] = []
    for tf_rank, tf in enumerate(tf_pref):
        candidates: list[tuple[int, str, pd.DataFrame, datetime | None]] = []
        for rank, exchange in enumerate(exchange_candidates):
            frame = file_store.load_ohlcv(exchange, symbol, tf)
            if frame is not None and not frame.empty:
                last_ts = None
                try:
                    last_ts = pd.to_datetime(frame["timestamp"], utc=True).max().to_pydatetime()
                except Exception:
                    pass
                candidates.append((rank, exchange, frame, last_ts))
        if candidates:
            preferred = min(candidates, key=lambda item: item[0])
            dated = [item for item in candidates if item[3] is not None]
            if not dated or preferred[3] is None:
                selected_by_tf.append((tf_rank, preferred[1], preferred[2], preferred[3], tf))
                continue
            venue_freshest = max(dated, key=lambda item: item[3])
            tolerance = timedelta(seconds=max(_timeframe_seconds(tf), 60))
            chosen = preferred if venue_freshest[3] - preferred[3] <= tolerance else venue_freshest
            selected_by_tf.append((tf_rank, chosen[1], chosen[2], chosen[3], tf))
    if selected_by_tf:
        dated = [item for item in selected_by_tf if item[3] is not None]
        if not dated:
            chosen = min(selected_by_tf, key=lambda item: item[0])
            return chosen[2], chosen[1], chosen[4]
        global_latest = max(item[3] for item in dated)
        for item in sorted(selected_by_tf, key=lambda value: value[0]):
            if item[3] is None:
                continue
            allowed_lag = timedelta(seconds=max(_timeframe_seconds(item[4]) * 2, 300))
            if global_latest - item[3] <= allowed_lag:
                return item[2], item[1], item[4]
        chosen = max(dated, key=lambda item: item[3])
        return chosen[2], chosen[1], chosen[4]
    return None, "", ""


def _load_crypto_execution_ohlcv(
    file_store: FileStore,
    config: ProjectConfig,
    symbol: str,
    exchange_focus: str = "",
) -> tuple[pd.DataFrame | None, str]:
    """Load the freshest cached 1m crypto frame for a point-in-time entry check.

    This is deliberately separate from :func:`_load_ohlcv_for_signal`: the
    latter is the strategy's canonical structural timeframe (15m for
    intraday).  Replacing it with 1m would silently change the historical
    strategy/exit model.  The 1m frame answers one much narrower question:
    "is the planned entry executable *right now*?"
    """
    exchanges: list[str] = []
    for exchange in (
        str(exchange_focus or "").lower(),
        str(getattr(config, "anchor_exchange", "") or "").lower(),
        "binance", "bybit", "mexc",
    ):
        if exchange and exchange not in exchanges:
            exchanges.append(exchange)

    candidates: list[tuple[str, pd.DataFrame, datetime | None]] = []
    for exchange in exchanges:
        frame = file_store.load_ohlcv(exchange, symbol, "1m")
        if frame is None or frame.empty:
            continue
        last_ts = None
        try:
            last_ts = pd.to_datetime(frame["timestamp"], utc=True).max().to_pydatetime()
        except Exception:
            pass
        candidates.append((exchange, frame, last_ts))
    if not candidates:
        return None, ""
    dated = [item for item in candidates if item[2] is not None]
    chosen = max(dated, key=lambda item: item[2]) if dated else candidates[0]
    return chosen[1], chosen[0]


def _load_stocks_ohlcv_for_signal(
    file_store: FileStore,
    symbol: str,
    mode: str,
) -> tuple[pd.DataFrame | None, str, str]:
    """Stocks counterpart: reads data/raw/stocks/{tf}/{SYMBOL}.csv.

    The 'exchange' slot in the returned tuple is always 'stocks' — there is
    no per-venue tree on the stocks side (yfinance is the single source).
    """

    tf_pref = STOCKS_TIMEFRAME_PREFERENCE.get(
        mode, STOCKS_TIMEFRAME_PREFERENCE["intraday"]
    )
    candidates: list[tuple[int, str, pd.DataFrame, datetime | None]] = []
    for rank, tf in enumerate(tf_pref):
        frame = file_store.load_stocks_ohlcv(symbol, tf)
        if frame is not None and not frame.empty:
            last_ts = None
            try:
                last_ts = pd.to_datetime(frame["timestamp"], utc=True).max().to_pydatetime()
            except Exception:
                pass
            candidates.append((rank, tf, frame, last_ts))
    if candidates:
        dated = [item for item in candidates if item[3] is not None]
        if not dated:
            chosen = min(candidates, key=lambda item: item[0])
            return chosen[2], "stocks", chosen[1]
        global_latest = max(item[3] for item in dated)
        for item in sorted(candidates, key=lambda value: value[0]):
            if item[3] is None:
                continue
            allowed_lag = timedelta(seconds=max(_timeframe_seconds(item[1]) * 2, 120))
            if global_latest - item[3] <= allowed_lag:
                return item[2], "stocks", item[1]
        chosen = max(dated, key=lambda item: item[3])
        return chosen[2], "stocks", chosen[1]
    return None, "", ""


def _filter_candles_after(frame: pd.DataFrame, after_iso: str) -> pd.DataFrame:
    if "timestamp" not in frame.columns:
        return frame
    after_dt = _parse_ts(after_iso)
    if after_dt is None:
        return frame
    mask = frame["timestamp"] >= after_dt
    return frame.loc[mask].reset_index(drop=True)


def _candles_until(frame: pd.DataFrame, until_iso: str, limit: int = 120) -> list[dict[str, Any]]:
    if frame is None or frame.empty or "timestamp" not in frame.columns:
        return []
    until_dt = _parse_ts(until_iso)
    if until_dt is None:
        return []
    hist = frame.loc[frame["timestamp"] <= until_dt].tail(limit)
    out: list[dict[str, Any]] = []
    for _, row in hist.iterrows():
        out.append({
            "open": row.get("open"),
            "high": row.get("high"),
            "low": row.get("low"),
            "close": row.get("close"),
        })
    return out


def _promoted_entry_mode(signal: dict[str, Any], frame: pd.DataFrame) -> dict[str, Any] | None:
    """Return a promoted entry, a stock-policy rejection, or ``None``.

    A known, non-promoted *stocks intraday* mode must never silently fall back
    to the legacy pullback geometry. That would make a disabled taker/no-chase
    mode look like an authorised Paper entry. Other asset/mode combinations
    retain their established behaviour.
    """
    try:
        from src.execution.entry_mode_classifier import classify
        from src.execution.paper_entry_mode_policy import (
            disabled_shadow_reason,
            paper_promotion_reason,
        )

        mode = str(signal.get("mode") or "")
        asset_class = str(signal.get("asset_class") or "crypto")
        classified = classify(
            entry_low=_to_float(signal.get("entry_low")),
            entry_high=_to_float(signal.get("entry_high")),
            direction=str(signal.get("direction") or "long"),
            candles=_candles_until(frame, str(signal.get("created_at") or "")),
        )
        entry_mode = str(classified.get("entry_mode") or "").upper()
        is_stock_intraday = asset_class.lower() == "stocks" and mode.lower() == "intraday"
        if is_stock_intraday and int(classified.get("candles_used") or 0) <= 0:
            return {
                "blocked": True,
                "entry_mode": "UNCLASSIFIED",
                "reason": "stocks_intraday_entry_mode_unclassified_no_history",
            }
        reason = paper_promotion_reason(
            asset_class=asset_class, trade_mode=mode, entry_mode=entry_mode
        )
        if is_stock_intraday and not reason:
            disabled_reason = disabled_shadow_reason(
                asset_class=asset_class, trade_mode=mode, entry_mode=entry_mode
            )
            return {
                "blocked": True,
                "entry_mode": entry_mode or "UNCLASSIFIED",
                "reason": disabled_reason or "stocks_intraday_entry_mode_not_promoted_to_paper",
            }
        if not reason:
            return None
        if entry_mode == "BREAKOUT_CONTINUATION":
            trigger = _to_float(classified.get("suggested_entry")) or _to_float(signal.get("entry_trigger"))
            if trigger is None:
                return None
            return {
                "entry_mode": entry_mode,
                "reason": reason,
                "entry_low": None,
                "entry_high": None,
                "entry_trigger": trigger,
            }
        if entry_mode == "PULLBACK_LIMIT":
            return {
                "entry_mode": entry_mode,
                "reason": reason,
                "entry_low": _to_float(signal.get("entry_low")),
                "entry_high": _to_float(signal.get("entry_high")),
                "entry_trigger": _to_float(signal.get("entry_trigger")),
            }
    except Exception:
        if (str(signal.get("asset_class") or "crypto").lower() == "stocks"
                and str(signal.get("mode") or "").lower() == "intraday"):
            return {
                "blocked": True,
                "entry_mode": "UNCLASSIFIED",
                "reason": "stocks_intraday_entry_mode_classification_error",
            }
        return None
    return None


def _crypto_intraday_level_hold_plan(
    signal: dict[str, Any],
    frame: pd.DataFrame,
    candles: pd.DataFrame,
    *,
    now: datetime,
    timeframe: str,
) -> dict[str, Any]:
    """Resolve the opt-in Paper level-hold profile without using future bars.

    The profile is intentionally limited to still-pending crypto intraday
    pullbacks. Existing entered/closed trades retain their original lifecycle.
    """
    if (
        str(signal.get("asset_class") or "crypto").lower() != "crypto"
        or str(signal.get("mode") or "").lower() != "intraday"
        or str(signal.get("status") or STATUS_WAITING) not in {"generated", STATUS_WAITING, "pending", "not_triggered"}
    ):
        return {"applied": False}
    try:
        from src.execution.crypto_intraday_level_hold_paper import resolve_entry
        from src.execution.entry_mode_classifier import classify

        classified = classify(
            entry_low=_to_float(signal.get("entry_low")),
            entry_high=_to_float(signal.get("entry_high")),
            direction=str(signal.get("direction") or "long"),
            candles=_candles_until(frame, str(signal.get("created_at") or "")),
        )
        if int(classified.get("candles_used") or 0) <= 0:
            return {"applied": False}
        return resolve_entry(
            signal=signal,
            source_entry_mode=str(classified.get("entry_mode") or ""),
            candles=candles,
            now=now,
            timeframe_seconds=_timeframe_seconds(timeframe),
        )
    except Exception:
        # This is an optional Paper profile. Preserve the pre-existing tracker
        # behavior if its read-only confirmation helper is unavailable.
        return {"applied": False}


def _crypto_intraday_breakout_plan(signal: dict[str, Any], frame: pd.DataFrame) -> dict[str, Any]:
    """Attach the versioned Paper profile to a forward intraday breakout.

    This is deliberately provenance-only. Current 1m revalidation below still
    decides whether a real Paper entry exists; no historical candle touch is
    converted into an entry by this helper.
    """
    if (
        str(signal.get("asset_class") or "crypto").lower() != "crypto"
        or str(signal.get("mode") or "").lower() != "intraday"
        or str(signal.get("status") or STATUS_WAITING)
        not in {"generated", STATUS_WAITING, "pending", "not_triggered"}
    ):
        return {"applied": False}
    try:
        from src.execution.crypto_intraday_breakout_paper import resolve_profile
        from src.execution.entry_mode_classifier import classify

        classified = classify(
            entry_low=_to_float(signal.get("entry_low")),
            entry_high=_to_float(signal.get("entry_high")),
            direction=str(signal.get("direction") or "long"),
            candles=_candles_until(frame, str(signal.get("created_at") or "")),
        )
        if int(classified.get("candles_used") or 0) <= 0:
            return {"applied": False}
        return resolve_profile(
            signal=signal,
            source_entry_mode=str(classified.get("entry_mode") or ""),
        )
    except Exception:
        return {"applied": False}


def _crypto_intraday_pullback_plan(signal: dict[str, Any], frame: pd.DataFrame) -> dict[str, Any]:
    """Attach the versioned Paper profile to a forward intraday pullback.

    This is provenance-only. The current 1m revalidation below still decides
    whether a real Paper entry exists; this helper only gives the raw
    PULLBACK_LIMIT path a stable profile id for reports and live policy.
    """
    if (
        str(signal.get("asset_class") or "crypto").lower() != "crypto"
        or str(signal.get("mode") or "").lower() != "intraday"
        or str(signal.get("status") or STATUS_WAITING)
        not in {"generated", STATUS_WAITING, "pending", "not_triggered"}
    ):
        return {"applied": False}
    try:
        from src.execution.crypto_intraday_pullback_paper import resolve_profile
        from src.execution.entry_mode_classifier import classify

        classified = classify(
            entry_low=_to_float(signal.get("entry_low")),
            entry_high=_to_float(signal.get("entry_high")),
            direction=str(signal.get("direction") or "long"),
            candles=_candles_until(frame, str(signal.get("created_at") or "")),
        )
        if int(classified.get("candles_used") or 0) <= 0:
            return {"applied": False}
        return resolve_profile(
            signal=signal,
            source_entry_mode=str(classified.get("entry_mode") or ""),
        )
    except Exception:
        return {"applied": False}


def _crypto_swing_breakout_reclaim_plan(
    signal: dict[str, Any],
    frame: pd.DataFrame,
    candles: pd.DataFrame,
    *,
    now: datetime,
    timeframe: str,
) -> dict[str, Any]:
    """Resolve the Paper-only reclaim gate for swing breakouts.

    The source classifier still calls the original setup
    ``BREAKOUT_CONTINUATION``. This profile replaces that raw touch with a
    closed-bar reclaim/hold plus retest window, and it is intentionally not
    live-routable.
    """
    if (
        str(signal.get("asset_class") or "crypto").lower() != "crypto"
        or str(signal.get("mode") or "").lower() != "swing"
        or str(signal.get("status") or STATUS_WAITING)
        not in {"generated", STATUS_WAITING, "pending", "not_triggered", STATUS_TRIGGERED, STATUS_TP1, STATUS_TP2}
    ):
        return {"applied": False}
    try:
        from src.execution.crypto_swing_breakout_reclaim_paper import resolve_entry
        from src.execution.entry_mode_classifier import classify

        classified = classify(
            entry_low=_to_float(signal.get("entry_low")),
            entry_high=_to_float(signal.get("entry_high")),
            direction=str(signal.get("direction") or "long"),
            candles=_candles_until(frame, str(signal.get("created_at") or "")),
        )
        if int(classified.get("candles_used") or 0) <= 0:
            return {"applied": False}
        return resolve_entry(
            signal=signal,
            source_entry_mode=str(classified.get("entry_mode") or ""),
            candles=candles,
            now=now,
            timeframe_seconds=_timeframe_seconds(timeframe),
        )
    except Exception:
        return {"applied": False}


def _crypto_breakout_entry_mode_for_stop_profile(
    signal: dict[str, Any],
    frame: pd.DataFrame,
    *,
    intraday_breakout_plan: dict[str, Any],
    swing_breakout_reclaim_plan: dict[str, Any] | None = None,
    promoted_entry: dict[str, Any] | None,
    active_paper_entry: dict[str, Any] | None = None,
) -> str | None:
    if str(signal.get("asset_class") or "crypto").lower() != "crypto":
        return None
    for candidate in (
        intraday_breakout_plan.get("entry_mode"),
        (swing_breakout_reclaim_plan or {}).get("source_entry_mode"),
        (promoted_entry or {}).get("entry_mode"),
        (active_paper_entry or {}).get("paper_execution_entry_mode"),
        signal.get("paper_execution_entry_mode"),
        signal.get("paper_source_entry_mode"),
    ):
        value = str(candidate or "").strip().upper()
        if value:
            return value
    if str(signal.get("mode") or "").lower() != "swing":
        return None
    try:
        from src.execution.entry_mode_classifier import classify

        classified = classify(
            entry_low=_to_float(signal.get("entry_low")),
            entry_high=_to_float(signal.get("entry_high")),
            direction=str(signal.get("direction") or "long"),
            candles=_candles_until(frame, str(signal.get("created_at") or "")),
        )
        if int(classified.get("candles_used") or 0) <= 0:
            return None
        return str(classified.get("entry_mode") or "").strip().upper() or None
    except Exception:
        return None


def _crypto_swing_pullback_plan(
    signal: dict[str, Any],
    frame: pd.DataFrame,
    candles: pd.DataFrame,
    *,
    now: datetime,
    timeframe: str,
) -> dict[str, Any]:
    """Resolve versioned Paper-only crypto-swing pullback replacements.

    The source classifier may still label the production idea as
    ``PULLBACK_LIMIT``.  These profiles deliberately replace that blind touch
    with a confirmed retest/fib retest execution mode, without making it live
    eligible.
    """
    if (
        str(signal.get("asset_class") or "crypto").lower() != "crypto"
        or str(signal.get("mode") or "").lower() != "swing"
        or str(signal.get("status") or STATUS_WAITING)
        not in {"generated", STATUS_WAITING, "pending", "not_triggered", STATUS_TRIGGERED, STATUS_TP1, STATUS_TP2}
    ):
        return {"applied": False}
    try:
        from src.execution.crypto_swing_pullback_paper import resolve_entry
        from src.execution.entry_mode_classifier import classify

        classified = classify(
            entry_low=_to_float(signal.get("entry_low")),
            entry_high=_to_float(signal.get("entry_high")),
            direction=str(signal.get("direction") or "long"),
            candles=_candles_until(frame, str(signal.get("created_at") or "")),
        )
        if int(classified.get("candles_used") or 0) <= 0:
            return {"applied": False}
        return resolve_entry(
            signal=signal,
            source_entry_mode=str(classified.get("entry_mode") or ""),
            candles=candles,
            all_candles=frame,
            now=now,
            timeframe_seconds=_timeframe_seconds(timeframe),
        )
    except Exception:
        # Optional Paper profile. A resolver failure must not break legacy
        # tracking; diagnostics can still catch the missing profile via tests.
        return {"applied": False}


def _stocks_intraday_breakout_1bar_plan(
    signal: dict[str, Any], candles: pd.DataFrame, *, now: datetime, timeframe: str,
) -> dict[str, Any]:
    """Resolve the versioned Paper one-bar stock breakout profile, if tagged."""
    try:
        from src.execution.stocks_intraday_breakout_1bar_paper import resolve_entry
        return resolve_entry(
            signal=signal, candles=candles, now=now,
            timeframe_seconds=_timeframe_seconds(timeframe),
        )
    except Exception:
        return {"applied": False}


def _raw_signal_payload(signal: dict[str, Any]) -> dict[str, Any]:
    raw = signal.get("raw_idea_json") if isinstance(signal, dict) else None
    if isinstance(raw, dict):
        return dict(raw)
    try:
        parsed = json.loads(raw or "{}")
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def _stock_paper_profile_timeframe(signal: dict[str, Any]) -> str | None:
    """Return the explicit tracking timeframe for a tagged stock Paper profile."""
    for module_name, default_tf in STOCK_PAPER_PROFILE_MODULES:
        try:
            module = __import__(module_name, fromlist=["matches_signal"])
            if module.matches_signal(signal):
                return str(getattr(module, "TRACKER_TIMEFRAME", default_tf) or default_tf)
        except Exception:
            continue
    return None


def _stocks_intraday_profile_plan(
    signal: dict[str, Any], candles: pd.DataFrame, *, now: datetime, timeframe: str,
) -> dict[str, Any]:
    """Route an explicitly tagged stock Paper signal to exactly one resolver."""
    for module_name, _default_tf in STOCK_PAPER_PROFILE_MODULES:
        try:
            module = __import__(module_name, fromlist=["resolve_entry"])
            result = module.resolve_entry(
                signal=signal, candles=candles, now=now,
                timeframe_seconds=_timeframe_seconds(timeframe),
            )
            if result.get("applied"):
                return result
        except Exception:
            continue
    return {"applied": False}


def _effective_expiry(signal: dict[str, Any]) -> datetime | None:
    """Return the actual validity deadline, including the stock intraday EOD rule."""
    configured = _parse_ts(signal.get("expires_at"))
    if (str(signal.get("asset_class") or "crypto").lower() != "stocks"
            or str(signal.get("mode") or "").lower() != "intraday"):
        return configured
    created = _parse_ts(signal.get("created_at"))
    if created is None:
        return configured
    try:
        from src.stocks.market_calendar import stock_intraday_target_session_close
        session_close = stock_intraday_target_session_close(created)
    except Exception:
        session_close = None
    if session_close is None:
        return configured
    if configured is not None and configured < created:
        return session_close
    return min(configured, session_close) if configured is not None else session_close


@dataclass
class _LevelTouches:
    triggered: bool = False
    triggered_at: str | None = None
    entry_price: float | None = None
    stop_hit: bool = False
    stop_hit_at: str | None = None
    tp1_hit: bool = False
    tp1_hit_at: str | None = None
    tp2_hit: bool = False
    tp2_hit_at: str | None = None
    tp3_hit: bool = False
    tp3_hit_at: str | None = None
    ambiguous: bool = False
    ambiguous_note: str = ""
    mfe_pct: float = 0.0  # max favorable excursion as fraction of entry price
    mae_pct: float = 0.0  # max adverse (negative) excursion as fraction
    # 2026-06-09 audit additions — annotation-only, headline R unchanged.
    # See reports/PAPER_EXECUTION_MODEL_SPEC.md §6.
    pre_entry_invalidation: bool = False
    intrabar_entry_stop: bool = False
    intrabar_entry_tp: bool = False
    gap_slip_stop_pct_of_risk: float = 0.0   # how far past stop the wick went
    gap_slip_tp_pct_of_risk: float = 0.0     # how far past tp1 the wick went


@dataclass(frozen=True)
class _EntryObservation:
    observed_at: str | None
    executable_price: float | None
    time_basis: str
    currently_executable: bool
    reason: str
    bar_open_at: str | None
    bar_timeframe: str


def _timeframe_seconds(timeframe: str | None) -> int:
    raw = str(timeframe or "").strip().lower()
    try:
        if raw.endswith("m"):
            return int(raw[:-1]) * 60
        if raw.endswith("h"):
            return int(raw[:-1]) * 3600
        if raw.endswith("d"):
            return int(raw[:-1]) * 86400
    except (TypeError, ValueError):
        pass
    return 0


def _entry_observation(
    *,
    signal: dict[str, Any],
    promoted_entry: dict[str, Any] | None,
    touches: _LevelTouches,
    candles: pd.DataFrame,
    timeframe: str,
    now: datetime,
    asset_class: str,
) -> _EntryObservation:
    """Describe what was executable when this tracker invocation ran.

    ``touches.triggered_at`` is a bar-open timestamp and remains useful for
    historical path reconstruction. It is not a point-in-time fill timestamp.
    A fresh execution observation exists only when the latest available close
    is recent and still satisfies the entry geometry without chasing.
    """
    historical = _EntryObservation(
        observed_at=None,
        executable_price=None,
        time_basis="historical_bar_range",
        currently_executable=False,
        reason="entry was inferred from a candle range; current price not verified",
        bar_open_at=touches.triggered_at,
        bar_timeframe=timeframe,
    )
    if not touches.triggered or candles is None or candles.empty:
        return historical
    try:
        row = candles.iloc[-1]
        bar_open = pd.to_datetime(row.get("timestamp"), utc=True).to_pydatetime()
        price = float(row.get("close"))
    except Exception:
        return historical
    if price <= 0:
        return historical

    bar_sec = _timeframe_seconds(timeframe)
    if bar_sec <= 0:
        return historical
    bar_end = bar_open + timedelta(seconds=bar_sec)
    # Crypto REST OHLCV includes the currently-forming candle. yfinance is a
    # delayed fallback, so retain a bounded 20-minute observation window and
    # label it honestly; it is never considered live-grade by the live policy.
    is_stocks = str(asset_class or "").lower().startswith("stock")
    grace = timedelta(minutes=20 if is_stocks else 2)
    if now < bar_open - timedelta(minutes=1) or now > bar_end + grace:
        return _EntryObservation(
            None, None, "stale_historical_bar", False,
            f"latest {timeframe} bar is not current at decision time",
            touches.triggered_at, timeframe,
        )

    entry_low = (promoted_entry.get("entry_low") if promoted_entry
                 else _to_float(signal.get("entry_low")))
    entry_high = (promoted_entry.get("entry_high") if promoted_entry
                  else _to_float(signal.get("entry_high")))
    entry_trigger = (promoted_entry.get("entry_trigger") if promoted_entry
                     else _to_float(signal.get("entry_trigger")))
    invalidation = _to_float(signal.get("invalidation"))
    direction = str(signal.get("direction") or "").lower()
    if direction == "long" and invalidation is not None and price <= invalidation:
        return _EntryObservation(None, None, "current_price_invalidated", False,
                                 "current price is beyond invalidation",
                                 touches.triggered_at, timeframe)
    if direction == "short" and invalidation is not None and price >= invalidation:
        return _EntryObservation(None, None, "current_price_invalidated", False,
                                 "current price is beyond invalidation",
                                 touches.triggered_at, timeframe)

    executable = False
    reason = "current price no longer satisfies entry geometry"
    if entry_low is not None and entry_high is not None:
        lo, hi = sorted((float(entry_low), float(entry_high)))
        executable = lo <= price <= hi
        reason = "current price is inside the entry zone" if executable else reason
    elif entry_trigger is not None:
        trigger = float(entry_trigger)
        risk = abs(trigger - invalidation) if invalidation is not None else 0.0
        max_chase = max(risk * 0.25, abs(trigger) * 0.001)
        if direction == "long":
            executable = trigger <= price <= trigger + max_chase
        elif direction == "short":
            executable = trigger - max_chase <= price <= trigger
        reason = ("current price confirms trigger within 0.25R chase cap"
                  if executable else "trigger was crossed but current price exceeds chase cap")
    if not executable:
        return _EntryObservation(None, None, "historical_not_currently_executable", False,
                                 reason, touches.triggered_at, timeframe)

    if is_stocks:
        observed = min(now, bar_end)
        basis = "provider_delayed_current_bar"
    else:
        observed = now
        basis = "point_in_time_current_bar"
    return _EntryObservation(
        _iso(observed), price, basis, True, reason,
        touches.triggered_at, timeframe,
    )


def _current_crypto_intraday_entry(
    *,
    signal: dict[str, Any],
    promoted_entry: dict[str, Any] | None,
    file_store: FileStore,
    project_config: ProjectConfig,
    now: datetime,
) -> tuple[_LevelTouches | None, _EntryObservation | None, str]:
    """Return a fresh 1m Paper-entry observation for a pending crypto intraday setup.

    The structural signal remains a 15m strategy.  This function is only the
    live-grade execution probe used before a Paper entry is created.  It never
    authorizes a historical fill and it never turns an already-missed 15m touch
    into a later synthetic entry.
    """
    frame, exchange = _load_crypto_execution_ohlcv(
        file_store, project_config, str(signal.get("symbol") or ""),
        str(signal.get("exchange_focus") or ""),
    )
    if frame is None or frame.empty:
        return None, None, exchange
    try:
        latest_open = pd.to_datetime(frame.iloc[-1].get("timestamp"), utc=True)
        probe = _LevelTouches(triggered=True, triggered_at=_iso(latest_open.to_pydatetime()))
    except Exception:
        return None, None, exchange
    observation = _entry_observation(
        signal=signal,
        promoted_entry=promoted_entry,
        touches=probe,
        candles=frame,
        timeframe="1m",
        now=now,
        asset_class="crypto",
    )
    if not observation.currently_executable or observation.executable_price is None:
        return None, observation, exchange
    # The decision timestamp, not a candle-open timestamp, is the entry.  The
    # next tracker cycle will start PnL/exit evaluation after this timestamp.
    return (
        _LevelTouches(
            triggered=True,
            triggered_at=observation.observed_at,
            entry_price=observation.executable_price,
        ),
        observation,
        exchange,
    )


def _current_stock_breakout_entry(
    *,
    signal: dict[str, Any],
    promoted_entry: dict[str, Any] | None,
    confirmation_at: str | None,
    now: datetime,
) -> tuple[_LevelTouches | None, _EntryObservation, str]:
    """Revalidate a confirmed stock profile against a fresh, timestamped quote.

    The 15m close establishes structure only. A Paper entry remains valid only
    if the current quote is inside the same 0.25R no-chase window. This keeps
    the strict point-in-time contract rather than converting delayed candles
    into synthetic fills.
    """
    historical_anchor = confirmation_at or _iso(now)
    unavailable = _EntryObservation(
        None, None, "stock_quote_unavailable", False,
        "fresh stock quote was not available after breakout confirmation",
        historical_anchor, "quote",
    )
    try:
        from src.stocks.market_calendar import is_us_cash_session_open
        from src.stocks.realtime_provider import finnhub_quote

        if not is_us_cash_session_open(now):
            return None, _EntryObservation(
                None, None, "outside_rth", False,
                "stock breakout execution is restricted to regular US session",
                historical_anchor, "quote",
            ), "finnhub"
        quote = finnhub_quote(str(signal.get("symbol") or ""))
    except Exception as exc:  # noqa: BLE001 - quote failure is a safe no-entry
        return None, _EntryObservation(
            None, None, "stock_quote_error", False,
            f"stock quote revalidation failed: {type(exc).__name__}",
            historical_anchor, "quote",
        ), "finnhub"

    source = str(quote.get("source") or "finnhub")
    if not quote.get("ok"):
        return None, _EntryObservation(
            None, None, "stock_quote_unavailable", False,
            f"stock quote unavailable: {quote.get('reason') or 'unknown'}",
            historical_anchor, "quote",
        ), source
    price = _to_float(quote.get("price"))
    observed_at = _parse_ts(quote.get("observed_at"))
    if price is None or price <= 0 or observed_at is None:
        return None, unavailable, source
    quote_age_sec = abs((now - observed_at).total_seconds())
    if quote_age_sec > 120:
        return None, _EntryObservation(
            None, None, "stock_quote_stale", False,
            f"stock quote age {quote_age_sec:.0f}s exceeds 120s execution limit",
            historical_anchor, "quote",
        ), source

    trigger = _to_float((promoted_entry or {}).get("entry_trigger"))
    invalidation = _to_float(signal.get("invalidation"))
    direction = str(signal.get("direction") or "").lower()
    if trigger is None or invalidation is None or direction not in {"long", "short"}:
        return None, _EntryObservation(
            None, None, "stock_quote_invalid_geometry", False,
            "stock profile trigger or invalidation missing for quote revalidation",
            historical_anchor, "quote",
        ), source
    if (direction == "long" and price <= invalidation) or (direction == "short" and price >= invalidation):
        return None, _EntryObservation(
            None, None, "current_price_invalidated", False,
            "fresh quote is beyond stock profile invalidation",
            historical_anchor, "quote",
        ), source
    risk = abs(trigger - invalidation)
    chase_r = _to_float((promoted_entry or {}).get("max_chase_r"))
    if chase_r is None:
        chase_r = 0.25
    chase_r = min(0.50, max(0.0, chase_r))
    max_chase = max(risk * chase_r, abs(trigger) * 0.001)
    executable = (
        trigger <= price <= trigger + max_chase
        if direction == "long"
        else trigger - max_chase <= price <= trigger
    )
    if not executable:
        return None, _EntryObservation(
            None, None, "historical_not_currently_executable", False,
            f"fresh quote is outside the stock profile {chase_r:.2f}R no-chase window",
            historical_anchor, "quote",
        ), source
    observation = _EntryObservation(
        _iso(observed_at), price, "point_in_time_current_bar", True,
        "fresh stock quote confirms the closed 15m breakout within 0.25R chase cap",
        historical_anchor, "quote",
    )
    return (
        _LevelTouches(triggered=True, triggered_at=observation.observed_at, entry_price=price),
        observation,
        source,
    )


def _resolve_crypto_swing_touch(
    *,
    signal: dict[str, Any],
    promoted_entry: dict[str, Any] | None,
    touches: _LevelTouches,
    file_store: FileStore,
    project_config: ProjectConfig,
    now: datetime,
    execution_timeframe: str,
) -> tuple[str | None, str]:
    """Resolve a swing entry inside an active higher-timeframe candle.

    The swing simulator remains 1h/4h deterministic.  This helper is strictly
    telemetry provenance: if a cached 1m/5m bar can show the first zone touch,
    latency is measured from that bar instead of incorrectly from the opening
    timestamp of the 1h candle.  Missing lower-timeframe data is *unknown*, not
    an invented fast touch.
    """
    if (not touches.triggered or str(signal.get("asset_class") or "crypto").lower() != "crypto"
            or str(signal.get("mode") or "").lower() != "swing"
            or _timeframe_seconds(execution_timeframe) < 3600):
        return None, "not_applicable"

    entry_low = promoted_entry.get("entry_low") if promoted_entry else _to_float(signal.get("entry_low"))
    entry_high = promoted_entry.get("entry_high") if promoted_entry else _to_float(signal.get("entry_high"))
    entry_trigger = (promoted_entry.get("entry_trigger") if promoted_entry
                     else _to_float(signal.get("entry_trigger")))
    direction = str(signal.get("direction") or "").lower()
    if entry_low is None and entry_high is None and entry_trigger is None:
        return None, "missing_entry_geometry"
    lo, hi = sorted((float(entry_low), float(entry_high))) if entry_low is not None and entry_high is not None else (None, None)

    exchanges: list[str] = []
    for exchange in (str(signal.get("exchange_focus") or "").lower(),
                     str(project_config.anchor_exchange or "").lower(), "binance", "bybit", "mexc"):
        if exchange and exchange not in exchanges:
            exchanges.append(exchange)
    created = _parse_ts(str(signal.get("created_at") or ""))
    for tf in ("1m", "5m"):
        for exchange in exchanges:
            try:
                frame = file_store.load_ohlcv(exchange, str(signal.get("symbol") or ""), tf)
                if frame is None or frame.empty:
                    continue
                df = frame.copy()
                df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
                df = df[df["timestamp"] <= pd.Timestamp(now)]
                if created is not None:
                    df = df[df["timestamp"] >= pd.Timestamp(created)]
                for _, row in df.sort_values("timestamp").iterrows():
                    high = _to_float(row.get("high"))
                    low = _to_float(row.get("low"))
                    if high is None or low is None:
                        continue
                    hit = ((lo is not None and low <= hi and high >= lo) or
                           (entry_trigger is not None and direction == "long" and high >= float(entry_trigger)) or
                           (entry_trigger is not None and direction == "short" and low <= float(entry_trigger)))
                    if hit:
                        ts = pd.to_datetime(row["timestamp"], utc=True).to_pydatetime()
                        return _iso(ts), f"lower_tf_{tf}_first_touch"
            except Exception:
                continue
    return None, "higher_tf_touch_unresolved"


def _evaluate_signal_walk(
    *,
    direction: str,
    entry_low: float | None,
    entry_high: float | None,
    entry_trigger: float | None,
    invalidation: float | None,
    tp1: float | None,
    tp2: float | None,
    tp3: float | None,
    candles: pd.DataFrame,
    same_candle_conservative: bool,
    require_short_pullback_rejection: bool = False,
    confirmed_entry_at: str | None = None,
    confirmed_entry_price: float | None = None,
) -> _LevelTouches:
    """Iterate candles, detect trigger/stop/TPs in chronological order.

    ``confirmed_entry_*`` is used only for an already accepted point-in-time
    Paper entry.  In that case the walk starts from the recorded entry instead
    of re-discovering a historical touch from the original signal timestamp.
    """

    result = _LevelTouches(
        triggered=bool(confirmed_entry_at and confirmed_entry_price is not None),
        triggered_at=confirmed_entry_at,
        entry_price=confirmed_entry_price,
    )
    if invalidation is None or candles is None or candles.empty:
        return result
    if direction not in ("long", "short"):
        return result

    # Determine entry condition.
    has_zone = entry_low is not None and entry_high is not None
    has_trigger = entry_trigger is not None

    for _, row in candles.iterrows():
        ts_value = row.get("timestamp")
        if pd.isna(ts_value):
            continue
        ts_iso = pd.to_datetime(ts_value, utc=True).strftime("%Y-%m-%dT%H:%M:%S+00:00")
        high = float(row.get("high", row.get("close", 0)))
        low = float(row.get("low", row.get("close", 0)))
        close = float(row.get("close", 0))
        triggered_this_bar = False  # set to True below when entry fires on this bar

        if not result.triggered:
            triggered_now = False
            entry_used = None
            if has_zone:
                # Candle range overlaps entry zone.
                lo = min(entry_low, entry_high)
                hi = max(entry_low, entry_high)
                if low <= hi and high >= lo:
                    # A short pullback needs a real rejection, not merely a
                    # wick through the entry zone while the bounce continues.
                    open_price = float(row.get("open", close))
                    short_rejected = (
                        not require_short_pullback_rejection
                        or direction != "short"
                        or (high >= lo and close < lo and close <= open_price)
                    )
                    triggered_now = short_rejected
                    # Use midpoint of overlap as conservative estimate; if the
                    # candle's open is inside zone, prefer that.
                    if triggered_now and lo <= open_price <= hi:
                        entry_used = open_price
                    elif triggered_now:
                        # Touch price = closer edge.
                        entry_used = hi if direction == "long" and low <= hi else lo
                        if direction == "short":
                            entry_used = lo if high >= lo else hi
            elif has_trigger:
                trig = float(entry_trigger)
                if direction == "long" and high >= trig:
                    triggered_now = True
                    entry_used = trig
                elif direction == "short" and low <= trig:
                    triggered_now = True
                    entry_used = trig
            if not triggered_now:
                # Even before trigger, check invalidation — if it's hit before
                # entry, mark invalidated-before-entry and stop walking.
                # 2026-06-09 audit: use a separate flag so the raw row is not
                # paradoxical (was: stop_hit=1 with entry_triggered=0). Final
                # outcome classification still routes to missed_no_entry.
                if direction == "long" and low <= float(invalidation):
                    result.pre_entry_invalidation = True
                    result.stop_hit_at = ts_iso
                    return result
                if direction == "short" and high >= float(invalidation):
                    result.pre_entry_invalidation = True
                    result.stop_hit_at = ts_iso
                    return result
                continue
            result.triggered = True
            result.triggered_at = ts_iso
            result.entry_price = entry_used
            triggered_this_bar = True

        # We're in-position. Check stop and TPs on this candle.
        entry_anchor = float(result.entry_price or (entry_high if direction == "long" else entry_low) or close)
        # MFE/MAE updates
        if direction == "long":
            favorable = (high - entry_anchor) / entry_anchor
            adverse = (low - entry_anchor) / entry_anchor
        else:
            favorable = (entry_anchor - low) / entry_anchor
            adverse = (entry_anchor - high) / entry_anchor
        if favorable > result.mfe_pct:
            result.mfe_pct = favorable
        if adverse < result.mae_pct:
            result.mae_pct = adverse

        stop_touched = (
            (direction == "long" and low <= float(invalidation))
            or (direction == "short" and high >= float(invalidation))
        )

        def _tp_hit(level: float | None) -> bool:
            if level is None:
                return False
            if direction == "long":
                return high >= float(level)
            return low <= float(level)

        tp1_now = _tp_hit(tp1) and not result.tp1_hit
        tp2_now = _tp_hit(tp2) and not result.tp2_hit
        tp3_now = _tp_hit(tp3) and not result.tp3_hit

        # 2026-06-09 audit additions: intrabar entry+stop / entry+TP flags +
        # gap-slip annotations. Headline R unchanged; see PAPER_EXECUTION_MODEL_SPEC.md.
        risk_distance = abs(entry_anchor - float(invalidation)) if entry_anchor else 0.0
        if triggered_this_bar and stop_touched:
            result.intrabar_entry_stop = True
        if triggered_this_bar and (tp1_now or tp2_now or tp3_now):
            result.intrabar_entry_tp = True
        if stop_touched and risk_distance > 0:
            if direction == "long":
                slip = (float(invalidation) - low) / risk_distance
            else:
                slip = (high - float(invalidation)) / risk_distance
            if slip > result.gap_slip_stop_pct_of_risk:
                result.gap_slip_stop_pct_of_risk = slip
        if tp1_now and tp1 is not None and risk_distance > 0:
            if direction == "long":
                slip = (high - float(tp1)) / risk_distance
            else:
                slip = (float(tp1) - low) / risk_distance
            if slip > result.gap_slip_tp_pct_of_risk:
                result.gap_slip_tp_pct_of_risk = slip

        if stop_touched and (tp1_now or tp2_now or tp3_now):
            # Same-candle ambiguity. Conservative model: count stop and flag.
            result.ambiguous = True
            result.ambiguous_note = (
                "Stop and TP touched in same candle; tick-level order unknown."
            )
            if same_candle_conservative:
                if tp1_now:
                    result.tp1_hit = True
                    result.tp1_hit_at = ts_iso
                if tp2_now:
                    result.tp2_hit = True
                    result.tp2_hit_at = ts_iso
                if tp3_now:
                    result.tp3_hit = True
                    result.tp3_hit_at = ts_iso
                result.stop_hit = True
                result.stop_hit_at = ts_iso
                return result
            # Non-conservative path (not used by default): pick TP.
            if tp1_now:
                result.tp1_hit = True
                result.tp1_hit_at = ts_iso
            if tp2_now:
                result.tp2_hit = True
                result.tp2_hit_at = ts_iso
            if tp3_now:
                result.tp3_hit = True
                result.tp3_hit_at = ts_iso
            return result

        if tp1_now:
            result.tp1_hit = True
            result.tp1_hit_at = ts_iso
        if tp2_now:
            result.tp2_hit = True
            result.tp2_hit_at = ts_iso
        if tp3_now:
            result.tp3_hit = True
            result.tp3_hit_at = ts_iso

        if stop_touched:
            result.stop_hit = True
            result.stop_hit_at = ts_iso
            return result

        if result.tp3_hit:
            return result  # nothing left to track

    return result


def _classify(
    *,
    touches: _LevelTouches,
    expired: bool,
    r_stop: float,
    r_tp1: float,
    r_tp2: float,
    r_tp3: float,
) -> tuple[str, str, float]:
    """Return (proposed_status, final_outcome, final_r)."""

    if touches.ambiguous and (touches.tp1_hit or touches.tp2_hit or touches.tp3_hit) and touches.stop_hit:
        return STATUS_AMBIGUOUS, OUTCOME_AMBIGUOUS, r_stop  # conservative: -1R
    if not touches.triggered:
        if touches.stop_hit:
            # Invalidation hit before entry — treat as not_triggered with note.
            return STATUS_MISSED_NO_ENTRY, OUTCOME_NOT_TRIGGERED, 0.0
        if expired:
            return STATUS_MISSED_NO_ENTRY, OUTCOME_NOT_TRIGGERED, 0.0
        return STATUS_WAITING, OUTCOME_NOT_TRIGGERED, 0.0
    # Triggered.
    if touches.tp3_hit:
        return STATUS_TP3, OUTCOME_WIN, r_tp3
    if touches.stop_hit:
        # Preserve legacy touch R/outcome, but make the lifecycle truthful: a
        # post-TP1/TP2 stop is a terminal stop, not an indefinitely open TP state.
        if touches.tp2_hit:
            return STATUS_STOPPED, OUTCOME_WIN, r_tp2
        if touches.tp1_hit:
            return STATUS_STOPPED, OUTCOME_WIN, r_tp1
        return STATUS_STOPPED, OUTCOME_LOSS, r_stop
    if touches.tp2_hit:
        return STATUS_TP2, OUTCOME_WIN, r_tp2
    if touches.tp1_hit and not touches.stop_hit:
        return STATUS_TP1, OUTCOME_WIN, r_tp1
    if touches.tp1_hit and touches.stop_hit:
        # TP1 hit before stop in this walk order → win.
        return STATUS_TP1, OUTCOME_WIN, r_tp1
    if touches.stop_hit:
        return STATUS_STOPPED, OUTCOME_LOSS, r_stop
    if expired:
        return STATUS_EXPIRED, OUTCOME_EXPIRED, 0.0
    return STATUS_TRIGGERED, OUTCOME_EXPIRED, 0.0


def track_signal(
    *,
    signal: dict[str, Any],
    file_store: FileStore,
    project_config: ProjectConfig,
    tracker_config: SignalTrackingConfig,
    now: datetime | None = None,
    active_paper_entry: dict[str, Any] | None = None,
) -> tuple[SignalOutcome, str] | None:
    """Track a single signal. Returns (outcome, proposed_status) or None when
    no OHLCV is available."""

    now = now or _now()
    symbol = str(signal.get("symbol", ""))
    mode = str(signal.get("mode", "intraday"))
    exchange_focus = str(signal.get("exchange_focus", ""))
    direction = str(signal.get("direction", ""))
    asset_class = str(signal.get("asset_class") or "crypto").lower()
    original_signal = dict(signal)

    stock_profile_tf = _stock_paper_profile_timeframe(signal) if asset_class == "stocks" else None
    stock_profile = bool(stock_profile_tf)
    if asset_class == "stocks":
        # Versioned stock profiles own their timeframe. Intraday profiles use
        # closed 15m bars; the event/RS swing profile uses completed daily bars.
        frame, exch, tf = _load_stocks_ohlcv_for_signal(file_store, symbol, mode)
        if stock_profile_tf:
            loader = getattr(file_store, "load_stocks_ohlcv", None)
            forced = loader(symbol, stock_profile_tf) if callable(loader) else None
            if forced is not None and not forced.empty:
                frame, tf = forced, stock_profile_tf
    else:
        frame, exch, tf = _load_ohlcv_for_signal(
            file_store, project_config, symbol, mode, exchange_focus
        )
    if frame is None:
        return None

    created_at = str(signal.get("created_at", ""))
    promoted_entry = _promoted_entry_mode(signal, frame)
    # The versioned one-bar profile has its own deterministic promotion and
    # confirmation rule.  Its raw provenance is checked again by the resolver
    # below; an ordinary classifier rejection must not pre-empt that explicit
    # profile before it gets a chance to wait for its closed 15m bar.
    if stock_profile and promoted_entry and promoted_entry.get("blocked"):
        promoted_entry = None
    if promoted_entry and promoted_entry.get("blocked"):
        reason = str(promoted_entry.get("reason") or "stocks_intraday_entry_mode_not_promoted_to_paper")
        mode_label = str(promoted_entry.get("entry_mode") or "UNCLASSIFIED")
        outcome = SignalOutcome(
            signal_id=str(signal["signal_id"]),
            checked_at=_iso(now),
            status=STATUS_MISSED_NO_ENTRY,
            final_r=0.0,
            final_outcome=OUTCOME_NOT_TRIGGERED,
            notes=f"paper_entry_mode={mode_label}; paper_entry_policy={reason}; no paper entry",
        )
        return outcome, STATUS_MISSED_NO_ENTRY
    candles = _filter_candles_after(frame, created_at)
    if candles.empty and not (asset_class == "crypto" and mode.lower() == "intraday"):
        # No new candle since registration yet.
        outcome = SignalOutcome(
            signal_id=str(signal["signal_id"]),
            checked_at=_iso(now),
            status=str(signal.get("status", STATUS_WAITING)),
            notes=f"no candles since registration on {exch}/{tf}",
        )
        return outcome, str(signal.get("status", STATUS_WAITING))

    expires_at = _effective_expiry(signal)
    expired = bool(expires_at and now >= expires_at)
    if expires_at is not None:
        # Trim candles past expiry so outcome reflects what was possible within
        # the validity window.
        # OHLCV timestamps mark bar opens. A bar stamped exactly at the cash
        # close is outside the intraday session, so the expiry boundary is
        # strict rather than inclusive.
        candles = candles.loc[candles["timestamp"] < expires_at].reset_index(drop=True)

    level_hold_plan = _crypto_intraday_level_hold_plan(
        signal, frame, candles, now=now, timeframe=tf,
    )
    # V2 has a deliberately short retest window after the closed confirmation.
    # Apply it before both historical evaluation and the 1m point-in-time probe;
    # a signal cannot become executable again after that window has elapsed.
    profile_entry_expiry = _parse_ts(level_hold_plan.get("entry_expires_at"))
    if profile_entry_expiry is not None and (expires_at is None or profile_entry_expiry < expires_at):
        expires_at = profile_entry_expiry
        expired = now >= expires_at
        candles = candles.loc[candles["timestamp"] < expires_at].reset_index(drop=True)
    intraday_breakout_plan = _crypto_intraday_breakout_plan(signal, frame)
    intraday_pullback_plan = _crypto_intraday_pullback_plan(signal, frame)
    swing_breakout_reclaim_plan = _crypto_swing_breakout_reclaim_plan(
        signal, frame, candles, now=now, timeframe=tf,
    )
    swing_breakout_entry_expiry = _parse_ts(swing_breakout_reclaim_plan.get("entry_expires_at"))
    if swing_breakout_entry_expiry is not None and (expires_at is None or swing_breakout_entry_expiry < expires_at):
        expires_at = swing_breakout_entry_expiry
        expired = now >= expires_at
        candles = candles.loc[candles["timestamp"] < expires_at].reset_index(drop=True)
    swing_pullback_plan = _crypto_swing_pullback_plan(
        signal, frame, candles, now=now, timeframe=tf,
    )
    swing_profile_entry_expiry = _parse_ts(swing_pullback_plan.get("entry_expires_at"))
    if swing_profile_entry_expiry is not None and (expires_at is None or swing_profile_entry_expiry < expires_at):
        expires_at = swing_profile_entry_expiry
        expired = now >= expires_at
        candles = candles.loc[candles["timestamp"] < expires_at].reset_index(drop=True)
    # Profile resolvers need the complete originating RTH session to compute
    # causal session VWAP and relative volume. Each resolver still enforces
    # decision_at and closed-bar visibility, so pre-signal bars provide context
    # only and can never become an entry.
    stock_breakout_plan = _stocks_intraday_profile_plan(
        signal, frame, now=now, timeframe=tf,
    )
    crypto_breakout_stop_profile: dict[str, Any] = {"applied": False}
    crypto_breakout_entry_mode = _crypto_breakout_entry_mode_for_stop_profile(
        signal,
        frame,
        intraday_breakout_plan=intraday_breakout_plan,
        swing_breakout_reclaim_plan=swing_breakout_reclaim_plan,
        promoted_entry=promoted_entry,
        active_paper_entry=active_paper_entry,
    )
    if crypto_breakout_entry_mode == "BREAKOUT_CONTINUATION":
        try:
            from src.execution.crypto_breakout_stop_profile import (
                apply_wider_125_if_crypto_breakout,
            )

            signal, crypto_breakout_stop_profile = apply_wider_125_if_crypto_breakout(
                signal,
                entry_mode=crypto_breakout_entry_mode,
            )
        except Exception:
            crypto_breakout_stop_profile = {
                "applied": False,
                "reason": "crypto_breakout_stop_profile_error",
            }
    evaluation_candles = candles
    if level_hold_plan.get("applied"):
        promoted_entry = {
            "entry_mode": str(level_hold_plan.get("entry_mode") or "LEVEL_HOLD_V2"),
            "reason": str(level_hold_plan.get("reason") or "crypto_intraday_level_hold"),
            "entry_low": _to_float(signal.get("entry_low")),
            "entry_high": _to_float(signal.get("entry_high")),
            "entry_trigger": _to_float(signal.get("entry_trigger")),
        }
        if level_hold_plan.get("ready"):
            planned_candles = level_hold_plan.get("candles")
            if isinstance(planned_candles, pd.DataFrame) and profile_entry_expiry is not None:
                planned_candles = planned_candles.loc[
                    planned_candles["timestamp"] < profile_entry_expiry
                ].reset_index(drop=True)
            evaluation_candles = (planned_candles if isinstance(planned_candles, pd.DataFrame)
                                  else candles.iloc[:0].copy())
        else:
            # A confirmation has not closed yet (or failed). Do not credit the
            # original zone touch as an entry while the Paper profile waits.
            evaluation_candles = candles.iloc[:0].copy()


    if swing_breakout_reclaim_plan.get("applied"):
        promoted_entry = {
            "entry_mode": str(swing_breakout_reclaim_plan.get("entry_mode") or "BREAKOUT_RECLAIM_V2"),
            "reason": str(swing_breakout_reclaim_plan.get("reason") or "crypto_swing_breakout_reclaim_v2"),
            "entry_low": _to_float(swing_breakout_reclaim_plan.get("entry_low")),
            "entry_high": _to_float(swing_breakout_reclaim_plan.get("entry_high")),
            "entry_trigger": _to_float(swing_breakout_reclaim_plan.get("entry_trigger")),
        }
        if swing_breakout_reclaim_plan.get("ready"):
            planned_candles = swing_breakout_reclaim_plan.get("candles")
            if isinstance(planned_candles, pd.DataFrame) and swing_breakout_entry_expiry is not None:
                planned_candles = planned_candles.loc[
                    planned_candles["timestamp"] < swing_breakout_entry_expiry
                ].reset_index(drop=True)
            evaluation_candles = (planned_candles if isinstance(planned_candles, pd.DataFrame)
                                  else candles.iloc[:0].copy())
        else:
            evaluation_candles = candles.iloc[:0].copy()


    if swing_pullback_plan.get("applied"):
        if swing_pullback_plan.get("ready"):
            try:
                from src.execution.crypto_swing_pullback_paper import apply_signal_updates

                signal = apply_signal_updates(signal, swing_pullback_plan)
            except Exception:
                pass
            promoted_entry = {
                "entry_mode": str(swing_pullback_plan.get("entry_mode") or "PULLBACK_CONFIRMED_RETEST"),
                "reason": str(swing_pullback_plan.get("reason") or "crypto_swing_pullback_profile"),
                "entry_low": _to_float(signal.get("entry_low")),
                "entry_high": _to_float(signal.get("entry_high")),
                "entry_trigger": _to_float(signal.get("entry_trigger")),
            }
            planned_candles = swing_pullback_plan.get("candles")
            if isinstance(planned_candles, pd.DataFrame) and swing_profile_entry_expiry is not None:
                planned_candles = planned_candles.loc[
                    planned_candles["timestamp"] < swing_profile_entry_expiry
                ].reset_index(drop=True)
            evaluation_candles = (planned_candles if isinstance(planned_candles, pd.DataFrame)
                                  else candles.iloc[:0].copy())
        else:
            promoted_entry = {
                "entry_mode": str(swing_pullback_plan.get("entry_mode") or "PULLBACK_CONFIRMED_RETEST"),
                "reason": str(swing_pullback_plan.get("reason") or "crypto_swing_pullback_profile_pending"),
                "entry_low": _to_float(signal.get("entry_low")),
                "entry_high": _to_float(signal.get("entry_high")),
                "entry_trigger": _to_float(signal.get("entry_trigger")),
            }
            evaluation_candles = candles.iloc[:0].copy()


    if stock_breakout_plan.get("applied"):
        promoted_entry = {
            "entry_mode": str(stock_breakout_plan.get("entry_mode") or "BREAKOUT_CONTINUATION"),
            "reason": str(stock_breakout_plan.get("reason") or "stocks_intraday_profile"),
            "entry_low": _to_float(signal.get("entry_low")),
            "entry_high": _to_float(signal.get("entry_high")),
            "entry_trigger": (_to_float(stock_breakout_plan.get("entry_trigger"))
                              or _to_float(stock_breakout_plan.get("entry_price"))
                              or _to_float(signal.get("entry_trigger"))),
            "max_chase_r": _to_float(stock_breakout_plan.get("max_chase_r")),
            "paper_size_weight": _to_float(stock_breakout_plan.get("paper_size_weight")),
            "paper_size_reason": str(stock_breakout_plan.get("paper_size_reason") or ""),
        }
        planned_candles = stock_breakout_plan.get("candles")
        evaluation_candles = (planned_candles if stock_breakout_plan.get("ready") and isinstance(planned_candles, pd.DataFrame)
                              else candles.iloc[:0].copy())

    entry_low = (promoted_entry.get("entry_low") if promoted_entry
                 else _to_float(signal.get("entry_low")))
    entry_high = (promoted_entry.get("entry_high") if promoted_entry
                  else _to_float(signal.get("entry_high")))
    entry_trigger = (promoted_entry.get("entry_trigger") if promoted_entry
                     else _to_float(signal.get("entry_trigger")))
    walk_kwargs = dict(
        direction=direction, entry_low=entry_low, entry_high=entry_high,
        entry_trigger=entry_trigger, invalidation=_to_float(signal.get("invalidation")),
        tp1=_to_float(signal.get("tp1")), tp2=_to_float(signal.get("tp2")),
        tp3=_to_float(signal.get("tp3")),
        same_candle_conservative=(
            tracker_config.outcome_ambiguous_same_candle == "conservative"
        ),
        require_short_pullback_rejection=(
            asset_class == "stocks" and mode.lower() == "intraday"
            and direction.lower() == "short"
            and str((promoted_entry or {}).get("entry_mode") or "").upper() == "PULLBACK_LIMIT"
        ),
    )

    active_entry_at = str((active_paper_entry or {}).get("entry_at") or "") or None
    active_entry_price = _to_float((active_paper_entry or {}).get("entry_price_used"))
    paper_execution_source = ""
    if active_entry_at and active_entry_price is not None:
        # Once a Paper entry was accepted, never replay the signal from its
        # original creation time.  That would let a pre-entry historical stop
        # or TP close a trade before its actual entry.  Intraday exits are
        # therefore observed from the accepted entry on 1m candles.
        if asset_class == "crypto" and mode.lower() in {"intraday", "swing"}:
            execution_frame, execution_exchange = _load_crypto_execution_ohlcv(
                file_store, project_config, symbol, exchange_focus,
            )
        elif asset_class == "stocks" and mode.lower() == "intraday":
            # After a point-in-time stock entry, only 1m execution data after
            # that entry may resolve exits. Never replay the original setup.
            execution_frame = file_store.load_stocks_ohlcv(symbol, "1m")
            execution_exchange = "stocks"
        else:
            execution_frame, execution_exchange = None, ""
        if execution_frame is not None and not execution_frame.empty:
            entry_dt = _parse_ts(active_entry_at)
            execution_candles = execution_frame
            if entry_dt is not None:
                execution_candles = execution_candles.loc[
                    pd.to_datetime(execution_candles["timestamp"], utc=True) > pd.Timestamp(entry_dt)
                ].reset_index(drop=True)
            touches = _evaluate_signal_walk(
                candles=execution_candles, confirmed_entry_at=active_entry_at,
                confirmed_entry_price=active_entry_price, **walk_kwargs,
            )
            evaluation_candles, tf, exch = execution_candles, "1m", execution_exchange
            paper_execution_source = "accepted_point_in_time_entry"
        else:
            # No fresh execution frame: retain the honest open lifecycle.  Do
            # not fall back to the pre-entry historical 15m walk.
            touches = _LevelTouches(
                triggered=True, triggered_at=active_entry_at, entry_price=active_entry_price,
            )
            evaluation_candles = candles.iloc[:0].copy()
            paper_execution_source = "accepted_entry_waiting_for_fresh_1m"
        observation = _EntryObservation(
            active_entry_at, active_entry_price, "point_in_time_current_bar", True,
            "accepted Paper entry; exits evaluated only after its entry time",
            active_entry_at, "1m",
        )
    elif stock_breakout_plan.get("applied") and stock_breakout_plan.get("ready"):
        confirmed_at = str(stock_breakout_plan.get("confirmation_at") or "") or None
        stock_touches, stock_observation, quote_source = _current_stock_breakout_entry(
            signal=signal, promoted_entry=promoted_entry, confirmation_at=confirmed_at, now=now,
        )
        touches = stock_touches or _LevelTouches()
        observation = stock_observation
        evaluation_candles = candles.iloc[:0].copy()
        tf, exch = "quote", quote_source
        paper_execution_source = "stocks_profile_quote_revalidated"
    elif (level_hold_plan.get("applied")
          and str(level_hold_plan.get("entry_mode") or "").upper() == "LEVEL_HOLD_V2"
          and expired):
        # A V2 confirmation creates a 45-minute retest opportunity, not a
        # licence to reconstruct a fill later from historical 15m ranges.
        # This preserves the same point-in-time entry contract as the other
        # crypto intraday Paper profiles.
        touches = _LevelTouches()
        observation = _EntryObservation(
            None, None, "profile_retest_expired", False,
            "level-hold V2 retest window expired before a current-price entry",
            str(level_hold_plan.get("confirmation_at") or ""), tf,
        )
        evaluation_candles = candles.iloc[:0].copy()
        paper_execution_source = "level_hold_v2_retest_window_expired"
    else:
        # A crypto intraday setup may enter only on an observed current price.
        # Probe the 1m cache *before* walking 15m history.  A currently forming
        # 15m candle can contain a touch from earlier in the same bar; letting
        # that range win would again turn a real-time decision into an
        # indistinguishable historical fill.
        fresh_touches = fresh_observation = None
        execution_exchange = ""
        if (asset_class == "crypto" and mode.lower() == "intraday" and not expired
                and not (level_hold_plan.get("applied") and not level_hold_plan.get("ready"))):
            fresh_touches, fresh_observation, execution_exchange = _current_crypto_intraday_entry(
                signal=signal, promoted_entry=promoted_entry, file_store=file_store,
                project_config=project_config, now=now,
            )
        if fresh_touches is not None and fresh_observation is not None:
            touches, observation = fresh_touches, fresh_observation
            evaluation_candles, tf, exch = candles.iloc[:0].copy(), "1m", execution_exchange
            paper_execution_source = "fresh_1m_point_in_time_entry"
        elif (level_hold_plan.get("applied")
              and str(level_hold_plan.get("entry_mode") or "").upper() == "LEVEL_HOLD_V2"):
            # V2 may wait for the next scheduler tick if no current 1m quote
            # was available, but it must never fall back to a synthetic 15m
            # historical fill.  The next tick can still enter inside the
            # bounded retest window once a fresh quote arrives.
            touches = _LevelTouches()
            observation = fresh_observation or _EntryObservation(
                None, None, "fresh_quote_unavailable", False,
                "level-hold V2 awaits a current 1m execution price",
                str(level_hold_plan.get("confirmation_at") or ""), "1m",
            )
            evaluation_candles = candles.iloc[:0].copy()
            paper_execution_source = "level_hold_v2_awaiting_fresh_1m"
        else:
            touches = _evaluate_signal_walk(candles=evaluation_candles, **walk_kwargs)
            observation = _entry_observation(
                signal=signal, promoted_entry=promoted_entry, touches=touches,
                candles=evaluation_candles, timeframe=tf, now=now, asset_class=asset_class,
            )
    resolved_touch_at, touch_time_basis = _resolve_crypto_swing_touch(
        signal=signal, promoted_entry=promoted_entry, touches=touches,
        file_store=file_store, project_config=project_config, now=now,
        execution_timeframe=tf,
    )

    proposed_status, final_outcome, final_r = _classify(
        touches=touches,
        expired=expired,
        r_stop=tracker_config.stop_loss_r,
        r_tp1=tracker_config.tp1_r,
        r_tp2=tracker_config.tp2_r,
        r_tp3=tracker_config.tp3_r,
    )

    # Convert MFE/MAE pct to R using risk_per_unit / entry_anchor.
    risk = _to_float(signal.get("risk_per_unit"))
    entry_anchor = _to_float(signal.get("suggested_entry")) or _to_float(signal.get("entry_high")) or _to_float(signal.get("entry_low")) or 0.0
    mfe_r: float | None = None
    mae_r: float | None = None
    if risk and risk > 0 and entry_anchor:
        # mfe_pct is signed fraction relative to entry; (mfe_pct * entry) gives
        # price distance, divided by risk gives R.
        mfe_r = (touches.mfe_pct * entry_anchor) / risk
        mae_r = (touches.mae_pct * entry_anchor) / risk

    note_bits = [f"src={exch}/{tf}, candles={len(evaluation_candles)}"]
    if paper_execution_source:
        note_bits.append(f"paper_execution_source={paper_execution_source}")
    if touches.ambiguous:
        note_bits.append(touches.ambiguous_note)
    # 2026-06-09 audit annotations — additive only, no R-model impact.
    if touches.intrabar_entry_stop:
        note_bits.append("execution_ambiguous=intrabar_entry_stop")
    if touches.intrabar_entry_tp:
        note_bits.append("execution_ambiguous=intrabar_entry_tp")
    if touches.pre_entry_invalidation:
        note_bits.append("pre_entry_invalidation=1")
    if touches.gap_slip_stop_pct_of_risk >= 0.10:
        note_bits.append(f"gap_slip_stop_pct_of_risk={touches.gap_slip_stop_pct_of_risk*100:.0f}")
    if touches.gap_slip_tp_pct_of_risk >= 0.10:
        note_bits.append(f"gap_slip_tp_pct_of_risk={touches.gap_slip_tp_pct_of_risk*100:.0f}")
    if promoted_entry:
        note_bits.append(
            f"paper_entry_mode={promoted_entry['entry_mode']}"
            f"; paper_entry_policy={promoted_entry['reason']}"
        )
    if level_hold_plan.get("applied"):
        note_bits.append(f"paper_entry_profile={level_hold_plan.get('profile_id')}")
        if level_hold_plan.get("confirmation_at"):
            note_bits.append(f"level_hold_confirmation_at={level_hold_plan['confirmation_at']}")
        if level_hold_plan.get("entry_expires_at"):
            note_bits.append(f"level_hold_retest_expires_at={level_hold_plan['entry_expires_at']}")
        if level_hold_plan.get("profile_gate"):
            gate_bits = level_hold_plan["profile_gate"]
            note_bits.append(
                "level_hold_profile_gate="
                + ",".join(f"{key}={gate_bits[key]}" for key in sorted(gate_bits))
            )
    if intraday_breakout_plan.get("applied"):
        note_bits.append(f"paper_entry_profile={intraday_breakout_plan.get('profile_id')}")
        note_bits.append(f"intraday_breakout_profile={intraday_breakout_plan.get('reason')}")
    if intraday_pullback_plan.get("applied"):
        note_bits.append(f"paper_entry_profile={intraday_pullback_plan.get('profile_id')}")
        note_bits.append(f"intraday_pullback_profile={intraday_pullback_plan.get('reason')}")
    if crypto_breakout_stop_profile.get("applied"):
        note_bits.append(
            "initial_stop_profile="
            f"{crypto_breakout_stop_profile.get('profile_version')}"
            f"; widen_factor={crypto_breakout_stop_profile.get('widen_factor')}"
        )
    if swing_breakout_reclaim_plan.get("applied"):
        note_bits.append(f"paper_entry_profile={swing_breakout_reclaim_plan.get('profile_id')}")
        if swing_breakout_reclaim_plan.get("confirmation_at"):
            note_bits.append(f"swing_breakout_reclaim_confirmation_at={swing_breakout_reclaim_plan['confirmation_at']}")
        if swing_breakout_reclaim_plan.get("entry_expires_at"):
            note_bits.append(f"swing_breakout_reclaim_retest_expires_at={swing_breakout_reclaim_plan['entry_expires_at']}")
        if swing_breakout_reclaim_plan.get("profile_gate"):
            gate_bits = swing_breakout_reclaim_plan["profile_gate"]
            note_bits.append(
                "swing_breakout_reclaim_profile_gate="
                + ",".join(f"{key}={gate_bits[key]}" for key in sorted(gate_bits))
            )
    if swing_pullback_plan.get("applied"):
        note_bits.append(f"paper_entry_profile={swing_pullback_plan.get('profile_id')}")
        if swing_pullback_plan.get("confirmation_at"):
            note_bits.append(f"swing_pullback_confirmation_at={swing_pullback_plan['confirmation_at']}")
        if swing_pullback_plan.get("entry_expires_at"):
            note_bits.append(f"swing_pullback_retest_expires_at={swing_pullback_plan['entry_expires_at']}")
        if swing_pullback_plan.get("profile_gate"):
            gate_bits = swing_pullback_plan["profile_gate"]
            note_bits.append(
                "swing_pullback_profile_gate="
                + ",".join(f"{key}={gate_bits[key]}" for key in sorted(gate_bits))
            )
    if stock_breakout_plan.get("applied"):
        note_bits.append(f"paper_entry_profile={stock_breakout_plan.get('profile_id')}")
        if stock_breakout_plan.get("confirmation_at"):
            note_bits.append(f"stock_profile_confirmation_at={stock_breakout_plan['confirmation_at']}")
    if touches.triggered:
        note_bits.append(f"entry_time_basis={observation.time_basis}")
        note_bits.append(f"current_price_revalidated={int(observation.currently_executable)}")
        if touch_time_basis != "not_applicable":
            note_bits.append(f"entry_touch_time_basis={touch_time_basis}")
    if expired and proposed_status not in (STATUS_TP1, STATUS_TP2, STATUS_TP3, STATUS_STOPPED, STATUS_AMBIGUOUS):
        note_bits.append("expired within validity window")

    outcome = SignalOutcome(
        signal_id=str(signal["signal_id"]),
        checked_at=_iso(now),
        status=proposed_status,
        entry_triggered=touches.triggered,
        entry_triggered_at=touches.triggered_at,
        entry_price_used=touches.entry_price,
        stop_hit=touches.stop_hit,
        stop_hit_at=touches.stop_hit_at,
        tp1_hit=touches.tp1_hit,
        tp1_hit_at=touches.tp1_hit_at,
        tp2_hit=touches.tp2_hit,
        tp2_hit_at=touches.tp2_hit_at,
        tp3_hit=touches.tp3_hit,
        tp3_hit_at=touches.tp3_hit_at,
        max_favorable_excursion_pct=float(touches.mfe_pct) if touches.mfe_pct else 0.0,
        max_adverse_excursion_pct=float(touches.mae_pct) if touches.mae_pct else 0.0,
        max_favorable_excursion_r=mfe_r,
        max_adverse_excursion_r=mae_r,
        final_r=final_r,
        final_outcome=final_outcome,
        notes="; ".join(note_bits),
    )
    paper_live_exit_path = None
    if active_entry_at and active_entry_price is not None:
        try:
            from src.execution.paper_live_exit_path import (
                VERSION as LIVE_EXIT_PARITY_VERSION,
                simulate_live_exit_path,
            )

            frozen = json.loads(str((active_paper_entry or {}).get("signal_snapshot_json") or "{}"))
            if not isinstance(frozen, dict):
                frozen = {}
            # Only completed 1m candles are path evidence. The currently
            # forming candle cannot establish whether a moved stop preceded a
            # target touch.
            path_candles = evaluation_candles
            if isinstance(path_candles, pd.DataFrame) and not path_candles.empty:
                cutoff = pd.Timestamp(now - timedelta(minutes=1))
                path_candles = path_candles.loc[
                    pd.to_datetime(path_candles["timestamp"], utc=True) <= cutoff
                ].reset_index(drop=True)
            prior_path_state = None
            if str((active_paper_entry or {}).get("version") or "") == LIVE_EXIT_PARITY_VERSION:
                prior_path_state = active_paper_entry
            paper_live_exit_path = simulate_live_exit_path(
                direction=str(frozen.get("direction") or direction),
                entry=float(active_entry_price),
                stop=float(
                    _to_float(frozen.get("invalidation"))
                    or _to_float(frozen.get("stop_loss"))
                    or _to_float(signal.get("invalidation"))
                    or _to_float(signal.get("stop_loss"))
                ),
                tp1=_to_float(frozen.get("tp1")) or _to_float(signal.get("tp1")),
                tp2=_to_float(frozen.get("tp2")) or _to_float(signal.get("tp2")),
                tp3=_to_float(frozen.get("tp3")) or _to_float(signal.get("tp3")),
                candles=path_candles,
                initial_state=prior_path_state,
                path_start_at=active_entry_at,
            )
        except Exception:
            paper_live_exit_path = None
    raw_payload = _raw_signal_payload(signal)
    profile_weight = _to_float((promoted_entry or {}).get("paper_size_weight"))
    if profile_weight is None:
        profile_weight = _to_float(signal.get("paper_size_weight"))
    if profile_weight is None:
        profile_weight = _to_float(raw_payload.get("paper_size_weight"))
    # Point-in-time execution observability. These private attributes are not
    # written to legacy signal_outcomes; Paper accounting, alerts and latency
    # telemetry consume them only on the first entered transition. The legacy
    # candle-open timestamp remains untouched for historical compatibility.
    try:
        setattr(outcome, "_decision_at", observation.observed_at)
        setattr(outcome, "_first_executable_price", observation.executable_price)
        setattr(outcome, "_entry_time_basis", observation.time_basis)
        setattr(outcome, "_entry_currently_executable", observation.currently_executable)
        setattr(outcome, "_entry_revalidation_reason", observation.reason)
        setattr(outcome, "_entry_bar_open_at", observation.bar_open_at)
        setattr(outcome, "_entry_bar_timeframe", observation.bar_timeframe)
        setattr(outcome, "_entry_touch_at", resolved_touch_at)
        setattr(outcome, "_entry_touch_time_basis", touch_time_basis)
        setattr(
            outcome,
            "_strategy_ready_at",
            (observation.observed_at
             if touches.triggered and observation.currently_executable
             else resolved_touch_at if touches.triggered else None),
        )
        setattr(
            outcome,
            "_paper_entry_profile",
            level_hold_plan.get("profile_id")
            or intraday_breakout_plan.get("profile_id")
            or intraday_pullback_plan.get("profile_id")
            or swing_breakout_reclaim_plan.get("profile_id")
            or swing_pullback_plan.get("profile_id")
            or stock_breakout_plan.get("profile_id")
            or signal.get("paper_entry_profile")
            or raw_payload.get("paper_entry_profile"),
        )
        setattr(
            outcome,
            "_paper_execution_entry_mode",
            str(
                level_hold_plan.get("entry_mode")
                or intraday_breakout_plan.get("entry_mode")
                or intraday_pullback_plan.get("entry_mode")
                or swing_breakout_reclaim_plan.get("entry_mode")
                or swing_pullback_plan.get("entry_mode")
                or stock_breakout_plan.get("entry_mode")
                or crypto_breakout_entry_mode
                or (promoted_entry or {}).get("entry_mode")
                or signal.get("paper_execution_entry_mode")
                or raw_payload.get("paper_execution_entry_mode")
                or ""
            ).upper() or None,
        )
        setattr(
            outcome,
            "_paper_entry_profile_gate",
            level_hold_plan.get("profile_gate")
            or swing_breakout_reclaim_plan.get("profile_gate")
            or swing_pullback_plan.get("profile_gate")
            or stock_breakout_plan.get("profile_gate"),
        )
        setattr(outcome, "_paper_size_weight", profile_weight)
        setattr(outcome, "_paper_live_exit_path", paper_live_exit_path)
        setattr(outcome, "_paper_size_reason", str(
            (promoted_entry or {}).get("paper_size_reason")
            or signal.get("paper_size_reason")
            or raw_payload.get("paper_size_reason")
            or ""
        ))
        setattr(
            outcome,
            "_paper_source_entry_mode",
            str(
                intraday_breakout_plan.get("source_entry_mode")
                or intraday_pullback_plan.get("source_entry_mode")
                or swing_breakout_reclaim_plan.get("source_entry_mode")
                or swing_pullback_plan.get("source_entry_mode")
                or stock_breakout_plan.get("source_entry_mode")
                or crypto_breakout_entry_mode
                or signal.get("entry_mode")
                or signal.get("entry_mode_candidate")
                or ""
            ).upper() or None,
        )
        if crypto_breakout_stop_profile.get("applied"):
            from src.execution.crypto_breakout_stop_profile import signal_overrides
            setattr(outcome, "_execution_signal_overrides", signal_overrides(original_signal, signal))
        if swing_pullback_plan.get("applied") and swing_pullback_plan.get("ready"):
            from src.execution.crypto_swing_pullback_paper import signal_overrides
            setattr(outcome, "_execution_signal_overrides", signal_overrides(original_signal, signal))
    except Exception:
        pass
    return outcome, proposed_status


def _to_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _emit_latency_event(store, row, outcome, event_type: str, *, source: str = "track-signals",
                        once: bool = False, note: str | None = None) -> None:
    """Add-only latency telemetry hook. Records wall-clock latency from signal creation and from
    entry-touch at detection/alert time. FAIL-OPEN — never raises, never changes execution/scoring/
    alert routing. `once=True` writes at most one row per (signal_id, event_type, source) so a
    repeated tracker tick can't flood the table (transition events). See
    src/signals/latency_telemetry.py."""
    try:
        from datetime import datetime as _dt, timezone as _tz
        from src.signals import latency_telemetry as _tel

        def _p(ts):
            try:
                t = str(ts).strip().replace("Z", "+00:00")
                d = _dt.fromisoformat(t)
                return d if d.tzinfo else d.replace(tzinfo=_tz.utc)
            except Exception:
                return None

        now = _dt.now(_tz.utc)
        c0 = _p(row.get("created_at"))
        bar_open = _p(getattr(outcome, "entry_triggered_at", None))
        observed = _p(getattr(outcome, "_decision_at", None))
        resolved_touch = _p(getattr(outcome, "_entry_touch_at", None))
        strategy_ready = _p(getattr(outcome, "_strategy_ready_at", None))
        touch_basis = str(getattr(outcome, "_entry_touch_time_basis", "") or "")
        revalidated = bool(getattr(outcome, "_entry_currently_executable", False))
        # When current price is explicitly revalidated, the executable
        # opportunity is this observation, not an earlier visit to the same
        # swing entry zone. Keep the historical first touch in bar diagnostics,
        # but never turn it into several hours of fake system latency.
        effective_entry = (
            observed if revalidated and observed is not None else resolved_touch
        )
        lfs = round((now - c0).total_seconds(), 1) if c0 else None
        lft = round((now - effective_entry).total_seconds(), 1) if effective_entry else None
        lfb = round((now - bar_open).total_seconds(), 1) if bar_open else None
        lfr = round((now - strategy_ready).total_seconds(), 1) if strategy_ready else None
        outcome_note = str(getattr(outcome, "notes", None) or "")
        import re as _re
        tf_match = _re.search(r"src=[^,;]+/([^,;\s]+)", outcome_note)
        bar_tf = str(getattr(outcome, "_entry_bar_timeframe", "") or
                     (tf_match.group(1) if tf_match else ""))
        basis = str(getattr(outcome, "_entry_time_basis", "historical_bar_range"))
        tf_note = f"entry_bar_timeframe={bar_tf}" if bar_tf else None
        # Provenance has dedicated typed columns; keep `note` backward
        # compatible for consumers that expect a plain skip/failure reason.
        touch_note = f"entry_touch_time_basis={touch_basis}" if touch_basis else None
        latency_basis = (
            "system_latency_basis=current_revalidation" if revalidated and observed is not None
            else "system_latency_basis=first_observed_touch"
        )
        telemetry_note = "; ".join(x for x in (tf_note, touch_note, latency_basis, note) if x)
        runtime_match = _re.search(r"stage_runtime_ms=([0-9.]+)", str(note or ""))
        stage_runtime_ms = float(runtime_match.group(1)) if runtime_match else None
        fn = _tel.emit_once if once else _tel.emit
        fn(store, event_type=event_type, signal_id=row.get("signal_id"),
           symbol=row.get("symbol"), asset_class=(row.get("asset_class") or "crypto"),
           mode=row.get("mode"), source=source, latency_from_signal_sec=lfs,
           latency_from_entry_touch_sec=lft,
           latency_from_bar_open_sec=lfb,
           strategy_ready_at=(strategy_ready.isoformat() if strategy_ready else None),
           latency_from_strategy_ready_sec=lfr,
           entry_bar_open_at=(bar_open.isoformat() if bar_open else None),
           entry_time_basis=basis,
           current_price_revalidated=revalidated,
           stage_runtime_ms=stage_runtime_ms,
           market_data_timestamp=(effective_entry.isoformat() if effective_entry else None),
           note=(telemetry_note or None))
    except Exception:
        pass


def _active_point_in_time_paper_entry(store: SQLiteStore, signal_id: str) -> dict[str, Any] | None:
    """Return a still-open, actually observed Paper entry if one exists.

    `paper_execution_outcomes` already stores the durable point-in-time entry
    provenance.  Reading it here prevents a later tracker tick from replaying
    the original signal history before that accepted entry.  Legacy/backfill
    rows are intentionally excluded.
    """
    try:
        with store.connect() as conn:
            row = conn.execute(
                "SELECT entry_at, entry_price_used, paper_entry_profile, "
                "paper_execution_entry_mode,signal_snapshot_json,version,"
                "stop_current_r,highest_tp_touched,path_realized_r,"
                "path_remaining_fraction,path_last_candle_at,path_tp1_filled,"
                "path_tp2_filled,path_tp3_filled,path_max_mfe_r,path_data_quality "
                "FROM paper_execution_outcomes "
                "WHERE signal_id=? AND lifecycle_state='OPEN' "
                "AND entry_time_basis='point_in_time_current_bar' "
                "AND current_price_revalidated=1 "
                "AND entry_at IS NOT NULL AND entry_price_used IS NOT NULL "
                "LIMIT 1",
                (str(signal_id),),
            ).fetchone()
        return dict(row) if row is not None else None
    except Exception:
        return None


def track_active_signals(
    *,
    store: SQLiteStore,
    file_store: FileStore,
    project_config: ProjectConfig,
    tracker_config: SignalTrackingConfig,
    mode: str | None = None,
    signal_ids: Iterable[str] | None = None,
    paper_entry_notifier: Any = None,
    paper_entry_dry_run: bool = False,
    telemetry_source: str = "track-signals",
    coordinate_signal_writes: bool = False,
    signal_lock_blocking: bool = True,
    _preloaded_rows: list[dict[str, Any]] | None = None,
    _tracking_now: datetime | None = None,
) -> TrackingResult:
    """Update outcomes for all active signals (or a filtered subset).

    paper_entry_notifier: optional TelegramNotifier-like object with .send(text, parse_mode=).
        When provided AND a signal transitions from a pending status to an
        entered state, a one-shot paper-entry alert is dispatched and recorded
        in signal_alerts. None disables alerting (legacy behavior).
    telemetry_source: the `source` recorded on the add-only latency-telemetry events
        (entry_condition_detected / paper_entry_alert_*). Defaults to "track-signals"; the fast
        pending-monitor passes "pending-monitor" so SLA can attribute fast-path latency correctly.
        Attribution only — it does NOT change status/alert/outcome logic.
    """

    result = TrackingResult()
    if not tracker_config.enabled:
        return result

    rows = list(_preloaded_rows) if _preloaded_rows is not None else store.load_active_signals()
    if signal_ids is not None:
        wanted = {str(s) for s in signal_ids}
        rows = [r for r in rows if r.get("signal_id") in wanted]
    if mode:
        rows = [r for r in rows if r.get("mode") == mode]

    now = _tracking_now or _now()
    if coordinate_signal_writes:
        # The full sweep and the latency-critical monitor may run concurrently,
        # but they must never mutate the same signal together. Per-signal
        # locking preserves that guarantee without blocking unrelated entries.
        for row in rows:
            signal_id = str(row.get("signal_id") or "")
            if not signal_id:
                continue
            with signal_writer_lock(
                project_config.root,
                signal_id,
                blocking=signal_lock_blocking,
            ) as got_signal_lock:
                if not got_signal_lock:
                    result.skipped_writer_lock += 1
                    continue
                one = track_active_signals(
                    store=store,
                    file_store=file_store,
                    project_config=project_config,
                    tracker_config=tracker_config,
                    paper_entry_notifier=paper_entry_notifier,
                    paper_entry_dry_run=paper_entry_dry_run,
                    telemetry_source=telemetry_source,
                    coordinate_signal_writes=False,
                    _preloaded_rows=[row],
                    _tracking_now=now,
                )
                _merge_tracking_result(result, one)
        if result.skipped_writer_lock and result.checked == 0:
            result.skip_reason = "signal_writer_lock_contended"
        return result

    for row in rows:
        result.checked += 1
        active_paper_entry = _active_point_in_time_paper_entry(store, str(row.get("signal_id") or ""))
        track_kwargs = dict(
            signal=row, file_store=file_store, project_config=project_config,
            tracker_config=tracker_config, now=now,
        )
        # Keep the public call shape backward-compatible for lightweight test
        # doubles and external integrations.  The extra state is relevant only
        # for a real, accepted Paper entry.
        if active_paper_entry is not None:
            track_kwargs["active_paper_entry"] = active_paper_entry
        outcome_pair = track_signal(**track_kwargs)
        if outcome_pair is None:
            result.skipped_no_ohlcv += 1
            continue
        outcome, status = outcome_pair
        execution_row = row
        execution_overrides = getattr(outcome, "_execution_signal_overrides", None)
        if isinstance(execution_overrides, dict) and execution_overrides:
            execution_row = dict(row)
            execution_row.update(execution_overrides)
        if getattr(outcome, "_strategy_ready_at", None):
            _emit_latency_event(store, row, outcome, "strategy_entry_ready", once=True,
                                source=telemetry_source)
        outcome_row = outcome.to_row()
        save_outcome = getattr(store, "add_signal_outcome_if_changed", None)
        if callable(save_outcome):
            save_outcome(outcome_row)
        else:
            # Preserve compatibility with external/test stores that implement
            # only the original append API.
            store.add_signal_outcome(outcome_row)
        prev_status = str(row.get("status") or "")
        is_entry_transition = (
            prev_status in ("generated", STATUS_WAITING)
            and bool(outcome.entry_triggered)
        )
        if is_entry_transition:
            # Record detection even when a bar contains an immediate stop/TP
            # and therefore cannot produce a Paper-entry alert. Previously
            # those late observations disappeared from the alert-only metric.
            _emit_latency_event(store, row, outcome, "entry_condition_detected", once=True,
                                source=telemetry_source)
            try:
                touch = _parse_ts(getattr(outcome, "entry_triggered_at", None))
                if touch is not None and (now - touch).total_seconds() > 120:
                    _emit_latency_event(
                        store, row, outcome, "entry_observed_late", once=True,
                        source=telemetry_source,
                        note="observation_delay_over_120s",
                    )
            except Exception:
                pass
        # Paper execution accounting (Model F) — PAPER/ACCOUNTING ONLY, fail-open.
        # Computes the honest paper_execution_r beside the legacy touch-based
        # final_r and upserts it into the additive paper_execution_outcomes
        # table. NEVER touches signal_outcomes / final_r, never places orders.
        try:
            from src.execution.paper_execution_accounting import record_paper_execution
            record_paper_execution(
                store, signal=execution_row, outcome_row=outcome.to_row(), now_iso=_iso(now),
                decision_at=(getattr(outcome, "_decision_at", None) if is_entry_transition else None),
                first_executable_price=(getattr(outcome, "_first_executable_price", None)
                                        if is_entry_transition else None),
                entry_time_basis=(getattr(outcome, "_entry_time_basis", None)
                                  if is_entry_transition else None),
                current_price_revalidated=(
                    getattr(outcome, "_entry_currently_executable", None)
                    if is_entry_transition else None),
                paper_entry_profile=getattr(outcome, "_paper_entry_profile", None),
                paper_execution_entry_mode=getattr(
                    outcome, "_paper_execution_entry_mode", None),
                paper_entry_profile_gate=getattr(outcome, "_paper_entry_profile_gate", None),
                execution_path=getattr(outcome, "_paper_live_exit_path", None),
            )
        except Exception:
            # Accounting must never block legacy tracking.
            pass
        if is_entry_transition:
            # Freeze the latency/coverage facts while the same tracker tick still
            # has the entry-time candle frame. This is diagnostic-only and cannot
            # change lifecycle, scoring, routing, paper execution, or live.
            try:
                from src.signals.entry_latency_audit import capture_entry_snapshot
                capture_entry_snapshot(signal=row, outcome_row=outcome, file_store=file_store,
                                       project_config=project_config, db=str(store.db_path))
            except Exception:
                pass
        # Paper-entry Telegram alert hook. Fires once per signal on real
        # waiting→triggered transition; gated by tier/playbook/asset; dedup
        # via signal_alerts.alert_type='paper_entry'.
        # Gate on status==STATUS_TRIGGERED (entered AND still OPEN): a single
        # evaluation that already shows the trade closed (status terminal) must
        # NOT emit an "entry" alert — the operator never had a live window.
        # This is the other half of the 2026-06-16 simultaneous open+close fix.
        hold_lifecycle_for_retry = False
        if paper_entry_notifier is not None and should_alert_paper_entry(
            bool(outcome.entry_triggered), status
        ):
            # Latency telemetry (add-only, fail-open, ONCE per signal): record entry-touch detection
            # and the ACTUAL alert outcome. Pure observability — never changes execution/scoring/
            # alert routing. `entry_condition_detected` is gated on the real waiting→triggered
            # transition (and emit-once) so a repeated tick can't re-log an already-entered signal.
            try:
                from src.notifiers.paper_entry import send_paper_entry_alert
                decision_started = time.perf_counter()
                alert_signal = dict(execution_row)
                paper_profile = (
                    getattr(outcome, "_paper_entry_profile", None)
                    or (active_paper_entry or {}).get("paper_entry_profile")
                )
                if paper_profile:
                    alert_signal["paper_entry_profile"] = paper_profile
                execution_entry_mode = (
                    getattr(outcome, "_paper_execution_entry_mode", None)
                    or (active_paper_entry or {}).get("paper_execution_entry_mode")
                )
                source_entry_mode = getattr(outcome, "_paper_source_entry_mode", None)
                if execution_entry_mode:
                    alert_signal["paper_execution_entry_mode"] = execution_entry_mode
                if source_entry_mode:
                    alert_signal["paper_source_entry_mode"] = source_entry_mode
                profile_size_weight = _to_float(
                    getattr(outcome, "_paper_size_weight", None)
                )
                if profile_size_weight is not None:
                    alert_signal["paper_size_weight"] = profile_size_weight
                    alert_signal["paper_size_reason"] = str(
                        getattr(outcome, "_paper_size_reason", None) or ""
                    )
                res = send_paper_entry_alert(
                    store=store,
                    notifier=paper_entry_notifier,
                    signal=alert_signal,
                    prev_status=prev_status,
                    outcome_entry_triggered=bool(outcome.entry_triggered),
                    outcome_entry_triggered_at=(
                        getattr(outcome, "_decision_at", None)
                        if getattr(outcome, "_entry_currently_executable", None) is True
                        else outcome.entry_triggered_at),
                    outcome_entry_price_used=(
                        getattr(outcome, "_first_executable_price", None)
                        if getattr(outcome, "_entry_currently_executable", None) is True
                        else outcome.entry_price_used),
                    outcome_entry_bar_open_at=outcome.entry_triggered_at,
                    outcome_entry_time_basis=getattr(
                        outcome, "_entry_time_basis", "historical_bar_range"),
                    outcome_entry_currently_executable=getattr(
                        outcome, "_entry_currently_executable", None),
                    outcome_entry_revalidation_reason=getattr(
                        outcome, "_entry_revalidation_reason", ""),
                    outcome_entry_bar_timeframe=getattr(
                        outcome, "_entry_bar_timeframe", None),
                    dry_run=paper_entry_dry_run,
                )
                hold_lifecycle_for_retry = bool(
                    is_entry_transition
                    and isinstance(res, dict)
                    and res.get("reason_skipped") == "delivery_persistence_error"
                )
                decision_runtime_ms = round((time.perf_counter() - decision_started) * 1000.0, 1)
                timing_note = [f"stage_runtime_ms={decision_runtime_ms}"]
                if isinstance(res, dict):
                    for key, label in (
                        ("pre_capture_runtime_ms", "pre_capture_ms"),
                        ("live_capture_runtime_ms", "live_capture_ms"),
                        ("post_capture_runtime_ms", "post_capture_ms"),
                    ):
                        value = res.get(key)
                        if isinstance(value, (int, float)):
                            timing_note.append(f"{label}={value}")
                    capture_status = (res.get("payload") or {}).get("mexc_canary_capture_status")
                    if capture_status:
                        timing_note.append(f"capture_status={capture_status}")
                _emit_latency_event(
                    store, row, outcome, "paper_entry_decision_completed", once=True,
                    source=telemetry_source, note="; ".join(timing_note),
                )
                # Only record a SENT event when the alert was actually pushed; a duplicate / shadow /
                # not-actionable / late skip records `paper_entry_alert_skipped` with its reason.
                if isinstance(res, dict) and res.get("sent") is True:
                    _emit_latency_event(store, row, outcome, "paper_entry_alert_sent", once=True,
                                        source=telemetry_source)
                elif (isinstance(res, dict)
                      and str(res.get("telegram_status") or "").startswith("queued:")):
                    _emit_latency_event(store, row, outcome, "paper_entry_alert_queued", once=True,
                                        source=telemetry_source)
                else:
                    reason = (res.get("reason_skipped") if isinstance(res, dict) else None) or "skipped"
                    _emit_latency_event(store, row, outcome, "paper_entry_alert_skipped",
                                        once=True, note=str(reason), source=telemetry_source)
            except Exception:
                # Never block the tracker on alert failures.
                hold_lifecycle_for_retry = bool(is_entry_transition)
                _emit_latency_event(store, row, outcome, "paper_entry_alert_failed", once=True,
                                    source=telemetry_source)
                pass
        # Persist lifecycle after the Paper decision has been durably staged.
        # If staging itself fails, proposed_signals remains pending and the next
        # monitor tick can retry instead of losing the entry forever.
        if status != prev_status and not hold_lifecycle_for_retry:
            changed = store.update_signal_status(
                row["signal_id"],
                status=status,
                updated_at=_iso(now),
            )
            if changed:
                result.updated += 1
        # Close / outcome Telegram alert hook. Fires once per signal ONLY on a
        # GENUINE terminal transition out of the OPEN state. We key on `status`
        # (terminal) NOT on `outcome.final_outcome`, because _classify returns
        # OUTCOME_EXPIRED as a placeholder for still-open trades — keying on it
        # made the hook fire a bogus close_expired in the same tick as the
        # paper-entry (2026-06-16 simultaneous open+close fix). Requiring
        # prev_status==STATUS_TRIGGERED also means a close is only sent for a
        # trade that was previously announced as open, so a same-tick round
        # trip (enter+close in one evaluation) pushes neither alert. The
        # prev_status terminal guard inside decide_close remains as defense in
        # depth against the historical-backfill flood on deploy/restart.
        if paper_entry_notifier is not None and should_alert_close(status, prev_status):
            try:
                from src.notifiers.close_alert import send_close_alert
                send_close_alert(
                    store=store,
                    notifier=paper_entry_notifier,
                    signal=row,
                    outcome_row=outcome.to_row(),
                    prev_status=prev_status,
                    dry_run=paper_entry_dry_run,
                )
            except Exception:
                pass
        if status == STATUS_STOPPED:
            result.stopped += 1
        if status in (STATUS_TP1, STATUS_TP2, STATUS_TP3):
            result.tp_hits += 1
        if status == STATUS_AMBIGUOUS:
            result.ambiguous += 1
        if status == STATUS_MISSED_NO_ENTRY:
            result.not_triggered += 1
        if status == STATUS_EXPIRED:
            result.expired += 1
        result.details.append(
            {
                "signal_id": row["signal_id"],
                "symbol": row.get("symbol"),
                "previous_status": prev_status,
                "new_status": status,
                "final_outcome": outcome.final_outcome,
                "final_r": outcome.final_r,
            }
        )
    return result


# ===========================================================================
# Option B (2026-06-16): lightweight pending-only entry tracker for the 5-min
# monitor tick, so entry-touch is detected in ~minutes instead of the ~2h full
# `track-signals` cadence (see reports/LATENCY_REDUCTION_OPTIONS.md).
#
# Safety model:
#   * scoped to tier A/B, non-terminal signals only — no full scan, no scoring,
#     no news/LLM, no report;
#   * reuses track_active_signals → same status gates + alert dedup (idempotent,
#     so it can never double-fire vs the full pass);
#   * legacy pending workers keep their own exclusive lock so two lightweight
#     ticks never overlap;
#   * full and pending passes coordinate per signal_id, so the same lifecycle
#     cannot be mutated concurrently while unrelated signals remain unblocked;
#   * DB is WAL + busy_timeout (SQLiteStore.connect) so concurrent writers
#     serialize instead of erroring.
# ===========================================================================

_LOCK_DIRNAME = ".locks"
_FULL_PASS_MARKER = "track_signals_full.running"
_PENDING_LOCK = "track_pending.lock"
_STALE_LOCK_SEC = 1800.0  # 30 min — steal a lock older than this (dead process)
# The full-pass marker and the legacy pending-wide locks are retained for
# backward compatibility with older workers. They are not the cross-worker
# safety boundary. signal_writer_lock() is the strict guarantee between current
# full and pending passes, scoped to one signal_id.
_PENDING_WAIT_TIMEOUT_SEC = 5.0
_PENDING_WAIT_POLL_SEC = 0.25

# ---- legacy pending-wide mutex -----------------------------------------------------------------
# Retained so older pending workers cannot overlap a current pending worker.
# Current full/pending coordination is performed by signal_writer_lock().
_WRITER_LOCK = "tracker_writer.lock"
_WRITER_STALE_SEC = _STALE_LOCK_SEC       # same "unambiguously orphaned" threshold — 30 min
_WRITER_BLOCK_TIMEOUT_SEC = 10.0          # full pass: bounded wait for an in-flight pending pass
_WRITER_POLL_SEC = 0.1
_SIGNAL_WRITER_PREFIX = "tracker_signal_"


def _pid_is_running(pid: int) -> bool:
    """Cross-platform process liveness check used only for orphan lock repair."""
    if pid <= 0:
        return False
    if os.name == "nt":
        try:
            import ctypes

            handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)
            if not handle:
                return False
            ctypes.windll.kernel32.CloseHandle(handle)
            return True
        except Exception:
            return True  # fail conservative: never steal when liveness is unknown
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return True
    return True


def _lock_is_reclaimable(lock: Path, *, stale_sec: float) -> bool:
    """A lock is reclaimable when old, or when its recorded owner is dead.

    An empty/partially-written fresh lock is treated as live.  That preserves
    atomicity during the tiny window between O_EXCL creation and PID write.
    """
    try:
        if time.time() - lock.stat().st_mtime > stale_sec:
            return True
        owner_text = lock.read_text(encoding="utf-8").strip().split()
        if not owner_text:
            return False
        return not _pid_is_running(int(owner_text[0]))
    except (OSError, ValueError):
        return False


def _try_acquire_writer_lock_once(root: Path) -> int | None:
    """One atomic attempt. Returns an open fd on success, None if the lock is held
    and not (yet) stale. Only steals a lock that is unambiguously old — never a
    fresh one, regardless of caller."""
    lock = _lock_dir(root) / _WRITER_LOCK
    try:
        return os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        try:
            if _lock_is_reclaimable(lock, stale_sec=_WRITER_STALE_SEC):
                lock.unlink()
                return os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except Exception:
            pass
        return None


def _signal_writer_lock_path(root: Path, signal_id: str) -> Path:
    digest = hashlib.sha1(str(signal_id).encode("utf-8")).hexdigest()
    return _lock_dir(root) / f"{_SIGNAL_WRITER_PREFIX}{digest}.lock"


def _try_acquire_signal_writer_lock_once(root: Path, signal_id: str) -> tuple[int | None, Path]:
    lock = _signal_writer_lock_path(root, signal_id)
    try:
        return os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY), lock
    except FileExistsError:
        try:
            if _lock_is_reclaimable(lock, stale_sec=_WRITER_STALE_SEC):
                lock.unlink()
                return os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY), lock
        except Exception:
            pass
        return None, lock


@contextmanager
def signal_writer_lock(root: Path, signal_id: str, *, blocking: bool):
    """Serialize writes for one signal without blocking unrelated signals."""
    fd, lock = _try_acquire_signal_writer_lock_once(root, signal_id)
    waited = 0.0
    if fd is None and blocking:
        while fd is None and waited < _WRITER_BLOCK_TIMEOUT_SEC:
            time.sleep(_WRITER_POLL_SEC)
            waited += _WRITER_POLL_SEC
            fd, lock = _try_acquire_signal_writer_lock_once(root, signal_id)
    if fd is None:
        yield False
        return
    try:
        try:
            os.write(fd, f"{os.getpid()} {_iso(_now())} {signal_id}".encode("utf-8"))
        except Exception:
            pass
        yield True
    finally:
        try:
            os.close(fd)
        except Exception:
            pass
        try:
            lock.unlink()
        except Exception:
            pass


@contextmanager
def writer_lock(root: Path, *, blocking: bool):
    """Legacy pending-wide mutual exclusion kept for worker compatibility.

    Current full/pending passes use ``signal_writer_lock`` as their strict
    cross-worker boundary. This broader lock only prevents overlapping legacy
    lightweight passes and must not be reintroduced around a full sweep because
    that would stall fresh entries for unrelated symbols.

    ``blocking=True`` retries for up to _WRITER_BLOCK_TIMEOUT_SEC. The current
    pending path uses ``blocking=False`` and fails fast.

    Windows-safe: the fd is closed on the SAME thread/process that opened it, before
    unlink — never delete the lock file from another thread while its fd is open
    elsewhere (that fails with PermissionError on Windows)."""
    fd = _try_acquire_writer_lock_once(root)
    waited = 0.0
    if fd is None and blocking:
        while fd is None and waited < _WRITER_BLOCK_TIMEOUT_SEC:
            time.sleep(_WRITER_POLL_SEC)
            waited += _WRITER_POLL_SEC
            fd = _try_acquire_writer_lock_once(root)
    if fd is None:
        yield False
        return
    lock = _lock_dir(root) / _WRITER_LOCK
    try:
        try:
            os.write(fd, f"{os.getpid()} {_iso(_now())}".encode("utf-8"))
        except Exception:
            pass
        yield True
    finally:
        try:
            os.close(fd)
        except Exception:
            pass
        try:
            lock.unlink()
        except Exception:
            pass


def _lock_dir(root: Path) -> Path:
    d = Path(root) / _LOCK_DIRNAME
    try:
        d.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    return d


def _pending_lock_active(root: Path) -> bool:
    """True if the pending-pass lockfile is currently held and fresh — the mirror
    check of _full_pass_active(), used by the full pass to detect an
    already-in-flight pending pass before it starts (see _PENDING_WAIT_* above)."""
    p = _lock_dir(root) / _PENDING_LOCK
    try:
        if not p.exists():
            return False
        if _lock_is_reclaimable(p, stale_sec=_STALE_LOCK_SEC):
            p.unlink()
            return False
        return (time.time() - p.stat().st_mtime) < _STALE_LOCK_SEC
    except Exception:
        return False


@contextmanager
def full_pass_marker(root: Path):
    """Mark that the full `track-signals` pass is running so the lightweight
    pending tracker yields to it. Best-effort — never blocks the full pass.

    Symmetric half of the coordination: before claiming the marker, wait briefly
    (bounded by _PENDING_WAIT_TIMEOUT_SEC) for an already-in-flight pending pass
    to finish and release its lockfile, so the two never process the same
    signal_id concurrently. Never waits indefinitely — a stuck/orphaned pending
    lock must never delay the primary 2h outcome sweep."""
    waited = 0.0
    while _pending_lock_active(root) and waited < _PENDING_WAIT_TIMEOUT_SEC:
        time.sleep(_PENDING_WAIT_POLL_SEC)
        waited += _PENDING_WAIT_POLL_SEC
    p = _lock_dir(root) / _FULL_PASS_MARKER
    wrote = False
    try:
        p.write_text(f"{os.getpid()} {_iso(_now())}", encoding="utf-8")
        wrote = True
    except Exception:
        wrote = False
    try:
        yield
    finally:
        if wrote:
            try:
                p.unlink()
            except Exception:
                pass


def _full_pass_active(root: Path) -> bool:
    p = _lock_dir(root) / _FULL_PASS_MARKER
    try:
        if not p.exists():
            return False
        if _lock_is_reclaimable(p, stale_sec=_STALE_LOCK_SEC):
            p.unlink()
            return False
        # ignore a stale marker left by a crashed full pass
        return (time.time() - p.stat().st_mtime) < _STALE_LOCK_SEC
    except Exception:
        return False


@contextmanager
def _pending_lock(root: Path):
    """Exclusive lock for the lightweight pending pass. Yields True if acquired,
    False if the full pass or another pending tick holds it (caller must skip)."""
    if _full_pass_active(root):
        yield False
        return
    lock = _lock_dir(root) / _PENDING_LOCK
    fd = None
    try:
        try:
            fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            # steal only if clearly stale (dead process)
            try:
                if _lock_is_reclaimable(lock, stale_sec=_STALE_LOCK_SEC):
                    lock.unlink()
                    fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                else:
                    yield False
                    return
            except Exception:
                yield False
                return
        try:
            os.write(fd, f"{os.getpid()} {_iso(_now())}".encode("utf-8"))
        except Exception:
            pass
        yield True
    finally:
        if fd is not None:
            try:
                os.close(fd)
            except Exception:
                pass
            try:
                lock.unlink()
            except Exception:
                pass


# Modes that never emit actionable alerts (paper-paused) are excluded from the
# latency-critical pass. Crypto scalp is retained in the historical journal,
# but its strategy is disabled and no longer merits continuous OHLCV refreshes.
_FAST_PASS_PAUSED = {
    ("crypto", "scalp"),
    ("stocks", "swing"),
    ("stocks", "invest"),
}


def select_pending_ab_signal_ids(store: SQLiteStore, *, asset_class: str | None = None,
                                 modes: set[str] | None = None) -> list[str]:
    """Tier A/B, non-terminal, non-paused signals — the universe the lightweight
    pass re-checks. (load_active_signals already restricts to non-terminal
    statuses.) Paper-paused stocks swing/invest are excluded: they never alert,
    so fast-tracking them is pure waste and would touch paused modes needlessly.

    When ``asset_class`` is given (e.g. "crypto"), ONLY that asset class is returned — this is what
    keeps the fast `pending-monitor` crypto-only. ``modes`` optionally restricts to a set of modes.
    Both default to None → the legacy all-asset behaviour (used by `monitor-watchlist`)."""
    want_ac = str(asset_class).lower() if asset_class else None
    want_modes = {str(m).lower() for m in modes} if modes else None
    ids: list[str] = []
    for r in store.load_active_signals():
        tier = str(r.get("tier") or "").upper()
        asset = str(r.get("asset_class") or "crypto").lower()
        mode = str(r.get("mode") or "").lower()
        if tier not in ("A", "B") or not r.get("signal_id"):
            continue
        if (asset, mode) in _FAST_PASS_PAUSED:
            continue
        if want_ac is not None and asset != want_ac:
            continue
        if want_modes is not None and mode not in want_modes:
            continue
        ids.append(str(r["signal_id"]))
    return ids


def track_pending_entries(
    *,
    store: SQLiteStore,
    file_store: FileStore,
    project_config: ProjectConfig,
    tracker_config: SignalTrackingConfig,
    paper_entry_notifier: Any = None,
    paper_entry_dry_run: bool = False,
    asset_class: str | None = None,
    modes: set[str] | None = None,
    signal_ids: Iterable[str] | None = None,
    telemetry_source: str = "track-signals",
) -> TrackingResult:
    """Lightweight Option-B pass: detect entry-touch / terminal outcomes for
    tier A/B non-terminal signals only, firing paper-entry/close alerts via the
    same (idempotent, status-gated) path as the full tracker. It coordinates with
    the full pass per signal_id and returns an empty result when skipped or when
    nothing is pending.

    ``asset_class``/``modes`` scope the selection — the fast `pending-monitor` passes
    ``asset_class="crypto"`` so it never touches stocks intraday. Both default to None → the legacy
    all-asset behaviour (unchanged for `monitor-watchlist`).

    ``signal_ids``: when the caller already selected the pending ids, pass them here so the SAME
    snapshot is tracked (keeps the caller's `selected` count consistent with `checked`); otherwise
    the ids are (re)selected internally with the same rules. ``telemetry_source`` sets the `source`
    on the latency-telemetry events so SLA can attribute fast-path latency to "pending-monitor".
    Neither changes selection rules, status/alert gates, or outcome semantics."""
    root = project_config.root
    with _pending_lock(root) as acquired:
        if not acquired:
            return TrackingResult(skip_reason="pending_or_full_pass_lock_contended")
        ids = list(signal_ids) if signal_ids is not None else \
            select_pending_ab_signal_ids(store, asset_class=asset_class, modes=modes)
        if not ids:
            return TrackingResult()
        # Keep legacy pending workers mutually exclusive. Cross-worker lifecycle
        # safety against the full pass is enforced per signal_id below.
        with writer_lock(root, blocking=False) as got_lock:
            if not got_lock:
                return TrackingResult(skip_reason="writer_lock_contended")
            return track_active_signals(
                store=store,
                file_store=file_store,
                project_config=project_config,
                tracker_config=tracker_config,
                signal_ids=ids,
                paper_entry_notifier=paper_entry_notifier,
                paper_entry_dry_run=paper_entry_dry_run,
                telemetry_source=telemetry_source,
                coordinate_signal_writes=True,
                signal_lock_blocking=False,
            )
