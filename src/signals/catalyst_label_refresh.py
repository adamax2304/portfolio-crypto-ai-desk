"""Operational refresh of the catalyst/news linkage on tracked signals.

WHY THIS EXISTS
---------------
Two coupled regressions were observed (2026-06-20):

1. ``signal_catalyst_labels`` was a **one-shot backfill** (PART 9, stamped
   2026-06-15T16:32:53) and no scheduler step ever rewrote it. Every signal
   created afterwards had **no label row at all** (0/43 of the last-2-day
   signals were labelled).

2. ``proposed_signals.news_supported`` **under-fires at scan time**. The
   scan-time catalyst enrichment (``CatalystAgent`` over
   ``load_recent_news(limit=100)``) only sees the freshest ~100 crypto news
   rows — which, given the desk's news volume (~460 crypto rows/day), is barely
   the last ~5 hours. A genuine, symbol-tagged catalyst published earlier the
   same day falls outside that window, so the symbol's ``CatalystSummary`` stays
   empty and ``news_supported`` is left 0. Verified examples: ONDO, TAO, WLD,
   XLM, AVAX, SUI all had real ``detected_symbols_json`` hits within 48 h of
   signal creation yet were stamped ``news_supported=0``.

WHAT THIS DOES (and explicitly does NOT do)
-------------------------------------------
A per-cycle, **post-scan** pass that, for recent/active signals:

* re-derives "does this symbol have a direct, symbol-tagged news catalyst near
  the signal's creation time" using robust word-boundary membership (we read the
  JSON symbol columns — never a title substring, so "Ordinals" never fabricates
  an ``ORDI`` catalyst and "Sweden" never fabricates ``EDEN``);
* **additively** upgrades ``news_supported`` / ``telegram_supported`` 0 -> 1 on
  the signal row when such a hit exists (never 1 -> 0, so an in-flight position
  is never *downgraded* / re-sized smaller);
* recomputes the display labels via :func:`compute_labels` and upserts them into
  ``signal_catalyst_labels`` with a fresh ``computed_at`` (so the derived table
  stops being frozen at the backfill timestamp).

It does NOT touch scoring, tier, TP/SL, entry/exit, routing/actionability,
filters, validity windows, or the scan-time enrichment. It only corrects the
catalyst/news *flags* and the derived *label* cache — both documented as
display/measurement-only.

TRUST LAYER (2026-07-08) — what counts as a catalyst source:
  * ``detected_symbols_json`` is the **broad candidate set**: a union of the
    entity resolver's hits AND the collector's naive bare-ticker ingest scan. It
    is used only to FIND candidate rows, never to prove a catalyst on its own.
  * ``trusted_symbols_json`` (written by :mod:`src.news.entity_resolver`) is the
    **allowed source** for flipping ``news_supported`` — only symbols with real
    provenance (company/token alias, cashtag, listing parser, cross-asset match).
    An unresolved row (``resolution_status``/``trusted_symbols_json`` NULL) or a
    bare-acronym-only tag (e.g. "DIA" in "…Receives DIA Approval") is NOT trusted
    and cannot flip the flag; an explicit ``$TICKER`` cashtag is a per-asset
    fallback (stocks: ``$`` only; crypto: ``$`` or ``#``).
  * **Legacy behaviour** applies only when the DB predates the trust layer (no
    ``trusted_symbols_json`` column): then membership in ``detected_symbols_json``
    alone is honoured, exactly as before, so old databases still work.
"""

from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

from src.catalysts.collector import CATALYST_MIN_IMPORTANCE
from src.signals.catalyst_labels import compute_labels

# Statuses for which a signal is still "live" and worth keeping labelled even if
# it was created before the recency window. Mirrors models.OPEN_STATUSES.
ACTIVE_STATUSES = (
    "generated", "waiting_for_entry", "triggered", "tp1_hit", "tp2_hit",
)

DEFAULT_DAYS = 7
DEFAULT_LOOKBACK_HOURS = 48
DEFAULT_FORWARD_HOURS = 2
REFRESH_RUN_VERSION = "catalyst_label_refresh_runs_v1"


def _ensure_refresh_indexes(conn: sqlite3.Connection) -> None:
    """Keep the per-cycle label refresh bounded on production-sized DBs.

    ``direct_news_for_signal`` filters canonical events by ``effective_at`` and
    ``linkage_allowed``.  Older migrations only indexed ``published_at`` there,
    which makes the scheduler watchdog vulnerable to a slow full scan as the
    news table grows.
    """
    try:
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_news_canonical_effective_linkage "
            "ON news_canonical_events(effective_at, linkage_allowed)"
        )
    except sqlite3.OperationalError:
        pass


