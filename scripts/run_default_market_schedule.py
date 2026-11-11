"""Default market scheduler — the desk's permanent operating loop.

Cadence
-------
Every **2 hours** by default. On each tick:

* always: track-signals → crypto scalp + intraday → support commands
  (active-signals, signal-stats, detector, post-track, daily review).
* **weekdays (Mon-Fri Asia/Nicosia)**: also run `stocks-intraday-report`
  + stocks active/stats. Stocks scalp does NOT exist in this CLI;
  we log "stocks scalp unavailable" and continue.
* **weekends (Sat/Sun)**: crypto-only, stocks fully skipped.

Long-horizon (swing/invest) runs **once per day** — gated by a marker
file ``daily_<date>.done`` in the run folder. First cycle of a UTC day
runs the long-horizon pass; later cycles skip cleanly.

Opus / enriched-review is NOT called from this scheduler. It only
prepares packets / reports / news / Obsidian for a manual run via
`.claude/skills/enriched-review/SKILL.md`. The user triggers Opus.

No auto-trade. No scoring / threshold / agent / strategy code change.
The same safety contract as `run_24h_crypto_only_schedule.py`.

CLI
---
``--hours``                     total run length (default 24).
``--interval-hours``            gap between cycles (default 2).
``--interval-minutes``          smoke-test override for the interval.
``--minutes``                   smoke-test override for total length.
``--monitor-minutes``           bounded crypto monitor window per cycle (default 90).
``--crypto-only``               force crypto-only even on weekdays.
``--no-stocks``                 same as ``--crypto-only``.
``--run-once``                  run exactly one cycle then exit.
``--date YYYY-MM-DD``           override "today" (useful with ``--run-once``
                                to dry-run a specific day's logic).
``--send-telegram / --no-send-telegram``
``--dry-run``                   validate plan + CLI, no subprocess calls.
"""

from __future__ import annotations

import argparse
import logging
import os
import signal
import subprocess
import sys
import time
import traceback
from dataclasses import dataclass, field
from datetime import date as _date_t
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TZ = "Asia/Nicosia"

# Windows DLL init failure — observed in cycle 10 of the prior 24h run.
# Treated as a transient infrastructure error; retry with backoff.
WINDOWS_DLL_INIT_FAILED_EXIT = 3221225794  # 0xC0000142
DLL_RETRY_BACKOFF_SECONDS = 60
DLL_RETRY_MAX = 2

# The scheduler waits two hours *after* a cycle completes before starting the
# next one, and the replacement monitor is launched near the end of that next
# cycle. Cover the two-hour wait plus up to one hour of cycle work; the scoped
# PID lock replaces a still-running predecessor without creating duplicates.
PENDING_MONITOR_MINUTES = 180

# Most read-model helpers should finish inside five minutes. The two paired
# historical simulations legitimately walk hundreds of signals and repeatedly
# load candle history, so the generic limit was killing healthy work before it
# could persist a result.
NONFATAL_TIMEOUT_SECONDS = 300
NONFATAL_TIMEOUT_OVERRIDES: dict[str, int] = {
    # The label pass now scans a seven-figure outcome ledger. It runs after
    # the execution monitors are already bootstrapped, so allowing completion
    # here does not delay live/paper entry handling.
    "catalyst label refresh": 900,
    "crypto quality overlay report (counterfactual)": 900,
    "crypto swing versioned shadow sweep (counterfactual)": 900,
    # This local analytics pass scans up to 80 cached symbols.  It normally
    # completes well below this after sharing one read-only archive connection,
    # but cold Windows file cache should not truncate a healthy refresh.
    "intelligence layer update": 600,
    "signal outcome path retention (daily)": 900,
    "market intelligence retention (daily)": 1200,
    # The preceding tracker and dedicated collectors already refreshed the
    # caches. This presentation/candidate pass must not hold the shared DB
    # behind live reconciliation for many minutes.
    "crypto intraday report": 180,
    # Operator dashboards are disposable presentation work. They must never
    # consume a large fraction of the next research cycle when Telegram or an
    # Obsidian file handle becomes unavailable.
    "refresh obsidian dashboard": 60,
    "telegram dashboard refresh (read-only)": 60,
}


# (label, argv, kind, duration_min)
Step = tuple[str, list[str], str, int]


def _cli(*args: str) -> list[str]:
    return [sys.executable, "-m", "src.cli", *args]


def _script(*args: str) -> list[str]:
    return [sys.executable, "-m", *args]


def _utc_today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# Calendar
# ---------------------------------------------------------------------------


def is_weekend(now: datetime) -> bool:
    """Saturday (5) or Sunday (6) in the project's TZ."""

    tz = now.astimezone(ZoneInfo(DEFAULT_TZ))
    return tz.weekday() >= 5


# Long-horizon (swing / invest) used to run once per UTC day. PART 9 (2026-06)
# expands it to **two windows** per day:
#   * Window 1 ≈ 04:00 EEST — crypto daily candles just closed (1h after 00:00 UTC).
#   * Window 2 ≈ 16:00 EEST — US pre-market (~30 min before NYSE open).
# Both windows fire on the closest scheduler cycle inside the inclusive
# bucket. Stocks pieces still respect ``stocks_enabled()`` so weekends only
# run the crypto half.
LONG_HORIZON_WINDOW_HOURS: dict[int, tuple[int, int]] = {
    1: (3, 5),   # cycle starts inside [03:00, 05:00) EEST → window 1
    2: (15, 17),  # cycle starts inside [15:00, 17:00) EEST → window 2
}


def current_long_horizon_window(now: datetime) -> int | None:
    """Return 1, 2, or None depending on whether ``now`` falls into a
    long-horizon firing window in the project TZ."""
    tz = now.astimezone(ZoneInfo(DEFAULT_TZ))
    hour = tz.hour
    for window_id, (lo, hi) in LONG_HORIZON_WINDOW_HOURS.items():
        if lo <= hour < hi:
            return window_id
    return None


def due_long_horizon_window(
    now: datetime,
    *,
    is_done: Callable[[int], bool],
) -> tuple[int | None, bool]:
    """Return the next required long-horizon window and recovery status.

    A machine restart after 17:00 used to skip the afternoon swing scan until
    the following day. A catch-up runs the most recent missed window once,
    using current data and the same marker contract as an on-time run.
    """
    current = current_long_horizon_window(now)
    if current is not None and not is_done(current):
        return current, False

    hour = now.astimezone(ZoneInfo(DEFAULT_TZ)).hour
    for window_id, (_, end_hour) in reversed(list(LONG_HORIZON_WINDOW_HOURS.items())):
        if hour >= end_hour and not is_done(window_id):
            return window_id, True
    return None, False


def stocks_enabled(
    now: datetime, *, force_crypto_only: bool = False
) -> bool:
    """Return True iff the stocks pipeline should run this cycle.

    * ``force_crypto_only=True`` → never.
    * Weekend → never.
    * Weekday → yes (the report itself stamps data freshness, so
      stale-after-market-close prices are visible to downstream readers).
    """

    if force_crypto_only:
        return False
    return not is_weekend(now)


# ---------------------------------------------------------------------------
# Steps
# ---------------------------------------------------------------------------


def core_pre_steps() -> list[Step]:
    # 2026-06-09: --revalidate-pending wires the pending-signal revalidator
    # into every cycle. After the candle walk, signals still in
    # waiting_for_entry are checked against per-mode freshness horizons and
    # the favorable-excursion-without-fill rule. Read-mostly: never mutates
    # entry/stop/TP/expires_at; only the lifecycle `status` and a notes
    # annotation. See reports/PENDING_SIGNAL_REVALIDATION_REPORT.md.
    return [
        ("track-signals (pre)",
         _cli("track-signals", "--all", "--revalidate-pending"),
         "command", 0),
    ]


def telegram_outbox_retry_step() -> Step:
    """Delivery-only retry for failed paper entry/close Telegram alerts."""
    return (
        "telegram paper-alert outbox retry",
        _cli("telegram-outbox-retry", "--limit", "25"),
        "command_nonfatal",
        0,
    )


def crypto_report_steps() -> list[Step]:
    return [
        ("crypto scalp report", ["__note__", "disabled: negative forward edge; research data retained"],
         "note", 0),
        ("crypto intraday report",
         _cli("intraday-report", "--no-update", "--skip-packet"),
         "command_nonfatal", 0),
    ]


def news_entity_resolve_step(hours: int = 72) -> Step:
    """PRODUCTION news entity/narrative RESOLVER — runs BEFORE catalyst-scan / catalyst-label-refresh so
    those steps read freshly-resolved detected_symbols / entity columns. Reads title + body/url slug +
    structured fields, resolves crypto+stock symbols (cross-asset), listing tickers, and macro tags;
    UNION-only enriches news_items. Never touches score/tier/proposed_signals/final_r/live. Non-fatal."""
    return (
        f"news entity resolve ({hours}h, enrichment)",
        _cli("news-entity-resolve", "--hours", str(hours), "--limit", "10000"),
        "command_nonfatal",
        0,
    )


def news_health_monitor_step() -> Step:
    """Alert-only watchdog for RSS/API transport and Telegram channel health.

    It writes the news error journal and sends transition/recovery notices to
    the operator chat. Fail-open: it cannot block reports, paper execution, or
    any trading path.
    """
    return (
        "news source health monitor (alert-only)",
        _cli("news-health-monitor", "--send-telegram"),
        "command_nonfatal",
        0,
    )


def news_source_health_snapshot_step() -> Step:
    """Refresh the full per-source health report before evaluating alerts."""
    return (
        "news source health snapshot refresh",
        _cli("news-source-health"),
        "command_nonfatal",
        0,
    )


def news_entity_health_step() -> Step:
    """2026-07-13 audit: this resolver-freshness/coverage diagnostic previously existed ONLY as a
    manual CLI command (data/diagnostics/news_entity_health.json aged 5+ days stale in production
    because nothing ever ran it). Alert-only + fail-open, same shape as news_health_monitor_step
    above: writes the health report/JSON and sends a deduped Telegram alert on a CRITICAL
    transition/recovery. Never blocks a report, signal, paper execution, or live path."""
    return (
        "news entity resolver health monitor (alert-only)",
        _cli("news-entity-health", "--send-telegram"),
        "command_nonfatal",
        0,
    )


def entry_mode_calibration_refresh_step() -> Step:
    """2026-07-13 audit: the per-slice (asset x mode x entry_mode x branch x window) calibration
    read-model previously only refreshed when someone ran the CLI by hand. It's a cheap, pure-SQL
    aggregation over already-persisted paper_shadow_execution_outcomes (no OHLCV/network work of its
    own), so it's safe to run every cycle rather than only on the heavier long-horizon window.
    Writes ONLY entry_mode_calibration_* tables/JSON; never proposed_signals/signal_outcomes/final_r;
    no live; nothing promoted automatically."""
    return (
        "entry-mode calibration refresh (read-model)",
        _cli("entry-mode-calibration-refresh"),
        "command_nonfatal",
        0,
    )


def sec_edgar_refresh_step() -> Step:
    """Ingest recent SEC EDGAR filings (8-K/10-Q/10-K/S-1/424B/13D/13G etc.) for the stock universe into
    news_items. Runs BEFORE the entity resolver / catalyst-scan so fresh filings are resolved + linked the
    same cycle. Was previously unscheduled → the source aged out past 72h and showed DEAD in source-health;
    running it per cycle (it is a light CIK-mapped submissions-API fetch, a few dozen requests) keeps it
    fresh 24/7. Advisory/enrichment only; never a score/tier/final_r/live change. Non-fatal (fail-open on
    a network blip)."""
    return (
        "sec edgar filings ingest",
        _cli("sec-edgar-refresh"),
        "command_nonfatal",
        0,
    )


def telegram_catchup_step(hours: int = 24) -> Step:
    """SAFETY-NET Telegram backfill (long-horizon / ~2x day). The live event-driven collector
    (`CryptoAIDesk_TelegramCollector` task) is the primary path, but it only captures NEW messages and
    — as seen 2026-07-07 — can be killed and sit down silently with no rows landing. This one-shot
    catch-up fetches recent messages for all configured channels and UNION-saves them to news_items via
    the SAME normalization path (dedup by t.me url), so telegram news self-heals even if the live
    collector is down. It uses public `t.me/s` pages and never opens the live collector's Telethon
    session.
    Ingest/read-model only; never alerts / scores / trades. Non-fatal."""
    return (
        f"telegram news catch-up (safety-net {hours}h)",
        _script("scripts.telegram_catchup_news", "--hours", str(hours), "--limit-per-channel", "20"),
        "command_nonfatal",
        0,
    )


def telegram_stale_recovery_step() -> Step:
    """Targeted recovery for a truly unhealthy Telegram source, not normal channel quietness.

    The helper first reads source health and performs no public-page request unless
    a channel has an error or zero 72h rows. It uses a cooldown and records failures
    through the existing telemetry/journal path without touching the Telethon session.
    """
    return (
        "telegram stale-source targeted recovery",
        _script("scripts.telegram_stale_recovery", "--hours", "72", "--limit-per-channel", "20", "--max-targets", "6"),
        "command_nonfatal",
        0,
    )


def news_content_coverage_step() -> Step:
    return (
        "news content coverage diagnostic (read-only)",
        _cli("news-content-coverage", "--hours", "72"),
        "command_nonfatal",
        0,
    )


def news_coverage_gaps_step() -> Step:
    return (
        "news coverage gaps diagnostic (read-only)",
        _cli("news-coverage-gaps", "--hours", "72"),
        "command_nonfatal",
        0,
    )


def news_asset_registry_step() -> Step:
    """Local/versioned asset inventory. DISCOVERED exchange symbols remain
    untrusted until curated; no signal or trade-universe promotion occurs."""
    return (
        "news asset registry refresh",
        _cli("news-asset-registry-refresh"),
        "command_nonfatal",
        0,
    )


def news_canonical_refresh_step(hours: int = 168) -> Step:
    """Repair/backfill pass for the incremental canonical-event pipeline."""
    return (
        f"news canonical events + influence policy ({hours}h)",
        _cli("news-canonical-refresh", "--hours", str(hours)),
        "command_nonfatal",
        0,
    )


def news_quality_gate_step() -> Step:
    """Gold cases + production replay. Diagnostic only; a failed trust claim
    never blocks raw ingest or an unrelated paper execution path."""
    return (
        "news quality gold/replay gate",
        _cli("news-quality-gate"),
        "command_nonfatal",
        0,
    )


