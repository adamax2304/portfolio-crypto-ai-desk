"""Weekend Mode overlay.

Automatically activates on Saturdays and Sundays (per config/weekend_mode.yaml
+ project timezone). When active, applies a small risk/scoring overlay that:
  - subtracts `a_tier_score_penalty` from scores >= 80,
  - re-evaluates tier per existing thresholds,
  - caps weak signals at B,
  - caps weak MEXC-only signals at C,
  - appends weekend-specific cap_reasons + warnings to ScoreBreakdown,
  - returns a per-symbol adjustment summary the report / packet can render.

Strict invariants:
  - Pure overlay: never raises score, never changes direction.
  - Safe by default: if config is missing or any error occurs, returns no-op.
  - Mutates ScoreBreakdown in place (Pydantic models are mutable).
  - Does not touch news_trader/ or any external store.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

try:  # Python 3.9+ stdlib.
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
except ImportError:  # pragma: no cover - py < 3.9 unsupported but keep import safe.
    ZoneInfo = None  # type: ignore[assignment]
    ZoneInfoNotFoundError = Exception  # type: ignore[assignment,misc]


DAY_NAMES = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


# ---------- Config ---------------------------------------------------------


@dataclass
class WeekendConfig:
    enabled: bool = True
    timezone: str = "project_default"
    active_days: tuple[str, ...] = ("Saturday", "Sunday")
    confidence_penalty: float = 0.10
    a_tier_score_penalty: float = 5.0
    overextension_penalty_multiplier: float = 1.25
    max_tier_for_weak_signals: str = "B"
    max_tier_for_weak_mexc_only_signals: str = "C"
    require_retest_after_impulse: bool = True
    tight_stop_warning: bool = True
    prefer_structure_or_atr_stops: bool = True
    downgrade_chasing_entries: bool = True
    mode_overrides: dict[str, dict[str, Any]] = field(default_factory=dict)
    banner: str = (
        "WEEKEND MODE ACTIVE: weekend liquidity is thinner. Demand cleaner "
        "structure, prefer retests, expect wider wicks. A-tier requires real margin."
    )

    def for_mode(self, mode: str) -> "WeekendConfig":
        """Return a copy with mode-specific overrides applied."""
        override = self.mode_overrides.get(mode) or {}
        if not override:
            return self
        merged = WeekendConfig(
            enabled=self.enabled,
            timezone=self.timezone,
            active_days=self.active_days,
            confidence_penalty=float(override.get("confidence_penalty", self.confidence_penalty)),
            a_tier_score_penalty=float(
                override.get("a_tier_score_penalty", self.a_tier_score_penalty)
            ),
            overextension_penalty_multiplier=float(
                override.get(
                    "overextension_penalty_multiplier", self.overextension_penalty_multiplier
                )
            ),
            max_tier_for_weak_signals=str(
                override.get("max_tier_for_weak_signals", self.max_tier_for_weak_signals)
            ),
            max_tier_for_weak_mexc_only_signals=str(
                override.get(
                    "max_tier_for_weak_mexc_only_signals",
                    self.max_tier_for_weak_mexc_only_signals,
                )
            ),
            require_retest_after_impulse=bool(
                override.get("require_retest_after_impulse", self.require_retest_after_impulse)
            ),
            tight_stop_warning=bool(
                override.get("tight_stop_warning", self.tight_stop_warning)
            ),
            prefer_structure_or_atr_stops=bool(
                override.get(
                    "prefer_structure_or_atr_stops", self.prefer_structure_or_atr_stops
                )
            ),
            downgrade_chasing_entries=bool(
                override.get("downgrade_chasing_entries", self.downgrade_chasing_entries)
            ),
            mode_overrides=self.mode_overrides,
            banner=self.banner,
        )
        merged._extra_warnings = list(override.get("extra_warnings", []))  # type: ignore[attr-defined]
        return merged

    def extra_warnings(self) -> list[str]:
        return getattr(self, "_extra_warnings", [])


def load_config(project_root: Path) -> WeekendConfig:
    """Load config/weekend_mode.yaml. Safe-defaults if missing or malformed."""
    path = project_root / "config" / "weekend_mode.yaml"
    if not path.exists():
        return WeekendConfig(enabled=False)
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    except Exception:
        return WeekendConfig(enabled=False)
    return WeekendConfig(
        enabled=bool(data.get("enabled", True)),
        timezone=str(data.get("timezone", "project_default")),
        active_days=tuple(data.get("active_days") or ("Saturday", "Sunday")),
        confidence_penalty=float(data.get("confidence_penalty", 0.10)),
        a_tier_score_penalty=float(data.get("a_tier_score_penalty", 5.0)),
        overextension_penalty_multiplier=float(
            data.get("overextension_penalty_multiplier", 1.25)
        ),
        max_tier_for_weak_signals=str(data.get("max_tier_for_weak_signals", "B")),
        max_tier_for_weak_mexc_only_signals=str(
            data.get("max_tier_for_weak_mexc_only_signals", "C")
        ),
        require_retest_after_impulse=bool(data.get("require_retest_after_impulse", True)),
        tight_stop_warning=bool(data.get("tight_stop_warning", True)),
        prefer_structure_or_atr_stops=bool(data.get("prefer_structure_or_atr_stops", True)),
        downgrade_chasing_entries=bool(data.get("downgrade_chasing_entries", True)),
        mode_overrides=dict(data.get("mode_overrides") or {}),
        banner=str(
            data.get(
                "banner",
                "WEEKEND MODE ACTIVE: weekend liquidity is thinner. Demand cleaner "
                "structure, prefer retests, expect wider wicks. A-tier requires real margin.",
            )
        ),
    )


# ---------- Status detection ----------------------------------------------


@dataclass
class WeekendStatus:
    enabled: bool
    active: bool
    day_name: str
    now_local: datetime
    timezone_name: str
    active_days: tuple[str, ...]
    config: WeekendConfig

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "active": self.active,
            "day_name": self.day_name,
            "now_local": self.now_local.isoformat(timespec="seconds"),
            "timezone": self.timezone_name,
            "active_days": list(self.active_days),
        }


def _resolve_timezone(config: WeekendConfig, settings: dict[str, Any]) -> tuple[Any, str]:
    """Pick the timezone object based on config + settings.yaml."""
    candidate = config.timezone
    if candidate == "project_default":
        project = settings.get("project") or {}
        candidate = str(project.get("timezone") or "UTC")
    if ZoneInfo is None:
        return timezone.utc, "UTC"
    try:
        return ZoneInfo(candidate), candidate
    except (ZoneInfoNotFoundError, Exception):
        return timezone.utc, "UTC"


def current_status(
    config: WeekendConfig | None,
    settings: dict[str, Any],
    now: datetime | None = None,
) -> WeekendStatus:
    """Return live status. If now is None, uses real time in configured tz."""
    config = config or WeekendConfig(enabled=False)
    tz, tz_name = _resolve_timezone(config, settings)
    if now is None:
        now_local = datetime.now(tz)
    else:
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)
        now_local = now.astimezone(tz)
    day_name = DAY_NAMES[now_local.weekday()]
    active_days = tuple(config.active_days)
    active = bool(config.enabled) and day_name in active_days
    return WeekendStatus(
        enabled=bool(config.enabled),
        active=active,
        day_name=day_name,
        now_local=now_local,
        timezone_name=tz_name,
        active_days=active_days,
        config=config,
    )


# ---------- Overlay --------------------------------------------------------


TIER_RANK = {"rejected": 0, "C": 1, "B": 2, "A": 3}
RANK_TIER = {0: "rejected", 1: "C", 2: "B", 3: "A"}


def _cap_tier(current: str, ceiling: str) -> str:
    """Return min(current, ceiling) by TIER_RANK."""
    cur = TIER_RANK.get(current, 0)
    cap = TIER_RANK.get(ceiling, 0)
    return current if cur <= cap else RANK_TIER[cap]


def _is_weak_signal(score: Any) -> bool:
    """Heuristic: signal lacks data confidence or has heavy risk."""
    try:
        if getattr(score, "data_quality", "") == "acceptable":
            return True
        if float(getattr(score, "risk_penalty", 0)) >= 12:
            return True
        tech = (score.components or {}).get("technical_setup", 0)
        if float(tech) < 12:
            return True
    except Exception:
        return False
    return False


def _is_mexc_only_capped(score: Any) -> bool:
    for reason in getattr(score, "cap_reasons", []) or []:
        if "mexc-only" in str(reason).lower():
            return True
    return False


def _is_overextended(setup: Any, candidate: Any | None = None) -> bool:
    """True when candidate/setup looks chasey (extension > 2 ATR)."""
    try:
        if candidate is not None and getattr(candidate, "distance_from_ema20_atr", None) is not None:
            return abs(float(candidate.distance_from_ema20_atr)) > 2.0
    except Exception:
        pass
    warnings = getattr(setup, "warnings", []) or []
    return any("extend" in str(w).lower() or "chase" in str(w).lower() for w in warnings)


@dataclass
class AdjustmentRecord:
    symbol: str
    original_score: float
    new_score: float
    original_tier: str
    new_tier: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbol": self.symbol,
            "original_score": round(self.original_score, 1),
            "new_score": round(self.new_score, 1),
            "original_tier": self.original_tier,
            "new_tier": self.new_tier,
            "notes": list(self.notes),
            "downgraded": self.new_tier != self.original_tier,
        }


def apply_overlay(
    scores: dict[str, Any],
    setups: list[Any] | None,
    status: WeekendStatus,
    mode: str = "intraday",
    candidates: list[Any] | None = None,
) -> dict[str, AdjustmentRecord]:
    """Apply weekend overlay to ScoreBreakdown objects in place.

    Returns: per-symbol adjustment record (for report / packet rendering).
    No-op if status.active is False.
    """
    if not status.active:
        return {}

    config = status.config.for_mode(mode)
    setups_by_symbol = {s.symbol: s for s in (setups or []) if getattr(s, "symbol", None)}
    candidates_by_symbol = {
        c.symbol: c for c in (candidates or []) if getattr(c, "symbol", None)
    }
    records: dict[str, AdjustmentRecord] = {}

    a_tier_threshold = 80.0
    b_tier_threshold = 65.0
    c_tier_threshold = 50.0

    for symbol, score in scores.items():
        if score is None:
            continue
        try:
            original_score = float(score.final_score)
            original_tier = str(score.tier)
        except Exception:
            continue

        notes: list[str] = []
        new_score = original_score
        cap_reasons = list(getattr(score, "cap_reasons", []) or [])
        warnings = list(getattr(score, "warnings", []) or [])
        reasons = list(getattr(score, "reasons", []) or [])

        # 1. A-tier margin penalty.
        if new_score >= a_tier_threshold and config.a_tier_score_penalty > 0:
            new_score = max(new_score - config.a_tier_score_penalty, 0.0)
            notes.append(
                f"weekend: -{config.a_tier_score_penalty:.0f} a-tier margin penalty"
            )

        # 2. Overextension multiplier (only if setup/candidate shows extension).
        setup = setups_by_symbol.get(symbol)
        candidate = candidates_by_symbol.get(symbol)
        if setup is not None and _is_overextended(setup, candidate):
            extra = round(8 * (config.overextension_penalty_multiplier - 1.0), 1)
            if extra > 0:
                new_score = max(new_score - extra, 0.0)
                notes.append(
                    f"weekend: -{extra} extra overextension penalty (x{config.overextension_penalty_multiplier:.2f})"
                )

        # 3. Decide tier from updated score using existing thresholds.
        invalidation_missing = any(
            "invalidation" in str(r).lower() for r in cap_reasons
        )
        stale_cap = any("stale" in str(r).lower() for r in cap_reasons)
        direction = getattr(setup, "direction", "no_trade") if setup is not None else "no_trade"

        if invalidation_missing or stale_cap:
            new_tier = "rejected"
        elif direction in {"long", "short"} and new_score >= a_tier_threshold and not cap_reasons:
            new_tier = "A"
        elif direction in {"long", "short"} and new_score >= b_tier_threshold:
            new_tier = "B"
        elif new_score >= c_tier_threshold:
            new_tier = "C"
        else:
            new_tier = "rejected"

        # 4. Weak signal cap.
        if _is_weak_signal(score):
            ceiling = config.max_tier_for_weak_signals
            capped = _cap_tier(new_tier, ceiling)
            if capped != new_tier:
                notes.append(f"weekend: weak signal capped at {ceiling}-tier")
                new_tier = capped
            else:
                notes.append(f"weekend: weak signal flagged (would cap at {ceiling}-tier)")

        # 5. Weak + MEXC-only cap (tighter).
        if _is_weak_signal(score) and _is_mexc_only_capped(score):
            ceiling = config.max_tier_for_weak_mexc_only_signals
            capped = _cap_tier(new_tier, ceiling)
            if capped != new_tier:
                notes.append(
                    f"weekend: weak MEXC-only capped at {ceiling}-tier (watchlist)"
                )
                new_tier = capped

        # 6. Chasing demotion (extension + downgrade flag).
        if (
            config.downgrade_chasing_entries
            and setup is not None
            and _is_overextended(setup, candidate)
            and new_tier in {"A", "B"}
        ):
            notes.append("weekend: chasing entry — downgraded to C (wait for pullback)")
            new_tier = "C"

        # 7. Tight stop + structure / retest warnings (informational).
        if config.tight_stop_warning:
            atr = getattr(setup, "atr", None) if setup is not None else None
            inval = getattr(setup, "invalidation", None) if setup is not None else None
            if atr and inval and setup is not None:
                close = getattr(setup, "current_price", None)
                try:
                    if close and abs(float(close) - float(inval)) < 0.8 * float(atr):
                        warnings.append(
                            "Weekend Mode: stop is less than 0.8 ATR from price; weekend wicks can hit it easily."
                        )
                        notes.append("weekend: tight stop warning")
                except Exception:
                    pass

        if config.require_retest_after_impulse and candidate is not None:
            try:
                ret24 = candidate.return_24h
                if ret24 is not None and abs(float(ret24)) >= 6:
                    warnings.append(
                        "Weekend Mode: large 24h move detected — demand retest acceptance before entry."
                    )
                    notes.append("weekend: retest after impulse required")
            except Exception:
                pass

        if config.prefer_structure_or_atr_stops and setup is not None:
            warnings.append(
                "Weekend Mode: prefer structural invalidation (recent S/R ± 0.15 ATR) over a fixed ATR stop."
            )

        # 8. Banner + mode-specific extra warnings.
        for line in config.extra_warnings():
            warnings.append(f"Weekend Mode ({mode}): {line}")

        # 9. Confidence shift.
        if config.confidence_penalty > 0:
            new_confidence = _confidence_after_penalty(
                score.confidence, config.confidence_penalty
            )
            if new_confidence != score.confidence:
                notes.append(
                    f"weekend: confidence {score.confidence} -> {new_confidence}"
                )
                try:
                    score.confidence = new_confidence
                except Exception:
                    pass

        # 10. Persist mutations.
        new_score = round(new_score, 1)
        if new_score != original_score or new_tier != original_tier or notes:
            cap_reasons.extend(
                f"weekend: {n}" for n in notes if "capped at" in n or "downgraded to C" in n
            )
            reasons.append(
                f"Weekend Mode applied: original score {original_score:.1f}/{original_tier} -> "
                f"{new_score:.1f}/{new_tier}. Notes: " + "; ".join(notes)
            )
            try:
                score.final_score = new_score
                score.tier = new_tier  # type: ignore[assignment]
                score.cap_reasons = cap_reasons
                score.reasons = reasons
                score.warnings = list(dict.fromkeys(warnings))
            except Exception:
                pass

        records[symbol] = AdjustmentRecord(
            symbol=symbol,
            original_score=original_score,
            new_score=new_score,
            original_tier=original_tier,
            new_tier=new_tier,
            notes=notes,
        )

    return records


def _confidence_after_penalty(label: str, penalty: float) -> str:
    """Step the confidence label down by one band if penalty >= 0.05, by two if >= 0.25."""
    if not label or penalty < 0.05:
        return label
    ladder = ["low", "medium", "medium-high", "high"]
    label_lower = str(label).lower()
    if label_lower not in ladder:
        return label
    idx = ladder.index(label_lower)
    drop = 2 if penalty >= 0.25 else 1
    return ladder[max(idx - drop, 0)]


# ---------- Reporting helpers ---------------------------------------------


def status_markdown(status: WeekendStatus, mode: str = "intraday") -> str:
    """Human-readable status block for reports / packets."""
    cfg = status.config.for_mode(mode)
    lines = [
        "## Weekend Mode Status",
        "",
        f"- Weekend Mode enabled: `{status.enabled}`",
        f"- Currently active: `{status.active}`",
        f"- Current project time: `{status.now_local.isoformat(timespec='seconds')}`",
        f"- Timezone: `{status.timezone_name}`",
        f"- Day: `{status.day_name}`",
        f"- Active days: `{', '.join(status.active_days)}`",
        f"- Mode: `{mode}`",
    ]
    if status.active:
        lines.extend(
            [
                "",
                f"**{cfg.banner}**",
                "",
                "**Active adjustments**:",
                f"- A-tier score penalty: `{cfg.a_tier_score_penalty}` (subtracted from scores >= 80)",
                f"- Confidence penalty: `{cfg.confidence_penalty}` (steps down by one band)",
                f"- Overextension penalty multiplier: `{cfg.overextension_penalty_multiplier}x`",
                f"- Weak signals capped at: `{cfg.max_tier_for_weak_signals}`",
                f"- Weak MEXC-only capped at: `{cfg.max_tier_for_weak_mexc_only_signals}`",
                f"- Require retest after impulse: `{cfg.require_retest_after_impulse}`",
                f"- Tight stop warning: `{cfg.tight_stop_warning}`",
                f"- Prefer structural / ATR stops: `{cfg.prefer_structure_or_atr_stops}`",
                f"- Downgrade chasing entries: `{cfg.downgrade_chasing_entries}`",
            ]
        )
        if cfg.extra_warnings():
            lines.append("")
            lines.append(f"**Mode-specific notes ({mode})**:")
            lines.extend(f"- {w}" for w in cfg.extra_warnings())
    else:
        lines.extend(
            [
                "",
                "_Weekend Mode is not active right now. No overlay applied._",
            ]
        )
    return "\n".join(lines)


__all__ = [
    "WeekendConfig",
    "WeekendStatus",
    "AdjustmentRecord",
    "load_config",
    "current_status",
    "apply_overlay",
    "status_markdown",
    "DAY_NAMES",
]
