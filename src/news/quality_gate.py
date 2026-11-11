"""Deterministic gold cases plus production replay health for the news block."""
from __future__ import annotations

import json
import math
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from src.config import load_config
from src.news import canonical_events, entity_resolver
from src.news.content_coverage import content_level
from src.news.entity_health import compute_entity_health
from src.news.source_health import _parse_ts, compute_source_health


_ROOT = Path(__file__).resolve().parents[2]
_GOLD = _ROOT / "config" / "news_gold_cases.yaml"


def _base(values: list[str]) -> set[str]:
    return {str(v).split("/")[0].upper() for v in values}


def run_gold_cases(path: Path = _GOLD) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    cases = payload.get("cases") or []
    crypto, stocks = entity_resolver._matchers()
    failures: list[dict[str, Any]] = []
    for case in cases:
        row = {
            "title": case.get("title"), "source": case.get("source"),
            "asset_class": case.get("asset_class"), "content_text": case.get("content"),
            "raw_json": "{}", "url": f"gold://{case.get('name')}",
        }
        resolved = entity_resolver.resolve_row(row, crypto_matcher=crypto, stocks_matcher=stocks)
        mentioned = _base(resolved.get("trusted_symbols") or [])
        row["trusted_symbols_json"] = json.dumps(sorted(mentioned))
        row["detected_entities_json"] = json.dumps(resolved.get("detected_entities") or [])
        expected = _base(case.get("expected_symbols") or [])
        forbidden = _base(case.get("forbidden_symbols") or [])
        text = str(case.get("title") or "")
        event_type, _ = canonical_events.classify_event(text, str(case.get("asset_class") or "crypto"))
        direction = canonical_events.direction_hint(text, event_type)
        symbols = set(canonical_events._subject_symbols(row, text, event_type, sorted(mentioned)))
        quality = canonical_events.source_quality(case.get("source"))
        level = content_level(row)
        confidence = canonical_events._confidence(quality, level, event_type, sorted(symbols))
        allowed, reason, _ = canonical_events._policy(
            {"event_type": event_type, "source_quality": quality, "content_level": level,
             "direction_hint": direction, "confidence": confidence, "symbols": sorted(symbols)},
            corroboration=1, non_social=int(quality != "social"),
        )
        problems: list[str] = []
        if not expected <= symbols:
            problems.append(f"missing_symbols={sorted(expected-symbols)}")
        if forbidden & symbols:
            problems.append(f"forbidden_symbols={sorted(forbidden & symbols)}")
        if case.get("expected_event_type") and event_type != case["expected_event_type"]:
            problems.append(f"event_type={event_type}")
        if case.get("expected_direction") and direction != case["expected_direction"]:
            problems.append(f"direction={direction}")
        if "expected_linkage" in case and bool(allowed) != bool(case["expected_linkage"]):
            problems.append(f"linkage={allowed}:{reason}")
        if problems:
            failures.append({"name": case.get("name"), "problems": problems,
                             "symbols": sorted(symbols), "mentioned_symbols": sorted(mentioned),
                             "event_type": event_type,
                             "direction": direction, "linkage_allowed": allowed,
                             "linkage_reason": reason})
    return {"cases": len(cases), "passed": len(cases) - len(failures), "failed": len(failures),
            "failures": failures, "pass_rate": round((len(cases)-len(failures))/len(cases), 4) if cases else 0}


def _percentile(values: list[float], p: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, math.ceil(p * len(ordered)) - 1))
    return round(ordered[index], 3)


def production_replay(db: str | None = None, *, now: datetime | None = None) -> dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    path = db or str(load_config().db_path)
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    latencies: list[float] = []
    canonical_rows = policy_covered = primaries = recent_news_rows = 0
    try:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(news_items)")}
        if {"resolution_trigger", "resolution_latency_seconds"} <= cols:
            for r in conn.execute(
                    "SELECT resolution_latency_seconds FROM news_items "
                    "WHERE resolver_version LIKE 'entity_resolver_v%' "
                    "AND resolution_trigger='incremental_post_ingest' "
                    "AND resolution_latency_seconds IS NOT NULL"):
                latencies.append(float(r["resolution_latency_seconds"]))
        if "published_at" in cols:
            cutoff = now.timestamp() - 24 * 3600
            for r in conn.execute("SELECT published_at FROM news_items"):
                published = _parse_ts(r["published_at"])
                if published is not None and published.timestamp() >= cutoff:
                    recent_news_rows += 1
        has = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' "
                           "AND name='news_canonical_events'").fetchone()
        if has:
            canonical_rows = conn.execute("SELECT COUNT(*) FROM news_canonical_events").fetchone()[0]
            policy_covered = conn.execute(
                "SELECT COUNT(*) FROM news_canonical_events WHERE policy_version IS NOT NULL "
                "AND linkage_reason IS NOT NULL").fetchone()[0]
            primaries = conn.execute(
                "SELECT COUNT(*) FROM news_canonical_events WHERE is_cluster_primary=1").fetchone()[0]
    finally:
        conn.close()
    entity = compute_entity_health(path, now=now)
    source = compute_source_health(path, now=now)
    try:
        from src.news.coverage_gaps import compute_coverage_gaps
        gaps = compute_coverage_gaps(path, hours=72, now=now, examples=0).get("by_state") or {}
    except Exception:
        gaps = {}
    source_summary = source.get("summary") or {}
    return {
        "resolution_latency_seconds": {"n": len(latencies), "p50": _percentile(latencies, .5),
                                       "p95": _percentile(latencies, .95), "max": max(latencies) if latencies else None,
                                       "status": "MEASURED" if latencies else "NO_FORWARD_SAMPLE"},
        "recent_news_rows_24h": recent_news_rows, "canonical_rows": canonical_rows,
        "canonical_primary_clusters": primaries,
        "policy_coverage_pct": round(policy_covered / canonical_rows, 4) if canonical_rows else 0,
        "unresolved_symbol_tagged_24h": entity["windows"]["24h"]["unresolved_symbol_tagged"],
        "entity_severity": entity["severity"], "source_error": source_summary.get("error", 0),
        "source_dead": source_summary.get("dead", 0), "source_stale": source_summary.get("stale", 0),
        "source_blocking_error_dead": source_summary.get("blocking_error_dead", 0),
        "source_primary_errors": source_summary.get("error_primary", []),
        "source_primary_dead": source_summary.get("dead_primary", []),
        "unmapped_impact": int(gaps.get("unmapped_impact", 0)),
        "resolver_pending_persist": int(gaps.get("resolver_pending_persist", 0)),
        "untracked_entity_queue": int(gaps.get("untracked_entity", 0)),
        "outside_trade_universe_queue": int(gaps.get("outside_trade_universe", 0)),
    }


