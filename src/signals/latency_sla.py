"""Latency SLA report (read-only, 2026-07-05).

Turns the raw `execution_latency_events` telemetry + the authoritative
`proposed_signals`/`signal_outcomes`/`entry_latency_audit` tables into an operational SLA view:
p50/p90/p95/max for each latency segment, market-data age, and DATA_GAP_LATE share — broken down by
mode (crypto scalp/intraday/swing, stocks intraday) and by source (scheduler / monitor-watchlist /
pending-monitor / stocks-monitor-session).

It is PURE OBSERVABILITY. It never changes score/tier/actionability/TP/SL/sizing and never unlocks
live. It surfaces two hard flags so latency is a first-class risk metric:
  * LIVE_BLOCKED_UNTIL_LATENCY_SLA      — always present (live is hard-locked; shown for clarity).
  * STOCKS_INTRADAY_DATA_GAP_BLOCKED    — when stocks-intraday DATA_GAP_LATE share exceeds the block.
"""
from __future__ import annotations

import re
import sqlite3
from datetime import datetime, timezone
from typing import Any

from src.config import load_config

_DEFAULT_SLA = {
    "crypto_pending_detect_p50_sec": 60,
    "crypto_pending_detect_p90_sec": 180,
    "crypto_alert_after_entry_p90_sec": 180,
    "stocks_intraday_data_gap_block_share": 0.30,
    "stocks_intraday_entry_detect_p90_sec": 300,
    "crypto_min_detect_samples": 20,
    "crypto_min_alert_samples": 10,
    "crypto_required_fast_source": "pending-monitor",
    "crypto_fast_source_min_share": 0.80,
    "stocks_intraday_min_detect_samples": 20,
    "stocks_intraday_min_alert_samples": 5,
    "stocks_required_fast_source": "stocks-monitor-session",
    "stocks_fast_source_min_share": 0.80,
    "alert_dispatch_p90_sec": 30,
    "alert_fast_path_activated_at": None,
    "signal_discovery_activated_at": None,
}

_DEFAULT_BAR_SEC = {
    ("crypto", "scalp"): 5 * 60,
    ("crypto", "intraday"): 15 * 60,
    ("crypto", "swing"): 60 * 60,
    ("stocks", "intraday"): 15 * 60,
}


def _sla_cfg() -> dict:
    try:
        import yaml
        p = load_config().root / "config" / "latency.yaml"
        data = (yaml.safe_load(p.read_text(encoding="utf-8")) or {}).get("sla") or {}
        out = dict(_DEFAULT_SLA)
        out.update({k: v for k, v in data.items() if k in _DEFAULT_SLA})
        return out
    except Exception:
        return dict(_DEFAULT_SLA)


def _conn(db=None):
    c = sqlite3.connect(db or load_config().db_path, timeout=30.0)
    c.row_factory = sqlite3.Row
    return c


def _pct(vals: list[float], q: float) -> float | None:
    v = sorted(x for x in vals if isinstance(x, (int, float)))
    if not v:
        return None
    if len(v) == 1:
        return round(float(v[0]), 1)
    # linear interpolation on rank
    idx = q * (len(v) - 1)
    lo = int(idx)
    hi = min(lo + 1, len(v) - 1)
    frac = idx - lo
    return round(v[lo] + (v[hi] - v[lo]) * frac, 1)


def _stats(vals: list[float]) -> dict:
    v = [x for x in vals if isinstance(x, (int, float))]
    return {"n": len(v), "p50": _pct(v, 0.50), "p90": _pct(v, 0.90),
            "p95": _pct(v, 0.95), "max": round(max(v), 1) if v else None}


def _parse(ts) -> datetime | None:
    if not ts:
        return None
    try:
        t = str(ts).strip().replace("Z", "+00:00")
        dt = datetime.fromisoformat(t)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def _mode_label(asset_class: str, mode: str) -> str:
    ac = "stocks" if str(asset_class or "").lower().startswith("stock") else "crypto"
    return f"{ac} {str(mode or '?').lower()}"


def _bar_seconds(event: dict) -> int:
    match = re.search(r"entry_bar_timeframe=(\d+)([mhd])", str(event.get("note") or ""))
    if match:
        scale = {"m": 60, "h": 3600, "d": 86400}[match.group(2)]
        return int(match.group(1)) * scale
    ac = "stocks" if str(event.get("asset_class") or "").lower().startswith("stock") else "crypto"
    return _DEFAULT_BAR_SEC.get((ac, str(event.get("mode") or "").lower()), 0)


