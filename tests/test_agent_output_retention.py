from datetime import datetime, timedelta, timezone

from src.maintenance.agent_output_retention import plan, run


def _write(path, stamp: datetime, text: str = "{}"):
    path.write_text(text, encoding="utf-8")
    ts = stamp.timestamp()
    import os
    os.utime(path, (ts, ts))


def test_retention_keeps_recent_outputs_and_removes_only_old_json(tmp_path):
    now = datetime(2026, 8, 16, 12, tzinfo=timezone.utc)
    old = tmp_path / "20260801_trade_idea_agent.json"
    recent = tmp_path / "20260815_trade_idea_agent.json"
    non_json = tmp_path / "20260801_notes.txt"
    _write(old, now - timedelta(days=8), '{"old": true}')
    _write(recent, now - timedelta(days=1), '{"recent": true}')
    _write(non_json, now - timedelta(days=8), "keep")

    preview = plan(tmp_path, days=7, now=now)
    assert preview["candidate_files"] == 1
    assert preview["retained_files"] == 1

    result = run(tmp_path, days=7, dry_run=False, now=now)
    assert result["removed_files"] == 1
    assert not old.exists()
    assert recent.exists()
    assert non_json.exists()


def test_retention_dry_run_is_non_mutating(tmp_path):
    now = datetime(2026, 8, 16, tzinfo=timezone.utc)
    old = tmp_path / "20260801_news_agent.json"
    _write(old, now - timedelta(days=8))

    result = run(tmp_path, days=7, dry_run=True, now=now)
    assert result["candidate_files"] == 1
    assert result["removed_files"] == 0
    assert old.exists()
