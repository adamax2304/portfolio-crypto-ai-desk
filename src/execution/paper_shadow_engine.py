"""PART 2-5 — Paper-shadow execution engine (PAPER MEASUREMENT ONLY, add-only).

Runs TWO branches over the SAME signals and the SAME real OHLCV, with the SAME partial-exit +
fee + max-5x-sizing model, differing ONLY in the strategy inputs — so the A/B delta is pure
strategy, not accounting:

  A = old_paper        : pullback-zone entry · production direction · mechanical (ATR) TP ·
                         invalidation stop · BE/lock stop moves  (mirrors the production paper branch)
  B = new_logic_shadow : crypto entry per lookahead-safe `signal_entry_mode_preentry` · stock side per `stock_direction_score` ·
                         structural TP per `signal_paper_tp` · structural stop per `signal_stop_plan` ·
                         maker-first where the mode is a limit

Writes `paper_shadow_execution_outcomes` (2 rows/signal) + `paper_shadow_events`. NEVER places an
order, NEVER mutates `signal_outcomes`/`final_r`, NEVER changes scoring/routing/actionability.
Live + auto-live remain locked. This is a measurement lane only.
"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

import pandas as pd

from src.config import load_config
from src.execution.paper_entry_mode_policy import disabled_shadow_reason
from src.storage.file_store import FileStore
from src.execution.fees import fee_rate, slippage_rate
from src.execution.position_sizing import size_position
from src.signals.config import DEFAULT_VALIDITY_HOURS

PARTIALS = {1: 0.33, 2: 0.33, 3: 0.34}
_STRUCT_BASES = {"higher_low", "lower_high", "support", "resistance", "vwap"}
EQUITY = 5000.0
RISK_PCT = 0.005
MAX_LEV = 5
PREENTRY_V2 = "preentry_v2"
# Per-asset PAPER cost model. This selects ONLY the fee/slippage profile — never direction, entry,
# TP/SL, or any A/B strategy input. Stocks/ETFs are NOT crypto perps: commission-free + ~1bp effective
# fee, no perp funding. Using the crypto perp profile on stock shadow rows over-charged them and
# distorted the stock A/B delta — this is the accounting fix.
CRYPTO_FEE_PROFILE = "bybit_non_vip_usdt_perp"
STOCK_FEE_PROFILE = "stock_etf_default"
DEFAULT_FEE_PROFILE = CRYPTO_FEE_PROFILE   # back-compat: default crypto profile


def _asset_is_stock(asset_class) -> bool:
    a = str(asset_class or "").strip().lower()
    return a.startswith("stock") or a.startswith("equit") or a in ("etf", "etfs")


def select_fee_profile(asset_class, crypto_default: str = CRYPTO_FEE_PROFILE) -> str:
    """Return the PAPER fee profile for an asset class — cost model only, never strategy.

    stocks / stock / equities / ETFs -> ``stock_etf_default``; crypto (everything else) ->
    ``crypto_default`` (bybit_non_vip_usdt_perp by default).
    """
    return STOCK_FEE_PROFILE if _asset_is_stock(asset_class) else crypto_default

_DDL_OUTCOMES = """
CREATE TABLE IF NOT EXISTS paper_shadow_execution_outcomes (
  signal_id TEXT, branch TEXT, economic_trade_key TEXT, symbol TEXT, side TEXT, asset_class TEXT,
  playbook TEXT, entry_mode TEXT, direction_model TEXT, direction_changed INTEGER, old_side TEXT,
  entry_price REAL, entry_fill_status TEXT, entry_fill_time TEXT, entry_late_status TEXT,
  missed_entry_reason TEXT, skipped_shadow_reason TEXT,
  structural_tp_set TEXT, tp1 REAL, tp2 REAL, tp3 REAL, tp1_r REAL, tp2_r REAL, tp3_r REAL,
  stop_initial REAL, stop_current REAL, stop_plan TEXT, structural_stop_used INTEGER,
  maker_plan TEXT, entry_order_type TEXT, exit_order_type TEXT,
  qty REAL, notional REAL, leverage INTEGER, risk_usdt REAL,
  fees_usdt REAL, slippage_usdt REAL, net_pnl_usdt REAL, net_r REAL, gross_r REAL,
  mfe_r REAL, mae_r REAL, missed_move_r REAL,
  maker_entry_posted INTEGER, maker_entry_filled INTEGER, maker_entry_missed INTEGER,
  taker_fallback_used INTEGER, maker_tp_fills INTEGER,
  close_reason TEXT, outcome_status TEXT, fee_profile TEXT, mode_source TEXT,
  entry_mode_source TEXT, entry_mode_version TEXT,
  cost_model_asset_class TEXT, fee_profile_selected TEXT, cost_model_status TEXT,
  shadow_lane TEXT,
  window TEXT, created_at TEXT, updated_at TEXT,
  PRIMARY KEY (signal_id, branch, fee_profile)
);
"""
_DDL_META = """
CREATE TABLE IF NOT EXISTS paper_shadow_meta (k TEXT PRIMARY KEY, v TEXT);
"""
_DDL_EVENTS = """
CREATE TABLE IF NOT EXISTS paper_shadow_events (
  signal_id TEXT, branch TEXT, seq INTEGER, event TEXT, timestamp TEXT,
  price REAL, r REAL, qty REAL, remaining REAL, fee_usdt REAL, note TEXT,
  PRIMARY KEY (signal_id, branch, seq)
);
"""


def ensure_tables(conn):
    conn.execute(_DDL_OUTCOMES)
    conn.execute(_DDL_EVENTS)
    conn.execute(_DDL_META)
    # forward-compatible migration: add `window` to a table created before this column existed
    cols = {r[1] for r in conn.execute("PRAGMA table_info(paper_shadow_execution_outcomes)").fetchall()}
    for col, typ in (("window", "TEXT"), ("maker_entry_posted", "INTEGER"),
                     ("maker_entry_filled", "INTEGER"), ("maker_entry_missed", "INTEGER"),
                     ("taker_fallback_used", "INTEGER"), ("maker_tp_fills", "INTEGER"),
                     ("cost_model_asset_class", "TEXT"), ("fee_profile_selected", "TEXT"),
                     ("cost_model_status", "TEXT"),
                     ("shadow_lane", "TEXT"),
                     ("entry_mode_source", "TEXT"), ("entry_mode_version", "TEXT"),
                     # (S2) per-outcome data-coverage fields — populated by the stock coverage gate;
                     # is_clean_for_edge=0 means the trade is a coverage artifact, never counted as edge.
                     ("data_coverage_status", "TEXT"), ("coverage_timeframe", "TEXT"),
                     ("first_bar_after_signal", "TEXT"), ("missing_bars_count", "INTEGER"),
                     ("coverage_gap_minutes", "REAL"), ("is_clean_for_edge", "INTEGER")):
        if col not in cols:
            conn.execute(f"ALTER TABLE paper_shadow_execution_outcomes ADD COLUMN {col} {typ}")
    conn.commit()


def mark_stale_cost_model(conn) -> int:
    """Item 2 — flag stock shadow rows written under a NON-stock (crypto) fee profile as
    ``stale_cost_model`` so readiness/reports exclude them. Never deletes; keeps the row for audit.
    Returns the number of rows marked. Read/repair of accounting only — no strategy change."""
    try:
        cur = conn.execute(
            "UPDATE paper_shadow_execution_outcomes SET cost_model_status='stale_cost_model' "
            "WHERE lower(COALESCE(asset_class,'')) LIKE 'stock%' AND fee_profile != ? "
            "AND COALESCE(cost_model_status,'') != 'stale_cost_model'",
            (STOCK_FEE_PROFILE,))
        return cur.rowcount or 0
    except sqlite3.OperationalError:
        return 0


def _activation_iso(conn, now_iso: str) -> str:
    """The instant the forward lane went live. Signals created at/after it = forward evidence;
    earlier ones = historical_backfill (look-ahead contaminated, NOT proof)."""
    row = conn.execute("SELECT v FROM paper_shadow_meta WHERE k='activated_at'").fetchone()
    if row and row[0]:
        return row[0]
    conn.execute("INSERT OR REPLACE INTO paper_shadow_meta (k, v) VALUES ('activated_at', ?)", (now_iso,))
    conn.commit()
    return now_iso


def _stock_intraday_candidate_cfg() -> dict:
    try:
        from src.execution.entry_mode_calibration import load_calibration_config
        return (load_calibration_config() or {}).get("stocks_intraday_forward_shadow") or {}
    except Exception:
        return {}


def _stock_intraday_activation_iso(conn, now_iso: str) -> str:
    """Activation marker for the fresh, candidate-based stock intraday lane."""
    key = str(_stock_intraday_candidate_cfg().get(
        "activation_meta_key", "stocks_intraday_forward_shadow_activated_at"))
    row = conn.execute("SELECT v FROM paper_shadow_meta WHERE k=?", (key,)).fetchone()
    if row and row[0]:
        return row[0]
    conn.execute("INSERT OR REPLACE INTO paper_shadow_meta (k, v) VALUES (?, ?)", (key, now_iso))
    conn.commit()
    return now_iso


def demote_legacy_stock_candidate_forward_evidence(conn, activation_iso: str) -> int:
    """Quarantine every stock-candidate row that predates the causal v2 lane.

    Changing the activation key alone is insufficient because rows not selected
    by the latest deduplicated refresh retain their old ``window`` value.  The
    timestamp gate makes the reset complete and idempotent without deleting the
    audit history.
    """
    try:
        cur = conn.execute(
            "UPDATE paper_shadow_execution_outcomes SET window='historical_backfill' "
            "WHERE shadow_lane='stocks_intraday_forward' "
            "AND window='forward_since_activation' "
            "AND (created_at IS NULL OR created_at < ?)",
            (activation_iso,),
        )
        return max(0, int(cur.rowcount or 0))
    except sqlite3.OperationalError:
        return 0


def _preentry_v2_activation_iso(conn, now_iso: str) -> str:
    """Start a fresh, fair forward lane for crypto entry-mode testing."""
    key = "preentry_v2_activated_at"
    row = conn.execute("SELECT v FROM paper_shadow_meta WHERE k=?", (key,)).fetchone()
    if row and row[0]:
        return row[0]
    conn.execute("INSERT OR REPLACE INTO paper_shadow_meta (k, v) VALUES (?, ?)", (key, now_iso))
    conn.commit()
    return now_iso


def demote_legacy_crypto_forward_evidence(conn) -> int:
    """Quarantine pre-v2 crypto A/B rows from every forward-facing report.

    The prior B rows used a post-entry mode classifier. Both branches of each
    affected pair are hypothesis-only, not valid A/B evidence. The rows remain
    intact in the same table under ``historical_backfill``.
    """
    cols = {r[1] for r in conn.execute("PRAGMA table_info(paper_shadow_execution_outcomes)")}
    if "entry_mode_version" not in cols:
        return 0
    cur = conn.execute(
        "UPDATE paper_shadow_execution_outcomes SET window='historical_backfill' "
        "WHERE lower(COALESCE(asset_class,''))='crypto' AND window='forward_since_activation' "
        "AND signal_id IN (SELECT signal_id FROM paper_shadow_execution_outcomes "
        "                  WHERE branch='new_logic_shadow' "
        "                  AND COALESCE(entry_mode_version,'') != ?)",
        (PREENTRY_V2,))
    return cur.rowcount or 0


def _f(v):
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


def _r_of(price, entry, risk, long):
    if price is None or entry is None or not risk:
        return None
    return ((price - entry) if long else (entry - price)) / risk


# --------------------------------------------------------------------------- candles
def _load_candles(fs, cfg, symbol, mode, asset_class, exchange_focus, created_at):
    """Real OHLCV (with timestamp) from signal creation forward. None on miss."""
    try:
        if str(asset_class or "").lower().startswith("stock"):
            from src.signals.tracker import _load_stocks_ohlcv_for_signal
            df, _, tf = _load_stocks_ohlcv_for_signal(fs, symbol, mode or "intraday")
        else:
            from src.signals.tracker import _load_ohlcv_for_signal
            df, _, tf = _load_ohlcv_for_signal(fs, cfg, symbol, mode or "intraday", exchange_focus or "")
        if df is None or df.empty or "timestamp" not in df.columns:
            return None, None
        df = df.copy()
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        if created_at:
            cre = pd.to_datetime(created_at, utc=True)
            df = df[df["timestamp"] >= cre]
        return (df.reset_index(drop=True) if not df.empty else None), tf
    except Exception:
        return None, None


# --------------------------------------------------------------------------- walker
@dataclass
class _Walk:
    entered: bool = False
    entry_px: float | None = None
    entry_ts: str | None = None
    entry_order_type: str = "maker"
    realized_r: float = 0.0
    remaining: float = 1.0
    cur_stop: float | None = None
    close_reason: str = "open"
    outcome: str = "open"
    mfe_r: float = 0.0
    mae_r: float = 0.0
    missed_move_r: float = 0.0
    # PART 4 — maker fill realism counters
    maker_entry_posted: int = 0
    maker_entry_filled: int = 0
    maker_entry_missed: int = 0
    taker_fallback_used: int = 0
    maker_tp_fills: int = 0
    blocked_by_expiry: bool = False   # a fill condition existed but past the signal's validity window
    events: list = field(default_factory=list)


_MAKER_TIMEOUT_BARS = 8   # LIMIT_THEN_TAKER_TIMEOUT: take market if the maker limit hasn't filled
# PART 7: a passive maker limit needs the market to trade THROUGH the level by this much to fill —
# a mere touch is a post-only miss. Conservative default (~5 bps); configurable.
_MAKER_TRADE_THROUGH_BPS = 0.0005


def _entry_fill(mode, bar, *, long, entry_low, entry_high, entry_trigger, suggested, is_first):
    """Return (fill_price, order_type, at_open) for this bar, else (None, _, False). `at_open` is
    True only when the fill IS the bar open — the only case where a same-candle TP can be trusted
    to be AFTER entry (intrabar order of a trade-through/trigger fill vs the extreme is unknown)."""
    hi, lo, op, cl = float(bar["high"]), float(bar["low"]), float(bar.get("open", bar["close"])), float(bar["close"])
    m = (mode or "PULLBACK_LIMIT").upper()
    if m == "NO_CHASE_SKIP":
        return None, "none", False
    if m == "MOMENTUM_TAKER_NOW":
        return (op if is_first else cl), "taker", bool(is_first)   # first bar fills at open
    if m == "BREAKOUT_CONTINUATION":
        trig = entry_trigger if entry_trigger is not None else (entry_high if long else entry_low)
        if trig is None:
            return None, "none", False
        if (long and hi >= trig) or (not long and lo <= trig):
            return float(trig), "taker", False             # intrabar trigger cross, NOT at open
        return None, "none", False
    # limit modes: PULLBACK_LIMIT / STRUCTURAL_RETEST / LIMIT_THEN_TAKER_TIMEOUT
    if m == "STRUCTURAL_RETEST" and suggested is not None:
        z_lo = z_hi = float(suggested)
    else:
        if entry_low is None or entry_high is None:
            return None, "none", False
        z_lo, z_hi = min(entry_low, entry_high), max(entry_low, entry_high)
    # PART 7: a resting maker limit fills only on a genuine TRADE-THROUGH of the level (configurable
    # bps), NOT a mere touch — a bar that just kisses the zone edge would not reliably fill a passive
    # order. The near edge (top for a buy, bottom for a sell) is the limit price.
    bps = _MAKER_TRADE_THROUGH_BPS
    if z_lo <= op <= z_hi:
        return op, "maker", True                           # opened inside the zone → fills at open
    if long and lo <= z_hi * (1.0 - bps):                  # traded through the buy limit
        return z_hi, "maker", False                        # intrabar trade-through, NOT at open
    if (not long) and hi >= z_lo * (1.0 + bps):            # traded through the sell limit
        return z_lo, "maker", False
    return None, "none", False                             # only touched the edge → post-only miss


def _walk(*, direction, entry_mode, entry_low, entry_high, entry_trigger, suggested,
          tp1, tp2, tp3, stop0, stop_after_tp1, stop_after_tp2, candles, entry_deadline=None) -> _Walk:
    w = _Walk(cur_stop=stop0)
    long = str(direction).lower() != "short"
    if candles is None or candles.empty or stop0 is None:
        w.outcome, w.close_reason = "no_data", "no_data"
        return w
    risk = abs((entry_high if long else entry_low) or 0) - 0  # placeholder; set after entry
    tps = [(1, tp1), (2, tp2), (3, tp3)]
    filled = {1: False, 2: False, 3: False}
    seq = 0
    n = len(candles)
    _m = (entry_mode or "PULLBACK_LIMIT").upper()
    is_limit_mode = _m in ("PULLBACK_LIMIT", "STRUCTURAL_RETEST", "LIMIT_THEN_TAKER_TIMEOUT")
    if is_limit_mode:
        w.maker_entry_posted = 1                    # a resting maker limit is posted
    entry_bar_idx = None                            # bar the fill happened on
    entry_at_open = False                           # whether the fill was at the bar open
    for idx in range(n):
        bar = candles.iloc[idx]
        ts = str(bar["timestamp"])
        hi, lo = float(bar["high"]), float(bar["low"])
        if not w.entered:
            fill, otype, at_open = _entry_fill(entry_mode, bar, long=long, entry_low=entry_low,
                                               entry_high=entry_high, entry_trigger=entry_trigger,
                                               suggested=suggested, is_first=(idx == 0))
            # LIMIT_THEN_TAKER_TIMEOUT: maker limit not filled within the timeout → take market
            if fill is None and _m == "LIMIT_THEN_TAKER_TIMEOUT" and idx >= _MAKER_TIMEOUT_BARS:
                fill, otype, at_open = float(bar.get("open", bar["close"])), "taker", True
                w.taker_fallback_used = 1
            # Entry validity window: a signal that never filled by its expiry is expired, not filled.
            # If a fill condition genuinely exists on a bar past the deadline, distinguish that
            # (blocked_by_expiry -> entry_late_status="after_expiry_blocked") from a bar that simply
            # never would have filled at all (ordinary expired_no_fill/"missed").
            if entry_deadline is not None and bar["timestamp"] > entry_deadline:
                if fill is not None:
                    w.blocked_by_expiry = True
                    w.taker_fallback_used = 0   # the fallback tentatively flagged above never executes
                    w.outcome, w.close_reason = "no_entry", "expired_no_fill"
                    return w
                continue
            if fill is None:
                # pre-entry invalidation: price hit the initial stop before we got filled
                if (long and lo <= stop0) or (not long and hi >= stop0):
                    if w.maker_entry_posted:
                        w.maker_entry_missed = 1     # maker never filled — opportunity lost
                    w.outcome, w.close_reason = "no_entry", "invalidated_before_entry"
                    return w
                continue
            if otype == "maker":
                w.maker_entry_filled = 1
            w.entered, w.entry_px, w.entry_ts, w.entry_order_type = True, fill, ts, otype
            entry_bar_idx, entry_at_open = idx, bool(at_open)
            seq += 1
            w.events.append({"seq": seq, "event": "shadow_entry_filled", "timestamp": ts,
                             "price": round(fill, 10), "r": 0.0, "qty": 1.0, "remaining": 1.0,
                             "fee_usdt": None, "note": f"{entry_mode} ({otype})"})
            # NO `continue`: evaluate stop/TP on the ENTRY candle too (fast same-bar entry+exit).
        entry = w.entry_px
        rk = abs(entry - stop0) or 1e-9
        # CONSERVATIVE entry candle for a NON-open fill (maker trade-through / breakout trigger):
        # intrabar order of the fill vs the favorable extreme is unknown, so NEVER credit a
        # same-candle TP or its MFE — honor only the adverse side (stop-first). The trade stays open
        # for a later, unambiguous TP.
        if idx == entry_bar_idx and not entry_at_open:
            w.mae_r = min(w.mae_r, ((lo - entry) if long else (entry - hi)) / rk)
            if (long and lo <= w.cur_stop) or (not long and hi >= w.cur_stop):
                r = _r_of(w.cur_stop, entry, rk, long)
                w.realized_r += w.remaining * r
                seq += 1
                w.events.append({"seq": seq, "event": "shadow_stop_filled", "timestamp": ts,
                                 "price": round(w.cur_stop, 10), "r": round(r, 3), "qty": w.remaining,
                                 "remaining": 0.0, "fee_usdt": None, "note": "stop (same-candle entry)"})
                w.remaining = 0.0
                w.close_reason = "stopped_full"
                w.outcome = "closed"
                return w
            continue                                # skip MFE + TP crediting on the ambiguous entry bar
        # MFE/MAE in R
        fav = ((hi - entry) if long else (entry - lo)) / rk
        adv = ((lo - entry) if long else (entry - hi)) / rk
        w.mfe_r = max(w.mfe_r, fav)
        w.mae_r = min(w.mae_r, adv)
        # stop first (conservative)
        if (long and lo <= w.cur_stop) or (not long and hi >= w.cur_stop):
            r = _r_of(w.cur_stop, entry, rk, long)
            w.realized_r += w.remaining * r
            seq += 1
            w.events.append({"seq": seq, "event": "shadow_stop_filled", "timestamp": ts,
                             "price": round(w.cur_stop, 10), "r": round(r, 3), "qty": w.remaining,
                             "remaining": 0.0, "fee_usdt": None, "note": "stop"})
            w.remaining = 0.0
            w.close_reason = "stop" if any(filled.values()) else "stopped_full"
            w.outcome = "closed"
            return w
        # TPs in order
        for i, lvl in tps:
            if lvl is None or filled[i]:
                continue
            if (long and hi >= lvl) or (not long and lo <= lvl):
                filled[i] = True
                r = _r_of(lvl, entry, rk, long)
                w.realized_r += PARTIALS[i] * r
                w.remaining = max(0.0, w.remaining - PARTIALS[i])
                w.maker_tp_fills += 1                # TP exits are maker limits
                seq += 1
                w.events.append({"seq": seq, "event": f"shadow_tp{i}_filled", "timestamp": ts,
                                 "price": round(lvl, 10), "r": round(r, 3), "qty": PARTIALS[i],
                                 "remaining": round(w.remaining, 4), "fee_usdt": None, "note": "maker TP"})
                if i == 1 and stop_after_tp1 is not None:
                    w.cur_stop = stop_after_tp1
                    seq += 1
                    w.events.append({"seq": seq, "event": "shadow_stop_moved_after_tp1", "timestamp": ts,
                                     "price": round(stop_after_tp1, 10), "r": round(_r_of(stop_after_tp1, entry, rk, long), 3),
                                     "qty": None, "remaining": round(w.remaining, 4), "fee_usdt": None, "note": "structural/BE"})
                if i == 2 and stop_after_tp2 is not None:
                    w.cur_stop = stop_after_tp2
                    seq += 1
                    w.events.append({"seq": seq, "event": "shadow_stop_moved_after_tp2", "timestamp": ts,
                                     "price": round(stop_after_tp2, 10), "r": round(_r_of(stop_after_tp2, entry, rk, long), 3),
                                     "qty": None, "remaining": round(w.remaining, 4), "fee_usdt": None, "note": "structural/lock"})
        if w.remaining <= 1e-9:
            w.close_reason, w.outcome = "closed_win", "closed"
            return w
    # data ran out
    if not w.entered:
        w.outcome, w.close_reason = "no_entry", "expired_no_fill"
        # missed move: best favorable excursion the trade would have offered (TP1 R if reached)
        return w
    # expired with remainder → mark to last close
    last = candles.iloc[-1]
    entry = w.entry_px
    rk = abs(entry - stop0) or 1e-9
    long2 = long
    r_last = _r_of(float(last["close"]), entry, rk, long2)
    w.realized_r += w.remaining * r_last
    w.close_reason, w.outcome = "expired_exit", "closed"
    return w


# --------------------------------------------------------------------------- session risk guard
def _session_guard_cfg():
    """Load config/session_risk.yaml once (cached). Safe no-op cfg on failure."""
    from functools import lru_cache
    from pathlib import Path

    @lru_cache(maxsize=1)
    def _load():
        from src.analysis import session_guard as _sg
        return _sg.load_config(Path(__file__).resolve().parents[2])

    try:
        return _load()
    except Exception:
        return None


def _parse_iso_utc(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except Exception:
        return None


def _aware_utc(dt):
    if dt is None:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def entry_deadline_for(sig) -> datetime | None:
    """Latest instant an entry may still fill for this signal (PAPER simulation only — mirrors, but
    never writes, the live validity window). Priority: expires_at, then
    created_at + validity_window_hours, then the SAME mode default live signal tracking uses
    (src.signals.config.DEFAULT_VALIDITY_HOURS) only when both fields are absent/unusable.
    Returns None only when created_at itself can't be parsed (no anchor to compute any window)."""
    exp = _aware_utc(_parse_iso_utc(sig.get("expires_at")))
    is_stock_intraday = (
        _asset_is_stock(sig.get("asset_class"))
        and str(sig.get("mode") or "").lower() == "intraday"
    )
    if is_stock_intraday:
        created_for_session = _aware_utc(_parse_iso_utc(sig.get("created_at")))
        try:
            from src.stocks.market_calendar import stock_intraday_target_session_close
            session_close = (
                stock_intraday_target_session_close(created_for_session)
                if created_for_session else None
            )
        except Exception:
            session_close = None
        if session_close is not None:
            if exp is not None and created_for_session is not None and exp < created_for_session:
                exp = session_close
            else:
                exp = min(exp, session_close) if exp is not None else session_close
    if exp is not None:
        return exp
    created = _aware_utc(_parse_iso_utc(sig.get("created_at")))
    if created is None:
        return None
    vh = _f(sig.get("validity_window_hours"))
    if not vh or vh <= 0:
        vh = DEFAULT_VALIDITY_HOURS.get(str(sig.get("mode") or "").lower(), DEFAULT_VALIDITY_HOURS["intraday"])
    return created + timedelta(hours=float(vh))