def _acceptance_slice(events: list[dict], sent_events: list[dict], dispatch: list[float], *,
                      detect_p50_limit: float | None, detect_p90_limit: float,
                      min_detect: int, min_alert: int,
                      required_source: str, source_min_share: float,
                      dispatch_p90_limit: float) -> dict[str, Any]:
    def _lower_tf_touch(e: dict) -> bool:
        return bool(re.search(r"entry_touch_time_basis=lower_tf_(?:1m|5m)_first_touch",
                              str(e.get("note") or "")))

    def _current_revalidation(e: dict) -> bool:
        return "system_latency_basis=current_revalidation" in str(e.get("note") or "")

    def _legacy_revalidation(e: dict) -> bool:
        return e.get("current_price_revalidated") == 1 and not _current_revalidation(e)

    def _point_in_time(e: dict) -> bool:
        return (_current_revalidation(e)
                and e.get("current_price_revalidated") == 1
                and str(e.get("entry_time_basis") or "") in {
                    "point_in_time_current_bar", "provider_delayed_current_bar"}) or (
                        e.get("current_price_revalidated") is None and _lower_tf_touch(e)
                    )

    # A candle-open timestamp on an unresolved 1h/4h bar is neither a genuine
    # fill time nor a latency SLA sample.  Keep it in raw diagnostics, but do
    # not let it manufacture a system-latency breach.
    def _unresolved_higher_tf(e: dict) -> bool:
        return _bar_seconds(e) >= 3600 and not _point_in_time(e)

    raw = [e.get("latency_from_entry_touch_sec") for e in events
           if isinstance(e.get("latency_from_entry_touch_sec"), (int, float))]
    usable = [e for e in events
              if not _legacy_revalidation(e) and e.get("current_price_revalidated") != 0]
    lower = [max(float(e["latency_from_entry_touch_sec"]) - _bar_seconds(e), 0.0) for e in usable
             if not _unresolved_higher_tf(e)
             if isinstance(e.get("latency_from_entry_touch_sec"), (int, float))]
    exact = [float(e["latency_from_entry_touch_sec"]) for e in usable
             if _point_in_time(e)
             and isinstance(e.get("latency_from_entry_touch_sec"), (int, float))]
    raw_stats, lower_stats = _stats(raw), _stats(lower)
    exact_stats, dispatch_stats = _stats(exact), _stats(dispatch)
    detection_stats = exact_stats if exact_stats["n"] >= min_detect else lower_stats
    detection_method = ("point-in-time revalidated price" if exact_stats["n"] >= min_detect
                        else "lower-timeframe / sub-hour candle estimate")
    source_n = sum(1 for e in usable if str(e.get("source") or "") == required_source)
    source_share = round(source_n / len(usable), 3) if usable else 0.0
    breaches: list[str] = []
    insufficient: list[str] = []
    ambiguous: list[str] = []
    if detection_stats["n"] < min_detect:
        insufficient.append(f"usable detect sample {detection_stats['n']} < {min_detect}")
    else:
        if detect_p50_limit is not None and detection_stats["p50"] is not None \
                and detection_stats["p50"] > detect_p50_limit:
            breaches.append(f"detection p50 {detection_stats['p50']}s > {detect_p50_limit}s "
                            f"({detection_method})")
        if detection_stats["p90"] is not None and detection_stats["p90"] > detect_p90_limit:
            breaches.append(f"detection p90 {detection_stats['p90']}s > {detect_p90_limit}s "
                            f"({detection_method})")
        elif raw_stats["p90"] is not None and raw_stats["p90"] > detect_p90_limit:
            ambiguous.append("raw p90 breaches but lower bound passes; tick-level touch time unavailable")
        if source_share < source_min_share:
            breaches.append(f"fast-source {required_source} share {source_share:.0%} < {source_min_share:.0%}")
    if len(sent_events) < min_alert:
        insufficient.append(f"sent-alert sample {len(sent_events)} < {min_alert}")
    elif dispatch_stats["p90"] is not None and dispatch_stats["p90"] > dispatch_p90_limit:
        breaches.append(f"detect-to-alert dispatch p90 {dispatch_stats['p90']}s > "
                        f"{dispatch_p90_limit}s")
    if breaches:
        verdict = "SLA_BREACH"
    elif insufficient:
        verdict = "INSUFFICIENT_SAMPLE"
    elif ambiguous:
        verdict = "CANDLE_RESOLUTION_AMBIGUOUS"
    else:
        verdict = "PASS"
    return {"verdict": verdict, "raw_touch_to_detect_sec": raw_stats,
            "after_bar_close_lower_bound_sec": lower_stats,
            "point_in_time_detect_sec": exact_stats,
            "acceptance_detection_sec": detection_stats,
            "detect_to_alert_dispatch_sec": dispatch_stats,
            "sent_alerts": len(sent_events), "required_fast_source": required_source,
            "fast_source_share": source_share, "breaches": breaches,
            "insufficient": insufficient, "ambiguities": ambiguous,
            "method": detection_method,
            "legacy_revalidation_excluded": sum(1 for e in events if _legacy_revalidation(e)),
            "non_actionable_unrevalidated_excluded": sum(
                1 for e in events if e.get("current_price_revalidated") == 0
            )}


