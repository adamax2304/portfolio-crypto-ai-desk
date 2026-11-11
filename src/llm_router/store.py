from __future__ import annotations

import hashlib
import json
import sqlite3
import zlib
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


DDL = """
CREATE TABLE IF NOT EXISTS llm_router_requests (
  request_id TEXT PRIMARY KEY,
  parent_request_id TEXT,
  timestamp TEXT NOT NULL,
  agent TEXT NOT NULL,
  task_type TEXT NOT NULL,
  selected_tier TEXT NOT NULL,
  selected_model TEXT NOT NULL,
  routing_reason TEXT NOT NULL,
  escalation_reason TEXT,
  status TEXT NOT NULL,
  input_tokens INTEGER NOT NULL DEFAULT 0,
  output_tokens INTEGER NOT NULL DEFAULT 0,
  latency_ms REAL NOT NULL DEFAULT 0,
  cost_usd REAL NOT NULL DEFAULT 0,
  tool_calls_json TEXT NOT NULL DEFAULT '[]',
  structured_output_valid INTEGER NOT NULL DEFAULT 0,
  retry_count INTEGER NOT NULL DEFAULT 0,
  confidence REAL,
  review_status TEXT,
  model_disagreement INTEGER NOT NULL DEFAULT 0,
  disagreement_fields_json TEXT NOT NULL DEFAULT '[]',
  final_downstream_action TEXT,
  signal_id TEXT,
  asset_class TEXT,
  symbol TEXT,
  mode TEXT,
  input_hash TEXT NOT NULL,
  output_hash TEXT,
  error_type TEXT,
  evaluation_only INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_llm_router_requests_time
  ON llm_router_requests(timestamp);
CREATE INDEX IF NOT EXISTS idx_llm_router_requests_agent
  ON llm_router_requests(agent, task_type, timestamp);
CREATE INDEX IF NOT EXISTS idx_llm_router_requests_signal
  ON llm_router_requests(signal_id, timestamp);

CREATE TABLE IF NOT EXISTS llm_router_attempts (
  attempt_id TEXT PRIMARY KEY,
  request_id TEXT NOT NULL,
  timestamp TEXT NOT NULL,
  agent TEXT NOT NULL,
  task_type TEXT NOT NULL,
  selected_tier TEXT NOT NULL,
  selected_model TEXT NOT NULL,
  purpose TEXT NOT NULL,
  attempt_number INTEGER NOT NULL DEFAULT 1,
  status TEXT NOT NULL,
  input_tokens INTEGER NOT NULL DEFAULT 0,
  output_tokens INTEGER NOT NULL DEFAULT 0,
  latency_ms REAL NOT NULL DEFAULT 0,
  cost_usd REAL NOT NULL DEFAULT 0,
  generation_id TEXT,
  error_type TEXT,
  FOREIGN KEY(request_id) REFERENCES llm_router_requests(request_id)
);
CREATE INDEX IF NOT EXISTS idx_llm_router_attempts_time
  ON llm_router_attempts(timestamp);
CREATE INDEX IF NOT EXISTS idx_llm_router_attempts_request
  ON llm_router_attempts(request_id, attempt_number);
CREATE INDEX IF NOT EXISTS idx_llm_router_attempts_agent
  ON llm_router_attempts(agent, task_type, timestamp);

CREATE TABLE IF NOT EXISTS llm_router_replay_tasks (
  request_id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  input_hash TEXT NOT NULL,
  compressed_payload BLOB NOT NULL,
  FOREIGN KEY(request_id) REFERENCES llm_router_requests(request_id)
);

CREATE TABLE IF NOT EXISTS llm_router_replay_results (
  replay_id TEXT PRIMARY KEY,
  source_request_id TEXT NOT NULL,
  request_id TEXT NOT NULL,
  tier TEXT NOT NULL,
  model TEXT NOT NULL,
  status TEXT NOT NULL,
  payload_json TEXT,
  latency_ms REAL NOT NULL DEFAULT 0,
  cost_usd REAL NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL,
  error_type TEXT,
  FOREIGN KEY(source_request_id) REFERENCES llm_router_replay_tasks(request_id)
);
CREATE INDEX IF NOT EXISTS idx_llm_router_replay_source
  ON llm_router_replay_results(source_request_id, created_at);
"""


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


def stable_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


