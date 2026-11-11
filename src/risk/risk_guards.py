"""Risk-guard visibility field assembler with a narrow paper-only floor.

Composes the diagnostic field bundle attached to the paper-entry payload (and
usable by reports / Control Plane). Every sub-computation fails open, so this
can never break the alert path. The diagnostic fields never change scoring,
TP/SL, live routing, or existing positions. A separate, explicit helper may
apply one conservative new-entry floor in paper only.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.risk.circuit_breaker import (
    circuit_breaker_for_signal,
    circuit_breaker_warning_line,
    paper_circuit_breaker_for_signal,
)
from src.risk.risk_off import compute_risk_off
from src.signals.lifecycle import compute_lifecycle_label
from src.signals.sector_cap_shadow import would_bind_sector_cap


_DEFAULT_PAPER_RISK_AUTHORITY = {
    "enabled": True,
    "paper_only": True,
    "live_enabled": False,
    "crypto_modes": ("intraday", "swing"),
    "circuit_breaker": {
        "enabled": True,
        "required_state": "would_pause",
        "min_level": 2,
        # A normal sequence of stopped Paper trades should reduce new-entry
        # risk before it suppresses the whole research lane.  A wider
        # portfolio-level loss remains a hard pause below.
        "l2_action": "HALF_SIZE",
        "l3_action": "HALF_SIZE",
        "scope": "mode_isolated",
        "global_pause_daily_r": -5.0,
        "global_pause_action": "SHADOW_ONLY",
    },
}


def load_paper_risk_authority() -> dict[str, Any]:
    """Load the narrow paper-only authority switch.

    A malformed or unavailable registry must preserve the old diagnostic-only
    behaviour. This helper therefore fails closed for the *new authority* (no
    block), while the existing diagnostic fields continue to be best-effort.
    """
    try:
        import yaml

        path = Path(__file__).resolve().parents[2] / "config" / "paper_features.yaml"
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        cfg = raw.get("paper_risk_authority") or {}
        cb = cfg.get("circuit_breaker") or {}
        if not isinstance(cfg, dict) or not isinstance(cb, dict):
            return {"enabled": False, "paper_only": True, "live_enabled": False}
        modes = cfg.get("crypto_modes", _DEFAULT_PAPER_RISK_AUTHORITY["crypto_modes"])
        if isinstance(modes, str):
            modes = (modes,)
        return {
            "enabled": bool(cfg.get("enabled", False)),
            "paper_only": bool(cfg.get("paper_only", True)),
            "live_enabled": bool(cfg.get("live_enabled", False)),
            "crypto_modes": tuple(str(x).lower() for x in modes),
            "circuit_breaker": {
                "enabled": bool(cb.get("enabled", False)),
                "required_state": str(cb.get("required_state", "would_pause")),
                "min_level": int(cb.get("min_level", 2)),
                # `action` is retained as a backward-compatible fallback for
                # older operator config files.
                "l2_action": str(cb.get("l2_action", cb.get("action", "SHADOW_ONLY"))),
                "l3_action": str(cb.get("l3_action", cb.get("action", "SHADOW_ONLY"))),
                "scope": str(cb.get("scope", "mode_isolated")),
                "global_pause_daily_r": float(cb.get("global_pause_daily_r", -5.0)),
                "global_pause_action": str(cb.get("global_pause_action", "SHADOW_ONLY")),
            },
        }
    except Exception:
        return {"enabled": False, "paper_only": True, "live_enabled": False}


def paper_risk_floor(
    fields: dict[str, Any],
    signal: dict[str, Any],
    *,
    cfg: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return the worst confirmed paper-only floor for a new crypto entry.

    Circuit-breaker L2+ and a persistent, multi-venue stablecoin depeg are the
    only authoritative inputs.  The circuit-breaker is deliberately
    graduated: a normal mode drawdown reduces fresh entries to HALF_SIZE;
    only a materially worse asset-wide loss pauses the crypto book.  All other
    diagnostics remain visibility-only.
    This function never upgrades, closes, or modifies an existing position.
    """
    cfg = cfg if cfg is not None else load_paper_risk_authority()
    empty = {
        "paper_risk_floor_action": None,
        "paper_risk_floor_size_weight": None,
        "paper_risk_floor_source": None,
        "paper_risk_floor_reason": None,
    }
    if not isinstance(cfg, dict) or not cfg.get("enabled") or not cfg.get("paper_only"):
        return empty
    if cfg.get("live_enabled"):
        return empty
    asset = str(signal.get("asset_class") or "crypto").lower()
    mode = str(signal.get("mode") or "").lower()
    if asset != "crypto":
        return empty
    candidates: list[tuple[int, str, str, str]] = []

    cb_cfg = cfg.get("circuit_breaker") or {}
    if cb_cfg.get("enabled") and mode in tuple(cfg.get("crypto_modes") or ("intraday", "swing")):
        isolated = str(cb_cfg.get("scope") or "mode_isolated") == "mode_isolated"
        prefix = "paper_mode_" if isolated else "paper_"
        state = str(fields.get(f"{prefix}circuit_breaker_state") or "")
        try:
            level = int(fields.get(f"{prefix}circuit_breaker_level") or 0)
            min_level = int(cb_cfg.get("min_level") or 2)
        except (TypeError, ValueError):
            level = 0
            min_level = 2
        try:
            asset_r = float(fields.get("paper_day_realized_r_asset"))
        except (TypeError, ValueError):
            asset_r = None
        try:
            global_pause_r = float(cb_cfg.get("global_pause_daily_r", -5.0))
        except (TypeError, ValueError):
            global_pause_r = -5.0
        if asset_r is not None and asset_r <= global_pause_r:
            action = str(cb_cfg.get("global_pause_action") or "SHADOW_ONLY")
            reason = (f"paper-ledger global crypto drawdown {asset_r:g}R <= "
                      f"{global_pause_r:g}R: new crypto paper entries paused")
            if action in ("HALF_SIZE", "SHADOW_ONLY", "BLOCK"):
                severity = {"HALF_SIZE": 1, "SHADOW_ONLY": 2, "BLOCK": 3}[action]
                candidates.append((severity, action, "paper_risk_guard_circuit_breaker", reason))
        elif state == str(cb_cfg.get("required_state") or "would_pause") and level >= min_level:
            action = str(cb_cfg.get("l3_action" if level >= 3 else "l2_action")
                         or "HALF_SIZE")
            scope_label = "mode-isolated " if isolated else ""
            reason = (f"paper-ledger {scope_label}circuit breaker {state} L{level}: "
                      "new crypto paper entries reduced")
            if action in ("HALF_SIZE", "SHADOW_ONLY", "BLOCK"):
                severity = {"HALF_SIZE": 1, "SHADOW_ONLY": 2, "BLOCK": 3}[action]
                candidates.append((severity, action, "paper_risk_guard_circuit_breaker", reason))

    peg_action = str(fields.get("stablecoin_guard_action") or "")
    if peg_action in ("SHADOW_ONLY", "BLOCK") and fields.get("stablecoin_guard_persistent") is True:
        state = str(fields.get("stablecoin_guard_state") or "STRESS")
        stable = str(fields.get("stablecoin_guard_asset") or "stablecoin")
        candidates.append((2 if peg_action == "SHADOW_ONLY" else 3, peg_action,
                           "paper_risk_guard_stablecoin_depeg",
                           f"persistent multi-venue {stable} depeg ({state}): new crypto entries paused"))

    if not candidates:
        return empty
    _, action, source, reason = max(candidates, key=lambda item: item[0])
    return {
        "paper_risk_floor_action": action,
        "paper_risk_floor_size_weight": 0.5 if action == "HALF_SIZE" else 0.0,
        "paper_risk_floor_source": source,
        "paper_risk_floor_reason": reason,
    }


