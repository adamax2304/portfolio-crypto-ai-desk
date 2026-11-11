"""Paper execution accounting — authoritative PAPER PnL (Model F).

WHY
---
The legacy `signal_outcomes.final_r` is **touch-based**: it books the R of the
highest TP the price touched, so a trade that pops to TP1 then reverses to the
stop is recorded as a +TP1 WIN. Audits showed this overstates the actionable
book by ~+100..+143R; under realistic single-position exits the book is
−96..−137R. This module computes an honest **paper execution R** for each trade
using an early MFE-armed protective stop ("Model F"), which historical replay
turned net-positive (+74R / PF ~1.43) — pending forward validation.

SCOPE (hard limits)
-------------------
* PAPER / ACCOUNTING ONLY. No live, no auto-live, no exchange orders, no
  force-close.
* NEVER writes `signal_outcomes`; NEVER changes `final_r` / `final_outcome`.
* Writes only to the additive `paper_execution_outcomes` table.
* Pure function `compute_paper_execution(...)` + storage helpers. Fail-open: a
  caller that errors must keep legacy tracking working.

MODEL F — aggregate fallback vs live-parity forward evidence
-----------------------------------------------------------
`early_mfe_protection_v1` is retained only as the legacy/backfill aggregate
fallback reconstructed from TP/stop touches + MFE in R. It cannot prove event
order or reproduce partial exits and therefore is not live-comparable.

New point-in-time entries are evaluated by `live_exit_parity_v3_incremental`:
closed 1m candles are consumed once, state is persisted between tracker ticks,
TP1/TP2/TP3 close 33%/33%/34%, and newly armed protection applies from the next
candle. Missing candle continuity invalidates the row rather than inventing a
path. The protection thresholds remain:
  * initial stop = original invalidation (−1R);
  * once **+0.6R favorable excursion** is reached -> stop to **breakeven (0R)**;
  * once **+1.0R favorable excursion** is reached -> lock **+0.5R**;
  * the remaining runner continues through the three target legs;
  * if the (moved) stop is later hit: close at the moved-stop R (0R after BE,
    +0.5R after lock); if the ORIGINAL stop is hit before +0.6R: −1R;
  * if expired after entry: closed at the protected level (0R, or +0.5R if the
    lock had armed) — never left as "unresolved win".
Same-candle ambiguity: conservative stop-first. A candle high can precede the
limit fill later in that same candle, so its MFE cannot arm Model F protection.
If the original stop is subsequently recorded, it remains a −1R loss; without
a later stop it resolves flat at expiry. This is deliberately stricter than
crediting a TP/lock from an unknowable intrabar order. Absolute R is
relative-leaning at 5m/15m granularity.

FREEZE / VERSIONING (2026-07-09) — read this before touching ARM_BE_AT_R / LOCK_AT_R / LOCK_LEVEL_R
-----------------------------------------------------------------------------------------------------
These thresholds were originally chosen by replaying the SAME historical trades under several
parameter combinations and keeping the one that looked best in that replay (+74R / PF~1.43) — i.e.
in-sample, hindsight-informed tuning, not a forward-validated rule. An audit (2026-07-09) found ~87%
of `paper_execution_outcomes` rows were populated by a same-day backfill re-walk of history under
these CURRENT parameters, so most of the apparent track record is that same replay, not genuinely
accumulated forward experience.

`FROZEN_AT` pins the moment these three constants stop being casually retuned. Model F itself is
UNCHANGED and stays fully ENABLED — it continues to protect every position exactly as before; this
freeze does NOT disable or alter any protective behaviour. All it does is (a) stop silent parameter
retuning and (b) let every row honestly self-report whether it is `forward_postfreeze` evidence (the
underlying trade's real entry happened at/after FROZEN_AT — genuine, sequential, un-gameable) or
`backfill_pretrained` (entry predates the freeze — the in-sample replay, informational only, never
cited as proof of edge). Re-freezing (bumping FROZEN_AT after a deliberate, conscious re-tune) is
allowed — but must never be a reaction to "the forward number looks bad so far," which would just
repeat the original hindsight-fitting mistake one level up.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from src.stocks.entry_provenance import (
    is_accepted_stock_intraday_paper_basis,
    paper_provenance_rank,
)
from src.execution.paper_live_exit_path import VERSION as LIVE_EXIT_PARITY_VERSION

RISK_MODELS = ("legacy_touch", "first_tp_close", "early_mfe_protection_v1")
DEFAULT_RISK_MODEL = "early_mfe_protection_v1"
# Parameter thresholds remain frozen. This suffix records the path-correctness
# fix: ambiguous same-candle highs can no longer arm a protective stop.
MODEL_VERSION = "early_mfe_protection_v1_frozen@2026-07-09_path_safe@2026-07-31"

# Model F thresholds (paper accounting only — NOT production TP/SL). FROZEN as of FROZEN_AT — see the
# module-level "FREEZE / VERSIONING" note above before changing any of the three.
ARM_BE_AT_R = 0.6        # +0.6R favorable -> stop to breakeven
LOCK_AT_R = 1.0          # +1.0R favorable -> lock +0.5R
LOCK_LEVEL_R = 0.5

# Evidence-class cutoff: a trade whose real entry is at/after this instant is genuine forward
# (out-of-sample) evidence for these parameters; before it, the trade predates the freeze and any
# paper_execution_r computed for it is backfill/in-sample only. Keyed off the trade's OWN entry time
# (entry_triggered_at, falling back to created_at) — never off `computed_at`, which is always fresh
# because every refresh cycle recomputes every row regardless of when the trade actually happened.
FROZEN_AT = "2026-07-09T00:00:00+00:00"
EVIDENCE_FORWARD = "forward_postfreeze"
EVIDENCE_BACKFILL = "backfill_pretrained"


def _parse_ts(v: Any) -> datetime | None:
    if not v:
        return None
    s = str(v).strip()
    if not s:
        return None
    try:
        s = s.replace("Z", "+00:00")
        dt = datetime.fromisoformat(s)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None


def evidence_class_for(entry_ts: Any, *, frozen_at: str = FROZEN_AT) -> str:
    """Classify one trade as forward (post-freeze, trustworthy) or backfill (pre-freeze, in-sample
    replay) evidence, keyed off the trade's real entry time. Unparseable/missing timestamps default
    conservatively to backfill — we never credit a trade as forward evidence we can't date."""
    dt = _parse_ts(entry_ts)
    cutoff = _parse_ts(frozen_at)
    if dt is None or cutoff is None:
        return EVIDENCE_BACKFILL
    return EVIDENCE_FORWARD if dt >= cutoff else EVIDENCE_BACKFILL


def _f(v: Any) -> float | None:
    try:
        return None if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return None


def r_multiple(entry: float | None, stop: float | None, level: float | None,
               direction: str) -> float | None:
    """R of `level` relative to entry, risk = |entry - stop|. Sign-flipped for shorts."""
    if entry is None or stop is None or level is None:
        return None
    risk = abs(entry - stop)
    if risk <= 0:
        return None
    return (entry - level) / risk if str(direction).lower() == "short" else (level - entry) / risk


def legacy_touch_r(reached_tp1: bool, reached_tp2: bool, reached_tp3: bool,
                   hit_stop: bool, R1: float, R2: float, R3: float) -> float:
    """The current production accounting: R of the highest TP touched."""
    if reached_tp3:
        return R3
    if reached_tp2:
        return R2
    if reached_tp1:
        return R1
    return -1.0 if hit_stop else 0.0