def _trim_stock_intraday_to_rth(candles, sig):
    """Keep a stock intraday simulation inside the originating RTH session."""
    if (not _asset_is_stock(sig.get("asset_class"))
            or str(sig.get("mode") or "").lower() != "intraday"
            or candles is None or candles.empty):
        return candles
    deadline = entry_deadline_for(sig)
    if deadline is None:
        return candles.iloc[0:0]
    import pandas as pd
    out = candles.copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True, errors="coerce")
    # Timestamps mark bar opens: the 16:00 bar belongs to the next interval,
    # so the last eligible 15m bar starts at 15:45 ET.
    return out.loc[out["timestamp"] < pd.Timestamp(deadline)].reset_index(drop=True)


def _asia_dead_zone_skip(sig):
    """Skip reason when the Session Risk Guard would demote this trade out of
    actionable — new-logic branch mirrors the production guard. Covers BOTH the
    hard mode kill-switch (e.g. crypto scalp disabled) and the 00–06 UTC Asia
    dead-zone window. Returns the decision kind ('mode_disabled' | 'asia_dead_zone')
    or None. Fail-open → None."""
    try:
        from src.analysis import session_guard as _sg
        cfg = _session_guard_cfg()
        if cfg is None:
            return None
        dec = _sg.guard_decision(
            _parse_iso_utc(sig.get("created_at")),
            sig.get("mode"),
            sig.get("asset_class") or "crypto",
            cfg,
        )
        return (dec.kind or "session_guard") if dec.blocked else None
    except Exception:
        return None