def news_entity_resolve_fast_step(hours: int = 24) -> Step:
    """Lightweight post-ingest RESOLVER pass. There is no standalone news/rss/telegram ingest step —
    ingest is baked into the report steps (RSSNewsCollector runs inside scalp/intraday and the stock
    reports). The main `news_entity_resolve_step` (72h) runs right after the CRYPTO reports, but STOCK
    news is ingested later (in `stocks_report_steps`), so without this pass those rows would sit with a
    `detected_symbols_json` yet no `resolution_status` / `trusted_symbols_json` until the next cycle. This
    fast 24h pass resolves them same-cycle. Idempotent + UNION-only + non-fatal; never touches
    score/tier/proposed_signals/final_r/live."""
    return (
        f"news entity resolve (fast {hours}h post-ingest)",
        _cli("news-entity-resolve", "--hours", str(hours), "--limit", "10000"),
        "command_nonfatal",
        0,
    )


def catalyst_scan_step() -> Step:
    """Structured catalyst / narrative scan (PART 1 of Sprint 22-style).

    Pure read of news_items → classification → narrative baskets →
    JSONL files in data/catalysts/<date>/. Non-fatal: a failure here
    must never block the cycle (the wrapper logs and continues).
    """

    return (
        "catalyst / narrative scan",
        _cli("catalyst-scan", "--no-print"),
        "command_nonfatal",
        0,
    )


def catalyst_integrity_step() -> Step:
    """Catalyst integrity monitor — runs right AFTER the catalyst scan so it
    checks the freshly-written narrative_baskets/catalyst_events against
    news_items. Read-only: writes reports/CATALYST_INTEGRITY_DAILY_SUMMARY.md and
    prints a warning if a no-catalyst basket still contains a direct-news symbol
    (the ASTER regression signature). Never promotes a trade. Non-fatal."""
    return (
        "catalyst integrity scan",
        _script("scripts.catalyst_integrity_scan"),
        "command_nonfatal",
        0,
    )


def catalyst_label_refresh_step() -> Step:
    """Refresh the catalyst/news linkage on tracked signals — runs right AFTER
    the integrity scan. Re-derives news_supported/telegram_supported from a
    robust detected_symbols_json join windowed around each signal's creation
    time (fixing the scan-time limit=100 ~5h under-fire) and rebuilds the
    signal_catalyst_labels derived cache so it stops being frozen at the one-time
    backfill. Display/measurement only: never fabricates a catalyst, never
    downgrades a flag, never touches scoring/TP/SL/entry/routing. Non-fatal."""
    return (
        "catalyst label refresh",
        _cli("catalyst-label-refresh"),
        "command_nonfatal",
        0,
    )


def catalyst_label_refresh_post_stock_step() -> Step:
    """Second lightweight label refresh after the stock report has ingested fresh stock news and the
    fast entity resolver has trusted-tagged it. This closes the same-cycle gap for stock
    news_supported / signal_catalyst_labels without changing score/tier/routing/live."""
    return (
        "catalyst label refresh (post-stock news)",
        _cli("catalyst-label-refresh"),
        "command_nonfatal",
        0,
    )


def paper_execution_refresh_step() -> Step:
    """Recompute the PAPER execution accounting (Model F) for all entered signals.
    Computes the honest paper_execution_r (early MFE-armed protection: BE @ +0.6R,
    lock +0.5R @ +1R, runner to TP3) beside the legacy touch-based final_r and
    upserts into the additive paper_execution_outcomes table. PAPER/ACCOUNTING
    ONLY: never rewrites signal_outcomes/final_r, never places orders, never
    changes scoring/TP/SL/entry/routing. Idempotent. Non-fatal."""
    return (
        "paper execution accounting refresh",
        _cli("paper-execution-refresh", "--limit", "120"),
        "command_nonfatal",
        0,
    )


def paper_tp_refresh_step() -> Step:
    """Recompute the structural PAPER take-profit set (PART 3) for entry-triggered
    signals — runs right AFTER the paper execution refresh. Loads the real OHLCV the
    tracker uses and derives TPs from chart structure (swing H/L, range, round numbers,
    volume profile), persisting mechanical_tp* + active_paper_tp* + tp_set_type
    (STRUCTURAL/HYBRID/ATR_FALLBACK/NO_VALID_TP) into the additive signal_paper_tp
    table. PAPER ONLY: never touches proposed_signals.tp* / final_r / scoring / entry /
    routing, never places orders. Idempotent. Non-fatal."""
    return (
        "paper structural TP refresh",
        # The structural engine reads OHLCV per signal.  A bounded round-robin
        # batch finishes inside the scheduler timeout; signal_paper_tp ordering
        # refreshes the oldest/missing record first on the next cycle.
        _cli("paper-tp-refresh", "--limit", "200"),
        "command_nonfatal",
        0,
    )


def entry_mode_refresh_step() -> Step:
    """Classify the PAPER entry mode (PART 4) for entry-triggered signals — runs right
    after the structural TP refresh. Labels each signal PULLBACK_LIMIT / STRUCTURAL_RETEST
    / BREAKOUT_CONTINUATION / MOMENTUM_TAKER_NOW / LIMIT_THEN_TAKER_TIMEOUT / NO_CHASE_SKIP
    from real chart structure + momentum into the additive signal_entry_mode table.
    PAPER ONLY: never touches production entry / final_r / scoring / routing. Non-fatal."""
    return (
        "paper entry-mode classify",
        _cli("entry-mode-refresh", "--limit", "200"),
        "command_nonfatal",
        0,
    )


def preentry_classifier_step() -> Step:
    """Classify the mode available at signal creation, using only closed candles.

    This is deliberately separate from the post-entry diagnostic classifier and
    runs every cycle before the shadow engine. The paper-entry hook also has an
    inline capture fallback, so an alert never has to wait for this scheduler.
    """
    return (
        "pre-entry mode classify (lookahead-safe)",
        _cli("preentry-classifier-refresh"),
        "command_nonfatal",
        0,
    )


def stock_direction_refresh_step() -> Step:
    """Compute the causal multi-factor PAPER stock direction for recent stock
    signals — runs after the entry-mode classify. Fuses EMA + VWAP + prior-day H/L break +
    momentum + RS-vs-SPY + (MSTR) BTC-trend into a signed direction score + label into the
    additive stock_direction_score table. PAPER ONLY: never touches production direction /
    final_r / scoring / routing. Non-fatal."""
    return (
        "paper stock direction (multi-factor)",
        _cli("stock-direction-refresh", "--limit", "240"),
        "command_nonfatal",
        0,
    )


def paper_stop_refresh_step() -> Step:
    """Compute the structural PAPER stop-move plan (PART 8) for entry-triggered signals — runs
    after the structural TP refresh. Derives the post-TP1/TP2 stop from real chart structure
    (higher-low/lower-high/support/VWAP) beside the BE/lock fallback into signal_stop_plan.
    PAPER ONLY: never moves a production stop / final_r. Non-fatal."""
    return (
        "paper structural stop plan",
        _cli("paper-stop-refresh", "--limit", "200"),
        "command_nonfatal",
        0,
    )


def paper_shadow_execution_step() -> Step:
    """Run the paper-shadow A/B execution lane (NEXT STEP) — runs after the overlay refreshes so it
    consumes fresh entry-mode / structural-TP / stop-plan / stock-direction. Simulates A (old paper)
    vs B (new logic) over the same OHLCV + fees, splitting historical_backfill from
    forward_since_activation. MEASUREMENT ONLY: never places orders / mutates final_r / no live.
    Fail-open (CLI swallows errors). Non-fatal."""
    return (
        "paper-shadow A/B execution",
        _cli(
            "paper-shadow-execution-refresh",
            "--lookback-hours", "336",
            "--max-signals", "240",
        ),
        "command_nonfatal",
        0,
    )


def sequential_promotion_gate_step() -> Step:
    """Refresh forward paired A/B promotion evidence after its inputs refresh.

    This is evaluation-only and cannot promote or route a strategy.
    """
    return (
        "sequential promotion gate (forward A/B, read-model)",
        _cli("sequential-gate-report"),
        "command_nonfatal",
        0,
    )


def crypto_intraday_idea_sweep_step() -> Step:
    """Run the narrowly-scoped crypto intraday parameter tests after B refresh.

    This writes only its own experiment read-model tables/report. It is intentionally
    non-fatal and does not alter the production overlay, entry policy, or paper book.
    """
    return (
        "crypto intraday idea sweep (read-model)",
        _cli("crypto-intraday-idea-sweep", "--limit", "400"),
        "command_nonfatal",
        0,
    )


def paper_shadow_digest_step() -> Step:
    """Send the once-daily paper-shadow A/B Telegram digest if due (PART 2). Idempotent: the CLI
    guards on send-time + once-per-day, so running it every cycle sends at most once daily.
    Observability only: never trades / promotes B / changes scoring / final_r. Non-fatal."""
    return (
        "paper-shadow A/B telegram digest",
        _cli("paper-shadow-digest-send", "--no-dry-run"),
        "command_nonfatal",
        0,
    )


def telegram_dashboard_refresh_step() -> Step:
    """Refresh an operator-created pinned dashboard after a completed cycle.

    The CLI is intentionally a no-op until `/dashboard` has created a message.
    It reads current Paper/Shadow evidence and may edit that one message, but
    cannot create a trade, mutate a guard, or route Live execution.
    """
    return (
        "telegram dashboard refresh (read-only)",
        _cli("telegram-dashboard-refresh"),
        "command_nonfatal",
        0,
    )


def _telegram_dashboard_enabled() -> bool:
    """Read only the UI feature flag; never reaches trading configuration."""
    try:
        from src.notifiers.telegram_dashboard.config import load_dashboard_config
        return load_dashboard_config(PROJECT_ROOT).enabled
    except Exception:
        return False


def telegram_dashboard_monitor_step() -> Step:
    """Long-poll dashboard callbacks without creating an unsolicited post."""
    return (
        "telegram dashboard callbacks (read-only, background)",
        _cli("telegram-dashboard", "--no-create", "--duration-hours", "0"),
        "telegram_dashboard_monitor",
        0,
    )


def crypto_quality_cooldown_step() -> Step:
    """CRYPTO QUALITY OVERLAY (read-model): fast per-cycle recompute of rolling session + per-symbol
    cooldown state from recent closed crypto paper outcomes, so the paper-entry overlay reads fresh
    cooldowns. Writes ONLY crypto_quality_cooldowns; never proposed_signals / signal_outcomes /
    final_r / live. Non-fatal."""
    return ("crypto quality cooldown refresh (read-model)", _cli("crypto-cooldown-refresh"),
            "command_nonfatal", 0)


def crypto_overlay_report_step() -> Step:
    """CRYPTO QUALITY OVERLAY (read-model): heavier overlay decisions + counterfactual (avoided-loss vs
    missed-profit, missed runners) → reports/CRYPTO_QUALITY_OVERLAY.md. Fires on the long-horizon
    windows only. Read-model / display only; never final_r / live. Non-fatal."""
    return ("crypto quality overlay report (counterfactual)", _cli("crypto-overlay-report"),
            "command_nonfatal", 0)


def crypto_swing_policy_sweep_step() -> Step:
    """Crypto swing versioned shadow sweep: native-geometry control plus T140/T130 and overlay
    counterfactuals. Writes only additive diagnostic/counterfactual read-models + report.
    Never proposed_signals, signal_outcomes, final_r, active paper ledger, or live. Non-fatal."""
    return ("crypto swing versioned shadow sweep (counterfactual)",
            _script("scripts.crypto_swing_entry_sweep", "--persist-counterfactual"),
            "command_nonfatal", 0)


def crypto_swing_breakout_refinement_step() -> Step:
    """Run the separate forward-only swing-breakout reclaim/failure tests.

    This is a report-only Shadow experiment. It cannot alter the production
    swing geometry, Paper routing, ledger, or any live execution path.
    """
    return ("crypto swing breakout reclaim/refailure refinements (shadow)",
            _script("scripts.crypto_swing_entry_sweep", "--breakout-refinements"),
            "command_nonfatal", 0)


def entry_latency_audit_step() -> Step:
    """Classify entry-latency root cause (PART 6) for entry-triggered signals — runs after the
    stock direction refresh. Labels DATA_GAP_LATE (coverage gap, e.g. the MSTR 184-min case) vs
    DETECTION_LATENCY (genuine missed fill) vs LEGITIMATE_LATE / FAST into the additive
    entry_latency_audit table. Read-only diagnostic; never touches outcomes / final_r. Non-fatal."""
    return (
        "entry latency audit (root cause)",
        _cli("entry-latency-audit", "--limit", "120"),
        "command_nonfatal",
        0,
    )


def latency_acceptance_step() -> Step:
    """Persist the independent crypto/stocks latency acceptance report. Observability only."""
    return (
        "latency acceptance report (per asset, read-only)",
        _cli("latency-sla-report", "--recent-days", "7", "--write"),
        "command_nonfatal",
        0,
    )


def paper_operational_audit_step() -> Step:
    """One authoritative Paper health view after ledger/overlay/funnel refreshes."""
    return (
        "paper operational audit (USD/evidence/funnel)",
        _cli("paper-operational-audit", "--recent-days", "7", "--write"),
        "command_nonfatal",
        0,
    )


def live_funnel_report_step() -> Step:
    """Proposed -> Paper alert -> MEXC decision -> outbox -> order diagnostics."""
    return (
        "live funnel report",
        _cli("live-funnel-report", "--hours", "24"),
        "command_nonfatal",
        0,
    )


def crypto_live_fallback_capture_step() -> Step:
    """Safety-net capture for fresh crypto Paper entries missed by the notifier."""
    return (
        "crypto live fallback capture",
        _cli("crypto-live-fallback-capture", "--max-age-seconds", "300"),
        "command_nonfatal",
        0,
    )


def crypto_live_mode_audit_step() -> Step:
    """Paper->Live route audit plus Crypto Invest / Liquidity Sweep v2 health."""
    return (
        "crypto live mode audit",
        _cli("crypto-live-mode-audit", "--hours", "96"),
        "command_nonfatal",
        0,
    )


def strategy_governance_step() -> Step:
    """Evidence lifecycle, frozen-config and micro-canary guard report."""
    return (
        "strategy evidence governance",
        _cli("strategy-governance-refresh"),
        "command_nonfatal",
        0,
    )