def _ensure_refresh_run_table(conn: sqlite3.Connection) -> None:
    """Persist a completion marker even when there are no labels to rewrite.

    ``signal_catalyst_labels.computed_at`` only advances when at least one
    in-scope signal exists. Using it as a scheduler heartbeat therefore turns a
    quiet but successful refresh into a false operational incident. This tiny
    append-only table is strictly telemetry; it has no role in scoring,
    routing, or execution.
    """
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS catalyst_label_refresh_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            completed_at TEXT NOT NULL,
            scanned INTEGER NOT NULL,
            labels_written INTEGER NOT NULL,
            news_flips INTEGER NOT NULL,
            telegram_flips INTEGER NOT NULL,
            version TEXT NOT NULL
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_catalyst_label_refresh_runs_completed "
        "ON catalyst_label_refresh_runs(completed_at)"
    )


def _record_refresh_run(
    conn: sqlite3.Connection,
    *,
    completed_at: str,
    stats: RefreshStats,
) -> None:
    conn.execute(
        """
        INSERT INTO catalyst_label_refresh_runs(
            completed_at, scanned, labels_written, news_flips,
            telegram_flips, version
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            completed_at,
            stats.scanned,
            stats.labels_written,
            stats.news_flips,
            stats.telegram_flips,
            REFRESH_RUN_VERSION,
        ),
    )
    try:
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_news_items_asset_published "
            "ON news_items(asset_class, published_at)"
        )
    except sqlite3.OperationalError:
        pass
    try:
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_news_items_published_at "
            "ON news_items(published_at)"
        )
    except sqlite3.OperationalError:
        pass


@dataclass
class RefreshStats:
    scanned: int = 0
    news_flips: int = 0
    telegram_flips: int = 0
    labels_written: int = 0
    flipped_symbols: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "scanned": self.scanned,
            "news_flips": self.news_flips,
            "telegram_flips": self.telegram_flips,
            "labels_written": self.labels_written,
            "flipped_symbols": list(self.flipped_symbols),
        }


def _base_ticker(symbol: str | None) -> str:
    return str(symbol or "").split("/")[0].strip().upper()


def _is_telegram_source(source: str | None) -> bool:
    s = (source or "").lower()
    return s.startswith("t.me") or "telegram" in s


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def _parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        d = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        return d
    except Exception:
        return None


def direct_news_for_signal(
    conn: sqlite3.Connection,
    symbol: str,
    created_at: str,
    *,
    asset_class: str = "crypto",
    lookback_hours: int = DEFAULT_LOOKBACK_HOURS,
    forward_hours: int = DEFAULT_FORWARD_HOURS,
    min_importance: float = CATALYST_MIN_IMPORTANCE,
    direction: str | None = None,
    mode: str | None = None,
) -> dict[str, Any] | None:
    """Return the best direct, symbol-tagged news observable at signal time.

    Robust by construction: candidate rows are found via ``detected_symbols_json``
    (the broad union set; word-boundary membership re-checked, never a raw title
    substring), then a **trust gate** keeps only rows whose ticker has real
    provenance — present in ``trusted_symbols_json`` (resolver-written) or carried
    by an explicit cashtag (stocks: ``$TICKER`` only; crypto: ``$``/``#``). A row
    the resolver has not processed yet (``trusted_symbols_json`` NULL) is not
    trusted. On a pre-trust-layer DB (no ``trusted_symbols_json`` column) the gate
    is skipped and legacy ``detected_symbols_json`` membership applies. Read-only.
    """
    ticker = _base_ticker(symbol)
    if not ticker:
        return None

    ref = _parse_iso(created_at) or datetime.now(timezone.utc)
    lo = _iso(ref - timedelta(hours=lookback_hours))
    # ``forward_hours`` survives for CLI/API compatibility but must never
    # admit a catalyst that was unavailable when the signal was decided.
    hi = _iso(ref)

    try:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(news_items)")}
    except sqlite3.OperationalError:
        return None
    if "detected_symbols_json" not in cols:
        return None

    # Production contract: when canonical events are materialized, only a
    # trusted directional event that passed content/source confidence may set
    # news_supported.  Old/test databases without this table retain the legacy
    # trust-column path below.
    try:
        has_canonical = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='news_canonical_events'"
        ).fetchone()
    except sqlite3.OperationalError:
        has_canonical = None
    if has_canonical:
        try:
            canonical = conn.execute(
                "SELECT * FROM news_canonical_events WHERE linkage_allowed=1 "
                "AND effective_at>=? AND effective_at<=? AND trusted_symbols_json LIKE ? "
                "ORDER BY is_cluster_primary DESC, confidence DESC, effective_at DESC",
                (lo, hi, f'%\"{ticker}\"%'),
            ).fetchall()
        except sqlite3.OperationalError:
            canonical = []
        expected = "bullish" if str(direction or "").lower() == "long" else (
            "bearish" if str(direction or "").lower() == "short" else None)
        matches: list[dict[str, Any]] = []
        telegram_clusters: set[str] = set()
        for raw_event in canonical:
            event = dict(raw_event)
            try:
                symbols = {_base_ticker(v) for v in json.loads(event.get("trusted_symbols_json") or "[]")}
            except (TypeError, ValueError):
                symbols = set()
            if ticker not in symbols:
                continue
            if expected and event.get("direction_hint") != expected:
                continue
            from src.news.freshness import supports_mode
            if not supports_mode(event.get("event_latency_class"), mode):
                continue
            expires = _parse_iso(event.get("expires_at"))
            if expires is not None and expires < ref:
                continue
            if _is_telegram_source(event.get("source")):
                telegram_clusters.add(str(event.get("cluster_key") or ""))
            matches.append(event)
        if not matches:
            return None
        # One cluster is one catalyst regardless of how many outlets repeated it.
        by_cluster: dict[str, dict[str, Any]] = {}
        for event in matches:
            key = str(event.get("cluster_key") or event.get("event_id"))
            if key not in by_cluster or int(event.get("is_cluster_primary") or 0) > int(
                    by_cluster[key].get("is_cluster_primary") or 0):
                by_cluster[key] = event
        best_event = max(by_cluster.values(), key=lambda e: (
            float(e.get("confidence") or 0), str(e.get("published_at") or "")))
        cluster = str(best_event.get("cluster_key") or "")
        # Corroborating Telegram may not be the canonical primary.
        if cluster and cluster not in telegram_clusters:
            try:
                telegram_clusters.update(str(r["cluster_key"]) for r in conn.execute(
                    "SELECT cluster_key, source FROM news_canonical_events WHERE cluster_key=?", (cluster,)).fetchall()
                    if _is_telegram_source(r["source"]))
            except Exception:
                pass
        return {
            "headline": str(best_event.get("title") or ""),
            "source": str(best_event.get("source") or ""),
            "published_at": best_event.get("published_at"), "importance": None,
            "available_at": best_event.get("available_at") or best_event.get("effective_at"),
            "event_latency_class": best_event.get("event_latency_class"),
            "telegram": _is_telegram_source(best_event.get("source")),
            "has_telegram": cluster in telegram_clusters,
            "n_hits": len(by_cluster), "cross_asset": False,
            "event_type": best_event.get("event_type"),
            "direction_hint": best_event.get("direction_hint"),
            "content_level": best_event.get("content_level"),
            "confidence": best_event.get("confidence"),
            "linkage_reason": best_event.get("linkage_reason"),
            "canonical": True,
        }
    has_imp = "importance" in cols
    # trust layer (2026-07-08): once the resolver has run, only symbols with real provenance may drive
    # catalyst / news_supported. A bare ingest tag (e.g. "DIA" from "King Copper Receives DIA Approval")
    # is NOT trusted. When the column is absent (pre-migration DB) we keep the legacy behaviour.
    has_trusted = "trusted_symbols_json" in cols

    sel = "title, source, published_at, detected_symbols_json, asset_class" + (
        ", importance" if has_imp else "") + (", trusted_symbols_json" if has_trusted else "")
    # Asset-aware news pool. Crypto: unchanged (crypto/NULL rows). Stocks: stock news for the ticker
    # PLUS cross-asset crypto-feed rows that named the bare ticker (e.g. a stock story that arrived on a
    # crypto RSS feed) — the exact-membership re-check below prevents any false cross-match.
    ac = (asset_class or "crypto").lower()
    where_asset = ("asset_class IN ('stocks','crypto')" if ac == "stocks"
                   else "(asset_class='crypto' OR asset_class IS NULL)")
    try:
        rows = conn.execute(
            f"SELECT {sel} FROM news_items "
            f"WHERE {where_asset} "
            "AND published_at >= ? AND published_at <= ? "
            "AND detected_symbols_json LIKE ? "
            "ORDER BY published_at DESC",
            (lo, hi, f'%"{ticker}"%'),
        ).fetchall()
    except sqlite3.OperationalError:
        return None

    best: dict[str, Any] | None = None
    best_telegram: dict[str, Any] | None = None
    n_hits = 0
    for row in rows:
        raw = row["detected_symbols_json"]
        try:
            syms = json.loads(raw) if isinstance(raw, str) else (raw or [])
        except (TypeError, ValueError, json.JSONDecodeError):
            syms = []
        # Confirm membership exactly (defensive vs. LIKE substring surprises).
        if ticker not in {str(s).split("/")[0].strip().upper() for s in (syms or [])}:
            continue
        # TRUST GATE: the symbol must have real provenance for THIS row — it is in the resolver's
        # trusted_symbols_json, OR a cashtag ($TICKER/#TICKER) is in the title. An untrusted preexisting
        # tag (bare acronym, entity_match_source none/confidence 0) never flips news_supported.
        if has_trusted:
            trusted_ok = False
            try:
                tj = row["trusted_symbols_json"]
                # A NULL trusted_symbols_json means the resolver has NOT processed this row yet
                # (resolution_status IS NULL) — it is NOT trusted. Only a resolver-written, non-empty
                # list counts. An unresolved row can still qualify below via an explicit cashtag.
                if tj:
                    trusted_ok = ticker in {str(s).split("/")[0].strip().upper() for s in json.loads(tj)}
            except (TypeError, ValueError, KeyError):
                trusted_ok = False
            if not trusted_ok:
                # Cashtag fallback for an untrusted / not-yet-resolved row. Asset-aware:
                #   stocks → ONLY '$TICKER' (a '#TICKER' hashtag is social noise on equities);
                #   crypto → '$TICKER' or '#TICKER' (both are conventional token references).
                cashtag_re = (rf"\${re.escape(ticker)}\b" if ac == "stocks"
                              else rf"[$#]{re.escape(ticker)}\b")
                if re.search(cashtag_re, str(row["title"] or "")):
                    trusted_ok = True
            if not trusted_ok:
                continue
        imp = row["importance"] if has_imp else None
        if has_imp and imp is not None:
            try:
                if float(imp) < min_importance:
                    continue
            except (TypeError, ValueError):
                pass
        n_hits += 1
        hit = {
            "headline": str(row["title"] or ""),
            "source": str(row["source"] or ""),
            "published_at": row["published_at"],
            "importance": float(imp) if (has_imp and imp is not None) else None,
            "telegram": _is_telegram_source(row["source"]),
            "cross_asset": bool(ac and str(row["asset_class"] or "").lower() not in ("", ac)),
        }
        # "best" = first (newest) overall; "best_telegram" = newest telegram one.
        if best is None or (
            (hit["importance"] or 0) > (best.get("importance") or 0)
        ):
            best = hit
        if hit["telegram"] and best_telegram is None:
            best_telegram = hit

    if best is None:
        return None
    best["has_telegram"] = best_telegram is not None
    best["n_hits"] = n_hits
    return best


def _label_signal_dict(
    signal_row: dict[str, Any],
    *,
    effective_news: bool,
    hit: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build the dict fed to :func:`compute_labels`.

    Overlays a synthetic ``catalyst_meta`` (headline / source / published_at /
    importance) from the matched news hit so the freshness/strength/source
    labels reflect the *real* catalyst. This synthetic payload is used ONLY for
    the derived label cache; it is never written back to ``proposed_signals``.
    """
    raw = signal_row.get("raw_idea_json") or "{}"
    try:
        raw_obj = json.loads(raw) if isinstance(raw, str) else dict(raw or {})
    except (TypeError, ValueError, json.JSONDecodeError):
        raw_obj = {}
    if not isinstance(raw_obj, dict):
        raw_obj = {}

    if hit:
        meta = dict(raw_obj.get("catalyst_meta") or {})
        meta.setdefault("headline_short", hit.get("headline") or "")
        meta.setdefault("source", hit.get("source") or "")
        meta.setdefault("published_at", hit.get("published_at"))
        if meta.get("importance") is None and hit.get("importance") is not None:
            meta["importance"] = hit.get("importance")
        meta.setdefault("mapping", "exact")  # detected_symbols_json is exact
        raw_obj["catalyst_meta"] = meta

    return {
        "asset_class": signal_row.get("asset_class") or "crypto",
        "news_supported": bool(effective_news),
        "created_at": signal_row.get("created_at"),
        "funding_context": signal_row.get("funding_context") or "",
        "oi_context": signal_row.get("oi_context") or "",
        "raw_idea_json": raw_obj,
    }


def _upsert_label(
    conn: sqlite3.Connection,
    signal_id: str,
    labels: dict[str, str],
    computed_at: str,
) -> None:
    conn.execute(
        """
        INSERT INTO signal_catalyst_labels
            (signal_id, catalyst_freshness, catalyst_strength, source_quality,
             symbol_mapping, derivatives_label, headline_short, computed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(signal_id) DO UPDATE SET
            catalyst_freshness = excluded.catalyst_freshness,
            catalyst_strength  = excluded.catalyst_strength,
            source_quality     = excluded.source_quality,
            symbol_mapping     = excluded.symbol_mapping,
            derivatives_label  = excluded.derivatives_label,
            headline_short     = excluded.headline_short,
            computed_at        = excluded.computed_at
        """,
        (
            signal_id,
            labels.get("catalyst_freshness"),
            labels.get("catalyst_strength"),
            labels.get("source_quality"),
            labels.get("symbol_mapping"),
            labels.get("derivatives_label"),
            labels.get("headline_short"),
            computed_at,
        ),
    )


def refresh_signal_catalyst_labels(
    conn: sqlite3.Connection,
    *,
    now: datetime | None = None,
    days: int = DEFAULT_DAYS,
    lookback_hours: int = DEFAULT_LOOKBACK_HOURS,
    forward_hours: int = DEFAULT_FORWARD_HOURS,
    min_importance: float = CATALYST_MIN_IMPORTANCE,
    update_flags: bool = True,
) -> RefreshStats:
    """Refresh the catalyst/news linkage for recent + active signals.

    For each in-scope ``proposed_signals`` row:
      * find a direct symbol-tagged news hit near ``created_at``;
      * additively upgrade ``news_supported`` / ``telegram_supported`` (0 -> 1)
        when a hit exists and ``update_flags`` is True;
      * recompute and upsert the derived ``signal_catalyst_labels`` row.

    The caller owns the connection / transaction. Returns :class:`RefreshStats`.
    """
    now = now or datetime.now(timezone.utc)
    _ensure_refresh_indexes(conn)
    _ensure_refresh_run_table(conn)
    computed_at = _iso(now)
    cutoff = _iso(now - timedelta(days=days))

    placeholders = ",".join("?" for _ in ACTIVE_STATUSES)
    rows = conn.execute(
        f"""
        SELECT * FROM proposed_signals
        WHERE created_at >= ? OR status IN ({placeholders})
        ORDER BY created_at DESC
        """,
        (cutoff, *ACTIVE_STATUSES),
    ).fetchall()

    stats = RefreshStats()
    for row_index, raw_row in enumerate(rows, start=1):
        row = dict(raw_row)
        stats.scanned += 1
        signal_id = row.get("signal_id")
        if not signal_id:
            continue

        hit = direct_news_for_signal(
            conn,
            row.get("symbol") or "",
            row.get("created_at") or "",
            asset_class=(row.get("asset_class") or "crypto"),
            lookback_hours=lookback_hours,
            forward_hours=forward_hours,
            min_importance=min_importance,
            direction=row.get("direction"),
            mode=row.get("mode"),
        )

        cur_news = int(row.get("news_supported") or 0) == 1
        cur_tg = int(row.get("telegram_supported") or 0) == 1
        effective_news = cur_news or bool(hit)
        effective_tg = cur_tg or bool(hit and hit.get("has_telegram"))

        # Additive-only flag correction (never downgrade 1 -> 0).
        if update_flags and hit:
            if effective_news and not cur_news:
                conn.execute(
                    "UPDATE proposed_signals SET news_supported = 1 "
                    "WHERE signal_id = ? AND COALESCE(news_supported,0) = 0",
                    (signal_id,),
                )
                stats.news_flips += 1
                stats.flipped_symbols.append(_base_ticker(row.get("symbol")))
            if effective_tg and not cur_tg:
                conn.execute(
                    "UPDATE proposed_signals SET telegram_supported = 1 "
                    "WHERE signal_id = ? AND COALESCE(telegram_supported,0) = 0",
                    (signal_id,),
                )
                stats.telegram_flips += 1

        signal_dict = _label_signal_dict(
            row, effective_news=effective_news, hit=hit
        )
        labels = compute_labels(signal_dict, now=now).as_dict()
        _upsert_label(conn, signal_id, labels, computed_at)
        stats.labels_written += 1
        if row_index % 10 == 0:
            # Keep the additive signal+label pair atomic, but release SQLite
            # frequently so a 27-second catalyst repair cannot stall Paper.
            conn.commit()

    _record_refresh_run(conn, completed_at=computed_at, stats=stats)
    return stats