# --------------------------------------------------------------------------- simulate one branch
def _reorient_stock_geometry(sig, mode: str, old_side: str, new_side: str) -> dict | None:
    """Mirror a stock setup when the causal direction overlay changes its side.

    Keeping a long stop below the market after changing the side to short makes
    the simulator count an immediately touched *profitable* stop.  Rebuild the
    complete geometry around the executable anchor instead.
    """
    low, high = _f(sig.get("entry_low")), _f(sig.get("entry_high"))
    trigger, stop = _f(sig.get("entry_trigger")), _f(sig.get("stop0"))
    if low is None or high is None or stop is None:
        return None
    low, high = min(low, high), max(low, high)
    breakout = str(mode or "").upper() == "BREAKOUT_CONTINUATION"
    if breakout:
        source_anchor = trigger if trigger is not None else (high if old_side != "short" else low)
        if trigger is not None:
            target_trigger = (
                low - max(0.0, trigger - high)
                if old_side != "short" and new_side == "short"
                else high + max(0.0, low - trigger)
            )
        else:
            target_trigger = low if new_side == "short" else high
        target_anchor = target_trigger
    else:
        source_anchor = high if old_side != "short" else low
        target_trigger = trigger
        target_anchor = high if new_side != "short" else low
    risk = (source_anchor - stop) if old_side != "short" else (stop - source_anchor)
    if risk <= 0:
        return None

    def mirror_target(value):
        value = _f(value)
        if value is None:
            return None
        distance = (value - source_anchor) if old_side != "short" else (source_anchor - value)
        if distance <= 0:
            return None
        return target_anchor + distance if new_side != "short" else target_anchor - distance

    targets = [mirror_target(sig.get(name)) for name in ("tp1", "tp2", "tp3")]
    if any(value is None for value in targets):
        return None
    target_stop = target_anchor - risk if new_side != "short" else target_anchor + risk
    return {
        "entry_trigger": target_trigger,
        "stop0": target_stop,
        "tp1": targets[0], "tp2": targets[1], "tp3": targets[2],
    }


