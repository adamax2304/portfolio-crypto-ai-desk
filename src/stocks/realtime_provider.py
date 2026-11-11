"""Stocks realtime data provider abstraction + session-gap guard (2026-07-05).

Two read-model concerns for stocks-intraday latency:

  1. `StocksRealtimeDataProvider` — a provider abstraction whose DEFAULT is yfinance, explicitly
     marked `live_grade=False` (delayed / rolling-window feed — NOT adequate for live/paper latency).
     Live-grade providers (Alpaca / Polygon / IEX / IBKR) are env-gated and only enable when their
     API key is present. Nothing ships with a key, so the system keeps working on yfinance while
     honestly reporting `live_grade: false`.

  2. Session-gap classification — a stocks signal created outside the US regular cash session, or
     before a fresh intraday bar exists, must NOT be treated as a real late fill; it is tagged
     SESSION_GAP / DATA_GAP_LATE so it never masquerades as an actionable paper entry.

Read-only / advisory. Never changes score/tier/actionability/TP/SL/sizing, never unlocks live.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from src.config import load_config
from src.stocks.market_calendar import is_us_cash_session_open, us_session_label

# a signal whose first intraday bar appears more than this many minutes after creation is a
# data-coverage artifact, not a real fill delay.
FIRST_BAR_GAP_BLOCK_MIN = 30.0


@dataclass(frozen=True)
class ProviderStatus:
    name: str
    live_grade: bool
    enabled: bool
    reason: str
    env_var: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "live_grade": self.live_grade, "enabled": self.enabled,
                "reason": self.reason, "env_var": self.env_var}


def _providers_cfg() -> list[dict]:
    try:
        import yaml
        p = load_config().root / "config" / "latency.yaml"
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        return (data.get("stocks_realtime") or {}).get("providers") or []
    except Exception:
        return []


def _load_local_env() -> None:
    """Load local or Windows user-scoped provider credentials."""
    try:
        from dotenv import load_dotenv
        load_dotenv(load_config().root / ".env", override=False)
    except Exception:
        pass
    if os.name != "nt":
        return
    try:
        import winreg

        names = {
            "ALPACA_API_KEY", "ALPACA_API_SECRET", "ALPACA_DATA_BASE_URL",
            "ALPACA_TRADING_BASE_URL", "FINNHUB_API_KEY", "POLYGON_API_KEY",
            "IEX_API_KEY", "IBKR_ACCOUNT",
        }
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            for name in names:
                # An explicitly empty process variable is meaningful in tests
                # and in an operator-requested temporary disable. Only inherit
                # from HKCU when the variable is genuinely absent.
                if name in os.environ:
                    continue
                try:
                    value, _ = winreg.QueryValueEx(key, name)
                except FileNotFoundError:
                    continue
                if str(value or "").strip():
                    os.environ[name] = str(value).strip()
    except (OSError, ImportError):
        pass


def provider_statuses() -> list[ProviderStatus]:
    """Every configured stocks realtime provider + whether it's enabled (env key present). yfinance
    is always enabled but live_grade=False. Read-only."""
    _load_local_env()
    cfg = _providers_cfg()
    if not cfg:
        # safe default: yfinance only, not live-grade
        return [ProviderStatus("yfinance", False, True,
                               "free delayed/rolling-window feed — fallback only, not live-grade")]
    out: list[ProviderStatus] = []
    for pv in cfg:
        name = str(pv.get("name") or "?")
        live = bool(pv.get("live_grade"))
        env = pv.get("env_var")
        secret_env = pv.get("secret_env_var")
        if name == "yfinance" or not env:
            out.append(ProviderStatus(name, live, True,
                                      str(pv.get("reason") or "default fallback provider"), env))
        else:
            has_key = bool(os.environ.get(str(env), "").strip())
            has_secret = not secret_env or bool(
                os.environ.get(str(secret_env), "").strip()
            )
            enabled = bool(has_key and has_secret)
            if enabled and live:
                reason = "api key present - live-grade OHLCV provider active"
            elif enabled:
                reason = str(pv.get("reason") or "api key present for its configured role")
            elif has_key and secret_env:
                reason = f"disabled - set {secret_env} to complete provider credentials"
            else:
                reason = f"disabled - set {env} to enable this provider"
            out.append(ProviderStatus(
                name, live, enabled,
                reason, env))
    return out


def active_provider() -> ProviderStatus:
    """The provider that would actually be used: the first ENABLED live-grade provider (if a key is
    present), otherwise the yfinance fallback (not live-grade)."""
    statuses = provider_statuses()
    for s in statuses:
        if s.enabled and s.live_grade:
            return s
    try:
        import yaml
        path = load_config().root / "config" / "latency.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        default = str((data.get("stocks_realtime") or {}).get("default_provider") or "").lower()
        for s in statuses:
            if s.enabled and s.name.lower() == default:
                return s
    except Exception:
        pass
    for s in statuses:
        if s.enabled and s.name == "yfinance":
            return s
    return statuses[0] if statuses else ProviderStatus(
        "yfinance", False, True, "default fallback")


def finnhub_quote(symbol: str) -> dict[str, Any]:
    """Fetch one current Finnhub quote for diagnostics or non-authoritative revalidation.

    The installed Finnhub plan has quote/news access but not candle access. A single quote must not
    be treated as a synthetic bar because that would corrupt VWAP, RVOL and entry-touch evidence.
    A failure remains explicit and never changes a trading decision.
    """
    _load_local_env()
    token = os.environ.get("FINNHUB_API_KEY", "").strip()
    if not token:
        return {"ok": False, "source": "finnhub", "reason": "missing_api_key"}
    try:
        import requests
        response = requests.get(
            "https://finnhub.io/api/v1/quote", params={"symbol": str(symbol).upper(), "token": token},
            timeout=8,
        )
        response.raise_for_status()
        payload = response.json() or {}
        price = float(payload.get("c") or 0.0)
        if price <= 0:
            return {"ok": False, "source": "finnhub", "reason": "empty_quote"}
        try:
            observed_at = datetime.fromtimestamp(float(payload.get("t")), tz=timezone.utc).isoformat()
        except (TypeError, ValueError, OSError):
            observed_at = None
        return {"ok": True, "source": "finnhub", "symbol": str(symbol).upper(),
                "price": price, "observed_at": observed_at}
    except Exception as exc:
        response = getattr(exc, "response", None)
        code = getattr(response, "status_code", None)
        return {"ok": False, "source": "finnhub", "reason": f"http_{code}" if code else type(exc).__name__}


def provider_chain_summary() -> dict[str, Any]:
    """Read-only provider routing across asset classes, without conflating price and news feeds."""
    stock = active_provider()
    return {
        "stocks": {"ohlcv_active": stock.to_dict(), "quote_primary": "finnhub",
                   "ohlcv_note": "Finnhub candle entitlement unavailable; quote/news remain usable."},
        "crypto": {"ohlcv_primary": "binance", "ohlcv_fallbacks": ["bybit", "mexc"],
                   "note": "direct exchange OHLCV; no yfinance/Finnhub dependency."},
        "news": {"fast_primary": ["finnhub", "telegram", "fast_rss"],
                 "slow_context": ["editorial_rss", "enriched_review"]},
    }


def classify_session_gap(created_at: datetime | str, *, first_bar_ts: datetime | str | None = None,
                         now: datetime | None = None) -> dict[str, Any]:
    """Classify a stocks-intraday signal's fillability at creation time. Pure / testable.

    Returns a dict with `classification` in {OK, SESSION_GAP, DATA_GAP_LATE} + reason:
      * SESSION_GAP    — created outside the US regular cash session (no live intraday market);
                         a later "fill" is a next-session artifact, not a real entry.
      * DATA_GAP_LATE  — created in-session but the first intraday bar is missing / arrives
                         >FIRST_BAR_GAP_BLOCK_MIN after creation (coverage gap, not a real fill).
      * OK             — in-session and a fresh bar exists close to creation.
    """
    c0 = _parse(created_at)
    fb = _parse(first_bar_ts) if first_bar_ts is not None else None
    if c0 is None:
        return {"classification": "DATA_GAP_LATE", "reason": "unparseable created_at",
                "session_label": None, "first_bar_gap_min": None}
    label = us_session_label(c0)
    in_session = is_us_cash_session_open(c0)
    if not in_session:
        return {"classification": "SESSION_GAP",
                "reason": f"signal created outside RTH ({label}) — late fill not real",
                "session_label": label, "first_bar_gap_min": None}
    gap_min = None
    if fb is not None:
        gap_min = round((fb - c0).total_seconds() / 60.0, 1)
    if fb is None or (gap_min is not None and gap_min > FIRST_BAR_GAP_BLOCK_MIN):
        return {"classification": "DATA_GAP_LATE",
                "reason": ("no fresh intraday bar near creation" if fb is None
                           else f"first bar {gap_min}min after creation > {FIRST_BAR_GAP_BLOCK_MIN}min"),
                "session_label": label, "first_bar_gap_min": gap_min}
    return {"classification": "OK", "reason": "in-session with a fresh bar",
            "session_label": label, "first_bar_gap_min": gap_min}


def provider_quality(*, created_at: datetime | str | None = None,
                     first_bar_ts: datetime | str | None = None,
                     data_age_sec: float | None = None, now: datetime | None = None) -> dict[str, Any]:
    """Provider-quality fields for the report: live_grade / data_age_sec / first_bar_gap_min /
    coverage_window_ok. Read-only."""
    prov = active_provider()
    fb = _parse(first_bar_ts) if first_bar_ts is not None else None
    c0 = _parse(created_at) if created_at is not None else None
    first_bar_gap_min = round((fb - c0).total_seconds() / 60.0, 1) if (fb and c0) else None
    coverage_ok = (first_bar_gap_min is not None and first_bar_gap_min <= FIRST_BAR_GAP_BLOCK_MIN)
    return {"provider": prov.name, "live_grade": prov.live_grade,
            "data_age_sec": data_age_sec, "first_bar_gap_min": first_bar_gap_min,
            "coverage_window_ok": coverage_ok}


def stocks_intraday_status(db=None) -> dict[str, Any]:
    """Combined stocks-intraday latency gate: provider live-grade + DATA_GAP_LATE share + p90
    entry-detect SLA. Reports `promotion_blocked` + reasons. Read-only — it reports, never promotes."""
    prov = active_provider()
    reasons: list[str] = []
    blocked = False
    if not prov.live_grade:
        blocked = True
        reasons.append(f"provider '{prov.name}' is not live-grade ({prov.reason})")
    # Recent A/B cohort is operationally relevant; lifetime planning artifacts
    # remain available as historical context but must not masquerade as current lag.
    share = None
    all_time_share = None
    sample_n = 0
    try:
        from src.signals.latency_readmodel import data_gap_diagnostics, STOCKS_DGL_BLOCK_SHARE
        dg = data_gap_diagnostics(db, recent_days=7)
        for m in dg.get("by_mode", []):
            if str(m["asset_class"]).startswith("stock") and m["mode"] == "intraday":
                share = m.get("recent_actionable_data_gap_late_share")
                sample_n = int(m.get("recent_actionable_n") or 0)
                all_time_share = m.get("actionable_data_gap_late_share")
                if all_time_share is None:
                    all_time_share = m.get("data_gap_late_share")
                if share is not None and share > STOCKS_DGL_BLOCK_SHARE:
                    blocked = True
                    reasons.append(f"DATA_GAP_LATE share {int(share*100)}% > "
                                   f"{int(STOCKS_DGL_BLOCK_SHARE*100)}% block threshold (recent A/B)")
    except Exception:
        pass
    # p90 entry-detect SLA
    try:
        from src.signals.latency_sla import sla_report
        r = sla_report(db)
        si = (r.get("acceptance") or {}).get("stocks_intraday") or {}
        p90 = (si.get("after_bar_close_lower_bound_sec") or {}).get("p90")
        sla_p90 = r["sla_thresholds"]["stocks_intraday_entry_detect_p90_sec"]
        if p90 is not None and p90 > sla_p90:
            blocked = True
            reasons.append(f"entry-detect p90 {p90}s > {sla_p90}s SLA")
    except Exception:
        pass
    quote_ready = any(status.name == "finnhub" and status.enabled for status in provider_statuses())
    paper_allowed = bool(quote_ready and (share is None or share <= 0.30))
    return {"provider": prov.to_dict(), "data_gap_late_share": share,
            "data_gap_late_share_all_time": all_time_share,
            "data_gap_recent_sample_n": sample_n, "data_gap_window_days": 7,
            # Backward-compatible key: it now explicitly means LIVE promotion.
            "promotion_blocked": True, "live_promotion_blocked": True,
            "paper_forward_testing_allowed": paper_allowed,
            "reasons": reasons or ["live promotion is hard-locked independent of latency"],
            "note": "Paper profiles may use delayed structural bars only with fresh Finnhub quote "
                    "revalidation; live/auto-live/manual-live remain hard-locked."}


def render_markdown(db=None) -> str:
    lines = ["## Stocks realtime provider + session-gap gate (read-only; live hard-locked)"]
    for s in provider_statuses():
        grade = "LIVE-GRADE" if s.live_grade else "NOT live-grade"
        state = "enabled" if s.enabled else "disabled"
        lines.append(f"- {s.name}: {grade} · {state} — {s.reason}")
    st = stocks_intraday_status(db)
    share = (f"{int(st['data_gap_late_share']*100)}% (A/B, recent {st['data_gap_window_days']}d, "
             f"n={st['data_gap_recent_sample_n']})" if st["data_gap_late_share"] is not None else
             f"— (A/B, recent {st['data_gap_window_days']}d, n=0)")
    lifetime = (f"{int(st['data_gap_late_share_all_time']*100)}%" if
                st["data_gap_late_share_all_time"] is not None else "—")
    lines.append("")
    lines.append(f"- Active provider: **{st['provider']['name']}** "
                 f"(live_grade={st['provider']['live_grade']})")
    lines.append(f"- stocks-intraday DATA_GAP_LATE: {share}; all-time historical context {lifetime}")
    lines.append(f"- live_promotion_blocked: {st['live_promotion_blocked']} — {'; '.join(st['reasons'])}")
    lines.append(f"- paper_forward_testing_allowed: {st['paper_forward_testing_allowed']} — "
                 "15m structure is revalidated against a fresh Finnhub quote before entry")
    chain = provider_chain_summary()
    lines.append(f"- Crypto OHLCV route: **{chain['crypto']['ohlcv_primary']}** -> "
                 f"{' -> '.join(chain['crypto']['ohlcv_fallbacks'])}")
    return "\n".join(lines)


def _parse(ts) -> datetime | None:
    if ts is None:
        return None
    if isinstance(ts, datetime):
        return ts if ts.tzinfo else ts.replace(tzinfo=timezone.utc)
    try:
        t = str(ts).strip().replace("Z", "+00:00")
        dt = datetime.fromisoformat(t)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except Exception:
        return None