def compute_paper_execution(
    *,
    direction: str,
    entry: float | None,
    stop: float | None,
    tp1: float | None,
    tp2: float | None,
    tp3: float | None,
    reached_tp1: bool,
    reached_tp2: bool,
    reached_tp3: bool,
    hit_stop: bool,
    expired: bool,
    entered: bool,
    mfe_r: float | None,
    same_candle_ambiguous: bool = False,
    risk_model: str = DEFAULT_RISK_MODEL,
    entry_ts: Any = None,
) -> dict[str, Any]:
    """Compute the paper execution outcome for ONE economic trade.

    Returns a dict with paper_execution_r + all ledger fields. paper_execution_r
    is None for trades that never entered or are still open (not yet resolved).

    ``entry_ts`` (the trade's real entry timestamp, e.g. entry_triggered_at) drives
    ``evidence_class`` — forward_postfreeze vs backfill_pretrained (see FROZEN_AT
    above). Optional/backward-compatible: omitted or unparseable defaults to
    backfill_pretrained, never fabricating forward evidence.
    """
    R1 = r_multiple(entry, stop, tp1, direction) or 0.0
    R2 = r_multiple(entry, stop, tp2, direction) or 0.0
    R3 = r_multiple(entry, stop, tp3, direction) or 0.0
    mfe = mfe_r if mfe_r is not None else 0.0
    m0 = legacy_touch_r(reached_tp1, reached_tp2, reached_tp3, hit_stop, R1, R2, R3)

    highest_tp = 3 if reached_tp3 else 2 if reached_tp2 else 1 if reached_tp1 else 0
    first_event = ("tp" if (reached_tp1 or reached_tp2 or reached_tp3) and not hit_stop
                   else "stop" if hit_stop else "none")
    # TP1/TP2 are milestones for Model F, not terminal exits. The runner remains
    # open until TP3, a stop (original/protected), expiry, or an ambiguous close.
    # Legacy comparison models intentionally retain their historical semantics.
    if risk_model == DEFAULT_RISK_MODEL:
        resolved = entered and (reached_tp3 or hit_stop or expired or same_candle_ambiguous)
    else:
        resolved = entered and (reached_tp1 or reached_tp2 or reached_tp3 or hit_stop or expired)

    rec: dict[str, Any] = {
        "risk_model": risk_model,
        "touch_r": round(m0, 4),
        "paper_execution_r": None,
        "paper_execution_outcome": "open" if entered else "no_entry",
        "close_reason": "open" if entered else "no_entry",
        "stop_initial": stop,
        "stop_current_r": -1.0,
        "protection_armed": False,
        "protection_level_r": None,
        "lock_armed": False,
        "lock_level_r": None,
        "highest_tp_touched": highest_tp,
        "first_event": first_event,
        "close_event": None,
        "giveback": False,
        "same_candle_ambiguous": bool(same_candle_ambiguous),
        "version": MODEL_VERSION,
        "evidence_class": evidence_class_for(entry_ts),
        "frozen_at": FROZEN_AT,
    }
    if risk_model == "legacy_touch":
        if not resolved:
            return rec
        r = m0
        rec.update(paper_execution_r=round(r, 4),
                   paper_execution_outcome=("win" if r > 0 else "loss" if r < 0 else "flat"),
                   close_reason="legacy_touch", close_event="touch")
        return rec
    if risk_model == "first_tp_close":
        if not resolved:
            return rec
        r = R1 if reached_tp1 else (-1.0 if hit_stop else 0.0)
        rec.update(paper_execution_r=round(r, 4),
                   paper_execution_outcome=("win" if r > 0 else "loss" if r < 0 else "flat"),
                   close_reason="first_tp_close", close_event="tp1" if reached_tp1 else first_event)
        return rec

    # A candle whose range contains both a late limit fill and an earlier TP
    # touch has no observable intrabar ordering at this resolution. Its MFE may
    # be entirely pre-entry, so never use it to manufacture BE/profit-lock PnL.
    # A later original-stop touch is still decisive; otherwise expiry is flat.
    if same_candle_ambiguous:
        if hit_stop:
            rec.update(
                paper_execution_r=-1.0,
                paper_execution_outcome="loss",
                close_reason="original_stop",
                close_event="ambiguous_stop_first",
                stop_current_r=-1.0,
            )
        elif expired:
            rec.update(
                paper_execution_r=0.0,
                paper_execution_outcome="expired",
                close_reason="expired_flat",
                close_event="ambiguous_expiry_flat",
                stop_current_r=-1.0,
            )
        return rec

    # ---- early_mfe_protection_v1 (Model F) ----
    armed = mfe >= ARM_BE_AT_R
    locked = mfe >= LOCK_AT_R
    rec["protection_armed"] = bool(armed)
    rec["protection_level_r"] = 0.0 if armed else None
    rec["lock_armed"] = bool(locked)
    rec["lock_level_r"] = LOCK_LEVEL_R if locked else None
    rec["stop_current_r"] = LOCK_LEVEL_R if locked else (0.0 if armed else -1.0)

    if not resolved:
        return rec

    if reached_tp3:
        r, reason, outcome, ce = R3, "tp3_runner", "win", "tp3"
        rec["stop_current_r"] = LOCK_LEVEL_R if locked else (0.0 if armed else -1.0)
    elif locked:
        r, reason, outcome, ce = LOCK_LEVEL_R, "profit_lock_stop", "win", "moved_stop"
        rec["stop_current_r"] = LOCK_LEVEL_R
        rec["giveback"] = True  # reached >=1R favorable, came back to the lock
    elif armed:
        r, reason, outcome, ce = 0.0, "breakeven_stop", "breakeven", "moved_stop"
        rec["stop_current_r"] = 0.0
        rec["giveback"] = True  # reached >=0.6R favorable, scratched at BE
    else:
        # never got +0.6R favorable
        if hit_stop:
            r, reason, outcome, ce = -1.0, "original_stop", "loss", "stop"
        else:  # expired without meaningful excursion
            r, reason, outcome, ce = 0.0, "expired_flat", "expired", "expiry"
        rec["stop_current_r"] = -1.0

    rec.update(paper_execution_r=round(r, 4), paper_execution_outcome=outcome,
               close_reason=reason, close_event=ce)
    return rec


# ----------------------------------------------------------------- storage ----
_TABLE = "paper_execution_outcomes"
_COLS = (
    "signal_id", "economic_trade_key", "risk_model", "touch_r", "paper_execution_r",
    "paper_execution_outcome", "close_reason", "stop_initial", "stop_current_r",
    "protection_armed", "protection_level_r", "lock_armed", "lock_level_r",
    "highest_tp_touched", "first_event", "close_event", "giveback",
    "same_candle_ambiguous", "computed_at", "version", "evidence_class", "frozen_at",
    "lifecycle_state", "entry_at", "entry_price_used", "exit_at", "exit_at_source",
    "decision_at", "first_executable_price", "entry_drift_bps", "signal_snapshot_json",
    "entry_bar_open_at", "entry_time_basis", "current_price_revalidated",
    "effective_expires_at", "execution_validity", "paper_entry_profile",
    "paper_execution_entry_mode",
    "path_realized_r", "path_remaining_fraction", "path_last_candle_at",
    "path_tp1_filled", "path_tp2_filled", "path_tp3_filled",
    "path_max_mfe_r", "path_data_quality", "path_gap_seconds",
)
# additive columns layered on after the original table shipped (2026-07-09 freeze) — idempotent
# ALTER TABLE migration for any DB created before evidence_class/frozen_at existed.
_NEW_COLUMNS = (
    ("evidence_class", "TEXT"), ("frozen_at", "TEXT"),
    ("lifecycle_state", "TEXT"), ("entry_at", "TEXT"),
    ("entry_price_used", "REAL"), ("exit_at", "TEXT"),
    ("exit_at_source", "TEXT"), ("decision_at", "TEXT"),
    ("first_executable_price", "REAL"), ("entry_drift_bps", "REAL"),
    ("signal_snapshot_json", "TEXT"),
    ("entry_bar_open_at", "TEXT"), ("entry_time_basis", "TEXT"),
    ("current_price_revalidated", "INTEGER"),
    ("effective_expires_at", "TEXT"), ("execution_validity", "TEXT"),
    ("paper_entry_profile", "TEXT"), ("paper_execution_entry_mode", "TEXT"),
    ("path_realized_r", "REAL"), ("path_remaining_fraction", "REAL"),
    ("path_last_candle_at", "TEXT"),
    ("path_tp1_filled", "INTEGER"), ("path_tp2_filled", "INTEGER"),
    ("path_tp3_filled", "INTEGER"), ("path_max_mfe_r", "REAL"),
    ("path_data_quality", "TEXT"), ("path_gap_seconds", "REAL"),
)


