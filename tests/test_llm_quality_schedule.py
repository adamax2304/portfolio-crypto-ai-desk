from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

from scripts import run_llm_quality_schedule as schedule


def test_run_once_updates_heartbeat_when_no_new_events(tmp_path):
    heartbeat = tmp_path / "heartbeat.json"
    now = datetime(2026, 9, 20, 10, 0, tzinfo=timezone.utc)

    result = schedule.run_once(
        refresh_fn=lambda **_: {
            "status": "OK", "targets": 0, "recorded": 0,
            "skipped_fresh": 0, "errors": 0,
        },
        metrics_fn=lambda **_: {"calls": 0, "warnings": []},
        db_path=tmp_path / "desk.sqlite",
        now_fn=lambda: now,
        heartbeat_path=heartbeat,
    )

    assert result["status"] == "OK"
    persisted = json.loads(heartbeat.read_text(encoding="utf-8"))
    assert persisted["status"] == "OK"
    assert persisted["advisory"]["targets"] == 0
    assert persisted["completed_at"] == now.isoformat()


def test_run_once_records_degraded_provider_result(tmp_path):
    result = schedule.run_once(
        refresh_fn=lambda **_: {
            "status": "DEGRADED", "targets": 2, "recorded": 2, "errors": 1,
        },
        metrics_fn=lambda **_: {"calls": 1, "warnings": []},
        db_path=tmp_path / "desk.sqlite",
        heartbeat_path=tmp_path / "heartbeat.json",
    )
    assert result["status"] == "DEGRADED"


def test_run_once_records_budget_pause_as_nonfatal_status(tmp_path):
    result = schedule.run_once(
        refresh_fn=lambda **_: {
            "status": "BUDGET_PAUSED",
            "targets": 2,
            "recorded": 1,
            "errors": 1,
            "error": "llm_daily_budget_exhausted:total:1.0>=0.8",
        },
        metrics_fn=lambda **_: {"calls": 1, "warnings": ["DAILY_LLM_HARD_BUDGET"]},
        db_path=tmp_path / "desk.sqlite",
        heartbeat_path=tmp_path / "heartbeat.json",
    )

    assert result["status"] == "BUDGET_PAUSED"
    assert result["error"].startswith("llm_daily_budget_exhausted:total:")


def test_metrics_lock_does_not_invalidate_successful_advisory(tmp_path):
    result = schedule.run_once(
        refresh_fn=lambda **_: {"status": "OK", "targets": 1, "recorded": 1},
        metrics_fn=lambda **_: (_ for _ in ()).throw(RuntimeError("database is locked")),
        db_path=tmp_path / "desk.sqlite",
        heartbeat_path=tmp_path / "heartbeat.json",
    )

    assert result["status"] == "OK"
    assert result["metrics"]["status"] == "DEGRADED"
    assert "database is locked" in result["metrics"]["error"]


def test_health_snapshot_marks_missing_and_stale_heartbeat(tmp_path):
    config = tmp_path / "config"
    config.mkdir()
    (config / "quality_agents.yaml").write_text(
        "quality_agents:\n"
        "  enabled: true\n"
        "  llm_advisory_refresh:\n"
        "    enabled: true\n"
        "    interval_minutes: 15\n"
        "    stale_after_minutes: 45\n",
        encoding="utf-8",
    )
    now = datetime(2026, 9, 20, 12, 0, tzinfo=timezone.utc)
    missing = schedule.health_snapshot(root=tmp_path, now=now)
    assert missing["required"] is True
    assert missing["stale"] is True

    heartbeat = tmp_path / "data" / "runtime" / "llm_quality_refresh.heartbeat.json"
    heartbeat.parent.mkdir(parents=True)
    heartbeat.write_text(json.dumps({
        "status": "OK",
        "completed_at": (now - timedelta(minutes=46)).isoformat(),
    }), encoding="utf-8")
    stale = schedule.health_snapshot(root=tmp_path, now=now)
    assert stale["stale"] is True
    assert stale["age_minutes"] == 46.0


def test_health_snapshot_does_not_require_disabled_llm_refresh(tmp_path):
    config = tmp_path / "config"
    config.mkdir()
    (config / "quality_agents.yaml").write_text(
        "quality_agents:\n"
        "  enabled: true\n"
        "  llm_advisory_refresh:\n"
        "    enabled: false\n",
        encoding="utf-8",
    )

    snapshot = schedule.health_snapshot(
        root=tmp_path,
        now=datetime(2026, 9, 20, 12, 0, tzinfo=timezone.utc),
    )

    assert snapshot["required"] is False
    assert snapshot["stale"] is False


def test_live_lock_is_not_stolen(tmp_path, monkeypatch):
    lock = tmp_path / "refresh.lock"
    lock.write_text(json.dumps({"pid": 123, "started_at": "2026-09-20T00:00:00+00:00"}))
    monkeypatch.setattr(schedule, "_pid_alive", lambda pid: pid == 123)
    with schedule._lease(lock) as acquired:
        assert acquired is False
    assert lock.exists()
