"""Standard 'SETUP — WAITING FOR ENTRY' Telegram template.

Shared by both the crypto supervisor and the stocks monitor. Renders a
short, mobile-friendly setup-waiting message in plain text.

The legacy templates (`supervisor._format_idea_alert`, `format_stocks_alert`)
delegate here so the visible header / footer / disclaimer are identical
across asset classes.

Read-only with respect to scoring / TP / SL / sizing. Only template
formatting changes.
"""

from __future__ import annotations

from typing import Any

from src.notifiers.alert_headers import (
    DISCLAIMER_MANUAL_SHADOW,
    HEADER_SETUP_WAITING,
    HEADER_STOCKS_SETUP_NEW,
    HEADER_STOCKS_SETUP_ENTRY_CHANGE,
    HEADER_STOCKS_SETUP_SCORE_IMPROVEMENT,
    HEADER_STOCKS_SETUP_TIER_UPGRADE,
    HEADER_STOCKS_SETUP_INVALIDATION_CHANGE,
    MAX_SETUP,
    cap,
    fmt_price,
    tradingview_link,
)
from src.signals.playbooks import label_for
from src.signals.sizing import size_decision


STOCKS_HEADER_BY_ALERT_TYPE: dict[str, str] = {
    "new_signal": HEADER_STOCKS_SETUP_NEW,
    "entry_change": HEADER_STOCKS_SETUP_ENTRY_CHANGE,
    "score_improvement": HEADER_STOCKS_SETUP_SCORE_IMPROVEMENT,
    "tier_upgrade": HEADER_STOCKS_SETUP_TIER_UPGRADE,
    "invalidation_change": HEADER_STOCKS_SETUP_INVALIDATION_CHANGE,
}


def _short_rationale(signal: dict[str, Any]) -> str:
    """Single-line WHY: prefers `thesis` first sentence, else a generic note."""
    thesis = (signal.get("thesis") or "").strip()
    if thesis:
        first = thesis.split(".")[0].strip()
        if first and len(first) > 12:
            return first[:140]
    setup_type = (signal.get("setup_type") or "").strip()
    if setup_type:
        return f"{setup_type} setup"
    return "technical setup triggered"


def _risk_caution_line(signal: dict[str, Any]) -> str | None:
    """One-line risk caution if the signal hits a known weak cohort."""
    asset = (signal.get("asset_class") or "crypto").lower()
    mode = (signal.get("mode") or "").lower()
    tier = (signal.get("tier") or "").upper()
    direction = (signal.get("direction") or "").lower()
    try:
        pl = label_for(signal).playbook
    except Exception:
        pl = ""
    if pl == "crypto_scalp_momentum_continuation":
        return "⚠️ LOW-CONFIDENCE SCALP — paper only unless manually approved"
    if asset == "stocks" and pl == "stocks_intraday_rth_momentum" \
            and tier == "A" and direction == "long":
        return "⚠️ A-tier long caution — 0.5x only"
    if asset == "crypto" and mode == "intraday" and direction == "short" \
            and int(signal.get("news_supported") or 0) == 0:
        return "⚠️ NO-NEWS / NO-DERIV SHORT — historically weak edge"
    return None


def render_setup_alert(
    signal: dict[str, Any],
    *,
    stocks_subtype: str | None = None,
) -> str:
    """Render the standardized SETUP — WAITING FOR ENTRY message.

    Parameters
    ----------
    signal
        proposed_signals-shaped dict. Must include at least
        ``asset_class, symbol, direction, mode, tier, score, entry_low,
        entry_high, stop_loss, tp1`` and optionally ``primary_exchange,
        signal_id, thesis, setup_type, news_supported, raw_idea_json``.
    stocks_subtype
        For stocks: pass the decision alert_type so the header reflects
        the sub-type ("new_signal", "entry_change", ...). For crypto,
        pass None.

    Returns
    -------
    Plain-text message body. Must be sent with ``parse_mode=""``.
    """
    asset = (signal.get("asset_class") or "crypto").lower()
    symbol = signal.get("symbol") or "?"
    direction = (signal.get("direction") or "long").upper()
    tier = (signal.get("tier") or "?").upper()
    mode = (signal.get("mode") or "").lower()
    try:
        score = float(signal.get("score") or 0)
    except (TypeError, ValueError):
        score = 0.0
    try:
        pl = label_for(signal)
        playbook = pl.playbook
    except Exception:
        playbook = ""
    sized = size_decision(signal)
    size_weight = sized.weight
    size_label = f"{size_weight:g}x"

    entry_low = signal.get("entry_low")
    entry_high = signal.get("entry_high")
    if entry_low and entry_high:
        entry_str = f"{fmt_price(entry_low)}–{fmt_price(entry_high)}"
    else:
        entry_str = fmt_price(entry_low or entry_high or signal.get("entry_trigger"))
    stop_str = fmt_price(signal.get("stop_loss") or signal.get("invalidation"))
    tp1_str = fmt_price(signal.get("tp1"))
    tp2_str = fmt_price(signal.get("tp2"))
    tp3_str = fmt_price(signal.get("tp3"))

    # Header
    if asset == "stocks" and stocks_subtype:
        header = STOCKS_HEADER_BY_ALERT_TYPE.get(stocks_subtype, HEADER_STOCKS_SETUP_NEW)
    else:
        header = HEADER_SETUP_WAITING

    lines: list[str] = []
    lines.append(header)
    lines.append(f"{asset.upper()} {symbol} {direction}")
    lines.append("")
    lines.append(f"Playbook: {playbook or '—'}")
    lines.append(f"Tier/Score: {tier} / {score:g}")
    if mode:
        lines.append(f"Mode: {mode}")
    lines.append(f"Size if entered: {size_label}")
    caution = _risk_caution_line(signal)
    if caution:
        lines.append(caution)
    lines.append("")
    lines.append(f"Entry: {entry_str}")
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
    lines.append("Why:")
    lines.append(_short_rationale(signal))
    lines.append("")
    lines.append("Status:")
    lines.append("Waiting for price to reach entry.")
    lines.append("No paper entry yet.")
    lines.append(DISCLAIMER_MANUAL_SHADOW)
    lines.append("")
    sid = signal.get("signal_id") or ""
    if sid:
        lines.append(f"signal_id: {sid}")
    tv = tradingview_link(asset, symbol, signal.get("primary_exchange"))
    lines.append(f"TradingView: {tv}")
    return cap("\n".join(lines), MAX_SETUP)
