"""Stocks Catalyst Relative-Strength Continuation, isolated shadow strategy v1.

This is a long-only, same-day catalyst continuation experiment.  It consumes
trusted canonical news plus cached RTH OHLCV and writes only its own tables.
Existing PULLBACK_LIMIT/BREAKOUT_CONTINUATION signals are neither read as
candidates nor modified; the event, RS and confirmation sequence is independent.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd
import yaml

from src.config import load_config
from src.execution.shadow_strategy_common import (
    clean_forward_summary, diagnostics_markdown, ensure_columns, json_text, load_yaml_block, normalize_frame,
    parse_dt, preserve_first_observation, simulate_confirmed_close_entry, strategy_diagnostics,
    table_exists, utc_now,
)
from src.execution.fees import trade_costs
from src.intelligence.context_config import section as context_filter_config
from src.storage.file_store import FileStore


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "shadow_stocks_catalyst_rs.yaml"
UNIVERSE_PATH = ROOT / "config" / "stocks" / "universe.yaml"
STRATEGY_KEY = "stocks_catalyst_rs"
NY = ZoneInfo("America/New_York")

DEFAULTS: dict[str, Any] = {
    "feature_flag": False, "strategy_id": "stocks_catalyst_rs_v1",
    "profile_id": "stocks_catalyst_rs_profile_v2", "shadow_lane": "shadow_catalyst_rs",
    "timeframe": "15m", "catalyst_lookback_hours": 168, "catalyst_freshness_hours": 24,
    "trusted_source_qualities": ["company_pr", "regulator", "reputable", "primary"],
    "min_secondary_corroboration": 2,
    "exploratory_single_secondary_enabled": False,
    "exploratory_secondary_event_types": ["mna", "partnership", "product_launch",
                                            "strategic_investment", "contract_award", "guidance"],
    "exploratory_blocked_title_markers": ["?", "could ", "might ", "should you"],
    "confirmation_minutes": 15, "impulse_window_minutes": 20, "min_gap_or_impulse_pct": 5.0,
    "min_rvol": 1.5, "rvol_baseline_bars": 20, "min_rs_spy_pct": 0.25,
    "min_rs_sector_pct": 0.15, "min_dollar_volume": 25_000_000,
    "strict_min_gap_or_impulse_pct": 5.0, "strict_min_rvol": 1.5,
    "strict_min_rs_spy_pct": 0.25, "strict_min_rs_sector_pct": 0.15,
    "sector_benchmark_overrides": {"ai_hardware": "SMH", "ai_software": "XLK",
                                   "crypto_equity": "QQQ"},
    "max_market_data_age_minutes": 20, "max_entry_data_gap_minutes": 20,
    "excluded_event_types": ["earnings", "legal_risk", "offering_dilution", "sec_filing",
                             "analyst_action", "calendar_risk", "macro_headline",
                             "geopolitical_risk", "cpi", "fed", "jobs"],
    "allowed_directions": ["long"], "max_stop_adr_multiple": 1.0, "adr_lookback_days": 20,
    "target_r": [1.0, 2.0, 3.0], "fee_profile": "stock_etf_default",
    "force_same_day_exit": True, "log_next_session_close": True,
    "min_clean_closed": 30, "min_forward_days": 28, "min_profit_factor": 1.25,
    "max_review_drawdown_usd": 250.0,
    "report_path": "reports/STOCKS_CATALYST_RS_SHADOW.md",
}

REJECTION_REASONS = {
    "CATALYST_UNTRUSTED", "CATALYST_STALE", "CATALYST_TYPE_EXCLUDED", "CATALYST_TIME_UNKNOWN",
    "SYMBOL_NOT_IN_UNIVERSE", "SECTOR_BENCHMARK_MISSING", "STOCK_BARS_MISSING", "NOT_RTH",
    "MARKET_CONTEXT_MISSING",
    "MARKET_CONTEXT_STALE", "SECTOR_CONTEXT_MISSING", "SECTOR_CONTEXT_STALE",
    "IMPULSE_BELOW_THRESHOLD", "RVOL_BELOW_THRESHOLD", "FIRST_BAR_ENTRY_BLOCKED",
    "CONFIRMATION_CLOSE_MISSING", "ORH_NOT_CONFIRMED", "VWAP_NOT_RECLAIMED",
    "RS_SPY_TOO_WEAK", "RS_SECTOR_TOO_WEAK", "LIQUIDITY_TOO_LOW", "ADR_MISSING",
    "STOP_INVALID", "STOP_WIDER_THAN_ADR", "DATA_COVERAGE_DIRTY", "NO_SAME_DAY_EXIT_BAR",
}

OUTCOME_COLUMNS = (
    "candidate_id", "strategy_id", "profile_id", "shadow_lane", "window", "generated_at",
    "decision_at", "catalyst_at", "news_event_id", "symbol", "direction", "sector", "sector_etf",
    "market_regime", "catalyst_type", "catalyst_source_quality", "evidence_cohort",
    "source_trust_tier", "candidate_origin", "eligibility_status",
    "rejection_reason", "data_status", "is_clean_for_edge", "entry_ts", "entry_price",
    "stop_price", "tp1", "tp2", "tp3", "gap_or_impulse_pct", "rvol", "rs_spy_pct",
    "rs_sector_pct", "outcome_status", "close_reason", "exit_price", "exit_ts", "gross_pnl_usd",
    "net_pnl_usd", "net_r", "fees_usd", "slippage_usd", "funding_usd", "funding_source",
    "funding_estimated", "funding_event_count", "risk_usd",
    "mfe_r", "mae_r", "protection_armed", "lock_armed", "highest_tp_touched", "bars_held",
    "latency_seconds", "tradable_latency_seconds", "catalyst_age_at_entry_seconds",
    "source_ingestion_latency_seconds", "overnight_eligible", "overnight_reasons_json",
    "would_have_held_open_next_session", "would_have_held_close_next_session",
    "would_next_open_net_pnl_usd", "would_next_close_net_pnl_usd", "features_json", "notes_json",
)

OUTCOME_DDL = """
CREATE TABLE IF NOT EXISTS stocks_catalyst_rs_shadow_outcomes (
  candidate_id TEXT PRIMARY KEY, strategy_id TEXT NOT NULL, profile_id TEXT NOT NULL,
  shadow_lane TEXT NOT NULL, window TEXT NOT NULL, generated_at TEXT NOT NULL,
  decision_at TEXT NOT NULL, catalyst_at TEXT, news_event_id TEXT, symbol TEXT NOT NULL,
  direction TEXT, sector TEXT, sector_etf TEXT, market_regime TEXT, catalyst_type TEXT,
  catalyst_source_quality TEXT, evidence_cohort TEXT, source_trust_tier TEXT,
  candidate_origin TEXT, eligibility_status TEXT NOT NULL, rejection_reason TEXT,
  data_status TEXT, is_clean_for_edge INTEGER NOT NULL DEFAULT 0, entry_ts TEXT,
  entry_price REAL, stop_price REAL, tp1 REAL, tp2 REAL, tp3 REAL,
  gap_or_impulse_pct REAL, rvol REAL, rs_spy_pct REAL, rs_sector_pct REAL,
  outcome_status TEXT, close_reason TEXT, exit_price REAL, exit_ts TEXT, gross_pnl_usd REAL,
  net_pnl_usd REAL, net_r REAL, fees_usd REAL, slippage_usd REAL, funding_usd REAL,
  funding_source TEXT, funding_estimated INTEGER, funding_event_count INTEGER,
  risk_usd REAL, mfe_r REAL, mae_r REAL, protection_armed INTEGER, lock_armed INTEGER,
  highest_tp_touched INTEGER, bars_held INTEGER, latency_seconds REAL,
  tradable_latency_seconds REAL, catalyst_age_at_entry_seconds REAL,
  source_ingestion_latency_seconds REAL,
  overnight_eligible INTEGER, overnight_reasons_json TEXT,
  would_have_held_open_next_session REAL, would_have_held_close_next_session REAL,
  would_next_open_net_pnl_usd REAL, would_next_close_net_pnl_usd REAL,
  features_json TEXT, notes_json TEXT
)
"""
EVAL_DDL = """
CREATE TABLE IF NOT EXISTS stocks_catalyst_rs_shadow_evaluations (
  generated_at TEXT PRIMARY KEY, strategy_id TEXT, profile_id TEXT, activated_at TEXT,
  forward_rows INTEGER, clean_rows INTEGER, dirty_rows INTEGER, clean_closed INTEGER,
  net_pnl_usd REAL, net_r REAL, fees_usd REAL, slippage_usd REAL, funding_usd REAL,
  profit_factor REAL, winrate REAL, max_drawdown_usd REAL, forward_days REAL,
  verdict TEXT, rejection_counts_json TEXT, by_sector_json TEXT, diagnostics_json TEXT, config_json TEXT
)
"""
META_DDL = """CREATE TABLE IF NOT EXISTS stocks_catalyst_rs_shadow_meta (
  k TEXT PRIMARY KEY, v TEXT NOT NULL
)"""


def load_strategy_config() -> dict[str, Any]:
    return load_yaml_block(CONFIG_PATH, STRATEGY_KEY, DEFAULTS)


def ensure_tables(conn: sqlite3.Connection) -> None:
    conn.execute(OUTCOME_DDL)
    conn.execute(EVAL_DDL)
    conn.execute(META_DDL)
    text_cols = {"strategy_id", "profile_id", "shadow_lane", "window", "generated_at", "decision_at",
                 "catalyst_at", "news_event_id", "symbol", "direction", "sector", "sector_etf",
                 "market_regime", "catalyst_type", "catalyst_source_quality", "evidence_cohort",
                 "source_trust_tier", "candidate_origin", "eligibility_status",
                 "rejection_reason", "data_status", "entry_ts", "outcome_status", "close_reason", "exit_ts",
                 "funding_source", "overnight_reasons_json",
                 "features_json", "notes_json"}
    int_cols = {"is_clean_for_edge", "protection_armed", "lock_armed", "highest_tp_touched", "bars_held",
                "funding_estimated", "funding_event_count", "overnight_eligible"}
    ensure_columns(conn, "stocks_catalyst_rs_shadow_outcomes", {
        name: ("TEXT" if name in text_cols else "INTEGER" if name in int_cols else "REAL")
        for name in OUTCOME_COLUMNS if name != "candidate_id"
    })
    eval_text = {"strategy_id", "profile_id", "activated_at", "verdict", "rejection_counts_json",
                 "by_sector_json", "diagnostics_json", "config_json"}
    ensure_columns(conn, "stocks_catalyst_rs_shadow_evaluations", {
        name: ("TEXT" if name in eval_text else "INTEGER" if name in {"forward_rows", "clean_rows",
               "dirty_rows", "clean_closed"} else "REAL")
        for name in ("strategy_id", "profile_id", "activated_at", "forward_rows", "clean_rows",
                     "dirty_rows", "clean_closed", "net_pnl_usd", "net_r", "fees_usd", "slippage_usd",
                     "funding_usd", "profit_factor", "winrate", "max_drawdown_usd", "forward_days",
                     "verdict", "rejection_counts_json", "by_sector_json", "diagnostics_json", "config_json")
    })
    conn.execute("CREATE INDEX IF NOT EXISTS idx_catalyst_rs_window ON "
                 "stocks_catalyst_rs_shadow_outcomes(window,is_clean_for_edge,outcome_status)")


def _f(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


_SOURCE_QUALITY_RANK = {
    "regulator": 6, "primary": 6, "company_pr": 5, "reputable": 4,
    "secondary": 2, "social": 1,
}
_CONTENT_LEVEL_RANK = {
    "full_body": 4, "summary_only": 3, "body_equals_title": 2, "title_only": 1,
}
_LOCAL_EVENT_PATTERNS: tuple[tuple[str, tuple[str, ...], tuple[str, ...]], ...] = (
    ("strategic_investment", ("takes stake", "acquires stake", "discloses stake", "invests in",
                              "investment in", "% stake"), ()),
    ("contract_award", ("wins contract", "awarded contract", "selected by", "contract award"), ()),
    ("product_launch", ("launches", "unveils", "debuts", "rolls out", "introduces"),
     ("product", "platform", "system", "solution", "suite", "model", "chip", "service",
      "software", "hardware", "network", "app", "accelerator")),
    ("partnership", ("partnership", "partners with", "collaboration", "collaborates with",
                     "strategic alliance"), ()),
)
_LOCAL_DIRECTIONAL_TYPES = {
    "guidance", "mna", "fda_clinical", "management_change", "product_launch",
    "partnership", "strategic_investment", "contract_award",
}


def _source_family(source: Any) -> str:
    value = re.sub(r"[^a-z0-9]", "", str(source or "").lower())
    return value[:48] or "unknown"


def _local_event_type(event: dict[str, Any]) -> tuple[str, str]:
    """Conservatively recover a Catalyst-RS event type without changing Paper news policy."""
    canonical = str(event.get("event_type") or "unknown").lower()
    title = str(event.get("title") or "").lower()
    if canonical == "management_change" and not re.search(
        r"\b(appoint(?:s|ed)?|names?|hires?|resign(?:s|ed)?|steps? down|new ceo|"
        r"succeeds?|retires?|leadership transition)\b", title,
    ):
        return "other_news", "shadow_taxonomy_correction_v1"
    if canonical not in {"macro_headline", "other_news", "unknown"}:
        return canonical, "canonical"
    for event_type, action_terms, context_terms in _LOCAL_EVENT_PATTERNS:
        if not any(term in title for term in action_terms):
            continue
        if context_terms and not any(term in title for term in context_terms):
            continue
        return event_type, "shadow_taxonomy_v1"
    return canonical, "canonical"


def _event_anchor(title: str, event_type: str) -> int | None:
    terms = {
        "mna": ("acquire", "acquisition", "merger", "buyout", "takeover"),
        "product_launch": ("launch", "unveil", "debut", "rolls out", "introduc"),
        "partnership": ("partner", "collaborat", "alliance"),
        "strategic_investment": ("stake", "invest"),
        "contract_award": ("contract", "selected by"),
        "guidance": ("guidance", "outlook", "forecast"),
        "management_change": ("appoint", "names", "hire", "resign", "steps down", "new ceo", "retires"),
        "fda_clinical": ("fda", "phase 3", "clinical", "trial"),
    }.get(event_type, ())
    positions = [str(title).lower().find(term) for term in terms if str(title).lower().find(term) >= 0]
    return min(positions) if positions else None


def _shadow_subject_symbols(event: dict[str, Any], universe: set[str], event_type: str) -> tuple[set[str], str]:
    trusted = set(_event_symbols(event.get("trusted_symbols_json")))
    mentioned = set(_event_symbols(event.get("mentioned_symbols_json"))) | trusted
    title = str(event.get("title") or "")
    anchor = _event_anchor(title, event_type)
    recovered: set[str] = set()
    for symbol in universe:
        match = re.search(rf"(?<![A-Za-z0-9])[$#]?{re.escape(symbol)}(?![A-Za-z0-9])", title)
        if not match:
            continue
        # A curated uppercase ticker may seed Shadow only when it is the event
        # subject (normally before the action), never merely a later comparison.
        if title[match.start():match.end()].lstrip("$#") != symbol:
            continue
        if anchor is None or match.start() <= anchor:
            recovered.add(symbol)
    if recovered:
        return recovered, "shadow_title_ticker"
    if not mentioned:
        return set(), "no_subject_symbol"

    # Canonical rows classified before a local taxonomy correction can contain
    # every company mentioned in a headline. Re-evaluate issuer position here so
    # a partner, customer or competitor does not become the traded subject.
    alias_subjects: set[str] = set()
    try:
        from src.news.canonical_events import _configured_aliases
        for symbol in mentioned & universe:
            configured = _configured_aliases("stocks", symbol)
            leading_name = str(configured[0]).split()[0].strip(".,") if configured else ""
            aliases = (*configured, *(
                (leading_name,) if len(leading_name) >= 5 and title.lower().startswith(leading_name.lower()) else ()
            ), symbol)
            for alias in aliases:
                match = re.search(
                    rf"(?<![A-Za-z0-9]){re.escape(str(alias))}(?![A-Za-z0-9])", title, re.I,
                )
                if not match:
                    continue
                if event_type == "strategic_investment":
                    prefix = title[max(0, match.start() - 32):match.start()].lower()
                    if re.search(r"(?:stake|invest(?:ment|s|ed|ing)?)\s+(?:in\s+)?$", prefix):
                        alias_subjects.add(symbol)
                    continue
                if event_type == "partnership" and re.search(
                    r"\bits\s+$", title[max(0, match.start() - 12):match.start()].lower()
                ):
                    continue
                if anchor is not None and match.start() <= anchor:
                    alias_subjects.add(symbol)
    except Exception:
        alias_subjects = set()
    if alias_subjects:
        return alias_subjects, "shadow_subject_role_v1"
    return set(), "no_subject_symbol"


def _event_available_at(event: dict[str, Any]) -> datetime | None:
    observed = parse_dt(event.get("available_at"))
    if observed is not None:
        return observed
    published = parse_dt(event.get("published_at") or event.get("effective_at"))
    materialized = parse_dt(event.get("created_at"))
    values = [value for value in (published, materialized) if value is not None]
    return max(values) if values else None


def _event_group_key(symbol: str, event_type: str, event: dict[str, Any]) -> str:
    observed = parse_dt(event.get("published_at") or event.get("effective_at")) or _event_available_at(event)
    if observed is None:
        bucket = "unknown"
    else:
        local = observed.astimezone(NY)
        bucket = f"{local.date().isoformat()}:{local.hour // 12}"
    return f"{symbol}|{event_type}|{bucket}"


def _title_is_speculative(title: Any, cfg: dict[str, Any]) -> bool:
    value = str(title or "").lower()
    return any(str(marker).lower() in value for marker in cfg.get("exploratory_blocked_title_markers", []))


def _trust_trigger(members: list[dict[str, Any]], cfg: dict[str, Any]) -> tuple[str, dict[str, Any], int, int]:
    """Return the earliest point-in-time source state that could admit the event."""
    ordered = sorted(members, key=lambda item: (_event_available_at(item) or datetime.max.replace(tzinfo=timezone.utc),
                                                int(item.get("news_item_id") or 0)))
    trusted = {str(value).lower() for value in cfg.get("trusted_source_qualities", [])}
    seen_families: set[str] = set()
    seen_non_social: set[str] = set()
    secondary_allowed = {str(value).lower() for value in cfg.get("exploratory_secondary_event_types", [])}
    for member in ordered:
        quality = str(member.get("source_quality") or "unknown").lower()
        family = _source_family(member.get("source"))
        seen_families.add(family)
        if quality != "social":
            seen_non_social.add(family)
        if quality in trusted:
            return "trusted_primary_or_reputable", member, len(seen_families), len(seen_non_social)
        if quality == "secondary" and len(seen_non_social) >= int(cfg.get("min_secondary_corroboration", 2)):
            return "corroborated_secondary", member, len(seen_families), len(seen_non_social)
        if (quality == "secondary" and cfg.get("exploratory_single_secondary_enabled", False)
                and str(member.get("event_type") or "").lower() in secondary_allowed
                and str(member.get("content_level") or "unknown").lower() != "title_only"
                and not _title_is_speculative(member.get("title"), cfg)):
            return "exploratory_single_secondary", member, len(seen_families), len(seen_non_social)
    fallback = ordered[0] if ordered else {}
    return "untrusted", fallback, len(seen_families), len(seen_non_social)


def _candidate_id(strategy: str, event_id: str, symbol: str, profile_id: str | None = None) -> str:
    raw = f"{strategy}|{profile_id or 'legacy'}|{event_id}|{symbol.upper()}"
    return "scrs_" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]


def _ny_date(ts: Any):
    dt = parse_dt(ts)
    return dt.astimezone(NY).date() if dt else None


def _is_rth(ts: Any) -> bool:
    dt = parse_dt(ts)
    if dt is None:
        return False
    ny = dt.astimezone(NY)
    return ny.weekday() < 5 and time(9, 30) <= ny.time() < time(16, 0)


def _rth(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty or "timestamp" not in frame.columns:
        return frame
    out = frame.copy()
    ny = out["timestamp"].dt.tz_convert(NY)
    mask = ((ny.dt.weekday < 5) &
            ((ny.dt.hour > 9) | ((ny.dt.hour == 9) & (ny.dt.minute >= 30))) &
            (ny.dt.hour < 16))
    return out[mask].reset_index(drop=True)


def _closed_as_of(frame: pd.DataFrame, ts: datetime, bar_minutes: int) -> pd.DataFrame:
    d = normalize_frame(frame)
    if d.empty:
        return d
    return d[d["timestamp"] + pd.Timedelta(minutes=bar_minutes) <= pd.Timestamp(ts)]


def _close_at_or_before(frame: pd.DataFrame, ts: datetime, bar_minutes: int) -> tuple[float | None, datetime | None]:
    d = _closed_as_of(frame, ts, bar_minutes)
    if d.empty:
        return None, None
    row = d.iloc[-1]
    closed_at = row["timestamp"].to_pydatetime() + timedelta(minutes=bar_minutes)
    return _f(row.get("close")), closed_at


def _return_between(frame: pd.DataFrame, start: datetime, end: datetime, bar_minutes: int) -> float | None:
    d = normalize_frame(frame)
    # A missing sector/ETF cache is a data-quality rejection, never a strategy
    # exception.  ``normalize_frame`` legitimately returns an empty frame with
    # no columns for an unavailable source.
    if d.empty or "timestamp" not in d.columns or "close" not in d.columns:
        return None
    closes_at = d["timestamp"] + pd.Timedelta(minutes=bar_minutes)
    before = d[closes_at <= pd.Timestamp(start)]
    through = d[closes_at <= pd.Timestamp(end)]
    if before.empty or through.empty:
        return None
    p0, p1 = _f(before.iloc[-1].get("close")), _f(through.iloc[-1].get("close"))
    return ((p1 / p0) - 1.0) * 100.0 if p0 and p1 else None


def _vwap(day: pd.DataFrame, through_idx: int) -> float | None:
    d = day.iloc[:through_idx + 1]
    if d.empty or "volume" not in d:
        return None
    volume = d["volume"].astype(float)
    if float(volume.sum()) <= 0:
        return None
    typical = (d["high"].astype(float) + d["low"].astype(float) + d["close"].astype(float)) / 3.0
    return float((typical * volume).sum() / volume.sum())


def _adr(daily: pd.DataFrame, as_of: datetime, count: int) -> float | None:
    d = normalize_frame(daily, as_of=as_of)
    if len(d) < count or not {"high", "low"}.issubset(d.columns):
        return None
    return float((d["high"].astype(float) - d["low"].astype(float)).tail(count).mean())


def _previous_close(daily: pd.DataFrame, event_at: datetime) -> float | None:
    d = normalize_frame(daily)
    if d.empty or "timestamp" not in d.columns or "close" not in d.columns:
        return None
    prior = d[d["timestamp"].dt.tz_convert(NY).dt.date < event_at.astimezone(NY).date()]
    return _f(prior.iloc[-1].get("close")) if not prior.empty else None


def _next_session_prices(
    frame: pd.DataFrame, session_date: Any, bar_minutes: int,
) -> tuple[float | None, datetime | None, float | None, datetime | None]:
    d = _rth(normalize_frame(frame))
    if d.empty:
        return None, None, None, None
    dates = d["timestamp"].dt.tz_convert(NY).dt.date
    future_dates = sorted({x for x in dates if x > session_date})
    if not future_dates:
        return None, None, None, None
    next_day = d[dates == future_dates[0]]
    if next_day.empty:
        return None, None, None, None
    first = next_day.iloc[0]
    last = next_day.iloc[-1]
    open_at = first["timestamp"].to_pydatetime().astimezone(timezone.utc)
    close_at = (last["timestamp"].to_pydatetime() + timedelta(minutes=bar_minutes)).astimezone(NY)
    if close_at.time() < time(16, 0):
        return _f(first.get("open")), open_at, None, None
    return (_f(first.get("open")), open_at, _f(last.get("close")), close_at.astimezone(timezone.utc))


def _next_session_close(
    frame: pd.DataFrame, session_date: Any, bar_minutes: int,
) -> tuple[float | None, datetime | None]:
    _, _, close, close_at = _next_session_prices(frame, session_date, bar_minutes)
    return close, close_at


def overnight_eligibility(*, session_date: Any, event_type: str, close_price: float,
                          day_low: float, day_high: float, day_vwap: float | None,
                          rs_spy: float, rs_sector: float, event_valid_next_session: bool,
                          cfg: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    reasons: list[str] = []
    close_location = ((close_price - day_low) / (day_high - day_low)
                      if day_high > day_low else None)
    if cfg.get("exclude_friday", True) and getattr(session_date, "weekday", lambda: 0)() == 4:
        reasons.append("FRIDAY_EXCLUDED")
    if str(event_type).lower() in {str(x).lower() for x in cfg.get("excluded_event_types", [])}:
        reasons.append("EVENT_TYPE_EXCLUDED")
    if close_location is None or close_location < float(cfg.get("min_close_location", 0.8)):
        reasons.append("WEAK_CLOSE_LOCATION")
    if cfg.get("require_above_vwap", True) and (day_vwap is None or close_price < day_vwap):
        reasons.append("CLOSE_BELOW_VWAP")
    if cfg.get("require_positive_relative_strength", True) and (rs_spy <= 0 or rs_sector <= 0):
        reasons.append("RELATIVE_STRENGTH_NOT_POSITIVE")
    if not event_valid_next_session:
        reasons.append("CATALYST_EXPIRED")
    return not reasons, reasons, {"close_location": close_location, "close_vwap": day_vwap}


def _counterfactual_net(entry: float, exit_price: float | None, risk_per_share: float,
                        risk_usd: float | None, symbol: str, fee_profile: str) -> float | None:
    if exit_price is None or risk_usd is None or risk_per_share <= 0:
        return None
    qty = float(risk_usd) / risk_per_share
    gross = (float(exit_price) - entry) * qty
    costs = trade_costs(notional_usdt=qty * entry, exit_notional_usdt=qty * float(exit_price),
                        symbol=symbol, fee_profile=fee_profile,
                        entry_order_type="taker", exit_order_type="taker")
    return round(gross - costs.total_cost_usdt, 4)


def _coverage_clean(day: pd.DataFrame, expected_minutes: int) -> bool:
    if len(day) < 2:
        return False
    gaps = day["timestamp"].sort_values().diff().dropna().dt.total_seconds() / 60.0
    return bool(gaps.empty or float(gaps.max()) <= expected_minutes * 2.1)


def evaluate_candidate(
    *, event: dict[str, Any], symbol: str, stock_bars: Any, daily_bars: Any,
    spy_bars: Any, sector_bars: Any, sector: str, sector_etf: str,
    coverage_clean: bool | None = None, cfg: dict[str, Any] | None = None,
    window: str = "forward_post_activation", generated_at: datetime | None = None,
) -> dict[str, Any]:
    cfg = cfg or load_strategy_config()
    generated_at = generated_at or utc_now()
    published_at = parse_dt(event.get("published_at"))
    event_at = parse_dt(event.get("available_at")) or published_at
    event_id = str(event.get("event_id") or event.get("news_item_id") or "unknown")
    decision_fallback = event_at or generated_at
    base = {
        "candidate_id": _candidate_id(cfg["strategy_id"], event_id, symbol, cfg["profile_id"]),
        "strategy_id": cfg["strategy_id"], "profile_id": cfg["profile_id"],
        "shadow_lane": cfg["shadow_lane"], "window": window,
        "generated_at": generated_at.isoformat(), "decision_at": decision_fallback.isoformat(),
        "catalyst_at": published_at.isoformat() if published_at else None, "news_event_id": event_id,
        "symbol": symbol.upper(), "direction": "long", "sector": sector, "sector_etf": sector_etf,
        "market_regime": "unknown", "catalyst_type": str(event.get("event_type") or "unknown").lower(),
        "catalyst_source_quality": str(event.get("source_quality") or "unknown").lower(),
        "evidence_cohort": str(event.get("evidence_cohort") or "unclassified"),
        "source_trust_tier": str(event.get("source_trust_tier") or "unclassified"),
        "candidate_origin": str(event.get("candidate_origin") or "canonical"),
        "eligibility_status": "rejected", "rejection_reason": None, "data_status": "clean",
        "is_clean_for_edge": 1, "entry_ts": None, "entry_price": None, "stop_price": None,
        "tp1": None, "tp2": None, "tp3": None, "gap_or_impulse_pct": None, "rvol": None,
        "rs_spy_pct": None, "rs_sector_pct": None, "outcome_status": "skipped",
        "close_reason": None, "exit_price": None, "exit_ts": None, "gross_pnl_usd": None,
        "net_pnl_usd": None,
        "net_r": None, "fees_usd": 0.0, "slippage_usd": 0.0, "funding_usd": 0.0,
        "funding_source": "not_applicable", "funding_estimated": 0, "funding_event_count": 0,
        "risk_usd": None, "mfe_r": None, "mae_r": None, "protection_armed": 0,
        "lock_armed": 0, "highest_tp_touched": 0, "bars_held": 0, "latency_seconds": None,
        "tradable_latency_seconds": None, "catalyst_age_at_entry_seconds": None,
        "source_ingestion_latency_seconds": None,
        "overnight_eligible": 0, "overnight_reasons_json": "[]",
        "would_have_held_open_next_session": None, "would_have_held_close_next_session": None,
        "would_next_open_net_pnl_usd": None, "would_next_close_net_pnl_usd": None,
        "features_json": "{}", "notes_json": "{}",
    }

    def reject(reason: str, features: dict[str, Any], *, dirty: bool = False) -> dict[str, Any]:
        if reason not in REJECTION_REASONS:
            raise ValueError(f"unregistered rejection reason: {reason}")
        base["rejection_reason"] = reason
        base["features_json"] = json_text(features)
        if dirty:
            base["data_status"], base["is_clean_for_edge"] = "dirty", 0
        return base

    if published_at is None or event_at is None:
        return reject("CATALYST_TIME_UNKNOWN", {}, dirty=True)
    if not bool(event.get("linkage_allowed", True)) or symbol.upper() not in {
        str(x).split("/")[0].upper() for x in event.get("trusted_symbols", [symbol])
    }:
        return reject("CATALYST_UNTRUSTED", {"event": event})
    if base["catalyst_type"] in set(cfg["excluded_event_types"]):
        return reject("CATALYST_TYPE_EXCLUDED", {"event_type": base["catalyst_type"]})
    source_quality = base["catalyst_source_quality"]
    corroboration = max(int(event.get("corroboration_count") or 0),
                        int(event.get("independent_non_social_count") or 0))
    trusted_quality = source_quality in {str(x).lower() for x in cfg["trusted_source_qualities"]}
    secondary_confirmed = (source_quality == "secondary"
                           and corroboration >= int(cfg["min_secondary_corroboration"]))
    explicit_trust = str(event.get("source_trust_tier") or "").lower()
    exploratory_secondary = explicit_trust == "exploratory_single_secondary"
    if not exploratory_secondary and source_quality == "secondary" \
            and cfg.get("exploratory_single_secondary_enabled", False):
        exploratory_secondary = (
            base["catalyst_type"] in {str(x).lower() for x in cfg.get("exploratory_secondary_event_types", [])}
            and str(event.get("content_level") or "unknown").lower() != "title_only"
            and not _title_is_speculative(event.get("title"), cfg)
            and int(event.get("independent_non_social_count") or 1) >= 1
        )
    if not trusted_quality and not secondary_confirmed and not exploratory_secondary:
        return reject("CATALYST_UNTRUSTED", {
            "source_quality": source_quality, "corroboration": corroboration,
        })
    if explicit_trust:
        base["source_trust_tier"] = explicit_trust
    elif trusted_quality:
        base["source_trust_tier"] = "trusted_primary_or_reputable"
    elif secondary_confirmed:
        base["source_trust_tier"] = "corroborated_secondary"
    else:
        base["source_trust_tier"] = "exploratory_single_secondary"
    strict_source = base["source_trust_tier"] in {
        "trusted_primary_or_reputable", "corroborated_secondary",
    }
    base["evidence_cohort"] = "strict_v1" if strict_source else "exploratory_v1"

    stock = _rth(normalize_frame(stock_bars))
    daily = normalize_frame(daily_bars)
    spy = _rth(normalize_frame(spy_bars))
    sector_frame = _rth(normalize_frame(sector_bars))
    if stock.empty or daily.empty:
        return reject("STOCK_BARS_MISSING", {}, dirty=True)
    eligible = stock[stock["timestamp"] >= pd.Timestamp(event_at)]
    if eligible.empty:
        # Premarket catalyst: use the first following RTH bar. After-hours naturally rolls forward.
        eligible = stock[stock["timestamp"].dt.tz_convert(NY).dt.date >= event_at.astimezone(NY).date()]
    if eligible.empty:
        return reject("NOT_RTH", {}, dirty=True)
    first_pos = int(eligible.index[0])
    first_ts = stock.loc[first_pos, "timestamp"]
    if _is_rth(event_at) and (
        first_ts.to_pydatetime() - event_at
    ) > timedelta(minutes=float(cfg.get("max_entry_data_gap_minutes", 20))):
        return reject("DATA_COVERAGE_DIRTY", {
            "event_at": event_at.isoformat(), "first_bar": first_ts.isoformat(),
            "reason": "late_first_bar_after_rth_catalyst",
        }, dirty=True)
    session_date = stock.loc[first_pos, "timestamp"].tz_convert(NY).date()
    session_mask = stock["timestamp"].dt.tz_convert(NY).dt.date == session_date
    day = stock[session_mask].reset_index(drop=True)
    day_positions = day.index[day["timestamp"] == first_ts].tolist()
    if not day_positions:
        return reject("NOT_RTH", {}, dirty=True)
    initial = int(day_positions[0])
    if initial + 1 >= len(day):
        return reject("CONFIRMATION_CLOSE_MISSING", {}, dirty=True)
    first_bar_close = first_ts.to_pydatetime() + timedelta(minutes=int(cfg["confirmation_minutes"]))
    if first_bar_close - published_at > timedelta(hours=float(cfg["catalyst_freshness_hours"])):
        return reject("CATALYST_STALE", {
            "age_hours_at_first_observable_bar": (first_bar_close - published_at).total_seconds() / 3600.0,
        })

    prior_close = _previous_close(daily, event_at)
    if prior_close is None:
        return reject("STOCK_BARS_MISSING", {"missing": "previous_close"}, dirty=True)
    impulse_end = first_ts + pd.Timedelta(minutes=float(cfg["impulse_window_minutes"]))
    bar_minutes = float(cfg["confirmation_minutes"])
    # A bar is evidence only after it closes. With 15m bars and a 20m impulse
    # window, the 09:45 bar closes at 10:00 and must not leak into the window.
    impulse = day[(day["timestamp"] >= first_ts) &
                  (day["timestamp"] + pd.Timedelta(minutes=bar_minutes) <= impulse_end)]
    impulse_high = float(impulse["high"].astype(float).max())
    impulse_pct = (impulse_high / prior_close - 1.0) * 100.0
    base["gap_or_impulse_pct"] = round(impulse_pct, 4)
    if impulse_pct < float(cfg["min_gap_or_impulse_pct"]):
        return reject("IMPULSE_BELOW_THRESHOLD", {"impulse_pct": impulse_pct})
    prior_vol = stock[stock["timestamp"] < first_ts]["volume"].astype(float).tail(int(cfg["rvol_baseline_bars"]))
    rvol = (float(impulse["volume"].astype(float).mean()) / float(prior_vol.mean())
            if len(prior_vol) and prior_vol.mean() else None)
    base["rvol"] = round(rvol, 4) if rvol is not None else None
    if rvol is None or rvol < float(cfg["min_rvol"]):
        return reject("RVOL_BELOW_THRESHOLD", {"rvol": rvol})

    opening_high = float(day.loc[initial, "high"])
    confirm_idx = None
    first_candidate = initial + 1  # explicitly blocks the first impulse bar
    for idx in range(first_candidate, len(day)):
        close = float(day.loc[idx, "close"])
        if close <= opening_high:
            continue
        vwap = _vwap(day, idx)
        if vwap is None or close < vwap:
            continue
        confirm_idx = idx
        break
    if confirm_idx is None:
        return reject("ORH_NOT_CONFIRMED", {"opening_range_high": opening_high})
    if confirm_idx == initial:
        return reject("FIRST_BAR_ENTRY_BLOCKED", {})
    # Intraday cache timestamps are bar-open timestamps. The close used for
    # confirmation cannot be acted on until the configured bar has completed.
    decision_at = (day.loc[confirm_idx, "timestamp"].to_pydatetime()
                   + timedelta(minutes=int(cfg["confirmation_minutes"])))
    base["decision_at"] = decision_at.isoformat()
    base["entry_ts"] = decision_at.isoformat()
    entry = float(day.loc[confirm_idx, "close"])
    vwap = _vwap(day, confirm_idx)
    if vwap is None or entry < vwap:
        return reject("VWAP_NOT_RECLAIMED", {"vwap": vwap})

    spy_ret = _return_between(spy, published_at, decision_at, int(cfg["confirmation_minutes"]))
    sector_ret = _return_between(sector_frame, published_at, decision_at, int(cfg["confirmation_minutes"]))
    stock_ret = (entry / prior_close - 1.0) * 100.0
    if spy_ret is None:
        return reject("MARKET_CONTEXT_MISSING", {}, dirty=True)
    if sector_ret is None:
        return reject("SECTOR_CONTEXT_MISSING", {}, dirty=True)
    _, spy_ts = _close_at_or_before(spy, decision_at, int(cfg["confirmation_minutes"]))
    _, sector_ts = _close_at_or_before(sector_frame, decision_at, int(cfg["confirmation_minutes"]))
    max_age = timedelta(minutes=float(cfg["max_market_data_age_minutes"]))
    if spy_ts is None or decision_at - spy_ts > max_age:
        return reject("MARKET_CONTEXT_STALE", {"spy_ts": spy_ts}, dirty=True)
    if sector_ts is None or decision_at - sector_ts > max_age:
        return reject("SECTOR_CONTEXT_STALE", {"sector_ts": sector_ts}, dirty=True)
    rs_spy, rs_sector = stock_ret - spy_ret, stock_ret - sector_ret
    base["rs_spy_pct"], base["rs_sector_pct"] = round(rs_spy, 4), round(rs_sector, 4)
    base["market_regime"] = "risk_on" if spy_ret >= 0 else "risk_off"
    if rs_spy < float(cfg["min_rs_spy_pct"]):
        return reject("RS_SPY_TOO_WEAK", {"stock_return": stock_ret, "spy_return": spy_ret})
    if rs_sector < float(cfg["min_rs_sector_pct"]):
        return reject("RS_SECTOR_TOO_WEAK", {"stock_return": stock_ret, "sector_return": sector_ret})
    dollar_volume = float((day.iloc[:confirm_idx + 1]["close"].astype(float) *
                           day.iloc[:confirm_idx + 1]["volume"].astype(float)).sum())
    if dollar_volume < float(cfg["min_dollar_volume"]):
        return reject("LIQUIDITY_TOO_LOW", {"dollar_volume": dollar_volume})

    adr = _adr(daily, decision_at, int(cfg["adr_lookback_days"]))
    if adr is None:
        return reject("ADR_MISSING", {}, dirty=True)
    low_of_day = float(day.iloc[:confirm_idx + 1]["low"].astype(float).min())
    midpoint = (float(day.loc[confirm_idx, "high"]) + float(day.loc[confirm_idx, "low"])) / 2.0
    stop = max(low_of_day, midpoint)  # higher stop is narrower for a long
    if stop >= entry:
        return reject("STOP_INVALID", {"entry": entry, "stop": stop})
    if entry - stop > adr * float(cfg["max_stop_adr_multiple"]):
        return reject("STOP_WIDER_THAN_ADR", {"risk": entry - stop, "adr": adr})
    clean = _coverage_clean(day.iloc[:confirm_idx + 1], int(cfg["confirmation_minutes"]))
    if coverage_clean is not None:
        clean = clean and bool(coverage_clean)
    if not clean:
        return reject("DATA_COVERAGE_DIRTY", {"session_bars": confirm_idx + 1}, dirty=True)

    strict_thresholds_passed = (
        impulse_pct >= float(cfg.get("strict_min_gap_or_impulse_pct", 5.0))
        and rvol is not None and rvol >= float(cfg.get("strict_min_rvol", 1.5))
        and rs_spy >= float(cfg.get("strict_min_rs_spy_pct", 0.25))
        and rs_sector >= float(cfg.get("strict_min_rs_sector_pct", 0.15))
    )
    base["evidence_cohort"] = (
        "strict_v1" if strict_source and strict_thresholds_passed else "exploratory_v1"
    )
    risk = entry - stop
    targets = [entry + float(r) * risk for r in cfg["target_r"]]
    base.update(entry_price=entry, stop_price=stop, tp1=targets[0], tp2=targets[1], tp3=targets[2])
    future = day.iloc[confirm_idx + 1:]
    if future.empty:
        return reject("NO_SAME_DAY_EXIT_BAR", {"decision_at": decision_at.isoformat()}, dirty=True)
    last_bar_close = (day.iloc[-1]["timestamp"].to_pydatetime()
                      + timedelta(minutes=int(cfg["confirmation_minutes"])))
    session_complete = last_bar_close.astimezone(NY).time() >= time(16, 0)
    sim = simulate_confirmed_close_entry(
        direction="long", entry=entry, stop=stop, tp1=targets[0], tp2=targets[1], tp3=targets[2],
        future_candles=future, symbol=symbol.upper(), fee_profile=cfg["fee_profile"],
        funding_rate_8h=None, funding_intervals=0.0, entry_at=decision_at,
        bar_minutes=int(cfg["confirmation_minutes"]), force_close=session_complete,
    )
    base["eligibility_status"] = "eligible"
    for key, value in sim.to_dict().items():
        target = "outcome_status" if key == "status" else key
        if target in base:
            base[target] = value
    # Keep three clocks separate. An after-hours catalyst can legitimately wait
    # for the next RTH session; that closed-market interval is news age, not
    # execution latency or a data-pipeline outage.
    first_actionable_at = max(event_at, first_ts.to_pydatetime())
    tradable_latency = max(0.0, (decision_at - first_actionable_at).total_seconds())
    catalyst_age = max(0.0, (decision_at - published_at).total_seconds())
    ingestion_latency = max(0.0, (event_at - published_at).total_seconds())
    base["latency_seconds"] = tradable_latency
    base["tradable_latency_seconds"] = tradable_latency
    base["catalyst_age_at_entry_seconds"] = catalyst_age
    base["source_ingestion_latency_seconds"] = ingestion_latency
    overnight_features: dict[str, Any] = {}
    if bool(cfg.get("log_next_session_close")):
        next_open, next_open_at, next_close, next_close_at = _next_session_prices(
            stock, session_date, int(cfg["confirmation_minutes"])
        )
        expires_at = parse_dt(event.get("expires_at"))
        next_reference = next_open_at or next_close_at
        event_valid = expires_at is None or (next_reference is not None and expires_at >= next_reference)
        overnight_cfg = cfg.get("overnight_context") or context_filter_config("catalyst_overnight")
        day_close = float(day.iloc[-1]["close"])
        day_low = float(day["low"].astype(float).min())
        day_high = float(day["high"].astype(float).max())
        day_vwap = _vwap(day, len(day) - 1)
        eligible_overnight, overnight_reasons, overnight_features = overnight_eligibility(
            session_date=session_date, event_type=base["catalyst_type"], close_price=day_close,
            day_low=day_low, day_high=day_high, day_vwap=day_vwap,
            rs_spy=rs_spy, rs_sector=rs_sector, event_valid_next_session=event_valid,
            cfg=overnight_cfg,
        )
        base["overnight_eligible"] = int(eligible_overnight)
        base["overnight_reasons_json"] = json_text(overnight_reasons)
        if eligible_overnight:
            base["would_have_held_open_next_session"] = next_open
            base["would_have_held_close_next_session"] = next_close
            base["would_next_open_net_pnl_usd"] = _counterfactual_net(
                entry, next_open, risk, base.get("risk_usd"), symbol.upper(), cfg["fee_profile"])
            base["would_next_close_net_pnl_usd"] = _counterfactual_net(
                entry, next_close, risk, base.get("risk_usd"), symbol.upper(), cfg["fee_profile"])
    base["features_json"] = json_text({
        "event": {k: event.get(k) for k in ("event_id", "event_type", "source_quality", "published_at",
                                             "available_at", "expires_at")},
        "latency": {
            "definition": "tradable_opportunity_to_confirmed_entry",
            "first_actionable_at": first_actionable_at.isoformat(),
            "tradable_latency_seconds": tradable_latency,
            "catalyst_age_at_entry_seconds": catalyst_age,
            "source_ingestion_latency_seconds": ingestion_latency,
        },
        "impulse_pct": impulse_pct, "rvol": rvol, "opening_range_high": opening_high,
        "vwap": vwap, "stock_return_pct": stock_ret, "spy_return_pct": spy_ret,
        "sector_return_pct": sector_ret, "rs_spy_pct": rs_spy, "rs_sector_pct": rs_sector,
        "dollar_volume": dollar_volume, "adr20": adr, "coverage_clean": clean,
        "evidence_cohort": base["evidence_cohort"], "source_trust_tier": base["source_trust_tier"],
        "candidate_origin": base["candidate_origin"],
        "strict_thresholds_passed": strict_thresholds_passed,
        "overnight": {"eligible": bool(base["overnight_eligible"]),
                      "reasons": json.loads(base["overnight_reasons_json"]), **overnight_features},
    })
    base["protection_armed"] = int(bool(base["protection_armed"]))
    base["lock_armed"] = int(bool(base["lock_armed"]))
    return base


def _universe(cfg: dict[str, Any] | None = None) -> tuple[set[str], dict[str, str], dict[str, str]]:
    try:
        raw = yaml.safe_load(UNIVERSE_PATH.read_text(encoding="utf-8")) or {}
    except Exception:
        raw = {}
    symbol_sector = {str(k).upper(): str(v) for k, v in (raw.get("symbol_sector_map") or {}).items()}
    sector_etfs = {str(k): str(v).upper() for k, v in (raw.get("sector_etfs") or {}).items()}
    sector_etfs.update({
        str(k): str(v).upper()
        for k, v in ((cfg or {}).get("sector_benchmark_overrides") or {}).items()
    })
    benchmarks = {str(x).upper() for x in raw.get("indices", [])} | set(sector_etfs.values())
    symbols = {str(x).upper() for x in raw.get("default_symbols", [])} - benchmarks
    return symbols, symbol_sector, sector_etfs


def _event_symbols(raw: Any) -> list[str]:
    try:
        values = json.loads(raw or "[]") if isinstance(raw, str) else (raw or [])
        return sorted({str(x).split("/")[0].upper() for x in values})
    except (TypeError, ValueError):
        return []


def _event_rows(conn: sqlite3.Connection, cfg: dict[str, Any], now: datetime) -> list[dict[str, Any]]:
    if not table_exists(conn, "news_canonical_events"):
        return []
    start = now - timedelta(hours=float(cfg["catalyst_lookback_hours"]))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM news_canonical_events WHERE lower(COALESCE(asset_class,''))='stocks' "
        "AND linkage_allowed=1 AND is_cluster_primary=1 AND effective_at>=? AND effective_at<=? "
        "ORDER BY effective_at", (start.isoformat(), now.isoformat()),
    ).fetchall()
    out = []
    for row in rows:
        item = dict(row)
        item["trusted_symbols"] = _event_symbols(item.get("trusted_symbols_json"))
        published = parse_dt(item.get("published_at") or item.get("effective_at"))
        materialized = parse_dt(item.get("created_at"))
        available = max(x for x in (published, materialized) if x is not None) if (published or materialized) else None
        item["available_at"] = available.isoformat() if available else None
        if available is not None and available <= now:
            out.append(item)
    return out


def _event_candidates(
    conn: sqlite3.Connection, cfg: dict[str, Any], now: datetime,
    universe: set[str], sector_by_symbol: dict[str, str], etf_by_sector: dict[str, str],
    *, start_at: datetime | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Build an auditable Shadow-only catalyst funnel from canonical news rows.

    The production canonical policy is not changed.  This strategy may recover
    narrowly defined event types and title-leading tracked tickers, and labels
    every such candidate so exploratory evidence cannot masquerade as strict.
    """
    funnel: Counter[str] = Counter()
    upstream: Counter[str] = Counter()
    by_type: Counter[str] = Counter()
    by_origin: Counter[str] = Counter()
    by_trust: Counter[str] = Counter()
    if not table_exists(conn, "news_canonical_events"):
        return [], {"status": "unavailable", "upstream_rejections": {"TABLE_MISSING": 1}}
    start = start_at or (now - timedelta(hours=float(cfg["catalyst_lookback_hours"])))
    conn.row_factory = sqlite3.Row
    raw_rows = [dict(row) for row in conn.execute(
        "SELECT * FROM news_canonical_events WHERE lower(COALESCE(asset_class,''))='stocks' "
        "AND effective_at<=? AND (effective_at>=? OR created_at>=?) "
        "ORDER BY effective_at,news_item_id",
        (now.isoformat(), start.isoformat(), start.isoformat()),
    ).fetchall()]
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    excluded = {str(value).lower() for value in cfg.get("excluded_event_types", [])}
    blocked_symbols = {"SPY", "QQQ", "IWM", "DIA"}
    funnel["canonical_rows"] = len(raw_rows)

    for raw in raw_rows:
        available = _event_available_at(raw)
        if available is None:
            upstream["CATALYST_TIME_UNKNOWN"] += 1
            continue
        if available > now:
            upstream["FUTURE_MATERIALIZATION"] += 1
            continue
        if available < start:
            upstream["EVENT_BEFORE_WINDOW"] += 1
            continue
        funnel["point_in_time_visible_rows"] += 1
        event_type, taxonomy_origin = _local_event_type(raw)
        raw["event_type"] = event_type
        symbols, symbol_origin = _shadow_subject_symbols(raw, universe, event_type)
        if not symbols:
            upstream["NO_SUBJECT_SYMBOL"] += 1
            continue
        funnel["rows_with_subject_symbol"] += 1
        for symbol in symbols:
            if symbol in blocked_symbols:
                upstream["BENCHMARK_SYMBOL_EXCLUDED"] += 1
                continue
            if symbol not in universe:
                upstream["SYMBOL_NOT_IN_UNIVERSE"] += 1
                continue
            sector = sector_by_symbol.get(symbol)
            sector_etf = etf_by_sector.get(sector or "")
            if not sector or not sector_etf:
                upstream["SECTOR_BENCHMARK_MISSING"] += 1
                continue
            if event_type in excluded:
                upstream["EVENT_TYPE_EXCLUDED"] += 1
                by_type[event_type] += 1
                continue
            # A specialised derivative lane (for example earnings-gap) may
            # explicitly narrow the otherwise broad Catalyst-RS taxonomy.  An
            # empty list is meaningful here: it admits no directional events.
            # The legacy ``extra_*`` option remains additive for Catalyst-RS.
            if "allowed_directional_event_types" in cfg:
                directional_types = {
                    str(value).lower() for value in cfg.get("allowed_directional_event_types", [])
                }
            else:
                directional_types = _LOCAL_DIRECTIONAL_TYPES | {
                    str(value).lower() for value in cfg.get("extra_directional_event_types", [])
                }
            if event_type not in directional_types:
                upstream["EVENT_TYPE_NOT_SUPPORTED"] += 1
                by_type[event_type] += 1
                continue
            item = dict(raw)
            item["available_at"] = available.isoformat()
            item["_symbol"] = symbol
            item["_sector"] = sector
            item["_sector_etf"] = sector_etf
            if taxonomy_origin != "canonical":
                origin = taxonomy_origin
            elif symbol_origin != "canonical_subject":
                origin = symbol_origin
            elif int(raw.get("linkage_allowed") or 0) == 1:
                origin = "canonical_linked"
            else:
                origin = "canonical_subject_recovered"
            item["candidate_origin"] = origin
            groups[_event_group_key(symbol, event_type, item)].append(item)

    candidates: list[dict[str, Any]] = []
    for group_key, members in sorted(groups.items()):
        tier, trigger, corroboration, non_social = _trust_trigger(members, cfg)
        seed = min(members, key=lambda item: (_event_available_at(item) or now,
                                              int(item.get("news_item_id") or 0)))
        event = dict(trigger or seed)
        event["event_id"] = str(seed.get("event_id") or f"shadow_{hashlib.sha1(group_key.encode()).hexdigest()[:16]}")
        event["published_at"] = trigger.get("published_at") or trigger.get("effective_at")
        trigger_available = _event_available_at(trigger)
        event["available_at"] = trigger_available.isoformat() if trigger_available else None
        event["trusted_symbols"] = [str(seed["_symbol"])]
        event["linkage_allowed"] = True
        event["source_trust_tier"] = tier
        event["candidate_origin"] = str(trigger.get("candidate_origin") or seed.get("candidate_origin") or "canonical")
        event["corroboration_count"] = corroboration
        event["independent_non_social_count"] = non_social
        event["cluster_member_count"] = len(members)
        event["cluster_event_ids"] = [str(member.get("event_id")) for member in members]
        event["evidence_cohort"] = (
            "strict_v1" if tier in {"trusted_primary_or_reputable", "corroborated_secondary"}
            else "exploratory_v1" if tier == "exploratory_single_secondary" else "unclassified"
        )
        candidates.append({
            "event": event, "symbol": str(seed["_symbol"]), "sector": str(seed["_sector"]),
            "sector_etf": str(seed["_sector_etf"]), "group_key": group_key,
        })
        by_type[str(event.get("event_type") or "unknown")] += 1
        by_origin[str(event.get("candidate_origin") or "unknown")] += 1
        by_trust[tier] += 1

    funnel["candidate_groups"] = len(groups)
    funnel["candidates_emitted"] = len(candidates)
    return candidates, {
        "status": "ok", **dict(funnel),
        "upstream_rejections": dict(sorted(upstream.items())),
        "by_event_type": dict(sorted(by_type.items())),
        "by_candidate_origin": dict(sorted(by_origin.items())),
        "by_source_trust_tier": dict(sorted(by_trust.items())),
    }