def sla_report(db=None, *, recent_days: int = 7, now: datetime | None = None) -> dict[str, Any]:
    """Compute the SLA view. Read-only; safe on empty/missing tables."""
    now = now or datetime.now(timezone.utc)
    from datetime import timedelta
    cutoff = (now - timedelta(days=int(recent_days))).isoformat()
    sla = _sla_cfg()

    conn = _conn(db)
    try:
        # 1) Authoritative signal→entry latency from proposed_signals + latest outcome.
        try:
            sig_cols = {r[1] for r in conn.execute("PRAGMA table_info(proposed_signals)")}
            tier_col = ", tier" if "tier" in sig_cols else ", NULL AS tier"
            sig_rows = [dict(r) for r in conn.execute(
                "SELECT signal_id, symbol, mode, asset_class, created_at" + tier_col
                + " FROM proposed_signals").fetchall()]
        except sqlite3.OperationalError:
            sig_rows = []
        sig_by_id = {r["signal_id"]: r for r in sig_rows}
        recent_signal_ids = [str(r["signal_id"]) for r in sig_rows
                             if str(r.get("created_at") or "") >= cutoff]
        try:
            # ONE entry per signal_id (the earliest entry_triggered_at) — signal_outcomes has many
            # rows per signal (one per tracker tick); counting them all would weight by check-count.
            out_rows = []
            for start in range(0, len(recent_signal_ids), 400):
                batch = recent_signal_ids[start:start + 400]
                if not batch:
                    continue
                placeholders = ",".join("?" for _ in batch)
                out_rows.extend(dict(r) for r in conn.execute(
                    "SELECT signal_id, MIN(entry_triggered_at) AS entry_triggered_at "
                    "FROM signal_outcomes WHERE signal_id IN (" + placeholders + ") "
                    "AND entry_triggered=1 AND entry_triggered_at IS NOT NULL GROUP BY signal_id",
                    batch,
                ).fetchall())
        except sqlite3.OperationalError:
            out_rows = []
        # 2) entry_latency_audit for DATA_GAP_LATE share by mode.
        try:
            ela_cols = {r[1] for r in conn.execute("PRAGMA table_info(entry_latency_audit)")}
            snapshot_expr = ("snapshot_kind" if "snapshot_kind" in ela_cols
                             else "NULL AS snapshot_kind")
            ela = [dict(r) for r in conn.execute(
                "SELECT signal_id, symbol, asset_class, mode, cause, data_gap_min, "
                f"recorded_latency_min, created_at, {snapshot_expr} FROM entry_latency_audit "
                "WHERE created_at>=?", (cutoff,)).fetchall()]
        except sqlite3.OperationalError:
            ela = []
        # 3) telemetry events (finer segments + source breakdown).
        try:
            tel = [dict(r) for r in conn.execute(
                "SELECT * FROM execution_latency_events WHERE event_at>=?", (cutoff,)).fetchall()]
        except sqlite3.OperationalError:
            tel = []
    finally:
        conn.close()

    # =====================================================================
    # MARKET WAIT (NOT system latency, NOT an SLA breach): created_at → first
    # entry_triggered_at. This is how long the market took to reach the entry — dominated by price
    # action, not by our system. Approximated from the candle timestamp (no true tick).
    # =====================================================================
    market_wait_by_mode: dict[str, list[float]] = {}
    market_wait_overall: list[float] = []
    for o in out_rows:
        sig = sig_by_id.get(o["signal_id"])
        if not sig or str(sig.get("created_at") or "") < cutoff:
            continue
        c0, e1 = _parse(sig.get("created_at")), _parse(o.get("entry_triggered_at"))
        if not c0 or not e1:
            continue
        secs = max((e1 - c0).total_seconds(), 0.0)
        label = _mode_label(sig.get("asset_class"), sig.get("mode"))
        market_wait_by_mode.setdefault(label, []).append(secs)
        market_wait_overall.append(secs)

    # =====================================================================
    # SYSTEM LATENCY (the SLA basis): derived from telemetry, DEDUPED per signal_id (earliest event)
    # so a repeated tick can't skew percentiles, and SENT-ONLY for the alert leg (skipped/failed and
    # duplicate rows never count).
    #   * system_detection_sec = entry_condition_detected.latency_from_entry_touch_sec (touch→detect)
    #   * entry_to_alert_sec    = paper_entry_alert_sent.latency_from_entry_touch_sec (entry→alert)
    #   * alert_dispatch_sec    = detected.event_at → sent.event_at (per signal)
    # =====================================================================
    tel_recent = [t for t in tel if str(t.get("event_at") or "") >= cutoff]

    def _dedup_by_signal(event_type: str) -> dict[str, dict]:
        best: dict[str, dict] = {}
        for t in tel_recent:
            if t.get("event_type") != event_type or not t.get("signal_id"):
                continue
            sid = str(t["signal_id"])
            ea = str(t.get("event_at") or "")
            if sid not in best or ea < best[sid].get("_ea", "~"):
                d = dict(t); d["_ea"] = ea; best[sid] = d
        return best

    discovered = _dedup_by_signal("pending_signal_discovered")
    strategy_ready = _dedup_by_signal("strategy_entry_ready")
    detected = _dedup_by_signal("entry_condition_detected")
    decision_completed = _dedup_by_signal("paper_entry_decision_completed")
    sent = _dedup_by_signal("paper_entry_alert_sent")   # only real sends are ever this type post-fix
    queued = _dedup_by_signal("paper_entry_alert_queued")
    mexc_captured = _dedup_by_signal("mexc_decision_captured")
    mexc_preflight = _dedup_by_signal("mexc_preflight_started")
    mexc_submitted = _dedup_by_signal("mexc_order_submitted")

    sys_detect_by_mode: dict[str, list[float]] = {}
    entry_to_alert_by_mode: dict[str, list[float]] = {}
    alert_dispatch_by_mode: dict[str, list[float]] = {}
    sys_detect_overall: list[float] = []
    entry_to_alert_overall: list[float] = []
    discovery_cutover = _parse(sla.get("signal_discovery_activated_at"))
    discovery_overall = [
        float(e["latency_from_signal_sec"]) for e in discovered.values()
        if isinstance(e.get("latency_from_signal_sec"), (int, float))
        and (
            discovery_cutover is None
            or (_parse((sig_by_id.get(str(e.get("signal_id") or "")) or {}).get("created_at"))
                or datetime.min.replace(tzinfo=timezone.utc)) >= discovery_cutover
        )
    ]
    strategy_wait_overall = [float(e["latency_from_signal_sec"]) for e in strategy_ready.values()
                             if isinstance(e.get("latency_from_signal_sec"), (int, float))]
    strategy_ready_to_detect = [float(e["latency_from_strategy_ready_sec"]) for e in detected.values()
                                if isinstance(e.get("latency_from_strategy_ready_sec"), (int, float))]
    decision_runtime = [float(e["stage_runtime_ms"]) for e in decision_completed.values()
                        if isinstance(e.get("stage_runtime_ms"), (int, float))]
    detect_to_mexc_capture: list[float] = []
    mexc_queue_to_preflight: list[float] = []
    mexc_preflight_to_submit: list[float] = []
    # system detection = entry_condition_detected (touch→detect)
    for sid, d in detected.items():
        label = _mode_label(d.get("asset_class"), d.get("mode"))
        v = d.get("latency_from_entry_touch_sec")
        if isinstance(v, (int, float)):
            sys_detect_by_mode.setdefault(label, []).append(v)
            sys_detect_overall.append(v)
    # entry→alert = paper_entry_alert_sent (SENT-only, deduped) — independent of a detect row;
    # alert_dispatch = detected→sent when both exist.
    for sid, s in sent.items():
        label = _mode_label(s.get("asset_class"), s.get("mode"))
        av = s.get("latency_from_entry_touch_sec")
        if isinstance(av, (int, float)):
            entry_to_alert_by_mode.setdefault(label, []).append(av)
            entry_to_alert_overall.append(av)
        d = detected.get(sid)
        if d:
            dd, sd = _parse(d.get("event_at")), _parse(s.get("event_at"))
            if dd and sd:
                alert_dispatch_by_mode.setdefault(label, []).append(max((sd - dd).total_seconds(), 0.0))

    for sid, captured in mexc_captured.items():
        detected_at = _parse((detected.get(sid) or {}).get("event_at"))
        captured_at = _parse(captured.get("event_at"))
        preflight_at = _parse((mexc_preflight.get(sid) or {}).get("event_at"))
        submitted_at = _parse((mexc_submitted.get(sid) or {}).get("event_at"))
        if detected_at and captured_at:
            detect_to_mexc_capture.append(max((captured_at - detected_at).total_seconds(), 0.0))
        if captured_at and preflight_at:
            mexc_queue_to_preflight.append(max((preflight_at - captured_at).total_seconds(), 0.0))
        if preflight_at and submitted_at:
            mexc_preflight_to_submit.append(max((submitted_at - preflight_at).total_seconds(), 0.0))

    # scheduler / data freshness signals (aggregate; no per-signal identity needed)
    md_age_all = [t.get("market_data_age_sec") for t in tel_recent
                  if isinstance(t.get("market_data_age_sec"), (int, float))]
    scheduler_delay_all = [t.get("market_data_age_sec") for t in tel_recent
                           if t.get("event_type") == "market_data_refreshed"
                           and isinstance(t.get("market_data_age_sec"), (int, float))]

    by_source: dict[str, dict] = {}
    for sid, s in sent.items():
        src = str(s.get("source") or "?")
        by_source.setdefault(src, {"sent": 0, "entry_to_alert": []})
        by_source[src]["sent"] += 1
        av = s.get("latency_from_entry_touch_sec")
        if isinstance(av, (int, float)):
            by_source[src]["entry_to_alert"].append(av)

    # ---- DATA_GAP_LATE share by mode (from entry_latency_audit) ----
    dgl_by_mode: dict[str, dict] = {}
    has_stock_tiers = any(
        str(r.get("asset_class") or "").lower().startswith("stock")
        and str(r.get("tier") or "").upper() in {"A", "B", "C"}
        for r in sig_rows
    )
    for r in ela:
        # Do not let old rolling-cache backfills contaminate a current SLA
        # window. The row belongs to the window of its signal, not the day on
        # which a diagnostic refresh happened to recompute it.
        if str(r.get("created_at") or "") < cutoff:
            continue
        label = _mode_label(r.get("asset_class"), r.get("mode"))
        if label == "stocks intraday" and has_stock_tiers:
            tier = str((sig_by_id.get(r.get("signal_id")) or {}).get("tier") or "").upper()
            if tier not in {"A", "B"}:
                continue
        g = dgl_by_mode.setdefault(label, {"n": 0, "dgl": 0})
        g["n"] += 1
        if r.get("cause") == "DATA_GAP_LATE":
            g["dgl"] += 1

    modes = sorted(set(market_wait_by_mode) | set(sys_detect_by_mode) | set(dgl_by_mode)
                   | set(entry_to_alert_by_mode))
    by_mode = []
    for m in modes:
        dgl = dgl_by_mode.get(m, {"n": 0, "dgl": 0})
        share = round(dgl["dgl"] / dgl["n"], 3) if dgl["n"] else None
        by_mode.append({
            "mode": m,
            # Signal -> entry is the age of a plan while price/strategy waited.
            # It is retained for research but is never an execution SLA.
            "plan_age_to_entry_sec": _stats(market_wait_by_mode.get(m, [])),
            "market_wait_sec": _stats(market_wait_by_mode.get(m, [])),          # legacy alias, NOT an SLA metric
            "system_detection_sec": _stats(sys_detect_by_mode.get(m, [])),      # SLA: crypto detect
            "entry_to_alert_sec": _stats(entry_to_alert_by_mode.get(m, [])),    # SLA: alert (sent)
            "alert_dispatch_sec": _stats(alert_dispatch_by_mode.get(m, [])),
            "data_gap_late_share": share, "data_gap_late_n": dgl["n"],
        })

    def _dispatch_for(sent_subset: list[dict]) -> list[float]:
        vals: list[float] = []
        for event in sent_subset:
            prior = detected.get(str(event.get("signal_id") or ""))
            dd, sd = _parse((prior or {}).get("event_at")), _parse(event.get("event_at"))
            if dd and sd:
                vals.append(max((sd - dd).total_seconds(), 0.0))
        return vals

    crypto_detect = [e for e in detected.values()
                     if not str(e.get("asset_class") or "").lower().startswith("stock")]
    crypto_sent = [e for e in sent.values()
                   if not str(e.get("asset_class") or "").lower().startswith("stock")]
    stock_detect_all = [e for e in detected.values()
                        if str(e.get("asset_class") or "").lower().startswith("stock")
                        and str(e.get("mode") or "").lower() == "intraday"]
    stock_sent_all = [e for e in sent.values()
                      if str(e.get("asset_class") or "").lower().startswith("stock")
                      and str(e.get("mode") or "").lower() == "intraday"]
    stock_tier_scope_available = any(
        str(row.get("asset_class") or "").lower().startswith("stock")
        and str(row.get("tier") or "").upper() in {"A", "B", "C"}
        for row in sig_rows
    )

    def _stock_live_cohort(event: dict) -> bool:
        signal = sig_by_id.get(str(event.get("signal_id") or "")) or {}
        tier = str(signal.get("tier") or "").upper()
        return not stock_tier_scope_available or tier in {"A", "B"}

    stock_detect = [e for e in stock_detect_all if _stock_live_cohort(e)]
    stock_sent = [e for e in stock_sent_all if _stock_live_cohort(e)]
    stock_non_live_tier_excluded = len(stock_detect_all) - len(stock_detect)
    fast_path_cutover = _parse(sla.get("alert_fast_path_activated_at"))
    cutover_active = bool(fast_path_cutover and now >= fast_path_cutover)

    def _post_fast_path(events: list[dict]) -> list[dict]:
        if not cutover_active:
            return events
        return [event for event in events
                if (_parse(event.get("event_at")) or datetime.min.replace(tzinfo=timezone.utc))
                >= fast_path_cutover]

    crypto_sent_acceptance = _post_fast_path(crypto_sent)
    stock_sent_acceptance = _post_fast_path(stock_sent)
    acceptance = {
        "crypto": _acceptance_slice(
            crypto_detect, crypto_sent_acceptance, _dispatch_for(crypto_sent_acceptance),
            detect_p50_limit=float(sla["crypto_pending_detect_p50_sec"]),
            detect_p90_limit=float(sla["crypto_pending_detect_p90_sec"]),
            min_detect=int(sla["crypto_min_detect_samples"]),
            min_alert=int(sla["crypto_min_alert_samples"]),
            required_source=str(sla["crypto_required_fast_source"]),
            source_min_share=float(sla["crypto_fast_source_min_share"]),
            dispatch_p90_limit=float(sla["alert_dispatch_p90_sec"]),
        ),
        "stocks_intraday": _acceptance_slice(
            stock_detect, stock_sent_acceptance, _dispatch_for(stock_sent_acceptance),
            detect_p50_limit=None,
            detect_p90_limit=float(sla["stocks_intraday_entry_detect_p90_sec"]),
            min_detect=int(sla["stocks_intraday_min_detect_samples"]),
            min_alert=int(sla["stocks_intraday_min_alert_samples"]),
            required_source=str(sla["stocks_required_fast_source"]),
            source_min_share=float(sla["stocks_fast_source_min_share"]),
            dispatch_p90_limit=float(sla["alert_dispatch_p90_sec"]),
        ),
    }
    stock_mode = next((m for m in by_mode if m["mode"] == "stocks intraday"), None)
    stock_dgl_share = stock_mode.get("data_gap_late_share") if stock_mode else None
    stock_dgl_n = stock_mode.get("data_gap_late_n", 0) if stock_mode else 0
    acceptance["stocks_intraday"]["actionable_data_gap_late_share"] = stock_dgl_share
    acceptance["stocks_intraday"]["actionable_data_gap_late_n"] = stock_dgl_n
    acceptance["stocks_intraday"]["non_live_tier_excluded"] = stock_non_live_tier_excluded
    for value in acceptance.values():
        value["alert_fast_path_activated_at"] = (
            fast_path_cutover.isoformat() if cutover_active and fast_path_cutover else None
        )
    if stock_dgl_share is not None and stock_dgl_share > sla["stocks_intraday_data_gap_block_share"]:
        acceptance["stocks_intraday"]["breaches"].append(
            f"actionable A/B DATA_GAP_LATE {stock_dgl_share:.0%} > "
            f"{sla['stocks_intraday_data_gap_block_share']:.0%}")
        acceptance["stocks_intraday"]["verdict"] = "SLA_BREACH"
    try:
        from src.stocks.realtime_provider import active_provider
        provider = active_provider()
        acceptance["stocks_intraday"]["provider"] = provider.to_dict()
        acceptance["stocks_intraday"]["live_acceptance"] = (
            "LATENCY_AND_PROVIDER_ACCEPTED" if provider.live_grade
            and acceptance["stocks_intraday"]["verdict"] == "PASS"
            else "BLOCKED_NOT_LIVE_GRADE" if not provider.live_grade
            else "BLOCKED_LATENCY"
        )
    except Exception:
        acceptance["stocks_intraday"]["live_acceptance"] = "BLOCKED_PROVIDER_UNKNOWN"

    # if we have market-wait rows but NO forward telemetry, we cannot judge system latency yet.
    insufficient = (len(sys_detect_overall) + len(entry_to_alert_overall)) == 0

    # ---- SLA flags (system latency only; market wait NEVER breaches) ----
    flags: list[str] = ["LIVE_BLOCKED_UNTIL_LATENCY_SLA"]
    breaches: list[str] = []
    raw_candle_diagnostics: list[str] = []
    stocks_intraday = next((m for m in by_mode if m["mode"] == "stocks intraday"), None)
    if stocks_intraday and stocks_intraday["data_gap_late_share"] is not None and \
            stocks_intraday["data_gap_late_share"] > sla["stocks_intraday_data_gap_block_share"]:
        flags.append("STOCKS_INTRADAY_DATA_GAP_BLOCKED")
        breaches.append(
            f"stocks intraday DATA_GAP_LATE share {int(stocks_intraday['data_gap_late_share']*100)}% "
            f"> {int(sla['stocks_intraday_data_gap_block_share']*100)}% block threshold")
    if insufficient:
        flags.append("INSUFFICIENT_FORWARD_TELEMETRY")
    else:
        for m in by_mode:
            if m["mode"].startswith("crypto"):
                sd = m["system_detection_sec"]
                if sd["p50"] is not None and sd["p50"] > sla["crypto_pending_detect_p50_sec"]:
                    raw_candle_diagnostics.append(
                        f"{m['mode']} raw bar-open detect p50 {sd['p50']}s > "
                        f"{sla['crypto_pending_detect_p50_sec']}s target")
                if sd["p90"] is not None and sd["p90"] > sla["crypto_pending_detect_p90_sec"]:
                    raw_candle_diagnostics.append(
                        f"{m['mode']} raw bar-open detect p90 {sd['p90']}s > "
                        f"{sla['crypto_pending_detect_p90_sec']}s target")
            al = m["entry_to_alert_sec"]
            if m["mode"].startswith("crypto") and al["p90"] is not None \
                    and al["p90"] > sla["crypto_alert_after_entry_p90_sec"]:
                raw_candle_diagnostics.append(
                    f"{m['mode']} raw bar-open entry→alert p90 {al['p90']}s > "
                    f"{sla['crypto_alert_after_entry_p90_sec']}s target")
    for key, label in (("crypto", "crypto"), ("stocks_intraday", "stocks intraday")):
        breaches.extend(f"{label}: {reason}" for reason in acceptance[key]["breaches"])
    flags.extend([
        f"CRYPTO_LATENCY_ACCEPTANCE_{acceptance['crypto']['verdict']}",
        f"STOCKS_INTRADAY_LATENCY_ACCEPTANCE_{acceptance['stocks_intraday']['verdict']}",
    ])

    return {
        "available": bool(market_wait_overall or tel_recent or ela),
        "recent_days": recent_days, "sla_thresholds": sla,
        "approx_from_candle_timestamp": True,
        "insufficient_forward_telemetry": insufficient,
        # PLAN AGE / MARKET WAIT — informational, NOT judged against SLA
        "plan_age_to_entry_sec": _stats(market_wait_overall),
        "market_wait_sec": _stats(market_wait_overall),
        "signal_discovery_sec": _stats(discovery_overall),
        "strategy_wait_sec": _stats(strategy_wait_overall),
        "strategy_ready_to_detect_sec": _stats(strategy_ready_to_detect),
        "paper_decision_runtime_ms": _stats(decision_runtime),
        # SYSTEM LATENCY — the SLA basis
        "system_detection_sec": _stats(sys_detect_overall),
        "entry_to_alert_sec": _stats(entry_to_alert_overall),
        "detect_to_mexc_capture_sec": _stats(detect_to_mexc_capture),
        # Backward-compatible alias for older dashboard/report readers.  The
        # basis is detect -> capture; capture deliberately precedes Telegram.
        "paper_to_mexc_capture_sec": _stats(detect_to_mexc_capture),
        "mexc_queue_to_preflight_sec": _stats(mexc_queue_to_preflight),
        "mexc_preflight_to_submit_sec": _stats(mexc_preflight_to_submit),
        # Explicit grouping for consumers which must never mistake a strategy
        # wait for an execution delay.
        "execution_latency": {
            "system_detection_sec": _stats(sys_detect_overall),
            "entry_to_alert_sec": _stats(entry_to_alert_overall),
            "detect_to_mexc_capture_sec": _stats(detect_to_mexc_capture),
            "mexc_queue_to_preflight_sec": _stats(mexc_queue_to_preflight),
            "mexc_preflight_to_submit_sec": _stats(mexc_preflight_to_submit),
        },
        "market_data_age_sec": _stats(md_age_all),
        "scheduler_delay_sec": _stats(scheduler_delay_all),
        "by_mode": by_mode,
        "acceptance": acceptance,
        "by_source": {k: {"sent": v["sent"], "entry_to_alert_sec": _stats(v["entry_to_alert"])}
                      for k, v in sorted(by_source.items())},
        "telemetry_events_recent": len(tel_recent),
        "sent_alert_events": len(sent), "queued_alert_events": len(queued),
        "detected_events": len(detected), "discovered_events": len(discovered),
        "alert_fast_path_activated_at": (
            fast_path_cutover.isoformat() if cutover_active and fast_path_cutover else None
        ),
        "flags": flags, "sla_breaches": breaches,
        "raw_candle_diagnostics": raw_candle_diagnostics,
        "note": "READ-ONLY latency SLA. Market wait is price action (not judged); SLA uses SYSTEM "
                "latency from deduped, sent-only telemetry. Never changes execution/score/tier/"
                "sizing; never unlocks live.",
    }