def profit_protection_hint(mfe_r: float | None) -> dict[str, Any]:
    """Informational profit-protection hint from realised MFE (in R).

    At entry MFE≈0 → 'none'. As a trade runs, a refresh can pass the live MFE.
    These are HINTS only; profit protection stays disabled (config unchanged)."""
    if mfe_r is None:
        return {"profit_protection_hint": "unknown",
                "would_move_to_BE": None, "would_partial_TP1": None}
    if mfe_r >= 1.0:
        return {"profit_protection_hint": "reached_+1R",
                "would_move_to_BE": True, "would_partial_TP1": True}
    if mfe_r >= 0.5:
        return {"profit_protection_hint": "reached_+0.5R",
                "would_move_to_BE": True, "would_partial_TP1": False}
    return {"profit_protection_hint": "none",
            "would_move_to_BE": False, "would_partial_TP1": False}


def assemble_risk_guard_fields(
    store: Any,
    signal: dict[str, Any],
    *,
    file_store: Any = None,
    now: datetime | None = None,
    mfe_r: float | None = 0.0,
    regime_now: str | None = None,
    entry_triggered_at: str | None = None,
    latency_critical: bool = False,
) -> dict[str, Any]:
    """Build the full diagnostic field bundle.

    Each block is independently fail-open so a failure in one never drops the
    others. This function itself does not apply the paper floor; callers must
    explicitly invoke :func:`paper_risk_floor`.
    """
    now = now or datetime.now(timezone.utc)
    fields: dict[str, Any] = {}

    # The legacy breaker is diagnostic-only and scans the large historical
    # outcome table. It must not sit between an executable price and the Paper
    # decision. The authoritative Paper-ledger breaker below remains enabled.
    if not latency_critical:
        try:
            fields.update(circuit_breaker_for_signal(store, signal, now=now))
        except Exception:
            pass
    try:
        fields.update(paper_circuit_breaker_for_signal(store, signal, now=now))
    except Exception:
        pass
    if latency_critical:
        # Preserve the operator-facing warning contract without re-running the
        # legacy signal_outcomes scan. These aliases come from the same
        # authoritative, mode-isolated Paper-ledger result used by the floor.
        for key in (
            "circuit_breaker_state", "circuit_breaker_level",
            "circuit_breaker_reason", "would_pause_new_entries",
            "day_realized_r", "stops_today",
        ):
            paper_key = f"paper_mode_{key}"
            if paper_key in fields:
                fields[key] = fields[paper_key]
        fields["circuit_breaker_source"] = "accepted_point_in_time_paper_ledger"

    # Risk-off is already enforced by the point-in-time crypto overlay. Keep
    # this duplicate computation for reports, but not on the alert fast path.
    if not latency_critical:
        try:
            ro = compute_risk_off(file_store, now=now)
            fields.update(ro)
            if regime_now is None:
                regime_now = ro.get("regime_context")
        except Exception:
            pass

    # 3) intraday lifecycle (PART 5)
    if not latency_critical:
        try:
            fields.update(compute_lifecycle_label(
                signal, now=now, entry_triggered_at=entry_triggered_at,
                regime_at_entry=signal.get("market_regime"), regime_now=regime_now))
        except Exception:
            pass

    # 4) sector-cap shadow / would-bind (PART 3)
    if not latency_critical:
        try:
            fields.update(would_bind_sector_cap(store, signal, now=now))
        except Exception:
            pass

    # 5) profit-protection hint (PART 4 visibility)
    try:
        fields.update(profit_protection_hint(mfe_r))
    except Exception:
        pass

    # 6) catalyst integrity per-signal (PART 7 of prior stage)
    if not latency_critical:
        try:
            from src.catalysts.integrity import catalyst_integrity_for_signal
            with store.connect() as conn:
                fields.update(catalyst_integrity_for_signal(conn, signal))
        except Exception:
            pass

    # 6b) stocks-intraday C-tier restriction labels (FAST SAFE ACCELERATION)
    try:
        from src.signals.tier_policy import (
            c_tier_restriction_fields, load_stocks_intraday_c_tier_policy)
        fields.update(c_tier_restriction_fields(
            signal, load_stocks_intraday_c_tier_policy()))
    except Exception:
        pass

    # 7) position / leverage advisor — label-only (operational PART 7)
    # Systemic crypto collateral health. Only a persistent multi-venue depeg
    # can receive an action; missing or stale quotes stay diagnostic.
    try:
        from src.intelligence.market_risk_context import stablecoin_state
        peg = stablecoin_state(as_of=now)
        fields.update({
            "stablecoin_guard_state": peg.get("state"),
            "stablecoin_guard_action": peg.get("action"),
            "stablecoin_guard_reason": peg.get("reason"),
            "stablecoin_guard_asset": peg.get("stablecoin"),
            "stablecoin_guard_deviation_pct": peg.get("deviation_pct"),
            "stablecoin_guard_fresh_venues": peg.get("fresh_venues"),
            "stablecoin_guard_persistent": peg.get("persistent"),
            "stablecoin_guard_context_ts": peg.get("context_ts"),
        })
    except Exception:
        fields.update({"stablecoin_guard_state": "UNKNOWN", "stablecoin_guard_action": None})

    if not latency_critical:
        try:
            from src.risk.position_advisor import position_leverage_advice
            entry = (signal.get("entry_used") or signal.get("suggested_entry")
                     or signal.get("entry_trigger") or signal.get("entry_low"))
            stop = signal.get("stop_loss") or signal.get("invalidation")
            adv = position_leverage_advice(entry=entry, stop=stop, mode=signal.get("mode"),
                                           tier=signal.get("tier"))
            for k in ("position_advisor_status", "stop_distance_pct", "suggested_notional",
                      "max_safe_leverage_estimate", "leverage_warning",
                      "suggested_margin_at_1x", "suggested_margin_at_2x",
                      "suggested_margin_at_3x", "suggested_margin_at_5x",
                      "capital_efficiency_note"):
                fields[k] = adv.get(k)
        except Exception:
            pass

    fields["diagnostic_only"] = True
    return fields


