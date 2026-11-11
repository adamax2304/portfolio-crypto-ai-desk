"""Alert-only circuit breaker (profitability guardrails stage).

Computes a per-day, per-asset/mode realised-R + stop-count state and emits
"would-pause" diagnostics. It NEVER blocks a trade, changes size, or changes
routing — every output is a flag/label with ``diagnostic_only=True``.

Evidence motivating it (see CIRCUIT_BREAKER_WOULD_PAUSE_AUDIT.md): on 06-15 the
engine took 27+ crypto stops and on 06-17 16+, opening new longs throughout,
with no daily-loss / consecutive-stop halt anywhere in the engine.

Thresholds (alert-only):
  * daily realised <= -2R          -> level L2
  * daily realised <= -3R          -> level L3
  * >= 3 stops same asset/mode/day -> stops trigger
  * >= 2 crypto long stops same regime/day -> crypto-long-streak trigger
  * >= 1 stop today                -> size-stepdown CANDIDATE (flag only)
  * >= 3 consecutive stops OR crypto-long-streak -> require-fresh-catalyst flag
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


# Terminal outcomes that count as a realised stop/loss.
def _is_stop(row: dict[str, Any]) -> bool:
    if str(row.get("final_outcome") or "").lower() == "loss":
        return True
    try:
        return int(row.get("stop_hit") or 0) == 1
    except (TypeError, ValueError):
        return False


def _r(row: dict[str, Any]) -> float:
    try:
        return float(row.get("final_r") or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _exit_dt(row: dict[str, Any]) -> datetime | None:
    ts = row.get("exit_at") or row.get("checked_at")
    if not ts:
        return None
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    except Exception:
        return None


@dataclass(frozen=True)
class CircuitBreakerConfig:
    """Alert-only thresholds. Changing these changes ONLY when a diagnostic
    flag fires — it never blocks anything."""
    daily_r_l2: float = -2.0
    daily_r_l3: float = -3.0
    stops_per_day: int = 3
    crypto_long_streak: int = 2
    consec_for_fresh_catalyst: int = 3


def _day_key(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%d")


def evaluate_circuit_breaker(
    rows: list[dict[str, Any]],
    *,
    scope_asset: str | None = None,
    scope_mode: str | None = None,
    scope_direction: str | None = None,
    scope_regime: str | None = None,
    mode_isolated: bool = False,
    now: datetime | None = None,
    config: CircuitBreakerConfig | None = None,
) -> dict[str, Any]:
    """Pure evaluator. ``rows`` are terminal outcomes (each with final_r,
    final_outcome/stop_hit, exit_at, asset_class, mode, direction, market_regime).

    Returns the circuit-breaker diagnostic field dict for the scope of a
    prospective new entry (its asset_class/mode/direction/regime). Never raises.
    """
    cfg = config or CircuitBreakerConfig()
    now = now or datetime.now(timezone.utc)
    today = _day_key(now)

    asset = (scope_asset or "").lower() or None
    mode = (scope_mode or "").lower() or None
    direction = (scope_direction or "").lower() or None
    regime = (scope_regime or "").lower() or None

    def _today_rows():
        out = []
        for row in rows:
            dt = _exit_dt(row)
            if dt is None or _day_key(dt) != today:
                continue
            if asset and str(row.get("asset_class") or "").lower() != asset:
                continue
            out.append(row)
        return out

    asset_rows = _today_rows()
    asset_rows.sort(key=lambda r: (_exit_dt(r) or now))
    mode_rows = [r for r in asset_rows
                 if not mode or str(r.get("mode") or "").lower() == mode]

    day_r_asset = round(sum(_r(r) for r in asset_rows), 2)
    day_r_scope = round(sum(_r(r) for r in mode_rows), 2)
    stops_asset = sum(1 for r in asset_rows if _is_stop(r))
    stops_scope = sum(1 for r in mode_rows if _is_stop(r))

    # consecutive stops on the scope (asset+mode), trailing run in exit order
    consec = 0
    for r in reversed(mode_rows):
        if _is_stop(r):
            consec += 1
        else:
            break

    # crypto long stops in the same regime today
    crypto_long_streak = 0
    if asset == "crypto":
        for r in asset_rows:
            if (str(r.get("direction") or "").lower() == "long"
                    and _is_stop(r)
                    and (regime is None
                         or str(r.get("market_regime") or "").lower() == regime)):
                crypto_long_streak += 1

    last_stop = None
    for r in reversed(mode_rows):
        if _is_stop(r):
            last_stop = r.get("exit_at")
            break

    # The default diagnostic view is intentionally conservative: a clean mode
    # does not mask a bleeding asset book.  Paper routing also needs a separate
    # mode-isolated view so intraday noise cannot suppress independent swing
    # evidence; the asset-wide number remains available for a hard portfolio
    # emergency floor.
    threshold_r = day_r_scope if mode_isolated else min(day_r_asset, day_r_scope)

    breaches: list[str] = []
    level = 0
    if threshold_r <= cfg.daily_r_l3:
        level = 3
        breaches.append(f"daily {threshold_r:g}R <= {cfg.daily_r_l3:g}R")
    elif threshold_r <= cfg.daily_r_l2:
        level = 2
        breaches.append(f"daily {threshold_r:g}R <= {cfg.daily_r_l2:g}R")
    if stops_scope >= cfg.stops_per_day:
        level = max(level, 2)
        breaches.append(f"{stops_scope} stops today ({asset or 'all'}"
                        f"{'/' + mode if mode else ''})")
    if crypto_long_streak >= cfg.crypto_long_streak:
        level = max(level, 2)
        breaches.append(f"{crypto_long_streak} crypto long stops same regime")

    state = "would_pause" if level >= 2 else ("watch" if (
        stops_scope >= 1 or threshold_r < 0) else "ok")

    would_pause = level >= 2
    would_throttle_crypto_longs = crypto_long_streak >= cfg.crypto_long_streak
    would_reduce_size = stops_scope >= 1  # stepdown candidate after first stop
    would_require_fresh_catalyst = (
        consec >= cfg.consec_for_fresh_catalyst
        or crypto_long_streak >= cfg.crypto_long_streak
    )

    reason = "; ".join(breaches) if breaches else (
        "watch: drawdown/stops building" if state == "watch" else "no breach")

    return {
        "circuit_breaker_state": state,
        "circuit_breaker_level": level,
        "circuit_breaker_reason": reason,
        "day_realized_r": day_r_scope,
        "day_realized_r_asset": day_r_asset,
        "stops_today": stops_scope,
        "stops_today_asset": stops_asset,
        "consecutive_stops": consec,
        "crypto_long_streak_count": crypto_long_streak,
        "last_stop_time": last_stop,
        "would_pause_new_entries": would_pause,
        "would_throttle_crypto_longs": would_throttle_crypto_longs,
        "would_reduce_size": would_reduce_size,
        "would_require_fresh_catalyst": would_require_fresh_catalyst,
        "diagnostic_only": True,
    }


def _start_of_utc_day(now: datetime) -> str:
    d = now.astimezone(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0)
    return d.isoformat()


def circuit_breaker_for_signal(
    store: Any,
    signal: dict[str, Any],
    *,
    now: datetime | None = None,
    config: CircuitBreakerConfig | None = None,
) -> dict[str, Any]:
    """Store-driven wrapper for the paper-entry path. Loads today's terminal
    outcomes and evaluates the breaker for this signal's scope. Fails open
    (returns an 'ok' state) on any error so it can never break the loop."""
    now = now or datetime.now(timezone.utc)
    try:
        rows = store.load_recent_terminal_outcomes(_start_of_utc_day(now))
        return evaluate_circuit_breaker(
            rows,
            scope_asset=signal.get("asset_class") or "crypto",
            scope_mode=signal.get("mode"),
            scope_direction=signal.get("direction"),
            scope_regime=signal.get("market_regime"),
            now=now,
            config=config,
        )
    except Exception:
        return {
            "circuit_breaker_state": "ok",
            "circuit_breaker_level": 0,
            "circuit_breaker_reason": "unavailable",
            "day_realized_r": None,
            "stops_today": None,
            "consecutive_stops": None,
            "crypto_long_streak_count": None,
            "would_pause_new_entries": False,
            "would_throttle_crypto_longs": False,
            "would_reduce_size": False,
            "would_require_fresh_catalyst": False,
            "diagnostic_only": True,
        }


def paper_circuit_breaker_for_signal(
    store: Any,
    signal: dict[str, Any],
    *,
    now: datetime | None = None,
    config: CircuitBreakerConfig | None = None,
) -> dict[str, Any]:
    """Evaluate the authoritative Paper-only circuit-breaker view.

    Unlike :func:`circuit_breaker_for_signal`, this helper never reads legacy
    ``signal_outcomes.final_r`` and never sees shadow-only trades.  Its input
    is the active-fee-profile Paper ledger and its PnL is normalised from
    realised ``net_pnl_usdt / risk_usdt`` solely to retain the existing
    R-based circuit-breaker thresholds.
    """
    now = now or datetime.now(timezone.utc)
    try:
        from src.execution.paper_portfolio import load_cfg

        fee_profile = str(load_cfg().get("fee_profile") or "bybit_default_futures")
        rows = store.load_recent_paper_terminal_outcomes(
            _start_of_utc_day(now), fee_profile=fee_profile
        )
        result = evaluate_circuit_breaker(
            rows,
            scope_asset=signal.get("asset_class") or "crypto",
            scope_mode=signal.get("mode"),
            scope_direction=signal.get("direction"),
            scope_regime=signal.get("market_regime"),
            now=now,
            config=config,
        )
        mode_result = evaluate_circuit_breaker(
            rows,
            scope_asset=signal.get("asset_class") or "crypto",
            scope_mode=signal.get("mode"),
            scope_direction=signal.get("direction"),
            scope_regime=signal.get("market_regime"),
            now=now,
            config=config,
            mode_isolated=True,
        )
        return {
            f"paper_{key}": value
            for key, value in result.items()
            if key != "diagnostic_only"
        } | {
            f"paper_mode_{key}": value
            for key, value in mode_result.items()
            if key != "diagnostic_only"
        } | {
            "paper_circuit_breaker_fee_profile": fee_profile,
            "paper_circuit_breaker_source": "accepted_point_in_time_paper_ledger",
            "paper_circuit_breaker_evidence_count": len(rows),
        }
    except Exception:
        return {
            "paper_circuit_breaker_state": "ok",
            "paper_circuit_breaker_level": 0,
            "paper_circuit_breaker_reason": "unavailable",
            "paper_would_pause_new_entries": False,
            "paper_circuit_breaker_fee_profile": None,
            "paper_circuit_breaker_source": "unavailable",
            "paper_circuit_breaker_evidence_count": 0,
        }


def circuit_breaker_warning_line(state: dict[str, Any]) -> str | None:
    """Compact one-line Telegram warning, or None if nothing to warn about."""
    if not state or state.get("circuit_breaker_state") != "would_pause":
        return None
    dr = state.get("day_realized_r")
    stops = state.get("stops_today")
    parts = []
    if dr is not None:
        parts.append(f"{dr:g}R today")
    if stops:
        parts.append(f"{stops} stops")
    detail = " / ".join(parts) if parts else state.get("circuit_breaker_reason", "")
    return f"⚠ Circuit breaker would pause new entries ({detail}) — diagnostic, not blocked"