def _coverage_status(conn: sqlite3.Connection, symbol: str, as_of: datetime) -> bool | None:
    if not table_exists(conn, "stock_coverage_by_mode"):
        return None
    row = conn.execute(
        "SELECT is_clean,status,missing_bars,computed_at FROM stock_coverage_by_mode "
        "WHERE upper(symbol)=? AND mode='intraday' "
        "ORDER BY computed_at DESC LIMIT 1", (symbol.upper(),),
    ).fetchone()
    if not row:
        return None
    computed_at = parse_dt(row[3])
    if computed_at is None or computed_at.astimezone(NY).date() != as_of.astimezone(NY).date():
        return None
    status = str(row[1] or "unknown").upper()
    if status in {"SESSION_WARMUP", "MARKET_CLOSED", "NOT_APPLICABLE"} \
            and int(row[2] or 0) == 0:
        return None
    return bool(row[0])


def _all_rows(conn: sqlite3.Connection, profile_id: str | None = None) -> list[dict[str, Any]]:
    conn.row_factory = sqlite3.Row
    if profile_id is None:
        query, args = "SELECT * FROM stocks_catalyst_rs_shadow_outcomes", ()
    else:
        query, args = "SELECT * FROM stocks_catalyst_rs_shadow_outcomes WHERE profile_id=?", (profile_id,)
    return [dict(r) for r in conn.execute(query, args)]