def stock_coverage_gate_step(prewarm: bool) -> Step:
    """Stock OHLCV coverage gate (S2/S5/S6). prewarm=False (per-cycle) = cache-only re-classify +
    populate per-outcome coverage/clean flags (no network). prewarm=True (RTH/nightly windows) =
    fetch + local archive via the fallback chain so delay never manufactures false late entries.
    Read-model + local OHLCV archive only; never proposed_signals / signal_outcomes / final_r / live.
    Non-fatal."""
    label = ("stock coverage gate + prewarm/archive" if prewarm
             else "stock coverage gate (cache-only re-classify + mark outcomes)")
    return (
        label,
        _cli("stock-coverage-gate", "--prewarm" if prewarm else "--no-prewarm"),
        "command_nonfatal",
        0,
    )


def stocks_intraday_forward_shadow_evaluation_step() -> Step:
    """Evaluate the separate clean-only forward candidate lane after coverage flags are fresh.

    This never promotes a mode or changes paper candidate routing; it only makes
    the currently excluded stocks-intraday shadow evidence visible and honest.
    """
    return (
        "stocks intraday forward shadow evaluation (clean-only)",
        _cli("stocks-intraday-forward-shadow-evaluate"),
        "command_nonfatal",
        0,
    )


def stocks_catalyst_rs_shadow_step() -> Step:
    """Independent catalyst/RS experiment after stock bars, resolver and coverage."""
    return (
        "stocks catalyst RS continuation (isolated shadow)",
        _cli("shadow-stocks-catalyst-rs-refresh"),
        "command_nonfatal",
        0,
    )


def stocks_earnings_gap_shadow_step() -> Step:
    """Independent earnings-only continuation experiment."""
    return (
        "stocks earnings gap continuation (isolated shadow)",
        _cli("shadow-stocks-earnings-gap-refresh"),
        "command_nonfatal",
        0,
    )


def stocks_preus_candidate_bundle_step() -> Step:
    """Prepare the deterministic pre-US review bundle for the external routine.

    This only writes the review packet.  The routine remains the sole LLM
    caller and the validated ingest command remains the sole narrow write path
    for review verdicts.
    """
    return (
        "stocks pre-US review candidate bundle (advisory)",
        _cli("stocks-preus-candidates"),
        "command_nonfatal",
        0,
    )


def stocks_intraday_variants_shadow_step() -> Step:
    """Research-only stock entry refinements, isolated from Paper routing.

    The command has its own 15-minute freshness bound, so the ordinary
    scheduler supplies recovery coverage without causing duplicate scans when
    the fast RTH monitor is already maintaining the evidence.
    """
    return (
        "stocks intraday VWAP/confirmed-breakout variants (isolated shadow)",
        _cli("shadow-stocks-intraday-variants-refresh"),
        "command_nonfatal",
        0,
    )


def stocks_intraday_breakout_1bar_paper_step() -> Step:
    """Candidate generation for the versioned, non-live one-bar Paper lane."""
    return (
        "stocks intraday breakout one-bar (versioned Paper lane)",
        _cli("stocks-intraday-breakout-1bar-paper-refresh", "--no-update"),
        "command_nonfatal",
        0,
    )


def stocks_intraday_pullback_paper_step() -> Step:
    """Candidate generation for the isolated pullback/VWAP-hold Paper lane."""
    return (
        "stocks intraday pullback VWAP hold (versioned Paper lane)",
        _cli("stocks-intraday-pullback-paper-refresh", "--no-update"),
        "command_nonfatal",
        0,
    )


def stocks_catalyst_rs_paper_step() -> Step:
    """Consume fresh clean Catalyst RS confirmations after its Shadow refresh."""
    return (
        "stocks catalyst RS continuation (versioned Paper lane)",
        _cli("stocks-catalyst-rs-paper-refresh", "--no-shadow-refresh"),
        "command_nonfatal",
        0,
    )


def stocks_swing_event_rs_pullback_paper_step() -> Step:
    """Candidate generation for the Paper-only daily stock swing event/RS lane."""
    return (
        "stocks swing event RS pullback (versioned Paper lane)",
        _cli("stocks-swing-event-rs-pullback-paper-refresh", "--no-update"),
        "command_nonfatal",
        0,
    )


def ohlcv_archive_step() -> Step:
    """Append-only OHLCV archival (5m/15m crypto) for future path-aware replay.
    Appends the freshly-fetched rolling-cache candles into a deduped long-history
    store. Read-only w.r.t. trading; never overwrites the rolling cache. Non-fatal."""
    return (
        "ohlcv archive (5m/15m)",
        _script("scripts.archive_ohlcv_history", "--timeframes", "5m,15m"),
        "command_nonfatal",
        0,
    )


def intelligence_update_step() -> Step:
    """Shadow Intelligence Layer background update (timeline bootstrap + derivatives
    trajectory + squeeze phase for active symbols + health report). Compute happens
    here, NOT in the alert path. Read-only on the trading DB; writes only to
    data/intelligence/. Non-fatal."""
    return (
        "intelligence layer update",
        _script("scripts.intelligence_update", "--limit", "80"),
        "command_nonfatal",
        0,
    )


def context_market_risk_step() -> Step:
    return (
        "stablecoin + cross-exchange risk context",
        _cli("context-market-risk-refresh"),
        "command_nonfatal",
        0,
    )


def context_options_step() -> Step:
    return (
        "options context (IV/RV + GEX)",
        _cli("context-options-refresh"),
        "command_nonfatal",
        0,
    )


def context_token_unlock_step() -> Step:
    return (
        "token unlock context (shadow advisory)",
        _cli("context-token-unlock-refresh"),
        "command_nonfatal",
        0,
    )


def context_insider_step() -> Step:
    return (
        "SEC Form 4 insider context (shadow confirmation)",
        _cli("context-insider-refresh"),
        "command_nonfatal",
        0,
    )


def context_filters_report_step() -> Step:
    return (
        "context filters status report",
        _cli("context-filters-report"),
        "command_nonfatal",
        0,
    )


def market_intelligence_health_step() -> Step:
    return (
        "market intelligence health (alert-only)",
        _script("scripts.market_intelligence_health", "--send-telegram"),
        "command_nonfatal",
        0,
    )


def derivatives_backfill_step() -> Step:
    return (
        "derivatives funding/OI public backfill (30d)",
        _script("scripts.derivatives_backfill", "--days", "30", "--limit", "20"),
        "command_nonfatal",
        0,
    )


def market_snapshot_step() -> Step:
    """Refresh the market-dashboard snapshot (crypto/stocks mode, F&G, VIX, main-risk) each cycle so
    the Mini App Market tab never goes stale. Previously only the ~4h Opus routine wrote it, so a
    stopped routine left it 26h+ old. Display-only; no trading logic / scoring / routing. Non-fatal."""
    return (
        "market dashboard snapshot",
        _script("scripts.populate_market_dashboard_now"),
        "command_nonfatal",
        0,
    )


def paper_ledger_refresh_step() -> Step:
    """Rebuild the derived paper-portfolio ledger (equity / today+7d P&L the Mini App shows) from the
    current paper-execution outcomes. Previously only a manual/Opus run wrote it, so it froze 2 days
    after that routine stopped. Derived/read-only accounting; no live, never mutates final_r. Non-fatal."""
    return (
        "paper portfolio ledger refresh",
        _script("scripts.paper_portfolio_backfill", "--skip-execution-refresh"),
        "command_nonfatal",
        0,
    )


def monitor_heartbeat_watchdog_step() -> Step:
    """Operational watchdog for scheduler satellites.

    Runs non-fatal and diagnostic-only. With --auto-restart it can start the
    stock pre-US/RTH monitor, Telegram collector or MEXC live monitor when the
    process is absent/stale; it does not change trading decisions.
    """
    return (
        "monitor heartbeat watchdog",
        _script("scripts.monitor_heartbeat", "--event", "check", "--auto-restart"),
        "command_nonfatal",
        0,
    )


def stocks_report_steps() -> list[Step]:
    # stocks-scalp-report does not exist in this CLI — we expose a
    # placeholder so the cycle summary records "stocks scalp unavailable"
    # without exiting non-zero. The kind 'note' is handled inert.
    return [
        ("stocks scalp report", ["__note__", "stocks scalp unavailable in this CLI"],
         "note", 0),
        ("stocks intraday report", _cli("stocks-intraday-report"), "command", 0),
        ("stocks RTH plan revalidation", _cli("stocks-rth-revalidate"), "command_nonfatal", 0),
    ]


def stocks_mexc_paper_tick_step() -> Step:
    """Bridge validated stock Paper candidates into the MEXC stock-futures Paper lane.

    This is not live execution. It is the operational hand-off that was easy to
    miss when only the RTH revalidation command ran: reviewed pre-open plans and
    fresh RTH candidates must still be staged/marked/rejected by the MEXC stock
    paper adapter each cycle.
    """
    return (
        "stocks MEXC futures paper tick",
        _cli("stocks-mexc-paper-tick"),
        "command_nonfatal",
        0,
    )


def stocks_intraday_post_trade_step() -> Step:
    """SI-7 READ-MODEL: classify CLOSED stock-intraday paper trades (why won/lost/expired) from
    Model-F paper_execution_r + the actionability-gate context recorded at signal creation. Runs
    before the intraday report so its post-trade diagnostics section is fresh. Writes ONLY
    stocks_intraday_post_trade_diagnostics; never final_r / signal_outcomes / live / crypto. Non-fatal."""
    return (
        "stocks intraday post-trade classifier (read-model)",
        _cli("stocks-intraday-post-trade-refresh"),
        "command_nonfatal",
        0,
    )


def quality_agents_refresh_step() -> Step:
    """Bounded diagnostic refresh for all quality agents and matched outcomes.

    Runs on long-horizon cycles only. Live signal verdicts are already captured
    synchronously at the outbox boundary; this step only labels closed trades,
    prunes bounded telemetry and writes the effectiveness report.
    """
    return (
        "quality agents post-trade + effectiveness refresh",
        _cli("quality-agents-refresh", "--lookback-days", "30"),
        "command_nonfatal",
        0,
    )


def quality_agents_openrouter_step() -> Step:
    """Refresh cached OpenRouter advisory verdicts out-of-band.

    Live execution only reads the cache through ``llm_cached_advisory``. This
    step must stay non-fatal and must not carry model/provider slugs in the
    scheduler plan, preserving the old no-desktop-review guardrails.
    """
    return (
        "quality agents openrouter advisory cache refresh",
        _cli("quality-agents-openrouter-refresh"),
        "command_nonfatal",
        0,
    )


def llm_router_metrics_step() -> Step:
    """Emit the rolling cost/tier distribution and abnormal-share warnings."""
    return (
        "central LLM router cost and distribution monitor",
        _cli("llm-router-metrics", "--hours", "24"),
        "command_nonfatal",
        0,
    )


def _intraday_review_cycle(now: datetime) -> str:
    """Map the current UTC time to a routine review-cycle label (US RTH is 13:30–20:00 UTC)."""
    ny = now.astimezone(ZoneInfo("America/New_York"))
    minutes = ny.hour * 60 + ny.minute
    if minutes < 9 * 60 + 30:
        return "pre_open"
    if minutes < 10 * 60 + 30:
        return "after_open"
    if minutes < 15 * 60:
        return "midday"
    if minutes < 15 * 60 + 45:
        return "power_hour"
    if minutes <= 16 * 60 + 30:
        return "eod"
    return "adhoc"


def stocks_intraday_review_packet_step(now: datetime) -> Step:
    """SI-6 ADVISORY: build the scheduled stocks-intraday LLM-review PACKET (current A/B + demoted-C
    with gate reasons + post-trade diagnostics) → reports/STOCKS_INTRADAY_LLM_REVIEW_LATEST.md. The
    LLM review runs OUT-OF-BAND (routine, not realtime) — this step only assembles the packet; it does
    NOT call the LLM, create trades, change score/tier/TP/SL, or unlock live. Non-fatal."""
    cycle = _intraday_review_cycle(now)
    return (
        f"stocks intraday LLM-review packet ({cycle}, advisory)",
        _cli("stocks-intraday-review-refresh", "--cycle", cycle),
        "command_nonfatal",
        0,
    )


def _position_framework_scheduler_enabled() -> bool:
    """Read config/stocks/position_framework.yaml:scheduler_enabled. Fail-safe → False."""
    try:
        from src.stocks.position_framework.config import load_config as _pf_cfg
        return bool(_pf_cfg().get("scheduler_enabled", False))
    except Exception:
        return False


def _strategy_config_enabled(relative_path: str, section: str, flag: str) -> bool:
    """Fail-closed scheduler gate for archived strategy subprocesses."""
    try:
        import yaml

        raw = yaml.safe_load((PROJECT_ROOT / relative_path).read_text(encoding="utf-8")) or {}
        block = raw.get(section) or {}
        return bool(block.get(flag, False)) if isinstance(block, dict) else False
    except Exception:
        return False


def _position_framework_v2_scheduler_enabled() -> bool:
    """Read the isolated V2 scheduler flag. Fail-safe to False."""
    try:
        from src.stocks.position_framework.v2_config import load_config as _v2_cfg
        return bool(_v2_cfg().get("scheduler_enabled", False))
    except Exception:
        return False


def stocks_position_scan_step() -> Step:
    """Daily after-US-close shadow scan for the NEW stocks position framework
    (stocks_swing_growth_breakout). Fail-open (command_nonfatal) so a failure never blocks the
    cycle. SHADOW ONLY — no Telegram, no actionability, no live, never writes proposed_signals."""
    return (
        "stocks position framework scan (shadow, daily)",
        _cli("stocks-position-scan"),
        "command_nonfatal",
        0,
    )


def stocks_position_outcome_refresh_step() -> Step:
    """Refresh outcomes for open Stocks Position Framework shadow candidates. Separate shadow tables
    only; never proposed_signals / signal_outcomes / final_r / live."""
    return (
        "stocks position framework outcome refresh (shadow, daily)",
        _cli("stocks-position-outcome-refresh"),
        "command_nonfatal",
        0,
    )


def stocks_position_v2_scan_step() -> Step:
    """Daily isolated Stocks Position Swing V2 scan (shadow only)."""
    return (
        "stocks position swing v2 scan (shadow, daily)",
        _cli("stocks-position-v2-scan", "--no-update"),
        "command_nonfatal",
        0,
    )


