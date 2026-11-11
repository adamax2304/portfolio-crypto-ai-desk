"""Paper-entry Telegram alert builder + dispatcher.

Fires once when the tracker detects a true entry transition:
  prev status in {waiting_for_entry, not_triggered, pending, generated}
  AND outcome.entry_triggered=True
  AND no existing signal_alerts row with alert_type='paper_entry' for the signal_id.

Eligibility gates:
  * tier in {A, B}; C / watchlist / shadow are filtered out.
  * stocks swing/invest are filtered out (paused playbooks).
  * data_confidence != 'low' (informational; still send but flag).
  * playbook status != watchlist_only.

Operator Telegram is intentionally live-only: a Paper entry is pushed to the
phone only after the live handoff accepts it into the preflight queue. Paper-
only/rejected/shadow entries are still recorded for the dashboard and research.

This module is reporting / notification only. It does NOT:
  * change scoring, thresholds, TP/SL, signal generation, mode routing;
  * write to proposed_signals / signal_outcomes / watchlist_alerts;
  * place any order.

See PAPER_ENTRY_TELEGRAM_ALERTS_IMPLEMENTATION_REPORT.md for spec.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any

from src.signals.playbooks import label_for
from src.signals.sizing import size_decision
from src.notifiers.alert_headers import MAX_PAPER_ENTRY, cap as _cap
from src.stocks.entry_provenance import (
    PROVIDER_DELAYED_CURRENT_BAR,
    is_accepted_stock_intraday_paper_basis,
)


# Statuses that count as "pending" (eligible for transition into entry)
PENDING_STATUSES = {
    "waiting_for_entry", "not_triggered", "pending", "generated",
}

# Statuses that mean "entry actually happened" (post-transition)
ENTERED_STATUSES = {
    "triggered", "entered", "active", "entry_triggered",
    "tp1_hit", "tp2_hit", "tp3_hit", "stopped", "ambiguous",
}

PLAYBOOKS_FORBIDDEN_FOR_ENTRY_ALERT = {
    "stocks_swing_watchlist_rs_rotation",
    "stocks_invest_watchlist_30d_thesis",
}


@dataclass
class PaperEntryDecision:
    should_send: bool
    reason_skipped: str = ""
    message: str = ""
    risk_flags: list[str] | None = None
    rationale_bullets: list[str] | None = None
    size_weight: float = 1.0
    size_reason: str = ""
    playbook: str = ""
    payload: dict[str, Any] | None = None


def _eest_format(iso_ts: str | None) -> str:
    """Render ISO timestamp in EEST (UTC+3) for the operator."""
    if not iso_ts:
        return "—"
    try:
        if isinstance(iso_ts, datetime):
            dt = iso_ts
        else:
            dt = datetime.fromisoformat(str(iso_ts).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        eest = timezone(timedelta(hours=3))
        return dt.astimezone(eest).strftime("%Y-%m-%d %H:%M EEST")
    except Exception:
        return str(iso_ts)


def _fmt_price(value: Any) -> str:
    try:
        v = float(value)
    except (TypeError, ValueError):
        return "—"
    if abs(v) >= 100:
        return f"{v:.2f}"
    if abs(v) >= 1:
        return f"{v:.4f}"
    return f"{v:.6f}"


def _tradingview_link(asset_class: str, symbol: str, primary_exchange: str | None = None) -> str:
    if asset_class == "crypto":
        venue = (primary_exchange or "binance").upper()
        bare = symbol.replace("/", "").replace("-", "")
        return f"https://www.tradingview.com/chart/?symbol={venue}:{bare}"
    return f"https://www.tradingview.com/chart/?symbol={symbol}"


def _short_id(value: Any, n: int = 8) -> str:
    text = str(value or "").strip()
    return text[:n] if text else "—"


def _float_or_none(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _live_risk_usdt(payload: dict[str, Any]) -> float | None:
    for key in (
        "live_risk_usdt",
        "mexc_live_risk_usdt",
        "risk_usdt",
        "actual_risk_usdt",
        "planned_worst_case_risk_usdt",
    ):
        value = _float_or_none(payload.get(key))
        if value is not None and value > 0:
            return value
    multiplier = _float_or_none(payload.get("live_risk_multiplier"))
    if multiplier is None:
        multiplier = _display_size_weight(payload)
    if multiplier is not None and multiplier > 0:
        # Current live canary config uses fixed $10 full risk. This fallback is
        # presentation-only; the exchange preflight still owns authoritative risk.
        return 10.0 * min(1.0, multiplier)
    return None


def _display_size_weight(payload: dict[str, Any]) -> float | None:
    size_weight = _float_or_none(payload.get("size_weight"))
    effective = _float_or_none(payload.get("concentration_effective_weight"))
    if effective is not None and effective > 0 and (
        size_weight is None or effective < size_weight
    ):
        return effective
    return size_weight


def _stop_label_for_alert(signal: dict[str, Any], payload: dict[str, Any]) -> str | None:
    for candidate in (
        payload.get("stop_contract"),
        payload.get("initial_stop_contract"),
        signal.get("stop_contract"),
    ):
        if isinstance(candidate, dict) and candidate:
            label = candidate.get("label") or candidate.get("stop_label") or candidate.get("stop_source")
            return str(label).replace("_", " ") if label else None
    raw = signal.get("raw_idea_json")
    if raw:
        try:
            data = json.loads(raw) if isinstance(raw, str) else raw
            if isinstance(data, dict):
                candidate = data.get("initial_stop_contract") or data.get("stop_contract") or {}
                if isinstance(candidate, dict) and candidate:
                    label = candidate.get("label") or candidate.get("stop_source")
                    return str(label).replace("_", " ") if label else None
        except Exception:
            return None
    return None


def _compact_live_entry_message(
    signal: dict[str, Any],
    payload: dict[str, Any],
    *,
    fresh_line: str,
) -> str:
    asset = (signal.get("asset_class") or "crypto").lower()
    symbol = str(signal.get("symbol") or "?").replace("_", "/")
    direction = str(signal.get("direction") or "long").upper()
    side_emoji = "🟢" if direction == "LONG" else "🔴"
    score = _float_or_none(signal.get("score"))
    tier = str(signal.get("tier") or "?").upper()
    entry_mode = (
        payload.get("paper_execution_entry_mode")
        or signal.get("paper_execution_entry_mode")
        or payload.get("cqo_entry_mode")
        or "—"
    )
    profile = payload.get("paper_entry_profile") or signal.get("paper_entry_profile") or "—"
    decision_id = payload.get("mexc_canary_decision_id")
    risk = _live_risk_usdt(payload)
    size_weight = _display_size_weight(payload)
    size_suffix = f" · {size_weight:g}x" if size_weight is not None and size_weight > 0 else ""
    risk_line = (
        f"💵 Риск: ${risk:.2f}{size_suffix}"
        if risk is not None else f"💵 Риск: live preflight{size_suffix}"
    )
    stop_label = _stop_label_for_alert(signal, payload)
    lines = [
        f"{side_emoji} LIVE QUEUED",
        f"{symbol} {direction} · {asset.upper()}",
        "",
        f"🎯 Entry: {_fmt_price(payload.get('entry_used') or signal.get('entry_trigger'))}",
        f"🛡 SL: {_fmt_price(payload.get('stop') or signal.get('stop_loss') or signal.get('invalidation'))}",
        *(["🧭 Stop: " + stop_label] if stop_label else []),
        (
            "🏁 TP: "
            f"{_fmt_price(payload.get('tp1') or signal.get('tp1'))} / "
            f"{_fmt_price(payload.get('tp2') or signal.get('tp2'))} / "
            f"{_fmt_price(payload.get('tp3') or signal.get('tp3'))}"
        ),
        risk_line,
        f"⚙️ {entry_mode} · {profile}",
        f"⭐ {tier}" + (f" / {score:g}" if score is not None else ""),
        f"🆔 {_short_id(decision_id or signal.get('signal_id'))}",
        "",
        "⏳ Live preflight запущен. Fill придёт отдельным сообщением.",
    ]
    if payload.get("mexc_live_repriced"):
        lines.insert(
            4,
            "🔁 Reprice: "
            f"{_fmt_price(payload.get('mexc_live_reprice_reference_entry'))} → "
            f"{_fmt_price(payload.get('entry_used'))}",
        )
    if fresh_line:
        lines.append(f"🕒 {fresh_line.replace('Entry freshness: ', '')}")
    return _cap("\n".join(lines), 620)


def _compact_not_queued_message(
    signal: dict[str, Any],
    capture_status: str,
    capture_reasons: list[str],
) -> str:
    reason = ", ".join(capture_reasons[:3]) or capture_status or "not live eligible"
    symbol = str(signal.get("symbol") or "?").replace("_", "/")
    direction = str(signal.get("direction") or "long").upper()
    return _cap(
        "\n".join([
            "⚪ PAPER ONLY",
            f"{symbol} {direction}",
            f"Live: not queued ({reason})",
            "Logged to dashboard only.",
        ]),
        260,
    )


def _extract_rationale(signal: dict[str, Any]) -> list[str]:
    """Pull up to 2 short reasons from existing signal data.

    Never hallucinates: only echoes evidence already present in the row or
    raw_idea_json. If empty, returns a generic fallback line.
    """
    bullets: list[str] = []
    pl = label_for(signal)

    # 1. Playbook + tier line (always available)
    tier = (signal.get("tier") or "").upper()
    direction = (signal.get("direction") or "long").lower()
    if pl.playbook:
        bullets.append(f"{pl.playbook} ({tier}-tier {direction})")

    # 2. Catalyst / news support
    if int(signal.get("news_supported") or 0) == 1:
        bullets.append("catalyst/news support confirmed at proposal time")
    # 3. Regime line
    regime = (signal.get("market_regime") or "").strip()
    if regime:
        bullets.append(f"market regime: {regime}")
    # 4. Derivatives / OI
    oi = (signal.get("oi_context") or "").strip()
    if oi and "deleveraging" in oi.lower() and direction == "long":
        bullets.append("OI deleveraging supports long bounce")
    elif oi and "build" in oi.lower():
        bullets.append(f"OI context: {oi}")
    # 5. Raw idea thesis (very short)
    thesis = (signal.get("thesis") or "").strip()
    if thesis:
        first = thesis.split(".")[0].strip()
        if first and len(first) > 12:
            bullets.append(first[:140])
    # 6. raw_idea_json evidence list, if present and structured
    raw = signal.get("raw_idea_json")
    if raw:
        try:
            d = json.loads(raw) if isinstance(raw, str) else raw
            evidence = d.get("evidence") or d.get("setup_evidence") or []
            if isinstance(evidence, list) and evidence:
                for e in evidence[:2]:
                    text = str(e).strip()
                    if text and text not in bullets:
                        bullets.append(text[:140])
        except Exception:
            pass

    if not bullets:
        return ["reason: technical setup triggered; detailed evidence unavailable."]
    # cap to 4
    return bullets[:4]


def _risk_flags(signal: dict[str, Any]) -> list[str]:
    flags: list[str] = []
    pl = label_for(signal)
    tier = (signal.get("tier") or "").upper()
    direction = (signal.get("direction") or "").lower()
    mode = (signal.get("mode") or "").lower()
    asset = (signal.get("asset_class") or "crypto").lower()

    if pl.playbook == "crypto_scalp_momentum_continuation":
        flags.append("LOW-CONFIDENCE SCALP — paper only unless manually approved")
    if asset == "crypto" and mode == "intraday" and direction == "short" \
            and int(signal.get("news_supported") or 0) == 0:
        # No fresh catalyst + no derivatives confirmation → historically thin.
        funding = (signal.get("funding_context") or "").lower()
        oi = (signal.get("oi_context") or "").lower()
        has_deriv = ("crowded" in funding and "long" in funding) or "deleveraging" in oi
        if not has_deriv:
            flags.append("NO-NEWS / NO-DERIV SHORT — historically weak edge")
    if asset == "stocks" and pl.playbook == "stocks_intraday_rth_momentum" \
            and tier == "A" and direction == "long":
        flags.append("A-tier long caution / RTH-open chase risk")
    if direction == "short":
        # crowding / squeeze risk
        funding = (signal.get("funding_context") or "").lower()
        if "crowded" in funding or "squeeze" in funding:
            flags.append("squeeze risk: shorts crowded per funding context")
    if (signal.get("data_confidence") or "").lower() == "low":
        flags.append("low data confidence")
    if (signal.get("primary_exchange") or "").lower() == "mexc":
        flags.append("MEXC primary — thin liquidity")
    if not flags:
        flags.append("none")
    return flags


def _paper_entry_profile(signal: dict[str, Any]) -> str | None:
    """Return the versioned Paper profile carried with an entry alert.

    This is provenance, not a routing decision. The live canary separately
    rejects a Paper profile whose version is not explicitly allowlisted there.
    """
    explicit = str(signal.get("paper_entry_profile") or "").strip()
    if explicit:
        return explicit
    if ((signal.get("asset_class") or "crypto").lower() == "crypto"
            and (signal.get("mode") or "").lower() == "swing"):
        try:
            from src.execution.crypto_swing_paper_policy import load_cfg, target_profile, targets_match_profile
            cfg = load_cfg()
            profile = target_profile(signal, profile="production", cfg=cfg)
            if profile.get("available") and targets_match_profile(signal, profile):
                return str(profile.get("version") or "") or None
        except Exception:
            return None
    return None


def decide_paper_entry(signal: dict[str, Any], prev_status: str,
                      entry_triggered: bool,
                      entry_triggered_at: str | None,
                      entry_price_used: float | None,
                      *,
                      db: str | None = None,
                      ) -> PaperEntryDecision:
    """Return a decision object for the paper-entry alert.

    Caller is responsible for dedup (check signal_alerts before sending).
    """
    if not entry_triggered:
        return PaperEntryDecision(False, reason_skipped="entry not triggered")

    # Transition gate: must have come FROM a pending status
    norm_prev = (prev_status or "").lower().strip()
    if norm_prev and norm_prev not in PENDING_STATUSES:
        # only skip if previous was already an entered state
        if norm_prev in {"triggered", "entered", "active"}:
            return PaperEntryDecision(False, reason_skipped="already in entered state")

    # Tier gate: A/B only. The ONE narrow exception: a stocks-intraday C-tier
    # demoted ONLY by market_closed_intraday_planning_only (pre-gate A/B) can
    # be treated as actionable here if a fresh, non-BLOCK pre-US-open LLM
    # review supports it (review_adjusted tier A/B) — see
    # src/execution/stocks_preus_review.py. This never changes the stored
    # tier/score on proposed_signals; it only affects THIS decision. Any
    # missing/expired/errored review falls straight back to the unmodified
    # deterministic tier gate below — the LLM review is never waited on.
    tier = (signal.get("tier") or "").upper()
    if tier not in {"A", "B"}:
        review_supported = False
        # Keep pre-US promotion point-in-time: replay/backfill decisions must
        # be judged against the review that existed when the entry triggered,
        # not against the wall clock when a notifier later renders the alert.
        review_now = _parse_iso(entry_triggered_at)
        if db and (signal.get("asset_class") or "").lower() == "stocks" \
                and (signal.get("mode") or "").lower() == "intraday" and tier == "C":
            try:
                from src.execution.stocks_preus_review import is_review_supported_for_preopen
                review_supported, _reason = is_review_supported_for_preopen(
                    db, signal, now=review_now
                )
            except Exception:
                review_supported = False
        if not review_supported:
            return PaperEntryDecision(False, reason_skipped=f"tier={tier} not actionable")

    # Playbook gate
    pl = label_for(signal)
    if pl.playbook in PLAYBOOKS_FORBIDDEN_FOR_ENTRY_ALERT:
        return PaperEntryDecision(False, reason_skipped=f"playbook {pl.playbook} paused")
    if pl.status == "watchlist_only":
        return PaperEntryDecision(False, reason_skipped="playbook is watchlist-only")

    # Asset class + mode gate (defense in depth)
    asset = (signal.get("asset_class") or "crypto").lower()
    mode = (signal.get("mode") or "").lower()
    if asset == "stocks" and mode in {"swing", "invest"}:
        return PaperEntryDecision(False, reason_skipped="stocks swing/invest is paper-paused")

    # All gates passed — build the message
    direction = (signal.get("direction") or "long").upper()
    symbol = signal.get("symbol") or "?"
    score = float(signal.get("score") or 0)
    entry_str = _fmt_price(entry_price_used or signal.get("suggested_entry") or signal.get("entry_trigger"))
    stop_str = _fmt_price(signal.get("stop_loss") or signal.get("invalidation"))
    tp1_str = _fmt_price(signal.get("tp1"))
    tp2_str = _fmt_price(signal.get("tp2"))
    tp3_str = _fmt_price(signal.get("tp3"))
    paper_profile = _paper_entry_profile(signal)
    sized = size_decision(signal)
    size_weight = sized.weight
    size_reason = sized.reason or ("primary cohort" if size_weight == 1.0 else
                                   ("paused cohort" if size_weight == 0.0 else "scaled cohort"))
    if paper_profile == "stocks_intraday_pullback_vwap_paper_v2":
        try:
            profile_weight = max(0.0, min(1.0, float(signal.get("paper_size_weight"))))
        except (TypeError, ValueError):
            profile_weight = 1.0
        if profile_weight < size_weight:
            size_weight = profile_weight
            size_reason = str(signal.get("paper_size_reason") or "pullback_v2_quality_size")

    rationale = _extract_rationale(signal)
    flags = _risk_flags(signal)
    tv = _tradingview_link(asset, symbol, signal.get("primary_exchange"))

    # 2026-06-14 standardization — explicit colored emoji header per direction,
    # signal_id in visible body, condensed rationale.
    from src.notifiers.alert_headers import (
        HEADER_PAPER_ENTRY_LONG,
        HEADER_PAPER_ENTRY_SHORT,
    )

    header = HEADER_PAPER_ENTRY_SHORT if direction.lower() == "short" \
        else HEADER_PAPER_ENTRY_LONG
    lines: list[str] = []
    lines.append(header)
    lines.append(f"{asset.upper()} {symbol} {direction}")
    lines.append("")
    lines.append(f"Entry: {entry_str}")
    lines.append(f"Time: {_eest_format(entry_triggered_at)}")
    lines.append(f"Playbook: {pl.playbook}")
    if paper_profile:
        lines.append(f"Paper profile: {paper_profile}")
    execution_entry_mode = str(signal.get("paper_execution_entry_mode") or "").strip()
    source_entry_mode = str(signal.get("paper_source_entry_mode") or "").strip()
    if execution_entry_mode:
        lines.append(f"Executed entry mode: {execution_entry_mode}")
    if source_entry_mode and source_entry_mode != execution_entry_mode:
        lines.append(f"Source entry mode: {source_entry_mode}")
    lines.append(f"Tier/Score: {tier} / {score:g}")
    lines.append(f"Size: {size_weight:g}x")
    lines.append("")
    lines.append(f"Stop: {stop_str}")
    lines.append(f"TP: {tp1_str} / {tp2_str} / {tp3_str}")
    lines.append("")
    # 2026-06-15 catalyst safe-fix PART 4: compact 3-line catalyst context.
    try:
        from src.signals.catalyst_labels import telegram_block
        lines.extend(telegram_block(signal))
        lines.append("")
    except Exception:
        pass
    lines.append("Why now:")
    # Keep at most 2 short rationale lines on the wire.
    for b in rationale[:2]:
        lines.append(f"- {b}")
    lines.append("")
    lines.append("Risk:")
    for f in flags[:3]:
        lines.append(f"- {f}")
    lines.append("")
    lines.append("Manual check:")
    lines.append("Confirm chart + liquidity before any real trade.")
    lines.append("Paper entry recorded. MEXC execution is confirmed separately after preflight.")
    lines.append("")
    sid = signal.get("signal_id") or ""
    if sid:
        lines.append(f"signal_id: {sid}")
    lines.append(f"TradingView: {tv}")

    message = _cap("\n".join(lines), MAX_PAPER_ENTRY)

    payload = {
        "signal_id": signal.get("signal_id"),
        "symbol": symbol,
        "asset_class": asset,
        "tier": tier,
        "playbook": pl.playbook,
        "size_weight": size_weight,
        "size_reason": size_reason,
        "rationale": rationale,
        "risk_flags": flags,
        "entry_used": entry_price_used,
        # Preserve the geometry anchor separately from the executable quote.
        # A stock confirmation can arrive after price moved beyond the planned
        # trigger; the live bridge needs both values to rebuild the same R
        # ladder without guessing.
        "entry_reference": (
            signal.get("entry_trigger") or signal.get("suggested_entry")
            or signal.get("entry_high") or signal.get("entry_low")
        ),
        "entry_triggered_at": entry_triggered_at,
        "stop": signal.get("stop_loss"),
        "tp1": signal.get("tp1"), "tp2": signal.get("tp2"), "tp3": signal.get("tp3"),
        "tradingview": tv,
        "paper_entry_profile": paper_profile,
        "paper_execution_entry_mode": execution_entry_mode or None,
        "paper_source_entry_mode": source_entry_mode or None,
    }
    try:
        raw = json.loads(signal.get("raw_idea_json") or "{}")
        if isinstance(raw, dict):
            stop_contract = raw.get("initial_stop_contract") or raw.get("stop_contract") or {}
            if isinstance(stop_contract, dict) and stop_contract:
                payload["initial_stop_contract"] = stop_contract
                payload["stop_contract"] = stop_contract
                payload["stop_label"] = stop_contract.get("label") or stop_contract.get("stop_source")
            candidate_contract = raw.get("candidate_structural_stop_contract") or {}
            if isinstance(candidate_contract, dict) and candidate_contract:
                payload["candidate_structural_stop_contract"] = candidate_contract
    except Exception:
        pass

    return PaperEntryDecision(
        should_send=True,
        message=message,
        risk_flags=flags,
        rationale_bullets=rationale,
        size_weight=size_weight,
        size_reason=size_reason,
        playbook=pl.playbook,
        payload=payload,
    )


def is_shadow_only_scalp(signal: dict[str, Any]) -> bool:
    """Crypto scalp is SHADOW ONLY (2026-06-15 downgrade).

    The 12-month historical backtest showed crypto scalp is net-negative after
    realistic fees (WR 43% / PF 0.63 / avg -0.466R; train+val+OOS all negative;
    no exit/regime variant flips positive). So scalp paper-entry alerts are NOT
    sent as immediate actionable Telegram — they are recorded as shadow_only for
    research/journal visibility but never pushed to the operator's phone.
    See reports/SCALP_KEEP_REWORK_DISABLE_DECISION.md.
    Scoped to crypto scalp ONLY for paper-entry classification. The live-only
    Telegram dispatcher separately suppresses all non-live Paper notifications.
    """
    asset = (signal.get("asset_class") or "crypto").lower()
    mode = (signal.get("mode") or "").lower()
    return asset == "crypto" and mode == "scalp"


# Paper-entry alerts older than this (entry touch → send time) are not
# realistically actionable for a manual mirror, so they are routed shadow-only
# instead of pushed as an actionable alert. Evidence: ENTRY_DETECTION_LATENCY_AUDIT.md
# (current median entry-age ~135 min until the Phase-2 cadence fix lands).
LATE_ENTRY_SHADOW_MINUTES = 15.0


def _parse_iso(ts: str | None) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    except Exception:
        return None


# Timeframe-aware freshness thresholds (minutes): (fresh, acceptable, very_late_over).
# Calibrated by the candle timeframe each mode trades — a touch on an N-min candle cannot
# be detected in < N min, so a universal 15m cutoff wrongly flags 15m-candle stock intraday
# entries as very-late. Crypto intraday/short/scalp stay TIGHT (do not loosen). Stocks
# intraday widened to its 15m-candle floor. A `note` is appended where a price-check is
# mandatory regardless of time.
_FRESHNESS_THRESHOLDS: dict[tuple[str, str], tuple[float, float, float, str]] = {
    ("crypto", "intraday"): (2, 5, 15, ""),
    ("crypto", "short"):    (2, 5, 15, ""),
    ("crypto", "scalp"):    (2, 5, 15, ""),       # shadow anyway; kept tight
    ("crypto", "swing"):    (15, 60, 240, ""),    # higher TF tolerates more delay
    ("stocks", "intraday"): (20, 30, 45, " (15m candle floor — price check required)"),
    ("stocks", "swing"):    (60, 240, 1440, ""),
}
_DEFAULT_THRESHOLD = (2, 5, 15, "")


def _freshness_thresholds(asset_class: str | None, mode: str | None):
    key = ((asset_class or "crypto").lower(), (mode or "").lower())
    return _FRESHNESS_THRESHOLDS.get(key, _DEFAULT_THRESHOLD)


def entry_freshness(
    entry_triggered_at: str | None,
    now: datetime | None = None,
    asset_class: str | None = None,
    mode: str | None = None,
) -> tuple[str, float | None, bool]:
    """Classify how stale a paper-entry alert is at send time, timeframe-aware.

    Returns ``(label_line, age_seconds, actionable)``. Never fabricates a
    fresher age (constraint: "do not make late paper-entry alerts look fresh").
    A negative age (candle/clock alignment) clamps to 0 = fresh. Thresholds vary by
    (asset_class, mode) — see ``_FRESHNESS_THRESHOLDS``; default stays the tight crypto
    intraday 2/5/15. ``actionable`` is False only for very-late / unknown.
    """
    now = now or datetime.now(timezone.utc)
    fresh_m, ok_m, late_m, note = _freshness_thresholds(asset_class, mode)
    t = _parse_iso(entry_triggered_at)
    if t is None:
        return ("Entry freshness: unknown — treat as NOT actionable", None, False)
    age = (now - t).total_seconds()
    if age < 0:
        age = 0.0
    m = age / 60.0
    if m <= fresh_m:
        return (f"Entry freshness: fresh {int(age)}s{note}", age, True)
    if m <= ok_m:
        return (f"Entry freshness: acceptable {m:.1f}m{note}", age, True)
    if m <= late_m:
        return (f"Entry freshness: late {m:.0f}m — check price before manual entry{note}", age, True)
    return (f"Entry freshness: very late {m:.0f}m — NOT actionable manually{note}", age, False)


def has_existing_paper_entry_alert(store: Any, signal_id: str) -> bool:
    """Return True if signal_alerts already has alert_type='paper_entry' for this signal_id."""
    try:
        with store.connect() as conn:
            row = conn.execute(
                "SELECT 1 FROM signal_alerts WHERE signal_id = ? AND alert_type = 'paper_entry' LIMIT 1",
                (signal_id,),
            ).fetchone()
        return row is not None
    except Exception:
        return False


def send_paper_entry_alert(
    *,
    store: Any,
    notifier: Any,
    signal: dict[str, Any],
    prev_status: str,
    outcome_entry_triggered: bool,
    outcome_entry_triggered_at: str | None,
    outcome_entry_price_used: float | None,
    outcome_entry_bar_open_at: str | None = None,
    outcome_entry_time_basis: str | None = None,
    outcome_entry_currently_executable: bool | None = None,
    outcome_entry_revalidation_reason: str | None = None,
    outcome_entry_bar_timeframe: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """High-level entry point.

    Returns a dict with keys:
      sent (bool), reason_skipped (str | None), payload (dict | None),
      alert_id (str | None), telegram_status (str | None).
    """
    decision_path_started = time.perf_counter()
    signal_id = signal.get("signal_id") or ""
    if has_existing_paper_entry_alert(store, signal_id):
        return {"sent": False, "reason_skipped": "duplicate", "payload": None,
                "alert_id": None, "telegram_status": None}

    decision = decide_paper_entry(
        signal,
        prev_status=prev_status,
        entry_triggered=outcome_entry_triggered,
        entry_triggered_at=outcome_entry_triggered_at,
        entry_price_used=outcome_entry_price_used,
        db=str(store.db_path) if getattr(store, "db_path", None) else None,
    )
    if not decision.should_send:
        return {"sent": False, "reason_skipped": decision.reason_skipped,
                "payload": None, "alert_id": None, "telegram_status": None}

    alert_id = str(uuid.uuid4())
    sent_at = datetime.now(timezone.utc).isoformat()

    # 2026-06-15 scalp downgrade: crypto scalp paper-entry is SHADOW ONLY.
    # Record the row (so journal/research keep visibility) but do NOT push an
    # actionable Telegram message to the operator. The stored message carries an
    # explicit shadow banner in case a digest renders it.
    shadow_only = is_shadow_only_scalp(signal)
    message = decision.message
    payload = dict(decision.payload or {})
    initial_size_weight = float(payload.get("size_weight") or 0.0)

    # Entry freshness (PART 5): tell the operator whether this entry is still
    # actionable, and route very-late entries shadow-only so the system never
    # nudges a chase of a stale entry. Scalp is already shadow; freshness is
    # informational there. Applies to all non-scalp modes too.
    fresh_line, entry_age_sec, actionable = entry_freshness(
        outcome_entry_triggered_at,
        asset_class=(signal.get("asset_class") or "crypto"),
        mode=signal.get("mode"),
    )
    provenance_supplied = outcome_entry_currently_executable is not None
    if provenance_supplied and not outcome_entry_currently_executable:
        actionable = False
        why = outcome_entry_revalidation_reason or "current executable price was not verified"
        fresh_line = f"Entry freshness: historical candle touch only - NOT actionable ({why})"
    is_stock_intraday = (
        (signal.get("asset_class") or "").lower() == "stocks"
        and (signal.get("mode") or "").lower() == "intraday"
    )
    stock_basis_accepted = (
        outcome_entry_time_basis is None
        or is_accepted_stock_intraday_paper_basis(outcome_entry_time_basis)
    )
    if is_stock_intraday and not stock_basis_accepted:
        actionable = False
        fresh_line = (
            "Entry freshness: unsupported stock-provider provenance - NOT actionable"
        )
    elif (is_stock_intraday
          and str(outcome_entry_time_basis) == PROVIDER_DELAYED_CURRENT_BAR
          and outcome_entry_currently_executable is True):
        fresh_line = (
            "Entry freshness: current price revalidated; delayed stock-data cohort"
        )
    payload["entry_freshness"] = fresh_line
    if entry_age_sec is not None:
        payload["entry_age_seconds"] = round(entry_age_sec)
    payload["entry_bar_open_at"] = outcome_entry_bar_open_at or outcome_entry_triggered_at
    payload["entry_time_basis"] = outcome_entry_time_basis or "legacy_unclassified"
    payload["current_price_revalidated"] = outcome_entry_currently_executable
    payload["entry_revalidation_reason"] = outcome_entry_revalidation_reason
    payload["entry_bar_timeframe"] = outcome_entry_bar_timeframe
    payload["entry_detected_at"] = (
        outcome_entry_triggered_at if outcome_entry_currently_executable else None
    )
    bar_at = _parse_iso(outcome_entry_bar_open_at)
    if bar_at is not None:
        payload["entry_bar_age_seconds"] = round(max(
            0.0, (datetime.now(timezone.utc) - bar_at).total_seconds()))
    late_entry = (not shadow_only) and (not actionable)  # very-late / unknown, non-scalp

    # Stocks concentration cap (2026-06-16): for stocks intraday A/B, de-noise
    # correlated stacking — 2nd same-bucket exposure → half-size warning (still
    # sent), 3rd+ or proxy-duplicate → shadow (not pushed). Crypto/other modes
    # return 'not_applicable'. Never raises (fails open).
    try:
        from src.signals.portfolio_caps import concentration_for_live_signal
        conc = concentration_for_live_signal(store, signal)
    except Exception:
        conc = {"concentration_status": "not_applicable", "concentration_reason": "",
                "risk_bucket": "n/a", "proxy_group": "n/a", "concentration_rank": None,
                "concentration_effective_weight": None}
    for k in ("risk_bucket", "proxy_group", "concentration_status",
              "concentration_rank", "concentration_effective_weight", "concentration_reason"):
        payload[k] = conc.get(k)
    conc_shadow = conc.get("concentration_status") in ("shadow_proxy_duplicate", "shadow_sector_cap")
    conc_half = conc.get("concentration_status") == "half_size"

    # Point-in-time stock options context. GEX/IV-RV is shadow/advisory by
    # default and cannot upgrade a candidate.
    stocks_context_shadow = False
    stocks_context_half = False
    stocks_context_reason = ""
    try:
        if (signal.get("asset_class") or "crypto").lower() == "stocks":
            from src.execution.stocks_market_context_overlay import decide_and_persist
            _stocks_ctx = decide_and_persist(
                signal, as_of=datetime.now(timezone.utc), trading_db_path=str(store.db_path))
            for _k, _v in _stocks_ctx.items():
                payload[f"stocks_context_{_k}"] = _v
            stocks_context_reason = str(_stocks_ctx.get("reason") or "")
            stocks_context_shadow = _stocks_ctx.get("action") in ("SHADOW_ONLY", "BLOCK")
            stocks_context_half = _stocks_ctx.get("action") == "HALF_SIZE"
    except Exception as _sce:
        payload["stocks_context_error"] = type(_sce).__name__

    # Risk-guard visibility fields. Most guards remain diagnostic-only. The two
    # narrow paper-only exceptions are circuit-breaker L2+ and a persistent,
    # multi-venue stablecoin depeg. Neither closes an existing position or can
    # authorize live execution.
    rg_fields: dict[str, Any] = {}
    rg_lines: list[str] = []
    risk_guard_shadow = False
    risk_guard_half = False
    risk_guard_reason = ""
    try:
        from src.risk.risk_guards import (
            assemble_risk_guard_fields, paper_risk_floor, risk_guard_warning_lines)
        rg_fields = assemble_risk_guard_fields(
            store, signal, now=datetime.now(timezone.utc),
            mfe_r=0.0, entry_triggered_at=outcome_entry_triggered_at,
            latency_critical=True)
        for k, v in rg_fields.items():
            payload.setdefault(k, v)
        floor = paper_risk_floor(rg_fields, signal)
        for k, v in floor.items():
            payload[k] = v
        risk_guard_shadow = floor.get("paper_risk_floor_action") in ("SHADOW_ONLY", "BLOCK")
        risk_guard_half = floor.get("paper_risk_floor_action") == "HALF_SIZE"
        risk_guard_reason = str(floor.get("paper_risk_floor_reason") or "")
        rg_lines = risk_guard_warning_lines(rg_fields)
        # Circuit-breaker line is deduped one-per asset/mode/day/level so we do not
        # spam the same would-pause warning on every entry that day.
        cb_key = None
        if rg_fields.get("circuit_breaker_state") == "would_pause":
            _day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            cb_key = (f"cb_diag:{(signal.get('asset_class') or 'crypto')}:"
                      f"{signal.get('mode') or '?'}:{_day}:"
                      f"L{rg_fields.get('circuit_breaker_level')}")
            try:
                if store.last_alert_by_type(cb_key) is not None:
                    # already warned for this asset/mode/day/level → drop the CB line
                    rg_lines = [ln for ln in rg_lines if "Circuit breaker" not in ln]
                    cb_key = None
            except Exception:
                cb_key = None
        payload["_cb_dedupe_key"] = cb_key
    except Exception:
        rg_fields = {}
        rg_lines = []

    # Stocks-intraday C-tier policy (FAST SAFE ACCELERATION 2026-06-17): route a
    # restricted C-tier signal to shadow/review-only. ROUTING + LABEL ONLY — never
    # changes scoring, tier, TP/SL, or size. Crypto and A/B stocks are unaffected.
    try:
        from src.signals.tier_policy import (
            c_tier_restriction_fields,
            is_restricted,
            load_stocks_intraday_c_tier_policy,
        )
        _ctier_policy = load_stocks_intraday_c_tier_policy()
        c_tier_restricted = is_restricted(signal, _ctier_policy)
        for _k, _v in c_tier_restriction_fields(signal, _ctier_policy).items():
            payload[_k] = _v
    except Exception:
        c_tier_restricted = False

    # Pre-US-open review overlay (stocks intraday only): the ONE case where a
    # session-cap-only C (demoted purely by market_closed_intraday_planning_only,
    # pre-gate tier A/B) can be treated as actionable — never touches the stored
    # tier/score, never applies to a substantively-rejected C. Missing/expired/
    # errored review is silently treated as "not supported" (deterministic
    # fallback); this never waits or blocks the pipeline.
    preus_review_supported = False
    try:
        if c_tier_restricted and (signal.get("asset_class") or "").lower() == "stocks" \
                and (signal.get("mode") or "").lower() == "intraday":
            from src.execution.stocks_preus_review import active_review, is_review_supported_for_preopen
            supported, support_reason = is_review_supported_for_preopen(str(store.db_path), signal)
            payload["preus_review_supported"] = supported
            payload["preus_review_reason"] = support_reason
            if supported:
                review_row = active_review(str(store.db_path), str(signal.get("signal_id") or ""))
                if review_row:
                    payload["preus_review_verdict"] = review_row.get("review_verdict")
                    payload["preus_review_score_adjustment"] = review_row.get("review_score_adjustment")
                    payload["preus_review_adjusted_score"] = review_row.get("review_adjusted_score")
                    payload["preus_review_tier"] = review_row.get("review_tier")
                    payload["preus_reviewed_at"] = review_row.get("reviewed_at")
                    payload["preus_review_expires_at"] = review_row.get("review_expires_at")
                    try:
                        payload["preus_review_reason_codes"] = json.loads(
                            review_row.get("review_reason_codes_json") or "[]")
                    except (TypeError, ValueError):
                        payload["preus_review_reason_codes"] = []
                preus_review_supported = True
                c_tier_restricted = False
    except Exception:
        preus_review_supported = False

    # SI-6 scheduled-LLM-review routing (ADVISORY, config-gated). Scoped to stocks intraday A/B only.
    # A fresh LLM reject/wait routes the paper candidate to review-only/shadow; when the operator has
    # opted into require_fresh, a missing fresh review also routes to shadow. Missing review does NOT
    # block by default. NEVER changes tier/score/TP/SL, never touches proposed_signals, never live.
    llm_review_shadow = False
    llm_review_reason = ""
    try:
        _asset = (signal.get("asset_class") or "crypto").lower()
        _mode = (signal.get("mode") or "").lower()
        _tier = (signal.get("tier") or "").upper()
        if _asset == "stocks" and _mode == "intraday" and _tier in ("A", "B"):
            from src.stocks import intraday_llm_review as _llm
            from src.stocks import load_stocks_config as _lsc
            _lr_cfg = ((getattr(_lsc(), "risk", {}) or {}).get("intraday_guards") or {})
            llm_review_shadow, llm_review_reason = _llm.should_route_to_review(
                db=str(store.db_path), signal_id=signal_id,
                cfg={"llm_review": (_lr_cfg.get("llm_review") or {})})
            payload["llm_review_routed_to_shadow"] = bool(llm_review_shadow)
            payload["llm_review_reason"] = llm_review_reason
    except Exception:
        # fail-open here is safe: this is an ADVISORY overlay on top of the fail-conservative gates
        # that already ran at signal creation; a routing-helper error must not crash the tracker.
        llm_review_shadow = False
        llm_review_reason = ""

    # Crypto quality/risk overlay (2026-07-08): soft sizing/routing breaker for crypto paper candidates
    # based on BTC/ETH regime, session quality, rolling session+symbol cooldowns, exposure and
    # entry-mode quality. HALF_SIZE → 0.5x; SHADOW_ONLY/BLOCK → recorded, not pushed. Scoped to crypto
    # only; ONLY ever downgrades (never upgrades); never touches tier/score/TP-SL/proposed_signals/live.
    # Fail-conservative inside the module. Config: crypto_quality_overlay.yaml (paper_actionability_enabled).
    crypto_overlay_shadow = False
    crypto_overlay_half = False
    crypto_overlay_reason = ""
    try:
        if (signal.get("asset_class") or "crypto").lower() == "crypto":
            from src.execution import crypto_quality_overlay as _cqo
            _cqo_cfg = _cqo.load_cfg()
            if _cqo_cfg.get("enabled", True) and _cqo_cfg.get("paper_actionability_enabled", True):
                _cq = _cqo.decide_for_signal(signal, db=str(store.db_path), cfg=_cqo_cfg)
                _cqf = _cq.fields()
                crypto_overlay_reason = ", ".join(_cq.reasons[:4])
                for _k in ("quality_action", "crypto_quality_verdict", "crypto_quality_score",
                           "btc_regime_state", "session_bucket_utc", "session_quality_state",
                           "symbol_cooldown_state", "mode_session_cooldown_state",
                           "would_have_been_action_without_overlay", "entry_mode",
                           "entry_mode_source", "preentry_data_quality", "overlay_version",
                           "overlay_config_hash", "token_unlock_status",
                           "token_unlock_would_action", "token_unlock_reason",
                           "token_unlock_days_to_unlock", "token_unlock_pct_circulating",
                           "cross_exchange_status", "cross_exchange_action",
                           "cross_exchange_would_action", "cross_exchange_reason",
                           "cross_exchange_divergence_bps", "cross_exchange_fresh_venues",
                           "cross_exchange_persistent", "options_status", "options_iv30",
                           "options_rv30", "options_vrp", "options_iv_rank"):
                    payload[f"cqo_{_k}"] = _cqf.get(_k)
                payload["cqo_reasons"] = _cq.reasons
                try:
                    payload["cqo_snapshot_persisted"] = bool(
                        _cqo.persist_point_in_time_decision(_cq, db=str(store.db_path)))
                    payload["context_filter_decisions_persisted"] = int(
                        _cqo.persist_context_filter_decisions(_cq))
                except Exception as _snap_exc:
                    payload["cqo_snapshot_error"] = type(_snap_exc).__name__
                if _cq.action in ("SHADOW_ONLY", "BLOCK"):
                    crypto_overlay_shadow = True
                elif _cq.action == "HALF_SIZE":
                    crypto_overlay_half = True
    except Exception as _cqe:
        # FAIL-CONSERVATIVE (not fail-open): an overlay error must NOT let a crypto paper candidate ride
        # at full size. Apply the config default (HALF_SIZE) and record the error for diagnostics.
        if (signal.get("asset_class") or "crypto").lower() == "crypto":
            try:
                from src.execution import crypto_quality_overlay as _cqo2
                _default = str((_cqo2.load_cfg() or {}).get("default_unknown_data_action", "HALF_SIZE"))
            except Exception:
                _default = "HALF_SIZE"
            crypto_overlay_shadow = _default in ("SHADOW_ONLY", "BLOCK")
            crypto_overlay_half = _default == "HALF_SIZE"
            crypto_overlay_reason = f"overlay_error:{type(_cqe).__name__}"
            payload["cqo_error"] = type(_cqe).__name__
            payload["cqo_quality_action"] = _default
            payload["cqo_reasons"] = [crypto_overlay_reason]
        else:
            crypto_overlay_shadow = False
            crypto_overlay_half = False

    # Late alerts are research records, never executable paper positions. Keep
    # the requested overlay action for diagnostics but make the persisted
    # payload internally consistent with the non-actionable alert status.
    if late_entry:
        if crypto_overlay_half:
            payload["cqo_requested_size_weight"] = 0.5
        payload["cqo_effective_paper_action"] = "SHADOW_ONLY"
        payload["size_weight"] = 0.0
        payload["size_reason"] = "late_shadow_non_actionable"

    # Optional crypto-swing main-paper floor. It is currently disabled while the
    # native swing geometry remains the production-paper control and target
    # profiles are evaluated in shadow. Keep the legacy overlay behaviour intact.
    try:
        if (signal.get("asset_class") or "crypto").lower() == "crypto" and (signal.get("mode") or "").lower() == "swing":
            from src.execution.crypto_swing_paper_policy import apply_main_paper_floor
            _action = str(payload.get("cqo_quality_action") or ("SHADOW_ONLY" if crypto_overlay_shadow else
                                                                "HALF_SIZE" if crypto_overlay_half else "FULL_SIZE"))
            _base = {
                "paper_action": _action,
                "size_weight": 0.0 if crypto_overlay_shadow else (0.5 if crypto_overlay_half else
                                                                  float(payload.get("size_weight") or 1.0)),
                "source": "alert_payload" if payload.get("cqo_quality_action") else "legacy_actionable",
                "reason": crypto_overlay_reason or str(payload.get("size_reason") or _action),
                "overlay_version": payload.get("cqo_overlay_version"),
            }
            with store.connect() as _pol_conn:
                _floor = apply_main_paper_floor(
                    _pol_conn, signal_id=signal_id, asset_class="crypto", mode="swing",
                    tier=signal.get("tier"), base=_base, signal=signal,
                    extra_reasons=[str(x) for x in (payload.get("cqo_reasons") or [])],
                )
            for _k in ("crypto_swing_policy_profile", "crypto_swing_policy_version",
                       "crypto_swing_target_multipliers", "crypto_swing_latency_cause",
                       "crypto_swing_clean_for_main_paper", "crypto_swing_main_policy_applied",
                       "crypto_swing_breakout_experiment_id", "crypto_swing_breakout_latency_cause",
                       "crypto_swing_breakout_experiment_applied"):
                if _k in _floor:
                    payload[_k] = _floor[_k]
            payload["crypto_swing_main_paper_action"] = _floor.get("paper_action")
            payload["crypto_swing_main_paper_reason"] = _floor.get("reason")
            _policy_applied = bool(_floor.get("crypto_swing_main_policy_applied"))
            if _policy_applied and float(_floor.get("size_weight") or 0.0) <= 0.0:
                crypto_overlay_shadow = True
                crypto_overlay_half = False
                crypto_overlay_reason = str(_floor.get("reason") or "crypto swing strict paper policy")
            elif _policy_applied:
                crypto_overlay_shadow = False
                crypto_overlay_half = False
                payload["size_weight"] = float(_floor.get("size_weight") or payload.get("size_weight") or 1.0)
                payload["size_reason"] = str(_floor.get("reason") or payload.get("size_reason") or "")
    except Exception as _cspe:
        if (signal.get("asset_class") or "crypto").lower() == "crypto" and (signal.get("mode") or "").lower() == "swing":
            crypto_overlay_shadow = True
            crypto_overlay_half = False
            crypto_overlay_reason = f"crypto_swing_policy_error:{type(_cspe).__name__}"
            payload["crypto_swing_policy_error"] = type(_cspe).__name__

    if shadow_only:
        message = ("[SHADOW ONLY — DO NOT TRADE]\nCRYPTO SCALP\n"
                   "Not actionable. Research only.\n\n" + message + "\n" + fresh_line)
        payload["telegram_channel"] = "shadow_only"
    elif c_tier_restricted:
        message = ("[SHADOW / REVIEW ONLY — C-TIER RESTRICTED]\n"
                   "Stocks intraday C-tier restricted to shadow/review-only "
                   "(stocks_intraday_c_tier_30d_negative).\n\n"
                   + message + "\n" + fresh_line)
        payload["telegram_channel"] = "shadow_only_c_tier"
    elif conc_shadow:
        message = ("[SHADOW ONLY — SECTOR CAP]\n"
                   f"Reason: {conc.get('concentration_reason')}\n\n" + message + "\n" + fresh_line)
        payload["telegram_channel"] = "shadow_only_sector_cap"
    elif stocks_context_shadow:
        message = ("[SHADOW ONLY - STOCKS MARKET CONTEXT]\n"
                   f"Reason: {stocks_context_reason}\n\n" + message + "\n" + fresh_line)
        payload["telegram_channel"] = "shadow_only_stocks_context"
    elif late_entry:
        message = ("[LATE ENTRY DETECTED — DO NOT CHASE]\n"
                   + message + "\n" + fresh_line)
        payload["telegram_channel"] = "shadow_only_late"
    elif risk_guard_shadow:
        message = ("[SHADOW ONLY — PAPER RISK GUARD]\n"
                   f"Reason: {risk_guard_reason or 'circuit-breaker pause'}\n\n"
                   + message + "\n" + fresh_line)
        if rg_lines:
            message = message + "\n" + "\n".join(rg_lines)
        payload["telegram_channel"] = "shadow_only_risk_guard"
    elif llm_review_shadow:
        message = ("[SHADOW / REVIEW ONLY — LLM REVIEW]\n"
                   f"Stocks intraday A/B routed to review-only ({llm_review_reason}).\n\n"
                   + message + "\n" + fresh_line)
        payload["telegram_channel"] = "shadow_only_llm_review"
    elif crypto_overlay_shadow:
        message = ("[SHADOW ONLY — CRYPTO QUALITY OVERLAY]\n"
                   f"Reason: {crypto_overlay_reason or 'quality overlay downgrade'}\n\n"
                   + message + "\n" + fresh_line)
        payload["telegram_channel"] = "shadow_only_crypto_quality"
    else:
        if risk_guard_half:
            # Apply the authoritative Paper floor before optional overlay
            # reductions.  Two independent HALF_SIZE protections compound to
            # 0.25x; a floor is never allowed to make a trade larger.
            base_w = float(payload.get("size_weight") or 1.0)
            payload["size_weight"] = round(base_w * 0.5, 4)
            existing = str(payload.get("size_reason") or "")
            payload["size_reason"] = (
                f"{existing}; paper_risk_guard_half".strip("; ")
            )
            message = (f"Paper risk guard: HALF SIZE ({risk_guard_reason})\n" + message)
        if crypto_overlay_half:
            # HALF_SIZE: keep actionable but halve the paper size and say why. Mirrors conc_half.
            base_w = float(payload.get("size_weight") or 1.0)
            payload["size_weight"] = round(base_w * 0.5, 4)
            payload["size_reason"] = f"crypto_quality_half: {crypto_overlay_reason}"
            message = (f"Crypto quality overlay: HALF SIZE ({crypto_overlay_reason})\n" + message)
        if conc_half:
            message = (f"Correlation cap: {conc.get('concentration_reason')}\n" + message)
        if stocks_context_half:
            base_w = float(payload.get("size_weight") or 1.0)
            payload["size_weight"] = round(base_w * 0.5, 4)
            payload["size_reason"] = f"stocks_market_context_half: {stocks_context_reason}"
            message = (f"Stocks market context: HALF SIZE ({stocks_context_reason})\n" + message)
        if preus_review_supported:
            # Compact one-liner only — never the LLM's full reasoning on the wire.
            adj = payload.get("preus_review_score_adjustment")
            adj_str = f"{adj:+.0f}" if isinstance(adj, (int, float)) else "+0"
            codes = payload.get("preus_review_reason_codes") or []
            detail = " | ".join(str(c) for c in codes[:2]) or "session-cap review support"
            message = (f"Pre-US review: {payload.get('preus_review_verdict', 'SUPPORT')} "
                       f"({adj_str}) | {detail}\n" + message)
        final_size_weight = float(payload.get("size_weight") or 0.0)
        if final_size_weight != initial_size_weight:
            message = message.replace(
                f"Size: {initial_size_weight:g}x",
                f"Size: {final_size_weight:g}x",
                1,
            )
        message = message + "\n" + fresh_line
        if rg_lines:
            message = message + "\n" + "\n".join(rg_lines)
        payload["telegram_channel"] = "telegram"

    # Stable, enumerable reason codes for the dashboard, audit exports and
    # MEXC handoff diagnostics.  Keep the human explanation separately in the
    # message; consumers must never parse free-form prose to learn why a Paper
    # candidate was not tradeable.
    decision_codes: list[str] = []
    if outcome_entry_currently_executable is False:
        decision_codes.append("PRICE_NOT_REVALIDATED")
    if is_stock_intraday and outcome_entry_time_basis is not None and not stock_basis_accepted:
        decision_codes.append("STOCK_ENTRY_NOT_POINT_IN_TIME")
    elif (is_stock_intraday
          and str(outcome_entry_time_basis) == PROVIDER_DELAYED_CURRENT_BAR):
        decision_codes.append("STOCK_ENTRY_DELAYED_DATA_COHORT")
    if late_entry:
        decision_codes.append("LATE_PRICE")
    if risk_guard_shadow:
        decision_codes.append("PAPER_RISK_GUARD_PAUSE")
    elif risk_guard_half:
        decision_codes.append("PAPER_RISK_GUARD_HALF")
    if crypto_overlay_shadow:
        decision_codes.append("CRYPTO_QUALITY_SHADOW")
    elif crypto_overlay_half:
        decision_codes.append("CRYPTO_QUALITY_HALF")
    if stocks_context_shadow:
        decision_codes.append("STOCKS_CONTEXT_SHADOW")
    elif stocks_context_half:
        decision_codes.append("STOCKS_CONTEXT_HALF")
    if llm_review_shadow:
        decision_codes.append("LLM_REVIEW_SHADOW")
    payload["paper_decision_reason_codes"] = decision_codes or ["PAPER_ACTIONABLE"]
    # Freeze the final point-in-time Paper decision into an isolated MEXC
    # outbox before Telegram I/O. This cannot authorize a trade on its own and
    # any failure remains invisible to Paper lifecycle/accounting.
    pre_capture_runtime_ms = round((time.perf_counter() - decision_path_started) * 1000.0, 1)
    capture_started = time.perf_counter()
    try:
        from src.live_execution.service import capture_paper_candidate
        payload["paper_entry_dry_run"] = bool(dry_run)
        _mexc_capture = capture_paper_candidate(
            store=store, signal=signal, payload=payload, paper_alert_id=alert_id)
        # Stocks use a version-pinned bridge rather than the crypto policy.
        # Queue the exact point-in-time Paper entry here, before Telegram I/O,
        # so a one-minute stock-monitor poll cannot miss the five-minute live
        # handoff window.
        if (
            _mexc_capture.get("status") == "OUT_OF_SCOPE"
            and str(signal.get("asset_class") or "").lower() == "stocks"
            and str(signal.get("mode") or "").lower() == "intraday"
        ):
            from src.live_execution.stocks_breakout_bridge import (
                capture_standard_paper_breakouts,
            )
            _stock_capture = capture_standard_paper_breakouts(
                db=getattr(store, "db_path", None),
                now=datetime.now(timezone.utc),
                source_signal_id=str(signal.get("signal_id") or ""),
                payload_override=payload,
                paper_alert_id=alert_id,
            )
            if int(_stock_capture.get("queued") or 0) > 0:
                _mexc_capture = {
                    "status": "QUEUED",
                    "queued": True,
                    "decision_id": None,
                    "reasons": [],
                    "execution_mode": "live",
                }
            elif int(_stock_capture.get("duplicate") or 0) > 0:
                _mexc_capture = {
                    "status": "DUPLICATE",
                    "queued": False,
                    "decision_id": None,
                    "reasons": [],
                    "execution_mode": "live",
                }
            elif int(_stock_capture.get("rejected") or 0) > 0:
                _mexc_capture = {
                    "status": "REJECTED",
                    "queued": False,
                    "decision_id": None,
                    "reasons": list((_stock_capture.get("reasons") or {}).keys()),
                    "execution_mode": "live",
                }
            elif int(_stock_capture.get("seen") or 0) > 0:
                _mexc_capture = {
                    "status": "REJECTED",
                    "queued": False,
                    "decision_id": None,
                    "reasons": list((_stock_capture.get("reasons") or {}).keys()),
                    "execution_mode": "live",
                }
        _mexc_overrides = _mexc_capture.get("payload_overrides") or {}
        if isinstance(_mexc_overrides, dict) and _mexc_overrides:
            payload.update(_mexc_overrides)
        payload["mexc_canary_capture_status"] = _mexc_capture.get("status")
        payload["mexc_canary_decision_id"] = _mexc_capture.get("decision_id")
        payload["mexc_canary_capture_reasons"] = _mexc_capture.get("reasons") or []
        payload["mexc_canary_execution_mode"] = _mexc_capture.get("execution_mode")
        payload["mexc_handoff_reason_codes"] = [str(x) for x in (_mexc_capture.get("reasons") or [])]
    except Exception as _mexc_exc:
        payload["mexc_canary_capture_status"] = f"error:{type(_mexc_exc).__name__}"
    live_capture_runtime_ms = round((time.perf_counter() - capture_started) * 1000.0, 1)

    # Diagnostic enrichment is deliberately after the live handoff snapshot:
    # it cannot change actionability and must not delay a candidate reaching
    # preflight. The compact fields remain available to the alert journal.
    intel_lines: list[str] = []
    try:
        from src.intelligence.intelligence_layer import (
            assemble_intelligence_fields, intelligence_telegram_lines)
        intel = assemble_intelligence_fields(
            signal, store=store, now=datetime.now(timezone.utc), prior_fields=payload)
        for _k, _v in intel.items():
            payload.setdefault(_k, _v)
        intel_lines = intelligence_telegram_lines(intel)
    except Exception:
        intel_lines = []

    # A Paper alert is not an execution confirmation. Operator Telegram is now
    # live-only: only an accepted live-handoff queue emits a phone message.
    # Rejected/out-of-scope Paper entries remain fully recorded for dashboards
    # and research, but they no longer masquerade as tradable alerts.
    capture_status = str(payload.get("mexc_canary_capture_status") or "")
    capture_reasons = [str(item) for item in (payload.get("mexc_canary_capture_reasons") or [])]
    if capture_status == "QUEUED":
        if payload.get("mexc_live_repriced"):
            late_entry = False
        payload["telegram_channel"] = "live_handoff"
        message = _compact_live_entry_message(signal, payload, fresh_line=fresh_line)
    elif (
        shadow_only
        or c_tier_restricted
        or conc_shadow
        or stocks_context_shadow
        or late_entry
        or risk_guard_shadow
        or llm_review_shadow
        or crypto_overlay_shadow
    ):
        # Keep the shadow/review/risk diagnostic message already built above.
        pass
    elif capture_status == "DUPLICATE":
        payload["telegram_channel"] = "live_duplicate"
        message = _compact_not_queued_message(signal, capture_status, ["duplicate live handoff"])
    elif capture_status == "REJECTED":
        if not str(payload.get("telegram_channel") or "").lower().startswith("shadow"):
            payload["telegram_channel"] = "live_not_queued"
        message = _compact_not_queued_message(signal, capture_status, capture_reasons)
    elif capture_status.startswith("error:"):
        if not str(payload.get("telegram_channel") or "").lower().startswith("shadow"):
            payload["telegram_channel"] = "live_capture_error"
        message = _compact_not_queued_message(signal, capture_status, ["capture unavailable"])
    elif capture_status:
        if not str(payload.get("telegram_channel") or "").lower().startswith("shadow"):
            payload["telegram_channel"] = "live_not_queued"
        message = _compact_not_queued_message(signal, capture_status, capture_reasons)
    else:
        if not str(payload.get("telegram_channel") or "").lower().startswith("shadow"):
            payload["telegram_channel"] = "live_capture_missing"
        message = _compact_not_queued_message(signal, capture_status, ["capture missing"])
    message_hash = hashlib.sha256(message.encode("utf-8")).hexdigest()[:16]

    cb_dedupe_key = payload.pop("_cb_dedupe_key", None)
    staged_delivery = False
    telegram_status: str
    if shadow_only:
        # Never push to the phone; route to shadow/journal/digest.
        telegram_status = "shadow_only"
    elif c_tier_restricted:
        # Stocks-intraday C-tier: recorded for review/journal, never pushed actionable.
        telegram_status = "shadow_c_tier"
    elif conc_shadow:
        # 3rd+ correlated / proxy-duplicate stock exposure: recorded, not pushed.
        telegram_status = "shadow_sector_cap"
    elif stocks_context_shadow:
        telegram_status = "shadow_stocks_context"
    elif late_entry:
        # Very-late entry: recorded for research/journal, never pushed as an
        # actionable alert (PART 5 late-entry shadow routing).
        telegram_status = "late_shadow"
    elif risk_guard_shadow:
        # Explicit paper-only circuit-breaker floor. This is intentionally
        # separate from the diagnostic warning status for auditability.
        telegram_status = "shadow_risk_guard"
    elif llm_review_shadow:
        # SI-6 advisory: fresh LLM reject/wait (or require_fresh+missing) → recorded, not pushed.
        telegram_status = "shadow_llm_review"
    elif crypto_overlay_shadow:
        # BLOCK is a Paper veto, not a Shadow experiment. Keep its audit record
        # separate so risk-off rejections do not appear as Shadow evidence.
        telegram_status = ("blocked_crypto_quality"
                           if str(payload.get("cqo_quality_action") or "").upper() == "BLOCK"
                           else "shadow_crypto_quality")
    elif dry_run:
        telegram_status = "dry_run"
    elif capture_status == "DUPLICATE":
        telegram_status = "live_duplicate"
    elif capture_status != "QUEUED":
        telegram_status = (
            "live_capture_error" if capture_status.startswith("error:")
            else "live_not_queued"
        )
    else:
        try:
            from src.notifiers.telegram_outbox import stage_alert
            staged_delivery = stage_alert(
                store,
                alert_id=alert_id,
                signal_id=signal_id,
                alert_type="paper_entry",
                asset_class=(signal.get("asset_class") or "crypto"),
                symbol=signal.get("symbol") or "?",
                tier=(signal.get("tier") or "?"),
                sent_at=sent_at,
                message=message,
                parse_mode="",
                mode=signal.get("mode"),
                score=float(signal.get("score") or 0),
                direction=signal.get("direction"),
                message_hash=message_hash,
                payload=payload,
            )
        except Exception as exc:
            return {
                "sent": False,
                "reason_skipped": "delivery_persistence_error",
                "payload": payload,
                "alert_id": alert_id,
                "telegram_status": f"persistence_error:{type(exc).__name__}",
                "message": message,
            }
        if not staged_delivery:
            return {
                "sent": False,
                "reason_skipped": "duplicate",
                "payload": payload,
                "alert_id": alert_id,
                "telegram_status": "duplicate",
                "message": message,
            }
        try:
            # Trading alerts use one short network attempt.  On failure the
            # durable outbox below retries independently; the tracker must not
            # wait through the notifier's normal 2 x 15 second retry path.
            fast_send_impl = getattr(type(notifier), "send_fast", None)
            if callable(fast_send_impl):
                fast_send_impl(notifier, message, parse_mode="")
            else:
                notifier.send(message, parse_mode="")  # test doubles / legacy notifier
            from src.notifiers.telegram_outbox import mark_sent
            mark_sent(store, alert_id=alert_id)
            telegram_status = "sent"
        except Exception as exc:
            telegram_status = f"queued:{type(exc).__name__}"
            try:
                from src.notifiers.telegram_outbox import mark_error
                mark_error(store, alert_id=alert_id, error=type(exc).__name__)
            except Exception:
                pass

    # Internal control field — not part of the persisted diagnostic payload.
    if not staged_delivery:
        try:
            store.record_signal_alert(
                alert_id=alert_id,
                signal_id=signal_id,
                asset_class=(signal.get("asset_class") or "crypto"),
                symbol=signal.get("symbol") or "?",
                tier=(signal.get("tier") or "?"),
                sent_at=sent_at,
                alert_type="paper_entry",
                mode=signal.get("mode"),
                score=float(signal.get("score") or 0),
                direction=signal.get("direction"),
                telegram_status=telegram_status,
                message_hash=message_hash,
                payload=payload,
            )
        except Exception:
            pass

    # Record the circuit-breaker dedupe marker (one per asset/mode/day/level) so the
    # would-pause warning is not repeated on the day's later entries. Best-effort.
    if cb_dedupe_key and telegram_status not in ("dry_run",):
        try:
            store.record_signal_alert(
                alert_id=str(uuid.uuid4()),
                signal_id=signal_id,
                asset_class=(signal.get("asset_class") or "crypto"),
                symbol=signal.get("symbol") or "?",
                tier=(signal.get("tier") or "?"),
                sent_at=sent_at,
                alert_type=cb_dedupe_key,
                mode=signal.get("mode"),
                direction=signal.get("direction"),
                telegram_status="diagnostic",
                payload={"diagnostic_only": True, "kind": "circuit_breaker_would_pause"},
            )
        except Exception:
            pass

    return {
        "sent": telegram_status == "sent",
        "reason_skipped": ("shadow_only" if shadow_only
                           else "c_tier_restricted" if c_tier_restricted
                           else "late_entry" if late_entry
                           else "risk_guard_shadow" if risk_guard_shadow
                           else "llm_review_shadow" if llm_review_shadow
                           else "crypto_overlay_shadow" if crypto_overlay_shadow
                           else "live_duplicate" if capture_status == "DUPLICATE"
                           else "live_not_queued" if capture_status != "QUEUED" and not dry_run
                           else None),
        "payload": payload,
        "alert_id": alert_id,
        "telegram_status": telegram_status,
        "message": message,
        "pre_capture_runtime_ms": pre_capture_runtime_ms,
        "live_capture_runtime_ms": live_capture_runtime_ms,
        "post_capture_runtime_ms": round(
            (time.perf_counter() - capture_started) * 1000.0 - live_capture_runtime_ms, 1),
    }