def _branch_inputs(branch, sig, overlays):
    """Return the strategy inputs (entry_mode/direction/tp/stop) for the given branch."""
    prod_dir = (sig.get("direction") or "long").lower()
    if branch == "old_paper":
        return {
            "entry_mode": "PULLBACK_LIMIT", "direction": prod_dir, "direction_changed": False,
            "old_side": prod_dir, "entry_low": _f(sig.get("entry_low")), "entry_high": _f(sig.get("entry_high")),
            "entry_trigger": _f(sig.get("entry_trigger")), "suggested": None,
            "tp1": _f(sig.get("tp1")), "tp2": _f(sig.get("tp2")), "tp3": _f(sig.get("tp3")),
            "stop0": _f(sig.get("stop0")), "stop_after_tp1": None, "stop_after_tp2": None,
            "structural_tp_set": "ATR_LADDER", "structural_stop_used": 0, "skip_reason": None,
            "entry_mode_source": "legacy_baseline",
        }
    # new_logic_shadow
    asset_is_crypto = not _asset_is_stock(sig.get("asset_class"))
    em = (overlays.get("preentry_mode") or {}) if asset_is_crypto else (overlays.get("entry_mode") or {})
    tp = overlays.get("paper_tp") or {}
    sp = overlays.get("stop_plan") or {}
    sd = overlays.get("stock_dir") or {}
    direction = prod_dir
    changed = False
    skip = None
    stock_signal = str(sig.get("asset_class") or "").lower().startswith("stock")
    if stock_signal:
        if not sd.get("direction"):
            skip = "stock_direction_missing"
        elif not bool(sd.get("is_point_in_time")):
            skip = "stock_direction_not_point_in_time"
        else:
            nd = sd["direction"]
            if nd == "neutral":
                skip = "stock_direction_neutral"
            elif nd != prod_dir:
                direction, changed = nd, True
    mode = em.get("entry_mode")
    if not mode and _asset_is_stock(sig.get("asset_class")):
        hint = str(sig.get("entry_mode_hint") or sig.get("playbook") or "").upper()
        mode = ("BREAKOUT_CONTINUATION" if "BREAKOUT" in hint or "OPENING_DRIVE" in hint
                else "PULLBACK_LIMIT")
    mode = mode or "PULLBACK_LIMIT"
    if asset_is_crypto and str(em.get("data_quality") or "") != "ok":
        skip = "preentry_mode_unavailable"
    if mode == "NO_CHASE_SKIP":
        skip = skip or "no_chase_skip"
    policy_skip = disabled_shadow_reason(
        asset_class=sig.get("asset_class") or "crypto",
        trade_mode=sig.get("mode") or "",
        entry_mode=mode,
    )
    if policy_skip:
        skip = skip or policy_skip
    # Session Risk Guard — new-logic branch mirrors the production actionability guard:
    # scalp/intraday in the 00–06 UTC Asia dead-zone are demoted out of actionable in
    # prod, so the new-logic shadow skips them too (old_paper baseline is left alone,
    # so the A/B delta measures the guard). Uses sig["mode"] (trade mode), NOT the
    # entry-mode `mode` above. Fail-open.
    if skip is None:
        skip = _asia_dead_zone_skip(sig)
    use_struct_tp = tp.get("tp_set_type") in ("STRUCTURAL", "HYBRID")
    tp1 = _f(tp.get("active_paper_tp1")) if use_struct_tp else _f(sig.get("tp1"))
    tp2 = _f(tp.get("active_paper_tp2")) if use_struct_tp else _f(sig.get("tp2"))
    tp3 = _f(tp.get("active_paper_tp3")) if use_struct_tp else _f(sig.get("tp3"))
    entry_trigger = _f(sig.get("entry_trigger"))
    stop0 = _f(sig.get("stop0"))
    if stock_signal and changed:
        rebuilt = _reorient_stock_geometry(sig, mode, prod_dir, direction)
        if rebuilt is None:
            skip = skip or "stock_direction_flip_geometry_unavailable"
        else:
            entry_trigger = rebuilt["entry_trigger"]
            stop0 = rebuilt["stop0"]
            tp1, tp2, tp3 = rebuilt["tp1"], rebuilt["tp2"], rebuilt["tp3"]
    return {
        "entry_mode": mode, "direction": direction, "direction_changed": changed, "old_side": prod_dir,
        "entry_low": _f(sig.get("entry_low")), "entry_high": _f(sig.get("entry_high")),
        "entry_trigger": entry_trigger, "suggested": _f(em.get("suggested_entry")),
        "tp1": tp1, "tp2": tp2, "tp3": tp3, "stop0": stop0,
        "stop_after_tp1": _f(sp.get("stop_after_tp1")), "stop_after_tp2": _f(sp.get("stop_after_tp2")),
        "structural_tp_set": tp.get("tp_set_type") or "ATR_LADDER",
        "structural_stop_used": 1 if (sp.get("prefers_structure")) else 0, "skip_reason": skip,
        "entry_mode_source": (str(em.get("source") or "preentry") if asset_is_crypto
                               else ("candidate_setup_hint" if sig.get("candidate_lane")
                                     else "post_entry_diagnostic")),
    }