def stocks_position_v2_outcome_refresh_step() -> Step:
    """Refresh isolated V2 next-session outcomes."""
    return (
        "stocks position swing v2 outcome refresh (shadow, daily)",
        _cli("stocks-position-v2-outcome-refresh", "--no-update"),
        "command_nonfatal",
        0,
    )


def stocks_position_v2_analysis_step() -> Step:
    """Build the read-only enriched-review packet for V2."""
    return (
        "stocks position swing v2 enriched packet (shadow, daily)",
        _cli("prepare-stocks-position-v2-analysis"),
        "command_nonfatal",
        0,
    )


def regime_policy_calibration_step() -> Step:
    """Refresh the read-only regime evidence report once per long cycle.

    The command only reads frozen decision/outcome history and writes Markdown.
    It cannot modify a score, Paper/live route, order, or trade table.
    """
    return (
        "market-regime policy calibration (daily, read-only)",
        _cli("regime-policy-calibration-report"),
        "command_nonfatal",
        0,
    )


def daily_long_horizon_steps(*, include_stocks: bool) -> list[Step]:
    steps: list[Step] = [
        # Disposable per-run JSON outputs are only a latest-snapshot cache. Keep
        # a bounded window so their unbounded growth cannot starve SQLite of disk.
        ("agent output retention (daily)",
         _cli("agent-outputs-retention", "--no-dry-run", "--days", "2"),
         "command_nonfatal", 0),
        # Keep the audit metadata and report path, but clear only old write-only
        # AI response duplicates. SQLite reuses these pages without a full vacuum.
        ("agent run summary retention (daily)",
         _cli("agent-runs-retention", "--no-dry-run", "--no-archive", "--days", "3"),
         "command_nonfatal", 0),
        ("signal outcome path retention (daily)",
         _cli("signal-outcomes-retention", "--no-dry-run", "--no-archive", "--days", "7",
              "--max-rows", "1000000"),
         "command_nonfatal", 0),
        ("market intelligence retention (daily)",
         _script("scripts.market_intelligence_retention", "--apply", "--max-rows-per-table", "500000"),
         "command_nonfatal", 0),
        ("live fill and rejection evidence (daily)",
         _script("scripts.live_execution_evidence"), "command_nonfatal", 0),
        regime_policy_calibration_step(),
        # On-chain risk update runs on the daily long-horizon pass only (heavier /
        # less frequent). No-op + INTERFACE_READY_CONFIG_MISSING until a provider/
        # contracts config exists. Non-fatal, background, never blocks anything.
        ("intelligence onchain risk update (daily)",
         _script("scripts.onchain_risk_update", "--limit", "40"),
        "command_nonfatal", 0),
    ]
    if _strategy_config_enabled(
        "config/crypto_swing_paper_policy.yaml", "crypto_swing_paper_policy", "enabled"
    ):
        steps.append(("crypto swing report (daily)", _cli("swing-report"), "command", 0))
    if include_stocks:
        steps.append(context_insider_step())
        # Old stocks swing/invest reports are DEPRECATED/REMOVED — no longer scheduled (they only
        # print a deprecation notice now). The NEW stocks position framework runs as a shadow-only
        # daily scan, guarded by config/stocks/position_framework.yaml:scheduler_enabled (default
        # false) and fail-open. Never blocks the cycle; no Telegram/actionability/live.
        if _position_framework_scheduler_enabled():
            steps.append(stocks_position_outcome_refresh_step())
            steps.append(stocks_position_scan_step())
            steps.append(stocks_position_outcome_refresh_step())
        else:
            steps.append(
                ("stocks position framework scan (disabled)",
                 ["__note__", "set position_framework.scheduler_enabled: true in "
                  "config/stocks/position_framework.yaml to enable the daily shadow scan"],
                 "note", 0))
        if _position_framework_v2_scheduler_enabled():
            steps.append(stocks_position_v2_outcome_refresh_step())
            steps.append(stocks_position_v2_scan_step())
            steps.append(stocks_position_v2_outcome_refresh_step())
            steps.append(stocks_position_v2_analysis_step())
        else:
            steps.append(
                ("stocks position swing v2 scan (disabled)",
                 ["__note__", "set stocks_position_swing_v2.scheduler_enabled: true in "
                  "config/stocks/position_swing_v2.yaml to enable the V2 shadow scan"],
                 "note", 0))
    return steps


def crypto_monitor_step(monitor_minutes: int) -> Step:
    """Keep the lightweight crypto re-evaluator alive across report cycles.

    The heavy scalp/intraday reports discover the broad universe.  This
    monitor re-scores the resulting C/rejected watchlist between those runs,
    so it must start before the reports and cannot be allowed to expire after
    one scheduler window.
    """
    return (
        "crypto watchlist monitor (continuous, 5m cadence, background)",
        _cli(
            "monitor-watchlist",
            "--interval", "300",
            "--duration-hours", "0",
        ),
        "crypto_monitor",
        0,
    )


def pending_monitor_step(monitor_minutes: int) -> Step:
    """Fast paper-only crypto entry detector, independent of the full monitor."""
    return (
        "crypto pending monitor (continuous, 30s cadence, background)",
        _cli(
            "pending-monitor",
            "--interval", "30",
            "--duration-hours", "0",
        ),
        "pending_monitor",
        0,
    )


def mexc_canary_monitor_step(monitor_minutes: int) -> Step:
    """Consume immutable Paper fan-out decisions; config stays dry-run by default."""
    return (
        "MEXC canary monitor (continuous, 3s cadence, background)",
        _cli(
            "mexc-canary-monitor",
            "--interval", "3",
            "--duration-hours", "0",
        ),
        "mexc_canary_monitor",
        0,
    )


def crypto_invest_forward_monitor_step() -> Step:
    """Run the isolated Regime Reclaim scanner on closed 15-minute bars."""
    return (
        "Crypto Invest regime-conditioned forward/live bridge (15m, boundary-aligned)",
        [
            sys.executable, "-m",
            "research_labs.regime_conditioned_continuation.src.forward_shadow",
            "--loop", "--workers", "12",
        ],
        "crypto_invest_forward_monitor",
        0,
    )


def mexc_parity_step() -> Step:
    """Refresh MEXC-native exit evidence separately from Paper and live orders."""
    return (
        "MEXC parity exits (shadow-only, 1m candles)",
        _cli("mexc-parity-refresh", "--limit", "30"),
        "command_nonfatal",
        0,
    )


def mexc_canary_watchdog_step() -> Step:
    """Alert on live execution safety issues without racing the continuous monitor."""
    return (
        "MEXC live execution watchdog (alert only)",
        _cli("mexc-canary-watchdog", "--no-repair", "--send-telegram"),
        "command_nonfatal",
        0,
    )


def derivatives_monitor_step(monitor_minutes: int) -> Step:
    """Two-minute funding/OI refresh, forward liquidations, and event-time
    Derivatives Reset v3 plus short-retest Shadow observation. Both ticks are
    isolated from Paper/Live and run immediately after fresh data collection."""
    duration_minutes = 24 * 60
    return (
        f"derivatives monitor ({duration_minutes} min, 2m cadence, background)",
        _script("scripts.derivatives_monitor", "--minutes", str(duration_minutes),
                "--cadence-seconds", "120"),
        "derivatives_monitor",
        duration_minutes,
    )


def fast_news_monitor_step() -> Step:
    """Keep API news off the two-hour report cadence.

    Telegram remains event-driven; this monitor only polls the small fast API
    lane. It is ingest/enrichment-only and cannot create or route a trade.
    """
    duration_minutes = 24 * 60
    return (
        f"fast Finnhub news monitor ({duration_minutes} min, 2m cadence, background)",
        _script("scripts.fast_news_monitor", "--minutes", str(duration_minutes),
                "--interval-seconds", "120"),
        "fast_news_monitor",
        duration_minutes,
    )


def stocks_monitor_step(monitor_minutes: int) -> Step:
    """Background stocks A/B alert monitor for the current cycle window.

    Re-evaluates the full stock universe every 15 minutes, including a forced
    09:10 ET pass for the public-data-only MEXC stock-futures Paper lane.
    The lightweight pending-entry tracker checks existing A/B stocks-intraday
    signals every minute during US regular session.
    It sends Telegram alerts on
    new / tier-upgrade / score-improvement / entry-change / invalidation
    events (with the 45-min cooldown from PART 2). ``--market-hours-only``
    means ticks outside 13:30–20:00 UTC Mon-Fri are no-ops, so the cost
    of running it on weekends or off-hours is essentially zero.
    """
    # The default scheduler cycles every two hours. A 26-hour session keeps
    # the prior monitor alive through the following pre-market hand-off even
    # when its replacement has not started yet.
    duration_minutes = 26 * 60
    return (
        f"stocks monitor ({duration_minutes} min, 1m pending cadence, background)",
        _cli(
            "stocks-monitor-session",
            "--minutes", str(duration_minutes),
            "--interval-minutes", "1",
            "--report-refresh-minutes", "15",
            "--market-hours-only",
            "--send-telegram",
        ),
        "stocks_monitor",
        duration_minutes,
    )


def execution_monitor_steps(*, now: datetime, crypto_only: bool,
                            monitor_minutes: int) -> list[Step]:
    """Latency-critical monitors launched near the start of every cycle."""
    steps = [
        # This must precede the heavy reports.  Otherwise a cold scheduler
        # waits for their full wall time before it can re-evaluate an existing
        # intraday watchlist candidate.
        crypto_monitor_step(monitor_minutes),
        pending_monitor_step(monitor_minutes),
        mexc_canary_monitor_step(monitor_minutes),
        mexc_parity_step(),
        derivatives_monitor_step(monitor_minutes),
        fast_news_monitor_step(),
    ]
    if _strategy_config_enabled(
        "config/crypto_invest_live.yaml", "crypto_invest_live", "enabled"
    ):
        steps.insert(3, crypto_invest_forward_monitor_step())
    if stocks_enabled(now, force_crypto_only=crypto_only):
        steps.append(stocks_monitor_step(monitor_minutes))
    if _telegram_dashboard_enabled():
        steps.append(telegram_dashboard_monitor_step())
    return steps


def bootstrap_execution_monitors(
    ctx: "RunContext", *, now: datetime | None = None,
) -> list[dict[str, Any]]:
    """Start latency-critical background workers before the heavy cycle.

    A cold boot previously reached these steps only after risk context, token
    unlock and signal tracking. Those bounded commands can legitimately take
    tens of minutes, leaving open-position reconciliation and news ingestion
    uncovered. Every launcher below is idempotent and adopts an existing
    process, so the normal cycle may safely encounter the same steps later.
    """
    moment = now or datetime.now(ZoneInfo(DEFAULT_TZ))
    launchers = {
        "crypto_monitor": start_crypto_monitor,
        "pending_monitor": start_pending_monitor,
        "mexc_canary_monitor": start_mexc_canary_monitor,
        "crypto_invest_forward_monitor": start_crypto_invest_forward_monitor,
        "derivatives_monitor": start_derivatives_monitor,
        "fast_news_monitor": start_fast_news_monitor,
        "stocks_monitor": start_stocks_monitor,
        "telegram_dashboard_monitor": start_telegram_dashboard_monitor,
    }
    results: list[dict[str, Any]] = []
    for label, argv, kind, _duration in execution_monitor_steps(
        now=moment,
        crypto_only=ctx.crypto_only,
        monitor_minutes=ctx.monitor_minutes,
    ):
        launcher = launchers.get(kind)
        if launcher is None:
            continue
        try:
            result = launcher(ctx, argv, label=label)
        except Exception as exc:  # noqa: BLE001
            ctx.logger.exception("bootstrap monitor failed: %s: %s", label, exc)
            result = {
                "label": label, "ok": False, "exit_code": -1,
                "duration_s": 0, "stdout_tail": str(exc), "attempts": 1,
            }
        results.append(result)
    return results


def support_tail_steps(*, include_stocks: bool) -> list[Step]:
    today = _utc_today_str()
    tail: list[Step] = [
        ("active-signals (crypto)",
         _cli("active-signals", "--asset-class", "crypto", "--limit", "20"),
         "command", 0),
        ("signal-stats (crypto)",
         _cli("signal-stats", "--asset-class", "crypto"),
         "command", 0),
    ]
    if include_stocks:
        tail.extend([
            ("active-signals (stocks)",
             _cli("active-signals", "--asset-class", "stocks", "--limit", "20"),
             "command", 0),
            ("signal-stats (stocks)",
             _cli("signal-stats", "--asset-class", "stocks"),
             "command", 0),
            stocks_mexc_paper_tick_step(),
        ])
    tail.extend([
        ("open intraday lifecycle review",
         _script("scripts.open_intraday_lifecycle_review"),
         "command_nonfatal", 0),
        ("untracked-legacy detector",
         _script("scripts.detect_untracked_legacy_alerts", "--since", today),
         "command", 0),
        ("track-signals (post)",
         _cli("track-signals", "--all", "--revalidate-pending"),
         "command", 0),
        monitor_heartbeat_watchdog_step(),
        crypto_live_fallback_capture_step(),
        mexc_canary_watchdog_step(),
        crypto_live_mode_audit_step(),
        strategy_governance_step(),
        # Lifecycle-aware paper-monitor status to Telegram (display only): honest
        # open/waiting/entered-unresolved/review-shadow/no-entry counts + expired
        # split, never "+0R"/"no active trades" confusion. Runs after track-signals
        # so counts are fresh. Non-fatal; 90-min cooldown prevents per-cycle spam;
        # fail-open if Telegram offline. No trade decision / execution / LLM.
        ("paper monitor status (telegram)",
         _script("scripts.paper_monitor_status", "--send-telegram", "--compact",
                 "--write-report", "--cooldown-min", "90"),
         "command_nonfatal", 0),
        ("daily review (obsidian)",
         _cli("review-day", "--no-print", "--write-obsidian"),
         "command", 0),
        # PART 8 — refresh the 8 pinned Obsidian dashboard tabs
        # (Dashboard / Active Signals / Trade History / Today's Catalysts /
        # Latest Reports / Opus Auto Reviews / Telegram Feed / Schedule
        # Status). Pure read + Markdown write — never modifies scoring.
        ("refresh obsidian dashboard",
         _script("scripts.refresh_obsidian_dashboard"),
         "command_nonfatal", 0),
        # Run after final lifecycle tracking and the regular display refreshes,
        # so the pinned UI sees the completed cycle's latest statuses.
        telegram_dashboard_refresh_step(),
    ])
    return tail