def risk_guard_warning_lines(fields: dict[str, Any]) -> list[str]:
    """Compact operator-facing warning lines (Telegram/report). Only the
    actionable diagnostics — empty when nothing is noteworthy."""
    lines: list[str] = []
    cb = circuit_breaker_warning_line(fields)
    if cb:
        lines.append(cb)
    if fields.get("btc_intraday_risk_off"):
        lines.append(
            f"⚠ Risk-off context: {fields.get('risk_off_diagnostic', 'BTC down')}"
            " — long bias, diagnostic only")
    if fields.get("next_day_revalidation_required"):
        lines.append(
            f"⚠ Carryover/revalidation: {fields.get('lifecycle_label')}"
            f" (held {fields.get('held_hours')}h) — review next session, not auto-closed")
    if fields.get("would_bind_sector_cap") in (
            "shadow_sector_cap", "half_size", "shadow_proxy_duplicate"):
        lines.append(
            f"⚠ Sector cap would bind: {fields.get('would_bind_sector_cap')}"
            f" rank {fields.get('would_sector_rank')} ({fields.get('would_sector_bucket')})"
            " — shadow diagnostic, live size unchanged")
    if fields.get("catalyst_integrity_status") == "catalyst_backed_confirmed":
        lines.append("ℹ Catalyst-backed (direct news_items hit confirmed)")
    if fields.get("stablecoin_guard_state") in ("WATCH", "STRESS", "CRISIS"):
        dev = fields.get("stablecoin_guard_deviation_pct")
        suffix = f" ({float(dev):.2f}%)" if dev is not None else ""
        lines.append(
            f"Stablecoin guard: {fields.get('stablecoin_guard_asset') or '?'} "
            f"{fields.get('stablecoin_guard_state')}{suffix}")
    if fields.get("position_advisor_status") in ("ok", "warning", "unsafe") and \
            fields.get("suggested_notional") is not None:
        sd = fields.get("stop_distance_pct")
        lev = fields.get("max_safe_leverage_estimate")
        ln = (f"ℹ Position advisor: stop {sd:.2f}%, risk 0.5% → notional "
              f"~${fields['suggested_notional']:,.0f}, max safe {lev:g}x — diagnostic only")
        if fields.get("leverage_warning"):
            ln += f" · {fields['leverage_warning']}"
        lines.append(ln)
    return lines