def ensure_table(conn) -> None:
    """Create the additive paper_execution_outcomes table if missing, and add any
    columns introduced later (idempotent ALTER). Never touches signal_outcomes."""
    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {_TABLE} (
            signal_id TEXT PRIMARY KEY,
            economic_trade_key TEXT,
            risk_model TEXT,
            touch_r REAL,
            paper_execution_r REAL,
            paper_execution_outcome TEXT,
            close_reason TEXT,
            stop_initial REAL,
            stop_current_r REAL,
            protection_armed INTEGER,
            protection_level_r REAL,
            lock_armed INTEGER,
            lock_level_r REAL,
            highest_tp_touched INTEGER,
            first_event TEXT,
            close_event TEXT,
            giveback INTEGER,
            same_candle_ambiguous INTEGER,
            computed_at TEXT,
            version TEXT,
            evidence_class TEXT,
            frozen_at TEXT,
            lifecycle_state TEXT,
            entry_at TEXT,
            entry_price_used REAL,
            exit_at TEXT,
            exit_at_source TEXT,
            decision_at TEXT,
            first_executable_price REAL,
            entry_drift_bps REAL,
            signal_snapshot_json TEXT,
            entry_bar_open_at TEXT,
            entry_time_basis TEXT,
            current_price_revalidated INTEGER,
            effective_expires_at TEXT,
            execution_validity TEXT,
            paper_entry_profile TEXT,
            paper_execution_entry_mode TEXT,
            path_realized_r REAL,
            path_remaining_fraction REAL,
            path_last_candle_at TEXT,
            path_tp1_filled INTEGER,
            path_tp2_filled INTEGER,
            path_tp3_filled INTEGER,
            path_max_mfe_r REAL,
            path_data_quality TEXT,
            path_gap_seconds REAL
        )
        """
    )
    existing = {r[1] for r in conn.execute(f"PRAGMA table_info({_TABLE})")}
    for col, typ in _NEW_COLUMNS:
        if col not in existing:
            try:
                conn.execute(f"ALTER TABLE {_TABLE} ADD COLUMN {col} {typ}")
            except Exception:
                pass
    # Rows that predate lifecycle_state and never entered are safe to classify.
    # Entered legacy rows are repaired by backfill_all; do not guess them here.
    conn.execute(
        f"UPDATE {_TABLE} SET lifecycle_state='NO_ENTRY' "
        "WHERE lifecycle_state IS NULL AND paper_execution_r IS NULL "
        "AND COALESCE(paper_execution_outcome,'no_entry')='no_entry'"
    )
    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{_TABLE}_key ON {_TABLE}(economic_trade_key)")


def upsert_outcome(conn, *, signal_id: str, economic_trade_key: str, computed_at: str,
                   record: dict[str, Any], repair: bool = False) -> None:
    """Monotonic upsert keyed by signal_id.

    Normal tracker writes can advance NO_ENTRY -> OPEN -> CLOSED, never rewind,
    and the first CLOSED record wins. ``repair`` is reserved for the explicit
    deterministic backfill that repairs rows created under the old TP1/TP2-as-
    terminal semantics.
    """
    canonical_profile = _canonical_profile_for_entry_mode(
        record.get("paper_entry_profile"), record.get("paper_execution_entry_mode"))
    row = {
        "signal_id": signal_id,
        "economic_trade_key": economic_trade_key,
        "risk_model": record.get("risk_model"),
        "touch_r": record.get("touch_r"),
        "paper_execution_r": record.get("paper_execution_r"),
        "paper_execution_outcome": record.get("paper_execution_outcome"),
        "close_reason": record.get("close_reason"),
        "stop_initial": record.get("stop_initial"),
        "stop_current_r": record.get("stop_current_r"),
        "protection_armed": int(bool(record.get("protection_armed"))),
        "protection_level_r": record.get("protection_level_r"),
        "lock_armed": int(bool(record.get("lock_armed"))),
        "lock_level_r": record.get("lock_level_r"),
        "highest_tp_touched": record.get("highest_tp_touched"),
        "first_event": record.get("first_event"),
        "close_event": record.get("close_event"),
        "giveback": int(bool(record.get("giveback"))),
        "same_candle_ambiguous": int(bool(record.get("same_candle_ambiguous"))),
        "computed_at": computed_at,
        "version": record.get("version"),
        "evidence_class": record.get("evidence_class"),
        "frozen_at": record.get("frozen_at"),
        "lifecycle_state": record.get("lifecycle_state"),
        "entry_at": record.get("entry_at"),
        "entry_price_used": record.get("entry_price_used"),
        "exit_at": record.get("exit_at"),
        "exit_at_source": record.get("exit_at_source"),
        "decision_at": record.get("decision_at"),
        "first_executable_price": record.get("first_executable_price"),
        "entry_drift_bps": record.get("entry_drift_bps"),
        "signal_snapshot_json": record.get("signal_snapshot_json"),
        "entry_bar_open_at": record.get("entry_bar_open_at"),
        "entry_time_basis": record.get("entry_time_basis"),
        "current_price_revalidated": (
            None if record.get("current_price_revalidated") is None
            else int(bool(record.get("current_price_revalidated")))
        ),
        "effective_expires_at": record.get("effective_expires_at"),
        "execution_validity": record.get("execution_validity") or "valid",
        "paper_entry_profile": canonical_profile,
        "paper_execution_entry_mode": record.get("paper_execution_entry_mode"),
        "path_realized_r": record.get("path_realized_r"),
        "path_remaining_fraction": record.get("path_remaining_fraction"),
        "path_last_candle_at": record.get("path_last_candle_at"),
        "path_tp1_filled": (
            None if record.get("path_tp1_filled") is None
            else int(bool(record.get("path_tp1_filled")))
        ),
        "path_tp2_filled": (
            None if record.get("path_tp2_filled") is None
            else int(bool(record.get("path_tp2_filled")))
        ),
        "path_tp3_filled": (
            None if record.get("path_tp3_filled") is None
            else int(bool(record.get("path_tp3_filled")))
        ),
        "path_max_mfe_r": record.get("path_max_mfe_r"),
        "path_data_quality": record.get("path_data_quality"),
        "path_gap_seconds": record.get("path_gap_seconds"),
    }
    cur = conn.execute(f"SELECT * FROM {_TABLE} WHERE signal_id=?", (signal_id,))
    existing = cur.fetchone()
    if existing is not None:
        old = (dict(existing) if hasattr(existing, "keys") else
               dict(zip((d[0] for d in cur.description), existing)))
        old_state = str(old.get("lifecycle_state") or
                        ("CLOSED" if old.get("paper_execution_r") is not None else
                         "OPEN" if old.get("paper_execution_outcome") == "open" else "NO_ENTRY"))
        new_state = str(row.get("lifecycle_state") or "NO_ENTRY")
        profile_upgrade = _is_specific_profile_upgrade(
            old.get("paper_entry_profile"), row.get("paper_entry_profile"),
            row.get("paper_execution_entry_mode") or old.get("paper_execution_entry_mode"),
        )
        if (repair
                and str(old.get("version") or "") == LIVE_EXIT_PARITY_VERSION
                and str(row.get("version") or "") != LIVE_EXIT_PARITY_VERSION):
            # Aggregate legacy touches cannot replace a path-ordered forward
            # observation from the live-parity state machine.
            return
        if (not repair
                and str(old.get("version") or "") == LIVE_EXIT_PARITY_VERSION
                and str(row.get("version") or "") != LIVE_EXIT_PARITY_VERSION):
            # A transient candle/API failure must not roll an incremental
            # path row back to the aggregate touch model on a later tick.
            if profile_upgrade:
                conn.execute(
                    f"UPDATE {_TABLE} SET paper_entry_profile=?, "
                    "paper_execution_entry_mode=COALESCE(paper_execution_entry_mode, ?) "
                    "WHERE signal_id=?",
                    (row.get("paper_entry_profile"), row.get("paper_execution_entry_mode"), signal_id),
                )
            return
        if not repair and (old_state == "CLOSED" or (old_state == "OPEN" and new_state == "NO_ENTRY")):
            if profile_upgrade:
                conn.execute(
                    f"UPDATE {_TABLE} SET paper_entry_profile=?, "
                    "paper_execution_entry_mode=COALESCE(paper_execution_entry_mode, ?) "
                    "WHERE signal_id=?",
                    (row.get("paper_entry_profile"), row.get("paper_execution_entry_mode"), signal_id),
                )
            return
        # A historical candle reconstruction is useful for research, but it
        # must never permanently win over the first genuinely point-in-time
        # execution observation.  Otherwise a later live handoff inherits an
        # hours-old ``entry_at`` and is rejected as ENTRY_TOO_OLD even though
        # the current price was freshly revalidated.
        signal_snapshot = {}
        try:
            signal_snapshot = json.loads(row.get("signal_snapshot_json") or "{}")
        except (TypeError, ValueError, json.JSONDecodeError):
            pass
        is_stocks_intraday = (
            str(signal_snapshot.get("asset_class") or "").lower().startswith("stock")
            and str(signal_snapshot.get("mode") or "").lower() == "intraday"
        )
        old_rank = paper_provenance_rank(
            old.get("entry_time_basis"), stocks_intraday=is_stocks_intraday)
        new_rank = paper_provenance_rank(
            row.get("entry_time_basis"), stocks_intraday=is_stocks_intraday)
        promote_realtime_provenance = bool(row.get("current_price_revalidated")) and (
            new_rank > old_rank
            or (new_rank == old_rank and new_rank > 0
                and not bool(old.get("current_price_revalidated")))
        )
        for name in ("entry_at", "entry_price_used", "decision_at", "first_executable_price",
                     "entry_drift_bps", "signal_snapshot_json", "entry_bar_open_at",
                     "entry_time_basis", "current_price_revalidated", "effective_expires_at",
                     "paper_entry_profile", "paper_execution_entry_mode"):
            # A deterministic repair may correct the displayed entry timestamp
            # and price for a known delayed-provider stock row. Do not let old
            # candle-touch values win over the recorded decision-time quote.
            if (repair and name in {"entry_at", "entry_price_used"}
                    and str(old.get("entry_time_basis") or "")
                    == "provider_delayed_current_bar"):
                continue
            if promote_realtime_provenance and name in {
                    "entry_at", "entry_price_used", "decision_at", "first_executable_price",
                    "entry_drift_bps", "entry_bar_open_at", "entry_time_basis",
                    "current_price_revalidated"}:
                continue
            if name == "paper_entry_profile" and profile_upgrade:
                continue
            if old.get(name) not in (None, ""):
                row[name] = old[name]
        row["highest_tp_touched"] = max(int(old.get("highest_tp_touched") or 0),
                                         int(row.get("highest_tp_touched") or 0))
        # A path-safety repair can deliberately invalidate a previously
        # inferred MFE/lock. Do not retain a stale ``lock_armed=1`` beside an
        # ``original_stop`` result; that is internally contradictory and
        # leaks the old optimistic interpretation into reports.
        if not bool(row.get("same_candle_ambiguous")):
            row["protection_armed"] = max(int(old.get("protection_armed") or 0),
                                           int(row.get("protection_armed") or 0))
            row["lock_armed"] = max(int(old.get("lock_armed") or 0), int(row.get("lock_armed") or 0))
    cols = ", ".join(_COLS)
    placeholders = ", ".join("?" for _ in _COLS)
    updates = ", ".join(f"{c}=excluded.{c}" for c in _COLS if c != "signal_id")
    conn.execute(
        f"INSERT INTO {_TABLE} ({cols}) VALUES ({placeholders}) "
        f"ON CONFLICT(signal_id) DO UPDATE SET {updates}",
        [row[c] for c in _COLS],
    )


# --------------------------------------------------- signal/outcome adapters --
def _round_zone(entry: float | None) -> Any:
    if not entry:
        return None
    import math
    digits = 3 - int(math.floor(math.log10(abs(entry))))
    return round(entry, max(0, digits))


def economic_trade_key(signal: dict[str, Any], entry_day: str) -> str:
    """Deterministic dedup key — mirrors the Control Plane read-model's key."""
    entry = (_f(signal.get("entry_trigger")) or _f(signal.get("suggested_entry"))
             or _f(signal.get("entry_low")))
    parts = (
        str(signal.get("symbol") or "?"),
        str(signal.get("asset_class") or "crypto").lower(),
        str(signal.get("mode") or "").lower(),
        str(signal.get("direction") or "").lower(),
        str(signal.get("tier") or "").upper(),
        str(signal.get("setup_type") or signal.get("playbook") or ""),
        str(_round_zone(entry)),
        entry_day,
    )
    return "|".join(parts)