def build_cycle_steps(
    *,
    now: datetime,
    crypto_only: bool,
    include_long_horizon: bool,
    monitor_minutes: int,
    skip_reports: bool,
) -> list[Step]:
    """Compose the step list for a single cycle."""

    steps: list[Step] = []
    if skip_reports:
        # Repair the derived catalyst cache immediately on a cold/recovery
        # cycle. The full post-ingest pass below remains authoritative when
        # reports are enabled, but health must not wait behind network work.
        steps.append(catalyst_label_refresh_step())
        steps.append(context_market_risk_step())
        steps.append(context_options_step())
        if include_long_horizon:
            steps.append(context_token_unlock_step())
        steps.extend(core_pre_steps())
        steps.append(telegram_outbox_retry_step())
        steps.append(preentry_classifier_step())
        steps.extend(execution_monitor_steps(
            now=now, crypto_only=crypto_only, monitor_minutes=monitor_minutes))
    else:
        # Fast repair from already-ingested news before any heavy context or
        # tracker pass. A second post-stock pass below consumes same-cycle
        # news after resolver/materialization has completed.
        steps.append(catalyst_label_refresh_step())
        # Refresh the two authoritative execution-safety contexts before the
        # tracker can emit a new paper entry on a cold scheduler start.
        steps.append(context_market_risk_step())
        # Refresh provisional GEX/IV-RV before entry alerts. GEX remains
        # shadow-only, but its point-in-time counterfactual must predate entry.
        steps.append(context_options_step())
        if include_long_horizon:
            # Public calendar fetch is heavier, so it runs only in the daily
            # window, still before any entry alert can be emitted.
            steps.append(context_token_unlock_step())
        steps.extend(core_pre_steps())
        steps.append(telegram_outbox_retry_step())
        steps.append(preentry_classifier_step())
        steps.extend(execution_monitor_steps(
            now=now, crypto_only=crypto_only, monitor_minutes=monitor_minutes))
        steps.extend(crypto_report_steps())
        # PART 1: structured catalyst / narrative scan — non-fatal.
        # Reads news_items already populated by RSSNewsCollector;
        # writes data/catalysts/<date>/{events,baskets}.jsonl.
        # SEC EDGAR filings ingest — runs BEFORE the resolver so fresh 8-K/10-Q/S-1 filings land in
        # news_items and get resolved + catalyst-linked the same cycle (previously unscheduled → DEAD).
        steps.append(sec_edgar_refresh_step())
        # Telegram safety-net backfill (2x/day on the long-horizon pass): self-heals telegram news if the
        # live collector task is down (as it silently was 2026-07-07). It uses public pages and never opens
        # the live Telethon session. Runs before the resolver so caught-up rows get resolved/linked the same cycle.
        if include_long_horizon:
            steps.append(telegram_catchup_step(hours=24))
        # Fast bounded recovery before resolution: only targets channels with an
        # actual transport error/no-row state. Quiet editorial channels are left alone.
        steps.append(telegram_stale_recovery_step())
        # Keep the local asset inventory current. Exchange-discovered symbols
        # are visibility-only until explicitly curated.
        steps.append(news_asset_registry_step())
        # PRODUCTION news entity resolver runs FIRST so catalyst-scan / label-refresh see freshly
        # resolved detected_symbols + entity/event columns (72h per cycle; longer on the daily pass).
        steps.append(news_entity_resolve_step(hours=168 if include_long_horizon else 72))
        # Incremental post-ingest materialization is the low-latency primary
        # path; this full-window pass repairs any fail-open/journaled miss.
        steps.append(news_canonical_refresh_step(hours=168 if include_long_horizon else 72))
        steps.append(catalyst_scan_step())
        # Catalyst integrity monitor — immediately after the scan so it audits
        # the just-written baskets/events. Non-fatal, read-only.
        steps.append(catalyst_integrity_step())
        # Catalyst/news linkage refresh — re-derives news_supported and rebuilds
        # the signal_catalyst_labels cache for recent/active signals so the
        # derived labels stay current and the scan-time ~5h news window no longer
        # leaves genuine catalysts unflagged. Non-fatal, display/measurement only.
        # Paper execution accounting (Model F) — recompute the honest
        # paper_execution_r beside the legacy touch-based final_r for every
        # entered signal. PAPER/ACCOUNTING ONLY; never rewrites signal_outcomes,
        # never places orders, never changes scoring/TP/SL/entry/routing. Non-fatal.
        steps.append(paper_execution_refresh_step())
        # Structural PAPER take-profit refresh (PART 3): re-price entry-triggered
        # signals' TPs from real chart structure beside the mechanical ATR ladder.
        # PAPER ONLY; never touches production TP / final_r / scoring / entry. Non-fatal.
        steps.append(paper_tp_refresh_step())
        # Structural PAPER stop-move plan (PART 8): post-TP1/TP2 stop from chart structure.
        # PAPER ONLY; never moves a production stop / final_r. Non-fatal.
        steps.append(paper_stop_refresh_step())
        # Paper entry-mode classification (PART 4): label breakout/momentum/retest vs
        # pullback entries from real chart structure. PAPER ONLY; never touches production
        # entry / final_r / scoring / routing. Non-fatal.
        steps.append(entry_mode_refresh_step())
        # Multi-factor PAPER stock direction (PART 5): fuse EMA + VWAP + PDH/PDL + momentum +
        # RS-vs-SPY + MSTR-BTC sensitivity beside the production EMA-only call. PAPER ONLY;
        # never touches production direction / final_r / scoring / routing. Non-fatal.
        steps.append(stock_direction_refresh_step())
        # Entry-latency root-cause audit (PART 6): label late entries DATA_GAP_LATE vs
        # DETECTION_LATENCY etc. Read-only diagnostic; never touches outcomes. Non-fatal.
        steps.append(entry_latency_audit_step())
        # Paper-shadow A/B execution lane (NEXT STEP): simulate old vs new logic on the same
        # signals/OHLCV with real fees, split backfill vs forward. Measurement only; fail-open;
        # never places orders / mutates final_r / no live. Non-fatal.
        steps.append(paper_shadow_execution_step())
        steps.append(sequential_promotion_gate_step())
        # A/B also materializes stock shadow rows on weekends. This cache-only pass gives those
        # fresh rows their conservative clean/dirty verdict in the same cycle; it has no network
        # I/O and is intentionally available whenever stocks are not explicitly disabled.
        if not crypto_only:
            steps.append(stock_coverage_gate_step(prewarm=False))
        # Focused crypto intraday experiments: PULLBACK depth/hold one factor at a time;
        # BREAKOUT strong-confirmation only; MOMENTUM HALF control; LIMIT_THEN_TAKER disabled.
        # Read-model only, after fresh B outcomes, and never a promotion mechanism.
        steps.append(crypto_intraday_idea_sweep_step())
        # Crypto quality overlay: fast per-cycle cooldown recompute so the paper-entry overlay reads
        # fresh session/symbol cooldown state. Read-model only; never final_r / live. Non-fatal.
        steps.append(crypto_quality_cooldown_step())
        # Once-daily paper-shadow A/B Telegram digest (PART 2): idempotent send-if-due. Runs after
        # the shadow refresh so the digest reflects the freshest forward window. Observability only;
        # never trades / promotes B / changes scoring / final_r. Non-fatal.
        steps.append(paper_shadow_digest_step())
        # Keep the Mini App's Market snapshot + paper-portfolio equity ledger fresh every cycle so they
        # don't silently freeze when the separate ~4h Opus routine stops. Display/derived only; non-fatal.
        steps.append(market_snapshot_step())
        steps.append(paper_ledger_refresh_step())
        # Append-only OHLCV archival of the freshly-fetched candles (the reports
        # above refresh the rolling cache). Non-fatal, never touches the cache.
        steps.append(ohlcv_archive_step())
        # Shadow intelligence background update (timeline / derivatives / squeeze
        # phase) — compute outside the alert path. Non-fatal, shadow/diagnostic only.
        steps.append(intelligence_update_step())
        steps.append(context_filters_report_step())
        steps.append(market_intelligence_health_step())
        # Derivatives Reset v3 is owned by the continuous two-minute derivatives monitor above.
        if stocks_enabled(now, force_crypto_only=crypto_only):
            # SI-7: classify closed stock-intraday paper trades BEFORE the report so its post-trade
            # diagnostics section is fresh. Read-model only; never final_r / live.
            steps.append(stocks_intraday_post_trade_step())
            steps.extend(stocks_report_steps())
            # The main A/B calibration deliberately excludes this candidate lane. Evaluate it only
            # after coverage marks are current, with clean forward evidence kept separate.
            steps.append(stocks_intraday_forward_shadow_evaluation_step())
            # Fast post-ingest resolver pass: the stock reports just ingested fresh stock news AFTER the
            # main 72h resolver above, so resolve the freshly-landed rows same-cycle (trust-layer columns
            # populated promptly instead of waiting a full cycle). Idempotent/additive/non-fatal.
            steps.append(news_entity_resolve_fast_step(hours=24))
            # Repair canonical materialization too if the fail-open immediate
            # post-ingest hook journaled an error during the stock report.
            steps.append(news_canonical_refresh_step(hours=24))
            # Then refresh derived catalyst/news labels again so same-cycle stock news can affect the
            # display/measurement flags immediately. Additive 0->1 only; no score/tier/routing/live.
            steps.append(catalyst_label_refresh_post_stock_step())
            # Current stock bars, clean/dirty coverage and same-cycle canonical news are now ready.
            if _strategy_config_enabled(
                "config/shadow_stocks_catalyst_rs.yaml", "stocks_catalyst_rs", "feature_flag"
            ):
                steps.append(stocks_catalyst_rs_shadow_step())
            if _strategy_config_enabled(
                "config/shadow/stocks/earnings_gap_continuation.yaml",
                "stocks_earnings_gap_continuation",
                "feature_flag",
            ):
                steps.append(stocks_earnings_gap_shadow_step())
            # Generate the three isolated Paper lanes before the pre-US candidate
            # bundle, so the existing Enriched Review can see these signals in
            # the same scheduler cycle.
            if _strategy_config_enabled(
                "config/paper/stocks/catalyst_rs.yaml", "stocks_catalyst_rs_paper", "enabled"
            ):
                steps.append(stocks_catalyst_rs_paper_step())
            if _strategy_config_enabled(
                "config/paper/stocks/pullback_limit.yaml",
                "stocks_intraday_pullback_paper",
                "new_signals_enabled",
            ):
                steps.append(stocks_intraday_pullback_paper_step())
            if _strategy_config_enabled(
                "config/stocks/intraday_breakout_1bar_paper.yaml",
                "stocks_intraday_breakout_1bar_paper",
                "enabled",
            ):
                steps.append(stocks_intraday_breakout_1bar_paper_step())
            if _strategy_config_enabled(
                "config/paper/stocks/event_rs_pullback.yaml",
                "stocks_swing_event_rs_pullback_paper",
                "enabled",
            ):
                steps.append(stocks_swing_event_rs_pullback_paper_step())
            # The pre-US bundle is deliberately owned by its dedicated 08:50
            # ET hand-off.  Running it in this long two-hour cycle can arrive
            # after the 09:12 review deadline and overwrite the exact snapshot
            # the reviewer was meant to assess.
            # Separate research-only entry refinements. The internal cadence
            # prevents this recovery invocation from duplicating the RTH monitor.
            if _strategy_config_enabled(
                "config/shadow_stocks_intraday_variants.yaml",
                "stocks_intraday_variants",
                "feature_flag",
            ):
                steps.append(stocks_intraday_variants_shadow_step())
            # SI-6: assemble the routine (NOT realtime) stocks-intraday LLM-review packet for
            # out-of-band review. Advisory only — never calls the LLM here, never trades/promotes.
            steps.append(stocks_intraday_review_packet_step(now))
        steps.append(latency_acceptance_step())
        # Current-cycle ingestion and both resolver passes are complete. These
        # reports make content loss and high-impact mapping gaps visible without
        # changing any trade/catalyst/actionability decision.
        steps.append(news_content_coverage_step())
        steps.append(news_coverage_gaps_step())
        # Operational news watchdog after all current-cycle ingest/resolver work. It is explicitly
        # alert-only and fail-open; it never gates a report, signal, paper execution, or live path.
        steps.append(news_source_health_snapshot_step())
        steps.append(news_health_monitor_step())
        # 2026-07-13 audit: same alert-only/fail-open shape, closes the gap where this diagnostic
        # could silently go stale for days with nothing checking or alerting on it.
        steps.append(news_entity_health_step())
        steps.append(news_quality_gate_step())
        # Consume the just-refreshed news verdict alongside USD accounting,
        # guard sizing, stocks funnel and MEXC handoff telemetry.
        steps.append(paper_operational_audit_step())
        steps.append(live_funnel_report_step())
        # Cheap read-model aggregation (no OHLCV/network cost of its own); safe every cycle.
        steps.append(entry_mode_calibration_refresh_step())
        if include_long_horizon and stocks_enabled(now, force_crypto_only=crypto_only):
            # Daily/weekly PREWARM + local archive of stock OHLCV via the fallback chain — fires on the
            # 2x/day long-horizon windows so intraday delay / yfinance rolling-window stops manufacturing
            # false late entries. Fetches network; archives locally. Non-fatal.
            steps.append(stock_coverage_gate_step(prewarm=True))
        if include_long_horizon:
            # Heavier crypto quality overlay decisions + counterfactual (2x/day) → CRYPTO_QUALITY_OVERLAY.md.
            steps.append(crypto_overlay_report_step())
            steps.append(quality_agents_refresh_step())
            # OpenRouter advisory refresh and router metrics have their own
            # short 15-minute task. Keeping them here put time-sensitive cache
            # work behind hours of Paper/research maintenance.
            steps.append(crypto_swing_policy_sweep_step())
            steps.append(crypto_swing_breakout_refinement_step())
            steps.append(derivatives_backfill_step())
            steps.extend(
                daily_long_horizon_steps(
                    include_stocks=stocks_enabled(now, force_crypto_only=crypto_only)
                )
            )
    steps.extend(
        support_tail_steps(
            include_stocks=stocks_enabled(now, force_crypto_only=crypto_only)
        )
    )
    return steps


# ---------------------------------------------------------------------------
# Run context
# ---------------------------------------------------------------------------