class LLMRouterStore:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as conn:
            # DDL is idempotent and doubles as the migration path for new
            # observability tables on an existing production database.
            conn.executescript(DDL)

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=30.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA busy_timeout=30000")
        try:
            current_mode = str(conn.execute("PRAGMA journal_mode").fetchone()[0]).lower()
            if current_mode != "wal":
                conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
        except sqlite3.DatabaseError:
            pass
        return conn

    def record_request(self, row: dict[str, Any], replay_payload: dict[str, Any] | None) -> None:
        columns = list(row)
        placeholders = ",".join("?" for _ in columns)
        with self.connect() as conn:
            conn.execute(
                f"INSERT INTO llm_router_requests({','.join(columns)}) VALUES({placeholders})",
                [row[column] for column in columns],
            )
            if replay_payload is not None:
                packed = zlib.compress(canonical_json(replay_payload).encode("utf-8"), level=9)
                conn.execute(
                    "INSERT OR REPLACE INTO llm_router_replay_tasks VALUES(?,?,?,?)",
                    (row["request_id"], row["timestamp"], row["input_hash"], packed),
                )
            conn.commit()

    def record_attempt(self, row: dict[str, Any]) -> None:
        columns = list(row)
        placeholders = ",".join("?" for _ in columns)
        with self.connect() as conn:
            conn.execute(
                f"INSERT INTO llm_router_attempts({','.join(columns)}) VALUES({placeholders})",
                [row[column] for column in columns],
            )
            conn.commit()

    def daily_spend(self, *, now: datetime | None = None) -> dict[str, float]:
        """Return UTC-day spend without double-counting migrated request rows.

        New traffic is measured from every provider attempt. Historical rows
        created before the attempt ledger are included only when that logical
        request has no attempt rows.
        """
        moment = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
        cutoff = moment.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        totals = {"routine": 0.0, "analyst": 0.0, "review": 0.0}
        with self.connect() as conn:
            attempt_rows = conn.execute(
                "SELECT selected_tier,SUM(cost_usd) cost FROM llm_router_attempts "
                "WHERE timestamp>=? GROUP BY selected_tier",
                (cutoff,),
            ).fetchall()
            legacy_rows = conn.execute(
                "SELECT r.selected_tier,SUM(r.cost_usd) cost FROM llm_router_requests r "
                "WHERE r.timestamp>=? AND r.evaluation_only=0 AND NOT EXISTS ("
                "SELECT 1 FROM llm_router_attempts a WHERE a.request_id=r.request_id) "
                "GROUP BY r.selected_tier",
                (cutoff,),
            ).fetchall()
        for row in [*attempt_rows, *legacy_rows]:
            tier = str(row["selected_tier"] or "")
            if tier in totals:
                totals[tier] += float(row["cost"] or 0.0)
        totals = {key: round(value, 8) for key, value in totals.items()}
        totals["total"] = round(sum(totals.values()), 8)
        return totals

    def update_review(
        self,
        request_id: str,
        *,
        review_status: str,
        model_disagreement: bool,
        disagreement_fields: tuple[str, ...],
        escalation_reason: str | None,
    ) -> None:
        with self.connect() as conn:
            conn.execute(
                "UPDATE llm_router_requests SET review_status=?,model_disagreement=?,"
                "disagreement_fields_json=?,escalation_reason=? WHERE request_id=?",
                (
                    review_status,
                    int(model_disagreement),
                    canonical_json(disagreement_fields),
                    escalation_reason,
                    request_id,
                ),
            )
            conn.commit()

    def mark_downstream_action(self, request_id: str, action: str) -> None:
        with self.connect() as conn:
            conn.execute(
                "UPDATE llm_router_requests SET final_downstream_action=? WHERE request_id=?",
                (str(action)[:200], request_id),
            )
            conn.commit()

    def load_replay_task(self, request_id: str) -> dict[str, Any]:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT compressed_payload FROM llm_router_replay_tasks WHERE request_id=?",
                (request_id,),
            ).fetchone()
        if row is None:
            raise KeyError(request_id)
        return json.loads(zlib.decompress(row[0]).decode("utf-8"))

    def record_replay_result(self, row: dict[str, Any]) -> None:
        columns = list(row)
        with self.connect() as conn:
            conn.execute(
                f"INSERT INTO llm_router_replay_results({','.join(columns)}) "
                f"VALUES({','.join('?' for _ in columns)})",
                [row[column] for column in columns],
            )
            conn.commit()

    def prune(self, *, request_days: int, replay_days: int) -> dict[str, int]:
        request_cutoff = (datetime.now(timezone.utc) - timedelta(days=max(1, request_days))).isoformat()
        replay_cutoff = (datetime.now(timezone.utc) - timedelta(days=max(1, replay_days))).isoformat()
        with self.connect() as conn:
            attempts = conn.execute(
                "DELETE FROM llm_router_attempts WHERE timestamp<?", (request_cutoff,)
            ).rowcount
            replay_results = conn.execute(
                "DELETE FROM llm_router_replay_results WHERE created_at<?", (replay_cutoff,)
            ).rowcount
            replay_tasks = conn.execute(
                "DELETE FROM llm_router_replay_tasks WHERE created_at<?", (replay_cutoff,)
            ).rowcount
            requests = conn.execute(
                "DELETE FROM llm_router_requests WHERE timestamp<?", (request_cutoff,)
            ).rowcount
            conn.commit()
        return {
            "requests": requests,
            "attempts": attempts,
            "replay_tasks": replay_tasks,
            "replay_results": replay_results,
        }


__all__ = ["DDL", "LLMRouterStore", "canonical_json", "stable_hash", "utc_now_iso"]
