"""Telegram alert header constants + shared rendering helpers.

Single source of truth for every visible message header. All actionable
alerts MUST use one of these prefixes so the operator can tell at a glance
what kind of message they just received on their phone.

Design notes:
- Plain text everywhere. No Markdown — Telegram parse_mode="" is the only
  supported path because $, _, +/-, parens have repeatedly broken Markdown.
- Emoji prefixes are ASCII-safe single chars; never decorative-only.
- All headers begin with `[...]` so the operator's eye anchors there.
"""

from __future__ import annotations

from typing import Any

# ---- Setup alerts -------------------------------------------------------
HEADER_SETUP_WAITING = "[\U0001F7E1 SETUP — WAITING FOR ENTRY]"
HEADER_STOCKS_SETUP_NEW = "[\U0001F7E1 STOCKS SETUP — NEW SIGNAL]"
HEADER_STOCKS_SETUP_ENTRY_CHANGE = "[\U0001F7E1 STOCKS SETUP — ENTRY CHANGE]"
HEADER_STOCKS_SETUP_SCORE_IMPROVEMENT = "[\U0001F7E1 STOCKS SETUP — SCORE IMPROVEMENT]"
HEADER_STOCKS_SETUP_TIER_UPGRADE = "[\U0001F7E1 STOCKS SETUP — TIER UPGRADE]"
HEADER_STOCKS_SETUP_INVALIDATION_CHANGE = "[⚠️ STOCKS SETUP — INVALIDATION CHANGE]"

# ---- Paper-entry alerts --------------------------------------------------
HEADER_PAPER_ENTRY_LONG = "[\U0001F7E2 PAPER ENTRY — TRIGGERED]"
HEADER_PAPER_ENTRY_SHORT = "[\U0001F534 PAPER ENTRY — TRIGGERED]"

# ---- Close / outcome alerts ---------------------------------------------
HEADER_CLOSE_TP = "[✅ CLOSE — TP HIT]"
HEADER_CLOSE_STOP = "[❌ CLOSE — STOP HIT]"
HEADER_CLOSE_EXPIRED = "[⏳ CLOSE — EXPIRED]"
HEADER_CLOSE_FLAT = "[⚪ CLOSE — FLAT]"
HEADER_CLOSE_AMBIGUOUS = "[⚠️ CLOSE — AMBIGUOUS]"

# ---- Cancelled pending setup --------------------------------------------
HEADER_SETUP_CANCELLED = "[⚠️ SETUP — CANCELLED]"

# ---- Watchlist (not actionable) -----------------------------------------
HEADER_WATCHLIST = "[\U0001F440 WATCHLIST — NOT ACTIONABLE]"

# ---- Operator / digest summaries ----------------------------------------
HEADER_OPERATOR_SUMMARY = "[\U0001F9FE OPERATOR SUMMARY — NOT A TRADE]"
HEADER_DAILY_SUMMARY = "[\U0001F4CA DAILY SUMMARY]"

# Shared disclaimers
DISCLAIMER_MANUAL_SHADOW = "Manual shadow only — system did not place a real order."
DISCLAIMER_NOT_ACTIONABLE = "NOT ACTIONABLE — commentary only.\nNo paper entry recorded."

# Maximum character budgets (sanity caps, not hard cuts)
MAX_SETUP = 900
MAX_PAPER_ENTRY = 1100
MAX_CLOSE = 700
MAX_SUMMARY = 3000


def tradingview_link(asset_class: str, symbol: str, primary_exchange: str | None = None) -> str:
    """Single source of truth for TradingView URLs."""
    if (asset_class or "crypto").lower() == "crypto":
        venue = (primary_exchange or "binance").upper()
        bare = symbol.replace("/", "").replace("-", "")
        return f"https://www.tradingview.com/chart/?symbol={venue}:{bare}"
    return f"https://www.tradingview.com/chart/?symbol={symbol}"


def fmt_price(value: Any) -> str:
    """Compact price formatter: 2dp for >=100, 4dp for >=1, 6dp otherwise."""
    try:
        v = float(value)
    except (TypeError, ValueError):
        return "—"
    if abs(v) >= 100:
        return f"{v:.2f}"
    if abs(v) >= 1:
        return f"{v:.4f}"
    return f"{v:.6f}"


def operator_summary(body: str, *, title: str | None = None) -> str:
    """Wrap any operator-sent text with the standard header + disclaimer.

    Example::

        msg = operator_summary("Open trades: 1\\nToday R: +1.5", title="DAILY 2026-06-14")
        notifier.send(msg, parse_mode="")
    """
    parts = [HEADER_OPERATOR_SUMMARY, ""]
    if title:
        parts.append(title)
        parts.append("")
    parts.append(body.rstrip())
    parts.append("")
    parts.append(DISCLAIMER_NOT_ACTIONABLE)
    text = "\n".join(parts)
    if len(text) > MAX_SUMMARY:
        text = text[: MAX_SUMMARY - 16].rstrip() + "\n…(truncated)"
    return text


def cap(text: str, limit: int) -> str:
    """Trim to limit with a tail marker. No-op if already under budget."""
    if len(text) <= limit:
        return text
    return text[: limit - 16].rstrip() + "\n…(truncated)"
