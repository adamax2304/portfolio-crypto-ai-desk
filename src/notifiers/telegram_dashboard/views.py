"""Telegram-safe rendering for the read-only dashboard."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any


def _usd(value: Any) -> str:
    try:
        return f"${float(value or 0):+,.2f}"
    except (TypeError, ValueError):
        return "$0.00"


def _plain_usd(value: Any) -> str:
    try:
        return f"${float(value or 0):,.2f}"
    except (TypeError, ValueError):
        return "n/a"


def _pct(value: Any) -> str:
    return "n/a" if value is None else f"{float(value):.1f}%"


def _pnl_icon(value: Any) -> str:
    try:
        return "🟢" if float(value or 0) >= 0 else "🔴"
    except (TypeError, ValueError):
        return "⚪"


def _short_time(value: Any) -> str:
    if not value:
        return "n/a"
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed.astimezone(timezone.utc).strftime("%d %b %H:%M UTC")
    except (TypeError, ValueError):
        return str(value)[:16]


def _mode_key(item: dict[str, Any]) -> str:
    return f"{item['asset_class']}:{item['mode']}"


def _callback(value: str) -> str:
    """Telegram callback_data is capped at 64 bytes."""
    return value.encode("utf-8")[:64].decode("utf-8", errors="ignore")


def home(snapshot: dict[str, Any]) -> tuple[str, list[list[dict[str, str]]]]:
    paper = snapshot["paper"]
    shadow = snapshot["shadow"]
    positions = snapshot["positions"]
    balance = _plain_usd(paper["balance"])
    text = "\n".join([
        "🧭 AI DESK · CONTROL",
        "Read-only dashboard · no trading controls",
        "",
        f"💼 Paper equity  {balance}",
        f"{_pnl_icon(paper['week_pnl'])} 7D P/L {_usd(paper['week_pnl'])} · {paper['week_closed']} closed · WR {_pct(paper['week_winrate'])}",
        f"📌 Open positions  {len(positions)}",
        f"🔬 Shadow lanes  {len(shadow['lanes'])}",
        "",
        f"🕒 {_short_time(snapshot['generated_at'])}",
    ])
    keyboard = [
        [{"text": "📘 Paper", "callback_data": "td:paper"},
         {"text": "🔬 Shadow", "callback_data": "td:shadow"}],
        [{"text": "📌 Positions", "callback_data": "td:positions"},
         {"text": "🩺 Health", "callback_data": "td:health"}],
        [{"text": "🔄 Refresh", "callback_data": "td:home"}],
    ]
    return text, keyboard


def paper_overview(data: dict[str, Any]) -> tuple[str, list[list[dict[str, str]]]]:
    costs = data["costs"]
    lines = [
        "📘 PAPER · 7D",
        f"💼 Equity  {_plain_usd(data['balance'])}",
        f"{_pnl_icon(data['week_pnl'])} Net P/L {_usd(data['week_pnl'])} · {data['week_closed']} closed · WR {_pct(data['week_winrate'])}",
        f"💸 Costs  fee {_plain_usd(costs['fees'])} · slip {_plain_usd(costs['slippage'])} · funding {_plain_usd(costs['funding'])}",
        "",
        "🎯 BY ASSET / MODE",
    ]
    keyboard: list[list[dict[str, str]]] = []
    for item in data["by_mode"]:
        label = (f"{_pnl_icon(item['pnl'])} {item['asset_class'].upper()} · {item['mode']}  "
                 f"{_usd(item['pnl'])} · {item['closed']} closed · WR {_pct(item.get('winrate'))}")
        lines.append(label)
        keyboard.append([{
            "text": f"{item['asset_class'].title()} · {item['mode']}"[:48],
            "callback_data": _callback(f"td:pm:{_mode_key(item)}"),
        }])
    keyboard.extend([
        [{"text": "📜 Last 10 closed", "callback_data": "td:pt:0"}],
        [{"text": "🏠 Home", "callback_data": "td:home"}],
    ])
    return "\n".join(lines), keyboard


def paper_trades(data: dict[str, Any], *, page: int, page_size: int,
                 title: str = "📜 PAPER · LAST 10 CLOSED") -> tuple[str, list[list[dict[str, str]]]]:
    window = "All history" if data["days"] is None else f"Last {data['days']}D"
    lines = [title, f"{window} · {data['total']} closed total", ""]
    if not data["rows"]:
        lines.append("⚪ No closed trades in this period.")
    for row in data["rows"]:
        pnl = row.get("net_pnl_usdt")
        lines.append(
            f"{_pnl_icon(pnl)} {_short_time(row.get('exit_at') or row.get('timestamp'))} · "
            f"{row.get('symbol', '?')} · {str(row.get('direction', '?')).upper()} · {row.get('mode', '?')}\n"
            f"   P/L {_usd(pnl)} · {row.get('close_reason') or 'n/a'}"
        )
    keyboard: list[list[dict[str, str]]] = []
    navigation: list[dict[str, str]] = []
    if page > 0:
        navigation.append({"text": "◀ Previous", "callback_data": _callback(f"td:pt:{page - 1}")})
    if (page + 1) * page_size < data["total"]:
        navigation.append({"text": "Next ▶", "callback_data": _callback(f"td:pt:{page + 1}")})
    if navigation:
        keyboard.append(navigation)
    keyboard.append([{"text": "📘 Paper", "callback_data": "td:paper"},
                     {"text": "🏠 Home", "callback_data": "td:home"}])
    return "\n".join(lines), keyboard


def shadow_overview(data: dict[str, Any]) -> tuple[str, list[list[dict[str, str]]]]:
    lines = ["🔬 SHADOW · ISOLATED EVIDENCE", "No lane is auto-promoted from this screen.", ""]
    keyboard: list[list[dict[str, str]]] = []
    if not data["lanes"]:
        lines.append("⚪ No Shadow evaluations available yet.")
    for item in data["lanes"]:
        lines.append(
            f"🧪 {item['label']}\n"
            f"   Raw {item['raw_closed']} · P/L {_usd(item['raw_pnl'])} | "
            f"Clean {item['clean_closed']} · evidence {_usd(item['pnl'])} · PF {item.get('profit_factor') or 'n/a'}\n"
            f"   Verdict: {item['verdict']}"
        )
        if item.get("dirty_closed") or item.get("unclassified_closed"):
            lines.append(
                f"   ⚠ Excluded: dirty {item.get('dirty_closed', 0)} / {_usd(item.get('dirty_pnl'))}; "
                f"unclassified {item.get('unclassified_closed', 0)} / {_usd(item.get('unclassified_pnl'))}"
            )
        digest = hashlib.sha1(item["key"].encode("utf-8")).hexdigest()[:12]
        keyboard.append([{
            "text": f"🧪 {item['label']}"[:48],
            "callback_data": f"td:sh:{digest}",
        }])
    keyboard.append([{"text": "🏠 Home", "callback_data": "td:home"}])
    return "\n".join(lines), keyboard


def shadow_detail(data: dict[str, Any]) -> tuple[str, list[list[dict[str, str]]]]:
    summary = data.get("summary")
    if not summary:
        return "⚪ Shadow lane is no longer available.", [[{"text": "🔬 Shadow", "callback_data": "td:shadow"}]]
    lines = [
        f"🔬 SHADOW · {summary['label']}",
        f"📊 Rows {summary['forward_rows']} · raw {summary['raw_closed']} · raw P/L {_usd(summary['raw_pnl'])}",
        f"✅ Clean {summary['clean_closed']} · evidence {_usd(summary['pnl'])} · dirty rows {summary['dirty_rows']}",
        f"⚠ Excluded: dirty {summary.get('dirty_closed', 0)} / {_usd(summary.get('dirty_pnl'))}; "
        f"unclassified {summary.get('unclassified_closed', 0)} / {_usd(summary.get('unclassified_pnl'))}",
        f"📈 WR {_pct(summary.get('winrate'))} · PF {summary.get('profit_factor') or 'n/a'}",
        f"🏷 Verdict: {summary['verdict']}", "", "📜 LATEST 10 CANDIDATES / OUTCOMES",
    ]
    if not data["rows"]:
        lines.append("⚪ No candidate rows recorded yet.")
    for row in data["rows"]:
        reason = row.get("close_reason") or row.get("rejection_reason") or row.get("outcome_status") or "pending"
        lines.append(
            f"{_pnl_icon(row.get('net_pnl_usd'))} {_short_time(row.get('exit_ts') or row.get('decision_at'))} · "
            f"{row.get('symbol', '?')} · {str(row.get('direction', '?')).upper()}\n"
            f"   P/L {_usd(row.get('net_pnl_usd'))} · {reason}"
        )
    return "\n".join(lines), [[{"text": "🔬 Shadow", "callback_data": "td:shadow"},
                                  {"text": "🏠 Home", "callback_data": "td:home"}]]


def positions(rows: list[dict[str, Any]]) -> tuple[str, list[list[dict[str, str]]]]:
    lines = ["📌 OPEN POSITIONS", ""]
    if not rows:
        lines.append("⚪ No open Paper or tracked Shadow position.")
    for row in rows:
        unrealized = row.get("unrealized_pnl_usd")
        extra = f" | uPnL {_usd(unrealized)}" if unrealized is not None else ""
        lines.append(
            f"• {row.get('symbol', '?')} · {str(row.get('direction', '?')).upper()} · {row.get('mode', '?')}\n"
            f"  Entry {_short_time(row.get('entry_at'))} · stop {row.get('stop_initial') or 'n/a'}{extra}"
        )
    return "\n".join(lines), [[{"text": "🏠 Home", "callback_data": "td:home"}]]


def health(data: dict[str, Any]) -> tuple[str, list[list[dict[str, str]]]]:
    lines = ["🩺 SYSTEM HEALTH · READ MODEL", ""]
    for item in data["freshness"]:
        lines.append(f"🕒 {item['label']}: {_short_time(item['latest'])}")
    for item in data["data_quality"]:
        lines.append(
            f"📊 {item['label']}: clean {item.get('clean') or 0} · dirty {item.get('dirty') or 0} · "
            f"unknown {item.get('unknown') or 0}"
        )
    live = data.get("mexc_live")
    if live:
        heartbeat = live.get("heartbeat") or {}
        lines.append(
            f"MEXC live: pending {live.get('pending', 0)} · submitted {live.get('submitted', 0)} · "
            f"preflight rejected {live.get('rejected_preflight', 0)}"
        )
        lines.append(f"  monitor: {heartbeat.get('status') or 'unknown'} · {_short_time(heartbeat.get('updated_at'))}")
    lines.extend(["", "🔒 Dashboard is read-only: guards, Paper, and Live are unchanged."])
    return "\n".join(lines), [[{"text": "🏠 Home", "callback_data": "td:home"}]]


def fingerprint(text: str, keyboard: list[list[dict[str, str]]]) -> str:
    encoded = json.dumps({"text": text, "keyboard": keyboard}, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()