def simulate_branch(branch, sig, overlays, candles, fee_profile):
    candles = _trim_stock_intraday_to_rth(candles, sig)
    inp = _branch_inputs(branch, sig, overlays)
    long = inp["direction"] != "short"
    stop0 = inp["stop0"]
    entry_anchor = inp["entry_trigger"] or (inp["entry_low"] if long else inp["entry_high"]) \
        or inp["entry_high"] or inp["entry_low"]
    now = datetime.now(timezone.utc).isoformat()
    base = {
        "signal_id": sig["signal_id"], "branch": branch, "economic_trade_key": sig.get("economic_trade_key"),
        "symbol": sig["symbol"], "side": inp["direction"], "asset_class": sig.get("asset_class"),
        "playbook": sig.get("playbook"), "entry_mode": inp["entry_mode"], "direction_model": branch,
        "direction_changed": 1 if inp["direction_changed"] else 0, "old_side": inp["old_side"],
        "structural_tp_set": inp["structural_tp_set"], "tp1": inp["tp1"], "tp2": inp["tp2"], "tp3": inp["tp3"],
        "stop_initial": stop0, "stop_plan": json.dumps({"after_tp1": inp["stop_after_tp1"], "after_tp2": inp["stop_after_tp2"]}),
        "structural_stop_used": inp["structural_stop_used"], "fee_profile": fee_profile,
        # explicit cost-model provenance (item 1): which asset class drove the fee profile and which
        # profile was actually applied to THIS row. cost_model_status='current' = written under the
        # correct per-asset profile (stale rows are marked by mark_stale_cost_model()).
        "cost_model_asset_class": "stocks" if _asset_is_stock(sig.get("asset_class")) else "crypto",
        "fee_profile_selected": fee_profile, "cost_model_status": "current",
        "shadow_lane": ("stocks_intraday_forward" if sig.get("candidate_lane") else "ab_main"),
        "mode_source": "shadow_engine", "entry_mode_source": inp.get("entry_mode_source"),
        "entry_mode_version": (PREENTRY_V2 if branch == "new_logic_shadow" and not _asset_is_stock(sig.get("asset_class"))
                                else "legacy_shadow_v1"),
        "created_at": now, "updated_at": now,
        "tp1_r": None, "tp2_r": None, "tp3_r": None, "stop_current": stop0,
        "maker_plan": "maker_first" if branch == "new_logic_shadow" else "as_production",
        "missed_move_r": None,
        "maker_entry_posted": 0, "maker_entry_filled": 0, "maker_entry_missed": 0,
        "taker_fallback_used": 0, "maker_tp_fills": 0,
    }
    # skip (B no-chase / neutral) → record without execution
    if inp["skip_reason"]:
        base.update({"entry_fill_status": "skipped", "skipped_shadow_reason": inp["skip_reason"],
                     "outcome_status": "skipped", "close_reason": "skipped", "net_r": 0.0, "gross_r": 0.0,
                     "net_pnl_usdt": 0.0, "fees_usdt": 0.0, "slippage_usdt": 0.0, "qty": 0.0,
                     "notional": 0.0, "leverage": 0, "risk_usdt": 0.0, "entry_price": None,
                     "entry_fill_time": None, "entry_order_type": "none", "exit_order_type": "none",
                     "entry_late_status": "n/a", "missed_entry_reason": None})
        return base, []
    if stop0 is None or entry_anchor is None or abs(entry_anchor - stop0) <= 0:
        base.update({"entry_fill_status": "invalid", "outcome_status": "invalid", "close_reason": "invalid_geometry",
                     "net_r": None, "gross_r": None, "net_pnl_usdt": None, "fees_usdt": None,
                     "slippage_usdt": None, "qty": None, "notional": None, "leverage": None,
                     "risk_usdt": None, "entry_price": None, "entry_fill_time": None,
                     "entry_order_type": "none", "exit_order_type": "none", "entry_late_status": "n/a",
                     "skipped_shadow_reason": None, "missed_entry_reason": "invalid geometry"})
        return base, []

    entry_deadline = entry_deadline_for(sig)
    w = _walk(direction=inp["direction"], entry_mode=inp["entry_mode"], entry_low=inp["entry_low"],
              entry_high=inp["entry_high"], entry_trigger=inp["entry_trigger"], suggested=inp["suggested"],
              tp1=inp["tp1"], tp2=inp["tp2"], tp3=inp["tp3"], stop0=stop0,
              stop_after_tp1=inp["stop_after_tp1"], stop_after_tp2=inp["stop_after_tp2"], candles=candles,
              entry_deadline=entry_deadline)

    risk_px = abs(entry_anchor - stop0)
    sz = size_position(equity_usdt=EQUITY, entry_price=(w.entry_px or entry_anchor), stop_price=stop0,
                       direction=inp["direction"], risk_pct=RISK_PCT, max_leverage=MAX_LEV,
                       max_margin_pct=0.25, max_notional_pct=1.50, liquidation_buffer_to_stop=3.0)
    risk_usdt = EQUITY * RISK_PCT
    qty, notional, lev = sz.qty, sz.notional_usdt, sz.leverage_used
    tp_r = {1: _r_of(inp["tp1"], (w.entry_px or entry_anchor), risk_px, long),
            2: _r_of(inp["tp2"], (w.entry_px or entry_anchor), risk_px, long),
            3: _r_of(inp["tp3"], (w.entry_px or entry_anchor), risk_px, long)}

    if not w.entered:
        # missed move = TP1 R if price reached TP1 after creation (opportunity B/A lost)
        base.update({"entry_fill_status": "missed", "outcome_status": w.outcome, "close_reason": w.close_reason,
                     "net_r": 0.0, "gross_r": 0.0, "net_pnl_usdt": 0.0, "fees_usdt": 0.0,
                     "slippage_usdt": 0.0, "qty": 0.0, "notional": 0.0, "leverage": 0, "risk_usdt": 0.0,
                     "entry_price": None, "entry_fill_time": None, "entry_order_type": "none",
                     "exit_order_type": "none",
                     "entry_late_status": "after_expiry_blocked" if w.blocked_by_expiry else "missed",
                     "missed_entry_reason": w.close_reason, "skipped_shadow_reason": None,
                     "tp1_r": tp_r[1], "tp2_r": tp_r[2], "tp3_r": tp_r[3], "mfe_r": w.mfe_r, "mae_r": w.mae_r,
                     "missed_move_r": round(max(0.0, w.mfe_r), 3),
                     "maker_entry_posted": w.maker_entry_posted, "maker_entry_filled": 0,
                     "maker_entry_missed": w.maker_entry_missed or w.maker_entry_posted,
                     "taker_fallback_used": w.taker_fallback_used, "maker_tp_fills": 0})
        return base, w.events

    # fees: entry slice + each exit slice, maker/taker per side
    entry_rate = fee_rate(fee_profile, w.entry_order_type)
    exit_taker = fee_rate(fee_profile, "taker")
    exit_maker = fee_rate(fee_profile, "maker")
    slip_rate, _ = slippage_rate(sig["symbol"])
    fees = qty * (w.entry_px or entry_anchor) * entry_rate
    slip = qty * (w.entry_px or entry_anchor) * slip_rate
    # exit slices: TP fills = maker; stop/expired remainder = taker
    for ev in w.events:
        if ev["event"].startswith("shadow_tp") and ev["event"].endswith("_filled"):
            f = ev["qty"] * qty * float(ev["price"]) * exit_maker
            ev["fee_usdt"] = round(f, 4)
            fees += f
        elif ev["event"] in ("shadow_stop_filled",):
            f = ev["qty"] * qty * float(ev["price"]) * exit_taker
            ev["fee_usdt"] = round(f, 4)
            fees += f
            slip += ev["qty"] * qty * float(ev["price"]) * slip_rate
    gross_r = round(w.realized_r, 4)
    net_pnl = gross_r * risk_usdt - fees - slip
    net_r = net_pnl / risk_usdt if risk_usdt else None
    base.update({
        "entry_price": round(w.entry_px, 10), "entry_fill_status": "filled", "entry_fill_time": w.entry_ts,
        "entry_late_status": "ok", "missed_entry_reason": None, "skipped_shadow_reason": None,
        "tp1_r": tp_r[1], "tp2_r": tp_r[2], "tp3_r": tp_r[3], "stop_current": w.cur_stop,
        "entry_order_type": w.entry_order_type, "exit_order_type": "maker/taker",
        "qty": round(qty, 8), "notional": round(notional, 2), "leverage": lev, "risk_usdt": round(risk_usdt, 2),
        "fees_usdt": round(fees, 4), "slippage_usdt": round(slip, 4), "net_pnl_usdt": round(net_pnl, 4),
        "net_r": round(net_r, 4) if net_r is not None else None, "gross_r": gross_r,
        "mfe_r": round(w.mfe_r, 3), "mae_r": round(w.mae_r, 3), "missed_move_r": 0.0,
        "close_reason": w.close_reason, "outcome_status": w.outcome,
        "maker_entry_posted": w.maker_entry_posted, "maker_entry_filled": w.maker_entry_filled,
        "maker_entry_missed": w.maker_entry_missed, "taker_fallback_used": w.taker_fallback_used,
        "maker_tp_fills": w.maker_tp_fills,
    })
    return base, w.events


