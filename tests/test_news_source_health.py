from datetime import datetime, timezone

from src.news.source_health import _classify


def test_fresh_successful_quiet_transport_is_idle_not_stale():
    now = datetime(2026, 7, 26, 12, tzinfo=timezone.utc)
    status, warnings = _classify(
        {"enabled": True, "primary": False, "source_type": "rss", "name": "Quiet RSS"},
        {"total": 8, "r24": 0, "r72": 2, "matched24": 0}, None, now=now,
        transport={"status": "ok_empty", "finished_at": now.isoformat()},
    )
    assert status == "OK_IDLE"
    assert any("fresh successful transport" in item for item in warnings)


def test_old_transport_does_not_hide_a_stale_source():
    now = datetime(2026, 7, 26, 12, tzinfo=timezone.utc)
    status, _ = _classify(
        {"enabled": True, "primary": False, "source_type": "rss", "name": "Old RSS"},
        {"total": 8, "r24": 0, "r72": 2, "matched24": 0}, None, now=now,
        transport={"status": "ok", "finished_at": "2026-07-25T00:00:00+00:00"},
    )
    assert status == "STALE"
