"""Session Risk Guard — always-on, time-of-day trading guard.

Separate from the day-based Weekend Mode (src/analysis/weekend_mode.py). This
guard is HOUR-based and fires every day: inside the configured low-liquidity
UTC window ("Asia dead-zone", default 00–06 UTC) it demotes the configured
crypto modes (default scalp + intraday) out of the actionable A/B tiers, because
audit data shows those modes bleed there (intraday ~47% stop, scalp ~19% win)
while swing tolerates it. Monday — the worst weekday — supports a stricter
variant.

Strict invariants (same discipline as weekend_mode):
  - Pure overlay: never RAISES a tier, never changes direction, never touches
    TP/SL/entry or any live-execution lock.
  - Safe by default: missing/malformed config or any error -> no-op.
  - Deterministic on the passed `now` (UTC); callers pass the decision time.

The same `guard_decision()` is reused by:
  - production actionability (supervisor / registry) — demote tier, and
  - the paper-shadow `new_logic_shadow` branch — skip / de-risk the entry.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

# Reuse the tier ranking from the weekend overlay so both stay consistent.
from src.analysis.weekend_mode import RANK_TIER, TIER_RANK

DAY_NAMES = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
]


# ---------- Config ---------------------------------------------------------


@dataclass
class MondayStricter:
    enabled: bool = True
    extra_blocked_modes: tuple[str, ...] = ()
    allowed_mode_risk_multiplier: float = 0.5


@dataclass
class SessionGuardConfig:
    enabled: bool = False
    dz_enabled: bool = False
    utc_start_hour: int = 0
    utc_end_hour: int = 6  # window is [start, end) in UTC hours
    asset_classes: tuple[str, ...] = ("crypto",)
    blocked_modes: tuple[str, ...] = ("scalp", "intraday")
    demote_to_tier: str = "C"
    allowed_mode_risk_multiplier: float = 1.0
    monday: MondayStricter = field(default_factory=MondayStricter)
    # Hard mode kill-switch — ANY hour, ANY day (independent of the dead-zone window).
    # {asset_class: (mode, ...)}. Demoted to 'rejected' in prod (not registered, no
    # alert) and skipped in the new-logic shadow branch. e.g. {"crypto": ("scalp",)}.
    disabled_modes_enabled: bool = False
    disabled_modes: dict[str, tuple[str, ...]] = field(default_factory=dict)
    banner: str = (
        "SESSION GUARD (Asia dead-zone 00–06 UTC): scalp/intraday demoted to "
        "watchlist (low-liquidity window). Swing unaffected."
    )


def load_config(project_root: Path) -> SessionGuardConfig:
    """Load config/session_risk.yaml. Safe no-op defaults if missing/malformed."""
    path = Path(project_root) / "config" / "session_risk.yaml"
    if not path.exists():
        return SessionGuardConfig(enabled=False, dz_enabled=False)
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    except Exception:
        return SessionGuardConfig(enabled=False, dz_enabled=False)
    try:
        dz = data.get("asia_dead_zone") or {}
        mon_raw = dz.get("monday_stricter") or {}
        monday = MondayStricter(
            enabled=bool(mon_raw.get("enabled", True)),
            extra_blocked_modes=tuple(mon_raw.get("extra_blocked_modes") or ()),
            allowed_mode_risk_multiplier=float(
                mon_raw.get("allowed_mode_risk_multiplier", 0.5)
            ),
        )
        dm_raw = data.get("disabled_modes") or {}
        disabled_modes = {
            str(k).lower(): tuple(str(x).lower() for x in (v or []))
            for k, v in dm_raw.items()
            if k not in ("enabled",)
        }
        return SessionGuardConfig(
            enabled=bool(data.get("enabled", True)),
            dz_enabled=bool(dz.get("enabled", True)),
            utc_start_hour=int(dz.get("utc_start_hour", 0)),
            utc_end_hour=int(dz.get("utc_end_hour", 6)),
            asset_classes=tuple(dz.get("asset_classes") or ("crypto",)),
            blocked_modes=tuple(
                dz["blocked_modes"] if "blocked_modes" in dz else ("scalp", "intraday")
            ),
            demote_to_tier=str(dz.get("demote_to_tier", "C")),
            allowed_mode_risk_multiplier=float(
                dz.get("allowed_mode_risk_multiplier", 1.0)
            ),
            monday=monday,
            disabled_modes_enabled=bool(dm_raw.get("enabled", bool(disabled_modes))),
            disabled_modes=disabled_modes,
            banner=str(dz.get("banner", SessionGuardConfig.banner)),
        )
    except Exception:
        return SessionGuardConfig(enabled=False, dz_enabled=False)


# ---------- Decision -------------------------------------------------------


@dataclass
class GuardDecision:
    active: bool = False          # guard enabled AND time in window AND asset in scope
    in_window: bool = False       # time is inside the UTC window (regardless of mode)
    blocked: bool = False         # this mode is demoted out of actionable here
    demote_to_tier: str = "C"     # tier ceiling applied when blocked
    risk_multiplier: float = 1.0  # for still-allowed modes (e.g. swing)
    is_monday: bool = False
    kind: str = ""                # "" | "asia_dead_zone" | "mode_disabled"
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "active": self.active,
            "in_window": self.in_window,
            "blocked": self.blocked,
            "demote_to_tier": self.demote_to_tier,
            "risk_multiplier": round(self.risk_multiplier, 3),
            "is_monday": self.is_monday,
            "kind": self.kind,
            "reason": self.reason,
        }


def _in_window(hour: int, start: int, end: int) -> bool:
    """True if hour in [start, end) UTC. Supports wrap-around (e.g. 22..2)."""
    start %= 24
    end %= 24
    if start == end:
        return False
    if start < end:
        return start <= hour < end
    return hour >= start or hour < end  # wraps past midnight


def guard_decision(
    now_utc: datetime | None,
    mode: str,
    asset_class: str,
    cfg: SessionGuardConfig,
) -> GuardDecision:
    """Core decision. `now_utc` is the entry/decision time (any tz -> normalized
    to UTC; naive treated as UTC). Returns a no-op GuardDecision on any problem."""
    try:
        if cfg is None or not cfg.enabled:
            return GuardDecision()
        m = (mode or "").lower()
        asset = (asset_class or "").lower()
        u = None
        if now_utc is not None:
            if now_utc.tzinfo is None:
                now_utc = now_utc.replace(tzinfo=timezone.utc)
            u = now_utc.astimezone(timezone.utc)

        def _win(hh):
            return _in_window(hh, cfg.utc_start_hour, cfg.utc_end_hour)

        # (1) hard mode kill-switch — ANY hour, ANY day, independent of the window.
        if cfg.disabled_modes_enabled:
            killed = {x.lower() for x in (cfg.disabled_modes.get(asset) or ())}
            if m in killed:
                return GuardDecision(
                    active=True,
                    in_window=(_win(u.hour) if u else False),
                    blocked=True,
                    demote_to_tier="rejected",  # fully off, not just watchlist
                    risk_multiplier=0.0,
                    is_monday=(u.weekday() == 0 if u else False),
                    kind="mode_disabled",
                    reason=f"{asset}_{m}_disabled (kill-switch: mode off, any hour/day)",
                )

        # (2) Asia dead-zone window (needs a time; crypto-scoped by asset_classes).
        if not cfg.dz_enabled or u is None:
            return GuardDecision(in_window=(_win(u.hour) if u else False))
        if cfg.asset_classes and asset not in {a.lower() for a in cfg.asset_classes}:
            return GuardDecision(in_window=_win(u.hour))
        in_win = _win(u.hour)
        if not in_win:
            return GuardDecision(in_window=False)

        is_monday = u.weekday() == 0
        blocked_modes = {m.lower() for m in cfg.blocked_modes}
        risk_mult = cfg.allowed_mode_risk_multiplier
        if is_monday and cfg.monday.enabled:
            blocked_modes |= {m.lower() for m in cfg.monday.extra_blocked_modes}
            risk_mult = cfg.monday.allowed_mode_risk_multiplier

        blocked = m in blocked_modes
        window = f"{cfg.utc_start_hour:02d}-{cfg.utc_end_hour:02d} UTC"
        if blocked:
            reason = (
                f"asia_dead_zone_guard: {m} demoted to {cfg.demote_to_tier} "
                f"({window}{', Monday' if is_monday else ''}; low-liquidity window)"
            )
        else:
            reason = (
                f"asia_dead_zone_guard: {m} allowed, risk x{risk_mult:g} "
                f"({window}{', Monday' if is_monday else ''})"
            )
        return GuardDecision(
            active=True,
            in_window=True,
            blocked=blocked,
            demote_to_tier=cfg.demote_to_tier,
            risk_multiplier=risk_mult if not blocked else 0.0,
            is_monday=is_monday,
            kind="asia_dead_zone",
            reason=reason,
        )
    except Exception:
        return GuardDecision()


# ---------- Production overlay (tier cap) ----------------------------------


def _cap_tier(current: str, ceiling: str) -> str:
    cur = TIER_RANK.get(current, 0)
    cap = TIER_RANK.get(ceiling, 0)
    return current if cur <= cap else RANK_TIER[cap]


@dataclass
class GuardAdjustment:
    symbol: str
    original_tier: str
    new_tier: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbol": self.symbol,
            "original_tier": self.original_tier,
            "new_tier": self.new_tier,
            "demoted": self.new_tier != self.original_tier,
            "reason": self.reason,
        }


def apply_to_scores(
    scores: dict[str, Any],
    mode: str,
    asset_class: str,
    now_utc: datetime | None,
    cfg: SessionGuardConfig,
) -> dict[str, GuardAdjustment]:
    """Demote A/B -> `demote_to_tier` for a blocked (mode, time, asset) run.

    Mirrors weekend_mode.apply_overlay: mutates ScoreBreakdown.tier in place,
    appends a cap_reason. No-op unless the guard is active AND the mode is
    blocked. Never raises a tier.
    """
    decision = guard_decision(now_utc, mode, asset_class, cfg)
    if not decision.active or not decision.blocked:
        return {}
    records: dict[str, GuardAdjustment] = {}
    for symbol, score in (scores or {}).items():
        if score is None:
            continue
        try:
            original_tier = str(score.tier)
        except Exception:
            continue
        new_tier = _cap_tier(original_tier, decision.demote_to_tier)
        if new_tier != original_tier:
            try:
                cap_reasons = list(getattr(score, "cap_reasons", []) or [])
                cap_reasons.append(decision.reason)
                score.cap_reasons = cap_reasons
                reasons = list(getattr(score, "reasons", []) or [])
                reasons.append(
                    f"Session Guard: {original_tier} -> {new_tier}. {decision.reason}"
                )
                score.reasons = reasons
                score.tier = new_tier  # type: ignore[assignment]
            except Exception:
                pass
        records[symbol] = GuardAdjustment(
            symbol=symbol,
            original_tier=original_tier,
            new_tier=new_tier,
            reason=decision.reason,
        )
    return records


__all__ = [
    "SessionGuardConfig",
    "MondayStricter",
    "GuardDecision",
    "GuardAdjustment",
    "load_config",
    "guard_decision",
    "apply_to_scores",
    "DAY_NAMES",
]