# --------------------------------------------------------------------------- persistence + driver
def _upsert_outcome(conn, rec):
    cols = list(rec.keys())
    conn.execute(f"INSERT OR REPLACE INTO paper_shadow_execution_outcomes ({','.join(cols)}) "
                 f"VALUES ({','.join('?' * len(cols))})", [rec[c] for c in cols])


def _write_events(conn, signal_id, branch, events):
    conn.execute("DELETE FROM paper_shadow_events WHERE signal_id=? AND branch=?", (signal_id, branch))
    for ev in events:
        conn.execute("INSERT OR REPLACE INTO paper_shadow_events "
                     "(signal_id,branch,seq,event,timestamp,price,r,qty,remaining,fee_usdt,note) "
                     "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                     (signal_id, branch, ev["seq"], ev["event"], ev["timestamp"], ev.get("price"),
                      ev.get("r"), ev.get("qty"), ev.get("remaining"), ev.get("fee_usdt"), ev.get("note")))


def _load_signals(conn, lookback_hours, signal_id=None, limit=1200,
                  include_stock_intraday_candidates: bool = False,
                  candidate_only: bool = False):
    """limit=1200 preserves the historical default for every existing caller (scheduler refresh,
    CLI, tests). Pass limit=None for full-coverage non-destructive recomputes (e.g.
    rebuild_and_diagnose's expiry-aware fix) -- safe because this path never DELETEs first."""
    where = "AND p.signal_id=?" if signal_id else "AND o.entry_triggered=1"
    params = ([signal_id] if signal_id else [])
    if not signal_id and lookback_hours:
        where += " AND (julianday('now') - julianday(o.entry_triggered_at)) * 24.0 <= ?"
        params.append(lookback_hours)
    ps_cols = {r[1] for r in conn.execute("PRAGMA table_info(proposed_signals)")}
    optional = [c for c in ("exchange_focus", "expires_at", "validity_window_hours", "tier", "status")
                if c in ps_cols]
    extra_sel = ("," + ",".join(f"p.{c}" for c in optional)) if optional else ""
    limit_sql = ""
    if limit is not None:
        limit_sql = " LIMIT ?"
        params.append(limit)
    has_shadow_outcomes = bool(conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' "
        "AND name='paper_shadow_execution_outcomes'"
    ).fetchone())
    refresh_order = (
        "COALESCE((SELECT MIN(pse.updated_at) "
        "FROM paper_shadow_execution_outcomes pse "
        "WHERE pse.signal_id=p.signal_id),''), "
        if has_shadow_outcomes else ""
    )
    base_sql = (
        "SELECT p.signal_id, p.symbol, p.direction, p.mode, p.asset_class, p.setup_type, "
        f"p.market_regime, p.created_at, p.suggested_entry, p.entry_trigger, "
        f"p.entry_low, p.entry_high, p.stop_loss, p.invalidation, p.tp1, p.tp2, p.tp3{extra_sel}, "
        "o.entry_triggered_at AS observed_entry_at, 0 AS candidate_lane "
        "FROM proposed_signals p "
        "JOIN signal_outcomes o ON o.id=("
        "  SELECT so.id FROM signal_outcomes so WHERE so.signal_id=p.signal_id "
        "  ORDER BY so.id DESC LIMIT 1"
        ") "
        f"WHERE 1=1 {where}"
    )
    if candidate_only:
        rows = []
        column_names = []
    else:
        base_cursor = conn.execute(
            base_sql
            + " ORDER BY " + refresh_order + "observed_entry_at DESC"
            + limit_sql,
            params,
        )
        rows = base_cursor.fetchall()
        column_names = [d[0] for d in (base_cursor.description or [])]

    if (include_stock_intraday_candidates and not signal_id
            and "tier" in ps_cols and "status" in ps_cols):
        # Candidate lane is deliberately A/B-only and time-anchored to
        # proposed_signals.created_at.  It does not replay C-tier/stale ideas
        # as if they were actionable and it includes untriggered candidates so
        # misses are counted rather than silently disappearing.
        cand_params = [lookback_hours] if lookback_hours else []
        cand_limit = " LIMIT ?" if limit is not None else ""
        if limit is not None:
            cand_params.append(limit)
        age_clause = ""
        if lookback_hours:
            age_clause = "AND (julianday('now') - julianday(p.created_at)) * 24.0 <= ?"
        candidate_sql = (
            "SELECT p.signal_id, p.symbol, p.direction, p.mode, p.asset_class, p.setup_type, "
            "p.market_regime, p.created_at, p.suggested_entry, p.entry_trigger, p.entry_low, "
            "p.entry_high, p.stop_loss, p.invalidation, p.tp1, p.tp2, p.tp3"
            f"{extra_sel}, o.entry_triggered_at AS observed_entry_at, 1 AS candidate_lane "
            "FROM proposed_signals p LEFT JOIN signal_outcomes o ON o.id=("
            "  SELECT so.id FROM signal_outcomes so WHERE so.signal_id=p.signal_id "
            "  ORDER BY so.id DESC LIMIT 1"
            ") "
            "WHERE lower(COALESCE(p.asset_class,'')) LIKE 'stock%' AND lower(p.mode)='intraday' "
            "AND upper(COALESCE(p.tier,'')) IN ('A','B') " + age_clause +
            " ORDER BY " + refresh_order + "p.created_at DESC" + cand_limit
        )
        candidate_cursor = conn.execute(candidate_sql, cand_params)
        candidate_rows = candidate_cursor.fetchall()
        if not column_names:
            column_names = [d[0] for d in (candidate_cursor.description or [])]
        candidate_ids = {str(r[0]) for r in candidate_rows}
        # Candidate lane owns the current stock-intraday row even when the
        # tracker has already recorded an entry; otherwise the earlier
        # entry-triggered query would silently keep it in the excluded lane.
        rows = [r for r in rows if str(r[0]) not in candidate_ids]
        rows.extend(candidate_rows)
    out = []
    for r in rows:
        d = dict(r) if isinstance(r, sqlite3.Row) else dict(zip(column_names, r))
        entry = _f(d.get("entry_trigger")) or _f(d.get("suggested_entry")) or _f(d.get("entry_low"))
        stop = _f(d.get("invalidation")) or _f(d.get("stop_loss"))
        out.append({
            "signal_id": d["signal_id"], "symbol": d["symbol"], "direction": (d.get("direction") or "long").lower(),
            "mode": d.get("mode"), "asset_class": d.get("asset_class"), "playbook": d.get("setup_type") or "",
            "entry_mode_hint": d.get("setup_type") or "",
            "regime": d.get("market_regime") or "", "exchange_focus": d.get("exchange_focus") or "",
            "created_at": d.get("created_at"), "entry_low": _f(d.get("entry_low")), "entry_high": _f(d.get("entry_high")),
            "entry_trigger": _f(d.get("entry_trigger")), "suggested_entry": _f(d.get("suggested_entry")),
            "tp1": _f(d.get("tp1")), "tp2": _f(d.get("tp2")), "tp3": _f(d.get("tp3")),
            "stop0": stop, "expires_at": d.get("expires_at"),
            "validity_window_hours": _f(d.get("validity_window_hours")),
            "tier": d.get("tier"), "status": d.get("status"),
            "candidate_lane": bool(d.get("candidate_lane")),
            "economic_trade_key": "|".join(str(x) for x in
                (d["symbol"], (d.get("direction") or "").lower(), (d.get("mode") or "").lower(),
                 round(entry or 0, 8), str(d.get("created_at"))[:10])),
        })
    # The stock scanner may emit the same immutable setup more than once in a
    # session. Production keeps the first candidate; mirror that contract in
    # the forward lane so repeated scans cannot manufacture extra evidence.
    ordinary = [item for item in out if not item.get("candidate_lane")]
    candidate_by_key: dict[str, dict] = {}
    for item in sorted(
        (item for item in out if item.get("candidate_lane")),
        key=lambda value: (str(value.get("created_at") or ""), str(value.get("signal_id") or "")),
    ):
        candidate_by_key.setdefault(str(item["economic_trade_key"]), item)
    candidates = sorted(
        candidate_by_key.values(),
        key=lambda value: str(value.get("created_at") or ""),
        reverse=True,
    )
    return ordinary + candidates


