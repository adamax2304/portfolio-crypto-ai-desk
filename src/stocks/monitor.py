"""Stocks Intraday Monitor — minimal, safe alert plumbing.

Adds a continuous monitoring loop for stocks A/B-tier signals. The crypto
side already has ``WatchlistMonitor`` for the same job; this module is
the stocks-only equivalent that respects the existing safety rails:

* never modify scoring;
* never auto-trade;
* never auto-change thresholds;
* read-only with respect to scoring/strategy.

The monitor also owns the isolated MEXC stock-futures Paper lane. From
08:50 New York time it refreshes source ideas, forces a fresh decision pass
at 09:15 (15 minutes before the cash open), and then simulates orders from
public MEXC data. That lane has no private exchange access and cannot place
real orders.

Architecture
------------
1. ``MaterialImprovementChecker`` — decides whether a new state of a
   signal is materially better than its last sent alert. Implements the
   four rules in the spec: tier upgrade, score delta, entry zone change,
   invalidation change.
2. ``StocksMonitorSession.run_once`` — single tick: rebuild the full stock
   universe on a bounded slower cadence, refresh/track existing pending A/B
   intraday signals every minute, then dispatch new/materially-improved alerts.
3. ``StocksMonitorSession.run`` — wraps ``run_once`` in a time-bounded
   loop with optional market-hours gating.

Telegram safety:
* Failures in the Telegram client never crash the loop.
* Setup/improvement alerts are journal-only; the phone trade feed is reserved
  for live-routed entries/fills/closes plus critical health/watchdog notices.
* Dry-run mode short-circuits Telegram entirely and only writes
  ``signal_alerts`` rows with ``telegram_status='dry_run'``.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
import uuid
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.config import ProjectConfig
from src.storage.sqlite import SQLiteStore

_LOG = logging.getLogger("crypto_ai_desk.stocks_monitor")

# Material improvement defaults — overridable via constructor for tests.
DEFAULT_SCORE_IMPROVEMENT = 5.0
DEFAULT_ENTRY_CHANGE_PCT = 0.5  # 0.5 % of mid-entry counts as material
DEFAULT_INVALIDATION_CHANGE_PCT = 0.5
# PART 2 fix: 45-minute per-signal cooldown for "soft" alert types
# (entry_change / invalidation_change). The 12h cycle-2 monitor fired 78
# alerts in ~1h because the same 8–10 setups re-triggered entry_change on
# every 0.5% wobble. Cooldown suppresses those duplicates without
# blocking genuinely material events.
DEFAULT_COOLDOWN_MINUTES = 45.0
# These alert types are always material — they bypass the cooldown.
COOLDOWN_BYPASS_TYPES = frozenset({"new_signal", "tier_upgrade"})
LIQUIDITY_SHOCK_FAST_CADENCE_SECONDS = 15.0
LIQUIDITY_SHOCK_BAR_SETTLE_SECONDS = 5.0


def _aligned_fast_lane_delay() -> float:
    now = time.time()
    shifted = now - LIQUIDITY_SHOCK_BAR_SETTLE_SECONDS
    next_tick = (
        int(shifted // LIQUIDITY_SHOCK_FAST_CADENCE_SECONDS) + 1
    ) * LIQUIDITY_SHOCK_FAST_CADENCE_SECONDS + LIQUIDITY_SHOCK_BAR_SETTLE_SECONDS
    return max(0.05, next_tick - now)


def _write_liquidity_shock_heartbeat(root: Path, *, status: str,
                                     detail: dict[str, Any]) -> None:
    """Publish a quiet health/latency record for the one-minute Paper lane."""
    target = root / "data" / "runtime_locks" / "stocks_liquidity_shock_paper.heartbeat.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "at": datetime.now(timezone.utc).isoformat(),
        "pid": os.getpid(),
        "status": status,
        "detail": detail,
    }
    temporary = target.with_name(f"{target.name}.{os.getpid()}.{time.monotonic_ns()}.tmp")
    try:
        temporary.write_text(json.dumps(payload, sort_keys=True, default=str), encoding="utf-8")
        temporary.replace(target)
    except OSError:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


# ---------------------------------------------------------------------------
# Decision: send / skip / update
# ---------------------------------------------------------------------------


@dataclass
class AlertDecision:
    """Outcome of comparing a current signal against the last alert."""

    should_send: bool
    alert_type: str  # "new_signal" / "tier_upgrade" / "score_improvement" /
                    # "entry_change" / "invalidation_change" / "duplicate"
    reason: str


class MaterialImprovementChecker:
    """Pure-logic helper. No I/O. Easily unit-tested.

    The same instance can be reused across many comparisons; it holds no
    mutable state.
    """

    def __init__(
        self,
        *,
        score_threshold: float = DEFAULT_SCORE_IMPROVEMENT,
        entry_change_pct: float = DEFAULT_ENTRY_CHANGE_PCT,
        invalidation_change_pct: float = DEFAULT_INVALIDATION_CHANGE_PCT,
        cooldown_minutes: float = DEFAULT_COOLDOWN_MINUTES,
    ) -> None:
        self.score_threshold = float(score_threshold)
        self.entry_change_pct = float(entry_change_pct)
        self.invalidation_change_pct = float(invalidation_change_pct)
        self.cooldown_minutes = float(cooldown_minutes)

    def decide(
        self,
        *,
        current: dict[str, Any],
        last_alert: dict[str, Any] | None,
        now: datetime | None = None,
    ) -> AlertDecision:
        """Return whether the current signal warrants an alert.

        ``current`` is a row from ``proposed_signals`` (dict). ``last_alert``
        is the row returned by ``last_signal_alert_for_signal`` (or for the
        same setup key) — ``None`` means we've never alerted this signal.
        ``now`` (UTC) is injectable for tests; defaults to ``datetime.now(timezone.utc)``.

        PART 2 fix: after determining the *candidate* alert type, apply a
        per-signal cooldown to suppress ``entry_change`` /
        ``invalidation_change`` / ``score_improvement`` re-fires within
        ``self.cooldown_minutes``. ``new_signal`` and ``tier_upgrade``
        bypass the cooldown (they are always material).
        """

        candidate = self._classify(current=current, last_alert=last_alert)
        if not candidate.should_send:
            return candidate
        if candidate.alert_type in COOLDOWN_BYPASS_TYPES:
            return candidate
        if last_alert is None:
            return candidate
        cooldown_remaining = self._cooldown_remaining_minutes(last_alert, now=now)
        if cooldown_remaining > 0:
            return AlertDecision(
                False,
                "cooldown",
                (
                    f"{candidate.alert_type} suppressed — {cooldown_remaining:.1f} min "
                    f"of {self.cooldown_minutes:.0f}-min cooldown remaining "
                    f"(candidate reason: {candidate.reason})"
                ),
            )
        return candidate

    def _classify(
        self,
        *,
        current: dict[str, Any],
        last_alert: dict[str, Any] | None,
    ) -> AlertDecision:
        """Pure setup-comparison logic. No cooldown — that's applied by
        :meth:`decide`. Returns the *candidate* AlertDecision."""

        tier = str(current.get("tier") or "").strip().upper()
        if tier not in {"A", "B"}:
            return AlertDecision(False, "duplicate", f"tier={tier} not A/B")
        if current.get("invalidation") in (None, "", 0, 0.0):
            return AlertDecision(False, "duplicate", "missing invalidation")
        # PART 3 fix: block Telegram dispatch for stocks A/B with active
        # legal headline risk (indictment/SEC/DOJ/auditor/class action).
        # SMCI cycle-2 regression case. Tier remains A/B in the report —
        # only Telegram is suppressed.
        from src.stocks.legal_risk import signal_has_legal_block

        if signal_has_legal_block(current):
            return AlertDecision(
                False,
                "legal_block",
                "active legal headline risk — Telegram suppressed; verify report",
            )

        if last_alert is None:
            return AlertDecision(True, "new_signal", "no prior alert for this signal")

        prev_tier = str(last_alert.get("tier") or "").strip().upper()
        if _tier_rank(tier) > _tier_rank(prev_tier):
            return AlertDecision(
                True,
                "tier_upgrade",
                f"tier upgraded {prev_tier}→{tier}",
            )

        # Score improvement.
        cur_score = _as_float(current.get("score"))
        prev_score = _as_float(last_alert.get("score"))
        if cur_score is not None and prev_score is not None:
            if cur_score - prev_score >= self.score_threshold:
                return AlertDecision(
                    True,
                    "score_improvement",
                    f"score +{cur_score - prev_score:.2f} (>= {self.score_threshold})",
                )

        # Entry zone change vs prior alert payload.
        prev_payload = _safe_payload(last_alert)
        cur_entry_mid = _entry_mid(current)
        prev_entry_mid = _entry_mid(prev_payload.get("entry") or {}) or _entry_mid(
            prev_payload
        )
        if cur_entry_mid and prev_entry_mid:
            denom = max(abs(prev_entry_mid), 1e-9)
            pct = abs(cur_entry_mid - prev_entry_mid) / denom * 100.0
            if pct >= self.entry_change_pct:
                return AlertDecision(
                    True,
                    "entry_change",
                    f"entry mid moved {pct:.2f}% (>= {self.entry_change_pct}%)",
                )

        # Invalidation change.
        cur_inv = _as_float(current.get("invalidation"))
        prev_inv = _as_float(
            prev_payload.get("invalidation")
            or (prev_payload.get("entry") or {}).get("invalidation")
        )
        if cur_inv and prev_inv:
            denom = max(abs(prev_inv), 1e-9)
            pct = abs(cur_inv - prev_inv) / denom * 100.0
            if pct >= self.invalidation_change_pct:
                return AlertDecision(
                    True,
                    "invalidation_change",
                    f"invalidation moved {pct:.2f}% (>= {self.invalidation_change_pct}%)",
                )

        return AlertDecision(
            False,
            "duplicate",
            "no tier upgrade, score < threshold, entry/inv unchanged",
        )

    def _cooldown_remaining_minutes(
        self,
        last_alert: dict[str, Any],
        *,
        now: datetime | None = None,
    ) -> float:
        """Minutes left on the cooldown window. ``0`` means cooldown
        has elapsed (or could not be determined — fail-open to alert)."""

        sent_at_raw = last_alert.get("sent_at")
        if not sent_at_raw:
            return 0.0
        try:
            sent_at = datetime.fromisoformat(str(sent_at_raw).replace("Z", "+00:00"))
        except Exception:
            return 0.0
        if sent_at.tzinfo is None:
            sent_at = sent_at.replace(tzinfo=timezone.utc)
        moment = now or datetime.now(timezone.utc)
        if moment.tzinfo is None:
            moment = moment.replace(tzinfo=timezone.utc)
        elapsed_min = (moment - sent_at).total_seconds() / 60.0
        remaining = self.cooldown_minutes - elapsed_min
        return max(0.0, remaining)


# ---------------------------------------------------------------------------
# Alert formatter — Telegram-friendly Markdown
# ---------------------------------------------------------------------------


def format_stocks_alert(
    *,
    signal: dict[str, Any],
    decision: AlertDecision,
    context: dict[str, Any] | None = None,
) -> str:
    """Render the Telegram message for a stocks A/B setup alert.

    2026-06-14: standardized to use the shared SETUP — WAITING FOR ENTRY
    template (`src/notifiers/setup_alert.py`). Sub-type is reflected in the
    header (NEW SIGNAL / ENTRY CHANGE / SCORE IMPROVEMENT / TIER UPGRADE /
    INVALIDATION CHANGE). Plain text — `parse_mode=""`.
    """
    from src.notifiers.setup_alert import render_setup_alert

    # Carry the `signal_id` through so the visible body includes it.
    enriched = dict(signal)
    enriched.setdefault("asset_class", "stocks")
    enriched.setdefault("mode", "intraday")
    return render_setup_alert(enriched, stocks_subtype=decision.alert_type)


def message_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Monitor session
# ---------------------------------------------------------------------------


@dataclass
class MonitorTickResult:
    started_at: str
    finished_at: str
    a_b_active: int = 0
    new_alerts: int = 0
    upgrade_alerts: int = 0
    skipped_duplicate: int = 0
    skipped_no_invalidation: int = 0
    skipped_cooldown: int = 0  # PART 2: 45-min per-signal cooldown suppressions
    skipped_legal_block: int = 0  # PART 3: active legal headline risk
    telegram_failed: int = 0
    report_refreshed: bool = False
    pending_symbols_refreshed: int = 0
    pending_refresh_failed: int = 0
    pending_checked: int = 0
    pending_tp: int = 0
    pending_stop: int = 0
    rth_plans_checked: int = 0
    rth_plans_ready: int = 0
    rth_plans_rejected: int = 0
    mexc_stock_paper_evaluated: int = 0
    mexc_stock_paper_staged: int = 0
    mexc_stock_paper_rejected: int = 0
    mexc_stock_paper_filled: int = 0
    mexc_stock_paper_closed: int = 0
    mexc_stock_paper_failed: int = 0
    liquidity_shock_setups: int = 0
    liquidity_shock_rows: int = 0
    liquidity_shock_failed: int = 0
    decisions: list[dict[str, Any]] = field(default_factory=list)


class StocksMonitorSession:
    """Time-bounded stocks A/B alert orchestrator.

    Parameters
    ----------
    config: :class:`ProjectConfig`
        Project configuration (provides DB path + root).
    minutes / interval_minutes:
        Total session length and inter-tick wait. ``minutes <= 0`` runs a
        single tick.
    market_hours_only:
        When True, ticks that fall outside US equity regular hours
        (13:30–20:00 UTC, Mon-Fri) are skipped. The session still wakes
        and counts towards ``minutes``.
    send_telegram:
        When False, alerts are recorded in ``signal_alerts`` with
        ``telegram_status='dry_run'`` and no network call is made.
    dry_run:
        Convenience flag: ``True`` implies ``send_telegram=False`` *and*
        skips the costly ``stocks-intraday-report`` re-run inside each
        tick. Useful for tests and smoke checks.
    """

    def __init__(
        self,
        config: ProjectConfig,
        *,
        minutes: int = 60,
        interval_minutes: int = 10,
        market_hours_only: bool = True,
        send_telegram: bool = True,
        dry_run: bool = False,
        score_improvement: float = DEFAULT_SCORE_IMPROVEMENT,
        cooldown_minutes: float = DEFAULT_COOLDOWN_MINUTES,
        report_refresh_minutes: int = 10,
        max_pending_symbols: int = 40,
        background_report_refresh: bool = True,
    ) -> None:
        self.config = config
        self.minutes = int(minutes)
        self.interval_minutes = max(1, int(interval_minutes))
        self.market_hours_only = bool(market_hours_only)
        self.send_telegram = bool(send_telegram) and not bool(dry_run)
        self.dry_run = bool(dry_run)
        self.report_refresh_minutes = max(1, int(report_refresh_minutes))
        self.max_pending_symbols = max(1, int(max_pending_symbols))
        self.background_report_refresh = bool(background_report_refresh)
        self._last_report_refresh_mono: float | None = None
        self._report_executor: ThreadPoolExecutor | None = None
        self._report_future: Future[Any] | None = None
        self._shadow_executor: ThreadPoolExecutor | None = None
        self._shadow_future: Future[Any] | None = None
        # Tests that request a synchronous report retain synchronous Shadow
        # behaviour. The production monitor keeps research off the entry path.
        self.background_shadow_refresh = bool(background_report_refresh)
        self._last_profile_refresh_summary: dict[str, dict[str, Any]] = {}
        self._preopen_decision_refresh_session: str | None = None
        self.checker = MaterialImprovementChecker(
            score_threshold=score_improvement,
            cooldown_minutes=cooldown_minutes,
        )
        self.db = SQLiteStore(config.db_path)
        self.db.init_db()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self) -> list[MonitorTickResult]:
        """Run the monitor for ``minutes`` minutes. Returns each tick's
        result so the CLI can print a compact summary."""
        # The stock execution lane has one writer/observer. A second session
        # cannot make entries faster; it only competes for SQLite and can
        # observe the same touch twice. Reuse the proven pending-monitor lease
        # implementation, but keep a distinct stocks lease.
        from src.signals.pending_monitor import leader_lock, leader_status

        ttl = max(180.0, float(self.interval_minutes * 60 * 5))
        worker_id = f"stocks-monitor-{os.getpid()}"
        with leader_lock(self.config.root, "stocks", worker_id=worker_id, ttl_sec=ttl) as heartbeat:
            if heartbeat is None:
                state = leader_status(self.config.root, "stocks", ttl_sec=ttl)
                result = MonitorTickResult(
                    started_at=datetime.now(timezone.utc).isoformat(),
                    finished_at=datetime.now(timezone.utc).isoformat(),
                )
                result.decisions.append({"action": "skip_session", "reason": "leader_active", "leader": state})
                _LOG.warning("stocks monitor standby: another leader is active (%s)", state.get("holder"))
                return [result]
            deadline = time.monotonic() + max(0, self.minutes) * 60
            results: list[MonitorTickResult] = []
            ticks = 0
            while True:
                heartbeat()
                ticks += 1
                tick = self.run_once()
                results.append(tick)
                if self.minutes <= 0:
                    break
                next_full_tick = min(
                    deadline, time.monotonic() + self.interval_minutes * 60,
                )
                # The full monitor remains one-minute. Liquidity-shock Paper
                # confirmation gets an isolated 15-second lane so a newly
                # closed 1m/15m bar does not wait for the next full report tick.
                while time.monotonic() < next_full_tick:
                    sleep_for = min(
                        _aligned_fast_lane_delay(),
                        max(0.0, next_full_tick - time.monotonic()),
                    )
                    if sleep_for > 0:
                        time.sleep(sleep_for)
                    if time.monotonic() >= next_full_tick:
                        break
                    heartbeat()
                    fast_now = datetime.now(timezone.utc)
                    if not self.dry_run and _is_us_market_hours(fast_now):
                        fast_result = MonitorTickResult(
                            started_at=fast_now.isoformat(),
                            finished_at=fast_now.isoformat(),
                        )
                        self._run_liquidity_shock_paper(fast_result, fast_now)
                if time.monotonic() >= deadline:
                    break
            _LOG.info("stocks monitor session finished after %d tick(s)", ticks)
            return results

    def run_once(self) -> MonitorTickResult:
        """Single monitoring tick. Never raises; failures are captured in
        the returned ``MonitorTickResult`` log."""
        now = datetime.now(timezone.utc)
        result = MonitorTickResult(
            started_at=now.isoformat(),
            finished_at=now.isoformat(),
        )

        market_open = _is_us_market_hours(now)
        mexc_paper = None
        mexc_paper_cfg: dict[str, Any] = {}
        mexc_paper_window = False
        if not self.dry_run:
            try:
                from src.stocks import mexc_stock_futures_paper as mexc_paper

                mexc_paper_cfg = mexc_paper.load_cfg()
                mexc_paper_window = bool(
                    mexc_paper_cfg.get("enabled")
                    and mexc_paper.in_refresh_window(now, mexc_paper_cfg)
                )
            except Exception as exc:  # noqa: BLE001
                result.mexc_stock_paper_failed += 1
                result.decisions.append(
                    {"action": "mexc_stock_paper_init_failed", "error": str(exc)}
                )

        if self.market_hours_only and not market_open and not mexc_paper_window:
            result.finished_at = datetime.now(timezone.utc).isoformat()
            result.decisions.append(
                {"action": "skip_tick", "reason": "outside US market hours"}
            )
            return result

        notifier = self._notifier_or_none() if self.send_telegram else None
        self._collect_report_refresh(result, now)
        self._collect_forward_shadow_refresh(result)

        # The source signal is deliberately recomputed before the cash open.
        # Review/actionability refresh starts at 08:50 ET. The immutable price
        # decision begins at 09:15, leaving the LLM's real review budget.
        if (
            self.market_hours_only
            and mexc_paper_window
            and not market_open
            and mexc_paper is not None
        ):
            force_preopen = self._preopen_decision_refresh_due(now, mexc_paper_cfg)
            local = now.astimezone(mexc_paper.NY)
            refresh_hour, refresh_minute = str(
                mexc_paper_cfg.get("preopen_refresh_start_et") or "08:50"
            ).split(":", 1)
            end_hour, end_minute = str(
                mexc_paper_cfg.get("preopen_decision_end_et") or "09:30"
            ).split(":", 1)
            local_minute = local.hour * 60 + local.minute
            is_preopen = (
                int(refresh_hour) * 60 + int(refresh_minute)
                <= local_minute
                < int(end_hour) * 60 + int(end_minute)
            )
            # The structured review runs out-of-band.  Materialize any verdict
            # already ingested before the slow report work so the one-minute
            # Paper lane can immediately consume the same-plan permission.
            if is_preopen:
                self._refresh_preopen_actionability(result, now)
            if is_preopen and (force_preopen or self._report_refresh_due()):
                if force_preopen:
                    self._preopen_decision_refresh_session = (
                        now.astimezone(mexc_paper.NY).date().isoformat()
                    )
                self._last_report_refresh_mono = time.monotonic()
                try:
                    refresh_state = self._start_report_refresh(refresh_earnings=True)
                    if refresh_state == "completed":
                        result.report_refreshed = True
                        self._after_report_refresh(result, now)
                    else:
                        result.decisions.append(
                            {"action": "preopen_report_refresh_started"})
                except Exception as exc:  # noqa: BLE001
                    _LOG.warning("stocks preopen report refresh failed: %s", exc)
                    result.decisions.append(
                        {"action": "preopen_report_refresh_failed", "error": str(exc)}
                    )
            self._run_mexc_stock_paper(
                module=mexc_paper,
                cfg=mexc_paper_cfg,
                now=now,
                notifier=notifier,
                result=result,
            )
            result.finished_at = datetime.now(timezone.utc).isoformat()
            return result

        # 1. Service existing pending entries first. The full stock report can spend minutes in
        # provider/agent work, so it must never sit in front of the one-minute execution lane.
        if not self.dry_run:
            try:
                pending_ids = self._pending_signal_ids()
                refresh = self._refresh_pending_ohlcv(pending_ids)
                result.pending_symbols_refreshed = int(refresh.get("fetched", 0))
                result.pending_refresh_failed = int(refresh.get("failed", 0))
            except Exception as exc:  # noqa: BLE001
                _LOG.warning("stocks pending OHLCV refresh failed: %s", exc)
                result.pending_refresh_failed += 1
                result.decisions.append(
                    {"action": "pending_refresh_failed", "error": str(exc)}
                )

            # Same idempotent tracker and notifier used by the full signal tracker. This scopes
            # strictly to stocks/intraday and preserves every freshness/actionability/guard check.
            try:
                tracked = self._track_pending_entries(notifier, pending_ids)
                result.pending_checked = tracked.checked
                result.pending_tp = tracked.tp_hits
                result.pending_stop = tracked.stopped
                # Append lifecycle diagnostics without mutating the signal or
                # Paper ledger. This makes the daily funnel report explain
                # whether a candidate was observed, expired, or resolved.
                try:
                    from src.stocks.paper_funnel import record_event_for_db

                    for detail in tracked.details:
                        previous = str(detail.get("previous_status") or "")
                        current = str(detail.get("new_status") or "")
                        if previous != current:
                            record_event_for_db(
                                self.config.db_path,
                                signal_id=str(detail.get("signal_id") or ""),
                                stage="TRACKER_STATUS",
                                reason=current,
                                payload={"previous_status": previous,
                                         "final_outcome": detail.get("final_outcome")},
                                now=now,
                            )
                except Exception:
                    pass
            except Exception as exc:  # noqa: BLE001
                _LOG.warning("stocks pending tracker failed: %s", exc)
                result.decisions.append(
                    {"action": "pending_tracker_failed", "error": str(exc)}
                )

            # Independent Paper-only mean-reversion research. It consumes the
            # already refreshed stock caches, writes only its own outcome
            # tables and has no route into the generic signal/live pipeline.
            self._run_liquidity_shock_paper(result, now)

            # Discover new setups on a slower cadence only after existing pending entries have
            # been serviced. New candidates join the execution lane on the next one-minute tick.
            if self._report_refresh_due():
                # Mark the attempt before network I/O. A failed provider must not be hammered every
                # minute; the pending lane keeps running fail-conservatively until the retry.
                self._last_report_refresh_mono = time.monotonic()
                try:
                    refresh_state = self._start_report_refresh()
                    result.report_refreshed = refresh_state == "completed"
                except Exception as exc:  # noqa: BLE001
                    _LOG.warning("stocks report refresh failed: %s", exc)
                    result.decisions.append(
                        {"action": "report_refresh_failed", "error": str(exc)}
                    )

                if result.report_refreshed:
                    # The report has just rebuilt all levels and SI-1..SI-5
                    # gates from current RTH data. Link recent outside-session
                    # plans to that fresh candidate for auditability only;
                    # this never promotes or executes the old plan.
                    try:
                        from src.stocks import rth_revalidation

                        revalidation = rth_revalidation.refresh(
                            db=str(self.config.db_path), now=now)
                        result.rth_plans_checked = int(revalidation.get("plans", 0))
                        result.rth_plans_ready = int(revalidation.get("ready", 0))
                        result.rth_plans_rejected = int(revalidation.get("rejected", 0))
                        result.decisions.append({
                            "action": "rth_revalidation",
                            "status": revalidation.get("status"),
                            "plans": result.rth_plans_checked,
                            "ready": result.rth_plans_ready,
                            "rejected": result.rth_plans_rejected,
                        })
                    except Exception as exc:  # noqa: BLE001 - audit bridge must not interrupt Paper
                        _LOG.warning("stocks RTH revalidation failed: %s", exc)
                        result.decisions.append(
                            {"action": "rth_revalidation_failed", "error": str(exc)})

                    self._start_forward_shadow_refresh(result)

        if self.market_hours_only and mexc_paper_window and mexc_paper is not None:
            self._run_mexc_stock_paper(
                module=mexc_paper,
                cfg=mexc_paper_cfg,
                now=now,
                notifier=notifier,
                result=result,
            )

        # 2. Walk active A/B stocks signals and dispatch alerts.
        try:
            active = self._load_active_ab()
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("could not load active A/B stocks signals: %s", exc)
            active = []
        result.a_b_active = len(active)

        for sig in active:
            last_alert = None
            sig_id = sig.get("signal_id")
            if sig_id:
                try:
                    last_alert = self.db.last_signal_alert_for_signal(sig_id)
                except Exception as exc:  # noqa: BLE001
                    _LOG.warning("last_signal_alert lookup failed: %s", exc)
            if last_alert is None:
                # Fall back to a setup-level lookup so reissues of "the
                # same idea with a new signal_id" still de-dupe.
                try:
                    last_alert = self.db.last_signal_alert_for_setup(
                        asset_class="stocks",
                        symbol=str(sig.get("symbol", "")),
                        mode=str(sig.get("mode", "")),
                        direction=str(sig.get("direction", "")),
                    )
                except Exception as exc:  # noqa: BLE001
                    _LOG.warning("setup-level alert lookup failed: %s", exc)
                    last_alert = None

            decision = self.checker.decide(current=sig, last_alert=last_alert)
            if not decision.should_send:
                if decision.alert_type == "cooldown":
                    result.skipped_cooldown += 1
                elif decision.alert_type == "legal_block":
                    result.skipped_legal_block += 1
                elif "missing invalidation" in decision.reason:
                    result.skipped_no_invalidation += 1
                else:
                    result.skipped_duplicate += 1
                result.decisions.append({
                    "symbol": sig.get("symbol"),
                    "tier": sig.get("tier"),
                    "action": "skip",
                    "reason": decision.reason,
                    "alert_type": decision.alert_type,
                })
                continue

            text = format_stocks_alert(
                signal=sig,
                decision=decision,
                context=self._extra_context_for(sig),
            )
            telegram_status = (
                "dry_run" if not self.send_telegram else "setup_suppressed_live_only"
            )

            try:
                self.db.record_signal_alert(
                    alert_id=str(uuid.uuid4()),
                    signal_id=str(sig_id or f"unknown_{sig.get('symbol')}"),
                    asset_class="stocks",
                    symbol=str(sig.get("symbol", "")),
                    mode=str(sig.get("mode") or "intraday"),
                    tier=str(sig.get("tier", "")),
                    score=_as_float(sig.get("score")),
                    direction=str(sig.get("direction", "")),
                    sent_at=datetime.now(timezone.utc).isoformat(),
                    alert_type=decision.alert_type,
                    telegram_status=telegram_status,
                    message_hash=message_hash(text),
                    payload={
                        "entry_low": sig.get("entry_low"),
                        "entry_high": sig.get("entry_high"),
                        "invalidation": sig.get("invalidation"),
                        "tp1": sig.get("tp1"),
                        "tp2": sig.get("tp2"),
                        "telegram_channel": "journal_only",
                    },
                )
            except Exception as exc:  # noqa: BLE001
                _LOG.warning("could not record signal_alert row: %s", exc)

            if decision.alert_type in {"tier_upgrade", "score_improvement",
                                       "entry_change", "invalidation_change"}:
                result.upgrade_alerts += 1
            else:
                result.new_alerts += 1
            result.decisions.append({
                "symbol": sig.get("symbol"),
                "tier": sig.get("tier"),
                "action": "alert",
                "alert_type": decision.alert_type,
                "telegram_status": telegram_status,
                "reason": decision.reason,
            })

        result.finished_at = datetime.now(timezone.utc).isoformat()
        return result

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _run_liquidity_shock_paper(
        self, result: MonitorTickResult, now: datetime
    ) -> None:
        started = time.monotonic()
        try:
            from src.execution import stocks_liquidity_shock_reclaim_paper

            summary = stocks_liquidity_shock_reclaim_paper.tick(
                db=str(self.config.db_path), now=now, persist=True,
                refresh_candidates=True,
            )
            result.liquidity_shock_setups = int(summary.get("setups", 0))
            result.liquidity_shock_rows = len(summary.get("rows") or [])
            elapsed = round(time.monotonic() - started, 3)
            open_tracking = summary.get("open_tracking") or {}
            tracking_stale = int(open_tracking.get("stale", 0))
            open_refresh = summary.get("open_position_refresh") or {}
            degraded = (
                elapsed > LIQUIDITY_SHOCK_FAST_CADENCE_SECONDS
                or tracking_stale > 0
                or open_refresh.get("status") == "unavailable"
            )
            _write_liquidity_shock_heartbeat(
                Path(self.config.root),
                status="DEGRADED" if degraded else "OK",
                detail={
                    "elapsed_seconds": elapsed,
                    "setups": result.liquidity_shock_setups,
                    "rows": result.liquidity_shock_rows,
                    "closed_matured": summary.get("closed_matured", 0),
                    "open_tracking": open_tracking,
                    "open_position_refresh": open_refresh,
                    "base_refresh": summary.get("base_refresh"),
                    "candidate_refresh": summary.get("candidate_refresh"),
                },
            )
            # Keep the ordinary one-minute monitor log quiet when there was
            # no event. This also preserves the established ordering of
            # user-facing signal diagnostics.
            if result.liquidity_shock_setups or result.liquidity_shock_rows or tracking_stale:
                result.decisions.append({
                    "action": "stocks_liquidity_shock_paper",
                    "status": "degraded" if degraded else "ok",
                    "paper_only": True,
                    "setups": result.liquidity_shock_setups,
                    "rows": result.liquidity_shock_rows,
                    "closed_matured": summary.get("closed_matured", 0),
                    "open_tracking": open_tracking,
                    "candidate_refresh": summary.get("candidate_refresh"),
                })
        except Exception as exc:  # noqa: BLE001 - research cannot stop the entry lane
            result.liquidity_shock_failed += 1
            _write_liquidity_shock_heartbeat(
                Path(self.config.root), status="ERROR", detail={
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                    "error": f"{type(exc).__name__}: {exc}",
                },
            )
            _LOG.warning("stocks liquidity-shock Paper tick failed: %s", exc)
            result.decisions.append({
                "action": "stocks_liquidity_shock_paper_failed",
                "error": f"{type(exc).__name__}: {exc}",
            })

    def _refresh_report(
        self,
        *,
        refresh_earnings: bool = False,
    ) -> dict[str, dict[str, Any]]:
        """Re-run the intraday pipeline and register versioned Paper lanes.

        BREAKOUT and PULLBACK consume the already-computed result. This keeps
        their discovery cadence aligned with the fast monitor without doing
        two additional universe downloads and scoring passes.
        """
        from src.execution import stocks_intraday_breakout_1bar_paper
        from src.execution import stocks_catalyst_rs_paper
        from src.execution import stocks_intraday_pullback_paper
        from src.stocks.pipelines.stocks_pipeline import StocksPipeline

        summary: dict[str, dict[str, Any]] = {}

        def _capture(name: str, callback: Any) -> None:
            try:
                summary[name] = callback()
            except Exception as exc:  # noqa: BLE001
                _LOG.warning("stocks %s profile refresh failed: %s", name, exc)
                summary[name] = {
                    "status": "failed", "registered": 0,
                    "error": f"{type(exc).__name__}: {exc}",
                }

        def _register_profiles(pipeline: Any, result: Any) -> None:
            _capture(
                "breakout_1bar",
                lambda: stocks_intraday_breakout_1bar_paper.register_result(
                    pipeline=pipeline,
                    result=result,
                    now=datetime.now(timezone.utc),
                ),
            )
            _capture(
                "pullback_vwap",
                lambda: stocks_intraday_pullback_paper.register_result(
                    pipeline=pipeline,
                    result=result,
                    now=datetime.now(timezone.utc),
                ),
            )
            _capture(
                # Catalyst RS confirmations expire after 30 minutes. The old
                # two-hour scheduler cadence guaranteed that most valid rows
                # were stale before the Paper adapter saw them.
                "catalyst_rs",
                lambda: stocks_catalyst_rs_paper.refresh(
                    db=str(self.config.db_path),
                    now=datetime.now(timezone.utc),
                    refresh_shadow=True,
                ),
            )
            self._last_profile_refresh_summary = summary

        pipeline = StocksPipeline(self.config)
        pipeline.run_report(
            mode="intraday",
            on_decision=_register_profiles,
            fast_data_update=True,
            refresh_earnings=refresh_earnings,
            # The shared source scan feeds several independently measured
            # Paper profiles. Their rolling guards run in register_result(),
            # after the profile is known, never as one mixed pre-filter here.
            apply_intraday_guards=False,
            # The monitor owns versioned profile registration in the callback.
            # Do not also create an unprofiled, unguarded generic Paper lane.
            shadow_only=True,
        )
        self._last_profile_refresh_summary = summary
        return summary

    def _start_report_refresh(self, *, refresh_earnings: bool = False) -> str:
        """Start at most one slow universe rebuild without blocking entries."""
        if self._report_future is not None and not self._report_future.done():
            return "running"
        self._last_profile_refresh_summary = {}
        if not self.background_report_refresh:
            if refresh_earnings:
                self._refresh_report(refresh_earnings=True)
            else:
                self._refresh_report()
            return "completed"
        if self._report_executor is None:
            self._report_executor = ThreadPoolExecutor(
                max_workers=1, thread_name_prefix="stocks-report")
        if refresh_earnings:
            self._report_future = self._report_executor.submit(
                self._refresh_report,
                refresh_earnings=True,
            )
        else:
            self._report_future = self._report_executor.submit(self._refresh_report)
        return "started"

    def _collect_report_refresh(
        self, result: MonitorTickResult, now: datetime
    ) -> None:
        future = self._report_future
        if future is None or not future.done():
            return
        self._report_future = None
        try:
            summary = future.result()
            if isinstance(summary, dict):
                self._last_profile_refresh_summary = summary
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("stocks background report refresh failed: %s", exc)
            result.decisions.append(
                {"action": "report_refresh_failed", "error": str(exc)})
            return
        result.report_refreshed = True
        self._after_report_refresh(result, now)

    def _start_forward_shadow_refresh(self, result: MonitorTickResult) -> None:
        """Keep Shadow accounting off the one-minute Paper execution lane.

        The forward evaluator can scan a sizeable historical window.  It is
        useful evidence, but it must never delay a pending Paper entry or its
        quote refresh.  Synchronous monitor instances are retained for the
        deterministic unit-test/single-run contract.
        """
        if not self.background_shadow_refresh:
            try:
                self._refresh_forward_shadow()
            except Exception as exc:  # noqa: BLE001
                _LOG.warning("stocks forward Shadow refresh failed: %s", exc)
                result.decisions.append(
                    {"action": "forward_shadow_refresh_failed", "error": str(exc)}
                )
            else:
                result.decisions.append(
                    {"action": "forward_shadow_refresh", "status": "completed"}
                )
            return

        if self._shadow_future is not None:
            if not self._shadow_future.done():
                result.decisions.append(
                    {"action": "forward_shadow_refresh", "status": "running"}
                )
                return
            # The result is normally collected at the beginning of the next
            # tick.  Clear a completed future here too so a rare report
            # completion in the same tick cannot suppress the next refresh.
            self._collect_forward_shadow_refresh(result)

        if self._shadow_executor is None:
            self._shadow_executor = ThreadPoolExecutor(
                max_workers=1,
                thread_name_prefix="stocks-shadow",
            )
        self._shadow_future = self._shadow_executor.submit(
            self._refresh_forward_shadow
        )
        result.decisions.append(
            {"action": "forward_shadow_refresh", "status": "started"}
        )

    def _collect_forward_shadow_refresh(self, result: MonitorTickResult) -> None:
        """Record a completed asynchronous Shadow refresh without blocking."""
        future = self._shadow_future
        if future is None or not future.done():
            return
        self._shadow_future = None
        try:
            future.result()
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("stocks forward Shadow refresh failed: %s", exc)
            result.decisions.append(
                {"action": "forward_shadow_refresh_failed", "error": str(exc)}
            )
        else:
            result.decisions.append(
                {"action": "forward_shadow_refresh", "status": "completed"}
            )

    def _after_report_refresh(
        self, result: MonitorTickResult, now: datetime
    ) -> None:
        """Refresh dependent read models after the slow report completes."""
        if self._last_profile_refresh_summary:
            result.decisions.append({
                "action": "versioned_paper_profiles_refresh",
                "profiles": self._last_profile_refresh_summary,
            })
        self._refresh_preopen_actionability(result, now)
        try:
            from src.stocks import rth_revalidation

            revalidation = rth_revalidation.refresh(
                db=str(self.config.db_path), now=now)
            result.rth_plans_checked = int(revalidation.get("plans", 0))
            result.rth_plans_ready = int(revalidation.get("ready", 0))
            result.rth_plans_rejected = int(revalidation.get("rejected", 0))
            result.decisions.append({
                "action": "rth_revalidation",
                "status": revalidation.get("status"),
                "plans": result.rth_plans_checked,
                "ready": result.rth_plans_ready,
                "rejected": result.rth_plans_rejected,
            })
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("stocks RTH revalidation failed: %s", exc)
            result.decisions.append(
                {"action": "rth_revalidation_failed", "error": str(exc)})
        self._start_forward_shadow_refresh(result)

    def _refresh_preopen_actionability(
        self,
        result: MonitorTickResult,
        now: datetime,
    ) -> None:
        """Materialize reviewed plans and repair only proven expiry defects."""
        try:
            from src.execution.stocks_preus_review import refresh_actionability
            from src.stocks.preopen_lifecycle import repair_bug_expired_actionable_plans

            actionability = refresh_actionability(
                db=self.config.db_path,
                now=now,
            )
            repaired = repair_bug_expired_actionable_plans(
                db=self.config.db_path,
                now=now,
            )
            result.decisions.append({
                "action": "preopen_actionability",
                "evaluated": int(actionability.get("evaluated", 0)),
                "actionable": int(actionability.get("actionable", 0)),
                "blocked": int(actionability.get("blocked", 0)),
                "reactivated": int(repaired.get("reactivated", 0)),
            })
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("stocks pre-open actionability refresh failed: %s", exc)
            result.decisions.append({
                "action": "preopen_actionability_failed",
                "error": str(exc),
            })

    def _report_refresh_due(self, *, now_mono: float | None = None) -> bool:
        if self._last_report_refresh_mono is None:
            return True
        moment = time.monotonic() if now_mono is None else float(now_mono)
        return (moment - self._last_report_refresh_mono) >= self.report_refresh_minutes * 60

    def _preopen_decision_refresh_due(
        self,
        now: datetime,
        cfg: dict[str, Any],
    ) -> bool:
        """Force exactly one source-idea rebuild from the configured ET boundary."""
        from zoneinfo import ZoneInfo

        local = now.astimezone(ZoneInfo("America/New_York"))
        session = local.date().isoformat()
        if self._preopen_decision_refresh_session == session:
            return False
        hour, minute = str(cfg.get("preopen_decision_start_et") or "09:10").split(":", 1)
        boundary = int(hour) * 60 + int(minute)
        end_hour, end_minute = str(
            cfg.get("preopen_decision_end_et") or "09:30"
        ).split(":", 1)
        end = int(end_hour) * 60 + int(end_minute)
        minute_of_day = local.hour * 60 + local.minute
        return boundary <= minute_of_day < end

    def _run_mexc_stock_paper(
        self,
        *,
        module: Any,
        cfg: dict[str, Any],
        now: datetime,
        notifier: Any,
        result: MonitorTickResult,
    ) -> None:
        """Run the public-data-only stock-futures Paper lane for one minute."""
        try:
            outcome = module.tick(db=self.config.db_path, now=now, cfg=cfg)
            stage = outcome.get("stage") or {}
            active = outcome.get("active") or {}
            health = outcome.get("health") or {}
            result.mexc_stock_paper_evaluated += int(stage.get("evaluated", 0))
            result.mexc_stock_paper_staged += int(stage.get("staged", 0))
            result.mexc_stock_paper_rejected += int(stage.get("rejected", 0))
            result.mexc_stock_paper_filled += int(active.get("filled", 0))
            result.mexc_stock_paper_closed += int(active.get("closed", 0))
            result.decisions.append({
                "action": "mexc_stock_futures_paper",
                "stage_status": stage.get("status"),
                "evaluated": stage.get("evaluated", 0),
                "staged": stage.get("staged", 0),
                "rejected": stage.get("rejected", 0),
                "filled": active.get("filled", 0),
                "closed": active.get("closed", 0),
                "quote_health": health.get("status"),
            })
            # The LLM routine is intentionally out-of-band, but this minute
            # monitor owns the operational hand-off. By the configured review
            # deadline it must be
            # able to prove that every current eligible pre-US plan has an
            # ingested structured verdict, or alert once while there is still
            # time to intervene before the Paper decision boundary.
            try:
                from src.execution import stocks_preus_review as preus_review

                review_health = preus_review.review_health(
                    db=self.config.db_path, now=now
                )
                review_alerts = preus_review.consume_new_review_health_alert(
                    db=self.config.db_path, health=review_health, now=now
                )
                result.decisions.append({
                    "action": "preus_review_handoff",
                    "status": review_health.get("status"),
                    "eligible": review_health.get("eligible_count", 0),
                    "reviewed": review_health.get("reviewed_count", 0),
                    "missing": review_health.get("missing_count", 0),
                })
                if self.send_telegram and notifier is not None and review_alerts:
                    row = review_alerts[0]
                    review_cfg = preus_review.load_cfg()
                    deadline_et = str(review_cfg.get("review_deadline_et") or "09:12")
                    if row.get("status") == "BASELINE_READY_LLM_MISSING":
                        action = (
                            f"deterministic baseline is ready, but the LLM overlay did not finish by "
                            f"{deadline_et} ET; no LLM promotion is assumed."
                        )
                    else:
                        action = (
                            f"structured review was not complete by {deadline_et} ET; "
                            "no promotion is assumed."
                        )
                    lines = [
                        "STOCKS PRE-US REVIEW WARNING",
                        f"- session: {row.get('session_date')}",
                        f"- status: {row.get('status')}",
                        f"- eligible/reviewed/missing: {row.get('eligible_count', 0)}/"
                        f"{row.get('reviewed_count', 0)}/{row.get('missing_count', 0)}",
                        f"- action: {action}",
                    ]
                    try:
                        notifier.send("\n".join(lines), parse_mode="")
                    except Exception as exc:  # noqa: BLE001
                        result.telegram_failed += 1
                        _LOG.warning("stocks pre-US review-health Telegram failed: %s", exc)
            except Exception as exc:  # noqa: BLE001
                result.decisions.append({
                    "action": "preus_review_handoff_failed",
                    "error": str(exc),
                })
                _LOG.warning("stocks pre-US review hand-off health failed: %s", exc)
            alerts = outcome.get("health_alerts") or []
            if self.send_telegram and notifier is not None and alerts:
                lines = ["MEXC STOCK PAPER DATA WARNING"]
                for row in alerts[:8]:
                    lines.append(
                        f"- {row.get('ticker')}: {row.get('reason') or row.get('status')}"
                    )
                try:
                    notifier.send("\n".join(lines), parse_mode="")
                except Exception as exc:  # noqa: BLE001
                    result.telegram_failed += 1
                    _LOG.warning("MEXC stock quote-health Telegram failed: %s", exc)
            preopen_alerts = outcome.get("preopen_health_alerts") or []
            if self.send_telegram and notifier is not None and preopen_alerts:
                for row in preopen_alerts:
                    lines = [
                        "MEXC STOCK PAPER PREOPEN WARNING",
                        f"- session: {row.get('session_date')}",
                        f"- actionable: {row.get('actionable_count', 0)}",
                        f"- processed: {row.get('processed_count', 0)}",
                        f"- reason: {row.get('reason') or row.get('status')}",
                    ]
                    try:
                        notifier.send("\n".join(lines), parse_mode="")
                    except Exception as exc:  # noqa: BLE001
                        result.telegram_failed += 1
                        _LOG.warning("MEXC stock preopen-health Telegram failed: %s", exc)
            fill_rows = active.get("fill_rows") or []
            if fill_rows:
                result.decisions.append({
                    "action": "mexc_stock_futures_paper_fill_telegram_suppressed",
                    "fills": len(fill_rows),
                    "reason": "phone_trade_feed_live_only",
                })
            try:
                from src.live_execution import stocks_breakout_bridge

                live_capture = stocks_breakout_bridge.capture_filled_positions(
                    active.get("fill_rows") or [], db=self.config.db_path, now=now
                )
                result.decisions.append({
                    "action": "mexc_stock_futures_live_bridge",
                    "status": live_capture.get("status"),
                    "seen": live_capture.get("seen", 0),
                    "queued": live_capture.get("queued", 0),
                    "duplicate": live_capture.get("duplicate", 0),
                    "rejected": live_capture.get("rejected", 0),
                    "reasons": live_capture.get("reasons", {}),
                    "risk_usdt": live_capture.get("risk_usdt"),
                })
            except Exception as exc:  # noqa: BLE001
                result.decisions.append({
                    "action": "mexc_stock_futures_live_bridge_failed",
                    "error": str(exc),
                })
                _LOG.warning("MEXC stock-futures live bridge failed: %s", exc)
            module.write_report(db=self.config.db_path, now=now, cfg=cfg)
        except Exception as exc:  # noqa: BLE001
            result.mexc_stock_paper_failed += 1
            _LOG.warning("MEXC stock-futures Paper tick failed: %s", exc)
            result.decisions.append(
                {"action": "mexc_stock_paper_failed", "error": str(exc)}
            )

        # The standard Paper breakout route is independent of the public-data
        # MEXC stock Paper simulator. A transient simulator quote failure must
        # never consume the short live-preflight window for an ordinary A/B
        # Paper signal such as the RTH breakout lane.
        try:
            from src.live_execution import stocks_breakout_bridge

            standard_live_capture = stocks_breakout_bridge.capture_standard_paper_breakouts(
                db=self.config.db_path, now=now
            )
            result.decisions.append({
                "action": "mexc_stock_standard_paper_live_bridge",
                "status": standard_live_capture.get("status"),
                "seen": standard_live_capture.get("seen", 0),
                "queued": standard_live_capture.get("queued", 0),
                "duplicate": standard_live_capture.get("duplicate", 0),
                "rejected": standard_live_capture.get("rejected", 0),
                "reasons": standard_live_capture.get("reasons", {}),
                "risk_usdt": standard_live_capture.get("risk_usdt"),
            })
        except Exception as exc:  # noqa: BLE001
            result.decisions.append({
                "action": "mexc_stock_standard_paper_live_bridge_failed",
                "error": str(exc),
            })
            _LOG.warning("standard Paper stock live bridge failed: %s", exc)

    def _pending_signal_ids(self) -> set[str]:
        """Current A/B ids plus immutable RTH and reviewed pre-open plans.

        Reviewed C plans enter only through materialized actionability after
        an immutable pre-gate A/B snapshot and a fresh A/B review.
        """
        from src.execution.stocks_preus_review import active_actionable_signal_ids
        from src.signals.tracker import select_pending_ab_signal_ids
        from src.stocks.paper_funnel import active_eligible_signal_ids

        ids = set(select_pending_ab_signal_ids(
            self.db, asset_class="stocks", modes={"intraday"}))
        ids.update(active_eligible_signal_ids(self.config.db_path))
        ids.update(active_actionable_signal_ids(self.config.db_path))
        rows_by_id = {
            str(row.get("signal_id") or ""): row for row in self.db.load_active_signals()
        }
        try:
            from src.signals.latency_telemetry import emit_discovered
            for signal_id in ids:
                row = rows_by_id.get(str(signal_id))
                if row:
                    emit_discovered(
                        self.db, row, source="stocks-monitor-session",
                        worker_id="stocks-monitor-session",
                    )
        except Exception:
            pass
        return ids

    def _refresh_pending_ohlcv(self, ids: set[str] | None = None) -> dict[str, int]:
        """Fetch only current stocks-intraday A/B symbols; no scoring or policy changes."""
        from src.stocks.configs.loader import load_stocks_config
        from src.stocks.data_collectors.stock_ohlcv_collector import StockOHLCVCollector

        ids = ids if ids is not None else self._pending_signal_ids()
        symbols = []
        for row in self.db.load_active_signals():
            if row.get("signal_id") in ids and row.get("symbol"):
                symbols.append(str(row["symbol"]).upper())
        symbols = sorted(set(symbols))[:self.max_pending_symbols]
        if not symbols:
            return {"attempted": 0, "fetched": 0, "failed": 0}
        collector = StockOHLCVCollector(self.config, load_stocks_config(self.config.root))
        # 1m is the execution-observation lane; 15m remains the deterministic
        # fallback and the report/scoring timeframe. This narrows a stock touch
        # from a 15-minute range to a one-minute bar without changing setup
        # generation, score, stop or targets.
        # These are already-approved candidates in the one-minute execution
        # lane, not a broad archival pull. Fetch their independent CSVs in a
        # small bounded pool so a multi-symbol queue cannot turn a fresh touch
        # into a stale observation before the tracker sees it.
        summary = collector.collect(
            symbols,
            ["1m", "15m"],
            period="5d",
            throttle_seconds=0.0,
            max_workers=4,
        )
        return {"attempted": len(symbols), "fetched": len(summary.fetched),
                "failed": len(summary.failed)}

    def _track_pending_entries(self, notifier, signal_ids: set[str] | None = None):
        from src.signals.config import load_signal_tracking_config
        from src.signals.tracker import track_pending_entries

        tracker_cfg = load_signal_tracking_config(self.config.root)
        return track_pending_entries(
            store=self.db,
            file_store=self._file_store(),
            project_config=self.config,
            tracker_config=tracker_cfg,
            paper_entry_notifier=notifier,
            paper_entry_dry_run=not self.send_telegram,
            asset_class="stocks",
            modes={"intraday"},
            signal_ids=sorted(signal_ids) if signal_ids is not None else None,
            telemetry_source="stocks-monitor-session",
        )

    def _file_store(self):
        from src.storage.file_store import FileStore
        return FileStore(self.config)

    def _refresh_forward_shadow(self) -> None:
        """Refresh the current stocks-intraday lane plus isolated research.

        The added variants are explicitly Shadow-only and cadence-bounded in
        their own module. A failure must never interrupt the authoritative
        pending-entry tracker or the current Paper candidate lane.
        """
        from src.execution.paper_shadow_engine import refresh as shadow_refresh
        from src.stocks import coverage_gate

        shadow_refresh(lookback_hours=336, max_signals=200, candidate_only=True,
                       db=str(self.config.db_path))
        # The report just refreshed the local cache. Reclassify that cache
        # without another network request so clean/dirty labels are current.
        coverage_gate.refresh(symbols=None, modes=["intraday"], prewarm=False,
                              mark_outcomes=True, db=str(self.config.db_path))
        try:
            from src.execution import stocks_catalyst_rs_shadow

            stocks_catalyst_rs_shadow.refresh(db=str(self.config.db_path))
        except Exception as exc:  # noqa: BLE001 - research must remain non-fatal
            _LOG.warning("stocks catalyst RS shadow refresh failed: %s", exc)
        try:
            from src.execution import stocks_intraday_variants_shadow

            stocks_intraday_variants_shadow.refresh(db=str(self.config.db_path))
        except Exception as exc:  # noqa: BLE001 - research must remain non-fatal
            _LOG.warning("stocks intraday variants shadow refresh failed: %s", exc)

    def _load_active_ab(self) -> list[dict[str, Any]]:
        rows = self.db.load_active_signals()
        out: list[dict[str, Any]] = []
        for row in rows:
            if (row.get("asset_class") or "crypto").lower() != "stocks":
                continue
            if str(row.get("tier") or "").upper() not in {"A", "B"}:
                continue
            out.append(row)
        return out

    def _notifier_or_none(self):
        try:
            from src.notifiers.trade_telegram import notifier_for
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("Telegram notifier import failed: %s", exc)
            return None
        try:
            notifier = notifier_for(self.config.root)
            if not notifier.enabled or not notifier.chat_id:
                _LOG.info("Telegram notifier not enabled/configured — dry-run only.")
                return None
            return notifier
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("Telegram notifier init failed: %s", exc)
            return None

    def _extra_context_for(self, sig: dict[str, Any]) -> dict[str, Any]:
        """Pull a thin slice of useful context for the Telegram message.

        Strictly read-only. Failures fall back to safe defaults.
        """
        ctx: dict[str, Any] = {}
        try:
            from src.signals.analytics import compute_breakdowns
            from src.signals.config import load_signal_tracking_config

            cfg = load_signal_tracking_config(self.config.root)
            br = compute_breakdowns(
                self.db, config=cfg, period="week", asset_class="stocks"
            )
            ctx["recent_sample_size"] = (br.overall or {}).get("sample_size")
        except Exception:  # noqa: BLE001
            pass
        regime = sig.get("market_regime") or "bullish"
        ctx["regime"] = regime
        ctx["sector_confirmation"] = sig.get("sector") or "see report"
        ctx["earnings_risk"] = "UNKNOWN" if not sig.get("news_supported") else "see report"
        ctx["news_catalyst"] = (
            "yes" if sig.get("news_supported") else "none verified"
        )
        ctx["main_risk"] = (
            "earnings UNKNOWN — undated event risk"
            if not sig.get("news_supported")
            else "see counter-thesis"
        )
        ctx["what_to_monitor"] = (
            "SPY/QQQ direction; sector ETF alignment; relative volume"
        )
        return ctx


# ---------------------------------------------------------------------------
# Module-level utilities
# ---------------------------------------------------------------------------


def _tier_rank(tier: str) -> int:
    return {"A": 3, "B": 2, "C": 1}.get(tier.upper(), 0)


def _as_float(v: Any) -> float | None:
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _entry_mid(payload: Any) -> float | None:
    if not isinstance(payload, dict):
        return None
    low = _as_float(payload.get("entry_low"))
    high = _as_float(payload.get("entry_high"))
    if low is not None and high is not None:
        return (low + high) / 2.0
    return low if low is not None else high


def _safe_payload(alert_row: dict[str, Any]) -> dict[str, Any]:
    import json

    raw = alert_row.get("payload_json")
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except Exception:  # noqa: BLE001
        return {}


def _is_us_market_hours(now: datetime) -> bool:
    """Use the canonical DST/holiday-aware US cash-session calendar."""
    try:
        from src.stocks.market_calendar import is_us_cash_session_open
        return is_us_cash_session_open(now)
    except Exception:
        # Conservative fallback if the calendar module itself is unavailable.
        if now.weekday() >= 5:
            return False
        minutes = now.hour * 60 + now.minute
        return 13 * 60 + 30 <= minutes <= 20 * 60
