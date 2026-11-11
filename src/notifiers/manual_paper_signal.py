"""Short, deduplicated Telegram notices for explicitly selected Paper entries."""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
import math
from pathlib import Path
from typing import Any

import pandas as pd

from src.notifiers.telegram_outbox import mark_error, mark_sent, stage_alert
from src.storage.sqlite import SQLiteStore


def _parse_time(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _price(value: Any, asset_class: str) -> str:
    number = float(value)
    if asset_class == "stocks":
        return f"${number:,.2f}"
    if abs(number) >= 1000:
        return f"${number:,.2f}"
    if abs(number) >= 1:
        return f"${number:.4f}".rstrip("0").rstrip(".")
    if abs(number) >= 0.01:
        return f"${number:.6f}".rstrip("0").rstrip(".")
    return f"${number:.9f}".rstrip("0").rstrip(".")


def latest_closed_minute(frame: Any, *, now: datetime) -> tuple[float, datetime] | None:
    """Return the newest closed 1m close and its close timestamp."""
    if frame is None or getattr(frame, "empty", True):
        return None
    if "timestamp" not in frame or "close" not in frame:
        return None
    now_utc = _parse_time(now)
    if now_utc is None:
        return None
    stamps = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")
    mask = stamps + pd.Timedelta(minutes=1) <= pd.Timestamp(now_utc)
    closed = frame.assign(_manual_bar_start=stamps).loc[mask].sort_values("_manual_bar_start")
    if closed.empty:
        return None
    row = closed.iloc[-1]
    try:
        price = float(row["close"])
        bar_start = _parse_time(row["timestamp"])
    except (TypeError, ValueError, KeyError):
        return None
    if not math.isfinite(price) or price <= 0 or bar_start is None:
        return None
    return price, bar_start + timedelta(minutes=1)


def render_manual_paper_entry(*, asset_class: str, symbol: str, direction: str,
                              title: str, reference_price: float,
                              reference_at: datetime, variants: list[dict[str, Any]],
                              now: datetime) -> str:
    asset = "АКЦИИ" if asset_class == "stocks" else "КРИПТА"
    side = str(direction or "long").upper()
    emoji = "🟢" if side == "LONG" else "🔴"
    now_utc = _parse_time(now) or datetime.now(timezone.utc)
    reference_at = _parse_time(reference_at) or now_utc
    ref_age = max(0, int((now_utc - reference_at).total_seconds()))
    lines = [f"{emoji} {asset} · PAPER СИГНАЛ", f"{symbol} · {side} · {title}"]
    lines.append(f"Рынок ≈ {_price(reference_price, asset_class)} · 1m close {ref_age}с")
    for variant in variants:
        label = str(variant.get("label") or "Paper")
        lines.append(
            f"{label}: вход {_price(variant['entry'], asset_class)} · "
            f"стоп {_price(variant['stop'], asset_class)} · "
            f"цели {_price(variant['tp1'], asset_class)} / "
            f"{_price(variant['tp2'], asset_class)}"
        )
    lines.append("Только ручной сигнал; автоордер не отправлялся.")
    return "\n".join(lines)


def send_manual_paper_entry(*, root: Path, db_path: str | Path, signal_id: str,
                            asset_class: str, symbol: str, direction: str,
                            title: str, entry_at: Any, reference_price: float | None,
                            reference_at: Any, variants: list[dict[str, Any]],
                            now: datetime, max_age_seconds: int) -> dict[str, Any]:
    entry_time = _parse_time(entry_at)
    quote_time = _parse_time(reference_at)
    now = _parse_time(now) or datetime.now(timezone.utc)
    if entry_time is None or quote_time is None or reference_price is None:
        return {"sent": False, "status": "missing_price_or_timestamp"}
    entry_age = max(0, (now - entry_time).total_seconds())
    quote_age = max(0, (now - quote_time).total_seconds())
    if entry_age > max_age_seconds or quote_age > max_age_seconds:
        return {"sent": False, "status": "stale", "entry_age_seconds": round(entry_age),
                "quote_age_seconds": round(quote_age)}
    if not variants:
        return {"sent": False, "status": "no_variants"}
    try:
        reference_price = float(reference_price)
        if not math.isfinite(reference_price) or reference_price <= 0:
            return {"sent": False, "status": "invalid_reference_price"}
        for variant in variants:
            for key in ("entry", "stop", "tp1", "tp2"):
                number = float(variant[key])
                if not math.isfinite(number) or number <= 0:
                    return {"sent": False, "status": "invalid_variant_price"}
    except (KeyError, TypeError, ValueError):
        return {"sent": False, "status": "invalid_variant_price"}

    message = render_manual_paper_entry(
        asset_class=asset_class, symbol=symbol, direction=direction, title=title,
        reference_price=reference_price, reference_at=quote_time, variants=variants,
        now=now,
    )
    store = SQLiteStore(Path(db_path))
    alert_id = str(uuid.uuid4())
    payload = {
        "manual_entry_signal": True, "paper_only": True,
        "automatic_order_sent": False, "entry_at": entry_time.isoformat(),
        "entry_age_seconds": round(entry_age), "reference_at": quote_time.isoformat(),
        "reference_price": float(reference_price), "variants": variants,
        "expires_at": min(
            entry_time + timedelta(seconds=max_age_seconds),
            quote_time + timedelta(seconds=max_age_seconds),
        ).isoformat(),
    }
    try:
        staged = stage_alert(
            store, alert_id=alert_id, signal_id=signal_id,
            alert_type="manual_paper_entry", asset_class=asset_class,
            symbol=symbol, tier="PAPER", sent_at=now.isoformat(),
            message=message, parse_mode="", mode=title, direction=direction,
            payload=payload,
        )
    except Exception as exc:  # notifications must never interrupt Paper recording
        return {"sent": False, "status": f"storage_error:{type(exc).__name__}"}
    if not staged:
        return {"sent": False, "status": "duplicate"}

    try:
        from src.notifiers.trade_telegram import notifier_for

        response = notifier_for(Path(root)).send_fast(message, parse_mode="")
        if isinstance(response, dict) and response.get("ok") is False:
            raise RuntimeError("telegram_rejected_message")
        mark_sent(store, alert_id=alert_id)
        return {"sent": True, "status": "sent", "alert_id": alert_id}
    except Exception as exc:  # durable outbox will retry delivery
        try:
            mark_error(store, alert_id=alert_id, error=type(exc).__name__)
        except Exception:
            pass
        return {"sent": False, "status": f"queued:{type(exc).__name__}",
                "alert_id": alert_id}


def _close_reason_label(reason: Any) -> str:
    labels = {
        "tp1": "TP1",
        "tp2": "TP2",
        "tp3": "TP3",
        "original_stop": "СТОП",
        "breakeven_stop": "ЗАЩИТА · BE",
        "profit_lock_stop": "ФИКСАЦИЯ ПРИБЫЛИ",
        "time_exit": "ВЫХОД ПО ВРЕМЕНИ",
    }
    value = str(reason or "close").strip()
    return labels.get(value, value.replace("_", " ").upper())


def render_manual_paper_close(*, asset_class: str, symbol: str, direction: str,
                              title: str, variants: list[dict[str, Any]]) -> str:
    asset = "АКЦИИ" if asset_class == "stocks" else "КРИПТА"
    side = str(direction or "long").upper()
    lines = [f"📊 PAPER · ИТОГ СДЕЛКИ · {asset}", f"{symbol} · {side} · {title}"]
    for variant in variants:
        label = str(variant.get("label") or "Paper")
        pnl = float(variant["net_pnl_usd"])
        net_r = float(variant["net_r"])
        reason = _close_reason_label(variant.get("close_reason"))
        highest_tp = int(variant.get("highest_tp_touched") or 0)
        if highest_tp and variant.get("close_reason") in {"breakeven_stop", "profit_lock_stop"}:
            reason = f"TP{highest_tp} · {reason}"
        line = (f"{label}: {reason} · "
                f"{net_r:+.2f}R · {pnl:+.2f} USD")
        exit_price = variant.get("exit_price")
        if exit_price is not None:
            line += f" · выход {_price(exit_price, asset_class)}"
        lines.append(line)
    lines.append("Параллельные Paper-профили; это не реальные ордера.")
    return "\n".join(lines)


def send_manual_paper_close(*, root: Path, db_path: str | Path, signal_id: str,
                            asset_class: str, symbol: str, direction: str,
                            title: str, variants: list[dict[str, Any]],
                            now: datetime) -> dict[str, Any]:
    if not variants or any(str(v.get("outcome_status")) != "closed" for v in variants):
        return {"sent": False, "status": "outcome_not_closed"}
    try:
        for variant in variants:
            for key in ("net_pnl_usd", "net_r"):
                number = float(variant[key])
                if not math.isfinite(number):
                    return {"sent": False, "status": "invalid_outcome"}
            if variant.get("exit_price") is not None:
                price = float(variant["exit_price"])
                if not math.isfinite(price) or price <= 0:
                    return {"sent": False, "status": "invalid_outcome"}
    except (KeyError, TypeError, ValueError):
        return {"sent": False, "status": "invalid_outcome"}

    now = _parse_time(now) or datetime.now(timezone.utc)
    message = render_manual_paper_close(
        asset_class=asset_class, symbol=symbol, direction=direction,
        title=title, variants=variants,
    )
    store = SQLiteStore(Path(db_path))
    alert_id = str(uuid.uuid4())
    payload = {
        "manual_close_signal": True, "paper_only": True,
        "automatic_order_sent": False, "variants": variants,
    }
    try:
        staged = stage_alert(
            store, alert_id=alert_id, signal_id=signal_id,
            alert_type="manual_paper_close", asset_class=asset_class,
            symbol=symbol, tier="PAPER", sent_at=now.isoformat(),
            message=message, parse_mode="", mode=title, direction=direction,
            payload=payload,
        )
    except Exception as exc:
        return {"sent": False, "status": f"storage_error:{type(exc).__name__}"}
    if not staged:
        return {"sent": False, "status": "duplicate"}

    try:
        from src.notifiers.trade_telegram import notifier_for

        response = notifier_for(Path(root)).send_fast(message, parse_mode="")
        if isinstance(response, dict) and response.get("ok") is False:
            raise RuntimeError("telegram_rejected_message")
        mark_sent(store, alert_id=alert_id)
        return {"sent": True, "status": "sent", "alert_id": alert_id}
    except Exception as exc:
        try:
            mark_error(store, alert_id=alert_id, error=type(exc).__name__)
        except Exception:
            pass
        return {"sent": False, "status": f"queued:{type(exc).__name__}",
                "alert_id": alert_id}


__all__ = [
    "latest_closed_minute", "render_manual_paper_entry", "send_manual_paper_entry",
    "render_manual_paper_close", "send_manual_paper_close",
]
