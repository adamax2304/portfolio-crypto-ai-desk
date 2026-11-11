from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Iterable

from src.models import NewsItem, RejectedIdea, TradeIdea, utc_now_iso
from src.news.content import content_hash as make_content_hash
from src.utils.validation import model_to_dict


class SQLiteStore:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.busy_timeout_ms = 30_000

    def connect(self) -> sqlite3.Connection:
        # WAL + a busy timeout let the 2h full `track-signals` writer and the
        # lightweight 5-min pending-entry tracker (2026-06-16 Option B) write
        # concurrently without "database is locked" errors: WAL allows readers
        # during a write, and busy_timeout makes a second writer wait briefly
        # instead of failing. Both passes are idempotent (alert dedup + status
        # gates), so serialized writes are always safe.
        busy_timeout_ms = max(0, int(getattr(self, "busy_timeout_ms", 30_000)))
        conn = sqlite3.connect(self.db_path, timeout=busy_timeout_ms / 1000.0)
        conn.row_factory = sqlite3.Row
        try:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute(f"PRAGMA busy_timeout={busy_timeout_ms}")
            conn.execute("PRAGMA synchronous=NORMAL")
        except sqlite3.DatabaseError:
            # Never block connection setup on a PRAGMA (e.g. read-only FS).
            pass
        return conn

    def init_db(self) -> None:
        with self.connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS trade_ideas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    report_id TEXT,
                    symbol TEXT NOT NULL,
                    direction TEXT NOT NULL,
                    score REAL NOT NULL,
                    confidence TEXT,
                    risk_level TEXT,
                    timeframe TEXT,
                    entry_low REAL,
                    entry_high REAL,
                    invalidation REAL,
                    tp1 REAL,
                    tp2 REAL,
                    tp3 REAL,
                    thesis TEXT,
                    evidence_json TEXT,
                    counterarguments_json TEXT,
                    tier TEXT,
                    mode TEXT,
                    exchange_focus TEXT,
                    data_confidence TEXT,
                    cap_reasons_json TEXT,
                    asset_class TEXT NOT NULL DEFAULT 'crypto',
                    status TEXT NOT NULL DEFAULT 'open',
                    raw_json TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS idea_checks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    idea_id INTEGER NOT NULL,
                    checked_at TEXT NOT NULL,
                    current_price REAL,
                    status TEXT,
                    mfe REAL,
                    mae REAL,
                    notes TEXT,
                    FOREIGN KEY (idea_id) REFERENCES trade_ideas(id)
                );

                CREATE TABLE IF NOT EXISTS news_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    source TEXT,
                    url TEXT UNIQUE,
                    published_at TEXT,
                    detected_symbols_json TEXT,
                    detected_narratives_json TEXT,
                    importance REAL,
                    asset_class TEXT NOT NULL DEFAULT 'crypto',
                    raw_json TEXT,
                    content_text TEXT,
                    ingested_at TEXT,
                    first_seen_at TEXT,
                    available_at TEXT,
                    event_latency_class TEXT,
                    source_observation_delay_seconds REAL,
                    last_seen_at TEXT,
                    content_hash TEXT,
                    source_message_id TEXT,
                    source_channel_id TEXT,
                    source_category TEXT
                );

                -- Fast bounded news-risk queries.  Do not wrap published_at in
                -- SQLite date functions at read time: that defeats this index
                -- once the archive becomes large.
                CREATE INDEX IF NOT EXISTS idx_news_items_published_at
                ON news_items(published_at);

                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_date TEXT,
                    ticker TEXT,
                    event TEXT,
                    event_type TEXT,
                    source TEXT,
                    importance REAL,
                    asset_class TEXT NOT NULL DEFAULT 'crypto',
                    raw_json TEXT
                );

                CREATE UNIQUE INDEX IF NOT EXISTS idx_events_unique
                ON events(event_date, ticker, event);

                CREATE TABLE IF NOT EXISTS agent_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT NOT NULL,
                    run_at TEXT NOT NULL,
                    output_path TEXT,
                    asset_class TEXT NOT NULL DEFAULT 'crypto',
                    summary_json TEXT
                );

                CREATE TABLE IF NOT EXISTS symbols (
                    symbol TEXT PRIMARY KEY,
                    exchange TEXT,
                    active INTEGER DEFAULT 1,
                    first_seen TEXT,
                    last_seen TEXT
                );

                CREATE TABLE IF NOT EXISTS rejected_ideas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    report_id TEXT,
                    symbol TEXT NOT NULL,
                    direction_bias TEXT,
                    score REAL,
                    primary_reason TEXT,
                    reasons_json TEXT,
                    exchanges_json TEXT,
                    risk_flags_json TEXT,
                    asset_class TEXT NOT NULL DEFAULT 'crypto'
                );

                CREATE TABLE IF NOT EXISTS watchlist_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sent_at TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    previous_tier TEXT,
                    new_tier TEXT,
                    score REAL,
                    direction TEXT,
                    mode TEXT,
                    asset_class TEXT NOT NULL DEFAULT 'crypto',
                    payload_json TEXT
                );

                CREATE TABLE IF NOT EXISTS proposed_signals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    signal_id TEXT NOT NULL UNIQUE,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    direction TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    tier TEXT NOT NULL,
                    score REAL,
                    confidence TEXT,
                    data_confidence TEXT,
                    exchange_focus TEXT,
                    listed_exchanges_json TEXT,
                    primary_exchange TEXT,
                    exchange_confirmation_type TEXT,
                    market_regime TEXT,
                    weekend_mode_active INTEGER DEFAULT 0,
                    sector TEXT,
                    narrative TEXT,
                    setup_type TEXT,
                    news_supported INTEGER DEFAULT 0,
                    telegram_supported INTEGER DEFAULT 0,
                    derivatives_supported INTEGER DEFAULT 0,
                    oi_context TEXT,
                    funding_context TEXT,
                    asset_class TEXT NOT NULL DEFAULT 'crypto',
                    entry_type TEXT,
                    entry_low REAL,
                    entry_high REAL,
                    entry_trigger REAL,
                    suggested_entry REAL,
                    stop_loss REAL,
                    invalidation REAL,
                    tp1 REAL,
                    tp2 REAL,
                    tp3 REAL,
                    risk_per_unit REAL,
                    expected_rr_tp1 REAL,
                    expected_rr_tp2 REAL,
                    expected_rr_tp3 REAL,
                    validity_window_hours REAL,
                    expires_at TEXT,
                    thesis TEXT,
                    counter_thesis TEXT,
                    no_entry_conditions_json TEXT,
                    source_report_path TEXT,
                    source_context_path TEXT,
                    report_id TEXT,
                    raw_idea_json TEXT,
                    status TEXT NOT NULL DEFAULT 'waiting_for_entry'
                );

                CREATE INDEX IF NOT EXISTS idx_proposed_signals_status
                    ON proposed_signals(status);
                CREATE INDEX IF NOT EXISTS idx_proposed_signals_symbol
                    ON proposed_signals(symbol);
                CREATE INDEX IF NOT EXISTS idx_proposed_signals_tier_mode
                    ON proposed_signals(tier, mode);
                CREATE INDEX IF NOT EXISTS idx_proposed_signals_created_at
                    ON proposed_signals(created_at);

                CREATE TABLE IF NOT EXISTS signal_initial_stop_plan (
                    signal_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    symbol TEXT,
                    asset_class TEXT,
                    mode TEXT,
                    direction TEXT,
                    entry_price REAL,
                    stop_price REAL,
                    stop_source TEXT,
                    stop_model TEXT,
                    structure_timeframe TEXT,
                    structure_level REAL,
                    stop_distance_pct REAL,
                    fallback_used INTEGER DEFAULT 0,
                    contract_json TEXT NOT NULL,
                    source TEXT
                );

                CREATE INDEX IF NOT EXISTS idx_signal_initial_stop_plan_source
                    ON signal_initial_stop_plan(asset_class, mode, stop_source);

                CREATE TABLE IF NOT EXISTS signal_outcomes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    signal_id TEXT NOT NULL,
                    checked_at TEXT NOT NULL,
                    status TEXT,
                    entry_triggered INTEGER DEFAULT 0,
                    entry_triggered_at TEXT,
                    entry_price_used REAL,
                    stop_hit INTEGER DEFAULT 0,
                    stop_hit_at TEXT,
                    tp1_hit INTEGER DEFAULT 0,
                    tp1_hit_at TEXT,
                    tp2_hit INTEGER DEFAULT 0,
                    tp2_hit_at TEXT,
                    tp3_hit INTEGER DEFAULT 0,
                    tp3_hit_at TEXT,
                    max_favorable_excursion_pct REAL,
                    max_adverse_excursion_pct REAL,
                    max_favorable_excursion_r REAL,
                    max_adverse_excursion_r REAL,
                    final_r REAL,
                    final_outcome TEXT,
                    notes TEXT,
                    FOREIGN KEY (signal_id) REFERENCES proposed_signals(signal_id)
                );

                CREATE INDEX IF NOT EXISTS idx_signal_outcomes_signal_id
                    ON signal_outcomes(signal_id);
                CREATE INDEX IF NOT EXISTS idx_signal_outcomes_signal_id_id
                    ON signal_outcomes(signal_id, id DESC);

                CREATE TABLE IF NOT EXISTS signal_performance_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    period TEXT NOT NULL,
                    mode TEXT,
                    tier TEXT,
                    direction TEXT,
                    metrics_json TEXT
                );

                -- signal_alerts: tracks Telegram notifications sent for proposed
                -- signals. Distinct from watchlist_alerts (legacy crypto-only
                -- cooldown log) — this is the modern, asset-class-aware
                -- per-signal alert ledger used by the stocks monitor session and
                -- (in future) by crypto. Read-only with respect to scoring.
                CREATE TABLE IF NOT EXISTS signal_alerts (
                    alert_id TEXT PRIMARY KEY,
                    signal_id TEXT NOT NULL,
                    asset_class TEXT NOT NULL,
                    mode TEXT,
                    symbol TEXT NOT NULL,
                    tier TEXT NOT NULL,
                    score REAL,
                    direction TEXT,
                    sent_at TEXT NOT NULL,
                    alert_type TEXT NOT NULL,
                    telegram_status TEXT,
                    message_hash TEXT,
                    payload_json TEXT
                );
                CREATE INDEX IF NOT EXISTS idx_signal_alerts_signal_id
                    ON signal_alerts(signal_id);
                CREATE INDEX IF NOT EXISTS idx_signal_alerts_symbol_mode_class
                    ON signal_alerts(symbol, mode, asset_class);
                CREATE INDEX IF NOT EXISTS idx_signal_alerts_sent_at
                    ON signal_alerts(sent_at);

                -- 2026-06-15 catalyst safe-fix PART 2: append-only derivatives
                -- archive. Write-only audit trail of funding / OI snapshots as
                -- they are fetched for live scoring. PRODUCTION SCORING DOES
                -- NOT READ THESE TABLES — they exist purely for historical
                -- replay + funding-cost modelling. Dedup on
                -- (exchange, symbol, fetched_at).
                CREATE TABLE IF NOT EXISTS funding_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fetched_at TEXT NOT NULL,
                    exchange TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    normalized_symbol TEXT,
                    funding_rate REAL,
                    next_funding_time TEXT,
                    mark_price REAL,
                    index_price REAL,
                    long_short_ratio REAL,
                    crowding_label TEXT,
                    raw_json TEXT,
                    source_file TEXT,
                    created_at TEXT NOT NULL,
                    UNIQUE(exchange, symbol, fetched_at)
                );
                CREATE INDEX IF NOT EXISTS idx_funding_snapshots_sym
                    ON funding_snapshots(symbol, fetched_at);

                CREATE TABLE IF NOT EXISTS oi_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fetched_at TEXT NOT NULL,
                    exchange TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    normalized_symbol TEXT,
                    oi_value REAL,
                    oi_value_usd REAL,
                    oi_change_pct REAL,
                    long_short_ratio REAL,
                    crowding_label TEXT,
                    raw_json TEXT,
                    source_file TEXT,
                    created_at TEXT NOT NULL,
                    UNIQUE(exchange, symbol, fetched_at)
                );
                CREATE INDEX IF NOT EXISTS idx_oi_snapshots_sym
                    ON oi_snapshots(symbol, fetched_at);

                -- Derived display-only catalyst labels (PART 9 backfill cache).
                -- Never feeds scoring; safe to rebuild from raw payloads.
                CREATE TABLE IF NOT EXISTS signal_catalyst_labels (
                    signal_id TEXT PRIMARY KEY,
                    catalyst_freshness TEXT,
                    catalyst_strength TEXT,
                    source_quality TEXT,
                    symbol_mapping TEXT,
                    derivatives_label TEXT,
                    headline_short TEXT,
                    computed_at TEXT NOT NULL
                );
                """
            )
            self._migrate_trade_ideas(conn)
            self._migrate_asset_class(conn)
            self._migrate_news_items(conn)
            # High-cadence derivatives/on-chain observations live in their own
            # WAL sidecar. Keeping them out of the trading DB prevents report
            # and tracker writers from delaying pre-entry market context.

    @staticmethod
    def _migrate_trade_ideas(conn: sqlite3.Connection) -> None:
        """Add new columns to legacy trade_ideas tables without dropping data."""
        existing = {row["name"] for row in conn.execute("PRAGMA table_info(trade_ideas)").fetchall()}
        for column, ddl in (
            ("tier", "TEXT"),
            ("mode", "TEXT"),
            ("exchange_focus", "TEXT"),
            ("data_confidence", "TEXT"),
            ("cap_reasons_json", "TEXT"),
        ):
            if column not in existing:
                conn.execute(f"ALTER TABLE trade_ideas ADD COLUMN {column} {ddl}")

    @staticmethod
    def _migrate_asset_class(conn: sqlite3.Connection) -> None:
        """Add asset_class column to legacy tables and backfill 'crypto' on existing rows."""
        for table in (
            "trade_ideas",
            "proposed_signals",
            "news_items",
            "events",
            "rejected_ideas",
            "watchlist_alerts",
            "agent_runs",
        ):
            try:
                existing = {row["name"] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
            except sqlite3.OperationalError:
                continue
            if not existing:
                continue
            if "asset_class" not in existing:
                # SQLite cannot add a NOT NULL column with default via ALTER on legacy rows,
                # so add nullable then backfill, mirroring DEFAULT='crypto'.
                conn.execute(f"ALTER TABLE {table} ADD COLUMN asset_class TEXT")
                conn.execute(f"UPDATE {table} SET asset_class = 'crypto' WHERE asset_class IS NULL")

    @staticmethod
    def _migrate_news_items(conn: sqlite3.Connection) -> None:
        """Additive news ingest metadata migration for old databases.

        These columns are transport/enrichment metadata only. Existing resolver
        columns and historical rows remain untouched.
        """
        try:
            existing = {row["name"] for row in conn.execute("PRAGMA table_info(news_items)").fetchall()}
        except sqlite3.OperationalError:
            return
        for column in (
            "content_text", "ingested_at", "first_seen_at", "last_seen_at",
            "content_hash", "source_message_id", "source_channel_id", "source_category",
        ):
            if column not in existing:
                conn.execute(f"ALTER TABLE news_items ADD COLUMN {column} TEXT")
        for column, ddl in (
            ("available_at", "TEXT"),
            ("event_latency_class", "TEXT"),
            ("source_observation_delay_seconds", "REAL"),
        ):
            if column not in existing:
                conn.execute(f"ALTER TABLE news_items ADD COLUMN {column} {ddl}")

    def save_symbols(self, symbols: Iterable[str], exchange: str) -> None:
        now = utc_now_iso()
        with self.connect() as conn:
            for symbol in symbols:
                conn.execute(
                    """
                    INSERT INTO symbols(symbol, exchange, active, first_seen, last_seen)
                    VALUES(?, ?, 1, ?, ?)
                    ON CONFLICT(symbol) DO UPDATE SET
                        exchange = excluded.exchange,
                        active = 1,
                        last_seen = excluded.last_seen
                    """,
                    (symbol, exchange, now, now),
                )

    def save_agent_run(
        self,
        agent_name: str,
        output_path: str | None,
        summary: dict[str, Any],
        *,
        asset_class: str = "crypto",
    ) -> None:
        """Persist an agent output with bounded retry on short writer contention."""
        for attempt, delay in enumerate((0.0, 0.1, 0.35, 1.0, 2.0)):
            if delay:
                time.sleep(delay)
            try:
                self._save_agent_run_once(
                    agent_name,
                    output_path,
                    summary,
                    asset_class=asset_class,
                )
                return
            except sqlite3.OperationalError as exc:
                locked = "locked" in str(exc).lower() or "busy" in str(exc).lower()
                if not locked or attempt == 4:
                    raise

    def _save_agent_run_once(
        self,
        agent_name: str,
        output_path: str | None,
        summary: dict[str, Any],
        *,
        asset_class: str = "crypto",
    ) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO agent_runs(agent_name, run_at, output_path, asset_class, summary_json)
                VALUES(?, ?, ?, ?, ?)
                """,
                (agent_name, utc_now_iso(), output_path, asset_class, json.dumps(summary)),
            )

    def save_news_items(
        self, items: list[NewsItem], *, asset_class: str = "crypto"
    ) -> int:
        """Persist news with bounded retry for concurrent writers.

        Telegram is event-driven; an incoming item must not be discarded just
        because a short API poll or report owns SQLite's writer lock briefly.
        The underlying upsert is idempotent, so retrying a rolled-back attempt
        is safe. Other database errors still surface immediately.
        """
        for attempt, delay in enumerate((0.0, 0.1, 0.35, 1.0, 2.0)):
            if delay:
                time.sleep(delay)
            try:
                return self._save_news_items_once(items, asset_class=asset_class)
            except sqlite3.OperationalError as exc:
                locked = "locked" in str(exc).lower() or "busy" in str(exc).lower()
                if not locked or attempt == 4:
                    raise
        return 0  # pragma: no cover

    def _save_news_items_once(
        self, items: list[NewsItem], *, asset_class: str = "crypto"
    ) -> int:
        saved = 0
        saved_urls: list[str] = []
        with self.connect() as conn:
            self._migrate_news_items(conn)
            for item in items:
                ingested_at = item.ingested_at or utc_now_iso()
                first_seen_at = item.first_seen_at or ingested_at
                available_at = item.available_at or first_seen_at
                from src.news.freshness import classify_observation
                timing = classify_observation(item.published_at, available_at)
                event_latency_class = item.event_latency_class or timing.event_latency_class
                source_observation_delay_seconds = (
                    item.source_observation_delay_seconds
                    if item.source_observation_delay_seconds is not None
                    else timing.source_observation_delay_seconds
                )
                body = item.content or item.summary or ""
                fingerprint = item.content_hash or make_content_hash(item.title, body)
                prior = (
                    conn.execute("SELECT content_hash FROM news_items WHERE url=?", (item.url,)).fetchone()
                    if item.url else None
                )
                conn.execute(
                    """
                    INSERT INTO news_items(
                        title, source, url, published_at, detected_symbols_json,
                        detected_narratives_json, importance, asset_class, raw_json,
                        content_text, ingested_at, first_seen_at, available_at,
                        event_latency_class, source_observation_delay_seconds, last_seen_at,
                        content_hash, source_message_id, source_channel_id, source_category
                    )
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(url) DO UPDATE SET
                        title = excluded.title,
                        source = excluded.source,
                        published_at = excluded.published_at,
                        detected_symbols_json = excluded.detected_symbols_json,
                        detected_narratives_json = excluded.detected_narratives_json,
                        importance = excluded.importance,
                        asset_class = excluded.asset_class,
                        raw_json = excluded.raw_json,
                        content_text = excluded.content_text,
                        ingested_at = excluded.ingested_at,
                        first_seen_at = COALESCE(news_items.first_seen_at, excluded.first_seen_at),
                        available_at = COALESCE(news_items.available_at, excluded.available_at),
                        event_latency_class = COALESCE(news_items.event_latency_class, excluded.event_latency_class),
                        source_observation_delay_seconds = COALESCE(
                            news_items.source_observation_delay_seconds,
                            excluded.source_observation_delay_seconds
                        ),
                        last_seen_at = excluded.last_seen_at,
                        content_hash = excluded.content_hash,
                        source_message_id = excluded.source_message_id,
                        source_channel_id = excluded.source_channel_id,
                        source_category = excluded.source_category
                    """,
                    (
                        item.title,
                        item.source,
                        item.url,
                        item.published_at,
                        json.dumps(item.detected_symbols),
                        json.dumps(item.detected_narratives),
                        item.importance,
                        asset_class,
                        json.dumps(model_to_dict(item)),
                        body,
                        ingested_at,
                        first_seen_at,
                        available_at,
                        event_latency_class,
                        source_observation_delay_seconds,
                        ingested_at,
                        fingerprint,
                        item.source_message_id,
                        item.source_channel_id,
                        item.source_category,
                    ),
                )
                changed = prior is None or str(prior["content_hash"] or "") != str(fingerprint or "")
                if changed:
                    saved += 1
                if changed and item.url:
                    saved_urls.append(str(item.url))
        # Resolve only after the ingest transaction commits.  This keeps the
        # raw-news write authoritative and avoids holding a write lock while
        # the enrichment layers open their own short transactions.
        try:
            from src.news.pipeline import process_ingested_urls
            process_ingested_urls(str(self.db_path), saved_urls)
        except Exception:
            pass
        return saved

    def save_news_rows(self, rows: list[dict], *, asset_class: str = "crypto") -> int:
        for attempt, delay in enumerate((0.0, 0.1, 0.35, 1.0, 2.0)):
            if delay:
                time.sleep(delay)
            try:
                return self._save_news_rows_once(rows, asset_class=asset_class)
            except sqlite3.OperationalError as exc:
                locked = "locked" in str(exc).lower() or "busy" in str(exc).lower()
                if not locked or attempt == 4:
                    raise
        return 0  # pragma: no cover

    def _save_news_rows_once(self, rows: list[dict], *, asset_class: str = "crypto") -> int:
        """Upsert PRE-NORMALIZED news rows preserving a caller-supplied ``raw_json`` intact.

        Unlike :meth:`save_news_items` (which serializes the NewsItem model and would drop structured
        metadata), this keeps the exact ``raw_json`` the caller built — used by the SEC EDGAR ingest so
        ``form_type`` / ``cik`` / ``filing_url`` / ``event_type`` / ``source_quality`` persist. Same
        ON CONFLICT(url) upsert contract. Each row dict: title, source, url, published_at,
        detected_symbols_json, importance, raw_json (+ optional detected_narratives_json).
        """
        saved = 0
        saved_urls: list[str] = []
        with self.connect() as conn:
            self._migrate_news_items(conn)
            for r in rows:
                raw_payload = r.get("raw_json")
                if isinstance(raw_payload, dict):
                    raw_payload = json.dumps(raw_payload, ensure_ascii=False)
                try:
                    raw_dict = json.loads(raw_payload) if raw_payload else {}
                except (TypeError, ValueError):
                    raw_dict = {}
                body = r.get("content_text") or r.get("content") or r.get("body") or r.get("summary") \
                    or raw_dict.get("content") or raw_dict.get("body") or raw_dict.get("summary") or ""
                ingested_at = r.get("ingested_at") or utc_now_iso()
                first_seen_at = r.get("first_seen_at") or ingested_at
                available_at = r.get("available_at") or first_seen_at
                from src.news.freshness import classify_observation
                timing = classify_observation(r.get("published_at"), available_at)
                event_latency_class = r.get("event_latency_class") or timing.event_latency_class
                source_observation_delay_seconds = r.get("source_observation_delay_seconds")
                if source_observation_delay_seconds is None:
                    source_observation_delay_seconds = timing.source_observation_delay_seconds
                fingerprint = r.get("content_hash") or make_content_hash(r.get("title"), body)
                prior = (
                    conn.execute("SELECT content_hash FROM news_items WHERE url=?", (r.get("url"),)).fetchone()
                    if r.get("url") else None
                )
                conn.execute(
                    """
                    INSERT INTO news_items(
                        title, source, url, published_at, detected_symbols_json,
                        detected_narratives_json, importance, asset_class, raw_json,
                        content_text, ingested_at, first_seen_at, available_at,
                        event_latency_class, source_observation_delay_seconds, last_seen_at,
                        content_hash, source_message_id, source_channel_id, source_category
                    )
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(url) DO UPDATE SET
                        title = excluded.title,
                        source = excluded.source,
                        published_at = excluded.published_at,
                        detected_symbols_json = excluded.detected_symbols_json,
                        detected_narratives_json = excluded.detected_narratives_json,
                        importance = excluded.importance,
                        asset_class = excluded.asset_class,
                        raw_json = excluded.raw_json,
                        content_text = excluded.content_text,
                        ingested_at = excluded.ingested_at,
                        first_seen_at = COALESCE(news_items.first_seen_at, excluded.first_seen_at),
                        available_at = COALESCE(news_items.available_at, excluded.available_at),
                        event_latency_class = COALESCE(news_items.event_latency_class, excluded.event_latency_class),
                        source_observation_delay_seconds = COALESCE(
                            news_items.source_observation_delay_seconds,
                            excluded.source_observation_delay_seconds
                        ),
                        last_seen_at = excluded.last_seen_at,
                        content_hash = excluded.content_hash,
                        source_message_id = excluded.source_message_id,
                        source_channel_id = excluded.source_channel_id,
                        source_category = excluded.source_category
                    """,
                    (
                        r.get("title"), r.get("source"), r.get("url"), r.get("published_at"),
                        r.get("detected_symbols_json") or "[]",
                        r.get("detected_narratives_json") or "[]",
                        r.get("importance"), asset_class, raw_payload,
                        body, ingested_at, first_seen_at, available_at, event_latency_class,
                        source_observation_delay_seconds, ingested_at, fingerprint,
                        r.get("source_message_id"), r.get("source_channel_id"), r.get("source_category"),
                    ),
                )
                changed = prior is None or str(prior["content_hash"] or "") != str(fingerprint or "")
                if changed:
                    saved += 1
                if changed and r.get("url"):
                    saved_urls.append(str(r.get("url")))
        try:
            from src.news.pipeline import process_ingested_urls
            process_ingested_urls(str(self.db_path), saved_urls)
        except Exception:
            pass
        return saved

    #: News sources that are produced by tests / fixtures and must never
    #: leak into production reports unless explicitly opted in via the
    #: ``CRYPTO_AI_DESK_INCLUDE_TEST_NEWS`` env var (set to ``1`` / ``true``).
    TEST_NEWS_SOURCES: set[str] = {
        "test_source",
        "test-source",
        "test",
        "fixture",
    }

    def load_recent_news(
        self,
        limit: int = 100,
        *,
        asset_class: str | None = None,
        include_test_sources: bool | None = None,
    ) -> list[dict[str, Any]]:
        """Load recent news items.

        Parameters
        ----------
        limit:
            Maximum number of rows to return.
        asset_class:
            Optional ``"crypto"`` / ``"stocks"`` filter. ``None`` returns all
            asset classes (current behaviour for callers that have not been
            migrated yet).
        include_test_sources:
            When ``False`` (the default unless overridden via the
            ``CRYPTO_AI_DESK_INCLUDE_TEST_NEWS`` env var) drops rows whose
            ``source`` belongs to ``TEST_NEWS_SOURCES``. Set to ``True``
            to inspect raw fixtures (e.g. for testing or debugging).
        """
        import os

        if include_test_sources is None:
            include_test_sources = os.getenv(
                "CRYPTO_AI_DESK_INCLUDE_TEST_NEWS", ""
            ).strip().lower() in {"1", "true", "yes"}

        clauses: list[str] = []
        params: list[Any] = []
        if asset_class:
            # Tolerate rows that have NULL asset_class (older fixtures) by
            # also accepting NULL when the requested asset_class is crypto
            # (the historical default for the table).
            if asset_class == "crypto":
                clauses.append("(asset_class = ? OR asset_class IS NULL)")
            else:
                clauses.append("asset_class = ?")
            params.append(asset_class)
        if not include_test_sources:
            placeholders = ",".join("?" for _ in self.TEST_NEWS_SOURCES)
            clauses.append(f"source NOT IN ({placeholders})")
            params.extend(self.TEST_NEWS_SOURCES)

        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        sql = f"""
            SELECT * FROM news_items
            {where}
            ORDER BY COALESCE(published_at, '') DESC, id DESC
            LIMIT ?
        """
        params.append(limit)
        with self.connect() as conn:
            rows = conn.execute(sql, tuple(params)).fetchall()
        return [dict(row) for row in rows]

    def load_news_window(
        self,
        *,
        hours: float = 48.0,
        limit: int = 5000,
        asset_class: str | None = None,
        include_test_sources: bool | None = None,
    ) -> list[dict[str, Any]]:
        """Load news items published within the last ``hours`` — a TIME WINDOW, not a lexical latest-N
        tail. Timestamps are parsed robustly in Python (mixed ISO formats) via the source_health parser,
        so a stale-string sort can never truncate the real recent window. Rows carry ``_ts`` (aware UTC).
        Read-only; falls back to ``load_recent_news`` if the window helper is unavailable."""
        import os
        from datetime import datetime, timezone
        if include_test_sources is None:
            include_test_sources = os.getenv(
                "CRYPTO_AI_DESK_INCLUDE_TEST_NEWS", "").strip().lower() in {"1", "true", "yes"}
        clauses: list[str] = []
        params: list[Any] = []
        if asset_class:
            if asset_class == "crypto":
                clauses.append("(asset_class = ? OR asset_class IS NULL)")
            else:
                clauses.append("asset_class = ?")
            params.append(asset_class)
        if not include_test_sources:
            ph = ",".join("?" for _ in self.TEST_NEWS_SOURCES)
            clauses.append(f"source NOT IN ({ph})")
            params.extend(self.TEST_NEWS_SOURCES)
        where = " AND ".join(clauses) or None
        try:
            from src.news.source_health import window_news_rows
            with self.connect() as conn:
                conn.row_factory = sqlite3.Row
                rows = window_news_rows(conn, hours=int(hours), limit=limit, where=where,
                                        params=tuple(params))
            if rows is not None:
                return rows
        except Exception:
            pass
        # fallback: widen the limit and post-filter by the window so we never silently truncate.
        rows = self.load_recent_news(limit=max(limit, 5000), asset_class=asset_class,
                                     include_test_sources=include_test_sources)
        cutoff = datetime.now(timezone.utc).timestamp() - hours * 3600
        out = []
        for r in rows:
            try:
                ts = datetime.fromisoformat(str(r.get("published_at") or "").replace("Z", "+00:00"))
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=timezone.utc)
                if ts.timestamp() >= cutoff:
                    out.append(r)
            except Exception:
                continue
        return out[:limit]

    def save_events(
        self, events: list[dict[str, Any]], *, asset_class: str = "crypto"
    ) -> int:
        saved = 0
        with self.connect() as conn:
            for event in events:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO events(
                        event_date, ticker, event, event_type, source, importance,
                        asset_class, raw_json
                    )
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        str(event.get("date") or event.get("event_date") or ""),
                        str(event.get("ticker") or "").upper(),
                        str(event.get("event") or ""),
                        str(event.get("type") or event.get("event_type") or "other"),
                        str(event.get("source") or ""),
                        float(event.get("importance") or 1),
                        str(event.get("asset_class") or asset_class),
                        json.dumps(event),
                    ),
                )
                saved += 1
        return saved

    def load_events(self, limit: int = 200) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM events
                ORDER BY event_date DESC, id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    def save_trade_ideas(
        self,
        report_id: str,
        ideas: list[TradeIdea],
        *,
        asset_class: str = "crypto",
    ) -> list[int]:
        ids: list[int] = []
        with self.connect() as conn:
            for idea in ideas:
                raw = model_to_dict(idea)
                setup = raw.get("raw", {}).get("setup", {})
                # Prefer the idea's own asset_class if it carries one (stocks pipeline
                # sets this), otherwise fall back to the caller-supplied default.
                idea_asset_class = getattr(idea, "asset_class", None) or asset_class
                cursor = conn.execute(
                    """
                    INSERT INTO trade_ideas(
                        created_at, report_id, symbol, direction, score, confidence,
                        risk_level, timeframe, entry_low, entry_high, invalidation,
                        tp1, tp2, tp3, thesis, evidence_json,
                        counterarguments_json, tier, mode, exchange_focus,
                        data_confidence, cap_reasons_json, asset_class, status, raw_json
                    )
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        utc_now_iso(),
                        report_id,
                        idea.symbol,
                        idea.direction,
                        idea.score,
                        idea.confidence,
                        idea.risk_level,
                        idea.timeframe,
                        setup.get("entry_low"),
                        setup.get("entry_high"),
                        setup.get("invalidation"),
                        setup.get("tp1"),
                        setup.get("tp2"),
                        setup.get("tp3"),
                        idea.thesis,
                        json.dumps(idea.evidence),
                        json.dumps(idea.counterarguments),
                        idea.tier,
                        idea.mode,
                        idea.exchange_focus,
                        idea.data_confidence,
                        json.dumps(idea.cap_reasons),
                        idea_asset_class,
                        idea.status,
                        json.dumps(raw),
                    ),
                )
                ids.append(int(cursor.lastrowid))
        return ids

    def save_rejected_ideas(
        self,
        report_id: str,
        rejected: list[RejectedIdea],
        *,
        asset_class: str = "crypto",
    ) -> int:
        if not rejected:
            return 0
        saved = 0
        with self.connect() as conn:
            for item in rejected:
                conn.execute(
                    """
                    INSERT INTO rejected_ideas(
                        created_at, report_id, symbol, direction_bias, score,
                        primary_reason, reasons_json, exchanges_json, risk_flags_json,
                        asset_class
                    )
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        utc_now_iso(),
                        report_id,
                        item.symbol,
                        item.direction_bias,
                        item.score,
                        item.primary_reason,
                        json.dumps(item.reasons),
                        json.dumps(item.exchanges),
                        json.dumps(item.risk_flags),
                        asset_class,
                    ),
                )
                saved += 1
        return saved

    def load_recent_ideas(self, limit: int = 100) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM trade_ideas
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    def load_open_ideas(self) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM trade_ideas
                WHERE status IN ('open', 'watchlist', 'watchlist only', 'unknown')
                   OR status IS NULL
                ORDER BY created_at DESC
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def add_idea_check(
        self,
        idea_id: int,
        current_price: float | None,
        status: str,
        mfe: float | None,
        mae: float | None,
        notes: str,
    ) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO idea_checks(
                    idea_id, checked_at, current_price, status, mfe, mae, notes
                )
                VALUES(?, ?, ?, ?, ?, ?, ?)
                """,
                (idea_id, utc_now_iso(), current_price, status, mfe, mae, notes),
            )
            conn.execute(
                "UPDATE trade_ideas SET status = ? WHERE id = ?",
                (status, idea_id),
            )

    def record_watchlist_alert(
        self,
        symbol: str,
        previous_tier: str,
        new_tier: str,
        score: float,
        direction: str,
        mode: str,
        payload: dict[str, Any],
        *,
        asset_class: str = "crypto",
    ) -> int:
        with self.connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO watchlist_alerts(
                    sent_at, symbol, previous_tier, new_tier, score,
                    direction, mode, asset_class, payload_json
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    utc_now_iso(),
                    symbol,
                    previous_tier,
                    new_tier,
                    float(score),
                    direction,
                    mode,
                    asset_class,
                    json.dumps(payload),
                ),
            )
            return int(cursor.lastrowid)

    def last_alert_for(self, symbol: str) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute(
                """
                SELECT * FROM watchlist_alerts
                WHERE symbol = ?
                ORDER BY sent_at DESC
                LIMIT 1
                """,
                (symbol,),
            ).fetchone()
        return dict(row) if row else None

    # ------------------------------------------------------------------
    # Derivatives archive (append-only). Write-only — NOT read by scoring.
    # ------------------------------------------------------------------

    def record_funding_snapshot(
        self,
        *,
        fetched_at: str,
        exchange: str,
        symbol: str,
        normalized_symbol: str | None = None,
        funding_rate: float | None = None,
        next_funding_time: str | None = None,
        mark_price: float | None = None,
        index_price: float | None = None,
        long_short_ratio: float | None = None,
        crowding_label: str | None = None,
        raw_json: str | None = None,
        source_file: str | None = None,
    ) -> bool:
        """Append a funding snapshot. Dedup on (exchange, symbol, fetched_at).

        Returns True if a row was inserted, False if it was a duplicate.
        Best-effort: never raises to the caller's live path."""
        with self.connect() as conn:
            cur = conn.execute(
                """
                INSERT OR IGNORE INTO funding_snapshots(
                    fetched_at, exchange, symbol, normalized_symbol, funding_rate,
                    next_funding_time, mark_price, index_price, long_short_ratio,
                    crowding_label, raw_json, source_file, created_at
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (fetched_at, exchange, symbol, normalized_symbol, funding_rate,
                 next_funding_time, mark_price, index_price, long_short_ratio,
                 crowding_label, raw_json, source_file, utc_now_iso()),
            )
            return cur.rowcount > 0

    def record_oi_snapshot(
        self,
        *,
        fetched_at: str,
        exchange: str,
        symbol: str,
        normalized_symbol: str | None = None,
        oi_value: float | None = None,
        oi_value_usd: float | None = None,
        oi_change_pct: float | None = None,
        long_short_ratio: float | None = None,
        crowding_label: str | None = None,
        raw_json: str | None = None,
        source_file: str | None = None,
    ) -> bool:
        """Append an OI snapshot. Dedup on (exchange, symbol, fetched_at)."""
        with self.connect() as conn:
            cur = conn.execute(
                """
                INSERT OR IGNORE INTO oi_snapshots(
                    fetched_at, exchange, symbol, normalized_symbol, oi_value,
                    oi_value_usd, oi_change_pct, long_short_ratio, crowding_label,
                    raw_json, source_file, created_at
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (fetched_at, exchange, symbol, normalized_symbol, oi_value,
                 oi_value_usd, oi_change_pct, long_short_ratio, crowding_label,
                 raw_json, source_file, utc_now_iso()),
            )
            return cur.rowcount > 0

    # ------------------------------------------------------------------
    # signal_alerts — modern, asset-class-aware Telegram alert ledger.
    # Used by the stocks intraday monitor; can be reused by crypto later.
    # ------------------------------------------------------------------

    def record_signal_alert(
        self,
        *,
        alert_id: str,
        signal_id: str,
        asset_class: str,
        symbol: str,
        tier: str,
        sent_at: str,
        alert_type: str,
        mode: str | None = None,
        score: float | None = None,
        direction: str | None = None,
        telegram_status: str | None = None,
        message_hash: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        """Insert a row into ``signal_alerts``.

        Read-only with respect to scoring. Failures here must never block a
        monitor loop; the caller is responsible for wrapping in try/except
        if continuation is required.
        """
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO signal_alerts(
                    alert_id, signal_id, asset_class, mode, symbol, tier,
                    score, direction, sent_at, alert_type, telegram_status,
                    message_hash, payload_json
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    alert_id, signal_id, asset_class, mode, symbol, tier,
                    score, direction, sent_at, alert_type, telegram_status,
                    message_hash, json.dumps(payload or {}),
                ),
            )

    def last_signal_alert_for_signal(self, signal_id: str) -> dict[str, Any] | None:
        """Most recent ``signal_alerts`` row for a given ``signal_id``."""
        with self.connect() as conn:
            row = conn.execute(
                """
                SELECT * FROM signal_alerts
                WHERE signal_id = ?
                ORDER BY sent_at DESC
                LIMIT 1
                """,
                (signal_id,),
            ).fetchone()
        return dict(row) if row else None

    def last_signal_alert_for_setup(
        self,
        *,
        asset_class: str,
        symbol: str,
        mode: str | None,
        direction: str | None,
    ) -> dict[str, Any] | None:
        """Most recent ``signal_alerts`` row matching the setup key
        (asset_class, symbol, mode, direction)."""
        clauses = ["asset_class = ?", "symbol = ?"]
        params: list[Any] = [asset_class, symbol]
        if mode is not None:
            clauses.append("mode = ?")
            params.append(mode)
        if direction is not None:
            clauses.append("direction = ?")
            params.append(direction)
        sql = (
            "SELECT * FROM signal_alerts WHERE "
            + " AND ".join(clauses)
            + " ORDER BY sent_at DESC LIMIT 1"
        )
        with self.connect() as conn:
            row = conn.execute(sql, tuple(params)).fetchone()
        return dict(row) if row else None

    def alert_status_summary(
        self, *, asset_class: str | None = None
    ) -> dict[str, Any]:
        """Counts for the ``alert-status`` CLI: A/B signals registered,
        alerts sent, not alerted, duplicates skipped (inferred from
        repeated signal_id rows)."""
        with self.connect() as conn:
            ac_clause = ""
            params: list[Any] = []
            if asset_class:
                ac_clause = "WHERE asset_class = ?"
                params = [asset_class]
            ab_total = conn.execute(
                f"SELECT COUNT(*) AS n FROM proposed_signals "
                f"{ac_clause}{' AND ' if ac_clause else 'WHERE '}tier IN ('A','B')",
                tuple(params),
            ).fetchone()
            alerted_signal_ids = {
                row["signal_id"]
                for row in conn.execute(
                    f"SELECT DISTINCT signal_id FROM signal_alerts "
                    f"{ac_clause}",
                    tuple(params),
                ).fetchall()
            }
            ab_signal_ids = {
                row["signal_id"]
                for row in conn.execute(
                    f"SELECT signal_id FROM proposed_signals "
                    f"{ac_clause}{' AND ' if ac_clause else 'WHERE '}tier IN ('A','B')",
                    tuple(params),
                ).fetchall()
            }
            alerts_total = conn.execute(
                f"SELECT COUNT(*) AS n FROM signal_alerts {ac_clause}",
                tuple(params),
            ).fetchone()
        ab_n = int(ab_total["n"]) if ab_total else 0
        ab_alerted = len(ab_signal_ids & alerted_signal_ids)
        ab_not_alerted = max(0, ab_n - ab_alerted)
        total_alerts = int(alerts_total["n"]) if alerts_total else 0
        duplicates_skipped = max(0, total_alerts - len(alerted_signal_ids))
        return {
            "asset_class": asset_class or "all",
            "ab_signals_total": ab_n,
            "alerts_sent_total": total_alerts,
            "ab_alerted": ab_alerted,
            "ab_not_alerted_yet": ab_not_alerted,
            "duplicate_alerts_skipped_estimate": duplicates_skipped,
        }

    def counts(self) -> dict[str, int]:
        tables = [
            "trade_ideas",
            "idea_checks",
            "news_items",
            "events",
            "agent_runs",
            "symbols",
            "rejected_ideas",
            "watchlist_alerts",
            "proposed_signals",
            "signal_outcomes",
            "signal_performance_snapshots",
        ]
        output: dict[str, int] = {}
        with self.connect() as conn:
            for table in tables:
                try:
                    row = conn.execute(f"SELECT COUNT(*) AS n FROM {table}").fetchone()
                    output[table] = int(row["n"])
                except sqlite3.OperationalError:
                    # Table may not yet exist on legacy databases that haven't
                    # run init_db() after the signal-tracking migration.
                    output[table] = 0
        return output

    # ------------------------------------------------------------------
    # Signal tracking helpers
    # ------------------------------------------------------------------

    def upsert_proposed_signal(self, row: dict[str, Any]) -> bool:
        """Insert a proposed signal. Returns True if newly inserted, False if
        the signal_id already existed (idempotent re-register).

        Re-registration may enrich a pending setup, but it must never rewind an
        entered/closed lifecycle or rewrite the execution geometry after entry.
        The tracker is the sole owner of ``status`` transitions.
        """
        columns = list(row.keys())
        placeholders = ", ".join("?" for _ in columns)
        column_sql = ", ".join(columns)
        execution_geometry = {
            "symbol", "direction", "mode", "asset_class", "entry_type",
            "entry_low", "entry_high", "entry_trigger", "suggested_entry",
            "stop_loss", "invalidation", "tp1", "tp2", "tp3",
            "risk_per_unit", "expires_at", "validity_window_hours",
            "setup_type", "playbook",
        }
        updates = []
        for col in columns:
            if col in ("signal_id", "created_at", "status"):
                continue
            if col in execution_geometry:
                updates.append(
                    f"{col}=CASE WHEN proposed_signals.status IN "
                    "('generated','waiting_for_entry') "
                    f"THEN excluded.{col} ELSE proposed_signals.{col} END"
                )
            else:
                updates.append(f"{col}=excluded.{col}")
        update_sql = ", ".join(updates)
        sql = (
            f"INSERT INTO proposed_signals({column_sql}) VALUES({placeholders}) "
            f"ON CONFLICT(signal_id) DO UPDATE SET {update_sql}"
        )
        with self.connect() as conn:
            before = conn.execute(
                "SELECT * FROM proposed_signals WHERE signal_id = ?",
                (row["signal_id"],),
            ).fetchone()
            write_row = dict(row)
            # The proposed-signal lifecycle can legitimately lag the Paper
            # ledger by one tracker tick. Once Paper has entered, its original
            # entry/stop/target geometry is authoritative even if the proposal
            # still says waiting_for_entry. Without this second ownership
            # check, re-registering the same signal_id mixes an old fill with
            # new targets and can manufacture impossible Paper R multiples.
            paper_entered = False
            try:
                paper = conn.execute(
                    "SELECT lifecycle_state FROM paper_execution_outcomes "
                    "WHERE signal_id=?",
                    (row["signal_id"],),
                ).fetchone()
                paper_entered = bool(
                    paper and str(paper["lifecycle_state"] or "").upper()
                    in {"OPEN", "CLOSED"}
                )
            except sqlite3.OperationalError:
                # The additive Paper table is created lazily on legacy DBs.
                pass
            if paper_entered and before is not None:
                for col in execution_geometry.intersection(columns):
                    write_row[col] = before[col]
            conn.execute(sql, [write_row[col] for col in columns])
            return before is None

    def load_active_signals(self) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM proposed_signals
                WHERE status IN (
                    'generated', 'waiting_for_entry', 'triggered',
                    'tp1_hit', 'tp2_hit'
                )
                ORDER BY created_at DESC
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def load_signal(self, signal_id: str) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM proposed_signals WHERE signal_id = ?",
                (signal_id,),
            ).fetchone()
        return dict(row) if row else None

    def load_signals_for_period(
        self,
        *,
        since: str | None = None,
        until: str | None = None,
        mode: str | None = None,
        tier: str | None = None,
        direction: str | None = None,
        asset_class: str | None = None,
    ) -> list[dict[str, Any]]:
        clauses: list[str] = []
        params: list[Any] = []
        if since is not None:
            clauses.append("created_at >= ?")
            params.append(since)
        if until is not None:
            clauses.append("created_at <= ?")
            params.append(until)
        if mode is not None:
            clauses.append("mode = ?")
            params.append(mode)
        if tier is not None:
            clauses.append("tier = ?")
            params.append(tier)
        if direction is not None:
            clauses.append("direction = ?")
            params.append(direction)
        if asset_class is not None:
            # Treat legacy NULL rows as 'crypto' so existing data stays visible
            # when callers ask for crypto specifically.
            if asset_class == "crypto":
                clauses.append("(asset_class = ? OR asset_class IS NULL)")
                params.append(asset_class)
            else:
                clauses.append("asset_class = ?")
                params.append(asset_class)
        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        with self.connect() as conn:
            rows = conn.execute(
                f"SELECT * FROM proposed_signals {where} ORDER BY created_at DESC",
                params,
            ).fetchall()
        return [dict(row) for row in rows]

    def update_signal_status(
        self,
        signal_id: str,
        *,
        status: str,
        updated_at: str,
    ) -> bool:
        """Advance a signal lifecycle monotonically.

        Returns ``True`` when the stored status changed. Once entered, a signal
        cannot return to a pre-entry state; TP milestones cannot regress; and a
        closed signal is immutable. This changes no entry/exit rule, it only
        prevents concurrent/repeated tracker passes from rewriting history.
        """
        pre_entry = {"generated", "waiting_for_entry"}
        entered_rank = {"triggered": 1, "tp1_hit": 2, "tp2_hit": 3}
        entered_terminal = {"tp3_hit", "stopped", "expired", "ambiguous"}
        pre_entry_terminal = {
            "missed_no_entry", "invalidated_before_entry", "stale_before_entry",
            "entry_moved_away",
        }
        with self.connect() as conn:
            current_row = conn.execute(
                "SELECT status FROM proposed_signals WHERE signal_id = ?", (signal_id,)
            ).fetchone()
            if current_row is None:
                return False
            current = str(current_row["status"] or "")
            target = str(status or "")
            if not target or target == current:
                return False
            if current in entered_terminal or current in pre_entry_terminal:
                return False
            if current in entered_rank:
                if target in pre_entry or target in pre_entry_terminal:
                    return False
                if target in entered_rank and entered_rank[target] < entered_rank[current]:
                    return False
            cursor = conn.execute(
                "UPDATE proposed_signals SET status = ?, updated_at = ? "
                "WHERE signal_id = ? AND status = ?",
                (target, updated_at, signal_id, current),
            )
            return cursor.rowcount > 0

    def add_signal_outcome(self, row: dict[str, Any]) -> int:
        columns = list(row.keys())
        placeholders = ", ".join("?" for _ in columns)
        column_sql = ", ".join(columns)
        with self.connect() as conn:
            cursor = conn.execute(
                f"INSERT INTO signal_outcomes({column_sql}) VALUES({placeholders})",
                [row[col] for col in columns],
            )
            return int(cursor.lastrowid)

    def add_signal_outcome_if_changed(self, row: dict[str, Any]) -> int:
        """Append an outcome snapshot only when its state changed.

        Pending monitors may evaluate an unchanged signal every few seconds.
        Persisting identical snapshots on every tick creates large write load
        without adding audit information. Keep the first snapshot and every
        meaningful transition, while treating ``checked_at`` as observation
        metadata. Once the same signal is already entered in the same state,
        its first entry timestamp/price are immutable; subsequent quote samples
        must not masquerade as new entry updates.
        """
        columns = list(row.keys())
        placeholders = ", ".join("?" for _ in columns)
        column_sql = ", ".join(columns)
        signal_id = str(row.get("signal_id") or "")
        with self.connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            latest = conn.execute(
                "SELECT * FROM signal_outcomes WHERE signal_id = ? "
                "ORDER BY checked_at DESC, id DESC LIMIT 1",
                (signal_id,),
            ).fetchone()
            ignored = {"checked_at"}
            if (
                latest is not None
                and bool(latest["entry_triggered"])
                and bool(row.get("entry_triggered"))
                and str(latest["status"] or "") == str(row.get("status") or "")
            ):
                ignored.update({"entry_triggered_at", "entry_price_used"})
            if latest is not None and all(
                latest[column] == row[column]
                for column in columns
                if column not in ignored
            ):
                return int(latest["id"])
            cursor = conn.execute(
                f"INSERT INTO signal_outcomes({column_sql}) VALUES({placeholders})",
                [row[col] for col in columns],
            )
            return int(cursor.lastrowid)

    def load_latest_outcome(self, signal_id: str) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute(
                """
                SELECT * FROM signal_outcomes
                WHERE signal_id = ?
                ORDER BY checked_at DESC, id DESC
                LIMIT 1
                """,
                (signal_id,),
            ).fetchone()
        return dict(row) if row else None

    def load_all_outcomes_for(self, signal_id: str) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM signal_outcomes WHERE signal_id = ? "
                "ORDER BY checked_at ASC, id ASC",
                (signal_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def signal_id_exists(self, signal_id: str) -> bool:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT 1 FROM proposed_signals WHERE signal_id = ?",
                (signal_id,),
            ).fetchone()
        return row is not None

    def load_recent_terminal_outcomes(
        self, since_iso: str
    ) -> list[dict[str, Any]]:
        """Read-only: latest outcome per signal that reached a TERMINAL result
        (win/loss/partial_win) and exited on/after ``since_iso``.

        Diagnostic helper for the alert-only circuit breaker (PART: profitability
        guardrails). ``exit_at`` is the realised-exit timestamp (stop/TP hit, else
        checked_at). Joins signal metadata (asset_class/mode/tier/direction/symbol/
        market_regime). Pure SELECT — never mutates, never changes scoring.
        """
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT o.signal_id, o.checked_at, o.status, o.final_r,
                       o.final_outcome, o.stop_hit, o.entry_triggered_at,
                       COALESCE(o.stop_hit_at, o.tp3_hit_at, o.tp2_hit_at,
                                o.tp1_hit_at, o.checked_at) AS exit_at,
                       s.asset_class, s.mode, s.tier, s.direction, s.symbol,
                       s.market_regime, s.created_at
                FROM proposed_signals s
                JOIN signal_outcomes o ON o.id = (
                    SELECT latest.id FROM signal_outcomes latest
                    WHERE latest.signal_id = s.signal_id
                    ORDER BY latest.id DESC LIMIT 1
                )
                WHERE s.status IN (
                    'stopped', 'tp3_hit', 'expired', 'ambiguous', 'missed_no_entry'
                )
                  AND o.final_outcome IN ('win', 'loss', 'partial_win')
                  AND COALESCE(o.stop_hit_at, o.tp3_hit_at, o.tp2_hit_at,
                               o.tp1_hit_at, o.checked_at) >= ?
                ORDER BY exit_at ASC
                """,
                (since_iso,),
            ).fetchall()
        return [dict(row) for row in rows]

    def load_recent_paper_terminal_outcomes(
        self,
        since_iso: str,
        *,
        fee_profile: str,
    ) -> list[dict[str, Any]]:
        """Return accepted Paper exits for the active fee profile only.

        This is deliberately separate from :meth:`load_recent_terminal_outcomes`.
        The latter is a legacy, all-signal diagnostic view and includes shadow
        observations plus ``final_r``.  A Paper risk floor must instead use the
        realised net USD result of entries that were actually accepted at
        point-in-time.  ``final_r`` below is only the net-USD/risk normalisation
        required by the existing circuit-breaker thresholds.
        """
        try:
            with self.connect() as conn:
                rows = conn.execute(
                    """
                    SELECT l.signal_id,
                           COALESCE(l.exit_at, l.timestamp) AS exit_at,
                           CASE
                               WHEN COALESCE(l.net_pnl_usdt, 0) < 0 THEN 'loss'
                               WHEN COALESCE(l.net_pnl_usdt, 0) > 0 THEN 'win'
                               ELSE 'partial_win'
                           END AS final_outcome,
                           CASE
                               WHEN lower(COALESCE(l.close_reason, ''))
                                    IN ('original_stop', 'same_bar_original_stop')
                                AND COALESCE(l.net_pnl_usdt, 0) < 0
                               THEN 1 ELSE 0
                           END AS stop_hit,
                           CASE
                               WHEN COALESCE(l.risk_usdt, 0) > 0
                               THEN l.net_pnl_usdt / l.risk_usdt
                               ELSE 0
                           END AS final_r,
                           s.asset_class, s.mode, s.tier, s.direction, s.symbol,
                           s.market_regime, s.created_at,
                           l.net_pnl_usdt, l.risk_usdt, l.close_reason,
                           l.paper_action, l.actionability_source, l.fee_profile
                    FROM paper_portfolio_ledger l
                    JOIN proposed_signals s ON s.signal_id = l.signal_id
                    WHERE l.event_type = 'exit'
                      AND l.fee_profile = ?
                      AND l.paper_action IN ('FULL_SIZE', 'HALF_SIZE')
                      AND l.actionability_source IN (
                          'alert_payload', 'paper_entry_alert_point_in_time'
                      )
                      AND COALESCE(l.exit_at, l.timestamp) >= ?
                    ORDER BY exit_at ASC
                    """,
                    (fee_profile, since_iso),
                ).fetchall()
            return [dict(row) for row in rows]
        except sqlite3.OperationalError:
            # Old/read-only databases without the derived Paper ledger leave
            # the new authority fail-open rather than falling back to shadow
            # or legacy final-R evidence.
            return []

    def last_alert_by_type(self, alert_type: str) -> dict[str, Any] | None:
        """Read-only: most recent ``signal_alerts`` row for an exact alert_type.

        Used to dedupe/cooldown the alert-only circuit-breaker warning, whose
        key is encoded in the alert_type (e.g. ``cb_diag:crypto:intraday:2026-06-17:L2``).
        Pure SELECT.
        """
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM signal_alerts WHERE alert_type = ? "
                "ORDER BY sent_at DESC LIMIT 1",
                (alert_type,),
            ).fetchone()
        return dict(row) if row else None
