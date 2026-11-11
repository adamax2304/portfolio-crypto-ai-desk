"""Stocks-intraday actionability gates (SI-1..SI-5) — READ-MODEL / PAPER ONLY.

Pure, config-driven, fail-conservative gates that can only DEMOTE a stock-intraday A/B candidate to
C (watchlist / not actionable) — they never promote, never change score, never touch live / final_r,
never re-enable the retired stocks swing/invest frameworks. Every demotion carries an explainable
reason string so reports / UI / diagnostics can show WHY a candidate was demoted.

Composed by ``evaluate(...)`` which returns the full diagnostic field set + the demotion decision.
The rule everywhere: if the confirming evidence is missing / stale / unknown, FAIL CONSERVATIVE
(demote), never assume confirmation. Applied only when ``mode == 'intraday'`` and current tier ∈ {A,B}.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# ---- session phases (RTH, US cash) ------------------------------------------------------------
PREMARKET = "premarket"
FIRST_15M = "first_15m"
MORNING = "morning"            # 09:45–11:30 ET — normal momentum window
LUNCH = "lunch"                # 11:30–13:30 ET — stricter
AFTERNOON = "afternoon"        # 13:30–15:30 ET — normal
LAST_30M = "last_30m"          # 15:30–16:00 ET — late-day rule
OUTSIDE_RTH = "outside_rth"    # closed / after-hours / weekend / holiday


def session_phase(now) -> str:
    """Classify the RTH phase (DST-safe via the ET conversion). now is a tz-aware UTC datetime."""
    try:
        from src.stocks.market_calendar import _to_ny, is_us_holiday, us_cash_session_close
    except Exception:
        return OUTSIDE_RTH
    ny = _to_ny(now)
    if ny.weekday() >= 5 or is_us_holiday(now):
        return OUTSIDE_RTH
    mins = ny.hour * 60 + ny.minute
    open_m = 9 * 60 + 30
    close_dt = us_cash_session_close(now)
    close_m = (close_dt.astimezone(ny.tzinfo).hour * 60 + close_dt.astimezone(ny.tzinfo).minute
               if close_dt is not None else 16 * 60)
    if mins < open_m or mins >= close_m:
        return PREMARKET if mins < open_m else OUTSIDE_RTH
    if mins < open_m + 15:
        return FIRST_15M
    if mins < 11 * 60 + 30:
        return MORNING
    if mins < 13 * 60 + 30:
        return LUNCH
    if mins < close_m - 30:
        return AFTERNOON
    return LAST_30M


# ---- gate result container ---------------------------------------------------------------------
@dataclass
class GateResult:
    decision: str = "AB"                       # "AB" (stays actionable) or "C" (demoted)
    demote_reasons: list[str] = field(default_factory=list)
    fields: dict[str, Any] = field(default_factory=dict)

    def demote(self, reason: str) -> None:
        self.decision = "C"
        if reason not in self.demote_reasons:
            self.demote_reasons.append(reason)


def _f(v):
    try:
        return None if v is None or v == "" else float(v)
    except (TypeError, ValueError):
        return None


def _long(direction) -> bool:
    return str(direction or "long").lower() != "short"


# ---- SI-1 Market Context Gate ------------------------------------------------------------------
def market_context_gate(*, direction, market_ctx: dict, cfg: dict) -> tuple[str, str | None]:
    """SPY/QQQ RTH direction + vs-VWAP + intraday regime. Long/short allowed only if the market
    context does NOT contradict. Unknown/stale → conservative demote."""
    status = str((market_ctx or {}).get("status") or "unknown").lower()
    if status in ("unknown", "stale", "no_data"):
        return "unknown", "market_context_unknown_or_stale"
    regime = str((market_ctx or {}).get("regime") or "unknown").lower()
    spy = _f((market_ctx or {}).get("spy_rth_return_pct"))
    qqq = _f((market_ctx or {}).get("qqq_rth_return_pct"))
    spy_vwap = str((market_ctx or {}).get("spy_vs_vwap") or "unknown").lower()
    qqq_vwap = str((market_ctx or {}).get("qqq_vs_vwap") or "unknown").lower()
    thr = float(cfg.get("index_return_conflict_pct", 0.15))  # broad-index move against the trade
    long = _long(direction)
    if regime == "risk_off":
        # risk_off contradicts longs outright; shorts tolerated
        if long:
            return "conflict", "market_context_conflict"
    both_down = (spy is not None and qqq is not None and spy <= -thr and qqq <= -thr
                 and spy_vwap == "below" and qqq_vwap == "below")
    both_up = (spy is not None and qqq is not None and spy >= thr and qqq >= thr
               and spy_vwap == "above" and qqq_vwap == "above")
    if long and (both_down or regime == "trend_down"):
        return "conflict", "market_context_conflict"
    if (not long) and (both_up or regime == "trend_up"):
        return "conflict", "market_context_conflict"
    return "ok", None


# ---- SI-2 Sector Confirmation Hard Gate --------------------------------------------------------
def sector_confirmation_gate(*, direction, sector_ctx: dict, catalyst_strong: bool,
                             cfg: dict) -> tuple[str, str | None]:
    """Sector ETF direction/VWAP + RS vs SPY + RS vs sector. confirmed keeps A/B; weak/unknown →
    demote unless catalyst is strong; conflict → demote (not actionable)."""
    status = str((sector_ctx or {}).get("status") or "unknown").lower()
    if status == "conflict":
        return "conflict", "sector_confirmation_conflict"
    if status == "confirmed":
        return "confirmed", None
    if status == "unknown" and bool(cfg.get("allow_unknown_sector_for_pure_technical_ab", False)):
        return "provisional", None
    # weak / unknown → conservative demote unless a strong catalyst carries it
    if catalyst_strong:
        return status if status in ("weak", "unknown") else "weak", None
    return (status if status in ("weak", "unknown") else "unknown"), "sector_confirmation_weak_or_unknown"


def classify_sector(*, direction, sector_rth_return_pct, sector_vs_vwap, rs_vs_spy, rs_vs_sector,
                    cfg: dict) -> str:
    """Deterministic sector_confirmation_status from the raw sector fields. Fail-conservative:
    missing inputs → unknown; sector breaking against the trade → conflict."""
    sret = _f(sector_rth_return_pct)
    svwap = str(sector_vs_vwap or "unknown").lower()
    rss = _f(rs_vs_spy)
    rsec = _f(rs_vs_sector)
    if sret is None or svwap == "unknown":
        return "unknown"
    long = _long(direction)
    thr = float(cfg.get("sector_return_conflict_pct", 0.15))
    # sector ETF breaking the wrong way = hard conflict
    if long and (sret <= -thr and svwap == "below"):
        return "conflict"
    if (not long) and (sret >= thr and svwap == "above"):
        return "conflict"
    # don't take a weak stock in a strong sector (long) / strong stock in weak sector (short)
    if rss is None or rsec is None:
        return "unknown"
    if long:
        sector_ok = sret >= 0 or svwap == "above"
        stock_ok = rss > 0 and rsec > 0
    else:
        sector_ok = sret <= 0 or svwap == "below"
        stock_ok = rss < 0 and rsec < 0
    if sector_ok and stock_ok:
        return "confirmed"
    return "weak"


# ---- SI-3 Session Rules ------------------------------------------------------------------------
def session_gate(*, phase: str, setup_type, rvol_strong: bool, catalyst_strong: bool,
                 trend_continuation: bool, cfg: dict) -> tuple[str, str | None]:
    """RTH-phase actionability rule for stock intraday A/B."""
    st = str(setup_type or "").lower()
    if phase == OUTSIDE_RTH:
        return "blocked", "outside_rth"
    if phase == PREMARKET:
        return "blocked", "premarket_watchlist_only"
    if phase == FIRST_15M:
        is_orb = ("orb" in st or "opening_drive" in st or "opening" in st)
        if not (is_orb and rvol_strong):
            return "blocked", "first_15m_requires_orb_or_opening_drive"
        return "ok", None
    if phase == LUNCH:
        if not (catalyst_strong and rvol_strong):
            return "blocked", "lunch_requires_strong_confirmation"
        return "ok", None
    if phase == LAST_30M:
        if not trend_continuation:
            return "blocked", "last_30m_requires_trend_continuation"
        return "ok", None
    return "ok", None   # MORNING / AFTERNOON — normal gates


# ---- SI-4 RVOL + Liquidity Gate ----------------------------------------------------------------
def liquidity_gate(*, liquidity: dict, cfg: dict) -> tuple[str, str | None]:
    """RVOL / dollar-volume / spread / data-freshness / no-DGL gate. Unknown spread → demote unless
    the name is on the liquidity whitelist AND unknown spread is explicitly allowed."""
    rvol = _f((liquidity or {}).get("rvol"))
    dv = _f((liquidity or {}).get("dollar_volume"))
    spread = _f((liquidity or {}).get("spread_bps_est"))
    fresh = str((liquidity or {}).get("data_freshness_status") or "unknown").lower()
    dgl = bool((liquidity or {}).get("data_gap_late"))
    whitelisted = bool((liquidity or {}).get("liquidity_whitelisted"))
    min_rvol = float(cfg.get("min_rvol", 1.5))
    min_dv = float(cfg.get("min_dollar_volume", 20_000_000))
    max_spread = float(cfg.get("max_spread_bps", 25))
    allow_unknown_spread = bool(cfg.get("allow_unknown_spread_for_liquid_names", False))
    if dgl:
        return "blocked", "liquidity_data_gap_late"
    if fresh in ("stale", "unknown", "no_data"):
        return "blocked", "liquidity_data_stale"
    if rvol is None or rvol < min_rvol:
        return "blocked", "liquidity_rvol_below_min"
    if dv is None or dv < min_dv:
        return "blocked", "liquidity_dollar_volume_below_min"
    if spread is None:
        if not (allow_unknown_spread and whitelisted):
            return "blocked", "liquidity_spread_unknown"
    elif spread > max_spread:
        return "blocked", "liquidity_spread_too_wide"
    return "ok", None


# ---- SI-5 Catalyst Quality Gate ----------------------------------------------------------------
def classify_catalyst_quality(*, primary_type, age_minutes, source_count, source_quality,
                              cfg: dict) -> str:
    """strong / medium / weak / none from EXISTING catalyst metadata (never fabricated)."""
    pt = str(primary_type or "").lower()
    age = _f(age_minutes)
    sc = int(source_count or 0)
    sq = str(source_quality or "unknown").lower()
    max_age = float(cfg.get("catalyst_max_age_minutes", 24 * 60))
    if not pt or pt in ("none", "unknown") or sc <= 0:
        return "none"
    if age is not None and age > max_age:
        return "stale"
    strong_types = set(cfg.get("catalyst_strong_types",
                       ["earnings", "guidance", "fda", "regulatory_approval", "mna", "merger",
                        "acquisition", "major_contract", "index_inclusion", "analyst_action_major"]))
    if pt in strong_types and sq in ("high", "medium") and sc >= 1:
        return "strong"
    medium_types = set(cfg.get("catalyst_medium_types",
                       ["analyst_action", "product", "partnership", "sector_sympathy", "macro"]))
    if pt in medium_types or (sq == "high" and sc >= 2):
        return "medium"
    return "weak"


def catalyst_gate(*, catalyst_quality: str, market_confirmed: bool, sector_confirmed: bool,
                  rvol_strong: bool, cfg: dict, direction: str | None = None,
                  setup_type: str | None = None, catalyst_direction_hint: str | None = None,
                  catalyst_age_minutes: float | None = None) -> tuple[str, str | None]:
    """A/B allowed if: strong catalyst OR medium+all-confirmed OR (no/weak catalyst only with an
    EXCEPTIONAL pure-technical confirmation = market+sector+RVOL all confirmed)."""
    q = str(catalyst_quality or "none").lower()
    is_short_pullback = (str(direction or "").lower() == "short"
                         and str(setup_type or "").lower() in {"pullback", "retest"})
    if is_short_pullback and bool(cfg.get("short_pullback_require_bearish_catalyst", True)):
        fresh_limit = float(cfg.get("short_pullback_catalyst_max_age_minutes", 360))
        if (q not in {"strong", "medium"}
                or str(catalyst_direction_hint or "").lower() != "bearish"
                or catalyst_age_minutes is None or catalyst_age_minutes > fresh_limit):
            return "blocked", "short_pullback_requires_fresh_bearish_catalyst"
    if q == "strong":
        return "ok", None
    all_confirmed = market_confirmed and sector_confirmed and rvol_strong
    if q == "medium":
        return ("ok", None) if all_confirmed else ("blocked", "catalyst_medium_without_full_confirmation")
    # weak / none / stale → only survive on exceptional pure-technical confirmation
    if all_confirmed and bool(cfg.get("allow_pure_technical_ab", True)):
        return "ok", None
    return "blocked", f"catalyst_{q or 'none'}_and_not_exceptional_technical"


# ---- composer ----------------------------------------------------------------------------------
def evaluate(*, direction, phase: str, setup_type, market_ctx: dict, sector_ctx: dict,
             liquidity: dict, catalyst: dict, cfg: dict) -> GateResult:
    """Run all SI-1..SI-5 gates; ANY demote → tier C. Returns decision + reasons + the full
    diagnostic field set for report/UI/diagnostics."""
    res = GateResult()
    rvol_strong = (_f((liquidity or {}).get("rvol")) or 0.0) >= float(cfg.get("min_rvol", 1.5))
    cat_q = str((catalyst or {}).get("catalyst_quality") or "none").lower()
    catalyst_strong = cat_q == "strong"

    mkt_status, mkt_reason = market_context_gate(direction=direction, market_ctx=market_ctx, cfg=cfg)
    sec_status, sec_reason = sector_confirmation_gate(direction=direction, sector_ctx=sector_ctx,
                                                      catalyst_strong=catalyst_strong, cfg=cfg)
    market_confirmed = mkt_status == "ok"
    sector_confirmed = sec_status in {"confirmed", "provisional"}
    trend_cont = market_confirmed and sec_status == "confirmed" and rvol_strong
    ses_status, ses_reason = session_gate(phase=phase, setup_type=setup_type, rvol_strong=rvol_strong,
                                           catalyst_strong=catalyst_strong, trend_continuation=trend_cont,
                                           cfg=cfg)
    liq_status, liq_reason = liquidity_gate(liquidity=liquidity, cfg=cfg)
    cat_status, cat_reason = catalyst_gate(catalyst_quality=cat_q, market_confirmed=market_confirmed,
                                           sector_confirmed=sector_confirmed, rvol_strong=rvol_strong,
                                           direction=direction, setup_type=setup_type,
                                           catalyst_direction_hint=(catalyst or {}).get("catalyst_direction_hint"),
                                           catalyst_age_minutes=_f((catalyst or {}).get("catalyst_age_minutes")),
                                           cfg=cfg)
    for reason in (mkt_reason, sec_reason, ses_reason, liq_reason, cat_reason):
        if reason:
            res.demote(reason)

    res.fields = {
        # SI-1
        "market_context_status": mkt_status,
        "spy_rth_return_pct": _f((market_ctx or {}).get("spy_rth_return_pct")),
        "qqq_rth_return_pct": _f((market_ctx or {}).get("qqq_rth_return_pct")),
        "spy_vs_vwap": (market_ctx or {}).get("spy_vs_vwap"),
        "qqq_vs_vwap": (market_ctx or {}).get("qqq_vs_vwap"),
        "market_regime_intraday": (market_ctx or {}).get("regime"),
        "market_context_reason": mkt_reason,
        # SI-2
        "sector_etf": (sector_ctx or {}).get("sector_etf"),
        "sector_rth_return_pct": _f((sector_ctx or {}).get("sector_rth_return_pct")),
        "sector_vs_vwap": (sector_ctx or {}).get("sector_vs_vwap"),
        "rs_vs_spy": _f((sector_ctx or {}).get("rs_vs_spy")),
        "rs_vs_sector": _f((sector_ctx or {}).get("rs_vs_sector")),
        "sector_confirmation_status": sec_status,
        "sector_confirmation_reason": sec_reason,
        # SI-3
        "session_phase": phase,
        "session_rule_status": ses_status,
        "session_rule_reason": ses_reason,
        # SI-4
        "rvol": _f((liquidity or {}).get("rvol")),
        "dollar_volume": _f((liquidity or {}).get("dollar_volume")),
        "spread_bps_est": _f((liquidity or {}).get("spread_bps_est")),
        "spread_estimation_method": (liquidity or {}).get("spread_estimation_method"),
        "liquidity_status": liq_status,
        "liquidity_reason": liq_reason,
        "data_freshness_status": (liquidity or {}).get("data_freshness_status"),
        "data_age_seconds": _f((liquidity or {}).get("data_age_seconds")),
        "last_closed_bar_at": (liquidity or {}).get("last_closed_bar_at"),
        # SI-5
        "catalyst_quality": cat_q,
        "catalyst_age_minutes": _f((catalyst or {}).get("catalyst_age_minutes")),
        "catalyst_source_count": (catalyst or {}).get("catalyst_source_count"),
        "catalyst_primary_type": (catalyst or {}).get("catalyst_primary_type"),
        "catalyst_direction_hint": (catalyst or {}).get("catalyst_direction_hint"),
        "catalyst_quality_reason": cat_reason,
    }
    return res


__all__ = ["evaluate", "session_phase", "classify_sector", "classify_catalyst_quality",
           "market_context_gate", "sector_confirmation_gate", "session_gate", "liquidity_gate",
           "catalyst_gate", "GateResult",
           "PREMARKET", "FIRST_15M", "MORNING", "LUNCH", "AFTERNOON", "LAST_30M", "OUTSIDE_RTH"]