def _overlays(conn, signal_id):
    def one(sql):
        try:
            row = conn.execute(sql, (signal_id,)).fetchone()
            return dict(row) if row else {}
        except Exception:
            return {}
    return {
        "entry_mode": one("SELECT entry_mode, entry_style, suggested_entry FROM signal_entry_mode WHERE signal_id=?"),
        "preentry_mode": one("SELECT entry_mode, suggested_entry, data_quality, source "
                             "FROM signal_entry_mode_preentry WHERE signal_id=?"),
        "paper_tp": one("SELECT tp_set_type, active_paper_tp1, active_paper_tp2, active_paper_tp3 FROM signal_paper_tp WHERE signal_id=?"),
        "stop_plan": one("SELECT stop_after_tp1, stop_after_tp2, prefers_structure FROM signal_stop_plan WHERE signal_id=?"),
        "stock_dir": one("SELECT direction, dir_label, is_point_in_time, as_of_at, "
                         "data_cutoff_at, version FROM stock_direction_score WHERE signal_id=?"),
    }


def _load_shadow_scope() -> tuple[set, set]:
    """(excluded, new_logic_only) sets of (asset_class, mode) from config `shadow_scope`. PAPER/SHADOW
    read-model only — controls which combos the A/B engine simulates and which branches. Reversible;
    never touches live / final_r / proposed_signals / routing / actionability."""
    try:
        from src.execution.entry_mode_calibration import load_calibration_config
        sc = (load_calibration_config() or {}).get("shadow_scope") or {}
    except Exception:
        sc = {}

    def _pairs(key):
        return {(str(x.get("asset_class", "")).lower(), str(x.get("mode", "")).lower())
                for x in (sc.get(key) or []) if isinstance(x, dict)}
    return _pairs("exclude"), _pairs("new_logic_only")


def _branches_for(asset_class, mode, new_logic_only: set) -> tuple:
    """Branches to simulate for this signal. new_logic_only combos skip the deprecated old_paper (A)."""
    if (str(asset_class or "").lower(), str(mode or "").lower()) in new_logic_only:
        return ("new_logic_shadow",)
    return ("old_paper", "new_logic_shadow")


def _branches_for_candidate(sig, candidate_cfg: dict) -> tuple:
    configured = tuple(str(x) for x in (candidate_cfg.get("branches") or ("new_logic_shadow",)))
    return configured or ("new_logic_shadow",)


def _candidate_entry_mode(sig: dict, overlays: dict) -> str:
    em = (overlays.get("entry_mode") or {}).get("entry_mode")
    if em:
        return str(em).upper()
    hint = str(sig.get("entry_mode_hint") or sig.get("playbook") or "").upper()
    return ("BREAKOUT_CONTINUATION" if "BREAKOUT" in hint or "OPENING_DRIVE" in hint
            else "PULLBACK_LIMIT")


def prune_shadow_scope(conn) -> dict:
    """Delete now-out-of-scope rows so the shadow tables match config (self-heals every refresh).
    PAPER read-model only: excluded combos → all branches removed; new_logic_only combos → old_paper
    rows removed. Never touches proposed_signals / signal_outcomes / final_r / live."""
    excl, nlo = _load_shadow_scope()
    removed = {"excluded_rows": 0, "old_paper_rows": 0, "candidate_mode_rows": 0,
               "orphan_events": 0}
    outcome_cols = {r[1] for r in conn.execute(
        "PRAGMA table_info(paper_shadow_execution_outcomes)").fetchall()}
    lane_guard = " AND COALESCE(shadow_lane,'') != 'stocks_intraday_forward'" \
        if "shadow_lane" in outcome_cols else ""
    for ac, mode in excl:
        cur = conn.execute(
            "DELETE FROM paper_shadow_execution_outcomes WHERE signal_id IN "
            "(SELECT signal_id FROM proposed_signals WHERE lower(asset_class)=? AND lower(mode)=?) "
            + lane_guard,
            (ac, mode))
        removed["excluded_rows"] += cur.rowcount or 0
    for ac, mode in nlo:
        cur = conn.execute(
            "DELETE FROM paper_shadow_execution_outcomes WHERE branch='old_paper' AND signal_id IN "
            "(SELECT signal_id FROM proposed_signals WHERE lower(asset_class)=? AND lower(mode)=?)",
            (ac, mode))
        removed["old_paper_rows"] += cur.rowcount or 0
    allowed = {str(x).upper() for x in (_stock_intraday_candidate_cfg().get("entry_modes") or [])}
    if allowed and {"shadow_lane", "entry_mode"}.issubset(outcome_cols):
        marks = ",".join("?" for _ in allowed)
        cur = conn.execute(
            "DELETE FROM paper_shadow_execution_outcomes WHERE shadow_lane='stocks_intraday_forward' "
            f"AND upper(COALESCE(entry_mode,'')) NOT IN ({marks})", tuple(sorted(allowed)))
        removed["candidate_mode_rows"] = cur.rowcount or 0
    # Pruning outcomes without pruning their event streams leaves stale rows that can
    # be misread as active execution evidence. Events are subordinate to outcomes.
    events_exists = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='paper_shadow_events'"
    ).fetchone()
    if events_exists:
        cur = conn.execute(
            "DELETE FROM paper_shadow_events WHERE NOT EXISTS ("
            "SELECT 1 FROM paper_shadow_execution_outcomes e "
            "WHERE e.signal_id=paper_shadow_events.signal_id AND e.branch=paper_shadow_events.branch)"
        )
        removed["orphan_events"] = cur.rowcount or 0
    conn.commit()
    return removed