_SNAPSHOT_FIELDS = (
    "signal_id", "symbol", "asset_class", "mode", "direction", "tier", "setup_type",
    "entry_type", "entry_low", "entry_high", "entry_trigger", "suggested_entry",
    "stop_loss", "invalidation", "tp1", "tp2", "tp3", "risk_per_unit",
    "created_at", "expires_at", "paper_entry_profile", "paper_execution_entry_mode",
    "paper_entry_profile_gate",
)


def _execution_snapshot(signal: dict[str, Any]) -> str:
    return json.dumps({k: signal.get(k) for k in _SNAPSHOT_FIELDS}, sort_keys=True,
                      separators=(",", ":"), default=str)


_FROZEN_GEOMETRY_FIELDS = (
    "direction", "entry_type", "entry_low", "entry_high", "entry_trigger",
    "suggested_entry", "stop_loss", "invalidation", "tp1", "tp2", "tp3",
    "risk_per_unit", "expires_at",
)


def _snapshot_payload(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    try:
        parsed = json.loads(value or "{}")
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _same_geometry_value(left: Any, right: Any) -> bool:
    left_num, right_num = _f(left), _f(right)
    if left_num is not None and right_num is not None:
        return abs(left_num - right_num) <= max(1e-12, abs(left_num) * 1e-10)
    return left == right


def _apply_frozen_geometry(
    signal: dict[str, Any], snapshot_json: Any,
) -> tuple[dict[str, Any], bool]:
    """Overlay immutable execution geometry captured at the first Paper entry.

    Returns the corrected signal plus whether the caller supplied conflicting
    geometry. Profile/provenance fields deliberately remain upgradeable.
    """
    snapshot = _snapshot_payload(snapshot_json)
    corrected = dict(signal)
    changed = False
    for field in _FROZEN_GEOMETRY_FIELDS:
        if field not in snapshot:
            continue
        if not _same_geometry_value(corrected.get(field), snapshot.get(field)):
            changed = True
        corrected[field] = snapshot.get(field)
    return corrected, changed


def _stored_stop_disagrees_with_snapshot(stop_initial: Any, snapshot_json: Any) -> bool:
    snapshot = _snapshot_payload(snapshot_json)
    frozen_stop = _f(snapshot.get("invalidation")) or _f(snapshot.get("stop_loss"))
    stored_stop = _f(stop_initial)
    return bool(
        frozen_stop is not None and stored_stop is not None
        and not _same_geometry_value(stored_stop, frozen_stop)
    )


def _raw_signal_payload(signal: dict[str, Any]) -> dict[str, Any]:
    raw = signal.get("raw_idea_json")
    if isinstance(raw, dict):
        return raw
    try:
        parsed = json.loads(raw or "{}")
    except Exception:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _record_paper_profile(signal: dict[str, Any]) -> str | None:
    explicit = str(signal.get("paper_entry_profile") or "").strip()
    if explicit:
        return explicit
    raw = _raw_signal_payload(signal)
    for key in ("paper_entry_profile", "paper_target_profile_version"):
        value = raw.get(key)
        if value:
            return str(value)
    setup = raw.get("raw_setup") if isinstance(raw.get("raw_setup"), dict) else raw.get("setup")
    if isinstance(setup, dict):
        for key in ("paper_entry_profile", "paper_target_profile_version"):
            value = setup.get(key)
            if value:
                return str(value)
    if (str(signal.get("asset_class") or "crypto").lower() == "crypto"
            and str(signal.get("mode") or "").lower() == "swing"):
        try:
            from src.execution.crypto_swing_paper_policy import load_cfg, target_profile, targets_match_profile
            cfg = load_cfg()
            profile = target_profile(signal, profile="production", cfg=cfg)
            if profile.get("available") and targets_match_profile(signal, profile):
                return str(profile.get("version") or "") or None
        except Exception:
            return None
    return None


def _record_entry_mode(signal: dict[str, Any]) -> str | None:
    for key in ("paper_execution_entry_mode", "stored_entry_mode", "paper_source_entry_mode"):
        value = str(signal.get(key) or "").strip().upper()
        if value:
            return value
    raw = _raw_signal_payload(signal)
    for key in ("paper_execution_entry_mode", "entry_mode", "source_entry_mode"):
        value = str(raw.get(key) or "").strip().upper()
        if value:
            return value
    setup = raw.get("raw_setup") if isinstance(raw.get("raw_setup"), dict) else raw.get("setup")
    if isinstance(setup, dict):
        for key in ("paper_execution_entry_mode", "entry_mode", "source_entry_mode"):
            value = str(setup.get(key) or "").strip().upper()
            if value:
                return value
    return None


_GENERIC_CRYPTO_SWING_PROFILE = "crypto_swing_paper_t130_v1"
_SPECIFIC_CRYPTO_SWING_PROFILE_BY_MODE = {
    "BREAKOUT_RECLAIM_V2": "crypto_swing_breakout_reclaim_paper_v2",
    "PULLBACK_CONFIRMED_RETEST": "crypto_swing_pullback_confirmed_retest_paper_v1",
    "FIB_IMPULSE_RETEST": "crypto_swing_fib_impulse_retest_paper_v1",
}


def _canonical_profile_for_entry_mode(profile: Any, entry_mode: Any) -> str | None:
    current = str(profile or "").strip()
    mode = str(entry_mode or "").strip().upper()
    specific = _SPECIFIC_CRYPTO_SWING_PROFILE_BY_MODE.get(mode)
    if specific and current in ("", _GENERIC_CRYPTO_SWING_PROFILE):
        return specific
    return current or None


def _is_specific_profile_upgrade(old_profile: Any, new_profile: Any, entry_mode: Any) -> bool:
    mode = str(entry_mode or "").strip().upper()
    expected = _SPECIFIC_CRYPTO_SWING_PROFILE_BY_MODE.get(mode)
    return bool(
        expected
        and str(new_profile or "").strip() == expected
        and str(old_profile or "").strip() in ("", _GENERIC_CRYPTO_SWING_PROFILE)
    )


def repair_specific_crypto_swing_profiles(conn) -> dict[str, int]:
    """Split three versioned swing strategies out of the legacy T130 bucket.

    This is provenance-only repair: outcomes, lifecycle, prices, R and PnL are
    untouched. It is idempotent and intentionally requires a known executed
    mode, so generic swing rows are never guessed into a strategy.
    """
    ensure_table(conn)
    repaired: dict[str, int] = {}
    for mode, profile in _SPECIFIC_CRYPTO_SWING_PROFILE_BY_MODE.items():
        cur = conn.execute(
            f"UPDATE {_TABLE} SET paper_entry_profile=? "
            "WHERE UPPER(COALESCE(paper_execution_entry_mode,''))=? "
            "AND COALESCE(paper_entry_profile,'') IN ('', ?)",
            (profile, mode, _GENERIC_CRYPTO_SWING_PROFILE),
        )
        repaired[mode] = max(0, int(cur.rowcount or 0))
    return repaired


def _terminal_time(outcome_row: dict[str, Any], rec: dict[str, Any]) -> tuple[str | None, str | None]:
    reason = str(rec.get("close_reason") or "")
    if reason == "tp3_runner":
        return outcome_row.get("tp3_hit_at"), "tp3_hit_at"
    if reason == "original_stop":
        return outcome_row.get("stop_hit_at"), "original_stop_hit_at"
    if reason in ("breakeven_stop", "profit_lock_stop"):
        # The legacy candle walk records the later original-stop touch. It is the
        # only path-safe timestamp available for the inferred moved-stop exit.
        if outcome_row.get("stop_hit_at"):
            return outcome_row.get("stop_hit_at"), "original_stop_touch_proxy"
        return (outcome_row.get("expires_at") or outcome_row.get("checked_at"),
                "expires_at_protected" if outcome_row.get("expires_at") else
                "checked_at_expiry_proxy")
    if "expired" in reason or rec.get("close_event") == "expiry":
        return (outcome_row.get("expires_at") or outcome_row.get("checked_at"),
                "expires_at" if outcome_row.get("expires_at") else "checked_at_expiry_proxy")
    if rec.get("same_candle_ambiguous"):
        return (outcome_row.get("stop_hit_at") or outcome_row.get("checked_at"),
                "ambiguous_stop_first")
    return None, None


def _entry_drift_bps(direction: str, planned: float | None, observed: float | None) -> float | None:
    if planned in (None, 0) or observed is None:
        return None
    sign = -1.0 if str(direction or "long").lower() == "short" else 1.0
    return round(sign * (observed - planned) / planned * 10000.0, 3)


def _effective_expiry(signal: dict[str, Any], configured_expiry: Any) -> datetime | None:
    """Return the economic expiry, including the non-negotiable stock EOD rule."""
    expiry = _parse_ts(configured_expiry)
    if not (
        str(signal.get("asset_class") or "").lower().startswith("stock")
        and str(signal.get("mode") or "").lower() == "intraday"
    ):
        return expiry
    created = _parse_ts(signal.get("created_at"))
    if created is None:
        return expiry
    try:
        from src.stocks.market_calendar import stock_intraday_target_session_close
        close = stock_intraday_target_session_close(created)
    except Exception:
        close = None
    if close is None:
        return expiry
    if expiry is not None and expiry < created:
        return close
    return min(expiry, close) if expiry is not None else close


def _finalize_expired_execution_path(
    path: dict[str, Any], *, expiry: datetime | None, as_of_iso: str | None,
) -> dict[str, Any]:
    """Finalize a parity path without inventing a market close price."""
    finalized = dict(path)
    if finalized.get("terminal") or str(finalized.get("path_data_quality") or "") == "gap":
        return finalized
    remaining = _f(finalized.get("path_remaining_fraction"))
    realized = _f(finalized.get("path_realized_r"))
    stop_r = _f(finalized.get("stop_current_r"))
    if remaining is None or realized is None or stop_r is None:
        return finalized
    remaining = min(1.0, max(0.0, remaining))
    total_r = realized + remaining * max(0.0, stop_r)
    reason = "expiry_profit_lock" if stop_r > 0 else (
        "expiry_breakeven" if stop_r == 0 else "expired_flat")
    outcome = "win" if total_r > 1e-12 else "loss" if total_r < -1e-12 else "expired"
    observed = _parse_ts(as_of_iso)
    use_expiry = expiry is not None and (observed is None or expiry <= observed)
    exit_at = expiry.isoformat() if use_expiry else None
    if exit_at is None:
        exit_at = observed.isoformat() if observed is not None else None
    finalized.update(
        terminal=True,
        paper_execution_r=round(total_r, 4),
        paper_execution_outcome=outcome,
        close_reason=reason,
        close_event="expiry",
        exit_at=exit_at,
        exit_at_source=("expires_at_protected" if use_expiry
                        else "expiry_observed_at"),
        path_realized_r=round(total_r, 6),
        path_remaining_fraction=0.0,
        remaining_fraction=0.0,
    )
    return finalized


def _stored_execution_path(row: dict[str, Any]) -> dict[str, Any] | None:
    """Rehydrate a persisted parity-v3 path from its additive ledger fields."""
    if str(row.get("version") or "") != LIVE_EXIT_PARITY_VERSION:
        return None
    return {
        "version": row.get("version"),
        "terminal": (str(row.get("lifecycle_state") or "").upper() == "CLOSED"
                     or row.get("paper_execution_r") is not None),
        "paper_execution_r": row.get("paper_execution_r"),
        "paper_execution_outcome": row.get("paper_execution_outcome"),
        "close_reason": row.get("close_reason"),
        "close_event": row.get("close_event"),
        "exit_at": row.get("exit_at"),
        "exit_at_source": row.get("exit_at_source"),
        "highest_tp_touched": row.get("highest_tp_touched"),
        "stop_current_r": row.get("stop_current_r"),
        "protection_armed": bool(row.get("protection_armed")),
        "lock_armed": bool(row.get("lock_armed")),
        "same_candle_ambiguous": bool(row.get("same_candle_ambiguous")),
        "path_realized_r": row.get("path_realized_r"),
        "path_remaining_fraction": row.get("path_remaining_fraction"),
        "path_last_candle_at": row.get("path_last_candle_at"),
        "path_tp1_filled": bool(row.get("path_tp1_filled")),
        "path_tp2_filled": bool(row.get("path_tp2_filled")),
        "path_tp3_filled": bool(row.get("path_tp3_filled")),
        "path_max_mfe_r": row.get("path_max_mfe_r"),
        "path_data_quality": row.get("path_data_quality"),
        "path_gap_seconds": row.get("path_gap_seconds"),
    }


def _stock_intraday_execution_validity(
    signal: dict[str, Any], outcome_row: dict[str, Any], expiry: datetime | None,
    *, entry_time_basis: str | None = None, current_price_revalidated: bool | None = None,
) -> str:
    """Reject legacy stock-intraday PnL whose decisive event was after RTH.

    We retain the source outcome for audit, but it cannot be an intraday Paper
    execution. A past close without an event timestamp is also not eligible for
    an authoritative ledger: it has no proof that it closed inside RTH.
    """
    if not (
        str(signal.get("asset_class") or "").lower().startswith("stock")
        and str(signal.get("mode") or "").lower() == "intraday"
    ):
        return "valid"
    # A historical candle range cannot prove an executable Paper entry.  The
    # free stock provider's delayed current bar is accepted only when the
    # Paper-only config flag is enabled AND the current price was independently
    # revalidated. A missing basis remains legacy/backfill diagnostics only.
    if entry_time_basis is not None and (
        not is_accepted_stock_intraday_paper_basis(entry_time_basis)
        or current_price_revalidated is not True
    ):
        return "invalid_stock_intraday_entry_not_point_in_time"
    if expiry is None:
        return "invalid_stock_intraday_missing_session_expiry"
    entry_at = _parse_ts(outcome_row.get("entry_triggered_at"))
    if entry_at is not None and entry_at >= expiry:
        return "invalid_stock_intraday_entry_after_rth"
    status = str(outcome_row.get("status") or "").lower()
    hit_fields = (
        ("tp1_hit", "tp1_hit_at"), ("tp2_hit", "tp2_hit_at"),
        ("tp3_hit", "tp3_hit_at"), ("stop_hit", "stop_hit_at"),
    )
    for hit_field, at_field in hit_fields:
        if not outcome_row.get(hit_field):
            continue
        event_at = _parse_ts(outcome_row.get(at_field))
        if event_at is None:
            return "invalid_stock_intraday_missing_terminal_time"
        if event_at >= expiry:
            return "invalid_stock_intraday_overnight_event"
    if status in {"tp3_hit", "stopped", "ambiguous"}:
        terminal_at = _parse_ts(outcome_row.get("checked_at"))
        if terminal_at is not None and terminal_at >= expiry and not any(
            outcome_row.get(at_field) for _, at_field in hit_fields
        ):
            return "invalid_stock_intraday_missing_terminal_time"
    return "valid"


def build_record_from_signal(signal: dict[str, Any], outcome_row: dict[str, Any],
                             risk_model: str = DEFAULT_RISK_MODEL, *,
                             decision_at: str | None = None,
                             first_executable_price: float | None = None,
                             entry_time_basis: str | None = None,
                             current_price_revalidated: bool | None = None,
                             as_of_iso: str | None = None,
                             execution_path: dict[str, Any] | None = None,
                             ) -> tuple[str, str, dict[str, Any]]:
    """Build (signal_id, economic_trade_key, paper-execution record) from a
    signal dict + its latest signal_outcomes row. Pure / read-only."""
    status = str(outcome_row.get("status") or "").lower()
    entered = bool(outcome_row.get("entry_triggered")) or bool(outcome_row.get("entry_triggered_at"))
    reached_tp1 = bool(outcome_row.get("tp1_hit"))
    reached_tp2 = bool(outcome_row.get("tp2_hit"))
    reached_tp3 = bool(outcome_row.get("tp3_hit"))
    hit_stop = bool(outcome_row.get("stop_hit"))
    # final_outcome='expired' is a legacy placeholder even while status is
    # triggered/open. Only the lifecycle status (or explicit note) is terminal.
    expires_at = outcome_row.get("expires_at") or signal.get("expires_at")
    as_of = _parse_ts(as_of_iso)
    expiry = _effective_expiry(signal, expires_at)
    # A later revalidator row can be `entry_moved_away` even after a real entry
    # occurred. Once the original validity window has passed, the entered trade
    # must resolve through Model F instead of remaining OPEN forever.
    expired = (
        status == "expired"
        or "expired within validity window" in str(outcome_row.get("notes") or "").lower()
        or bool(as_of and expiry and as_of >= expiry)
    )
    same_candle = "ambiguous" in str(outcome_row.get("notes") or "").lower() or str(outcome_row.get("status") or "") == "ambiguous"
    planned_entry = (_f(signal.get("entry_trigger")) or _f(signal.get("suggested_entry"))
                     or _f(signal.get("entry_low")))
    legacy_entry = _f(outcome_row.get("entry_price_used")) or planned_entry
    # Preserve the time/price the engine actually observed whenever it is
    # available, even when a later validity rule rejects it as non-executable
    # (for example a delayed stock-provider bar).  The validity gate below is
    # the authority for ledger inclusion; this distinction keeps audit and UI
    # timestamps honest without manufacturing Paper PnL.
    observed_entry = bool(decision_at and first_executable_price is not None)
    entry = _f(first_executable_price) if observed_entry else legacy_entry
    entry = entry or legacy_entry
    bar_open_at = str(outcome_row.get("entry_triggered_at") or "") or None
    ts = (str(decision_at or "") if observed_entry else
          (bar_open_at or str(signal.get("created_at") or "")))
    rec = compute_paper_execution(
        direction=str(signal.get("direction") or "long"),
        entry=entry,
        stop=(_f(signal.get("invalidation")) or _f(signal.get("stop_loss"))),
        tp1=_f(signal.get("tp1")), tp2=_f(signal.get("tp2")), tp3=_f(signal.get("tp3")),
        reached_tp1=reached_tp1, reached_tp2=reached_tp2, reached_tp3=reached_tp3,
        hit_stop=hit_stop, expired=expired, entered=entered,
        mfe_r=_f(outcome_row.get("max_favorable_excursion_r")),
        same_candle_ambiguous=same_candle, risk_model=risk_model,
        entry_ts=ts or None,
    )
    resolved_execution_path = execution_path
    if (execution_path
            and str(execution_path.get("version") or "") == LIVE_EXIT_PARITY_VERSION
            and expired and not execution_path.get("terminal")):
        resolved_execution_path = _finalize_expired_execution_path(
            execution_path, expiry=expiry, as_of_iso=as_of_iso)
    if (resolved_execution_path
            and str(resolved_execution_path.get("version") or "") == LIVE_EXIT_PARITY_VERSION):
        rec.update(
            paper_execution_r=resolved_execution_path.get("paper_execution_r"),
            paper_execution_outcome=resolved_execution_path.get("paper_execution_outcome"),
            close_reason=resolved_execution_path.get("close_reason"),
            close_event=resolved_execution_path.get("close_event"),
            highest_tp_touched=int(resolved_execution_path.get("highest_tp_touched") or 0),
            stop_current_r=resolved_execution_path.get("stop_current_r"),
            protection_armed=bool(resolved_execution_path.get("protection_armed")),
            lock_armed=bool(resolved_execution_path.get("lock_armed")),
            same_candle_ambiguous=bool(resolved_execution_path.get("same_candle_ambiguous")),
            path_realized_r=resolved_execution_path.get("path_realized_r"),
            path_remaining_fraction=resolved_execution_path.get("path_remaining_fraction"),
            path_last_candle_at=resolved_execution_path.get("path_last_candle_at"),
            path_tp1_filled=resolved_execution_path.get("path_tp1_filled"),
            path_tp2_filled=resolved_execution_path.get("path_tp2_filled"),
            path_tp3_filled=resolved_execution_path.get("path_tp3_filled"),
            path_max_mfe_r=resolved_execution_path.get("path_max_mfe_r"),
            path_data_quality=resolved_execution_path.get("path_data_quality"),
            path_gap_seconds=resolved_execution_path.get("path_gap_seconds"),
            version=LIVE_EXIT_PARITY_VERSION,
        )
    validity = _stock_intraday_execution_validity(
        signal, outcome_row, expiry, entry_time_basis=entry_time_basis,
        current_price_revalidated=current_price_revalidated,
    )
    is_crypto = str(signal.get("asset_class") or "crypto").lower() == "crypto"
    if (validity == "valid" and is_crypto and entered and entry_time_basis is not None
            and (entry_time_basis != "point_in_time_current_bar"
                 or current_price_revalidated is not True)):
        # A candle-range touch is research evidence, not an executable Paper
        # fill. Live already requires this provenance; applying the same rule
        # here removes a major Paper/Live selection mismatch.
        validity = "invalid_crypto_entry_not_point_in_time"
    if signal.get("_execution_geometry_mutated_after_entry"):
        validity = "invalid_signal_geometry_mutated_after_entry"
    if (resolved_execution_path
            and str(resolved_execution_path.get("path_data_quality") or "") == "gap"):
        validity = "invalid_execution_path_gap"
    elif (expired and execution_path
          and str(execution_path.get("version") or "") == LIVE_EXIT_PARITY_VERSION
          and not (resolved_execution_path or {}).get("terminal")):
        validity = "invalid_expired_execution_path_state"
    paper_entry_mode = _record_entry_mode(signal)
    paper_profile = _canonical_profile_for_entry_mode(
        _record_paper_profile(signal), paper_entry_mode)
    if validity == "valid" and paper_profile:
        from src.execution.paper_entry_provenance import PROFILE_ENTRY_MODES
        expected_mode = PROFILE_ENTRY_MODES.get(paper_profile)
        if expected_mode and paper_entry_mode != expected_mode:
            validity = "invalid_paper_profile_entry_mode_mismatch"
    terminal_row = dict(outcome_row)
    terminal_row["expires_at"] = expiry.isoformat() if expiry is not None else None
    exit_at, exit_source = _terminal_time(terminal_row, rec)
    if resolved_execution_path and resolved_execution_path.get("terminal"):
        exit_at = resolved_execution_path.get("exit_at")
        exit_source = resolved_execution_path.get("exit_at_source")
    first_exec = _f(first_executable_price if first_executable_price is not None
                    else outcome_row.get("first_executable_price"))
    lifecycle = ("CLOSED" if rec.get("paper_execution_r") is not None else
                 "OPEN" if entered else "NO_ENTRY")
    if validity != "valid":
        # Never transform a next-day touch into synthetic EOD PnL without the
        # complete session path. Keep the raw source rows, but remove this
        # contaminated legacy observation from the authoritative Paper ledger.
        rec.update(paper_execution_r=None, paper_execution_outcome="invalid_session",
                   close_reason=validity, close_event="invalid_session")
        exit_at, exit_source, lifecycle = None, None, "INVALID"
    rec.update(
        lifecycle_state=lifecycle,
        entry_at=(ts or None),
        entry_price_used=entry,
        exit_at=exit_at,
        exit_at_source=exit_source,
        decision_at=decision_at or outcome_row.get("decision_at"),
        first_executable_price=first_exec,
        entry_drift_bps=_entry_drift_bps(str(signal.get("direction") or "long"), planned_entry, first_exec),
        signal_snapshot_json=_execution_snapshot(signal),
        entry_bar_open_at=bar_open_at,
        # None means legacy/backfill-unclassified. The realtime tracker always
        # supplies an explicit basis on a new entry transition; deterministic
        # historical repair must not retroactively label old rows unverified.
        entry_time_basis=entry_time_basis,
        current_price_revalidated=current_price_revalidated,
        effective_expires_at=expiry.isoformat() if expiry is not None else None,
        execution_validity=validity,
        paper_entry_profile=paper_profile,
        paper_execution_entry_mode=paper_entry_mode,
    )
    entry_day = ts[:10] if ts else "?"
    return str(signal.get("signal_id")), economic_trade_key(signal, entry_day), rec


def record_paper_execution(store, *, signal: dict[str, Any], outcome_row: dict[str, Any],
                           now_iso: str, risk_model: str = DEFAULT_RISK_MODEL,
                           decision_at: str | None = None,
                           first_executable_price: float | None = None,
                           entry_time_basis: str | None = None,
                           current_price_revalidated: bool | None = None,
                           paper_entry_profile: str | None = None,
                           paper_execution_entry_mode: str | None = None,
                           paper_entry_profile_gate: dict[str, Any] | None = None,
                           execution_path: dict[str, Any] | None = None) -> bool:
    """Fail-open: compute + upsert paper execution outcome for one signal.

    Opens its own connection (mirrors store.add_signal_outcome). Returns True on
    success, False on any error (caller must NOT block legacy tracking)."""
    try:
        with store.connect() as conn:
            ensure_table(conn)
            previous = conn.execute(
                f"SELECT COALESCE(decision_at,entry_at),"
                "COALESCE(first_executable_price,entry_price_used),"
                "entry_time_basis,current_price_revalidated,lifecycle_state,"
                f"signal_snapshot_json,stop_initial FROM {_TABLE} WHERE signal_id=?",
                (str(signal.get("signal_id") or ""),),
            ).fetchone()
            # Later tracker ticks and the full-refresh repair only carry the
            # legacy candle-touch row. Preserve the entry-time provenance
            # captured on the actual transition instead of silently replacing
            # it with the signal creation time and planned price.
            if entry_time_basis is None:
                if previous is not None and previous[2] is not None:
                    decision_at = previous[0]
                    first_executable_price = previous[1]
                    entry_time_basis = previous[2]
                    current_price_revalidated = bool(previous[3])
            execution_signal = dict(signal)
            if paper_entry_profile:
                execution_signal["paper_entry_profile"] = paper_entry_profile
            if paper_execution_entry_mode:
                execution_signal["paper_execution_entry_mode"] = paper_execution_entry_mode
            if paper_entry_profile_gate:
                execution_signal["paper_entry_profile_gate"] = paper_entry_profile_gate
            if (previous is not None
                    and str(previous[4] or "").upper() in {"OPEN", "CLOSED"}
                    and previous[5]):
                execution_signal, geometry_changed = _apply_frozen_geometry(
                    execution_signal, previous[5])
                if geometry_changed:
                    execution_signal["_execution_geometry_mutated_after_entry"] = True
            sid, key, rec = build_record_from_signal(
                execution_signal, outcome_row, risk_model, decision_at=decision_at,
                first_executable_price=first_executable_price,
                entry_time_basis=entry_time_basis,
                current_price_revalidated=current_price_revalidated,
                as_of_iso=now_iso,
                execution_path=execution_path)
            upsert_outcome(conn, signal_id=sid, economic_trade_key=key,
                           computed_at=now_iso, record=rec)
        return True
    except Exception:
        return False


def _has_table(conn, name: str) -> bool:
    return bool(conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)).fetchone())


