"""Playbook labeling — single source of truth.

Annotation-only. Given a signal-shaped dict (or a `TradeIdea`-shaped dict),
returns a `PlaybookLabel` carrying the named playbook, status, overlay
labels, "why this playbook" line, known failure mode, and manual-review
hint. Used by:

- crypto report builder (`src/reports/markdown_templates.py`)
- stocks report builder (`src/stocks/reports/stocks_report_builder.py`)
- Obsidian dashboard (`scripts/write_obsidian_current_state_dashboard.py`)
- LLM packets (`src/analysis/packet.py`)

No code path here changes scoring, thresholds, TP/SL, or signal generation.
See reports/STRATEGY_PLAYBOOK_AUDIT.md for the strategy descriptions and
reports/CURRENT_TRADING_PLAYBOOKS.md for the one-page summary.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


# Primary playbook labels (per-mode + cross-mode strategy lenses).
# Cross-mode lenses are emitted as overlays, not as the primary label.
PLAYBOOK_CRYPTO_SCALP = "crypto_scalp_momentum_continuation"
PLAYBOOK_CRYPTO_INTRADAY = "crypto_intraday_catalyst_or_momentum"
PLAYBOOK_CRYPTO_SWING = "crypto_swing_narrative_rs_momentum"
PLAYBOOK_CRYPTO_FAILED_BOUNCE_SHORT = "crypto_failed_bounce_short"
PLAYBOOK_CRYPTO_CATALYST_BACKED = "crypto_catalyst_backed_setup"
PLAYBOOK_CRYPTO_RS_LEADER = "crypto_rs_leader_long"

PLAYBOOK_STOCKS_INTRADAY = "stocks_intraday_rth_momentum"
PLAYBOOK_STOCKS_SWING_EVENT_RS_PULLBACK = "stocks_swing_event_rs_pullback"
PLAYBOOK_STOCKS_SWING_WATCH = "stocks_swing_watchlist_rs_rotation"
PLAYBOOK_STOCKS_INVEST_WATCH = "stocks_invest_watchlist_30d_thesis"
STOCKS_SWING_EVENT_RS_PROFILES = {
    "stocks_swing_event_rs_pullback_quality_paper_v1",
    "stocks_swing_event_rs_pullback_flow_paper_v1",
}

# Overlay labels (any subset can attach to a primary).
OVERLAY_CATALYST_BACKED = "catalyst_backed"
OVERLAY_RS_LEADER = "rs_leader"
OVERLAY_SHORT_PLAYBOOK = "short_playbook"
OVERLAY_LOW_CONFIDENCE_SCALP = "low_confidence_scalp"
OVERLAY_WATCHLIST_ONLY_MODE = "watchlist_only_mode"

# Statuses.
STATUS_ACTIONABLE = "actionable"
STATUS_LOW_CONFIDENCE = "low_confidence"
STATUS_WATCHLIST_ONLY = "watchlist_only"


@dataclass(frozen=True)
class PlaybookLabel:
    playbook: str
    status: str
    overlays: tuple[str, ...] = ()
    why: str = ""
    failure_mode: str = ""
    manual_review_hint: str = ""

    def overlay_str(self) -> str:
        return ", ".join(self.overlays) if self.overlays else "—"

    def to_dict(self) -> dict[str, Any]:
        return {
            "playbook": self.playbook,
            "status": self.status,
            "overlays": list(self.overlays),
            "why": self.why,
            "failure_mode": self.failure_mode,
            "manual_review_hint": self.manual_review_hint,
        }

    def to_markdown_block(self, *, heading_level: int = 4) -> str:
        """Compact markdown block suitable for embedding in idea cards."""
        # Section header uses ###/#### — caller picks the level.
        hashes = "#" * max(1, min(heading_level, 6))
        ovl = self.overlay_str()
        lines = [
            f"{hashes} Playbook",
            f"- Playbook: `{self.playbook}`",
            f"- Status: **{self.status}**",
            f"- Overlays: {ovl}",
        ]
        if self.why:
            lines.append(f"- Why this playbook: {self.why}")
        if self.failure_mode:
            lines.append(f"- Known failure mode: {self.failure_mode}")
        if self.manual_review_hint:
            lines.append(f"- Manual review hint: {self.manual_review_hint}")
        return "\n".join(lines)


def _bool(v: Any) -> bool:
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v != 0
    if isinstance(v, str):
        return v.lower() in {"1", "true", "yes", "y"}
    return False


def _raw_payload(signal: dict[str, Any]) -> dict[str, Any]:
    raw = signal.get("raw_idea_json") if isinstance(signal, dict) else None
    if isinstance(raw, dict):
        return dict(raw)
    try:
        parsed = json.loads(raw or "{}")
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def _paper_profile(signal: dict[str, Any]) -> str:
    direct = str(signal.get("paper_entry_profile") or "").strip()
    if direct:
        return direct
    return str(_raw_payload(signal).get("paper_entry_profile") or "").strip()


def _overlays(signal: dict[str, Any], asset_class: str, mode: str, direction: str,
              news: bool, tier: str, score: float) -> tuple[str, ...]:
    out: list[str] = []
    if news:
        out.append(OVERLAY_CATALYST_BACKED)
    if direction == "short":
        out.append(OVERLAY_SHORT_PLAYBOOK)
    # RS-leader proxy: score >= 80 on crypto intraday/swing AND not a watchlist tier.
    # Direct RS field is not always persisted on the signal row; the high score
    # captures the top-decile cohort the audit identified empirically.
    if asset_class == "crypto" and mode in {"intraday", "swing"} and direction == "long" and score >= 80:
        out.append(OVERLAY_RS_LEADER)
    if asset_class == "crypto" and mode == "scalp":
        out.append(OVERLAY_LOW_CONFIDENCE_SCALP)
    if (
        asset_class == "stocks"
        and mode in {"swing", "invest"}
        and _paper_profile(signal) not in STOCKS_SWING_EVENT_RS_PROFILES
    ):
        out.append(OVERLAY_WATCHLIST_ONLY_MODE)
    return tuple(out)


def label_for(signal: dict[str, Any]) -> PlaybookLabel:
    """Map a signal-shaped dict to a PlaybookLabel.

    Accepts both raw `proposed_signals` rows and TradeIdea-style dicts (the
    field names overlap on `mode`, `asset_class`, `direction`, `news_supported`,
    `tier`, `score`). Never raises — missing fields fall through to safe
    defaults.
    """
    asset = (signal.get("asset_class") or "crypto").lower()
    mode = (signal.get("mode") or "intraday").lower()
    direction = (signal.get("direction") or "long").lower()
    news = _bool(signal.get("news_supported"))
    tier = (signal.get("tier") or "C").upper()
    try:
        score = float(signal.get("score") or 0)
    except Exception:
        score = 0.0

    overlays = _overlays(signal, asset, mode, direction, news, tier, score)

    # Stocks branches ----------------------------------------------------
    if asset == "stocks":
        if mode == "intraday":
            why = "stocks intraday B-tier 14d: WR 55%, PF 2.03, +80R; shorts subset PF 9.00"
            fail = ("A-tier overpromotion on losing names — NVDA/SMCI/SMH longs "
                    "structurally lose in this regime")
            hint = "Spot-check chart structure against thesis; avoid NVDA/SMCI longs without strong catalyst."
            return PlaybookLabel(
                playbook=PLAYBOOK_STOCKS_INTRADAY,
                status=STATUS_ACTIONABLE,
                overlays=overlays,
                why=why, failure_mode=fail, manual_review_hint=hint,
            )
        if mode == "swing":
            if _paper_profile(signal) in STOCKS_SWING_EVENT_RS_PROFILES:
                why = ("stock swing event/RS pullback Paper lane: impulse + relative strength "
                       "+ daily pullback/reclaim; news can boost or block, but is not mandatory")
                fail = "late-cycle momentum failure or broad-market risk-off invalidates daily pullbacks"
                hint = "Paper-only: compare quality vs flow sleeve before any live decision."
                return PlaybookLabel(
                    playbook=PLAYBOOK_STOCKS_SWING_EVENT_RS_PULLBACK,
                    status=STATUS_ACTIONABLE,
                    overlays=overlays,
                    why=why, failure_mode=fail, manual_review_hint=hint,
                )
            why = ("stocks swing paused after 48h audit: WR 11% / PF 0.15 / −33R "
                   "pre-pause; demoted to C")
            fail = ("A-tier-long bias in chop/top; stops fire 1–6 d while thesis "
                    "needs 7+ d")
            hint = "Use for research only; do not act until 20+ post-pause C closures accumulate."
            return PlaybookLabel(
                playbook=PLAYBOOK_STOCKS_SWING_WATCH,
                status=STATUS_WATCHLIST_ONLY,
                overlays=overlays,
                why=why, failure_mode=fail, manual_review_hint=hint,
            )
        if mode == "invest":
            why = ("stocks invest paused after mode-viability audit: WR 0% / "
                   "0W/24L / −24R")
            fail = "Stop-to-horizon mismatch — invalidates in 1–6 d vs 30 d thesis"
            hint = "Watchlist only; same pipeline failure mode as paused swing."
            return PlaybookLabel(
                playbook=PLAYBOOK_STOCKS_INVEST_WATCH,
                status=STATUS_WATCHLIST_ONLY,
                overlays=overlays,
                why=why, failure_mode=fail, manual_review_hint=hint,
            )

    # Crypto branches ----------------------------------------------------
    if mode == "scalp":
        why = ("entry edge real (100% of expired scalps had positive MFE, avg "
               "+0.54R); TP1/2h horizon mismatch caps capture")
        fail = "TP1 distance ~1.86R vs typical captured MFE 0.54R — mean reverts before TP"
        hint = "Treat with lower confidence; consider taking partial off the table early."
        return PlaybookLabel(
            playbook=PLAYBOOK_CRYPTO_SCALP,
            status=STATUS_LOW_CONFIDENCE,
            overlays=overlays,
            why=why, failure_mode=fail, manual_review_hint=hint,
        )
    if mode == "intraday":
        if direction == "short":
            why = ("crypto failed-bounce short — 14d crypto shorts WR 40% / PF "
                   "2.00 / +9R")
            fail = "Squeeze risk under extreme-negative funding; catalyst pop against position"
            hint = "Avoid extreme-negative funding setups; check OI/funding context."
            return PlaybookLabel(
                playbook=PLAYBOOK_CRYPTO_FAILED_BOUNCE_SHORT,
                status=STATUS_ACTIONABLE,
                overlays=overlays,
                why=why, failure_mode=fail, manual_review_hint=hint,
            )
        if news:
            why = ("catalyst-backed crypto intraday: 14d WR 50% / PF 2.75 / +7R "
                   "— catalyst is the discriminator")
            fail = "Sell-the-news on already-priced catalysts; chase risk if catalyst already moved price"
            hint = "Confirm catalyst is fresh and price hasn't already absorbed it."
            return PlaybookLabel(
                playbook=PLAYBOOK_CRYPTO_INTRADAY,
                status=STATUS_ACTIONABLE,
                overlays=overlays,
                why=why, failure_mode=fail, manual_review_hint=hint,
            )
        why = ("crypto intraday momentum (no catalyst) — 14d no-news cut: WR "
               "23% / PF 0.70 / −3R")
        fail = "No-catalyst intraday in chop is net-negative — needs RS-leader or breakout confirmation"
        hint = "Without catalyst, prefer RS-leader long or wait for breakout confirmation."
        return PlaybookLabel(
            playbook=PLAYBOOK_CRYPTO_INTRADAY,
            status=STATUS_ACTIONABLE,
            overlays=overlays,
            why=why, failure_mode=fail, manual_review_hint=hint,
        )
    if mode == "swing":
        if direction == "short":
            why = "crypto failed-bounce swing short — same playbook as intraday shorts on a 7d horizon"
            fail = "Squeeze risk + BTC range tops invalidating swing shorts"
            hint = "Confirm bearish HTF structure; avoid against active narrative basket."
            return PlaybookLabel(
                playbook=PLAYBOOK_CRYPTO_FAILED_BOUNCE_SHORT,
                status=STATUS_ACTIONABLE,
                overlays=overlays,
                why=why, failure_mode=fail, manual_review_hint=hint,
            )
        why = ("crypto swing — primary playbook. 14d WR 72% / PF 5.80 / +24R; "
               "RS-leader + narrative basket confirmations")
        fail = "Chase risk after a vertical 24h move; BTC dump invalidating correlated swing longs"
        hint = ("Strongest mode — confirm RS leadership and not already extended. "
                "Catalyst-backed is the cleanest sub-cohort.")
        return PlaybookLabel(
            playbook=PLAYBOOK_CRYPTO_SWING,
            status=STATUS_ACTIONABLE,
            overlays=overlays,
            why=why, failure_mode=fail, manual_review_hint=hint,
        )
    if mode == "invest":
        # Crypto "invest" reuses the swing playbook (rare). Mark accordingly.
        return PlaybookLabel(
            playbook=PLAYBOOK_CRYPTO_SWING,
            status=STATUS_ACTIONABLE,
            overlays=overlays,
            why="crypto invest treated as long-horizon swing (rare path)",
            failure_mode="same as swing — chase risk / BTC dump",
            manual_review_hint="Use swing-mode discipline.",
        )

    # Safety fallback ----------------------------------------------------
    return PlaybookLabel(
        playbook="unknown",
        status=STATUS_ACTIONABLE,
        overlays=overlays,
        why="signal does not match a known mode/asset combo",
        failure_mode="—",
        manual_review_hint="Manual review required.",
    )


def label_from_trade_idea(idea: Any) -> PlaybookLabel:
    """Convenience: pull fields from a `TradeIdea` and route through label_for."""
    raw = getattr(idea, "raw", None) or {}
    # news_count + news flag come from raw idea payload
    news_count = raw.get("news_count") or raw.get("news") or 0
    return label_for({
        "asset_class": getattr(idea, "asset_class", "crypto"),
        "mode": getattr(idea, "mode", "intraday"),
        "direction": getattr(idea, "direction", "long"),
        "tier": getattr(idea, "tier", "C"),
        "score": getattr(idea, "score", 0),
        "news_supported": bool(news_count),
        "paper_entry_profile": raw.get("paper_entry_profile"),
        "raw_idea_json": json.dumps(raw, default=str),
    })