@dataclass
class RunContext:
    send_telegram: bool
    dry_run: bool
    skip_reports: bool
    monitor_minutes: int
    crypto_only: bool
    started_at: datetime
    explicit_date: str | None = None
    logger: logging.Logger = field(default=None)

    def __post_init__(self):
        date_str = (
            self.explicit_date
            or self.started_at.astimezone(ZoneInfo(DEFAULT_TZ)).date().isoformat()
        )
        self.day_dir = (
            PROJECT_ROOT / "data" / "scheduled_runs" / f"{date_str}_default_schedule"
        )
        self.day_dir.mkdir(parents=True, exist_ok=True)
        # Monitor processes deliberately outlive a two-hour cycle and can also
        # outlive a scheduler restart.  Locks must therefore be global to the
        # service, not scoped to a date/run directory: date-scoped locks let a
        # restarted scheduler spawn a second copy of an otherwise healthy
        # monitor.  Per-day reports remain in ``day_dir`` below.
        runtime_dir = PROJECT_ROOT / "data" / "runtime_locks"
        runtime_dir.mkdir(parents=True, exist_ok=True)
        self.crypto_lock = runtime_dir / "crypto_monitor.pid"
        self.pending_lock = runtime_dir / "pending_monitor.pid"
        self.mexc_canary_lock = runtime_dir / "mexc_canary_monitor.pid"
        self.crypto_invest_forward_lock = runtime_dir / "crypto_invest_forward_monitor.pid"
        self.derivatives_lock = runtime_dir / "derivatives_monitor.pid"
        self.fast_news_lock = runtime_dir / "fast_news_monitor.pid"
        self.stocks_lock = runtime_dir / "stocks_monitor.pid"
        self.telegram_dashboard_lock = runtime_dir / "telegram_dashboard_monitor.pid"
        self.log_path = self.day_dir / "scheduler.log"
        self.cycle_results: list[dict[str, Any]] = []

        log = logging.getLogger("defaultsched")
        log.setLevel(logging.INFO)
        if not log.handlers:
            fh = logging.FileHandler(self.log_path, encoding="utf-8")
            fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
            log.addHandler(fh)
            sh = logging.StreamHandler(sys.stdout)
            sh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
            log.addHandler(sh)
        self.logger = log

    # ------------------------------------------------------------------
    # Twice-daily gate for swing / invest
    # ------------------------------------------------------------------
    #
    # PART 9 — long-horizon (swing + invest) used to run once per UTC day.
    # Now runs twice per UTC day, gated by window-aware markers:
    #   data/scheduled_runs/<date>_default_schedule/daily_<date>_window<N>.done
    # The legacy single-marker ``daily_<date>.done`` is intentionally not
    # checked anymore — backwards compatibility was not promised and the
    # window markers are scoped per UTC date so duplicate runs are blocked
    # correctly even across scheduler restarts.

    def _window_marker(self, the_date: str, window_id: int) -> Path:
        return self.day_dir / f"daily_{the_date}_window{window_id}.done"

    def long_horizon_window_done(self, the_date: str, window_id: int) -> bool:
        return self._window_marker(the_date, window_id).exists()

    def mark_long_horizon_window_done(
        self, the_date: str, window_id: int
    ) -> None:
        try:
            self._window_marker(the_date, window_id).write_text(
                f"completed at {datetime.now(timezone.utc).isoformat()}\n",
                encoding="utf-8",
            )
        except Exception as exc:  # noqa: BLE001
            self.logger.warning(
                "could not write daily marker (window=%d): %s",
                window_id, exc,
            )


# ---------------------------------------------------------------------------
# Subprocess helpers with Windows-DLL retry
# ---------------------------------------------------------------------------


def _truncate(text: str, n: int = 4000) -> str:
    if len(text) <= n:
        return text
    return text[: n // 2] + "\n…[truncated]…\n" + text[-n // 2:]


def run_command(
    ctx: RunContext,
    argv: list[str],
    *,
    label: str,
    timeout: int | None = None,
) -> dict[str, Any]:
    """Run a subprocess with Windows-DLL-init retry.

    If the process exits with ``3221225794`` (``0xC0000142``,
    ``STATUS_DLL_INIT_FAILED``) — observed in cycle 10 of the prior
    24h run — we treat it as transient: sleep 60s, retry up to 2x,
    skip after that. Each attempt is logged.
    """

    ctx.logger.info("CMD START: %s", label)
    if ctx.dry_run:
        return {
            "label": label,
            "ok": True,
            "exit_code": 0,
            "duration_s": 0,
            "stdout_tail": "(dry-run)",
            "attempts": 1,
        }

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env.setdefault("PYTHONPATH", str(PROJECT_ROOT))

    last_result: dict[str, Any] | None = None
    for attempt in range(1, DLL_RETRY_MAX + 2):
        t0 = time.monotonic()
        try:
            p = subprocess.run(
                argv,
                cwd=PROJECT_ROOT,
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
            )
            dur = time.monotonic() - t0
            out = (p.stdout or "") + (
                ("\n--STDERR--\n" + p.stderr) if p.stderr else ""
            )
            result = {
                "label": label,
                "ok": p.returncode == 0,
                "exit_code": p.returncode,
                "duration_s": round(dur, 1),
                "stdout_tail": _truncate(out),
                "attempts": attempt,
            }
            if p.returncode == WINDOWS_DLL_INIT_FAILED_EXIT:
                ctx.logger.warning(
                    "Windows DLL init transient failure for %s "
                    "(attempt %d/%d, exit=%d). Sleeping %ds and retrying.",
                    label, attempt, DLL_RETRY_MAX + 1,
                    p.returncode, DLL_RETRY_BACKOFF_SECONDS,
                )
                last_result = result
                if attempt <= DLL_RETRY_MAX:
                    time.sleep(DLL_RETRY_BACKOFF_SECONDS)
                    continue
                ctx.logger.error(
                    "Windows DLL init failure persists for %s after %d attempts — skipping step.",
                    label, attempt,
                )
                return result
            if p.returncode != 0:
                # Preserve the actual failure while the process output is still
                # available.  Previously the long-running scheduler only wrote
                # ``exit=1`` and the useful traceback disappeared with this
                # local result when a cycle was interrupted before its summary.
                ctx.logger.error(
                    "CMD OUTPUT (%s):\n%s",
                    label,
                    _truncate(out or "(no stdout/stderr)", 4000),
                )
            ctx.logger.info(
                "CMD END: %s exit=%d %.1fs (attempt %d)",
                label, p.returncode, dur, attempt,
            )
            return result
        except subprocess.TimeoutExpired as exc:
            ctx.logger.error("CMD TIMEOUT: %s", label)
            partial = ""
            for name, value in (("stdout", exc.stdout), ("stderr", exc.stderr)):
                if value:
                    if isinstance(value, bytes):
                        value = value.decode("utf-8", errors="replace")
                    partial += f"\n--{name.upper()}--\n{value}"
            if partial:
                ctx.logger.error(
                    "CMD PARTIAL OUTPUT (%s):\n%s", label, _truncate(partial, 4000)
                )
            return {
                "label": label,
                "ok": False,
                "exit_code": -1,
                "duration_s": round(time.monotonic() - t0, 1),
                "stdout_tail": _truncate(f"(timeout)\n{exc}{partial}"),
                "attempts": attempt,
            }
        except Exception as exc:  # noqa: BLE001
            ctx.logger.error("CMD FAILED: %s :: %s", label, exc)
            return {
                "label": label,
                "ok": False,
                "exit_code": -2,
                "duration_s": round(time.monotonic() - t0, 1),
                "stdout_tail": f"(exception) {exc}\n{traceback.format_exc()}",
                "attempts": attempt,
            }

    return last_result or {
        "label": label, "ok": False, "exit_code": -3, "duration_s": 0,
        "stdout_tail": "(unknown)", "attempts": DLL_RETRY_MAX + 1,
    }


def _read_lock_pid(lock: Path) -> int | None:
    if not lock.exists():
        return None
    try:
        return int(lock.read_text().strip())
    except Exception:
        return None


def _is_pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if sys.platform == "win32":
        try:
            out = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
                capture_output=True, text=True, timeout=10,
            )
            return str(pid) in (out.stdout or "")
        except Exception:
            return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _process_age_minutes(pid: int) -> float | None:
    try:
        import psutil  # type: ignore

        return max(0.0, (time.time() - psutil.Process(pid).create_time()) / 60.0)
    except Exception:
        return None


def _kill_pid(pid: int) -> None:
    if not _is_pid_alive(pid):
        return
    if sys.platform == "win32":
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(pid)],
            capture_output=True, text=True, timeout=15,
        )
    else:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            pass


def _reclaim_orphaned_monitor_leader_lock(asset_class: str, *, logger: logging.Logger) -> bool:
    """Remove an internal monitor lease only when its recorded owner is dead.

    ``pending-monitor``, MEXC and the stocks monitor have their own leader
    leases in ``.locks``.  A forced scheduler restart can leave a freshly
    timestamped lease behind even though its process is gone; the replacement
    then exits immediately and latency coverage silently disappears.  Reading
    the recorded PID and checking it is still alive makes reclamation safe:
    live owners remain authoritative.
    """
    lock = PROJECT_ROOT / ".locks" / f"pending_monitor_leader_{asset_class}.lock"
    try:
        if not lock.exists():
            return False
        holder = lock.read_text(encoding="utf-8").strip().split(maxsplit=1)
        if not holder or not holder[0].isdigit():
            return False
        owner_pid = int(holder[0])
        if _is_pid_alive(owner_pid):
            return False
        lock.unlink(missing_ok=True)
        logger.warning(
            "reclaimed orphaned %s monitor leader lease from dead pid=%d",
            asset_class, owner_pid,
        )
        return True
    except Exception as exc:  # noqa: BLE001
        logger.warning("could not inspect %s monitor leader lease: %s", asset_class, exc)
        return False


def _process_has_marker(pid: int, marker: str) -> bool | None:
    """Return whether a live Python PID is the expected monitor.

    ``None`` means process inspection is unavailable; callers then preserve
    the older conservative PID-lock behaviour. This prevents PID reuse from
    being mistaken for a healthy worker when psutil is present.
    """
    try:
        import psutil  # type: ignore
        process = psutil.Process(int(pid))
        name = str(process.name() or "").lower()
        if name not in {"python", "python.exe", "pythonw", "pythonw.exe", "py", "py.exe"}:
            return False
        return marker in " ".join(process.cmdline() or [])
    except ImportError:
        return None
    except Exception:
        return False


def _find_running_monitor(marker: str) -> int | None:
    """Find an already-running Python monitor started outside this scheduler.

    The manual/legacy service may have the real internal leader lease but no
    scheduler PID file. Adopt it instead of spawning a wasteful standby which
    competes for SQLite writes and hides latency problems.
    """
    try:
        import psutil  # type: ignore
        current_pid = os.getpid()
        for process in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                if int(process.info.get("pid") or -1) == current_pid:
                    continue
                name = str(process.info.get("name") or "").lower()
                cmd = " ".join(process.info.get("cmdline") or [])
                if (name in {"python", "python.exe", "pythonw", "pythonw.exe", "py", "py.exe"}
                        and marker in cmd):
                    return int(process.info["pid"])
            except Exception:
                continue
    except Exception:
        return None
    return None


def _start_background_monitor(
    ctx: RunContext,
    argv: list[str],
    *,
    label: str,
    lock_path: Path,
    log_prefix: str,
    pretty_name: str,
    process_marker: str | None = None,
    child_env: dict[str, str] | None = None,
    replace_after_minutes: float | None = None,
) -> dict[str, Any]:
    """Shared launcher for the background monitor processes (crypto / stocks).

    Each monitor keeps its own ``*.pid`` lock so cycles can clean stale
    children without touching the other monitor.
    """

    if ctx.dry_run:
        return {"label": label, "ok": True, "exit_code": 0, "duration_s": 0,
                "stdout_tail": "(dry-run)", "attempts": 1}
    prior = _read_lock_pid(lock_path)
    prior_alive = prior is not None and _is_pid_alive(prior)
    prior_age = _process_age_minutes(prior) if prior_alive and prior is not None else None
    if (prior_alive and replace_after_minutes is not None and prior_age is not None
            and prior_age >= replace_after_minutes):
        ctx.logger.warning(
            "%s MONITOR pid=%d exceeded %.0f min; rotating",
            pretty_name.upper(), prior, replace_after_minutes,
        )
        _kill_pid(prior)
        prior_alive = False
    if prior is not None and prior_alive and (
            process_marker is None or _process_has_marker(prior, process_marker) is not False):
        # Healthy monitors intentionally span scheduler cycles. Reusing the
        # process removes the stop/start detection gap at every two-hour turn.
        ctx.logger.info("%s MONITOR already healthy pid=%d; reusing", pretty_name.upper(), prior)
        return {"label": label, "ok": True, "exit_code": 0, "duration_s": 0,
                "stdout_tail": f"(already running pid={prior})", "attempts": 1}
    # A monitor can be intentionally launched by a previous service manager
    # or manually. If it is already the correct process, record that fact in
    # this scheduler's lock and reuse it instead of creating a standby.
    adopted = _find_running_monitor(process_marker) if process_marker else None
    if adopted is not None:
        try:
            lock_path.parent.mkdir(parents=True, exist_ok=True)
            lock_path.write_text(str(adopted), encoding="utf-8")
        except Exception:
            pass
        ctx.logger.info("%s MONITOR adopted existing pid=%d", pretty_name.upper(), adopted)
        return {"label": label, "ok": True, "exit_code": 0, "duration_s": 0,
                "stdout_tail": f"(adopted existing pid={adopted})", "attempts": 1}
    try:
        lock_path.unlink(missing_ok=True)
    except Exception:
        pass
    env = dict(child_env) if child_env is not None else os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env.setdefault("PYTHONPATH", str(PROJECT_ROOT))
    logf = ctx.day_dir / f"{log_prefix}_{int(time.time())}.log"
    try:
        flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) if sys.platform == "win32" else 0
        p = subprocess.Popen(
            argv, cwd=PROJECT_ROOT, env=env,
            stdout=open(logf, "w", encoding="utf-8"),
            stderr=subprocess.STDOUT, creationflags=flags,
        )
        lock_path.write_text(str(p.pid))
        ctx.logger.info("%s MONITOR pid=%d -> %s", pretty_name.upper(), p.pid, logf.name)
        return {"label": label, "ok": True, "exit_code": 0, "duration_s": 0,
                "stdout_tail": f"(background pid={p.pid})", "attempts": 1}
    except Exception as exc:  # noqa: BLE001
        ctx.logger.error("%s MONITOR FAILED: %s", pretty_name.upper(), exc)
        return {"label": label, "ok": False, "exit_code": -3, "duration_s": 0,
                "stdout_tail": str(exc), "attempts": 1}