def backfill_evidence_class_only(conn, *, now_iso: str) -> dict[str, int]:
    """Fixup pass for paper_execution_outcomes rows whose evidence_class is still NULL — rows OUTSIDE
    backfill_all()'s join scope (e.g. their signal_id no longer resolves through signal_outcomes/
    proposed_signals, a pruned/legacy row, or the row predates the evidence_class column and was
    never revisited). For each: try to recover the trade's real entry_ts the same way
    build_record_from_signal does (entry_triggered_at, falling back to created_at); evidence_class_for
    already defaults conservatively to backfill_pretrained when the timestamp is missing or
    unparseable, so an unrecoverable row is classified backfill_pretrained rather than left NULL — a
    deliberate choice (never a gray zone, never fabricated forward evidence).

    ONLY updates evidence_class/frozen_at via a narrow UPDATE — never touches touch_r,
    paper_execution_r, close_reason, or any other field, and never touches signal_outcomes/
    proposed_signals/final_r. Returns {scanned, recovered_ts, defaulted_backfill}."""
    ensure_table(conn)
    rows = conn.execute(f"SELECT signal_id FROM {_TABLE} WHERE evidence_class IS NULL").fetchall()
    has_so = _has_table(conn, "signal_outcomes")
    has_ps = _has_table(conn, "proposed_signals")
    recovered = defaulted = 0
    for index, (sid,) in enumerate(rows, start=1):
        ts = None
        if has_so:
            so = conn.execute(
                "SELECT entry_triggered_at FROM signal_outcomes WHERE signal_id=? "
                "ORDER BY checked_at DESC, id DESC LIMIT 1", (sid,)).fetchone()
            if so and so[0]:
                ts = so[0]
        if not ts and has_ps:
            ps = conn.execute("SELECT created_at FROM proposed_signals WHERE signal_id=?", (sid,)).fetchone()
            if ps and ps[0]:
                ts = ps[0]
        cls = evidence_class_for(ts)
        if ts is not None and _parse_ts(ts) is not None:
            recovered += 1
        else:
            defaulted += 1
        conn.execute(
            f"UPDATE {_TABLE} SET evidence_class=?, frozen_at=? WHERE signal_id=? AND evidence_class IS NULL",
            (cls, FROZEN_AT, sid))
        if index % 50 == 0:
            conn.commit()
    return {"scanned": len(rows), "recovered_ts": recovered, "defaulted_backfill": defaulted}