def _evidence_summaries(
    rows: list[dict[str, Any]], *, activated_at: str, now: datetime, cfg: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    kwargs = {
        "activated_at": activated_at, "now": now, "min_closed": int(cfg["min_clean_closed"]),
        "min_days": float(cfg["min_forward_days"]), "min_pf": float(cfg["min_profit_factor"]),
        "max_review_drawdown_usd": float(cfg["max_review_drawdown_usd"]),
    }
    all_summary = clean_forward_summary(rows, **kwargs)
    strict_summary = clean_forward_summary(
        [row for row in rows if row.get("evidence_cohort") == "strict_v1"], **kwargs,
    )
    exploratory_summary = clean_forward_summary(
        [row for row in rows if row.get("evidence_cohort") == "exploratory_v1"], **kwargs,
    )
    # The headline shows everything the lane simulated, while promotion remains
    # based only on the original strict thresholds and trusted-source cohort.
    all_summary["verdict"] = strict_summary["verdict"]
    all_summary["review_checks"] = strict_summary["review_checks"]
    all_summary["promotion_evidence_cohort"] = "strict_v1"
    return all_summary, strict_summary, exploratory_summary


def _latency_aware_diagnostics(
    rows: list[dict[str, Any]], *, group_keys: tuple[str, ...],
) -> dict[str, Any]:
    """Build SLA diagnostics without treating closed-market waits as latency."""
    diagnostic_rows: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["latency_seconds"] = row.get("tradable_latency_seconds")
        diagnostic_rows.append(item)
    diagnostics = strategy_diagnostics(diagnostic_rows, group_keys=group_keys)
    catalyst_ages = [
        float(row["catalyst_age_at_entry_seconds"])
        for row in rows if row.get("catalyst_age_at_entry_seconds") is not None
    ]
    ingestion = [
        float(row["source_ingestion_latency_seconds"])
        for row in rows if row.get("source_ingestion_latency_seconds") is not None
    ]
    diagnostics.update({
        "latency_definition": "tradable_opportunity_to_confirmed_entry",
        "avg_catalyst_age_at_entry_seconds": (
            sum(catalyst_ages) / len(catalyst_ages) if catalyst_ages else None
        ),
        "avg_source_ingestion_latency_seconds": (
            sum(ingestion) / len(ingestion) if ingestion else None
        ),
        "legacy_wall_clock_latency_rows_excluded": sum(
            row.get("latency_seconds") is not None
            and row.get("tradable_latency_seconds") is None
            for row in rows
        ),
    })
    return diagnostics


def refresh(*, db: str | None = None, persist: bool = True, backfill: bool = False,
            now: datetime | None = None, cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = cfg or load_strategy_config()
    now = now or utc_now()
    path = Path(db) if db else Path(load_config().db_path)
    if not bool(cfg.get("feature_flag")):
        return {"enabled": False, "generated_at": now.isoformat(), "strategy_id": cfg["strategy_id"],
                "shadow_lane": cfg["shadow_lane"], "rows": [], "summary": {},
                "reason": "feature_flag_false"}
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        ensure_tables(conn)
        # Schema repair must not keep a write lease while candidates are
        # loaded and simulated. Paper entry workers share this SQLite file.
        conn.commit()
        activation_key = f"activated_at:{cfg['profile_id']}"
        activation_row = conn.execute(
            "SELECT v FROM stocks_catalyst_rs_shadow_meta WHERE k=?", (activation_key,),
        ).fetchone()
        if activation_row:
            activated_at = str(activation_row[0])
        else:
            activated_at = now.isoformat()
            if persist:
                conn.execute(
                    "INSERT INTO stocks_catalyst_rs_shadow_meta(k,v) VALUES (?,?)",
                    (activation_key, activated_at),
                )
                conn.commit()
        symbols, sector_by_symbol, etf_by_sector = _universe(cfg)
        fs = FileStore(load_config())
        spy = fs.load_stocks_ohlcv("SPY", cfg["timeframe"])
        rows = []
        candidate_specs, candidate_funnel = _event_candidates(
            conn, cfg, now, symbols, sector_by_symbol, etf_by_sector,
        )
        for spec in candidate_specs:
            event = spec["event"]
            symbol = str(spec["symbol"])
            sector = str(spec["sector"])
            sector_etf = str(spec["sector_etf"])
            event_at = parse_dt(event.get("available_at")) or now
            activation = parse_dt(activated_at)
            window = ("historical_backfill" if backfill or not activation or event_at < activation
                      else "forward_post_activation")
            row = evaluate_candidate(
                event=event, symbol=symbol,
                stock_bars=fs.load_stocks_ohlcv(symbol, cfg["timeframe"]),
                daily_bars=fs.load_stocks_ohlcv(symbol, "1d"), spy_bars=spy,
                sector_bars=fs.load_stocks_ohlcv(sector_etf, cfg["timeframe"]),
                sector=sector, sector_etf=sector_etf,
                coverage_clean=_coverage_status(conn, symbol, event_at), cfg=cfg, window=window,
                generated_at=now,
            )
            rows.append(row)
        if persist and rows:
            preserve_first_observation(conn, "stocks_catalyst_rs_shadow_outcomes", rows)
            sql = ("INSERT OR REPLACE INTO stocks_catalyst_rs_shadow_outcomes (" + ",".join(OUTCOME_COLUMNS)
                   + ") VALUES (" + ",".join("?" for _ in OUTCOME_COLUMNS) + ")")
            conn.executemany(sql, [tuple(row.get(col) for col in OUTCOME_COLUMNS) for row in rows])
            # Release the writer before the full evidence diagnostics below.
            conn.commit()
        stored_rows = _all_rows(conn, cfg["profile_id"])
        if persist:
            all_rows = stored_rows
        else:
            merged = {str(row.get("candidate_id")): row for row in stored_rows}
            merged.update({str(row.get("candidate_id")): row for row in rows})
            all_rows = list(merged.values())
        summary, strict_summary, exploratory_summary = _evidence_summaries(
            all_rows, activated_at=activated_at, now=now, cfg=cfg,
        )
        historical_rows = [
            {**row, "window": "forward_post_activation"}
            for row in all_rows if row.get("window") == "historical_backfill"
        ]
        historical_summary = clean_forward_summary(
            historical_rows, activated_at=activated_at, now=now,
            min_closed=int(cfg["min_clean_closed"]), min_days=float(cfg["min_forward_days"]),
            min_pf=float(cfg["min_profit_factor"]),
            max_review_drawdown_usd=float(cfg["max_review_drawdown_usd"]),
        )
        historical_summary["verdict"] = "MEASUREMENT_ONLY"
        rejection_counts: dict[str, dict[str, int]] = {
            "forward_post_activation": {}, "historical_backfill": {},
        }
        by_sector: dict[str, dict[str, float]] = {}
        for row in all_rows:
            if row.get("rejection_reason"):
                window_counts = rejection_counts.setdefault(str(row.get("window") or "unclassified"), {})
                reason = str(row["rejection_reason"])
                window_counts[reason] = window_counts.get(reason, 0) + 1
            if (row.get("window") == "forward_post_activation" and row.get("outcome_status") == "closed"
                    and int(row.get("is_clean_for_edge") or 0) == 1):
                sector = str(row.get("sector") or "unknown")
                block = by_sector.setdefault(sector, {"closed": 0, "net_pnl_usd": 0.0})
                block["closed"] += 1
                block["net_pnl_usd"] += float(row.get("net_pnl_usd") or 0.0)
        diagnostics = _latency_aware_diagnostics(
            all_rows, group_keys=("evidence_cohort", "source_trust_tier", "candidate_origin", "sector",
                                  "market_regime", "catalyst_type", "catalyst_source_quality"),
        )
        diagnostics["candidate_funnel"] = candidate_funnel
        diagnostics["strict_promotion_summary"] = strict_summary
        diagnostics["exploratory_summary"] = exploratory_summary
        diagnostics["historical_backfill_summary"] = historical_summary
        overnight_rows = [r for r in all_rows if r.get("window") == "forward_post_activation"
                          and int(r.get("is_clean_for_edge") or 0) == 1
                          and int(r.get("overnight_eligible") or 0) == 1]
        diagnostics["overnight_counterfactual"] = {
            "eligible": len(overnight_rows),
            "next_open_resolved": sum(r.get("would_next_open_net_pnl_usd") is not None for r in overnight_rows),
            "next_close_resolved": sum(r.get("would_next_close_net_pnl_usd") is not None for r in overnight_rows),
            "next_open_net_pnl_usd": round(sum(float(r.get("would_next_open_net_pnl_usd") or 0.0)
                                                   for r in overnight_rows), 4),
            "next_close_net_pnl_usd": round(sum(float(r.get("would_next_close_net_pnl_usd") or 0.0)
                                                    for r in overnight_rows), 4),
            "official_same_day_metrics_unchanged": True,
        }
        if persist:
            cols = ("generated_at", "strategy_id", "profile_id", "activated_at", "forward_rows",
                    "clean_rows", "dirty_rows", "clean_closed", "net_pnl_usd", "net_r", "fees_usd",
                    "slippage_usd", "funding_usd", "profit_factor", "winrate", "max_drawdown_usd",
                    "forward_days", "verdict", "rejection_counts_json", "by_sector_json",
                    "diagnostics_json", "config_json")
            values = (now.isoformat(), cfg["strategy_id"], cfg["profile_id"], activated_at,
                      *(summary[k] for k in ("forward_rows", "clean_rows", "dirty_rows", "clean_closed",
                                             "net_pnl_usd", "net_r", "fees_usd", "slippage_usd",
                                             "funding_usd", "profit_factor", "winrate",
                                             "max_drawdown_usd", "forward_days", "verdict")),
                      json_text(rejection_counts), json_text(by_sector), json_text(diagnostics), json_text(cfg))
            conn.execute("INSERT OR REPLACE INTO stocks_catalyst_rs_shadow_evaluations (" + ",".join(cols)
                         + ") VALUES (" + ",".join("?" for _ in cols) + ")", values)
            conn.commit()
        return {"enabled": True, "generated_at": now.isoformat(), "activated_at": activated_at,
                "strategy_id": cfg["strategy_id"], "profile_id": cfg["profile_id"],
                "shadow_lane": cfg["shadow_lane"], "rows": rows, "summary": summary,
                "rejection_counts": rejection_counts, "by_sector": by_sector,
                "diagnostics": diagnostics, "candidate_funnel": candidate_funnel,
                "strict_summary": strict_summary, "exploratory_summary": exploratory_summary,
                "historical_summary": historical_summary,
                "config": cfg,
                "paired_control_status": "UNAVAILABLE_NO_IDENTICAL_EXISTING_ENTRY"}
    finally:
        conn.close()


def render_markdown(result: dict[str, Any]) -> str:
    if not result.get("enabled"):
        return ("# Stocks Catalyst RS Continuation (Shadow)\n\n"
                f"- strategy: `{result['strategy_id']}`\n- status: **DISABLED** (`feature_flag=false`)\n"
                "- No candidates were evaluated and no trading table was touched.\n")
    s = result["summary"]
    strict = result.get("strict_summary") or {}
    exploratory = result.get("exploratory_summary") or {}
    historical = result.get("historical_summary") or {}
    funnel = result.get("candidate_funnel") or {}
    lines = [
        "# Stocks Catalyst Relative-Strength Continuation (Shadow)", "",
        f"- strategy/profile: `{result['strategy_id']}` / `{result['profile_id']}`",
        f"- lane: `{result['shadow_lane']}`; activated: `{result['activated_at']}`",
        "- Long-only; non-earnings/non-legal catalyst; 15m ORH close; RS vs SPY + sector.",
        "- `strict_v1` preserves the original 5%/1.5x/trusted-source rules. `exploratory_v1` "
        "uses 2%/1.25x and may admit one factual secondary source.",
        "- Only `strict_v1` can determine the review verdict. Exploratory trades increase observation "
        "frequency but cannot promote the strategy.",
        "- Same-day forced exit is authoritative. Next-session close is informational only.",
        "- Latency counts only tradable RTH time; closed-market wait is reported separately as "
        "catalyst age.",
        "- Paired control: unavailable until an identical existing entry exists; no mixed-entry delta is shown.", "",
        "## All simulated forward rows", "",
        "| forward rows | clean closed | dirty | net USD | PF | win% | DD USD | fees | slippage | strict verdict |",
        "|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|",
        f"| {s['forward_rows']} | {s['clean_closed']} | {s['dirty_rows']} | {s['net_pnl_usd']:.2f} | "
        f"{s['profit_factor'] if s['profit_factor'] is not None else '-'} | "
        f"{(s['winrate'] * 100) if s['winrate'] is not None else '-'} | {s['max_drawdown_usd']:.2f} | "
        f"{s['fees_usd']:.2f} | {s['slippage_usd']:.2f} | {s['verdict']} |", "",
        "## Evidence cohorts", "",
        "| cohort | forward | clean closed | net USD | PF | win% | verdict |",
        "|---|--:|--:|--:|--:|--:|---|",
        f"| strict_v1 | {strict.get('forward_rows', 0)} | {strict.get('clean_closed', 0)} | "
        f"{float(strict.get('net_pnl_usd', 0.0)):.2f} | "
        f"{strict.get('profit_factor') if strict.get('profit_factor') is not None else '-'} | "
        f"{(float(strict['winrate']) * 100) if strict.get('winrate') is not None else '-'} | "
        f"{strict.get('verdict', 'INSUFFICIENT_CLEAN_SAMPLE')} |",
        f"| exploratory_v1 | {exploratory.get('forward_rows', 0)} | "
        f"{exploratory.get('clean_closed', 0)} | {float(exploratory.get('net_pnl_usd', 0.0)):.2f} | "
        f"{exploratory.get('profit_factor') if exploratory.get('profit_factor') is not None else '-'} | "
        f"{(float(exploratory['winrate']) * 100) if exploratory.get('winrate') is not None else '-'} | "
        "MEASUREMENT_ONLY |", "",
        "## Historical backfill (not promotion evidence)", "",
        "| rows | clean closed | net USD | PF | win% |",
        "|--:|--:|--:|--:|--:|",
        f"| {historical.get('forward_rows', 0)} | {historical.get('clean_closed', 0)} | "
        f"{float(historical.get('net_pnl_usd', 0.0)):.2f} | "
        f"{historical.get('profit_factor') if historical.get('profit_factor') is not None else '-'} | "
        f"{(float(historical['winrate']) * 100) if historical.get('winrate') is not None else '-'} |", "",
        "## Candidate funnel", "",
        f"- canonical rows: `{funnel.get('canonical_rows', 0)}`; point-in-time visible: "
        f"`{funnel.get('point_in_time_visible_rows', 0)}`; with subject: "
        f"`{funnel.get('rows_with_subject_symbol', 0)}`; candidate groups: "
        f"`{funnel.get('candidate_groups', 0)}`; emitted: `{funnel.get('candidates_emitted', 0)}`.",
        "- Upstream exclusions: " + (", ".join(
            f"`{reason}`={count}" for reason, count in sorted((funnel.get("upstream_rejections") or {}).items())
        ) or "_none_"), "",
        "## Rejections", "",
    ]
    for window, counts in result["rejection_counts"].items():
        lines.extend([f"### {window}", ""])
        lines.extend(f"- `{reason}`: {count}" for reason, count in sorted(counts.items()))
        if not counts:
            lines.append("- _none_")
        lines.append("")
    lines.extend([""] + diagnostics_markdown(result["diagnostics"]))
    overnight = result["diagnostics"].get("overnight_counterfactual") or {}
    lines.extend(["", "## Overnight counterfactual", "",
                  f"- eligible: `{overnight.get('eligible', 0)}`; next-open resolved: "
                  f"`{overnight.get('next_open_resolved', 0)}`; next-close resolved: "
                  f"`{overnight.get('next_close_resolved', 0)}`",
                  f"- next-open net USD: `{overnight.get('next_open_net_pnl_usd', 0.0)}`; "
                  f"next-close net USD: `{overnight.get('next_close_net_pnl_usd', 0.0)}`",
                  "- Informational only; official same-day PnL, exits and promotion verdict are unchanged."])
    lines.extend(["", "The strategy is distinct from generic pullback/breakout: point-in-time catalyst "
                  "availability, impulse, RVOL, dual RS, ORH close and same-day exit are mandatory.", "",
                  "No auto-promotion. `REVIEW_ONLY` is operator review, never a routing change."])
    return "\n".join(lines) + "\n"


def write_report(result: dict[str, Any], path: str | None = None) -> str:
    target = Path(path) if path else ROOT / result.get("config", DEFAULTS).get("report_path", DEFAULTS["report_path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_markdown(result), encoding="utf-8")
    return str(target)


__all__ = [
    "OUTCOME_COLUMNS", "REJECTION_REASONS", "ensure_tables", "evaluate_candidate",
    "load_strategy_config", "refresh", "render_markdown", "write_report",
]