def start_crypto_monitor(
    ctx: RunContext, argv: list[str], *, label: str
) -> dict[str, Any]:
    return _start_background_monitor(
        ctx, argv,
        label=label,
        lock_path=ctx.crypto_lock,
        log_prefix="crypto_monitor",
        pretty_name="crypto",
        process_marker="monitor-watchlist",
    )


def start_pending_monitor(
    ctx: RunContext, argv: list[str], *, label: str
) -> dict[str, Any]:
    _reclaim_orphaned_monitor_leader_lock("crypto", logger=ctx.logger)
    return _start_background_monitor(
        ctx, argv,
        label=label,
        lock_path=ctx.pending_lock,
        log_prefix="pending_monitor",
        pretty_name="pending",
        process_marker="pending-monitor",
    )


def start_mexc_canary_monitor(
    ctx: RunContext, argv: list[str], *, label: str
) -> dict[str, Any]:
    _reclaim_orphaned_monitor_leader_lock("mexc-canary", logger=ctx.logger)
    try:
        from scripts.monitor_heartbeat import _live_canary_child_environment
        child_env = _live_canary_child_environment()
    except Exception:
        child_env = os.environ.copy()
    return _start_background_monitor(
        ctx, argv,
        label=label,
        lock_path=ctx.mexc_canary_lock,
        log_prefix="mexc_canary_monitor",
        pretty_name="mexc-canary",
        process_marker="mexc-canary-monitor",
        child_env=child_env,
    )


def start_crypto_invest_forward_monitor(
    ctx: RunContext, argv: list[str], *, label: str
) -> dict[str, Any]:
    return _start_background_monitor(
        ctx, argv,
        label=label,
        lock_path=ctx.crypto_invest_forward_lock,
        log_prefix="crypto_invest_forward_monitor",
        pretty_name="crypto-invest-forward",
        process_marker="regime_conditioned_continuation.src.forward_shadow",
    )


def start_derivatives_monitor(
    ctx: RunContext, argv: list[str], *, label: str
) -> dict[str, Any]:
    return _start_background_monitor(
        ctx, argv,
        label=label,
        lock_path=ctx.derivatives_lock,
        log_prefix="derivatives_monitor",
        pretty_name="derivatives",
        # The real command is ``python -m scripts.derivatives_monitor``.
        # A hyphenated marker never matches it and allowed duplicate workers
        # after a scheduler restart.
        process_marker="scripts.derivatives_monitor",
        replace_after_minutes=23 * 60,
    )


def start_fast_news_monitor(
    ctx: RunContext, argv: list[str], *, label: str
) -> dict[str, Any]:
    return _start_background_monitor(
        ctx, argv,
        label=label,
        lock_path=ctx.fast_news_lock,
        log_prefix="fast_news_monitor",
        pretty_name="fast-news",
        process_marker="scripts.fast_news_monitor",
    )


def start_stocks_monitor(
    ctx: RunContext, argv: list[str], *, label: str
) -> dict[str, Any]:
    _reclaim_orphaned_monitor_leader_lock("stocks", logger=ctx.logger)
    try:
        from scripts.monitor_heartbeat import _stocks_market_data_child_environment
        child_env = _stocks_market_data_child_environment()
    except Exception:
        child_env = os.environ.copy()
    return _start_background_monitor(
        ctx, argv,
        label=label,
        lock_path=ctx.stocks_lock,
        log_prefix="stocks_monitor",
        pretty_name="stocks",
        process_marker="stocks-monitor-session",
        child_env=child_env,
    )


def start_telegram_dashboard_monitor(
    ctx: RunContext, argv: list[str], *, label: str
) -> dict[str, Any]:
    """Reuse the global dashboard poller across scheduler days and cycles."""
    global_lock = PROJECT_ROOT / "data" / "telegram" / "dashboard_state.json.poll.lock"
    existing = _read_lock_pid(global_lock)
    if existing is not None and _is_pid_alive(existing):
        identity = _process_has_marker(existing, "telegram-dashboard")
        if identity is not False:
            ctx.logger.info("TELEGRAM DASHBOARD already healthy pid=%d; reusing", existing)
            return {"label": label, "ok": True, "exit_code": 0, "duration_s": 0,
                    "stdout_tail": f"(already running pid={existing})", "attempts": 1}
        ctx.logger.warning(
            "reclaiming dashboard poll lock with reused/non-dashboard pid=%d", existing
        )
    if existing is not None:
        try:
            global_lock.unlink(missing_ok=True)
        except OSError:
            pass
    return _start_background_monitor(
        ctx, argv,
        label=label,
        lock_path=ctx.telegram_dashboard_lock,
        log_prefix="telegram_dashboard",
        pretty_name="telegram-dashboard",
        process_marker="telegram-dashboard",
    )


def send_telegram(ctx: RunContext, text: str) -> str:
    """Send a Telegram message with one ReadTimeout retry."""

    if not ctx.send_telegram or ctx.dry_run:
        return "skipped"
    capped = text if len(text) <= 3800 else text[:3700] + "\n…[truncated]…"
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from src.notifiers.telegram import TelegramNotifier  # type: ignore

        n = TelegramNotifier(PROJECT_ROOT / "config" / "notifications.yaml")
        if not n.enabled or not n.chat_id:
            return "skipped"
        for attempt in (1, 2):
            try:
                n.send(capped, parse_mode="")
                return "sent" if attempt == 1 else "sent (retry)"
            except Exception as exc:  # noqa: BLE001
                name = exc.__class__.__name__
                if "ReadTimeout" in name or "Timeout" in name:
                    ctx.logger.warning(
                        "Telegram %s on attempt %d — retrying once",
                        name, attempt,
                    )
                    if attempt == 1:
                        time.sleep(3)
                        continue
                ctx.logger.warning("Telegram send failed: %s", exc)
                return f"failed:{name}"
        return "failed:exhausted"
    except Exception as exc:  # noqa: BLE001
        ctx.logger.warning("Telegram notifier init failed: %s", exc)
        return f"failed:{exc.__class__.__name__}"


# ---------------------------------------------------------------------------
# Cycle execution
# ---------------------------------------------------------------------------


def execute_cycle(
    ctx: RunContext,
    *,
    cycle_num: int,
    total_cycles: int,
    now: datetime,
) -> dict[str, Any]:
    start = now
    tz_now = start.astimezone(ZoneInfo(DEFAULT_TZ))
    today = tz_now.date().isoformat()
    weekend = is_weekend(start)
    incl_stocks = stocks_enabled(start, force_crypto_only=ctx.crypto_only)

    # PART 9 — twice-daily gate for long-horizon (swing + invest) reports.
    # Each UTC day has two firing windows (04:00 + 16:00 EEST). A window
    # only triggers if the current cycle falls inside it AND its marker
    # has not been written yet today. Outside both windows (or once both
    # markers exist), long-horizon is skipped.
    current_window, recovery_run = due_long_horizon_window(
        start,
        is_done=lambda window_id: ctx.long_horizon_window_done(today, window_id),
    )
    include_long_horizon = current_window is not None

    ctx.logger.info("=" * 60)
    if current_window is None:
        long_horizon_label = "no (outside windows)"
    elif include_long_horizon:
        long_horizon_label = (
            f"yes ({'recovery ' if recovery_run else ''}window {current_window})"
        )
    else:
        long_horizon_label = f"no (window {current_window} already done)"
    ctx.logger.info(
        "CYCLE %d/%s START — %s, %s, %s, long_horizon=%s",
        cycle_num,
        total_cycles if total_cycles else "∞",
        tz_now.strftime("%a %Y-%m-%d %H:%M"),
        "weekend" if weekend else "weekday",
        "crypto-only" if not incl_stocks else "crypto+stocks",
        long_horizon_label,
    )
    ctx.logger.info("=" * 60)

    steps = build_cycle_steps(
        now=start,
        crypto_only=ctx.crypto_only,
        include_long_horizon=include_long_horizon,
        monitor_minutes=ctx.monitor_minutes,
        skip_reports=ctx.skip_reports,
    )
    results: list[dict[str, Any]] = []
    for label, argv, kind, duration in steps:
        try:
            if kind == "crypto_monitor":
                results.append(start_crypto_monitor(ctx, argv, label=label))
            elif kind == "pending_monitor":
                results.append(start_pending_monitor(ctx, argv, label=label))
            elif kind == "mexc_canary_monitor":
                results.append(start_mexc_canary_monitor(ctx, argv, label=label))
            elif kind == "crypto_invest_forward_monitor":
                results.append(start_crypto_invest_forward_monitor(ctx, argv, label=label))
            elif kind == "derivatives_monitor":
                results.append(start_derivatives_monitor(ctx, argv, label=label))
            elif kind == "fast_news_monitor":
                results.append(start_fast_news_monitor(ctx, argv, label=label))
            elif kind == "stocks_monitor":
                results.append(start_stocks_monitor(ctx, argv, label=label))
            elif kind == "telegram_dashboard_monitor":
                results.append(start_telegram_dashboard_monitor(ctx, argv, label=label))
            elif kind == "note":
                msg = argv[1] if len(argv) > 1 else ""
                ctx.logger.info("NOTE: %s — %s", label, msg)
                results.append({
                    "label": label, "ok": True, "exit_code": 0,
                    "duration_s": 0, "stdout_tail": msg, "attempts": 1,
                })
            elif kind == "command_nonfatal":
                # PART 1 catalyst scan: short timeout, failures logged
                # but don't count toward cycle "failed" if they're
                # transient (we still mark ok=False so summary shows
                # the issue, but Telegram doesn't escalate).
                r = run_command(
                    ctx, argv, label=label,
                    timeout=NONFATAL_TIMEOUT_OVERRIDES.get(
                        label, NONFATAL_TIMEOUT_SECONDS
                    ),
                )
                if not r.get("ok"):
                    ctx.logger.warning(
                        "non-fatal step failed: %s (exit=%s) — cycle continues",
                        label, r.get("exit_code"),
                    )
                    r["nonfatal"] = True
                results.append(r)
            else:
                # PART 14c — bumped 1500 s → 1800 s (30 min). The audit
                # window showed crypto scalp report wall-time peaking at
                # 1119 s (~19 min) and PART 14b multi-exchange fallback
                # adds one more HTTP per Binance-miss symbol; 1800 s
                # gave comfortable headroom under the 2 h interval.
                # PART 21 — the widened funnel (deep 30→40 + up to 8 reserved
                # short slots = ~48 deep symbols) raises peak wall-time;
                # bumped 1800 s → 2700 s (45 min), still well under the 2 h
                # interval, to avoid truncating a healthy wider scan.
                results.append(run_command(ctx, argv, label=label, timeout=2700))
        except Exception as exc:  # noqa: BLE001
            ctx.logger.error("STEP EXCEPTION: %s", exc)
            results.append({
                "label": label, "ok": False, "exit_code": -4,
                "duration_s": 0, "stdout_tail": f"(exception) {exc}",
                "attempts": 1,
            })

    if include_long_horizon and current_window is not None and any(
        "swing report" in r["label"] or "invest report" in r["label"]
        for r in results if r.get("ok")
    ):
        ctx.mark_long_horizon_window_done(today, current_window)

    end = datetime.now(ZoneInfo(DEFAULT_TZ))
    ok = sum(1 for r in results if r.get("ok"))
    bad = len(results) - ok

    summary_path = (
        ctx.day_dir / f"cycle_{cycle_num:02d}_{tz_now.strftime('%H-%M')}_summary.md"
    )
    lines = [
        f"# Cycle {cycle_num} ({tz_now.strftime('%a %Y-%m-%d %H:%M EEST')})",
        "",
        f"- Mode: **{'weekend (crypto-only)' if weekend or ctx.crypto_only else 'weekday (crypto+stocks)'}**",
        f"- Stocks enabled: **{incl_stocks}**",
        f"- Daily long-horizon swing/invest included: **{include_long_horizon}**",
        f"- Started: {start.isoformat()}",
        f"- Finished: {end.isoformat()}",
        f"- Steps: ok={ok} failed={bad}",
        f"- Monitor window: {ctx.monitor_minutes} min",
        "",
        "## Steps",
        "",
    ]
    for i, r in enumerate(results, start=1):
        mark = "OK" if r.get("ok") else "FAIL"
        attempts = r.get("attempts", 1)
        lines.append(
            f"### {i}. [{mark}] {r['label']} "
            f"(exit={r.get('exit_code')}, {r.get('duration_s')}s, "
            f"attempts={attempts})"
        )
        lines.append("")
        lines.append("```text")
        lines.append((r.get("stdout_tail") or "")[:5000])
        lines.append("```")
        lines.append("")
    summary_path.write_text("\n".join(lines), encoding="utf-8")

    tg = (
        f"[DEFAULT SCHED] cycle {cycle_num}/{total_cycles or '∞'} "
        f"({'weekend' if weekend else 'weekday'}, "
        f"{'stocks ON' if incl_stocks else 'crypto-only'})\n"
        f"started: {tz_now.strftime('%a %H:%M')}  "
        f"finished: {end.strftime('%H:%M')}\n"
        f"steps: ok={ok} failed={bad}  long_horizon={'yes' if include_long_horizon else 'no'}\n"
    )
    if bad:
        for r in results:
            if not r.get("ok"):
                tg += f"FAIL: {r['label']} (exit={r.get('exit_code')})\n"
    tg_status = send_telegram(ctx, tg)
    ctx.logger.info(
        "CYCLE %d END ok=%d failed=%d telegram=%s",
        cycle_num, ok, bad, tg_status,
    )

    # PART 13 (2026-06) — DO NOT kill the background monitors at end of
    # cycle. They were just spawned ~30 s ago with their configured lifetime and
    # are meant to run BETWEEN cycles (re-evaluate watchlist symbols
    # every 5 min for crypto, 10 min for stocks during US RTH). Killing
    # them here defeats the whole point and was the silent reason
    # Telegram tier-upgrade alerts stopped firing after the first wave.
    #
    # Stale survivors from a previous cycle (if a cycle takes longer than
    # the monitor lifetime) are already handled at cycle START inside
    # ``_start_background_monitor`` — it reads the lock file, kills any
    # alive PID, then spawns the new monitor. So end-of-cycle cleanup is
    # redundant AND harmful; we only log the heartbeat.
    for monitor_lock, pretty, lifetime_minutes in (
        (ctx.crypto_lock, "crypto", ctx.monitor_minutes),
        (ctx.pending_lock, "pending", max(ctx.monitor_minutes, PENDING_MONITOR_MINUTES)),
        (ctx.mexc_canary_lock, "mexc-canary", max(ctx.monitor_minutes, PENDING_MONITOR_MINUTES)),
        (ctx.crypto_invest_forward_lock, "crypto-invest-forward",
         max(ctx.monitor_minutes, PENDING_MONITOR_MINUTES)),
        (ctx.derivatives_lock, "derivatives", max(ctx.monitor_minutes, PENDING_MONITOR_MINUTES)),
        (ctx.fast_news_lock, "fast-news", max(ctx.monitor_minutes, PENDING_MONITOR_MINUTES)),
        (ctx.stocks_lock, "stocks", max(ctx.monitor_minutes, PENDING_MONITOR_MINUTES)),
    ):
        prior = _read_lock_pid(monitor_lock)
        if prior is not None and _is_pid_alive(prior):
            ctx.logger.info(
                "end-of-cycle: %s monitor pid=%d still running (lifetime ~%d min)",
                pretty, prior, lifetime_minutes,
            )

    record = {
        "cycle": cycle_num,
        "weekend": weekend,
        "stocks": incl_stocks,
        "long_horizon": include_long_horizon,
        "started": start.isoformat(),
        "finished": end.isoformat(),
        "ok": ok, "failed": bad, "telegram": tg_status,
    }
    ctx.cycle_results.append(record)
    return record