def quarantine_mixed_execution_geometry(conn) -> int:
    """Remove proven mixed-geometry rows from authoritative Paper evidence.

    A mismatch between ``stop_initial`` used in the computed record and the
    stop captured in its immutable signal snapshot proves that at least two
    plans were combined. The raw row remains available for audit, but it must
    not contribute R/PF or be treated as a closed Paper trade.
    """
    ensure_table(conn)
    rows = conn.execute(
        f"SELECT signal_id,stop_initial,signal_snapshot_json FROM {_TABLE} "
        "WHERE signal_snapshot_json IS NOT NULL "
        "AND lifecycle_state IN ('OPEN','CLOSED')"
    ).fetchall()
    signal_ids = [
        str(row[0]) for row in rows
        if _stored_stop_disagrees_with_snapshot(row[1], row[2])
    ]
    for signal_id in signal_ids:
        conn.execute(
            f"UPDATE {_TABLE} SET lifecycle_state='INVALID',paper_execution_r=NULL,"
            "paper_execution_outcome='invalid_session',"
            "close_reason='invalid_signal_geometry_mutated_after_entry',"
            "close_event='invalid_session',exit_at=NULL,exit_at_source=NULL,"
            "execution_validity='invalid_signal_geometry_mutated_after_entry' "
            "WHERE signal_id=?",
            (signal_id,),
        )
    return len(signal_ids)