def refresh(*, lookback_hours: float | None = 168.0, fee_profile: str = DEFAULT_FEE_PROFILE,
            signal_id: str | None = None, dry_run: bool = False, rebuild: bool = False,
            db: str | None = None, max_signals: int | None = 1200,
            candidate_only: bool = False) -> dict:
    cfg = load_config()
    fs = FileStore(cfg)
    conn = sqlite3.connect(db or cfg.db_path)
    conn.row_factory = sqlite3.Row
    ensure_tables(conn)
    conn.commit()
    if rebuild and not signal_id:
        # clear BOTH per-asset profiles (crypto default + stock) so a rebuild is complete
        conn.execute("DELETE FROM paper_shadow_execution_outcomes WHERE fee_profile IN (?, ?)",
                     (fee_profile, STOCK_FEE_PROFILE))
        conn.execute("DELETE FROM paper_shadow_events")
    excl_scope, new_logic_only = _load_shadow_scope()      # shadow-testing scope (paper read-model)
    if not dry_run:
        prune_shadow_scope(conn)                           # self-heal: drop out-of-scope rows
    now = datetime.now(timezone.utc).isoformat()
    activation = _activation_iso(conn, now)
    preentry_v2_activation = _preentry_v2_activation_iso(conn, now)
    candidate_cfg = _stock_intraday_candidate_cfg()
    candidate_enabled = bool(candidate_cfg.get("enabled", False)) and not signal_id
    candidate_activation = (_stock_intraday_activation_iso(conn, now)
                            if candidate_enabled else now)
    legacy_forward_demoted = 0
    stock_candidate_legacy_demoted = 0
    if not dry_run:
        legacy_forward_demoted = demote_legacy_crypto_forward_evidence(conn)
        if candidate_enabled:
            stock_candidate_legacy_demoted = demote_legacy_stock_candidate_forward_evidence(
                conn, candidate_activation)
        # Scope repair is idempotent. Release the writer slot before loading
        # candles and simulating up to 1200 signals.
        conn.commit()
    sigs = _load_signals(conn, lookback_hours, signal_id, limit=max_signals,
                          include_stock_intraday_candidates=(candidate_enabled or candidate_only),
                          candidate_only=candidate_only)
    def _blank():
        return {"A_net_r": 0.0, "B_net_r": 0.0, "A_net_usd": 0.0, "B_net_usd": 0.0,
                "A_filled": 0, "B_filled": 0}
    stats = {"processed": 0, "A_net_r": 0.0, "B_net_r": 0.0, "A_net_usd": 0.0, "B_net_usd": 0.0,
             "B_filled": 0, "B_missed": 0, "B_skipped": 0, "B_dir_flips": 0, "B_structural_tp": 0,
             "A_filled": 0, "candidate_processed": 0, "candidate_filled": 0,
             "candidate_missed": 0, "candidate_skipped": 0,
             "candidate_excluded_mode": 0,
             "candidate_outside_rth": 0,
             "candidate_net_r": 0.0, "candidate_net_usd": 0.0,
             "candidate_by_mode": {},
             "fee_profile": fee_profile, "activated_at": activation,
             "stocks_intraday_candidate_activated_at": candidate_activation,
             "stocks_intraday_candidate_legacy_forward_demoted": stock_candidate_legacy_demoted,
             "preentry_v2_activated_at": preentry_v2_activation,
             "preentry_v2_legacy_forward_demoted": legacy_forward_demoted,
             "historical_backfill": _blank(), "forward_since_activation": _blank(),
             # per-asset A/B books + which fee profile each asset used (item 2)
             "by_asset": {"crypto": _blank(), "stocks": _blank()},
             "fee_profile_by_asset": {"crypto": fee_profile, "stocks": STOCK_FEE_PROFILE}}
    for sig in sigs:
        # shadow-testing scope: skip excluded combos entirely (e.g. stocks intraday — already live in
        # paper); new_logic_only combos simulate ONLY the new logic (drop deprecated old_paper A).
        is_candidate = bool(sig.get("candidate_lane"))
        if is_candidate and bool(candidate_cfg.get("require_rth_created", True)):
            try:
                from src.stocks.market_calendar import is_us_cash_session_open
                created_dt = _parse_iso_utc(sig.get("created_at"))
                if created_dt is None or not is_us_cash_session_open(created_dt):
                    stats["candidate_outside_rth"] += 1
                    continue
            except Exception:
                # Unparseable timestamps are not eligible for a clean forward lane.
                stats["candidate_outside_rth"] += 1
                continue
        if (not is_candidate and
                (str(sig.get("asset_class") or "").lower(), str(sig.get("mode") or "").lower()) in excl_scope):
            continue
        if is_candidate:
            stats["candidate_processed"] += 1
        ov = _overlays(conn, sig["signal_id"])
        if is_candidate:
            allowed = {str(x).upper() for x in (candidate_cfg.get("entry_modes") or [])}
            if allowed and _candidate_entry_mode(sig, ov) not in allowed:
                stats["candidate_excluded_mode"] += 1
                continue
        candles, _tf = _load_candles(fs, cfg, sig["symbol"], sig["mode"], sig["asset_class"],
                                     sig["exchange_focus"], sig["created_at"])
        activation_for_signal = (candidate_activation if is_candidate else
                                 (preentry_v2_activation if not _asset_is_stock(sig.get("asset_class"))
                                  else activation))
        window = ("forward_since_activation"
                  if str(sig.get("created_at") or "") >= activation_for_signal else "historical_backfill")
        akey = "stocks" if _asset_is_stock(sig.get("asset_class")) else "crypto"
        fp = select_fee_profile(sig.get("asset_class"), fee_profile)   # per-asset cost model
        branches = (_branches_for_candidate(sig, candidate_cfg) if is_candidate else
                    _branches_for(sig.get("asset_class"), sig.get("mode"), new_logic_only))
        for branch in branches:
            rec, events = simulate_branch(branch, sig, ov, candles, fp)
            rec["window"] = window
            if not dry_run:
                _upsert_outcome(conn, rec)
                _write_events(conn, sig["signal_id"], branch, events)
            if rec.get("entry_fill_status") == "filled":
                if is_candidate:
                    # Candidate lane is deliberately B-only. Keep it out of the
                    # paired A/B books; those books require the same signal under
                    # both branches. It gets its own absolute-PnL diagnostics.
                    candidate_mode = str(rec.get("entry_mode") or "UNKNOWN").upper()
                    cb = stats["candidate_by_mode"].setdefault(
                        candidate_mode, {"filled": 0, "net_r": 0.0, "net_usd": 0.0})
                    cb["filled"] += 1
                    cb["net_r"] += rec.get("net_r") or 0.0
                    cb["net_usd"] += rec.get("net_pnl_usdt") or 0.0
                    stats["candidate_net_r"] += rec.get("net_r") or 0.0
                    stats["candidate_net_usd"] += rec.get("net_pnl_usdt") or 0.0
                else:
                    bkey = "A" if branch == "old_paper" else "B"
                    stats[window][f"{bkey}_filled"] += 1
                    stats[window][f"{bkey}_net_r"] += rec.get("net_r") or 0.0
                    stats[window][f"{bkey}_net_usd"] += rec.get("net_pnl_usdt") or 0.0
                    stats["by_asset"][akey][f"{bkey}_filled"] += 1
                    stats["by_asset"][akey][f"{bkey}_net_r"] += rec.get("net_r") or 0.0
                    stats["by_asset"][akey][f"{bkey}_net_usd"] += rec.get("net_pnl_usdt") or 0.0
            if branch == "old_paper" and not is_candidate:
                if rec.get("entry_fill_status") == "filled":
                    stats["A_filled"] += 1
                    stats["A_net_r"] += rec.get("net_r") or 0.0
                    stats["A_net_usd"] += rec.get("net_pnl_usdt") or 0.0
            elif not is_candidate:
                if rec.get("entry_fill_status") == "filled":
                    stats["B_filled"] += 1
                    stats["B_net_r"] += rec.get("net_r") or 0.0
                    stats["B_net_usd"] += rec.get("net_pnl_usdt") or 0.0
                    if rec.get("structural_tp_set") in ("STRUCTURAL", "HYBRID"):
                        stats["B_structural_tp"] += 1
                elif rec.get("entry_fill_status") == "missed":
                    stats["B_missed"] += 1
                elif rec.get("entry_fill_status") == "skipped":
                    stats["B_skipped"] += 1
                if rec.get("direction_changed"):
                    stats["B_dir_flips"] += 1
            if is_candidate and branch == "new_logic_shadow":
                candidate_key = {"filled": "candidate_filled", "missed": "candidate_missed",
                                 "skipped": "candidate_skipped"}.get(rec.get("entry_fill_status"))
                if candidate_key:
                    stats[candidate_key] += 1
        stats["processed"] += 1
        if not dry_run:
            # Persist one complete signal (all branches/events) atomically, then
            # yield SQLite to latency-critical Paper decisions. A crash may
            # leave later signals stale, but the refresh is idempotent and the
            # next run resumes them without holding a multi-minute write lease.
            conn.commit()
    stale_marked = 0
    if not dry_run:
        stale_marked = mark_stale_cost_model(conn)   # item 2: flag any wrong-profile stock rows
        conn.commit()
    conn.close()
    for k in ("A_net_r", "B_net_r", "A_net_usd", "B_net_usd"):
        stats[k] = round(stats[k], 2)
    stats["candidate_net_r"] = round(stats["candidate_net_r"], 2)
    stats["candidate_net_usd"] = round(stats["candidate_net_usd"], 2)
    for book in stats["candidate_by_mode"].values():
        book["net_r"] = round(book["net_r"], 2)
        book["net_usd"] = round(book["net_usd"], 2)
    for akey, book in stats["by_asset"].items():
        for k in ("A_net_r", "B_net_r", "A_net_usd", "B_net_usd"):
            book[k] = round(book[k], 2)
        book["delta_net_r"] = round(book["B_net_r"] - book["A_net_r"], 2)
        book["delta_net_usd"] = round(book["B_net_usd"] - book["A_net_usd"], 2)
    stats["stale_cost_model_marked"] = stale_marked
    stats["delta_net_r"] = round(stats["B_net_r"] - stats["A_net_r"], 2)
    stats["delta_net_usd"] = round(stats["B_net_usd"] - stats["A_net_usd"], 2)
    return stats
