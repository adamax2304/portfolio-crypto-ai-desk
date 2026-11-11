"""Close / outcome Telegram alert (new).

Fires exactly once when a triggered A/B signal transitions to a terminal
outcome (win / loss / expired / ambiguous). Mirrors the design of
``src/notifiers/paper_entry.py``:

  * Eligibility gates (tier, asset+mode, playbook).
  * Dedup via ``signal_alerts.alert_type`` ∈
    {close_tp, close_stop, close_expired, close_flat, close_ambiguous}.
  * Plain text, mobile-friendly.

No production behavior changes besides recording one extra Telegram message
per signal when it actually closes. Never sends for setup-only signals that
did NOT enter; never sends for C-tier / shadow / stocks swing/invest paused.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from src.notifiers.alert_headers import (
    DISCLAIMER_MANUAL_SHADOW,
    HEADER_CLOSE_AMBIGUOUS,
    HEADER_CLOSE_EXPIRED,
    HEADER_CLOSE_FLAT,
    HEADER_CLOSE_STOP,
    HEADER_CLOSE_TP,
    MAX_CLOSE,
    cap,
    fmt_price,
)
from src.signals.playbooks import label_for
from src.signals.sizing import size_decision


PLAYBOOKS_FORBIDDEN_FOR_CLOSE_ALERT = {
    "stocks_swing_watchlist_rs_rotation",
    "stocks_invest_watchlist_30d_thesis",
}

OUTCOME_TO_ALERT_TYPE: dict[str, str] = {
    "win": "close_tp",
    "loss": "close_stop",
    "expired": "close_expired",
    "ambiguous": "close_ambiguous",
}

# proposed_signals.status values that mean the trade already closed in a
# PRIOR tracker cycle. A close alert must only fire on the *transition* into
# a terminal state — if the previous status is already terminal, this is a
# re-evaluation of an old trade, NOT a fresh close, and must be skipped.
# (2026-06-15 fix: prevents the historical-backfill flood on deploy/restart.)
TERMINAL_STATUSES = {
    "tp3_hit", "stopped", "expired",
    "missed_no_entry", "ambiguous", "invalidated_before_entry",
    "stale_before_entry", "entry_moved_away",
}

# Defensive backstop: never alert a "close" for a signal created more than
# this many days ago, even if dedup state is lost. Generous enough to cover
# multi-day swing trades.
MAX_CLOSE_AGE_DAYS = 4

OUTCOME_TO_HEADER: dict[str, str] = {
    "win": HEADER_CLOSE_TP,
    "loss": HEADER_CLOSE_STOP,
    "expired": HEADER_CLOSE_EXPIRED,
    "ambiguous": HEADER_CLOSE_AMBIGUOUS,
    "flat": HEADER_CLOSE_FLAT,
}


@dataclass
class CloseDecision:
    should_send: bool
    reason_skipped: str = ""
    message: str = ""
    alert_type: str = ""
    payload: dict[str, Any] | None = None


def _hold_duration(entry_at: str | None, exit_at: str | None) -> str:
    if not entry_at or not exit_at:
        return "—"
    try:
        a = datetime.fromisoformat(str(entry_at).replace("Z", "+00:00"))
        b = datetime.fromisoformat(str(exit_at).replace("Z", "+00:00"))
    except Exception:
        return "—"
    delta = b - a
    secs = int(delta.total_seconds())
    if secs < 0:
        return "—"
    days = secs // 86400
    hours = (secs % 86400) // 3600
    mins = (secs % 3600) // 60
    if days >= 1:
        return f"{days}d {hours}h"
    if hours >= 1:
        return f"{hours}h {mins:02d}m"
    return f"{mins}m"


def _which_tp(signal: dict[str, Any], outcome_row: dict[str, Any]) -> tuple[str, float | None]:
    """Identify which TP got hit. Returns (label, price)."""
    for key, label in (("tp3_hit", "TP3"), ("tp2_hit", "TP2"), ("tp1_hit", "TP1")):
        if int(outcome_row.get(key) or 0) == 1:
            return label, signal.get(label.lower())
    return "TP1", signal.get("tp1")


def decide_close(
    signal: dict[str, Any],
    outcome_row: dict[str, Any],
    *,
    prev_status: str | None = None,
    prev_final_outcome: str | None = None,
) -> CloseDecision:
    """Decide whether to send a close alert.

    Transition guard (primary): ``prev_status`` is ``proposed_signals.status``
    BEFORE this tracker tick. If it is already a terminal status, the trade
    closed in a prior cycle — this is a re-evaluation, not a fresh close, so
    we skip. This is what prevents the historical-backfill flood when the
    feature (or the dedup table) is deployed/reset.

    ``prev_final_outcome`` is kept for backwards compatibility with direct
    callers/tests; if it already equals the new outcome we also skip.
    """
    new_outcome = (outcome_row.get("final_outcome") or "").strip()
    terminal_status = str(outcome_row.get("status") or "").lower().strip()
    if terminal_status in {"tp1_hit", "tp2_hit"}:
        return CloseDecision(False, reason_skipped=f"{terminal_status} is an open-position milestone")
    if (new_outcome == "win" and terminal_status not in {"tp3_hit", "stopped", "ambiguous"}
            and not outcome_row.get("tp3_hit") and not outcome_row.get("stop_hit")):
        return CloseDecision(False, reason_skipped="TP1/TP2 touch is an open-position milestone")
    if not new_outcome:
        return CloseDecision(False, reason_skipped="no final outcome")
    if new_outcome not in OUTCOME_TO_ALERT_TYPE:
        return CloseDecision(False, reason_skipped=f"outcome {new_outcome} is non-terminal")
    if prev_final_outcome is not None and prev_final_outcome == new_outcome:
        return CloseDecision(False, reason_skipped="outcome already alerted")
    # Transition guard — skip if the trade was ALREADY closed in a prior cycle.
    norm_prev = (prev_status or "").lower().strip()
    if norm_prev in TERMINAL_STATUSES:
        return CloseDecision(
            False,
            reason_skipped=f"already closed in prior cycle (prev_status={norm_prev})",
        )
    # Defensive age backstop — never alert a stale historical close.
    created_at = signal.get("created_at")
    if created_at:
        try:
            from datetime import datetime, timezone, timedelta
            c = datetime.fromisoformat(str(created_at).replace("Z", "+00:00"))
            if c.tzinfo is None:
                c = c.replace(tzinfo=timezone.utc)
            age_days = (datetime.now(timezone.utc) - c).total_seconds() / 86400
            if age_days > MAX_CLOSE_AGE_DAYS:
                return CloseDecision(
                    False,
                    reason_skipped=f"signal too old ({age_days:.1f}d > {MAX_CLOSE_AGE_DAYS}d) — backfill guard",
                )
        except Exception:
            pass
    # MUST have entered
    if int(outcome_row.get("entry_triggered") or 0) != 1:
        return CloseDecision(False, reason_skipped="never entered — no close alert for setup-only")
    # Tier gate
    tier = (signal.get("tier") or "").upper()
    if tier not in {"A", "B"}:
        return CloseDecision(False, reason_skipped=f"tier={tier} not actionable")
    # Asset/mode gate
    asset = (signal.get("asset_class") or "crypto").lower()
    mode = (signal.get("mode") or "").lower()
    if asset == "stocks" and mode in {"swing", "invest"}:
        return CloseDecision(False, reason_skipped="stocks swing/invest paper-paused")
    # Playbook gate
    try:
        pl = label_for(signal)
    except Exception:
        pl = None
    if pl is not None:
        if pl.playbook in PLAYBOOKS_FORBIDDEN_FOR_CLOSE_ALERT:
            return CloseDecision(False, reason_skipped=f"playbook {pl.playbook} paused")
        if getattr(pl, "status", "") == "watchlist_only":
            return CloseDecision(False, reason_skipped="watchlist-only playbook")
    status_alert_type = {
        "tp3_hit": "close_tp", "stopped": "close_stop",
        "expired": "close_expired", "ambiguous": "close_ambiguous",
    }
    alert_type = status_alert_type.get(terminal_status, OUTCOME_TO_ALERT_TYPE[new_outcome])

    # Resolve the authoritative Model-F close once. Legacy final_outcome/final_r
    # remains visible for diagnostics but no longer decides whether a stopped
    # runner is announced as TP or stop.
    try:
        from src.execution.paper_execution_accounting import build_record_from_signal
        accounting_outcome = dict(outcome_row)
        if not terminal_status and new_outcome in {"expired", "ambiguous"}:
            accounting_outcome["status"] = new_outcome
        _, _, paper_exec = build_record_from_signal(signal, accounting_outcome)
    except Exception:
        paper_exec = {}
    display_outcome = str(paper_exec.get("paper_execution_outcome") or new_outcome)

    # Build payload
    direction = (signal.get("direction") or "long").upper()
    symbol = signal.get("symbol") or "?"
    raw_r = outcome_row.get("final_r")
    try:
        raw_r_f = float(raw_r) if raw_r is not None else 0.0
    except (TypeError, ValueError):
        raw_r_f = 0.0
    sized = size_decision({**signal, "final_r": raw_r_f})
    sized_r = sized.sized_r if sized.sized_r is not None else 0.0

    entry_at = outcome_row.get("entry_triggered_at") or signal.get("entry_triggered_at")
    exit_at = (paper_exec.get("exit_at") or
               (outcome_row.get("stop_hit_at") if terminal_status == "stopped" else
                outcome_row.get("tp3_hit_at") if terminal_status == "tp3_hit" else
                outcome_row.get("checked_at")))
    hold = _hold_duration(entry_at, exit_at)

    header = (HEADER_CLOSE_STOP if terminal_status == "stopped" else
              OUTCOME_TO_HEADER.get(display_outcome, HEADER_CLOSE_FLAT))
    lines: list[str] = []
    lines.append(header)
    lines.append(f"{asset.upper()} {symbol} {direction}")
    lines.append("")
    # Lifecycle-aware Result wording. Dedup is by (signal_id, alert_type) — NOT by
    # message text — so this wording change can never cause a resend of an already
    # sent / historical close alert. `:+.1f` also guarantees no "+-" can appear.
    contradiction = (
        (new_outcome == "win" and raw_r_f < 0) or (new_outcome == "loss" and raw_r_f > 0)
    )
    # The AUTHORITATIVE result is the paper-execution R (Model F) + paper USD net shown below.
    # The legacy touch `final_r` (highest TP touched) is OPTIMISTIC and is NEVER the headline PnL.
    if display_outcome == "expired":
        lines.append("Result: 0R — unresolved (entered, no TP/SL before validity window)")
    elif display_outcome == "ambiguous":
        lines.append("Result: ambiguous — see Paper exec R (Model F) + Paper $ net below")
    elif raw_r_f == 0.0:
        lines.append("Result: CLOSED FLAT 0R")
    else:
        lines.append("Result: see Paper exec R (Model F) + Paper $ net below")
    lines.append(f"(legacy touch {raw_r_f:+.1f}R = highest TP touched · optimistic · NOT PnL)")
    if contradiction:
        lines.append("⚠ data check: outcome label vs R sign mismatch")
    if terminal_status == "tp3_hit":
        tp_label, tp_price = _which_tp(signal, outcome_row)
        lines.append(f"Exit: {tp_label} {fmt_price(tp_price)}")
    elif terminal_status == "stopped":
        label = str(paper_exec.get("close_reason") or "stop").replace("_", " ")
        lines.append(f"Exit: {label} (Model F)")
    elif display_outcome == "loss":
        lines.append(f"Exit: Stop {fmt_price(signal.get('stop_loss') or signal.get('invalidation'))}")
    elif display_outcome == "expired":
        lines.append("Reason: No TP/stop before validity window ended.")
    elif display_outcome == "ambiguous":
        lines.append("Reason: Same-candle TP+stop touch; resolved conservatively.")
    # Paper execution accounting (Model F) — honest paper PnL beside the
    # touch-based number above. The "Result" line is the legacy highest-TP-touched
    # value (optimistic). PAPER/ACCOUNTING ONLY; fail-open so a compute error
    # never blocks the alert. No live orders.
    try:
        _pe = paper_exec
        _pe_r = _pe.get("paper_execution_r")
        if _pe_r is not None:
            _prot = ("lock +0.5R @ +1R" if _pe.get("lock_armed")
                     else "BE @ +0.6R" if _pe.get("protection_armed") else "")
            lines.append(f"Paper exec R (Model F): {_pe_r:+.1f}R" + (f" · {_prot}" if _prot else ""))
            if _pe.get("close_reason") in ("breakeven_stop", "profit_lock_stop"):
                lines.append("Closed at protected stop, not the touched TP.")
            # Paper portfolio USD line: $5000 deposit, 0.5% risk, dynamic leverage,
            # net of fees. PAPER/ACCOUNTING ONLY; fail-open. Uses initial equity
            # (live equity not tracked per-tick in this alert path).
            try:
                from src.execution.paper_portfolio import load_cfg
                from src.execution.position_sizing import size_position
                from src.execution.fees import trade_costs
                def _tf(v):
                    try:
                        return None if v in (None, "") else float(v)
                    except (TypeError, ValueError):
                        return None
                _cfg = load_cfg()
                _entry = (_tf(signal.get("entry_trigger")) or _tf(signal.get("suggested_entry"))
                          or _tf(signal.get("entry_low")))
                _stop = _tf(signal.get("invalidation")) or _tf(signal.get("stop_loss"))
                if _entry and _stop and abs(_entry - _stop) > 0:
                    _sz = size_position(equity_usdt=float(_cfg["initial_equity_usdt"]),
                                        entry_price=_entry, stop_price=_stop,
                                        direction=str(signal.get("direction") or "long"),
                                        risk_pct=float(_cfg["risk_per_trade_pct"]),
                                        max_leverage=int(_cfg["max_leverage"]),
                                        max_margin_pct=float(_cfg["max_margin_per_trade_pct"]),
                                        max_notional_pct=float(_cfg["max_notional_per_trade_pct"]))
                    _long = str(signal.get("direction") or "long").lower() != "short"
                    _risk = abs(_entry - _stop)
                    # maker-first paper execution plan + structural TP label (PAPER ONLY)
                    from src.execution.maker_first_execution import plan_for as _plan_for
                    from src.execution.structural_tp_engine import generate_structural_tps as _gen_stp
                    _pb = str(signal.get("setup_type") or "")
                    _is_pull = any(k in _pb.lower() for k in ("swing", "failed_bounce", "retest", "pullback", "bounce"))
                    _plan = _plan_for(playbook=_pb, setup_is_pullback=_is_pull, is_urgent=not _is_pull,
                                       reached_tp=_pe_r > 0, expired=(str(display_outcome) == "expired"),
                                       invalid_or_stale=(terminal_status == "stopped"))
                    _stp = _gen_stp(entry=_entry, stop=_stop, direction=str(signal.get("direction") or "long"),
                                    candles=None, atr=_risk, market_regime=str(signal.get("market_regime") or ""),
                                    playbook=_pb)
                    # taker baseline vs maker-first
                    _cost = trade_costs(notional_usdt=_sz.notional_usdt, exit_notional_usdt=_sz.notional_usdt,
                                        symbol=str(signal.get("symbol") or ""), fee_profile=str(_cfg["fee_profile"]),
                                        slip_cfg=_cfg.get("default_slippage"), majors=_cfg.get("majors"))
                    _cost_mf = trade_costs(notional_usdt=_sz.notional_usdt, exit_notional_usdt=_sz.notional_usdt,
                                           symbol=str(signal.get("symbol") or ""), fee_profile=str(_cfg["fee_profile"]),
                                           entry_order_type=_plan.entry_order_type, exit_order_type=_plan.exit_order_type,
                                           slip_cfg=_cfg.get("default_slippage"), majors=_cfg.get("majors"))
                    _net = _pe_r * _sz.actual_risk_usdt - _cost_mf.total_cost_usdt
                    _saved = (_cost.fee_usdt + _cost.slippage_usdt) - (_cost_mf.fee_usdt + _cost_mf.slippage_usdt)
                    lines.append(
                        f"Paper $: net {_net:+.1f} (risk ${_sz.actual_risk_usdt:.0f}/0.5%, "
                        f"{_sz.leverage_used}x≤2x, fees ${_cost_mf.fee_usdt + _cost_mf.slippage_usdt:.1f}"
                        f"{f', saved ${_saved:.1f} vs taker' if _saved > 0.01 else ''})")
                    lines.append(
                        f"Paper exec: {_plan.entry_order_type}E/{_plan.exit_order_type}X (stop taker) · "
                        f"TP {_stp.tp_set_label}")
                    # Exact TP R-multiples (NOT "+1R" by name) + TP quality.
                    def _tpr(tp):
                        v = _tf(tp)
                        if v is None or _risk <= 0:
                            return "—"
                        return f"{((v - _entry) if _long else (_entry - v)) / _risk:.1f}R"
                    lines.append(
                        f"TPs (exact R): {_tpr(signal.get('tp1'))}/{_tpr(signal.get('tp2'))}/"
                        f"{_tpr(signal.get('tp3'))} · prod MECHANICAL_ATR · paper TP=structural/maker-first")
            except Exception:
                pass
    except Exception:
        pass
    lines.append(f"Hold: {hold}")
    # Informational only: the same read-only snapshot used by setup and
    # Paper-entry alerts. It cannot change a closed outcome or any routing.
    try:
        from src.notifiers.derivatives_context import telegram_lines
        deriv_lines, deriv_payload = telegram_lines(signal)
        lines.extend(deriv_lines)
    except Exception:
        deriv_payload = {"source": "unavailable"}
    lines.append("")
    lines.append(f"Playbook: {pl.playbook if pl else '—'}")
    sid = signal.get("signal_id") or ""
    if sid:
        lines.append(f"signal_id: {sid}")
    lines.append("")
    lines.append(DISCLAIMER_MANUAL_SHADOW)

    message = cap("\n".join(lines), MAX_CLOSE)
    payload = {
        "signal_id": sid,
        "symbol": symbol,
        "asset_class": asset,
        "tier": tier,
        "outcome": new_outcome,
        "paper_execution_outcome": display_outcome,
        "terminal_status": terminal_status,
        "raw_r": raw_r_f,
        "sized_r": sized_r,
        "playbook": pl.playbook if pl else "",
        "entry_triggered_at": entry_at,
        "exit_at": exit_at,
        "hold": hold,
        "derivatives_at_alert": deriv_payload,
    }
    return CloseDecision(True, message=message, alert_type=alert_type, payload=payload)


def has_existing_close_alert(store: Any, signal_id: str, alert_type: str = "") -> bool:
    try:
        with store.connect() as conn:
            row = conn.execute(
                "SELECT 1 FROM signal_alerts WHERE signal_id = ? AND alert_type LIKE 'close_%' LIMIT 1",
                (signal_id,),
            ).fetchone()
        return row is not None
    except Exception:
        return False


def _entry_alert_lineage(store: Any, signal_id: str) -> dict[str, Any] | None:
    """Read whether the latest matching Paper entry was accepted by live handoff."""
    try:
        with store.connect() as conn:
            row = conn.execute(
                "SELECT telegram_status,payload_json,sent_at FROM signal_alerts "
                "WHERE signal_id=? AND alert_type='paper_entry' "
                "ORDER BY sent_at DESC,rowid DESC LIMIT 1",
                (signal_id,),
            ).fetchone()
        if row is None:
            return None
        try:
            entry_payload = json.loads(str(row[1] or "{}"))
        except (TypeError, json.JSONDecodeError):
            entry_payload = {}
        telegram_status = str(row[0] or "")
        telegram_channel = str(entry_payload.get("telegram_channel") or "")
        capture_status = str(entry_payload.get("mexc_canary_capture_status") or "").upper()
        live_routed = (
            telegram_channel in {"live_handoff", "live_duplicate"}
            or (telegram_channel == "telegram" and capture_status in {"QUEUED", "DUPLICATE"})
            or capture_status in {"QUEUED", "DUPLICATE"}
        )
        return {
            "telegram_status": telegram_status,
            "telegram_channel": telegram_channel or None,
            "mexc_canary_capture_status": capture_status or None,
            "sent_at": str(row[2] or ""),
            "operator_visible": bool(live_routed and entry_payload.get("paper_entry_dry_run") is not True),
        }
    except Exception:
        return None


def _compact_live_close_message(signal: dict[str, Any], payload: dict[str, Any]) -> str:
    status = str(payload.get("terminal_status") or payload.get("outcome") or "").lower()
    outcome = str(payload.get("paper_execution_outcome") or payload.get("outcome") or "").lower()
    if status == "stopped" or outcome == "loss":
        emoji = "❌"
    elif outcome == "expired":
        emoji = "⏳"
    elif outcome == "ambiguous":
        emoji = "⚠️"
    elif outcome == "flat":
        emoji = "⚪"
    else:
        emoji = "✅"
    symbol = str(payload.get("symbol") or signal.get("symbol") or "?").replace("_", "/")
    direction = str(signal.get("direction") or "").upper()
    asset = str(payload.get("asset_class") or signal.get("asset_class") or "crypto").upper()
    try:
        sized_r = float(payload.get("sized_r") or 0.0)
        r_line = f"{sized_r:+.2f}R"
    except (TypeError, ValueError):
        r_line = "—"
    sid = str(payload.get("signal_id") or signal.get("signal_id") or "")
    return cap("\n".join([
        f"{emoji} LIVE ROUTE CLOSE",
        f"{symbol} {direction} · {asset}",
        "",
        f"📊 Result: {r_line} · {outcome or status or 'closed'}",
        f"🚪 Exit: {status or 'closed'}",
        f"⏱ Hold: {payload.get('hold') or '—'}",
        f"🆔 {sid[:8] if sid else '—'}",
        "",
        "Paper model close for a live-routed entry.",
    ]), 420)


def send_close_alert(
    *,
    store: Any,
    notifier: Any,
    signal: dict[str, Any],
    outcome_row: dict[str, Any],
    prev_status: str | None = None,
    prev_final_outcome: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """High-level entry point — analogous to ``send_paper_entry_alert``."""
    sid = signal.get("signal_id") or ""
    decision = decide_close(
        signal, outcome_row,
        prev_status=prev_status,
        prev_final_outcome=prev_final_outcome,
    )
    if not decision.should_send:
        return {"sent": False, "reason_skipped": decision.reason_skipped,
                "alert_type": "", "payload": None}

    if has_existing_close_alert(store, sid, decision.alert_type):
        return {"sent": False, "reason_skipped": "duplicate close alert",
                "alert_type": decision.alert_type, "payload": None}

    alert_id = str(uuid.uuid4())
    sent_at = datetime.now(timezone.utc).isoformat()

    # 2026-06-15 scalp downgrade: crypto scalp is SHADOW ONLY — close alerts are
    # recorded but not pushed to the operator (mirrors paper-entry routing).
    from src.notifiers.paper_entry import is_shadow_only_scalp
    entry_lineage = _entry_alert_lineage(store, sid)
    shadow_only = (
        is_shadow_only_scalp(signal)
        or entry_lineage is None
        or not bool(entry_lineage["operator_visible"])
    )
    message = decision.message
    payload = dict(decision.payload or {})
    payload["entry_alert_lineage"] = entry_lineage
    if shadow_only:
        message = ("[SHADOW ONLY - ENTRY WAS NOT OPERATOR-ACTIONABLE]\n"
                   "Research lifecycle only.\n\n" + message)
        payload["telegram_channel"] = "shadow_only"
    else:
        payload["telegram_channel"] = "live_handoff_close"
        message = _compact_live_close_message(signal, payload)
    message_hash = hashlib.sha256(message.encode("utf-8")).hexdigest()[:16]

    if shadow_only:
        telegram_status = "shadow_only"
    elif dry_run:
        telegram_status = "dry_run"
    else:
        try:
            notifier.send(message, parse_mode="")
            telegram_status = "sent"
        except Exception as exc:
            telegram_status = f"error:{type(exc).__name__}"

    try:
        store.record_signal_alert(
            alert_id=alert_id,
            signal_id=sid,
            asset_class=(signal.get("asset_class") or "crypto"),
            symbol=signal.get("symbol") or "?",
            tier=(signal.get("tier") or "?"),
            sent_at=sent_at,
            alert_type=decision.alert_type,
            mode=signal.get("mode"),
            score=float(signal.get("score") or 0),
            direction=signal.get("direction"),
            telegram_status=telegram_status,
            message_hash=message_hash,
            payload=payload,
        )
    except Exception:
        pass

    if str(telegram_status).startswith("error:"):
        try:
            from src.notifiers.telegram_outbox import enqueue
            enqueue(store, alert_id=alert_id, signal_id=sid,
                    alert_type=decision.alert_type, message=message,
                    parse_mode="", error=telegram_status)
        except Exception:
            pass

    return {
        "sent": telegram_status == "sent",
        "reason_skipped": "shadow_only" if shadow_only else None,
        "alert_type": decision.alert_type,
        "telegram_status": telegram_status,
        "payload": payload,
        "alert_id": alert_id,
        "message": message,
    }