def render_markdown(db=None, *, recent_days: int = 7) -> str:
    r = sla_report(db, recent_days=recent_days)
    lines = ["## Latency SLA report (read-only - general live promotion blocked; MEXC canary separately gated)"]
    if not r.get("available"):
        # Keep older market-wait context visible when only the recent window
        # is empty; system latency remains explicitly insufficient.
        historic = sla_report(db, recent_days=36500)
        if historic.get("available"):
            r = historic
            lines.append(f"- no rows in the recent {recent_days}d window; showing all-history context.")
        else:
            lines.append("- no latency data yet (run the pending monitor / track-signals to populate).")
            lines.append(f"- {', '.join(r['flags'])}")
            return "\n".join(lines)
    plan_age = r.get("plan_age_to_entry_sec") or r["market_wait_sec"]
    discovery = r.get("signal_discovery_sec") or _stats([])
    strategy_wait = r.get("strategy_wait_sec") or _stats([])
    ready_detect = r.get("strategy_ready_to_detect_sec") or _stats([])
    decision_runtime = r.get("paper_decision_runtime_ms") or _stats([])
    sd = r["system_detection_sec"]
    ea = r["entry_to_alert_sec"]
    pc = r["paper_to_mexc_capture_sec"]
    qp = r["mexc_queue_to_preflight_sec"]
    ps = r["mexc_preflight_to_submit_sec"]
    a = r["market_data_age_sec"]
    lines.append("_Plan age = price/strategy wait (NOT an SLA metric). Historical touch→event records include retrospective observations. Actionable SLA requires current-price revalidation; alert dispatch is measured separately._")
    lines.append(f"- PLAN AGE signal→entry (n {plan_age['n']}, price/strategy wait only): "
                 f"p50 {_mins(plan_age['p50'])} · p90 {_mins(plan_age['p90'])} · max {_mins(plan_age['max'])}")
    lines.append(f"- OBSERVED touch→event (all detections, n {sd['n']}): "
                 f"p50 {_secs(sd['p50'])} · p90 {_secs(sd['p90'])} · "
                 f"p95 {_secs(sd['p95'])} · max {_secs(sd['max'])}")
    lines.append(f"- SYSTEM entry→alert (sent-only, n {ea['n']}): "
                 f"p50 {_secs(ea['p50'])} · p90 {_secs(ea['p90'])} · max {_secs(ea['max'])}")
    lines.append(f"- market-data age: p50 {_secs(a['p50'])} · p90 {_secs(a['p90'])} "
                 f"(telemetry {r['telemetry_events_recent']}, sent {r['sent_alert_events']})")
    lines.append(f"- MEXC handoff: Paper-to-capture p90 {_secs(pc['p90'])} (n{pc['n']}) · "
                 f"queue-to-preflight p90 {_secs(qp['p90'])} (n{qp['n']}) · "
                 f"preflight-to-submit p90 {_secs(ps['p90'])} (n{ps['n']})")
    lines.append(f"- ROSTER signal->fast monitor (n {discovery['n']}): "
                 f"p50 {_secs(discovery['p50'])}, p90 {_secs(discovery['p90'])}")
    lines.append(f"- STRATEGY WAIT signal->executable setup (n {strategy_wait['n']}): "
                 f"p50 {_mins(strategy_wait['p50'])}, p90 {_mins(strategy_wait['p90'])}")
    lines.append(f"- SYSTEM ready->detect (n {ready_detect['n']}): "
                 f"p50 {_secs(ready_detect['p50'])}, p90 {_secs(ready_detect['p90'])}")
    lines.append(f"- Paper decision runtime (n {decision_runtime['n']}): "
                 f"p50 {decision_runtime['p50']}ms, p90 {decision_runtime['p90']}ms")
    if r.get("insufficient_forward_telemetry"):
        lines.append("- NOTE: insufficient_forward_telemetry — not enough forward telemetry to judge "
                     "SYSTEM latency SLA yet (market-wait shown for context; run pending-monitor forward).")
    lines.append("")
    lines.append("**Current acceptance (crypto and stocks are independent):**")
    for key, label in (("crypto", "crypto"), ("stocks_intraday", "stocks intraday")):
        acc = r["acceptance"][key]
        raw = acc["raw_touch_to_detect_sec"]
        lower = acc["after_bar_close_lower_bound_sec"]
        exact = acc["point_in_time_detect_sec"]
        accepted = acc["acceptance_detection_sec"]
        dispatch = acc["detect_to_alert_dispatch_sec"]
        lines.append(
            f"- {label}: **{acc['verdict']}** · raw detect p90 {raw['p90']}s (n{raw['n']}) · "
            f"point-in-time p90 {_secs(exact['p90'])} (n{exact['n']}) · "
            f"accepted detect p90 {_secs(accepted['p90'])} ({acc['method']}) · "
            f"legacy lower-bound p90 {_secs(lower['p90'])} · "
            f"dispatch p90 {_secs(dispatch['p90'])} "
            f"(sent n{acc['sent_alerts']}) · fast-source share {acc['fast_source_share']:.0%}")
        lines.append(
            f"  - excluded from actionable SLA: "
            f"{acc['non_actionable_unrevalidated_excluded']} historical/non-revalidated observations")
        if key == "stocks_intraday":
            lines.append(
                f"  - excluded from live A/B cohort: "
                f"{acc.get('non_live_tier_excluded', 0)} non-live-tier observations")
        for reason in acc["breaches"] + acc["insufficient"] + acc["ambiguities"]:
            lines.append(f"  - {reason}")
        if key == "stocks_intraday":
            lines.append(f"  - live acceptance: {acc.get('live_acceptance')} · provider "
                         f"{(acc.get('provider') or {}).get('name', 'unknown')}")
    lines.append("")
    lines.append("**By mode** (plan age vs recorded touch→event diagnostics, seconds):")
    for m in r["by_mode"]:
        w, d, al = m["market_wait_sec"], m["system_detection_sec"], m["entry_to_alert_sec"]
        share = f"{int(m['data_gap_late_share']*100)}%" if m["data_gap_late_share"] is not None else "—"
        lines.append(
            f"- {m['mode']}: plan-age p50 {_mins(w['p50'])} (n{w['n']}) · "
            f"recorded detect p90 {_secs(d['p90'])} (n{d['n']}) · "
            f"entry→alert p90 {_secs(al['p90'])} (n{al['n']}) · DATA_GAP_LATE {share}")
    if r["by_source"]:
        lines.append("")
        lines.append("**By source** (SYSTEM entry→alert p90, sent-only):")
        for src, v in r["by_source"].items():
            lines.append(f"- {src}: sent {v['sent']} · "
                         f"entry→alert p90 {_secs(v['entry_to_alert_sec']['p90'])}")
    lines.append("")
    for f in r["flags"]:
        lines.append(f"- FLAG: {f}")
    for b in r["sla_breaches"]:
        lines.append(f"- SLA breach (system latency): {b}")
    for d in r.get("raw_candle_diagnostics", []):
        lines.append(f"- Raw candle-open diagnostic (not an acceptance verdict): {d}")
    return "\n".join(lines)


def _mins(sec) -> str:
    if sec is None:
        return "—"
    return f"{round(sec/60, 1)}min" if sec >= 120 else f"{sec}s"


def _secs(sec) -> str:
    return "—" if sec is None else f"{sec}s"