def evaluate(db: str | None = None, *, now: datetime | None = None) -> dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    gold = run_gold_cases()
    replay = production_replay(db, now=now)
    reasons: list[str] = []
    if gold["failed"]:
        reasons.append(f"gold_failures={gold['failed']}")
    if replay["unresolved_symbol_tagged_24h"]:
        reasons.append(f"unresolved_24h={replay['unresolved_symbol_tagged_24h']}")
    blocking_sources = replay.get("source_blocking_error_dead")
    if blocking_sources is None:
        blocking_sources = replay["source_error"] + replay["source_dead"]
    if blocking_sources:
        reasons.append(f"primary_source_error_dead={blocking_sources}")
    if replay["unmapped_impact"] or replay["resolver_pending_persist"]:
        reasons.append(f"mapping_gap={replay['unmapped_impact']} "
                       f"pending={replay['resolver_pending_persist']}")
    if replay["canonical_rows"] and replay["policy_coverage_pct"] < 1:
        reasons.append("canonical_policy_coverage_below_100pct")
    if replay["recent_news_rows_24h"] and not replay["canonical_rows"]:
        reasons.append("canonical_event_layer_empty")
    p95 = replay["resolution_latency_seconds"]["p95"]
    if p95 is not None and p95 > 120:
        reasons.append(f"resolution_p95={p95}s")
    return {"generated_at": now.isoformat(), "ready": not reasons, "reasons": reasons,
            "gold": gold, "production_replay": replay,
            "criteria": {"gold_pass_rate": 1.0, "unresolved_symbol_tagged_24h": 0,
                         "primary_source_error_dead": 0, "policy_coverage_pct": 1.0,
                         "unmapped_impact_and_pending": 0,
                         "resolution_latency_p95_seconds_max": 120},
            "note": "A failing gate blocks trust claims, not ingestion or paper trading."}


def render_markdown(result: dict[str, Any]) -> str:
    g, r = result["gold"], result["production_replay"]
    lines = ["# News Quality Gate", "", f"Generated: {result['generated_at']}", "",
             f"**READY: {'YES' if result['ready'] else 'NO'}**",
             f"Reasons: {', '.join(result['reasons']) or 'none'}", "",
             f"Gold cases: **{g['passed']}/{g['cases']} passed**", "",
             f"Canonical rows/clusters: {r['canonical_rows']}/{r['canonical_primary_clusters']}",
             f"Policy coverage: {r['policy_coverage_pct']*100:.1f}%",
             f"Resolution latency: {r['resolution_latency_seconds']['status']} "
             f"(n={r['resolution_latency_seconds']['n']}, p50={r['resolution_latency_seconds']['p50']}, "
             f"p95={r['resolution_latency_seconds']['p95']})",
             f"Unresolved symbol-tagged 24h: {r['unresolved_symbol_tagged_24h']}",
             f"Source ERROR/DEAD/STALE: {r['source_error']}/{r['source_dead']}/{r['source_stale']}"]
    lines.append(f"Blocking primary ERROR/DEAD: {r.get('source_blocking_error_dead', 0)}; "
                 "redundant-source failures remain warnings.")
    lines.append(f"Mapping gaps (unmapped/pending; blocking): {r['unmapped_impact']}/"
                 f"{r['resolver_pending_persist']} · review queues (untracked/outside universe): "
                 f"{r['untracked_entity_queue']}/{r['outside_trade_universe_queue']}")
    if g["failures"]:
        lines += ["", "## Gold failures"]
        lines += [f"- {x['name']}: {', '.join(x['problems'])}" for x in g["failures"]]
    lines += ["", result["note"]]
    return "\n".join(lines)


def refresh(db: str | None = None, *, now: datetime | None = None, write: bool = True) -> dict[str, Any]:
    result = evaluate(db, now=now)
    if write:
        (_ROOT / "reports").mkdir(parents=True, exist_ok=True)
        (_ROOT / "data" / "diagnostics").mkdir(parents=True, exist_ok=True)
        (_ROOT / "reports" / "NEWS_QUALITY_GATE.md").write_text(render_markdown(result), encoding="utf-8")
        (_ROOT / "data" / "diagnostics" / "news_quality_gate.json").write_text(
            json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result


__all__ = ["run_gold_cases", "production_replay", "evaluate", "render_markdown", "refresh"]