def backfill_all(
    conn,
    *,
    now_iso: str,
    risk_model: str = DEFAULT_RISK_MODEL,
    limit: int | None = None,
    expired_only: bool = False,
) -> dict[str, int]:
    """Recompute paper execution outcomes for ALL entered tracked signals (latest
    outcome row each). Idempotent upsert. READ-ONLY w.r.t. signal_outcomes.

    Also sweeps any remaining NULL evidence_class rows outside this query's own join scope (see
    backfill_evidence_class_only) so a full refresh always leaves zero NULL evidence_class rows.

    Returns {scanned, written, resolved, errors, null_evidence_recovered, null_evidence_defaulted}."""
    ensure_table(conn)
    if not expired_only:
        # Idempotent provenance migration for databases restored from a backup
        # that predates the split of the versioned crypto-swing profiles.
        repair_specific_crypto_swing_profiles(conn)
        conn.commit()
    ps_cols = {r[1] for r in conn.execute("PRAGMA table_info(proposed_signals)")}
    expires_expr = "p.expires_at" if "expires_at" in ps_cols else "NULL"
    raw_expr = "p.raw_idea_json" if "raw_idea_json" in ps_cols else "NULL"
    has_entry_mode_table = _has_table(conn, "signal_entry_mode")
    entry_mode_join = "LEFT JOIN signal_entry_mode sem ON sem.signal_id=p.signal_id" if has_entry_mode_table else ""
    entry_mode_expr = "sem.entry_mode" if has_entry_mode_table else "NULL"
    # New entries are synchronously inserted into paper_execution_outcomes by
    # the tracker. Repair any fail-open miss from the recent append-only tail,
    # then rotate existing OPEN/old rows from the 10k-row derived table. This
    # avoids probing all 8M+ lifecycle snapshots merely to discover which
    # signals have ever entered.
    missing_ids: list[str] = []
    if not expired_only:
        latest_outcome_id = int(conn.execute(
            "SELECT COALESCE(MAX(id),0) FROM signal_outcomes"
        ).fetchone()[0])
        recent_floor = max(0, latest_outcome_id - 50000)
        missing_ids = [str(row[0]) for row in conn.execute(
            f"SELECT DISTINCT so.signal_id FROM signal_outcomes so "
            f"LEFT JOIN {_TABLE} pe ON pe.signal_id=so.signal_id "
            "WHERE so.id>? AND so.entry_triggered=1 AND pe.signal_id IS NULL "
            "ORDER BY so.id DESC LIMIT 250",
            (recent_floor,),
        ).fetchall()]
    batch_limit = int(limit) if limit is not None and int(limit) > 0 else None
    remaining = None if batch_limit is None else max(0, batch_limit - len(missing_ids))
    existing_limit_sql = "" if remaining is None else " LIMIT ?"
    existing_params: list[Any] = [] if remaining is None else [remaining]
    select_fields = f"""
        p.signal_id, p.symbol, p.direction, p.mode, p.tier,
        p.asset_class, p.setup_type,
        p.created_at, p.suggested_entry, p.entry_trigger, p.entry_low,
        p.stop_loss, p.invalidation, p.tp1, p.tp2, p.tp3,
        {expires_expr} AS p_expires_at,
        {raw_expr} AS p_raw_idea_json,
        {entry_mode_expr} AS stored_entry_mode
    """
    candidates = []
    for sid in missing_ids[:batch_limit]:
        row = conn.execute(
            f"SELECT {select_fields} FROM proposed_signals p {entry_mode_join} "
            "WHERE p.signal_id=?",
            (sid,),
        ).fetchone()
        if row is not None:
            candidates.append(row)
    if expired_only:
        expired_limit_sql = "" if batch_limit is None else " LIMIT ?"
        expired_params: list[Any] = [now_iso]
        if batch_limit is not None:
            expired_params.append(batch_limit)
        candidates.extend(conn.execute(
            f"""
            SELECT {select_fields}
            FROM {_TABLE} existing
            JOIN proposed_signals p ON p.signal_id=existing.signal_id
            {entry_mode_join}
            WHERE existing.entry_at IS NOT NULL
              AND existing.effective_expires_at IS NOT NULL
              AND existing.effective_expires_at<=?
              AND (
                existing.lifecycle_state='OPEN'
                OR (existing.lifecycle_state='INVALID'
                    AND existing.close_reason='invalid_paper_profile_entry_mode_mismatch'
                    AND existing.path_remaining_fraction=0
                    AND existing.path_realized_r IS NOT NULL)
              )
            ORDER BY existing.effective_expires_at,existing.computed_at
            {expired_limit_sql}
            """,
            expired_params,
        ).fetchall())
    elif remaining is None or remaining > 0:
        candidates.extend(conn.execute(
            f"""
            SELECT {select_fields}
            FROM {_TABLE} existing
            JOIN proposed_signals p ON p.signal_id=existing.signal_id
            {entry_mode_join}
            ORDER BY CASE WHEN existing.lifecycle_state='OPEN' THEN 0 ELSE 1 END,
                     COALESCE(existing.computed_at,'') ASC,
                     p.created_at DESC
            {existing_limit_sql}
            """,
            existing_params,
        ).fetchall())
    rows: list[dict[str, Any]] = []
    signal_fields = (
        "symbol", "direction", "mode", "tier", "asset_class", "setup_type",
        "created_at", "suggested_entry", "entry_trigger", "entry_low",
        "stop_loss", "invalidation", "tp1", "tp2", "tp3",
    )
    for candidate in candidates:
        c = dict(candidate)
        sid = c["signal_id"]
        first = conn.execute(
            "SELECT entry_triggered_at,entry_price_used FROM signal_outcomes "
            "WHERE signal_id=? AND entry_triggered=1 ORDER BY id ASC LIMIT 1",
            (sid,),
        ).fetchone()
        terminal = conn.execute(
            "SELECT * FROM signal_outcomes WHERE signal_id=? AND entry_triggered=1 AND ("
            "status IN ('tp3_hit','stopped','expired','ambiguous') OR tp3_hit=1 OR stop_hit=1"
            ") ORDER BY id ASC LIMIT 1",
            (sid,),
        ).fetchone()
        chosen = terminal or conn.execute(
            "SELECT * FROM signal_outcomes WHERE signal_id=? AND entry_triggered=1 "
            "ORDER BY id DESC LIMIT 1",
            (sid,),
        ).fetchone()
        if chosen is None or first is None:
            continue
        combined = dict(chosen)
        combined["first_entry_at"] = first[0]
        combined["first_entry_price"] = first[1]
        for field in signal_fields:
            combined[field] = c.get(field)
        combined["expires_at"] = c.get("p_expires_at")
        combined["raw_idea_json"] = c.get("p_raw_idea_json")
        combined["stored_entry_mode"] = c.get("stored_entry_mode")
        rows.append(combined)
    scanned = written = resolved = errors = 0
    for row_index, r in enumerate(rows, start=1):
        scanned += 1
        d = dict(r)
        d["entry_triggered_at"] = d.get("first_entry_at") or d.get("entry_triggered_at")
        d["entry_price_used"] = d.get("first_entry_price") or d.get("entry_price_used")
        try:
            previous = conn.execute(
                f"SELECT * FROM {_TABLE} WHERE signal_id=?",
                (str(d.get("signal_id") or ""),),
            ).fetchone()
            previous_record = dict(previous) if previous is not None else None
            provenance = {}
            if previous_record and previous_record.get("entry_time_basis") is not None:
                provenance = {
                    "decision_at": (previous_record.get("decision_at")
                                    or previous_record.get("entry_at")),
                    "first_executable_price": (
                        previous_record.get("first_executable_price")
                        if previous_record.get("first_executable_price") is not None
                        else previous_record.get("entry_price_used")),
                    "entry_time_basis": previous_record.get("entry_time_basis"),
                    "current_price_revalidated": bool(
                        previous_record.get("current_price_revalidated")),
                }
            if (previous is not None
                    and str(previous_record.get("lifecycle_state") or "").upper()
                    in {"OPEN", "CLOSED"}
                    and previous_record.get("signal_snapshot_json")):
                d, _ = _apply_frozen_geometry(d, previous_record["signal_snapshot_json"])
                if _stored_stop_disagrees_with_snapshot(
                        previous_record.get("stop_initial"),
                        previous_record["signal_snapshot_json"]):
                    d["_execution_geometry_mutated_after_entry"] = True
            if previous_record:
                # The entry-time Paper provenance is authoritative. The generic
                # classifier stored in signal_entry_mode may disagree with a
                # post-classification Paper execution profile (for example a
                # stock swing event/RS entry executed as EVENT_RS_PULLBACK).
                for field in ("paper_entry_profile", "paper_execution_entry_mode"):
                    if previous_record.get(field) not in (None, ""):
                        d[field] = previous_record[field]
            execution_path = _stored_execution_path(previous_record or {})
            sid, key, rec = build_record_from_signal(
                d, d, risk_model, as_of_iso=now_iso,
                execution_path=execution_path, **provenance
            )
            upsert_outcome(conn, signal_id=sid, economic_trade_key=key,
                           computed_at=now_iso, record=rec, repair=True)
            written += 1
            if rec.get("paper_execution_r") is not None:
                resolved += 1
        except Exception:
            errors += 1
        if row_index % 50 == 0:
            conn.commit()
    quarantined = 0
    null_stats = {"recovered_ts": 0, "defaulted_backfill": 0}
    if not expired_only:
        quarantined = quarantine_mixed_execution_geometry(conn)
        null_stats = backfill_evidence_class_only(conn, now_iso=now_iso)
    return {"scanned": scanned, "written": written, "resolved": resolved, "errors": errors,
            "mixed_geometry_quarantined": quarantined,
            "null_evidence_recovered": null_stats["recovered_ts"],
            "null_evidence_defaulted": null_stats["defaulted_backfill"]}