# ---------------------------------------------------------------------------
# Final review
# ---------------------------------------------------------------------------


def write_final_review(ctx: RunContext) -> Path:
    def _capture(argv: list[str]) -> str:
        try:
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env.setdefault("PYTHONPATH", str(PROJECT_ROOT))
            p = subprocess.run(
                argv, cwd=PROJECT_ROOT, env=env,
                capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=180,
            )
            return (p.stdout or "")[:2500]
        except Exception as exc:  # noqa: BLE001
            return f"(capture failed: {exc})"

    review = ctx.day_dir / "final_daily_default_schedule_review.md"
    root_review = PROJECT_ROOT / "FINAL_DAILY_DEFAULT_SCHEDULE_REVIEW.md"

    lines = [
        "# Final Daily Default-Schedule Review — "
        f"{ctx.started_at.astimezone(ZoneInfo(DEFAULT_TZ)).date()}",
        "",
        f"_Session: {ctx.started_at.isoformat()} → "
        f"{datetime.now(ZoneInfo(DEFAULT_TZ)).isoformat()}_",
        "",
        "## 1. Cycles completed",
        "",
        "| # | Mode | Long-horizon | Started | Finished | ok | failed | TG |",
        "|---|------|--------------|---------|----------|----|--------|----|",
    ]
    for r in ctx.cycle_results:
        mode = "weekend" if r["weekend"] else "weekday"
        if not r["stocks"]:
            mode += " / crypto-only"
        lines.append(
            f"| {r['cycle']} | {mode} | "
            f"{'yes' if r['long_horizon'] else 'no'} | "
            f"{r['started'][11:16]} | {r['finished'][11:16]} | "
            f"{r['ok']} | {r['failed']} | {r['telegram']} |"
        )
    today = _utc_today_str()
    lines += [
        "",
        "## 2. Final track-signals snapshot",
        "",
        "```text", _capture(_cli("track-signals", "--all")), "```",
        "",
        "## 3. Final signal-stats (crypto)",
        "",
        "```text", _capture(_cli("signal-stats", "--asset-class", "crypto")), "```",
        "",
        "## 4. Final signal-stats (stocks)",
        "",
        "```text", _capture(_cli("signal-stats", "--asset-class", "stocks")), "```",
        "",
        "## 5. Active signals — crypto",
        "",
        "```text",
        _capture(_cli("active-signals", "--asset-class", "crypto", "--limit", "40")),
        "```",
        "",
        "## 6. Active signals — stocks",
        "",
        "```text",
        _capture(_cli("active-signals", "--asset-class", "stocks", "--limit", "40")),
        "```",
        "",
        "## 7. Untracked legacy detector",
        "",
        "```text",
        _capture(_script("scripts.detect_untracked_legacy_alerts", "--since", today)),
        "```",
        "",
        "## 8. Daily review (obsidian refresh)",
        "",
        "```text",
        _capture(_cli("review-day", "--no-print", "--write-obsidian")),
        "```",
        "",
        "## 9–17. Manual interpretation",
        "",
        "- Best / worst signals: see per-cycle summaries + signal-stats above.",
        "- Crypto vs stocks balance: was the weekday cycle producing distinct stocks A/B?",
        "- Long-horizon hygiene: confirm swing/invest only ran once (`daily_*.done` marker).",
        "- Filter strictness: 0 A/B is fine in downtrend / vol-compression / weekend; investigate only if 0 A/B during a clean trend day.",
        "- Stocks legal/headline gate: PART 3 fix surfaces blocked signals in the report; verify any blocked A/B in the day's stocks report.",
        "- What to improve next: typically nothing — this scheduler is workflow hygiene only.",
        "- Final verdict: human read — the scheduler does not auto-judge tradeability.",
        "",
        "## Safety",
        "",
        "- No auto-trade.",
        "- No scoring / threshold / agent / strategy changes.",
        "- No Opus / LLM calls auto-invoked.",
        "- Telegram A/B-only gates inherited from PART 1 (registration-before-alert) + PART 2 cooldown + PART 3 legal-block.",
        "",
    ]
    content = "\n".join(lines)
    review.write_text(content, encoding="utf-8")
    root_review.write_text(content, encoding="utf-8")
    ctx.logger.info("Final review written: %s (and %s)", review, root_review)
    return review


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------


def run_loop(
    ctx: RunContext,
    *,
    total_seconds: float,
    interval_seconds: float,
    run_once: bool,
) -> None:
    deadline = ctx.started_at + timedelta(seconds=total_seconds)
    total_cycles = 0 if run_once else max(1, int(total_seconds / interval_seconds))
    ctx.logger.info(
        "default scheduler boot — total=%.0fs interval=%.0fs run_once=%s "
        "cycles=%s deadline=%s telegram=%s skip_reports=%s monitor_min=%d "
        "crypto_only=%s",
        total_seconds, interval_seconds, run_once,
        "1" if run_once else (total_cycles or "∞"),
        deadline.isoformat(), ctx.send_telegram, ctx.skip_reports,
        ctx.monitor_minutes, ctx.crypto_only,
    )
    cycle_num = 0
    next_at = datetime.now(ZoneInfo(DEFAULT_TZ))
    while True:
        now = datetime.now(ZoneInfo(DEFAULT_TZ))
        if not run_once and cycle_num > 0 and now >= deadline:
            break
        if now < next_at:
            time.sleep(min(30, (next_at - now).total_seconds()))
            continue
        cycle_num += 1
        execute_cycle(ctx, cycle_num=cycle_num, total_cycles=total_cycles, now=now)
        if run_once:
            break
        next_at = datetime.now(ZoneInfo(DEFAULT_TZ)) + timedelta(seconds=interval_seconds)
        if datetime.now(ZoneInfo(DEFAULT_TZ)) >= deadline:
            break
    write_final_review(ctx)
    ctx.logger.info("default scheduler session complete — %d cycle(s)", cycle_num)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--hours", type=float, default=24.0)
    ap.add_argument("--interval-hours", type=float, default=2.0)
    ap.add_argument("--minutes", type=float, default=None)
    ap.add_argument("--interval-minutes", type=float, default=None)
    ap.add_argument("--monitor-minutes", type=int, default=90)
    ap.add_argument(
        "--crypto-only", action="store_true",
        help="Force crypto-only even on weekdays.",
    )
    ap.add_argument(
        "--no-stocks", action="store_true",
        help="Alias for --crypto-only.",
    )
    ap.add_argument(
        "--run-once", action="store_true",
        help="Run exactly one cycle then exit. Useful for testing or "
        "manual triggers.",
    )
    ap.add_argument(
        "--date", type=str, default=None,
        help="Override today (YYYY-MM-DD). The run folder is named "
        "after this date.",
    )
    ap.add_argument(
        "--skip-reports", action="store_true",
        help="Skip the heavy report steps. Loop + tracking smoke test only.",
    )
    ap.add_argument("--dry-run", action="store_true")
    tg = ap.add_mutually_exclusive_group()
    tg.add_argument("--send-telegram", dest="send_tg", action="store_true")
    tg.add_argument("--no-send-telegram", dest="send_tg", action="store_false")
    ap.set_defaults(send_tg=True)
    args = ap.parse_args()

    crypto_only = bool(args.crypto_only) or bool(args.no_stocks)

    total_seconds = (
        (args.minutes * 60) if args.minutes is not None else (args.hours * 3600)
    )
    interval_seconds = (
        (args.interval_minutes * 60)
        if args.interval_minutes is not None
        else (args.interval_hours * 3600)
    )

    ctx = RunContext(
        send_telegram=bool(args.send_tg) and not args.dry_run,
        dry_run=args.dry_run,
        skip_reports=args.skip_reports,
        monitor_minutes=int(args.monitor_minutes),
        crypto_only=crypto_only,
        started_at=datetime.now(ZoneInfo(DEFAULT_TZ)),
        explicit_date=args.date,
    )

    if args.dry_run:
        ctx.logger.info("=== DRY RUN ===")
        n_cycles = 1 if args.run_once else max(1, int(total_seconds / interval_seconds))
        now = datetime.now(ZoneInfo(DEFAULT_TZ))
        for i in range(n_cycles):
            when = now + timedelta(seconds=interval_seconds * i)
            weekend = is_weekend(when)
            incl_stocks = stocks_enabled(when, force_crypto_only=crypto_only)
            steps = build_cycle_steps(
                now=when, crypto_only=crypto_only,
                include_long_horizon=(i == 0),
                monitor_minutes=ctx.monitor_minutes,
                skip_reports=ctx.skip_reports,
            )
            ctx.logger.info(
                "cycle %d @ %s (%s, stocks=%s, steps=%d)",
                i + 1, when.strftime("%a %H:%M"),
                "weekend" if weekend else "weekday",
                "on" if incl_stocks else "off",
                len(steps),
            )
        ctx.logger.info("--- validating CLI surface ---")
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env.setdefault("PYTHONPATH", str(PROJECT_ROOT))
        crypto_cmds = [
            "track-signals", "scalp-report", "intraday-report", "swing-report",
            "active-signals", "signal-stats", "monitor-watchlist", "pending-monitor", "review-day",
            "mexc-canary-preflight", "mexc-canary-monitor", "mexc-canary-status", "sequential-gate-report",
            "live-funnel-report",
        ]
        # Old stocks-swing-report / stocks-invest-report are DEPRECATED/REMOVED (no longer
        # scheduled); validate the NEW shadow-only stocks-position commands instead.
        stocks_cmds = [
            "stocks-intraday-report", "stocks-position-scan", "stocks-position-report",
            "stocks-position-v2-scan", "stocks-position-v2-outcome-refresh",
            "stocks-position-v2-report", "prepare-stocks-position-v2-analysis",
            "stocks-monitor-session", "stocks-intraday-forward-shadow-evaluate",
            "shadow-stocks-catalyst-rs-refresh", "shadow-stocks-earnings-gap-refresh",
            "shadow-stocks-intraday-variants-refresh",
            "stocks-catalyst-rs-paper-refresh", "stocks-intraday-pullback-paper-refresh",
            "stocks-intraday-breakout-1bar-paper-refresh",
            "stocks-swing-event-rs-pullback-paper-refresh", "paper-strategy-registry",
            "stocks-preus-candidates",
            # These are the two operational links in the pre-US -> RTH -> MEXC
            # Paper hand-off. Validate their Typer surface in dry-run as well.
            "stocks-preus-actionability-refresh", "stocks-preus-review-health",
            "stocks-rth-revalidate",
            "stocks-mexc-paper-tick",
        ]
        for cmd in crypto_cmds + stocks_cmds:
            try:
                p = subprocess.run(
                    [sys.executable, "-m", "src.cli", cmd, "--help"],
                    cwd=PROJECT_ROOT, env=env,
                    capture_output=True, text=True,
                    encoding="utf-8", errors="replace", timeout=60,
                )
                ctx.logger.info(
                    "validate %-26s %s",
                    cmd, "OK" if p.returncode == 0 else "FAIL",
                )
            except Exception as exc:  # noqa: BLE001
                ctx.logger.warning("validate %s raised %s", cmd, exc)
        # Verify scheduler does NOT auto-invoke the legacy desktop Opus/Claude review.
        rendered = " ".join(
            " ".join(s[1]) if isinstance(s[1], list) else "" for s in
            build_cycle_steps(
                now=now, crypto_only=crypto_only, include_long_horizon=True,
                monitor_minutes=ctx.monitor_minutes, skip_reports=False,
            )
        )
        forbidden = {"opus", "enriched-review", "claude api", "anthropic"}
        offenders = [w for w in forbidden if w in rendered.lower()]
        if offenders:
            ctx.logger.error("forbidden token(s) in plan: %s", offenders)
            return 2
        ctx.logger.info("--- desktop-review auto-invoke check OK (no Opus/Claude tokens in plan) ---")
        ctx.logger.info("=== dry run complete ===")
        return 0

    try:
        bootstrap_execution_monitors(ctx)
        run_loop(
            ctx,
            total_seconds=total_seconds,
            interval_seconds=interval_seconds,
            run_once=args.run_once,
        )
        return 0
    except KeyboardInterrupt:
        ctx.logger.warning("interrupted — cleaning up")
        for lock in (ctx.crypto_lock, ctx.pending_lock, ctx.mexc_canary_lock,
                     ctx.crypto_invest_forward_lock, ctx.derivatives_lock, ctx.stocks_lock):
            prior = _read_lock_pid(lock)
            if prior is not None:
                _kill_pid(prior)
            try:
                lock.unlink(missing_ok=True)
            except Exception:
                pass
        return 130
    except Exception as exc:  # noqa: BLE001
        ctx.logger.exception("fatal: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
